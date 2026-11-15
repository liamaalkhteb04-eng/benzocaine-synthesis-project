"""Prepare target-neutral Solar input; paid execution requires two explicit gates."""
import argparse
from pathlib import Path
import os
import json
import urllib.request
from _runtime import ROOT,load,save,digest

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',required=True,type=Path);p.add_argument('--attempt-id',required=True)
    group=p.add_mutually_exclusive_group(required=True);group.add_argument('--prepare-only',action='store_true');group.add_argument('--execute-solar',action='store_true');a=p.parse_args()
    if Path(a.attempt_id).name!=a.attempt_id or a.attempt_id in {'.','..'}:p.error('Use a new simple attempt ID')
    plan=load(ROOT/'configs/report-plan.json')
    if a.execute_solar and not (plan['paid_calls_authorized'] and plan['report_generation_authorized']):p.error('Paid calls and report generation are not authorized by the current phase')
    run=a.run_dir.resolve();evidence=load(run/'report-evidence.json')
    for name,sha in evidence['source_hashes'].items():
        if digest(run/name)!=sha:raise ValueError('Evidence source changed: '+name)
    attempt=run/'solar-attempts'/a.attempt_id;attempt.mkdir(parents=True,exist_ok=False)
    skill=ROOT/'skill/synthesis_report_skill.md'
    evidence['execution_record']=load(run/'manifest.json')
    request={'model':plan['model'],'temperature':plan['temperature'],'max_tokens':plan['max_tokens'],'stream':False,'messages':[{'role':'system','content':skill.read_text(encoding='utf-8')},{'role':'user','content':'실제 근거를 읽어 지침에 따른 한국어 보고서 전문을 작성하세요.\n'+json.dumps(evidence,ensure_ascii=False)}]}
    save(attempt/'solar-request.json',request)
    status={'status':'prepared_not_executed','inference_executed':False,'model':plan['model'],'skill_sha256':digest(skill),'request_sha256':digest(attempt/'solar-request.json'),'paid_calls':0,'reason':'Preparation only; no network request and no report authored'}
    if a.execute_solar:
        key=os.environ.get('UPSTAGE_API_KEY','').strip()
        if not key:raise ValueError('UPSTAGE_API_KEY missing from process environment; no key value logged')
        req=urllib.request.Request('https://api.upstage.ai/v1/chat/completions',data=json.dumps(request,ensure_ascii=False).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=300) as response:raw=json.loads(response.read())
            save(attempt/'solar-response.raw.json',raw)
            if not raw.get('model','').startswith('solar-pro4') or raw['choices'][0]['finish_reason']!='stop':raise ValueError('Unexpected model or incomplete response')
            text=raw['choices'][0]['message']['content'];output=ROOT/'reports'/(run.name+'-'+a.attempt_id);output.mkdir(parents=True,exist_ok=False)
            (output/'report.md').write_bytes(text.encode('utf-8'));status.update(status='success',inference_executed=True,returned_model=raw['model'],report_path=str(output/'report.md'),paid_calls=1,reason='Solar authored genuine report')
        except Exception as exc:status.update(status='failed',reason=type(exc).__name__,paid_calls=1)
    save(attempt/'solar-status.json',status);print(status['status'])

if __name__=='__main__':main()
