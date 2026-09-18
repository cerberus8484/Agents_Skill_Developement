import hashlib
import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OVERLAY = ROOT / ".github" / "skills" / "ccd-wertesystem" / "SKILL.md"
DEFAULT_MANAGED_SKILL = (
    Path.home()
    / ".codex"
    / "plugins"
    / "cache"
    / "claude-cowork"
    / "anthropic-skills"
    / "1.0.0"
    / "skills"
    / "clean-code-developer"
)
MANAGED_SKILL_ROOT = Path(os.environ.get("CCD_MANAGED_SKILL_ROOT", DEFAULT_MANAGED_SKILL))
REVIEWED_SKILL_SHA256 = "e9e92b6ed073ad6c86dac95c793c41d1b66bffed09daa41b618a815596450007"


class CcdSkillContractTests(unittest.TestCase):
    def test_overlay_is_a_github_compatible_no_tool_framework_skill(self) -> None:
        content = OVERLAY.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: ccd-wertesystem\n"))
        self.assertIn("description:", content)
        self.assertNotIn("allowed-tools:", content)
        for required_term in (
            "FACT",
            "CCD MAPPING",
            "SMALLEST NEXT STEP",
            "OUT OF SCOPE",
            "untrusted data",
            "not a technical Local-Only",
        ):
            self.assertIn(required_term, content)

    @unittest.skipUnless(MANAGED_SKILL_ROOT.is_dir(), "reviewed external managed skill unavailable")
    def test_reviewed_managed_package_has_expected_surface_and_no_scripts(self) -> None:
        self.assertTrue(MANAGED_SKILL_ROOT.is_dir(), "Reviewed managed skill is unavailable")
        skill_file = MANAGED_SKILL_ROOT / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("name: clean-code-developer", content)
        self.assertNotIn("allowed-tools:", content)
        self.assertEqual(
            REVIEWED_SKILL_SHA256,
            hashlib.sha256(skill_file.read_bytes()).hexdigest(),
            "Managed skill changed; re-run the CCD provenance and contract review.",
        )
        expected_references = {
            "wertesystem.md",
            "grade-rot.md",
            "grade-orange.md",
            "grade-gelb.md",
            "grade-gruen.md",
            "grade-blau.md",
        }
        actual_references = {path.name for path in (MANAGED_SKILL_ROOT / "references").glob("*.md")}
        self.assertEqual(expected_references, actual_references)
        self.assertFalse((MANAGED_SKILL_ROOT / "scripts").exists())

    @unittest.skipUnless(MANAGED_SKILL_ROOT.is_dir(), "reviewed external managed skill unavailable")
    def test_managed_skill_covers_the_reviewed_values_and_grade_routing(self) -> None:
        content = (MANAGED_SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for required_term in (
            "Wandelbarkeit",
            "Korrektheit",
            "Produktionseffizienz",
            "Kontinuierliche Verbesserung",
            "references/wertesystem.md",
            "references/grade-rot.md",
            "references/grade-blau.md",
        ):
            self.assertIn(required_term, content)


if __name__ == "__main__":
    unittest.main()
