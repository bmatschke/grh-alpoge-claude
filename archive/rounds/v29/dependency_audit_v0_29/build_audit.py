#!/usr/bin/env python3
"""Build the v0.29 sufficient-obligation map without changing prior records."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OLD = WORK / 'dependency_audit_v0_28'
ARCHIVE = WORK / 'history/version_0_28'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
D = P + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
COMPONENTS = ['symplectic_universal_arithmetic', 'symplectic_modular_support',
              'symplectic_automorphic_seeds', 'symplectic_promodular_realization',
              'case_two_installation']
REVIEW_PREFIXES = ('universal_arithmetic_', 'symplectic_universal_', 'modular_support_',
                  'symplectic_modular_', 'automorphic_seed_', 'automorphic_seeds_',
                  'symplectic_automorphic_seed', 'seed_', 'promodular_realization_',
                  'symplectic_promodular_', 'case_two_', 'integration_scope_')


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
            hits = [i+1 for i, t in enumerate(lines) if pat.match(t)]
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
            'first_line': lines[start-1],
            'url': REPO + '/blob/' + PIN + '/' + path + f'#L{start}-L{end}',
            'verified_equal_to_pinned_git_blob': True})

    baseline = read(OLD / 'obligation_map.json')
    assert len(baseline['nodes']) == 129
    old_targets = read(OLD / 'next_targets.json')['targets']
    for a in walk_anchors(old_targets):
        verify(a)
    for a in read(OLD / 'source_anchors.json')['sources']:
        verify(a)
    for a in read(OLD / 'input_manifest.json')['files']:
        assert sha((WORK / a['path']).read_bytes()) == a['sha256'], a['path']
    for name in ['obligation_map.json', 'audit.txt', 'input_manifest.json',
                 'next_targets.json', 'source_anchors.json']:
        file_input(OLD / name)
    prior_ledger = read(ARCHIVE / 'provenance.json')
    file_input(ARCHIVE / 'provenance.json')

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
            if p.is_file() and (p.suffix in {'.json', '.tex', '.py'} or p.name in {'report.txt', 'report.md', 'source_locators.txt', 'README.md', 'README.txt'}):
                file_input(p)
                if p.suffix == '.json':
                    for a in walk_anchors(read(p)):
                        verify(a)

    all_new_claims = {c for group in component_claims.values() for c in group}
    assert len(all_new_claims) == sum(map(len, component_claims.values())) == 41
    supplementary = WORK / 'ordinary_support_dependency_audit'
    support_audit = read(supplementary / 'audit.json')
    for p in sorted(supplementary.iterdir()):
        if p.is_file() and p.suffix in {'.json', '.txt', '.py'}:
            file_input(p)
            if p.suffix == '.json':
                for a in walk_anchors(read(p)):
                    verify(a)
    for p in sorted((WORK / 'reviews_v0_29').glob('*')):
        downstream = p.name.startswith(('audit_', 'coverage_', 'package_', 'final_scope_',
                                        'semantic_scope_', 'release_preservation_'))
        mathematical = p.suffix in {'.json', '.txt', '.md'} and (
            p.name.startswith(REVIEW_PREFIXES) or
            p.name == 'ordinary_support_core_scope_validation.json')
        if p.is_file() and not downstream and mathematical:
            file_input(p)
    for name in ['configure_v0_29.py', 'increment_v0_29.json']:
        p = WORK / name
        if p.exists():
            file_input(p)

    pm_cut = ['Literal PMExAlt: for each given Fit/Deep tower and fixed iota, one coefficient threshold precedes every later coefficient ring and every actual Space, with fin/p1/seed/pur/aut on the same ideal']
    support_cut = ['For each given Fit/Deep tower and fixed iota, actual rank-four HidaPropsAlt plus P1core on the same two QX Links and same ideals, uniformly after one common coefficient threshold']
    height_cut = ['Actual CountI', 'Actual CountIII', 'Actual CountV'] + pm_cut
    old_height_cut = copy.deepcopy(baseline['current_count_cut'])
    paired_cut = pm_cut + ['Actual CountIII']
    updates = {
        'DA28-SP-01': {
            'human_status': 'five_clause_PMEx_join_complete_actual_rank_four_Hecke_support_producer_retained',
            'supplied_by': [f'KX{i}' for i in range(1, 10)] + [f'QX{i}' for i in range(1, 11)],
            'supplied_scope': 'Actual levels, local reciprocity, weight algebra, Phi, universal Pair rings and maps; literal adjoint lifting; two actual Links and IsPhi; full five-clause PMExAlt join from the exact rank-four ordinary-support input.',
            'remaining_human_scope': 'Construct the actual six-field HidaPropsAlt ideals and P1core on those same ideals for the two QX Links, with a threshold chosen before every later coefficient DVR and every actual universal B/Lambda. QX10 supplies PMExAlt once this input is supplied. Generic finiteness, a seed, a characteristic-zero adjoint theorem, or a different ideal does not supply it.',
            'retained_inputs': support_cut,
            'not_inferred': ['Unconditional PMExAlt', 'All-rank HidaUAlt or ModUAlt', 'P3core', 'Whole HypothesesH-prime or UnramifiedInputs']},
        'DA28-SP-02': {
            'human_status': 'literal_SeedIIAlt_complete_compound_target_retains_SeedIVAlt',
            'supplied_by': ['SX8'],
            'supplied_scope': 'Literal SeedIIAlt for every original Ctx2, Ok/Two/Deep tower and already fixed iota, including the actual finite coefficient extension, residual root entries, local flags and automorphic witness.',
            'remaining_human_scope': 'Literal SeedIVAlt remains: the original Ctx3/Four data, auxiliary w and residual s chosen before every later Dies tower, exact root-entry and coefficient conditions, and the original common-embedding automorphic conclusion. This historical target has both II and IV scope and is not retired.',
            'retained_inputs': ['Literal SeedIVAlt in its original quantifier order'],
            'whole_target_retired': False},
        'DA28-SP-03': {
            'human_status': 'complete_case_II_realization_from_PMExAlt_case_III_realization_retained',
            'supplied_by': ['SX8'] + [f'UX{i}' for i in range(1, 13)] + ['YX1'],
            'supplied_scope': 'For every original Ctx2 and every already fixed iota, PMExAlt supplies the full original ProModAlt witness through actual towers, normalized lattices, three residual lines, spaces, support components and coefficient descent.',
            'remaining_human_scope': 'The complete case-III original-point realization remains, including its SeedIVAlt/tensor tower/rank-four chain/finite coefficient descent and support-reaching argument. PMExAlt itself also remains conditional on its actual support producer. The historical target covers both cases and is not retired.',
            'retained_inputs': pm_cut + ['Literal SeedIVAlt', 'Full original Ctx3 star-point ProModAlt realization at one fixed iota'],
            'whole_target_retired': False},
        'DA25-HV-04': {
            'human_status': 'case_II_full_image_conclusion_from_PMExAlt_full_two_case_ImageDense_retained',
            'supplied_by': ['YX1', 'SX8', 'UX12', 'IX8', 'IX9', 'IX10'],
            'remaining_human_scope': 'YX1 proves Fin0, NoEnd and AllIrr(IsAut4Alt iota) on every original Ctx2 datum from PMExAlt, for every fixed iota. Full SymplecticFourImageDense still includes the original case-III data. Its SeedIVAlt and actual promodular realization, together with the actual support producer, remain.',
            'retained_inputs': support_cut + ['Literal SeedIVAlt and full case-III original-point realization']},
        'DA27-SP-02': {
            'human_status': 'arithmetic_universal_and_case_II_subchains_complete_case_III_and_support_retained',
            'supplied_by': ['BX8', 'TW1', 'KX2', 'KX3', 'KX5', 'KX6', 'KX8', 'QX1', 'QX10', 'SX8', 'UX12', 'YX1'],
            'remaining_human_scope': 'The original sp4In_alt two-case scope is retained. Complete cohomology/Ferrero-Washington, exact universal arithmetic packages, literal adjoint theorem and the actual case-II seed/realization are supplied. The actual rank-four ordinary-support producer and the entire SeedIVAlt/case-III realization remain. Larger printed-source records are not silently installed.',
            'retained_inputs': support_cut + ['Literal SeedIVAlt', 'Complete case-III ProModAlt realization'],
            'bypassed_not_promoted': ['Whole HypothesesH-prime', 'Whole UnramifiedInputs', 'All-rank HidaUAlt or ModUAlt', 'P3core']},
        'DA24-HV-02': {
            'human_status': 'literal_CountII_complete_conditional_only_on_PMExAlt',
            'supplied_by': ['YX2', 'YX1', 'SX8', 'UX12', 'QX10'],
            'remaining_human_scope': 'Supply the literal PMExAlt, or the exact sufficient rank-four HidaPropsAlt/P1core input to QX10. Every original Case-II point, length, exponent, Frobenius, model, rigidity, catalogue and coefficient-return join is then proved. CountII remains conditional on this arithmetic producer.',
            'retained_inputs': pm_cut,
            'sufficient_retained_producer': support_cut},
        'DA24-HV-03': {
            'human_status': 'literal_CountIII_retained_with_existing_ImageDense_route',
            'supplied_by': ['JX1'],
            'remaining_human_scope': 'Actual CountIII remains in the selected YX2 height cut. JX1 still supplies it from full ImageDense. The new case-II realization does not supply the distinct Case-III datum or its seed/support chain.',
            'retained_inputs': ['Actual CountIII, or its sufficient full ImageDense source route']},
        'DA25-HV-03': {
            'human_status': 'paired_count_join_complete_with_added_PMExAlt_and_CountIII_route',
            'supplied_by': ['JX1', 'YX2', 'SP10'],
            'remaining_human_scope': 'The literal paired CountII/CountIII conclusion follows either from full ImageDense by JX1, or from PMExAlt and actual CountIII by YX2. All original paired arithmetic joins remain unchanged; the new single-case proof does not establish CountIII.',
            'retained_inputs': paired_cut,
            'alternative_retained_cut': ['Literal SymplecticFourImageDense']},
        'DA-next-01-b': {
            'human_status': 'height_window_assembly_complete_selected_CountI_CountIII_CountV_PMExAlt_cut',
            'supplied_by': ['YX2', 'JX2', 'HV10', 'TW8', 'OB8', 'VW3', 'VW4'],
            'remaining_human_scope': 'The selected complete height implication retains actual CountI, CountIII, CountV and PMExAlt. YX2 supplies CountII and all HV/TW/OB/VW joins are written. The previous CountI/CountV/full-ImageDense sufficient route remains valid. Window prime-pair guards and the separate final arithmetic family/gap inputs remain.',
            'retained_inputs': height_cut,
            'alternative_retained_cut': old_height_cut},
        'DA26-SP-01': {
            'human_status': 'G1_complete_with_full_ImageDense_route_and_PMExAlt_case_II_specialization',
            'supplied_by': ['AX10', 'JX1', 'YX1', 'YX2'],
            'remaining_human_scope': 'The actual data/Good/OfCase/level/safe constructors remain complete. YX reruns the pointwise G1 proof for every Ctx2 datum using PMExAlt, without asking for full two-case ImageDense. The full G1 target retains literal full ImageDense on the original Good/OfCase data to supply its case-III Fin0/NoEnd/common automorphy. Actual CountIII completes the downstream paired count but does not construct this missing case-III G1 geometry.',
            'retained_inputs': ['Literal full SymplecticFourImageDense on the original Good/OfCase data, including Fin0, NoEnd and one common embedding before all point quantifiers'],
            'case_II_retained_input': pm_cut[0],
            'downstream_paired_count_cut': paired_cut},
        'DA26-SP-03': {
            'human_status': 'G2_complete_with_full_ImageDense_route_and_PMExAlt_case_II_specialization',
            'supplied_by': ['MX10', 'PX10', 'RX6', 'JX1', 'YX1', 'YX2'],
            'remaining_human_scope': 'Every Model/grading/M1-M4/point/trace/orbit step is supplied. YX1 supplies Fin0/NoEnd/automorphy on the same Ctx2 datum from PMExAlt; RX6 gives its actual irreducible rigidity and YX2 completes the count. The full G2 target retains literal full ImageDense on the original Good/OfCase data, supplying case-III Fin0/NoEnd/common automorphy and hence RX6 rigidity. Actual CountIII completes the downstream paired count but does not construct these missing case-III G2 hypotheses.',
            'retained_inputs': ['Literal full SymplecticFourImageDense on the original Good/OfCase data, including Fin0, NoEnd and one common embedding supplying the actual RX6 irreducible-rigidity application'],
            'case_II_retained_input': pm_cut[0],
            'downstream_paired_count_cut': paired_cut},
        'DA27-SP-01': {
            'human_status': 'same_D_rigidity_installed_in_case_II_from_PMExAlt_and_globally_from_ImageDense',
            'supplied_by': ['RX6', 'RX7', 'YX1', 'YX2'],
            'remaining_human_scope': 'RX6 is complete as a universal implication. On Ctx2, YX1 supplies the exact same-D automorphy from PMExAlt at the common fixed iota, and YX2 applies RX6. On the full two-case scope the corresponding Case-III automorphy is still needed. QX1 separately supplies the full literal adjoint lifting theorem, without installing the larger original producer records.',
            'retained_inputs': pm_cut + ['The actual Case-III automorphy for the full two-case application'],
            'not_inferred': ['Whole UnramifiedInputs or HypothesesH-prime']}
    }
    targets = []
    for old in old_targets:
        q = copy.deepcopy(old)
        if q['id'] in updates:
            q.setdefault('history', []).append({'version': '0.28', 'snapshot': copy.deepcopy(old)})
            q.update(updates[q['id']])
        targets.append(q)

    qx_next = read(WORK / 'symplectic_modular_support/next_targets.json')['targets']
    support_sources = list(walk_anchors(support_audit))
    support_sources += [a for t in qx_next for a in t.get('sources', [])]
    def unique_sources(values):
        result = {}
        for a in values:
            verify(a)
            result[(a['path'], a['line_start'], a['line_end'])] = copy.deepcopy(a)
        return list(result.values())

    def add_target(tid, primary, title, scope, retained, sources, priority):
        q = copy.deepcopy(primary)
        q.update(id=tid, title=title, priority_group=priority,
                 status='human_supplier_retained', human_status='precise_remaining_actual_supplier',
                 remaining_human_scope=scope, retained_inputs=retained,
                 supporting_sources=unique_sources(sources))
        targets.append(q)

    add_target('DA29-SP-01', anchor(D + 'PointTheoremBaseObject.lean', 'HidaPropsAlt'),
        'Same-ideal rank-four ordinary Hecke and characteristic-ell support producer',
        'Construct on each of the two actual QX Links an ideal J0 satisfying ring, dense, pt, end1, end2 and twist, and P1core for that very same ideal. Choose the common coefficient threshold before every later coefficient DVR and every actual universal B and weight algebra Lambda, at the already fixed iota. QX10 then supplies PMExAlt and YX2 immediately supplies literal CountII.',
        support_cut, support_sources, 1)
    ux_next = read(WORK / 'symplectic_promodular_realization/next_targets.json')['targets']
    case_three_sources = unique_sources(ux_next[1]['sources'])
    seed4 = anchor(D + 'PromodularityCaseThree.lean', 'SeedIVAlt')
    add_target('DA29-SP-02', seed4,
        'Exact case-IV seed for the remaining case-III realization',
        'Supply the original SeedIVAlt: auxiliary split w and residual pair s before every later permitted Dies tower; exact Four character/residual-root alternative, finite coefficient extension, original local flags, fixed iota and automorphic witness. SX8 supplies only SeedIIAlt.',
        ['Every original SeedIVAlt quantifier and actual constructor'],
        [seed4] + case_three_sources + targets[[t['id'] for t in targets].index('DA28-SP-02')].get('supporting_sources', []), 2)
    add_target('DA29-SP-03', anchor(D + 'PromodularityCaseThreeOfLemmas.lean', 'UpperTheory.V.Cu.promodularity_case_three_of_chain_reduction'),
        'Whole original case-III star-point support realization',
        'Close the actual tensor-factor tower, ChainRankFour, ChainDesc4 and RankFourChainReductionDense supplier chain and then construct literal ProModAlt on every original Ctx3 star point, preserving the chosen iota and all coefficient, support, restriction and inertia maps. This exact second case is not a consequence of UX12.',
        pm_cut + ['Literal SeedIVAlt', 'Original tensor tower, rank-four chain, finite descent and support-reaching producers'],
        case_three_sources + targets[[t['id'] for t in targets].index('DA28-SP-03')].get('supporting_sources', []), 2)
    for a in walk_anchors(targets):
        verify(a)

    unkeyed = anchor('src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean', 'VWinAt')
    global_scope_updates = [{
        'match': {'path': unkeyed['path'], 'declaration': 'UpperTheory.Top.VWinAt'}, 'source': unkeyed,
        'human_status': 'Complete guarded cohomological-window chain with added CountI_CountIII_CountV_PMExAlt sufficient cut',
        'remaining_human_scope': 'YX2 supplies CountII from PMExAlt. The selected height/window route therefore retains actual CountI, CountIII and CountV together with PMExAlt, whose exact rank-four ordinary-support producer remains. The previous JX CountI/CountV/ImageDense route remains valid. TW8 and OB8 supply ThmBab and ThmBcFree240; HV/VW supplies every original-field assembly and fixed-pair rescaling. The original prime-pair, host, independent family and final-gap hypotheses are retained.',
        'retained_inputs': height_cut + ['Established VW/QP prime-pair and host hypotheses where stated'],
        'alternative_retained_cut': old_height_cut,
        'supplied_by': ['YX1', 'YX2', 'SX8', 'UX12', 'QX10', 'JX2', 'TW8', 'OB8', 'HV10', 'VW3', 'VW4', 'QP22']}]

    m = copy.deepcopy(baseline)
    m.update(artifact_version='0.29', baseline='0.28', previous_map='previous_obligation_map.json',
        current_count_cut=height_cut, alternative_count_cuts=[old_height_cut],
        sufficient_support_refinement=['Actual CountI', 'Actual CountIII', 'Actual CountV'] + support_cut,
        conditional_count_suppliers={'CountII': 'YX2 from PMExAlt; JX1 from full ImageDense remains an alternative',
                                    'CountIII': 'JX1 from full ImageDense; retained as an actual input in the selected YX route'},
        increment_integration='KX closes exact universal arithmetic and Pair objects; QX closes literal adjoint lifting and the actual two-Link/five-clause PMEx join from a narrowed same-ideal rank-four Hecke/support input; SX supplies SeedIIAlt; UX supplies the whole actual case-II witness; YX closes PMExAlt -> CountII. Case-IV seed, case-III realization, actual support producer and independent global branches remain.')
    byid = {n['id']: n for n in m['nodes']}
    changed = []

    def update(nid, remove=(), **kwargs):
        assert nid not in changed, nid
        n = byid[nid]
        previous = copy.deepcopy(n)
        n.setdefault('history', []).append({'version': '0.28', 'snapshot': previous})
        for key in remove:
            n.pop(key, None)
        n.update(kwargs)
        changed.append(nid)

    def node(nid, title, gate='LEAF', **kwargs):
        assert nid not in byid, nid
        n = {'id': nid, 'title': title, 'gate': gate, 'introduced_in': '0.29', **kwargs}
        m['nodes'].append(n)
        byid[nid] = n

    def registry_ids(component):
        if component == 'symplectic_universal_arithmetic':
            values = read(WORK / component / 'input_registry.json')['new_classical_theorem_inputs']
        else:
            values = read(WORK / component / 'classical_inputs.json')['inputs']
        return list(values) if isinstance(values, dict) else [v['id'] for v in values]

    node('CLASSICAL_UNIVERSAL_ARITHMETIC', 'Matched local arithmetic and determinant-representability leaves',
        status='named_classical_inputs_with_written_original_object_specializations',
        registry='symplectic_universal_arithmetic/input_registry.json:new_classical_theorem_inputs',
        input_ids=registry_ids('symplectic_universal_arithmetic'))
    node('ACTUAL_TOWER_LEVELS', 'Literal LevEx and LocCFTAll on the original groups', gate='AND',
        requires=['CLASSICAL_UNIVERSAL_ARITHMETIC'], claims=['KX1', 'KX2', 'KX3'],
        status='human_actual_arithmetic_supplier_complete',
        premise='Actual coefficient maps, prescribed global/local decomposition groups, local reciprocity normalization and the exact muOf abelian torsion condition are retained.')
    node('ACTUAL_WEIGHT_ALGEBRA', 'Full actual LamEx with its torsion factors and maps', gate='AND',
        requires=['ACTUAL_TOWER_LEVELS', 'CLASSICAL_UNIVERSAL_ARITHMETIC'], claims=['KX4', 'KX5'],
        status='literal_weight_algebra_supplier_complete',
        premise='The universal characters represent the actual local inertia quotients, with exactly n times the real-field degree variables and all finite torsion factors. No unrelated power-series algebra is substituted.')
    node('ACTUAL_ALL_GROUP_PHI', 'Literal PhiAll for the actual arithmetic groups', gate='AND',
        requires=['SYMPLECTIC_SOURCE_COHOMOLOGY', 'ACTUAL_TOWER_LEVELS', 'CLASSICAL_UNIVERSAL_ARITHMETIC'], claims=['KX6'],
        status='human_actual_group_finiteness_supplier_complete')
    node('UNIVERSAL_ORDINARY_PAIR_RING', 'Literal universal ordinary Pair ring and weight-map triangle', gate='AND',
        requires=['ACTUAL_ALL_GROUP_PHI', 'ACTUAL_WEIGHT_ALGEBRA', 'CLASSICAL_UNIVERSAL_ARITHMETIC'],
        claims=['KX7', 'KX8', 'KX9'], status='complete_universal_theorem_with_original_nonempty_pair_antecedent',
        theorem_antecedents=['Exactly the original existence of one actual Pair over some IsCO coefficient algebra'],
        premise='The determinant is universal on the original coefficient DVR, including nonfree finite coefficient algebras and the source degree-zero conventions. KX preserves the nonempty-Pair antecedent; QX5 supplies an actual Pair when this theorem is used in the selected Links. Pair relations are not the stronger Hecke RingProps.')
    node('CLASSICAL_ORDINARY_SUPPORT_TRANSPORT', 'Matched adjoint, class-field, base-change and local automorphic leaves',
        status='named_primary_classical_inputs_with_written_hypothesis_matching',
        registry='symplectic_modular_support/classical_inputs.json',
        input_ids=registry_ids('symplectic_modular_support'))
    node('FULL_ADJOINT_LIFTING', 'Literal AdjointLiftingTheorem in its original quantified hypotheses', gate='AND',
        requires=['FULL_LOCAL_BLOCH_KATO', 'ALGEBRAIC_COEFFICIENT_VANISHING', 'COMPACT_FINITE_COHOMOLOGY_TRANSPORT', 'CLASSICAL_ORDINARY_SUPPORT_TRANSPORT'],
        claims=['QX1'], status='literal_general_adjoint_theorem_supplied',
        premise='The complete original theorem is proved with its original automorphic, irreducibility, polarization and local hypotheses, matching the polarized adjoint theorem and exact scalar/Bloch-Kato parts. This is not an installation of the entire HypothesesH-prime or UnramifiedInputs record.')
    node('ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT', 'Exact regular-local support implication at arithmetic points', gate='AND',
        requires=['FULL_ADJOINT_LIFTING', 'UNIVERSAL_ORDINARY_PAIR_RING', 'CLASSICAL_ORDINARY_SUPPORT_TRANSPORT'],
        claims=['QX2', 'QX3'], status='human_arithmetic_point_support_implication_complete',
        theorem_antecedents=['The same actual ideal, its ring/density data and the original arithmetic automorphic point conditions'],
        proof_step_reuse={'DX5': 'Only the generic finite algebraic-point and dual-number coefficient-capture argument, explicitly reproved in QX2. No application of the whole Raw/Good LocBase or SmoothPt theorem is made.'},
        premise='QX2 proves its generic complete-local-algebra support criterion directly, including finite point capture. QX3 proves the determinant tangent and all local finite conditions in its own stated hypotheses. The full actual LocBase constructor with different Raw/Good data is not an incoming premise. This gives the characteristic-zero LocZero conclusion, not the characteristic-ell P1core producer.')
    node('ACTUAL_TWO_LINKS', 'Two actual rank-four Links and their exact IsPhi maps', gate='AND',
        requires=['ACTUAL_TOWER_LEVELS', 'ACTUAL_WEIGHT_ALGEBRA', 'UNIVERSAL_ORDINARY_PAIR_RING', 'CLASSICAL_ORDINARY_SUPPORT_TRANSPORT'],
        claims=['QX4', 'QX5'], status='human_actual_link_constructor_complete',
        premise='The two auxiliary places, characters, conjugation/weight equations and coefficient threshold are chosen before every later coefficient ring and Space. The actual determinant Pair supplies KX8 nonemptiness; IsPhi preserves the original maps and residual characteristic, including ell=3.')
    node('ACTUAL_RANK_FOUR_HECKE_SUPPORT', 'One same-ideal rank-four Hecke and characteristic-ell support supplier',
        status='major_actual_arithmetic_producer_retained', source_target_ids=['DA29-SP-01', 'DA28-SP-01'],
        related_nodes=['ACTUAL_TWO_LINKS', 'ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT'],
        premise='For each given Fit/Deep tower and fixed iota, construct the two Links and choose one common coefficient threshold. For each Link, every later coefficient DVR and every actual universal B/Lambda, construct one ideal J0 with ring, dense, pt, end1, end2, twist and P1core simultaneously. The existential same-ideal binding is part of this one obligation; separate existence claims for the fields would not suffice.',
        component_fields=['ring', 'dense', 'pt', 'end1', 'end2', 'twist', 'P1core'],
        registry='symplectic_modular_support/frontier_registry.json',
        supplementary_audit='ordinary_support_dependency_audit/audit.json',
        not_inferred=['P3core', 'All-rank HidaUAlt or ModUAlt', 'A generic finite quotient or unrelated dense set', 'Characteristic-ell support from characteristic-zero adjoint vanishing'])
    node('ACTUAL_PM_TOWER_JOIN', 'Complete same-object five-clause PMExAlt construction from ordinary support', gate='AND',
        requires=['ACTUAL_TWO_LINKS', 'ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT', 'CLASSICAL_ORDINARY_SUPPORT_TRANSPORT'],
        claims=['QX4', 'QX5', 'QX6', 'QX7', 'QX8', 'QX9', 'QX10'],
        status='human_complete_conditional_five_clause_tower_join',
        theorem_antecedents=support_cut,
        proof_step_reuse={'IX9': 'Only the finite-weight-module/IsPhi-to-special-fibre subargument, applied to the actual objects supplied by the retained Hecke package. The complete PROMODULAR_TRANSPORT_JOIN is not invoked and no IX10 witness-existence premise is inserted.'},
        premise='The two pulled-back ideals are added on the actual Space. Integral finite-group-algebra twist transport, actual seed support, NiceI checks, all-place purity and every-quadratic attachment establish fin/p1/seed/pur/aut together. IX9 supplies the exact finite-fibre algebraic implication. P3core is unused. The Hecke sign correction preserves the avatar on the quadratic restriction; no corrected global-avatar equality is asserted.')
    node('CLASSICAL_CASE_TWO_SEED', 'Matched ordinary Eisenstein, Hasse, control and automorphic seed inputs',
        status='named_primary_classical_inputs_with_written_seed_hypothesis_matching',
        registry='symplectic_automorphic_seeds/classical_inputs.json',
        input_ids=registry_ids('symplectic_automorphic_seeds'))
    node('CASE_TWO_SEED', 'Literal SeedIIAlt on every original given tower and fixed embedding', gate='AND',
        requires=['CLASSICAL_CASE_TWO_SEED', 'ACTUAL_GOOD_FACTS', 'ALGEBRAIC_COEFFICIENT_VANISHING'],
        claims=[f'SX{i}' for i in range(1, 9)], status='literal_case_II_seed_supplier_complete',
        theorem_antecedents=['Original Ctx2 datum', 'Original tower with Ok, Two and Deep', 'Already fixed iota'],
        premise='The mixed refinements force cuspidality. Fixed-central weight change, integral Ribet lattice, index-two induction and finite coefficient return give the exact original residual root-entry alternative, flags, multiplier, muOf and AllWin clauses. This does not supply SeedIVAlt.')
    node('CASE_FOUR_SEED', 'Literal SeedIVAlt with its prior auxiliary and later-tower quantifiers',
        status='major_actual_case_IV_seed_supplier_retained', source_target_ids=['DA29-SP-02', 'DA28-SP-02'],
        premise='The original auxiliary split prime and residual pair are chosen before every later Dies tower. The exact root-entry, residual coefficient, Four pattern and common-embedding attachment conditions remain; the different SeedIIAlt scope is not substituted.')
    node('CLASSICAL_PROMODULAR_GEOMETRY', 'Matched connectedness, curve, local-field and completion leaves',
        status='named_classical_inputs_with_complete_actual_space_specializations',
        registry='symplectic_promodular_realization/classical_inputs.json',
        input_ids=registry_ids('symplectic_promodular_realization'))
    node('CASE_TWO_PROMODULAR_JOIN', 'Full actual case-II star-point realization implication', gate='AND',
        requires=['ACTUAL_GOOD_FACTS', 'COR_X_RESIDUAL_SUPPLIER', 'SYMPLECTIC_SOURCE_COHOMOLOGY',
                  'FERRERO_WASHINGTON_MATCH', 'CLASSICAL_FRAMED_ALGEBRA', 'CLASSICAL_PROMODULAR_GEOMETRY'],
        claims=[f'UX{i}' for i in range(1, 13)], status='human_complete_case_II_realization_implication',
        theorem_antecedents=['Literal SeedIIAlt'] + pm_cut,
        proof_step_reuse={'FP1/FP2': 'Finite-entry continuous matrix-lift construction, with the actual quotient-group Phi and normalized split residual representation verified in UX6.',
                         'FP5': 'The torus action, homogeneous cotangent generators and completion argument is used for the explicit UX6 equations; the full local-condition antecedents of FP8 are not asserted.',
                         'FP7': 'The small-extension relation-detection argument is reproduced for the explicitly constructed ordinary cone in UX7; its complete obstruction property is proved there.'},
        not_assumed=['The whole FP8 LemmaP theorem instantiated with unverified local-condition hypotheses'],
        premise='Choose the residual label first, then the initial tower and separating g0, then normalize the lattice at that g0; later towers are compatible fit extensions. Three actual polynomial residual links meet one actual Space. UX6 constructs the exact ring/flags/grading directly and UX7 proves its exact cone obstruction and presentation bound; no full FP8 installation is used. Uniform cohomology precedes later layers and coefficients; trace-fibre bounds give support propagation. Final descent keeps the original valued field and exact residue coefficient ring, which need not itself be a DVR.')
    node('CASE_TWO_PROMODULAR_REALIZATION', 'Actual ProModAlt for every original Ctx2 star pair', gate='AND',
        requires=['CASE_TWO_SEED', 'ACTUAL_FINITE_MODULAR_QUOTIENT', 'CASE_TWO_PROMODULAR_JOIN'],
        claims=['SX8', 'UX12'], status='complete_actual_case_II_witness_conditional_only_on_PMExAlt',
        source_target_ids=['DA28-SP-03'],
        premise='For every original Ctx2 datum and every already fixed iota, construct a witness for every ambient and star KPair, preserving all original fields, maps, restrictions and ordered inertia characters. The PMEx threshold is combined with the seed/link/small-pair thresholds before Space construction. It is not a case-III statement.')
    node('CASE_THREE_PROMODULAR_REALIZATION', 'Actual common-embedding ProModAlt for every original Ctx3 star pair',
        status='major_actual_case_III_realization_retained', source_target_ids=['DA29-SP-03', 'DA28-SP-03'],
        related_nodes=['CASE_FOUR_SEED', 'ACTUAL_FINITE_MODULAR_QUOTIENT'],
        premise='The original tensor-factor tower, rank-four chain, chain descent, chain reduction and support-reaching construction remain. Choose one iota before all ambient/star-pair quantifiers; every actual field, coefficient, restriction and conjugacy condition belongs to the same witness. The source continuation relationships are not asserted completed proof edges.')
    node('CASE_TWO_IMAGE_DENSITY', 'Actual Fin0, NoEnd and common-embedding automorphy on Ctx2', gate='AND',
        requires=['CASE_TWO_PROMODULAR_REALIZATION', 'PROMODULAR_TRANSPORT_JOIN'], claims=['YX1'],
        status='human_complete_case_II_image_conclusion_conditional_on_PMExAlt',
        premise='IX9 applies the actual fin clause in characteristic ell; IX10 gives purity and attachment in characteristic zero; IX8 supplies all three conclusions. YX fixes D and iota first. No full two-case ImageDense premise is used or concluded.')
    node('CASE_TWO_COUNT_SUPPLIER', 'Literal CountII through every original arithmetic and model join', gate='AND',
        requires=['CASE_TWO_IMAGE_DENSITY', 'ACTUAL_RAW_GOOD_DATA', 'ACTUAL_LEVEL_SAFE_COMPARISON',
                  'ACTUAL_WEIGHTED_MODEL', 'ACTUAL_G2_INTERNAL_IMPLICATION', 'SYMPLECTIC_RIGIDITY',
                  'LITERAL_NUMBER_SP4', 'SYMPLECTIC_PAIRED_ASSEMBLY'],
        claims=['YX2'], status='literal_CountII_implication_complete_with_single_PMExAlt_premise',
        source_target_ids=['DA24-HV-02'], theorem_antecedents=pm_cut,
        premise='The original G1 and G2 proofs are rerun pointwise on Ctx2, so a full two-case ImageDense statement is not assumed. Catalogue constants precede the primitive character exponent and every host/ring/twist. Original L,k,p, factor two and strict Selmer injection remain; permitted coefficient enlargement returns normalized length to the original ring.')
    node('COUNT_III_SUPPLIER', 'Actual original CountIII in the selected height route',
        status='actual_count_III_retained', source_target_ids=['DA24-HV-03'],
        related_nodes=['CASE_THREE_PROMODULAR_REALIZATION', 'PAIRED_COUNT_ONE_INPUT_JOIN'],
        premise='Literal CountIII retains its original uniform CountShape quantifiers. Full ImageDense is an already proved sufficient route through JX1. Its separate seed/realization chain remains unclosed; case-II normalization and support do not imply it.')
    node('CASE_TWO_HEIGHT_JOIN', 'Complete added CountI, CountIII, CountV and PMExAlt height route', gate='AND',
        requires=['ACTUAL_POINT_COUNTS', 'POINT_HV_ASSEMBLY'], claims=['YX2'],
        status='human_complete_selected_height_implication', theorem_antecedents=height_cut,
        premise='YX2 supplies CountII; HV10 applies to the unchanged four actual counts, with the established CountVs/IV/Z suppliers. TW/OB/VW propagate the same original-field and reference-layer assembly with all prime-pair guards. No final H-window is inferred.')

    update('ACTUAL_FINITE_MODULAR_QUOTIENT', gate='AND',
        requires=['ACTUAL_PM_TOWER_JOIN', 'ACTUAL_RANK_FOUR_HECKE_SUPPORT'],
        status='complete_PMEx_construction_from_precise_same_ideal_rank_four_support',
        claims=['QX10'], source_target_ids=['DA28-SP-01', 'DA29-SP-01'],
        premise='The node keeps the entire actual modular quotient/Link/support/PMEx meaning. KX and QX supply the universal objects, both Links, IsPhi and all five tower clauses from the exact same-ideal arithmetic support input. That actual rank-four HidaPropsAlt plus P1core producer remains; PMExAlt is not unconditional.')
    update('EXACT_AUTOMORPHIC_SEEDS', gate='AND', requires=['CASE_TWO_SEED', 'CASE_FOUR_SEED'],
        status='SeedIIAlt_complete_SeedIVAlt_retained_in_original_compound_scope', claims=['SX8'],
        source_target_ids=['DA28-SP-02', 'DA29-SP-02'],
        premise='Both original seed meanings are preserved. SX8 supplies the entire case-II seed on the actual given tower and fixed embedding. SeedIVAlt has different auxiliary/tower/root-entry quantifiers and remains. The conjunction is not marked closed.')
    update('ACTUAL_PROMODULAR_REALIZATION', gate='AND',
        requires=['CASE_TWO_PROMODULAR_REALIZATION', 'CASE_THREE_PROMODULAR_REALIZATION'],
        status='case_II_complete_conditional_on_PMExAlt_case_III_retained',
        claims=['UX12', 'YX1'], source_target_ids=['DA28-SP-03', 'DA29-SP-03'],
        premise='The original every-Good/OfCase star-pair meaning is preserved. The full case-II witness is supplied at every already fixed iota. The separate case-III witness remains; its one common iota can also be used for case II because UX is universal in that iota. Every witness retains actual fields, maps, support and local characters.')
    update('SYMPLECTIC_IMAGE_DENSITY',
        status='complete_case_II_image_conclusion_from_PMExAlt_full_case_III_and_support_retained',
        claims=['IX8', 'IX9', 'IX10', 'YX1'],
        source_target_ids=['DA25-HV-04', 'DA27-SP-02', 'DA28-SP-01', 'DA28-SP-02', 'DA28-SP-03', 'DA29-SP-01', 'DA29-SP-02', 'DA29-SP-03'],
        related_nodes=['SYMPLECTIC_SOURCE_COHOMOLOGY', 'ACTUAL_FINITE_MODULAR_QUOTIENT', 'EXACT_AUTOMORPHIC_SEEDS', 'CASE_TWO_IMAGE_DENSITY'],
        premise='The node still means literal Fin0/NoEnd/common-iota automorphy on every original Good/OfCase D. YX1 supplies the complete Ctx2 conclusion from PMExAlt, for every fixed iota. Full ImageDense retains the distinct Ctx3 realization and the actual support producer. Both earlier sufficient global alternatives remain unchanged.')
    update('SYMPLECTIC_RIGIDITY',
        bypassed_not_promoted=['Whole UnramifiedInputs', 'Whole HypothesesH-prime'],
        separately_supplied_general_theorem={'AdjointLiftingTheorem': 'QX1'},
        premise='Literal RigiditySymplecticFour remains supplied by the direct RX6 proof and retains its exact IsAut4Alt antecedent. QX1 now separately supplies the full original adjoint lifting theorem, but not the entire source producer records. Application uses actual automorphy: YX1 provides it on Ctx2 from PMExAlt; Case III remains separate.')
    update('DIRECT_SYMPLECTIC_RIGIDITY',
        premise='The direct RX theorem and its original proof are unchanged: cyclotomic irreducibility, CM restriction, exact polarized adjoint and explicit sp4 projection are complete. The Hecke sign correction preserves the theta*cyclo^3 avatar on the quadratic restriction. The broader UnramifiedInputs record remains uninstalled; QX1 separately supplies AdjointLiftingTheorem without being a new dependency of RX6.')
    update('SYMPLECTIC_DATA_REALIZATION',
        status='full_G1_join_unchanged_case_II_input_supplied_from_PMExAlt',
        related_nodes=['CASE_TWO_IMAGE_DENSITY', 'CASE_TWO_COUNT_SUPPLIER'],
        premise='The original full paired G1 meaning and full-ImageDense sufficient route are unchanged. AX supplies the actual data, level and safe class. YX2 separately reruns the pointwise G1 proof on Ctx2 using YX1 from PMExAlt, without inserting a case-II theorem into a full two-case antecedent.')
    update('SYMPLECTIC_MODEL_COMPARISON',
        status='full_G2_join_unchanged_case_II_inputs_supplied_from_PMExAlt',
        related_nodes=['CASE_TWO_IMAGE_DENSITY', 'CASE_TWO_COUNT_SUPPLIER'],
        premise='The complete same-D Model, grading, M1-M4, points, trace and orbit comparison remains. YX1 supplies Fin0/NoEnd and the common automorphic embedding for each Ctx2 datum; RX6 then supplies its actual rigidity and YX2 reruns G2 there. The broader two-case scope retains its own arithmetic supply.')
    update('ACTUAL_SAME_DATUM_RIGIDITY',
        status='actual_rigidity_from_full_ImageDense_or_case_II_PMExAlt',
        related_nodes=['ACTUAL_TANGENT_BLOCH_KATO', 'CASE_TWO_IMAGE_DENSITY'],
        premise='The full same-D supplier remains RX7 from ImageDense. The new YX2 route applies RX6 directly to each irreducible point on its Ctx2 datum, using the exact automorphy from YX1 and PMExAlt. It retains the original coefficient, completion, flags and multiplier and does not infer Case-III automorphy.')
    update('SYMPLECTIC_COUNT_CHAIN', gate='OR', remove=['requires'],
        alternatives=[['PAIRED_COUNT_ONE_INPUT_JOIN'], ['CASE_TWO_COUNT_SUPPLIER', 'COUNT_III_SUPPLIER']],
        status='complete_paired_join_with_full_ImageDense_and_new_single_case_alternatives',
        claims=['JX1', 'YX2'], source_target_ids=['DA24-HV-02', 'DA24-HV-03', 'DA25-HV-03', 'DA25-HV-04', 'DA27-SP-02'],
        remaining_bespoke_cut=paired_cut, alternative_remaining_cut=['Literal SymplecticFourImageDense'],
        premise='The literal CountII-and-CountIII meaning is unchanged. JX1 supplies both from full ImageDense. The added route combines the complete PMExAlt-to-CountII theorem YX2 with actual CountIII. All original count quantifiers are retained, and neither route asserts unconditional counts.')
    update('ACTUAL_POINT_COUNTS',
        status='CountZ_complete_CountII_from_PMExAlt_actual_I_III_V_retained',
        premise='The original five count meanings are preserved. CountZ is supplied. The selected route obtains CountII from PMExAlt and retains actual I, III and V; the earlier full-ImageDense route to II/III remains. HV supplies the unchanged case/layer/sum assembly.')
    update('ODD_PLUS_BOUND',
        status='complete_PointHV_assembly_with_added_CountI_CountIII_CountV_PMExAlt_cut',
        claims=['HV10', 'JX2', 'YX2'], remaining_actual_inputs=height_cut,
        alternative_remaining_cut=old_height_cut, remaining_paired_count_cut=paired_cut,
        related_nodes=['LEMMA_K_BOUND', 'LOCAL_K_INTERFACE_MATCH', 'ACTUAL_POINT_COUNTS', 'REDUCED_POINT_HV_JOIN', 'CASE_TWO_HEIGHT_JOIN'],
        premise='Literal PointHV and the original assembly remain unchanged. YX2 adds the complete sufficient route from actual I/III/V and PMExAlt. Original E, separately quantified reference-layer models, host, twist cutoff and the order of every uniform constant are retained. The arithmetic antecedents remain.')
    update('COHOMOLOGICAL_WINDOW',
        status='complete_guarded_window_with_added_CountI_CountIII_CountV_PMExAlt_cut',
        claims=['VW3', 'JX2', 'YX2'], remaining_count_cut=height_cut,
        alternative_remaining_cut=old_height_cut, remaining_paired_count_cut=paired_cut,
        premise='TW8 and OB8 supply simultaneous two-primary and odd-minus240. YX2 supplies CountII from PMExAlt and HV/VW assembles the guarded window from I/III/V. Original E is common to the three summands; separately quantified reference layers share the fixed pair/window and need not equal E. Prime-pair guards and independent final H-window/family/gap inputs remain.')
    update('FIXED_PAIR_WINDOWS',
        status='complete_fixed_pair_window_with_added_single_case_sufficient_cut',
        claims=['QP22', 'VW4', 'JX2', 'YX2'], remaining_cohomological_supplier=height_cut,
        alternative_remaining_cut=old_height_cut, remaining_paired_count_cut=paired_cut,
        premise='The same pair works on every real scale in a late interval. The selected added cut is I/III/V/PMExAlt, with the original prime-pair and separate-layer-model ties. Ct=401 still yields cutoff400. Compatible host, global family and final arithmetic gap are independent obligations.')

    for old in baseline['nodes']:
        current = byid[old['id']]
        if old['id'] in changed:
            assert current['history'][-1] == {'version': '0.28', 'snapshot': old}, old['id']
        else:
            assert current == old, old['id']
    seen, active = set(), set()
    def visit(nid):
        assert nid in byid, nid
        if nid in seen:
            return
        assert nid not in active, ('cycle', nid)
        active.add(nid)
        n = byid[nid]
        assert n['gate'] in {'AND', 'OR', 'LEAF'}, nid
        if n['gate'] == 'LEAF':
            assert not n.get('requires') and not n.get('alternatives'), nid
        for dep in n.get('requires', []) + [x for group in n.get('alternatives', []) for x in group]:
            visit(dep)
        active.remove(nid)
        seen.add(nid)
    for nid in byid:
        visit(nid)
    selected_case_ii_nodes = set()
    def select_case_ii(nid):
        if nid in selected_case_ii_nodes:
            return
        selected_case_ii_nodes.add(nid)
        n = byid[nid]
        for dep in n.get('requires', []) + [x for group in n.get('alternatives', []) for x in group]:
            select_case_ii(dep)
    select_case_ii('CASE_TWO_COUNT_SUPPLIER')
    case_ii_open_leaves = sorted(nid for nid in selected_case_ii_nodes
        if byid[nid]['gate'] == 'LEAF' and any(word in byid[nid].get('status', '')
            for word in ('unreconstructed', 'retained', 'unclosed', 'open_')))
    assert case_ii_open_leaves == ['ACTUAL_RANK_FOUR_HECKE_SUPPORT'], case_ii_open_leaves
    assert not selected_case_ii_nodes.intersection({
        'SYMPLECTIC_IMAGE_DENSITY', 'CASE_THREE_PROMODULAR_REALIZATION',
        'CASE_FOUR_SEED', 'COUNT_III_SUPPLIER'})
    tids = {t['id'] for t in targets}
    assert len(tids) == len(targets)
    available_claims = all_new_claims | {c['id'] for c in prior_ledger['claims']}
    for n in m['nodes']:
        for dep in n.get('related_nodes', []):
            assert dep in byid, dep
        for tid in n.get('source_target_ids', []) + n.get('related_source_target_ids', []):
            assert tid in tids, (n['id'], tid)
        for cid in n.get('claims', []):
            assert cid in available_claims, (n['id'], cid)
    m['validation'] = {**m.get('validation', {}), 'node_count': len(m['nodes']),
        'node_ids_unique': True, 'acyclic': True, 'all_edges_resolve': True, 'all_related_nodes_resolve': True,
        'all_current_target_ids_resolve': True, 'all_current_claim_ids_resolve': True,
        'historical_node_meanings_preserved': True, 'historical_node_count': len(baseline['nodes']),
        'changed_historical_nodes': changed, 'complete_previous_records_preserved': True,
        'historical_validation_preserved_in_previous_map': True,
        'literal_AdjointLiftingTheorem_supplied': True, 'AdjointLifting_supplier': 'QX1',
        'literal_SeedIIAlt_supplied': True, 'SeedIVAlt_supplied': False,
        'complete_case_II_ProModAlt_implication_supplied': True, 'case_III_ProModAlt_supplier_supplied': False,
        'unconditional_PMExAlt_CountII_ImageDense_or_PointHV_promoted': False,
        'whole_HidaUAlt_ModUAlt_Hprime_UnramifiedInputs_promoted': False,
        'P3core_promoted': False, 'same_ideal_Hida_and_P1_binding_retained': True,
        'case_II_count_open_substantive_leaf_ids': case_ii_open_leaves,
        'case_II_count_requires_full_ImageDense_case_III_or_SeedIV': False,
        'whole_DX_LocBase_or_FP8_inferred_from_partial_proof_reuse': False,
        'related_node_annotations_are_not_proof_edges': True}
    anchors = sorted(source_index.values(), key=lambda a: (a['path'], a['line_start'], a['line_end']))
    source_obj = {'commit': PIN, 'sources': anchors, 'source_files': len(blobs), 'source_ranges': len(anchors)}
    source_bytes = (json.dumps(source_obj, ensure_ascii=False, indent=2) + '\n').encode()
    m['source_manifest_sha256'] = sha(source_bytes)
    (HERE / 'previous_obligation_map.json').write_bytes((OLD / 'obligation_map.json').read_bytes())
    write('obligation_map.json', m)
    write('source_anchors.json', source_obj)
    write('next_targets.json', {'targets': targets})
    write('retirement_candidates.json', {'targets': [], 'count': 0,
        'reason': 'No historical target is retired as a whole. DA28-SP-01 still contains the actual support producer; DA28-SP-02 contains SeedIVAlt; DA28-SP-03 contains the unclosed case-III realization. Complete proper subchains are supplied and recorded in target_scope_updates.'})
    write('target_scope_updates.json', updates)
    write('global_branch_scope_updates.json', {'updates': global_scope_updates})
    write('symplectic_frontier_sources.json', {
        'actual_support_frontier': unique_sources(support_sources),
        'remaining_case_III_frontier': case_three_sources,
        'case_II_count_remaining_cut': pm_cut, 'sufficient_actual_producer': support_cut,
        'height_remaining_cut': height_cut, 'alternative_height_cut': old_height_cut,
        'same_ideal_binding_required': True, 'related_nodes_are_not_proof_edges': True})
    file_input(HERE / 'build_audit.py')
    file_input(HERE / 'audit.txt')
    write('input_manifest.json', {'artifact_version': '0.29', 'components': COMPONENTS,
        'review_input_policy': 'Only explicit mathematical component reviews/source validations and integration-scope reviews. Downstream semantic/final-scope/coverage/package/audit outputs are excluded. The upstream ordinary-support mathematical dependency audit is explicitly included. Current mutable root provenance/targets are not inputs; the frozen v0.28 archive is used.',
        'files': [input_index[k] for k in sorted(input_index)]})
    write('summary.json', {'artifact_version': '0.29', 'new_claim_ids': [],
        'increment_supplier_claims': component_claims, 'retirement_candidate_ids': [], 'retirement_count': 0,
        'historical_nodes_preserved': len(baseline['nodes']), 'map_node_count': len(m['nodes']),
        'changed_historical_node_ids': changed,
        'complete_new_chain': 'Literal PMExAlt -> original Ctx2 Fin0/NoEnd/AllIrr IsAut4Alt -> literal CountII',
        'conditional_supplied_counts': {'CountII': 'YX2 from PMExAlt', 'CountII and CountIII': 'Earlier JX1 from full ImageDense'},
        'current_count_cut': height_cut, 'alternative_count_cuts': [old_height_cut],
        'sufficient_actual_support_refinement': support_cut,
        'supplied_counts': {'CountZ': 'CZ6', 'CountVs': 'HV5', 'CountIV': 'HV6'},
        'literal_SeedIIAlt_supplier': 'SX8', 'literal_AdjointLiftingTheorem_supplier': 'QX1',
        'actual_case_II_ProModAlt_supplier': 'UX12 from SeedIIAlt and PMExAlt',
        'ordinary_support_audit': 'ordinary_support_dependency_audit/audit.json',
        'not_globally_closed': ['RH', 'Dirichlet GRH', 'PointHV', 'Actual CountI, CountIII and CountV',
          'Unconditional CountII', 'SymplecticFourImageDense', 'Actual PMExAlt',
          'Actual rank-four same-ideal HidaPropsAlt/P1core supplier', 'SeedIVAlt and case-III realization',
          'Actual-family LinkN', 'Actual compatible family/DesignExists/HostExW',
          'Theta/type/rank/metric/spectral joins', 'Final arithmetic gap/gain'],
        'not_promoted': ['Whole UnramifiedInputs', 'Whole HypothesesH-prime', 'All-rank HidaUAlt or ModUAlt',
                         'P3core', 'LiteratureRankNHypothesis', 'All-rank CountQAlt', 'Unchanged-level LevelPNAlt']})
    write('verification.json', {'artifact_version': '0.29', 'source_commit': PIN,
        'source_files_checked': len(blobs), 'source_ranges_indexed': len(anchors),
        'all_cited_source_files_equal_pinned_git_blobs': True, 'all_source_range_hashes_verified': True,
        'new_component_proof_ranges_verified': len(proof_checks), 'all_component_main_and_proof_hashes_match': True,
        'available_component_manifest_entries_verified': component_manifest_checks,
        'previous_release_input_manifest_verified': True, 'historical_node_ids_preserved': True,
        'complete_changed_node_snapshots_verified': True, 'historical_snapshot_byte_identical': True,
        'sufficient_condition_graph_acyclic': True, 'current_validation_node_count': len(m['nodes']),
        'case_II_count_open_substantive_leaf_ids': case_ii_open_leaves,
        'case_II_count_requires_full_ImageDense_case_III_or_SeedIV': False,
        'historical_validation_not_edited': True, 'all_related_and_target_ids_resolve': True,
        'retirement_count': 0, 'prior_files_modified': False, 'root_targets_modified': False, 'new_claim_ids': [],
        'Lean_kernel_replay_run': False, 'formal_transitive_Lean_dependency_audit': False,
        'audit_txt_sha256': sha((HERE / 'audit.txt').read_bytes()),
        'scope': 'Human semantic sufficient-condition audit. Integrity and graph checks validate provenance/bookkeeping, not mathematical proofs.'})
    print(json.dumps({'retirements': 0, 'targets': len(targets), 'source_files': len(blobs),
        'source_ranges': len(anchors), 'proof_ranges': len(proof_checks), 'historical_nodes': len(baseline['nodes']),
        'map_nodes': len(m['nodes']), 'manifest_inputs': len(input_index)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=WORK.parent / 'lean-source')
    main(parser.parse_args().repo.resolve())
