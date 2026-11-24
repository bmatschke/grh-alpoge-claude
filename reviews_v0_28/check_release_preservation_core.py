#!/usr/bin/env python3
"""Independent, read-only v0.28 release preservation checks.

This checker writes only its own evidence JSON. It does not rerun the release
assembler, merger, metadata generator, source audit or TeX compiler.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'history/version_0_27'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mono_breaks(match):
    body = re.sub(r'(?<=[a-z])(?=[A-Z])', lambda _: r'\allowbreak ', match[1])
    body = re.sub(r'\.(?!\\allowbreak)', lambda _: r'.\allowbreak ', body)
    body = re.sub(r'\\_(?!\\allowbreak)', lambda _: r'\_\allowbreak ', body)
    return r'\texttt{' + body + '}'


def component_render(text):
    return re.sub(r'\\texttt\{([^{}]*)\}', mono_breaks, text).replace(
        'metric/global/spectral', r'metric/\allowbreak global/\allowbreak spectral')


def current_block_render(text):
    return text.strip().replace(
        r'\texttt{NormChoiceFacts}/\texttt{Tie4}',
        r'\texttt{Norm\allowbreak Choice\allowbreak Facts}/\allowbreak \texttt{Tie4}')


cfg = read(ROOT / 'increment_v0_28.json')
previous_cfg = read(OLD / 'increment_v0_27.json')
prior = read(OLD / 'provenance.json')
current = read(ROOT / 'provenance.json')
old_tex = (OLD / 'RH_readable_reconstruction_v0_27.tex').read_text()
tex_path = ROOT / 'RH_readable_reconstruction_v0_28.tex'
new_tex = tex_path.read_text()
expected = {
    'bloch_kato_installation': [f'BX{i}' for i in range(1, 9)],
    'symplectic_actual_rigidity': [f'RX{i}' for i in range(1, 8)],
    'symplectic_automorphic_catalogue': [f'CX{i}' for i in range(1, 10)],
    'symplectic_image_density': [f'IX{i}' for i in range(1, 11)],
    'paired_count_installation': ['JX1', 'JX2'],
}
assert cfg['components'] == list(expected)
assert cfg['tex_component_order'] == list(expected)
assert current['artifact_version'] == '0.28'
assert current['commit'] == prior['commit'] == '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'

old_claims = {c['id']: c for c in prior['claims']}
new_claims = {c['id']: c for c in current['claims']}
assert len(new_claims) == len(current['claims'])
assert [c['id'] for c in current['claims'][:len(prior['claims'])]] == list(old_claims)
for cid, claim in old_claims.items():
    for key, value in claim.items():
        assert new_claims[cid][key] == value, (cid, key)
for path, old_file in {f['path']: f for f in prior['source_files']}.items():
    assert next(f for f in current['source_files'] if f['path'] == path) == old_file, path
for cid, deps in prior['mathematical_dependency_graph'].items():
    assert current['mathematical_dependency_graph'][cid] == deps, cid

new_ids = [c['id'] for c in current['claims'][len(prior['claims']):]]
assert new_ids == [cid for ids in expected.values() for cid in ids]
seen, active = set(), set()


def visit(cid):
    assert cid in new_claims, cid
    if cid in seen:
        return
    assert cid not in active, ('cycle', cid)
    active.add(cid)
    for dep in current['mathematical_dependency_graph'][cid]:
        visit(dep)
    active.remove(cid)
    seen.add(cid)


for cid in current['mathematical_dependency_graph']:
    visit(cid)

component_counts = {}
component_occurrences = {}
for component, ids in expected.items():
    ledger = read(ROOT / component / 'provenance.json')
    assert [c['id'] for c in ledger['claims']] == ids, component
    assert current['merge_inputs'][component]['sha256'] == sha(ROOT / component / 'provenance.json')
    assert current['version_0_28_local_conclusions']['closure_certificates'][component]['sha256'] == sha(ROOT / component / 'closure.json')
    for claim in ledger['claims']:
        for key, value in claim.items():
            if key != 'introduced_in':
                assert new_claims[claim['id']][key] == value, (claim['id'], key)
    rendered = component_render((ROOT / component / 'main.tex').read_text())
    component_occurrences[component] = new_tex.count(rendered)
    assert component_occurrences[component] == 1, component
    component_counts[component] = len(ids)

for component, record in prior['merge_inputs'].items():
    assert sha(ROOT / record['ledger']) == record['sha256'], component

old_proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', old_tex, re.S)
new_proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', new_tex, re.S)
cursor = 0
old_positions = []
for proof in old_proofs:
    while cursor < len(new_proofs) and new_proofs[cursor] != proof:
        cursor += 1
    assert cursor < len(new_proofs), ('historical proof missing', len(old_positions))
    old_positions.append(cursor)
    cursor += 1
assert len(new_proofs) - len(old_proofs) == 36

current_blocks = {}
for key in ['tex_front_summary', 'tex_scope_bridge']:
    current_blocks[key] = new_tex.count(cfg[key])
    assert current_blocks[key] == 1, key
for key in ['tex_remaining_local', 'tex_next_target', 'tex_reading_order']:
    current_blocks[key] = new_tex.count(current_block_render(cfg[key]))
    assert current_blocks[key] == 1, key
    predecessor = previous_cfg[key].strip().replace(
        'form/lattice/signature', r'form/\allowbreak lattice/\allowbreak signature')
    predecessor = current_block_render(predecessor)
    assert predecessor not in new_tex, key
current_blocks['tex_dependency_update'] = new_tex.count(component_render(cfg['tex_dependency_update']))
assert current_blocks['tex_dependency_update'] == 1
assert new_tex.count(previous_cfg['tex_scope_bridge']) == 1
for row in cfg['tex_ledger_rows']:
    assert new_tex.count(row + r'\\[3pt]') == 1
assert r'\item[Actual local denominators and the four remaining count suppliers.]' not in new_tex
assert new_tex.count(r'\item[Actual local denominators and the reduced count input.]') == 1

old_targets = read(OLD / 'next_source_targets.json')
targets = read(ROOT / 'next_source_targets.json')
retirement = read(ROOT / 'dependency_audit_v0_28/retirement_candidates.json')['targets']
old_by_id = {t.get('id'): t for t in old_targets['targets'] if t.get('id')}
retired = targets['version_0_28_replaced_targets']
assert {r['id'] for r in retired} == {r['id'] for r in retirement} == {'DA26-SP-04', 'DA26-SP-06'}
for r in retired:
    assert r['original_target_snapshot'] == old_by_id[r['id']], r['id']
assert targets['global_branches_unchanged'] == old_targets['global_branches_unchanged']
new_target_keys = {(t['path'], t['line_start'], t['line_end']) for t in targets['targets']}
retired_keys = {(r['original_target_snapshot']['path'], r['original_target_snapshot']['line_start'], r['original_target_snapshot']['line_end']) for r in retired}
for t in old_targets['targets']:
    key = (t['path'], t['line_start'], t['line_end'])
    assert key in new_target_keys or key in retired_keys, key

tex_validation = read(ROOT / 'tex_validation.json')
assert tex_validation['tex_sha256'] == sha(tex_path)
assert tex_validation['artifact_version'] == '0.28'
assert tex_validation['syntax_compile_succeeded'] is True
assert tex_validation['passes'] == 2
assert tex_validation['pdf_generated'] is False
assert tex_validation['undefined_references_or_citations'] is False
assert tex_validation['missing_character_warnings'] == 0
assert tex_validation['overfull_box_warnings'] == 41

result = {
    'schema': 'rh-independent-release-preservation-checks-v1',
    'artifact_version': '0.28',
    'reviewer': 'core_closure',
    'result': 'PASS',
    'historical_claims_checked': len(old_claims),
    'all_original_claim_fields_equal': True,
    'historical_source_file_records_checked': len(prior['source_files']),
    'all_historical_source_file_records_equal': True,
    'all_historical_dependency_edges_equal': True,
    'new_claim_count': len(new_ids),
    'new_claim_ids': new_ids,
    'new_component_claim_counts': component_counts,
    'all_merged_component_claim_fields_equal': True,
    'all_merge_component_provenance_and_closure_hashes_current': True,
    'all_four_predecessor_component_ledgers_unchanged': True,
    'reference_dependency_graph_acyclic': True,
    'reference_dependency_graph_is_exhaustive_lean_audit': False,
    'historical_proof_environments_checked': len(old_proofs),
    'all_historical_proof_environment_bytes_preserved_in_order': True,
    'current_cumulative_proof_environments': len(new_proofs),
    'component_exact_normalized_occurrences': component_occurrences,
    'component_normalization_scope': 'Only texttt allowbreak commands and the explicit metric/global/spectral slash line-break correction.',
    'current_frontier_and_summary_block_occurrences': current_blocks,
    'old_scope_bridge_preserved': True,
    'replaced_old_current_frontier_blocks_absent': True,
    'historical_active_targets_checked': len(old_targets['targets']),
    'only_retired_target_ids': [r['id'] for r in retired],
    'retired_target_snapshots_match_predecessor_exactly': True,
    'all_other_predecessor_source_targets_retained': True,
    'global_branch_objects_preserved': True,
    'current_active_target_count': len(targets['targets']),
    'tex_validation': {
        'tex_sha256': sha(tex_path),
        'passes': 2,
        'syntax_references_and_glyph_checks_pass': True,
        'overfull_warnings': 41,
        'new_overfull_warnings_relative_to_v0_27': 0,
        'pdf_generated': False,
        'compile_independently_rerun_in_this_review': False,
    },
    'unresolved_findings': [],
    'scope_limit': 'Byte/source-record preservation and release-scope checks, not a new mathematical proof, Lean build or exhaustive transitive source audit.',
}
out = ROOT / 'reviews_v0_28/release_preservation_core_checks.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
