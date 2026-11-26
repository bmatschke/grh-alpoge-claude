#!/usr/bin/env python3
"""Rebuild PQL provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v038

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
COMPONENT = "proell_descent"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v038")
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"PQL\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written PQL block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


a="src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
p=a+"PatchingModules/"
s=p+"SeparableMatrixStability/"
w=a+"WeilGroupCharacters/"
ca=a+"CommutativeAlgebraHeight/"
anchors={f"PQL{i}":[] for i in range(1,22)}
anchor_rows=[]
def add(ids,path,names):
    for name in names.split(";"):
        entry=source(path,name)
        for key in ids.split():
            assert key in anchors,key
            if entry not in anchors[key]:anchors[key].append(entry)
    anchor_rows.append(ids+"|"+path+"|"+names)
add("PQL1 PQL2 PQL3 PQL4",p+"PairedDualFirstOrderDualMatrixSpace.lean","Glob;Hom;Compat;PL")
add("PQL1 PQL5 PQL15",p+"ThetaCoefficientMapEq.lean","TWGrp;ProL;B1;B2")
add("PQL1 PQL16 PQL20 PQL21",p+"PatchedSupportCompletions.lean","Pt;Adapted;ChainConcl;Core;CoreBC;Raw")
add("PQL2",s+"PlProps.lean","UpperTheory.V.Pa.pl_props")
add("PQL3",s+"PlMap.lean","UpperTheory.V.Pa.pl_map")
add("PQL3 PQL9 PQL12",s+"PlSub.lean","UpperTheory.V.Pa.pl_sub")
add("PQL4",s+"QuotEx.lean","pl_le_ker;UpperTheory.V.Pa.quot_ex")
add("PQL5",s+"TwquotEx.lean","exists_desc;UpperTheory.V.Pa.twquot_ex")
add("PQL5",s+"HomDesc.lean","UpperTheory.V.Pa.hom_desc")
add("PQL5",s+"HomlDesc.lean","UpperTheory.V.Pa.homl_desc")
add("PQL5",s+"SecondSelmerSpanBoundAtAllLevels.lean","TWQuot;grp;proL")
add("PQL6 PQL10",w+"UniversalOrdinaryDeterminantRing.lean","Resid;Dbar;Ip;IsPsi;Pair;Pair.Maps")
add("PQL6",s+"ResidDesc.lean","UpperTheory.V.Pa.resid_desc")
add("PQL6 PQL10 PQL17 PQL18",s+"MapStar.lean","UpperTheory.V.Pa.map_star")
add("PQL7 PQL8 PQL9",w+"RepAlg.lean","Kills@103;CH@110;IsCont;closureIdeal")
add("PQL7",ca+"DChKer.lean","UpperTheory.V.CA.d_ch_ker")
add("PQL7",ca+"DkerOfKills.lean","UpperTheory.V.CA.d_ker")
add("PQL7 PQL10",ca+"DFactor.lean","UpperTheory.V.CA.d_factor")
add("PQL8",ca+"DClosed.lean","UpperTheory.V.CA.d_closed")
add("PQL9",s+"PlChBar.lean","exists_prime_power_pow_eq_one;ch_mem;chi_diag;UpperTheory.V.Pa.pl_chBar")
add("PQL10",s+"GdetDesc.lean","gdesc_ker;UpperTheory.V.Pa.gdet_desc")
add("PQL10",s+"PairDesc.lean","UpperTheory.V.Pa.pair_desc")
add("PQL10 PQL16 PQL17 PQL18",s+"ComapLam.lean","UpperTheory.V.Pa.comap_lam")
add("PQL11",s+"PtUnip.lean","kills_max;UpperTheory.V.Pa.pt_unip")
add("PQL11",s+"UnipOf.lean","cast_zero;key;UpperTheory.V.Pa.unip_of")
add("PQL11",s+"MapEta.lean","NP.UnipOn")
add("PQL12",s+"CocPl.lean","cp_U;cp_pow;UpperTheory.V.Pa.coc_pl")
add("PQL12 PQL13",s+"NpDesc.lean","np_desc_sep;UpperTheory.V.Pa.np_desc")
add("PQL13",s+"SecondSelmerSpanBoundAtAllLevels.lean","sel_iff;bd_iff;NP.desc;Kap.desc")
add("PQL14",s+"SelDesc.lean","UpperTheory.V.Pa.sel_desc_fac;UpperTheory.V.Pa.epM_mul_self_eq_zero;UpperTheory.V.Pa.sel_desc")
add("PQL14",s+"RhoHom.lean","UpperTheory.V.Pa.rho_hom")
add("PQL14",s+"AmFin.lean","UpperTheory.V.Pa.am_fin")
add("PQL15",s+"BDesc.lean","coboundary_first_eq_image_pullback;UpperTheory.V.Pa.b_desc")
add("PQL16",s+"PtDesc.lean","UpperTheory.V.Pa.pt_desc")
add("PQL17",s+"AutDesc.lean","baseDesc;ringDesc;maps_desc;UpperTheory.V.Pa.aut_desc")
add("PQL17",p+"ThetaCoefficientMapEq.lean","TWBase;TWRing;TWMaps;TWAut")
add("PQL18 PQL19",p+"ThetaCoefficientMapEq.lean","pairGens;augmentationIdealKernel;StOrTh")
add("PQL18",s+"NonssDesc.lean","md_ker;md_span;closure_down")
add("PQL19",s+"NonssDesc.lean","nonSS_down;UpperTheory.V.Pa.nonss_desc")
add("PQL19",p+"PairedDualFirstOrderDualMatrixSpace.lean","DiscSt;NonSS")
add("PQL20",s+"RawMain.lean","UpperTheory.V.Pa.raw_main")
add("PQL20",p+"ThetaCoefficientMapEq.lean","pairVals")
add("PQL21",p+"ThetaCoefficientMapEq.lean","Lim")
(HERE/"source_anchors.txt").write_text("\n".join(anchor_rows)+"\n")

titles=[
"The exact original quotient and matched-descent contract",
"The relative pro-ell residual and its finite quotients",
"Surjective residual functoriality and open-subgroup descent",
"Quotient preserving sign, involution, cyclotomic character and every local map",
"All fields of the actual TWQuot and its ProL system",
"Residual characters and unchanged local data descend",
"Three hypothesis-checked Chenevier determinant applications",
"Closedness of the full polynomial-law determinant kernel",
"Pro-ell residual killed in every exact closed Cayley-Hamilton ideal",
"Descent of the full determinant pair over the original ring",
"Actual original point unipotence modulo every power of t",
"Representation and adjoint cocycle descend through the same residual",
"Complete NP and Kap records with the same coefficients and local witnesses",
"Exact truncated SelP, Sel1 and Sel2 descent",
"Original B1 and B2 with unchanged constants and eventual level sets",
"Descended point retains literal f, K and prime kernel",
"Complete TWAut transport retaining all rings, modules, maps and J",
"Exact two-parameter closed augmentation ideals under quotient",
"One-way NonSS descent and two-way discriminant equivalence at original primes",
"Full original CoreBC implies Raw",
"Selected Count-II internal closure and precise residual arithmetic cut"]
deps={
1:[],2:[],3:[2],4:[2],5:[3,4],6:[],
7:[],8:[7],9:[3,7,8],10:[6,7,9],
11:[],12:[3],13:[11,12],14:[11,12,13],
15:[13,14],16:[10,11,13,15],17:[5,6,10],
18:[9,10],19:[18],20:[5,6,10,16,17,19],
21:[20]}
scopes=[
"Original TWGrp, coefficient DVR and IsCO ring, adapted residual pair, same J/TWAut and arbitrary finite chain of Pt; final implication CoreBC to Raw.",
"Any profinite Gamma with open normal H; exact relative PL equals intrinsic pro-ell residual and all finite-quotient equivalences.",
"Continuous surjections with H=f inverse Hprime, plus exact open-normal subgroup passage for ambient PL.",
"Every original Glob and open H satisfying original eta/epsilon guards, for every prime ell.",
"Every original TWGrp T; nonempty TWQuot T with all original fields, unchanged hb/local PhiCond and exact descended ProL.",
"Original quotient morphism and residual characters killed on its kernel; same psib/theta and exact Ip=Iu transport.",
"Original full GDet polynomial laws of any relevant rank, exact CH coefficients, discrete reductions and surjective group-algebra quotient.",
"Any I-adically separated coefficient ring and I-adically continuous full determinant law, exact source closureIdeal.",
"Every Z and every k in original relative PL, all coefficient powers and open normal subgroups; same B and residual determinant.",
"Full original Pair over the same IsCO B, all scalar algebras, polarization, ordinary and inertia clauses.",
"Every original Pt, including when O does not surject onto its finite residue field K; all m and all h in H.",
"Characteristic-ell coefficient ring, original continuous representation/cocycle and unipotence on H; every ideal power, with separation for exact descent.",
"Original NP and arbitrary Kap, same K/A/t/a/psi/w/type/Y and complete membership, independence and generation fields.",
"Original Am m and DD(Am m,g), arbitrary g and original SelP/Sel1/Sel2 on the actual quotient at every level.",
"One original C before m; same eventual N set, same K, same D0; original full B1 and B2 statements.",
"Every original Pt and exact chosen quotient; f is literally the old B-to-K[[t]] map, K unchanged.",
"Every given TWAut at arbitrary parameter type sigma, complete base/rings/maps/annihilator relations; original ideal J and all modules unchanged.",
"Original closed CH+pair generator ideals with every coefficient power and open normal subgroup; preimage inclusion and kernel annihilation.",
"Every original field-valued map B-to-kappa and prime ideal; NonSS forward implication only, DiscSt equivalence.",
"Entire original CoreBC-to-Raw implication for all h, same prime list, J and all original chain hypotheses.",
"Selected h=0,a=n=4,g=0,ell=3 interface; coefficient normalization/Unit and actual limiting patching/S5 remain; compound CountII remains open."]
commonguards=[
"One actual quotient Q from the given T; original local list and PhiCond.",
"Same B, J, determinant law, local characters, field K and point homomorphism f.",
"Full polynomial-law kernel, including all scalar algebras; no n! inversion.",
"Exact Selmer local/polarization conditions; B1/B2 constants precede m and thresholds are preserved.",
"Finite-level TWAut transport is distinct from producing its limiting patched support."]
claims=[]
for i,title in enumerate(titles,1):
    key=f"PQL{i}"
    starts=[j for j,line in enumerate(lines) if line.strip()==f"% BEGIN {key}"]
    ends=[j+1 for j,line in enumerate(lines) if line.strip()==f"% END {key}"]
    assert len(starts)==len(ends)==1 and starts[0]<ends[0] and anchors[key],key
    st,en=starts[0],ends[0];block="".join(lines[st:en]).encode()
    needs=[f"PQL{x}" for x in deps[i]]+(["CRW21"] if i==21 else [])
    claims.append(dict(id=key,title=title,introduced_in="0.39",
        classification="A" if i==7 else "B",
        status="Complete human proof in the exact stated scope",
        proof_status="complete in stated scope",review_status="pending independent mathematical review",
        depends_on=needs,scope=scopes[i-1],quantifier_scope=scopes[i-1],
        hypotheses_retained=commonguards,
        proof_location=dict(file=COMPONENT+"/main.tex",paragraph=key,label="claim:"+key,
            line_start=st+1,line_end=en,bytes=len(block),sha256=sha(block),range_sha256=sha(block),file_sha256=sha(raw)),
        sources=anchors[key]))
url="https://maths.dur.ac.uk/events/Meetings/LMS/2011/GRAF11/papers/chenevier.pdf"
apps=[]
for j,(theorem,statement,checks,claimuses) in enumerate([
 ("Lemma 1.19","Kernel characterization for the full law and factorization through a surjective algebra quotient.",
  ["D is the original multiplicative homogeneous full GDet, not its trace.",
   "Coefficient ring is commutative and the group algebra is associative unital.",
   "Every scalar-extended group-algebra map is surjective; its kernel is generated by killed elements.",
   "No reducedness, field, residual irreducibility or n! invertibility premise."],["PQL7","PQL8","PQL10"]),
 ("Lemma 1.21","The generic coefficient Cayley-Hamilton ideal is contained in the full determinant kernel.",
  ["Original CH is precisely coefficients of characteristic identities for generic finite tuples.",
   "All commutative scalar algebras are retained; rank positive on every actual Pt.",
   "Rank-zero case is the constant-one law, treated directly."],["PQL7","PQL8","PQL9"]),
 ("Lemma 2.33","A continuous discrete-valued determinant on a profinite group kills an open normal subgroup's augmentation ideal.",
  ["The group is the original compact totally disconnected Hausdorff plus subgroup.",
   "The coefficient ring B/I^a has the discrete topology.",
   "Original IsCont makes each characteristic coefficient locally constant modulo I^a.",
   "No finite coefficient-ring or finitely generated group hypothesis is used."],["PQL7","PQL8"])
],1):
    apps.append(dict(id=f"PQL_CHEN_{j}",citation="Chenevier, The p-adic analytic space of pseudocharacters of a profinite group and pseudorepresentations over arbitrary rings",
        theorem=theorem,url=url,source_url=url,classification="A",status="hypotheses checked",
        statement_used=statement,hypotheses_checked=checks,claims=claimuses,
        checked_in="proell_descent/main.tex PQL7; subsequent applications as listed"))
dump("published_applications.json",apps)
standing="The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Statuses refer only to the human reconstruction."
remaining=[
dict(id="PQL_CORE_COEFFICIENT_NORMALIZATION",classification="B",contract="Original Core-to-CoreBC construction: simultaneous coefficient normalization and added Unit parameter, with the same original prime kernels and J after descent."),
dict(id="PQL_LIMITING_PATCHING_AND_S5",classification="C",contract="Original limiting patched ring/maps/modules, S5 support dimension/fiber/annihilator on the actual Lim and original finite-level TWAut."),
dict(id="PQL_ORDINARY_HIDA_HASAUT",classification="C",contract="Original ordinary/control/separating fibers, type/neatU/TThetaEx, four Hida endpoints and all-level same-J HasAut, both original rank-four Links and common coefficient threshold.")]
closed=[
dict(id="PQL_ACTUAL_TWQUOT",claims=[f"PQL{i}" for i in range(1,6)],contract="Actual original TWQuot exists and its grp satisfies ProL with every field."),
dict(id="PQL_FULL_PAIR_DESCENT",claims=[f"PQL{i}" for i in range(6,11)],contract="Original full determinant Pair descends on the same B without residual irreducibility."),
dict(id="PQL_MATCHED_POINT_AND_BOUNDS",claims=[f"PQL{i}" for i in range(11,17)],contract="Exact NP/Kap, truncated Selmer/B1/B2 and Pt descend with same K,f, constants and level thresholds."),
dict(id="PQL_SAME_TWAUT",claims=["PQL17"],contract="Given full TWAut descends on the same rings/modules/maps/J."),
dict(id="PQL_COREBC_TO_RAW",claims=["PQL18","PQL19","PQL20"],contract="Full original CoreBC implies Raw for arbitrary finite chains with exact same point kernels and J.")]
for x in closed:x.update(classification="B",status="closed in exact original scope")
prov=dict(schema="rh-human-component-provenance/1",artifact_version="0.39",date="2026-11-22",
 component=COMPONENT,source_commit=PIN,repository="CocoSgt/riemann-hypothesis-lean",standing_assumption=standing,
 main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 range_convention="Inclusive one-based physical lines, exact original UTF-8 bytes including line endings.",
 claims=claims,claim_total=len(claims),published_applications=apps,
 external_literature=[dict(author="Gaetan Chenevier",url=url,uses=["Lemma 1.19","Lemma 1.21","Lemma 2.33"])],
 source_files=[dict(path=p,sha256=sha(b),file_sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True) for p,(b,ls,_) in sorted(cache.items())],
 metadata_builder=dict(file="build_provenance.py",sha256=sha(Path(__file__).read_bytes()),
 portable_invocation="python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v038"))
dump("provenance.json",prov)
closure=dict(schema="rh-human-component-closure/1",version="0.39",component=COMPONENT,source_commit=PIN,
 standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 provenance_sha256=sha((HERE/"provenance.json").read_bytes()),
 new_claim_ids=[c["id"] for c in claims],closed_contracts=closed,remaining_inputs=remaining,
 same_object_guards=commonguards,selected_top_level_leaf_closed=False,
 not_closed=["Core or CoreBC producers","Limiting patched rings/modules and S5 support",
 "Complete Count-II compound producer","Unconditional RH or Dirichlet GRH human reconstruction"],
 review_status="pending independent mathematical review")
dump("closure.json",closure)
unique={(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
val=dict(status="PASS",source_commit=PIN,main_sha256=sha(raw),claims=len(claims),
 claim_source_references=sum(len(c["sources"]) for c in claims),distinct_source_ranges=len(unique),
 source_files=len(cache),published_applications=len(apps),
 checks=["Fresh prefix","Every source file equals pinned Git blob","Unique declaration anchors",
 "Marked proof blocks hashed","Source ranges and all claim dependencies checked"],
 not_performed="No Lean build or kernel replay; mathematical review and draft TeX recorded separately.")
for c in claims:
    assert all(x in old or x in {a["id"] for a in claims} for x in c["depends_on"])
dump("validation.json",val)
loc=[f"PQL source/proof locators at {PIN}",f"main.tex SHA256 {sha(raw)}",""]
for c in claims:
    q=c["proof_location"];loc.append(f'{c["id"]} | {c["title"]} | proof {q["line_start"]}-{q["line_end"]} SHA256 {q["sha256"]}')
    for x in c["sources"]:loc.append(f'  {x["path"]}:{x["line_start"]}-{x["line_end"]} | {x["declaration"]} | file {x["sha256"]} | range {x["range_sha256"]}')
    loc.append("")
(HERE/"source_locators.txt").write_text("\n".join(loc)+"\n")
(HERE/"report.txt").write_text("""v0.39 — original pro-ell quotient and matched descent, PQL1–PQL21

Complete original TWQuot and full CoreBC-to-Raw implication.
Generic residual facts are proved directly through finite quotients.
The full determinant descends over the original possibly residually
reducible ring B, using exactly checked Chenevier Lemmas 1.19, 1.21
and 2.33. No n! is inverted; the selected ell=3 case is retained.
Actual NP/Kap and point maps descend; K and f:B->K[[t]] are unchanged.
Both B1/B2 retain the original constants before m and identical eventual
level sets. Supplied TWAut transports with the same rings, modules, maps,
annihilator/support data and J. Exact closed augmentation ideals yield
the needed one-way NonSS implication, and discriminant equivalence.
All finite chains of prime kernels are transported, proving the full
source CoreBC=>Raw implication.

Remaining: Core-to-CoreBC coefficient normalization and Unit parameter;
actual limiting patched ring/maps/modules and S5 support; original
ordinary/control/type/Hida/HasAut producers. The selected compound
Count-II obligation remains open. The original Lean proof is assumed
correct; this package records human reconstruction, not a Lean replay.
""")
print(json.dumps(val,indent=2))
