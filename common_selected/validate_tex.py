#!/usr/bin/env python3
"""Bounded offline draft-mode TeX syntax check; no PDF is generated."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--baseline", type=Path, default=HERE.parents[1]/"reconstruction_v036")
args = ap.parse_args()
BASE = args.baseline.resolve()
OUT = HERE/"validation"
OUT.mkdir(exist_ok=True)
pre = (BASE/"RH_readable_reconstruction_v0_36.tex").read_text().split(r"\begin{document}", 1)[0]
(OUT/"check.tex").write_text(pre + "\\begin{document}\n\\input{main.tex}\n\\end{document}\n")
env = os.environ.copy()
env["TEXMF"] = "{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}"
env["TEXFONTMAPS"] = str(BASE/"build") + ":"
for i in range(2):
    result = subprocess.run([
        "pdflatex", "-fmt="+str(BASE/"build/pdflatex.fmt"),
        "-draftmode", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
        "-output-directory="+str(OUT), str(OUT/"check.tex")],
        cwd=HERE, env=env, capture_output=True, text=True)
    (OUT/"console.txt").write_text(result.stdout+result.stderr)
    log = (OUT/"check.log").read_text(errors="replace") if (OUT/"check.log").exists() else result.stdout+result.stderr
    if result.returncode or not any(x in log for x in ("Rerun to get", "Label(s) may have changed", "rerunfilecheck Warning")):
        break
record = {
    "status": "PASS" if result.returncode == 0 else "FAIL",
    "main_sha256": hashlib.sha256((HERE/"main.tex").read_bytes()).hexdigest(),
    "method": "Offline pdflatex -draftmode -no-shell-escape with the inherited cumulative preamble; no PDF or visual layout review",
    "returncode": result.returncode, "passes": i+1,
    "overfull_box_count": len(re.findall("Overfull", log)),
    "missing_characters": log.count("Missing character"),
    "warnings": [x for x in log.splitlines() if "Warning" in x],
    "no_pdf_generated": not (OUT/"check.pdf").exists(),
}
(HERE/"tex_validation.json").write_text(json.dumps(record, indent=2)+"\n")
print(json.dumps(record, indent=2))
for match in re.finditer("Overfull", log):
    print(log[match.start():match.start()+330])
if result.returncode:
    print((result.stdout+result.stderr)[-2400:])
raise SystemExit(result.returncode)
