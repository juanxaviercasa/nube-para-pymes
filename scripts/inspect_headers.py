from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Check root index.html header
root_index = ROOT / "index.html"
content = root_index.read_text(encoding="utf-8", errors="ignore")
header_match = re.search(r'<header.*?</header>', content, flags=re.DOTALL)
if header_match:
    print("=== ROOT index.html HEADER ===")
    print(header_match.group(0)[:500])
    print()

# Check en/index.html header
en_index = ROOT / "en" / "index.html"
en_content = en_index.read_text(encoding="utf-8", errors="ignore")
en_header_match = re.search(r'<header.*?</header>', en_content, flags=re.DOTALL)
if en_header_match:
    print("=== EN index.html HEADER ===")
    print(en_header_match.group(0)[:500])
    print()
