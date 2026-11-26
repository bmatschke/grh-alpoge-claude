#!/usr/bin/env python3
"""Build exact GLE proof/source provenance, checking all pinned git blobs."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
PIN="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument("--source",type=Path,default=HERE.parents[1]/"lean_source")
ap.add_argument("--baseline",type=Path,default=HERE.parents[1]/"reconstruction_v031")
args=ap.parse_args(); SOURCE=args.source.resolve(); BASE=args.baseline.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=SOURCE,text=True).strip()==PIN
raw=(HERE/"main.tex").read_bytes(); lines=raw.decode().splitlines(keepends=True)
old={c["id"]:c for c in json.loads((BASE/"provenance.json").read_text())["claims"]}
assert not any(k.startswith("GLE") for k in old)
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
    f=[(j,i) for j,(i,n) in enumerate(ds) if n==name]
    assert len(f)==1,(path,name,f)
    j,s=f[0]; e=ds[j+1][0] if j+1<len(ds) else len(ls)
    for i in range(s+1,e):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)",ls[i]): e=i; break
    while e>s+1 and not ls[e-1].strip(): e-=1
    rb="".join(ls[s:e]).encode()
    return {"path":path,"declaration":name,"source_spelling":name,"line_start":s+1,"line_end":e,
      "sha256":sha(b),"range_sha256":sha(rb),"range_bytes":len(rb),"first_line":ls[s].rstrip(),
      "verified_equal_to_pinned_git_blob":True,
      "role":"Original contract, object dictionary, or substantive proof checked against the independent human argument; source citation alone is not human closure.",
      "url":f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{s+1}-L{e}"}
sources={f"GLE{i}":[] for i in range(1,13)}
for line in (HERE/"source_anchors.txt").read_text().splitlines():
    if not line or line.startswith("#"):continue
    ids,path,names=line.split("|"); path="src/Formalism/"+path
    for name in names.split(";"):
        s=source(path,name)
        for k in ids.split():
            if s not in sources[k]:sources[k].append(s)
titles=["Original parameter windows and a uniform interval for every lifted weight",
 "TuSize gives every clause of HidaSetting on one late-family threshold",
 "Exact integral Weyl invariance, homogeneous basis and row mean",
 "Exact original rational and two local coordinate lattices",
 "Original integral up and down operators with the finite character",
 "Exact second-branch inclusion and DVR length on the original lattice",
 "Original diamond matchings and character-one local comparisons",
 "Complete original DU formula by endpoint fibers and elementary counts",
 "Ramified stability and inverse composite on the original forms",
 "One normalized original operator: finite cokernel and DVR bound",
 "Original ordered product and power: full congruence lattice length",
 "Uniform FamU installation with explicit same-selector upstream columns"]
deps={"GLE1":[],"GLE2":["GLE1"],"GLE3":[],"GLE4":["GLE3"],
 "GLE5":["GLE3","GLE4","FC1","NB2","NB3","NB7","NB8"],
 "GLE6":["GLE3","GLE4","GLE5"],"GLE7":["GLE5","NB2","NB3","NB7","NB8","RSL8"],
 "GLE8":["GLE7"],"GLE9":["GLE7","GLE8"],"GLE10":["GLE4","GLE5","GLE6","GLE9"],
 "GLE11":["GLE10"],"GLE12":["GLE2","GLE5","GLE6","GLE9","GLE11","RSL6","RSL7","RSL11","RSL12"]}
hyp={"GLE1":["Original D,L and ParameterChoice′; x>=4 and exp(x^(eps/3))>=x"],
 "GLE2":["Original FamP eps, 0<eps<1/52 and TuSize on that family"],
 "GLE3":["Original delSq, determinant shift and coefficient embedding"],
 "GLE4":["Same original Forms0 and admS; original val0.rat, val0.lat, bw0 and embeddings"],
 "GLE5":["Same original Forms0, finite K-valued level character ChiFin0, admS, original AtTTied and naturality"],
 "GLE6":["Same Forms0 and admS, plus bTop(tauOf w v)>=0; GLE5 local-prime dictionary reused without its character hypothesis"],
 "GLE7":["Same Forms0 and its naturality/level-character ties; auxiliary-prime separation from RSL8"],
 "GLE8":["Same Forms0; actual down/up indices and its original residue projections"],
 "GLE9":["Same Forms0 and its original finite-dimensional complex forms"],
 "GLE10":["Same D,u,w,v, hI/hR/hB, unique original rational descent and bTop>=0"],
 "GLE11":["Original HidaSetting and same-object hI/hR/hB; original Sram, Uprod, expT and Nlam"],
 "GLE12":["Original FamP and TuSize; same-selector eventual RealPlaceSecondLayerConditions, FormsTiedSym, ChiFin0 and admS via RSL6–7; common selector producer remains open"]}
claims=[]
for i,title in enumerate(titles,1):
    k=f"GLE{i}"; st=next(j for j,l in enumerate(lines) if l.strip()==f"% BEGIN {k}"); en=next(j+1 for j,l in enumerate(lines) if l.strip()==f"% END {k}")
    b="".join(lines[st:en]).encode(); assert all(d in old or d in deps for d in deps[k]),(k,deps[k])
    claims.append({"id":k,"title":title,"introduced_in":"0.32","classification":"B",
      "status":"Complete independent human proof of the stated conditional implication; independent review pending",
      "mathematical_status":"Human reconstruction assuming the pinned Lean proof fully checked and correct; no kernel replay or new formalization claimed",
      "scope":"Original fixed record, field, parameter witnesses, member/word, class representatives, lattices, character and operators; no replacement family",
      "depends_on":deps[k],"hypotheses_retained":hyp[k],"classical_inputs":[],
      "dependency_usage":({"GLE5":"Only the character-independent AtTTied norm/place dictionary, not the hI theorem or its ChiFin0 hypothesis"} if k=="GLE6" else {"GLE5":"Only the character-independent local move and actual finite-sum dictionary; finite character is not used for hR"} if k=="GLE7" else {}),
      "proof_location":{"file":"global_local_estimates/main.tex","paragraph":k,"label":"claim:"+k,"line_start":st+1,"line_end":en,"sha256":sha(b),"bytes":len(b)},"sources":sources[k]})
inputs=[]
for file in ["global_forms/main.tex","neighbor_geometry/main.tex","second_layer_global/main.tex","second_layer_global/provenance.json","second_layer_global/closure.json","dependency_audit_v0_31/remaining_leaf_register.json"]:
    p=BASE/file; assert p.exists(),file
    inputs.append({"file":file,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size,"scope":"Unmodified inherited v0.31 input, used only within its stated scope"})
standing="The pinned Alpoge-Claude Lean proof is fully checked and correct. Open/D statuses concern only human reconstruction and source understanding."
notclosed=["Actual compatible common selector producer","GL4 hZa/hZb/tCV original slope/operator producers","Complete eleven-field FamGLmin assembly","Full RH or unrestricted Dirichlet GRH human proof"]
prov={"schema":"rh-human-component-provenance/1","artifact_version":"0.32","date":"2026-11-22","source_commit":PIN,"component":"global_local_estimates",
 "standing_assumption":standing,"main_sha256":sha(raw),"claims":claims,"inherited_proof_inputs":inputs,
 "range_convention":"Inclusive one-based physical source/proof lines; SHA256 covers exact UTF-8 bytes including line endings.","not_closed":notclosed}
dump("provenance.json",prov)
loc=[f"GLE source locators; CocoSgt/riemann-hypothesis-lean at {PIN}","All source blobs checked against pinned git objects.",f"main.tex SHA256 {sha(raw)}",""]
for c in claims:
    p=c['proof_location']; loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c['sources']:loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append("")
(HERE/'source_locators.txt').write_text("\n".join(loc)+"\n")
nodes=[
 {"id":"ORIGINAL_FAMILY","role":"retained given input","contract":"Literal FamP eps, params/sizes/ex and common original selector, 0<eps<1/52"},
 {"id":"ORIGINAL_TUSIZE","role":"upstream producer input","contract":"TuSize on that same family; construction-class proof supplied separately"},
 {"id":"SAME_FORMS0","role":"upstream producer input","contract":"Same-selector FormsTiedSym projected to original Forms0, uniformly for each late member/word"},
 {"id":"SAME_CHIFIN0","role":"upstream producer input","contract":"Finite K-valued level character on exactly SAME_FORMS0; RSL5–6 conditionally supply it"},
 {"id":"SAME_ADMS","role":"closed conditional upstream input","contract":"admS on exactly SAME_FORMS0, by inherited RSL7"},
 {"id":"SAME_RECORD_SELECTOR","role":"open producer outside component","classification":"C","contract":"Common compatible selector realizing all original columns/forms/real-place ties; not replaced by independent choices"}]
tasks=[
 ("TASK_GL6_SIZE_SETTING","GLE2",["ORIGINAL_FAMILY","ORIGINAL_TUSIZE"],"Every literal HidaSetting clause on one late-family threshold, before i,u"),
 ("TASK_GL6_INTEGRAL","GLE5",["SAME_FORMS0","SAME_CHIFIN0","SAME_ADMS"],"HeckeIntegralLevelZero on original S_w,Bw,U,D"),
 ("TASK_GL6_RAMIFIED","GLE9",["SAME_FORMS0"],"HeckeRamifiedLevelZero on actual joint norm kernel, with p^(k-1)"),
 ("TASK_GL6_SECOND_BRANCH","GLE6",["SAME_FORMS0","SAME_ADMS"],"SecondBranchInclusionLength retaining its built-in bTop>=0 hypothesis"),
 ("TASK_GL6_CONGRUENCE_LENGTH","GLE11",["TASK_GL6_SIZE_SETTING","TASK_GL6_INTEGRAL","TASK_GL6_RAMIFIED","TASK_GL6_SECOND_BRANCH"],"Eventual CongruenceLatticeLengthBound, original product/power and unseen places")]
gates=[]
for ident,c,req,con in tasks:
    nodes.append({"id":ident,"role":"closed proof-of-implication task","classification":"B","status":"conditionally closed; independent review pending","claim":c,"contract":con})
    gates.append({"id":"GATE_"+ident,"semantics":"proved sufficient AND implication in stated scope","all_of":req,"implies":ident,"proof_claims":[c],"same_object":"Every premise on the same original D,u or FamP; no independent existential reselection"})
nodes.append({"id":"UNIFORM_GL6_LOCAL_OUTPUTS","role":"closed conditional output","contract":"Original guarded FamU hI,hR,hB plus SettingEventually and actual congruence lattice length"})
gates.append({"id":"GATE_UNIFORM_INSTALLATION","semantics":"proved sufficient guarded-family transport","all_of":[x[0] for x in tasks]+["ORIGINAL_FAMILY","SAME_FORMS0","SAME_CHIFIN0","SAME_ADMS"],"implies":"UNIFORM_GL6_LOCAL_OUTPUTS","proof_claims":["GLE12"],"threshold_order":"max(A_setting,A_forms) before i,u,w,v; preserve FamU HidaSetting guard then discharge on that same late family"})
closure={"schema":"rh-conditional-closure/1","artifact_version":"0.32","source_commit":PIN,"component":"global_local_estimates","main_sha256":sha(raw),"standing_assumption":standing,
 "closure_semantics":"A task closes only as the stated implication. Retained producer inputs remain explicit; completed implications do not assert their existence.","nodes":nodes,"sufficient_gates":gates,
 "refinement_links":[{"from":"SAME_RECORD_SELECTOR","to":["SAME_FORMS0","SAME_CHIFIN0","SAME_ADMS"],"semantics":"shared producer/navigation, not a sufficient construction of selector"}],
 "closed_task_ids":[x[0] for x in tasks],"not_closed":notclosed,
 "exact_object_checks":["tauOf on F extended to E-local ring by explicit CM trace argument","Original determinant shift in integral transport and exact length","DU line endpoint uses a^-1, whose inversion permutes diamond sum","Original foldr product, with no assumed U_v commutativity","Original d_S=D.duS distinct from smaller ramified dimension","FamU guard discharged only by same-family late threshold"]}
dump("closure.json",closure)
nids={x['id'] for x in nodes}
for g in gates:assert g['implies'] in nids and all(x in nids for x in g['all_of'])
validation={"status":"PASS","scope":"Mechanical provenance validation; mathematical review separate","source_commit":PIN,"main_sha256":sha(raw),"claim_count":len(claims),
 "claim_source_range_count":sum(map(len,sources.values())),"distinct_source_range_count":len({(s['path'],s['line_start'],s['line_end']) for v in sources.values() for s in v}),"source_file_count":len(cache),
 "all_source_files_equal_pinned_git_blobs":True,"new_claim_ids_unique_against_baseline":True,"all_proof_hashes_verified":True,"all_dependencies_resolve":True,"all_closure_references_resolve":True,
 "inherited_input_count":len(inputs),"provenance_sha256":sha((HERE/'provenance.json').read_bytes()),"closure_sha256":sha((HERE/'closure.json').read_bytes())}
dump("validation.json",validation)
report=f"""Global/local estimates, v0.32\n\nStanding assumption: the pinned Lean proof is fully checked and correct. Human reconstruction only; no kernel replay or new formal verification claimed.\n\nOutcome\nTwelve conditional claims close five selected B implication tasks: late-family Hida setting, integral original operators, ramified Hecke identity, second-branch inclusion/length, and original ordered-product congruence lattice length. The common selector remains C. Original Forms0, finite K-valued character and admS remain explicit supplied columns.\n\nMathematical contributions\nGLE1–2 extract a short weight interval from actual parameter fields and use the lower TuGe bound. One threshold before i/u supplies all strict Hida inequalities and bTop nonnegativity.\nGLE3–6 prove original integral/rational polynomial invariance and coordinate-lattice equalities, CM trace place identification, integral original transports, and determinant-shift-aware second-branch length.\nGLE7–9 prove actual diamond matchings, character-one endpoint comparisons, the finite DU fibers, trace vanishing on the joint norm kernel, and inverse UD on the original finite-dimensional ramified space.\nGLE10–11 prove the one-operator finite cokernel bound and accumulate it through the source's ordered list and mth power, including the unseen-place case.\nGLE12 installs guarded FamU outputs with a maximum threshold before i/u/w/v and retains the common selector.\n\nExact sufficient conditional cut\nOriginal FamP + original TuSize -> SettingEventually. Same Forms0 + ChiFin0 + admS -> hI. Same Forms0 -> hR. Same Forms0 + admS -> hB with its built-in bTop>=0 guard. These same-object outputs + HidaSetting -> CongruenceLatticeLengthBound. This does not construct the common selector or complete FamGLmin.\n\nNot closed\nCompatible common selector, original GL4 hZa/hZb/tCV producers, full eleven-field assembly, complete human RH/GRH.\n\nVerification\n{len(claims)} claims, {validation['claim_source_range_count']} claim-source ranges, {validation['distinct_source_range_count']} distinct ranges, {len(cache)} pinned files, all checked against {PIN}. Exact proof ranges and inherited hashes recorded. Independent mathematical review initially pending.\n\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {validation['provenance_sha256']}\nclosure.json SHA256 {validation['closure_sha256']}\n"""
(HERE/'report.txt').write_text(report)
print(json.dumps(validation,indent=2))
