#!/usr/bin/env python3
"""Draft-only standalone syntax validation; no PDF or Lean build."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument("--preamble",type=Path,required=True)
a=p.parse_args();BUILD=HERE/"validation";BUILD.mkdir(exist_ok=True)
preamble=a.preamble.read_text().split(r"\begin{document}",1)[0]
(BUILD/"check.tex").write_text(preamble+r"\begin{document}"+"\n"+(HERE/"main.tex").read_text()+r"\end{document}"+"\n")
env=os.environ.copy();trees=[Path("/usr/share/texlive/texmf-dist"),Path("/usr/share/texmf"),Path("/etc/texmf")]
env["TEXMF"]="{"+",".join(str(p) for p in trees if p.is_dir())+"}";env["TEXFONTMAPS"]=str(BUILD)+":"
maps=[trees[1]/"fonts/map/dvips/lm/lm.map"]+[trees[0]/("fonts/map/dvips/amsfonts/"+s+".map") for s in ["cm","symbols","euler","latxfont","cmextra"]]
(BUILD/"pdftex.map").write_text("\n".join(p.read_text() for p in maps))
fmt=HERE.parent.parent/"reconstruction_v037/build/pdflatex.fmt"
if not fmt.is_file():
    fmt=BUILD/"pdflatex.fmt"
    if not fmt.exists():
        r=subprocess.run(["pdftex","-ini","-etex","-no-shell-escape","-interaction=nonstopmode","-halt-on-error","-jobname=pdflatex",r"\input pdflatex.ini"],cwd=BUILD,env=env,capture_output=True,text=True)
        (BUILD/"format_build.txt").write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr)[-2000:]
for i in [1,2]:
    r=subprocess.run(["pdflatex",f"-fmt={fmt}","-draftmode","-no-shell-escape","-interaction=nonstopmode","-halt-on-error","check.tex"],cwd=BUILD,env=env,capture_output=True,text=True)
    (BUILD/f"console_{i}.txt").write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr)[-3000:]
log=(BUILD/"check.log").read_text()
d={"artifact_version":"0.38","component":"seed_boundedness","main_tex_sha256":hashlib.sha256((HERE/"main.tex").read_bytes()).hexdigest(),
 "syntax_compile_succeeded":True,"passes":2,"pdf_generated":(BUILD/"check.pdf").exists(),
 "undefined_references":bool(re.search("undefined references|undefined citations",log)),
 "missing_character_warnings":log.count("Missing character"),"overfull_box_warnings":len(re.findall(r"Overfull \\[hv]box",log)),
 "scope":"Standalone draft syntax only; no PDF, mathematical certification or Lean replay."}
assert not d["pdf_generated"] and not d["undefined_references"] and d["missing_character_warnings"]==0
(BUILD/"validation.json").write_text(json.dumps(d,indent=2)+"\n");print(json.dumps(d,indent=2))

