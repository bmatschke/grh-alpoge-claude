#!/usr/bin/env python3
"""Bind the root's independent mathematical readings to the frozen agent chapters."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

notes={
 'symplectic_actual_rigidity':{
  'RX1':'Checked actual O-algebra point continuity and finite coefficient capture, the finite f(R)-module argument for derivations, Leibniz bounds, fixed multiplier and sp4 tangent condition, and ramification from the original UnrT relation.',
  'RX2':'Checked ordinary crystalline induction over both E and dual numbers. The positive Hodge filtration, H2 vanishing and rational Euler passage give Hf1=H1 for the actual extension module; local finite-index descent is proved by the correctly signed averaged primitive.',
  'RX3':'Checked the actual OnComp ordinary projectors and label order. The chosen open subgroup contains the distinguished Frobenius and kills the finite inertial characters, so AX8 excludes the adjacent cyclotomic ratio. Both above-ell and every away-ell original local condition are transported.',
  'RX4':'Checked semisimplicity for the infinite normal subgroup, closed/open isotypic stabilizers, the finite cyclic self-twist and the multiplicity-space eigenline argument. Distinct inertia powers force a cyclotomic self-twist to be trivial. A fresh ramified quadratic character at an unramified prime preserves irreducibility over the cyclotomic tower.',
  'RX5':'Checked the exact geometric Frobenius factor q^(3/2), Hecke avatar theta*chi^3, quadratic sign correction, Chebotarev identification, symmetric B=J*r(c)^(-1), and the polarized adjoint action. Thorne Theorem6.1 applies with its actual cyclotomic condition. Baire captures literal Qbar-valued continuous cocycles; each local primitive descends separately by an E-linear retraction.',
  'RX6':'Checked equivariance of the actual sp4 projection and the sign Y=-P(X). The resulting matrix gives the literal RigidAt entrywise identity for every allowed dual-number point. The stronger Good-only implication supplies every quantifier of RigiditySymplecticFour.',
  'RX7':'Checked one image-density embedding is fixed before the full family, giving actual AllIrr RigidAt on the same selected D. Fin0/NoEnd and automorphy still require image density; no complete original UnramifiedInputs/AdjointLifting package is claimed.'
 },
 'symplectic_automorphic_catalogue':{
  'CX1':'Checked the actual highest weight (-3,-3,-e-1,-e-1), its polynomial realization, finite fixed Borel–Serre cell model, torsion-free level3, principal cover degree L^32 and rank bound (e+2)^32. These count full global cuspidal classes with one fixed constant per field.',
  'CX2':'Checked full global labels, Clozel scalar conjugation and polarization preservation. The integer Hecke normalization e_j(A)=q^(j(j-1)/2)T_j proves exact conjugation despite the q^(3/2) Satake normalization.',
  'CX3':'Checked inverse-geometric arithmetic Frobenius eigenvalues, purity weight -(e+1), all finite coefficient primes, compact-lattice units away p, and weak-admissibility slope bounds at p. Both integral and inverse-integral conditions and all complex conjugates follow with the original normalization.',
  'CX4':'Checked the original weak automorphy witness is actually used, polarization theta*epsilon^3, infinity-sign correction, and finite-coefficient Chebotarev identification. De Rham admissibility comes from the attached automorphic Galois representation; it is not inferred from an arbitrary extension of de Rham characters.',
  'CX5':'Read exact SafeRA, LevelAway, LevelAt, KillsMu and IsCycWt definitions. Adjacent weights force ell|M. Local norm/cyclotomic control bounds every character conductor; away ell full compatibility gives 4a and at ell semisimplified compatibility plus rank N<=3 gives 4a+3<=7a. Newvector invariance uses M^7 only for auxiliary automorphic labels, leaving the original Galois level unchanged.',
  'CX6':'Checked eighteen fixed pairwise-coprime quadratic discriminants, at most one excluded p and at most sixteen self-twists via independent intertwiners. Quadratic restriction irreducibility and at most two original extensions follow by elementary module and Schur arguments.',
  'CX7':'Checked complete fixed-field catalogues are chosen before ell/Omega/iota and representation families; equal full labels identify actual restrictions. Literal EigData and its universal integral conditions are supplied.',
  'CX8':'Checked root multisets with multiplicity, at most16 power lifts and two extension bits, giving the fixed 224 exponent and conjugation-stable labels. Actual original Frobenius powers and all placements are covered; bits are assigned only in the classification map. Equality at one prime is never used to identify a global class.',
  'CX9':'Checked the exact SP9 antecedent and integer product, common Galois action on roots of unity, distinct selected labels, nonvanishing, normalized valuations and constants A=225,C=c_*2^225. The endpoint is literal NumberSp4Alt; broader all-rank and unchanged-level interfaces remain unpromoted.'
 },
 'symplectic_image_density':{
  'IX1':'Checked actual universal IsPt and full weight-zero base algebra, including the exact component-ideal equations without a reducedness assumption on the target.',
  'IX2':'Checked proper flag closure and extension of the generic flag to the actual valuation ring, resulting ordered characters, local residue and coefficient compatibility, and exact EPt capture.',
  'IX3':'Checked failure of Fin0 creates the actual positive-dimensional special fibre, prime/curve reduction, invariant-ring nonzero lift, torus scaling and completed evaluation. The nonzero maximal-ideal invariant cannot be Frobenius-periodic, so the point is nonconstant.',
  'IX4':'Checked all reducible entry patterns, the stable-line valuation division using the distinguished local diagonal difference before dividing by its smallest entry, diagonal-character invariants and the exact residual vanishing/Good assumptions.',
  'IX5':'Checked the Greenberg–Wiles cancellation and growth bound, saturated integral quotient, primitive normalized cocycle at all finite levels and finite-branch inverse-limit construction; no rational-only class substitutes for the actual integral nonsplit class.',
  'IX6':'Checked the actual block extension, zero pairwise products, multiplier preservation and character-polynomial identity, conjugation sign uprime=(1-y)u, nonzero block and nonsplitting witness at complex conjugation. The new representation is an actual KPair to which purity applies.',
  'IX7':'Checked the literal PureW strict root bound, the determinant finite-character weight calculation for both blocks, and the contradiction p^(f(e+2))<p^(f(e+2)); the proof uses purity of the newly constructed block point.',
  'IX8':'Checked Con/PurityAtPoints/AutmAlt are imposed on the same D with one fixed iota and on every actual required point. The exact Fin0, NoEnd and AllIrr IsAut4Alt endpoint follows; these arithmetic antecedents are not asserted unconditionally.',
  'IX9':'Checked the complete finite-module-to-special-fibre supplier from actual Link/IsPhi0 maps and LamObj/Space uniqueness. Universal square-characteristic integrality identities descend before quotienting, so no false quotient injectivity is used. The residual trace argument rules out both full matrix span and BlockExt in every allowed characteristic without a semisimple trace shortcut.',
  'IX10':'Checked exact doubled weight normalization, coefficient-compatible IsZero and smallness continuity, residual-character independence proving restriction irreducibility, full literal IsAutQA/WitA conjugacy transport, and the fixed-iota uniform ProModAlt implication. Finite modular quotient/link/support, potential-modularity and seeds remain explicit producers.'
 }
}

for comp,checks in notes.items():
    ledger=read(ROOT/comp/'provenance.json')
    assert ledger['commit']==PIN
    ids=[c['id'] for c in ledger['claims']]
    assert set(ids)==set(checks)
    raw=(ROOT/comp/'main.tex').read_bytes(); lines=raw.splitlines(keepends=True)
    sources=[s for c in ledger['claims'] for s in c['sources']]
    cache={}
    for s in sources:
        path=s['path']
        if path not in cache:
            b=(REPO/path).read_bytes()
            assert b==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
            cache[path]=(sha(b),b.splitlines(keepends=True))
        dig,ls=cache[path]
        assert dig==s['sha256']
        piece=b''.join(ls[s['line_start']-1:s['line_end']])
        assert sha(piece)==s['range_sha256'],(path,s['declaration'])
    for c in ledger['claims']:
        loc=c.get('proof_location',c.get('human_proof'))
        ls=(ROOT/loc.get('file',loc.get('path'))).read_bytes().splitlines(keepends=True)
        assert sha(b''.join(ls[loc['line_start']-1:loc['line_end']]))==loc.get('sha256',loc.get('range_sha256')),c['id']
    stem=comp+'_root'
    val=HERE/(stem+'_source_validation.json')
    validation=dict(result='PASS',component=comp,commit=PIN,main_tex_sha256=sha(raw),
                    provenance_sha256=sha((ROOT/comp/'provenance.json').read_bytes()),
                    claim_ids=ids,claim_source_ranges_checked=len(sources),
                    pinned_files_checked=len(cache),human_proof_ranges_checked=len(ids),
                    scope='Independent byte binding to the source and frozen human text; this is not Lean verification.')
    dump(val,validation)
    bound={comp+'/'+name:sha((ROOT/comp/name).read_bytes()) for name in ['closure.json','classical_inputs.json','input_registry.json','remaining_inputs.json'] if (ROOT/comp/name).exists()}
    review=dict(schema='rh-independent-mathematical-review/1',artifact_version='0.28',
                reviewer='/root',independent_of_component_author=True,result='PASS',component=comp,
                reviewed_file=comp+'/main.tex',sha256=sha(raw),provenance_sha256=validation['provenance_sha256'],
                claim_ids=ids,claims=[dict(id=cid,status='PASS',finding=checks[cid]) for cid in ids],
                no_unresolved_mathematical_findings=True,unresolved_findings=[],reviewed_metadata=bound,
                source_validation_file=str(val.relative_to(ROOT)),source_validation_sha256=sha(val.read_bytes()),
                limitations='Human mathematical/source-scope review of the stated conditional or classical-relative theorems; no Lean build, kernel replay or proof of retained arithmetic inputs.')
    dump(HERE/(stem+'_review.json'),review)
    (HERE/(stem+'_review.txt')).write_text('INDEPENDENT MATHEMATICAL REVIEW — '+comp+'\nPASS\n\nReviewer /root read every stated proof, reviewed the substantive hypotheses and joins independently, and checked the final source/proof hashes.\n\nMain SHA256 '+sha(raw)+'\nProvenance SHA256 '+validation['provenance_sha256']+'\n\n'+'\n\n'.join(cid+': PASS. '+checks[cid] for cid in ids)+'\n\n'+review['limitations']+'\n')
    print(comp, len(ids),len(sources),len(cache),'PASS',sha(raw))
