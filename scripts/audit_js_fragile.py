import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / "js"

print("=== AUDITING JS FOR STRING-BASED LOGIC & TRANSLATION VULNERABILITIES ===")

fragile_patterns = [
    (r'(?:\.textContent|\.innerText)\s*(?:===|==|!==|!=)\s*["\']([^"\']+)["\']', "Direct textContent/innerText comparison"),
    (r'confirm\s*\(\s*["\']([^"\']+)["\']', "Hardcoded confirm() message"),
    (r'prompt\s*\(\s*[`"\']([^`"\']+)[`"\']', "Hardcoded prompt() message"),
    (r'alert\s*\(\s*["\']([^"\']+)["\']', "Hardcoded alert() message"),
    (r'Intl\.NumberFormat\s*\(\s*["\']es-PE["\']', "Hardcoded es-PE NumberFormat"),
    (r'Intl\.DateTimeFormat\s*\(\s*["\']es-PE["\']', "Hardcoded es-PE DateTimeFormat"),
    (r'===\s*["\'](?:Pendiente|En curso|Bloqueada|Terminada|Ganado|Perdido|Prospecto|Calificado|Propuesta|Alta|Media|Baja|Ventas|Servicios|Compras|Personal|Impuestos|Operación|Financiamiento|Otros)["\']', "Hardcoded Spanish business status check"),
    (r'includes\s*\(\s*["\'](?:Ganado|Perdido|Terminada)["\']\)', "Hardcoded Spanish status list membership"),
]

findings = {}

for js_file in sorted(JS_DIR.glob("*.js")):
    content = js_file.read_text(encoding="utf-8", errors="ignore")
    file_findings = []
    
    for regex, desc in fragile_patterns:
        matches = re.findall(regex, content)
        if matches:
            file_findings.append((desc, matches[:5]))
            
    if file_findings:
        findings[js_file.name] = file_findings

for fname, issues in findings.items():
    print(f"\nFile: {fname}")
    for desc, m in issues:
        print(f"  - [{desc}]: {m}")
