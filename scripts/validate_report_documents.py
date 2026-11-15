"""Future DOCX/PDF check against target-specific evidence. Does not create reports."""
import argparse
from pathlib import Path
import zipfile
import pymupdf
from _runtime import load,save,digest
from validate_report_content import check_content

def main():
    p=argparse.ArgumentParser();p.add_argument('--report-dir',required=True,type=Path);p.add_argument('--attempt-dir',required=True,type=Path);p.add_argument('--run-dir',required=True,type=Path);a=p.parse_args()
    folder=a.report_dir;md=folder/'report.md';text=md.read_text(encoding='utf-8');response=load(a.attempt_dir/'solar-response.raw.json');status=load(a.attempt_dir/'solar-status.json')
    assert status['status']=='success' and response['model'].startswith('solar-pro4')
    assert text==response['choices'][0]['message']['content'],'Solar original text modified'
    evidence=load(a.run_dir/'report-evidence.json');check=check_content(text,evidence);assert not check['errors'],check['errors']
    expected=len(evidence['report_figure_assets']);export=load(folder/'docx-export.json')
    assert export['markdown_sha256']==digest(md) and len(export['images'])==expected
    with zipfile.ZipFile(folder/'report.docx') as z:
        assert len([n for n in z.namelist() if n.startswith('word/media/')])==expected
    doc=pymupdf.open(folder/'report.pdf');word=load(folder/'word-export.json')
    assert len(doc)==word['pages'] and len(doc)<=evidence['report_plan']['maximum_pages_including_references']
    flat=''.join(''.join(p.get_text().split()) for p in doc)
    assert '모델예측' in flat and '실험' in flat
    for s in evidence['report_steps']:
        assert s['route_id'] in flat and s['step_id'] in flat
        if s['yield_prediction'] and s['yield_prediction'].get('yield_percent') is not None:
            assert (f"{s['yield_prediction']['yield_percent']:.1f}" in flat or f"{s['yield_prediction']['yield_percent']:.2f}" in flat)
    images=[];outside=[];urls=set();preview=folder/'validation-previews';preview.mkdir(exist_ok=True)
    for i,page in enumerate(doc,1):
        for img in page.get_image_info():
            assert page.rect.contains(pymupdf.Rect(img['bbox']));images.append({'page':i,'bbox':img['bbox']})
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    b=pymupdf.Rect(span['bbox'])
                    if b.x0 < -1 or b.y0 < -1 or b.x1>page.rect.width+1 or b.y1>page.rect.height+1:outside.append(i)
        urls.update(l['uri'] for l in page.get_links() if l.get('uri','').startswith('http'))
        page.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(preview/f'page-{i:02d}.png')
    assert len(images)==expected and not outside
    assert all(r['url'] in urls for r in evidence['required_references'])
    save(folder/'document-validation.json',{'status':'passed','author':response['model'],'solar_text_unchanged':True,'page_count':len(doc),'figure_count':expected,'step_count':len(evidence['report_steps']),'visual_review':'pending','reference_count':len(evidence['required_references']),'source_accessibility':'Not probed; links structurally checked','files':{n:digest(folder/n) for n in ['report.md','report.docx','report.pdf']}})

if __name__=='__main__':main()
