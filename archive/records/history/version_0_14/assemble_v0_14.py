#!/usr/bin/env python3
"""Assemble cumulative v0.14 TeX; do not render a PDF."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'increment_v0_14.json').read_text())
old=ROOT/'history/version_0_13/RH_readable_reconstruction_v0_13.tex'
s=old.read_text()
s=s.replace(r'\usepackage{lmodern,amsmath,amssymb,amsthm,mathtools,microtype}',
            r'\usepackage{lmodern,amsmath,amssymb,amsthm,mathtools,microtype,mathrsfs}')
s=s.replace('working version 0.13','working version 0.14').replace('Working version 0.13','Working version 0.14')
s=s.replace('One global frame and the exact comparison lattice','Explicit forms, values and adelic geometry')
s=s.replace('Class ranks, integral descent and local lattice patching','Canonical refill and quantitative block parameters')
start=s.index(r'\textbf{What version 0.13 achieves.}')
end=s.index(r'\end{minipage}',start)
s=s[:start]+config['tex_front_summary']+'\n'+s[end:]

old_status=r'''The existence of the
polynomial values \texttt{ValEx}, and the simultaneous forms and carrier
data on which those values depend, remain stated inputs.'''
new_status=r'''The conditional comparison proof below retains its stated
\texttt{ValEx} premise; VE1--VE9 in Section~\ref{sec:value-existence}
now construct those polynomial values from the exact compatible global
form record. FC/CV and the adelic-geometry sections reconstruct the
specified portions of that record. Their remaining arithmetic and
geometric suppliers are recorded separately.'''
assert old_status in s
s=s.replace(old_status,new_status)

old_end=r'''Thus the remaining
comparison input is the compatible global forms/value construction,
including \texttt{ValEx} and the supply of \texttt{Joint0}, not a second
unproved integral-span assertion. For supplied \texttt{Joint0},
\texttt{SameUloc} is its literal local-subgroup equality and needs
no further theorem.'''
new_end=r'''VE now proves \texttt{ValEx} from the same global record and
supplies every field of the actual comparison hypothesis. In particular,
the existence of a representing polynomial is no longer an additional
assumption. The remaining input is the compatible global record with its
actual arithmetic and geometric construction; FC, CV and the adelic
geometry below specify which parts have been supplied. For supplied
\texttt{Joint0}, \texttt{SameUloc} is its literal local-subgroup equality
and needs no further theorem.'''
assert old_end in s
s=s.replace(old_end,new_end)

start=s.index(r'\paragraph{Exact boundary of the point construction.}',s.index(r'\label{sec:lattice-patching}'))
end=s.index(r'\section{Why simultaneous local exceptions have product size}',start)
s=s[:start]+r'''\paragraph{Updated boundary of the point construction.}
LP4 uses the local containment and commensurability assertions in
\texttt{RecOK.atT} and \texttt{LedOK}; LP5 installs the resulting
local lengths. RF below now constructs the canonical refill itself,
proves the literal conditional \texttt{exists\_ledPart}, and carries
the result into the point's lattice and height fields. The actual
\texttt{Lay}/\texttt{RecOK}/\texttt{LedOK} supply remains geometric.
RF also proves the complete block-length record \texttt{ParamsT}, seven
parameter families and the band/lambda/prime estimates. The remaining
\texttt{ParameterChoice'} conditions, \texttt{SizesAt}, and the
level/size existence suppliers are recorded there. In particular,
the selected local lattices are already patched exactly; that
patching step is not an additional open input.

'''+s[end:]

marker=r'\section{Why simultaneous local exceptions have product size}'
addition='\n\n'.join((ROOT/name/'main.tex').read_text()for name in config['tex_component_order'])+'\n\n'
fc_heading=r'\section{Constructing charts, residue functionals and Hermitian carriers}'
assert addition.count(fc_heading)==1
addition=addition.replace(fc_heading,r'''\paragraph{Using the realization theorem in the following constructions.}
The FC and NB arguments below state the initial-realizer premise at each
place where it is used. For the supplied CM and valid-decoration data,
DR3 now supplies that premise. Those conditional intermediate statements
therefore introduce no further realizability assumption in the actual
comparison. VE11 records their combined application with the original
arithmetic host and true-column law data.

'''+fc_heading)
# Editorial TeX repair only: amsmath requires the tag outside split.
# Frozen mathematical fragments and their review hashes are preserved.
tag_in_split=' \\tag{FC.40}\n\\end{split}'
assert addition.count(tag_in_split)==1
addition=addition.replace(tag_in_split,'\\end{split}\n \\tag{FC.40}')
def outer_split_tag(match):
    block=match.group()
    tags=re.findall(r'\\tag\{[^}]+\}',block)
    assert len(tags)<=1
    return block if not tags else block.replace(tags[0],'').rstrip()+'\n '+tags[0]
addition=re.sub(r'\\begin\{split\}[\s\S]*?\\end\{split\}',outer_split_tag,addition)
rf_display_end=' \\end{gathered}\nFor the divisibility assertion'
assert addition.count(rf_display_end)==1
addition=addition.replace(rf_display_end,' \\end{gathered}\n\\]\nFor the divisibility assertion')
assert addition.count(r'L.\etaSz')==1
addition=addition.replace(r'L.\etaSz',r'L.\operatorname{etaSz}')
for identifier in ['stepZeroHermitianLevel_with_formsFunctional',
                   'stepZeroHermitianLevel_uniformiser_kills_values',
                   'stepBefore_oneLevel',
                   'hermitianChart_complex_rational_integral_forms',
                   'move_down_adelic']:
    encoded=identifier.replace('_',r'\_')
    addition=addition.replace(r'\texttt{'+encoded+'}',
                              r'\texttt{'+encoded.replace(r'\_',r'\_\allowbreak ')+'}')
def break_identifier(match):
    return r'\texttt{'+re.sub(r'\\_(?!\\allowbreak)',lambda _:r'\_\allowbreak ',match.group(1))+'}'
addition=re.sub(r'\\texttt\{([^{}]*)\}',break_identifier,addition)
inline_height=r'''Replace the source-lattice field of $D$ by $N'_u$, its height field by
the prescribed $h_u=\texttt{hExpl6}(D,L,Y.X,C_{\rm sz},u)$, and its
common height allowance by'''
assert addition.count(inline_height)==1
addition=addition.replace(inline_height,r'''Replace the source-lattice field of $D$ by $N'_u$, set its height field to
\[
 h_u=\texttt{hExpl6}(D,L,Y.X,C_{\rm sz},u),
\]
and set its common height allowance to''')
assert s.count(marker)==1
s=s.replace(marker,addition+marker)

start=s.index('LI proves the compatible local places, completions, position identities',s.index(r'\section{The arithmetic still'))
end=s.index(r'\item[Theta identities',start)
s=s[:start]+config['tex_remaining_local']+'\n\n'+s[end:]
start=s.index(r'\paragraph{The next target: construct the compatible global forms and actual points.}')
end=s.index(r'\section{Claim ledger and reading order}',start)
s=s[:start]+config['tex_next_target']+'\n\n'+s[end:]

oldrow=r'''CS1--9 & Exact integral comparison & Valuation descent, odd-position Weyl/Gram compatibility, integrality equivalence, rational surjectivity and full integral span; polynomial-value construction retained.\\[3pt]
LP1--5 & Patch the selected lattices & Exact finite-place patch, local inclusion/equality and ramification-normalized length; geometric local conditions and full point construction retained.\\[3pt]'''
newrow=r'''CS1--9 & Exact integral comparison & Valuation descent, odd-position Weyl/Gram compatibility and exact integral span; VE now supplies its polynomial-value premise.\\[3pt]
LP1--5 & Patch the selected lattices & Exact finite-place patch and ramification-normalized length; RF now supplies the canonical refill and conditional point installation.\\[3pt]'''
assert oldrow in s
rows=[]
for entry in config['tex_ledger_rows']:
    rows.append(entry+'\\\\[3pt]')
s=s.replace(oldrow,newrow+'\n'+'\n'.join(rows))

start=s.index('For the global spine, read Sections~',s.index(r'\section{Claim ledger'))
end=s.index('GJ4--GJ5 in Section~',start)
s=s[:start]+config['tex_reading_order']+'\n\n'+s[end:]
s=s.replace('with version-0.13 updates where an input','with version-0.14 updates where an input')
out=ROOT/'RH_readable_reconstruction_v0_14.tex'
out.write_text(s)
print(out)
