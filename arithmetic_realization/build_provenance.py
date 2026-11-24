#!/usr/bin/env python3
"""Rebuild AR provenance from pinned Git objects, without checkout mutation."""
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
ND = "src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/"
P = {
    'endpoint': IW + 'StatementCOfCasselmanWallach.lean',
    'lev': IW + 'ReadsHecke.lean',
    'bad': IW + 'BadPlacesSubOfAdmissibleTwist.lean',
    'extra': IW + 'TwistedTupleFiniteOrderPartUnramifiedAtTypePrime.lean',
    'qplaces': IW + 'QPlacesOfAdmissibleTwist.lean',
    'places': IW + 'CellPlacesOfAdmissibleTwist.lean',
    'tameeta': IW + 'CellPlacesMembershipTwist.lean',
    'realreading': IE + 'ExistsReadingRealSide.lean',
    'sread': IW + 'ReadsHeckeOfSideRead.lean',
    'dread': IW + 'ReadsHeckeOfSideReadCell.lean',
    'wildval': IW + 'CellQPlacesOfAdmissibleTwist.lean',
    'resart': IE + 'ResidueCharacterArtinTameGaloisEqTameValue.lean',
    'artunit': IW + 'ExistsIneOfUnit.lean',
    'wild': IW + 'OpenKerCharWildEqOneOfPowEqOne.lean',
    'localhecke': IW + 'TameHeckeCharacterSplitPlaceLocalComponent.lean',
    'paralocal': IW + 'LevelByPlacesParahoricAtConductorPlaceTameCharac.lean',
    'parashape': IW + 'SideReadHeckeOfAdmissibleTwist.lean',
    'addext': IW + 'ExistsAddCharCompletionOfResidueAddChar.lean',
    'psine': IW + 'RationalDatumCharactersNeOneAtFixedElementResidu.lean',
    'tau': IE + 'LevelCharactersTypePlacesEqLocalComponents.lean',
    'first': IE + 'FirstTwistCharacterEqLadicHeckeCharacter.lean',
    'block': ND + 'CharpolySmulOfProd.lean',
    'adic': IW + 'InertialOrderFifteenCharAuxiliaryPrimeSpec.lean',
    'compbase': IW + 'CompAtBaseCharacterMulUnramifiedEqTypeCharacter.lean',
    'unimem': IW + 'MemLevelIffUnipotentAtTypePlace.lean',
    'unichi': IW + 'LevelCharacterEqLocalFactorAtTypePlace.lean',
    'super': IW + 'ComplexTypePlaceCharacterEqSuperdiagAddCharMulLo.lean',
    'unishape': IW + 'SplitPlaceOfAdmissibleTwist.lean',
    'frame': IE + 'FrameKeepsMatricesSplitPlaceReductionLocal.lean',
    'level': IE + 'AlgebraicFormsLevelGroupEqTwistLevel.lean',
    'joint': IW + 'JointEtaOfAdmissibleTwist.lean',
    'mdesc': IE + 'NonzeroMatrixIntertwinerDescendsToSubfield.lean',
    'algdual': IE + 'IsAlgWeightOfContragredientHighestWeight.lean',
    'wdesc': IE + 'IrreducibleWeightDescendsToPolynomialModule.lean',
    'classify': IE + 'AlgebraicWeightDominantIsoExists.lean',
    'dualhw': IE + 'ContragredientPolynomialWeightUniqueHighestWeigh.lean',
    'cellwt': IW + 'CellWeightOfAdmissibleTwist.lean',
    'wtmatrix': IW + 'WeightMatricesMatchOfCoeffSpaceIso.lean',
    'bcmatrix': IW + 'MatchingMatricesOfBaseChangeRepresentation.lean',
    'admtwist': IE + 'AdmissibleTwistOfTwistingCharacter.lean',
    'fock': ND + 'TranslateMemCoefLatFn.lean',
    'minor': IE + 'FockMinorProductEqSignDualWeylExtremalVector.lean',
    'himage': IE + 'FockHarmonicValueSpaceMapEqDualWeylModuleFunctio.lean',
    'hinj': IE + 'HarmonicPolynomialEqZeroOfFunction.lean',
    'cinj': IE + 'CoeffPolynomialEqZeroOfVanishingOnGLFamily.lean',
    'wtembed': IE + 'ExistsWeightEmbeddingHarmonicPolynomialsLattices.lean',
    'levelchi': IE + 'AlgebraicLevelCharacterEqTwistLevelCharacter.lean',
    'pretie': IW + 'ExistsNewThetaDataSeriesClassSumsLattices.lean',
    'actual': AM + 'SubsetTwistExceptionalPlaces.lean',
    'sideb': AM + 'RingSpecNormalisedCharacterEq.lean',
    'choice': IE + 'ExistsTiedChoiceOfReads.lean',
    'ntw': LE + 'DataN.lean',
    'rowpk': AM + 'ReadPk.lean',
    'colw': AM + 'PositionOfIntro.lean',
    'pre2': AM + 'NonzeroPlacesOverPrimesLifts.lean',
    'orb': 'src/Development/AbelianVarietyTheory/Proofs/CuspFormEvaluations/CoefficientSpaceEqSpanOrbitExtremalVector.lean',
    'polyfn': 'src/Formalism/LocalToGlobal/Columns/PolyFnLemmas.lean',
    'coeflat': 'src/Formalism/LocalToGlobal/Columns/CoefModAt.lean',
    'artin': 'src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',
    'real': 'src/Formalism/LocalToGlobal/GaloisLevelStructure/TiedHecke.lean',
    'cell': 'src/Formalism/LocalToGlobal/NormalizedHeckeFactors/RingHomOfBaseOrderToFraction.lean',
    'gal': 'src/Formalism/LocalToGlobal/UnitaryNorms/CharGal.lean',
    'hostchar': 'src/Formalism/LocalToGlobal/UnitaryNorms/CharHost.lean',
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
markers = list(re.finditer(r"(?m)^\\paragraph\{(AR\d+):", tex))
assert [m.group(1) for m in markers] == [f"AR{i}" for i in range(1, 23)]
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
    cid = f"AR{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.19", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "arithmetic_realization/main.tex",
            "expanded": "arithmetic_realization/report.txt",
            "section": cid, **paragraphs[cid],
        }, "sources": sources,
    })


claim(1, "Exact bad-place inclusion and type-prime unramified twist",
      "The actual tuple ramification laws give badV subset gPl union qPl and the extra twist is unramified at each type prime.",
      [], many("bad", ["unr_of_twist", "not_unr_of_delta", "unr_of_mul_left", "unr_of_mul_right", "badV_sub_gPl_qPl"]) +
      many("extra", ["nat_not_mem_of_ne", "unrAt_xiTw"]),
      ["Same actual cell and eta=mu0*delta_l*psi_H", "Literal IsMu0, IsDelta, IsPsi and IsTwist laws"])
claim(2, "Exact halves and split-place separation",
      "The actual half equals qpOf; selected conductor and auxiliary primes separate, and cover every qPl place.",
      ["AR1"], many("realreading", ["half_eq_qpOf"]) +
      many("places", ["mem_of_conj", "not_mem_two", "same_v", "sep_gen", "cell_places_sep"]) +
      many("qplaces", ["unr_mul", "main"]),
      ["Pq chooses a prime over each real prime", "Actual QP/DP covering, exclusion and no-conjugate-pair fields", "Conjugation-stable split support"])
claim(3, "Tame residue and exact Artin local value",
      "Open-kernel prime-to-residue-characteristic inertia kills wild inertia; tame residue values agree with the specified Hecke local component.",
      ["RC3", "RC4"], many("wild", ["eq_one_of_wild_prime", "eq_one_of_wild"]) +
      many("wildval", ["tameVal_eq_one", "tameVal_wild_one"]) +
      many("artunit", ["exists_ine_of_unit"]) +
      many("resart", ["tameVal_eq_of_tameRep", "zpow_apply_root", "tameRep_zpow", "eq_res_locU", "res_zpow_eq_tameVal"]) +
      many("sread", ["tameVal_eq_locK", "main"]) +
      many("artin", ["IsGlobalArtin"]),
      ["Exact global Artin reciprocity, including local inverse-Frobenius convention", "Open kernel and the literal tame exponent", "Finite local ramification filtration and Hensel lifting"])
claim(4, "Auxiliary side signs and tame delta",
      "DeltaRead and SideRead identify the auxiliary character with side exponent epsilon_b; no additional inverse is inserted.",
      ["AR3", "RC3", "RC4"], many("dread", ["exists_gal", "delta_tame", "read_of_side", "delta_isHeckeOf", "tameVal_delta", "main"]) +
      many("tameeta", ["tameAt_mul", "tameAt_one", "eta_tameAt"]) +
      many("realreading", ["delta_tame"]) +
      many("localhecke", ["le_exp_neg_one_of_lt_one", "main"]),
      ["Actual order-15 DeltaRead", "Auxiliary norm congruent to 1 modulo 15", "Unitary finite Hecke characters and exact side embedding"])
claim(5, "Literal parahoric membership and local character",
      "At a selected conductor place the level is the specified parahoric and its character is the local eta value of the lower determinant.",
      ["AR2", "AR3", "AR4"], many("paralocal", ["locM_eq_one_of_ne", "intLift_one", "intLift_zero", "redMat_one", "gVal_one", "resRep_one", "mem_iff", "levelPara_loc"]) +
      many("parashape", ["paraShape_export"]) + many("lev", ["ParaShape"]),
      ["Actual cell local level definition and selected split component", "Separation and same SideRead", "Tame local component"])
claim(6, "Actual additive completion character",
      "A nontrivial residue additive character extends to the completion with the exact integral values and maximal-ideal kernel condition.",
      [], many("addext", ["charUnitC", "addChar_extend_subring", "red_eq_zero_of_lt_one", "exists_addChar_completion_lift_residue"]),
      ["Residue additive character and its nontriviality", "Divisibility of nonzero complex numbers", "Choice for the maximal extension"])
claim(7, "Normalized type base-character identification",
      "The normalized first Galois character and all-place cover give tau equal to the actual mu0 local component.",
      ["AR3", "RC4"], many("first", ["firstTwistCharacter_eq_ladic_heckeCharacter"]) +
      many("block", ["blockChar_val", "exists_shift", "exists_blockChar"]) +
      many("tau", ["GlobalTheory.TwInputs.tau_eq_locK"]) +
      many("compbase", ["isUnit_of_val_eq_one", "red_eq_zero_of_val_lt_one", "compAt_baseCharacter_mul_unramified_eq_typeCharacter_alt"]) +
      many("adic", ["exists_isGal"], "retained normalized algebraic adic-character constructor"),
      ["Actual NChiData and NormalizedCharacterCompatibility", "Bs.cover for all required places; not empty Tw", "Global Artin and actual IsAlgPos/AlmostIn coefficient containment"])
claim(8, "Literal type-prime unipotent level and character",
      "The type level is UniRT and its scalar is the superdiagonal additive character times the lower-determinant local component; psi0 and xi precede forall e.",
      ["AR1", "AR2", "AR6", "AR7"], many("psine", ["theta_xiRed_ne_one"]) +
      many("unimem", ["mem_iff_uniRT"]) +
      many("unichi", ["locM_eq_one", "intLift_one", "intLift_zero", "redMat_topR_one", "detT_one", "gVal_one", "loc_one_eq", "chi_eq_at"]) +
      many("super", ["red_zero", "intLift_coe", "sum_top", "supSum_small", "loc_read", "_root_.GlobalTheory.T.complex_typePlaceCharacter_eq_superdiag_addChar_mul_lowerDet"]) +
      many("unishape", ["levelUni_export"]),
      ["Actual rational datum psiU nontriviality", "Exact all-place reading/normalization of AR7", "Same tuple and selected type place"])
claim(9, "Identity-frame integrality and residue bridge",
      "An actual IdFrame preserves the integral entries and exact residue matrices at the specified split component.",
      [], many("frame", ["ALint_eq", "proj_tmul_one", "proj_mem", "proj_lt_one", "resS_iff", "castE", "castE_rfl", "castE_mem_iff", "resS_castE_iff", "frGL_one_val", "mem_St_one", "red_eq_local"]) +
      many("admtwist", ["IdFrame"]),
      ["Actual identity frame and host embeddings", "Specified localizations and residue maps"])
claim(10, "Common UniDat and the exact g-1 power",
      "Two actual UniDat descriptions have the same membership conditions and their unipotent characters agree after the source power g-1.",
      ["AR9"], many("joint", ["locM_eq_one", "red_eq_one", "umax_of_para", "inParah_of_para", "inLevG_of_uni", "UniDat", "ut_one", "mem_lev_of_red", "unipotentBlockLevel_unipotentFactor_independent_of_datum", "levFn_pow", "over_unique", "natCast_mem_of_over", "red_one'", "para_mem", "red_Q", "uni_mem", "chr_pow"]),
      ["Same actual block sizes, residue identifications and selected place sets", "Exact residue cardinality g", "No raw character equality asserted before taking the power"])
claim(11, "Actual geometric-arithmetic Joint",
      "MtAd/RatAd/SideB/SerAt with Keep, Elem and the actual tuple produce all Joint clauses using theta=id and the intersection scalar subgroup.",
      ["AR9", "AR10"], many("joint", ["ek_toKk", "hasLaw_one", "rdV_law", "exists_iso", "joint_of", "joint"]) +
      many("actual", ["MtAd", "RatAd", "SerAt"]) + many("lev", ["FrameAut", "Joint"]),
      ["One actual global realization and series reading", "Literal SerAt.join, or AR21 installed reading", "RatAd.psi and false-side conjugation", "Keep/Elem and exact tuple eta"])
claim(12, "Matrix descent and polynomiality from the dual",
      "A nonzero complex intertwiner of K-matrix families descends by a coefficient functional; dual polynomiality gives original IsAlgWeight by unitary inverse-conjugate-transpose.",
      [], many("mdesc", ["matrix_intertwiner_descends"]) + many("algdual", ["isAlgWeight_of_hwAtF_dual"]),
      ["Specified K-to-C embedding", "Literal HWAtF polynomial matrices", "Choice of a K-linear functional; no finite-generation assumption"])
claim(13, "Actual coefficient-field representation descent",
      "An irreducible K-representation with the specified dual weights is isomorphic over K to the canonical polynomial module, conditional on the two named complex representation inputs.",
      ["AR12"], many("wdesc", ["weight_descends"]) +
      many("classify", ["exists_equiv_VV"], "retained complex algebraic-representation classification") +
      many("dualhw", ["GlobalTheory.mtRatDual_hw"], "retained canonical contragredient highest-weight theorem"),
      ["Complex classification by VV", "Canonical dual highest-weight uniqueness", "Actual finite-dimensional irreducible representation and complete CM type"])
claim(14, "Actual CellWt and base-change matrices",
      "Strictly decreasing infinitesimal-character lists, CharSide and literal rhoW/parameter/bc fields give CellWt for every permitted embedding.",
      ["AR12", "AR13"], many("admtwist", ["eq_of_infOf_eq"]) +
      many("cellwt", ["match_mtwRat", "domWeight_ext", "cellWt_all"]) +
      many("wtmatrix", ["vvmatch_repr", "wtMatch_of_coef"]) +
      many("bcmatrix", ["bcmatch_main"]) + many("lev", ["WtMatch", "CellWt"]),
      ["Actual MtReal and NExpTied cell weight/parameter/bc fields", "Same side-compatible embedding and host CM involution", "Two retained representation inputs of AR13"])
claim(15, "Extremal orbit spans the field coefficient module",
      "Vandermonde extraction gives every divided-power word in the extremal orbit span, hence the dual Weyl tensor module under the explicit characteristic-zero identity.",
      [], many("orb", ["coeff_mem_of_eval_mem", "eval_rowGen", "isUnit_elem", "rowDiv_mem_of_stable", "applyWord_mem_of_stable", "orbit_stable", "dualWeyl_le_span_orbit", "prod_mem_span_prod", "trAct_ten", "VV_eq_span_orbit"]) +
      many("polyfn", ["dualWeyl_eq_weyl"], "retained characteristic-zero identity only"),
      ["Characteristic zero", "Literal dualWeyl_eq_weyl over the field", "No equality of integral Delta and nabla"])
claim(16, "Exact harmonic extremal sign and image",
      "Complementary minors give the product of reversal signs, and equivariance plus AR15 identifies the whole harmonic and coefficient-function images.",
      ["AR15"], many("minor", ["det_inv_rev", "aeval_minorPlus", "aeval_minorMinus", "sum_drops", "prod_exponents", "eval_extremal", "harmFn_delta"]) +
      many("himage", ["coefLin", "coefFn_actP", "invTrK_invTrK", "map_harm_eq"]) +
      many("fock", ["fockSubst", "fockGL", "harm", "fockPt", "aeval_fockPt_fockSubst", "harmFn"]),
      ["Actual good weight and Fock rank", "Exact determinant shifts and reversed negative-block indices", "Characteristic-zero input of AR15"])
claim(17, "Harmonic injectivity and canonical coefficient isomorphism",
      "Fock positivity, adjointness and the triangular big cell prove harmonic injectivity; coefficient evaluation is injective, yielding the unique equivariant isomorphism Psi.",
      ["AR16"], many("hinj", ["fockL_fockSubst_adj", "fockSubst_delta_eig", "aeval_delta_unitri", "exists_ul", "continuousAt_lsub", "ev_det", "eq_zero_of_triangular", "fock_pos", "compare", "orth_end", "substRep", "harm_inj"]) +
      many("cinj", ["eq_zero_of_coefFn_id_eq_zero"]) +
      many("wtembed", ["cfn", "cfn_apply", "cfn_injective", "coefFn_eq_cfn", "exists_psi", "psi_inj", "psi_rhoVr"]),
      ["Positive Fock pairing and actual mixed substitution", "Harmonic orbit-span definition", "AR15 only for common-image/isomorphism part, not injectivity"])
claim(18, "All five WtMap properties",
      "The actual base-change basis and Psi give an injective equivariant harmonic map; the lattice image and denominator clauses follow from the full coefficient lattice.",
      ["AR13", "AR17"], many("wtembed", ["domWeight_eq", "mapK", "mapVV_mapK", "sumMap", "sumMap_apply", "linInd_mapVV", "mem_coefLat_iff", "exists_wtMap"]) +
      many("admtwist", ["WtMap"]) + many("coeflat", ["nabAtr_isLattice"]) +
      many("realreading", ["exists_wtMap"]),
      ["Actual good base and identity frame", "Specified coefficient-ring chain with e f s=iota", "Literal IsCoefRing and base-change matrices", "Full actual lattice"])
claim(19, "Global level and character agreement",
      "Entrywise identity-frame reductions, exact selected halves and all literal local factors give LevMatch for arbitrary global level elements.",
      ["AR2", "AR4", "AR9"], many("level", ["blockSizes_sub_eq_twoBlock", "mem_levJ_iff", "loc_zero", "loc_one", "cast_surj", "inParah_iff", "inLevG_iff", "UT_iff", "rTup_mem_iff", "levMem"]) +
      many("levelchi", ["resRep_spec", "psiU_prod", "secondBlock_blockOf_eq_blockTwo", "detRed", "qPlace", "typePlace", "levChi_read"]) +
      many("realreading", ["levMatch"]) + many("admtwist", ["LevMatch"]),
      ["Same IdFrame and actual global level definitions", "Exact QP/DP/series half identities", "Same SideRead, tame auxiliary values and type characters"])
claim(20, "Integral global forms and rational spanning",
      "The pointwise reading is injective, contains every integral geometric form, and its integral preimage spans after a finite double-coset denominator product.",
      ["AR18", "AR19"], many("admtwist", ["finite_kP", "isOfFinOrder_levFn", "mem_range_of_finOrder", "read_abstract", "read_cell"]),
      ["Actual realization with the exact form-space range", "Finite double-coset quotient", "Integrally closed coefficient ring", "All five WtMap properties"])
claim(21, "Actual constructed reading and installed SerAt.join",
      "The explicit reading has all three range/span/injectivity properties and supplies the literal SerAt.join when the same reading is installed in the series tie.",
      ["AR14", "AR18", "AR19", "AR20"], many("realreading", ["exists_reading", "exists_idFrame"]) +
      many("pretie", ["exists_preTie"], "only the actual reading/join installation portion reconstructed") +
      many("actual", ["SerAt"]),
      ["Full actual exists_reading input list", "Pinned good setup, scalar normalization, faithful reading and theta/class-sum installation", "Literal CellTie.rdV equals the constructed reading; no replacement of unrelated rdV"])
claim(22, "RankTie and the precise simultaneous-choice boundary",
      "AR local shapes, Joint and CellWt feed RC19 and RC1–RC2 to give actual LevEq and RankTie; exact LocsCarry and MuIsW same-object inputs remain separate.",
      ["AR1", "AR5", "AR8", "AR11", "AR14", "AR21", "RC1", "RC2", "RC10", "RC11", "RC13", "RC19", "NC12", "NC16"],
      many("endpoint", ["levEq", "rank_of_levEq", "exists_choice", "muIsW", "choices_exist_for"]) +
      many("choice", ["RankTie", "LocsCarry", "ReadElsewhere"]) +
      many("sideb", ["SideB"]),
      ["One actual compatible stage and all exact global realization inputs", "Nonvacuous all-place twist coverage", "Actual local IsGalOf/index/side ties and ColW/Pre2/RowPk/St for the downstream joins"])

for c in claims:
    for d in c["depends_on"]:
        if d.startswith("AR"):
            assert int(d[2:]) < int(c["id"][2:]), (c["id"], d)

remaining = []


def target(i, interface, scope, sources, completed):
    remaining.append({
        "id": f"AR-next-{i:02d}", "interface": interface,
        "status": "retained_supplier", "scope": scope,
        "sources": sources, "conditional_work_completed": completed,
    })


target(1, "Exact global Artin reciprocity",
       "Retain the published reciprocity map with its local inertia and inverse-Frobenius clauses; AR3 reconstructs the tame comparison using that map.",
       many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]), ["AR3", "AR4", "AR7"])
target(2, "Actual normalized algebraic adic-character realization",
       "Supply exists_isGal with the actual IsAlgPos, adic coefficient ring, AlmostIn and compatible embeddings; this is stronger than a complex finite-order character or HFrame alone.",
       many("adic", ["exists_isGal"]) + many("block", ["exists_shift", "exists_blockChar"]) +
       many("first", ["firstTwistCharacter_eq_ladic_heckeCharacter"]),
       ["AR7", "AR8"])
target(3, "Complex algebraic rational-unitary representation classification",
       "Prove the complete exists_equiv_VV for the source's IsAlgWeight and irreducible rational-unitary representation. AR13 descends that classification; it does not prove the complex classification itself.",
       many("classify", ["exists_equiv_VV"]), ["AR13", "AR14", "AR18"])
target(4, "Canonical dual highest-weight theorem",
       "Supply the exact conjugate-CM-type contragredient highest-weight theorem mtRatDual_hw, including polynomiality and weight uniqueness.",
       many("dualhw", ["GlobalTheory.mtRatDual_hw"]), ["AR13", "AR14"])
target(5, "Characteristic-zero dual-Weyl equality",
       "Retain dualWeyl_eq_weyl over a field of characteristic zero; its source uses the standard bideterminant basis and integral rational-saturation theorem. No integral equality is asserted.",
       many("polyfn", ["dualWeyl_eq_weyl"]), ["AR15", "AR16", "AR17", "AR18"])
target(6, "Compatible nonempty twist/local data and all-place normalized coverage",
       "Construct one actual NTw/SideB with the required nonempty all-place cover, NChiData and NormalizedCharacterCompatibility on the same D. The bare empty-Tw LS stage cannot provide this.",
       many("sideb", ["SideB"]) + many("tau", ["GlobalTheory.TwInputs.tau_eq_locK"]) +
       [interface_range("ntw", "NTw.TwCover", 450, 453, "retained all-place coverage interface")],
       ["AR7", "AR8", "AR22"])
target(7, "Actual common global representation and realization structures",
       "Supply compatible MtReal/MtFam/MtAd and NExpTied cells, including irreducibility, polynomial/highest-weight parameters, local lattices and base-change fields; equal dimensions alone do not supply them.",
       many("real", ["MtReal", "MtFam"]) + many("cell", ["MtVReal", "NExpTied"]) +
       many("actual", ["MtAd", "RatAd"]), ["AR11", "AR14", "AR18", "AR22"])
target(8, "Pinned setup and same-reading series installation",
       "Supply the full good pinned setup, scalar normalization, faithful reading, theta/class-sum installation, Hecke tie and universal-character fields of exists_preTie; install exactly the reading constructed by AR21.",
       many("pretie", ["exists_preTie"]) + many("actual", ["SerAt"]), ["AR11", "AR21"])
target(9, "Exact local Galois/index/side join for LocsCarry",
       "Supply actual local IsGalOf(D,a,univ,psiL,chi(w(a)),0) and literal twOf/twSide identities; RC10 derives character and support equality once these hold.",
       many("gal", ["IsGalOf", "NGalChrTied"]) + many("choice", ["LocsCarry"]) +
       [interface_range("ntw", "NTw local character/index/side data", 409, 424, "retained exact local compatibility")],
       ["AR22", "RC10"])
target(10, "Simultaneous choice and ColW/Pre2/RowPk/St data",
       "Supply the full same-object choice hypotheses and actual ColW/Pre2/RowPk/St identities. The conditional exists_choice and MuIsW verifications are already proved; their witnesses must be compatible with this stage.",
       many("endpoint", ["exists_choice", "muIsW", "choices_exist_for"]) +
       many("colw", ["ColW"]) + many("pre2", ["Pre2", "St"]) +
       many("rowpk", ["RowPk"]), ["AR22", "RC11", "RC13", "NC12", "NC16"])

completed = []


def done(key, name, ids, scope):
    s = source(key, name)
    completed.append({"declaration": s["declaration"],
                      "status": "proved_conditionally", "supplied_by": ids,
                      "scope": scope, "source": s})


done("bad", "badV_sub_gPl_qPl", ["AR1"], "Complete literal bad-place conclusion under the character and admissibility laws.")
done("extra", "unrAt_xiTw", ["AR1"], "Complete exact type-prime unramified extra factor.")
done("realreading", "half_eq_qpOf", ["AR2"], "Complete equality of the two actual half constructions.")
done("places", "cell_places_sep", ["AR2"], "Complete separation of the actual selected places.")
done("qplaces", "main", ["AR2"], "Complete actual qPl coverage by selected halves.")
done("sread", "tameVal_eq_locK", ["AR3"], "Complete tame local comparison under the retained specified Artin map.")
done("dread", "delta_isHeckeOf", ["AR4"], "Complete side-normalized auxiliary reading.")
done("dread", "tameVal_delta", ["AR4"], "Complete exact auxiliary tame exponent.")
done("parashape", "paraShape_export", ["AR5"], "Complete actual local parahoric description under source premises.")
done("addext", "exists_addChar_completion_lift_residue", ["AR6"], "Complete additive completion-character construction.")
done("tau", "GlobalTheory.TwInputs.tau_eq_locK", ["AR7"], "Complete conditional normalized type-character comparison; adic realization and all-place cover retained.")
done("unishape", "levelUni_export", ["AR8"], "Complete exact unipotent description, with characters chosen before all embeddings.")
done("frame", "red_eq_local", ["AR9"], "Complete entrywise identity-frame residue bridge.")
done("joint", "unipotentBlockLevel_unipotentFactor_independent_of_datum", ["AR10"], "Complete actual UniDat unipotent comparison.")
done("joint", "exists_iso", ["AR11"], "Conditionally complete helper: supplied Keep.grp gives the place equivalence and residue isomorphisms; transport along its place equality and apply its entrywise equation to eG.symm(cG.symm g). This proves the exact inverse-cG reindexing, not existence of Keep.")
done("joint", "joint_of", ["AR11"], "Complete Joint on the actual supplied global/series structures.")
done("joint", "joint", ["AR11"], "Complete actual on-support wrapper, preserving the tuple identity.")
done("mdesc", "matrix_intertwiner_descends", ["AR12"], "Complete matrix descent, including infinitely many intertwining equations.")
done("algdual", "isAlgWeight_of_hwAtF_dual", ["AR12"], "Complete polynomiality from the literal dual HWAtF.")
done("wdesc", "weight_descends", ["AR13"], "Complete field descent conditional on the two named complex representation inputs.")
done("cellwt", "cellWt_all", ["AR14"], "Complete actual CellWt under actual weight fields and retained classification inputs.")
done("orb", "VV_eq_span_orbit", ["AR15"], "Complete orbit-span proof conditional on characteristic-zero dualWeyl_eq_weyl.")
done("minor", "harmFn_delta", ["AR16"], "Complete exact extremal sign and determinant identity.")
done("himage", "map_harm_eq", ["AR15", "AR16"], "Complete harmonic image identity under the stated characteristic-zero input.")
done("hinj", "harm_inj", ["AR17"], "Complete direct Fock-positive harmonic injectivity.")
done("cinj", "eq_zero_of_coefFn_id_eq_zero", ["AR17"], "Complete coefficient-function injectivity.")
done("wtembed", "exists_wtMap", ["AR17", "AR18"], "All five actual WtMap clauses, including image and denominators.")
done("realreading", "levMatch", ["AR19"], "Complete arbitrary-global-element group and character comparison.")
done("admtwist", "read_cell", ["AR20"], "Complete pointwise reading with integral-image and rational-span properties.")
done("realreading", "exists_reading", ["AR21"], "Complete conditional reading constructor for all cells and exact pointwise join.")
done("endpoint", "rank_of_levEq", ["AR22", "RC1", "RC2", "RC19"], "Actual rank conclusion with local comparison suppliers reconstructed and global simultaneous premises retained.")

audits = [
    {"record": "WtMap", "field_count": 5, "supplied_by": ["AR18"],
     "fields": ["injective", "harmonic image", "rational equivariance", "geometric lattice contained in image", "nonzero scalar makes each value integral"]},
    {"record": "exists_reading conclusion", "field_count": 4, "supplied_by": ["AR20", "AR21"],
     "fields": ["injective reading", "all integral forms in range", "integral preimage spans", "exact pointwise omega/real join"]},
]
links = sum(len(c["sources"]) for c in claims)
unique = {(s["path"], s["line_start"], s["line_end"]) for c in claims for s in c["sources"]}
source_files = [{
    "path": p, "sha256": sha(b), "full_file_sha256": sha(b),
    "bytes": len(b), "line_count": len(b.splitlines()),
    "pinned_url": f"{URL}/blob/{COMMIT}/{p}",
    "verified_equal_to_pinned_git_blob": True,
} for p, b in sorted(cache.items())]
artifacts = [{
    "path": "arithmetic_realization/" + n, "sha256": sha((ROOT/n).read_bytes()),
    "bytes": (ROOT/n).stat().st_size,
} for n in ["main.tex", "report.txt", "build_provenance.py"]]
reviews = []
for name in ["root_reviews_arithmetic_realization.txt"]:
    path = ROOT.parent / "reviews_v0_19" / name
    if path.is_file():
        raw = path.read_bytes()
        checked = [cid for cid, info in paragraphs.items() if info["sha256"] in raw.decode()]
        assert checked, ("review does not identify any current paragraph", str(path))
        reviews.append({
            "file": "reviews_v0_19/" + name, "sha256": sha(raw),
            "current_paragraph_hashes_identified": checked,
            "scope_note": "Only paragraphs whose exact current hashes occur in the independent review are attached.",
        })
scope = (
    "AR1–AR22 reconstruct actual bad-place, selected-half, tame, parahoric, unipotent, "
    "identity-frame, Joint, CellWt and harmonic integral-reading comparisons on one fixed D. "
    "They feed the prior RC local-to-global level and rank proof. Global Artin, normalized "
    "algebraic adic-character realization, two named complex highest-weight inputs, "
    "the characteristic-zero dual-Weyl identity, compatible nonempty twist/local coverage, "
    "actual common global realizations and same-reading series installation remain explicit. "
    "No full exists_preTie, LocsCarry, ColW/Pre2/RowPk/St existence, arbitrary reading "
    "replacement, integral Delta=nabla identity or unconditional RH/GRH conclusion is asserted."
)
provenance = {
    "artifact_version": "0.19", "component": "arithmetic_realization",
    "repository": URL, "commit": COMMIT, "scope": scope,
    "claim_count": len(claims), "source_link_count": links,
    "unique_claim_source_range_count": len(unique), "source_file_count": len(source_files),
    "claims": claims, "source_files": source_files, "proof_artifacts": artifacts,
    "record_audits": audits, "audited_conditional_field_count": 9,
    "retained_interface_count": len(remaining), "retained_inputs": remaining,
    "completed_targets": completed, "independent_reviews": reviews,
    "precision_notes": [
        "All primes, cells, halves, embeddings, tuples and representations belong to the same supplied datum D.",
        "Tame Artin comparison retains the actual inverse-arithmetic-Frobenius convention.",
        "The auxiliary norm may be a prime power; its congruence modulo 15 makes its residue characteristic coprime to 15.",
        "The type tau value has the positive convention; false-side conjugation cancels RatAd.psi only in Joint.",
        "The local characters in levelUni_export are chosen before forall complex embeddings.",
        "AR13 uses a minimal complex invariant subspace and matrix-functional descent, not absolute irreducibility.",
        "Characteristic-zero Delta=nabla is retained over a field; no integral equality is inferred.",
        "Fock plus substitution uses inverse coefficients and minus substitution uses transpose coefficients.",
        "WtMap includes both lattice-image and denominator clauses; neither follows from equal dimensions alone.",
        "SerAt.join is proved for the installed constructed reading, not for an unrelated pre-existing rdV.",
        "Bs.cover requires genuine all-place twist coverage; empty Tw is not a substitute.",
        "The retained full NumbersIn field belongs to the separate TT analysis.",
    ],
    "validation": {
        "read_only_source_access": True, "present_checkout_files_equal_pinned_blobs": True,
        "source_range_hashes_regenerated": True, "literal_record_fields_audited": True,
        "claim_dependency_order_acyclic": True, "lean_build_performed": False,
        "pdf_build_performed": False,
    },
}
manifest = {
    "artifact_version": "0.19", "component": "arithmetic_realization",
    "repository": URL, "commit": COMMIT, "source_file_count": len(source_files),
    "source_files": source_files, "proof_artifacts": artifacts,
}
targets = {
    "artifact_version": "0.19", "component": "arithmetic_realization",
    "repository": URL, "commit": COMMIT, "status": scope,
    "target_count": len(remaining), "targets": remaining,
    "retained_interface_count": len(remaining), "retained_interfaces": remaining,
    "completed_targets": completed,
}
for name, value in [("provenance.json", provenance), ("source_manifest.json", manifest), ("next_targets.json", targets)]:
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
lines = [
    "ARITHMETIC REALIZATION AR1–AR22: PINNED SOURCE LOCATORS",
    f"Repository: {URL}", f"Commit: {COMMIT}",
    f"Claims: {len(claims)}; links: {links}; unique claim ranges: {len(unique)}; source files: {len(source_files)}.",
    f"Audited conditional clauses: 9; retained interface families: {len(remaining)}.",
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
    "source_files": len(source_files), "audited_conditional_clauses": 9,
    "completed_targets": len(completed), "retained_interface_families": len(remaining),
    "main_sha256": sha(main), "report_sha256": sha(report),
}, indent=2))


