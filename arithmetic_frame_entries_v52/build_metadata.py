#!/usr/bin/env python3
"""Bind AFE human arguments, original contracts and inherited reviewed proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
V = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
F = V + "FrobeniusSmoothVectors/"
C = V + "CurveDVRSpecialization/"
H = V + "HeightAndVanishing/"
U = V + "UnitaryThreeGroups/"
D = V + "UnitaryThreeDeformations/"
SPECS = {
    "parts": (H+"DirichletPrimeToLPartMulLPowerPart.lean", "Original Coef, CRT comp, primary parts, c2, Sb and Tb"),
    "gd": (H+"Counts.lean", "Full original twelve-field GD antecedent"),
    "dat": (U+"RhoKApply.lean", "Full original Dat, its character and specified conjugation"),
    "gen": (F+"FrobeniusSplitPrimeDatum.lean", "All nineteen Gen fields and full HasFrameW"),
    "gd_entry": (F+"SqrtDiscr.lean", "Original gen_gd; discriminant and residue dictionary"),
    "host_data": (D+"IsHostFrame.lean", "Full HostData, eta4 and ten IsHostFrame fields"),
    "host_entry": (F+"GenHost.lean", "Original gen_host; exact Hb and both nondegeneracy conditions"),
    "dyadic": (D+"DyadicCharacterPowerNeOne.lean", "Dyadic conductor obstruction, corrected Frobenius and original exists_sigma"),
    "host_frame": (D+"HostEx.lean", "Original actual GS/toGS auxiliary Host-frame construction"),
    "cyclotomic": (V+"CharacterLevelBounds/ClsFacts.lean", "Exact finite cyclotomic action and inertia dictionary"),
    "dat_facts": (U+"DatFacts.lean", "Source context for original Dat facts; full dat_facts is not separately claimed"),
    "has_frame": (C+"HostFrameEx.lean", "GalLink, SeedClause, HasFrame, GdFrameEx and HostFrameEx"),
    "gd_join": (F+"GdEx.lean", "Original Hypotheses2 implies GdFrameEx"),
    "host_join": (F+"HostEx.lean", "Original Hypotheses2 implies HostFrameEx"),
    "frame_ex": (F+"FrameEx.lean", "Inherited exact full frame_ex constructor"),
    "seed": (F+"SeedCl.lean", "Q-before-field coefficient-DVR character seed"),
    "P": (V+"GaloisCochains/GLinkQuot.lean", "Original retained GC.Hypotheses2"),
    "automorphic_seeds": (V+"IdeleGenerators/ShapeFacts.lean", "Separate original Seed2 and Seed3 producers remain unsupplied"),
    "ordinary_end": (C+"RatTorsionFree.lean", "Exact OrdPt, FinEnd, AutEnd2/3, HostEnd and GdEnd"),
    "nrep": (C+"ExistsNrep3.lean", "Full original ordinary-point-to-NRep transport"),
    "fin_end": (C+"FinEndOfFinPt.lean", "Full original finEnd_of_finPt with subgroup before coefficients"),
    "fin_pt": (C+"PropagationTheoremGL2.lean", "Literal IsLiftA and retained FinPt"),
    "nrep_defs": (F+"LeAdicClosure.lean", "Actual NRep, ordered product, IsBar and IsDiag"),
    "frame_defs": (F+"ContinuousCoboundaries2.lean", "Frame topologies, localization and Ok normalization"),
    "gg": (U+"UnitaryThreeReflectionRight.lean", "Semidirect group, J, weights, reference representation and Normalised"),
    "marks": (U+"BaseRepGL3NormalisedOfPsiEqOne.lean", "All five original Marks fields"),
    "local": (D+"AdjointDiagonalRepPreservesWeightPiece.lean", "Exact Red, CondT, TriIn and adic continuity"),
    "star": (U+"MatGstar.lean", "Literal polarization matrix identity"),
    "cd": (C+"IsUnitOrIsUnitOfAddOne.lean", "Exact IsCD coefficient class"),
}
REL = {
  1: ([], ["parts","gd_entry","dyadic"], []),
  2: ([1], ["parts","dyadic"], []),
  3: ([1,2], ["cyclotomic","gd_entry","dyadic"], []),
  4: ([], ["gd","dat","gd_entry"], []),
  5: ([1,3,4], ["gd_entry","dat_facts"], []),
  6: ([1,2,3,5], ["gd","dat","gd_entry","host_entry"], []),
  7: ([1,3,4,5,6], ["gd","dat","gen","gd_entry"], []),
  8: ([1,2,3], ["host_data","host_entry"], []),
  9: ([2], ["parts","dyadic"], []),
 10: ([1,2,3,9], ["host_data","dyadic","host_entry"], []),
 11: ([1,2,3], ["parts","host_entry"], []),
 12: ([1,3,6,8,10,11], ["gen","host_data","host_entry"], []),
 13: ([3], ["host_data","host_frame","cyclotomic"], []),
 14: ([1,10], ["host_data","dyadic"], []),
 15: ([7], ["gd_join","has_frame","frame_ex","seed","P"], ["CAF7","CAF11","LFC22","LFC23"]),
 16: ([12], ["host_join","has_frame","frame_ex","seed","P"], ["CAF7","CAF11","LFC22","LFC23"]),
 17: ([7,12,15,16], ["marks","has_frame"], []),
 18: ([], ["local","nrep","nrep_defs","gg"], []),
 19: ([18], ["has_frame","ordinary_end","nrep","nrep_defs","frame_defs","star","fin_pt"], []),
 20: ([19], ["ordinary_end","fin_end","fin_pt","cd"], []),
 21: ([1,15,16,17,20], ["has_frame","ordinary_end","fin_end","fin_pt"], []),
}
EXT = {
 "AFE_GALOIS_FOUNDATIONS": {
   "kind": "standard_algebraic_number_theory",
   "statement": "Finite/infinite Galois correspondence; algebraic embeddings and extension of valuations; local decomposition/inertia and residue Frobenius dictionary; compactness of profinite Galois groups; elementary integral-basis theory; Hensel's lemma for Z_ell. Required cyclotomic surjectivity, discriminant containment, torsion and conductor calculations are proved in AFE1–12.",
   "source_keys": ["cyclotomic","gd_entry","host_frame","dyadic"]},
 "AFE_ORIGINAL_DAT": {
   "kind": "original_theorem_antecedent",
   "statement": "The full original Dat, hence all original GD fields, coefficient c.O, specified imaginary quadratic field/embedding, character, complex conjugation and arbitrary specified valuation above ell. No original input is silently weakened in the asserted full implication.",
   "source_keys": ["parts","gd","dat","gd_entry"]},
 "AFE_ORIGINAL_HOST": {
   "kind": "original_theorem_antecedent",
   "statement": "The full original HostData, c.O, N nonzero, specified complex conjugation and arbitrary specified valuation. ell is an odd prime, including 3. In AFE14 the full supplied IsHostFrame is retained.",
   "source_keys": ["parts","host_data","host_entry","dyadic"]},
 "AFE_ORIGINAL_P": {
   "kind": "original_theorem_antecedent",
   "statement": "Original GC.Hypotheses2, at exactly the LFC22–23 scope; the local/global cohomological suppliers and inherited classical foundations are retained. P is used only in the common-frame conclusions and their resulting marking/finite-end joins.",
   "source_keys": ["P","gd_join","host_join"]},
 "AFE_ORIGINAL_LINKED_POINT_INPUTS": {
   "kind": "original_theorem_antecedent",
   "statement": "For AFE19–20: full GalLink, full Ok, residue characteristic ell, ell divides M, sigma squared equals one; original OrdPt over a local Noetherian domain with a local coefficient map. AFE20 retains actual FinPt on that same frame and the exact IsCD coefficient class.",
   "source_keys": ["has_frame","ordinary_end","nrep","fin_end","fin_pt","cd"]},
 "AFE_STANDARD_LOCAL_ALGEBRA": {
   "kind": "named_classical_commutative_algebra",
   "statement": "Artin–Rees and Nakayama over Noetherian local rings, used in AFE19 to prove the needed Krull intersection and closed matrix-identity locus. No completeness or flatness is added to exists_nrep3.",
   "source_keys": ["nrep"]},
}
USES = {i: ["AFE_GALOIS_FOUNDATIONS"] for i in REL}
for i in [4,5,6,7,15]: USES[i].append("AFE_ORIGINAL_DAT")
for i in [8,10,12,13,14,16]: USES[i].append("AFE_ORIGINAL_HOST")
for i in [15,16,17,21]: USES[i].append("AFE_ORIGINAL_P")
for i in [19,20]: USES[i].append("AFE_ORIGINAL_LINKED_POINT_INPUTS")
USES[19].append("AFE_STANDARD_LOCAL_ALGEBRA")
USES[18] = []

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n")

def inherited(cid):
    component = "linked_frame_completion_v51" if cid.startswith("LFC") else "common_arithmetic_frame_v50"
    rel = component+"/main.tex"
    raw = (ROOT/rel).read_bytes()
    provrel = component+"/provenance.json"
    provraw = (ROOT/provrel).read_bytes()
    old = next(c for c in json.loads(provraw)["claims"] if c["id"] == cid)
    loc = old["proof_location"]
    first, last = loc["line_start"], loc["line_end"]
    piece = b"".join(raw.splitlines(keepends=True)[first-1:last])
    if sha(piece) != loc.get("sha256",loc.get("proof_range_sha256")):
        raise ValueError(("inherited proof hash",cid))
    return {"id":cid,"component":component,"file":rel,"label":"claim:"+cid,
        "file_sha256":sha(raw),"line_start":first,"line_end":last,
        "proof_range_sha256":sha(piece),"parent_provenance_file":provrel,
        "exact_parent_provenance_sha256":sha(provraw),
        "scope":"Inherited reviewed human theorem at its exact original scope, including retained P/classical inputs"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    args = ap.parse_args()
    repo = args.repo.resolve()
    if subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip() != PIN:
        raise ValueError("wrong source pin")
    sources, files, excerpts, source_texts = {}, {}, [], {}
    for key,(rel,title) in SPECS.items():
        blob = subprocess.check_output(["git","-C",str(repo),"show",PIN+":"+rel])
        if (repo/rel).read_bytes() != blob:
            raise ValueError(("source checkout differs from pin",rel))
        dst = ROOT/"source_snapshot_v0_52/arithmetic"/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(blob)
        count = len(blob.splitlines())
        url = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/"+PIN+"/"+rel
        files[rel] = {"path":rel,"snapshot_file":str(dst.relative_to(ROOT)),
            "sha256":sha(blob),"bytes":len(blob),"line_count":count,
            "source_commit":PIN,"url":url,"verified_equal_to_pinned_git_blob":True}
        sources[key] = {"id":"AFE_SRC_"+key.upper(),"path":rel,"declaration":title,
            "line_start":1,"line_end":count,"source_commit":PIN,
            "file_sha256":sha(blob),"full_file_sha256":sha(blob),"range_sha256":sha(blob),
            "range_bytes":len(blob),"snapshot_file":str(dst.relative_to(ROOT)),
            "verified_equal_to_pinned_git_blob":True,"url":url+f"#L1-L{count}"}
        source_texts[key] = blob.decode()
        excerpts.append("["+sources[key]["id"]+"] "+title+"\n"+sources[key]["url"]+"\n"+blob.decode())
    txt = (HERE/"main.tex").read_text()
    mainhash = sha(txt.encode())
    blocks = {m.group(1):m for m in re.finditer(r"% BEGIN (AFE\d+)\n.*?% END \1\n",txt,re.S)}
    expected = {"AFE"+str(i) for i in REL}
    if set(blocks) != expected:
        raise ValueError("claim block set mismatch")
    blockhash = {cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews = []
    for p in sorted(set(HERE.glob("review_*.json"))|set(HERE.glob("independent_review*.json"))):
        data = json.loads(p.read_text())
        if data.get("result",data.get("status")) != "PASS":
            continue
        full = data.get("proof_file_sha256",data.get("main_sha256",data.get("main_tex_sha256")))
        if full and full != mainhash:
            raise ValueError(("stale review main hash",p))
        rc = data.get("claims_reviewed",data.get("reviewed_claims",[]))
        ids = []
        for item in rc:
            cid = item if isinstance(item,str) else item.get("id",item.get("claim"))
            bh = (rc.get(cid) if isinstance(rc,dict) else data.get("proof_hashes",{}).get(cid)) if isinstance(item,str) else item.get("proof_range_sha256",item.get("block_sha256"))
            if bh is None and full == mainhash:
                bh = blockhash.get(cid)
            if cid not in blockhash or bh != blockhash[cid]:
                raise ValueError(("stale review proof block",p,cid))
            ids.append(cid)
        reviews.append({"file":str(p.relative_to(ROOT)),"sha256":sha(p.read_bytes()),
            "reviewer":data.get("reviewer"),"result":"PASS","proof_file_sha256":mainhash,"claims":ids})
    reviewed = {cid for r in reviews for cid in r["claims"]}
    status = "complete_at_stated_scope_independently_reviewed" if expected <= reviewed else "complete_at_stated_scope_pending_independent_review"
    human = {cid:inherited(cid) for _,_,ids in REL.values() for cid in ids}
    claims = []
    for i,(deps,keys,ids) in REL.items():
        cid = "AFE"+str(i)
        m = blocks[cid]
        start = txt[:m.start()].count("\n")+1
        claims.append({"id":cid,"title":m.group().split("\n")[1],
            "introduced_in":"0.52","classification":"B",
            "depends_on":["AFE"+str(d) for d in deps]+ids,
            "external_input_ids":USES[i],"sources":[sources[k] for k in keys],
            "proof_location":{"file":HERE.name+"/main.tex","label":"claim:"+cid,
                "line_start":start,"line_end":start+m.group().count("\n")-1,
                "sha256":blockhash[cid],"bytes":len(m.group().encode())},
            "status":"complete_at_stated_scope_independently_reviewed" if cid in reviewed else "complete_at_stated_scope_pending_independent_review",
            "independent_review_files":[r["file"] for r in reviews if cid in r["claims"]],
            "source_proof_is_not_human_proof":True})
    ext = [{"id":eid,**e,"source_bindings":[sources[k] for k in e["source_keys"]]} for eid,e in EXT.items()]
    common = {"artifact_version":"0.52","component":HERE.name,"source_commit":PIN,
        "proof_file_sha256":mainhash,"status":status}
    endpoints = [
      {"id":"full_original_gen_gd","claim":"AFE7","Gen_fields":19,"Hb":"top","M":"ell*N*abs(disc K)","coefficient_scope":"original Coef DVR c.O"},
      {"id":"full_original_gen_host","claim":"AFE12","Gen_fields":19,"Hb":"ker(dirG(kapB ell psi))","M":"ell*N","host_ell_3_allowed":True,"specified_valuation_retained":True},
      {"id":"full_original_exists_hostFrame","claim":"AFE13","fields":10,"P_required":False},
      {"id":"full_original_exists_sigma","claim":"AFE14","scope":"every v in Tb on every supplied original IsHostFrame","P_required":False},
      {"id":"full_original_GdFrameEx_at_P","claim":"AFE15","Q_before_L_w":True,"same_g1":True},
      {"id":"full_original_HostFrameEx_at_P","claim":"AFE16","Q_before_L_w":True,"same_g1":True,"host_ell_3_allowed":True},
      {"id":"original_Marks_on_same_g1","claim":"AFE17","fields":5},
      {"id":"full_original_exists_nrep3","claim":"AFE19","scope":"arbitrary original local O and local Noetherian domain A, local coefficient map, literal GalLink/Ok/OrdPt","no_flatness_added":True,"no_completeness_added":True},
      {"id":"full_original_finEnd_of_finPt","claim":"AFE20","FinPt_retained":True,"subgroup":"G_L","subgroup_before_coefficient_algebra_and_point":True},
      {"id":"same_frame_Marks_and_FinPt_implies_FinEnd","claim":"AFE21","P_retained":True,"same_g1":True},
    ]
    field_map = {
      "odd":[7,12],"fin":[1,7,12],"M_ne":[7,12],"l_dvd":[7,12],
      "two_dvd":[7,12],"cc":[7,12],"over_l":[7,12],"quad":[4,7,12],
      "cyc":[3,5,7,12],"eta_l":[3,5,7,12],"even":[7,12],
      "Psi_l":[6,7,12],"g4":[6,7,8,12],"g5":[6,7,10,12],
      "Hb_open":[7,11,12],"Hb_ab":[7,11,12],"Hb_idx":[7,11,12],
      "Hb_l":[7,11,12],"teich":[1,3,7,11,12]}
    contracts = {"schema":"rh-human-component-contract/1",**common,
      "closed_subcontracts":endpoints,
      "entry_premises":["Full original Dat/GD for Dat branch","Full original HostData for Host branch",
        "Original Coef DVR for both Gen entries and character SeedClause",
        "Original GC.Hypotheses2 for final frame constructors",
        "CAF7/CAF11 and LFC22/LFC23 at exact reviewed scope",
        "Literal GalLink, Ok and OrdPt for general transport",
        "Actual FinPt remains an antecedent of FinEnd transport"],
      "Gen_field_proofs":{k:["AFE"+str(i) for i in v] for k,v in field_map.items()},
      "full_original_Gen_supplied_for_Dat":True,"full_original_Gen_supplied_for_HostData":True,
      "full_GdFrameEx_closed_at_original_P":True,"full_HostFrameEx_closed_at_original_P":True,
      "original_P_retained":True,"host_ell_3_allowed":True,
      "full_exists_hostFrame_closed":True,"full_exists_sigma_closed":True,
      "full_exists_nrep3_closed":True,"full_finEnd_of_finPt_closed":True,
      "FinPt_producer_supplied":False,"AutEnd_transports_supplied":False,
      "full_GdEnd_closed":False,"full_HostEnd_closed":False,
      "both_automorphic_seed_producers_remain_open":True,"original_alt_matching_remains_open":True,
      "choice_order":["original Dat/HostData and specified valuation",
        "full Gen with its literal Hb and modulus","CAF7 character data and Q",
        "LFC22 L,g1,Phi,C0,w at that Q","all 28 Ok fields and Big on same Phi,C0",
        "CAF11 SeedClause on same L,w with same marked g1",
        "conditional FinPt on same Phi","G_L before every later coefficient algebra and ordinary point"],
      "simplifications":["Quadratic Gauss sums replace general abelian-field cyclotomic containment",
        "Original GD kernel and weight conditions directly supply g4 and g5",
        "Host local witness obtained directly at each specified valuation using corrected Frobenius and actual dyadic conductor",
        "Ordered ordinary product proved from the preserved standard flag"],
      "selected_producer_closed":False,"new_global_frontier_leaf_closures":[],
      "root_ledger_modified":False,"no_lean_replay":True}
    dump("contracts.json",contracts)
    dump("original_contracts.json",{**contracts,
      "verbatim_source_contract_files":{k:source_texts[k] for k in ["parts","gd","dat","gen","host_data","has_frame","ordinary_end","fin_pt","cd"]}})
    dump("provenance.json",{"schema":"rh-human-component-provenance/1",**common,
      "claims":claims,"inherited_human_inputs":list(human.values()),
      "classical_and_foundational_inputs":ext,"independent_reviews":reviews,
      "source_proof_is_not_human_proof":True,"root_ledger_modified":False})
    dump("source_manifest.json",{"schema":"rh-pinned-source-manifest/1",**common,
      "source_repository":"https://github.com/CocoSgt/riemann-hypothesis-lean",
      "files":list(files.values()),"ranges":list(sources.values()),
      "file_count":len(files),"range_count":len(sources)})
    dump("inherited_inputs.json",{"schema":"rh-inherited-proof-bindings/1",**common,"inputs":list(human.values())})
    dump("closure.json",{"schema":"rh-human-component-closure/1",**common,
      "closed_subcontracts":endpoints,"independent_reviews":reviews,
      "pending_review_claims":sorted(expected-reviewed,key=lambda x:int(x[3:])),
      "new_global_frontier_leaf_closures":[],"proposed_global_frontier_leaf_closures":[],
      "full_original_gen_gd_closed":True,"full_original_gen_host_closed":True,
      "full_GdFrameEx_closed_at_original_P":True,"full_HostFrameEx_closed_at_original_P":True,
      "original_P_retained":True,"full_finEnd_of_finPt_closed":True,
      "FinPt_producer_remains_open":True,"full_GdEnd_remains_open":True,"full_HostEnd_remains_open":True})
    dump("retained_foundations.json",ext)
    dump("classical_inputs.json",{"schema":"rh-classical-input-registry/1",**common,"inputs":ext})
    dump("published_inputs.json",[])
    dump("claim_dag.json",{"schema":"rh-human-claim-dag/1",**common,
      "claims":[{"id":c["id"],"depends_on":c["depends_on"]} for c in claims]})
    (HERE/"source_excerpts.txt").write_text("\n\n".join(excerpts))
    report = """ARITHMETIC FRAME ENTRIES — v0.52

AFE1–AFE21 prove both full original nineteen-field Gen implications:
gen_gd uses Hb=top and M=ell*N*abs(disc K);
gen_host uses Hb=ker(dirG(kapB ell psi)) and M=ell*N.
Every originally specified ell-adic valuation is retained.
The Host proof permits ell=3.

Underlying human arguments include finite coefficient residue fields,
prime-to-ell torsion reduction, exact CRT and primary character parts,
cyclotomic inertia surjectivity at every prolongation, corrected local
Frobenius, the quadratic integral basis and discriminant root, and an
elementary quadratic Gauss-sum cyclotomic containment. The Dat g4/g5
conditions follow directly from its original kernel and weight fields.

The Host proof gives the dyadic kernel obstruction and proves the exact
conductor-power inequality through principal-unit generation. It then
constructs the nonquadratic witness at every p in Tb and every place
above p. Full original exists_hostFrame and exists_sigma are also
proved, without the cohomological P premise.

With original P=GC.Hypotheses2 retained, both full GdFrameEx and
HostFrameEx now follow from the inherited LFC constructor. CAF7 selects
Q before L,w. CAF11 installs the actual character seed on that same L,
with the same g1, Phi and C0. All original Marks fields hold.

A further bounded transport is completed: the actual ordinary Galois
point descends to an NRep, with polarization, every normalization entry,
the ordered ordinary-product law, adic continuity and exact local
characters. This proves full original exists_nrep3 for arbitrary
Noetherian local-domain target A and a local coefficient map. No
flatness or completeness is added. The original finEnd_of_finPt follows,
choosing G_L before every coefficient algebra and every ordinary point.

EXACT BOUNDARY
P remains an original premise. The character SeedClause is not either
automorphic seed representation. The actual FinPt producer, AutPt and
AutPtAlt producers and their remaining automorphic transports remain
separate. Neither full GdEnd nor full HostEnd, and no whole selected
compound leaf or complete human RH/Dirichlet GRH proof, is asserted
closed. All v51 and earlier artifacts are unchanged.

The direct Host argument avoids importing an unproved earlier Host
frame; the latter is reconstructed independently. Standard retained
foundations are the local/global Galois-place dictionary, Hensel,
integral-basis theory, and Artin–Rees/Nakayama for the closed matrix
kernel argument. All specialized character and matrix calculations are
given in the numbered human proofs.
No Lean replay and no PDF. All source snapshots equal pinned git blobs.
"""
    (HERE/"report.txt").write_text(report+f"\nPin: {PIN}\nMain SHA256: {mainhash}\nStatus: {status}\nClaims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}\n")
    dump("hashes.json",{"component":HERE.name,"artifact_version":"0.52",
      "hashes":{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
                if p.is_file() and p.name!="hashes.json"}})
    print(json.dumps({"component":HERE.name,"claims":len(claims),"source_files":len(files),
        "source_ranges":len(sources),"main_sha256":mainhash,"status":status},indent=2))

if __name__ == "__main__":
    main()
