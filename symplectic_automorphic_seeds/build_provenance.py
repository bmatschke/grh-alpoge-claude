#!/usr/bin/env python3
"""Bind the complete case-II seed construction to the unchanged pinned source."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=WORK.parent / 'lean-source')
REPO = ap.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMP = 'symplectic_automorphic_seeds'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DC = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
BR = AV + 'BuildingsResidueChars/'
PI = AV + 'ModularityArgument/AutomorphyLifting/PrimeIndexConstruction/'
QS = AV + 'IdeleGenerators/QuadraticSplitting/'
HI = AV + 'IdeleGenerators/HolomorphicIrreducibility/'
TK = 'src/PositivityTheory/AutomorphicForms/PublishedInputs/JacquetLanglands/TorusKernels/'
PREFIX = {'DC/': DC, 'BR/': BR, 'PI/': PI, 'QS/': QS, 'HI/': HI, 'TK/': TK}
cache = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def source(file, spelling, role):
    if file.startswith('src/'):
        path = file + '.lean'
    else:
        pre = next((x for x in PREFIX if file.startswith(x)), None)
        path = (PREFIX[pre] + file[len(pre):] if pre else AV + file) + '.lean'
    raw = (REPO / path).read_bytes()
    ls = raw.splitlines(keepends=True)
    pat = r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)'
    starts = [(i, m.group(1)) for i, s in enumerate(ls, 1)
              if (m := re.match(pat, s.decode()))]
    found = [(i, n) for i, n in starts if n == spelling or n.endswith('.' + spelling)]
    assert len(found) == 1, (file, spelling, found)
    start, name = found[0]
    end = min([i for i, _ in starts if i > start] or [len(ls) + 1]) - 1
    while not ls[end - 1].strip():
        end -= 1
    block = b''.join(ls[start-1:end])
    if path not in cache:
        pinned = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
        assert pinned == raw, 'Pinned Git blob mismatch: ' + path
        cache[path] = dict(path=path, sha256=sha(raw), bytes=len(raw), lines=len(ls),
                           verified_equal_to_pinned_git_blob=True)
    return dict(path=path, declaration=name, source_spelling=spelling,
                line_start=start, line_end=end, sha256=sha(raw),
                range_sha256=sha(block), range_bytes=len(block),
                first_line=ls[start-1].decode().rstrip(), role=role,
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}',
                verified_equal_to_pinned_git_blob=True)


specs = {
    'SX1': [
        ('WeakShimuraTheory/NearSplit', 'Ctx2', 'Original case-II context'),
        ('WeakShimuraTheory/NearSplit', 'Tower', 'Original embedded fields, abelian F, places and labels'),
        ('WeakShimuraTheory/NearSplit', 'chi', 'Literal two possible orderings of four characters'),
        ('WeakShimuraTheory/NearSplit', 'Ok', 'Original residual separation and inertia controls'),
        ('WeakShimuraTheory/NearSplit', 'Two', 'Original real quadratic, splitting, finite xi and nontriviality'),
        ('WeakShimuraTheory/NearSplit', 'Deep', 'Prime-to-ell order of psi on original G_F'),
        ('QS/QuadSplit', 'Hyp', 'Exact quadratic input used by source induction'),
        ('QS/QuadSplit', 'CharDat', 'Exact character table and original t0'),
        ('BR/ExistsQuadraticCharacterOfSubgroupIndexTwo', 'exists_sign_character_index_two', 'Elementary continuous sign character'),
        ('BR/ExistsQuadraticCharacterOfSubgroupIndexTwo', 'exists_quadratic_character_of_subgroup_index_two', 'Actual original-field quadratic supplier'),
        ('BR/GaloisCharacterResidualDecomposition', 'induced_characters_values', 'Literal diagonal table on both cosets'),
        ('BR/GaloisCharacterResidualDecomposition', 'galois_character_residual_decomposition', 'All original character properties'),
        ('PI/ContRes', 'mixOfP', 'Source restriction to the two split ell places of the quadratic field'),
    ],
    'SX2': [
        ('PublishedTheorems/Hilbert', 'HilbertEisOne', 'Exact weight-one series with constant independent of finite idele'),
        ('LiteratureResults/OneUseOf', 'OneUse', 'Level-one form congruent to one; replaced by the Hasse norm construction'),
        ('IdeleGenerators/IsCondAt', 'HasExp', 'Normalized adelic constants and positive coefficients'),
        ('IdeleGenerators/IsCondAt', 'IsHol', 'Original finite central character and holomorphic level'),
        ('IdeleGenerators/IsCondAt', 'hkCoef', 'Hecke coefficient recurrence at the original weight'),
        ('IdeleGenerators/WeightChange', 'Emix', 'Actual mixed stabilized series'),
        ('HI/MemMirabQuot', 'holB', 'Degeneracy sends c0(y) to c0(yu), including narrow-class components'),
        ('HI/NotDvdMul', 'step', 'Finite prime-by-prime stabilization and constant cancellation'),
        ('HI/NotDvdMul', 'emix', 'Full stabilized integral positive q-expansion'),
        ('DC/THolLift', 'Phi_inj', 'Positive coefficient injectivity on the full holomorphic space'),
        ('DC/THolLift', 'holLift_alt', 'Finite algebra eigenlift from the integral coefficient lattice'),
        ('DC/MPropMHol', 'gal_of', 'Residual finite-character comparison for Eisenstein systems'),
        ('DC/MPropMHol', 'propMHolZ_alt', 'Actual cusp supplier by incompatible ordinary refinements'),
        ('IdeleGenerators/WeightChange', 'PropMHol', 'Precise full-holomorphic congruence interface being specialized'),
    ],
    'SX3': [
        ('TK/IsHolVOf', 'HolWC', 'Actual ordinary weight-change predicate; matched only in the needed quadratic setting'),
        ('IdeleGenerators/IsCondAt', 'OrdForm', 'Determinant, local characters, U refinement and weights'),
        ('DC/SVRPropMV', 'pf_PropMV_sv_alt', 'Source ordinary classical point and Galois specialization'),
        ('DC/BirthMix', 'mix_birth_of_prints', 'Exact dual/cyclotomic normalization and ordered residual flags'),
        ('ModularityArgument/BaseChangeUnits/BaseChangeNorms/MixSeed', 'ordAt_tw', 'Residual upper-character orientation after chi^k twist'),
        ('ModularityArgument/BaseChangeUnits/BaseChangeNorms/MixSeed', 'irrOpen_of', 'Irreducibility on every open subgroup'),
        ('HI/LineOfNotIrr', 'line_of_not_irr', 'Invariant lines from a distinct local eigenvalue'),
        ('HI/LineOfNotIrr', 'sIabs', 'Trace-zero coset contradicts nontrivial residual square'),
        ('PI/MixSeedPAlt', 'MixSeedP', 'Full source rank-two supplier; only its actual quadratic specialization is promoted'),
        ('PI/MixSeedPAlt', 'PR', 'Actual regular algebraic cuspidal witness and PlainR'),
        ('QS/QuadSplit', 'MixDat', 'Exact determinant, strong irreducibility, local type and mixed weights'),
        ('ModularityArgument/AutomorphyLifting/PlainAtR', 'PlainR', 'Every finite component is unlinked principal series or spherical'),
        ('AutomorphicForms/BlochKatoSelmerVanishes', 'FrobEig', 'Geometric rather than arithmetic Frobenius convention'),
        ('AutomorphicForms/BlochKatoSelmerVanishes', 'algSat', 'q^((n-1)/2) normalization'),
        ('AutomorphicForms/IsoOfFrob', 'infOf', 'Exact half-shifted infinitesimal weights'),
    ],
    'SX4': [
        ('HI/RibetLat', 'core', 'Actual trace identities and compact maximum normalization'),
        ('HI/RibetLat', 'ribetLat', 'Complete source Ribet lattice theorem'),
        ('BR/ExistsRibetLattice', 'exists_ribet_lattice', 'Original subgroup H and original t0 squared'),
        ('BR/SymmetricSquareMixedExists', 'Pm', 'Explicit integral mixing basis'),
        ('BR/SymmetricSquareMixedExists', 'Qmix', 'Full mixed subgroup matrix'),
        ('BR/SymmetricSquareMixedExists', 'Qoff', 'Diagonal matrix for the original element outside H'),
        ('BR/SymmetricSquareMixedExists', 'gram', 'Exact alternating-form sign'),
        ('BR/SymmetricSquareMixedExists', 'symmetric_square_mixed_exists', 'Actual induced symplectic representation'),
        ('BR/MixMatrixResidueProperties', 'key', 'Integral support and the unit-entry alternative'),
        ('BR/MixMatrixResidueProperties', 'mixMatrix_residue_properties', 'Literal source MixRes'),
        ('QS/IndGlobOfKill', 'indGlob_of_kill', 'Global integrality on both cosets after near-one twist'),
        ('DC/BirthSeedII', 'indEx', 'Original assembly of r, roots, induction and correcting character'),
    ],
    'SX5': [
        ('BR/MixStableLineLocal', 'mix_stable_line_local', 'Coordinates of the two actual ordinary invariant lines'),
        ('BR/MixFlagExists', 'low_nn', 'Exact symplectic condition for the lower-unipotent chart'),
        ('BR/MixFlagExists', 'case1', 'First explicit flag matrix and ordered diagonal'),
        ('BR/MixFlagExists', 'case2', 'Second explicit flag matrix and ordered diagonal'),
        ('BR/MixFlagExists', 'mix_flag_exists', 'Valuation bounds and original nonzero local entry'),
        ('BR/InducedFlagCondition', 'induced_flag_condition', 'Every original valuation and common four weights'),
        ('BR/InducedDeletionCondition', 'induced_deletion_condition', 'Exact correcting character, finite-order exponent and open subgroup'),
        ('BR/InducedRepresentationConstituentVanishing', 'induced_representation_constituent_vanishing', 'Literal global inertia kernel N'),
        ('WeakShimuraTheory/RedIdeal', 'muOf', 'Closed-commutator ell-power definition; not identified with all inertia'),
        ('BR/InertiaActsTriviallyOnRootsOfUnity', 'inertia_acts_trivially_on_roots_of_unity', 'muOf is contained in inertia and cyclotomic kernel'),
        ('src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/IndLoc0', 'indLoc0', 'Full local pair and exact doubled Wts construction'),
        ('WeakShimuraTheory/NearSplit', 'Wts', 'One open subgroup before all original places and indices'),
        ('WeakShimuraTheory/RedIdeal', 'IsPair', 'Every actual pair equation, including literal muOf'),
    ],
    'SX6': [
        ('BR/ResidualCharactersPsiNe', 'lim_pt', 'Compact ell-power cluster point in a closed coset'),
        ('BR/ResidualCharactersPsiNe', 'eta_om', 'Cyclotomic-kernel triviality implies omega-kernel triviality'),
        ('BR/ResidualCharactersPsiNe', 'residual_characters_psi_ne', 'Actual Ok.g3-prime no-self-twist argument'),
        ('BR/InducedIrreducible', 'induced_irreducible', 'Exact cyclotomic irreducibility of original induction'),
        ('BR/InducedIrreducible', 'cp_ne', 'Different local weight polynomials on an infinite-order inertia element'),
        ('ModularityArgument/BaseChangeUnits/QuadraticInductionGL2Alt', 'AttInd', 'Untwisted AI attaches R chi^-1, hence required extra determinant twist'),
        ('ModularityArgument/BaseChangeUnits/QuadraticInductionGL2Alt', 'UpQuadI', 'Source first quadratic CM base change'),
        ('ModularityArgument/BaseChangeUnits/QuadraticInductionGL2Alt', 'UpSolI', 'Source later solvable base change'),
        ('DC/BirthIndS', 'indAutLP_of_upQuad_upSol_indAutCs', 'Source automorphic induction assembly; specialized here to the constructed r'),
        ('PI/RankFourAutomorphyOfTensor', 'IndAutLP', 'Larger universal interface is not separately promoted'),
        ('PI/CuspidalRankFourRegularAlgebraicTotallyComplex', 'CuspidalRankFourRegularAlgebraicTotallyComplex', 'Exact regular algebraicity AND AllWin target'),
        ('ModularityArgument/LeviSmoothLocalization/WinUpDown', 'WinAt', 'Strict one-half width at a finite place'),
        ('ModularityArgument/LeviSmoothLocalization/WinUpDown', 'AllWin', 'One real center before every finite place'),
    ],
    'SX7': [
        ('BR/AutomorphicFormsDescentToSmallerLevel', 'automorphic_forms_descent_to_smaller_level', 'Actual finite coefficient capture source endpoint'),
        ('DC/InducedFinalStatement', 'fin_adj', 'Symplectic adjoint commutes with injective coefficient maps'),
        ('DC/InducedFinalStatement', 'fin_conj', 'Original conjugation equations descend'),
        ('DC/InducedFinalStatement', 'fin_gsp', 'Exact multiplier identity returns to O_c1'),
        ('DC/InducedFinalStatement', 'induced_final_statement_alt', 'Actual pair, original residual record and root entries'),
        ('WeakShimuraTheory/RedIdeal', 'Res', 'Original residual pair congruences'),
        ('WeakShimuraTheory/RedIdeal', 'InV', 'Both global support and all original local flag supports'),
        ('WeakShimuraTheory/RedIdeal', 'Ent', 'Existence of an actual nonzero root entry'),
        ('DC/PotentialModularityTower', 'SeedPairAlt', 'Integral pair, adic continuity, residual pair and seed'),
    ],
    'SX8': [
        ('DC/PotentialModularityTower', 'IsSeedAlt', 'Full irreducibility, weights, parity, local twist, cusp and AllWin clauses'),
        ('DC/PotentialModularityTower', 'SeedPairAlt', 'Original integral seed record'),
        ('DC/PotentialModularityTower', 'SeedIIAlt', 'Literal universal endpoint and exact root alternative'),
        ('DC/BirthSeedII', 'seedII_of_p_alt', 'Final source endpoint with same original iota and coefficient return'),
        ('DC/SeedIIZ', 'seedII_Z_alt', 'Original source producer replaced by the complete selected chain'),
        ('DC/BcIndCs', 'seedIIs_alt', 'Original packaged producer; no blanket HypothesesH-prime premise retained'),
    ],
}
titles = {
    'SX1': 'Original quadratic field, character table and residual separation',
    'SX2': 'Actual cuspidal eigenlift from mixed Eisenstein refinements',
    'SX3': 'Fixed-central ordinary weight change and the complete mixed rank-two representation',
    'SX4': 'Explicit normalized Ribet lattice and symplectic induction',
    'SX5': 'Every original local flag, literal muOf condition and exact correcting character',
    'SX6': 'Cyclotomic irreducibility, actual automorphic induction and the all-place strict window',
    'SX7': 'Finite coefficient capture and return of actual pair and residual entries',
    'SX8': 'Complete literal SeedIIAlt',
}
deps = {'SX1': [], 'SX2': ['SX1'], 'SX3': ['SX1', 'SX2'],
        'SX4': ['SX1', 'SX3'], 'SX5': ['SX1', 'SX3', 'SX4'],
        'SX6': ['SX1', 'SX3', 'SX4'], 'SX7': ['SX4', 'SX5', 'RV4'],
        'SX8': ['SX5', 'SX6', 'SX7']}
classical = {'SX1': ['SX-C'], 'SX2': ['SX-E', 'SX-H', 'SX-C'],
             'SX3': ['SX-O', 'SX-BC', 'SX-G', 'SX-C'], 'SX4': [],
             'SX5': ['SX-C'], 'SX6': ['SX-BC', 'SX-IR'], 'SX7': [], 'SX8': []}
scope = {
    'SX1': 'Every original Ctx2 datum and Ok+Two+Deep tower, with its original embedded quadratic field, t0, character labeling and valuations. No new tower is chosen.',
    'SX2': 'The real quadratic F0 supplied by Two, with ell split, finite totally odd xi of nontrivial conductor at norm2, and nontrivial residual character at both ell places. Fixed iota; an actual cuspidal ordinary eigenlift is produced, with geometric nebentype xi and arithmetic Hecke character xi^-1.',
    'SX3': 'The actual quadratic input of SX1. Complete MixDat and PR for the constructed r=chi^k r_f^vee; k,t>=2 divisible by ell-1; exact determinant and ordered residual characters, inertia type, strong irreducibility and all-place principal-series control. The universal higher-degree MixSeedP package is not promoted.',
    'SX4': 'Actual representation on original G_Q with multiplier chi^k xi phi, its integral restriction to the unchanged G_F, prescribed t0 diagonalization, support and a concrete unit-entry alternative.',
    'SX5': 'Every original local valuation of the unchanged tower, one correcting character, explicit integral symplectic flags, all IsPair equations, literal muOf subset argument, one global finite-order exponent and one open subgroup for all Wts clauses.',
    'SX6': 'The constructed R on the exact original G_L intersect ker cyclotomic. A cuspidal GL4 witness is constructed by cyclic base change and quadratic induction; a single real window center controls every finite place, including above ell. No pre-existing automorphic witness is assumed.',
    'SX7': 'The actual continuous matrix homomorphism and finitely many original local matrices descend to one c1>=c. Closed-subgroup Baire capture is proved for matrices; arbitrary compact subsets are never asserted to lie in a finite extension. All exact residual pair and entry equations return.',
    'SX8': 'Literal SeedIIAlt: forall original Omega,ell,c,D,T satisfying Ctx2,Ok,Two,Deep, forall fixed iota, exists c1>=c and actual Q satisfying SeedPairAlt,InV,and Ent(-alpha) or (Ent(beta) and Ent(-theta)). All weights, gaps, parity, twist exponent and original place quantifiers are retained.',
}
hyp = {
    'SX1': ['D.Ctx2', 'T.Ok', 'T.Two', 'T.Deep'],
    'SX2': ['Original F0 and xi from SX1', 'fixed iota', 'P is one of the two ell places'],
    'SX3': ['Original F0 and xi from SX1', 'fixed iota'],
    'SX4': ['The actual r constructed in SX3', 'the original t0 and labeling from SX1'],
    'SX5': ['Original Ctx2,Ok,Two,Deep data', 'the actual induced R from SX4'],
    'SX6': ['Original Ok,Two tower', 'the constructed r and R from SX3--SX4'],
    'SX7': ['Actual continuous integral pair of SX5'],
    'SX8': ['All original premises of SeedIIAlt; these are not assertions about arbitrary towers'],
}
relations = {
    'SX1': 'Complete elementary reconstruction of original quadratic and character suppliers.',
    'SX2': 'Source stabilization/eigenlift/Eisenstein exclusion reconstructed. The OneUse supplier is proved by a Hasse lift and finite product descent, a simpler classical route than the original package.',
    'SX3': 'Actual ordinary control and Galois theorem matched to primary Hida statements. Independent local conductor and unitary arguments replace larger source H-prime and rank-two packages only in the required real quadratic specialization.',
    'SX4': 'Full explicit source Ribet lattice and matrix induction with the exact alternating-form sign.',
    'SX5': 'Full original local pair and doubled-weight chain, including the actual closed-commutator definition of muOf.',
    'SX6': 'Complete direct proof of the needed induced irreducibility and actual automorphic witness; source IndAutLP is used as a provenance comparison rather than retained as an assumption.',
    'SX7': 'Complete matrix adaptation of the reconstructed RV4 Baire/Krasner mechanism, followed by literal coefficient-map descent.',
    'SX8': 'Full exact outgoing predicate. Broader automorphy, ordinary support and the case-III seed are not promoted.',
}

external = {}
for cid, component in [('RV4', 'rank_one_cohomology')]:
    p = WORK / component / 'provenance.json'
    data = json.loads(p.read_bytes())
    claim = next(c for c in data['claims'] if c['id'] == cid)
    pl = claim['proof_location']
    raw_in = (WORK / component / 'main.tex').read_bytes()
    lines_in = raw_in.splitlines(keepends=True)
    assert sha(b''.join(lines_in[pl['line_start']-1:pl['line_end']])) == pl['sha256']
    external[cid] = dict(component=component, provenance_file=component+'/provenance.json',
                         provenance_sha256=sha(p.read_bytes()), main_tex_sha256=sha(raw_in),
                         proof_location=pl, use='Countability, closed finite fields and Baire mechanism; SX7 proves the matrix subgroup adaptation explicitly.')

main = (HERE / 'main.tex').read_bytes()
lines = main.splitlines(keepends=True)
claims = []
for cid in titles:
    label = next(i for i, l in enumerate(lines, 1) if l.decode().strip() == '\\label{claim:'+cid+'}')
    start = max(i for i, l in enumerate(lines, 1) if i < label and l.decode().startswith(('\\begin{proposition}', '\\begin{theorem}')))
    end = next(i for i, l in enumerate(lines, 1) if i > label and l.decode().strip() == '\\end{proof}')
    block = b''.join(lines[start-1:end])
    claims.append(dict(id=cid, title=titles[cid], introduced_in='0.29',
                       status='Complete human proof in its stated scope with exact named classical inputs',
                       mathematical_status='Actual automorphic seed supplier; no Lean replay',
                       scope=scope[cid], depends_on=deps[cid], classical_inputs=classical[cid],
                       theorem_hypotheses=hyp[cid], remaining_bespoke_inputs=[],
                       proof_location=dict(file=COMP+'/main.tex', paragraph=cid, label='claim:'+cid,
                                           line_start=start, line_end=end, sha256=sha(block), bytes=len(block)),
                       sources=[source(*s) for s in specs[cid]], source_relation=relations[cid],
                       component_ledger=COMP+'/provenance.json'))

boundaries = [
    source('DC/AfDesc', "HypothesesH'", 'Whole published/Hida/descent record is not promoted'),
    source('PI/MixSeedPAlt', 'MixSeedP', 'Higher-degree universal mixed Hilbert seed is not separately promoted'),
    source('PI/RankFourAutomorphyOfTensor', 'IndAutLP', 'Full universal rank-four induction predicate is not separately promoted'),
    source('DC/PromodularityCaseThree', 'SeedIVAlt', 'Separate case-III auxiliary-prime and later-tower seed remains unproved here'),
    source('DC/PotentialModularityTower', 'PMExAlt', 'General modular support remains independent of the seed'),
    source('DC/PotentialModularityTower', 'ProModAlt', 'Actual point realization is owned by UX, not asserted by SX'),
]
validation = dict(claim_count=len(claims), claim_source_links=sum(len(c['sources']) for c in claims),
                  scope_boundary_source_links=len(boundaries),
                  source_files_checked_against_pinned_git_blobs=len(cache),
                  main_tex_sha256=sha(main),
                  verification_kind='Exact declaration/proof byte ranges and equality to pinned Git blobs; no Lean replay')
provenance = dict(schema='rh-human-reconstruction-provenance/1', artifact_version='0.29',
                  date='2026-11-22', repository='https://github.com/CocoSgt/riemann-hypothesis-lean',
                  commit=PIN, component=COMP, main_tex_sha256=sha(main),
                  scope='Complete literal SeedIIAlt by an actual Hilbert cusp, fixed-central ordinary weight change and explicit symplectic induction; all original tower and fixed-iota quantifiers retained.',
                  claims=claims, dependency_graph=deps, external_claim_dependencies=external,
                  classical_input_registry=COMP+'/classical_inputs.json',
                  scope_boundary_sources=boundaries, source_files=list(cache.values()),
                  downstream_consumer_claims=['UX12'], validation=validation)
dump('provenance.json', provenance)

registry = [
    dict(id='SX-E', name='Hilbert Eisenstein series, rational Fourier expansion and holomorphic decomposition',
         statement='Weight-one E_1(1,zeta) for nontrivial totally odd finite zeta has divisor-sum positive coefficients and constant 2^-d L(zeta,0) on every narrow-class component; higher-weight holomorphic eigenforms have the cuspidal/Eisenstein dichotomy.',
         source='Dasgupta--Darmon--Pollack, Hilbert modular forms and the Gross--Stark conjecture, Annals174(2011),439--484',
         theorem='Proposition2.1 formula(50); section2.3 decomposition', printed_pages='458--459,466',
         pdf_zero_based_pages=[19,20,27], url='https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p12-p.pdf',
         used_by=['SX2'], primary_source_inspected=True,
         scope_match='eta=1 has conductor1; zeta has nontrivial conductor from norm2 inertia, so no second weight-one constant term occurs. Degeneracy normalization and cusp exclusion are proved explicitly.'),
    dict(id='SX-H', name='Canonical determinant Hasse invariant and high-power integral lift',
         statement='At good unramified ell level, the determinant Hasse invariant extends to the minimal compactification, is functorial under prime-to-ell isogenies and has Tate-cusp expansion1; every sufficiently high power lifts by Serre vanishing.',
         source='Mok--Tan, Overconvergent Families of Siegel--Hilbert Modular Forms, CJM67(2015),893--922',
         theorem='Lemma2.10 and Proposition2.11', printed_pages='905--906', pdf_zero_based_pages=[12,13],
         url='https://www.cambridge.org/core/services/aop-cambridge-core/content/view/50FFF1DA2A710C2115FCA445AA2F0A66/S0008414X00007628a.pdf/overconvergent-families-of-siegelhilbert-modular-forms.pdf',
         doi='10.4153/CJM-2014-017-9', used_by=['SX2'], primary_source_inspected=True,
         scope_match='Genus1, real quadratic F0, ell split. SX2 proves finite deck and central ideal-class product descent; even starting exponent makes normalized rational norm factors congruent1. No division by the class number or deck-group order.'),
    dict(id='SX-O', name='Fixed-central cuspidal ordinary control and ordinary Galois representation',
         statement='With fixed algebraic central character, the cuspidal ordinary Hecke algebra is finite and torsion-free over the component weight algebra. Dominant arithmetic specialization is classical after inverting ell; normalized U operators are preserved. The classical covariant Galois representation has upper beta and lower alpha, with alpha the ordinary quotient and the stated inertia weights.',
         source='Hida, Control of nearly ordinary Hecke algebras, Luminy lecture18July2007',
         theorem='Theorem1.2; Lemmas2.1--2.2; Theorem2.4; Corollary2.5; Theorem3.1 and Remark3.1',
         printed_pages='3--8', pdf_zero_based_pages=[2,3,4,5,6,7],
         url='https://www.math.ucla.edu/~hida/Lum07.pdf', used_by=['SX3'], primary_source_inspected=True,
         scope_match='Definite quaternion algebra ramified at both real places and no finite places; original tame character and level fixed. (kappa1,kappa2)=(-t,k+t-1)/(0,k-1), common sumk-1. Residual absolute irreducibility is not required for the characteristic-zero point. r=chi^k r_f^vee reverses the ordinary line exactly.'),
    dict(id='SX-BC', name='Cyclic base change and automorphic induction with local compatibility',
         statement='Cyclic base change and induction exist for cuspidal GLn, with the self-twist/conjugacy cuspidality criteria and strong local compatibility. The needed solvable base change is a finite chain of cyclic ones.',
         source='Arthur--Clozel, Simple Algebras, Base Change, and the Advanced Theory of the Trace Formula(1989); Henniart, Induction automorphe globale pour les corps de nombres(2012)',
         theorem='Arthur--Clozel III4.2,III5.1,III6.2; Henniart Theorems4--5,section3.7',
         printed_pages='Arthur--Clozel202--203,212--213,215--217; Henniart6--7,16',
         urls=['https://www.claymath.org/library/cw/arthur/pdf/30.pdf', 'https://www.numdam.org/article/BSMF_2012__140_1_1_0.pdf'],
         used_by=['SX3','SX6'], primary_source_inspected=True,
         scope_match='Only quadratic/abelian extensions and principal-series or unramified local parameters. Unitariy formulation is applied after removing a common real norm twist. The extra |det| in rank4 is proved from the source q^(n-1)/2 normalization.'),
    dict(id='SX-G', name='Normalized polarized CM Galois attachment away from ell',
         statement='A regular algebraic cuspidal polarized representation over a CM field has a continuous semisimple Galois representation with Frobenius-semisimplified local compatibility at every place away from ell.',
         source='Barnet-Lamb--Gee--Geraghty--Taylor, Potential automorphy and change of weight, Annals179(2014),501--609',
         theorem='Section2.1 and Theorem2.1.1(1)--(2)', printed_pages='535--538', pdf_zero_based_pages=[34,35,36,37],
         url='https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf',
         used_by=['SX3'], primary_source_inspected=True,
         scope_match='Only n=2 on an auxiliary CM quadratic split at the inspected place. Strong irreducibility proves base-change cuspidality; central character supplies polarization, adjusted by the CM quadratic sign. No finite discrete-series-place hypothesis is assumed.'),
    dict(id='SX-C', name='Class field, unit, Chebotarev and local GL2 conductor background',
         statement='Local/global Artin reciprocity with geometric convention; Dirichlet units span the logarithmic sum-zero hyperplane; Chebotarev compares continuous traces. Casselman newvector theory bounds local conductor by the chosen level; local GL2 correspondence preserves determinant and Artin conductor, and identifies principal series and special parameters.',
         sources=[
             {'author':'J.S.Milne','title':'Class Field Theory','version':'4.03','location':'ChaptersI,VIII','url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf'},
             {'author':'J.S.Milne','title':'Algebraic Number Theory','version':'3.08','location':'Dirichlet unit theorem;Theorem8.31','url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf'},
             {'author':'W.Casselman','title':'On some results of Atkin and Lehner','location':'Theorem1,printed302--306; scanned theorem page302 directly inspected','url':'https://lesesvre.perso.math.cnrs.fr/newforms-references/casselman.pdf'},
             {'authors':'H.Jacquet,R.P.Langlands','title':'Automorphic forms on GL(2)','location':'ChapterI,section3; local determinant/conductor normalization','url':'https://publications.ias.edu/sites/default/files/automorphic-forms-on-gl2_rpl_9.pdf'},
         ], used_by=['SX1','SX2','SX3','SX5'], primary_source_inspected=True,
         scope_match='Character, conductor equality, unitary bounds and all elementary consequences are proved in the chapter. Only standard local principal-series/special representation facts are used.'),
    dict(id='SX-IR', name='Irreducibility of unlinked principal induction',
         statement='Normalized induction of cuspidal characters rho_i is irreducible if no rho_j equals |det| rho_i. Applied to four one-dimensional characters.',
         source='Bernstein--Zelevinsky, Induced representations of reductive p-adic groups.I, ASENS10(1977),441--472',
         theorem='Theorem4.2', printed_pages='454', pdf_zero_based_pages=[14],
         url='https://www.math.tau.ac.il/~bernstei/Publication_list/publication_texts/BZ-induced-1.pdf',
         used_by=['SX6'], primary_source_inspected=True,
         scope_match='Strict common half-width window puts each exponent difference strictly between-1 and1, giving exactly the theorem premise.'),
]
dump('classical_inputs.json', dict(schema='rh-classical-input-registry/1', artifact_version='0.29',
                                  component=COMP, inputs=registry,
                                  inherited_inputs={'RV4':'Krasner countability of finite local extensions and compact Hausdorff Baire theorem; the required matrix adaptation is proved in SX7.'}))
dump('input_registry.json', dict(schema='rh-component-inputs/1', artifact_version='0.29', component=COMP,
                                 incoming_claims=external, theorem_hypotheses=hyp,
                                 classical_input_registry=COMP+'/classical_inputs.json',
                                 principle='Every original tower and fixed iota is given before any seed or coefficient-extension choice. Classical theorems are matched individually, with no HypothesesH-prime or RankN package retained.'))
dump('remaining_inputs.json', dict(schema='rh-component-remaining-inputs/1', artifact_version='0.29', component=COMP,
                                   endpoint='SeedIIAlt', missing_suppliers_inside_endpoint_proof=[],
                                   original_endpoint_hypotheses=hyp['SX1'],
                                   classical_inputs=[r['id'] for r in registry],
                                   independent_frontier=['SeedIVAlt','PMExAlt and its actual modular-support producer','ImageDense and the other count branches'],
                                   bypassed_not_promoted=["HypothesesH'",'RankN','full general MixSeedP','full general IndAutLP'],
                                   no_case_three_seed_claim=True))
dump('closure.json', dict(schema='rh-component-closure/1', artifact_version='0.29', component=COMP,
                           main_tex_sha256=sha(main), provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
                           claim_ids=list(titles), final_claims=['SX8'], literal_endpoints={'SeedIIAlt':'SX8'},
                           complete_chains=[
                               {'path':['SX1','SX2','SX3'],'conclusion':'Actual mixed rank-two cuspidal ordinary Galois representation, all local types and exact normalization'},
                               {'path':['SX3','SX4','SX5'],'conclusion':'Actual induced symplectic pair with original residual entries, all local flags and exact weights'},
                               {'path':['SX1','SX3','SX4','SX6'],'conclusion':'Exact cyclotomic irreducibility and actual rank-four cuspidal witness with one all-place strict window'},
                               {'path':['SX5','SX6','SX7','SX8'],'conclusion':'Full literal SeedIIAlt over one finite coefficient extension of the original c'},
                           ],
                           retained_original_data=['Omega','ell','c','D','T','F,K,L','pr','g0','all original valuations and frames','fixed iota'],
                           no_remaining_bespoke_supplier_in_literal_SeedIIAlt_proof=True,
                           actual_automorphic_witness_constructed=True,
                           coefficient_return='Closed-subgroup Baire capture for the actual continuous matrix homomorphism plus finitely many local matrices; exact injective-map descent.',
                           important_normalizations=['geometric nebentype xi has arithmetic avatar xi^-1','r=chi^k r_f^vee','pi0=pi_f |det|^((k+1)/2)','Pi=AI(pi_M)|det|','literal muOf only proved contained in I intersect ker chi'],
                           not_claimed=['SeedIVAlt','general HidaUAlt/HasAut or PMExAlt','blanket HypothesesH-prime or RankN','unconditional image density or counts','RH/GRH completion'],
                           no_lean_replay=True, no_pdf_requested_or_generated=True))
dump('next_targets.json', dict(schema='rh-next-targets/1', artifact_version='0.29', component=COMP,
                               completed=['literal SeedIIAlt'],
                               targets=[{'target':'SeedIVAlt','scope':'Original Ctx3/Four data, one auxiliary split prime and residual pair before every later Dies tower; not attempted in this component.'},
                                        {'target':'PMExAlt','scope':'Actual modular support independent of the case-II seed; parallel QX component.'}],
                               integration='UX12 consumes SX8 only after its original tower and iota have already been chosen.'))
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' -- '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nfile '+s['sha256']+'\nrange '+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
(HERE/'report.txt').write_text(
    'SX1--SX8: complete actual case-II automorphic seed\n'
    '================================================\n'
    'Literal endpoint: SeedIIAlt (SX8). No bespoke supplier remains inside this endpoint proof; the original Ctx2, Ok, Two and Deep premises remain the quantified theorem premises.\n\n'
    'SX2 constructs an actual ordinary cuspidal eigenlift. A mixed weight-one stabilization kills the component-independent standard constants for integral multiplication by a lifted Hasse invariant. The eigenlift occurs in the full holomorphic space. Every Eisenstein alternative is excluded by incompatible unit refinements at the two ell places; multiplication by a form congruent1 is not itself asserted to create a cusp form.\n\n'
    'SX3 uses the primary fixed-central-character Hida control theorem, with exact coordinates and no residual irreducibility assumption. The required r is chi^k r_f^vee, not the raw ordinary representation; the actual automorphic witness is pi_f |det|^((k+1)/2). Global characters and Dirichlet units give irreducibility, the residual-square argument gives strong irreducibility, and conductor/local-type/unitary arguments give all-place principal-series control.\n\n'
    'SX4--SX5 write the entire Ribet lattice, induced mixing basis, alternating form, local flags, correcting character and global inertia-kernel calculation. Literal muOf is treated through the closed commutator power condition and its containment in I intersect ker cyclotomic. SX6 proves the exact infinite cyclotomic irreducibility and constructs the rank-four cusp by cyclic base change and quadratic automorphic induction; one strict local window works at every place. SX7 proves matrix Baire capture and returns every equation and nonzero residual entry to the actual original coefficient extension.\n\n'
    'SeedIVAlt, general modular support, image density and the final counts remain separate. No HypothesesH-prime or RankN package is promoted. Primary references and exact source alternatives are recorded individually.\n\n'
    f'Pin: {PIN}\nMain SHA256: {sha(main)}\nClaims: {len(claims)}; claim anchors: {validation["claim_source_links"]}; boundary anchors: {len(boundaries)}; pinned source files: {len(cache)}.\n'
    'No Lean build or proof PDF. Exact source/proof range validation and two-pass draft TeX validation accompany the component.\n')
dump('source_validation.json', dict(schema='rh-source-validation/1', artifact_version='0.29', component=COMP,
                                    result='PASS', commit=PIN, main_tex_sha256=sha(main),
                                    provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
                                    claim_ids=list(titles), human_proof_ranges_checked=len(claims),
                                    claim_source_ranges_checked=validation['claim_source_links'],
                                    scope_boundary_source_ranges_checked=len(boundaries),
                                    distinct_source_files_checked_against_pinned_git_blobs=len(cache),
                                    incoming_human_proof_ranges_checked=len(external),
                                    checks=['All pinned source files equal Git blobs','Every declaration resolves uniquely','All source and human proof ranges have exact SHA256/line bindings','All claim dependencies are stable IDs; classical leaves and original theorem premises are separate','Incoming RV4 proof range matches its frozen provenance'],
                                    mathematical_verification='Separate independent review; byte checks do not certify mathematics.',
                                    no_lean_replay=True))
print(json.dumps(validation, indent=2))
