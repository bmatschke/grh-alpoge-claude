#!/usr/bin/env python3
"""Assemble v0.43 while preserving the complete v0.42 historical proof body."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
CFG=read('increment_v0_43.json')
ST=read('integration_stats_v0_43.json')
REG=read('dependency_audit_v0_43/remaining_leaf_register.json')

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

head=r'''\section{Current dependency audit: integral types, arithmetic fibers, and finite local weights}
\label{sec:dependency-audit-v43}

\subsection{Current status and reading order}

Version 0.43 supplies the original integral type and Hecke-data
constructor, the actual compact-unitary automorphic decomposition,
the exact classical and ordinary part decomposition, and the dense
arithmetic-fiber and scalar-separation arguments. It also completes
the finite local estimates used by the selected retained-row weight
consumer. These results are proved on the original objects and at
their stated scopes; their still-required global suppliers are listed
below.

The pinned Alpoge--Claude formal proof is accepted as fully checked
and correct. This remains a \textbf{partial human reconstruction} of
RH and unrestricted Dirichlet GRH. The common arithmetic and geometric
families and the global quantitative producers have not all been
reconstructed. No formal correctness question is reopened, and no
Lean build or kernel replay is claimed.

There are @NEW@ new and @TOTAL@ cumulative claims. All @OLD@ predecessor
claim records, their source arrays and dependency edges are preserved.
The selected sufficient-route graph still has 121 nodes and 161 edges.
No whole selected leaf is closed by this increment: its 31 remaining
whole obligations consist of 22 class-C and 9 class-B tasks. Of these,
24 are shared by RH and Dirichlet GRH, and 7 are additional for Dirichlet
GRH. These counts measure recorded scopes, not a percentage of proof
completion. Progress inside the two affected compound obligations is
substantial and recorded exactly.

Read ITA for the integral type, ADP then CFD for the two decompositions,
AFS for arithmetic points and separation, and FLC for the finite local
weight theorem. The earlier CMP1--CMP6 contain the complete conditional
terminal deduction; they are not repeated or promoted to an unconditional
human proof. The separate reader's edition contains this audit and only
the five new chapters. The cumulative edition preserves the earlier
chapters, whose conditional statements retain their printed hypotheses.

\subsection{The original integral type and Hecke data}

ITA1--ITA13 produce one representation over the original coefficient
DVR $O$, before the later choices of a Teichmuller lift family,
local correspondence or test representation. Uniqueness of the original
Teichmuller lifts handles the first universal quantifier. On the toral
zero-monodromy sector, the written reciprocity and singleton Langlands
quotient calculation handles every weaker source \texttt{IsRecT} map;
it does not presume global uniqueness for those maps.

The explicitly matched crystalline inertial-type theorem supplies a
complex local detector. The original normalization makes its inducing
norm exponents integers, so arbitrary coefficient automorphisms fixing
$j(O)$ preserve the detected predicate. A stable lattice is constructed
over a finite extension and then restricted as a module to the original
$O$. Every conjugate summand still detects exactly the prescribed type.
The dual representation gives the source's precise inverse-transpose
column equation. Successive finite tensor--Hom constructions establish
the product theorem for every nonzero individually isotypic module,
without adding finite length or admissibility of that module.

This proves \texttt{TypeForAlt} at every original allowed prime and
rank, including coefficient prime three, repeated inertia characters,
and an empty set of type places. ITA13 substitutes it into OTW13 and
CAP17, giving the original \texttt{HdEx}/\texttt{UnitaryHeckeData}.
Classical local Langlands and the source's \texttt{RecTExists}
nonemptiness remain explicit inherited foundations; the type theorem
is a matched established input, not a new proof of the entire local
classification.

\subsection{Actual automorphic and classical decompositions}

ADP1--ADP12 work with the original identity-form definite unitary group.
The exact finite class representatives yield a compact fundamental set;
the original quotient measure supplies a positive definite invariant
form on actual continuous functions. Finite multiplicity and the
checked algebraic semisimplicity argument give finite globally
equivariant projections. The explicit scalarization
\[
 \mathcal T_F(\lambda^*)(g)
  =\lambda^*\bigl(R(g^{-1})E(F(p(g)))\bigr)
\]
and its bidual inverse keep the prescribed complex embedding, basis,
infinity representation and rational equivariance. Projecting all
scalarizations and inverting preserves the full matrix-valued
coefficient equations. This proves the original \texttt{formU} and
\texttt{decompU}, on the actual quotient rather than a substituted
representation space.

CFD1--CFD12 show how a supplied decomposition into the original parts
can be refined without changing the level, depth or scalar characters.
Finite averaging uses left cosets and is valid for nonnormal
stabilizers. Commuting compact-group scalar profiles preserve the
original classical equations. Polynomial generalized-eigenspace
projectors then preserve the exact norm-one ordinary condition for
the original normalized $U_z$. This proves full \texttt{clParts\_alt},
including its useful arbitrary-predicate refinement.

The distinction between these endpoints is essential. ADP gives
actual automorphic constituents. The original \texttt{PartAltAlt}
additionally includes a Galois representation, spherical readings,
local comparisons and arithmetic point properties. Its producer,
\texttt{partX\_alt}/\texttt{partU\_alt}, still has to be reconstructed.
CFD retains the exact \texttt{AutomorphicHeckeSet} premise that this
producer will supply.

\subsection{Dense weights, nonflat fibers, scalar action and the same ideal}

AFS1--AFS8 prove the domain and full \texttt{DenseWt} statements for
every supplied original universal weight ring and every original
dominant weight. Bounded integral power series are separated by the
written infinite Cartesian torsion sets in the open unit disk. The
torsion levels distinguish the finite-part characters, and the exact
stored Artin-map and cyclotomic identities give the literal arithmetic
and good-point predicates. The target remains
$\overline{\mathbf Q}_\ell$, not its completion.

AFS9--AFS19 supply the original fiber and scalar arguments. Every
specified character of the faithful finite operator algebra occurs
in its module fiber, even for a nonflat point map. Every nonzero
finite free ordinary block has nonzero fibers; this does not assert
that an arbitrary residual label gives a nonzero block. The compact
averaging description of the Jacquet kernel and the stated original
local literature clauses prove the distinct-unit principal-series
criterion with the exact scalar normalization. The determinant
argument turns the source's integral eigenvalues into units.

The tensor identification uses the split ordinary idempotent and
the already reconstructed specialization map. Consequently it
transports the actual part decomposition, every Hecke generator,
each specified fiber character and the unique scalar character on
each nonzero good part. This proves full \texttt{partAct0\_alt}.
AFS20 then proves the exact \texttt{TCoreSep}/\texttt{Out.sep}
assertion: a Hecke element vanishing at all good arithmetic points
is zero. The proof expands its action in the original ordinary
basis and applies \texttt{DenseWt} to every coefficient.

AFS21--AFS22 apply this separation to the original map $f:B\to T$.
For the same ideal $J=\ker f$,
\[
 \bigl[x(b)=0\text{ for every original good point }x
                  \text{ killing }J\bigr]\quad\Longrightarrow\quad b\in J.
\]
No radical, larger support ideal or replacement quotient is introduced.
The zero-module case has $J=B$ and is treated separately. The complete
density implication is written with the exact remaining
\texttt{AutomorphicHeckeSet} supplier exposed. Thus the bare original
\texttt{TJDense} installation, the point-output record and the other
same-ideal Hida fields remain part of the current frontier.

\subsection{The selected finite local weight theorem}

FLC1--FLC5 prove the remaining original root-injectivity collision
estimate with its constant $23$, for every finite field of cardinality
at least $2^{12}$ and every original degree. The same-factor estimate
uses the shortened Frobenius orbit after removing the prime-primary
part. In the cross-factor estimate, a common Frobenius translation
places every possible collision in one fixed fiber, avoiding a loss
by the degree of the fixed factor. Weighted divisor bounds and the
explicit numerical series estimates give the stated constant.

FLC6--FLC18 prove the exact finite mirabolic and root-exchange
calculations, the lower $e_J$ comparison and the squarefree $e_U$
weight formula. Green's cuspidal classification is the one explicit
published finite-group input, with its original simplex, sign, degree
and elliptic-value dictionary checked. The comparison to the supplied
normalized-type record preserves the actual series projectors and
factor degrees. Polynomial root predicates are still evaluated on
the original polynomial, and are never transported by an arbitrary
permutation of labels.

FLC19 assembles the actual \texttt{WeightAllRows} assertion for the
selected eventual family, with the unchanged $W_g$ and all five local
error terms. The last term uses RRT10's eventual rank threshold;
the original selected rank growth, not \texttt{SizesAt} alone,
absorbs it uniformly. The stronger fourth \texttt{admLq} upper
comparison is unused by this consumer and is not claimed.

The original normalized-type compatibility, adelic reduction and
inflation with its Haar normalization, row identities, common
\texttt{AllRows} object and arithmetic cylinder counts remain actual
inputs to be produced. A local weight theorem therefore does not close
the whole \texttt{GLOBAL\_RETAINED\_DEFECT} obligation.

\subsection{Every remaining selected obligation}

Each contract below is the full selected output. Completed nested
theorems remain available inputs; no compound contract is closed until
its other suppliers, shared objects and choice-order conditions have
been reconstructed. The current notes govern the historical frontier
descriptions retained in the cumulative chapters.
'''
head=head.replace('@NEW@',str(ST['new_claims'])).replace('@TOTAL@',str(ST['cumulative_claims'])).replace('@OLD@',str(ST['cumulative_claims']-ST['new_claims']))
blocks=[]
for i,r in enumerate(REG['records'],1):
    blocks.append(r'\paragraph{'+str(i)+'. '+esc(r['id'])+' — '+esc(r['category'])+' — '+esc(r['title'])+'}\n')
    blocks.append(esc(r['contract'])+'\n')
    if r.get('bindings'):
        blocks.append(r'\emph{Shared objects and choice order.} '+esc('; '.join(r['bindings']))+'\n')
    progress=r.get('version_0_43_progress')
    if progress:
        blocks.append(r'\emph{New completed inputs.} '+esc(', '.join(progress['completed']))+'\n')
        blocks.append(r'\emph{Current remaining subfrontier.} '+esc(progress['remaining'])+'\n')
    elif r.get('version_0_42_progress'):
        p=r['version_0_42_progress']
        blocks.append(r'\emph{Retained predecessor progress.} '+esc(', '.join(p['completed'])+'. '+p['remaining'])+'\n')
    for e in r.get('evidence',[]):
        link=e.get('url')
        if link:
            blocks.append(r'\emph{Source.} \href{'+link+'}{'+esc(e.get('declaration',e.get('path','source')))+'}.\n')
    blocks.append('\n')
audit=wraps(head+'\n'.join(blocks))
(ROOT/'dependency_audit_v0_43/main.tex').write_text(audit)

source=(ROOT/'RH_readable_reconstruction_v0_42.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_42/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
assert source.count(marker)==1
pos=source.index(marker)
prefix=source[:pos]
prefix=prefix.replace('working version 0.42','working version 0.43').replace('Working version 0.42','Working version 0.43')
prefix=prefix.replace('Ordinary structure, rigidity, and quantitative reductions','Integral types, arithmetic fibers, and finite local weights',1)
prefix=prefix.replace('A completion audit with 154 new proof claims',f'A completion audit with {ST["new_claims"]} new proof claims',1)
a=prefix.index(r'\textbf{What version 0.42 achieves.}')
b=prefix.index(r'\end{minipage}',a)
front=r'''\textbf{What version 0.43 achieves.}
The full original integral type and Hecke-data supplier are constructed.
The actual compact-unitary and classical decompositions are proved.
Dense good weight points, the original fiber/scalar actions and the
same-kernel separation argument are written out. The selected finite
local weight theorem now has all of its local quantitative inputs.

There are @NEW@ new and @TOTAL@ cumulative claims. The selected
whole-obligation register still has 31 entries: 22 C and 9 B.
Actual Galois-decorated automorphic parts, their same-ideal Hida/support
installation, common geometry and global quantitative producers remain.
This is a \textbf{partial human reconstruction}; the formal proof is
accepted as correct and the exact remaining supplier boundaries are
preserved. The current audit governs historical frontier notes.
'''.replace('@NEW@',str(ST['new_claims'])).replace('@TOTAL@',str(ST['cumulative_claims']))
prefix=prefix[:a]+front+prefix[b:]
chapters=wraps('\n\n'.join((ROOT/c/'main.tex').read_text() for c in CFG['components']))
historical=r'''\paragraph{Historical version-0.42 audit.}
The following audit and proof chapters are preserved for provenance.
Section~\ref{sec:dependency-audit-v43} is the current frontier authority.
Historical conditional theorems retain their printed hypotheses,
including hypotheses subsequently supplied by the new chapters.

'''
main=prefix+audit+'\n\\clearpage\n'+chapters+'\n\\clearpage\n'+historical+source[pos:]
a=main.index(r'\section{The arithmetic still to be written out}')
b=main.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}
Section~\ref{sec:dependency-audit-v43} gives the current complete selected
register. The new integral type, decomposition, arithmetic fiber and
finite local chapters are available at their explicitly stated scopes.
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
a=main.index('Start with the version-0.42 audit in',main.index(r'\section{Claim ledger and reading order}'))
b=main.index('RF16 correction.',a)+len('RF16 correction.')
main=main[:a]+r'''Start with the version-0.43 audit in
Section~\ref{sec:dependency-audit-v43}. The new chapters are ITA
(integral types), ADP and CFD (actual automorphic and classical
decomposition), AFS (dense arithmetic fibers and separation), and FLC
(the selected finite local weight theorem). CMP1--CMP6 give the inherited
complete conditional terminal deduction. All named dependencies and
their exact source and proof ranges are recorded in the current ledger.
All historical chapters remain available, including the preserved
RF16 correction.'''+main[b:]
(ROOT/'RH_readable_reconstruction_v0_43.tex').write_text(main)
preamble=prefix[:prefix.index(r'\begin{document}')]
new_title=r'''\begin{document}
\begin{center}
{\LARGE\bfseries RH and Dirichlet GRH: new reconstruction chapters}\\[7pt]
{\large Version 0.43 --- 23 November 2026}\\[5pt]
{\large Integral types, arithmetic fibers, and finite local weights}
\end{center}
\textbf{Scope.} This edition contains the current audit and the five new
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
(ROOT/'RH_new_proofs_v0_43.tex').write_text(short)

txt=['RH AND DIRICHLET GRH — DEPENDENCY AUDIT v0.43','23 November 2026','',CFG['status'],'',
     'SOURCE PIN',CFG['source_commit'],'','INVENTORY',
     f"New claims: {ST['new_claims']}; cumulative claims: {ST['cumulative_claims']}.",
     'Selected graph:121 nodes,161 edges.31 whole obligations remain:22 C+9 B.24 shared RH/GRH;7 extra Dirichlet-GRH;0 RH-only.',
     'No whole selected leaf is newly closed. Completed nested theorems are recorded separately. Inventory is not a percentage of completion.','',
     'NEW PROVED RESULTS']
for i,s in enumerate(CFG['local_conclusions'],1):txt += [f'{i}. {s}','']
txt += ['COMPLETE CURRENT WHOLE-OBLIGATION REGISTER','']
for i,r in enumerate(REG['records'],1):
    txt += [f"{i:02d}. {r['id']} — {r['category']} — {r['title']}",'Contract: '+r['contract']]
    if r.get('bindings'):txt+=['Shared objects and choice order: '+'; '.join(r['bindings'])]
    for version in ['0_43','0_42']:
        p=r.get('version_'+version+'_progress')
        if p:
            txt+=['Version '+version.replace('_','.')+' completed inputs: '+', '.join(p['completed']), 'Remaining at that checkpoint: '+p['remaining']]
            break
    for e in r.get('evidence',[]):txt+=['Source: '+e.get('declaration','')+' — '+e.get('url',e.get('path',''))]
    txt.append('')
txt+=['NEXT LARGE ENDPOINTS']+CFG['remaining_major_inputs']+['','VALIDATION SCOPE',
 'See validation_v0_43.json, tex_validation.json and hash-bound independent mathematical and integration reviews. TeX compilation checks syntax and references; no PDF visual review or formal replay is claimed.']
(ROOT/'RH_dependency_audit_v0_43.txt').write_text('\n'.join(txt)+'\n')

readme=['# RH and unrestricted Dirichlet-GRH reconstruction — v0.43','','23 November 2026','',CFG['status'],'',
 '## Reading order','','1. `RH_reconstruction_progress_v0_43.txt`: substantive progress, mathematical ideas and exact next suppliers.',
 '2. `RH_new_proofs_v0_43.tex`: current audit and all five new chapters.',
 '3. `RH_readable_reconstruction_v0_43.tex`: complete cumulative manuscript.',
 '4. `RH_dependency_audit_v0_43.txt`: all31 remaining selected contracts and current progress.',
 '5. `continuation_checkpoint.json`, `next_source_targets.json`, `provenance.json`, and `dependency_audit_v0_43/`: exact continuation records.','',
 '## Current scope','',f"{ST['new_claims']} new claims; {ST['cumulative_claims']} cumulative claims. The selected graph retains121 nodes and161 edges, with31 whole obligations open (22 C,9 B). No whole leaf is newly closed. The new exact nested endpoints are specified in increment_v0_43.json.",
 '','The original coefficient rings and embeddings, prime3, both rank-four Links, the same J, one common coefficient threshold, and original metrics/lattices/measures remain in scope.','',
 '## New chapters','']+['- `'+c+'/main.tex`' for c in CFG['components']]+['',
 '## Provenance, review and history','',
 'Every new claim has exact proof and source ranges with hashes. New cited source files are distributed in source_snapshot_v0_43; all source bytes equal the pinned git blobs. Published inputs are explicitly identified and matched. The mathematical dependency DAG is not a mechanically extracted Lean dependency audit.','',
 'Independent mathematical reviews and the integration audit are hash-bound. Draft TeX compilation checks syntax and references. No Lean replay or PDF visual certification is asserted.','',
 'All predecessor claim records and historical proof chapters are preserved. Mutable v0.42 root metadata is frozen in history/version_0_42. SHA256SUMS covers the distributed files. Integration, assembly, validation and packaging scripts are included.','',
 'Source pin: `'+CFG['source_commit']+'`.','']
(ROOT/'README.md').write_text('\n'.join(readme))
print(json.dumps({'main_bytes':len(main.encode()),'increment_bytes':len(short.encode()),'new_claims':ST['new_claims'],'open_count':ST['open_count']},indent=2))
