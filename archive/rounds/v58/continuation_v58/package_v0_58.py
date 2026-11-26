#!/usr/bin/env python3
"""Package the preserved proof state, full original source and portable handoff."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=ROOT.parent
def read(path):return json.loads(path.read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4194304),b''):h.update(block)
    return h.hexdigest()

audit=read(HERE/'review/handoff_audit.json')
assert audit['status']=='PASS' and not audit['errors']
for path,digest in audit['input_bindings'].items():
    assert sha(ROOT/path)==digest,('Audited input changed',path)
checkpoint=read(ROOT/'CURRENT_CHECKPOINT_v0_58.json')
assert checkpoint['mathematical_state']['new_claims_in_this_package']==0
assert checkpoint['mathematical_state']['cumulative_claims']==3746
assert checkpoint['mathematical_state']['whole_open_obligations']==24
snapshot=read(HERE/'reconstruction_bundle.json')
source=read(HERE/'source/source_bundle.json')
for folder,record,key in [(HERE,snapshot,'archive'),(HERE,snapshot,'inventory'),
                          (HERE/'source',source,'archive'),(HERE/'source',source,'tree_manifest'),
                          (HERE/'source',source,'raw_commit')]:
    value=record[key];p=folder/value['file']
    assert p.stat().st_size==value['bytes'] and sha(p)==value['sha256']
names={record['path'] for record in checkpoint['direct_reading_files']}
names.update(['CURRENT_CHECKPOINT_v0_58.json','RH_START_HERE_v0_58.txt','RH_NEW_CHAT_PROMPT_v0_58.txt'])
for path in HERE.rglob('*'):
    if not path.is_file() or '__pycache__' in path.parts:continue
    if path.suffix in {'.tmp','.partial'}:continue
    names.add(path.relative_to(ROOT).as_posix())
names.discard('SHA256SUMS_v0_58')
files=[ROOT/name for name in sorted(names)]
manifest=ROOT/'SHA256SUMS_v0_58'
manifest.write_text(''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
files.append(manifest)
archive_path=OUT/'RH_reconstruction_v0_58.zip'
print(json.dumps({'phase':'packaging','outer_members':len(files),
                  'preserved_reconstruction_members':snapshot['member_count'],
                  'preserved_source_files':source['tracked_files']}),flush=True)
with zipfile.ZipFile(archive_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as archive:
    for path in sorted(files):
        name=path.relative_to(ROOT).as_posix()
        if path.suffix=='.xz':method=zipfile.ZIP_STORED
        else:method=zipfile.ZIP_DEFLATED
        archive.write(path,name,compress_type=method,compresslevel=9)
assert archive_path.stat().st_size<=536870912,'Complete package exceeds the observed upload limit'
print(json.dumps({'phase':'checking','archive_bytes':archive_path.stat().st_size}),flush=True)
with zipfile.ZipFile(archive_path) as archive:
    assert len(archive.namelist())==len(files) and set(archive.namelist())=={p.relative_to(ROOT).as_posix() for p in files}
    assert archive.testzip() is None
    for path in files:
        info=archive.getinfo(path.relative_to(ROOT).as_posix())
        assert info.file_size==path.stat().st_size
for name in ['RH_START_HERE_v0_58.txt','RH_NEW_CHAT_PROMPT_v0_58.txt']:
    shutil.copy2(ROOT/name,OUT/name)
record={'package_version':'0.58','mathematical_edition':'0.57','new_mathematical_claims':0,
 'archive':archive_path.name,'archive_sha256':sha(archive_path),'archive_bytes':archive_path.stat().st_size,
 'outer_archive_members':len(files),'manifest':'SHA256SUMS_v0_58','crc_check':'PASS',
 'primary_baseline':checkpoint['primary_baseline'],
 'preserved_reconstruction_members':snapshot['member_count'],
 'original_source_files':source['tracked_files'],'original_source_commit':source['source_commit'],
 'original_source_tree':source['source_tree'],
 'offline_reconstruction_restore':'PASS','offline_source_restore':'PASS',
 'handoff_audit_sha256':sha(HERE/'review/handoff_audit.json'),
 'compression':'The full unchanged reconstruction and original source are in XZ-compressed tar snapshots. Use the included Python restore helpers. Latest mathematical reading files are also directly available in the outer ZIP.',
 'direct_handoff_files':[{'file':name,'sha256':sha(OUT/name),'bytes':(OUT/name).stat().st_size}
                        for name in ['RH_START_HERE_v0_58.txt','RH_NEW_CHAT_PROMPT_v0_58.txt']]}
(OUT/'RH_reconstruction_v0_58_delivery.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
