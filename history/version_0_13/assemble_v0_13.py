#!/usr/bin/env python3
"""Assemble the next cumulative readable note, preserving v0.12 sources."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
old=ROOT/'history/version_0_12/RH_readable_reconstruction_v0_12.tex'
s=old.read_text()
s=s.replace('working version 0.12','working version 0.13').replace('Working version 0.12','Working version 0.13')
s=s.replace('Selecting the actual tops and identifying the local places','One global frame and the exact comparison lattice')
s=s.replace('Biased probabilities, arithmetic hosts and Frobenius orbits','Class ranks, integral descent and local lattice patching')
start=s.index('\\textbf{What version 0.12 achieves.}')
end=s.index('\\end{minipage}',start)
s=s[:start]+r'''\textbf{What version 0.13 achieves.} The common global-frame algebra, the actual class-rank identity and the exact integral comparison-lattice span are now proved for the supplied compatible global forms. The odd-position comparison preserves the integral Weyl lattice, and the prescribed served/type-prime lattices are patched into one global lattice with the exact valuation normalization. The remaining simultaneous forms and polynomial-value construction is stated precisely, alongside the host/point and numerical suppliers and the independent spectral, metric, cohomological and prime-window arguments. Both earlier local theorems are preserved. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.
'''+s[end:]

old_boundary=r'''These choices can be made for all supplied words and places. A common
global frame still uses \texttt{StdTied} and \texttt{Companion}; the
class-rank equality and the actual global comparison-lattice theorem
also remain separate. Neither the existence of the host nor those
global joins follows merely from the local identifications proved here.'''
new_boundary=r'''These choices can be made for all supplied words and places. The
following SF, CR and CS sections now prove the common-frame algebra,
class-rank equality and integral comparison span under their exact
compatible-forms hypotheses. The simultaneous global construction
supplying those hypotheses remains distinct from these local
identifications; the existence of the host is not inferred from them.'''
assert old_boundary in s
s=s.replace(old_boundary,new_boundary)
marker=r'\section{Why simultaneous local exceptions have product size}'
addition='\n\n'.join((ROOT/name/'main.tex').read_text()for name in ['global_frame','class_rank','comparison_span','lattice_patching'])+'\n\n'
assert s.count(marker)==1
s=s.replace(marker,addition+marker)

start=s.index('LI proves the compatible local places, completions, position identities,',s.index(r'\section{The arithmetic still'))
end=s.index(r'\item[Theta identities',start)
s=s[:start]+r'''LI proves the compatible local places, completions, position identities
and integral away character. SF now gives one global frame and the actual
companion-lattice identity; CR gives the exact class-rank equality; CS
proves the exact integral span of the comparison image. These are proved
for the same supplied compatible forms, with \texttt{Joint0} and
\texttt{LevelZeroCharacterRational} used exactly where needed. The
simultaneous forms/value construction, including \texttt{ValEx},
\texttt{Forms0}, carrier identifications and their global arithmetic
existence, remains an input. The literal rank equality itself does not
use \texttt{Joint0}; the integral comparison does.

LP proves the finite-place patch of the selected \texttt{NP} lattices
and the separate type-prime target, together with its normalized length
installation. The supplied local containment/commensurability and the
complete canonical refill, point and \texttt{NumAt} construction remain.
GW/HW already select one degree pair at the host and rebuild all
distinguished positions, yielding \texttt{ChosenWall};
\texttt{CoverAll} and \texttt{IsRecCEv} remain optional sufficient
interfaces.
\textsf{[GI1--8, GII1--10, BC1--8, GJ1--5, GW1--6, HW1--3,
BO1--5, BS1--7, HC1--10, LI1--8, SF1--7, CR1--6, CS1--9, LP1--5]}

'''+s[end:]

start=s.index(r'\paragraph{The next target: the global comparison and underlying arithmetic inputs.}')
end=s.index(r'\section{Claim ledger and reading order}',start)
s=s[:start]+r'''\paragraph{The next target: construct the compatible global forms and actual points.}
The next step is the simultaneous standard-forms/value construction
feeding the now-proved comparison algebra, not another abstract
integral-span theorem. Its source \texttt{formsTiedSym\_std} supplies
charts, polynomial values, level characters, norm ties and class data;
\texttt{colsTiedSym\_std} carries those objects into the same global
columns. The point branch must supply the remaining canonical refill,
\texttt{RecOK}/\texttt{LedOK}, level and size records, and the stronger
\texttt{NumAt} inequalities. LP has removed its finite-place patching
step from that list. In parallel the field/different-ideal and analytic
prime inputs retained in HC, and the independent cohomological, metric
and theta/spectral branches, remain as above. The checkpoint gives
exact source targets and preserves the distinction between proving a
theorem with its literal hypotheses and constructing those hypotheses
simultaneously for the arithmetic family.

'''+s[end:]

oldrow=r'LI1--8 & Actual local identifications & All local places, completions, parity-correct positions, local lattice frames and integral away character; global frame/rank/comparison retained.\\[3pt]'
newrows=r'''LI1--8 & Actual local identifications & All local places, completions, parity-correct positions, local lattice frames and integral away character; global comparison algebra now in SF/CR/CS.\\[3pt]
SF1--7 & One global frame & Exact standard matrix, actual diagonal companion lattice and simultaneous local frame replacement; full standard-forms construction retained.\\[3pt]
CR1--6 & Actual class-rank equality & Weyl fiber ranks, class bijection, two-prime stabilizer triviality and literal pack dimension equality; no metric conclusion.\\[3pt]
CS1--9 & Exact integral comparison & Valuation descent, odd-position Weyl/Gram compatibility, integrality equivalence, rational surjectivity and full integral span; polynomial-value construction retained.\\[3pt]
LP1--5 & Patch the selected lattices & Exact finite-place patch, local inclusion/equality and ramification-normalized length; geometric local conditions and full point construction retained.\\[3pt]'''
assert oldrow in s
s=s.replace(oldrow,newrows)
start=s.index('For the global spine, read Sections~',s.index(r'\section{Claim ledger'))
end=s.index('GJ4--GJ5 in Section~',start)
s=s[:start]+r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For this increment, read
SF in Section~\ref{sec:standard-global-frame} for the common coordinates,
CR in Section~\ref{sec:class-rank} for the exact dimension, then
CS in Section~\ref{sec:comparison-span} for the integral comparison.
LP in Section~\ref{sec:lattice-patching} installs the selected local
lattices globally. Their expanded companion reports retain the full
source joins, hypotheses and simplifications. BO/BS/HC supply the
earlier finite selection and conditional host assembly; LI gives the
local places and maps that all four new sections use.

'''+s[end:]
s=s.replace('with version-0.12 updates where an input','with version-0.13 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_13.tex'
out.write_text(s)
print(out)
