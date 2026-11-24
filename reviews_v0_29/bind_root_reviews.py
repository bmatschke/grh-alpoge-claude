#!/usr/bin/env python3
"""Bind completed independent root mathematical reviews to final component bytes.

The findings below record actual readings; this script verifies locators and
hashes and does not itself perform mathematical verification.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

REVIEWS={
 'symplectic_modular_support': {
  'claim_ids':['QX1','QX2','QX3'],
  'expected_main_sha256':'9e17c111d638dcd11242d421fe241ee3c0a976c34d1fb42088253aa952b3c5f8',
  'findings':[
   'QX1: Checked the exact cyclotomic quotient surjection, the CSD polarization delta^n chi^(1-n) with sign -1, Schur comparison of arbitrary source forms, the polarized complex-conjugation adjoint and finite coefficient capture for representations and cocycles. The matched Thorne Theorem 6.1 has no residual-image hypothesis or lower bound on ell. The conclusion covers all n>=2 and hence every literal source case 2<=n<=4.',
   'QX1: Checked transport of the original Af.IsBK cocycle through KB/BX, finite local coefficients and inflation back to Gamma. Vanishing gives the required actual matrix coboundary for every source form/action, not only a symplectic Lie submodule.',
   'QX2: Checked finite capture of arbitrary algebra maps from a formal power-series algebra into algebraic ell-adic points, including dual-number lifts via squared distinguished relations. The fixed-weight tangent injects into an N-dimensional tangent space; finite torsion-free weight support gives dimension at least N by minimal primes and going down. The local ring is regular, so the ideal localizes to zero and lies in every prime below the point.',
   'QX3: Checked the split irreducible Cayley–Hamilton construction, continuity through finite trace coordinates, and Burnside/Nakayama/nondegenerate trace pairing upgrading the actual weak Pair relations to matrix ordinary/inertial identities. Distinct inertia eigenvalues give ordered flags; the polarized character equality gives an actual infinitesimal intertwiner and the unitary-adjoint cocycle.',
   'QX3: Checked the local Bloch–Kato dimension calculation for 0->n->b->E^n->0. Positive weight gaps at least two give H0(n)=H2(n)=0 and H1(n)=Hf1(n); the preimage of unramified diagonal classes has dimension t_n+h0(b), exactly Hf1(b). This supplies the finite local condition without an unsupported surjectivity assertion.',
   'QX3: Checked every away-ell local condition and the auxiliary place: only repeated residual Frobenius eigenvalues are used, not a scalar residual matrix; determinant(Ad(Frob)-q) reduces to (1-q)^(n^2). After adjoint vanishing, equality of determinant and ordered characters gives equality of continuous maps by their topological generators. The universal IsCO property is not incorrectly applied directly to a dual-number field.'
  ],
  'retained_inputs':['An actual finite torsion-free modular quotient and a characteristic-zero automorphic point on it for QX3.','Precisely matched classical Chenevier and Thorne theorems; existing BX/KB/KX interface suppliers.'],
  'not_reviewed_here':['QX4','QX5','QX6','QX7','QX8','QX9','QX10']
 },
 'symplectic_automorphic_seeds': {
  'claim_ids':['SX1','SX2','SX3','SX4','SX5','SX6','SX7','SX8'],
  'expected_main_sha256':'417d314d78c8017fa32f51ad65c0bb1ac306835b0a5f0731d277641a3d2bb2fa',
  'findings':[
   'SX1: Checked both labelings on the original subgroup, the separating-element eigenvalues, the totally real quadratic splitting conditions, the nontrivial dyadic conductor and both ell-adic residual characters. The multiplier congruence retains the actual quadratic character and original tower.',
   'SX2: Checked the mixed ordinary stabilization and the precise constant normalization. DDP Proposition 2.1(50) has only its first constant term because the odd character has nontrivial conductor; the normalized degeneracy map preserves that component-independent constant. The even Hasse exponent, product descent and central norm normalization preserve reduction 1 without division by a class number.',
   'SX2: Checked the finite Hecke-algebra characteristic-zero lift and the separate cuspidality argument. The two global residual Eisenstein characters would have to be 1 and xi inverse, while the unique unit ordinary root must be the same global character at both ell-adic places. The prescribed incompatible refinements exclude both possibilities. Multiplication by a Hasse lift alone is not treated as cuspidality.',
   'SX3: Verified Hida fixed-central-character torsion-freeness, weight independence, control and characteristic-zero ordinary flags against Theorems 1.2, 2.4 and 3.1 of the primary text. The arithmetic avatar is xi inverse, the required representation is chi^k times the dual, and the automorphic normalization is pi_f times |det|^((k+1)/2). The unit-lattice argument and quadratic self-twist exclusion prove irreducibility on every open subgroup.',
   'SX3: Checked the conductor-equality principal-series argument, the split CM base-change comparison for away-ell inertia, the ordinary-slope exclusion of Steinberg at ell, and the strict unitarity bound for all finite inducing characters. No unavailable finite discrete-series hypothesis is imposed on the even-degree Hilbert field.',
   'SX4–SX5: Checked the trace-based Ribet lattice normalization, induced basis and quadratic multiplier sign, the exact root-entry alternative, both explicit local lower-unipotent flags and their unit denominators, and the correcting square-root character. The literal muOf set is handled through its ell-primary torsion image in local abelianization and its inclusion in inertia intersect ker chi.',
   'SX6: Checked the compact-power use of Ok.g3prime, the finite-algebra/procyclic restriction argument, distinct local weight multisets under the two conjugates, cuspidal cyclic induction, the extra |det| attachment twist and the all-finite-place strict window. The same fixed iota is used throughout.',
   'SX7–SX8: Checked matrix-image capture by a countable closed-subgroup cover and Baire, exact finite coefficient descent, nonzero residual entries, the original Wts/IsSeedAlt twist-parity conditions and the full order of quantifiers. The result is literal SeedIIAlt on every original permitted tower; SeedIVAlt and general support are not inferred.',
   'Primary verification: DDP https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p12-p.pdf Proposition 2.1; Hida https://www.math.ucla.edu/~hida/Lum07.pdf Theorems 1.2, 2.4, 3.1 and Remark 3.1; Mok–Tan Overconvergent Families of Siegel–Hilbert Modular Forms, Lemma 2.10 and Proposition 2.11 (Cambridge primary PDF). The retained cyclic base-change and normalized CM Galois compatibility leaves are stated explicitly in the chapter.'
  ],
  'retained_inputs':['Precisely stated classical Eisenstein, Hasse, ordinary-control/Galois, cyclic base-change/induction and CM compatibility theorems.','Original Ctx2/Ok/Two/Deep hypotheses on the given tower, not a producer assertion for arbitrary towers.'],
  'not_reviewed_here':[]
 },
 'symplectic_promodular_realization': {
  'claim_ids':['UX1','UX2','UX3','UX4','UX5','UX6','UX11','UX12'],
  'expected_main_sha256':'2f1513df511aa6160642fe42ebc2432cbe81ac4834486a86fd2bfa21703b4748',
  'findings':[
   'UX1: Checked the auxiliary quadratic-character construction, the original labelling and separating element, removal of added tame degree-ell ramification, and cyclotomic layer order. The final proof explicitly factors the ell-primary part of psi through cyclotomic image and kills its Teichmuller subgroup before the compactness argument; source Good.decompSigma_ord gives infinite cyclotomic order for s0.',
   'UX2: Checked the lattice normalization, preservation of the nonsplit block alternative and all four failed moves in the integer weight polyhedron. The first two tight-root conditions imply A+B even, justifying equality for the two moves with a possible drop of two. The six root configurations and odd-cocycle eliminations produce the literal lattice shape. The final statement first fixes the label and UX1 initial tower/separating g0, then normalizes at that g0 and quantifies only over its compatible fit extensions.',
   'UX3: Checked the finite Poitou–Tate cardinal inequality, the finite coefficient span for arbitrary residue fields, cocycle normalization and the explicit class-two symplectic matrices. U(x,y,t)^ell=1 for every odd ell, including ell=3; the proof does not assume this for arbitrary rank-four unipotents.',
   'UX4: Checked that each interpolation difference lies in the stated square-zero block ideal, so representation, symplectic and flag equations remain polynomial identities. The adjusted local flags commute with the relevant diagonal by Two.atL. Nonzero-entry and local-character alternatives verify goodness, not merely connectedness.',
   'UX5: Checked the exact cyclotomic fixed-field identification, uniform class-rank and prime-count bounds, strict restriction and finite Greenberg–Wiles estimates, arbitrary-field scalar extension and the order of choosing C before the deep layer and seed coefficients.',
   'UX6: Checked the finite-entry universal ring, exact degree-zero invariant argument using spectral projectors and adjoint, finite generation of homogeneous pieces, the Artinian rescaling construction for nonsplit residual patterns, polynomial-line realization and flat local completion. The final muOf wording correctly concerns its image in local abelianization.',
   'UX11: Checked the original ordered inertia characters under label changes, the actual lower/upper restriction factorization, the algebraic-valued intersection argument, finiteness of E intersect V over the small DVR, and the exact-residue pullback ring R. R is not incorrectly asserted to be a DVR; continuity and all polynomial-chain coefficients descend to the one threshold.',
   'UX12: Checked the repaired label -> initial tower/g0 -> normalized lattice order and the four coefficient thresholds, with the PMExAlt threshold chosen before the arbitrary Space. The actual seed gives SomeIn, quantitative propagation gives AllIn, and a minimal prime below the original valued-point kernel forces annihilation of J. Every original coefficient, inertia, multiplier and conjugacy equality is retained under the same fixed iota. The conclusion covers Ctx2 only.',
  ],
  'retained_inputs':['Exact SeedIIAlt, supplied separately by SX8.','Exact PMExAlt, still conditional on its actual arithmetic producer.','Already reconstructed BX/TW/BR/AX inputs in their stated scopes.'],
  'not_reviewed_here':['UX7','UX8','UX9','UX10']
 }
}

selected=sys.argv[1:] or list(REVIEWS)
for component in selected:
    job=REVIEWS[component]
    main=ROOT/component/'main.tex'
    raw=main.read_bytes()
    assert sha(raw)==job['expected_main_sha256'],('Changed after mathematical reading',component)
    pp=ROOT/component/'provenance.json'
    p=json.loads(pp.read_text())
    assert p['commit']==PIN
    claims={c['id']:c for c in p['claims']}
    assert set(job['claim_ids'])<=set(claims)
    cache={}
    source_count=0
    proof_checks=[]
    for cid in job['claim_ids']:
        c=claims[cid]
        loc=c.get('proof_location',c.get('human_proof'))
        path=ROOT/loc.get('file',loc.get('path'))
        lines=path.read_bytes().splitlines(keepends=True)
        piece=b''.join(lines[loc['line_start']-1:loc['line_end']])
        expected=loc.get('sha256',loc.get('range_sha256'))
        assert sha(piece)==expected,cid
        proof_checks.append({'claim_id':cid,'proof_location':loc,'range_sha256':sha(piece)})
        for s in c['sources']:
            if s['path'] not in cache:
                b=(REPO/s['path']).read_bytes()
                assert b==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+s['path']]),s['path']
                cache[s['path']]=b
            b=cache[s['path']]
            assert sha(b)==s['sha256'],s['path']
            ls=b.splitlines(keepends=True)
            piece=b''.join(ls[s['line_start']-1:s['line_end']])
            assert sha(piece)==s['range_sha256'],(cid,s['declaration'])
            source_count+=1
    vf=HERE/(component+'_root_source_validation.json')
    write(vf,{'schema':'rh-independent-source-validation/1','result':'PASS','component':component,
        'commit':PIN,'claim_ids':job['claim_ids'],'main_tex_sha256':sha(raw),'provenance_sha256':sha(pp.read_bytes()),
        'source_file_count':len(cache),'claim_source_range_count':source_count,'proof_checks':proof_checks,
        'all_source_bytes_equal_pinned_git_blobs':True,'all_ranges_match':True})
    rec={'schema':'rh-independent-mathematical-review/1','reviewer':'/root',
        'component':component,'reviewed_file':component+'/main.tex','sha256':sha(raw),
        'provenance_sha256':sha(pp.read_bytes()),'claim_ids':job['claim_ids'],
        'no_unresolved_mathematical_findings':True,'unresolved_findings':[],
        'findings':job['findings'],'retained_inputs':job['retained_inputs'],
        'not_reviewed_here':job['not_reviewed_here'],
        'source_validation_file':str(vf.relative_to(ROOT)),'source_validation_sha256':sha(vf.read_bytes()),
        'scope':'Independent mathematical reading and primary/source-scope checks; not Lean compilation or kernel replay.'}
    write(HERE/(component+'_root_review.json'),rec)
    (HERE/(component+'_root_review.txt')).write_text(
        'INDEPENDENT MATHEMATICAL REVIEW — '+component+'\n\nPASS\n'+
        'Claims: '+', '.join(job['claim_ids'])+'\nMain SHA256: '+sha(raw)+
        '\nProvenance SHA256: '+sha(pp.read_bytes())+'\n\n'+
        '\n\n'.join(job['findings'])+'\n\nRetained inputs:\n'+
        '\n'.join('- '+x for x in job['retained_inputs'])+'\n')
    print(component+': '+str(len(job['claim_ids']))+' claims; '+str(source_count)+' source ranges; PASS')
