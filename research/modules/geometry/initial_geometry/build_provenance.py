#!/usr/bin/env python3
"""Reproduce the IG source ledger from immutable Lean bytes, without a build.

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

common = [
 'The pinned arithmetic and geometric definitions, including the actual host involution, integral norm factors, coordinate frames, mass and volume definitions, are retained.',
 'Standard elementary complex analysis, Gaussian Fourier transform, ideal factorization, finite-group duality, and the named previously reconstructed claims are used as explained in main.tex; no prime-in-short-interval theorem is assumed.',
 'The qualitative initial existence construction does not construct arbitrary large-scale ChGood data or supply LevelPrime, a full HFrame, or V4.Core.',
 'No Lean compilation, kernel replay, replacement formalization, PDF, RH or GRH proof is asserted.'
]

main_raw = (HERE / 'main.tex').read_bytes()
paragraphs, proof_locs = {}, {}
for i in range(1, 15):
    start = main_raw.index(f'\\paragraph{{IG{i}:'.encode())
    stop = main_raw.index(f'\\paragraph{{IG{i+1}:'.encode(), start + 1) if i < 14 else len(main_raw)
    paragraphs[f'IG{i}'] = digest(main_raw[start:stop])
    proof_locs[f'IG{i}'] = dict(file='main.tex', anchors=[f'IG{i}'], sha256=paragraphs[f'IG{i}'],
        line_start=main_raw[:start].count(b'\n') + 1, line_end=main_raw[:stop].count(b'\n'), bytes=stop-start)

def claim(i, title, statement, deps, srcs, relation, assumptions=(), status='derived_simplification'):
    return dict(id=i, title=title, status=status, statement=statement,
        introduced_in='0.18', depends_on=deps, assumptions=common + list(assumptions),
        proof_location=proof_locs[i], expanded_notes=dict(file='report.txt', section=i),
        source_relation=relation,
        mathematical_status=('conditional_reduction_with_explicit_remaining_primitive_inputs'
          if status == 'conditional_reduction' else 'proved_under_exact_declared_hypotheses'), sources=srcs)

ray = A + 'NonemptyRayDataOfNeZero.lean'
epstein = I + 'LatticeEpsteinZetaContinuation.lean'
partial = I + 'RayClassPartialZetaContinuation.lean'
euler = I + 'RayLSeriesEulerProduct.lean'
prod = I + 'DedekindZetaFactorizationRay.lean'
nonzero = I + 'RayLNonvanishingAtOne.lean'
primes = I + 'InfinitelyManyPrimesInRayClass.lean'
norm = I + 'ExistsNormPrime.lean'
host = 'src/Development/AutomorphicArithmetic/PrimeDiscriminants/ExistsHost.lean'
rt = 'src/Formalism/SharpRestriction/InertJacobiLevels/HostFam.lean'
bb = I + 'ExistsModulusBbDisjoint.lean'
relevel = I + 'ExistsHostCongruencePrimes.lean'
hc = I + 'HarishChandraParameterFormula.lean'
prescribed = I + 'ExistsHarishChandraWeights.lean'
prech = A + 'DuStarPos.lean'
level = I + 'ExistsLevelCharactersLarge.lean'
pre = F + 'RootOfUnityEightQMemCoeffGaloisSubfield.lean'
prex = A + 'SpreadLe.lean'
diag = I + 'DiagSingleSingle.lean'
spaces = I + 'SpacesNormHasFrame.lean'
two = I + 'ExistsNatBoundPre.lean'
integer = I + 'CardDvdCardGL.lean'
colin = A + 'TrueColumnChoicesHeckeCharReferenceEqOne.lean'
jets = G + 'ExistsHypJetsAll.lean'
assembled = I + 'ExistsColumnInputAssembled.lean'
vol = F + 'CdScaleTieIff.lean'
gj = I + 'InhabitedStage.lean'
sizes = I + 'DsPPosAndLower.lean'
ctx = A + 'CmQuadraticFormEqAlternatingForm.lean'
g_big = A + 'ExistsMuIsRamified.lean'
du_nat = A + 'RecExGOfRecAtG.lean'
window = G + 'WindowLower.lean'
rec = I + 'ExistsLayeredDataOfGoodScaleContexts.lean'
bpt = W + 'ValidForConstructedPointClassesEventuallyWorking.lean'
qd = W + 'FamilyClassSevenDutiesAndStableLattices.lean'
setdiv = G + 'TwGoodOneSetDiv.lean'
lay = W + 'SetUnipotentTranslate.lean'
layof = I + 'ExistsLayerParametersAdmissible.lean'
count = I + 'SizesEqCount.lean'
core = A + 'RationalRootsDef.lean'
hframe = I + 'NonemptyHostHeckeCharacterFrame.lean'

claims = [
 claim('IG1', 'Full partial ray-zeta continuation from a shifted lattice',
  'For any imaginary-quadratic RayData and integer modulus M>=2, construct the ideal/lattice bijection with exact unit multiplicity and covolume; Gaussian Poisson and Mellin splitting give a common positive residue at one and the zero at minus one.',
  ['TL14'],
  ss(ray, 'primeTo rayCon finite_quot RayData equivRayGroup cnt finite_cnt') +
  ss(epstein, 'summable_shiftedLattice_normSq_rpow exists_entire_dirichlet_of_theta epsteinZeta_shifted_continuation') +
  ss(partial, 'finite_units abs_im_eq cls_iff lattice_bij gen_bij hasSum_cnt partial_zeta_continuation'),
  'Direct planar Fourier/Mellin proof supplies the substantive global analytic continuation, with exact source class multiplicities and common residue; no nonvanishing premise.'),
 claim('IG2', 'Nonvanishing at one and arbitrarily large prime norms',
  'Prove all nonprincipal ray L-functions are nonzero at one by the entire character product, nonnegative coefficients and Taylor/Tonelli positivity at minus one; then use logarithmic orthogonality to obtain prime ideals of arbitrarily large rational-prime norm in every ray class.',
  ['IG1'],
  ss(euler, 'lseriesSummable_card_absNorm summable_norm_absNorm_cpow RayData.coef_eq_tsum RayData.lseries_eq_exp_tsum') +
  ss(prod, 'sum_characters_nonneg posDirichlet_local ray_prod_LSeries_nonneg') +
  ss(nonzero, 'RayData.LSeries_coef_eq_sum rayLSeries_entire_ne_zero_one') +
  ss(primes, 'log_bounded logSum_sub_bounded sum_char_eq_zero not_summable_class summable_of_not_prime_or_le exists_prime_in_class'),
  'Replaces a general nonnegative-series continuation argument by an explicit entire Taylor expansion; states the full analytic domain and does not assume an abscissa lower bound or prime existence.'),
 claim('IG3', 'Integral norm factors and rational progression primes',
  'Construct an actual integral pi in the specified imaginary quadratic subfield with prime norm and the prescribed congruence; derive rational progression primes via a temporary quadratic field unramified at the modulus and local norm surjectivity.',
  ['IG1', 'IG2', 'DR1'],
  ss(norm, 'norm_nonneg_of_imag_quadratic exists_prime_norm_of_two_le exists_prime_norm norm_eq_mul_conj sqrtMinusD_mem finrank_K isTotallyComplex_K norm_K dvd_of_eq_mul_integral exists_norm_prime'),
  'The exact integral factor proof follows ideal cancellation; the arbitrary rational progression corollary is an explicit human reduction using the already proved generic norm-unit lemma, not a claimed literal source proof.'),
 claim('IG4', 'Original arithmetic host with exact ranks and labels',
  'Choose the literal Rt(0) ranks and cyclic host by two explicit prime progressions, then supply the actual raw and derived host, top ideal, initial level labels and distinguished finite data.',
  ['IG3', 'AH1', 'AH2', 'AH3', 'AH4', 'AH5', 'AH13', 'AH17'],
  ss(rt, 'Rt') + ss(host, 'top_not_le_span withTop oddProd_odd exists_d exists_q exists_host_of_injective exists_host_over_cyclic_two_power'),
  'Reconstructs the prime choices and every additional Host label; reuses the prior full raw/derived arithmetic host proof rather than assuming Host existence.'),
 claim('IG5', 'Separated auxiliary primes and norm factors',
  'Choose pi0,pi1 and g0,g1 with exact conductor congruences and prove disjoint BB sets from the square-modulus factorization and valuation bound; then choose the two larger distinguished primes.',
  ['IG3', 'IG4'],
  ss('src/Formalism/CyclotomicNorms/StatementI.lean', 'Exc BB') +
  ss(bb, 'exc_dvd_prod_range not_exc_of_cong_sq exists_modulus_bb_disjoint') +
  ss(relevel, 'exists_relevel_primes_one_mod exists_host_level_primes_one_mod'),
  'Explicit valuation calculation retains the exponent 2r+1, squared modulus, strict exceptional inequality, and original arithmetic host.'),
 claim('IG6', 'Two coded HC columns with integral shift and common spread',
  'Give all HC entries for two constant Boolean words, verify gaps and five shared-coordinate identities, prove MUQ from parallel integer shifts, and choose one finite spread bound giving the literal HasLetters identity.',
  ['IG4', 'IG5', 'AC2', 'AC3'],
  ss(hc, 'hcStdU hcStdU_zero hcStdU_succ hcStdU_last exists_hcParam_std') +
  ss(prescribed, 'exists_preCh_of_prescribed') + ss(prech, 'PreCh') +
  ss(two, 'exists_nat_bound_pre exists_pre_two_words'),
  'Displays the actual formulas behind the prescribed-parameter producer; e_even is treated as MUQ and not as literal parity of the integer entries.'),
 claim('IG7', 'Common type prime and exact initial window',
  'Choose an actual common type norm factor, set duStar=1, Dstar=4*T^(fk), Gamma=2, and verify every LevCh clause and the exact lower window endpoint T; retain the literal scalar quotient.',
  ['IG3', 'IG5', 'IG6'],
  ss(level, 'window_low exists_levCh_gt') + ss(prech, 'LevCh LevCh.host LevCh.piT_ne Pre.ofCh') +
  ss(pre, 'Pre'),
  'Free initial numerical choices prove actual existence with the exact window; this does not prove LevelPrime for a preassigned interval.'),
 claim('IG8', 'Actual spaces and all original PreX fields',
  'Use the same type factor for the diagonal top line and explicit hyperbolic pairs; supply the finite-adelic sign isometry using local norm-minus-one units; then construct the two-word PreX and its exact splitting and spread fields.',
  ['IG4', 'IG5', 'IG6', 'IG7', 'SE15', 'AH9', 'AH11', 'DR1'],
  ss(diag, 'sign_congr spacesStd GlobalTheory.Mem.exists_spaces') +
  ss(spaces, 'planeVec planeVec_planeVec top_line_norm spacesNorm spacesNorm_z_norm spacesNorm_hasFrame spacesNorm_coord spacesNorm_T spacesNorm_Vneg spacesNorm_Y_sig') +
  ss(prech, 'DiagSpaces Pre.ofCh') + ss(prex, 'PreX') + ss(two, 'exists_pre_two_words'),
  'Supplies the actual finite-adelic isometry in addition to archimedean signatures; checks all 17 literal PreX data/condition fields on the same object.'),
 claim('IG9', 'Exact positive integer mass-index size',
  'Reduce finite lattice automorphisms injectively at a large degree-one prime, prove their orders divide the column index, and sum the finite genus mass; binomial-polynomial determinants give the exact positive integral HC dimensions and duStarOf.',
  ['IG5', 'CR4', 'AH9'],
  ss(integer, 'idx_eq dimV_nat resHom finrank_red card_dvd_card_GL mass_mul_idx duStarOf_nat') +
  ss(H + 'HermitianLatticesProofs/MassBasic.lean', 'massBasic_mass_eq massBasic_self_mem_genus massBasic') +
  ss(colin, 'duStarOf'),
  'Gives integral divisibility rather than rational rank alone, including arbitrary local ramification in the prime-to-g kernel step; finite mass is used without an analytic mass ratio formula.'),
 claim('IG10', 'Actual original sized preliminary input',
  'Restrict the constructed two-word datum to its base word, choose the exact positive integer duStarOf, reset Dstar=T^(fk)*Gamma^2*duStar, and prove all four literal exists_pre_sized conclusions with the exact window.',
  ['IG8', 'IG9'],
  ss(jets, 'exists_pre_sized') + ss(pre, 'Pre') + ss(prex, 'PreX') + ss(colin, 'duStarOf'),
  'Actual source construction on Unit; preserves host, spaces, norm factors, letters and all PreX clauses and does not claim simultaneous normalization of two distinct words.'),
 claim('IG11', 'Orientation and both pins on the same input',
  'For any supplied PiBar orient each auxiliary norm factor by conjugation, prove the exact prime-membership equivalence, and obtain coordinate and scalar pins without changing type factors, size or frame data.',
  ['IG8', 'IG10', 'SE15', 'SE16'],
  ss(assembled, 'isMaximal_span cjO cjO_coe conj_conj exists_orient Oriented exists_oriented') +
  ss(prech, 'Pre.ofCh') + ss(hframe, 'nonempty_hFrame', 'explicit_remaining_full_character_frame_boundary'),
  'Closes original existence and orientation before the prior pins normal form; a supplied PiBar is not treated as a full HFrame.',
  ['PiBar is supplied for the orientation statement. Full HFrame character producers remain separately identified.']),
 claim('IG12', 'The exact baseVol empty-jet stage',
  'Apply the genuine prescribed-rank GJ model to the exact positive function baseVol and same CDHaar; obtain J.cd=cd, J.vol=baseVol(B,J.cd), noJet, and all FinClasses clauses.',
  ['SE11', 'SE12'],
  ss(vol, 'IsCMFam IsVolMeasF VolIs trueVol trueVol_pos trueVol_spec FiniteVolume₂') +
  ss(gj, 'baseVol baseVol_pos noJet oneJet exists_noJet exists_oneJet nonempty_stage'),
  'Preserves the chosen-volume definition including its fallback; no geometric volume witness or VolumeEqMass2 follows from positivity alone.',
  ['A Base B and Cols B are supplied. For the fixed-cd conclusion that CDHaar is supplied; SE11 supplies one when only existence is required.']),
 claim('IG13', 'Actual recursive size positivity and uniform integrality',
  'Identify trueDsig with the ordered row Vandermonde polynomial, prove positive DsP and its literal two-thirds lower bound, and prove uniform positive integral duP for every supplied large-scale ChOK word.',
  ['IG9', 'RF11', 'RF12'],
  ss(ctx, 'duP DsP') + ss(sizes, 'dimV_cast trueDsig_eq_dimV idxRowLoc_pos DsP_pos_and_lower') +
  ss(g_big, 'g_big') + ss(du_nat, 'exists_du_nat') + ss(vol, 'trueDsig'),
  'Separates equality of defined formal-degree polynomials from analytic discrete-series existence; does not substitute the fixed-rank initial input for arbitrary large-scale input.'),
 claim('IG14', 'Exact recursive-existence join with remaining numerical and core inputs',
  'Under the displayed quantitative window, actual RecAtG package and EvP premise, construct RecExP with the original threshold order, sizes before every level choice, dependent-pair transport, and unchanged QD witnesses after setDiv.',
  ['IG13'],
  ss(window, 'window_lower', 'retained_quantitative_source_input') +
  ss(rec, 'recExP_of_recAtG') + ss(ctx, 'Ctx Ctx.Over RecExG RecAtG') +
  ss(bpt, 'large_of_sup BPt BPt.Is FromCoreK EvP RecExP') +
  ss(qd, 'TupUsedAt TwAllAt MtStableAt QD withQD') + ss(setdiv, 'twGoodOne_setDiv qd_setDiv') +
  ss(lay, 'Lay RecOK LedOK LedPart', 'literal_remaining_recursive_record_boundary') +
  ss(core, 'Core', 'literal_remaining_core_boundary') +
  ss(layof, 'lay layObj_lay lay_of_core', 'remaining_actual_core_to_layer_producer') +
  ss(count, 'sizes_eq_count', 'remaining_actual_mass_volume_size_bridge'),
  'Complete logical and same-object join conditional on the explicit window theorem and actual core package; the original SiegelMassRatioCM-to-window deduction and core supply are not marked reconstructed.',
  ['The quantitative window_lower conclusion at duP, DsP and GamS remains supplied. Its source deduction from SiegelMassRatioCM is a continuation target.',
   'The actual RecAtG witness with FromCoreAt, tuple use, all twists and integral scalar stability is supplied, as is the stated EvP implication.'],
  status='conditional_reduction')
]

# Every historical dependency must resolve before the cumulative merge.
old_path = HERE.parent / 'history/version_0_17/provenance.json'
old_ids = {c['id'] for c in json.loads(old_path.read_text())['claims']} if old_path.exists() else set()
new_ids = {c['id'] for c in claims}
if old_ids:
    assert not new_ids & old_ids
    assert {d for c in claims for d in c['depends_on']} <= old_ids | new_ids

target_specs = [
 (1, hframe, 'nonempty_hFrame',
  'Construct the actual host HFrame, retaining all prescribed mu0, etaT, chiPsi, delta and delta-prime character laws on the same host.',
  'IG11 supplies only factor orientation for a PiBar. The four actual Hecke-character producers below remain; a synthetic NStage etaT is not this producer.',
  [(I+'ExistsUnitaryMuZeroCharactersOfSplitTypePrimesAl.lean', 'exists_unitary_mu_zero_characters_of_split_type_primes'),
   (I+'HostEtaTildeCharacterExists.lean', 'etaT_exists'),
   (I+'ExistsUnramifiedCmTypeHeckeCharOnHost.lean', 'exists_chiPsi'),
   (I+'HostDeltaCharacterInertialOrderFifteenExists.lean', 'delta_exists')]),
 (1, window, 'window_lower',
  'Prove the quantitative logarithmic window from literal SiegelMassRatioCM, local-index ratios and averaged Vandermonde bounds, uniformly in the original threshold order.',
  'IG13 gives exact positive/integral sizes, while IG14 retains this quantitative conclusion. Qualitative norm-prime existence and the freely set initial window do not imply it.',
  [(window, 'places_ok'), (window, 'rank_consts')]),
 (1, layof, 'lay_of_core',
  'Supply an actual V4.Core and the true VolumeEqMass2/size bridge, then prove the nine RecOK duties and universal LedOK lattice comparisons on the same object.',
  'IG14 reconstructs only the dependent join. Bare GJStage or adapted NStage does not imply these fields; the source untwisted-empty Core is explicitly impossible.',
  [(core, 'Core'), (count, 'sizes_eq_count'), (A+'ExistsStagesClauses.lean', 'isEmpty_core_untw'),
   (A+'ExistsStagesClauses.lean', 'exists_stages_clauses')]),
 (2, jets, 'exists_colIn_jets',
  'Join the actual sized/oriented preliminary input to the actual HFrame, finite field extensions, ambient input and bounded-jet field so the original existential ColIn/JetsIn theorem follows.',
  'IG10 removes original PreX existence and IG11 gives its orientation; prior conditional CA13 supplies canonical EvLg. The genuine host-character frame and exact same-base field/jet join must still be established, not inferred from bare stage existence.',
  [(assembled, 'exists_holds'), (assembled, 'exists_colIn')])
]
targets = []
for priority, path, name, objective, remaining, support in target_specs:
    s = source(path, name, 'retained_primitive_or_actual_producer')
    targets.append(dict(priority=priority, path=path, declaration=s['declaration'], source=s,
      source_ranges=[s]+[source(p,n,'substantive_remaining_supplier') for p,n in support],
      objective=objective, remaining_human_scope=remaining, already_reconstructed=['IG10','IG11','IG12','IG13','IG14'],
      supplied_conclusion_not_assumed_proved=True))

closed_specs = [
 (epstein, 'epsteinZeta_shifted_continuation', ['IG1']),
 (partial, 'partial_zeta_continuation', ['IG1']),
 (nonzero, 'rayLSeries_entire_ne_zero_one', ['IG2']),
 (primes, 'exists_prime_in_class', ['IG2']),
 (norm, 'exists_norm_prime', ['IG3']),
 (host, 'exists_host_over_cyclic_two_power', ['IG4']),
 (bb, 'exists_modulus_bb_disjoint', ['IG5']),
 (relevel, 'exists_host_level_primes_one_mod', ['IG5']),
 (hc, 'exists_hcParam_std', ['IG6']),
 (level, 'exists_levCh_gt', ['IG7']),
 (two, 'exists_pre_two_words', ['IG4','IG5','IG6','IG7','IG8']),
 (integer, 'duStarOf_nat', ['IG9']),
 (jets, 'exists_pre_sized', ['IG10']),
 (assembled, 'exists_oriented', ['IG11']),
 (gj, 'exists_noJet', ['IG12']),
 (gj, 'nonempty_stage', ['IG12']),
 (sizes, 'DsP_pos_and_lower', ['IG13']),
 (du_nat, 'exists_du_nat', ['IG13'])
]
closed = []
for path, name, ids in closed_specs:
    s = source(path, name, 'literal_completed_source_target')
    closed.append(dict(path=path, declaration=s['declaration'], closed_by=ids, source=s,
      scope='Human reconstruction under the precise displayed original parameter hypotheses; see the named paragraphs for unchanged data and qualitative versus quantitative scope.'))

conditional = [dict(source=source(rec,'recExP_of_recAtG','conditionally_reconstructed_join'),
  reconstructed_by=['IG13','IG14'], retained=['window_lower from SiegelMassRatioCM', 'actual RecAtG with FromCoreAt', 'stated EvP'],
  scope='Thresholds, dependent transport and QD conclusion reconstructed. The quantitative and actual-core suppliers remain explicit.')]

record_specs = [
 (prex, 'PreX', ['piG','piG_K','piG_norm','piG_cong','piT','piT_K','piT_norm','piT_cong','pde_split','ccK_top','e_even','hcW_inj','a','g_big','T_gt','a_gt','spread_le'],
  {'piG':'IG5','piG_K':'IG5','piG_norm':'IG5','piG_cong':'IG5','piT':'IG7','piT_K':'IG7','piT_norm':'IG7','piT_cong':'IG7',
   'pde_split':'IG8','ccK_top':'IG4','e_even':'IG6','hcW_inj':'IG6','a':'IG6','g_big':'IG5','T_gt':'IG7','a_gt':'IG6','spread_le':'IG6'}, False),
 (prech, 'LevCh', ['T','T_prime','T_cond','piT','piT_K','piT_norm','piT_cong','T_ne_pde','duStar','duStar_pos','Dstar','Dstar_pos','GamP','one_lt_gammaP','T_win'],
  {}, False),
 (lay, 'RecOK', ['del','etaF','untw','fin','dgam','full','tame','mink','atT'], {}, True)
]
record_audits = []
for path,name,expected,support,retained in record_specs:
    s=source(path,name,'literal_record_field_inventory')
    rows=read_source(path)[1][s['line_start']-1:s['line_end']]
    field_names=[m.group(1) for line in rows[1:] if (m:=re.match(r'^  ([^\s:]+)\s*:',line))]
    assert field_names==expected,(name,field_names)
    record_audits.append(dict(record=s['declaration'],source=s,field_count=len(field_names),
      all_fields_constructed=not retained,
      fields=[dict(name=f,supplied_by=('explicit_retained_actual_core_input' if retained else support.get(f,'IG7')))
        for f in field_names]))

out = dict(schema_version='1.3',artifact_version='0.18',date='2026-11-21',
 component='initial_geometry',owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes with no newline or Unicode normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(
  derived_simplification='Human proof under exact declared hypotheses; source arguments may be replaced by explicitly explained shorter proofs.',
  conditional_reduction='Logical and same-object implication proved with the displayed remaining quantitative/core inputs retained.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,record_audits=record_audits,
 prior_components_reused=['TL','AH','AC','DR','CR','RF','SE'],same_iteration_companions=[],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Qualitative imaginary-quadratic ray prime norms and actual integral factors',
  'Original two-word PreX with actual host and diagonal spaces including finite-adelic sign isometry',
  'Positive integer duStarOf and actual exists_pre_sized',
  'Original auxiliary-factor orientation and prior coordinate/scalar pins on the same input',
  'Exact baseVol/noJet GJStage with same CDHaar and all finite-class clauses',
  'Actual DsP positivity and uniform duP integrality',
  'Complete recursive-existence quantifier and transport join conditional on explicit remaining window/core inputs'],
 scope_precision=[
  'IG1 supplies full-plane continuation before IG2 uses its entire-product contradiction; no nonvanishing is hidden in prime selection.',
  'Qualitative initial prime choices give no uniform short-interval LevelPrime or arbitrary large-scale ChGood.',
  'The sized source input has Unit words; no two-word simultaneous mass normalization is claimed.',
  'No integral Weyl/dual-Weyl equality is inferred from the dimension determinant.',
  'baseVol positivity does not prove VolIs, finite covolume or VolumeEqMass2; its fallback is explicit.',
  'Full HFrame, quantitative mass-window deduction, and genuine V4.Core/Lay/RecOK/LedOK suppliers remain.',
  'IG14 is conditional; it does not close the original SiegelMassRatioCM-to-window primitive or actual-core existence.',
  'All predecessor files and claims are preserved; this builder writes only the current component.'])

review_specs = [
 ('root_reviews_initial_geometry.txt','/root',list(range(1,15)),'Independent full initial-geometry, exact-size, analytic-prime and recursive-boundary review.'),
 ('ls_reviews_ig_1_3.txt','/root/global_frame',list(range(1,4)),'Independent ray-zeta, nonvanishing and integral norm-prime review.')
]
for filename,reviewer,indices,scope in review_specs:
    p=HERE.parent/'reviews_v0_18'/filename
    if not p.exists():continue
    raw=p.read_bytes();content=raw.decode()
    chosen={f'IG{i}':paragraphs[f'IG{i}'] for i in indices}
    for key,sha in chosen.items():assert sha in content,('review paragraph changed',filename,key,sha)
    out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
      review_record='../reviews_v0_18/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
      paragraph_range='Bytes from named IG paragraph through immediately before the next IG paragraph; EOF for IG14.',
      lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc += [f"{c['id']} | {c['title']} | {c['status']}",c['statement'],
            f"  proof_paragraph_sha256: {paragraphs[c['id']]}"]
    for s in c['sources']:
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
    loc += ['']
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.18',commit=PIN,targets=targets,
    closed_source_targets=closed,conditionally_reconstructed_targets=conditional,retained_inputs=common,
    remaining_boundary='Original sized preliminary geometry and exact baseVol/noJet are supplied. Genuine HFrame characters, quantitative mass-window deduction, actual Core and mass/volume/recursive lattice duties, and their precise ColIn/JetsIn join remain as stated.'),
    ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 distinct_claim_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 source_files=len(files),next_targets=len(targets),completed_source_targets=len(closed),
 conditionally_reconstructed_targets=len(conditional),verified_equal_to_pinned_git_blob=True,
 record_field_counts={a['record']:a['field_count'] for a in record_audits},
 independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))

