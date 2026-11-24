"""Regenerate the IP1--IP11 source ledger from unchanged pinned Lean bytes.

Run with Python 3.11+ from any directory. No network or Lean installation is
needed. Every cited working-tree file is compared byte-for-byte with git's
pinned blob before any ledger is emitted. The script does not edit sources.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

WORK = Path(__file__).resolve().parent
REPO = WORK.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
JP = "src/Formalism/ThetaLogCoordinates/JacobiPathWeights/"
PATHS = {
    "O": GB + "ObjPol.lean",
    "ST": GB + "StatementOfDegreeAndBound.lean",
    "SC": GB + "SourceCleaning.lean",
    "WITT": GB + "WittFrameLocaliserOrders.lean",
    "GI": GB + "PathWeight/GeneratorImageIsSymbol.lean",
    "CO": GB + "PathWeight/CoeUntopDLeAlt.lean",
    "LW": GB + "PathWeight/LetterWeightPos.lean",
    "KID": GB + "BinomialPolynomialIdentities/KcolEqPathWord.lean",
    "STD": GB + "BinomialPolynomialIdentities/IndexOffRange.lean",
    "RES": GB + "BinomialPolynomialIdentities/ExtendByZeroRestrictOfVanish.lean",
    "AP": GB + "BinomialPolynomialIdentities/AdmissiblePolynomialBasisProv.lean",
    "CAN": JP + "JacobiMinorProofs/IsWeightedHomogeneousZeroStripPathWord.lean",
    "FLAG": JP + "JacobiMinorProofs/LinearIndependentOfLead.lean",
    "JAC": JP + "JacobiMinorProofs/JacobiMinorProof.lean",
    "EV": JP + "JacobiMinorProofs/LemmaA2indepOf.lean",
    "MAT": JP + "JacobiMinorProofs/PathBasisOfCount.lean",
    "PB": JP + "PathBasisTheorem.lean",
    "CP": JP + "StatementP.lean",
    "FP": JP + "FinalP.lean",
    "SUP": JP + "JacobiMinorProofs/ExistsSuppOfEvalNe.lean",
    "A3": GB + "FrobeniusPaths/ComponentsInFiltrationContractionSingle.lean",
    "PG": GB + "MonomialOrderSegments/LiftBoundOfHypotheses.lean",
    "BR": GB + "MonomialOrderSegments/BrSpan.lean",
    "BRG": GB + "MonomialOrderSegments/BrSpanG.lean",
    "COL": GB + "ProjectionOfIsotypicDecomposition.lean",
    "JOIN": GB + "FrobeniusPaths/AntitoneOfAppend.lean",
    "SPLIT": GB + "FrobeniusPaths/JointTypeLatticeSaturated.lean",
    "OK": GB + "FrobeniusPaths/ColOKOfPath.lean",
    "WS": GB + "FrobeniusPaths/WedgeSplitTan.lean",
    "STEP": GB + "FrobeniusPaths/SelfDualLatticesOneOrbit.lean",
    "NOM": GB + "FrobeniusPaths/NmHContrPos.lean",
    "ORD": GB + "FrobeniusPaths/LiftedColumnOrder.lean",
    "FC": GB + "FrobeniusPaths/LatticeCountingFormula.lean",
    "OWN": GB + "FrobeniusPaths/ColStepFactor.lean",
    "CONG": GB + "FrobeniusPaths/LiftedColumnCongruence.lean",
    "INT": GB + "FrobeniusPaths/ColumnKernelComponentsIntegral.lean",
    "DEG": GB + "FrobeniusPaths/LiftedColumnMultidegree.lean",
    "KEY": GB + "FrobeniusPaths/CanonicalTranslateJetIdentity.lean",
}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|instance|namespace|end|section|variable|attribute|open|include)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")
FILES = {}

for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise ValueError(f"Working-tree bytes differ from pinned source: {path}")
    lines = raw.splitlines(keepends=True)
    stack = []
    declarations = []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if match := NS.match(line):
            stack.append(("namespace", match.group(1)))
        elif match := SEC.match(line):
            stack.append(("section", match.group(1)))
        elif match := END.match(line):
            if not stack:
                raise ValueError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if match.group(1) and match.group(1) != label:
                raise ValueError((path, i + 1, "end label mismatch", label, match.group(1)))
        elif match := DECL.match(line):
            name = match.group(1)
            ns = ".".join(label for kind, label in stack if kind == "namespace")
            declarations.append({"name": name, "line": i, "qualified": f"{ns}.{name}" if ns else name})
    FILES[key] = {
        "path": path,
        "sha256": sha256(raw).hexdigest(),
        "bytes": len(raw),
        "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines,
        "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    item = FILES[key]
    hits = [decl for decl in item["_declarations"] if decl["name"] == name]
    if occurrence >= len(hits):
        raise ValueError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = item["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": item["path"],
        "declaration": decl["qualified"],
        "source_spelling": name,
        "line_start": start + 1,
        "line_end": end,
        "role": role,
        "full_file_sha256": item["sha256"],
        "range_sha256": sha256(excerpt).hexdigest(),
        "range_bytes": len(excerpt),
        "pinned_url": f"{URL}/blob/{COMMIT}/{item['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]


CLAIMS = [
    {
        "id": "IP1",
        "title": "The literal signed path, exterior-column, and standard-index family",
        "status": "faithful_translation",
        "statement": "Signed horizontal-strip paths of dominant integer weights define Kcol by right exterior multiplication/contraction. Complementing nonpositive-column index subsets gives the source IsSt inequalities. The finite product equals Psi exactly, including all identity factors outside the effective range.",
        "sources": many("O", ["HStrip", "PPath", "colH", "extOne", "wedgeR", "contrR", "colStep", "Kcol", "colRange", "Psi", "Ican", "tabCol", "IsSt"], "literal_definition")
          + many("KID", ["wedgeR_eq_wedgeF", "contrR_eq_contrF", "Kcol_eq_pathWord", "restPsi"], "proved_normalization_identity")
          + many("STD", ["hstrip_iff", "restPathTo", "restPathFrom", "restStd"], "proved_normalization_identity"),
    },
    {
        "id": "IP2",
        "title": "Independence in every characteristic by canonical leading terms and generic flag minors",
        "status": "faithful_translation",
        "statement": "Canonical path products have a unit leading component recovering the preceding endpoint. Their fixed-endpoint independence holds over every field. Jacobi converts generic terminal-index coefficients into determinant powers times standard flag-minor products with distinct diagonal leading monomials. A maximal-endpoint projection combines the two independence statements. No rational isotypic membership is asserted.",
        "sources": many("CAN", ["rw_", "rho", "psi_lead", "end_determined", "psi_lead_unit", "pathProductLinearIndependent"])
          + many("FLAG", ["Lead_minor", "tab_inj", "Lead_tab", "path_basis_lemma"])
          + many("JAC", ["jacobi_gen", "brk_eq", "fact_break"])
          + many("EV", ["col_act", "act_psi", "idxWeight_can", "factEV_of", "lemmaA2indep_of"]),
    },
    {
        "id": "IP3",
        "title": "Pieri counting and the unimodular integral path basis",
        "status": "faithful_translation_with_alternative_count_proof",
        "statement": "Row insertion proves the horizontal-strip counting identity; complement-reversal gives downward strips and determinant shifts allow arbitrary integer weights. Iteration matches the monomial count. All-prime independence forces the integer coefficient determinant to be a unit, giving the actual basis over every commutative ring.",
        "derivation": "The all-prime determinant argument translates the source. The expanded report proves the count directly by semistandard row insertion; the archive's exported count uses Gelfand--Tsetlin recursion. The count is not an unresolved representation theorem.",
        "sources": many("CP", ["GTPieri", "StdCountGT", "CountPAll", "CountCont"], "exact_count_target")
          + many("FP", ["gtPieri", "stdCountGT", "countCont", "countPAll"], "archival_count_binding")
          + many("MAT", ["det_unit", "basis_of", "path_basis_of_count"])
          + many("PB", ["path_basis_theorem", "psiPath_basis"], "source_export")
          + many("RES", ["word_basis_of_path_restrictions"], "exact_finite_index_transport")
          + many("AP", ["admissible_standardPath_basis"], "source_export"),
    },
    {
        "id": "IP4",
        "title": "Simultaneous integral adaptation to every prefix minimum and maximum",
        "status": "derived_alternative_proof",
        "statement": "Over an integral domain, the same integral basis is adapted to all source generic-conjugated rank-one prefix minimum/maximum bounds. The full-prefix converse isolates a maximal bad endpoint. Earlier prefixes follow from cutting the actual columns and counting continuations. Uniqueness intersects all prefix conditions, and fraction-field descent retains integral coefficients.",
        "derivation": "This replaces the source's larger abstract representation-filtration route with an elementary generic-weight and dimension argument. It does not assert an integral direct sum of individual rational irreducibles. The exact coordinate-weight/generic-conjugate identification is explained in IP4 of report.txt.",
        "sources": many("O", ["twistSub", "sDegs", "valS", "lam1S"], "literal_weight_definition")
          + many("SUP", ["conj_mem_supp", "gen_mem_supp"], "generic_weight_identification")
          + many("ST", ["A3at", "DefiniteRankOne", "PathBasisOverRing", "FirstLettersLowerSet"], "exact_target_and_archival_interface")
          + many("A3", ["mem_span_words_of_valuation_bounds", "valuation_bounds_of_mem_span_words", "lemma_A3_over_field", "lemma_A3_over_domain"], "parallel_archival_filtration_route")
          + many("CP", ["CountCont"], "exact_continuation_count"),
    },
    {
        "id": "IP5",
        "title": "All column clauses of the shared PlaneGram SPAN interface",
        "status": "faithful_translation_with_direct_column_proof",
        "statement": "The exact Kcol factors are multilinear on their occurrence sets, each letter occurs in d_i factors, positive height is bounded by preceding vector occurrences, prefix column valuation is at least colVal, and summing colVal gives the last path coordinate. Together with IP3--IP4 these prove the literal PlaneGram.SPAN, over the valuation ring in that interface.",
        "sources": many("PG", ["colVal", "SPAN"], "exact_downstream_interface")
          + many("COL", ["Kcol_hom", "column_height_le_used_count", "span_column_clauses_at"])
          + many("BRG", ["col_est", "stage_identity", "span_mem"])
          + many("BR", ["brSPAN"], "source_interface_assembly")
          + many("A3", ["column_kernel_support_degree", "twisted_column_lower_filtration"], "parallel_column_weight_proof"),
    },
    {
        "id": "IP6",
        "title": "The exact integral MGen0-to-PGen spanning inclusion",
        "status": "faithful_translation",
        "statement": "Apply the simultaneous integral path basis to A and G in each literal MGen0 generator. The source CondM zero-gap bounds give precisely the cross-block interlacing inequalities; the initial preceding-frame block has only vector letters and G-degree zero. Appending the two paths produces exactly PGen, so multiplying the integral expansions proves GeneratorSpanInclusion.",
        "hypotheses": ["source frame segment and increasing lifted positions", "r,K positive", "integral coefficient domain", "the literal MGen0 degree and CondM conditions"],
        "sources": many("GI", ["Ctx", "LLs", "CondM", "MGen0", "PGen", "GeneratorSpanInclusion"], "exact_setting_family_and_target")
          + many("CO", ["lattice_path_nonneg_prefix", "lattice_path_zero_prefix", "even_of_lower_letter", "first_letter_is_lower", "generator_pair_conditions_of_admitted"])
          + many("JOIN", ["hstrip_append", "antitone_append", "prvB1_of_D7"]),
    },
    {
        "id": "IP7",
        "title": "Literal split-product identity and direct weighted normal homogeneity",
        "status": "derived_simplification",
        "statement": "For each actual PGen, prod_plTan gives P as the product of its joined split columns. A column's block changes once per used letter; the normal weighted degree is exactly the sum of p^(z-s_i) at costly steps. The source size bound N+r<=K keeps every negative column above the rank boundary. Parity is preserved by reduction modulo even n'.",
        "derivation": "The product identity is copied exactly from the source. Direct block-by-block homogeneity proves the needed conclusion without importing PathWeightComponents or the saturated joint-type parts of ConclusionB3. The selected PGen family has not been replaced.",
        "sources": many("O", ["joinPT", "PsiPl", "PsiTan", "plTanCol", "joinI", "symWt", "IsCostly", "oc", "IsUsed"], "literal_definition")
          + many("SPLIT", ["joinI_pl", "joinI_tan", "prod_plTan"], "exact_product_identity")
          + many("OK", ["ColOK", "colOK_of_path"], "negative_column_height_control")
          + many("LW", ["letter_enum_strictMono", "normal_iff_letter_column", "segment_substitution_aeval", "segment_count_add_rank_le"], "actual_frame_normalization")
          + many("ST", ["PathWeightComponents", "ConclusionB3"], "larger_archival_inputs_not_assumed"),
    },
    {
        "id": "IP8",
        "title": "The actual integral Frobenius column polynomial",
        "status": "faithful_translation",
        "statement": "The key is KKc: between used lifted positions raise every component of the exterior array to p^(gap), apply the next adapted-letter wedge/contraction, and apply the final power to z. Integrality and final letter degrees follow by induction. This is not a characteristic-zero Frobenius substitution of the finished ordinary column.",
        "hypotheses": ["the actual finite faithful Witt algebra O", "O a DVR with uniformizer w and w^2=p", "p>=13 and even n'>0 in the source context", "g integral invertible over the Witt ring", "strict selected positions and terminal bound"],
        "sources": many("SC", ["OHyp"], "literal_coefficient_ring_hypotheses")
          + many("O", ["WF", "sigPow", "letG", "powC", "KKstate", "KKc", "powSubst"], "literal_key_definition")
          + many("INT", ["KKstate_eq", "KKc_eq", "column_kernel_components_integral"])
          + many("DEG", ["lifted_column_multidegree"]),
    },
    {
        "id": "IP9",
        "title": "All-chart divisibility and the two-extra-powers margin",
        "status": "faithful_translation",
        "statement": "The moving exterior-basis identity V^[P]L_t=w^(aP)(Z^[P]+pR), P=p^(t-s), follows from entrywise Witt-Frobenius congruence. Since p=w^2, a nonnominal component gains two extra powers across a strict gap. Nominal support and costly-step geometry then give the exact predicted column order in every chart, including negative columns.",
        "sources": many("STEP", ["sum_pow_dvd", "step1"], "core_integral_power_calculation")
          + many("FC", ["frobCong"], "witt_congruence_proof")
          + many("NOM", ["NmH", "step_nom", "step_van", "TS", "Ord_main"], "support_and_order_induction")
          + many("ORD", ["FrobCong", "mkTS", "zetaL", "lift_substitution_letter", "lifted_column_order"], "actual_chart_transfer"),
    },
    {
        "id": "IP10",
        "title": "Own-chart leading congruence with exact signs and uniform key bound",
        "status": "faithful_translation",
        "statement": "After division by the predicted w-power, only the prescribed split block survives modulo w. Strict gaps kill unwanted tangential terms at costly steps. The right-wedge signs equal those of plTanCol; the negative-column height bound is used here. Residue Frobenius produces phSeg, and distinct positions give a_c<2p^(z-s_0)<=2Q. This proves all IsKey clauses and the separate TT-support requirement.",
        "sources": many("WS", ["wedge_split_tan", "contr_split_tan", "wedge_split_pl", "contr_split_pl", "plTanCol_eq_SgW"], "exact_split_sign_identities")
          + many("OWN", ["Inv_main"], "normalized_residue_induction")
          + many("CONG", ["lift_letG", "lift_KKc", "lifted_column_congruence"])
          + many("INT", ["column_order_le_two_power"], "uniform_order_estimate")
          + many("KEY", ["canonical_translate_jet_identity"], "source_clause_assembly")
          + many("SC", ["IsKey"], "literal_key_interface")
          + many("LW", ["rename_supported_tops", "substitution_rename_lift", "keyLeadingPart", "key_column_leading_bound"], "actual_segment_transport"),
    },
    {
        "id": "IP11",
        "title": "Products of the actual column keys prove GeneratorImageIsSymbol",
        "status": "derived_simplification",
        "statement": "Multiplying the literal leading keys gives w^o phSeg(P), with o the sum of their costly orders. Its normal degree is exactly o. The product belongs to bc_KP and hence bc_agen(o,0) with coefficient one, so it satisfies the exact Sy definition. Zero factors cause no exception.",
        "derivation": "This direct assembly uses IP7--IP10 and the source definitions. Unlike LetterWeightPos.generator_path_homogeneous_holds it does not invoke the larger ConclusionB3 or full PathWeightComponents packages. It proves the same actual-setting GeneratorImageIsSymbol statement.",
        "sources": many("GI", ["Sy", "GeneratorImageIsSymbol"], "exact_target")
          + many("WITT", ["bc_KP", "bc_agen"], "literal_symbol_product_definition")
          + many("LW", ["key_polynomial_leading_part", "generator_path_homogeneous_holds"], "parallel_larger_archival_route"),
    },
]

out = {
    "schema_version": "1.2",
    "artifact_version": "0.5",
    "date": "2026-11-21",
    "owner": "/root/remarks_math",
    "repository": {"url": URL, "commit": COMMIT},
    "range_convention": "One-indexed inclusive line ranges; bytes and line endings preserved. A range starts at the named declaration and stops before the next top-level declaration or namespace/section/variable command. Trailing blank lines are excluded. Qualified source names are resolved from the lexical namespace stack.",
    "verification": {
        "full_file_bytes_compared_with_pinned_git_blob": True,
        "range_bytes_hashed_without_normalization": True,
        "local_lean_compilation": False,
        "lean_kernel_replay": False,
        "replacement_arguments_formalized": False,
        "human_mathematical_proofs_supplied": True,
        "mathematical_cross_review": [
            {"reviewer": "/root", "scope": "IP1--IP6, including all-prime independence, determinant unit, prefix continuation counts, and avoidance of integral semisimplicity", "result": "No mathematical correction found."},
            {"reviewer": "/root/lean_audit", "scope": "IP2--IP5: the four signed column leading-term cases, complementary minors, maximal-dominance isolation, downward complement bijection, prefix continuation count, and the exact SPAN clauses", "result": "No substantive mathematical gap found. The shared integral filtered basis closes the previously retained SPAN input."},
        ],
    },
    "status_definitions": {
        "faithful_translation": "A mathematical proof reconstructing the cited source argument and its literal setting.",
        "faithful_translation_with_alternative_count_proof": "The source's universal integral basis argument, with a direct row-insertion proof replacing its exported Gelfand--Tsetlin count route.",
        "derived_alternative_proof": "An explicitly supplied human proof of the exact target statement by a different argument.",
        "faithful_translation_with_direct_column_proof": "The exact source interface, with its column estimates proved directly from exterior covariance.",
        "derived_simplification": "A direct proof for the exact source family avoiding a larger unused source package; no enlargement of the family is claimed.",
    },
    "files": [{k: v for k, v in item.items() if not k.startswith("_")} for item in FILES.values()],
    "claims": CLAIMS,
    "closed_previous_inputs": [
        "SY6 / GeneratorSpanInclusion, for the actual integral MGen0 and PGen families",
        "SY6 / GeneratorImageIsSymbol, with the literal normal-degree and bc_agen conditions",
        "PlaneGram.SPAN, shared by the local Gram reconstruction: integral basis, all prefix lower-weight conditions, actual factors and column data",
    ],
    "inputs_not_reconstructed_or_claimed_here": [
        "Quantitative Fock projector estimate PROJ",
        "Density or rank lower bound for the selected global symbol space",
        "Remaining spectral, archimedean, arithmetic, or global RH/GRH inputs",
        "An integral direct sum of individual rational irreducible/isotypic lattices (not asserted)",
    ],
    "deliverables": [
        {"path": name, "sha256": sha256((WORK / name).read_bytes()).hexdigest(), "bytes": (WORK / name).stat().st_size}
        for name in ["path_generators_section.tex", "report.txt", "regenerate_provenance.py"]
    ],
}
(WORK / "provenance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    "IP1--IP11 PINNED SOURCE LOCATORS", "", f"Repository: {URL}", f"Commit: {COMMIT}",
    "All files were compared byte-for-byte with this git commit.",
    "All inclusive line ranges retain original bytes and line endings.", "",
]
for claim in CLAIMS:
    lines += [f"{claim['id']}. {claim['title']}", f"Status: {claim['status']}", claim["statement"], ""]
    if "derivation" in claim:
        lines += [claim["derivation"], ""]
    for source in claim["sources"]:
        lines += [
            source["declaration"],
            f"  {source['path']}:{source['line_start']}-{source['line_end']}",
            f"  Role: {source['role']}",
            f"  Full-file SHA256: {source['full_file_sha256']}",
            f"  Range SHA256:     {source['range_sha256']}",
            f"  {source['pinned_url']}",
        ]
    lines.append("")
(WORK / "source_locators.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

unique = {(s["path"], s["line_start"], s["line_end"]) for c in CLAIMS for s in c["sources"]}
print(json.dumps({"claims": len(CLAIMS), "files": len(FILES), "unique_ranges": len(unique), "pinned_bytes_verified": True}))
