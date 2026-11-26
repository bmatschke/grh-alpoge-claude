#!/usr/bin/env python3
"""Validate the complete reconstructed release against its original baseline."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_57.json')
stats=read(ROOT/'integration_stats_v0_57.json')
ledger=read(ROOT/'provenance.json')
old=read(ROOT/'history/version_0_56/provenance.json')
assert len(old['claims'])==3645
assert ledger['claims'][:len(old['claims'])]==old['claims']
new=ledger['claims'][len(old['claims']):]
assert len(new)==stats['new_claims']
assert len(ledger['claims'])==stats['cumulative_claims']

audit_path=ROOT/'reviews_v0_57/integration_arithmetic_common_frame.json'
audit=read(audit_path)
assert audit['status']=='PASS' and not audit['errors']
assert audit['statistics']==stats
assert audit['exact_whole_closures']==cfg['closed_selected_leaves']
for p,h in audit['input_bindings'].items():
    assert sha(ROOT/p)==h,('independent release audit input changed',p)

registry=read(ROOT/'reviews_v0_57/review_registry.json')
covered=set()
new_claims={c['id']:c for c in new}
for comp in registry['complete_component_reviews']:
    intended=set(comp['claims']);seen=set()
    assert comp['result']=='PASS'
    for r in comp['independent_reviews']:
        assert r['reviewer']!=comp['author']
        assert sha(ROOT/r['review_file'])==r['review_sha256']
        assert sha(ROOT/r['proof_file'])==r['proof_file_sha256']
        raw=(ROOT/r['proof_file']).read_bytes()
        for cid,h in r['proof_hashes'].items():
            pl=new_claims[cid]['proof_location']
            block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
            assert hashlib.sha256(block).hexdigest()==h,(cid,'independent block review changed')
        seen.update(r['claims'])
    assert seen==intended
    covered.update(seen)
assert covered==set(new_claims)

previous=(ROOT/'RH_readable_reconstruction_v0_56.tex').read_text()
current=(ROOT/'RH_readable_reconstruction_v0_57.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_56/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
end=r'\section{The arithmetic still to be written out}'
assert previous[previous.index(marker):previous.index(end)]==current[current.index(marker):current.index(end)],'Historical cumulative proof body changed'
short=(ROOT/'RH_new_proofs_v0_57.tex').read_text()
for c in new:
    pl=c['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert hashlib.sha256(part).hexdigest()==pl['sha256'],c['id']
    assert sha(ROOT/pl['file'])==pl['file_sha256'],c['id']
    for text in [short,current]:
        assert '% BEGIN '+c['id'] in text and '% END '+c['id'] in text,('assembled claim absent',c['id'])

tex=read(ROOT/'tex_validation.json')
assert tex['artifact_version']=='0.57' and len(tex['documents'])==2
oldtex=read(ROOT/'history/version_0_56/tex_validation.json')
old_overfull=next(d['overfull_box_warnings'] for d in oldtex['documents'] if 'readable_reconstruction' in d['tex_filename'])
for item in tex['documents']:
    assert item['tex_sha256']==sha(ROOT/item['tex_filename'])
    assert item['syntax_compile_succeeded'] and not item['undefined_references_or_citations']
    assert not item['missing_character_warnings']
    assert not item['pdf_generated'] and not item['pdf_visual_review_performed']
    assert not any('multiply defined' in w for w in item['warnings'])
    if item['tex_filename']=='RH_new_proofs_v0_57.tex':assert item['overfull_box_warnings']==0
    else:assert item['overfull_box_warnings']<=old_overfull

snapshot=read(ROOT/'source_snapshot_v0_57/manifest.json')
assert snapshot['commit']==cfg['source_commit']
for rec in snapshot['files']:
    assert sha(ROOT/rec['snapshot_path'])==rec['sha256'],rec['path']

result={'artifact_version':'0.57','date':'2026-11-24','result':'PASS','source_commit':cfg['source_commit'],
 'baseline_claims_preserved':len(old['claims']),'new_claims':len(new),'cumulative_claims':len(ledger['claims']),
 'baseline_manifest_artifacts_preserved':audit['baseline_manifest_artifacts_preserved'],
 'baseline_files_retained_in_history':audit['baseline_artifacts_retained_in_history'],
 'historical_cumulative_proof_body_preserved_verbatim':True,
 'all_new_claims_independently_reviewed_in_stated_scope':True,
 'mathematical_review_registry':'reviews_v0_57/review_registry.json',
 'independent_integration_and_scope_audit':{'file':str(audit_path.relative_to(ROOT)),'sha256':sha(audit_path),'status':'PASS'},
 'selected_graph_sha256':sha(ROOT/'dependency_audit_v0_57/obligation_map.json'),
 'selected_route_statistics':stats,'closed_selected_whole_leaves':sorted(cfg['closed_selected_leaves']),
 'source_files_new_increment_verified_against_pin':stats['new_source_files_checked'],
 'unique_source_ranges_new_increment_verified':stats['new_unique_source_ranges_checked'],
 'source_snapshot_manifest_sha256':sha(ROOT/'source_snapshot_v0_57/manifest.json'),
 'tex_validation':tex,'lean_build':False,'kernel_replay':False,'pdf_generated':False,
 'new_edition_overfull_box_warnings':0,
 'historical_cumulative_overfull_box_warnings_preserved':old_overfull,
 'limitations':[
  'This is a partial human reconstruction of the accepted formal proof.',
  'The mathematical graph records the human argument, not a mechanically extracted Lean transitive dependency graph.',
  'The independent reviews are mathematical and source-contract reviews, not formal proofs or kernel replay.',
  'Draft TeX checks syntax and references. No PDF rendering or visual layout certification is claimed.',
  'Completed conditional implications retain their printed original inputs. All remaining producers are in the current register and roadmap.',
  'Claim and obligation counts are inventories, not percentages of completion.'
 ]}
dump(ROOT/'validation_v0_57.json',result)
print(json.dumps({k:result[k] for k in ['result','baseline_claims_preserved','new_claims','cumulative_claims','selected_route_statistics']},indent=2))
