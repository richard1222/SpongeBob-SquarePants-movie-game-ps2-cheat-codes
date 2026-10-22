"""Execute retail and patched health callbacks; external UI/hash calls are modeled."""
from pathlib import Path
import argparse,hashlib,json,struct

if not __debug__:raise RuntimeError('Run without -O / PYTHONOPTIMIZE.')
BIAS=0xfff80
ELF_SHA='2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956'
RETURN=0xbadf00d
PLAYER=0x710000

def run(image,health,maximum,count,flow_exists,flow_state):
    regs=[0x1000+i for i in range(32)];regs[0]=0;regs[28]=0x63dbf0;regs[29]=0x1001000;regs[31]=RETURN
    saved=regs[16:24]+[regs[28],regs[29],regs[30]]
    mem={};writes=[];calls=[];pending=None;pc=0x2d2620
    def put(addr,value,size=4,record=False):
        for index in range(size):mem[addr+index]=(value>>(8*index))&255
        if record:writes.append((addr,size))
    def get(addr,size=4,signed=False):
        if any(addr+i not in mem for i in range(size)):raise AssertionError(('unmapped read',hex(pc),hex(addr),size))
        value=sum(mem[addr+i]<<(8*i) for i in range(size))
        return value-(1<<(8*size)) if signed and value>>(8*size-1) else value
    for addr,value in [(0x7ac084,3),(0x7ac4f4,3),(0x636528,count),(0x63652c,0x720000),(0x7abc10,PLAYER),(PLAYER+0x460,health),(PLAYER+0x464,maximum)]:put(addr,value)
    put(0x7abc01,0,1);put(0x7abc02,0,1);put(0x7acfe8,7,2)
    for index,(key,kind,obj) in enumerate([(10,10,0x730000),(123,11,0x731000),(9,10,0x732000),(10,10,0)]):
        base=0x5fc510+16*index
        for off,value in [(0,key),(4,0),(8,kind),(12,obj)]:put(base+off,value)
        if obj:put(obj+0x14,0x1234,2)
        put(0x7abbf9+kind,4,1)
    put(0x740014,flow_state&65535,2)
    for _ in range(1800):
        if pc==RETURN:
            assert regs[16:24]+[regs[28],regs[29],regs[30]]==saved,'callee-saved register or stack changed'
            return {'hp':get(PLAYER+0x460),'max':get(PLAYER+0x464),'slots':(get(0x7ac084),get(0x7ac4f4)),'bonus':(get(0x7abc01,1),get(0x7abc02,1)),'memory':mem,'writes':writes,'calls':calls}
        if pc in [0x44dea0,0x2eed90,0x3eb940]:
            ra=regs[31]
            if pc==0x44dea0:
                assert regs[4]==0x61fec4,('flow string changed',hex(regs[4]));result=0xbeef;calls.append(('hash',regs[4]))
            elif pc==0x2eed90:
                assert regs[4]==0xbeef;result=0x740000 if flow_exists else 0;calls.append(('lookup',regs[4]))
            else:
                assert regs[4:6]==[0x720000,0x3c];result=0;calls.append(('confirm',regs[4],regs[5]))
            for index in [1,2,3,*range(4,16),24,25]:regs[index]=0xdead0000+index
            regs[2]=result;pc=ra;pending=None;continue
        assert 0x2d2620<=pc<0x2d2730 or 0x10f06c<=pc<0x10f080,hex(pc)
        word=struct.unpack_from('<I',image,pc-BIAS)[0];op=word>>26;rs=word>>21&31;rt=word>>16&31;rd=word>>11&31;im=word&65535;si=im if im<32768 else im-65536;nxt=None
        if op==15:regs[rt]=im<<16
        elif op==9:regs[rt]=(regs[rs]+si)&0xffffffff
        elif op in [35,36,33,55]:
            size={35:4,36:1,33:2,55:8}[op];regs[rt]=get((regs[rs]+si)&0xffffffff,size,op in [35,33])&0xffffffffffffffff
        elif op in [43,40,41,63]:put((regs[rs]+si)&0xffffffff,regs[rt],{43:4,40:1,41:2,63:8}[op],True)
        elif op in [4,5]:
            if (regs[rs]==regs[rt])==(op==4):nxt=pc+4+si*4
        elif op==3:regs[31]=pc+8;nxt=(pc+4)&0xf0000000|(word&0x3ffffff)<<2
        elif op==14:regs[rt]=regs[rs]^im
        elif op==11:regs[rt]=int((regs[rs]&0xffffffff)<(si&0xffffffff))
        elif word==0:pass
        elif op==0:
            fn=word&63
            if fn in [0x21,0x2d]:regs[rd]=(regs[rs]+regs[rt])&0xffffffffffffffff
            elif fn==0x2b:regs[rd]=int(regs[rs]<regs[rt])
            elif fn==8:nxt=regs[rs]
            else:raise AssertionError(('unsupported R instruction',hex(pc),hex(word)))
        else:raise AssertionError(('unsupported instruction',hex(pc),hex(word)))
        assert not (pending is not None and nxt is not None),'control transfer in a delay slot'
        regs[0]=0;old=pending;pending=nxt;pc=old if old is not None else pc+4
    raise AssertionError('instruction limit')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('elf',type=Path)
    parser.add_argument('--patched-iso',type=Path,help='Optionally verify and compare the built image too')
    args=parser.parse_args()
    original=args.elf.read_bytes();assert hashlib.sha256(original).hexdigest()==ELF_SHA,'Wrong retail ELF'
    at=0x61fec4-BIAS
    assert original[at:original.index(b'\0',at)]==b'PAUSESTATE MENU OR POWERUP COUNTER'
    spec=json.loads(Path(__file__).with_name('HealthRefillPatch.json').read_text());patched=bytearray(original)
    for item in spec['patches']:
        at=item['va']-BIAS;old=bytes.fromhex(item['old']);new=bytes.fromhex(item['new'])
        assert original[at:at+len(old)]==old;assert len(old)==len(new);patched[at:at+len(new)]=new
    assert hashlib.sha256(patched).hexdigest()=='1175a8d7650a7c2a01cb76a955e23f00a73a8847f0d88f277ab6c0547a30b492'
    if args.patched_iso:
        with args.patched_iso.open('rb') as stream:
            assert hashlib.file_digest(stream,'sha256').hexdigest()==spec['output_sha256'],'Wrong candidate ISO'
            first=spec['patches'][0]
            stream.seek(first['iso_offset']-(first['va']-BIAS))
            assert stream.read(len(original))==patched,'ISO executable differs from modeled bytes'
    count_cases=0
    for maximum in [3,6]:
        for hp in range(maximum+1):
            for count in [0,1,2,4]:
                for flow_exists in [False,True]:
                    for state in [0,1,2,3]:
                        before=run(original,hp,maximum,count,flow_exists,state);after=run(patched,hp,maximum,count,flow_exists,state)
                        assert before['hp']==hp and after['hp']==(maximum if count else hp)
                        assert before['slots']==after['slots']==(6,6) and before['bonus']==after['bonus']==(3,3)
                        assert before['max']==after['max']==maximum
                        assert before['calls']==after['calls']
                        assert any(c[0]=='confirm' for c in after['calls'])==(flow_exists and state==2)
                        def halfword(addr):return after['memory'][addr]|after['memory'][addr+1]<<8
                        assert halfword(0x730014)==(7 if count>=1 else 0x1234)
                        assert halfword(0x731014)==(4 if count>=2 else 0x1234)
                        assert halfword(0x732014)==0x1234
                        ignored=set(range(PLAYER+0x460,PLAYER+0x464))
                        assert {a:v for a,v in before['memory'].items() if a not in ignored}=={a:v for a,v in after['memory'].items() if a not in ignored}
                        hpwrites=[w for w in after['writes'] if w[0]==PLAYER+0x460]
                        assert len(hpwrites)==int(count>0)
                        count_cases+=1
    print(json.dumps({'callback_comparison_cases':count_cases,'retail_and_patched_runs':2*count_cases,'register_stack_return_preserved':True,'slot_bonus_ui_effects_preserved':True,'flow_confirm_condition':'object exists and state equals 2','zero_table_count_skips_refill':True,'built_iso_bytes_verified':bool(args.patched_iso),'external_hash_lookup_ui_calls':'modeled; UI function bodies not executed','hardware_tested':False},indent=2))

if __name__=='__main__':main()
