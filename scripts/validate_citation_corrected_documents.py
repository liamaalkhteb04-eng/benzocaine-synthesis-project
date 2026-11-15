"""Inspect DOCX/PDF contents, pagination, references, figures, and clipping."""
import argparse
import json
import re
import zipfile
from pathlib import Path

import pymupdf
from docx import Document
from _runtime import digest, save
from validate_report_content import check_content


def compact(text):
    return re.sub(r"\s+", "", text)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report-dir", type=Path, required=True)
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--citation-validation", type=Path, required=True)
    a = p.parse_args()
    folder = a.report_dir
    md = folder / "report.md"
    docx_path = folder / "report.docx"
    pdf_path = folder / "report.pdf"
    report = md.read_text(encoding="utf-8")
    evidence = json.loads((a.run_dir / "report-evidence.json").read_text(encoding="utf-8"))
    citation_gate = json.loads(a.citation_validation.read_text(encoding="utf-8"))
    report_text = md.read_text(encoding="utf-8")
    content_check = check_content(report, evidence)
    doc = Document(docx_path)
    doc_text = "\n".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for row in t.rows for c in row.cells])
    with zipfile.ZipFile(docx_path) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        drawing_count = xml.count("<w:drawing>")
    pdf = pymupdf.open(pdf_path)
    page_text = [page.get_text() for page in pdf]
    all_text = "\n".join(page_text)
    normalized = compact(all_text)
    expected_figures = len(evidence["report_figure_assets"])
    image_instances, out_of_bounds_images, out_of_bounds_text = [], [], []
    links = set()
    preview = folder / "validation-previews"
    preview.mkdir(exist_ok=True)
    for i, page in enumerate(pdf, 1):
        for info in page.get_image_info():
            rect = pymupdf.Rect(info["bbox"])
            image_instances.append({"page": i, "bbox": list(info["bbox"])})
            if not page.rect.contains(rect):
                out_of_bounds_images.append(i)
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    box = pymupdf.Rect(span["bbox"])
                    if box.x0 < -1 or box.y0 < -1 or box.x1 > page.rect.width + 1 or box.y1 > page.rect.height + 1:
                        out_of_bounds_text.append(i)
        links.update(link.get("uri", "") for link in page.get_links() if link.get("uri", "").startswith("http"))
        page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4), alpha=False).save(preview / f"page-{i:02d}.png")

    expected_strings = [
        "CCOC(=O)c1ccc([N+](=O)[O-])cc1",
        "CCOC(=O)c1ccc(N)cc1",
        "82.95%", "91", "100%",
        "ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd",
        "9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563",
        "20261031-03", "20261031-04", "benzocaine-live-repro-20261105-01",
    ]
    missing_pdf_text = [value for value in expected_strings if compact(value) not in normalized]
    forbidden = ["<<<SECTION_", "TODO:", "[INSERT", "작성 지시문", "모든 출력 마커를", "초안을 생성해"]
    drafting_leaks = [value for value in forbidden if value.lower() in all_text.lower()]
    d10_line = next((line for line in report_text.splitlines() if line.startswith("- [D10]")), "")
    corrected_d10 = "evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-corrected.json"
    original_d10 = "evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-original-conflicting.json"
    table_font_sizes = [run.font.size.pt for table in doc.tables for row in table.rows for cell in row.cells
                        for paragraph in cell.paragraphs for run in paragraph.runs if run.font.size is not None]
    normalized_pages = [compact(text) for text in page_text]
    integrated_page = [page for page, normalized in zip(page_text, normalized_pages)
                       if "\uD1B5\uD569\uC870\uAC74\u00B7\uC218\uC728\uD45C" in compact(page)]
    integrated_table_same_page = (len(integrated_page) == 1
                                  and "route/step" in compact(integrated_page[0]).lower()
                                  and "step-01" in integrated_page[0])
    missing_urls = [ref["url"] for ref in evidence.get("required_references", []) if ref.get("url") not in links]
    checks = {
        "citation_release_validation_passed": citation_gate.get("status") == "passed",
        "report_content_check_passed": content_check.get("status") == "passed",
        "pdf_within_20_pages": 0 < len(pdf) <= 20,
        "docx_has_expected_embedded_figures": len(media) == expected_figures and drawing_count == expected_figures,
        "pdf_has_expected_figure_instances": len(image_instances) == expected_figures,
        "four_distinct_expected_tables": len(doc.tables) == 4 and content_check.get("table_count") == 4,
        "one_integrated_route_step_yield_table": content_check.get("yield_table_count") == 1,
        "no_pdf_image_or_text_outside_page": not out_of_bounds_images and not out_of_bounds_text,
        "critical_smiles_and_values_present_in_pdf": not missing_pdf_text,
        "all_reference_urls_linked": not missing_urls,
        "no_authoring_instruction_or_marker_leaks": not drafting_leaks,
        "citation_and_config_hash_claims_present_in_docx": all(s in compact(doc_text) for s in ["[D10]", "ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd", "9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563"]),
        "D10_corrected_and_original_records_distinguished": corrected_d10 in d10_line and original_d10 in d10_line and "7087c15ddeabf85006934214fb148f3b3a6bbc173b69502b011a9b3517cef287" in d10_line and "63ab33c238fda07120f87ff9e4024195b12bb68cc689565539f83112dd7db7a8" in d10_line and "reproduction-validation.json`" not in d10_line,
        "integrated_table_title_same_page_as_table": integrated_table_same_page,
        "tables_use_readable_9pt_text": bool(table_font_sizes) and min(table_font_sizes) >= 8.9,
        "specified_authoring_directives_removed": all(term not in report_text for term in ["\uBA3C\uC800 \uBA85\uC2DC\uD574\uC57C \uD55C\uB2E4", "README \uBC0F \uC99D\uAC70 \uBB38\uC11C\uC640 \uC77C\uCE58\uC2DC\uCF1C\uC57C \uD558\uBA70"]),
    }
    result = {
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "page_count": len(pdf),
        "docx_table_count": len(doc.tables),
        "embedded_docx_media_count": len(media),
        "docx_drawing_count": drawing_count,
        "pdf_image_instances": image_instances,
        "out_of_bounds_images": out_of_bounds_images,
        "out_of_bounds_text_pages": sorted(set(out_of_bounds_text)),
        "missing_pdf_text": missing_pdf_text,
        "missing_reference_urls": missing_urls,
        "drafting_instruction_leaks": drafting_leaks,
        "content_validation": content_check,
        "files": {name: digest(folder / name) for name in ("report.md", "report.docx", "report.pdf")},
    }
    save(folder / "document-validation.json", result)
    print(json.dumps({"status": result["status"], "page_count": len(pdf), "checks": checks, "output": str(folder / "document-validation.json")}, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "passed" else 2)


if __name__ == "__main__":
    main()
