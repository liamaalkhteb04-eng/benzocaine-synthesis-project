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
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--run-dir",type=Path,required=True); ap.add_argument("--attempt-dir",type=Path,required=True); ap.add_argument("--report-dir",type=Path,required=True); ap.add_argument("--matrix-audit",type=Path); ap.add_argument("--citation-audit",type=Path); ap.add_argument("--composition-validation",type=Path); a=ap.parse_args()
    run=a.run_dir.resolve(); attempt=a.attempt_dir.resolve(); folder=a.report_dir.resolve(); errors=[]; md=folder/"report.md"; layout=load(folder/"layout-validation.json"); evidence=load(run/"report-evidence.json"); raw=load(attempt/"solar-response.raw.json"); status=load(attempt/"solar-status.json"); text=md.read_text(encoding="utf-8")
    if layout.get("status")!="passed" or layout.get("rendered_markdown_sha256")!=sha(md): errors.append("layout validation hash/status mismatch")
    if layout.get("solar_raw_response_sha256")!=sha(attempt/"solar-response.raw.json"): errors.append("Solar raw response provenance mismatch")
    if status.get("status")!="success" or not str(raw.get("model","")).startswith("solar-pro4"): errors.append("saved Solar report source is not successful Solar Pro 4")
    verification_path=run/"verification.json"
    if not verification_path.is_file(): verification_path=run/"latest-route-reproduction"/"verification.json"
    if not verification_path.is_file() or load(verification_path).get("status")!="passed": errors.append("run verification missing/failed")
    redaction_path=run/"latest-route-reproduction"/"public-redaction-validation.json"
    redaction=load(redaction_path) if redaction_path.is_file() else {}
    if redaction and redaction.get("status")!="passed": errors.append("public run data redaction validation failed")
    redacted={x["file"]:x["public_sha256"] for x in redaction.get("checks",[])}
    fig_redaction=load(run/"figures"/"manifest-redaction-validation.json") if (run/"figures"/"manifest-redaction-validation.json").is_file() else {}
    for rel,expected in evidence.get("source_hashes",{}).items():
        artifact=run/rel
        if not artifact.is_file() and (run/"latest-route-reproduction"/rel).is_file(): artifact=run/"latest-route-reproduction"/rel
        if not artifact.is_file(): errors.append(f"normalized source missing: {rel}"); continue
        if artifact.parent.name=="latest-route-reproduction" and artifact.name in redacted:
            if sha(artifact)!=redacted[artifact.name]: errors.append(f"public run data hash mismatch: {rel}")
        elif rel=="figures/manifest.json" and fig_redaction:
            if sha(artifact)!=fig_redaction.get("public_sha256") or fig_redaction.get("source_sha256")!=expected: errors.append(f"figure manifest redaction mismatch: {rel}")
        elif sha(artifact)!=expected: errors.append(f"normalized source hash mismatch: {rel}")
    if FIGURE_MARKER.search(text): errors.append("unresolved [figure: ...] marker")
    tokens=MarkdownIt("commonmark").enable("table").parse(text); images=[]; tables=[]
    for token in tokens:
        if token.type=="inline": images.extend(x.attrGet("src") for x in token.children or [] if x.type=="image")
    from render_report_evidence import markdown_tables, build_table
    tables=markdown_tables(text); asset_names={Path(x["path"]).name for x in evidence.get("report_figure_assets",[])}
    linked={Path(str(x).replace("\\","/")).name for x in images}
    if linked!=asset_names or len(images)!=len(asset_names): errors.append("Markdown figure list does not exactly cover report_figure_assets")
    integrated=[(start,end,rows) for start,end,rows in tables if rows and any("route_id / step_id"==c.lower() for c in rows[0]) and any("yield" in c.lower() for c in rows[0])]
    candidate_tables=[(start,end,rows) for start,end,rows in tables if rows and any("parrot rank"==c.lower() for c in rows[0]) and any("parrot 원래 슬롯" in c.lower() for c in rows[0]) and any("sequence_score" in c.lower() for c in rows[0])]
    matrix_audit=load(a.matrix_audit) if a.matrix_audit else None
    if len(integrated)!=1: errors.append("expected one concise route/step rank-1 conditions/yield summary table")
    elif matrix_audit:
        summary_rows=integrated[0][2]
        if len(summary_rows)!=5: errors.append("rank-1 conditions/yield summary must contain four route/step rows")
        if len(candidate_tables)!=1: errors.append("expected one candidate-level Parrot matrix")
        detail_rows=candidate_tables[0][2] if candidate_tables else []
        if matrix_audit.get("status")!="passed" or matrix_audit.get("row_count")!=13 or len(detail_rows)!=14:
            errors.append("route comparison matrix row count/audit mismatch")
        summary=[rows for _,_,rows in tables if rows and rows[0] and "경로·단계" in rows[0][0]]
        if len(summary)!=1 or len(summary[0])!=5: errors.append("expected one 4-step route summary table")
        data={}
        for row in detail_rows[1:]:
            if len(row)>=5:
                key=(row[0].split("(",1)[0].strip().replace(" [D1]", ""), row[1].strip())
                data[key]=row
        for expected in matrix_audit.get("rows",[]):
            key=(f"{expected['route_id']} / {expected['step_id']}",str(expected["parrot_rank"]))
            row=next((x for (k,r),x in data.items() if k.startswith(key[0]) and r==key[1]),None)
            if row is None: errors.append(f"missing matrix candidate row {key}"); continue
            if compact(expected["reaction_smiles"]) not in compact(text.replace("`", "")):
                errors.append(f"route/step reaction SMILES is absent from the report body for {key}")
            if str(expected["parrot_sequence_score"]) not in row[2]: errors.append(f"matrix sequence score mismatch {key}")
            slots=row[3].replace("`", "")
            for field,value in expected["parrot_original_slots"].items():
                if f"{field}={value}" not in slots: errors.append(f"matrix Parrot slot mismatch {key}: {field}")
            yield_value=f"{expected['yield_percent']:.2f}%"
            if yield_value not in row[4] or expected["yield_status"] not in row[4]: errors.append(f"matrix yield/status mismatch {key}")
        # The step summary intentionally contains only the highest-ranked Parrot
        # row; the 13-row matrix retains all candidates and ranks separately.
        for route_step in sorted({(x["route_id"],x["step_id"]) for x in matrix_audit.get("rows",[])}):
            route,sid=route_step
            expected=next((x for x in matrix_audit["rows"] if x["route_id"]==route and x["step_id"]==sid and x["parrot_rank"]==1),None)
            row=next((r for r in summary_rows[1:] if r and r[0].strip().replace(" [D1]","")==f"{route} / {sid}"),None)
            if expected is None or row is None:
                errors.append(f"missing rank-1 summary row {route}/{sid}"); continue
            for field,value in expected["parrot_original_slots"].items():
                if f"{field}={value}" not in row[2].replace("`", ""):
                    errors.append(f"rank-1 summary slot mismatch {route}/{sid}: {field}")
            expected_yield=f"{expected['yield_percent']:.2f}%"
            if expected_yield not in row[4] or expected["yield_status"] not in row[4]:
                errors.append(f"rank-1 summary yield/status mismatch {route}/{sid}")
        if a.citation_audit and load(a.citation_audit).get("status")!="passed": errors.append("claim-to-source citation audit failed")
        if a.composition_validation and load(a.composition_validation).get("status")!="passed_composed_reproduction_source": errors.append("composition provenance did not pass")
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
    result={"status":"passed" if not errors else "failed","errors":errors,"run_id":status.get("run_id"),"solar_raw_response_sha256":sha(attempt/"solar-response.raw.json"),"source_report_markdown_sha256":layout.get("source_markdown_sha256"),"rendered_markdown_sha256":sha(md),"normalized_step_count":len(evidence.get("report_steps",[])),"candidate_matrix_rows":None if matrix_audit is None else matrix_audit.get("row_count"),"figure_count":len(asset_names),"docx_table_count":len(Document(docx).tables) if docx.is_file() else None,"pdf_pages":len(pdf) if docx.is_file() and pdfpath.is_file() else None,"pdf_images":image_count if docx.is_file() and pdfpath.is_file() else None,"clipped_items":clipped if docx.is_file() and pdfpath.is_file() else [],"full_page_previews":str(preview) if docx.is_file() and pdfpath.is_file() else None,"scientific_prose_reauthored":False,"solar_recall":False}
    save(folder/"document-validation.json",result); print(json.dumps(result,ensure_ascii=True,indent=2)); return 0 if result["status"]=="passed" else 2
if __name__=="__main__": raise SystemExit(main())
