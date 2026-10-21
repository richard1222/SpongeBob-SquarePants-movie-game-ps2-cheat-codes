# Run only in an isolated container: Xvfb TCP access control is disabled.
# Uses a dedicated test profile and sends Start/A periodically; not a gameplay assertion.
import subprocess,os,socket,time
from pathlib import Path
from Xlib import display,X,XK
from Xlib.ext import xtest
from PIL import Image
import argparse
parser = argparse.ArgumentParser(description="Isolated Linux container Dolphin smoke test (TCP Xvfb).")
parser.add_argument("build_dir", type=Path, help="Contains xruntime, squashfs-root and dolphin-smoke-user")
parser.add_argument("disc", type=Path)
parser.add_argument("--frames", type=int, default=30)
parser.add_argument("--output", type=Path, default=Path("dolphin-test-output"))
args = parser.parse_args()
base = args.build_dir.resolve()
args.output.mkdir(parents=True, exist_ok=True)
(base / 'dolphin-smoke-user/Config').mkdir(parents=True, exist_ok=True)
(base/'dolphin-smoke-user/Config/Dolphin.ini').write_text('[Analytics]\nEnabled = False\nPermissionAsked = True\n[Interface]\nConfirmStop = False\n[Core]\nEnableCheats = False\n')
(base/'dolphin-smoke-user/Config/GCPadNew.ini').write_text('[GCPad1]\nDevice = XInput2/0/Virtual core pointer\nButtons/A = X\nButtons/B = Z\nButtons/Start = Return\nMain Stick/Up = W\nMain Stick/Down = S\nMain Stick/Left = A\nMain Stick/Right = D\nD-Pad/Up = Up\nD-Pad/Down = Down\nD-Pad/Left = Left\nD-Pad/Right = Right\n')
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(base/'xruntime/usr/lib/x86_64-linux-gnu')
x=subprocess.Popen([str(base/'xruntime/usr/bin/Xvfb'),':101','-screen','0','1024x768x24','-ac','-nolisten','unix','-nolisten','local','-listen','tcp'],env=env,stdout=open(args.output/'xvfb.log','w'),stderr=subprocess.STDOUT)
p=None
try:
 for i in range(50):
  try:s=socket.create_connection(('127.0.0.1',6101),timeout=.2);s.close();break
  except OSError:time.sleep(.2)
 env=os.environ.copy();env.update(DISPLAY='127.0.0.1:101',QT_QPA_PLATFORM='xcb',LIBGL_ALWAYS_SOFTWARE='1')
 p=subprocess.Popen([str(base/'squashfs-root/AppRun'),'-u',str(base/'dolphin-smoke-user'),'-b','-v','OGL','-C','Dolphin.DSP.Backend=Null','-e',str(args.disc.resolve())],env=env,stdout=open(args.output/'dolphin.log','w'),stderr=subprocess.STDOUT)
 d=display.Display('127.0.0.1:101');root=d.screen().root
 for step in range(args.frames):
  time.sleep(10)
  for w in root.query_tree().children:
   try:
    if w.get_attributes().map_state==X.IsViewable:w.set_input_focus(X.RevertToParent,X.CurrentTime)
   except Exception:pass
  if step>=2:
   key=d.keysym_to_keycode(XK.string_to_keysym('Return' if step%2==0 else 'x'))
   xtest.fake_input(d,X.KeyPress,key);d.sync();time.sleep(.15);xtest.fake_input(d,X.KeyRelease,key);d.sync()
  raw=root.get_image(0,0,1024,768,X.ZPixmap,0xffffffff)
  Image.frombytes('RGB',(1024,768),raw.data,'raw','BGRX').save(args.output/('frame-%02d.png'%step))
  print('frame',step,'process',p.poll(),flush=True)
  if p.poll() is not None:break
finally:
 for child in (p,x):
  if child is not None:
   child.terminate()
   try: child.wait(timeout=5)
   except subprocess.TimeoutExpired:
    child.kill()
    child.wait()
