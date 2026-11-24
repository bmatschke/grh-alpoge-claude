#!/usr/bin/env python3
"""Rebuild the exact pinned-source ledger for the v0.11 finite coefficient extension and standard-subring proof.

The builder only writes this component directory. Every cited source file is
byte-compared with its Git blob; declaration ranges are inclusive and hashed
without normalization. No Lean build or replacement formalization is claimed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

WORK = Path(__file__).resolve().parents[2]
ROOT = WORK / "alpoge-rh"
OUT = Path(__file__).resolve().parent
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
GL = "src/Formalism/LocalToGlobal/GroupLattices/"
PR = GL + "PerfectRings/"
FM = GL + "FockModels/"
GW = "src/Formalism/GradedWeylDivisibility/"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == COMMIT
files, cache = {}, {}
TOP = re.compile(
    r"^(?:(?:private\s+)?(?:noncomputable\s+)?"
    r"(?:theorem|lemma|def|structure|abbrev|class|inductive|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[\s*)"
)


def source(path):
    if path not in cache:
        raw = (ROOT / path).read_bytes()
        pinned = subprocess.check_output(["git", "show", COMMIT + ":" + path], cwd=ROOT)
        assert raw == pinned, ("source differs from pin", path)
        lines = raw.decode("utf-8").splitlines(keepends=True)
        cache[path] = (raw, lines)
        files[path] = dict(
            path=path, sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw), line_count=len(lines),
            verified_equal_to_pinned_git_blob=True,
            url=f"{REPO}/blob/{COMMIT}/{path}",
        )
    return cache[path]


def namespace_at(lines, first):
    stack = []
    for line in lines[:first - 1]:
        ns = re.match(r"^namespace\s+(\S+)", line)
        sec = re.match(r"^(?:noncomputable\s+)?section(?:\s|$)", line)
        end = re.match(r"^end(?:\s|$)", line)
        if ns:
            stack.append(("namespace", ns.group(1)))
        elif sec:
            stack.append(("section", ""))
        elif end:
            assert stack, ("unmatched end", first, line)
            stack.pop()
    return ".".join(value for kind, value in stack if kind == "namespace")


def ref(path, name, role="proof"):
    _, lines = source(path)
    pat = re.compile(
        r"^(?:private\s+)?(?:noncomputable\s+)?"
        r"(?:theorem|lemma|def|structure|abbrev|class|instance|inductive)\s+"
        + re.escape(name) + r"(?=[\s{(:])"
    )
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits) == 1, (path, name, hits)
    first = hits[0] + 1
    last = next((i for i in range(first, len(lines)) if TOP.match(lines[i])), len(lines))
    while last > first and not lines[last - 1].strip():
        last -= 1
    namespace = namespace_at(lines, first)
    qualified = (
        name.removeprefix("_root_.") if name.startswith("_root_.")
        else (namespace + "." if namespace else "") + name
    )
    excerpt = "".join(lines[first - 1:last]).encode("utf-8")
    return dict(
        path=path, declaration=qualified, source_spelling=name,
        line_start=first, line_end=last, role=role,
        sha256=files[path]["sha256"], full_file_sha256=files[path]["sha256"], range_sha256=hashlib.sha256(excerpt).hexdigest(),
        range_bytes=len(excerpt), first_line=lines[first - 1].rstrip("\r\n"),
        declaration_lines_within_range=[first],
        url=f"{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}",
    )


def group(base, file, names, role="proof"):
    return [ref(base + file + ".lean", n, role) for n in names]


def gb(file, names, role="proof"):
    return group(GB, file, names, role)

def gl(file, names, role="proof"):
    return group(GL, file, names, role)

def pr(file, names, role="proof"):
    return group(PR, file, names, role)

def fm(file, names, role="proof"):
    return group(FM, file, names, role)

def gw(file, names, role="proof"):
    return group(GW, file, names, role)


claims = []
BASE = [
    "All coefficient rings in the application are DVR domains with compatible fraction-field embeddings. The source unramified ring W, its field Q, Frobenius and lattice edges stay fixed.",
    "BC1 uses the literal p>=5, f>=2 and Even f. Its field/Witt-vector existence and Teichmuller expansions are declared classical background; the required finite, quadratic, square-root and residue properties are proved in the report.",
    "BC2 proves the complete-DVR integral-closure and chosen-place construction, using only standard characteristic-zero separability, trace linear algebra and number-field integer-ring facts.",
    "CB1-CB2 and CB7 are prior proved integral tableau-basis/change-of-basis results; no integral semisimplicity premise is introduced.",
    "The full globally compatible family is not constructed here. The pointwise StdSubAt conclusion applies to recC data or supplied RingCompatibleAt identifications. Eventual compatible ring data can come from IsRecCEv or directly from GroupCompatibilityFamily; neither route is required simultaneously with the other.",
]


def claim(cid, title, statement, sources, dependencies=(), status="faithful_translation", note="", extra=()):
    claims.append(dict(
        id=cid, title=title, status=status, statement=statement,
        depends_on=list(dependencies), assumptions=BASE + list(extra),
        proof_location=dict(file="main.tex", anchors=[cid]),
        expanded_notes=dict(file="report.txt", section=cid),
        source_relation=note,
        mathematical_status="proved_relative_to_declared_classical_background_and_named_proved_companion_results",
        sources=sources,
    ))


claim(
    "BC1", "Construct the literal standard coefficient ring and all its quadratic-setting properties",
    "For p>=5 prime and even f>=2, O_s=W(F_(p^(2f)))[omega]/(omega^2-p) is the complete DVR with uniformizer omega, residue cardinal p^(2f), a finite rank-four structural map from W(F_(p^f)), compatible Frobenius period f, and a square root of every integer. This is the actual settingStd record.",
    pr("ExistsSqEqIntCast", ["F1", "F2", "WQ", "W2", "jW", "card_wittVector_quot_p_eq_card_field", "card_quot_WQ", "card_quotient_extRing", "frob_WQ", "frob_iter_WQ", "sig", "sig_alg", "sig_pow_alg", "sig_period", "jW_natCast", "jW_coeff", "jW_injective", "isAdicComplete_span_p_wittVector", "jW_finite", "isSquare_algebraMap", "sq_lift", "exists_sq_eq_intCast_of_not_dvd_of_ne_two"])
    + pr("JOInjective", ["QQ", "OO", "KO", "wU", "jO", "jO_injective", "inj_WK", "iota", "wU_sq", "sq_OO", "settingStd", "setting"])
    + pr("AlgebraMapFinite", ["toRes", "toRes_surjective", "mem_span_om", "ker_toRes", "resEquiv", "card_res", "algebraMap_finite", "algebraMap_injective"])
    + group("src/Formalism/LocalRingCardinality/SpanPowerMembership/", "GatRing", ["om_sq", "isUnit_of_re", "fact", "isDomain", "om_irreducible", "isDVR", "isAdicComplete"], "quadratic_DVR_counterpart")
    + gb("UnramifiedQuadraticSetting", ["HidaSetting", "UnramifiedQuadraticSetting"], "literal_interface"),
    status="derived_simplification",
    note="Residue-basis lifting proves rank two for W2/W, and the opposite-parity valuation gives the quadratic DVR directly. The source name does not mean O_s/W is unramified: its ramification and residue degrees are both two.",
)

claim(
    "BC2", "Finite complete-DVR normalization and an embedding inducing the selected finite place",
    "A finite extension of the fraction field of a complete characteristic-zero DVR has finite free complete-DVR integral closure. For each number-field prime over p, some embedding tau into an algebraic closure of K_s induces exactly that prime; E_tau=K_s tau(L), S_tau and embRec satisfy tau(x) integral iff v(x)>=0.",
    pr("IsLocalRingOfComplete", ["precomplete_equiv", "complete_of_pow", "isPrecomplete_fin_pi", "isLocalRing_of_complete", "algL_injective", "alg_injective", "dedekind", "finite", "frac", "free", "map_ne_bot", "complete_map", "isLocalRing", "not_isField", "isDVR", "complete"], "finite_normalization_counterpart")
    + pr("CharZeroWittQuadratic", ["charZero_witt_quadratic", "instCharZeroOO", "instCharZeroKO", "completeOO", "OL", "instDvrOL", "extOf", "settingOL", "Om", "Lt", "range_le_simple", "instFinLt", "embL", "embL_val", "Ot", "extOt", "embL_integral", "embO", "embO_val", "placeIdeal", "wU_mem_max", "under_max", "p_mem_max", "p_mem_placeIdeal", "placeOf", "isUnit_embO", "induces"])
    + pr("ExtWEx", ["dvd_of_mem", "p_inv_not_integral", "inv_integral", "exists_emb", "exists_ringAt", "tauAt", "placeOf_tauAt", "induces_tauAt"])
    + pr("ExtWRec", ["val_nonneg_iff", "resChar_mem", "tauRec", "KfRec", "ORec", "embRec", "extRec", "embRec_int"], "actual_place_objects")
    + gl("LevelGatherings/StdSubPlacesConst", ["ExtOf"], "actual_finite_extension_record"),
    dependencies=["BC1"], status="derived_simplification",
    note="The report supplies trace-dual finiteness and an elementary idempotent-lifting/DVR proof rather than merely invoking IntCl records. CRT replaces prime avoidance in the norm contradiction without changing the selected-place conclusion.",
)

claim(
    "BC3", "Faithful descent and exact finite-free lattice, dual, intersection and valuation transport",
    "For a finite compatible inclusion R->S of DVRs, S has an R-basis beginning with 1. All R-defined submodules in a K-space extend coordinatewise, so arbitrary intersections, kernels and lattice duals commute, inclusions descend, and saturation/ranks are preserved. Integer valuations and module lengths scale by the ramification index; p-normalized valuations and lengths do not change.",
    pr("IsLocalRingOfComplete", ["algL_injective", "alg_injective", "finite", "free", "frac"], "finite_free_source_counterpart")
    + fm("NablaLTwEqMap", ["BC", "BC.mem", "bc_span", "muS", "vecS", "map_smulK", "bc_map"], "source_coefficient_and_span_maps")
    + fm("LPBase", ["muV", "muV_coe", "bc_comap", "deltaS", "deltaS_apply", "dual_mem", "scale_mem"], "source_subspace_dual_and_scaling_counterparts")
    + gb("UnramifiedQuadraticSetting", ["scale", "Nsrc", "Ntgt"], "actual_intersections")
    + pr("ExtWRec", ["val_nonneg_iff", "resChar_mem", "embRec_int"], "actual_place_normalization_dictionary"),
    dependencies=["BC2"], status="derived_simplification",
    note="The source needs only forward lattice membership. The report explicitly proves the stronger arbitrary-intersection and descent statements by finite freeness, not by flatness alone. Duals are field-valued algebraic duals, not trace duals; no different is omitted.",
    extra=["The formulas using normalized p-valuations concern the mixed-characteristic setting with p nonzero and nonunit; zero is treated by the usual value +infinity."],
)

claim(
    "BC4", "The literal integral dual-Weyl lattice, its determinant twist and exact base change",
    "The already proved universal monic tableau basis identifies S tensor nabla_mu(R) with the literal target dualWeyl module. For Lambda=gR^k, the actual H0 is det(g)^(-lambda_k) T(g^-1)nabla_(lambda-lambda_k)(R); it is independent of the chosen lattice basis and commutes exactly with coefficient extension and disjoint-block tensors.",
    gw("StatementA", ["colAddGen", "dualWeyl", "rowAct"], "literal_generic_invariant_module")
    + gw("StatementD", ["blockEmb", "tensorLat", "TensorBasis", "blockAct", "nablaLTw", "NablaLTwMem"], "literal_twisted_and_tensor_models")
    + gw("FinalD", ["sSBasis", "rowActMul", "nablaLBasis", "nablaLKBasis", "nablaLTwMem"], "prior_CB_source_endpoints")
    + fm("NablaLTwEqMap", ["bc_dualWeyl", "map_map_alg", "det_map", "inv_map", "psiL", "psiL_apply", "nablaLTw_eq_map", "bc_map", "bc_nablaLTw", "map_blockEmb", "bc_tensorLat", "bc_colSpan", "base_change_H0"])
    + gb("LatticeSystems", ["H0IndepOfBasis", "H0_eq_twisted_nabla", "la_basis", "la_factor", "la_indep"], "basis_independence_counterparts")
    + gb("UnramifiedQuadraticSetting", ["H0", "nuOf", "Hten", "Vsp"], "actual_model_definitions"),
    dependencies=["CB1", "CB2", "CB7"],
    note="CB1-CB2 were independently confirmed to apply over every domain with universal polynomial invariance. The row-action order T(g)T(h)=T(hg), the inverse basis change, and the signed determinant power are all retained.",
)

claim(
    "BC5", "Exact actual tensor, edge, source-clean and dual-clean base change",
    "For the actual signed weights and W-lattice edges, coefficient and dual maps identify H(L), H(e), omega^(-A_r)H(e), its normalized algebraic dual, and the full Nsrc/Ntgt intersections after finite extension. The normalized pairing satisfies b'(nu F,delta G)=phi_K(b(F,G)), with unchanged p^A_r and all alternative-edge omega^c* divisibilities.",
    gb("UnramifiedQuadraticSetting", ["colSpan", "IsLattice", "twistVec", "extO", "IsDominant", "lamAt", "H0", "Hten", "Vsp", "dimV", "toV", "HL", "Edge", "IsEdge", "IsEdgeBasis", "LeAt", "HLe", "Ar", "scale", "Re", "Re'", "be", "Nsrc", "Ntgt"], "literal_lattices_and_normalizations")
    + fm("LPBase", ["muV", "bc_comap", "span_muV_top", "deltaS", "deltaS_apply", "dual_mem", "scale_mem", "bc_extO", "bc_LeAt", "bc_Hten", "Hten_le_V", "bc_Vsp", "be_sum", "lpAt_dom"])
    + gb("LatticeSystems", ["je_extO_lat", "je_LeAt_lat", "jm_HL_basis", "jr_dim"], "actual_full_lattice_and_dimension_counterparts"),
    dependencies=["BC3", "BC4"], status="derived_simplification",
    note="The source proves only the memberships needed in lpAt_dom. Exact clean-lattice equality is a new finite-free refinement, proved by coordinates. The W-edge quotient and q=p^f are fixed even if the coefficient residue field grows.",
)

claim(
    "BC6", "GoodRankK extends without loss, and fixed-family descent follows from fractional Smith form",
    "Map the original GoodRankK matrix entrywise and extend the images of its dual test vectors linearly over S. The resulting literal target certificate has the same n and D. For fixed linear tests on the exact scalar extension of a finite-free lattice, GoodRankK is also equivalent to having at least n fractional Smith exponents <=D ord(p), and therefore descends under finite extension.",
    gb("UnramifiedQuadraticSetting", ["GoodRankK", "be", "Ntgt"], "exact_matrix_rank_interface")
    + fm("LPBase", ["deltaS", "deltaS_apply", "dual_mem", "be_sum", "lpAt_dom"], "explicit_source_matrix_calculation"),
    dependencies=["BC3", "BC5"], status="derived_simplification",
    note="The forward proof is the literal source calculation and does not infer primitive partners from field rank. The optional descent criterion is proved separately, allows negative fractional Smith exponents, and concerns a FIXED scalar-extended family of tests; arbitrary newly chosen source vectors are not asserted to descend.",
)

claim(
    "BC7", "The actual LPBaseChange theorem with identical numerical parameters",
    "For every compatible finite coefficient extension and both literal HidaSetting records, LPprime_O(t,D,kappa,c*) implies LPprime_S(t,D,kappa,c*) for all weights and lattice targets. The source edge list, rank n and the inequalities n>=(1-kappa)dim V and 4(D+1)<=c* are unchanged, including the empty non-dominant branch.",
    gb("UnramifiedQuadraticSetting", ["HidaSetting", "IsDominant", "Vsp", "dimV", "GoodRankK", "LPprimeAt", "LPprime", "LPBaseChange"], "exact_source_statement")
    + fm("LPBase", ["Vsp_bot", "lpAt_nondom", "lpAt_dom", "lpBaseChange"])
    + gl("AdmissibleFamilyNoKernel", ["family_satisfies_ties", "linkG_fam_noKer"], "actual_family_consumers")
    + gb("Joints", ["linear_programming_input_of_hypotheses"], "parent_assembly_consumer"),
    dependencies=["BC5", "BC6"],
    note="The proof maps omega^a and p^D literally. It neither treats the image of omega as a new uniformizer nor multiplies t,D,c* by the ramification index. The finite-map hypothesis is unused in the source's core forward lpAt_dom proof; it remains in the exact exported interface and is used for our stronger equality/descent claims.",
)

claim(
    "BC8", "Supply literal StdSubAt on the actual recC rings, with the exact eventual-family boundary",
    "BC1-BC2's standard ring and finite prescribed-place extension give the displayed compatible iota/j/omega maps. Literal locPackC/recC uses those exact rings and maps, so StdSubAt holds pointwise. Compatible RingCompatibleAt isomorphisms and supplied IsRecCEv identifications transport this conclusion to the actual family without a new local subring premise.",
    gb("Joints", ["StdSubAt"], "exact_global_family_interface")
    + gl("LevelGatherings/StdSubPlacesConst", ["ExtOf", "setting_ext", "stdSub_placesConst"])
    + gl("LevelGatherings/StdSub", ["settingStd_iso", "stdSub_of_iso"])
    + gl("StdSubAtOfRing", ["ExtOf.map", "RingCompatibleAt", "stdSubAt_of_ring", "GroupCompatibilityAll", "GroupCompatibilityFamily"])
    + gl("TiedFamilies/LocPackC", ["nFr", "nFr_spec", "locPackC"])
    + gl("TiedFamilies/FullTiedCBase", ["packC", "recC", "ringTied_recC", "groupCompatibilityOfRecursion"])
    + gl("TiedFamilies/GTiedFOfIsRecCEv", ["IsRecC", "gTiedAll_of_isRecC", "IsRecCEv", "IsRecCF"], "explicit_supplied_family_boundary")
    + gl("LinkGConcreteNoKer", ["stdSubF_of_tied", "linkG_concrete", "linkG_concrete_noKer"], "actual_eventual_supplier_and_consumers")
    + gl("AdmissibleFamilyNoKernel", ["Fam", "family_satisfies_ties", "linkG_fam_noKer"], "actual_global_assembly_usage")
    + group("src/Formalism/LocalRingCardinality/", "RhoDetPrimeEqMuTildeMulChiPow", ["GIdx"], "actual_prime_and_even_order_input"),
    dependencies=["BC1", "BC2"], status="derived_simplification",
    note="The recC coefficient ring is deliberately constructed to contain the doubled residue-field standard subring. The proof does not infer such a subring in an arbitrary Hida DVR. IsRecCEv is one sufficient identification, not a necessary route: the ring field of an actual GroupCompatibilityFamily also supplies the literal RingCompatibleAt identifications directly. Only these coefficient-ring data are consumed; global levels, characters, rank/metric comparison data and their simultaneous existence remain outside this component.",
    extra=["For the eventual conclusion, literal compatible ring identifications must be supplied. IsRecCEv or the ring field of GroupCompatibilityFamily is sufficient; these are alternative interfaces, not simultaneous requirements. The complete construction of that global family is not asserted here."],
)

reviews_path = OUT / "independent_reviews.json"
reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else []
unique_ranges = {(s["path"], s["line_start"], s["line_end"]) for c in claims for s in c["sources"]}
artifact_paths = [OUT / "main.tex", OUT / "report.txt", Path(__file__).resolve()]
if reviews_path.exists(): artifact_paths.append(reviews_path)
artifact_files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifact_paths}
out = dict(
    schema_version="1.2", artifact_version="0.11", date="2026-11-21", owner="/root/lean_audit",
    repository=dict(url=REPO, commit=COMMIT),
    range_convention="One-indexed inclusive declaration ranges; exact source bytes are compared with the pinned Git blob and hashed without normalization.",
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True, range_bytes_hashed_without_normalization=True,
                      human_mathematical_proofs_supplied=True, lean_source_files_edited=False, local_lean_compilation=False,
                      lean_kernel_replay=False, replacement_arguments_formalized=False),
    status_definitions=dict(
        faithful_translation="A complete human proof of the exact source assertion, with named already-proved companion results.",
        derived_simplification="A proved shorter argument or explicitly identified strengthening, with exact source counterparts and unchanged application parameters.",
        remaining_input="A genuinely unexpanded input; no BC local construction or transport theorem has this status. The general global-family existence boundary is explicit below."),
    independent_reviews=reviews, claims=claims, files=[files[p] for p in sorted(files)],
    artifact_sha256=artifact_files,
    prior_components_reused=[
        dict(ids=["CB1", "CB2", "CB7"], component="v0_6/complementary_basis", role="Literal universal monic integral dual-Weyl/tableau basis and matrix/determinant twist over every domain."),
    ],
    same_iteration_companions=[
        dict(role="The parent family_join component consumes BC7 as LPBaseChange and BC8 as StdSubAt under supplied actual-family compatibility.", ids=[]),
    ],
    boundary_resolved=[
        dict(interface="LPBaseChange", discharged_by=["BC3", "BC4", "BC5", "BC6", "BC7"], scope="Exact finite coefficient extension of the literal LPprime certificate, with unchanged t,D,kappa,c*."),
        dict(interface="StdSubAt", discharged_by=["BC1", "BC2", "BC8"], scope="Pointwise on literal recC and under compatible isomorphisms; eventual under supplied compatible ring data. IsRecCEv and GroupCompatibilityFamily's ring field are alternative sufficient interfaces. Global existence of the fully compatible family remains separate."),
    ],
    scope_precision=[
        "StdSubAt is a standard coefficient-subring existence record, not an arbitrary standard-invariant-submodule theorem.",
        "The source unramified ring W and its residue cardinal q remain fixed; only the coefficient ring is extended.",
        "The mapped square root of p need not be a target uniformizer. Integral valuations and lengths scale by e; p-normalized quantities are invariant.",
        "Finite freeness justifies arbitrary clean-lattice intersections. The original forward LPBase proof requires only termwise inclusion and does not make a general flatness/intersection claim.",
        "Algebraic duals use K'-valued evaluation, not trace duals. There is no missing different or discriminant factor.",
        "The optional GoodRankK descent criterion treats a fixed family of scalar-extended tests and allows negative Smith exponents. It does not descend arbitrary new vector choices.",
        "The standard-subring supply is intrinsic to recC's construction, not to every abstract HidaSetting. IsRecCEv is an optional sufficient identification; the class-based GroupCompatibilityFamily route instead supplies its ring field directly. All globally compatible-family existence remains explicit.",
        "HM12's RS-isomorphism proof and BC's finite coefficient-extension proof are separate results.",
    ],
    retained_inputs=[
        "A well-formed recC datum, or the actual family's supplied RingCompatibleAt identifications. IsRecCEv or GroupCompatibilityFamily's ring field is sufficient. The local subring property is then proved, but the global family is not constructed in this component.",
        "The local LPprime certificate to extend; the companion Type-I/II and family-join arguments supply it with their literal hypotheses.",
        "All separately listed global orbit abundance, simultaneous arithmetic choices, theta/spectral/metric and cohomological-window inputs remain outside this component.",
    ],
    independent_review_targets=["BC2 finite normalization and prescribed-place norm argument", "BC3-BC5 finite-free intersections, duals and exact model normalizations", "BC6-BC8 fractional Smith criterion, LP parameters and actual-family boundary"],
)
(OUT / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n")
(OUT / "source_manifest.json").write_text(json.dumps(dict(repository=out["repository"], files=out["files"]), ensure_ascii=False, indent=2)+"\n")
locators=[]
for c in claims:
    locators += [c["id"]+": "+c["title"], "Status: "+c["status"]]
    for s in c["sources"]:
        locators += ["  "+s["declaration"], "  "+s["url"], "  full-file SHA256 "+s["sha256"], "  inclusive-range SHA256 "+s["range_sha256"]]
    locators.append("")
(OUT / "source_locators.txt").write_text("\n".join(locators))
print(json.dumps(dict(claims=len(claims), source_files=len(files), source_references=sum(len(c["sources"]) for c in claims), unique_ranges=len(unique_ranges))))
