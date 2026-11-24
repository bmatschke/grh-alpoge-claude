#!/usr/bin/env python3
"""Rebuild exact PUN source/proof metadata. No Lean or kernel replay."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENT = HERE.name
VERSION = '0.48'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
repo = parser.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

A = 'src/Development/AbelianVarietyTheory/'
U = A + 'Proofs/UnitaryExistence/'
M = A + 'Proofs/ModuliProofs/'
G = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/'
T = G + 'BirationalGeometry/ToroidalCompactification/'
F = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'

# Inclusive pinned-blob ranges. None denotes the checked final line.
specs = {
 'host': (T+'TwoWeightEqOneAddRoot.lean',14,27,'Original Host: fixed rt/rt0/w0, conjugation, and everywhere-unramified O_F -> O_E'),
 'datum': (T+'TwoWeightEqOneAddRoot.lean',30,49,'Original finite projective Datum, perfect alternating form, rank and positive J with exact trace identities'),
 'level': (T+'TwoWeightEqOneAddRoot.lean',53,66,'Original Level: odd M>=3, half-ideal product/coprimality, A>0 and N=lcm(M,A)'),
 'SAB': (T+'TwoWeightEqOneAddRoot.lean',72,82,'Original SAB: actual cubical, symmetric, adjoint and primitive line identities'),
 'TateIso_Obj': (T+'TwoWeightEqOneAddRoot.lean',132,None,'Every original TateIso and Obj field, including n=0 addition/linearity and all geometric base fields'),
 'Moduli': (T+'PushInvertible.lean',12,44,'Actual KA/baseKA, dimension, representing Moduli and coefficient records'),
 'HasseNormSt': (A+'PublishedTheorems/Landherr₂/ExistsNormTensor.lean',10,None,'Whole original quadratic HasseNormSt, including square delta and every finite place'),
 'same_space': (U+'HermitianFormsSameSignatureSameSpace.lean',112,None,'Literal model_in_same_space with fixed Gm/xi, original lattices and all ranks'),
 'signature': (U+'SignatureHermitianModelOfDatum.lean',475,None,'Original signature_of_model: same p/q and exact trace-form convention'),
 'latModel': (A+'Definitions/ExistenceOfLattices/NormConst.lean',128,180,'Exact original principal subgroup, every LatModel field and NegXi'),
 'latModel_producer': (U+'LatticeModelOfSameSignatureHasseNorm.lean',24,None,'Whole original denominator and latModel_of_same_signature producer'),
 'half_congruence': (U+'ExistsEqNsmulOfDvdPairing.lean',14,None,'Original trivial_mod_of_trivial_on_half at integral precision M'),
 'finite_index': (U+'PrincipalLevelGroupFiniteIndexUnitaryStabiliser.lean',19,None,'Exact finite representatives with s inverse times gamma in princ'),
 'free_flags': (U+'PrincipalGroupActsFreelyOnFlags.lean',60,None,'Actual lattice stabilizer equivalence and princ_free on GG/Bor'),
 'transvection': (U+'TransvectionMemPrincipalCongruenceGroup.lean',20,None,'Original transv_mem_princ: one m before every vector, scalar and both kappa signs'),
 'Data': (G+'FundamentalDomains/Signature.lean',12,111,'Original left-linear herm, GG/Bor, IsUStab and all Data fields'),
 'ModelsOf_ModelBase': (A+'Definitions/ExistenceOfLattices/NormConst.lean',16,33,'Exact ModelsOf and all six ModelBase fields'),
 'models_producer': (U+'ExistsFlagDomainModelsOfFamilyUniformisation.lean',66,None,'Actual dataOf/exists_modelsOf with prescribed Gm/xi and supplied FamilyUnif'),
 'center_definitions': (F+'IntegrableOnIntegrand.lean',139,193,'Exact CuspFD, I/crdI/dualZE/dualOE/XcFD, skew/Hermitian, zMatE/zGam/nZ/IsZBasis and phase prE'),
 'LatZ_ExpoMatch': (F+'IntegrableOnIntegrand.lean',236,247,'Literal all-family LatZ and ExpoMatch with original all-cusp/all-matrix quantifiers'),
 'center_algebra': (U+'ZMatEInjective.lean',59,None,'Actual center action, additivity, unitarity, injectivity and subgroup'),
 'center_finite_generation': (U+'SpanCuspCentreArithmeticGroupFg.lean',32,None,'Exact displacement injection and finite generation of the original zGam'),
 'center_fullness': (U+'SkewMatrixMultipleInLattice.lean',20,None,'Integral denominator and finite-index positive multiple in the actual zGam'),
 'LatZ_producer': (U+'ArithmeticGroupCuspCentreLattice.lean',21,None,'Original exact integer-basis construction and whole latZ producer'),
 'periods': (T+'IsHolPeriods.lean',14,39,'Literal ordered type, IsPeriod, holomorphic test and dual-number derivative'),
 'period_existence': (U+'TypeFnPeriodExistModuliNonempty.lean',152,None,'Original typeFn_period_exist; PUN15 supplies its first two clauses, without using N1c'),
 'pseudo_basis': (U+'ExistsCuspPseudoBasisAdaptedLattice.lean',35,None,'Actual cusp pseudobasis in the same lattice and original field'),
 'center_congruence': (U+'MemPrincipalCongruenceInterCuspCentreIff.lean',45,None,'Exact principal-congruence/center intersection at modulus N'),
 'dual_coordinates': (U+'MemDualCuspCharacterLatticeIffAdaptedBasis.lean',17,None,'Actual crdI and dualOE(XcFD) coordinate dictionaries'),
 'trace_phase': (U+'CuspPairingIntIffHermitianExponentIntegral.lean',136,None,'Original prE, trace-one/factor-two calculation, and all-entry integrality equivalence'),
 'trace_one': (U+'CmFieldHostElementAddConjEqOne.lean',21,None,'Original host conjugation, w0+bar(w0)=1 and even trace on real codifferent elements'),
 'basis_change': (U+'ExponentMatchingIndependentOfCuspBasis.lean',53,None,'Exact center, cusp, phase and dual-coordinate transport for an arbitrary change of cusp basis'),
 'ExpoMatch_producer': (U+'FlagDomainModelsExponentsLevelM.lean',39,None,'Literal mem_gamma_iff and expoMatch_models for A=1, every rho'),
 'HolUnif_IsAH': (T+'IsLieBasis.lean',69,106,'Actual HolUnif, reading/frame conventions, rigidification, derivative and Appell-Humbert equation'),
 'RelAmple_KTriv': (G+'ExtensionDescent/NonzeroLocus.lean',28,75,'Original relative-ampleness and every-coefficient-ring KTriv tests'),
 'WeilIs': (G+'ExtensionDescent/ConstGen.lean',17,None,'Actual thetaLB, CommIsOf multiplication order and universally tested WeilIs'),
 'primitive_normalization': (M+'ExistsPrimitiveNormalisation.lean',330,None,'Original normalized line and primitive line supplier; PUN20 gives a direct complex Appell-Humbert argument'),
 'principal_torus': (M+'PrincipalTorusAlgebraic.lean',1,None,'Original principalTorus_algebraic contract'),
 'tate_periods': (M+'ExistsTateIsoOfPeriods.lean',120,None,'Actual all-field TateIso from compatible marked periods'),
 'Lie_and_half_level': (M+'DetCondOfEigenbasis.lean',1,None,'Exact DetCond from the eigenbasis and the actual half-level marking'),
 'point_period': (M+'ExistsPointOfIsPeriod.lean',24,None,'Whole original exists_point_of_isPeriod with every field and both level identities'),
 'point_equality': (M+'PointEqIffIsometryClosed.lean',19,None,'Whole original point_eq_iff_isometry_closed with exact half/full congruences'),
 'InGenus_Unif': (M+'FamilyUnifOfParts.lean',18,42,'Literal marked InGenus and individual Unif predicates'),
 'genus_nonempty': (M+'FamilyUnifOfParts.lean',63,84,'Original exists_inGenus construction and positive-n,m guards'),
 'FamilyUnif_N1c': (T+'IsHolPeriods.lean',41,None,'Full simultaneous theta-frame, FamilyUnif and N1c contracts; retained boundary'),
 'remaining_point_extraction': (M+'ExistsUniformisationAtPointClosed.lean',1,None,'Original reverse uniformization-at-point producer; not supplied in PUN'),
 'remaining_local_lift': (M+'ExistsLocalPeriodLift.lean',1,None,'Original local period lift preserving the prescribed initial period; not supplied in PUN'),
 'remaining_hol_family': (M+'IsHolToModulipointExpOfHolomorphicPeriodsStatement.lean',1,None,'Original arbitrary holomorphic period-family/moduli/exponential producer; not supplied in PUN'),
 'remaining_theta_family': (M+'ExistsThetaFrameFamily.lean',1,None,'Original simultaneous theta frame and per-fiber algebraic section; not supplied in PUN'),
 'remaining_frame_contracts': (A+'Definitions/ExistenceOfLattices/NormConst.lean',35,126,'Actual FrameOK/FramesOK/CoverTri/FibTri with Gaussian norm and all weights'),
 'principal_endpoint': (U+'CongrOfDvdModulus.lean',26,None,'Literal congruence transport and exists_unf_hasPrinc endpoint; not closed by PUN'),
}

relations = {
 1:(['MF4'],['HasseNormSt']),
 2:(['MF3','MF4'],['HasseNormSt','same_space']),
 3:([],['host','datum','signature','Data']),
 4:(['PCL2','PCL3','MF2'],['host','datum','same_space']),
 5:([2,3,4,'PCL1'],['same_space','datum']),
 6:([],['level','datum','half_congruence','latModel']),
 7:([6],['finite_index','latModel']),
 8:([6],['free_flags','Data','level']),
 9:([6],['transvection','Data']),
 10:([5,7,8,9],['latModel','latModel_producer']),
 11:([3,10],['ModelsOf_ModelBase','models_producer','Data','FamilyUnif_N1c']),
 12:([],['center_definitions','center_algebra']),
 13:([12],['center_definitions','center_finite_generation','center_fullness','Data']),
 14:([12,13],['LatZ_ExpoMatch','LatZ_producer','Data']),
 15:([],['host','datum','periods','period_existence']),
 16:(['PCL2'],['pseudo_basis','dual_coordinates','datum']),
 17:([6,12,16],['center_congruence','center_definitions','ModelsOf_ModelBase']),
 18:([17],['trace_phase','trace_one','center_definitions']),
 19:([16,17,18,'PCL2'],['dual_coordinates','basis_change','ExpoMatch_producer','LatZ_ExpoMatch']),
 20:([],['host','SAB','periods','HolUnif_IsAH','RelAmple_KTriv','primitive_normalization','principal_torus']),
 21:([20],['WeilIs','HolUnif_IsAH','TateIso_Obj']),
 22:([20,21],['point_period','tate_periods','Lie_and_half_level','TateIso_Obj','Moduli','periods']),
 23:([20,21],['point_equality','SAB','Moduli','InGenus_Unif']),
 24:([15,22,'MF2'],['InGenus_Unif','genus_nonempty','host','level','Moduli']),
}

conrad = 'https://math.stanford.edu/~conrad/papers/cmchina.pdf'
milne = 'https://www.jmilne.org/math/CourseNotes/AV.pdf'
foundations = [
 {'id':'PUN_STANDARD_ALGEBRA','kind':'standard_algebraic_foundations','name':'Number fields, Dedekind ideals and finite linear algebra','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Finite torsion-free modules over Dedekind domains are projective; nonzero fractional ideals are invertible; the field trace is nondegenerate and the codifferent is its integral dual. Smith reduction, elementary finite-dimensional linear algebra, completions and the Chinese remainder theorem are used. Integral symplectic bases exist for perfect alternating Z-forms.',
  'application_checked':'The actual nonfree lattice, exact trace-dual scalar, integral pseudobasis, center congruence ideals and exact phase are proved in PUN, rather than inferred from a commensurable replacement.'},
 {'id':'PUN_HASSE_MINKOWSKI','kind':'named_published_foundation','name':'Hasse-Minkowski over a number field','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'A nondegenerate quadratic form over a number field is isotropic if it is isotropic over every completion.',
  'inherited_human_locator':'MF4','application_checked':'PUN1 handles square delta explicitly and complex completions automatically. PUN2 handles both t nonzero and a global isotropic vector at t=0, and local cancellation includes split algebras.',
  'references':[{'author':'Jonathan Hanke','title':'Quadratic Forms and Automorphic Forms','location':'Theorem 1.9.1 and Remark 1.9.2, printed p. 20','url':'https://swc-math.github.io/aws/2009/09HankeNotes.pdf','checked_in_inherited_packet':'mass_formula/MF4'},{'author':'Sungjin Kim','title':'Hasse-Minkowski Theorem','location':'Theorem 1.1','url':'https://www.csun.edu/~sungjin/HasseMinkowski.pdf','checked_in_inherited_packet':'mass_formula/MF4'}]},
 {'id':'PUN_ORIGINAL_ARITHMETIC_DATA','kind':'original_quantified_input_data','name':'Original Host, Datum, Level and fixed Hermitian model','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'The actual Host, finite projective perfect alternating Datum, Level and each theorem printed fixed Hermitian-space hypotheses remain exactly as quantified. PUN does not construct the common field/host/Moduli family. The same Gm, xi0, embedding type and original lattices are retained.',
  'source_groups':['host','datum','level','same_space']},
 {'id':'PUN_SUPPLIED_FAMILY','kind':'retained_original_hypothesis','name':'A supplied original FamilyUnif','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'PUN11 quantifies over the original supplied FamilyUnif and constructs all its ModelsOf/ModelBase/NegXi fields on the prescribed Hermitian space. It does not prove N1c.',
  'source_groups':['ModelsOf_ModelBase','FamilyUnif_N1c']},
 {'id':'PUN_ORIGINAL_DATA_CUSPS','kind':'original_quantified_input_data','name':'Original all-family Data and CuspFD inputs','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'PUN12-PUN14 use every original Data, arbitrary component type, every rank and every CuspFD. Finite index is the original Gamma_index field; no normality or additional principal-level condition is assumed.'},
 {'id':'PUN_MODELBASE_FOR_EXPONENTS','kind':'retained_original_hypothesis','name':'Exact supplied ModelBase for ExpoMatch','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'PUN17-PUN19 retain the literal model with its integral equivalence, trace pairing and exact original principal group, and A=1 for the final exponent theorem. This is the source expoMatch_models scope.'},
 {'id':'PUN_COMPLEX_ANALYSIS','kind':'standard_analytic_foundations','name':'Complex tori, analytic coverings and tangent derivations','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'A full discrete lattice defines a compact complex torus; its quotient is the universal cover. Holomorphic additive maps are complex linear. Smooth-scheme tangent vectors are derivations or maps from dual numbers. Global holomorphic functions on a connected compact complex manifold are constant.',
  'application_checked':'PUN15 constructs the actual periods directly from the positive complex structure; PUN20 and PUN23 give the precise source tangent and integral-kernel dictionaries.'},
 {'id':'PUN_RIEMANN_ALGEBRAICITY','kind':'named_published_foundation','name':'Riemann algebraicity and algebraic/analytic torus equivalence','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'A complex torus with a positive integral Riemann form is the analytification of an abelian variety; analytic homomorphisms between such tori are algebraic.',
  'application_checked':'The supplied IsPeriod gives the exact positive Hermitian form with imaginary part the original integral perfect B. PUN20 uses the resulting original torus and R-action; it does not appeal to a moduli-uniformization theorem.',
  'references':[{'author':'J. S. Milne','title':'Abelian Varieties, version 2.0, 16 March 2008','location':'Chapter I, Theorems 2.8-2.9, printed p. 14 / PDF p. 20','url':milne,'checked_online':True},{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic, 8 July 2005','location':'Example 4.1.4, printed p. 34 / PDF p. 34','url':conrad,'checked_online':True}]},
 {'id':'PUN_APPELL_HUMBERT','kind':'named_published_foundation','name':'Appell-Humbert classification and positivity','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Hermitian-form/semicharacter factors classify holomorphic line bundles on a complex torus. The line is ample precisely when its Hermitian form is positive definite.',
  'application_checked':'PUN20 explicitly constructs alpha(Pa)=exp(pi i B(a,w0 a)), verifies the cocycle, symmetry, adjoint and primitive identities, and writes the normalized cubic cancellation. PUN21 computes the actual source commutator sign; PUN23 uses prim to identify the line itself.',
  'references':[{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic','location':'Theorem 2.2.3, printed p. 16 / PDF p. 16; Theorem 3.1.3, printed p. 24 / PDF p. 24','url':conrad,'checked_online':True}]},
 {'id':'PUN_GAGA','kind':'named_published_foundation','name':'GAGA for the projective complex varieties used here','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Analytification identifies coherent algebraic and analytic sheaves and their homomorphisms on a projective complex variety, and algebraizes the analytic maps between the projective varieties in use.',
  'application_checked':'Every application is to a constructed projective torus, its finite powers, a line bundle, its generators or a map of these varieties. No analytic relative theta-family or general nonproper algebraization theorem is inferred.',
  'references':[{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic','location':'Example 4.1.4, printed p. 34 / PDF p. 34','url':conrad,'checked_online':True}]},
 {'id':'PUN_PICARD_ALL_SCHEMES','kind':'named_published_foundation','name':'Dual abelian variety with universal Poincare bundle on all test schemes','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'The dual abelian variety represents the rigidified algebraically trivial line-bundle functor on every test scheme and commutes with field extension.',
  'application_checked':'PUN20 proves that the polarization map is an isomorphism using the perfect integral B. The original KTriv hypothesis gives a trivial translation class Zariski locally on Spec(A0), so its image in the represented functor is zero; the isomorphism forces x=0 for arbitrary, possibly nonreduced, C-algebras A0.',
  'references':[{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic','location':'Theorem 4.3.2, printed p. 39 / PDF p. 39','url':conrad,'checked_online':True},{'author':'J. S. Milne','title':'Abelian Varieties, version 2.0','location':'Chapter I, Remark 8.7, printed pp. 36-37 / PDF pp. 42-43; paragraph immediately preceding Remark 8.15, printed p. 40 / PDF p. 46, explicitly every scheme T','url':milne,'checked_online':True}]},
 {'id':'PUN_PROPER_GLOBAL_FUNCTIONS','kind':'standard_algebraic_geometric_foundation','name':'Global functions on a proper geometrically connected reduced variety','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'For a proper geometrically connected geometrically reduced variety over a field, global functions are the base field and this remains true after any field extension.',
  'application_checked':'PUN21 applies this only to the original constructed abelian variety after C -> k, so any two global generators differ by a scalar in k and the universal WeilIs condition follows.',
  'references':[{'author':'The Stacks Project Authors','title':'The Stacks Project','location':'Tag 0E0L, the proper flat geometrically reduced connected universal base-functions statement, as already checked in CNC1','url':'https://stacks.math.columbia.edu/tag/0E0L','checked_in_inherited_packet':'canonical_cusp_connection_v47/CNC1'}]},
 {'id':'PUN_SUPPLIED_MODULI','kind':'original_quantified_input_data','name':'The actual supplied Moduli record and marked period data','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'PUN22-PUN24 retain the original supplied Xo:Moduli D l, fixed sigma with the exact rt0 law, ordered IsTypeFn, positive p+q where required, and all compatible marked-period hypotheses. Existence of the representing scheme is not constructed.',
  'source_groups':['Moduli','point_period','point_equality','InGenus_Unif']},
]

external = {
 1:['PUN_HASSE_MINKOWSKI'], 2:['PUN_HASSE_MINKOWSKI','PUN_STANDARD_ALGEBRA'],
 3:['PUN_ORIGINAL_ARITHMETIC_DATA','PUN_STANDARD_ALGEBRA'],
 4:['PUN_ORIGINAL_ARITHMETIC_DATA','PUN_STANDARD_ALGEBRA'],
 5:['PUN_ORIGINAL_ARITHMETIC_DATA'], 6:['PUN_ORIGINAL_ARITHMETIC_DATA','PUN_STANDARD_ALGEBRA'],
 7:['PUN_STANDARD_ALGEBRA'],8:['PUN_STANDARD_ALGEBRA','PUN_COMPLEX_ANALYSIS'],
 9:['PUN_STANDARD_ALGEBRA'],10:['PUN_ORIGINAL_ARITHMETIC_DATA'],
 11:['PUN_SUPPLIED_FAMILY','PUN_ORIGINAL_ARITHMETIC_DATA'],
 12:['PUN_ORIGINAL_DATA_CUSPS','PUN_STANDARD_ALGEBRA'],
 13:['PUN_ORIGINAL_DATA_CUSPS','PUN_STANDARD_ALGEBRA'],
 14:['PUN_ORIGINAL_DATA_CUSPS','PUN_STANDARD_ALGEBRA'],
 15:['PUN_ORIGINAL_ARITHMETIC_DATA','PUN_STANDARD_ALGEBRA','PUN_COMPLEX_ANALYSIS'],
 16:['PUN_STANDARD_ALGEBRA'],17:['PUN_MODELBASE_FOR_EXPONENTS'],
 18:['PUN_STANDARD_ALGEBRA','PUN_ORIGINAL_ARITHMETIC_DATA'],19:['PUN_MODELBASE_FOR_EXPONENTS'],
 20:['PUN_ORIGINAL_ARITHMETIC_DATA','PUN_COMPLEX_ANALYSIS','PUN_RIEMANN_ALGEBRAICITY','PUN_APPELL_HUMBERT','PUN_GAGA','PUN_PICARD_ALL_SCHEMES'],
 21:['PUN_GAGA','PUN_PROPER_GLOBAL_FUNCTIONS'],
 22:['PUN_SUPPLIED_MODULI','PUN_STANDARD_ALGEBRA','PUN_GAGA'],
 23:['PUN_SUPPLIED_MODULI','PUN_COMPLEX_ANALYSIS','PUN_APPELL_HUMBERT','PUN_GAGA'],
 24:['PUN_SUPPLIED_MODULI','PUN_ORIGINAL_ARITHMETIC_DATA','PUN_STANDARD_ALGEBRA'],
}

scopes = {
 1:'Every original number field, nonzero delta and x, every real embedding and finite place, with square delta and all dyadic places included.',
 2:'All finite dimensions, indefinite Hermitian spaces allowed, every local completion including split algebras; exact E-isometry.',
 3:'Same original positive J, trace sign, ordered CM type and p/q; no accidental interchange of signatures.',
 4:'Actual unramified Host, arbitrary projective integral lattices, exact shared xi and different scalar at every finite place including 2.',
 5:'Whole literal model_in_same_space on fixed Gm and xi; zero-xi case forces the original zero lattice and is retained.',
 6:'Exact original half-lattice condition and whole-level condition, equality with the kernel modulo lcm(M,A), not just inclusion.',
 7:'Actual finite representatives, with original left-coset factor order s inverse gamma.',
 8:'Every original flag and every b in Bor, all signatures, original odd M>=3 and no omitted small prime.',
 9:'One m before every integral isotropic vector, every real integral scalar, and both original kappa0 signs.',
 10:'Every original LatModel field; same Gm, xi0, integral lattice and principal subgroup.',
 11:'Whole ModelsOf/ModelBase/NegXi producer conditional only on its original supplied FamilyUnif and fixed model hypotheses.',
 12:'Every original CuspFD, all ranks including zero; actual zMatE action and exact additive law.',
 13:'Actual zGam itself finitely generated with full skew-Hermitian rational span; finite index need not be normal.',
 14:'Whole LatZ for every original component type, family and cusp rank, with original nZ=card(Psi)*rho^2.',
 15:'Every original ordered type, exact g=[E:Q]/2*(p+q), all IsPeriod fields; no N1c used.',
 16:'Exact original primitive cusp intersection and fractional-ideal pseudobasis; exact surjectivity onto conjugate-ideal trace duals.',
 17:'Actual center intersection with the original principal group, A=1, modulus M, no saturation or denominator-only substitute.',
 18:'Original phase denominator kappa0/2, both kappa signs, all Hermitian arguments, trace-one w0 handles the factor two at dyadic places.',
 19:'Whole ExpoMatch_models on the supplied original ModelBase, for every rho and every original cusp, A=1 and exact original XcFD.',
 20:'Actual primitive rigidified cubical line on each original period torus; full KTriv on every C-algebra including nonreduced rings.',
 21:'Original CommIsOf multiplication order and negative Weil sign; every positive n and every C -> k scalar extension.',
 22:'Whole exists_point_of_isPeriod with original fixed sigma/type, positive rank, compatible f_n/nu_n and both exact level markings; every Obj.geom field.',
 23:'Whole point_eq_iff_isometry_closed for arbitrary original period-point data, actual primitive line, full integral form and half/full marked congruences.',
 24:'Actual InGenus at every prescribed sigma, with D prime = D, all positive-n,m guards and exact root identity; actual moduli nonemptiness for positive rank.',
}

files = {}; sources = {}; excerpts = []
for key,(rel,lo,hi,title) in specs.items():
    data=(repo/rel).read_bytes()
    assert data == subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel]),rel
    lines=data.splitlines(keepends=True); hi=hi or len(lines)
    assert 1 <= lo <= hi <= len(lines),(key,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi]); base=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':base}
    sources[key]={'id':'PUN_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':lo,'line_end':hi,'source_commit':PIN,'file_sha256':sha(data),'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':base+f'#L{lo}-L{hi}'}
    excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

body=(HERE/'main.tex').read_text()
assert not any(ord(c)<32 and c not in '\n\t' for c in body)
main_sha=sha(body.encode()); claims=[]; foundation_ids={f['id'] for f in foundations}
for i,(deps,groups) in relations.items():
    cid=f'PUN{i}'; match=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',body,re.M|re.S)
    assert match and r'\label{claim:'+cid+'}' in match.group(),cid
    ds=[f'PUN{d}' if isinstance(d,int) else d for d in deps]
    assert all(not d.startswith('PUN') or int(d[3:])<i for d in ds)
    assert set(external.get(i,[])) <= foundation_ids
    lo=body[:match.start()].count('\n')+1
    claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1),'introduced_in':VERSION,'classification':'B','depends_on':ds,'external_input_ids':external.get(i,[]),'scope_note':scopes[i],'source_groups':groups,'sources':[sources[k] for k in groups],'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':lo,'line_end':lo+match.group().count('\n')-1,'sha256':sha(match.group().encode()),'bytes':len(match.group().encode())},'source_proof_is_not_human_proof':True})

inherited=[]
for cid in ['MF2','MF3','MF4','PCL1','PCL2','PCL3']:
    rel='mass_formula/main.tex' if cid.startswith('MF') else 'principal_cusp_lattices_v47/main.tex'
    p=ROOT/rel; text=p.read_text()
    if cid.startswith('MF'):
        m=re.search(r'^\\paragraph\{'+cid+r':.*?(?=^\\paragraph\{MF\d+:|\Z)',text,re.M|re.S)
    else:
        m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':rel,'file_sha256':sha(p.read_bytes()),'claim_sha256':sha(m.group().encode()),'line_start':text[:m.start()].count('\n')+1,'line_end':text[:m.end()].count('\n'),'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False})

reviews=[]; reviewed=set(); lookup={c['id']:c['proof_location']['sha256'] for c in claims}
for p in sorted(HERE.glob('review_*.json')):
    r=json.loads(p.read_text()); assert r.get('status',r.get('result'))=='PASS',p
    ids=[]; stale=False
    for e in r.get('claims_reviewed',r.get('reviewed_claims',[])):
        cid=e if isinstance(e,str) else e.get('id',e.get('claim'))
        expected=r.get('proof_hashes',{}).get(cid) if isinstance(e,str) else e.get('proof_range_sha256',e.get('block_sha256'))
        assert cid in lookup,(p,cid)
        stale=stale or expected!=lookup[cid]; ids.append(cid)
    if stale: continue
    reviewed.update(ids)
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':r.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':r.get('proof_file_sha256',r.get('proof_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids})
status='complete_at_stated_scope_independently_reviewed' if set(lookup)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
for c in claims:
    c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
    c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]

completed=[
 {'endpoint':'GlobalTheory.Published.HasseNormSt','claim':'PUN1','status':'whole_literal_theorem_written_from_named_Hasse_Minkowski','scope':scopes[1]},
 {'endpoint':'GlobalTheory.model_in_same_space','claim':'PUN5','status':'whole_literal_fixed_space_constructor_written','scope':scopes[5]},
 {'endpoint':'GlobalTheory.LevelHalf.trivial_mod_of_trivial_on_half','claim':'PUN6','status':'whole_literal_integral_congruence_implication_written','scope':scopes[6]},
 {'endpoint':'GlobalTheory.FrameUnif.latModel_of_same_signature','claim':'PUN10','supporting_claims':['PUN7','PUN8','PUN9'],'status':'whole_literal_LatModel_constructor_written','scope':scopes[10],'supporting_endpoints':['GlobalTheory.FrameUnif.princ_finiteIndex','GlobalTheory.PrincFree.princ_free','GlobalTheory.PrincTransv.transv_mem_princ']},
 {'endpoint':'GlobalTheory.ModelsExist.exists_modelsOf','claim':'PUN11','status':'whole_literal_constructor_at_original_supplied_FamilyUnif','scope':scopes[11]},
 {'endpoint':'GlobalTheory.CuspCentre.latZ','claim':'PUN14','status':'whole_literal_all_family_all_rank_supplier_written','scope':scopes[14]},
 {'endpoint':'GlobalTheory.PeriodExists.typeFn_period_exist, first two conjuncts','claim':'PUN15','status':'complete_original_type_and_period_producers_written','scope':scopes[15]},
 {'endpoint':'GlobalTheory.ExpoModels.expoMatch_models','claim':'PUN19','status':'whole_literal_A_equals_one_exponent_supplier_written','scope':scopes[19]},
 {'endpoint':'Canonical primitive line / actual Out.KTriv on each original period torus','claim':'PUN20','status':'explicit_actual_object_constructor_from_named_classical_foundations','scope':scopes[20]},
 {'endpoint':'Original Out.WeilIs on all period torsion points','claim':'PUN21','status':'literal_commutator_and_base_change_proof_written','scope':scopes[21]},
 {'endpoint':'GlobalTheory.Moduli.exists_point_of_isPeriod','claim':'PUN22','status':'whole_literal_individual_point_constructor_written','scope':scopes[22]},
 {'endpoint':'GlobalTheory.UnifPoint.point_eq_iff_isometry_closed','claim':'PUN23','status':'whole_literal_individual_point_equality_written','scope':scopes[23]},
 {'endpoint':'GlobalTheory.UnifParts.exists_inGenus and complex point nonemptiness at fixed sigma','claim':'PUN24','status':'actual_marked_genus_constructor_written','scope':scopes[24]},
]
boundaries=[
 'The supplied original Host, Datum, Level and Moduli record are retained; no common field or representing moduli scheme is constructed.',
 'N1c is not closed. Reverse uniformization at an arbitrary given moduli point, local period lifting with the prescribed initial period, holomorphic moduli/exponential dependence for arbitrary period families, the simultaneous theta frame and finite-family assembly remain.',
 'PUN11 constructs ModelsOf/ModelBase/NegXi for a supplied FamilyUnif; it does not choose or prove that family.',
 'FramesOK, CoverTri and FibTri remain: simultaneous normalized framed points, the exact Gaussian mean norm, all triangular weight characters, arithmetic invariance, readings, cover and fiber comparison on the same family.',
 'The final IsUnf and FromTest dictionary must use the same constructed framed points. The complete FrameUnif.exists_unf_hasPrinc endpoint is not supplied.',
 'The same common field/metric/measure/phase obligations, unconditional full LatFull, higher CoversAt, all-tuple ClsEx/PointIdentCore/ClassSumsSpan, and full RH/GRH are not inferred.',
]
contract={'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'claims':'PUN1-PUN24','claim_count':24,'classification_note':'All 24 numbered claims are class B written deductions. Named published foundations are separately recorded external inputs, not synthetic numbered DAG claims.','main_outcome':'Original fixed-space arithmetic lattice/flag models, all-family center lattices, exact A=1 exponent matching, periods, and actual individual primitive moduli points with every geometric/torsion/level clause.','completed_source_endpoints':completed,'quantifier_order':['Retain the original Host/Datum/Level, every prescribed complex base embedding and ordered type.','For arithmetic model construction retain the same fixed Gm and xi, then construct an exact integral model for each original datum of the same signature.','Choose the transvection modulus before every isotropic lattice vector, real integral scalar and either kappa sign.','For every supplied FamilyUnif choose ModelsOf on the same fixed Gm/xi with exact principal groups.','Construct LatZ for every original component family and every rank; construct ExpoMatch for every cusp and rho of an original ModelBase when A=1.','Given all original compatible f_n and nu_n, construct each moduli point with every positive torsion level, every scalar extension C -> k, and the original two markings.','Do not interchange these individual constructions with existence of a finite holomorphic FamilyUnif or its normalized framed points.'],'literal_normalizations':{'Hermitian':'linear in the first variable, h_G(x,y)=x^t G conjugate(y)','arithmetic_trace':'B=Tr(xi h), with xi=-xi0 for original ModelBase','principal_modulus':'N=lcm(M,A), and M when A=1','phase':'prE uses kappa0/2 and equals +/- one-half the rational trace in PUN18','cusp_lattice':'the actual zGam, not a commensurable lattice','exponent_lattice':'original XcFD(1,cu) and dualOE','canonical_semicharacter':'alpha(Pa)=exp(pi i B(a,w0 a))','Weil_sign':'exp(-2 pi i B(a,b)/n)','root_at_A':'sigma(zeta_A)=exp(-2 pi i nu_A/A)','level_maps':'eta on conjugate(Mb)*L, etaA on all L'},'all_finite_places_including_two':True,'original_prime_three_not_excluded':True,'rank_zero_in_generic_arithmetic_claims':True,'positive_rank_in_individual_moduli_contract_retained':True,'all_KTriv_coefficient_algebras_including_nonreduced':True,'all_geometric_base_fields_and_embeddings_retained':True,'no_free_O_lattice_assumption':True,'no_ideal_principalization_or_saturation_substitute':True,'retained_input_ids':[f['id'] for f in foundations],'not_supplied':boundaries,'whole_obligations_closed':[],'non_premise_references':[{'location':'Final remaining-boundary subsection','references':['N1c','FrameOK','FramesOK','CoverTri','FibTri','IsUnf','FromTest','LatFull','CoversAt','ClsEx','PointIdentCore','ClassSumsSpan'],'reason':'Exact remaining source contracts and later consumers, not asserted proved premises.'}]}
manifest={'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,'file_count':len(files),'range_count':len(sources)}
prov={'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'main_tex_sha256':main_sha,'status':status,'claims':claims,'source_groups':sources,'inherited_human_inputs':inherited,'classical_and_foundational_inputs':foundations,'independent_reviews':reviews,'dependency_convention':'depends_on contains only numbered human proofs. Original records, named classical foundations and remaining producer hypotheses use separate external_input_ids.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
dag={'schema':'rh-component-human-claim-dag/1','artifact_version':VERSION,'component':COMPONENT,'nodes':[{'id':c['id'],'classification':c['classification'],'scope_note':c['scope_note'],'proof_sha256':c['proof_location']['sha256']} for c in claims],'inherited_nodes':inherited,'edges':[{'from':d,'to':c['id']} for c in claims for d in c['depends_on']],'external_inputs_are_not_DAG_claims':True}
closure={'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'completed_source_endpoints':completed,'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'remaining':boundaries,'full_LatZ_supplied':True,'full_A_equals_one_ExpoMatch_at_original_ModelBase_supplied':True,'full_modelsOf_at_supplied_FamilyUnif_supplied':True,'full_individual_point_and_equality_suppliers_written':True,'full_N1c_supplied':False,'full_principal_uniformization_supplied':False,'full_LatFull_unconditional_supplier_closed':False,'independent_reviews':reviews,'pending_independent_review':sorted(set(lookup)-reviewed),'validation':'Two-pass standalone draft TeX, no PDF, no Lean replay; exact pinned Git blobs and independently authored hash-bound reviews.'}
for name,obj in [('provenance.json',prov),('source_manifest.json',manifest),('contracts.json',contract),('original_contracts.json',contract),('closure.json',closure),('claim_dag.json',dag),('retained_foundations.json',foundations),('classical_inputs.json',foundations)]:
    (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
report=[
 'PRINCIPAL UNIFORMIZATION SUPPLIERS — v0.48',
 'Source pin: '+PIN,'Proof SHA256: '+main_sha,
 f'Claims: 24; source files: {len(files)}; exact ranges: {len(sources)}; inherited human bindings: {len(inherited)}.',
 'Status: '+status,'',
 'PUN1-PUN5 derive the literal quadratic Hasse norm theorem and place every original',
 'perfect alternating datum of the same signature into the prescribed Hermitian space.',
 'The direct quadratic induction handles a global isotropic vector and split local',
 'algebras; the local common scalar comes from the exact trace dual and the unramified',
 'Host. All finite places, including dyadic ones, and the original ranks are retained.',
 '',
 'PUN6-PUN11 prove the integral half-level-to-full-level congruence, finite index with',
 'the source factor order, flag freeness, one simultaneous transvection modulus,',
 'every LatModel field, and the full ModelsOf/ModelBase/NegXi constructor for a',
 'supplied original FamilyUnif. Fixed Gm/xi, original lattices and groups are unchanged.',
 '',
 'PUN12-PUN14 construct the original zGam itself as a full integer lattice for every',
 'family and cusp rank. PUN15 constructs periods for every ordered original type.',
 'PUN16-PUN19 use an exact fractional-ideal pseudobasis, integral trace perfection,',
 'the original kappa0/2 phase and w0+bar(w0)=1 to prove the entire A=1 ExpoMatch.',
 'No ideal principalization, saturation or bounded-denominator substitute is used.',
 '',
 'PUN20-PUN24 construct the canonical primitive Appell-Humbert line, the exact negative',
 'Weil pairing, the whole individual marked-period-to-moduli-point endpoint, equality',
 'by marked integral isometry, and actual marked genus nonemptiness at every fixed',
 'base embedding. The KTriv proof covers arbitrary nonreduced C-algebras; Obj.geom',
 'covers every algebraically closed field and every C-to-k embedding without continuity.',
 '',
 'Hasse-Minkowski, Riemann algebraicity, Appell-Humbert/positivity, GAGA and the',
 'all-scheme Poincare/Picard theorem are separately named published foundations.',
 'Their applications are checked; their global classical proofs are not counted as',
 'new numbered deductions. All 24 PUN claims are class B human deductions.',
 '',
 'The original Moduli scheme is supplied. N1c is not closed: reverse extraction, local',
 'period lifting, holomorphic period-family dependence, the simultaneous theta frame',
 'and finite-family assembly remain. The exact normalized frame/metric, cover/fiber',
 'and FromTest constructors also remain. The complete exists_unf_hasPrinc, unconditional',
 'LatFull, higher covers and all-tuple common-family obligations are not inferred.',
 '',
 'Rebuild: python build_metadata.py --repo /path/to/formal_source',
 'Validate: python validate_tex.py --format /path/to/pdflatex.fmt',
 'All sources are compared with the pinned Git blobs. The proof blocks and inherited',
 'inputs are SHA256-bound. Root/shared files, source files and frozen packets are untouched.',
]
(HERE/'report.txt').write_text('\n'.join(report)+'\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'artifact_version':VERSION,'component':COMPONENT,'hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_human_inputs':len(inherited),'proof_file_sha256':main_sha,'status':status},indent=2))
