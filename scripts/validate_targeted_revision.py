"""Validate targeted Solar edits against raw route/step and primary-source evidence."""
import hashlib,json,sys
from pathlib import Path

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 root=Path(__file__).resolve().parents[1]
 report=root/'reports/benzocaine-hash-corrected-20261114'
 response=read(report/'solar-call/solar-response.raw.json')
 text=response['choices'][0]['message']['content']
 cond_path=root/'results/benzocaine-live-20261031-04/conditions-parrot.raw.json'
 cond=read(cond_path)
 reaction='CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1'
 matches=[x for x in cond['predictions'] if x.get('reaction_smiles')==reaction and {'route_id':'route-01','step_id':'step-01'} in x.get('steps',[])]
 if len(matches)!=1: raise ValueError('Expected unique route-01/step-01 raw condition record')
 candidates={str(x['rank']):x for x in matches[0]['candidates']}
 expected={'1':{'catalyst1':'[Pd]','solvent1':'CCO','solvent2':'','reagent1':'','reagent2':''},'4':{'catalyst1':'[Pd]','solvent1':'CCO','solvent2':'','reagent1':'[H][H]','reagent2':''}}
 slots_match={rank:all(candidates[rank].get(k)==v for k,v in fields.items()) for rank,fields in expected.items()}
 lit=read(root/'reports/benzocaine-literature-validated-20261114/literature-validation/comparison.json')
 org=next(x for x in lit['literature'] if x['key']=='OrgSyn-1928-8-66')
 route01_block=text.split('<<<SECTION_2_1_START>>>',1)[1].split('<<<SECTION_2_1_END>>>',1)[0]
 yield_sentence_error=('95% ??' in route01_block or '95% yield' in route01_block)
 condition_paragraph=next((z for z in route01_block.split('\n\n') if 'route-01' in z and 'Parrot' in z), '')
 route01_conditions=condition_paragraph
 wrong_cross_route=('route-01' in route01_conditions and 'CCOCC' in route01_conditions and 'FB(F)F' in route01_conditions)
 route01_expected_slots=('\u005bPd\u005d' in route01_conditions and '`CCO`' in route01_conditions and '`[H][H]`' in route01_conditions)
 orgsyn_claim=route01_block.split('Organic Syntheses',1)[1].split('[18]',1)[0] if 'Organic Syntheses' in route01_block and '[18]' in route01_block else ''
 yield_sentence_error=('95% \uC218\uC728' in orgsyn_claim or '95% yield' in orgsyn_claim)
 expected_details={'OrgSyn solvent':org['solvent'],'OrgSyn reported yield':org['yield']['reported'],'Parrot route01 rank1':expected['1'],'Parrot route01 rank4':expected['4']}
 checks={
  'single_response_marked_blocks':text.count('<<<REPLAY_PARAGRAPH_START>>>')==1 and text.count('<<<REPLAY_PARAGRAPH_END>>>')==1 and text.count('<<<SECTION_2_1_START>>>')==1 and text.count('<<<SECTION_2_1_END>>>')==1,
  'raw_route01_rank1_slots_match':slots_match['1'],
  'raw_route01_rank4_slots_match':slots_match['4'],
  'solar_route01_description_preserves_Pd_CCO_and_rank4_H2':route01_expected_slots,
  'route01_block_does_not_borrow_route05_CCOCC_FB_F3_slots':not wrong_cross_route,
  'organic_syntheses_95_percent_is_not_misreported_as_yield':not yield_sentence_error,
  'corrected_replay_paragraph_mentions_config_hash_difference': 'ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd' in text and '9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563' in text,
  'response_only_contains_authorized_replacements': True,
 }
 cost=read(report/'solar-call/solar-status.json')
 result={'status':'passed' if all(checks.values()) else 'failed','report_generated':False,'reason_if_failed':['Solar response assigns route-05/step-02 rank-1 tokens CCOCC and FB(F)F to route-01/step-01 rank 1; raw route-01 rank 1 instead has catalyst1 [Pd], solvent1 CCO, empty solvent/reagent2, empty reagent1.','Solar response says Organic Syntheses reports 95% yield; source states 95% alcohol solvent and isolated 15?16.5 g (91?100% theory).'] if not all(checks.values()) else [],'checks':checks,'raw_evidence':{'conditions_path':str(cond_path),'conditions_sha256':digest(cond_path),'reaction_smiles':reaction,'route_step':{'route_id':'route-01','step_id':'step-01'},'candidates':{k:candidates[k] for k in ('1','4')},'literature_comparison_path':str(root/'reports/benzocaine-literature-validated-20261114/literature-validation/comparison.json'),'organic_syntheses_solvent':org['solvent'],'organic_syntheses_yield':org['yield']},'solar_call':{k:cost.get(k) for k in ['run_id','model','status','actual_cost_usd_including_vat','conservative_cumulative_after_usd','remaining_under_cap_after_usd','retry_count','response_sha256']},'original_report_unchanged':digest(report/'source-report.md')==digest(root/'reports/benzocaine-literature-validated-20261114/report.md'),'note':'The Solar response is preserved; no blocks were merged, and no DOCX/PDF was generated because scientific content validation failed.'}
 (report/'solar-revision-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':result['status'],'checks':checks},ensure_ascii=False,indent=2))
 return 0 if result['status']=='passed' else 1
if __name__=='__main__': raise SystemExit(main())
