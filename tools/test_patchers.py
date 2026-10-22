"""v0.2 patcher regressions. Fixtures need Windows PowerShell, not game data."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, tempfile

# This regression harness uses assertions for its safety checks. Under python -O
# they are stripped, so refuse to run rather than print a misleading PASS.
if not __debug__:
    raise RuntimeError('Run regression tests without Python optimization (-O / PYTHONOPTIMIZE).')

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--iso-dir', type=Path, help='Optional directory containing stage ISO inputs')
    parser.add_argument('--original-iso', type=Path, help='Original USA ISO for full stage checks')
    parser.add_argument('--work-dir', type=Path, default=Path(tempfile.gettempdir()))
    args=parser.parse_args()
    base=args.work_dir.resolve();base.mkdir(parents=True,exist_ok=True)
    scratch=Path(tempfile.mkdtemp(prefix='spongebob-v02-tests-',dir=base)).resolve()
    assert scratch.parent==base and scratch.name.startswith('spongebob-v02-tests-')
    tools=Path(__file__).resolve().parent
    stages=json.loads((tools/'STAGES.json').read_text())
    template=(tools/'health-menu/Apply-HealthMenu.ps1').read_bytes()
    source=bytes(range(256))*16;expected=bytearray(source);expected[16:20]=b'ABCD'
    initial={'input_sha256':hashlib.sha256(source).hexdigest(),'output_sha256':hashlib.sha256(expected).hexdigest(),'patches':[{'iso_offset':16,'old':source[16:20].hex(),'new':b'ABCD'.hex()}]}
    results=[]
    try:
        cases=['success','wrong source','old bytes','offset bounds','negative offset','fractional offset','overlap','bad hex','odd hex','length mismatch','output mismatch cleanup','existing output','same input output','hash cmdlet unavailable']
        for index,case in enumerate(cases):
            folder=scratch/('fixture '+str(index));folder.mkdir()
            script=folder/'Apply-HealthMenu.ps1';script.write_bytes(template)
            inp=folder/'source space.iso';inp.write_bytes(source)
            dest=folder/'output space.iso'
            spec=json.loads(json.dumps(initial));want='';success=case in ['success','hash cmdlet unavailable']
            if case=='wrong source':spec['input_sha256']='0'*64;want='Wrong source'
            elif case=='old bytes':spec['patches'][0]['old']='00000000';want='Source code guard'
            elif case=='offset bounds':spec['patches'][0]['iso_offset']=len(source);want='offset'
            elif case=='negative offset':spec['patches'][0]['iso_offset']=-1;want='offset'
            elif case=='fractional offset':spec['patches'][0]['iso_offset']=16.5;want='integer'
            elif case=='overlap':spec['patches'].append({'iso_offset':18,'old':source[18:22].hex(),'new':'45464748'});want='overlap'
            elif case=='bad hex':spec['patches'][0]['new']='zzzzzzzz';want='hex'
            elif case=='odd hex':spec['patches'][0]['new']='123';want='hex'
            elif case=='length mismatch':spec['patches'][0]['new']='1234';want='lengths differ'
            elif case=='output mismatch cleanup':spec['output_sha256']='0'*64;want='Output hash mismatch'
            elif case=='existing output':dest.write_bytes(b'KEEP THIS');want='already exists'
            elif case=='same input output':dest=inp;want='different files'
            (folder/'HealthMenuPatch.json').write_text(json.dumps(spec))
            command=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),'-InputIso',str(inp),'-OutputIso',str(dest)]
            if case=='hash cmdlet unavailable':
                wrapper=folder/'hash compatibility.ps1'
                wrapper.write_text('param($ToolPath,$FixtureInput,$FixtureOutput)\nfunction Get-FileHash { throw "Get-FileHash is unavailable in this test" }\n& $ToolPath -InputIso $FixtureInput -OutputIso $FixtureOutput\nexit $LASTEXITCODE\n')
                command=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(wrapper),str(script),str(inp),str(dest)]
            r=subprocess.run(command,capture_output=True,text=True)
            log=r.stdout+r.stderr
            assert (r.returncode==0)==success,(case,r.returncode,log)
            assert inp.read_bytes()==source,(case,'source changed')
            if success:assert dest.read_bytes()==expected,(case,'wrong output')
            elif case=='existing output':assert dest.read_bytes()==b'KEEP THIS'
            elif case!='same input output':assert not dest.exists(),(case,'failed final output left behind')
            if want:assert want.lower() in log.lower(),(case,log)
            assert not list(folder.glob('*.partial')) and not list(folder.glob('.*.partial')),(case,'temporary output left behind')
            results.append(case)
        full=[]
        if args.iso_dir:
            for stage in stages:
                inp=(args.original_iso if stage['folder']=='overlay' and args.original_iso else args.iso_dir/stage['input_name']).resolve()
                assert sha(inp)==stage['input_sha256'],('wrong stage fixture',stage['folder'])
                dest=scratch/stage['output_name']
                script=tools/stage['folder']/stage['script']
                r=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),'-InputIso',str(inp),'-OutputIso',str(dest)],capture_output=True,text=True)
                assert r.returncode==0,(stage['folder'],r.stdout+r.stderr)
                assert dest.stat().st_size==inp.stat().st_size and sha(dest)==stage['output_sha256']
                assert sha(inp)==stage['input_sha256'],'source changed'
                full.append({'stage':stage['folder'],'output_sha256':stage['output_sha256'],'bytes':dest.stat().st_size})
                dest.unlink()
        print(json.dumps({'fixture_cases_passed':len(results),'fixtures':results,'full_iso_stages':full,'hardware_validation':'not performed by this tool'},indent=2))
    finally:
        # Only remove this newly created, checked test directory.
        assert scratch.resolve().parent==base and scratch.name.startswith('spongebob-v02-tests-')
        shutil.rmtree(scratch)

if __name__=='__main__':main()
