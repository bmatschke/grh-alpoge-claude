#!/usr/bin/env python3
"""Rebuild SCI provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v039

Only files beside this script are written. This is source backtracking and
human-proof bookkeeping, not a Lean kernel replay.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENT = "selected_core"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v039")
parser.add_argument("--companions", type=Path, default=HERE.parent)
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
COMPANIONS = args.companions.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"SCI\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written SCI block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }

a = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
p = a + "PatchingModules/"
h = p + "AnnihilatorBaseChange/"
bc = p + "PatchingBaseChange/"
ca = a + "CommutativeAlgebraHeight/"
w = a + "WeilGroupCharacters/"
anchors = {f"SCI{i}": [] for i in range(1, 14)}
anchor_rows = []
def add(ids, path, names):
    for name in names.split(";"):
        entry = source(path, name)
        for key in ids.split():
            assert key in anchors, key
            if entry not in anchors[key]:
                anchors[key].append(entry)
    anchor_rows.append(ids + "|" + path + "|" + names)

add("SCI1 SCI11 SCI12 SCI13", p+"PatchedSupportCompletions.lean",
    "Pt;Adapted;ChainConcl;Core;CoreBC;Raw")
add("SCI2 SCI3", ca+"GKillsTr.lean", "UpperTheory.V.CA.g_kills_tr")
add("SCI3", ca+"GmaKills.lean", "UpperTheory.V.CA.gma_kills")
add("SCI3", ca+"DComm.lean", "UpperTheory.V.CA.d_comm")
add("SCI2 SCI3 SCI4", h+"OoFiniteHom.lean",
    "oo_kills;oo_adic_map;oo_def_map;UpperTheory.V.Pa.Core.ooDet")
add("SCI4 SCI5 SCI6 SCI10 SCI11", h+"SpecializationMapCompUniversalSection.lean",
    "Rel;ii;OoPair;ooKer")
add("SCI4 SCI11", h+"CharpolyElementEqAevalGroupElement.lean", "UpperTheory.V.Pa.Core.piKer")
add("SCI5 SCI10", h+"ResPull.lean", "UpperTheory.V.Pa.Core.resPull")
add("SCI5", h+"OoPair.lean", "UpperTheory.V.Pa.Core.ooPair")
add("SCI5 SCI10", h+"OoMaps.lean", "UpperTheory.V.Pa.Core.ooMaps")
add("SCI6", h+"RrGen.lean", "UpperTheory.V.Pa.Core.rrGen")
add("SCI6", h+"RrExt.lean", "UpperTheory.V.Pa.Core.rrExt")
add("SCI7", bc+"ChainLift.lean",
    "UpperTheory.V.Pa.BC.chain_lift_down;UpperTheory.V.Pa.BC.prime_chain_lift_extension;UpperTheory.V.Pa.BC.chain_lift")
add("SCI7 SCI8", a+"AlgebraTools/CaOverLift.lean",
    "exists_field_lift;UpperTheory.V.AlgebraTools.exists_lift_ker_eq")
add("SCI7 SCI8 SCI9 SCI12", p+"AutomorphicDetection/LiftPt.lean", "lift_pt;core")
add("SCI9 SCI10", h+"InjOfProd.lean", "inj_of_prod;UpperTheory.V.Pa.Core.ooPt")
add("SCI10 SCI11", p+"PatchedSupportCompletions.lean", "OoPt;OoPt.ker")
add("SCI11", p+"PatchedSupportCompletions.lean",
    "IsCoef;CohLim;PatchedSupportCompletions;S5;GalOut")
add("SCI11", p+"AutomorphicDetection/AnnBc.lean", "ann_bc;s5_lemma;s5")
add("SCI11", p+"AutomorphicDetection/CohLim.lean", "cohLim")
add("SCI11 SCI12", p+"AutomorphicDetection/GalOut.lean", "ctx_out;galOut")
add("SCI12", h+"ChainAbs.lean", "UpperTheory.V.Pa.Core.chainAbs")
add("SCI12", h+"PiSurj.lean", "UpperTheory.V.Pa.Core.piSurj")
add("SCI12", h+"PatchedModuleAnnihilatorLeComapIffIdealLe.lean",
    "UpperTheory.V.Pa.Core.patchedModule_annihilator_le_comap_iff_ideal_le")
(HERE/"source_anchors.txt").write_text("\n".join(anchor_rows)+"\n")

titles = [
    "The exact selected one-point full-block contract",
    "Checked multiplicity-free Cayley-Hamilton structure theorem",
    "Trace-kernel equals the full determinant kernel in the actual setting",
    "Full determinant descent to the actual limiting global group",
    "Complete original OoPair and its exact specialization",
    "Adic generation by the actual determinant and point data",
    "One splitting prime with both endpoint primes below it",
    "Original point lift with exactly the prescribed kernel",
    "Actual ordered roots avoid the original patching denominator",
    "Every field of the actual lifted ordinary point",
    "Actual S5 completion matched to the actual ordinary point",
    "Complete selected normalized Core theorem",
    "Complete selected Raw endpoint by normalization and descent",
]
deps = {
    1:["CRW1"],
    2:["PQL7","PRG2","PRG3","PRG7"],
    3:["SCI2","PQL7"],
    4:["LIM18","PRG13","PRG24","PMS30","SCI3","PRG3"],
    5:["SCI4","PRG23"],
    6:["JSP9","SCI4","SCI5","PRG14"],
    7:["PRG18"],
    8:["PRG18","SCI7"],
    9:["SCI8","PRG23"],
    10:["SCI5","SCI6","SCI9","LIM18"],
    11:["SCI4","SCI8","SCI9","SCI10","PMS15","PMS16","PMS29","LIM19","CRW15"],
    12:["SCI1","SCI7","SCI11","PMS31","PMS32","CRW18","CRW19","CRW20"],
    13:["SCI12","BCN24","BCN25","PQL20","PQL21"],
}
scopes = [
    "Original Core antecedents at h=0, a=n=4, k.g=0, D0=D+4q; exact original ChainConcl and same J.",
    "Every positive-degree full determinant over an IsCO base with split distinct residual characters; ordinary full Cayley-Hamilton quotient; no finite-module or factorial hypothesis.",
    "Full determinant kernel equals the trace radical under exactly SCI2, with all scalar extensions; characteristic 3 retained.",
    "Actual W.R/ii(W), original pi and global limit group; every full determinant and continuity field of ooDet.",
    "Actual residual pullback, all Pair polarization/ordinary/inertia clauses and full ooMaps; unchanged coefficient maps.",
    "Exact rrGen and quotient OoPt.gen; full-law uniqueness proved from integral word identity, not traces alone.",
    "Actual finite free Spo/B; one prime above the original point and simultaneous exact lifts of both endpoint primes below it.",
    "Every prime P of actual Spo above ker(x.f), exact lift to the same original K[[t]] with kernel P; no field replacement.",
    "Original fEl(1,U), exact ordered roots and original eigenvalue list; no new Selmer or point witnesses.",
    "Full original OoPt on the actual quotient pair and selected prime, including literal equality of its closed relation set with ooKer.",
    "Actual R, pi, PMod, augmentation fiber and S5 completion; normalized dimension 1+D and minimal support dimension 1+D+nq.",
    "Selected full-block normalized h=0 Core on original data, with every ring/module/point supplier constructed; same J containment.",
    "Selected h=0,a=n=4,k.g=0 Raw on original antecedents via actual coefficient normalization and original pro-ell descent; TWAut is still an original upstream input.",
]
guards = [
    "Original pinned Lean proof assumed fully checked and correct; statuses concern only the human reconstruction.",
    "Both original rank-four Links, prime 3, fixed complex embedding and common coefficient threshold are unchanged.",
    "Same original B,J,K,f,Kap and B1/B2 constants-before-truncation/eventual-level quantifiers at the final conclusion.",
    "Actual Lim, RRObj, RMaps, finite modules and S5 completion are supplied, never independently assumed at the selected endpoint.",
    "One splitting prime is used for both endpoint lifts and for the same ordinary point and completion.",
    "Original stable and stable-or-thick hypotheses remain in the selected statement; full-block dimension makes them unused in its proof.",
    "No general arbitrary-chain Core, unrestricted Kap, arithmetic TWAut producer or full Count-II closure is claimed.",
]
companion_data = {}
available = dict(old)
for name in ["patched_ring","patched_support","coefficient_normalization"]:
    path = COMPANIONS/name/"provenance.json"
    obj = json.loads(path.read_text())
    main = (COMPANIONS/name/"main.tex").read_bytes()
    assert obj["source_commit"] == PIN
    assert obj.get("main_sha256",obj.get("main_tex_sha256")) == sha(main)
    for c in obj["claims"]:
        assert c["id"] not in available, c["id"]
        available[c["id"]] = c
    companion_data[name] = dict(
        provenance_file=name+"/provenance.json", provenance_sha256=sha(path.read_bytes()),
        main_file=name+"/main.tex",main_sha256=sha(main),claim_ids=[c["id"] for c in obj["claims"]])
claims = []
for i,title in enumerate(titles,1):
    key=f"SCI{i}"
    starts=[j for j,line in enumerate(lines) if line.strip()==f"% BEGIN {key}"]
    ends=[j+1 for j,line in enumerate(lines) if line.strip()==f"% END {key}"]
    assert len(starts)==len(ends)==1 and starts[0]<ends[0] and anchors[key],key
    st,en=starts[0],ends[0]; block="".join(lines[st:en]).encode()
    assert all(x in available or x in {f"SCI{j}" for j in range(1,i)} for x in deps[i]), (key,deps[i])
    claims.append(dict(
        id=key,title=title,introduced_in="0.40",classification="A" if i in (2,7) else "B",
        status="Complete human proof in the exact stated scope",proof_status="complete in stated scope",
        review_status="pending independent mathematical review",depends_on=deps[i],
        scope=scopes[i-1],quantifier_scope=scopes[i-1],hypotheses_retained=guards,
        proof_location=dict(file=COMPONENT+"/main.tex",paragraph=key,label="claim:"+key,
            line_start=st+1,line_end=en,bytes=len(block),sha256=sha(block),range_sha256=sha(block),file_sha256=sha(raw)),
        sources=anchors[key]))
external_ids=sorted({d for c in claims for d in c["depends_on"] if not d.startswith("SCI")})
inherited=[]
for key in external_ids:
    c=available[key];loc=c["proof_location"]
    if key in old:
        base=BASE
    else:
        base=COMPANIONS
    block_file=base/loc["file"]
    ls=block_file.read_bytes().splitlines(keepends=True)
    block=b"".join(ls[loc["line_start"]-1:loc["line_end"]])
    expected=loc.get("range_sha256",loc.get("sha256"))
    assert sha(block)==expected,(key,block_file,sha(block),expected)
    inherited.append(dict(id=key,proof_file=loc["file"],
        line_start=loc["line_start"],line_end=loc["line_end"],
        proof_sha256=sha(block),source_version="0.39 or earlier" if key in old else "0.40 companion"))
url="https://maths.dur.ac.uk/events/Meetings/LMS/2011/GRAF11/papers/chenevier.pdf"
apps=[
    dict(id="SCI_CHEN_GMA",citation="Gaetan Chenevier, The p-adic analytic space of pseudocharacters of a profinite group and pseudorepresentations over arbitrary rings",
        theorem="Theorem 2.22(ii), pp. 34-35 in the cited version",url=url,source_url=url,
        classification="A",status="hypotheses checked",
        statement_used="A Cayley-Hamilton determinant over a henselian local base with split multiplicity-free residual law gives a generalized matrix algebra with the determinant trace; in rank-one residual blocks its diagonal corners are the base ring.",
        hypotheses_checked=[
            "C is the actual IsCO complete Noetherian local quotient; henselianity is established by the coprime-factor lifting argument.",
            "E is the ordinary full Cayley-Hamilton quotient C[H]/CH(D); PQL7 proves CH(D) lies in the full determinant kernel.",
            "The residual characters are the actual distinct pulled-back characters, hence split multiplicity free with every block of rank one.",
            "Degree is positive, in particular n=4, and ell=3 is allowed.",
            "The theorem's multiplicity-free alternative is used with no finite generation of E, absolute irreducibility, ell>n or n! inversion."
        ],claims=["SCI2","SCI3","SCI4"],checked_in="selected_core/main.tex SCI2-SCI4"),
    dict(id="SCI_STACKS_FLAT_PRIMES",citation="The Stacks Project",
        theorem="Lemmas 10.39.16, 10.39.17, 10.39.19; Tags 00HQ,00HR,00HS",
        url="https://stacks.math.columbia.edu/tag/00HS",source_url="https://stacks.math.columbia.edu/tag/00HS",
        classification="A",status="hypotheses checked",
        statement_used="Faithfully flat maps are surjective on spectra; a flat local map is faithfully flat; flat maps satisfy going down.",
        hypotheses_checked=[
            "PRG18 proves the exact Spo is finite free of positive rank over the original B.",
            "B to Spo is consequently flat and faithful, so a prime exists above the exact original kernel p.",
            "The localized B_p to Spo_P is flat and local; going down lifts both endpoint primes below the single selected P.",
            "All contractions are equalities; no primes over unrelated splitting factors are used."
        ],claims=["SCI7","SCI12"],checked_in="selected_core/main.tex SCI7 and SCI12")
]
dump("published_applications.json",apps)
standing=guards[0]
closed=[
    dict(id="SCI_QUOTIENT_PAIR_POINT",classification="B",status="closed in exact stated scope",
        claims=[f"SCI{i}" for i in range(2,11)],
        contract="Actual quotient determinant, complete OoPair/ooMaps, exact lifted point and full OoPt on the actual universal ring/maps."),
    dict(id="SCI_SELECTED_CORE",classification="B",status="closed in exact original selected scope",
        claims=["SCI11","SCI12"],
        contract="Original normalized one-point full-block Core at h=0,a=n=4,k.g=0, conditional only on its original antecedents, including given TWAut."),
    dict(id="SCI_SELECTED_RAW",classification="B",status="closed in exact original selected scope",
        claims=["SCI13"],
        contract="Original selected Raw after actual coefficient normalization/Unit and pro-ell descent; final original B,J,K,f and all Selmer quantifiers retained.")
]
remaining=[
    dict(id="SCI_ORIGINAL_ARITHMETIC_PACKET",classification="C",
        contract="Original ordinary/control/separating-fiber and type/neatU/TThetaEx producers, four Hida endpoints, all-level same-J TWAut/HasAut."),
    dict(id="SCI_BOTH_LINKS_COMMON_THRESHOLD",classification="C",
        contract="Those arithmetic producers on both original rank-four Links with prime 3, fixed iota and one common coefficient threshold."),
    dict(id="SCI_OTHER_FINAL_SHARED_INPUTS",classification="C",
        contract="Other unresolved selected local/global/common-family estimates and unrestricted-character branches in the complete dependency audit.")
]
prov=dict(schema="rh-human-component-provenance/1",artifact_version="0.40",date="2026-11-22",
    component=COMPONENT,source_commit=PIN,repository="CocoSgt/riemann-hypothesis-lean",
    standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
    range_convention="Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.",
    claims=claims,claim_total=len(claims),published_applications=apps,inherited_proof_blocks=inherited,
    companion_bindings=companion_data,
    source_files=[dict(path=x,sha256=sha(b),file_sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True) for x,(b,ls,_) in sorted(cache.items())],
    metadata_builder=dict(file="build_provenance.py",sha256=sha(Path(__file__).read_bytes()),
        portable_invocation="python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v039 --companions /path/to/reconstruction_v040"))
dump("provenance.json",prov)
closure=dict(schema="rh-human-component-closure/1",version="0.40",component=COMPONENT,source_commit=PIN,
    standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
    provenance_sha256=sha((HERE/"provenance.json").read_bytes()),new_claim_ids=[x["id"] for x in claims],
    closed_contracts=closed,remaining_inputs=remaining,same_object_guards=guards,
    selected_top_level_leaf_closed=False,
    not_closed=["Whole compound Count-II producer","Original arithmetic TWAut/HasAut producer",
        "General arbitrary-chain/arbitrary-Kap Core","Unconditional complete human RH or Dirichlet-GRH proof"],
    review_status="pending independent mathematical review")
dump("closure.json",closure)
unique={(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
val=dict(status="PASS",source_commit=PIN,main_sha256=sha(raw),claims=len(claims),
    claim_source_references=sum(len(c["sources"]) for c in claims),distinct_source_ranges=len(unique),
    source_files=len(cache),published_applications=len(apps),bound_dependency_blocks=len(inherited),
    checks=["Fresh prefix","Every source file equals pinned Git blob","Unique declaration anchors",
        "All marked SCI proof blocks hashed","All prior and companion dependencies exist and proof blocks match",
        "Complete Core/Raw scope distinguished from unresolved arithmetic antecedents"],
    not_performed="No Lean build or kernel replay; independent mathematics review and draft TeX recorded separately.")
dump("validation.json",val)
loc=[f"SCI source/proof locators at {PIN}",f"main.tex SHA256 {sha(raw)}",""]
for c in claims:
    q=c["proof_location"]
    loc.append(f'{c["id"]} | {c["title"]} | proof {q["line_start"]}-{q["line_end"]} SHA256 {q["sha256"]}')
    for x in c["sources"]:
        loc.append(f'  {x["path"]}:{x["line_start"]}-{x["line_end"]} | {x["declaration"]} | file {x["sha256"]} | range {x["range_sha256"]}')
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
(HERE/"report.txt").write_text("""v0.40 — selected actual Core and Raw closure, SCI1–SCI13

The actual quotient determinant is obtained from a checked multiplicity-free
Cayley–Hamilton structure theorem and an integral full-kernel proof. Every
OoPair, ooMaps, generation, point-lift and OoPt field is reconstructed on the
original universal ring and maps. One splitting prime is used for both
endpoints and for the exact point kernel and completion.

PMS supplies the actual module and S5 support; CRW's selected full-block
cotangent bound forces the minimal support prime to be zero. Thus the support
ideal itself is zero and the actual annihilator comparison yields the
original J-containment. This completes normalized Core at h=0,a=n=4,k.g=0.
BCN24/25 and original PQL then complete the selected Raw endpoint.

This is a selected original producer, not an unconditional RH/GRH proof.
The original ordinary/control/type, four Hida endpoints and all-level same-J
TWAut/HasAut antecedents remain. Both rank-four Links, prime 3, fixed iota and
the common coefficient threshold are retained. No Lean replay is performed.
""")
print(json.dumps(val,indent=2))

