"""Download public research PDFs; publish only complete-looking PDF files.

Usage: python3 scripts/download_papers.py [paper_id ...]
Run scripts/extract_pdf afterwards for an independent parser check.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

def complete(path):
    if not path.exists():
        return False
    data = path.read_bytes()
    return data.startswith(b"%PDF-") and b"%%EOF" in data[-4096:]

def download(paper):
    dest = ROOT / "papers" / paper["file"]
    # Recover only a complete previous download.
    for suffix in (".part", ".retry"):
        candidate = Path(str(dest) + suffix)
        if not complete(dest) and complete(candidate):
            candidate.replace(dest)
    attempts = []
    if not complete(dest):
        for url in dict.fromkeys([paper["pdf_url"]] + paper.get("fallback_pdf_urls", [])):
            temp = Path(str(dest) + ".download")
            command = ["curl", "--location", "--fail", "--silent", "--show-error",
                       "--connect-timeout", "20", "--max-time", "600",
                       "--continue-at", "-", "--output", str(temp), url]
            result = subprocess.run(command, capture_output=True, text=True)
            attempts.append({"url": url, "exit_code": result.returncode,
                             "error": result.stderr.strip()[-1500:]})
            if result.returncode == 0 and complete(temp):
                temp.replace(dest)
                paper["downloaded_from"] = url
                break
    if complete(dest):
        data = dest.read_bytes()
        paper.update(status="downloaded", bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    else:
        paper["status"] = "download_failed"
    if attempts and paper["status"] == "download_failed":
        print(json.dumps(attempts, indent=2), file=sys.stderr)
    print(paper["id"], paper["status"], paper["file"], flush=True)
    return paper

papers = json.loads((ROOT / "papers.json").read_text())
selected = set(sys.argv[1:])
with ThreadPoolExecutor(max_workers=5) as pool:
    updated = list(pool.map(download, [p for p in papers if not selected or p["id"] in selected]))
by_id = {p["id"]: p for p in updated}
papers = [by_id.get(p["id"], p) for p in papers]
(ROOT / "papers.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n")
