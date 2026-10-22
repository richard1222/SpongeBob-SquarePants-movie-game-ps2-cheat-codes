"""Check actual combined ISO bytes and execute menu/refill instruction cases."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,runpy,struct,sys

if not __debug__:
    raise RuntimeError('Run without -O / PYTHONOPTIMIZE.')
BIAS=0xFFF80
HERE=Path(__file__).resolve().parent

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('retail_elf',type=Path)
    parser.add_argument('--health-menu-iso',required=True,type=Path)
    parser.add_argument('--combined-iso',required=True,type=Path)
    args=parser.parse_args()
    retail=args.retail_elf.read_bytes()
    assert hashlib.sha256(retail).hexdigest()=='2ff117f45e80be5e2d73b6c952f4b5adfb8d359c8cc6c14eb5906197994ce956'
    spec=json.loads((HERE/'HealthMenuRefillPatch.json').read_text())
    assert sha(args.health_menu_iso)==spec['input_sha256'],'Wrong HealthMenu source'
    assert sha(args.combined_iso)==spec['output_sha256'],'Wrong combined ISO'
    first=spec['patches'][0]
    elf_offset=first['iso_offset']-(first['va']-BIAS)
    def extract(path):
        with path.open('rb') as f:f.seek(elf_offset);return f.read(len(retail))
    baseline=extract(args.health_menu_iso)
    combined=extract(args.combined_iso)
    expected=bytearray(baseline)
    spans=[]
    for patch in spec['patches']:
        at=patch['va']-BIAS;old=bytes.fromhex(patch['old']);new=bytes.fromhex(patch['new'])
        assert baseline[at:at+len(old)]==old
        expected[at:at+len(new)]=new
        spans.append((patch['iso_offset'],patch['iso_offset']+len(new)))
    assert combined==expected,'Combined ELF differs outside the refill additions'
    changed=0;offset=0
    with args.health_menu_iso.open('rb') as before,args.combined_iso.open('rb') as after:
        while True:
            x=before.read(1024*1024);y=after.read(1024*1024)
            assert len(x)==len(y)
            if not x:break
            if x!=y:
                for i,(a,b) in enumerate(zip(x,y)):
                    if a!=b:
                        assert any(lo<=offset+i<hi for lo,hi in spans),'Unexpected ISO change'
                        changed+=1
            offset+=len(x)
    assert changed==22
    # Run existing exhaustive menu tests, then bind their executor to actual ISO words.
    previous=sys.argv
    try:
        sys.argv=['test_health_menu.py',str(args.retail_elf)]
        menu=runpy.run_path(str(HERE.parent/'health-menu/test_health_menu.py'))
    finally:sys.argv=previous
    runmenu=menu['run'];g=runmenu.__globals__
    for va,word in g['words'].items():
        actual=struct.unpack_from('<I',combined,va-BIAS)[0]
        assert actual==word,('Menu instruction differs from tested specification',hex(va))
    g['words']={va:struct.unpack_from('<I',combined,va-BIAS)[0] for va in g['words']}
    mspec=importlib.util.spec_from_file_location('retail_refill',HERE.parent/'health-refill-test/test_health_refill.py')
    refill=importlib.util.module_from_spec(mspec);mspec.loader.exec_module(refill)
    count_cases=0
    for maximum in [3,6]:
        for hp in range(maximum+1):
            for count in [0,1,2,4]:
                for exists in [False,True]:
                    for flow_count in [0,1,2,3]:
                        before=refill.run(retail,hp,maximum,count,exists,flow_count)
                        after=refill.run(combined,hp,maximum,count,exists,flow_count)
                        assert before['hp']==hp and after['hp']==(maximum if count else hp)
                        assert before['calls']==after['calls']
                        assert any(c[0]=='confirm' for c in after['calls'])==(exists and flow_count==2)
                        assert before['slots']==after['slots']==(6,6)
                        assert before['bonus']==after['bonus']==(3,3)
                        assert before['max']==after['max']==maximum
                        ignored=set(range(refill.PLAYER+0x460,refill.PLAYER+0x464))
                        assert {a:v for a,v in before['memory'].items() if a not in ignored}=={a:v for a,v in after['memory'].items() if a not in ignored}
                        count_cases+=1
    interactions=0
    for maximum in [3,6]:
        for hp in range(maximum+1):
            for state in range(32):
                for damage in [0,1]:
                    before=runmenu(state,0,damage=damage,health=hp)
                    result=refill.run(combined,hp,maximum,1,True,2)
                    after=runmenu(before['state'],0,damage=before['damage'],health=result['hp'])
                    assert result['hp']==maximum
                    assert after['state']==before['state'] and after['damage']==damage
                    if state&1:
                        assert before['formats'][-1][8]==hp
                        assert after['formats'][-1][8]==maximum
                    else:assert not after['formats']
                    # The existing row-4 action still toggles damage after refilling.
                    toggled=runmenu(7,0x10000,damage=damage,health=result['hp'])
                    assert toggled['damage']==1-damage
                    assert toggled['formats'][-1][8]==maximum
                    again=refill.run(combined,result['hp'],maximum,1,True,2)
                    assert again['hp']==maximum,'Repeated refill not idempotent'
                    interactions+=1
    previous=sys.argv
    try:
        sys.argv=['test_retail_damage.py',str(args.retail_elf)]
        damage_test=runpy.run_path(str(HERE.parent/'health-menu/test_retail_damage.py'))
    finally:sys.argv=previous
    # The two instruction windows used by that test are unchanged in this ISO.
    for lo,hi in [(0x32B774,0x32B784),(0x32BAE8,0x32BAF8)]:
        assert combined[lo-BIAS:hi-BIAS]==retail[lo-BIAS:hi-BIAS]
    receipt={'combined_iso_sha256':sha(args.combined_iso),
             'combined_elf_sha256':hashlib.sha256(combined).hexdigest(),
             'size_bytes':args.combined_iso.stat().st_size,
             'added_changed_bytes_vs_health_menu':changed,
             'menu_instruction_cases':g['count'],'menu_pointer_guard_cases':g['guardcases'],
             'menu_hp_readout_cases':g['healthcases'],'menu_sequence_steps':len(g['sequence']),
             'callback_comparison_cases':count_cases,'callback_executions':count_cases*2,
             'menu_refill_interaction_cases':interactions,
             'retail_damage_cases':damage_test['count'],
             'actual_iso_menu_words_match_tested_spec':True,
             'menu_elf_preserved_outside_two_refill_sites':True,
             'hardware_tested':False,
             'limits':'Synthetic valid runtime objects; external hash/object/event, renderer, position/scene and sound backend calls modeled. This does not boot PS2/PS3, test live cheat input, saves or transitions.'}
    (HERE/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    print('COMBINED PASS',json.dumps(receipt,indent=2))

if __name__=='__main__':main()
