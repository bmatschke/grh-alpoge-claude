#!/usr/bin/env python3
"""Reproduce the CW source ledger from immutable Lean bytes, without a build.

This script checks the canonical full-Weil reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
I = D + 'Proofs/IwasawaDecomposition/'
G = D + 'Proofs/GlobalInterpolation/'
A = D + 'Definitions/AutomorphicMembership/'
F = D + 'Definitions/Foundations/'
W = D + 'Definitions/GlobalTwisting/'
H = 'src/Formalism/HermitianLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]

def whole_decls(path, role='substantive_local_proof_and_definitions'):
    """Link each declaration separately; never hash a reconstructed source."""
    _, _, decls = read_source(path)
    return [source(path, d['qualified'], role) for d in decls]

V = D+'Proofs/DivisorProofs/'
AL = D+'Proofs/AdelicLatticeProofs/'
FND = D+'Proofs/FoundationProofs/'
T = D+'Proofs/TwistedOperators/'
DV = D+'Definitions/Divisors/'
FORM = 'src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean'
DEFS = 'src/Formalism/LocalToGlobal/BesselHermitianTheta/DefsReal.lean'
PARTS = DV+'IsUnitaryOnTheta.lean'
FIN = V+'ExistsIsFinWeil.lean'
RHO = V+'ActOMemFinSub.lean'
REAL = V+'ExistsOscillatorActionOfGaussianPairings.lean'
FOUR = V+'ContinuousFourierGau.lean'
COMP = V+'LintegralNormSqEqToL2.lean'
INF = V+'LintegralEqOfNorms.lean'
RAT = V+'ThetaDistributionInvariantRationalTarget.lean'
FD = V+'FiniteDetSmulSubOne.lean'
GAUSS = V+'GaussianPoincareSeriesThetaVacuum.lean'
UNF = V+'RationalIsometryVacuumScalarGaussSumIntegral.lean'
RINT = V+'IntegralGaussianRealIsometryNoFixed.lean'
ETA = V+'EtaTildeHeckeCharSplitMulSignOfNormFormula.lean'
CANON = V+'ExistsWeilDatumPowersUnramifiedEtaTilde.lean'
GEN = V+'ExistsWeilDatumOfSplittingCharacters.lean'
TWIST = V+'ExistsWeilDatumTwistHeckeCharacters.lean'
BOT = T+'BottomExistsIntegrable.lean'
NFBOT = T+'NormalFormBottom.lean'

common=[
 'The literal D7 arithmetic CM host, sign-minus-one standard additive character, actual infinity family, original Hermitian spaces and original host.AA trace-dual Hom lattice are fixed.',
 'CW1--CW23 take full self-dual integral lattices and the exact stated IsEtaTilde input for the canonical endpoint. Ranks may be zero and need not be even.',
 'The generic finite Heisenberg cocycle uses CA3--CA4, not CA5\'s separate even-rank positive-normalization conclusion.',
 'Finite-dimensional Fourier inversion, Banach-valued absolutely integrable Haar calculus, the Hermitian spectral theorem, elementary lattice/ideal theory and Stone--Weierstrass on a compact abelian quotient are explicitly used.',
 'No arbitrary complex field embedding is interchanged with an infinite series, limit, derivative or integral.',
 'CW24 uses HF11\'s explicit auxiliary character and the supplied prescribed-character ResEta clauses; it does not assume or prove globalNormIndexTwo merely by transporting that auxiliary character.',
 'CW25 retains the supplied level-character datum, its Is witness, the actual grid and grid Weil realization. The common bottom field requires finite T, as supplied by the literal admissible setting.',
 'These are human mathematical proofs, not kernel replay. No Lean build, source mutation, PDF or complete RH/GRH conclusion is claimed.'
]
main_raw=(HERE/'main.tex').read_bytes();paragraphs={};proof_locs={}
for n in range(1,26):
 start=main_raw.index(f'\\paragraph{{CW{n}:'.encode())
 stop=main_raw.index(f'\\paragraph{{CW{n+1}:'.encode(),start+1) if n<25 else len(main_raw)
 key=f'CW{n}';paragraphs[key]=digest(main_raw[start:stop])
 proof_locs[key]=dict(file='main.tex',anchors=[key],sha256=paragraphs[key],
  line_start=main_raw[:start].count(b'\n')+1,line_end=main_raw[:stop].count(b'\n'),bytes=stop-start)

def claim(i,title,statement,deps,srcs,relation,assumptions=(),status='derived_simplification'):
 return dict(id=i,title=title,status=status,statement=statement,introduced_in='0.21',depends_on=deps,
  assumptions=common+list(assumptions),proof_location=proof_locs[i],proof_paragraph_sha256=paragraphs[i],
  expanded_notes=dict(file='report.txt',section=i),source_relation=relation,
  mathematical_status='proved_under_exact_declared_hypotheses',sources=srcs)

claims=[
 claim('CW1','Actual trace-dual finite lattice and integral half',
  'The original AA-times-Hom lattice is self-dual; an integral w with w+bar(w)=1 gives the exact corrected finite Heisenberg law, and actual moves are commensurable.',['WA1'],
  ss(FORM,'hO symplO symplOH heisO actO IsThetaFunO')+
  ss(RHO,'rhoF latF thetaSub gamF phase isHeis_opF exists_w')+
  ss(AL+'SelfDualLatticePairingDual.lean','latO_selfDual_approx_sign')+
  ss(V+'CompletedHomLatticeFinitelyGenerated.lean','latO_finitely_generated')+
  ss(V+'CompletedHomLatticeMultipleMemOpenLevel.lean','level_of_generators'),
  'Uses exact local trace/codifferent duality, an integral trace-one element and finite-generator denominator clearing; retains dyadic and projective-lattice cases.'),
 claim('CW2','Signed lattice intertwiners at every residue characteristic',
  'The host admits one GoodNorm lambda with the required negative inert Gauss values, and normalized finite lattice sums compose exactly.',['CA3','CA4','CW1'],
  ss(FND+'ExistsGoodIndexNormalizationNegativeInert.lean','ofPrimeValues exists_lam exists_goodNorm')+
  ss(FIN,'IsLatRep exists_isLatRep')+
  ss(V+'InvariantFormNormalizedHeisenbergIntertwiner.lean','lam_idx_sq_eq_idx_of_fixed_ne_zero'),
  'Reuses the generic signed CA4 cocycle; no even-rank condition or globally positive replacement is introduced.'),
 claim('CW3','Finite character projectors span the actual theta space',
  'Each theta vector is a finite complex linear combination of finite Heisenberg translates of A-fixed theta vectors.',['CW1'],
  ss(V+'SpanHeisenbergTranslatesOfLatticeVacuaEqTop.lean','sum_over_quotient_fixed_of_fixed span_translates_vacua')+
  ss(FIN,'exists_isLatRep'),
  'The proof constructs the two dual finite quotient groups and averages their characters. The result is algebraic span, with no dimension-one assertion.'),
 claim('CW4','A genuine finite representation from relations',
  'Omega_f(p)(W_x e)=W_(r(p)x)J_(A,r(p)A)e descends to the actual theta space and satisfies the exact group law and covariance.',['CW1','CW2','CW3'],
  ss(V+'ExistsWeilRepresentationOfLatticeVacua.lean','eq_zero_of_sum_eigenvectors_eq_zero_of_injective isHeis_sum_filter_quotient_eq_zero_of_sum_eq_zero isHeis_sum_map_eq_zero_of_sum_eq_zero exists_weil_rep_of_vacua')+
  ss(FIN,'IsLatRep exists_isLatRep fix_vac heis_fin'),
  'Splits every finite relation by its lattice eigencharacters, checks same-coset cocycles and proves multiplication from signed J composition.'),
 claim('CW5','Finite local constancy, commutants and exact Haar norm',
  'The constructed finite action commutes with every finite-Heisenberg commutant, is locally constant on each vector, and preserves every original Haar quotient norm.',['CW1','CW2','CW3','CW4'],
  ss(FIN,'real_triv comm eventually_fix cont unit')+
  ss(V+'EventuallyUnitaryPairKeepsCompletedLattice.lean','eventually_move eventually_actO')+
  ss(V+'ExistsHeisenbergInvariantMeanSquareForm.lean','exists_form exists_invariant_form')+
  ss(V+'InvariantFormNormalizedHeisenbergIntertwiner.lean','invariantForm_translate_vacuum_eq_zero invariantForms_eq_of_eq_on_vacua invForm_intertwiner'),
  'Uses actual finite generators and orthogonality, not an assumed joint operator topology or a measure rescaling.'),
 claim('CW6','Positive split normalization and nonsplit vacuum fixing',
  'For the actual split half-functional, the action scalar is a positive count divided by the positive split index normalization; the actual nonsplit local vacuum is fixed.',['CW1','CW2','CW3','CW4','CW5'],
  ss(FIN,'split inert')+
  ss(V+'InvariantFormNormalizedHeisenbergIntertwinerEq.lean','invariantForm_translate_eq_zero invariantForm_normOp_eq')+
  ss(V+'InertPrimeNotDvdRelIndexSplitPlace.lean','not_dvd_relIndex')+
  ss(V+'IntertwinerFixesOfLocalVacuum.lean','intertwiner_fixes_of_local_vacuum')+
  ss(PARTS,'NonSplitAt SuppPl UnramAt FixesVacAt'),
  'Counts exactly the surviving projected cosets and treats the host nonsplit half-phase with its actual local lattice.'),
 claim('CW7','Constructing the complete finite Weil constituent',
  'The exact crossed cut-determinant character times Omega_f constructs IsFinWeil on the original functions and preserves the required split and nonsplit clauses.',['CW1','CW2','CW3','CW4','CW5','CW6'],
  ss(V+'ExistsSplitCharacter.lean','cut exists_glue exists_select exists_split_character')+
  ss(V+'ExistsUnitaryGroupCharacterOfHeckeChar.lean','char_norm char_eq_of_mul_conj cutDet continuous_cutDet cutDet_same cutDet_conj exists_character')+
  ss(FIN,'IsLatRep.Heisenberg₂ exists_isFinWeil')+
  ss(PARTS,'IsUnitaryOnTheta IsFinWeil')+ss(DEFS,'IsHeckeChar ResEta'),
  'The characters are deliberately crossed. Extension by an algebraic complement is only a full-function realization; analytic properties remain restricted to theta functions.'),
 claim('CW8','Gaussian projectors and the exact Banach smooth domain',
  'The Gaussian projector satisfies P^2=P and P rho(v) P=G(v)P; actual smooth vectors are exactly those with all polynomial coherent-coefficient moments integrable. ',[],
  ss(FOUR,'gau IsHeis Sm IsOsc proj Good proj_translate Good.inversion Good.sm')+
  ss(V+'PowMulNormGauLe.lean','Sm.good')+
  ss(V+'IntegralGauTwistedConv.lean','proj_heis_proj'),
  'Explicit translated derivative bounds give Schwartz decay; Banach Fourier inversion supplies the coherent resolution and its converse.'),
 claim('CW9','Exact Gaussian two- and three-projector determinants',
  'For the unitary signature group, c(g)=det(P_+g+P_-) is nonzero and gives the exact two/triple Gaussian scalars, including their phases.',['CW8'],
  ss(V+'IntegralComplexGaussianPosDefHermitianPart.lean','exists_congr_diagonal gaussian_diagonal integral_gaussian')+
  ss(V+'HalfAddSelf.lean','det_diag det_block detPlus_identities')+
  ss(V+'GaussianPairingUnitaryGroupTwoThree.lean','lam_mu_eq')+
  ss(FOUR,'dP lam mu'),
  'Writes the positive-Hermitian-part exponent matrices and the projection-block determinant factorization. Complex Gaussian evaluation chooses no determinant square root.'),
 claim('CW10','The actual smooth oscillator representation',
  'The absolutely convergent coherent integral with T_g=c(g)P_gP defines a genuine oscillator action on smooth vectors, preserving every invariant Hilbert norm and bounded commutant.',['CW8','CW9'],
  ss(REAL,'intw intw_integrable proj_heis_intw good_intw intw_heis intw_proj proj_twist_proj proj_twist_twist_proj norm_intw continuous_twist_intw vacOp osc sm_osc scalar_mul osc_mul norm_osc exists_isOsc'),
  'Uses the exact coherent-coefficient identity and explicit moment inequality for smooth closure; determinant identities remove the projective multiplier.'),
 claim('CW11','Cartan vacuum determinant with the correct orientation',
  'The annihilation equations imply Gaussian projection fixing, and the actual real vacuum scalar is det((1+s)g/2+(1-s)/2), transported through the same congruence for arbitrary Hermitian H.',['CW8','CW9','CW10'],
  ss(V+'ProjEqSelfOfAnnihilated.lean','circleAverage_orbit_line_eq_gaussian_smul proj_eq_self_of_annihilated')+
  ss(V+'ExistsOscillatorActionUnitaryGroupHermitian.lean','detPlus_conj₂ exists_osc_involution exists_osc')+
  ss(PARTS,'detPlus VacCharPlus'),
  'Holomorphic normalized line orbits and circle means prove the projector statement; unitary Cartan conjugacy gives the determinant itself, not its reciprocal.'),
 claim('CW12','Literal theta smoothness is Banach smoothness',
  'The original pointwise theta derivatives yield uniform Banach Fréchet derivatives, and conversely Banach smoothness with an actual finite level gives the literal theta space. ',['CW1'],
  ss(COMP,'QB ev norm_ev_le norm_QB_le BB rhoB norm_rhoB continuous_rhoB')+
  ss(V+'HeisenbergSmoothOfWeakDerivativeClosedSet.lean','hasFDerivAt_of_norming sm_of_weak_deriv_closed')+
  ss(INF,'theta_of_sm exists_deriv ev_fderiv sm_of_theta')+
  ss(FORM,'IsThetaFunO'),
  'A norming evaluation family and the scalar mean-value bound justify uniform Fréchet differentiability; pointwise smoothness alone is not invoked as sufficient.'),
 claim('CW13','Constructing the complete real Weil constituent',
  'The original real Hom matrices and host-scaled Hermitian form yield IsInfWeil and the exact positive Cartan vacuum determinant on the same theta functions.',['CW8','CW9','CW10','CW11','CW12'],
  ss(COMP,'unvecL vecL blk blk_mul detPlus_blockDiagonal HM im_HM isHeis_rhoB HM_herm HM_det mM mM_unitary continuous_mM HM_cartan toL2 lintegral_norm_sq_eq_toL2')+
  ss(INF,'rhoB_comm exists_hom lintegral_eq_of_norms detPlus_pairMatrix exists_isInfWeil')+
  ss(PARTS,'IsInfWeil VacCharPlus'),
  'Vectorizes h tensor transpose(g inverse), preserves actual finite levels by commutants, and applies the oscillator norm theorem to every original Haar L2 map.'),
 claim('CW14','Same-action commutation and the adelic product',
  'The actual finite and real constituents commute on theta functions, and their product has full covariance, original Haar norm and pointwise continuity.',['CW5','CW7','CW13'],
  ss(V+'ContinuousProduct.lean','fin_inf_comm eventually_smul continuous_product')+
  ss(CANON,'exists_weilDatum_etaTilde')+
  ss(INF,'exists_extend'),
  'Uses the commutant property of the constructed finite action directly. The single product is extended once; no commutation outside the theta space is asserted.'),
 claim('CW15','Norm-sensitive scalar comparison with rational pullback',
  'A theta-preserving Heisenberg commutant preserving the Haar norm is a common unit-modulus scalar; rational pullback therefore differs from the constructed action by c_p with |c_p|=1.',['CW14'],
  ss(V+'SchurLemmaThetaFunctionsOrientedPair.lean','heisO_rat prod_eq schur')+
  ss(FD,'subst IsScalar exists_isScalar IsScalar.mul')+
  ss(I+'RationalSymplecticPointsSelfAnnihilator.lean','inf_rat fin_eq_zero adele_rat tensor_rat ratL_annihilator'),
  'Polarization and separating compact-quotient characters prove the scalar. Its positivity/algebraicity is not inferred from unitarity.'),
 claim('CW16','Signed finite Hermitian Gauss sum by simple-module induction',
  'For a finite nondegenerate symmetric conjugate-adjoint bicharacter, the actual quadratic Gauss sum is lambda(|M|), and lambda(|M|)^2=|M|.',['CA3','CW1','CW2'],
  ss(V+'GaussSumNondegenerateFiniteHermitianModule.lean','gauss_fin gauss_hermitian')+
  ss(FD,'gauss_isometry'),
  'Inducts through isotropic simple modules or nondegenerate residue lines. The residue norm sum fixes the negative inert sign, including characteristic two.'),
 claim('CW17','Paired integral indices and actual rational finite Gauss data',
  'For u(x)=h^{-1}xg and det(u-1) nonzero, the two actual quotient indices share c0,N,m and have the exact determinant norm formulas; the finite sum equals lambda(n).',['CW1','CW2','CW16'],
  ss(V+'RationalLatticeSelfDualFgFullIndex.lean','fg_of_denom exists_denom_latQ exists_rat_add_nsmul latQ_selfDual_fg_full_index')+
  ss(FD,'gauss_isometry finite_data')+
  ss(V+'ExistsIsHalfIdem.lean','latQ gamQ sandw det_sandw det_sandw_sub_one'),
  'The radical calculation on (u-1)^(-1)L/(L cap u^(-1)L) and the shared denominator preserve integral rather than merely rational-span information.'),
 claim('CW18','Exact eta phase and signed norm normalization',
  'For the supplied IsEtaTilde, its split cut times lambda(absNorm x) times the actual CM-type product of x is positive, with the precise value sqrt(k) product|tau(x)|.',['CW2','HF9'],
  ss(ETA,'eta_inf eta_norm decomp product lam_int eta_split_mul_lam_pos')+
  ss(DEFS,'IsEta ResEta HasInfExp UnramEverywhere')+ss(PARTS,'IsEtaTilde'),
  'Replaces the source fixed-prime construction by testing AllSome ResEta against HF9\'s explicit quadratic character, then ideal factorization and denominator cancellation.'),
 claim('CW19','Actual Gaussian theta tests and the zero Fourier coefficient',
  'The explicit same-chart Gaussian Poincare family consists of lattice and Cartan vacua, is not identically zero, and proves lambda(n) integral(G_u)=positive_covolume*kappa for the actual scalar relation.',['CW1','CW17','CW20'],
  ss(V+'ExistsIsHalfIdem.lean','chiLat serO gaussR')+
  ss(GAUSS,'series_inv_scalar series_regular quad_identity chiLat_add_lat series_theta_vacuum')+
  ss(UNF,'serO_eq gaussQ left_side coefQ right_side summable_coefQ coefQ_zero gauss_mul_integral')+
  ss(V+'UnfoldPoincareSeriesLatticeFourier.lean','unfold_poincare_fourier'),
  'Every derivative and unfolding is Gaussian dominated. Opposite-order phase is the right magnetic translate; the unique zero coset contributes exactly one.'),
 claim('CW20','The real integral with its fixed Cartan sign',
  'For u commuting with the Cartans and det(u-1) nonzero, the real Gaussian has positive Hermitian exponent part and its determinant gives I*P=r2*det(-s)*Q*delta with r2 positive.',['CW9','CW17'],
  ss(RINT,'expM expM_herm expM_mul dot_expM gauss_det integral_gaussR')+
  ss(V+'IntegralComplexGaussianPosDefHermitianPart.lean','integral_gaussian'),
  'Keeps the actual host form, inverse pair orientation, original coordinate Jacobian and exact vacuum determinant; no unknown phase is absorbed into r2.'),
 claim('CW21','Cancellation of the rational automorphy scalar phase',
  'For a Cartan-commuting no-fixed-vector rational pair, c_p*epsilon0=r*s0 with r=r1*r3/(r2*r4*n)>0 and s0 the same order-two eta cut.',['CW7','CW13','CW15','CW17','CW18','CW19','CW20'],
  ss(RAT,'phase_identity exists_idempotentUnitEmbeddings_character_relation exists_phi oi_vac final_algebra scalar_const')+
  ss(FD,'det_unitary_sub_one kronecker_unitary'),
  'Eliminates exact finite indices, real determinant and common denominator. Every cancellation is nonzero and the crossed cut identity has the explicit original orientation.'),
 claim('CW22','Full rational theta-distribution automorphy',
  'The actual product action equals rational pullback on every theta function for every rational unitary pair, hence fixes evaluation at zero in both factors.',['CW15','CW19','CW21','WA10'],
  ss(FD,'infinite_norm_one rat_induction IsScalar.mul')+
  ss(RAT,'isScalar_one_of_comm exists_cartan_refl of_oi_eq_subst of_oi_apply_zero automorphy_target')+
  ss(V+'ThetaDistributionAutomorphySourceGroup.lean','automorphy_source')+
  ss(AL+'UnitaryMatrixEqProdQuasiReflections.lean','isUnE_eq_prod_refl'),
  'A norm-one scalar avoids the finitely many forbidden determinant roots; comparing two identical phase constants makes c positive, then norm one gives c=1. Quasi-reflection generation removes the Cartan restriction.'),
 claim('CW23','All eleven canonical Weil fields and both extra clauses',
  'The literal exists_weilDatum_etaTilde is constructed on the exact supplied objects, including FixesVacAt and VacCharPlus.',['CW7','CW13','CW14','CW22'],
  ss(CANON,'isHeckeChar_pow resEta_pow mem_GfC_of_suppAt exists_weilDatum_etaTilde')+
  ss(FORM,'IsWeilDatumO')+ss(PARTS,'FixesVacAt VacCharPlus IsEtaTilde'),
  'Joins the already constructed action once, preserves every Haar measure and rational domain, and verifies split/real/nonsplit restrictions with the original lattices and characters.'),
 claim('CW24','Actual prescribed-character full existence without new norm-index uniqueness',
  'For arbitrary given HSp and prescribed Hecke characters with their literal rank restrictions, a full oriented Weil datum exists on the same functions; no independent canonical-Weil or IsEta uniqueness premise remains.',['CW1','CW7','CW13','CW14','CW16','CW17','CW18','CW19','CW20','CW21','CW22','HF9','HF10','HF11','WA18'],
  ss(AL+'IsSelfDualCLatFrame.lean','latFrame mem_latFrame isSelfDualC_latFrame')+
  ss(I+'ExistsCmAdeleUnitCharacterReadingHeckeChar.lean','exists_toAdele exists_hom exists_chrEq')+
  ss(I+'ExistsUnramifiedHeckeCharHalfExponentRestrictQua.lean','val_finite val_infinite isEta_res exists_etaTilde')+
  ss(TWIST,'exists_weilDatum_twist')+
  ss(GEN,'isHeckeChar_div_pow resEta_div_pow exists_isWeilDatumO')+
  ss(DEFS,'IsEta ResEta'),
  'Reuses the operator formulas under HF11\'s explicit eta0 properties; final prescribed characters supply the universal ResEta fields. This bypasses, and does not claim to prove, globalNormIndexTwo.'),
 claim('CW25','Actual bottom families and the common bottom period field',
  'The exact two new bottom Weil families, standard bottom triangles and NFBot are supplied on every given admissible level/grid realization, with finite twist set for the field conclusion.',['CW24','WA16','WA17','TT12'],
  ss(BOT,'exists_stdRig bottom_chars isSelfDualC_neg\' exists_bottomTri IsBottomTri.integrable')+
  ss(NFBOT,'field_of_gens sumsIn_bottom sumsIn_mono GlobalTheory.RowEx.nfBot_holds')+
  ss(T+'RangeAlgebraMapMono.lean','nfAll_of'),
  'Removes WA17\'s independent new full-Weil existence premise. The actual level eta, frames, vacuum, conductors, measures and grid realization remain fixed; toric ratio fields and Choice embedding joins are separate.',
  ['The given level datum has its Is witness and the grid has its actual Weil realization. The finite T condition is explicit for the common field.'])
]

target_specs=[
 (1,T+'ExistsUnitModulusScalarLocal.lean','exists_kappa',
  'Prove the stronger quantitative arithmetic of the prescribed moving-vacuum scalar and exact all-embedding/local-unit dictionary bounds.',
  'CW constructs the full actual representation and WA11--WA16 already prove qualitative finite-Weil arithmetic, normalized jets and bottom periods. The all-embedding unit modulus, prescribed local-unit, denominator and dictionary size bounds remain separate; unitarity in the distinguished complex realization does not prove them.',
  [(T+'ExistsLatticesEntireIntertwining.lean','movedVacuum_dict'),(T+'DictionarySizeBound.lean','dictAt_big')],['CW23','CW24','WA11','WA14','WA16']),
 (1,V+'ToricRatioConjugatesOfTransport.lean','toricRatioConjugates_of_transport',
  'Supply the actual twisted CM transport and critical toric-ratio conjugacy, then the ratio field on the same reference twist.',
  'The canonical and prescribed full Weil constructors and actual NFBot are now supplied by CW23--CW25. Critical toric L-value arithmetic is not a finite Heisenberg or Gaussian normalization assertion; actual TwistedTransport/CM data and the reference-twist identities remain.',
  [(T+'NormalFormToricRatio.lean','ratio_algebraic'),(T+'NormalFormToricRatio.lean','nfRatio')],['CW25','WA19','TT18','TT19']),
 (1,T+'ExKeyOf.lean','exKey_of',
  'Complete the literal same-object compatible field/choice join, including actual range inclusion in the prescribed embLL and remaining matching clauses.',
  'The jet field, actual two-period bottom fields and new bottom Weil existence are supplied (WA14, WA16, CW24--CW25). The remaining critical ratio field and original-embedding/choice compatibility are not obtained by choosing an unrelated complex subfield or a new grid realization.',
  [(T+'ExFieldOfKeyFinExKey.lean','exField_of_keyFin_exKey'),(T+'TestChoicesExistLargeCoeffFieldAdelicData.lean','dat_choice_exists')],['CW24','CW25','WA14','WA16','WA19','TT19'])
]
targets=[]
for priority,path,name,objective,remaining,support,ids in target_specs:
 s=source(path,name,'retained_actual_primitive_supplier')
 targets.append(dict(priority=priority,path=path,declaration=s['declaration'],source=s,
  source_ranges=[s]+[source(p,n,'substantive_remaining_supplier') for p,n in support],
  objective=objective,remaining_human_scope=remaining,already_reconstructed=ids,
  supplied_conclusion_not_assumed_proved=True))

closed_specs=[
 (V+'SpanHeisenbergTranslatesOfLatticeVacuaEqTop.lean','span_translates_vacua',['CW3'],'Actual finite algebraic spanning, no fixed-line assumption.'),
 (V+'ExistsWeilRepresentationOfLatticeVacua.lean','exists_weil_rep_of_vacua',['CW4'],'Actual quotient-by-relations construction and genuine finite group law.'),
 (FIN,'exists_isFinWeil',['CW1','CW2','CW3','CW4','CW5','CW6','CW7'],'Complete finite constituent with original lattices, positive split scalar and nonsplit fixing.'),
 (REAL,'exists_isOsc',['CW8','CW9','CW10'],'Actual Banach-smooth oscillator construction with exact Gaussian determinant phase.'),
 (V+'ExistsOscillatorActionUnitaryGroupHermitian.lean','exists_osc',['CW10','CW11'],'Arbitrary nonsingular Hermitian form and actual Cartan-vacuum determinant.'),
 (INF,'exists_isInfWeil',['CW8','CW9','CW10','CW11','CW12','CW13'],'Complete real constituent on original theta functions and all Haar norm realizations.'),
 (V+'ContinuousProduct.lean','fin_inf_comm',['CW14'],'Exact commutation for the specifically constructed finite/real actions; the stronger generic comparison route is bypassed.'),
 (V+'ContinuousProduct.lean','continuous_product',['CW14'],'Exact product pointwise continuity for the constructed actions, with a fixed-vector local constancy argument.'),
 (V+'SchurLemmaThetaFunctionsOrientedPair.lean','schur',['CW15'],'Norm-sensitive scalar lemma on the actual theta functions.'),
 (V+'GaussSumNondegenerateFiniteHermitianModule.lean','gauss_hermitian',['CW16'],'Actual signed finite Hermitian Gauss sum, including characteristic two.'),
 (FD,'finite_data',['CW17'],'Both integral indices and finite sum, with one common denominator.'),
 (ETA,'eta_split_mul_lam_pos',['CW18'],'Exact character/norm positivity using HF9 as a shorter source-hypothesis argument.'),
 (GAUSS,'series_theta_vacuum',['CW19'],'Actual same-chart convergent Gaussian theta family with finite and Cartan vacuum laws.'),
 (UNF,'gauss_mul_integral',['CW19','CW20'],'Finite zero coefficient and absolutely convergent unfolding fix the scalar relation.'),
 (RINT,'integral_gaussR',['CW20'],'Exact real integral determinant and fixed Cartan phase.'),
 (RAT,'scalar_const',['CW17','CW18','CW19','CW20','CW21'],'Exact phase cancellation under the source Cartan/no-fixed-vector hypotheses.'),
 (RAT,'of_oi_eq_subst',['CW22'],'Full rational-pair pullback identity for the actions constructed here.'),
 (RAT,'automorphy_target',['CW22'],'Actual target automorphy from the stronger full rational-pair identity.'),
 (V+'ThetaDistributionAutomorphySourceGroup.lean','automorphy_source',['CW22'],'Actual source automorphy from the same full identity; no transposed-space reconstruction needed.'),
 (CANON,'exists_weilDatum_etaTilde',['CW23'],'Literal canonical full Weil existence under its original IsEtaTilde and self-dual lattice hypotheses, including both extra clauses.'),
 (GEN,'exists_isWeilDatumO',['CW24'],'Actual prescribed-character full existence; the independent eta existence premise is bypassed by HF11 explicit data plus the supplied final ResEta fields.'),
 (BOT,'exists_bottomTri',['CW24','CW25'],'Actual new bottom representations and triangle on the supplied level/grid realization.'),
 (BOT,'IsBottomTri.integrable',['CW25','TT12'],'Actual definite bottom integrability on the same measures and theta functions.'),
 (NFBOT,'nfBot_holds',['CW25','WA16'],'Actual finite common bottom field on every supplied admissible realization; finite T and original periods are retained.')
]
closed=[]
for path,name,ids,scope in closed_specs:
 s=source(path,name,'literal_completed_source_target')
 closed.append(dict(path=path,declaration=s['declaration'],closed_by=ids,source=s,
  scope=scope+' All hypotheses of the named human claims remain explicit.'))

optional=[
 dict(source=source(I+'MemNormGroupIffEverywhereNorm.lean','globalNormIndexTwo','optional_bypassed_source_route'),
  support=[source(I+'MemNormGroupIffEverywhereNorm.lean','existsUnique_isEta','optional_universal_character_uniqueness'),
   source(I+'ExistsUnramifiedHeckeCharHalfExponentRestrictQua.lean','exists_etaTilde','optional_full_universal_eta_record')],
  scope='Reconstruct the general global norm-index-two uniqueness theorem and the universal IsEtaTilde producer if desired. CW24 does not require them: its actual auxiliary eta has explicit restriction, and the prescribed final characters supply universal ResEta.'),
 dict(source=source(V+'ThetaDistributionAutomorphySourceGroup.lean','swap_inf','optional_transposed_source_route'),
  scope='The separate transposed/dual-Hom representation proof is optional. CW22 already proves the actual full rational-pair pullback identity for the constructed action, hence both distribution automorphy clauses.')
]
conditional=[
 dict(source=source(T+'RangeAlgebraMapMono.lean','nfAll_of','remaining_compatible_full_field_join'),
  reconstructed_by=['CW25','WA14','WA16','WA19','TT11','TT19'],
  retained=['Critical toric ratio arithmetic','Literal original-embedding/Choice compatibility'],
  scope='New bottom full Weil existence and NFBot are no longer retained inputs. Independent complex fields do not by themselves satisfy the original Choice.FieldOK.')
]

record_audits=[]
for path,name,expected,inherited,support in [
 (FORM,'IsWeilDatumO',['std','hecS','hecT','resS','resT','om_pres','om_heis','om_aut','om_cont','om_unit','om_split'],[],
  'CW23 proves every field for the supplied canonical eta; CW24 proves every field for the specified splitting characters, without claiming universal eta uniqueness.'),
 (PARTS,'IsUnitaryOnTheta',['pres','cont','unit'],[],
  'CW5/CW7 for the finite constituent and CW12/CW13 for the real constituent.'),
 (PARTS,'IsFinWeil',['triv','Heisenberg₂','split','inert'],['pres','cont','unit'],
  'CW1--CW7 construct all four own fields and the three inherited IsUnitaryOnTheta fields.'),
 (PARTS,'IsInfWeil',['triv','Heisenberg₂','vac'],['pres','cont','unit'],
  'CW8--CW13 construct all three own fields and the three inherited IsUnitaryOnTheta fields.')
]:
 s=source(path,name,'literal_record_field_inventory')
 rows=read_source(path)[1][s['line_start']-1:s['line_end']]
 names=[m.group(1) for line in rows[1:] if (m:=re.match(r'^  ([^\s:]+)\s*:',line))]
 assert names==expected,(name,names,expected)
 record_audits.append(dict(record=s['declaration'],source=s,field_count=len(names),inherited_fields=inherited,
  total_including_inherited=len(names)+len(inherited),all_fields_constructed=True,
  fields=[dict(name=f,supplied_by=support) for f in names]))

# Verify new IDs are unused in the immutable predecessor and every old dependency exists.
prior=HERE.parent/'history/version_0_20/provenance.json'
if prior.exists():
 prior_obj=json.loads(prior.read_text()); prior_claims=prior_obj['claims']
 old_ids=set(prior_claims) if isinstance(prior_claims,dict) else {c['id'] for c in prior_claims}
else:
 raise AssertionError('Expected immutable v0.20 predecessor ledger')
new_ids={c['id'] for c in claims}
assert not old_ids & new_ids, ('prefix collision',old_ids & new_ids)
for c in claims:
 assert set(c['depends_on']) <= old_ids|new_ids,(c['id'],set(c['depends_on'])-(old_ids|new_ids))
visiting=set();done=set();by_id={c['id']:c for c in claims}
def visit(k):
 if k in done or k not in by_id:return
 assert k not in visiting,('cycle',k)
 visiting.add(k)
 for d in by_id[k]['depends_on']:visit(d)
 visiting.remove(k);done.add(k)
for k in new_ids:visit(k)

out=dict(schema_version='1.3',artifact_version='0.21',date='2026-11-22',component='canonical_weil',
 owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes without Unicode or newline normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False,new_prefix_unused_in_predecessor=True,
  new_dependency_graph_acyclic=True),
 status_definitions=dict(derived_simplification='Human proof under exact declared hypotheses, using explicitly proved constructions and identified shorter arguments.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,record_audits=record_audits,
 prior_components_reused=['CA','WA','HF','TT'],same_iteration_companions=[],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Actual finite Heisenberg/lattice representation with its signed normalized intertwiners',
  'Actual real Banach-smooth oscillator with the full determinant phase and Haar norm',
  'Exact finite-real commutation and rational theta-distribution automorphy',
  'All eleven canonical IsWeilDatumO fields plus FixesVacAt and VacCharPlus',
  'Actual same-space prescribed-character full Weil existence, bypassing extra universal eta uniqueness',
  'Actual standard bottom triangles and NFBot on the supplied admissible level/grid realization'],
 scope_precision=[
  'All finite Gauss signs and half-pairing/codifferent factors are retained, including dyadic places.',
  'No even-rank condition is imposed on the generic canonical construction.',
  'Analytic integrals use actual Banach smoothness, coherent moment bounds and positive-Hermitian Gaussian domination.',
  'The norm-one rational scalar is proved positive by exact phase cancellation before it is set equal to one.',
  'The CW24 auxiliary eta is not asserted to satisfy the universal AllSome restriction; final prescribed characters supply that clause.',
  'General prescribed-character twisting does not assert the canonical extra vacuum clauses.',
  'The supplied level data, grid representation, fields and embeddings are not independently replaced.',
  'Quantitative dictionary estimates, critical toric ratio fields and the remaining exact Choice.FieldOK embedding join are separate.',
  'All predecessor component and pinned checkout bytes are preserved.'])

review_specs=[
 ('canonical_weil_CW1_13_review.json','/root',list(range(1,14)),
  'Independent finite and real construction review, with exact analytic domains and determinant phases.'),
 ('canonical_weil_CW14_end_review.json','/root',list(range(14,26)),
  'Independent product, rational scalar, canonical endpoint and same-data bottom existence review.'),
 ('canonical_weil_rational_independent_review.json','/root/global_frame',list(range(16,26)),
  'Independent finite Gauss, real integral, rational phase, full constructor and eta/AllSome boundary review.')
]
for filename,reviewer,indices,scope in review_specs:
 p=HERE.parent/'reviews_v0_21'/filename
 if not p.exists():continue
 raw=p.read_bytes();r=json.loads(raw);chosen={f'CW{i}':paragraphs[f'CW{i}'] for i in indices}
 reviewed=r.get('reviewed_claims',{})
 for key,sha in chosen.items():
  actual=reviewed.get(key)
  if isinstance(actual,dict):actual=actual.get('proof_paragraph_sha256',actual.get('paragraph_sha256',actual.get('sha256')))
  assert actual==sha,('review paragraph changed',filename,key,sha,actual)
 verdict=r.get('verdict',r.get('result',r.get('status','')))
 assert str(verdict).upper().startswith('PASS'),('review not PASS',filename,verdict)
 out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
  review_record='../reviews_v0_21/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
  paragraph_range='Named CW paragraph through immediately before next paragraph; EOF for CW25.',lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
 loc += [f"{c['id']} | {c['title']} | {c['status']}",c['statement'],f"  proof_paragraph_sha256: {paragraphs[c['id']]}"]
 for s in c['sources']:
  loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
   f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
 loc += ['']
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.21',commit=PIN,targets=targets,
 closed_source_targets=closed,conditionally_reconstructed_targets=conditional,retained_inputs=common,
 optional_not_required=optional,
 remaining_boundary='The canonical finite/real full Weil construction and actual bottom families/NFBot are supplied. Quantitative dictionary arithmetic, critical toric ratios and literal original-embedding/Choice compatibility retain their separate scopes. The universal global norm-index-two route is optional for this proof.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 distinct_claim_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 claim_source_files=len({s['path'] for c in claims for s in c['sources']}),source_files=len(files),next_targets=len(targets),
 closed_endpoints=len(closed),independent_reviews=len(out['independent_reviews'])),indent=2))
