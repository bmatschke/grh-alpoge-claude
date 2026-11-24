#!/usr/bin/env python3
"""Validate and package the v0.13 continuation, excluding transient builds."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_12'
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
OUT = args.output_dir.resolve()
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'pdf').mkdir(exist_ok=True)

def read(path):
    return json.loads(path.read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def sha(path):
    return digest(path.read_bytes())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

prior = read(OLD / 'provenance.json')
current = read(ROOT / 'provenance.json')
checkpoint = read(ROOT / 'continuation_checkpoint.json')
targets = read(ROOT / 'next_source_targets.json')
visual = read(ROOT / 'visual_qa.json')
pdf = ROOT / 'RH_readable_reconstruction_v0_13.pdf'
assert sha(pdf) == visual['pdf_sha256']
assert checkpoint['artifact_version'] == current['artifact_version'] == '0.13'
assert checkpoint['validation']['pdf'] == visual
assert len(prior['claims']) == 438 and len(current['claims']) == 465
assert sum(len(c['sources']) for c in current['claims']) == 7593
current_claims = {c['id']: c for c in current['claims']}
for claim in prior['claims']:
    now = current_claims[claim['id']]
    assert all(now[k] == value for k, value in claim.items()), claim['id']
prior_files = {f['path']: f for f in prior['source_files']}
current_files = {f['path']: f for f in current['source_files']}
assert len(prior_files) == 1032 and len(current_files) == 1098
for path, record in prior_files.items():
    assert current_files[path] == record, path
graph = current['mathematical_dependency_graph']
for claim, edges in prior['mathematical_dependency_graph'].items():
    assert graph[claim] == edges, claim
positions = {claim: index for index, claim in enumerate(current['dependency_topological_order'])}
assert set(positions) == set(graph) == set(current_claims)
for claim, dependencies in graph.items():
    assert all(positions[d] < positions[claim] for d in dependencies), claim
assert targets['target_count'] == len(targets['targets']) == 30
all_source_paths = set(current_files) | {t['path'] for t in targets['targets']}
assert len(all_source_paths) == 1109

# The old checksum manifest excludes itself. All twelve overwritten root
# records, including that manifest, also have a separately audited archive.
archived_roots = {p.name for p in OLD.iterdir() if p.is_file()}
assert len(archived_roots) == 12
old_checked = 0
for line in (OLD / 'SHA256SUMS').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    path = OLD / relative if relative in archived_roots else ROOT / relative
    assert path.is_file() and sha(path) == expected, relative
    old_checked += 1
assert old_checked == 424
for report in ['continuity_audit.txt', 'final_scope_review.txt', 'source_verification.txt']:
    assert (ROOT / 'reviews_v0_13' / report).is_file(), report
for review in visual['reviews']:
    path = ROOT / review['record']
    assert sha(path) == review['record_sha256'], path
for key in ['version_0_10_local_conclusions', 'version_0_11_local_conclusions', 'version_0_12_local_conclusions']:
    assert current[key] == prior[key]

validation = {
    'version': '0.13',
    'result': 'passed',
    'source_commit': current['commit'],
    'main_pdf_sha256': sha(pdf),
    'main_pdf_pages': visual['page_count'],
    'claims': len(current_claims),
    'new_claims': len(current_claims) - len(prior['claims']),
    'claim_source_ranges': 7593,
    'indexed_source_files': len(current_files),
    'files_including_next_targets': len(all_source_paths),
    'next_target_ranges': len(targets['targets']),
    'previous_manifest_entries_checked': old_checked,
    'previous_total_files_preserved': 425,
    'previous_root_files_archived': 12,
    'all_old_claim_fields_source_arrays_file_records_and_dependency_lists_preserved': True,
    'dependency_graph_acyclic': True,
    'old_edges': sum(map(len, prior['mathematical_dependency_graph'].values())),
    'new_edges': sum(map(len, graph.values())) - sum(map(len, prior['mathematical_dependency_graph'].values())),
    'no_lean_build_or_kernel_replay': True,
    'records': {
        name: sha(ROOT / 'reviews_v0_13' / name)
        for name in ['continuity_audit.txt', 'final_scope_review.txt', 'source_verification.txt']
    },
    'archive_policy': 'Package every regular file below this root except transient build directories, Python cache files and SHA256SUMS itself when generating that manifest. Include SHA256SUMS in the ZIP. Verify every archived entry against the manifest after writing.',
}
write(ROOT / 'reviews_v0_13/package_validation.json', validation)

def eligible(path):
    relative = path.relative_to(ROOT)
    return (path.is_file() and 'build' not in relative.parts
            and '__pycache__' not in relative.parts and path.suffix != '.pyc')

paths = sorted(p for p in ROOT.rglob('*') if eligible(p) and p != ROOT / 'SHA256SUMS')
manifest = {str(p.relative_to(ROOT)): sha(p) for p in paths}
(ROOT / 'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name, value in manifest.items()))
archive = OUT / 'RH_reconstruction_v0_13.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
    for path in paths + [ROOT / 'SHA256SUMS']:
        z.write(path, str(path.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(manifest) | {'SHA256SUMS'}
    assert z.read('SHA256SUMS') == (ROOT / 'SHA256SUMS').read_bytes()
    for name, expected in manifest.items():
        assert digest(z.read(name)) == expected, name
pdf_copy = OUT / 'pdf' / pdf.name
shutil.copy2(pdf, pdf_copy)
assert sha(pdf_copy) == sha(pdf)
print(json.dumps({
    'result': 'passed',
    'archive_files': len(manifest) + 1,
    'checksummed_files': len(manifest),
    'pdf': str(pdf_copy),
    'pdf_sha256': sha(pdf_copy),
    'pdf_bytes': pdf_copy.stat().st_size,
    'zip': str(archive),
    'zip_sha256': sha(archive),
    'zip_bytes': archive.stat().st_size,
}, indent=2))
