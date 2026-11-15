"""Splice two validated Solar-authored paragraphs; verify all other markdown bytes are preserved."""
import argparse,json,hashlib
from pathlib import Path
MARKERS={'s21o':'<<<SECTION_2_1_START>>>','s21c':'<<<SECTION_2_1_END>>>','s8o':'<<<SECTION_8_REPRO_START>>>','s8c':'<<<SECTION_8_REPRO_END>>>'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--response',type=Path,required=True);ap.add_argument('--status',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--manifest',type=Path,required=True);a=ap.parse_args()
 source=a.source.read_text(encoding='utf-8-sig'); raw=a.response.read_bytes(); response=json.loads(raw.decode('utf-8-sig')); status=json.loads(a.status.read_text(encoding='utf-8'))
 if status.get('status')!='success' or status.get('retry_count')!=0 or status.get('run_id')!='benzocaine-hash-correction-final-20261115-01':raise SystemExit('Solar status/run/retry gate failed')
 content=response['choices'][0]['message']['content']
 if any(content.count(m)!=1 for m in MARKERS.values()):raise SystemExit('Marker count invalid')
 if not content.strip().startswith(MARKERS['s21o']) or not content.strip().endswith(MARKERS['s8c']):raise SystemExit('Extraneous response content outside markers')
 b21=content.split(MARKERS['s21o'],1)[1].split(MARKERS['s21c'],1)[0].strip();b8=content.split(MARKERS['s8o'],1)[1].split(MARKERS['s8c'],1)[0].strip()
 if '\n\n' in b21 or '\n\n' in b8:raise SystemExit('Each Solar block must be a single paragraph')
 target=next((x for x in source.split('\n\n') if x.startswith('\uC774 \uBE44\uAD50\uC5D0\uC11C route-01\uC744 \uBA3C\uC800')),None)
 h8=next((x for x in source.splitlines() if x.startswith('## 8.')),None)
 if target is None or h8 is None:raise SystemExit('Target paragraph/headings not found')
 tail=source[source.index(h8)+len(h8):].lstrip('\n'); old8=tail.split('\n\n',1)[0]
 if not old8.startswith('\uC774 \uBCF4\uACE0\uC11C\uC758 \uC608\uCE21 \uACB0\uACFC\uB294'):raise SystemExit('Unexpected section 8 target paragraph')
 if source.count(target)!=1 or source.count(old8)!=1:raise SystemExit('Target paragraph is not unique')
 merged=source.replace(target,b21,1).replace(old8,b8,1)
 # Reverse the two splices and require byte-equivalent source text.
 restored=merged.replace(b21,target,1).replace(b8,old8,1)
 if restored!=source:raise SystemExit('Unexpected changes outside the two replacement paragraphs')
 if a.output.exists():raise SystemExit('Output already exists; refusing overwrite')
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(merged,encoding='utf-8')
 man={'status':'solar_authored_targeted_replacements_applied','source_report_path':str(a.source.resolve()),'source_report_sha256':sha(a.source.read_bytes()),'solar_response_path':str(a.response.resolve()),'solar_response_sha256':sha(raw),'merged_report_sha256':sha(a.output.read_bytes()),'solar_call_count':1,'retry_count':0,'run_id':status['run_id'],'replaced_blocks':['section 2.1 final route-selection rationale paragraph','section 8 opening reproducibility paragraph'],'all_other_report_text_preserved':True,'source_chars':len(source),'merged_chars':len(merged)}
 a.manifest.write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(man,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
