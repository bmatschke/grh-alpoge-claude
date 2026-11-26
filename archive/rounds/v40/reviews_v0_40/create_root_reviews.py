#!/usr/bin/env python3
"""Bind the parent's independent mathematical reviews to final component bytes."""
from pathlib import Path
import argparse, hashlib, json, subprocess
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument("--components",type=Path,default=HERE.parent)
p.add_argument("--baseline",type=Path,default=HERE.parents[1]/"reconstruction_v039")
p.add_argument("--source",type=Path,default=HERE.parents[1]/"lean_source")
a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda q:json.loads(q.read_text())
pin="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
old={c["id"]:c for c in read(a.baseline/"provenance.json")["claims"]}
findings={
"comparison_packet":[
"Exact Mat1/Sp1/Tie1, ChT/LfT/Reps/PkT contracts and original Inputs are retained; the choice order is explicit.",
"The positive complexification carries exactly the original integral lattice, with finite integer generators and coefficient integrality rather than an assumed surjection O onto O_K.",
"Only the required central action is constructed; class-sum extension proves its laws and its exact rational restriction.",
"The algebraic smooth representation is the union of finite-level fixed spaces; original admissibility and unitarity inputs are used in their original scope.",
"Orthogonal projection uses finite fixed-vector spaces and a finite compact orbit span, so it does not incorrectly assume Hilbert completion of the smooth representation.",
"Irreducibles are obtained by minimizing the fixed-space dimension and induction; their finite type catalogue depends on the actual chosen levels.",
"The original function model and finite-type convention are recovered from a nonzero coefficient functional, with disjoint inequivalent isotypes.",
"The original level and character projectors preserve isotypic pieces; the finite catalogue covers both original levels simultaneously.",
"The direct and conjugate type conventions are distinguished and the bases are chosen within their actual isotypic subspaces.",
"The compact definite coefficient representation, perfect pairing and tensor dimension use the original Hermitian data; the finite-dimensional algebra argument is supplied.",
"Both directions of TopMultH use the actual definite row form and coefficient pairing, with the original regularity, growth and cusp predicates checked.",
"The compact Schur calculation preserves mass-one compact integration, stabilizer factors and the coefficient dimension; no Haar scale is changed.",
"The row and lift Gram identities keep their exact n_b and d_X constants; actual rational spans are identified before the Hilbert models are selected.",
"The finite Hilbert models and Riesz adjoints give each transition map, including valid, endpoint and unused indices.",
"Both full ChT records retain the same representative catalogue and exact coordinate readings.",
"The lift integral carrier is identified with the original good integral forms through the inherited exact lattice argument, without replacing it by a commensurable lattice.",
"The target map has the required square-root n_0 scale and exact range; its normalization agrees with the original divided pairing.",
"The source maps are prescribed and the theta field is conditional on the source's existing extension witness; a linear left inverse does not assert new extension existence.",
"Every LfT field, including unused tuples, out-of-range indices, type intersections and exact reading, follows on the same maps.",
"The full RrT and all-place basis maps are inherited on the actual three-stage data; Dall precedes the good cut and only delp<=1 is asserted.",
"The complete exists_pkT contract is assembled under the original Inputs/Holds/laws restrictions with literal mL.",
"The Hd constructor uses local standard frames and their exact conjugation, not an unjustified globally free integral lattice.",
"The ten Mat1.Laws and the restricted/all-tuples coordinate identities are checked, including central-only multiplicativity.",
"The period equivalences are actual pullback/descent maps with the original disjoint local place sets and frame character law; no period nonvanishing is invented.",
"The permitted auxiliary stand-in fields are explicit and later replaced by the packet; the prescribed weight integrality, tuple choices and Sha dictionary remain exact.",
"One numerical record is fixed before every eta and later V/S/N/G; the conditional period scalar and canonical local indices are independent of later rational models.",
"The full RowPk record includes both universal KapDef and NumOK fields and retains the supplied realization.",
"The copied realization retains the same finite group through its specified place-label isomorphism, original Pins/Holds and conditional CoreP.",
"All compared spaces, metrics, measures, maps and etaOf are identical under copying; no new orthonormal bases are selected.",
"The full exists_moved endpoint supplies Copy and Coh for every fitting later stage; full ReadL still retains the original o.eta=q.eta guard."
],
"coefficient_normalization":[
"One finite-field minimal polynomial works for all equal-cardinality point fields and the original residue maps.",
"The actual monic quotient O' is proved finite free, complete, local and a DVR, with uniformizer and residue field verified.",
"The actual tensor ring and adjoining one formal variable satisfy the original IsCO requirements and precise residue conditions.",
"Finite module presentations justify coefficientwise series and tensor identities; completeness and exactness are established at the finite modules used.",
"The two nested power-series presentations, actual Unit variable, delta ideals and ordered splitting algebra commute through explicit coefficient maps.",
"The splitting and Taylor-Wiles tensor modules are finite over the actual source rings, including the possibly repeated residual roots.",
"All residual characters, Pair fields, adaptedness and adic generation survive on the same groups and local indices.",
"The base module is the exact tensor extension, remains free over the weight ring, and its support is compared prime by prime with the extension of the same J.",
"Every original auxiliary module retains its level, exponent array, rank and exact additive/scalar presentation.",
"Both comparison maps and every ordered q1/q2 annihilator relation tensor correctly, with the same fEl and exponent.",
"The complete all-level Unit-parameter TWAut uses the identical group packet and its original exponents, ranks and root lifts.",
"A point is lifted to the same K[[t]] with the prescribed prime on the coefficient tensor ring; the new O'-action is onto K.",
"The underlying NP/Kap/eigenvalues and B1/B2 quantifiers and witnesses are literally preserved.",
"Faithful flatness, going down and integrality/going up produce a whole finite chain with exact contractions and orientations.",
"Finite generation of the prime ideal identifies its formal-series quotient and proves primality and exact contraction.",
"Full polynomial-law Cayley-Hamilton generators commute with arbitrary extension through finite-support generic substitution, without factorial inversion.",
"Finite-free coordinates commute with all closed relation intersections; cofinal maximal-ideal powers use N and cN with the same open normal subgroup.",
"Coefficient extraction at depth N+r and a fixed finite group support prove the actual series closed-ideal equality; no infinite-support group-algebra element is introduced.",
"The literal augmentation generators, including star and inertia, match the exact coefficient image; only the actual finite unramified normalization is claimed.",
"The exact pinned complemented-left-ideal definition of semisimplicity is used; a scalar functional retracts complements without a finite-dimensional premise.",
"The original existential NonSS witness is transported through a common overfield and the correctly oriented quotient surjection.",
"The same two group tuples give the discriminant equivalence; the alternative NonSS predicate is transported in the needed direction.",
"Full Core=>CoreBC is proved for arbitrary equal-cardinality finite chains, with lifted point choices made within the permitted universal quantifier order.",
"The restricted h=0,a=n,g=0 consumer needs only restricted normalized Core; it does not smuggle in the full arbitrary-chain theorem.",
"Full and selected compositions with the inherited pro-ell descent retain original B,J,K,f and Selmer quantifiers, while preserving arithmetic TWAut as an upstream input."
]}
cache={}
for comp,notes in findings.items():
    root=a.components/comp
    d=read(root/"provenance.json")
    cclose=read(root/"closure.json")
    raw=(root/"main.tex").read_bytes()
    lines=raw.splitlines(keepends=True)
    assert d["source_commit"]==pin
    assert d.get("main_sha256",d.get("main_tex_sha256"))==sha(raw)
    assert cclose["provenance_sha256"]==sha((root/"provenance.json").read_bytes())
    assert cclose["main_sha256"]==sha(raw)
    assert len(notes)==len(d["claims"])
    ids={c["id"] for c in d["claims"]}
    ranges=set();files=set();per=[];refs=0
    for c,note in zip(d["claims"],notes):
        loc=c["proof_location"]
        block=b"".join(lines[loc["line_start"]-1:loc["line_end"]])
        assert sha(block)==loc.get("range_sha256",loc["sha256"])
        assert b"% BEGIN "+c["id"].encode() in block and b"% END "+c["id"].encode() in block
        assert all(k in old or k in ids for k in c["depends_on"]),(comp,c["id"],c["depends_on"])
        for s in c["sources"]:
            path=s["path"]
            if path not in cache:
                b=(a.source/path).read_bytes()
                assert b==subprocess.check_output(["git","show",pin+":"+path],cwd=a.source)
                cache[path]=b
            b=cache[path]
            assert sha(b)==s.get("file_sha256",s["sha256"])
            rb=b"".join(b.splitlines(keepends=True)[s["line_start"]-1:s["line_end"]])
            assert sha(rb)==s["range_sha256"],(comp,c["id"],path)
            ranges.add((path,s["line_start"],s["line_end"],s["range_sha256"]))
            files.add(path);refs+=1
        per.append(dict(id=c["id"],status="PASS",title=c["title"],finding=note,
            proof_location=loc,source_reference_count=len(c["sources"]),depends_on_checked=c["depends_on"]))
    bound=0
    for x in d.get("inherited_proof_inputs",[]):
        assert sha((a.baseline/x["file"]).read_bytes())==x["sha256"]
    for x in d.get("inherited_proof_blocks",[]):
        b=(a.baseline/x["file"]).read_bytes()
        rb=b"".join(b.splitlines(keepends=True)[x["line_start"]-1:x["line_end"]])
        assert sha(rb)==x["range_sha256"];bound+=1
    for x in d.get("baseline_dependencies",[]):
        b=(a.baseline/x["file"]).read_bytes()
        assert sha(b)==x["sha256"]
        for y in x["claims"]:
            rb=b"".join(b.splitlines(keepends=True)[y["line_start"]-1:y["line_end"]])
            assert sha(rb)==y["range_sha256"];bound+=1
    for x in d.get("external_definition_inputs",[]):
        b=(root/x["local_copy"]).read_bytes()
        assert sha(b)==x["sha256"]
        rb=b"".join(b.splitlines(keepends=True)[x["line_start"]-1:x["line_end"]])
        assert sha(rb)==x["range_sha256"]
        assert sha((a.source/x["source_manifest_file"]).read_bytes())==x["source_manifest_sha256"]
        manifest=read(a.source/x["source_manifest_file"])
        assert any(z.get("rev")==x["commit"] for z in manifest["packages"])
    report=dict(schema="rh-independent-component-review/1",artifact_version="0.40",
        component=comp,reviewer="/root",status="PASS",
        verdict="PASS — independently read all mathematical claims, checked exact source contracts and quantified scope, and bound review to final bytes.",
        source_commit=pin,proof_file=comp+"/main.tex",proof_file_sha256=sha(raw),main_tex_sha256=sha(raw),
        provenance_file_sha256=sha((root/"provenance.json").read_bytes()),
        closure_file_sha256=sha((root/"closure.json").read_bytes()),
        published_applications_file_sha256=sha((root/"published_applications.json").read_bytes()),
        claims_reviewed=[c["id"] for c in d["claims"]],per_claim_review=per,
        source_checks=dict(files=len(files),distinct_ranges=len(ranges),claim_source_references=refs,
            all_equal_to_pinned_git_blobs=True,bound_inherited_blocks=bound),
        corrections_required=[],outstanding_findings=[],
        scope_limit="Completion is only at the stated original interfaces. No complete RH/Dirichlet-GRH proof or whole compound selected-leaf closure is inferred.",
        not_performed="No Lean build or kernel replay.")
    (HERE/(comp+"_review.json")).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    out=[f"Independent review: {comp}",report["verdict"],f"Main SHA256 {sha(raw)}",
        f"Provenance SHA256 {report['provenance_file_sha256']}",f"Closure SHA256 {report['closure_file_sha256']}",""]
    out.extend(f'{r["id"]}: PASS — {r["finding"]}' for r in per)
    out+=["",f"Pinned sources: {len(files)} files, {len(ranges)} distinct ranges, {refs} references.",
        f"Inherited proof blocks verified: {bound}.","No outstanding correction. No Lean replay."]
    (HERE/(comp+"_review.txt")).write_text("\n".join(out)+"\n")
    print(comp,len(per),"claims: PASS;",len(files),"source files;",len(ranges),"ranges")
