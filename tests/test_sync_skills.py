"""Safety and drift tests for Nexora Skills adapter generation."""

import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tools import sync_skills


class SkillSyncTests(unittest.TestCase):
    def test_repository_adapters_match_canonical_sources(self):
        outputs = sync_skills.render_all()
        self.assertGreater(len(outputs), 0)
        self.assertEqual([], sync_skills.find_drift(outputs))

    def test_qradar_investigation_bundles_machine_readable_schemas(self):
        outputs = sync_skills.render_all()
        for adapter in (".github", ".agents", ".claude"):
            for schema in sync_skills.SCHEMA_BUNDLES["qradar-investigation"]:
                relative = Path(adapter) / "skills" / "qradar-investigation" / "references" / "schemas" / schema
                self.assertIn(relative, outputs)
                json.loads(outputs[relative].decode("utf-8"))

    def test_check_is_read_only_and_reports_drift(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "framework" / "skills" / "sample-skill"
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: Synthetic test.\n---\n",
                encoding="utf-8",
            )
            adapters = tuple(root / name / "skills" for name in (".github", ".agents", ".claude"))
            sentinel = root / "sentinel.txt"
            sentinel.write_text("preserve", encoding="utf-8")

            with patch.object(sync_skills, "ROOT", root), patch.object(
                sync_skills, "CANONICAL", root / "framework" / "skills"
            ), patch.object(sync_skills, "ADAPTERS", adapters), patch(
                "sys.argv", ["sync_skills.py", "--check"]
            ), redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as result:
                    sync_skills.main()
                self.assertEqual(1, result.exception.code)
                self.assertFalse((root / ".github").exists())
                self.assertEqual("preserve", sentinel.read_text(encoding="utf-8"))

    def test_default_sync_preserves_unexpected_files_and_prune_is_explicit(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "framework" / "skills" / "sample-skill"
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: Synthetic test.\n---\n",
                encoding="utf-8",
            )
            adapters = tuple(root / name / "skills" for name in (".github", ".agents", ".claude"))
            platform_specific = adapters[0] / "manual-skill" / "keep.txt"
            platform_specific.parent.mkdir(parents=True)
            platform_specific.write_text("keep", encoding="utf-8")
            unexpected = adapters[0] / "sample-skill" / "legacy.txt"
            unexpected.parent.mkdir(parents=True)
            unexpected.write_text("remove only when explicit", encoding="utf-8")

            with patch.object(sync_skills, "ROOT", root), patch.object(
                sync_skills, "CANONICAL", root / "framework" / "skills"
            ), patch.object(sync_skills, "ADAPTERS", adapters):
                outputs = sync_skills.render_all()
                sync_skills.write_outputs(outputs)
                self.assertTrue(platform_specific.is_file())
                self.assertTrue(unexpected.is_file())
                self.assertTrue(any(item.startswith("UNEXPECTED ") for item in sync_skills.find_drift(outputs)))
                sync_skills.prune_unexpected(outputs)
                self.assertFalse(unexpected.exists())
                self.assertTrue(platform_specific.is_file())
                self.assertEqual([], sync_skills.find_drift(outputs))

    def test_invalid_names_and_symlinks_fail_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_root = root / "framework" / "skills"
            invalid = canonical_root / "Invalid_Name"
            invalid.mkdir(parents=True)
            (invalid / "SKILL.md").write_text("---\nname: invalid\n---\n", encoding="utf-8")
            with patch.object(sync_skills, "CANONICAL", canonical_root):
                with self.assertRaisesRegex(ValueError, "Invalid skill name"):
                    sync_skills.discover_skills()


if __name__ == "__main__":
    unittest.main()
