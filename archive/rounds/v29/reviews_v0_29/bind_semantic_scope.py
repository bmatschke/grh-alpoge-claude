#!/usr/bin/env python3
"""Bind the root's prose scope review to the final finite obligation map.

The structural checks below do not verify mathematical proofs.  They keep
the stated scope review attached to the exact objects reviewed.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'dependency_audit_v0_29'
OUT = ROOT / 'reviews_v0_29'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


current = read(AUDIT / 'obligation_map.json')
prior = read(ROOT / 'dependency_audit_v0_28/obligation_map.json')
nodes = {node['id']: node for node in current['nodes']}
old_nodes = {node['id']: node for node in prior['nodes']}
assert len(nodes) == len(current['nodes'])
assert set(old_nodes) <= set(nodes)
changed = []
for key, old in old_nodes.items():
    if nodes[key] != old:
        assert any(record.get('snapshot') == old
                   for record in nodes[key].get('history', [])), key
        changed.append(key)

edges = {}
for key, node in nodes.items():
    if node['gate'] == 'AND':
        deps = node.get('requires', [])
    elif node['gate'] == 'OR':
        deps = [dep for option in node.get('alternatives', []) for dep in option]
    else:
        deps = []
    assert set(deps) <= set(nodes), key
    edges[key] = deps

done, active = set(), set()


def visit(key):
    if key in done:
        return
    assert key not in active, ('cycle', key)
    active.add(key)
    for dep in edges[key]:
        visit(dep)
    active.remove(key)
    done.add(key)


for key in nodes:
    visit(key)

case_two = set()


def collect(key):
    if key in case_two:
        return
    case_two.add(key)
    for dep in edges[key]:
        collect(dep)


collect('CASE_TWO_COUNT_SUPPLIER')
for excluded in ['CASE_THREE_PROMODULAR_REALIZATION', 'CASE_FOUR_SEED',
                 'COUNT_III_SUPPLIER', 'SYMPLECTIC_IMAGE_DENSITY']:
    assert excluded not in case_two, excluded
leaves = sorted(key for key in case_two if not edges[key])
open_leaves = [key for key in leaves
               if 'retained' in nodes[key].get('status', '').lower()
               or 'open' in nodes[key].get('status', '').lower()]
assert open_leaves == ['ACTUAL_RANK_FOUR_HECKE_SUPPORT'], open_leaves
assert 'ACTUAL_LOCAL_BASES' not in edges['ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT']
assert 'FRAMED_WEIGHTED_PRESENTATION' not in edges['CASE_TWO_PROMODULAR_JOIN']
assert 'DX5' in nodes['ARITHMETIC_CHARACTERISTIC_ZERO_SUPPORT']['proof_step_reuse']
assert {'FP1/FP2', 'FP5', 'FP7'} <= set(nodes['CASE_TWO_PROMODULAR_JOIN']['proof_step_reuse'])

retirements = read(AUDIT / 'retirement_candidates.json')
assert retirements['targets'] == []
updates = read(AUDIT / 'target_scope_updates.json')
old_targets = read(ROOT / 'history/version_0_28/next_source_targets.json')['targets']
by_id = {target['id']: target for target in old_targets if target.get('id')}
assert set(updates) <= set(by_id)
for compound in ['DA28-SP-02', 'DA28-SP-03']:
    assert updates[compound]['whole_target_retired'] is False
assert 'SeedIVAlt' in updates['DA28-SP-02']['remaining_human_scope']
assert 'case-III' in updates['DA28-SP-03']['remaining_human_scope']
for geometry in ['DA26-SP-01', 'DA26-SP-03']:
    assert any('ImageDense' in item for item in updates[geometry]['retained_inputs'])
    assert 'Actual CountIII' in updates[geometry]['downstream_paired_count_cut']
for update in read(AUDIT / 'global_branch_scope_updates.json')['updates']:
    matches = [target for target in old_targets
               if all(target.get(key) == value for key, value in update['match'].items())]
    assert len(matches) == 1
    assert all(matches[0][key] == update['source'][key]
               for key in ['path', 'line_start', 'line_end', 'sha256', 'range_sha256'])

names = ['obligation_map.json', 'source_anchors.json', 'retirement_candidates.json',
         'target_scope_updates.json', 'global_branch_scope_updates.json']
bindings = {name: sha(AUDIT / name) for name in names}
notes = """ROOT MATHEMATICAL SCOPE REVIEW — VERSION 0.29
Reviewer: /root, an assistant agent; review of the human-readable reconstruction.
Result: PASS for the finite sufficient-obligation map and its stated scope.

This is a review of mathematical scope and application hypotheses, not a
kernel verification, exhaustive Lean dependency extraction, or completion
percentage.  The separate source audit verifies all referenced source ranges.

1. The completed endpoint is the literal implication PMExAlt => CountII.
SX8 supplies the original SeedIIAlt; UX12 constructs the actual original
Ctx2 ProModAlt witness; YX1 applies IX on that same datum and fixed embedding;
YX2 uses the pointwise G1/rigidity arguments, the original model, catalogue,
trace inequality and normalized coefficient return.  Its exponent is chosen
before every varying host, coefficient, character and point parameter.  The
factor two and original valuation normalization in the count are preserved.

2. The selected case-II traversal does not import full two-case ImageDense,
SeedIVAlt, case-III realization or CountIII.  Its only retained substantive
arithmetic leaf is ACTUAL_RANK_FOUR_HECKE_SUPPORT.  Other leaves in this
traversal are already written suppliers or explicitly named and matched
classical inputs.  The graph records sufficient routes, not necessary or
minimal hypotheses.  The proof-step bindings, not only graph edges, govern
which part of a prior argument is used.

3. QX10 reconstructs all five PMEx fields from rank-four HidaPropsAlt plus
P1core on the same ideal for each of the two actual Links.  The six Hida
fields cannot be supplied by unrelated ideals.  The fixed embedding,
universal rings, weight maps and common coefficient threshold are shared;
the threshold precedes all later coefficient and Space choices.  KX's
universal Pair quotient and QX's characteristic-zero tangent argument do
not construct this arithmetic Hecke/support input.  P3core and the larger
all-rank HidaUAlt/ModUAlt or printed-source records are not promoted.

4. Two scope corrections were required during root review.  QX2 directly
reproves the generic finite-point/dual-number capture subargument identified
with DX5; the map no longer imports the full Raw/Good local-base constructor.
UX6 uses the finite-entry and torus constructions of FP1/2/5 and UX7 proves
its actual ordinary-cone obstruction using FP7's relation-detection argument.
The map no longer implies an application of full FP8 with unsupplied local
antecedents.  These changes clarify proof-step reuse; no new mathematical
endpoint or proof text was created by altering graph edges.

5. Universal arithmetic retains the original nonempty-Pair antecedent.
QX supplies it in its selected application.  SX retains the original tower,
residual entries, local flags and fixed embedding.  UX chooses the residual
label, initial tower and separating element before lattice normalization;
later towers are compatible extensions.  Its uniform cohomology constant
precedes later layers and coefficients, and final descent returns to the
original valued point and exact residue field.  The final coefficient ring
need not itself be a DVR.  These qualifiers agree with the reviewed texts.

6. The added height route retains CountI, CountIII, CountV and PMExAlt.
The earlier CountI/CountV/full-ImageDense route remains an alternative.
The full G1/G2 continuation records retain their sufficient ImageDense
input; PMExAlt plus CountIII is labeled only as a downstream paired-count
route, since a count alone does not construct the case-III geometry.
The old II/IV seed and II/III realization targets are compound records:
closing their case-II parts does not retire them.  Zero whole-target
retirements is therefore correct.  The global VWinAt update matches its
original exact source range and retains the prime-pair/host hypotheses
and separate family, gap, theta/local, denominator and spectral branches.

7. Every prior semantic node identity remains.  Each modified prior node
contains its exact preceding snapshot.  The claim/source ledgers and old
mathematical-reference edges are preserved separately by the release audit.
These integrity checks bind reviewed assertions to the supplied texts;
they do not prove the remaining arithmetic producers.

BOUND FINAL FILES
"""
notes += '\n'.join(f'{name}: {digest}' for name, digest in bindings.items()) + '\n'
(OUT / 'semantic_scope_review.txt').write_text(notes)
record = {
    'schema': 'rh-root-semantic-scope-validation/1',
    'version': '0.29', 'reviewer': '/root', 'result': 'PASS',
    'scope': 'Finite sufficient-obligation map; mathematical review of prose scope with structural binding checks, not formal verification',
    'bound_sha256': bindings,
    'review_text_sha256': sha(OUT / 'semantic_scope_review.txt'),
    'prior_node_count': len(old_nodes), 'current_node_count': len(nodes),
    'changed_prior_node_ids_with_exact_snapshot': sorted(changed),
    'case_two_transitive_node_count': len(case_two),
    'case_two_leaf_ids': leaves,
    'case_two_retained_substantive_leaf_ids': open_leaves,
    'case_two_has_no_case_three_case_four_or_full_image_density_dependency': True,
    'scope_update_ids_match_prior_targets': sorted(updates),
    'whole_target_retirements': 0,
    'unresolved_findings': [],
}
(OUT / 'semantic_scope_validation.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'result': record['result'], 'nodes': len(nodes),
                  'case_two_nodes': len(case_two), 'open_leaves': open_leaves,
                  'bindings': bindings}, indent=2))
