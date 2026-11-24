#!/usr/bin/env python3
"""Read-only proof/source/contract verification; no Lean execution."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path);args=ap.parse_args()
    errors=[]
    def check(ok,msg):
        if not ok: errors.append(msg)
    mainbytes=(HERE/"main.tex").read_bytes();mainsha=sha(mainbytes)
    p=read(HERE/"provenance.json");s=read(HERE/"source_manifest.json")
    c=read(HERE/"contracts.json");cl=read(HERE/"closure.json")
    inherited=read(HERE/"inherited_inputs.json")["inputs"]
    blocks={m.group(1).decode():m.group() for m in re.finditer(rb"% BEGIN (ALC\d+)\n.*?% END \1\n",mainbytes,re.S)}
    expected={"ALC"+str(i) for i in range(1,23)}
    check(set(blocks)==expected,"proof block inventory")
    check({x["id"] for x in p["claims"]}==expected,"provenance claim inventory")
    for name,d in [("provenance",p),("source_manifest",s),("contracts",c),("closure",cl)]:
        check(d["proof_file_sha256"]==mainsha,name+" main binding")
        check(d["source_commit"]==PIN,name+" source pin")
    for claim in p["claims"]:
        cid=claim["id"];loc=claim["proof_location"]
        piece=b"".join(mainbytes.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]])
        check(piece==blocks.get(cid),cid+" exact line range")
        check(sha(piece)==loc["sha256"],cid+" proof hash")
        check(("\\label{claim:"+cid+"}").encode() in piece,cid+" label")
        for dep in claim["depends_on"]:
            check(dep in expected or dep in {x["id"] for x in inherited},cid+" unknown dependency "+dep)
            if dep in expected: check(int(dep[3:])<int(cid[3:]),cid+" non-predecessor dependency "+dep)
    if args.repo:
        head=subprocess.check_output(["git","-C",str(args.repo),"rev-parse","HEAD"],text=True).strip()
        check(head==PIN,"repository HEAD differs from accepted pin")
    for f in s["files"]:
        body=(ROOT/f["snapshot_file"]).read_bytes()
        check(sha(body)==f["sha256"],f["path"]+" full source hash")
        check(len(body.splitlines())==f["line_count"],f["path"]+" line count")
        if args.repo:
            blob=subprocess.check_output(["git","-C",str(args.repo),"show",PIN+":"+f["path"]])
            check(body==blob,f["path"]+" pinned Git equality")
    ranges={x["id"]:x for x in s["ranges"]}
    for r in ranges.values():
        body=(ROOT/r["snapshot_file"]).read_bytes();lines=body.splitlines(keepends=True)
        piece=b"".join(lines[r["line_start"]-1:r["line_end"]])
        check(sha(piece)==r["range_sha256"],r["id"]+" range hash")
        check(sha(body)==r["file_sha256"],r["id"]+" full source binding")
    for claim in p["claims"]:
        for src in claim["sources"]: check(src==ranges.get(src["id"]),claim["id"]+" source ledger mismatch")
    for h in inherited:
        body=(ROOT/h["file"]).read_bytes();pr=(ROOT/h["parent_provenance_file"]).read_bytes()
        piece=b"".join(body.splitlines(keepends=True)[h["line_start"]-1:h["line_end"]])
        check(sha(body)==h["file_sha256"],h["id"]+" inherited file hash")
        check(sha(piece)==h["proof_range_sha256"],h["id"]+" inherited proof hash")
        check(sha(pr)==h["exact_parent_provenance_sha256"],h["id"]+" inherited provenance hash")
    for field in ["full_loc_cpl_supplied","full_loc_flat_supplied","full_loc_rho_supplied",
                  "full_original_types_supplied","full_original_loc_ex_supplied",
                  "general_local_O_scope_of_completion_suppliers_preserved",
                  "arbitrary_field_ring_map_types_scope_preserved","upstream_FinA_not_assumed"]:
        check(c.get(field) is True,"required completed scope: "+field)
    for field in ["full_sharp2_supplied","full_sharp3_supplied","full_PropagationTheoremGL2_supplied",
                  "full_PropagationTheoremGL3_supplied","actual_OffFin_producer_supplied",
                  "actual_automorphic_or_Alt_producer_supplied","full_cone_u_supplied",
                  "full_general_UnramExtY_supplied","full_GdEnd_supplied","full_HostEnd_supplied"]:
        check(c.get(field) is False,"retained boundary: "+field)
    check(c["exact_whole_closures"]=={} and cl["exact_whole_closures"]=={},"whole closure overclaim")
    t=read(HERE/"tex_validation.json")
    check(t["status"]=="PASS" and t["proof_file_sha256"]==mainsha,"TeX binding")
    check(all(v==0 for v in t["diagnostics"].values()),"TeX diagnostics")
    for rev in p["independent_reviews"]:
        b=(ROOT/rev["file"]).read_bytes();r=json.loads(b)
        check(sha(b)==rev["sha256"],"review file hash")
        check(r.get("proof_file_sha256",r.get("main_sha256",r.get("main_tex_sha256")))==mainsha,"review main binding")
        for cid in rev["claims"]: check(r["proof_hashes"].get(cid)==sha(blocks[cid]),cid+" review proof binding")
    manifest=read(HERE/"hashes.json")
    for name,h in manifest["hashes"].items(): check(sha((HERE/name).read_bytes())==h,"artifact hash "+name)
    result={"status":"PASS" if not errors else "FAIL","errors":errors,
      "component":HERE.name,"claims":len(p["claims"]),"source_files":len(s["files"]),
      "source_ranges":len(s["ranges"]),"inherited_inputs":len(inherited),
      "proof_file_sha256":mainsha,"whole_closures":{},"no_lean_replay":True}
    print(json.dumps(result,indent=2))
    if errors: raise SystemExit(1)

if __name__=="__main__": main()
