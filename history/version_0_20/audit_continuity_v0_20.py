#!/usr/bin/env python3
"""Audit v0.19 preservation and the exact v0.20 human dependency graph.

Run from any working directory after the cumulative v0.20 merge. This
checks recorded dependencies and file identity, not Lean kernel proofs.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_19'
REV = ROOT / 'reviews_v0_20'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
# Fixed from the frozen v0.19 package, independently compared with its
# original work/v0_19/SHA256SUMS before preparing this portable validator.
PRIOR_MANIFEST_SHA256 = 'afe0557b418ef5bac9cd748b4ce8b6b5466da3740585394bb2decb75427e1f23'
COMPONENTS = {
    'adic_realization': ('GA', 23),
    'finite_weil_arithmetic': ('WA', 19),
    'mass_formula': ('MF', 20),
    'ray_prime_estimates': ('QR', 25),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


prior = read(OLD / 'provenance.json')
now = read(ROOT / 'provenance.json')
assert prior['commit'] == now['commit'] == PIN
assert len(prior['claims']) == 896
assert len(prior['source_files']) == 1972
claims = {claim['id']: claim for claim in now['claims']}
assert len(claims) == len(now['claims']) == 983
prior_ids = {claim['id'] for claim in prior['claims']}
assert len(prior_ids) == 896
expected_new = {
    f'{prefix}{i}'
    for prefix, count in COMPONENTS.values()
    for i in range(1, count + 1)
}
assert len(expected_new) == 87 and not prior_ids & expected_new
assert set(claims) == prior_ids | expected_new
for claim in prior['claims']:
    assert all(claims[claim['id']].get(k) == v for k, v in claim.items()), claim['id']

files = {entry['path']: entry for entry in now['source_files']}
assert len(files) == len(now['source_files'])
for entry in prior['source_files']:
    assert files[entry['path']] == entry, entry['path']

graph = now['mathematical_dependency_graph']
for cid, dependencies in prior['mathematical_dependency_graph'].items():
    assert graph[cid] == dependencies, cid
for component, (prefix, count) in COMPONENTS.items():
    raw = read(ROOT / component / 'provenance.json')
    component_claims = {claim['id']: claim for claim in raw['claims']}
    assert set(component_claims) == {f'{prefix}{i}' for i in range(1, count + 1)}
    for cid, claim in component_claims.items():
        assert graph[cid] == claim['depends_on'], ('component graph mismatch', cid)
        assert claims[cid]['sources'] == claim['sources'], ('component source mismatch', cid)

order = now['dependency_topological_order']
assert len(order) == len(set(order)) == len(claims)
positions = {cid: i for i, cid in enumerate(order)}
assert set(positions) == set(graph) == set(claims)
for cid, dependencies in graph.items():
    assert all(positions[dep] < positions[cid] for dep in dependencies), cid
for key, value in prior.items():
    if key.startswith('version_') and 'conclusion' in key:
        assert now[key] == value, key

archived = {path.name for path in OLD.iterdir() if path.is_file()}
assert len(archived) == 20
assert sha(OLD / 'SHA256SUMS') == PRIOR_MANIFEST_SHA256
checked = []
for line in (OLD / 'SHA256SUMS').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    path = OLD / relative if relative in archived else ROOT / relative
    assert path.is_file() and sha(path) == expected, relative
    checked.append(relative)
assert len(checked) == len(set(checked)) == 927
assert 'SHA256SUMS' not in checked

targets = read(ROOT / 'next_source_targets.json')
old_targets = read(OLD / 'next_source_targets.json')
assert targets['commit'] == PIN
assert len(targets['global_branches_unchanged']) == 4
assert targets['global_branches_unchanged'] == old_targets['global_branches_unchanged']
assert targets['target_count'] == len(targets['targets'])
completed_names = {
    'laws_of_ok', 'laws_all', 'exists_gLevH', 'levels_top_row_sym', 'til_ties',
    'formsTiedSym_std', 'hermitian_data_at_level_prime', 'colsTiedSym_std',
    'explicitConstants_parameterConditions_large', 'szRow_sizesAt', 'szRow_numAt',
    'exists_sizeData_explicit', 'exists_sizeData_over', 'exists_ranks_rankVal_frame',
    'chGood_of_host', 'exists_levCh_of_levelPrime',
}
assert not any(t['declaration'].split('.')[-1] in completed_names for t in targets['targets'])
config = read(ROOT / 'increment_v0_20.json')
assert set(config['components']) == set(COMPONENTS)


def target_key(target):
    return target['path'] + ':' + target['declaration'].split('.')[-1]


assert not any(target_key(t) in config['replaced_target_keys'] for t in targets['targets'])


def ancestors(cid):
    seen = set()

    def walk(node):
        for dep in graph[node]:
            if dep not in seen:
                seen.add(dep)
                walk(dep)

    walk(cid)
    return seen


# Preserve every previously identified constructor/consumer cycle boundary.
assert 'DR3' in graph['VE11'] and 'VE10' in graph['VE11']
assert set(graph['DR2']) == {'DR1', 'NB1', 'LP1', 'AD4'}
assert set(graph['DR3']) == {'DR2', 'AD4'}
assert not ancestors('TL13') & ({'FC19', 'VE9', 'VE10', 'VE11'} | {f'TG{i}' for i in range(1, 13)})
assert not ancestors('SZ11') & {'PN16', 'SZ8', 'SZ9'}
assert not ancestors('SZ13') & {'PN16', 'SZ8', 'SZ9', 'SZ11'}
assert 'PA15' not in ancestors('TA10')
assert 'PA15' not in ancestors('TA14')
assert not ancestors('CI13') & ({'TL13', 'FC19', 'VE10', 'VE11'} | {f'TX{i}' for i in range(1, 17)})
assert not ancestors('TX10') & {'TX11', 'TX12', 'TX15', 'TX16'}
assert not ancestors('CA2') & {'VI11', 'CA11', 'CA12', 'CA13'}
assert 'CA2' in ancestors('VI11')
assert 'VI11' in ancestors('CA11')
assert not ancestors('CA11') & {f'SE{i}' for i in range(1, 17)}
assert not ancestors('TD8') & {'TD9', 'TD13', 'TD14', 'TD15', 'TD16'}
assert not ancestors('TD1') & {'TD9', 'TD15', 'TD16'}
assert not ancestors('IG2') & {'IG3', 'IG4', 'IG7', 'IG10'}
assert not ancestors('LS13') & {f'LS{i}' for i in range(14, 23)}
assert 'LS13' in ancestors('LS15')
assert not ancestors('AR14') & {'AR22'}
assert not ancestors('AR21') & {'AR11', 'AR22'}
assert not ancestors('TT10') & {'TD15', 'TD16'}
assert not ancestors('QW1') & {'QW3', 'QW6', 'QW9'}
assert not ancestors('QW9') & {f'QW{i}' for i in range(10, 16)}

# New v0.20 guards follow the actual supplier/consumer distinctions.
assert not ancestors('GA8') & {f'GA{i}' for i in range(13, 24)}
assert not ancestors('GA17') & ({'GA16'} | {f'GA{i}' for i in range(18, 24)})
assert 'GA17' in ancestors('GA16')
assert not ancestors('GA18') & {'GA16', 'GA23'}
assert not ancestors('GA21') & {'GA22', 'GA23'}
assert not ancestors('WA3') & {
    'WA8', 'WA9', 'WA11', 'WA13', 'WA14', 'WA15', 'WA16', 'WA17', 'WA18', 'WA19',
    'TT13', 'TT16',
}
assert not ancestors('WA11') & {
    'TT13', 'TT16', 'WA13', 'WA14', 'WA15', 'WA16', 'WA17', 'WA18', 'WA19',
}
assert not ancestors('WA10') & {f'WA{i}' for i in range(1, 20) if i != 10}
assert not ancestors('MF6') & {'MF17', 'MF18', 'MF19', 'MF20', 'QW3', 'QW9'}
assert not ancestors('MF19') & {'MF20', 'QW3', 'QW9'}
assert {'MF19', 'QW9'} <= ancestors('MF20')
assert not ancestors('QR9') & {f'QR{i}' for i in range(10, 26)}
assert not ancestors('QR10') & {f'QR{i}' for i in range(1, 10)}
assert not ancestors('QR13') & {f'QR{i}' for i in range(14, 26)}
assert not ancestors('QR24') & ({f'QR{i}' for i in range(1, 10)} | {'QR25'})
assert {'QR9', 'QR24'} <= ancestors('QR25')

report = f'''CONTINUITY AND DEPENDENCY AUDIT: VERSION 0.20
Result: PASS
Method: audit_continuity_v0_20.py
Pinned source: {now['commit']}

All {len(prior['claims'])} predecessor claims preserve every original field,
including exact statements, source arrays, proof/status fields and earlier
version annotations. New annotations are additive. All {len(prior['source_files'])}
predecessor source-file records are exactly preserved. Every old mathematical
dependency adjacency list and every prior version-local conclusion object
is unchanged.

The cumulative ledger has {len(claims)} distinct claims. Its {len(expected_new)} new
claims are exactly GA1--GA23, WA1--WA19, MF1--MF20 and QR1--QR25. Every new
source array and dependency adjacency list agrees with the corresponding
component ledger. The stored topological order contains every claim once
and respects every edge; the human dependency graph is acyclic.

All {len(checked)} entries of the v0.19 checksum manifest match preserved
bytes. The manifest itself matches its fixed predecessor SHA256. Its
{len(archived)} root files are archived in history/version_0_19/;
all other old files remain at their prior relative paths. Including the
preserved manifest, all {len(checked) + 1} predecessor package files remain.
Any historical PDF retains its original bytes and is not a v0.20 rendering.

All four independent global branch records are exactly equal as JSON
values to the predecessor map. The current map contains
{len(targets['targets'])} precise source ranges. Configured retired targets are
absent from this map; their historical records remain in the archive.
Conditional endpoints are retired only at their proved source interface.
Nonempty compatible arithmetic data, full Core, canonical bottom-Weil
existence, quantitative dictionary and the remaining same-field analytic
and global hypotheses are not discharged by this target-map operation.

All earlier cycle guards are preserved. In particular, the original
initial-realizer, value-comparison, column-law, initial-size, theta-phase,
finite-indicator, rational-descent and bare-stage supply boundaries remain.
AR weight/series descent still precedes the final rank join. The QW mass
window retains its original conditional adjacency list; MF supplies its
mass premise through a later explicit join without rewriting QW9.

NEW CONSTRUCTOR/CONSUMER CHECKS
The normalized adic-character construction GA8 does not depend on its
installed-reading consequences. GA17's direct local unit calculation is
independent of the later host character law GA16 that uses it. The local
IsGalOf calculation and the splitting-character comparison do not use
the final same-object arithmetic rank join.

The finite Heisenberg algebraic expansion WA3 and finite-Weil conclusion
WA11 do not depend on the conditional TT jet/bottom consumers they supply.
WA10's local unitary generation uses no finite-Weil endpoint. MF's local
density and global mass law do not depend on the conditional QW mass
window; MF20 explicitly joins MF19 with that previously proved window.

QR9 constructs the literal arithmetic LFam without the later analytic
estimates. QR10--QR24 prove those estimates for a supplied family, with
the Mellin and Bessel arguments preceding the zero-region/prime bounds.
QR24 does not use QR1--QR9 or the final application QR25. QR25 explicitly
joins QR9's actual family with QR24's uniform weighted interval theorem.

These checks validate the recorded human proof graph and preservation
claims. They are not an automated mathematical proof checker, a Lean
dependency audit, a Lean build, a kernel replay or a complete RH/GRH proof.
No new PDF or visual layout review is asserted.

Current provenance SHA256: {sha(ROOT / 'provenance.json')}
Preserved v0.19 provenance SHA256: {sha(OLD / 'provenance.json')}
Preserved v0.19 manifest SHA256: {sha(OLD / 'SHA256SUMS')}
Current next-target map SHA256: {sha(ROOT / 'next_source_targets.json')}
Current increment configuration SHA256: {sha(ROOT / 'increment_v0_20.json')}
Audit script SHA256: {sha(Path(__file__))}
'''
REV.mkdir(exist_ok=True)
(REV / 'continuity_audit.txt').write_text(report)
print(json.dumps({
    'result': 'PASS',
    'old_claims_preserved': len(prior['claims']),
    'new_claims': len(expected_new),
    'total_claims': len(claims),
    'old_source_file_records_preserved': len(prior['source_files']),
    'old_package_files_preserved': len(checked) + 1,
    'archived_root_files': len(archived),
    'global_branches_unchanged': 4,
    'graph_acyclic': True,
}))
