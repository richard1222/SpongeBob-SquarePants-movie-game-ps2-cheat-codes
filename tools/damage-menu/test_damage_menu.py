from pathlib import Path
import struct,json,itertools,hashlib,argparse
parser=argparse.ArgumentParser(description='Emitted-instruction tests; supply your matching original retail ELF.')
parser.add_argument('elf',type=Path)
args=parser.parse_args()
P=Path(__file__).resolve().parent;s=json.loads((P/'DEVELOPER-SPEC.json').read_text());b=args.elf.read_bytes();L=s['labels']
assert hashlib.sha256(b).hexdigest()==s['elf_sha256'], 'Wrong retail ELF'
words={p['base']+i*4:w for p in s['blocks'].values() for i,w in enumerate(p['words'])}
for va in range(0x2bf7e0,0x2bf900,4):words[va]=struct.unpack_from('<I',b,va-0xfff80)[0]
STOP={0x4a9300,0x4a97b8};MASK=(1<<64)-1
def valid(p):return p%4==0 and 0x100000<=p<0x1fff000
def run(state,pressed,paused=0,pad=True,chain=(0x701000,0x702000,0x703000),scene=0x704000,sceneid=0x42423032,handles=(101,202),damage=1):
 r=[0]*32;r[28]=0x63dbf0;r[29]=0x800000;r[31]=0x12345678
 mem={0x7abb20:damage,0x7ab520:0x700000 if pad else 0,0x700030:pressed,0x70002c:0x12345678,0x6378f8:state,0x673670:paused,0x673620:handles[0]&0xffffffff,0x673644:handles[1]&0xffffffff,0x636928:chain[0],0x7ab920:scene}
 for a,v in [(chain[0]+0x80c,chain[1]),(chain[1]+0x48,chain[2]),(scene,sceneid)]:
  if a not in mem:mem[a]=v
 pc=L['driver'];pending=None;formats=[];calls=[];audio=[]
 for steps in range(1800):
  if pc in STOP:return {'damage':mem[0x7abb20],'state':mem[0x6378f8],'paused':mem[0x673670],'formats':formats,'calls':calls,'audio':audio,'exit':pc}
  if pc in (0x11ac28,0x454d70,0x2e0690,0x2e0720):
   result=0
   if pc==0x11ac28:
    formats.append(tuple(r[4:12]))
    if r[5]==L['format']:assert r[4]==0x800260
    elif r[5]==L['pad_format']:assert r[4]==0x800180
    else:raise AssertionError(('unexpected printf',hex(r[5])))
   elif pc==0x454d70:audio.append((r[4]&0xffffffff,r[5]))
   elif pc==0x2e0690:
    assert all(valid(x) for x in chain),chain;calls.append('position');result=0x67ff70
   else:
    assert valid(scene) and sceneid,scene;calls.append('scene');result=0x67ff30
   ra=r[31]
   for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25]:r[i]=0xdead0000+i
   r[2]=result;pc=ra;pending=None;continue
  assert pc in words,hex(pc)
  w=words[pc];op=w>>26;rs=w>>21&31;rt=w>>16&31;rd=w>>11&31;sa=w>>6&31;im=w&65535;si=im if im<32768 else im-65536;nxt=None
  if op==15:r[rt]=(im<<16)&MASK
  elif op in (35,36,55,30):
   a=(r[rs]+si)&0xffffffff;assert a in mem,('unexpected load',hex(pc),hex(a));r[rt]=mem[a]
   if op==36:r[rt]&=255
  elif op in (43,40,63,31):mem[(r[rs]+si)&0xffffffff]=r[rt]&(255 if op==40 else MASK)
  elif op==9:r[rt]=(r[rs]+si)&0xffffffff
  elif op==11:r[rt]=int((r[rs]&0xffffffff)<(si&0xffffffff))
  elif op==12:r[rt]=r[rs]&im
  elif op==14:r[rt]=r[rs]^im
  elif op in (4,5):
   if (r[rs]==r[rt])==(op==4):nxt=pc+4+si*4
  elif op==1:
   assert rt==1
   if (r[rs]&0x80000000)==0:nxt=pc+4+si*4
  elif op in (2,3):
   nxt=(pc+4)&0xf0000000|(w&0x3ffffff)<<2
   if op==3:r[31]=pc+8
  elif w==0:pass
  elif w==0x03e00008:nxt=r[31]
  elif op==0:
   fn=w&63
   if fn==0x2d:r[rd]=(r[rs]+r[rt])&MASK
   elif fn==0x24:r[rd]=r[rs]&r[rt]
   elif fn==0x25:r[rd]=r[rs]|r[rt]
   elif fn==0x26:r[rd]=r[rs]^r[rt]
   elif fn==2:r[rd]=(r[rt]&0xffffffff)>>sa
   elif fn==4:r[rd]=(r[rt]<<(r[rs]&31))&0xffffffff
   else:raise AssertionError((hex(pc),hex(w)))
  else:raise AssertionError((hex(pc),hex(w)))
  r[0]=0;old=pending;pending=nxt;pc=old if old is not None else pc+4
 raise AssertionError('Instruction limit')

def expected(state,pressed,pad):
 p=pressed if pad else 0;st=state^(1 if p&2 else 0);action=False
 if st&1:
  row=(st>>1)&3
  if p&0x50==0x10:row=(row-1)%4
  elif p&0x50==0x40:row=(row+1)%4
  st=(st&0x19)|(row<<1)
  if p&0x10000:
   if row==0:action=True
   elif row<3:st^=4<<row
 return st,action

# Explicit restoration and isolation, including noncanonical incoming flags.
for d in [0,1,2,0xffffffff]:
 a=run(7,0x10000,damage=d);assert a['damage']==int(d==0)
 a=run(7,0x10000,damage=a['damage']);assert a['damage']==int(d!=0)
 for st in [0,1,3,5,6]:
  a=run(st,0x10000,damage=d);assert a['damage']==d
for st in range(32):
 a=run(st,0,damage=1);assert a['damage']==1

count=0
states=[v|(row<<1)|flags for v,row,flags in itertools.product([0,1],range(4),[0,8,16,24])]
presses=[0,1,2,0x10,0x40,0x50,0x10000,0x10010,0x10040,0x10002,0x12,0x42,0x40000]
for state,pressed,pad,paused,handles in itertools.product(states,presses,[False,True],[0,1],[(-1,-1),(101,-1),(-1,202),(101,202)]):
 a=run(state,pressed,paused,pad,handles=handles);st,act=expected(state,pressed,pad);mu=paused^act
 assert (a['state'],a['paused'])==(st,mu),(state,pressed,pad,a,st,mu)
 assert a['audio']==([(h&0xffffffff,mu) for h in handles if h!=-1] if act else [])
 if st&1:
  last=a['formats'][-1];assert last[1]==L['format'] and last[2]==((st>>1)&3)+1
  assert last[3]==L['paused' if mu else 'playing']
  assert last[4]==(0x67ff70 if st&8 else L['off'])
  assert last[5]==(0x67ff30 if st&16 else L['off'])
  assert last[7]==(0 if pad and pressed&0x10000 and (st>>1&3)==3 else 1)
  assert last[6]==(0x800180 if st&16 else L['blank'])
  assert a['calls']==(['position'] if st&8 else [])+(['scene'] if st&16 else [])
  if st&16:assert a['formats'][0][2:4]==(0x12345678 if pad else 0,pressed if pad else 0)
 else:assert not a['formats'] and not a['calls']
 count+=1

guardcases=0
for bad in [0,1,0xffffc,0x100001,0x1fff000,0x1fffffc,0x2000000,0xffffffff]:
 for index in range(3):
  chain=[0x701000,0x702000,0x703000];chain[index]=bad
  a=run(9,0,chain=tuple(chain));assert not a['calls'] and a['formats'][-1][4]==L['na'];guardcases+=1
 a=run(17,0,scene=bad);assert not a['calls'] and a['formats'][-1][5]==L['na'];guardcases+=1
a=run(17,0,sceneid=0);assert not a['calls'];guardcases+=1
for good in [0x100000,0x100004,0x1ffeffc]:
 a=run(25,0,chain=(good,0x702000,0x703000),scene=0x704000);assert a['calls']==['position','scene'];guardcases+=1

st,mu=1,0
sequence=[0x10000,0x40,0x10000,0x40,0x10000,2,0x10000,2,0x40,0x10000,0x10,0x10]
for p in sequence:
 ex,act=expected(st,p,True);a=run(st,p,mu);assert a['state']==ex and a['paused']==(mu^act);st,mu=ex,mu^act

# Confirm all replaced code/data lies in the file-backed read/write/execute PT_LOAD.
phoff=struct.unpack_from('<I',b,28)[0];psz,pnum=struct.unpack_from('<HH',b,42)
loads=[struct.unpack_from('<8I',b,phoff+i*psz) for i in range(pnum)]
for patch in s['patches']:
 va=patch['va'];n=len(bytes.fromhex(patch['new']))
 assert any(t==1 and flags&7==7 and v<=va and va+n<=v+fs for t,off,v,pa,fs,ms,flags,al in loads)
assert len(bytes.fromhex(s['patches'][0]['new']))==64
receipt={'instruction_cases':count,'pointer_guard_cases':guardcases,'interaction_steps':len(sequence),'retail_music_instructions_executed':True,'position_scene_and_sound_backend':'external calls modeled; retail position/scene bodies inspected statically','hardware_tested':False,'damage_flag_hardware_tested':False,'source_music_hardware':'owner reported it worked on CFW PS3 on 2026-10-22'}
print('PASS',json.dumps(receipt))
