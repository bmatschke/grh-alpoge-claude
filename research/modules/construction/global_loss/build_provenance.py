#!/usr/bin/env python3
"""Rebuild LFS provenance against the exact source pin and unmodified v0.34.
Usage: python build_provenance.py --source /path/to/lean_source
                                --baseline /path/to/reconstruction_v034
All output is local to this component. No Lean kernel replay is claimed.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--source", type=Path, default=HERE.parents[1]/"lean_source")
ap.add_argument("--baseline", type=Path, default=HERE.parents[1]/"reconstruction_v034")
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n")

assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=SOURCE,text=True).strip()==PIN
old = {c["id"]: c for c in json.loads((BASE/"provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"LFS\d+", k) for k in old)
raw = (HERE/"main.tex").read_bytes()
assert not any(c<32 and c not in (9,10) for c in raw)
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}
def source(path, name):
    if path not in cache:
        b=(SOURCE/path).read_bytes()
        assert b==subprocess.check_output(["git","show",PIN+":"+path],cwd=SOURCE),path
        ls=b.decode().splitlines(keepends=True)
        ds=[(i,DECL.match(x).group(1)) for i,x in enumerate(ls) if DECL.match(x)]
        cache[path]=(b,ls,ds)
    b,ls,ds=cache[path]
    found=[(j,i) for j,(i,n) in enumerate(ds) if n==name]
    assert len(found)==1,(path,name,found)
    j,st=found[0]
    en=ds[j+1][0] if j+1<len(ds) else len(ls)
    for k in range(st+1,en):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)",ls[k]):
            en=k
            break
    while en>st+1 and not ls[en-1].strip():
        en-=1
    rb="".join(ls[st:en]).encode()
    return {"path":path,"declaration":name,"source_spelling":name,
            "line_start":st+1,"line_end":en,"sha256":sha(b),"file_sha256":sha(b),
            "range_sha256":sha(rb),"range_bytes":len(rb),"first_line":ls[st].rstrip(),
            "verified_equal_to_pinned_git_blob":True,
            "role":"Exact original contract, definition or corresponding formal argument. The human proof is the independently hashed LFS block; citing this declaration is not used as its proof.",
            "url":f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}"}

anchors={f"LFS{i}":[] for i in range(1,18)}
for line in (HERE/"source_anchors.txt").read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    ids,path,names=line.split("|")
    for name in names.split(";"):
        a=source(path,name)
        for k in ids.split():
            if a not in anchors[k]:
                anchors[k].append(a)

titles=[
"Elementary exact log-four prime bounds and reciprocal-square tail",
"Dyadic order-to-residue calculation and small-order prime constant twelve",
"All first-kind small-order and narrow-power-band primes",
"Finite requested sums, discriminant term and high-prime endpoint error",
"Exact four-class deficit splitting with unchanged net gain",
"All floor, common, precision and orbit served-prime envelopes",
"Complete eleven-term original second-kind loss decomposition",
"One small-share inequality controls the second class, io sum and omitted tops",
"Uniform explicit coefficient majorants give the original leading constant and thirteen errors",
"All original Windows and WindowsD clauses with one family threshold",
"Exact lift, top, bad-top, gain and IOsum dictionaries",
"Actual type-prime exclusion, four prime classes, order projection and omitted-top inclusion",
"All eleven finite-ledger clauses installed on the original local gain record",
"Universal original ASK identity for every Reads, HEq and permitted cutoff",
"Complete same-record PrimeClassLossHypotheses from the original chosen inequalities",
"Literal LossesSmallShares with both Loss_at outputs and uniform constant",
"Literal LossFS at exponent zero, preserving the chosen pair and realizing member",
]
deps={
"LFS1":[],"LFS2":[],"LFS3":["LFS2"],"LFS4":[],
"LFS5":[],"LFS6":["LFS1"],"LFS7":["LFS3","LFS4","LFS5","LFS6"],
"LFS8":[],"LFS9":["LFS7","LFS8"],
"LFS10":["SZ1","SZ3","SZ4","SZ5","SZ6","SZ8"],
"LFS11":["LC3"],
"LFS12":["AH1","AH9","AH10","AH11","AH12","LFS11"],
"LFS13":["LFS10","LFS11","LFS12","GFA10"],
"LFS14":["AH9","AH10","AH11","GFA10","LFS11","LFS13"],
"LFS15":["LFS8","LFS11","LFS12","LFS13","GFA4"],
"LFS16":["LFS9","LFS10","LFS11","LFS14","LFS15"],
"LFS17":["LFS16"],
}
hyp={
"LFS1":["Finite prime set below Y>=1; tail starts at integer p0>=3."],
"LFS2":["e,J>=1 and Y>=1; the actual dyadic quotient order of each odd prime is <=J."],
"LFS3":["Exact first-class order-or-power-band alternative, X>=2, p0>=8, 0<=rho<=1/2."],
"LFS4":["Finite sets of natural exponents and displayed positivity, weight lower bounds, top windows and Xpp*wpp=a."],
"LFS5":["Exact unit rule, same served-top subset and ledger, zero gains/correction on unserved primes."],
"LFS6":["All displayed nonnegative envelopes, served prime upper bound, small-prime order cutoff and p0>=3; x,X,Xpp>=1."],
"LFS7":["All eleven literal ParametersHyp clauses and FirstHyp; exact original Par definitions, h<=1/2 and other displayed elementary side conditions."],
"LFS8":["The same chosen-weight inequality, bad-top inequality, second-class inclusion, io pointwise bound and omitted-top inclusion."],
"LFS9":["0<eps<1/4; e>=0; K>=1 and Cord=12<=K; original WindowsD and finite ledger with q>=1,m>=0. Threshold depends only on eps,e,K."],
"LFS10":["Same supplied FamP and its actual sizes/parameters/rho fields; fixed C and original delta(x)->0 from LinkG; no member-dependent threshold."],
"LFS11":["Same original D,L,X_G and original ParametersFill, support saturation and zero-off-support/class fields; exact coefficient-field normalization."],
"LFS12":["Same original host, type-prime norm/congruence witness, FamP drop_iff, fixed GK and Cr, literal prime-class and Frobenius definitions."],
"LFS13":["Same original LinkG_at, original parameter dictionary, actual fills, support, NumN and size fields; no new local gain producer."],
"LFS14":["Same supplied FamP with actual fill/NumN fields and original host arithmetic. Every Reads tuple, HEq and specified cutoff remains universally quantified."],
"LFS15":["Same-record ChBadp_at, ChW_at and LinkG_at, nonempty TT, literal ParTie and original family support/fill/kapI identities."],
"LFS16":["Same original FamP plus ChosenTT, ChosenBadp and LinkG. ChW_at is the pointwise premise for every sufficiently late member."],
"LFS17":["Same original FamP plus ChosenTT, ChosenBadp, LinkG and ChosenWS; preserve exact i0,av,bv,existing i1 and all-carrying-member quantifier."],
}
claims=[]
for i,title in enumerate(titles,1):
    k=f"LFS{i}"
    sts=[j for j,l in enumerate(lines) if l.strip()==f"% BEGIN {k}"]
    ens=[j+1 for j,l in enumerate(lines) if l.strip()==f"% END {k}"]
    assert len(sts)==len(ens)==1,k
    st,en=sts[0],ens[0]
    assert st<en and anchors[k]
    b="".join(lines[st:en]).encode()
    assert all(d in old or d in deps for d in deps[k]),(k,deps[k])
    claims.append({"id":k,"title":title,"introduced_in":"0.35","classification":"B",
                   "status":"Complete human proof in stated conditional scope; independent review pending",
                   "proof_status":"complete in the stated scope","review_status":"pending independent review",
                   "scope":"Original family and original loss data; exact sets, integer labels, weights, fields, gains and cutoffs.",
                   "depends_on":deps[k],"hypotheses_retained":hyp[k],"classical_inputs":[],
                   "inherited_classical_scope":"No new published theorem application. Inherited original arithmetic-host and normalized degree identities retain their recorded hypotheses.",
                   "proof_location":{"file":"global_loss/main.tex","paragraph":k,"label":"claim:"+k,
                                     "line_start":st+1,"line_end":en,"sha256":sha(b),"range_sha256":sha(b),
                                     "file_sha256":sha(raw),"bytes":len(b)},"sources":anchors[k]})
claims[9]["dependency_usage"]={"SZ8":"Original SizesAt is already a FamP field. The inherited size chapters explain each selected scalar clause; no new construction-class hypothesis is added."}
claims[13]["dependency_usage"]={"LFS11":"Only the unconditional finite set/label dictionary, with actual support/fills as FamP fields.",
                               "LFS13":"Only its original exponent-set and positive-weight dictionary. The served LinkG ledger is not needed for AskIsF; LFS14 is unconditional on LinkG for a supplied FamP."}
claims[16]["contextual_indexed_links"]=[{"id":"HW3","role":"Existing optional supplier of the exact assumed ChosenWS in the active construction; not an additional premise of the general LFS17 implication."}]

input_files=[
"size_conditions/main.tex","size_conditions/provenance.json",
"arithmetic_hosts/main.tex","arithmetic_hosts/provenance.json",
"local_accounting/local_accounting.tex",
"global_assembly/main.tex","global_assembly/provenance.json",
"global_weight_choice/main.tex","global_weight_choice/provenance.json",
"host_weight_join/main.tex","host_weight_join/provenance.json",
"second_layer_global/main.tex","second_layer_global/provenance.json",
"window_bridge/main.tex","continuation_notes_v0_34/next_global_assembly.txt",
]
inputs=[]
for f in input_files:
    b=(BASE/f).read_bytes()
    inputs.append({"file":f,"sha256":sha(b),"bytes":len(b),
                   "scope":"Unmodified v0.34 inherited proof or continuation input, used only in its stated scope."})
standing="The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Remaining classifications concern the human reconstruction only."
not_closed=[
"Existence of the compatible original FamP and its common selector or second layer.",
"An independent arithmetic producer of LinkG or its local gain inequalities.",
"A new producer for ChosenTT, ChosenBadp or ChosenWS; their supplied predicates remain exact hypotheses.",
"CoverAll or realization of arbitrary admissible weights; neither is required or asserted.",
"The source's exact pointwise size implication for every record satisfying only its particular LargeX cutoff. LFS9 proves the sufficient uniform eventual version at a possibly larger cutoff with the same constants.",
"The subsequent same-family ChainTied and Closed installation, handled by the parent component.",
"Any cohomological CountI/II/III/V producer or the complete human RH/Dirichlet-GRH proof.",
]
prov={"schema":"rh-human-component-provenance/1","artifact_version":"0.35","date":"2026-11-22",
      "source_commit":PIN,"repository":"CocoSgt/riemann-hypothesis-lean","component":"global_loss",
      "standing_assumption":standing,"main_sha256":sha(raw),"sha256":sha(raw),
      "range_convention":"Inclusive one-based physical lines. Every range hash covers exact UTF-8 bytes and line endings; sha256 aliases are explicit.",
      "claims":claims,"claim_total":len(claims),"external_literature":[],"inherited_proof_inputs":inputs,
      "not_closed":not_closed,
      "source_files":[{"path":p,"sha256":sha(b),"bytes":len(b),"line_count":len(ls),
                       "verified_equal_to_pinned_git_blob":True} for p,(b,ls,_) in sorted(cache.items())]}
dump("provenance.json",prov)
dump("published_applications.json",[])
contracts=[
{"id":"LFS_FINITE_LOSS","classification":"B","status":"closed conditional implication",
 "claims":[f"LFS{i}" for i in range(1,10)],
 "contract":"Exact original finite four-class ledger plus same small-share/bad-top hypotheses yields both (ASK-Ga)<= (2log(4)C+13sg)U and sum(log(p)io(p))<=sgU, eventually under WindowsD.",
 "requires":["all eleven ParametersHyp fields","FirstHyp","the same chosen-weight and chosen-bad inequalities","original Par definitions and WindowsD"],
 "dependency_mode":"sufficient conditional conjunction",
 "quantifiers":"Fix eps,e,K; choose one numerical threshold; then every eligible Par and every finite ledger. No dependence on cardinalities or particular primes.",
 "constants":{"Cord":12,"sg":"100*K*x^(4*eps)/x","leading":"2*log(4)*C","remainder":13}},
{"id":"LFS_WINDOWS","classification":"B","status":"closed original family implication",
 "claims":["LFS10"],"contract":"Original FamP and fixed LinkG witnesses C,delta imply the complete original Windows, its WindowsD projection, and p0<=Xprime on every late family member.",
 "requires":["same supplied original FamP","delta(x)->0"],"dependency_mode":"sufficient conditional conjunction",
 "quantifiers":"Fix family,C,delta, then e=max(40,Ct+3), K=13+abs(C), then x0, then all x>=x0,i.",
 "not_required":"GFA Win_at is a different later consumer and is not used to infer the loss windows."},
{"id":"LFS_ORIGINAL_DICTIONARY","classification":"B","status":"closed conditional installation",
 "claims":["LFS11","LFS12","LFS13","LFS15"],
 "contract":"Actual same-record fills, support, type-prime norm/congruence, LinkG_at, ChW_at and ChBadp_at install every original PrimeClassLossHypotheses field with exact lift/top/bad-top cardinalities and Ga/IOsum identities.",
 "requires":["same original D,L,X_G,GK","LinkG_at","ChBadp_at","ChW_at","nonempty original TT"],
 "dependency_mode":"sufficient conditional conjunction","quantifiers":"Pointwise in one unchanged original member; all primes, tops and lifts use that member."},
{"id":"LFS_UNIVERSAL_ASK","classification":"B","status":"closed original family implication",
 "claims":["LFS14"],"contract":"Literal AskIsF on every supplied FamP; exact original finite requested sum agrees for every Reads tuple, HEq arithmetic datum and permitted cutoff.",
 "requires":["same supplied original FamP with original host/fill/size fields"],"dependency_mode":"sufficient original field implication",
 "quantifiers":"One threshold before all x,i and then every frame,m,AD,N,TT,a,w,Reads,HEq,cutoff proof.",
 "not_required":"LinkG_at is not needed for this arithmetic identity; only the exponent/weight dictionary portion of LFS13 is reused."},
{"id":"LFS_SMALL_SHARES","classification":"B","status":"closed conditional implication",
 "claims":["LFS16"],"contract":"ChosenTT and ChosenBadp and LinkG, on the same original FamP, imply literal LossesSmallShares.",
 "requires":["ChosenTT(Fm)","ChosenBadp(Fm)","LinkG(Fm)"],"dependency_mode":"sufficient AND",
 "quantifiers":"Choose C_L and x_L once before every x>=x_L,i; ChW_at is a pointwise premise and both universally read Loss_at conclusions follow.",
 "constants":{"C_L":"3*abs(K)+13","K":"13+abs(C)","eL":0}},
{"id":"LFS_LOSS_FS","classification":"B","status":"closed conditional implication",
 "claims":["LFS17"],"contract":"ChosenTT and ChosenBadp and LinkG and ChosenWS on the same FamP imply original LossFS(Fm,0), preserving i0,av,bv and the already realizing i1.",
 "requires":["ChosenTT(Fm)","ChosenBadp(Fm)","LinkG(Fm)","ChosenWS(Fm)"],"dependency_mode":"sufficient AND",
 "quantifiers":"exists C_L,x0; forall x>=x0 in Fm.Win; exists original i0,av,bv and realizing i1; exact windows; forall original i carrying these same functions, Loss_at(L(x,i),C_L,0).",
 "forbidden_extra_assumption":"CoverAll is not an input.","endpoint_for_parent":"LFS17"},
]
closure={"schema":"rh-human-component-closure/1","version":"0.35","component":"global_loss",
         "source_commit":PIN,"standing_assumption":standing,"main_sha256":sha(raw),"sha256":sha(raw),
         "provenance_sha256":sha((HERE/"provenance.json").read_bytes()),"new_claim_ids":[c["id"] for c in claims],
         "closed_contracts":contracts,"shared_bindings":[
         "Original Fm, D, L, Gx, GK, host and coefficient field are unchanged.",
         "Original lift set has cardinality m; integer top-label set has cardinality |TT|; bad subsets agree exactly.",
         "The same Sigma and same original av,bv control the second-prime class and io sum; no reselection at another index.",
         "Original Ga has factor two; IOsum has the exact lE ramification normalization and no spurious factor two.",
         "Original ASK identity is universal in all Reads, heterogeneous arithmetic identifications and allowed cutoffs.",
         "One threshold precedes every family member and every reading; chosen i1 is retained from ChosenWS.",
         "Original joint_core constants 2log4 and 13 are retained, with Cord=12, sg=100K*x^(4eps)/x and eL=0."],
         "remaining_inputs":[
         {"classification":"C","role":"retained upstream producer","contract":"Compatible original family/common selector and its original local arithmetic LinkG producer."},
         {"classification":"inherited exact predicates","role":"retained supplied same-family choices","contract":"ChosenTT, ChosenBadp and ChosenWS with their existing producer hypotheses; their arithmetic existence is not reconstructed here."},
         {"classification":"B","role":"complementary assembly","contract":"Same-family ChainTied and Closed installation, handled by the parent GFI chapter."}],
         "not_closed":not_closed,"review_status":"pending independent mathematical review"}
dump("closure.json",closure)
loc=[f"LFS source locators — {PIN}","Inclusive one-based source and proof ranges; exact byte hashes.",f"main.tex SHA256 {sha(raw)}",""]
for c in claims:
    p=c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
ranges={(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
validation={"status":"PASS","source_commit":PIN,"main_sha256":sha(raw),"claims":len(claims),
            "claim_source_references":sum(len(c["sources"]) for c in claims),"distinct_source_ranges":len(ranges),
            "source_files":len(cache),"inherited_files":len(inputs),"checks":[
            "Exact source HEAD and every referenced pinned Git blob verified",
            "Unique exact declaration anchors and unique BEGIN/END proof blocks",
            "All actual depends_on values are new or inherited indexed claim IDs",
            "All source/proof ranges and inherited inputs have exact byte hashes",
            "Fresh LFS prefix and no unexpected control bytes"],
            "not_performed":"No Lean compilation or kernel replay; mathematical peer review is separate."}
dump("validation.json",validation)
report="""v0.35 original global loss reconstruction — LFS1–LFS17

Endpoint: the full original LossFS(Fm,0) follows from ChosenTT,
ChosenBadp, LinkG and ChosenWS ON THE SAME SUPPLIED ORIGINAL FAMILY.
No CoverAll premise is used. LFS17 preserves i0,av,bv,the realizing i1,
the exact windows, and the implication for every index carrying that pair.
LFS16 proves both original Loss_at outputs: IOsum and ASK-Ga, with the
second statement universal over all Reads/HEq/cutoff data.

The substantive proof comprises: elementary exact log-four prime bounds;
the dyadic ± residue/order calculation with constant 12; narrow power
bands; finite geometric requested sums; the four-class splitting and all
eleven loss terms; simultaneous use of the same weighted share; explicit
uniform coefficient majorants with exact leading 2 log 4 C and 13 sg;
all original Windows/WindowsD fields; same-object Ga/IO/cardinality and
arithmetic reading identities; and one-threshold family installation.

The only different numerical implementation is deliberate and stated:
the elementary asymptotic majorants choose a possibly larger common
threshold than the source's particular LargeX sufficient cutoff. They
prove the exact sufficient eventual interface, preserving every source
constant and the order of its quantifiers. They do not claim the stronger
pointwise inequality at every source-LargeX record.

Threshold order: original family, LinkG witnesses C/delta, then
e=max(40,Ct+3), K=13+abs(C), then numerical/family threshold, then x,
member i and all arithmetic readings. C_L=3 abs(K)+13; eL=0.

The upstream family and LinkG arithmetic producers remain actual inputs.
ChosenTT/ChosenBadp/ChosenWS retain their established construction scopes.
The parent handles subsequent same-family ChainTied/Closed installation.
No claim of a completed human proof of RH/GRH is made by this component.

Source and provenance verification are reproducible with build_provenance.py.
No Lean build is performed; the user's checked-source assumption is retained.
"""
report+=f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE/'closure.json').read_bytes())}\n"
report+=f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} pinned source files; {len(inputs)} inherited files.\n"
(HERE/"report.txt").write_text(report)
print(json.dumps({**validation,"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
                  "closure_sha256":sha((HERE/"closure.json").read_bytes())},indent=2))
