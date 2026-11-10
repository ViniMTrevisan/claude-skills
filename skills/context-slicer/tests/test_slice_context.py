import unittest

from scripts.slice_context import slice_context


CANDIDATES = [
    {"path": "CLAUDE.md", "kind": "instruction", "reason": "repo rules", "required": True, "lines": 80},
    {"path": "src/service.ts", "kind": "target", "reason": "edit target", "score": 90, "lines": 180, "ranges": ["1-120"]},
    {"path": "src/service.spec.ts", "kind": "test", "reason": "focused proof", "score": 80, "lines": 140, "ranges": ["1-120"]},
    {"path": "src/generated.ts", "kind": "generated", "reason": "generated output", "score": 100, "lines": 500, "ranges": ["1-120"], "source": "schema.yml"},
    {"path": "src/unrelated.ts", "kind": "unrelated", "reason": "dirty workspace", "score": 100, "lines": 50},
]


class SliceContextTests(unittest.TestCase):
    def test_selects_required_and_high_signal_with_caps(self):
        result = slice_context({"candidates": CANDIDATES, "max_files": 3, "max_lines_per_file": 120})
        paths = [item["path"] for item in result["selected"]]
        self.assertEqual(paths, ["CLAUDE.md", "src/service.ts", "src/service.spec.ts"])
        self.assertTrue(all(item["included_lines"] <= 120 for item in result["selected"]))
        self.assertTrue(all(item["reason"] for item in result["selected"]))
        self.assertEqual(result["selected"][1]["ranges"], ["1-120"])

    def test_excludes_generated_and_unrelated_by_default(self):
        result = slice_context({"candidates": CANDIDATES})
        excluded = {item["path"]: item["disposition"] for item in result["deferred"]}
        self.assertEqual(excluded["src/generated.ts"], "source-first")
        self.assertEqual(excluded["src/unrelated.ts"], "out-of-scope")

    def test_rejects_required_items_over_budget(self):
        candidates = [
            {"path": "a", "kind": "target", "reason": "a", "required": True},
            {"path": "b", "kind": "target", "reason": "b", "required": True},
        ]
        with self.assertRaisesRegex(ValueError, "required"):
            slice_context({"candidates": candidates, "max_files": 1})

    def test_expansion_requires_reason_and_is_auditable(self):
        with self.assertRaisesRegex(ValueError, "reason"):
            slice_context({"candidates": CANDIDATES, "expand": [{"path": "src/generated.ts"}]})
        with self.assertRaisesRegex(ValueError, "expansion"):
            slice_context({"candidates": CANDIDATES, "max_files": 3, "expand": [{"path": "src/generated.ts", "reason": "runtime imports generated code"}]})
        result = slice_context({"candidates": CANDIDATES, "max_files": 6, "expand": [{"path": "src/generated.ts", "reason": "runtime imports generated code"}]})
        self.assertEqual(result["expansions"][0]["reason"], "runtime imports generated code")

    def test_rejects_ambiguous_truncation(self):
        candidate = {"path": "CLAUDE.md", "kind": "instruction", "reason": "rules", "required": True, "lines": 180}
        with self.assertRaisesRegex(ValueError, "ranges"):
            slice_context({"candidates": [candidate], "max_lines_per_file": 100})

    def test_rejects_expansion_of_unrelated_file(self):
        with self.assertRaisesRegex(ValueError, "unrelated"):
            slice_context({"candidates": CANDIDATES, "expand": [{"path": "src/unrelated.ts", "reason": "inspect dirty change"}]})


if __name__ == "__main__":
    unittest.main()
