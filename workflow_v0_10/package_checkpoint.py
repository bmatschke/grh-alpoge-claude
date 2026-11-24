#!/usr/bin/env python3
"""Package the final visually reviewed v0.10 note and cumulative proof record.

Do not run until root has written and confirmed v0_10/visual_qa.json.
The merged ledger must already exist in output/RH_reconstruction_v0_10.
This script never edits the source checkout, old package, main TeX/PDF,
component originals, or merged ledgers. It validates and copies them.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unicodedata
import zipfile

import fitz

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "output/RH_reconstruction_v0_10"
OLD = BASE / "output/RH_reconstruction_v0_9"
REPO = BASE / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENTS = {
    "RU": ("rank_upper", "main.tex", [f"RU{i}" for i in range(1, 12)]),
    "RD": ("rank_lower", "main.tex", [f"RD{i}" for i in range(1, 16)]),
    "HM": ("harmonic_model", "main.tex", [f"HM{i}" for i in range(1, 13)]),
    "NP": ("numerical_parameters", "main.tex", [f"NP{i}" for i in range(1, 10)]),
    "TC": ("type_one_closure", "main.tex", [f"TC{i}" for i in range(1, 7)]),
}
UPDATED_PRIOR_IDS = {"JR10", "TI7", "TI8", "TI9", "SW8", "SW9", "SW11", "SW12", "RL11"}
EXPECTED_COUNTS = {
    "old_claims": 315, "claims": 368, "new_claims": 53,
    "old_source_files": 764, "source_files": 890,
    "old_source_links": 4579, "source_links": 5817,
}

MERGED_NAMES = ("provenance.json", "provenance.txt", "source_index.json")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def heading_key(value):
    """Ignore punctuation, whitespace, ligatures and PDF line hyphenation."""
    value = unicodedata.normalize("NFKC", value).casefold()
    return "".join(c for c in value if c.isalnum())


def range_records(value):
    """Find source-range records in the separately supplied next-target file."""
    if isinstance(value, dict):
        required = {"path", "sha256", "line_start", "line_end", "range_sha256"}
        if required.issubset(value):
            yield value
        else:
            for child in value.values():
                yield from range_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from range_records(child)


def verify_sources(ledger, target_records):
    """Recheck exact bytes against both recorded hashes and pinned Git blobs."""
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
    ).strip()
    require(head == PIN, "The source checkout no longer has the pinned HEAD.")
    records = {record["path"]: record for record in ledger["source_files"]}
    require(len(records) == len(ledger["source_files"]),
            "Duplicate primary source paths in the merged ledger.")
    expected_hashes = {path: record["sha256"] for path, record in records.items()}
    for record in target_records:
        old_hash = expected_hashes.setdefault(record["path"], record["sha256"])
        require(old_hash == record["sha256"],
                f"Conflicting next-target hash: {record['path']}")

    # A Git object hash includes its 'blob <length>\\0' header. This checks the
    # actual file bytes against the pinned tree without hundreds of git calls.
    object_format = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "--show-object-format"], text=True
    ).strip()
    require(object_format in {"sha1", "sha256"}, "Unknown Git object format.")
    listing = subprocess.check_output(
        ["git", "-C", str(REPO), "ls-tree", "-rz", "--full-tree", PIN, "--",
         *sorted(expected_hashes)]
    )
    pinned_objects = {}
    for item in listing.split(b"\0"):
        if not item:
            continue
        metadata, encoded_path = item.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        require(kind == "blob", "A cited source path is not a pinned blob.")
        pinned_objects[encoded_path.decode("utf-8")] = object_id
    require(set(pinned_objects) == set(expected_hashes),
            "The pinned tree does not contain every cited/target source file.")

    raw_files, lines = {}, {}
    for path, expected in expected_hashes.items():
        raw = (REPO / path).read_bytes()
        require(sha(raw) == expected, f"Source-file hash mismatch: {path}")
        object_bytes = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        require(hashlib.new(object_format, object_bytes).hexdigest() == pinned_objects[path],
                f"Source bytes differ from the pinned Git blob: {path}")
        raw_files[path] = raw
        lines[path] = raw.splitlines(keepends=True)

    def check_range(record, label):
        path = record["path"]
        require(path in raw_files, f"Unindexed source in {label}: {path}")
        require(sha(raw_files[path]) == record["sha256"],
                f"Record/source-file hash mismatch: {label} {path}")
        first, last = record["line_start"], record["line_end"]
        require(1 <= first <= last <= len(lines[path]),
                f"Invalid inclusive range: {label} {path}:{first}-{last}")
        excerpt = b"".join(lines[path][first - 1:last])
        require(sha(excerpt) == record["range_sha256"],
                f"Source-range hash mismatch: {label} {path}:{first}-{last}")

    count = 0
    for claim in ledger["claims"]:
        for record in claim["sources"]:
            check_range(record, claim["id"])
            count += 1
    for i, record in enumerate(target_records, 1):
        check_range(record, f"next target {i}")
    return count, len(expected_hashes)


def reviewed_pages(qa, pages):
    """Check explicit review coverage as well as the all-pages certification."""
    covered = set(qa.get("reviewed_pages", []))
    for review in qa.get("reviews", []):
        covered.update(review.get("pages", []))
        covered.update(review.get("individual_pages", []))
        intervals = list(review.get("page_ranges", []))
        if "page_range" in review:
            intervals.append(review["page_range"])
        for interval in intervals:
            require(isinstance(interval, list) and len(interval) == 2,
                    "Invalid review page interval.")
            first, last = interval
            require(isinstance(first, int) and isinstance(last, int) and
                    1 <= first <= last <= pages, "Out-of-range visual review.")
            covered.update(range(first, last + 1))
    require(covered == set(range(1, pages + 1)),
            "The final QA review entries do not cover every PDF page exactly as a set.")
    return len(covered)


def portable_backtrack():
    """Keep lookup portable; neither network access nor this workspace is needed."""
    return r'''#!/usr/bin/env python3
"""Read-only claim lookup and exact source verification for the RH reconstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('claim', nargs='?', help='Claim ID, for example RU8, RD15, HM12, TC6, or SW8.')
parser.add_argument('--repo', type=Path, help='Local pinned source checkout, containing src/.')
parser.add_argument('--entry', type=int, help='Print only this numbered source entry (one-based).')
parser.add_argument('--max-lines', type=int, default=160, help='Maximum excerpt lines per entry; default 160.')
parser.add_argument('--list', action='store_true', help='List every stable claim ID and title.')
parser.add_argument('--check-all', action='store_true', help='Verify every source-file and inclusive-range hash, including next targets; requires --repo.')
args = parser.parse_args()
ledger = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
claims = {c['id']: c for c in ledger['claims']}
cache = {}

def source_ranges(value):
    if isinstance(value, dict):
        if {'path', 'sha256', 'line_start', 'line_end', 'range_sha256'} <= value.keys():
            yield value
        else:
            for child in value.values():
                yield from source_ranges(child)
    elif isinstance(value, list):
        for child in value:
            yield from source_ranges(child)

def checked_source(record):
    rel = Path(record['path'])
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError(f'Non-relative source path: {rel}')
    path = args.repo / rel
    if record['path'] not in cache:
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise ValueError(f'{path}: {exc}') from exc
        cache[record['path']] = (hashlib.sha256(raw).hexdigest(), raw.splitlines(keepends=True))
    digest, lines = cache[record['path']]
    if digest != record['sha256']:
        raise ValueError(f'File hash mismatch: {path}\nexpected {record["sha256"]}\nobserved {digest}')
    if 'range_sha256' in record:
        first, last = record['line_start'], record['line_end']
        if not (isinstance(first, int) and isinstance(last, int) and 1 <= first <= last <= len(lines)):
            raise ValueError(f'Invalid inclusive source range: {path}:{first}-{last}')
        if hashlib.sha256(b''.join(lines[first - 1:last])).hexdigest() != record['range_sha256']:
            raise ValueError(f'Inclusive source-range hash mismatch: {path}:{first}-{last}')
    return [line.decode('utf-8').rstrip('\r\n') for line in lines]

def update_keys(claim):
    pairs = []
    for key in claim:
        match = re.fullmatch(r'version_(\d+)_(\d+)_update', key)
        if match:
            pairs.append((tuple(map(int, match.groups())), key))
    return [key for _, key in sorted(pairs)]

def show_field(key, value):
    shown = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    print(key.replace('_', ' ') + ': ' + shown)

def latest_proofs(claim):
    updates = update_keys(claim)
    if not updates:
        return
    update = claim[updates[-1]]
    linked = update.get('discharged_by', []) if isinstance(update, dict) else []
    if isinstance(linked, str):
        linked = re.findall(r'\b[A-Z]+[0-9]+\b', linked)
    linked = [cid for cid in dict.fromkeys(linked) if cid in claims]
    if linked:
        print('\nLatest linked proof locations (' + updates[-1] + '):')
        for cid in linked:
            proof = claims[cid].get('proof_location', {})
            print('  ' + cid + ': ' + json.dumps(proof, ensure_ascii=False))

if args.max_lines < 1:
    parser.error('--max-lines must be positive')
if args.check_all:
    if args.repo is None:
        parser.error('--check-all requires --repo')
    targets_path = ROOT / 'next_source_targets.json'
    target_records = list(source_ranges(json.loads(targets_path.read_text(encoding='utf-8')))) if targets_path.exists() else []
    source_records = [record for c in ledger['claims'] for record in c['sources']]
    errors = []
    for record in [*ledger['source_files'], *source_records, *target_records]:
        try:
            checked_source(record)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        print('\n\n'.join(dict.fromkeys(errors)), file=sys.stderr)
        sys.exit(1)
    print(f'Verified {len(cache)} distinct source files, {len(source_records)} claim-source ranges, and {len(target_records)} next-target ranges against the SHA256 records for pinned commit {ledger["commit"]}.')
    print('This checks recorded source bytes and ranges; it does not compile Lean or replay its kernel.')
if args.list:
    for claim in ledger['claims']:
        print(f'{claim["id"]:5} {claim["title"]}')
if args.claim:
    claim = claims.get(args.claim.upper())
    if claim is None:
        parser.error(f'Unknown claim {args.claim!r}; use --list')
    print(f'{claim["id"]} — {claim["title"]}\nHistorical/recorded status: {claim["status"]}')
    fields = ['statement', 'claims', 'remaining_inputs', 'assumptions', 'source_relation',
              *update_keys(claim), 'proof_location', 'expanded_notes', 'depends_on',
              'dependencies', 'merged_application', 'merged_scope_classification',
              'resolved_companion_inputs', 'merge_scope_note']
    for key in fields:
        if key in claim:
            show_field(key, claim[key])
    latest_proofs(claim)
    if args.entry is not None and not 1 <= args.entry <= len(claim['sources']):
        parser.error(f'--entry must be between 1 and {len(claim["sources"])}')
    for number, record in enumerate(claim['sources'], 1):
        if args.entry is not None and args.entry != number:
            continue
        print(f'\n[{number}] {record["declaration"]}\n{record["path"]}:{record["line_start"]}–{record["line_end"]}\n{record["url"]}\nFile SHA256 {record["sha256"]}\nInclusive-range SHA256 {record["range_sha256"]}')
        if args.repo is not None:
            try:
                lines = checked_source(record)
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                sys.exit(1)
            stop = min(record['line_end'], record['line_start'] + args.max_lines - 1)
            for line_number in range(record['line_start'], stop + 1):
                print(f'{line_number:6}  {lines[line_number - 1]}')
            if stop < record['line_end']:
                print(f'... excerpt capped at {args.max_lines} lines; increase --max-lines to read the rest.')
if not (args.claim or args.list or args.check_all):
    parser.print_help()
'''


def verify_history(ledger, old_ledger):
    """Preserve literal old fields and graph edges, not just their meanings."""
    require(ledger['commit'] == PIN and ledger['artifact_version'] == '0.10',
            'Wrong current merged ledger.')
    require(old_ledger['commit'] == PIN and old_ledger['artifact_version'] == '0.9',
            'Wrong predecessor ledger.')
    by_id = {claim['id']: claim for claim in ledger['claims']}
    old_by_id = {claim['id']: claim for claim in old_ledger['claims']}
    require(len(old_by_id) == len(old_ledger['claims']) == EXPECTED_COUNTS['old_claims'],
            'Wrong predecessor claim count or duplicate ID.')
    require(len(by_id) == len(ledger['claims']) == EXPECTED_COUNTS['claims'],
            'Wrong current claim count or duplicate ID.')
    for cid, prior in old_by_id.items():
        require(cid in by_id, f'Missing historical claim: {cid}')
        for key, value in prior.items():
            if key == 'version_history':
                require(by_id[cid].get(key, [])[:len(value)] == value,
                        f'Historical status history changed: {cid}')
            else:
                require(by_id[cid].get(key) == value,
                        f'Historical claim field changed: {cid}.{key}')
        require(by_id[cid]['sources'] == prior['sources'],
                f'Historical source array changed: {cid}')
    expected_ids = {cid for _, _, ids in COMPONENTS.values() for cid in ids}
    require(set(by_id) - set(old_by_id) == expected_ids and
            len(expected_ids) == EXPECTED_COUNTS['new_claims'],
            'New IDs must be exactly RU11 + RD15 + HM12 + NP9 + TC6.')
    actual_updates = {cid for cid in old_by_id if 'version_0_10_update' in by_id[cid]}
    require(actual_updates == UPDATED_PRIOR_IDS, 'Unexpected current historical update IDs.')
    current_files = {record['path']: record for record in ledger['source_files']}
    old_files = {record['path']: record for record in old_ledger['source_files']}
    require(len(old_files) == len(old_ledger['source_files']) == EXPECTED_COUNTS['old_source_files'],
            'Wrong predecessor source-file count.')
    require(len(current_files) == len(ledger['source_files']) == EXPECTED_COUNTS['source_files'],
            'Wrong current source-file count.')
    for path, record in old_files.items():
        require(current_files.get(path) == record, f'Historical source-file record changed: {path}')
    old_graph = old_ledger['mathematical_dependency_graph']
    graph = ledger['mathematical_dependency_graph']
    for cid, dependencies in old_graph.items():
        require(graph.get(cid) == dependencies, f'Historical dependency graph changed: {cid}')
    order = ledger['dependency_topological_order']
    require(len(order) == len(by_id) and set(order) == set(by_id), 'Invalid current topological-order IDs.')
    position = {cid: i for i, cid in enumerate(order)}
    require(set(graph) == set(by_id), 'Current graph does not cover exactly the claim IDs.')
    for cid, dependencies in graph.items():
        for dependency in dependencies:
            require(dependency in position and position[dependency] < position[cid],
                    f'Unresolved or cyclic dependency: {cid} -> {dependency}')
    for key in ('version_0_8_local_conclusion', 'version_0_9_local_conclusions'):
        require(ledger[key] == old_ledger[key], f'Historical local conclusion changed: {key}')
    old_links = sum(len(claim['sources']) for claim in old_ledger['claims'])
    require(old_links == EXPECTED_COUNTS['old_source_links'], 'Wrong predecessor source-link count.')
    require(sum(len(claim['sources']) for claim in ledger['claims']) == EXPECTED_COUNTS['source_links'],
            'Wrong current source-link count.')
    return by_id, current_files


def make_readme(pages, starts, count):
    return f'''RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.10
21 November 2026

START HERE
RH_readable_reconstruction_v0_10.pdf is the cumulative {pages}-page note.
RH_readable_reconstruction_v0_10.tex is its self-contained LaTeX source.

NEW LOCAL CONCLUSION
TC6 completes the supplied-data local Type-I theorem: the literal HypI
implies Conclusion2 with C0>=880, CH>=2800001 and C=302114. The argument
now supplies the actual upper/lower ranks, weighted density, harmonic
models and cloud maps, uniform numerical fields, paired lattice lifts,
shifted height and exceptional-function conclusion. It uses direct
constructions instead of retaining the bundled AdmB/AdmT conditions as
unproved mathematical inputs.

The earlier supplied-data local Type-II theorem EA9 is unchanged:
ConclusionE holds under literal Hyps for C>=4129, with the cloud
constants (10,54,1088). Both statements retain their supplied local data.

This is still a partial human reconstruction of RH and Dirichlet GRH.
It is not a self-contained proof of either. GRH here concerns Dirichlet
L-functions; the note does not claim general automorphic or Dedekind GRH.
The actual global family existence and good-orbit abundance, finite-place
base change, theta/spectral and metric comparisons, cohomological windows
and simultaneous prime-selection arguments remain explicit work.

WHAT IS NEW
RU1–RU11: actual coarse upper rank, exact digit/HH dimensions, weighted
coefficient lattices and the paired HH assembly with primitive partners.
RD1–RD15: actual signed-chain lower rank, weighted bad-tail counting,
half-density, harmonic density and the final averaged segment loss.
HM1–HM12: harmonic-model and dimension identification, Smith/edge
transfer and KeyIneq, integral cloud maps via complementary minors,
and the complete-DVR RS-isomorphism argument for ring uniformity.
NP1–NP9: literal Std with H=4 and the full numerical package, including
all floor/ceiling bounds and the final shifted Type-I height.
TC1–TC6: primitive retraction, Smith splitting, Weyl losses, tensor
transport, the actual incoming GoodRankK construction, and Conclusion2.

The final heading-based section starts are:
  RU {starts['RU']}, RD {starts['RD']}, HM {starts['HM']},
  NP {starts['NP']}, TC {starts['TC']}.
The titles are detected in heading-sized PDF spans, so prose references
on the cover cannot be mistaken for a section. Shared start pages are
allowed. No page number is hard-coded in the packaging procedure.

READING ORDER
For the new endpoint, read TC and its exact hypotheses, then RU/RD,
HM and NP. The previous GG/TP/SW/RL sections give the actual graded
Gram, compatible-partner, weighted-form and paired-lift mechanisms.
The expanded reports are in rank_upper/, rank_lower/, harmonic_model/,
numerical_parameters/ and type_one_closure/.
For the RH implication, begin with the analytic endpoint, scalar balance
and frame/slope sections. Ordinary RH and a fixed Dirichlet character
have distinct host/window sections and remain separately identified.

CURRENT GLOBAL FRONTIER
The next_source_targets.json map has {count['next_target_ranges']} exact
declaration ranges in {count['next_target_source_files']} source files,
plus the same four independent global branches as the prior checkpoint.
It now points to the actual arithmetic-family HypIAt/HypIIAt supply,
uniform good-orbit abundance and finite-place StdSubAt/LPBaseChange.
These are different from the literal local HypI/Hyps implications
completed here. In particular, HM12 proves invariance under RS
isomorphisms; it does not prove arbitrary finite coefficient extension
or the global standard-submodule/base-change construction.

The theta/common-image and spectral/arithmetic-kernel identities,
retained-source metric transport and discarded-target control,
congruence denominators, two-primary and odd cohomological windows,
PairEx prime selection and the uniform centered-prime-sum conclusion
remain as stated in the main note. Supplied good-orbit geometry alone
does not prove that sufficiently many global good orbits exist.

PROVENANCE AND BACKTRACKING
provenance.json has {count['claims']} stable claims, including
{count['new_claims']} new claims, {count['source_links']} exact source
links and {count['source_files']} indexed primary source files.
provenance.txt is the readable ledger; source_index.json indexes files.
All 315 old claim fields/source arrays, all 764 old source-file records,
and every old dependency-graph entry are preserved. Version histories
only append annotations. The current version_0_10_update fields explain
which earlier local premises have been discharged. Historical component
reports retain their original scope and wording.

Every predecessor component/workflow/history file remains byte-identical.
The twelve superseded v0.9 root files, including its PDF/TeX, target map
and ledger, are preserved under history/version_0_9/. The earlier history
and baseline_provenance.json remain at their existing paths.

Pinned repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: {PIN}

Portable read-only lookup:
  python3 backtrack.py --list
  python3 backtrack.py RU8
  python3 backtrack.py RD15
  python3 backtrack.py HM12
  python3 backtrack.py TC6
  python3 backtrack.py SW8
  python3 backtrack.py RU11 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

The tool displays all version updates through version_0_10_update,
current proof locations linked by discharged_by, exact source ranges,
dependencies and merged applications. Historical status is labelled as
such, so it is read alongside the newer completion annotation.
With --repo, every excerpt is preceded by file- and inclusive-range
SHA256 verification. --check-all verifies all indexed source files,
all claim-source ranges and all current next-target ranges. The default
excerpt cap is 160 lines; --max-lines changes it. No network or third-party
Python package is required for the portable backtrack utility.

The huge source checkout and render/build caches are omitted. The
workflow_v0_10/ directory records the assembly, provenance, source-target,
review-metadata, rendering and packaging scripts. Those workflow scripts
record this workspace's layout; backtrack.py is the portable reader.
Review text, JSON join-source metadata and its builders are included
under reviews_v0_10/ as well as their applicable workflow locations.

PRECISION AND REVIEW
All earlier precision constraints remain in continuation_checkpoint.json,
with explicit supersession notes where the new local proofs apply.
The exact representation-dimension weights, digit multiplicities,
factorials and p/w normalizations are retained. The pairing convention
beHH=p^AHH G(F) is multiplicative. The lower-rank count uses actual kept
blocks; the upper matching does not require monotone early caps.

TC keeps the primitive dual factor p^(AH_minus-AH_plus), the one-sided
Smith hypothesis nLeD, the signs of the Weyl losses, and the small-weight
tensor height correction. Its incoming vectors are genuinely in the
cleaned lattices and satisfy GoodRankK through their actual pairing
matrix. An attained integer-valued exceptional certificate is transported
between RS-isomorphic coefficient rings; independently chosen exceptional
functions are not asserted equal. The constants stated above are
sufficient and are not claimed optimal.

Scoped mathematical cross-reviews are included. The exact final PDF has
been rendered and every page visually reviewed. No Lean source was
modified and no full Lean compilation or independent kernel replay was
run for this human reconstruction. Source-byte checks and mathematical
reviews are not presented as a kernel replay.

CONTINUATION AND INTEGRITY
continuation_checkpoint.json leads with the two completed local theorems
and the remaining global frontier. It preserves earlier findings and
precision constraints with their historical status.
visual_qa.json identifies the exact reviewed PDF by SHA256.
SHA256SUMS covers every bundled file except itself. ZIP membership,
duplicate-name absence, every CRC and every archived byte are checked
against the final folder. All predecessor files are preserved either
at their existing paths or in history/version_0_9/.
'''


def main():
    pdf_path = BASE / 'output/pdf/RH_readable_reconstruction_v0_10.pdf'
    tex_path = pdf_path.with_suffix('.tex')
    qa_path = BASE / 'v0_10/visual_qa.json'
    targets_path = BASE / 'v0_10/next_source_targets.json'
    require(qa_path.is_file(), 'Root must finish and approve v0_10/visual_qa.json before packaging.')
    qa_raw, targets_raw = qa_path.read_bytes(), targets_path.read_bytes()
    qa, next_doc = json.loads(qa_raw), json.loads(targets_raw)
    pdf_raw, tex_raw = pdf_path.read_bytes(), tex_path.read_bytes()
    pdf_sha = sha(pdf_raw)
    require(qa.get('all_pages_visually_reviewed') is True,
            'Every final PDF page must be visually reviewed.')
    require(qa.get('pdf_sha256') == pdf_sha, 'QA refers to another PDF.')
    require(qa.get('corrections_required_after_final_render') is False,
            'The final PDF still requires correction.')
    require(str(next_doc.get('version')) == '0.10' and next_doc.get('commit') == PIN,
            'Incorrect next-source target version or pin.')
    target_records = list(range_records(next_doc))
    target_paths = {record['path'] for record in target_records}
    require(next_doc.get('target_count') == len(target_records) == 24,
            'The current next-source map must contain exactly 24 declared ranges.')
    require(next_doc.get('source_file_count') == len(target_paths) == 12,
            'The current next-source map must contain exactly 12 source files.')
    old_next = read_json(OLD / 'next_source_targets.json')
    require(next_doc['global_branches_unchanged'] == old_next['global_branches_unchanged'],
            'The four global source branches changed.')
    require(len(next_doc['global_branches_unchanged']) == 4,
            'Expected four preserved global source branches.')

    merged_snapshots = {name: (OUT / name).read_bytes() for name in MERGED_NAMES}
    ledger = json.loads(merged_snapshots['provenance.json'])
    old_ledger = read_json(OLD / 'provenance.json')
    by_id, current_files = verify_history(ledger, old_ledger)
    source_index = json.loads(merged_snapshots['source_index.json'])
    require(source_index.get('commit') == PIN and source_index.get('artifact_version') == '0.10',
            'Wrong source-index version or pin.')
    require(source_index['source_files'] == ledger['source_files'],
            'Source index disagrees with the authoritative merged ledger.')
    checked_links, checked_source_files = verify_sources(ledger, target_records)
    require(checked_links == EXPECTED_COUNTS['source_links'], 'Unexpected verified source-link count.')
    conclusions = ledger['version_0_10_local_conclusions']
    require(conclusions['constants']['C0_min'] == 880 and
            conclusions['constants']['TM'] == 2800001 and
            conclusions['constants']['C'] == 302114,
            'The completed local Type-I constants changed.')

    headings = {}
    for label, (component, filename, _) in COMPONENTS.items():
        fragment = (BASE / 'v0_10' / component / filename).read_text(encoding='utf-8')
        match = re.search(r'\\(?:sub)?section\{([^{}]+)\}', fragment)
        require(match is not None, f'Missing section heading: {component}')
        heading = match.group(1)
        require(heading in tex_raw.decode('utf-8'), f'Current section missing from main: {label}')
        headings[label] = heading
    with fitz.open(stream=pdf_raw, filetype='pdf') as pdf:
        pages = len(pdf)
        matches = {label: [] for label in COMPONENTS}
        for number, page in enumerate(pdf, 1):
            # TC's exact title also occurs in cover prose. Restrict the search to
            # heading-sized spans; actual section titles are about 14.35 pt.
            heading_spans = [span['text'] for block in page.get_text('dict')['blocks']
                             for line in block.get('lines', [])
                             for span in line.get('spans', []) if span['size'] >= 12.5]
            key = heading_key(' '.join(heading_spans))
            for label, heading in headings.items():
                if heading_key(heading) in key:
                    matches[label].append(number)
    require(all(len(found) == 1 for found in matches.values()),
            'Each new section title must appear on exactly one heading-sized PDF page: ' + str(matches))
    starts = {label: found[0] for label, found in matches.items()}
    require(list(starts.values()) == sorted(starts.values()),
            'The new component section order is inconsistent.')
    require(qa.get('page_count') == pages, 'PDF/QA page count mismatch.')
    coverage = reviewed_pages(qa, pages)
    page_map = {label: {'component': component, 'title': headings[label],
                        'page_start': starts[label], 'fragment': filename}
                for label, (component, filename, _) in COMPONENTS.items()}

    excluded = {'README.txt', *MERGED_NAMES, 'continuation_checkpoint.json', 'SHA256SUMS',
                'backtrack.py', 'component_filename_map.json', 'next_source_targets.json',
                'visual_qa.json', 'RH_readable_reconstruction_v0_9.pdf',
                'RH_readable_reconstruction_v0_9.tex'}
    require(len(excluded) == 12 and all((OLD / name).is_file() for name in excluded),
            'Expected exactly twelve predecessor root files to archive.')
    plan = []
    for source in sorted(OLD.rglob('*')):
        if not source.is_file():
            continue
        rel = source.relative_to(OLD)
        if source.parent == OLD and source.name in excluded:
            dest, category = Path('history/version_0_9') / source.name, 'archived_previous_root'
        else:
            dest, category = rel, 'historical'
        plan.append((source, dest, category))
    for component, _, _ in COMPONENTS.values():
        component_root = BASE / 'v0_10' / component
        for source in sorted(component_root.rglob('*')):
            if (source.is_file() and source.suffix in {'.tex', '.txt', '.json', '.py'} and
                    source.name not in {'source_paths.json', 'declaration_catalog.json'} and
                    '__pycache__' not in source.parts):
                plan.append((source, Path(component) / source.relative_to(component_root), 'new_component'))
    for source in sorted((BASE / 'v0_10').rglob('*.py')):
        if '__pycache__' not in source.parts:
            plan.append((source, Path('workflow_v0_10') / source.relative_to(BASE / 'v0_10'), 'workflow'))
    review_root = BASE / 'v0_10/reviews'
    for source in sorted(review_root.rglob('*')):
        if (source.is_file() and source.suffix in {'.txt', '.json', '.py', '.tex'} and
                '__pycache__' not in source.parts):
            plan.append((source, Path('reviews_v0_10') / source.relative_to(review_root), 'review'))
    plan += [(pdf_path, Path(pdf_path.name), 'main'), (tex_path, Path(tex_path.name), 'main'),
             (qa_path, Path('visual_qa.json'), 'qa'),
             (qa_path, Path('workflow_v0_10/visual_qa.json'), 'workflow'),
             (targets_path, Path('next_source_targets.json'), 'targets'),
             (targets_path, Path('workflow_v0_10/next_source_targets.json'), 'workflow')]
    names = [rel.as_posix() for _, rel, _ in plan]
    require(len(names) == len(set(names)), 'Duplicate package destination.')
    generated = {*MERGED_NAMES, 'README.txt', 'continuation_checkpoint.json', 'backtrack.py',
                 'component_filename_map.json', 'SHA256SUMS'}
    expected = set(names) | generated
    existing = {path.relative_to(OUT).as_posix() for path in OUT.rglob('*') if path.is_file()}
    require(existing <= expected, 'Unmanaged files in final package: ' + ', '.join(sorted(existing - expected)))
    # Hold exact input bytes. The final copy checks also reject concurrent edits
    # to any historical file, review, component, or workflow during packaging.
    plan_snapshots = {source: source.read_bytes() for source, _, _ in plan}
    categories = {category: sum(kind == category for _, _, kind in plan)
                  for category in {kind for _, _, kind in plan}}
    require(categories.get('archived_previous_root') == 12, 'The twelve old root files were not all archived.')

    previous = read_json(OLD / 'continuation_checkpoint.json')
    results = [
        'RU1–RU11: exact coarse upper rank on each actual digit class; source and retained weighted-lattice dimensions; actual paired HH assembly from attained GoodShare lattices, with its primitive normalization and scalar loss.',
        'RD1–RD15: signed-chain lower matching and weighted tail counts; lower rank and half-density; actual harmonic density, segment summation and the final averaged loss.',
        'HM1–HM12: actual harmonic models and dimensions, Smith and edge transfer, KeyIneq, integral cloud maps with explicit complementary-minor duality, and complete-DVR RS-isomorphism invariance.',
        'NP1–NP9: a uniform literal numerical package, Std at H=4, actual model and partner bounds, all floor/ceiling comparisons, and the final shifted Type-I height.',
        'TC1–TC6: primitive retraction and Smith splitting, Weyl comparison, small-weight tensor transport, actual incoming GoodRankK, ring-uniform exceptional functions and the complete supplied-data local Type-I Conclusion2.',
    ]
    remaining = [
        'Global abundance and compatibility of the actual HypIAt/HypIIAt family records, including uniformly many good orbits and simultaneous weights, primes, fields and local choices. TC6 and EA9 prove the two local conclusions under supplied literal data; they do not construct all these global data.',
        'Finite-place standard-submodule and finite coefficient-extension input StdSubAt/LPBaseChange. HM12 proves invariance under RS isomorphisms; it does not prove this distinct finite-extension/base-change theorem.',
        *previous['remaining_major_inputs'][2:],
    ]
    additions = [
        'All prior precision constraints remain verbatim as historical records. The v0.10 updates supersede only the old supplied-data local Type-I boundary; the separate global parameter, arithmetic, metric and cohomological inputs remain explicit.',
        'RU identifies the actual digit and weighted coefficient lattices before counting. Its early caps need not be monotone; the matching retains every endpoint, order and level index.',
        'RD counts pairs with their exact representation-dimension weights, not an unweighted fraction of paths. Its half-density uses literal Std(H=4), signed strips, the ceiling margin, and C0>=880.',
        'The HH assembly uses actual saturated GoodSub lattices and finite rank attainment. The beHH normalization is multiplicative p^AHH. The mass bound is automatic when the total loss is at least one, and only otherwise are the nonnegative loss factors multiplied.',
        'HM uses the actual harmonic polynomial models and integral complementary-minor maps. The source and dual denominators are retained; the small-weight tensor height loss is exactly 2n-prime times its conductor.',
        'HM12 concerns complete-DVR RS-isomorphism invariance. It does not discharge the distinct finite-place StdSubAt/LPBaseChange or finite coefficient-extension construction in the global target map.',
        'NP supplies the literal Std and numerical records with their quantifier order, odd-power excluded band, floors and ceilings. Its final comparison is the constructed height plus the exact small-weight tensor correction, bounded by tI.',
        'TC keeps the primitive retraction dual factor p^(AH_minus-AH_plus), the one-sided nLeD hypothesis in the Smith split, and the correct signs of the Weyl losses. Its incoming GoodRankK uses the actual pairing matrix and integral near-identity inversion.',
        'The integer-valued exceptional infimum is attained. Ring uniformity chooses a certificate and transports it through the actual RS isomorphism; it does not assert that independently chosen exceptional functions are equal.',
        'TC6 proves supplied-data local Type I with C0>=880, CH>=2800001 and C=302114. EA9 remains the supplied-data local Type-II theorem with C>=4129 and cloud constants (10,54,1088). These sufficient constants are not asserted optimal.',
        'Every previous claim field, source array, source-file record and old dependency-graph entry is retained. Current version_0_10_update fields and linked proof locations explain the superseded local boundaries without rewriting historical proofs.',
    ]
    supersessions = list(previous.get('precision_supersessions', []))
    for historical in previous['precision_constraints']:
        if (historical.startswith('TI6 retains') or 'SW8 is conditional' in historical or
                'The complete Type-I Conclusion2' in historical):
            supersessions.append({
                'previous_checkpoint_version': '0.9', 'historical_statement': historical,
                'current_statement': 'RU/RD supply the actual ranks and density; HM supplies the actual harmonic/cloud maps and RS-isomorphism transport; NP supplies the uniform numerical and height comparisons. TC6 completes supplied-data local Type I. All distinct global existence, base-change, window and analytic inputs remain.',
                'completed_by': ['RU8', 'RU11', 'RD15', 'HM12', 'NP8', 'TC6'],
            })
    count = {'claims': len(by_id), 'new_claims': EXPECTED_COUNTS['new_claims'],
             'source_links': checked_links, 'source_files': len(current_files),
             'next_target_ranges': len(target_records), 'next_target_source_files': len(target_paths),
             'source_files_checked_including_next_targets': checked_source_files}
    checkpoint = {
        'project': previous['project'], 'artifact_version': '0.10', 'date': '2026-11-21',
        'predecessor_version': '0.9', 'source_repository': ledger['repository'], 'source_commit': PIN,
        'user_instruction': previous['user_instruction'], 'main_note_pages': pages,
        'new_section_start_pages': starts, 'new_section_headings': headings,
        'logical_component_page_map': page_map,
        'status': 'Partial RH/Dirichlet-GRH human reconstruction. Both local types are now complete under supplied literal data: Type I by TC6 (C0>=880, CH>=2800001, C=302114), and unchanged Type II by EA9 (C>=4129). Global family existence, finite-place base change, spectral/metric and cohomological-window inputs remain.',
        'new_in_this_version': results,
        'retained_prior_results': previous['retained_prior_results'] + previous['new_in_this_version'],
        'retained_prior_results_note': 'Earlier entries describe their own versions. Current local conclusions and remaining inputs are stated in version_0_10_update and remaining_major_inputs.',
        'remaining_major_inputs': remaining,
        'next_targets': [next_doc['next_local_priority'],
                         'Distinguish the actual global HypIAt/HypIIAt family supply and finite-place StdSubAt/LPBaseChange from the completed local HypI/Hyps constructions and HM12 RS-isomorphism invariance.',
                         'Advance the four unchanged independent global branches; do not relabel the completed local theorems as global abundance or arithmetic-window theorems.'],
        'next_source_targets_file': 'next_source_targets.json',
        'previous_source_targets_file': 'history/version_0_9/next_source_targets.json',
        'precision_constraints': previous['precision_constraints'] + additions,
        'precision_supersessions': supersessions,
        **{key: value for key, value in previous.items()
           if key.startswith('version_') and key.endswith('_update')},
        'version_0_10_update': {
            'local_conclusions': conclusions,
            'superseded_previous_local_frontier': previous['remaining_major_inputs'][0],
            'remaining_global_frontier': remaining,
            'historical_claim_updates': sorted(UPDATED_PRIOR_IDS),
            'historical_source_arrays': 'All 315 prior claim fields/source arrays and 764 prior source-file records are preserved; version histories only append new annotations.',
            'historical_dependency_graph': 'Every old graph entry is preserved exactly; the new graph is checked against its topological order.',
            'historical_components': 'Every predecessor file is byte-identical at its former path or archived under history/version_0_9; exactly twelve predecessor root files are archived.',
        },
        'validation': {
            **count, 'all_cited_ranges_and_file_hashes_checked': True,
            'all_source_bytes_match_pinned_git_blobs': True,
            'all_prior_claim_fields_and_source_arrays_preserved': True,
            'all_prior_source_records_preserved_exactly': True,
            'all_prior_dependency_graph_entries_preserved': True,
            'historical_component_files_preserved': categories.get('historical', 0),
            'previous_root_files_archived': categories.get('archived_previous_root', 0),
            'new_component_files_copied': categories.get('new_component', 0),
            'review_files_copied': categories.get('review', 0),
            'all_reviewed_pages': coverage, 'full_lean_build_or_kernel_replay': False,
            'lean_sources_modified': False,
            'cross_reviews': 'Independent records cover RU matching and HH lattice assembly, RD tails and density, HM harmonic/cloud and ring transport, NP numerical constants, TC primitive retraction/Smith/Weyl/tensor/GoodRankK, and the final GoodShare/D0/exceptional-function joins. Review JSON source metadata and its builders are included.',
            'pdf': qa,
        },
    }
    filename_map = read_json(OLD / 'component_filename_map.json')
    filename_map['note'] = 'Historical component bytes and source arrays are preserved. The current main and version_0_10_update complete supplied-data local Type I. Global family, finite-extension, metric and arithmetic-window inputs remain. Superseded root files are archived under history/version_0_9/.'
    filename_map['version_0_10_component_pages'] = page_map
    backtrack = portable_backtrack()
    compile(backtrack, 'backtrack.py', 'exec')  # Syntax only; no package utility is executed here.
    readme = make_readme(pages, starts, count)

    # Every scope/source/history/QA check above precedes writes to the package.
    for source, rel, _ in plan:
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        require(source.read_bytes() == plan_snapshots[source], f'Input changed before copying: {source}')
        target.write_bytes(plan_snapshots[source])
        require(target.read_bytes() == plan_snapshots[source], f'Copy mismatch: {rel}')
    (OUT / 'backtrack.py').write_text(backtrack, encoding='utf-8')
    write_json(OUT / 'component_filename_map.json', filename_map)
    write_json(OUT / 'continuation_checkpoint.json', checkpoint)
    (OUT / 'README.txt').write_text(readme, encoding='utf-8')
    for path, raw in [(pdf_path, pdf_raw), (tex_path, tex_raw), (qa_path, qa_raw), (targets_path, targets_raw)]:
        require(path.read_bytes() == raw, f'Input changed during packaging: {path}')
    for name, raw in merged_snapshots.items():
        require((OUT / name).read_bytes() == raw, f'Authoritative ledger changed: {name}')
    for source, rel, category in plan:
        require(source.read_bytes() == plan_snapshots[source], f'Source changed during packaging ({category}): {source}')
        require((OUT / rel).read_bytes() == plan_snapshots[source], f'Final copy mismatch ({category}): {rel}')

    entries = [path for path in sorted(OUT.rglob('*')) if path.is_file() and path != OUT / 'SHA256SUMS']
    require({path.relative_to(OUT).as_posix() for path in entries} == expected - {'SHA256SUMS'},
            'Final folder membership differs from the validated copy/generation plan.')
    sums = ''.join(sha(path.read_bytes()) + '  ' + path.relative_to(OUT).as_posix() + '\n' for path in entries)
    (OUT / 'SHA256SUMS').write_text(sums, encoding='utf-8')
    entries.append(OUT / 'SHA256SUMS')
    zip_path = OUT.with_suffix('.zip')
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(entries):
            archive.write(path, arcname=path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(zip_path) as archive:
        require(archive.testzip() is None, 'ZIP CRC failure.')
        expected_names = {path.relative_to(OUT).as_posix() for path in entries}
        require(len(archive.namelist()) == len(expected_names) and set(archive.namelist()) == expected_names,
                'ZIP membership or multiplicity mismatch.')
        for path in entries:
            require(archive.read(path.relative_to(OUT).as_posix()) == path.read_bytes(),
                    f'ZIP byte mismatch: {path}')
    # Recheck every recorded sum after the archive verification, not only before it.
    for row in sums.splitlines():
        digest, relative = row.split('  ', 1)
        require(sha((OUT / relative).read_bytes()) == digest, f'Final SHA256SUMS mismatch: {relative}')
    receipt = {
        **count, 'pdf_pages': pages, 'new_section_start_pages': starts, 'pdf_sha256': pdf_sha,
        'zip_sha256': sha(zip_path.read_bytes()), 'zip_bytes': zip_path.stat().st_size,
        'zip_members': len(entries), 'copied_file_categories': categories,
        'zip_crc_membership_and_every_byte_verified': True, 'all_sha256sums_rechecked': True,
        'all_predecessor_files_preserved': True, 'all_old_dependency_graph_entries_preserved': True,
        'all_pages_visually_reviewed': True, 'full_lean_build_or_kernel_replay': False,
    }
    write_json(BASE / 'v0_10/package_validation.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

