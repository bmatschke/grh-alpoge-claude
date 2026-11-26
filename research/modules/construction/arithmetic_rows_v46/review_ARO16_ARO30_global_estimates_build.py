#!/usr/bin/env python3
"""Bind the independently read row-evaluation, labels and count interface."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha = lambda b: hashlib.sha256(b).hexdigest()
data = (HERE/'main.tex').read_bytes()
assert sha(data) == '1ed4d31d5fce6de4a7cf2d9b9164722a65a6928e7e88b72950a905301030d873'
text = data.decode()
blocks = {}
for n in range(16,31):
    cid = f'ARO{n}'
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n', text, re.M|re.S)
    assert m, cid
    blocks[cid] = sha(m.group().encode())
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
R = S+'FlagStabilizerTensors/RootLatticeThresholds/'
H = S+'HaarTransversals/'
C = 'src/Formalism/SharpRestriction/CuspSpanNormBounds/'
A = 'src/Formalism/SharpRestriction/LevelLetterCocycles/'
F = 'src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'
specs = [
 (H+'RowsDef.lean',19,119),
 (S+'FlagStabilizerTensors/RowDict.lean',110,154),
 (S+'FlagStabilizerTensors/AllRowsOf.lean',18,80),
 (S+'FlagStabilizerTensors/AllRowsOf.lean',492,555),
 (S+'FlagStabilizerTensors/AllRowsOf.lean',701,747),
 (S+'FlagStabilizerTensors/AllRowsOf.lean',760,890),
 (A+'ArithmeticCylinders.lean',240,278),
 (C+'BridgeCountE.lean',289,330),
 (R+'AllRowsCountBase.lean',16,85),
 (F+'AllRowsAtRecord.lean',23,None),
 ('src/Formalism/LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',180,205),
 ('src/Formalism/LocalToGlobal/HilbertRowConditions/AllJoin.lean',14,24),
 ('src/Formalism/LocalToGlobal/HilbertRowConditions/AllJoinP.lean',18,26),
]
sources = []
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip()==PIN
for rel,lo,hi in specs:
    b=(SRC/rel).read_bytes()
    assert b==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+rel])
    lines=b.splitlines(keepends=True)
    hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines), (rel,lo,hi,len(lines))
    sources.append(dict(path=rel,line_start=lo,line_end=hi,
      file_sha256=sha(b),range_sha256=sha(b''.join(lines[lo-1:hi])),
      source_commit=PIN,verified_equal_to_pinned_git_blob=True))
review = dict(
 schema='rh-independent-mathematical-review/1',artifact_version='0.46',
 reviewer='/root/global_estimates',component='arithmetic_rows_v46',
 status='PASS',result='PASS',
 proof_file='arithmetic_rows_v46/main.tex',
 proof_sha256=sha(data),proof_file_sha256=sha(data),source_commit=PIN,
 claims_reviewed=list(blocks),proof_hashes=blocks,source_ranges_inspected=sources,
 scope='Focused independent mathematical and literal-contract review of ARO16-ARO30. ARO1-ARO15 are used as their stated prior lemmas; their proofs are covered by the separate ordinary_structure review.',
 checks=[
  'The Schur compression uses the actual Hilbert tensor, Haar measure and unit vector. Conjugate-linearity in the first scalar-product argument gives the displayed matrix-coefficient orientation and the exact rank-one compression.',
  'The evaluation inverse is defined first on the cyclic tensor span, is well-defined by the stated norm identity, and extends boundedly. It intertwines the full infinity action and evaluates at the original vector, proving both directions of RowsBij.',
  'RowsFinDim remains an explicit full original input. Its finite-dimensional specialization is used only after its gap and local-setting guards are discharged.',
  'Event sums are finite and orthogonal; ranks add on the actual intertwiner space. The semilinear RowDictTie comparison preserves the complex dimensions and handles repeated labels without requiring label injectivity.',
  'The single completed label set, its original-row injection, and event counts are chosen together before any cylinder. Good labels have exactly the original row multiplicities; only bad labels receive added rows.',
  'Every AllRows and AllJoinA field uses the same original X.B, AutTie and event kernels. The standard nontrivial finite characters, complete splitting, dimensions and universal event are kept literally.',
  'Cylinder unipotence uses the complementary prime. RedDatum keeps both congruence kernels and the actual two-prime quotient. IsCountIdem uses inverse character coefficients and the denominator mu(K(q0) intersect K(q1)), not a one-prime volume.',
  'The corrected ARO27 chooses one pair p,q from epsS and uses AutTie.eps_eq at every infinity place. The same b=L.sc.b and h=C*n^19*f^5*log(b*rd) work for both primes and every cylinder, with every original count guard.',
  'CountIdempotentsClass(PCount) remains an explicit antecedent of ARO28. The c<=c3 enlargement, nonnegativity deduced from the count inequality, positive universal Dstar, and epsilon<1 give all four CountAllRows fields.',
  'The FLC19 weight input retains its actual-rank threshold and exact normalized Dstar. ARO30 invokes GQT5 only on one common family with one common eventual threshold; it does not claim the count theorem or outer GLOBAL_RETAINED_DEFECT producer closed.'
 ],
 resolved_findings=[
  dict(claim='ARO27',kind='literal existential clarity',
       finding='SetBase requires the same pAt and qAt at every infinity place, beyond a bound on qAt.',
       resolution='The final reviewed block explicitly chooses the true/false epsS counts and invokes eps_eq to give this same pair at every place. The mathematical conclusion and hypotheses are unchanged.')
 ],
 unresolved_findings=[],material_corrections_required=[],
 method='Independent written mathematical/source-interface review. No formal replay or appeal to kernel correctness replaces a human argument.'
)
out=HERE/'review_ARO16_ARO30_global_estimates.json'
out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(review=str(out),sha256=sha(out.read_bytes()),
                     claims=len(blocks),source_ranges=len(sources))))
