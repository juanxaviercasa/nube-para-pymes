"""
Strip all floating language switcher asides and lingering geo-lang-detect script tags
from all HTML files in en/ and dist/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def strip_unwanted_elements():
    count_aside = 0
    count_script = 0

    aside_pattern = re.compile(r'<aside[^>]*class=["\']np-lang-switch-floating["\'][^>]*>[\s\S]*?</aside>', re.IGNORECASE)
    script_pattern = re.compile(r'<script[^>]*src=["\'][^"\']*geo-lang-detect[^"\']*["\'][^>]*></script>', re.IGNORECASE)

    target_dirs = [ROOT / "en"]

    for tdir in target_dirs:
        if not tdir.exists():
            continue
        for html_path in tdir.rglob("*.html"):
            try:
                content = html_path.read_text(encoding="utf-8", errors="ignore")
                modified = False

                if aside_pattern.search(content):
                    content = aside_pattern.sub("", content)
                    modified = True
                    count_aside += 1

                if script_pattern.search(content):
                    content = script_pattern.sub("", content)
                    modified = True
                    count_script += 1

                if modified:
                    html_path.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"Error processing {html_path}: {e}")

    print(f"Cleaned {count_aside} floating asides and {count_script} geo-lang script tags from en/.")

if __name__ == "__main__":
    strip_unwanted_elements()
