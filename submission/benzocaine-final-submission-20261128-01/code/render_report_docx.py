"""Render the exact fresh Solar manuscript to DOCX; no prose rewriting/API calls."""
from pathlib import Path
import sys,json,re,hashlib,argparse
from markdown_it import MarkdownIt
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image
from authoring_contract import prepare_generated_text
HERE=Path(__file__).resolve().parents[1]/'report'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--markdown',type=Path,required=True);ap.add_argument('--solar-response',type=Path,default=None);a=ap.parse_args()
    if a.output.exists():raise FileExistsError('Preserve previous DOCX')
    src=a.markdown;text,provenance=prepare_generated_text(src,a.solar_response)
    manifest=json.loads((HERE/'figure-manifest.render.json').read_text(encoding='utf-8'));assets={Path(x['path']).name:x for x in manifest}
    doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
    sec.left_margin=sec.right_margin=Cm(2);sec.top_margin=sec.bottom_margin=Cm(1.5);sec.header_distance=sec.footer_distance=Cm(.65)
    sizes={'Normal':11,'Title':19,'Heading 1':14,'Heading 2':12,'Heading 3':11,'Caption':10}
    for name,size in sizes.items():
        st=doc.styles[name];st.font.name='Malgun Gothic';st.font.size=Pt(size)
        fonts=st.element.get_or_add_rPr().get_or_add_rFonts()
        for k in ['ascii','hAnsi','eastAsia']:fonts.set(qn('w:'+k),'Malgun Gothic')
        pf=st.paragraph_format;pf.line_spacing=Pt(14 if name=='Normal' else 13 if name=='Caption' else size*1.25);pf.space_after=Pt(1.5);pf.widow_control=True
        snap=OxmlElement('w:snapToGrid');snap.set(qn('w:val'),'0');st.element.get_or_add_pPr().append(snap)
        if name.startswith('Heading') or name=='Title':
            st.font.color.rgb=RGBColor.from_string('17365D');pf.keep_with_next=True;pf.space_before=Pt(5)
        if name=='Caption':st.font.color.rgb=RGBColor.from_string('006C70');pf.keep_together=True
    sec.header.paragraphs[0].add_run('벤조카인(Benzocaine) 합성 경로 예측 및 근거 기반 분석 보고서').font.size=Pt(9.5)
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
    doc.core_properties.title='벤조카인 합성 경로의 AI 예측과 근거 검토';doc.core_properties.author='Solar Pro 4'
    figures=[];tables=[];events=[]
    def inline(p,children):
        bold=italic=False;href=None
        for t in children or []:
            if t.type=='strong_open':bold=True
            elif t.type=='strong_close':bold=False
            elif t.type=='em_open':italic=True
            elif t.type=='em_close':italic=False
            elif t.type=='link_open':href=t.attrGet('href')
            elif t.type=='link_close':href=None
            elif t.type in ['text','code_inline']:
                if href:
                    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(href,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');v=OxmlElement('w:t');v.text=t.content;r.append(v);h.append(r);p._p.append(h)
                else:r=p.add_run(t.content);r.bold=bold;r.italic=italic
            elif t.type in ['softbreak','hardbreak']:p.add_run(' ' if t.type=='softbreak' else '\n')
            elif t.type=='html_inline' and t.content.lower().startswith('<br'):p.add_run('\n')
    def picture(token):
        name=Path(token.attrGet('src')).name;asset=assets[name];path=HERE/asset['path'];assert sha(path)==asset['sha256']
        with Image.open(path) as im:ratio=im.height/im.width
        width=asset['width_cm']
        if 'draft' not in name:width=min(width,17/ratio)
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True;p.paragraph_format.keep_together=True
        p.paragraph_format.line_spacing=1.0  # Inline images must use automatic line height; exact body leading clips them.
        p.add_run().add_picture(str(path),width=Cm(width));doc.add_paragraph(''.join(t.content for t in token.children or []),style='Caption')
        figures.append({'figure_id':asset['figure_id'],'width_cm':width,'caption_author':'Solar'})
    def paba_pair(first,second):
        table=doc.add_table(rows=1,cols=2);table.autofit=False
        for cell,token in zip(table.rows[0].cells,[first,second]):
            cell.width=Cm(8.5);name=Path(token.attrGet('src')).name;asset=assets[name];path=HERE/asset['path'];assert sha(path)==asset['sha256']
            pp=cell.paragraphs[0];pp.paragraph_format.keep_with_next=True;pp.paragraph_format.line_spacing=1.0;pp.add_run().add_picture(str(path),width=Cm(8.1))
            cap=cell.add_paragraph(''.join(t.content for t in token.children or []),style='Caption');cap.paragraph_format.keep_together=True
            figures.append({'figure_id':asset['figure_id'],'width_cm':8.1,'caption_author':'saved Solar caption','panel':'PABA same conformer, alternative view'})
        table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    tokens=MarkdownIt('commonmark').enable('table').parse(text);i=0;prefix='';stack=[];pending_step_figure=None;pending_paba=None
    while i<len(tokens):
        t=tokens[i]
        if t.type in ['ordered_list_open','bullet_list_open']:stack.append({'n':int(t.attrGet('start') or 1),'ordered':t.type=='ordered_list_open'})
        elif t.type in ['ordered_list_close','bullet_list_close']:stack.pop()
        elif t.type=='list_item_open':prefix=(str(stack[-1]['n'])+'. ') if stack[-1]['ordered'] else '• ';stack[-1]['n']+=1
        elif t.type in ['heading_open','paragraph_open']:
            c=tokens[i+1];images=[x for x in c.children or [] if x.type=='image'];events.append(c.content)
            if images:
                for image in images:
                    if Path(image.attrGet('src')).name=='19_paba_ball_and_stick.png':pending_paba=image
                    elif Path(image.attrGet('src')).name=='visualizer-route05-paba-edge.png' and pending_paba:
                        paba_pair(pending_paba,image);pending_paba=None
                    elif Path(image.attrGet('src')).name=='route-05-step-02-ko.png':pending_step_figure=image
                    else:picture(image)
            else:
                sty='Normal' if t.type=='paragraph_open' else ['Title','Heading 1','Heading 2','Heading 3'][min(int(t.tag[1:])-1,3)]
                p=doc.add_paragraph(style=sty)
                if prefix:p.add_run(prefix);prefix=''
                inline(p,c.children)
                if t.type=='heading_open' and c.content.startswith('3.3.2') and pending_step_figure:
                    picture(pending_step_figure);pending_step_figure=None
            i+=1
        elif t.type=='table_open':
            data=[];j=i+1
            while tokens[j].type!='table_close':
                x=tokens[j]
                if x.type=='tr_open':data.append([])
                elif x.type=='inline':data[-1].append(x)
                j+=1
            cols=len(data[0]);weights=[max(8,min(42,max(len(r[k].content) for r in data))) for k in range(cols)];widths=[17*w/sum(weights) for w in weights]
            header=' '.join(x.content for x in data[0])
            if cols==4 and '비교 항목' in header:widths=[2.2,4.7,4.5,5.6]
            if cols==5 and 'Parrot' in header and '순서 생성 점수' in header:widths=[2.8,1.15,2.0,6.45,4.6]
            if cols==7 and '허용 보고 수준' in header:widths=[1.65,2.5,1.65,2.8,3.05,3.05,2.3]
            table=doc.add_table(rows=0,cols=cols);table.style='Table Grid';table.autofit=False
            for col,w in zip(table.columns,widths):col.width=Cm(w)
            for ri,row in enumerate(data):
                cells=table.add_row().cells
                for ci,(cell,val,w) in enumerate(zip(cells,row,widths)):
                    cell.width=Cm(w);p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=Pt(13);p.paragraph_format.keep_with_next=ri==0
                    snap=OxmlElement('w:snapToGrid');snap.set(qn('w:val'),'0');p._p.get_or_add_pPr().append(snap)
                    numeric=re.fullmatch(r'[-+−]?[\d]+(?:\.\d+)?',val.content.strip())
                    if ri and numeric and ('score' in data[0][ci].content.lower() or '순서 생성 점수' in data[0][ci].content):p.add_run(f'{float(val.content.strip().replace("−","-")):.4f}')
                    else:inline(p,val.children)
                    if numeric:p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
                    for r in p.runs:r.font.size=Pt(10);r.bold=ri==0 or r.bold
                    if ri==0:
                        shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EEF2F4');cell._tc.get_or_add_tcPr().append(shade)
                pr=table.rows[-1]._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
                if ri==0:pr.append(OxmlElement('w:tblHeader'))
            tables.append({'rows':len(data),'columns':cols,'font_pt':10,'repeat_header':True});events.append([[x.content for x in r] for r in data]);i=j
        elif t.type in ['fence','code_block']:doc.add_paragraph(t.content.rstrip())
        i+=1
    assert pending_paba is None,'Unplaced PABA panel'
    assert pending_step_figure is None,'Unplaced step figure'
    a.output.parent.mkdir(parents=True,exist_ok=True);doc.save(a.output)
    record={'source_sha256':sha(src),'science_prose_modified':False,'provenance':provenance,'figures':figures,'tables':tables,'fonts_pt':sizes,'table_pt':10,'docx_sha256':sha(a.output),'DOCX_page_count':'pending actual Word repagination and PDF export','body_events':events}
    a.output.with_suffix('.docx.layout-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'docx':a.output.name,'figures':len(figures),'tables':len(tables),'science_prose_modified':False}))
if __name__=='__main__':main()
