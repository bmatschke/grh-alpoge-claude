#!/usr/bin/env python3
"""Rebuild CSR provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v036 --peer-root /path/to/work_v037

Only files beside this script are written. The peer root contains the original
smooth_representatives component, whose SPR25 is used in CSR22. This is source
backtracking and human-proof bookkeeping, not a Lean kernel replay.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENT = "common_selected"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v036")
parser.add_argument("--peer-root", type=Path, default=HERE.parent)
args = parser.parse_args()
SOURCE, BASE, PEER = args.source.resolve(), args.baseline.resolve(), args.peer_root.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"CSR\d+", key) for key in old)
peer_ledger_path = PEER / "smooth_representatives/provenance.json"
peer_ledger = json.loads(peer_ledger_path.read_text())
peer = {c["id"]: c for c in peer_ledger["claims"]}
assert "SPR25" in peer
raw = (HERE / "main.tex").read_bytes()
assert not any(c < 32 and c not in (9, 10) for c in raw)
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r"^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}


def source(path, anchor):
    name, sep, n = anchor.partition("@")
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        ls = b.decode().splitlines(keepends=True)
        ds = [(i, DECL.match(s).group(1)) for i, s in enumerate(ls) if DECL.match(s)]
        cache[path] = (b, ls, ds)
    b, ls, ds = cache[path]
    found = [(j, i) for j, (i, x) in enumerate(ds) if x == name and (not sep or i + 1 == int(n))]
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
        "declaration_anchor": anchor, "line_start": st + 1, "line_end": en,
        "sha256": sha(b), "file_sha256": sha(b), "range_sha256": sha(rb),
        "range_bytes": len(rb), "first_line": ls[st].rstrip(),
        "verified_equal_to_pinned_git_blob": True,
        "role": "Original definition, exact contract or corresponding formal argument. The independently written CSR block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


anchors = {f"CSR{i}": [] for i in range(1, 23)}
for s in (HERE / "source_anchors.txt").read_text().splitlines():
    if not s or s.startswith("#"):
        continue
    ids, path, names = s.split("|")
    for name in names.split(";"):
        entry = source(path, name)
        for key in ids.split():
            assert key in anchors, key
            if entry not in anchors[key]:
                anchors[key].append(entry)

titles = [
    "One literal level-row reader",
    "Character membership and original signed weights",
    "Actual ramified coordinate equivalence and all-place Hermitian metric",
    "Original relative-determinant character, unchanged kernels and literal period point",
    "One original ReadC with all six fields",
    "Complete original compatible column record",
    "All ten ColPins on the same columns",
    "Simultaneous transport through the entire original package",
    "Complete original SelC.cols_of_witnesses",
    "Exact original evaluation placement and normalization",
    "Inactive scalar update preserves both original row metrics",
    "Exact reFace, error and thirteen-map reading update",
    "Actual TwIn and TwArgs construction conditional on original DivDef3",
    "Original selected realization with one period update",
    "Original standard character, StageAt and NExp transports",
    "Every field of original RealIn and RealTB",
    "Terminal-coordinate scalar cancellation in the actual lower map",
    "Complete original RowSideDetermined record",
    "Finite carrier selection and exact RecIn/PartsRow assembly",
    "Selected-prime equality and both distinguished contractions",
    "Original seven-field Bundle and every BTw/BWit field",
    "Exact eventual same-R BunU implication",
]
deps = {
    "CSR1": ["TL2", "TL6", "TL7", "TG3"],
    "CSR2": [],
    "CSR3": ["TL4", "TL5", "TL6", "TL7", "TX10", "SE5"],
    "CSR4": ["CSR3", "CI17", "CI18", "TL12", "TL13", "FC8", "TX10", "TX14", "HF14", "HF15"],
    "CSR5": ["CSR1", "CSR3", "CSR4"],
    "CSR6": ["CSR1", "CSR2", "CSR4"],
    "CSR7": ["CSR1", "CSR2", "CSR6", "CI17", "CI18"],
    "CSR8": ["CSR6", "CSR7"],
    "CSR9": ["CSR5", "CSR8"],
    "CSR10": [],
    "CSR11": [],
    "CSR12": ["CSR11"],
    "CSR13": ["CSR9", "CSR11", "CSR12"],
    "CSR14": ["CSR9", "CSR10", "CSR12", "CSR13"],
    "CSR15": [],
    "CSR16": ["CSR14", "CSR15"],
    "CSR17": ["TG12", "TX14", "TX15", "TX16"],
    "CSR18": ["CSR8", "CSR12", "CSR13", "CSR17", "TL2"],
    "CSR19": ["CSR13", "CSR16"],
    "CSR20": ["CSR8", "CSR19"],
    "CSR21": ["CSR14", "CSR16", "CSR18", "CSR19", "CSR20"],
    "CSR22": ["CSR21", "SPR25"],
}
scopes = [
    "One actual level-row complex reader for every specified original model/basis datum; the family version chooses it before all tuples whose image is the same base tuple.",
    "All original words, old coordinate indices, valid stages and embeddings; all natural-subtraction and determinant-shift guards retained.",
    "All original words and every infinite place; one map fixed by the original ramified basis, with equality of the actual integral lattices and complete Hermitian forms.",
    "Every norm-one fractional ideal and every original kernel/period entry; the exact canonical coupling and zero branches are preserved.",
    "For any entire period and scale families, one actual ReadC, with all words and used tuples; its wU/eNu do not depend on the later period update.",
    "Every original standard kernel and specified ExtendedDataRemainder; the whole compatible column record is built without altering the original RowSideFamily.",
    "All ten original pin fields, including exact selected normal-form images and both actual complex evaluation clauses.",
    "Equality of the entire dependent group/family/levels/face/period package; all transports apply to full functions before evaluation at the actual Zs.",
    "There exist Dc,Sp0,Zsc0,C0 before forall T,a,x; every later original TwArgs sharing C0.wU and C0.eNu receives compatible columns with all five literal conclusions.",
    "Given the original EvalTieT and models_HE, one semilinear map and kappa=(c*nP)^(-1/2); the exact norm law is asserted only on the original guarded level subspace.",
    "All tuples, both levels and every place, conditional on the stated nonzero-part support; the full Gram matrix and majorant pairing are equal.",
    "For arbitrary face/period/scale families, conditional on original Pins/Holds and support, one scalar/error update preserves every original reading map and both metrics.",
    "For the actual updated data and the exact first DivDef3 output, construct all TwIn and TwArgs fields; no full DivRows3 or ratG/MLat producer is asserted.",
    "For every supplied original q,R,RecPinE,sP,sS,Del,h0,c, one C0 is retained and the period family is updated only at the actual Zs.",
    "Uniqueness of the original standard character and exact transports of StageAt, NExp and rational iota under the given scalar/error update.",
    "All original RealIn and RealTB fields, conditional on the original host/frame packet and the already constructed selected realization.",
    "Every original word and every nonbase used tuple in its source domain; all branching determinant shifts and nonzero scalar guards are explicit.",
    "All six RowSideDetermined fields for the same original divisionPair(x), including both all-class/all-tuple stabilizer divisibilities.",
    "One carrier per finite eigensystem before all type/embedding comparisons; all eight RecIn fields and complete PartsRow, conditional on exactly named original producer outputs.",
    "Every selected prime and every used tuple; both distinguished primes independently, conditional on HD.d3b equaling the original q pin.",
    "For each original q,R,RecPinE,c,DH and the same supplied packets, one Bundle with b.R=R and one complete BWit on that Bundle.",
    "Exact original EvP/ParEv nesting: eps then common K0, C then c1, cD then c2, ch and positivity then x0, then all K,q,R,c,DH; one ReadC precedes later TwArgs.",
]
hyps = [
    ["Original TC, Ok, Pins, Laws, Later, canonical-index IsTw and JetsIn; supplied semilinear model with independent spanning basis images."],
    ["Original finite group/central-idempotent tie and the stated original weight/jet laws."],
    ["Original Later.V injective nuIn with exact ramified image, lattice and norm laws; no existence of that Later stage is proved here."],
    ["Original kernel with KPin, actual RelDetPinned, retained jet rationality and the original period/later-stage laws."],
    ["The supplied original RXs(t), with its exact all-tuple same-map/coordinate clauses."],
    ["Original standard kernel and literal ExtendedDataRemainder including its original division, ambient and lift ties."],
    ["Same original TC/column packet and its actual sharp FormsTie, not a replacement row reader."],
    ["The stated full dependent-package equality or original TwArgs.pack, including unchanged exact tuple and word maps."],
    ["Original q,k,KPin and Nonempty(RXs(t)); later outputs require the exact displayed TwArgs/wU/eNu equalities."],
    ["Actual original MMap, EvalTieT including its chosen map and c>0, and models_HE; no boundedness or continuity of the algebraic extension outside the guard."],
    ["Original Pins/Holds, Ok3/type separation and nonzero E_p implies all required W_i,p/PartAt support."],
    ["Original Pins/Holds/readings and support; all old mLat/rational tests are only transported."],
    ["Original ambient/lift/group ties and geometric half, support, and the exact updated first DivDef3 contract at the given sEE/ReadC."],
    ["Original q,R,RecPinE and whole transported q.sat; original support and exact updated DivDef3 remain."],
    ["Original standard-character laws, StageAt and NExp; their original models/level/readings."],
    ["Original host/frame packet including positive V_i and specified standard V_i/X' frames and lattices."],
    ["Original TC/ColsTiedSym standard and nonbase twisted comparisons, interlace and pi*bar(pi)=T."],
    ["Original sharp ambient tie, whole TwArgs and same retained group/lattice data."],
    ["Original spherical eigensystem, carrier, isotropic inclusion, row/lift part producers and all-embedding logLam identity CSR.40; no producer is inferred just from its name."],
    ["Original HD:HostDatumC(R.T.toTiedDataS) with HD.d3b=q.x.pin.d3b; original selected-place/above pins."],
    ["The same five producer packets, same x,a,y,r,HD and DH equalities; no independent selection by output field."],
    ["Original p=prmR(N,SExt.none,Gamma), full universal N-to-NEb extension guard wherever used, and the exact five producer packets in the displayed eventual order. SPR25 is used only in its conditional same-R scope."],
]
claims = []
for i, title in enumerate(titles, 1):
    key = f"CSR{i}"
    st = [j for j, s in enumerate(lines) if s.strip() == f"% BEGIN {key}"]
    en = [j + 1 for j, s in enumerate(lines) if s.strip() == f"% END {key}"]
    assert len(st) == len(en) == 1 and st[0] < en[0] and anchors[key], key
    block = "".join(lines[st[0]:en[0]]).encode()
    assert all(d in old or d in peer or d in deps for d in deps[key]), key
    claims.append({
        "id": key, "title": title, "introduced_in": "0.37", "classification": "B",
        "status": "Complete independent human proof in the explicitly stated conditional scope",
        "proof_status": "complete in stated scope", "review_status": "pending independent mathematical review",
        "depends_on": deps[key], "scope": scopes[i - 1], "quantifier_scope": scopes[i - 1],
        "hypotheses_retained": hyps[i - 1], "classical_inputs": [],
        "proof_location": {
            "file": COMPONENT + "/main.tex", "paragraph": key, "label": "claim:" + key,
            "line_start": st[0] + 1, "line_end": en[0], "bytes": len(block),
            "sha256": sha(block), "range_sha256": sha(block), "file_sha256": sha(raw),
        },
        "sources": anchors[key],
    })

visited, visiting = set(), set()
def visit(key):
    if key in visited or key not in deps:
        return
    assert key not in visiting, ("cycle", key)
    visiting.add(key)
    for d in deps[key]:
        visit(d)
    visiting.remove(key)
    visited.add(key)
for key in deps:
    visit(key)

inputs, inherited_blocks = [], []
old_ids = sorted({d for ds in deps.values() for d in ds if d in old})
input_names = set()
for key in old_ids:
    pl = old[key]["proof_location"]
    file = pl["file"]
    input_names.add(file)
    companion = str(Path(file).with_name("provenance.json"))
    if (BASE / companion).exists():
        input_names.add(companion)
    ls = (BASE / file).read_text().splitlines(keepends=True)
    if "line_start" in pl and "line_end" in pl:
        st, en = pl["line_start"] - 1, pl["line_end"]
    else:
        hits = [j for j, s in enumerate(ls) if "\\paragraph" in s and re.search(r"\b" + key + r"(?!\d)", s)]
        assert len(hits) == 1, (key, hits)
        st = hits[0]
        en = next((j for j in range(st + 1, len(ls)) if ls[j].startswith("\\paragraph")), len(ls))
    inherited_blocks.append({
        "id": key, "file": file, "release": "0.36", "line_start": st + 1, "line_end": en,
        "sha256": sha("".join(ls[st:en]).encode()), "range_sha256": sha("".join(ls[st:en]).encode()),
        "file_sha256": sha((BASE / file).read_bytes()),
    })
input_names.add("continuation_notes_v0_36/next_global_assembly.txt")
for file in sorted(input_names):
    b = (BASE / file).read_bytes()
    inputs.append({"file": file, "release": "0.36", "sha256": sha(b), "file_sha256": sha(b), "bytes": len(b)})
for file in ("smooth_representatives/main.tex", "smooth_representatives/provenance.json", "smooth_representatives/closure.json"):
    b = (PEER / file).read_bytes()
    inputs.append({"file": file, "release": "0.37 peer", "sha256": sha(b), "file_sha256": sha(b), "bytes": len(b)})
pl = peer["SPR25"]["proof_location"]
pb = (PEER / pl["file"]).read_bytes()
pls = pb.decode().splitlines(keepends=True)
rb = "".join(pls[pl["line_start"] - 1:pl["line_end"]]).encode()
assert sha(rb) == pl["sha256"], "SPR25 proof-range mismatch"
inherited_blocks.append({
    "id": "SPR25", "file": pl["file"], "release": "0.37 peer",
    "line_start": pl["line_start"], "line_end": pl["line_end"],
    "sha256": sha(rb), "range_sha256": sha(rb), "file_sha256": sha(pb),
    "scope": "Only conditional original same-R multiplicity-map production; initial target FinPair and extremal boundedness remain.",
})

standing = "The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. These are human-reconstruction statuses only."
remaining = [
    {"id": "CSR_ORIGINAL_COMMON_POINT", "classification": "C", "role": "retained shared producer",
     "contract": "Produce one original q/WPt with RXs, Pins/Holds, ambient and lift readings, geometric half and same compatible final R/RecPinE; the constructor only uses these original objects."},
    {"id": "CSR_HOST_FRAMES", "classification": "B", "role": "retained original uniform installation",
     "contract": "The exact hostHyp_frames_ev packet, on all original Stages over K, including positive V_i and the specified V_i/X' frame and lattice equalities. Its elementary standard-coordinate clauses are not a substitute for the original host input."},
    {"id": "CSR_MULTIPLICITY_SUPPORT", "classification": "C", "role": "retained original producer",
     "contract": "Original MultEq on q.x.what2.r.z.R.toRealDat must supply E_p nonzero implies all W_i,p nonzero and all off-place PartAt on this same datum."},
    {"id": "CSR_ACTUAL_DIVDEF", "classification": "B", "role": "retained exact installation with upstream C inputs",
     "contract": "First DivDef3 output of divisionCompatible_at_readIdentifications on the actual updated R',F',Y',Z', C' and specified sEE; includes original sharp/base row definitions and theta coefficient data. Full DivRows3 is a separate stronger output.",
     "upstream_boundary": "The original analytic/geometric/rational reading producers are retained; this classification does not classify their existence as B."},
    {"id": "CSR_EIGEN_PARTS", "classification": "C", "role": "retained original representation-theoretic producer",
     "contract": "Original spherical eigensystems, common carriers, nonzero isotropic inclusions and row/lift part containments, with the required original nonzero character-level idempotents."},
    {"id": "CSR_ALL_EMBEDDING_PARAMETERS", "classification": "C", "role": "retained original reciprocity producer",
     "contract": "Exact all-embedding logLam identity CSR.40 under its nonzero/comap guards, on the same R',F',Y'; the nested current source-matching/reciprocity D obligations remain unaltered."},
    {"id": "CSR_HOST_DATUM", "classification": "C", "role": "retained exact host/class-field producer",
     "contract": "Original HD:HostDatumC(R.T.toTiedDataS) with HD.d3b=q.x.pin.d3b; class-field and ray-field inputs must match their original scope."},
    {"id": "CSR_INITIAL_ANALYTIC_INPUTS", "classification": "C", "role": "retained upstream inputs to closed SPR25",
     "contract": "The original initial target FinPair and bounded extremal theta seed, with all same-R guards in SPR25. The downstream MMap consumer is closed conditionally and is not an additional independent open theorem."},
]
closed = [
    {"id": "CSR_COLS_OF_WITNESSES", "claims": ["CSR1","CSR2","CSR3","CSR4","CSR5","CSR6","CSR7","CSR8","CSR9"],
     "contract": "Literal SelC.cols_of_witnesses: choose Dc,Sp0,Zsc0 and one ReadC before all later T/TwArgs/x, then construct the actual compatible columns, same face/period/W/Xg and all ten ColPins.",
     "requires": ["original q,k,KPin", "Nonempty(RXs)", "supplied TC laws/later stages/jets", "exact later TwArgs and wU/eNu equalities"]},
    {"id": "CSR_ACTUAL_PLACEMENT", "claims": ["CSR10"],
     "contract": "Original sEE placement with exact same chosen EvalTieT map and kappa=(c*nP)^(-1/2), preserving the original guarded subspace and nP norm.",
     "requires": ["original EvalTieT and models_HE", "c>0", "same finite P and actual MMap"]},
    {"id": "CSR_REFACE_READINGS", "claims": ["CSR11","CSR12"],
     "contract": "Original zeroLam/withErr/reFace preserves Pins,Holds,ErrEq, both row metrics and all thirteen original reading maps.",
     "requires": ["original Pins/Holds/readings", "literal nonzero-part support CSR.22"]},
    {"id": "CSR_SELECTED_REALIZATION", "claims": ["CSR13","CSR14"],
     "contract": "Actual TwIn/TwArgs and selected compatible columns/periods/scales, keeping the single original ReadC maps and transported whole q.sat.",
     "requires": ["CSR_COLS_OF_WITNESSES", "CSR_ACTUAL_PLACEMENT", "CSR_REFACE_READINGS", "actual updated DivDef3", "original geometric/ambient/lift data"]},
    {"id": "CSR_REAL_AND_ROW_PINS", "claims": ["CSR15","CSR16","CSR17","CSR18"],
     "contract": "All RealIn/RealTB and RowSideDetermined fields, including exact lower-map determinant cancellation, original sharp ambient and all stabilizer divisibilities.",
     "requires": ["CSR_SELECTED_REALIZATION", "original host/frame packet", "original standard/twisted column comparison and sharp ambient tie"]},
    {"id": "CSR_RECIN_FINITE_ASSEMBLY", "claims": ["CSR19"],
     "contract": "Finite EigIdx/PartsRec selection and all eight RecIn fields, preserving one carrier per eigensystem and all embedding equalities.",
     "requires": ["same original eigensystem/carrier/isotropic/part producers", "exact all-embedding logLam", "same original y/readings/character tuple"]},
    {"id": "CSR_SELECTED_SIDE", "claims": ["CSR20"],
     "contract": "All four original SelSideRT fields with exact QE image and both distinguished prime contractions.",
     "requires": ["same original TwArgs/RecPin", "HD on same R with original d3b"]},
    {"id": "CSR_BUNDLE_BWIT", "claims": ["CSR21"],
     "contract": "One literal seven-field Bundle b with b.R=the prescribed R, all five BTw fields and every BWit field through equality of the whole RPk.",
     "requires": ["CSR_SELECTED_REALIZATION", "CSR_REAL_AND_ROW_PINS", "CSR_RECIN_FINITE_ASSEMBLY", "CSR_SELECTED_SIDE", "same DH and same q.sat"]},
    {"id": "CSR_BUNU_EVENTUAL", "claims": ["CSR22"],
     "contract": "Original SelAll.bwit_exists/BunU implication in the exact EvP order, conditional on the displayed same-object producer outputs; no top-level common-producer closure is claimed.",
     "requires": ["CSR_BUNDLE_BWIT", "five original packets in exact EvP/pointwise scope", "full original universal NEb guard where upstream used"]},
]
for item in closed:
    item.update({"classification": "B", "status": "closed conditional implication",
                 "dependency_mode": "sufficient conjunction in the expressly stated original-object scope"})
not_closed = [
    "Existence of the common original point/family and compatible same-selector data.",
    "Initial target FinPair and bounded extremal theta seed; SPR25 closes their downstream consumer conditionally.",
    "Original multiplicity support, updated DivDef3 installation, eigensystem/carrier/part and all-embedding reciprocity producers.",
    "Original uniform host/frame and exact HD/d3b production.",
    "The separate ratG/MLat, full DivRows3G, MemberE, ExBL, RowL and RawSel existence branches.",
    "Any new unconditional RH/Dirichlet-GRH theorem or any claimed gap in the assumed-correct formal source.",
]
prov = {
    "schema": "rh-human-component-provenance/1", "artifact_version": "0.37", "date": "2026-11-22",
    "component": COMPONENT, "source_commit": PIN, "repository": "CocoSgt/riemann-hypothesis-lean",
    "standing_assumption": standing, "main_sha256": sha(raw), "main_tex_sha256": sha(raw), "sha256": sha(raw),
    "range_convention": "Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.",
    "metadata_builder": {"file": "build_provenance.py", "sha256": sha(Path(__file__).read_bytes()),
        "portable_invocation": "python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v036 --peer-root /path/to/work_v037",
        "source_anchor_file": "source_anchors.txt", "source_anchor_sha256": sha((HERE / "source_anchors.txt").read_bytes())},
    "claims": claims, "claim_total": len(claims), "external_literature": [], "published_applications": [],
    "inherited_proof_inputs": inputs, "inherited_proof_blocks": inherited_blocks,
    "not_closed": not_closed,
    "source_files": [{"path": p, "sha256": sha(b), "file_sha256": sha(b), "bytes": len(b),
        "line_count": len(ls), "verified_equal_to_pinned_git_blob": True}
        for p, (b, ls, _) in sorted(cache.items())],
}
dump("provenance.json", prov)
dump("published_applications.json", [])
closure = {
    "schema": "rh-human-component-closure/1", "version": "0.37", "component": COMPONENT,
    "source_commit": PIN, "standing_assumption": standing,
    "main_sha256": sha(raw), "main_tex_sha256": sha(raw), "sha256": sha(raw),
    "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
    "new_claim_ids": [c["id"] for c in claims], "closed_contracts": closed,
    "remaining_inputs": remaining, "selected_top_level_leaf_closed": False,
    "same_object_guards": [
        "One original q, same prescribed R and complete RecPinE, including cols/theta/character/kernel.",
        "Whole q.sat.P/S transported once, preserving original t,c,Hilbert space, good operator and chosen evaluation map.",
        "One ReadC before every later T/TwArgs; its exact wU/eNu survive every update.",
        "Only inactive scalars are changed; both entire Gram matrices and thirteen reading maps are equal.",
        "The exact first DivDef3 is on the actual updated R/F/readings/sEE; no arbitrary compatible substitute.",
        "One finite carrier per eigensystem, all-embedding logLam under its original nonzero guards.",
        "Same HD.d3b, both distinguished prime contractions, and full RPk equality before final Bundle/BTw/BWit.",
        "Exact EvP threshold nesting and complete universal NEb input where needed; no separately selected projections.",
    ],
    "not_closed": not_closed, "review_status": "pending independent mathematical review",
}
dump("closure.json", closure)
loc = [f"CSR source locators — {PIN}", "Inclusive one-based source/proof lines and exact byte hashes.",
       f"main.tex SHA256 {sha(raw)}", ""]
for c in claims:
    p = c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE / "source_locators.txt").write_text("\n".join(loc) + "\n")
ranges = {(s["path"], s["line_start"], s["line_end"], s["range_sha256"]) for c in claims for s in c["sources"]}
validation = {
    "status": "PASS", "source_commit": PIN, "main_sha256": sha(raw), "claims": len(claims),
    "claim_source_references": sum(len(c["sources"]) for c in claims),
    "distinct_source_ranges": len(ranges), "source_files": len(cache), "inherited_files": len(inputs),
    "inherited_claim_blocks": len(inherited_blocks),
    "checks": ["Pinned HEAD and every referenced Git blob", "Unique source anchors and marked human proof ranges",
               "All depends_on entries indexed in old/new/peer claim ledgers", "New-claim dependency DAG acyclic",
               "Exact source/proof/input hashes and fresh CSR prefix", "No unexpected control characters"],
    "not_performed": "No Lean compilation or kernel replay; mathematical peer review and standalone draft TeX are separately recorded.",
}
dump("validation.json", validation)
report = """v0.37 — original common selected constructor, CSR1–CSR22

The full finite/record chain is reconstructed. CSR9 proves literal
SelC.cols_of_witnesses: one ReadC is chosen before all later TwArgs, with
actual compatible columns, original periods, exact weights/Xg and all ten
ColPins. CSR10 proves the original evaluation placement with its forced
kappa=(c*nP)^(-1/2). CSR11–12 reconstruct zeroLam/reFace, equal entire row
metrics and all thirteen unchanged reading maps. CSR13–16 construct the
actual TwIn/TwArgs and selected RealIn/RealTB records, conditional on the
explicit original division and host inputs.

CSR17 proves the terminal branching scalar cancellation monomial by
monomial, including the signed determinant shift. CSR18 checks all six
RowSideDetermined fields. CSR19 constructs the finite EigIdx, one carrier
per eigensystem and every RecIn/PartsRow field, conditional on the explicit
original spectral/part producers and all-embedding logLam. CSR20 proves
all selected-prime conditions, including both distinguished contractions.
CSR21 builds the exact Bundle, BTw and BWit on the prescribed original R
using equality of the whole five-field RPk. CSR22 supplies the full EvP
join and same-R BunU conclusion, with the original threshold/choice order.

Five retained realization packets: original host/frame; multiplicity
nonzero-part support; exact updated first DivDef3; original eigensystem/
carrier/part producers together with all-embedding logLam; original HD
with the exact d3b pin. Their common original point/readings/geometric data
and universal NEb guards remain. The downstream MMap consumer is now
conditionally supplied by SPR25 on that same R, while its initial target
FinPair and bounded extremal seed remain. The separate ratG/MLat, full
DivRows3G and common-family/selector producers are not silently closed.

All proofs are independent human arguments in their displayed scopes;
the pinned formal source is assumed fully correct. No new published
theorem application or additional top-level whole-leaf closure is claimed.
The portable builder verifies exact pinned source bytes and binds all
22 proof blocks, inherited inputs and the conditional same-round SPR25.
"""
report += f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE / 'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE / 'closure.json').read_bytes())}\n"
report += f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} source files; {len(inputs)} inherited/peer files.\n"
(HERE / "report.txt").write_text(report)
print(json.dumps({**validation, "provenance_sha256": sha((HERE / "provenance.json").read_bytes()),
                  "closure_sha256": sha((HERE / "closure.json").read_bytes())}, indent=2))
