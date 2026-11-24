#!/usr/bin/env python3
"""Write a self-contained current audit and every exact remaining contract."""
from pathlib import Path
import collections,json,re
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_34'
cfg=json.loads((ROOT/'increment_v0_34.json').read_text());g=json.loads((AUD/'obligation_map.json').read_text())
records=json.loads((AUD/'remaining_leaf_register.json').read_text())['records'];cats=collections.Counter(x['category']for x in records)
intro=(AUD/'audit_intro.tex').read_text()
def esc(t):
 mapping={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}',
 '→':r'$\to$','−':r'$-$','≥':r'$\ge$','≤':r'$\le$','ε':r'$\varepsilon$','λ':r'$\lambda$','Ψ':r'$\Psi$','𝒞':r'$\mathcal C$','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
 return ''.join(mapping.get(c,c)for c in t)
tex= intro+'\n\\begin{description}[style=nextline]\n'
for i,n in enumerate(records,1):tex+=f"\\item[{i}. {esc(n['id'])} --- {n['category']}] {esc(n['title'])}. {esc(n['contract'])}\n\n"
tex+='\\end{description}\n\n'
tex+=r'''\paragraph{Validation and continuity.}
The release preserves predecessor claim fields, source arrays and
mathematical dependency edges. New source and proof ranges are bound
to the pinned commit and independently reviewed. The release
validator checks all inherited source ranges, graph connectivity,
exact remaining contracts, review hashes and draft TeX references.
These checks are not a new Lean replay. Historical RF16 remains
governed by its explicit DEX11 correction; no historical proof
bytes are silently rewritten. The current audit and additive scope
updates govern superseded historical frontier statements.
'''
(AUD/'main.tex').write_text(tex)
plain=(AUD/'audit_intro.txt').read_text()
for i,n in enumerate(records,1):plain+=f"\n{i}. {n['id']} — {n['category']} — {n['title']}\n\n{n['contract']}\n\n"
plain+='''VALIDATION AND CONTINUITY
Every predecessor claim field, source array and mathematical dependency edge
is preserved. Source/proof ranges are bound to the same pinned commit:
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
Independent mathematical reviews bind the final proof/metadata bytes; the
release validator checks continuity, source ranges, exact outstanding
contracts, graph reachability and review bindings. Draft TeX checks syntax
and reference resolution. It generates no PDF and is not a Lean replay.
Historical RF16 is governed by its preserved DEX11 correction. The present
audit and additive scope updates govern superseded historical frontiers.
'''
(ROOT/'RH_dependency_audit_v0_34.txt').write_text(plain)
(AUD/'audit.txt').write_text(plain)
print('Audit written:',len(plain.split()),'words;',len(records),'exact open contracts.')
