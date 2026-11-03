"""Validate local research artifacts without network access or GPU execution."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import unquote
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
papers = json.loads((ROOT / "papers.json").read_text())
results = []
errors = []
for paper in papers:
    pdf = ROOT / "papers" / paper["file"]
    txt = ROOT / "paper-text" / (pdf.stem + ".txt")
    data = pdf.read_bytes() if pdf.exists() else b""
    extracted = txt.read_text() if txt.exists() else ""
    header = re.search(r"^Pages: (\d+)$", extracted, re.M)
    pages = re.findall(r"===== PDF PAGE (\d+) =====\n(.*?)(?=\n===== PDF PAGE|\Z)", extracted, re.S)
    digest = hashlib.sha256(data).hexdigest()
    checks = {
        "status_complete": paper["status"] == "downloaded",
        "pdf_header": data.startswith(b"%PDF-"),
        "pdf_eof": b"%%EOF" in data[-4096:],
        "bytes_match_manifest": len(data) == paper.get("bytes"),
        "sha256_match_manifest": digest == paper.get("sha256"),
        "parsed_page_count_positive": bool(header and int(header[1]) > 0),
        "page_markers_match_count": bool(header and len(pages) == int(header[1])),
        "text_present": len(extracted) > 1000,
    }
    sparse = [int(n) for n, body in pages
              if len(re.sub(r"\[Sparse text layer: inspect the original PDF\]", "", body).strip()) < 80]
    result = {"id": paper["id"], "file": "papers/" + pdf.name,
              "bytes": len(data), "sha256": digest,
              "parsed_pdf_pages": int(header[1]) if header else None,
              "text_file": "paper-text/" + txt.name,
              "sparse_text_pages": sparse, "checks": checks,
              "valid": all(checks.values())}
    results.append(result)
    errors.extend(f"{paper['id']}: {key}" for key, ok in checks.items() if not ok)

broken_links = []
checked_links = 0
for doc in ROOT.glob("*.md"):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text()):
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        target = unquote(target.strip("<>").split("#", 1)[0])
        checked_links += 1
        if not (doc.parent / target).exists():
            broken_links.append({"document": doc.name, "target": target})
errors.extend(f"broken link: {x}" for x in broken_links)
bib = (ROOT / "references.bib").read_text()
bib_count = len(re.findall(r"^@(?:inproceedings|article)\{", bib, re.M))
if bib_count != len(papers):
    errors.append("BibTeX entry count differs from manifest")
report = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Offline artifact checks; no network, inference, GPU or controller evaluation",
    "paper_count": len(papers), "valid_pdf_count": sum(r["valid"] for r in results),
    "bibtex_entry_count": bib_count, "relative_markdown_links_checked": checked_links,
    "broken_relative_links": broken_links,
    "text_limitations": "PDFKit text may omit figures, equations or text in images. Sparse pages are reported; the original PDF is authoritative.",
    "papers": results, "errors": errors, "all_checks_pass": not errors,
}
(ROOT / "evidence" / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("paper_count", "valid_pdf_count", "bibtex_entry_count", "relative_markdown_links_checked", "all_checks_pass", "errors")}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
