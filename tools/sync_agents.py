"""Render the eight team profiles; never install globally or contact a service."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CLAUDE_TOOLS = {
    "read": ["Read"],
    "search": ["Grep", "Glob"],
    "edit": ["Edit", "Write"],
    "execute": ["Bash"],
    "agent": ["Agent"],
}


def render_all():
    """Return deterministic repository-relative outputs without writing."""
    source = ROOT / "framework" / "agents"
    profiles = json.loads((source / "team.json").read_text(encoding="utf-8"))
    shared = (source / "team-contract.md").read_text(encoding="utf-8")
    outputs = {}
    for profile in profiles:
        name = profile["id"]
        if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
            raise ValueError(f"Invalid agent ID: {name!r}")
        body = shared + "\n" + (source / f"{name}.md").read_text(encoding="utf-8")
        description = json.dumps(profile["description"], ensure_ascii=False)
        copilot = (
            "---\n"
            f"name: {json.dumps(profile['name'])}\n"
            f"description: {description}\n"
            f"tools: {json.dumps(profile['tools'])}\n"
            "user-invocable: true\ndisable-model-invocation: false\n---\n\n"
            + body
        )
        claude_tools = [tool for alias in profile["tools"] for tool in CLAUDE_TOOLS[alias]]
        claude = (
            f"---\nname: {name}\ndescription: {description}\n"
            f"tools: {json.dumps(claude_tools)}\n---\n\n" + body
        )
        # JSON quoted strings are valid TOML basic strings for this content.
        # Do not invent unsupported per-agent tool filters for the Codex host.
        codex = (
            f'name = "{name}"\ndescription = {description}\n'
            f"developer_instructions = {json.dumps(body, ensure_ascii=False)}\n"
        )
        for path, content in (
            (Path(".github/agents") / f"{name}.agent.md", copilot),
            (Path(".claude/agents") / f"{name}.md", claude),
            (Path(".codex/agents") / f"{name}.toml", codex),
        ):
            if path in outputs:
                raise ValueError(f"Duplicate agent output: {path}")
            outputs[path] = content
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Detect drift without writes.")
    args = parser.parse_args()
    outputs = render_all()
    drift = []
    for relative, content in outputs.items():
        path = ROOT / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            drift.append(str(relative))
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
    if args.check and drift:
        parser.exit(1, "Adapter drift:\n" + "\n".join(drift) + "\n")
    print(f"{len(outputs)} adapters checked; {len(drift)} differences"
          + ("" if args.check else " synchronized") + ".")


if __name__ == "__main__":
    main()
