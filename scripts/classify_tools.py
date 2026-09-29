from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / "js"

tools_tech = {}
for f in sorted(JS_DIR.glob("*.js")):
    txt = f.read_text(encoding="utf-8", errors="ignore")
    is_react = "react" in txt.lower() or "createRoot" in txt or "createElement" in txt
    tools_tech[f.name] = "React" if is_react else "Vanilla/Other"

for k, v in tools_tech.items():
    print(f"{k:45} : {v}")
