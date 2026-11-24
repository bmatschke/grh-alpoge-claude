#!/usr/bin/env python3
"""Portable OTW source/proof certificates. No Lean replay or build.

python3 build_metadata.py --source /path/to/pinned/checkout \
    --human-root /path/to/reconstruction --neat-root /path/to/neat_levels
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_HUMAN = HERE.parent if (HERE.parent / "count_ii_producer").exists() else HERE.parents[1] / "reconstruction_v040"
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--human-root", type=Path, default=DEFAULT_HUMAN)
ap.add_argument("--neat-root", type=Path, default=HERE.parent / "neat_levels")
args = ap.parse_args()
SOURCE, HUMAN, NEAT = args.source.resolve(), args.human_root.resolve(), args.neat_root.resolve()
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe|scoped)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache, sources = {}, {}


def add(sid, path, anchor, stop=None, role="Exact original definition or endpoint in the claim's printed scope"):
    path = "src/" + path
    if path not in cache:
        data = (SOURCE / path).read_bytes()
        assert data == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        cache[path] = data, data.decode().splitlines(keepends=True)
    data, lines = cache[path]
    pattern = re.compile(re.escape(anchor.rstrip()) + r"(?=$|[\s:({])")
    hits = [i for i, line in enumerate(lines) if pattern.search(line)]
    assert len(hits) == 1, (sid, path, anchor, hits)
    a = hits[0]
    z = next((i for i in range(a + 1, len(lines)) if (stop in lines[i] if stop else decl.match(lines[i]))), len(lines))
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid, "path": path, "declaration": anchor, "declaration_anchor": anchor,
        "line_start": a + 1, "line_end": z, "sha256": sha(data), "file_sha256": sha(data),
        "range_sha256": sha(block), "range_bytes": len(block), "first_line": lines[a].rstrip(),
        "role": role, "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a+1}-L{z}",
    }


A = "Development/AutomorphicArithmetic/AutomorphicVarieties/"
H = A + "HeckeAlgebras/"
W = A + "WeilGroupCharacters/"
D = A + "ModularityArgument/ThresholdArguments/DenseThresholdCases/"
T = D + "TThetaEx.lean"
C = H + "ContinuousTorusCharacter.lean"
U = W + "UniversalOrdinaryDeterminantRing.lean"
S = H + "CoefficientRepTrivialOnUnramified.lean"

add("Coef", A + "HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean", "structure Coef")
for sid, anchor in [("IsCO", "class IsCO"), ("AdicCont", "def AdicCont")]:
    add(sid, A + "CommutativeAlgebra/ResMapBijective.lean", anchor)
for sid, anchor in [("IsCNL", "class IsCNL"), ("Iwa", "structure Iwa"),
                    ("ContChar", "def ContChar"), ("Frame", "structure Frame"),
                    ("Neat", "def Neat"), ("Free", "def Free")]:
    add(sid, C, anchor)
for sid, anchor in [("GFrame", "structure GFrame"), ("Resid", "structure Resid"),
                    ("IsPsi", "structure IsPsi"), ("IsInert", "def IsInert"),
                    ("LamObj", "structure LamObj")]:
    add(sid, U, anchor)
add("IsLocalArtin", "Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/HasExponentZeroIff.lean", "structure IsLocalArtin")
add("WeilSmooth", "Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/MonodromyZeroOfWeilDeligneRepClassIff.lean", "def IsSmooth")
add("cycZ", "ReciprocityTheory/GaloisValuations/Global.lean", "def cycZ")
add("continuous_cycZ", "ReciprocityTheory/GaloisValuations/Global.lean", "theorem continuous_cycZ")

for sid, anchor in [("th_Uc", "private theorem th_Uc"), ("th_fin", "private theorem th_fin"),
                    ("th_char", "private theorem th_char"), ("th_eps", "private theorem th_eps"),
                    ("th_mul", "private theorem th_mul"), ("th_diag", "private theorem th_diag"),
                    ("th_char_adjusted", "private theorem th_char'"), ("th_torus", "private theorem th_torus"),
                    ("th_free", "private theorem th_free"),
                    ("TThetaEx", "theorem UpperTheory.V.Hi.exists_theta_is_weight_of_lam_obj")]:
    add(sid, T, anchor)
for sid, anchor in [("piData", "def piData"), ("Kc", "def Kc"), ("Uo", "def Uo"),
                    ("Uc", "def Uc"), ("glData", "def glData"), ("eT", "def eT")]:
    add(sid, H + "TcAnti.lean", anchor)
for sid, anchor in [("glIwa", "def glIwa"), ("piIwa", "def piIwa")]:
    add(sid, H + "Distinct.lean", anchor)
for sid, anchor in [("iwS", "def iwS"), ("eV", "def eV"), ("HSet", "structure HSet"),
                    ("actual_X", "def X"), ("HLev", "abbrev Lev"), ("lev", "def lev"),
                    ("HSetAx", "structure Ax"), ("tauA", "def τA"), ("MK", "def MK"),
                    ("IsWt", "structure IsWt"), ("epsV", "def epsV")]:
    add(sid, S, anchor)
for sid, anchor in [("artOf", "def artOf"), ("KT", "abbrev KT"), ("QData", "structure QData"),
                    ("hset", "def hset"), ("IsTheta", "def IsTheta"), ("IsRes", "structure IsRes")]:
    add(sid, H + "IsTheta.lean", anchor)
for sid, anchor in [("HidaSetting", "structure HidaSetting"), ("Vl", "abbrev _root_.UpperTheory.V.W.Vl"),
                    ("VLev", "structure Lev"), ("actual_GFrame", "def HidaSetting.Lev.frame")]:
    add(sid, W + "ContinuousResP.lean", anchor)
add("neatU", H + "OrdinaryHeckeCharacters/NtExpand.lean", "theorem UpperTheory.V.Hi.neatU",
    role="Original full neatU endpoint, independently reconstructed by inherited peer claim NTL17 on all original QData, arbitrary integral tau0 and every K.")
for sid, anchor in [("IsTypeAlt", "def IsTypeAlt"), ("TypeForAlt", "def TypeForAlt"),
                    ("UnitaryHeckeData", "structure UnitaryHeckeData"),
                    ("UnitaryHeckeData_M", "abbrev UnitaryHeckeData.M"),
                    ("UnitaryHeckeData_IsJ", "def UnitaryHeckeData.IsJ")]:
    add(sid, D + "UnitaryHeckeData.lean", anchor)
add("HdEx", D + "HdEx.lean", "theorem UpperTheory.V.Hi.nonempty_unitaryHeckeData",
    role="Conditional assembly is reconstructed after the full original TypeForAlt is supplied; its unconditional type producer remains separate.")
add("TTypeEx", D + "TTypeEx.lean", "theorem UpperTheory.V.Hi.exists_integral_type_for_residual_rep",
    role="Retained original integral-type producer, not proved by this packet.")
add("TResEx", D + "TResEx.lean", "theorem UpperTheory.V.Hi.exists_is_res_of_residual_rep_and_type",
    role="Original residual coefficient endpoint inherited in its full arbitrary-tau0 scope from CAP17.")


def blocks(root, rel, ids, role):
    data = (root / rel).read_bytes()
    lines = data.splitlines(keepends=True)
    out = []
    for cid in ids:
        aa = [i for i, x in enumerate(lines) if x.strip() == ("% BEGIN " + cid).encode()]
        zz = [i for i, x in enumerate(lines) if x.strip() == ("% END " + cid).encode()]
        assert len(aa) == len(zz) == 1 and aa[0] < zz[0], (rel, cid)
        a, z = aa[0], zz[0] + 1
        block = b"".join(lines[a:z])
        out.append({"id": cid, "line_start": a + 1, "line_end": z,
                    "sha256": sha(block), "range_sha256": sha(block), "bytes": len(block)})
    return {"file": rel, "sha256": sha(data), "file_sha256": sha(data), "role": role, "claims": out}


inherited = [
    blocks(HUMAN, "count_ii_producer/main.tex", ["CIP4", "CIP5"],
           "Checked actual artOf and inverse reciprocity convention at the original split CM places above ell; positive cyclotomic local norm only in that original scope."),
    blocks(HUMAN, "count_auxiliary_primes/main.tex", ["CAP17"],
           "Full original IsRes on arbitrary integral tau0 and the same coefficient ring, residual datum, reciprocity map and fixed iota."),
    blocks(NEAT.parent, NEAT.name + "/main.tex", ["NTL17"],
           "Full original neatU for every QData, arbitrary tau0 and every compact-open K; no TypeForAlt or HSet.Ax premise."),
]
# Release paths are component-relative even when the peer packet was built in a work directory.
inherited[-1]["file"] = "neat_levels/main.tex"
component_bindings = []
for root, name in [(HUMAN, "count_ii_producer"), (HUMAN, "count_auxiliary_primes"), (NEAT.parent, NEAT.name)]:
    files = []
    for filename in ["main.tex", "provenance.json", "closure.json", "published_applications.json"]:
        data = (root / name / filename).read_bytes()
        release_name = "neat_levels" if root == NEAT.parent and name == NEAT.name else name
        files.append({"file": release_name + "/" + filename, "sha256": sha(data), "file_sha256": sha(data)})
    component_bindings.append({"component": "neat_levels" if root == NEAT.parent and name == NEAT.name else name, "files": files})

cip_apps = json.loads((HUMAN / "count_ii_producer/published_applications.json").read_text())
published = {
    "schema": "rh-published-applications/1", "component": "ordinary_theta_weight", "version": "0.41",
    "source_commit": PIN, "applications": [], "new_published_theorem_imports": 0,
    "inherited_publication_scope": "CIP4/CIP5 already certify actual artOf and its inverse-normalized cyclotomic formula at the split CM places used here. This packet neither broadens that application nor invokes local Langlands for the character construction.",
    "inherited_application_manifest": {"file": "count_ii_producer/published_applications.json",
        "sha256": sha((HUMAN / "count_ii_producer/published_applications.json").read_bytes()),
        "used_via_claims": ["CIP4", "CIP5"],
        "primary_url": "https://www.jmilne.org/math/CourseNotes/CFT.pdf",
        "hypothesis_match": "Original L is CM; every v in V.frame.Vl lies above ell; s.split implies s.w(v) differs from its conjugate. The valuation s.A(v), place s.w(v), artOf, inertia, epsV and embeddings are unchanged."},
    "independent_proof_scope": "Finite-abelian character separation, adic-quotient kernel descent to the whole complete coefficient ring, principal-unit topology, diagonal torus coordinates and all-level record assembly are proved in full.",
    "not_imported": ["A fresh global or local reciprocity map", "A different arithmetic Artin normalization", "General glBridge", "Integral TypeForAlt production", "HSet.Ax", "Ordinary control or arithmetic fiber separation"],
}
(HERE / "published_applications.json").write_text(json.dumps(published, indent=2, ensure_ascii=False) + "\n")

titles = {
    "OTW1": "Actual complete coefficient ring and all finite adic quotients",
    "OTW2": "Literal principal-unit neighborhood base",
    "OTW3": "Finite abelian character separation by explicit extension",
    "OTW4": "Finite smooth characters vanish beyond one Artin depth",
    "OTW5": "Unique descent to a character valued in the whole complete ring",
    "OTW6": "Actual cyclotomic and multiplicative adic continuity",
    "OTW7": "Exact inverse cyclotomic adjustment with the ordered identity",
    "OTW8": "Original diagonal coordinates and the exact c+1 congruence",
    "OTW9": "Single product-torus character and one depth per precision",
    "OTW10": "Original IsTheta and ContChar on the same hset, with uniqueness",
    "OTW11": "Original Neat implies every field of Free",
    "OTW12": "Full original theta-and-weight producer, one theta before every K",
    "OTW13": "Exact UnitaryHeckeData assembly after the original type is supplied",
}
deps = {
    "OTW1": [], "OTW2": [], "OTW3": [], "OTW4": ["OTW2", "OTW3"],
    "OTW5": ["OTW1", "OTW4"], "OTW6": ["OTW1"],
    "OTW7": ["OTW5", "OTW6", "CIP4", "CIP5"], "OTW8": ["OTW2"],
    "OTW9": ["OTW8"], "OTW10": ["OTW1", "OTW6", "OTW7", "OTW8", "OTW9", "CIP4"],
    "OTW11": [], "OTW12": ["OTW10", "OTW11", "NTL17", "CIP4"],
    "OTW13": ["OTW12", "CAP17", "CIP4"],
}
maps = {
    "OTW1": ["Coef", "IsCO", "IsCNL", "LamObj", "TThetaEx"],
    "OTW2": ["Uo", "Uc", "th_Uc"],
    "OTW3": ["th_fin"],
    "OTW4": ["IsLocalArtin", "WeilSmooth", "Uc", "th_fin"],
    "OTW5": ["IsLocalArtin", "WeilSmooth", "IsCNL", "AdicCont", "th_char"],
    "OTW6": ["AdicCont", "epsV", "cycZ", "continuous_cycZ", "th_eps", "th_mul", "th_char_adjusted"],
    "OTW7": ["IsLocalArtin", "AdicCont", "epsV", "th_char_adjusted"],
    "OTW8": ["Kc", "Uo", "Uc", "glData", "eT", "glIwa", "th_diag"],
    "OTW9": ["piData", "piIwa", "iwS", "eV", "ContChar", "th_torus"],
    "OTW10": ["HidaSetting", "Vl", "VLev", "actual_GFrame", "GFrame", "Resid", "IsPsi", "IsInert", "LamObj", "artOf", "KT", "QData", "hset", "IsTheta", "epsV", "TThetaEx"],
    "OTW11": ["Iwa", "Frame", "Neat", "Free", "th_free"],
    "OTW12": ["HidaSetting", "HSet", "actual_X", "HLev", "lev", "tauA", "IsWt", "hset", "IsTheta", "neatU", "TThetaEx"],
    "OTW13": ["IsTypeAlt", "TypeForAlt", "UnitaryHeckeData", "IsRes", "TResEx", "HdEx", "TTypeEx", "MK", "UnitaryHeckeData_M", "UnitaryHeckeData_IsJ"],
}
scopes = {
    "OTW1": "Every original Coef ell and IsCO(O,R), including the literal LamObj.Lambda. Finite R/m^N for all N, locality, finite residue and separatedness; no reducedness/domain premise on R.",
    "OTW2": "Every original nonarchimedean local field, actual Uo and Uc, and every open subgroup W. One c before all d>=c; exact d=0 convention retained.",
    "OTW3": "Every finite abelian group and nonidentity element; explicit complex character extension, with no decomposition theorem imported.",
    "OTW4": "Every actual IsLocalArtin and finite-abelian-target character smooth on the original inertia. One c before all d>=c and all Weil elements; no stronger unstated Weil topology.",
    "OTW5": "Every IsCNL ring and adically continuous character of the original decomposition group. One unique full-ring character, exact equality on same Galois elements, then for every N one c before all d>=c and all y in Uc(d).",
    "OTW6": "Every local Z_ell-to-R map and continuous Z_ell-valued function; product/power/inverse congruence calculus, then actual epsV on original hset. No finite-order or reducedness assumption.",
    "OTW7": "Every pair of adically continuous characters, every nonnegative i and the same actual Artin map. Exact ordered psi(g)*eps(g)^i*chi(a(x))=1; the CIP4/CIP5 sign observation is only in the original split CM specialization.",
    "OTW8": "Every original glIwa(k,n), including n=0. Unique actual diagonal coordinates, full integral-unit image, exact eT and Tc(c) iff all coordinates in Uc(c+1).",
    "OTW9": "Every finite place index and n; one product theta before every coefficient precision and before any compact-open K. One common depth at each precision, exact eV values.",
    "OTW10": "All original l,L,Omega,s,n>=1,V,Q,c,m,arbitrary integral tau0,r,Lambda. The same hset, artOf, inertia, epsV and ordered kappa; full IsTheta and ContChar, plus uniqueness on the actual torus.",
    "OTW11": "Every original frame, subgroup, commutative coefficient ring, representation of any rank and torus character. No type, smoothness or character-continuity premise is needed for Neat=>Free.",
    "OTW12": "Full original exists_theta_is_weight_of_lam_obj, including its LiteratureRankNHypothesis. One theta before every family K of compact-open Q-levels; arbitrary tau0, no HSet.Ax or TypeForAlt premise, all original odd ell including ell=3.",
    "OTW13": "Conditional on one supplied original m,tau0 with full TypeForAlt(r,iota,tau0), assemble the entire original UnitaryHeckeData with the same O,r,Lambda,Q,iota. The type producer itself is retained; theta and residual a are fixed before all K.",
}
assert set(titles) == set(deps) == set(maps) == set(scopes)
incoming = {c["id"] for f in inherited for c in f["claims"]}
assert all(c in titles or c in incoming for ds in deps.values() for c in ds)
assert all(sid in sources for ss in maps.values() for sid in ss)
tex = (HERE / "main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    aa = [i for i, x in enumerate(lines) if x.strip() == ("% BEGIN " + cid).encode()]
    zz = [i for i, x in enumerate(lines) if x.strip() == ("% END " + cid).encode()]
    assert len(aa) == len(zz) == 1 and aa[0] < zz[0], cid
    a, z = aa[0], zz[0] + 1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": titles[cid], "introduced_in": "0.41", "classification": "B",
        "status": "complete independent human proof in the stated scope", "depends_on": deps[cid],
        "classical_inputs": [], "quantifier_scope": scopes[cid],
        "proof_location": {"file": "ordinary_theta_weight/main.tex", "label": "claim:" + cid,
                           "line_start": a + 1, "line_end": z, "sha256": sha(block),
                           "range_sha256": sha(block), "bytes": len(block)},
        "source_ids": maps[cid], "sources": [sources[sid] for sid in maps[cid]],
    })
remaining = [
    {"id": "OTW_ORIGINAL_INTEGRAL_TYPE", "classification": "C", "status": "retained original producer",
     "contract": "Produce one m,tau0 satisfying the entire TypeForAlt(r,iota,tau0), with every original Teichmuller lift and every allowed IsRecT. OTW13 consumes this exact premise; no unconditional HdEx-from-HypothesesHprime theorem is claimed here.",
     "source_ids": ["IsTypeAlt", "TypeForAlt", "TTypeEx", "HdEx"], "not_new_independent_top_level_obligation": True},
    {"id": "OTW_ORIGINAL_ORDINARY_AND_SAME_IDEAL_DATA", "classification": "C", "status": "retained original downstream producers outside this packet",
     "contract": "Remaining HSet.Ax fields, actual ordinary modules/control, determinant and arithmetic-fiber separation, four Hida endpoints, and all-level HasAut with the original common ideal and original coefficient-threshold order.",
     "source_ids": ["HSetAx", "MK", "UnitaryHeckeData_M", "UnitaryHeckeData_IsJ"], "not_new_independent_top_level_obligation": True},
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.41", "date": "2026-11-22",
    "component": "ordinary_theta_weight", "source_commit": PIN, "main_tex_sha256": sha(tex),
    "metadata_builder": {"file": "build_metadata.py", "sha256": sha(Path(__file__).read_bytes()),
        "portable_invocation": "python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --neat-root /path/to/neat_levels"},
    "claims": claims, "source_inventory": list(sources.values()), "baseline_dependencies": inherited,
    "component_bindings": component_bindings,
    "published_applications": {"file": "published_applications.json", "sha256": sha((HERE / "published_applications.json").read_bytes()), "certificate_ids": []},
    "remaining_producer_contracts": remaining,
    "validation": {"source_commit_verified": True, "pinned_blob_verified_files": len(cache),
        "source_ranges": len(sources), "claim_source_occurrences": sum(map(len, maps.values())),
        "all_source_ranges_exact": True, "all_inherited_claim_edges_explicit": True,
        "new_lean_build": False, "tex_validation": "See validation/validation.json; offline draft mode, no PDF."},
    "scope_note": "Complete original TThetaEx producer using completed actual reciprocity and full neatU; HdEx only after the full original integral type is supplied. No whole Count-II closure.",
}
(HERE / "provenance.json").write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n")
closure = {
    "schema": "rh-human-component-closure/1", "version": "0.41", "component": "ordinary_theta_weight", "source_commit": PIN,
    "standing_assumption": "The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Statuses concern the human reconstruction only.",
    "main_sha256": sha(tex), "main_tex_sha256": sha(tex), "sha256": sha(tex),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claim_ids": list(titles), "claim_count": len(titles), "class_counts": {"A": 0, "B": 13, "C": 0, "D": 0},
    "published_application_certificate_ids": [],
    "closed_contracts": [
        {"id": "OTW_COMPLETE_COEFFICIENT_CHARACTERS", "claims": ["OTW1", "OTW2", "OTW3", "OTW4", "OTW5", "OTW6", "OTW7"],
         "classification": "B", "status": "complete independent producer",
         "contract": "Actual finite adic quotients and unique full-ring character descent from every supplied IsLocalArtin/adic decomposition character, exact inverse cyclotomic identity and all precision-depth quantifiers."},
        {"id": "OTW_ORIGINAL_TORUS_CHARACTER", "claims": ["OTW8", "OTW9", "OTW10"], "classification": "B",
         "status": "complete original producer with completed inherited reciprocity",
         "contract": "Same original torus, hset, artOf, Lambda, kappa and epsV; one theta satisfying IsTheta and ContChar, unique on this torus."},
        {"id": "ORIGINAL_TTHETAEX", "claims": ["OTW10", "OTW11", "OTW12"], "inherited_claims": ["CIP4", "NTL17"],
         "classification": "B", "status": "complete original producer",
         "contract": "Full exists_theta_is_weight_of_lam_obj: all original input data, one theta before every compact-open K, complete IsTheta and IsWt, arbitrary integral tau0, no TypeForAlt/HSet.Ax premise."},
        {"id": "OTW_HDEX_AFTER_TYPE", "claims": ["OTW13"], "inherited_claims": ["CAP17"], "classification": "B",
         "status": "complete record assembly on the exact retained original TypeForAlt antecedent",
         "contract": "Full original UnitaryHeckeData on the same Q,iota,Lambda and supplied integral type, with theta and a before all K. Does not produce the type antecedent."},
    ],
    "same_object_sufficient_rule": {
        "antecedent": "Exactly the original TThetaEx input prefix: LiteratureRankNHypothesis, l prime, L CM, Omega algebraic closure, s:HidaSetting, n>=1, V,Q,c,m,arbitrary tau0,r,Lambda.",
        "inherited_completed_inputs": ["CIP4: actual artOf and its full source predicate in this split CM scope", "CIP5: exact sign observation in that same scope", "NTL17: full neatU"],
        "quantifier_order": ["all original fixed input data", "one theta on the original torus", "for every N one c before all t in Tc(c)", "for every original compact-open Q-level family K, Free for this same theta"],
        "unchanged": ["c.O", "Lambda.Lambda", "r", "Q", "tau0", "hset", "artOf", "original decomposition and inertia groups", "kappa order", "epsV normalization", "eV coordinates"],
        "exact_identity": "kappa(v,i)(g) * epsV(v)(g)^i * theta(eV(v,i,y)) = 1 for every original x,g,hg,y and equality guard",
        "output": "One theta with full original IsTheta and IsWt. With the exact TypeForAlt supplied, CAP17 gives the remaining residual field and OTW13 assembles UnitaryHeckeData.",
    },
    "remaining_inputs": remaining, "selected_top_level_leaf_closed": False,
    "not_claimed": ["Original integral-type producer", "Unconditional HdEx from HypothesesHprime without TypeForAlt construction", "Remaining HSet.Ax fields", "Ordinary/control/fiber-separation producers", "Four Hida endpoints or all-level same-J HasAut", "Whole Count-II support leaf", "New Lean replay/build"],
    "review_status": "Awaiting independent final-byte review; external hash-bound review records final disposition.",
}
(HERE / "closure.json").write_text(json.dumps(closure, indent=2, ensure_ascii=False) + "\n")
loc = ["OTW source locators", "Pinned source: " + PIN, "All intervals inclusive; file bytes verified against pinned Git blobs.", ""]
for cid in titles:
    loc.append(cid + ": " + titles[cid])
    for sid in maps[cid]:
        s = sources[sid]
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']}  {s['declaration']}",
                "    file_sha256=" + s["file_sha256"] + " range_sha256=" + s["range_sha256"]]
    loc.append("")
loc += ["Inherited completed claims: CIP4, CIP5, CAP17, NTL17. Exact source and proof bindings are in provenance.json.",
        "No new published theorem import; no Lean replay/build."]
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
result = {"claims": len(claims), "source_files": len(cache), "source_ranges": len(sources),
    "claim_source_occurrences": sum(map(len, maps.values())), "inherited_blocks": sum(len(x["claims"]) for x in inherited),
    "main_sha256": sha(tex), "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "closure_sha256": sha((HERE / "closure.json").read_bytes()),
    "published_applications_sha256": sha((HERE / "published_applications.json").read_bytes())}
print(json.dumps(result, indent=2))
