import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_skill_usage.py"
SPEC = importlib.util.spec_from_file_location("audit_skill_usage", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


class AuditSkillUsageTest(unittest.TestCase):
    def test_excludes_injected_catalog_and_counts_codex_load(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_jsonl(
                root / "catalog.jsonl",
                [{"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [{"type": "input_text", "text": "deep-mode catalog"}]}}],
            )
            write_jsonl(
                root / "load.jsonl",
                [{"type": "response_item", "payload": {"type": "function_call", "name": "exec_command", "arguments": "sed -n 1,200p /tmp/skills/deep-mode/SKILL.md"}}],
            )

            result = MODULE.audit(root, 30, ["deep-mode"])["deep-mode"]

            self.assertEqual({"loads": 1, "mentions": 1}, result)

    def test_counts_claude_read_and_assistant_mention_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_jsonl(root / "user.jsonl", [{"type": "user", "message": {"content": "ponytail catalog"}}])
            write_jsonl(
                root / "assistant.jsonl",
                [{"type": "assistant", "message": {"content": [
                    {"type": "text", "text": "Using ponytail."},
                    {"type": "tool_use", "name": "Read", "input": {"file_path": "/tmp/ponytail/SKILL.md"}},
                ]}}],
            )

            result = MODULE.audit(root, 30, ["ponytail"])["ponytail"]

            self.assertEqual({"loads": 1, "mentions": 1}, result)


if __name__ == "__main__":
    unittest.main()
