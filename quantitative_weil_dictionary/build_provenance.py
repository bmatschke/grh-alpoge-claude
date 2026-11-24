#!/usr/bin/env python3
"""Reproduce the QD source ledger from immutable Lean bytes, without a build.

This script checks the quantitative Weil dictionary's source provenance. It
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
ST = D+'Statements/PlaceShiftStatements/'
GL3 = 'src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLatticesGL3.lean'
EQAT = 'src/Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/IsDiscriminantTwelfthRootOfIdealLattice.lean'
SPLIT = T+'SplitOff.lean'
CHAR = T+'SplitIdempotentUnitDecomposition.lean'
DET = T+'EvenRankSelfDualUnitary.lean'
RAT = T+'DifferentiableThetaLocalSum.lean'
PER = FND+'ThetaPullbackConstantSqEqDet.lean'
NORM = T+'JetScalarUnitModulus.lean'
KAP = T+'ExistsUnitModulusScalarLocal.lean'
MOV = T+'ExistsLatticesEntireIntertwining.lean'
HEIS = T+'FiniteHeisenbergTranslateSelfDualVacuumFockJets.lean'
DICT = T+'DictionarySizeBound.lean'

common = [
 'The literal D7 CM host, supplied Choice and Choice.Is, standard sign-minus-one additive character, prescribed splitting characters and actual finite/real Weil action are fixed.',
 'The three literal source endpoints retain their original FunPr.Hypotheses2 and forall D NormSum.Inp D arguments; no independent construction of those entire packages is claimed.',
 'DefPair is exactly a top edge or a rightmost chi edge; source/target reversal, negative Hermitian source and opp conjugation on chi are retained.',
 'The rational orthonormal frames, original period delta, un-killed half-point, oddE0, nonzero c0 and actual self-dual integral lattices are not replaced or renormalized.',
 'f=D.R.f=[F:Q]. The finite coset datum has k>0, IsCosetDatum k d, d.z=1 and d.P=locPl of the same choice.',
 'Finite-dimensional Hermitian spectral theory, finite-place field weak approximation, ideal-class finiteness, finite character orthogonality and absolutely convergent positive-Hermitian Gaussian calculus are explicitly used.',
 'All-conjugate modulus and local units follow from algebraic power/determinant identities. Distinguished complex unitarity alone is used only for the remaining positive real factor.',
 'No arbitrary embedding is interchanged with a derivative, infinite sum, limit or integral. No uniform number field for infinitely many arbitrary dictionaries is asserted.',
 'The result is a human mathematical reconstruction, not Lean kernel replay; no Lean build, checkout edit, PDF, full RH or GRH conclusion is claimed.'
]
main_raw = (HERE/'main.tex').read_bytes()
paragraphs = {}; proof_locs = {}
for n in range(1,23):
 start=main_raw.index(f'\\paragraph{{QD{n}:'.encode())
 stop=main_raw.index(f'\\paragraph{{QD{n+1}:'.encode(),start+1) if n<22 else len(main_raw)
 key=f'QD{n}';paragraphs[key]=digest(main_raw[start:stop])
 proof_locs[key]=dict(file='main.tex',anchors=[key],sha256=paragraphs[key],
  line_start=main_raw[:start].count(b'\n')+1,line_end=main_raw[:stop].count(b'\n'),bytes=stop-start)

def claim(i,title,statement,deps,srcs,relation,assumptions=()):
 return dict(id=i,title=title,status='derived_simplification',statement=statement,introduced_in='0.22',
  depends_on=deps,assumptions=common+list(assumptions),proof_location=proof_locs[i],
  proof_paragraph_sha256=paragraphs[i],expanded_notes=dict(file='report.txt',section=i),
  source_relation=relation,mathematical_status='proved_under_exact_declared_hypotheses',sources=srcs)

claims=[
 claim('QD1','Positive-power arithmetic, all embeddings and local units',
  'Algebraic positive powers with all-conjugate norm one or all-q-adic unit norm transfer those properties to every root; roots of unity also remain algebraic integers.',[],
  ss(GL3,'Mod1All')+ss(SPLIT,'UnitAt')+ss(DET,'NormOne NormOne.mul NormOne.pow NormOne.of_pow NormOne.root')+
  ss(T+'JetScalarIdempotentValue.lean','qbar_of_root mod1All_root unitAt_mul unitAt_inv unitAt_root'),
  'Proves the actual field arithmetic separately from the distinguished norm. Positive exponents and algebraicity are retained.'),
 claim('QD2','All-conjugate and local-unit values of the actual splitting characters',
  'Every finite splitting-character value has Mod1All; it has UnitAt q if the idele is one above q. The positive-power CM conjugate-ratio formula is proved.',['QD1','WA7','HF9'],
  ss(CHAR,'values_of_rel inf_val exists_pow_rel finIso_idem char_split_value offPrime_conj split_chars')+
  ss(T+'SplittingHeckeCharExistsArchimedeanExponent.lean','exists_zpow_of_trivial map_sq_eq_one exists_hasInfExp')+
  ss(AL+'ContinuousCharacterFiniteOrderIntegralUnits.lean','finite_order_of_small char_finUnit_finite_order')+
  ss(FND+'UnitaryHeckeCharacterValues.lean','exists_coprime_denom root_value'),
  'The argument strengthens WA7 using the exact finite class relation and conjugate ratios, testing ResEta only against the actual HF9 character.'),
 claim('QD3','Exact EqAt witnesses force rational unitary determinant units',
  'The determinant of a rational unitary matrix has all complex conjugates on the unit circle and is a unit at every embedding above q when both actual lattices are EqAt q standard.',['QD1'],
  ss(EQAT,'EqAt')+ss(DET,'norm_le_one_of_int norm_nat_eq_one det_mul_det_star norm_det_complex norm_det_le norm_det_padic')+
  ss(RAT,'norm_det_padic'),
  'Uses integer denominators prime to q in both directions for U and its inverse, not rank or rational-span equality.'),
 claim('QD4','Finite quadratic Gauss phase without a parity restriction',
  'A finite root-valued quadratic Gauss sum is zero or positive times a root of unity, including the dyadic case.',[],
  ss(FND+'UnitaryFiniteGaussSumPhaseRootOfUnity.lean','finite_quot gauss_phase')+
  whole_decls(D+'Proofs/SiegelThetaTransformation/IsZeroOrPosMulRootOfUnityFiniteGaussSum.lean'),
  'A shorter finite Fourier proof reduces the radical and proves (FT)^3=(S/sqrt(N))I; its determinant forces the phase to have finite order.'),
 claim('QD5','Positive-intertwiner compositions have finite-order phase',
  'For the actual compatible commensurable self-dual period lattices, the composition scalar for positive intertwiners is a root of unity.',['QD4','VI2','VI5'],
  ss(FND+'AdmissibleCharactersExist.lean','wLin cocExp wLin_heis iop_eq_itw triple_constant')+
  ss(FND+'KernelLatticesFormSelfDualTriples.lean','theta_cocycle_eq_exp_hermitian nice_of_klat index_ne_zero iop_self klat_triples'),
  'Proves exactly the finite-order phase needed by QD through the finite Heisenberg triple-projector trace. Does not newly assert the stronger fixed eighth-power bound.'),
 claim('QD6','Theta-product change-of-basis scalar squares to a determinant',
  'For the same product theta and half-point, theta_bprime=c I theta_b with c^2=zeta det(G), zeta a root of unity; fixed vectors and rank zero are treated.',['QD4','QD5','VI2','VI5','VI10'],
  ss(PER,'ph_const_mul_det sq_eq_of_ph infinite_norm_one exists_unitary pullB_mem const_sq_of_det_ne_zero const_sq_eq_det')+
  ss(FND+'PhDetMulIntegral.lean','term_eq value_eq term_shift ph_det_mul_integral')+
  ss(FND+'IntegralGaussianUnitary.lean','integral_gaussian_unitary')+
  ss(FND+'HeisenbergReproducingKernelSumSpec.lean','norm_kerTerm_le kerSum_spec')+
  ss(FND+'IntegralHeisKerSumDiag.lean','integral_heis_kerSum_diag'),
  'Expands the actual convergent Gaussian trace, finite quadratic phase and determinant conjugation identity, then removes fixed vectors by one rational norm-one scalar.'),
 claim('QD7','Rational period-intertwiner transport has all arithmetic norms',
  'The actual Iop pullback under rational unitary U,Uprime has a Mod1All scalar, and UnitAt q under the four exact EqAt lattice premises.',['QD1','QD3','QD5','QD6','VI10'],
  ss(DET,'det_move onB_move push_LaB push_La pullB_move iop_move iop_pull_rat'),
  'Retains the restriction-of-scalars determinant and the unchanged oddE0 presentation scalar; avoids the both-ranks-even CA5 route.'),
 claim('QD8','Actual compact vacuum character and rational finite jet transport',
  'The actual real vacuum scalar is an integer determinant character; rational automorphy gives the exact JetTh substitution with Mod1All and local units, then rational JetKap propagation.',['QD3','QD7','WA3','CW13','CW22','CW24'],
  ss(RAT,'vac_scalar om_rat move_fin jets_scale jets_subst coord_data arith jetTh_rat GlobalTheory.T.differentiable_theta_local_sum')+
  ss(V+'WeilDatumRealPlacesFockVacuumCharacter.lean','vacuum_character')+
  ss(T+'SplittingHeckeCharExistsArchimedeanExponent.lean','exists_zpow_of_trivial')+
  whole_decls(T+'JetScalarRationalTranslate.lean'),
  'Replaces only the auxiliary eta uniqueness route: classify the actual compact U(n) line character by diagonal tori and permutation conjugation. The exact c-inverse/top and c/chi orientations are retained.'),
 claim('QD9','Root-of-unity scalar for the standard-lattice base case',
  'When both actual moved vertex lattices are globally standard, JetKap holds with a root of unity, hence with every all-embedding/local-unit conclusion.',['QD1','WA3','CW5'],
  ss(T+'IsOpenLevelGroupSubgroupOf.lean','mem_Qbar_of_pow norm_map_of_pow isOpen_levelGroup_subgroupOf exists_pow_mem exists_pow_level exists_root moved_root GlobalTheory.T.standard_lattice_size_sum')+
  ss(DV+'KernelNormConstantSpec.lean','DefPair'),
  'Uses the compact stabilizer character or the same smooth principal level, keeping c0 and the period-normalized e0 unchanged.'),
 claim('QD10','Exact distinguished norm of a JetKap scalar',
  'Any JetKap scalar has complex absolute value one by the two identical c0-weighted mean-square identities.',['VI2','VI5','WA15','CW24'],
  ss(NORM,'mean_eq_of_swap setIntegral_shift vol_fd normSq_real_form scal_eq normSq_intertwiner_image_vacuum_selfDual normSq_scalar norm_eq_one_of_sq norm_kappa')+
  ss(T+'ExistsUnitScalarFourier.lean','fock_jets_moved intertwining_mem_ne_zero'),
  'Explains the normalized fundamental-domain averages, exact period scaling, and entire-function identity before canceling |c0|^2 N0.'),
 claim('QD11','Split moves read as the same positive lattice intertwiner',
  'A split-supported pair propagates JetKap with positive real factor times a root of unity times the exact crossed splitting-character value.',['QD5','WA5','VI2','CW24'],
  ss(T+'SplitIdempotentLatticePair.lean','moves_gen law_infRat exists_reading jets_move exists_detAt jets_transfer GlobalTheory.T.split_idempotent_lattice_pair')+
  ss(T+'JetScalarLocalIdentity.lean','om_toPair_mul jetKap_split_move')+
  ss(D+'Proofs/DecoratedLatticeProofs/SplitPlacePairMovesLatticeVacuumReading.lean','moves_reading')+
  ss(AL+'OmVacuumEqSplitFacSmulSum.lean','form_sum om_vacuum_eq_splitFac_smul_sum'),
  'The finite two-half sum, nonzero positive functional evaluation, rational approximation modulo twice the common lattice and exact period quotient reindexing fix its phase.'),
 claim('QD12','Arithmetic propagation along finite split-supported words',
  'The positive factor is one; the remaining crossed-character/root-of-unity scalar has Mod1All and UnitAt at every avoided rational prime, also through inverses and finite products.',['QD1','QD2','QD10','QD11'],
  ss(T+'JetScalarIdempotentValue.lean','moved_split')+ss(CHAR,'offPrime_conj split_chars')+ss(SPLIT,'OffPrime splitOff'),
  'Distinguished unitarity is used solely to cancel the positive factor after the independent algebraic character calculation; subgroup closure is algebraic finite-word closure.'),
 claim('QD13','Norm-one correction and nonsplit denominator control',
  'Hilbert-90 ratios and finite-place approximation correct actual reflection parameters to prescribed level precision while keeping both inverses integral at every other nonsplit place.',[],
  ss(AL+'NormOneApproximationAtLevelPrimes.lean','hilbert90_matrix_subalgebra_norm_one GlobalTheory.UnRep.normOne_approx')+
  ss(AL+'ExistsNormOneReflectionCorrectionAtLevel.lean','exists_nat_smul_map_mem exists_refl_correction')+
  ss(AL+'ExistsUnitaryCorrectionCongruentOneAtLevel.lean','congAt_mul congAt_conj exists_unitary_correction')+
  whole_decls(AL+'ValuationEqOneOfNormOneOfNotMoved.lean'),
  'A shorter mixed local approximation proof supplies the actual definite-vertex correction; conjugation-fixed valuations vanish even at ramified primes.'),
 claim('QD14','Actual rational/split/stabilizer factorization away from a finite set',
  'For every actual definite vertex g and finite rational-prime set Q, g=r s k exactly, with r rational finite, s a finite word supported at split primes away from Q and k the original lattice stabilizer.',['QD13','WA10'],
  ss(AL+'UnitaryGroupWeakApproximationAtPrimes.lean','core skewPart weak_approximation')+
  ss(AL+'ExistsRationalUnitarySplitDenominator.lean','inv_integral exists_rep_split_denominator')+
  ss(AL+'ExistsUnitaryAdelicDecompositionSplitSupport.lean','mix GlobalTheory.UnRep.SplitRep.mix_mul_mix GlobalTheory.UnRep.SplitRep.isUnA_mix GlobalTheory.UnRep.exists_rep_suppSplit')+
  ss(AL+'ExistsRepSuppSplit.lean','exists_rep_suppSplit')+
  ss(T+'ExistsRationalSplitStabilizerDecomposition.lean','stab_iff exists_rat_split_lat'),
  'Uses a rational Cayley chart, finitely many corrected reflections and a literal conjugation-fixed support cut. Its claimed scope is the definite vertices required by QD, not every generic source Hermitian form.'),
 claim('QD15','One arithmetic scalar for each protected finite prime set',
  'For every finite Q where the two original lattices are standard, a JetKap scalar has Mod1All and all UnitAt q for q in Q.',['QD3','QD7','QD8','QD9','QD12','QD14'],
  ss(T+'ExistsRationalFiniteTranslate.lean','eqAt_refl eqAt_symm eqAt_trans exists_dec')+
  ss(T+'ExistsRationalSplitStabilizerDecomposition.lean','exists_rat_split_lat')+
  ss(KAP,'unitAt_mul exists_kappa'),
  'Tracks x=r s x0 and y=rprime sprime y0 on the same frames; the four rational-stage EqAt premises are checked before invoking determinant units.'),
 claim('QD16','The same scalar is a unit at every good prime',
  'The scalar satisfying all literal JetKap jets is unique, so the empty-set choice equals each singleton-prime choice and satisfies actual exists_kappa.',['QD15','VI5'],
  ss(KAP,'selfDualLattice_intertwiner_baseVector_ne_zero applyAt0_monomial\' jetKap_unique exists_kappa')+
  ss(T+'ExistsUnitScalarFourier.lean','applyAt0_const_mul intertwining_mem_ne_zero')+ss(SPLIT,'JetKap'),
  'Uses one nonzero Taylor coefficient of the same entire Iop image and nonzero factorial/period/c0, rather than simultaneous independent scalar choices.'),
 claim('QD17','All literal movedVacuum_dict clauses on the original lattices',
  'The actual srcLat/tgtLat, unique scalar, moved vacuum, entire Iop image, orbit inclusion, exact EqAt readings and all jets satisfy movedVacuum_dict with zero additional Big thresholds.',['QD16','VI2','VI5','CW24'],
  ss(MOV,'movedVacuum_dict')+
  whole_decls(T+'LatticesSelfDualMovedPair.lean')+
  whole_decls(T+'VacuumVectorMovedPair.lean')+
  whole_decls(T+'LatticeOrbitVectorsMovedPair.lean')+
  whole_decls(T+'DifferentiableIntertwiningPair.lean')+
  whole_decls(T+'SrcLat.lean'),
  'Proves the actual geometric input by local duality and Hom generators, then assembles only the already proved clauses; chi reverses the two vertex lattices.'),
 claim('QD18','Sharp split-half quotient cardinality',
  'The opposite-half k-torsion quotient has n>0 terms with n=(product selected |O_Fv/k|)^(ab) dividing k^(f ab), where f=[F:Q].',['CW1'],
  ss(T+'ExistsHalfCosetRepresentativesCardDvd.lean','halfCoset_reps_card')+
  ss(T+'RelIndexNsmulIdempotentHalfAtSplitPlace.lean','relIndex_nsmul_half')+
  ss(T+'RelIndexNsmulHalfOrthogonalIdempotentSum.lean','kIdx_prod splitEquiv kIdx_half_sum relIndex_nsmul_half_sum')+
  ss(T+'ConjugateIdempotentChartPlacesInjective.lean','chart_places_injective')+
  ss(T+'ProdCardAdicCompletionIntegersQuotDvdPowFinrank.lean','prod_card_quot_natCast_dvd_pow_finrank'),
  'Keeps actual base-place injectivity and all ramification multiplicities; zero-rank, empty support and k=1 give n=1.'),
 claim('QD19','Actual normalized coset Fourier expansion with sharp denominators',
  'For the specified FinDatum, vec(d)=sum (zeta_i/n) U(w_i) v, k w_i in the old lattice, no infinite component, and zeta_i^(2k^2)=1. Coefficient l1 is one under every complex embedding.',['QD18','CA1','CW3'],
  ss(T+'HalfLatticeCharSumDetectsNsmulMultiple.lean','charSum_detects_multiple')+
  ss(T+'CosetDatumVectorFiniteHeisenbergCombination.lean','stdSelfDual pow_psi_eq_one model_coset GlobalTheory.RowEx.fourierVec')+
  ss(ST+'DictAt.lean','DictAt'),
  'Finite perfect pairing orthogonality determines the coefficients of the actual normalized half-Schwartz map. The exponent 2k^2 retains the half-symplectic factor.'),
 claim('QD20','Actual finite torsion translates give the same period jets',
  'A finite Heisenberg translate with k w in the old lattice has the exact moved period-jet expression kappa zeta U(s)G with k s in the same new lattice.',['QD17','CA1','WA15','CW24'],
  ss(HEIS,'applyAt0_scale core coreNeg qbar_of_root GlobalTheory.HeisTrans.main')+
  ss(T+'HeisenbergRootSmulFiniteRationalLatticeDecomp.lean','heisO_eq_root_smul_finRat')+
  ss(T+'DeltaOrthonormalCoordsMemLatticeOfFiniteRational.lean','coord_mem_RL mem_La_of_finRat')+
  ss(T+'HeisenbergTranslateFiniteRationalRealGaussian.lean','heisO_finRat_real')+
  ss(T+'EntireEqOfMonomialDerivationsAtZeroEq.lean','eq_of_applyAt0_monomial_eq')+
  ss(T+'IsSelfDualImageOrthonormalFrameLattice.lean','isSelfDualC_inV')+
  ss(T+'SelfDualLatticesDifferentiableOperator.lean','jetTab_heisO actO_nsmul jets_moved'),
  'Keeps rational approximation modulo the actual lattice, its sign epsilon, zeta^(2k)=1, the negative real coordinate X, s=delta X, exact sqrt(2 pi xiR) periods and chi conjugation.'),
 claim('QD21','Full quantitative DictAt identity and bounds',
  'The same lattices and kappa with r_i=oppQ(c_i) zeta_i and the actual translations satisfy every DictAt clause, including all-good-prime units, k^(f ab) integrality and all-conjugate l1<=1.',['QD17','QD19','QD20'],
  ss(DICT,'conjQ oppQ oppQ_coe opp_opp jetTab_comb differentiable_U dictAt_big')+
  ss(ST+'DictAt.lean','DictAt'),
  'Only finite sums are moved through actual entire derivatives; the two opp involutions on coefficients cancel exactly. In this uncollected presentation r_i=nu_i/n with nu_i^(2k^2)=1, a fixed cyclotomic coefficient field for the stated k.'),
 claim('QD22','Literal Big dictionary endpoint and precise remaining field boundary',
  'The original dictAt_big statement is reconstructed with zero additional thresholds, and its exact torsion/denominator/norm bounds; critical-ratio and original-embedding Choice fields remain separate.',['QD21','CW24','WA14','WA16'],
  ss(DICT,'dictAt_big')+ss(MOV,'movedVacuum_dict')+ss(T+'SelfDualLatticesDifferentiableOperator.lean','jets_moved')+
  ss(ST+'DictAt.lean','DictK'),
  'Finishing a finite dictionary does not assert a uniform number field for arbitrary infinitely many points or the missing critical toric ratios.')
]

target_specs=[
 (1,V+'ToricRatioConjugatesOfTransport.lean','toricRatioConjugates_of_transport',
  'Reconstruct actual twisted CM transport and the reference-twist critical toric-ratio conjugacy on the same arithmetic datum.',
  'QD closes the all-conjugate/local-unit theta dictionary; CW25 already supplies actual bottom data and NFBot. Neither supplies TwistedTransport or the critical L-value/reference-twist arithmetic. Retain these exact primitive inputs.',
  [(T+'NormalFormToricRatio.lean','ratio_algebraic'),(T+'NormalFormToricRatio.lean','nfRatio')],['QD22','CW25','WA19','TT18','TT19']),
 (1,T+'ExKeyOf.lean','exKey_of',
  'Complete the actual same-choice coefficient-field join at the prescribed original embedding, including the remaining critical-ratio field.',
  'The quantitative dictionary, normalized jets and bottom fields are reconstructed; the original embLL range/choice compatibility and critical toric ratios remain. An unrelated finite complex field, or finitely many pointwise algebraic dictionary scalars, is insufficient.',
  [(T+'ExFieldOfKeyFinExKey.lean','exField_of_keyFin_exKey'),(T+'TestChoicesExistLargeCoeffFieldAdelicData.lean','dat_choice_exists')],['QD22','WA14','WA16','CW25','TT19'])
]
targets=[]
for priority,path,name,objective,remaining,support,ids in target_specs:
 s=source(path,name,'retained_actual_primitive_supplier')
 targets.append(dict(priority=priority,path=path,declaration=s['declaration'],source=s,
  source_ranges=[s]+[source(p,n,'substantive_remaining_supplier') for p,n in support],
  objective=objective,remaining_human_scope=remaining,already_reconstructed=ids,
  supplied_conclusion_not_assumed_proved=True))

closed_specs=[
 (CHAR,'split_chars',['QD1','QD2'],'Actual split character values with all-complex-embedding modulus and local units away from support.'),
 (DET,'iop_pull_rat',['QD3','QD4','QD5','QD6','QD7'],'Actual rational positive-Iop pullback scalar, retaining all four EqAt premises.'),
 (RAT,'GlobalTheory.T.differentiable_theta_local_sum',['QD3','QD8'],'Actual rational finite-move jet substitution and arithmetic norms, using the compact character argument for the same action.'),
 (T+'IsOpenLevelGroupSubgroupOf.lean','GlobalTheory.T.standard_lattice_size_sum',['QD9'],'Root-of-unity JetKap base case on the actual global standard lattices.'),
 (T+'JetScalarIdempotentValue.lean','moved_split',['QD1','QD2','QD10','QD11','QD12'],'Exact split scalar with the positive factor removed only after independent arithmetic control.'),
 (T+'ExistsRationalFiniteTranslate.lean','exists_dec',['QD13','QD14','QD15'],'Actual definite-vertex decomposition and preservation of each protected prime; generic nondefinite extensions are not asserted.'),
 (KAP,'jetKap_unique',['QD16'],'Uniqueness on the same nonzero entire Iop image, all periods and c0 unchanged.'),
 (KAP,'exists_kappa',['QD1','QD2','QD3','QD4','QD5','QD6','QD7','QD8','QD9','QD10','QD11','QD12','QD13','QD14','QD15','QD16'],'Literal all-embedding and simultaneous local-unit conclusion under the original source input hypotheses.'),
 (MOV,'movedVacuum_dict',['QD17'],'Every literal moved-vacuum dictionary clause on actual source/target lattices and same frames, with zero additional thresholds.'),
 (T+'ExistsHalfCosetRepresentativesCardDvd.lean','halfCoset_reps_card',['QD18'],'Exact positive quotient cardinality dividing k^(f ab), with f=[F:Q].'),
 (T+'CosetDatumVectorFiniteHeisenbergCombination.lean','GlobalTheory.RowEx.fourierVec',['QD18','QD19'],'Actual normalized coset-vector expansion, sharp integrality and all-conjugate l1 bound.'),
 (HEIS,'GlobalTheory.HeisTrans.main',['QD20'],'Finite rational Heisenberg translate with root-of-unity scalar, same torsion level and exact period-scaled jets.'),
 (T+'SelfDualLatticesDifferentiableOperator.lean','jets_moved',['QD17','QD20'],'All actual translated-vacuum clauses using the same lattices and simultaneous scalar.'),
 (DICT,'dictAt_big',['QD21','QD22'],'Literal full quantitative dictionary endpoint under its original source hypotheses, including both zero extra thresholds.')
]
closed=[]
for path,name,ids,scope in closed_specs:
 s=source(path,name,'literal_completed_source_target')
 closed.append(dict(path=path,declaration=s['declaration'],closed_by=ids,source=s,
  scope=scope+' All explicit human-claim hypotheses remain.'))

optional=[dict(
 source=source(I+'MemNormGroupIffEverywhereNorm.lean','globalNormIndexTwo','optional_bypassed_source_route'),
 support=[source(I+'MemNormGroupIffEverywhereNorm.lean','existsUnique_isEta','optional_universal_character_uniqueness'),
  source(I+'ExistsUnramifiedHeckeCharHalfExponentRestrictQua.lean','exists_etaTilde','optional_universal_eta_record')],
 scope='Universal IsEta/IsEtaTilde uniqueness remains optional for this endpoint. QD2 tests supplied ResEta against HF9, QD8 classifies the actual compact vacuum character, and CW24 supplies the prescribed full action without this route.'),
 dict(source=source(AL+'ExistsRepSuppSplit.lean','exists_rep_suppSplit','optional_more_general_source_route'),
 scope='QD13--QD14 prove the actual definite-vertex instance needed here, with arbitrary finite protected prime set. A separate proof of the whole generic nondefinite source theorem is not claimed.')]

prior=HERE.parent/'history/version_0_21/provenance.json'
prior_obj=json.loads(prior.read_text()); prior_claims=prior_obj['claims']
old_ids=set(prior_claims) if isinstance(prior_claims,dict) else {c['id'] for c in prior_claims}
new_ids={c['id'] for c in claims}
assert not old_ids & new_ids,('prefix collision',old_ids & new_ids)
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

out=dict(schema_version='1.3',artifact_version='0.22',date='2026-11-22',component='quantitative_weil_dictionary',
 owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes without Unicode or newline normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False,new_prefix_unused_in_predecessor=True,
  new_dependency_graph_acyclic=True),
 status_definitions=dict(derived_simplification='Human proof under exact declared hypotheses, with substantive finite/arithmetic/analytic constructions and identified shorter routes.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,prior_components_reused=['VI','CA','WA','CW','HF','TT'],same_iteration_companions=[],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Actual all-complex-conjugate and all-good-prime local-unit scalar on the same moved vacuum',
  'Actual same-frame moved-vacuum dictionary, including self-dual lattices, orbit inclusion and all jets',
  'Actual finite coset Fourier expansion with denominator k^(f ab), f=[F:Q], and all-conjugate l1 at most one',
  'Exact k-torsion period translations and complete DictAt with zero additional Big thresholds'],
 scope_precision=[
  'Only a positive real residual factor is removed by distinguished complex norm equality.',
  'The generic finite quadratic Gauss argument includes dyadic groups and needs no both-ranks-even hypothesis.',
  'The positive-Iop composition proof asserts finite-order phase, not a newly reconstructed exact eighth-power bound.',
  'QD8 preserves the actual action and character; it does not need universal eta uniqueness.',
  'The approximation/decomposition closure is scoped to the actual definite vertices needed for DefPair.',
  'The finite quotient exponent is [F:Q], with all ramification multiplicities and no duplicate conjugate supports.',
  'The original supplied Choice.Is and source Hypotheses2/NormSum.Inp inputs remain explicit.',
  'Critical toric ratios and exact original-embedding Choice.FieldOK are not consequences of the dictionary.',
  'All predecessor component and pinned checkout bytes remain unchanged.'])

review_specs=[
 ('quantitative_weil_dictionary_independent_review.json','/root/class_rank',list(range(1,23)),
  'Independent arithmetic, positive-intertwiner phase, decomposition, finite dictionary and same-data scope review.'),
 ('quantitative_weil_dictionary_root_review.json','/root',list(range(1,23)),
  'Independent source and mathematical audit of the full QD chain.')
]
for filename,reviewer,indices,scope in review_specs:
 p=HERE.parent/'reviews_v0_22'/filename
 if not p.exists():continue
 raw=p.read_bytes();r=json.loads(raw);chosen={f'QD{i}':paragraphs[f'QD{i}'] for i in indices}
 reviewed=r.get('reviewed_claims',{})
 # A root review may deliberately cover a smaller named subset.
 if reviewer=='/root':chosen={k:v for k,v in chosen.items() if k in reviewed}
 assert chosen,('empty review scope',filename)
 for key,sha in chosen.items():
  actual=reviewed.get(key)
  if isinstance(actual,dict):actual=actual.get('proof_paragraph_sha256',actual.get('paragraph_sha256',actual.get('sha256')))
  assert actual==sha,('review paragraph changed',filename,key,sha,actual)
 verdict=r.get('verdict',r.get('result',r.get('status','')))
 assert str(verdict).upper().startswith('PASS'),('review not PASS',filename,verdict)
 out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
  review_record='../reviews_v0_22/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
  paragraph_range='Named QD paragraph through immediately before next paragraph; EOF for QD22.',lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
 loc += [f"{c['id']} | {c['title']} | {c['status']}",c['statement'],f"  proof_paragraph_sha256: {paragraphs[c['id']]}" ]
 for s in c['sources']:
  loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
   f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
 loc += ['']
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.22',commit=PIN,targets=targets,
 closed_source_targets=closed,conditionally_reconstructed_targets=[],retained_inputs=common,
 optional_not_required=optional,
 remaining_boundary='The three actual quantitative dictionary endpoints are reconstructed under their exact original supplied-choice/source hypotheses. Critical toric-ratio arithmetic and original-embedding Choice compatibility remain. Universal eta uniqueness and the full generic nondefinite approximation source route are not asserted.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 distinct_claim_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 claim_source_files=len({s['path'] for c in claims for s in c['sources']}),source_files=len(files),next_targets=len(targets),
 closed_endpoints=len(closed),independent_reviews=len(out['independent_reviews'])),indent=2))

