#!/usr/bin/env python3
"""Package the final visually reviewed v0.9 note and cumulative proof record.

Do not run until root has written and confirmed v0_9/visual_qa.json.
The merged ledger must already exist in output/RH_reconstruction_v0_9.
This script never edits the source checkout, old package, main TeX/PDF,
component originals, or merged ledgers. It validates and copies them.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import unicodedata
import zipfile

import fitz

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "output/RH_reconstruction_v0_9"
OLD = BASE / "output/RH_reconstruction_v0_8"
REPO = BASE / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENTS = {
    "GG": ("graded_gram", "graded_gram_section.tex", [f"GG{i}" for i in range(1,9)]),
    "TP": ("tie_partners", "main.tex", [f"TP{i}" for i in range(1,12)]),
    "SW": ("segment_weighted", "segment_weighted_section.tex", [f"SW{i}" for i in range(1,12)]),
    "SW12": ("segment_numerics", "main.tex", ["SW12"]),
    "RL": ("paired_lifts", "paired_lifts_section.tex", [f"RL{i}" for i in range(1,12)]),
}
UPDATED_PRIOR_IDS = {"TI2","TI4","TI6","TI7","TI8","TI9","JR10"}

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


def main():
    pdf_path = BASE / "output/pdf/RH_readable_reconstruction_v0_9.pdf"
    tex_path = pdf_path.with_suffix(".tex")
    qa_path = BASE / "v0_9/visual_qa.json"
    targets_path = BASE / "v0_9/next_source_targets.json"
    qa_raw, targets_raw = qa_path.read_bytes(), targets_path.read_bytes()
    qa, next_doc = json.loads(qa_raw), json.loads(targets_raw)
    pdf_raw, tex_raw = pdf_path.read_bytes(), tex_path.read_bytes()
    pdf_sha = sha(pdf_raw)
    require(qa.get("all_pages_visually_reviewed") is True, "Every final PDF page must be visually reviewed.")
    require(qa.get("pdf_sha256") == pdf_sha, "QA refers to another PDF.")
    require(qa.get("corrections_required_after_final_render") is False, "Final PDF still requires correction.")
    require(str(next_doc.get("version")) == "0.9" and next_doc.get("commit") == PIN, "Incorrect next-source target version.")
    target_records = list(range_records(next_doc))
    require(15 <= len(target_records) <= 30, "Expected a focused set of exact next-source targets.")
    old_next = read_json(OLD / "next_source_targets.json")
    require(next_doc["global_branches_unchanged"] == old_next["global_branches_unchanged"], "Global source branches changed.")

    merged_snapshots = {name:(OUT/name).read_bytes() for name in MERGED_NAMES}
    ledger = json.loads(merged_snapshots["provenance.json"])
    old_ledger = read_json(OLD / "provenance.json")
    require(ledger["commit"] == PIN and ledger["artifact_version"] == "0.9", "Wrong merged ledger.")
    require(len(old_ledger["claims"]) == 273, "Wrong predecessor claim count.")
    by_id = {c["id"]:c for c in ledger["claims"]}
    old_by_id = {c["id"]:c for c in old_ledger["claims"]}
    require(len(by_id) == len(ledger["claims"]) == 315, "Wrong cumulative claim count or duplicate IDs.")
    for cid, prior in old_by_id.items():
        current = by_id[cid]
        for key,value in prior.items():
            if key == "version_history":
                require(current.get(key,[])[:len(value)] == value, f"Historical status history changed: {cid}")
            else:
                require(current[key] == value, f"Historical field changed: {cid}.{key}")
        require(current["sources"] == prior["sources"], f"Historical source array changed: {cid}")
    expected_ids = {cid for _,_,ids in COMPONENTS.values() for cid in ids}
    require(set(by_id)-set(old_by_id) == expected_ids and len(expected_ids) == 42, "New IDs must be GG8+TP11+SW12+RL11.")
    for cid in UPDATED_PRIOR_IDS:
        require("version_0_9_update" in by_id[cid], f"Missing current boundary: {cid}")
    current_files = {r["path"]:r for r in ledger["source_files"]}
    for record in old_ledger["source_files"]:
        require(current_files[record["path"]] == record, f"Historical source record changed: {record['path']}")
    require(ledger["version_0_8_local_conclusion"] == old_ledger["version_0_8_local_conclusion"], "Completed Type-II conclusion changed.")
    checked_links, checked_source_files = verify_sources(ledger, target_records)

    headings = {}
    for label,(component,filename,_) in COMPONENTS.items():
        fragment = (BASE/"v0_9"/component/filename).read_text()
        match = re.search(r"\\(?:sub)?section\{([^{}]+)\}", fragment)
        require(match is not None, f"Missing section heading: {component}")
        heading = match.group(1)
        require(heading in tex_raw.decode(), f"Current section missing from main: {label}")
        headings[label] = heading
    with fitz.open(stream=pdf_raw, filetype="pdf") as pdf:
        pages, starts = len(pdf), {}
        for number,page in enumerate(pdf,1):
            key = heading_key(page.get_text())
            for label,heading in headings.items():
                if heading_key(heading) in key:
                    starts.setdefault(label,number)
    require(set(starts) == set(COMPONENTS), "Could not locate all new sections in final PDF.")
    require(list(starts.values()) == sorted(starts.values()), "New section page order is inconsistent.")
    require(qa["page_count"] == pages, "PDF/QA page count mismatch.")
    coverage = reviewed_pages(qa,pages)
    page_map = {label:{"component":component,"title":headings[label],"page_start":starts[label],"fragment":filename}
                for label,(component,filename,_) in COMPONENTS.items()}

    excluded = {"README.txt",*MERGED_NAMES,"continuation_checkpoint.json","SHA256SUMS",
                "backtrack.py","component_filename_map.json","next_source_targets.json","visual_qa.json",
                "RH_readable_reconstruction_v0_8.pdf","RH_readable_reconstruction_v0_8.tex"}
    plan=[]
    for source in sorted(OLD.rglob("*")):
        if not source.is_file():
            continue
        rel=source.relative_to(OLD)
        if source.parent == OLD and source.name in excluded:
            dest=Path("history/version_0_8")/source.name
            category="archived_previous_root"
        else:
            dest=rel
            category="historical"
        plan.append((source,dest,category))
    for component,_,_ in COMPONENTS.values():
        for source in sorted((BASE/"v0_9"/component).rglob("*")):
            if source.is_file() and source.suffix in {".tex",".txt",".json",".py"} and source.name not in {"source_paths.json","declaration_catalog.json"}:
                plan.append((source,Path(component)/source.relative_to(BASE/"v0_9"/component),"new_component"))
    for source in sorted((BASE/"v0_9").rglob("*.py")):
        if "__pycache__" not in source.parts:
            plan.append((source,Path("workflow_v0_9")/source.relative_to(BASE/"v0_9"),"workflow"))
    for source in sorted((BASE/"v0_9/reviews").glob("*.txt")):
        plan.append((source,Path("reviews_v0_9")/source.name,"review"))
    plan += [(pdf_path,Path(pdf_path.name),"main"),(tex_path,Path(tex_path.name),"main"),
             (qa_path,Path("visual_qa.json"),"qa"),(qa_path,Path("workflow_v0_9/visual_qa.json"),"workflow"),
             (targets_path,Path("next_source_targets.json"),"targets"),
             (targets_path,Path("workflow_v0_9/next_source_targets.json"),"workflow")]
    names=[rel.as_posix() for _,rel,_ in plan]
    require(len(names) == len(set(names)),"Duplicate package destination.")
    generated={*MERGED_NAMES,"README.txt","continuation_checkpoint.json","backtrack.py","component_filename_map.json","SHA256SUMS"}
    expected=set(names)|generated
    existing={p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()}
    require(existing<=expected,"Unmanaged files in final package: "+", ".join(sorted(existing-expected)))

    backtrack=(OLD/"backtrack.py").read_text()
    backtrack=backtrack.replace("for example FG7, OR8, CP8, EA9, or TI9.","for example GG7, TP11, SW8, SW12, or RL11.")
    require(backtrack.count("'version_0_8_update'")==1,"Unexpected backtrack version fields.")
    backtrack=backtrack.replace("'version_0_8_update'","'version_0_8_update','version_0_9_update','proof_location','expanded_notes','depends_on','dependencies'")
    original="    return raw.decode().splitlines()"
    require(backtrack.count(original)==1,"Unexpected source lookup function.")
    backtrack=backtrack.replace(original,"""    if 'range_sha256' in record:
        first,last=record['line_start'],record['line_end']
        excerpt=b''.join(raw.splitlines(keepends=True)[first-1:last])
        if hashlib.sha256(excerpt).hexdigest()!=record['range_sha256']:
            raise ValueError(f'Inclusive source-range hash mismatch: {path}:{first}-{last}')
    return raw.decode().splitlines()""")

    previous=read_json(OLD/"continuation_checkpoint.json")
    results=[
        "GG1–GG8: actual graded coefficient-image lattice, integral auxiliary action, highest generation, order/saturation and exact Gram determinant constant; no new local integral representation premise.",
        "TP1–TP11: sharper exact GamIntC, explicit single-tie partial inverses, simultaneous compatible partners, actual multiplicities and endpoint injection; exact TheoremMV7 with CM=1.",
        "SW1–SW11: actual level directness/saturation/base change, harmonic change and Fock normalization, ramified GoodSub, terminal Gram window, dimension-weighted summation with coarse rank explicit, depth and coarse-degree gap.",
        "SW12: literal Std gives BLk(0), oPlus<=147a/250<=aPlus and the exact total order<=t0 for Ct>=30.",
        "RL1–RL11: factorial correction with explicit scalar bound, actual Frobenius columns/keys/localizer, derived raw numerical interfaces, quotient/remainder reblocking, finite cleanup and actual source/dual CCe pairing at floor(t0).",
    ]
    remaining=[
        "Actual Type-I coarse rank-on-digits upper/lower estimates, harmonic-model dimension identification and KeyIneq application, full uniform numerical package, final height comparison and exceptional-function application. GG/TP and RL are completed within their explicit scopes; SW8 retains coarse rank.",
        *previous["remaining_major_inputs"][1:],
    ]
    additions=[
        "All prior precision constraints below are preserved as historical records. Current v0.9 scope and exact supersessions govern the old Type-I boundary; no global arithmetic or cohomological input is silently discharged.",
        "GG uses the actual restriction-image lattice. Its auxiliary divided-power flow is integral; the reduced projector begins with the cost-free z-degree-zero projection. Its determinant exponent is (K+3)e1+4D4 and the segment constant is (s+4)r^2ell.",
        "TP2 proves exact GamIntC; TP11 uses CM=1. Endpoint continuation dimensions and their multiplicities are retained, and partial inverses are composed in order without assuming they commute.",
        "SW1 base change uses words in each prefix's own Lie generators separately. SW2 retains the exact harmonic factorial normalization, and SW3 keeps the additive monomial-factorial valuation and ramified w^q scaling.",
        "SW5 multiplies the actual terminal form by an integral binomial scalar and reuses TI5. SW8 is conditional on the literal upper coarse-rank estimate; its finite summation alone does not prove dimension density.",
        "SW10 and SW12 consume literal Std, including the odd-power excluded band. SW12 keeps signed caps, proves oPlus<=147a/250, and preserves the exact min terms in total order<=t0.",
        "RL uses exact physical factorials, including fixed factorials outside the auxiliary-variable image. It constructs actual CCe/CCe' vectors with scalar valuation<=4kappa0 and height floor(t0). The beHH convention is multiplicative p^AHH.",
        "RL derives ColNum, Room and NumCore from Std. Its cleanup is finite; w^h cancels the added correction height h. SSg is an O-span of generators of bounded actual order, so raw terms use each generator's actual order before comparing with the upper bound.",
        "Literal local standard/admissible data are inputs, not an assertion that all global choices exist. The complete Type-I Conclusion2 and global arithmetic-window theorem remain unproved in this human text.",
    ]
    supersessions=list(previous.get("precision_supersessions",[]))
    for historical in previous["precision_constraints"]:
        if "The sharper GamIntC exponent is not asserted" in historical or historical.startswith("TI6 retains") or historical.startswith("TI's polynomial"):
            supersessions.append({"previous_version":"0.8","historical_statement":historical,
                "current_statement":"GG supplies actual graded Gram; TP supplies sharp GamIntC and exact simultaneous mean; RL supplies actual cleaned lifts under literal Std. SW8's rank input and full numerical/global supply remain explicit.",
                "completed_by":["GG7","GG8","TP2","TP11","RL11"]})
    categories={cat:sum(kind==cat for _,_,kind in plan) for cat in {kind for _,_,kind in plan}}
    count={"claims":len(by_id),"new_claims":42,"source_links":checked_links,"source_files":len(current_files),
           "next_target_ranges":len(target_records),"source_files_checked_including_next_targets":checked_source_files}
    checkpoint={
        "project":previous["project"],"artifact_version":"0.9","date":"2026-11-21","predecessor_version":"0.8",
        "source_repository":ledger["repository"],"source_commit":PIN,"user_instruction":previous["user_instruction"],
        "main_note_pages":pages,"new_section_start_pages":starts,"new_section_headings":headings,"logical_component_page_map":page_map,
        "status":"Partial human reconstruction. Local Type II is complete under literal hypotheses. Actual Type-I Gram/partner/form/lift mechanisms are reconstructed; density, full numerical supply and global RH/Dirichlet-GRH inputs remain.",
        "new_in_this_version":results,"retained_prior_results":previous["retained_prior_results"]+previous["new_in_this_version"],
        "retained_prior_results_note":"Earlier entries describe their versions; current boundaries are the v0.9 update and remaining_major_inputs.",
        "remaining_major_inputs":remaining,"next_targets":[next_doc["next_local_priority"],
            "Match harmonic-model dimensions, uniform Std/admissible data and the exact shifted-height comparison before applying TI7–TI8.",
            "Advance the unchanged independent global branches without reopening completed local Type-II or Type-I mechanisms."],
        "next_source_targets_file":"next_source_targets.json","previous_source_targets_file":"history/version_0_8/next_source_targets.json",
        "precision_constraints":previous["precision_constraints"]+additions,"precision_supersessions":supersessions,
        **{key:value for key,value in previous.items() if key.startswith("version_") and key.endswith("_update")},
        "version_0_9_update":{"local_conclusions":ledger["version_0_9_local_conclusions"],
            "historical_source_arrays":"All 273 previous claim/source arrays and 598 previous source-file records are preserved.",
            "historical_components":"Previous component bytes are preserved; superseded root files are archived under history/version_0_8."},
        "validation":{**count,"all_cited_ranges_and_file_hashes_checked":True,"all_source_bytes_match_pinned_git_blobs":True,
            "all_prior_claim_ids_preserved":True,"all_prior_source_records_preserved_exactly":True,
            "historical_component_files_preserved":categories.get("historical",0),"previous_root_files_archived":categories.get("archived_previous_root",0),
            "new_component_files_copied":categories.get("new_component",0),"all_reviewed_pages":coverage,
            "full_lean_build_or_kernel_replay":False,"lean_sources_modified":False,
            "cross_reviews":"Independent mathematical review covered GG auxiliary action/image lifting and final exponent, TP sharp integrality and continuation injection, SW1–SW5 harmonic/ramified/window arguments, all SW12 numerics, and RL factorial/reblocking/cleanup/source-dual transport. Root reviewed remaining numerical and weighted-sum steps. Scoped records are included.",
            "pdf":qa},
    }
    filename_map=read_json(OLD/"component_filename_map.json")
    filename_map["note"]="Historical component bytes and source arrays are preserved. Read the current main and version_0_9_update for the narrowed Type-I boundary. Superseded root files are archived under history/version_0_8/."
    filename_map["version_0_9_component_pages"]=page_map
    readme=f"""RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.9
21 November 2026

START HERE
RH_readable_reconstruction_v0_9.pdf is the cumulative {pages}-page main note.
RH_readable_reconstruction_v0_9.tex is its self-contained LaTeX source.

This is a partial human reconstruction, not a self-contained RH or GRH
proof. GRH here concerns Dirichlet L-functions. It does not assert all
automorphic or Dedekind GRH. The completed local Type-II theorem from
v0.8 remains unchanged under its literal hypotheses, with C>=4129.

WHAT IS NEW
GG: the actual graded Gram lattice, its integral image lifting and exact
determinant bound. The proof uses an explicit integral auxiliary action
and does not import integral semisimplicity as a missing premise.
TP: sharper exact gamma integrality, compatible integral partners for
all ties, continuation multiplicities and their endpoint injection.
The source's literal TheoremMV7 is proved with CM=1.
SW: actual level saturation, an explicit harmonic change of basis,
its exact Fock normalization, ramified good block lattices, and a
terminal-window proof reusing TI5. The finite weighted sum retains the
actual coarse rank inequality rather than assuming density follows.
SW12: literal Std supplies kept-block legality, oPlus<=147a/250<=aPlus,
and total order<=t0 for Ct>=30.
RL: actual paired lifts into CCe and CCe', at height floor(t0), with
scalar valuation<=4kappa0. The factorial correction, raw generators,
reblocking and finite cleanup are explicit. ColNum, Room and NumCore
are derived from Std. The cleanup has no accumulated height penalty.

The new section starts are:
  GG {starts['GG']}, TP {starts['TP']}, SW {starts['SW']},
  SW12 {starts['SW12']}, RL {starts['RL']}.
Some sections share a physical page. The starts are detected in the
final rendered PDF from the exact live section titles.

READING ORDER
For this iteration's endpoint, read RL and its closing scope paragraph,
then GG, TP and SW. TI3–TI5 are the earlier polynomial mechanism.
The expanded reports are in graded_gram/, tie_partners/,
segment_weighted/, segment_numerics/ and paired_lifts/.
For the global implication, begin with the analytic endpoint, scalar
balance and frame/slope sections. Ordinary RH and the general fixed
Dirichlet-character case have separate host/window sections.

REMAINING LOCAL WORK
Prove the upper and lower coarse rank-on-digits bounds. The upper bound
supplies SW8.1; the lower bound supplies retained mass for Type-I density.
Then identify the actual harmonic dimensions and KeyIneq interface,
supply the full numerical parameter package with its quantifier order,
and compare the constructed t0 height with the final shifted tI bound.
Only after those inputs match may TI7–TI8 be used for the full Type-I
exceptional-function result. The new next_source_targets.json provides
{len(target_records)} exact declaration ranges for that work.

The global theta/spectral, metric, cohomological-window and simultaneous
prime-selection branches remain as stated in the main note. A proof
under literal local Std is not a proof that all global choices exist.

PROVENANCE AND BACKTRACKING
provenance.json has {count['claims']} stable claims, {count['source_links']}
exact source links and {count['source_files']} primary source files.
provenance.txt is the readable ledger; source_index.json indexes files.
All earlier claim fields/source arrays and source-file records remain
verbatim. Current version_0_9_update fields state which old inputs are
now discharged. Older component reports retain their historical scope.
Superseded root files, including the previous PDF/TeX and target list,
are archived under history/version_0_8/.

Pinned repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: {PIN}

Portable read-only lookup:
  python3 backtrack.py --list
  python3 backtrack.py GG7
  python3 backtrack.py TP11
  python3 backtrack.py SW8
  python3 backtrack.py RL11 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py TI9
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

With --repo, source-file SHA256 is checked before any excerpt is shown;
the selected inclusive-range SHA256 is checked as well. Default excerpts
are capped at160 lines; --max-lines changes that. The tool displays
version updates, exact proof locations and dependencies. No network is
needed if the pinned source is available locally.

The archive omits the huge source checkout and build caches. The
workflow_v0_9/ scripts record this workspace's assembly and checks;
backtrack.py is the portable reader utility. Expanded reports contain
longer proofs and source correspondence, not silently additional axioms.

PRECISION AND REVIEW
GG includes a z-degree-zero projection before its reduced highest
projector. SW1 treats each prefix kernel separately. SW3 retains the
additive factorial bound and the ramified w^q scaling. TP's multiplicity
weights are not dropped, and its partial inverses need not commute.
RL keeps fixed physical factorials and the multiplicative beHH=p^AHH
normalization. Its SSg is the span of generators of bounded actual
order; cleanup uses each generator's actual order, then the common bound.
The odd-power excluded band is an explicit Std hypothesis.

The mathematical peer-review records are in reviews_v0_9/. The main PDF
has been rendered and every page visually reviewed. No Lean source was
modified and no full Lean compilation or independent kernel replay was
run for this human reconstruction. Hash checks and mathematical reviews
are not presented as such a replay.

CONTINUATION AND INTEGRITY
continuation_checkpoint.json preserves earlier results and precision
constraints, records exact supersessions, and names the current inputs.
visual_qa.json identifies the exact reviewed PDF by SHA256.
SHA256SUMS covers every bundled file except itself. ZIP membership,
each CRC and every archived byte are checked against the final folder.
Every predecessor file is preserved either at its old component path
or in history/version_0_8/.
"""

    # All scope, source, preservation and review checks precede final writes.
    for source,rel,_ in plan:
        target=OUT/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        require(target.read_bytes()==source.read_bytes(),f"Copy mismatch: {rel}")
    (OUT/"backtrack.py").write_text(backtrack)
    write_json(OUT/"component_filename_map.json",filename_map)
    write_json(OUT/"continuation_checkpoint.json",checkpoint)
    (OUT/"README.txt").write_text(readme)
    for path,raw in [(pdf_path,pdf_raw),(tex_path,tex_raw),(qa_path,qa_raw),(targets_path,targets_raw)]:
        require(path.read_bytes()==raw,f"Input changed during packaging: {path}")
    for name,raw in merged_snapshots.items():
        require((OUT/name).read_bytes()==raw,f"Authoritative ledger changed: {name}")
    for source,rel,category in plan:
        require((OUT/rel).read_bytes()==source.read_bytes(),f"Final copy mismatch ({category}): {rel}")

    entries=[p for p in sorted(OUT.rglob("*")) if p.is_file() and p!=OUT/"SHA256SUMS"]
    (OUT/"SHA256SUMS").write_text("".join(sha(p.read_bytes())+"  "+p.relative_to(OUT).as_posix()+"\n" for p in entries))
    entries.append(OUT/"SHA256SUMS")
    zip_path=OUT.with_suffix(".zip")
    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(entries):
            archive.write(path,arcname=path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(zip_path) as archive:
        require(archive.testzip() is None,"ZIP CRC failure.")
        require(set(archive.namelist())=={p.relative_to(OUT).as_posix() for p in entries},"ZIP membership mismatch.")
        for path in entries:
            require(archive.read(path.relative_to(OUT).as_posix())==path.read_bytes(),f"ZIP byte mismatch: {path}")
    receipt={**count,"pdf_pages":pages,"new_section_start_pages":starts,"pdf_sha256":pdf_sha,
             "zip_sha256":sha(zip_path.read_bytes()),"zip_bytes":zip_path.stat().st_size,"zip_members":len(entries),
             "copied_file_categories":categories,"zip_crc_and_all_bytes_verified":True,
             "all_predecessor_files_preserved":True,"all_pages_visually_reviewed":True}
    write_json(BASE/"v0_9/package_validation.json",receipt)
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()


