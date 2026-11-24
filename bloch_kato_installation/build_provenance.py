#!/usr/bin/env python3
"""Bind BX1--BX8 to exact source blobs, proof ranges and matched classical inputs."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parent / "lean-source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMP = "bloch_kato_installation"
AV = "src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
FP = "src/Formalism/WeaklyAdmissibleFiltrations/"
LC = "src/Formalism/SharpRestriction/LevelLetterCocycles/LocCoh.lean"
DN = "src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean"
LT = "src/Formalism/LocalRingCardinality/AdicCompletionLocal/LocTied.lean"
PER = "src/Formalism/LocalRingCardinality/AdicCompletionLocal/InstIsAdicCompleteOCSpanSingletonSetCast.lean"
RINGS = "src/Development/AutomorphicArithmetic/IntegralCasts/CrystallinePeriods/TruncLogEqOfPowEqZero.lean"
BK = "src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/RationalDualityOfAllCoefficients.lean"
GC = "src/ReciprocityTheory/Hypotheses/GalCoh.lean"
LK = "src/Formalism/GaloisCohomology/LocalTateDualityK.lean"
cache = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def source(path, spelling, role, line_hint=None):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pattern = (r"^(?:(?:private|protected|noncomputable)\s+)*"
               r"(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)")
    starts = [(i, m.group(1)) for i, line in enumerate(lines, 1)
              if (m := re.match(pattern, line.decode()))]
    matches = [(i, n) for i, n in starts if n == spelling or n.endswith("." + spelling)]
    if line_hint is not None:
        matches = [(i, n) for i, n in matches if i == line_hint]
    assert len(matches) == 1, (path, spelling, matches)
    start, name = matches[0]
    end = min([i for i, _ in starts if i > start] or [len(lines) + 1]) - 1
    while not lines[end - 1].strip():
        end -= 1
    block = b"".join(lines[start - 1:end])
    if path not in cache:
        pinned = subprocess.check_output(["git", "-C", str(REPO), "show", PIN + ":" + path])
        assert raw == pinned, path
        cache[path] = dict(path=path, sha256=sha(raw), bytes=len(raw), lines=len(lines),
                           verified_equal_to_pinned_git_blob=True)
    return dict(path=path, declaration=name, source_spelling=spelling,
                line_start=start, line_end=end, sha256=sha(raw),
                range_sha256=sha(block), range_bytes=len(block),
                first_line=lines[start - 1].decode().rstrip("\n"),
                url=f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}",
                role=role, verified_equal_to_pinned_git_blob=True)


specs = {
    "BX1": [
        (LT, "LocTied", "Actual eB/eD, scalar, action and filtration witnesses; no abstract unattached period model"),
        (DN, "LocPrime", "Native finite extensions, actions, root residues and exact PD cyclotomic character"),
        (DN, "LocAinf", "Original tilt, Witt and compatible-root construction"),
        (PER, "Bcris", "Literal standard-model crystalline ring"),
        (PER, "BdR", "Literal standard-model de Rham field"),
        (PER, "FilD", "Actual full integer filtration"),
        (RINGS, "acrisZero", "Generated divided powers x^n/n! in Ainf[1/ell]"),
        (RINGS, "Acris", "Actual ell-adic completion"),
        (RINGS, "BcrisPlus", "Inverting ell"),
        (RINGS, "periods", "All primitive logarithmic periods, equivalent to one t"),
        (RINGS, "Bcris", "Localization at the original period submonoid"),
        (RINGS, "BdRPlus", "Actual kernel-of-theta completion"),
        (RINGS, "BdR", "Fraction field of the completed ring"),
        (RINGS, "fil", "Positive powers and negative fractional ideal filtration", 166),
    ],
    "BX2": [
        (FP + "Statement.lean", "actVB", "Tensor Galois action on original crystalline period model"),
        (FP + "Statement.lean", "actVdR", "Tensor Galois action on original de Rham period model"),
        (FP + "Statement.lean", "Dcris", "Literal crystalline invariants"),
        (FP + "Statement.lean", "DdR", "Literal de Rham invariants"),
        (FP + "Statement.lean", "FilV", "Actual image of tensoring the filtration"),
        (FP + "Statement.lean", "continuousCocycles", "Original continuous cocycle equations"),
        (FP + "Statement.lean", "B1", "Actual rational coboundaries"),
        (FP + "Statement.lean", "finiteCocycles", "Exact crystalline coboundary witness"),
        (FP + "Statement.lean", "FiniteCohomology", "Literal quotient by actual rational coboundaries"),
        (LC, "IsDR", "Q_ell dimension with the precise [K:Q_ell] factor"),
    ],
    "BX3": [
        (FP + "Statement.lean", "Lattice", "All actual stable finite free spanning lattices"),
        (FP + "Statement.lean", "LatticeCohomology", "Actual continuous lattice cocycle quotient"),
        (FP + "StatementTor.lean", "DivisibleCohomology", "Actual locally constant divisible cocycle quotient"),
        (LK, "LocalFinitenessK", "Finite local cohomology supplier for every finite quotient"),
        (LK, "LocalTateDualityK", "Compatible finite cup duality with original cyclotomic roots"),
        (LC, "cupL", "Exact rational cup formula"),
        (LC, "cupLD", "Exact lattice-divisible cup formula"),
    ],
    "BX4": [
        (BK, "DimFormula", "Full universally quantified literal endpoint"),
        (LC, "IsDR", "Exact de Rham antecedent"),
        (FP + "Statement.lean", "H0V", "Original common kernel of rho(g)-1"),
        (FP + "Statement.lean", "DdR", "Original Q_ell-linear de Rham space"),
        (FP + "Statement.lean", "FilV", "Original zero filtration intersection"),
        (FP + "Statement.lean", "FiniteCohomology", "Original quotient in the dimensional equality"),
    ],
    "BX5": [
        (BK, "RationalDuality", "Both rational cocycle annihilator directions"),
        (LC, "IsDual1", "Original pairing, equal ranks and two nondegeneracy conditions"),
        (LC, "cycLL", "Literal cyclotomic coefficient twist"),
        (LC, "cupL", "Source cup order and action"),
        (LC, "CobL", "Actual continuous rational 2-coboundary predicate"),
        (FP + "Statement.lean", "finiteCocycles", "All finite representatives retained"),
    ],
    "BX6": [
        (FP + "Statement.lean", "latticeFiniteCocycles", "Full preimage local condition including cohomological torsion"),
        (FP + "Statement.lean", "latticeFiniteCohomology", "Actual finite lattice cohomology submodule"),
        (FP + "StatementTor.lean", "HfD", "Image plus actual divisible coboundaries"),
        (FP + "StatementTor.lean", "divisibleFiniteCohomology", "Image finite condition on actual divisible H1"),
        (LC, "IsDualLat1", "Exact integral duality of the given lattices"),
        (BK, "IntegralDuality", "Both directions required by the full endpoint"),
    ],
    "BX7": [
        (BK, "BlochKatoLocal", "Original prime/model/tie/extension quantifier order"),
        (BK, "IntegralDuality", "All lattices, arbitrary pairing and specified cyclotomic target lattice"),
        (LC, "IsDualLat1", "Exact lattice-dual biconditional"),
        (LC, "liftD", "Arbitrary representative choice, no unproved continuity assumption"),
        (LC, "repD", "Actual quotient representation"),
        (LC, "cupLD", "Cup independent of chosen representative modulo the target lattice"),
        (LC, "CobO", "Literal B2 predicate on the discrete target"),
        (FP + "StatementTor.lean", "divisibleCocycles", "Source local constancy and cocycle condition"),
        (FP + "StatementTor.lean", "BD", "Actual divisible coboundaries"),
        (FP + "StatementTor.lean", "HfD", "Source representative-level image-plus-coboundaries condition"),
    ],
    "BX8": [
        (AV + "PadicHodgeTheory/LocalPublishedTheorems.lean", "LocalPublishedTheorems", "Every one of the seven local record fields"),
        (AV + "SymplecticGSp4/EntryMem.lean", "CohomologyHyp", "Every one of the six global record fields"),
        (LK, "LocalFinitenessK", "LK2 supplier"),
        (LK, "LocalTateDualityK", "LK3 supplier"),
        (LK, "LocalEulerCharK", "LK4 supplier"),
        (GC, "LocalFiniteness", "DX1 native supplier"),
        (GC, "LocalTateDuality", "DX1 native supplier"),
        (GC, "LocalEulerChar", "DX1 native supplier"),
        (GC, "GlobalFiniteness", "DX1 with exact higher-degree oddness condition"),
        (GC, "GlobalEulerChar", "DX1 including the truncated 2-primary case"),
        (GC, "UnramifiedOrthogonality", "LD2 exact two-sided supplier"),
        (GC, "GreenbergWiles", "DX3 with its original odd-prime antecedent"),
        (BK, "BlochKatoLocal", "Full BX7 supplier including ell=2"),
        ("src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/PoitouTateNormalised.lean", "PoitouTateNormalised", "LD3 exact DX1 projection"),
    ],
}
titles = {
    "BX1": "Actual tied period models and cyclotomic twist",
    "BX2": "Exact finite cocycles, period invariants and de Rham condition",
    "BX3": "Compact-discrete and rational Tate passage on the actual lattices",
    "BX4": "Full literal BlochKato.DimFormula",
    "BX5": "Both literal rational annihilator implications",
    "BX6": "Integral annihilators with torsion and saturation retained",
    "BX7": "Complete literal Published.BlochKatoLocal",
    "BX8": "Complete LocalPublishedTheorems and CohomologyHyp installation",
}
deps = {
    "BX1": [], "BX2": ["BX1"], "BX3": ["LK3", "DX1"],
    "BX4": ["BX2"], "BX5": ["BX1", "BX2", "BX3"],
    "BX6": ["BX3", "BX5"], "BX7": ["BX1", "BX2", "BX4", "BX5", "BX6"],
    "BX8": ["BX7", "LK2", "LK3", "LK4", "LD2", "LD3", "DX1", "DX3"],
}
scopes = {
    "BX1": "Every prime, arbitrary source LocPrime/LocAinf with an actual LocTied witness, every original finite local extension. The identifications needed here use precisely scalars, actions, filtration and the original root-residue character; no claim for unattached abstract PeriodData.",
    "BX2": "Every actual finite-dimensional continuous Q_ell representation and specified module topology; representative-level crystalline witnesses, actual quotients, exact restriction-of-scalars dimensions.",
    "BX3": "All stable dual Z_ell lattices, including torsion in H1. Inverse/direct finite cohomology limits and exact normalized cup pairing are proved; no localization of a torsion pairing target.",
    "BX4": "Full source DimFormula, including finite-dimensionality and integer subtraction, for arbitrary de Rham representations; no crystalline or odd-prime restriction.",
    "BX5": "Full source RationalDuality on the given nondegenerate pairing, both orders and all cocycle representatives; actual CobL and the original cyclotomic twist.",
    "BX6": "Exact integral preimage and divisible image local conditions, including all torsion. Saturated quotient and closed double annihilator are proved.",
    "BX7": "Full source BlochKatoLocal with original prime, period-model, LocTied and finite-extension quantifiers. Full IntegralDuality, arbitrary liftD, exact CobO, all actual lattices and both directions are matched.",
    "BX8": "All seven LocalPublished fields and all six CohomologyHyp fields. Original global oddness antecedents are retained and local Bloch-Kato is supplied at every prime. No actual automorphic seed or promodular support is inferred.",
}
classical = {cid: [] for cid in titles}
classical["BX1"] = ["BX-FONTAINE"]
classical["BX4"] = ["BX-BK-DIM"]
classical["BX5"] = ["BX-BK-DUAL"]
external = {"LK2": "local_k_duality", "LK3": "local_k_duality", "LK4": "local_k_duality",
            "LD2": "local_duality_closure", "LD3": "local_duality_closure",
            "DX1": "symplectic_local_installation", "DX3": "symplectic_local_installation"}
external_records = {}
for cid, component in external.items():
    lr = (WORK / component / "provenance.json").read_bytes()
    ledger = json.loads(lr)
    claim = next(c for c in ledger["claims"] if c["id"] == cid)
    external_records[cid] = dict(component=component, provenance_file=component + "/provenance.json",
                                provenance_sha256=sha(lr),
                                main_tex_sha256=sha((WORK / component / "main.tex").read_bytes()),
                                proof_location=claim["proof_location"])

raw = (HERE / "main.tex").read_bytes()
lines = raw.splitlines(keepends=True)
claims = []
for cid in titles:
    begin = next(i for i, l in enumerate(lines, 1) if l.decode().strip() == "% BEGIN " + cid)
    start = next(i for i, l in enumerate(lines, 1) if i > begin and l.decode().startswith("\\begin{"))
    end = next(i for i, l in enumerate(lines, 1) if l.decode().strip() == "% END " + cid) - 1
    while not lines[end - 1].strip():
        end -= 1
    assert lines[end - 1].decode().strip() == r"\end{proof}"
    proof = b"".join(lines[start - 1:end])
    claims.append(dict(id=cid, title=titles[cid], introduced_in="0.28",
                       status="Complete human proof with exact original theorem scope and named classical inputs",
                       mathematical_status="Actual full-record installation with precise classical theorem matching; no Lean replay",
                       scope=scopes[cid], depends_on=deps[cid], classical_inputs=classical[cid],
                       remaining_bespoke_inputs=[],
                       proof_location=dict(file=COMP + "/main.tex", paragraph=cid, label="claim:" + cid,
                                           line_start=start, line_end=end, sha256=sha(proof), bytes=len(proof)),
                       sources=[source(*s) for s in specs[cid]],
                       source_relation="The source's complete local published interface is reconstructed using matched standard period-ring/local Bloch-Kato theorems, with explicit cochain, lattice and record transport.",
                       component_ledger=COMP + "/provenance.json"))

out = dict(schema="rh-human-reconstruction-provenance/1", artifact_version="0.28",
           date="2026-11-22", repository="https://github.com/CocoSgt/riemann-hypothesis-lean",
           commit=PIN, component=COMP, main_tex_sha256=sha(raw),
           scope="Complete actual BlochKatoLocal and containing LocalPublishedTheorems/CohomologyHyp records on all original tied period models, with named matched classical inputs.",
           claims=claims, dependency_graph=deps, external_claim_dependencies=external_records,
           classical_input_registry=COMP + "/classical_inputs.json",
           source_files=list(cache.values()),
           validation=dict(claim_count=len(claims), claim_source_links=sum(len(c["sources"]) for c in claims),
                           source_files_checked_against_pinned_git_blobs=len(cache),
                           main_tex_sha256=sha(raw),
                           verification_kind="Exact proof/source byte ranges and pinned Git blob checks; no Lean kernel replay"))
dump("provenance.json", out)
(HERE / "source_locators.txt").write_text("\n\n".join(
    c["id"] + " — " + c["title"] + "\n" +
    "\n".join(s["declaration"] + "\n" + s["url"] + "\nfile " + s["sha256"] +
              "\nrange " + s["range_sha256"] for s in c["sources"]) for c in claims) + "\n")

inputs = [
    dict(id="BX-FONTAINE", name="Standard crystalline and de Rham period rings",
         statement="For C_p, theta has principal kernel, Acris is the p-adic completion of Ainf[xi^n/n!], Bcris=Acris[1/p,1/t], BdR+ is the theta-adic completion of Ainf[1/p], and its filtration is generated by t. The Tate period logarithm is Z_p-linear.",
         primary_sources=[dict(author="Jean-Marc Fontaine", title="Le corps des périodes p-adiques",
                               publication="Astérisque 223 (1994), 59–101",
                               url="https://www.numdam.org/item/AST_1994__223__59_0.pdf",
                               location="Sections 1.5 and 2.3.3–2.3.4")],
         native_match="BX1 identifies the actual generated algebra, completions, all-primitive-period localization, action, scalars and filtration; LocTied supplies the explicit model isomorphisms.",
         used_by=["BX1"]),
    dict(id="BX-BK-DIM", name="Local finite-part dimension formula",
         statement="For every finite K/Q_p and continuous finite-dimensional de Rham Q_p representation V, H1_f(K,V) is finite-dimensional and has dimension h0(K,V)+dim_Qp(DdR(V)/Fil0).",
         primary_sources=[dict(author="Spencer Bloch and Kazuya Kato", title="L-functions and Tamagawa numbers of motives",
                               publication="The Grothendieck Festschrift I (1990), 333–400",
                               url="https://math.stanford.edu/~conrad/BSDseminar/refs/BKTamagawa.pdf",
                               location="Corollary 3.8.4, printed page 355, PDF zero-based page 22")],
         native_match="BX1/BX2 identify actual crystalline coboundary witnesses, de Rham dimensions over Q_p and the original filtered intersection; BX4 supplies the full source DimFormula.",
         used_by=["BX4"]),
    dict(id="BX-BK-DUAL", name="Rational finite-part local duality",
         statement="For every finite K/Q_p and continuous finite-dimensional de Rham Q_p representation V, H1_f(K,V) and H1_f(K,V*(1)) are exact annihilators under local Tate duality.",
         primary_sources=[dict(author="Spencer Bloch and Kazuya Kato", title="L-functions and Tamagawa numbers of motives",
                               publication="The Grothendieck Festschrift I (1990), 333–400",
                               url="https://math.stanford.edu/~conrad/BSDseminar/refs/BKTamagawa.pdf",
                               location="Proposition 3.8, printed page 354; finite-part proof printed page 356, PDF zero-based pages 21 and 23")],
         native_match="BX5 carries the actual IsDual1 pairing to evaluation and matches both source cocycle-level CobL directions. BX6/BX7 prove the integral version, rather than leaving it as an unnamed input.",
         used_by=["BX5"]),
]
dump("classical_inputs.json", dict(schema="rh-classical-input-registry/1", artifact_version="0.28",
                                 component=COMP, commit=PIN, inputs=inputs,
                                 inherited_matched_inputs=[dict(via=["LK3", "DX1"], statement="Normalized finite local Tate duality on every original finite quotient.")],
                                 not_assumed=["Global Bloch–Kato conjecture", "Any arbitrary PeriodData without LocTied",
                                              "Automorphic seeds, promodular supports, image density or a uniform automorphic catalogue"]))
dump("input_registry.json", dict(schema="rh-component-input-registry/1", artifact_version="0.28",
                                component=COMP, main_tex_sha256=sha(raw), claim_inputs=external_records,
                                classical_inputs=[x["id"] for x in inputs], remaining_bespoke_inputs=[]))
dump("closure.json", dict(schema="rh-human-component-closure/1", artifact_version="0.28", component=COMP,
                         commit=PIN, main_tex_sha256=sha(raw),
                         provenance_sha256=sha((HERE / "provenance.json").read_bytes()),
                         closed_claim_ids=list(titles), dependency_graph=deps,
                         external_claim_dependencies=external_records,
                         named_classical_inputs=[x["id"] for x in inputs], remaining_bespoke_inputs=[],
                         endpoints=[
                             dict(name="GlobalTheory.Published.BlochKato.DimFormula", supplied_by="BX4", scope=scopes["BX4"]),
                             dict(name="GlobalTheory.Published.BlochKato.RationalDuality", supplied_by="BX5", scope=scopes["BX5"]),
                             dict(name="GlobalTheory.Published.BlochKato.IntegralDuality", supplied_by="BX7", scope=scopes["BX7"]),
                             dict(name="GlobalTheory.Published.BlochKatoLocal", supplied_by="BX7", scope=scopes["BX7"]),
                             dict(name="UpperTheory.V.Loc.LocalPublishedTheorems", supplied_by="BX8", scope=scopes["BX8"]),
                             dict(name="UpperTheory.V.GradeZeroInterpolatingElement.CohomologyHyp", supplied_by="BX8", scope=scopes["BX8"]),
                         ],
                         no_new_lean_build_or_kernel_replay=True))
dump("remaining_inputs.json", dict(schema="rh-component-remaining-inputs/1", artifact_version="0.28",
                                  component=COMP, main_tex_sha256=sha(raw),
                                  remaining_bespoke_inputs_for_full_BlochKatoLocal_and_CohomologyHyp=[],
                                  named_classical_inputs=[x["id"] for x in inputs],
                                  unrelated_unpromoted_targets=["Actual image density and automorphic seeds", "Actual uniform automorphic catalogue", "Full RH/Dirichlet-GRH theorem"]))
dump("next_targets.json", dict(schema="rh-next-source-targets/1", artifact_version="0.28", component=COMP,
                               retired_target_ids=["DA26-SP-04"], targets=[],
                               explanation="The entire previously retained CohomologyHyp record is now supplied by BX8; no separate automorphic target is retired by this component."))
(HERE / "report.txt").write_text(
    "Version 0.28 — full local Bloch–Kato and cohomology installation\n\n" +
    "\n".join(c["id"] + ": " + c["title"] for c in claims) +
    "\n\nThe complete Published.BlochKatoLocal, LocalPublishedTheorems and CohomologyHyp records are supplied. "
    "The original tied period models, all primes, arbitrary source pairings and lattices, both annihilator directions, "
    "actual cocycle representatives and target normalization are preserved. "
    "Classical inputs are explicitly matched Fontaine period-ring construction and local Bloch–Kato dimension/rational duality. "
    "Integral duality is proved from finite Tate duality and the rational theorem. "
    "Automorphic seeds, image density and uniform catalogues are separate obligations.\n\n" +
    json.dumps(out["validation"], indent=2) + "\n")
print(json.dumps(out["validation"], indent=2))
