#!/usr/bin/env python3
"""Reproduce AH provenance from pinned Git blobs; never alter the checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=ROOT.parents[1] / "lean-source")
args = parser.parse_args()
REPO = args.repo.resolve()
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
HC = "src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/"
IG = HC + "InertiaGaloisSymmetry/"
CH = "src/Development/AutomorphicArithmetic/CharacterBoxes/"
FO = "src/Formalism/FrobeniusOrbits/FrobeniusOrbitsProofs/"
WC = "src/Development/AutomorphicArithmetic/WeightCongruences/"
IP = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"

P = {
    "statement": "src/Formalism/FrobeniusOrbits/Statement.lean",
    "frame": HC + "ZsmulGeneratorEqZeroOfProjection.lean",
    "frame_cyc": HC + "FrameCyclicGenerator.lean",
    "raw": HC + "ConjEMemHostFIff.lean",
    "analytic": HC + "Analytic.lean",
    "level": HC + "ExplicitFormulaErrorOfHostConditions.lean",
    "sign": HC + "ArtinMapSecondEqJacobiSym.lean",
    "gauss": FO + "EqZeroOfNegEq.lean",
    "char": IG + "OfChar.lean",
    "crt": IG + "OfCharFrame.lean",
    "modulus": IG + "OfCharLevel.lean",
    "any_frame": IG + "AnyFrame.lean",
    "any_level": IG + "AnyLevel.lean",
    "ord": CH + "OrdAny.lean",
    "ker": CH + "KerChiAny.lean",
    "twist": CH + "TwistAny.lean",
    "twist_def": CH + "TwistForm.lean",
    "field": CH + "FieldChi.lean",
    "core": IG + "DecompTypeI.lean",
    "basic": IG + "CycBasic.lean",
    "lift": IG + "CycLift.lean",
    "roots": IG + "RootEqOfSubMem.lean",
    "groups": IG + "CycGrp.lean",
    "all": IG + "CycAll.lean",
    "kc_base": IG + "KcBase.lean",
    "kc_diff": IG + "KcDiff.lean",
    "kc_pair": IG + "KcPair.lean",
    "kc_dual": IG + "KcDiffSmulMem.lean",
    "kc_norm": IG + "KcEqOfPowEqOne.lean",
    "rd_diff": IG + "RdDiff.lean",
    "rd_arith": IG + "RdArith.lean",
    "rd_bound": IG + "RdBound.lean",
    "rd": IG + "DvdDiscrOfInertia.lean",
    "derived": IG + "OfRawToHostRaw.lean",
    "split": FO + "SplitK.lean",
    "decomp": FO + "Decomp.lean",
    "eta": FO + "NcardEqTwoIff.lean",
    "coords": IP + "NormOneIffOfSqrt.lean",
    "norm": WC + "NormRootOfUnityQuadraticSubfield.lean",
    "seam": "src/Development/AutomorphicArithmetic/CoprimeRanks/SecondSetNoRelation.lean",
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
    text = [line.decode().rstrip("\r\n") for line in lines]
    pattern = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure)\s+" + re.escape(spelling) + r"(?=\s|\{|\(|:|$)")
    hits = [i for i, line in enumerate(text) if pattern.match(line)]
    if namespace is not None:
        hits = [i for i in hits if namespace_at(text, i) == namespace]
    assert len(hits) == 1, (path, spelling, hits, namespace)
    start = hits[0]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(text[end]):
        end += 1
    while end > start + 1 and not text[end - 1].strip():
        end -= 1
    part = b"".join(lines[start:end])
    ns = namespace_at(text, start)
    full_name = ((ns + ".") if ns else "") + spelling
    if full_name.startswith("_root_."):
        full_name = full_name[len("_root_."):]
    url = f"{URL}/blob/{COMMIT}/{path}#L{start + 1}-L{end}"
    return {
        "path": path, "declaration": full_name, "source_spelling": spelling,
        "line_start": start + 1, "line_end": end,
        "sha256": sha(raw), "full_file_sha256": sha(raw),
        "range_sha256": sha(part), "range_bytes": len(part),
        "first_line": text[start], "declaration_lines_within_range": [start + 1],
        "url": url, "pinned_url": url, "role": role,
        "verified_equal_to_pinned_git_blob": True,
    }


def many(key, spellings, role="literal conclusion or substantive supplier"):
    return [source(key, spelling, role) for spelling in spellings]


main = (ROOT / "main.tex").read_bytes()
report = (ROOT / "report.txt").read_bytes()
main_text = main.decode()
markers = list(re.finditer(r"(?m)^\\paragraph\{(AH\d+):", main_text))
assert [m.group(1) for m in markers] == [f"AH{i}" for i in range(1, 19)]
paragraphs = {}
for i, match in enumerate(markers):
    end = markers[i + 1].start() if i + 1 < len(markers) else len(main_text)
    text = main_text[match.start():end]
    paragraphs[match.group(1)] = {
        "sha256": sha(text.encode()),
        "line_start": main_text[:match.start()].count("\n") + 1,
        "line_end": main_text[:end].count("\n"),
        "bytes": len(text.encode()),
    }

claims = []


def claim(i, title, statement, dependencies, sources, assumptions):
    cid = f"AH{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.16",
        "depends_on": dependencies, "assumptions": assumptions,
        "proof_location": {
            "file": "arithmetic_hosts/main.tex",
            "expanded": "arithmetic_hosts/report.txt",
            "section": cid,
            **paragraphs[cid],
        },
        "sources": sources,
    })


claim(1, "Finite duality and the cyclic two-adic quotient",
      "H_e is cyclic of order 2^e; for arbitrary Xi the quotient by its annihilator has order |Xi| and exactly Xi as its complex character group; unit reduction is surjective.",
      ["SZ13"],
      many("statement", ["HGrp", "hcl"]) +
      many("frame_cyc", ["cycIso"]) +
      many("modulus", ["ann", "mem_ann", "mem_iff", "B", "card_B", "xiW_surj"]),
      ["M is positive and Xi is a subgroup of the complex characters modulo M; no evenness or TwoGroup premise."])

claim(2, "Minimal character modulus and actual mixed frame",
      "Choose the least good Q, descend xiW, form image(cl,xi), select the cyclic kernel generator and transport to Fin(n); obtain o=|Xi| and the literal Frame generator condition.",
      ["AH1"],
      many("modulus", ["xiW", "Good", "exists_good", "QS", "good_QS", "not_good", "QS_dvd", "QS_dvd_mul", "QS_pos", "xi", "xi_unitsMap", "xi_surj"]) +
      many("any_frame", ["ModData", "eta", "projection_surjective", "exists_gen", "hA_ker", "frame", "isoA", "iso", "ord_eq", "toA", "toA_surj", "hH_toA", "xiA", "xiA_toA", "mem_cusp_forms_iff_automorphic_compact", "o_eq", "twoGroup"]) +
      many("frame_cyc", ["ofGroup", "ofGroupIso", "ofGroup_generator"]) +
      many("frame", ["Frame"]),
      ["M>0, e>=0, supplied finite character subgroup Xi."])

claim(3, "The sign-corrected CRT Artin map",
      "The literal art(u)=(alpha,beta,a(u)w(alpha)) is onto and satisfies every CharData Artin field, including art(-1)=cc for odd characters.",
      ["AH1", "AH2"],
      many("statement", ["HostHyp"]) +
      many("crt", ["exists_unit_three"]) +
      many("any_frame", ["w", "w_mul_self", "hH_w", "art", "art_snd", "art_ps", "art_ch", "art_surj", "charData"]) +
      many("char", ["CharData"]) +
      many("sign", ["sgnN", "sgnN_val"]),
      ["Exact HostHyp(q,d), gcd(Q,qd)=1, e>=2, T_e|Q and supplied splitting at all odd primes dividing Q."])

claim(4, "Actual fixed field and quadratic Gauss roots",
      "The fixed field of ker art in Q(zeta_N) gives the specified raw host and Artin restriction; Gauss sums construct s_d and, for AH3, s_q with their exact sign actions.",
      ["AH3"],
      many("char", ["L", "cyc", "res", "E", "gal", "gal_restrict", "gal_symm_apply", "exists_root", "exists_sqd", "toHostRaw", "exists_sqq"]) +
      many("any_frame", ["host", "exists_sqq"]) +
      many("any_level", ["host", "exists_sqq"]) +
      many("gauss", ["gs", "gs_sq", "sqrt_exists"]) +
      many("sign", ["gs_act", "sqrt_act"]) +
      many("raw", ["HostRaw"]),
      ["The supplied CharData hypotheses, or the explicit AH3 hypotheses. Finite Galois and cyclotomic foundations are stated."])

claim(5, "Exact modulus and primitive conductor",
      "For each prime l|Q construct v=1 mod Q/l with eta(v)!=1 and its CRT Artin lift; for primitive cyclic psi prove M|Q, hence Q=lcm(T_e,M).",
      ["AH1", "AH2", "AH3"],
      many("any_level", ["exact_data", "exact"]) +
      many("any_frame", ["exact"]) +
      many("ker", ["ann_zpowers", "xiW_eq_one", "dvd_QS"]) +
      many("raw", ["Exact"]) +
      many("modulus", ["not_good"]),
      ["e>=1 for the exactness witness; primitive psi for the conductor divisibility."])

claim(6, "An eventually constant frame-order multiplier",
      "For fixed M,Xi, n_e=2^e|J_e| with a descending finite sequence J_e; choose 1<=c0<=|Xi| and e1 before q,d,b such that n_e=c0*2^e for all e>=e1.",
      ["AH1", "AH2"],
      many("ord", ["ord_eq_mul", "cl_eq_one_iff", "step", "UpperTheory.Top.ordAny"]) +
      many("any_level", ["data", "frame", "o_eq"]),
      ["Fixed positive M and subgroup Xi; no analytic size or prime-window premise."])

claim(7, "Prescribed characters are kept and first sign is excluded",
      "Define theta_chi(s,t,a)=chi_B(xi_A(a w(s))); prove KeptInXp and the complete ExceptionalCharacterKept predicate for Level.ofSub with psK=none.",
      ["AH1", "AH2", "AH3", "AH4"],
      many("any_level", ["thetaA", "theta", "theta_mem", "thetaA_toA", "theta_art", "prim_theta", "keptInXp", "exceptional_character_condition"]) +
      many("level", ["Level.ofSub", "Level.mem_ofSub", "Level.cyc"]) +
      many("analytic", ["TrivialOnFirstFactor", "Xp", "KeptInXp", "ExceptionalCharacterKept"]) +
      many("modulus", ["HostRaw.art_eq_of_prim_eq"]),
      ["The same AH3 host and fixed Xi; no assertion of KeptEqXp or evenness."])

claim(8, "The exact kernel and all permitted quadratic twists",
      "For primitive psi obtain KerChi with M|Q and both Legendre signs; every character trivial on A0 has chi(a)(a/q)^i(a/d)^j with chi in <psi> and theta(iod)=(-1)^j.",
      ["AH1", "AH2", "AH3", "AH5"],
      many("ker", ["art_iff", "hcl_nat", "UpperTheory.Top.kerChiAny"]) +
      many("twist", ["exA", "exSign", "dvd_lemma_3", "UpperTheory.Top.twistAny"]) +
      many("twist_def", ["KerChi", "TwistForm"]),
      ["Primitive psi; exact AH3 host; theta kills the designated A0, not necessarily the whole A."])

claim(9, "Cyclotomic integral reduction and local Galois groups",
      "Prove integral generation, prime-to-p residue order, inertia and Frobenius congruences, and their exact descent to a supplied Galois subfield; decomposition exponents are powers of p.",
      ["AH1"],
      many("roots", ["root_eq_of_sub_mem", "ringHom_ext_zO", "zO_sub_mem_iff", "tauN_inertia_iff", "tauN_frob", "inertia", "frob_of_modEq", "exists_frob", "frob_any", "decomp"]) +
      many("lift", ["inertia_res", "frob_res", "inertia_lift", "exists_over", "frob_iff_inertia"]) +
      many("decomp", ["stab_eq_inertia_mul"]),
      ["Positive N; finite Galois subfield of Q(zeta_N) with the actual restriction map. The local Galois residue theorem is explained; no HostCore premise."])

claim(10, "CM data and local identification for every raw host",
      "Identify any raw host with its cyclotomic fixed-field image; prove art surjectivity, all CM and degree/type fields, first-sign eigenvector, art_ch, and the unramified Frobenius coordinates.",
      ["AH4", "AH9"],
      many("basic", ["exists_lift", "exists_emb_lift", "tauN_neg_one", "emb_art", "gal_eq_art_iff", "art_surj", "conj_apply", "conj_iff", "cm", "finrank_E", "finrank_F", "mem_F", "art_ch", "gal_mem_Psi_iff"]) +
      many("all", ["emb_sqd", "cmType_iff", "cmType", "ps_root"]) +
      many("groups", ["jac_lemma", "frob"]) +
      many("raw", ["HostRaw", "K", "cmType", "psAt"]),
      ["An arbitrary literal HostRaw. AH4 is used for its general Gauss-root calculation, not to assume the raw host was newly constructed."])

claim(11, "Ramified decomposition and finite unramified CM extension",
      "Prove I_d={1,iod}, D_p subset Psi for p|Qq, ps_d without PsQ, exclusion of cc from every decomposition group over N, and finite unramified E/F.",
      ["AC8", "AH9", "AH10"],
      many("coords", ["half_int_coords", "exists_rat_coords"]) +
      many("split", ["two_case", "ram_case", "odd_case", "clause"]) +
      many("groups", ["sq_two_pow", "sq_odd_pow", "sq_mod", "split_QSq", "ordCompl_d", "ps_congr", "ps_d", "exists_art_iod", "inertia_d", "decomp_typeI", "decompConj", "unramEF"]),
      ["An arbitrary HostRaw; its exact d=7 mod16, e>=2 and splitting hypotheses remain in force."])

claim(12, "Exact split, ordinary and eta clauses",
      "Prove the literal splitK criterion, universal ordinary equivalence, and all three eta clauses using quadratic factorization and the actual decomposition groups.",
      ["AH9", "AH10", "AH11"],
      many("kc_base", ["kc_mem_Psi_iff", "kc_fixK", "splitK", "ordinary", "kc_unr", "eta"]) +
      many("split", ["clause"]) +
      many("eta", ["split_or_inert", "ncard_eq_two_iff"]),
      ["The same arbitrary raw host; no additional splitting conclusion beyond its literal predicates."])

claim(13, "The selected half-different integral ideal",
      "Prove different support above Qq, separate the conjugate K-primes, choose one side with the actual exponents, and obtain D=b*bar(b), b+bar(b)=O_E and Psi-invariance.",
      ["AH9", "AH10", "AH11", "AH12"],
      many("kc_diff", ["kc_below_smul", "diffSupport", "kc_below_ne", "principal"]) +
      many("kc_pair", ["kc_nf_map", "kc_pairing", "kc_not_dvd_different"]) +
      many("kc_dual", ["kc_mem_dual_iff", "kc_mem_diff_iff", "kc_dual_smul", "kc_diff_smul_eq"]),
      ["An arbitrary HostRaw. The source's principal means an integral ideal with this factorization, not a principal ideal or a class-number hypothesis."])

claim(14, "Both directions of conjugated trace self-duality",
      "For any integral b with D=b*bar(b), prove x in b^-1 iff Tr_E/K(x*bar(y)) is integral for every y in b^-1, using the exact fractional-ideal dual formula.",
      ["AH10", "AH13"],
      many("kc_dual", ["kc_mem_dual_iff", "kc_mem_diff_iff", "kc_smul_ne_bot", "kc_mem_inv_smul", "unimodular"]),
      ["Any integral ideal satisfying the literal different factorization; the constructed ideal is one such input. No generator or metric identification is assumed."])

claim(15, "Derive the finite-kernel root-discriminant identity",
      "From integral cyclotomic generation, the monogenic different and norm of 1 minus a root, derive log rd(E)=sum_{a|N} Lambda(a)*rho_U(N/a).",
      ["AH1", "AH9"],
      many("rd_diff", ["log_abs_eval_one_cyclotomic_eq_vonMangoldt", "log_norm_root", "adjoin_top", "minpoly_map", "absNorm_diff", "log_discr_tower", "log_discr_sub", "log_norm_weight", "log_rd"]) +
      many("rd_arith", ["sum_totient_pow", "weight_sum", "order_dvd_iff", "card_KK", "rho", "abel"]) +
      many("rd", ["log_rd_eq"]),
      ["Any subfield of a positive-modulus cyclotomic field with its actual fixing subgroup; no analytic estimate."])

claim(16, "All discriminant bounds and support",
      "Prove rd^2>=4n, rd<=Q/2 sqrt(qd), rd>=2^(e+1-2^-e)sqrt(d), discriminant support in N with 2,d present, and signed disc(E)=disc(F)^2.",
      ["AH1", "AH9", "AH10", "AH11", "AH15"],
      many("rd_arith", ["rho_nonneg", "rho_eq", "rho_le", "half_le_rho", "rho_le_half", "KK_gcd"]) +
      many("rd_bound", ["SS", "log_index_le", "SS_le", "rho_two", "le_SS"]) +
      many("rd", ["rho_d", "rho_q", "exists_two", "discr_primes", "rd_ge", "rd_le", "rd_sq_ge"]) +
      many("kc_diff", ["discr_sq"]),
      ["An arbitrary raw host; exact two-adic kernel, q/d inertia conditions and e>=2 retained."])

claim(17, "Every HostDer field is supplied",
      "Assemble all 30 proved HostDer fields for every HostRaw; retain its exact raw projection in HostAx.ofRaw, with norm_mu supplied acyclically by AC2–AC3.",
      ["AC2", "AC3", "AH9", "AH10", "AH11", "AH12", "AH13", "AH14", "AH15", "AH16"],
      many("raw", ["HostDer", "DerOfRaw", "HostAx"]) +
      many("core", ["HostCore"]) +
      many("all", ["hostCore"]) +
      many("derived", ["HostRaw.der", "HostAx.ofRaw", "HostAx.ofRaw_toHostRaw"]) +
      many("norm", ["UpperTheory.norm_root_of_unity_quadratic_subfield"]) +
      many("kc_norm", ["norm_mu"], "literal endpoint supplied by the prior AC2–AC3 reconstruction"),
      ["Only the literal HostRaw fields; no retained HostCore, HostDer, half-different, or discriminant supplier."])

claim(18, "The full prescribed-character fieldChi constructor",
      "Choose c0,e0 from psi before e,q,d,b; construct the exact HostAx with all eight FieldRows fields and every conductor, kept-character, kernel and twist conjunct of fieldChi.",
      ["AH2", "AH3", "AH4", "AH5", "AH6", "AH7", "AH8", "AH17"],
      many("field", ["conductor_divisor_bounds", "UpperTheory.Top.fieldChi"]) +
      many("seam", ["FieldRows"]) +
      many("any_level", ["QS_le", "o_eq", "o_eq_level"]) +
      many("level", ["Level.cyc"]) +
      many("twist_def", ["WinDatum"], "exact analytic window interface remains outside this arithmetic construction"),
      ["Primitive psi; for every e>=e0 supplied HostHyp(q,d), q!=3, gcd(M,qd)=1, 4M<=b, and splitting of -d at all odd primes <=b. No selection of such q,d in analytic windows."])


def fields(key, spelling):
    loc = source(key, spelling, "literal record field audit")
    text = blob(loc["path"]).decode().splitlines()[loc["line_start"] - 1:loc["line_end"]]
    names = []
    for line in text[1:]:
        m = re.match(r"^  (?:\[)?([A-Za-z_][A-Za-z0-9_']*)\s*:", line)
        if m:
            names.append(m.group(1))
    return loc, names


frame_map = {f: "AH2" for f in ["e", "ord", "grp", "h0", "projection_surjective_field", "gen0", "zsmul_generator_eq_zero_of_projection"]}
char_map = {f: "AH3" for f in ["q", "d", "QS", "hyp", "two_le_e", "QS_pos", "tower_dvd", "QS_coprime", "QS_split", "art", "art_surj", "art_neg_one", "art_h", "art_d", "art_q", "art_ch"]}
raw_map = {f: "AH4" for f in ["q", "d", "QS", "hyp", "two_le_e", "QS_pos", "tower_dvd", "QS_coprime", "QS_split", "E", "instField", "instNF", "galois", "gal", "sqd", "sqd_sq", "gal_sqd", "cycEmb", "cycZeta", "cycZeta_prim", "art", "art_spec", "art_neg_one", "art_h", "art_d", "art_q"]}
der_map = {}
for supplier, names in {
    "AH10": "art_surj cm conj_iff finrank_E finrank_F mem_F cmType ps_root art_ch",
    "AH9,AH10": "frob frob_any inertia decomp",
    "AH11": "ps_d inertia_d decomp_typeI decompConj unramEF",
    "AH12": "splitK ordinary eta",
    "AH13": "diffSupport principal",
    "AH14": "unimodular",
    "AH15,AH16": "discr_sq discr_primes rd_ge rd_le rd_sq_ge",
    "AC2,AC3": "norm_mu",
}.items():
    der_map.update({name: supplier for name in names.split()})
rows_map = {
    "psQ": "AH3", "sqq": "AH4", "QS_exact": "AH5", "QS_le": "AH18",
    "o_pow": "AH18", "q_ne_three": "AH18 exact input",
    "split_small": "AH18 exact input", "small_le": "AH18",
}
audits = []
for key, spelling, mapping, count in [
    ("frame", "Frame", frame_map, 7),
    ("char", "CharData", char_map, 16),
    ("raw", "HostRaw", raw_map, 26),
    ("raw", "HostDer", der_map, 30),
    ("seam", "FieldRows", rows_map, 8),
]:
    loc, names = fields(key, spelling)
    assert len(names) == count, (spelling, names, count)
    assert set(names) == set(mapping), (spelling, names, mapping)
    audits.append({
        "record": loc["declaration"], "field_count": count, "source": loc,
        "fields": [{"name": name, "supplied_by": mapping[name]} for name in names],
        "scope": "Exact conditional record fields; supplied hypotheses are identified, not erased.",
    })

completed_specs = [
    ("field", "UpperTheory.Top.fieldChi", "AH18"),
    ("any_frame", "charData", "AH3"),
    ("any_frame", "host", "AH4"),
    ("any_level", "host", "AH4"),
    ("char", "toHostRaw", "AH4"),
    ("derived", "HostRaw.der", "AH17"),
    ("derived", "HostAx.ofRaw", "AH17"),
    ("kc_diff", "principal", "AH13"),
    ("kc_diff", "diffSupport", "AH13"),
    ("kc_dual", "unimodular", "AH14"),
    ("ord", "UpperTheory.Top.ordAny", "AH6"),
    ("ker", "UpperTheory.Top.kerChiAny", "AH8"),
    ("twist", "UpperTheory.Top.twistAny", "AH8"),
    ("any_level", "exact", "AH5"),
    ("any_level", "keptInXp", "AH7"),
    ("any_level", "exceptional_character_condition", "AH7"),
    ("all", "hostCore", "AH17"),
    ("rd", "rd_ge", "AH16"),
    ("rd", "rd_le", "AH16"),
    ("rd", "rd_sq_ge", "AH16"),
]
completed = []
for key, spelling, cid in completed_specs:
    completed.append({
        **source(key, spelling, "completed literal arithmetic constructor or substantive prerequisite"),
        "completed_by": cid, "human_status": "proved_under_explicit_hypotheses",
        "remaining_human_scope": "None within the literal conditional conclusion.",
    })

remaining = [
    {
        "interface": "Analytic pair/character-field window",
        "scope": "Select q,d,e,Y in the simultaneous analytic windows, including VVle; AH18 assumes the literal HostHyp, coprimality and splitting conditions.",
        "source_anchors": [source("twist_def", "WinDatum", "retained analytic window definition")],
    },
    {
        "interface": "HC analytic top-window and prime suppliers",
        "scope": "The exact ShortNorm, SmallOne, ThinH and top-window hypotheses remain outside AH; no prime-distribution estimate follows from its fixed-field or discriminant construction.",
    },
    {
        "interface": "Full HostGood/WinOK, LevelPrime and du–Ds inputs",
        "scope": "AH supplies arithmetic HostAx and FieldRows. It does not claim all geometric/automorphic host inputs or analytic level/window hypotheses.",
    },
    {
        "interface": "Over, RecExP/RecOK and the four global branches",
        "scope": "These are independent remaining global joins. No old proof or branch premise is modified by this component.",
    },
]

source_files = []
for path in sorted(cache):
    raw = cache[path]
    source_files.append({
        "path": path, "sha256": sha(raw), "bytes": len(raw),
        "lines": len(raw.splitlines()), "commit": COMMIT,
        "url": f"{URL}/blob/{COMMIT}/{path}",
        "verified_equal_to_pinned_git_blob": True,
    })
links = sum(len(c["sources"]) for c in claims)
unique = {(s["path"], s["line_start"], s["line_end"], s["range_sha256"])
          for c in claims for s in c["sources"]}
artifacts = {
    "main.tex": {"sha256": sha(main), "bytes": len(main)},
    "report.txt": {"sha256": sha(report), "bytes": len(report)},
    "build_provenance.py": {"sha256": sha(Path(__file__).read_bytes()), "bytes": len(Path(__file__).read_bytes())},
}
assert len(set(c["id"] for c in claims)) == 18
known = {c["id"] for c in claims}
for c in claims:
    for d in c["depends_on"]:
        if d.startswith("AH"):
            assert d in known and int(d[2:]) < int(c["id"][2:]), (c["id"], d)

provenance = {
    "artifact_version": "0.16", "component": "arithmetic_hosts",
    "repository": URL, "commit": COMMIT,
    "scope": "Actual conditional arithmetic host and fieldChi reconstruction, including every HostDer field. Analytic prime/window existence and separate global joins remain explicit.",
    "claim_count": len(claims), "source_link_count": links,
    "unique_claim_source_range_count": len(unique), "source_file_count": len(source_files),
    "line_range_convention": "Inclusive one-based source lines, hashed with original newline bytes from pinned Git blobs.",
    "claims": claims, "record_audits": audits,
    "record_field_count": sum(a["field_count"] for a in audits),
    "record_field_count_scope": "7 Frame + 16 CharData + 26 HostRaw + 30 HostDer + 8 FieldRows; 87 fields, including exact supplied input fields and two HostRaw typeclass fields.",
    "proof_artifacts": artifacts, "source_files": source_files,
    "completed_targets": completed, "retained_interfaces": remaining,
    "foundational_scope": [
        "Finite abelian character duality, CRT and the two-adic unit computation are proved in the text.",
        "Cyclotomic integral generation and residue-order calculations are explained; standard finite Galois prime and Dedekind ideal facts are stated with their local justification.",
        "The finite-kernel root-discriminant formula and all three estimates are derived, not retained as analytic assumptions.",
        "The name principal refers to a selected half-different ideal, not an assertion of principal ideal generation.",
        "Norm_mu uses prior AC2–AC3 under raw hypotheses and is acyclic.",
    ],
    "validation": {
        "read_only_source_access": True,
        "present_checkout_files_equal_pinned_blobs": True,
        "source_range_hashes_regenerated": True,
        "literal_record_fields_audited": True,
        "claim_dependency_order_acyclic": True,
        "lean_build_performed": False, "pdf_build_performed": False,
    },
}
manifest = {
    "artifact_version": "0.16", "component": "arithmetic_hosts",
    "repository": URL, "commit": COMMIT,
    "source_file_count": len(source_files), "source_files": source_files,
    "proof_artifacts": artifacts,
}
next_targets = {
    "artifact_version": "0.16", "repository": URL, "commit": COMMIT,
    "status": "All assigned literal conditional arithmetic endpoints and the listed substantive prerequisites are discharged.",
    "targets": [], "target_count": 0, "completed_targets": completed,
    "retained_interfaces": remaining,
    "precision_notes": [
        "FieldChi preserves the original quantifiers: c0,e0 depend only on psi, before e,q,d,b.",
        "No surviving HostCore, HostDer, half-different or discriminant supplier is hidden behind a record wrapper.",
        "The mixed-character frame allows odd-order factors and non-even characters.",
        "No analytic prime/window existence, full HostGood or global reciprocity branch is inferred.",
    ],
}
for name, obj in [("provenance.json", provenance), ("source_manifest.json", manifest), ("next_targets.json", next_targets)]:
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

locators = [
    "ARITHMETIC HOSTS (AH1–AH18): PINNED SOURCE LOCATORS",
    f"Repository: {URL}", f"Commit: {COMMIT}",
    f"Claims: {len(claims)}; source links: {links}; unique claim ranges: {len(unique)}; source files: {len(source_files)}.",
    "Ranges are inclusive, one-based; all range bytes are read from the pinned Git blob.",
    f"main.tex SHA256: {sha(main)}", f"report.txt SHA256: {sha(report)}", "",
]
for c in claims:
    locators += [c["id"] + ": " + c["title"],
                 "  Proof paragraph SHA256: " + c["proof_location"]["sha256"]]
    for s in c["sources"]:
        locators += [
            f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['role']}",
            "    " + s["pinned_url"],
            f"    file SHA256 {s['full_file_sha256']}; range SHA256 {s['range_sha256']}",
        ]
    locators.append("")
locators += ["RECORD FIELD AUDIT"]
for a in audits:
    locators.append(f"  {a['record']}: {a['field_count']} fields")
    for f in a["fields"]:
        locators.append(f"    {f['name']} <- {f['supplied_by']}")
locators += ["", "RETAINED BOUNDARY"]
for item in remaining:
    locators.append("  " + item["interface"] + ": " + item["scope"])
(ROOT / "source_locators.txt").write_text("\n".join(locators) + "\n")
print(json.dumps({
    "claims": len(claims), "source_links": links,
    "unique_claim_ranges": len(unique), "source_files": len(source_files),
    "record_fields": sum(a["field_count"] for a in audits),
    "completed_targets": len(completed), "remaining_arithmetic_targets": 0,
    "main_sha256": sha(main), "report_sha256": sha(report),
}, indent=2))
