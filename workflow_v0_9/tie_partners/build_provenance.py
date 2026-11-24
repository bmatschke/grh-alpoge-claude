"""Rebuild TP1--TP11 provenance from the pinned, byte-identical Lean checkout.

Writes only this component's provenance.json and source_locators.txt.
No network, Lean edits, compilation or kernel replay. Inclusive line ranges
retain their original bytes and line endings. Requires Python 3.11+.
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
GM = "src/Formalism/MahlerMeasure/"
PM = "src/Formalism/ThetaLogCoordinates/PartnerMeanCoordinates/"
PD = "src/Formalism/PolynomialDimension/"
PATHS = {
    "OBJ": GM + "GoodCount.lean",
    "FROZEN": GM + "IsFrozenInv.lean",
    "SUBSPACE": GM + "CsSaturated.lean",
    "STMT": GM + "StatementT.lean",
    "TM": GM + "StatementTM.lean",
    "LEVEL": GM + "LevelSum.lean",
    "FREEZEIN": GM + "MahlerMeasureProofs/FreezeInto.lean",
    "FREEZEBIJ": GM + "MahlerMeasureProofs/FreezeBij.lean",
    "FREEZEY": GM + "MahlerMeasureProofs/FreezeY.lean",
    "ADAPTED": GM + "MahlerMeasureProofs/TheoremM.lean",
    "GAMINT": GM + "MahlerMeasureProofs/GamInt.lean",
    "GAMINTC": PM + "PartnerMeanProofs/GamIntC.lean",
    "MC": PM + "TheoremMCB.lean",
    "MX": PM + "TheoremMXB.lean",
    "MEANX": PM + "PartnerMeanProofs/NatLogLeOfLe.lean",
    "MEAN": GM + "MahlerMeasureProofs/MeanGam.lean",
    "TIE": PD + "MultinomialDepth/TieOps.lean",
    "PARTNER": PM + "PartnerMeanProofs/GammaZeroIntegral.lean",
    "YPARTNER": PM + "PartnerMeanProofs/PartnerConditionHolds.lean",
    "MONOCOUNT": PD + "MultinomialDepth/MonoCount.lean",
    "MONOTONE": GM + "MahlerMeasureProofs/WeightSpaceDimensionMonotone.lean",
    "PARTNERM": PD + "MultinomialDepth/PartnerM.lean",
    "BAD": GM + "MahlerMeasureProofs/BadCrit.lean",
    "MXPROOF": PM + "PartnerMeanProofs/TheoremMXBOfPoint.lean",
    "MVPROOF": PM + "PartnerMeanProofs/GramHypothesisOfLogBound.lean",
    "CHAIN": PD + "ChainOrderLetters.lean",
    "NUM": PD + "DigitSumValuationBound.lean",
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
        "id": "TP1",
        "title": "Literal prefix and highest-vector lattices, integral freeze isomorphism and adapted bases",
        "status": "proved_from_explicit_substitution_and_saturated_coefficient_filtration",
        "dependencies": [],
        "statement": "Freeze is an integral isomorphism from the actual smaller-GL highest/full-weight prefix lattice MMwZ to the full highest-vector lattice after adjoining a covector of degree n>=S, with exactly the old prefix constraints. The order filtration has an integral adapted basis.",
        "sources": many("OBJ", ["Letters", "glAct", "wt", "YCond", "Y", "YZ", "fockN", "TieData", "TieData.Admissible", "TieData.S"], "literal_objects")
            + many("SUBSPACE", ["HWC", "MMw", "MMwZ", "FilE", "grLat"], "literal_lattices")
            + many("FROZEN", ["freezeSub", "freeze", "FreezeBij", "FreezeY"], "literal_substitution_and_targets")
            + many("TM", ["Letters.setTies", "TieData.thrUpTo", "TieData.Ffull"], "literal_parameters")
            + many("FREEZEIN", ["extendMapsTo"])
            + many("FREEZEBIJ", ["extendBijOn"])
            + many("FREEZEY", ["extendWeightBounded"])
            + many("TIE", ["hw_is_Ffull", "Ffull_indep", "mmw_finite"])
            + many("ADAPTED", ["existsAdaptedBasis"]),
    },
    {
        "id": "TP2",
        "title": "Exact GamIntC by a shorter paired-contraction factorial calculation",
        "status": "proved_with_exact_archival_exponent; four_B_residual_bound_is_a_derived_simplification",
        "dependencies": ["TI3"],
        "statement": "For integral f,g, p^(((K+4)r+6)floor log_p(S+o+r)) Gamma has integral binomial coefficients and degree<=S+o. After the coefficient and row groupings the residual valuation is exactly -v binom(S,j-a)-2v binom(o,j)-v binom(j,a'), so the source's six-B allowance is sufficient.",
        "sources": many("MC", ["GamIntC"], "exact_source_target")
            + many("LEVEL", ["tieE", "tieF", "tiePhi"], "literal_operators")
            + many("GAMINT", ["FT_pow_coeff_norm", "termF", "fock_Dop_term", "tieGam_expand"], "source_expansion_correspondence")
            + many("GAMINTC", ["kapE", "term_valE", "termF_IVPE", "gamma_integral_holds"], "parallel_source_proof; human_factorial_cancellation_compresses_it"),
    },
    {
        "id": "TP3",
        "title": "Exact MeanGamX including its ceiling and digit-sum compensation",
        "status": "proved_using_GG_for_the_literal_initial_Gram_input",
        "dependencies": ["TP1", "TP2", "TI3", "TI5", "GG7"],
        "statement": "The adapted-order determinant leading term and exact Legendre compensation give average bad Smith count <= b[2S/Y+(kappa+3ell+kappa4+2Sell/Y)/E] for the actual p^ceil(kappa) Gamma matrix, with the literal MeanGamX premises.",
        "sources": many("MX", ["MeanGamX"], "exact_source_target")
            + many("STMT", ["GramDeterminantGradedHypothesis"], "explicit_input_supplied_by_GG")
            + many("MEAN", ["betaT", "gramT", "lead_part", "lead_bound"], "exact_leading_coefficient_and_budget")
            + many("MEANX", ["per_rowX", "meanGamX_of"])
            + many("MVPROOF", ["meanGamX"], "actual_source_assembly"),
    },
    {
        "id": "TP4",
        "title": "Prefix extension and exact integral cost of an equivariant highest-vector map",
        "status": "proved_using_GG_HypP_and_HypW; no_integral_isotypic_splitting",
        "dependencies": ["GG2"],
        "statement": "The product of the early cutoff projectors costs j0*e1; extension of a map integral on highest vectors spends e1 for pure-type projection and e1 for Weyl generation. Thus p^((j0+2)e1) times the actual coefficientwise extension preserves YZ.",
        "sources": many("STMT", ["HypP", "HypW"], "inputs_supplied_by_GG2")
            + many("TIE", ["Cset", "IsProjC", "projC", "divpow_int", "int_main", "IsEqC", "inOp", "bigOp", "bigOp_Y", "bigOp_int"]),
    },
    {
        "id": "TP5",
        "title": "Explicit one-tie partial inverse, adjointness and exact weighted codimension",
        "status": "proved_for_the_actual_Smith_bases_and_prefix_constraints",
        "dependencies": ["TP1", "TP4"],
        "statement": "The good Smith blocks define tau and varpi by the explicit highest-vector formula. Their full-word extensions satisfy the source adjointness, integer cost K_i=e1(pos_i+4), later-tie commutation and codimension bounded by sum_w bad_i,w*dim(YYsp_i,w).",
        "sources": many("MX", ["TieOpsX"], "exact_source_target")
            + many("PARTNER", ["gamma_zero_integral", "tieOpsX_main"])
            + many("TIE", ["eqExt", "form_zero", "phi_glAct", "phi_ext_comm", "fock_ext_reduce", "smith_bases", "good_norm", "count_le", "transport_le", "tie_core"])
            + many("TM", ["TieData.YYsp"], "literal_continuation_space"),
    },
    {
        "id": "TP6",
        "title": "An actual integral primitive partner before ties",
        "status": "proved_from_a_unit_coefficient_and_self_adjoint_prefix_projections",
        "dependencies": ["GG2"],
        "statement": "Every primitive u in YZ has an integral z in YZ with |FockN(u,z)|>=p^(-e1(N+1)). The normalized monomial pairing is an inverse product of integer multinomials; the exact projector product supplies the partner.",
        "sources": many("MC", ["YPartnerC"], "exact_source_target")
            + many("YPARTNER", ["partner_condition_holds"])
            + many("OBJ", ["fockN", "YZ"], "actual_form_and_lattice"),
    },
    {
        "id": "TP7",
        "title": "Simultaneous ordered integral partners and the actual pointwise bad count",
        "status": "proved; saturation_and_ordered_peeling_explicit",
        "dependencies": ["TP5", "TP6"],
        "statement": "The saturated intersection of all pi_i-fixed spaces has the stated weighted codimension. Ordered products of p^K_i T_i give an integral partner for every primitive vector at exact depth floor[t(E+kappa)+kappa]; Smith form then proves PointMX.",
        "sources": many("MX", ["PartnerMX", "PointMX"], "exact_source_targets")
            + many("PARTNER", ["partnerMX_of_parts", "pointMX_of_partner"])
            + many("PARTNERM", ["peel", "finrank_lattice", "codim_inf_le"])
            + many("STMT", ["BadCrit"], "exact_linear_algebra_interface")
            + many("BAD", ["bad_criterion_holds"])
            + many("OBJ", ["goodCount", "bad"], "literal_rank_count"),
    },
    {
        "id": "TP8",
        "title": "Exact highest-weight multiplicity identity for the selected continuation spaces",
        "status": "proved_over_the_field; no_integral_semisimplicity_assumption",
        "dependencies": ["TP1"],
        "statement": "The actual selected subspace satisfies sum_w dim(MMw_i,w)*dim(YYsp_i,w)=dim(Y). The equality is independent of the chosen nonzero highest vector in each type.",
        "sources": many("TM", ["MonoCount", "TieData.YYsp"], "exact_source_target_and_space")
            + many("MONOCOUNT", ["GlX.exists_theta", "count_Y", "count_HW", "tie_onto", "tie_into", "finrank_MMw", "monomial_count"]),
    },
    {
        "id": "TP9",
        "title": "Monotonicity of actual continuation dimensions by Cartan-projected multiplication",
        "status": "proved_by_explicit_rational_injection; source_Casimir_route_identified",
        "dependencies": ["TP1"],
        "statement": "Increasing a tied covector degree by u sends the frozen highest vector to y_rho^u h. Projection of multiplication by that monomial onto its Cartan component gives an injection of the actual YYsp spaces, preserving every early and late prefix cutoff.",
        "sources": many("TM", ["WeightSpaceDimMonotone"], "exact_source_target")
            + many("MONOTONE", ["ycond_mul_cov", "Ffull_step", "weight_zero_span_highest", "highest_weight_dim_monotone"], "source_Casimir_implementation_of_the_same_injection"),
    },
    {
        "id": "TP10",
        "title": "The exact rectangular-grid mean with coordinate-top dimension weights",
        "status": "proved_with_literal_TheoremMXB_constants_and_weights",
        "dependencies": ["TP3", "TP7", "TP8", "TP9"],
        "statement": "The average bad count at depth floor[t(E+kappa)+kappa] is <=sum_i epsilon_i Avg dim Y(n with i at top), epsilon_i=2Si(top)/Yi+(2kappa+2Si(top)ell/Yi)/E. No endpoint-update injectivity or uniform dimension substitution is used.",
        "sources": many("MX", ["TheoremMXB"], "exact_source_target")
            + many("MXPROOF", ["theoremMXB_of_point"])
            + many("ADAPTED", ["grid_average"])
            + many("MVPROOF", ["theoremMXB"], "actual_source_assembly"),
    },
    {
        "id": "TP11",
        "title": "Literal TheoremMV7 with exact kapSeg and no new partner or multiplicity input",
        "status": "proved_using_TP_and_GG_under_literal_word_grid_and_SizeHypothesis",
        "dependencies": ["TP10", "GG8"],
        "statement": "For N=2s+1 and the literal admissible chain and size hypotheses, use ell=log_p(8a+r)+1, e1=floor(r^2ell), kappa4=(s+4)r^2ell, kappa=3(s+2)r^2ell. The exact source TheoremMV7 follows, retaining endpoint dimensions and floor depth. Later segment/digit and edge-lift applications remain separate.",
        "sources": many("CHAIN", ["ChainOrderLetters", "ConditionShape", "SizeHypothesis", "TheoremMV7", "TheoremMV7Of"], "literal_hypotheses_and_target")
            + many("NUM", ["lgSeg", "kapSeg", "epsSeg"], "literal_constants")
            + many("MVPROOF", ["gram_hypothesis_of_log_bound", "theoremMV7Of", "theoremMV7"], "actual_source_application"),
    },
]

artifacts = []
for name in ("report.txt", "main.tex", "build_provenance.py"):
    raw = (HERE / name).read_bytes()
    artifacts.append({"path": name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})

all_ids = {claim["id"] for claim in CLAIMS}
external = {"TI3", "TI5", "GG2", "GG7", "GG8"}
for claim in CLAIMS:
    assert set(claim["dependencies"]) <= all_ids | external
assert len(CLAIMS) == 11 and len(all_ids) == 11

payload = {
    "artifact_version": "0.9",
    "component": "simultaneous integral tie partners and exact dimension-weighted mean",
    "claims": CLAIMS,
    "repository": BASE_URL,
    "commit": COMMIT,
    "head_verified": actual_head,
    "line_range_convention": "inclusive, one-indexed, original bytes including line endings",
    "source_files": [{k: v for k, v in info.items() if not k.startswith("_")} for info in FILES.values()],
    "artifacts": artifacts,
    "explicit_external_dependencies": sorted(external),
    "reused_completed_inputs": {
        "TI3": "actual gamma degree and leading coefficient, including all Fock normalization",
        "TI5": "p-adic polynomial-matrix average with integer disc depth h",
        "GG2": "literal HypP, HypW and their common integral exponent",
        "GG7": "actual order-initial lattice Gram bound for every adapted basis",
        "GG8": "literal tie-prefix and full-word quantitative application",
    },
    "derived_simplifications": [
        "TP2 exact factorial cancellation leaves four binomial B losses; downstream source allowance six B retained.",
        "TP9 rational Cartan-component projection compresses the source's explicit Casimir-chain injection; all cutoff conditions are proved.",
        "TP7 ordered peeling keeps the noncommuting partial inverses in their actual source order.",
    ],
    "outside_scope": [
        "Subsequent segment/digit-class and endpoint dimension-family comparison (SW).",
        "Actual paired polynomial lifts into cleaned Type-I edge lattices (RL).",
        "Global arithmetic, spectral, metric, and cohomological input supply for RH/GRH.",
    ],
    "scope_note": "TP1--TP11 are human mathematical reconstructions. GG supplies precisely identified projection/Weyl/graded-Gram inputs; no further partner, highest-weight-multiplicity, or dimension-monotonicity premise remains. Field-level split characteristic-zero highest-weight theory is declared background. No Lean build or kernel replay is asserted.",
}
(HERE / "provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
lines = [f"Tie-partner provenance at {COMMIT}", ""]
for claim in CLAIMS:
    lines.extend([f"{claim['id']}: {claim['title']}", f"Status: {claim['status']}",
                  "Dependencies: " + ", ".join(claim["dependencies"])])
    for src in claim["sources"]:
        lines.append(f"  {src['declaration']} | {src['path']}:{src['line_start']}-{src['line_end']} | {src['role']}")
        lines.append(f"    {src['pinned_url']}")
        lines.append(f"    file sha256 {src['full_file_sha256']} ; range sha256 {src['range_sha256']}")
    lines.append("")
(HERE / "source_locators.txt").write_text("\n".join(lines) + "\n")
print(json.dumps({"claims": len(CLAIMS), "source_files": len(FILES),
                  "locators": sum(len(c["sources"]) for c in CLAIMS),
                  "verified_commit": COMMIT, "artifacts": artifacts}, indent=2))


