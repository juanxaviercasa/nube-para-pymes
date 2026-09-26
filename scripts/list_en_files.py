from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
files = sorted([f.name for f in (ROOT / "en").glob("*.html")])
for f in files:
    print(f)
