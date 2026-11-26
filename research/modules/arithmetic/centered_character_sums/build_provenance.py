#!/usr/bin/env python3
"""Build CC provenance from pinned Git blobs; no source checkout mutation."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--repo", type=Path, default=ROOT.parents[1] / "lean-source")
args = ap.parse_args()
REPO = args.repo.resolve()
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
assert subprocess.check_output(["git","-C",str(REPO),"rev-parse","HEAD"],text=True).strip()==COMMIT
MS = "src/Development/AutomorphicArithmetic/MeanSquareBounds/"
PI = "src/Formalism/PeriodIntegrals/"
GL = "src/Formalism/GL3MeanSquares/"
ZF = "src/Formalism/LandauZeroFreeBounds/"
GI = "src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/"
P = {
 "def": MS+"PrimeSetTwoBounds.lean",
 "psi": MS+"PsiThin.lean",
 "int": MS+"IntThin.lean",
 "gint": MS+"GIntegral.lean",
 "thin": MS+"Thin.lean",
 "host": MS+"GaussSumFunctionEq.lean",
 "real": MS+"realCond.lean",
 "small": MS+"SmallZeros.lean",
 "ef": PI+"ExplicitFormula.lean",
 "closed": PI+"ExplicitFormulaCounts/ExplicitFormula.lean",
 "analytic": PI+"ExplicitFormulaCounts/AnalyticInputs.lean",
 "zw": PI+"OrbitalBoundsConclusion/ZerosWindow.lean",
 "efof": PI+"OrbitalBoundsConclusion/ExplicitFormula.lean",
 "zfr": ZF+"NoZeroComplex.lean",
 "growth": ZF+"ExceptionalZeroBounds/LGrowth.lean",
 "right": ZF+"ExceptionalZeroBounds/LRight.lean",
 "rem": GL+"HookFormulaTorsion/SmoothedRemainderRealIntegralFormula.lean",
 "constant": GL+"HookFormulaTorsion/PsiZeroIntegral.lean",
 "remdef": GL+"SmoothedRemainderRealIntegralFormula.lean",
 "pairgood": "src/Development/AutomorphicArithmetic/CharacterBoxes/PairGood.lean",
 "pair": MS+"pairEx.lean",
 "pair_exists": MS+"PairExists.lean",
 "pair_share": MS+"PairShare.lean",
 "msq": MS+"meanSqK.lean",
 "primesrel": GI+"PrimesInProgressionsRelativeError.lean",
}
cache = {}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(path):
    if path not in cache:
        raw = subprocess.check_output(["git", "-C", str(REPO), "show", COMMIT + ":" + path])
        if (REPO / path).is_file():
            assert (REPO / path).read_bytes() == raw, ("modified checkout", path)
        cache[path] = raw
    return cache[path]


PREFIX = r"^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
BOUNDARY = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option|attribute|include|omit)\b|^@\[[^\n]*\]")


def namespace_at(lines, index):
    stack = []
    for line in lines[:index]:
        m = re.match(r"^namespace\s+(\S+)", line)
        if m:
            stack.append(("namespace", m.group(1)))
        elif re.match(r"^(?:noncomputable\s+)?section(?:\s|$)", line):
            stack.append(("section", None))
        elif re.match(r"^end(?:\s|$)", line) and stack:
            stack.pop()
    return ".".join(value for kind, value in stack if kind == "namespace")


def source(key, spelling, role="literal conclusion or substantive supplier", namespace=None):
    path = P.get(key, key)
    raw = blob(path)
    lines = raw.splitlines(keepends=True)
    texts = [line.decode().rstrip("\r\n") for line in lines]
    pat = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure)\s+" + re.escape(spelling) + r"(?=\s|\{|\(|:|$)")
    hits = [i for i, line in enumerate(texts) if pat.match(line)]
    if not hits:
        # A source may spell a theorem with its explicit namespace prefix.
        decl = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure)\s+([^\s({:]+)")
        suffix = []
        for i, line in enumerate(texts):
            m = decl.match(line)
            if m and m.group(1).endswith("." + spelling):
                suffix.append((i, m.group(1)))
        if len(suffix) == 1:
            hits = [suffix[0][0]]
            spelling = suffix[0][1]
    if namespace is not None:
        hits = [i for i in hits if namespace_at(texts, i) == namespace]
    assert len(hits) == 1, (path, spelling, hits, namespace)
    start = hits[0]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(texts[end]):
        end += 1
    while end > start + 1 and not texts[end - 1].strip():
        end -= 1
    part = b"".join(lines[start:end])
    ns = namespace_at(texts, start)
    full_name = spelling[7:] if spelling.startswith("_root_.") else ((ns + ".") if ns else "") + spelling
    url = f"{URL}/blob/{COMMIT}/{path}#L{start + 1}-L{end}"
    return {
        "path": path, "declaration": full_name, "source_spelling": spelling,
        "line_start": start + 1, "line_end": end,
        "sha256": sha(raw), "full_file_sha256": sha(raw),
        "range_sha256": sha(part), "range_bytes": len(part),
        "first_line": texts[start], "declaration_lines_within_range": [start + 1],
        "url": url, "pinned_url": url, "role": role,
        "verified_equal_to_pinned_git_blob": True,
    }


def many(key, names, role="literal conclusion or substantive supplier"):
    return [source(key, name, role) for name in names]


def interface_range(key, spelling, start, end, role):
    """An explicitly delimited field interface, not a declaration proof range."""
    path = P[key]
    raw = blob(path)
    lines = raw.splitlines(keepends=True)
    assert 1 <= start <= end <= len(lines)
    part = b"".join(lines[start-1:end])
    url = f"{URL}/blob/{COMMIT}/{path}#L{start}-L{end}"
    return {
        "path": path, "declaration": spelling, "source_spelling": spelling,
        "line_start": start, "line_end": end,
        "sha256": sha(raw), "full_file_sha256": sha(raw),
        "range_sha256": sha(part), "range_bytes": len(part),
        "first_line": lines[start-1].decode().rstrip("\r\n"),
        "declaration_lines_within_range": [],
        "url": url, "pinned_url": url, "role": role,
        "range_kind": "literal record-field interface",
        "verified_equal_to_pinned_git_blob": True,
    }



main=(ROOT/"main.tex").read_bytes(); report=(ROOT/"report.txt").read_bytes(); tex=main.decode()
assert not [c for c in tex if ord(c)<32 and c not in "\n\r\t"]
markers=list(re.finditer(r"(?m)^\\paragraph\{(CC\d+):",tex))
assert [m[1]for m in markers]==[f"CC{i}"for i in range(1,21)]
paragraphs={}
for i,m in enumerate(markers):
 end=markers[i+1].start()if i+1<len(markers)else len(tex)
 part=tex[m.start():end].encode()
 paragraphs[m[1]]=dict(sha256=sha(part),bytes=len(part),line_start=tex[:m.start()].count("\n")+1,line_end=tex[:end].count("\n"))
claims=[]
def claim(i,title,statement,deps,sources,assumptions):
 cid=f"CC{i}"
 claims.append(dict(id=cid,title=title,statement=statement,status="derived_simplification",
 mathematical_status="proved_under_explicit_hypotheses",introduced_in="0.21",depends_on=deps,
 assumptions=assumptions,proof_location=dict(file="centered_character_sums/main.tex",
 expanded="centered_character_sums/report.txt",section=cid,**paragraphs[cid]),sources=sources))
BASE=["Usual finite Dirichlet characters with zero extension at nonunits; complex analytic continuation and zeros count analytic multiplicity."]
PRIM=BASE+["N>=1, chi primitive modulo N; the primitive principal case has N=1."]
EXC=["Fixed c0>0; if chi is real nonprincipal, L(chi,beta) is nonzero for 1-c0<beta<1."]
STD=["Basic real and complex analysis: Gaussian Fourier transform, Fourier inversion for Schwartz functions, Mellin integration, Jensen formula, residue theorem and dominated convergence, proved or used with explicit domains in the text."]
claim(1,"Primitive functional equation from Gauss sums and Poisson",
 "Prove the primitive completion and functional equation with tau(chi)/(i^a sqrt(N)), including the separate zeta poles; no RH or zero-free region is assumed.",
 [],many("psi",["pt_zero_symm"],"source use of the primitive functional equation; CC supplies its analytic derivation"),
 PRIM+STD)
claim(2,"Uniform growth and Euler-product estimates",
 "F=(s-1)^delta L has polynomial growth on -2<=Re(s)<=6, a fixed lower bound at 2+it, Euler logarithmic derivative and no zeros in Re(s)>1.",
 [],many("growth",["character_sum_range_modulus_eq_zero","character_sum_range_add_modulus","norm_character_sum_range_le","norm_character_sum_Icc_le","lfunction_polynomial_growth"])+many("right",["inverseBound","negLD_eq_LSeries_mul_vonMangoldt","l_log_deriv_right"])+many("analytic",["chk_zetaBoundRight","chk_lInvRight","chk_lBoundRight"]),
 BASE+["Periodic character sums, four periodic primitives and absolutely convergent Euler products."])
claim(3,"Local zero windows and finite logarithmic derivatives",
 "Jensen and the finite Blaschke lemma give O(log(N(|t|+2))) unit-height critical-zero counts and uniform local logarithmic derivative expansions.",
 ["CC2","QR15"],many("zw",["zerosWindow_of"])+many("closed",["zerosWindow_closed"])+many("zfr",["localZeros"]),
 BASE+STD)
claim(4,"Boundary nonvanishing and the zero at the origin",
 "Exclude the line Re(s)=1, principal real zeros in (0,1), and identify the only possible zero in -1/2<=Re(s)<=0 for primitive chi: a simple zero at 0 for nonprincipal even chi.",
 ["CC1","CC2","QW14"],many("psi",["pt_zero_symm"])+many("zfr",["zFRDirichlet"]),
 PRIM+["For nonprincipal nonvanishing at one: QW14."])
claim(5,"Uniform zero-free region with the exact real exception",
 "The Dirichlet zero-free strip has at most one real simple exceptional zero for a real nonprincipal character at a fixed modulus. Under NoExc(c0), every nontrivial zero satisfies beta<=1-c/(lambda+log(|gamma|+3)).",
 ["CC2","CC3","CC4","QR17","QR18"],many("zfr",["localZeros","noZeroComplex","realLargeT","realSmallT","twoReal","zFRDirichlet"])+many("psi",["pt_zero_free"])+many("def",["NoExc"]),
 BASE+EXC+["The first assertion does not assume NoExc; the final bound does. lambda>=max(1,log N)."])
claim(6,"Primitive reflection bounds reciprocal denominators",
 "Invert a primitive character and reflect rho to 1-rho. Under the same NoExc hypothesis, low zeros have Re(rho)>=c/(3lambda).",
 ["CC1","CC4","CC5"],many("psi",["pt_factorsThrough_inv","pt_isPrimitive_inv","pt_zero_symm"]),
 PRIM+EXC+["lambda>=max(1,log N); low means |Im(rho)|<=2."])
claim(7,"Sum all reciprocal zero weights",
 "The complete multiplicity-weighted sum below T is <=C2(lambda+log T)^2 for T>=1, with C2 depending only on c0.",
 ["CC3","CC4","CC6"],many("psi",["pt_zero_sum"])+many("ef",["ZerosBelow"]),
 PRIM+EXC+["lambda>=max(1,log N)."])
claim(8,"The exact uniform explicit formula and its zero residue",
 "Prove ExplicitFormulaWith using full floor endpoints, separately chosen good heights, the left-line functional equation, and the actual zero-at-origin residue; retain the low-zero reciprocal sum.",
 ["CC1","CC2","CC3","CC4","QR20"],many("ef",["psi0","ZerosBelow","ExplicitFormulaWith","ExplicitFormula"])+many("efof",["explicitFormula_of"])+many("closed",["explicitFormula_closed"]),
 PRIM+STD+["2<=T<=u. No real-zero exclusion is needed in this formula."])
claim(9,"The conductor-sensitive height choice",
 "Choose T=exp(sqrt(log u)) and bound every explicit-formula term to obtain the actual psi0 estimate with exponent -c log u/(lambda+sqrt(log u)).",
 ["CC5","CC7","CC8"],many("psi",["pt_rpow_le","pt_core"]),
 PRIM+EXC+["u>=e; lambda>=max(1,log N)."])
claim(10,"Supply the literal primitive psi_thin theorem",
 "For each c0>0, choose C,c>0 before N,chi,lambda,u and obtain |psi0|<=Cu(log u+lambda)^2 exp(-c log u/(lambda+sqrt(log u))) under the source NoExc condition.",
 ["CC5","CC6","CC7","CC8","CC9"],many("psi",["psi_thin"])+many("def",["NoExc"]),
 PRIM+EXC+["u>=e; lambda>=max(1,log N)."])
claim(11,"Fixed-character integrability without a uniform Siegel input",
 "For a fixed character, psi0=O(u/log^2 u), including imprimitive Euler-factor deletion; psi0/u^2 is absolutely integrable from 1 to infinity.",
 ["CC10","QW15"],many("gint",["psi0_bound","psi_zero_div_sq_integrable"])+many("constant",["rem_measurable","core_integrable","core_tendsto"]),
 BASE+["A fixed modulus; QW15 supplies a fixed finite real-zero margin. No uniform conductor-dependent Siegel estimate is asserted."])
claim(12,"The nonprincipal logarithmic-derivative centering",
 "Prove convergence of sum Lambda(n)chi(n)/n to -L'(1)/L(1) and derive the exact tail integral for the nonprincipal centered ramp sum, with full floor endpoints.",
 ["CC11","QW14"],many("constant",["logDerivSeries_main","log_deriv_series"])+many("rem",["integral_partial_sum_div_sq","smoothedRemainderIntegralFormula"])+many("gint",["gChi_ne","series_aChi"]),
 BASE+["chi nonprincipal; y>=1. The series is convergent, not asserted absolutely convergent."])
claim(13,"The exact principal constant",
 "Compute integral_1^infinity (psi(u)-u)/u^2=-1-gamma and derive the exact principal centered ramp sum tail integral.",
 ["CC11"],many("constant",["zeta_logderiv_limit","psiZeroConst_main","psi_zero_integral_constant"])+many("rem",["integral_psumR_sub_div_sq_eq_partial_sums","smoothedRemainderRealIntegralFormula"])+many("gint",["gChi_one"]),
 ["Primitive principal character N=1; Euler's constant with its usual harmonic-sum definition; y>=1."])
claim(14,"Match G0, An.gChi and g_integral literally",
 "For every primitive chi and y>=1, G0=-y integral_y^infinity psi0/u^2; identify An.gChi by removing max on its original finite support and checking both exact centerings.",
 ["CC12","CC13"],many("def",["G0"])+many("gint",["one_apply_of_primitive","l21a","g_integral"])+many("host",["gauss_sum_function_eq"]),
 PRIM+["y>=1."])
claim(15,"Uniform exponential-cutoff tail integration",
 "With lambda<=A x^(eps/5) log^2 x and y>=exp(x^(eps/3))/3, integrate the psi_thin majorant uniformly to get y exp(-c' x^(eps/8)) for any prescribed c'>0.",
 [],many("int",["thin_intH","thin_ptw","thin_integral","int_thin"]),
 ["eps,c,C,A,c'>0 fixed; lambda>=1; actual integrands are measurable. The source's unused nonintegrable totalized-integral case gives zero."])
claim(16,"Supply the exact QH.thin endpoint",
 "For fixed eps,A,c',c0>0, one threshold gives |G0(chi,y)|<=y exp(-c' x^(eps/8)) for all primitive conductor-bounded chi with NoExc, and all y above the exponential cutoff.",
 ["CC10","CC14","CC15"],many("thin",["thin"])+many("def",["G0","NoExc"]),
 PRIM+EXC+["log N<=A x^(eps/5)log^2 x; y>=exp(x^(eps/3))/3; x sufficiently large uniformly in N,chi,y."])
claim(17,"The actual quadratic conductor exponent restriction",
 "A primitive square-one character has odd conductor exponents at most 1 and its exponent at 2 at most 3. Under the source prime-support hypotheses N divides Mqd, and if q,d do not divide N then N divides M.",
 [],many("real",["conductor_le_of_quadratic_squares","real_cond_odd","real_cond_two","real_cond"]),
 PRIM+["chi^2=1; 8 divides M; q,d primes; every prime dividing N divides M or equals q or d."])
claim(18,"The exact bounded-modulus small_zeros theorem",
 "For every fixed B0, all nonprincipal characters modulo N<=B0 have one common positive real-zero exclusion interval; no reality or primitivity restriction is needed.",
 ["QW14"],many("small",["noExc_mono","noExc_one","noExc_level","small_zeros"])+many("def",["NoExc"]),
 ["N>=1; B0 a fixed nonnegative integer; continuity and nonvanishing at one."])
claim(19,"Install ThinH for the same actual host",
 "For supplied HostRaw with bounded odd part of QS and bounded log condN, RealBox implies its actual ChebyshevCharacterBound uniformly. The ThinH outer constant is 1.",
 ["CC14","CC16","CC17","CC18"],many("host",["isReal_of_sq","level_dvd","thinH"])+many("pairgood",["RealBox","ThinH"]),
 ["Actual HostRaw H; q,d primes and condN=QS*q*d; eps>0 and source eps<1/52; oddPart(QS)<=B; log condN<=2 x^(eps/5)log^2 x; supplied RealBox. No assertion of existence of RealBox hosts."])
claim(20,"An additional uniform derivative and increment bound",
 "Above the same exponential cutoff, for every b>0 the actual centered function is locally absolutely continuous and |G0(y2)-G0(y1)|<=(y2-y1) exp(-b x^(eps/8)) uniformly under CC16 assumptions.",
 ["CC10","CC14","CC15","CC16"],
 many("gint",["g_integral"],"source exact integral identity used for a further human consequence")+
 many("remdef",["SmoothedRemainderHasDerivBound","SmoothedRemainderRealHasDerivBound"],"related source derivative interfaces, not claimed to be identical to CC20"),
 PRIM+EXC+["CC16 conductor bound; exp(x^(eps/3))/3<=y1<=y2; threshold may depend on b. This does not prove the different polynomial-window square-root estimates."])
completed=[]
def done(k,n,ids,conditions,scope="Literal conditional endpoint reconstructed"):
 completed.append(dict(endpoint=n,claim_ids=ids,status="completed_conditionally",scope=scope,conditions=conditions,source=source(k,n)))
done("closed","zerosWindow_closed",["CC2","CC3"],BASE)
done("closed","explicitFormula_closed",["CC1","CC2","CC3","CC4","CC8"],PRIM+["2<=T<=u in ExplicitFormulaWith"])
done("zfr","zFRDirichlet",["CC2","CC3","CC4","CC5"],BASE)
done("psi","pt_zero_symm",["CC1","CC6"],PRIM+["A zero strictly in the critical strip."])
done("psi","pt_zero_free",["CC5"],PRIM+EXC)
done("psi","psi_thin",["CC1","CC2","CC3","CC4","CC5","CC6","CC7","CC8","CC9","CC10"],PRIM+EXC)
done("constant","log_deriv_series",["CC11","CC12"],BASE+["chi nonprincipal"])
done("constant","psi_zero_integral_constant",["CC11","CC13"],["Primitive principal character"])
done("gint","g_integral",["CC11","CC12","CC13","CC14"],PRIM+["y>=1"])
done("int","int_thin",["CC15"],["All original positive-parameter, cutoff, lambda and pointwise-majorant hypotheses."])
done("thin","thin",["CC10","CC14","CC15","CC16"],PRIM+EXC+["Original positive parameters, conductor bound and exponential y cutoff."])
done("real","real_cond",["CC17"],PRIM+["Square-one and exact original prime-support hypotheses."])
done("small","small_zeros",["CC18"],["Fixed bound B0; all nonprincipal characters modulo N<=B0."])
done("host","thinH",["CC14","CC16","CC17","CC18","CC19"],["Supplied HostRaw and RealBox, exact odd-part/log-conductor bounds, 0<eps<1/52."])
targets=[
 dict(id="CC-next-01",title="Actual simultaneous PairEx and its mean-square/density suppliers",
 scope="Construct the source's actual q,d pair with both square-root centered-window estimates and all twisted real zero boxes. CC supplies only ThinH conditional on RealBox, above the much later exponential cutoff. It does not supply Jacobi-twist mean squares or exceptional-character density at polynomial-window heights.",
 sources=many("pairgood",["PairGood","PairEx"])+many("pair",["pairEx"])+many("pair_exists",["pair_exists"])+many("pair_share",["pair_share"])+many("msq",["meanSqK"])+many("remdef",["ZeroDensityBound","ExceptionalCharacterCountBound","JacobiTwistedMeanSquareBound"])),
 dict(id="CC-next-02",title="Relative prime progression estimate with its exceptional main term",
 scope="Reconstruct the actual PrimesRel theorem, including the conductor-uniform unique exceptional character and the relative main-term error at polynomial thresholds. CC's zero-free strip and thin bound do not imply this stronger Linnik-type relative estimate.",
 sources=many("primesrel",["primesRel_holds"])),
 dict(id="CC-next-03",title="Same-object host boxes and the remaining global centered-window join",
 scope="Keep RealBox as a premise of the proved ThinH implication. Supply that condition on the actual selected host through PairEx and retain the independent cohomological and gain-to-prime-sum/final-parameter branches. CC20 only adds a derivative consequence above the exponential cutoff.",
 sources=many("pairgood",["RealBox","PairGood"]),
 discharged_subscope=["QH.thin and ThinH under their original zero-exclusion/RealBox hypotheses","Exact centering and integral identity, including the principal -1-gamma","Uniform later-cutoff derivative consequence"])
]
all_sources=[s for c in claims for s in c["sources"]]
ids={c["id"]for c in claims}
graph={c["id"]:[d for d in c["depends_on"]if d in ids]for c in claims}
active=set();visited=set()
def visit(cid):
 assert cid not in active,("cycle",cid)
 if cid in visited:return
 active.add(cid)
 for d in graph[cid]:visit(d)
 active.remove(cid);visited.add(cid)
for cid in graph:visit(cid)
reviews=[]
for filename,expected in [
 ("centered_character_sums_analytic_review.json",[f"CC{i}"for i in range(1,9)]),
 ("centered_character_sums_tail_review.json",[f"CC{i}"for i in range(9,21)])]:
 f=ROOT.parent/"reviews_v0_21"/filename
 if f.exists():
  raw=f.read_bytes(); txt=raw.decode()
  bound=[cid for cid,p in paragraphs.items()if p["sha256"]in txt]
  assert set(expected)<=set(bound),("stale or incomplete independent review",filename,set(expected)-set(bound))
  reviews.append(dict(file="reviews_v0_21/"+filename,sha256=sha(raw),expected_claim_ids=expected,bound_current_claim_ids=bound))
scope="Actual primitive Dirichlet functional equation, zero windows, zero-free region and explicit formula; exact centered integrals; uniform QH.thin and same-host ThinH conditional on RealBox. PairEx, relative prime progression errors and independent global windows remain."
provenance=dict(component="centered_character_sums",version="0.21",claim_prefix="CC",source_commit=COMMIT,repository=URL,scope=scope,
 main_sha256=sha(main),report_sha256=sha(report),builder_sha256=sha(Path(__file__).read_bytes()),
 claims=claims,completed_source_endpoints=completed,remaining_targets=targets,independent_reviews=reviews,
 external_primary_sources=[dict(url="https://dlmf.nist.gov/25.15",role="Normalization cross-check for the primitive completion; not a substitute for the supplied Poisson-Mellin proof.")],
 derived_additional_implications=[dict(claim_id="CC20",statement=claims[-1]["statement"],status="proved_conditionally",not_claimed="Polynomial-window square-root estimates or arbitrary-conductor real-zero exclusion.")],
 counts=dict(claims=len(claims),claim_source_links=len(all_sources),distinct_claim_ranges=len({(s["path"],s["line_start"],s["line_end"],s["range_sha256"])for s in all_sources}),indexed_source_files=len(cache),completed_source_endpoints=len(completed),remaining_supplier_families=len(targets)),
 verification=dict(git_objects_only=True,source_checkout_unchanged=True,old_components_unchanged=True,lean_compiled=False,pdf_generated=False,hypothesis_policy="Real-zero exclusion and actual host RealBox are retained; no RH, GRH, uniform Siegel bound, PairEx or relative progression result is assumed proved."))
manifest=dict(component="centered_character_sums",version="0.21",commit=COMMIT,repository=URL,source_files=[
 dict(path=p,sha256=sha(raw),bytes=len(raw),line_count=len(raw.splitlines()),verified_equal_to_pinned_git_blob=True,url=f"{URL}/blob/{COMMIT}/{p}")for p,raw in sorted(cache.items())])
for name,obj in [
 ("provenance.json",provenance),("source_manifest.json",manifest),
 ("next_targets.json",dict(component="centered_character_sums",version="0.21",commit=COMMIT,scope=scope,completed_endpoints=completed,next_targets=targets))]:
 (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
lines=["CENTERED CHARACTER SUMS -- CC1--CC20","Pinned commit: "+COMMIT,"Inclusive declaration ranges are exact pinned bytes.",""]
for c in claims:
 lines += [c["id"]+" "+c["title"],"TeX paragraph SHA-256: "+paragraphs[c["id"]]["sha256"]]
 for s in c["sources"]:lines += ["  "+s["declaration"],"  "+s["pinned_url"],"  file_sha256="+s["sha256"],"  range_sha256="+s["range_sha256"]]
 lines.append("")
(ROOT/"source_locators.txt").write_text("\n".join(lines)+"\n")
print(json.dumps(provenance["counts"],indent=2))
