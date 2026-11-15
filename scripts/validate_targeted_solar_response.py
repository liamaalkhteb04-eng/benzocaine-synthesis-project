"""Pre-merge verification of targeted Solar blocks against saved primary evidence."""
import json,hashlib
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 root=Path(__file__).resolve().parents[1]; out=root/'reports/benzocaine-hash-correction-submission-20261115'; call=out/'solar-call'; base=root/'reports/benzocaine-literature-validated-20261114'; audit=root/'analyses/route-replay-hash-audit-20261114'; rawroot=root/'results/benzocaine-live-20261031-04'
 response=read(call/'solar-response.raw.json'); status=read(call/'solar-status.json'); content=response['choices'][0]['message']['content']
 marks={'s21_open':'<<<SECTION_2_1_START>>>','s21_close':'<<<SECTION_2_1_END>>>','s8_open':'<<<SECTION_8_REPRO_START>>>','s8_close':'<<<SECTION_8_REPRO_END>>>'}
 counts={k:content.count(v) for k,v in marks.items()}
 blocks={};
 for op,cl,key in [('s21_open','s21_close','s21'),('s8_open','s8_close','s8')]:
  if counts[op]!=1 or counts[cl]!=1:blocks[key]=''
  else:blocks[key]=content.split(marks[op],1)[1].split(marks[cl],1)[0].strip()
 route_rxn='CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1'
 cond=read(rawroot/'conditions-parrot.raw.json')
 r1=[r for r in cond['predictions'] if r.get('reaction_smiles')==route_rxn and {'route_id':'route-01','step_id':'step-01'} in r.get('steps',[])]
 c1={str(c['rank']):c for c in r1[0]['candidates']} if len(r1)==1 else {}
 r5=[r for r in cond['predictions'] if r.get('reaction_smiles')=='CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1' and {'route_id':'route-05','step_id':'step-02'} in r.get('steps',[])]
 c5=next((x for x in r5[0]['candidates'] if x.get('rank')==1),{}) if len(r5)==1 else {}
 lit=read(base/'literature-validation/comparison.json')
 org=next(x for x in lit['literature'] if x['key']=='OrgSyn-1928-8-66')
 corrected=read(audit/'reproduction-validation-corrected.json')
 report=(base/'report.md').read_text(encoding='utf-8-sig')
 d10=next((x for x in report.splitlines() if x.startswith('- [D10]')), '')
 section21=blocks['s21']; section8=blocks['s8']
 checks={
  'Solar_call_success_and_run_id':status.get('status')=='success' and status.get('run_id')=='benzocaine-hash-correction-final-20261115-01' and response.get('model')=='solar-pro4-260806',
  'all_four_output_markers_once':all(v==1 for v in counts.values()),
  'no_text_outside_two_blocks':content.strip().startswith(marks['s21_open']) and content.strip().endswith(marks['s8_close']),
  'route01_rank1_raw_slots_confirmed':bool(c1) and all(c1['1'].get(k)==v for k,v in {'catalyst1':'[Pd]','solvent1':'CCO','solvent2':'','reagent1':'','reagent2':''}.items()),
  'route01_rank4_raw_slots_confirmed':bool(c1) and all(c1['4'].get(k)==v for k,v in {'catalyst1':'[Pd]','solvent1':'CCO','solvent2':'','reagent1':'[H][H]','reagent2':''}.items()),
  'route05_tokens_are_not_assigned_to_route01':bool(c5) and c5.get('reagent1')=='CCOCC' and c5.get('reagent2')=='FB(F)F' and 'CCOCC' not in section21 and 'FB(F)F' not in section21,
  'primary_source_is_same_transformation':lit.get('reaction_smiles')==route_rxn and org.get('starting_material','').startswith('ethyl p-nitrobenzoate') and org.get('product','').startswith('ethyl p-aminobenzoate'),
  '95_percent_alcohol_is_solvent_not_yield_in_source':org.get('solvent','').startswith('95% alcohol') and '95%' not in org.get('yield',{}).get('reported',''),
  'isolated_yield_detail_in_verified_literature_markdown': '91\u2013100%' in (base/'literature-validation/literature-comparison.md').read_text(encoding='utf-8-sig') and '15\u201316.5 g' in (base/'literature-validation/literature-comparison.md').read_text(encoding='utf-8-sig') and '95% alcohol' in (base/'literature-validation/literature-comparison.md').read_text(encoding='utf-8-sig'),
  'section21_cites_literature_and_states_post_inference':all(x in section21 for x in ['[18]','[19]','[D9]']) and '\uC774 \uBB38\uD5CC \uAC80\uD1A0\uB294 AI \uCD94\uB860 \uC774\uD6C4' in section21,
  'selection_rationale_does_not_claim_literature_exclusivity': not any(x in section21.lower() for x in ['only route','only pathway','no literature precedent for route-02','no literature precedent for route-05']),
  'route01_reference_subsection_exists': '### 3.1.1 route-01 direct experimental literature and AI-condition comparison' in report,
  'reproducibility_all_model_stock_hashes_present':all(x in section8 for x in ['bd0a3cb74cd7068de474c8fb789a00a66bc42c75636d66510ccac585ebe928f8','a4f1945e90cfa195538320833d68aed38f14e2fcc2f8afb5d958bc920edcafbe','99d39a6f807c3e815487500bafc2b4a9dc66a31af189e3b1776874fb0d4a188d']),
  'reproducibility_config_hashes_and_unresolved_cause_correct':all(x in section8 for x in ['ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd','9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563']) and '\uACBD\uB85C \uAD6C\uBD84\uC790 \uC815\uADDC\uD654 \uD6C4 \uC77C\uCE58' in section8 and 'unresolved' in section8 and corrected.get('status')=='passed',
  'run_roles_match_corrected_evidence':all(x in section8 for x in ['benzocaine-live-20261031-03','benzocaine-live-20261031-04','benzocaine-live-repro-20261105-01']) and corrected.get('historical_route_run_id')=='benzocaine-live-20261031-03' and corrected.get('historical_representative_run_id')=='benzocaine-live-20261031-04',
  'citation_D10_path_in_new_packet_resolves_to_corrected_record': read(out/'evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation.json').get('status')=='passed' and read(out/'evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-original-conflicting.json').get('comparison_to_historical_benzocaine',{}).get('model_and_template_hashes_same') is False,
  'response_matches_requested_two_edit_scope':len(section21)>0 and len(section8)>0 and 'A/B' not in content and 'OpenCode' not in content and 'Pi Coding' not in content,
 }
 failed=[k for k,v in checks.items() if not v]
 result={'status':'passed' if not failed else 'failed','premerge_only':True,'report_merged':False,'docx_pdf_generated':False,'response_path':str(call/'solar-response.raw.json'),'response_sha256':sha(call/'solar-response.raw.json'),'run_id':status.get('run_id'),'blocks':{'section21_chars':len(section21),'section8_chars':len(section8),'marker_counts':counts},'checks':checks,'failed_checks':failed,'evidence':{'conditions_raw_path':str(rawroot/'conditions-parrot.raw.json'),'conditions_raw_sha256':sha(rawroot/'conditions-parrot.raw.json'),'literature_comparison_path':str(base/'literature-validation/comparison.json'),'literature_comparison_sha256':sha(base/'literature-validation/comparison.json'),'corrected_validation_path':str(audit/'reproduction-validation-corrected.json'),'corrected_validation_sha256':sha(audit/'reproduction-validation-corrected.json'),'D10_source_line':d10},'finding':('The section 2.1 wording implies that route-01 alone among reviewed transformations has direct literature precedent, while this literature search only documents the route-01 transformation; it does not establish that routes 02/05 lack such precedent. Also, current D10 mapping still names the older validation JSON with contradictory flags, not the corrected JSON.' if failed else 'All pre-merge checks passed.')}
 dest=Path(__file__).resolve().parents[1]/'reports/benzocaine-hash-correction-submission-20261115/solar-response-validation.json'
 dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':result['status'],'failed_checks':failed,'result_path':str(dest)},ensure_ascii=True,indent=2))
 return 0 if not failed else 1
if __name__=='__main__':raise SystemExit(main())
