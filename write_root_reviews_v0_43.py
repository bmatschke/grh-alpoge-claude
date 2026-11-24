#!/usr/bin/env python3
"""Record the root's completed independent mathematical reviews of agent chapters."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reviews_v0_43'
OUT.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
notes={
 'integral_type_v43':[
  'Actual complete coefficient DVR and algebraic closure over its embedded fraction field follow from the inherited GA1/GA2; no complex continuity is inferred.',
  'Newton lifting and the unit geometric sum establish the unique full Teichmuller family, exact kernel equality and all later lift quantifiers.',
  'Each actual decomposition-group character has finite image and open kernel; the given extensions make the diagonal inertia datum an inertial type.',
  'The split type-place hypothesis allows the CIP3 local-unit injectivity argument away from ell; the actual global Artin equation fixes the geometric sign and every allowed local map.',
  'Zero monodromy, extending inertia characters and Frobenius semisimplicity give a toral parameter. Ordered singleton Langlands quotients and source Good/inj compare every IsRecT only on that sector. RecTExists nonvacuity is retained explicitly.',
  'Emerton–Gee Theorem8.2.1 was checked in the primary text, together with conventions and CEGGPS3.7. It detects zero monodromy and exact inertia for all irreducibles without genericity or prime-to-rank restrictions. The actual field is a finite extension of Qp.',
  'The half-modulus and algNorm inverse twist combine to integral exponents n−1−i. Arbitrary coefficient automorphisms fix those rational norm values and preserve the nonprecedence condition; no positive square-root invariance is assumed.',
  'Finite matrix descent, stable lattice, restriction of scalars to the original O and all conjugate summands are correct. Every E/K embedding extends over the algebraic closure, and ITA7 preserves the detection predicate in each summand.',
  'The inverse transpose is exactly the source column equation: its invariant tensor corresponds to Hom(B,M), not to the dual detector. Open kernel survives integral and complex scalar extension.',
  'The algebraic semisimple-module complement argument proves submodule isotypy without finite length. Finite-dimensional Hom sources see finite subsums.',
  'Successive Hom functors preserve isotypy for every remaining commuting factor. Nonzero output is equivalent to every local predicate; the empty product gives rank1 and the original nonzero M.',
  'Choice order, one original integral representation, every Teichmuller family and every IsRecT/test module are matched to the literal TypeForAlt definition. Classical foundations remain declared.',
  'Exact substitution into inherited OTW13/CAP17 supplies all eight original UnitaryHeckeData fields and HdEx, with no same-J or global automorphy consequence asserted.'
 ],
 'arithmetic_fibers_v43':[
  'The first maximum coefficient index bounds zeros in the entire algebraic open unit disk by successive divisions over finite extensions. The multivariable induction does not require an interior accumulation point.',
  'Disjoint ell-power order progressions combined with prime-to-ell lifts give infinite Cartesian torsion sets with the literal index distinction, including ell3.',
  'Actual KX3 inertia abelianization and coordinate generators make torsion values imply finite inertia image, open kernel and one finite-part depth on the stored Artin map.',
  'The algebraic unit character extends with trivial uniformizer value; the actual coefficient-point decay gives continuity, and the IsTheta identity gives the correct inverse finite part.',
  'KX4/KX5 transport the torsion-box evaluations to every supplied LamObj. A nonzero local free coordinate supplies the distinctness witness, and all original Good clauses are checked.',
  'The reversed integer-weight formula is dominant. Distinct selected primes cannot yield the same global restriction, and embeddings at one prime agree by continuity and density.',
  'Compact inertia-to-unit quotient and the precise reciprocal product identity establish both directions of local algebraicity and all allowed Artin-map quantifiers.',
  'The corrected CIP5 citation supplies the cyclotomic sign. The original toPair/IsTheta formula, common depth and equality of finite-part functions give both exact bridge equivalences.',
  'Faithful finite T-module support and Nakayama imply nonzero fiber for every specified y; the Artinian character block supplies an eigenvector and one stable summand, without flatness.',
  'The residual idempotent gives a finite free split block. Nonzero rank survives every coefficient point; exact specialization basis independence gives the original injective fiber identification.',
  'Finite compact averaging proves the original Jacquet-kernel criterion with the integer double-coset index; stabilized positive images are finite-dimensional and inject into coinvariants.',
  'The retained bz/geo/disj premises suffice for the explicit principal-series embedding, exact Jacquet filtration, distinct-unit one-dimensional block and irreducibility. The index and modulus exponents give exactly the source psEig.',
  'Semisimple isotypic sums have detecting equivariant coordinate maps; extending to the ambient space only asserts intertwining on the original subspace.',
  'Surjective positive operators put every detecting image in the same local invPart. One selected principal series then gives scalar identities on all images and hence on the original part.',
  'The adjugate determinant argument produces an annihilating polynomial with constant term1; the original integral coefficients and eigenvalue bound force norm1.',
  'Local isotypy and spherical scalar fields prove preservation by each actual opC. Product double-coset representatives give the exact single-place finite sum.',
  'Original specialization and ordinary invertibility make every local operator surjective on the finite part intersection. Exact finite-part distinctions, lowVal normalization and determinant units prove all goodScalB_alt clauses.',
  'The split inclusion supplies tensor injectivity without flatness. Polynomial transport of the actual idempotent preserves each given part and the same operator action.',
  'CFD12 with the supplied actual hAut decomposes the fiber; the faithful point lemma gives every specified character in one original part. Scalar uniqueness on a nonzero good part gives one compatible ring point for all t,F.',
  'The original good points kill the scalar action on every part; basis independence and DenseWt then kill every coefficient of tf. Reducedness is deduced rather than assumed.',
  'Composing each separating T-point with the original f proves membership in the literal kernel; neither a radical nor a different quotient is substituted.',
  'The zero-module branch and the original IsJ map are both retained. The full same-J density implication follows with the exact additional AutomorphicHeckeSet supplier explicit; bare TJDense and Out.pt are not marked complete.'
 ],
 'finite_local_completion_v43':[
  'Frobenius orbits and the prime-primary root-fiber bound include every characteristic and degree with nonzero roots.',
  'A collision within an irreducible shortens the projected orbit to a proper divisor e<=d/2. Dividing the uniform root count by d gives the full q^(3d/4) factor count.',
  'Common Frobenius transport puts each cross-factor collision in one fixed projection fiber; no degree(Pprime) loss occurs.',
  'Weighted union bounds keep only distinct squarefree divisor pairs before applying RRT5. Possible primes divide the indicated original root orders.',
  'The geometric-series estimates for x<=1/8 give the stated constant23, including degree0 and1; all finite-field quantifiers are preserved.',
  'Finite induced function models, double-coset decomposition, reciprocity, semisimplicity and normalized trace averages are correctly stated.',
  'Both root-compatibility conditions force decreasing consecutive intervals. Counting r blocks and diagonal constants yields (q−1)q^(n−1) exactly.',
  'The abelian last-column orbit construction proves mirabolic irreducibility and the restriction to the actual Gelfand–Graev module; its norm gives the sharp lower coefficient.',
  'The conjugation change of variables cancels each outside-subgroup sum; the two orders of the intersection sum give equality of normalized character averages.',
  'Every literal H_i pattern, character edge and union pattern is checked. The p-to-W/W-to-t exchange has the required conjugates and nontrivial p-to-t character. The endpoint permutation matches original eJ with Jprime.',
  'The tail subgroup is normalized by the correct mirabolic and preserves its character. The actual semidirect products identify both fixed spaces; RRT normalization gives exactly1−q^(−1).',
  'Cuspidality removes the zero-character eigenspace at every mirabolic step; the remaining equal nonzero orbits give the exact cuspidal degree/Whittaker multiplicity identity.',
  'Parabolic double cosets are indexed by flag-intersection matrices. A split row or column produces a proper radical acting on one coefficient and trivially on the other, so cuspidality kills it. Matching supports and squarefree irreducibility follow.',
  'Only the decreasing contiguous block shuffle survives the nondegenerate Whittaker character. The remaining factors are exactly the original within-block Whittaker spaces.',
  'The explicit proper-subfield bound satisfies the strict q5,d2 boundary. Fourier support uncertainty then gives equality of prime labels from original elliptic values.',
  'The primary Green simplex/partition(1), sign, degree and elliptic sum dictionary was checked. Original supplied Teichmuller map and degree generators identify the exact thetaOf labels; no new compatible system is selected.',
  'Unique cuspidal support and distinct factors give a singleton squarefree series. Finite parabolic degrees and Whittaker multiplicity give the exact normalized sqWeight, including rank0.',
  'Finite injective prime-label maps give degree-preserving permutations. The same irreducible constituents yield equality of actual central idempotents. Collision predicates remain on the unchanged original polynomial.',
  'All five original Wg terms assemble on the original supplied normalized-type/AllRows records. RRT10 is used only with the explicit eventual rank-growth guard. The unused fourth admLq upper law and actual global row/count suppliers remain unclaimed.'
 ]
}

for component, findings in notes.items():
    ledger=json.loads((ROOT/component/'provenance.json').read_text())
    raw=(ROOT/component/'main.tex').read_bytes()
    lines=raw.splitlines(keepends=True)
    assert len(ledger['claims'])==len(findings),component
    reviewed=[]
    for c,note in zip(ledger['claims'],findings):
        pl=c['proof_location']
        excerpt=b''.join(lines[pl['line_start']-1:pl['line_end']])
        assert pl['sha256'] in {sha(excerpt),sha(excerpt.rstrip(b'\r\n'))},c['id']
        reviewed.append({'id':c['id'],'result':'PASS','line_start':pl['line_start'],'line_end':pl['line_end'],
                         'proof_range_sha256':sha(excerpt),'review':note})
    result={'schema':'rh-independent-mathematical-review/1','artifact_version':'0.43','date':'2026-11-23',
      'reviewer':'root','author':{'integral_type_v43':'main_proof_rigidity','arithmetic_fibers_v43':'ordinary_structure','finite_local_completion_v43':'global_estimates'}[component],
      'source_commit':ledger['source_commit'],'result':'PASS','proof_file':component+'/main.tex',
      'proof_sha256':sha(raw),'claims_reviewed':reviewed,'unresolved_findings':[],
      'scope':'Independent human mathematical and exact-interface review of every new claim in this component, at its explicitly stated hypotheses. Published applications and foundational inputs are retained as written.',
      'limitations':['Not a Lean build, kernel replay, proof assistant verification or assertion of a completed RH/GRH human proof.',
                     'Conditional nested producers do not assert existence of their remaining global input records.']}
    target=OUT/(component+'_root_review.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'review':str(target.relative_to(ROOT)),'claims':len(reviewed),'proof_sha256':sha(raw)}))
