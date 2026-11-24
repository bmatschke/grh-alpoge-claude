#!/usr/bin/env python3
"""Rebuild NC provenance from pinned Git objects, without checkout mutation."""
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
    "closure": "src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/IsDiscreteValuationRingIntegralClosure.lean",
    "dvr": "src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/ExistsDvrExtensionEmbedding.lean",
    "descent": IE + "ExistsCharDescent.lean",
    "lattice": IE + "ExistsEquivMapLattice.lean",
    "reads": IE + "ExistsReadsAtOfCover.lean",
    "choice": IE + "ExistsTiedChoiceOfReads.lean",
    "nchoice": LC + "DataNChoice.lean",
    "nchtie": LC + "DataNChTie.lean",
    "d7": LC + "RhoDetPrimeEqMuTildeMulChiPow.lean",
    "rows": LC + "DataRows.lean",
    "ntw": LE + "DataN.lean",
    "normal": LE + "BlochKatoPhases.lean",
    "good": LE + "TwGood.lean",
    "hec": "src/Formalism/LocalToGlobal/UnitaryNorms/CharHost.lean",
    "tup": "src/Formalism/LocalToGlobal/UnitaryNorms/CharTied.lean",
    "twist": AM + "IsRationalUnitaryDeterminantMapRationalUnitaryTo.lean",
    "twdat": AM + "CmQuadraticFormEqAlternatingForm.lean",
    "muisw": AM + "RationalRootsDef.lean",
    "tup_good": IW + "TupTiedOfMuIs.lean",
    "support": IW + "ResCharConj.lean",
    "tuptied": IW + "TupTiedOfMuIsW.lean",
    "levcmp": IW + "StatementCOfCasselmanWallach.lean",
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
    full_name = ((ns + ".") if ns else "") + spelling
    if full_name.startswith("_root_."):
        full_name = full_name[7:]
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
text = main.decode()
assert not [c for c in text if ord(c) < 32 and c not in "\n\r\t"]
markers = list(re.finditer(r"(?m)^\\paragraph\{(NC\d+):", text))
assert [m.group(1) for m in markers] == [f"NC{i}" for i in range(1, 18)]
paragraphs = {}
for i, match in enumerate(markers):
    end = markers[i+1].start() if i+1 < len(markers) else len(text)
    part = text[match.start():end].encode()
    paragraphs[match.group(1)] = {
        "sha256": sha(part), "bytes": len(part),
        "line_start": text[:match.start()].count("\n") + 1,
        "line_end": text[:end].count("\n"),
    }
claims = []


def claim(i, title, statement, deps, sources, assumptions):
    cid = f"NC{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.17", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "arithmetic_choice/main.tex",
            "expanded": "arithmetic_choice/report.txt", "section": cid,
            **paragraphs[cid],
        },
        "sources": sources,
    })


d7_base = interface_range("d7", "Formalism.BasicNotions.D7 coefficient/place fields", 106, 140,
                          "retained number-field, Galois, conjugation and exact prime/valuation fields")
ntw_base = interface_range("ntw", "Formalism.BasicNotions.NTw coefficient-ring fields", 262, 303,
                           "retained DVR rings, base-field embeddings, injections, completeness and finite extensions")
mt_global = interface_range("rows", "Formalism.BasicNotions.Rows.Data Mt fields", 133, 145,
                            "retained complex form, coefficient form, basis and generator descent fields")
mt_local = interface_range("ntw", "Formalism.BasicNotions.NExp Mt fields", 833, 843,
                           "retained actual local fraction-field module and finite full lattice")
tuple_base = interface_range("rows", "Formalism.BasicNotions.Rows.Data tuple support fields", 51, 60,
                             "retained tuples and their conjugation/on-or-reference laws")

claim(1, "Finite complete DVR extensions in characteristic zero",
      "The integral closure in a finite characteristic-zero fraction-field extension is a finite free complete DVR and the base inclusion is injective and local.",
      [], many("closure", ["finite_integralClosure", "isDiscreteValuationRing_integralClosure", "isAdicComplete_maximalIdeal_of_finite"],
               "source supplier; NC proves the characteristic-zero instance by trace duality, idempotent lifting and the DVR criterion") +
      many("dvr", ["exists_complete_dvr_ext_numberField_sqrt"], "application interface; the square root is unnecessary when a=1"),
      ["A is a complete DVR whose fraction field has characteristic zero; K'/Frac(A) is finite.",
       "No finite-residue-field, unramifiedness or local-compactness hypothesis is introduced."])

claim(2, "Integral images and exact prime detection",
      "An embedding whose integral map contracts the DVR maximal ideal to p has exactly the p-valuation ring as inverse image; finite Galois prime transitivity aligns the contraction with a chosen p.",
      [], many("descent", ["exists_intMap", "induces_of_ideal", "exists_coeff_ext"]) + [d7_base],
      ["F is a number field; B is a DVR; the specified contraction equality is assumed.",
       "The prime-transitivity argument assumes a finite Galois extension and proves the needed inverse-image orientation."])

claim(3, "Actual finite coefficient extension at the selected prime",
      "Construct finite complete DVR B/A and L->Frac(B) extending the exact L0 embedding and reading the prescribed prime, with all denominator identities.",
      ["NC1", "NC2"], many("dvr", ["exists_finite_ext_numberField_sqrt", "exists_complete_dvr_ext_numberField_sqrt"]) +
      many("descent", ["exists_coeff_ext"]),
      ["L/Q is Galois, L0 is an intermediate field, A is a complete DVR, and the base-field prime is read correctly.",
       "This proves the full literal conditional exists_coeff_ext conclusion; no numerical valuation equality is asserted."])

claim(4, "Actual Reading, residue characteristic and the cover implication",
      "ReadsAt produces a Reading for every coefficient index; the actual injections are local, finite coefficient extensions complete, ell equals resChar, and TwCover implies ReadElsewhere.",
      ["NC1", "NC2", "NC3"], [ntw_base, d7_base] +
      many("normal", ["phiK"]) +
      many("reads", ["sideEmb", "ReadsAt", "l_mem_max", "ReadsAt.l_eq", "isLocalHom_phiK", "Reading",
                     "ReadsAt.nonempty_reading", "below", "mem_below", "resChar_mem_below", "exists_readsAt_of_cover"]) +
      many("ntw", ["TwCover"]) + many("choice", ["ReadElsewhere", "readElsewhere_of_cover"]),
      ["Supplied D7/NTw coefficient objects and exact ReadsAt prime condition.",
       "TwCover is retained when invoking its implication; its existence is not proved."])

claim(5, "Finite rational pullback of the complex generator set",
      "A semilinear rational form carrying a basis to a complex basis has finite dimension, is injective, and the exact pullback of any finite spanning generator set in its image is finite and spans rationally.",
      [], many("lattice", ["form_gen"]) + many("rows", ["OLat"]) + [mt_global],
      ["The supplied jMt_basis and MtLat_sub fields, and the actual finite complex-spanning MtLat.gen set."])

claim(6, "Rank and full lattice after scalar extension",
      "For A->B injective and Lambda finite full over A, Frac(B) tensor_A V preserves dimension and the B-span of 1 tensor Lambda is a full finite lattice.",
      [], many("lattice", ["baseChange_lattice"]) + many("nchoice", ["fracEquiv", "fracEquiv_tmul"]) + [mt_local],
      ["A and B are domains with an injective algebra map; Lambda is finitely generated and spans over Frac(A)."])

claim(7, "Semilinear matching of full DVR lattices",
      "Equal dimensions and a finite spanning source set yield a semilinear map taking every basis to a basis after field extension and taking its exact integral span to a prescribed full DVR lattice.",
      [], many("lattice", ["exists_equiv_map_lattice", "exists_semilinear"]) +
      many("descent", ["exists_subbasis"], "least-valuation minimal-generator argument supplying the freeness proof"),
      ["A field embedding L->Frac(B), B a DVR, a finite spanning source set, a full finite target lattice, and the exact dimension equality.",
       "No operator or metric compatibility is part of the conclusion."])

claim(8, "The literal exists_formsIso comparison",
      "Construct the actual Mt semilinear map with basis and generator-span comparisons whenever the supplied proposition c entails equality of ranks; use zero when c is false.",
      ["NC5", "NC6", "NC7"], many("choice", ["exists_formsIso"]) + [mt_global, mt_local],
      ["Supplied D7 row form and local finite full lattice; the conditional rank equality is retained."])

claim(9, "All 21 normalized NChoice fields and exact packet recovery",
      "Readings and RankTie give the full NChoice; its side-normalized character is inverted twice by packet extraction, recovering the original packet literally.",
      ["NC4", "NC8"], many("nchoice", ["NChoice"]) +
      many("choice", ["RankEq", "RankTie", "choiceOf", "choiceOfPack", "pack_choiceOf"]) +
      many("normal", ["psiAt"]) + many("good", ["TwPack", "twPack", "NChoicePack", "psiAt_psiAt"]),
      ["Readings and ReadsAt for every place; RankTie only at nonreference places and 1<=j<=m.",
       "The actual D7/NExp objects are fixed before this construction."])

claim(10, "Finite character descent and conjugate readings",
      "Primitive roots descend finite-exponent characters uniquely; conjugating the coefficient embedding and reversing the side pulls the same L-valued Galois character.",
      ["NC2", "NC4"], many("descent", ["exists_char_descent"]) +
      many("choice", ["Reading.Pulls", "HasReading", "ValuesIn", "psiAt_not", "psiAt_pow", "pull_inv", "exists_pull",
                      "Reading.Pulls.conj", "HasReading.conj", "exists_hasReading"]) +
      many("reads", ["exists_star_int", "exists_star", "sideEmb_not", "ReadsAt.conj", "Reading.conj", "star_root"]),
      ["ValuesIn supplies a primitive root and finite exponent; L0/Q is separately Galois for the conjugation assertion.",
       "The two coefficient embeddings obey their exact supplied conjugation relation."])

claim(11, "Coherent IsCharOf on conjugation orbits",
      "ValuesIn, compatible packets/opposite sides and L0/Q Galois give a common character invariant under conjugation, equal to 1 off the twisted support, with actual readings everywhere required.",
      ["NC4", "NC10"], many("choice", ["GoodData", "IsCharOf", "exists_isCharOf"]) +
      many("reads", ["exists_orbitRep"]) + many("good", ["TwistedAt", "twistedAt_conj"]),
      ["Exact reading and conjugation parts of GoodData; ValuesIn for every twisted packet; L0/Q Galois.",
       "LocsCarry for an independently specified local character is not a conclusion."])

claim(12, "The full tied choice and all five NChTie fields",
      "ReadElsewhere, twisted ReadsAt/RankTie, one fixed IsCharOf family and its same-object LocsCarry produce C:NChoice, NChTie and exact Records; supplied GoodData transports to TwConjAt/TwGoodAt.",
      ["NC4", "NC9"], many("nchtie", ["NChTie"]) +
      many("choice", ["Records", "Records.good", "LocsCarry", "ReadElsewhere", "exists_choice",
                      "exists_tied_choice_of_reads", "exists_tied_choice", "psiAt_one", "Reading.pulls_one"]) +
      many("good", ["TwConjAt", "TwGoodAt", "TwGoodOne"]),
      ["The same fixed psi0 satisfies IsCharOf and LocsCarry; RankTie and off-support coverage remain explicit.",
       "GoodData is used only for the additional goodness-transport conclusion."])

claim(13, "Necessary rank and reading conditions",
      "Any NChoice supplies RankTie for its extracted packet; a tied choice supplies ReadsAt and ReadElsewhere, and two tied choices have identical local index/side/Q at existing local objects.",
      ["NC4", "NC6", "NC9", "NC12"], many("choice", ["readsAt_of_tie", "readElsewhere_of_tie", "rankTie_of_choice", "tied_unique"]),
      ["An already constructed NChoice, and NChTie for the reading/local uniqueness statements.",
       "These converse statements are not used circularly to construct their own hypotheses."])

claim(14, "Finite tame characters and nontrivial twists",
      "All characters in T.set(f) have finite order, are trivial on F and tame; distinguished twists are nontrivial and the character/support sets are finite with conjugation invariance.",
      [], many("twdat", ["offSet", "TwDat", "TwDat.xiTw", "TwDat.set"]) +
      many("hec", ["IsDelta", "IsPsi"]) + many("twist", ["IsTwist"]) +
      many("tup_good", ["Good", "resFin_mul", "resInf_mul", "good_one", "Good.mul", "good_set"]) +
      many("support", ["exists_over", "finite_mem", "mul_ne_one", "resChar_conj", "finite_pl", "tw_fin"]),
      ["Supplied character frame f and TwDat T; their IsDelta and IsTwist fields are used literally.",
       "Existence/finiteness of primes over p is proved via the nonzero finite quotient of the integer ring."])

claim(15, "Exact finite support from MuIsW",
      "MuIsW implies muAt(w)!=mu0 iff w belongs to W, and W is finite and conjugation-stable.",
      ["NC14"], many("muisw", ["MuIsW"]) + many("tuptied", ["tupTied_of_muIsW"]) + [tuple_base],
      ["All ten MuIsW fields are retained on the same X,f,T,W,xi; W is not replaced by all places over T.pl."])

claim(16, "All twelve TupTied fields",
      "MuIsW and C.Q=T.Q on its exact support construct TupTied with tp.xi=xi and tp.psi=T.psi literally.",
      ["NC14", "NC15"], many("tup", ["TupTied", "CharFrame.delAt"]) +
      many("twdat", ["Fr.at"]) + many("tuptied", ["tupTied_of_muIsW"]),
      ["Supplied NChoice C, MuIsW and exact Q equality on W.",
       "No k'=T.k equality is required; no Galois/Hecke psi identification is inferred."])

claim(17, "Same-object arithmetic join and exact remaining frontier",
      "The tied choice and TupTied are constructed simultaneously on the prescribed packet Q; exact frame/xi equalities supply TX16's arithmetic arguments while its other premises remain.",
      ["NC12", "NC15", "NC16", "TX16"],
      many("choice", ["exists_tied_choice_of_reads", "exists_choice", "Records"]) +
      many("tuptied", ["tupTied_of_muIsW"]) + many("muisw", ["MuIsW"]),
      ["Same D=X.toD7, packet Q=T.Q on W, the fixed character compatibility of NC12, and MuIsW.",
       "For TX16, the literal frame and xi equalities and all its separate geometric/stage premises remain."])


def fields(key, name):
    loc = source(key, name, "literal record field audit")
    lines = blob(loc["path"]).decode().splitlines()[loc["line_start"]:loc["line_end"]]
    names = []
    for line in lines:
        m = re.match(r"^  \[?([A-Za-z_][A-Za-z_0-9'₂]*)\s*:", line)
        if m:
            names.append(m.group(1))
    return loc, names


audit_specs = [
    ("reads", "Reading", 11, {
        "Oe":"NC3–NC4", "cr":"NC1", "dom":"NC1", "dvr":"NC1",
        "alg":"NC3–NC4", "inj":"NC1–NC4", "fin":"NC1–NC4", "loc":"NC1–NC4",
        "emb":"NC3–NC4", "emb_w":"NC2–NC4", "emb_side":"NC3–NC4",
    }),
    ("nchoice", "NChoice", 21, {
        "twI":"NC9 prescribed packet", "twI_l":"NC4", "sd":"NC9 prescribed side",
        "Q":"NC9 prescribed packet", "k'":"NC9 prescribed packet",
        "psi'":"NC9 exact side normalization", "Oe":"NC4 Reading",
        "crOe":"NC4 Reading", "domOe":"NC4 Reading", "dvrOe":"NC4 Reading",
        "algOe":"NC4 Reading", "algOOe":"NC9 actual composite algebra", "towOe":"NC9 composite-map equality",
        "Oe_inj":"NC4 Reading", "Oe_fin":"NC4 Reading", "Oe_loc":"NC4 Reading",
        "embW":"NC4 Reading", "embW_w":"NC4 Reading",
        "eMt":"NC8–NC9", "eMt_basis":"NC8–NC9 under RankTie", "eMt_lat":"NC8–NC9 under RankTie",
    }),
    ("nchtie", "NChTie", 5, {
        "twOf_eq":"NC12 retained LocsCarry and Records",
        "twSide_eq":"NC12 retained LocsCarry and Records",
        "Q_eq":"NC12 retained LocsCarry and Records",
        "psi_eq":"NC10–NC12 same IsCharOf/LocsCarry witness",
        "embedding_baseField_condition":"NC4/NC12 exact Reading.emb_side",
    }),
    ("tup", "TupTied", 12, {
        "xi":"NC16 supplied xi", "xi_inj":"NC16 MuIsW.inj",
        "xi_fin":"NC14/NC16 MuIsW.range", "xi_triv":"NC14/NC16 MuIsW.range",
        "xi_tame":"NC14/NC16 MuIsW.range", "psi":"NC16 supplied T.psi",
        "trueColumnChoices_heckeChar_reference_eq_one":"NC16 MuIsW.mu0",
        "xi_star":"NC16 MuIsW.star", "xi_star'":"NC16 MuIsW.star'",
        "xi_tw":"NC16 MuIsW.tw and exact Fr.at",
        "psi_is":"NC15–NC16 exact Q equality and TwDat.psi_is",
        "psi_un":"NC15–NC16 MuIsW.supp",
    }),
]
audits = []
for key, name, count, mapping in audit_specs:
    loc, names = fields(key, name)
    assert len(names) == count, (name, names, count)
    assert set(names) == set(mapping), (name, names, mapping)
    audits.append({
        "record":loc["declaration"], "field_count":count, "source":loc,
        "fields":[{"name":n, "supplied_by":mapping[n]} for n in names],
        "scope":"Complete conditional construction; retained hypotheses are identified explicitly.",
    })
mu_loc, mu_fields = fields("muisw", "MuIsW")
assert len(mu_fields) == 10, mu_fields

completed_specs = [
    ("descent","exists_intMap","NC2"), ("descent","induces_of_ideal","NC2"),
    ("descent","exists_coeff_ext","NC3"),
    ("reads","ReadsAt.l_eq","NC4"), ("reads","isLocalHom_phiK","NC4"),
    ("reads","ReadsAt.nonempty_reading","NC4"), ("reads","exists_readsAt_of_cover","NC4"),
    ("choice","readElsewhere_of_cover","NC4"),
    ("lattice","form_gen","NC5"), ("lattice","baseChange_lattice","NC6"),
    ("lattice","exists_equiv_map_lattice","NC7"), ("lattice","exists_semilinear","NC7"),
    ("choice","exists_formsIso","NC8"), ("choice","choiceOf","NC9"),
    ("choice","choiceOfPack","NC9"), ("choice","pack_choiceOf","NC9"),
    ("descent","exists_char_descent","NC10"), ("reads","Reading.conj","NC10"),
    ("choice","exists_hasReading","NC10"), ("choice","HasReading.conj","NC10"),
    ("choice","exists_isCharOf","NC11"),
    ("choice","exists_choice","NC12"), ("choice","exists_tied_choice_of_reads","NC12"),
    ("choice","exists_tied_choice","NC12"), ("choice","Records.good","NC12"),
    ("choice","readsAt_of_tie","NC13"), ("choice","readElsewhere_of_tie","NC13"),
    ("choice","rankTie_of_choice","NC13"), ("choice","tied_unique","NC13"),
    ("tup_good","good_set","NC14"), ("support","tw_fin","NC14"),
    ("tuptied","tupTied_of_muIsW","NC16"),
]
completed = [{
    **source(key,name,"completed literal conditional endpoint or substantive prerequisite"),
    "completed_by":cid, "human_status":"proved_under_explicit_hypotheses",
    "remaining_human_scope":"None within the stated conditional conclusion.",
} for key,name,cid in completed_specs]

remaining = [
    {
        "id":"NC-next-A", "interface":"Actual D7 row and local coefficient models",
        "scope":"Supply the actual global Mt form and local NExp/NTw objects with their basis, generator, finite-lattice and coefficient-ring fields. NC works on these objects and does not construct all of D7.",
        "source_anchors":[d7_base, mt_global, mt_local, ntw_base],
    },
    {
        "id":"NC-next-B", "interface":"Same-packet RankTie, readings and off-support coverage",
        "scope":"Supply twist packets/sides with ReadsAt and the exact RankTie for every nonreference w and 1<=j<=m, plus ReadElsewhere or actual TwCover. A precise next rank route is LevCmp.rank_of_levEq with its true MtReal/NExpTied, LevEq, CellWt and complexification suppliers.",
        "source_anchors":many("choice",["RankEq","RankTie","ReadElsewhere"]) +
                         many("ntw",["TwCover"]) +
                         many("reads",["exists_settings"],"unreconstructed simultaneous index/side selector from TwCoverPair") +
                         many("levcmp",["rank_of_levEq"],"upstream exact rank supplier requiring its substantive level/weight interfaces"),
    },
    {
        "id":"NC-next-C", "interface":"Common finite Galois character with the exact local compatibility",
        "scope":"Supply one family satisfying IsCharOf and LocsCarry simultaneously. NC11 produces IsCharOf under ValuesIn and conjugation/Galois hypotheses, but not its equality with independently chosen psiL. Stronger Hecke-to-Galois reciprocity and ring-class descent remain distinct.",
        "source_anchors":many("choice",["ValuesIn","IsCharOf","LocsCarry"]) +
                         many("levcmp",["exists_choice"],"stronger same-character/choice-side supplier; assumes empty Loc and further reciprocity and level-rank inputs"),
    },
    {
        "id":"NC-next-D", "interface":"MuIsW and exact Q/frame/xi identities",
        "scope":"Supply MuIsW for the actual tuple assignment, Q of those same packets equal to T.Q on W, and the exact frame/xi identifications when invoking TX16. NC15–NC16 derive support and TupTied from these hypotheses.",
        "source_anchors":[mu_loc] + many("levcmp",["muIsW"],"upstream assembly from actual ColW/Pre2/St with prescribed tuple assignments"),
        "retained_record_field_count":10, "retained_record_fields":mu_fields,
    },
    {
        "id":"NC-next-E", "interface":"Optional good-packet selection and separate global existence",
        "scope":"Actual GoodData/GoodTw selectors, including auxiliary Hecke conditions and avoidance, remain if those stronger outputs are required. Later, Pins, analytic host/window supply and the final global branches are independent of NC.",
        "source_anchors":many("choice",["GoodData","ExistsData","existsData"],
                              "retained stronger good-packet supplier; NC proves only conditional transport of its supplied output"),
    },
]
source_files = []
for path in sorted(cache):
    raw = cache[path]
    source_files.append({
        "path":path,"sha256":sha(raw),"bytes":len(raw),"lines":len(raw.splitlines()),
        "commit":COMMIT,"url":f"{URL}/blob/{COMMIT}/{path}",
        "verified_equal_to_pinned_git_blob":True,
    })
artifacts = {}
for name in ["main.tex","report.txt","build_provenance.py"]:
    raw=(ROOT/name).read_bytes()
    artifacts[name]={"sha256":sha(raw),"bytes":len(raw)}
links=sum(len(c["sources"]) for c in claims)
unique={(s["path"],s["line_start"],s["line_end"],s["range_sha256"]) for c in claims for s in c["sources"]}
assert len(claims)==17 and len({c["id"] for c in claims})==17
for c in claims:
    for dep in c["depends_on"]:
        if dep.startswith("NC"):
            assert int(dep[2:])<int(c["id"][2:]),(c["id"],dep)
independent_reviews = []
for name, reviewer, numbers in [
    ("ca_reviews_nc_1_4_10_13.txt", "/root/global_frame", list(range(1, 5)) + list(range(10, 14))),
    ("vi_reviews_nc_5_9_14_17.txt", "/root/comparison_span", list(range(5, 10)) + list(range(14, 18))),
]:
    review_path = ROOT.parent / "reviews_v0_17" / name
    if review_path.exists():
        raw = review_path.read_bytes()
        body = raw.decode()
        assert sha(main) in body and sha(report) in body, (name, "reviewed proof artifact changed")
        paragraph_hashes = {}
        for number in numbers:
            claim = claims[number - 1]
            paragraph_hash = claim["proof_location"]["sha256"]
            assert paragraph_hash in body, (name, claim["id"], "reviewed paragraph changed")
            paragraph_hashes[claim["id"]] = paragraph_hash
        independent_reviews.append({
            "reviewer": reviewer, "result": "PASS", "claim_ids": list(paragraph_hashes),
            "review_record": "../reviews_v0_17/" + name,
            "review_record_sha256": sha(raw), "paragraph_sha256": paragraph_hashes,
            "main_sha256": sha(main), "report_sha256": sha(report),
            "lean_replay": False,
        })
scope = ("Actual conditional finite-DVR/valuation reading, normalized NChoice with full integral Mt comparison, "
         "NChTie and TupTied. RankTie, MuIsW, exact same-character LocsCarry and simultaneous packet/frame supply remain explicit.")
provenance = {
    "artifact_version":"0.17","component":"arithmetic_choice","repository":URL,"commit":COMMIT,
    "scope":scope,"claim_count":len(claims),"source_link_count":links,
    "unique_claim_source_range_count":len(unique),"source_file_count":len(source_files),
    "line_range_convention":"Inclusive one-based source lines; range hashes preserve exact pinned Git newline bytes.",
    "claims":claims,"record_audits":audits,"record_field_count":49,
    "record_field_count_scope":"11 Reading + 21 NChoice + 5 NChTie + 12 TupTied; ten retained MuIsW fields are not counted as constructed.",
    "proof_artifacts":artifacts,"source_files":source_files,
    "independent_reviews":independent_reviews,
    "completed_targets":completed,"retained_interfaces":remaining,
    "foundational_scope":[
        "Characteristic-zero complete DVR extension is proved by trace-dual bounds, idempotent lifting and an explicit DVR criterion.",
        "The more general arbitrary-characteristic integral-closure theorem in the source is not claimed.",
        "Number-field localizations at nonzero primes are DVRs; ordinary finite separable field algebra and the PID submodule theorem are explicit classical inputs.",
        "RankTie remains exact; scalar extension and arbitrary full-lattice matching do not supply it.",
        "No Hecke equivariance or metric preservation is claimed for eMt.",
        "Galois psi0 and Hecke T.psi are different data and are not conflated.",
    ],
    "validation":{
        "read_only_source_access":True,"present_checkout_files_equal_pinned_blobs":True,
        "source_range_hashes_regenerated":True,"literal_record_fields_audited":True,
        "claim_dependency_order_acyclic":True,"lean_build_performed":False,"pdf_build_performed":False,
    },
}
manifest = {
    "artifact_version":"0.17","component":"arithmetic_choice","repository":URL,"commit":COMMIT,
    "source_file_count":len(source_files),"source_files":source_files,"proof_artifacts":artifacts,
}
next_targets = {
    "artifact_version":"0.17","component":"arithmetic_choice","repository":URL,"commit":COMMIT,
    "status":"All assigned literal conditional NChoice/NChTie/TupTied endpoints are discharged; the next targets supply their exact simultaneous hypotheses.",
    "target_count":len(remaining),"targets":remaining,"completed_targets":completed,
    "retained_interface_count":len(remaining),"retained_interfaces":remaining,
    "precision_notes":[
        "NC9 applies psiAt twice when extracting a packet, so the character and Q are recovered literally.",
        "NC11's IsCharOf construction does not automatically supply LocsCarry for the chosen family.",
        "TupTied needs exact Q on W but not k'=T.k; stronger choice-side outputs can need more.",
        "The explicit same-frame and xi identifications are retained in the join to TX16.",
        "No complete Later/Pins, analytic host window or final RH/GRH conclusion is claimed.",
    ],
}
for name,obj in [("provenance.json",provenance),("source_manifest.json",manifest),("next_targets.json",next_targets)]:
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
locators = [
    "ARITHMETIC CHOICE (NC1–NC17): PINNED SOURCE LOCATORS",
    f"Repository: {URL}",f"Commit: {COMMIT}",
    f"Claims: {len(claims)}; source links: {links}; unique claim ranges: {len(unique)}; source files: {len(source_files)}.",
    f"Constructed record fields: 49; retained interface families: {len(remaining)}.",
    "Inclusive one-based ranges are hashed from pinned Git bytes.",
    f"main.tex SHA256: {sha(main)}",f"report.txt SHA256: {sha(report)}","",
]
for c in claims:
    locators += [c["id"]+": "+c["title"],"  Proof paragraph SHA256: "+c["proof_location"]["sha256"]]
    for s in c["sources"]:
        locators += [
            f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['role']}",
            "    "+s["pinned_url"],
            f"    file SHA256 {s['full_file_sha256']}; range SHA256 {s['range_sha256']}",
        ]
    locators.append("")
locators += ["RECORD FIELD AUDIT"]
for a in audits:
    locators.append(f"  {a['record']}: {a['field_count']} fields")
    locators += [f"    {f['name']} <- {f['supplied_by']}" for f in a["fields"]]
locators += ["","RETAINED BOUNDARY"]
for item in remaining:
    locators.append("  "+item["id"]+" "+item["interface"]+": "+item["scope"])
(ROOT/"source_locators.txt").write_text("\n".join(locators)+"\n")
print(json.dumps({
    "claims":len(claims),"source_links":links,"unique_claim_ranges":len(unique),
    "source_files":len(source_files),"record_fields":49,"completed_targets":len(completed),
    "retained_interface_families":len(remaining),
    "main_sha256":sha(main),"report_sha256":sha(report),
},indent=2))
