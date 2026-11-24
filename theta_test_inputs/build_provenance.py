#!/usr/bin/env python3
"""Reproduce the TT source ledger from immutable Lean bytes, without a build.

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

T = D + 'Proofs/TwistedOperators/'
V = D + 'Proofs/DivisorProofs/'
DT = D + 'Definitions/TwistedInnerProducts/'
DV = D + 'Definitions/Divisors/'
ST = D + 'Statements/HeckeThetaIntegrals/'

common = [
 'One literal Choice R and its original HidaSetting are fixed, with the actual grid, normal datum, Weil representations, characters, measures, frames, reference twist and finite representatives.',
 'Standard elementary local-field topology, Haar integration, finite character orthogonality, finite-dimensional algebra, ideal/ray-class finiteness, and the explicitly cited prior human claims are used.',
 'Field membership is distinguished from integrality; no integral Weyl/dual-Weyl equality is inferred from rational basis descent.',
 'No global theta convergence, separation, matching tower, critical L-value algebraicity/nonvanishing, or positive spectral operator identity is inferred from the finite arithmetic alone.',
 'The reconstruction has not been formalized or kernel-checked; no Lean compilation, source mutation, PDF, RH or GRH proof is asserted.'
]
main_raw=(HERE/'main.tex').read_bytes()
paragraphs,proof_locs={},{}
for i in range(1,20):
 start=main_raw.index(f'\\paragraph{{TT{i}:'.encode())
 stop=main_raw.index(f'\\paragraph{{TT{i+1}:'.encode(),start+1) if i<19 else len(main_raw)
 paragraphs[f'TT{i}']=digest(main_raw[start:stop])
 proof_locs[f'TT{i}']=dict(file='main.tex',anchors=[f'TT{i}'],sha256=paragraphs[f'TT{i}'],
   line_start=main_raw[:start].count(b'\n')+1,line_end=main_raw[:stop].count(b'\n'),bytes=stop-start)
def claim(i,title,statement,deps,srcs,relation,assumptions=(),status='derived_simplification'):
 return dict(id=i,title=title,status=status,statement=statement,introduced_in='0.19',depends_on=deps,
   assumptions=common+list(assumptions),proof_location=proof_locs[i],proof_paragraph_sha256=paragraphs[i],
   expanded_notes=dict(file='report.txt',section=i),source_relation=relation,
   mathematical_status=('conditional_reduction_with_explicit_remaining_primitive_inputs' if status=='conditional_reduction'
     else 'proved_under_exact_declared_hypotheses'),sources=srcs)
LC=T+'IntegralUnfoldingVariablesMemFieldRange.lean'
SG=T+'IntegralRamifiedCharDetSingularMatrixCosetEqZero.lean'
BL=T+'IntegralDetCharInvertibleMatrixBallMemSubfield.lean'
DP=T+'LatticeDepthCompFrameBlockBoundedPeriodic.lean'
SF=T+'GlOrbitIntegralDepthDatumMemSubfield.lean'
OP=T+'OppositePathLocalTotalTensorMemCoefficientField.lean'
MT=T+'MovedTensorFactorMemCoeffField.lean'
FILL=V+'HasCompactSupportFlatIntegrand.lean'
FL=T+'FlatIntegrandFlippedTensorLocallyConstantCompact.lean'
UF=T+'UnfoldedFlipTensorValuesMemCoeffField.lean'
SUP=V+'FiniteUnfSupportOfNeOne.lean'
COS=V+'SumOKEx.lean'
IND=V+'GridKernelPairingIndependentOfExpansion.lean'
COEF=T+'TopRowNormalisedKernelChainPreservesCoeffs.lean'
LAST=T+'LastColumnNormalizedKernelChainCoeffField.lean'
BR=T+'BranchingPairingMemCoefficientField.lean'
SUM=T+'RowTestRationalSumsOfFiniteSumsMeaningful.lean'
ROOT=T+'IsIntegralOfPowEqOne.lean'
JETS=T+'NormalFormJets.lean'
AVG=T+'ExistsWeightedAverageHaar.lean'
PER=T+'PeriodAlgebraicFixedDegree.lean'
BOT=T+'BottomTrianglePeriodAlgebraic.lean'
NF=T+'NormalFormBottom.lean'
MONO=T+'RangeAlgebraMapMono.lean'
RATIO=T+'NormalFormToricRatio.lean'
NUM=DT+'MemHalfCosetSelf.lean'
CHOICE=DT+'ExistsMatchOver.lean'
AGREE=DT+'TwistPlacesOffPrimeQZero.lean'
FORM=ST+'FormulaAt.lean'
CFIN=V+'ContinuousReGLSymm.lean'
PURE=T+'FinitePureDataOfCosetIndicatorExpansionsDepth.lean'
CHAR=T+'NormalFormCharacters.lean'
PHASE=V+'ExistsPowEqOneOfLe.lean'
MOVED=T+'LatticesSelfDualMovedPair.lean'
HOM=T+'LatticeOrbitVectorsMovedPair.lean'
VAC=T+'VacuumVectorMovedPair.lean'
KALG=T+'NormalisedDefiniteKernelEntriesIsAlgebraic.lean'
HAAR=T+'IsAlgebraicIntegral.lean'
DEG=T+'ExistsFourierDegreeBound.lean'
RCHAR=T+'ExistsArchimedeanCharacterTheta.lean'
RT=T+'RatInOfDefinite.lean'
TOWER=T+'RatioOfLocalMatchingTowers.lean'

claims=[
 claim('TT1','Locally constant additive integrals are finite arithmetic sums',
 'A compactly supported locally constant K-valued function integrates to K under a Haar measure normalized on a compact open set containing zero; product Vars uses the actual unit volumes.',[],
 whole_decls(LC),'Replaces the source stabilizer/quotient calculation by an explicit common-period finite-coset proof, retaining the normalization set rather than assuming it is a subgroup.'),
 claim('TT2','Singular matrix cancellation and rational Haar ball volumes',
 'A ramified unit-character determinant integral over a matrix ball containing a singular matrix vanishes; an entirely invertible compact ball has a finite-coset formula with rational normalized volume.',[],
 ss(SG,'integral_coset_singular_eq_zero')+ss(BL,'integral_eq_sum_of_rightInv measureReal_eq_inv_natCast isOpen_rightStab isCompact_isOpen_glBall integral_glBall_mem'),
 'Explicit rank-one matrix gives determinant u and fixes the singular center; the nonsingular case uses a deep compact subgroup and vol(U)=1/[J:U]. Totalized versus convergent integral scope is explicit.'),
 claim('TT3','Field membership for the actual smallF frame-orbit integral',
 'The source smallF value is in K under its depth, ramification, conductor, character-value and half-norm hypotheses, including its nonintegrable zero branch.',['TT2'],
 ss(DP,'exists_unit_bound frameMatrixSecondColumnBlock_mul_transpose latticeDepth_comp_frameBlock_bounded_periodic')+ss(SF,'isCompact_ballM smallF_mem'),
 'Full rank gives a right inverse and bounds support; depth gives a finite matrix-ball decomposition; TT2 treats the two kinds of ball. This does not assert the missing analytic GL integral convergence.'),
 claim('TT4','Arithmetic and depth of the actual ordered Fourier flips',
 'The literal Tflip and moved tensors preserve their field values and IsTensor support/period clauses, with exact q-power and half-norm factors.',['TT3'],
 ss(OP,'apow_nat_half_mem fourierSum_mem invFourierSum_inv_mem smallF_mem phiA_mem flipTensor_mem flips_mem givenStage_mem nu_mem psiAt_mem apow_half_mem Tflip_mem_range')+
 ss(COS,'isNatDatum_squareFlip isNatDatum_sliceB isTensor_flipTensor isTensor_flips isTensor_Tflip')+
 ss(V+'MemGlLatCongOfSmul.lean','invT_mem_of_dual HasDepth.mul_glLatCong hasDepth_phiA')+
 ss(V+'ExistsGlLatCongMove.lean','exists_glLatCong_move')+
 ss(V+'MemMatLatSmulBlockLat.lean','GlobalTheory.SplitFlip.FourierDepth.fourier_exchange')+
 whole_decls(T+'WeilTraceAddCharAtPlaceMemSubfieldOfRoots.lean')+
 ss(T+'GridGivenPathTensorMemSubfield.lean','givenDatum_mem')+
 ss(MT,'exists_zpow_unit apow_half_mem loc_mem_of_unrAt GlobalTheory.MovedField.moved_mem'),
 'Finite character orthogonality proves lattice exchange; a primitive integral frame extends to a basis and realizes a period by a congruence matrix; exact inverse-transpose duality and conductor cancellation prove depth. Arithmetic uses TT3 and iterates the source flipOrder.'),
 claim('TT5','Compact flat integrals and bounded support phases',
 'The actual flat integrand is locally constant with compact support and genuinely integrable; bounded phase values under the two exact nonvanishing clauses and supplied PhasesIn put term.datum and AA scalars in K.',['TT1','TT4'],
 ss(FILL,'isLocallyConstant_of_isTensor continuous_fill continuous_phase exists_fill_entry exists_isCompact_of_mul_mem hasCompactSupport_flatIntegrand flatIntegrable_of_isTensor')+
 ss(FL,'flatIntegrand_lc_cpt')+ss(UF,'term_datum_mem_range')+
 ss(PHASE,'phase_bounded')+
 whole_decls(V+'FlatTensorVanishesUnlessLastRowBounded.lean')+
 ss(V+'FlatIntegrableAaVacOfConductor.lean','isLocallyConstant_aaVac hasCompactSupport_aaVac flatIntegrable_aaVac aaScalar_eq_pow flatIntegrable_aaVac_of_conductor')+
 ss(NUM,'PhasesIn','exact_input_definition'),
 'Recovers integration coordinates from actual fill entries; a translation-annihilator argument bounds the otherwise missing last row; the phase is a bounded polynomial on the required support. Distinguishes additive convergence from TT3 totalization.'),
 claim('TT6','Finite support of the literal unfolding labels',
 'Nonzero local unfolding terms admit compact representatives modulo the exact symmetric row groups, and induction gives finite actual global unfolding support.',['TT4','TT5'],
 ss(SUP,'symLev mul_stepPt_apply exists_symR_mul IsAuxiliaryHeckeCharacter stepPt_shift phase_shift char_eq_one tensor_shift exists_rowR_mul finite_image_mk exists_unit_bd finite_unfSupport_of_ne_one finite_unfSupport')+
 ss(T+'CharEqOneOfOpENeZero.lean','exists_embX_mul')+
 ss(D+'Definitions/Foundations/SimpleSum.lean','Free ch')+
 ss(DV+'FlatTensorVacuum.lean','symN symR Kept stepPt')+
 ss(T+'FourierJacobiUnipotentEqProdRootExchange.lean','midLev'),
 'Explicit rectangular free-tail translations give h^-1 d=kappa^-1 Et with a period ball independent of b. The tail length one and last-column cases are retained. Block factorization bounds both w and w^-1; compactness modulo an open right group proves finiteness.'),
 claim('TT7','Pure coset expansions and fixed-depth uniqueness',
 'The actual flat datum has a positive-depth finite half-coset expansion, with coefficient given by its value at centers; all expansions at one fixed depth use a common finite set of pure data.',['TT5','TT6'],
 ss(COS,'exists_isSBArgs_flat sum_reps_eq GridChoice.exists_isCosExpansion GridChoice.sumOK_flat_fin_ex GridChoice.sumOK_ex')+
 ss(NUM,'IsCosetDatum IsCosetExpansion expDepth IsCosetExpansion.coef_eq')+
 ss(PURE,'finDatum_eq pureDat_eq mem_support_of finite_pureDat_of_depth'),
 'Bounded support modulo a full period lattice gives actual finite coset representatives. Disjoint coset indicators, with the same prime set/idempotent/z, give uniqueness at centers and control the union over every fixed-depth expansion.'),
 claim('TT8','Expansion-independent class pairing and actual SumOKK',
 'All eleven literal SumOK fields hold, and SumOKK needs no additional asymptotic threshold or unused FunPr hypothesis.',['TT4','TT5','TT6','TT7','CR3'],
 ss(IND,'tOp vec_eq_tOp pairML colMap_eq rowMap_eq GlobalTheory.FunObj.sumOK_vec_indep')+
 ss(V+'ExistsIsThetaAtOfVac.lean','exists_isThetaAt_of_vac Normal.hasVec_of_defPair hasVec')+
 ss(CFIN,'isCO_levTop isCO_levRow posDef_top posDef_grid readOK GridChoice.sumOK_classes')+
 ss(DV+'InvVolConjLevelOne.lean','SumOK vCore_eq','literal_endpoint_and_formula')+
 ss(V+'RowSumOfHyp.lean','rowSum_of_hypotheses')+
 ss(FORM,'SumOKK','literal_endpoint_definition'),
 'Finite evaluation coordinates prove the tensor relation and multilinear independence; actual positive definite class finiteness and finite stabilizer orders supply the class conditions. Lists and supplies every record field.'),
 claim('TT9','Field descent in polynomial chains and branching',
 'Bideterminant coordinates descend to K exactly when polynomial coefficients do; actual rational frame actions, normalized kernel chains, branching and the actual source rational values preserve this field.',['CS2','VE5','VE11'],
 ss(COEF,'coeff_bVV_mem coeff_mem_of_repr_mem repr_mem_of_coeff_mem coeff_map_mem coeff_rhoVr_mem chainTo_preserves colMap_coeff_mem')+
 ss(LAST,'embLL_labLL rowMap_coeff_mem')+
 ss(BR,'projVV_of_mem map_frDet map_dualSubst isFunForm_map covOf_eq covOf_desc brPair_mem_range brPair_mem_coefField')+
 ss(T+'RationalFormCoordinatesCoeffMemCoefficientField.lean','typeX_mem coeff_formC_mem'),
 'A nonzero rational coefficient minor gives field descent without unimodularity; rational Fock Gram inverse and exact covariant/function identification give branching. Uses the original jX model and level characters rather than rank alone.',
 ['Actual normalized kk matrices are in K when JetsIn is invoked; no primitive algebraicity of those entries is assumed in TT13--TT14.']),
 claim('TT10','The actual SumRatK supplier under FieldOK',
 'The literal global vK is in the prescribed embLL range for every rational input and selected test, using actual finite support, expansions, quotient volumes, source values and kernel entries.',['TT4','TT5','TT7','TT8','TT9'],
 ss(SUM,'sAA_mem psiC_rat vK_mem sumRatK_of_sumOKK')+
 ss(DV+'InvVolConjLevelOne.lean','invGam colMap rowMap pairAt classSum vCore vCore_eq')+
 ss(CHOICE,'vK')+ss(FORM,'SumRatK','literal_endpoint_definition'),
 'Expands the actual vK finite sum and checks every factor. SumOKK is supplied by TT8. Retains FieldOK exactly as in SumRatK; proves no global-period identity.',
 ['The literal FieldOK of the same Choice R is supplied.']),
 claim('TT11','Actual character, root and phase number fields',
 'The exact Hida/level data supply NFChars, NFRoot and NFPhase via finite ray-class values, finite root adjunction and support-bounded additive phases.',['TT5','TT6','HF16','TL14'],
 ss(CHAR,'locIn_fin locIn_alg charsIn_nf GlobalTheory.RowEx.nfChars')+
 ss(ROOT,'exists_nf_of_finite rootsOne_finite isIntegral_of_pow_eq_one isIntegral_sqrt_nat nfRoot')+
 ss(PHASE,'exists_field_roots val_resCard_le exists_pow_eq_one_of_le phase_bounded phases_core')+
 ss(T+'NormalFormPhase.lean','nfPhase_of_sumOKK')+
 ss(NUM,'CharsIn PhasesIn')+
 ss(AGREE,'RootCl PhaseCl NFChars NFRoot NFPhase'),
 'Finitely many ray-class representatives control infinitely many local character values. Only finite active/AA square roots are adjoined; eta keeps its exact normalized half-twist. Actual finite support makes one root order suffice for phases.'),
 claim('TT12','Actual moved self-dual lattices and normalized vacuum',
 'The same rational frame turns the literal moved lattice into globLat(B^-1(xu)B,O^n); unitarity proves self-duality, and actual Weil covariance/norm preservation transports every vacuum clause.',['LP2','NB1','SF2'],
 ss(MOVED,'move_vec mem_globLat_move move_mem_UAd sd_latAt GlobalTheory.MovedSD.sd_srcLat_tgtLat')+
 ss(HOM,'movedLat_eq actO_latO_le actO_actO_inv actO_latO_onto GlobalTheory.MovedDict.actO_latO_moved')+
 ss(VAC,'movedVac_isVacO'),
 'Explicit matrix order and inverse are checked from lattice membership. Hom-lattice inclusion plus its inverse gives onto. Fock and unit-norm clauses are transported at identity infinity. No algebraicity of a comparison scalar is inferred.'),
 claim('TT13','Normalized jet algebraicity from same-vacuum finite Weil arithmetic',
 'Under the explicit finite algebraic Heisenberg-span condition for the actual moved vacuum, the actual normalized kk entries are algebraic; the same conclusion follows from the literal qualitative DictAt formula.',['TT4','TT9','TT12','TA10','VI4','VI9','VI10'],
 ss(KALG,'coefIn_dict applyAt0_monomial_mem opp_isAlgebraic kk_isAlgebraic')+
 ss(T+'FrameGramUnitaryIdentity.lean','fock_jets_heisO_fin')+
 ss(T+'FiniteHeisenbergTranslateSelfDualVacuumFockJets.lean','core coreNeg GlobalTheory.HeisTrans.main')+
 ss(T+'ThetaKernelAlgebraicExpansion.lean','ind_nsmul_mem mem_of_finite_cosets mem_algSpan psi_mem psiH_mem stdFst_mem finDatum_eq_sum_heis')+
 ss(D+'Statements/PlaceShiftStatements/DictAt.lean','DictAt','optional_stronger_input')+
 ss('src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLatticesGL3.lean','ThetaVectorUpToUnits','same_base_entire_function_definition')+
 ss(T+'ThetaJetMapWeightedTableScaleStatement.lean','thetaJetMap_weighted_table_scale')+
 ss(T+'JetOperatorBideterminantBasisReprIsAlgebraicStatement.lean','jetOperator_bideterminantBasis_repr_isAlgebraic'),
 'Uses direct rational-translate germs from TA/VI and finite Heisenberg algebra, bypassing the stronger arbitrary-theta NormSum input. Weighted homogeneity cancels exactly the original c0 and period powers. Retains the concrete same-representation finite-Weil arithmetic instead of assuming NFJet.',
 ['Equation TT.19 for each actual needed finite-adelic pair and actual fixed unit vacuum, or the literal same-data DictAt formula, is retained. Quantitative DictAt norms/denominators/q-adic units are not proved.'],
 'conditional_reduction'),
 claim('TT14','One finite field for all required normalized jet entries',
 'The universal JetsIn entries at least depth form a finite set, so their TT13 algebraicity supplies a single finite JetCl field.',['TT6','TT7','TT8','TT13'],
 ss(JETS,'dset jetCl_of_choice nfJet_holds')+ss(PURE,'mem_support_of finite_pureDat_of_depth')+ss(NUM,'JetsIn expDepth')+
 ss(AGREE,'JetCl NFJet'),
 'Uses fixed-depth disjointness to control every expansion, then finite class and matrix indices. Proves the actual finite-generation step without claiming the remaining moving-Weil arithmetic.',
 ['The exact TT13 finite-Weil/qualitative-dictionary input is supplied on the same choice.'],'conditional_reduction'),
 claim('TT15','Algebraic compact averaging and the common degree',
 'Haar averaging of a compact finite-dimensional representation algebraic on a dense set is an algebraic projector; actual bottom vacuum weights force at most one surviving place degree common to all twists.',[],
 ss(HAAR,'rho_mul_avg avg_mul_rho isAlgebraic_integral')+
 ss(RCHAR,'detPlus_neg_one_one detChar continuous_detChar isAlgebraic_detChar exists_realChar')+
 ss(DEG,'substMat_alg substMat_central avg_kernel_alg')+
 ss(T+'BottomTriangleMonomialSupportFinite.lean','classSum_vanish_off_finite'),
 'Replaces automorphism descent for the averaging matrix by the algebraic fixed-space/difference-space splitting. Explains the actual negative-source determinant exponent and finite-twist independence, then central infinite-order scalars select a common degree.'),
 claim('TT16','Normalized definite bottom periods and finite field generation',
 'For an actual bottom triangle with explicit finite-Weil arithmetic, the actual class-integral formula and common degree give SumsIn in one number field, retaining both Haar volumes and the separate full-Weil existence needed for NFBot.',['TT11','TT13','TT15','VI9','VI10','CR3'],
 ss(AVG,'level_all integral_eq_classSum_bottom')+
 ss(PER,'jet_negSp_heis even_bot jets_div_period_isAlgebraic')+
 ss(BOT,'ker_algebraic classSums_algebraic')+
 ss(T+'BottomTriangleAlgebraicityFiniteData.lean','span_classSums')+
 ss(T+'BottomTriangleRationalCoefficients.lean','galFld_fin compAt_mem fockSub_mem real_translate')+
 ss(NF,'field_of_gens sumsIn_bottom GlobalTheory.RowEx.nfBot_holds')+
 ss(T+'FiniteAdelicAlgebraicExpansion.lean','moved_translate_algComb','retained_finite_weil_arithmetic')+
 ss(T+'VacuumValueAlgebraicCongruence.lean','vac_eq_smul exists_level_fix level_vac_alg')+
 ss(T+'BottomExistsIntegrable.lean','exists_stdRig bottom_chars exists_bottomTri IsBottomTri.integrable')+
 ss(NUM,'IsBottomTri SumsIn BottomIn'),
 'Keeps the actual period v*Omega rather than calling Haar volume rational. Finite class representatives, degree support and rational substitutions reduce all values to finitely many normalized algebraic generators. Additional bottom Weil representation existence remains explicit.',
 ['For both source sides of the supplied actual bottom triangle, its finite-adelic vacuum images satisfy the finite algebraic Heisenberg-span assertion of TT.19.',
  'To conclude NFBot, actual bottom triangles/full adelic Weil representations with the stated characters must be constructed.'],
 'conditional_reduction'),
 claim('TT17','Bottom scalar-ratio descent from the actual common factorization',
 'Given the literal common bottom Factor and rational monomial periods, a finite coefficient-extraction proof gives lambda_t/lambda_t0 in K^times; definite automorphy proves the needed finite-point determination.',[],
 ss(RT,'ratPart ratPart_rat ratPart_eq exists_dual Factor.ratIn ratIn_of_definite'),
 'Expands the rational-part argument using a noncontinuous K-linear Hamel functional, a surjective polynomial map, injective actual function realizations and a nonzero comparison vector. Rational archimedean density is used only with continuity of the actual kernels.',
 ['The same triangle has the literal Factor with nonzero lambdas, common Pi,p,p-prime,J_t, and the stated rational monomial periods. Existence of Factor remains an analytic input.'],
 'conditional_reduction'),
 claim('TT18','Exact RatioK consequence of the matching tower',
 'The literal tower identity, exact critical nonvanishing interval and selected bottom Factor imply each actual square ratio belongs to the same field, with the original Big threshold order.',['TT17'],
 ss(TOWER,'sqRatio_mem_grid ratioK_holds')+ss(NUM,'LRatiosIn BottomIn NumbersIn')+
 ss(FORM,'RatioK','literal_endpoint_definition'),
 'Reproduces both tower product directions and proves division uses nonzero factors in [1,halfRank]; invokes Factor for the bottom triangle selected by NumbersIn, not an unrelated witness.',
 ['Actual nonzero square constants, LNe on [1-e0,halfRank], bottom existence, the same matching tower identity, and Factor for every valid selected bottom triangle remain supplied.'],
 'conditional_reduction'),
 claim('TT19','Compatible finite coefficient-field join and precise remaining boundary',
 'The actual finite fields for the eight NumbersIn clauses have a finite compositum, which gives FieldOK only after embedding in the same embLL or providing the literal same-object transport; the remaining analytic test endpoints are retained.',['TT10','TT11','TT14','TT16','TD15','TD16'],
 ss(MONO,'charsIn_mono rootCl_mono phaseCl_mono jetCl_mono lRatios_mono botCl_mono InNF.and nfAll_of')+
 ss(NUM,'NumbersIn NumbersIn.mono FieldIn FieldOK HasNumberField')+
 ss(AGREE,'AllIn LAgree GAgree WAgree SAgree Agree FlipAgree')+
 ss(CHOICE,'Choice RealOK IsBase Is')+
 ss(T+'ExKeyOf.lean','exKey_of','retained_compatible_choice_producer')+
 ss(T+'ExFieldOfKeyFinExKey.lean','exField_of_keyFin_exKey','retained_compatible_choice_producer')+
 ss(T+'TestChoicesExistLargeCoeffFieldAdelicData.lean','GlobalTheory.RowEx.dat_choice_exists','retained_final_choice_producer')+
 ss(FORM,'LinK InjK FormulaAt Formula2K RatioK')+
 ss('src/Formalism/LocalToGlobal/IndefiniteReal/CutTuples2.lean','ThmBop PartsE ThmAop PartsW','retained_stronger_operator_endpoints'),
 'Proves finite same-choice field assembly, not original Choice or FieldOK existence. Separates actual root/germ arithmetic from critical L-ratios and same-object transport; retains convergence, separation, tower and positive operator identities.',
 ['TT13/TT16 finite-Weil inputs, actual bottom representations and critical L-ratio algebraicity remain.',
  'The same embLL must contain the composite field, or actual LAgree/GAgree/WAgree/SAgree/FlipAgree constructions and original Choice.Is including RealOK must be supplied.'],
 'conditional_reduction')
]

# These target ranges identify actual producers, with their unresolved duties
# stated narrowly. Their existence in Lean source is not a human proof.
target_specs=[
 (1,T+'ExistsUnitModulusScalarLocal.lean','exists_kappa',
  'Prove arithmetic of the scalar comparing the actual finite-adelic moved vacuum with the same positive Iop model, or prove the narrower finite algebraic Heisenberg-span assertion TT.19 for every required grid pair.',
  'TT12 proves the actual moved lattice and all normalized vacuum clauses. TT13--TT14 prove germ algebraicity, exact period cancellation and finite jet-field generation conditional only on this arithmetic or the literal qualitative DictAt. Full DictAt quantitative denominator, all-embedding norm and local-unit estimates are not claimed.',
  [(T+'ExistsLatticesEntireIntertwining.lean','movedVacuum_dict'),(T+'DictionarySizeBound.lean','dictAt_big')],['TT12','TT13','TT14']),
 (1,T+'FiniteAdelicAlgebraicExpansion.lean','moved_translate_algComb',
  'Prove the actual bottom Weil action preserves the finite algebraic Heisenberg span of the same vacuum, including nonsplit support and its splitting-character normalization.',
  'TT15--TT16 already prove compact algebraic averaging, common degree, correct Haar-volume period, and finite field generation from this input. The generic finite-Adelic algebraicity producer still uses congruence-vacuum values, split-place action and rational/real decomposition, all on the same chosen representation.',
  [(T+'WeilActionSplitSupport.lean','suppSplit_algComb'),(T+'ThetaExpansionRationalPoints.lean','rat_real_algComb'),
   (D+'Proofs/AdelicLatticeProofs/ExistsRepSuppSplit.lean','exists_rep_suppSplit')],['TT15','TT16']),
 (1,RATIO,'ratio_algebraic',
  'Prove actual completed critical Hecke-L ratio algebraicity for the exact characters in LRatiosIn, preserving normalization, field embeddings and nonzero reference denominators.',
  'TT19 reduces common-field generation to finitely many actual ratios. TT11 character fields and any qualitative finite-order L(1) result do not supply these critical CM ratios. The source uses ToricRatioConjugates plus the completed L characterization and nonvanishing.',
  [(V+'ToricRatioConjugatesOfTransport.lean','toricRatioConjugates_of_transport'),(RATIO,'nfRatio')],['TT11','TT19']),
 (1,T+'LinearIndependenceOfCuspidalLifts.lean','linK',
  'Reconstruct convergence of the actual iterated theta-chain tests and Bessel pairing, with the original cusp-lift and uniform scale hypotheses.',
  'TT1 and TT5 prove genuine local additive convergence; TT3 only totalized multiplicative arithmetic. None replaces the actual global rapid-decay/theta convergence used here.',
  [(T+'ThetaConvergenceAtScale.lean','thetaConv_and_isAutFun_thetaChi_of_hidaSetting'),
   (T+'BesselPeriodCorankConvergesColumn.lean','bplusConv_col')],['TT1','TT3','TT5']),
 (1,T+'InjKOfSeparates.lean','injK_of_separates',
  'Supply actual FunctionalsSeparate for the same theta/Bessel realization, then apply the literal convergence and real-match join to obtain InjK and RealOK.',
  'No stronger primitive producer of FunctionalsSeparate was identified in the traced proof subtree; it is explicitly an input to this actual InjK producer. Finite-dimensional rational values and finite support do not prove separation.',
  [(D+'BlockTheory/DivisorBase/LevelPlusSubgroup.lean','FunctionalsSeparate'),
   (T+'InjKOfSeparatesLinB.lean','injK_of_separates_linB'),(T+'IsExOfSeparates.lean','isEx_of_separates')],['TT19']),
 (1,T+'RowTestLiftFormulaPrincipalLevel.lean','formulaAt_steps',
  'Prove the four actual same-choice period identities ProjAt, FlipAt, UnfoldAt and JetsAt, with absolute convergence and nonzero square constants, before concluding Formula2K.',
  'TT8 supplies actual SumOKK and TT10 its FieldOK arithmetic. The retained equality between this finite sum and the actual period tests is not a formal consequence of those arithmetic statements.',
  [(T+'ProjectionOfFunctorialityAdopted.lean','CompanionTheory.Member.projection_of_functoriality'),
   (T+'UnfoldingOfCuspidalLifts.lean','stepUnfold'),(T+'JetsOfOrthogonalSum.lean','stepJets')],['TT8','TT10','TT19']),
 (1,TOWER,'ratioK_holds',
  'Construct the matched square tower, nonzero square constants, the full critical nonvanishing interval, and the common bottom Factor for the same selected bottom triangle.',
  'TT17 gives the explicit noncontinuous rational-part descent from Factor, and TT18 checks the exact tower arithmetic, product directions and denominators. The tower and Factor are not assumed proved by those conditional deductions.',
  [(TOWER,'sqRatio_mem_grid'),(V+'TowerOfThetaMatching.lean','tower')],['TT17','TT18']),
 (1,T+'BottomExistsIntegrable.lean','exists_bottomTri',
  'Construct the additional full adelic Weil representations with the exact parity-twisted characters on the standard bottom spaces, giving actual bottom triangles for all squares.',
  'TT16 proves SumsIn for a supplied bottom triangle under finite-Weil arithmetic; the standard lattices and ranks do not by themselves construct its new full representations. The grid W is not silently reused on different spaces.',
  [(T+'BottomExistsIntegrable.lean','bottom_chars')],['TT12','TT16']),
 (1,T+'ExKeyOf.lean','exKey_of',
  'Construct compatible Choice.Is and the exact field-extension transports so the finite NumbersIn compositum embeds into the same actual Base and coefficient embedding.',
  'TT19 proves the finite field join but retains RealOK/separation and the actual LAgree/GAgree/WAgree/SAgree/FlipAgree producers. HF16--HF18 supply the HFrame value field only, not the full Choice.FieldOK.',
  [(T+'ExFieldOfKeyFinExKey.lean','exField_of_keyFin_exKey'),
   (T+'TestChoicesExistLargeCoeffFieldAdelicData.lean','GlobalTheory.RowEx.dat_choice_exists')],['TT11','TT14','TT16','TT19'])
]
targets=[]
for priority,path,name,objective,remaining,support,ids in target_specs:
 s=source(path,name,'retained_primitive_or_actual_producer')
 targets.append(dict(priority=priority,path=path,declaration=s['declaration'],source=s,
  source_ranges=[s]+[source(p,n,'substantive_remaining_supplier') for p,n in support],
  objective=objective,remaining_human_scope=remaining,already_reconstructed=ids,
  supplied_conclusion_not_assumed_proved=True))
closed_specs=[
 (LC,'integral_mem_range',['TT1']),
 (SG,'integral_coset_singular_eq_zero',['TT2']),
 (BL,'integral_glBall_mem',['TT2']),
 (SF,'smallF_mem',['TT3']),
 (OP,'Tflip_mem_range',['TT4']),
 (MT,'GlobalTheory.MovedField.moved_mem',['TT4']),
 (UF,'term_datum_mem_range',['TT5']),
 (SUP,'finite_unfSupport',['TT6']),
 (PURE,'finite_pureDat_of_depth',['TT7']),
 (IND,'GlobalTheory.FunObj.sumOK_vec_indep',['TT8']),
 (V+'RowSumOfHyp.lean','rowSum_of_hypotheses',['TT8']),
 (SUM,'sumRatK_of_sumOKK',['TT8','TT9','TT10']),
 (CHAR,'GlobalTheory.RowEx.nfChars',['TT11']),
 (ROOT,'nfRoot',['TT11']),
 (T+'NormalFormPhase.lean','nfPhase_of_sumOKK',['TT11']),
 (MOVED,'GlobalTheory.MovedSD.sd_srcLat_tgtLat',['TT12']),
 (VAC,'movedVac_isVacO',['TT12']),
 (HAAR,'isAlgebraic_integral',['TT15']),
 (DEG,'avg_kernel_alg',['TT15'])
]
closed=[]
for path,name,ids in closed_specs:
 s=source(path,name,'literal_completed_source_target')
 closed.append(dict(path=path,declaration=s['declaration'],closed_by=ids,source=s,
  scope='The human argument reconstructs this source conclusion under the exact original data and explicit hypotheses in the named paragraphs. SumRatK retains FieldOK; no global analytic identities are added.'))
conditional=[
 dict(source=source(KALG,'kk_isAlgebraic','conditionally_reconstructed_jet_supplier'),
  reconstructed_by=['TT13'],retained=['Same actual finite-Weil arithmetic TT.19 or literal qualitative DictAt'],
  scope='Actual germ and homogeneous normalization calculation reconstructed; no arbitrary CoefInTranslate or full quantitative DictAt asserted.'),
 dict(source=source(JETS,'nfJet_holds','conditionally_reconstructed_finite_field_supplier'),
  reconstructed_by=['TT7','TT13','TT14'],retained=['TT13 exact finite-Weil or qualitative dictionary hypothesis'],
  scope='Actual finite set of entries over every least-depth expansion and finite field generation reconstructed.'),
 dict(source=source(NF,'GlobalTheory.RowEx.nfBot_holds','conditionally_reconstructed_bottom_field_supplier'),
  reconstructed_by=['TT15','TT16'],retained=['Actual bottom Weil representations','Finite algebraic action on the same vacuum'],
  scope='Actual Haar-volume periods, common degree and finite generation reconstructed.'),
 dict(source=source(RT,'Factor.ratIn','conditionally_reconstructed_factor_ratio'),
  reconstructed_by=['TT17'],retained=['The actual common Factor','Rational monomial periods'],
  scope='Complete rational-part descent reconstructed; existence of Factor is not claimed.'),
 dict(source=source(TOWER,'ratioK_holds','conditionally_reconstructed_tower_arithmetic'),
  reconstructed_by=['TT17','TT18'],retained=['Actual matching tower','LNe critical interval','Nonzero constants','Bottom existence and Factor'],
  scope='All field arithmetic and exact product denominators reconstructed.'),
 dict(source=source(MONO,'nfAll_of','conditionally_reconstructed_field_join'),
  reconstructed_by=['TT11','TT14','TT16','TT19'],retained=['Critical L-ratio algebraicity','Remaining jet/bottom finite-Weil suppliers'],
  scope='Finite compositum for all eight literal NumbersIn clauses; embedding and same-choice transport remain explicit.')
]
record_specs=[
 (DV+'InvVolConjLevelOne.lean','SumOK',['flat','flatA','fin','ex','vec','indep','cls','gam','wts','br','read'],
  {f:'TT8' for f in ['flat','flatA','fin','ex','vec','indep','cls','gam','wts','br','read']},True),
 (NUM,'NumbersIn',['chars','eighth','roots','phases','sqrt','jets','ratios','bottom'],
  dict(chars='TT11',eighth='TT11',roots='TT11',phases='TT11',sqrt='TT11',jets='TT13--TT14 conditional',
       ratios='retained actual critical L-ratio algebraicity',bottom='TT16 conditional'),False),
 (CHOICE,'Choice',['sc','G','W','M','ρ','ξ','cv','rm','S','rp','n','e','c'],{},False),
 (CHOICE,'IsBase',['guard','weil','vol','vac','w_ne','const'],{},False),
 (CHOICE,'Is',['real'],dict(real='retained RealOK/separation; Is extends IsBase'),False)
]
record_audits=[]
for path,name,expected,support,all_constructed in record_specs:
 s=source(path,name,'literal_record_field_inventory')
 rows=read_source(path)[1][s['line_start']-1:s['line_end']]
 field_names=[m.group(1) for line in rows[1:] if (m:=re.match(r'^  ([^\s:]+)\s*:',line))]
 assert field_names==expected,(name,field_names)
 record_audits.append(dict(record=s['declaration'],source=s,field_count=len(field_names),
  all_fields_constructed=all_constructed,
  fields=[dict(name=f,supplied_by=support.get(f,'explicit supplied actual Choice; construction retained')) for f in field_names]))

out=dict(schema_version='1.3',artifact_version='0.19',date='2026-11-22',component='theta_test_inputs',
 owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes, without Unicode or newline normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Human proof under exact declared hypotheses, possibly using a shorter explicitly proved argument.',
  conditional_reduction='The actual mathematical implication is proved; the specifically identified primitive arithmetic/analytic supplier remains supplied.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,record_audits=record_audits,
 prior_components_reused=['CS','CR','SF','LP','NB','VE','TA','VI','TL','TD'],same_iteration_companions=['HF'],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Actual compact local integral arithmetic including singular-ball cancellation and totalized smallF distinction',
  'Actual finite Fourier/depth iteration and local term values',
  'Actual finite unfolding support, least-depth expansion uniqueness and every SumOK field',
  'Literal SumRatK under its literal FieldOK',
  'Actual NFChars, NFRoot and NFPhase on the fixed Hida/level data',
  'Actual same-frame moved lattice and normalized vacuum geometry',
  'Substantive normalized-jet and finite-jet-field deduction from explicit same-vacuum finite-Weil arithmetic',
  'Algebraic compact Haar projector and same-twist degree selection',
  'Substantive common bottom-period and scalar-ratio arithmetic under explicit remaining suppliers'],
 scope_precision=[
  'Field/rational span is distinguished from integral lattice membership.',
  'No compact-support conclusion is inferred for the global theta/Bessel test merely from finite local support.',
  'The finite-Weil arithmetic on the actual vacuum remains explicit, as do critical L-ratio algebraicity and common Factor/tower identities.',
  'The common bottom period includes the actual Haar volume, which need not be rational.',
  'No arbitrary field embedding is interchanged with limits, derivatives or Haar integrals.',
  'NumbersIn finite field generation does not by itself place that field inside the original embLL or prove Choice.Is/RealOK.',
  'LinK, InjK, Formula2K, original RatioK suppliers and positive ThmAop/ThmBop/PartsW/PartsE remain as stated.',
  'All predecessor artifact files and source checkout bytes are preserved.'])
review_specs=[('root_reviews_theta_test_inputs.txt','/root',list(range(1,20)),
 'Independent full TT mathematics, exact source interfaces and retained analytic/field boundary review.')]
for filename,reviewer,indices,scope in review_specs:
 p=HERE.parent/'reviews_v0_19'/filename
 if not p.exists():continue
 raw=p.read_bytes();content=raw.decode();chosen={f'TT{i}':paragraphs[f'TT{i}'] for i in indices}
 for key,sha in chosen.items():assert sha in content,('review paragraph changed',filename,key,sha)
 out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
  review_record='../reviews_v0_19/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
  paragraph_range='Bytes from named TT paragraph to immediately before next TT paragraph; EOF for TT19.',lean_replay=False))
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
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.19',commit=PIN,targets=targets,
 closed_source_targets=closed,conditionally_reconstructed_targets=conditional,retained_inputs=common,
 remaining_boundary='Actual SumOKK, SumRatK under FieldOK, and elementary coefficient fields are supplied. Same-vacuum finite-Weil arithmetic, critical CM L-ratios, global theta convergence/separation/matching, bottom Factor/tower and exact compatible field/choice construction remain as narrowly stated.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 distinct_claim_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 claim_source_files=len({s['path'] for c in claims for s in c['sources']}),source_files=len(files),next_targets=len(targets),
 completed_source_targets=len(closed),conditionally_reconstructed_targets=len(conditional),
 verified_equal_to_pinned_git_blob=True,record_field_counts={a['record']:a['field_count'] for a in record_audits},
 independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']]),ensure_ascii=False))
