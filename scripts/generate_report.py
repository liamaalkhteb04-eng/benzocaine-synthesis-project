"""Prepare target-neutral Solar input; paid execution requires two explicit gates."""
import argparse
from pathlib import Path
import os
import json
import urllib.request
from _runtime import ROOT,load,save,digest

def build_request(run, plan):
    evidence=load(run/'report-evidence.json')
    for name,sha in evidence['source_hashes'].items():
        if digest(run/name)!=sha:raise ValueError('Evidence source changed: '+name)
    skill=ROOT/plan.get('report_writing_skill_path','skill/report-writing/SKILL.md')
    if not skill.is_file():raise FileNotFoundError(f'Report-writing skill is missing: {skill.relative_to(ROOT)}')
    record=load(run/'manifest.json')
    if record.get('artifact_type')=='public_curated_evidence_derivative_not_execution_record':
        evidence['execution_record']={
            'artifact_type':record['artifact_type'],
            'source_run_id':record['source_run_id'],
            'source_execution_manifest_sha256':record['source_execution_manifest_sha256'],
            'prediction_statuses_from_source_run':record['prediction_statuses_from_source_run'],
            'new_inference_executed':False,
            'solar_call_executed':False,
        }
        evidence['public_derivation_record']=load(run/'public-derivation.json')
    else:
        evidence['execution_record']=record
    request={'model':plan['model'],'temperature':plan['temperature'],'max_tokens':plan['max_tokens'],'stream':False,'messages':[{'role':'system','content':skill.read_text(encoding='utf-8')},{'role':'user','content':'보고서 작성 스킬과 실제 실행 근거에 따라 전체 한국어 보고서 원고를 작성하세요. 근거에 없는 값은 만들지 말고 누락 사항을 표시하세요.\n'+json.dumps(evidence,ensure_ascii=False)}]}
    return request,skill

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',required=True,type=Path);p.add_argument('--attempt-id',required=True)
    group=p.add_mutually_exclusive_group(required=True);group.add_argument('--prepare-only',action='store_true');group.add_argument('--execute-solar',action='store_true');a=p.parse_args()
    if Path(a.attempt_id).name!=a.attempt_id or a.attempt_id in {'.','..'}:p.error('Use a new simple attempt ID')
    plan=load(ROOT/'configs/report-plan.json')
    if a.execute_solar and not (plan['paid_calls_authorized'] and plan['report_generation_authorized']):p.error('Paid calls and report generation are not authorized by the current phase')
    run=a.run_dir.resolve();attempt=run/'solar-attempts'/a.attempt_id
    skill=ROOT/plan.get('report_writing_skill_path','skill/report-writing/SKILL.md')
    if a.prepare_only:
        attempt.mkdir(parents=True,exist_ok=False)
        request,skill=build_request(run,plan)
        save(attempt/'solar-request.json',request)
        status={'status':'prepared_not_executed','inference_executed':False,'model':plan['model'],'report_writing_skill_path':str(skill.relative_to(ROOT)),'skill_sha256':digest(skill),'request_sha256':digest(attempt/'solar-request.json'),'paid_calls':0,'reason':'Preparation only; no network request and no report authored'}
        save(attempt/'solar-prepare-status.json',status)
        print(status['status']);return
    request_path=attempt/'solar-request.json'
    if not attempt.is_dir() or not request_path.is_file():p.error('Execute requires a previously prepared request in this attempt directory')
    if ((attempt/'solar-response.raw.json').exists() or (attempt/'solar-status.json').exists()
            or (attempt/'solar-execution-started.json').exists()):p.error('This attempt already has an execution record; retries are blocked')
    request=load(request_path)
    skill_text=skill.read_text(encoding='utf-8')
    if request.get('messages',[{}])[0].get('content')!=skill_text:p.error('Prepared request does not contain the current report-writing skill; prepare a new attempt')
    status={'status':'executing_single_request','inference_executed':False,'model':plan['model'],'report_writing_skill_path':str(skill.relative_to(ROOT)),'skill_sha256':digest(skill),'request_sha256':digest(request_path),'paid_calls':0}
    if a.execute_solar:
        key=os.environ.get('UPSTAGE_API_KEY','').strip()
        if not key:raise ValueError('UPSTAGE_API_KEY missing from process environment; no key value logged')
        save(attempt/'solar-execution-started.json',{'status':'single_request_started','model':plan['model'],'request_sha256':digest(request_path),'report_writing_skill_sha256':digest(skill),'automatic_retries':0,'api_key_logged':False})
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
