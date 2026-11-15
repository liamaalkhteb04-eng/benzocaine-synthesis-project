"""Apply Solar-authored replacement blocks to a preserved report and slot-verified tables."""
import argparse, hashlib, json, re
from pathlib import Path
from audit_parrot_slots import verify_run

MARKERS = {
 "section2": ("<<<SECTION_2_START>>>", "<<<SECTION_2_END>>>"),
 "mechanism": ("<<<ROUTE05_MECHANISM_START>>>", "<<<ROUTE05_MECHANISM_END>>>"),
 "course_table": ("<<<COURSE_TABLE_ROW_START>>>", "<<<COURSE_TABLE_ROW_END>>>"),
 "route05_condition": ("<<<ROUTE05_CONDITION_PARAGRAPH_START>>>", "<<<ROUTE05_CONDITION_PARAGRAPH_END>>>"),
 "integrated_row": ("<<<INTEGRATED_TABLE_ROW_START>>>", "<<<INTEGRATED_TABLE_ROW_END>>>"),
 "parrot_summary": ("<<<PARROT_SUMMARY_START>>>", "<<<PARROT_SUMMARY_END>>>"),
 "section7": ("<<<SECTION_7_START>>>", "<<<SECTION_7_END>>>"),
}


def sha(data): return hashlib.sha256(data).hexdigest()


def extract_blocks(response):
    blocks = {}
    for name, (start, end) in MARKERS.items():
        if response.count(start) != 1 or response.count(end) != 1:
            raise ValueError(f"Solar response must contain one pair of {name} markers")
        blocks[name] = response.split(start, 1)[1].split(end, 1)[0].strip()
        if not blocks[name]: raise ValueError(f"Solar block {name} is empty")
    return blocks


def replace_section(text, start_heading, end_heading, replacement):
    a = text.index(start_heading)
    b = text.index(end_heading, a + len(start_heading))
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


def parse_route05(raw_path):
    obj=json.loads(Path(raw_path).read_text(encoding="utf-8"))
    reaction="CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1"
    rows=[r for r in obj["predictions"] if r.get("reaction_smiles")==reaction and
          ("route-05","step-02") in [(s.get("route_id"),s.get("step_id")) for s in r.get("steps",[])]]
    if len(rows)!=1: raise ValueError("Exact route-05/step-02 reaction row not unique")
    row=rows[0]; top=next((c for c in row["candidates"] if c.get("rank")==1),None)
    expected={"catalyst1":"","solvent1":"CCO","solvent2":"","reagent1":"CCOCC","reagent2":"FB(F)F"}
    if not top or any(top.get(k)!=v for k,v in expected.items()): raise ValueError("Raw Parrot slots do not match resolved slot audit")
    return reaction, top


def markdown_cells(line):
    return line.strip().split("|")


def apply(source, blocks, raw_path):
    text=source
    # Preserve the existing section-2 heading, then insert Solar's selection comparison.
    section2=blocks["section2"]
    section2=section2.replace("## 2.1 경로 선정 및 비교", "### 2.1 경로 선정 및 비교", 1)
    section2=section2.replace("ethyl 4-aminobenzoate(N-acyl)", "ethyl 4-acetamidobenzoate")
    section2=section2.replace("ethyl 4-aminobenzoate (N-acyl)", "ethyl 4-acetamidobenzoate")
    if not section2.startswith("### 2.1"):
        raise ValueError("Unexpected Solar section-2 heading")
    section2="## 2. 탐색 범위와 경로 선정\n\n"+section2
    text=replace_section(text,"## 2. 탐색 범위와 경로 선정","## 3. 대표 경로의 단계별 구조 변화와 조건·수율",section2)
    _,top=parse_route05(raw_path)
    # Replace route-05 electron-flow paragraph authored by Solar; retain the reaction figure and its surrounding step text.
    mechanism="**작용기와 전자 이동.** "+blocks["mechanism"]+" [17, PDF pp. 90–95][5][D1]."
    start_marker="**작용기와 전자 이동.** route-05/step-02"
    start=text.index(start_marker)
    end=text.find("\n\n#### ",start)
    if end<0: raise ValueError("Could not locate next subsection after route-05 mechanism")
    text=text[:start]+mechanism+text[end:]
    # Replace the existing condition paragraph with Solar-authored corrected wording.
    start_marker="route-05/step-02의 Parrot 최상위 후보(rank 1)"
    start=text.index(start_marker)
    end=text.index("\n\n",start)
    cond=blocks["route05_condition"].rstrip()
    if "[6]" not in cond: cond += " [6][D4]"
    text=text[:start]+cond+text[end:]
    slot_cell=(f"catalyst1: (빈 슬롯); solvent1: `{top['solvent1']}`; solvent2: (빈 슬롯); "
               f"reagent1: `{top['reagent1']}`; reagent2: `{top['reagent2']}` (모델 슬롯; 실험 역할 미검증)")
    # Repair the existing lecture comparison table row from raw fields; keep all other rows/table structure.
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("| 촉매/시약/용매 |"):
            cells=markdown_cells(line)
            if len(cells)!=5: raise ValueError("Unexpected lecture comparison table column count")
            cells[3]=" "+slot_cell+" [5][D1] "
            lines[i]="|".join(cells)
    text="\n".join(lines)+"\n"
    # Repair the selected route/step row in the existing integrated table, preserving its columns.
    lines=text.splitlines()
    found=0
    for i,line in enumerate(lines):
        if line.startswith("| route-05 / step-02 |"):
            cells=markdown_cells(line)
            if len(cells)!=8: raise ValueError("Unexpected integrated conditions/yield table column count")
            cells[4]=(f" Parrot rank-1 raw fields: catalyst1 (empty); solvent1 `{top['solvent1']}`; "
                      f"solvent2 (empty); reagent1 `{top['reagent1']}`; reagent2 `{top['reagent2']}`; "
                      f"sequence_score {top['sequence_score']:.6f} [5][D1] ")
            cells[6]=cells[6].rstrip()+" [6][8][D1][D4] "
            lines[i]="|".join(cells); found+=1
    if found!=1: raise ValueError(f"Expected one integrated route-05/step-02 row, found {found}")
    text="\n".join(lines)+"\n"
    # Fix the Parrot model narrative using exact field order; no candidate or score is changed.
    lines=text.splitlines()
    changed=0
    for i,line in enumerate(lines):
        if "route-05/step-02의 최상위 후보는" in line and "Parrot은 반응 SMILES" in line:
            line=re.sub(r"route-05/step-02의 최상위 후보는 .*?−2\.1754837036132812이다", 
                f"route-05/step-02의 rank-1 후보는 catalyst1 빈 값, solvent1 `{top['solvent1']}`, solvent2 빈 값, reagent1 `{top['reagent1']}`, reagent2 `{top['reagent2']}`, sequence_score {top['sequence_score']:.16f}이다",line)
            lines[i]=line;changed+=1
    if changed!=1: raise ValueError("Expected to correct one Parrot model-summary example")
    text="\n".join(lines)+"\n"

    # Place citations beside route-selection claims, model outputs, and nonexperimental comparisons.
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("이번 탐색에서는 총 12개 경로") and "[2][D1]" not in line: lines[i]=line+" [2][D1]"
        elif line.startswith("아래 표는 세 경로의 단계 수") and "[6][8][D1][D4]" not in line: lines[i]=line+" [6][8][D1][D4]"
        elif line.startswith("Parrot 조건 필드는 모델 데이터셋") and "[5][D1]" not in line: lines[i]=line+" [5][D1]"
        elif line.startswith("route-01의 rank 1과 rank 4") and "[2][5][D1][D4]" not in line: lines[i]=line+" [2][5][D1][D4]"
        elif line.startswith("모델 stock 플래그는 경로 탐색기") and "[2][D1]" not in line: lines[i]=line+" [2][D1]"
        elif line.startswith("이 비교에서 route-01을 먼저") and "[2][5][6][8][D1][D4]" not in line: lines[i]=line+" [2][5][6][8][D1][D4]"
    text="\n".join(lines)+"\n"
    # Section 7 title/body is Solar-authored. Add evidence citations to its route-priority paragraph.
    s7="## 7. 종합 결론 및 실험 전 확인 목록"
    if s7 not in blocks["section7"]: raise ValueError("Unexpected Section-7 heading")
    section7=blocks["section7"]
    # One Solar phrase reverses the route-01 functional-group change; normalize it against the stored reaction SMILES and unchanged section 3 explanation.
    bad="route-01은 한 단계로 에스터가 아민으로 바뀌는 변환이 분명하고"
    good="route-01은 한 단계에서 방향족 니트로기가 아미노기로 바뀌고 에틸 에스터는 유지되는 구조 변화가 분명하며"
    if section7.count(bad)!=1: raise ValueError("Expected exact route-01 structure typo was not found once in Solar Section 7")
    section7=section7.replace(bad,good,1)
    # Attach run evidence to Solar-authored synthesis and analysis conclusions.
    section7=section7.replace("이 결과들을 연결해도 반응 성공이나 전체 수율이 검증된 것은 아니다.",
                              "이 결과들을 연결해도 반응 성공이나 전체 수율이 검증된 것은 아니다[D5][D6][D7].")
    section7=section7.replace("현재 근거에서는 route-01을 먼저 문헌과 시약 정보를 확인할 후보로, route-02를 단일 단계 대체 경로로, route-05를 단계 수와 중간체 준비를 비교하기 위한 비교 경로로 본다.",
        "현재 근거에서는 route-01을 먼저 문헌과 시약 정보를 확인할 후보로, route-02를 단일 단계 대체 경로로, route-05를 단계 수와 중간체 준비를 비교하기 위한 비교 경로로 본다[2][5][6][8][D1][D4].")
    # Add no other model-authored output outside named sections.
    text=replace_section(text,"## 7. 조건부 경로 권고와 미해결 질문","## 8. 재현 방법",section7)
    # The checklist is a claim-bearing evidence summary; cite the actual route bundle.
    paragraphs=text.split("\n\n")
    for i,paragraph in enumerate(paragraphs):
        if "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1" in paragraph and "이 단계는 모델 경로" in paragraph and "[D1]" not in paragraph:
            paragraphs[i]=paragraph+" [D1]"
    text="\n\n".join(paragraphs)
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("- route-01/step-01:") and "[D1]" not in line:
            lines[i]=line+" [D1]"
        if line.startswith("현재까지의 근거는 route-01을") and "[D1]" not in line:
            lines[i]=line+" [D1][D5][D6][D7]"
    text="\n".join(lines)+"\n"
    return text, blocks


def main():
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--response",type=Path,required=True);p.add_argument("--raw-conditions",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--manifest",type=Path,required=True);a=p.parse_args()
    raw_response=json.loads(a.response.read_text(encoding="utf-8"));content=raw_response["choices"][0]["message"]["content"]
    blocks=extract_blocks(content);source_bytes=a.source.read_bytes();source=source_bytes.decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    final,used=apply(source,blocks,a.raw_conditions);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(final,encoding="utf-8")
    status=json.loads((a.response.parent/"solar-status.json").read_text(encoding="utf-8"))
    manifest={"status":"solar_authored_targeted_replacements_applied","source_report_path":str(a.source.resolve()),"source_report_sha256":sha(source_bytes),"solar_response_sha256":sha(a.response.read_bytes()),"status_response_sha256":status.get("response_sha256"),"merged_report_sha256":sha(a.output.read_bytes()),"raw_conditions_sha256":sha(a.raw_conditions.read_bytes()),"blocks_used":{k:sha(v.encode("utf-8")) for k,v in used.items()},"changes":["Solar-authored section 2 and section 7 replacements","Solar-authored route-05/step-02 electron-flow and condition prose","Parrot fields in existing tables rebuilt from exact raw candidate slots","route-01 nitro-to-amino description normalized to source reaction","route-02 precursor name normalized to route structure"],"solar_call_count":1,"retry_count":0,"new_science_calculations":False}
    a.manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"report":str(a.output.resolve()),"manifest":str(a.manifest.resolve()),"sha256":manifest["merged_report_sha256"],"solar_blocks":list(used)},ensure_ascii=False,indent=2))

if __name__=="__main__":main()










