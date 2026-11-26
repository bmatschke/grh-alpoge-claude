#!/usr/bin/env python3
"""Package the exact checked v0.27 artifact and verify all archive bytes."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile

ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
ledger=read(ROOT/'provenance.json');cp=read(ROOT/'continuation_checkpoint.json');audit=read(ROOT/'reviews_v0_27/source_verification_v0_27_audit.json');texcheck=read(ROOT/'tex_validation.json')
assert ledger['artifact_version']==cp['artifact_version']=='0.27'
assert audit['result']=='PASS'
for name,expected in audit['input_sha256'].items():assert sha(ROOT/name)==expected,name
tex=ROOT/'RH_readable_reconstruction_v0_27.tex'
assert sha(tex)==texcheck['tex_sha256'] and cp['validation']['tex']==texcheck
assert not texcheck['pdf_generated'] and not texcheck['undefined_references_or_citations']
assert not (ROOT/'RH_readable_reconstruction_v0_27.pdf').exists()
for path,expected in cp['validation']['mathematical_reviews'].items():assert sha(ROOT/path)==expected,path
for name in ['source_verification.txt','continuity_audit.txt','final_scope_review.txt']:
 assert (ROOT/'reviews_v0_27'/name).is_file(),name
report={'version':'0.27','result':'PASS','main_tex_sha256':sha(tex),'claims':len(ledger['claims']),'new_claims':ledger['validation']['new_claims'],'claim_source_ranges':ledger['validation']['source_link_count'],'indexed_source_files':len(ledger['source_files']),'active_target_ranges':audit['active_target_ranges'],'all_previous_files_preserved':audit['previous_total_files_preserved'],'all_original_claim_fields_and_edges_preserved':True,'all_new_endpoints_independently_reviewed':True,'no_lean_build_or_kernel_replay':True,'pdf_generated':False,'pdf_visual_review_performed':False,'audit_scope':'Finite semantic sufficient-obligation map; not exhaustive Lean dependency extraction','manifest_policy':'All regular files except build directories, Python caches and the manifest itself when computing checksums; the manifest is included in the ZIP.'}
write(ROOT/'reviews_v0_27/package_validation.json',report)
def eligible(p):
 rel=p.relative_to(ROOT)
 return p.is_file() and 'build' not in rel.parts and '__pycache__' not in rel.parts and p.suffix!='.pyc'
paths=sorted(p for p in ROOT.rglob('*') if eligible(p) and p!=ROOT/'SHA256SUMS')
manifest={str(p.relative_to(ROOT)):sha(p) for p in paths}
(ROOT/'SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in manifest.items()))
archive=OUT/'RH_reconstruction_v0_27.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in paths+[ROOT/'SHA256SUMS']:z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(manifest)|{'SHA256SUMS'}
 assert z.read('SHA256SUMS')==(ROOT/'SHA256SUMS').read_bytes()
 for name,expected in manifest.items():assert digest(z.read(name))==expected,name
deliverables=[archive]
for name in [tex.name,'RH_dependency_audit_v0_27.txt']:
 dest=OUT/name;shutil.copy2(ROOT/name,dest);assert sha(dest)==sha(ROOT/name);deliverables.append(dest)
print(json.dumps({'archive_entries':len(manifest)+1,'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in deliverables],'pdf_generated':False},indent=2))
