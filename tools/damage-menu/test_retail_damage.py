from pathlib import Path
import struct,json,hashlib,argparse
parser=argparse.ArgumentParser(description='Test actual retail health-decrement instructions.')
parser.add_argument('elf',type=Path)
args=parser.parse_args()
b=args.elf.read_bytes()
assert hashlib.sha256(b).hexdigest()=='2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956','Wrong retail ELF'
def run(flag,health,amount):
 r=[0]*32;r[4]=0x900460;r[16]=amount
 mem={0x7abb20:flag,0x7abc10:0x900000,0x900460:health};pc=0x32b774;pending=None;writes=[]
 for _ in range(40):
  if pc in (0x32b784,0x32baf8):return mem[0x900460],writes
  w=struct.unpack_from('<I',b,pc-0xfff80)[0];op=w>>26;rs=w>>21&31;rt=w>>16&31;rd=w>>11&31;im=w&65535;si=im if im<32768 else im-65536;nxt=None
  if op==15:r[rt]=im<<16
  elif op==35:r[rt]=mem[(r[rs]+si)&0xffffffff]
  elif op==43:
   a=(r[rs]+si)&0xffffffff;mem[a]=r[rt];writes.append(a)
  elif op in (4,5):
   if (r[rs]==r[rt])==(op==4):nxt=pc+4+si*4
  elif op==0 and w&63==0x23:r[rd]=(r[rs]-r[rt])&0xffffffff
  elif w==0:pass
  else:raise AssertionError(hex(w))
  r[0]=0;old=pending;pending=nxt;pc=old if old is not None else pc+4
 raise AssertionError('did not reach post-damage continuation')
count=0
for flag in [0,1,2,0xffffffff]:
 for health in [1,3,6,10]:
  for amount in range(health+1):
   actual,writes=run(flag,health,amount)
   assert actual==(health-amount if flag else health)
   assert writes==([0x900460] if flag else [])
   count+=1
print(json.dumps({'retail_damage_subtraction_cases':count,'entry':'0x0032B774','subtraction':'0x0032BAE8','stop_addresses':['0x0032B784','0x0032BAF8'],'scope':'actual retail instructions around one health-decrement branch; not all damage/death paths','hardware_tested':False}))
