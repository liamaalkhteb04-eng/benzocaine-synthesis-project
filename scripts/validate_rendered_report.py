"""Validate one code-rendered report against run evidence and its saved Solar source."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path
from markdown_it import MarkdownIt
import pymupdf
from docx import Document
from _runtime import save
from render_report_evidence import FIGURE_MARKER, figure_marker_id

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def compact(s): return re.sub(r"\s+", "", s)
def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--run-dir",type=Path,required=True); ap.add_argument("--attempt-dir",type=Path,required=True); ap.add_argument("--report-dir",type=Path,required=True); a=ap.parse_args()
    run=a.run_dir.resolve(); attempt=a.attempt_dir.resolve(); folder=a.report_dir.resolve(); errors=[]; md=folder/"report.md"; layout=load(folder/"layout-validation.json"); evidence=load(run/"report-evidence.json"); raw=load(attempt/"solar-response.raw.json"); status=load(attempt/"solar-status.json"); text=md.read_text(encoding="utf-8")
    if layout.get("status")!="passed" or layout.get("rendered_markdown_sha256")!=sha(md): errors.append("layout validation hash/status mismatch")
    if layout.get("solar_raw_response_sha256")!=sha(attempt/"solar-response.raw.json"): errors.append("Solar raw response provenance mismatch")
    if status.get("status")!="success" or not str(raw.get("model","")).startswith("solar-pro4"): errors.append("saved Solar report source is not successful Solar Pro 4")
    if not (run/"verification.json").is_file() or load(run/"verification.json").get("status")!="passed": errors.append("run verification missing/failed")
    for rel,expected in evidence.get("source_hashes",{}).items():
        if not (run/rel).is_file() or sha(run/rel)!=expected: errors.append(f"normalized source hash mismatch: {rel}")
    if FIGURE_MARKER.search(text): errors.append("unresolved [figure: ...] marker")
    tokens=MarkdownIt("commonmark").enable("table").parse(text); images=[]; tables=[]
    for token in tokens:
        if token.type=="inline": images.extend(x.attrGet("src") for x in token.children or [] if x.type=="image")
    from render_report_evidence import markdown_tables, build_table
    tables=markdown_tables(text); asset_names={Path(x["path"]).name for x in evidence.get("report_figure_assets",[])}
    linked={Path(str(x).replace("\\","/")).name for x in images}
    if linked!=asset_names or len(images)!=len(asset_names): errors.append("Markdown figure list does not exactly cover report_figure_assets")
    integrated=[(start,end,rows) for start,end,rows in tables if rows and any("route_id / step_id"==c.lower() for c in rows[0]) and any("yield" in c.lower() for c in rows[0])]
    if len(integrated)!=1: errors.append("expected one normalized route/step conditions/yield table")
    else:
        rows={row[0].replace("`","").strip():row for row in integrated[0][2][1:] if row}
        headers,expected_rows=build_table(evidence)
        if len(rows)!=len(expected_rows): errors.append("integrated table row count differs from selected evidence steps")
        for exp in expected_rows:
            key=exp[0]; row=rows.get(key)
            if row is None: errors.append(f"missing table route/step {key}"); continue
            if len(row)!=len(headers): errors.append(f"wrong column count at {key}"); continue
            for idx in range(1,len(headers)):
                plain=lambda s:re.sub(r"[*`]", "", str(s)).replace("<br>"," ")
                if compact(plain(exp[idx])) not in compact(plain(row[idx])): errors.append(f"normalized table value mismatch: {key}, column {headers[idx]}")
    if FIGURE_MARKER.search(text) or any(x.lower() in text.lower() for x in ("[insert ","todo:","write the complete final project report")): errors.append("draft marker/instruction remains")
    docx=folder/"report.docx"; pdfpath=folder/"report.pdf"
    if not docx.is_file() or not pdfpath.is_file(): errors.append("DOCX/PDF missing")
    else:
        document=Document(docx)
        with zipfile.ZipFile(docx) as z: media=len([x for x in z.namelist() if x.startswith("word/media/")])
        if media!=len(asset_names): errors.append("DOCX figure count mismatch")
        if len(document.tables)!=len(tables): errors.append("DOCX table count differs from Markdown")
        doc_text="\n".join(x.text for x in document.paragraphs)+"\n"+"\n".join(c.text for t in document.tables for row in t.rows for c in row.cells)
        if not any(n and n in doc_text for n in (evidence.get("target",{}).get("name"),evidence.get("target",{}).get("name_ko"))): errors.append("DOCX target identity missing")
        pdf=pymupdf.open(pdfpath); full="\n".join(p.get_text() for p in pdf); normalized=compact(full); expected_figures=len(asset_names); image_count=0; clipped=[]; links=set(); preview=folder/"validation-previews"; preview.mkdir(exist_ok=True)
        if len(pdf)==0 or len(pdf)>20: errors.append(f"PDF page count invalid: {len(pdf)}")
        if not any(n and n in full for n in (evidence.get("target",{}).get("name"),evidence.get("target",{}).get("name_ko"))): errors.append("PDF target identity missing")
        for ref in evidence.get("required_references",[]):
            if compact(ref["url"]) not in normalized: errors.append(f"PDF reference text missing: {ref.get('id')}")
        for step in evidence.get("report_steps",[]):
            yield_value=step.get("yield_prediction",{}).get("yield_percent")
            if step["route_id"] not in full or step["step_id"] not in full: errors.append(f"PDF route/step missing: {step['route_id']}/{step['step_id']}")
            if yield_value is not None and compact(f"{float(yield_value):.2f}%") not in normalized: errors.append(f"PDF yield missing: {step['route_id']}/{step['step_id']}")
        for i,page in enumerate(pdf,1):
            for info in page.get_image_info():
                image_count+=1
                if not page.rect.contains(pymupdf.Rect(info["bbox"])): clipped.append({"page":i,"type":"image"})
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines",[]):
                    for span in line["spans"]:
                        b=pymupdf.Rect(span["bbox"])
                        if b.x0 < -1 or b.y0 < -1 or b.x1>page.rect.width+1 or b.y1>page.rect.height+1: clipped.append({"page":i,"type":"text"})
            links.update(link.get("uri","") for link in page.get_links())
            page.get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False).save(preview/f"page-{i:02d}.png")
        if image_count!=expected_figures: errors.append("PDF figure count mismatch")
        if clipped: errors.append("PDF text/image extends outside page")
        for ref in evidence.get("required_references",[]):
            if ref["url"] not in links: errors.append(f"PDF hyperlink missing: {ref.get('id')}")
    result={"status":"passed" if not errors else "failed","errors":errors,"run_id":status.get("run_id"),"solar_raw_response_sha256":sha(attempt/"solar-response.raw.json"),"source_report_markdown_sha256":layout.get("source_markdown_sha256"),"rendered_markdown_sha256":sha(md),"normalized_step_count":len(evidence.get("report_steps",[])),"figure_count":len(asset_names),"pdf_pages":len(pdf) if docx.is_file() and pdfpath.is_file() else None,"pdf_images":image_count if docx.is_file() and pdfpath.is_file() else None,"clipped_items":clipped if docx.is_file() and pdfpath.is_file() else [],"full_page_previews":str(preview) if docx.is_file() and pdfpath.is_file() else None,"scientific_prose_reauthored":False,"solar_recall":False}
    save(folder/"document-validation.json",result); print(json.dumps(result,ensure_ascii=True,indent=2)); return 0 if result["status"]=="passed" else 2
if __name__=="__main__": raise SystemExit(main())
