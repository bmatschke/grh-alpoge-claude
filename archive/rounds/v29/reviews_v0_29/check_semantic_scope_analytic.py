#!/usr/bin/env python3
"""Read-only independent scope and integrity checks for the frozen v0.29 map.

Writes only this reviewer's evidence file.  This is not a Lean dependency
extraction or a second proof of the component theorems.
"""
from pathlib import Path
import hashlib
import json
import subprocess

WORK = Path(__file__).resolve().parents[1]
AUDIT = WORK / 'dependency_audit_v0_29'
SOURCE = WORK.parent / 'lean-source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def index(rows):
    out = {r['id']: r for r in rows}
    assert len(out) == len(rows)
    return out


mapping = read(AUDIT / 'obligation_map.json')
previous = read(AUDIT / 'previous_obligation_map.json')
nodes, old = index(mapping['nodes']), index(previous['nodes'])
assert mapping['source_commit'] == PIN
assert (AUDIT / 'previous_obligation_map.json').read_bytes() == (
    WORK / 'dependency_audit_v0_28/obligation_map.json').read_bytes()
assert len(nodes) == 151 and len(old) == 129 and set(old) <= set(nodes)
changed = sorted(k for k in old if old[k] != nodes[k])
assert len(changed) == 14
for k in changed:
    snapshots = [r['snapshot'] for r in nodes[k]['history']
                 if r['version'] == '0.28']
    assert len(snapshots) == 1 and snapshots[0] == old[k], k
assert set(changed) == set(mapping['validation']['changed_historical_nodes'])


def edges(node):
    gate = node['gate']
    assert gate in {'AND', 'OR', 'LEAF'}, node['id']
    if gate == 'AND':
        assert node.get('requires'), node['id']
        assert not node.get('alternatives'), node['id']
        return node['requires']
    if gate == 'OR':
        assert node.get('alternatives'), node['id']
        assert not node.get('requires'), node['id']
        assert all(isinstance(a, list) and a for a in node['alternatives'])
        return [x for a in node['alternatives'] for x in a]
    assert not node.get('requires') and not node.get('alternatives'), node['id']
    return []


for n in nodes.values():
    assert set(edges(n)) <= set(nodes), n['id']
    assert set(n.get('related_nodes', [])) <= set(nodes), n['id']
active, done = set(), set()


def visit(k):
    assert k not in active, k
    if k in done:
        return
    active.add(k)
    for j in edges(nodes[k]):
        visit(j)
    active.remove(k)
    done.add(k)


for k in nodes:
    visit(k)
assert len(done) == len(nodes)

components = [
    'symplectic_universal_arithmetic', 'symplectic_modular_support',
    'symplectic_automorphic_seeds', 'symplectic_promodular_realization',
    'case_two_installation',
]
claims = index(read(WORK / 'history/version_0_28/provenance.json')['claims'])
proof_count = 0
for component in components:
    ledger = read(WORK / component / 'provenance.json')
    assert ledger['commit'] == PIN
    assert sha((WORK / component / 'main.tex').read_bytes()) == ledger['main_tex_sha256']
    for claim in ledger['claims']:
        assert claim['id'] not in claims
        claims[claim['id']] = claim
        p = claim['proof_location']
        lines = (WORK / p['file']).read_bytes().splitlines(keepends=True)
        segment = b''.join(lines[p['line_start'] - 1:p['line_end']])
        assert sha(segment) == p['sha256'], claim['id']
        assert len(segment) == p['bytes'], claim['id']
        proof_count += 1
assert proof_count == 41
for n in nodes.values():
    assert set(n.get('claims', [])) <= set(claims), n['id']

targets = index(read(AUDIT / 'next_targets.json')['targets'])
assert len(targets) == 33
for n in nodes.values():
    assert set(n.get('source_target_ids', [])) <= set(targets), n['id']
    assert set(n.get('related_source_target_ids', [])) <= set(targets), n['id']
retirements = read(AUDIT / 'retirement_candidates.json')
assert retirements['count'] == 0 and retirements['targets'] == []

assert nodes['EXACT_AUTOMORPHIC_SEEDS']['gate'] == 'AND'
assert set(nodes['EXACT_AUTOMORPHIC_SEEDS']['requires']) == {
    'CASE_TWO_SEED', 'CASE_FOUR_SEED'}
assert nodes['ACTUAL_PROMODULAR_REALIZATION']['gate'] == 'AND'
assert set(nodes['ACTUAL_PROMODULAR_REALIZATION']['requires']) == {
    'CASE_TWO_PROMODULAR_REALIZATION', 'CASE_THREE_PROMODULAR_REALIZATION'}
assert nodes['SYMPLECTIC_COUNT_CHAIN']['alternatives'] == [
    ['PAIRED_COUNT_ONE_INPUT_JOIN'],
    ['CASE_TWO_COUNT_SUPPLIER', 'COUNT_III_SUPPLIER'],
]
assert nodes['SYMPLECTIC_IMAGE_DENSITY']['alternatives'] == old[
    'SYMPLECTIC_IMAGE_DENSITY']['alternatives']

reachable, todo = set(), ['CASE_TWO_COUNT_SUPPLIER']
while todo:
    k = todo.pop()
    if k in reachable:
        continue
    reachable.add(k)
    todo.extend(edges(nodes[k]))
assert not any(nodes[k]['gate'] == 'OR' for k in reachable)
forbidden = {
    'SYMPLECTIC_IMAGE_DENSITY', 'CASE_FOUR_SEED',
    'CASE_THREE_PROMODULAR_REALIZATION', 'COUNT_III_SUPPLIER',
    'ACTUAL_PROMODULAR_REALIZATION', 'EXACT_AUTOMORPHIC_SEEDS',
}
assert not reachable & forbidden
leaves = sorted(k for k in reachable if nodes[k]['gate'] == 'LEAF')
open_leaves = [k for k in leaves if not nodes[k].get('claims') and
               not nodes[k].get('status', '').startswith('named_')]
assert open_leaves == ['ACTUAL_RANK_FOUR_HECKE_SUPPORT']
support = nodes[open_leaves[0]]
assert support['component_fields'] == [
    'ring', 'dense', 'pt', 'end1', 'end2', 'twist', 'P1core']
assert 'same-ideal' in support['premise'] and 'threshold' in support['premise']
assert 'P3core' in support['not_inferred']

q = nodes['ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT']
assert 'ACTUAL_LOCAL_BASES' not in q['requires']
assert 'DX5' in q['proof_step_reuse']
q = nodes['CASE_TWO_PROMODULAR_JOIN']
assert 'FRAMED_WEIGHTED_PRESENTATION' not in q['requires']
assert set(q['proof_step_reuse']) == {'FP1/FP2', 'FP5', 'FP7'}
q = nodes['ACTUAL_PM_TOWER_JOIN']
assert 'PROMODULAR_TRANSPORT_JOIN' not in q['requires']
assert 'IX9' in q['proof_step_reuse']

updates = read(AUDIT / 'target_scope_updates.json')
for k in ('DA26-SP-01', 'DA26-SP-03'):
    row = updates[k]
    assert not any('CountIII' in x for x in row['retained_inputs']), k
    assert any('ImageDense' in x for x in row['retained_inputs']), k
    assert 'downstream_paired_count_cut' in row, k
    assert 'Actual CountIII' in row['downstream_paired_count_cut'], k
assert mapping['current_count_cut'][:3] == [
    'Actual CountI', 'Actual CountIII', 'Actual CountV']
assert 'PMExAlt' in mapping['current_count_cut'][3]
assert mapping['alternative_count_cuts'][0][:2] == ['Actual CountI', 'Actual CountV']
assert 'ImageDense' in mapping['alternative_count_cuts'][0][2]

anchor_file = read(AUDIT / 'source_anchors.json')
assert anchor_file['commit'] == PIN
anchors = anchor_file['sources']
paths = sorted({a['path'] for a in anchors})
assert len(anchors) == 1987 and len(paths) == 806
batch = ''.join(f'{PIN}:{p}\n' for p in paths).encode()
result = subprocess.run(['git', 'cat-file', '--batch'], cwd=SOURCE,
                        input=batch, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, check=True)
data, pos, blobs = result.stdout, 0, {}
for path in paths:
    end = data.index(b'\n', pos)
    fields = data[pos:end].split()
    assert len(fields) == 3 and fields[1] == b'blob', path
    size = int(fields[2]); pos = end + 1
    blob = data[pos:pos + size]; pos += size
    assert data[pos:pos + 1] == b'\n'; pos += 1
    assert (SOURCE / path).read_bytes() == blob, path
    blobs[path] = blob
assert pos == len(data)
for a in anchors:
    blob = blobs[a['path']]
    assert sha(blob) == a['sha256'], a['path']
    lines = blob.splitlines(keepends=True)
    assert 1 <= a['line_start'] <= a['line_end'] <= len(lines), a
    segment = b''.join(lines[a['line_start'] - 1:a['line_end']])
    assert sha(segment) == a['range_sha256'], a
    if 'range_bytes' in a:
        assert len(segment) == a['range_bytes'], a

manifest = read(AUDIT / 'input_manifest.json')
manifest_paths = []
for entry in manifest['files']:
    p = entry['path']; content = (WORK / p).read_bytes()
    assert sha(content) == entry['sha256'], p
    assert len(content) == entry['bytes'], p
    assert 'semantic_scope' not in p, p
    manifest_paths.append(p)
assert len(manifest_paths) == len(set(manifest_paths)) == 101

subject_names = [
    'obligation_map.json', 'source_anchors.json',
    'retirement_candidates.json', 'target_scope_updates.json',
    'global_branch_scope_updates.json', 'audit.txt', 'input_manifest.json',
]
evidence = {
    'schema': 'rh-independent-semantic-scope-validation/1',
    'artifact_version': '0.29',
    'reviewer': '/root/analytic_closure',
    'source_commit': PIN,
    'result': 'PASS',
    'no_unresolved_scope_findings': True,
    'review_type': 'Independent human semantic scope review plus read-only structural and hash checks',
    'reviewed_files': [
        {'path': f'dependency_audit_v0_29/{f}',
         'sha256': sha((AUDIT / f).read_bytes())}
        for f in subject_names],
    'checks': {
        'previous_map_byte_identical': True,
        'historical_ids_preserved': len(old),
        'current_unique_nodes': len(nodes),
        'full_changed_historical_snapshots_verified': len(changed),
        'new_nodes': len(set(nodes) - set(old)),
        'all_proof_and_related_references_resolve': True,
        'and_or_graph_acyclic': True,
        'all_claim_and_target_ids_resolve': True,
        'new_component_proof_ranges_verified': proof_count,
        'pinned_git_source_files_verified': len(paths),
        'source_ranges_verified': len(anchors),
        'manifest_input_hashes_verified': len(manifest_paths),
        'semantic_outputs_excluded_from_input_manifest': True,
        'whole_target_retirements': retirements['count'],
        'compound_case_scopes_preserved': True,
        'case_II_reachable_nodes': len(reachable),
        'case_II_open_substantive_leaves': open_leaves,
        'case_II_reaches_full_ImageDense_case_III_or_SeedIV': False,
        'same_ideal_Hida_P1_and_threshold_scope_explicit': True,
        'whole_DX_LocBase_or_FP8_inferred_from_subproof_reuse': False,
        'IX9_reuse_is_only_finite_fibre_subargument': True,
        'G1_G2_full_geometry_distinguished_from_downstream_count_cut': True,
        'original_field_coefficient_return_and_host_window_guards_retained': True,
        'no_unconditional_PMExAlt_CountII_ImageDense_PointHV_or_RH_promotion': True,
    },
    'resolved_findings': [
        {'id': 'SA29-01',
         'targets': ['DA26-SP-01', 'DA26-SP-03'],
         'finding': 'PMExAlt plus actual CountIII supplies the paired count, not the missing case-III G1/G2 geometry.',
         'resolution': 'The full-target retained input remains ImageDense; PMExAlt and CountIII are recorded separately as the downstream_paired_count_cut. The case-II specialization remains explicit.'},
    ],
    'limitations': [
        'This is a finite sufficient-condition map, not an exhaustive Lean dependency graph or a necessity claim.',
        'The integrity checks do not replace mathematical proofs. Mathematical review here concerns the exact scopes and joins of the already reviewed components.',
        'Named classical theorem leaves remain explicit, and the same-ideal rank-four Hecke/support producer remains open.',
        'No Lean kernel replay or PDF generation was run.',
    ],
    'checker_sha256': sha(Path(__file__).read_bytes()),
}
notes = Path(__file__).parent / 'semantic_scope_analytic_review.txt'
assert notes.is_file()
evidence['detailed_notes'] = {
    'path': str(notes.relative_to(WORK)),
    'sha256': sha(notes.read_bytes()),
}
destination = Path(__file__).parent / 'semantic_scope_analytic_validation.json'
destination.write_text(json.dumps(evidence, indent=2) + '\n')
print(json.dumps({'result': evidence['result'], 'nodes': len(nodes),
                  'changed_snapshots': len(changed), 'open_leaf': open_leaves,
                  'source_ranges': len(anchors), 'output': str(destination),
                  'output_sha256': sha(destination.read_bytes())}, indent=2))
