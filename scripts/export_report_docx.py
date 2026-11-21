"""Format an unchanged Solar Markdown response into an illustrated, linked DOCX."""
import argparse
from pathlib import Path
import re
from urllib.parse import unquote
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from markdown_it import MarkdownIt
from PIL import Image
from _runtime import digest, load, save, local_artifact


def font_run(run, size=None, bold=False, italic=False, code=False):
    run.font.name = "Consolas" if code else "Malgun Gothic"
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Malgun Gothic")
    if size:
        run.font.size = Pt(size)
    run.bold, run.italic = bold, italic


def link(paragraph, text, url, bold=False, italic=False):
    element = OxmlElement("w:hyperlink")
    element.set(qn("r:id"), paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True))
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    for key in ["ascii", "hAnsi", "eastAsia"]:
        fonts.set(qn("w:" + key), "Malgun Gothic")
    props.append(fonts)
    color = OxmlElement("w:color"); color.set(qn("w:val"), "175080"); props.append(color)
    if bold:
        props.append(OxmlElement("w:b"))
    if italic:
        props.append(OxmlElement("w:i"))
    run.append(props)
    content = OxmlElement("w:t"); content.text = text; run.append(content)
    element.append(run); paragraph._p.append(element)


def field(paragraph, name):
    run = paragraph.add_run()
    node = OxmlElement("w:fldSimple"); node.set(qn("w:instr"), name)
    run._r.addnext(node)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--solar-status", required=True, type=Path)
    parser.add_argument("--citation-edit-validation", type=Path,
                        help="Verified provenance for a narrowly scoped citation-only edit after a targeted Solar merge")
    parser.add_argument("--layout-validation", type=Path,
                        help="Provenance for exact manifest figure mapping and normalized-result table rendering")
    parser.add_argument("--verified-edits-validation", type=Path,
                        help="Validation record for Solar-approved sentence edits plus explicitly authorized local table/citation formatting edits")
    parser.add_argument("--compact-layout", action="store_true",
                        help="Tighter typography and spacing for a page-limit export; report wording remains unchanged")
    args = parser.parse_args()
    status = load(args.solar_status)
    returned_model = status.get("returned_model") or status.get("upstream_model") or status.get("model") or ""
    if status.get("status") != "success" or not returned_model.startswith("solar-pro4"):
        raise ValueError("A verified Solar Pro 4 report is required")
    response_path = args.solar_status.parent / "solar-response.raw.json"
    response = load(response_path)
    original = response["choices"][0]["message"]["content"]
    text = args.markdown.read_text(encoding="utf-8")
    evidence = load(args.run_dir / "report-evidence.json")
    selected_provenance = sum(bool(x) for x in (args.layout_validation, args.verified_edits_validation, args.citation_edit_validation))
    if selected_provenance > 1:
        raise ValueError("Choose only one report transformation provenance record")
    if args.layout_validation:
        layout = load(args.layout_validation)
        allowed = ({"exact_manifest_figure_mapping", "manifest_visualizer_figure_completion", "verified_route_comparison_matrix", "normalized_route_step_table"}
                   if layout.get("table", {}).get("action") in {"inserted_verified_route_comparison_matrix", "inserted_verified_route_comparison_matrix_and_step_summary"}
                   else {"exact_manifest_figure_mapping", "normalized_route_step_table", "manifest_visualizer_figure_completion"})
        if (layout.get("status") != "passed"
                or layout.get("rendered_markdown_sha256") != digest(args.markdown)
                or layout.get("solar_raw_response_sha256") != digest(response_path)
                or layout.get("report_evidence_sha256") != digest(args.run_dir / "report-evidence.json")
                or set(layout.get("transformations", [])) != allowed
                or layout.get("scientific_prose_modified") is not False):
            raise ValueError("Evidence-rendered Markdown does not match its verified layout provenance")
    elif args.verified_edits_validation:
        validation = load(args.verified_edits_validation)
        if (validation.get("status") != "passed"
                or validation.get("final_report_sha256") != digest(args.markdown)
                or validation.get("solar_response_sha256") != digest(response_path)
                or validation.get("solar_targeted_blocks_verified") is not True
                or validation.get("approved_local_edits_verified") is not True):
            raise ValueError("Verified-edit provenance does not validate this report/response")
    elif args.citation_edit_validation:
        validation = load(args.citation_edit_validation)
        if (validation.get("status") != "passed"
                or validation.get("final_report_sha256") != digest(args.markdown)
                or validation.get("solar_response_sha256") != digest(response_path)
                or validation.get("citation_only_changes") is not True
                or validation.get("solar_targeted_blocks_verified") is not True):
            raise ValueError("Citation-only edit provenance does not validate this report/response")
    elif original != text:
        raise ValueError("Markdown was modified after Solar generation")
    output = args.markdown.with_suffix(".docx")
    if output.exists():
        raise FileExistsError(output)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    if args.compact_layout:
        sec.top_margin, sec.bottom_margin = Cm(1.35), Cm(1.3)
        sec.left_margin = sec.right_margin = Cm(1.6)
        style_sizes = [("Normal",9.5),("Title",16),("Heading 1",12.5),("Heading 2",10.5),("Heading 3",9.5)]
        base_spacing, base_after = 1.03, 3
    else:
        sec.top_margin, sec.bottom_margin = Cm(2), Cm(1.8)
        sec.left_margin = sec.right_margin = Cm(2)
        style_sizes = [("Normal",11),("Title",18),("Heading 1",14),("Heading 2",12),("Heading 3",11)]
        base_spacing, base_after = 1.25, 6
    for name, size in style_sizes:
        style = doc.styles[name]
        style.font.name = "Malgun Gothic"; style.font.size = Pt(size)
        style.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Malgun Gothic")
        style.paragraph_format.space_after = Pt(base_after)
        style.paragraph_format.line_spacing = base_spacing
        if name.startswith("Heading"):
            style.font.color.rgb = RGBColor.from_string("17365D")
            style.paragraph_format.keep_with_next = True
            style.paragraph_format.space_before = Pt(12)
    doc.core_properties.author = "Solar Pro 4 (" + returned_model + ")"
    doc.core_properties.title = text.splitlines()[0].lstrip("# ")
    doc.core_properties.subject = evidence["target"]["name"] + ": actual model predictions; experimental validation not performed"
    header = sec.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    font_run(header.add_run("AI 유기합성 프로젝트 | Solar Pro 4"), size=8)
    footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field(footer,"PAGE"); footer.add_run(" / "); field(footer,"NUMPAGES")
    known = {}
    for item in evidence["report_figure_assets"]:
        path = Path(item["path"])
        if not path.is_file():
            folder = args.run_dir / ("target" if item["figure_id"]=="target" else "figures")
            path = local_artifact(item["path"],folder)
        if path.name in known:raise ValueError("Figure basenames must be unique")
        if digest(path)!=item["sha256"]:raise ValueError("Evidence figure hash mismatch")
        known[path.name]=path
    images = []
    links = []

    def add_text(p, content, bold=False, italic=False, code=False, href=None):
        if href:
            link(p,content,href,bold,italic); links.append(href); return
        # Make source URLs clickable even when the model wrote plain URLs.
        pieces = re.split(r"(https?://[^\s<>]+)", content) if not code else [content]
        for piece in pieces:
            if piece.startswith(("https://","http://")) and not code:
                link(p,piece,piece,bold,italic); links.append(piece)
            else:
                font_run(p.add_run(piece),bold=bold,italic=italic,code=code)

    def inline(p, children):
        bold = italic = False
        href = None
        for token in children or []:
            if token.type == "strong_open": bold = True
            elif token.type == "strong_close": bold = False
            elif token.type == "em_open": italic = True
            elif token.type == "em_close": italic = False
            elif token.type == "link_open": href = token.attrGet("href")
            elif token.type == "link_close": href = None
            elif token.type in {"text","code_inline"}:
                if token.type == "text" and "**" in token.content:
                    # CommonMark does not recognize a closing strong delimiter immediately
                    # followed by some CJK letters. Render that literal delimiter pair as bold
                    # in DOCX without changing the Solar-authored Markdown source.
                    pieces = re.split(r"(\*\*.*?\*\*)", token.content)
                    for piece in pieces:
                        if piece.startswith("**") and piece.endswith("**") and len(piece) >= 4:
                            add_text(p,piece[2:-2],True,italic,False,href)
                        elif piece:
                            add_text(p,piece,bold,italic,False,href)
                else:
                    add_text(p,token.content,bold,italic,token.type=="code_inline",href)
            elif token.type == "softbreak": add_text(p," ")
            elif token.type == "hardbreak": p.add_run().add_break()
            elif token.type == "html_inline" and token.content.lower().startswith("<br"):
                p.add_run().add_break()
            elif token.type == "image":
                requested = unquote(token.attrGet("src") or "").replace("\\","/")
                basename = requested.rsplit("/",1)[-1]
                if basename not in known:
                    raise ValueError("Unrecognized report image: " + requested)
                path = known[basename]
                with Image.open(path) as picture:
                    ratio = picture.height / picture.width
                width = min(16.0, (4.7 if args.compact_layout else 6.0) / ratio)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.keep_together = True
                p.add_run().add_picture(str(path),width=Cm(width))
                p.add_run().add_break()
                font_run(p.add_run(token.content),size=9,italic=True)
                images.append({"requested":requested,"source_path":str(path.resolve()),
                               "sha256":digest(path),"caption":token.content})

    tokens = MarkdownIt("commonmark").enable("table").parse(text)
    index = 0
    lists = []
    prefix = None
    table_count = 0
    deferred_table_intro = None
    deferred_table_heading = None
    while index < len(tokens):
        token = tokens[index]
        if token.type in {"bullet_list_open","ordered_list_open"}:
            lists.append({"kind":token.type,"next":int(token.attrGet("start") or 1)})
        elif token.type in {"bullet_list_close","ordered_list_close"}:
            lists.pop()
        elif token.type == "list_item_open":
            current = lists[-1]
            prefix = "• " if current["kind"] == "bullet_list_open" else str(current["next"]) + ". "
            current["next"] += 1
        elif token.type in {"heading_open","paragraph_open"}:
            content = tokens[index+1]
            if (token.type == "heading_open" and content.type == "inline"
                    and content.content.startswith("4. ")
                    and "\uD1B5\uD569" in content.content):
                deferred_table_heading = (content, int(token.tag[1:]))
                index += 2
                continue
            if (token.type == "heading_open" and content.type == "inline"
                    and index + 3 < len(tokens) and tokens[index+2].type == "heading_close"
                    and tokens[index+3].type == "table_open"):
                deferred_table_heading = (content, int(token.tag[1:]))
                index += 2
                continue
            if (token.type == "paragraph_open" and content.type == "inline"
                    and content.content.startswith("\uC544\uB798 \uD45C\uB294 \uC120\uC815\uB41C")
                    and index + 3 < len(tokens) and tokens[index+3].type == "table_open"):
                deferred_table_intro = content
                index += 2
                continue
            if content.type != "inline":
                raise ValueError("Unexpected Markdown block")
            if token.type == "heading_open":
                level = int(token.tag[1:])
                p = doc.add_paragraph(style="Title" if level==1 else "Heading " + str(min(level-1,3)))
            else:
                p = doc.add_paragraph()
                if re.match(r"^\*\*route-\d+", content.content):
                    p.paragraph_format.keep_with_next = True
                if lists:
                    p.paragraph_format.left_indent = Cm(.45*len(lists))
                    p.paragraph_format.first_line_indent = Cm(-.35)
                    if prefix:
                        p.add_run(prefix); prefix = None
            inline(p,content.children)
            index += 1
        elif token.type == "table_open":
            rows = []; row = None
            cursor = index+1
            while tokens[cursor].type != "table_close":
                t = tokens[cursor]
                if t.type == "tr_open": row=[]; rows.append(row)
                elif t.type == "inline": row.append(t)
                cursor += 1
            # Compact the integrated route/conditions/yield table for a readable landscape page.
            if len(rows[0]) == 10 and any("Parrot" in cell.content for cell in rows[0]):
                inline_parser = MarkdownIt("commonmark")
                def cell_text(value: str):
                    parsed = inline_parser.parseInline(value, {})
                    return parsed[0]
                compact = [[rows[0][0], cell_text("\uC804\uAD6C\uCCB4 \u2192 \uC0DD\uC131\uBB3C / \uC791\uC6A9\uAE30 \uBCC0\uD654"),
                            cell_text("Parrot \uCD5C\uC0C1\uC704 \uD6C4\uBCF4 / \uC11C\uC5F4 \uC810\uC218"),
                            cell_text("\uC628\uB3C4\u00B7\uC2DC\uAC04\u00B7\uB2F9\uB7C9\u00B7\uC870\uAC74 \uC218\uC728"), rows[0][8], rows[0][9]]]
                labels = ["\uC628\uB3C4", "\uC2DC\uAC04", "\uB2F9\uB7C9", "\uC870\uAC74 \uC218\uC728"]
                for row in rows[1:]:
                    condition_values = [row[i].content.strip() for i in range(4, 8)]
                    if all(value == "NOT SUPPLIED" for value in condition_values):
                        condition_text = "\uC628\uB3C4\u00B7\uC2DC\uAC04\u00B7\uB2F9\uB7C9\u00B7\uC870\uAC74 \uC218\uC728 \uBAA8\uB450 NOT SUPPLIED"
                    else:
                        condition_text = " / ".join(f"{label}: {value}" for label, value in zip(labels, condition_values))
                    compact.append([row[0], row[1], cell_text(f"{row[2].content} / score {row[3].content}"),
                                    cell_text(condition_text), row[8], row[9]])
                rows = compact
            columns = len(rows[0])
            header_text = " ".join(cell.content for cell in rows[0]).lower()
            normalized_route_table = ("parrot top candidates" in header_text and "rxn_yields predicted yield" in header_text)
            comparison_candidate_table = ("parrot rank" in header_text and "parrot original slots" in header_text)
            step_conditions_summary = ("parrot rank 1" in header_text and "original slots" in header_text and "yield-bert" in header_text)
            landscape = columns > 5 or normalized_route_table or comparison_candidate_table or step_conditions_summary
            if not landscape and doc.paragraphs:
                doc.paragraphs[-1].paragraph_format.keep_with_next = True
            if landscape:
                # Orientation changes need explicit page boundaries in Word.
                # Continuous section breaks can leave a blank page between a
                # landscape data table and the following portrait section.
                section = doc.add_section(WD_SECTION.NEW_PAGE)
                section.orientation = WD_ORIENT.LANDSCAPE
                section.page_width, section.page_height = Cm(29.7), Cm(21)
                section.top_margin = section.bottom_margin = Cm(0.9 if args.compact_layout else 1.2)
                section.left_margin = section.right_margin = Cm(0.9 if args.compact_layout else 1.2)
                if deferred_table_intro is not None:
                    intro = doc.add_paragraph()
                    intro.paragraph_format.space_after = Pt(4)
                    intro.paragraph_format.keep_with_next = True
                    inline(intro, deferred_table_intro.children)
                    deferred_table_intro = None
                usable_width = 27.3
                if columns == 5 and normalized_route_table:
                    weights = [1.4, 5.0, 10.0, 5.0, 2.4]
                elif columns == 5 and comparison_candidate_table:
                    weights = [2.8, 1.2, 2.5, 14.8, 4.0]
                elif columns == 5 and step_conditions_summary:
                    weights = [2.0, 6.0, 8.0, 6.0, 3.0]
                elif columns == 6 and comparison_candidate_table:
                    weights = [2.4, 5.5, 1.2, 2.4, 9.0, 3.0]
                elif columns == 6:
                    first_header = rows[0][0].content.strip().lower()
                    weights = ([1.0,2.3,3.2,3.0,1.5,2.2] if first_header.startswith("route / step")
                               else [1.6,1.8,1.8,2.4,1.6,2.0])
                elif columns == 7:
                    weights = [0.9,0.65,1.0,1.35,2.0,2.7,1.6]
                elif columns == 10:
                    weights = [1.1,1.1,3.0,1.1,1.3,1.3,1.3,1.3,1.7,1.3]
                else:
                    weights = [1.0]*columns
                if len(weights) != columns: weights = [1.0]*columns
                total_weight = sum(weights)
                widths = [usable_width*w/total_weight for w in weights]
            else:
                usable_width = 17.0
                weights = ([1.25,2.2,2.4,2.8,1.9] if columns == 5 else [1.0]*columns)
                if len(weights) != columns: weights = [1.0]*columns
                total_weight = sum(weights)
                widths = [usable_width*w/total_weight for w in weights]
            if deferred_table_heading is not None:
                heading_content, heading_level = deferred_table_heading
                title = doc.add_paragraph(style="Heading 1" if heading_level <= 2 else "Heading 3")
                title.paragraph_format.keep_with_next = True
                inline(title, heading_content.children)
                deferred_table_heading = None
            table = doc.add_table(rows=0, cols=columns); table.style="Table Grid"; table.autofit=False
            for column, width in zip(table.columns,widths): column.width=Cm(width)
            for row_index, cells in enumerate(rows):
                cells_out = table.add_row().cells
                for cell, value, width in zip(cells_out,cells,widths):
                    cell.width=Cm(width)
                    p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(2 if args.compact_layout else 3)
                    p.paragraph_format.line_spacing=1.04 if args.compact_layout else 1.1
                    p.paragraph_format.keep_with_next = row_index < len(rows)-1
                    inline(p,value.children)
                    for run in p.runs:
                        run.font.size=Pt(9 if args.compact_layout else 9)
                        if row_index==0: run.bold=True
                    if row_index==0:
                        shade=OxmlElement("w:shd");shade.set(qn("w:fill"),"E7EEF6");cell._tc.get_or_add_tcPr().append(shade)
                trpr=table.rows[-1]._tr.get_or_add_trPr();trpr.append(OxmlElement("w:cantSplit"))
                if row_index==0:trpr.append(OxmlElement("w:tblHeader"))
            table_count += 1
            # A blank portrait paragraph between a full landscape table page
            # and the following section can consume an otherwise empty page.
            if not landscape:
                doc.add_paragraph().paragraph_format.space_after=Pt(2)
            if landscape:
                portrait = doc.add_section(WD_SECTION.NEW_PAGE)
                portrait.orientation = WD_ORIENT.PORTRAIT
                portrait.page_width, portrait.page_height = Cm(21), Cm(29.7)
                portrait.top_margin, portrait.bottom_margin = ((Cm(1.35), Cm(1.3)) if args.compact_layout else (Cm(2), Cm(1.8)))
                portrait.left_margin = portrait.right_margin = Cm(1.6 if args.compact_layout else 2)
            index=cursor
        elif token.type in {"fence","code_block"}:
            p=doc.add_paragraph()
            font_run(p.add_run(token.content.rstrip("\n")),size=9,code=True)
        index += 1
    if len(images)!=len(known) or {Path(x["source_path"]).name for x in images} != set(known):
        raise ValueError("Report must embed exactly the selected evidence figures")
    doc.save(output)
    save(output.parent / "docx-export.json",{
        "status":"success","solar_returned_model":returned_model,
        "markdown_sha256":digest(args.markdown),"solar_response_sha256":digest(response_path),
        "docx_path":str(output.resolve()),"docx_sha256_before_word":digest(output),
        "images":images,"table_count":table_count,"external_links":sorted(set(links)),
        "authoring_note":("Solar-authored targeted sentences verified; approved local evidence-path and table-format edits applied; Markdown-to-DOCX formatting applied."
                          if args.verified_edits_validation else ("Solar targeted sections preserved; source-number citations were independently validated; Markdown-to-DOCX formatting applied."
                          if args.citation_edit_validation else "Original Solar text unchanged; only Markdown-to-DOCX formatting applied.")),
        "citation_edit_validation":str(args.citation_edit_validation.resolve()) if args.citation_edit_validation else None,
        "verified_edits_validation":str(args.verified_edits_validation.resolve()) if args.verified_edits_validation else None,
        "layout_preset":"compact" if args.compact_layout else "standard"})
    print(f"DOCX written: {output}; embedded images: {len(images)}; tables: {table_count}")


if __name__ == "__main__":
    main()
