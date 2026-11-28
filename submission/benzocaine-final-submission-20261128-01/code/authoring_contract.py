from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parents[1]/'report'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prepare_generated_text(markdown_path,response_path):
 proof=json.loads((HERE.parent/'provenance/final-validation/sentence-edit.json').read_text(encoding='utf-8'))
 base=(HERE.parent/'archive/baselines/baseline20.md').read_text(encoding='utf-8');assert sha(HERE.parent/'archive/baselines/baseline20.md')==proof['source_report_SHA256']
 assert sha(HERE.parent/'provenance/pressure-call/response.raw.json')==proof['raw_response_SHA256']
 assert base.count(proof['before'])==1
 expected=base.replace(proof['before'],proof['accepted_sentence'],1)
 assert expected==Path(markdown_path).read_text(encoding='utf-8') and sha(markdown_path)==proof['corrected_report_SHA256']
 for f in json.loads((HERE/'figure-manifest.render.json').read_text(encoding='utf-8')):assert sha(HERE/f['path'])==f['sha256']
 return expected,{'type':'one authorized source-verified Solar replacement; citation-only normalization','all_other_scientific_text_unchanged':True,'new_Solar_calls':1}
