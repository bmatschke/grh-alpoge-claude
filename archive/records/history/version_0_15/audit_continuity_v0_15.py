#!/usr/bin/env python3
"""Audit predecessor preservation and the current human dependency graph."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_14'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

prior=read(OLD/'provenance.json')
now=read(ROOT/'provenance.json')
claims={c['id']:c for c in now['claims']}
assert len(claims)==len(now['claims'])
for c in prior['claims']:
    assert all(claims[c['id']].get(k)==v for k,v in c.items()),c['id']
files={f['path']:f for f in now['source_files']}
for f in prior['source_files']:assert files[f['path']]==f,f['path']
graph=now['mathematical_dependency_graph']
for cid,deps in prior['mathematical_dependency_graph'].items():
    assert graph[cid]==deps,cid
order=now['dependency_topological_order']
assert len(order)==len(set(order))==len(claims)
positions={c:i for i,c in enumerate(order)}
assert set(positions)==set(graph)==set(claims)
for cid,deps in graph.items():
    assert all(positions[d]<positions[cid]for d in deps),cid
for k,v in prior.items():
    if k.startswith('version_')and'conclusion'in k:assert now[k]==v,k

archived={p.name for p in OLD.iterdir()if p.is_file()}
assert len(archived)==20
checked=[]
for line in (OLD/'SHA256SUMS').read_text().splitlines():
    expected,relative=line.split('  ',1)
    p=OLD/relative if relative in archived else ROOT/relative
    assert p.is_file()and sha(p)==expected,relative
    checked.append(relative)
assert len(checked)==574
targets=read(ROOT/'next_source_targets.json')
old_targets=read(OLD/'next_source_targets.json')
assert targets['global_branches_unchanged']==old_targets['global_branches_unchanged']
assert targets['target_count']==len(targets['targets'])
completed_names=['laws_of_ok','laws_all','exists_gLevH','levels_top_row_sym','til_ties',
                 'formsTiedSym_std','hermitian_data_at_level_prime','colsTiedSym_std',
                 'explicitConstants_parameterConditions_large','szRow_sizesAt','szRow_numAt',
                 'exists_sizeData_explicit','exists_sizeData_over','exists_ranks_rankVal_frame',
                 'chGood_of_host','exists_levCh_of_levelPrime']
assert not any(t['declaration'].split('.')[-1]in completed_names for t in targets['targets'])
assert 'DR3'in graph['VE11']and'VE10'in graph['VE11']
assert set(graph['DR2'])=={'DR1','NB1','LP1','AD4'}
assert set(graph['DR3'])=={'DR2','AD4'}
def ancestors(cid):
    seen=set()
    def walk(node):
        for dep in graph[node]:
            if dep not in seen:
                seen.add(dep); walk(dep)
    walk(cid)
    return seen
assert not ancestors('TL13') & ({'FC19','VE9','VE10','VE11'} | {f'TG{i}'for i in range(1,13)})
assert not ancestors('SZ11') & {'PN16','SZ8','SZ9'}
assert not ancestors('SZ13') & {'PN16','SZ8','SZ9','SZ11'}

text=f'''CONTINUITY AND DEPENDENCY AUDIT: VERSION 0.15
Result: PASS
Method: audit_continuity_v0_15.py
Pinned source: {now['commit']}

All {len(prior['claims'])} predecessor claims preserve every original field,
including source arrays, exact statements, original proof/status fields
and all earlier version annotations. Current annotations are additive.
All {len(prior['source_files'])} predecessor source-file records are exactly
preserved. Every old mathematical dependency adjacency list is unchanged.
All prior version-local conclusion objects are unchanged.

The cumulative ledger contains {len(claims)} distinct claims, including
{len(claims)-len(prior['claims'])} new claims, with an acyclic mathematical
dependency graph. Its stored topological order was checked against every
edge. This is the reconstruction's human proof graph, not a transitive
Lean dependency audit. Conditional FC/NB/AD proofs retain their original
premises; new discharge annotations are explicit. TL13 has no dependency
on completed Forms0, value comparison or terminal TG conclusions. SZ11
has no dependency on PN16 or final SizesAt/NumAt; SZ13 also precedes the
initial size constructor. These checks enforce the identified cycle
boundaries, in addition to the complete graph topological check.
The earlier DR2/DR3 initial-realizer dependency boundaries are preserved.

All {len(checked)} entries in the v0.14 checksum manifest match their
preserved bytes. Its {len(archived)} root files are archived under
history/version_0_14/; all other prior files remain at their old relative
paths. Including that preserved checksum manifest, all 575 predecessor
package files remain present. The historical PDF is unchanged and is
not presented as a current v0.15 rendering.

The four independent global branch records are byte-for-byte equal as
JSON values to the v0.14 map. The current map contains {len(targets['targets'])}
exact next-source ranges. Completed laws, reference terminal geometry,
parameter/size records and conditional arithmetic constructors have been
removed. Canonical analytic/local suppliers, all-twist comparisons,
primitive host and geometric/prime-window inputs remain explicit.

The audit does not assert a Lean build, kernel replay, complete RH/GRH
proof, or visual review of a newly rendered PDF.

Current provenance SHA256: {sha(ROOT/'provenance.json')}
Preserved v0.14 provenance SHA256: {sha(OLD/'provenance.json')}
Preserved v0.14 manifest SHA256: {sha(OLD/'SHA256SUMS')}
Current next-target map SHA256: {sha(ROOT/'next_source_targets.json')}
'''
(ROOT/'reviews_v0_15/continuity_audit.txt').write_text(text)
print(json.dumps({'result':'passed','old_claims_preserved':len(prior['claims']),
    'new_claims':len(claims)-len(prior['claims']),'old_files_preserved':len(checked)+1,
    'archived_root_files':len(archived),'graph_acyclic':True}))
