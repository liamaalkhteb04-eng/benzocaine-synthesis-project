"""Synthetic contract fixtures only. These are NOT scientific report paragraphs."""
import unittest,json,csv,io,tempfile,copy
from pathlib import Path
from unittest.mock import patch
import report_pipeline as p

CONFIG=p.load(p.HERE/'config.json')
U,R,F,T=p.context_data(CONFIG)
def fixture(section):
 chunks=[]
 for tag in section['fragments']:
  body=[]
  ids=section.get('fragment_item_ownership',{}).get(tag,[x['id'] for x in section['items']])
  for item in section['items']:
   if item['id'] not in ids:continue
   body+=['[[item:'+item['id']+']]',f'Synthetic contract fixture only for {section["id"]} {tag} {item["id"]}; no scientific assertion is made in this test. '+ ' '.join('[cite: '+c+']' for c in item['required_cites']),'[[/item]]']
  if tag==section['fragments'][0]:
   body+=['[table: '+tid+']' for tid in section['tables']]
   body+=['[figure: '+fid+']\n\n캡션: Synthetic caption fixture '+fid+' only.' for fid in section['figures']]
  chunks+=['[[BEGIN:'+tag+']]','\n\n'.join(body),'[[END:'+tag+']]']
 return '\n'.join(chunks)
def check(sec,text):return p.validate(sec,text,CONFIG,U,R,F,T)
class PipelineTests(unittest.TestCase):
 def test_all_sixty_raw_parrot_rows_and_values_retained(self):
  out=list(csv.DictReader(io.StringIO(T['T_PARROT']['CSV'])))
  self.assertEqual(len(out),60)
  self.assertEqual(out,[{k:r.get(k,'') for k in T['T_PARROT']['columns']} for r in U['parrot_candidates']['data']])
 def test_BF3_reagent2_not_reagent1(self):
  found=[x for x in T['T_PARROT']['rows'] if 'FB(F)F' in x.values()]
  self.assertEqual(len(found),1);self.assertEqual(found[0]['reagent2'],'FB(F)F');self.assertEqual(found[0]['reagent1'],'CCOCC')
 def test_predeclared_body_selection(self):self.assertEqual(T['T_PARROT']['body_row_count'],13)
 def test_yield_exact_raw_and_display_values(self):
  rows=list(csv.DictReader(io.StringIO(T['T_YIELDS']['CSV'])))
  self.assertEqual(len(rows),4);self.assertEqual([r['input_truncated'] for r in rows],['False']*4)
  self.assertIn('77.59',T['T_YIELDS']['markdown']);self.assertIn('77.58890327412914',T['T_YIELDS']['CSV'])
 def test_timeline_has_three_distinct_objects(self):
  rows=T['T_TIMELINE']['rows'];self.assertEqual(len({r['object'] for r in rows}),3);self.assertEqual(rows[1]['date'],'2026-11-23');self.assertEqual(rows[2]['recorded_status'],0)
 def test_six_valid_synthetic_contracts(self):
  for s in CONFIG['sections']:self.assertTrue(check(s,fixture(s))['structural_pass'],s['id'])
 def test_missing_item_rejected(self):
  s=CONFIG['sections'][4];text=fixture(s).replace('[[item:H_DIFF]]','[[item:FOREIGN]]');self.assertFalse(check(s,text)['structural_pass'])
 def test_comment_only_item_rejected(self):
  s=CONFIG['sections'][4];text=fixture(s);text=text.replace('[[item:H_DIFF]]','<!-- [[item:H_DIFF]]').replace('[[/item]]','[[/item]] -->',1)
  self.assertFalse(check(s,text)['structural_pass'])
 def test_empty_item_rejected(self):
  s=CONFIG['sections'][4];text=fixture(s);a=text.index('Synthetic');b=text.index('[[/item]]',a);text=text[:a]+'ok\n'+text[b:];self.assertFalse(check(s,text)['structural_pass'])
 def test_foreign_citation_12_in_identity_section_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[cite: D12]','[cite: 12]'))['structural_pass'])
 def test_bare_D12_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[cite: D12]','[D12]'))['structural_pass'])
 def test_internal_unit_citation_rejected(self):
  s=CONFIG['sections'][1];self.assertFalse(check(s,fixture(s).replace('[cite: D16]','[checkpoint_eval]'))['structural_pass'])
 def test_table_rewrite_even_equal_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[table: T_PARROT]',T['T_PARROT']['markdown']))['structural_pass'])
 def test_missing_table_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[table: T_PARROT]',''))['structural_pass'])
 def test_duplicate_table_rejected(self):
  s=CONFIG['sections'][0];text=fixture(s).replace('[table: T_PARROT]','[table: T_PARROT]\n[table: T_PARROT]');self.assertFalse(check(s,text)['structural_pass'])
 def test_unknown_figure_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[figure: SCI-ROUTES]','[figure: GUESS]'))['structural_pass'])
 def test_missing_figure_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('[figure: SCI-ROUTES]',''))['structural_pass'])
 def test_missing_caption_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,fixture(s).replace('캡션:','not-caption:',1))['structural_pass'])
 def test_outside_prose_rejected(self):
  s=CONFIG['sections'][0];self.assertFalse(check(s,'outside\n'+fixture(s))['structural_pass'])
 def test_S06_wrong_fragment_ownership_rejected(self):
  s=CONFIG['sections'][5];text=fixture(s).replace('[[item:INTRO]]','[[item:TEMP]]').replace('[[item:CONCLUSION]]','[[item:INTRO]]').replace('[[item:TEMP]]','[[item:CONCLUSION]]');self.assertFalse(check(s,text)['structural_pass'])
 def test_all_thirteen_assemble_once_without_science_rewrite(self):
  results={s['id']:check(s,fixture(s)) for s in CONFIG['sections']};md,record=p.assemble(results,CONFIG,U,R,F,T)
  self.assertEqual(md.count('!['),13);self.assertEqual(len(record['figures']),13);self.assertFalse(record['scientific_prose_rewritten'])
  self.assertIn(T['T_PARROT']['markdown'],md);self.assertIn('[D12](#ref-D12)',md);self.assertIn('PENDING',record['semantic_status'])
 def test_missing_section_blocks_assembly(self):
  with self.assertRaises(ValueError):p.assemble({},CONFIG,U,R,F,T)
 def test_duplicate_cross_section_prose_rejected(self):
  results={s['id']:check(s,fixture(s)) for s in CONFIG['sections']}
  para='A repeated long synthetic prose paragraph with no scientific assertion at all, solely to test duplicate detection across independent owned sections.'
  for sid in ['S01','S02']:results[sid]['fragments'][sid]+='\n\n'+para
  with self.assertRaises(ValueError):p.assemble(results,CONFIG,U,R,F,T)
 def test_review_flag_not_scientific_word_matching_failure(self):
  s=CONFIG['sections'][1];text=fixture(s).replace('Synthetic contract fixture only','잘렸다는 기록이 없다는 의미를 검토하는 합성 예제입니다. Synthetic contract fixture only',1)
  result=check(s,text);self.assertTrue(result['structural_pass']);self.assertTrue(result['review_flags']);self.assertEqual(result['semantic_status'],'PENDING_INDEPENDENT_REVIEW')
 def test_prepare_is_offline_and_requests_use_only_owned_inputs(self):
  with tempfile.TemporaryDirectory() as temp,patch.object(p.urllib.request,'Request',side_effect=AssertionError('Network forbidden')):
   out=Path(temp)/'offline';cost=p.prepare(out,CONFIG);self.assertEqual(cost['actual_calls'],0)
   q=p.load(out/'requests/S05.json');u=json.loads(q['messages'][1]['content'])
   self.assertEqual(set(u['evidence_data']['additional_run_metadata']),{'harness'})
   self.assertNotIn('EDIT_EXISTING',q['messages'][0]['content']);self.assertNotIn('old_block_id',q['messages'][0]['content'])
   self.assertEqual(set(u['allowed_citations']),{'D8'});self.assertNotIn('original_path',q['messages'][1]['content'])
 def test_prepare_refuses_existing_output(self):
  with tempfile.TemporaryDirectory() as temp:
   with self.assertRaises(FileExistsError):p.prepare(Path(temp),CONFIG)
 def test_unapproved_template_cannot_reach_network(self):
  with tempfile.TemporaryDirectory() as temp,patch.object(p.urllib.request,'Request',side_effect=AssertionError('Network forbidden')):
   out=Path(temp)/'offline';p.prepare(out,CONFIG)
   with self.assertRaises(PermissionError):p.execute(out,CONFIG,p.HERE/'approval-template.NOT-APPROVED.json')
 def test_assets_are_exact_source_hashes(self):
  for f in F:self.assertEqual(p.digest(p.HERE/f['asset_path']),f['sha256'])
 def test_assembly_duplicate_fragment_fails(self):
  results={s['id']:check(s,fixture(s)) for s in CONFIG['sections']};results['S02']['fragments']['S01']=results['S01']['fragments']['S01']
  with self.assertRaises(ValueError):p.assemble(results,CONFIG,U,R,F,T)
 def test_scientific_meaning_never_auto_approved(self):
  s=CONFIG['sections'][4];result=check(s,fixture(s));self.assertTrue(result['structural_pass']);self.assertEqual(result['semantic_status'],'PENDING_INDEPENDENT_REVIEW')
