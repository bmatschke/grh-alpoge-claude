#!/usr/bin/env python3
"""Bind the independently authored v0.48 semantic-scope review to final bytes.

The findings below are the reviewer's judgments after reading the release
narrative, exact endpoint interfaces, original source contracts and final
generated reports. Assertions guard inventory and bindings; they do not
replace the independent component proof reviews or integration audit.
"""
import collections
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT.parent / "formal_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"


def read(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path, scope):
    return {"path": path, "sha256": digest(ROOT / path), "review_scope": scope}


cfg = read("increment_v0_48.json")
stats = read("integration_stats_v0_48.json")
prior_map = read("dependency_audit_v0_47/obligation_map.json")
now_map = read("dependency_audit_v0_48/obligation_map.json")
prior_nodes = {n["id"]: n for n in prior_map["nodes"]}
now_nodes = {n["id"]: n for n in now_map["nodes"]}
prior_open = {n["id"]: n for n in read("dependency_audit_v0_47/remaining_leaf_register.json")["records"]}
now_open = {n["id"]: n for n in read("dependency_audit_v0_48/remaining_leaf_register.json")["records"]}
closed = {"TASK_ONE_CHAR_PROOF"}
qualified = {"AUT_UNRAM_COEF", "GLOBAL_RETAINED_DEFECT", "GLOBAL_SPECTRAL",
             "GLOBAL_LOCAL_GAIN", "DESIGN_CHOICES_COMMON", "BASE_THETA_RATIONAL_TESTS"}
assert prior_nodes.keys() == now_nodes.keys()
assert set(prior_open) - set(now_open) == closed
assert not (set(now_open) - set(prior_open))
assert len(now_nodes) == 121
assert sum(len(n["requires"]) for n in now_nodes.values()) == 161
assert all(prior_nodes[k]["requires"] == now_nodes[k]["requires"] for k in now_nodes)
for key in now_nodes:
    if key not in closed:
        for field in ["category", "kind", "status", "gate"]:
            assert prior_nodes[key].get(field) == now_nodes[key].get(field), (key, field)
    if key in qualified:
        assert now_nodes[key]["contract"].startswith(prior_nodes[key]["contract"])
        assert now_nodes[key]["contract"] == cfg["updated_contracts"][key]
    else:
        assert now_nodes[key].get("contract") == prior_nodes[key].get("contract")
assert set(cfg["updated_contracts"]) == qualified
assert prior_nodes["TASK_ONE_CHAR_PROOF"]["category"] == "C"
assert now_nodes["TASK_ONE_CHAR_PROOF"]["category"] == "B"
assert now_nodes["TASK_ONE_CHAR_PROOF"]["status"] == "proved_in_stated_scope"
assert collections.Counter(n["category"] for n in now_open.values()) == {"C": 18, "B": 7}
assert stats == {
    "new_claims": 89, "cumulative_claims": 2940,
    "selected_nodes": 121, "selected_edges": 161,
    "open_count": 25, "open_categories": {"C": 18, "B": 7},
    "shared_open": 18, "extra_grh_open": 7,
    "new_source_files_checked": 185, "new_unique_source_ranges_checked": 226,
}
assert set(cfg["closed_selected_leaves"]) == closed
assert all(n["contract"] in (ROOT / "RH_dependency_audit_v0_48.txt").read_text()
           for n in now_open.values())

coverage = read("dependency_audit_v0_48/route_coverage.json")
assert coverage["ordinary_rh_open_leaf_count"] == 18
assert coverage["dirichlet_grh_open_leaf_count"] == 25
assert coverage["shared_open_leaf_count"] == 18
assert len(coverage["dirichlet_grh_only_open_leaf_ids"]) == 7
assert not coverage["ordinary_rh_only_open_leaf_ids"]
onechar_review = read("one_character_v48/review_OCH1_OCH30_root.json")
exact = onechar_review["selected_whole_contract_reviewed"]
assert exact["id"] == "TASK_ONE_CHAR_PROOF"
assert exact["full_original_contract_closed_in_stated_scope"]
assert exact["baseline_contract_sha256"] == hashlib.sha256(
    prior_nodes["TASK_ONE_CHAR_PROOF"]["contract"].encode()).hexdigest()

provenance = read("provenance.json")
checkpoint = read("continuation_checkpoint.json")
targets = read("next_source_targets.json")
assert provenance["scope"] == checkpoint["status"] == targets["current_status_v0_48"] == cfg["status"]
assert provenance["version_0_48_local_conclusions"] == checkpoint["new_in_this_version"] == cfg["local_conclusions"]
assert provenance["component_input_boundaries_v0_48"] == checkpoint["remaining_major_inputs"] == cfg["remaining_major_inputs"]
assert checkpoint["next_targets"] == targets["next_local_priority"] == cfg["next_targets"]
assert targets["version_0_48_precision_notes"] == cfg["local_conclusions"] + cfg["remaining_major_inputs"]
for key, value in checkpoint["current_dependency_audit"].items():
    if key not in {"artifact_version", "scope"}:
        assert value.startswith("dependency_audit_v0_48/") and (ROOT / value).exists()
assert checkpoint["current_deliverable"]["main"] == "RH_readable_reconstruction_v0_48.tex"
assert checkpoint["current_deliverable"]["new_chapters"] == "RH_new_proofs_v0_48.tex"

new_claims = []
for comp in cfg["components"]:
    new_claims.extend(read(comp + "/provenance.json")["claims"])
assert len(new_claims) == 89
assert collections.Counter(c["classification"] for c in new_claims) == {"B": 89}
assert not cfg["published_applications"]
new_by_id = {c["id"]: c for c in new_claims}
assert "PUN12" in new_by_id["PUN17"]["depends_on"]
assert "PUN12" in provenance["mathematical_dependency_graph"]["PUN17"]
assert len({s["path"] for c in new_claims for s in c.get("sources", []) if "path" in s}) == 185
assert len({(s["path"], s["line_start"], s["line_end"])
            for c in new_claims for s in c.get("sources", []) if "line_start" in s}) == 226

tex = read("tex_validation.json")
assert tex["artifact_version"] == "0.48"
expected_hashes = {
    "RH_new_proofs_v0_48.tex": "1b1f69502739d91cca6fb04354a74ac1f1afd572cc37a34ae4ce2f29b3f5d6d1",
    "RH_readable_reconstruction_v0_48.tex": "6d2fd4dae1638a9cbfcb809cd14234f03e5608ce69634fa03890962740ac3c8d",
    "RH_reconstruction_progress_v0_48.txt": "1a5093a77a083802fee1577f07e64c90cc1ec4593ccb8023af461b69dcf6db32",
    "README.txt": "dda25fc62340e313216cacf05dc766841e4064dd8503a38d0172e1b910639f62",
    "write_progress_v0_48.py": "54cdcc351c64a632f35de083aa84b9caadb26b845e79650c20da28e9eefe2a3b",
}
assert all(digest(ROOT / p) == h for p, h in expected_hashes.items())
for item in tex["documents"]:
    assert digest(ROOT / item["tex_filename"]) == item["tex_sha256"]
    assert item["syntax_compile_succeeded"]
    assert not item["undefined_references_or_citations"]
    assert item["missing_character_warnings"] == 0
    assert not item["pdf_generated"] and not item["pdf_visual_review_performed"]
assert [d["passes"] for d in tex["documents"]] == [2, 3]
assert [d["overfull_box_warnings"] for d in tex["documents"]] == [0, 53]
progress = (ROOT / "RH_reconstruction_progress_v0_48.txt").read_text()
for name in ["increment_v0_48.json", "integration_stats_v0_48.json"]:
    assert name + " SHA256: " + digest(ROOT / name) in progress

reviewed = []
script_scope = "Current semantic scope, choice order, exact selected implication closure, retained antecedents and generated narrative; exhaustive source/preservation mechanics belong to the separate integration audit."
for path in ["increment_v0_48.json", "configure_v0_48.py", "assemble_v0_48.py",
             "integrate_v0_48.py", "write_progress_v0_48.py", "v0_48_frontmatter.tex", "v0_48_audit_intro.tex"]:
    reviewed.append(binding(path, script_scope))
for path, scope in [
    ("provenance.json", "Current scope, current_boundary_authority, version_0_48_local_conclusions, component_input_boundaries_v0_48, inventory and corrected PUN17 premise; not a rereading of every historical record."),
    ("continuation_checkpoint.json", "Current status, new_in_this_version, remaining_major_inputs, next_targets, current_dependency_audit, current_deliverable and version_0_48_update."),
    ("next_source_targets.json", "Current v0.48 status, precision notes, selected-frontier paths and next_local_priority; earlier version-specific records remain historical."),
]:
    reviewed.append(binding(path, scope))
for version, names in [
    ("0_47", ["obligation_map.json", "remaining_leaf_register.json"]),
    ("0_48", ["obligation_map.json", "remaining_leaf_register.json", "route_coverage.json",
              "closure_delta.json", "target_disposition.json", "published_applications.json"]),
]:
    for name in names:
        reviewed.append(binding("dependency_audit_v" + version + "/" + name,
            "Original selected whole-contract scope, only the exact OneChar implication closure, unchanged requires edges and remaining categories. Six current qualifications append the preserved contract text; historical target-disposition entries are not freshly re-reviewed in full."))

for comp in cfg["components"]:
    reviewed.append(binding(comp + "/main.tex",
        "Endpoint, quantifier, normalization, guard and consumer scope; this is not a fresh independent mathematical re-review of every claim. Separately bound component proof reviews provide that coverage."))
    for name in ["contracts.json", "closure.json", "retained_foundations.json", "classical_inputs.json"]:
        if (ROOT / comp / name).exists():
            reviewed.append(binding(comp + "/" + name,
                "Original endpoint and retained-input boundaries, distinguishing numbered deductions, exactly matched named foundations, supplied original data and still-open producers."))
    reviewed.append(binding(comp + "/provenance.json",
        "Current claim classification, inherited inputs and named-foundation boundaries, exact endpoint identifiers and final independent review coverage."))
    for path in sorted((ROOT / comp).glob("review_*.json")):
        data = json.loads(path.read_text())
        assert data.get("result", data.get("status")) == "PASS"
        assert data.get("proof_sha256", data.get("proof_file_sha256")) == digest(ROOT / comp / "main.tex")
        reviewed.append(binding(str(path.relative_to(ROOT)),
            "Separately authored mathematical/source review, proof hash and actual reviewed block scope. Root's OCH review additionally binds the exact original selected whole-contract text."))

generated = [binding(path,
    "Final current front matter, endpoint summaries, complete current audit, retained-input and continuation narrative, inventory and validation scope. The cumulative reader binding does not assert a fresh reading of every preserved historical chapter.")
    for path in ["RH_new_proofs_v0_48.tex", "RH_readable_reconstruction_v0_48.tex",
                 "dependency_audit_v0_48/main.tex", "RH_dependency_audit_v0_48.txt",
                 "README.md", "RH_reconstruction_progress_v0_48.txt", "README.txt",
                 "integration_stats_v0_48.json", "tex_validation.json"]]

selected = {
    "one_character_v48": ["OCH27", "OCH28", "OCH29", "OCH30"],
    "adelic_measures_v48": ["AMD" + str(i) for i in range(10, 18)],
    "principal_uniformization_v48": ["PUN1", "PUN10", "PUN11", "PUN14", "PUN17", "PUN19", "PUN20", "PUN22", "PUN23", "PUN24"],
    "common_compatibility_v48": ["GCF" + str(i) for i in range(12, 19)],
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
            "review_scope": "Focused endpoint/guard/interface reading. AMD10-AMD17 also have this reviewer's separate complete mathematical/source review. PUN is authored by this reviewer and independently reviewed by root; OCH and GCF full proof reviews are separately bound."})

source_specs = [
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean", 54, 64, "Literal OneChar: all original closures, fixed iota and coefficient data, both admissibility branches, nonvanishing premise, finite length and exact factor-two isomorphism-irredundant trace sum."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicCases/AutomorphyUnramifiedCoefficients.lean", 12, 27, "Separate FinA, AutB and universal LemW fields supplied jointly by one marked g1 for the same datum and fixed iota; this producer stays open."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean", 9, 22, "Every original GD field retained, including ell-1 not dividing 2e; no added prime or weight restriction and no assertion of full-GD data at ell=3."),
    ("src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/KatoQuadraticCharacters/OneChar.lean", 158, 178, "Exact complete implication and same-valued unramified coefficient return, not an embedding of the whole original ramified coefficient ring."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/CokernelGLCounts/Measures.lean", 65, 128, "Actual five-entry MeasG and eight-entry MeasW, six/eleven clauses, exact rational subgroup and source choice-based covolume."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/MExistsCut.lean", 11, 47, "Full MExistsCore/MExists with same bridge and literal antecedent blocks, including supplied Wb."),
    ("src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/UnitaryHaarProducts/MeasCore.lean", 17, 26, "Original standard-frame guard in MWCore and InfTransfer; no unguarded arbitrary-frame strengthening."),
    ("src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsMeasWPrescribed.lean", 1, 51, "All prescribed infinity/global-N/global-H/local-S measures retained exactly; source does not add local/restricted-product ties."),
    ("src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/ExistsHaarMeasureUnipotentRadicalCovolumeOneStatement.lean", 1, 8, "Original rational-unipotent covolume-one endpoint."),
    ("src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/CongrOfDvdModulus.lean", 36, 57, "Remaining full principal-chart constructor: the arithmetic models, LatZ and ExpoMatch suppliers do not by themselves supply N1c, simultaneous normalized frames or IsUnf/FromTest."),
    ("src/Development/AbelianVarietyTheory/Definitions/ExistenceOfLattices/NormConst.lean", 16, 33, "Literal ModelsOf and ModelBase on a supplied family, keeping the fixed space, scalar and exact arithmetic lattice."),
    ("src/Formalism/LocalToGlobal/ProjectiveLattices/IntegrableOnIntegrand.lean", 139, 193, "Original cusp coefficient lattices, zMatE/zGam, rank and phase conventions, preserving exact half-trace normalization and all-rank scope."),
    ("src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsGIs.lean", 146, 165, "Full true-volume GIs2 stage chosen once before every later W,V,S,N on the original column input."),
    ("src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/DsigEq.lean", 24, 66, "Remaining Wit fields, single dependent (Gt,cmp,tw,ker) equality and joint (D,O) realization; a canonical stage alone does not identify a supplied family."),
    ("src/Formalism/LocalToGlobal/ThresholdSelection.lean", 9, 16, "Original TSelF and class TSel with cutoff chosen before all later family indices and data."),
    ("src/Formalism/LocalToGlobal/ClassSLinks.lean", 9, 13, "Actual same-family compatibility and original threshold order."),
    ("src/Formalism/LocalToGlobal/Divisibility/DivisibilityRemainder/AdmissibleClasses/LinkGCl.lean", 11, 32, "Selected D3 admission and full class-level LinkG consumer retain the original TSel realization and Closed order."),
]
source_checks = []
for path, first, last, scope in source_specs:
    data = (SOURCE / path).read_bytes()
    assert data == subprocess.check_output(["git", "-C", str(SOURCE), "show", PIN + ":" + path])
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    excerpt = b"".join(lines[first - 1:last])
    source_checks.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(),
        "line_start": first, "line_end": last,
        "range_sha256": hashlib.sha256(excerpt).hexdigest(), "scope": scope,
        "source_commit": PIN, "verified_equal_to_pinned_git_blob": True})

findings = [
    ("ONLY_THE_LITERAL_ONECHAR_IMPLICATION_CLOSES", "Only TASK_ONE_CHAR_PROOF leaves the selected whole-obligation register. Its complete original contract text is byte-for-byte preserved, and the exact implication InpZ -> AutomorphyUnramifiedCoefficients -> OneChar is independently reviewed. The old class-C reconstruction task is now a class-B proved certificate. AUT_UNRAM_COEF remains open; no geometric or global-gain whole obligation closes."),
    ("JOINT_AUTOMORPHY_WITNESS_RETAINED", "One marked g1 must jointly provide FinA, AutB and LemW for the same original Dat and fixed iota. FinA quantifies over every actual local/global ring; AutB retains every push and Type-I point; LemW retains the middle-entry guard and every actual IsExt. OCH's local component, global model, rigidity and trace estimate do not manufacture that separate producer or invoke OneChar circularly to obtain it."),
    ("EXACT_COEFFICIENT_GUARDS_AND_SMALL_PRIMES", "OCH30 retains every original closure, Coef, N!=0, e, GD, fixed iota, sigma and supplied base trace. No additional lower bound on ell or e is inserted. Applicable local finite-Artin constructions include nonreduced targets and critical e=1; full GD itself excludes ell=3 by its unchanged ell-1 not dividing 2e condition. Preserving prime-three scope does not assert a nonexistent full-GD case."),
    ("ACTUAL_LOCAL_AND_GLOBAL_MODEL", "The OCH scope is the actual saturated ordinary component It, its twelve-variable chart with multiplicities (1,2,3,4,2), and the original normalized integral graded model. FinA is used for its quotient weight-zero module, not to claim finiteness of the ambient graded algebra. Formal Taylor division supplies the needed extension and lifting for arbitrary actual maps and derivations; no extra continuity premise is inserted."),
    ("TRACE_SUM_AND_LENGTH_NORMALIZATION", "The finite set consists of actual Adm3(iota,e,N) or Adm2(iota,e,N*abs(disc K)) homomorphisms, pairwise irredundant under RepIso. The Adm2 branch can be reducible in dimension three. The upper bound is reapplied to the final covering set rather than obtained by deleting positive summands. Vlen is bounded before finiteness is used; Vn divides by eO, v_ell(ell)=1, and the factor two remains exact."),
    ("UNRAMIFIED_RETURN_IS_SAME_VALUED", "OCH29 places the same finite character values in an unramified coefficient datum inside the fixed algebraic closure. It does not embed the entire possibly ramified original coefficient ring in an unramified ring. The exact GD predicate and trace scalar persist, and RV7 returns the identical representation set and normalized bound to the original supplied datum."),
    ("MEASURED_BLOCK_AT_LITERAL_SCOPE", "AMD proves the exact bridge, MGExists, standard-frame MWCore, InfTransfer and full MExistsCore/MExists. The weak original Haar-on-set predicate is promoted by its explicit Tonelli argument; no hidden Radon assumption is substituted. One bridge precedes every word and all five MeasTie equalities are literal. The original antecedent blocks, including Wb, remain supplied in MExists; its proof does not assert Bessel existence."),
    ("PRESCRIBED_MEASURES_AND_COVOLUME", "The prescribed MeasW constructor retains both infinity measures, both global N/H measures and every local S measure, absorbing required Haar scalars in finite factors. Rational-unipotent compact representatives and a Borel fundamental domain justify the source's choice-based covolume, including its almost-everywhere version. Covolume one then preserves infinity/H/local-S data. This supplies the measured portion, not the remaining normalized orbital/fiber or Siegel-Weil identities."),
    ("EXACT_ARITHMETIC_PRINCIPAL_MODELS", "PUN keeps the actual CM host, fixed Hermitian matrix/scalar, every finite place including dyadic places, and nonprincipal projective lattices. Its local-to-global argument, exact principal congruence, finite index, flag freeness and uniform transvection modulus give every LatModel field. ModelsOf/ModelBase/NegXi still take the original FamilyUnif as a supplied input. All-family/all-rank LatZ and A=1 ExpoMatch use the original coefficient ideals, different and half-trace factor without saturation or a replacement lattice."),
    ("INDIVIDUAL_MODULI_POINTS_AND_FOUNDATIONS", "PUN20-PUN24 construct actual individual primitive marked period points, the source negative Weil sign, every positive torsion level, both markings, every C-to-k scalar extension, exact point equality and marked-genus nonemptiness. KTriv holds on all C-algebras, including nonreduced ones, by the separately named universal Picard foundation on every test scheme. The original Moduli representing object is supplied; named Riemann, Appell-Humbert, GAGA and Picard theorems are not counted as newly proved foundations."),
    ("FINITE_HOLOMORPHIC_FAMILY_STAYS_OPEN", "Individual period points and their arithmetic models do not establish N1c or FrameUnif.exists_unf_hasPrinc. Reverse extraction at every moduli point, prescribed local period lifts, holomorphic families, simultaneous normalized theta frames and the exact FramesOK/CoverTri/FibTri/IsUnf/FromTest dictionary remain. Integral cusp spanning, higher CoversAt, all-tuple phase-correct class sums, one PointIdentCore with common lambda,z and base ClassSumsSpan remain coupled to the original common field, metric, measure, phase, both levels, Fits and eta agreements."),
    ("ACTUAL_COMPATIBILITY_BEFORE_LATER_CHOICES", "GCF supplies the finer KDq determinant law, all-rank relative determinant on given frames, prescribed-column extension keeping the actual local family, and OmegaCompatible in the existing coefficient field with the given period root. All five GroupCompatibilityAll fields and the joint IsRecG are constructed together. One GJStage is fixed before every later W,V,S,N; its VolTieG uses GV19 at its explicit retained true-volume foundation."),
    ("DIVISION_TRANSPORT_IS_NOT_REALIZATION", "GCF15-GCF16 preserve the literal comparison map under arbitrary original submodules and real heights, including off-lattice tuples, and transport full IsRecG/ColT/ColumnDataSplitPrimes. GCF17 still requires the given WPt's single dependent (Gt,cmp,tw,ker) equality and joint (D,O) realization to identify the actual Extra.cmp/kernel. A canonical stage or unrelated isomorphic record does not supply the remaining rows, kernel/theta, divisor, object and gauge fields of Wit."),
    ("SELECTED_D3_ADMISSION_AND_CLOSED_ORDER", "On the selected D3 class, its original ChosenE supplies ChosenTT and ChosenBad, hence TopsF and Adm2F on the same subset with the unchanged threshold. Outside D3, arbitrary-family admission remains an antecedent. The class-level LinkG consumer retains original TSel/common realization and both Closed quantifier orders, with all cutoffs and coefficient bounds chosen before later family data. GLOBAL_LOCAL_GAIN remains open."),
    ("UNCHANGED_COMMON_AND_ADDITIONAL_FRONTIER", "All 121 selected nodes and 161 requires edges are preserved. The 25 remaining whole obligations retain category, kind, status and gate; only six additive current qualifications change their contract text, preserving every previous word. Counts are 18 C plus 7 B, with 18 shared RH/Dirichlet-GRH, seven additional Dirichlet-GRH and zero RH-only. The seven Case-III/tensor/seed/rank-four tasks are unchanged and are not closed by the rank-three OneChar implication."),
    ("PRIOR_RESULTS_AND_CURRENT_METADATA", "Completed six-field same-J Hida, LevelAlt/HasAut, both selected support Links, CNR3, finite PGK implication, Kato/InpZ/RigII, structural rows/RowsFinDim, canonical connection and integral-cusp finite generation remain available at their existing scopes. The active roadmap does not reopen them or restore Case II. Current root scope, checkpoint, continuation priorities, audit paths and reader titles all identify v0.48; the progress report's configuration/statistics hashes match the frozen inputs."),
    ("CLASSIFICATION_REVIEW_AND_VALIDATION_LIMITS", "All 89 new numbered claims are class-B human deductions. External foundations are separately named, with exact applications and inherited boundaries; no synthetic foundation nodes inflate the claim DAG. Every claim has an independent mathematical/interface review separate from its author. The corrected PUN17->PUN12 edge records a genuine premise already in the unchanged proof. Draft TeX syntax/reference checks are distinct from proof review and integration validation; no formal replay, PDF visual certification, completion percentage or complete human RH/GRH proof is asserted."),
]

report = {
    "schema": "rh-semantic-scope-review/1", "artifact_version": "0.48",
    "reviewer": "ordinary_structure", "date": "2026-11-23", "status": "PASS",
    "source_commit": PIN,
    "scope": "Final independent semantic review of v0.48 configuration, integration/assembly narrative, current continuation metadata, all four endpoint packets and generated readers/audit/progress/README. Direct comparison with the v0.47 selected whole-contract register. Separate from the exhaustive preservation/source/dependency audit.",
    "independence": "The reviewer independently reviews root/peer-authored release scope and authored the separate complete AMD10-AMD17 mathematical/source review. The reviewer authored PUN; root's full PUN1-PUN24 review supplies its independent mathematical coverage. OCH, GCF and AMD1-AMD9 are checked here for exact endpoints, quantifiers, guards, retained foundations and consumer scope, not claimed as a fresh full mathematical re-review of all their blocks.",
    "reviewed_files": reviewed,
    "focused_claim_blocks": blocks,
    "generated_outputs_reviewed": generated,
    "literal_source_boundary_checks": source_checks,
    "checks": [{"id": key, "result": "PASS", "finding": text} for key, text in findings],
    "inventory_checked": {
        "new_claim_blocks": 89, "new_claim_classifications": {"A": 0, "B": 89},
        "cumulative_claims": 2940, "predecessor_claims": 2851,
        "selected_nodes": 121, "selected_edges": 161,
        "prior_whole_obligations": 26, "whole_obligations": 25,
        "categories": {"C": 18, "B": 7},
        "root_scope_counts": {"shared_RH_GRH": 18, "GRH_only": 7, "RH_only": 0},
        "new_whole_leaf_closures": 1, "closed_whole_obligation_ids": sorted(closed),
        "whole_obligation_ids": list(now_open),
        "new_pinned_source_files": 185, "new_distinct_source_ranges": 226,
    },
    "tex_validation_checked": [{k: d[k] for k in ["tex_filename", "tex_sha256", "passes", "syntax_compile_succeeded", "missing_character_warnings", "undefined_references_or_citations", "overfull_box_warnings", "pdf_generated", "pdf_visual_review_performed"]} for d in tex["documents"]],
    "corrections_resolved": [
        {"item": "The early release draft described the trace sum as irreducible", "resolution": "Configuration and generated narrative now say isomorphism-irredundant and explicitly retain the Adm2 branch, which need not be irreducible in rank three. Proof bytes did not change."},
        {"item": "PUN17 cited PUN12 unitarity without a direct recorded premise edge", "resolution": "The component metadata builder, provenance and claim DAG now include PUN17->PUN12, and final root integration includes it. The written proof and its independent review hashes are unchanged."},
    ],
    "material_corrections_required": [],
    "not_claimed": [
        "No fresh full independent mathematical review of all 89 new claims or every historical proof.",
        "No replacement for separately bound component mathematical reviews or exhaustive integration audit.",
        "No actual AutomorphyUnramifiedCoefficients producer, unconditional OneChar or completed RH Case I from its implication alone.",
        "No embedding of an entire ramified original coefficient ring into the auxiliary unramified one, and no assertion that every Adm2 rank-three representation is irreducible.",
        "No N1c/finite holomorphic FamilyUnif, simultaneous normalized frame family, full principal-chart theorem, common geometric member, unconditional cusp spanning or all-tuple rational-test producer.",
        "No normalized Bessel existence/decay, full orbital/fiber/Siegel-Weil comparison, arithmetic cylinder count or unconditional normalized spectral producer.",
        "No actual eventual common WPt/TSel realization or whole GLOBAL_LOCAL_GAIN from a canonical compatibility stage and its division transport alone.",
        "No new proofs of the separately named classical foundations themselves.",
        "No complete human-readable RH or unrestricted Dirichlet-GRH proof, Lean replay, completion percentage or PDF visual certification.",
    ],
}
out = ROOT / "reviews_v0_48/semantic_scope_ordinary_structure.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": report["status"], "reviewed_files": len(reviewed),
    "generated_outputs": len(generated), "focused_claim_blocks": len(blocks),
    "source_boundary_ranges": len(source_checks), "sha256": digest(out)}, indent=2))
