#!/usr/bin/env python3
"""Validate continuity and package v0.19 TeX and its complete source ledger."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_18'
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
OUT=args.output_dir.resolve()
OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

prior=read(OLD/'provenance.json')
current=read(ROOT/'provenance.json')
checkpoint=read(ROOT/'continuation_checkpoint.json')
targets=read(ROOT/'next_source_targets.json')
texcheck=read(ROOT/'tex_validation.json')
assert checkpoint['artifact_version']==current['artifact_version']=='0.19'
assert len(prior['claims'])==820
assert current['validation']['claim_count']==len(current['claims'])
assert current['validation']['source_link_count']==sum(len(c['sources'])for c in current['claims'])
assert current['validation']['source_file_count']==len(current['source_files'])
claims={c['id']:c for c in current['claims']}
for c in prior['claims']:
    assert all(claims[c['id']][k]==v for k,v in c.items()),c['id']
files={f['path']:f for f in current['source_files']}
for f in prior['source_files']:assert files[f['path']]==f,f['path']
graph=current['mathematical_dependency_graph']
for c,deps in prior['mathematical_dependency_graph'].items():assert graph[c]==deps,c
positions={c:i for i,c in enumerate(current['dependency_topological_order'])}
assert set(positions)==set(graph)==set(claims)
for c,deps in graph.items():assert all(positions[d]<positions[c]for d in deps),c
for k,v in prior.items():
    if k.startswith('version_')and'conclusion'in k:assert current[k]==v,k
assert targets['global_branches_unchanged']==read(OLD/'next_source_targets.json')['global_branches_unchanged']
assert targets['target_count']==len(targets['targets'])
assert not (ROOT/'RH_readable_reconstruction_v0_19.pdf').exists()
assert not (ROOT/'visual_qa.json').exists()
assert texcheck['pdf_generated'] is False
tex=ROOT/'RH_readable_reconstruction_v0_19.tex'
assert texcheck['tex_sha256']==sha(tex)
assert checkpoint['validation']['tex']==texcheck

archived_roots={p.name for p in OLD.iterdir()if p.is_file()}
assert len(archived_roots)==20
old_checked=0
for line in (OLD/'SHA256SUMS').read_text().splitlines():
    expected,relative=line.split('  ',1)
    p=OLD/relative if relative in archived_roots else ROOT/relative
    assert p.is_file()and sha(p)==expected,relative
    old_checked+=1
assert old_checked==862
for name in ['source_verification.txt','continuity_audit.txt','final_scope_review.txt']:
    assert (ROOT/'reviews_v0_19'/name).is_file(),name
for path,expected in checkpoint['validation']['mathematical_reviews'].items():
    assert sha(ROOT/path)==expected,path
source_paths=set(files)|{t['path']for t in targets['targets']}

report={
    'version':'0.19','result':'passed','source_commit':current['commit'],
    'main_tex_sha256':sha(tex),'pdf_generated':False,'pdf_visual_review_performed':False,
    'claims':len(claims),'new_claims':len(claims)-len(prior['claims']),
    'claim_source_ranges':sum(len(c['sources'])for c in current['claims']),
    'indexed_source_files':len(files),'files_including_next_targets':len(source_paths),
    'next_target_ranges':len(targets['targets']),
    'previous_manifest_entries_checked':old_checked,
    'previous_total_files_preserved':old_checked+1,'previous_root_files_archived':20,
    'all_old_claim_fields_source_arrays_file_records_and_dependency_lists_preserved':True,
    'dependency_graph_acyclic':True,'human_graph_is_not_lean_transitive_audit':True,
    'old_edges':sum(map(len,prior['mathematical_dependency_graph'].values())),
    'new_edges':sum(map(len,graph.values()))-sum(map(len,prior['mathematical_dependency_graph'].values())),
    'no_lean_build_or_kernel_replay':True,
    'records':{name:sha(ROOT/'reviews_v0_19'/name)for name in ['source_verification.txt','continuity_audit.txt','final_scope_review.txt']},
    'archive_policy':'Include every regular file below this root except transient build directories, Python caches and the checksum manifest when generating that manifest. Include the manifest in the ZIP. Verify archive CRCs, entry set and every archived hash.',
}
write(ROOT/'reviews_v0_19/package_validation.json',report)
def eligible(p):
    rel=p.relative_to(ROOT)
    return p.is_file()and'build'not in rel.parts and'__pycache__'not in rel.parts and p.suffix!='.pyc'
paths=sorted(p for p in ROOT.rglob('*')if eligible(p)and p!=ROOT/'SHA256SUMS')
manifest={str(p.relative_to(ROOT)):sha(p)for p in paths}
(ROOT/'SHA256SUMS').write_text(''.join(f'{value}  {name}\n'for name,value in manifest.items()))
archive=OUT/'RH_reconstruction_v0_19.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8)as z:
    for p in paths+[ROOT/'SHA256SUMS']:z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive)as z:
    assert z.testzip()is None
    assert set(z.namelist())==set(manifest)|{'SHA256SUMS'}
    assert z.read('SHA256SUMS')==(ROOT/'SHA256SUMS').read_bytes()
    for name,expected in manifest.items():assert digest(z.read(name))==expected,name
tex_copy=OUT/tex.name
shutil.copy2(tex,tex_copy)
assert sha(tex_copy)==sha(tex)
print(json.dumps({'archive':str(archive),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
    'files_in_archive':len(manifest)+1,'tex':str(tex_copy),'tex_sha256':sha(tex_copy),
    'claims':len(claims),'new_claims':len(claims)-len(prior['claims']),'pdf_generated':False},indent=2))
