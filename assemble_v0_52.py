#!/usr/bin/env python3
"""Assemble the current human reading editions, retaining the v0.51 proof body."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
def read(name): return json.loads((ROOT/name).read_text())
CFG=read('increment_v0_52.json')
ST=read('integration_stats_v0_52.json')
REG=read('dependency_audit_v0_52/remaining_leaf_register.json')

def esc(s):
    table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_',
      '{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}',
      '≤':r'$\le$','≥':r'$\ge$','→':r'$\to$','ℓ':r'$\ell$',
      '𝒞':r'$\mathcal C$','𝒜':r'$\mathcal A$','⇒':r'$\Rightarrow$',
      'ε':r'$\epsilon$','λ':r'$\lambda$','κ':r'$\kappa$',
      'τ':r'$\tau$','Ω':r'$\Omega$','ℚ':r'$\mathbb Q$'}
    return ''.join(table.get(c,c) for c in s)

def mono(m):
    t=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    t=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',t)
    t=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',t)
    t=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)
    return r'\texttt{'+t+'}'

def wraps(t):
    # The sole long \path in the new source appendix needs CamelCase breaks.
    # This affects no claim block or historical text.
    t=re.sub(r'\\path\{([^{}]*)\}',lambda m:r'\texttt{'+esc(m[1])+'}',t)
    t=re.sub(r'\\texttt\{([^{}]*)\}',mono,t)
    return re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',t)

tokens={'@NEW@':ST['new_claims'],'@TOTAL@':ST['cumulative_claims'],
 '@OLD@':ST['cumulative_claims']-ST['new_claims'],'@OPEN@':ST['open_count'],
 '@C@':ST['open_categories']['C'],'@B@':ST['open_categories']['B'],
 '@SHARED@':ST['shared_open'],'@EXTRA@':ST['extra_grh_open']}
def tokenized(s):
    for k,v in tokens.items(): s=s.replace(k,str(v))
    return s

intro=tokenized((ROOT/'v0_52_audit_intro.tex').read_text())
blocks=[]
for i,r in enumerate(REG['records'],1):
    blocks.append(r'\paragraph{'+str(i)+'. '+esc(r['id'])+' — '+esc(r['category'])+' — '+esc(r['title'])+'}\n')
    blocks.append(esc(r['contract'])+'\n')
    if r.get('bindings'):
        blocks.append(r'\emph{Shared objects and choice order.} '+esc('; '.join(r['bindings']))+'\n')
    for version in ['0_52','0_51','0_50','0_48','0_47','0_46','0_45','0_44','0_43','0_42']:
        p=r.get('version_'+version+'_progress')
        if p:
            blocks.append(r'\emph{Completed inputs (version '+version.replace('_','.')+').} '+esc(', '.join(p['completed']))+'\n')
            blocks.append(r'\emph{Remaining producer scope.} '+esc(p['remaining'])+'\n')
            break
    for e in r.get('evidence',[]):
        if e.get('url'):
            blocks.append(r'\emph{Source.} \href{'+e['url']+'}{'+esc(e.get('declaration',e.get('path','source')))+'}.\n')
    blocks.append('\n')
audit=wraps(intro+'\n'.join(blocks))
(ROOT/'dependency_audit_v0_52/main.tex').write_text(audit)

source=(ROOT/'RH_readable_reconstruction_v0_51.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_51/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
assert source.count(marker)==1
pos=source.index(marker)
prefix=source[:pos].replace('version 0.51','version 0.52')
prefix=prefix.replace(read('increment_v0_51.json')['title'],CFG['title'],1)
prefix=re.sub(r'A completion audit with \d+ new proof claims',
 f'A completion audit with {ST["new_claims"]} new proof claims',prefix,count=1)
a=prefix.index(r'\textbf{What version 0.52 achieves.}')
b=prefix.index(r'\end{minipage}',a)
prefix=prefix[:a]+tokenized((ROOT/'v0_52_frontmatter.tex').read_text())+prefix[b:]
chapters=wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in CFG['components']))
historical=r'''\paragraph{Historical version-0.51 audit and proof body.}
The following audit and all earlier proof chapters are preserved for provenance.
Section~\ref{sec:dependency-audit-v52} governs the current frontier.
Historical conditional statements retain their hypotheses; a later chapter
may now supply a hypothesis without rewriting the earlier proof.

'''
main=prefix+audit+'\n\\clearpage\n'+chapters+'\n\\clearpage\n'+historical+source[pos:]
a=main.index(r'\section{The arithmetic still to be written out}')
b=main.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}
Section~\ref{sec:dependency-audit-v52} is the current whole-contract register.
The v0.49 local-gain closure and all its original scope are retained.
The new chapters complete the exact subresults stated in that register;
they do not infer existence of their original supplied inputs.
The next substantial producers are:
\begin{enumerate}
'''
remaining+='\n'.join(r'\item '+esc(s) for s in CFG['remaining_major_inputs'])
remaining+=r'''
\end{enumerate}
All source fields, coefficient embeddings, metrics, phases, measures, common
marked objects and simultaneous thresholds remain in scope. The formal
proof is accepted as correct; the open items concern the human reconstruction.

'''
main=main[:a]+wraps(remaining)+main[b:]
a=main.index('Start with the version-0.51 audit in',main.index(r'\section{Claim ledger and reading order}'))
b=main.index('RF16 correction.',a)+len('RF16 correction.')
reading='Start with the version-0.52 audit in\nSection~\\ref{sec:dependency-audit-v52}.\n'
reading+='The new component reading order is '+esc(', '.join(CFG['components']))+'.\n'
reading+=r'''CMP1--CMP6 remain the inherited complete conditional terminal deduction.
The exact proof/source ranges and dependency graph are in the current ledger.
All historical chapters remain available, including the preserved RF16 correction.'''
main=main[:a]+wraps(reading)+main[b:]
(ROOT/'RH_readable_reconstruction_v0_52.tex').write_text(main)
preamble=prefix[:prefix.index(r'\begin{document}')]
title=r'''\begin{document}
\begin{center}
{\LARGE\bfseries RH and Dirichlet GRH: new human proofs}\\[7pt]
{\large Version 0.52 --- 23 November 2026}\\[5pt]
{\large '''+esc(CFG['title'])+r'''}
\end{center}
\textbf{Scope.} This edition contains the current audit and all new chapters.
It is a partial human reconstruction of the accepted formal proof.
Earlier named claims are in the cumulative manuscript and preserved components.
Each result below states its original inputs and exact remaining producers.
\setcounter{tocdepth}{1}
\tableofcontents
\clearpage
\begingroup\emergencystretch=3em
'''
short=preamble+title+audit+'\n\\clearpage\n'+chapters+'\n\\endgroup\n\\end{document}\n'
(ROOT/'RH_new_proofs_v0_52.tex').write_text(short)

txt=['RH AND DIRICHLET GRH — DEPENDENCY AUDIT v0.52','23 November 2026','',CFG['status'],'',
 'SOURCE PIN',CFG['source_commit'],'','INVENTORY',
 f"New claims: {ST['new_claims']}; cumulative claims: {ST['cumulative_claims']}.",
 f"Selected graph: {ST['selected_nodes']} nodes, {ST['selected_edges']} edges. {ST['open_count']} whole obligations remain: {ST['open_categories']['C']} C + {ST['open_categories']['B']} B. {ST['shared_open']} shared RH/GRH; {ST['extra_grh_open']} additional GRH; 0 RH-only.",
 'New whole selected closures: '+(', '.join(CFG['closed_selected_leaves']) or 'none')+'. Counts are an inventory, not a completion percentage.','',
 'NEW PROVED RESULTS']
for i,s in enumerate(CFG['local_conclusions'],1):txt += [f'{i}. {s}','']
txt+=['COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(REG['records'],1):
    txt += [f"{i:02d}. {r['id']} — {r['category']} — {r['title']}",'Contract: '+r['contract']]
    if r.get('bindings'):txt+=['Shared objects and choice order: '+'; '.join(r['bindings'])]
    for version in ['0_52','0_51','0_50','0_48','0_47','0_46','0_45','0_44','0_43','0_42']:
        p=r.get('version_'+version+'_progress')
        if p:
            txt+=['Version '+version.replace('_','.')+' completed inputs: '+', '.join(p['completed']),
                  'Remaining at that checkpoint: '+p['remaining']]
            break
    for e in r.get('evidence',[]):txt+=['Source: '+e.get('declaration','')+' — '+e.get('url',e.get('path',''))]
    txt.append('')
txt+=['NEXT LARGE ENDPOINTS']+CFG['remaining_major_inputs']+['','VALIDATION SCOPE',
 'See validation_v0_52.json, tex_validation.json and exact-hash independent mathematical and integration reviews. TeX compilation checks syntax and references; no PDF visual review or formal replay is claimed.']
(ROOT/'RH_dependency_audit_v0_52.txt').write_text('\n'.join(txt)+'\n')

readme=['# RH and unrestricted Dirichlet-GRH human reconstruction — v0.52','','23 November 2026','',
 CFG['status'],'','## Reading order','',
 '1. `RH_reconstruction_progress_v0_52.txt`: mathematical results, methods and current boundary.',
 '2. `RH_new_proofs_v0_52.tex`: all new proofs and the current audit.',
 '3. `RH_readable_reconstruction_v0_52.tex`: complete cumulative manuscript.',
 '4. `RH_GRH_reconstruction_roadmap_v0_52.txt`: updated concrete research tasks.',
 '5. `RH_GRH_parallel_execution_plan_v0_52.txt`: independent work packages and integration requirements.',
 '6. `RH_dependency_audit_v0_52.txt`, `continuation_checkpoint.json`, `next_source_targets.json` and `provenance.json`: full contracts and exact continuation records.','',
 '## Current inventory','',
 f"{ST['new_claims']} new claims; {ST['cumulative_claims']} cumulative claims. The selected sufficient graph has {ST['selected_nodes']} nodes and {ST['selected_edges']} edges. {ST['open_count']} whole obligations remain ({ST['open_categories']['C']} C, {ST['open_categories']['B']} B), comprising {ST['shared_open']} shared RH/GRH and {ST['extra_grh_open']} additional GRH obligations.",
 'New whole selected closures: '+(', '.join(CFG['closed_selected_leaves']) or 'none')+'. Complete subtheorems and their retained producer premises are recorded separately. Claim counts are not a completion percentage.','',
 '## New chapters','']
readme+=['- `'+c+'/main.tex`' for c in CFG['components']]
readme+=['','## Preservation and verification','',
 'Every predecessor claim record and the entire historical cumulative proof body are preserved. Mutable v0.51 root metadata and the two supplied v0.51 plans are frozen in `history/version_0_51`. All new cited source files were compared byte-for-byte with the exact pinned Git blobs and are included in `source_snapshot_v0_52`.','',
 'Every new claim has exact proof/source ranges and an independent mathematical review. The dependency graph records the human argument; it is not a mechanically extracted Lean dependency graph. Draft TeX compilation checks syntax and references. No Lean replay, PDF generation or PDF visual certification is asserted.','',
 'The archive includes integration, assembly, validation and packaging scripts. `SHA256SUMS` binds all distributed files.','',
 'Source pin: `'+CFG['source_commit']+'`.','']
(ROOT/'README.md').write_text('\n'.join(readme))
print(json.dumps({'main_bytes':len(main.encode()),'increment_bytes':len(short.encode()),
 'new_claims':ST['new_claims'],'open_count':ST['open_count']},indent=2))
