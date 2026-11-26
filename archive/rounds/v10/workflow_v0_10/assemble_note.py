"""Assemble v0.10 while preserving all earlier mathematical proofs."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]
s = (BASE / "output/pdf/RH_readable_reconstruction_v0_9.tex").read_text()

def sub(old, new):
    global s
    assert old in s, old[:180]
    s = s.replace(old, new)

s = s.replace("version 0.9", "version 0.10").replace("version-0.9", "version-0.10")
sub(r"{\large Type-I Gram forms, integral partners and cleaned lifts}\\[-1pt]",
    r"{\large Both local constructions, with explicit constants}\\[-1pt]")
sub(r"{\large With the completed local Type-II proof preserved}\\[8pt]",
    r"{\large The global arithmetic frontier remains explicit}\\[8pt]")
a = s.index(r"\textbf{What version 0.10 achieves.}")
b = s.index("\n\\end{minipage}", a)
s = s[:a] + r"""\textbf{What version 0.10 achieves.} The complete local Type-I theorem is now reconstructed for the source's literal input data. It includes both coarse rank estimates, harmonic density, the general-weight cloud maps, every numerical and height comparison, and one exceptional function valid in every coefficient-ring setting. Sufficient constants are $C_0\ge880$, $C_H\ge2800001$, $C=302114$. The completed local Type-II theorem is preserved. The global supply of the data, theta/spectral identities, metric comparison, cohomological windows and simultaneous prime selection still require reconstruction. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.""" + s[b:]

sub("The full rank-one local theorem still needs the coarse rank/density\nand uniform numerical inputs specified there.",
    r"The later RU/RD/HM/NP/TC sections supply the remaining local inputs and prove the full rank-one theorem in Section~\ref{sec:type-one-closure}.")
sub(r"\paragraph{TI7--TI9: the remaining bridge to the final exceptional function.}",
    r"\paragraph{TI7--TI9: the bridge to the final exceptional function.}")
sub("This final elementary transfer is proved in the companion.\nIt does not by itself establish the remaining block-density,\nharmonic-model identification or uniform-parameter hypotheses of the\nfull Type-I conclusion.",
    r"""This elementary transfer is proved in the companion. RU/RD now
prove the actual rank and density estimates; HM identifies the harmonic
objects and cloud maps; NP supplies every numerical field. TC below
assembles them into the complete local conclusion.""")
sub(r"""\paragraph{SW11: scope and the next obligation.}
This completes the integral-form and summation mechanisms.
To obtain the full Type-I exceptional-function theorem one must still
supply the coarse rank/density input (including the lower-rank half),
the full numerical parameter package and the final comparison
$t_0\le t_I$. RL and SW12 below construct the actual cleaned lifts under
literal \texttt{Std}, including their raw-lift numerical conditions.
The common implication to RH and Dirichlet GRH
also retains the global obligations listed later.""",
    r"""\paragraph{SW11: scope and the completed application.}
This completes the integral-form and summation mechanisms.
RU/RD below supply both coarse rank bounds, HM the actual harmonic
and cloud comparisons, and NP the uniform numerical package and
shifted height estimate. RL and SW12 construct the cleaned lifts
under literal \texttt{Std}. TC proves the full local exceptional-function
theorem; the global obligations are listed later.""")
sub("The uniform supply of those hypotheses and the comparison $t_0\\le t_I$\nremain separate.",
    "NP below supplies those hypotheses uniformly and proves the final shifted-height comparison.")
a=s.index(r"\paragraph{The exact local endpoint of this version.}")
b=s.index(r"\section{Why simultaneous local exceptions have product size}",a)
s=s[:a]+r"""\paragraph{The paired-lift endpoint and its application.}
RL constructs the actual paired maps into $\mathrm{CCe}$ and
$\mathrm{CCe}'$ at height $\lfloor t_0\rfloor$, with scalar
valuation at most $4\kappa_0$. The following sections prove the
remaining rank, harmonic, numerical and general-weight steps,
culminating in TC6's complete local Type-I theorem.

""" + s[b:]

components = [
    ("rank_upper","coarse-rank-upper"),
    ("rank_lower","coarse-rank-lower"),
    ("harmonic_model","harmonic-cloud-actual"),
    ("numerical_parameters","type-one-numerical"),
    ("type_one_closure","type-one-complete"),
]
parts=[]
for component,cite in components:
    part=(BASE/"v0_10"/component/"main.tex").read_text()
    part+=r"\noindent\textit{Primary source route.}\cite{"+cite+"}\n"
    parts.append(part)
sub(r"\section{Why simultaneous local exceptions have product size}",
    "\n\n".join(parts)+"\n\n"+r"\section{Why simultaneous local exceptions have product size}")

sub("the remaining Type-I and global inputs are listed", "the remaining global inputs are listed")
sub("The separate $r=1$ treatment now has the TI polynomial mechanism, GG graded Gram bound, TP simultaneous partners and exact mean, SW form/weighted-sum comparison and RL actual cleaned lifts. Its coarse rank/density and full numerical supply remain.",
    r"The separate $r=1$ treatment is now completed by RU/RD/HM/NP/TC, with the full $\texttt{Conclusion2}$ under literal $\texttt{HypI}$. The global supply of both types of local data remains.")
sub("The separate Type-I and global arithmetic obligations remain.",
    "TC now supplies the separate Type-I theorem. The global arithmetic obligations remain.")

a=s.index(r"\item[Complete the separate Type-I construction.]")
b=s.index(r"\item[Theta identities",a)
s=s[:a]+r"""\item[Supply the actual local data globally.]
Both local constructions are complete under their literal supplied
hypotheses: Type II has $C\ge4129$, and Type I has
$C_0\ge880$, $C_H\ge2800001$, $C=302114$.
The remaining task is to construct the simultaneous arithmetic data
that satisfy those hypotheses, including the Type-II orbit abundance
and the Type-I odd-power exclusion, windows and size inequalities.
The local theorems alone do not prove this global compatibility.
The finite extension to each actual place, through
\texttt{StdSubAt} and \texttt{LPBase.lpBaseChange}, is also
distinct from HM12's isomorphism invariance between allowed
coefficient-ring settings.
\textsf{[EA9, TC6]}

""" +s[b:]
a=s.index(r"\paragraph{The next local target.}")
b=s.index(r"\section{Claim ledger",a)
s=s[:a]+r"""\paragraph{The next target: from local hypotheses to global data.}
Use the completed EA9 and TC6 as inputs. Trace the actual
\texttt{HypIAt}, \texttt{HypIIAt} and
\texttt{linear\_programming\_input\_of\_hypotheses} in
\texttt{GrowthBounds/Joints.lean} to their quantitative suppliers.
The next proof must establish the required orbit and numerical
hypotheses for the same globally selected data; naming the local
theorems is no substitute for this construction.
The independent cohomological, metric and theta/spectral branches
remain as stated above. Exact source targets are retained in the
accompanying checkpoint.

""" +s[b:]
sub("TI1--9 & Rank-one polynomial mechanism & Exact gamma and averaging proofs; their former Gram and lift premises are now supplied by GG/TP/RL. Final density and numerical inputs remain.",
    "TI1--9 & Rank-one polynomial mechanism & Exact gamma and averaging proofs, now incorporated into the complete local Type-I theorem TC6.")
sub("SW1--12 & Segment forms and weights & Harmonic lattice comparison, terminal average and weighted sum proved; coarse rank retained. Literal Std gives kept-block and $t_0$ bounds.",
    "SW1--12 & Segment forms and weights & Harmonic block comparison and weighted mean proved. RU supplies coarse rank, NP the uniform hypotheses and final height.")
row=r"RL1--11 & Actual cleaned paired lifts & Factorial correction, raw tails, finite cleanup and source/dual transport proved at height $\lfloor t_0\rfloor$.\\[3pt]"
sub(row,row+r"""
RU1--11 & Coarse upper rank and HH assembly & Actual path injection, digit sum, weighted-lattice Smith selection and integral paired certificate proved.\\[3pt]
RD1--15 & Coarse lower rank and density & Weighted bad-tail count, kept injection, finite harmonic density and exact exceptional mean proved.\\[3pt]
HM1--12 & Actual harmonic and cloud maps & Integral projections, all edge normalizations, complementary contraction, tensor and coefficient-ring transport proved.\\[3pt]
NP1--9 & Uniform numerical supply & Literal Std, rounded windows, depth, conductors and shifted final height proved with explicit thresholds.\\[3pt]
TC1--6 & Full local Type-I theorem & Actual general-weight and edge assembly; Conclusion2 for $C_0\ge880$, $C_H\ge2800001$, $C=302114$.\\[3pt]""")
a=s.index("For the global spine, read Sections~")
b=s.index("\n\nEvery earlier claim ID",a)
s=s[:a]+r"""For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For the completed Type-I
result, begin with TC6 in Section~\ref{sec:type-one-closure}.
Read TC1--TC5 for its general-weight assembly, HM for the harmonic
and cloud maps, RU/RD for the two rank bounds, and NP for the
uniform numerical and height checks. GG/TP/SW/RL provide the
underlying Gram, partner and lift arguments.
The completed Type-II theorem remains Corollary~\ref{cor:typeII}.
JR, LW and LC/SR turn these local tests into integral cost estimates.
The ordinary and general-character host sections explain the two
arithmetic specializations. Expanded companions preserve the longer
calculations and exact source links; historical reports retain their
original wording, superseded only by the current boundary annotations."""+s[b:]

bib=r"""
\bibitem{coarse-rank-upper} \src{Formalism/SharpRestriction/GrowthBounds/BinomialRatio/RankOnDigitsCast.lean}{RankOnDigitsCast.lean}; \src{Formalism/SharpRestriction/GrowthBounds/BinomialRatio/ExtendedStatementOfParts.lean}{ExtendedStatementOfParts.lean}. RU proves the actual upper count, digit-to-HH dimension comparison and integral paired assembly.
\bibitem{coarse-rank-lower} \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/ThresholdDensityFacts.lean}{ThresholdDensityFacts.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/LocalHypothesisOfGlobal.lean}{LocalHypothesisOfGlobal.lean}. RD records the complete lower-rank source route and proves the density and final mean, using a shorter finite telescoping argument.
\bibitem{harmonic-cloud-actual} \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/CloudPropOfMapsRetractionBasis.lean}{CloudPropOfMapsRetractionBasis.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/RestHLTransport.lean}{RestHLTransport.lean}. HM constructs the actual harmonic and complementary-middle maps, with exact integral normalization and coefficient-ring transport.
\bibitem{type-one-numerical} \src{Formalism/SharpRestriction/GrowthBounds/BinomialRatio/ThresholdLowerBounds.lean}{ThresholdLowerBounds.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/ThresholdFixedWeightFacts.lean}{ThresholdFixedWeightFacts.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/SegStartSpec.lean}{SegStartSpec.lean}. NP supplies the literal numerical fields and the final shifted height.
\bibitem{type-one-complete} \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/CloudCount.lean}{CloudCount.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ColumnSpanDensity/LatticeCountPrimeMonoLevel.lean}{LatticeCountPrimeMonoLevel.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ProjectionLemmaBaseLevel.lean}{ProjectionLemmaBaseLevel.lean}. TC proves the actual local Conclusion2 with explicit sufficient constants, bypassing unused bundled admissibility fields.
"""
sub(r"\end{thebibliography}",bib+"\n"+r"\end{thebibliography}")
assert len(re.findall(r"(?<!\\)\\\[",s))==len(re.findall(r"(?<!\\)\\\]",s))
out=BASE/"output/pdf/RH_readable_reconstruction_v0_10.tex"
out.write_text(s)
print({"output":str(out),"whitespace_words":len(s.split()),"new_claims":53})
