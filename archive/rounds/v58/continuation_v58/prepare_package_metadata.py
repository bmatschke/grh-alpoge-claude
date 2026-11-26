#!/usr/bin/env python3
"""Write the portable v0.58 entry points without modifying v0.57 artifacts."""
from pathlib import Path
import hashlib
import json
import shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent
def read(path):return json.loads(path.read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4194304),b''):h.update(block)
    return h.hexdigest()
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

old=read(OUT/'RH_reconstruction_v0_57_delivery.json')
stats=read(ROOT/'integration_stats_v0_57.json')
coverage=read(ROOT/'dependency_audit_v0_57/route_coverage.json')
source=read(HERE/'source/source_bundle.json')
assert old['archive_sha256']=='b326cc620d0064eda3126cce27f3dafd31e83d8516741aaf2ffcac450788bd33'
assert stats['cumulative_claims']==3746 and stats['open_count']==24
history=HERE/'history';history.mkdir(exist_ok=True)
shutil.copy2(OUT/'RH_reconstruction_v0_57_delivery.json',history/'RH_reconstruction_v0_57_delivery.json')
readers=['RH_readable_reconstruction_v0_57.tex','RH_new_proofs_v0_57.tex',
 'RH_reconstruction_progress_v0_57.txt','RH_GRH_reconstruction_roadmap_v0_57.txt',
 'RH_GRH_parallel_execution_plan_v0_57.txt','RH_dependency_audit_v0_57.txt']
data={'schema':'rh-portable-continuation-checkpoint/1','package_version':'0.58',
 'date':'2026-11-24','mathematical_edition':'0.57',
 'purpose':'A complete portable continuation package starting from the latest delivered v0.57.',
 'primary_baseline':{'archive':old['archive'],'sha256':old['archive_sha256'],
                     'bytes':old['archive_bytes'],'members':old['archive_members']},
 'mathematical_state':{'new_claims_in_this_package':0,'cumulative_claims':3746,
   'whole_open_obligations':24,'selected_graph_nodes':121,'selected_graph_edges':161,
   'shared_rh_grh_open':17,'additional_unrestricted_dirichlet_grh_open':7,
   'new_whole_obligation_closures':[],
   'global_local_gain':'Remains fully closed at its original v0.49 scope.',
   'scope':'Partial human reconstruction of the accepted original formal proof; no new mathematical conclusions in package v0.58.'},
 'entry_points':{'start':'RH_START_HERE_v0_58.txt','new_chat_prompt':'RH_NEW_CHAT_PROMPT_v0_58.txt',
   'source_access':'continuation_v58/SOURCE_ACCESS.txt',
   'next_tasks':'continuation_v58/next_tasks_source_index.txt',
   'current_mathematical_checkpoint_after_unpack':'continuation_checkpoint.json',
   'current_claim_ledger_after_unpack':'provenance.json'},
 'restore_commands':['python3 continuation_v58/unpack_reconstruction.py',
                     'python3 continuation_v58/restore_source.py --destination formal_source'],
 'preserved_reconstruction':{'metadata':'continuation_v58/reconstruction_bundle.json',
  'inventory':'continuation_v58/reconstruction_inventory.json','members':9551,
  'scope':'Every delivered v0.57 member remains at its original relative path and exact bytes after unpacking.'},
 'original_source':{'metadata':'continuation_v58/source/source_bundle.json',
  'commit':source['source_commit'],'tree':source['source_tree'],
  'tracked_files':source['tracked_files'],'tracked_bytes':source['tracked_bytes'],
  'complete_tracked_project_source':True,'offline_exact_shallow_git_restore':True,
  'third_party_dependencies':'Pins are retained in lake-manifest.json; previously supplied dependency snapshots are retained. Full dependency checkouts and compiled Lean artifacts are not part of this source snapshot.'},
 'direct_reading_files':[{'path':name,'sha256':sha(ROOT/name),'bytes':(ROOT/name).stat().st_size} for name in readers],
 'shared_open_ids':coverage['shared_open_leaf_ids'],
 'additional_grh_open_ids':coverage['dirichlet_grh_only_open_leaf_ids'],
 'next_parallel_tasks':['Actual local records, Herr class maps and quantitative comparison',
   'Rank-three exceptional presentation, Sharp, corner and thick-chain constructions',
   'Original Cartier LemmaM normal form and its existing DJW consumer',
   'Actual InHHC range equation and same-setting KExpTied installation'],
 'independent_handoff_audit':'continuation_v58/review/handoff_audit.json'}
dump(ROOT/'CURRENT_CHECKPOINT_v0_58.json',data)
shutil.copy2(HERE/'START_HERE.txt',ROOT/'RH_START_HERE_v0_58.txt')
shutil.copy2(HERE/'NEW_CHAT_PROMPT.txt',ROOT/'RH_NEW_CHAT_PROMPT_v0_58.txt')
print(json.dumps({'package_version':'0.58','mathematical_edition':'0.57','new_claims':0,
                  'cumulative_claims':3746,'whole_open':24,'source_files':source['tracked_files']}))
