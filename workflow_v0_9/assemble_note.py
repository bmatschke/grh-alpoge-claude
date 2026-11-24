"""Assemble v0.9, preserving the completed earlier proofs and their history."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]
s = (BASE / 'output/pdf/RH_readable_reconstruction_v0_8.tex').read_text()

def sub(old, new):
    global s
    assert old in s, old[:180]
    s = s.replace(old, new)

s = s.replace('version 0.8', 'version 0.9').replace('version-0.8', 'version-0.9')
sub(r'{\large A complete local Type-II construction}\\[-1pt]',
    r'{\large Type-I Gram forms, integral partners and cleaned lifts}\\[-1pt]')
sub(r'{\large With a separate reconstruction of the rank-one branch}\\[8pt]',
    r'{\large With the completed local Type-II proof preserved}\\[8pt]')
a = s.index(r'\textbf{What version 0.9 achieves.}')
b = s.index('\n\\end{minipage}', a)
s = s[:a] + r'''\textbf{What version 0.9 achieves.} The rank-one branch now has proofs of its actual graded Gram estimate, simultaneous integral partners, exact multiple-tie mean, harmonic block comparison and paired lifts into the cleaned edge lattices. The lift height is the source's $t_0$, and its numerical raw-tail conditions are derived from the literal standard hypotheses. A separate coarse rank/density estimate, the complete numerical parameter package and the comparison $t_0\le t_I$ remain. The local Type-II theorem from version 0.8 is preserved. Global analytic and cohomological inputs are still substantial. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.''' + s[b:]

sub('The full rank-one local theorem remains conditional on the restricted\ngraded Gram, simultaneous-partner and paired-lift inputs specified at the end.',
    r'''Sections~\ref{sec:graded-gram}--\ref{sec:paired-lifts} now supply its
actual graded Gram, simultaneous-partner and cleaned-lift inputs.
The full rank-one local theorem still needs the coarse rank/density
and uniform numerical inputs specified there.''')
sub('This keeps the integral normalization and the rounding term explicit.',
    r'''This keeps the integral normalization and the rounding term explicit.
GG below now proves the retained graded Gram premise; TP gives the
sharper source normalization and removes the rounding loss in its exact
one-tie estimate.''')
sub('Those representation and lifting inputs remain open in this reconstruction.',
    r'''Those representation and lifting inputs are now proved in GG, TP
and RL below. SW proves the form and weighted-sum mechanisms, retaining
the actual coarse rank inequality and explicitly stated numerical inputs.''')
sub('It does not by itself establish the missing representation, block-density,\nraw-lift or uniform-parameter hypotheses of the full Type-I conclusion.',
    r'''It does not by itself establish the remaining block-density,
harmonic-model identification or uniform-parameter hypotheses of the
full Type-I conclusion.''')

components = [
    ('graded_gram', 'graded_gram_section.tex', 'graded-gram-actual'),
    ('tie_partners', 'main.tex', 'tie-partners-actual'),
    ('segment_weighted', 'segment_weighted_section.tex', 'segment-weighted-actual'),
    ('segment_numerics', 'main.tex', 'segment-numerics-actual'),
    ('paired_lifts', 'paired_lifts_section.tex', 'paired-lifts-actual'),
]
parts = []
for component, filename, cite in components:
    part = (BASE / 'v0_9' / component / filename).read_text()
    part += r'\noindent\textit{Primary source route.}\cite{' + cite + '}\n'
    parts.append(part)
parts.append(r'''
\paragraph{The exact local endpoint of this version.}
Under the literal Type-I standard hypotheses, with
$C_{E1},C_{E2},C_m\ge17$ and $C_t\ge30$, RL constructs the actual
paired maps into $\mathrm{CCe}$ and $\mathrm{CCe}'$ at height
$\lfloor t_0\rfloor$, with scalar valuation at most $4\kappa_0$.
Independently, under the stated admissible segment bounds, GG and TP
prove the source's multiple-tie mean with constant $C_M=1$; SW turns it
into a weighted segment estimate conditional on the actual coarse rank
inequality (SW8.1). These two conclusions are constructions with explicit
inputs. They do not yet imply the full Type-I \texttt{Conclusion2}.
''')
marker = r'\section{Why simultaneous local exceptions have product size}'
sub(marker, '\n\n'.join(parts) + '\n\n' + marker)

sub('The separate $r=1$ treatment has the polynomial and averaging proofs TI below its own hypotheses; its restricted Gram, simultaneous-partner, dimension and paired-lift bridges remain. Neither conclusion is inferred merely from counting planes.',
    'The separate $r=1$ treatment now has the TI polynomial mechanism, GG graded Gram bound, TP simultaneous partners and exact mean, SW form/weighted-sum comparison and RL actual cleaned lifts. Its coarse rank/density and full numerical supply remain. Neither local conclusion is inferred merely from counting planes.')

old = 'The Type-II local input is now complete under its literal hypotheses: FG constructs full frames, OR proves the additional outgoing realization, CP supplies the actual chains and cloud constants $10,54$, and EA gives \\texttt{ConclusionE} for $C\\ge4129$. The independent Type-I route now has its exact gamma degree/leading form, binomial integrality and polynomial-matrix averaging proofs. It still needs the actual restricted graded Gram bound, compatible partners across several ties, dimension-weighted segment and digit-class transfer, and paired lifts into the cleaned rank-one edge lattices. Its uniform numerical supply must then be matched to those constructions. Global abundance of valid Type-II orbits is also outside the local theorem. \\textsf{[FG1--FG8, OR1--OR8, CP1--CP8, EA1--EA9, TI1--TI9]}'
new = r'''The local Type-II theorem remains complete under its literal hypotheses, with $C\ge4129$. The separate Type-I branch now has the actual graded Gram bound, compatible partners, exact weighted multiple-tie mean, integral harmonic block comparison and cleaned paired lifts. Its remaining local tasks are the coarse rank-on-digits upper and lower bounds; the harmonic-model dimension identification and KeyIneq application; the full admissible numerical package with its quantifier order; and the comparison $t_0\le t_I$ with the final exceptional-function bounds. SW8 deliberately retains its coarse rank input, so summation is not mistaken for density. RL proves the lift construction under literal Std, not the existence of all such parameters in the arithmetic application. Global abundance of Type-II orbit data also remains separate. \textsf{[EA9, TI7--TI9, GG1--GG8, TP1--TP11, SW1--SW12, RL1--RL11]}'''
sub(old, new)
a = s.index(r'\paragraph{The next local target.}')
b = s.index('\n\\section{Claim ledger', a)
s = s[:a] + r'''\paragraph{The next local target.}
Prove both clauses of the actual coarse rank-on-digits comparison,
starting from \texttt{UpAt} and \texttt{LowAt} in \texttt{RankDefs}.
Next follow \texttt{restUp\_of} in \texttt{RankOnDigitsCast}, then the
source theorem \texttt{one\_segment\_of\_upper\_lower}.
The upper clause supplies
(SW8.1); the lower clause gives the retained mass needed for Type-I
density. Then match the harmonic-model and numerical interfaces,
including $t_0\le t_I$, before applying TI7--TI8.
GG, TP, the proved SW mechanisms and RL should be reused as completed
inputs within their stated scopes. The cohomological windows and
theta/spectral arithmetic remain independent major branches.
''' + s[b:]

row = r'TI1--9 & Separate rank-one branch & Gamma degree/leading form, integrality and polynomial averaging proved; actual Gram, partners, weighted transfer and lifts remain.\\[3pt]'
sub(row, r'''TI1--9 & Rank-one polynomial mechanism & Exact gamma and averaging proofs; their former Gram and lift premises are now supplied by GG/TP/RL. Final density and numerical inputs remain.\\[3pt]
GG1--8 & Actual graded Gram lattice & Integral image lifting, highest projection and exact determinant constant proved.\\[3pt]
TP1--11 & Simultaneous tie partners & Sharp gamma integrality, compatible integral partners and literal weighted mean with $C_M=1$ proved.\\[3pt]
SW1--12 & Segment forms and weights & Harmonic lattice comparison, terminal average and weighted sum proved; coarse rank retained. Literal Std gives kept-block and $t_0$ bounds.\\[3pt]
RL1--11 & Actual cleaned paired lifts & Factorial correction, raw tails, finite cleanup and source/dual transport proved at height $\lfloor t_0\rfloor$.\\[3pt]''')
a = s.index('For the global spine, read Sections~')
b = s.index('\n\nEvery earlier claim ID', a)
s = s[:a] + r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For the new Type-I material, begin
with the endpoint of Section~\ref{sec:paired-lifts}, then read
GG for its Gram input, TP for the weighted mean, and SW for its passage
to segment blocks. The terminal polynomial average SW5 is a direct
reuse of TI5; it avoids a separate matrix-window argument.
The completed Type-II theorem remains Corollary~\ref{cor:typeII}, with
FG/OR/CP providing its construction and constants. JR, LW and LC/SR
turn the local tests into integral cost estimates. The ordinary and
general-character host sections explain the two arithmetic specializations.
Expanded companions retain the longer coefficient, factorial and
numerical calculations, with exact source records.''' + s[b:]

bib = r'''
\bibitem{graded-gram-actual} \src{Formalism/MahlerMeasure/StatementT.lean}{StatementT.lean}; \src{Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/PartnerMeanProofs/GramHypothesisOfLogBound.lean}{GramHypothesisOfLogBound.lean}. The actual restricted graded Gram hypothesis and its partner-mean interface; GG reconstructs the coefficient-image lattice argument.
\bibitem{tie-partners-actual} \src{Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/PartnerMeanProofs/GamIntC.lean}{GamIntC.lean}; \src{Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/PartnerMeanProofs/GammaZeroIntegral.lean}{GammaZeroIntegral.lean}. Sharp gamma integrality, compatible tie partners and the exact multiple-tie mean, reconstructed in TP.
\bibitem{segment-weighted-actual} \src{Formalism/MahlerMeasure/MahlerMeasureProofs/SSDirect.lean}{SSDirect.lean}; \src{Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/BlockBoundOfDualFamilies.lean}{BlockBoundOfDualFamilies.lean}; \src{Formalism/SharpRestriction/GrowthBounds/MonomialFactorials/SegmentWeightedCountingBoundOfAllRemainingBounds.lean}{SegmentWeightedCountingBoundOfAllRemainingBounds.lean}. Actual block lattices, good dual families and dimension-weighted summation, reconstructed in SW with its coarse rank input explicit.
\bibitem{segment-numerics-actual} \src{Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/PolyUpperBoundDelta.lean}{PolyUpperBoundDelta.lean}; \src{Formalism/SharpRestriction/GrowthBounds/BinomialRatio/TopDegreeLeTwoB.lean}{TopDegreeLeTwoB.lean}. Kept-block, terminal-degree and total-order estimates from the literal standard hypotheses.
\bibitem{paired-lifts-actual} \src{Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/RestBlockForm.lean}{RestBlockForm.lean}; \src{Formalism/SharpRestriction/GrowthBounds/CoarseMultiplicity/PairedLiftAtOfIdentity.lean}{PairedLiftAtOfIdentity.lean}; \src{Formalism/SharpRestriction/GrowthBounds/BinomialRatio/PairLift.lean}{PairLift.lean}. Actual factorial correction, raw polynomial tails, finite cleanup and source/dual edge pairing, reconstructed in RL.
'''
sub(r'\end{thebibliography}', bib + '\n' + r'\end{thebibliography}')

assert len(re.findall(r'(?<!\\)\\\[', s)) == len(re.findall(r'(?<!\\)\\\]', s)), 'Unbalanced display math'
out = BASE / 'output/pdf/RH_readable_reconstruction_v0_9.tex'
out.write_text(s)
print({'output': str(out), 'whitespace_words': len(s.split()), 'new_claims': 42})
