#!/usr/bin/env python3
"""Rebuild GA provenance from pinned Git blobs without checkout mutation."""
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
P = {
 'coef': IW+'EmbeddingClosedIntegral.lean',
 'products': IW+'IsOpenConnectedComponentOfOneInf.lean',
 'openker': IW+'IsOpenKerOfInfConn.lean',
 'finiteker': AM+'IsOpenKerFinIdele.lean',
 'artin': AB+'PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',
 'avatar': IW+'UniversalAnticyclotomicCharacterLaws.lean',
 'main': IW+'InertialOrderFifteenCharAuxiliaryPrimeSpec.lean',
 'cmtype': IW+'BijectiveCmType.lean',
 'block': ND+'CharpolySmulOfProd.lean',
 'first': IE+'FirstTwistCharacterEqLadicHeckeCharacter.lean',
 'reading': ND+'IsCharsOfReading.lean',
 'normv': IW+'NormVEqAbsNorm.lean',
 'conj': IW+'IsPlaceOverMoveValConjPl.lean',
 'wildunits': IW+'ValuedPowSubOneLtOne.lean',
 'tamegen': IW+'MemZpowersOfTameGen.lean',
 'sqgen': IW+'ExistsGeneratorSqEqOfSqMemZpowers.lean',
 'dense': IW+'DenseRangeUnits.lean',
 'normemb': IW+'NormEmbeddingIntegerLeOne.lean',
 'extension': IW+'ExistsContinuousExtensionAdicCompletion.lean',
 'placeeq': IW+'PlaceEqOfContEmbCompEq.lean',
 'hostchar': UN+'CharHost.lean',
 'chartied': UN+'CharTied.lean',
 'chargal': UN+'CharGal.lean',
 'normread': 'src/Formalism/LocalToGlobal/NormalizedHeckeFactors/RingSpecSidedEmbeddingFixedField.lean',
 'chidef': 'src/Formalism/LocalToGlobal/NormalizedHeckeFactors/ChiDefs.lean',
 'sideb': AM+'RingSpecNormalisedCharacterEq.lean',
 'ntw': 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataN.lean',
 'ranks': 'src/Formalism/LocalRingCardinality/Params.lean',
 'unr': IW+'HeckeCharacterUnramifiedAeAndExistsLevel.lean',
 'localres': IW+'ExistsNatCongrOfAbsNormPrime.lean',
 'split': IW+'CompletelySplitPrimeHostPlaceProperties.lean',
 'hostcm': IW+'HostCmEmbeddingProperties.lean',
 'readexists': IW+'ExistsPadicAlgClRingEquivComplexCompEqOfCountabl.lean',
 'isGaldef': IE+'PolarizedGaloisRep.lean',
 'choice': IE+'ExistsTiedChoiceOfReads.lean',
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


main = (ROOT / "main.tex").read_bytes()
report = (ROOT / "report.txt").read_bytes()
tex = main.decode()
assert not [c for c in tex if ord(c) < 32 and c not in "\n\r\t"]
markers = list(re.finditer(r"(?m)^\\paragraph\{(GA\d+):", tex))
assert [m.group(1) for m in markers] == [f"GA{i}" for i in range(1, 24)]
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
    cid = f"GA{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.20", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "adic_realization/main.tex",
            "expanded": "adic_realization/report.txt",
            "section": cid, **paragraphs[cid],
        }, "sources": sources,
    })


COEF = [
    "O is a domain DVR finite over Z_l with the actual maximal-ideal-adic topology",
    "The fraction embedding kappa into Qbar_l agrees with Z_l",
]
CFT = [
    "The supplied IsGlobalArtin map, including open quotient, kernel, inertia, inverse-arithmetic-Frobenius and decomposition clauses",
    "E is a number field and Omega is its algebraic closure",
]
HOST = [
    "Same actual Host and HFrame; integral e(j,tau)",
    "Actual CM conjugation and host unramified quadratic valuation law",
]

claim(1, "Norm reflection of the coefficient DVR and its units",
      "The actual coefficient norm is at most one exactly on O, equals one exactly on its units, and l lies in the maximal ideal.",
      [], many("coef", ["norm_le_one", "norm_unit", "norm_prime_lt_one", "embedding_closed_integral"]),
      COEF)
claim(2, "Closed finite-dimensional coefficient field image",
      "kappa(Frac O) is the Q_l-span of images of finitely many Z_l-generators and is closed in the possibly incomplete Qbar_l.",
      ["GA1"], many("coef", ["embedding_closed_integral"]),
      COEF + ["Completeness and local compactness of Q_l; elementary finite-dimensional norm equivalence"])
claim(3, "Actual adic embedding and continuity of coefficient extensions",
      "O embeds topologically via kappa, and any unital map into an adic local ring taking l into its maximal ideal is continuous.",
      ["GA1"], many("coef", ["embedding_closed_integral"]) +
      many("main", ["continuous_units", "isEmbedding_toQ", "continuous_ringHom"]),
      COEF + ["For extension: O' is an adic topological local ring and the image of l lies in its maximal ideal"])
claim(4, "Finite archimedean and adic algebraic products",
      "The literal infPow and lPow are continuous multiplicative maps, with the exact principal-idele product identities; lPow has finite support only above l.",
      ["GA2"], many("artin", ["IsAlgPos", "infPow", "locPow", "lPow", "finite_contEmb", "finite_contEmbInf",
                             "isEmpty_contEmb", "locPow_of_notMem", "finite_support_lPow",
                             "infPow_localIdele", "lPow_localIdele"]) +
      many("products", ["exists_units_hom", "exists_infPow_hom", "exists_lPow_hom", "infPow_diagUnits"]) +
      many("openker", ["lPow_diagUnits"]) +
      many("normemb", ["norm_embedding_integer_le_one", "exists_place_of_embedding"]) +
      many("extension", ["exists_finite_intermediateField_range_le", "exists_continuous_extension_adicCompletion"]) +
      many("placeeq", ["norm_lt_one_of_contEmb", "place_eq_of_contEmb_comp_eq"]),
      ["E number field, l prime, supplied algebraic iota:Qbar_l~C", "Integer-valued type n", "Number-field localizations/completions and elementary weak approximation"])
claim(5, "Open kernel of the nonalgebraic remainder",
      "chi/infPow is trivial on the connected infinite component and has open kernel; composing that remainder with iota inverse is therefore continuous.",
      ["GA4"], many("finiteker", ["eq_one_of_pow_near", "isOpen_ker_finIdele"]) +
      many("products", ["isOpen_connectedComponentOfOne_inf", "denseRange_units_inf", "pos_of_mem_connectedComponentOfOne"]) +
      many("openker", ["IsAlgPos.eq_infPow", "isOpen_ker_of_infConn"]) +
      many("artin", ["continuous_of_isOpen_ker'"]),
      ["chi is an actual continuous Hecke character satisfying IsAlgPos n", "Weak approximation; restricted-product topology of finite ideles"])
claim(6, "Normalized adic character from the stated Artin map",
      "The corrected idele character iota^{-1}(chi/infPow)*lPow descends uniquely and continuously through Art, proving exists_isLAdicOf and GlobalArtinReciprocity.heckeLAdicCharacter.",
      ["GA4", "GA5", "RC3"], many("openker", ["lPow_of_mem_infConn", "IsGlobalArtin.exists_isLAdicOf", "GlobalArtinReciprocity.heckeLAdicCharacter"]) +
      many("artin", ["IsGlobalArtin", "IsLAdicOf", "IsLAdicOf.unique", "GlobalArtinReciprocity", "HeckeLAdicCharacter"]),
      CFT + ["Actual chi, n satisfying IsAlgPos", "Specified algebraic iota; no topological assumption on iota"])
claim(7, "Exact local units, inertia, decomposition and inverse Frobenius",
      "The adic realization reads local units directly and arithmetic Frobenius inversely, with identical inertia image/exponents away from l or at type zero.",
      ["GA6"], many("artin", ["IsLAdicOf.loc", "IsLAdicOf.loc_away", "IsLAdicOf.ine_image", "IsLAdicOf.unr_iff",
                             "IsLAdicOf.frob", "IsLAdicOf.frob_unr", "IsLAdicOf.dec_triv", "IsLAdicOf.mul", "IsLAdicOf.inv"]) +
      many("main", ["IsGal.frob", "IsGal.loc", "exists_unit", "exists_ine", "IsGal.ine_pow_iff", "IsGal.unr_iff"]),
      CFT + ["The exact IsLAdicOf/IsGal realization", "Local prime away from l or type n=0"])
claim(8, "Normalized character in the specified finite DVR",
      "Closed-quotient Frobenius detection and compactness put the exact normalized character in O^times and recover its continuity, proving exists_isGal.",
      ["GA1", "GA2", "GA3", "GA6", "GA7", "RC4"],
      many("main", ["norm_le_one_of_compact", "AlmostIn", "eq_of_frob", "exists_isGal"]) +
      many("avatar", ["toQ", "inQ", "IsGal"]) + many("dense", ["eq_one_of_frob"]),
      COEF + CFT + ["epsilon:K->C and f:K->Frac O with iota*kappa*f=epsilon", "AlmostIn epsilon chi and IsAlgPos chi n"])
claim(9, "Finite-order realization and its inverse construction",
      "Finite-order Hecke characters have type zero; finite-order continuous Galois characters recover their unique Hecke character; the kernels are open.",
      ["GA6", "GA7", "GA8"], many("artin", ["isOpen_ker_of_pow", "exists_unique_hchar_of_finite_order",
                                          "isAlgPos_zero_of_orderDvd", "IsLAdicOf.pow_eq_one",
                                          "liftAb", "continuous_liftAb"]) +
      many("main", ["IsGal.pow_eq_one", "IsGal.isOpen_ker", "IsGal.ramExactly", "IsGal.dec_triv"]),
      CFT + ["A positive integer m and the exact order-dividing-m hypothesis", "For O-valued descent: the actual coefficient datum and field reading"])
claim(10, "Actual anticyclotomic identity",
      "Triviality on the host real subfield gives r(cc*sigma*cc^{-1})=r(sigma)^{-1}, with the literal supplied conjugation.",
      ["GA7", "GA8", "RC4"], many("conj", ["conjHom", "conjHom_apply", "isFrob_conjHom", "continuous_conjHom",
                                         "normV_conjPl", "isPlaceOver_moveVal_conjPl", "val_mul_val_conj", "antiHom_of_trivOn"]) +
      many("main", ["IsGal.anti"]) + many("hostcm", ["valuation_eq_of_unram", "host_cm"]),
      CFT + HOST + ["The actual Hecke character is TrivOn F and has the stated normalized realization"])
claim(11, "CM parity and explicit integral infinite types",
      "Even argument exponents have paired algebraic type (a,-a); eta^{-1}|.|^{-r/2} for r=2h+1 has type (-h-1,-h).",
      ["HF13"], many("cmtype", ["bijective_cmType", "prod_split", "isAlg_of", "even_pow", "odd_pow", "isAlg_even_odd"]) +
      many("main", ["odd_r", "exists_isAlgPos_mu0", "block_alg", "del_alg"]) +
      many("hostchar", ["IsMu0", "IsEtaT"]) + many("ranks", ["r", "nV"]),
      HOST + ["Actual host CM type", "Even k,m and odd t of Ranks", "No reindexing of the global chain length"])
claim(12, "The odd block has values in the same field",
      "For r=2h+1, the block value is epsilon(y*z^{-1}*N(P)^h); on units its local value equals mu when eta is unramified.",
      ["GA11"], many("avatar", ["block"]) +
      many("main", ["AlmostIn", "AlmostIn.mul", "AlmostIn.inv", "almostIn_of_valuesIn", "block_val", "AlmostIn.block", "block_loc"]),
      ["AlmostIn epsilon mu", "eta.ValuesIn(1/2) epsilon", "Odd r; exact absolute-value character convention"])
claim(13, "Exact shift and block realization in each supplied reading",
      "Triple.exists_shift and exists_blockChar follow in the actual O0(i) from actual ValLL0 and Reading.",
      ["GA8", "GA9", "GA11", "GA12", "HF16"],
      many("block", ["embSide", "Reading", "Reading.toC", "muBase", "blockChar", "shiftChar", "hframe",
                     "eExp_int", "exists_shift", "exists_blockChar"]) +
      many("main", ["inertialOrderFifteenChar_auxiliaryPrime_spec"]),
      COEF + CFT + ["Same D, actual CharFrame C and ValLL0 D C", "Already supplied twist index i, side b and actual Reading"])
claim(14, "Independence from the reading of the same coefficient ring",
      "The same integral block character realizes the block under any other Reading with the same embSide; IsChars is similarly independent.",
      ["GA3", "GA7", "GA12", "GA13", "RC4"],
      many("reading", ["toC_eq_of_mem", "almostIn_blockChar", "isGal_of_reading", "isChars_of_reading"]),
      CFT + ["Same i,b,O0,embSide", "Actual ValLL0 and both readings", "A normalized realization for the first reading"])
claim(15, "The installed first character is the normalized block character",
      "firstTwistCharacter_eq_ladic_heckeCharacter follows from exact normalized cofinite readings and the three actual frame character identities.",
      ["GA3", "GA7", "GA12", "GA13", "RC4"],
      many("first", ["firstTwistCharacter_eq_ladic_heckeCharacter"]) +
      many("normv", ["isFrob_conj", "frob_any", "val_of_at", "normV_eq_absNorm", "val_block"]) +
      many("normread", ["NChiData.firstHeckeCharacter", "NormalizedCharacterCompatibility"]),
      CFT + ["Same actual D, CharFrame, ValLL0, NChiData and NormalizedCharacterCompatibility",
             "Actual eta/mu0/del identities", "Continuity of the installed NTw.chi1", "Existing index, side and Reading"])
claim(16, "Both side families and exact auxiliary inertia order fifteen",
      "Construct all clauses of HeckeTwistCharactersDeltaChi, including exact order 15, selected support, two sides and type-prime inertia exponents.",
      ["GA7", "GA8", "GA9", "GA10", "GA11", "GA12", "GA17", "HF12", "HF13"],
      many("main", ["sideIso_true", "sideIso_false", "IsGal.side", "sideIso_read", "read_conj",
                    "inertialOrderFifteenChar_auxiliaryPrime_spec", "card_eq_of_pow_iff", "absNorm_eq_pow",
                    "HeckeTwistCharactersDeltaChi", "hostHeckeFrame_twist_galois_characters"]) +
      many("hostchar", ["IsDelta"]) + many("avatar", ["sideIso", "delAt"]) +
      many("wildunits", ["orders_on_units"]) + many("split", ["splitsC_main"]),
      COEF + CFT + HOST + ["Both f and conjugate f' readings", "Actual common field of mu0, eta and selected delta values",
                           "Complete splitting at both type primes", "Exact pD set of primes above the selected auxiliary rational prime"])
claim(17, "Exact tame and wild local unit power laws",
      "Tame images have exponent q-1; characters killing the local (q-1)st roots have q-power unit values; prime-to-residue-characteristic inertia images are generated by the specified tame generator.",
      ["GA5", "AR3"], many("wildunits", ["val_pow_sub_one_le", "val_pow_pow_sub_one_le", "valued_pow_sub_one_lt_one",
                                 "exists_rootOfUnity_congr", "orders_on_units"]) +
      many("tamegen", ["wild_mem_Ine", "finite_roots", "eq_one_of_wild_prime", "mem_zpowers_of_tameGen"]),
      ["Actual local completion of a number field", "Continuity and the stated tame/root-triviality assumptions",
       "For Galois version: TameGenAt and inertia exponent prime to residue characteristic", "Finite ramification and Hensel facts as explicitly used in AR3"])
claim(18, "Tame generator calibration uniform in coefficients and row",
      "A single residue generator yields the exact Teichmuller value for every row and coefficient realization, and constructs a new TameTie array.",
      ["GA6", "GA7", "GA11", "GA12", "GA17", "HF13"],
      many("main", ["range_eq_rootsOfUnity", "mu0_loc_eq_inv_om_pow_of_div_of_absNorm_eq",
                    "TameInertiaGeneratorCharacterSpec", "hostHeckeFrame_tame_galois_characters"]) +
      many("sqgen", ["exists_generator_sq_eq_of_sq_mem_zpowers"]) +
      many("localres", ["localUnit_congr_global", "exists_nat_congr_of_absNorm_prime"]) +
      many("reading", ["TameTie", "exists_tameTie"]),
      CFT + HOST + ["Chosen half of a completely split type prime", "Specified TameGenAt element and injective Teichmuller map",
                     "At least row j=0; no extra value-field containment for its auxiliary Qbar realization",
                     "Any identification with preinstalled nd.chiT remains explicit"])
claim(19, "Actual toric quotient character and integral Frobenius values",
      "Construct ToricHeckeQuotientCharacter with the actual side, coefficient extension, anticyclotomic law and q-power auxiliary quotient values.",
      ["GA3", "GA7", "GA8", "GA9", "GA10", "GA11", "GA17"],
      many("main", ["ToricHeckeQuotientCharacter", "hostHeckeFrame_toric_quotient_character"]),
      COEF + CFT + HOST + ["Actual even-infinity vartheta trivial on F, with stated values in K",
                           "vartheta kills local q-1 roots at auxiliary places", "Exact support S0 and allowable O->O' map",
                           "The actual normalized delta and selected side"])
claim(20, "Actual localization family and exact cyclotomic exponent",
      "Construct LocalisationCharacterSpec for the supplied IsPsi(l,Q), including genuine inertia at every Q-place and chi_c=chi_1*cyc_l^{-(c-1)}.",
      ["GA3", "GA7", "GA8", "GA9", "GA10", "GA11", "GA12"],
      many("main", ["continuous_cyc", "LocalisationCharacterSpec", "hostHeckeFrame_localisation_character_spec"]) +
      many("hostchar", ["IsPsi"]) + many("ranks", ["nV"]) + many("normread", ["chi_c_read"]),
      COEF + CFT + HOST + ["Actual IsPsi(l,Q), exact support and prime separation",
                           "Same value-field containment for mu0,eta,delta,psi", "The actual continuous cyclotomic character"])
claim(21, "Exact normalized twist under coefficient extension",
      "Construct LocalisationTwistCharacterCompat from the literal integral K-value square; no agreement of whole fraction-field readings is assumed.",
      ["GA3", "GA7", "GA12", "RC4"],
      many("main", ["LocalisationTwistCharacterCompat", "hostFrame_localisationTwistCharacterCompat"]),
      COEF + CFT + ["Both actual coefficient data have the same l", "Common K and exact integral relation (GA.28)",
                    "The three supplied exact normalized realizations", "Actual mu0,eta,delta values in K"])
claim(22, "Installed local character and full exact local readings",
      "Prove literal chi1_loc_isGal and the conditional upgrades from cofinite normalized delta/psi readings to full DeltaRead and IsGalOf for the same tuple.",
      ["GA3", "GA7", "GA8", "GA12", "GA15", "GA21", "RC4"],
      many("normv", ["chi1_loc_isGal", "frob_any", "val_block"]) +
      many("chargal", ["IsGalOf", "DeltaRead", "delta_side", "CharFrame.delAt_unitary",
                       "isGalOf_delta_of_deltaRead", "NGalChrTied", "NGalChrTied.delta"]) +
      many("sideb", ["SideB"]) + many("normread", ["NormalizedCharacterCompatibility"]),
      COEF + CFT + ["Literal same-object SideB normalized readings, LocNd/LocTw/NdSpec/LocAut/AutSpec identities for chi1_loc_isGal",
                    "Its original further endpoint premises are preserved",
                    "For DeltaRead upgrade: same installed normalized delta, actual value containment and coefficient map",
                    "For psi: the local chosen character equals the actual tuple psi component"])
claim(23, "Exact conditional character installation and nonempty-stage boundary",
      "Construct Chars for each existing Tw index and the literal empty-local exists_isTripleOf; explicitly retain nonempty same-object coverage, normalized readings and genuine form representations.",
      ["GA13", "GA14", "GA16", "GA18", "GA20", "GA21", "GA22", "RC8"],
      many("reading", ["rd", "rd_conj", "Chars", "chars_nonempty", "tw", "ex", "isTripleFor_ex", "exists_isTripleOf"]) +
      many("block", ["Reading.nonempty", "IsChars", "IsTripleWith", "IsTripleFor"]) +
      many("sideb", ["SideB"]) + many("ntw", ["NTw"]) +
      many("main", ["galois_characters_of_artin"]),
      CFT + ["Same actual D and existing Tw coefficient skeleton", "Actual star-stable LL0 containing the frame values",
             "For replacement endpoint: IsEmpty(nd.Loc) and TameTie for preinstalled chiT",
             "This replacement empties Sig/abelian_2 and sets Fm=0; no genuine nonempty compatible stage is claimed"])


completed = []


def done(key, name, ids, condition, scope="literal conditional endpoint"):
    completed.append({
        "endpoint": name, "claim_ids": ids,
        "status": "completed_conditionally", "scope": scope,
        "conditions": condition, "source": source(key, name),
    })


done("coef", "embedding_closed_integral", ["GA1", "GA2", "GA3"], COEF)
done("main", "continuous_ringHom", ["GA3"], ["Exact source and target adic local topology hypotheses; l nonzero in source and in target maximal ideal"])
done("products", "exists_infPow_hom", ["GA4"], ["Number field, integer type"])
done("products", "exists_lPow_hom", ["GA4"], ["Number field, prime l, supplied algebraic iota and integer type"])
done("openker", "isOpen_ker_of_infConn", ["GA5"], ["Continuous idele character trivial on connected infinite component"])
done("openker", "IsGlobalArtin.exists_isLAdicOf", ["GA6"], CFT + ["Actual IsAlgPos chi n"])
done("openker", "GlobalArtinReciprocity.heckeLAdicCharacter", ["GA6"], ["GlobalArtinReciprocity"])
done("main", "exists_isGal", ["GA8"], COEF + CFT + ["Actual AlmostIn and commuting K embeddings; IsAlgPos"])
done("artin", "exists_unique_hchar_of_finite_order", ["GA9"], CFT + ["Continuous finite-order Galois character"])
done("main", "IsGal.anti", ["GA10"], CFT + HOST + ["Actual normalized character trivial on F"])
done("cmtype", "isAlg_even_odd", ["GA11"], HOST + ["Actual even argument type or odd-r eta normalization"])
done("main", "AlmostIn.block", ["GA12"], ["Actual AlmostIn mu, ValuesIn(1/2) eta and odd r"])
done("block", "exists_shift", ["GA13"], CFT + ["Actual D, CharFrame, ValLL0 and Reading"])
done("block", "exists_blockChar", ["GA13"], CFT + ["Actual D, CharFrame, ValLL0 and Reading"])
done("reading", "isGal_of_reading", ["GA14"], CFT + ["Same coefficient ring and embSide, both readings, ValLL0 and one normalized realization"])
done("reading", "isChars_of_reading", ["GA14"], CFT + ["Same coefficient ring and embSide, both readings, ValLL0 and actual IsChars"])
done("first", "firstTwistCharacter_eq_ladic_heckeCharacter", ["GA15"], CFT + ["Exact installed NormalizedCharacterCompatibility and eta/mu0/del identities; actual ValLL0 and Reading"])
done("main", "hostHeckeFrame_twist_galois_characters", ["GA16"], COEF + CFT + HOST + ["Both side embeddings and actual field of values", "Complete splitting at type primes"])
done("wildunits", "orders_on_units", ["GA17"], ["Actual local continuous character and stated tame/root-triviality alternatives"])
done("tamegen", "mem_zpowers_of_tameGen", ["GA17"], ["Actual continuous Galois character, TameGenAt and prime-to-residue-characteristic inertia exponent"])
done("sqgen", "exists_generator_sq_eq_of_sq_mem_zpowers", ["GA18"], ["Finite residue field and exact square-generation premise"])
done("main", "hostHeckeFrame_tame_galois_characters", ["GA18"], CFT + HOST + ["Chosen type half, complete splitting, TameGenAt and injective Teichmuller"])
done("reading", "exists_tameTie", ["GA18"], CFT + ["Actual chosen-half membership for every specified type place", "Produces a new array; fixed chiT equality not inferred"])
done("main", "hostHeckeFrame_toric_quotient_character", ["GA19"], COEF + CFT + HOST + ["Exact ToricHeckeQuotientCharacter input predicates"])
done("main", "hostHeckeFrame_localisation_character_spec", ["GA20"], COEF + CFT + HOST + ["Actual IsPsi and all LocalisationCharacterSpec input predicates"])
done("main", "hostFrame_localisationTwistCharacterCompat", ["GA21"], COEF + CFT + ["Exact common-prime integral K-reading square and normalized characters"])
done("normv", "chi1_loc_isGal", ["GA22"], ["All literal endpoint premises on the same D, SideB, local and automorphic package", "Constructed argument uses actual normalized readings and coefficient squares"])
done("chargal", "isGalOf_delta_of_deltaRead", ["GA22"], ["Same actual DeltaRead and star-stable LL0"])
done("reading", "chars_nonempty", ["GA23"], CFT + ["Actual existing Tw index, star-stable LL0, ValLL0 and coefficient readings"])
done("reading", "isTripleFor_ex", ["GA23"], CFT + ["Empty local index type, actual Chars family and fixed-array TameTie", "Only the source's empty Sig/zero Fm replacement"])
done("reading", "exists_isTripleOf", ["GA23"], CFT + ["Empty local index type, star-stable LL0, ValLL0 and fixed-array TameTie", "Preserves an existing Tw skeleton; no cover or genuine form space construction"])


targets = [
    {
        "id": "GA-next-01", "title": "Actual global reciprocity map",
        "scope": "Retain GlobalArtinReciprocity with the exact open quotient/kernel/inertia/inverse-Frobenius/decomposition convention; GA6 eliminates the separate HeckeLAdicCharacter primitive.",
        "sources": many("artin", ["GlobalArtinReciprocity", "IsGlobalArtin"]),
        "discharged_subscope": ["IsGlobalArtin.exists_isLAdicOf", "GlobalArtinReciprocity.heckeLAdicCharacter"],
    },
    {
        "id": "GA-next-02", "title": "Compatible actual coefficient field, readings and all-place cover",
        "scope": "Install the HF finite value field inside the actual fixed LL0 and select all coefficient place embeddings on the same D. A Reading for each existing i and normalized adic realization do not imply forall w exists i with the literal SidePl true.",
        "sources": many("sideb", ["SideB"]) + many("block", ["Reading", "Reading.Induces", "Reading.nonempty"]) +
                   many("ntw", ["NTw"]),
        "discharged_subscope": ["Character construction after each supplied Reading", "Independence of readings of the same O0/embSide"],
    },
    {
        "id": "GA-next-03", "title": "Actual compatible nonempty NTw/local and form data",
        "scope": "Construct nonempty twist/local data, genuine Sig/form/Galois representation spaces, and cover on the same D. The proved exists_isTripleOf requires Loc empty and resets Sig and abelian_2 to empty and Fm to zero; it cannot replace this supplier.",
        "sources": many("ntw", ["NTw"]) + many("block", ["IsTripleWith", "IsTripleFor"]) +
                   many("reading", ["tw", "ex", "exists_isTripleOf"]) + many("sideb", ["SideB"]),
        "discharged_subscope": ["Chars for each already supplied index", "Literal empty-local conditional replacement"],
    },
    {
        "id": "GA-next-04", "title": "Normalized installed-stage character and tuple compatibility",
        "scope": "Supply the normalized reading record and exact eta/mu0/del/psi identities for the actual installed stage; preserve twist_2/embK/Sp.iq/AutSpec and tuple psi squares. Newly constructed characters alone do not transport existing forms/cohomology.",
        "sources": many("normread", ["NChiData", "NormalizedCharacterCompatibility"]) +
                   many("sideb", ["SideB", "ChoiceSide"]) + many("chargal", ["NGalChrTied", "CharacterChoiceData'"]),
        "discharged_subscope": ["firstTwistCharacter_eq_ladic_heckeCharacter from these identities", "chi1_loc_isGal with its exact package", "Conditional cofinite delta reading to full DeltaRead", "IsGalOf for the same chosen psi"],
    },
    {
        "id": "GA-next-05", "title": "Actual anticyclotomic Hecke characters on required nonempty support",
        "scope": "Construct the required IsPsi(l,Q), or equivalent exact anticyclotomic finite Galois characters with the specified nonempty ramification and trivial l-decomposition action. GA20 constructs its adic localization only after such a psi is supplied.",
        "sources": many("hostchar", ["IsPsi"]) + many("avatar", ["IsDel", "delOf", "delOf_laws", "UniversalAnticyclotomicCharLaws", "delUTie_of_exists"]),
        "discharged_subscope": ["LocalisationCharacterSpec for the supplied exact IsPsi", "Finite-order inverse Hecke realization"],
    },
    {
        "id": "GA-next-06", "title": "Tame array agreement for the already fixed NData",
        "scope": "The uniform tame calibration constructs some array c. If nd.chiT is already installed, prove the exact TameTie for that same array or transport every dependent object coherently.",
        "sources": many("reading", ["TameTie", "exists_tameTie", "isTripleFor_ex"]) + many("ntw", ["NData"]),
        "discharged_subscope": ["Uniform coefficient-independent Teichmuller calibration and existence of a new TameTie array"],
    },
    {
        "id": "GA-next-07", "title": "Remaining genuine representation and same-object arithmetic joins",
        "scope": "Retain genuine representation/Galois suppliers and MtReal/MtFam/MtAd/NExpTied and fixed ColW/Pre2/St/RowPk compatibility from AR/RC/NC. One-dimensional IsGal does not give those modules, ranks or comparison maps.",
        "sources": many("block", ["IsParam", "IsResidual", "IsTripleWith", "IsTripleFor"]) + many("sideb", ["SideB", "ChoiceSide"]),
        "discharged_subscope": ["Normalized one-dimensional characters used inside those records"],
    },
]

all_sources = [s for c in claims for s in c["sources"]]
unique_ranges = {(s["path"], s["line_start"], s["line_end"], s["range_sha256"]) for s in all_sources}
claim_ids = {c["id"] for c in claims}
for c in claims:
    for dep in c["depends_on"]:
        if dep.startswith("GA") and dep[2:].isdigit():
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

manifest = {
    "component": "adic_realization", "version": "0.20", "commit": COMMIT,
    "repository": URL, "source_files": [
        {
            "path": path, "sha256": sha(raw), "bytes": len(raw),
            "line_count": len(raw.splitlines()),
            "verified_equal_to_pinned_git_blob": True,
            "url": f"{URL}/blob/{COMMIT}/{path}",
        } for path, raw in sorted(cache.items())
    ],
}
reviews = []
for name, expected in [
    ("adic_realization_GA1_12_review.txt", [f"GA{i}" for i in range(1, 13)]),
    ("adic_realization_GA13_23_review.txt", [f"GA{i}" for i in range(13, 24)]),
]:
    path = ROOT.parent / "reviews_v0_20" / name
    if path.exists():
        data = path.read_bytes()
        text = data.decode()
        bound = [cid for cid, p in paragraphs.items() if p["sha256"] in text]
        assert set(expected) <= set(bound), ("review misses current scoped paragraph hashes", path, sorted(set(expected)-set(bound)))
        reviews.append({"file": "reviews_v0_20/"+name, "sha256": sha(data),
                        "expected_claim_ids": expected, "bound_current_claim_ids": bound})

provenance = {
    "component": "adic_realization", "version": "0.20", "claim_prefix": "GA",
    "source_commit": COMMIT, "repository": URL,
    "scope": "Actual normalized one-dimensional adic characters from the stipulated GlobalArtin map, exact finite-DVR descent, shift/block and installed-character identification, all five host character laws and conditional local installation. Retains same-object nonempty cover, actual installed readings/field/tuples, nonempty IsPsi and genuine representation suppliers.",
    "main_sha256": sha(main), "report_sha256": sha(report),
    "builder_sha256": sha(Path(__file__).read_bytes()),
    "claims": claims, "completed_source_endpoints": completed,
    "derived_additional_implications": [{
        "claim_id": "GA22",
        "statement": "Cofinite normalized installed-delta reading plus actual ValuesIn and exact reading square imply full DeltaRead at every unramified place.",
        "status": "proved_conditionally",
        "not_claimed": "DeltaRead for arbitrary same-order or same-support characters",
    }],
    "remaining_targets": targets, "independent_reviews": reviews,
    "counts": {
        "claims": len(claims), "claim_source_links": len(all_sources),
        "distinct_claim_ranges": len(unique_ranges), "indexed_source_files": len(cache),
        "completed_source_endpoints": len(completed), "remaining_supplier_families": len(targets),
    },
    "verification": {
        "git_objects_only": True, "source_checkout_unchanged": True,
        "old_components_unchanged": True, "lean_compiled": False, "pdf_generated": False,
        "hypothesis_policy": "Every completed endpoint is conditional on its literal compatible inputs; no empty-index construction is used for nonempty coverage.",
    },
}
next_targets = {
    "component": "adic_realization", "version": "0.20", "commit": COMMIT,
    "scope": provenance["scope"], "completed_endpoints": completed,
    "next_targets": targets,
}
for name, obj in [
    ("provenance.json", provenance), ("source_manifest.json", manifest),
    ("next_targets.json", next_targets),
]:
    (ROOT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+"\n")
lines = [
    "ADIC REALIZATION SOURCE LOCATORS -- GA1--GA23",
    "Pinned commit: "+COMMIT,
    "Inclusive line ranges; range bytes are exact Git blob lines including line endings.",
    "",
]
for c in claims:
    lines.append(c["id"]+" "+c["title"])
    lines.append("TeX paragraph SHA-256: "+paragraphs[c["id"]]["sha256"])
    for s in c["sources"]:
        lines.extend([
            f'  {s["declaration"]}',
            f'  {s["path"]}:{s["line_start"]}-{s["line_end"]}',
            f'  full SHA-256 {s["full_file_sha256"]}',
            f'  range SHA-256 {s["range_sha256"]}',
            f'  {s["url"]}',
        ])
    lines.append("")
lines.append("Completed endpoints: "+str(len(completed))+"; remaining supplier families: "+str(len(targets)))
(ROOT/"source_locators.txt").write_text("\n".join(lines)+"\n")
print(json.dumps(provenance["counts"], sort_keys=True))

