#!/usr/bin/env python3
"""Bind the independently authored v0.47 semantic-scope review to final bytes.

The findings are the reviewer's mathematical and editorial judgments.  These
assertions guard the final inventory, original contracts and file bindings;
they do not replace the separate proof reviews or integration audit.
Run only after the final readers, progress report and TeX report were read.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT.parent / "formal_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path, scope):
    return {"path": path, "sha256": digest(ROOT / path), "review_scope": scope}


cfg = read("increment_v0_47.json")
stats = read("integration_stats_v0_47.json")
prior_map = read("dependency_audit_v0_46/obligation_map.json")
now_map = read("dependency_audit_v0_47/obligation_map.json")
prior_nodes = {n["id"]: n for n in prior_map["nodes"]}
now_nodes = {n["id"]: n for n in now_map["nodes"]}
prior_open = {n["id"]: n for n in read("dependency_audit_v0_46/remaining_leaf_register.json")["records"]}
now_open = {n["id"]: n for n in read("dependency_audit_v0_47/remaining_leaf_register.json")["records"]}
closed = {"RIG_II", "TASK_INP_Z_ASSEMBLY"}
qualified = {"DESIGN_CHOICES_COMMON", "BASE_THETA_RATIONAL_TESTS",
             "GLOBAL_RETAINED_DEFECT", "GLOBAL_LOCAL_GAIN", "TASK_ONE_CHAR_PROOF"}
assert prior_nodes.keys() == now_nodes.keys()
assert set(prior_open) - set(now_open) == closed
assert not (set(now_open) - set(prior_open))
assert len(now_nodes) == 121
assert sum(len(n["requires"]) for n in now_nodes.values()) == 161
assert all(prior_nodes[k]["requires"] == now_nodes[k]["requires"] for k in now_nodes)
for key in now_nodes:
    for field in ["category", "kind", "status", "gate"]:
        if key not in closed:
            assert prior_nodes[key].get(field) == now_nodes[key].get(field), (key, field)
    if key in qualified:
        assert now_nodes[key]["contract"].startswith(prior_nodes[key]["contract"])
    else:
        assert now_nodes[key].get("contract") == prior_nodes[key].get("contract")
assert prior_nodes["RIG_II"]["category"] == "C"
assert prior_nodes["TASK_INP_Z_ASSEMBLY"]["category"] == "B"
assert collections.Counter(n["category"] for n in now_open.values()) == {"C": 19, "B": 7}
assert stats == {
    "new_claims": 83, "cumulative_claims": 2851,
    "selected_nodes": 121, "selected_edges": 161,
    "open_count": 26, "open_categories": {"C": 19, "B": 7},
    "shared_open": 19, "extra_grh_open": 7,
    "new_source_files_checked": 148, "new_unique_source_ranges_checked": 207,
}
assert set(cfg["closed_selected_leaves"]) == closed
audit_text = (ROOT / "RH_dependency_audit_v0_47.txt").read_text()
assert all(n["contract"] in audit_text for n in now_open.values())

provenance = read("provenance.json")
checkpoint = read("continuation_checkpoint.json")
targets = read("next_source_targets.json")
assert provenance["scope"] == checkpoint["status"] == targets["current_status_v0_47"] == cfg["status"]
assert provenance["version_0_47_local_conclusions"] == checkpoint["new_in_this_version"] == cfg["local_conclusions"]
assert provenance["component_input_boundaries_v0_47"] == checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"]
assert checkpoint["next_targets"] == targets["next_local_priority"] == cfg["next_targets"]
for key, value in checkpoint["current_dependency_audit"].items():
    if key not in {"artifact_version", "scope"}:
        assert value.startswith("dependency_audit_v0_47/") and (ROOT / value).exists()

new_claims = []
for comp in cfg["components"]:
    new_claims.extend(read(comp + "/provenance.json")["claims"])
assert len(new_claims) == 83
assert collections.Counter(c["classification"] for c in new_claims) == {"A": 4, "B": 79}
assert {c["id"] for c in new_claims if c["classification"] == "A"} == {"KTR2", "KTR9", "RFD1", "ASG3"}

tex = read("tex_validation.json")
assert tex["artifact_version"] == "0.47"
expected_reader_hashes = {
    "RH_new_proofs_v0_47.tex": "7acdf66a11f0e6184e697dcdc58ae5c1df09fb5e6dfa8cea231b4d0a5b6b0ac2",
    "RH_readable_reconstruction_v0_47.tex": "56d7985fcd5079e9b4367d8c956a9cc0d2fea015fc739f565cc54ffd616c4da1",
    "RH_reconstruction_progress_v0_47.txt": "1e1afda9f007c7588edb46d5c4e74834504a56d1f09f86d15e023b17e02311b7",
    "README.txt": "2b0235247ae161001537e05de7f79f8204a9b7bbfb4d8dffada310ce91c2d256",
    "write_progress_v0_47.py": "e6a8ce88f2484fa83c46475f4d09ce6826c4faa9eb9b3cd6c001bc085d9c147e",
}
assert all(digest(ROOT / p) == h for p, h in expected_reader_hashes.items())
for item in tex["documents"]:
    assert digest(ROOT / item["tex_filename"]) == item["tex_sha256"]
    assert item["syntax_compile_succeeded"]
    assert not item["undefined_references_or_citations"]
    assert item["missing_character_warnings"] == 0
    assert not item["pdf_generated"] and not item["pdf_visual_review_performed"]
assert [d["passes"] for d in tex["documents"]] == [2, 3]
assert [d["overfull_box_warnings"] for d in tex["documents"]] == [0, 53]

reviewed = []
scope_scripts = "Current semantic scope, choice order, retained antecedents, selected closure and generated-output narrative; exhaustive preservation mechanics belong to the separate integration audit."
for path in ["increment_v0_47.json", "configure_v0_47.py", "assemble_v0_47.py", "integrate_v0_47.py", "write_progress_v0_47.py", "v0_47_frontmatter.tex", "v0_47_audit_intro.tex"]:
    reviewed.append(binding(path, scope_scripts))
for path, scope in [
    ("provenance.json", "Current scope, current_boundary_authority, version_0_47_local_conclusions, component_input_boundaries_v0_47 and inventory; not a rereading of every historical nested record."),
    ("continuation_checkpoint.json", "Current status, new_in_this_version, remaining_major_inputs, next_targets, current_dependency_audit, current_deliverable and version_0_47_update."),
    ("next_source_targets.json", "Current v0.47 status, precision notes, selected-frontier files and next_local_priority; the earlier version-specific statuses are historical."),
]:
    reviewed.append(binding(path, scope))
for version, names in [
    ("0_46", ["obligation_map.json", "remaining_leaf_register.json"]),
    ("0_47", ["obligation_map.json", "remaining_leaf_register.json", "route_coverage.json", "closure_delta.json", "target_disposition.json", "published_applications.json"]),
]:
    for name in names:
        reviewed.append(binding("dependency_audit_v" + version + "/" + name,
            "Original selected whole-contract scopes, the two exact closures, unchanged dependency edges and remaining categories; current additive qualifications are distinguished from historical evidence. Historical target-disposition records are not freshly reread in full."))

for comp in cfg["components"]:
    reviewed.append(binding(comp + "/main.tex",
        "Stated endpoint, quantifier, normalization, guard and consumer scope. This is not a fresh independent mathematical review of every block; separately bound component reviews supply that coverage."))
    for name in ["contracts.json", "closure.json", "retained_foundations.json", "classical_inputs.json"]:
        if (ROOT / comp / name).exists():
            reviewed.append(binding(comp + "/" + name,
                "Exact original endpoint and retained-input boundaries, distinguishing actual producers, conditional theorems and precisely matched named foundations."))
    reviewed.append(binding(comp + "/provenance.json",
        "Current claim classification, inherited-input and external-foundation boundaries, plus final independent review coverage and endpoint identifiers."))

for path in [
    "canonical_cusp_connection_v47/review_CNC1_CNC16_root.json",
    "principal_cusp_lattices_v47/review_PCL1_PCL12_root.json",
    "local_growth_suppliers_v47/review_LGS1_LGS13_ordinary_structure.json",
    "type_ii_rigidity_v47/review_KTR1_KTR13_root.json",
    "kato_input_assembly_v47/review_KIZ1_KIZ2_root.json",
]:
    reviewed.append(binding(path, "Separately saved mathematical/source review and final proof/block bindings; establishes authorship/review separation and the exact whole-contract scope where stated."))

generated = []
for path in [
    "RH_new_proofs_v0_47.tex", "RH_readable_reconstruction_v0_47.tex",
    "dependency_audit_v0_47/main.tex", "RH_dependency_audit_v0_47.txt",
    "README.md", "RH_reconstruction_progress_v0_47.txt", "README.txt",
    "integration_stats_v0_47.json", "tex_validation.json",
]:
    generated.append(binding(path,
        "Current front matter, audit, endpoint summaries, inventory, retained-input and continuation prose, and reported validation scope. For the cumulative reader this does not assert a fresh reading of every preserved historical chapter."))

selected = {
    "type_ii_rigidity_v47": ["KTR3", "KTR13"],
    "kato_input_assembly_v47": ["KIZ1", "KIZ2"],
    "row_finiteness_v47": ["RFD1", "RFD8", "RFD9"],
    "adelic_setting_v47": ["ASG18"],
    "canonical_cusp_connection_v47": ["CNC12", "CNC14", "CNC15", "CNC16"],
    "principal_cusp_lattices_v47": ["PCL5", "PCL11", "PCL12"],
    "local_growth_suppliers_v47": ["LGS1", "LGS7", "LGS10", "LGS11", "LGS12", "LGS13"],
}
blocks = []
for comp, ids in selected.items():
    data = (ROOT / comp / "main.tex").read_bytes()
    for claim in ids:
        start = data.index(("% BEGIN " + claim + "\n").encode())
        end = data.index(("% END " + claim).encode(), start) + len(("% END " + claim).encode())
        if data[end:end + 1] == b"\n":
            end += 1
        blocks.append({"claim": claim, "path": comp + "/main.tex",
            "line_start": data[:start].count(b"\n") + 1,
            "line_end": data[:end].count(b"\n"),
            "block_sha256": hashlib.sha256(data[start:end]).hexdigest(),
            "review_scope": "Focused endpoint/guard/interface reading; independent full mathematical coverage is separately recorded. CNC and PCL are authored by this reviewer and independently reviewed by root."})

source_checks = []
source_specs = [
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean", 13, 24, "Literal universal KatoUse and all five CohInp fields; original prime, twist and uniform-constant scope."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean", 54, 64, "Separate original OneChar trace/length producer, which is neither a field of InpZ nor closed by its assembly."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean", 43, 61, "Full KatoTwo, literal RigII with universal extension-modularity antecedent, and all six extra InpZ fields."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/RowsDef.lean", 67, 81, "Full RowsFinDim with arbitrary supplied supported locally constant function, unit vectors, original weak operators and measures."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/SettingBlocks.lean", 337, 379, "Exact dependent setting constructor and distinction between the eight constructed blocks and original W/M producer inputs."),
    ("src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsGlobalSetting.lean", 45, 81, "Same-D actual setting and spectral endpoints retain Siegel-Weil, Bessel uniqueness, local ties and all-form transport requirements."),
    ("src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/CongrOfDvdModulus.lean", 36, 57, "Actual remaining principal-chart/uniformization constructor, including family models, simultaneous normalized framed points, LatZ and exponent match; PCL does not assume this conclusion as a new theorem."),
]
for path, first, last, scope in source_specs:
    data = (SOURCE / path).read_bytes()
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    excerpt = b"".join(lines[first - 1:last])
    source_checks.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(),
        "line_start": first, "line_end": last,
        "range_sha256": hashlib.sha256(excerpt).hexdigest(), "scope": scope})

findings = [
    ("TWO_LITERAL_SELECTED_CLOSURES", "Only RIG_II and TASK_INP_Z_ASSEMBLY leave the selected whole-obligation register. The first was a class-C original producer and is now a proved class-B certificate; the second was already an implication/record reconstruction task. Both original contract texts and all selected requires edges are unchanged. No geometric, global-gain, retained-defect, OneChar or automorphy whole obligation is closed."),
    ("TYPE_II_ORIGINAL_POINT_AND_GUARD", "KTR13 consumes the original marked Dat/ULoc/IsPt, fixed iota and exact universal IsExt-to-IsModular antecedent. It produces a primitive for the full nine-dimensional polarized adjoint, with actual local inertia data, full infinite-cyclotomic irreducibility and an explicit 4+2+2+1 decomposition. It does not construct the separate modularity antecedent, change the point or replace the full adjoint by its trace-zero part. No new coefficient-prime restriction is added; all original GD guards remain."),
    ("KATO_AND_PUBLISHED_SCOPE", "KatoUse/KatoTwo use the original W=V_f(e), weight 2e+1 and the noncentral critical twist e, with the source geometric-Frobenius convention and exact local finite conditions. The four new class-A applications are KTR2, KTR9, RFD1 and ASG3. Their primary statements and matching are separately reviewed. Earlier polarized adjoint, cohomological, period, automorphic and geometric foundations are retained as foundations rather than counted as newly proved mathematics."),
    ("ENTIRE_INPZ_SAME_OBJECT_ASSEMBLY", "KIZ1 constructs all five CohInp fields, using the already fixed normalized local/global conventions and the uniform LemmaK constant 31 before all later arithmetic data. KIZ2 inserts the exact six additional fields LemmaM, LemmaMprime, LemmaP, RigII, AdVanishK and CongruenceNumberRankThree. Their universal antecedents remain part of each field; prime-two cohomological guards, prime-three scope of applicable odd-prime fields, and the original rank-three rather than rank-four congruence contract are retained."),
    ("ONECHAR_AND_AUTOMORPHY_STAY_OPEN", "Supplying InpZ does not establish its OneChar consumer or AutomorphyUnramifiedCoefficients. The latter still requires one actual marked g1 furnishing FinA, AutB and LemW together. The former still needs the original coefficient ring/point construction and exact trace/length inequality. The completed finite PGK implication remains available and is not presented as unconditional PropGK or Case I."),
    ("UNIVERSAL_ROWS_FINDIM", "RFD8 matches every quantifier of literal RowsFinDim. Its finite kernel is only locally constant and supported in the original compact Kset; no idempotence or self-adjointness is inserted. The given archimedean vectors are arbitrary unit vectors, and the original Haar measures, right regular action and weak operator identities are retained. Compact-finite auxiliary vectors serve only in the finite-multiplicity argument. RFD9 removes this one premise from ARO without producing the remaining common setting, ties or arithmetic cylinder counts."),
    ("EIGHT_DEPENDENT_ADELIC_BLOCKS", "ASG18 constructs A,L,P,Rf,Xu,Bu,Pi,Mu in the original dependent order, from the original Forms0(D,u0) and GapHyp. The same lattice/reference choices precede every word. Generic ScRefExists and ScXuExists retain arbitrary supplied original reference frames. The finite weights remain lowK(allPos,u)=u-rhoC; the quotient measure normalization does not silently rescale the prescribed ambient Haar measure."),
    ("ADELIC_SETTING_BOUNDARY", "The actual nonzero Bessel W with its normalized integral and decay, measured-field block, Siegel-Weil rescaling and measure/character ties, Bessel uniqueness/local ties, full same-D transport and common-family thresholds remain explicit. Eight setting blocks and RowsFinDim do not by themselves establish ConcreteSettingExists, exists_spectralData, CountIdempotentsClass or GLOBAL_RETAINED_DEFECT."),
    ("CANONICAL_CONNECTION_PRODUCED", "CNC supplies the full original IsNab and generic canonical gauge for every original coefficient algebra, including nonreduced and nonlocal rings. It retains the actual moduli object, rigidified line, framing, germ and derivative conventions. The two named Stacks foundations concern proper universal base functions and smooth-section formal coordinates; neither stands for an unproved specialized IsNab predicate. This removes exactly the old connection input from ICL's conditional spanning route."),
    ("PRINCIPAL_LATTICE_NORMALIZATION_ONLY", "PCL produces the literal Hermitian-coordinate and trace-dual constructors, exact nonprincipal ideal identities, actual self-dual lattice A^(-1)Lambda, prescribed NA=Norm(b), NC=Norm(ccK), k0 and the exact logarithmic bounds. Its all-row/all-good-embedding/all-component DataX endpoints keep the original metric, scalar, groups, congruence modulus and order before later weights. IsUnf, HasPrinc/GamAt and LawsCore remain supplied hypotheses; the actual principal-chart family and analytic uniformization are not inferred."),
    ("FIVE_GEOMETRIC_GROUPS_REMAIN", "After CNC and the bounded PCL subproducer, the actual principal charts/common uniformization, finite level systems, raw Gaussian/reproduction, short-rule/simultaneous dictionary, and ramified-jet producers remain. Full LatFull spanning, both-level MLat transport on actual common geometry, higher CoversAt, all-tuple phase-correct class sums/uniqueness, one PointIdentCore with common lambda,z before every tuple, ClassSumsSpan, Fits and eta agreement remain original coupled tasks."),
    ("ACTUAL_LOCAL_GROWTH_AND_AUXILIARY_CHAIN", "LGS proves the original integral lattice sandwich, chosen dyadic small-order and band estimates, canonical mean deficit, local exceptional-generator/walk length estimate and all twelve auxiliary admission fields with exact constants and choice order. The zero-chain construction changes only auxiliary LatInst.Ch. It does not change the original FamP/geometric theta chain or transport the original Extra.ker predicate; all original valuation lattices, degrees, comparison maps, support and normalized ramification factors are preserved."),
    ("LINKG_POINTWISE_AND_CLOSED_SCOPES", "LGS13 gives all five literal LinkG conclusions with C_G=4C_count+1 and b_o=b^(x^(-epsilon/2)). Its pointwise theorem retains actual GroupCompatibilityFamily and Adm2F on the same family, with TopsF as an actual supplier of Adm2F. Its class-level linkG_concrete5 retains the two original Closed predicates, including cutoffs and coefficient bounds chosen before the family. These quantified class hypotheses are not weakened to unrelated pointwise witnesses; GLOBAL_LOCAL_GAIN remains open."),
    ("UNCHANGED_COMPOUND_FRONTIER", "All 121 selected nodes and 161 requires edges are preserved. The 26 remaining obligations keep their old category, kind, status and gate. Five compound contracts retain the complete previous text and append explicit current qualifications; every other selected contract is unchanged. The new register is 19 C plus 7 B, with 19 shared RH/Dirichlet-GRH, seven additional Dirichlet-GRH and zero RH-only obligations. Counts are not percentages or minimality claims."),
    ("PRIOR_COMPLETIONS_AND_REMAINING_CASES", "The full six-field same-J Hida theorem, all-level LevelAlt/HasAut, both selected support Links, CNR3, finite PGK implication, structural arithmetic rows, ICL finite generation and logarithmic counting remain available at their existing scopes. The active roadmap does not reopen those results or restore Case II. RH retains the indicated Cases I/V, host/support and OneChar/automorphy work; unrestricted Dirichlet GRH retains its separate Case III/promodularity, Seed IV, tensor-factor and rank-four chain tasks."),
    ("CURRENT_METADATA_AND_READING_ORDER", "Current provenance.scope, checkpoint.status and next_source_targets.current_status_v0_47 agree with the final increment. Current conclusions, retained-input lists and next priorities agree; active audit/deliverable pointers name v0.47 outputs. The current reader titles and chapter list identify KTR,KIZ,RFD,ASG,CNC,PCL,LGS, with predecessor chapters explicitly historical. The TXT audit includes every full current contract."),
    ("PRESERVATION_AND_VALIDATION_SCOPE", "The release states preservation of predecessor claim records and the complete historical proof body, with mutable v0.46 metadata archived in history/version_0_46; it does not promise that active front matter is unchanged. Proof reviews, exact source/proof hashes, draft TeX syntax/reference checks and the separate integration audit have distinct scopes. No PDF visual certification, formal replay, mechanically extracted Lean dependency graph, completion percentage or completed human RH/GRH proof is asserted."),
]

report = {
    "schema": "rh-semantic-scope-review/1", "artifact_version": "0.47",
    "reviewer": "ordinary_structure", "date": "2026-11-23", "status": "PASS",
    "source_commit": PIN,
    "scope": "Final independent semantic review of v0.47 configuration, integration/assembly narrative, current continuation metadata, all seven completed endpoint packets and generated readers/audit/progress/README. Direct comparison with the v0.46 selected whole-contract register. Separate from the exhaustive preservation/source/dependency audit.",
    "independence": "The reviewer independently reviews root-authored release scope and authored the separate full LGS1-LGS13 mathematical/source review. The reviewer authored CNC and PCL; their independent mathematical coverage is supplied by root's full reviews. KTR,KIZ,RFD and ASG are checked here for exact endpoints, quantifiers, guards, retained foundations and consumer scope, not claimed as a fresh full mathematical re-review of every block.",
    "reviewed_files": reviewed,
    "focused_claim_blocks": blocks,
    "generated_outputs_reviewed": generated,
    "literal_source_boundary_checks": source_checks,
    "checks": [{"id": key, "result": "PASS", "finding": text} for key, text in findings],
    "inventory_checked": {
        "new_claim_blocks": 83, "new_claim_classifications": {"A": 4, "B": 79},
        "cumulative_claims": 2851, "predecessor_claims": 2768,
        "selected_nodes": 121, "selected_edges": 161,
        "prior_whole_obligations": 28, "whole_obligations": 26,
        "categories": {"C": 19, "B": 7},
        "root_scope_counts": {"shared_RH_GRH": 19, "GRH_only": 7, "RH_only": 0},
        "new_whole_leaf_closures": 2, "closed_whole_obligation_ids": sorted(closed),
        "whole_obligation_ids": list(now_open),
        "new_pinned_source_files": 148, "new_distinct_source_ranges": 207,
    },
    "tex_validation_checked": [{k: d[k] for k in ["tex_filename", "tex_sha256", "passes", "syntax_compile_succeeded", "missing_character_warnings", "undefined_references_or_citations", "overfull_box_warnings", "pdf_generated", "pdf_visual_review_performed"]} for d in tex["documents"]],
    "corrections_resolved": [
        {"item": "Stale v0.46 title and new-chapter reading order in the assembly draft", "resolution": "Root replaced the inherited title and chapter list with the actual v0.47 title and seven new packets before freezing the readers."},
        {"item": "Auxiliary zero-chain and class-level LinkG precision", "resolution": "The independently reviewed LGS proof distinguishes absent-basis model intersections from off-lattice function values and preserves original Extra.ker. Current release prose also distinguishes pointwise compatibility/admission from the two original Closed predicates with their earlier cutoffs and coefficient choices."},
    ],
    "material_corrections_required": [],
    "not_claimed": [
        "No fresh full independent mathematical review of all 83 new claims or every historical proof.",
        "No replacement for separately bound component mathematical reviews or exhaustive integration audit.",
        "No OneChar or AutomorphyUnramifiedCoefficients producer, unconditional PropGK or completed Case I from the new RigII/InpZ theorems.",
        "No stronger local crystalline-component theorem than the original RigII argument needs.",
        "No common arithmetic/geometric-family existence, principal-chart/uniformization theorem, full cusp spanning, arithmetic cylinder count or unconditional global-gain producer from the conditional constructions.",
        "No construction of the original geometric chain's Extra.ker or weakening of class-level Closed hypotheses to separate pointwise witnesses.",
        "No new proofs of the separately named classical foundations themselves.",
        "No complete human-readable RH or unrestricted Dirichlet-GRH proof, Lean replay, completion percentage or PDF visual certification.",
    ],
}
out = ROOT / "reviews_v0_47/semantic_scope_ordinary_structure.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": report["status"], "reviewed_files": len(reviewed),
    "generated_outputs": len(generated), "focused_claim_blocks": len(blocks),
    "source_boundary_ranges": len(source_checks), "sha256": digest(out)}, indent=2))
