# GitHub Copilot adapter

Status: STRUCTURAL_ONLY.

GitHub Copilot discovers project skills in .github/skills/name/SKILL.md and supports resources and optional allowed-tools. This repository generates that adapter from the canonical source using tools/sync_skills.py.

Generated output is not the source of truth. allowed-tools is omitted for review-only skills unless a reviewed, necessary tool contract exists.

Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
