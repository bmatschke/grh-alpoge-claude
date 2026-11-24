#!/usr/bin/env python3
"""Build GVC provenance from the unchanged pinned source and v0.33 baseline.
Usage: python build_provenance.py --source /path/to/lean_source
                                --baseline /path/to/reconstruction_v033
No Lean compilation or kernel replay is performed or claimed.
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

assert subprocess.check_output(["git","rev-parse","HEAD"], cwd=SOURCE,text=True).strip()==PIN
old={c["id"]:c for c in json.loads((BASE/"provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"GVC\d+", k) for k in old), "GVC prefix already used"
raw=(HERE/"main.tex").read_bytes()
lines=raw.decode().splitlines(keepends=True)
DECL=re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache={}
def source(path,name):
    if path not in cache:
        b=(SOURCE/path).read_bytes()
        assert b==subprocess.check_output(["git","show",PIN+":"+path],cwd=SOURCE),path
        ls=b.decode().splitlines(keepends=True)
        ds=[(i,DECL.match(x).group(1)) for i,x in enumerate(ls) if DECL.match(x)]
        cache[path]=(b,ls,ds)
    b,ls,ds=cache[path]
    found=[(j,i) for j,(i,n) in enumerate(ds) if n==name]
    assert len(found)==1,(path,name,found)
    j,s=found[0]
    e=ds[j+1][0] if j+1<len(ds) else len(ls)
    for i in range(s+1,e):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)",ls[i]):
            e=i
            break
    while e>s+1 and not ls[e-1].strip():
        e-=1
    rb="".join(ls[s:e]).encode()
    return {"path":path,"declaration":name,"source_spelling":name,
            "line_start":s+1,"line_end":e,
            "sha256":sha(b),"file_sha256":sha(b),
            "range_sha256":sha(rb),"range_bytes":len(rb),"first_line":ls[s].rstrip(),
            "verified_equal_to_pinned_git_blob":True,
            "role":"Exact original contract, dictionary or corresponding source proof. Human proof is the separately hashed GVC block, not an invocation of this declaration.",
            "url":f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{s+1}-L{e}"}
anchors={f"GVC{i}":[] for i in range(1,19)}
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
"Logarithmic perturbation and harmonic gap sum",
"Exact separated-coordinate Vandermonde variation",
"Original endpoint, interior interval and top/non-top coordinate installation",
"Common mass-factor cancellation and literal logXu dictionary",
"Same original GamP and prime-center cross-word variation",
"All three clauses of the original Count_at",
"One uniform CountF constant and threshold on the original family",
"All original Wts clauses including appended weights",
"Four large finite numerical inequalities",
"All sixteen original Nums clauses with exact scaled parameter",
"Full NumsL/WtsL family supplier with the original quantifier order",
"Finite signed-sum, positive-weight, shift and spread bounds",
"Direct complete original Conclusion5 and Conclusion6 inequalities",
"Exact ConclusionF5/F6 family quantifiers",
"Original sizes imply the two required slope dominations",
"Literal SlopesM_at with exact constant 2Cc+P(12+Cc+cL)",
"Uniform original SlopesMF from the numerical packet and same ColVal",
"Actual FamP derivative projection and the final minimal supplied-family interfaces",
]
deps={
"GVC1":[],
"GVC2":["GVC1"],
"GVC3":["GVC2","DSZ4","GLE1"],
"GVC4":["GVC3","QW1","QW2","MF19"],
"GVC5":["GVC4","DSZ9"],
"GVC6":["GVC5","QW6","DSZ3","DSZ4","DSZ6","DSZ8","DSZ9"],
"GVC7":["GVC6","MF19","RSL1","RSL2","RSL3","DSZ3","DSZ5"],
"GVC8":["GLE1"],
"GVC9":[],
"GVC10":["GVC8","GVC9","AH16"],
"GVC11":["GVC8","GVC10","AH16"],
"GVC12":["GVC8"],
"GVC13":["GVC12","GLS7","GLS11"],
"GVC14":["GVC13","GLS12"],
"GVC15":[],
"GVC16":["GVC13","GVC15"],
"GVC17":["GVC11","GVC14","GVC16"],
"GVC18":["GVC7","GVC11","GVC14","GVC17","GLS12"],
}
hyp={
"GVC1":["Positive lower bound c for both real logarithm arguments; nonnegative displacement bound; finite harmonic sum."],
"GVC2":["Exactly the displayed first-row and remaining-row positive gap and displacement bounds; no family input."],
"GVC3":["For generic DataA: original fixed endpoint identities. For actual FamP: same original parameters and size records, no newly chosen Delta; one eventual threshold."],
"GVC4":["Same D, same mass/index/row factor, exact original duStar_def and Dstar_def ties; generic zero-factor cases treated explicitly."],
"GVC5":["Original GamP_eq and T_win on the same D and original two words; positive original center."],
"GVC6":["Same h2b/h2v, original degree ties and inherited DSZ/QW identities on actual coordinates; exact lower finite-sum dictionary."],
"GVC7":["One supplied original FamP and eventual same-record mass-ratio/base-volume interfaces; original degree supplier DSZ3, with its retained HC-Deg input."],
"GVC8":["Original ParameterChoice' D L; x>=4, x<=X', Cn>=3; exact original HC data and its appended weights."],
"GVC9":["All displayed finite real inequalities; no asymptotic, analytic or arithmetic existence input."],
"GVC10":["Original parameter record; all explicitly listed bounds, including derivative bound and count upper; no derivative theorem inferred."],
"GVC11":["Same supplied FamP; eventual prime upper bound and eventual derivative bound; Cn0 before Cn,cL before x0 before x,i,u."],
"GVC12":["Arbitrary original D,u with supplied Nums and Wts; x>=max(1,Cn). Only the stated numerical clauses are used."],
"GVC13":["Original open lower and upper column predicates and arbitrary same-object ColVal; no unrelated polynomial model."],
"GVC14":["Same family open-part predicates; Cn chosen before constants and thresholds; arbitrary numerical tuples and original ColVal remain universally quantified."],
"GVC15":["Original SizesAt; x>=2 and x^14<=X'; actual positive TT size and actual SizeDel."],
"GVC16":["Original Conclusion5/6, full NumsL/WtsL and all original ColVal; exact Count upper and size dominations."],
"GVC17":["Same family CountF, ConclusionF5/F6, derivative bound and eventual original ColVal; one constant and threshold before all later indices."],
"GVC18":["Original FamP.sizes already contains SizeQD derivative field. This is a projection conditional on that supplied family, not a new analytic estimate or family existence proof."],
}
claims=[]
for i,title in enumerate(titles,1):
    k=f"GVC{i}"
    starts=[j for j,l in enumerate(lines) if l.strip()==f"% BEGIN {k}"]
    ends=[j+1 for j,l in enumerate(lines) if l.strip()==f"% END {k}"]
    assert len(starts)==len(ends)==1,k
    st,en=starts[0],ends[0]
    assert st<en and anchors[k]
    b="".join(lines[st:en]).encode()
    assert all(d in old or d in deps for d in deps[k]),(k,deps[k])
    claims.append({
        "id":k,"title":title,"introduced_in":"0.34","classification":"B",
        "status":"Complete human proof in the stated conditional scope; independent review pending",
        "proof_status":"complete in the stated scope","review_status":"pending independent review",
        "scope":"Original family, member, word, field, coordinates, mass factors, level prime and column lattice; no replacement object.",
        "depends_on":deps[k],"hypotheses_retained":hyp[k],
        "classical_inputs":[],
        "inherited_classical_scope":"No new published application. Original mass/degree and GLS inputs retain their already recorded classical hypotheses.",
        "proof_location":{"file":"global_count/main.tex","paragraph":k,"label":"claim:"+k,
                          "line_start":st+1,"line_end":en,"sha256":sha(b),
                          "range_sha256":sha(b),"file_sha256":sha(raw),"bytes":len(b)},
        "sources":anchors[k],
    })
claims[11]["dependency_usage"]={"GVC8":"Only the unconditional integral-HC monotonicity argument and original coordinate dictionary; GVC12 does not import GVC8's actual ParameterChoice' existence premise."}
claims[12]["dependency_usage"]={"GLS11":"The actual c5=4 application; the displayed general c5 implication assumes the corresponding literal SlopeMax predicate."}
claims[17]["dependency_usage"]={"GVC7":"Supplies CountF in the selected route; the general implication in GVC18 accepts any given original CountF.","GLS12":"Supplies same-object open bounds and the conditional original tCV; upstream compatible columns remain a retained producer."}

input_files=[
"quantitative_windows/main.tex","quantitative_windows/provenance.json",
"degree_prime_size/main.tex","degree_prime_size/provenance.json",
"global_local_estimates/main.tex","global_local_estimates/provenance.json",
"global_slope/main.tex","global_slope/provenance.json","global_slope/published_applications.json",
"second_layer_global/main.tex","second_layer_global/provenance.json",
"mass_formula/main.tex","arithmetic_hosts/main.tex",
"continuation_notes_v0_33/next_global_assembly.txt",
]
inputs=[]
for file in input_files:
    b=(BASE/file).read_bytes()
    inputs.append({"file":file,"sha256":sha(b),"bytes":len(b),
                   "scope":"Unmodified v0.33 input, used only in the claims' stated conditional scopes."})
standing="The pinned Alpoge-Claude Lean proof is fully checked and correct. Open classifications concern the human reconstruction only."
not_closed=[
"Existence of the original compatible family, common selector, real-place second layer and original ColsTiedSym/adm3 data.",
"Stronger unused FamilyVandermondeCountExplicit, PartFiveFamilyBounds and arbitrary-space zeta_proposition_second/third interfaces.",
"Complementary quotient slopes, frame/loss estimates and the final ChainTied/LinkGLOBAL assembly; handled separately by the parent branch.",
"An analytic derivative estimate independent of the supplied FamP size fields.",
"Any cohomological CountI/II/III/V arithmetic producer.",
"The full human-readable proof of RH or unrestricted Dirichlet GRH.",
]
prov={
"schema":"rh-human-component-provenance/1","artifact_version":"0.34","date":"2026-11-22",
"source_commit":PIN,"repository":"CocoSgt/riemann-hypothesis-lean","component":"global_count",
"standing_assumption":standing,"main_sha256":sha(raw),"sha256":sha(raw),
"range_convention":"Inclusive one-based physical lines. Every range hash covers exact UTF-8 bytes and line endings. Source sha256/file_sha256 alias the pinned entire file; proof sha256/range_sha256 alias its exact claim block.",
"claims":claims,"claim_total":len(claims),"external_literature":[],
"inherited_proof_inputs":inputs,"not_closed":not_closed,
"source_files":[{"path":p,"sha256":sha(b),"bytes":len(b),"line_count":len(ls),
                 "verified_equal_to_pinned_git_blob":True} for p,(b,ls,_) in sorted(cache.items())],
}
dump("provenance.json",prov)
dump("published_applications.json",[])

contracts=[
{"id":"GVC_VANDERMONDE","status":"closed conditional implication","classification":"B",
 "claims":["GVC1","GVC2","GVC3","GVC4"],
 "contract":"Every original D and supplied DataA imply literal VandermondeVariationExplicitBound; on an original FamP the necessary coordinate subconditions are installed uniformly on the actual Delta and endpoints.",
 "quantifiers":"Generic forall D,sc,C0,CY,Delta,w,hA,omega,omega',tau; actual family exists x0 before all x,i,omega,omega',tau.",
 "requires":["original fixed endpoint and cloud identities"],"dependency_mode":"sufficient conditional hypotheses",
 "stronger_not_claimed":["full FamilyVandermondeCountExplicit","full PartFiveFamilyBounds"]},
{"id":"GVC_COUNT_F","status":"closed conditional implication","classification":"B",
 "claims":["GVC4","GVC5","GVC6","GVC7"],
 "contract":"Same FamP plus eventual original MassRatio2 and BaseVolumeEqualsMass, with DSZ3 degree supplier, imply literal CountF.",
 "quantifiers":"After FamP, fix CY and Cc=max(Ceps+2,8+3CY,4), then x0, then all x>=x0,i and both words.",
 "requires":["same original FamP","same-record mass ratio","same-record base volume identity","inherited DSZ3 and QW/DSZ proofs"],
 "dependency_mode":"sufficient conditional hypotheses","constants":{"Ceps":"30+(2+2CY)/eps","Cc":"max(Ceps+2,8+3CY,4)"}},
{"id":"GVC_NUMS_WTS_PARAMETERIZED","status":"closed conditional implication","classification":"B",
 "claims":["GVC8","GVC9","GVC10","GVC11"],
 "contract":"Original family, eventual log(T)<=Cc*m*ell and eventual actual derivative bound imply full NumsL and WtsL.",
 "quantifiers":"exists Cn0, forall Cn>=Cn0, forall cL>=3, exists x0, forall x>=x0, forall i, forall omega.",
 "requires":["same original FamP","eventual count upper","eventual original derivative bound"],
 "dependency_mode":"sufficient conditional hypotheses",
 "constant":"Cn0=max(max(3,max(Cc,0)),Fm.PK.getD(19,0)+1)"},
{"id":"GVC_DERIVATIVE_PROJECTION","status":"closed original field projection","classification":"B",
 "claims":["GVC18"],
 "contract":"FamP.sizes -> seventh SizesAt conjunct SizeQD -> sixth SizeQD conjunct gives original derivative bound, threshold Fm.x1+1.",
 "quantifiers":"exists x0=Fm.x1+1 before all x>=x0,i.",
 "requires":["same supplied original FamP including its size fields"],"dependency_mode":"sufficient exact projection",
 "not_claimed":"No independent analytic derivative theorem and no new FamP existence theorem."},
{"id":"GVC_NUMS_WTS_ACTUAL","status":"closed conditional implication","classification":"B",
 "claims":["GVC11","GVC18"],
 "contract":"Original FamP and CountF imply full literal NumsL/WtsL, including fixed cL=3, by the parameterized supplier and derivative projection.",
 "quantifiers":"exists Cn0, forall Cn>=Cn0, forall cL>=3, exists x0, forall x>=x0,i,omega.",
 "requires":["same original FamP","CountF"],"dependency_mode":"sufficient proved conjunction",
 "use_by_parent":"At cL=3 supplies full numerical/weight input for original weight9 and adm26=36; those latter calculations are outside GVC."},
{"id":"GVC_CONCLUSION_F5_F6","status":"closed conditional implication","classification":"B",
 "claims":["GVC12","GVC13","GVC14"],
 "contract":"Original family lower/maximal open column inequalities imply exact ConclusionF5/F6.",
 "quantifiers":"forall Cn, exists C-,C+,x-,x+, forall later x,i, then all original word/numerical tuples/ColVal.",
 "requires":["same family FamilySlopeLowerOpenPart","same family FamilySlopeMaxOpenPart(c5)"],
 "dependency_mode":"sufficient conditional hypotheses",
 "constants":{"K":"max(1,Cn)","Cminus":"K+2","Cplus":"(max(c5,0)+1)*(K+4)","actual_c5":4},
 "stronger_not_claimed":["zeta_proposition_second","zeta_proposition_third"]},
{"id":"GVC_SLOPES_MF","status":"closed conditional implication","classification":"B",
 "claims":["GVC11","GVC14","GVC15","GVC16","GVC17","GVC18"],
 "contract":"Same original FamP, CountF, lower/maximal open column predicates and eventual same-object ColVal imply literal SlopesMF.",
 "quantifiers":"Choose Cc, then Cn and cL=3, then C-/C+, then Cs and x0, then all x>=x0,i,omega.",
 "requires":["same original FamP","CountF","FamilySlopeLowerOpenPart","FamilySlopeMaxOpenPart(4)","eventual original ColVal on that same family"],
 "dependency_mode":"sufficient proved conjunction",
 "constants":{"P":"max(Cminus,Cplus,0)","Cs":"2*Cc+P*(12+Cc+cL)","cL":3},
 "exact_object":"(D.fm omega).lat 0, with the actual rational lattice and all original ColVal norms."},
]
closure={
"schema":"rh-human-component-closure/1","version":"0.34","component":"global_count",
"source_commit":PIN,"standing_assumption":standing,"main_sha256":sha(raw),"sha256":sha(raw),
"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
"new_claim_ids":[c["id"] for c in claims],"closed_contracts":contracts,
"shared_bindings":[
"All contracts use the same supplied FamP, D=Fm.D(x,i), L=Fm.L(x,i), and original word. No family is reselected.",
"Original Delta, first/last endpoints, dsig, mass/index factors, coefficient field, GamP and Tstar/T windows are preserved.",
"Both finite sums use the original f-place Tau set; normalization is 1/f and logXu normalization 1/(f*k).",
"Column metric and rational lattice are exactly the GLS ColVal object on (D.fm omega).lat 0.",
"Thresholds precede all member, word, archimedean-place and coefficient-place choices.",
"Global Cabs=2,C0=3,C5=4,eD=2,eL=0 are unchanged; CY is only an unrelated auxiliary size constant.",
],
"remaining_inputs":[
{"classification":"C","role":"retained upstream producer","contract":"Compatible original family/common selector and original real-place second layer/ColsTiedSym/adm3 required by tCV; GVC supplies no existence construction."},
{"classification":"inherited","role":"retained same-record interfaces","contract":"Mass ratio/base volume and original degree supplier retain the MF/RSL/DSZ hypotheses and published inputs."},
{"classification":"B","role":"complementary reconstruction","contract":"Original quotient slopes, frame/loss estimates and one-family terminal assembly; parent's separate branch."}
],
"not_closed":not_closed,
"review_status":"pending independent mathematical review",
}
dump("closure.json",closure)
loc=[f"GVC source locators — {PIN}","All hashes bind exact pinned Git blobs; inclusive one-based ranges.",
     f"main.tex SHA256 {sha(raw)}",""]
for c in claims:
    p=c["proof_location"]
    loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c["sources"]:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
ranges={(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
validation={
"status":"PASS","source_commit":PIN,"main_sha256":sha(raw),
"claims":len(claims),"claim_source_references":sum(len(c["sources"]) for c in claims),
"distinct_source_ranges":len(ranges),"source_files":len(cache),"inherited_files":len(inputs),
"checks":["Source HEAD equals exact pin","Every referenced file equals its pinned Git blob",
          "Every source declaration found uniquely","Every claim has unique exact BEGIN/END block",
          "Every inherited claim dependency exists in unchanged v0.33 provenance",
          "GVC prefix is unused in baseline","All input files hashed","Every source/proof range hashed"],
"not_performed":"No Lean build or kernel replay; independent mathematical review remains separate.",
}
dump("validation.json",validation)
print(json.dumps({**validation,"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
                  "closure_sha256":sha((HERE/"closure.json").read_bytes())},indent=2))
