"""Rebuild works.js from whatever is in graphics/ and motion/.

Run from anywhere:  python3 ~/Desktop/SUNS-ARTCHIVE/update.py
Order: numbered files first (01-..., 02-...), then everything else newest
first, then files starting with "z-" last (use that to push pieces down).
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
KINDS = {
    "graphics": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"},
    "motion": {".mp4", ".webm", ".mov", ".m4v"},
}


def collect(kind, exts):
    files = [p for p in (ROOT / kind).iterdir() if p.is_file() and p.suffix.lower() in exts]
    numbered = sorted([p for p in files if p.name[:2].isdigit()], key=lambda p: p.name)
    last = sorted([p for p in files if p.name.startswith("z-")], key=lambda p: p.name)
    rest = sorted(
        [p for p in files if not p.name[:2].isdigit() and not p.name.startswith("z-")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    # ?v=<modified time> makes browsers refetch a file whenever it changes.
    return [f"{kind}/{quote(p.name)}?v={int(p.stat().st_mtime)}" for p in numbered + rest + last]


works = {kind: collect(kind, exts) for kind, exts in KINDS.items()}
(ROOT / "works.js").write_text("window.WORKS = " + json.dumps(works, indent=2) + ";\n")

# Bump the works.js / app.js / styles.css version in index.html so browsers
# pick up the new list instead of a cached one.
index = ROOT / "index.html"
stamp = str(int(time.time()))
index.write_text(re.sub(r"(works\.js|app\.js|styles\.css)\?v=\w+", rf"\1?v={stamp}", index.read_text()))
print(f"{len(works['graphics'])} graphics, {len(works['motion'])} motion videos")
