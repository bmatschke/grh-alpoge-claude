#!/usr/bin/env python3
"""Assemble the cumulative v0.31 TeX without changing historical proof chapters."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_30'
cfg=json.loads((ROOT/'increment_v0_31.json').read_text())
s=(OLD/'RH_readable_reconstruction_v0_30.tex').read_text()
s=s.replace('working version 0.30','working version 0.31').replace('Working version 0.30','Working version 0.31')
s=s.replace('A complete-proof dependency audit and five closed joins',
 'Compatible producers and completed finite arguments',1)
s=s.replace('Separate RH and Dirichlet-GRH routes, with exact remaining inputs',
 'A refined completion audit with 41 new proof claims',1)
a=s.index(r'\textbf{What version 0.30 achieves.}');b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.31 achieves.}
This version adds 41 proof claims and refines the complete-proof audit
at four shared interfaces: design existence, original local coverage,
small-level rank, and the actual second-layer ramified lattice.
The finite arguments are written out; their actual compatible
geometric, analytic and arithmetic producer premises remain explicit.

The design now has a proved three-input sufficient rule. Small-level
rank requires only original base rows and the base-tuple theta square
on one bundle. Actual local specialization supplies coverage by finite
generalized-eigenblock algebra. The integral and metrized ramified
model gives a smaller fullness route that does not require the GL4
slope estimates. Remaining GL4, GL6 and final assembly tasks are listed
individually. The I/II/V counts for RH, and additional III for general
Dirichlet targets, retain their original scopes.

An omitted $\epsilon/100$ in the historical RF16 intermediate rank
estimate is corrected in DEX11; the original word-bound conclusion
is reproved. All historical source and proof records are retained.

We accept the underlying Lean proof as fully checked and correct.
This remains \textbf{a partial human reconstruction}, with exact
remaining producer obligations and no new Lean replay.
''' +s[b:]

def mono_breaks(m):
    body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    body=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',body)
    body=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',body)
    body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
    return r'\texttt{'+body+'}'
def wraps(t):return re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,t)

marker=r'\paragraph{Current scope and historical chapters.}'
assert s.count(marker)==1
audit=(ROOT/'dependency_audit_v0_31/main.tex').read_text()
s=s.replace(marker,wraps(audit)+r'''

\paragraph{Historical version-0.30 audit.}
The next audit is retained as a historical checkpoint. Its frontier
statements are superseded precisely by Section~\ref{sec:dependency-audit-v31}
and the version-0.31 scope updates. Its conditional proofs and source
identities retain their stated hypotheses.

'''+marker,1)
s=s.replace('The version-0.30 audit below is the current boundary of this exposition.',
 'The version-0.30 audit below records the preceding boundary of this exposition.',1)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
addition='\n\n'.join((ROOT/c/'main.tex').read_text() for c in cfg['components'])+'\n\n'
s=s.replace(marker,wraps(addition)+marker,1)

a=s.index(r'\section{The arithmetic still to be written out}')
b=s.index(r'\section{Claim ledger and reading order}',a)
remaining=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

Section~\ref{sec:dependency-audit-v31} is the current completion audit.
The exact final interface remains one compatible design and nine
closed predicates. The finite design assembly, original projection
and small-level rank consumer, local coverage consumer, mass/volume
match and actual integral ramified model are now reconstructed.
Their original compatible producer data still have to be supplied.

\begin{description}[style=nextline]
\item[Common construction and actual readings.]
Construct the original recursive core and one common bundle with the
actual base rows, base theta square, local specialization, rational
row spectrum and prescribed coefficient-field period data. Complete
the three same-class design inputs, including the original rank
formula and the \texttt{TuSize} implication. QW9/MF20 already provide
the logarithmic window and TG12 the terminal-column implication;
these are no longer independent open tasks.
\item[Local arithmetic and spectral producers.]
Complete original \texttt{LinkN}, retained defect, period height,
local gain and spectral estimates. LTD closes exact transport,
SLR closes the finite base-rank consequence, and RSL closes the
actual metric transport; none constructs these arithmetic estimates
merely from the names of their source records.
\item[The remaining global proof tasks.]
Supply the original eventual ramified inclusion for fullness.
For global slope, reconstruct the actual GL4 three slots, GL6
integral and ramified operators, second-branch and composite lengths,
the required size installation, the $h_3$ finite bounds and the
final original numerical/lattice assembly. Each is listed separately
in the selected graph; the entire \texttt{link\_gl} human proof is
not declared finished.
\item[Counts on the original fields.]
RH and every power-of-two-order target retain I, II and V.
CountII needs all six \texttt{HidaPropsAlt} fields and
\texttt{P1core} on the same ideal on both original Links, after
one coefficient threshold. The CountI and CountV fields and
coefficient-prime ranges remain distinct. Unrestricted Dirichlet
targets also retain the actual Case-III/SeedIV/chain construction.
\end{description}

The next priority is the actual original base-row/base-theta producer,
with the GL6 local calculations and original rank supplier in parallel.
The same-ideal ordinary Hecke/support producer remains a substantial
independent count priority. AQ remains a proved alternative analytic
endpoint awaiting an arithmetic envelope supplier.

The RF16 intermediate inequality must be read with the explicit
correction in DEX11 and Section~\ref{sec:dependency-audit-v31}.
Its original word-bound conclusion has a complete corrected proof.

'''
s=s[:a]+wraps(remaining)+s[b:]
start=s.index(r'\section{Claim ledger and reading order}')
end=s.index(r'\end{longtable}',start)
rows=r'''
DEX1--DEX11 & Compatible design assembly & Three same-class inputs; exact thinning, denominator, rank proviso, selector and kit joins.\\[3pt]
LTD1--LTD8 & Original local and theta dictionary & Actual specialization gives finite coverage; exact maps, operators and embedded fields retained.\\[3pt]
SLR1--SLR9 & Small-level rank consumer & Exact projection and base-only theta square; actual row/theta producer retained.\\[3pt]
RSL1--RSL13 & Second layer and ramified lattice & Original mass, finite characters, integral isometry and smaller fullness cut; remaining global slots explicit.\\[3pt]
'''
s=s[:end]+rows+s[end:]
old_read=r'''Start with the version-0.30 audit in
Section~\ref{sec:dependency-audit-v30}.  Read HX for the actual host,
MT for metric transport, KA for CountI and the power-of-two-target
specialization, and ZW for the complete numerical endpoint.  AQ gives
the weaker positive-part alternative.  The earlier SX/UX/YX and QX
chapters give the complete conditional Case-II chain and its precise
remaining same-ideal ordinary-support producer.  Earlier chapters
retain their original hypotheses and provenance; the current audit
specifies which premises have subsequently been supplied.'''
new_read=r'''Start with the version-0.31 audit in
Section~\ref{sec:dependency-audit-v31}. Read DEX for compatible design
assembly and its three remaining inputs; SLR for the base-only small-rank
consumer; LTD for the exact local/row/theta dictionary and finite
coverage; and RSL for original mass, integral metrics and the smaller
fullness rule. The prior HX/MT/KA/ZW chapters give the host, metric,
count aggregation and numerical endpoint. QX/YX give the conditional
Case-II chain and its precise same-ideal producer. Historical frontier
statements are governed by the current audit and additive scope updates,
including the explicit RF16 correction.'''
assert s.count(old_read)==1
s=s.replace(old_read,new_read)
s=s.replace('with version-0.30 updates where an input','with version-0.31 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_31.tex'
out.write_text(s)
print(out.name,len(s.encode()),'bytes; historical mathematical chapters retained.')
