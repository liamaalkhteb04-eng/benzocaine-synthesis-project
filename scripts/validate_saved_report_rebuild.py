"""Check a saved-response DOCX/Edge-PDF rebuild without making model calls."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

import pymupdf
from docx import Document


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pdf(path, phrases, figure_count):
    document = pymupdf.open(path)
    text = "\n".join(page.get_text() for page in document)
    images = []
    out_of_bounds = []
    blank_pages = []
    for number, page in enumerate(document, 1):
        if not page.get_text().strip():
            blank_pages.append(number)
        for image in page.get_image_info():
            images.append(image)
            if image["width"] < 100 or image["height"] < 100 or not page.rect.contains(pymupdf.Rect(image["bbox"])):
                out_of_bounds.append({"page": number, "kind": "image"})
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    box = pymupdf.Rect(span["bbox"])
                    if box.x0 < -1 or box.y0 < -1 or box.x1 > page.rect.width + 1 or box.y1 > page.rect.height + 1:
                        out_of_bounds.append({"page": number, "kind": "text", "sample": span["text"][:30]})
    urls = {link.get("uri") for page in document for link in page.get_links()
            if link.get("uri", "").startswith("http")}
    normalized = re.sub(r"\s+", " ", text)
    return {
        "pages": len(document), "under_20_pages": len(document) <= 20,
        "figure_count": len(images), "all_figures_are_real": len(images) == figure_count
            and all(i["width"] >= 100 and i["height"] >= 100 for i in images),
        "out_of_bounds": out_of_bounds, "blank_pages": blank_pages,
        "unique_external_links": len(urls),
        "four_electron_flow_sections": text.count(phrases["electron"]) == 4,
        "lecture_comparison_and_yield": phrases["lecture"] in normalized and "79.80%" in normalized,
        "lecture_page_range": phrases["page_range"] in text,
        "bibliography_1_to_17": bool(re.search(r"(?m)^\s*1\.", text))
            and bool(re.search(r"(?m)^\s*17\.", text)),
        "evidence_refs_D1_D8": "[D1]" in text and "[D8]" in text,
        "nitro_charge_smiles": "[N+]" in text and "[O-]" in text,
        "analysis_sections_present": all(x in text for x in ["MOPAC", "EPI Suite", "Visualizer", "OpenCode"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    folder = args.work_dir.resolve()
    source = folder.parent / "benzocaine-citation-corrected-20261105" / "report.md"
    source_text = source.read_text(encoding="utf-8")
    copied_text = (folder / "report.md").read_text(encoding="utf-8")
    old = "PDF pp. 90?95"
    new = "PDF pp. 90\u201395"
    provenance = json.loads((folder / "text-normalization.json").read_text(encoding="utf-8"))
    expected_copy = source_text.replace(old, new)
    document = Document(folder / "report.docx")
    docx_text = "\n".join(p.text for p in document.paragraphs) + "\n" + "\n".join(
        cell.text for table in document.tables for row in table.rows for cell in row.cells)
    phrase = "\uC791\uC6A9\uAE30\uC640 \uC804\uC790 \uC774\uB3D9"
    lecture = "\uAC15\uC758 \uC608\uC2DC\uC640 AI \uC608\uCE21 \uBE44\uAD50"
    page_range = "90\u201395"
    checks = {
        "markdown_diff_only_known_page_range_glyph": copied_text == expected_copy,
        "normalization_manifest_hashes_match": provenance["source_sha256"] == sha256(source)
            and provenance["output_sha256"] == sha256(folder / "report.md"),
        "normalization_records_one_repair": provenance["typographic_repairs"][0]["count"] == 1,
        "saved_solar_response_hash_matches": json.loads((folder / "source-solar-call-record/status.json").read_text(encoding="utf-8"))["response_sha256"]
            == sha256(folder / "source-solar-call-record/response.raw.json"),
        "docx_figures": len(document.inline_shapes) == 10,
        "docx_tables": len(document.tables) == 2,
        "docx_four_electron_flow_sections": docx_text.count(phrase) == 4,
        "docx_lecture_comparison_and_yield": lecture in docx_text and "79.80%" in docx_text,
        "docx_lecture_page_range": page_range in docx_text,
        "docx_nitro_charge_smiles": "[N+]" in docx_text and "[O-]" in docx_text,
        "citation_audit_passed": json.loads((folder / "citation-audit.json").read_text(encoding="utf-8"))["status"] == "passed",
    }
    checks["edge_pdf"] = check_pdf(folder / "report.pdf", {"electron": phrase, "lecture": lecture,
        "page_range": page_range}, 10)
    checks["word_pagination"] = json.loads((folder / "validation/word-export-check.json").read_text(encoding="utf-8-sig"))
    checks["word_pdf"] = check_pdf(folder / "validation/report-word-check.pdf", {"electron": phrase,
        "lecture": lecture, "page_range": page_range}, 10)
    result = {"status": "passed", "checks": checks}
    if not all(v is True for k, v in checks.items() if isinstance(v, bool)):
        result["status"] = "failed"
    for key in ("edge_pdf", "word_pdf"):
        part = checks[key]
        if not part["under_20_pages"] or not part["all_figures_are_real"] or part["out_of_bounds"] or part["blank_pages"]:
            result["status"] = "failed"
        if not all(part[k] for k in ["four_electron_flow_sections", "lecture_comparison_and_yield",
                                     "lecture_page_range", "bibliography_1_to_17", "evidence_refs_D1_D8",
                                     "nitro_charge_smiles", "analysis_sections_present"]):
            result["status"] = "failed"
    output = folder / "rebuild-validation.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "edge_pages": checks["edge_pdf"]["pages"],
        "word_pages": checks["word_pagination"].get("pages"), "docx_figures": len(document.inline_shapes),
        "docx_tables": len(document.tables)}))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
