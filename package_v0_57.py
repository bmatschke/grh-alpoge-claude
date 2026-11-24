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

v=read(ROOT/'validation_v0_57.json')
assert v['result']=='PASS'
for item in v['tex_validation']['documents']:
    assert item['tex_sha256']==sha(ROOT/item['tex_filename'])
assert v['selected_graph_sha256']==sha(ROOT/'dependency_audit_v0_57/obligation_map.json')
review=v['independent_integration_and_scope_audit']
assert review['status']=='PASS' and review['sha256']==sha(ROOT/review['file'])
audit=read(ROOT/review['file'])
for name,h in audit['input_bindings'].items():
    assert sha(ROOT/name)==h,('independently audited file changed',name)
cfg=read(ROOT/'increment_v0_57.json')
baseline={s.split('  ',1)[1] for s in (ROOT/'history/version_0_56/SHA256SUMS').read_text().splitlines() if s.strip()}
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
dest=OUT/'RH_reconstruction_v0_57.zip'
lzma_members={
    'provenance.json',
    'history/version_0_56/provenance.json',
    'history/version_0_55/provenance.json',
    'history/version_0_54/provenance.json',
}
assert lzma_members <= {p.relative_to(ROOT).as_posix() for p in files}
print(json.dumps({'phase':'packaging','archive':dest.name,'members':len(files)}),flush=True)
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as archive:
    for p in sorted(files):
        name=p.relative_to(ROOT).as_posix()
        method=zipfile.ZIP_LZMA if name in lzma_members else zipfile.ZIP_DEFLATED
        archive.write(p,name,compress_type=method,compresslevel=9)
assert dest.stat().st_size <= 536870912,'Archive exceeds the observed upload size limit'
print(json.dumps({'phase':'checking_archive','bytes':dest.stat().st_size}),flush=True)
with zipfile.ZipFile(dest) as archive:
    assert len(archive.namelist())==len(files)
    assert set(archive.namelist())=={p.relative_to(ROOT).as_posix() for p in files}
    assert archive.testzip() is None,'ZIP CRC failure'
    for name in lzma_members:
        assert archive.getinfo(name).compress_type==zipfile.ZIP_LZMA
        assert hashlib.sha256(archive.read(name)).hexdigest()==sha(ROOT/name),('Recompressed ledger bytes changed',name)
names=['RH_new_proofs_v0_57.tex','RH_readable_reconstruction_v0_57.tex',
 'RH_reconstruction_progress_v0_57.txt','RH_GRH_reconstruction_roadmap_v0_57.txt',
 'RH_GRH_parallel_execution_plan_v0_57.txt','RH_dependency_audit_v0_57.txt']
for name in names:shutil.copy2(ROOT/name,OUT/name)
result={'artifact_version':'0.57','archive':dest.name,'archive_sha256':sha(dest),
 'archive_bytes':dest.stat().st_size,'archive_members':len(files),'crc_check':'PASS',
 'compression':{'default':'DEFLATE','large_ledger_method':'LZMA',
                'lzma_members':sorted(lzma_members),'upload_size_limit_bytes':536870912},
 'manifest':'SHA256SUMS','manifest_entries':len(files)-1,
 'reading_files':[{'file':n,'sha256':sha(OUT/n),'bytes':(OUT/n).stat().st_size} for n in names]}
(OUT/'RH_reconstruction_v0_57_delivery.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
