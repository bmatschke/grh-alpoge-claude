#!/usr/bin/env python3
"""Package the final visually reviewed v0.11 note and cumulative proof record.

Do not run until root has written and confirmed v0_11/visual_qa.json.
The merged ledger must already exist in output/RH_reconstruction_v0_11.
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
OUT = BASE / "output/RH_reconstruction_v0_11"
OLD = BASE / "output/RH_reconstruction_v0_10"
REPO = BASE / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENTS = {
    "GII": ("type_two_family", "main.tex", [f"GII{i}" for i in range(1,11)]),
    "GI": ("type_one_family", "main.tex", [f"GI{i}" for i in range(1,9)]),
    "BC": ("base_change", "main.tex", [f"BC{i}" for i in range(1,9)]),
    "GJ": ("family_join", "main.tex", [f"GJ{i}" for i in range(1,6)]),
    "GW": ("global_weight_choice", "main.tex", [f"GW{i}" for i in range(1,7)]),
    "HW": ("host_weight_join", "main.tex", [f"HW{i}" for i in range(1,4)]),
}
UPDATED_PRIOR_IDS = {"EA9", "TC6"}
EXPECTED_COUNTS = {'old_claims': 368, 'claims': 408, 'new_claims': 40, 'old_source_files': 890, 'source_files': 949, 'old_source_links': 5817, 'source_links': 6793}

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
parser.add_argument('claim', nargs='?', help='Claim ID, for example GW5, HW2, GJ4, BC7, GI8, or TC6.')
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
    require(ledger['commit'] == PIN and ledger['artifact_version'] == '0.11',
            'Wrong current merged ledger.')
    require(old_ledger['commit'] == PIN and old_ledger['artifact_version'] == '0.10',
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
            'New IDs must be exactly GII10 + GI8 + BC8 + GJ5 + GW6 + HW3.')
    actual_updates = {cid for cid in old_by_id if 'version_0_11_update' in by_id[cid]}
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
    for key in ('version_0_8_local_conclusion', 'version_0_9_local_conclusions', 'version_0_10_local_conclusions'):
        require(ledger[key] == old_ledger[key], f'Historical local conclusion changed: {key}')
    old_links = sum(len(claim['sources']) for claim in old_ledger['claims'])
    require(old_links == EXPECTED_COUNTS['old_source_links'], 'Wrong predecessor source-link count.')
    require(sum(len(claim['sources']) for claim in ledger['claims']) == EXPECTED_COUNTS['source_links'],
            'Wrong current source-link count.')
    return by_id, current_files


def make_readme(pages, starts, count):
    return f'''RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.11
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed independent proof
of RH or Dirichlet GRH. It preserves both completed supplied-data local
theorems and now proves the actual numerical family supply, finite
coefficient extension, orbit application and global degree selection.
Full arithmetic-family construction and four independent global branches
remain explicit. These are limits of this exposition, not assertions of
omitted arguments in the released source.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_11.pdf is the cumulative {pages}-page note.
Its matching TeX source is included. Start with the route and analytic
argument, or go directly to the new application:

  GJ1–GJ5: actual family/orbit join, page {starts['GJ']}.
  GW1–GW6: one degree pair controlling all candidate primes, page {starts['GW']}.
  HW1–HW3: the active host preselection and fixed-pair family, page {starts['HW']}.
  GII1–GII10: actual Type-II family data and probability, page {starts['GII']}.
  GI1–GI8: actual Type-I family hypotheses and mean, page {starts['GI']}.
  BC1–BC8: standard coefficient ring and finite extension, page {starts['BC']}.

The shorter main sections are supported by complete expanded report.txt
companions in those six component directories. Each directory also has
a standalone source-ledger builder and declaration/range locators.

WHAT THE NEW PROOFS ESTABLISH
GII proves the actual per-good-orbit count, logarithmic windows and every
Type-II numerical inequality, including N1^2<=rN and the full Q^5 size
budget. Its probability argument proves uniform-Bernoulli BadProb and
existential TopsOK, with forced-point conditioning handled explicitly.
The actual host additionally needs biased coset selection and Frame.Shares;
uniform per-good-orbit density alone is not an abundance assertion.

GI proves all fourteen actual Type-I numerical fields, exact window and
forbidden-band translation, the actual cyclic predecessor/time bound,
and the canonical mean from the completed local theorem TC6. The fixed
coefficient vector is chosen before a single threshold uniform in all
family indices, primes and good representatives.

BC constructs the standard ring W(F_(q^2))[omega]/(omega^2-p), a finite
normalization and an embedding inducing the specified number-field place.
It proves integral coefficient-lattice, algebraic-dual, arbitrary clean
intersection and GoodRankK transport. LPprime extends with precisely the
same height t, depth D, deficit kappa and conductor c*. The image of omega
need not be a uniformizer in the larger ring. StdSubAt means a standard
coefficient SUBRING. The actual GroupCompatibilityFamily ring field is
one application; recC/IsRecCEv is another sufficient identification.

GJ proves attainment of the universal Type-I deficit infimum without
losing its ring/weight/target quantifiers. It obtains explicit uniform
scale bounds, identifies the actual cyclic orbits and weights, and proves
the literal OrbitLatticeBounds join for both prime ranges.

GW uses exact constant-fibre marginalization of the finite degree boxes.
The local mean bound E kappa_v<=Nv*x^-12 yields E Sigma_p<=m*|TT|*x^-12.
An elementary harmonic sum and the indicator bound give
  E Z <=8*x^(-9-gamma), gamma=1/2-(1453/150)eps>2447/7800.
For 32*x^-gamma<=1, one pair satisfies the exact source inequality
  sum_candidates (log p)/p * (2*1_(Sigma_p>x^-eps)+4*Sigma_p) <= x^-9.
The same pair is used at all primes; independence between primes is not
required. ChosenW transports it through every member carrying the pair.
Optional CoverAll gives a carrier, but it is not imposed on the active route.

HW follows that active route: transfer the point degree condition to host
WOK, preselect one pair, rebuild points at all distinguished positions
with that fixed pair, and pass through KitS/famOfKits to ChosenWall and
ChosenWS. The upstream host and point constructors, numerical supply at
that construction, and biased Frame.Shares remain explicit premises.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants (10,54,1088). The sufficient constants are not
claimed optimal. Their original proofs and ledgers are unchanged.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: {count['claims']} stable claims, {count['source_links']}
source links, {count['source_files']} indexed primary source files.
There are 40 new claims: GII10+GI8+BC8+GJ5+GW6+HW3.

Every source record has its qualified declaration, inclusive original
line range, pinned URL, full-file SHA256 and range SHA256. The current
component builders compare source bytes with the pinned Git blobs.
provenance.json is authoritative; provenance.txt is its readable view.
source_index.json records the full-file hashes. The explicit mathematical
dependency graph is acyclic; it is not a Lean transitive dependency audit.

Examples after unpacking, with a local pinned source checkout:
  python backtrack.py GW5
  python backtrack.py HW2 --repo /path/to/riemann-hypothesis-lean
  python backtrack.py BC7 --repo /path/to/riemann-hypothesis-lean --entry 1
  python backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean
The read-only helper works without network access and can resolve every
historical ID, its newer annotations, and the current continuation ranges.

CONTINUITY
All 368 prior claim fields/source arrays, all 890 prior source-file
records and every prior mathematical dependency edge are preserved.
Only version_0_11_update annotations are appended to EA9 and TC6.
Every predecessor file is byte-identical at its original package path or
under history/version_0_10/. Exactly twelve superseded root files are
archived there, including the v0.10 note and checkpoint. Earlier histories
and all earlier source locators remain included.

NEXT WORK
The concrete next targets are in next_source_targets.json and the
continuation checkpoint. They prioritize actual host construction with
biased Frame.Shares, the underlying local-place/character/rank/comparison
data, and the remaining gain/prime-loss estimates. They distinguish
active constructors from wrappers and optional sufficient interfaces.
The same four independent branches remain: actual theta/spectral kernels,
dimension/metric/discarded-target control, congruence/cohomological windows,
and simultaneous PairEx plus the centered prime-sum window theorem.

VERIFICATION AND LIMITS
The mathematical cross-reviews, exact-source checks, historical-preservation
checks, PDF visual review and package checksums are recorded. visual_qa.json
names the exact reviewed PDF by SHA256. Every PDF page was rendered and
visually reviewed. SHA256SUMS covers every package file except itself.
No Lean source was modified; no full Lean build or independent kernel replay
was run. This package makes no new public verification-status assertion.
'''

def main():
    pdf_path = BASE / 'output/pdf/RH_readable_reconstruction_v0_11.pdf'
    tex_path = pdf_path.with_suffix('.tex')
    qa_path = BASE / 'v0_11/visual_qa.json'
    targets_path = BASE / 'v0_11/next_source_targets.json'
    require(qa_path.is_file(), 'Root must finish and approve v0_11/visual_qa.json before packaging.')
    qa_raw, targets_raw = qa_path.read_bytes(), targets_path.read_bytes()
    qa, next_doc = json.loads(qa_raw), json.loads(targets_raw)
    pdf_raw, tex_raw = pdf_path.read_bytes(), tex_path.read_bytes()
    pdf_sha = sha(pdf_raw)
    require(qa.get('all_pages_visually_reviewed') is True,
            'Every final PDF page must be visually reviewed.')
    require(qa.get('pdf_sha256') == pdf_sha, 'QA refers to another PDF.')
    require(qa.get('corrections_required_after_final_render') is False,
            'The final PDF still requires correction.')
    require(str(next_doc.get('version')) == '0.11' and next_doc.get('commit') == PIN,
            'Incorrect next-source target version or pin.')
    target_records = list(range_records(next_doc))
    target_paths = {record['path'] for record in target_records}
    require(next_doc.get('target_count') == len(target_records) and len(target_records)>=8,
            'The current next-source map range count is inconsistent.')
    require(next_doc.get('source_file_count') == len(target_paths),
            'The current next-source map file count is inconsistent.')
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
    require(source_index.get('commit') == PIN and source_index.get('artifact_version') == '0.11',
            'Wrong source-index version or pin.')
    require(source_index['source_files'] == ledger['source_files'],
            'Source index disagrees with the authoritative merged ledger.')
    checked_links, checked_source_files = verify_sources(ledger, target_records)
    require(checked_links == EXPECTED_COUNTS['source_links'], 'Unexpected verified source-link count.')
    conclusions = ledger['version_0_11_local_conclusions']
    require(ledger['version_0_10_local_conclusions']['constants']['C0_min'] == 880 and
            ledger['version_0_10_local_conclusions']['constants']['TM'] == 2800001 and
            ledger['version_0_10_local_conclusions']['constants']['C'] == 302114,
            'The completed local Type-I constants changed.')

    headings = {}
    for label, (component, filename, _) in COMPONENTS.items():
        fragment = (BASE / 'v0_11' / component / filename).read_text(encoding='utf-8')
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
                'visual_qa.json', 'RH_readable_reconstruction_v0_10.pdf',
                'RH_readable_reconstruction_v0_10.tex'}
    require(len(excluded) == 12 and all((OLD / name).is_file() for name in excluded),
            'Expected exactly twelve predecessor root files to archive.')
    plan = []
    for source in sorted(OLD.rglob('*')):
        if not source.is_file():
            continue
        rel = source.relative_to(OLD)
        if source.parent == OLD and source.name in excluded:
            dest, category = Path('history/version_0_10') / source.name, 'archived_previous_root'
        else:
            dest, category = rel, 'historical'
        plan.append((source, dest, category))
    for component, _, _ in COMPONENTS.values():
        component_root = BASE / 'v0_11' / component
        for source in sorted(component_root.rglob('*')):
            if (source.is_file() and source.suffix in {'.tex', '.txt', '.json', '.py'} and
                    source.name not in {'source_paths.json', 'declaration_catalog.json'} and
                    '__pycache__' not in source.parts):
                plan.append((source, Path(component) / source.relative_to(component_root), 'new_component'))
    for source in sorted((BASE / 'v0_11').rglob('*.py')):
        if '__pycache__' not in source.parts:
            plan.append((source, Path('workflow_v0_11') / source.relative_to(BASE / 'v0_11'), 'workflow'))
    review_root = BASE / 'v0_11/reviews'
    for source in sorted(review_root.rglob('*')):
        if (source.is_file() and source.suffix in {'.txt', '.json', '.py', '.tex'} and
                '__pycache__' not in source.parts):
            plan.append((source, Path('reviews_v0_11') / source.relative_to(review_root), 'review'))
    for source in sorted((BASE/'v0_11').glob('next_*_targets.txt')):
        plan.append((source,Path('workflow_v0_11')/source.name,'workflow'))
    plan += [(pdf_path, Path(pdf_path.name), 'main'), (tex_path, Path(tex_path.name), 'main'),
             (qa_path, Path('visual_qa.json'), 'qa'),
             (qa_path, Path('workflow_v0_11/visual_qa.json'), 'workflow'),
             (targets_path, Path('next_source_targets.json'), 'targets'),
             (targets_path, Path('workflow_v0_11/next_source_targets.json'), 'workflow')]
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
        'GII1–GII10: exact per-good-orbit counts, logarithmic window bounds, every Type-II numerical field and local application; conditional BadProb and existential uniform-Bernoulli TopsOK.',
        'GI1–GI8: every actual Type-I numerical field, uniform HypIAt, exact band/window/depth comparison, cyclic predecessor and height, and canonical mean.',
        'BC1–BC8: actual standard coefficient ring, prescribed-place finite normalization, exact integral/dual/clean lattice transfer, LPBaseChange and StdSubAt for identified constructions.',
        'GJ1–GJ5: universal canonical infimum attainment, explicit uniform scale bounds, actual cyclic and weight identifications, exact OrbitLatticeBounds join.',
        'GW1–GW6: exact local/global finite marginal averages, one simultaneous degree choice with WReq<=x^-9, ChosenW and optional full-coverage realization.',
        'HW1–HW3: active point-to-host WReq/WOK transfer, fixed-pair/all-position rebuilding, and transport to ChosenWall/ChosenWS without CoverAll.',
    ]
    remaining = [
        'Construct the actual host and full point/family data simultaneously: biased coset top selection and Frame.Shares, the point construction for admissible degrees, and the associated numerical and analytic/arithmetic duties. HW proves their preselected-pair transport without assuming optional CoverAll.',
        'Construct the underlying compatible local place identifications, integral away-characters, exact rank matching and global-to-local comparison-lattice span. BC proves coefficient extension, GJ the orbit application; supplied GroupCompatibilityFamily data must still be realized with the rest of the construction.',
        *previous['remaining_major_inputs'][2:],
    ]
    additions = [
        'All prior precision constraints remain as historical records; current v0.11 annotations supersede the numerical-family and finite-extension boundaries only to the extent explicitly proved.',
        'GI/GII prove numerical and geometric implications for the actual supplied family fields, with constants before one uniform threshold, then family index, candidate prime and good representative.',
        'Scale.A is 26; the Type-I averaging width is x^13. Global chain length m_ch=D.R.m differs from local m=k-1.',
        'Per-good-orbit top density is separate from abundance of good orbits. GII9–10 use uniform Bernoulli selection; the actual host uses biased coset probabilities and the separate Frame.Shares property.',
        'StdSubAt means a standard coefficient subring. BC constructs it rather than assuming an arbitrary Hida DVR has the doubled residue field.',
        'Finite extension preserves the source W, q, Frobenius and edge set. The image of omega^2=p need not be a uniformizer; height/depth/conductor use its actual powers and p-normalization, without an extra ramification multiplier.',
        'The universal Type-I infimum is attained after fixing each ring, weight and target. Witnesses may vary; no uniform bound on representation dimensions or interchange of infimum and universal quantifiers is assumed.',
        'GW marginalization uses exact constant-size restriction fibres. Independence across primes is not required. The selected pair bounds a weighted exceptional set, not every prime separately.',
        'CoverAll is a separate optional sufficient property. The active HW route preselects a pair, then rebuilds all distinguished positions and supplies ChosenWall; it does not require CoverAll for the final family.',
        'IsRecCEv is an optional sufficient identification. Active linked-family routes construct GroupCompatibilityFamily through local places, characters, dimensions and comparison-lattice data.',
        'All 368 prior claim fields/source arrays, 890 prior source-file records and every old dependency graph entry remain unchanged. Current annotations do not overwrite historical claims.',
    ]
    supersessions = list(previous.get('precision_supersessions', []))
    for historical in previous['precision_constraints']:
        if ('StdSubAt/LPBaseChange' in historical or 'Global abundance and compatibility' in historical):
            supersessions.append({
                'previous_checkpoint_version':'0.10','historical_statement':historical,
                'current_statement':'GI/GII supply the actual numerical-family implications; BC proves the standard-subring and finite-extension arguments; GJ proves the exact orbit join; GW/HW prove degree selection and active transport. Full host/local-comparison/family construction remains separate.',
                'completed_by':['GI5','GI8','GII7','GII8','BC7','BC8','GJ4','GW5','HW3'],
            })
    count = {'claims': len(by_id), 'new_claims': EXPECTED_COUNTS['new_claims'],
             'source_links': checked_links, 'source_files': len(current_files),
             'next_target_ranges': len(target_records), 'next_target_source_files': len(target_paths),
             'source_files_checked_including_next_targets': checked_source_files}
    checkpoint = {
        'project': previous['project'], 'artifact_version': '0.11', 'date': '2026-11-21',
        'predecessor_version': '0.10', 'source_repository': ledger['repository'], 'source_commit': PIN,
        'user_instruction': previous['user_instruction'], 'main_note_pages': pages,
        'new_section_start_pages': starts, 'new_section_headings': headings,
        'logical_component_page_map': page_map,
        'status':'Partial RH/Dirichlet-GRH reconstruction. Actual supplied-family numerical hypotheses, finite coefficient extension, orbit application, one global degree selection and active host/family transport are proved. Full joint construction and independent global branches remain.',
        'new_in_this_version': results,
        'retained_prior_results': previous['retained_prior_results'] + previous['new_in_this_version'],
        'retained_prior_results_note': 'Earlier entries describe their own versions. Current local conclusions and remaining inputs are stated in version_0_11_update and remaining_major_inputs.',
        'remaining_major_inputs': remaining,
        'next_targets': [next_doc['next_local_priority'],
                         'Construct the actual biased top/frame data and underlying local comparison objects; preserve the distinction between the active HW preselection route and optional CoverAll/IsRecCEv interfaces.',
                         'Advance the four unchanged independent global branches; do not relabel the completed local theorems as global abundance or arithmetic-window theorems.'],
        'next_source_targets_file': 'next_source_targets.json',
        'previous_source_targets_file': 'history/version_0_10/next_source_targets.json',
        'precision_constraints': previous['precision_constraints'] + additions,
        'precision_supersessions': supersessions,
        **{key: value for key, value in previous.items()
           if key.startswith('version_') and key.endswith('_update')},
        'version_0_11_update': {
            'local_conclusions': conclusions,
            'superseded_previous_local_frontier': previous['remaining_major_inputs'][0],
            'remaining_global_frontier': remaining,
            'historical_claim_updates': sorted(UPDATED_PRIOR_IDS),
            'historical_source_arrays': 'All 368 prior claim fields/source arrays and 890 prior source-file records are preserved; version histories only append new annotations.',
            'historical_dependency_graph': 'Every old graph entry is preserved exactly; the new graph is checked against its topological order.',
            'historical_components': 'Every predecessor file is byte-identical at its former path or archived under history/version_0_10; exactly twelve predecessor root files are archived.',
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
            'cross_reviews': 'Independent records cover GI numerical and exact local translation, GII numerical/probability/selection bounds, BC finite normalization and integral/dual/rank transfer, GJ universal infimum and orbit join, GW finite averaging and family transport, and HW actual preselection/rebuilding quantifiers.',
            'pdf': qa,
        },
    }
    filename_map = read_json(OLD / 'component_filename_map.json')
    filename_map['note'] = 'Historical component bytes and source arrays are preserved. Current v0.11 supplies actual family numerics, finite coefficient extension, orbit application and global degree selection/transport. Full joint construction and independent global inputs remain. Superseded root files are archived under history/version_0_10/.'
    filename_map['version_0_11_component_pages'] = page_map
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
    write_json(BASE / 'v0_11/package_validation.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

