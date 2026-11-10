import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from scripts.validate_handoff import main, redact, render_markdown, validate_text


FIXTURES = Path(__file__).parent / "fixtures"


class HandoffContractTests(unittest.TestCase):
    def test_valid_contract_passes(self):
        result = validate_text((FIXTURES / "valid.md").read_text())
        self.assertTrue(result.valid, result.errors)

    def test_missing_section_fails(self):
        result = validate_text((FIXTURES / "missing-section.md").read_text())
        self.assertIn("Risks", " ".join(result.errors))

    def test_secret_fails(self):
        result = validate_text((FIXTURES / "secret.md").read_text())
        self.assertIn("segredo", " ".join(result.errors).lower())

    def test_placeholder_fails(self):
        result = validate_text((FIXTURES / "placeholder.md").read_text())
        self.assertIn("placeholder", " ".join(result.errors).lower())

    def test_vague_next_action_fails(self):
        result = validate_text((FIXTURES / "vague-next.md").read_text())
        self.assertIn("Next action", " ".join(result.errors))

    def test_oversized_fails(self):
        text = (FIXTURES / "valid.md").read_text() + ("x" * 6000)
        self.assertIn("6.000", " ".join(validate_text(text).errors))

    def test_jwt_and_local_path_are_flagged(self):
        base = (FIXTURES / "valid.md").read_text()
        jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature"
        result = validate_text(base.replace("Credenciais sandbox", jwt + " /Users/alice/private Credenciais"))
        self.assertFalse(result.valid)

    def test_redact_hides_sensitive_values(self):
        cleaned = redact("TOKEN=abc /Users/alice/file eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.signature")
        self.assertNotIn("abc", cleaned)
        self.assertNotIn("/Users", cleaned)
        self.assertNotIn("eyJ", cleaned)

    def test_markdown_lists_errors(self):
        output = render_markdown(validate_text((FIXTURES / "missing-section.md").read_text()))
        self.assertIn("INVALID", output)
        self.assertIn("Risks", output)

    def test_cli_json_round_trip_and_exit_codes(self):
        output = StringIO()
        with redirect_stdout(output):
            valid_code = main([str(FIXTURES / "valid.md"), "--format", "json"])
        self.assertEqual(0, valid_code)
        self.assertTrue(json.loads(output.getvalue())["valid"])
        with redirect_stdout(StringIO()):
            invalid_code = main([str(FIXTURES / "secret.md")])
        self.assertEqual(1, invalid_code)

    def test_evidence_without_command_warns(self):
        text = (FIXTURES / "valid.md").read_text().replace(
            "`python3 -m unittest tests.test_payment -v` falha na asserção de status em `tests/test_payment.py`.",
            "O teste falha na asserção de status.",
        )
        self.assertTrue(validate_text(text).warnings)

    def test_integration_handoff_requires_refs_order_and_authorization(self):
        base = (FIXTURES / "valid.md").read_text()
        result = validate_text(base, integration=True)
        self.assertFalse(result.valid)
        self.assertIn("Source ref", " ".join(result.errors))

        complete = base.replace(
            "## Evidence\n",
            "## Evidence\nSource ref: `feature/a@abc123`\nTarget ref: `develop@def456`\n",
        ).replace(
            "## Decisions\n",
            "## Decisions\nIntegration order: parser -> endpoint -> screen\n",
        ).replace(
            "## Boundaries\n",
            "## Boundaries\nMerge authorization: not granted\n",
        )
        self.assertTrue(validate_text(complete, integration=True).valid)


if __name__ == "__main__":
    unittest.main()
