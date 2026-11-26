#!/usr/bin/env python3
"""Record the root's completed independent mathematical readings and source checks."""
from pathlib import Path
import hashlib, json, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parent/'lean-source'
def sha(b): return hashlib.sha256(b).hexdigest()

def record(component, expected, findings, scope):
    base=ROOT/component
    raw=(base/'main.tex').read_bytes()
    assert sha(raw)==expected, (component,sha(raw))
    p=json.loads((base/'provenance.json').read_text())
    for f in p['source_files']:
        b=(REPO/f['path']).read_bytes()
        assert sha(b)==f['sha256'],f['path']
        assert b==subprocess.check_output(['git','-C',str(REPO),'show',p['commit']+':'+f['path']])
    for c in p['claims']:
        for s in c['sources']:
            b=(REPO/s['path']).read_bytes()
            frag=b''.join(b.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
            assert sha(frag)==s['range_sha256'],s['declaration']
        loc=c['proof_location']; b=(ROOT/loc['file']).read_bytes()
        assert sha(b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]))==loc['sha256'],c['id']
    metadata=['provenance.json','closure.json','classical_inputs.json','source_hashes.json','verification.json','tex_validation.json','input_manifest.json','remaining_inputs.json']
    out={'schema':'rh-human-reconstruction-independent-review/1','artifact_version':'0.26','date':'2026-11-22',
      'component':component,'reviewer_role':'Root integrating agent, independent of the component author',
      'reviewed_file':component+'/main.tex','review_kind':'Independent full mathematical argument and literal source-interface review',
      'status':'PASS','result':'PASS','reviewed_main_sha256':sha(raw),
      'claims':[c['id']for c in p['claims']],'reviewed_claim_ids':[c['id']for c in p['claims']],
      'reviewed_metadata':{str((base/f).relative_to(ROOT)):sha((base/f).read_bytes())for f in metadata if (base/f).is_file()},
      'mathematical_checks':findings,'unresolved_findings':[],'scope':scope,
      'verification':{'source_files':len(p['source_files']),'source_anchors':sum(len(c['sources'])for c in p['claims']),
        'proof_ranges':len(p['claims']),'all_source_files_equal_pinned_git_blobs':True,
        'all_source_range_hashes_match':True,'all_proof_range_hashes_match':True,
        'mathematical_proofs_read_in_full':True,'kernel_replay':False,'lean_build':False}}
    (HERE/(component+'_root_review.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(component, out['result'], len(p['claims']), out['reviewed_main_sha256'])

record('rank_one_cohomology','a9ef0a4497c7c22cb441b1cb9bbdf1126350a8084478f63f21520d46ef65b401',[
 'RV1 proves injective finite-free DVR coefficients, exact cochain and simultaneous local-kernel base change, length scaling by relative ramification, and preservation of infinite length. Arbitrary local families are not replaced by finite subfamilies.',
 'RV2 matches the negative twist with the Cartier dual of Z/ell^r(e+1), checks original local data through KB6/LK, and proves the finite-to-integral inverse/direct-limit identification before using KB8.',
 'RV3 chooses the actual finite field inside the original closure, controls H0 before the finite quotient H1 kernel, and imposes no prime-to-ell assumption on the character order or extension degree.',
 'RV4 proves a countable cofinal finite-field cover by rational approximation and the Krasner isometry argument. Baire is applied to actual closed subgroups defined by the cocycle, not to an arbitrary compact subset of the algebraic closure.',
 'RV5 scales the vector cocycle through the same finite torsion Selmer module and obtains an explicit exact witness using one nontrivial scalar. No unsupported convergence of chosen coboundaries is used.',
 'RV6 constructs the actual finite DVR lattice, returns every local witness to that same finite field by division or zero action, and applies RV3/RV5 on the original local subgroups.',
 'RV7 matches literal SoV and SoFin with every original universal quantifier, and proves coefficient independence for nonnested rings through a common compositum, including e=0 and the infinite-length toNat convention.'
], 'Complete SoFin, SoV and coefficient-independence suppliers. Other symplectic cohomology/model, automorphy, catalogue and rigidity inputs remain. No complete CountII/III or RH/GRH theorem is asserted.')

record('bernoulli_residual_vanishing','06fc9a464c7cb3cb4dc34f1f4c17b5e15d116f8e0d656e5526628e947c3b94eb',[
 'BR1 derives exact dyadic generation, Frobenius projection, and the two congruence classes of small-order character values; all divisions are by powers of two in odd characteristic.',
 'BR2 derives the integral partial sum using a full endpoint shift identity. Its recurrence removes division by the odd conductor, including when that conductor is divisible by ell.',
 'BR3 preserves the source threshold f*4^v2(ell^d-1)<=2^n. The half-period character value, residue projection, endpoints 1 and -1, and cancellation force exactly the contradiction 0=-2.',
 'BR4 treats the actual relative-index UnrEv condition and a possibly infinite original coefficient field. Finite cocycle image gives class-field descent on the original cyclotomic field. The required Eone relation follows from OS1 with the arbitrary-a floor identity and cancellation of 2, not from an unproved integral Stickelberger theorem.',
 'BR5 proves the unit criterion for the specified possibly nonsurjective residue map, preserves inverse-character normalization, and chooses the odd integer a in both conductor cases before applying the exact Bernoulli scalar identity.',
 'BR6 uses the actual conjugation action and nonzero scalar to kill the restriction to the cyclotomic field, then an explicit abelian-quotient identity gives one global coboundary witness in the original field.',
 'BR7 verifies the CRT cyclotomic exclusion for both characters at the same original Galois element, preserves conductor and order under inversion and the original coefficient inclusion, and supplies the complete literal CorX.'
], 'Complete LemmaX, the residual Bernoulli-unit vanishing theorem and CorX. The odd-characteristic specialization of homKill is proved; unrestricted integral clKill/homKill and the full symplectic count are not asserted.')

record('symplectic_count_closure','be6f26510549b7b3879e5a65f46c00b5ab0108909550340ed2342f57d0827c92',[
 'SP1 matches literal LemmaMprime, including arbitrary grading, possibly infinite equation index and an additive rather than O-linear injection. Finite residue cardinalities justify the exact module-length conclusion.',
 'SP2 gives the finite graded prime-filtration proof of eventual Koszul Euler positivity, exact-sequence monotonicity, the product formula and the scaling lower bound, with admissibility checked at every quotient.',
 'SP3 proves actual Rees prime support, the symmetric one-sided ideal and the M3 contradiction. The Nullstellensatz is applied to a nonzero finite-type localized fibre, not directly to an arbitrary residue field. Finiteness and admissibility follow from explicit power containments.',
 'SP4 proves finite orbit covers and reducedness of the actual generic two-sided slice by a faithfully flat square-root cover. This gives multiplicity one in every weight; replacing the prescribed equations by squares gives the precise power-of-two bound.',
 'SP5 preserves the integral Smith exponents while using rational formal coordinates, kills exactly the zero-weight equations, computes the full leading-form rank and the Hilbert difference 2^(r-1+rprime).',
 'SP6 matches M1–M5 and IsWRing/IsNVal exactly. The cover consists only of two-sided points. Torsion removal and determinant norms give the actual valuation sum, and the ratio of lower and upper multiplicities is exactly 2.',
 'SP7 constructs one common annihilator and the actual normalized ShaCoc representatives with all local UnrT clauses. The augmentation descends through the actual model quotient. Square-zero uniqueness proves additivity of derivation reductions; the homogeneous entry gives injectivity. The source GradedAlgebra hypothesis is retained.',
 'SP8 preserves the exact unit kernels, conductor, parity, component characters and all numerical case parameters under injective coefficient extension. RV1 supplies the normalized return to the original ring, not merely an auxiliary bound.',
 'SP9 constructs a nonzero integer product from the precisely quantified conjugation-stable finite catalogue. The archimedean bound proves each factor nonzero; omitted algebraic-integer factors have ell-adic norm at most 1. Uniform choices precede ell, the closure and representation family.',
 'SP10 checks the original trace convention, Selmer inclusion at added primes, exact factor-two valuation normalization, explicit polynomial absorption and coefficient return. Its actual G1 data/admissible-class production, G2 weighted Model/point-orbit comparison and uniform catalogue are retained, so CountII/III remain conditional.'
], 'Full literal LemmaMprime and LemmaM, actual shaCoc/mPrime on a supplied graded Model, coefficient return and finite trace-product/count arithmetic. The actual G1/G2 and catalogue hypotheses are not supplied. LemmaP arithmetic installation, all remaining cohomology/automorphy/rigidity inputs and actual CountII/III remain substantive.')
