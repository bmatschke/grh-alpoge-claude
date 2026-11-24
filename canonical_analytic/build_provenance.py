#!/usr/bin/env python3
"""Reproduce the CA source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
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
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive|instance)\s+([^\s:({]+)')
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


GI = D + 'Proofs/GlobalInterpolation/'
DV = D + 'Proofs/DivisorProofs/'
FP = D + 'Proofs/FoundationProofs/'
KL = F + 'KernelLattices/'
SG = 'src/Formalism/SharpRestriction/GlobalSchurBounds/'
HOST = A + 'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean'
AMB = A + 'TrueColumnChoicesHeckeCharReferenceEqOne.lean'

COMMON = ('All arithmetic fields, the induced CM type, curve ideal, prescribed discriminant root, '
          'actual period pair/half-point/four-copy isometry/correction data and field embeddings are '
          'the literal supplied source data. The Hermitian form is linear in its first argument; '
          'rational points are delta times embedded E-matrices. Even rectangular ranks are required '
          'where stated. No replacement vacuum or arbitrary field enlargement is hidden.')
BOUND = ('This is a human mathematical reconstruction from pinned bytes, without Lean compilation, '
         'kernel replay, formalization of the alternative argument, source modification or PDF rendering. '
         'It does not assert RH/GRH, arbitrary Pins.iX, raw PreX existence or Later existence.')


def cl(i, title, statement, deps, assumptions, sources, relation, conditional=False):
    return dict(id=i, title=title, status='derived_simplification', statement=statement,
        depends_on=deps, assumptions=[COMMON, BOUND]+assumptions,
        proof_location=dict(file='main.tex', anchors=[i]),
        expanded_notes=dict(file='report.txt', section=i),
        mathematical_status=('proved_conditional_assembly_with_exact_source_quantifiers' if conditional
                            else 'proved_under_exact_declared_supplied_data_hypotheses'),
        source_relation=relation, sources=sources)


claims = [
cl('CA1','Exact rational Heisenberg phases',
   'The actual Weyl operators satisfy U_x U_y=exp(-pi i Im H(x,y)) U_(x+y) and W_x W_y=gamma(w x,y) W_(x+y), with integral w=(1+sqrt(-d))/2 and gamma=exp(-2pi i Im H). Rational embedded points give root-of-unity phases, with unit modulus under every algebraic embedding.',
   [], ['The actual area normalization and induced quadratic CM type are used; no arbitrary complex Gaussian factor is called algebraic.'],
   ss(GI+'WeylHeisenbergOperatorCalculusRational.lean','HV_conj alpha_opU_mul Wx_Wx imH_eq Wx_comm contDiff_Wx')+
   ss(FP+'AdmissibleAtOfIrreducibleTame.lean','wd_wd hf_pt pt_add wd_cocycle')+
   ss(FP+'ExistsIntegerMapEqHalfOneAddSqrt.lean','isIntegral_half_one_add exists_integer_map_eq_w0')+
   ss(DV+'RationalPoints.lean','rational_points')+
   ss(HOST,'Hf al U','literal_definition'),
   'Expands the exponents and trace/area reading, checking the sign and factor two in the actual IsHeis cocycle.'),
cl('CA2','Actual finite presentation and conjugate coefficient bound for thInd',
   'After chiF cancellation the actual thInd is a sum of at most c^[E:Q]ab rational Heisenberg translates of the same thMoved, with algebraic coefficients whose every conjugate has absolute value at most one. This proves literal Pres for every finite S, including rank-zero cases.',
   ['CA1'], ['Fields.Ok, Seam.Ok, actual curve data, self-dual L and L-prime, and c>0. No no-conjugate-pair condition is needed for this finite presentation.'],
   ss(DV+'CosetIndicatorThetaTorsionTranslates.lean','Sm sm_avg sm_of_pow sm_exp sm_vol sm_inv_mul opU_neg_opU xiInd_expand pres_of_finset HV_eq rel_embH AA_fg pres_thInd')+
   ss(DV+'RelIndexOfLeNsmul.lean','relIndex_nsmul relIndex_of_nsmul_le relIndex_of_le_nsmul nsmul_mem_twO nsmul_mem_of_twO half_reps')+
   ss(DV+'CosetRefinement.lean','Pres toHost','literal_definition')+
   ss(KL+'XiIndCClass.lean','hatS xiInd halfAO halfBO IsLiftS AC BC volC','literal_definition'),
   'Proves the actual normalization before algebraicity: chiF inverse times chiF is 0/1, and the two inverse square roots cancel volC. Does not assume algebraicity of chiF.'),
cl('CA3','Negative finite Hermitian norm Gauss sum',
   'For a nontrivial finite residue involution, the exact sum chi(w t sigma(t)) is -sqrt(|k|). Trace surjectivity, norm fibers and additive-character orthogonality give a proof valid also in residue characteristic two.',
   [], ['Finite field k with nontrivial involution; nontrivial sigma-invariant additive character and w+sigma(w)=1.'],
   ss(FP+'SumEqZeroAddUnits.lean','card_eq_sq sum_norm_units sum_eq_zero_add_units gauss_field gauss_quotient'),
   'Uses the q+1 norm fibers and a nonzero degree-q trace polynomial; no division by two or dyadic exclusion.'),
cl('CA4','Signed finite intertwiners compose with the exact inert sign',
   'The actual GoodNorm normalization exists for the abelian unramified CM host. Its normalized finite Heisenberg intertwiners compose exactly on self-dual commensurable modules; the adjacent equal-intersection case has the negative norm Gauss scalar and general composition follows by strictly decreasing finite index.',
   ['CA1','CA3','DR1'], ['Generic IsHeis, mutually commensurable self-dual O_E modules and fixed vectors; actual E/Q abelian and E/E+ unramified for the one global multiplicative normalization.'],
   ss(FP+'IsHeisTrivial.lean','IsHeis SelfDual Fixes idx sumOp normOp GoodNorm Adj comm','literal_definition_and_finite_algebra')+
   ss(FP+'ExistsGoodIndexNormalizationNegativeInert.lean','ofPrimeValues exists_lam exists_card_eq_pow exists_goodNorm')+
   ss(FP+'PerfectPairingQuotients.lean','exists_addChar_quotient exists_injective_addChar perfect_pairing_quotients')+
   ss(FP+'HeisenbergIntertwiningSumsCompEqIndex.lean','sumOp_sumOp_eq_idx_smul')+
   ss(FP+'HeisenbergIntertwiningSumCompOfIntermediateLatti.lean','sumOp_comp_of_between')+
   ss(FP+'HeisenbergSumCompOfAdjacentOfInfEq.lean','sumOp_comp_of_adj_of_inf_eq')+
   ss(FP+'NormalizedIntertwinerCompOfAdjacentLattices.lean','idx_congr_of_inf_eq normOp_comp_of_adj')+
   ss(FP+'ExistsAdjacentSelfDualLatticeToward.lean','exists_mem_maximal_annihilator exists_adj_selfDual_step')+
   ss(FP+'NormalizedHeisenbergIntertwinerComp.lean','normOp_comp'),
   'Gives the genuine finite-module proof; does not import a completed Weil representation or presume global lattice freeness.'),
cl('CA5','Even opposite rank identifies signed J with the actual positive Iop moves',
   'Local Hom-lattice quotient lengths are multiples of the unchanged opposite rank. Even ranks remove every inert sign on each one-factor edge, so the source two-step thMoved equals J(A0,La(L,L-prime)) thZero. Rational unitary naturality follows directly on finite sums.',
   ['CA1','CA4','VI2','VI5','VI10'], ['Both rectangular dimensions are even; period lattices and thZero are those of the actual given VacIn/Base.'],
   ss(FP+'KernelLatticesFormSelfDualTriples.lean','theta_cocycle_eq_exp_hermitian nice_of_klat index_ne_zero iop_self klat_triples','source_counterpart_of_direct_local_length_proof')+
   ss(HOST,'La Iop thZero thHalf thMoved','literal_definition')+
   ss(KL+'LateralTheory.lean','thHalf thMoved','literal_definition'),
   'Alternative direct DVR index-parity proof identifies the actual positive normalization only on the specified one-factor moves. Arbitrary positive-Iop composition is not claimed.'),
cl('CA6','Gaussian trace computes the rational-unitary theta scalar',
   'For a unitary u with 1-u inverse invertible, the actual theta pull scalar is r det(1-u inverse)^-1 times the finite Gauss sum over A/mA, with r>0. Normal kernel convergence, the diagonal x+y character cancellation and explicit complex Gaussian integration prove the formula.',
   ['CA1','VI4','VI5','VI10'], ['Full self-dual period lattice, commensurable unitary image, nonzero theta vector, det(1-u inverse) nonzero, and a positive integer denominator satisfying CA.18.'],
   ss(FP+'IsPosHermFormV.lean','Sesq IsPosHerm Heisenberg₂ kerTerm kerSum IsSemichar','literal_definition')+
   ss(FP+'HeisenbergReproducingKernelSumSpec.lean','exists_bound norm_kerTerm_le differentiable_kerTerm kerTerm_shift kerSum_spec')+
   ss(FP+'IntegralHeisKerSumDiag.lean','heis_kerSum_diag integral_heis_kerSum_diag')+
   ss(FP+'IntegralKerSumGraphEq.lean','integral_kerSum_graph_eq')+
   ss(FP+'PhDetMulIntegral.lean','term_eq value_eq term_shift ph_det_mul_integral')+
   ss(FP+'IntegralGaussianUnitaryPos.lean','integral_gaussian_unitary_pos')+
   ss(FP+'ThetaTransport.lean','mean_transport mean_pos theta_transport')+
   ss(FP+'PullEqGaussSmulIntertwiner.lean','const_eq pull_eq_gauss_smul_intertwiner'),
   'Includes the analytic interchange and both diagonal integrals; line uniqueness/unit modulus alone is explicitly insufficient.'),
cl('CA7','The even-factor Gauss sum is a nonzero real square',
   'An orthogonal half projection and swap factor the actual finite Gauss sum into equal halves. Integral norm -1 modulo 4m conjugates each half sum, making it real; hence the full sum is positive and fixes the scalar as |det(1-u inverse)|/det(1-u inverse).',
   ['CA6','DR1'], ['Standard rectangular period lattice; u acts on one matrix factor and the other rank is even; the same positive denominator m and lattice semicharacter are used.'],
   ss(FP+'UnitaryThetaConstantEqInverseDeterminantPhase.lean','gauss_nonneg hfL hfL_apply hfL_swap semi const_of_symm')+
   ss(FP+'FinsumQuotientNonnegOfSwapConj.lean','sum_nonneg_of_swap_conj_fintype finsum_quotient_nonneg_of_swap_conj')+
   ss(FP+'ExistsDvdMulInvolutionAddOne.lean','exists_dvd_mul_involution_add_one exists_norm_eq_neg_one'),
   'The local norm/CRT construction includes dyadic places; exact exponent differences are even integers, and unit modulus excludes a zero square.'),
cl('CA8','Exact determinant powers for every rational unitary matrix',
   'For pull by gamma-prime inverse on the target and gamma on the source, the actual standard-vector scalar is product det(gamma)^(-b/2) det(gamma-prime)^(a/2). Scalar norm-one factorization removes the eigenvalue-one exclusion, using exact J composition and naturality.',
   ['CA4','CA5','CA7'], ['Even rectangular ranks and actual standard thZero; zero ranks are handled by constants. No general adelic Weil representation is assumed.'],
   ss(FP+'ThetaPullbackFirstGroupRationalPointEqSmul.lean','det_mul_conj phase pull_eq_smul_iop')+
   ss(FP+'ThetaPullbackSecondGroupRationalPointEqDetSmul.lean','norm_div_prod pull_right_eq_det_smul')+
   ss(FP+'OddEqOfEven.lean','exists_factor IsPull.mul oddEq_of_even','source_counterpart_of_direct_J_factorization')+
   ss(FP+'MulVSubRight.lean','adj mulV Hf_mulV pull_eq mulV_pt','literal_action_and_coordinate_binding'),
   'Checks the inverse and both determinant signs, then extends from det(1-gamma) nonzero by an explicit infinite rational norm-one scalar family.'),
cl('CA9','All three actual normalized-family equivariance laws',
   'The principal IsChi law makes chiFac transform by exactly CA8 scalar. Actual thMoved=J(A0,A)thZero therefore gives rational-unitary covariance and both one-factor Iop transport laws, proving literal Base.EqP for the supplied Base.',
   ['CA5','CA8','VI10'], ['The actual IsChi and curve/discriminant hypotheses; the same chosen Base thZero and correction roots remain fixed.'],
   ss(I+'NormalisedFamilySatisfiesEquivarianceLaws.lean','chi_smulLat chiFac_ne_zero chiFac_right chiFac_left eqP','source_counterpart_of_alternative_direct_proof')+
   ss(I+'NormalisedFamilySatisfiesEquivarianceLawsStatement.lean','normalisedFamily_satisfies_equivarianceLaws','closed_source_endpoint')+
   ss(I+'DetIdLatGmap.lean','detId_image norm_one_span star_det_mul detId_lat_gmap chi_lat_gmap')+
   ss(SG+'TaylorLogMetric.lean','eq22','literal_three_clause_interface')+
   ss(KL+'LateralTheory.lean','EqP eNat chiFac','literal_definition'),
   'Replaces the auxiliary-family/Weil detour by a proof for the actual family. It does not claim the unused full Weil or exists_kappa constructor has been reconstructed.'),
cl('CA10','Lift independence and exact covariance of the actual coset indicator',
   'The actual finite Fourier indicator equals n^-1 W(-t) sum_y W(y)e for every compatible rational lift t. CRT, local half-lattice tables, integral cocycles and quotient orthogonality prove lift independence and the precise scalar. Rational conjugation then gives literal ThIndEq and ChiLaw.',
   ['CA1','CA9','LP1'], ['LaHyp, nonzero actual period ideal, positive M and c, and exact InRange data; S has no conjugate pair and AAUnit on S.'],
   ss(GI+'ThetaMovedCosetIndicatorVacuumShape.lean','hatS_ind mem_twO loc_le_sup exists_smul_le expS_cases volC_pos Wx_mul Wx_sum coc_int_twO expS_conj two_lifts thInd_shape')+
   ss(GI+'ExistsLiftHalfLatticeRational.lean','exists_lift_halfAO')+
   ss(I+'GmapToAddSubgroup.lean','apply_mem_locP twO_gmap conjH perO_gmap pullV_eq pullV_emb HV_pullV Wx_pull thInd_index thIndEq_of_vacEq')+
   ss(I+'DetIdLatGmap.lean','chiLaw_ambOf')+
   ss(I+'SmulLatMatOf.lean','smulLat_matOf matOf_unitary vacEq_ambOf')+
   ss(KL+'ThDistC.lean','InRange Amb.AAUnit Amb.LaHyp Amb.ThIndEq Amb.ChiLaw','literal_interface'),
   'Carries every module, lift, quotient index and representative to its image. The actual chosen lift and source determinant normalization are retained.'),
cl('CA11','The actual selected step has a finite algebraic jet field',
   'For ColIn.Ok, every actual selected S_b step and M>0 has FinAlg(jetSet) in every fixed degree. The host-level AmbIn supplies all analytic data directly, avoiding an unused Stages existence detour. LaHyp, JetAlg, covariance, finite semilocal classes and Taylor-chain algebra establish the result.',
   ['CA2','CA9','CA10','VI2','VI10','VI11','TL1','TL19','LP1'], ['Literal Base, PreX, ColIn.Ok and its actual AmbIn. The source HasLetters antecedent is retained but unused by this shorter analytic proof. No LocStage/NStage witness is inserted.'],
   ss(GI+'AbsNormEqOfSplit.lean','absNorm_eq_of_split notMem_sq_of_split bad_primes')+
   ss(GI+'NotDvdDifferent.lean','not_dvd_different locP_eq_one locP_AA_eq_one')+
   ss(I+'PeriodLatticeIdealTrivialAtChainBadPrimes.lean','inverseHalfDifferent_local_trivial_at_prime_norm aaUnit_sall')+
   ss(I+'DegreeEqTotDeg.lean','eNat_mem laHyp_empty finAlg_step','closed_source_counterpart_with_unused_stage_detour_bypassed')+
   ss(I+'FinAlgJetSet.lean','finAlg_range thInd_congr finite_thInd pullLin finAlg_jetSet')+
   ss(I+'DerivAt0CompMem.lean','eq_sum_coordX exists_derivAt0 derivAt0_comp_mem')+
   ss(DV+'FiniteSemilocalHomLatticeClassesMod.lean','finite_card_classes')+
   ss(I+'FinAlgOfFinite.lean','FinAlg jetSet JetAlg VacEq','literal_interface')+
   ss(I+'VacuumEntireAndNormalizedJetsAlgebraicStatement.lean','vacuum_entire_and_normalizedJets_algebraic','VI_companion_endpoint')+
   ss(HOST,'VacIn thMM thZero thHalf thMoved eNat VacIn.toRec VacIn.thMM_rec VacIn.eNat_rec perAA_top','literal_host_only_binding')+
   ss(AMB,'AmbIn AmbIn.Ok AmbIn.amb AmbIn.toRec AmbIn.amb_eq_ambOf AmbIn.ok_iff','literal_host_only_binding'),
   'Proves the source conclusion using only host/VacIn fields. The Taylor component has finite degree; the theta function is not called polynomial.'),
cl('CA12','Finite generators for all actual canonical JetsIn values',
   'The source restricted finite allSet has a finite algebraic generator set. For actual Ok/IsTw with J=amb0 the modulus is exactly q_R^(m+1)*(T_u*q_R^(m+1)); CA11 proves the required selected-step FinAlg membership, so generator containment gives literal JetsIn.',
   ['CA11','TL19'], ['Finite actual twist range; canonical Ok/IsTw, exact J=amb0 and original containment of gens in the full embedded coefficient field.'],
   ss(I+'EvLgCanonical.lean','stepSet allSet finAlg_allSet gens gens_algebraic allSet_subset jetsIn_of_isTw lg_gens')+
   ss(I+'DegreeEqTotDeg.lean','hostFields hostAmb jetSet_amb totDeg degree_eq_totDeg badP badPrimes_finite₂ rowSG_subset Sb_subset amb0')+
   ss(I+'FinAlgOfFinite.lean','finAlg_biUnion FinAlg.closure'),
   'Retains the FinAlg filter in allSet and proves it for the actual step, rather than asserting all arbitrary prime sets have the needed geometry.'),
cl('CA13','The same-data canonical EvLg implication with exact antecedents',
   'Finite fixed/full coefficient-field requirements, PA9 actual amb0, TL character/orientation suppliers and CI local indices construct initial Ok, then the actual canonical replacement has Ok/Pins/IsTw/JetsIn, preserves the prescribed selection/frame/excluded set/twist range/J, and has universal-later ValLL0 plus FieldOK. TL13 yields Laws afterward.',
   ['CA12','CI15','CI16','CI17','CI18','CI19','TL13','TL14','TL15','TL16','TL21','PA9','PA13'],
   ['The source context/base/field-containment quantifiers remain; literal frame inclusion and Nonempty PreX are antecedents. No Later existence, arbitrary raw-data construction or unrestricted field enlargement is asserted.'],
   ss(I+'EvLgCanonical.lean','lg_gens exists_quot evLg_canonical','closed_literal_conditional_endpoint')+
   ss(I+'ExistsColumnInputAssembled.lean','exists_oriented Holds exists_holds_one exists_holds exists_colIn avoid isTwist_of_mem_set of_over valuesIn_of lg_colIn ev_of_forall')+
   ss(I+'ExistsColInJetsIn.lean','hasLetters_of_over')+
   ss(A+'CmQuadraticFormEqAlternatingForm.lean','Ctx large₂ Ev EvLg','literal_quantifier_interface')+
   ss(A+'LatAtLattice.lean','TC Pins Later','literal_retained_record_boundary')+
   ss(A+'SpreadLe.lean','PreX','literal_retained_raw_data'),
   'Closes the actual normalized analytic/canonical constructor join. A universal assertion over later assemblies is explicitly distinguished from their existence.',True)
]

targets = []
def target(path, name, group, scope, connections):
    t=source(path,name,'remaining_human_reconstruction_target')
    t.update(priority_group=group,remaining_human_scope=scope,source_connections=connections,
             human_status='continuation_target_only; retained antecedent or separate stage supplier')
    targets.append(t)

target(A+'LatAtLattice.lean','Pins',4,
       'CA13 proves the Pins join from the literal frame-inclusion antecedent plus the normalized piT quotient. SE may normalize coordinates for its supplied geometric data; constructing arbitrary compatible primitive frames is not inferred from the canonical analytic theorem.',
       ['CA13','TL16','SE15'])
target(A+'SpreadLe.lean','PreX',4,
       'The canonical implication starts with Nonempty PreX. Preserve the exact raw norm elements and congruence/geometry requirements; coordinate normalization is not a new arithmetic existence theorem.',
       ['CA13','TL16','SE15'])
target(A+'LatAtLattice.lean','Later',4,
       'CA13 supplies no Later existence. SE reconstructs its stated component stages and isolates the still-unsupplied full LocStage/NStage branches; keep their genuine data and quantitative geometric assumptions explicit.',
       ['CA13','SE16'])

closed=[]
for path,name,ids in [
    (DV+'CosetIndicatorThetaTorsionTranslates.lean','pres_thInd',['CA1','CA2']),
    (I+'NormalisedFamilySatisfiesEquivarianceLawsStatement.lean','normalisedFamily_satisfies_equivarianceLaws',['CA3','CA4','CA5','CA6','CA7','CA8','CA9']),
    (I+'GmapToAddSubgroup.lean','thIndEq_of_vacEq',['CA9','CA10']),
    (I+'DegreeEqTotDeg.lean','finAlg_step',['CA10','CA11','VI11']),
    (I+'EvLgCanonical.lean','jetsIn_of_isTw',['CA11','CA12']),
    (I+'EvLgCanonical.lean','evLg_canonical',['CA13'])]:
    t=source(path,name,'closed_source_target_under_literal_hypotheses')
    t['closed_by']=ids;closed.append(t)

# Verify the exact host-only record interface used to bypass an unused full
# Stages existence detour. This checks source bytes, not a Lean theorem.
audits=[]
for path,name,expected in [
    (HOST,'VacIn',['L','lat','ω₀','t0','γ₀','gC','gC_spec','kc']),
    (AMB,'AmbIn',['δ','V','cD']),
    (AMB,'AmbIn.Ok',['delta','dgen'])]:
    src=source(path,name,'literal_host_only_field_audit')
    lines,_,_=read_source(path)
    txt=b''.join(lines[src['line_start']-1:src['line_end']]).decode()
    fields=re.findall(r'^  ([^\s:]+)\s*:',txt,re.M)
    assert fields==expected,(name,fields,expected)
    audits.append(dict(source=src,fields=fields,field_count=len(fields),used_by=['CA11','CA13']))

out=dict(schema_version='1.3',artifact_version='0.17',date='2026-11-22',owner='/root/global_frame',
    repository=dict(url=URL,commit=PIN),
    range_convention='One-indexed inclusive; exact original declaration bytes, without newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
        replacement_arguments_formalized=False,pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof of the precisely stated supplied-data assertion or conditional assembly, with source hypotheses and quantifier order retained.'),
    claims=claims,files=[files[p] for p in sorted(files)],record_field_audits=audits,
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    prior_components_reused=['LP1','DR1','TL1','TL13','TL14','TL15','TL16','TL19','TL21','PA9','PA13','CI15','CI16','CI17','CI18','CI19'],
    same_iteration_companions=['VI','SE','NC'],independent_reviews=[],
    scope='CA1–CA10 reconstruct exact normalized indicator/Heisenberg/covariance laws, including the Gaussian determinant scalar. CA11–CA13 prove actual FinAlg, canonical JetsIn and the literal EvLg implication on the same supplied data. Raw PreX, arbitrary Pins.iX, source context/field requirements and Later existence remain explicit.',
    boundary_resolved=['Actual Pres(thInd)','Actual three-clause normalized-family EqP','Actual chosen-lift ThIndEq and ChiLaw','Actual finAlg_step with direct host-level proof bypassing unused Stages construction','Actual jetsIn_of_isTw with the allSet FinAlg restriction preserved','Literal evLg_canonical implication with exact original antecedents'],
    retained_inputs=[COMMON,BOUND,'Actual arithmetic context and its host, with fixed/full coefficient-field containment quantifiers','Literal Pins.iX/frame-inclusion and Nonempty PreX antecedents','Later existence, especially full LocStage/NStage as scoped by SE','No claim to the unused full adelic Weil/exists_kappa or exists_stages_over constructions'],
    dependency_precision=['CA1–CA4 do not use VI or any vacuum theorem.','Only independent CA2 is used by VI11; VI1–VI10 have no CA dependency.','CA5–CA9 use VI2/VI4/VI5/VI10; CA11 uses VI11 after CA10.','CA11 acts directly on host-level VacIn and therefore has no LocStage/NStage or full Stages existence edge.','CA13 supplies the literal canonical implication, then Laws by inherited TL13; no Laws-to-Ok cycle.','All predecessor claim fields and source arrays remain immutable.'])

mb=(HERE/'main.tex').read_bytes()
for c in claims:
    n=int(c['id'][2:]);a=mb.index(f'\\paragraph{{CA{n}:'.encode())
    z=mb.index(f'\\paragraph{{CA{n+1}:'.encode(),a+1) if n<13 else len(mb)
    c['proof_paragraph_sha256']=digest(mb[a:z])

for name,who,nums in [
    ('root_reviews_ca.txt','/root',list(range(1,14))),
    ('nc_reviews_ca_3_8.txt','/root/class_rank',list(range(3,9)))]:
    review=HERE.parent/'reviews_v0_17'/name
    if review.exists():
        rb=review.read_bytes();rt=rb.decode();ph={}
        for n in nums:
            sh=claims[n-1]['proof_paragraph_sha256']
            assert sh in rt,('independent review paragraph changed',n,sh)
            ph[f'CA{n}']=sh
        out['independent_reviews'].append(dict(reviewer=who,result='PASS',claim_ids=list(ph),
            review_record='../reviews_v0_17/'+name,review_record_sha256=digest(rb),paragraph_sha256=ph,lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc.extend([f"{c['id']} | {c['title']} | {c['mathematical_status']}",c['statement']])
    for s in c['sources']:
        loc.extend([f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            '  role: '+s['role'],'  file_sha256: '+s['full_file_sha256'],
            '  range_sha256: '+s['range_sha256'],'  '+s['url']])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.17',commit=PIN,targets=targets,closed_source_targets=closed,
    remaining_boundary='Normalized vacuum/indicator/covariance and finite-jet suppliers are now supplied by VI/CA. The actual canonical EvLg implication is proved with its original context, field, frame-inclusion and Nonempty PreX antecedents. Later existence is separate; SE records its remaining LocStage/NStage suppliers. No unused full Weil or Stages existence theorem is claimed.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),
    record_fields=sum(a['field_count'] for a in audits),next_targets=len(targets),closed_targets=len(closed),
    verified_equal_to_pinned_git_blob=True,artifact_sha256=out['artifact_sha256'])))
