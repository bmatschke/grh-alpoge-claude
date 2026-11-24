#!/usr/bin/env python3
"""Assemble v0.48 while preserving the complete v0.47 historical proof body."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
CFG=read('increment_v0_48.json')
ST=read('integration_stats_v0_48.json')
REG=read('dependency_audit_v0_48/remaining_leaf_register.json')

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

head=(ROOT/'v0_48_audit_intro.tex').read_text()
tokens={'@NEW@':ST['new_claims'],'@TOTAL@':ST['cumulative_claims'],'@OLD@':ST['cumulative_claims']-ST['new_claims'],'@OPEN@':ST['open_count'],'@C@':ST['open_categories']['C'],'@B@':ST['open_categories']['B'],'@SHARED@':ST['shared_open'],'@EXTRA@':ST['extra_grh_open']}
for token,value in tokens.items():head=head.replace(token,str(value))
blocks=[]
for i,r in enumerate(REG['records'],1):
    blocks.append(r'\paragraph{'+str(i)+'. '+esc(r['id'])+' — '+esc(r['category'])+' — '+esc(r['title'])+'}\n')
    blocks.append(esc(r['contract'])+'\n')
    if r.get('bindings'):
        blocks.append(r'\emph{Shared objects and choice order.} '+esc('; '.join(r['bindings']))+'\n')
    progress=r.get('version_0_48_progress')
    if progress:
        blocks.append(r'\emph{New completed inputs.} '+esc(', '.join(progress['completed']))+'\n')
        blocks.append(r'\emph{Current remaining subfrontier.} '+esc(progress['remaining'])+'\n')
    elif r.get('version_0_47_progress'):
        p=r['version_0_47_progress']
        blocks.append(r'\emph{Retained predecessor progress.} '+esc(', '.join(p['completed'])+'. '+p['remaining'])+'\n')
    for e in r.get('evidence',[]):
        link=e.get('url')
        if link:
            blocks.append(r'\emph{Source.} \href{'+link+'}{'+esc(e.get('declaration',e.get('path','source')))+'}.\n')
    blocks.append('\n')
audit=wraps(head+'\n'.join(blocks))
(ROOT/'dependency_audit_v0_48/main.tex').write_text(audit)

source=(ROOT/'RH_readable_reconstruction_v0_47.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_47/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
assert source.count(marker)==1
pos=source.index(marker)
prefix=source[:pos]
prefix=prefix.replace('working version 0.47','working version 0.48').replace('Working version 0.47','Working version 0.48')
prefix=prefix.replace('Rigidity, canonical connections, and original setting inputs','One-character estimates, exact measures, and common compatibility',1)
prefix=re.sub(r'A completion audit with \d+ new proof claims',f'A completion audit with {ST["new_claims"]} new proof claims',prefix,count=1)
a=prefix.index(r'\textbf{What version 0.47 achieves.}')
b=prefix.index(r'\end{minipage}',a)
front=(ROOT/'v0_48_frontmatter.tex').read_text()
for token,value in tokens.items():front=front.replace(token,str(value))
prefix=prefix[:a]+front+prefix[b:]
chapters=wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in CFG['components']))
historical=r'''\paragraph{Historical version-0.47 audit.}
The following audit and proof chapters are preserved for provenance.
Section~\ref{sec:dependency-audit-v48} is the current frontier authority.
Historical conditional theorems retain their printed hypotheses,
including hypotheses subsequently supplied by the new chapters.

'''
main=prefix+audit+'\n\\clearpage\n'+chapters+'\n\\clearpage\n'+historical+source[pos:]
a=main.index(r'\section{The arithmetic still to be written out}')
b=main.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}
Section~\ref{sec:dependency-audit-v48} gives the current complete selected
register. The full original one-character implication is now
reconstructed, with its separate common automorphy premise retained.
The full measured-data constructor, prescribed-measure covolume
normalization, principal arithmetic models, actual individual primitive
moduli points, and one common true-volume group stage are complete
at their stated scopes. The selected D3 admission follows from its
original chosen-data premise.
The remaining large input-producing tasks are:
\begin{enumerate}
'''
remaining+='\n'.join(r'\item '+esc(s) for s in CFG['remaining_major_inputs'])
remaining+=r'''
\end{enumerate}
The original fields and embeddings, a single common arithmetic and
geometric family, simultaneous thresholds, and the same lattices,
metrics, phases and measures must be preserved. The completed six-field
Hida and selected two-Link support results remain available.
The optional AQ route remains optional;
historical RF16 remains governed by DEX11. The formal proof's correctness
is not at issue in this reconstruction.

'''
main=main[:a]+wraps(remaining)+main[b:]
a=main.index('Start with the version-0.47 audit in',main.index(r'\section{Claim ledger and reading order}'))
b=main.index('RF16 correction.',a)+len('RF16 correction.')
main=main[:a]+r'''Start with the version-0.48 audit in
Section~\ref{sec:dependency-audit-v48}. The new chapters are OCH
(the full one-character implication), AMD (the complete measured-data
constructor and prescribed-measure covolume normalization), PUN
(principal models and actual primitive moduli points), and GCF
(exact common compatibility, a single true-volume stage, transport
and selected D3 admission).
CMP1--CMP6 give the inherited complete conditional terminal deduction.
All named dependencies and exact source and proof ranges are recorded
in the current ledger. All historical chapters remain available,
including the preserved RF16 correction.'''+main[b:]
(ROOT/'RH_readable_reconstruction_v0_48.tex').write_text(main)
preamble=prefix[:prefix.index(r'\begin{document}')]
new_title=r'''\begin{document}
\begin{center}
{\LARGE\bfseries RH and Dirichlet GRH: new reconstruction chapters}\\[7pt]
{\large Version 0.48 --- 23 November 2026}\\[5pt]
{\large One-character estimates, exact measures, and common compatibility}
\end{center}
\textbf{Scope.} This edition contains the current audit and the new
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
(ROOT/'RH_new_proofs_v0_48.tex').write_text(short)

txt=['RH AND DIRICHLET GRH — DEPENDENCY AUDIT v0.48','23 November 2026','',CFG['status'],'',
     'SOURCE PIN',CFG['source_commit'],'','INVENTORY',
     f"New claims: {ST['new_claims']}; cumulative claims: {ST['cumulative_claims']}.",
     f"Selected graph: {ST['selected_nodes']} nodes, {ST['selected_edges']} edges. {ST['open_count']} whole obligations remain: {ST['open_categories']['C']} C + {ST['open_categories']['B']} B. {ST['shared_open']} shared RH/GRH; {ST['extra_grh_open']} extra Dirichlet-GRH; 0 RH-only.",
     'New whole selected closures: '+', '.join(CFG['closed_selected_leaves'])+'. Original producer hypotheses of conditional results remain explicit. Inventory is not a percentage of completion.','',
     'NEW PROVED RESULTS']
for i,s in enumerate(CFG['local_conclusions'],1):txt += [f'{i}. {s}','']
txt += ['COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(REG['records'],1):
    txt += [f"{i:02d}. {r['id']} — {r['category']} — {r['title']}",'Contract: '+r['contract']]
    if r.get('bindings'):txt+=['Shared objects and choice order: '+'; '.join(r['bindings'])]
    for version in ['0_48','0_47','0_44','0_43','0_42','0_41']:
        p=r.get('version_'+version+'_progress')
        if p:
            txt+=['Version '+version.replace('_','.')+' completed inputs: '+', '.join(p['completed']), 'Remaining at that checkpoint: '+p['remaining']]
            break
    for e in r.get('evidence',[]):txt+=['Source: '+e.get('declaration','')+' — '+e.get('url',e.get('path',''))]
    txt.append('')
txt+=['NEXT LARGE ENDPOINTS']+CFG['remaining_major_inputs']+['','VALIDATION SCOPE',
 'See validation_v0_48.json, tex_validation.json and hash-bound independent mathematical and integration reviews. TeX compilation checks syntax and references; no PDF visual review or formal replay is claimed.']
(ROOT/'RH_dependency_audit_v0_48.txt').write_text('\n'.join(txt)+'\n')

readme=['# RH and unrestricted Dirichlet-GRH reconstruction — v0.48','','23 November 2026','',CFG['status'],'',
 '## Reading order','','1. `RH_reconstruction_progress_v0_48.txt`: substantive progress, mathematical ideas and exact next suppliers.',
 '2. `RH_new_proofs_v0_48.tex`: current audit and all new chapters.',
 '3. `RH_readable_reconstruction_v0_48.tex`: complete cumulative manuscript.',
 f"4. `RH_dependency_audit_v0_48.txt`: all {ST['open_count']} remaining selected contracts and current progress.",
 '5. `continuation_checkpoint.json`, `next_source_targets.json`, `provenance.json`, and `dependency_audit_v0_48/`: exact continuation records.','',
 '## Current scope','',f"{ST['new_claims']} new claims; {ST['cumulative_claims']} cumulative claims. The selected graph retains {ST['selected_nodes']} nodes and {ST['selected_edges']} edges, with {ST['open_count']} whole obligations open ({ST['open_categories']['C']} C, {ST['open_categories']['B']} B). Newly closed selected contracts: "+', '.join(CFG['closed_selected_leaves'])+'. Exact endpoints and retained foundations are specified in increment_v0_48.json.',
 '','All original coefficient rings and embeddings, prime3, fixed data before later choices, exact Haar/formal-degree normalizations, the same row objects, and common geometric/arithmetic witnesses remain in scope. The integral-cusp spanning and global-family existence hypotheses are explicitly retained.','',
 '## New chapters','']+['- `'+c+'/main.tex`' for c in CFG['components']]+['',
 '## Provenance, review and history','',
 'Every new claim has exact proof and source ranges with hashes. New cited source files are distributed in source_snapshot_v0_48; all source bytes equal the pinned git blobs. Previously matched published applications and separately retained original foundations are explicitly identified. The mathematical dependency DAG is not a mechanically extracted Lean dependency audit.','',
 'Independent mathematical reviews and the integration audit are hash-bound. Draft TeX compilation checks syntax and references. No Lean replay or PDF visual certification is asserted.','',
 'All predecessor claim records and historical proof chapters are preserved. Mutable v0.47 root metadata is frozen in history/version_0_47. SHA256SUMS covers the distributed files. Integration, assembly, validation and packaging scripts are included.','',
 'Source pin: `'+CFG['source_commit']+'`.','']
(ROOT/'README.md').write_text('\n'.join(readme))
print(json.dumps({'main_bytes':len(main.encode()),'increment_bytes':len(short.encode()),'new_claims':ST['new_claims'],'open_count':ST['open_count']},indent=2))
