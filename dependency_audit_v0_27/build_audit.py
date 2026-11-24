#!/usr/bin/env python3
"""Build v0.27's finite semantic sufficient-condition map and exact source audit."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OLD = WORK / 'dependency_audit_v0_26'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
S = P + 'SymplecticGSp4/'
D = P + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
COMPONENTS = ['symplectic_arithmetic_data', 'symplectic_local_installation',
              'symplectic_model_construction', 'symplectic_model_comparison']
REVIEW_PREFIXES = ('arithmetic_data_', 'symplectic_arithmetic_',
                  'local_installation_', 'symplectic_local_',
                  'model_construction_', 'symplectic_model_',
                  'model_comparison_', 'integration_scope_review')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def walk_anchors(value):
    if isinstance(value, dict):
        if {'path', 'line_start', 'line_end', 'sha256', 'range_sha256', 'url'} <= value.keys():
            yield value
        for child in value.values():
            yield from walk_anchors(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_anchors(child)


def main(repo):
    blobs, source_index, input_index = {}, {}, {}
    proof_checks, component_claims, ledgers = [], {}, {}
    component_manifest_checks = 0

    def file_input(p):
        input_index[str(p.relative_to(WORK))] = {
            'path': str(p.relative_to(WORK)), 'sha256': sha(p.read_bytes()),
            'bytes': p.stat().st_size}

    def blob(path):
        if path not in blobs:
            b = (repo / path).read_bytes()
            assert b == subprocess.check_output(['git', '-C', str(repo), 'show', PIN + ':' + path]), path
            blobs[path] = b
        return blobs[path]

    def verify(a):
        b = blob(a['path'])
        fragment = b''.join(b.splitlines(keepends=True)[a['line_start']-1:a['line_end']])
        assert sha(b) == a['sha256'], a['path']
        assert sha(fragment) == a['range_sha256'], (a['path'], a['line_start'])
        assert PIN in a['url'], a['url']
        source_index[(a['path'], a['line_start'], a['line_end'])] = copy.deepcopy(a)
        return a

    def anchor(path, decl, start=None, end=None):
        b = blob(path)
        lines = b.decode().splitlines()
        if start is None:
            pat = re.compile(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure)\s+' + re.escape(decl) + r'(?=[\s:(])')
            hits = [i+1 for i,t in enumerate(lines) if pat.match(t)]
            assert len(hits) == 1, (path, decl, hits)
            start = hits[0]
        if end is None:
            end = len(lines)
            for i in range(start, len(lines)):
                if re.match(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[', lines[i]):
                    end = i
                    break
            while end > start and not lines[end-1].strip():
                end -= 1
        fragment = b''.join(b.splitlines(keepends=True)[start-1:end])
        return verify({'path': path, 'declaration': decl, 'line_start': start, 'line_end': end,
            'sha256': sha(b), 'range_sha256': sha(fragment), 'range_bytes': len(fragment),
            'first_line': lines[start-1], 'url': REPO + '/blob/' + PIN + '/' + path + f'#L{start}-L{end}',
            'verified_equal_to_pinned_git_blob': True})

    baseline = read(OLD / 'obligation_map.json')
    assert len(baseline['nodes']) == 96
    old_targets = read(OLD / 'next_targets.json')['targets']
    for a in walk_anchors(old_targets):
        verify(a)
    for a in read(OLD / 'source_anchors.json')['sources']:
        verify(a)
    for a in read(OLD / 'input_manifest.json')['files']:
        p = WORK / a['path']
        assert sha(p.read_bytes()) == a['sha256'], a['path']
    for name in ['obligation_map.json', 'audit.txt', 'input_manifest.json',
                 'next_targets.json', 'source_anchors.json']:
        file_input(OLD / name)

    for name in COMPONENTS:
        directory = WORK / name
        ledger = read(directory / 'provenance.json')
        ledgers[name] = ledger
        expected = ledger.get('main_tex_sha256', ledger.get('validation', {}).get('main_tex_sha256'))
        assert sha((directory / 'main.tex').read_bytes()) == expected, name
        component_claims[name] = [c['id'] for c in ledger['claims']]
        for claim in ledger['claims']:
            loc = claim.get('proof_location', claim.get('human_proof'))
            assert loc is not None, claim['id']
            b = (WORK / loc['file']).read_bytes()
            fragment = b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
            assert sha(fragment) == loc['sha256'], claim['id']
            proof_checks.append(claim['id'])
        manifest = directory / 'input_manifest.json'
        if manifest.exists():
            for a in read(manifest).get('files', []):
                p = WORK / a['path']
                assert sha(p.read_bytes()) == a['sha256'], a['path']
                component_manifest_checks += 1
                file_input(p)
        for p in sorted(directory.iterdir()):
            if p.is_file() and (p.suffix in {'.json', '.tex', '.py'} or p.name in {'report.txt', 'report.md', 'source_locators.txt', 'README.md'}):
                file_input(p)
                if p.suffix == '.json':
                    for a in walk_anchors(read(p)):
                        verify(a)

    all_new_claims = {c for group in component_claims.values() for c in group}
    assert len(all_new_claims) == sum(map(len, component_claims.values())) == 38
    for p in sorted((WORK / 'reviews_v0_27').glob('*')):
        downstream = any(s in p.name for s in ('audit', 'coverage', 'package', 'final_scope', 'semantic_scope'))
        mathematical = p.suffix in {'.json', '.txt', '.md'} and p.name.startswith(REVIEW_PREFIXES)
        if p.is_file() and not downstream and mathematical:
            file_input(p)
    for name in ['configure_v0_27.py', 'increment_v0_27.json']:
        p = WORK / name
        if p.exists():
            file_input(p)

    paired_cut = ['Literal SymplecticFourImageDense on the actual Good/OfCase data',
                  'Actual D.AllIrr D.RigidAt on each same constructed datum',
                  'Exact uniform finite catalogue SP-R3']
    native = ['LocalFiniteness', 'LocalTateDuality', 'LocalEulerChar',
              'GlobalFiniteness', 'GlobalEulerChar', 'PoitouTateNormalised']
    retirement = {'DA26-SP-02': (['AX6', 'DX2', 'DX4', 'DX8', 'MX10'],
        'Actual exModel: every original Good D has a concrete Model D. Exact PhiCond, Nums and LocBase are installed on the same D; FP8 and every Model field are supplied. No image, rigidity or catalogue premise remains in this constructor.')}
    updates = {
        'DA26-SP-01': {
            'human_status': 'actual_data_level_safe_constructor_closed_ImageDense_retained',
            'supplied_by': ['AX3', 'AX5', 'AX6', 'AX7', 'AX8', 'AX9', 'AX10'],
            'remaining_human_scope': 'Supply literal SymplecticFourImageDense on each original Good/OfCase D: actual Fin0, NoEnd and one common IsAutQA embedding before all irreducible points. dataEx, facts, levOf, spPtL, level and safe4-prime are complete.',
            'retained_inputs': ['SymplecticFourImageDense; exact sp4In_alt/sp4In0_alt hypotheses remain unless independently supplied.']},
        'DA26-SP-03': {
            'human_status': 'all_actual_G2_internal_comparisons_closed_precise_arithmetic_predicates_retained',
            'supplied_by': [f'PX{i}' for i in range(1,11)] + ['MX10', 'DX6', 'AX6', 'AX8'],
            'remaining_human_scope': 'Supply actual Fin0, NoEnd and D.AllIrr D.RigidAt on each same constructed D. PX closes the source grading, aSmooth/M1-M4, two-sided point lifting/irreducibility, exact trace and conjugacy-to-orbit comparisons. Fin0/NoEnd come from retained ImageDense; actual irreducible rigidity remains.',
            'retained_inputs': ['PX-R1: actual D.Fin0', 'PX-R2: actual D.NoEnd', 'PX-R3: actual D.AllIrr D.RigidAt'],
            'guard_note': 'The trace nonvanishing antecedent is supplied by the catalogue/prime selection in the paired join, not assumed as a model-construction input.'},
        'DA26-SP-04': {
            'human_status': 'native_finite_fields_supplied_whole_period_ring_record_unpromoted_and_bypassed_for_Model',
            'supplied_by': ['DX1', 'DX2', 'DX3', 'DX4', 'DX6', 'DX8', 'LK2', 'LK3', 'LK4', 'LD2', 'LD3'],
            'supplied_parts': native + ['LocalFinitenessK/LocalTateDualityK/LocalEulerCharK', 'UnramifiedOrthogonality', 'Literal GreenbergWiles with its original odd-prime antecedent', 'Direct actual PhiCond/Nums/LocBase'],
            'remaining_human_scope': 'Whole CohomologyHyp remains unproved: the remaining record field is loc.bk, the full Published.BlochKatoLocal predicate. All six finite LocalPublished fields and pt/gf/ge/uo/gw are supplied by LK/DX/LD. The selected Model and internal comparison bypass the whole record; source image/rigidity producers can still need its actual period-ring applications.',
            'retained_inputs': ['Exact remaining loc.bk = GlobalTheory.Published.BlochKatoLocal, with its original full period-ring/cohomology scope; no blanket inference from finite duality or rational charts.']},
        'DA26-SP-06': {
            'human_status': 'actual_rigidity_producer_retained_internal_tangent_to_M4_comparison_closed',
            'supplied_by': ['PX9', 'PX10', 'AX7', 'AX8', 'AX9'],
            'remaining_human_scope': 'Prove actual D.AllIrr D.RigidAt on the original constructed D. The source rigSp4_alt route retains its UnramifiedInputs, local deformation-to-Bloch-Kato/tanBK comparison and global AdjointLiftingTheorem joins. PX9 proves only the implication from actual rigidity to M4.',
            'retained_inputs': ['Actual same-D irreducible rigidity', 'Exact source local Hodge/Bloch-Kato and global adjoint producer hypotheses'],
            'not_inferred': 'RigiditySymplecticFour is not silently equated with or assumed to instantiate the actual rigidity predicate without its source hypotheses and same-D join.'},
        'DA25-HV-04': {
            'human_status': 'actual_ImageDense_supplier_retained_all_data_level_and_Model_construction_supplied',
            'supplied_by': ['AX5', 'AX6', 'AX7', 'AX9', 'AX10', 'DX8', 'MX10'],
            'remaining_human_scope': 'Literal SymplecticFourImageDense: Fin0, NoEnd and one common embedding on every original Good/OfCase datum. The actual G1 construction and actual Model now exist; this deeper automorphic supplier remains.',
            'retained_inputs': ['Exact image-density/automorphy producers sp4In_alt or sp4In0_alt with all original hypotheses.']},
        'DA25-HV-03': {
            'human_status': 'paired_count_full_internal_chain_complete_exact_ImageDense_rigidity_catalogue_cut',
            'supplied_by': ['AX10', 'DX2', 'DX4', 'DX8', 'MX10', 'PX10', 'SP8', 'SP9', 'SP10'],
            'remaining_human_scope': 'Actual CountII and CountIII remain conditional only on the selected route\'s exact ImageDense, actual same-D irreducible rigidity and uniform SP catalogue. All G1 data/level/safe, Model construction, local installations and internal G2 comparisons are supplied.',
            'retained_inputs': paired_cut},
        'DA25-HV-08': {
            'human_status': 'native_finite_duality_Euler_premises_supplied_actual_CountV_host_chain_retained',
            'supplied_by': ['SP1', 'SP6', 'DX1'],
            'supplied_parts': ['LemmaMprime', 'LemmaM'] + native,
            'remaining_human_scope': 'Full actual large-conductor CountV on its original host/frame, marked point and universal ring: ThmS6_s, HostVanE, HostXpp, HostRigid_s, HostNumber_s and their arithmetic model/automorphic comparisons. DX1 now supplies the identically quantified native finite premises; CountVs is not CountV.',
            'retained_inputs': ['ThmS6_s', 'HostVanE', 'HostXpp', 'HostRigid_s', 'HostNumber_s', 'Actual original host/frame/model and normalized coefficient comparisons']},
        'DA-next-01-b': {
            'human_status': 'PointHV_assembly_closed_four_actual_counts_retained_paired_cut_narrowed',
            'supplied_by': ['HV10', 'TW8', 'OB8', 'AX10', 'DX8', 'MX10', 'PX10'],
            'remaining_human_scope': 'Actual CountI, CountII, CountIII and CountV on unchanged hosts and uniform quantifiers. CountII/III now reduce to exact ImageDense, same-D irreducible rigidity and catalogue. Full four-count-to-PointHV and downstream window assembly remain supplied.',
            'retained_inputs': ['Actual CountI', 'Actual CountV'] + paired_cut}}
    for tid, name in [('DA24-HV-02', 'CountII'), ('DA24-HV-03', 'CountIII')]:
        updates[tid] = {
            'human_status': 'actual_count_retained_internal_model_and_comparison_chain_complete',
            'supplied_by': ['AX10', 'DX8', 'MX10', 'PX10', 'SP10'],
            'remaining_human_scope': 'Literal ' + name + ' with the original uniform host/character/coefficient quantifiers. The selected paired route now retains exactly ImageDense, actual same-D irreducible rigidity and the uniform SP catalogue.',
            'retained_inputs': paired_cut}
    updates['DA24-HV-04'] = copy.deepcopy(updates['DA25-HV-08'])

    targets, retired = [], []
    for old in old_targets:
        q = copy.deepcopy(old)
        q.setdefault('history', []).append({'version': '0.26', 'snapshot': copy.deepcopy(old)})
        if q['id'] in retirement:
            suppliers, scope = retirement[q['id']]
            q.update(status='safe_to_retire_in_stated_scope', supplied_by=suppliers, closed_scope=scope)
            retired.append(q)
        else:
            q.update(updates.get(q['id'], {}))
            targets.append(q)

    image = read(WORK / 'symplectic_arithmetic_data' / 'next_targets.json')['targets'][0]
    rigidity_sources = [anchor(S+'DecompSigmaOrd.lean', d) for d in ['Fin0', 'NoEnd', 'AllIrr', 'RigidAt']]
    rigidity_sources += [anchor(D+'RigEnd3.lean', 'RigiditySymplecticFour'),
                         anchor(D+'RigSp4.lean', 'UpperTheory.V.Th.rigSp4_alt'),
                         anchor(S+'TbTriDiag.lean', 'UpperTheory.V.GradeZeroInterpolatingElement.tanBK')]
    q = copy.deepcopy(rigidity_sources[3])
    q.update(id='DA27-SP-01', work_package='actual_same_datum_irreducible_rigidity', priority_group=1,
             status='human_proof_retained', human_status='exact_actual_rigidity_frontier_after_PX',
             remaining_human_scope='For each original Good/OfCase D constructed in AX5, every irreducible actual EPt and every actual PtIn dual-number lift have derivative [X,r] with X in sp4. Retain the local and global hypotheses of the source producer; PX9/PX10 only consume this actual predicate.',
             retained_inputs=['Exact local tanBK/deformation-to-Bloch-Kato comparison', 'Actual global adjoint lifting and vanishing', 'Same datum, common level and embedding installation'],
             supporting_sources=rigidity_sources,
             downstream='PX9/PX10 actual G2 -> SP10 paired counts -> HV10 PointHV')
    targets.append(q)
    q = copy.deepcopy(image['continuation_sources'][0])
    q.update(id='DA27-SP-02', work_package='actual_symplectic_image_density', priority_group=1,
             status='human_proof_retained', human_status='exact_producer_of_retained_ImageDense',
             remaining_human_scope='Supply all three ImageDense clauses uniformly on the original Good/OfCase data. Complete an actual source image-density producer with its original hypotheses; independent pointwise embeddings or generic automorphy do not suffice.',
             retained_inputs=['Source sp4In_alt retains actual CohomologyHyp, SeedIIAlt, SeedIVAlt and PMExAlt; its FerreroWashington premise is an already recorded classical input. The alternative sp4In0_alt retains actual HypothesesH-prime. Already proved finite pieces do not supply the whole packages.'],
             supporting_sources=[{k:v for k,v in image.items() if k not in {'continuation_sources'}}] + image['continuation_sources'],
             downstream='AX10 complete G1 and PX Fin0/NoEnd -> paired-count chain')
    targets.append(q)
    for a in walk_anchors(targets):
        verify(a)

    unkeyed = anchor('src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean', 'VWinAt')
    global_scope_updates = [{
        'match': {'path': unkeyed['path'], 'declaration': 'UpperTheory.Top.VWinAt'},
        'source': unkeyed,
        'human_status': 'Complete conditional window chain; actual four counts remain with paired arithmetic cut narrowed',
        'remaining_human_scope': 'TW8 and OB8 supply ThmBab and ThmBcFree240; HV10 supplies complete original-field four-count-to-PointHV assembly. CountI/II/III/V remain. The paired II/III route now has actual data, local bases, Model and internal comparisons; its remaining cut is ImageDense, actual same-D irreducible rigidity and exact uniform catalogue. Compatible-host/global-family/gap requirements remain independent.',
        'supplied_by': ['TW8','OB8','HV10','VW3','VW4','QP22','AX10','DX8','MX10','PX10']}]

    m = copy.deepcopy(baseline)
    m.update(artifact_version='0.27', baseline='0.26', previous_map='previous_obligation_map.json',
             increment_integration='AX closes actual G1 data/level/safe construction under exact retained ImageDense; DX installs native finite interfaces and actual PhiCond/Nums/LocBase; MX closes actual Model; PX closes internal G2 under actual Fin0/NoEnd/AllIrr RigidAt. Paired-count cut is ImageDense, same-D irreducible rigidity and catalogue. Four actual counts and the global family/gap/theta/metric/spectral frontier remain.')
    byid = {n['id']: n for n in m['nodes']}
    changed = []

    def update(nid, **kwargs):
        n = byid[nid]
        previous = copy.deepcopy(n)
        n.setdefault('history', []).append({'version': '0.26', 'snapshot': previous})
        n.update(kwargs)
        changed.append(nid)

    def node(nid, title, gate='LEAF', **kwargs):
        assert nid not in byid, nid
        n = {'id':nid, 'title':title, 'gate':gate, 'introduced_in':'0.27', **kwargs}
        m['nodes'].append(n)
        byid[nid] = n

    def registry_ids(component):
        values = read(WORK / component / 'classical_inputs.json')['inputs']
        return list(values) if isinstance(values, dict) else [v['id'] for v in values]

    node('CLASSICAL_ACTUAL_ARITHMETIC', 'Matched finite cyclotomic, local-field, valuation and Henselian inputs',
         status='named_classical_inputs_with_written_actual_data_transfers',
         registry='symplectic_arithmetic_data/classical_inputs.json', input_ids=registry_ids('symplectic_arithmetic_data'))
    node('ACTUAL_RAW_GOOD_DATA', 'Literal original-host dataEx with exact Good and OfCase', gate='AND',
         requires=['COR_X_RESIDUAL_SUPPLIER','CLASSICAL_ACTUAL_ARITHMETIC','EXACT_COEFFICIENT_RETURN'],
         status='human_actual_constructor_complete', claims=['AX1','AX2','AX3','AX4','AX5'],
         premise='Original Omega/host/character/twist and exact nII/nIII parameters. Allowed finite coefficient enlargement supplies roots; original normalized length returns by RV1/SP8. Actual T-subset, residual kernel and both-character BR7 joins are proved.')
    node('ACTUAL_GOOD_FACTS', 'Literal facts and normalization unit for every original Good datum', gate='AND',
         requires=['CLASSICAL_ACTUAL_ARITHMETIC'], status='human_universal_actual_data_consequences_complete', claims=['AX3','AX6'],
         theorem_antecedents=['The original Good D'],
         premise='Adic continuity, open residual kernel, original local inertia weights, ph congruence, cross-block separation, distinct s0 and hEl diagonal-difference unit. No new image, model or rigidity assumption.')
    node('ACTUAL_LEVEL_SAFE_COMPARISON', 'Exact common level, ordinary specialization and safe admissible class', gate='AND',
         requires=['ACTUAL_RAW_GOOD_DATA','ACTUAL_GOOD_FACTS','CLASSICAL_ACTUAL_ARITHMETIC'],
         status='human_same_datum_level_and_local_comparison_complete', claims=['AX7','AX8','AX9'],
         premise='Actual OnComp domain and diagonal O-point; integral divided eigenvalue control; global extensions of finite inertia characters; original multiplier and all-place noncritical branch. One common level precedes the varying points.')
    node('CLASSICAL_NATIVE_FINITE_COHOMOLOGY', 'Precisely matched native finite local/global duality and Euler inputs',
         status='named_classical_inputs_with_written_native_and_rational_transports',
         registry='symplectic_local_installation/classical_inputs.json', input_ids=registry_ids('symplectic_local_installation'))
    node('NATIVE_FINITE_COHOMOLOGY', 'Literal native finite interfaces and normalized finite Poitou-Tate', gate='AND',
         requires=['CLASSICAL_NATIVE_FINITE_COHOMOLOGY','FINITE_DUALITY_SPECIALIZATION','LOCAL_K_INTERFACE_MATCH','COMPACT_FINITE_COHOMOLOGY_TRANSPORT'],
         status='human_interface_matching_complete_in_source_scope', claims=['DX1'],
         supplied_interfaces=native,
         premise='Original finite possibly nonfree modules, decomposition groups, places, coefficients, cup maps and invariants. Rational comparison is derived by actual lattices/limits. Real-place Euler contribution and conditional high-degree vanishing are preserved; no entire period-ring package is inferred.')
    node('ACTUAL_PHI_COND', 'Actual PhiCond on the original global quotient and local groups', gate='AND',
         requires=['ACTUAL_GOOD_FACTS','NATIVE_FINITE_COHOMOLOGY'], status='human_actual_arithmetic_installation_complete', claims=['DX2'],
         theorem_antecedents=['Good D'], premise='Every original open subgroup and coefficient field, with the finite-H1 condition required by FP8; no replacement global quotient.')
    node('ACTUAL_DEFORMATION_NUMERICS', 'Actual Greenberg-Wiles and literal Nums on original residual descents', gate='AND',
         requires=['ACTUAL_GOOD_FACTS','NATIVE_FINITE_COHOMOLOGY','FINITE_DUALITY_SPECIALIZATION'],
         status='human_actual_arithmetic_installation_complete', claims=['DX3','DX4'],
         theorem_antecedents=['Good D'], premise='Odd-prime GreenbergWiles; finite actual framed Ob and exact unquotiented H1c dimension identities at every weight, for every original rb descent and normalization.')
    node('ACTUAL_LOCAL_BASES', 'Literal LocBase and local tangent chart on the original Good datum', gate='AND',
         requires=['ACTUAL_GOOD_FACTS','NATIVE_FINITE_COHOMOLOGY','ACTUAL_PHI_COND','ACTUAL_DEFORMATION_NUMERICS','FRAMED_WEIGHTED_PRESENTATION'],
         status='human_actual_local_constructor_complete', claims=['DX5','DX6','DX7','DX8'],
         theorem_antecedents=['Good D'], premise='Original O/places/groups, ordinary14 and finite-inertial10 variable charts, original local universal lifts and origin. SmoothPt is characteristic-zero rational saturated-cotangent data, not integral formal smoothness. No BlochKatoLocal premise remains for these charts.')
    node('CLASSICAL_ACTUAL_MODEL_ALGEBRA', 'Matched finite-group and complete Noetherian algebra inputs',
         status='named_classical_inputs_with_written_actual_model_transfers',
         registry='symplectic_model_construction/classical_inputs.json', input_ids=registry_ids('symplectic_model_construction'))
    node('ACTUAL_WEIGHTED_MODEL', 'Every original Good datum has its actual full weighted Model', gate='AND',
         requires=['ACTUAL_GOOD_FACTS','ACTUAL_PHI_COND','ACTUAL_DEFORMATION_NUMERICS','ACTUAL_LOCAL_BASES','FRAMED_WEIGHTED_PRESENTATION','CLASSICAL_ACTUAL_MODEL_ALGEBRA'],
         status='human_actual_model_constructor_complete', claims=component_claims['symplectic_model_construction'],
         theorem_antecedents=['Good D'],
         premise='MX10 supplies all literal Model fields on unchanged D. The intrinsic constructor retains PhiCond/Nums/LocBase until DX2/4/8 substitutes them. Actual domain/chart, equations, universal representation, generation and every integral derivation are proved; no automorphy or count is used.')
    node('CLASSICAL_MODEL_COMPARISON_ALGEBRA', 'Matched algebra and finite arithmetic for actual charts and point comparisons',
         status='named_classical_inputs_with_written_point_and_chart_specializations',
         registry='symplectic_model_comparison/classical_inputs.json', input_ids=registry_ids('symplectic_model_comparison'))
    node('ACTUAL_GRADED_MODEL', 'The actual source grading, invariant chart and local M1 comparison', gate='AND',
         requires=['ACTUAL_WEIGHTED_MODEL','ACTUAL_LOCAL_BASES','ACTUAL_GOOD_FACTS','ALGEBRAIC_COEFFICIENT_VANISHING','CLASSICAL_MODEL_COMPARISON_ALGEBRA'],
         status='human_actual_grading_and_chart_installation_complete', claims=['PX1','PX2','PX3','PX4'],
         premise='Source GradedAlgebra Model.gr on the same first-weight-zero algebra, complete degree-zero ring, actual original equations and rational saturated chart; actual point lifts. The finite homogeneous algebra remains distinct from its completion.')
    node('ACTUAL_SAME_DATUM_RIGIDITY', 'Actual irreducible rigidity on each constructed Good/OfCase datum',
         status='major_actual_arithmetic_rigidity_supplier_retained', source_target_ids=['DA27-SP-01','DA26-SP-06'],
         retained_input_registry='symplectic_model_comparison/remaining_inputs.json#PX-R3',
         related_nodes=['SYMPLECTIC_RIGIDITY','SYMPLECTIC_SOURCE_COHOMOLOGY','ACTUAL_LEVEL_SAFE_COMPARISON'],
         premise='D.AllIrr D.RigidAt for each actual D. Every EPt and actual PtIn K[epsilon] lift must have derivative [X,r] with X in sp4. No automatic implication from a named rigidity package, ordinary chart, or finite local duality is asserted.')
    node('ACTUAL_G2_INTERNAL_IMPLICATION', 'All internal model/point/trace/orbit comparisons under their exact arithmetic inputs', gate='AND',
         requires=['ACTUAL_GRADED_MODEL','ACTUAL_LEVEL_SAFE_COMPARISON','NATIVE_FINITE_COHOMOLOGY','ALGEBRAIC_COEFFICIENT_VANISHING','MODEL_SELMER_COTANGENT','LEMMA_M'],
         status='human_complete_internal_G2_implication', claims=component_claims['symplectic_model_comparison'],
         theorem_antecedents=['Actual D.Fin0','Actual D.NoEnd','Actual D.AllIrr D.RigidAt'],
         conclusion_guards=['For D.Ineq(g), the actual trace difference is nonzero at every irreducible EPt; supplied by the catalogue prime selection in the paired join.'],
         premise='Full source grading and M1-M4, two-sided actual point lifting/scaling/irreducibility, original trace, exact second-torus conjugacy and tangent comparison. PX10 gives literal D.Ineq with factor2; its actual arithmetic antecedents are not proved by this implication.')

    update('SYMPLECTIC_DATA_REALIZATION', gate='AND',
           requires=['ACTUAL_RAW_GOOD_DATA','ACTUAL_LEVEL_SAFE_COMPARISON','SYMPLECTIC_IMAGE_DENSITY'],
           status='actual_G1_constructor_complete_conditional_only_on_ImageDense',
           source_target_ids=['DA26-SP-01','DA25-HV-04','DA27-SP-02'],
           claims=['AX10'],
           current_retained_input_registry='symplectic_arithmetic_data/remaining_inputs.json',
           related_nodes=['COR_X_RESIDUAL_SUPPLIER','EXACT_COEFFICIENT_RETURN'],
           premise='The node retains the full G1 meaning. AX supplies dataEx/facts/levOf/spPtL/level/safe4-prime on unchanged actual data; exact ImageDense supplies Fin0, NoEnd and one embedding before every varying irreducible point.')
    update('SYMPLECTIC_IMAGE_DENSITY', source_target_ids=['DA25-HV-04','DA27-SP-02'],
           related_nodes=['SYMPLECTIC_SOURCE_COHOMOLOGY'],
           premise='Literal SymplecticFourImageDense on every original Good/OfCase D: Fin0, NoEnd and one common automorphic embedding. sp4In_alt and sp4In0_alt remain exact producer targets. AX constructs the data and proves level/safe membership; it does not supply image density.')
    update('SYMPLECTIC_MODEL_COMPARISON', gate='AND',
           requires=['ACTUAL_WEIGHTED_MODEL','ACTUAL_G2_INTERNAL_IMPLICATION','SYMPLECTIC_IMAGE_DENSITY','ACTUAL_SAME_DATUM_RIGIDITY'],
           status='actual_model_and_all_internal_G2_comparisons_complete_exact_arithmetic_cut_retained',
           source_target_ids=['DA26-SP-03','DA27-SP-01'], claims=['MX10','PX10'],
           current_retained_input_registry='symplectic_model_comparison/remaining_inputs.json',
           related_nodes=['FRAMED_WEIGHTED_PRESENTATION','RANK_ONE_FINITE_SELMER','ALGEBRAIC_COEFFICIENT_VANISHING'],
           premise='The node still means full G2 on the same D as G1, including source GradedAlgebra Model.gr. DX/MX construct the actual Model; PX closes M1-M4 and actual point/trace/orbit comparisons. ImageDense supplies Fin0/NoEnd, while actual AllIrr RigidAt remains. Whole CohomologyHyp is not a prerequisite of this selected route.')
    update('SYMPLECTIC_SOURCE_COHOMOLOGY',
           status='native_finite_fields_supplied_whole_period_ring_record_retained',
           supplied_parts={'Native finite interfaces':'DX1','Local-K finite interfaces':'LK2/LK3/LK4','GreenbergWiles with original odd-prime antecedent':'DX3','UnramifiedOrthogonality':'LD2','Direct PhiCond/Nums/LocBase':'DX2/DX4/DX8'},
           remaining_record_fields={'loc.bk':'GlobalTheory.Published.BlochKatoLocal'},
           related_nodes=['NATIVE_FINITE_COHOMOLOGY','ACTUAL_PHI_COND','ACTUAL_DEFORMATION_NUMERICS','ACTUAL_LOCAL_BASES'],
           premise='This node still means the entire CohomologyHyp record. All finite fields are supplied; the remaining loc.bk = Published.BlochKatoLocal field is not promoted. DX/MX/PX bypass the whole record for the actual model/internal comparison; exact source image/rigidity producers may still retain its period-ring applications.')
    update('SYMPLECTIC_RIGIDITY', related_nodes=['ACTUAL_SAME_DATUM_RIGIDITY','NATIVE_FINITE_COHOMOLOGY'],
           premise='The node retains the source RigiditySymplecticFour theorem and rigSp4_alt producer. Exact UnramifiedInputs, local tanBK/Bloch-Kato and global adjoint-lifting/vanishing joins remain. PX consumes actual AllIrr RigidAt and does not prove this source producer or its automatic installation.')
    update('SYMPLECTIC_COUNT_CHAIN',
           status='full_internal_paired_chain_complete_exact_ImageDense_rigidity_catalogue_cut',
           source_target_ids=['DA24-HV-02','DA24-HV-03','DA25-HV-03','DA25-HV-04','DA26-SP-01','DA26-SP-03','DA26-SP-05','DA26-SP-06','DA27-SP-01','DA27-SP-02'],
           supplied_inputs={**byid['SYMPLECTIC_COUNT_CHAIN']['supplied_inputs'],
              'Actual data/level/safe':'AX5/AX7/AX8/AX9','Actual local arithmetic inputs':'DX2/DX4/DX8',
              'Actual Model':'MX10','All internal G2 comparisons':'PX10'},
           remaining_bespoke_cut=paired_cut,
           premise='Actual CountII/III meanings and uniform quantifiers are unchanged. AX/DX/MX/PX now supply all G1/G2 construction and internal comparison, with retained exact ImageDense and actual same-D rigidity. SP9/SP10 retain the uniform catalogue and supply the full trace/integer/normalized coefficient join.')
    update('COUNT_V_SUPPLIER',
           status='actual_host_frame_chain_retained_native_finite_and_general_algebra_supplied',
           supplied_general_inputs={**byid['COUNT_V_SUPPLIER']['supplied_general_inputs'], **{v:'DX1' for v in native}},
           related_nodes=['LEMMA_M_PRIME','LEMMA_M','NATIVE_FINITE_COHOMOLOGY'],
           premise='The actual large-conductor CountV host/frame/universal-ring chain, ThmS6_s and HostVanE/Xpp/Rigid_s/Number_s remain. DX1 supplies its identically quantified native finite duality/Euler/PTNormalised premises, but not those arithmetic installations. CountVs is not CountV.')
    update('ACTUAL_POINT_COUNTS',
           status='CountZ_supplied_four_actual_counts_retained_paired_internal_cut_narrowed',
           premise='Original CountI/II/III/V/Z meanings are unchanged. CountZ is complete; I/II/III/V remain. The paired branch now has actual data, local installations, Model and all internal comparisons; its exact ImageDense/actual-rigidity/catalogue suppliers remain. HV count/layer/sum assembly is complete.')
    update('ODD_PLUS_BOUND',
           status='PointHV_assembly_complete_four_counts_retained_paired_internal_chain_supplied',
           remaining_paired_count_cut=paired_cut,
           premise='Literal PointHV still needs the four actual counts. HV10 supplies their full implication. New actual paired-data/model/comparison closures narrow II/III but do not replace them by an implication or alter original field/layer/constant quantifiers.')
    update('COHOMOLOGICAL_WINDOW',
           status='complete_conditional_four_count_window_chain_with_paired_cut_narrowed',
           remaining_paired_count_cut=paired_cut,
           premise='ThmBab and ThmBcFree240 are supplied; PointHV assembly is written. Four actual counts remain, with II/III now reduced to ImageDense, same-D rigidity and catalogue. Original E is common to summands; separate reference-layer models share the fixed pair/window and need not equal E.')
    update('FIXED_PAIR_WINDOWS',
           remaining_paired_count_cut=paired_cut,
           premise='One q,d for every real scale in a late interval, with all original field/conductor and separately quantified layer-model ties. Four actual counts remain; II/III internal construction is supplied. Compatible host and global arithmetic-family/gap requirements are not inferred.')

    for old in baseline['nodes']:
        current = byid[old['id']]
        if old['id'] in changed:
            assert current['history'][-1] == {'version':'0.26','snapshot':old}, old['id']
        else:
            assert current == old, old['id']
    seen, active = set(), set()

    def visit(nid):
        assert nid in byid, nid
        if nid in seen:
            return
        assert nid not in active, ('cycle',nid)
        active.add(nid)
        n = byid[nid]
        assert n['gate'] in {'AND','OR','LEAF'}, nid
        for dep in n.get('requires',[]) + [x for group in n.get('alternatives',[]) for x in group]:
            visit(dep)
        active.remove(nid)
        seen.add(nid)

    for nid in byid:
        visit(nid)
    tids = {t['id'] for t in targets}
    assert len(tids) == len(targets)
    available_claims = all_new_claims | {c for n in baseline['nodes'] for c in n.get('claims',[])}
    for n in m['nodes']:
        for dep in n.get('related_nodes',[]):
            assert dep in byid,dep
        for tid in n.get('source_target_ids',[]):
            assert tid in tids,(n['id'],tid)
        for cid in n.get('claims',[]):
            assert cid in available_claims,(n['id'],cid)
    m['validation'] = {**m.get('validation',{}),'node_count':len(m['nodes']),
        'node_ids_unique':True,'acyclic':True,'all_edges_resolve':True,
        'all_related_nodes_resolve':True,'all_current_target_ids_resolve':True,
        'all_current_claim_ids_resolve':True,'historical_node_meanings_preserved':True,
        'historical_node_count':len(baseline['nodes']),'changed_historical_nodes':changed,
        'complete_previous_records_preserved':True,'historical_validation_preserved_in_previous_map':True,
        'unproved_generic_model_implication_inserted':False,
        'whole_CohomologyHyp_or_LocalPublished_promoted':False,
        'actual_rigidity_distinguished_from_generic_source_rigidity':True}
    anchors = sorted(source_index.values(), key=lambda a:(a['path'],a['line_start'],a['line_end']))
    source_obj = {'commit':PIN,'sources':anchors,'source_files':len(blobs),'source_ranges':len(anchors)}
    source_bytes = (json.dumps(source_obj,ensure_ascii=False,indent=2)+'\n').encode()
    m['source_manifest_sha256'] = sha(source_bytes)
    (HERE/'previous_obligation_map.json').write_bytes((OLD/'obligation_map.json').read_bytes())
    write('obligation_map.json',m)
    write('source_anchors.json',source_obj)
    write('next_targets.json',{'targets':targets})
    write('retirement_candidates.json',{'targets':retired})
    write('target_scope_updates.json',updates)
    write('global_branch_scope_updates.json',{'updates':global_scope_updates})
    write('symplectic_frontier_sources.json',{'ImageDense':image,'actual_rigidity':rigidity_sources,
          'paired_count_remaining_cut':paired_cut,'related_nodes_are_not_proof_edges':True})
    write('input_manifest.json',{'artifact_version':'0.27','components':COMPONENTS,
          'review_input_policy':'Only mathematical component reviews/source validations and integration-scope reviews. Downstream semantic/final-scope/coverage/package/audit outputs are excluded to avoid circular hash dependencies.',
          'files':[input_index[k] for k in sorted(input_index)]})
    write('summary.json',{'artifact_version':'0.27','new_claim_ids':[],
        'increment_supplier_claims':component_claims,'retirement_candidate_ids':list(retirement),
        'retirement_count':len(retired),'historical_nodes_preserved':len(baseline['nodes']),
        'map_node_count':len(m['nodes']),'changed_historical_node_ids':changed,
        'remaining_counts':['CountI','CountII','CountIII','CountV'],
        'supplied_counts':{'CountZ':'CZ6','CountVs':'HV5','CountIV':'HV6'},
        'remaining_count_assembly':False,'paired_count_remaining_cut':paired_cut,
        'whole_CohomologyHyp_required_for_selected_actual_Model_route':False,
        'whole_CohomologyHyp_promoted':False,
        'not_globally_closed':['RH','Dirichlet GRH','PointHV','Actual CountI/II/III/V',
          'SymplecticFourImageDense','Actual same-D irreducible rigidity','Uniform automorphic catalogue',
          'Whole LocalPublishedTheorems/BlochKatoLocal/CohomologyHyp',
          'Actual-family LinkN','Actual compatible family/DesignExists/HostExW',
          'Theta/type/rank/metric/spectral joins','Final arithmetic gap/gain']})
    write('verification.json',{'artifact_version':'0.27','source_commit':PIN,
        'source_files_checked':len(blobs),'source_ranges_indexed':len(anchors),
        'all_cited_source_files_equal_pinned_git_blobs':True,'all_source_range_hashes_verified':True,
        'new_component_proof_ranges_verified':len(proof_checks),
        'all_component_main_and_proof_hashes_match':True,
        'available_component_manifest_entries_verified':component_manifest_checks,
        'previous_release_input_manifest_verified':True,'historical_node_ids_preserved':True,
        'complete_changed_node_snapshots_verified':True,'historical_snapshot_byte_identical':True,
        'sufficient_condition_graph_acyclic':True,'current_validation_node_count':len(m['nodes']),
        'historical_validation_not_edited':True,'all_related_and_target_ids_resolve':True,
        'prior_files_modified':False,'root_targets_modified':False,'new_claim_ids':[],
        'Lean_kernel_replay_run':False,'formal_transitive_Lean_dependency_audit':False,
        'audit_txt_sha256':sha((HERE/'audit.txt').read_bytes()),
        'scope':'Human semantic sufficient-condition audit. Integrity and graph checks validate provenance/bookkeeping, not mathematical proofs.'})
    print(json.dumps({'retirements':len(retired),'targets':len(targets),'source_files':len(blobs),
          'source_ranges':len(anchors),'proof_ranges':len(proof_checks),
          'historical_nodes':len(baseline['nodes']),'map_nodes':len(m['nodes'])},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=WORK.parent/'lean-source')
    main(parser.parse_args().repo.resolve())
