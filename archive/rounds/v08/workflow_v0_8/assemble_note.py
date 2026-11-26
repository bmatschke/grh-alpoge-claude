"""Assemble v0.8, preserving earlier proofs and updating their exact boundary."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]
s = (BASE / 'output/pdf/RH_readable_reconstruction_v0_7.tex').read_text()

def sub(old, new):
    global s
    assert old in s, old[:180]
    s = s.replace(old, new)

s = s.replace('version 0.7', 'version 0.8').replace('version-0.7', 'version-0.8')
sub(r'{\large A quantitative theorem for the actual selected symbols}\\[-1pt]',
    r'{\large A complete local Type-II construction}\\[-1pt]')
sub(r'{\large From integral path bases to a complete local rank estimate}\\[8pt]',
    r'{\large With a separate reconstruction of the rank-one branch}\\[8pt]')
a = s.index(r'\textbf{What version 0.8 achieves.}')
b = s.index('\n\\end{minipage}', a)
s = s[:a] + r'''\textbf{What version 0.8 achieves.} The local Type-II theorem now has a human proof under its literal orbit and weight hypotheses. We construct its full periodic frames, match every chain and degree budget, prove the additional outgoing realization, and assemble the primitive cloud and all edges. The cloud constants are $10$ and $54$; $C\ge4129$ suffices for the final local conclusion. A separate Type-I section proves the gamma-polynomial identities, logarithmic integrality and polynomial-matrix averaging, while retaining its unfinished Gram and lifting inputs explicitly. Major global analytic and cohomological work also remains. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}. Earlier proofs and source records are preserved.''' + s[b:]

sub('The pointwise local tests and selected-symbol rank are now reconstructed below; constructing compatible numerical data on every edge remains separate.',
    r'The pointwise local tests and selected-symbol rank are reconstructed below; Sections~\ref{sec:frame-geometry}--\ref{sec:edge-assembly} now supply their compatible data and the full Type-II edge theorem.')
sub('complete parameter supply remains separate;',
    r'the local parameter construction is now supplied in Sections~\ref{sec:frame-geometry}--\ref{sec:edge-assembly};')
sub('full parameter supply stays separate.',
    r'Sections~\ref{sec:frame-geometry}--\ref{sec:edge-assembly} now supply the full local Type-II parameter matching. Global abundance of the required orbits remains separate.')
sub('The selected-symbol rank is now proved in RK under its exact data; complete numerical frame supply and compatibility remain explicit inputs.',
    'The selected-symbol rank is proved in RK; FG/OR/CP/EA below supply the complete local frame, outgoing realization and numerical compatibility.')
sub('RK now supplies quantitative selected-symbol rank. Complete frame/parameter supply and matching the hypotheses of all pointwise constructions remain for the full Type-II theorem.',
    'RK supplies quantitative selected-symbol rank. FG constructs the actual frames, OR supplies the additional outgoing realization, CP matches all pointwise budgets, and EA proves the full Type-II conclusion below.')
sub('Complete numerical frame supply and compatibility remain separate.',
    r'FG/OR/CP/EA below supply the full local Type-II frame construction, realization and numerical compatibility.')
sub('Supplying the global\nframe and parameter data remains a separate step.',
    'FG/CP/EA below supply the actual local frames and compatible parameters;\nglobal abundance of the required orbit data remains a separate step.')
sub('constructing the data needed by the full local theorem remains separate.',
    'FG/OR/CP/EA below construct and match the data needed by the full local Type-II theorem.')
sub('No claim of global parameter existence enters this proof. In particular\nthe separate $r=1$ construction, the matching of all numerical data to\nthe full Type-II hypotheses, and the arithmetic windows for RH and\nDirichlet GRH remain as stated in Section~\\ref{sec:remaining}.',
    r'''The following FG/OR/CP/EA sections now match these data to the full
local Type-II hypotheses. Global abundance and simultaneous parameter
existence, the separate $r=1$ construction, and the arithmetic windows for
RH and Dirichlet GRH remain as stated in Section~\ref{sec:remaining}.''')

components = [
    ('frame_geometry', 'frames-actual'),
    ('outgoing_realization', 'outgoing-actual'),
    ('cloud_parameters', 'cloud-actual'),
    ('edge_assembly', 'edges-actual'),
    ('type_one', 'type-one-actual'),
]
parts = []
for component, cite in components:
    part = (BASE / 'v0_8' / component / (component + '_section.tex')).read_text()
    if component == 'edge_assembly':
        part += r'''
\begin{corollary}[The actual local Type-II theorem]\label{cor:typeII}
Under the literal Type-II coefficient, orbit and weight hypotheses,
with the numerical inequalities (EA.2), every $C\ge4129$ gives the
source's full \texttt{ConclusionE}. In its \texttt{LPprime} output,
the rank loss is at most $CNr^2k/Y$, the denominator exponent is $D_p$,
and other-edge errors have order $c_*$. One may use every integer height
\[
 t\ge CrN\left(\frac{CN_1^2\log(a)\,a}{pk}
                  +ap^{-L_1}+kQ+c_0\right)+2rn'c''.
\]
\end{corollary}
\begin{proof}
CP8 proves the uniform \texttt{CloudStep}$(C,10,54,1088)$ for
$C\ge4129$, using OR's proved threshold $100$. Substitute
$(C_{\rm cloud},A,B)=(4129,10,54)$ in the edge-assembly theorem.
Every threshold is fixed before choosing the local field, orbit, weights,
target lattice or primitive coefficient array. This discharges the
cloud premise within this reconstruction. \textsf{[CP8, EA9]}
\end{proof}
The result constructs the local objects from valid input data. It leaves
the global selection and abundance of such data to the arithmetic part
of the RH/GRH argument.
'''
    part += r'\noindent\textit{Primary source route.}\cite{' + cite + '}\n'
    parts.append(part)
marker = r'\section{Why simultaneous local exceptions have product size}'
sub(marker, '\n\n'.join(parts) + '\n\n' + marker)

sub('The remaining parameter and Type-I inputs are listed in Section~\\ref{sec:remaining}.',
    r'The local Type-II input is now proved in Corollary~\ref{cor:typeII}; the remaining Type-I and global inputs are listed in Section~\ref{sec:remaining}.')
sub('For $r\\ge2$, the pointwise symbol-rank, realization and dual-test arguments are now available, including the complete selected-symbol rank theorem RK. Their full numerical compatibility and frame construction must still be supplied on each edge. The separate $r=1$ treatment and its averaged bound on $\\kappa$ remain. These claims are not inferred merely from counting planes.',
    r'For $r\ge2$, FG/OR/CP/EA now prove the full local Type-II input, including frames, selected-symbol rank, outgoing realization, primitive dual tests and all numerical compatibility. The separate $r=1$ treatment has the polynomial and averaging proofs TI below its own hypotheses; its restricted Gram, simultaneous-partner, dimension and paired-lift bridges remain. Neither conclusion is inferred merely from counting planes.')
sub('IN/WT prove incoming membership and RK proves the selected-symbol rank; the parameter compatibility and separate Type-I obligations remain.',
    'IN/WT prove incoming membership, RK proves the selected-symbol rank, and FG/OR/CP/EA supply the entire local Type-II theorem. The separate Type-I and global arithmetic obligations remain.')
sub(r'\item[Supply compatible Type-II data and reconstruct Type I.]',
    r'\item[Complete the separate Type-I construction.]')
old = 'The local pointwise chain now includes IP\'s integral path realization, IW\'s normalized duality, CB\'s complementary basis and Cartan span, IN/WT\'s incoming membership, PG\'s Gram construction, and DT\'s outgoing test assembly. CG/LA/GP/RS now complete the selected-symbol density proof, and RK gives all rank, basis, complement and degree clauses with witnesses $1088,1,10$. What remains locally is to construct and match the full frame, chain, degree, size and large-constant data across these supplied-data theorems. The $r=1$ route and its averaged exceptional bound also remain. \\textsf{[RK1--RK3, CL12, JR9--JR10]}'
new = r'''The Type-II local input is now complete under its literal hypotheses: FG constructs full frames, OR proves the additional outgoing realization, CP supplies the actual chains and cloud constants $10,54$, and EA gives \texttt{ConclusionE} for $C\ge4129$. The independent Type-I route now has its exact gamma degree/leading form, binomial integrality and polynomial-matrix averaging proofs. It still needs the actual restricted graded Gram bound, compatible partners across several ties, dimension-weighted segment and digit-class transfer, and paired lifts into the cleaned rank-one edge lattices. Its uniform numerical supply must then be matched to those constructions. Global abundance of valid Type-II orbits is also outside the local theorem. \textsf{[FG1--FG8, OR1--OR8, CP1--CP8, EA1--EA9, TI1--TI9]}'''
sub(old, new)
a = s.index(r'\paragraph{The next local target.}')
b = s.index('\n\\section{Claim ledger', a)
s = s[:a] + r'''\paragraph{The next local target.}
Prove the restricted graded initial-Gram estimate and its compatible
integral partners for the actual Type-I segment spaces. Then carry these
through several ties and the dimension-weighted digit-class comparison,
and construct the paired cleaned lifts. TI3--TI5 should be used as proved
inputs, as should the complete Type-II theorem. The cohomological windows
and the theta/spectral arithmetic remain independent major branches.
''' + s[b:]
sub('Quantitative dimension is supplied by RK; parameter compatibility remains separate.',
    'RK supplies dimension; FG/OR/CP/EA complete local Type-II compatibility.')
sub('RK supplies symbol rank; complete parameter supply remains.',
    'RK supplies symbol rank; CP proves the actual cloud with constants $10,54$.')
row = r'RK1--3 & Quantitative selected-symbol theorem & Every local rank, primitive-basis, complement and degree clause proved with constants $1088,1,10$.\\[3pt]'
sub(row, row + r'''
FG1--8 & Actual periodic frames & Complete FramesOK, cyclic wrap, strong gaps, span and counts proved from OrbitHyp.\\[3pt]
OR1--8 & Outgoing integral realization & Determinant extraction and exact monPh lift proved under the actual hypotheses for $C\ge100$.\\[3pt]
CP1--8 & Actual chain and cloud parameters & Floor-correct margins, signed-chain constructor, $50L$ flat and $54L$ cloud costs, and height constant $10$ proved.\\[3pt]
EA1--9 & Full local Type-II theorem & All compatibility, realization, primitive edge tests and assembly proved; final threshold $C\ge4129$.\\[3pt]
TI1--9 & Separate rank-one branch & Gamma degree/leading form, integrality and polynomial averaging proved; actual Gram, partners, weighted transfer and lifts remain.\\[3pt]''')
a = s.index('For the global spine, read Sections~')
b = s.index('\n\nEvery earlier claim ID', a)
s = s[:a] + r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For this version's main result,
start with the edge-assembly theorem and Corollary~\ref{cor:typeII}, then
read FG, OR and CP for the construction and parameter matching. They use
the earlier local chain EL, SY/IP, IW/CB/CL, IN/WT, PG/DT, SD and
CG/LA/GP/RS/RK. JR, LW and LC/SR turn those local tests into integral
cost estimates. TI is an independent branch; its completed polynomial
mechanism and its unfinished representation inputs are kept separate.
The ordinary and general-character host sections explain the two
arithmetic specializations. Expanded companions retain the longer
calculations and exact source records.''' + s[b:]

bib = r'''
\bibitem{frames-actual} \src{Formalism/SharpRestriction/GrowthBounds/WittFrameLocaliserOrders.lean}{WittFrameLocaliserOrders.lean}. Full periodic frames, strict spans, gaps and counts, reconstructed in FG.
\bibitem{outgoing-actual} \src{Formalism/SharpRestriction/GrowthBounds/SourceCleaning.lean}{SourceCleaning.lean}; \src{Formalism/SharpRestriction/GrowthBounds/PathWeight/PhProdShift.lean}{PhProdShift.lean}; \src{Formalism/SharpRestriction/GrowthBounds/PathWeight/FixedSymbolFactorIntegral.lean}{FixedSymbolFactorIntegral.lean}. Actual outgoing determinant extraction and one-sided realization, reconstructed in OR.
\bibitem{cloud-actual} \src{Formalism/SharpRestriction/GrowthBounds/DiagonalSupport/LeOfOneLeMul.lean}{LeOfOneLeMul.lean}; \src{Formalism/SharpRestriction/GrowthBounds/DualFockLinear/TestSideExplicitIdentification.lean}{TestSideExplicitIdentification.lean}. Actual numerical chain data, normalized flat tests and uniform cloud, reconstructed in CP.
\bibitem{edges-actual} \src{Formalism/SharpRestriction/GrowthBounds/ScaleEdges/ManyEdges.lean}{ManyEdges.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ScaleEdges/InitialLevelMonoWeights.lean}{InitialLevelMonoWeights.lean}. Literal Type-II hypotheses and final uniform edge assembly, reconstructed in EA.
\bibitem{type-one-actual} \src{Formalism/SharpRestriction/GrowthBounds/ObjSeg.lean}{ObjSeg.lean}; \src{Formalism/MahlerMeasure/MahlerMeasureProofs/GamDeg.lean}{GamDeg.lean}; \src{Formalism/MahlerMeasure/MahlerMeasureProofs/GamLead.lean}{GamLead.lean}; \src{Formalism/MahlerMeasure/MahlerMeasureProofs/WindowAP.lean}{WindowAP.lean}; \src{Formalism/SharpRestriction/GrowthBounds/ProjectionLemmaBaseLevel.lean}{ProjectionLemmaBaseLevel.lean}. Actual Type-I segment, contraction polynomials, matrix averaging and final local interfaces.
'''
sub(r'\end{thebibliography}', bib + '\n' + r'\end{thebibliography}')

assert len(re.findall(r'(?<!\\)\\\[',s)) == len(re.findall(r'(?<!\\)\\\]',s)), 'Unbalanced display math'
out = BASE / 'output/pdf/RH_readable_reconstruction_v0_8.tex'
out.write_text(s)
print({'output': str(out), 'whitespace_words': len(s.split()), 'new_claims': 42})
