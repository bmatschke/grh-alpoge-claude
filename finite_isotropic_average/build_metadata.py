#!/usr/bin/env python3
"""Rebuild FIA certificates from this chapter and a pinned source checkout.

Portable usage:
    python3 build_metadata.py --source /path/to/riemann-hypothesis-lean

The default checkout is ../../lean_source relative to this script.
This validates source bytes against git objects; it does not run Lean.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parent.parent / "lean_source")
args = parser.parse_args()
SOURCE = args.source.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip()
assert head == PIN, (head, PIN)
declaration = re.compile(
    r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*"
    r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+"
)
cache = {}
sources = {}


def add(sid, path, start, stop=None, role="Exact original contract or source argument reconstructed independently"):
    path = "src/" + path
    if path not in cache:
        content = (SOURCE / path).read_bytes()
        blob = subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE)
        assert content == blob, path
        cache[path] = content, content.decode().splitlines(keepends=True)
    content, lines = cache[path]
    occurrences = [i for i, line in enumerate(lines) if start in line]
    assert len(occurrences) == 1, (sid, path, start, occurrences)
    a = occurrences[0]
    if stop:
        z = next(i for i in range(a + 1, len(lines)) if stop in lines[i])
    else:
        z = next((i for i in range(a + 1, len(lines)) if declaration.match(lines[i])), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid,
        "path": path,
        "declaration": start,
        "declaration_anchor": start,
        "line_start": a + 1,
        "line_end": z,
        "sha256": sha(content),
        "file_sha256": sha(content),
        "range_sha256": sha(block),
        "range_bytes": len(block),
        "first_line": lines[a].rstrip(),
        "role": role,
        "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a + 1}-L{z}",
    }


D = "Development/AbelianVarietyTheory/"
IW = D + "Proofs/IwasawaDecomposition/"
AL = D + "Proofs/AdelicLatticeProofs/"
SP = D + "Proofs/SatakeParameters/"
TO = D + "Proofs/TwistedOperators/"
FM = D + "Proofs/FlagMeasures/"
DP = D + "Proofs/DivisorProofs/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
BT = "Formalism/LocalToGlobal/BesselHermitianTheta/"
DV = "Formalism/LocalToGlobal/Divisibility/"
PRIMARY = IW + "FockVectorsKilledHeisenbergAverageIsotropic.lean"
GENUS = "Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean"

add("all_some", GENUS, "def AllSome ")
add("global_character", GENUS, "def IsCharAF ")
add("local_character", GENUS, "def psiV ")
add("arch_frequency", FM + "AdelicCharacterFrequenciesAndConductorProduct.lean", "theorem exists_freq ")
add("global_character_scaling", FM + "AdelicCharacterFrequenciesAndConductorProduct.lean", "theorem exists_scaling ")
add("edge", PRIMARY, "theorem exists_edge ", "variable {v :")
add("split_idempotent", BT + "TiedWeil.lean", "def IsSplitIdem ")
add("idempotent_at", "Formalism/LocalToGlobal/HeckeThetaElements/IsHeckeElt.lean", "def IsIdemAt ")
add("chart_contract", SP + "IsIntOv.lean", "def Chart ")
add("chart_comp", SP + "ExistsPlaceChartOfSplitIdempotent.lean", "theorem chart_comp ")
add("chart_exists", SP + "ExistsPlaceChartOfSplitIdempotent.lean", "theorem exists_chart ", "end GlobalTheory.SplitChart")
add("chart_finite_factor", SP + "ExistsSplitFrameSelfDualLatticeCompletion.lean", "theorem exists_factor ")
add("chart_residue_levels", PRIMARY, "theorem exists_chart_levels ")
add("valuation_of_prime_member", PRIMARY, "theorem val_lt_one_of_mem ")
add("split_trace", IW + "SplitPlaceAnnihilatorRelativelyCompact.lean", "theorem trace_split ")
add("char_trace", PRIMARY, "theorem char_trace ")
add("extended_ideal", DV + "DefGroup.lean", "def idS ")
add("residue_map", DV + "DefGroup.lean", "def resS ")
add("residue_kernel", DV + "DefGroupLemmas.lean", "theorem resS_eq_zero_iff ")
add("orientation", IR + "LocalNewformFunction.lean", "def hO ", "structure IsThetaFunO ")
add("theta_fun", IR + "LocalNewformFunction.lean", "structure IsThetaFunO ")
add("weil_covariance", IR + "LocalNewformFunction.lean", "structure IsWeilDatumO ")
add("frame_map", IR + "DatumVec.lean", "def frMapAdj ")
add("integral_matrix", IR + "DatumVec.lean", "def IsIntM ")
add("residue_matrix", IR + "DatumVec.lean", "def redM ")
add("top_block", IR + "DatumVec.lean", "def topL ")
add("row_estimate", PRIMARY, "theorem val_row_lt ")
add("source_adjoint", PRIMARY, "def adj ")
add("rank_one_pairing", PRIMARY, "theorem hO_vecMulVec ")
add("rank_one_symplectic", PRIMARY, "theorem symplO_vecMulVec ")
add("residue_row_precision", PRIMARY, "theorem val_sub_lt ", "set_option maxHeartbeats")
add("constant_phase", PRIMARY, "theorem exists_const ", "set_option maxHeartbeats")
add("weighted_lattice", IR + "LocalNewformFunction.lean", "def latO ")
add("half_contract", IR + "LocalNewformFunction.lean", "def IsHalf ")
add("sb_guard", IR + "LocalNewformFunction.lean", "def IsSBHalf ", "open Classical in")
add("place_model", IR + "LocalNewformFunction.lean", "structure IsPlaceModel ")
add("theta_at", IR + "LocalNewformFunction.lean", "def IsThetaAt ")
add("omega_q", IR + "DatumVec.lean", "def omegaQ ", "open Classical in")
add("omega_k", IR + "DatumVec.lean", "def omegaK ")
add("idempotent_sum", IR + "DatumVec.lean", "def IsIdemSum ", "open Classical in")
add("actual_half_datum", TO + "ExistsDetInt.lean", "def adjDatum ")
add("lattice_clear_up", IW + "ExistsNsmulIntMemLatO.lean", "theorem exists_nsmul_latO_int ")
add("lattice_clear_down", IW + "ExistsNsmulIntMemLatO.lean", "theorem exists_nsmul_int_mem_latO ")
add("sb_finite_residues", IW + "ExistsNsmulIntMemLatO.lean", "theorem isSBHalf_of_red ")
add("frame_additivity", IW + "GramMapMulInv.lean", "theorem frMapAdj_add ")
add("frame_clear_up", IW + "GramMapMulInv.lean", "theorem frMapAdj_up ")
add("frame_clear_down", IW + "GramMapMulInv.lean", "theorem frMapAdj_down ")
add("original_vector", IR + "DatumVec.lean", "def IsThPVecOf ")
add("vacuum", IR + "LocalNewformFunction.lean", "def IsVacO ")
add("standard_character", BT + "TiedWeil.lean", "def IsStdChar ")
add("orthogonal_idempotents", IW + "EqZeroOrEqOfPlaceIdem.lean", "theorem eq_or_mul_eq_zero ")
add("orthogonal_sum", IW + "EqZeroOrEqOfPlaceIdem.lean", "theorem isOrthSum_of_isIdemSum ")
add("actual_eigenvector", PRIMARY, "theorem exists_eigen ")
add("prime_bar", "Formalism/LocalToGlobal/UnitaryNorms/CharHost.lean", "structure PiBar ")
add("prime_bar_divides", "Formalism/LocalToGlobal/UnitaryNorms/CharHost.lean", "def PiBar.Div ")
add("level_choice", IR + "LinksDefs.lean", "structure LevCh ", "namespace LevCh")
add("level_contract", IR + "LinksDefs.lean", "structure Is (μ0 : T)", "end LevCh")
add("sd_frame", IR + "LinksDefs.lean", "def IsSDFrame ")
add("base_frame", IR + "SubgroupCharExtensionOneApply.lean", "def IsBaseFrame ")
add("self_dual_lattice", IR + "LocalNewformFunction.lean", "def IsSelfDualC ", "section Props")
add("frame_lattice_transport", TO + "IsSelfDualCoordLatticeOfSelfDualFrame.lean", "theorem isSelfDualC_of_isSDFrame ", "end GlobalTheory.SDFrameLattice")
add("good_prime_exists", PRIMARY, "theorem exists_mem_Pg ")
add("inf_family", BT + "IsAutFunDef.lean", "def IsInfFam ")
add("real_line_contract", IR + "LocalNewformFunction.lean", "def IsLineAt ")
add("real_line", IR + "LocalNewformFunction.lean", "def lineAt ")
add("real_derivative", IR + "LocalNewformFunction.lean", "def dRho ")
add("creation", IR + "LocalNewformFunction.lean", "def crea ")
add("creation_scaling", IR + "LocalNewformFunction.lean", "def aPlus ")
add("operator_word", IR + "LocalNewformFunction.lean", "def opPow ")
add("pure_tensor_linear", IR + "LocalNewformFunction.lean", "def pureTensorL ")
add("pure_tensor_oriented", IR + "DatumVec.lean", "def pureTensorO ")
add("finite_real_pairing", AL + "SmulEqZeroOfInf.lean", "theorem symplOH_fin_real ")
add("finite_derivative", AL + "SmulEqZeroOfInf.lean", "theorem dRho_heisO ")
add("word_commutation", AL + "SmulEqZeroOfInf.lean", "theorem pureTensorL_comm ")
add("finite_translate", AL + "SmulEqZeroOfInf.lean", "theorem finite_translate ", "end GlobalTheory.FinTranslate")
add("pure_tensor_scalars", TO + "OmPureTensorOOfFinite.lean", "theorem pureTensorO_smul ")
add("pure_tensor_one", TO + "OmPureTensorOOfFinite.lean", "theorem pureTensorO_one ")
add("actual_polynomial", IR + "LinksChar.lean", "def ptP ")
add("models_inf", IR + "LinksChar.lean", "abbrev models_inf ")
add("actual_weil_hypothesis", IR + "LinksChar.lean", "abbrev thP_ωP ")
add("actual_vector_hypothesis", IR + "LinksChar.lean", "abbrev thP_vP ")
add("actual_polynomial_hypothesis", IR + "LinksChar.lean", "abbrev thP_pt_theta ")
add("source_rank_bound", IR + "LinksDefs.lean", "theorem r_le_V ", "variable (D) in")
add("along", IW + "EqTopOfTranslates.lean", "def along ", "open Classical in")
add("isotropic_vector", D + "Definitions/Divisors/IsSmoothVector.lean", "def IsoVec ")
add("matrix_inverse", PRIMARY, "theorem mt_mul_inv ")
add("original_average", PRIMARY, "theorem sum_heisO_along_eq_zero ", "end GlobalTheory.ThetaSupport")
add("average_wrapper", IW + "FockVectorsKilledHeisenbergAverageIsotropicStatement.lean",
    "theorem _root_.GlobalTheory.T.fock_vectors_killed_heisenberg_average_isotropic ")

titles = {
    "FIA1": "Every actual local additive character is nontrivial and has a first nontrivial valuation shell",
    "FIA2": "Exact split-place chart, trace identity, and residue-kernel valuation precision",
    "FIA3": "Explicit constant nontrivial root-of-unity phase on the original frame top block",
    "FIA4": "The actual weighted half-datum satisfies every Schwartz-Bruhat model guard",
    "FIA5": "Eigencharacter of the stored IsThPVecOf vector with period equal to its selected residue norm",
    "FIA6": "Original Pg is nonempty and original SDFrame supplies the exact full self-dual lattices",
    "FIA7": "Finite Heisenberg shifts commute pointwise with the original creation words",
    "FIA8": "One uniform finite period and a polynomial-independent list annihilate every original translated kernel",
}
maps = {
    "FIA1": ["global_character", "local_character", "arch_frequency", "global_character_scaling", "edge"],
    "FIA2": ["split_idempotent", "idempotent_at", "chart_contract", "chart_comp", "chart_exists",
             "chart_finite_factor", "chart_residue_levels", "valuation_of_prime_member", "split_trace",
             "char_trace", "extended_ideal", "residue_map", "residue_kernel"],
    "FIA3": ["constant_phase", "orientation", "frame_map", "integral_matrix", "residue_matrix",
             "top_block", "row_estimate", "source_adjoint", "rank_one_pairing",
             "rank_one_symplectic", "residue_row_precision"],
    "FIA4": ["weighted_lattice", "half_contract", "sb_guard", "omega_q", "omega_k", "actual_half_datum",
             "lattice_clear_up", "lattice_clear_down", "sb_finite_residues", "frame_additivity",
             "frame_clear_up", "frame_clear_down"],
    "FIA5": ["actual_eigenvector", "all_some", "original_vector", "vacuum", "standard_character",
             "place_model", "theta_at", "idempotent_sum", "orthogonal_idempotents", "orthogonal_sum"],
    "FIA6": ["good_prime_exists", "prime_bar", "prime_bar_divides", "level_choice", "level_contract",
             "sd_frame", "base_frame", "self_dual_lattice", "frame_lattice_transport"],
    "FIA7": ["inf_family", "real_line_contract", "real_line", "real_derivative", "creation",
             "creation_scaling", "operator_word", "pure_tensor_linear", "pure_tensor_oriented",
             "finite_real_pairing", "finite_derivative", "word_commutation", "finite_translate",
             "pure_tensor_scalars", "pure_tensor_one"],
    "FIA8": ["original_average", "average_wrapper", "models_inf", "actual_weil_hypothesis",
             "actual_vector_hypothesis", "actual_polynomial_hypothesis", "actual_polynomial",
             "source_rank_bound", "along", "isotropic_vector", "matrix_inverse", "weil_covariance", "theta_fun"],
}
dependencies = {
    "FIA1": [],
    "FIA2": [],
    "FIA3": ["FIA1", "FIA2"],
    "FIA4": [],
    "FIA5": ["FIA1", "FIA2", "FIA3", "FIA4"],
    "FIA6": [],
    "FIA7": [],
    "FIA8": ["FIA5", "FIA6", "FIA7"],
}
scopes = {
    "FIA1": "Any exact IsCharAF on the original totally real F; every finite F-place; no standard-sign restriction is needed.",
    "FIA2": "Every supplied IsIdemAt(e,PP) on the original host; chart factors through the literal toEAf and matches the literal resS.",
    "FIA3": "Every supplied original S,T, arbitrary invertible finite frames, m<=n, IsCharAF, IsIdemAt(e,PP), and nonzero e-projection of c; forall integral top-identity t, one l,zeta works.",
    "FIA4": "Every original full lattice pair, actual weighted latO, frames, finite sets, residue characters and idempotent sum; one positive integer verifies both exact IsSBHalf guards.",
    "FIA5": "The supplied original IsThPVecOf vector and the selected PP in Pg, m<=n, self-dual lattices, and c nonzero at each split projection; all natural k; the period is exactly absNorm(PP).",
    "FIA6": "Every original LevCh.Is(mu0); exists PP in its actual Pg; IsSDFrame at N=1 yields the stored full self-dual lattices.",
    "FIA7": "Same original psi/theta/Cartan/bases/scale; any finite u; every exact ordered creation word and every polynomial; no arbitrary Weil-operator continuity is assumed.",
    "FIA8": "For each R satisfying its five exact hypotheses, exists NR>0, forall i,t,h,g,xi!=0, exists a:Fin NR->AE^rank(Vc), forall polynomials P, the original function sum is zero. NR depends only on one PP in R.Pg; a may depend on i,t,h,g,xi but not P.",
}

tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    a = next(i for i, line in enumerate(lines) if line.strip() == ("% BEGIN " + cid).encode())
    z = next(i for i, line in enumerate(lines) if line.strip() == ("% END " + cid).encode()) + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid,
        "title": title,
        "introduced_in": "0.33",
        "classification": "B",
        "status": "complete independent human proof of the stated original-data implication",
        "depends_on": dependencies[cid],
        "proof_location": {
            "file": "finite_isotropic_average/main.tex",
            "label": "claim:" + cid,
            "line_start": a + 1,
            "line_end": z,
            "sha256": sha(block),
            "bytes": len(block),
        },
        "source_ids": maps[cid],
        "sources": [sources[s] for s in maps[cid]],
        "quantifier_scope": scopes[cid],
    })

provenance = {
    "schema": "rh-human-component-provenance/1",
    "artifact_version": "0.33",
    "date": "2026-11-22",
    "component": "finite_isotropic_average",
    "source_commit": PIN,
    "main_tex_sha256": sha(tex),
    "metadata_builder": {
        "file": "build_metadata.py",
        "sha256": sha(Path(__file__).read_bytes()),
        "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout",
    },
    "claims": claims,
    "source_inventory": list(sources.values()),
    "baseline_dependencies": [],
    "validation": {
        "source_commit_verified": True,
        "pinned_blob_verified_files": len(cache),
        "source_ranges": len(sources),
        "claim_source_occurrences": sum(len(x) for x in maps.values()),
        "all_source_ranges_exact": True,
        "independent_human_mathematical_proof": True,
        "new_lean_build": False,
        "tex_validation": "See validation/validation.json when present; a draft compile is syntax validation only.",
    },
    "scope_note": "The Lean source is assumed fully checked and correct. No new category-A published-theorem certificate. BTH13-BTH15 normalization is compatible but not needed by this covariance-only proof.",
}
(HERE / "provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n")
(HERE / "source_locators.txt").write_text("\n".join(
    [f"Source pin: {PIN}", f"Main TeX SHA256: {sha(tex)}", ""]
    + [f"{s['id']} | {s['declaration_anchor']}\n{s['path']}:{s['line_start']}-{s['line_end']}\n"
       f"file_sha256={s['file_sha256']}\nrange_sha256={s['range_sha256']}\n{s['url']}\n"
       for s in sources.values()]
))
exact_inputs = [
    "R.toLevCh.Is A.mu0",
    "R.models_inf (IsInfFam R.theta)",
    "R.thP_omegaP (the supplied original IsWeilDatumO for every i,t)",
    "R.thP_vP (the stored original IsThPVecOf for every i,t)",
    "R.thP_pt_theta (each original polynomial vector is a theta function)",
]
closure = {
    "schema": "rh-component-closure/1",
    "version": "0.33",
    "component": "finite_isotropic_average",
    "source_commit": PIN,
    "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claims": list(titles),
    "claim_count": len(titles),
    "class_counts": {"A": 0, "B": len(titles), "C": 0, "D": 0},
    "all_new_claims_are_conditional_implications": True,
    "exact_original_inputs": exact_inputs,
    "closed_subtargets": [
        {"source_declaration": "GlobalTheory.ThetaSupport.exists_edge", "proof": ["FIA1"]},
        {"source_declaration": "GlobalTheory.ThetaSupport.exists_chart_levels", "proof": ["FIA2"]},
        {"source_declaration": "GlobalTheory.ThetaSupport.exists_const", "proof": ["FIA1", "FIA2", "FIA3"]},
        {"source_declaration": "GlobalTheory.ThetaSupport.exists_eigen", "proof": ["FIA1", "FIA2", "FIA3", "FIA4", "FIA5"]},
        {"source_declaration": "GlobalTheory.ThetaSupport.exists_mem_Pg", "proof": ["FIA6"]},
        {"source_declaration": "GlobalTheory.ThetaSupport.sum_heisO_along_eq_zero", "proof": ["FIA1", "FIA2", "FIA3", "FIA4", "FIA5", "FIA6", "FIA7", "FIA8"]},
        {"source_declaration": "GlobalTheory.T.fock_vectors_killed_heisenberg_average_isotropic", "proof": ["FIA8"]},
    ],
    "sufficient_rules": [
        {
            "id": "FIA_ORIGINAL_AVERAGE",
            "kind": "AND on one supplied original R",
            "requires": exact_inputs,
            "concludes": scopes["FIA8"],
            "proof": list(titles),
        }
    ],
    "quantifiers": {
        "period": "Choose PP in R.Pg once and put NR=absNorm(PP)>0.",
        "list": "For fixed i,t,h,g,xi!=0, use c=mt(T,g^-1)*incA(xi), the FIA5 l, and a_k^transpose=(k*l)^transpose*mt(S,h^-1).",
        "simultaneous_polynomials": True,
        "all_original_tuples": True,
        "stronger_direction_hypothesis": "Only xi!=0 is used; IsoVec's norm-zero clause is not needed for the finite average.",
        "no_family_threshold": "This is pointwise for each supplied R; no new eventual threshold is introduced or changed.",
    },
    "remaining_producers": [
        {
            "id": "FIA_INHERITED_ORIGINAL_WEAK_DATA",
            "classification": "C",
            "status": "inherited original-data existence premise, not a new independent obligation",
            "contract": "Produce the same original R and all five coupled predicates in exact_original_inputs on the selected Bundle.",
            "not_new_counted_obligation": True,
        },
        {
            "id": "BTH_BASE_CUSPIDAL_EXTENSION",
            "classification": "C",
            "status": "still open as a whole; its finite hsupp subtarget is now proved under the original weak data",
            "contract": "Actual smooth cuspidal multiplicity extension of the convergent original lowest-type integral.",
            "closed_here": ["finite isotropic average for all original polynomial/translated kernels"],
            "outside_this_component": ["constant-term invariance and cuspidality transfer", "actual differentiation and uniform growth", "simultaneous ioP and lowering", "bounded holomorphic realization"],
            "not_new_counted_obligation": True,
        },
    ],
    "new_unresolved_internal_suppliers": [],
    "new_D_obligations": [],
    "not_closed": [
        "Existence of the original weak data on the selected Bundle",
        "Full original base smooth cuspidal extension",
        "Same-Bundle geometric reading and simultaneous rational tests",
        "RowsHold0_3",
        "Complete RH/GRH human proof",
    ],
    "new_lean_replay": False,
    "no_new_A_certificate": True,
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "claims": len(claims),
    "source_files": len(cache),
    "source_ranges": len(sources),
    "claim_source_occurrences": sum(len(x) for x in maps.values()),
    "main_tex_sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "closure_sha256": sha((HERE / "closure.json").read_bytes()),
    "proof_hashes": {c["id"]: c["proof_location"]["sha256"] for c in claims},
}, indent=2))
