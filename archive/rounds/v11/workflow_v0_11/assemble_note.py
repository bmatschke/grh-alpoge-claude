"""Assemble v0.11, retaining every earlier mathematical proof."""
from pathlib import Path
import re

BASE=Path(__file__).resolve().parents[1]
s=(BASE/'output/pdf/RH_readable_reconstruction_v0_10.tex').read_text()
def sub(old,new):
    global s
    assert old in s,old[:180]
    s=s.replace(old,new)

s=s.replace('version 0.10','version 0.11').replace('version-0.10','version-0.11')
sub(r'{\large Both local constructions, with explicit constants}\\[-1pt]',
    r'{\large From local certificates to arithmetic families}\\[-1pt]')
sub(r'{\large The global arithmetic frontier remains explicit}\\[8pt]',
    r'{\large Uniform parameters, finite places and one global degree choice}\\[8pt]')
a=s.index(r'\textbf{What version 0.11 achieves.}')
b=s.index('\n\\end{minipage}',a)
s=s[:a]+r'''\textbf{What version 0.11 achieves.} The actual Type-I and Type-II numerical hypotheses now follow uniformly from the supplied family's size conditions. The standard coefficient subring and finite-extension argument are reconstructed, giving exact orbit certificates at actual finite places under the stated construction identifications. One global degree pair satisfies the source's $x^{-9}$ weighted exceptional-loss bound. Its actual host preselection, rebuilding and family transport are also written out. The underlying host, point and compatible local-comparison construction, together with the independent spectral, metric, cohomological and prime-selection branches, remain explicit. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.'''+s[b:]

components=[
 ('type_two_family','type-two-family'),
 ('type_one_family','type-one-family'),
 ('base_change','finite-base-change'),
 ('family_join','family-orbit-join'),
 ('global_weight_choice','global-degree-choice'),
 ('host_weight_join','host-degree-realization'),
]
parts=[]
for directory,cite in components:
    part=(BASE/'v0_11'/directory/'main.tex').read_text()
    part+=r'\noindent\textit{Primary source route.}\cite{'+cite+'}\n'
    parts.append(part)
sub(r'\section{Why simultaneous local exceptions have product size}',
    '\n\n'.join(parts)+'\n\n'+r'\section{Why simultaneous local exceptions have product size}')

sub('The global supply of both types of local data remains.',
    'GI/GII now supply the uniform numerical and good-orbit hypotheses for a supplied family, and BC/GJ give the finite-place application. Constructing all the global data together remains separate.')

a=s.index(r'\item[Supply the actual local data globally.]')
b=s.index(r'\item[Theta identities',a)
s=s[:a]+r'''\item[Construct one family realizing all the selected data.]
The two local theorems remain complete under their literal hypotheses.
GI/GII now derive their actual numerical, window, band and per-good-orbit
inputs uniformly from the supplied \texttt{FamP} data. BC proves finite
coefficient extension, and constructs \texttt{StdSubAt} for the literal
\texttt{recC} data; GJ proves the exact \texttt{OrbitLatticeBounds}
application. The words \texttt{StdSubAt} refer to a standard coefficient
subring, not a standard-submodule assertion.

The remaining construction step is to supply one arithmetic family
with these fields and identifications simultaneously. GII9--GII10
produce a uniform Bernoulli selected subset; the host additionally
needs its biased coset selection and \texttt{Frame.Shares}.
GW proves the exact weighted-loss choice. HW follows the active
route that selects the pair at the host, then rebuilds its points at
every distinguished position and obtains \texttt{ChosenWall}.
Its upstream host, point and numerical constructors remain explicit.
The compatible local places, integral characters, rank equality and
comparison-lattice span must also be constructed for those same data.
The stronger \texttt{CoverAll} and the \texttt{IsRecCEv} interface are
optional sufficient routes, not requirements imposed on the active proof.
\textsf{[GI1--8, GII1--10, BC1--8, GJ1--5, GW1--6, HW1--3]}

'''+s[b:]
a=s.index(r'\paragraph{The next target: from local hypotheses to global data.}')
b=s.index(r'\section{Claim ledger',a)
s=s[:a]+r'''\paragraph{The next target: joint arithmetic realization.}
The quantitative local hypotheses, canonical deficit, finite-place
transport, global degree averaging and active degree-realization join
are now written out. Next prove the biased coset selection and exact
\texttt{Frame.Shares}, the general-character host and point constructors,
and the compatible local place, character, rank and comparison-lattice
data. Then expand the remaining gain and prime-loss estimates on those
actual objects. The independent cohomological, metric and theta/spectral
branches remain as stated above. The checkpoint records exact source
targets, and distinguishes construction obligations from implications
already proved here.

'''+s[b:]
row=r'TC1--6 & Full local Type-I theorem & Actual general-weight and edge assembly; Conclusion2 for $C_0\ge880$, $C_H\ge2800001$, $C=302114$.\\[3pt]'
sub(row,row+r'''
GII1--10 & Actual Type-II family supply & Good-orbit count, all numerical fields, local application and conditional probability; existential tops selection keeps the host-identification boundary.\\[3pt]
GI1--8 & Actual Type-I family supply & All fourteen numerical fields, exact band/window/depth translation, cyclic time bound and canonical averaged deficit.\\[3pt]
BC1--8 & Finite places and coefficient extension & Concrete standard ring, prescribed number-field place, integral lattice/dual/clean transport and exact LPBaseChange; recC gives StdSubAt.\\[3pt]
GJ1--5 & Family orbit application & Universal infimum, explicit scale bounds, exact orbit identifications and OrbitLatticeBounds with unchanged height/depth/loss.\\[3pt]
GW1--6 & One global degree pair & Exact marginals, total prime-loss estimate, MeanEx/WReq and ChosenW; CoverAll additionally supplies a carrier.\\[3pt]''')
sub(r'GW1--6 & One global degree pair & Exact marginals, total prime-loss estimate, MeanEx/WReq and ChosenW; CoverAll additionally supplies a carrier.\\[3pt]',
    r'''GW1--6 & One global degree pair & Exact marginals, total prime-loss estimate, MeanEx/WReq and ChosenW; optional CoverAll supplies a carrier.\\[3pt]
HW1--3 & Actual degree realization & Exact point/host WReq--WOK transfer, fixed-pair rebuilding and ChosenWall--ChosenWS; host and point construction remain supplied.\\[3pt]''')

a=s.index('For the global spine, read Sections~')
b=s.index('\n\nEvery earlier claim ID',a)
s=s[:a]+r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For the new family application,
start with GJ4--GJ5 in Section~\ref{sec:family-join}, then the single
global degree choice in Section~\ref{sec:global-weight-choice} and its
actual realization in Section~\ref{sec:host-weight-join}.
GII and GI supply the two sets of quantitative hypotheses; BC supplies
the coefficient rings and finite-extension proof. Their expanded
companions preserve the longer numerical and algebraic calculations.

The complete local Type-I theorem is TC6 in
Section~\ref{sec:type-one-closure}; TC1--TC5 assemble HM, RU/RD and NP
with the earlier Gram, partner and lift arguments. The complete local
Type-II theorem remains Corollary~\ref{cor:typeII}.
JR, LW and LC/SR turn local tests into integral cost estimates.
The ordinary and general-character host sections separate the two
arithmetic specializations. Historical reports retain their original
wording, with their superseded boundaries explained by the current
annotations and continuation checkpoint.'''+s[b:]

bib=r'''
\bibitem{type-two-family} \src{Formalism/SharpRestriction/GrowthBounds/TopChoiceBounds.lean}{TopChoiceBounds.lean}; \src{Formalism/SharpRestriction/GrowthBounds/SizesAtRecord.lean}{SizesAtRecord.lean}; \src{Formalism/SharpRestriction/GrowthBounds/Joints.lean}{Joints.lean}. GII gives the actual good-orbit counts, uniform numerical supply, conditional bad-orbit probability and simultaneous tops selection.
\bibitem{type-one-family} \src{Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/MeanNum.lean}{MeanNum.lean}; \src{Formalism/SharpRestriction/GrowthBounds/Joints.lean}{Joints.lean}. GI proves every actual Type-I family inequality, the exact band and window conversion, time comparison and canonical mean.
\bibitem{finite-base-change} \src{Formalism/LocalToGlobal/GroupLattices/FockModels/LPBase.lean}{LPBase.lean}; \src{Formalism/SharpRestriction/GrowthBounds/Joints.lean}{Joints.lean}. BC constructs the standard coefficient ring and prescribed-place extension, proves exact lattice and dual transport, and identifies the recC application. Its ledger follows the concrete construction to the individual ring declarations.
\bibitem{family-orbit-join} \src{Formalism/SharpRestriction/GrowthBounds/DefsInst.lean}{DefsInst.lean}; \src{Formalism/SharpRestriction/GrowthBounds/PlaneCountTheoremWithConstants.lean}{PlaneCountTheoremWithConstants.lean}; \src{Formalism/SharpRestriction/GrowthBounds/Joints.lean}{Joints.lean}. GJ proves the universal canonical infimum, uniform scales and actual finite-place join.
\bibitem{global-degree-choice} \src{Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean}{SlopeEstimateOfLemmaBSlopeLine.lean}; \src{Formalism/LocalToGlobal/GlobalTheory/LossRequirementsOfSmallShares.lean}{LossRequirementsOfSmallShares.lean}; \src{Formalism/SharpRestriction/FamCore.lean}{FamCore.lean}. GW proves exact finite marginal averages and the single degree pair; it preserves the separate full-coverage obligation.
\bibitem{host-degree-realization} \src{Development/AutomorphicArithmetic/CharacterBoxes/HostWW.lean}{HostWW.lean}; \src{Development/AutomorphicArithmetic/CharacterBoxes/KitS.lean}{KitS.lean}; \src{Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/ExistsFamPOfKits.lean}{ExistsFamPOfKits.lean}. HW proves the active host preselection, fixed-pair rebuilding and actual family transport, keeping the upstream construction premises explicit.
'''
sub(r'\end{thebibliography}',bib+'\n'+r'\end{thebibliography}')
assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
out=BASE/'output/pdf/RH_readable_reconstruction_v0_11.tex'
out.write_text(s)
print({'output':str(out),'whitespace_words':len(s.split()),'new_claims':40})
