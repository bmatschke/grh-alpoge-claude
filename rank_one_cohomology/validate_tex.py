#!/usr/bin/env python3
"""Validate the RV chapter with the established preamble, without making a PDF."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
BUILD = HERE / "build"
BUILD.mkdir(exist_ok=True)
preamble = (WORK / "RH_readable_reconstruction_v0_25.tex").read_text().split(
    r"\begin{document}", 1)[0]
wrapper = BUILD / "rank_one_check.tex"
wrapper.write_text(preamble + "\\begin{document}\n\\input{../main.tex}\n\\end{document}\n")
env = os.environ.copy()
env["TEXMF"] = "{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}"
env["TEXFONTMAPS"] = str(WORK / "build") + ":"
fmt = WORK / "build/pdflatex.fmt"
for i in range(2):
    p = subprocess.run(
        ["pdflatex", "-fmt=" + str(fmt), "-draftmode", "-no-shell-escape",
         "-interaction=nonstopmode", "-halt-on-error", wrapper.name],
        cwd=BUILD, env=env, text=True, capture_output=True)
    (BUILD / f"pass_{i + 1}.txt").write_text(p.stdout + p.stderr)
    if p.returncode:
        raise SystemExit((p.stdout + p.stderr)[-6000:])
raw = (BUILD / "rank_one_check.log").read_bytes()
log = raw.decode()
result = {
    "schema": "rh-tex-validation/1", "artifact_version": "0.26",
    "component": "rank_one_cohomology",
    "main_tex_sha256": hashlib.sha256((HERE / "main.tex").read_bytes()).hexdigest(),
    "mode": "pdflatex draftmode with no shell escape and established cumulative preamble",
    "passes": 2, "syntax_compile_succeeded": True,
    "pdf_generated": False, "visual_review_performed": False,
    "undefined_control_sequences": log.count("Undefined control sequence"),
    "undefined_reference_or_citation": bool(re.search("undefined references|undefined citations", log)),
    "missing_character_warnings": log.count("Missing character"),
    "overfull_box_warnings": len(re.findall(r"Overfull \\[hv]box", log)),
    "underfull_box_warnings": len(re.findall(r"Underfull \\[hv]box", log)),
    "warnings": [line for line in log.splitlines() if "Warning" in line],
    "log_sha256": hashlib.sha256(raw).hexdigest(),
    "scope": "Syntax/reference and box-warning check only; no mathematical certification or Lean replay.",
}
assert not (BUILD / "rank_one_check.pdf").exists()
(HERE / "tex_validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
