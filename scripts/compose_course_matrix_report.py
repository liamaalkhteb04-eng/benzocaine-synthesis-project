#!/usr/bin/env python3
"""Compose verified Solar course prose and a code-built comparison matrix into a report draft."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

BLOCK_START="<!-- BEGIN SOLAR INSERT: COURSE-COMPARISON-ROUTE05-STEP02 -->"
BLOCK_END="<!-- END SOLAR INSERT: COURSE-COMPARISON-ROUTE05-STEP02 -->"
MATRIX_MARKER="<!-- VERIFIED_ROUTE_COMPARISON_MATRIX -->"
def digest(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def read_json(path:Path): return json.loads(path.read_text(encoding="utf-8-sig"))

def matrix_fragment(path:Path)->str:
    source=path.read_text(encoding="utf-8-sig")
    lines=source.splitlines()
    # Keep the generated intro and the two tables; audit/evidence inventory remains in the standalone artifact.
    start=next((i for i,x in enumerate(lines) if x.startswith("## 경로 요약")),None)
    end=next((i for i,x in enumerate(lines) if x.startswith("## 입력·검증 자료")),len(lines))
    if start is None: raise ValueError("Comparison matrix has no path summary")
    intro=lines[2:3]
    body=lines[start:end]
    body=[x.replace("## 경로 요약","#### 경로 요약").replace("## Parrot 후보·단계별 예측 수율","#### Parrot 후보·단계별 예측 수율") for x in body]
    return "\n".join(["### 2.4 대표 경로 비교", "", *intro, "", *body]).strip()+"\n"

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-report",type=Path,required=True)
    p.add_argument("--base-report-sha256",required=True)
    p.add_argument("--solar-block",type=Path,required=True)
    p.add_argument("--solar-raw-json",type=Path,required=True)
    p.add_argument("--semantic-reassessment",type=Path,required=True)
    p.add_argument("--citation-correction",type=Path,required=True)
    p.add_argument("--matrix",type=Path,required=True)
    p.add_argument("--matrix-audit",type=Path,required=True)
    p.add_argument("--report-evidence",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args()
    if a.output_dir.exists(): raise SystemExit("Output folder exists; preserving prior run")
    base=a.base_report.read_text(encoding="utf-8-sig")
    if digest(a.base_report)!=a.base_report_sha256: raise SystemExit("Base report SHA-256 mismatch")
    block_source=a.solar_block.read_text(encoding="utf-8-sig")
    if block_source.count(BLOCK_START)!=1 or block_source.count(BLOCK_END)!=1: raise SystemExit("Citation-corrected Solar block markers are invalid")
    block=block_source[block_source.index(BLOCK_START):block_source.index(BLOCK_END)+len(BLOCK_END)]
    block_text=block.replace(BLOCK_START,"",1).replace(BLOCK_END,"",1).strip()
    solar_raw=read_json(a.solar_raw_json)["choices"][0]["message"]["content"]
    if block_text not in solar_raw:
        # Citation-only edits are verified separately; compare after removal of explicit citation tokens.
        import re
        def strip_citations(s):
            s=s.replace("[17이 아니라 D1]", "")
            return re.sub(r"\[(?:D\d+|\d+)(?:,\s*PDF\s+pp\.[^\]]+)?\]", "", s)
        rawblock=next(x for x in solar_raw.split(BLOCK_START,1)[1].split(BLOCK_END,1)[0].splitlines() if x.startswith("### "))
        if strip_citations(block_text)!=strip_citations(solar_raw.split(BLOCK_START,1)[1].split(BLOCK_END,1)[0].strip()):
            raise SystemExit("Citation derivative changed Solar-authored noncitation text")
    semantic=read_json(a.semantic_reassessment)
    if semantic.get("status")!="passed_semantic_review_no_substantive_omission": raise SystemExit("Semantic content reassessment did not pass")
    citation=read_json(a.citation_correction)
    if citation.get("status")!="passed_citation_only_derivative" or citation.get("noncitation_content_unchanged") is not True: raise SystemExit("Citation-only derivative is not validated")
    matrix_audit=read_json(a.matrix_audit)
    if matrix_audit.get("status")!="passed" or matrix_audit.get("row_count")!=13 or matrix_audit.get("unique_route_step_count")!=4: raise SystemExit("Route matrix audit failed or unexpected dimensions")
    if matrix_audit.get("outputs",{}).get("markdown_sha256")!=digest(a.matrix): raise SystemExit("Matrix markdown hash differs from audit")
    evidence=read_json(a.report_evidence)
    if not all(evidence.get("model_status",{}).get(x)=="success" for x in ("routes","conditions","yields")): raise SystemExit("Required route/condition/yield evidence is not successful")
    if base.count("### 3.3.2 route-05/step-02")!=1 or base.count("### 3.4 ")!=1: raise SystemExit("Expected Solar insertion point is missing or ambiguous")
    if MATRIX_MARKER in base: raise SystemExit("Unexpected pre-existing matrix marker")
    report3=base.index("## 3. 구조 변화와 단계별 조건·수율 예측")
    if "## 2. 탐색 범위와 경로 선정" not in base or "### 2.3 대표 경로의 기본 구성" not in base: raise SystemExit("Expected section 2 structure missing")
    matrix=matrix_fragment(a.matrix)
    source=base.replace("## 3. 구조 변화와 단계별 조건·수율 예측", MATRIX_MARKER+"\n\n## 3. 구조 변화와 단계별 조건·수율 예측",1)
    insertion=source.index("### 3.4 단계별 조건·수율 값의 표기 원칙")
    source=source[:insertion]+block_text+"\n\n"+source[insertion:]
    # Add matrix beneath section 2.3, after its route list and explanatory paragraph.
    section3=source.index("## 3. 구조 변화와 단계별 조건·수율 예측")
    placeholder=source.index(MATRIX_MARKER)
    if not placeholder < section3: raise SystemExit("Matrix marker is not in section 2")
    if source.count(block_text)!=1: raise SystemExit("Solar block did not occur exactly once in composed source")
    restored=source.replace(block_text+"\n\n", "", 1)
    restored=restored.replace(MATRIX_MARKER+"\n\n", "", 1)
    if restored!=base: raise SystemExit("Base report was changed outside the approved Solar block and matrix marker")
    # Save the composite source with one marker; renderer will materialize the matrix and exact manifest figures.
    a.output_dir.mkdir(parents=True,exist_ok=False)
    draft=a.output_dir/"report-composed-source.md"; draft.write_text(source,encoding="utf-8",newline="\n")
    comp={
      "status":"passed_composed_reproduction_source","base_report_path":str(a.base_report.resolve()),"base_report_sha256":digest(a.base_report),
      "composed_source_path":str(draft.resolve()),"composed_source_sha256":digest(draft),
      "solar_block_path":str(a.solar_block.resolve()),"solar_raw_json_path":str(a.solar_raw_json.resolve()),"solar_raw_json_sha256":digest(a.solar_raw_json),
      "semantic_reassessment_path":str(a.semantic_reassessment.resolve()),"semantic_reassessment_sha256":digest(a.semantic_reassessment),
      "citation_correction_path":str(a.citation_correction.resolve()),"citation_correction_sha256":digest(a.citation_correction),
      "matrix_path":str(a.matrix.resolve()),"matrix_sha256":digest(a.matrix),"matrix_audit_path":str(a.matrix_audit.resolve()),"matrix_audit_sha256":digest(a.matrix_audit),
      "solar_content_inserted_at":"after 3.3.2, before 3.4","matrix_marker_at":"section 2.4, before section 3",
      "all_base_report_text_preserved_outside_insertions":True,"solar_raw_response_unchanged":True,"scientific_prose_locally_edited":False,
      "normalization_table_policy":"the 13-row comparison matrix replaces a second duplicate conditions/yield table; the separate 4-step summary distinguishes route evidence from candidate-level slots and yields",
      "required_steps":4,"candidate_rows":13,"figures_pending_exact_manifest_renderer":10,
      "solar_call_count":0,"chemistry_inference":False
    }
    (a.output_dir/"composition-validation.json").write_text(json.dumps(comp,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":"passed","draft":str(draft),"candidate_rows":13},ensure_ascii=False))
    return 0
if __name__=="__main__":raise SystemExit(main())
