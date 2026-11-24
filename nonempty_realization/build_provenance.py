#!/usr/bin/env python3
"""Rebuild NR provenance from pinned Git blobs without checkout mutation."""
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
AB = "src/Development/AbelianVarietyTheory/"
IW = AB + "Proofs/IwasawaDecomposition/"
IE = AB + "Proofs/InertiaEigenvalues/"
ND = AB + "Definitions/NonGaloisDescent/"
AM = AB + "Definitions/AutomorphicMembership/"
UN = "src/Formalism/LocalToGlobal/UnitaryNorms/"
P = {'emb': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 'prime': 'src/Formalism/LocalRingCardinality/SpanPowerMembership/NDLocG.lean', 'low': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsCoefficientFieldLowerBounds.lean', 'ints': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteResidueField.lean', 'complete': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsIntegersCompletion.lean', 'unram': 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/NormEqZpowOfMemMaxUnramifiedSubfield.lean', 'coeff': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ClosureAdjoinUnitBallCoeffBound.lean', 'cyclo': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsCyclotomicUnramifiedCompletedIntegers.lean', 'ringclass': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsRingClassHost.lean', 'compact': 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CompactGroupRepDefinedOverFiniteExtension.lean', 'lattice': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsFinExtConjIntOf.lean', 'rho': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsGaloisRepFamilyBounded.lean', 'twist': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsGaloisRepOfCuspidal.lean', 'ring': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsTwistRingsCharactersClassGroups.lean', 'cover': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsTwistIndexOfCoefficientFieldPlace.lean', 'spec': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ConcreteTwistFrameExtraExcludedOverSmallPrimes.lean', 'side': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', 'triple': 'src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/CharpolySmulOfProd.lean', 'second': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/RowCuspMultiplicityInput.lean', 'twr': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/TwistBaseCoefficientRingResidueFieldFinite.lean', 'bridge': 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean', 'ntw': 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataN.lean', 'mt': 'src/Formalism/LocalToGlobal/GaloisLevelStructure/TiedHecke.lean', 'mtad': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/SubsetTwistExceptionalPlaces.lean', 'empty': 'src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/IsCharsOfReading.lean', 'exp': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExponentAndTwistData.lean', 'galex': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EventuallyNatCastNotMem.lean', 'cheb': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ChebSplitNd.lean', 'toric': 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ExistsToricCharactersInTwistCoefficientRings.lean', 'weights': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsWeightDataIntegral.lean', 'avatars': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/InertialOrderFifteenCharAuxiliaryPrimeSpec.lean', 'mttransport': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsMotiveAdjointWithLevels.lean', 'reps': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/BlocksUnique.lean', 'artin': 'src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean', 'frame': 'src/Formalism/LocalToGlobal/UnitaryNorms/CharTied.lean', 'values': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsGaloisGe.lean', 'unitindex': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteIndexUnitIdlSup.lean', 'cminvol': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/GoodTupleConditionOfIdempotentZero.lean'}

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
    pat = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure|instance)\s+" + re.escape(spelling) + r"(?=\s|\{|\(|:|$)")
    hits = [i for i, line in enumerate(texts) if pat.match(line)]
    if not hits:
        # A source may spell a theorem with its explicit namespace prefix.
        decl = re.compile(PREFIX + r"(?:theorem|lemma|def|abbrev|structure|instance)\s+([^\s({:]+)")
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


main = (ROOT / "main.tex").read_bytes()
report = (ROOT / "report.txt").read_bytes()
tex = main.decode()
assert not [c for c in tex if ord(c) < 32 and c not in "\n\r\t"]
assert not re.search(r"(?<![A-Za-z\\])q?quad\b", tex)
markers = list(re.finditer(r"(?m)^\\paragraph\{(NR\d+):", tex))
assert [m.group(1) for m in markers] == [f"NR{i}" for i in range(1, 25)]
paragraphs = {}
for i, match in enumerate(markers):
    end = markers[i+1].start() if i+1 < len(markers) else len(tex)
    part = tex[match.start():end].encode()
    paragraphs[match.group(1)] = {
        "sha256": sha(part), "bytes": len(part),
        "line_start": tex[:match.start()].count("\n")+1,
        "line_end": tex[:end].count("\n"),
    }
claims = []


def claim(i, title, statement, deps, sources, assumptions):
    cid = f"NR{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.21", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "nonempty_realization/main.tex",
            "expanded": "nonempty_realization/report.txt",
            "section": cid, **paragraphs[cid],
        }, "sources": sources,
    })


LOCAL = [
    "l is prime; fixed Qbar_l with |l|=l^-1 and its completion C_l",
    "Unique norm extension and completeness for finite local fields; finite-dimensional norm equivalence",
]
CFT = [
    "Supplied GlobalArtinReciprocity with its exact quotient, kernel, inertia and inverse-arithmetic-Frobenius laws",
    "E is the actual totally complex host number field and Omega its fixed algebraic closure",
]
FIXED = [
    "Same D, host, NData algebraic closure and places, original rows, K=LL0 subset L=what2.LL and epsilon",
    "Actual CharFrame, NData type-prime splitting and host auxiliary-prime laws",
    "ValLL0 for the fixed K embedding; star-stable K; integral eExp(j,g)",
]
REP = [
    "Literal SideA and GalEx for the same D and automorphic package",
    "Actual RowCusp including cofinite K-valued normalized Frobenius polynomials for each good occurring row",
    "ChebSplit for the actual split Frobenius lifts outside every finite set",
]

claim(1, "Actual prime-compatible algebraic embeddings",
      "Construct J_q at every finite prime of K with the exact strict-norm center, and a global algebraic-closure embedding inducing any prescribed valuation ring above l.",
      [], many("prime", ["Kphi", "Kphi_fin", "phi_mem", "exists_embAt"]) +
      many("emb", ["val_int_lt_one_iff", "exists_embedding"]) +
      many("ring", ["exists_prime_mem", "placesOver_nonempty"]),
      LOCAL + ["Number fields, their prime completions, transitivity of extensions of valuations in finite normal extensions and inverse-limit compactness"])
claim(2, "Density and normalized norm extension through the completion",
      "An algebraically closed global image is dense in Qbar_l. Equal valuation rings determine equal normalized norms; their isometry extends through C_l and restricts to a unique Q_l-automorphism.",
      ["NR1"], many("emb", ["denseRange_embedding", "norm_eq_of_le_one_iff", "exists_algEquiv", "norm_algEquiv", "algEquiv_ext"]),
      LOCAL + ["Omega algebraically closed and algebraic over Q; completeness of C_l"])
claim(3, "Actual local decomposition bridges and finite coefficient integer rings",
      "Construct the topological decomposition-group equivalence, the finite normal local bound and all LocBridge fields. Prove finite coefficient DVR, residue, fraction and adic-completeness laws for its actual integer ring.",
      ["NR1", "NR2"], many("emb", ["finiteDimensional_adjoin_range", "adjoin_range_subset_closure", "mem_GK_iff", "exists_restrict", "exists_mulEquiv", "exists_locBridge"]) +
      many("bridge", ["LocBridge"]) + many("ints", ["dvd_iff_norm_le", "isAdic_maximalIdeal", "finite_residueField", "integers_laws"]),
      LOCAL + ["The prescribed IsPlaceOver A v and v above l; compact Hausdorff profinite Galois groups"])
claim(4, "Discrete values of the prime-to-l root field",
      "Frobenius congruences and closed finite root rings prove that every nonzero element of the source's maximal unramified algebraic subfield has norm in l^Z.",
      [], many("unram", ["rootRing", "rootRing_eq_span_roots_of_unity", "norm_le_one", "isClosed_rootRing", "exists_pow_prime_pow_eq_add_prime_mul", "pow_prime_pow_totient_eq_self_of_pow_eq_one", "pow_sub_mem", "exists_eq_mul", "norm_rootRing", "exists_mul_mem", "norm_of_mem_Kur", "norm_of_mem_unramified_subfield"]),
      LOCAL + ["Compactness of Z_l and the prime-to-l root definition of MaximalUnramifiedExtension"])
claim(5, "A complete discrete valuation ring with algebraically closed residue",
      "For finite L0, the completed field L0 U_l has a discrete norm gap and a complete DVR integer ring, with algebraically closed residue, exact adic topology and the source's closure identity.",
      ["NR4", "LS8"], many("complete", ["norm_le_one_of_root", "ints", "div_mem_ints", "dvd_iff", "not_isUnit_iff", "irreducible_unif", "isDVR", "mem_pow_iff", "isAdic", "isAlgClosed_res", "coe_ints_closure", "exists_pow_norm", "exists_unif", "exists_integers_completion"]),
      LOCAL + ["C_l algebraically closed; residue-root lifting as in LS8; finite field norm formula"])
claim(6, "Bounded coefficients for an algebraic adjunction after completion",
      "The closure of F(z) equals Fhat(z), and every norm-at-most-one element has uniformly bounded coefficients in finitely many powers of z, using a complement to the coefficient-map kernel.",
      [], many("coeff", ["closure_adjoin_unitBall_coeff_bound"]),
      LOCAL + ["F contains Q_l; z algebraic over Q_l; finite-dimensional norm equivalence over the complete field Fhat"])
claim(7, "Finite cyclotomic DVR towers and exact denominator generation",
      "Construct the finite complete DVR extension O_k of O, a primitive l^k root and the literal Ok_gen assertion for every fraction-field element; no unproved monogenic integral-basis assertion is used.",
      ["NR5", "NR6"], many("cyclo", ["mem_clC", "coe_clC", "clC_mono", "clC_props", "muK_spec", "exists_cyclotomic_integers"]) + many("ring", ["ok_laws"]),
      LOCAL + ["K0 and Lw finite local subextensions; k is an arbitrary natural number"])
claim(8, "Principal units and infinite components vanish in finite l-primary characters",
      "Continuous finite l-primary characters kill principal units at residue characteristic different from l and kill all complex infinite components, giving one common congruence subgroup under the exact unramified-at-l condition.",
      [], many("ringclass", ["dvd_pow_pow_sub_one", "tendsto_pow_pow", "exists_nat_coprime", "tame", "map_finPartI", "map_congr_unit"]),
      ["E totally complex; finite l-primary character with open kernel; unramified outside Q and at every prime above l"])
claim(9, "Finite idelic congruence quotient",
      "Diagonal E* and the principal-unit congruence subgroup at finite Q have finite index, by finite residue-unit quotients and the ideal class group.",
      [], many("ringclass", ["red", "red_eq_one", "finiteIndex_of_congr"]) + many("unitindex", ["finiteIndex_unitIdl_sup"]),
      ["Number-field prime completions and finite residue fields; classical finiteness of the ideal class group"])
claim(10, "The universal anticyclotomic kernel is open and finite index",
      "The intersection of all exact permitted finite l-primary anticyclotomic kernels has finite index through the common Artin-congruence quotient; only then a finite-intersection argument proves openness and l-primary quotient.",
      ["NR8", "NR9"], many("ringclass", ["IsRingKer", "ringKer", "mem_ringKer", "isRingKer_top", "IsRingKer.inf", "finiteIndex_ringKer", "isRingKer_ringKer", "finite_ringClass", "isOpen_ker_art", "pow_eq_one"]) + many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]),
      CFT + ["Fixed conjugation c; finite Q; all permitted characters unramified also above l"])
claim(11, "Actual universal finite anticyclotomic quotients and restrictions",
      "Construct every finite RCG and surjective open-kernel Artin map, l-primary and anticyclotomic laws, and restriction maps. The universal assertion retains the literal condition that Q avoid l.",
      ["NR10"], many("ringclass", ["RingClass", "art", "art_surjective", "art_anti", "art_unram", "art_universal", "ringKer_anti", "res", "res_comp_art", "ringClass_laws", "exists_ringClass_host"]),
      CFT + ["No nontriviality or exact nonempty ramification of the quotient is asserted"])
claim(12, "Uniform local lower bound and compatible abstract complex readings",
      "Choose c0(l,j) before b0,b1,Sx, containing j(K), mu_l and the finite normal bridge fields; construct compatible complex isomorphisms of Qbar_l and C_l by countable-field transcendence bases.",
      ["NR3"], many("low", ["finiteDimensional_muK_one", "bridgeLow", "low", "exists_low"]) +
      many("ring", ["exists_ringEquiv_over", "card_padicAlgCl", "card_padicComplex", "exists_padicBaseField_integral_places"]),
      LOCAL + ["Fixed K number field; algebraic closedness of C_l; chosen places of the same Omega above host primes"])
claim(13, "Actual normalized characters and exact Read exponents",
      "Install GA16's normalized delta and both-sided chi1 into the actual finite base ring, with inverse Frobenius and NC.Read exponents 0 and -r; retain the literal natural-index reindexing and frame-value containment.",
      ["NR12", "GA6", "GA11", "GA12", "GA16", "HF11", "HF13", "HF16"],
      many("ring", ["hc_at", "vals_block", "vals_zero", "frob_read", "read_of_isGal"]) +
      many("avatars", ["hostHeckeFrame_twist_galois_characters", "galois_characters_of_artin"]) +
      many("frame", ["ValLL0"]),
      FIXED + CFT + LOCAL + ["r odd, m>=1 and the actual side embeddings; no global K enlargement"])
claim(14, "Actual nonempty all-prime TwR family",
      "Construct every TwR field with Tw=Spec1(O_K), literal b0/b1 coefficient rings, cyclotomic towers, normalized characters, exact finite excluded set and universal ring-class quotients. Every index has actual order-15 auxiliary inertia.",
      ["NR1", "NR3", "NR7", "NR11", "NR13"],
      many("twr", ["TwR"]) + many("ring", ["exists_prime_mem", "placesOver_nonempty", "exists_toClC", "exists_ringSpec"]) +
      many("cminvol", ["isAlgebraic_rat", "exists_isCMConjOm"]),
      FIXED + CFT + ["b0 dominates c0 pointwise; b1 arbitrary finite extension family; Sx finite"])
claim(15, "Every RingSpec field on the prescribed fixed global data",
      "Prove the full exists_ringSpec endpoint with exact j0=J, K0=b0 and Lw=b1, all bridge and coefficient squares, exact excluded set, all Read/value/eta/delta laws and the original quantifier order.",
      ["NR12", "NR13", "NR14", "HF11"], many("spec", ["RingSpec"]) +
      many("ring", ["mem_OL_iff", "mem_maximalIdeal_OL_iff", "exists_equiv_intOf", "placesOver_inj", "eta_unitArg", "exists_ringSpec"]),
      FIXED + CFT + ["Prescribed J_q with exact center law, constructed by NR1 if not given", "b0 dominates c0; arbitrary b1 and finite Sx"])
claim(16, "The same prime center determines the entire valuation ring",
      "Equality of positive centers on O_K for a number-field valuation and a DVR embedding implies exact integrality equivalence for every element of K, by localization fractions and unit denominators.",
      [], many("cover", ["vRing", "v_nonneg_int", "emb_int_mem", "exists_frac_compl", "cen", "mem_cen", "cen_isPrime", "v_nonneg_iff"]),
      ["K number field; nonzero prime center; supplied DVR embedding with exactly the same positive center"])
claim(17, "Exact all-place SidePl true and TwCover coefficient coverage",
      "The RingSpec constructed above supplies, for every actual place w of L, an index i with l(i)=resChar(w) and the full SidePl(w,i,true) equivalence; its positive-center form gives TwCover.",
      ["NR15", "NR16"], many("cover", ["exists_setting_of_place"]) +
      many("spec", ["SidePl"]) + many("ntw", ["TwCover"]) +
      [interface_range("side", "GlobalTheory.HeightCounting.SideB.cover", 191, 191, "exact coefficient clause within SideB; other fields not supplied")],
      ["Actual RingSpec and the unchanged coefficient-place system of D; no nonzero row assumption needed for coefficient coverage"])
claim(18, "A Reading inducing any prescribed full coefficient-field place",
      "Given the actual SidePl index and side, extend the matching K-completion embedding to a Q_l-automorphism, then choose a complex reading agreeing on all of L; obtain the exact Reading.Induces clause without changing O0 or its embedding.",
      ["NR1", "NR2", "NR12", "NR17"], many("prime", ["exists_embAt"]) + many("emb", ["norm_eq_of_le_one_iff", "exists_algEquiv", "norm_algEquiv"]) +
      many("triple", ["Reading", "Reading.Induces", "Reading.nonempty"]) + many("spec", ["SidePl"]),
      LOCAL + ["K subset L number fields with fixed epsilon", "Actual SidePl for the selected coefficient index and side", "For NTw notation, any later installation retains these actual coefficient rings and embeddings", "Standard extension of a finite separable-field embedding to its algebraic closure"])
claim(19, "Countable cofinal finite local fields through Krasner's inequality",
      "A dense embedded global Qbar and the strict conjugate-distance argument give a countable family of finite Q_l fields containing every finite subset of Qbar_l.",
      ["NR2"], many("compact", ["exists_mem_adjoin_simple", "exists_countable_family"]),
      LOCAL + ["Separable algebraic closure and its fixed-field theorem; countability of global Qbar"])
claim(20, "One finite coefficient field for a compact continuous representation",
      "Closed entry-and-inverse subgroups in a countable field cover, Baire, and finite coset representatives put every matrix entry in a single finite extension containing any prescribed initial finite extension.",
      ["NR19"], many("compact", ["entrySubgroup", "exists_finiteDimensional_entries_mem", "exists_finExt_entries_mem"]),
      LOCAL + ["Compact Hausdorff topological group; finite matrix rank and continuous entries; Baire theorem"])
claim(21, "Stable integral lattice and actual integral conjugation",
      "The sum of translates of O^n is contained in one bounded fractional lattice, hence finite free and stable; its basis gives the full exists_finExt_conj_intOf conclusion, including continuous integral inverse matrices.",
      ["NR20", "GA3"], many("lattice", ["norm_sum_le_one", "intSubgroup", "isOpen_intSubgroup", "exists_finExt_conj_intOf"]) +
      many("rho", ["isRepOf_conj", "restrictRep", "intOf_mono", "conjIntegral"]),
      LOCAL + ["Compact Hausdorff source group and a continuous finite-dimensional Qbar_l representation; no identification with a preinstalled residual model"])
claim(22, "Exact scalar twist of an existing cuspidal Galois representation",
      "Under GalEx, the avatar of eta^-1 abs^-t/2 scalar-twists the rank-r representation to the actual pi tensor etaTinv at shift (1-nV)/2; continuity, semisimplicity and Frobenius polynomials are proved.",
      ["GA6", "GA11", "GA13"], many("twist", ["exists_isRepOf_tw"]) + many("reps", ["IsRepOf", "GalEx"]) +
      many("rho", ["twistEx"]),
      CFT + ["Same actual SideA, GalEx, conjugate-self-dual regular algebraic cuspidal pi of rank r", "Actual r+t=nV, odd t and eta half-integral infinity type"])
claim(23, "Representation invariance under exact readings and split comparison",
      "Cofinite K-valued Frobenius polynomials preserve the same representation under any reading agreeing on K; Q_l coefficient automorphisms transport it; actual split Frobenius density transfers its characteristic polynomials to any matching supplied parameter.",
      ["NR2", "RC4"], many("rho", ["isRepOf_conj", "isRepOf_map", "isRepOf_of_read", "isRepOf_of_split"]) + many("reps", ["IsRepOf", "RowCusp"]),
      ["Both exact coefficient readings agree on the same embedded K", "Supplied cofinite K-polynomials", "For split comparison, the literal ChebSplit and both supplied continuous representations"])
claim(24, "Uniform integral row family and simultaneous all-prime realization",
      "Construct c1(l,j) before all RingSpec choices, and the actual continuous O0-valued rho_rows family for every good occurring row and both sides, universally for all compatible fraction/complex readings; join with c0 on the unchanged global D while retaining genuine form/residual/local compatibility.",
      ["NR12", "NR15", "NR18", "NR21", "NR22", "NR23", "GA1", "GA2", "GA3"],
      many("rho", ["core", "GoodOcc", "pickL", "pickRho", "pick_spec", "starRestrictSubfield", "jSide", "cBig", "pickL_le", "kap", "kap_alg", "twistFractionFieldToPadicAlgebraicClosure_padicInt", "kap_emb0", "rho_rows"]) +
      many("reps", ["GalEx", "RowCusp"]) + many("second", ["second_step"]) +
      many("mt", ["MtReal", "MtFam"]) + many("mtad", ["MtAd"]) +
      many("triple", ["IsParam", "IsResidual", "IsChars", "IsTripleWith", "IsTripleFor"]) +
      many("twr", ["TwF", "TwL", "TwR.ntw"]) + many("side", ["MtInput", "SideB"]),
      FIXED + CFT + REP + ["Finite actual row-type set", "Full SideB, MtFam/MtAd, form and tuple ties, fixed residual/Hecke labels and nonempty LocsCover are not concluded"])


completed = []


def done(key, name, ids, conditions, scope="literal conditional endpoint"):
    completed.append({
        "endpoint": name, "claim_ids": ids,
        "status": "completed_conditionally", "scope": scope,
        "conditions": conditions, "source": source(key, name),
    })


done("prime", "exists_embAt", ["NR1"], ["Number field K, finite prime q over l and standard local-completion embedding facts"])
done("emb", "exists_embedding", ["NR1"], ["Chosen valuation ring of the global algebraic closure above the prescribed prime over l"])
done("emb", "denseRange_embedding", ["NR2"], ["Algebraically closed source field and an embedding into Qbar_l"])
done("emb", "norm_eq_of_le_one_iff", ["NR2"], ["Same pulled-back valuation ring and the normalized l-adic norms"])
done("emb", "exists_algEquiv", ["NR2"], ["Dense first embedding and equal normalized norms; extension made in C_l before restricting"])
done("emb", "exists_mulEquiv", ["NR3"], ["Exact prescribed-place embedding; Kw=Q_l(j(E))"])
done("emb", "exists_locBridge", ["NR3"], ["Actual place of E above l and chosen valuation ring on Omega; all larger finite coefficient fields"])
done("ints", "integers_laws", ["NR3"], LOCAL + ["Finite local field; O0 is its actual integral closure/unit ball"])
done("unram", "norm_of_mem_Kur", ["NR4"], ["Nonzero element of the source's prime-to-l cyclotomic unramified field"])
done("unram", "norm_of_mem_unramified_subfield", ["NR4"], ["Nonzero element in the stated finite unramified subfield"])
done("complete", "exists_integers_completion", ["NR5"], LOCAL + ["Finite L0; algebraic closedness of C_l and residue-root lifting"])
done("coeff", "closure_adjoin_unitBall_coeff_bound", ["NR6"], LOCAL + ["F contains Q_l and z is algebraic over Q_l"])
done("cyclo", "exists_cyclotomic_integers", ["NR7"], LOCAL + ["Actual finite K0,Lw and arbitrary k in N"])
done("ringclass", "tame", ["NR8"], ["Finite l-primary target with open kernel, local residue characteristic different from l"])
done("ringclass", "finiteIndex_of_congr", ["NR9"], ["Subgroup contains diagonal E* and exact finite-set principal-unit congruences; ideal class group finite"])
done("ringclass", "finiteIndex_ringKer", ["NR10"], CFT + ["Totally complex E, prime l, finite Q and exact permitted kernel family"])
done("ringclass", "isRingKer_ringKer", ["NR10"], ["Finite index of the universal kernel; finite intersections preserve the permitted character laws"])
done("ringclass", "ringClass_laws", ["NR11"], CFT + ["Exact off-l universal property; no nontriviality or prescribed exact ramification asserted"])
done("ringclass", "exists_ringClass_host", ["NR11"], CFT + ["Actual host and conjugation; any supplied index/prime family"])
done("low", "exists_low", ["NR12"], LOCAL + ["Fixed D, every prime l and embedding j; finite normal bridge bounds"])
done("ring", "exists_padicBaseField_integral_places", ["NR12"], LOCAL + ["Fixed D and its chosen places; c0 precedes all larger coefficient choices"])
done("ring", "read_of_isGal", ["NR13"], CFT + ["Exact compatible field reading, normalized IsGal and the stated cofinite value formula with its exponent"])
done("ring", "exists_ringSpec", ["NR14", "NR15"], FIXED + CFT + ["Prescribed prime-compatible J, supplied by NR1 when needed; exact c0-before-b0/b1/Sx order"])
done("cover", "v_nonneg_iff", ["NR16"], ["Same nonzero prime center on O_K for the actual valuation and DVR embedding"])
done("cover", "exists_setting_of_place", ["NR17"], ["Actual RingSpec; same D coefficient-place system"], "literal coefficient coverage endpoint, not all of SideB")
done("compact", "exists_mem_adjoin_simple", ["NR19"], LOCAL + ["Dense algebraically closed image and the strict Krasner-distance argument"])
done("compact", "exists_countable_family", ["NR19"], LOCAL + ["Countable global algebraic closure and finite subsets"])
done("compact", "exists_finiteDimensional_entries_mem", ["NR20"], LOCAL + ["Compact Hausdorff group, finite rank and continuous matrix entries; Baire theorem"])
done("compact", "exists_finExt_entries_mem", ["NR20"], LOCAL + ["Same compact representation and any given finite lower-bound field"])
done("lattice", "exists_finExt_conj_intOf", ["NR21"], LOCAL + ["Compact continuous representation; exact stable lattice construction"])
done("twist", "exists_isRepOf_tw", ["NR22"], CFT + ["Literal SideA and GalEx, actual rank-r conjugate-self-dual regular algebraic pi and nV=r+t"])
done("rho", "isRepOf_of_read", ["NR23"], ["Both readings agree on the same j(K); exact cofinite K-polynomial premise"])
done("rho", "isRepOf_map", ["NR23"], ["Actual Q_l coefficient automorphism and the correspondingly composed complex reading"])
done("rho", "isRepOf_of_split", ["NR23"], ["Actual ChebSplit, both supplied representations and exact split-local parameter agreement"])
done("rho", "core", ["NR21", "NR22", "NR23", "NR24"], CFT + REP + ["Actual good occurring row and fixed l,j"])
done("rho", "rho_rows", ["NR24"], FIXED + CFT + REP + ["Finite actual row family; arbitrary actual RingSpec with b0 containing c1", "Universal output for every compatible fraction and complex reading"])


targets = [
    {
        "id": "NR-next-01", "title": "Contain the actual common character-value field in the fixed global K",
        "scope": "HF16 constructs a finite common frame-value field; NR15 retains ValLL0 for the already specified K=LL0. Supply that exact containment or a coherent transport of every dependent global object. Local coefficient enlargement b0,b1 cannot enlarge the fixed K or its epsilon.",
        "sources": many("frame", ["ValLL0"]) + many("values", ["frame_values", "exists_of_emb"]),
        "discharged_subscope": ["Prescribed prime embeddings J at every q", "Actual nonempty all-prime RingSpec under the fixed-field value hypothesis", "SidePl coefficient cover and full-place inducing Reading"],
    },
    {
        "id": "NR-next-02", "title": "The exact global reciprocity input",
        "scope": "Retain GlobalArtinReciprocity with its source quotient, kernel, inertia and inverse-Frobenius laws. The finite universal anticyclotomic quotients are now proved from that input, including their exact restriction at primes above l.",
        "sources": many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]),
        "discharged_subscope": ["Actual finite universal RCG and transition maps", "Normalized character realization from the retained reciprocity input, by GA"],
    },
    {
        "id": "NR-next-03", "title": "Genuine cuspidal Galois and row-parameter existence",
        "scope": "Supply literal GalEx and RowCusp on the same automorphic package, including cofinite K-polynomials, and the stated ChebSplit. The actual source route to GalEx uses LocalLanglandsGL, AutomorphicFormsFiniteGL, GaloisRepOfPolarizedCuspidal and a genuine CGTrue. Compact descent and stable lattices do not create those representations or row parameters.",
        "sources": many("reps", ["IsRepOf", "GalEx", "RowCusp"]) + many("galex", ["CGTrue.galEx", "galEx_of_cgTrue"]) + many("cheb", ["chebSplit", "chebSplit_nd"]),
        "discharged_subscope": ["Exact eta scalar twist of every supplied GalEx representation", "Single finite coefficient field and integral lattice for each compact representation", "Full bounded rho_rows family and all-reading compatibility under these inputs"],
    },
    {
        "id": "NR-next-04", "title": "Actual adelic form spaces, lattices, weights and full SideB",
        "scope": "Construct the actual MtFam/MtReal with full TypeSp range, the MtInput and RatDat/RatIn integral Hecke lattices, and MtAd's exact pointwise, rational-group, weight and finite-matrix identities for the fixed read. Then reconstruct remaining second_step suppliers, including genuine weight and signature spaces. ExistsMotiveAdjointWithLevels.mtAd_L transports an already supplied MtAd; it is not an initial constructor.",
        "sources": many("mt", ["MtReal", "MtFam", "HeckeTied", "HeckeRational", "AVTied"]) +
                   many("mtad", ["MtAd", "RatAd", "SerAt"]) +
                   many("side", ["MtInput", "RatIn", "SideB"]) +
                   many("second", ["second_step"]) + many("weights", ["wt_weights"]) +
                   many("mttransport", ["mtAd_L"]),
        "discharged_subscope": ["Actual RingSpec constructor", "Exact SideB.cover coefficient clause", "Conditional bounded row Galois representations", "No zero-form or empty-Sig substitute used"],
    },
    {
        "id": "NR-next-05", "title": "Toric installation and characters with genuinely required ramification",
        "scope": "Supply the actual toric character grid, its fixed-field values and RatioConj for exists_twL_installed, and separately any required nonempty-support IsPsi with exact ramification and trivial action on the whole l-decomposition group. The proved RCG universal property alone gives neither exact ramification nor decomposition triviality.",
        "sources": many("twr", ["TwL", "TwR.ntw"]) + many("toric", ["exists_twL_installed"]) +
                   many("frame", ["CharFrame"]),
        "discharged_subscope": ["Actual RCG for every finite Q with off-l universality", "Actual delta auxiliary inertia of order 15", "All coefficient rings and cyclotomic roots needed by a later toric installation"],
    },
    {
        "id": "NR-next-06", "title": "Genuine IsTripleWith and IsTripleFor on installed signatures",
        "scope": "For the actual nonempty signatures, prove exact occurring row/IsParam, the scalar equation with already installed rhoS, all hEig equations, residual characteristic-polynomial and Teichmuller identities, fixed chiT calibration and sig_all coverage. NR18 proves Induces and NR24 gives conditional integral row representations; those facts do not identify arbitrary installed signature or residual data.",
        "sources": many("triple", ["IsParam", "IsResidual", "IsChars", "IsTripleWith", "IsTripleFor"]) +
                   many("empty", ["TameTie", "exists_tameTie", "exists_isTripleOf"]) + many("twr", ["TwF"]),
        "discharged_subscope": ["Reading inducing the prescribed full-L place", "Normalized characters under exact frame containment", "Uniform coefficient and integral-representation primitives", "Empty-local exists_isTripleOf is explicitly not the required join"],
    },
    {
        "id": "NR-next-07", "title": "Compatible nonempty local indices and actual choice/form/tuple joins",
        "scope": "Construct the local NData/NTw indices and LocsCover, genuine Mt comparison and exact normalized local characters for the same forms, tuple xi/psi/Q and coefficient squares. Preserve RankTie, LocsCarry, MuIsW and the actual ColW/Pre2/St/RowPk compatibility from NC/RC/AR unless independently supplied. TwR itself has no local form slots and its ntw constructor requires a separate actual form/toric installation.",
        "sources": many("ntw", ["NData", "LocsCover", "NTw"]) + many("twr", ["TwF", "TwL", "TwR.ntw"]) +
                   many("side", ["ChoiceSide", "SideB", "TwNew"]),
        "discharged_subscope": ["Nonempty all-prime twist-ring family", "SidePl/TwCover coefficient coverage for every original place", "Full-place inducing readings without global field replacement"],
    },
]


def record_audit(key, name, claim_ids, groups):
    s = source(key, name, "literal record declaration for the field audit")
    lines = blob(s["path"]).decode().splitlines()
    body = lines[s["line_start"]:s["line_end"]]
    fields = []
    for line in body:
        m = re.match(r"^  (?:\[)?([\w'₂]+)\s*:", line)
        if m:
            fields.append(m.group(1))
    assert fields and len(fields) == len(set(fields)), (key, name, fields)
    flat = [field for g in groups for field in g["fields"]]
    assert sorted(flat) == sorted(fields), (key, name, "missing", set(fields)-set(flat), "extra", set(flat)-set(fields))
    return {"record": s["declaration"], "claim_ids": claim_ids, "source": s,
            "field_count": len(fields), "includes_instance_fields": True,
            "fields": fields, "proof_groups": groups}


audits = [
    record_audit("bridge", "LocBridge", ["NR3"], [
        {"claim_ids": ["NR3"], "fields": ["Kw", "j", "j_E", "j_dense", "e", "e_cont", "e_symm_cont", "e_comm", "LL", "LL_split", "eO", "eO_alg", "eO_cont", "eO_symm_cont"], "reason": "Chosen-place local field and decomposition equivalence; finite normal closure; identity coefficient ring map"},
    ]),
    record_audit("twr", "TwR", ["NR14"], [
        {"claim_ids": ["NR1", "NR14"], "fields": ["cc", "cc_cm", "Tw", "l", "lPrime"], "reason": "All finite K primes; actual pulled-back CM conjugation"},
        {"claim_ids": ["NR3", "NR14"], "fields": ["O0", "crO0", "twistBaseCoefficientRing_isDomain", "twistBaseCoefficientRing_isDVR", "algO0", "twistBaseCoefficientRing_finite_padic", "twistBaseCoefficientRing_residueField_finite", "topO0", "twistBaseCoefficientRing_topologicalRing", "twistBaseCoefficientRing_isAdic", "emb0", "emb0b", "restX_coefficientEmbedding_conj"], "reason": "Exact finite local integer ring and J/star coefficient embeddings"},
        {"claim_ids": ["NR5", "NR7", "NR14"], "fields": ["O", "crO", "domO", "dvrO", "algO", "O_inj", "O_l", "topO", "trO", "O_adic", "resO_ac", "O_complete", "Ok", "crOk", "domOk", "dvrOk", "algOk", "Ok_inj", "Ok_fin", "zk", "zk_prim", "Ok_gen"], "reason": "Explicit completed unramified/cyclotomic integer rings, actual inclusions, primitive roots and denominator generation"},
        {"claim_ids": ["NR13", "NR14", "GA16"], "fields": ["pD", "pD_eq", "delta", "delta_open", "delta_anti", "delta_ram", "delta_15", "delta_tame", "chi1", "twistCharacterFamily_continuous", "twistCharacterFamily_unramified", "twistCharacterFamily_at_auxiliaryPlaces", "twistCharacterFamily_tame"], "reason": "Actual normalized avatars and literal all-natural-index reindexing"},
        {"claim_ids": ["NR14"], "fields": ["S0", "twistExcludedPlaces_contains_residueChar", "placesOver_subset_exceptional", "primes_subset_exceptional"], "reason": "Exact finite union over residue, type, both auxiliary primes and Sx"},
        {"claim_ids": ["NR10", "NR11", "NR14"], "fields": ["RCG", "grpRCG", "finRCG", "RCG_l", "art", "art_surj", "art_cont", "art_anti", "art_unr", "art_univ", "res", "res_art"], "reason": "Actual finite universal quotient and restriction maps, with exact off-l universal scope"},
    ]),
    record_audit("spec", "RingSpec", ["NR15"], [
        {"claim_ids": ["NR1", "NR3", "NR7", "NR12", "NR15"], "fields": ["eTw", "pl_emb", "K0", "eO0", "j0", "Lw", "eO", "eOk", "iCq", "ringSpec_baseExtension_lowerBound", "Lw_big", "ringSpec_baseIntegersEquiv_algebraMap", "ringSpec_baseEmbedding_compatible", "eO_alg", "eOk_alg", "mu_g", "ringSpec_excludedPlaces_eq", "br", "br_ind"], "reason": "Identity all-prime indexing, exact b0/b1/J fields, actual inclusion squares and prescribed-place bridges"},
        {"claim_ids": ["NR13", "NR15", "HF11"], "fields": ["mu0H", "etaH", "delH", "embO", "del_fix", "delta", "chi1", "ringSpec_sidedEmbedding_fixedField", "etaT_unr", "etaT_inf", "eta_eq", "ringSpec_normalisedCharacter_eq", "del_eq", "iCq_embO", "embO_star", "deltaRead"], "reason": "Literal original frame characters, exponents 0/-r, exact field inclusions and inverse Frobenius at every permitted unramified prime"},
    ]),
    record_audit("triple", "Reading", ["NR18"], [
        {"claim_ids": ["NR18"], "fields": ["κ", "ι", "κ_alg", "read"], "reason": "Canonical O0 fraction embedding and complex field isomorphism agreeing on all of L; Induces proved separately"},
    ]),
]

all_sources = [s for c in claims for s in c["sources"]]
unique_ranges = {(s["path"], s["line_start"], s["line_end"], s["range_sha256"]) for s in all_sources}
claim_ids = {c["id"] for c in claims}
for c in claims:
    for dep in c["depends_on"]:
        if re.fullmatch(r"NR\d+", dep):
            assert dep in claim_ids, (c["id"], dep)
graph = {c["id"]: [d for d in c["depends_on"] if d in claim_ids] for c in claims}
visiting, visited = set(), set()
def visit(cid):
    assert cid not in visiting, ("dependency cycle", cid)
    if cid in visited:
        return
    visiting.add(cid)
    for dep in graph[cid]:
        visit(dep)
    visiting.remove(cid)
    visited.add(cid)
for cid in graph:
    visit(cid)

reviews = []
for name, expected in [
    ("nonempty_realization_NR1_18_review.json", [f"NR{i}" for i in range(1, 19)]),
    ("nonempty_realization_NR19_24_review.json", [f"NR{i}" for i in range(19, 25)]),
]:
    path = ROOT.parent / "reviews_v0_21" / name
    if path.exists():
        raw = path.read_bytes()
        data = json.loads(raw)
        mapped = data["reviewed_claims"]
        for cid in expected:
            item = mapped[cid]
            actual = item if isinstance(item, str) else item.get("paragraph_sha256", item.get("sha256", item.get("proof_paragraph_sha256")))
            assert actual == paragraphs[cid]["sha256"], ("review paragraph hash mismatch", path, cid, actual, paragraphs[cid]["sha256"])
        assert data.get("reviewer") == "/root" and data.get("author") == "/root/class_rank"
        reviews.append({"file": "reviews_v0_21/"+name, "sha256": sha(raw),
                        "expected_claim_ids": expected, "bound_current_claim_ids": expected,
                        "reviewer": data["reviewer"], "author": data["author"]})

manifest = {
    "component": "nonempty_realization", "version": "0.21", "commit": COMMIT,
    "repository": URL, "source_files": [
        {"path": path, "sha256": sha(raw), "bytes": len(raw),
         "line_count": len(raw.splitlines()), "verified_equal_to_pinned_git_blob": True,
         "url": f"{URL}/blob/{COMMIT}/{path}"}
        for path, raw in sorted(cache.items())
    ],
}
provenance = {
    "component": "nonempty_realization", "version": "0.21", "claim_prefix": "NR",
    "source_commit": COMMIT, "repository": URL,
    "scope": "Actual nonempty all-prime TwR/RingSpec, complete discrete coefficient towers, universal finite anticyclotomic quotients, full-place readings and exact coefficient SideB.cover; compact-representation finite descent and stable lattices yield the literal bounded rho_rows supplier under retained GalEx/RowCusp/ChebSplit. Fixed global value containment, reciprocity and genuine form/residual/nonempty-local compatibility remain explicit.",
    "main_sha256": sha(main), "report_sha256": sha(report),
    "builder_sha256": sha(Path(__file__).read_bytes()),
    "claims": claims, "completed_source_endpoints": completed,
    "record_field_audits": audits,
    "derived_additional_implications": [{
        "claim_id": "NR18", "status": "proved_conditionally",
        "statement": "Every actual SidePl index and side admits a Reading inducing that prescribed full-L place, using the same O0 and sided K embedding.",
        "source_scope": "Human consequence of the pinned prime-embedding/completion primitives and the exact Reading.Induces interface; not mislabelled as an identically named source theorem.",
    }, {
        "claim_id": "NR24", "status": "proved_conditionally",
        "statement": "The compositum c0*c1 is chosen before all coefficient rings and supplies the same all-prime RingSpec and bounded row matrices, universally for the full-place readings constructed in NR18.",
        "not_claimed": "A full SideB, MtFam/MtAd, IsTripleFor or nonempty LocsCover/NTw form installation",
    }],
    "remaining_targets": targets, "independent_reviews": reviews,
    "counts": {
        "claims": len(claims), "claim_source_links": len(all_sources),
        "distinct_claim_ranges": len(unique_ranges), "indexed_source_files": len(cache),
        "completed_source_endpoints": len(completed), "remaining_supplier_families": len(targets),
        "record_fields_audited": sum(a["field_count"] for a in audits),
        "record_audits": len(audits),
    },
    "verification": {
        "git_objects_only": True, "source_checkout_unchanged": True,
        "old_components_unchanged": True, "lean_compiled": False, "pdf_generated": False,
        "hypothesis_policy": "Every completed endpoint is conditional on the literal compatible inputs. New TwR data preserve the original host/rows/global fields and do not silently replace an installed arbitrary NTw or its dependent form/residual/local objects.",
    },
}
next_targets = {
    "component": "nonempty_realization", "version": "0.21", "commit": COMMIT,
    "scope": provenance["scope"], "completed_endpoints": completed,
    "next_targets": targets,
}
for name, obj in [("provenance.json", provenance), ("source_manifest.json", manifest), ("next_targets.json", next_targets)]:
    (ROOT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+"\n")
lines = ["NONEMPTY REALIZATION SOURCE LOCATORS -- NR1--NR24", "Pinned commit: "+COMMIT,
         "Inclusive line ranges; hashes use exact Git blob bytes including line endings.", ""]
for c in claims:
    lines.extend([c["id"]+" "+c["title"], "TeX paragraph SHA-256: "+paragraphs[c["id"]]["sha256"]])
    for s in c["sources"]:
        lines.extend(["  "+s["declaration"], f'  {s["path"]}:{s["line_start"]}-{s["line_end"]}',
                      "  full SHA-256 "+s["full_file_sha256"], "  range SHA-256 "+s["range_sha256"], "  "+s["url"]])
    lines.append("")
lines.append("Completed endpoints: "+str(len(completed))+"; remaining supplier families: "+str(len(targets)))
(ROOT/"source_locators.txt").write_text("\n".join(lines)+"\n")
print(json.dumps(provenance["counts"], sort_keys=True))


