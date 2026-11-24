#!/usr/bin/env python3
"""Rebuild RC provenance from pinned Git objects, without checkout mutation."""
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
IE = "src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/"
IW = "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/"
LC = "src/Formalism/LocalRingCardinality/"
LE = "src/Formalism/SharpRestriction/LevelLetterCocycles/"
AM = "src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/"
P = {
    'endpoint': IW + 'StatementCOfCasselmanWallach.lean',
    'lev': IW + 'ReadsHecke.lean',
    'real': 'src/Formalism/LocalToGlobal/GaloisLevelStructure/TiedHecke.lean',
    'cell': 'src/Formalism/LocalToGlobal/NormalizedHeckeFactors/RingHomOfBaseOrderToFraction.lean',
    'ntw': LE + 'DataN.lean',
    'frame': AM + 'ConcreteTwistFrameExtraExcludedOverSmallPrimes.lean',
    'choiceside': AM + 'RingSpecNormalisedCharacterEq.lean',
    'gal': 'src/Formalism/LocalToGlobal/UnitaryNorms/CharGal.lean',
    'complexify': IW + 'FinrankAlgebraicModularFormsComplexification.lean',
    'finitegal': IW + 'ExistsGaloisCharacterOfFiniteOrderHeckeCharacter.lean',
    'galprops': IW + 'GaloisCharacterAntiRamifiedExactly.lean',
    'descent': IW + 'ExistsRingClassGroupDescentOfCoeffFieldTwist.lean',
    'power': IW + 'RingClassGroupDescentsDifferByPowerPrimeToL.lean',
    'side': IW + 'TwistReadingInducesSideEmbeddingFixedField.lean',
    'complex': IW + 'ExistsComplexEmbeddingReadingFractionRingOverCoe.lean',
    'cp': IW + 'CardPadicAlgClPadicComplexEqComplex.lean',
    'algclosed': IE + 'AlgClosedContinuumRingEquivComplexExtending.lean',
    'dense': IW + 'DenseRangeUnits.lean',
    'conj': IW + 'IsPlaceOverMoveValConjPl.lean',
    'hecke': IW + 'ValuationPowSubPowLt.lean',
    'artin': 'src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',
    'colw': AM + 'PositionOfIntro.lean',
    'pre2': AM + 'NonzeroPlacesOverPrimesLifts.lean',
    'rowpk': AM + 'ReadPk.lean',
    'lift': AM + 'RowsRestWordColumnUnitBaseTupleAlt.lean',
    'muw': IW + 'ExistsRowsDatumPrescribedTuplesDefinedWeights.lean',
    'rowexist': IW + 'NonemptyRowLiftFamilyOverColumnChoices.lean',
    'q': AM + 'ThirdLevelOfGoodTwists.lean',
    'muisw': AM + 'RationalRootsDef.lean',
    'parahoric': IW + 'MemParahoricOfScalarActionOnRamifiedParahoricFor.lean',
    'orientation': IW + 'SplitPlaceEqOfAutomorphismMapsParahoric.lean',
    'additive': IW + 'AdditiveCharacterEqOfCommonUnipotentLevelEigenve.lean',
    'index': IW + 'RelIndexLevelUnipotentCoprimePrime.lean',
    'stabilizer': IW + 'ExistsClassTrivialStabiliserAtTypePlace.lean',
    'nonzero': IW + 'ExistsNeZeroAlgebraicModularFormOfTrivialStabili.lean',
    'shape': IW + 'ExpectedShapeLevelIntegralAndUnipotentAtTypePlac.lean',
    'product': IW + 'ProductLevelEqOfLocalAgreement.lean',
    'cellproduct': IW + 'IsProductLevelDefiniteFormsRealisationAtTwist.lean',
    'component': IW + 'HeckeCharacterSplitPlaceComponentUnique.lean',
    'block': IW + 'UpperParahoricLowerDetUnitAndSuperdiagIntegral.lean',
    'finiteplaces': IW + 'TypePlacesUnionRamifiedPlacesFinite.lean',
    'gsplit': 'src/Formalism/SharpRestriction/Divisibility/GeneratorPowers/GSplit.lean',
    'host': LC + 'DataHost.lean',
    'ranks': LC + 'Params.lean',
    'joint': IW + 'JointEtaOfAdmissibleTwist.lean',
    'cellwt': IW + 'CellWeightOfAdmissibleTwist.lean',
    'parashape': IW + 'SideReadHeckeOfAdmissibleTwist.lean',
    'unishape': IW + 'SplitPlaceOfAdmissibleTwist.lean',
    'bad': IW + 'BadPlacesSubOfAdmissibleTwist.lean',
    'ramunit': IW + 'ExistsLocalUnitCharacterNontrivial.lean',
    'gplaces': IW + 'GoodPlacesAllStates.lean',
    'avoid': IW + 'TwistConductorsAvoidExcludedPrimes.lean',
    'reads': IE + 'ExistsReadsAtOfCover.lean',
    'choice': IE + 'ExistsTiedChoiceOfReads.lean',
    'lattice': IE + 'ExistsEquivMapLattice.lean',
    'subbasis': IE + 'ExistsCharDescent.lean',
    'ihf': LE + 'IntegralHeckeForms.lean',
    'dataties': LC + 'DataTies.lean',
    'good': LE + 'TwGood.lean',
    'nchoice': LC + 'DataNChoice.lean',
    'nchtie': LC + 'DataNChTie.lean',
    'hostchar': 'src/Formalism/LocalToGlobal/UnitaryNorms/CharHost.lean',
    'reschar': IW + 'ResCharConj.lean',
    'muis': IW + 'TupTiedOfMuIsW.lean',
    'normal': LE + 'BlochKatoPhases.lean',
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
        "range_kind": "literal retained record-field interface",
        "verified_equal_to_pinned_git_blob": True,
    }


main = (ROOT / "main.tex").read_bytes()
report = (ROOT / "report.txt").read_bytes()
tex = main.decode()
assert not [c for c in tex if ord(c) < 32 and c not in "\n\r\t"]
markers = list(re.finditer(r"(?m)^\\paragraph\{(RC\d+):", tex))
assert [m.group(1) for m in markers] == [f"RC{i}" for i in range(1, 22)]
paragraphs = {}
for i, match in enumerate(markers):
    end = markers[i+1].start() if i+1 < len(markers) else len(tex)
    part = tex[match.start():end].encode()
    paragraphs[match.group(1)] = {
        "sha256": sha(part), "bytes": len(part),
        "line_start": tex[:match.start()].count("\n") + 1,
        "line_end": tex[:end].count("\n"),
    }
claims = []


def claim(i, title, statement, deps, sources, assumptions):
    cid = f"RC{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.18", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "arithmetic_compatibility/main.tex",
            "expanded": "arithmetic_compatibility/report.txt",
            "section": cid, **paragraphs[cid],
        }, "sources": sources,
    })


claim(1, "Finite evaluation scalar extension",
      "The exact coefficient form space complexifies to the actual complex form space under WtMatch and the congruence-kernel condition.",
      [], many("complexify", ["exists_finset_eval_eq_zero", "coordCx", "finrank_typeSp_cx"]) +
      many("lev", ["WtMatch"]),
      ["Finite-dimensional coefficient form space", "Exact common-basis representation matrices", "Congruence subgroup killed by the level character"])
claim(2, "Literal rank comparison and RankTie",
      "LevEq and CellWt for the actual MtReal and NExpTied cell give the exact MtL/MtV finrank equality and hence RankTie.",
      ["RC1"], many("endpoint", ["rank_of_levEq"]) + many("real", ["MtReal"]) +
      many("cell", ["MtVReal", "NExpTied"]) + many("choice", ["RankEq", "RankTie"]) +
      [interface_range("lift", "Pk.what₂: actual Mt/jMt basis fields", 396, 406, "retained actual rational/complex basis interface")],
      ["One fixed D and its actual realization maps", "LevEq and CellWt", "Actual finite full MtLat and jMt_basis"])
claim(3, "Finite-order coefficient-valued Artin character",
      "A finite-order Hecke character and a primitive root in L give an L-valued open-kernel GalOf character through the specified reciprocity map.",
      [], many("finitegal", ["galOf_of_orderDvd"]) + many("lev", ["GalOf"]) +
      many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]),
      ["GlobalArtinReciprocity with all exact image clauses", "Positive order bound and primitive root in L", "Specified complex embedding"])
claim(4, "Frobenius detection from Artin and weak approximation",
      "A continuous commutative character trivial on every Frobenius outside a finite set is trivial.",
      ["RC3"], many("dense", ["denseRange_proj", "denseRange_units", "eq_one_of_local", "eq_one_of_away", "eq_one_of_unif", "eq_one_of_frob"]) +
      many("artin", ["IsGlobalArtin"]),
      ["Exact Artin uniformizer and quotient clauses", "Weak approximation", "Hausdorff commutative target"])
claim(5, "Anticyclotomic symmetry and exact local character behavior",
      "GalOf and IsPsi give anti, exact ramification and decomposition triviality above ell.",
      ["RC3", "RC4"], many("galprops", ["galOf_twist_props"]) +
      many("conj", ["_root_.GlobalTheory.AntiLAdic.isFrob_conjHom", "_root_.GlobalTheory.AntiLAdic.continuous_conjHom", "_root_.GlobalTheory.AntiLAdic.normV_conjPl", "_root_.GlobalTheory.AntiLAdic.isPlaceOver_moveVal_conjPl", "_root_.GlobalTheory.AntiLAdic.val_mul_val_conj"]) +
      many("hecke", ["IsHeckeOf.unr_iff", "IsHeckeOf.val_eq"]) + many("hostchar", ["IsPsi"]) +
      many("artin", ["IsGlobalArtin"]),
      ["Actual quadratic host and unramified restriction of valuations", "Exact IsPsi predicates", "GalOf"])
claim(6, "Ring-class descent and all seven TwOK conjuncts",
      "The actual art_univ factors the finite local cyclic character; every reading descent has all TwOK clauses and implies AdmTw.",
      ["RC5"], many("descent", ["eq_iff_of_reads", "one_iff_of_reads", "twOK_of_reads", "exists_reads", "exists_pulls_twOK"]) +
      many("ihf", ["TwOK"]) + many("cell", ["AdmTw"]) +
      [interface_range("ntw", "NTw.RCG/art/art_univ", 388, 403, "retained finite ring-class group and exact universal property")],
      ["Actual NTw.art_univ and S0 exceptional-set containment", "Reading and specified primitive local root", "Split Q disjoint from S0"])
claim(7, "Allowed power ambiguity with exact side signs",
      "Two descents of the same common character differ by an exponent prime to ell; normalized packets acquire both side signs.",
      ["RC6"], many("power", ["pulls_eq_zpow"]) + many("frame", ["twPackPow"]) +
      many("good", ["twPack", "psiAt_psiAt"]) + many("endpoint", ["pack_pow"]),
      ["Same index, support and exponent", "Common global character", "Primitive global and local roots", "art surjectivity"])
claim(8, "Exact side embedding and algebraic complex extension",
      "The reading denominator identity reflects integrality and supplies SidePl; finite cardinality bounds give a complex embedding extending all L.",
      ["NC4"], many("side", ["mem_range_map_iff_of_isLocalHom", "reading_sidePl_emb"]) +
      many("complex", ["exists_ringHom_complex_extending", "mk_le_of_finite", "exists_complex_emb"]) +
      many("cp", ["mk_le_pow_aleph0_of_denseRange", "mk_padic_le", "mk_padicAlgCl", "mk_padicComplex", "card_padicAlgCl_padicComplex"]) +
      many("algclosed", ["algClosed_continuum_ringEquiv_complex_extending"]) +
      many("frame", ["TwFrameC", "SidePl", "fracOe"]),
      ["Actual reading and injective local coefficient maps", "TwFrameC embedding into C_ell", "L is a number field", "Algebraic choice and transcendence bases"])
claim(9, "Coherent readings and common complex Hecke reading",
      "Conjugation-orbit choices give exactly invariant normalized packets and SideRead plus ReadsHecke for the same complex embedding.",
      ["RC6", "RC8", "NC10"], many("endpoint", ["unpack", "exists_data", "reads_of_pulls"]) +
      many("choice", ["Reading.Pulls", "Reading.Pulls.conj", "HasReading.conj"]) +
      many("lev", ["SideRead", "ReadsHecke"]),
      ["L0/Q Galois", "Conjugation-invariant index/support/exponent/common-character families", "Every required reading admits a descent"])
claim(10, "A nonempty-local Frobenius criterion for LocsCarry",
      "Exact local IsGalOf at exponent zero gives the common psiL identity; exact ramification forces Q equality, leaving literal index and side identities.",
      ["RC4", "RC5"], many("gal", ["IsGalOf", "NGalChrTied"]) +
      many("choice", ["LocsCarry"]) +
      [interface_range("ntw", "NTw.psiL and local twist fields", 409, 424, "retained local character, exact ramification and index/side interface"),
       interface_range("ntw", "NAut.iotaQ/iotaQC/iota_LL", 510, 514, "actual coefficient comparison into the same complex embedding")],
      ["Local IsGalOf(D,a,univ,psiL,chi(w(a)),0)", "Global GalOf and IsPsi for the same chi", "Literal twOf and twSide identities; no empty-Loc assumption"])
claim(11, "Actual conditional simultaneous NChoice and ChoiceSide",
      "The exact LevCmp.exists_choice hypothesis supplies C, tp with prescribed xi/psi/Q/k/index, TwOK and all six ChoiceSide fields.",
      ["RC2", "RC3", "RC5", "RC6", "RC7", "RC8", "RC9", "NC9", "NC12"],
      many("endpoint", ["exists_choice", "rank_of_levEq"]) +
      many("frame", ["ChoiceC"]) + many("choiceside", ["ChoiceSide"]) +
      many("gal", ["PsiChoiceCompatible"]) + many("choice", ["LocsCarry"]) +
      many("nchoice", ["NChoice"]) + many("nchtie", ["NChTie"]),
      ["All literal exists_choice premises h1–h8 and hs/sc", "Loc empty, but all-place readings and nonvacuous global ties retained", "Actual tuple supplier for every C with prescribed Q", "No Hecke-equivariance assertion for arbitrary integral lattice matching"])
claim(12, "Actual MuW tuple reset on an existing row model",
      "Exact xi range and injectivity choose conjugate-compatible muTw and muAt maps on an existing RowsRest, giving all three MuW clauses.",
      [], many("muw", ["reset", "GlobalTheory.Mem.R3.Rw.exists_rowsRest_muW"]) + many("rowpk", ["MuW"]) +
      many("colw", ["ColW"]) + many("reschar", ["resChar_conj"]),
      ["Existing RowsRest for the actual ColW", "Conjugation-stable Wt", "Actual xi range/injectivity and conjugation law", "Only tuple reset/MuW portion claimed; full ka/sha reset and RowPk remain retained"])
claim(13, "Actual ColW/Pre2/St MuIsW and TupTied join",
      "Literal tuple preservation in Pk.what₂ gives all ten MuIsW fields on the actual stage and the same xi/psi TupTied after Q equality.",
      ["NC16"], many("endpoint", ["muIsW", "cfOf_eq", "exists_tp"]) +
      many("muisw", ["MuIsW"]) + many("q", ["qOf_eq"]) +
      many("colw", ["ColW"]) + many("pre2", ["Pre2", "St"]) +
      many("rowpk", ["RowPk", "MuW"]) +
      [interface_range("lift", "Pk.what₂: literal muAt/muTw preservation", 356, 362, "actual tuple-field identity")],
      ["One actual ColW, Pre2, RowPk and St", "Exact frame equality and Q construction", "No substitution of a bare stage or unrelated row model"])
claim(14, "Rank-one parahoric scalar-action rigidity",
      "A scalar-acting integral local matrix belongs to the parahoric detected by a nontrivial determinant character.",
      [], many("parahoric", ["Gmat", "Pmat", "det_G", "det_P", "conj_G", "detDD_G", "detDD_P", "mem_para_of_eig"]),
      ["Split local unitary identification", "Nonzero form", "Local unit with nontrivial character value", "Integral scalar action and the same character kernel"])
claim(15, "Opposite parahoric orientation is detected",
      "The two split embeddings agree when an integrality-preserving support automorphism sends a parahoric into both proposed parahorics.",
      ["RC14"], many("orientation", ["algHom_eq_or_conj", "proj_conj", "loc_conj", "restr_surjective", "core", "GlobalTheory.ParaOpp.splitPlace_eq_of_para"]),
      ["Actual FrameAut and both containment statements", "Nontrivial block size", "Finite residue field"])
claim(16, "Unipotent eigenvalues determine the additive character",
      "A prime-to-p index and prime-to-p power identity force equality of the two additive characters on integral elements.",
      [], many("additive", ["eig_unique", "eigSub", "eigChar", "fractionFieldToGenericStalk_algebraMap_eq"]) +
      many("index", ["coprime_prod_pow_sub_one", "unip_index"]),
      ["Two nonzero form eigenfunctions", "Common scalar-action subgroup", "gcd(m,p)=1 and additive characters trivial on the maximal ideal", "Actual source m=p-1"])
claim(17, "Explicit trivial-stabilizer class",
      "The two-column integral matrix gives a trivial rational unitary stabilizer under p>=2n and p notin P²; actual host/type-prime fields supply these conditions.",
      [], many("stabilizer", ["geom_sum_expand", "eq_one_of_finOrder", "monomial", "frameM", "det_frameM", "exists_class", "exists_trivial_stabiliser"]) +
      many("gsplit", ["split_of_ncard", "g_splits"]) +
      [interface_range("host", "Host.qd_big", 54, 54, "retained actual host size inequalities"),
       interface_range("host", "Host.g_prime", 70, 72, "retained actual type-prime primality"),
       interface_range("ntw", "NData.g_split", 165, 165, "actual full splitting count"),
       interface_range("ntw", "NTypes.g_cond", 916, 916, "actual type-prime congruence"),
       interface_range("ranks", "Ranks and nV conventions", 8, 34, "actual rank/block inequalities")],
      ["Positive definite standard unitary realization", "At least two unipotent columns", "Actual type-prime count, congruence and host size fields"])
claim(18, "Actual nonzero form from the stabilizer class",
      "The exact product shape supplies integrality, and a trivial-stabilizer double coset supports a nonzero form of any nonzero weight.",
      ["RC17"], many("shape", ["bound"]) +
      many("nonzero", ["double_coset_unique", "cosetForm", "exists_form_of_trivial_stabiliser"]) +
      many("endpoint", ["grpShape_of", "exists_form"]) + many("lev", ["GrpShape"]),
      ["Exact product, local parahoric/unipotent and outside-compact shape", "Nonempty actual type-prime set", "Nonzero weight; actual congruence-kernel/realization maps"])
claim(19, "Literal local-to-global LevEq",
      "The actual Joint and local shapes, bad-set inclusion and ramified-unit nontriviality give equality of the global levels and all character values.",
      ["RC14", "RC15", "RC16", "RC18"],
      many("endpoint", ["levEq"]) + many("lev", ["Joint", "LevEq", "GPlaces", "ParaShape"]) +
      many("cellproduct", ["main"]) + many("component", ["main"]) +
      many("product", ["mem_of_agree", "levEq_of_agree"]) +
      many("block", ["detDD_unit_supDiag_int"]) + many("finiteplaces", ["gPl_union_qPl_finite"]),
      ["Exact actual Joint", "Actual product/parahoric/unipotent/outside-compact descriptions", "Cell type character for every side-compatible complex reading", "Bad-set inclusion and local-unit nontriviality", "CellWt is separately retained"])
claim(20, "Coherent twisted-place selector",
      "TwCoverPair and L0 normality give the actual exists_settings, with readings only on twisted places and equal index on equal-center pairs.",
      [], many("reads", ["OverOne", "OverOnePair", "ReadsAt", "ReadsAt.conj", "ReadsAt.of_overOne", "ReadsAt.overOnePair", "exists_readsAt_of_pair", "exists_orbitRep", "exists_settings"]) +
      many("dataties", ["TwCoverPair"]),
      ["L0/Q Galois", "TwCoverPair", "A supplied index i0", "No all-place reading conclusion"])
claim(21, "Finite integral bases and finite avoidance construct ExistsData",
      "The exact retained twisting hypotheses yield a basis S before every forbidden A and coherent GoodData with finite rational-prime avoidance.",
      ["RC20"], many("subbasis", ["exists_subbasis"]) +
      many("lattice", ["twOK_one", "th_fg", "exists_basisOf"]) +
      many("choice", ["TwistedPairSettingHyps", "FullRank", "exists_inputs", "GoodPack", "GoodData", "Apart", "ExistsData", "exists_finset_apart", "exists_apart_choice", "goodTw_union", "existsData"]) +
      many("ihf", ["FullRk", "BasisOf", "IdxAt", "GoodTw", "TwistTheoremAtIndex", "admT4", "aux₃", "adm7"]) +
      many("good", ["TwIn.Ok", "twEps", "twEps_pos"]),
      ["aux₃ for the exact D,bk0,expansion datum,N0", "TwistedPairSettingHyps, FullRank, adm7, TwCoverPair", "L0/Q Galois", "Pairwise Apart only asserted when twisted-place set is finite", "ReadElsewhere remains separate"])


for c in claims:
    for d in c["depends_on"]:
        if d.startswith("RC"):
            assert int(d[2:]) < int(c["id"][2:]), (c["id"], d)

remaining = []


def target(i, interface, scope, sources, supplied_by):
    remaining.append({
        "id": f"RC-next-{i:02d}", "interface": interface,
        "status": "retained_supplier", "scope": scope,
        "sources": sources, "conditional_work_completed": supplied_by,
    })


target(1, "Actual global Artin reciprocity map",
       "Supply the published GlobalArtinReciprocity with quotient, kernel, inertia, inverse-Frobenius uniformizer and decomposition clauses.",
       many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]), ["RC3", "RC4", "RC5"])
target(2, "Actual finite ring-class system and all-place coefficient coverage",
       "Supply one NTw with RCG/art_univ, roots, TwCover and the exact chosen index/side reading data. TwCoverPair only covers twisted places.",
       [interface_range("ntw", "NTw.RCG/art/art_univ", 388, 403, "retained arithmetic constructor interface"),
        interface_range("ntw", "NTw.TwCover", 450, 453, "retained all-place coverage interface")] +
       many("choice", ["ReadElsewhere", "readElsewhere_of_cover"]) + many("dataties", ["TwCoverPair"]),
       ["RC6", "RC8", "RC9", "RC20", "NC4"])
target(3, "Actual common MtFam and NExpTied realization data",
       "Supply MtReal/NExpTied for the same fixed rows, cells and character frame; their real maps, exact range, algebraic weights and local lattices are retained.",
       many("real", ["MtReal", "MtFam"]) + many("cell", ["MtVReal", "NExpTied"]), ["RC1", "RC2"])
target(4, "Actual Joint through the geometric/period comparison",
       "Reconstruct joint_of and its all-states supplier with the genuine MtAd, RatAd, SideB, NExpRealS, Series/Keep/Elem and exact eta interfaces.",
       many("joint", ["exists_iso", "joint_of", "joint"]) + many("lev", ["Joint"]), ["RC14", "RC15", "RC16", "RC19"])
target(5, "Actual CellWt highest-weight comparison",
       "Supply the representation-theoretic classification/base-change join and exact infinitesimal/highest-weight equality of cellWt_all; equality of dimensions does not suffice.",
       many("cellwt", ["cellWt_all"]) + many("lev", ["WtMatch", "CellWt"]), ["RC1", "RC2"])
target(6, "Actual local shapes, bad places, type places and ramified-unit nontriviality",
       "Supply the exact cell and MtFam local descriptions on the same stage; RC19 proves their local-to-global conclusion, not these suppliers.",
       many("parashape", ["paraShape_export"]) + many("unishape", ["levelUni_export"]) +
       many("bad", ["badV_sub_gPl_qPl"]) + many("ramunit", ["GlobalTheory.CompRamified.exists_unit_ne_one"]) +
       many("gplaces", ["gPlaces"]),
       ["RC14", "RC15", "RC16", "RC17", "RC18", "RC19"])
target(7, "Nonempty-local IsGalOf and index/side compatibility",
       "Supply IsGalOf(D,a,univ,psiL,chi(w(a)),0) and literal twOf/twSide identities for the same local stage. RC10 then proves common character and Q equality.",
       many("gal", ["IsGalOf", "NGalChrTied"]) + many("choice", ["LocsCarry"]) +
       [interface_range("ntw", "NTw local twist/psiL interface", 409, 424, "retained same-object local arithmetic data")], ["RC10"])
target(8, "Actual ColW/Pre2/RowPk/St simultaneous constructor",
       "Supply the actual row-lift, numerical, local-stage, geometric and period data. RC12 only resets tuple maps on an existing row model; RC13 verifies MuIsW on actual supplied objects.",
       many("rowexist", ["rowPk_nonempty"]) + many("muw", ["GlobalTheory.Mem.R3.Rw.exists_rowsRest_muW"]) +
       many("colw", ["ColW"]) + many("pre2", ["Pre2", "St"]) + many("rowpk", ["RowPk"]),
       ["RC12", "RC13", "NC16"])
target(9, "All-place simultaneous character, conductor and comparison hypotheses",
       "Supply the literal exists_choice hs/sc and h1–h8 together, including conductor avoidance, equal-center exponent/character coherence, roots and universal LevEq/CellWt for one D.",
       many("endpoint", ["exists_choice"]) + many("avoid", ["conductors_avoid_lowAll"]), ["RC11", "RC19"])
target(10, "Genuine twisting, full-rank and integral-inclusion hypotheses",
       "Prove aux₃, FullRank, adm7 and TwistedPairSettingHyps for the same expansion datum and BK setting. RC21 proves the finite basis and avoidance constructor, retaining GoodTw's full lattice-index and arithmetic inequalities.",
       many("ihf", ["aux₃", "TwistTheoremAtIndex", "GoodTw", "admT4", "adm7"]) +
       many("choice", ["FullRank", "TwistedPairSettingHyps"]), ["RC21"])
target(11, "Compatible rebuilding after a change of data",
       "A rebuilding operation must preserve the exact common fields/packets and supply RankTie and LocsCarry for its output; the bare empty-Tw stage cannot replace this join.",
       many("choice", ["Rebuild", "RebuildTied", "TwoSteps", "exists_madeFrom"]), ["RC2", "RC10", "RC11", "NC12"])
target(12, "Full choices_exist_for supplier chain",
       "The final all-states theorem retains DiscreteSeriesCover, CasselmanWallach, HarishChandraModules, PrN, SerN and universally quantified LocalLanglandsGL, with the actual geometric/local/weight suppliers above.",
       many("endpoint", ["choices_exist_for"]), ["RC11", "RC13", "RC19", "RC21"])

completed = []


def done(key, name, ids, scope):
    completed.append({
        "declaration": source(key, name)["declaration"],
        "status": "proved_conditionally", "supplied_by": ids,
        "scope": scope, "source": source(key, name),
    })


done("complexify", "finrank_typeSp_cx", ["RC1"], "Complete literal conditional scalar-extension theorem.")
done("endpoint", "rank_of_levEq", ["RC2"], "Complete actual rank equality under exact level and weight matches.")
done("finitegal", "galOf_of_orderDvd", ["RC3"], "Complete under the retained global Artin map.")
done("dense", "eq_one_of_frob", ["RC4"], "Complete under the exact Artin and continuity hypotheses.")
done("galprops", "galOf_twist_props", ["RC5"], "Complete anti/exact-ram/decomposition conclusion from GalOf and IsPsi.")
done("descent", "exists_pulls_twOK", ["RC6"], "Complete under retained actual NTw.art_univ.")
done("power", "pulls_eq_zpow", ["RC7"], "Complete power ambiguity with primitive roots.")
done("side", "reading_sidePl_emb", ["RC8"], "Complete literal side embedding and valuation reflection.")
done("complex", "exists_complex_emb", ["RC8"], "Complete algebraic complex embedding; no continuity assertion.")
done("endpoint", "exists_data", ["RC9"], "Complete coherent reading/descent selection under its exact input families.")
done("endpoint", "reads_of_pulls", ["RC9"], "Complete same-embedding SideRead and ReadsHecke join.")
done("endpoint", "exists_choice", ["RC11"], "Complete conditional endpoint; all same-D hypotheses retained.")
done("endpoint", "muIsW", ["RC13"], "Complete ten-field verification on actual ColW/Pre2/St.")
done("endpoint", "cfOf_eq", ["RC13"], "Complete literal character-frame identity.")
done("endpoint", "exists_tp", ["RC13", "NC16"], "Complete prescribed xi/psi TupTied under exact Q.")
done("parahoric", "mem_para_of_eig", ["RC14"], "Complete local scalar-action rigidity.")
done("orientation", "GlobalTheory.ParaOpp.splitPlace_eq_of_para", ["RC15"], "Complete opposite-orientation exclusion.")
done("additive", "fractionFieldToGenericStalk_algebraMap_eq", ["RC16"], "Complete additive-character identification under common power/scalar conditions.")
done("stabilizer", "exists_trivial_stabiliser", ["RC17"], "Complete actual trivial-stabilizer construction from type-prime fields.")
done("nonzero", "exists_form_of_trivial_stabiliser", ["RC18"], "Complete supported nonzero-form construction.")
done("endpoint", "levEq", ["RC19"], "Complete local-to-global level and character equality; exact Joint/local shapes retained.")
done("reads", "exists_settings", ["RC20"], "Complete selector, readings on twisted places only.")
done("choice", "exists_inputs", ["RC21"], "Complete actual integral basis selection under FullRank and adm7.")
done("choice", "existsData", ["RC21"], "Complete finite coherent/avoidance constructor under the exact twisting hypotheses.")

audits = [
    {"record": "TwOK", "field_count": 7, "supplied_by": ["RC5", "RC6"],
     "fields": ["split", "disjoint", "open", "anti", "cyclic-root image", "RamExactly", "TrivAbove"]},
    {"record": "ChoiceC", "field_count": 6, "supplied_by": ["RC7", "RC8", "RC9", "RC11"],
     "fields": ["twI_conj", "sd_place", "emb_side", "sd_conj", "one", "conj"]},
    {"record": "ChoiceSide", "field_count": 6, "supplied_by": ["RC11", "NC9", "NC12"],
     "fields": ["nct", "choice", "off", "adm", "psi", "eMt_level"]},
    {"record": "LocsCarry", "field_count": 4, "supplied_by": ["RC10"],
     "fields": ["twOf identity retained", "twSide identity retained", "Q equality derived", "common psiL identity derived"]},
    {"record": "MuW", "field_count": 3, "supplied_by": ["RC12"], "fields": ["tw", "on", "off"]},
    {"record": "MuIsW", "field_count": 10, "supplied_by": ["RC13"],
     "fields": ["inj", "range", "mu0", "star", "star'", "tw", "on", "off", "sub", "supp"]},
    {"record": "GoodData", "field_count": 4, "supplied_by": ["RC20", "RC21"],
     "fields": ["ReadsAt", "packet conjugation", "nonfixed side conjugation", "GoodPack"]},
    {"record": "ExistsData conjunction after quantified S,A,t,sd", "field_count": 4, "supplied_by": ["RC21"],
     "fields": ["GoodData", "A avoidance", "OverOnePair constancy", "finite-place Apart"]},
]
assert sum(a["field_count"] for a in audits) == 44

links = sum(len(c["sources"]) for c in claims)
unique = {(s["path"], s["line_start"], s["line_end"]) for c in claims for s in c["sources"]}
source_files = [{
    "path": p, "sha256": sha(b), "full_file_sha256": sha(b),
    "bytes": len(b), "line_count": len(b.splitlines()),
    "pinned_url": f"{URL}/blob/{COMMIT}/{p}",
    "verified_equal_to_pinned_git_blob": True,
} for p, b in sorted(cache.items())]
artifacts = [{
    "path": "arithmetic_compatibility/" + n, "sha256": sha((ROOT/n).read_bytes()),
    "bytes": (ROOT/n).stat().st_size,
} for n in ["main.tex", "report.txt", "build_provenance.py"]]
reviews = []
for name in ["root_reviews_arithmetic_compatibility.txt"]:
    path = ROOT.parent / "reviews_v0_18" / name
    if path.is_file():
        raw = path.read_bytes()
        checked = [cid for cid, info in paragraphs.items() if info["sha256"] in raw.decode()]
        assert checked, ("review does not identify any current paragraph", str(path))
        reviews.append({
            "file": "reviews_v0_18/" + name, "sha256": sha(raw),
            "current_paragraph_hashes_identified": checked,
            "scope_note": "Only paragraphs whose exact current hashes occur in the independent review are attached.",
        })

scope = (
    "RC1–RC21 prove actual rank/character/side/finite-choice/local-level and tuple compatibility under "
    "exact retained simultaneous inputs. The literal rank_of_levEq, exists_choice, muIsW, levEq, "
    "exists_settings and ExistsData endpoints are conditionally reconstructed. Global Artin reciprocity, "
    "the actual NTw universal property and coverage, Joint/local-shape/CellWt suppliers, actual "
    "ColW/Pre2/RowPk/St existence, and genuine twisting/full-rank/integral-inclusion hypotheses remain "
    "explicit. RC10 derives nonempty-local character and conductor ties from the exact Frobenius "
    "criterion while retaining index and side identities. No bare empty-Tw stage, arbitrary "
    "equal-dimensional model, or tuple reset is substituted for the required same-object construction. "
    "No complete Later/Pins or final RH/GRH conclusion is asserted."
)
provenance = {
    "artifact_version": "0.18", "component": "arithmetic_compatibility",
    "repository": URL, "commit": COMMIT, "scope": scope,
    "claim_count": len(claims), "source_link_count": links,
    "unique_claim_source_range_count": len(unique), "source_file_count": len(source_files),
    "claims": claims, "source_files": source_files, "proof_artifacts": artifacts,
    "record_audits": audits, "audited_conditional_field_count": 44,
    "retained_interface_count": len(remaining), "retained_inputs": remaining,
    "completed_targets": completed, "independent_reviews": reviews,
    "precision_notes": [
        "Inverse arithmetic Frobenius convention is preserved throughout.",
        "TwOK concerns the unnormalized character; packet side inversion is applied twice when extracting it.",
        "RC10 uses psiL_open for locally constant complex characters and never assumes continuity of Qbar_ell-to-C.",
        "RC11 assumes Loc empty but still requires all-place twist readings; LS empty-Tw cannot supply them.",
        "RC12 proves only the tuple-reset/MuW portion, not the complete weight/sha or RowPk supplier.",
        "ChoiceSide.eMt_level is a level/character assertion, not full Hecke equivariance or metric preservation of the NC basis map.",
        "RC20 only reads twisted places; RC21 preserves exists S before forall forbidden A and Apart only for finite twisted-place sets.",
        "The 44 audited clauses include conditional and retained subclauses; they are not a count of newly unconditionally constructed record fields.",
    ],
    "validation": {
        "read_only_source_access": True, "present_checkout_files_equal_pinned_blobs": True,
        "source_range_hashes_regenerated": True, "literal_record_fields_audited": True,
        "claim_dependency_order_acyclic": True, "lean_build_performed": False,
        "pdf_build_performed": False,
    },
}
manifest = {
    "artifact_version": "0.18", "component": "arithmetic_compatibility",
    "repository": URL, "commit": COMMIT, "source_file_count": len(source_files),
    "source_files": source_files, "proof_artifacts": artifacts,
}
targets = {
    "artifact_version": "0.18", "component": "arithmetic_compatibility",
    "repository": URL, "commit": COMMIT, "status": scope,
    "target_count": len(remaining), "targets": remaining,
    "retained_interface_count": len(remaining), "retained_interfaces": remaining,
    "completed_targets": completed,
}
for name, value in [("provenance.json", provenance), ("source_manifest.json", manifest), ("next_targets.json", targets)]:
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
lines = [
    "ARITHMETIC COMPATIBILITY RC1–RC21: PINNED SOURCE LOCATORS",
    f"Repository: {URL}", f"Commit: {COMMIT}",
    f"Claims: {len(claims)}; links: {links}; unique claim ranges: {len(unique)}; source files: {len(source_files)}.",
    f"Audited conditional clauses: 44; retained interface families: {len(remaining)}.",
    "Inclusive one-based source ranges are hashed from exact pinned Git bytes.",
    f"main.tex SHA256: {sha(main)}", f"report.txt SHA256: {sha(report)}", "",
]
for c in claims:
    lines += [c["id"] + ": " + c["title"], "  Proof paragraph SHA256: " + c["proof_location"]["sha256"]]
    for s in c["sources"]:
        lines += [
            f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['role']}",
            "    " + s["pinned_url"],
            f"    file SHA256 {s['full_file_sha256']}; range SHA256 {s['range_sha256']}",
        ]
    lines.append("")
lines += ["EXACT RETAINED INTERFACES"]
for t in remaining:
    lines += [t["id"] + ": " + t["interface"], "  " + t["scope"]]
    for s in t["sources"]:
        lines += [f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']}",
                  "    " + s["pinned_url"],
                  f"    file SHA256 {s['full_file_sha256']}; range SHA256 {s['range_sha256']}"]
(ROOT/"source_locators.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({
    "claims": len(claims), "source_links": links, "unique_claim_ranges": len(unique),
    "source_files": len(source_files), "audited_conditional_clauses": 44,
    "completed_targets": len(completed), "retained_interface_families": len(remaining),
    "main_sha256": sha(main), "report_sha256": sha(report),
}, indent=2))


