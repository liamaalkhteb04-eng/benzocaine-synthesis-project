"""Target-neutral renderer tests; fixtures are synthetic and are not model outputs."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from render_report_evidence import build_step_summary_table, build_table, figure_marker_id, render_table


class ReportEvidenceRendererTests(unittest.TestCase):
    def setUp(self):
        self.evidence = {
            "report_steps": [{
                "route_id": "route-x", "step_id": "step-01", "reaction_smiles": "A.B>>C",
                "conditions": {
                    "candidates": [{
                        "rank": 1, "catalyst1": "", "solvent1": "O", "solvent2": "",
                        "reagent1": None, "reagent2": "", "sequence_score": -1.0
                    }],
                    "temperature": None, "time": None, "equivalents": None, "pressure": None
                },
                "yield_prediction": {"yield_percent": 12.345, "yield_status": "predicted_not_validated", "conditions_in_input": False}
            }]
        }

    def test_table_preserves_route_step_slots_missing_values_and_display_rounding(self):
        headers, rows = build_table(self.evidence)
        self.assertEqual(rows[0][0], "route-x / step-01")
        self.assertIn('solvent1=`O`', rows[0][2])
        self.assertIn('reagent1=`"미제공"`', rows[0][2])
        self.assertIn('reagent2=`""`', rows[0][2])
        self.assertIn("pressure=미제공", rows[0][3])
        self.assertEqual(rows[0][4], "12.35% / predicted_not_validated")
        self.assertEqual(len(headers), len(rows[0]))

    def test_step_summary_is_one_rank1_row_and_distinguishes_absent_output_fields(self):
        headers, rows = build_step_summary_table(self.evidence)
        self.assertEqual(headers[0], "route_id / step_id")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "route-x / step-01 [D1]")
        self.assertIn("catalyst1=`\"\"`", rows[0][2])
        self.assertIn("reagent1=`\"미제공\"`", rows[0][2])
        self.assertIn("solvent1=`O`", rows[0][2])
        self.assertIn("temperature=미제공", rows[0][3])
        self.assertIn("equivalents=출력 필드 없음", rows[0][3])
        self.assertEqual(rows[0][4], "12.35% / predicted_not_validated (conditions_in_input=False)")

    def test_figure_reference_requires_exact_manifest_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "figure.png"
            path.write_bytes(b"fixture")
            item = {"source_path": path, "path": "figures/figure.png"}
            self.assertEqual(figure_marker_id("route-x/step-01", {"route-x/step-01": item}), "route-x/step-01")
            with self.assertRaises(ValueError):
                figure_marker_id("missing-figure", {"route-x/step-01": item})

    def test_table_is_added_once_before_references(self):
        rendered, result = render_table("# Results\n\n## References\n\n[1] source\n", self.evidence)
        self.assertEqual(result["action"], "inserted_before_bibliography")
        self.assertEqual(result["row_count"], 1)
        self.assertEqual(rendered.count("### 단계별 조건·수율 통합표"), 1)
        self.assertLess(rendered.index("### 단계별 조건·수율 통합표"), rendered.index("## References"))

    def test_authored_route_step_table_is_never_overwritten(self):
        authored = "## Results\n\n| route_id / step_id | yield (%) |\n|---|---|\n| route-x / step-01 | 12.345 |\n\n## References\n"
        with self.assertRaisesRegex(ValueError, "Refusing to replace"):
            render_table(authored, self.evidence)


if __name__ == "__main__":
    unittest.main()
