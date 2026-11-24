"""Rebuild TI1--TI9 provenance from the byte-identical pinned Lean checkout.

Run with Python 3.11+. This reads source and writes only this component's
provenance.json/source_locators.txt. It does not invoke Lean or use the network.
Line ranges are inclusive and preserve all original bytes and line endings.
Qualified declaration names are lexical; private Lean internals may differ.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE_URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
GM = "src/Formalism/MahlerMeasure/"
PM = "src/Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/"
PATHS = {
    "OBJ": GB + "ObjSeg.lean",
    "ENDPOINT": GB + "ProjectionLemmaBaseLevel.lean",
    "BLOCKFG": GB + "BinomialRatio/BlockFG.lean",
    "PAIRLIFT": GB + "BinomialRatio/PairLift.lean",
    "COUNT": GB + "CountingStatementReduction.lean",
    "LEVEL": GM + "LevelSum.lean",
    "FROZEN": GM + "IsFrozenInv.lean",
    "GAMSTMT": GM + "HasOrder.lean",
    "GAMDEG": GM + "MahlerMeasureProofs/GamDeg.lean",
    "GAMLEAD": GM + "MahlerMeasureProofs/GamLead.lean",
    "INTSTMT": GM + "GamInt.lean",
    "GAMINT": GM + "MahlerMeasureProofs/GamInt.lean",
    "WINDOW": GM + "StatementD.lean",
    "AP": GM + "QuotientUpperBoundsOfPowerBounds.lean",
    "MAHLER": GM + "MahlerMeasureProofs/MahlerK.lean",
    "APCOUNT": GM + "MahlerMeasureProofs/WindowAP.lean",
    "APMEAN": GM + "MahlerMeasureProofs/WindowMeanAP.lean",
    "GRAM": GM + "StatementT.lean",
    "MEANSTMT": GM + "StatementTM.lean",
    "MEAN": GM + "MahlerMeasureProofs/MeanGam.lean",
    "SHARPINT": PM + "TheoremMCB.lean",
    "SHARPPROOF": PM + "PartnerMeanProofs/GamIntC.lean",
    "GRAMPART": PM + "PartnerMeanProofs/GramHypothesisOfLogBound.lean",
    "PARTNER": PM + "PartnerMeanProofs/GammaZeroIntegral.lean",
    "MEANDEFS": GB + "ColumnSpanDensity/MeanDefs.lean",
    "DENSITY": GB + "ColumnSpanDensity/DensityNumericalFacts.lean",
    "FINALMEAN": GB + "ColumnSpanDensity/ColumnSpanNumericalFacts.lean",
    "KAPPA": GB + "ColumnSpanDensity/RhoLowerBoundLargeConductor.lean",
    "ASSEMBLY": GB + "ColumnSpanDensity/TheoremIOfIntermediateBounds.lean",
    "BLOCKMEAN": GB + "MonomialFactorials/SegmentWeightedCountingBoundOfAllRemainingBounds.lean",
    "RAWLIFT": GB + "CoarseMultiplicity/PairedLiftAtOfIdentity.lean",
    "BRIDGE": GB + "ObjBridge.lean",
    "RAWTAIL": GB + "CoarseMultiplicity/CoarseMultiplicityAtIdentity.lean",
    "RAWFORM": GB + "CoarseMultiplicity/RestBlockForm.lean",
}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")

actual_head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if actual_head != COMMIT:
    raise RuntimeError(f"Source checkout is {actual_head}, expected {COMMIT}")

FILES = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise RuntimeError(f"Working tree differs from pinned bytes: {path}")
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if m := NS.match(line):
            stack.append(("namespace", m.group(1)))
        elif m := SEC.match(line):
            stack.append(("section", m.group(1)))
        elif m := END.match(line):
            if not stack:
                raise RuntimeError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if m.group(1) and m.group(1) != label:
                raise RuntimeError((path, i + 1, "end mismatch", label, m.group(1)))
        elif m := DECL.match(line):
            namespace = ".".join(label for kind, label in stack if kind == "namespace")
            name = m.group(1)
            declarations.append({"name": name, "line": i,
                                 "qualified": f"{namespace}.{name}" if namespace else name})
    FILES[key] = {
        "path": path, "full_file_sha256": sha256(raw).hexdigest(),
        "bytes": len(raw), "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines, "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    info = FILES[key]
    hits = [d for d in info["_declarations"] if d["name"] == name]
    if occurrence >= len(hits):
        raise RuntimeError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = info["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": info["path"], "declaration": decl["qualified"],
        "source_spelling": name, "line_start": start + 1, "line_end": end,
        "role": role, "full_file_sha256": info["full_file_sha256"],
        "range_sha256": sha256(excerpt).hexdigest(), "range_bytes": len(excerpt),
        "pinned_url": f"{BASE_URL}/blob/{COMMIT}/{info['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]


CLAIMS = [
    {
        "id": "TI1", "title": "Actual Type-I paired-contraction polynomials and factorial block lattices",
        "status": "literal_family_identified_and_translated; no_full_edge_lift_claim",
        "statement": "The actual SSZ generators, coarse degrees, retained predicates, scalar factorial multiplier, rational-span intersection and block-orthogonal form are specified without replacing the source family.",
        "sources": many("OBJ", ["YCond", "Yjt", "YjtZ", "BlockData.LevelOK", "BlockData.gens", "BlockData.SSZ", "Kept", "segChain", "blockData", "specConst", "bbSpec", "blockLat", "segLat", "segForm"], "literal_family_definition"),
    },
    {
        "id": "TI2", "title": "Finite full lattices, optimal primitive-test rank and tensor near-diagonal rank",
        "status": "complete_elementary_proof; paired_lift_identity_retained_as_input",
        "statement": "The source block lattices are finite free and full with integral pairing; Smith factors exactly determine maximal good saturated rank. A diagonal pairing modulo w^c gives the stated tests whenever each diagonal valuation is below c/2.",
        "sources": many("BLOCKFG", ["bb_coeff", "fg_inter", "blockFG_all", "partners_to_factors_holds"])
                   + many("COUNT", ["span_inf_bbSpec", "finrank_blockLat"])
                   + many("OBJ", ["GoodSub", "GoodShare", "badShare"], "exact_primitive_test_definitions")
                   + many("PAIRLIFT", ["PairLiftAt"], "retained_construction_input")
                   + many("PAIRLIFT", ["liftVecAt_of"]),
    },
    {
        "id": "TI3", "title": "Exact gamma polynomial degree and leading form by harmonic contraction and Taylor evaluation",
        "status": "complete_new_short_proof_of_exact_GamDeg_and_GamLead",
        "statement": "For the actual freeze substitution and tiePhi normalization, degree is at most S+o-max(e,e'), and the equal-order leading coefficient is e! binom(z+e,e) times the initial Fock pairing divided by o!S!product d_i!.",
        "sources": many("LEVEL", ["tieE", "tieF", "tiePhi", "LevelAct"], "literal_operators_and_identity")
                   + many("FROZEN", ["freezeSub", "freeze"], "literal_substitution")
                   + many("GAMSTMT", ["tieGam", "GamDeg", "GamLead"], "exact_source_target")
                   + many("GAMDEG", ["phi_E_pow", "gam_oneSided", "gamma_degree_bound"])
                   + many("GAMLEAD", ["gamma_leading_term"]),
    },
    {
        "id": "TI4", "title": "Integral binomial coefficients by multinomial carries and finite differences",
        "status": "complete_new_proof_of_GamInt_constant_10_and_parameter_dependent_variant; exact_GamIntC_not_claimed",
        "statement": "Integral coefficients hold after the explicit exponent (2r+1)floor log_p(S+o+r)+(N+2)(r-1)floor log_p(3S), with S=0 treated separately. This implies the source GamInt exponent 10(N+3)r^2(floor log_p(S+o+r)+1).",
        "sources": many("INTSTMT", ["GamInt"], "exact_source_target")
                   + many("GAMINT", ["tieGam_expand", "gamma_integrality_of_contraction", "gamma_integrality"])
                   + many("SHARPINT", ["GamIntC"], "stronger_source_statement_not_claimed")
                   + many("SHARPPROOF", ["gamma_integral_holds"], "source_proof_of_stronger_unreconstructed_statement"),
    },
    {
        "id": "TI5", "title": "Complete polynomial-matrix average on a p-adic-unit progression",
        "status": "complete_elementary_human_proof_of_WindowFullAP",
        "statement": "Integral binomial discs, a determinant-coefficient Smith bound, Gauss norm root factorization and residue-class counting give average bad Smith count <= n[d/Y+(L+dh/Y)/E].",
        "sources": many("WINDOW", ["MahlerK", "binMatK", "ValuationWindowLowerBound"], "exact_source_interfaces")
                   + many("AP", ["WindowCountAP", "DiscsDisjointAP", "WindowMeanAP", "WindowFullAP"], "exact_source_target")
                   + many("MAHLER", ["mahler_binomial_unit_ball"])
                   + many("APCOUNT", ["window_count_progression", "root_discs_disjoint_progression"])
                   + many("APMEAN", ["windowMeanAP_of", "windowFullAP_of"]),
    },
    {
        "id": "TI6", "title": "Actual one-tie Gram average with determinant and rounding constants explicit",
        "status": "proved_conditional_on_explicit_graded_Gram_hypothesis; source_normalization_preserved; slightly_weaker_constant_variant",
        "statement": "For the actual matrix p^ceil(kappa) Gamma, average bad count is at most n[2S/Y+(ceil(kappa)+kappa4+3ell+2Sell/Y)/E]. Equal-order initial Gram blocks supply the determinant leading coefficient. The source's restricted graded Gram input remains explicit.",
        "sources": many("GRAM", ["GramDeterminantGradedHypothesis"], "retained_representation_input")
                   + many("MEANSTMT", ["MeanGam"], "parallel_source_mean_statement")
                   + many("MEAN", ["betaT", "gramT", "meanGam_of"])
                   + many("SHARPINT", ["MeanGamC"], "sharpened_source_variant_not_identified_with_our_constants")
                   + many("GRAMPART", ["meanGamX", "gram_hypothesis_of_log_bound"], "actual_source_connection_and_retained_graded_bridge"),
    },
    {
        "id": "TI7", "title": "Dimension-weighted transfer by simultaneous degree translations",
        "status": "complete_elementary_proof_conditional_on_literal_KeyIneq_and_numeric_density",
        "statement": "The injective translate map and a product of scalar harmonic-dimension sums convert KeyIneq into mean kF<=2 mean kx under the source volume and density hypotheses.",
        "sources": many("MEANDEFS", ["RestDims", "KeyIneq", "Avg", "MeanX"], "exact_inputs_and_output")
                   + many("DENSITY", ["P1", "DensityNumericalFacts"], "literal_density_hypotheses")
                   + many("DENSITY", ["sum_kF_mul_prod_le_kx", "avg_abs", "avg_of"]),
    },
    {
        "id": "TI8", "title": "Final kappa translation and boundary loss",
        "status": "complete_elementary_proof_conditional_on_enlarged_mean_and_numeric_boundary_bounds",
        "statement": "The actual lower-shift/boundary term, twice upper-shift term and 12Nkc/b' give mean kText<=6(CA+Cs)NN1/Y+2/Y, hence the source constant 6(CA+Cs)+8.",
        "sources": many("KAPPA", ["kText"], "literal_final_exceptional_function")
                   + many("FINALMEAN", ["ColumnSpanNumericalFacts"], "literal_numerical_hypotheses")
                   + many("FINALMEAN", ["sum_first", "mean_of"]),
    },
    {
        "id": "TI9", "title": "Exact full-Type-I target and remaining construction bridges",
        "status": "explicit_open_boundary; full_Type_I_Conclusion2_not_proved_here",
        "statement": "Restricted graded Gram, simultaneous partner compatibility, weighted digit-class estimates, actual paired edge lifts, harmonic-model/cleaning passage and uniform numerical supply remain separate obligations.",
        "sources": many("ENDPOINT", ["HypI", "WeightI", "tI", "Conclusion2"], "literal_full_Type_I_target")
                   + many("GRAMPART", ["gram_hypothesis_of_log_bound", "theoremMV7"], "retained_representation_bridge")
                   + many("PARTNER", ["tieOpsX_main", "partnerMX_of_parts"], "retained_simultaneous_partner_bridge")
                   + many("BLOCKMEAN", ["RestAll", "segment_weighted_counting_bound_of_all_remaining_bounds"], "retained_weighted_block_bridge")
                   + many("BRIDGE", ["WittIdent"], "retained_actual_polynomial_comparison")
                   + many("RAWTAIL", ["RestRawTail1"], "retained_actual_raw_tail_estimate")
                   + many("RAWFORM", ["RestForm"], "retained_actual_pairing_identity")
                   + many("RAWLIFT", ["paired_lifts_of_identity"], "retained_actual_edge_lift_construction")
                   + many("ASSEMBLY", ["theorem_I_of_intermediate_bounds"], "source_final_uniform_assembly"),
    },
]

artifacts = []
for name in ("report.txt", "type_one_section.tex", "build_provenance.py"):
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
payload = {
    "component": "v0.8 Type-I r=1 local branch", "claims": CLAIMS,
    "repository": BASE_URL, "commit": COMMIT,
    "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "source_files": [{k: v for k, v in info.items() if not k.startswith("_")} for info in FILES.values()],
    "artifacts": artifacts,
    "scope_note": "TI3/TI4/TI5 are complete elementary reconstructions; TI6/TI7/TI8 retain precisely stated inputs. The full Type-I endpoint remains open. No Lean build is asserted.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
lines = [f"Type-I provenance at {COMMIT}", ""]
for claim in CLAIMS:
    lines.extend([f"{claim['id']}: {claim['title']}", f"Status: {claim['status']}"])
    for src in claim["sources"]:
        lines.append(f"  {src['declaration']} | {src['path']}:{src['line_start']}-{src['line_end']} | {src['role']}")
        lines.append(f"    {src['pinned_url']}")
        lines.append(f"    file sha256 {src['full_file_sha256']} ; range sha256 {src['range_sha256']}")
    lines.append("")
(HERE / "source_locators.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({"claims": len(CLAIMS), "source_files": len(FILES),
                  "locators": sum(len(c['sources']) for c in CLAIMS),
                  "verified_commit": COMMIT, "artifacts": artifacts}, indent=2))
