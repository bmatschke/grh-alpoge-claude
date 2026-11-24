#!/usr/bin/env python3
"""Rebuild MR provenance from pinned Git blobs without checkout mutation."""
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
P = {'HeckeOperatorKeepsRationalIntegralLevelForms.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeOperatorKeepsRationalIntegralLevelForms.lean', 'MemRationalGLOfUnitaryGroupGramUnitGram.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/MemRationalGLOfUnitaryGroupGramUnitGram.lean', 'IsIrreducibleBaseChangeWeightTensorDualRepOfEmbe.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/IsIrreducibleBaseChangeWeightTensorDualRepOfEmbe.lean', 'IsCentralGroupAlgebraIdempotentUniversal.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/IsCentralGroupAlgebraIdempotentUniversal.lean', 'ExistsWeightDataIntegral.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsWeightDataIntegral.lean', 'LocalisationHeckeRingIsLocalRing.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LocalisationHeckeRingIsLocalRing.lean', 'LevelUnipotentGenericCharTypePlace.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LevelUnipotentGenericCharTypePlace.lean', 'DefiniteLevelFormsIffStdGroupTypeSpace.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/DefiniteLevelFormsIffStdGroupTypeSpace.lean', 'WeightTensorDualRepDualHighestWeightAtEmbedding.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/WeightTensorDualRepDualHighestWeightAtEmbedding.lean', 'StdFrameLevelSubgroupBoundedOpenHyperspecial.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/StdFrameLevelSubgroupBoundedOpenHyperspecial.lean', 'UniversalCharacterAdmissibleConductorInertiaSurj.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/UniversalCharacterAdmissibleConductorInertiaSurj.lean', 'SideIn.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SideIn.lean', 'SideRationalEigenData.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SideRationalEigenData.lean', 'RowCuspMultiplicityInput.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/RowCuspMultiplicityInput.lean', 'ExponentAndTwistData.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExponentAndTwistData.lean', 'PlacesOverRealSubfieldSplit.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/PlacesOverRealSubfieldSplit.lean', 'ExtLvlFormMemCutSp.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExtLvlFormMemCutSp.lean', 'SideRationalLevelData.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SideRationalLevelData.lean', 'GenericUnipotentCharacterAtSideEqThetaSide.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/GenericUnipotentCharacterAtSideEqThetaSide.lean', 'HeckeDoubleCosetOperatorsStandardFacts.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeDoubleCosetOperatorsStandardFacts.lean', 'AdelicFormFunctionValuesMemCoefficientLattice.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/AdelicFormFunctionValuesMemCoefficientLattice.lean', 'TwistLiftFormsEqBaseChangeRationalDatumForms.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TwistLiftFormsEqBaseChangeRationalDatumForms.lean', 'ExistsPadicFiniteExtContainingAllHeckeEigenvalue.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsPadicFiniteExtContainingAllHeckeEigenvalue.lean', 'SpanRangeEquiv.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SpanRangeEquiv.lean', 'InfinitesimalCharacterHalfIntegral.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/InfinitesimalCharacterHalfIntegral.lean', 'HeckeStableRationalLattice.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeStableRationalLattice.lean', 'EigSpanOfIsotInternal.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EigSpanOfIsotInternal.lean', 'RhoStabChiInLL0.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/RhoStabChiInLL0.lean', 'HasTameBlockCharacterTypePlaceNotOverL.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HasTameBlockCharacterTypePlaceNotOverL.lean', 'CoefficientSpaceDefiniteFormIrreducibleAlgebraic.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/CoefficientSpaceDefiniteFormIrreducibleAlgebraic.lean', 'NonemptySpec.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/NonemptySpec.lean', 'LatticeBasisFreeModulePlace.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LatticeBasisFreeModulePlace.lean', 'RamifiedLevelEqParahoricWithTupleCharacter.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/RamifiedLevelEqParahoricWithTupleCharacter.lean', 'HeckeEigenspaceNeBotEveryLocalisationPoint.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeEigenspaceNeBotEveryLocalisationPoint.lean', 'LatticeBaseChangeFreeOverLocalisationCoeffRing.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LatticeBaseChangeFreeOverLocalisationCoeffRing.lean', 'WeightTensorRepOfEmbeddingsIsIrreducible.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/WeightTensorRepOfEmbeddingsIsIrreducible.lean', 'HeckeRingActsOnLatticeAsOperators.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeRingActsOnLatticeAsOperators.lean', 'IsProdLevelStdFrameTwoBlockUnipotentLevel.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/IsProdLevelStdFrameTwoBlockUnipotentLevel.lean', 'SideRationalHeckeData.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SideRationalHeckeData.lean', 'HeckeRingActsFaithfullyOnLocalisedLattice.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeRingActsFaithfullyOnLocalisedLattice.lean', 'ExistsSignatureDataSpan.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsSignatureDataSpan.lean', 'ExistsLevelGroupWithCharacterAtTypePlaces.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLevelGroupWithCharacterAtTypePlaces.lean', 'ExistsLiftFormsAdelicDecoratedLattices.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLiftFormsAdelicDecoratedLattices.lean', 'HeckeComparisonUnitAtFrobeniusEqDelta.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeComparisonUnitAtFrobeniusEqDelta.lean', 'HeckeOperatorsOnLocalisationSpaceSemisimple.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeOperatorsOnLocalisationSpaceSemisimple.lean', 'BaseChangeInfLatticeEqSubspace.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/BaseChangeInfLatticeEqSubspace.lean', 'InfOfLamLdefEqParamV.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/InfOfLamLdefEqParamV.lean', 'TwistedLatticeFinitelyGeneratedSpanning.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TwistedLatticeFinitelyGeneratedSpanning.lean', 'LiftWeightParamEqInfinitesimalCharacterOfHalfInt.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LiftWeightParamEqInfinitesimalCharacterOfHalfInt.lean', 'LatticeInIsotypicSup.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LatticeInIsotypicSup.lean', 'TiedHecke.lean': 'src/Formalism/LocalToGlobal/GaloisLevelStructure/TiedHecke.lean', 'SubsetTwistExceptionalPlaces.lean': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/SubsetTwistExceptionalPlaces.lean', 'TwistBaseCoefficientRingResidueFieldFinite.lean': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/TwistBaseCoefficientRingResidueFieldFinite.lean', 'HwFixEx.lean': 'src/Formalism/PeriodIntegrals/OrbitalBoundsConclusion/HwFixEx.lean', 'HwFixLine.lean': 'src/Formalism/PeriodIntegrals/OrbitalBoundsConclusion/HwFixLine.lean', 'MtAdWtIrr.lean': 'src/Formalism/LocalToGlobal/Columns/MtAdWtIrr.lean', 'GoodTwistSideFormsLeSpanGoodLiftForms.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/GoodTwistSideFormsLeSpanGoodLiftForms.lean', 'HFSSplit.lean': 'src/Formalism/LocalToGlobal/Columns/ColumnsProofs/HFSSplit.lean', 'FormsCAtState.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FormsCAtState.lean', 'SRatOfIsotInternal.lean': 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SRatOfIsotInternal.lean', 'RingSpecNormalisedCharacterEq.lean': 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', 'RingHomOfBaseOrderToFraction.lean': 'src/Formalism/LocalToGlobal/NormalizedHeckeFactors/RingHomOfBaseOrderToFraction.lean', 'NPartCNd.lean': 'src/Formalism/LocalToGlobal/NumberFieldFamilies/NPartCNd.lean', 'NPartCNdStd.lean': 'src/Formalism/LocalToGlobal/NumberFieldFamilies/NPartCNdStd.lean', 'RatDatObjects.lean': 'src/Formalism/LocalToGlobal/IndefiniteReal/DoubleCosetOperators/Objects.lean'}

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


P["bridge"] = "src/Formalism/LocalToGlobal/IndefiniteReal/Bridge.lean"
P["blocks"] = AM + "BlocksUnique.lean"
P["triple"] = AB + "Definitions/NonGaloisDescent/CharpolySmulOfProd.lean"
P["locall"] = AM + "LocAutHodgeTateWeightsLevelZeroDef.lean"
P["dataN"] = "src/Formalism/SharpRestriction/LevelLetterCocycles/DataN.lean"
P["artin"] = AB + "PublishedTheorems/AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean"
P["fieldvals"] = "src/Formalism/LocalToGlobal/UnitaryNorms/CharTied.lean"
P["toric"] = AB + "Proofs/InertiaEigenvalues/ExistsToricCharactersInTwistCoefficientRings.lean"
ALIASES = {
    "span": "SpanRangeEquiv.lean", "cut": "ExtLvlFormMemCutSp.lean",
    "hklat": "HeckeOperatorKeepsRationalIntegralLevelForms.lean",
    "std": "DefiniteLevelFormsIffStdGroupTypeSpace.lean",
    "open": "StdFrameLevelSubgroupBoundedOpenHyperspecial.lean",
    "prod": "IsProdLevelStdFrameTwoBlockUnipotentLevel.lean",
    "para": "RamifiedLevelEqParahoricWithTupleCharacter.lean",
    "uni": "LevelUnipotentGenericCharTypePlace.lean",
    "mat": "MemRationalGLOfUnitaryGroupGramUnitGram.lean",
    "coef": "CoefficientSpaceDefiniteFormIrreducibleAlgebraic.lean",
    "mtirr": "MtAdWtIrr.lean", "hwe": "HwFixEx.lean", "hwl": "HwFixLine.lean",
    "hw": "WeightTensorDualRepDualHighestWeightAtEmbedding.lean",
    "wtirr": "WeightTensorRepOfEmbeddingsIsIrreducible.lean",
    "wtbc": "IsIrreducibleBaseChangeWeightTensorDualRepOfEmbe.lean",
    "inflam": "InfOfLamLdefEqParamV.lean", "values": "AdelicFormFunctionValuesMemCoefficientLattice.lean",
    "hecke": "HeckeDoubleCosetOperatorsStandardFacts.lean", "sidein": "SideIn.lean",
    "mt": "TiedHecke.lean", "side": "RingSpecNormalisedCharacterEq.lean",
    "mtad": "SubsetTwistExceptionalPlaces.lean", "rat": "SRatOfIsotInternal.lean",
    "formsc": "FormsCAtState.lean", "rhoc": "RhoStabChiInLL0.lean",
    "eigspan": "EigSpanOfIsotInternal.lean", "stable": "HeckeStableRationalLattice.lean",
    "fg": "TwistedLatticeFinitelyGeneratedSpanning.lean", "exp": "ExponentAndTwistData.lean",
    "inf": "BaseChangeInfLatticeEqSubspace.lean", "idem": "IsCentralGroupAlgebraIdempotentUniversal.lean",
    "generic": "GenericUnipotentCharacterAtSideEqThetaSide.lean",
    "good": "GoodTwistSideFormsLeSpanGoodLiftForms.lean", "isot": "LatticeInIsotypicSup.lean",
    "sig": "ExistsSignatureDataSpan.lean", "cp": "LatticeBasisFreeModulePlace.lean",
    "twr": "TwistBaseCoefficientRingResidueFieldFinite.lean",
    "weights": "ExistsWeightDataIntegral.lean", "param": "LiftWeightParamEqInfinitesimalCharacterOfHalfInt.lean",
    "half": "InfinitesimalCharacterHalfIntegral.lean", "places": "PlacesOverRealSubfieldSplit.lean",
    "level": "ExistsLevelGroupWithCharacterAtTypePlaces.lean",
    "tame": "HasTameBlockCharacterTypePlaceNotOverL.lean",
    "ine": "UniversalCharacterAdmissibleConductorInertiaSurj.lean",
    "export": "TwistLiftFormsEqBaseChangeRationalDatumForms.lean",
    "frob": "HeckeComparisonUnitAtFrobeniusEqDelta.lean",
    "second": "RowCuspMultiplicityInput.lean",
    "ntied": "RingHomOfBaseOrderToFraction.lean",
    "split": "ExistsPadicFiniteExtContainingAllHeckeEigenvalue.lean",
    "splitpoly": "HFSSplit.lean", "local": "LocalisationHeckeRingIsLocalRing.lean",
    "nc": "NPartCNd.lean", "ncstd": "NPartCNdStd.lean",
    "eig": "HeckeEigenspaceNeBotEveryLocalisationPoint.lean",
    "free": "LatticeBaseChangeFreeOverLocalisationCoeffRing.lean",
    "nds": "SideRationalEigenData.lean", "auts": "SideRationalLevelData.lean",
    "all": "SideRationalHeckeData.lean", "spec": "NonemptySpec.lean",
    "act": "HeckeRingActsFaithfullyOnLocalisedLattice.lean",
    "acthk": "HeckeRingActsOnLatticeAsOperators.lean",
    "ratdat": "RatDatObjects.lean", "lift": "ExistsLiftFormsAdelicDecoratedLattices.lean",
}
P.update({key: P[name] for key, name in ALIASES.items()})

main = (ROOT / "main.tex").read_bytes()
report = (ROOT / "report.txt").read_bytes()
tex = main.decode()
assert not [c for c in tex if ord(c) < 32 and c not in "\n\r\t"]
assert not re.search(r"(?<![A-Za-z\\])q?quad\b", tex)
markers = list(re.finditer(r"(?m)^\\paragraph\{(MR\d+):", tex))
assert [m.group(1) for m in markers] == [f"MR{i}" for i in range(1, 27)]
paragraphs = {}
for i, match in enumerate(markers):
    end = markers[i+1].start() if i+1 < len(markers) else len(tex)
    part = tex[match.start():end].encode()
    paragraphs[match.group(1)] = {
        "sha256": sha(part), "bytes": len(part),
        "line_start": tex[:match.start()].count("\n")+1,
        "line_end": tex[:end].count("\n"),
    }
    loc = paragraphs[match.group(1)]
    assert b"".join(main.splitlines(keepends=True)[loc["line_start"]-1:loc["line_end"]]) == part
claims = []


def claim(i, title, statement, deps, sources, assumptions):
    cid = f"MR{i}"
    claims.append({
        "id": cid, "title": title, "statement": statement,
        "status": "derived_simplification",
        "mathematical_status": "proved_under_explicit_hypotheses",
        "introduced_in": "0.22", "depends_on": deps,
        "assumptions": assumptions,
        "proof_location": {
            "file": "automorphic_realization/main.tex",
            "expanded": "automorphic_realization/report.txt",
            "section": cid, **paragraphs[cid],
        }, "sources": sources,
    })


FIXED = [
    "Same D, host, original rows, L=what2.LL, K=LL0 subset L, epsilon and coefficient-place system",
    "All coefficient, tuple, field and frame maps are the specified maps; no transport is inferred from equal ranks",
]
GEOM = FIXED + [
    "Actual finite definite class presentation, ClassPres/CoefTie, unit Gram/frame and standard lattice",
    "Actual SideIn/TupIn and OLatTie, or the precise supplied St/ColPin/R3.Read/Rw.Tie1 inputs used by SpanRangeEquiv",
]
HW = [
    "The characteristic-zero canonical polynomial Schur/tensor highest-weight theorem, with existence and uniqueness of the highest fixed line and the stated dual convention, is retained explicitly",
    "Distinct nonconjugate CM embeddings; rational-unitary Zariski density is proved in MR5",
]
RAT = FIXED + [
    "Actual RatDat with Ks subset K and its common Ks/L basis and full finite integral lattice",
    "Literal RatIn, especially the good occurring-row simultaneous eigenspace span and norm(P)-power integral denominator bound, remains supplied",
]
RING = FIXED + [
    "The actual RingSpec, with its same two side embeddings, original O0/O/Ok and exact S0 exclusions",
    "Star-stable K and the literal finite generic characters and central good projector",
]
GAL = [
    "GlobalArtinReciprocity with the exact normalization, literal SideA, GalEx, RowCusp and ChebSplit on the same D",
    "No new cuspidal Galois existence, arbitrary residual-model identification or fixed-field value containment is inferred",
]

claim(1, "Finite class evaluation and full adelic extension",
      "Under the supplied class/coefficient presentation, finite stabilizer equations give all adelic forms and commute with scalar extension; their actual coefficient lattices are tested at the class representatives.",
      ["SE2", "FC19", "TX4", "TX5"],
      many("bridge", ["AdForms", "stab", "stabK", "ClassPres", "dec_spec", "ext", "extL"]) +
      many("values", ["ext_vals"]), GEOM)
claim(2, "Finite level projector and rational/integral basis",
      "The finite character average yields the entire cut space, an independent rational basis, rational-coordinate descent and the exact inverse-image integral lattice, without integral division by the group order.",
      ["MR1"], many("cut", ["lvlForm_eig", "exists_lvlForm", "lvlAvgF", "lvlAvgF_eig", "cutAvgL_ext", "cutAvgL_of_mem", "lvlForm_linInd", "lvlForm_span", "lvlForm_of_mem", "mem_lvlNab_iff", "lvlForm_adelic_basis"]),
      GEOM + ["Characteristic zero, actual finite group action ActTie and its specified subgroup character"])
claim(3, "Actual standard type space and inverse level character",
      "The standard frame gives compatible rational and adelic group isomorphisms; cutSp(psi0^-1) equals the full TypeSp with the exact standard level and ch*psi0^-1 character.",
      ["MR2"], many("mat", ["inclL_injective", "mem_rationalGL_of_unitaryGroupGram_unitGram", "ratE", "ratIso_ratE", "toGf_bij_ratIso"]) +
      many("std", ["mem_stdJ_iff", "extension_conj_character_eq", "stdX_eq", "red_J", "fwd_rat", "bwd_ad", "bwd_q", "cutSp_iff_typeSp"]) +
      many("sidein", ["dim", "nab", "fn"]), GEOM)
claim(4, "Genuine product/open/parahoric/generic/hyperspecial levels",
      "A norm-product congruence modulus and adelic idempotent cuts prove the actual open/product level laws; the exact local parahoric and generic characters are supplied under their literal half/split/LevCh hypotheses.",
      ["MR3", "AR5", "AR6", "AR7", "AR8"],
      many("open", ["cong_entry", "redFn_eq_one_of_cong", "exists_nat_mem", "stdJ_open"]) +
      many("prod", ["cutMat", "cutMat_mul", "cutMat_mul_compl", "eA", "cutGA", "cutGA_mem_Umax", "cut_mul_cut", "main"]) +
      many("para", ["levelPara"]) + many("uni", ["addChar_extend", "exists_localAddChar_lifting_residueChar", "levelUni_typePlace"]),
      GEOM + ["Literal LevCh.Is, selected split halves and original normalized local tuple components"])
claim(5, "Actual coefficient representation and rational-unitary density",
      "The prescribed coefficient map transports the canonical polynomial matrices and dual highest weight. Cayley density makes rational unitary invariant subspaces invariant under the full split product; the retained highest-weight theorem gives the actual irreducible weight and paramV identity.",
      ["MR3", "AR12"], many("coef", ["map_inv_mat", "isAlgWeight_of_equiv", "exists_weight_of_coefMap", "wt_main"]) +
      many("mtirr", ["mtw_stable_of_rat", "tenIrr_of", "HwFixedEx", "HwFixedLine", "mtWtOf", "mtWtOf_hw_dual"], "density/transport source and exact retained highest-weight interfaces") +
      many("hwe", ["highest_weight_fixed_exists"], "retained canonical highest-fixed-vector input") +
      many("hwl", ["highest_weight_fixed_line"], "retained canonical highest-line uniqueness input") +
      many("inflam", ["lamPrime_add_rho", "infOf_lamLdef_eq_paramV"]), GEOM + HW)
claim(6, "Actual normalized rational Hecke transforms",
      "The finite supported double-coset sum with normalization q_s^-k(n-1) preserves the full type space and has unique rational coordinates in the actual level basis.",
      ["MR1", "MR2", "MR3", "MR4"], many("hecke", ["exists_tSet_eq", "finite_dc", "exists_repsU", "heckeD_eq_sum", "hyp_at", "fixed_of_type", "heckeD_type", "heckeD_mem"]) +
      many("hklat", ["tN_val", "tN_core"]) + many("values", ["ext_vals"]),
      GEOM + ["Good split prime outside the actual level; fixed uniformizer and 1<=k<=n"])
claim(7, "Prime-local integral Hecke stability on the actual nabla lattice",
      "At a coefficient prime away from the Hecke residue characteristic, actual underlying and nabla lattices have equal localizations; one common denominator d outside that prime puts the rational transform back in the exact level lattice.",
      ["MR6"], many("hklat", ["localized_eq_of_commensurable", "localized_comap", "lat_dualFr_comm", "lat_tauLat_comm", "localized_nabla_eq_of_commensurable", "clear_den", "hLat_lev", "localization_nabAtr_eq'", "line₅", "tN_core", "tN_lvlForm"]),
      GEOM + ["Actual coefficient prime avoids the rational prime below the Hecke place", "No equality of integral Delta and nabla is assumed"])
claim(8, "The full MtReal on the original rational and complex row spaces",
      "Extending the specified rational tuple basis constructs every MtReal field, with injective map and full TypeSp range and the exact real(jMt(e(x))) equality.",
      ["MR2", "MR3", "MR4", "MR5", "MR6", "MR7"],
      many("sidein", ["SideIn", "TupIn"]) + many("span", ["constr_semi", "side_read", "tup_read"]) + many("mt", ["MtReal", "MtFam"]), GEOM + HW)
claim(9, "All eight Good/MtInput fields on the fixed generator lattice",
      "OLatTie and the prime-local denominator give nonnegative-valuation coefficients in the original finite generators; local level, weight, rational, integral and full-range clauses yield the literal Good and MtInput.",
      ["MR4", "MR5", "MR6", "MR7", "MR8"],
      many("sidein", ["Good"]) + many("span", ["eq_resChar", "tup_read", "fam_read", "gen_state", "inMt_of"]) +
      many("side", ["MtInput"]), GEOM + HW + ["Exact GenAt/GenAt0 and TwistedAt qualifications; 1<=j<=m, k<=r"])
claim(10, "Pointwise MtAd and both used/unused tuple branches",
      "Equality on the fixed complex basis proves the exact pointwise reading for all x and g; actual matrix ties give all seven MtAd fields, while mL=lMat transports the unused-tuple Rw.Tie1 and completes inMt_state/sMt on the supplied St.",
      ["MR3", "MR5", "MR8", "MR9"],
      many("span", ["Reads", "used_read", "rat_castFr", "std_castFr", "tie_cast", "inMt_of", "all_read", "selHalf_of", "real_state", "inMt_state", "inMt_idFrame", "sMt"]) +
      many("mtad", ["MtAd"]) + many("lift", ["exists_liftSide"], "retained original compatible lift/read presentation; not a newly proved unconditional state supplier"), GEOM + HW)
claim(11, "Finite rational lattice fields and exact RatIn/RatAd boundary",
      "The rational basis and finite full lattice construct ks/fd/mk_fg and the coefficient identities supply rho/chi; all fourteen RatIn and five RatAd fields assemble only with the literal good-row spectrum, normalized readings and norm-power Hecke-integrality inputs.",
      ["SE2", "SE4", "MR6"], many("formsc", ["formsC_of_full", "formsC_at_state"]) +
      many("rhoc", ["chi_val_small", "rhoStab_chiInLL0"]) + many("side", ["RatIn", "goodL"]) +
      many("mtad", ["HkDat", "EigAd", "RatAd"]) + many("eigspan", ["exists_eigAd_of_state", "eig_span_of_isotInternal"], "retained good-row spectral supplier") +
      many("rat", ["sRat_of_isotInternal", "sRat_of_duties"], "conditional field assembly; PrN/SerN/IsotInternal/LocalLanglands inputs retained"),
      FIXED + ["Supplied common rational basis/full lattice and actual coefficient identities", "Literal good-row eigenspace span, Hecke-transform/read/integrality, PrN/SerN and IsotInternal remain explicit when this assembly is used"])
claim(12, "Integral additive reading without local-field enlargement",
      "An integral primitive-vector splitting gives lambda:L→Frac(O), additive and K-semilinear with lambda(1)=1 and lambda(O_L) subset O, on the original DVR even when L has no embedding into its fraction field.",
      [], many("stable", ["exists_integral_functional", "exists_integral_reading"]),
      ["L number field, K a number subfield, O a DVR and the specified embedding K→Frac(O)", "Characteristic-zero algebraic closure and standard integral-basis theorem"])
claim(13, "Flat descent of the actual finite integral equations",
      "The coefficientwise additive reading intertwines every rational operator; flatness over O_K makes each O-valued solution of the finite K-equations an O-span of original integral O_K solutions.",
      ["MR12"], many("stable", ["mem_span_solutions", "exists_integral_descent"]),
      FIXED + ["Actual common Ks/L basis, Ks subset K, supplied reading K→Frac(O)", "O torsion-free over the Dedekind O_K; exact finite coefficient system"])
claim(14, "The genuine full lattice and its good intersection",
      "Bsup=O-span(1 tensor MK) is finite free and full; B=Bsup intersect V0 is finite free, and its exact fraction-space image is V0 by denominator clearing.",
      ["MR11", "NR15"], many("fg", ["readT_integral", "ksInt_mem", "one_tmul_smul", "bsupT_fg_span", "bsupT_fg_span_all"]) +
      many("exp", ["FmT", "BsupT", "V0T", "BT", "BI", "fg_BI", "tf_BI"]) + many("inf", ["baseChange_inf_lattice_eq_subspace"]), RAT + RING)
claim(15, "The original idempotent and sided generic good-space descent",
      "Injective coefficient extension reflects central idempotence; finite-root conjugation gives the exact inverse false-side character, and finite-kernel/projector descent transfers the retained good-row spectral span to the actual V0.",
      ["MR2", "MR11", "MR13", "MR14"], many("idem", ["eIdem_all"]) +
      many("generic", ["star_mul_self_of_pow", "readT_false_eq", "readT_false_mul_true", "mul_pow_g_eq_one", "psiUT_eq_thSide"]) +
      many("good", ["projL", "goodL_of", "projT", "projT_fix", "projT_phi", "goodTwistSideForms_le_span_goodLiftForms"]) +
      many("isot", ["descend_mem_V0T", "descend_mem_eigenspace", "goodPart_le_iSup_eigen"]) +
      many("exp", ["eL", "EIdem", "eAlgT_eq", "eAlgT_idem", "eAlgT_central"]), RAT + RING)
claim(16, "Hecke stability of the original good intersection lattice",
      "Integral finite-equation descent rewrites B by genuine integral good vectors; the norm(P)-denominator is a unit outside S0, proving exact cHk^k normalized HkStab for the specified split/admissible range.",
      ["MR11", "MR12", "MR13", "MR14", "MR15"],
      many("stable", ["normV_isUnit", "hL_goodL", "eqL", "mem_goodL_iff", "eqT", "eqL_rational", "descend_integral", "hkStab_all"]) +
      many("exp", ["HkCond", "HkStab", "hkB", "hkB_zero"]), RAT + RING + ["Sb subset Sx, hence all retained good Hecke primes off S0 are covered by RatIn.hL_int"])
claim(17, "Actual finite integral and separated signatures",
      "The monic characteristic-polynomial argument makes every actual nonzero eigenspace eigenvalue integral; the image of the finite row/side/eigenvalue-system map gives Sig with exact span, separation, selected good nonzero row, normalized values and hEig_zero=1.",
      ["MR14", "MR15", "MR16"], many("sig", ["eigenvalue_integral_of_baseChange", "sigVal", "sigLam", "SigIdx", "sigEig", "sigEig_on", "sigEig_off", "sigSys", "sigDataOf", "span_eig_BI", "sig_of_fg", "sigData_exists"]) +
      many("exp", ["SigData"]), RAT + RING + ["Finite original FT row-type set; no nonzero good space is asserted where the original space is zero"])
claim(18, "Split characteristic polynomials and genuine positive TwF fields",
      "The actual eigenvector span diagonalizes each admissible integral restriction after scalar extension, proving hkB characteristic-polynomial splitting; the positive TwF fields use that same B/Sig and NR24's actual row representation, with zero theta initialization recorded separately.",
      ["MR14", "MR16", "MR17", "NR24"], many("cp", ["charpoly_eq_prod_of_iSup_eigenspace", "charpoly_restrict_map_eq_prod", "hkB_charpoly_splits"]) +
      many("exp", ["RhoFam", "mkF"]) + many("twr", ["TwF"]), RAT + RING + GAL)
claim(19, "Explicit dominant weights over the original fraction fields",
      "The exact HC gaps and parity sort paramV into an integral dominant weight; the dual tensor polynomial representation at the actual sided embeddings has the required weights and absolute irreducibility under the retained highest-weight theorem, so the weight-bound field c2 is bottom.",
      ["MR5", "NR15", "HF11"], many("param", ["exists_domWeight_infOf", "qv", "paramV_eq", "card_qv", "nodup_qv", "int_qv", "paramV_eq_infOf"]) +
      many("half", ["sh_half"]) + many("weights", ["wt_weights"]) +
      many("wtirr", ["tenRepF_isIrreducible"], "canonical polynomial irreducibility under the explicit highest-weight input") +
      many("hw", ["tenRepF_toMatrix", "dd_toMatrix", "dd_hwAt"], "actual polynomial basis/dual convention and highest weight") +
      many("wtbc", ["dualBC", "dualBC_natural", "bcVV", "isIrreducible_bcRep_tenRepF", "isIrreducible_bcRep_wtRepF"]),
      RING + HW + ["Actual ranks/HC gap conditions, integer eExp, odd t and even nV; literal CharSide eta infinitesimal character"])
claim(20, "Actual local level characters and the whole TypeSpF",
      "Reduction proves the block-parabolic/unipotent level subgroup and exact tame determinant/generic character; finite class evaluation proves the full TypeSpF finite dimensional. Thus admissible MtSubT uses the genuine type space, with a finite full basis lattice rather than its fallback zero branch.",
      ["MR1", "MR4", "MR19", "GA17", "AR3", "NR15"],
      many("level", ["locM_cong", "bt_parah", "bt_levG", "i_parah_mul", "i_levG_mul", "i_parah_inv", "i_levG_inv", "i_detT_mul", "i_redMat_mul", "tame_mul", "gU_mul", "levJ", "chiU", "levGroup_exists"]) +
      many("tame", ["tauTame"]) + many("places", ["typeSpF_finiteDimensional", "levDatum_forms"]) +
      many("exp", ["LevLawsT", "MtSubT", "MtLatT", "MtLatT_fg", "MtLatT_span"]) +
      many("ntied", ["AdmTw", "MtVReal"]),
      RING + HW + ["Pq lies above each real-field prime; actual admissible Q/psi, auxiliary splitting, original type residue fields and normalized tame characters", "Comparison to an already installed original MtLat is not inferred"])
claim(21, "Exact initial NExpTied and tensor/Hecke comparisons",
      "The genuine weight/type/generic fields and universal characters supply NExpTied on the initial object. Inertia surjectivity uses literal AdmQ's supplied character. Identity tensors give eF/Bsup/action equality and the exact sided delta^k Hecke comparison, including k=0.",
      ["MR14", "MR15", "MR18", "MR19", "MR20", "NR11"],
      many("ine", ["universalCharacter_admissibleConductor_inertia_surjective"]) +
      many("export", ["formsExport_eq"]) + many("frob", ["cHkT_eq_of_isFrob"]) +
      many("exp", ["cHkT", "hkT", "twDelT", "eHT", "mkEx", "hLr_zero", "hkT_zero"]) +
      many("ntied", ["AdmQ", "NExpTied"]) + many("second", ["second_step"]),
      RAT + RING + GAL + ["Literal AdmQ for the inertia-surjectivity clause; exact initialized Dat=PEmpty/thP=0/twDel=0/eH=1, not a genuine theta supplier"])
claim(22, "Full conditional SideB with all placeholder and quantifier boundaries",
      "Choose c0 before every b0,b1,Sx,T,Sp; the actual form/signature data construct all 29 SideB fields on the specified setTw object for every subsequently supplied NTh. The source's zero Theta/ThetaPsi, empty Dat/TwL, zero thP/twDel and empty old Loc remain explicit, so no compatible nonplaceholder or nonempty-local realization is claimed.",
      ["MR8", "MR9", "MR10", "MR11", "MR14", "MR16", "MR17", "MR18", "MR19", "MR20", "MR21", "NR17", "NR24"],
      many("second", ["second_step"]) + many("side", ["SideA", "TwNew", "TwNew.toD7", "TwNew.cf", "TwNew.row", "TwNew.rat", "TwNew.mt", "SideB"]) +
      many("twr", ["TwR.ntw", "TwL.empty", "setTw"]) + many("exp", ["mkF", "mkEx"]),
      RAT + RING + GAL + ["Literal MtFam/MtInput arguments retained although unused in the second_step proof body", "c0<=b0, Sb subset Sx, conjugation-stable Sx containing all requested low primes; supplied NTh after the construction", "No new IsTripleFor, nonempty LocsCover, toric family or genuine theta image"])
claim(23, "One finite local splitting field for the entire commuting Hecke family",
      "For each fixed row/place choose finitely many operators spanning the whole commuting family, adjoin roots of their characteristic-polynomial product to Q_l, and obtain generalized eigenspace spanning for every operator over every later compatible field containing that finite extension.",
      ["MR8"], many("splitpoly", ["HeckePolyFor", "hfs_exists_poly"]) +
      many("split", ["aeval_baseChange", "iSup_maxGen_baseChange", "finiteDimensional_mtL", "exists_finExt_split"]),
      FIXED + ["Actual MtFam/NChoice/HeckeLift0, original PlEmb and pairwise commuting hLC operators", "Fixed (j,w) before arbitrary later CoefIn; generalized splitting, not semisimplicity or a single field for all places"])
claim(24, "The actual residual Hecke block algebra is local",
      "Equal residue kernels give congruent coordinate values; a monic product polynomial explicitly constructs inverses when one coordinate is a unit, making the finite nonempty block algebra local with the original residue field.",
      [], many("local", ["isLocalRing_of_congr", "sub_mem_of_ker_eq", "main"]) +
      many("nc", ["LocBase0", "LocT", "XOf", "TOf"]) + many("ncstd", ["HeckeStd0", "FinDimV", "xNe_of", "xFin_of"]),
      ["Actual LocBase0, HeckeStd0, finite-dimensional V and an existing LocT nonzero-support index", "No localization index is manufactured by this argument"])
claim(25, "A supported actual Hecke point has a nonzero eigenspace",
      "A minimal nonzero invariant subspace in the joint generalized weight space consists of eigenvectors; the supplied injective/range-correct Psi and ActHK transport one to the actual localized lattice, and generator induction proves the full algebra character equation.",
      [], many("eig", ["inf_ker_ne_bot", "exists_common_eigvec", "mem_heckeEig_of_gen", "heckeEig_ne_bot"]) +
      many("nc", ["MtLoc", "XOf"]) + many("acthk", ["actHK_holds"], "retained actual operator/comparison interface, not inferred solely from generalized splitting"),
      ["Actual HeckeStd0/FinDimV, existing supported x in XOf, genuine MtLoc/ActEx/ActHK on the same lattice", "The point's nonzero generalized space and actual Psi range/injectivity are essential"])
claim(26, "Freeness of the original relation quotient over the chosen DVR",
      "OsConcrete identifies the original coefficient order with a number-field integer ring; its original generator relation module is saturated, hence a direct summand over the Dedekind ring. Applying the actual coefficient map to the projection proves the literal BjC quotient free over the chosen DVR.",
      [], many("free", ["bcEnd", "bcEnd_comp", "free_quot", "exists_proj", "dedekind_of_concrete", "latRel_torsionFree", "bjC_free"]) +
      many("spec", ["nonempty_spec"], "remaining full NdSpec consumer; only its relation-freeness prerequisite is concluded here"),
      FIXED + ["Injective original OtoLL with image F intersect the global integral elements, the literal original generator relations, actual OsInt/LocBase0 and its prescribed A→O map", "No unrelated lattice is substituted by rank"])


completed = []


def done(key, name, ids, conditions, scope="literal conditional endpoint"):
    completed.append({
        "endpoint": name, "claim_ids": ids,
        "status": "completed_conditionally", "scope": scope,
        "conditions": conditions, "source": source(key, name),
    })


done("cut", "lvlForm_adelic_basis", ["MR1", "MR2"], GEOM + ["Literal finite ActTie and subgroup character; no integral averaging assertion"])
done("mat", "toGf_bij_ratIso", ["MR3"], ["Actual unit Gram/frame and the prescribed tensor order"])
done("std", "cutSp_iff_typeSp", ["MR3"], GEOM + ["Actual reduction map and inverse subgroup-character convention"])
done("open", "stdJ_open", ["MR4"], ["Specified finite conductor/type primes and actual standard level"])
done("prod", "main", ["MR4"], ["Actual standard level and componentwise parabolic/unipotent conditions"], "literal IsProdLevelStdFrameTwoBlockUnipotentLevel.main; not a generic arbitrary-level theorem")
done("para", "levelPara", ["MR4"], GEOM + ["Exact conductor split place, tuple component and selected half"])
done("uni", "levelUni_typePlace", ["MR4"], GEOM + ["Exact type prime, residue generic character and normalized tuple component"])
done("coef", "wt_main", ["MR5"], GEOM + HW)
done("inflam", "infOf_lamLdef_eq_paramV", ["MR5"], ["Actual Ranks/HC coefficient weight at n=R.nV"])
done("values", "ext_vals", ["MR1", "MR6", "MR7"], GEOM + ["Actual coefficient-map/lattice ties and integral level-character values"])
done("hklat", "tN_lvlForm", ["MR6", "MR7"], GEOM + ["Good split Hecke place; coefficient prime away from its residue characteristic"])
done("span", "side_read", ["MR2", "MR3", "MR4", "MR5", "MR6", "MR7", "MR8"], GEOM + HW)
done("span", "tup_read", ["MR8", "MR9"], GEOM + HW)
done("span", "fam_read", ["MR8", "MR9"], GEOM + HW + ["Actual family tuple comparison and original level maps"])
done("span", "inMt_of", ["MR8", "MR9", "MR10"], GEOM + HW + ["Given used and unused tuple realizations and exact conductor/generator conditions"])
done("span", "inMt_state", ["MR10"], GEOM + HW + ["Given actual St/ColPin with its R3.Read and all matrix/row ties"])
done("span", "sMt", ["MR10"], GEOM + HW + ["The source's quantified St/ColPin hypotheses at every requested state"], "conditional supplier on actual states, not initial compatible-state existence")
done("formsc", "formsC_of_full", ["MR11"], ["Actual rational datum IsKsForm and full finite integral lattice"])
done("rat", "sRat_of_isotInternal", ["MR11"], ["Literal PrN, SerN, AllSt IsotInternal, LocalLanglandsGL and their actual rational Hecke/eigenvalue/integrality suppliers"], "conditional field assembly only; the spectral suppliers remain separately targeted")
done("stable", "exists_integral_functional", ["MR12"], ["Finite lattice over a PID in its fraction-field vector space; specified nonzero primitive vector has only integral lattice multiples"])
done("stable", "exists_integral_reading", ["MR12"], ["Number field L, K subset L, actual PID/DVR O and fixed reading K→Frac(O)"])
done("stable", "mem_span_solutions", ["MR13"], ["Literal flat coefficient algebra and finite matrix system"])
done("stable", "exists_integral_descent", ["MR13"], ["Actual common rational basis, Ks subset K, fixed coefficient reading and finite system"])
done("fg", "bsupT_fg_span_all", ["MR14"], RAT + ["Actual TwR, including the source out-of-row padding"])
done("inf", "baseChange_inf_lattice_eq_subspace", ["MR14"], ["Finite full lattice over the specified DVR, actual ambient subspace"])
done("idem", "eIdem_all", ["MR15"], ["Actual D central coefficient identity with its supplied complex projector"])
done("generic", "psiUT_eq_thSide", ["MR15"], RAT + RING)
done("good", "goodTwistSideForms_le_span_goodLiftForms", ["MR13", "MR15"], RAT + RING)
done("stable", "hkStab_all", ["MR16"], RAT + RING + ["Sb subset Sx; exact off-S0 split positive Hecke range"])
done("sig", "sigData_exists", ["MR17"], RAT + RING + ["Actual HkStab and finite row labels"])
done("cp", "hkB_charpoly_splits", ["MR18"], RAT + RING + ["The actual finite free BI and normalized operator"])
done("param", "paramV_eq_infOf", ["MR19"], ["Exact HC gap/parity hypotheses, actual sh in Z+1/2"])
done("weights", "wt_weights", ["MR19"], RING + HW + ["Literal GlobalArtinReciprocity/SideA arguments, star-stable K and integral eExp; c2=bottom"])
done("level", "levGroup_exists", ["MR20"], RING + ["Exact selected split halves, type residues, normalized tame characters and admissible Q/psi"])
done("places", "typeSpF_finiteDimensional", ["MR20"], ["Actual finite-dimensional coefficient representation and specified congruence-open level/character"])
done("places", "levDatum_forms", ["MR19", "MR20"], RING + HW + ["Exact wt data, Pq over each real-field prime, auxiliary splitting and admissible Q/psi"])
done("exp", "MtLatT_fg", ["MR20"], RAT + RING + ["The constructed actual admissible TypeSpF basis lattice"])
done("exp", "MtLatT_span", ["MR20"], RAT + RING + ["The constructed actual admissible TypeSpF basis lattice"])
done("ine", "universalCharacter_admissibleConductor_inertia_surjective", ["MR21"], RING + ["Literal AdmQ's supplied two-prime surjective character; no inference from support alone"])
done("export", "formsExport_eq", ["MR21"], RAT + RING + ["Exact initialized mkF/mkEx, same coefficients/side embeddings and 1<=j<=m"])
done("frob", "cHkT_eq_of_isFrob", ["MR21"], ["Actual TwR delta, P outside S0 and a supplied IsFrob representative"])
done("second", "second_step", ["MR12", "MR13", "MR14", "MR15", "MR16", "MR17", "MR18", "MR19", "MR20", "MR21", "MR22"],
     RAT + RING + GAL + HW + ["All literal MtFam/MtInput/Pq/splitting/eExp hypotheses and c0-before-b0/b1/Sx order", "Conclusion is forall th:NTh on the initialized new data; NTh, nonempty local indices and genuine theta/toric data are not constructed"],
     "full literal conditional endpoint, including its explicit zero/empty initialization fields")
done("split", "exists_finExt_split", ["MR23"], ["Actual MtFam/NChoice/HeckeLift0, fixed PlEmb and pairwise commuting operators", "F0 chosen for fixed j,w before arbitrary larger compatible CoefIn"])
done("local", "main", ["MR24"], ["Actual LocBase0, HeckeStd0, FinDimV and existing LocT"], "literal LocalisationHeckeRingIsLocalRing.main on existing support, not local-index existence")
done("eig", "exists_common_eigvec", ["MR25"], ["Finite-dimensional space; commuting possibly infinite operator family; nonzero invariant generalized common weight space"])
done("eig", "heckeEig_ne_bot", ["MR25"], ["Actual HeckeStd0/FinDimV/MtLoc/ActEx/ActHK and existing x:XOf with its nonzero support"])
done("free", "free_quot", ["MR26"], ["Actual retraction onto the source relation submodule and prescribed coefficient map into a PID domain"])
done("free", "bjC_free", ["MR26"], ["Literal OsConcrete injection/image, original lattice generators, actual OsInt and localization coefficient map"])


targets = [
    {
        "id": "MR-next-01", "title": "Compatible original geometric state, read and tuple lattice ties",
        "scope": "Supply an actual St/ColPin/R3.Read with the specified xi/psi/Q, same frame and original row/basis/OLatTie/Rw.Tie1 data. MR8–MR10 now construct MtFam/MtReal/MtInput/MtAd from those inputs; generic requests for those conditional endpoints are completed, but existence of the compatible input witness remains.",
        "sources": many("span", ["used_read", "all_read", "real_state", "inMt_state"]) + many("lift", ["exists_liftSide"]) + many("mtad", ["MtAd", "SerAt"]),
        "discharged_subscope": ["Explicit full TypeSp real map on original Mt", "All eight MtInput and seven MtAd fields under supplied state/read ties", "Used and unused tuple branches"]
    },
    {
        "id": "MR-next-02", "title": "The genuine normalized good-row spectrum and integral RatIn inputs",
        "scope": "Supply PrN/SerN/IsotInternal or another proof of the exact normalized Hecke operators/readings, good occurring-row eigenspace span with values in fixed K, and norm(P)-power denominator bound. Finite/full rational-lattice fields and conditional fourteen/five-field RatIn/RatAd assembly are proved; those facts do not create the spectral or integral witnesses.",
        "sources": many("side", ["RatIn", "goodL"]) + many("mtad", ["HkDat", "EigAd", "RatAd"]) + many("eigspan", ["exists_eigAd_of_state", "eig_span_of_isotInternal"]) + many("rat", ["sRat_of_isotInternal"]),
        "discharged_subscope": ["formsC_of_full", "Actual integral reading/descent and B-lattice stability once RatIn is supplied", "Exact spectral-field boundary"]
    },
    {
        "id": "MR-next-03", "title": "The precise canonical polynomial highest-weight input",
        "scope": "Reconstruct the retained characteristic-zero canonical Schur/tensor irreducibility and highest fixed-line existence/uniqueness with the exact dual/conjugate convention. MR5 proves rational-unitary density and the basis transports; MR19 proves the literal dominant-weight combinatorics and scalar-extension models. These do not on their own prove the retained highest-line theorem.",
        "sources": many("hwe", ["highest_weight_fixed_exists"]) + many("hwl", ["highest_weight_fixed_line"]) + many("mtirr", ["HwFixedEx", "HwFixedLine", "hwInStable_of", "tenIrr_of'"]) + many("wtirr", ["tenRepF_isIrreducible"]),
        "discharged_subscope": ["Rational unitary Cayley density", "Coefficient-map and tensor/dual scalar-extension transports", "Actual paramV dominant-weight construction with c2=bottom"]
    },
    {
        "id": "MR-next-04", "title": "A compatible nonplaceholder theta and toric installation",
        "scope": "Construct genuine theta/toric NTh data compatible with the actual positive Fm/B/signatures and same host/rows/fields, rather than relying on mkF/mkEx initialization Theta=ThetaPsi=0, Dat=PEmpty, thP=twDel=0, eH=1, TwL.empty. MR22 proves only the source's forall-th conditional SideB on that initialized object; replacing its placeholders requires a new coherent witness and every affected identity.",
        "sources": many("exp", ["mkF", "twDelT", "eHT", "mkEx"]) + many("twr", ["TwL", "TwL.empty", "TwR.ntw"]) + many("toric", ["exists_twL_installed"]) + many("side", ["TwNew", "SideB"]) + many("second", ["second_step"]),
        "discharged_subscope": ["Actual Fm, full Bsup, good BI and signature fields", "All twenty-nine SideB clauses conditional on literal NTh", "No advancement of any global branch from this initialization alone"]
    },
    {
        "id": "MR-next-05", "title": "Same-object normalized choice and original-to-coefficient type comparison",
        "scope": "Supply the actual NChoice/TupTied/ChoiceSide with RankTie, MuIsW, LocsCarry, original tuple xi/psi/Q and all coefficient squares preserved. In particular ChoiceSide.eMt_level must compare the original MtReal level/character to the newly specified whole TypeSpF. Neither a full TypeSpF basis nor equal rank identifies the original integral MtLat with its new basis lattice.",
        "sources": many("side", ["ChoiceSide", "MtInput"]) + many("ntied", ["MtVReal", "NExpTied"]) + many("exp", ["MtSubT", "MtLatT"]),
        "discharged_subscope": ["Genuine finite-dimensional whole TypeSpF and full basis lattice under admissibility", "Actual local character formulas and signs", "Original MtReal constructed from supplied compatible geometry"]
    },
    {
        "id": "MR-next-06", "title": "The full compatible NdSpec/AutSpec/LocAll installation",
        "scope": "Supply every finite coefficient/twist embedding square, actual Psi range/injectivity and act/Hecke comparison, local Galois/automorphic specifications and BlocksUnique for the same nonempty-support objects. MR23–MR26 close the finite Hecke splitting field, local residual block algebra, supported eigenspace nonvanishing and original relation-lattice freeness; they do not create an index or the retained actual comparison.",
        "sources": many("nds", ["ndSpec_exists"]) + many("auts", ["exists_autSpec"]) + many("all", ["locAll_exists"]) + many("side", ["NdSpec", "AutSpec"]) + many("spec", ["nonempty_spec"]) + many("nc", ["MtLoc", "LocT", "XOf"]) + many("act", ["actEx_of"]) + many("blocks", ["BlocksUnique"]),
        "discharged_subscope": ["exists_finExt_split for every fixed j,w", "Locality of actual TOf for an existing LocT", "heckeEig_ne_bot at existing supported points under actual Psi/ActHK", "bjC_free on the original relation quotient"]
    },
    {
        "id": "MR-next-07", "title": "Original fixed-field containment and exact reciprocity/Galois row inputs",
        "scope": "Retain fixed-K ValLL0, GlobalArtinReciprocity, GalEx, RowCusp and ChebSplit on the same automorphic package. NR already constructs all-prime RingSpec and bounded integral row matrices under them; the present signature/weight/form constructions neither prove these inputs nor permit changing K or epsilon independently.",
        "sources": many("fieldvals", ["ValLL0"]) + many("artin", ["IsGlobalArtin", "GlobalArtinReciprocity"]) + many("blocks", ["IsRepOf", "GalEx", "RowCusp"]) + many("second", ["second_step"]),
        "discharged_subscope": ["Actual selected signature row, normalized integral eigenvalues and exact reuse of NR24 matrices", "No new global field or arbitrary normalized character substitution"]
    },
    {
        "id": "MR-next-08", "title": "Actual residual and IsTripleWith/For identities on installed signatures",
        "scope": "Supply the genuine occurring-row/parameter match, scalar equation with installed rhoS, residual characteristic-polynomial and Teichmuller identities, type-character calibration and sig_all coverage on the same nonempty local installation. MR17–MR18 determine their exact positive signature candidates but do not identify arbitrary installed residual models.",
        "sources": many("triple", ["IsParam", "IsResidual", "IsChars", "IsTripleWith", "IsTripleFor"]) + many("side", ["NdSpec", "AutSpec"]) + many("dataN", ["LocsCover"]),
        "discharged_subscope": ["Finite integral separated signatures and actual normalized rowS_eig", "Exact NR24 row matrices on those selected rows", "No use of an empty local family as a coverage witness"]
    },
]


def record_audit(key, name, ids, groups):
    s = source(key, name, "literal record declaration for the complete scoped field audit")
    lines = blob(s["path"]).decode().splitlines()
    fields = []
    for line in lines[s["line_start"]:s["line_end"]]:
        m = re.match(r"^  (?:\[)?([\w'₂]+)\s*:", line)
        if m:
            fields.append(m.group(1))
    flat = [field for g in groups for field in g["fields"]]
    assert len(fields) == len(set(fields)) and fields
    assert sorted(flat) == sorted(fields), (key, name, "missing", set(fields)-set(flat), "extra", set(flat)-set(fields))
    return {"record": s["declaration"], "claim_ids": ids, "source": s,
            "field_count": len(fields), "includes_instance_fields": True,
            "fields": fields, "proof_groups": groups}


def group(ids, fields, reason, status="constructed_under_explicit_hypotheses"):
    return {"claim_ids": ids, "fields": fields.split(), "reason": reason, "status": status}


audits = [
    record_audit("mt", "MtReal", ["MR8"], [
        group(["MR5"], "wt", "Actual coefficient representation and retained canonical highest-weight theorem"),
        group(["MR3", "MR4"], "J χ J_open", "Specified level, inverse-character sign and congruence kernel"),
        group(["MR2", "MR3", "MR8"], "real real_inj real_range", "Actual basis extension with full TypeSp range"),
    ]),
    record_audit("sidein", "Good", ["MR9"], [
        group(["MR4"], "prod para uni hyp", "Componentwise level and literal local character laws"),
        group(["MR5", "MR6"], "wt rat", "Actual coefficient weight and normalized rational Hecke"),
        group(["MR7", "MR9"], "int full", "Original OLatTie generators, common denominator and original rational/full span"),
    ]),
    record_audit("side", "MtInput", ["MR9"], [
        group(["MR4", "MR9"], "prod para uni hyp", "Literal generator-place exclusions and local tuple conditions"),
        group(["MR5", "MR6", "MR9"], "wt rat", "Exact row shift, index range and normalized operator"),
        group(["MR7", "MR8", "MR9"], "int full", "TwistedAt-qualified original lattice conditions"),
    ]),
    record_audit("mtad", "MtAd", ["MR10"], [
        group(["MR3", "MR5", "MR10"], "PV std eW rat wt id", "Actual standard frame, rational matrix and coefficient intertwining"),
        group(["MR8", "MR10"], "read", "Pointwise equality from the original complex basis for every x and g"),
    ]),
    record_audit("side", "RatIn", ["MR11"], [
        group(["MR11"], "rho chi ks fd mk_fg", "Actual coefficient identities and finite full rational lattice"),
        group(["MR11"], "Sb hL hs hL_zero θ θ_ne eig span hL_int", "Retained exact spectral/Hecke/reading/integrality suppliers; only their conditional assembly is asserted", "retained_then_assembled"),
    ]),
    record_audit("mtad", "RatAd", ["MR11"], [
        group(["MR11"], "hecke eig Sb_le lvl psi", "Actual original-state reading, level and support clauses from the retained RatIn suppliers", "retained_then_assembled"),
    ]),
    record_audit("exp", "SigData", ["MR17"], [
        group(["MR17"], "Sig fin jS jS_range side hEig rowS", "Finite image of the exact row/side/eigenvalue functions and chosen good original row"),
    ]),
    record_audit("twr", "TwF", ["MR18", "MR22"], [
        group(["MR17"], "Sig finSig jS jS_range side hEig", "Actual integral finite signatures and exact eigenvalues"),
        group(["NR24", "MR18"], "rhoS rhoS_cont", "Actual selected original-row Galois family, retaining GalEx/RowCusp/ChebSplit"),
        group(["MR14", "MR16"], "B acgB modB freeB finB hk hk_zero", "Actual good intersection lattice and restricted/identity operator definition"),
        group(["MR22"], "Theta ThetaPsi ThetaPsi_one", "Both theta submodules are literally zero in mkF; no genuine theta-image claim", "explicit_placeholder_initialization"),
    ]),
    record_audit("ntied", "MtVReal", ["MR19", "MR20"], [
        group(["MR19"], "W acg mod fd ρ irr alg bc", "Actual tensor polynomial coefficient module, retained canonical highest weight and exact base-change basis matrices"),
        group(["MR20"], "J χ J_open hyp QP QP_sub QP_cover QP_nconj DP DP_sub DP_cover DP_nconj sp sp_w redG J_mem chi_eq", "Actual selected split halves and explicit finite-prime level/character construction"),
        group(["MR20"], "real", "Exact identification of admissible MtSubT with its full TypeSpF; no comparison to original MtLat inferred"),
    ]),
    record_audit("ntied", "NExpTied", ["MR21"], [
        group(["MR15", "MR21"], "U_eq psiU_gen psiU_side psiU_xi", "Actual generic group, nontrivial finite characters and sided inverse convention"),
        group(["NR11", "MR21"], "delU_cont delU_ine", "Universal normalized character; surjectivity only under literal AdmQ witness"),
        group(["MR22"], "thU_empty", "Dat=PEmpty in the initialized object", "explicit_placeholder_initialization"),
        group(["MR19"], "Wt acgWt modWt fdWt rhoW rhoW_irr rhoW_alg rhoW_hw rhoW_wt", "Actual polynomial/dual weight and explicit paramV combinatorics under the retained highest-weight input"),
        group(["MR20", "MR21"], "sgnT sgnT_one tauG sgnG sgnG_one tau_galois_first_character mtV", "Signs both one, actual normalized tame values and genuine full TypeSpF"),
    ]),
    record_audit("side", "SideB", ["MR22"], [
        group(["NR15", "NR17", "MR18", "MR22"], "twF tw cover chiD chi eta_eq ringSpec_normalisedCharacter_eq del_eq iCq_embO embO_star deltaRead", "Exact original RingSpec/normalized character squares and coefficient coverage; unused toric/local slots remain empty"),
        group(["MR19", "MR20", "MR21"], "exp pq psiU", "Actual weights/type levels/generic fields in the initialized NExpTied"),
        group(["MR11"], "rho chiL hs", "The supplied original RatIn coefficient/action/Hecke stability fields", "retained_then_assembled"),
        group(["MR21"], "eF bsup act cHk hkEq cHk_del hk_emb", "Identity tensor export, exact original lattice and sided delta-normalized Hecke equations"),
        group(["MR17", "MR18"], "sigSpan rowS rowS_eig hEig_zero", "Actual finite signature and good original-row eigenvalue system"),
        group(["NR24", "MR18"], "rhoS", "Actual bounded row matrices under unchanged Galois/row hypotheses"),
    ]),
]
assert len(audits) == 11 and sum(a["field_count"] for a in audits) == 152


# Verify new identifiers/dependencies without editing the archived predecessor.
old_path = ROOT.parent / "history" / "version_0_21" / "provenance.json"
if old_path.is_file():
    old = json.loads(old_path.read_text())
    old_ids = {c["id"] for c in old["claims"]}
    new_ids = {c["id"] for c in claims}
    assert not old_ids.intersection(new_ids), "MR prefix collision"
    for c in claims:
        assert set(c["depends_on"]) <= old_ids | new_ids, (c["id"], set(c["depends_on"])-(old_ids|new_ids))
        assert all(not d.startswith("MR") or int(d[2:]) < int(c["id"][2:]) for d in c["depends_on"])

reviews = []
review_path = ROOT.parent / "reviews_v0_22" / "automorphic_realization_independent_review.json"
if review_path.is_file():
    data = json.loads(review_path.read_text())
    assert data["result"] == "PASS", "independent review not PASS"
    reviewed = data["reviewed_claims"]
    assert set(reviewed) == set(paragraphs)
    for cid, h in reviewed.items():
        if isinstance(h, dict):
            h = h.get("sha256", h.get("paragraph_sha256"))
        assert h == paragraphs[cid]["sha256"], ("stale review", cid)
    assert data.get("reviewer") != "/root/class_rank"
    reviews.append({"file": str(review_path.relative_to(ROOT.parent)),
                    "sha256": sha(review_path.read_bytes()), "result": "PASS",
                    "reviewer": data["reviewer"], "author": "/root/class_rank",
                    "reviewed_claims": {cid: paragraphs[cid]["sha256"] for cid in paragraphs}})

all_sources = [s for c in claims for s in c["sources"]]
unique_ranges = {(s["path"], s["line_start"], s["line_end"]) for s in all_sources}
claim_files = {s["path"] for s in all_sources}
manifest = {
    "component": "automorphic_realization", "version": "0.22", "commit": COMMIT,
    "repository": URL, "source_files": [
        {"path": path, "sha256": sha(raw), "bytes": len(raw),
         "line_count": len(raw.splitlines()), "verified_equal_to_pinned_git_blob": True,
         "url": f"{URL}/blob/{COMMIT}/{path}"}
        for path, raw in sorted(cache.items())
    ],
}
scope = (
    "Actual fixed-state MtReal/MtFam/MtInput/MtAd, full TypeSp range and prime-local integral Hecke; "
    "original-DVR additive reading and finite-equation descent, actual B/signature/weight/type spaces; "
    "the complete literal second_step/SideB conditional endpoint with zero/empty mkF/mkEx theta and toric initialization explicit; "
    "four genuine local Hecke/relation-lattice primitives. Retains exact geometric and spectral input, "
    "canonical highest-weight theorem, fixed-field containment/reciprocity/GalEx/RowCusp/ChebSplit and compatible "
    "nonplaceholder theta, residual and nonempty-local realization. No global branch is advanced by the initialization wrapper."
)
provenance = {
    "component": "automorphic_realization", "version": "0.22", "claim_prefix": "MR",
    "source_commit": COMMIT, "repository": URL, "scope": scope,
    "main_sha256": sha(main), "report_sha256": sha(report),
    "builder_sha256": sha(Path(__file__).read_bytes()),
    "claims": claims, "completed_source_endpoints": completed,
    "record_field_audits": audits, "remaining_targets": targets,
    "independent_reviews": reviews,
    "important_scope_distinctions": {
        "actual_positive_fields": "Full original MtReal range; Bsup/BI; finite integral signature system; actual coefficient-field weights and complete TypeSpF",
        "initial_placeholders": ["Theta=0", "ThetaPsi=0", "Dat=PEmpty", "thP=0", "twDel=0", "eH=1", "TwL.empty", "SideA.bare old Loc empty"],
        "quantifier_order": "c0 before every b0,b1,Sx,T,Sp; F/ex/h0 before every subsequently supplied th:NTh; this is not exists th",
        "unused_literal_parameters": "M,tup,Q,hM are introduced but unused in the second_step proof body; their literal hypotheses are retained and do not provide a hidden comparison",
        "local_support": "MR24/MR25 require existing LocT/XOf support and MR25 retains the actual Psi/MtLoc/ActHK; no empty family is used to fake coverage",
        "spectral_input": "Fourteen-field RatIn and five-field RatAd are conditional assemblies retaining exact good-row spectrum and norm-power integrality",
        "four_global_branches": "unchanged by this component",
    },
    "counts": {
        "claims": len(claims), "claim_source_links": len(all_sources),
        "distinct_claim_ranges": len(unique_ranges), "claim_source_files": len(claim_files),
        "indexed_source_files": len(cache), "completed_source_endpoints": len(completed),
        "remaining_supplier_families": len(targets), "record_fields_audited": 152,
        "record_audits": len(audits),
    },
    "verification": {
        "git_objects_only": True, "source_checkout_unchanged": True,
        "old_components_unchanged": True, "lean_compiled": False, "pdf_generated": False,
        "proof_paragraph_raw_ranges_verified": True,
        "hypothesis_policy": "Every endpoint preserves its literal compatible hypotheses; completed conditional field suppliers do not assert compatible witness existence.",
    },
}
next_targets = {
    "component": "automorphic_realization", "version": "0.22", "commit": COMMIT,
    "scope": scope, "completed_endpoints": completed, "next_targets": targets,
}
for name, obj in [("provenance.json", provenance), ("source_manifest.json", manifest), ("next_targets.json", next_targets)]:
    (ROOT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+"\n")
lines = ["AUTOMORPHIC REALIZATION SOURCE LOCATORS -- MR1--MR26", "Pinned commit: "+COMMIT,
         "Inclusive line ranges; hashes use exact Git blob bytes including line endings.", ""]
for c in claims:
    pl = paragraphs[c["id"]]
    lines.extend([c["id"]+" "+c["title"],
                  f'TeX main.tex:{pl["line_start"]}-{pl["line_end"]}; bytes {pl["bytes"]}; SHA-256 {pl["sha256"]}'])
    for s in c["sources"]:
        lines.extend(["  "+s["declaration"], f'  {s["path"]}:{s["line_start"]}-{s["line_end"]}',
                      "  full SHA-256 "+s["full_file_sha256"], "  range SHA-256 "+s["range_sha256"], "  "+s["url"]])
    lines.append("")
lines.append("Completed conditional endpoints: "+str(len(completed))+"; remaining supplier families: "+str(len(targets)))
lines.append("Record fields audited: 152 in eleven explicitly scoped records, including retained and placeholder fields.")
(ROOT/"source_locators.txt").write_text("\n".join(lines)+"\n")
print(json.dumps(provenance["counts"], sort_keys=True))


