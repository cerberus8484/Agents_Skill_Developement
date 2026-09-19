"""Audit Nexora agent permissions and generated adapter configuration offline."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POLICY = ROOT / "standards" / "agent-shield-policy.json"
DEFAULT_MANIFEST = ROOT / "framework" / "agents" / "team.json"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _frontmatter_value(path: Path, key: str) -> Any:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"Unterminated frontmatter: {path}")
    prefix = f"{key}: "
    for line in text[4:end].splitlines():
        if line.startswith(prefix):
            return json.loads(line[len(prefix):])
    raise ValueError(f"Missing {key!r} in {path}")


def audit(root: Path = ROOT, policy_path: Path | None = None) -> dict[str, Any]:
    policy_path = policy_path or root / "standards" / "agent-shield-policy.json"
    manifest_path = root / "framework" / "agents" / "team.json"
    policy = load_json(policy_path)
    manifest = load_json(manifest_path)
    violations: list[str] = []
    warnings: list[str] = []
    checks = 0

    if not isinstance(manifest, list):
        raise ValueError("Agent manifest must be a JSON array")

    known_tools = set(policy["known_tools"])
    policy_agents = policy["agents"]
    manifest_by_id = {entry["id"]: entry for entry in manifest}

    if set(manifest_by_id) != set(policy_agents):
        missing_policy = sorted(set(manifest_by_id) - set(policy_agents))
        missing_manifest = sorted(set(policy_agents) - set(manifest_by_id))
        if missing_policy:
            violations.append(f"Agents without shield policy: {missing_policy}")
        if missing_manifest:
            violations.append(f"Shield policy references missing agents: {missing_manifest}")
    checks += 1

    contract_path = root / "framework" / "agents" / "team-contract.md"
    contract = contract_path.read_text(encoding="utf-8")
    for clause in policy["required_contract_clauses"]:
        checks += 1
        if clause not in contract:
            violations.append(f"Shared contract missing required clause: {clause}")

    claude_map = policy["platform_tool_map"]["claude"]
    for agent_id, profile in manifest_by_id.items():
        actual = profile.get("tools", [])
        expected = policy_agents.get(agent_id, {}).get("allowed_tools", [])
        checks += 1

        unknown = sorted(set(actual) - known_tools)
        if unknown:
            violations.append(f"{agent_id}: unknown tools {unknown}")
        if actual != expected:
            violations.append(
                f"{agent_id}: manifest tools {actual} do not match shield policy {expected}"
            )

        copilot_path = root / ".github" / "agents" / f"{agent_id}.agent.md"
        checks += 1
        try:
            copilot_tools = _frontmatter_value(copilot_path, "tools")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            violations.append(f"{agent_id}: unreadable Copilot adapter: {error}")
        else:
            if copilot_tools != expected:
                violations.append(
                    f"{agent_id}: Copilot tools {copilot_tools} do not match policy {expected}"
                )

        claude_path = root / ".claude" / "agents" / f"{agent_id}.md"
        expected_claude = [
            platform_tool
            for tool in expected
            for platform_tool in claude_map[tool]
        ]
        checks += 1
        try:
            claude_tools = _frontmatter_value(claude_path, "tools")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            violations.append(f"{agent_id}: unreadable Claude adapter: {error}")
        else:
            if claude_tools != expected_claude:
                violations.append(
                    f"{agent_id}: Claude tools {claude_tools} do not match policy "
                    f"{expected_claude}"
                )

        codex_path = root / ".codex" / "agents" / f"{agent_id}.toml"
        checks += 1
        try:
            codex = tomllib.loads(codex_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as error:
            violations.append(f"{agent_id}: unreadable Codex adapter: {error}")
        else:
            if codex.get("name") != agent_id:
                violations.append(f"{agent_id}: Codex adapter identity mismatch")
            instructions = codex.get("developer_instructions", "")
            for clause in policy["required_contract_clauses"]:
                if clause not in instructions:
                    violations.append(
                        f"{agent_id}: Codex adapter missing contract clause: {clause}"
                    )
            warnings.append(
                f"{agent_id}: Codex host tool enforcement remains UNVERIFIED"
            )

    return {
        "product": "Nexora Agent Shield",
        "policy_version": policy["version"],
        "status": "PASS" if not violations else "FAIL",
        "checks": checks,
        "agents": len(manifest_by_id),
        "violations": violations,
        "warnings": warnings,
        "limitations": [
            "Static repository inspection only",
            "Does not observe runtime tool grants, network egress, or model-side data flow",
            "Codex adapter format has no repository-enforced per-agent tool allowlist",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit(args.root.resolve(), args.policy)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if report["status"] != "PASS":
        parser.exit(1, "Agent Shield failed.\n")


if __name__ == "__main__":
    main()
