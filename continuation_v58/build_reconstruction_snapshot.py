#!/usr/bin/env python3
"""Preserve every delivered v0.57 member in a solid-compressed snapshot."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import zipfile

HERE=Path(__file__).resolve().parent
BASELINE_SHA='b326cc620d0064eda3126cce27f3dafd31e83d8516741aaf2ffcac450788bd33'

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4194304),b''):h.update(block)
    return h.hexdigest()

def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

class HashedReader:
    def __init__(self,source):self.source=source;self.hash=hashlib.sha256();self.count=0
    def read(self,n=-1):
        data=self.source.read(n);self.hash.update(data);self.count+=len(data);return data

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline',type=Path,default=HERE.parent.parent/'RH_reconstruction_v0_57.zip')
    args=ap.parse_args()
    assert sha(args.baseline)==BASELINE_SHA,'The baseline is not the delivered v0.57 archive'
    with zipfile.ZipFile(args.baseline) as old:
        infos=old.infolist(); names=[i.filename for i in infos]
        assert len(infos)==9551 and len(set(names))==len(names)
        original_manifest=old.read('SHA256SUMS')
        expected=dict((name,h) for h,name in (line.split('  ',1) for line in original_manifest.decode().splitlines() if line))
        expected['SHA256SUMS']=hashlib.sha256(original_manifest).hexdigest()
        assert set(expected)==set(names)
        records=[]
        for i in infos:
            parts=i.filename.split('/')
            assert all(p not in ('','.','..') for p in parts) and '\\' not in i.filename
            assert not i.is_dir() and not i.flag_bits&1
            records.append({'path':i.filename,'bytes':i.file_size,'sha256':expected[i.filename],
                            'mode':(i.external_attr>>16)&0o777 or 0o644})
        inventory={'schema':'rh-preserved-reconstruction-members/1','baseline_version':'0.57',
          'baseline_archive_sha256':BASELINE_SHA,'members':sorted(records,key=lambda r:r['path']),
          'member_count':len(records),'uncompressed_bytes':sum(r['bytes'] for r in records)}
        inv_path=HERE/'reconstruction_inventory.json';dump(inv_path,inventory)
        byname={r['path']:r for r in records}
        def order(i):
            canonical=re.sub(r'v0_\d+','v0_VERSION',Path(i.filename).name)
            return canonical,i.file_size,i.filename
        target=HERE/'reconstruction_snapshot.tar.xz'
        print(json.dumps({'phase':'building_preserved_snapshot','members':len(infos),
                          'uncompressed_bytes':inventory['uncompressed_bytes']}),flush=True)
        with target.open('wb') as output:
            proc=subprocess.Popen(['xz','-T1','-3','--lzma2=dict=64MiB','--check=sha256','-c'],
                                  stdin=subprocess.PIPE,stdout=output,stderr=subprocess.PIPE)
            try:
                with tarfile.open(fileobj=proc.stdin,mode='w|',format=tarfile.PAX_FORMAT) as tar:
                    for number,i in enumerate(sorted(infos,key=order),1):
                        r=byname[i.filename]
                        info=tarfile.TarInfo(i.filename);info.size=i.file_size;info.mode=r['mode']
                        info.mtime=0;info.uid=info.gid=0;info.uname=info.gname=''
                        with old.open(i) as source:
                            reader=HashedReader(source);tar.addfile(info,reader)
                            assert reader.count==r['bytes'] and reader.hash.hexdigest()==r['sha256'],i.filename
                        if number%2500==0:print(json.dumps({'preserved_members':number}),flush=True)
                proc.stdin.close()
                errors=proc.stderr.read();code=proc.wait()
                assert code==0,errors.decode(errors='replace')
            except BaseException:
                proc.kill();proc.wait();raise
        metadata={'schema':'rh-preserved-reconstruction-bundle/1','package_version':'0.58',
          'mathematical_version':'0.57','baseline_archive_sha256':BASELINE_SHA,
          'archive':{'file':target.name,'sha256':sha(target),'bytes':target.stat().st_size},
          'inventory':{'file':inv_path.name,'sha256':sha(inv_path),'bytes':inv_path.stat().st_size},
          'member_count':len(records),'uncompressed_bytes':inventory['uncompressed_bytes'],
          'new_mathematical_claims':0,'cumulative_claims':3746,'whole_open_obligations':24,
          'scope':'Every delivered v0.57 archive member, at its original path and exact bytes.'}
        dump(HERE/'reconstruction_bundle.json',metadata)
        print(json.dumps(metadata,indent=2),flush=True)

if __name__=='__main__':main()
