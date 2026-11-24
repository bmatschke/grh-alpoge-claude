#!/usr/bin/env python3
"""Rebuild ASB source/proof certificates without invoking Lean.

Portable invocation:
  python3 build_metadata.py --source /path/to/pinned/checkout \
      --human-root /path/to/reconstruction --peer-root /path/to/reconstruction

In a release both human-root and peer-root are the release root.  During
drafting human-root is reconstruction_v036 and peer-root is work_v037.
Ranges are inclusive and retain original newline bytes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "canonical_weil").exists() else HERE.parent.parent / "reconstruction_v036"
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--source", type=Path, default=HERE.parent.parent / "lean_source")
p.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
p.add_argument("--peer-root", type=Path, default=HERE.parent)
args = p.parse_args()
SOURCE, HUMAN, PEER = args.source.resolve(), args.human_root.resolve(), args.peer_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}


def add(sid, path, anchor, stop=None, role="Exact original definition, contract or argument independently reconstructed in the stated scope"):
    anchor = anchor.rstrip()
    path = "src/" + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    anchor_re = re.compile(re.escape(anchor) + r"(?=$|[\s:({])")
    hits = [i for i, line in enumerate(lines) if anchor_re.search(line)]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    z = next((i for i in range(a + 1, len(lines)) if (stop in lines[i] if stop else decl.match(lines[i]))), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid, "path": path, "declaration": anchor, "declaration_anchor": anchor,
        "line_start": a + 1, "line_end": z, "sha256": sha(b), "file_sha256": sha(b),
        "range_sha256": sha(block), "range_bytes": len(block), "first_line": lines[a].rstrip(),
        "role": role, "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a + 1}-L{z}",
    }


D = "Development/AbelianVarietyTheory/"
DP = D + "Proofs/DivisorProofs/"
FM = D + "Proofs/FlagMeasures/"
HP = D + "Proofs/HeightProofs/"
IW = D + "Proofs/IwasawaDecomposition/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
REST = "Retained original datum or downstream consumer; ASB does not produce this input"

for sid, anchor in [
    ("original_group", "abbrev GA"), ("original_matrix", "def matHom"),
    ("infinite_component", "def infHom"), ("finite_component", "def finHom"),
    ("finite_subgroup", "def GfC"), ("infinite_subgroup", "def GinfC"),
    ("rational_subgroup", "def GQ"), ("original_inf_family", "def IsInfFam"),
    ("actual_one_place_spec", "def IsAtTau"), ("automorphic_function", "structure IsAutFun"),
]:
    add(sid, BT + "IsAutFunDef.lean", anchor)
for sid, anchor in [
    ("actual_atTau", "def atTau"), ("actual_lie", "def lieAt"),
    ("actual_oneP", "def oneP"), ("actual_Rder", "def Rder"),
    ("actual_normInf", "def normInf"), ("actual_smooth_automorphic", "structure IsAutFunSm"),
]:
    add(sid, BT + "TiedSmooth.lean", anchor)
add("original_archM", "Formalism/LocalToGlobal/ProjectiveLattices/EquivariantFiniteGroup.lean", "def archM")
add("original_gramAt", IR + "RealSeparation/IsRealPtO.lean", "def gramAt")
add("actual_real_lift", DP + "ExistsArchimedeanLiftUnitaryGroupProduct.lean", "theorem exists_real_lift",
    role="Exact same-object real component/lift/decomposition contract already reconstructed by inherited HCU14")

LOC = DP + "LocalSobolevInequalityAdelicUnitary.lean"
for sid, anchor in [
    ("local_adjoint", "def adj"), ("exponential_unitary", "theorem exp_mem"),
    ("one_place_unitary", "theorem mulSingle_mem"), ("adjoint_inverse", "theorem adj_mul_self"),
    ("adjoint_lie", "theorem adj_eq_neg_iff"), ("one_place_basis", "theorem exists_basis"),
    ("real_chart", "theorem exists_chart"), ("continuous_arch", "theorem continuous_arch"),
    ("original_oneP_laws", "theorem oneP_spec"), ("word_finite_invariance", "theorem foldr_inv"),
    ("word_smoothness", "theorem foldr_smooth"), ("adelic_chart", "theorem exists_adelic_chart"),
    ("local_sobolev", "theorem local_sobolev"),
]:
    add(sid, LOC, anchor)
add("second_kind_coordinates", DP + "UnitaryGroupSecondKindCoordinatesNearOne.lean", "theorem second_kind_chart",
    role="Original uniform shifted second-kind coordinate interface; ASB2 proves its actual nondegenerate Hermitian matrix instance by an explicit Cayley chart")
for sid, anchor in [
    ("expanding_volume", "theorem volume_le_mul_volume_image_of_expanding"),
    ("expanding_integral", "theorem setIntegral_le_of_expanding"),
]:
    add(sid, DP + "SetIntegralLeOfExpanding.lean", anchor)
add("left_Haar_comparison", DP + "LeMulSetIntegralImage2OfForallLe.lean", "theorem le_mul_setIntegral_image2_of_forall_le")
add("one_variable_Sobolev", FM + "SqIntervalIntegralLeMulIntervalIntegralSq.lean", "theorem sobolev_endpoint_one_variable")
add("cube_last_coordinate", FM + "SobolevIteratedOneParameterSubgroups.lean", "theorem integral_cube_succ_last")
add("ordered_word_Sobolev", DP + "SobolevIteratedOneParameterSubgroupsWords.lean", "theorem sobolev_iterated_one_parameter_subgroups_words")

COUNT = DP + "NcardRationalPointsTranslatedCompactLePow.lean"
for sid, anchor in [
    ("finite_algebraic_denominator", "theorem exists_nat_den"),
    ("compact_finite_denominator", "theorem exists_den_of_isCompact"),
    ("compact_tensor_denominator", "theorem exists_den_of_isCompact_tensor"),
    ("integral_coordinates_house", "theorem exists_repr_le_house"),
    ("integer_matrix_count", "theorem count_matrices"),
    ("normInf_inverse", "theorem normInf_inv"),
    ("normInf_nonnegative", "theorem normInf_nonneg"),
    ("normInf_continuous", "theorem continuous_normInf"),
    ("normInf_positive_rank", "theorem one_le_normInf"),
    ("rational_house_bound", "theorem house_le_normInf"),
    ("rational_point_count", "theorem ncard_rational_le"),
]:
    add(sid, COUNT, anchor)
add("entry_sum_product", HP + "NormInfSubmultiplicativeLeAdelicHeight.lean", "theorem entrySum_mul_le")
add("normInf_product", HP + "NormInfSubmultiplicativeLeAdelicHeight.lean", "theorem normInf_mul_le_and_le_height",
    role="ASB11 proves only the submultiplicative first conclusion, independently of the adelic-height comparison")
add("actual_CM_type_places", HP + "CmTypeRestrictRealSubfieldInfinitePlaceBijective.lean", "theorem mk_tauE_bijective",
    role="Exact source CM-type/absolute-place dictionary, inherited human reconstruction HCU14")

for sid, anchor in [
    ("finite_pair", "structure FinPair"), ("quotient_measure", "def nuQ"),
    ("global_representative", "def Repr"), ("regular_action", "structure IsReg"),
    ("original_smooth_vector", "def IsSmoothVector'"), ("original_Hilbert_derivative", "def dL2"),
]:
    add(sid, D + "Definitions/Divisors/IsSmoothVector.lean", anchor)
GROW = DP + "SobolevBoundForSmoothVectors.lean"
for sid, anchor in [
    ("nonnegative_unfolding_count", "theorem lintegral_le_of_count"),
    ("L2_integral_norm", "theorem lintegral_enorm_sq"),
    ("sum_square_bound", "theorem sum_sq_le"),
    ("L2_count_comparison", "theorem integral_le_of_count"),
    ("sum_to_norm_bound", "theorem le_of_sums"),
    ("actual_adelic_L2_comparison", "theorem integral_le_adelic"),
    ("same_level_from_representative", "theorem level_of_repr"),
    ("uniform_pointwise_growth", "theorem pointwise_growth"),
]:
    add(sid, GROW, anchor)
add("scalar_evaluation_consumer", DP + "SmoothVectorAutomorphicDerivatives.lean", "theorem exists_eval",
    role="Original consumer of ASB4's scalar cube/Haar comparison, independently reconstructed by companion SPR")
add("generic_smooth_representative", DP + "SmoothVectorAutomorphicDerivatives.lean", "theorem exists_smooth_rep",
    role="Original generic consumer of the exact scalar comparison; companion SPR owns the representative construction")
add("actual_smooth_representative", DP + "SmoothVectorAutomorphicDerivatives.lean", "theorem exists_smooth_repr",
    role="Incoming companion SPR13 endpoint; no later SPR multiplicity-map theorem is used by ASB14")
add("remaining_actual_volume", IW + "FiniteVolumeAdelicUnitaryQuotient.lean", "theorem finVol", role=REST)
add("remaining_boundedness", IW + "BoundedOfSmoothCuspidalUniformModerate.lean", "theorem bounded_of_smooth_unifModGrowth", role=REST)
add("full_theta_extension", IW + "ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem exists_extension", role=REST)

titles = {
    "ASB1": "Actual real coordinates and one-place Lie basis",
    "ASB2": "Uniformly controlled shifted second-kind coordinates",
    "ASB3": "Full original adelic chart on one open level",
    "ASB4": "Scalar cube-to-left-Haar comparison",
    "ASB5": "Ordered-word endpoint Sobolev inequality",
    "ASB6": "Complete original local Sobolev inequality",
    "ASB7": "One denominator for a finite-adelic compact set",
    "ASB8": "Exact original tensor-product denominator",
    "ASB9": "Integral coordinates bounded by the actual house",
    "ASB10": "Complete polynomial counting of integral-denominator matrices",
    "ASB11": "Precise original normInf estimates",
    "ASB12": "Full quantitative rational-point multiplicity bound",
    "ASB13": "Exact multiplicity-to-L2 unfolding",
    "ASB14": "One exponent and one word list before every vector",
}
maps = {
    "ASB1": ["original_group","original_inf_family","original_archM","original_gramAt","actual_real_lift",
        "finite_subgroup","infinite_subgroup","actual_atTau","actual_one_place_spec","actual_lie","actual_oneP",
        "exponential_unitary","one_place_unitary","one_place_basis","original_oneP_laws","continuous_arch"],
    "ASB2": ["local_adjoint","adjoint_inverse","adjoint_lie","real_chart","second_kind_coordinates"],
    "ASB3": ["adelic_chart","actual_real_lift","actual_oneP","finite_subgroup","infinite_subgroup"],
    "ASB4": ["expanding_volume","expanding_integral","left_Haar_comparison","scalar_evaluation_consumer","generic_smooth_representative"],
    "ASB5": ["one_variable_Sobolev","cube_last_coordinate","ordered_word_Sobolev"],
    "ASB6": ["local_sobolev","word_finite_invariance","word_smoothness","actual_Rder","actual_oneP"],
    "ASB7": ["finite_algebraic_denominator","compact_finite_denominator"],
    "ASB8": ["compact_tensor_denominator","finite_algebraic_denominator"],
    "ASB9": ["integral_coordinates_house"],
    "ASB10": ["integer_matrix_count","integral_coordinates_house"],
    "ASB11": ["actual_normInf","normInf_inverse","normInf_nonnegative","normInf_continuous",
        "normInf_positive_rank","rational_house_bound","entry_sum_product","normInf_product","actual_CM_type_places","original_inf_family"],
    "ASB12": ["rational_point_count","compact_tensor_denominator","integer_matrix_count","finite_component",
        "infinite_subgroup","original_matrix","rational_subgroup"],
    "ASB13": ["finite_pair","quotient_measure","global_representative","nonnegative_unfolding_count",
        "L2_integral_norm","L2_count_comparison","actual_adelic_L2_comparison"],
    "ASB14": ["uniform_pointwise_growth","actual_smooth_representative","regular_action","original_smooth_vector",
        "original_Hilbert_derivative","global_representative","same_level_from_representative",
        "sum_square_bound","sum_to_norm_bound","local_sobolev","rational_point_count"],
}
deps = {
    "ASB1": ["HCU14","RQC1"], "ASB2": ["ASB1"], "ASB3": ["ASB1","ASB2"],
    "ASB4": ["ASB3","RQC1"], "ASB5": [],
    "ASB6": ["ASB1","ASB2","ASB3","ASB4","ASB5"],
    "ASB7": [], "ASB8": ["ASB7"], "ASB9": ["ASB8"], "ASB10": ["ASB9"],
    "ASB11": ["HCU14"], "ASB12": ["ASB8","ASB10","ASB11","RQC1"],
    "ASB13": ["RQC2"], "ASB14": ["ASB6","ASB12","ASB13","SPR13","HCU16","RQC6"],
}
scopes = {
    "ASB1": "Any original D,theta,V with IsInfFam; exact archM/gramAt/atTau/oneP and finite-infinite decomposition. One finite concatenated one-place Lie basis; rank zero included.",
    "ASB2": "Same original nondegenerate Hermitian matrix group. Constants r,s>0,R>0,K>=1 and a real neighborhood precede every v; one f_v on the full cube with uniform image bound and inverse Lipschitz bound. No global real chart asserted.",
    "ASB3": "For every supplied open subgroup U of the original adelic group, one actual finite ordered chart and W precede x; for each x one a_x in U intersect Gf independent of t and one f_x satisfy the full literal source identity and uniform inequalities.",
    "ASB4": "Same fixed D,theta,V,U and arbitrary original left Haar measure. One compact Omega and C>=0 before EVERY continuous nonnegative right-U-intersect-Gf-invariant scalar function. Uses only left Haar invariance, with the source cube/product/measure unchanged.",
    "ASB5": "Any continuous one-parameter subgroups in a topological group, all continuous word functions with the actual prepend derivative law. Full cube bounds through word length r imply the endpoint bound with direct constant (2/s+2s)^r; no curve/operator commutation.",
    "ASB6": "Exactly original local_sobolev hypotheses. One finite list of admissible original right-fold words, compact Omega and C>=0 before every psi and y; all-product smoothness, word continuity and same supplied finite level retained.",
    "ASB7": "Every compact subset of the finite adeles of an arbitrary number field. One positive rational-integer denominator for the whole compact set, hence all its rational points; no discreteness assertion without archimedean control.",
    "ASB8": "Every compact subset of the original Af(F0) tensor_F0 E0 with its specified finite free module topology. One positive denominator before every rational tensor point.",
    "ASB9": "Any number field and any fixed integral basis, including the source basis; one coordinate constant before every algebraic integer. Actual house is the maximum of all complex embedding norms.",
    "ASB10": "Every number field E0 and matrix size n. b=[E0:Q] n^2 before every positive integer denominator m, then C_m before all R>=1. Finiteness and cardinal bound both proved, including n=0.",
    "ASB11": "Exactly original normInf. Continuity, nonnegativity, inverse and product bounds; positivity only for n>0; original rational-entry house comparison via the actual CM-type index dictionary. No equivalent height substituted.",
    "ASB12": "For every original compact Omega choose N=2[E:Q] n^2 before x, then C_x>=0 before EVERY u in Ginf and y. Denominator depends only on x and Omega, never on u/y; auxiliary rational base point changes only the injection. Full finite-set and cardinal conclusions, rank zero included.",
    "ASB13": "Same FinPair/Haar/fundamental domain/quotient measure and global-AE Repr. Uniform finite rational multiplicity bound M before all y yields exact original integral bound M^2 ||F||^2; no normalized or replacement measure.",
    "ASB14": "Fixed original D,theta,V, same FinPair, any IsReg and one open U: choose ONE N and list S; then for each x choose C_x before F,psi,u. IsSmoothVector', U-intersect-Gf fixedness, continuous global Repr and u in Ginf are the literal inputs. Incoming SPR13 only; later MMap construction not used.",
}
assert set(titles) == set(maps) == set(deps) == set(scopes)
assert all(s in sources for ss in maps.values() for s in ss)


def human_blocks(root, rel, ids, role):
    b = (root / rel).read_bytes()
    lines = b.splitlines(keepends=True)
    out = []
    for cid in ids:
        begin, end = ("% BEGIN " + cid).encode(), ("% END " + cid).encode()
        hits = [i for i, line in enumerate(lines) if line.strip() == begin]
        if hits:
            assert len(hits) == 1
            a = hits[0]
            z = next(i for i in range(a + 1, len(lines)) if lines[i].strip() == end) + 1
        else:
            pat = ("\\paragraph{" + cid + ":").encode()
            hits = [i for i, line in enumerate(lines) if line.startswith(pat)]
            assert len(hits) == 1, (rel, cid, hits)
            a = hits[0]
            z = next((i for i in range(a + 1, len(lines)) if lines[i].startswith(b"\\paragraph{")), len(lines))
            while z > a and not lines[z - 1].strip():
                z -= 1
        block = b"".join(lines[a:z])
        out.append({"id": cid, "line_start": a + 1, "line_end": z,
            "sha256": sha(block), "range_sha256": sha(block), "bytes": len(block)})
    return {"file": rel, "sha256": sha(b), "file_sha256": sha(b), "role": role, "claims": out}


inherited = [
    human_blocks(HUMAN, "holomorphic_uniqueness/main.tex", ["HCU14","HCU16"],
        "Incoming human proofs: exact original real lift/CM-type dictionary and uniqueness of continuous global-AE representatives."),
    human_blocks(HUMAN, "regular_quotient/main.tex", ["RQC1","RQC2","RQC6"],
        "Incoming human proofs: original locally compact second-countable topology, countable same-domain unfolding, and any original regular action."),
    human_blocks(PEER, "smooth_representatives/main.tex", ["SPR13"],
        "Same-iteration incoming endpoint ONLY for ASB14: one original smooth representative, same U-intersect-Gf level and all ordered derivative identities. SPR13 uses ASB3/4; it does not use ASB14. No later SPR MMap edge."),
]
incoming_ids = {b["id"] for r in inherited for b in r["claims"]}
assert all(d in titles or d in incoming_ids for ds in deps.values() for d in ds)
tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i, line in enumerate(lines) if line.strip() == ("% END " + cid).encode()) + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": title, "introduced_in": "0.37", "classification": "B",
        "status": "complete independent human proof of the explicitly stated original-data implication",
        "depends_on": deps[cid], "quantifier_scope": scopes[cid],
        "proof_location": {"file": "adelic_sobolev/main.tex", "label": "claim:" + cid,
            "line_start": a + 1, "line_end": z, "sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[s] for s in maps[cid]],
    })

remaining = [
    {"id": "ASB_ACTUAL_FINITE_PAIR", "classification": "C", "status": "retained upstream original producer",
     "contract": "Produce the finite target FinPair for the SAME original target V. ASB13/14 use its original Haar measure, finite fundamental domain and quotient measure; they do not prove actual finite volume.",
     "source_ids": ["finite_pair","remaining_actual_volume"], "not_new_independent_top_level_obligation": True},
    {"id": "ASB_INITIAL_THETA_BOUNDEDNESS", "classification": "C", "status": "retained upstream original producer",
     "contract": "Prove boundedness of the actual initial HolForm/theta integral on the SAME target. Pointwise Sobolev bounds for supplied L2 smooth vectors do not establish this initial boundedness or L2 membership.",
     "source_ids": ["remaining_boundedness","full_theta_extension"], "not_new_independent_top_level_obligation": True},
    {"id": "ASB_ORIGINAL_COMMON_DATA", "classification": "C", "status": "retained upstream original producer",
     "contract": "Produce the selected same Bundle/RealDat and its exact field/model/readings/rational-test packet. The Sobolev producer is universal on the supplied original D,theta,V and is not a construction of that selected datum.",
     "source_ids": ["original_group","original_inf_family","full_theta_extension"], "not_new_independent_top_level_obligation": True},
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.37", "date": "2026-11-22",
    "component": "adelic_sobolev", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
        "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --peer-root /path/to/reconstruction"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "remaining_producer_contracts": remaining,
    "dependency_order": ["ASB1-ASB4", "SPR13", "ASB14", "later original MMap installation"],
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
        "source_ranges": len(sources), "claim_source_occurrences": sum(map(len, maps.values())),
        "all_source_ranges_exact": True, "all_inherited_claim_edges_explicit": True,
        "new_lean_build": False, "tex_validation": "See validation/validation.json; draft syntax/layout only."},
    "scope_note": "All three original conditional endpoints are reconstructed: actual chart/local Sobolev, quantitative rational-point count, and fixed-level pointwise growth. ASB14 consumes only companion SPR13. Actual initial boundedness and target FinPair remain separate producers. Formal correctness is accepted; no Lean replay.",
}
(HERE / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n")
closure = {
    "schema": "rh-component-closure/1", "version": "0.37", "component": "adelic_sobolev",
    "source_commit": PIN, "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles), "claim_count": len(titles),
    "class_counts": {"A": 0, "B": len(titles), "C": 0, "D": 0},
    "all_new_claims_are_conditional_implications": True,
    "closed_subtargets": [
        {"id": "ASB_ORIGINAL_CHART_COMPARISON", "claims": ["ASB1","ASB2","ASB3","ASB4"],
         "contract": "Full original exists_adelic_chart and exact scalar cube-to-left-Haar comparison; one finite a_x independent of cube parameter, uniform inverse-Lipschitz bound, original ordered oneP product."},
        {"id": "ASB_ORIGINAL_LOCAL_SOBOLEV", "claims": ["ASB5","ASB6"],
         "contract": "Entire source local_sobolev on precisely its supplied smoothness/continuity/level hypotheses. Finite admissible word list and compact set chosen before every psi and y."},
        {"id": "ASB_ORIGINAL_RATIONAL_COUNT", "claims": ["ASB7","ASB8","ASB9","ASB10","ASB11","ASB12"],
         "contract": "Entire source ncard_rational_le: finite sets and count <= C_x normInf(u)^N with explicit N=2[E:Q]n^2 before x; denominator before u,y; rank-zero case included."},
        {"id": "ASB_ORIGINAL_POINTWISE_GROWTH", "claims": ["ASB13","ASB14"], "incoming_peer_claims": ["SPR13"],
         "contract": "Entire source pointwise_growth with one N/list S before x,F,psi,u on the SAME FinPair/IsReg/open level; original Repr and right-fold derivative words, no new MMap premise."},
    ],
    "same_object_sufficient_rule": {
        "universals": "Every original D, theta:InfFam D, V:HSp D with IsInfFam(theta), same supplied FinPair(V,mu,fd), any original IsReg(rho), and any open subgroup U.",
        "incoming_peer_endpoint": "SPR13 on exactly these objects, used only by ASB14.",
        "choice_order": ["D,theta,V,mu,fd,rho,U", "ONE natural N and ONE finite admissible word list S", "x then C_x", "F,psi and u"],
        "vector_inputs": ["IsSmoothVector'(theta,V,rho,F)", "forall k in U intersect Gf, rho(k)F=F", "Continuous psi", "global Repr(F,psi)", "u in Ginf"],
        "output": "|psi(x*u)| <= C_x * normInf(theta,V,u)^N * sum_{l in S} ||foldr dL2 l F||",
        "explicit_admissible_exponent": "N = 2 * [D.host.E:Q] * V.rank^2",
        "acyclic_order": "ASB1-4 -> SPR13 -> ASB14 -> later SPR MMap installation; no later SPR theorem feeds back into ASB.",
        "no_extra_producers_inside_rule": True,
    },
    "selected_route_effect": {
        "original_parent_node": "BASE_THETA_CUSPIDAL_EXTENSION",
        "closed_residue": "Actual fixed-level chart/local Sobolev, complete quantitative rational count and all-vector uniform pointwise growth, conditional on the supplied original finite pair and companion smooth representative theorem.",
        "parent_status_after_this_component": "still conditional on initial boundedness, actual target FinPair and exact common selected datum; later MMap installation belongs to companion SPR",
        "new_threshold": False, "new_independent_original_datum": False,
        "source_fully_checked_assumed": True,
    },
    "retained_producers": remaining,
    "not_claimed": ["Production of the actual target FinPair or initial theta boundedness",
        "A uniform exponent across changed levels, targets or parameter-dependent initial data",
        "Unconditional construction of the selected Bundle or its readings/rational tests",
        "A new Lean replay or full RH/GRH conclusion"],
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
loc = [
    "ASB source locators — v0.37", "Pin: " + PIN,
    "Inclusive ranges; file and range SHA256 checked against pinned git blobs.",
    "No Lean replay. Source names are locators, not substitutes for human proofs.", "",
]
for cid in titles:
    loc.append(cid + ": " + titles[cid])
    loc.append("  Proof dependencies: " + (", ".join(deps[cid]) or "none beyond stated ordinary background and inputs"))
    for sid in maps[cid]:
        s = sources[sid]
        loc += [f"  {sid}: {s['path']}:{s['line_start']}–{s['line_end']} [{s['declaration'].strip()}]",
            "    file_sha256=" + s["file_sha256"] + " range_sha256=" + s["range_sha256"],
            "    " + s["url"]]
    loc.append("")
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
report = f"""ASB — original adelic Sobolev producer, v0.37

Source: {REPO}
Pin: {PIN}
Formal correctness is assumed. No Lean build or replay was performed.

RESULT
Fourteen complete human proof claims, ASB1–ASB14, classified B.
The component reconstructs all three assigned original conditional
endpoints: LocalSobolevInequalityAdelicUnitary.local_sobolev,
RatCount.ncard_rational_le, and SobolevGrowth.pointwise_growth.
Its geometric input is the inherited exact HCU14 real lift; its global
growth implication consumes companion SPR13 on the same supplied FinPair.

ACTUAL CHART AND COMPARISON
ASB1–ASB3 retain the actual archM, gramAt, atTau and oneP maps.  A
one-place Lie basis has r=|Tau| n^2 elements.  A Cayley chart and the
finite-dimensional inverse function theorem give second-kind coordinates.
Compactness of a fixed neighborhood gives one inverse-Lipschitz constant
and one image ball for every shifted chart.  The finite component a_x is
in the supplied U intersect Gf and is independent of the cube parameter.
ASB4 proves the cube-to-Haar estimate by outer-volume distortion,
superlevel integration and averaging over a compact neighborhood.
It uses only left Haar invariance; it neither assumes finite quotient
volume nor changes the Haar normalization.  This is the exact comparison
needed upstream by SPR13.

LOCAL SOBOLEV
ASB5 proves the one-dimensional endpoint inequality and its ordered-word
induction with constant (2/s+2s)^r.  The word derivative is prepended; no
commutation of real vector fields is used.  ASB6 lists all words through
length r before psi and y and checks all original smoothness, continuity
and same-level hypotheses.  The smaller direct constant is legitimate:
the original endpoint quantifies existentially over its constant.

QUANTITATIVE RATIONAL COUNT
ASB7–ASB10 prove compact finite-adelic and tensor-product denominators,
integral-basis coordinates bounded by the actual house, and lattice
counting in d n^2 integer coordinates.  ASB11 preserves the literal
normInf and proves its continuity, inverse/product bounds and rational
entry comparison.  Positivity is used only when n>0.
ASB12 gives the explicit admissible exponent
    N = 2 [D.host.E : Q] (V.rank)^2.
For fixed compact Omega and x, the denominator is chosen from the finite
entries of x(Omega Omega^-1)x^-1 before u, y or any rational base point.
The base point only constructs an injection into a bounded matrix set.
Thus C_x is uniform in both u and y.  The empty/rank-zero cases are
included, with the original exponent-zero convention.

FIXED-LEVEL POINTWISE GROWTH
ASB13 unfolds the same fundamental domain and global-AE representative,
without changing quotient measure.  ASB14 chooses the finite list and
compact set first, then N, then C_x, and only afterward F, psi and u.
SPR13 supplies one continuous smooth representative and every original
right-fold derivative identity on that same level; uniqueness identifies
it with the arbitrary supplied continuous representative.  The final
estimate is
    |psi(xu)| <= C_x normInf(u)^N sum_(l in S) ||d_l F||.
The exponent and list remain fixed for derivative vectors at the same
level.  No claim of uniformity across changed targets or initial levels
is made.

ACYCLIC JOINT INTERFACE
    ASB1–ASB4 -> SPR13 -> ASB14 -> later original MMap installation.
No SPR14+ multiplicity-map claim is an incoming ASB dependency.  The
whole SPR file is hash-bound for provenance, but the mathematical
incoming peer edge is only SPR13.

RETAINED PRODUCERS
Actual target FinPair, initial theta boundedness/L2 membership, and the
selected common Bundle/readings/rational tests remain separate C inputs.
ASB supplies no new published-theorem certificate, no new threshold, and
no replacement original datum.

VALIDATION
All {len(cache)} source files equal pinned Git blobs; {len(sources)} distinct declaration
ranges and {sum(map(len, maps.values()))} claim-source occurrences are recorded.
All 14 proof blocks and inherited/peer claim edges have exact byte hashes.
Standalone draft validation is recorded in validation/validation.json:
offline pdflatex draft mode only, no PDF and no Lean replay.

CURRENT BYTES
main.tex SHA256: {sha(tex)}
provenance.json SHA256: {sha((HERE / "provenance.json").read_bytes())}
closure.json SHA256: {sha((HERE / "closure.json").read_bytes())}

PORTABLE REBUILD
python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --peer-root /path/to/reconstruction
The proof text is ready for independent review.  Refresh metadata if
the peer SPR whole-file hash changes before its final freeze.
"""
(HERE / "report.txt").write_text(report)
print(json.dumps({"claims": len(claims), "source_ranges": len(sources), "pinned_files": len(cache),
    "claim_source_occurrences": sum(map(len, maps.values())),
    "main_sha256": sha(tex), "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "closure_sha256": sha((HERE / "closure.json").read_bytes())}, indent=2))
