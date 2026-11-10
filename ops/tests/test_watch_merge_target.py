"""Unit tests for the merge target of scripts/watch.py save_intent (scan finding #1, CWE-22, ops/scan/baseline.json).

Run: python3 -m unittest discover -s ops/tests
The model chooses `into`; the watch job must append only to a file directly inside intent/auto/. Each test runs against a
temporary copy of the layout (ROOT and AUTO are patched), so a failing run never writes to the real repo.
"""
import sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import watch  # noqa: E402

DET = {"day": 40, "date": "2026-11-10", "metric": "ci_failure_rate"}


class MergeTarget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.auto = self.root / "intent" / "auto"
        self.auto.mkdir(parents=True)
        self.claude = self.root / "CLAUDE.md"
        self.claude.write_text("# rules\n")
        self.open = self.auto / "2026-11-09-ci.md"
        self.open.write_text("# open intent\n")
        self.saved = (watch.ROOT, watch.AUTO)
        watch.ROOT, watch.AUTO = self.root, self.auto

    def tearDown(self):
        watch.ROOT, watch.AUTO = self.saved
        self.tmp.cleanup()

    def save(self, into):
        return watch.save_intent(f'{{"action": "merge", "into": "{into}"}}\nINJECTED LINE\n', DET, 2)

    def test_dotdot_out_of_intent_auto_is_refused(self):
        f, how = self.save("intent/auto/../../CLAUDE.md")
        self.assertEqual(self.claude.read_text(), "# rules\n")
        self.assertEqual(how, "new")
        self.assertEqual(f.parent, self.auto)

    def test_subfolder_of_intent_auto_is_refused(self):
        (self.auto / "sub").mkdir()
        (self.auto / "sub" / "x.md").write_text("x\n")
        f, how = self.save("intent/auto/sub/x.md")
        self.assertEqual((self.auto / "sub" / "x.md").read_text(), "x\n")
        self.assertEqual(how, "new")

    def test_open_intent_directly_inside_is_merged(self):
        f, how = self.save("intent/auto/2026-11-09-ci.md")
        self.assertEqual(how, "merge")
        self.assertEqual(f.resolve(), self.open.resolve())
        self.assertIn("INJECTED LINE", self.open.read_text())


if __name__ == "__main__":
    unittest.main()
