"""Local predictions only. This entrypoint never calls a paid API or writes a report."""
import argparse
from datetime import datetime,timezone
from pathlib import Path
import shutil
import subprocess
import sys
from _runtime import ROOT,load,save,digest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True,type=Path);p.add_argument('--run-id',required=True);p.add_argument('--reuse-run',type=Path);a=p.parse_args()
    if Path(a.run_id).name!=a.run_id or a.run_id in {'.','..'}:p.error('Use a new simple run ID')
    run=ROOT/'results'/a.run_id;run.mkdir(parents=True,exist_ok=False);shutil.copyfile(a.input,run/'input.json');commands=[]
    def invoke(script,*arguments):
        command=[sys.executable,'-B','-X','utf8',str(ROOT/'scripts'/script),*map(str,arguments)]
        with (run/'pipeline.log').open('a',encoding='utf-8') as f:
            f.write('COMMAND '+repr(command)+'\n');f.flush();proc=subprocess.run(command,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        commands.append({'command':command,'exit_code':proc.returncode});print(script,proc.returncode,flush=True);return proc.returncode
    invoke('draw_structures.py','--input',run/'input.json','--output-dir',run/'target')
    reused={}
    def reuse(stem):
        if not a.reuse_run:return False
        previous=a.reuse_run.resolve()
        if load(previous/'input.json')!=load(run/'input.json'):raise ValueError('Cannot reuse a different target or input')
        path=previous/(stem+'.json')
        if not path.is_file() or load(path).get('status')!='success':return False
        reused[stem]={'source_run':str(previous),'files':{}}
        for source in previous.glob(stem+'.*'):
            if source.is_file():shutil.copyfile(source,run/source.name);reused[stem]['files'][source.name]=digest(source)
        commands.append({'action':'reuse_actual_successful_evidence','stem':stem,'source_run':str(previous)})
        return True
    if not reuse('routes'):invoke('predict_routes.py','--model','aizynthfinder','--input',run/'input.json','--output',run/'routes.json')
    routes=load(run/'routes.json')
    for task,model in [('conditions','parrot'),('yields','rxn_yields')]:
        if reuse(task+'-'+model):continue
        if routes.get('status')=='success' and routes.get('predictions'):
            invoke('predict_'+task+'.py','--model',model,'--input',run/'routes.json','--output',run/(task+'-'+model+'.json'))
        else:save(run/(task+'-'+model+'.json'),{'status':'not_implemented','inference_executed':False,'predictions':[],'reason':'No usable upstream synthesis route'})
    invoke('draw_routes.py','--input',run/'routes.json','--output-dir',run/'figures')
    if reused:save(run/'reused-evidence.json',reused)
    save(run/'additional-analysis-status.json',{n:{'status':'not_implemented','inference_executed':False,'reason':'Preparation only; tool installation or paid execution is not authorized in this phase'} for n in ['harness_comparison','mopac','epi_suite','discovery_studio']})
    invoke('build_evidence.py','--run-dir',run)
    statuses={name:load(run/(name+'.json')).get('status') for name in ['routes','conditions-parrot','yields-rxn_yields']}
    save(run/'manifest.json',{'created_at':datetime.now(timezone.utc).isoformat(),'statuses':statuses,'commands':commands,'paid_calls':0,'report_generated':False,'files':{f.relative_to(run).as_posix():digest(f) for f in run.rglob('*') if f.is_file()}})
    print(run,statuses);return 0 if all(s=='success' for s in statuses.values()) else 2

if __name__=='__main__':raise SystemExit(main())
