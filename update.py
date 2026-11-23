"""Rebuild works.js from whatever is in graphics/ and motion/.

Run from anywhere:  python3 ~/Desktop/SUNS-ARTCHIVE/update.py
Newest files show first. To pin an order, prefix names: 01-..., 02-...
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = {
    "graphics": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"},
    "motion": {".mp4", ".webm", ".mov", ".m4v"},
}


def collect(kind, exts):
    files = [p for p in (ROOT / kind).iterdir() if p.is_file() and p.suffix.lower() in exts]
    numbered = sorted([p for p in files if p.name[:2].isdigit()], key=lambda p: p.name)
    rest = sorted([p for p in files if not p.name[:2].isdigit()], key=lambda p: p.stat().st_mtime, reverse=True)
    return [f"{kind}/{p.name}" for p in numbered + rest]


works = {kind: collect(kind, exts) for kind, exts in KINDS.items()}
(ROOT / "works.js").write_text("window.WORKS = " + json.dumps(works, indent=2) + ";\n")
print(f"{len(works['graphics'])} graphics, {len(works['motion'])} motion videos")
