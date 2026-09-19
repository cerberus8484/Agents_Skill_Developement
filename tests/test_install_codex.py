"""Regression tests for the user-scoped Codex installer."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import install_codex


class CodexInstallerTests(unittest.TestCase):
    def test_install_replaces_owned_packages_and_preserves_unrelated_content(self):
        with TemporaryDirectory() as directory:
            home = Path(directory)
            legacy = home / ".agents" / "skills" / "soc-forensic-hunts" / "legacy-reference.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("stale", encoding="utf-8")
            unrelated = home / ".agents" / "skills" / "personal-skill" / "SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("personal", encoding="utf-8")

            result = install_codex.install(home)

            self.assertEqual("INSTALLED", result["status"])
            self.assertFalse(legacy.exists())
            self.assertEqual("personal", unrelated.read_text(encoding="utf-8"))
            self.assertTrue(
                (home / ".agents" / "skills" / "qradar-investigation" / "references" / "schemas" / "investigation.schema.json").is_file()
            )
            manifest = Path(result["backup"]) / "install-manifest.json"
            self.assertTrue(manifest.is_file())
            self.assertTrue(json.loads(manifest.read_text(encoding="utf-8"))["restart_required"])

    def test_dry_run_writes_nothing(self):
        with TemporaryDirectory() as directory:
            home = Path(directory)
            result = install_codex.install(home, dry_run=True)
            self.assertEqual("DRY_RUN", result["status"])
            self.assertFalse((home / ".agents").exists())
            self.assertFalse((home / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
