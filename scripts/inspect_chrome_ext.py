from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
lines = (ROOT / "calculadora-descuentos-promociones.html").read_text(encoding="utf-8", errors="ignore").splitlines()
for idx, l in enumerate(lines, 1):
    if "chrome-extension" in l:
        print(f"{idx}: {l.strip()[:100]}")
