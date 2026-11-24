#!/usr/bin/env python3
"""Draft-only TeX check of a completed v0.45 component."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
folder=ROOT/sys.argv[1]
proof=folder/'main.tex';build=folder/'validation';build.mkdir(exist_ok=True)
previous=(ROOT/'RH_new_proofs_v0_44.tex').read_text()
preamble=previous.split(r'\begin{document}',1)[0]
tex=build/'chapter.tex'
tex.write_text(preamble+'\n\\begin{document}\n'+proof.read_text()+'\n\\end{document}\n')
env=os.environ.copy();trees=[Path('/usr/share/texlive/texmf-dist'),Path('/usr/share/texmf'),Path('/etc/texmf')]
env['TEXMF']='{'+','.join(str(p) for p in trees if p.is_dir())+'}'
env['TEXFONTMAPS']=str(ROOT/'build_v0_44')+':'
fmt=ROOT/'build_v0_44/pdflatex.fmt';assert fmt.is_file()
for i in range(1,5):
 p=subprocess.run(['pdflatex',f'-fmt={fmt}','-draftmode','-no-shell-escape','-interaction=nonstopmode',
   '-halt-on-error',f'-output-directory={build}',str(tex)],cwd=ROOT,env=env,capture_output=True,text=True)
 (build/f'draft_pass_{i}.txt').write_text(p.stdout+p.stderr)
 if p.returncode:raise SystemExit((p.stdout+p.stderr)[-4500:])
 log=(build/'chapter.log').read_text()
 rerun=any(t in log for t in ['Rerun to get','Label(s) may have changed','Table widths have changed',
        'rerunfilecheck Warning','undefined references','Citation `'])
 if i>=2 and not rerun:break
else:raise SystemExit('Unresolved references after four passes')
assert not (build/'chapter.pdf').exists()
out={'artifact_version':'0.45','component':folder.name,'proof_file':str(proof.relative_to(ROOT)),
 'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'result':'PASS','draft_passes':i,
 'undefined_references_or_citations':any(t in log for t in ['undefined references','undefined citations','Citation `']),
 'missing_character_warnings':log.count('Missing character'),
 'overfull_box_warnings':len(re.findall(r'Overfull \\[hv]box',log)),
 'warnings':[s.strip() for s in log.splitlines() if 'Warning' in s],
 'pdf_generated':False,'visual_review_performed':False,'lean_replay':False,
 'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
assert not out['undefined_references_or_citations'] and not out['missing_character_warnings']
(folder/'tex_validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
