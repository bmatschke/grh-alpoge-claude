#!/usr/bin/env python3
"""Make the validated continuation snapshot and the two direct reading files."""
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

v=json.loads((ROOT/'validation_v0_32.json').read_text())
assert v['result']=='PASS'
assert v['tex_validation']['tex_sha256']==sha(ROOT/'RH_readable_reconstruction_v0_32.tex')
assert v['selected_graph_sha256']==sha(ROOT/'dependency_audit_v0_32/obligation_map.json')
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).parts[0]!='build' and p!=ROOT/'SHA256SUMS')
(ROOT/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
files.append(ROOT/'SHA256SUMS')
dest=OUT/'RH_reconstruction_v0_32.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
    for p in sorted(files):archive.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(dest) as archive:
    assert set(archive.namelist())=={p.relative_to(ROOT).as_posix() for p in files}
    bad=archive.testzip()
    assert bad is None,('ZIP CRC failure',bad)
for name in ['RH_readable_reconstruction_v0_32.tex','RH_dependency_audit_v0_32.txt']:
    if (OUT/name).resolve()!=(ROOT/name).resolve():shutil.copy2(ROOT/name,OUT/name)
result=dict(artifact_version='0.32',archive=dest.name,archive_sha256=sha(dest),
    archive_bytes=dest.stat().st_size,archive_members=len(files),crc_check='PASS',
    reading_files=[dict(file=name,sha256=sha(OUT/name),bytes=(OUT/name).stat().st_size)
      for name in ['RH_readable_reconstruction_v0_32.tex','RH_dependency_audit_v0_32.txt']])
(OUT/'RH_reconstruction_v0_32_delivery.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
