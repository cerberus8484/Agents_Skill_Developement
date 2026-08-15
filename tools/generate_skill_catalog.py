"""Generate the local Agent & Skill Framework runtime skill catalog."""

from __future__ import annotations

import html
import re
from collections import Counter
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPOSITORY_ROOT / "docs" / "skills-runtime-catalog.html"
SKILL_ROOTS = (
    (Path.home() / ".agents" / "skills", "User skills"),
    (Path.home() / ".codex" / "skills", "Codex skills"),
    (Path.home() / ".codex" / "plugins" / "cache", "Plugin and bundled skills"),
    (REPOSITORY_ROOT / ".github" / "skills", "Project skills"),
)


def read_metadata(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8", errors="replace")
    frontmatter = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter:
        return path.parent.name, "No frontmatter description available."

    metadata = frontmatter.group(1)
    name = re.search(r"^name:\s*([^\n]+)", metadata, re.MULTILINE)
    description = re.search(r"^description:\s*>?\s*(.*?)(?=\n\w[\w-]*:|\Z)", metadata, re.DOTALL | re.MULTILINE)
    resolved_name = name.group(1).strip().strip('"\'') if name else path.parent.name
    resolved_description = re.sub(r"\s+", " ", description.group(1)).strip().strip('"\'') if description else "No frontmatter description available."
    return resolved_name, resolved_description


def classify(name: str, source: str) -> str:
    text = f"{name} {source}".lower()
    if any(word in text for word in ("security", "privacy", "dsgvo", "compliance", "secret")):
        return "Security & Privacy"
    if any(word in text for word in ("test", "tdd", "verification", "eval", "build", "resolver")):
        return "Testing & Build"
    if any(word in text for word in ("network", "cisco", "bgp", "homelab")):
        return "Networking"
    if any(word in text for word in ("agent", "llm", "prompt", "harness", "model", "ai-")):
        return "AI & Agent Runtime"
    if any(word in text for word in ("doc", "pdf", "pptx", "xlsx", "presentation", "article")):
        return "Documentation & Content"
    if any(word in text for word in ("react", "frontend", "ui", "angular", "flutter", "swiftui", "android")):
        return "Frontend & Mobile"
    if any(word in text for word in ("database", "postgres", "mysql", "prisma", "clickhouse")):
        return "Data & Database"
    if any(word in text for word in ("docker", "deploy", "cloud", "github", "devops")):
        return "DevOps & Platform"
    if "Project skills" in source:
        return "SOC / SIEM"
    return "Engineering & Operations"


def collect_skills() -> list[dict[str, str]]:
    seen: set[Path] = set()
    skills: list[dict[str, str]] = []
    for root, source in SKILL_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("SKILL.md"):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            name, description = read_metadata(path)
            skills.append({
                "name": name,
                "description": description,
                "source": source,
                "category": classify(name, source),
                "location": str(path.parent),
            })
    return sorted(skills, key=lambda item: (item["category"], item["name"].lower(), item["location"]))


def render(skills: list[dict[str, str]]) -> str:
    categories = Counter(skill["category"] for skill in skills)
    rows = "\n".join(
        "<article class=\"skill\" data-search=\"{search}\">"
        "<h3>{name}</h3><p>{description}</p><div class=\"meta\">"
        "<span>{category}</span><span>{source}</span></div>"
        "<details><summary>Lokaler Bestand</summary><code>{location}</code></details></article>".format(
            search=html.escape(" ".join(skill.values()).lower(), quote=True),
            name=html.escape(skill["name"]),
            description=html.escape(skill["description"]),
            category=html.escape(skill["category"]),
            source=html.escape(skill["source"]),
            location=html.escape(skill["location"]),
        )
        for skill in skills
    )
    category_summary = "".join(f"<li><strong>{html.escape(name)}</strong>: {count}</li>" for name, count in sorted(categories.items()))
    return f"""<!doctype html>
<html lang=\"de\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Agent &amp; Skill Framework – Laufzeit-Skillkatalog</title>
<style>
:root{{--bg:#0b1220;--card:#131d2d;--text:#e8eef8;--muted:#aab8cc;--accent:#66d4ff;--line:#29405d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,sans-serif}}main{{max-width:1200px;margin:auto;padding:42px 24px 80px}}h1,h2,h3{{line-height:1.2}}.lead,summary{{color:var(--muted)}}input{{width:100%;padding:13px 15px;border:1px solid var(--line);border-radius:8px;background:#09101c;color:var(--text);font:inherit}}.summary{{display:flex;gap:24px;flex-wrap:wrap;margin:20px 0}}.summary ul{{margin:0;padding-left:20px;color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}}.skill{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}}.skill h3{{margin:0;font-family:ui-monospace,monospace;color:var(--accent);word-break:break-word}}.skill p{{margin:9px 0;color:var(--muted);font-size:.91rem}}.meta{{display:flex;flex-wrap:wrap;gap:6px}}.meta span{{border:1px solid var(--line);border-radius:999px;padding:2px 8px;font-size:.75rem}}details{{margin-top:10px;font-size:.78rem}}code{{display:block;overflow-wrap:anywhere;color:var(--muted);padding-top:5px}}a{{color:var(--accent)}}.hidden{{display:none}}
</style></head><body><main>
<p><a href=\"index.html\">← Agent &amp; Skill Framework</a></p><h1>Laufzeit-Skillkatalog</h1>
<p class=\"lead\">Automatisch aus den im lokalen Setup installierten <code>SKILL.md</code>-Dateien erzeugt. Diese Seite ist ein Inventar, keine Aussage über automatische Aktivierung, Sicherheitseinstufung oder Produktionsfreigabe.</p>
<div class=\"summary\"><strong>{len(skills)} Skill-Dateien</strong><ul>{category_summary}</ul></div>
<label>Suche nach Name, Kategorie, Quelle oder Beschreibung<input id=\"q\" type=\"search\" placeholder=\"z. B. security, qradar, python, docker\"></label>
<div class=\"grid\" id=\"catalog\">{rows}</div>
</main><script>const q=document.querySelector('#q');q.addEventListener('input',()=>{{const term=q.value.toLowerCase();document.querySelectorAll('.skill').forEach(card=>card.classList.toggle('hidden',!card.dataset.search.includes(term)))}});</script></body></html>"""


if __name__ == "__main__":
    OUTPUT.write_text(render(collect_skills()), encoding="utf-8")
    print(OUTPUT)
