"""Render saved Solar Markdown with exact run-manifest figures and validated route/step data."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from urllib.parse import unquote
from markdown_it import MarkdownIt

SLOTS = ("catalyst1", "solvent1", "solvent2", "reagent1", "reagent2")
FIGURE_MARKER = re.compile(r"\[figure:\s*([^\]]+)\]")
TRANSFORMS = {"exact_manifest_figure_mapping", "normalized_route_step_table"}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def md_cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")
def token(value) -> str:
    if value is None: return '`"미제공"`'
    if value == "": return '`""`'
    return "`" + str(value).replace("`", "\\`") + "`"
def resolve_asset(item: dict, run: Path, repo: Path) -> Path:
    raw = Path(item["path"])
    candidates = [raw] if raw.is_absolute() else [run / raw, repo / raw]
    matches = {p.resolve() for p in candidates if p.is_file() and sha(p) == item.get("sha256")}
    if len(matches) != 1: raise ValueError(f"Figure asset path/hash is missing or ambiguous for {item.get('figure_id')}")
    return next(iter(matches))
def figure_marker_id(label: str, assets: dict[str, dict]) -> str:
    label = unquote(label.strip()).replace("\\", "/")
    matches = []
    for fid, item in assets.items():
        source = item["source_path"].as_posix()
        if label in {fid, item["path"], source, item["source_path"].name}: matches.append(fid)
    if len(matches) != 1: raise ValueError(f"Figure marker does not identify exactly one manifest item: {label}")
    return matches[0]
def build_table(evidence: dict):
    headers = ["route_id / step_id", "Reaction SMILES (reactants >> product)", "Parrot top candidates (rank / original slots / sequence_score)", "Temperature / time / equivalents / pressure", "rxn_yields predicted yield (%) / status"]
    rows=[]; seen=set(); steps=evidence.get("report_steps", [])
    if not steps: raise ValueError("report-evidence.json has no report_steps")
    for step in steps:
        route,sid,reaction=step.get("route_id"),step.get("step_id"),step.get("reaction_smiles"); key=(route,sid)
        if not all(key) or not reaction or key in seen: raise ValueError(f"Missing or duplicate route/step/reaction key: {key}")
        seen.add(key); conditions=step.get("conditions") or {}; candidates=sorted(conditions.get("candidates", []),key=lambda x:x.get("rank",10**9))[:3]
        candidate_text=[]
        for candidate in candidates:
            slots="; ".join(f"{name}={token(candidate.get(name))}" for name in SLOTS)
            candidate_text.append(f"rank {candidate.get('rank','미제공')}: {slots}; sequence_score={token(candidate.get('sequence_score'))}")
        if not candidate_text: candidate_text=["미제공"]
        prediction=step.get("yield_prediction") or {}; value=prediction.get("yield_percent")
        yield_text="미제공" if value is None else f"{float(value):.2f}% / {prediction.get('yield_status','미제공')}"
        condition_text = "; ".join([
            "temperature=" + ("미제공" if conditions.get("temperature") is None else str(conditions["temperature"])),
            "time=" + ("미제공" if conditions.get("time") is None else str(conditions["time"])),
            "equivalents=" + ("미제공" if conditions.get("equivalents") is None else str(conditions["equivalents"])),
            "pressure=" + ("미제공" if conditions.get("pressure") is None else str(conditions["pressure"])),
        ])
        rows.append([f"{route} / {sid}",reaction,"<br>".join(candidate_text),condition_text,yield_text])
    return headers,rows
def markdown_tables(text: str):
    tokens=MarkdownIt("commonmark").enable("table").parse(text); out=[]; i=0
    while i<len(tokens):
        if tokens[i].type!="table_open": i+=1; continue
        start=tokens[i].map[0]; j=i+1
        while j<len(tokens) and tokens[j].type!="table_close": j+=1
        end=tokens[i].map[1]; rows=[]
        for tok in tokens[i:j+1]:
            if tok.type=="tr_open": rows.append([])
            elif tok.type=="inline" and rows: rows[-1].append(tok.content)
        out.append((start,end,rows)); i=j+1
    return out
def render_table(text: str,evidence:dict):
    headers,rows=build_table(evidence); table=["| "+" | ".join(headers)+" |","|"+"|".join(["---"]*len(headers))+"|"]
    table += ["| "+" | ".join(md_cell(v) for v in row)+" |" for row in rows]; block="\n".join(table)
    tables=markdown_tables(text)
    relevant=[(a,b,t) for a,b,t in tables if t and any("route" in c.lower() and "step" in c.lower() for c in t[0]) and any("yield" in c.lower() or "수율" in c.lower() for c in t[0])]
    if relevant:
        raise ValueError("A route/step conditions-yield table already exists. Refusing to replace its authored cells; prepare the Solar response without this table so the normalized renderer can add the single verified table.")
    lines=text.splitlines()
    headings=[(i,line) for i,line in enumerate(lines) if re.match(r"^#{1,6}\s+",line) and re.search(r"references|bibliography|참고문헌|출처",line,re.I)]
    if not headings: raise ValueError("No explicit bibliography heading for table insertion")
    deepest=max(len(line)-len(line.lstrip("#")) for _,line in headings)
    headings=[(i,line) for i,line in headings if len(line)-len(line.lstrip("#"))==deepest]
    if len(headings)!=1: raise ValueError(f"Ambiguous bibliography subsection for table insertion; found {len(headings)}")
    pos,_=headings[0]; lines[pos:pos]=["","### 단계별 조건·수율 통합표 (정규화 결과)","",block,""]
    return "\n".join(lines)+("\n" if text.endswith("\n") else ""),{"action":"inserted_before_bibliography","row_count":len(rows),"columns":headers}
def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--run-dir",required=True,type=Path); ap.add_argument("--attempt-dir",required=True,type=Path); ap.add_argument("--source-markdown",required=True,type=Path); ap.add_argument("--solar-status",required=True,type=Path); ap.add_argument("--output-dir",required=True,type=Path); ap.add_argument("--source-validation",type=Path,help="Passed provenance for any approved Solar-authored edits")
    a=ap.parse_args(); run=a.run_dir.resolve(); attempt=a.attempt_dir.resolve(); source=a.source_markdown.resolve(); output=a.output_dir.resolve()
    if output.exists(): raise FileExistsError(f"Preserve existing output folder: {output}")
    evidence=load(run/"report-evidence.json"); raw_path=attempt/"solar-response.raw.json"; status=load(a.solar_status.resolve()); raw=load(raw_path); raw_md=raw.get("choices",[{}])[0].get("message",{}).get("content"); source_hash=sha(source)
    model=status.get("returned_model") or status.get("upstream_model") or raw.get("model","")
    if status.get("status")!="success" or not str(model).startswith("solar-pro4"): raise ValueError("Saved response is not a successful Solar Pro 4 response")
    if not isinstance(raw_md,str) or not raw.get("model","").startswith("solar-pro4"): raise ValueError("Saved raw Solar response is missing or invalid")
    if status.get("response_sha256") and status["response_sha256"]!=sha(raw_path): raise ValueError("Solar status response hash does not match raw response")
    source_mode="raw_solar_markdown"
    if source.read_text(encoding="utf-8")!=raw_md:
        if not a.source_validation: raise ValueError("Source Markdown differs from saved Solar response without edit provenance")
        provenance=load(a.source_validation)
        if provenance.get("status")!="passed" or provenance.get("final_report_sha256")!=source_hash or provenance.get("solar_response_sha256")!=sha(raw_path): raise ValueError("Source edit provenance does not validate this Markdown and Solar response")
        source_mode="validated_solar_edit_derivative"
    if not evidence.get("model_status") or not all(evidence["model_status"].get(k)=="success" for k in ("routes","conditions","yields")): raise ValueError("Route, condition and yield model outputs are not all marked successful")
    for rel,expected in evidence.get("source_hashes",{}).items():
        artifact=run/rel
        if not artifact.is_file() or sha(artifact)!=expected: raise ValueError(f"Evidence source hash mismatch: {rel}")
    for name in ("verification.json","step-validation.json"):
        if not (run/name).is_file() or load(run/name).get("status")!="passed": raise ValueError(f"Required run validation did not pass: {name}")
    routes,conditions,yields=load(run/"routes.json"),load(run/"conditions-parrot.json"),load(run/"yields-rxn_yields.json")
    route_steps={(r["route_id"],s["step_id"]):s for r in routes.get("predictions",[]) for s in r.get("steps",[])}
    yield_rows={(y["route_id"],y["step_id"],y["reaction_smiles"]):y for y in yields.get("predictions",[])}; joins=[]
    for step in evidence.get("report_steps",[]):
        key=(step["route_id"],step["step_id"]); reaction=step["reaction_smiles"]; rs=route_steps.get(key)
        if not rs or rs.get("reaction_smiles")!=reaction: raise ValueError(f"Route/reaction mismatch at {key}")
        cond=next((c for c in conditions.get("predictions",[]) if c.get("reaction_smiles")==reaction and any(x.get("route_id")==key[0] and x.get("step_id")==key[1] for x in c.get("steps",[]))),None)
        if cond is None: raise ValueError(f"Parrot route/step/reaction join missing at {key}")
        normalized=step.get("conditions") or {}
        for field in ("reaction_smiles","candidates","temperature","time","yield_percent"):
            if normalized.get(field)!=cond.get(field): raise ValueError(f"Normalized Parrot {field} differs from source at {key}")
        y=step.get("yield_prediction") or {}; raw_y=yield_rows.get((key[0],key[1],reaction))
        if raw_y is None or any(raw_y.get(field)!=y.get(field) for field in ("yield_percent","raw_value","yield_status","conditions_in_input")): raise ValueError(f"Yield join mismatch at {key}")
        joins.append({"route_id":key[0],"step_id":key[1],"reaction_smiles_sha256":hashlib.sha256(reaction.encode()).hexdigest(),"parrot_candidate_count":len(normalized.get("candidates",[])),"yield_percent_raw":y.get("yield_percent"),"yield_status":y.get("yield_status")})
    assets={}; repo=Path(__file__).resolve().parent.parent
    for item in evidence.get("report_figure_assets",[]):
        fid=item.get("figure_id")
        if not fid or fid in assets: raise ValueError("Missing or duplicate figure_id in evidence manifest")
        path=resolve_asset(item,run,repo); assets[fid]={**item,"source_path":path}
    if not assets: raise ValueError("No report_figure_assets listed")
    manifest_path=run/"figures"/"manifest.json"; manifest=load(manifest_path); fig_checks=[]
    for fid,item in assets.items():
        if fid!="target" and "/" in fid:
            rid,sid=fid.split("/",1); step=next((x for x in evidence.get("report_steps",[]) if x.get("route_id")==rid and x.get("step_id")==sid),None)
            if step is not None:
                entry=next((x for x in manifest.get("figures",[]) if x.get("route_id")==rid and x.get("step_id")==sid),None)
                if entry is None or entry.get("reaction_smiles")!=step.get("reaction_smiles"): raise ValueError(f"Figure manifest route/step/reaction mismatch: {fid}")
                item["source_reaction_figure_sha256"] = entry.get("sha256")
        source_rel=item["source_path"].relative_to(run).as_posix() if item["source_path"].is_relative_to(run) else item["source_path"].name
        fig_checks.append({"figure_id":fid,"path_relative_to_run_or_basename":source_rel,"report_asset_sha256":item["sha256"],"source_reaction_figure_sha256":item.get("source_reaction_figure_sha256"),"reaction_image_bytes_match":None if item.get("source_reaction_figure_sha256") is None else item.get("source_reaction_figure_sha256")==item["sha256"],"exact_evidence_asset_match":True})
    text=source.read_text(encoding="utf-8"); markers=list(FIGURE_MARKER.finditer(text)); marker_ids=[figure_marker_id(m.group(1),assets) for m in markers]
    tokens=MarkdownIt("commonmark").enable("table").parse(text); md_images=[child.attrGet("src") for tok in tokens if tok.type=="inline" for child in (tok.children or []) if child.type=="image"]
    md_ids=[]; names=[]
    for src in md_images:
        base=Path(unquote(src.replace("\\","/"))).name; names.append(base); matches=[fid for fid,item in assets.items() if base==Path(item["path"]).name and (src==base or src.replace("\\","/").endswith("/"+base))]
        if len(matches)!=1: raise ValueError(f"Markdown image does not map to one exact manifest asset: {src}")
        md_ids.append(matches[0])
    if len(names)!=len(set(names)): raise ValueError("Duplicate Markdown image basenames are ambiguous")
    if set(marker_ids)|set(md_ids)!=set(assets): raise ValueError("Report figure references do not cover exactly the figure manifest")
    if any(marker_ids.count(fid) not in (0,1,2) for fid in assets): raise ValueError("Unexpected figure marker multiplicity")
    rendered=text
    for fid,item in assets.items():
        marker=[m for m in FIGURE_MARKER.finditer(rendered) if figure_marker_id(m.group(1),assets)==fid]
        for index,m in reversed(list(enumerate(marker))):
            replacement=f"![{item['caption']}](assets/{Path(item['path']).name})" if index==0 else ""
            rendered=rendered[:m.start()]+replacement+rendered[m.end():]
    if FIGURE_MARKER.search(rendered): raise ValueError("Unresolved figure marker remains")
    rendered,table_info=render_table(rendered,evidence)
    output.mkdir(parents=True,exist_ok=False); mdout=output/"report.md"; mdout.write_text(rendered,encoding="utf-8")
    layout={"status":"passed","renderer":"scripts/render_report_evidence.py","run_id":status.get("run_id"),"source_markdown_mode":source_mode,"source_markdown_sha256":source_hash,"solar_raw_response_sha256":sha(raw_path),"rendered_markdown_sha256":sha(mdout),"report_evidence_sha256":sha(run/"report-evidence.json"),"transformations":sorted(TRANSFORMS),"scientific_prose_modified":False,"figure_checks":fig_checks,"figure_marker_ids":marker_ids,"markdown_image_ids":md_ids,"route_step_joins":joins,"table":table_info}
    save(output/"layout-validation.json",layout)
    print(json.dumps({"status":"passed","figure_count":len(assets),"route_step_count":len(joins),"table_action":table_info["action"],"table_rows":table_info["row_count"]},ensure_ascii=True,indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
