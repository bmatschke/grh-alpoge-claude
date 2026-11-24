#!/usr/bin/env python3
"""Build portable GLS provenance and conditional closure from a pinned checkout.

Usage: python build_provenance.py --source /path/to/lean_source
                                --baseline /path/to/reconstruction_v032
No Lean compilation or kernel replay is claimed. Source bytes are checked
against git objects at PIN; human proof blocks are hashed independently.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1]/"lean_source")
ap.add_argument("--baseline", type=Path, default=HERE.parents[1]/"reconstruction_v032")
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()

def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n")

assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE,
                              text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE/"provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"GLS\d+", k) for k in old), "GLS prefix is not fresh"
raw = (HERE/"main.tex").read_bytes()
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}

def source(path, name):
    if path not in cache:
        b = (SOURCE/path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN+":"+path], cwd=SOURCE), path
        ls = b.decode().splitlines(keepends=True)
        ds = [(i, DECL.match(x).group(1)) for i,x in enumerate(ls) if DECL.match(x)]
        cache[path] = (b, ls, ds)
    b, ls, ds = cache[path]
    found = [(j,i) for j,(i,n) in enumerate(ds) if n == name]
    assert len(found) == 1, (path, name, found)
    j,s = found[0]
    e = ds[j+1][0] if j+1 < len(ds) else len(ls)
    for i in range(s+1,e):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)", ls[i]):
            e = i
            break
    while e > s+1 and not ls[e-1].strip():
        e -= 1
    rb = "".join(ls[s:e]).encode()
    return {"path": path, "declaration": name, "source_spelling": name,
            "line_start": s+1, "line_end": e,
            "sha256": sha(b), "file_sha256": sha(b),
            "range_sha256": sha(rb), "range_bytes": len(rb),
            "first_line": ls[s].rstrip(),
            "verified_equal_to_pinned_git_blob": True,
            "role": "Exact original contract, dictionary, or corresponding source proof; human closure comes from the separately hashed GLS proof block.",
            "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{s+1}-L{e}"}

anchors = {f"GLS{i}": [] for i in range(1,14)}
for line in (HERE/"source_anchors.txt").read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    ids, path, names = line.split("|")
    for name in names.split(";"):
        a = source(path, name)
        for k in ids.split():
            if a not in anchors[k]:
                anchors[k].append(a)

titles = [
    "Original class lattices and their exact scalar-extension column bases",
    "Original rational coefficient map and every-place integral criterion",
    "Original all-place normalized norm and literal ColVal construction",
    "Finite normal-order identity, highest-vector norm and hook bound",
    "Normalized integral Weyl slope from exact Fock duality and Cauchy–Binet",
    "Exact slope −log(T)/k of every column lattice in any supplied ColVal",
    "Exact polynomial determinant slope identity and the original lower bound",
    "Banaszczyk transference matched to the original trace-dual lattice",
    "Original coefficient ideal and signed finite/infinite determinant correction",
    "Exact class-map norm, tensor Fock bound and averaged trace estimate",
    "Original maximum slope with exact coefficient four",
    "All three GL4 family entries with their exact Closed and eventual quantifiers",
    "Complete eleven-field FamGLmin packet and explicit final assembly frontier",
]
deps = {
    "GLS1": ["RMP2"],
    "GLS2": ["GLS1", "GLE3", "GLE4"],
    "GLS3": ["GLS1", "GLS2", "RSL7"],
    "GLS4": [],
    "GLS5": ["GLS4", "IW5", "CB2"],
    "GLS6": ["MT2"],
    "GLS7": ["GLS4", "GLS5", "GLS6", "GLE3"],
    "GLS8": ["GLS6"],
    "GLS9": ["GLS6", "GLS8"],
    "GLS10": ["GLS5", "GLS8", "GLS9"],
    "GLS11": ["GLS4", "GLS9", "GLS10", "AH16"],
    "GLS12": ["GLS3", "GLS7", "GLS11", "RSL7"],
    "GLS13": ["GLS12", "MF19", "RSL1", "RSL2", "RSL3", "RSL5", "RSL6", "RSL7", "RSL8", "RSL9", "RSL10", "GLE5", "GLE6", "GLE9", "GLE12", "DSZ1", "DSZ2", "DSZ3"],
}
hyp = {
    "GLS1": ["Original D,u and supplied ColsTiedSym D; original definite S, frame, class bijection, atT.disc, class lattices and embeddings"],
    "GLS2": ["Same original ColsTiedSym and its Forms0 projection; adm3 D; no independent rational or integral form model"],
    "GLS3": ["Same ColsTiedSym/Forms0 as GLS1–GLS2; adm3; original norm0 at every coefficient embedding"],
    "GLS4": ["Integer partition ν, k≥1; literal leading-minor highest polynomial and Fock factorial normalization"],
    "GLS5": ["Same actual divided-power Weyl lattice and coefficient lattice; normalized exact integral duality IW5 and finite basis CB2"],
    "GLS6": ["Arbitrary original D,u and arbitrary supplied ColVal D u, including its precise bc_L, bc_norm, LatT and ranks"],
    "GLS7": ["Arbitrary original ColVal; exact source λ, determinant shifts and normalized tensor Weyl lattice"],
    "GLS8": ["Same actual ColVal and class lattice; original integral positive Hermitian form; GLS-BAN as the only new published input"],
    "GLS9": ["Same supplied ColVal; actual class c and short E-independent vectors in its Hermitian dual; signed determinant shifts"],
    "GLS10": ["Same coefficient map, original ColVal.inf, same finite ideal and every infinite-place frame"],
    "GLS11": ["Arbitrary original ColVal; original host discriminant and rank laws; no HidaSetting or TuSize hypothesis"],
    "GLS12": ["Original FamP and family class; for tCV retain the same-selector RealPlaceSecondLayerConditions; no new member-, word-, or place-dependent threshold"],
    "GLS13": ["Same class D3(3,A), original Duty and Closed RealPlaceSecondLayerConditions; inherited hU/hG and their published inputs; original finite characters; guarded FamU quantifiers"],
}
literature = {
    "id": "GLS-BAN", "classification": "A", "status": "Published theorem; all application hypotheses checked in GLS8",
    "author": "W. Banaszczyk",
    "title": "New bounds in some transference theorems in the geometry of numbers",
    "journal": "Mathematische Annalen", "volume": "296", "year": 1993,
    "pages": "625–635", "theorem": "Theorem (2.1)", "printed_page": 631,
    "doi": "10.1007/BF01445125", "url": "https://doi.org/10.1007/BF01445125",
    "primary_text_mirror": "https://paperzz.com/doc/7332762/new-bounds-in-some-transference-theorems-in-the-geometry-of",
    "primary_text_retrieval": "Original paper transcription, section 2, Theorem (2.1), printed p.631; publisher metadata independently checked. The primary text includes the n=1 equality case.",
    "statement_used": "For every full Euclidean lattice M in R^n, λ_i(M) λ_{n+1−i}(M*) ≤ n; only i=n is used.",
    "hypothesis_match": [
        "M is the original Hermitian dual L_c^vee embedded in S tensor_Q R; n=[E:Q]k.",
        "B(x,y)=Tr_{E/Q} h_S(x,y) is real symmetric positive definite, by CM trace invariance and original ColVal positivity.",
        "L_c^vee is a full finitely generated Z-lattice, hence discrete and spans the Euclidean space.",
        "Integer-pairing dual M* is exactly D_E^(-1)L_c, with no factor two in B.",
        "For nonzero z in M*, h(z,z) lies in D_E^(-2); ideal norm and AM–GM give λ_1(M*) ≥ sqrt([E:Q])/rd(E).",
        "Result gives k E-independent y_a in the original L_c^vee with Tr h(y_a,y_a)/(2f) ≤ k^2(2v)^2."
    ],
    "not_claimed": "The chapter does not reconstruct Banaszczyk's Gaussian transference proof; this is an explicit category A import.",
    "application_claim": "GLS8",
    "application_scope": "Any original ColVal D u and any original level-zero class c, before family, word, or place thresholds are introduced.",
    "original_source_facts": [
        "ColVal supplies the original full class lattice L_c, its positive definite Hermitian form, and LatT integrality.",
        "The original host has [E:Q]=2f and v=rd(E)/2; no redefinition of either normalization is made.",
        "The target ShortAt bound is Tr h(y_a,y_a)/(2f) <= k^2(2v)^2 for k E-independent vectors in L_c^vee."
    ],
    "independently_derived_normalization": [
        "For B=Tr h the integer-pairing dual of L_c^vee is D_E^(-1)L_c, since h is Hermitian and the codifferent is stable under CM conjugation.",
        "If z is nonzero in that trace dual, beta=h(z,z) is totally positive and belongs to D_E^(-2); therefore |Norm beta| disc(E)^2 >= 1.",
        "AM–GM gives B(z,z)>= [E:Q]/rd(E)^2, and hence lambda_1(M*)>=sqrt([E:Q])/rd(E).",
        "The published inequality in dimension n=[E:Q]k gives lambda_n(M)^2 <= [E:Q] k^2 rd(E)^2.",
        "Extracting k E-independent vectors and dividing by [E:Q]=2f yields the exact source target, with rd(E)=2v and no extra factor two or T."
    ],
}
claims = []
for i,title in enumerate(titles,1):
    k = f"GLS{i}"
    st = next(j for j,l in enumerate(lines) if l.strip() == f"% BEGIN {k}")
    en = next(j+1 for j,l in enumerate(lines) if l.strip() == f"% END {k}")
    b = "".join(lines[st:en]).encode()
    assert all(d in old or d in deps for d in deps[k]), (k, deps[k])
    claims.append({
        "id": k, "title": title, "introduced_in": "0.33",
        "classification": "A" if k == "GLS8" else "B",
        "status": "Complete human proof of the stated conditional result; independent review pending",
        "proof_status": "complete in the stated scope", "review_status": "pending independent review",
        "scope": "Original fields, family, selector, member, word, class, lattice, coefficient maps and all finite/infinite metrics; no replacement model",
        "depends_on": deps[k], "hypotheses_retained": hyp[k],
        "classical_inputs": ["GLS-BAN"] if i in (8,9,10,11,12,13) else [],
        "dependency_usage": ({"GLE4": "Original polynomial/rational/local dictionary only; adm3 is supplied independently as stated. GLS2 proves the rational class-value map directly and does not import RSL9's finite-character premise."} if k == "GLS2" else {}),
        "proof_location": {"file": "global_slope/main.tex", "paragraph": k, "label": "claim:"+k,
                           "line_start": st+1, "line_end": en,
                           "sha256": sha(b), "range_sha256": sha(b),
                           "file_sha256": sha(raw), "bytes": len(b)},
        "sources": anchors[k],
    })

input_files = [
    "rank_producer/main.tex", "global_local_estimates/main.tex", "global_local_estimates/provenance.json",
    "second_layer_global/main.tex", "second_layer_global/provenance.json",
    "integral_weyl/integral_weyl_section.tex", "complementary_basis/complementary_basis_section.tex",
    "metric_transport/main.tex", "arithmetic_hosts/main.tex", "mass_formula/main.tex",
    "degree_prime_size/main.tex", "dependency_audit_v0_32/remaining_leaf_register.json",
]
inputs = []
for file in input_files:
    b = (BASE/file).read_bytes()
    inputs.append({"file": file, "sha256": sha(b), "bytes": len(b),
                   "scope": "Unmodified inherited v0.32 proof input, used only in its stated conditional scope"})
standing = "The pinned Alpoge-Claude Lean proof is fully checked and correct. Open/D classifications concern human reconstruction or source understanding only."
not_closed = [
    "Actual compatible common selector, Duty and original RealPlaceSecondLayerConditions producer",
    "Final linkGLOBAL7_min/items/link8 numerical and identity installation, TASK_GL_FINAL_ASSEMBLY",
    "Full human-readable RH or unrestricted Dirichlet-GRH proof",
]
prov = {"schema": "rh-human-component-provenance/1", "artifact_version": "0.33", "date": "2026-11-22",
        "source_commit": PIN, "repository": "CocoSgt/riemann-hypothesis-lean", "component": "global_slope",
        "standing_assumption": standing, "main_sha256": sha(raw), "sha256": sha(raw),
        "range_convention": "Inclusive one-based physical source/proof lines. Every range hash covers exact UTF-8 bytes including line endings. Source sha256/file_sha256 alias the entire pinned blob; proof sha256/range_sha256 alias the exact proof block.",
        "claims": claims, "external_literature": [literature], "inherited_proof_inputs": inputs,
        "not_closed": not_closed,
        "claim_total": len(claims),
        "source_files": [{"path": p, "sha256": sha(b), "bytes": len(b), "line_count": len(ls),
                          "verified_equal_to_pinned_git_blob": True} for p,(b,ls,_) in sorted(cache.items())]}
dump("provenance.json", prov)
dump("literature.json", {"schema": "rh-exact-literature-application/1", "source_commit": PIN,
                         "main_sha256": sha(raw), "entries": [literature]})
dump("published_applications.json", [dict(literature,
    source_commit=PIN, main_sha256=sha(raw),
    proof_location=claims[7]["proof_location"])])

loc = [f"GLS source locators — CocoSgt/riemann-hypothesis-lean at {PIN}",
       "Source bytes checked against pinned git objects; inclusive one-based ranges.",
       f"main.tex SHA256 {sha(raw)}", ""]
for c in claims:
    p = c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")

nodes = [
    {"id": "SAME_COLSTIEDSYM", "role": "retained upstream producer input", "contract": "The original ColsTiedSym D, on the same selected D and family; its Forms0 and all original fields are projected from that witness."},
    {"id": "SAME_ADM3", "role": "closed conditional input", "contract": "Original adm3 D, proved pointwise from SAME_COLSTIEDSYM by inherited RSL7; no separate arithmetic producer."},
    {"id": "GIVEN_COLVAL", "role": "universally quantified argument", "contract": "Any literal ColVal D u on the original D,u; this argument is not an existential producer."},
    {"id": "GLS_BAN", "role": "published theorem certificate", "classification": "A", "status": "hypotheses checked", "claim": "GLS8", "literature_id": "GLS-BAN"},
    {"id": "GLOBAL_REAL_SECOND_LAYER", "role": "retained upstream producer", "classification": "C", "contract": "Closed RealPlaceSecondLayerConditions on the same class/family and selector, with the actual theta.real and cols fields; not constructed here."},
    {"id": "SAME_DUTY", "role": "retained upstream producer input", "contract": "Duty on the same class/family; its ChosenWall projection is retained for the future link8 consumer."},
    {"id": "INHERITED_FAMGLMIN_EIGHT_FIELDS", "role": "closed conditional input", "contract": "h2b,h2v,h3,hW,hμ,hI,hR,hB from MF19,RSL1–10,DSZ1–3,GLE5/6/9/12 on the same supplied second layer; FamU keeps HidaSetting."},
    {"id": "TASK_GL4_COLUMN_VALUES", "role": "closed implication task", "classification": "B", "status": "conditionally closed", "claims": ["GLS1", "GLS2", "GLS3", "GLS12"], "contract": "Original ColsTiedSym and adm3 imply literal ColVal; same-family RealPlaceSecondLayerConditions implies the exact unguarded eventual tCV."},
    {"id": "TASK_GL4_SLOPE_LOWER", "role": "closed implication task", "classification": "B", "status": "closed for every original ColVal", "claims": ["GLS4", "GLS5", "GLS6", "GLS7", "GLS12"], "contract": "For every D,u and any ColVal, source SlopeLow; hence Closed FamilySlopeLowerOpenPart with threshold zero."},
    {"id": "TASK_GL4_SLOPE_MAX", "role": "closed implication task", "classification": "B", "status": "closed using explicit A input GLS-BAN", "claims": ["GLS4", "GLS8", "GLS9", "GLS10", "GLS11", "GLS12"], "contract": "For every D,u and any ColVal, source SlopeMax(D,u,4); hence Closed FamilySlopeMaxOpenPart(4) with threshold zero."},
    {"id": "FAM_GLMIN_FOUR", "role": "closed conditional complete packet", "classification": "B", "claim": "GLS13", "contract": "Literal eleven-field FamGLmin(D3(3,A),4), conditional on same original second-layer input and inherited theorem scopes."},
    {"id": "TASK_GL_FINAL_ASSEMBLY", "role": "open implication reconstruction task", "classification": "B", "status": "human proof still required", "contract": "Remaining numerical and identity installations in linkGLOBAL7_min/items/link8 from the eleven-field packet to original LinkGLOBAL(2,CH,3,2,0), retaining TuSize,DGamSize,ChosenWall and original local inputs."},
    {"id": "COMMON_COMPATIBLE_SELECTOR", "role": "open upstream producer", "classification": "C", "status": "unchanged outside component", "contract": "One compatible selector supplies Duty and the original second-layer columns/real-place witnesses; no separate existential witnesses may be substituted."},
]
gates = [
    {"id": "GATE_ORIGINAL_ADM3", "status": "proved inherited implication", "all_of": ["SAME_COLSTIEDSYM"], "implies": "SAME_ADM3", "proof_claims": ["RSL7"]},
    {"id": "GATE_COLUMN_VALUES", "status": "proved sufficient AND implication", "all_of": ["SAME_COLSTIEDSYM", "SAME_ADM3"], "implies": "TASK_GL4_COLUMN_VALUES", "proof_claims": ["GLS1", "GLS2", "GLS3", "GLS12"]},
    {"id": "GATE_LOWER", "status": "proved universal implication", "all_of": ["GIVEN_COLVAL"], "implies": "TASK_GL4_SLOPE_LOWER", "proof_claims": ["GLS4", "GLS5", "GLS6", "GLS7"]},
    {"id": "GATE_MAX", "status": "proved universal implication using published A certificate", "all_of": ["GIVEN_COLVAL", "GLS_BAN"], "implies": "TASK_GL4_SLOPE_MAX", "proof_claims": ["GLS8", "GLS9", "GLS10", "GLS11"]},
    {"id": "GATE_ELEVEN_FIELDS", "status": "proved sufficient AND implication in inherited scopes", "all_of": ["GLOBAL_REAL_SECOND_LAYER", "INHERITED_FAMGLMIN_EIGHT_FIELDS", "TASK_GL4_COLUMN_VALUES", "TASK_GL4_SLOPE_LOWER", "TASK_GL4_SLOPE_MAX"], "implies": "FAM_GLMIN_FOUR", "proof_claims": ["GLS12", "GLS13"]},
]
for g in gates:
    g["same_object"] = "Every input and output uses the same original class/family, D,u, selector, forms, lattice and metrics. A universal ColVal argument does not assert its existence."
fields = [
    ("h2b", "Closed fam0 MassRatio₂", ["MF19"]),
    ("h2v", "Closed fam0 BaseVolumeEqualsMass", ["RSL1", "RSL2", "RSL3"]),
    ("h3", "Closed fam0 SigmaDegreeTwoSidedBoundOfGap", ["DSZ1", "DSZ2", "DSZ3"]),
    ("hZa", "Closed FamilySlopeLowerOpenPart", ["GLS7", "GLS12"]),
    ("hZb", "Closed FamilySlopeMaxOpenPart(4)", ["GLS11", "GLS12"]),
    ("tCV", "Closed: exists x0, forall x>=x0, forall i,u, Nonempty ColVal(D x i,u)", ["GLS3", "GLS12"]),
    ("hW", "Closed guarded FamU Nonempty FreeT", ["RSL7", "RSL8", "RSL9"]),
    ("hμ", "Closed guarded FamU SlopeLine", ["RSL10"]),
    ("hI", "Closed guarded FamU HeckeIntegralLevelZero", ["GLE5", "GLE12"]),
    ("hR", "Closed guarded FamU HeckeRamifiedLevelZero", ["GLE9", "GLE12"]),
    ("hB", "Closed guarded FamU SecondBranchInclusionLength", ["GLE6", "GLE12"]),
]
closure = {"schema": "rh-conditional-closure/1", "artifact_version": "0.33", "component": "global_slope",
           "source_commit": PIN, "main_sha256": sha(raw), "sha256": sha(raw),
           "provenance_sha256": sha((HERE/"provenance.json").read_bytes()),
           "standing_assumption": standing,
           "closure_semantics": "Completed implications retain their producer hypotheses. All_of in a proved gate is sufficient only for its explicitly scoped output; no open implication is treated as established.",
           "nodes": nodes, "sufficient_implication_gates": gates,
           "famGLmin_fields": [{"field": n,"contract": c,"proof_claims": p} for n,c,p in fields],
           "quantifier_checks": [
               "SlopeLow and SlopeMax(4) hold for any given ColVal, on all original D,u, before any family specialization.",
               "FamilySlopeLowerOpenPart and FamilySlopeMaxOpenPart(4) have fam0 threshold 0; no HidaSetting, TuSize or arbitrary hidden size condition is needed.",
               "The same second-layer record gives adm3 pointwise by RSL7; source-style tCV threshold max(a,b,Fm.x1+1) is chosen before i,u.",
               "Closed quantifiers are epsilon cutoff first, then a TransportedAlt tuple before Fm and CH; finite conjunction takes the minimum cutoff and tuple supremum.",
               "hI,hR,hB,hW,hμ keep the exact FamU HidaSetting guard; no TuSize hypothesis is needed merely to form the guarded packet.",
               "The full LinkGLOBAL output is not closed by FamGLmin packet formation; TASK_GL_FINAL_ASSEMBLY remains B.",
           ],
           "not_closed": not_closed,
           "review_status": "Independent mathematical review pending; final registry may supersede this historical status."}
dump("closure.json", closure)

refs = {(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
ids = {n["id"] for n in nodes}
assert len(ids)==len(nodes)
assert all(g["implies"] in ids and all(x in ids for x in g["all_of"]) for g in gates)
assert len(fields)==11
result = {"status": "PASS", "source_commit": PIN,
          "main_sha256": sha(raw), "provenance_sha256": sha((HERE/"provenance.json").read_bytes()),
          "closure_sha256": sha((HERE/"closure.json").read_bytes()),
          "claim_count": len(claims), "source_reference_count": sum(len(c["sources"]) for c in claims),
          "distinct_source_range_count": len(refs), "source_file_count": len(cache),
          "inherited_file_count": len(inputs), "all_source_blobs_match_pin": True,
          "all_claim_dependencies_resolve": True, "fresh_claim_prefix": True,
          "all_closure_references_resolve": True, "famGLmin_field_count": 11,
          "not_a_lean_recheck": True}
dump("validation.json", result)
report = f"""GLS global-slope reconstruction, v0.33

Standing assumption: {standing}

Outcome
GLS1–3 construct literal ColVal from the original ColsTiedSym and adm3;
GLS4–7 prove the exact original lower slope;
GLS8–11 prove the exact original maximum slope with coefficient 4;
GLS12 installs all three family entries with complete quantifier order;
GLS13 forms the full eleven-field FamGLmin(D3(3,A),4) conditional packet.

Main mathematical checks
The embedding is rhoC=embE o CM conjugation o sigmaOf. The local primal
frame Y and original dual frame (Y*G)^(-1) are connected by the literal
transpose identity, including signed determinant powers. The all-place
norm uses each original class weight 1; classwise frame independence
is obtained by restricting the original rational form to one class.

GLS4 proves the determinant normal-order identity by an explicit
derivative-contraction recurrence and sign-reversing transposition;
there is no unproved Capelli lemma in this chapter. The norm recurrence
gives the exact hook ratio. IW5 plus the coefficient-lattice basis CB2
and integral Cauchy–Binet give the normalized Weyl Gram bound.

Every ColVal column lattice has slope −log(T)/k: exact scalar extension
preserves normalized slope, Hermitian duality changes its sign, and
[L^vee:L]=T^(2f) supplies the index. No replacement lattice or metric
is used. The signed determinant ideal and archimedean frame term
cancel to −sum_tau s_tau log(T).

New published theorem, fully checked application
GLS-BAN: Banaszczyk, Math. Ann.296(1993),625–635, Theorem2.1,p.631,
https://doi.org/10.1007/BF01445125 . Original-paper primary transcription:
https://paperzz.com/doc/7332762/new-bounds-in-some-transference-theorems-in-the-geometry-of
The theorem is used only for the original trace Euclidean lattice
M=L_c^vee of dimension [E:Q]k. M*=D_E^(-1)L_c. Original integrality,
the codifferent norm and AM–GM give lambda1(M*)>=sqrt([E:Q])/rd(E).
This proves normalized squared norms <=k²(2v)². The trace average,
monomial coefficients and v>=2 give log(4k^4v²)<=4log(kv).

Closed implication tasks
TASK_GL4_COLUMN_VALUES, TASK_GL4_SLOPE_LOWER, TASK_GL4_SLOPE_MAX.
All are conditional in exactly the source sense; original compatible
second-layer/selector producers remain inputs. Slope statements work
for every ColVal; the column-value producer is supplied only from the
same original forms. FamU guards are unchanged. FamGLmin has all11fields.

Remaining B task
TASK_GL_FINAL_ASSEMBLY is narrowed to the actual numerical and identity
installations of linkGLOBAL7_min / linkGLOBAL7_items / FamGLmin.link8.
Precise sources:
src/Formalism/SharpRestriction/GlobalSchurBounds/LinkMin.lean
  linkGLOBAL7_min; linkGLOBAL7_items; items_of_min.
src/Formalism/SharpRestriction/GlobalSchurBounds/LogXLowerFamilyOfTheorems.lean
  FamGLmin.link7; FamGLmin.link8.
The final parameters remain (Cabs,CH,C0,eD,eL)=(2,CH,3,2,0), C5=4.
Duty provides the same ChosenWall; D3 membership provides same TuSize.
No claim is made that merely listing the source's calls reconstructs
the PartFive/ConclusionF5/ConclusionF6/count/frame/loss conversions.

Provenance
{len(claims)} new claims; {result['source_reference_count']} claim/source references;
{len(refs)} distinct ranges in {len(cache)} pinned files. All bytes verified.
{len(inputs)} unmodified inherited file inputs checked and hashed.
main.tex SHA256 {sha(raw)}
provenance.json SHA256 {result['provenance_sha256']}
closure.json SHA256 {result['closure_sha256']}

Reproduction
python build_provenance.py --source /path/to/pinned_checkout --baseline /path/to/reconstruction_v032
All proof blocks and exact inclusive source ranges are in provenance.json
and source_locators.txt. No source or predecessor file is modified.
Independent mathematical review is pending at generation time.
"""
(HERE/"report.txt").write_text(report)
print(json.dumps(result, ensure_ascii=False, indent=2))
