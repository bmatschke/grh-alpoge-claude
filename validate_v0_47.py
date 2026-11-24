#!/usr/bin/env python3
"""Validate the assembled release and its independently audited continuation data."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cfg=read(ROOT/'increment_v0_47.json')
stats=read(ROOT/'integration_stats_v0_47.json')
ledger=read(ROOT/'provenance.json')
old=read(ROOT/'history/version_0_46/provenance.json')
assert ledger['claims'][:len(old['claims'])]==old['claims']
new=ledger['claims'][len(old['claims']):]
assert len(new)==stats['new_claims']

audit=read(ROOT/'reviews_v0_47/integration_main_proof_rigidity.json')
assert audit['status']=='PASS' and not audit['errors']
assert audit['statistics']==stats
for p,h in audit['input_bindings'].items():
    assert sha(ROOT/p)==h,('independent integration audit input changed',p)
assert audit['exact_whole_closures']==cfg['closed_selected_leaves']

semantic_path=ROOT/'reviews_v0_47/semantic_scope_ordinary_structure.json'
semantic=read(semantic_path)
assert semantic['status']=='PASS' and not semantic['material_corrections_required']
for item in semantic['reviewed_files']+semantic['generated_outputs_reviewed']:
    assert sha(ROOT/item['path'])==item['sha256'],('semantic review input changed',item['path'])

authors=cfg['component_authors']
review_registry=[];covered=set()
for component in cfg['components']:
    component_claims={c['id']:c for c in read(ROOT/component/'provenance.json')['claims']}
    intended=set(component_claims);component_covered=set();review_files=[]
    for review_path in sorted((ROOT/component).glob('review_*.json')):
        location=review_path.relative_to(ROOT).as_posix();r=read(review_path)
        assert str(r.get('result',r.get('status',''))).startswith('PASS'),location
        for key in ['unresolved_findings','issues','corrections_requested','required_corrections',
                    'corrections_required','material_corrections_required']:
            assert not r.get(key,[]),(location,key)
        proof=r.get('proof_file',r.get('reviewed_file'))
        if isinstance(proof,dict):proof=proof['file']
        expected=r.get('proof_sha256',r.get('proof_file_sha256',r.get('reviewed_sha256')))
        assert proof==component+'/main.tex' and sha(ROOT/proof)==expected,('review proof binding',location)
        reviewer=r['reviewer'].removeprefix('/root/')
        assert reviewer!=authors[component],('reviewer is author',location)
        assert r['source_commit']==cfg['source_commit'],('review source pin',location)
        hashes=dict(r.get('proof_hashes',{}))
        claimed=r.get('claims_reviewed',r.get('reviewed_claims',r.get('blocks',r.get('claims',[]))))
        for x in claimed:
            if isinstance(x,str):
                assert x in hashes,('missing reviewed block hash',location,x)
            else:
                cid=x.get('id',x.get('claim'))
                h=x.get('block_sha256',x.get('proof_range_sha256',x.get('range_sha256',x.get('sha256'))))
                assert h,('missing reviewed block hash',location,cid)
                if cid in hashes:assert hashes[cid]==h
                hashes[cid]=h
        claimids=set(hashes)
        assert claimids and claimids<=intended,('review claim coverage',component,claimids,intended)
        for cid,h in hashes.items():
            pl=component_claims[cid]['proof_location']
            raw=(ROOT/pl['file']).read_bytes()
            block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
            assert h==hashlib.sha256(block).hexdigest(),('review block hash',location,cid)
        component_covered.update(claimids);covered.update(claimids)
        record={'review_file':location,'review_sha256':sha(review_path),
            'reviewer':reviewer,'proof_file':proof,'proof_sha256':expected,
            'claims':sorted(claimids),'claim_hashes':hashes,'result':'PASS'}
        review_files.append(record)
    assert component_covered==intended,('incomplete independent component review',component,intended-component_covered)
    review_registry.append({'component':component,'author':authors[component],
      'claims':sorted(intended),'independent_reviews':review_files,'coverage':'complete by union','result':'PASS'})
assert covered=={c['id'] for c in new}
write(ROOT/'reviews_v0_47/review_registry.json',{'artifact_version':'0.47',
   'complete_component_reviews':review_registry,
   'coverage':'Every new claim has an exact-block mathematical/interface review by an agent other than its author. Split reviews jointly cover each component. These reviews are not formal proofs or kernel replay.'})

# Verify the complete historical body is still present verbatim in the cumulative
# manuscript, not merely its separate preserved proof component files.
previous=(ROOT/'RH_readable_reconstruction_v0_46.tex').read_text()
current=(ROOT/'RH_readable_reconstruction_v0_47.tex').read_text()
old_audit=(ROOT/'dependency_audit_v0_46/main.tex').read_text()
marker=re.search(r'^\\section\{[^\n]+',old_audit,re.M)[0]
end=r'\section{The arithmetic still to be written out}'
previous_body=previous[previous.index(marker):previous.index(end)]
current_body=current[current.index(marker):current.index(end)]
assert current_body==previous_body,'Historical cumulative proof body changed'
short=(ROOT/'RH_new_proofs_v0_47.tex').read_text()
for c in new:
    pl=c['proof_location'];raw=(ROOT/pl['file']).read_bytes()
    part=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert hashlib.sha256(part).hexdigest()==pl['sha256'],('new proof range changed',c['id'])
    assert sha(ROOT/pl['file'])==pl['file_sha256'],('new proof file changed',c['id'])
    # Claim delimiters are retained through purely typographical line-break hints.
    begin='% BEGIN '+c['id'];finish='% END '+c['id']
    if begin in raw.decode():
        assert begin in current and finish in current and begin in short and finish in short,('assembled claim absent',c['id'])

tex=read(ROOT/'tex_validation.json')
assert tex['artifact_version']=='0.47' and len(tex['documents'])==2
for item in tex['documents']:
    assert item['tex_sha256']==sha(ROOT/item['tex_filename'])
    assert item['syntax_compile_succeeded'] and not item['undefined_references_or_citations']
    assert not item['missing_character_warnings']
    assert not item['pdf_generated'] and not item['pdf_visual_review_performed']
    assert not any('multiply defined' in w for w in item['warnings'])

# Source snapshot scope is checked by the independent audit; every snapshot file
# also has an explicit, distributable manifest binding.
snapshot=read(ROOT/'source_snapshot_v0_47/manifest.json')
assert snapshot['commit']==cfg['source_commit']
for rec in snapshot['files']:
    assert sha(ROOT/rec['snapshot_path'])==rec['sha256'],('snapshot changed',rec['path'])

result={
 'artifact_version':'0.47','date':'2026-11-23','result':'PASS','source_commit':cfg['source_commit'],
 'baseline_claims_preserved':len(old['claims']),'new_claims':len(new),'cumulative_claims':len(ledger['claims']),
 'baseline_manifest_artifacts_preserved':audit['baseline_manifest_artifacts_preserved'],
 'baseline_files_retained_in_history':audit['baseline_artifacts_retained_in_history'],
 'historical_cumulative_proof_body_preserved_verbatim':True,
 'all_new_claims_independently_reviewed_in_stated_scope':True,
 'mathematical_review_registry':'reviews_v0_47/review_registry.json',
 'independent_integration_audit':{'file':'reviews_v0_47/integration_main_proof_rigidity.json','sha256':sha(ROOT/'reviews_v0_47/integration_main_proof_rigidity.json'),'passed_check_count':audit['passed_check_count']},
 'independent_semantic_scope_review':{'file':str(semantic_path.relative_to(ROOT)),'sha256':sha(semantic_path),'result':'PASS'},
 'selected_graph_sha256':sha(ROOT/'dependency_audit_v0_47/obligation_map.json'),
 'selected_route_statistics':stats,'closed_selected_whole_leaves':sorted(cfg['closed_selected_leaves']),
 'source_files_new_increment_verified_against_pin':stats['new_source_files_checked'],
 'unique_source_ranges_new_increment_verified':stats['new_unique_source_ranges_checked'],
 'source_snapshot_manifest_sha256':sha(ROOT/'source_snapshot_v0_47/manifest.json'),
 'tex_validation':tex,'lean_build':False,'kernel_replay':False,'pdf_generated':False,
 'limitations':[
   'This is a partial human reconstruction, not a completed proof of RH or Dirichlet GRH.',
   'The source formal proof is accepted as correct; no formal correctness audit or Lean replay was performed.',
   'The mathematical claim graph records the human reconstruction; it is not a mechanically extracted Lean transitive dependency graph.',
   'Draft TeX compilation checks syntax and references; it is not PDF rendering or visual layout certification.',
   'Claim inventory is not a completion percentage; all new statements retain their exact foundational, conditional or eventual scope.',
   'The new full selected closures are exactly those in the configuration. Whole global quantitative, common geometry and arithmetic-family, arbitrary-chain and other recorded input producers remain open; completed conditional constructors do not assert their inputs.'
 ]}
write(ROOT/'validation_v0_47.json',result)
print(json.dumps({k:result[k] for k in ['result','baseline_claims_preserved','new_claims','cumulative_claims','baseline_manifest_artifacts_preserved','selected_route_statistics']},indent=2))
