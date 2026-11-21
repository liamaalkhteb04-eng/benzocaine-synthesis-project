"""Audit citation-number existence and claim-to-source scope for synthesis reports."""
import argparse
import json
import re
from pathlib import Path

CITATION = re.compile(r"\[(D\d+|\d+)(?:,\s*PDF\s+pp\.[^\]]+)?\]")
BIBLIOGRAPHY = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.M)
EVIDENCE_LIST = re.compile(r"^\s*-\s+(?:\[(D\d+)\]|(D\d+):)\s*(.+)$", re.M)


def source_requirements(paragraph):
    lower = paragraph.lower()
    req_ext, req_evidence = set(), set()
    # A model name alone is not a methodology claim. Require its repository
    # citation when this sentence actually describes method, inputs, outputs,
    # prediction behavior, or a defined model score.
    if "aizynthfinder" in lower and re.search(
        r"(search algorithm|policy network|template-based retrosynthesis|route-planning method|\uACBD\uB85C \uD0D0\uC0C9 \uBC29\uBC95|\uC815\uCC45 \uB124\uD2B8\uC6CC\uD06C|\uD15C\uD50C\uB9BF \uAE30\uBC18 \uC5ED\uD569\uC131)", lower
    ):
        req_ext.add("2")
    if "parrot" in lower and re.search(
        r"(condition[- ]prediction method|parrot predicts reaction conditions|sequence.score definition|\uC870\uAC74 \uC608\uCE21 \uBC29\uBC95|parrot\uC740 \uBC18\uC751 \uC870\uAC74\uC744 \uC608\uCE21|\uC11C\uC5F4 \uC810\uC218 \uC815\uC758|\uCD9C\uB825 \uD544\uB4DC \uC815\uC758)", lower
    ):
        req_ext.add("5")
    if "rxn_yields" in lower and re.search(
        r"(yield prediction method|rxn_yields predicts? (?:reaction )?yield|\uC218\uC728 \uBAA8\uB378\uC758 \uBC29\uBC95|\uC218\uC728 \uBAA8\uB378\uC774 \uC5B4\uB5BB\uAC8C \uC608\uCE21)", lower
    ):
        req_ext.add("6")
    if "drfp" in lower and re.search(r"(fingerprint|method|algorithm|descriptor|\uC9C0\uBB38|\uBC29\uBC95\uB860)", lower): req_ext.add("7")
    if "askcos" in lower and re.search(r"(method|model|algorithm|\uBC29\uBC95|\uBAA8\uB378)", lower): req_ext.add("4")
    if "synthex" in lower and re.search(r"(method|model|algorithm|\uBC29\uBC95|\uBAA8\uB378)", lower): req_ext.add("3")
    if re.search(r"\bmopac\b|\bpm7\b|\bgnorm\b", lower):
        req_evidence.add("D5")
        if re.search(r"\bpm7\b", lower): req_ext.add("10")
        if "gnorm" in lower: req_ext.add("11")
    if re.search(r"epi suite|mpbpwin|epiunified", lower):
        req_evidence.add("D6")
        if "mpbpwin" in lower or "epa" in lower: req_ext.add("12")
        if "web" in lower or "api" in lower: req_ext.add("13")
    if "visualizer" in lower: req_evidence.add("D7")
    if "opencode" in lower or "pi coding agent" in lower: req_evidence.add("D8")
    if re.search(r"route-\d|reaction smiles|reaction smi", lower): req_evidence.add("D1")
    if re.search(r"\d+(?:\.\d+)?\s*%", lower) and re.search(r"(predicted|prediction|\uC608\uCE21)", lower):
        req_ext.add("6"); req_evidence.add("D1")
    if "fischer" in lower or "lecture" in lower or "\uAC15\uC758" in paragraph:
        req_ext.add("17")
    if "australian government" in lower or "\uD638\uC8FC \uC815\uBD80" in paragraph: req_ext.add("14"); req_evidence.add("D6")
    if re.search(r"yield normalization|yield normalisation|\uC218\uC728 \uC815\uADDC\uD654", lower):
        req_ext.update({"6", "8"}); req_evidence.update({"D1", "D4"})
    if re.search(r"benzocaine-live-repro-|reproduction-validation|\uC7AC\uC2E4\uD589", lower):
        req_evidence.add("D10")
    return req_ext, req_evidence


def audit(text, evidence_dir, source_map):
    errors, rows = [], []
    headings=[(i,line) for i,line in enumerate(text.splitlines()) if line.startswith("#")]
    bibliography_heading=next(((i,line) for i,line in headings if re.search(r"references|bibliography|참고문헌|출처 목록",line,re.I)),None)
    evidence_heading=next(((i,line) for i,line in headings if re.search(r"project evidence|프로젝트 증거 파일",line,re.I)),None)
    if bibliography_heading is None:
        return {"status":"failed","errors":["Bibliography/source-list heading not found"],"claim_rows":[]}
    lines=text.splitlines(); bib_line,bib_title=bibliography_heading
    body="\n".join(lines[:bib_line])
    evidence_line=evidence_heading[0] if evidence_heading else None
    if evidence_line is None or evidence_line <= bib_line:
        errors.append("Project evidence-list heading is missing or precedes bibliography")
        bibliography_text="\n".join(lines[bib_line+1:]); evidence_text=""
    else:
        bibliography_text="\n".join(lines[bib_line+1:evidence_line])
        evidence_text="\n".join(lines[evidence_line+1:])
    bibliography = {m.group(1):m.group(2).strip() for m in BIBLIOGRAPHY.finditer(bibliography_text)}
    cited_in_body = set()
    evidence_entries = {(m.group(1) or m.group(2)):m.group(3).strip() for m in EVIDENCE_LIST.finditer(evidence_text)}
    for key, meta in source_map.get("sources",{}).items():
        if meta.get("type") in {"external","course"} and key.isdigit():
            if key not in bibliography: errors.append(f"Bibliography entry [{key}] missing")
            else:
                expected = meta.get("url") or meta.get("file")
                if expected and expected not in bibliography[key]: errors.append(f"Bibliography entry [{key}] points to a different source")
        if key.startswith("D") and key in evidence_entries:
            paths = meta.get("files",[]) or ([meta["file"]] if meta.get("file") else [])
            for item in paths:
                if evidence_dir is not None and not (evidence_dir / item.replace("evidence-run/", "", 1)).exists():
                    errors.append(f"Evidence source [{key}] missing file: {item}")
    claim_blocks=re.split(r"\n(?=-\s)|\n{2,}",body)
    for paragraph_number, paragraph in enumerate(claim_blocks,1):
        stripped=paragraph.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("!") or stripped.startswith("|") or stripped.startswith("---") or re.fullmatch(r"\[figure:\s*[^\]]+\]",stripped):
            continue
        cites=set(CITATION.findall(stripped)); cited_in_body.update(cites)
        req_ext,req_ev=source_requirements(stripped)
        missing_ext=sorted(req_ext-cites,key=lambda x:int(x))
        missing_ev=sorted(req_ev-cites,key=lambda x:int(x[1:]))
        if missing_ext: errors.append(f"Paragraph {paragraph_number}: missing method/source citation(s) {missing_ext}")
        if missing_ev: errors.append(f"Paragraph {paragraph_number}: missing result-evidence citation(s) {missing_ev}")
        # Reject cross-domain citations at sentence scope, even when a paragraph also mentions the unrelated model.
        sentence_text=re.sub(r"(?<=\d)\.(?=\d)", "<DECIMAL>", stripped)
        for sentence in re.split(r"(?<=[.!?])\s+", sentence_text):
            sentence_cites=set(CITATION.findall(sentence))
            low=sentence.lower()
            if re.search(r"\bmopac\b|\bpm7\b|\bgnorm\b",low) and "parrot" not in low and "5" in sentence_cites:
                errors.append(f"Paragraph {paragraph_number}: Parrot source [5] is unrelated to this MOPAC sentence")
            if re.search(r"epi suite|mpbpwin|epiunified",low) and "rxn_yields" not in low and "6" in sentence_cites:
                errors.append(f"Paragraph {paragraph_number}: rxn_yields source [6] is unrelated to this EPI sentence")
        rows.append({"paragraph":paragraph_number,"claim_excerpt":stripped[:260],"citations":sorted(cites),"required_method_sources":sorted(req_ext,key=lambda x:int(x)),"required_project_evidence":sorted(req_ev,key=lambda x:int(x[1:]))})
    for cite in sorted((x for x in cited_in_body if x.isdigit()),key=int):
        if cite not in bibliography: errors.append(f"In-text reference [{cite}] has no bibliography entry")
    for cite in sorted((x for x in cited_in_body if x.startswith("D")),key=lambda x:int(x[1:])):
        if cite not in evidence_entries: errors.append(f"In-text evidence citation [{cite}] has no project evidence-list entry")
    # Course mechanism citation must name its actual lecture pages, and run-specific facts may not cite it as a substitute.
    for paragraph_number, paragraph in enumerate(claim_blocks,1):
        if "fischer" in paragraph.lower() and not re.search(r"\[17,\s*PDF\s+pp\.\s*90\s*[^0-9A-Za-z\s]\s*95\]",paragraph):
            errors.append(f"Paragraph {paragraph_number}: Fischer mechanism must cite the relevant lecture pages 90-95")
    unused=sorted(set(bibliography)-cited_in_body,key=int)
    return {"status":"passed" if not errors else "failed","errors":errors,"bibliography_entries":sorted(bibliography,key=int),"unused_bibliography_entries":unused,"body_citations":sorted(cited_in_body,key=lambda x:(not x.startswith("D"),int(x[1:] if x.startswith("D") else x))),"evidence_list_entries":sorted(evidence_entries,key=lambda x:int(x[1:])),"claim_rows":rows}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--report",type=Path,required=True);p.add_argument("--evidence-dir",type=Path,required=True);p.add_argument("--source-map",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();result=audit(a.report.read_text(encoding="utf-8"),a.evidence_dir,json.loads(a.source_map.read_text(encoding="utf-8")))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"error_count":len(result["errors"]),"unused_bibliography_entries":result.get("unused_bibliography_entries",[]),"output":str(a.output)}))
    return 0 if result["status"]=="passed" else 2

if __name__=="__main__":raise SystemExit(main())
