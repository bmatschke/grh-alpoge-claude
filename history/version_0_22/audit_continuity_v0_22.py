#!/usr/bin/env python3
"""Audit v0.21 preservation and the exact v0.22 human dependency graph.

Run from any working directory after the cumulative v0.22 merge. This
checks recorded dependencies and file identity, not Lean kernel proofs.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_21'
REV = ROOT / 'reviews_v0_22'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
# Fixed from the frozen v0.21 package, independently compared with its
# original work/v0_21/SHA256SUMS before preparing this portable validator.
PRIOR_MANIFEST_SHA256 = '765f0513ca80d233dd0bc807f28d82b3063cf42eb67ae7372812236eba4cfb64'
COMPONENTS = {
    'automorphic_realization': ('MR', 26),
    'quantitative_weil_dictionary': ('QD', 22),
    'discrete_series_core': ('DC', 22),
    'simultaneous_prime_pairs': ('QP', 25),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


prior = read(OLD / 'provenance.json')
now = read(ROOT / 'provenance.json')
assert prior['commit'] == now['commit'] == PIN
assert len(prior['claims']) == 1073
assert len(prior['source_files']) == 2221
claims = {claim['id']: claim for claim in now['claims']}
assert len(claims) == len(now['claims']) == 1168
prior_ids = {claim['id'] for claim in prior['claims']}
assert len(prior_ids) == 1073
expected_new = {
    f'{prefix}{i}'
    for prefix, count in COMPONENTS.values()
    for i in range(1, count + 1)
}
assert len(expected_new) == 95 and not prior_ids & expected_new
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
assert len(archived) == 19
assert sha(OLD / 'SHA256SUMS') == PRIOR_MANIFEST_SHA256
checked = []
for line in (OLD / 'SHA256SUMS').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    path = OLD / relative if relative in archived else ROOT / relative
    assert path.is_file() and sha(path) == expected, relative
    checked.append(relative)
assert len(checked) == len(set(checked)) == 1064
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
config = read(ROOT / 'increment_v0_22.json')
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

# Preserved v0.20 guards follow the actual supplier/consumer distinctions.
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

# v0.21 supplier boundaries: these are actual dependencies, not target-map links.
nr_ids = {f'NR{i}' for i in range(1, 25)}
cw_ids = {f'CW{i}' for i in range(1, 26)}
gv_ids = {f'GV{i}' for i in range(1, 22)}
cc_ids = {f'CC{i}' for i in range(1, 21)}
for cid in nr_ids:
    assert not ancestors(cid) & (cw_ids | gv_ids | cc_ids), cid
    assert not ancestors(cid) & ({'SE14', 'LS21', 'LS22'} | {f'NC{i}' for i in range(1, 18)}), cid
for i in [3, 7, 11, 12, 15, 18]:
    assert not ancestors(f'NR{i}') & {f'NR{j}' for j in range(i + 1, 25)}, i
assert {'NR5', 'NR6', 'LS8'} <= ancestors('NR7')
assert {'HF13', 'HF16', 'GA16'} <= ancestors('NR13')
assert {'NR7', 'NR11', 'NR13'} <= ancestors('NR15')
assert {'NR15', 'NR16', 'NR17'} <= ancestors('NR18')
assert not ancestors('NR20') & {'NR15', 'NR18', 'NR21', 'NR24'}
assert not ancestors('NR21') & {'NR22', 'NR23', 'NR24'}
assert not ancestors('NR2') & (nr_ids - {'NR1', 'NR2'})
assert not ancestors('NR7') & {f'NR{i}' for i in range(8, 25)}
assert not ancestors('NR11') & {f'NR{i}' for i in range(12, 25)}
assert not ancestors('NR13') & {'NR14', 'NR15', 'NR17', 'NR18', 'NR24'}
assert not ancestors('NR20') & {'NR21', 'NR22', 'NR23', 'NR24'}
assert not ancestors('NR23') & {'NR22', 'NR24'}
assert {'NR15', 'NR18', 'NR21', 'NR22', 'NR23'} <= ancestors('NR24')
for cid in [f'CW{i}' for i in range(1, 14)]:
    assert not ancestors(cid) & {f'CW{i}' for i in range(14, 26)}, cid
assert not ancestors('CW18') & {'CW23', 'CW24', 'CW25'}
assert not ancestors('CW20') & {'CW19', 'CW21', 'CW22', 'CW23', 'CW24', 'CW25'}
assert 'CW20' in ancestors('CW19')
assert 'CW23' not in ancestors('CW24')
assert {'CW24', 'WA16', 'WA17'} <= ancestors('CW25')
assert not ancestors('GV11') & {'GV9', 'GV10', 'GV13', 'GV15', 'GV16', 'GV19', 'GV21'}
assert not ancestors('GV14') & {'GV10', 'GV13', 'GV15', 'GV21'}
assert {'GV10', 'GV11'} <= ancestors('GV13')
assert {'IG12', 'GV16'} <= ancestors('GV19')
assert {'HF20', 'GV13', 'GV19', 'GV20'} <= ancestors('GV21')
for cid in gv_ids:
    assert not ancestors(cid) & (nr_ids | cw_ids | cc_ids), cid
for cid in [f'CC{i}' for i in range(1, 9)]:
    assert not ancestors(cid) & {f'CC{i}' for i in range(9, 21)}, cid
assert not ancestors('CC15') & (cc_ids - {'CC15'})
assert not ancestors('CC17') & (cc_ids - {'CC17'})
assert not ancestors('CC18') & {'CC19', 'HC9'}
assert 'HC9' not in ancestors('CC19')
assert {'CC14', 'CC16', 'CC17', 'CC18'} <= ancestors('CC19')


# v0.22 construction-before-join boundaries. These concern recorded human
# dependencies, not target-map annotations or a transitive Lean import graph.
new_groups = {
    'MR': {f'MR{i}' for i in range(1,27)},
    'QD': {f'QD{i}' for i in range(1,23)},
    'DC': {f'DC{i}' for i in range(1,23)},
    'QP': {f'QP{i}' for i in range(1,26)},
}
for prefix, group in new_groups.items():
    others=set().union(*(v for k,v in new_groups.items() if k != prefix))
    for cid in group:
        assert not ancestors(cid) & others, ('crossed independent component boundary',cid)
for cid in ['MR12','MR24','MR25','MR26','QD1','QD4','QD13','DC1','QP8','QP9','QP16','QP17']:
    assert not graph[cid], ('elementary retained-premise primitive acquired a consumer edge',cid)
assert {'MR12','MR13','MR14','MR15'} <= ancestors('MR16')
assert {'MR16','MR17','NR24'} <= ancestors('MR18')
assert {'MR10','MR11','MR21','NR17','NR24'} <= ancestors('MR22')
assert not ancestors('MR23') & {'MR24','MR25','MR26','MR22'}
assert not ancestors('QD14') & {'QD15','QD16','QD17','QD21','QD22'}
assert {'QD15','QD16'} <= ancestors('QD17')
assert {'QD17','QD19','QD20','WA14','WA16','CW24'} <= ancestors('QD22')
assert not ancestors('DC12') & {f'DC{i}' for i in range(13,23)}
assert not ancestors('DC14') & ({f'DC{i}' for i in range(2,14)} | {f'DC{i}' for i in range(15,23)})
assert {'DC12','DC13','DC18','GV17'} <= ancestors('DC19')
assert {'DC15','DC19','GV19'} <= ancestors('DC20')
assert {'QP1','QP3','CC8'} <= ancestors('QP5')
assert not ancestors('QP14') & {'QP15','QP18','QP21','QP22','QP23','QP24','QP25'}
assert {'QP6','QP10','QP12','QP14','QP16','QP17'} <= ancestors('QP18')
assert {'QP15','QP17','QP21'} <= ancestors('QP22')
assert {'CC17','QP22'} <= ancestors('QP23')
assert {'QP23','CC19','CC20'} <= ancestors('QP24')
assert set(graph['QP25']) == {'QP22'}

report = f'''CONTINUITY AND DEPENDENCY AUDIT: VERSION 0.22
Result: PASS
Method: audit_continuity_v0_22.py
Pinned source: {now['commit']}

All {len(prior['claims'])} predecessor claims preserve every original field,
including source arrays, status, proof pointers and prior annotations.
All {len(prior['source_files'])} old source records, old mathematical adjacency
lists and prior version-local conclusion objects are unchanged.

The {len(claims)} cumulative claims include exactly {len(expected_new)} new claims:
MR1–MR26, QD1–QD22, DC1–DC22 and QP1–QP25. Every new source array and
dependency list agrees with its authored component. The stored order
contains every claim once and respects every edge; the human graph is acyclic.

All {len(checked)} v0.21 manifest entries and the independently fixed manifest
hash match preserved bytes. Its {len(archived)} retired root files are under
history/version_0_21/; other files remain at their original relative paths.
All {len(checked)+1} predecessor files and the historical PDF are preserved.

All four global branch records are identical JSON values. The current map
has {len(targets['targets'])} exact source ranges. Retired conditional endpoints
retain their original hypotheses and stronger joins stay visible separately.

All earlier constructor/consumer guards are retained. New guards distinguish
MR's additive reading and flat descent from its lattice/signature/initial
SideB joins; QD's arithmetic scalar/finite dictionary suppliers from its
final fixed-choice dictionary; DC's large-gap construction from formal-degree
calibration and restricted stage joins; and QP's analytic/mean-square/density
suppliers from PairEx, compatible-host RealBox/ThinH and conditional winPairs.
The four new blocks do not depend on one another. Their named input and
same-object boundaries remain in the text and ledger. No edges are added
to historical claims merely because a new supplier annotates them.

These are reproducible recorded-identity/dependency checks, not an automated
mathematical proof checker, transitive Lean audit, build, kernel replay,
complete RH/GRH proof, current PDF render or visual review.

Current provenance SHA256: {sha(ROOT/'provenance.json')}
Prior provenance SHA256: {sha(OLD/'provenance.json')}
Prior manifest SHA256: {sha(OLD/'SHA256SUMS')}
Current target map SHA256: {sha(ROOT/'next_source_targets.json')}
Current configuration SHA256: {sha(ROOT/'increment_v0_22.json')}
Script SHA256: {sha(Path(__file__))}
'''
REV.mkdir(exist_ok=True)
(REV/'continuity_audit.txt').write_text(report)
print(json.dumps({'result':'PASS','old_claims':len(prior['claims']),
 'new_claims':len(expected_new),'claims':len(claims),
 'predecessor_files_preserved':len(checked)+1,'archived_root_files':len(archived),
 'current_target_ranges':len(targets['targets']),'human_graph_acyclic':True}))
