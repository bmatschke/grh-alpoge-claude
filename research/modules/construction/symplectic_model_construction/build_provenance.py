#!/usr/bin/env python3
"""Bind MX1--MX10, every literal Model field, and exact incoming interfaces."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
REPO = parser.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
SG = AV + 'SymplecticGSp4/'
CA = AV + 'CommutativeAlgebra/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}


def source(path, name, role='Exact pinned definition or proof reconstructed in the stated MX scope'):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if m:
            starts.append((n, m.group(1)))
    matched = [(n, s) for n, s in starts if s == name or (name.startswith('@') and s.rsplit('.', 1)[-1] == name[1:])]
    if len(matched) != 1:
        raise ValueError((path, name, matched))
    start, spelling = matched[0]
    end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b''.join(lines[start - 1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw), 'lines': len(lines),
                   'url': f'{URL}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{URL}/blob/{PIN}/{path}#L{start}-L{end}', 'role': role,
            'verified_equal_to_pinned_git_blob': True}


spec = {
 'MX1': {
  SG+'DecompSigmaOrd.lean': ['Raw', 'Psi', 'al', 'th', 'ps', 'r0', 'rbar', 'Gp', 'Ip', 'Sb', 'T', 'UnrT', 'Good', 'condL', 'condP', 'hEl', 'Nrm', 'Mult', 'OnComp'],
  SG+'ResidueCharMemLevelPrimes.lean': ['w4', 'J4', 'form', 'SP', 'Gam', 'frame', 'LocEqs'],
  SG+'Descend.lean': ['closed_ker', 'exists_down', 'normalises', 'kill_iff', '@descend'],
  SG+'LMemMax.lean': ['@facts'],
  SG+'ExDefs.lean': ['isGSp_map', 'prj_map', 'ord_map', 'condL_map', 'condP_map', 'mult_map', 'unr_map', 'hEl_map', 'nrm_map', 'Raw.LocEqs.map'],
 },
 'MX2': {
  CA+'FramedTwoCoboundaries.lean': ['IsLocCond', 'killCond'],
  SG+'LocCondQ.lean': ['dec_unr', 'norm_diag', 'loc_diag', '@locCondQ'],
  CA+'KillLoc.lean': ['ker_inf', 'hh_section', 'cob_ker', '@kill_loc'],
  CA+'ExistsLocallyConstantDOneEqCocycleOfTameInertia.lean': ['second_cohomology_transfer', 'cocycle_sequence_periodic', '@exists_locallyConstant_dOne_eq_cocycle_of_tame_inertia'],
 },
 'MX3': {
  CA+'FramedTwoCoboundaries.lean': ['FormData', 'Normalises', 'Frame', 'H1c', 'Ob', 'IsUnivFramed', 'IsRelPres', 'LemmaP'],
  CA+'FramedOrigin.lean': ['@framed_origin'],
  SG+'ResidueCharMemLevelPrimes.lean': ['Nums', 'LocBase'],
  SG+'ExDefs.lean': ['IsFr', 'Fr'],
  SG+'NonemptyLocalFramesOfGoodData.lean': ['z_mem_max', '@nonempty_local_frames_of_good_data'],
 },
 'MX4': {
  CA+'ResMapBijective.lean': ['IsCO', 'IsHomog', 'WPres', 'HasOrigin', 'PtDer', 'HasWt', 'satSq'],
  CA+'OrbitVanishingLocal.lean': ['IsChart', 'SmoothPt'],
  CA+'KerPow.lean': ['exists_order', 'A_fin', 'A_sum', '@ker_pow'],
  CA+'ChartGr.lean': ['@chart_gr'],
  CA+'ChartAdd.lean': ['@chart_add'],
  SG+'SmoothPtPartOfSmoothPtAssociatedGraded.lean': ['extend', '@smoothPt_part_of_smoothPt_associatedGraded'],
  SG+'NonemptyCoverOfRelativePresentationSmoothPt.lean': ['rp_ext', 'rp_ex', 'rp_lift', 'rp_homog', '@nonempty_cover_of_relative_presentation_smoothPt'],
  SG+'ExDefs.lean': ['Cover'],
 },
 'MX5': {
  CA+'ChartCut.lean': ['cc_ift', 'cc_pivot', 'cc_series', '@chart_cut'],
  CA+'ChartKer.lean': ['homog_ker', '@chart_ker'],
  CA+'ChartGr.lean': ['@chart_gr'],
  SG+'ExistsSmoothQuotientByWeightedEquations.lean': ['indep', 'der_desc', '@exists_smooth_quotient_by_weighted_equations'],
 },
 'MX6': {
  SG+'MapRepApply.lean': ['adj', 'adj_apply', 'IsGSp', 'sp4', 'IsBlock'],
  SG+'ExModel.lean': ['p6', 'p4', 'rootVec', 'tOdd', 'ph_ne', 'tOdd_ind', 'al_one', 'nrm'],
  SG+'ExistsPointDerivationFramedCommutatorTangent.lean': ['dm_gsp', 'dm_lift', '@exists_pointDerivation_framed_commutator_tangent'],
  SG+'ExistsLocalFirstOrderLifts.lean': ['gsp_conj', 'ord_cj', '@exists_local_first_order_lifts'],
  SG+'SixBlock.lean': ['@sixBlock_unit', '@sixBlock'],
 },
 'MX7': {
  SG+'ExModel.lean': ['tower', 'dims', 'enum', 'cnt', 'sEq', 'wEq', 'sEq_mem', 'loc_eq', '@exModel'],
  SG+'EntryMem.lean': ['tDims', 'Model'],
  SG+'DecompSigmaOrd.lean': ['OnComp', 'IsPt'],
 },
 'MX8': {
  CA+'ResMapBijective.lean': ['Lift.Generates'],
  SG+'ExDefs.lean': ['Fr'],
  SG+'ExModel.lean': ['isFr_map', 'gen'],
 },
 'MX9': {
  SG+'EntryMem.lean': ['ShaCoc', 'Model'],
  SG+'MapRepApply.lean': ['Xm'],
  SG+'ExistsQuotientDerivationOfShaCocycle.lean': ['tw_mul', 'tw_gsp', 'Xm_sp', 'twRep', 'main', '@exists_quotientDerivation_of_shaCocycle'],
  SG+'SmoothPtWeightedPresentationOfPointDerivations.lean': ['sep_char', 'core', 'ex_unit', '@smoothPt_weightedPresentation_of_pointDerivations'],
  SG+'ExistsLocalFirstOrderLifts.lean': ['dU_conj', '@exists_local_first_order_lifts'],
  SG+'ExModel.lean': ['tower', 'Xm_wt', 'hEl_apply', '@exModel'],
 },
 'MX10': {
  SG+'ResidueCharMemLevelPrimes.lean': ['Nums', 'LocBase'],
  CA+'ResMapBijective.lean': ['PhiCond'],
  CA+'FramedTwoCoboundaries.lean': ['LemmaP'],
  SG+'EntryMem.lean': ['Model'],
  SG+'ExModel.lean': ['@exModel'],
 },
}

titles = {
 'MX1': 'Original global quotient, diagonal base point, and polynomial local-condition transport',
 'MX2': 'All five kill-inertia local-condition axioms, including continuous small-extension lifting',
 'MX3': 'Actual universal framed deformation ring, exact relation counts, and original augmentation',
 'MX4': 'Finite-jet graded comparison and complete relative smooth cover with integral derivation lifting',
 'MX5': 'Independent homogeneous cuts, actual domain quotient, and preservation of every integral point derivation',
 'MX6': 'Six root cuts, independent framed tangent directions, and exact symplectic normalization',
 'MX7': 'Actual rings R and S, all three equation lists, exact tDims, and original IsPt witnesses',
 'MX8': 'Literal Lift.Generates on every complete Noetherian coefficient target',
 'MX9': 'Full integral Model.der for every original ShaCoc and every entry preimage',
 'MX10': 'Literal exModel constructor and substitution of the exact installed arithmetic suppliers',
}

deps = {
 'MX1': ['AX6', 'KB6', 'FP1'],
 'MX2': ['MX1', 'FP4', 'KB6'],
 'MX3': ['MX1', 'MX2', 'FP8'],
 'MX4': ['MX3', 'FP1'],
 'MX5': ['MX4'],
 'MX6': ['MX1', 'MX3', 'AX6'],
 'MX7': ['MX3', 'MX4', 'MX5', 'MX6'],
 'MX8': ['MX3', 'MX7'],
 'MX9': ['MX1', 'MX3', 'MX4', 'MX5', 'MX6', 'MX7'],
 'MX10': ['MX7', 'MX8', 'MX9', 'DX2', 'DX4', 'DX8'],
}

scopes = {
 'MX1': 'Original Good D and actual LocBase: descend r0 and residual rbar to D.Gam; actual UnrT is equivalent to kill residual-trivial inertia at S minus T after pullback. Preserve multiplier and all original local polynomial equations under coefficient maps. AX6 supplies exact facts; KB6 supplies original-place completion transport.',
 'MX2': 'On each original Gq for q in S minus T, kill Iq intersect ker(rbar) is closed, conjugation invariant, torus invariant, satisfies the exact tangent iff, and lifts across every surjective IsCO map with maximal-ideal-annihilated kernel. No Bloch-Kato or integral local smoothness premise is used.',
 'MX3': 'Good, literal PhiCond D.Gam, D.Nums, actual LocBase, and supplied FP8. Produces every field of Fr D L, with all-target universality, exact H1c/Ob relation multiplicities, original origin, and actual centered-entry relative variables.',
 'MX4': 'Every finite weighted augmented presentation in the stated construction: graded finite-jet comparison in all degrees, exact contraction of augmentation powers, extension/restriction of the source rational cotangent chart. Produces complete Cover from B[[u]], with homogeneous lifting and integral point-derivation lift modulo arbitrary nonzero a.',
 'MX5': 'Any source-chart ring and homogeneous origin-zero cuts separated by integral point derivations. Produces actual IsCO domain quotient with exact weightwise dimension loss and preservation of every O-valued point derivation killing the cuts. No integral formal-smoothness strengthening is made.',
 'MX6': 'On the actual Fr, all 6(b+1) root cuts are separated by actual integral tangent derivations. Exact J signs, six positions and roots. Killing those cuts plus the four stated entries makes every frame I and makes r(ph) lambda-block diagonal over the actual local quotient ring.',
 'MX7': 'Actual constructed R/S: r=1+b+a(-P), r-prime=2+b+a(P), m=2+2b+a(0), exact tDims, exact F/E/Z lengths and weights, kernel generated by all equations. IsPt has actual OnComp witnesses using the same domain R; entry origin equality holds for every preimage.',
 'MX8': 'On the actual final S, any two maps to any IsCO target agreeing on the representation agree everywhere. Local-base and Fr uniqueness plus surjectivity prove literal Lift.Generates.',
 'MX9': 'Every nonzero a and every literal ShaCoc on original Omega/O/D. Constructs an integral derivation on actual domain R of weight -wPs, kills ker(pi) modulo a, and has both prescribed (2,0)/(3,1) values for every preimage. Local coboundary parameters are lifted without dividing gamma-1.',
 'MX10': 'First proves exact Good + PhiCond + Nums + Nonempty LocBase => Nonempty Model with LemmaP supplied by FP8. Then substitutes only DX2, DX4 and DX8 in their original-Good-D scopes. Does not infer image density, rigidity, automorphy, trace catalogue, or counting endpoints from model existence.',
}

inputs = {
 'MX-C1': {
  'kind': 'matched classical local Galois theory',
  'name': 'Finite unramified extensions and decomposition modulo inertia',
  'statement_used': 'For a complete discretely valued field with finite residue field, finite unramified extensions correspond to finite residue extensions; the inertia quotient is the residue Galois group. Passing to compatible finite extensions gives procyclic quotient generated by arithmetic Frobenius.',
  'source': 'J.S.Milne, Algebraic Number Theory, version3.08, Proposition7.50, Corollary7.52, Remark7.53 and subsequent finite-residue discussion, Theorem7.58(a).',
  'url': 'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
  'primary_source_checked': True,
  'matching': 'Used only on the chosen original D.pl(q). KB6 supplies henselization/completion equivalence and inertia/cochain compatibility. Conjugacy of places is used on finite normal extensions and passed through their inverse limit; no new place or field is substituted.',
 },
 'MX-C2': {
  'kind': 'matched classical finite-group cochain filtration',
  'name': 'Hochschild-Serre spectral sequence, finite-normal-subgroup specialization',
  'statement_used': 'For finite G and normal N, group cohomology has the cochain-filtration spectral sequence with E2(p,q)=H^p(G/N,H^q(N,V)). When order(N) is invertible on V, averaging kills all positive q and inflation identifies cohomology with that of G/N on V^N.',
  'source': 'G.Hochschild and J.-P.Serre, Cohomology of group extensions, Trans.Amer.Math.Soc.74(1953),110-134, ChapterII Theorems1-2, especially printed p125.',
  'url': 'https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/hochschild-serre.pdf',
  'primary_source_checked': True,
  'matching': 'MX2 proves the passage through finite continuous cochains and the cyclic H2 vanishing directly. I/N is finite of order prime to ell; coefficients are the exact finite residual-adjoint module tensor the small kernel. No unrelated pro-ell duality or local smoothness theorem is substituted.',
 },
 'MX-C3': {
  'kind': 'matched classical complete Noetherian algebra',
  'name': 'Noetherian formal power series and complete local quotients',
  'statement_used': 'Finite-variable formal power series over a Noetherian ring are Noetherian; a quotient of a complete Noetherian local ring by a proper ideal is complete Noetherian local. Krull intersection is zero for powers of a proper ideal on a finite module over a Noetherian local ring.',
  'source': 'Stacks Project, Lemma10.31.2 tag0306; Lemma10.160.2 tag0325; Lemma10.51.4 tag00IP.',
  'urls': ['https://stacks.math.columbia.edu/tag/0306', 'https://stacks.math.columbia.edu/tag/0325', 'https://stacks.math.columbia.edu/tag/00IP'],
  'primary_source_checked': True,
  'matching': 'Applied to the explicit finite formal-series cover and proper quotients whose origins survive. In MX2 a descending chain of subspaces of the finite small kernel stabilizes, and Krull intersection makes its stable term zero. FP1 already provides the automatic continuity and IsCO conventions.',
 },
 'MX-H1': {
  'kind': 'exact theorem hypothesis, installed by a separate human supplier',
  'name': 'Original PhiCond D.Gam', 'supplier_claim': 'DX2',
  'statement_used': 'For every open subgroup H of the original D.Gam, the set of group homomorphisms H to the multiplicative presentation of the additive group ZMod ell with open kernel is finite, exactly as required by FP8.',
  'matching': 'Kept as an explicit hypothesis of MX3 and MX10 intrinsic constructor; substituted only at MX10 installed endpoint. No inference from a generic global finiteness slogan.',
 },
 'MX-H2': {
  'kind': 'exact theorem hypothesis, installed by a separate human supplier',
  'name': 'Original D.Nums', 'supplier_claim': 'DX4',
  'statement_used': 'For every descended residual representation and normalizer, every weight j has finite framed Ob, finrank Ob=finrank H1c+(2 at0,1 atplus/minus wPs,0 otherwise), and H1c dimension vanishes outside0/plus/minus wPs.',
  'matching': 'The unquotiented H1c and actual framed Ob are used exactly. Equalities produce exact relation lists. Not replaced by a bound on unframed H1/H2.',
 },
 'MX-H3': {
  'kind': 'exact theorem hypothesis, installed by a separate human supplier',
  'name': 'Actual LocBase D', 'supplier_claim': 'DX8',
  'statement_used': 'Actual IsCO ring B with weighted presentation, original local universal lifts on all Gp, source local equations, uniqueness over all IsCO targets, origin r0, exact homogeneous entries, and literal SmoothPt with dimL+card(Sb)*dimP.',
  'matching': 'The rational cotangent chart of SmoothPt is kept distinct from integral formal smoothness. MX4 and MX5 supply all chart/domain transitions explicitly. Every local OnComp uses the same constructed domain and original augmentation.',
 },
}

uses = {
 'MX1': ['MX-C1', 'MX-H3'], 'MX2': ['MX-C1', 'MX-C2', 'MX-C3'],
 'MX3': ['MX-H1', 'MX-H2', 'MX-H3'], 'MX4': ['MX-C3', 'MX-H3'],
 'MX5': ['MX-C3'], 'MX6': [], 'MX7': ['MX-C3'], 'MX8': [],
 'MX9': [], 'MX10': ['MX-H1', 'MX-H2', 'MX-H3'],
}

tex = (HERE / 'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    start = next(n for n, line in enumerate(lines, 1) if line.strip() == ('% BEGIN ' + cid).encode()) + 1
    end = next(n for n, line in enumerate(lines, 1) if line.strip() == ('% END ' + cid).encode()) - 1
    claims.append({'id': cid, 'title': title, 'statement': scopes[cid], 'introduced_in': '0.27',
      'depends_on': deps[cid], 'input_ids': uses[cid],
      'status': 'Complete human proof in the exact stated scope; installed endpoint cites separate exact arithmetic suppliers',
      'mathematical_status': 'closed in its exact quantified scope', 'remaining_bespoke_inputs': [],
      'proof_location': {'file': 'symplectic_model_construction/main.tex', 'paragraph': cid,
        'line_start': start, 'line_end': end, 'label': 'claim:' + cid,
        'sha256': sha(b''.join(lines[start-1:end]))},
      'sources': [source(p,n) for p,names in spec[cid].items() for n in names],
      'source_relation': 'Consolidated human reconstruction with proved simplifications; source pointers alone do not discharge any unexplained supplier.',
      'component_ledger': 'symplectic_model_construction/provenance.json'})

for path, record in files.items():
    blob = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
    if sha(blob) != record['sha256']:
        raise ValueError('Pinned Git blob mismatch: ' + path)

suppliers = [
 {'claims': ['FP1', 'FP4', 'FP8'], 'file': 'framed_deformation_presentation/main.tex',
  'scope': 'Previously closed universal complete-local framing theorem and finite matrix lifts; its arithmetic hypotheses are installed explicitly here.'},
 {'claims': ['KB6'], 'file': 'k_theory_bridge/main.tex',
  'scope': 'Original global decomposition-group and finite-completion/native-local comparison only.'},
 {'claims': ['AX6'], 'file': 'symplectic_arithmetic_data/main.tex',
  'scope': 'Literal facts on the unchanged original Good D, supplied by the concurrent actual-data component.'},
 {'claims': ['DX2', 'DX4', 'DX8'], 'file': 'symplectic_local_installation/main.tex',
  'scope': 'Exact arithmetic installations on original Good D; used only through their stated interfaces.'},
]
for supplier in suppliers:
    if 'file' in supplier:
        supplier['file_sha256'] = sha((HERE.parent / supplier['file']).read_bytes())

fields = [
 {'fields': ['R', 'cR', 'aR', 'coR', 'dR', 'W', 'org'], 'claims': ['MX4', 'MX5', 'MX7']},
 {'fields': ['wt_mem', 'r', "r'", 'm', 'one_le', 'smooth'], 'claims': ['MX6', 'MX7']},
 {'fields': ['F', 'E', 'Z', 'hF', 'hE', 'hZ'], 'claims': ['MX7']},
 {'fields': ['S', 'cS', 'aS', 'coS', 'pi', 'surj', 'ker'], 'claims': ['MX7']},
 {'fields': ['ru', 'pt', 'hom', 'at0'], 'claims': ['MX7']},
 {'fields': ['gen'], 'claims': ['MX8']},
 {'fields': ['der'], 'claims': ['MX9']},
]
result = {'schema': 'rh-human-reconstruction-provenance/1', 'artifact_version': '0.27',
 'date': '2026-11-22', 'repository': URL, 'commit': PIN,
 'component': 'symplectic_model_construction',
 'scope': 'Every field of actual Model D, through the literal intrinsic exModel implication and the exact DX arithmetic installations. No downstream counting or catalogue promotion.',
 'claims': claims, 'source_files': list(files.values()), 'dependency_graph': deps,
 'input_ledger': inputs, 'human_suppliers': suppliers, 'model_field_coverage': fields,
 'retained_frontier': [],
 'validation': {'source_files_checked_against_pinned_git_blobs': len(files),
   'claim_source_links': sum(len(c['sources']) for c in claims),
   'main_tex_sha256': sha(tex), 'human_proof_ranges': len(claims),
   'verification_kind': 'Exact source and proof bytes, followed by independent mathematical review; no kernel replay'}}
(HERE / 'provenance.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
(HERE / 'classical_inputs.json').write_text(json.dumps({'schema': 'rh-classical-input-registry/1',
 'component': 'symplectic_model_construction', 'artifact_version': '0.27',
 'inputs': {k:v for k,v in inputs.items() if k.startswith('MX-C')}}, indent=2, ensure_ascii=False) + '\n')
(HERE / 'input_registry.json').write_text(json.dumps({'schema': 'rh-exact-input-registry/1',
 'component': 'symplectic_model_construction', 'artifact_version': '0.27',
 'inputs': inputs, 'human_suppliers': suppliers,
 'scope_rule': 'MX-H1/H2/H3 are hypotheses of the intrinsic theorem, and their separate DX installations are dependencies of the unconditional-on-Good consequence. No blanket CohomologyHyp is asserted.'}, indent=2, ensure_ascii=False) + '\n')
(HERE / 'source_locators.txt').write_text('\n\n'.join(c['id'] + ' — ' + c['title'] + '\n' +
 '\n'.join(s['declaration'] + '\n' + s['url'] + '\nfile ' + s['sha256'] + '\nrange ' + s['range_sha256'] for s in c['sources']) for c in claims) + '\n')

closure = {'schema': 'rh-dependency-closure/1', 'artifact_version': '0.27',
 'component': 'symplectic_model_construction', 'commit': PIN, 'main_tex_sha256': sha(tex),
 'graph': deps, 'model_field_coverage': fields,
 'closed_endpoints': [
  {'claim': 'MX2', 'literal_interface': 'Actual kill-inertia IsLocCond at every q in S minus T', 'retained_bespoke_inputs': []},
  {'claim': 'MX3', 'literal_interface': 'Nonempty (Fr D L)',
   'quantified_hypotheses': ['Good D', 'PhiCond D.Gam', 'D.Nums', 'actual L:LocBase D'],
   'retained_bespoke_inputs': []},
  {'claim': 'MX10', 'literal_interface': 'Good D and PhiCond D.Gam and D.Nums and Nonempty LocBase D imply Nonempty Model D',
   'equation': 'MX.40', 'supplied_universal_theorem': 'FP8', 'retained_bespoke_inputs': []},
  {'claim': 'MX10', 'literal_interface': 'For every original D, Good D implies Nonempty Model D',
   'equation': 'MX.41', 'arithmetic_installations': ['DX2', 'DX4', 'DX8'], 'retained_bespoke_inputs': []}],
 'same_object_bindings': ['Original Omega and O with its residue map', 'Original residual diagonal representation and all four characters',
  'Original valuation/decomposition/inertia subgroups', 'Original D.Gam quotient and framed local maps',
  'Actual universal B/U, complete cover P, domain R, and final quotient S', 'Original symplectic J and root-matrix signs',
  'Finite homogeneous subalgebra distinct from complete ring', 'Literal saturated rational cotangent chart, without integral smoothness strengthening',
  'Same R witnesses every OnComp local component', 'Every-preimage origin and integral-derivation assertions'],
 'noncircularity': ['MX2 proves the relevant finite H2 vanishing independently of any model or count.',
  'FP8 is a previously closed universal theorem; exact PhiCond/Nums/LocBase hypotheses remain visible before substitution.',
  'MX5 takes the kernel of a separately constructed rational formal chart; it does not assume a desired Model domain or point count.',
  'MX6 tangent directions come from actual dual-number conjugations and two universal properties, before the cuts are imposed.',
  'MX9 descends every integral derivation by saturated cotangent control, before using final S equations modulo a.',
  'MX10 asserts no image/automorphy/rigidity/catalogue or RH/GRH conclusion.'],
 'simplifications': ['Finite-normal-subgroup averaging and cyclic inflation replace the long explicit cochain-transfer calculation.',
  'The supplied local origin proves the diagonal local equations; no extra base-point arithmetic package is required.',
  'Finite Taylor jets prove both graded/full chart transports in one argument.',
  'Homogeneous formal implicit substitution and an image-kernel quotient produce the actual domain while preserving integral derivations.',
  'Two exact universal properties prove generation without asserting unspecified topological density.',
  'Torus character separation proves the exact negative-Psi weight on all local homogeneous pieces.'],
 'not_claimed': ['Entire CohomologyHyp', 'Integral formal smoothness of local deformation rings',
  'First-weight-zero M1-M4 and representation-point/orbit comparison, handled separately by PX',
  'Image density, automorphy, rigidity, finite trace catalogue', 'Unconditional CountII/III or full RH/Dirichlet-GRH', 'Lean kernel replay']}
(HERE / 'closure.json').write_text(json.dumps(closure, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(result['validation'], indent=2))
