import json,struct
from pathlib import Path
s=json.loads(Path(__file__).with_name('PanelPatch.json').read_text()); driver=next(p for p in s['patches'] if p['va']==0x4a9240); code=list(struct.unpack('<48I',bytes.fromhex(driver['new']))); base=0x4a9240; textbase=0x62f012; labels={'exit':0x4a97b8}; text=bytes.fromhex(next(p for p in s['patches'] if p['va']==textbase)['new']); offsets={'none':text.index(b' \0'),'selected':text.index(b'>\0'),'off':text.index(b'OFF\0'),'on':text.index(b'ON\0')}
def run(state,pressed,ptr=True):
 regs=[0]*32;regs[28]=0x63dbf0;regs[29]=0x800000;regs[31]=0x12345678
 mem={0x7ab520:0x700000 if ptr else 0,0x6378f8:state,0x700030:pressed};pc=base;pending=None; calls=[]
 for steps in range(200):
  if pc==0x4a97b8:return mem[0x6378f8],None
  if pc==0x4a9300:return mem[0x6378f8],calls[0]
  if pc==0x11ac28:
   calls.append((regs[4],regs[5],regs[6],regs[7]));pc=regs[31];pending=None;continue
  assert base<=pc<base+len(code)*4,hex(pc)
  w=code[(pc-base)//4];op=w>>26;rs=w>>21&31;rt=w>>16&31;rd=w>>11&31;im=w&65535;si=im if im<32768 else im-65536;nxt=None
  if op==15:regs[rt]=im<<16
  elif op==35:regs[rt]=mem[(regs[rs]+si)&0xffffffff]
  elif op==43:mem[(regs[rs]+si)&0xffffffff]=regs[rt]
  elif op==9:regs[rt]=(regs[rs]+si)&0xffffffff
  elif op==12:regs[rt]=regs[rs]&im
  elif op==14:regs[rt]=regs[rs]^im
  elif op==4:
   if regs[rs]==regs[rt]:nxt=pc+4+si*4
  elif op in (2,3):
   nxt=(pc+4)&0xf0000000|(w&0x3ffffff)<<2
   if op==3:regs[31]=pc+8
  elif w==0:pass
  elif op==0 and w&63==0x2d:regs[rd]=regs[rs]+regs[rt]
  elif op==0 and w&63==0x24:regs[rd]=regs[rs]&regs[rt]
  else:raise AssertionError(hex(w))
  regs[0]=0;old=pending;pending=nxt;pc=old if old is not None else pc+4
 raise AssertionError('Instruction limit')
count=0
for ptr in [False,True]:
 for state in range(8):
  for pressed in [0,1,2,0x10,0x40,0x50,0x10000,0x10010,0x10002,0x40000,0x12,0x42]:
   expected=state;p=pressed if ptr else 0
   if p&2:expected^=1
   if expected&1:
    if p&0x50:expected^=2
    if p&0x10000 and expected&2:expected^=4
   actual,call=run(state,pressed,ptr)
   assert actual==expected,(state,pressed,ptr,actual,expected)
   if expected&1:
    assert call==(0x800260,textbase,textbase+offsets['selected' if expected&2 else 'none'],textbase+offsets['on' if expected&4 else 'off']),call
   else:assert call is None
   count+=1
# Multi-action interaction sequence.
state=1
for pressed,expected in [(0x10,3),(0x10000,7),(2,6),(0x10000,6),(2,7),(0x40,5),(0x10000,5),(0x10,7),(0x10000,3)]:
 state,_=run(state,pressed);assert state==expected,(pressed,state,expected)
print('PASS',count,'instruction cases and 9-step interaction sequence')
