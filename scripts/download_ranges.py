"""Download one public PDF with verified HTTP ranges.

Usage: python3 scripts/download_ranges.py URL BYTE_LENGTH OUTPUT
Useful when a slow connection times out on large research PDFs.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import sys

url, size_text, output = sys.argv[1:]
size = int(size_text)
dest = Path(output)
parts_dir = dest.parent.parent / "evidence" / "download-ranges" / dest.stem
parts_dir.mkdir(parents=True, exist_ok=True)
block = 1024 * 1024

def fetch(start):
    end = min(size - 1, start + block - 1)
    piece = parts_dir / str(start)
    headers = parts_dir / (str(start) + ".headers")
    if piece.exists() and piece.stat().st_size == end-start+1 and headers.exists():
        saved = headers.read_text(errors="replace")
        if re.search(rf"content-range:\s*bytes {start}-{end}/{size}", saved, re.I):
            return piece
    result = subprocess.run(["curl", "--location", "--fail", "--silent", "--show-error",
                             "--connect-timeout", "20", "--max-time", "180",
                             "--range", f"{start}-{end}", "--dump-header", str(headers),
                             "--output", str(piece), url], capture_output=True, text=True)
    saved = headers.read_text(errors="replace") if headers.exists() else ""
    if result.returncode or not piece.exists() or piece.stat().st_size != end-start+1 or not re.search(rf"content-range:\s*bytes {start}-{end}/{size}", saved, re.I):
        raise RuntimeError(f"Invalid range {start}-{end}: {result.stderr[-400:]}")
    print(f"completed bytes {start}-{end}", flush=True)
    return piece

with ThreadPoolExecutor(max_workers=6) as pool:
    pieces = list(pool.map(fetch, range(0, size, block)))
combined = b"".join(piece.read_bytes() for piece in pieces)
assert len(combined) == size and combined.startswith(b"%PDF-") and b"%%EOF" in combined[-4096:]
temp = Path(str(dest) + ".ranges-complete")
temp.write_bytes(combined)
temp.replace(dest)
print(f"Saved {dest}: {len(combined)} bytes", flush=True)
