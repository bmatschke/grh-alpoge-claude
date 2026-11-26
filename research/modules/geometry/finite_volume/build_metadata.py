#!/usr/bin/env python3
"""Rebuild FV source/proof and published-application certificates; no Lean run.

Portable invocation:
  python3 build_metadata.py --source /path/to/pinned/checkout \
      --human-root /path/to/reconstruction

All source ranges are inclusive and preserve original newline bytes.
Only the named inherited proof blocks are mathematical dependencies;
their complete files are additionally hashed as provenance containers.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "holomorphic_uniqueness").exists() else HERE.parents[1] / "reconstruction_v037"
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
args = ap.parse_args()
SOURCE, HUMAN = args.source.resolve(), args.human_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe|scoped)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}


def add(sid, path, anchor, stop=None, role="Exact original definition or source endpoint in the stated human scope"):
    path = "src/" + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    anchor = anchor.rstrip()
    pattern = re.compile(re.escape(anchor) + r"(?=$|[\s:({])")
    hits = [i for i, line in enumerate(lines) if pattern.search(line)]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    z = next((i for i in range(a + 1, len(lines)) if (stop in lines[i] if stop else decl.match(lines[i]))), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid, "path": path, "declaration": anchor, "declaration_anchor": anchor,
        "line_start": a + 1, "line_end": z,
        "sha256": sha(b), "file_sha256": sha(b),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[a].rstrip(), "role": role,
        "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a + 1}-L{z}",
    }


D = "Development/AbelianVarietyTheory/"
IW = D + "Proofs/IwasawaDecomposition/"
DP = D + "Proofs/DivisorProofs/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
GEN = "Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean"
for sid, anchor in [
    ("cm_extension", "def IsCMExt"), ("hermitian_nondegenerate", "def IsHermND"),
    ("tensor_involution", "def sigR"), ("tensor_inclusion", "def inclR"),
    ("tensor_gram", "def JR"), ("unitary_subgroup", "def HR"),
    ("rational_image", "def HFin"), ("rational_subgroup_generic", "def HFinIn"),
    ("tensor_topology", "scoped instance topTens"), ("tensor_measurability", "scoped instance measTens"),
    ("original_HA", "def HA"), ("original_HA_matrix", "def HA.mat"),
    ("full_adele_algebra", "abbrev AF"), ("infinite_adele_algebra", "abbrev Ainf"),
    ("finite_adele_algebra", "abbrev Af"), ("infinite_projection", "def fstA"),
    ("finite_projection", "def sndA"),
]:
    add(sid, GEN, anchor)
add("unitary_equation", "Formalism/SatakeDualWeyl/Statement.lean", "def UJ")
add("matrix_conjugate_transpose", "Formalism/SatakeDualWeyl/Statement.lean", "def cT")
add("matrix_base_change", "Formalism/SatakeDualWeyl/Statement.lean", "def bc")
for sid, anchor in [
    ("actual_group", "abbrev GA"), ("actual_matrix", "def matHom"),
    ("actual_rational_subgroup", "def GQ"), ("actual_finite_subgroup", "def GfC"),
    ("actual_infinite_subgroup", "def GinfC"), ("actual_finHom", "def finHom"),
    ("actual_infHom", "def infHom"), ("actual_automorphic_function", "structure IsAutFun"),
]:
    add(sid, BT + "IsAutFunDef.lean", anchor)
add("actual_CM_data", "Formalism/LocalRingCardinality/DataSpaces.lean", "structure CMData")
add("actual_CM_involution", "Formalism/LocalRingCardinality/DataSpaces.lean", "def CMData.sig")
add("actual_Hermitian_space", "Formalism/LocalRingCardinality/DataSpaces.lean", "structure HSpace")
add("actual_Gram", "Formalism/LocalRingCardinality/DataSpaces.lean", "def gram")
add("actual_HSp", "Formalism/LocalRingCardinality/DataTheta.lean", "abbrev HSp")
add("actual_gramAt", "Formalism/LocalRingCardinality/DataTheta.lean", "def gramAt")
add("actual_lcsc", IW + "LocallyCompactSecondCountableT2.lean", "theorem locallyCompact_secondCountable_t2")
add("actual_rational_discrete", IW + "DiscreteCountableGQ.lean", "theorem discrete_countable_GQ")
add("actual_CM_Gram_producer", IW + "CmDataIsCMExtAndGramIsHermND.lean", "theorem cmData_isCMExt_and_gram_isHermND")
add("actual_Gram_nonsingular", IW + "CmDataIsCMExtAndGramIsHermND.lean", "theorem hspace_gram_det_ne_zero")
add("complete_finite_volume_contract", D + "Definitions/Foundations/CdScaleTieIff.lean", "def FiniteVolume₂")
add("original_finite_volume", IW + "FiniteVolumeAdelicUnitaryQuotient.lean", "theorem finVol",
    role="Complete universal original endpoint; FV1-FV8 give a checked published application and independent transports instead of reconstructing this source route")
add("original_unimodularity", DP + "IsMulRightInvariantHaarAdelicUnitaryGroupHermiti.lean",
    "theorem GlobalTheory.AdelicPointsUnimod.isMulRightInvariant_of_isHaarMeasure",
    role="Original same-group unimodularity endpoint; FV5 obtains it from checked Borel 5.5")
add("original_unimodular_domain", IW + "AdelicUnitaryUnimodularExistsFundamentalDomain.lean",
    "theorem rightInvariant_and_exists_fundamentalDomain")
for sid, anchor in [
    ("exact_Borel_section", "theorem exists_measurable_section"),
    ("general_domain", "theorem exists_isFundamentalDomain"),
    ("actual_domain", "theorem exists_fundDom"),
]:
    add(sid, IW + "ExistsIsFundamentalDomain.lean", anchor)
add("domain_measure_equality", IW + "FundamentalDomainUnitaryAdelicExistsMeasureEq.lean",
    "theorem fundamentalDomain_exists_measure_eq_of_discrete")
add("actual_domain_measure", IW + "FundamentalDomainUnitaryAdelicExistsMeasureEq.lean",
    "theorem fundamentalDomain_adelicUnitary",
    role="Original general equality/nonzero domain endpoint; FV7 proves it in the CM unitary scope needed here")
add("quotient_pair", D + "Definitions/AutomorphicMembership/AdelicDataRowMeasureScaleTrivialTuple.lean", "def IsQuot")
add("quotient_positive_finite", IW + "QuotVolumeNeZeroNeTop.lean", "theorem quot_volume_ne_zero_ne_top")
for sid, anchor in [
    ("finite_pair", "structure FinPair"), ("quotient_measure", "def nuQ"),
    ("global_representative", "def Repr"), ("remaining_HolForm", "structure HolForm"),
]:
    add(sid, D + "Definitions/Divisors/IsSmoothVector.lean", anchor)
add("finite_pair_producer", DP + "ExistsFinPair.lean", "theorem exists_finPair")
add("all_open_finite_classes", IW + "FiniteClassSetHermitianUnitaryOpenLevel.lean", "theorem exists_finset_classes",
    role="Complete source open-level endpoint; FV9 proves it by checked Borel 5.1 plus explicit finite-index refinement")
add("actual_real_lift", DP + "ExistsArchimedeanLiftUnitaryGroupProduct.lean", "theorem exists_real_lift",
    role="Exact actual archimedean product/lift/Gram identity, already reconstructed by HCU14")
add("original_theta_extension", IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem exists_extension",
    role="Consumer: FV8 closes its hfin subargument; initial seed boundedness is a separate root task")
add("original_theta_activation", IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem firesAt",
    role="Consumer: same stored target and quantification after the chosen finite pairs")
add("remaining_initial_boundedness", IW + "BoundedOfSmoothCuspidalUniformModerate.lean",
    "theorem bounded_of_smooth_unifModGrowth",
    role="Retained source stronger universal boundedness statement; FV does not assert it")


def blocks(root, rel, ids, role):
    b = (root / rel).read_bytes()
    lines = b.splitlines(keepends=True)
    out = []
    for cid in ids:
        a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
        z = next(i for i in range(a + 1, len(lines)) if lines[i].strip() == ("% END " + cid).encode()) + 1
        block = b"".join(lines[a:z])
        out.append({"id": cid, "line_start": a + 1, "line_end": z, "sha256": sha(block),
                    "range_sha256": sha(block), "bytes": len(block)})
    return {"file": rel, "sha256": sha(b), "file_sha256": sha(b), "role": role, "claims": out}


inherited = [
    blocks(HUMAN, "holomorphic_uniqueness/main.tex", ["HCU14"],
           "Only used in FV10 to match the actual original CM-type archM/gramAt real coordinate maps; the general adelic and algebraic-group dictionary is independently proved in FV1-FV4."),
    blocks(HUMAN, "smooth_representatives/main.tex", ["SPR25"],
           "Only the final conditional two-gate assembly is referenced in FV11. FV supplies its finite-pair gate; no SPR Hilbert or Sobolev claim is used to prove finite volume."),
]

pub_url = "https://www.numdam.org/item/PMIHES_1963__16__5_0.pdf"
publication = {
    "author": "Armand Borel",
    "title": "Some finiteness properties of adele groups over number fields",
    "journal": "Publications mathematiques de l'IHES",
    "volume": 16, "year": 1963, "pages": "5-30",
    "doi": "10.1007/BF02684289",
    "url": pub_url,
    "record_url": "https://www.numdam.org/item/PMIHES_1963__16__5_0/",
    "primary_source_verified": True,
    "verification_method": "Primary digitized published paper inspected directly; setup 1.1-1.4 and statements 5.1, 5.5, 5.6(i).",
}
common_match = [
    {"hypothesis": "Ground field is a number field", "actual_object": "The same F in IsCMExt", "verification": "Explicit source typeclass hypothesis, retained unchanged", "source_ids": ["cm_extension"]},
    {"hypothesis": "Linear algebraic matrix group defined over F", "actual_object": "U(J) realized faithfully in GL_(2n) by multiplication on E^n", "verification": "FV1: closed polynomial equations, exact source A-points and inverse", "claims": ["FV1"]},
    {"hypothesis": "Adelic and rational groups use the published conventions", "actual_object": "HA(AF F,sigma,J) and HFinIn(AF F,sigma,J)", "verification": "FV4: finite free module topology, all local integral tests outside a finite set, same diagonal subgroup", "claims": ["FV4"]},
]
applications = [
    {
        "id": "FV_BOREL_55", "classification": "A", "status": "checked published application",
        "publication": publication, "theorem": "Lemma 5.5, final implication",
        "printed_pages": "20-21", "pdf_pages_zero_based": [16,17],
        "statement_paraphrase": "Trivial ground-field rational characters on the identity component imply adelic unimodularity.",
        "matched_hypotheses": common_match + [
            {"hypothesis": "X_F(G^0) is trivial", "actual_object": "The same U(J)", "verification": "FV2 gives G^0=G; FV3 proves character triviality by the exact CM involution", "claims": ["FV2","FV3"]}],
        "output": "Every original left Haar measure is right invariant.",
        "consumer_claims": ["FV5"], "all_hypotheses_checked": True,
    },
    {
        "id": "FV_BOREL_56I", "classification": "A", "status": "checked published application",
        "publication": publication, "theorem": "Theorem 5.6(i)",
        "printed_pages": "21", "pdf_pages_zero_based": [17],
        "statement_paraphrase": "The adelic quotient by principal rational points has finite nonzero invariant volume when the identity component has no ground-field rational character.",
        "matched_hypotheses": common_match + [
            {"hypothesis": "X_F(G^0) is trivial", "actual_object": "The same U(J)", "verification": "FV2-FV3; no anisotropy of U(J) is assumed", "claims": ["FV2","FV3"]}],
        "quotient_orientation": "Published G(A)/G(F) is carried to the original left quotient by inversion; FV5 checks the right action.",
        "normalization_transport": "FV6-FV7 independently transfer the result to every original Haar measure and every original a.e. fundamental domain.",
        "output": "Nonzero finite right-invariant quotient measure on the actual left quotient.",
        "consumer_claims": ["FV5"], "all_hypotheses_checked": True,
    },
    {
        "id": "FV_BOREL_51", "classification": "A", "status": "checked published application",
        "publication": publication, "theorem": "Theorem 5.1",
        "printed_pages": "19", "pdf_pages_zero_based": [15],
        "statement_paraphrase": "The standard integral adelic subgroup and principal rational group have finitely many double cosets.",
        "matched_hypotheses": common_match + [
            {"hypothesis": "Standard integral subgroup", "actual_object": "G_infinity times product_(v finite)(G(F_v) intersect r^-1 GL_(2n)(O_v))", "verification": "FV4 and FV9 identify the exact matrix realization and integral compact-open subgroups", "claims": ["FV4","FV9"]}],
        "output": "Finite source classes at K0; FV9 refines to every open K by finite index in K0.",
        "consumer_claims": ["FV9"], "all_hypotheses_checked": True,
    },
]
published = {"schema": "rh-published-applications/1", "component": "finite_volume", "version": "0.38",
             "source_commit": PIN, "applications": applications,
             "note": "A certificates are primary published applications with hypotheses matched. Remaining FV measure/topology and finite-level transports have independent written proofs. No new Lean replay."}
(HERE / "published_applications.json").write_text(json.dumps(published, indent=2, ensure_ascii=False) + "\n")

titles = {
    "FV1": "The exact unitary algebraic group",
    "FV2": "Geometric splitting and connected reductivity",
    "FV3": "Trivial ground-field rational characters",
    "FV4": "Exact adelic topology and rational subgroup",
    "FV5": "Checked Borel finite-volume and unimodularity application",
    "FV6": "An exact Borel fundamental domain",
    "FV7": "Finite volume for every original Haar fundamental domain",
    "FV8": "Complete original FiniteVolume2 and FinPair producers",
    "FV9": "Finite classes for every original open finite level",
    "FV10": "Exact real arithmetic components and function descent",
    "FV11": "One target finite-pair family before every theta parameter",
}
deps = {
    "FV1": [], "FV2": ["FV1"], "FV3": ["FV1","FV2"],
    "FV4": ["FV1"], "FV5": ["FV1","FV2","FV3","FV4"],
    "FV6": [], "FV7": ["FV6"], "FV8": ["FV4","FV5","FV6","FV7"],
    "FV9": ["FV1","FV4"], "FV10": ["FV1","FV2","FV3","FV4","FV9","HCU14"],
    "FV11": ["FV8","SPR25"],
}
classical = {"FV5": ["FV_BOREL_55","FV_BOREL_56I"], "FV9": ["FV_BOREL_51"]}
maps = {
    "FV1": ["cm_extension","hermitian_nondegenerate","tensor_involution","tensor_inclusion","tensor_gram",
            "unitary_subgroup","original_HA","unitary_equation","matrix_conjugate_transpose"],
    "FV2": ["cm_extension","hermitian_nondegenerate","unitary_equation","complete_finite_volume_contract"],
    "FV3": ["cm_extension","hermitian_nondegenerate","complete_finite_volume_contract"],
    "FV4": ["tensor_topology","tensor_measurability","original_HA","original_HA_matrix",
            "full_adele_algebra","finite_adele_algebra","infinite_adele_algebra","infinite_projection","finite_projection",
            "rational_image","rational_subgroup_generic","matrix_base_change","actual_group","actual_matrix",
            "actual_rational_subgroup","actual_finite_subgroup","actual_infinite_subgroup","actual_finHom","actual_infHom",
            "actual_lcsc","actual_rational_discrete"],
    "FV5": ["complete_finite_volume_contract","original_finite_volume","original_unimodularity"],
    "FV6": ["exact_Borel_section","general_domain","actual_domain"],
    "FV7": ["domain_measure_equality","actual_domain_measure","complete_finite_volume_contract"],
    "FV8": ["complete_finite_volume_contract","original_finite_volume","finite_pair","finite_pair_producer",
            "actual_CM_data","actual_CM_involution","actual_Hermitian_space","actual_Gram","actual_HSp",
            "actual_CM_Gram_producer","actual_Gram_nonsingular","actual_group","actual_rational_subgroup",
            "original_unimodular_domain","quotient_pair","quotient_positive_finite"],
    "FV9": ["all_open_finite_classes","rational_subgroup_generic","original_HA","finite_adele_algebra"],
    "FV10": ["all_open_finite_classes","actual_automorphic_function","actual_real_lift","actual_gramAt",
             "actual_finite_subgroup","actual_infinite_subgroup","actual_finHom","actual_infHom"],
    "FV11": ["finite_pair","finite_pair_producer","quotient_measure","global_representative",
             "original_theta_extension","original_theta_activation","remaining_HolForm","remaining_initial_boundedness"],
}
scopes = {
    "FV1": "Every number-field IsCMExt and every original nondegenerate Hermitian J; exact A-points for every commutative F-algebra. No replacement group or isogeny.",
    "FV2": "The same G becomes GL_n over E by an explicit two-factor formula; n=0 is treated separately and included.",
    "FV3": "Every algebraic character defined over F on the actual connected G is trivial; no claim about all continuous adelic characters.",
    "FV4": "Exact moduleTopology/Borel structure and diagonal HFinIn at full, finite and infinite adele algebras; lcsc, countable discrete closed rational subgroup.",
    "FV5": "Borel 5.5 and 5.6(i) with all hypotheses checked on the same G; right quotient to left quotient by inversion; finite invariant volume, not compactness.",
    "FV6": "Every lcsc Hausdorff group and countable discrete closed subgroup; one Borel exact transversal valid for every Haar measure, with a Borel quotient section.",
    "FV7": "Every supplied left Haar and every original a.e. fundamental domain, given unimodularity and finite nonzero invariant quotient measure. Exact original scale retained.",
    "FV8": "Entire universal FiniteVolume2, followed by every original D,V and any original Haar measure; produces literal FinPair and positive finite volume for every IsQuot pair.",
    "FV9": "Every original IsCMExt/HermND and every open finite K, without a compactness hypothesis; S chosen after K before all g.",
    "FV10": "For compact-open finite K, each exact Gamma_s is arithmetic in Res_F/Q U(J), discrete, with original real matrices and function descent. Original open U permits a compact-open sublevel. No arithmetic claim for arbitrary noncompact open K.",
    "FV11": "For the stored targets W_i choose one mu_i,fd_i before all t,x,coefficients and functions. Only the finite-pair gate is closed; initial boundedness and common datum production remain separate.",
}
assert set(titles) == set(deps) == set(maps) == set(scopes)
incoming = {x["id"] for f in inherited for x in f["claims"]}
assert all(x in titles or x in incoming for ds in deps.values() for x in ds)
assert all(x in sources for ss in maps.values() for x in ss)
tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i in range(a + 1, len(lines)) if lines[i].strip() == ("% END " + cid).encode()) + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.38",
        "classification": "A" if cid == "FV5" else "B",
        "status": "complete checked published application" if cid == "FV5" else "complete independent human proof in the stated original-data scope",
        "depends_on": deps[cid], "classical_inputs": classical.get(cid, []),
        "quantifier_scope": scopes[cid],
        "proof_location": {"file": "finite_volume/main.tex", "label": "claim:" + cid,
                           "line_start": a + 1, "line_end": z, "sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[s] for s in maps[cid]],
    })
remaining = [
    {"id": "FV_INITIAL_SEED_BOUNDEDNESS", "classification": "C",
     "status": "separate root producer; not proved by this packet",
     "contract": "For every actual initial seed on the same target and its parameters, prove a bound before all adelic g. FV10 supplies the exact finite arithmetic-component dictionary; central finiteness, cusp descent and any rapid-decay application belong to the root seed packet.",
     "source_ids": ["remaining_HolForm","remaining_initial_boundedness","original_theta_extension"],
     "not_new_independent_top_level_obligation": True},
    {"id": "FV_ORIGINAL_COMMON_DATA", "classification": "C",
     "status": "retained original common producer",
     "contract": "Supply the selected same Bundle/RealDat, fields, models, readings and rational tests. FV proves a universal volume theorem and does not construct that datum.",
     "source_ids": ["original_theta_activation"],
     "not_new_independent_top_level_obligation": True},
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.38", "date": "2026-11-22",
    "component": "finite_volume", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
                         "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "published_applications": {"file": "published_applications.json", "sha256": sha((HERE / "published_applications.json").read_bytes()),
                               "certificate_ids": [a["id"] for a in applications]},
    "remaining_producer_contracts": remaining,
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
                   "source_ranges": len(sources), "claim_source_occurrences": sum(map(len, maps.values())),
                   "all_source_ranges_exact": True, "all_inherited_claim_edges_explicit": True,
                   "all_published_hypotheses_matched": True, "new_lean_build": False,
                   "tex_validation": "See validation/validation.json: offline draft syntax/layout only."},
    "scope_note": "Full FiniteVolume2 and literal target FinPair producer, plus full finite open-level classes and compact-open real arithmetic components. No seed boundedness, common datum construction, or Lean replay.",
}
(HERE / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n")
closure = {
    "schema": "rh-component-closure/1", "version": "0.38", "component": "finite_volume", "source_commit": PIN,
    "main_tex_sha256": sha(tex), "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles), "claim_count": len(titles), "class_counts": {"A": 1, "B": 10, "C": 0, "D": 0},
    "published_application_certificate_ids": [a["id"] for a in applications],
    "closed_subtargets": [
        {"id": "FV_FULL_FINITE_VOLUME", "claims": ["FV1","FV2","FV3","FV4","FV5","FV6","FV7","FV8"],
         "contract": "Entire original FiniteVolume2: every IsCMExt, every HermND matrix, every Haar measure, every original a.e. fundamental domain has finite measure."},
        {"id": "FV_ACTUAL_FINITE_PAIR", "claims": ["FV8","FV11"],
         "contract": "Every original D,V admits literal FinPair; stored W_i admit one family mu_i,fd_i chosen before every t,x."},
        {"id": "FV_ORIGINAL_FINITE_CLASSES", "claims": ["FV9"],
         "contract": "Entire original exists_finset_classes at every open finite level; no compactness assumption needed for this endpoint."},
        {"id": "FV_REAL_ARITHMETIC_COMPONENTS", "claims": ["FV10"],
         "contract": "For compact-open K, exact Gamma_s arithmetic/discrete in Res_F/Q U(J), exact original real product and compact center, and phi_s(u)=phi(su) descent. Every original open U supplies such a sublevel."},
    ],
    "same_object_sufficient_rule": {
        "universals": "Every original D,V; independently of theta, RealDat parameters, coefficients and seed function.",
        "choice_order": ["D and the stored target family W_i", "one original Haar mu_i and one original fundamental domain fd_i for each i", "all theta t, finite translations x, coefficient vectors and functions"],
        "output": "forall i, FinPair(W_i,mu_i,fd_i), with literal nuQ and no change of normalization.",
        "remaining_separate_input": "Actual initial seed boundedness on the same targets, supplied by the separate root packet if completed.",
        "no_new_parameter_threshold": True,
    },
    "selected_route_effect": {
        "original_parent_node": "BASE_THETA_CUSPIDAL_EXTENSION",
        "closed_residue": "All actual target FinPair production; full FiniteVolume2 also available to other retained original consumers.",
        "parent_status_from_this_component_alone": "Initial boundedness and the selected same original datum remain separate; this packet does not claim full base-theta or RH/GRH closure.",
        "source_fully_checked_assumed": True, "new_lean_replay": False,
    },
    "retained_producers": remaining,
    "not_claimed": ["The stronger universal CuspRapidDecay statement", "Initial seed boundedness or central finiteness",
                    "Compactness of an isotropic adelic unitary quotient",
                    "Arithmetic of Gamma_s for merely open noncompact K",
                    "Construction of the common selected datum/readings/rational tests",
                    "A new Lean replay or full RH/GRH conclusion"],
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
loc = ["FV source locators — v0.38", "Pin: " + PIN,
       "Inclusive ranges; every source file equals its pinned Git blob.",
       "Published hypotheses are checked in published_applications.json.",
       "Source declaration names are locators, not substitutes for proofs. No Lean replay.", ""]
for cid in titles:
    loc.extend([cid + ": " + titles[cid], "  Proof dependencies: " + (", ".join(deps[cid]) or "none beyond stated standard background"),
                "  Published certificates: " + (", ".join(classical.get(cid, [])) or "none")])
    for sid in maps[cid]:
        s = sources[sid]
        loc.extend([f"  {sid}: {s['path']}:{s['line_start']}-{s['line_end']} [{s['declaration']}]",
                    "    file_sha256=" + s["file_sha256"] + " range_sha256=" + s["range_sha256"], "    " + s["url"]])
    loc.append("")
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
report = f"""FV — original finite volume and finite components, v0.38

Source: {REPO}
Pin: {PIN}
Formal correctness is assumed. No Lean build or replay was performed.

RESULT
Eleven complete claims: FV1-FV11 (one A and ten B).
The entire source FiniteVolume2 is proved, not only existence of one
finite target pair. The literal exists_finPair and positive/finite
quotient-volume endpoints follow. One family of pairs is chosen for
the stored W_i before every theta parameter t, finite translation x,
coefficient vector, or seed function.

PUBLISHED APPLICATIONS
Borel, Some finiteness properties of adele groups over number fields,
Publ. Math. IHES 16 (1963), 5-30. Primary source:
{pub_url}
Checked Lemma 5.5 and Theorem 5.6(i), printed pp.20-21, and Theorem 5.1,
printed p.19. FV1-FV4 prove the precise algebraic/adelic/rational
dictionary and the absence of F-defined rational characters. All
hypotheses are recorded in published_applications.json.

INDEPENDENT BRIDGES
The algebraic unitary group becomes GL_n over the CM field. The
involution inverts determinant characters, forcing every F-defined
character to be trivial. Finite free tensor coordinates and local
integral tests identify the source module topology with the published
restricted-product topology, and identify the rational subgroup exactly.
FV6 constructs a Borel exact transversal by the first chart met by an
orbit. FV7 lifts the finite quotient measure by counting each rational
fiber, proves local finiteness using |Gamma intersect C C^-1|, invokes
basic Haar uniqueness, and explicitly transfers to every original
Haar measure and every a.e. fundamental domain. No quotient integration
or additional finite-volume theorem is silently assumed.

FINITE COMPONENTS
Borel 5.1 followed by finite-index refinement gives every original
open finite-level class cover. For a compact-open K, the exact
Gamma_s is commensurable with the integral matrix subgroup of
Res_(F/Q) U(J), hence arithmetic; its real projection is discrete
by compactness in the finite factor. The original real matrices,
compact center, and phi_s(u)=phi(su) descent are checked. An arbitrary
original open U supplies a compact-open finite sublevel. The arithmetic
assertion is not made for a merely open noncompact K.

RETAINED
Initial boundedness of the actual seed belongs to the separate root
producer. The selected Bundle/RealDat/readings/rational tests remain
separate original inputs. No universal CuspRapidDecay theorem or
compactness of an isotropic quotient is claimed.

VALIDATION
{len(cache)} source files equal pinned Git blobs; {len(sources)} distinct source ranges;
{sum(map(len, maps.values()))} claim-source occurrences; 11 exact proof blocks.
Only HCU14 and SPR25 are inherited proof edges, in their explicitly
limited roles. Three published application certificates have every
hypothesis matched. Standalone syntax/layout validation is separate
in validation/validation.json; no PDF and no Lean replay.

HASHES
main.tex {sha(tex)}
provenance.json {sha((HERE / "provenance.json").read_bytes())}
closure.json {sha((HERE / "closure.json").read_bytes())}
published_applications.json {sha((HERE / "published_applications.json").read_bytes())}
"""
(HERE / "report.txt").write_text(report)
print(json.dumps({"main": sha(tex), "provenance": sha((HERE / "provenance.json").read_bytes()),
                  "closure": sha((HERE / "closure.json").read_bytes()), "claims": len(claims),
                  "source_files": len(cache), "source_ranges": len(sources),
                  "claim_source_occurrences": sum(map(len, maps.values()))}, indent=2))
