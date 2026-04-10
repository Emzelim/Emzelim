import re
import urllib.request
import json
from pathlib import Path

PROJECTS_URL = "https://emzelim.com/projects.json"
README_PATH = Path(__file__).parent.parent / "README.md"
START_MARKER = "<!-- PROJECTS_START -->"
END_MARKER = "<!-- PROJECTS_END -->"


def fetch_projects():
    req = urllib.request.Request(
        PROJECTS_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; readme-sync/1.0)"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def build_table(projects):
    lines = [
        "| Project | Description | Stack |",
        "|---------|-------------|-------|",
    ]
    for p in projects:
        name = p["name"]
        url = p["url"]
        description = p["description"]
        stack = ", ".join(p["stack"])
        lines.append(f"| **[{name}]({url})** | {description} | {stack} |")
    return "\n".join(lines)


def update_readme(table):
    content = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"({re.escape(START_MARKER)}\n).*?(\n{re.escape(END_MARKER)})",
        re.DOTALL,
    )
    new_content = pattern.sub(rf"\g<1>{table}\g<2>", content)
    if new_content == content:
        print("No changes.")
        return False
    README_PATH.write_text(new_content, encoding="utf-8")
    print("README updated.")
    return True


if __name__ == "__main__":
    projects = fetch_projects()
    table = build_table(projects)
    update_readme(table)
