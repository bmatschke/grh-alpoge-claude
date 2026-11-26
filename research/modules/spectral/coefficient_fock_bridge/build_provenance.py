#!/usr/bin/env python3
"""Rebuild the CFB component against the pinned source and frozen v0.35.

Usage:
  python3 build_provenance.py --source /path/to/lean_source \
                             --baseline /path/to/reconstruction_v035

Outputs are written only beside this script. No Lean kernel replay is claimed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENT = "coefficient_fock_bridge"
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v035")
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"CFB\d+", k) for k in old)
raw = (HERE / "main.tex").read_bytes()
assert not any(c < 32 and c not in (9, 10) for c in raw)
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}


def source(path, anchor):
    name, sep, line_filter = anchor.partition("@")
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        ls = b.decode().splitlines(keepends=True)
        ds = [(i, DECL.match(x).group(1)) for i, x in enumerate(ls) if DECL.match(x)]
        cache[path] = (b, ls, ds)
    b, ls, ds = cache[path]
    found = [(j, i) for j, (i, n) in enumerate(ds)
             if n == name and (not sep or i + 1 == int(line_filter))]
    assert len(found) == 1, (path, anchor, found)
    j, st = found[0]
    en = ds[j + 1][0] if j + 1 < len(ds) else len(ls)
    for k in range(st + 1, en):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)", ls[k]):
            en = k
            break
    while en > st + 1 and not ls[en - 1].strip():
        en -= 1
    rb = "".join(ls[st:en]).encode()
    return {
        "path": path, "declaration": name, "source_spelling": name,
        "declaration_anchor": anchor,
        "line_start": st + 1, "line_end": en,
        "sha256": sha(b), "file_sha256": sha(b),
        "range_sha256": sha(rb), "range_bytes": len(rb),
        "first_line": ls[st].rstrip(), "verified_equal_to_pinned_git_blob": True,
        "role": "Exact original definition, contract or corresponding formal argument. Its independent human proof is the hashed CFB block; the declaration is not used as a substitute for that proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


anchors = {f"CFB{i}": [] for i in range(1, 14)}
for line in (HERE / "source_anchors.txt").read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    ids, path, names = line.split("|")
    for name in names.split(";"):
        a = source(path, name)
        for key in ids.split():
            if a not in anchors[key]:
                anchors[key].append(a)

titles = [
    "Literal polynomial base change and exact inverse-transpose action",
    "Unique complex extension of the supplied original coefficient map",
    "Rational approximation with the original finite component removed",
    "Original coefficient covariance at every source-real point",
    "Specified-frame polynomial embedding with range exactly VV",
    "Compact unitary cyclicity of the literal extremal polynomial",
    "Original ranks, parity and integral strictly decreasing row",
    "Exact floor removal and both antitone positive minor-degree sequences",
    "Forced original lamLdef from all admissible one-based WeightData",
    "Original signed enumeration and exact lowest compact weight",
    "All three integral character twists and both literal weight identities",
    "Complete ArithAt and installation on actual c0L, cV and BV",
    "One same-datum coefficient-and-weight package before every family parameter",
]
deps = {
    "CFB1": ["HP1"],
    "CFB2": ["CFB1", "SE1"],
    "CFB3": ["MF3", "HCU14"],
    "CFB4": ["CFB1", "CFB2", "CFB3", "HCU14"],
    "CFB5": ["CFB1", "CFB2", "CFB4"],
    "CFB6": ["CFB1", "HP1", "HP2"],
    "CFB7": [],
    "CFB8": ["CFB7"],
    "CFB9": ["CFB7", "CFB8"],
    "CFB10": ["CFB7", "CFB8", "HCU20"],
    "CFB11": ["CFB7", "CFB8", "CFB9", "CFB10"],
    "CFB12": ["CFB5", "CFB7", "CFB8", "CFB9", "CFB10"],
    "CFB13": ["CFB6", "CFB8", "CFB11", "CFB12", "HCU20"],
}
hyps = {
    "CFB1": ["A finite index set, arbitrary rank n>=0, original dominant integral weights, and a field embedding K into C. The original bVV is used as the supplied basis of the literal finite polynomial model."],
    "CFB2": ["The original phi-semilinear c0; complex independence and spanning of the images of the original bVV basis, exactly as supplied by CoefMapTie."],
    "CFB3": ["Original D, Hermitian V, theta and IsInfFam; original adelic topology, rational subgroup and finite/infinite kernels."],
    "CFB4": ["Original D,V,theta,c,lam,c0 and exactly IsInfFam(theta), c.Is, CoefMapTie(V,c.coef,c0,rhoVr(labLL(D),lam))."],
    "CFB5": ["The same original inputs as CFB4 and a specified tuple BS of invertible matrices; no isometry or additional intertwiner premise."],
    "CFB6": ["The literal VV(C,lam), original dominant integral weights, original ten(extremal) and full standard compact unitary tuple; no new cyclicity premise."],
    "CFB7": ["Original D7 and i:Fin(D.R.m), tau:D.what2.Tau, retaining all given Ranks, HCParam and Spaces fields."],
    "CFB8": ["Original data of CFB7 and literal aPl/aMi definitions. No ArithAt or arithmetic-of-weights theorem is an input."],
    "CFB9": ["Original data of CFB7, exact IsLamPrime/lamLdef definitions and original one-based WeightData. Unused values of auxiliary v/b functions are arbitrary and proved irrelevant."],
    "CFB10": ["Original D,i and sigma=embLL; any original DSModel for parAt(Wc,sigma), with its stored enumeration and the source's sign-order condition."],
    "CFB11": ["Same original D,i,sigma=embLL and DSModel/sign order as CFB10. The original lamLdef, floors and weights are preserved."],
    "CFB12": ["ArithAt needs only original D,i,tau. Its coefficient-model installation additionally retains one original RealDat R with R.IsFam and R.IsModels and one choice of the original fam_tie witnesses."],
    "CFB13": ["One same original RealDat R with R.IsFam, R.IsModels and its stored hv0. The whole c0L family is chosen once from R.IsFam.tie, before i and before every family parameter t."],
}
scopes = {
    "CFB1": "All ranks including zero and all finite index sets including the empty set; equality inside the literal polynomial ring.",
    "CFB2": "For every supplied c0 satisfying its exact basis conditions there exists a unique e, with equality on every rational coefficient vector.",
    "CFB3": "For each original pure-real point and each open neighborhood, there are one rational gamma and one finite k with gamma*k pure-real and in the neighborhood.",
    "CFB4": "One e determined by c0 works for all original u in GinfC and all complex coefficient vectors.",
    "CFB5": "One j determined by c0 and the specified BS has exact range VV and all-original-real-point covariance; no norm assertion is made.",
    "CFB6": "Exact span equality for the full original compact tuple orbit, including empty index/rank-zero cases.",
    "CFB7": "Pointwise for every original D,i,tau; all rank guards are checked at i+1.",
    "CFB8": "Every valid positive and negative degree index; the q=0 case is explicitly included.",
    "CFB9": "The original selected lamLdef is forced by a unique weight; the comparison with WeightData is universal over every allowed auxiliary witness.",
    "CFB10": "Every original model at sigma=embLL; no other coefficient embedding is claimed.",
    "CFB11": "For each D,i and original base model, there are x1,x2,x3 on Tau, with all three Q identities and both all-index K/U weight identities.",
    "CFB12": "Every original ArithAt field is proved. On supplied R, one j_i per i comes from the same c0L/cV/BV and has no t dependence.",
    "CFB13": "Choose the original fam_tie witnesses once; for every i choose one package, then all family parameters t. This is the finite coefficient/weight input to exists_ioP, not the complete ioP theorem.",
}
claims = []
for i, title in enumerate(titles, 1):
    key = f"CFB{i}"
    starts = [j for j, line in enumerate(lines) if line.strip() == f"% BEGIN {key}"]
    ends = [j + 1 for j, line in enumerate(lines) if line.strip() == f"% END {key}"]
    assert len(starts) == len(ends) == 1, key
    st, en = starts[0], ends[0]
    assert st < en and anchors[key]
    b = "".join(lines[st:en]).encode()
    assert all(d in old or d in deps for d in deps[key]), (key, deps[key])
    claims.append({
        "id": key, "title": title, "introduced_in": "0.36", "classification": "B",
        "status": "Complete human proof in the stated conditional scope; independent review pending",
        "proof_status": "complete in the stated scope", "review_status": "pending independent review",
        "scope": scopes[key], "quantifier_scope": scopes[key],
        "depends_on": deps[key], "hypotheses_retained": hyps[key],
        "classical_inputs": [],
        "inherited_classical_scope": "No new published theorem application. Only the already reconstructed HP finite polynomial arguments, elementary SE basis extension, MF3 weak approximation, and HCU14/HCU20 original-object dictionaries are reused in their stated scopes.",
        "proof_location": {
            "file": COMPONENT + "/main.tex", "paragraph": key, "label": "claim:" + key,
            "line_start": st + 1, "line_end": en,
            "sha256": sha(b), "range_sha256": sha(b), "file_sha256": sha(raw), "bytes": len(b),
        },
        "sources": anchors[key],
    })
claims[2]["dependency_usage"] = {
    "MF3": "Only the Cayley/weak-approximation argument for the same fixed Hermitian space; no mass formula, nonzero-norm orbit theorem or strong approximation is used.",
    "HCU14": "The exact continuous inverse of original theta evaluation and finite/infinite factor decomposition.",
}
claims[9]["dependency_usage"] = {
    "HCU20": "Only its base-label identity lab(embLL,tau)=tau and parAt at the original embedding; this computation depends on D alone. The actual signed enumeration and lowK calculation are reconstructed in CFB10 for every indicated model.",
}
claims[11]["dependency_usage"] = {
    "CFB10": "For ArithAt only the algebraic kapW identities, which depend on CFB7-CFB8 and no DSModel. The separate coefficient installation uses CFB5.",
}
claims[12]["dependency_usage"] = {
    "HCU20": "Only sg0=embLL and the same original model/ordering identification; full-lowest-type existence belongs to the inherited HCU consumer and is not claimed anew here.",
}

# Check the new implication DAG independently of source-anchor bookkeeping.
visiting, visited = set(), set()
def visit(key):
    if key in visited or key not in deps:
        return
    assert key not in visiting, ("new-claim dependency cycle", key)
    visiting.add(key)
    for d in deps[key]:
        visit(d)
    visiting.remove(key)
    visited.add(key)
for key in deps:
    visit(key)

input_files = [
    "stage_existence/main.tex", "stage_existence/provenance.json",
    "mass_formula/main.tex", "mass_formula/provenance.json",
    "chain_closure_core/main.tex", "chain_closure_core/provenance.json",
    "holomorphic_uniqueness/main.tex", "holomorphic_uniqueness/provenance.json",
    "continuation_notes_v0_35/next_base_extension.txt",
]
inputs = []
for name in input_files:
    b = (BASE / name).read_bytes()
    inputs.append({"file": name, "sha256": sha(b), "file_sha256": sha(b), "bytes": len(b),
                   "scope": "Unmodified v0.35 inherited proof or continuation input, used only in the explicitly stated scope."})

standing = "The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Remaining obligations concern the human reconstruction only."
not_closed = [
    "Existence of the common original D/family/RealDat and its compatible IsFam/IsModels producers.",
    "An arbitrary replacement coefficient model or an assumed unexplained real intertwiner; neither is used.",
    "A unitary normalization of j; the coefficient extension is fixed by original c0 and BV, and normalization belongs to the subsequent Fock map.",
    "The joint-harmonic bottom and lowest-type tensor map, the actual Weil action and unit-vector Delta normalization needed to finish exists_ioP.",
    "Analytic boundedness, FinPair/IsReg, Sobolev continuation, and the complete theta/form construction.",
    "The full human RH/Dirichlet-GRH proof or any remaining arithmetic CountI/II/III/V producer.",
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.36", "date": "2026-11-22",
    "source_commit": PIN, "repository": "CocoSgt/riemann-hypothesis-lean", "component": COMPONENT,
    "standing_assumption": standing, "main_sha256": sha(raw), "main_tex_sha256": sha(raw), "sha256": sha(raw),
    "range_convention": "Inclusive one-based physical lines. Every range hash covers exact UTF-8 bytes and line endings; sha256 aliases are explicit.",
    "metadata_builder": {"file": "build_provenance.py", "sha256": sha(Path(__file__).read_bytes()),
                         "portable_invocation": "python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v035"},
    "claims": claims, "claim_total": len(claims), "external_literature": [],
    "inherited_proof_inputs": inputs, "not_closed": not_closed,
    "source_files": [{"path": p, "sha256": sha(b), "file_sha256": sha(b), "bytes": len(b),
                      "line_count": len(ls), "verified_equal_to_pinned_git_blob": True}
                     for p, (b, ls, _) in sorted(cache.items())],
}
dump("provenance.json", prov)
dump("published_applications.json", [])
contracts = [
    {
        "id": "CFB_COMPLEX_EXTENSION", "classification": "B", "status": "closed conditional implication",
        "claims": ["CFB1", "CFB2"],
        "contract": "The specified original semilinear c0 whose bVV images are complex-independent and spanning extends uniquely to e:VV(C,lam) equiv c.W, with e(mapVV(v))=c0(v) for every original v.",
        "requires": ["original polynomial module and bVV basis", "exact CoefMapTie independence and spanning fields"],
        "dependency_mode": "sufficient conditional conjunction",
        "quantifiers": "For every K embedding into C and every specified c0; one unique e before all vectors.",
    },
    {
        "id": "CFB_ORIGINAL_REAL_POLYNOMIAL_MODEL", "classification": "B", "status": "closed conditional implication",
        "claims": ["CFB3", "CFB4", "CFB5"],
        "contract": "Literal CoefReal.exists_poly_model: j:c.W->Pol(C,Tau,n), range(j)=VV(C,lam), and j(c.rho(u)w)=vact(lam,BS^-1 compAt(theta,mt(u)) BS)(j(w)) for every original u in GinfC and every w.",
        "requires": ["same original D,V,theta,c,lam,c0", "IsInfFam(theta)", "c.Is", "CoefMapTie(V,c.coef,c0,rhoVr(labLL(D),lam))", "the specified BS is invertible at every tau"],
        "dependency_mode": "sufficient AND",
        "explicit_map": "j = inclusion o rhoK(lam,invTrK(BS^-1)) o e^-1; e is fixed by c0 on mapVV.",
        "quantifiers": "One j from these exact inputs, then every original real u and coefficient w; no member parameter occurs.",
        "not_required": "An extra real intertwiner, irreducibility comparison, or arbitrary replacement coefficient space.",
    },
    {
        "id": "CFB_COMPACT_EXTREMAL_CYCLICITY", "classification": "B", "status": "closed finite implication",
        "claims": ["CFB6"],
        "contract": "VV(C,lam) equals the complex span of vact(u) ten(extremal(lam)) for u in the original product Kset(allPos).",
        "requires": ["original dominant integral weights and literal VV polynomial module"],
        "dependency_mode": "sufficient supplied-definition implication",
        "quantifiers": "Every finite index set and every rank including zero; the literal extremal polynomial is fixed.",
    },
    {
        "id": "CFB_FULL_ARITH_AT", "classification": "B", "status": "closed original-data implication",
        "claims": ["CFB7", "CFB8", "CFB9", "CFB10", "CFB12"],
        "contract": "Every original D7,i,tau satisfies all fields of InfinityTypes.ArithAt, including every floor, both antitone/positive sequences, both kap identities, integer dShift, universal lamPrime_eq, forced original lamLdef and coef_eq.",
        "requires": ["original D7 with its existing Ranks, HCParam and Spaces fields", "i:Fin(D.R.m), tau:D.what2.Tau"],
        "dependency_mode": "sufficient original-field implication",
        "quantifiers": "All original D,i,tau; lamPrime_eq is universal over all WeightData satisfying the original IsDataOf. No DSModel is needed for this record.",
    },
    {
        "id": "CFB_EXACT_MINOR_WEIGHTS", "classification": "B", "status": "closed original-data implication",
        "claims": ["CFB10", "CFB11"],
        "contract": "Literal weights_of_minors with x1=-e+n/2, x2=-e-n/2, x3=-[(p-q)/2+(-e-1/2)], all three rational exponent identities, lowK=wtK and wtU=-lamLdef.w.",
        "requires": ["original D,i", "sigma=embLL", "original DSModel(Wc(D,i),parAt(Wc,sigma))", "original epsilon order true exactly at a<p"],
        "dependency_mode": "sufficient AND",
        "quantifiers": "For every indicated original base model there are integer functions x1,x2,x3 on Tau, then all tau and all target/source indices; q=0 included.",
        "sign_guard": "x3 is minus the entire bracket; its e coefficient is positive. Arithmetic dShift is distinguished from lam.detShift.",
    },
    {
        "id": "CFB_SAME_R_BEFORE_T_INSTALLATION", "classification": "B", "status": "closed conditional installation",
        "claims": ["CFB12", "CFB13"],
        "contract": "The same original R.IsFam and R.IsModels supply, for each i, the exact j_i/c0L/BV coefficient bridge, compact cyclicity, all ArithAt fields, ranks, ordered original M_i=R.MW(i,sg0), and all three twists/both weight identities used at exists_io_poly inside exists_ioP.",
        "requires": ["one unchanged original RealDat R", "R.IsFam", "R.IsModels", "the original stored hv0"],
        "dependency_mode": "sufficient AND",
        "quantifiers": "Choose the full original fam_tie witness once; forall i exists one coefficient-and-weight package; then forall original family parameters t. This component constructs no io map by itself.",
        "same_object_guard": ["c0=c0L(i) from the same hF.tie", "c=R.cV(i)", "BS=R.BV(i)", "lam=original lamLdef", "M=R.MW(i,sg0)", "theta=R.theta", "sg0=embLL by the original hv0"],
        "endpoint_for_joint_harmonic_consumer": "CFB13",
    },
]
closure = {
    "schema": "rh-human-component-closure/1", "version": "0.36", "component": COMPONENT,
    "source_commit": PIN, "standing_assumption": standing,
    "main_sha256": sha(raw), "main_tex_sha256": sha(raw), "sha256": sha(raw),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claim_ids": [c["id"] for c in claims], "closed_contracts": contracts,
    "shared_bindings": [
        "The original D, host CM field, coefficient field/embedding, real evaluations, rational subgroup and finite/infinite kernels are unchanged.",
        "The same original c0L, cV, BV, theta, MW, sg0 and chosen fam_tie witness are used together.",
        "The range is equality with VV(C,lam) as a subspace of the original polynomial ring, not merely an isomorphic module.",
        "The source action contains its exact inverse transpose; the BS conjugation has order BS^-1 * compAt * BS.",
        "Original natural-number floors and reversals are evaluated with all index guards; the empty negative block is included.",
        "The original lamLdef is forced by every admissible auxiliary WeightData, so its existential fallback is excluded.",
        "One package per i is chosen before t; there is no eventual threshold or parameter-dependent coefficient identification.",
    ],
    "remaining_inputs": [
        {"classification": "C", "role": "retained upstream compatible producer",
         "contract": "Existence of the common original family/RealDat with simultaneous IsFam and IsModels, on the actual class and common selector of the selected proof route."},
        {"classification": "B", "role": "separate finite consumer, owned by the simultaneous Fock branch",
         "contract": "Joint-harmonic bottom, actual lowest-type/Fock bilinear map, given Weil compact laws and unit-vector Delta normalization; CFB supplies their exact coefficient and weight inputs."},
        {"classification": "C", "role": "separate analytic producer/installation frontier",
         "contract": "Any still required analytic boundedness, same-data FinPair/IsReg and Sobolev/theta extension hypotheses, with their detailed current audit classifications preserved."},
    ],
    "not_closed": not_closed,
    "review_status": "pending independent mathematical review",
}
dump("closure.json", closure)

loc = [f"CFB source locators — {PIN}",
       "Inclusive one-based source and proof ranges; exact byte hashes.",
       f"main.tex SHA256 {sha(raw)}", ""]
for c in claims:
    p = c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
ranges = {(s["path"], s["line_start"], s["line_end"], s["range_sha256"])
          for c in claims for s in c["sources"]}
validation = {
    "status": "PASS", "source_commit": PIN, "main_sha256": sha(raw), "claims": len(claims),
    "claim_source_references": sum(len(c["sources"]) for c in claims),
    "distinct_source_ranges": len(ranges), "source_files": len(cache), "inherited_files": len(inputs),
    "checks": [
        "Exact source HEAD and every referenced pinned Git blob verified",
        "Unique anchored source declarations and unique BEGIN/END proof blocks",
        "All depends_on values are indexed new or inherited claim IDs; new dependency graph acyclic",
        "All source/proof ranges and inherited inputs have exact byte hashes",
        "Fresh CFB prefix and no unexpected control bytes",
    ],
    "not_performed": "No Lean compilation or kernel replay; mathematical peer review is separate.",
}
dump("validation.json", validation)
report = """v0.36 original coefficient/Fock bridge — CFB1–CFB13

Complete finite endpoints:
  CFB5: literal CoefReal.exists_poly_model, using the supplied original
  c0, c and BS, with range EXACTLY VV(C,lam) and covariance for every
  original source-real point. It also gives injectivity and the exact
  value of j on the original c0 image.

  CFB6: the original ten(extremal) is cyclic under the full original
  standard compact unitary tuple. The proof uses complexified Cayley
  coordinates and the already reconstructed HP2 irreducibility.

  CFB7–CFB12: all original ArithAt fields. The proof removes the literal
  floors by integrality and endpoint gaps, checks both antitone sequences,
  constructs a dominant coefficient weight, proves every admissible
  WeightData gives that same weight, and therefore identifies the actual
  selected lamLdef and excludes its fallback. No ArithAt premise is added.

  CFB11: full weights_of_minors at the original base coefficient embedding,
  including all three integer rational exponent identities and both
  signed weight identities. In particular x3=−[(p−q)/2−e−1/2], whose
  coefficient of e is POSITIVE. The negative block may be empty.

  CFB13: one same-R/i coefficient-and-weight package, before every t,
  at the exact exists_io_poly call inside original exists_ioP.

The real action is proved, not assumed: the original CoefMapTie first
gives rational covariance on the precise coefficient map. Its basis
images extend uniquely to C. Rational unitary weak approximation with
the finite component removed, finite-part triviality and orbit continuity
then give all original real points. The explicit original frame conjugation
gives j, with no arbitrary replacement module or unspecified intertwiner.

Retained original inputs: one compatible RealDat R with IsFam and IsModels;
the same c0L family selected from its fam_tie; cV,BV,theta,MW and hv0.
Their compatible existence remains an upstream producer. This chapter
does not by itself construct ioP, its unit-vector Delta normalization,
the actual Weil action or the subsequent analytic theta/Sobolev extension.
The sibling simultaneous Fock branch receives CFB5, CFB6, CFB11–CFB13.

No new published theorem is used. Inherited claims: HP1/HP2 finite polynomial
arguments, SE1 basis extension, MF3 Cayley weak approximation, and
HCU14/HCU20 exact original-object dictionaries, in their recorded scopes.

Every new claim has an independently hashed proof range and exact pinned
source ranges. build_provenance.py is portable with --source and --baseline.
The formal proof is assumed fully checked and correct; no kernel replay
is asserted. All statuses here concern the human reconstruction.
"""
report += f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE / 'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE / 'closure.json').read_bytes())}\n"
report += f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} pinned source files; {len(inputs)} inherited files.\n"
(HERE / "report.txt").write_text(report)
print(json.dumps({**validation,
                  "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
                  "closure_sha256": sha((HERE / "closure.json").read_bytes())}, indent=2))
