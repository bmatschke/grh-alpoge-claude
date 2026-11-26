#!/usr/bin/env python3
"""Compute overlap of current open obligations across the two final targets."""
from pathlib import Path
import collections,hashlib,json
ROOT=Path(__file__).resolve().parent;AUD=ROOT/'dependency_audit_v0_41'
read=lambda p:json.loads(p.read_text())
g=read(AUD/'obligation_map.json');nodes={n['id']:n for n in g['nodes']}
def reach(k):
 seen=set();todo=[k]
 while todo:
  q=todo.pop()
  if q in seen:continue
  seen.add(q);todo+=nodes[q]['requires']
 return seen
opened={n['id'] for n in read(AUD/'remaining_leaf_register.json')['records']}
rh=reach('ORDINARY_RH')&opened;grh=reach('DIRICHLET_GRH')&opened
shared=rh&grh
result=dict(artifact_version='0.41',graph_file='dependency_audit_v0_41/obligation_map.json',
 graph_sha256=hashlib.sha256((AUD/'obligation_map.json').read_bytes()).hexdigest(),
 ordinary_rh_open_leaf_count=len(rh),dirichlet_grh_open_leaf_count=len(grh),
 shared_open_leaf_count=len(shared),shared_open_leaf_ids=sorted(shared),
 shared_categories=dict(sorted(collections.Counter(nodes[k]['category'] for k in shared).items())),
 ordinary_rh_only_open_leaf_ids=sorted(rh-grh),dirichlet_grh_only_open_leaf_ids=sorted(grh-rh),
 meaning='Reachability in the retained selected sufficient graph. These are exact dependency counts, not weights of difficulty, completion percentages or proof of a globally minimal route.')
assert len(rh)==len(shared)==26 and len(grh)==33 and not rh-grh
(AUD/'route_coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k.endswith('_count') or k=='shared_categories'},indent=2))
