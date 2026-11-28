"""Restore original PNG resolution after Word export; keep every text/page placement unchanged."""
from pathlib import Path
import json,re,hashlib,io,shutil,math,argparse
import pymupdf
from PIL import Image,ImageChops,ImageStat
P=Path(__file__).resolve().parents[1]/'report'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=json.loads((P/'figure-manifest.render.json').read_text(encoding='utf-8'));byname={Path(f['path']).name:f for f in manifest}
names=re.findall(r'!\[[^\n]+\]\(([^)]+)\)',(P/'report.md').read_text(encoding='utf-8'))
ordered=[byname[Path(n).name] for n in names];assert len(ordered)==13
ap=argparse.ArgumentParser();ap.add_argument('--pdf',type=Path,required=True);ap.add_argument('--raw',type=Path,required=True);ap.add_argument('--record',type=Path,required=True);args=ap.parse_args()
path=args.pdf.resolve();raw=args.raw.resolve();assert not raw.exists()
raw.parent.mkdir(exist_ok=True);shutil.move(str(path),str(raw))
pdf=pymupdf.open(raw);before_text=[page.get_text() for page in pdf];before_boxes=[];rows=[];index=0
def rgb(im):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);return bg.convert('RGB')
for page in pdf:
 for im in page.get_image_info(xrefs=True):
  figure=ordered[index];index+=1;src=P/figure['path'];assert sha(src)==figure['sha256']
  old=rgb(Image.open(io.BytesIO(pdf.extract_image(im['xref'])['image'])));source=rgb(Image.open(src))
  assert abs(source.width/source.height-old.width/old.height)<.01
  # Prevent any source/order mix-up, especially four equally sized route drawings.
  candidates=[]
  for f in manifest:
   with Image.open(P/f['path']) as test:
    if abs(test.width/test.height-old.width/old.height)>.01:continue
    scaled=rgb(test).resize(old.size,Image.Resampling.LANCZOS)
   rms=ImageStat.Stat(ImageChops.difference(scaled,old)).rms
   candidates.append((math.sqrt(sum(v*v for v in rms)/3),f['figure_id']))
  best=min(candidates);assert best[1]==figure['figure_id'] and best[0]<20,(figure['figure_id'],best)
  before_boxes.append({'page':page.number+1,'bbox':list(im['bbox']),'figure_id':figure['figure_id']})
  page.replace_image(im['xref'],filename=str(src))
  rows.append({'figure_id':figure['figure_id'],'page':page.number+1,'raw_Word_raster_pixels':list(old.size),'restored_source_pixels':list(source.size),'placement_bbox_unchanged':list(im['bbox']),'nearest_image_verification_RMSE':best[0],'source_sha256':figure['sha256']})
assert index==13
pdf.save(path,garbage=4,deflate=True)
pdf.close();final=pymupdf.open(path)
assert [page.get_text() for page in final]==before_text
after=[]
for page in final:
 for im in page.get_image_info():after.append({'page':page.number+1,'bbox':list(im['bbox'])})
assert len(after)==13
for a,b in zip(before_boxes,after):assert a['page']==b['page'] and max(abs(x-y) for x,y in zip(a['bbox'],b['bbox']))<.001
save(args.record,{'raw_Word_PDF':str(raw),'raw_Word_PDF_sha256':sha(raw),'final_PDF_sha256':sha(path),'actual_pages':len(final),'text_extraction_before_after_exactly_equal':True,'all13_image_page_bboxes_unchanged':True,'source_images_not_modified':True,'reason':'Word PDF exporter resamples/reencodes PNGs; restore the exact original13 PNGs at identical xrefs/placement without changing page instructions, captions, font or text. This is export fidelity, not new figure generation.','figures':rows})
print(json.dumps({'pages':len(final),'original_images_restored':13,'text_and_placement_unchanged':True}))
