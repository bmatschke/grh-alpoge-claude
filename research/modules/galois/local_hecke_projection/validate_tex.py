#!/usr/bin/env python3
"""Compile the standalone HLP chapter twice in draft mode; no Lean is run."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess

HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--format',type=Path)
p.add_argument('--engine',default='pdflatex')
args=p.parse_args()
work=HERE/'validation'
work.mkdir(exist_ok=True)
command=[args.engine]
if args.format:
    command += ['-fmt='+str(args.format.resolve())]
command += ['-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
            '-draftmode','check.tex']
env=os.environ.copy()
env['TEXMF']='{/usr/share/texlive/texmf-dist,/usr/share/texmf,/etc/texmf}'
env['TEXFONTMAPS']=str(work)+':'
passes=[]
for index in [1,2]:
    result=subprocess.run(command,cwd=work,env=env,text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (work/f'pass_{index}.txt').write_text(result.stdout)
    passes.append(dict(pass_number=index,returncode=result.returncode,
                       transcript=f'pass_{index}.txt'))
    if result.returncode:
        raise SystemExit(f'TeX pass {index} failed; inspect its transcript.')
log=(work/'check.log').read_text()
diagnostics=dict(overfull_boxes=len(re.findall(r'Overfull \\[hv]box',log)),
                 missing_characters=len(re.findall(r'Missing character:',log)),
                 undefined_references=len(re.findall(r'(?:Reference|Citation).*undefined|There were undefined references',log)),
                 latex_errors=len(re.findall(r'^!',log,re.M)))
assert not any(diagnostics.values()),diagnostics
sha=lambda b:hashlib.sha256(b).hexdigest()
record=dict(schema='rh-standalone-tex-validation/1',component='local_hecke_projection',
 artifact_version='0.41',proof_file_sha256=sha((HERE/'main.tex').read_bytes()),
 status='PASS',mode='two-pass standalone draft TeX; no PDF produced; no Lean build',
 command=command,environment={'TEXMF':env['TEXMF']},passes=passes,
 diagnostics=diagnostics,source_frozen=True,
 files=[dict(file=name,sha256=sha((work/name).read_bytes())) for name in
        ['check.tex','pass_1.txt','pass_2.txt','check.log']])
(work/'validation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
