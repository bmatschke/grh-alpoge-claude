#!/usr/bin/env python3
"""Read-only release checks; write only this review's independent evidence."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'history/version_0_28'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


cfg = read(ROOT / 'increment_v0_29.json')
prior = read(OLD / 'provenance.json')
old_roots = {p.name for p in OLD.iterdir() if p.is_file()}
manifest_count = 0
for line in (OLD / 'SHA256SUMS').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    path = OLD / relative if relative in old_roots else ROOT / relative
    assert path.is_file() and sha(path) == expected, relative
    manifest_count += 1

# Execute the reviewed assembler with its two output expressions removed.
# Its remaining operations are reads and pure string transformations.
script = ROOT / 'assemble_v0_29.py'
tree = ast.parse(script.read_text(), filename=str(script))
nodes, omitted = [], []
for node in tree.body:
    is_output = (
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and ((isinstance(node.value.func, ast.Attribute)
              and node.value.func.attr == 'write_text')
             or (isinstance(node.value.func, ast.Name)
                 and node.value.func.id == 'print')))
    if is_output:
        omitted.append(ast.unparse(node))
    else:
        nodes.append(node)
assert omitted == ['out.write_text(s)', 'print(out)']
namespace = {'__file__': str(script)}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(script), 'exec'), namespace)
tex_path = ROOT / 'RH_readable_reconstruction_v0_29.tex'
text = tex_path.read_text()
assert namespace['s'].encode() == tex_path.read_bytes()

old_text = (OLD / 'RH_readable_reconstruction_v0_28.tex').read_text()
old_proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', old_text, re.S)
new_proofs = re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', text, re.S)
cursor = 0
for index, proof in enumerate(old_proofs):
    while cursor < len(new_proofs) and new_proofs[cursor] != proof:
        cursor += 1
    assert cursor < len(new_proofs), ('missing historical proof', index)
    cursor += 1

expected_components = {
    'symplectic_universal_arithmetic': [f'KX{i}' for i in range(1, 10)],
    'symplectic_modular_support': [f'QX{i}' for i in range(1, 11)],
    'symplectic_automorphic_seeds': [f'SX{i}' for i in range(1, 9)],
    'symplectic_promodular_realization': [f'UX{i}' for i in range(1, 13)],
    'case_two_installation': ['YX1', 'YX2'],
}
assert cfg['components'] == cfg['tex_component_order'] == list(expected_components)
claims = copy.deepcopy(prior['claims'])
graph = copy.deepcopy(prior['mathematical_dependency_graph'])
source_files = {f['path']: copy.deepcopy(f) for f in prior['source_files']}
component_bindings, occurrences = [], {}
for component, expected_ids in expected_components.items():
    directory = ROOT / component
    data = read(directory / 'provenance.json')
    closure = read(directory / 'closure.json')
    assert [c['id'] for c in data['claims']] == expected_ids
    assert data['commit'] == prior['commit']
    assert sha(directory / 'main.tex') == data['main_tex_sha256'] == closure['main_tex_sha256']
    assert sha(directory / 'provenance.json') == closure['provenance_sha256']
    component_text = (directory / 'main.tex').read_text()
    rendered = re.sub(r'\\texttt\{([^{}]*)\}', namespace['mono_breaks'], component_text)
    rendered = rendered.replace('metric/global/spectral',
                                r'metric/\allowbreak global/\allowbreak spectral')
    occurrences[component] = text.count(rendered)
    assert occurrences[component] == 1
    for claim in data['claims']:
        claims.append(copy.deepcopy(claim))
        graph[claim['id']] = list(claim.get('depends_on', []))
    for record in data['source_files']:
        if record['path'] in source_files:
            assert source_files[record['path']]['sha256'] == record['sha256']
        else:
            source_files[record['path']] = copy.deepcopy(record)
    component_bindings.append({
        'component': component, 'claim_ids': expected_ids,
        'main_sha256': sha(directory / 'main.tex'),
        'provenance_sha256': sha(directory / 'provenance.json'),
        'closure_sha256': sha(directory / 'closure.json'),
    })

ids = {c['id'] for c in claims}
assert len(ids) == len(claims) == len(prior['claims']) + 41
assert len(new_proofs) == len(old_proofs) + 41
assert claims[:len(prior['claims'])] == prior['claims']
for cid, deps in prior['mathematical_dependency_graph'].items():
    assert graph[cid] == deps
for record in prior['source_files']:
    assert source_files[record['path']] == record
done, active = set(), set()


def visit(cid):
    assert cid in ids
    if cid in done:
        return
    assert cid not in active, ('reference cycle', cid)
    active.add(cid)
    for dependency in graph[cid]:
        visit(dependency)
    active.remove(cid)
    done.add(cid)


for cid in graph:
    visit(cid)

frontier = text[text.index(r'\section{The arithmetic still to be written out}'):]
assert 'the four\nactual \\texttt{CountI/II/III/V} suppliers' not in frontier
assert r'YX2 supplies the entire \texttt{CountII} chain from \texttt{PMExAlt}' in frontier
assert 'QX retains the actual rank-four ordinary Hecke/support producer.' in frontier
assert r'\paragraph{Version-0.29 scope of the historical conditional proofs.}' in text
assert r'\paragraph{Version-0.28 scope of the historical conditional proofs.}' in text
assert r'\item[Actual local denominators and the reduced count input.]' not in frontier
assert r'\item[Actual local denominators and the case-II support producer.]' in frontier
assert "mapping['note'] = ('Current v0.29 locations" in (ROOT / 'finish_metadata_v0_29.py').read_text()

result = {
    'schema': 'rh-independent-release-preservation-checks-v1',
    'artifact_version': '0.29', 'reviewer': '/root/analytic_closure', 'result': 'PASS',
    'predecessor_manifest_entries_checked': manifest_count,
    'predecessor_files_including_manifest_preserved': manifest_count + 1,
    'predecessor_root_files_archived': len(old_roots),
    'all_predecessor_file_bytes_match': True,
    'historical_proof_environments_checked': len(old_proofs),
    'current_cumulative_proof_environments': len(new_proofs),
    'all_historical_proof_bytes_preserved_in_order': True,
    'assembler_reproduced_read_only': True,
    'assembler_omitted_output_expressions': omitted,
    'cumulative_tex_sha256': sha(tex_path),
    'new_claim_count': 41,
    'component_exact_normalized_occurrences': occurrences,
    'component_bindings': component_bindings,
    'prospective_merged_claim_count': len(claims),
    'prospective_merged_source_file_count': len(source_files),
    'all_historical_claim_source_and_edge_records_unchanged_in_additive_merge': True,
    'all_component_dependency_ids_resolve_and_reference_graph_acyclic': True,
    'current_frontier_uses_CountI_CountIII_CountV_PMExAlt': True,
    'old_scope_bridge_preserved': True,
    'unversioned_filename_map_note_updated': True,
    'unresolved_findings': [],
    'scope_limit': ('Independent read-only preservation, assembly and prospective additive-merge checks. '
                    'The later audited merge must verify the actual final root metadata and semantic target updates. '
                    'No new mathematical review, source-transitive audit, Lean build or PDF run is asserted.'),
}
output = ROOT / 'reviews_v0_29/release_preservation_analytic_checks.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
