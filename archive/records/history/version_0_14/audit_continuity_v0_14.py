#!/usr/bin/env python3
"""Audit predecessor preservation and the current human dependency graph."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_13'
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
assert len(archived)==18
checked=[]
for line in (OLD/'SHA256SUMS').read_text().splitlines():
    expected,relative=line.split('  ',1)
    p=OLD/relative if relative in archived else ROOT/relative
    assert p.is_file()and sha(p)==expected,relative
    checked.append(relative)
assert len(checked)==484
targets=read(ROOT/'next_source_targets.json')
old_targets=read(OLD/'next_source_targets.json')
assert targets['global_branches_unchanged']==old_targets['global_branches_unchanged']
assert targets['target_count']==len(targets['targets'])
assert not any(t['declaration'].split('.')[-1]in ['exists_isPtOf_cm','unimodGenus']for t in targets['targets'])
assert 'DR3'in graph['VE11']and'VE10'in graph['VE11']
assert set(graph['DR2'])=={'DR1','NB1','LP1','AD4'}
assert set(graph['DR3'])=={'DR2','AD4'}

text=f'''CONTINUITY AND DEPENDENCY AUDIT: VERSION 0.14
Result: PASS
Method: audit_continuity_v0_14.py
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
premises; the DR3/VE11 join explicitly discharges initial realization.
DR2 depends only on DR1, NB1, LP1 and AD4; DR3 only on DR2 and AD4.
No comparison or neighbor-naturality conclusion is used to construct
the initial realizer.

All {len(checked)} entries in the v0.13 checksum manifest match their
preserved bytes. Its {len(archived)} root files are archived under
history/version_0_13/; all other prior files remain at their old relative
paths. Including that preserved checksum manifest, all 485 predecessor
package files remain present. The historical PDF is unchanged and is
not presented as a current v0.14 rendering.

The four independent global branch records are byte-for-byte equal as
JSON values to the v0.13 map. The current map contains {len(targets['targets'])}
exact next-source ranges. Initial decorated-point realization and the
actual adelic genus target are removed as completed by DR1–DR3;
the stronger rational-semilocal genus route is bypassed, not asserted.

The audit does not assert a Lean build, kernel replay, complete RH/GRH
proof, or visual review of a newly rendered PDF.

Current provenance SHA256: {sha(ROOT/'provenance.json')}
Preserved v0.13 provenance SHA256: {sha(OLD/'provenance.json')}
Preserved v0.13 manifest SHA256: {sha(OLD/'SHA256SUMS')}
Current next-target map SHA256: {sha(ROOT/'next_source_targets.json')}
'''
(ROOT/'reviews_v0_14/continuity_audit.txt').write_text(text)
print(json.dumps({'result':'passed','old_claims_preserved':len(prior['claims']),
    'new_claims':len(claims)-len(prior['claims']),'old_files_preserved':len(checked)+1,
    'archived_root_files':len(archived),'graph_acyclic':True}))
