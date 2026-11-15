"""Create labeled reaction figures from stored route SMILES and enlarged genuine GUI screenshot crops.

No chemistry calculation, reaction inference, or model call is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def font(size, bold=False):
    candidates=[Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
               Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")]
    for p in candidates:
        if p.is_file(): return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()


def atom_match(mol, smarts):
    from rdkit import Chem
    if not smarts: return []
    query=Chem.MolFromSmarts(smarts)
    return list(mol.GetSubstructMatch(query)) if query else []


def draw_route(evidence, route_id, step_id, output, overrides):
    from rdkit import Chem, rdBase
    from rdkit.Chem import Draw, rdMolDescriptors
    step=next(s for s in evidence["report_steps"] if s["route_id"]==route_id and s["step_id"]==step_id)
    precursors=step["precursor_smiles"]; product=step["product_smiles"]
    smi_list=precursors+[product]; mols=[Chem.MolFromSmiles(s) for s in smi_list]
    if any(m is None for m in mols): raise ValueError(f"Invalid source SMILES at {route_id}/{step_id}")
    setting=overrides.get("highlights",{}).get(f"{route_id}/{step_id}",{})
    precursor_patterns=setting.get("precursor_smarts",[]); product_pattern=setting.get("product_smarts","")
    highlights=[atom_match(m,precursor_patterns[i] if i<len(precursor_patterns) else "") for i,m in enumerate(mols[:-1])]
    highlights.append(atom_match(mols[-1],product_pattern))
    label_map=overrides.get("labels",{})
    labels=[]
    for i,smi in enumerate(smi_list):
        label=label_map.get(smi)
        if not label:
            formula=rdMolDescriptors.CalcMolFormula(mols[i])
            label=f"전구체 {i+1 if i<len(precursors) else ''}\n{formula}" if i<len(precursors) else f"생성물\n{formula}"
        labels.append(label)
    panel_w,panel_h,gap=510,420,100
    total_w=len(mols)*panel_w+(len(mols)-1)*gap; total_h=575
    canvas=Image.new("RGB",(total_w,total_h),"white"); painter=ImageDraw.Draw(canvas)
    painter.text((35,18),f"{route_id} · {step_id}",fill="#17365D",font=font(34,True))
    painter.text((35,67),"예측 경로의 구조 표현 · 강조 색은 반응식에서 달라지는 작용기",fill="#3B4856",font=font(20))
    for i,(mol,label,atom_ids) in enumerate(zip(mols,labels,highlights)):
        x=i*(panel_w+gap)
        image=Draw.MolToImage(mol,size=(panel_w,385),highlightAtoms=atom_ids,highlightColor=(1.0,.78,.25),kekulize=True)
        canvas.paste(image,(x,115))
        bbox=painter.multiline_textbbox((0,0),label,font=font(23,True),align="center",spacing=4)
        label_w=bbox[2]-bbox[0]
        painter.multiline_text((x+(panel_w-label_w)//2,498),label,fill="#17202A",font=font(23,True),align="center",spacing=4)
        if i:
            cx=x-gap//2; cy=300
            if i==len(mols)-1:
                painter.line((cx-28,cy,cx+25,cy),fill="#222",width=5)
                painter.polygon([(cx+34,cy),(cx+16,cy-12),(cx+16,cy+12)],fill="#222")
            else:
                painter.line((cx-4,cy-14,cx-4,cy+14),fill="#222",width=5)
                painter.line((cx-18,cy,cx+10,cy),fill="#222",width=5)
    note=overrides.get("notes",{}).get(f"{route_id}/{step_id}")
    if note: painter.text((35,total_h-34),note,fill="#8A3B12",font=font(18,True))
    canvas.save(output,format="PNG",optimize=True)
    return {"route_id":route_id,"step_id":step_id,"reaction_smiles":step["reaction_smiles"],
            "asset":str(output),"sha256":sha(output),"drawing_only_no_inference":True,"rdkit_version":rdBase.rdkitVersion}


def crop_visualizer(source,output,crop_box,table_box):
    original=Image.open(source).convert("RGB"); viewer=original.crop(crop_box); table=original.crop(table_box)
    viewer=viewer.resize((viewer.width*3,viewer.height*3),Image.Resampling.LANCZOS)
    table=table.resize((table.width*3,table.height*3),Image.Resampling.LANCZOS)
    width=max(viewer.width,table.width)+48
    canvas=Image.new("RGB",(width,viewer.height+table.height+72),"white")
    canvas.paste(viewer,((width-viewer.width)//2,12));canvas.paste(table,((width-table.width)//2,viewer.height+36))
    canvas.save(output,format="PNG",optimize=True)
    return {"source":str(source),"source_sha256":sha(source),"asset":str(output),"sha256":sha(output),
            "source_capture_preserved":True,"transformation":"tight crop of source GUI viewer and monitor row, enlarged 3x; no chemical labels or values added"}


def crop_visualizer_view(source, output, crop_box):
    original = Image.open(source).convert("RGB")
    viewer = original.crop(crop_box).resize(((crop_box[2]-crop_box[0])*3, (crop_box[3]-crop_box[1])*3), Image.Resampling.LANCZOS)
    viewer.save(output, format="PNG", optimize=True)
    return {"source":str(source),"source_sha256":sha(source),"asset":str(output),"sha256":sha(output),
            "source_capture_preserved":True,"transformation":"tight crop of the genuine Visualizer molecular viewport, enlarged 3x; no atom labels, measurements, or data added"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence",required=True,type=Path);p.add_argument("--output-dir",required=True,type=Path)
    p.add_argument("--visualizer-source-dir",type=Path);p.add_argument("--figure-overrides",type=Path)
    p.add_argument("--route-step",action="append",default=[],help="route-id/step-id; repeat to choose report figures; defaults to all selected steps")
    p.add_argument("--visualizer-crop",action="append",default=[],help="source.png|output.png; include actual monitor row")
    p.add_argument("--visualizer-view-crop",action="append",default=[],help="source.png|output.png; crop only the genuine molecular viewer area")
    a=p.parse_args()
    if a.output_dir.exists(): raise FileExistsError(a.output_dir)
    a.output_dir.mkdir(parents=True)
    evidence=json.loads(a.evidence.read_text(encoding="utf-8")); overrides=json.loads(a.figure_overrides.read_text(encoding="utf-8")) if a.figure_overrides else {}
    if a.route_step:
        chosen=[tuple(x.split("/",1)) for x in a.route_step]
    else:
        chosen=[(s["route_id"],s["step_id"]) for s in evidence.get("report_steps",[])]
    route_records=[draw_route(evidence,r,s,a.output_dir/f"{r}-{s}.png",overrides) for r,s in chosen]
    visualizer_records=[]
    if a.visualizer_crop and not a.visualizer_source_dir: p.error("--visualizer-source-dir is required with --visualizer-crop")
    if (a.visualizer_crop or a.visualizer_view_crop) and not a.visualizer_source_dir: p.error("--visualizer-source-dir is required with Visualizer crops")
    for spec in a.visualizer_crop:
        source_name,output_name=spec.split("|",1);source=a.visualizer_source_dir/source_name
        if not source.is_file(): raise FileNotFoundError(source)
        # The crop coordinates are proportional to the recorded 1366x768 Visualizer display.
        im=Image.open(source); sx=im.width/1366; sy=im.height/768
        def box(x0,y0,x1,y1): return (round(x0*sx),round(y0*sy),round(x1*sx),round(y1*sy))
        visualizer_records.append(crop_visualizer(source,a.output_dir/output_name,box(575,245,990,470),box(232,586,730,664)))
    for spec in a.visualizer_view_crop:
        source_name,output_name=spec.split("|",1);source=a.visualizer_source_dir/source_name
        if not source.is_file(): raise FileNotFoundError(source)
        im=Image.open(source); sx=im.width/1366; sy=im.height/768
        box=(round(600*sx),round(245*sy),round(1005*sx),round(475*sy))
        visualizer_records.append(crop_visualizer_view(source,a.output_dir/output_name,box))
    manifest={"status":"report_asset_preparation_only_no_inference_or_scientific_calculation","routes":route_records,"visualizer_crops":visualizer_records}
    (a.output_dir/"asset-preparation-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":manifest["status"],"route_figures":len(route_records),"visualizer_crops":len(visualizer_records)},ensure_ascii=False))

if __name__=="__main__": main()