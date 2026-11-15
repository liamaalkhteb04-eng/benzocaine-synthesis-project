"""Build and inspect a targeted Solar request locally. This script never sends a request."""
import argparse,hashlib,json
from pathlib import Path
MARKERS=['<<<SECTION_2_1_START>>>','<<<SECTION_2_1_END>>>','<<<SECTION_8_REPRO_START>>>','<<<SECTION_8_REPRO_END>>>']
FORBIDDEN=['A/B','OpenCode','Pi Coding','harness comparison','draft comparison','cross-draft','previous conversation']
REQUIRED=['benzocaine-live-20261031-03','benzocaine-live-20261031-04','benzocaine-live-repro-20261105-01','[H][H]','CCOCC','FB(F)F','95% alcohol','91-100%','bd0a3cb74cd7068de474c8fb789a00a66bc42c75636d66510ccac585ebe928f8','a4f1945e90cfa195538320833d68aed38f14e2fcc2f8afb5d958bc920edcafbe','ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd','9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563','catalyst1=[Pd]','solvent1=CCO','reagent1=\'\'','reagent1=[H][H]','91-100%','corrected validation']
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--rules',type=Path,required=True); ap.add_argument('--section21',type=Path,required=True); ap.add_argument('--section8',type=Path,required=True); ap.add_argument('--source-report',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--audit',type=Path,required=True); a=ap.parse_args()
 rules=a.rules.read_text(encoding='utf-8-sig'); s21=a.section21.read_text(encoding='utf-8-sig'); s8=a.section8.read_text(encoding='utf-8-sig'); report=a.source_report.read_text(encoding='utf-8-sig')
 h21=next((x for x in report.splitlines() if x.startswith('### 2.1')),None); h3=next((x for x in report.splitlines() if x.startswith('## 3.')),None); h8=next((x for x in report.splitlines() if x.startswith('## 8.')),None)
 if not h21 or not h3 or not h8: raise SystemExit('Source report section anchors missing')
 sec=report[report.index(h21):report.index(h3,report.index(h21))]
 target21=next((line for line in sec.splitlines() if line.startswith('\uC774 \uBE44\uAD50\uC5D0\uC11C route-01\uC744 \uBA3C\uC800')),None)
 para8=report[report.index(h8)+len(h8):].strip().split('\n\n',1)[0]
 if not target21 or not para8.startswith('\uC774 \uBCF4\uACE0\uC11C\uC758 \uC608\uCE21 \uACB0\uACFC\uB294'): raise SystemExit('Exact replacement targets could not be isolated')
 user=("Write only the two specified Korean paragraph replacements using the targeted rules and the matching section evidence below. Do not make a cross-version evaluation, summarize the project, or discuss tool orchestration. Do not include any prior conversation. Keep all report content outside the two replacement paragraphs unchanged.\n\n"
       +"Task for section 2.1: replace only this existing final route-selection rationale paragraph:\n"+target21+"\n\n"
       +"Task for section 8: replace only the opening paragraph under the reproducibility heading:\n"+para8+"\n\n"
       +"Return exactly two blocks, each literal marker once, with no text outside the blocks:\n"
       +MARKERS[0]+"\n[Replacement paragraph for section 2.1]\n"+MARKERS[1]+"\n"
       +MARKERS[2]+"\n[Replacement paragraph for section 8]\n"+MARKERS[3]+"\n\n"
       +"--- Evidence for section 2.1 only ---\n"+s21+"\n"
       +"--- Evidence for section 8 only ---\n"+s8)
 payload={'model':'solar-pro4-260806','messages':[{'role':'system','content':rules},{'role':'user','content':user}],'temperature':0,'reasoning_effort':'none','max_tokens':2400,'n':1,'stream':False}
 combined=rules+'\n'+user
 checks={'exactly_two_messages_system_user':[m['role'] for m in payload['messages']]==['system','user'],'no_prior_conversation_or_tool_messages':len(payload['messages'])==2 and all(m['role'] in ('system','user') for m in payload['messages']),'each_required_marker_once':all(user.count(m)==1 for m in MARKERS),'no_ambiguous_old_task_terms':not any(x.lower() in combined.lower() for x in FORBIDDEN),'all_required_evidence_present':all(x in combined for x in REQUIRED),'only_two_target_paragraphs_selected':target21.startswith('\uC774 \uBE44\uAD50\uC5D0\uC11C route-01\uC744 \uBA3C\uC800') and para8.startswith('\uC774 \uBCF4\uACE0\uC11C\uC758 \uC608\uCE21 \uACB0\uACFC\uB294'),'targeted_rules_only':'# Targeted report revision rules' in rules and all(x not in rules for x in ['OpenCode','Pi Coding','harness','\uD558\uB124\uC2A4','\uC804\uCCB4 \uBCF4\uACE0\uC11C'])}
 if not all(checks.values()): raise SystemExit('Request preflight failed: '+json.dumps(checks,ensure_ascii=False))
 body=json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode('utf-8'); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_bytes(body)
 audit={'status':'passed_local_pre_send_inspection','external_request_sent':False,'model_call_made':False,'api_key_or_auth_header_present':False,'messages':[{'role':m['role'],'content_chars':len(m['content']),'content_sha256':sha(m['content'].encode())} for m in payload['messages']],'wire_body_sha256':sha(body),'source_files':{str(f):sha(f.read_bytes()) for f in [a.rules,a.section21,a.section8,a.source_report]},'checks':checks,'max_output_tokens':payload['max_tokens'],'note':'Prepared request only; no model request was made. Any later mock fixture may test marker parsing only, not Solar success.'}
 a.audit.parent.mkdir(parents=True,exist_ok=True); a.audit.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':audit['status'],'checks':checks,'wire_sha256':audit['wire_body_sha256'],'sent':False},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
