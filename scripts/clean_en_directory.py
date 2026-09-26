from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

OBSOLETE = [
    "ad-campaign-comparator.html",
    "basic-seo-auditor.html",
    "cloud-vs-onprem-tco.html",
    "inventory-purchase-orders.html",
    "labor-cost-calculator.html",
    "password-generator.html",
    "return-refund-policy-generator.html",
    "service-contract-generator.html",
    "task-project-tracker.html",
    "utm-campaign-console.html"
]

for name in OBSOLETE:
    p = EN_DIR / name
    if p.exists():
        p.unlink()
        print(f"Removed obsolete file: {name}")

files = list(EN_DIR.glob("*.html"))
print(f"Total clean HTML files in en/: {len(files)}")
