"""Send one already-inspected targeted Solar request; hard $0.01 reservation; no retry."""
import argparse,hashlib,json,os,time,urllib.error,urllib.request
from pathlib import Path
MODEL='solar-pro4-260806'; URL='https://api.upstage.ai/v1/chat/completions'; PRICE_IN=.30; PRICE_OUT=1.20; VAT=.10; RESERVE=.01; CAP=1.00; MAX_OUTPUT=700
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl): return None
def sha(b):return hashlib.sha256(b).hexdigest()
def load_key(path):
 if os.environ.get('UPSTAGE_API_KEY','').strip():return os.environ['UPSTAGE_API_KEY'].strip()
 for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
  line=line.strip()
  if line and not line.startswith('#') and '=' in line:
   k,v=line.split('=',1)
   if k.strip()=='UPSTAGE_API_KEY':return v.strip().strip('"\'')
 return ''
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--request',type=Path,required=True);ap.add_argument('--preflight-audit',type=Path,required=True);ap.add_argument('--prior-ledger',type=Path,required=True);ap.add_argument('--env-file',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--execute-live',action='store_true');a=ap.parse_args()
 body=a.request.read_bytes(); payload=json.loads(body); audit=json.loads(a.preflight_audit.read_text(encoding='utf-8')); prior=json.loads(a.prior_ledger.read_text(encoding='utf-8'))
 if audit.get('status')!='passed_local_pre_send_inspection' or audit.get('wire_body_sha256')!=sha(body):raise SystemExit('Pre-send audit mismatch; request not sent.')
 if [m.get('role') for m in payload.get('messages',[])]!=['system','user'] or payload.get('model')!=MODEL or payload.get('n')!=1 or payload.get('stream') is not False:raise SystemExit('Unsafe or unexpected payload shape; request not sent.')
 if int(payload.get('max_tokens',0))>MAX_OUTPUT:raise SystemExit('Output token limit exceeded; request not sent.')
 cumulative=float(prior['conservative_cumulative_after_usd']); reserved_after=cumulative+RESERVE
 if reserved_after>CAP+1e-9:raise SystemExit('Cumulative budget guard; request not sent.')
 content_bytes=sum(len(m['content'].encode('utf-8')) for m in payload['messages'])
 input_token_upper=content_bytes+2048
 estimate=round((input_token_upper*PRICE_IN+int(payload['max_tokens'])*PRICE_OUT)*(1+VAT)/1_000_000,8)
 if estimate>RESERVE+1e-9:raise SystemExit(f'Conservative request estimate exceeds ${RESERVE:.2f} reservation; request not sent.')
 out=a.output_dir.resolve(); call=out/'solar-call';call.mkdir(parents=True,exist_ok=True)
 stat=call/'solar-status.json';rawpath=call/'solar-response.raw.json'; reqpath=call/'solar-request.redacted.json'
 if stat.exists() or rawpath.exists():raise SystemExit('A request was already attempted; refusing any retry.')
 if reqpath.exists() and reqpath.read_bytes()!=body:raise SystemExit('A different request is already staged; refusing to overwrite.')
 if not reqpath.exists():reqpath.write_bytes(body)
 pre={'status':'prepared','run_id':'benzocaine-documentation-cleanup-20261115-01','model':MODEL,'request_sha256':sha(body),'input_bytes':content_bytes,'conservative_input_token_upper_bound':input_token_upper,'max_output_tokens':payload['max_tokens'],'max_external_posts':1,'retries':0,'max_reserved_cost_including_vat_usd':RESERVE,'conservative_estimated_cost_including_vat_usd':estimate,'prior_cumulative_usd':cumulative,'cumulative_with_reservation_usd':round(reserved_after,8),'remaining_under_cap_after_reservation_usd':round(CAP-reserved_after,8),'api_key_value_logged':False,'solar_request_sent':False}
 (call/'pre-call-budget.json').write_text(json.dumps(pre,indent=2)+'\n',encoding='utf-8')
 if not a.execute_live:
  print(json.dumps(pre,indent=2));return 0
 key=load_key(a.env_file)
 if not key:
  (call/'solar-status.json').write_text(json.dumps({**pre,'status':'blocked_missing_key','api_key_present':False},indent=2)+'\n',encoding='utf-8');print('Solar call not sent: key absent.');return 2
 (call/'solar-status.json').write_text(json.dumps({**pre,'status':'reserved_before_send','api_key_present':True},indent=2)+'\n',encoding='utf-8')
 request=urllib.request.Request(URL,data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'application/json'},method='POST')
 http=None;err=None;data=b'';start=time.perf_counter()
 try:
  with urllib.request.build_opener(NoRedirect).open(request,timeout=180) as response:http=response.status;data=response.read()
 except urllib.error.HTTPError as exc:http=exc.code;data=exc.read()
 except Exception as exc:err=type(exc).__name__;data=json.dumps({'transport_error_type':err}).encode()
 elapsed=round((time.perf_counter()-start)*1000,1);rawpath.write_bytes(data)
 try: decoded=json.loads(data.decode('utf-8'))
 except Exception: decoded={}
 usage=decoded.get('usage') if isinstance(decoded,dict) else None; inp=(usage or {}).get('prompt_tokens',(usage or {}).get('input_tokens')) if isinstance(usage,dict) else None; oup=(usage or {}).get('completion_tokens',(usage or {}).get('output_tokens')) if isinstance(usage,dict) else None; cached=((usage or {}).get('prompt_tokens_details') or {}).get('cached_tokens',0) if isinstance(usage,dict) else 0
 actual=None
 if isinstance(inp,(int,float)) and isinstance(oup,(int,float)):actual=round(((max(0,inp-(cached or 0))*PRICE_IN+(cached or 0)*.06+oup*PRICE_OUT)/1_000_000)*(1+VAT),8)
 choice=(decoded.get('choices') or [{}])[0] if isinstance(decoded,dict) else {}; msg=choice.get('message') or {}; content=msg.get('content') if isinstance(msg,dict) else None; finish=choice.get('finish_reason') if isinstance(choice,dict) else None; model=decoded.get('model') if isinstance(decoded,dict) else None
 ok=http==200 and model==MODEL and finish=='stop' and isinstance(content,str) and bool(content.strip())
 after=round(cumulative+(actual if actual is not None else RESERVE),8)
 final={**pre,'status':'success' if ok else 'failed_after_single_request','http_status':http,'returned_model':model,'finish_reason':finish,'latency_ms':elapsed,'usage':usage,'actual_cost_usd_including_vat':actual,'cumulative_after_usd':after,'remaining_under_cap_usd':round(CAP-after,8),'retry_count':0,'transport_error_type':err,'response_sha256':sha(data),'api_key_value_logged':False,'solar_request_sent':True}
 stat.write_text(json.dumps(final,indent=2)+'\n',encoding='utf-8')
 ledger={'previous_cumulative_usd':cumulative,'new_call_reserved_usd':RESERVE,'new_call_actual_including_vat_usd':actual,'cumulative_after_usd':after,'cap_usd':CAP,'cash_payment_or_topup':False,'calls':[{'run_id':pre['run_id'],'request_sha256':sha(body),'status':final['status'],'input_tokens':inp,'output_tokens':oup,'actual_cost_usd_including_vat':actual,'retry_count':0}]}
 (out/'cost-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:final[k] for k in ['status','run_id','http_status','returned_model','finish_reason','latency_ms','usage','conservative_estimated_cost_including_vat_usd','max_reserved_cost_including_vat_usd','actual_cost_usd_including_vat','cumulative_after_usd','remaining_under_cap_usd','retry_count','api_key_value_logged']},indent=2))
 return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
