#!/usr/bin/env python3
"""Build the cumulative note while retaining all prior mathematical chapters."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT/'history/version_0_29'
cfg = json.loads((ROOT/'increment_v0_30.json').read_text())
s = (OLD/'RH_readable_reconstruction_v0_29.tex').read_text()
s = s.replace('working version 0.29', 'working version 0.30')
s = s.replace('Working version 0.29', 'Working version 0.30')
s = s.replace('Closing the complete case-II count chain',
              'A complete-proof dependency audit and five closed joins',1)
s = s.replace('Actual seeds, promodularity and the remaining Hecke producer',
              'Separate RH and Dirichlet-GRH routes, with exact remaining inputs',1)
a=s.index(r'\textbf{What version 0.29 achieves.}')
b=s.index(r'\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.30 achieves.}
This version gives a connected dependency audit of the selected
complete-proof route and classifies every inherited continuation record.
It adds 26 proof claims: the original host construction from its
cohomological window, exact fractional-ideal metric transport,
the complete \texttt{PropGK}$\Rightarrow$\texttt{CorGK}$\Rightarrow$
\texttt{CountI} aggregation, the full numerical passage from a literal
tied family to the prime-sum window, and a weaker positive-part
analytic endpoint.

For ordinary RH, and more generally for a fixed target of power-of-two
order, the separate Case-III count is vacuous.  The selected cohomological
cut therefore retains only the actual I, II and V producers.  Unrestricted
Dirichlet targets still need Case III.  The same-family geometric,
local/theta, denominator and spectral arithmetic producers remain
substantial.  The next priority is their shared original-data dictionary,
not automatically the newest counting branch.

We accept the underlying Lean proof as fully checked and correct.
This remains \textbf{a partial human reconstruction}; the new audit
locates the remaining human obligations without alleging a formal gap.
''' +s[b:]
marker=r'\section{The prime sum and the exact missing arithmetic theorem}'
assert s.count(marker)==1
bridge=r'''
\paragraph{Current scope and historical chapters.}
The version-0.30 audit below is the current boundary of this exposition.
Earlier version-specific summaries and conditional arguments are retained
to preserve their provenance.  Their statements that a host, metric,
numerical gap, or Case-III premise is still open must be read with the
precise supersessions in this audit.  Closed implications retain their
actual arithmetic hypotheses.  The published applications are checked
in their stated scopes; inherited certificates are not described as new
independent reviews.  This round performs no Lean build or kernel replay.

'''
audit=(ROOT/'dependency_audit_v0_30/main.tex').read_text()
s=s.replace(marker,bridge+audit+'\n\n'+marker)
fragments=[]
for comp in cfg['components']:
    file='analytic_envelope.tex' if comp=='analytic_envelope' else 'main.tex'
    fragments.append((ROOT/comp/file).read_text())
addition='\n\n'.join(fragments)+'\n\n'
addition=addition.replace(r''' X=L.\texttt{sc}.X''(D.R.n),\quad
 T_u=(D.\texttt{mem}(u)).A.T,\quad
 \Delta_u=(D.\texttt{mem}(u)).C.\texttt{DGam},\quad
 g_0=D.\texttt{host}.g(0),\quad g_1=D.\texttt{host}.g(1),
 \quad d=D.\texttt{host}.d.''',r''' \begin{gathered}
 X=L.\texttt{sc}.X''(D.R.n),\quad
 T_u=(D.\texttt{mem}(u)).A.T,\\
 \Delta_u=(D.\texttt{mem}(u)).C.\texttt{DGam},\quad
 g_0=D.\texttt{host}.g(0),\quad g_1=D.\texttt{host}.g(1),
 \quad d=D.\texttt{host}.d.
 \end{gathered}''')
addition=addition.replace(r''' \text{for every $\eta>0$ and $Y_0$, there exists
 $Y\ge\max(2,Y_0)$ such that}\qquad
 \int_Y^{Y^{1+\delta}} H(x)_+\,x^{-\theta-1}\,dx\le Y^\eta.
 \tag{AQ.1}''',r''' \begin{gathered}
 \text{for every $\eta>0$ and $Y_0$, there exists
 $Y\ge\max(2,Y_0)$ such that}\\
 \int_Y^{Y^{1+\delta}} H(x)_+\,x^{-\theta-1}\,dx\le Y^\eta.
 \end{gathered}\tag{AQ.1}''')

def mono_breaks(m):
    body=re.sub(r'(?<=[a-z])(?=[A-Z])',lambda _:r'\allowbreak ',m[1])
    body=re.sub(r'\.(?!\\allowbreak)',lambda _:r'.\allowbreak ',body)
    body=re.sub(r'([/:])(?!\\allowbreak)',lambda m:m[1]+r'\allowbreak ',body)
    body=re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',body)
    return r'\texttt{'+body+'}'

addition=re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,addition)
marker=r'\section{Why simultaneous local exceptions have product size}'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)
a=s.index(r'\section{The arithmetic still to be written out}')
b=s.index(r'\section{Claim ledger and reading order}',a)
current=r'''\section{The arithmetic still to be written out}\label{sec:remaining}

The complete human proof remains unfinished at arithmetic producer
interfaces.  Section~\ref{sec:dependency-audit-v30} gives the current
connected audit; the following is its concise reading guide.  Every
obligation concerns the actual original fields, maps, lattices, metrics
and coefficient rings, with its uniform choices made in the required order.
These are limits of our reconstruction, under the assumed correctness
of the checked Lean proof.

\begin{description}[style=nextline]
\item[One compatible geometric family and its exact local dictionary.]
Construct the actual \texttt{DesignExists} witness and identify the
original \texttt{St}, \texttt{ColPin}, \texttt{R3.Read}, theta/local
operators, coefficient maps, row spectrum and lattice ties on that
same family.  Many individual implications are already reconstructed;
their compatible arithmetic premises remain.  The selected
\texttt{topDesWin} interface retains exactly nine \texttt{Closed}
predicates in addition to design existence, with its class inclusions
and \texttt{HypV}.  A semantic association with a shared dictionary
is not a proof that a producer's complete hypothesis list is supplied.

\item[Local denominators, coverage, retained defect and spectral comparisons.]
Supply the actual Galois denominator tables and type/theta/rank
identifications for \texttt{LinkN}; the original coverage and retained
defect inputs for \texttt{LinkEta} and \texttt{LinkIRR}; and the exact
period-height, local gain and spectral statements for
\texttt{LinkDIVt}, \texttt{LinkG} and \texttt{LinkS}.
\texttt{SmallLevelRankEq} is a bounded installation candidate after
the exact original small-level lattice is identified.  It is not
already supplied by an unrelated rank formula.

\item[Shared full-rank and global-slope arithmetic.]
Match the original \texttt{RealPlaceSecondLayerConditions},
\texttt{MassRatioUnderVolume} and \texttt{GenusMassAt} on the literal
second-layer datum.  Preserve the finite \texttt{LinkGl} installation
and its \texttt{Duty} and class hypotheses.  These producers contribute
to both retained full rank and global slope, so shared work is recorded
once.  MT has supplied the separate fractional-ideal metric and floor
transport on that same family; it is no longer an independent
unreconstructed arithmetic premise.

\item[Three count producers for ordinary RH.]
At the fixed target field $K_\chi=\texttt{Kstar}(\texttt{pK}\chi)$,
\texttt{CorGK} suffices for CountI; the stronger \texttt{PropGK}
source route remains available.  KA supplies every aggregation step.
The remaining arithmetic includes the marked automorphic input,
the exact rigidity/Kato and adjoint matches and the original uniform
rank-three congruence integer.  All hypotheses of an opaque open
\texttt{RigII} are retained; Kato alone is not a sufficient replacement.

For CountII, construct the actual rank-four ordinary Hecke ideal on
each of QX's two Links with all six \texttt{HidaPropsAlt} fields and
\texttt{P1core} on that very ideal, after one common coefficient
threshold.  QX and YX supply the full downstream
\texttt{PMExAlt}$\Rightarrow$\texttt{CountII} chain.

For CountV, supply the exact \texttt{ThmS6\_s},
\texttt{HostRigid\_s} and \texttt{HostNumber\_s} producers and the
separately identified frame, vanishing and XPP installations.
For the principal target, CountI uses $\mathbf Q(\sqrt{-7})$,
whereas the CountV endpoint uses its Gaussian/quartic character field.
The finite bad-prime set $\{3,7\}$ leaves the dyadic conductor unbounded.
A theorem restricted to coefficient primes greater than three cannot
alone cover this route.

\item[The additional Case-III branch for unrestricted Dirichlet GRH.]
KA5--KA6 remove Case III only when the fixed target has power-of-two
order, including order one.  General targets retain the actual
\texttt{SeedIVAlt}, Ctx3 promodularity and the associated rank-four
chain/component construction.  The already completed Case-II chain
does not supply those distinct hypotheses.
\end{description}

HX now supplies the literal host from \texttt{VWinAt}(401), with
cutoff $\lfloor x^{400}\rfloor$.  ZW supplies the complete numerical
deduction from the literal tied family, giving
$H_\psi(x)\le x^{1/2+(e_D+e_L+7)\varepsilon}$ and therefore
$1/2+9\varepsilon$ on the selected $(e_D,e_L)=(2,0)$ route.
There is no extra numerical-gap existence obligation after that
literal family is supplied.  Its upstream geometric slope hypothesis
remains one of the genuine arithmetic inputs.

The next reconstruction should resolve the shared actual
local/theta/operator and second-layer source identifications, then
carry a matched producer through one of the exact global predicates.
The same-ideal ordinary Hecke/support producer remains a separate deep
count task.  AQ is a fully proved weaker positive-part analytic
endpoint; until its arithmetic envelope is constructed, it is an
alternative route rather than a closed path to RH.

'''
s=s[:a]+current+s[b:]
row=r'YX1--YX2 & Complete conditional case-II count & PMExAlt gives CountII with all original point, length and coefficient quantifiers.\\[3pt]'
assert s.count(row)==1
rows=[
 r'HX1--HX4 & Original host installation & VWinAt(401) gives HostExW on the same field and pair, with cutoff400.',
 r'MT1--MT7 & Exact metric transport & Fractional-ideal index, common metrics, complete floor support and uniform LinkMu.',
 r'KA1--KA6 & CountI and target specialization & Complete PropGK-to-CountI aggregation; no Case III for power-of-two targets.',
 r'ZW1--ZW4 & Literal tied-family numerical endpoint & Complete weighted ledger and uniform error bound; exponent $1/2+9\varepsilon$ on the selected route.',
 r'AQ1--AQ5 & Positive-part analytic envelope & Fixed-stretch integral endpoint and integer interpolation; arithmetic supplier retained.'
]
s=s.replace(row,row+'\n'+'\n'.join(x+r'\\[3pt]' for x in rows))
oldcfg=json.loads((OLD/'increment_v0_29.json').read_text())
oldread=oldcfg['tex_reading_order'].strip()
assert s.count(oldread)==1
s=s.replace(oldread,r'''Start with the version-0.30 audit in
Section~\ref{sec:dependency-audit-v30}.  Read HX for the actual host,
MT for metric transport, KA for CountI and the power-of-two-target
specialization, and ZW for the complete numerical endpoint.  AQ gives
the weaker positive-part alternative.  The earlier SX/UX/YX and QX
chapters give the complete conditional Case-II chain and its precise
remaining same-ideal ordinary-support producer.  Earlier chapters
retain their original hypotheses and provenance; the current audit
specifies which premises have subsequently been supplied.''')
s=s.replace('with version-0.29 updates where an input',
            'with version-0.30 updates where an input')
s=s.replace(audit,re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,audit))
s=s.replace(current,re.sub(r'\\texttt\{([^{}]*)\}',mono_breaks,current))
out=ROOT/'RH_readable_reconstruction_v0_30.tex'
out.write_text(s)
print(out.name, len(s.encode()), 'bytes; all earlier proof chapters retained.')
