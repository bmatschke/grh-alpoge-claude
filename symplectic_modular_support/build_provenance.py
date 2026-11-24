#!/usr/bin/env python3
"""Bind QX's proved constructors and its exact retained modular-support cut."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent / 'lean-source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
COMP = HERE.name
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
WS = AV + 'WeakShimuraTheory/'
WG = AV + 'WeilGroupCharacters/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
WC = WS + 'CompactIntegralFields/'
FGR = 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/'
files = {}

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def source(path, name, role='Exact pinned definition or producer in the stated QX scope'):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pat = r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)'
    starts = [(i,m.group(1)) for i,l in enumerate(lines,1) if (m:=re.match(pat,l.decode()))]
    hits = [(i,n) for i,n in starts if n == name or n.endswith('.' + name)]
    assert len(hits) == 1, (path,name,hits)
    a,n = hits[0]
    b = min([i for i,_ in starts if i>a] or [len(lines)+1])-1
    while b>a and not lines[b-1].strip(): b-=1
    piece=b''.join(lines[a-1:b])
    if path not in files:
        blob = subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
        assert raw == blob, path
        files[path]=dict(path=path,sha256=sha(raw),bytes=len(raw),lines=len(lines),
            verified_equal_to_pinned_git_blob=True,url=f'{URL}/blob/{PIN}/{path}')
    return dict(path=path,declaration=n,source_spelling=n,line_start=a,line_end=b,
        sha256=sha(raw),range_sha256=sha(piece),range_bytes=len(piece),
        first_line=lines[a-1].decode().rstrip('\n'),role=role,
        verified_equal_to_pinned_git_blob=True,url=f'{URL}/blob/{PIN}/{path}#L{a}-L{b}')

spec = {
 'QX1': {
  DT+'AutomorphicPointGalois.lean':['AdjointLiftingTheorem','AutomorphicPointGalois','AutomorphicPointLocallyGeneric'],
  AV+'TheoremsMuLinked/OrdZero.lean':['TypeI','AdZero','Par','N3'],
  WS+'EigenbasisLifts/IsTanZero.lean':['IsAdExt'],
  WG+'UniversalOrdinaryDeterminantRing.lean':['GFrame','IsForm'],
  AV+'ModularityArgument/AutomorphyLifting/IsAutCsdA.lean':['IsAutCsdA'],
 },
 'QX2': {
  WS+'EigenbasisLifts/RegOfTan.lean':['rank_le_res','regOfTan'],
  WS+'EigenbasisLifts/IsTanZero.lean':['IsTan','isTan_zero'],
 },
 'QX3': {
  DT+'EigenbasisRankFour.lean':['tan_one','at_l','arith','noRatio','eigenbasis_rank_four'],
  WG+'UniversalOrdinaryDeterminantRing.lean':['Pair','UniversalOrdinaryDeterminantRing','IsForm','starOp','oEl','Ip'],
  WG+'ArithmeticPointClassicality.lean':['UniversalOrdinaryDeterminantRing.RingProps'],
  AV+'TheoremsMuLinked/OrdZero.lean':['OrdAt','OrdCoc','OrdZero'],
 },
 'QX4': {
  DT+'LinkTwo.lean':['exists_two_links_same_kappa_not_dvd_of_fit_deep'],
  FGR+'PlainTorsionPairs/LinkTwo.lean':['setAv','mkSetP'],
  WC+'LinkEx.lean':['pre_ex'],
  WS+'UnipotentIdempotents/TCont.lean':['Pre','κ','QCh','OCh','SetD'],
  WS+'FrobeniusDensity/CoprimeOfNotMem.lean':['kap0'],
  WS+'FrobeniusDensity/UnitDivNear.lean':['bt0'],
  WS+'UnipotentIdempotents/KapConj.lean':['kapConj_alg','kapConj'],
  WS+'UnipotentIdempotents/KapCyc.lean':['kapCyc'],
  WS+'UnipotentIdempotents/ResidEx.lean':['residEx'],
  WS+'UnipotentIdempotents/V0ok.lean':['v0ok'],
  WS+'IsAlgClosureField.lean':['Link'],
  WS+'NearSplit.lean':['Tower','Ok','Fit','Deep'],
 },
 'QX5': {
  DT+'TPhiEx.lean':['exists_phi_universal_ordinary_det_ring_of_link'],
  WS+'IsAlgClosureField.lean':['IsPhi'],
  WS+'PhiCharacterResidues/PhiDet.lean':['phiDet'],
  WS+'PhiCharacterResidues/SpacePsiMul.lean':['phiPsiEx'],
  WS+'PhiCharacterResidues/ResidueEqOneOfMap.lean':['residue_eq_one_of_map','phiIne'],
  WS+'PhiCharacterResidues/CharpolyGspConjInvScaled.lean':['charpoly_gsp_conj_inv_scaled','phiPol'],
  WS+'PhiCharacterResidues/PhiFlag.lean':['phiFlag'],
  WS+'PhiCharacterResidues/PhiUnr.lean':['phiUnr'],
  WG+'UniversalOrdinaryDeterminantRing.lean':['Pair','Pair.Maps','UniversalOrdinaryDeterminantRing'],
 },
 'QX6': {
  DT+'HidaModularIdealMap.lean':['hida_modular_ideal_map'],
  WS+'TwistedFourierKernels/LcOfKer.lean':['lc_of_ker','lift_mem','twJN'],
  WS+'TwistedFourierKernels/TwMapEx.lean':['twMapEx'],
  WS+'TwistedFourierKernels/PhiTw.lean':['phiTw'],
  WG+'ArithmeticPointClassicality.lean':['Dense','TwistOk'],
 },
 'QX7': {
  DT+'BirthPm.lean':['local_zero_of_modular_p'],
  DT+'BirthSeedB.lean':["ptAutR'_alt"],
  WS+'ResidueFlagPoints/PowMemOpen.lean':['pow_mem_open','ptWts'],
  DT+'PointTheoremBaseObject.lean':['PointTheoremBaseObject','HidaPropsAlt'],
  DT+'PotentialModularityTower.lean':['IsSeedAlt'],
  WS+'NearSplit.lean':["G'",'Wts'],
  AV+'ModularityArgument/AutomorphyLifting/PrimeIndexConstruction/CuspidalRankFourRegularAlgebraicTotallyComplex.lean':['CuspidalRankFourRegularAlgebraicTotallyComplex'],
 },
 'QX8': {
  DT+'ModularDeformationQuotientRegularAtPoint.lean':['modular_deformation_quotient_regular_at_point_alt'],
  WC+'H4.lean':['h4'],
  WS+'StabilizerIndexBounds/NonComm.lean':['exists_noncommuting_images_in_finiteIndex_normal_subgroup'],
  AV+'AlgebraTools/MonomialRepresentations/RegCosetFour.lean':['sepA','sepB','core','regCosetFour'],
  WG+'UniversalOrdinaryDeterminantRing.lean':['Point','N1','TypeI','N3','N4','NiceI','P1core'],
  DT+'PotentialModularityTower.lean':['PotentialModularityTower'],
 },
 'QX9': {
  DT+'VWinPm.lean':['pmPur_w_alt'],
  FGR+'AdmissibleResidues/ArithmeticPointDecomposition.lean':['PureW','ArithmeticPointDecomposition'],
  DT+'PmAutO.lean':['pmAutO_alt'],
  FGR+'PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean':['WitOff','AutOffN','IrrArithPointsAutomorphicAway','glueN'],
  DT+'DnPmDown.lean':['pmDown_alt'],
  DT+'AutomorphyDescentSolvableCMToImaginaryQuadraticA.lean':['isAutomorphicOverImagQuad_of_restriction_aut_irr'],
  AV+'ModularityArgument/AutomorphyLifting/IsAutCsdA.lean':['IsAutQA'],
  AV+'ModularityArgument/AutomorphyLifting/WeakOfAtt.lean':['Unl1','PotUnl','WitA','IneAb','Flagged','Keeps'],
  AV+'ModularityArgument/UpperTriangularPlaces/NormalValuationBounds/CommLeRbar.lean':['comm_le_fix','comm_le_rbar','ineQ'],
  AV+'ModularityArgument/UpperTriangularPlaces/NormalValuationBounds/UpTri.lean':['upTri'],
  DT+'IsAut4.lean':['IsAut4Alt'],
 },
 'QX10': {
  DT+'PmTwo.lean':['promodular_existence_of_local_zero'],
  DT+'PmExTh.lean':['pm_exists_of_unramified_adjoint_lifting'],
  DT+'PotentialModularityTower.lean':['PotentialModularityTower','PMExAlt'],
  DT+'PointTheoremBaseObject.lean':['HidaPropsAlt','ModularAlt','ModUAlt'],
  DT+'TPmFin.lean':['exists_pow_maximalIdeal_le_of_modular_phi'],
  DT+'WsLink.lean':['UnramifiedInputs'],
 },
}

titles = {
 'QX1':'Literal AdjointLiftingTheorem via the precisely matched polarized adjoint theorem',
 'QX2':'Complete local algebra from fixed-weight tangent vanishing to prime support',
 'QX3':'Actual determinant tangent, local finite conditions and fixed-weight support',
 'QX4':'Two literal arithmetic Links with common scalar characters and one coefficient threshold',
 'QX5':'Actual Pair construction and all universal IsPhi maps in the original Space',
 'QX6':'Integral twist invariance of the modular image ideal',
 'QX7':'Complete seed-point local support with exact weights and original coefficient ring',
 'QX8':'Full characteristic-ell NiceI construction and P1core support transport',
 'QX9':'Strict PureW and complete same-embedding original-field automorphic return',
 'QX10':'Exact five-clause PMExAlt constructor from the retained rank-four ordinary supports',
}
deps = {
 'QX1':['KB6','RV4','BX1','BX2','BX3','BX4'],
 'QX2':['DX5'],
 'QX3':['QX1','QX2','KX7','KX8','KB6','BX4'],
 'QX4':['KX2','KX3'],
 'QX5':['QX4','KX8','KX9'],
 'QX6':['QX5','KX1'],
 'QX7':['QX2','QX3','QX4','QX5','QX6'],
 'QX8':['QX4','QX5'],
 'QX9':['QX4','QX5','QX7','KB6'],
 'QX10':['QX4','QX5','QX6','QX7','QX8','QX9','IX9','KX5','KX8','KX9'],
}
scopes = {
 'QX1':'All n>=2, original level quotient, same Qbar/iota, arbitrary original polarization matrix and IsAdExt action, literal Af.IsBK and TypeI. Therefore the complete source AdjointLiftingTheorem for 2<=n<=4; no residual-image, Par, Free or N3 strengthening.',
 'QX2':'For the actual complete Noetherian local coefficient rings, a finite torsion-free quotient over O[[N]] and a point on it, vanishing of the relative tangent gives containment in every prime below the point. N=0 included.',
 'QX3':'A point already on the actual modular quotient, actual continuous CSD cusp with WitA, cyclotomic irreducibility, auxiliary unramifiedness and ordered ordinary weights with gaps at least2. Concludes literal fixed-weight prime support; it does not construct J or put the point on J.',
 'QX4':'Every actual Fit+Deep tower; constructs both full Link records with the same kappa,beta,t and different auxiliary primes, uniformly before every later coefficient extension and Space.',
 'QX5':'Every actual X over every allowed O-prime, every a>=0 and every actual universal B: constructs Pair over X.B, then unique IsPhi_a map with both exact determinant and local-character equations. No separatedness of X.A is assumed.',
 'QX6':'Given the same actual ordinary ideal and its Dense/TwistOk fields, proves equality of the image ideals for all a>=0 by finite group-algebra interpolation, without dividing by ell.',
 'QX7':'Given actual HidaPropsAlt on J0, every original IsSeedAlt point satisfies full LocZero for the a=0 image ideal. Retains AllWin, exact parity/gaps, every prime below the original X.B-kernel, and actual same-coefficient maps.',
 'QX8':'Given actual P1core on J0, every finite-field power-series test in PM.p1 becomes an actual NiceI point: N1, TypeI, N3 and N4 all proved, including ell=3. Returns full original LocZero.',
 'QX9':'Given actual HidaPropsAlt and an arithmetic point on its image, proves exact strict PureW for every original extension r. Under precisely PM.aut hypotheses, proves actual IsAutQA/IsAut4Alt over every required imaginary quadratic field with one fixed iota, including TorAt, Unl1=>PotUnl and one global strict-window center.',
 'QX10':'If actual rank-four ordinary ideals with six HidaPropsAlt fields and P1core exist on the two QX4 Links, constructs all five PM fields and literal PMExAlt, preserving the coefficient-threshold then all extensions then all Spaces quantifier order. The ideal-existence input remains open.',
}

classical = {
 'QX-THORNE':dict(name='Polarized adjoint Bloch--Kato vanishing',reference='J.A.Thorne, arXiv:2207.04925, Theorem6.1, printedp24; unitary-adjoint normalization and delta^n epsilon^(1-n) in Section6.3, p25.',
  url='https://arxiv.org/abs/2207.04925',statement='For an actual regular algebraic cuspidal polarized pair over a CM field and n>=2, irreducibility on the full cyclotomic extension implies vanishing of its polarized adjoint H1_f.',
  matching='QX1 proves surjectivity onto Gamma-prime, actual Frobenius attachment, exact form scalar cancellation and minus-transpose action, finite coefficient capture and original Af.IsBK matching. No residual adequacy or lower bound on ell is inferred.',primary_checked=True),
 'QX-BLGGT':dict(name='Polarized Galois representations and algebraic Hecke avatars',reference='Barnet-Lamb--Gee--Geraghty--Taylor, Annals179(2014), Theorem2.1.1(1)--(3), printedp538, and AppendixA.2, printedp600.',
  url='https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf',statement='Actual regular algebraic polarized cusp pairs have continuous semisimple Galois representations with geometric local compatibility away ell and de Rham property. Algebraic ell-adic rank-one characters are the avatars of algebraic Hecke characters, with the explicit infinity/cyclotomic normalization.',
  matching='QX1 uses the exact CSD polarization. QX7 checks integral local exponents before using rank-one reciprocity. QX9 first constructs and sign-corrects actual polarized pairs; no infinity sign is identified with the uncorrected avatar at complex conjugation.',primary_checked=True),
 'QX-CHENEVIER':dict(name='Determinants, integral coefficient identities and absolutely irreducible realization',reference='G.Chenevier, arXiv:0809.0415v2, Lemma1.12, Corollary1.14, Theorem1.15, Theorem2.22(i), Remark3.5.',
  url='https://arxiv.org/abs/0809.0415',statement='Integral mixed determinant coefficients are polynomials in group-word characteristic coefficients; a split absolutely irreducible residual Cayley--Hamilton determinant over a henselian ring is a matrix determinant; universal determinant rings are topologically generated by their coefficient functions.',
  matching='QX3 applies to the dual-number point and upgrades weak Pair trace relations by Burnside/Nakayama. QX5 descends the full law integrally, including ell=3. QX3 does not apply B.univ to Qbar[epsilon].',primary_checked=True),
 'QX-CFT':dict(name='Finite and local class field theory',reference='J.S.Milne, Class Field Theory v4.03, I Theorems1.1,1.4; V Theorems5.3,5.5 and Remark5.7.',
  url='https://www.jmilne.org/math/CourseNotes/CFT.pdf',statement='Local units correspond to inertia; global finite abelian extensions and ray-class characters are given by idele reciprocity with compatible norms and Frobenius.',
  matching='QX4 explicitly constructs kappa0 and the one-sided ell-adic character mu using finite ray classes; the root/continuity/parity/threshold calculations are proved. QX7 and QX9 use the original local embeddings and finite coefficient fields.',primary_checked=True),
 'QX-CHEBOTAREV':dict(name='Chebotarev and semisimple-character comparison',reference='J.S.Milne, Algebraic Number Theory, Theorem8.31; finite-dimensional semisimple character criterion.',
  url='https://www.jmilne.org/math/CourseNotes/ANT.pdf',statement='Each conjugacy class in a finite Galois group occurs at infinitely many unramified primes; continuous semisimple characteristic-zero representations agreeing on a dense Frobenius set are isomorphic.',
  matching='QX4 uses a class fixing the original F and K to obtain degree-one split auxiliary primes avoiding any finite set. QX1/QX9 check continuity and semisimplicity before comparison.',primary_checked=True),
 'QX-AC':dict(name='Cyclic cuspidal base change and descent with strong local compatibility',reference='Arthur--Clozel, Simple Algebras, Base Change, and the Advanced Theory of the Trace Formula, ChapterIII Theorem4.2(a),(b),(d), pp202--203; Theorem5.1, p212; ChapterI Section6, including Theorem6.2.',
  url='https://www.claymath.org/library/cw/arthur/pdf/30.pdf',statement='A Galois-invariant cusp descends through a cyclic prime-degree extension, uniquely up to its finite quotient characters; a cusp base changes cuspidally unless the prescribed quotient self-twist occurs; global base change is strong at every place and compatible with the local correspondence.',
  matching='Only rank4 cyclic steps are used in QX9. Invariance follows from the actual extended r and strong multiplicity one. Irreducibility and the fresh ramified prime exclude exceptional self-twists. Every finite character ambiguity is corrected before returning the original r.',primary_checked=True),
 'QX-HLTT':dict(name='Galois existence without a prior polarization',reference='Harris--Lan--Taylor--Thorne, On the rigid cohomology of certain Shimura varieties, TheoremA / Corollary7.14.',
  url='https://virtualmath1.stanford.edu/~rltaylor/rigcoh.pdf',statement='A regular algebraic cuspidal representation of GLn over a CM field has a continuous semisimple Galois representation matching geometric normalized unramified Satake polynomials.',
  matching='Used only after Arthur--Clozel constructs a specific descent cusp. Its restriction is the given irreducible r, so the finite-character discrepancy is explicitly removed. No automorphy of an arbitrary representation is inferred.',primary_checked=True),
 'QX-CAR':dict(name='Full CSD local compatibility and every-finite-place temperedness',reference='A.Caraiani, Duke Math.J.161(2012), Theorems1.1--1.2, printedp2312; Monodromy and local-global compatibility for l=p, Theorem1.1 (ANT8(2014)).',
  urls=['https://www.ma.imperial.ac.uk/~acaraian/papers/lgc1.pdf','https://www.ma.imperial.ac.uk/~acaraian/papers/lgc2.pdf'],statement='For any n>=2 and actual cohomological conjugate-self-dual CM cusp, full Frobenius-semisimplified local compatibility holds at every finite place, and every finite local component is tempered.',
  matching='QX9 applies only to the actual end2 CSD cusp at the chosen CM field, after the regular-algebraic/cohomological match. It then transports essential temperedness through the explicit cyclic chain. No Shin-regularity hypothesis is dropped from a theorem that has one.',primary_checked=True),
 'QX-BGP':dict(name='Semisimplified local compatibility at ell',reference='Barnet-Lamb--Gee--Geraghty--Taylor, Local-global compatibility for l=p, II, TheoremA; Theorem1.1 and Corollary1.2.',
  url='https://virtualmath1.stanford.edu/~rltaylor/lg2.pdf',statement='At ell, the semisimplified Weil representation attached to an actual regular algebraic polarized CM cusp agrees with geometric local Langlands. Full Frobenius-semisimplification in this theorem has a further Shin-regularity condition.',
  matching='QX9 uses only the first conclusion. Its equation QX.26 and literal Unl1 rule out norm-ratio monodromy entries, so N=0 is proved independently, then temperedness gives PotUnl and WinAt.',primary_checked=True),
 'QX-CLOZEL':dict(name='Regular algebraic cuspidal representations are cohomological',reference='L.Clozel, Motifs et formes automorphes (1990), Lemma3.14, with Theorem3.13; already matched in CX-CL.',
  url='https://www.jmilne.org/math/Books/AA1988a.pdf',statement='A regular C-algebraic cuspidal representation of GLn has nonzero relative Lie algebra cohomology with the algebraic coefficient of the same infinitesimal character.',
  matching='Matches the source IsRegAlg of the actual CSD cusp to Caraiani\'s cohomological premise. Only this archimedean consequence is reused; no counting or rationality bound is used.',
  inherited_registry='symplectic_automorphic_catalogue/classical_inputs.json:CX-CL',primary_checked_in_inherited_registry=True),
 'QX-LINEAR':dict(name='Finite-dimensional density, Clifford theory and elementary character independence',reference='P.Etingof et al., Introduction to Representation Theory, Theorem2.5(i), p24; elementary proofs of the needed finite-index and self-twist cases are supplied in QX8--QX9.',
  url='https://math.mit.edu/~etingof/replect.pdf',statement='A finite-dimensional irreducible representation over an algebraically closed field spans the full endomorphism algebra; distinct one-dimensional characters are linearly independent.',
  matching='Burnside gives the trace-coordinate and weak-relation upgrades. QX8 proves the exact rank4 char-ell N3 argument, including characteristic3, rather than importing a stronger residual-image theorem.',primary_checked_in_inherited_registry=True),
 'QX-LOCAL-ALGEBRA':dict(name='Noetherian local dimension and going-down facts',reference='Normal-domain going-down for integral extensions, the equality of regular-local dimension and cotangent dimension, and Krull intersection; the finite-point and formal-series comparison is already DX5.',
  statement='Integral finite domain extensions of a normal domain satisfy going-down; dimension is at most embedding dimension; equality characterizes a regular local ring, which is a domain; ideals of a complete Noetherian local ring are closed.',
  matching='QX2 uses normality of the actual regular weight ring and torsion-freeness before applying the dimension bound. It proves the support conclusion by localization. QX6 takes closed-ideal limits only in the complete Noetherian ring B.',kind='standard commutative-algebra input with the needed argument given in the human proof'),
}
use = {
 'QX1':['QX-THORNE','QX-BLGGT','QX-CHEBOTAREV','QX-LINEAR'],
 'QX2':['QX-LOCAL-ALGEBRA'],
 'QX3':['QX-CHENEVIER','QX-LINEAR','QX-LOCAL-ALGEBRA'],
 'QX4':['QX-CFT','QX-CHEBOTAREV'],
 'QX5':['QX-CHENEVIER'],
 'QX6':['QX-LOCAL-ALGEBRA'],
 'QX7':['QX-BLGGT','QX-CFT','QX-LINEAR'],
 'QX8':['QX-LINEAR'],
 'QX9':['QX-CFT','QX-CHEBOTAREV','QX-BLGGT','QX-AC','QX-HLTT','QX-CAR','QX-BGP','QX-CLOZEL','QX-LINEAR'],
 'QX10':[],
}
retained = {
 'QX1':[],
 'QX2':['The stated finite torsion-free quotient and point/tangent hypotheses; no arithmetic quotient existence is asserted.'],
 'QX3':['Actual modular quotient, point already on it, attached CSD cusp, stated local and irreducibility hypotheses.'],
 'QX4':[], 'QX5':[],
 'QX6':['The actual ideal J0 and its literal Dense and TwistOk fields.'],
 'QX7':['The actual ideal J0 with all six HidaPropsAlt fields; an actual IsSeedAlt point is the theorem antecedent.'],
 'QX8':['The actual ideal J0 with literal P1core; the original PM.p1 point test is the theorem antecedent.'],
 'QX9':['The actual ideal J0 with HidaPropsAlt and an arithmetic point on its image; PM.aut retains its original continuity, multiplier and restriction-irreducibility hypotheses.'],
 'QX10':['QX-HIDA4','QX-P1'],
}
bespoke = {cid:[] for cid in deps}
for cid in ['QX3','QX6','QX7','QX9']: bespoke[cid]=['QX-HIDA4']
bespoke['QX8']=['QX-P1']
bespoke['QX10']=['QX-HIDA4','QX-P1']

prior=json.loads((ROOT/'history/version_0_28/provenance.json').read_text())
registry={c['id']:(c,'history/version_0_28/provenance.json') for c in prior['claims']}
kx=json.loads((ROOT/'symplectic_universal_arithmetic/provenance.json').read_text())
registry.update({c['id']:(c,'symplectic_universal_arithmetic/provenance.json') for c in kx['claims']})
external=[]
for cid in sorted(set(sum(deps.values(),[]))-set(deps)):
    c,p=registry[cid]
    external.append(dict(claim_id=cid,title=c['title'],proof_location=copy.deepcopy(c['proof_location']),
        supplier_provenance=p,supplier_provenance_sha256=sha((ROOT/p).read_bytes())))

raw=(HERE/'main.tex').read_bytes()
lines=raw.splitlines(keepends=True)
claims=[]
for cid in deps:
    marker=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% BEGIN '+cid)
    a=next(i for i,l in enumerate(lines,1) if i>marker and l.decode().startswith('\\begin{'))
    b=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% END '+cid)-1
    while not lines[b-1].strip(): b-=1
    assert lines[b-1].decode().strip()==r'\end{proof}',(cid,b)
    piece=b''.join(lines[a-1:b])
    srcs=[source(path,name) for path,names in spec[cid].items() for name in names]
    claims.append(dict(id=cid,title=titles[cid],introduced_in='0.29',
        status='Complete human proof in the exact printed scope',
        mathematical_status=('Complete arithmetic supplier' if cid in ['QX1','QX4','QX5'] else 'Complete implication with exactly the stated antecedents'),
        scope=scopes[cid],depends_on=deps[cid],classical_inputs=use[cid],
        remaining_inputs=retained[cid],remaining_bespoke_inputs=bespoke[cid],
        source_relation='Explicit actual-data reconstruction; named classical replacements are matched separately. Source producer metadata is not evidence that a retained arithmetic hypothesis has been supplied.',
        proof_location=dict(file=COMP+'/main.tex',paragraph=cid,label='claim:'+cid,line_start=a,line_end=b,sha256=sha(piece),bytes=len(piece)),
        sources=srcs))

frontier_sources=[
 source(DT+'HidaU.lean','HidaUAlt','Retained full ordinary quotient producer; QX needs only rank4 actual Links'),
 source(DT+'THidaU.lean','hida_unitary_of_printed_hida','Retained exact type/control/Hecke-ideal producer'),
 source(DT+'PointTheoremBaseObject.lean','HidaPropsAlt','All six fields on one actual ideal are retained'),
 source(WG+'UniversalOrdinaryDeterminantRing.lean','P1core','Retained characteristic-ell prime-support assertion'),
 source(AV+'PatchingModules/AutomorphicDetection/PfromAut.lean','pFromAut','Original deeper patched-support producer, not supplied by adjoint vanishing'),
 source(AV+'PatchingModules/TaylorWilesObstructionBound.lean','PfromAut','Full exact incoming patched-module and cohomology hypotheses'),
 source(WG+'UniversalOrdinaryDeterminantRing.lean','P3core','Not used by the selected rank4 two-Link PMEx route; not promoted'),
]
auditpath=ROOT/'ordinary_support_dependency_audit/audit.json'
audit=json.loads(auditpath.read_text())
frontier={
 'QX-HIDA4':dict(status='retained arithmetic ideal-existence input',
    statement='On each actual QX4 rank4 Link over every allowed coefficient extension, every actual universal B and weight object Lambda admits the same ideal J0 with all six HidaPropsAlt fields, for the fixed original iota.',
    not_implied_by=['QX1 adjoint vanishing','KX8 universal Pair existence','a seed alone','finite weight-module structure alone'],
    actual_producer='THidaU -> HdEx / ExistsHeckeIdeal / TJRing / TJDense / HeckePolyCoeffZero / JEnd / JTwistA',
    source_anchors=frontier_sources[:3]),
 'QX-P1':dict(status='retained arithmetic support input on the same ideal',
    statement='For every actual NiceI finite-field power-series point matching B and killing the same J0, every prime below its kernel contains J0.',
    not_implied_by=['characteristic-zero tangent vanishing','residual multiplicity-free polarization without Schur hypotheses'],
    actual_producer='HasAut / PfromAut with exact norm/prime-choice/obstruction/patching inputs',
    source_anchors=frontier_sources[3:6]),
}
validation=dict(claim_count=len(claims),claim_source_anchor_count=sum(len(c['sources']) for c in claims),
    frontier_source_anchor_count=len(frontier_sources),source_file_count=len(files),
    human_proof_range_count=len(claims),every_source_file_checked_against_pinned_git_blob=True,
    source_commit=PIN,no_lean_build_or_kernel_replay=True)
out=dict(schema='rh-human-reconstruction-provenance/1',artifact_version='0.29',date='2026-11-22',
    component=COMP,repository=prior['repository'],commit=PIN,main_tex_sha256=sha(raw),
    scope='Complete adjoint, Link/IsPhi, twist, seed/NiceI support and arithmetic transport chains; exact five-clause PMEx remains conditional on actual rank4 HidaPropsAlt ideals and P1core.',
    claims=claims,source_files=list(files.values()),dependency_graph=deps,
    external_claim_dependencies=external,retained_frontier=frontier,
    new_classical_theorem_inputs=classical,
    complementary_producer_audit=dict(file='ordinary_support_dependency_audit/audit.json',sha256=sha(auditpath.read_bytes()),
        source_anchor_count=audit['validation']['source_anchor_count'],scope='Finite sufficient producer audit; no theorem installation.'),
    validation=validation)
dump('provenance.json',out)
endpoints=[
 dict(claim='QX1',endpoint='AdjointLiftingTheorem',status='complete original supplier; no new bespoke hypothesis'),
 dict(claim='QX4',endpoint='exists_two_links_same_kappa_not_dvd_of_fit_deep',status='complete actual construction on every Fit+Deep tower'),
 dict(claim='QX5',endpoint='exists_phi_universal_ordinary_det_ring_of_link',status='complete actual Pair and IsPhi construction'),
 dict(claim='QX10',endpoint='PMExAlt',status='complete constructor conditional on the stated actual rank4 ordinary-support ideal input',remaining_bespoke_inputs=['QX-HIDA4','QX-P1'])]
dump('closure.json',dict(schema='rh-component-closure/1',artifact_version='0.29',component=COMP,commit=PIN,
    main_tex_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
    closed_claim_ids=list(deps),dependency_graph=deps,external_claim_dependencies=external,
    endpoints=endpoints,retained_frontier=frontier,
    fully_closed_internal_subchains=[['QX1','QX3'],['QX4','QX5'],['QX4','QX5','QX6','QX7'],['QX4','QX5','QX8'],['QX4','QX5','QX9'],['QX4','QX5','QX6','QX7','QX8','QX9','QX10']],
    no_unconditional_PMExAlt=True,no_full_UnramifiedInputs=True,no_RH_or_GRH_claim=True,
    no_new_lean_build_or_kernel_replay=True))
dump('classical_inputs.json',dict(schema='rh-classical-input-registry/1',artifact_version='0.29',component=COMP,
    accessed='2026-11-22',main_tex_sha256=sha(raw),inputs=[dict(id=k,**v) for k,v in classical.items()]))
dump('input_registry.json',dict(schema='rh-component-input-registry/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),claim_inputs=external,retained_inputs=retained,retained_bespoke_inputs=frontier,
    classical_inputs=classical,proof_conditions_are_not_installed_arithmetic_suppliers=True))
dump('remaining_inputs.json',dict(schema='rh-component-remaining-inputs/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),retained_frontier=frontier,
    not_claimed=['Unconditional PMExAlt','Whole UnramifiedInputs','Whole HypothesesH-prime','All-rank HidaUAlt or ModUAlt','P3core','Uniform actual ProModAlt realization','Full paired CountII/CountIII or PointHV','RH or GRH'],
    clarification='The selected consumer requires only rank4 HidaPropsAlt and P1core on the same actual ideals. P3core is unused, not proved. The broader source packages remain uninstalled.'))
dump('frontier_registry.json',dict(schema='rh-component-frontier-registry/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),frontier=frontier,unused_source_field=frontier_sources[-1],
    complementary_audit_file='ordinary_support_dependency_audit/audit.json',
    complementary_audit_sha256=sha(auditpath.read_bytes()),
    rejected_shortcut=copy.deepcopy(audit['rejected_shortcut'])))
dump('next_targets.json',dict(schema='rh-next-source-targets/1',artifact_version='0.29',component=COMP,
    targets=[dict(id=k,title=v['status'],statement=v['statement'],sources=v['source_anchors']) for k,v in frontier.items()],
    target_retirement_policy='Retire AdjointLifting and actual Link/IsPhi producer subedges only. DA28-SP-01 as a whole remains because actual ordinary ideals and P1core are not yet supplied.'))
dump('source_validation.json',dict(schema='rh-source-validation/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),**validation))
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+
    '\n'.join(s['declaration']+'\n'+s['url']+'\n'+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
report=('Version 0.29 — actual symplectic modular support\n\n'
    'QX1 closes the literal AdjointLiftingTheorem. QX4 and QX5 construct the actual Links, Pair and universal comparison maps with the original threshold order. QX2--QX3, QX6--QX9 prove the substantive support and arithmetic transports. QX10 supplies all five PotentialModularityTower fields and literal PMExAlt conditional on exactly the retained rank-four ordinary support input.\n\n'
    'The ordinary ideal is not constructed here. Both six-field HidaPropsAlt and characteristic-ell P1core must hold on the same actual J0. No matched classical theorem was found that supplies them under the weaker source Resid/Fit/Deep hypotheses. The existing ANT theorem has extra residual-Schur, prime and local hypotheses, and is not installed. P3core is not used by this selected chain.\n\n'
    'Principal simplifications: Thorne removes residual-image hypotheses from the adjoint leaf; finite group-algebra interpolation proves integral twist invariance; QX8 proves every NiceI field directly in rank4, including ell=3; actual CSD temperedness plus explicit cyclic descent and the original local flags proves the entire IsAutQA/WitA return, so the broader H-prime package is unnecessary for this constructor.\n\n'
    + '\n'.join(cid+': '+scopes[cid] for cid in deps)+'\n\n'+json.dumps(validation,indent=2)+'\n')
(HERE/'report.txt').write_text(report)
(HERE/'README.txt').write_text('SYMPLECTIC MODULAR SUPPORT — VERSION0.29\n\n'
    'Read main.tex for the complete human arguments QX1--QX10. provenance.json binds each proof range to the exact pinned Lean definitions/producers and lists only stable claim dependencies. closure.json records both completed internal chains and the retained ordinary-support ideal input. input_registry.json and classical_inputs.json separate accepted named theorems from bespoke open assumptions. frontier_registry.json and next_targets.json give the exact remaining producer cut; ordinary_support_dependency_audit/audit.json contains the complementary 29-anchor producer map.\n\n'
    'Run build_provenance.py to reproduce byte/range checks and validate_tex.py for draft-mode syntax/reference checks. Research papers stay outside the release tree. No PDF, Lean build or kernel replay is performed. No unconditional PMExAlt, paired-count, PointHV, RH or GRH assertion is made.\n')
print(json.dumps(validation,indent=2))
