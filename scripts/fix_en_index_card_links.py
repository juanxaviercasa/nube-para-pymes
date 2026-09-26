from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
en_index = ROOT / "en" / "index.html"
text = en_index.read_text(encoding="utf-8")

SLUG_FIXES = {
    "./basic-seo-auditor.html": "./basic-on-page-seo-auditor.html",
    "./labor-cost-calculator.html": "./labor-cost-payroll-burden-calculator.html",
    "./ad-campaign-comparator.html": "./advanced-campaign-comparator.html",
    "./utm-campaign-console.html": "./campaign-utm-console.html",
    "./return-refund-policy-generator.html": "./return-policy-generator.html",
    "./cloud-vs-onprem-tco.html": "./cloud-vs-onprem-tco-simulator.html",
    "./password-generator.html": "./smb-password-generator.html",
    "./service-contract-generator.html": "./service-contracts-generator.html",
    "./inventory-purchase-orders.html": "./inventory-purchasing.html",
    "./task-project-tracker.html": "./tasks-projects-tracker.html"
}

for old, new in SLUG_FIXES.items():
    if old in text:
        text = text.replace(old, new)
        print(f"Replaced {old} with {new}")

en_index.write_text(text, encoding="utf-8")
print("en/index.html card links successfully updated!")
