from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
TEXT_SUFFIXES={'.json','.md','.txt','.csv','.py','.ps1','.yml','.yaml','.toml','.cfg','.ini','.sh','.log'}
EMAIL=re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I)
# Match serialized/plain Windows profile roots, including JSON-escaped backslashes.
HOME=re.compile(r'C:(?:\\)+Users(?:\\)+[^\\/"\s]+',re.I)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);a=ap.parse_args();root=a.package.resolve()
 smp=root/'provenance/package-source-map.json';rmp=root/'provenance/package-redaction-map.json'
 sm=json.loads(smp.read_text(encoding='utf-8')); rm=json.loads(rmp.read_text(encoding='utf-8'))
 source_by_path={x['package_path']:x for x in sm.get('files',[])}
 changes=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES or p in {smp,rmp}:continue
  try:old=p.read_text(encoding='utf-8-sig')
  except (UnicodeDecodeError,OSError):continue
  new=HOME.sub('<USER_HOME>',old)
  new=EMAIL.sub('<EMAIL_REDACTED>',new)
  if new==old:continue
  before=sha(p);p.write_text(new,encoding='utf-8',newline='\n');after=sha(p)
  rel=p.relative_to(root).as_posix();src=source_by_path.get(rel,{})
  changes.append({'package_path':rel,'source_sha256':src.get('source_sha256'),'pre_redaction_package_sha256':before,'package_sha256':after,'redactions':['Windows user-profile path anonymized','email address redacted'] if EMAIL.search(old) else ['Windows user-profile path anonymized'],'source_file_preserved':True})
  if rel in source_by_path:
   src['package_sha256']=after;src['bytes']=p.stat().st_size;src['redacted_derivative']=True
 sm['status']='updated_after_public_copy_anonymization';smp.write_text(json.dumps(sm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 prior=rm.get('redactions',[]); by={x['package_path']:x for x in prior}
 for x in changes:by[x['package_path']]=x
 rm['status']='updated';rm['note']='Source originals were preserved. This map records source and package-copy hashes for anonymized derivatives; PACKAGE-MANIFEST hashes the final copied bytes.';rm['redactions']=list(by.values())
 rmp.write_text(json.dumps(rm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'changed_text_files':len(changes),'redacted_path_or_email_values':True,'changed_paths':[x['package_path'] for x in changes]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
