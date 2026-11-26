#!/usr/bin/env python3
"""Build QP provenance from pinned Git blobs; no source checkout mutation."""
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

CB="src/Development/AutomorphicArithmetic/CharacterBoxes/"
JC=GL+"GenusMeanAsymptotics/JacobiCharacterSums/"
P.update({
 "exc":GI+"ExceptionalDirichletZeroUniqueZeroFreeRegion.lean",
 "psirel":GI+"ChebyshevPsiProgressionRelativeError.lean",
 "pirel":GI+"PrimeCountRelativeErrorOfPsiRelativeError.lean",
 "zrpow":GI+"SumRpowZerosLe.lean",
 "reldef":"src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ZerosDisc.lean",
 "page":JC+"MSqPage.lean", "count":JC+"MSqCount.lean",
 "twist":MS+"twistK.lean", "abs":MS+"MeanSqAbs.lean",
 "rr":MS+"RRLe.lean", "sp":MS+"SPsqLe.lean",
 "pp":MS+"SumMinLeDiv.lean", "cn":MS+"SumCNLe.lean",
 "bad":MS+"BadShare.lean", "tail":MS+"TailKExp.lean",
 "kap4":MS+"Kappa4Loglog.lean", "kapC":MS+"kappaC.lean",
 "countbad":MS+"CountBadCore.lean", "zdbox":JC+"CountSt.lean",
 "zdsupplier":JC+"CountZAll.lean", "prim":MS+"TwistPrim.lean",
 "unique":MS+"IndUnique.lean", "drop":MS+"IndDrop.lean",
 "stage":MS+"StagePow.lean", "stage1":MS+"Stage1Succ.lean",
 "stage2":MS+"CharOf.lean", "crt":MS+"ExistsCoprimePrimePairSetSecondEqPPset.lean",
 "oddM":MS+"LogOddM.lean", "split":CB+"RealSplit.lean",
 "realbox":CB+"RealBox.lean", "win":CB+"WinPairs.lean",
 "pntweak":JC+"MeanSquareHypWIff.lean",
 "pntdens":JC+"PNTDens.lean", "pntdh":JC+"PNTDHB.lean",
})
main=(ROOT/"main.tex").read_bytes();report=(ROOT/"report.txt").read_bytes();tex=main.decode()
markers=list(re.finditer(r"(?m)^\\paragraph\{(QP\d+):",tex))
assert [m[1]for m in markers]==[f"QP{i}"for i in range(1,26)]
paragraphs={}
for i,m in enumerate(markers):
 end=markers[i+1].start()if i+1<len(markers)else len(tex)
 part=tex[m.start():end].encode()
 paragraphs[m[1]]=dict(sha256=sha(part),bytes=len(part),line_start=tex[:m.start()].count("\n")+1,line_end=tex[:end].count("\n"))
claims=[]
BASE=["Usual complex Dirichlet characters, zero-extended at nonunits; critical zeros counted with analytic multiplicity; standard elementary real/complex analysis and finite character theory."]
CN=["Explicit unreconstructed classical input CN: quadratic analytic class-number formula with residue 2^r1(2pi)^r2 hR/(w sqrt(abs(D)))."]
BD=["Explicit unreconstructed classical input BD: Bombieri log-free primitive-family zero density, including the delta log R factor after deleting the exceptional zero at scale R."]
HD=["Explicit unreconstructed classical input HD: Heath-Brown 1979 Theorem 1 hybrid density, at sigma=399/400, T=Q, h=1/100."]
def claim(i,title,statement,deps,sources,assumptions):
 cid=f"QP{i}"
 claims.append(dict(id=cid,title=title,statement=statement,status="derived_simplification",mathematical_status="proved_under_explicit_hypotheses",introduced_in="0.22",depends_on=deps,assumptions=BASE+assumptions,proof_location=dict(file="simultaneous_prime_pairs/main.tex",expanded="simultaneous_prime_pairs/report.txt",section=cid,**paragraphs[cid]),sources=sources))
claim(1,"Effective exceptional-zero gap",
 "Derive the actual c/(m^2 log m) gap from the quadratic class-number formula and a periodic-sum derivative bound, uniformly for primitive conductor f<=m.",
 ["CC2","QW14"],many("exc",["main"],"source endpoint and exact effective-gap normalization")+many("reldef",["IsExc","PrimesRel"]),CN+["m>=3; real primitive nonprincipal character; a sufficiently small fixed logarithmic neighborhood of one."])
claim(2,"Across-conductor Page uniqueness",
 "Nonnegative logarithmic derivatives give one simple exceptional primitive character across conductors <=R and the unique fixed-modulus selection at a small existential c1<=1/8.",
 ["CC3","CC4","CC5"],many("page",["page_across"])+many("exc",["main"])+many("reldef",["IsExc","ExcData"]),["The CC local logarithmic-derivative and narrow zero-free-region inputs; no claimed fixed-1/8 Page constant."])
claim(3,"Weighted zeros with the exceptional factor",
 "From BD obtain sum e^((Re rho-1)V)/abs(rho)<=C min(1,delta H) exp(-cV/H), H=log(m(T+3)), retaining the factor needed for relative main terms.",
 ["QP2"],many("zrpow",["layers","sum_rpow_zeros_le"],"related source weighted-zero interface; alternative classical BD supplier explicitly retained")+many("psirel",["zsum","mainLower"]),BD+["m>=3,T>=2,V>=C0 H; omit the selected exceptional zero; no exception means factor one."])
claim(4,"Relative Chebyshev error at a power threshold",
 "Use the right-half explicit formula at T=m^8 exp(sqrt(log u)) and the matching exceptional factor to prove relative error for phi(m)psi(u;m,a) with main u-theta u^beta/beta.",
 ["QP1","QP2","QP3","CC8"],many("psirel",["orth","combine","struct","mainLower","realEnd","psiAP_relative"]),CN+BD+["m>=3,(a,m)=1,u>=m^C; selected exceptional pair or none; exact prime-power floor endpoints."])
claim(5,"The literal PrimesRel theorem",
 "Partial summation and prime-power removal preserve relative error for Li(u)-theta Li(u^beta); obtain all existential constants, unique exception and effective gap of GlobalTheory.Lin.PrimesRel.",
 ["QP1","QP2","QP4"],many("pirel",["integral_main","abel","psi_sub_wt","main_bounds","pi_rel_of_psi_rel"])+many("primesrel",["sign_of_sq_eq_one","primesRel_holds"])+many("reldef",["PrimesRel"]),CN+BD+["The fixed-1/8 PNTAPRelW wrapper is not identified; subsequent correlation proof directly uses PrimesRel's small existential c1."])
claim(6,"Admitted progression counts",
 "For every fixed epsilon>0 and sufficiently large Y, admitted progressions have at least U^(9/10) primes in (sqrt(U),U], uniformly even with an exceptional main term.",
 ["QP1","QP5"],many("def",["admitted"])+many("count",["count_a"],"same count endpoint, using QP5 directly instead of PNTAPRelW"),CN+BD+["m>0,8|m,(a,m)=1; exact admitted logarithmic window."])
claim(7,"Uniform Jacobi cancellation outside one index",
 "Prove literal twistK for every fixed A,B,epsilon>0 by CRT-fiber orthogonality, relative progression errors and one aligned exceptional squarefree index.",
 ["QP2","QP5","QP6"],many("twist",["twistK"])+many("page",["page_across"]),CN+BD+["Odd squarefree 1<s<=Y^A, (s,m)=1, s different from the selected index; threshold uniform in admitted data."])
claim(8,"Prime-power coefficient estimates and leading-one Mertens",
 "Prove sup prime-power block O(log y), squared block sum O(y log y), RR<=C(sqrt(y)+w log y), total coefficient O(y log(2N)), and sum Lambda(n)/n<=log z+C.",
 [],many("rr",["RR_le"])+many("sp",["sum_log_primes_le_mul_log_four","sPsq_le"])+many("pp",["exists_primePowerSum_le_mul_log"])+many("cn",["sum_cN_le"])+many("kap4",["kappa4_loglog"],"source use of leading-one Mertens bound"),["y>=3; every prime of m not exceeding N is <=w; elementary Chebyshev and factorial identities are derived in the paragraph."])
claim(9,"Quadratic mean-square expansion",
 "Partition prime powers and prove meanSq_abs with diagonal/RR, explicit 2B^2+2BR exceptional contributions, and arbitrary bounded kappa without multiplicativity.",
 [],many("abs",["meanSq_abs"])+many("pntweak",["soutPart","sP","RR"]),["P primes q>N^2 in one reduced class mod m,8|m; assumed squarefree correlations <=eta*card(P) except at most one index."])
claim(10,"Literal meanSqK on the polynomial window",
 "An absolute C gives MeanSq C (Y^K)^400 P [Y,Y^K] for all bounded sequences, under admitted data and the small-or-larger-than-truncation prime-divisor condition.",
 ["QP7","QP8","QP9"],many("msq",["meanSqK"])+many("def",["MeanSq"]),CN+BD+["0<epsilon<=1,K>=1; thresholds depend on epsilon,K; every prime dividing m is <=Y^(epsilon/5) or >(Y^K)^400."])
claim(11,"A continuum maximal estimate",
 "The exact derivative identity vD_q(v)=S(v,kappa*1_(n>v)) and an L2 fundamental-theorem argument allow each prime its own witness in a dyadic interval.",
 ["QP10"],many("bad",["bsD","bs_hasDeriv_S","bs_S_sub_S","bs_mul_D_eq_S","bs_normSq_S_le","bs_sum_D_le","bs_block"]),["The MeanSq hypothesis for all bounded coefficient sequences on the same real interval; finite cutoff and finite P."])
claim(12,"Uniform bad-share bound",
 "Dyadic Markov plus a geometric sum bounds the bad proportion by 32C/[tau(1-2^-tau)]Y^-tau, uniformly in the entire polynomial interval and finite base families.",
 ["QP11"],many("bad",["bs_markov","bad_share"]),["tau>0,Y>=2; same MeanSq hypothesis; empty P gives the corresponding trivial cardinal inequality."])
claim(13,"Explicit formula above the argument height",
 "Extend CC8 to T>u by retaining the left edge and derive a uniform psi bound from a finite 399/400 box, including reflected small-zero denominators and floor endpoints.",
 ["CC1","CC3","CC7","CC8"],many("closed",["explicitFormula_closed"],"CC explicit formula extended by retaining its left-edge term")+many("def",["GoodC"])+many("tail",["tailK"],"downstream tail endpoint supplied by the alternative two-range proof"),["Primitive nonprincipal conductor <=Q, Q sufficiently large; ZeroFreeBox Q; the assertion is not a zero-free region above Q."])
claim(14,"Two-range tail and all-GoodC polynomial truncation",
 "Split at exp(B log^2Q), prove |tail(Z)|<=C[Z^-1/400 log^2Q+log^6Q/Q+Z^-1 log^2(QZ)], extend to imprimitive original levels by 2log(N)/Z deleted-prime tails, and obtain literal tailK and kappaC.",
 ["QP13","QP8","CC10","CC11","CC12"],many("tail",["tailK"])+many("kapC",["kappaC"])+many("gint",["g_integral"])+many("def",["GoodC"]),["3<=Z<=exp(B log^2Q); for tailK, 0<epsilon<=1,K>=1,Y^(epsilon/6)<=logQ<=Y^(epsilon/4), actual GoodC with no primitivity premise."])
claim(15,"Exact four-logarithm derivative bound",
 "At Z=(logQ)^1000 the tail is bounded; leading-one Mertens gives 1000loglogQ+C, hence literal kappa4 with 4logY from the strict 2/13 exponent margin.",
 ["QP8","QP14"],many("kap4",["kappa4_loglog","kappa4"]),["0<epsilon<1/52,A>0; Y^(epsilon/6)<=logQ<=A Y^(epsilon/5)log^2Y; literal GoodC, possibly imprimitive."])
claim(16,"Bad primitive boxes and prime injection",
 "HD gives O(Q^(9/200)) bad nonprincipal primitive boxes, hence O(Q^1/4) including the separately counted primitive principal character; fq=f'q' and q,q'>F>=f,f' give q=q'.",
 [],many("zdbox",["ZeroDensityBox"])+many("zdsupplier",["zero_density_box"],"existential endpoint obtained from HD; original density proof not expanded")+many("countbad",["count_bad_core"]),HD+["Q>=3; for prime counting q>F, primitive conductor fq<=Q and f<=F. A totalized value at the principal pole is not treated as an analytic zero."])
claim(17,"Primitive coprime twists and ambient-level uniqueness",
 "Prove conductor fq of a primitive base twist at q>f, and uniqueness of primitive inducers agreeing on integers coprime to the ambient modulus; justify dropping an unused prime.",
 [],many("prim",["twist_prim"])+many("unique",["ind_unique"])+many("drop",["ind_drop"])+many("def",["Ind"]),["Primitive base conductor f and odd prime q>f; the prescribed twist has its actual common-level character; CRT and uniqueness of the primitive conductor."])
claim(18,"Generic simultaneous good-prime stage",
 "Combine O(U^3/8) bad-box primes, U^9/10 prime counts, continuum bad-share, actual truncation and induced-character uniqueness for every family of <=R primitive base characters with conductors <=F<=sqrt(U).",
 ["QP6","QP10","QP12","QP14","QP16","QP17"],many("stage",["stage"])+many("def",["Box","BoxAll"]),CN+BD+HD+["0<epsilon<=1/4,tau>0,K>=1,eta>0,R fixed; actual admitted and prime-divisor hypotheses; threshold uniform in F and the family."])
claim(19,"First prime stage",
 "Obtain almost all GoodQ primes q=3 mod8 in (exp(z/2),exp(z)], z=Y^(epsilon/5), simultaneously over every character mod N0; q>N0 and q>truncation eventually.",
 ["QP18"],many("stage1",["stage1"])+many("def",["primePairSetFirst","GoodQ"]),CN+BD+HD+["N0 fixed positive,0<epsilon<1/52,tau>0,K>=1."])
claim(20,"Second prime stage with a large modulus prime",
 "Use CRT at modulus16*q*primorial_odd(z), logarithm<=4z, exponent6epsilon/5 and <=2phi(N0) base characters to obtain almost all GoodD uniformly over q and z'.",
 ["QP8","QP18","QP19"],many("stage2",["char_of","stage2"])+many("oddM",["log_oddM"])+many("crt",["exists_coprime_primePairSetSecond_eq_PPset"])+many("def",["primeSetTwoBounds","GoodD"]),CN+BD+HD+["zlog^2Y<=z'<=K^2 zlog^2Y; q in the first prime set; q is the permitted modulus prime exceeding (Y^K)^400."])
claim(21,"Actual pair_share and pair_exists",
 "Choose positive good proportions at both nonempty stages, preserving the same pair, all Rows fields and the universal BoxAll bounds for every X<=Y^K.",
 ["QP19","QP20"],many("pair_share",["boxAll_mono","share_of_bad","pair_share"])+many("pair_exists",["pair_exists"])+many("def",["Rows"]),CN+BD+HD+["All literal fixed epsilon,tau,K,N0 hypotheses and z' window; absolute common C chosen before these parameters."])
claim(22,"Complete literal PairGood and PairEx",
 "At base8M, tau=epsilon/2, K=A, install exact WinPair/coprimality, all primitive twisted-character bounds, 4logy derivative and the j-dependent real-character zero boxes.",
 ["QP15","QP17","QP21"],many("pair",["pairEx_box","pairEx_g","log_exp_product_bounds","pairEx"])+many("pairgood",["tw","height","PairGood","PairEx"]),CN+BD+HD+["M>0,0<epsilon<1/52,A>=1; the source's all-induced-character quantifiers and the entire real interval [Y,Y^A]."])
claim(23,"RealBox on the same compatible host",
 "Decompose real primitive host characters into rho times q,d quadratic factors, prove rho.N divides8oddPart(QS), exact conductor factorization and zero boxes, hence actual RealBox and its conductor bound.",
 ["CC17","QP22"],many("split",["realSplit"])+many("realbox",["realBox_main","realBox"])+many("pairgood",["RealBox"]),["Actual supplied HostRaw with q,d from PairGood; (QS,qd)=1; every prime of QS divides2M and oddPart(QS)|M. This does not construct an arbitrary host."])
claim(24,"Discharge CC's exceptional-zero premise on that host",
 "Combine QP23 with the actual CC ThinH at the same host, odd-part/conductor hypotheses and late exponential cutoff; no host or geometric-window existence is inferred.",
 ["QP23","CC19","CC20"],many("host",["thinH"])+many("pairgood",["ThinH","RealBox"]),["QP23 compatible host; oddPart(QS)<=B; log(condN)<=2x^(epsilon/5)log^2x and original ThinH cutoffs. The named classical inputs remain via PairEx."])
claim(25,"Exact conditional winPairs rescaling",
 "Given the independent VWinAt(psi,401), PairEx supplies WinDatum on arbitrarily late [Z,Z^(3/2)] intervals, with exact page function rescaling and401-to400 cutoff.",
 ["QP22"],many("win",["winPairs"]),["Explicit retained VWinAt(psi,401); source epsilon,c conditions; genuine geometric window for the same pair. No claim to prove this premise or advance a global branch."])

completed=[]
def done(k,n,ids,conditions,scope="Literal endpoint reconstructed under the explicitly listed inputs"):
 completed.append(dict(endpoint=n,claim_ids=ids,status="completed_conditionally",scope=scope,conditions=conditions,source=source(k,n)))
done("primesrel","primesRel_holds",["QP1","QP2","QP3","QP4","QP5"],CN+BD)
done("twist","twistK",["QP5","QP6","QP7"],CN+BD)
for k,n,ids in [("rr","RR_le",["QP8"]),("sp","sPsq_le",["QP8"]),("abs","meanSq_abs",["QP9"]),("bad","bad_share",["QP11","QP12"]),("tail","tailK",["QP13","QP14"]),("kapC","kappaC",["QP14"]),("kap4","kappa4_loglog",["QP15"]),("kap4","kappa4",["QP15"]),("prim","twist_prim",["QP17"]),("unique","ind_unique",["QP17"]),("drop","ind_drop",["QP17"])]:
 done(k,n,ids,["Exact original displayed hypotheses; detailed proofs and quantifier checks in the cited QP paragraphs."])
done("msq","meanSqK",["QP7","QP8","QP9","QP10"],CN+BD)
done("zdsupplier","zero_density_box",["QP16"],HD,"Existential endpoint supplied by an explicit alternative classical HD input, with its original numerical proof remaining unexpanded")
done("countbad","count_bad_core",["QP16"],HD)
for k,n,ids in [("stage","stage",["QP18"]),("stage1","stage1",["QP19"]),("stage2","stage2",["QP20"]),("pair_share","pair_share",["QP21"]),("pair_exists","pair_exists",["QP21"]),("pair","pairEx",["QP22"])]:
 done(k,n,ids,CN+BD+HD)
done("split","realSplit",["QP23"],["Original supplied real character, host-level support and coprimality hypotheses."])
done("realbox","realBox",["QP23"],["Actual compatible HostRaw and PairGood, all original prime-support and odd-part divisibility conditions."])
done("win","winPairs",["QP22","QP25"],CN+BD+HD+["Independent VWinAt(psi,401) and original parameter hypotheses."])
targets=[
 dict(id="QP-next-01",title="Expand the named classical analytic inputs if full self-containment is required",scope="CN quadratic class-number formula, BD Bombieri log-free density with exceptional factor, and HD Heath-Brown hybrid density are named classical premises, not reconstructed proofs. PrimesRel and PairEx now have explicit suppliers from them; these inputs are not RH assumptions. Retain the original density source proof as an optional replacement for HD.",sources=many("exc",["main"],"CN effective-gap endpoint")+many("zrpow",["sum_rpow_zeros_le"],"BD weighted-density endpoint")+many("zdsupplier",["zero_density_box"],"HD endpoint available; original primitive density proof remains optional")),
 dict(id="QP-next-02",title="Optional exact source-route quantitative interfaces",scope="The original huge explicit ZeroDensityBound constants and fixed-1/8 PNTAPRelW exceptional selection have not been inferred from the alternative proofs. They are optional source-route targets, not missing prerequisites for the QP PrimesRel/twistK/PairEx endpoints.",sources=many("pntweak",["IsExcPair","PNTAPRelW"])+many("remdef",["ZeroDensityBound"])),
 dict(id="QP-next-03",title="Independent geometric window and final same-object global join",scope="Supply actual compatible HostRaw and the independent VWinAt(psi,401) and cohomological windows; finish global gain-to-centered-prime-sum and final parameter contradiction. QP supplies actual PairEx and RealBox on an already specified compatible host, then CC's ThinH; winPairs still retains VWinAt. No global branch is advanced from a conditional implication alone.",sources=many("win",["winPairs"])+many("pairgood",["RealBox","ThinH"]))
]
all_sources=[s for c in claims for s in c['sources']]
ids={c['id']for c in claims};graph={c['id']:[d for d in c['depends_on']if d in ids]for c in claims};active=set();visited=set()
def visit(cid):
 assert cid not in active,("cycle",cid)
 if cid in visited:return
 active.add(cid)
 for d in graph[cid]:visit(d)
 active.remove(cid);visited.add(cid)
for cid in graph:visit(cid)
reviews=[]
f=ROOT.parent/'reviews_v0_22/dc_reviews_qp.json'
if f.exists():
 raw=f.read_bytes();bound=[cid for cid,p in paragraphs.items()if p['sha256']in raw.decode()]
 assert ids<=set(bound),('stale or incomplete QP independent review',ids-set(bound))
 reviews.append(dict(file='reviews_v0_22/'+f.name,sha256=sha(raw),expected_claim_ids=sorted(ids),bound_current_claim_ids=bound))
scope="Actual PrimesRel, twistK, arbitrary-bounded-coefficient meanSqK, continuum bad-share, all-GoodC polynomial tail and exact kappa4, both positive prime stages and full PairEx. Retains named CN/BD/HD classical inputs. RealBox and ThinH supplied on the same already compatible host; winPairs still retains independent VWinAt. No global RH/GRH conclusion or full kernel replay."
primary=[
 dict(label='CN',url='https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf',role='Named quadratic analytic class-number formula and exact regulator normalization; not reproved.'),
 dict(label='BD',url='https://www.numdam.org/item/AST_1987__18__1_0.pdf',bibliography='E. Bombieri, Le grand crible, Asterisque18, section6 Theorem14, 1974; second edition1987.',role='Named log-free density with exceptional factor, not reproved.'),
 dict(label='HD',url='https://doi.org/10.4153/CJM-1979-024-0',bibliography='D. R. Heath-Brown, The density of zeros of Dirichlet L-functions, Canad.J.Math.31(1979),231–240, Theorem1.',role='Named hybrid primitive density, not reproved. Fixed h=1/100 only.'),
]
prov=dict(component='simultaneous_prime_pairs',version='0.22',claim_prefix='QP',source_commit=COMMIT,repository=URL,scope=scope,main_sha256=sha(main),report_sha256=sha(report),builder_sha256=sha(Path(__file__).read_bytes()),claims=claims,completed_source_endpoints=completed,remaining_targets=targets,independent_reviews=reviews,external_primary_sources=primary,counts=dict(claims=len(claims),claim_source_links=len(all_sources),distinct_claim_ranges=len({(s['path'],s['line_start'],s['line_end'],s['range_sha256'])for s in all_sources}),indexed_source_files=len(cache),completed_source_endpoints=len(completed),remaining_supplier_families=len(targets)),verification=dict(git_objects_only=True,source_checkout_unchanged=True,old_components_unchanged=True,lean_compiled=False,pdf_generated=False,hypothesis_policy='CN/BD/HD named classical inputs retained; actual compatible host and VWinAt not constructed by PairEx. Optional explicit-density/fixed-1/8 source wrappers not claimed.'))
manifest=dict(component='simultaneous_prime_pairs',version='0.22',commit=COMMIT,repository=URL,source_files=[dict(path=p,sha256=sha(raw),bytes=len(raw),line_count=len(raw.splitlines()),verified_equal_to_pinned_git_blob=True,url=f'{URL}/blob/{COMMIT}/{p}')for p,raw in sorted(cache.items())])
for name,obj in [('provenance.json',prov),('source_manifest.json',manifest),('next_targets.json',dict(component='simultaneous_prime_pairs',version='0.22',commit=COMMIT,scope=scope,completed_endpoints=completed,next_targets=targets))]:
 (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
lines=['SIMULTANEOUS PRIME PAIRS — QP1–QP25','Pinned commit: '+COMMIT,'Inclusive source ranges are exact pinned Git bytes.','']
for c in claims:
 lines += [c['id']+' '+c['title'],'TeX paragraph SHA-256: '+paragraphs[c['id']]['sha256']]
 for s in c['sources']:lines += ['  '+s['declaration'],'  '+s['pinned_url'],'  file_sha256='+s['sha256'],'  range_sha256='+s['range_sha256']]
 lines.append('')
(ROOT/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps(prov['counts'],indent=2))



