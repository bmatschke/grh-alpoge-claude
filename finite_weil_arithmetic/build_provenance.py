#!/usr/bin/env python3
"""Reproduce the WA source ledger from immutable Lean bytes, without a build.

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
AL = D + 'Proofs/AdelicLatticeProofs/'
IE = D + 'Proofs/InertiaEigenvalues/'
DE = D + 'Proofs/DecoratedLatticeProofs/'
UE = D + 'Proofs/UnitaryExistence/'
DT = D + 'Definitions/TwistedInnerProducts/'
DW = D + 'Definitions/ExistenceOfLattices/'
FORM = 'src/Formalism/LocalToGlobal/IndefiniteReal/LocalNewformFunction.lean'
TIED = 'src/Formalism/LocalToGlobal/BesselHermitianTheta/TiedWeil.lean'
SD = AL + 'SelfDualLatticePairingDual.lean'
WAVE = T + 'ThetaKernelAlgebraicExpansion.lean'
PAIR = T + 'VacuumSelfDualLattices.lean'
PROJ = T + 'WeilDatumFinitePairVacuumAlgebraicCombination.lean'
LEV = T + 'VacuumValueAlgebraicCongruence.lean'
FORMINV = IE + 'ExistsConjHalfInvariantFormIdemSumVacuumNeZero.lean'
FORMALG = T + 'ExistsAlgebraicInvariantFormVacuumSplitPlace.lean'
CH = T + 'HeckeCharFiniteIdelesIsAlgebraicOfResEta.lean'
SPAN = T + 'MemGfCOfSuppAt.lean'
GEN = T + 'FiniteUnitaryPointsMemOfLevelAndSplitPlace.lean'
SND = T + 'FiniteDatumIsAlgebraicCombinationDefiniteBottom.lean'
JET = T + 'NormalisedDefiniteKernelEntriesIsAlgebraic.lean'
NFJET = T + 'NormalFormJets.lean'
PER = T + 'PeriodAlgebraicFixedDegree.lean'
BOT = T + 'BottomTrianglePeriodAlgebraic.lean'
NFBOT = T + 'NormalFormBottom.lean'
BOTEX = T + 'BottomExistsIntegrable.lean'
TWIST = V + 'ExistsWeilDatumTwistHeckeCharacters.lean'
EXWEIL = V + 'ExistsWeilDatumOfSplittingCharacters.lean'
ETAWEIL = V + 'ExistsWeilDatumPowersUnramifiedEtaTilde.lean'
NUM = DT + 'MemHalfCosetSelf.lean'
AGREE = DT + 'TwistPlacesOffPrimeQZero.lean'
CHOICE = DT + 'ExistsMatchOver.lean'

common = [
 'The exact arithmetic CM host D, standard sign-minus-one additive character, actual infinity embeddings and the host trace-dual fractional ideal AA are fixed.',
 'For the generic finite-Weil theorem: actual IsVacO, self-dual full lattices, specified Cartan involutions, and actual IsWeilDatumO with its exact splitting characters, continuity, unitarity and positive split normalization are supplied.',
 'The theta pairing and finite Heisenberg operators use the original symplO and symplOH, including the half factor and host.AA lattice multiplier.',
 'Finite-dimensional algebra, local-field topology, finite Fourier orthogonality, ideal-class finiteness and the explicitly explained positive-theta Fourier recurrence are used.',
 'No arbitrary field embedding is interchanged with a limit, derivative, integral or Fourier series.',
 'These human proofs are not formally replayed; no Lean build, source mutation, PDF or complete RH/GRH conclusion is asserted.'
]
main_raw=(HERE/'main.tex').read_bytes()
paragraphs,proof_locs={},{}
for n in range(1,20):
 start=main_raw.index(f'\\paragraph{{WA{n}:'.encode())
 stop=main_raw.index(f'\\paragraph{{WA{n+1}:'.encode(),start+1) if n<19 else len(main_raw)
 key=f'WA{n}';paragraphs[key]=digest(main_raw[start:stop])
 proof_locs[key]=dict(file='main.tex',anchors=[key],sha256=paragraphs[key],
  line_start=main_raw[:start].count(b'\n')+1,line_end=main_raw[:stop].count(b'\n'),bytes=stop-start)

def claim(i,title,statement,deps,srcs,relation,assumptions=(),status='derived_simplification'):
 return dict(id=i,title=title,status=status,statement=statement,introduced_in='0.20',depends_on=deps,
  assumptions=common+list(assumptions),proof_location=proof_locs[i],proof_paragraph_sha256=paragraphs[i],
  expanded_notes=dict(file='report.txt',section=i),source_relation=relation,
  mathematical_status=('conditional_reduction_with_explicit_remaining_primitive_inputs' if status=='conditional_reduction'
    else 'proved_under_exact_declared_hypotheses'),sources=srcs)

claims=[
 claim('WA1','Exact finite Heisenberg phases and the actual algebraic span',
  'With the original host.AA-times-Hom lattice, finite Heisenberg phases are roots of unity and the finite algebraic translate span is Heisenberg-stable; the literal lattice-vacuum clauses determine signs on every lattice vector.',['VI2'],
  ss(FORM,'latO IsLatVac IsVacuum IsVacO heisO symplO symplOH')+
  ss('src/Formalism/LocalToGlobal/IndefiniteReal/FinitePlaces/GlobalDualOfBasis.lean','xi_AA_AAbar')+
  ss(SD,'char_sympl_eq_one le_of_two_of_half heisO_heisO latO_selfDual_approx_sign')+
  ss(WAVE,'nsmul_finite psi_mem psiH_mem')+
  ss(T+'HeisOSumSmul.lean','IsAlgComb IsAlgComb.Heisenberg₂'),
  'Integer denominator clearing gives finite-order phases. The source host dyadic splitting and 2*Lambda generate the literal sign law; no plain-Hom or odd-residue simplification is made.'),
 claim('WA2','Algebraic theta pairings and actual scalar rigidity',
  'All theta pairings of algebraic finite translates are algebraic, and a scalar relating two nonzero such vectors is algebraic.',['WA1'],
  ss(PAIR,'vac_translate translates thetaIP_algComb')+ss(SPAN,'vac_ne_zero rigid star_mem')+
  ss(IE+'SchurFiniteHeisenbergFockVacuumThetaFunctions.lean','thetaInner_heisenberg thetaInner_re_pos'),
  'Uses exact lattice/off-lattice character orthogonality, normalized norm and positivity; recovers the scalar by an inner-product quotient.'),
 claim('WA3','Finite algebraic projective model of a moved vacuum',
  'For each actual finite pair, omega(g)v=kappa F with F a nonzero algebraic finite Heisenberg combination and kappa nonzero, without yet asserting kappa algebraic.',['WA1','WA2','VI6'],
  ss(PROJ,'exists_level average om_vac_algComb')+ss(LEV,'vac_eq_smul')+
  ss(IE+'SchurFiniteHeisenbergFockVacuumThetaFunctions.lean','fd_vacSub irr_vac')+
  ss(T+'WeilFinitePointPreservesFockVacuum.lean','om_fin_fockVac')+
  ss(DE+'IsPolynomialFockThetaVectorWeilOperatorCartan.lean','om_annih')+
  ss(V+'CompletedHomLatticeFinitelyGenerated.lean','latO_finitely_generated')+
  ss(V+'CompletedHomLatticeMultipleMemOpenLevel.lean','level_of_generators'),
  'Replaces signed averaging plus irreducibility by explicit finite character eigenspaces and Qbar row reduction. Proves one-dimensionality by the positive theta Fourier recurrence; L2 covariance justifies moving derivatives through the actual isometry.'),
 claim('WA4','A principal finite congruence fixes the actual vacuum',
  'One positive integer level fixes the given unit vacuum exactly for every simultaneous finite pair in that level.',['WA1','WA3'],
  ss(LEV,'exists_level_frame om_pow_eq exists_level_fix level_vac_alg')+
  ss(T+'CongruentPairsFixVacuumWeilDatum.lean','pair_fix_vacO')+
  ss(DW+'CoeSelfDualLatticeInFrameCoordinatesEq.lean','FinCong')+
  ss(FORM,'IsWeilDatumO'),
  'A continuous character of the compact profinite lattice stabilizer has finite image and open kernel; this replaces the source no-small-subgroup power contradiction while retaining the exact vector.'),
 claim('WA5','A nonzero invariant split-half functional',
  'For the actual split idempotent, there exists a complex linear functional equal to one on v and invariant under the conjugate-half Heisenberg action on every theta function.',['WA1'],
  ss(FORMINV,'heisL_commute_of dual_half count_form invariant_form'),
  'Two explicit commuting-operator separation arguments construct the counting functional and show v survives the coinvariant quotient; the functional need not be continuous.'),
 claim('WA6','Algebraic refinement of the invariant functional',
  'The split-invariant functional can be chosen algebraic on any specified finite list of finite Heisenberg translates of v.',['WA1','WA5'],
  ss(FORMALG,'exists_alg_form')+ss(FORMINV,'dual_half'),
  'The e/bar-e/complement decomposition gives the integral case. A nonzero-denominator linear filter kills one remaining value and multiplies previous values by algebraic factors; finite induction supplies the exact quantifiers.'),
 claim('WA7','Algebraic finite values of actual splitting characters',
  'Every raw splitting Hecke-character value at an idele with identity infinity component is algebraic, without asserting all such values generate one number field.',[],
  ss(CH,'isAlgebraic_unit_zpow exists_pow_mul_int exists_decomp char_eq_prod isAlgebraic_of_infPart_eq_one finite_values_isAlgebraic')+
  ss(T+'SplittingHeckeCharExistsArchimedeanExponent.lean','exists_zpow_of_trivial exists_hasInfExp')+
  ss(AL+'ContinuousCharacterFiniteOrderIntegralUnits.lean','char_finUnit_finite_order'),
  'Integral circle infinity exponents, finite unit image and ideal-class principalization prove pointwise algebraicity. Normalized ValuesIn norm powers remain distinct.'),
 claim('WA8','The exact split normalization determines algebraic phase',
  'Every actual split-supported pair sends the vacuum into its algebraic Heisenberg span.',['WA2','WA3','WA6','WA7'],
  ss(SPAN,'mem_GfC_of_suppAt split_alg')+ss(FORM,'splitFacO IsWeilDatumO')+
  ss(TIED,'IsDetRoot IsSplitIdem SuppAt IsDetAt'),
  'Uses the actual crossed character factor and positive real scalar: kappa*a=r*z and r^2=|kappa|^2|a|^2. This fixes phase rather than inferring algebraicity from unitarity.'),
 claim('WA9','Algebraic action forms a subgroup closed under positive roots',
  'Finite pairs preserving the vacuum algebraic span form a subgroup, and if a positive power belongs then the pair itself belongs.',['WA1','WA2','WA3','WA4','WA8'],
  ss(SPAN,'om_scaled om_alg om_ne_zero root_closed algGroup'),
  'Covariance gives omega(g)A subset kappa A; exact vector rigidity proves inverse and power closure, with invertibility checking all nonzero factors.'),
 claim('WA10','Local quasi-reflections give the full finite group',
  'A finite-unitary subgroup containing a principal congruence and every split-supported element, and closed under positive roots, contains every finite unitary point.',[],
  ss(GEN,'exists_pow_sub_one exists_unit_pow_congr_one finCong_of_eq_one_add mt_pow_rfA mem_refl mem_of_level_of_split')+
  ss(AL+'ExistsQuasiReflectionProdMulVecEq.lean','refl_mulVec exists_refl exists_refl_prod_mulVec_eq')+
  ss(AL+'UnitaryMatrixEqProdQuasiReflections.lean','exists_fix isUnE_eq_prod_refl')+
  ss(AL+'UnitaryQuasiReflectionLaws.lean','refl_laws')+
  ss(DW+'CoeSelfDualLatticeInFrameCoordinatesEq.lean','FinCong'),
  'A new local proof replaces source rational/split approximation: nonsplit unitary groups are generated by quasi-reflections, norm-one eigenvalues have arbitrarily congruent positive powers, and only finitely many local factors are outside the given level. Explicitly valid at dyadic and ramified places; no prime distribution used.'),
 claim('WA11','Actual finite Weil operators preserve the algebraic span',
  'Every actual finite pair satisfies BotExpand.om_vac_algComb and preserves the same algebraic Heisenberg span, proving moved_translate_algComb qualitatively.',['WA4','WA8','WA9','WA10'],
  ss(SPAN,'source_mem target_mem om_vac_algComb')+
  ss(T+'HeisOSumSmul.lean','om_algComb')+
  ss(T+'FiniteAdelicAlgebraicExpansion.lean','moved_translate_algComb'),
  'Applies WA10 separately to source and target preimages of WA9 subgroup. The actual representation is supplied; no FunPr or universal NormSum premise is used by this generic proof.'),
 claim('WA12','Both actual bottom finite data have algebraic expansions',
  'The first and second standard bottom theta vectors, and all their finite Weil moves, are finite algebraic combinations of finite translates of their respective actual vacua.',['WA1','WA7','WA11'],
  ss(WAVE,'ind_nsmul_mem mem_of_finite_cosets mem_algSpan stdFst_mem finDatum_eq_sum_heis')+
  ss(SND,'unitChar_mem stdSnd_mem isAlgComb_of_isThetaAt finDatum\'_isAlgComb')+
  ss(SPAN,'ker\'_eq_sum_jets')+
  ss(FORM,'IsSBHalf IsThetaAt')+
  ss(DE+'HeisenbergCombinationCommFockPolynomialVectors.lean','heis_comb_pureTensorO'),
  'Finite support/period quotients and finite Fourier orthogonality yield actual waves; the same theta map carries the basic indicator to the actual vacuum. Second-side conjugate idempotent and character remain exact.'),
 claim('WA13','Actual normalized grid jet entries are algebraic',
  'The literal normalized kk matrices of the original Choice are algebraic with the same c0, delta, half-point, rational frame and period powers.',['WA11','WA12','TT9','TT12','TT13','TA10','VI9','VI10'],
  ss(JET,'coefIn_dict applyAt0_monomial_mem opp_isAlgebraic kk_isAlgebraic')+
  ss(T+'FrameGramUnitaryIdentity.lean','fock_jets_heisO_fin')+
  ss(T+'FiniteHeisenbergTranslateSelfDualVacuumFockJets.lean','core coreNeg main'),
  'WA11 discharges TT13 equation TT.19. The direct rational-translate germ calculation and homogeneous normalizing scalar cancel the original period and unit factors, bypassing stronger arbitrary-function translate closure.'),
 claim('WA14','The actual NFJet field exists',
  'Every fixed Choice has a finite number field satisfying the literal JetCl and NFJet, with no new size threshold.',['WA13','TT6','TT7','TT8','TT14'],
  ss(NFJET,'dset jetCl_of_choice nfJet_holds')+
  ss(T+'FinitePureDataOfCosetIndicatorExpansionsDepth.lean','mem_support_of finite_pureDat_of_depth')+
  ss(NUM,'JetsIn expDepth')+ss(AGREE,'JetCl NFJet'),
  'Uses fixed-depth support uniqueness to control all expansions, then finite adjunction of WA13 entries. No bound on the degree or denominators is inferred.'),
 claim('WA15','Exact fixed-degree periods for both actual bottom vacua',
  'For a literal bottom triangle, all finite-point monomial kernels of a fixed place degree become algebraic after division by one nonzero period per source side.',['WA3','WA12','TT13','TA10','VI9','VI10'],
  ss(PER,'conj_isAlgebraic applyAt0_isAlgebraic jet_negSp_heis std_eq_colLat_one even_bot jets_div_period_isAlgebraic')+
  ss(BOT,'ker_algebraic')+
  ss(T+'BottomTriangleDualPeriodAlgebraic.lean','classSums\'_algebraic')+
  ss(V+'FockJetsUnitVacuumEqUnitMulPeriodJets.lean','fock_jets_eq_unit_mul_period_jets'),
  'Includes the unknown actual nonzero comparison scalar in the period and conjugates the full negative-source expression. Uses exact even target rank/product parity, without claiming both source ranks even.'),
 claim('WA16','Actual definite period fields for supplied bottom triangles',
  'For every supplied literal IsBottomTri, a finite number field and two nonzero actual periods satisfy SumsIn; TT16 finite-Weil premise is discharged.',['WA4','WA12','WA15','TT15','TT16','CR3'],
  ss(T+'ExistsWeightedAverageHaar.lean','level_all integral_eq_classSum_bottom')+
  ss(T+'ExistsFourierDegreeBound.lean','avg_kernel_alg')+
  ss(BOT,'classSums_algebraic')+
  ss(T+'BottomTriangleDualPeriodAlgebraic.lean','classSums\'_algebraic')+
  ss(T+'BottomTriangleAlgebraicityFiniteData.lean','span_classSums')+
  ss(T+'BottomTriangleDualAlgebraicityFiniteData.lean','span_classSums\'')+
  ss(NFBOT,'field_of_gens sumsIn_bottom sumsIn_mono')+ss(NUM,'SumsIn'),
  'Retains the original positive Haar-volume factor and separate source periods. Rational invariance, finite classes, finite degree support and finite adjunction supply one field rather than only pointwise algebraicity.'),
 claim('WA17','Standard bottom geometry and the exact full-Weil boundary',
  'Standard spaces, self-dual lattices, identity frames and parity-adjusted characters produce literal bottom triangles once the two specified additional full oriented Weil data are supplied; WA16 then gives conditional NFBot.',['WA15','WA16'],
  ss(BOTEX,"exists_stdRig bottom_chars isSelfDualC_neg' exists_bottomTri")+
  ss(T+'RatInOfDefinite.lean','exists_expAt exists_meas exists_isWeil')+
  ss(NFBOT,'nfBot_holds')+ss(NUM,'IsBottomTri BottomIn')+
  ss(AGREE,'BotCl NFBot'),
  'Constructs the actual standard lattice and character inputs and identifies every join, retaining the new full representation existence rather than reusing the grid representation on different spaces.',
  ['Full oriented Weil data for the two new bottom pairs with the displayed exact characters remain supplied.'],'conditional_reduction'),
 claim('WA18','Explicit determinant-root adjustment of splitting characters',
  'A full Weil datum with the same eta-rank-power characters gives one for the prescribed rank-restricted characters by the exact crossed determinant-root twist.',['WA17'],
  ss(TWIST,'triv_of_resEta_zero exists_weilDatum_twist')+
  ss(UE+'ExistsUnitaryAdelicCharOfHeckeChar.lean','exists_muVal')+
  ss(UE+'ExistsRootNearOne.lean','exists_root_near_one')+
  ss(EXWEIL,'isHeckeChar_div_pow resEta_div_pow exists_isWeilDatumO')+
  ss(TIED,'IsDetRoot')+ss(FORM,'IsWeilDatumO splitFacO'),
  'Hilbert 90 roots define continuous characters independent of the root because quotient characters are trivial on F ideles. Checks all eleven Weil clauses, especially the exact split phase and unchanged positive multiplier.',
  ['The same-space canonical full oriented Weil datum for eta^rank is supplied; its finite/real construction and rational automorphy remain primitive targets.'],'conditional_reduction'),
 claim('WA19','Same-choice field consequence and remaining critical ratios',
  'The new jet and supplied-bottom fields join with the earlier elementary fields on the same realization; critical ratio algebraicity and the actual embLL/Choice compatibility remain explicit.',['WA14','WA16','WA17','WA18','TT11','TT19','HF16'],
  ss(T+'RangeAlgebraMapMono.lean','jetCl_mono botCl_mono InNF.and nfAll_of')+
  ss(NUM,'NumbersIn NumbersIn.mono FieldIn FieldOK HasNumberField')+
  ss(AGREE,'AllIn LAgree GAgree WAgree SAgree Agree FlipAgree')+
  ss(CHOICE,'Choice RealOK IsBase Is'),
  'Updates TT19 using actual new arithmetic endpoints, without inferring critical L-ratios from finite Heisenberg coefficients or embedding an independent number field into the original embLL.',
  ['Critical ToricRatioConjugates with its actual CM field data and reference twist remain supplied.',
   'A literal same-object embedding/choice transport, or inclusion of the fields in the original embLL, remains required.'],'conditional_reduction')
]

target_specs=[
 (1,T+'ExistsUnitModulusScalarLocal.lean','exists_kappa',
  'Prove the quantitative arithmetic of the prescribed moving-vacuum scalar: all-embedding unit modulus, selected local-unit conditions and the associated dictionary bounds.',
  'The narrower finite algebraic Heisenberg-span assertion and qualitative normalized jets are now proved by WA11--WA14. Do not retain these completed qualitative assertions as missing premises. Full DictAt norm, denominator, all-embedding and prescribed-place-unit estimates are not proved.',
  [(T+'ExistsLatticesEntireIntertwining.lean','movedVacuum_dict'),(T+'DictionarySizeBound.lean','dictAt_big')],['WA11','WA13','WA14']),
 (1,ETAWEIL,'exists_weilDatum_etaTilde',
  'Construct the canonical full same-space oriented Weil datum with eta-rank-power characters, including both finite and real actions and rational theta-distribution automorphy.',
  'WA17 constructs the standard bottom lattice/character geometry. WA18 proves the exact determinant-root character adjustment, so this canonical full existence is sufficient for all required new bottom pairs. The grid representation on different spaces is not a witness. WA11 proves arithmetic only for a supplied actual representation.',
  [(V+'ExistsIsFinWeil.lean','exists_isFinWeil'),(V+'LintegralEqOfNorms.lean','exists_isInfWeil'),
   (V+'ThetaDistributionInvariantRationalTarget.lean','automorphy_target'),
   (V+'ThetaDistributionAutomorphySourceGroup.lean','automorphy_source')],['WA17','WA18']),
 (1,V+'ToricRatioConjugatesOfTransport.lean','toricRatioConjugates_of_transport',
  'Supply the actual twisted CM transport and critical toric-ratio conjugacy, then the finite field of critical L-value ratios for the same reference twist.',
  'WA11--WA16 concern finite Weil coefficients, normalized jets and supplied definite bottom periods. They do not prove critical L-value algebraicity. The actual TwistedTransport and CM field-data requirements remain.',
  [(T+'NormalFormToricRatio.lean','ratio_algebraic'),(T+'NormalFormToricRatio.lean','nfRatio')],['WA19','TT18','TT19']),
 (1,T+'ExKeyOf.lean','exKey_of',
  'Complete the literal compatible field/choice construction, with the coefficient field in the original embLL and all required same-object transport and real matching clauses.',
  'The jet field is now supplied by WA14; SumsIn is supplied by WA16 for every actual bottom triangle. Canonical new bottom Weil existence and critical ratio fields remain as separately indexed. Independent complex subfields or isomorphic choices do not establish FieldOK for the given Choice.',
  [(T+'ExFieldOfKeyFinExKey.lean','exField_of_keyFin_exKey'),
   (T+'TestChoicesExistLargeCoeffFieldAdelicData.lean','dat_choice_exists')],['WA14','WA16','WA19','TT19'])
]
targets=[]
for priority,path,name,objective,remaining,support,ids in target_specs:
 s=source(path,name,'retained_actual_primitive_supplier')
 targets.append(dict(priority=priority,path=path,declaration=s['declaration'],source=s,
  source_ranges=[s]+[source(p,n,'substantive_remaining_supplier') for p,n in support],
  objective=objective,remaining_human_scope=remaining,already_reconstructed=ids,
  supplied_conclusion_not_assumed_proved=True))

closed_specs=[
 (PROJ,'om_vac_algComb',['WA3'],'Projective expansion only; no algebraicity of its unspecified scalar is inferred here.'),
 (LEV,'exists_level_fix',['WA4'],'The actual vacuum is fixed by one principal finite congruence.'),
 (FORMINV,'invariant_form',['WA5'],'A nonzero split-half coinvariant functional, without continuity.'),
 (FORMALG,'exists_alg_form',['WA5','WA6'],'Exact finite-list algebraicity of an actual normalized invariant functional.'),
 (CH,'isAlgebraic_of_infPart_eq_one',['WA7'],'Pointwise algebraic finite-idelic values, not a uniform field of raw half-normalized values.'),
 (SPAN,'split_alg',['WA8'],'The actual split scalar is algebraic using the positive split law and theta norm.'),
 (GEN,'mem_of_level_of_split',['WA10'],'Exact source group conclusion by the shorter local quasi-reflection proof.'),
 (SPAN,'om_vac_algComb',['WA1','WA2','WA3','WA4','WA5','WA6','WA7','WA8','WA9','WA10','WA11'],'The actual generic finite-Weil arithmetic on the same supplied vacuum.'),
 (T+'FiniteAdelicAlgebraicExpansion.lean','moved_translate_algComb',['WA11'],'Qualitative algebraic expansion for actual finite moves of finite translates.'),
 (WAVE,'finDatum_eq_sum_heis',['WA12'],'Actual first finite datum expansion.'),
 (SND,'finDatum\'_isAlgComb',['WA12'],'Actual second finite datum expansion with its own conjugate idempotent.'),
 (SPAN,'ker\'_eq_sum_jets',['WA12'],'Actual second kernel finite algebraic translate-jet expansion.'),
 (JET,'kk_isAlgebraic',['WA13'],'Qualitative normalized kk arithmetic; quantitative DictAt not asserted.'),
 (NFJET,'nfJet_holds',['WA14'],'Actual normalized jet field for all expansions with no new size threshold.'),
 (PER,'jets_div_period_isAlgebraic',['WA15'],'One period for each fixed degree including the actual nonzero comparison scalar.'),
 (BOT,'ker_algebraic',['WA15'],'Actual finite-point kernel arithmetic after division by that period.'),
 (BOT,'classSums_algebraic',['WA16'],'Common actual Haar-volume period for all monomial definite integrals.'),
 (T+'BottomTriangleDualPeriodAlgebraic.lean','classSums\'_algebraic',['WA16'],'Corresponding dual-source period, separately normalized.'),
 (NFBOT,'sumsIn_bottom',['WA16'],'Actual SumsIn for a supplied literal bottom triangle.'),
 (TWIST,'exists_weilDatum_twist',['WA18'],'Actual character-adjustment implication from a supplied same-space full datum.')
]
closed=[]
for path,name,ids,scope in closed_specs:
 s=source(path,name,'literal_completed_source_target')
 closed.append(dict(path=path,declaration=s['declaration'],closed_by=ids,source=s,
  scope=scope+' The exact hypotheses of the named paragraphs remain explicit.'))

conditional=[
 dict(source=source(BOTEX,'exists_bottomTri','conditionally_reconstructed_bottom_existence'),
  reconstructed_by=['WA17','WA18'],retained=['Canonical same-space eta-rank-power full oriented Weil existence'],
  scope='Actual standard spaces, self-dual lattices, ranks, parity characters, conductor/measure joins and character twisting are reconstructed.'),
 dict(source=source(NFBOT,'nfBot_holds','conditionally_reconstructed_uniform_bottom_field'),
  reconstructed_by=['WA16','WA17','WA18'],retained=['The same new canonical full Weil existence'],
  scope='SumsIn no longer retains a finite-Weil arithmetic premise; finite compositum over squares is explicit.'),
 dict(source=source(EXWEIL,'exists_isWeilDatumO','conditionally_reconstructed_full_existence_join'),
  reconstructed_by=['WA18'],retained=['exists_weilDatum_etaTilde on the same actual spaces'],
  scope='The quotient-character and determinant-root adjustment is proved, not the canonical representation itself.'),
 dict(source=source(T+'RangeAlgebraMapMono.lean','nfAll_of','conditionally_reconstructed_full_field_join'),
  reconstructed_by=['WA14','WA16','WA19','TT11','TT19'],
  retained=['Canonical new full bottom Weil existence','Critical L-ratio algebraicity','Actual compatible embedding/choice join'],
  scope='Jet arithmetic and finite-Weil bottom arithmetic are discharged; all remaining source inputs are separately named.')
]

record_audits=[]
for path,name,expected,all_constructed,support in [
 (FORM,'IsWeilDatumO',['std','hecS','hecT','resS','resT','om_pres','om_heis','om_aut','om_cont','om_unit','om_split'],False,
  'Input for WA1--WA16; all clauses transported explicitly in WA18 from the supplied canonical datum.'),
 (FORM,'IsVacuum',['inf','theta','lat','fock','norm'],False,
  'Actual supplied vacuum input, with exact lattice law expanded in WA1 and nonzero norm used in WA2.'),
 (NUM,'NumbersIn',['chars','eighth','roots','phases','sqrt','jets','ratios','bottom'],False,
  'TT11 supplies elementary fields, WA14 jets, WA16 supplied-bottom fields; critical ratios and actual bottom existence remain explicit.')
]:
 s=source(path,name,'literal_record_field_inventory')
 rows=read_source(path)[1][s['line_start']-1:s['line_end']]
 names=[m.group(1) for line in rows[1:] if (m:=re.match(r'^  ([^\s:]+)\s*:',line))]
 assert names==expected,(name,names,expected)
 record_audits.append(dict(record=s['declaration'],source=s,field_count=len(names),
  all_fields_constructed=all_constructed,fields=[dict(name=f,supplied_by=support) for f in names]))

out=dict(schema_version='1.3',artifact_version='0.20',date='2026-11-22',component='finite_weil_arithmetic',
 owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes without Unicode or newline normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Human proof under exact declared hypotheses, possibly using an explicitly proved shorter argument.',
  conditional_reduction='Actual implication proved; the identified primitive supplier remains supplied.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,record_audits=record_audits,
 prior_components_reused=['VI','TA','TT','CR','HF'],same_iteration_companions=[],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Actual generic finite-Weil arithmetic on the same unit vacuum, including the split phase',
  'Exact finite-data algebraic expansions on both bottom sides',
  'Actual normalized kk algebraicity and NFJet for the original Choice',
  'Actual common normalized period and SumsIn field for every supplied bottom triangle',
  'Explicit determinant-root adjustment reducing new full Weil existence to the canonical eta-rank-power case'],
 scope_precision=[
  'The finite Heisenberg lattice includes host.AA; the half-pairing and dyadic splitting signs are retained.',
  'The generic IsWeilDatumO is a supplied actual representation, not constructed by the arithmetic proof.',
  'No arbitrary complex unit is declared algebraic merely from its norm.',
  'WA10 is a proved local replacement argument; it is not a formal application of number-field Lean lemmas to completions.',
  'No quantitative DictAt all-embedding modulus, prescribed local-unit or denominator bound is claimed.',
  'Bottom periods include the actual positive Haar volume and the possibly nonalgebraic nonzero comparison scalar.',
  'New full bottom representations and critical ratio algebraicity remain distinct from qualitative finite Weil arithmetic.',
  'A field inside C is not automatically inside the original embLL; actual same-choice compatibility remains explicit.',
  'All predecessor component and pinned checkout bytes are preserved.'])

review_specs=[
 ('adic_reviews_finite_weil_arithmetic.txt','/root/class_rank',list(range(1,20)),
  'Independent full WA mathematical/source-interface review including phase, power closure, local generation and same-data arithmetic joins.'),
 ('root_reviews_finite_weil_arithmetic.txt','/root',list(range(1,20)),
  'Independent full WA mathematical and pinned-source review.')
]
for filename,reviewer,indices,scope in review_specs:
 p=HERE.parent/'reviews_v0_20'/filename
 if not p.exists():continue
 raw=p.read_bytes();content=raw.decode()
 chosen={f'WA{i}':paragraphs[f'WA{i}'] for i in indices}
 for key,sha in chosen.items():assert sha in content,('review paragraph changed',filename,key,sha)
 out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
  review_record='../reviews_v0_20/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
  paragraph_range='Named WA paragraph through immediately before next paragraph; EOF for WA19.',lean_replay=False))
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
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.20',commit=PIN,targets=targets,
 closed_source_targets=closed,conditionally_reconstructed_targets=conditional,retained_inputs=common,
 optional_not_required=[
  'The stronger general CoefInTranslate theorem is not needed by the direct rational-translate argument.',
  'The source rational/split/congruence factorization is bypassed by WA10; it is not a new mandatory arithmetic target.'
 ],
 remaining_boundary='Qualitative actual finite-Weil arithmetic, NFJet and supplied-bottom SumsIn are proved. Quantitative dictionary arithmetic, canonical new full bottom Weil existence, critical toric L-ratios and exact compatible field/choice construction remain narrowly scoped.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 distinct_claim_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 claim_source_files=len({s['path'] for c in claims for s in c['sources']}),source_files=len(files),next_targets=len(targets),
 independent_reviews=len(out['independent_reviews'])),indent=2))


