"""Six scoped Solar calls, immutable code tables, strict contracts and deterministic assembly.
Default build is OFFLINE. Network is reachable only with --execute and scoped approval.
"""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime,timezone
from collections import Counter
import argparse,csv,hashlib,io,json,re,os,sys,urllib.request,urllib.error,html,shutil

HERE=Path(__file__).resolve().parent
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dumps(x):return json.dumps(x,ensure_ascii=False,indent=2)
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(x if isinstance(x,str) else dumps(x),encoding='utf-8')
def clean(s):return re.sub(r'<!--.*?-->','',s,flags=re.S)
def markdown_table(columns,rows):
 def cell(x):return str(x if x is not None else '미확인').replace('|','\\|').replace('\n','<br>')
 return '\n'.join(['| '+' | '.join(columns)+' |','| '+' | '.join('---' for _ in columns)+' |']+['| '+' | '.join(cell(r.get(k,'')) for k in columns)+' |' for r in rows])
def table_record(id,owner,columns,rows,cites,body_rows=None):
 stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=columns,lineterminator='\n');writer.writeheader();writer.writerows([{c:r.get(c,'') for c in columns} for r in rows])
 csvtext=stream.getvalue();body=markdown_table(columns,body_rows if body_rows is not None else rows)
 return {'id':id,'owner':owner,'columns':columns,'rows':rows,'CSV':csvtext,'csv_SHA256':hashlib.sha256(csvtext.encode()).hexdigest(),'markdown':body,'markdown_SHA256':hashlib.sha256(body.encode()).hexdigest(),'cites':cites,'body_row_count':len(body_rows if body_rows is not None else rows)}

def make_tables(units):
 """No inferred experimental facts. Raw CSVs remain lossless; display formatting separate."""
 d={k:v['data'] for k,v in units.items()};tables=[]
 cols=['route_id','step_id','rank','catalyst1','solvent1','solvent2','reagent1','reagent2','sequence_score']
 rows=d['parrot_candidates']
 # Prespecified body selection; all60 records retained in CSV and writer evidence.
 selected=[r for r in rows if int(r['rank'])<=3 or (r['route_id']=='route-01' and int(r['rank'])==4)]
 display=[]
 for r in selected:
  rr=dict(r);rr['sequence_score']=f"{D(str(r['sequence_score'])):.4f}";display.append(rr)
 tables.append(table_record('T_PARROT','S01',cols,rows,['D1'],display))
 tables.append(table_record('T_IDENTITIES','S01',['smiles','rdkit_formula','identity','pubchem_cid'],d['token_identity'],['D12']))
 yields=[]
 for s in d['routes_and_steps']['steps']:
  y=s['yield_record'];yields.append({'route_id':s['route_id'],'step_id':s['step_id'],**{k:y[k] for k in ['raw_value','yield_percent','input_tokens','max_input_tokens','input_truncated','conditions_in_input']}})
 yd=[{**r,'raw_value':f"{D(str(r['raw_value'])):.8f}",'yield_percent':f"{D(str(r['yield_percent'])):.2f}"} for r in yields]
 tables.append(table_record('T_YIELDS','S02',list(yields[0]),yields,['D1','D16'],yd))
 c=d['checkpoint_eval'];n=d['normalization']
 stats=[{'field':k,'value':v} for k,v in {'checkpoint':c['checkpoint'],'R2':c['stored_eval_results']['r2'],'eval_loss':c['stored_eval_results']['eval_loss'],'train_rows':c['public_table_counts']['train'],'test_rows':c['public_table_counts']['test'],'normalization_mean':n['training_yield_mean'],'normalization_std':n['training_yield_std'],'saved_epochs':c['saved_checkpoint_args']['num_train_epochs'],'current_default_epochs':c['current_training_defaults']['num_train_epochs']}.items()]
 tables.append(table_record('T_MODEL','S02',['field','value'],stats,['8','21','D16']))
 tables.append(table_record('T_REVIEW','S02',['route_id','step_id','support','limitations','correctness_verdict'],d['yield_review_steps'],['D16']))
 timeline=[{'object':'historical_execution','date':'2026-10-31','recorded_status':d['routes_and_steps']['steps'][0]['yield_record']['applicability']},
           {'object':'official_method_review','date':c['method_source_review_completed_date'],'recorded_status':'completed'},
           {'object':'new_benzocaine_experimental_validation_records','date':'','recorded_status':len(c['new_benzocaine_experimental_validation_records'])}]
 tables.append(table_record('T_TIMELINE','S02',['object','date','recorded_status'],timeline,['D1','D16']))
 m=d['mcmaster_procedure'];lit=[]
 for r in d['primary_literature']:
  lit.append({'record':r['key'],'substrate':r['starting_material'],'catalyst':r['catalyst'],'solvent':r['solvent'],'temperature':r['temperature'],'time':r['time'],'yield':r['yield']['reported'],'yield_basis':r['yield']['basis']})
 lit.append({'record':'McMaster','substrate':m['substrate'],'catalyst':str(m['concentrated_H2SO4_volume_ml'])+' mL conc H2SO4','solvent':f"{m['ethanol_volume_ml']} mL {m['ethanol_percent']}% ethanol",'temperature':'reflux','time':str(m['reflux_minutes'])+' min','yield':m['representative_isolated_yield_percent'],'yield_basis':'대표 분리수율 미확인'})
 tables.append(table_record('T_LITERATURE','S03',list(lit[0]),lit,['18','19','22']))
 for tid,key,cols,cites in [
  ('T_MOPAC','mopac_all_conformers',['species_id','conformer_index','energy_quantity','raw_heat_kcal_mol','relative_heat_kcal_mol','energy_unit','comparison_eligible'],['D5']),
  ('T_EPI','epi_data',['species_id','property','series','value_celsius','unit','availability','classification'],['D6']),
  ('T_VISUALIZER','visualizer_measurements',['measurement_id','conformer_index','atoms_visualizer_names','measurement','value','unit'],['D7'])]:
  tables.append(table_record(tid,'S04',cols,d[key],cites))
 hr=[]
 for r in d['additional_run_metadata']['harness']:
  hr.append({'run':r['run'],**r['settings'],'system_bytes':r['message_bytes_by_role']['system'],'user_bytes':r['message_bytes_by_role']['user'],'roles':','.join(r['message_role_sequence']),'containers':','.join(r['content_container_types']),'assistant_bytes':r['assistant_message_bytes'],'tools_key_present':r['tools_key_present']})
 tables.append(table_record('T_HARNESS','S05',list(hr[0]),hr,['D8']))
 return {t['id']:t for t in tables}

def context_data(config):
 units=load(HERE/'data/evidence-units.json');registry=load(HERE/'data/citation-registry.json');figures=load(HERE/'data/figure-manifest.json')
 return units,registry,figures,make_tables(units)
def writer_projection(value):
 """Keep scientific values/locations; move local paths/hashes/extraction logs to audit data."""
 excluded={'original_path','source_file','raw_file','input_file','out','raw_heat_line','heat_line','source_pointer','screen_evidence','structure_file','template_hash','system_sha256','user_sha256','evidence_ids','source_locations'}
 if isinstance(value,dict):return {k:writer_projection(v) for k,v in value.items() if k not in excluded and not k.endswith('sha256')}
 if isinstance(value,list):return [writer_projection(v) for v in value]
 return value
def bundle_hash():
 paths=[HERE/'config.json',HERE/'skill/SKILL.md',HERE/'report_pipeline.py']+sorted((HERE/'data').glob('*'))
 return hashlib.sha256(dumps({str(p.relative_to(HERE)):digest(p) for p in paths if p.is_file()}).encode()).hexdigest()
def latest_cumulative(config,out=None):
 repo=(HERE/config['repository_relative']).resolve()
 candidates=[load(HERE/'data/ledger-baseline.json')['project_cumulative_conservative_USD']]
 for p in (repo/'reports').glob('**/cumulative-ledger-after.json'):
  try:
   d=load(p)
   if isinstance(d.get('project_cumulative_conservative_USD'),(int,float)):candidates.append(d['project_cumulative_conservative_USD'])
  except (OSError,ValueError):continue
 return D(str(max(candidates)))
def cost_upper(request,config):
 size=sum(len(m['content'].encode()) for m in request['messages']);proxy=size+2048
 price=config['price'];amount=(D(proxy)*D(str(price['input_per_M']))+D(request['max_tokens'])*D(str(price['output_per_M'])))*D('1.10')/D(1000000)
 return {'input_bytes':size,'input_byte_proxy':proxy,'max_output_tokens':request['max_tokens'],'context_proxy':proxy+request['max_tokens'],'upper_USD_VAT':float(amount),'exact_token_count':None}

def prepare(out,config):
 out=Path(out)
 if out.exists():raise FileExistsError('Choose a fresh output folder; existing run is preserved')
 units,registry,figures,tables=context_data(config);system=(HERE/'skill/SKILL.md').read_text(encoding='utf-8')
 out.mkdir(parents=True);save(out/'bundle.json',{'bundle_SHA256':bundle_hash(),'mode':'OFFLINE_PREPARATION','Solar_calls':0})
 source_index=[]
 for key,entry in registry.items():
  source_index+=['<a id="ref-'+key+'"></a>','## '+key,entry['title']]
  for data_key in entry.get('source_unit_ids',[]):
   save(out/f'provenance/units/{data_key}.json',units[data_key]);source_index.append('- ['+data_key+'](units/'+data_key+'.json)')
  if entry.get('url'):source_index.append(entry['url'])
 save(out/'provenance/source-index.md','\n\n'.join(source_index))
 for f in figures:
  src=HERE/f['asset_path'];dest=out/f['asset_path'];dest.parent.mkdir(parents=True,exist_ok=True)
  if digest(src)!=f['sha256']:raise ValueError('Asset snapshot mismatch')
  shutil.copyfile(src,dest)
 for tid,t in tables.items():
  save(out/f'tables/{tid}.csv',t['CSV']);save(out/f'tables/{tid}.md',t['markdown'])
 costs=[]
 for section in config['sections']:
  data={}
  for key in section['source_units']:
   datum=json.loads(dumps(units[key]['data']))
   if key=='additional_run_metadata':datum={'harness':datum['harness']} if section['id']=='S05' else {k:datum[k] for k in ['mopac','epi']}
   data[key]=writer_projection(datum)
  # Avoid repeating the exact same raw rows as CSV table evidence.
  for tid in section['tables']:
   key=config['table_source_units'].get(tid)
   if key:data.pop(key,None)
  fixed={tid:{k:tables[tid][k] for k in ['id','CSV','csv_SHA256','body_row_count','cites']} for tid in section['tables']}
  user={'section_contract':section,'evidence_data':data,'fixed_tables':fixed,
        'allowed_citations':{k:{field:registry[k][field] for field in ['title','url','supports'] if field in registry[k]} for k in section['allowed_citations']},
        'owned_figures':[f for f in figures if f['figure_id'] in section['figures']],
        'figure_pixels_sent':False,'data_keys_are_not_citations':True,
        'no_prior_manuscripts_or_Solar_sentences':True}
  req={'model':config['model'],'messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(user,ensure_ascii=False,separators=(',',':'))}],
       'temperature':0,'reasoning_effort':'none','max_tokens':section['max_output_tokens'],'n':1,'stream':False}
  save(out/f'requests/{section["id"]}.json',req)
  c=cost_upper(req,config);c.update(section_id=section['id'],request_SHA256=digest(out/f'requests/{section["id"]}.json'));costs.append(c)
 total=sum((D(str(c['upper_USD_VAT'])) for c in costs),D(0));cum=latest_cumulative(config)
 report={'per_section':costs,'all_six_upper_USD_VAT':float(total),'price_basis':config['price'],'project_cumulative_USD':float(cum),'project_cap_USD':1.5,'project_remaining_USD':float(D('1.5')-cum),'fits_project_cap':cum+total<=D('1.5'),'all_contexts_fit_512000':all(c['context_proxy']<=512000 for c in costs),'automatic_retries':0,'actual_calls':0,'approval_for_calls':False,'scope':'prepared bytes +2048 framing proxy; actual tokenizer/server not measured'}
 save(out/'cost-and-limits.json',report);save(out/'table-manifest.json',{k:{f:v for f,v in t.items() if f not in ['CSV','markdown','rows']} for k,t in tables.items()})
 return report

def span(text,tag):
 pat=r'\[\[BEGIN:'+re.escape(tag)+r'\]\](.*?)\[\[END:'+re.escape(tag)+r'\]\]'
 matches=list(re.finditer(pat,text,re.S))
 if len(matches)!=1:raise ValueError('Expected one fragment '+tag)
 return matches[0].group(1).strip(),matches[0].span()
def validate(section,text,config,units,registry,figures,tables):
 errors=[];warnings=[];fragments={};allspans=[]
 for tag in section['fragments']:
  try:body,s=span(text,tag);fragments[tag]=body;allspans.append(s)
  except ValueError as e:errors.append(str(e))
 outside=text
 for a,b in sorted(allspans,reverse=True):outside=outside[:a]+outside[b:]
 if outside.strip():errors.append('Output outside owned fragments')
 if errors:return {'structural_pass':False,'errors':errors,'semantic_status':'NOT_REVIEWED','fragments':fragments}
 body='\n\n'.join(fragments.values());visible=clean(body)
 found=re.findall(r'^\[\[item:([^\]\n]+)\]\]\s*$',visible,re.M)
 expected=[x['id'] for x in section['items']]
 if Counter(found)!=Counter(expected):errors.append('Missing, duplicate or foreign required item IDs')
 for tag,owned_items in section.get('fragment_item_ownership',{}).items():
  actual=re.findall(r'^\[\[item:([^\]\n]+)\]\]\s*$',clean(fragments.get(tag,'')),re.M)
  if Counter(actual)!=Counter(owned_items):errors.append('Item in wrong fragment '+tag)
 for item in section['items']:
  matches=list(re.finditer(r'^\[\[item:'+re.escape(item['id'])+r'\]\]\s*\n(.*?)^\[\[/item\]\]\s*$',visible,re.M|re.S))
  if len(matches)!=1:errors.append('Malformed item '+item['id']);continue
  prose=matches[0][1]
  if any('[cite: '+c+']' not in prose and '[cite:'+c+']' not in prose for c in item.get('required_cites',[])):errors.append('Missing item-specific citation '+item['id'])
  prose=re.sub(r'\[(?:cite|figure|table):[^\]]+\]','',prose);prose=re.sub(r'^캡션:.*$','',prose,flags=re.M)
  if len(re.sub(r'[\W\d_]','',prose))<20:errors.append('No explanatory body in '+item['id'])
 cites=re.findall(r'\[cite:\s*([^\]\n]+)\]',visible)
 if set(cites)-set(section['allowed_citations']):errors.append('Unknown/foreign citation ID')
 # Source keys and bare citation numbers are forbidden; chemical structures stay in inline code.
 no_code=re.sub(r'`[^`\n]+`','',visible)
 for m in re.finditer(r'\[([^\]\n]+)\]',no_code):
  val=m[1]
  if val in units or re.fullmatch(r'D\d+|\d+(?:,\s*\d+)*',val):errors.append('Bare or internal-data citation: '+val)
 if re.search(r'^#{1,6}\s*참고문헌',visible,re.M):errors.append('Model must not rewrite canonical bibliography')
 tableids=re.findall(r'^\[table:\s*([^\]\n]+)\]\s*$',visible,re.M)
 if Counter(tableids)!=Counter(section['tables']):errors.append('Missing, duplicate or foreign immutable table markers')
 if re.search(r'^\s*\|',visible,re.M):errors.append('Model rewrote a code-owned table')
 if re.search(r'!\[|^\[(?:그림|Figure)\s*\d',visible,re.M):errors.append('Unsupported figure format')
 figureids=re.findall(r'^\[figure:\s*([^\]\n]+)\]\s*$',visible,re.M)
 if Counter(figureids)!=Counter(section['figures']):errors.append('Missing, duplicate or foreign figure IDs')
 for fid in figureids:
  if not re.search(r'^\[figure:\s*'+re.escape(fid)+r'\]\s*\n\s*캡션:\s*[^\n]+',visible,re.M):errors.append('Missing Solar caption '+fid)
 for f in figures:
  if f['figure_id'] in section['figures'] and digest(HERE/f['asset_path'])!=f['sha256']:errors.append('Asset hash mismatch '+f['figure_id'])
 # These are review flags, not word-matching scientific decisions.
 if re.search(r'잘렸|절단되었|truncated\s*[:=]\s*true',visible,re.I):warnings.append('Review actual truncation assertion against four false records; wording/negation requires semantic review')
 if section['id']=='S01' and re.search(r'reagent1[^\n]{0,100}FB\(F\)F',visible):warnings.append('Review BF3 slot against reagent2; do not auto-rewrite')
 return {'structural_pass':not errors,'errors':sorted(set(errors)),'review_flags':warnings,'semantic_status':'PENDING_INDEPENDENT_REVIEW','fragments':fragments,'cited_IDs':sorted(set(cites))}

def assemble(results,config,units,registry,figures,tables):
 if set(results)!=set(s['id'] for s in config['sections']):raise ValueError('Missing section results')
 for sid,result in results.items():
  if not result['structural_pass']:raise ValueError('Structural failure '+sid)
 fragments={};seen=Counter();seen_tables=Counter();paragraphs={};dup=[]
 for sid,result in results.items():
  for tag,body in result['fragments'].items():
   if tag in fragments:raise ValueError('Duplicate owned fragment '+tag)
   fragments[tag]=body
   seen.update(re.findall(r'^\[figure:\s*([^\]\n]+)\]\s*$',body,re.M));seen_tables.update(re.findall(r'^\[table:\s*([^\]\n]+)\]\s*$',body,re.M))
   # Only prose paragraphs; repeated essential captions are checked via asset ownership.
   for para in clean(body).split('\n\n'):
    if para.startswith(('[','캡션:','#')):continue
    normalized=re.sub(r'\s+','',para)
    if len(normalized)>=50:
     if normalized in paragraphs and paragraphs[normalized]!=sid:dup.append([paragraphs[normalized],sid,para[:100]])
     paragraphs[normalized]=sid
 if dup:raise ValueError('Duplicate prose across sections: '+dumps(dup))
 if seen!=Counter(f['figure_id'] for f in figures):raise ValueError('Global figure ownership mismatch')
 if seen_tables!=Counter(tables.keys()):raise ValueError('Global table ownership mismatch')
 output='\n\n'.join(fragments[tag] for tag in config['assembly_order'])
 output=re.sub(r'^\[\[item:[^\]\n]+\]\]\s*\n|^\[\[/item\]\]\s*$', '',output,flags=re.M)
 allcites=set(re.findall(r'\[cite:\s*([^\]]+)\]',output))
 def insert_table(m):
  t=tables[m[1]];allcites.update(t['cites']);return t['markdown']+'\n\n'+' '.join('[cite: '+c+']' for c in t['cites'])
 output=re.sub(r'^\[table:\s*([^\]]+)\]\s*$',insert_table,output,flags=re.M)
 assets={f['figure_id']:f for f in figures}
 def insert_figure(m):
  f=assets[m[1]]
  return '!['+f['figure_id']+']('+f['asset_path']+')\n\n'+m[2]
 output=re.sub(r'^\[figure:\s*([^\]\n]+)\]\s*\n\s*캡션:\s*([^\n]+)',insert_figure,output,flags=re.M)
 output=re.sub(r'\[cite:\s*([^\]]+)\]',lambda m:'['+m[1]+'](#ref-'+m[1]+')',output)
 output+='\n\n## 참고문헌\n\n'
 for key in sorted(allcites,key=lambda k:(not k.isdigit(),int(k) if k.isdigit() else k)):
  r=registry[key];output+='<a id="ref-'+key+'"></a>\n\n- ['+key+'] '+r['title']+('. '+r['url'] if r.get('url','').startswith('http') else '')+' [근거 대응](provenance/source-index.md#ref-'+key+')\n\n'
 return output,{'figures':dict(seen),'tables':dict(seen_tables),'duplicate_prose':dup,'fragments':list(fragments),'scientific_prose_rewritten':False,'semantic_status':'PENDING_INDEPENDENT_REVIEW'}

def audit_run(out,config):
 if load(Path(out)/'bundle.json')['bundle_SHA256']!=bundle_hash():raise ValueError('Bundle changed since request preparation')
 units,registry,figures,tables=context_data(config);results={}
 for section in config['sections']:
  p=Path(out)/'responses'/f'{section["id"]}.json'
  if not p.exists():raise ValueError('Missing actual response '+section['id'])
  r=load(p)
  if r.get('model') not in ['solar-pro4-260806','solar-pro-4-260806'] or r['choices'][0].get('finish_reason')!='stop':raise ValueError('Incomplete or wrong-model response')
  text=r['choices'][0]['message']['content']
  results[section['id']]=validate(section,text,config,units,registry,figures,tables)
  save(Path(out)/'validation'/f'{section["id"]}.json',results[section['id']])
 assembled,record=assemble(results,config,units,registry,figures,tables)
 save(Path(out)/'candidate.NOT-VERIFIED.md',assembled);save(Path(out)/'validation/assembly.json',record)
 save(Path(out)/'semantic-review-template.json',{'approved':False,'candidate_SHA256':digest(Path(out)/'candidate.NOT-VERIFIED.md'),'bundle_SHA256':bundle_hash(),'section_response_SHA256':{s['id']:digest(Path(out)/'responses'/f'{s["id"]}.json') for s in config['sections']},'required_review':['each required item actual source support','past run versus completed review versus unvalidated accuracy','BF3 reagent2 and correct D12 identity citation','harness actual setting differences','cross-section numeric/route/limitation consistency','caption/data/figure agreement'],'note':'Structural checks and markers do NOT establish scientific accuracy or semantic completeness. No final report export until independent review.'})
 return record

class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
def execute(out,config,approval):
 """Future approved six-call run only. This function is never used by offline preparation/tests."""
 out=Path(out);auth=load(approval);cost=load(out/'cost-and-limits.json')
 if auth.get('approved') is not True or auth.get('bundle_SHA256')!=bundle_hash():raise PermissionError('Approval must match this exact bundle')
 if auth.get('max_calls')!=6 or auth.get('free_credit_only') is not True or auth.get('automatic_retries')!=0:raise PermissionError('Approval scope mismatch')
 if D(str(auth.get('project_cap_USD',0)))!=D('1.50'):raise PermissionError('Project cap mismatch')
 workcap=D(str(auth['work_cap_USD_VAT']));total=D(str(cost['all_six_upper_USD_VAT']))
 if total>workcap or latest_cumulative(config)+total>D('1.50'):raise ValueError('Insufficient work/project budget')
 expires=datetime.fromisoformat(auth['free_credit_expiry_UTC'].replace('Z','+00:00'))
 if datetime.now(timezone.utc)>=expires or D(str(auth['free_credit_conservative_available_USD']))<total:raise ValueError('Free credits insufficient/expired')
 if auth.get('official_free_first_rule_confirmed') is not True:raise PermissionError('Credit-only basis missing')
 key=os.environ.get('UPSTAGE_API_KEY','').strip()
 if not key:raise RuntimeError('UPSTAGE_API_KEY is unavailable; no request sent')
 global_claim=HERE/'approval-claims'/f'{digest(approval)}.claim';global_claim.parent.mkdir(exist_ok=True)
 with global_claim.open('x') as f:f.write(datetime.now(timezone.utc).isoformat())
 units,registry,figures,tables=context_data(config);used=D(0);base=latest_cumulative(config)
 for call_number,(section,c) in enumerate(zip(config['sections'],cost['per_section']),1):
  sid=section['id'];requestfile=out/'requests'/f'{sid}.json'
  if digest(requestfile)!=c['request_SHA256']:raise ValueError('Request bytes changed')
  remaining=sum((D(str(x['upper_USD_VAT'])) for x in cost['per_section'] if x['section_id']>=sid),D(0))
  if used+remaining>workcap or latest_cumulative(config)+remaining>D('1.50'):raise ValueError('Budget changed; stopped before POST')
  claim=out/'attempts'/f'{sid}.claim';claim.parent.mkdir(exist_ok=True)
  with claim.open('x') as f:f.write(datetime.now(timezone.utc).isoformat())
  raw=b'';http=None;error=None
  try:
   req=urllib.request.Request('https://api.upstage.ai/v1/chat/completions',data=requestfile.read_bytes(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
   with urllib.request.build_opener(NoRedirect).open(req,timeout=1200) as res:http=res.status;raw=res.read()
  except urllib.error.HTTPError as e:http=e.code;raw=e.read();error='HTTPError'
  except Exception as e:error=type(e).__name__
  raw=raw.replace(key.encode(),b'[REDACTED]');rp=out/'responses'/f'{sid}.json';rp.parent.mkdir(exist_ok=True);rp.write_bytes(raw)
  try:r=json.loads(raw)
  except ValueError:r={}
  usage=r.get('usage',{});it,ot=usage.get('prompt_tokens'),usage.get('completion_tokens');priced=None
  if isinstance(it,int) and isinstance(ot,int) and it>=0 and 0<=ot<=section['max_output_tokens']:priced=(D(it)*D(str(config['price']['input_per_M']))+D(ot)*D(str(config['price']['output_per_M'])))*D('1.10')/D(1000000)
  charge=priced if priced is not None else D(str(c['upper_USD_VAT']));used+=charge
  save(out/'execution/cumulative-ledger-after.json',{'prior_project_USD':float(base),'work_accounted_USD_VAT':float(used),'project_cumulative_conservative_USD':float(base+used),'project_cap_USD':1.5,'remaining_reserved_USD_VAT':float(max(D(0),remaining-D(str(c['upper_USD_VAT'])))),'status':'RUNNING_OR_PENDING_REVIEW','actual_Console_debit':None,'calls':call_number,'retries':0,'Paid_with_credits':None,'Postpaid':None})
  save(out/'bundle.json',{'bundle_SHA256':bundle_hash(),'mode':'ACTUAL_SCOPED_CALL_RUN','Solar_calls':call_number,'semantic_status':'PENDING_INDEPENDENT_REVIEW'})
  save(out/'execution'/f'{sid}.json',{'http':http,'usage':usage,'usage_priced_USD_VAT':float(priced) if priced is not None else None,'accounted_USD_VAT':float(charge),'error':error,'POST_attempts':1,'retries':0})
  if http!=200 or priced is None or priced>D(str(c['upper_USD_VAT'])) or r.get('model') not in ['solar-pro4-260806','solar-pro-4-260806'] or (r.get('choices') or [{}])[0].get('finish_reason')!='stop':raise RuntimeError('Transport/usage/model failure; remaining calls stopped')
  text=r['choices'][0]['message']['content'];check=validate(section,text,config,units,registry,figures,tables);save(out/'validation'/f'{sid}.json',check)
  if not check['structural_pass'] or check.get('review_flags'):raise RuntimeError('Section contract/review flag; remaining calls stopped without retry')
 record=audit_run(out,config)
 ledger=load(out/'execution/cumulative-ledger-after.json');ledger.update(closed=True,remaining_reserved_USD_VAT=0,status='SIX_DRAFTS_PENDING_SEMANTIC_REVIEW');save(out/'execution/cumulative-ledger-after.json',ledger)
 return record

def main():
 parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
 b=sub.add_parser('build');b.add_argument('--out',type=Path,required=True);b.add_argument('--execute',action='store_true');b.add_argument('--approval',type=Path)
 a=sub.add_parser('audit');a.add_argument('--out',type=Path,required=True)
 t=sub.add_parser('selftest')
 args=parser.parse_args();config=load(HERE/'config.json')
 if args.command=='selftest':
  import unittest
  suite=unittest.defaultTestLoader.discover(str(HERE/'tests'));result=unittest.TextTestRunner(verbosity=2).run(suite)
  save(HERE/'offline-test-results.json',{'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'pass':result.wasSuccessful(),'fixtures':'synthetic only, not Solar-authored prose','Solar_calls':0});sys.exit(0 if result.wasSuccessful() else 1)
 if args.command=='audit':print(dumps(audit_run(args.out,config)));return
 # Never create a live request just because the default offline build was invoked.
 if args.execute and not args.approval:raise PermissionError('Explicit bundle-scoped approval required before --execute')
 report=prepare(args.out,config)
 if args.execute:
  try:print(dumps(execute(args.out,config,args.approval)))
  except Exception:
   ledger=args.out/'execution/cumulative-ledger-after.json'
   if ledger.exists():v=load(ledger);v.update(closed=True,remaining_reserved_USD_VAT=0,status='STOPPED_NO_RETRY');save(ledger,v)
   raise
 else:print(dumps(report))
if __name__=='__main__':main()
