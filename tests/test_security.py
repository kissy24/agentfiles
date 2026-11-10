"""Regression tests for unsafe documentation execution and path handling."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "awf_verify", Path(__file__).resolve().parents[1] / "scripts/verify.py")
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)
SECRET_SPEC = importlib.util.spec_from_file_location(
    "awf_secret_check", Path(__file__).resolve().parents[1] / "scripts/check_secrets.py")
secret_check = importlib.util.module_from_spec(SECRET_SPEC)
SECRET_SPEC.loader.exec_module(secret_check)


class SecurityTests(unittest.TestCase):
    def test_scanner_finds_synthetic_tokens_without_returning_values(self):
        token = "gh" + "p_" + "A" * 36
        matches = list(secret_check.findings("example\n" + token))
        self.assertEqual(matches, [("github-token", 2)])
        self.assertNotIn(token, str(matches))

    def test_scanner_finds_private_key_header(self):
        header = "-----BEGIN " + "PRIVATE KEY-----"
        self.assertIn(("private-key", 1), list(secret_check.findings(header)))

    def test_modified_readme_command_is_rejected(self):
        body = verify.read(verify.ROOT / "adapters/codex/README.md")
        malicious = body.replace("  set -euC", "  touch injected\n  set -euC")
        with patch.object(verify, "read", return_value=malicious):
            with self.assertRaisesRegex(ValueError, "not approved"):
                verify.install_command()

    def test_unapproved_command_never_starts_process(self):
        with patch.object(verify.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "unapproved"):
                verify.run_install(verify.APPROVED_INSTALL + "\ntouch injected", Path("."))
            run.assert_not_called()

    def test_source_symlink_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "templates").mkdir()
            (source / "templates/AGENTS.md").write_text("entry")
            external = root / "private"
            external.mkdir()
            (external / "contract.md").write_text("must not copy")
            (external / "lifecycle.md").write_text("must not copy")
            (source / "core").symlink_to(external, target_is_directory=True)
            target = root / "target"
            target.mkdir()
            with patch.object(verify, "ROOT", source):
                result = verify.run_install(verify.APPROVED_INSTALL, target)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(target.iterdir()), [])

    def test_parent_traversal_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scope = root / "project"
            scope.mkdir()
            (root / "outside.md").write_text("private")
            document = scope / "README.md"
            document.write_text("[outside](../outside.md)")
            with self.assertRaisesRegex(ValueError, "outside allowed"):
                verify.check_links(document, base=scope)

    def test_symlink_link_outside_scope_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scope = root / "project"
            scope.mkdir()
            private = root / "outside.md"
            private.write_text("private")
            (scope / "linked.md").symlink_to(private)
            document = scope / "README.md"
            document.write_text("[outside](linked.md)")
            with self.assertRaisesRegex(ValueError, "outside allowed"):
                verify.check_links(document, base=scope)


if __name__ == "__main__":
    unittest.main()
