"""No-Computer-Use graph authoring tests. Run: python -m unittest discover -s scripts -p 'test_*.py'."""
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from generate_drawio import SpecError, make_drawio, main


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.spec = {
            "title": "Thai diagram",
            "page": {"width": 500, "height": 280, "background": "#FFFFFF"},
            "nodes": [
                {"id": "first", "x": 20, "y": 30, "width": 150, "height": 100,
                 "label": "ทดสอบ <หนึ่ง>\nคำใหม่"},
                {"id": "second", "x": 300, "y": 30, "width": 150, "height": 100,
                 "label": "สอง"},
            ],
            "edges": [
                {"id": "edge1", "source": "first", "target": "second",
                 "exit": [1, 0.5], "entry": [0, 0.5]}
            ],
        }
        self.src = self.folder / "diagram.json"
        self.src.write_text(json.dumps(self.spec), encoding="utf-8")

    def test_editable_cells_thai_and_anchors(self):
        xml, report = make_drawio(self.spec, self.src)
        model = ET.fromstring(xml).find("diagram/mxGraphModel")
        self.assertEqual(model.get("background"), "#FFFFFF")
        cells = {c.get("id"): c for c in model.iter("mxCell") if c.get("id")}
        self.assertEqual(cells["first"].get("value"), "ทดสอบ &lt;หนึ่ง&gt;<br/>คำใหม่")
        self.assertEqual(cells["edge1"].get("source"), "first")
        self.assertEqual(cells["edge1"].get("target"), "second")
        self.assertEqual(report["edges"], 1)

    def test_disallow_unknown_connector_target(self):
        self.spec["edges"][0]["target"] = "not-a-vertex"
        with self.assertRaises(SpecError):
            make_drawio(self.spec, self.src)

    def test_disallow_invalid_anchor(self):
        self.spec["edges"][0]["exit"] = [2, 0.5]
        with self.assertRaises(SpecError):
            make_drawio(self.spec, self.src)

    def test_cli_creates_source_and_refuses_overwrite(self):
        target = self.folder / "figure.drawio"
        trace = self.folder / "manifest.json"
        self.assertEqual(main([str(self.src), str(target), "--manifest", str(trace)]), 0)
        saved = target.read_bytes()
        self.assertEqual(main([str(self.src), str(target)]), 2)
        self.assertEqual(target.read_bytes(), saved)
        self.assertEqual(json.loads(trace.read_text())["status"], "SOURCE_GENERATED__NATIVE_EXPORT_AND_VISUAL_QA_PENDING")

    def test_embedded_png_without_external_url(self):
        p = self.folder / "leaf.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"placeholder")
        self.spec["nodes"] = [{"id": "leaf", "kind": "image", "path": "leaf.png",
                               "x": 10, "y": 20, "width": 80, "height": 100}]
        self.spec["edges"] = []
        xml, report = make_drawio(self.spec, self.src)
        self.assertIn(b"image=data:image/png,", xml)
        self.assertNotIn(str(p).encode(), xml)
        self.assertEqual(len(report["embedded_assets"]), 1)


if __name__ == "__main__":
    unittest.main()
