#!/usr/bin/env python3
"""Refresh only the PGR artifact inventory; proof/review content is untouched."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
items=[]
for path in sorted(HERE.rglob('*')):
    if not path.is_file() or path.name=='hashes.json' or '__pycache__' in path.parts:
        continue
    data=path.read_bytes()
    items.append({'file':str(path.relative_to(HERE.parent)),
        'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
record={'schema':'rh-component-artifact-hashes/1','artifact_version':'0.57',
    'component':HERE.name,
    'proof_file_sha256':hashlib.sha256((HERE/'main.tex').read_bytes()).hexdigest(),
    'files':items,'file_count':len(items),
    'excludes':['hashes.json itself','Python bytecode caches'],
    'no_proof_or_review_mutation':True}
(HERE/'hashes.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'component':HERE.name,'file_count':len(items),
    'main_sha256':record['proof_file_sha256']},indent=2))
