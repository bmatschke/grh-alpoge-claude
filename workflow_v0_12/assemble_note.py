"""Assemble v0.12 while retaining the preceding mathematical proofs."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]
s = (BASE / 'output/pdf/RH_readable_reconstruction_v0_11.tex').read_text()

def sub(old, new):
    global s
    assert old in s, old[:180]
    s = s.replace(old, new)

s = s.replace('version 0.11', 'version 0.12').replace('version-0.11', 'version-0.12')
sub(r'{\large From local certificates to arithmetic families}\\[-1pt]',
    r'{\large Selecting the actual tops and identifying the local places}\\[-1pt]')
sub(r'{\large Uniform parameters, finite places and one global degree choice}\\[8pt]',
    r'{\large Biased probabilities, arithmetic hosts and Frobenius orbits}\\[8pt]')
a = s.index(r'\textbf{What version 0.12 achieves.}')
b = s.index('\n\\end{minipage}', a)
s = s[:a] + r'''\textbf{What version 0.12 achieves.} One biased selected set now has the required character-coset shares and small weighted bad-orbit count, and is installed as the actual host's tops. The separate set with no short linear relations is constructed explicitly. The remaining host assembly is proved from precisely stated field and analytic inputs. Frobenius orbits are identified with all actual local places, with compatible completions, lattice frames and an integral away character. Both earlier local theorems and the global degree choice are preserved. The global comparison, field/point construction and independent spectral, metric, cohomological and prime-selection arguments remain explicit. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.''' + s[b:]

components = [
    ('biased_orbits', 'biased-orbit-probability'),
    ('balanced_tops', 'balanced-tops'),
    ('host_tops', 'actual-host-tops'),
    ('local_identifications', 'actual-local-places'),
]
parts = []
for directory, cite in components:
    part = (BASE / 'v0_12' / directory / 'main.tex').read_text()
    # Typesetting normalization only: preserve the component source bytes.
    for old, new in [(r'{g\choose b}', r'\binom{g}{b}'),
                     (r'{g\choose j}', r'\binom{g}{j}'),
                     (r'{L_2\choose K}', r'\binom{L_2}{K}')]:
        part = part.replace(old, new)
    part += r'\noindent\textit{Primary source route.}\cite{' + cite + '}\n'
    parts.append(part)
sub(r'\section{Why simultaneous local exceptions have product size}',
    '\n\n'.join(parts) + '\n\n' + r'\section{Why simultaneous local exceptions have product size}')

sub('''eventually. This is a simultaneous weighted abundance statement. If this
subset is the actual host subset, it is exactly \\texttt{adm2}; for an
arbitrary supplied host, that identification remains to be proved.''',
    '''eventually. This is a simultaneous weighted abundance statement.
BO and BS below extend the construction to the host's biased probabilities
and coset shares. HC identifies the selected set with the actual host
subset and proves the exact \\texttt{BadOK}/\\texttt{ChosenBad} transfer.''')
sub('''remaining global objects together. GII proves a uniform Bernoulli
selection; the host also needs its biased coset selection and
\\texttt{Frame.Shares}. GW proves the degree choice, and HW follows its
actual preselection and family transport. BC's ring identifications''',
    '''remaining global objects together. GII proves uniform Bernoulli
selection; BO/BS now prove the biased selection and exact
\\texttt{Frame.Shares}, and HC installs them in the host.
GW proves the degree choice, and HW follows its actual preselection
and family transport. LI constructs local-place, completion and
integral-character identifications for the supplied global data.
BC's ring identifications''')
sub('''problem. Arithmetic host existence, the biased top-set
\\texttt{Frame.Shares} condition, and the supplied point/numerical
construction are separate remaining obligations.''',
    '''problem. BO/BS/HC below supply the biased tops and
\\texttt{Frame.Shares}, and expand the conditional host assembly.
The underlying field and analytic inputs, together with the actual
point/numerical construction, remain separate obligations.''')

a = s.index(r'\item[Construct one family realizing all the selected data.]')
b = s.index(r'\item[Theta identities', a)
s = s[:a] + r'''\item[Construct one family realizing all the selected data.]
The two local theorems remain complete under their literal hypotheses.
GI/GII derive their numerical, window, band and per-good-orbit inputs
uniformly from supplied \texttt{FamP} data. BC proves finite coefficient
extension and the actual \texttt{StdSubAt} coefficient subring; GJ proves
the exact \texttt{OrbitLatticeBounds} application.

BO/BS now prove the biased top selection, exact \texttt{Frame.Shares}
and simultaneous weighted bad-orbit bound. HC installs this same set
in the host, constructs the separate no-relation set with $C_{T_2}=64$,
and proves the conditional \texttt{hostOfFieldOf}/character-window
assembly. Its remaining inputs are the actual \texttt{HostAx}/character
field and rank suppliers, \texttt{ShortNorm}, \texttt{SmallOne},
\texttt{ThinH}, \texttt{PairEx} and the cohomological window.
The predicate \texttt{HostParam.Seam.admitted} itself is constructed
from the supplied host fields; it is not an additional open interface.
The actual point constructor and its \texttt{NumAt} record also remain.

LI proves the compatible local places, completions, position identities,
lattice frames and integral away character for those supplied data.
The common global frame, class-rank equality and global comparison-lattice
span must still be proved for the same objects. GW/HW already select
one degree pair at the host and rebuild all distinguished positions,
yielding \texttt{ChosenWall}. \texttt{CoverAll} and \texttt{IsRecCEv}
remain optional sufficient interfaces.
\textsf{[GI1--8, GII1--10, BC1--8, GJ1--5, GW1--6, HW1--3,
BO1--5, BS1--7, HC1--10, LI1--8]}

''' + s[b:]
a = s.index(r'\paragraph{The next target: joint arithmetic realization.}')
b = s.index(r'\section{Claim ledger', a)
s = s[:a] + r'''\paragraph{The next target: the global comparison and underlying arithmetic inputs.}
The finite biased selection and actual local-place identification no
longer remain unexplained interfaces. Next construct the common global
frame and prove the actual class-rank and comparison-lattice identities;
then supply the point constructor and its numerical record. In parallel,
expand the field/different-ideal construction and the analytic prime
inputs retained in HC. The independent cohomological, metric and
theta/spectral branches remain as stated above. The checkpoint gives
exact source targets and keeps conditional assembly separate from
the construction of its hypotheses.

''' + s[b:]
sub(r'GII1--10 & Actual Type-II family supply & Good-orbit count, all numerical fields, local application and conditional probability; existential tops selection keeps the host-identification boundary.\\[3pt]',
    r'GII1--10 & Actual Type-II family supply & Good-orbit count, all numerical fields, local application and uniform probability; BO/BS/HC now supply the biased host selection.\\[3pt]')
row = r'HW1--3 & Actual degree realization & Exact point/host WReq--WOK transfer, fixed-pair rebuilding and ChosenWall--ChosenWS; host and point construction remain supplied.\\[3pt]'
sub(row, r'''HW1--3 & Actual degree realization & Exact point/host WReq--WOK transfer, fixed-pair rebuilding and ChosenWall--ChosenWS; HC now expands the conditional host assembly.\\[3pt]
BO1--5 & Biased orbit probability & Forced-point conditioning, empty and parity-marked cells, uniform $C_bx^{-2}$ badness bound and actual orbit transport.\\[3pt]
BS1--7 & One balanced set of tops & Simultaneous variance/bad-mass selection, exact $4:3$ shares, prime-weighted bound and Fourier explanation.\\[3pt]
HC1--10 & Actual host and family join & Literal tops, no-relation set with $C_{T_2}=64$, elementary prime/field joins and conditional host/window assembly; analytic and field inputs retained.\\[3pt]
LI1--8 & Actual local identifications & All local places, completions, parity-correct positions, local lattice frames and integral away character; global frame/rank/comparison retained.\\[3pt]''')
a = s.index('For the global spine, read Sections~')
b = s.index('\n\nEvery earlier claim ID', a)
s = s[:a] + r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For the new finite selection,
start with BS in Section~\ref{sec:balanced-tops}, then HC in
Section~\ref{sec:host-tops} for its actual arithmetic use.
BO supplies the conditional orbit probability, including the parity
issue. LI in Section~\ref{sec:local-identifications} gives the local
places and maps explicitly. The four expanded companions contain
the detailed probability, numerical and algebraic calculations.

GJ4--GJ5 in Section~\ref{sec:family-join} apply the local theorems;
GW/HW in Sections~\ref{sec:global-weight-choice}--\ref{sec:host-weight-join}
select and realize the global degrees. GI/GII give their uniform
numerical inputs, and BC the coefficient rings and finite extension.
The complete local Type-I theorem is TC6 in
Section~\ref{sec:type-one-closure}; the complete local Type-II theorem
remains Corollary~\ref{cor:typeII}. JR, LW and LC/SR convert local
tests to integral costs. The ordinary and general-character host
sections distinguish their arithmetic specializations. Historical
reports retain their wording; current annotations and the continuation
checkpoint explain which earlier boundaries have been discharged.''' + s[b:]

bib = r'''
\bibitem{biased-orbit-probability} \src{Development/AutomorphicArithmetic/ThickFrames/MarkedLow.lean}{MarkedLow.lean}; \src{Development/AutomorphicArithmetic/ThickFrames/orbitTerms.lean}{orbitTerms.lean}; \src{Development/AutomorphicArithmetic/ThickFrames/orbitSum.lean}{orbitSum.lean}. BO proves the literal biased conditional estimate, marked-tile lower bound and transport to the prescribed based orbit.
\bibitem{balanced-tops} \src{Development/AutomorphicArithmetic/ThickFrames/select.lean}{select.lean}; \src{Development/AutomorphicArithmetic/ThickFrames/SharesOfCounts.lean}{SharesOfCounts.lean}; \src{Development/AutomorphicArithmetic/ThickFrames/topsGroup.lean}{topsGroup.lean}. BS gives one simultaneous choice with the exact host coset shares, cardinality and weighted bad mass; its Fourier calculation explains the character weights.
\bibitem{actual-host-tops} \src{Development/AutomorphicArithmetic/ThickFrames/topsChoiceH.lean}{topsChoiceH.lean}; \src{Development/AutomorphicArithmetic/CoprimeRanks/SecondSetNoRelation.lean}{SecondSetNoRelation.lean}; \src{Development/AutomorphicArithmetic/ShortNorms/hostOfFieldOf.lean}{hostOfFieldOf.lean}; \src{Development/AutomorphicArithmetic/ShortNorms/supplyOfAdmOf.lean}{supplyOfAdmOf.lean}. HC constructs the actual tops and no-relation set and expands the finite/algebraic host assembly; its field and analytic inputs are stated explicitly.
\bibitem{actual-local-places} \src{Development/AbelianVarietyTheory/Proofs/SatakeParameters/ExistsPlTieOfInertCore.lean}{ExistsPlTieOfInertCore.lean}; \src{Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsCompletionEquiv.lean}{ExistsCompletionEquiv.lean}; \src{Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLocIdOfCompletions.lean}{ExistsLocIdOfCompletions.lean}; \src{Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/AddCharIsIntegral.lean}{AddCharIsIntegral.lean}. LI gives the exact local-place bijection, completions, splitting, frame, position compatibility and integral inverse character for the supplied data.
'''
sub(r'\end{thebibliography}', bib + '\n' + r'\end{thebibliography}')
assert len(re.findall(r'(?<!\\)\\\[', s)) == len(re.findall(r'(?<!\\)\\\]', s))
out = BASE / 'output/pdf/RH_readable_reconstruction_v0_12.tex'
out.write_text(s)
print({'output': str(out), 'whitespace_words': len(s.split()), 'new_claims': 30})
