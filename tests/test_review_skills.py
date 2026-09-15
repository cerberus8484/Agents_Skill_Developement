"""Package integrity checks, not proof of reviewer behavior or compliance."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
NEW_SKILLS = (
    "code-review-workflow", "test-review",
    "nis2-technical-review", "iso27001-control-review",
)


class ReviewSkillPackages(unittest.TestCase):
    def test_packages_and_references_are_identical_on_all_platforms(self):
        for name in NEW_SKILLS:
            source = ROOT / "framework/skills" / name
            expected = {p.relative_to(source): p.read_bytes()
                        for p in source.rglob("*") if p.is_file()}
            for host in (".github", ".agents", ".claude"):
                target = ROOT / host / "skills" / name
                actual = {p.relative_to(target): p.read_bytes()
                          for p in target.rglob("*") if p.is_file()}
                self.assertEqual(expected, actual, (name, host))
            body = (source / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(body.startswith(f"---\nname: {name}\n"))
            for reference in re.findall(r"references/[a-z-]+\.md", body):
                self.assertTrue((source / reference).is_file(), reference)
            self.assertNotIn("allowed-tools:", body.split("---", 2)[1])

    def test_reviewer_mapping_and_permissions(self):
        profiles = json.loads((ROOT / "framework/agents/team.json").read_text())
        reviewer = next(p for p in profiles if p["id"] == "code-security-reviewer")
        self.assertEqual(set(NEW_SKILLS) | {"clean-code", "security", "dsgvo"},
                         set(reviewer["skills"]))
        self.assertEqual(["read", "search"], reviewer["tools"])


if __name__ == "__main__":
    unittest.main()
