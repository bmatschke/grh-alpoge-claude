#!/usr/bin/env python3
"""Assemble v0.45 while preserving the complete v0.44 historical proof body."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
CFG=read('increment_v0_45.json')
ST=read('integration_stats_v0_45.json')
REG=read('dependency_audit_v0_45/remaining_leaf_register.json')

def esc(s):
    table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_',
           '{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}',
           '≤':r'$\le$','≥':r'$\ge$','→':r'$\to$','ℓ':r'$\ell$','𝒞':r'$\mathcal C$','𝒜':r'$\mathcal A$'}
    return ''.join(table.get(c,c) for c in s)

def mono(m):
    t=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    t=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',t)
    t=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',t)
    t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
    return r'\texttt{'+t+'}'

def wraps(t):
    t=re.sub(r'\\texttt\{([^{}]*)\}',mono,t)
    return re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)

head=(ROOT/'v0_45_audit_intro.tex').read_text()
head=head.replace('@NEW@',str(ST['new_claims'])).replace('@TOTAL@',str(ST['cumulative_claims'])).replace('@OLD@',str(ST['cumulative_claims']-ST['new_claims']))
blocks=[]
for i,r in enumerate(REG['records'],1):
    blocks.append(r'\paragraph{'+str(i)+'. '+esc(r['id'])+' — '+esc(r['category'])+' — '+esc(r['title'])+'}\n')
    blocks.append(esc(r['contract'])+'\n')
    if r.get('bindings'):
        blocks.append(r'\emph{Shared objects and choice order.} '+esc('; '.join(r['bindings']))+'\n')
    progress=r.get('version_0_45_progress')
    if progress:
        blocks.append(r'\emph{New completed inputs.} '+esc(', '.join(progress['completed']))+'\n')
        blocks.append(r'\emph{Current remaining subfrontier.} '+esc(progress['remaining'])+'\n')
    elif r.get('version_0_44_progress'):
        p=r['version_0_44_progress']
        blocks.append(r'\emph{Retained predecessor progress.} '+esc(', '.join(p['completed'])+'. '+p['remaining'])+'\n')
    for e in r.get('evidence',[]):
        link=e.get('url')
        if link:
            blocks.append(r'\emph{Source.} \href{'+link+'}{'+esc(e.get('declaration',e.get('path','source')))+'}.\n')
    blocks.append('\n')
audit=wraps(head+'\n'.join(blocks))
(ROOT/'dependency_audit_v0_45/main.tex').write_text(audit)

source=(ROOT/'RH_readable_reconstruction_v0_44.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_44/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
assert source.count(marker)==1
pos=source.index(marker)
prefix=source[:pos]
prefix=prefix.replace('working version 0.44','working version 0.45').replace('Working version 0.44','Working version 0.45')
prefix=prefix.replace('Automorphic parts, ordinary points, and the same ideal','The six Hida fields and both support installations',1)
prefix=prefix.replace('A completion audit with 119 new proof claims',f'A completion audit with {ST["new_claims"]} new proof claims',1)
a=prefix.index(r'\textbf{What version 0.44 achieves.}')
b=prefix.index(r'\end{minipage}',a)
front=(ROOT/'v0_45_frontmatter.tex').read_text().replace('@NEW@',str(ST['new_claims'])).replace('@TOTAL@',str(ST['cumulative_claims']))
prefix=prefix[:a]+front+prefix[b:]
chapters=wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in CFG['components']))
historical=r'''\paragraph{Historical version-0.44 audit.}
The following audit and proof chapters are preserved for provenance.
Section~\ref{sec:dependency-audit-v45} is the current frontier authority.
Historical conditional theorems retain their printed hypotheses,
including hypotheses subsequently supplied by the new chapters.

'''
main=prefix+audit+'\n\\clearpage\n'+chapters+'\n\\clearpage\n'+historical+source[pos:]
a=main.index(r'\section{The arithmetic still to be written out}')
b=main.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}
Section~\ref{sec:dependency-audit-v45} gives the current complete selected
register. The six original Hida fields, the all-level same-ideal automorphy
producer, and both selected rank-four Hida/$P_1$ support installations
are complete at their explicitly stated scopes.
The remaining large input-producing tasks are:
\begin{enumerate}
'''
remaining+='\n'.join(r'\item '+esc(s) for s in CFG['remaining_major_inputs'])
remaining+=r'''
\end{enumerate}
The same ideal, original fields and embeddings, both rank-four Links,
one coefficient threshold, and the common lattices, metrics and
measures must be preserved. The optional AQ route remains optional;
historical RF16 remains governed by DEX11. The formal proof's correctness
is not at issue in this reconstruction.

'''
main=main[:a]+wraps(remaining)+main[b:]
a=main.index('Start with the version-0.44 audit in',main.index(r'\section{Claim ledger and reading order}'))
b=main.index('RF16 correction.',a)+len('RF16 correction.')
main=main[:a]+r'''Start with the version-0.45 audit in
Section~\ref{sec:dependency-audit-v45}. The new chapters are HED
(arithmetic-point decomposition), HAW (automorphy away), HPT
(return to the actual Hecke support), HTS (twisting), HLM (the full
auxiliary-level module family), HTW (integral Taylor--Wiles data),
and HIA (the six-field Hida assembly and both selected support
installations).
CMP1--CMP6 give the inherited complete conditional terminal deduction.
All named dependencies and exact source and proof ranges are recorded
in the current ledger. All historical chapters remain available,
including the preserved RF16 correction.'''+main[b:]
(ROOT/'RH_readable_reconstruction_v0_45.tex').write_text(main)
preamble=prefix[:prefix.index(r'\begin{document}')]
new_title=r'''\begin{document}
\begin{center}
{\LARGE\bfseries RH and Dirichlet GRH: new reconstruction chapters}\\[7pt]
{\large Version 0.45 --- 23 November 2026}\\[5pt]
{\large The six Hida fields and both support installations}
\end{center}
\textbf{Scope.} This edition contains the current audit and the seven new
chapters. It remains a partial human reconstruction. Earlier named
claims are in the cumulative manuscript and preserved component files.
The underlying formal proof is accepted as correct; the exact remaining
human reconstruction boundaries are stated below.
\setcounter{tocdepth}{1}
\tableofcontents
\clearpage
\begingroup\emergencystretch=3em
'''
short=preamble+new_title+audit+'\n\\clearpage\n'+chapters+'\n\\endgroup\n\\end{document}\n'
(ROOT/'RH_new_proofs_v0_45.tex').write_text(short)

txt=['RH AND DIRICHLET GRH — DEPENDENCY AUDIT v0.45','23 November 2026','',CFG['status'],'',
     'SOURCE PIN',CFG['source_commit'],'','INVENTORY',
     f"New claims: {ST['new_claims']}; cumulative claims: {ST['cumulative_claims']}.",
     f"Selected graph: {ST['selected_nodes']} nodes, {ST['selected_edges']} edges. {ST['open_count']} whole obligations remain: {ST['open_categories']['C']} C + {ST['open_categories']['B']} B. {ST['shared_open']} shared RH/GRH; {ST['extra_grh_open']} extra Dirichlet-GRH; 0 RH-only.",
     'COUNT_II_SUPPORT is closed in its entire original selected scope. The other 30 whole obligations are unchanged. Inventory is not a percentage of completion.','',
     'NEW PROVED RESULTS']
for i,s in enumerate(CFG['local_conclusions'],1):txt += [f'{i}. {s}','']
txt += ['COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(REG['records'],1):
    txt += [f"{i:02d}. {r['id']} — {r['category']} — {r['title']}",'Contract: '+r['contract']]
    if r.get('bindings'):txt+=['Shared objects and choice order: '+'; '.join(r['bindings'])]
    for version in ['0_45','0_44']:
        p=r.get('version_'+version+'_progress')
        if p:
            txt+=['Version '+version.replace('_','.')+' completed inputs: '+', '.join(p['completed']), 'Remaining at that checkpoint: '+p['remaining']]
            break
    for e in r.get('evidence',[]):txt+=['Source: '+e.get('declaration','')+' — '+e.get('url',e.get('path',''))]
    txt.append('')
txt+=['NEXT LARGE ENDPOINTS']+CFG['remaining_major_inputs']+['','VALIDATION SCOPE',
 'See validation_v0_45.json, tex_validation.json and hash-bound independent mathematical and integration reviews. TeX compilation checks syntax and references; no PDF visual review or formal replay is claimed.']
(ROOT/'RH_dependency_audit_v0_45.txt').write_text('\n'.join(txt)+'\n')

readme=['# RH and unrestricted Dirichlet-GRH reconstruction — v0.45','','23 November 2026','',CFG['status'],'',
 '## Reading order','','1. `RH_reconstruction_progress_v0_45.txt`: substantive progress, mathematical ideas and exact next suppliers.',
 '2. `RH_new_proofs_v0_45.tex`: current audit and all seven new chapters.',
 '3. `RH_readable_reconstruction_v0_45.tex`: complete cumulative manuscript.',
 '4. `RH_dependency_audit_v0_45.txt`: all 30 remaining selected contracts and current progress.',
 '5. `continuation_checkpoint.json`, `next_source_targets.json`, `provenance.json`, and `dependency_audit_v0_45/`: exact continuation records.','',
 '## Current scope','',f"{ST['new_claims']} new claims; {ST['cumulative_claims']} cumulative claims. The selected graph retains 121 nodes and 161 edges, with 30 whole obligations open (21 C, 9 B). COUNT_II_SUPPORT is newly closed as an entire selected contract. The exact endpoints and retained foundations are specified in increment_v0_45.json.",
 '','The original coefficient rings and embeddings, prime3, both rank-four Links, the same J, one common coefficient threshold, and original metrics/lattices/measures remain in scope.','',
 '## New chapters','']+['- `'+c+'/main.tex`' for c in CFG['components']]+['',
 '## Provenance, review and history','',
 'Every new claim has exact proof and source ranges with hashes. New cited source files are distributed in source_snapshot_v0_45; all source bytes equal the pinned git blobs. Previously matched published applications and separately retained original foundations are explicitly identified. The mathematical dependency DAG is not a mechanically extracted Lean dependency audit.','',
 'Independent mathematical reviews and the integration audit are hash-bound. Draft TeX compilation checks syntax and references. No Lean replay or PDF visual certification is asserted.','',
 'All predecessor claim records and historical proof chapters are preserved. Mutable v0.44 root metadata is frozen in history/version_0_44. SHA256SUMS covers the distributed files. Integration, assembly, validation and packaging scripts are included.','',
 'Source pin: `'+CFG['source_commit']+'`.','']
(ROOT/'README.md').write_text('\n'.join(readme))
print(json.dumps({'main_bytes':len(main.encode()),'increment_bytes':len(short.encode()),'new_claims':ST['new_claims'],'open_count':ST['open_count']},indent=2))
