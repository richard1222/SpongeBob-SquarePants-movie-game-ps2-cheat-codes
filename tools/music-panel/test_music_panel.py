from pathlib import Path
import json,struct,hashlib
s=json.loads(Path(__file__).with_name('MusicPatch.json').read_text()); base=0x4a9240; textbase=0x62f012; driver=next(p for p in s['patches'] if p['va']==base); s['code']=list(struct.unpack('<48I',bytes.fromhex(driver['new']))); s['helper_va']=0x403bb8; wrapper=bytes.fromhex(next(p for p in s['patches'] if p['va']==0x403bb0)['new']); s['helper_words']=list(struct.unpack('<8I',wrapper[8:40])); text=bytes.fromhex(next(p for p in s['patches'] if p['va']==textbase)['new']); offsets={'none':text.index(b' \0'),'selected':text.index(b'>\0'),'off':text.index(b'PLAYING\0'),'on':text.index(b'PAUSED\0')}
import sys
if len(sys.argv)!=2: raise SystemExit('Usage: python test_music_panel.py path/to/SLUS_209.04 (your privately extracted USA executable)')
b=Path(sys.argv[1]).read_bytes();assert hashlib.sha256(b).hexdigest()=='2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956'
words={base+i*4:w for i,w in enumerate(s['code'])};words.update({s['helper_va']+i*4:w for i,w in enumerate(s['helper_words'])})
# Execute the real retail music pause/resume functions as well as the new driver/helper.
for va in range(0x2bf7e0,0x2bf900,4):words[va]=struct.unpack_from('<I',b,va-0xfff80)[0]
def run(state,pressed,paused,ptr=True,handles=(101,202)):
 regs=[0]*32;regs[28]=0x63dbf0;regs[29]=0x800000;regs[31]=0x12345678
 mem={0x7ab520:0x700000 if ptr else 0,0x6378f8:state,0x700030:pressed,0x673670:paused,0x673620:handles[0]&0xffffffff,0x673644:handles[1]&0xffffffff}
 pc=base;pending=None;formats=[];audio=[]
 for steps in range(800):
  if pc in (0x4a97b8,0x4a9300):return mem[0x6378f8],mem[0x673670],formats[0] if formats else None,audio
  if pc in (0x11ac28,0x454d70):
   if pc==0x11ac28:formats.append(tuple(regs[i] for i in [4,5,6,7]))
   else:audio.append((regs[4],regs[5]))
   ra=regs[31]
   # External functions may overwrite caller-saved registers.
   for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25]:regs[i]=0xdead0000+i
   pc=ra;pending=None;continue
  assert pc in words,hex(pc)
  w=words[pc];op=w>>26;rs=w>>21&31;rt=w>>16&31;rd=w>>11&31;im=w&65535;si=im if im<32768 else im-65536;nxt=None
  if op==15:regs[rt]=im<<16
  elif op in (35,36,55,30):
   addr=(regs[rs]+si)&0xffffffff;assert addr in mem,(hex(pc),hex(addr));regs[rt]=mem[addr]
   if op==36:regs[rt]&=255
  elif op in (43,40,63,31):mem[(regs[rs]+si)&0xffffffff]=regs[rt]&(255 if op==40 else 0xffffffffffffffffffffffffffffffff)
  elif op==9:regs[rt]=(regs[rs]+si)&0xffffffff
  elif op==11:regs[rt]=int(regs[rs]<(si&0xffffffff))
  elif op==12:regs[rt]=regs[rs]&im
  elif op==14:regs[rt]=regs[rs]^im
  elif op in (4,5):
   condition=regs[rs]==regs[rt]
   if condition==(op==4):nxt=pc+4+si*4
  elif op in (2,3):
   nxt=(pc+4)&0xf0000000|(w&0x3ffffff)<<2
   if op==3:regs[31]=pc+8
  elif w==0:pass
  elif w==0x03e00008:nxt=regs[31]
  elif op==0 and w&63==0x2d:regs[rd]=(regs[rs]+regs[rt])&0xffffffff
  elif op==0 and w&63==0x24:regs[rd]=regs[rs]&regs[rt]
  else:raise AssertionError((hex(pc),hex(w)))
  regs[0]=0;old=pending;pending=nxt;pc=old if old is not None else pc+4
 raise AssertionError('Instruction limit')
count=0
for ptr in [False,True]:
 for state in range(4):
  for paused in [0,1]:
   for handles in [(-1,-1),(101,-1),(-1,202),(101,202)]:
    for pressed in [0,1,2,0x10,0x40,0x50,0x10000,0x10010,0x10002,0x40000,0x12,0x42]:
     p=pressed if ptr else 0;st=state^(1 if p&2 else 0);mu=paused;did=False
     if st&1:
      if p&0x50:st^=2
      if p&0x10000 and st&2:mu^=1;did=True
     actual=run(state,pressed,paused,ptr,handles)
     expectedcalls=[(h,mu) for h in handles if h!=-1] if did else []
     assert actual[0]==st and actual[1]==mu and actual[3]==expectedcalls,(state,pressed,paused,ptr,handles,actual,st,mu,expectedcalls)
     if st&1:assert actual[2]==(0x800260,textbase,textbase+offsets['selected' if st&2 else 'none'],textbase+offsets['on' if mu else 'off']),actual
     else:assert actual[2] is None
     count+=1
st,mu=1,0
for p,exp in [(0x10,(3,0)),(0x10000,(3,1)),(2,(2,1)),(0x10000,(2,1)),(2,(3,1)),(0x10000,(3,0)),(0x40,(1,0)),(0x10000,(1,0))]:
 result=run(st,p,mu);st,mu=result[:2];assert (st,mu)==exp
print('PASS',count,'driver/helper/retail-function cases and 8-step sequence; sound backend modeled, not executed')
