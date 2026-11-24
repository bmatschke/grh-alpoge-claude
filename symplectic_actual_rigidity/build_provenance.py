#!/usr/bin/env python3
"""Bind the RX rigidity chain to its pinned interfaces and complete human proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=WORK.parent / "lean-source")
REPO = parser.parse_args().repo
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMP = "symplectic_actual_rigidity"
AV = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
PT = "src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/"
DC = "ModularityArgument/ThresholdArguments/DenseThresholdCases/"
cache = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def path_of(file):
    if file.startswith("src/"):
        return file + ".lean"
    if file.startswith("PT/"):
        return PT + file[3:] + ".lean"
    if file.startswith("DC/"):
        return AV + DC + file[3:] + ".lean"
    return AV + file + ".lean"


def source(file, spelling, role):
    path = path_of(file)
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pattern = (r"^(?:(?:private|protected|noncomputable)\s+)*"
               r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)")
    starts = [(i, m.group(1)) for i, line in enumerate(lines, 1)
              if (m := re.match(pattern, line.decode()))]
    matches = [(i, n) for i, n in starts if n == spelling or n.endswith("." + spelling)]
    assert len(matches) == 1, (path, spelling, matches)
    start, name = matches[0]
    end = min([i for i, _ in starts if i > start] or [len(lines) + 1]) - 1
    while not lines[end - 1].strip():
        end -= 1
    block = b"".join(lines[start - 1:end])
    if path not in cache:
        pinned = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
        assert raw == pinned, "Pinned blob mismatch: " + path
        cache[path] = dict(path=path, sha256=sha(raw), bytes=len(raw), lines=len(lines),
                           verified_equal_to_pinned_git_blob=True)
    return dict(path=path, declaration=name, source_spelling=spelling,
                line_start=start, line_end=end, sha256=sha(raw),
                range_sha256=sha(block), range_bytes=len(block),
                first_line=lines[start - 1].decode().rstrip("\n"),
                url=f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
                role=role, verified_equal_to_pinned_git_blob=True)


specs = {
    "RX1": [
        ("CommutativeAlgebra/ResMapBijective", "IsCO", "Actual complete Noetherian local coefficient-algebra hypotheses"),
        ("SymplecticGSp4/CopNormLt", "cop_norm_lt", "Strict maximal-ideal image estimate"),
        ("SymplecticGSp4/CopNormLt", "cop_geom", "Geometric decay on ideal powers"),
        ("SymplecticGSp4/CopNormLt", "cop_bdd", "Finite coefficient capture for the algebra map"),
        ("SymplecticGSp4/CopNormLt", "cop_snd", "Derivative coordinate continuity"),
        ("SymplecticGSp4/CopNormLt", "cop_main", "Simultaneous finite field and derivative bound"),
        ("SymplecticGSp4/CopNormLt", "coPt", "Literal coefficient/dual-number point supplier"),
        ("SymplecticGSp4/DecompSigmaOrd", "PtIn", "Original actual point witness and coefficient map"),
        ("SymplecticGSp4/DecompSigmaOrd", "IsPt", "Original multiplier, UnrT and component conditions"),
        ("SymplecticGSp4/DecompSigmaOrd", "UnrT", "Finite ramification follows from actual inertia equation"),
        ("SymplecticGSp4/EptInt", "eptInt", "Continuity and original finite coefficient point comparison"),
        ("SymplecticGSp4/TbTriDiag", "tb_coc", "Exact right-inverse tangent cocycle convention"),
        ("SymplecticGSp4/TbTriDiag", "tb_sp", "Fixed multiplier makes the cocycle symplectic"),
        ("SymplecticGSp4/TbTriDiag", "tb_cont", "Actual tangent-coordinate continuity"),
        ("SymplecticGSp4/TbTriDiag", "tb_desc", "One finite subfield containing both coordinates"),
    ],
    "RX2": [
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "ch_step", "Character-filtration induction"),
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "ch_step2", "Finite-extension character quotient step"),
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "h0dual_bot", "No cyclotomic constituent implies dual invariant vanishing"),
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "filt_tri", "Underlying coefficient character filtration"),
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "key", "Ordinary crystalline induction, specialized here to E and E[epsilon]"),
        ("PadicHodgeTheory/SnocZeroLastCoordinateLast", "prC", "Exact source conclusion used for the dual-number specialization; full arbitrary-Artin predicate not claimed"),
        ("PadicHodgeTheory/PrF", "prF", "Positive H1 equals finite H1 via dimension and dual invariants"),
        ("PadicHodgeTheory/TateRat", "tate_Q", "Finite lattice Euler growth and rationalization"),
        ("PadicHodgeTheory/TateRat", "tateRat", "Correct local-degree factor and original coefficient restriction"),
        ("PadicHodgeTheory/DeformCr", "extRep", "Actual extension representation of the cocycle"),
        ("PadicHodgeTheory/DeformCr", "deformCr", "Crystalline self-extension implies finite adjoint cocycle"),
        ("PadicHodgeTheory/Z1fDescAvg", "z1fDesc_avg", "Explicit finite-quotient primitive averaging sign"),
        ("PadicHodgeTheory/Z1fDescAvg", "z1fDesc", "Descent from an open subgroup, with no prime-to-ell restriction"),
        ("PadicHodgeTheory/CrystallineTransferSurjection", "pr6", "Source ordinary dual-number to finite-cocycle consumer"),
    ],
    "RX3": [
        ("SymplecticGSp4/MapRepApply", "Ord", "Original unnormalized spectral and inertia equations"),
        ("SymplecticGSp4/OrdLocal", "ordLocal", "Spectral projectors over actual E[epsilon]"),
        ("SymplecticGSp4/DecompSigmaOrd", "condL", "Original local ordinary condition"),
        ("SymplecticGSp4/DecompSigmaOrd", "condP", "Exact inertia intersection killed at Sb"),
        ("SymplecticGSp4/TbTriDiag", "tb_chars", "Continuous characters of the actual triangular matrices"),
        ("SymplecticGSp4/TbTriDiag", "tb_uniq", "Ordered diagonal character identity after reduction"),
        ("SymplecticGSp4/TbTriDiag", "tb_sub", "Open normal subgroup retaining the specified sigma"),
        ("SymplecticGSp4/TbTriDiag", "tb_loc", "Exact ordinary finite-cocycle local conclusion"),
        ("SymplecticGSp4/TbTriDiag", "tb_place", "Every original away-from-ell placement"),
        ("SymplecticGSp4/TbTriDiag", "tb_atL", "Original decomposition group, inertia and cyclotomic match"),
        ("SymplecticGSp4/TbTriDiag", "tanBK", "Full literal outgoing three-conjunct target"),
        ("PadicHodgeTheory/SplAdjUnit", "spPtL", "Incoming AX8 noncriticality on every open subgroup containing sigma"),
        ("PadicHodgeTheory/DecEmb", "decEmb", "Original henselization/completion/decomposition comparison"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "decJ", "Exact original graph subgroup in the above-ell condition"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "IsBK", "All local primitive clauses on original groups"),
    ],
    "RX4": [
        ("SymplecticGSp4/MapRepApply", "Irr", "Source full matrix-span irreducibility implies absolute irreducibility"),
        ("SymplecticGSp4/DecompSigmaOrd", "Good", "Odd ell, positive ordered weights, finite characters and original s0/sigma"),
        ("PadicHodgeTheory/SplAdjUnit", "spPtL", "Actual ordered local characters with exact inertia weights"),
        ("SymplecticGSp4/LMemMax", "facts", "Incoming AX6 finite kernel and original cyclotomic/inertia identities"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "IsIrr", "Exact irreducibility needed by the automorphy interface"),
        ("ModularityArgument/AutomorphyLifting/IsAutCsdA", "IsAutQA", "All original imaginary quadratics with irreducible restriction"),
        ("DC/ExistsCmFieldTwistH1", "exists_cm_field_twist_h1", "Source auxiliary-CM/adjoint supplier replaced by RX4--RX5; larger hypothesis packages not promoted"),
    ],
    "RX5": [
        ("DC/IsAut4", "IsAut4Alt", "Literal IsAutQA, unchanged"),
        ("ModularityArgument/AutomorphyLifting/IsAutCsdA", "IsAutQA", "Actual regular-algebraic cuspidal AttC witness; WitA unused"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "FrobEig", "Geometric Frobenius is the inverse of the source arithmetic Frobenius"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "algSat", "Exact q^((n-1)/2) normalization"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "AttachedSys", "Actual semisimplicity and cofinite unramified parameter matching"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "AttC", "Literal cuspidal attachment"),
        ("AutomorphicForms/CongruenceNumberRankThree", "DualTw", "Self-dual multiplier convention"),
        ("AutomorphicForms/CongruenceNumberRankThree", "IsAdOf", "Exact conjugate pairing and negative-transpose action at complex conjugation"),
        ("DC/UnderCPl", "polarization_k_of_printed_results", "Original normalized theta*cyc^(n-1) and quadratic infinity-sign correction"),
        ("BuildingsResidueChars/HeckeCharSignFixed", "heckeChar_sign_fixed", "Norm pullback and restricted-avatar preservation under the sign correction"),
        ("PT/GaloisRepOfPolarizedCuspidal", "algNorm", "The normalized local Langlands determinant twist"),
        ("PT/GaloisRepOfPolarizedCuspidal", "IsGalRepOf", "Classical attachment interface, used only in the needed normalized subcase"),
        ("PT/GaloisRepOfPolarizedCuspidal", "GaloisRepOfPolarizedCuspidal", "Matched primary published Galois attachment theorem; full record not separately promoted by RX"),
        ("DC/RigSp4", "rg_twist", "Direct sum of projected adjoint and quadratic complement"),
        ("DC/RigSp4", "rg_sign", "Actual quadratic character and original complex conjugation"),
        ("DC/RigSp4", "rgJ", "Original alternating matrix"),
        ("DC/RigSp4", "rg_adjConj", "Symplectic adjoint commutes with similitude conjugation"),
        ("DC/RigSp4", "rg_pair", "Exact B=J*r(c)^(-1) pairing identity"),
        ("AutomorphicForms/BlochKatoSelmerVanishes", "BlochKatoSelmerVanishes", "Original continuous algebraic-closure cocycle and actual-coboundary scope"),
    ],
    "RX6": [
        ("SymplecticGSp4/DecompSigmaOrd", "RigidAt", "Every actual dual-number point and entrywise fixed symplectic commutator"),
        ("DC/RigEnd3", "RigiditySymplecticFour", "Complete universally quantified outgoing endpoint"),
        ("WeakShimuraTheory/NearSplit", "Ctx2", "Original Case-II context contains Good"),
        ("WeakShimuraTheory/NearSplit", "Ctx3", "Original Case-III context contains Good"),
        ("DC/RigSp4", "rgP", "P=(1-adj)/2 with the exact sign"),
        ("DC/RigSp4", "rgP_mem", "Image in actual sp4"),
        ("DC/RigSp4", "rgP_of_mem", "Identity on actual symplectic cocycles"),
        ("DC/RigSp4", "rg_bk", "Projection of every inertia and period primitive"),
        ("DC/RigSp4", "rg_alg", "Negative projected matrix gives the exact RigidAt commutator"),
        ("DC/RigSp4", "rigSp4_alt", "Original full producer; RX supplies the same target by a shorter classical route"),
    ],
    "RX7": [
        ("SymplecticGSp4/DecompSigmaOrd", "AllIrr", "Pointwise original-D quantifier order"),
        ("DC/IsAut4", "SymplecticFourImageDense", "Same D, one iota, all original irreducible points; original host/threshold hypotheses retained"),
        ("DC/ConductorAtMapInjectiveCoeff", "main_big", "Actual paired-count consumer of automorphy and rigidity on one D"),
        ("DC/ConductorAtMapInjectiveCoeff", "sp4Main_alt", "Original paired-count chain retains separate catalogue and other suppliers"),
    ],
}

titles = {
    "RX1": "Finite coefficients, continuity and the actual symplectic tangent cocycle",
    "RX2": "Ordinary crystalline induction and finite-index primitive descent",
    "RX3": "Full original tanBK conclusion on every actual good datum",
    "RX4": "Cyclotomic irreducibility and an auxiliary CM field inside the original closure",
    "RX5": "Exact automorphic polarization and polarized-adjoint Selmer vanishing",
    "RX6": "Complete literal RigiditySymplecticFour",
    "RX7": "Same-datum AllIrr RigidAt installation from image density",
}
labels = {
    "RX1": "prop:rx-coefficients", "RX2": "prop:rx-ordinary-crystalline",
    "RX3": "prop:rx-tanbk", "RX4": "prop:rx-cyclotomic-irreducibility",
    "RX5": "prop:rx-adjoint-vanishing", "RX6": "thm:rx-literal-rigidity",
    "RX7": "cor:rx-same-datum",
}
deps = {
    "RX1": ["AX6"],
    "RX2": ["DX1", "BX1", "BX2", "BX3", "BX4"],
    "RX3": ["RX1", "RX2", "AX6", "AX8", "DX1", "BX1", "BX2"],
    "RX4": ["RX1", "AX3", "AX6", "AX8"],
    "RX5": ["RX1", "RX4", "AX3", "AX6", "BX1", "BX2", "RV4"],
    "RX6": ["RX3", "RX5"],
    "RX7": ["RX6"],
}
scopes = {
    "RX1": "Every actual point/dual-number point over the original complete Noetherian local O-algebra. Original maps and both coordinates captured in one finite extension, actual continuity, fixed-multiplier cocycle in sp4, and finite ramification.",
    "RX2": "Finite local extensions and A=E or E[epsilon], with exact strict inertia weights and no cyclotomic ratio among ordered reduced characters. Complete induction, higher-dimensional finite-to-rational Euler passage and cochain descent. Does not claim the source prC theorem for every general Artin algebra.",
    "RX3": "Full literal tanBK output on unchanged Good D and every allowed pair of actual points, using the original component and the open subgroup containing the prescribed sigma. All original placements and both away/above local conditions retained.",
    "RX4": "Every irreducible actual point on Good D; absolute irreducibility on ker cyclotomic and on G_{K(mu_ell^infty)} for a chosen imaginary quadratic K inside original Omega. Full infinite-profinite Clifford proof, with no residual-image or purity hypothesis.",
    "RX5": "For Good D and actual irreducible r satisfying literal IsAut4Alt, the exact polarized adjoint on original G_Q has zero actual Bloch--Kato Selmer group. The automorphy premise is retained. Full algebraic-closure cocycle scope is matched by matrix Baire capture and individual local-primitive return.",
    "RX6": "Literal universal RigiditySymplecticFour with every original Ctx2/Ctx3, positive level, character-killing, iota and actual-point premise. Proves the stronger Good+EPt+Irr+IsAut4Alt implication. Does not assert automorphy of arbitrary points.",
    "RX7": "For every original host h,t,ell,O,e,psi,D satisfying the literal image-density premises, one supplied iota gives AllIrr RigidAt on that same D. Image density remains the antecedent; no unguarded catalogue, count or RH/GRH closure is claimed.",
}
classical = {
    "RX1": [], "RX2": ["RX-FON"], "RX3": [], "RX4": [],
    "RX5": ["RX-SMO", "RX-GAL", "RX-CHEB", "RX-SV"],
    "RX6": [], "RX7": [],
}
hypotheses = {
    "RX1": ["D.Good", "original PtIn witness; for the cocycle an actual rprime reducing to r"],
    "RX2": ["finite L/Q_ell and E/Q_ell", "A=E or E[epsilon]", "continuous upper triangular representation", "strictly decreasing integer inertia weights", "bar(kappa_i) != bar(kappa_j)*chi for every i<j"],
    "RX3": ["D.Good", "D.EPt r", "D.PtIn dualnumbers rprime", "rprime reduces entrywise to r"],
    "RX4": ["D.Good", "D.EPt r", "Irr r"],
    "RX5": ["D.Good", "D.EPt r", "Irr r", "IsAut4Alt iota r, literally IsAutQA"],
    "RX6": ["All original premises of RigiditySymplecticFour, including IsAut4Alt"],
    "RX7": ["SymplecticFourImageDense", "h.Big t; ell odd; 0<e<t; psi in h.X", "original Good D and OfCase D h e psi"],
}
relations = {
    "RX1": "Complete elementary reconstruction of coPt and the actual tangent-cocycle suppliers.",
    "RX2": "Complete direct proof of precisely the ordinary crystalline specialization needed by tanBK, with actual coefficient and subgroup descent.",
    "RX3": "Full tanBK supplier, using reconstructed AX8 and matched BX local periods rather than assuming the larger local package.",
    "RX4": "Alternative full elementary restriction proof. The source obtains a suitable CM field through a longer tower route; this proof provides the needed field and the stronger cyclotomic irreducibility directly.",
    "RX5": "Alternative proof of the needed actual-point adjoint vanishing using Thorne2022 Theorem6.1 and explicit normalization. Source anchors bind the definitions and the replaced interface; they do not assert that the source's existing proof cites this theorem.",
    "RX6": "Complete proof of the exact outgoing RigiditySymplecticFour proposition. The broader UnramifiedInputs and AdjointLiftingTheorem are bypassed only for this endpoint and remain unpromoted.",
    "RX7": "Exact same-D substitution into AllIrr. Existing AX/MX/PX/SP statements are downstream consumers, not assumptions needed for the pointwise rigidity proof.",
}

external_components = {
    "AX3": "symplectic_arithmetic_data", "AX6": "symplectic_arithmetic_data",
    "AX8": "symplectic_arithmetic_data", "DX1": "symplectic_local_installation",
    "BX1": "bloch_kato_installation", "BX2": "bloch_kato_installation",
    "BX3": "bloch_kato_installation", "BX4": "bloch_kato_installation",
    "RV4": "rank_one_cohomology",
}
external = {}
for cid, component in external_components.items():
    ledger_raw = (WORK / component / "provenance.json").read_bytes()
    ledger = json.loads(ledger_raw)
    claim = next(x for x in ledger["claims"] if x["id"] == cid)
    pl = claim["proof_location"]
    incoming_raw = (WORK / component / "main.tex").read_bytes()
    incoming_lines = incoming_raw.splitlines(keepends=True)
    assert sha(b"".join(incoming_lines[pl["line_start"] - 1:pl["line_end"]])) == pl["sha256"], (cid, "incoming proof range mismatch")
    external[cid] = dict(component=component,
                         provenance_file=component + "/provenance.json",
                         provenance_sha256=sha(ledger_raw),
                         main_tex_sha256=sha((WORK / component / "main.tex").read_bytes()),
                         proof_location=claim["proof_location"])

raw = (HERE / "main.tex").read_bytes()
lines = raw.splitlines(keepends=True)
claims = []
for cid in titles:
    begin = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% BEGIN " + cid)
    start = next(i for i, line in enumerate(lines, 1) if i > begin and line.decode().startswith("\\begin{"))
    end = next(i for i, line in enumerate(lines, 1) if line.decode().strip() == "% END " + cid) - 1
    while not lines[end - 1].strip():
        end -= 1
    assert lines[end - 1].decode().strip() == r"\end{proof}"
    proof = b"".join(lines[start - 1:end])
    claims.append(dict(
        id=cid, title=titles[cid], introduced_in="0.28",
        status="Complete human proof in its stated scope with exact named classical inputs",
        mathematical_status="Actual supplier reconstruction and explicit alternative proof; no Lean replay",
        scope=scopes[cid], depends_on=deps[cid], classical_inputs=classical[cid],
        theorem_hypotheses=hypotheses[cid],
        remaining_bespoke_inputs=(["SymplecticFourImageDense"] if cid == "RX7" else []),
        proof_location=dict(file=COMP + "/main.tex", paragraph=cid, label=labels[cid],
                            line_start=start, line_end=end, sha256=sha(proof), bytes=len(proof)),
        sources=[source(*x) for x in specs[cid]], source_relation=relations[cid],
        component_ledger=COMP + "/provenance.json",
    ))

scope_sources = [
    source("DC/WsLink", "UnramifiedInputs", "Entire six-field record is bypassed, not supplied by RX"),
    source("DC/AutomorphicPointGalois", "AdjointLiftingTheorem", "Entire Hida-setting theorem is bypassed, not supplied by RX"),
    source("DC/AfDesc", "HypothesesH'", "Larger period/Hida/promodular suppliers are not promoted"),
    source("DC/AfStmt", "NumberSp4Alt", "Separate exact finite catalogue remains independent of RX"),
]

out = dict(
    schema="rh-human-reconstruction-provenance/1", artifact_version="0.28",
    date="2026-11-22", repository="https://github.com/CocoSgt/riemann-hypothesis-lean",
    commit=PIN, component=COMP, main_tex_sha256=sha(raw),
    scope="Full actual tanBK and literal RigiditySymplecticFour by a direct Thorne2022 route; same-D AllIrr RigidAt follows from the existing image-density antecedent. No enlarged Hida/unramified package or unconditional automorphy/count closure.",
    claims=claims, dependency_graph=deps, external_claim_dependencies=external,
    classical_input_registry=COMP + "/classical_inputs.json",
    scope_boundary_sources=scope_sources, source_files=list(cache.values()),
    downstream_consumer_claims=["AX10", "MX10", "PX10", "SP10"],
    validation=dict(claim_count=len(claims), claim_source_links=sum(len(c["sources"]) for c in claims),
                    scope_boundary_source_links=len(scope_sources),
                    source_files_checked_against_pinned_git_blobs=len(cache),
                    main_tex_sha256=sha(raw),
                    verification_kind="Exact proof/source byte ranges and pinned Git blob equality; no Lean replay"),
)
dump("provenance.json", out)
(HERE / "source_locators.txt").write_text("\n\n".join(
    c["id"] + " -- " + c["title"] + "\n" + "\n".join(
        s["declaration"] + "\n" + s["url"] + "\nfile " + s["sha256"] +
        "\nrange " + s["range_sha256"] for s in c["sources"]) for c in claims) + "\n")

classical_registry = [
    dict(id="RX-FON", name="Fontaine crystalline category, filtration and unramified descent",
         statement="Crystalline representations are stable under subquotients, tensor products and duals; Dcris is exact on admissible objects and DdR is strictly exact. Unramified finite-dimensional representations are crystalline, and chi^a has filtration degree -a.",
         source="J.-M. Fontaine, Representations p-adiques semi-stables, Asterisque223(1994),113--184",
         theorem="Proposition1.5.2; sections5.1.3--5.1.7", printed_pages="124,155--158", pdf_zero_based_pages=[12,43,44,45,46],
         url="https://www.numdam.org/item/AST_1994__223__113_0.pdf", used_by=["RX2"],
         primary_source_inspected=True, scope_match="Actual local rings and cyclotomic actions are identified by BX1--BX2; only finite local fields and E/E[epsilon] are used."),
    dict(id="RX-SMO", name="Strong multiplicity one for cuspidal GLn",
         statement="Cuspidal representations with identical unramified local parameters outside a finite set are isomorphic. This follows directly from the linear independence theorem for their prime-power traces.",
         source="H. Jacquet and J.A. Shalika, On Euler Products and the Classification of Automorphic Forms II, AJM103(1981),777--815",
         theorem="Theorem4.2", printed_pages="806--807", pdf_zero_based_pages=[30,31],
         url="https://www.math.columbia.edu/~hj/On%20Euler%20products%20II.pdf", used_by=["RX5"],
         primary_source_inspected=True, inspection="Original scanned pages806--807 read directly; nonunitary cuspidal representations are included by the theorem's positive-character normalization."),
    dict(id="RX-GAL", name="Normalized Galois attachment for polarized regular algebraic cuspidal representations",
         statement="A regular algebraic cuspidal polarized GLn representation over a CM field has a continuous semisimple attached ell-adic representation with normalized local compatibility away from ell and a totally odd polarization. Only these clauses are used.",
         source="Barnet-Lamb--Gee--Geraghty--Taylor, Potential automorphy and change of weight, Annals179(2014),501--609",
         theorem="Section2.1 and Theorem2.1.1(1),(2)", printed_pages="535--538", pdf_zero_based_pages=[34,35,36,37],
         url="https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf", used_by=["RX5"],
         primary_source_inspected=True, scope_match="Geometric Frobenius eigenvalues q^((n-1)/2) times Satake; Hecke avatar on G_K is theta*chi^(n-1). Infinity sign is corrected by the quadratic character without changing restriction to G_K."),
    dict(id="RX-CHEB", name="Chebotarev density",
         statement="Every conjugacy class in a finite Galois quotient occurs as Frobenius outside any given finite set. Thus cofinite Frobenius characteristic-polynomial agreement gives equality of continuous traces; the semisimple character criterion is proved in RX5.",
         source="J.S. Milne, Algebraic Number Theory, version3.08(2020)", theorem="Theorem8.31",
         printed_pages="147", pdf_zero_based_pages=[148], url="https://www.jmilne.org/math/CourseNotes/ANT.pdf",
         used_by=["RX5"], primary_source_inspected=True),
    dict(id="RX-SV", name="Thorne irreducible automorphic adjoint Selmer vanishing",
         statement="For CM F, n>=2 and regular algebraic cuspidal polarized pi, irreducibility of r_pi on G_{F(mu_ell^infty)} implies H1_f(Fplus,ad r_pi)=0, for the polarized unitary adjoint. No residual-image or enormousness hypothesis is imposed.",
         source="J.A. Thorne, On the vanishing of adjoint Bloch--Kato Selmer groups of irreducible automorphic Galois representations, PAMQ18(2022),no.5",
         theorem="Theorem6.1", printed_pages="Author preprint24; adjoint convention3,25", pdf_zero_based_pages=[23,2,24],
         url="https://arxiv.org/pdf/2207.04925", doi="10.4310/PAMQ.2022.v18.n5.a5",
         used_by=["RX5"], primary_source_inspected=True,
         scope_match="F=the original embedded imaginary quadratic K, Fplus=Q, n=4. RX4 proves the exact infinite cyclotomic irreducibility. RX5 identifies the negative-transpose polarized adjoint, and RX3/BX identify the local finite conditions."),
]
dump("classical_inputs.json", dict(schema="rh-classical-input-registry/1", artifact_version="0.28",
                                  component=COMP, inputs=classical_registry,
                                  inherited_inputs={"AX3": "Original finite abelian class-field theory/cyclotomic character and norm compatibility",
                                                    "DX1": "Finite local Tate duality and finite Euler formula",
                                                    "BX1--BX4": "Actual period models, compact/rational cohomology and local Bloch--Kato dimension formula",
                                                    "RV4": "Countable finite-field cover and Baire argument, with matrix generalization proved in RX5"}))
dump("input_registry.json", dict(schema="rh-component-inputs/1", artifact_version="0.28", component=COMP,
                                 incoming_claims=external, classical_input_registry=COMP + "/classical_inputs.json",
                                 theorem_hypotheses=hypotheses,
                                 principle="Original theorem premises remain premises. Proof of an implication is not unconditional arithmetic installation of its automorphy antecedent."))
dump("remaining_inputs.json", dict(schema="rh-component-remaining-inputs/1", artifact_version="0.28", component=COMP,
                                   endpoint="RigiditySymplecticFour",
                                   missing_suppliers_inside_endpoint_proof=[],
                                   endpoint_original_hypotheses=hypotheses["RX6"],
                                   actual_datum_installation_antecedent="SymplecticFourImageDense on the same original host and Good/OfCase D",
                                   independent_global_frontier=["SymplecticFourImageDense", "NumberSp4Alt and its exact guarded catalogue"],
                                   bypassed_not_promoted=["UnramifiedInputs", "HypothesesH'", "AdjointLiftingTheorem", "full Hida/promodular/unramified tower packages"],
                                   classical_inputs=[x["id"] for x in classical_registry],
                                   scope="The original IsAut4Alt antecedent remains in RX6. RX7 supplies actual AllIrr RigidAt only after the same-D image-density theorem supplies it. Other components may close the independent frontier separately."))
closure = dict(
    schema="rh-component-closure/1", artifact_version="0.28", component=COMP,
    main_tex_sha256=sha(raw), provenance_sha256=sha((HERE / "provenance.json").read_bytes()),
    claim_ids=list(titles), final_claims=["RX3", "RX6", "RX7"],
    literal_endpoints={"tanBK": "RX3", "RigiditySymplecticFour": "RX6",
                       "same_D_AllIrr_RigidAt_from_ImageDense": "RX7"},
    complete_chains=[
        {"path": ["RX1", "RX2", "RX3"], "conclusion": "Actual tangent cocycle satisfies every original finite local condition"},
        {"path": ["RX1", "AX8", "RX4", "RX5"], "conclusion": "Actual automorphic irreducible point has exact polarized-adjoint Selmer vanishing"},
        {"path": ["RX3", "RX5", "RX6"], "conclusion": "Every actual dual-number deformation is an exact symplectic commutator"},
        {"path": ["RX6", "RX7"], "conclusion": "Original common image-density embedding installs AllIrr RigidAt on unchanged D"},
    ],
    source_alternative="The direct Thorne2022 theorem replaces the source's broader Hida adjoint-lifting route only for this outgoing rigidity predicate.",
    retained_original_data=["Omega", "O", "D", "local places and inertia", "OnComp domain/base-point condition", "iota", "actual coefficient maps", "actual dual-number point"],
    no_remaining_bespoke_supplier_in_literal_RigiditySymplecticFour_proof=True,
    actual_same_D_installation_retains_ImageDense=True,
    not_claimed=["unconditional automorphy", "unconditional CountII or CountIII", "full source UnramifiedInputs or AdjointLiftingTheorem", "unconditional catalogue trace nonvanishing", "RH or GRH completion"],
    downstream_consumers=["AX10", "MX10", "PX10", "SP10"],
    no_lean_replay=True, no_pdf_requested_or_generated=True,
)
dump("closure.json", closure)
dump("next_targets.json", dict(schema="rh-next-targets/1", artifact_version="0.28", component=COMP,
                               completed=["literal tanBK", "literal RigiditySymplecticFour", "same-D actual rigidity once image density supplies automorphy"],
                               targets=[
                                   {"target": "SymplecticFourImageDense", "scope": "Exact same-D Fin0/NoEnd/common-iota automorphy supplier; owned by parallel image-density component"},
                                   {"target": "NumberSp4Alt", "scope": "Original uniform finite catalogue and trace guard; owned by parallel catalogue component"}],
                               avoid=["Reconstructing full Hida packages merely to duplicate the now-complete selected rigidity endpoint", "Replacing IsAut4Alt by an unnamed conditional vanishing package"]))
(HERE / "report.txt").write_text(
    "RX1--RX7: actual symplectic irreducible rigidity\n"
    "============================================\n"
    "Complete literal endpoints: tanBK (RX3), RigiditySymplecticFour (RX6), and same-D AllIrr RigidAt from the existing image-density premise (RX7).\n\n"
    "The source's long unramified Hida route is replaced by Thorne2022 Theorem6.1. The chapter proves its exact infinite cyclotomic irreducibility premise using a full profinite Clifford argument and the original ordinary characters. An imaginary quadratic field is chosen inside the original Omega by ramifying at an otherwise unramified auxiliary prime. Actual IsAutQA then supplies the cuspidal point. The normalized Hecke twist, infinity-sign correction, symmetric pairing and unitary adjoint are all checked.\n\n"
    "The local half is complete: original coefficient maps and derivatives are captured in one finite field; higher-dimensional finite-to-rational Euler control and the ordinary crystalline induction include unramified dual-number diagonal variations; finite-index descent is by an explicit averaged primitive. Every source placement and OnComp condition is retained. Matrix-cocycle Baire capture and local coefficient retractions give the full algebraic-closure cochain scope.\n\n"
    "Retained named classical leaves: Fontaine crystalline category/unramified descent; strong multiplicity one; normalized polarized Galois attachment; Chebotarev; Thorne adjoint Selmer vanishing. Incoming AX/BX/DX/RV claims and original theorem premises are recorded separately.\n\n"
    "The whole UnramifiedInputs, HypothesesHprime and AdjointLiftingTheorem records are deliberately not promoted. Actual image density and the exact catalogue remain independent frontier items; this chapter alone does not assert the counts or RH/GRH.\n\n"
    f"Pin: {PIN}\nMain SHA256: {sha(raw)}\n"
    f"Claims: {len(claims)}; claim source links: {out['validation']['claim_source_links']}; boundary source links: {len(scope_sources)}; pinned source files: {len(cache)}.\n"
    "Proof/source ranges are byte-bound and checked against pinned Git blobs. TeX is validated in draft mode. No Lean build and no proof PDF.\n")
dump("source_validation.json", dict(
    schema="rh-source-validation/1", artifact_version="0.28", component=COMP,
    result="PASS", commit=PIN,
    main_tex_sha256=sha(raw),
    provenance_sha256=sha((HERE / "provenance.json").read_bytes()),
    claim_ids=list(titles), human_proof_ranges_checked=len(claims),
    claim_source_ranges_checked=out["validation"]["claim_source_links"],
    scope_boundary_source_ranges_checked=len(scope_sources),
    distinct_source_files_checked_against_pinned_git_blobs=len(cache),
    incoming_human_proof_ranges_checked=len(external),
    checks=[
        "Every source file equals its exact pinned Git blob",
        "Every declaration spelling resolves uniquely at its recorded start line",
        "Every recorded source range has exact line, byte and SHA256 binding",
        "Every human claim range begins with its theorem and ends with its complete proof",
        "Every incoming stable claim has a matching actual proof-range SHA256",
        "All depends_on entries are stable claim IDs; classical leaves and theorem premises are separate",
    ],
    mathematical_verification="Recorded separately in independent reviews; byte verification alone is not a mathematical proof check.",
    no_lean_replay=True,
))
print(json.dumps(out["validation"], indent=2))
