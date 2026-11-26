#!/usr/bin/env python3
"""Package the fully reviewed cumulative checkpoint and direct reading files."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())

v=read(ROOT/'validation_v0_50.json')
assert v['result']=='PASS'
for item in v['tex_validation']['documents']:
    assert item['tex_sha256']==sha(ROOT/item['tex_filename'])
assert v['selected_graph_sha256']==sha(ROOT/'dependency_audit_v0_50/obligation_map.json')
review=v['independent_integration_and_scope_audit']
assert review['status']=='PASS' and review['sha256']==sha(ROOT/review['file'])
audit=read(ROOT/review['file'])
for name,h in audit['input_bindings'].items():
    assert sha(ROOT/name)==h,('independently audited file changed',name)
cfg=read(ROOT/'increment_v0_50.json')
baseline={s.split('  ',1)[1] for s in (ROOT/'history/version_0_49/SHA256SUMS').read_text().splitlines() if s.strip()}
def include(p):
    rel=p.relative_to(ROOT)
    if rel.as_posix() in baseline:return True
    if rel.parts[0]=='build' or rel.parts[0].startswith('build_v0_'):return False
    if '__pycache__' in rel.parts:return False
    if rel.parts[0] in cfg['components'] and len(rel.parts)>1 and rel.parts[1] in {'build','validation'}:return False
    return p!=ROOT/'SHA256SUMS'
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and include(p))
assert all((ROOT/p).is_file() for p in baseline)
(ROOT/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
files.append(ROOT/'SHA256SUMS')
dest=OUT/'RH_reconstruction_v0_50.zip'
print(json.dumps({'phase':'packaging','archive':dest.name,'members':len(files)}),flush=True)
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
    for p in sorted(files):archive.write(p,p.relative_to(ROOT).as_posix())
print(json.dumps({'phase':'checking_archive','bytes':dest.stat().st_size}),flush=True)
with zipfile.ZipFile(dest) as archive:
    assert len(archive.namelist())==len(files)
    assert set(archive.namelist())=={p.relative_to(ROOT).as_posix() for p in files}
    assert archive.testzip() is None,'ZIP CRC failure'
names=['RH_new_proofs_v0_50.tex','RH_readable_reconstruction_v0_50.tex',
 'RH_reconstruction_progress_v0_50.txt','RH_GRH_reconstruction_roadmap_v0_50.txt',
 'RH_GRH_parallel_execution_plan_v0_50.txt','RH_dependency_audit_v0_50.txt']
for name in names:shutil.copy2(ROOT/name,OUT/name)
result={'artifact_version':'0.50','archive':dest.name,'archive_sha256':sha(dest),
 'archive_bytes':dest.stat().st_size,'archive_members':len(files),'crc_check':'PASS',
 'manifest':'SHA256SUMS','manifest_entries':len(files)-1,
 'reading_files':[{'file':n,'sha256':sha(OUT/n),'bytes':(OUT/n).stat().st_size} for n in names]}
(OUT/'RH_reconstruction_v0_50_delivery.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
