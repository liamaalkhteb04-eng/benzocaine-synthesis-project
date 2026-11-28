"""Offline packaging audit only; never calls a model or evaluates chemistry."""
from pathlib import Path
import json,re,hashlib,ast,zipfile,xml.etree.ElementTree as ET,os
from urllib.parse import unquote,urlsplit
from markdown_it import MarkdownIt
import pymupdf
P=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
required=['report/20251312_리야마_벤조카인_최종보고서.pdf','report/20251312_리야마_벤조카인_최종보고서.docx','report/report.md','archive/baselines/baseline20.md','provenance/final-validation/sentence-edit.json','report/records/source-index.md','report/records/original-content.md','report/records/numeric-formatting.json','report/figure-manifest.render.json','code/render_report_docx.py','code/authoring_contract.py','code/word_export.ps1','code/restore_pdf_source_images.py','code/reflow.ps1','requirements-report.txt','.env.example','README.md','GITHUB_INCLUDE.md','configs/approval.example.json','data/final-facts-overlay.json','provenance/pressure-call/response.raw.json']
missing=[x for x in required if not(P/x).is_file()]
figs=load(P/'report/figure-manifest.render.json');figbad=[]
for f in figs:
 path=P/'report'/f['path']
 if not path.is_file() or sha(path)!=f['sha256']:figbad.append(f['figure_id'])
assert len(figs)==13
links=[];broken=[];parser=MarkdownIt('commonmark').enable('table')
mds=[P/'README.md',P/'GITHUB_INCLUDE.md',P/'STRUCTURE_CHANGES.md',P/'report/report.md',P/'archive/README.md']+list((P/'skill').rglob('*.md'))+list((P/'report/records').glob('*.md'))+list((P/'provenance').glob('*.md'))
def checklink(file,target,kind):
 info=urlsplit(target)
 if info.scheme or target.startswith('#'):return
 part=unquote(info.path)
 if not part:return
 dest=(file.parent/part).resolve();row={'file':str(file.relative_to(P)),'target':target,'kind':kind};links.append(row)
 if not dest.is_relative_to(P) or not dest.is_file():broken.append(row);return
 if info.fragment and dest.suffix=='.md':
  content=dest.read_text(encoding='utf-8-sig')
  # Explicit bibliography/source anchors are checked; ordinary heading slug rules vary by renderer.
  if info.fragment.startswith(('d','ref','c')) and '<a id="'+info.fragment+'"' not in content and '{#'+info.fragment+'}' not in content:broken.append({**row,'reason':'anchor missing'})
for file in mds:
 if not file.exists():continue
 for t in parser.parse(file.read_text(encoding='utf-8-sig')):
  for child in t.children or []:
   if child.type=='link_open':checklink(file,child.attrGet('href'),'Markdown link')
   elif child.type=='image':checklink(file,child.attrGet('src'),'Markdown image')
with zipfile.ZipFile(P/'report/20251312_리야마_벤조카인_최종보고서.docx') as z:
 for name in z.namelist():
  if name.endswith('.rels'):
   for rel in ET.fromstring(z.read(name)):
    if rel.get('TargetMode')=='External':checklink(P/'report/20251312_리야마_벤조카인_최종보고서.docx',rel.get('Target'),'DOCX external target')
with pymupdf.open(P/'report/20251312_리야마_벤조카인_최종보고서.pdf') as pdf:
 for page in pdf:
  for link in page.get_links():
   target=link.get('file') or link.get('uri')
   if target:checklink(P/'report/20251312_리야마_벤조카인_최종보고서.pdf',target,'PDF link')
source_manifest=load(P/'data/evidence/source-manifest.json')
for row in source_manifest['historical_sources']:
 path=P/row['packaged_path']
 if not path.is_file() or sha(path)!=row['sha256']:missing.append(row['packaged_path']+' (source manifest/hash)')
syntax=[]
for f in P.rglob('*.py'):
 if 'work' in f.relative_to(P).parts:continue
 try:ast.parse(f.read_text(encoding='utf-8-sig'))
 except SyntaxError as ex:syntax.append({'file':str(f.relative_to(P)),'line':ex.lineno})
# Do not print or record secret values. Exact environment keys are compared in memory only.
known=[os.environ[k].encode() for k in ['UPSTAGE_API_KEY','OPENAI_API_KEY'] if os.environ.get(k)]
secret_files=[];forbidden=[]
for f in P.rglob('*'):
 if not f.is_file() or 'work' in f.relative_to(P).parts:continue
 rel=str(f.relative_to(P)).replace('\\','/')
 if f.name.startswith('.env') and f.name!='.env.example':forbidden.append(rel)
 data=f.read_bytes();samples=[data]
 if f.suffix=='.docx':
  with zipfile.ZipFile(f) as z:samples += [z.read(n) for n in z.namelist() if n.endswith(('.xml','.rels'))]
 for sample in samples:
  if any(k and k in sample for k in known):secret_files.append({'file':rel,'type':'exact environment credential match'});break
  if re.search(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-proj-|sk-svcacct-)[A-Za-z0-9_-]{20,}|\bAKIA[A-Z0-9]{16}\b',sample):secret_files.append({'file':rel,'type':'credential signature'});break
  if f.suffix in ['.json','.md','.txt'] and re.search(rb'(?i)["\x27](?:authorization|api_key|access_token|secret_access_key)["\x27]\s*:\s*["\x27](?:Bearer\s+)?[A-Za-z0-9_./+=-]{20,}',sample):secret_files.append({'file':rel,'type':'literal credential-field candidate'});break
absolute_runtime=[]
for f in list((P/'code').glob('*.py'))+list((P/'code').glob('*.ps1'))+list((P/'configs').rglob('*.json')):
 if re.search(r'[A-Z]:[\\/]',f.read_text(encoding='utf-8-sig')):absolute_runtime.append(str(f.relative_to(P)))
record={'pass':not(missing or figbad or broken or syntax or secret_files or forbidden or absolute_runtime),'required_file_missing':missing,'figure_count':13,'figure_hash_failures':figbad,'checked_local_links':len(links),'broken_local_links':broken,'Python_syntax_errors':syntax,'literal_secret_candidates':secret_files,'forbidden_env_files':forbidden,'absolute_runtime_paths':absolute_runtime,'scope':'Offline packaging/path/credential checks; no completed scientific analysis repeated. Historical non-link origin strings are provenance, not runtime paths.','Solar_calls':0,'images_note':'13 scientific images are exact previously reviewed files; no new image OCR performed.'}
save(P/'validation/package-check.json',record)
print(json.dumps({'pass':record['pass'],'missing':len(missing),'broken_links':len(broken),'secret_candidates':len(secret_files),'syntax_errors':len(syntax),'absolute_runtime_paths':absolute_runtime}))
if not record['pass']:raise SystemExit(1)
