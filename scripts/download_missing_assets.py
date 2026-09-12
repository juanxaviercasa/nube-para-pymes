import urllib.request
from pathlib import Path

images_to_download = [
    "/wp-content/uploads/2026/07/logo-nubeparapymes-header-150x150.webp",
    "/wp-content/uploads/2026/08/app-01-1.webp",
    "/wp-content/uploads/2026/08/app-02.webp",
    "/wp-content/uploads/2026/08/app-03.webp",
    "/wp-content/uploads/2026/08/app-04.webp",
    "/wp-content/uploads/2026/08/app-05.webp",
    "/wp-content/uploads/2026/08/app-07.webp",
    "/wp-content/uploads/2026/08/app-08.webp",
    "/wp-content/uploads/2026/08/img-01.webp",
    "/wp-content/uploads/2026/08/img-02.webp",
    "/wp-content/uploads/2026/08/img-03.webp",
    "/wp-content/uploads/2026/08/img-04.webp",
    "/wp-content/uploads/2026/08/img-05.webp",
]

base_url = "https://dev-nube-para-pymes.pantheonsite.io"
root_export = Path(r"c:\Users\pc\Music\nube-para-pymes\nubepymesexport")

for rel in images_to_download:
    remote_url = base_url + rel
    local_path = root_export / rel.lstrip("/").replace("/", "\\")
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    req = urllib.request.Request(remote_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            local_path.write_bytes(data)
            print(f"Downloaded {rel} ({len(data)} bytes)")
    except Exception as e:
        print(f"FAILED {rel}: {e}")

print("Done downloading missing assets.")
