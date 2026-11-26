#!/usr/bin/env python3
"""Build portable GFA provenance and conditional closure from a pinned checkout.

Usage: python build_provenance.py --source /path/to/lean_source
                                --baseline /path/to/reconstruction_v033
No Lean compilation or kernel replay is claimed. Source bytes are checked
against git objects at PIN; human proof blocks are hashed independently.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1]/"lean_source")
ap.add_argument("--baseline", type=Path, default=HERE.parents[1]/"reconstruction_v033")
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()

def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n")

assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE,
                              text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE/"provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"GFA\d+", k) for k in old), "GFA prefix is not fresh"
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
            "role": "Exact original contract, dictionary, or corresponding source proof; human closure comes from the separately hashed GFA proof block.",
            "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{s+1}-L{e}"}

anchors = {f"GFA{i}": [] for i in range(1,13)}
for line in (HERE/"source_anchors.txt").read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    ids,path,names=line.split("|")
    for name in names.split(";"):
        a=source(path,name)
        for k in ids.split():
            if a not in anchors[k]: anchors[k].append(a)

titles = [
 "Exact original type-prime quotient-length cost with constant 36",
 "Direct coarse bound for the original total local correction, Ta≤b²",
 "Exact quotient mean and maximal slopes with unchanged metrics",
 "Original support, nonnegative integer corrections and exceptional-prime zeros",
 "Literal PlacesF and SlopesNF from original local gains and metric transport",
 "Positive actual RR rank, algebraic dual slope and LatF",
 "The original Bessel matrix and arithmetic map satisfy the exact frame dictionary",
 "The literal frame inequality for every admissible height, including zero spread",
 "One pair of error bounds chosen before the family member gives FrameF",
 "Exact original thick/top/thin node intervals and NodesF",
 "Every one of the seventeen Win_at clauses and the prescribed WinF quantifiers",
 "Original primitive readings, centered ramps, quadratic identities and CharF",
]
deps = {
 "GFA1":["RSL9","RSL10","RSL11","GLE2","GLE11","LC3","GVC11","GVC18"],
 "GFA2":["GII1","GII2","GII3","SZ1","SZ2","SZ3","SZ4","SZ5","SZ6","SZ7","SZ8"],
 "GFA3":["LC1","LC2","LC3","LC4","MT1","MT2","RSL11"],
 "GFA4":["GFA2","RSL9","GLE11","LC3"],
 "GFA5":["GFA1","GFA2","GFA3","GFA4","LC5","LC6","MT3","MT6"],
 "GFA6":["RSL12","GF1","GF2"],
 "GFA7":["GFA6","GF1","GF2","GF5","GF6"],
 "GFA8":["GFA6","GFA7","GF3","GF8"],
 "GFA9":["GFA8","SZ8","RSL10"],
 "GFA10":["SZ4","SZ5","SZ7","SZ8"],
 "GFA11":["SZ1","SZ2","SZ3","SZ4","SZ5","SZ6","SZ7","SZ8"],
 "GFA12":["AH9","AH10","WB1"],
}
hyp = {
 "GFA1":["Same original FamP, original supplied ramified model and guarded GLE local statements; TuSize; original NumsL/WtsL and DlSize fields"],
 "GFA2":["Original FamP with 0<epsilon<1/52 and its unchanged fixed constants; actual Cand,VV,Dp,tv,tauP definitions and finite-place weights"],
 "GFA3":["Same full-rank commensurable original NuLat, reference lattice, ideal Iu and original metrics; exact NuDef length identity"],
 "GFA4":["Same original local installation and LinkG, TuSize, finite support, actual stored EDef, NuAtTDef and nonnegative Sig correction"],
 "GFA5":["Same family with LevelTFamily, NuCommens, MuRank, TuSize, LinkG and LinkMu; original support set and zero/nonzero cases retained"],
 "GFA6":["Original ChosenProviso with C0>0, positive d_u, LinkS with diagonal defect<1, LinkIRR with target defect<1, LinkDIV.RRFull and positive Nu ranks"],
 "GFA7":["Same LinkDIV Bessel identity, actual rational map/OneMapIntoCC integrality and height, same LinkS diagonal/cross estimates, original metrics and target RR dual"],
 "GFA8":["GFA7 original maps and metrics; original ChosenCode/Proviso; source and target discard kept distinct; every H>0 satisfying the literal height inequality"],
 "GFA9":["Original fixed CH>0, sufficiently small epsilon, same chosen data and LinkS, LinkIRR, LinkDIV, TuSize; all thresholds chosen before i,u and places"],
 "GFA10":["Original FamP size record, actual gcode and tau inverse, actual ThickSet and top/thin node definitions"],
 "GFA11":["Original FamP size record and ThickSetDensityEventually on the same family; arbitrary fixed c6>0"],
 "GFA12":["Every original Host including its stored flPS:PsQ; original selected primitive readings; ChThin and ChQD estimates remain supplied premises"],
}
adjacent = HERE.parent/"global_count"/"provenance.json"
assert adjacent.is_file(), "Build GVC metadata before GFA metadata"
gvc=json.loads(adjacent.read_text())
known=set(old)|set(deps)|{c["id"] for c in gvc["claims"]}
claims=[]
for i,title in enumerate(titles,1):
    k=f"GFA{i}"
    st=next(j for j,l in enumerate(lines) if l.strip()==f"% BEGIN {k}")
    en=next(j+1 for j,l in enumerate(lines) if l.strip()==f"% END {k}")
    b="".join(lines[st:en]).encode()
    assert set(deps[k])<=known,(k,set(deps[k])-known)
    assert anchors[k],k
    claims.append(dict(id=k,title=title,introduced_in="0.34",classification="B",
      status="Complete human proof of the stated conditional result; independent review recorded separately",
      proof_status="complete in the stated scope",review_status="see frozen-byte independent review",
      scope="Same original family, host, selectors, fields, words, places, lattices, maps, metrics, fixed constants and threshold order",
      depends_on=deps[k],hypotheses_retained=hyp[k],classical_inputs=[],
      proof_location=dict(file="global_assembly/main.tex",paragraph=k,label="claim:"+k,
        line_start=st+1,line_end=en,sha256=sha(b),range_sha256=sha(b),file_sha256=sha(raw),bytes=len(b)),
      sources=anchors[k]))

# Component names have accumulated historically; resolve the exact ledger path
# from an inherited claim instead of guessing an alias.
input_claims=["GF8","LC6","MT6","RSL10","GLE11","GLS13","GII3","SZ8","AH10","WB1"]
inputs=[]
for k in input_claims:
    historical={"GF8":"gram_frame/gram_frame_section.tex","LC6":"local_accounting/local_accounting.tex","GII3":"type_two_family/main.tex"}
    p=historical[k] if k in historical else old[k]["proof_location"]["file"]
    if not any(i["file"]==p for i in inputs):
        b=(BASE/p).read_bytes()
        inputs.append(dict(file=p,sha256=sha(b),bytes=len(b),scope="Unmodified inherited v0.33 human proof, used only in its stated scope"))
inputs.append(dict(file="global_count/provenance.json",sha256=sha(adjacent.read_bytes()),
 bytes=adjacent.stat().st_size,scope="Same-version GVC ledger supplies GFA1 numerical inputs; its proof blocks are indexed independently"))
standing="The pinned Alpoge-Claude Lean proof is fully checked and correct. Open/D classifications concern human reconstruction or source understanding only."
not_closed=[
 "Actual LossFS(Fm,0) from the same chosen small-share inputs",
 "Exact common-family linkCore/ChainTied installation and final Closed wrapper with Cabs=2,C0=3,C5=4,eD=2,eL=0",
 "Original common compatible second layer, Duty, LinkG/LinkS/LinkIRR/LinkDIV and upstream geometric/arithmetic producers",
 "Stronger weighted-prime FamilyWeightSumBound or every intermediate source PartFive proposition; neither is claimed merely from the coarser sufficient arguments here",
 "Complete human-readable RH or unrestricted Dirichlet-GRH proof",
]
prov=dict(schema="rh-human-component-provenance/1",artifact_version="0.34",date="2026-11-22",
 source_commit=PIN,repository="CocoSgt/riemann-hypothesis-lean",component="global_assembly",
 standing_assumption=standing,main_sha256=sha(raw),sha256=sha(raw),
 range_convention="Inclusive one-based physical lines; exact UTF-8 range hashes include line endings. Source sha256 aliases full-file hash; proof sha256 aliases proof-block hash.",
 claims=claims,external_literature=[],inherited_proof_inputs=inputs,not_closed=not_closed,claim_total=len(claims),
 source_files=[dict(path=p,sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True) for p,(b,ls,_) in sorted(cache.items())])
dump("provenance.json",prov)
dump("literature.json",dict(schema="rh-exact-literature-application/1",source_commit=PIN,main_sha256=sha(raw),entries=[],note="No new published application; finite identities and estimates are proved directly from inherited human inputs."))
dump("published_applications.json",[])
loc=[f"GFA source locators at {PIN}",f"main.tex SHA256 {sha(raw)}","Inclusive one-based ranges; pinned source bytes checked against git.",""]
for c in claims:
    p=c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]: loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
nodes=[
 dict(id="SAME_ORIGINAL_FAMILY",role="retained original supplied family",contract="FamP, original fixed constants, literal size record, same fields and selected records"),
 dict(id="SAME_CHOSEN_INPUTS",role="retained producer premises",classification="C",contract="Original Duty/ChosenWall, LinkG, LinkS, LinkIRR, LinkDIV and same compatible second layer"),
 dict(id="EXACT_LOCAL_PREMISES",role="retained conditional arguments",contract="All GFA1–5 hypotheses: original ramified identities and guarded congruence length, TuSize, NuCommens, MuRank, LinkG and LinkMu on the same supplied family; numerical and weight windows from original FamP sizes and GVC11/GVC18"),
 dict(id="EXACT_FRAME_PREMISES",role="retained conditional arguments",contract="All GFA6–9 hypotheses: original ChosenProviso with C0>0, ChosenCode, positive d_u and Nu ranks, LinkS, LinkIRR, LinkDIV with RRFull/OneMapIntoCC/BesselId, and TuSize; fixed CH>0"),
 dict(id="EXACT_WINDOW_PREMISES",role="retained conditional arguments",contract="All GFA10–12 hypotheses: original FamP sizes, ThickSetDensityEventually on that same family, arbitrary fixed c6>0, original Host.flPS, and ChThin/ChQD retained as estimates"),
 dict(id="ORIGINAL_QUOTIENT_SLOPES",role="closed conditional consumer",claims=[f"GFA{i}" for i in range(1,6)],contract="Exact LevelTFamily, PlacesF and SlopesNF on the same original data"),
 dict(id="ORIGINAL_FRAMEF",role="closed conditional consumer",claims=[f"GFA{i}" for i in range(6,10)],contract="Exact RRRankF, LatF and literal all-H FrameF, with one pre-index pair of error constants"),
 dict(id="ORIGINAL_WINDOWS_CHARACTERS",role="closed conditional consumer",claims=["GFA10","GFA11","GFA12"],contract="Exact NodesF, all seventeen Win_at clauses, and all four Char_at clauses"),
 dict(id="LOSS_FS_ZERO",role="open implication reconstruction",classification="B",contract="Actual LossFS(Fm,0) from original small shares and chosen weights, with original IOsum and ASK−Ga"),
 dict(id="SAME_FAMILY_TIED_LEDGER",role="open implication reconstruction",classification="B",contract="All original ChainTied fields and numerical constants on the very same family, followed by the final Closed wrapper"),
 dict(id="TASK_GL_FINAL_ASSEMBLY",role="open shared implication task",classification="B",contract="Residual LossFS(Fm,0) plus same-family linkCore/ChainTied/Closed installation; the completed consumer subarguments are not producers"),
]
gates=[]
for out,ks,premise in [("ORIGINAL_QUOTIENT_SLOPES",list(range(1,6)),"EXACT_LOCAL_PREMISES"),("ORIGINAL_FRAMEF",list(range(6,10)),"EXACT_FRAME_PREMISES"),("ORIGINAL_WINDOWS_CHARACTERS",list(range(10,13)),"EXACT_WINDOW_PREMISES")]:
    gates.append(dict(id="GATE_"+out,status="proved sufficient conditional implication",all_of=["SAME_ORIGINAL_FAMILY","SAME_CHOSEN_INPUTS",premise],implies=out,proof_claims=[f"GFA{i}" for i in ks],same_object="Every premise retains the same supplied original family and literal objects; the exact individual hypotheses are listed in provenance and the proof."))
closure=dict(schema="rh-conditional-closure/1",artifact_version="0.34",component="global_assembly",source_commit=PIN,
 main_sha256=sha(raw),sha256=sha(raw),provenance_sha256=sha((HERE/"provenance.json").read_bytes()),standing_assumption=standing,
 closure_semantics="Completed implications do not supply their open producer hypotheses. Only the scoped sufficient gates are established.",
 nodes=nodes,sufficient_implication_gates=gates,not_closed=not_closed,
 quantifier_checks=[
 "Same FamP and fixed constants throughout; every eventual threshold is selected before i, word u and finite place.",
 "GFA1 uses the original DlSize projection, not an added family derivative producer.",
 "GFA2 proves only the sufficient coarse original total correction bound Ta<=b²; no stronger weighted-prime conclusion is silently inferred.",
 "GFA8 is valid for every H>0 satisfying the actual lower height condition, with no added upper bound on H and an explicit zero-spread case.",
 "GFA9 chooses etaB,eB before the family member and preserves the original CH.",
 "GFA11 preserves forall c6>0 exists eK,x0 forall x>=x0 forall i, with eK=5.",
 "GFA12 proves pointwise character identities with threshold zero and keeps ChThin/ChQD estimates as premises.",
 "The final Closed transport tuple and epsilon cutoff have not been manufactured from the pointwise consumer chapters."],
 review_status="Independent review bound to final released bytes is recorded separately")
dump("closure.json",closure)
refs={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
ids={n['id'] for n in nodes}
assert len(ids)==len(nodes)
assert all(g['implies'] in ids and set(g['all_of'])<=ids for g in gates)
result=dict(status="PASS",source_commit=PIN,main_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),closure_sha256=sha((HERE/'closure.json').read_bytes()),claim_count=len(claims),source_reference_count=sum(len(c['sources']) for c in claims),distinct_source_range_count=len(refs),source_file_count=len(cache),inherited_file_count=len(inputs),all_source_blobs_match_pin=True,all_claim_dependencies_resolve=True,fresh_claim_prefix=True,all_closure_references_resolve=True,not_a_lean_recheck=True)
dump("validation.json",result)
(HERE/"report.txt").write_text("GFA original quotient/frame installation, v0.34\n\n"+standing+"\n\n"+"\n".join(f"GFA{i}: {t}" for i,t in enumerate(titles,1))+"\n\nScope: all statements retain the original same-family arithmetic premises, maps, metrics and quantifier order. The stronger weighted-prime estimate is bypassed only for the sufficient bound Ta<=b². The frame estimate holds for every original admissible H, including the zero-spread case. Primitive-character uniqueness uses CRT and multiplicativity, with no prime-progression theorem.\n\nRemaining:\n"+"\n".join(not_closed)+"\n\n"+json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False,indent=2))

