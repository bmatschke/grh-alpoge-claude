#!/usr/bin/env python3
"""Package the final visually reviewed v0.8 note and cumulative proof record.

Do not run until root has written and confirmed v0_8/visual_qa.json.
The merged ledger must already exist in output/RH_reconstruction_v0_8.
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
OUT = BASE / "output/RH_reconstruction_v0_8"
OLD = BASE / "output/RH_reconstruction_v0_7"
REPO = BASE / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENTS = {
    "FG": ("frame_geometry", "frame_geometry_section.tex", 8),
    "OR": ("outgoing_realization", "outgoing_realization_section.tex", 8),
    "CP": ("cloud_parameters", "cloud_parameters_section.tex", 8),
    "EA": ("edge_assembly", "edge_assembly_section.tex", 9),
    "TI": ("type_one", "type_one_section.tex", 9),
}
UPDATED_PRIOR_IDS = {
    "SY8", "CL2", "CL3", "CL6", "CL9", "CL10", "CL11", "CL12", "WT9",
    "DT11", "SD8", "CG9", "RK1", "RK2", "RK3", "JR9", "JR10",
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


def main():
    pdf_path = BASE / "output/pdf/RH_readable_reconstruction_v0_8.pdf"
    tex_path = BASE / "output/pdf/RH_readable_reconstruction_v0_8.tex"
    qa_path = BASE / "v0_8/visual_qa.json"
    targets_path = BASE / "v0_8/next_source_targets.json"

    # Every acceptance gate below precedes the first package write.
    require(qa_path.is_file(),
            "Final v0_8/visual_qa.json is unavailable; do not package yet.")
    qa_raw = qa_path.read_bytes()
    qa = json.loads(qa_raw)
    pdf_raw, tex_raw = pdf_path.read_bytes(), tex_path.read_bytes()
    pdf_sha = sha(pdf_raw)
    require(qa.get("all_pages_visually_reviewed") is True,
            "The final QA record does not certify review of every page.")
    require(qa.get("pdf_sha256") == pdf_sha,
            "Final PDF SHA256 does not match v0_8/visual_qa.json.")
    require(qa.get("corrections_required_after_final_render") is False,
            "The final QA record must explicitly require no further correction.")
    require(targets_path.is_file(), "The new v0.8 next-source-target file is absent.")
    targets_raw = targets_path.read_bytes()
    next_doc = json.loads(targets_raw)
    require(str(next_doc.get("version")) == "0.8" and next_doc.get("commit") == PIN,
            "The new next-source targets have the wrong version or commit.")
    target_records = list(range_records(next_doc))
    require(len(target_records) == 16,
            "Expected the final 16 exact local source-target ranges.")
    require(len(next_doc.get("global_branches_unchanged", [])) == 4,
            "Expected the four unchanged global source branches.")

    merged_snapshots = {}
    for name in MERGED_NAMES:
        require((OUT / name).is_file(), f"Missing final merged artifact: {name}")
        merged_snapshots[name] = (OUT / name).read_bytes()
    ledger = json.loads(merged_snapshots["provenance.json"])
    old_ledger = read_json(OLD / "provenance.json")
    require(ledger["commit"] == PIN, "Merged ledger uses the wrong source commit.")
    require(str(ledger["artifact_version"]) == "0.8",
            "Merged ledger is not version 0.8.")
    require(len(old_ledger["claims"]) == 231, "Expected the 231-claim v0.7 baseline.")
    by_id = {claim["id"]: claim for claim in ledger["claims"]}
    old_by_id = {claim["id"]: claim for claim in old_ledger["claims"]}
    require(len(by_id) == len(ledger["claims"]), "Duplicate claim IDs.")
    for cid, old_claim in old_by_id.items():
        require(cid in by_id, f"Earlier claim is missing: {cid}")
        current = by_id[cid]
        for key, value in old_claim.items():
            if key == "version_history":
                require(current.get(key, [])[:len(value)] == value,
                        f"Earlier version history was changed: {cid}")
            else:
                require(current.get(key) == value,
                        f"An earlier claim field was changed: {cid}.{key}")
        require(current["sources"] == old_claim["sources"],
                f"Earlier source array altered: {cid}")
    new_ids = set(by_id) - set(old_by_id)
    expected_new = {
        f"{prefix}{i}"
        for prefix, (_, _, size) in COMPONENTS.items()
        for i in range(1, size + 1)
    }
    require(new_ids == expected_new,
            "The additions must be exactly FG1–8, OR1–8, CP1–8, EA1–9 and TI1–9.")
    require(len(ledger["claims"]) == 273 and len(new_ids) == 42,
            "Expected exactly 273 cumulative claims and 42 v0.8 additions.")
    for cid in UPDATED_PRIOR_IDS:
        require("version_0_8_update" in by_id[cid],
                f"Missing explicit v0.8 local-boundary update: {cid}")
    current_files = {record["path"]: record for record in ledger["source_files"]}
    for record in old_ledger["source_files"]:
        require(current_files.get(record["path"]) == record,
                f"Earlier full-source record altered: {record['path']}")
    local = ledger.get("version_0_8_local_conclusion", {})
    require(local.get("claim") == "EA9" and local.get("cloud_input") == "CP8" and
            local.get("C_lower_bound") == 4129 and
            local.get("cloud_constants") == [10, 54, 1088] and
            local.get("outgoing_threshold") == 100,
            "The merged local conclusion does not match the agreed exact theorem.")
    checked_links, checked_source_files = verify_sources(ledger, target_records)
    count = dict(claims=len(ledger["claims"]), new_claims=len(new_ids),
                 source_links=checked_links, source_files=len(ledger["source_files"]),
                 next_target_ranges=len(target_records),
                 source_files_checked_including_next_targets=checked_source_files)

    # Read the live inclusion-fragment titles, then locate their actual render.
    tex = tex_raw.decode("utf-8")
    headings = {}
    for prefix, (component, filename, _) in COMPONENTS.items():
        fragment = (BASE / "v0_8" / component / filename).read_text(encoding="utf-8")
        match = re.search(r"\\section\{([^{}]+)\}", fragment)
        require(match is not None, f"Missing actual section title: {component}")
        heading = match.group(1)
        require(r"\section{" + heading + "}" in tex,
                f"The assembled TeX lacks the current {prefix} heading.")
        headings[prefix] = heading
    with fitz.open(stream=pdf_raw, filetype="pdf") as pdf:
        pages = len(pdf)
        starts = {}
        for number, page in enumerate(pdf, 1):
            text_key = heading_key(page.get_text())
            for prefix, heading in headings.items():
                if heading_key(heading) in text_key:
                    starts.setdefault(prefix, number)
    require(qa.get("page_count") == pages,
            "QA page count differs from the final PDF.")
    qa_coverage = reviewed_pages(qa, pages)
    require(set(starts) == set(COMPONENTS),
            "Cannot locate all five new component sections in the rendered PDF.")
    ordered_starts = [starts[prefix] for prefix in COMPONENTS]
    require(ordered_starts == sorted(ordered_starts),
            "The detected sections are out of their logical order.")
    # Adjacent logical sections may begin on the same physical page.
    page_map = {
        prefix: dict(component=component, title=headings[prefix],
                     page_start=starts[prefix], fragment=filename)
        for prefix, (component, filename, _) in COMPONENTS.items()
    }

    excluded = {
        "README.txt", *MERGED_NAMES, "continuation_checkpoint.json", "SHA256SUMS",
        "backtrack.py", "component_filename_map.json", "next_source_targets.json",
        "visual_qa.json", "RH_readable_reconstruction_v0_7.pdf",
        "RH_readable_reconstruction_v0_7.tex",
    }
    plan = []
    for source in sorted(OLD.rglob("*")):
        if not source.is_file():
            continue
        rel = source.relative_to(OLD)
        if source.parent == OLD and source.name in excluded:
            # Preserve overwritten metadata and the old main artifact explicitly.
            dest = Path("history/version_0_7") / source.name
            category = "archived_previous_root"
        else:
            dest = rel
            category = "historical"
        plan.append((source, dest, category))
    require((OLD / "next_source_targets.json").is_file(),
            "The previous next-source-target file must be archived.")
    for component, _, _ in COMPONENTS.values():
        for source in sorted((BASE / "v0_8" / component).rglob("*")):
            if source.is_file() and source.suffix in {".tex", ".txt", ".md", ".json", ".py"}:
                rel = Path(component) / source.relative_to(BASE / "v0_8" / component)
                plan.append((source, rel, "new_component"))
    # Include exact v0.8 recipe scripts, including component builders, but no PNGs.
    for source in sorted((BASE / "v0_8").rglob("*.py")):
        if "__pycache__" not in source.parts:
            rel = Path("workflow_v0_8") / source.relative_to(BASE / "v0_8")
            plan.append((source, rel, "workflow"))
    workflow_names = {rel.as_posix() for _, rel, cat in plan if cat == "workflow"}
    for name in ["assemble_note.py", "merge_provenance.py", "package_checkpoint.py"]:
        require("workflow_v0_8/" + name in workflow_names,
                f"Missing v0.8 workflow script: {name}")
    plan += [
        (pdf_path, Path(pdf_path.name), "main"),
        (tex_path, Path(tex_path.name), "main"),
        (qa_path, Path("visual_qa.json"), "qa"),
        (qa_path, Path("workflow_v0_8/visual_qa.json"), "workflow"),
        (targets_path, Path("next_source_targets.json"), "targets"),
        (targets_path, Path("workflow_v0_8/next_source_targets.json"), "workflow"),
    ]
    copy_names = [rel.as_posix() for _, rel, _ in plan]
    require(len(copy_names) == len(set(copy_names)), "Two planned files share a destination.")
    generated_names = {
        *MERGED_NAMES, "README.txt", "continuation_checkpoint.json",
        "backtrack.py", "component_filename_map.json", "SHA256SUMS",
    }
    expected_names = set(copy_names) | generated_names
    existing_names = {
        path.relative_to(OUT).as_posix() for path in OUT.rglob("*") if path.is_file()
    }
    require(existing_names <= expected_names,
            "Unmanaged files are present in the package folder: " +
            ", ".join(sorted(existing_names - expected_names)))

    # Prepare all generated text before the first write.
    backtrack = (OLD / "backtrack.py").read_text(encoding="utf-8")
    old_examples = "for example CG6, LA5, GP5, RS8, or RK3."
    require(backtrack.count(old_examples) == 1,
            "Unexpected predecessor backtrack help text.")
    backtrack = backtrack.replace(old_examples, "for example FG7, OR8, CP8, EA9, or TI9.")
    fields = "'version_0_7_update']:"
    require(backtrack.count(fields) == 1, "Unexpected predecessor backtrack fields.")
    backtrack = backtrack.replace(fields, "'version_0_7_update','version_0_8_update','merged_application','merged_scope_classification','resolved_companion_inputs','merge_scope_note']:")
    filename_map = read_json(OLD / "component_filename_map.json")
    filename_map["note"] = (
        "Historical component bytes and source arrays are preserved. Current local boundaries "
        "are stated by the v0.8 main note and explicit version_0_8_update fields: the full "
        "Type-II ConclusionE is now proved under literal Hyps for C>=4129. Type-I and global "
        "obligations remain. Superseded root files, including the former source targets, are "
        "archived under history/version_0_7/."
    )
    filename_map["version_0_8_component_pages"] = page_map
    previous = read_json(OLD / "continuation_checkpoint.json")
    new_results = [
        "FG1–FG8: literal marked-tile enumeration including the physical wrap remainder; full FramesOK, common marked index and coverage; strict span, L2 endpoint gaps, segment counts and oldest-predecessor separation.",
        "OR1–OR8: generic determinant divisibility over every field, integral descent, all-prefix extraction, exact one-sided degree margin, RestModel and RestPh, and actual outgoing monPh realization; C>=100 suffices for its numerical application.",
        "CP1–CP8: actual signed-chain data with floors, MFH/Num/Size, primitive constrained tests, all denominator and error budgets, uniform word-height bound, and FlatAt/CloudStep with constants 10 and 54.",
        "EA1–EA9: exact K=m+1-r complement, symbol-dimension compatibility, universal field/basis choice, pre-word rank normalization and controlled families on every edge; complete local Type-II ConclusionE under literal Hyps with C>=4129 and cloud tuple (10,54,1088).",
        "TI1–TI9: explicit rank-one block lattices and primitive-test interpretation; gamma degree/leading form, logarithmic integrality and polynomial-matrix averaging; proved conditional transfers with the remaining graded Gram, partner, weighted-transfer and paired-lift premises identified.",
    ]
    remaining = [
        "Complete the separate Type-I construction: restricted graded initial-Gram bounds, compatible integral partners across multiple ties, dimension-weighted segment and digit-class transfer, paired cleaned rank-one lifts, and their uniform numerical supply. TI1–TI5's polynomial/arithmetic mechanism is completed and should be reused.",
        "Global abundance of the literal Type-II orbit and weight hypotheses, with the simultaneous global arithmetic data. The local ConclusionE construction under those hypotheses is completed.",
        *previous["remaining_major_inputs"][2:],
    ]
    precision_additions = [
        "The entire earlier precision-constraint array is preserved below as historical assertions; only its former local Type-II boundary is superseded by the explicit version_0_8_update and precision_supersessions. No global window, metric or prime-selection input is silently discharged.",
        "FG retains the physical remainder nPrime-floor(nPrime/ell)*ell at the cyclic wrap. Its one common marked-tile index works for all r coordinates; the stronger FramesOK span<GPrime and L2 gaps are preserved.",
        "OR proves the determinant lemma over every field by generic singular specialization, not by testing finite-field points. Integral monic division preserves quotients over arbitrary domains.",
        "OR uses only the outgoing upper-degree approximation. Each determinant extraction loses at most one unit at every prefix; the full overlapping task budget is paid before invoking completed IP/SY.",
        "OR RestPh keeps the exact p^cP error. Since w^2=p, after normal-degree scaling it is w^(o+2cP); the ordinary SymbolRealisableAt result alone does not prove the outgoing monPh realization.",
        "CP constructs the actual signed-chain datum, including floor slack, projector choice, Num/Size and MFH. PG's optional zero remainder does not eliminate the retained normal/digit approximation error.",
        "CP's contraction scalar need not be a unit. Its exact divisibility transfer remains beta(U,Lambda T)*(c*b)=p^(kappa+DX), with D1<=54 N k^2 log_p(a).",
        "EA uses K=m+1-r, applies the selected-symbol count to the original span before operator closure, and then uses the word family for tests. Its frame equality F.TT=TT and graph-plane normalization are retained.",
        "EA9 gives the full local Type-II ConclusionE under the literal supplied Hyps for C>=4129, with cloud constants (10,54,1088). It does not prove abundance of those hypotheses or replace the separate Type-I branch.",
        "TI's polynomial gamma identities, logarithmic GamInt with constant 10 and polynomial-matrix averaging are proved. The sharper GamIntC exponent is not asserted.",
        "TI6 retains the actual restricted graded Gram premise. TI7–TI8 are proved transfer implications, whose weighted KeyIneq, compatible partner, density, boundary and paired-lift inputs remain. TI9 records these exact open bridges.",
        "Historical component files remain byte-identical. backtrack.py displays every version update through version_0_8_update; old root metadata and the old next-source-target list are preserved under history/version_0_7/.",
    ]
    old_local_boundary = (
        "The source witnesses C0=1088,Crk=1,Cdeg=10 are now proved in the supplied-data "
        "Conclusion2 setting by SD+CG+LA+GP+RS+RK. This is the complete local rank/basis/"
        "complement/degree theorem; compatibility and existence of the full Type-II data remain separate."
    )
    old_rk_boundary = (
        "RK's theorem is for supplied valid periodic frames and all literal Conclusion2 DVR, degree "
        "and size hypotheses. It does not assert compatible data exist for every Type-II edge, "
        "supply Type I, or discharge any global arithmetic window."
    )
    for text in [old_local_boundary, old_rk_boundary]:
        require(text in previous["precision_constraints"],
                "The expected historical local-boundary constraint was not found.")
    supersessions = [
        dict(previous_version="0.7", historical_statement=old_local_boundary,
             current_statement="The selected-symbol theorem retains its exact supplied-data scope. FG/OR/CP/EA now match all local data and prove Type-II ConclusionE under literal Hyps for C>=4129; global abundance of those hypotheses remains separate.",
             completed_by=["FG7", "OR8", "CP8", "EA9"]),
        dict(previous_version="0.7", historical_statement=old_rk_boundary,
             current_statement="RK alone retains its stated scope. The following local compatibility and edge-assembly step is now proved by FG/OR/CP/EA. The separate Type-I construction and all global arithmetic windows remain.",
             completed_by=["FG7", "OR8", "CP8", "EA9"]),
    ]
    categories = {cat: sum(kind == cat for _, _, kind in plan)
                  for cat in {kind for _, _, kind in plan}}
    checkpoint = {
        "project": previous["project"],
        "artifact_version": "0.8", "date": "2026-11-21", "predecessor_version": "0.7",
        "source_repository": ledger["repository"], "source_commit": ledger["commit"],
        "user_instruction": previous["user_instruction"],
        "main_note_pages": pages,
        "new_section_start_pages": starts,
        "new_section_headings": headings,
        "logical_component_page_map": page_map,
        "status": "Partial human reconstruction: the full local Type-II ConclusionE is proved under literal Hyps for C>=4129; the complete Type-I and global RH/Dirichlet-GRH proof remain unfinished.",
        "new_in_this_version": new_results,
        "retained_prior_results": previous["retained_prior_results"] + previous["new_in_this_version"],
        "retained_prior_results_note": "Earlier entries describe the achievements and scope of their versions. Current obligations and explicit local-boundary supersessions are recorded below.",
        "remaining_major_inputs": remaining,
        "next_targets": [
            next_doc["next_local_priority"],
            "Prove the actual Type-I weighted and paired-lift bridges with their numerical hypotheses, reusing TI's completed polynomial/arithmetic results.",
            "Advance the independent theta/spectral, metric, cohomological-window and simultaneous-prime branches without reopening the completed local Type-II construction.",
        ],
        "next_source_targets_file": "next_source_targets.json",
        "previous_source_targets_file": "history/version_0_7/next_source_targets.json",
        "precision_constraints": previous["precision_constraints"] + precision_additions,
        "precision_supersessions": supersessions,
        **{key: value for key, value in previous.items()
           if key.startswith("version_") and key.endswith("_update")},
        "version_0_8_update": {
            "local_conclusion": local,
            "local_boundary_only": "The former frame/cloud/edge compatibility frontier is completed under literal Hyps. Type-I and global hypotheses remain explicit.",
            "Type_I": next_doc["precision_notes"],
            "historical_source_arrays": "Every prior claim field and source array is retained; only explicit update/history fields are appended.",
            "historical_components": "Every previous component file is copied byte-for-byte; superseded root files are archived.",
        },
        "validation": {
            **count,
            "all_cited_ranges_and_file_hashes_checked": True,
            "all_source_bytes_match_pinned_git_blobs": True,
            "all_prior_claim_ids_preserved": True,
            "all_prior_source_records_preserved_exactly": True,
            "historical_component_files_preserved": categories.get("historical", 0),
            "previous_root_files_archived": categories.get("archived_previous_root", 0),
            "new_component_files_copied": categories.get("new_component", 0),
            "workflow_files_copied": categories.get("workflow", 0),
            "all_reviewed_pages": qa_coverage,
            "full_lean_build_or_kernel_replay": False, "lean_sources_modified": False,
            "cross_reviews": (
                "FG wrap, isolation, endpoints, span and oldest geometry were independently reviewed. "
                "OR1–OR3 and OR4–OR8 received separate reviews of determinant algebra, one-sided "
                "numerics, homogeneous transfer and RestPh/monPh realization. Root and team reviewed "
                "CP/EA compatibility and the Type-I polynomial/integrality/averaging mechanism with "
                "its retained hypotheses. Detailed component review records and the final PDF review "
                "are preserved; no review is represented as a Lean kernel replay."
            ),
            "pdf": qa,
        },
    }
    readme = f"""RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — WORKING VERSION 0.8
21 November 2026

START HERE
RH_readable_reconstruction_v0_8.pdf is the complete {pages}-page main note.
RH_readable_reconstruction_v0_8.tex is self-contained LaTeX source.

The full local Type-II ConclusionE now has a human proof under its literal
orbit, weight and numerical hypotheses, for C>=4129. Its cloud constants
are 10 and 54, and the selected-symbol threshold is 1088.
This remains a partial human reconstruction, not a self-contained proof
of RH or Dirichlet GRH. The GRH scope is all Dirichlet L-functions;
unrestricted automorphic or Dedekind GRH is not asserted.

WHAT THE NEW LOCAL THEOREM INCLUDES
FG constructs the actual periodic frames with every stronger FramesOK
condition. OR supplies the additional outgoing one-sided realization.
CP constructs the actual signed-chain data, primitive tests and all
denominator/error budgets. EA assembles compatible symbols, normalized
ranks, controlled edge families and the exact Type-II ConclusionE.
All these statements retain the literal supplied Hyps. Global abundance
of the required orbits and simultaneous arithmetic choices remains open
in this reconstruction.

The separate rank-one Type-I branch now has explicit block lattices,
gamma degree/leading-form identities, logarithmic integrality and
polynomial-matrix averaging proofs. Its complete construction still needs
restricted graded Gram estimates, compatible partners across multiple
ties, dimension-weighted segment and digit-class transfer, paired cleaned
lifts and their uniform numerical supply.

NEW IN THIS VERSION
* FG1–FG8: full actual frame construction from marked tiles, including
  wrap remainder, strict span, L2 gaps, exact counts and oldest geometry.
* OR1–OR8: determinant divisibility in every characteristic, integral
  overlapping extraction, the one-sided margin with C>=100, exact RestPh,
  and realization of the outgoing monPh family.
* CP1–CP8: actual data, exact floor slack, MFH/Num/Size, primitive cloud
  tests, normalized errors and the constants 10 and 54.
* EA1–EA9: complement dimension, actual symbol compatibility, universal
  cloud application, pre-word rank normalization and every-edge assembly;
  ConclusionE with C>=4129 and cloud tuple (10,54,1088).
* TI1–TI9: explicit Type-I polynomial/arithmetic mechanism and proved
  conditional transfers, with each unresolved application premise named.

New section start pages:
  FG={starts['FG']}, OR={starts['OR']}, CP={starts['CP']},
  EA={starts['EA']}, TI={starts['TI']}.
Logical sections may share a physical start page. The page map is detected
from the exact live TeX headings in the final PDF.
Expanded proofs are in frame_geometry/, outgoing_realization/,
cloud_parameters/, edge_assembly/ and type_one/.

READING ORDER
For the newly completed local theorem, read EA and CP, then FG and OR.
For Type I, read TI independently; it is not supplied by Type II.
For the global route, start with the analytic endpoint, scalar balance
and common-lattice slope comparison. The local sequence is EL, SY/IP,
IW/CB/CL, IN/WT, PG/DT, SD, CG/LA/GP/RS/RK, FG/OR/CP/EA, then JR/LW/LC/SR.
Ordinary RH and fixed-character Dirichlet GRH have separate host/window
sections. Earlier reconstructed proofs remain in the main note.

HISTORY AND EXACT SOURCE BACKTRACKING
Every historical component report and ledger is preserved byte-for-byte.
Their older boundary prose remains historical. Explicit version_0_8_update
fields and the current main note describe which local obligations have
now closed. All earlier mathematical precision constraints are retained;
the checkpoint lists only the precise local-boundary supersessions.
The former root next_source_targets.json is preserved at
history/version_0_7/next_source_targets.json, with the old root metadata
and previous main PDF/TeX. The new root target list directs the next work.

provenance.json: {count['claims']} stable claim IDs, including {count['new_claims']} additions,
with {count['source_links']} exact source links.
provenance.txt: readable claim ledger.
source_index.json: hashes for {count['source_files']} primary source files.
The {count['next_target_ranges']} exact next-target ranges are also validated.
Every earlier claim/source array and full-file record is unchanged.
Every full-file and inclusive-range SHA256 is rechecked; all source bytes
are also compared with the pinned Git object hashes.

Pinned repository:
  https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit:
  {PIN}

Portable read-only lookup, requiring no network:
  python3 backtrack.py --list
  python3 backtrack.py FG7
  python3 backtrack.py OR8
  python3 backtrack.py CP8 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py EA9
  python3 backtrack.py TI9
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

The tool checks full-source hashes before showing excerpts and displays
version updates through version_0_8_update and the explicit merged application,
scope classification, resolved companion inputs and merge-scope note. In
particular EA9 displays its CP8 application beside its historical conditional
status. Its default excerpt limit is
160 lines; --max-lines changes it. The archive omits the enormous source
checkout and build caches. Inclusion fragments, companion notes and
component builders retain their original bytes. workflow_v0_8/ records
the assembly, merger, packaging and builder scripts from this workspace;
these record the original workflow rather than serving as portable build
tools for a source checkout at an arbitrary path. backtrack.py is portable.

PRECISION THAT MATTERS
The frame enumeration retains the incomplete-period remainder and the
stronger span/L2 conditions. OR's generic determinant proof uses no
finite-field point-count assertion; the quotient remains integral.
The outgoing degree assumption is one-sided. The error is p^cP=w^(2cP),
and no ordinary-symbol theorem is silently substituted for that proof.
CP retains floor slack and normal/digit approximation error. The
contraction scalar may be a nonunit; the exact divisibility transfer is
preserved. EA counts the initial span before operator closure and uses
K=m+1-r. Its local hypothesis does not assert global orbit abundance.

All prior precision statements remain in the checkpoint, including
prime-field-only Frobenius in CG, the actual periodic wrap x-nPrime in
LA, AdmLL versus BOK and the retained auxiliary monomial in GP,
the original integral/metric and cohomological limitations, and the
fixed Dirichlet-GRH scope.

NEXT LOCAL WORK
The new next_source_targets.json lists the exact Type-I restricted
initial-Gram, compatible-partner, weighted-transfer and paired-lift
source targets. TI6 remains conditional on its actual graded Gram
premise. TI7–TI8 are proved implications whose actual weighted inequality,
density, boundary and construction inputs remain. The sharper GamIntC
exponent is not claimed. Reuse the completed Type-II theorem and the
proved Type-I gamma/integrality/averaging mechanism.

GLOBAL WORK STILL REQUIRED
Actual theta/common-image identities and chain norms; spectral and
arithmetic kernel comparisons; dimension/metric/discarded-target bounds;
LinkN/LinkV congruence denominators and ordinary/fixed-character
cohomological windows; simultaneous prime selection and the uniform
centered-prime-sum estimate. These branches are unchanged by the new
local theorem.

VERIFICATION AND CONTINUATION
No Lean source was modified; no full Lean build or independent kernel
replay was run. The shorter human arguments are not asserted formalized
and replayed in Lean. Source checks and mathematical reviews are recorded
as such. visual_qa.json certifies all {pages} final pages and the exact PDF
SHA256. The package script rejects a mismatch or incomplete review.

continuation_checkpoint.json records the completed claims, current
assumptions, explicit supersessions, reviews and next targets.
SHA256SUMS covers every bundled file except itself. ZIP membership,
every CRC and every archived byte are checked against the completed
folder. The previous component files and archived root files are
compared byte-for-byte with the v0.7 package.
"""

    # Only after all preflight gates have passed do we write the package.
    for source, rel, _ in plan:
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        require(target.read_bytes() == source.read_bytes(),
                f"Copied bytes differ: {rel}")
    (OUT / "backtrack.py").write_text(backtrack, encoding="utf-8")
    write_json(OUT / "component_filename_map.json", filename_map)
    write_json(OUT / "continuation_checkpoint.json", checkpoint)
    (OUT / "README.txt").write_text(readme, encoding="utf-8")

    # Reject any authoritative change while packaging.
    require(pdf_path.read_bytes() == pdf_raw, "The final PDF changed during packaging.")
    require(tex_path.read_bytes() == tex_raw, "The final TeX changed during packaging.")
    require(qa_path.read_bytes() == qa_raw, "The final QA record changed during packaging.")
    require(targets_path.read_bytes() == targets_raw,
            "The new source-target file changed during packaging.")
    for name, raw in merged_snapshots.items():
        require((OUT / name).read_bytes() == raw,
                f"The authoritative merged artifact changed during packaging: {name}")
    for source, rel, category in plan:
        require((OUT / rel).read_bytes() == source.read_bytes(),
                f"Final copy mismatch ({category}): {rel}")
    require(sha((OUT / pdf_path.name).read_bytes()) == pdf_sha,
            "Packaged PDF differs from the reviewed PDF.")

    entries = [
        path for path in sorted(OUT.rglob("*"))
        if path.is_file() and path != OUT / "SHA256SUMS"
    ]
    sums = "".join(sha(path.read_bytes()) + "  " +
                   path.relative_to(OUT).as_posix() + "\n" for path in entries)
    (OUT / "SHA256SUMS").write_text(sums, encoding="utf-8")
    for line in sums.splitlines():
        digest, name = line.split("  ", 1)
        require(sha((OUT / name).read_bytes()) == digest,
                f"Package checksum mismatch: {name}")
    package_files = {path.relative_to(OUT).as_posix(): path
                     for path in OUT.rglob("*") if path.is_file()}
    require(set(package_files) == expected_names,
            "Final folder differs from the planned exact package inventory.")
    zip_path = BASE / "output/RH_reconstruction_v0_8.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for rel in sorted(package_files):
            archive.write(package_files[rel], OUT.name + "/" + rel)
    with zipfile.ZipFile(zip_path) as archive:
        require(archive.testzip() is None, "ZIP CRC verification failed.")
        infos = archive.infolist()
        names = {OUT.name + "/" + rel for rel in package_files}
        require(len(infos) == len(names) and
                {info.filename for info in infos} == names,
                "ZIP membership differs from the completed package folder.")
        for info in infos:
            rel = Path(info.filename).relative_to(OUT.name).as_posix()
            require(archive.read(info.filename) == package_files[rel].read_bytes(),
                    f"ZIP byte mismatch: {rel}")
    print(json.dumps({
        "pages": pages, "new_section_start_pages": starts,
        "pdf_sha256": pdf_sha, **count,
        "zip_files": len(infos), "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": sha(zip_path.read_bytes()),
        "sha256sums_verified": True, "archive_crc_verified": True,
        "archive_bytes_verified": True,
        "historical_files_preserved": categories.get("historical", 0),
        "previous_root_files_archived": categories.get("archived_previous_root", 0),
        "new_component_files_copied": categories.get("new_component", 0),
        "workflow_files_copied": categories.get("workflow", 0),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
