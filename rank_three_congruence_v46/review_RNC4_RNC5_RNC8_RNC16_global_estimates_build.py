#!/usr/bin/env python3
"""Bind the focused local-level and full trace-product review."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SRC=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha=lambda b:hashlib.sha256(b).hexdigest()
data=(HERE/'main.tex').read_bytes()
assert sha(data)=='93ab07e1a743dbdb5fb73fae95c8099a2c9888a2b8a2d3b1364eddafd5143f33'
text=data.decode()
ids=[f'RNC{n}' for n in [4,5,*range(8,17)]]
blocks={}
for cid in ids:
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert m,cid
    blocks[cid]=sha(m.group().encode())
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
AF=AV+'AutomorphicForms/'
SL=AV+'ModularityArgument/SemisimpleLevels/'
BR=AV+'BuildingsResidueChars/'
specs=[
 (AF+'BlochKatoSelmerVanishes.lean',65,116),
 (AF+'CongruenceNumberRankThree.lean',56,92),
 (AF+'CongruenceNumberRankThree.lean',107,140),
 (SL+'FlagPol.lean',17,None),
 (BR+'TracesFromEigenvaluesRank3.lean',1,None),
 (BR+'TracesFromEigenvaluesRank2.lean',1,None),
 (AF+'Classifies.lean',1,None),
 (BR+'EisensteinTraceDifferenceLogBound.lean',1,None),
 (BR+'ExistsIntEqProdOfGaloisPermutedIntegral.lean',1,None),
 (BR+'AdicNormProdLeProdOfInjectiveClasses.lean',1,None)
]
sources=[]
for rel,lo,hi in specs:
    b=(SRC/rel).read_bytes()
    assert b==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+rel]),rel
    lines=b.splitlines(keepends=True);hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines)
    sources.append(dict(path=rel,line_start=lo,line_end=hi,file_sha256=sha(b),
       range_sha256=sha(b''.join(lines[lo-1:hi])),source_commit=PIN,
       verified_equal_to_pinned_git_blob=True))
review=dict(
 schema='rh-independent-mathematical-review/1',artifact_version='0.46',
 reviewer='/root/global_estimates',component='rank_three_congruence_v46',
 status='PASS',result='PASS',
 proof_file='rank_three_congruence_v46/main.tex',
 proof_sha256=sha(data),proof_file_sha256=sha(data),
 source_commit=PIN,claims_reviewed=ids,proof_hashes=blocks,
 source_ranges_inspected=sources,
 scope='Focused independent mathematical review of RNC4-RNC5 and RNC8-RNC16. The checked published theorem application RNC1, actual newform/weight identification RNC2-RNC3 and finite catalogue RNC6-RNC7 are retained at their stated scopes; this review does not independently re-establish those foundations.',
 checks=[
  'The local character formula uses arithmetic Weil degree and the original cyclotomic convention. Compact continuous local Galois characters have unit ell-adic norm; the q-power ratio forces m_i=m_j+1 and then equality of the full continuous characters.',
  'The no-cyclotomic-quotient alternative excludes every possible nonzero monodromy entry. The potentially crystalline alternative invokes the explicitly retained full compatibility, so neither alternative introduces an ell factor outside the original M.',
  'For x in 1+M*O_v, the determinant of multiplication is congruent to 1 modulo M, including at ramified places. This gives conductor at most v(M) per finite character; n*a_v+n-1<= (2n-1)*a_v for a_v>=1. The separate a_v=0 case is treated.',
  'The generic newvector/principal-subgroup inclusion enlarges only the automorphic catalogue level to M^(2n-1); it leaves the original Galois Level predicate and coefficient-prime quantifier unchanged.',
  'The all-prime integrality argument uses a compact-image lattice away from p and both weak-admissibility slope endpoints at p. The arithmetic root intervals are [-e-1,e-1] in rank three and [-e,e] in rank two; both original integrality clauses follow.',
  'Rank-three geometric trace uses sum (q*b)^(-1), because r=rho*epsilon^(-1) gives r(geom)=q*rho(geom). Rank two uses 1+sum b^(-h) with q=p^h and the actual block positions0,2; no irreducibility of the restricted rank-two representation is assumed.',
  'Full cusp labels, rather than a single trace, classify representations. The disjoint-union choice handles the original Adm3 OR Adm2 predicate even if a representation satisfies both.',
  'For q>=7 and e>=1 the reverse triangle bound is strictly above3. Every q^e-scaled trace-gap factor is nonzero integral, and its absolute value is at most2*q^(2e).',
  'The whole indexed-orbit times label product is invariant under every complex automorphism, with multiplicities and empty sets included. It is a nonzero rational algebraic integer chosen before every later coefficient datum.',
  'Pairwise nonisomorphism gives an injection separately in each orbit fiber. Removing integral factors of norm<=1 gives the inequality in the correct direction; q^e is an ell-adic unit because ell!=p.',
  'The fixed constants c=5*(c3+c2*abs(discK)^12), A=103 depend only on K and dominate the catalogue/product bound. The literal CNR3 Frobenius inverse, discriminant factor only in Adm2, ell=3, all closures/prolongations and original quantifier order are preserved.'
 ],
 unresolved_findings=[],material_corrections_required=[],
 method='Independent human mathematical and source-interface review. No Lean replay and no new certification of the retained published theorem applications.')
out=HERE/'review_RNC4_RNC5_RNC8_RNC16_global_estimates.json'
out.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(review=str(out),sha256=sha(out.read_bytes()),claims=len(ids))))
