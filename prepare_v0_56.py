#!/usr/bin/env python3
"""Freeze the authoritative v0.55 roots before the next continuation."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / 'RH_reconstruction_v0_55.zip'
EXPECTED = 'bb3f23c782e0383e5380f75bf15106c1b5da35d661cdfb7a0cd247efb20e0863'
OLD = ROOT / 'history/version_0_55'
FILES = [
    'README.md', 'RH_GRH_parallel_execution_plan_v0_55.txt',
    'RH_GRH_reconstruction_roadmap_v0_55.txt', 'SHA256SUMS',
    'component_filename_map.json', 'continuation_checkpoint.json',
    'next_source_targets.json', 'provenance.json', 'provenance.txt',
    'source_index.json', 'tex_validation.json',
]

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

assert digest(ARCHIVE) == EXPECTED
OLD.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(ARCHIVE) as archive:
    for name in FILES:
        data = archive.read(name)
        target = OLD / name
        if target.exists():
            assert target.read_bytes() == data, ('frozen predecessor differs', name)
        else:
            target.write_bytes(data)
record = {
    'version': '0.55', 'archive': ARCHIVE.name, 'sha256': EXPECTED,
    'bytes': ARCHIVE.stat().st_size, 'baseline_claims': 3538,
    'source_commit': '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4',
    'frozen_root_files': FILES,
}
(OLD / 'baseline_record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
