"""Deterministic report checks tied to the current evidence bundle."""
import re
from pathlib import Path
from markdown_it import MarkdownIt
import json
from audit_citations import audit as audit_citations

KOREAN_YIELD='\uC218\uC728'
KOREAN_PREDICTION='\uC608\uCE21'
KOREAN_EXPERIMENT='\uC2E4\uD5D8'
KOREAN_EVIDENCE='\uC99D\uAC70 \uC790\uB8CC'

def check_content(text, evidence, citation_source_map_path=None):
    tokens=MarkdownIt('commonmark').enable('table').parse(text)
    images=[]; tables=[]; i=0
    while i<len(tokens):
        token=tokens[i]
        if token.type=='table_open':
            rows=[]; j=i+1
            while tokens[j].type!='table_close':
                cur=tokens[j]
                if cur.type=='tr_open': rows.append([])
                elif cur.type=='inline' and rows: rows[-1].append(cur.content)
                j+=1
            tables.append(rows)
        if token.type=='inline':
            images.extend(child.attrGet('src') for child in token.children or [] if child.type=='image')
        i+=1
    errors=[]
    required={Path(item['path']).name for item in evidence['report_figure_assets']}
    present=[str(src).replace('\\\\','/').rsplit('/',1)[-1] for src in images]
    if set(present)!=required or len(present)!=len(required): errors.append('Required evidence figures missing, duplicated, or unrecognized')
    names=[evidence['target'].get('name',''),evidence['target'].get('name_ko','')]
    if not any(name and name in text for name in names): errors.append('Target identity missing')
    # A route overview may legitimately repeat predicted step yields. Only the
    # integrated route/step conditions table is required to be unique; identify
    # it by both route and step columns instead of counting every table that
    # happens to include a yield column.
    yield_tables=[table for table in tables if table and table[0]
                  and any(KOREAN_YIELD in cell.lower() or 'yield' in cell.lower() for cell in table[0])
                  and re.search(r'route\s*/\s*step|route_id.*step_id', ' '.join(table[0]).lower())]
    predicted=[step for step in evidence['report_steps'] if step.get('yield_prediction') and step['yield_prediction'].get('yield_percent') is not None]
    if predicted and len(yield_tables)!=1: errors.append('Exactly one step-resolved conditions/yield table is required')
    for step in evidence['report_steps']:
        if step['route_id'] not in text or step['step_id'] not in text: errors.append('Missing selected route/step: '+step['route_id']+'/'+step['step_id'])
        prediction=step.get('yield_prediction')
        if prediction and prediction.get('yield_percent') is not None:
            expected={f"{prediction['yield_percent']:.1f}",f"{prediction['yield_percent']:.2f}"}
            matching=any(step['route_id'] in ' '.join(row) and step['step_id'] in ' '.join(row) and any(value in ' '.join(row) for value in expected) for table in yield_tables for row in table[1:])
            if not matching: errors.append('Predicted yield not matched to route/step: '+step['route_id']+'/'+step['step_id'])
    if predicted and not (KOREAN_PREDICTION in text and KOREAN_EXPERIMENT in text): errors.append('Prediction must be distinguished from experiment')
    for ref in evidence['required_references']:
        if ref['url'] not in text: errors.append('Missing source URL: '+ref['url'])
    known_urls={ref['url'] for ref in evidence['required_references']}
    github={u.rstrip('`.,;:') for u in re.findall(r'https://github\.com/[^\s)>]+',text)}
    if not github<=known_urls: errors.append('Unknown GitHub source URL')
    if '[D1]' not in text or '[D7]' not in text or '[D8]' not in text or 'reproducibility-manifest.json' not in text or 'Project evidence files' not in text and KOREAN_EVIDENCE not in text and '\uD504\uB85C\uC81D\uD2B8 \uC99D\uAC70 \uD30C\uC77C' not in text:
        errors.append('Project evidence citations and evidence-file list are incomplete')
    if any(word in text.lower() for word in ['[insert ', 'todo:', 'write the complete final project report']) or re.search(r'\?{2,}',text): errors.append('Drafting instruction or placeholder exposed')
    # Citation numbering can differ between report revisions. Prefer the map
    # shipped with the report/run being validated; use the project default
    # only when no report-specific map is available.
    source_map_path = Path(citation_source_map_path) if citation_source_map_path else None
    if source_map_path is None or not source_map_path.is_file():
        source_map_path=Path(__file__).resolve().parent.parent/'configs'/'citation-source-map.json'
    citation_result=audit_citations(text,None,json.loads(source_map_path.read_text(encoding='utf-8')))
    errors.extend('Citation audit: '+item for item in citation_result['errors'])
    return {'status':'passed' if not errors else 'failed','errors':errors,'image_count':len(images),'required_image_count':len(required),'table_count':len(tables),'yield_table_count':len(yield_tables),'citation_audit':citation_result}
