#!/usr/bin/env python3
"""Audit v0.20 preservation and the exact v0.21 human dependency graph.

Run from any working directory after the cumulative v0.21 merge. This
checks recorded dependencies and file identity, not Lean kernel proofs.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_20'
REV = ROOT / 'reviews_v0_21'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
# Fixed from the frozen v0.20 package, independently compared with its
# original work/v0_20/SHA256SUMS before preparing this portable validator.
PRIOR_MANIFEST_SHA256 = '9aa87d046384be2e6bc45ec00e695b8e95b726e4b850f009b987f39ae1df06be'
COMPONENTS = {
    'nonempty_realization': ('NR', 24),
    'canonical_weil': ('CW', 25),
    'geometric_volumes': ('GV', 21),
    'centered_character_sums': ('CC', 20),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


prior = read(OLD / 'provenance.json')
now = read(ROOT / 'provenance.json')
assert prior['commit'] == now['commit'] == PIN
assert len(prior['claims']) == 983
assert len(prior['source_files']) == 2106
claims = {claim['id']: claim for claim in now['claims']}
assert len(claims) == len(now['claims']) == 1073
prior_ids = {claim['id'] for claim in prior['claims']}
assert len(prior_ids) == 983
expected_new = {
    f'{prefix}{i}'
    for prefix, count in COMPONENTS.values()
    for i in range(1, count + 1)
}
assert len(expected_new) == 90 and not prior_ids & expected_new
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
assert len(checked) == len(set(checked)) == 996
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
config = read(ROOT / 'increment_v0_21.json')
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

report = f'''CONTINUITY AND DEPENDENCY AUDIT: VERSION 0.21
Result: PASS
Method: audit_continuity_v0_21.py
Pinned source: {now['commit']}

All {len(prior['claims'])} predecessor claims preserve every original field,
including statements, exact source arrays, proof/status fields and earlier
annotations. New version annotations are additive. All {len(prior['source_files'])}
predecessor source-file records, all old mathematical dependency adjacency
lists and every previous version-local conclusion object are unchanged.

The cumulative ledger has {len(claims)} distinct claims. Its {len(expected_new)} new
claims are exactly NR1--NR24, CW1--CW25, GV1--GV21 and CC1--CC20. Every new
source array and dependency list agrees with its component ledger. The
stored topological order contains every claim exactly once and respects
every edge. The recorded human dependency graph is acyclic.

All {len(checked)} entries of the v0.20 checksum manifest match preserved
bytes. The manifest itself matches its independently fixed predecessor
SHA256. The {len(archived)} replaced or retired root files are archived in
history/version_0_20/; all other old files remain at their prior relative
paths. Including the preserved manifest, all {len(checked)+1} predecessor
package files remain. The historical PDF is unchanged and does not render
this increment.

All four independent global-branch records are exactly equal as JSON
values to the predecessor map. The current map contains
{len(targets['targets'])} precise source ranges. Configured retired targets
are absent; their historical records remain. A completed conditional
endpoint is not converted into an unconditional construction by removal
from the work map. Stronger record interfaces stay visible separately.

All previously recorded constructor/consumer guards remain. In particular,
the initial realizer, initial size, theta phase, finite indicator, rational
descent, bare stage, AR series descent, QW mass window and v0.20 GA/WA/MF/QR
construction-before-join boundaries preserve their original edges.

NEW CONSTRUCTOR/CONSUMER CHECKS
NR's completion and finite quotient constructions precede the all-prime
family they supply. Its character normalization does not depend on the
installed RingSpec or inducing-reading consequences. Finite coefficient
descent and the universal reading comparison precede the final bounded
row-family join; GalEx, RowCusp, ChebSplit and SideA remain hypotheses.

The finite and real CW actions precede their adelic and rational
comparison. The real Gaussian integral CW20 precedes the test-series
unfolding CW19, despite numerical paragraph order. The explicit eta
normalization does not use the final full-Weil record. CW24's actual
prescribed-character construction does not require CW23's separate
universal IsEtaTilde premise. CW25 joins the new full Weil supplier with
WA16/WA17's previously conditional bottom construction and period fields.

GV11's direct definite quotient-to-mass identity is independent of GV10's
named unitary Tamagawa theorem. GV13 explicitly joins these two inputs.
The UnitSplit argument is independent of the volume equality it later
supplies, while retaining the named Hasse--Minkowski theorem. The trueVol
stage result uses the same IG12 stage and GV16; the final conditional Core
join keeps HF20's exact remaining fields and classical representation
premises rather than transporting a dependent Core automatically.

CC's analytic inputs precede its uniform psi estimate, centered integral
and thinning conclusion. The abstract exponential-tail argument CC15 and
quadratic conductor restriction CC17 use no later CC endpoint. The bounded
modulus exclusion is independent of the host join. CC19 supplies ThinH to
HC9 without using that consumer as a dependency. RealBox, simultaneous
PairEx, relative progression and the distinct polynomial-window estimates
remain separate requirements.

These checks validate recorded preservation and dependency claims. They
are not an automated mathematical proof checker, a transitive Lean
dependency audit, a Lean build, a kernel replay or a complete RH/GRH proof.
No current PDF or visual layout review is asserted.

Current provenance SHA256: {sha(ROOT / 'provenance.json')}
Preserved v0.20 provenance SHA256: {sha(OLD / 'provenance.json')}
Preserved v0.20 manifest SHA256: {sha(OLD / 'SHA256SUMS')}
Current next-target map SHA256: {sha(ROOT / 'next_source_targets.json')}
Current increment configuration SHA256: {sha(ROOT / 'increment_v0_21.json')}
Audit script SHA256: {sha(Path(__file__))}
'''
REV.mkdir(exist_ok=True)
(REV / 'continuity_audit.txt').write_text(report)
print(json.dumps({'result':'PASS','old_claims':len(prior['claims']),
 'new_claims':len(expected_new),'claims':len(claims),
 'predecessor_files_preserved':len(checked)+1,'archived_root_files':len(archived),
 'current_target_ranges':len(targets['targets']),'human_graph_acyclic':True}))
