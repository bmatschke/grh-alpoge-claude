#!/usr/bin/env python3
"""Build CR1--CR6 source locators from the exact pinned Lean bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPOSITORY = "https://github.com/CocoSgt/riemann-hypothesis-lean"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, default=HERE.parent.parent / "lean-source")
args = parser.parse_args()
repo = args.repo.resolve()

def sha(b):
    return hashlib.sha256(b).hexdigest()

head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
if head != COMMIT:
    raise SystemExit(f"Expected {COMMIT}, got {head}")

files = {}
def src(path, name, ns, role="source counterpart"):
    path = "src/" + path
    if path not in files:
        data = (repo / path).read_bytes()
        blob = subprocess.check_output(["git", "-C", str(repo), "show", f"{COMMIT}:{path}"])
        if data != blob:
            raise AssertionError(f"Working bytes differ from pinned Git blob: {path}")
        files[path] = {"path": path, "sha256": sha(data), "bytes": len(data),
                       "line_count": len(data.splitlines()),
                       "verified_equal_to_pinned_git_blob": True,
                       "url": f"{REPOSITORY}/blob/{COMMIT}/{path}"}
    data = (repo / path).read_bytes()
    lines = data.splitlines(keepends=True)
    start_re = re.compile(r"^(?:(?:private|protected) )?(?:theorem|lemma|def|abbrev|structure) " + re.escape(name) + r"(?:\s|\{|\(|:)")
    starts = [i for i, b in enumerate(lines) if start_re.match(b.decode())]
    if len(starts) != 1:
        raise AssertionError((path, name, starts))
    start = starts[0]
    boundary = re.compile(r"^(?:(?:private|protected) )?(?:theorem|lemma|def|abbrev|structure) |^(?:end|section|namespace|variable|attribute|include|omit|open|set_option)\b")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if boundary.match(lines[j].decode()):
            end = j
            break
    while end > start and not lines[end - 1].strip():
        end -= 1
    fragment = b"".join(lines[start:end])
    url = f"{REPOSITORY}/blob/{COMMIT}/{path}#L{start+1}-L{end}"
    qualified = name if not ns else ns + "." + name
    return {"path": path, "declaration": qualified, "source_spelling": name,
            "line_start": start + 1, "line_end": end,
            "sha256": files[path]["sha256"], "full_file_sha256": files[path]["sha256"],
            "range_sha256": sha(fragment), "range_bytes": len(fragment),
            "url": url, "pinned_url": url, "first_line": lines[start].decode().rstrip("\r\n"),
            "declaration_lines_within_range": [start + 1], "role": role,
            "verified_equal_to_pinned_git_blob": True}

CZ = "Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/CharZeroOfSetting.lean"
ER = "Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/EvalRepsSurjective.lean"
DU = "Formalism/LocalToGlobal/GlobalTheory/CoordinateLengths/DuCount.lean"
CP = "Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/"
TF = "Formalism/LocalToGlobal/GroupLattices/TiedFamilies/"
TT = "Formalism/LocalToGlobal/GroupLattices/TrivialTransfer/"
LG = "Formalism/LocalToGlobal/GroupLattices/LevelGatherings/"
CR = "GlobalTheory.ClassRank"
CMP = "Formalism.L2.G.Cmp"
TRIV = "Formalism.L2.G.Triv"
LEM = "Formalism.L2.GlobalTheoryTheory.LemB"
G = "Formalism.L2.G"

common = [
    "D7, LevelData, Forms0 and their defining global arithmetic/class/value fields are supplied; this component does not construct them.",
    "The literal local package uses the same host, p, orbit positions, coefficient extension and LocId as the source. LI1--LI7 supply those identifications under their stated hypotheses.",
    "The integral Weyl lattice Delta is not identified with the dual-Weyl coefficient lattice nabla. CB2--CB3 and IW3 are used for rational dimension only.",
    "No equality of ranks is claimed to imply a comparison map, integral lattice equality, metric identity, discarded-target control or arithmetic window."
]

claims = []
def claim(cid, title, statement, deps, sources, extra=None, status="faithful_translation", relation="The source statement is proved with explicit human arguments and unchanged literal hypotheses."):
    claims.append({"id": cid, "title": title, "status": status, "statement": statement,
                   "depends_on": deps, "assumptions": common + (extra or []),
                   "proof_location": {"file": "main.tex", "anchors": [cid]},
                   "expanded_notes": {"file": "report.txt", "section": cid},
                   "source_relation": relation, "sources": sources})

claim("CR1", "The actual integral Weyl fibers and their tensor ranks",
      "The supplied Hida setting is characteristic zero. The literal Dl0 is the determinant-twisted integral Weyl lattice; it has an actual O-basis and HtupW has rank product_(v,s) D_k(lambda0_(v,s)), with exact odd-position negative reversal.",
      ["CB2", "CB3", "IW3"], [
          src(CZ,"charZero_of_setting",CR), src(CZ,"span_map_weyl",CR),
          src(CZ,"exists_basis_Dl0",CR), src(CZ,"card_ssIdx_lamAt",CR),
          src(CZ,"exists_basis_HtupW",CR), src(DU,"finrank_weylZ",LEM),
          src(CP+"DeterminantTwistRowActionMem.lean","dw_eq",CMP),
          src(CP+"DeterminantTwistRowActionMem.lean","dw_tw",CMP),
          src("Formalism/LocalToGlobal/GlobalTheory/GL6/WeylLengthDiagonalUnitUniformiser.lean","weyl_homogeneous_basis","Formalism.L2.GlobalTheoryTheory.LocalLatticeBases"),
          src("Formalism/LocalToGlobal/GlobalTheory/GL6/WeylLengthDiagonalUnitUniformiser.lean","weyl_basis_lin_indep_field","Formalism.L2.GlobalTheoryTheory.LocalLatticeBases")
      ], status="derived_simplification", relation="Finite-free integral Weyl basis, exact word base change and a nonzero coefficient minor replace the source's basis bookkeeping. The tableau basis is used only for the rational dimension; no integral Delta=nabla assertion is made.")

claim("CR2", "Integral evaluation on free lattice-tuple orbits",
      "For a finite set of full-lattice orbits with trivial stabilizers, exact Weyl-fiber transport and a unit-valued character give an O-linear isomorphism from the actual equivariant-function module to the product of its representative fibers.",
      ["CR1"], [
          src(ER,"mem_funMod_iff",CR), src(ER,"IsReps",CR),
          src(ER,"evalReps",CR), src(ER,"evalReps_injective",CR),
          src(ER,"evalReps_surjective",CR), src(ER,"evalRepsEquiv",CR),
          src(CZ,"actHW",CR),
          src(CP+"DeterminantTwistRowActionMem.lean","determinant_twist_row_action_mem",CMP),
          src(CP+"DeterminantTwistRowActionMem.lean","equivSys_HtupW",CMP)
      ], ["This general evaluation lemma assumes free finite orbits; CR3 and CR4 prove those assumptions in the actual arithmetic application."])

claim("CR3", "The actual global class set is the local lattice-orbit set",
      "For the supplied level and LI local identifications at GIdx, the map clsR gives a bijection from the disjoint union of Gamma_i-orbits of full local lattice tuples onto C.cls 0. Its exact equality criterion and surjectivity are proved, including the actual local maximal-compact criterion.",
      ["LI3", "LI5", "LI7"], [
          src(CP+"ClsFib.lean","Fib",CMP), src(CP+"ClsFib.lean","K'_split",CMP+".Fib"),
          src(CP+"ClsFib.lean","cls_iff",CMP+".Fib"), src(CP+"ClsFib.lean","cls_surj",CMP+".Fib"),
          src(CP+"ClsLat.lean","isLattice_iff",CMP), src(CP+"ClsLat.lean","stabStd_iff",CMP),
          src(CP+"CastGLSymmApply.lean","prP",CMP), src(CP+"CastGLSymmApply.lean","jQ",CMP),
          src(CP+"CastGLSymmApply.lean","prP_jQ",CMP), src(CP+"CastGLSymmApply.lean","fibP",CMP),
          src(TF+"IntSplitOf.lean","notBad_C",G),
          src(TF+"SelfDualAtColLevel.lean","selfDualAt_colLevel",G),
          src(TF+"SelfDualAtColLevel.lean","isHyperbolicAt_rec_of_placeIdentification",G),
          src(CP+"ClsHyp.lean","isHyperbolicAt_of_integralSplit",CMP),
          src(CP+"ClsMain.lean","class_eq_iff_translate_level_zero",CMP),
          src(CP+"ClsMain.lean","level_action_lattice_eq",CMP),
          src(CP+"ClsStab.lean","clsOf",CMP), src(CP+"ClsStab.lean","clsOf_surj",CMP),
          src(CP+"ClsRec.lean","clsR",CMP), src(CP+"ClsRec.lean","clsR_iff",CMP),
          src(CP+"ClsRec.lean","clsR_surj",CMP), src(CP+"ClsGat.lean","finClasses",CMP)
      ], ["The supplied LevelData includes its class representative bijection y_bij with the finite set C.cls 0. This component proves the local/global join, not the existence of the arithmetic class record."],
      status="derived_simplification", relation="A direct split-local group and double-coset proof expands Fib, clsC and clsR. The actual HypAtP premise is derived from GIdx, local self-duality and the same LocId frames.")

claim("CR4", "Two auxiliary unipotent levels make the actual stabilizers trivial",
      "The definite integral lattice makes every rational level-class stabilizer finite. At two distinct auxiliary rational primes, the literal iwU conditions force its order to be a power of each prime; hence it is trivial. This also proves freeness of the actual local lattice-tuple action and C.StabZero.",
      ["CR3"], [
          src(TT+"FiniteStabAtOfLocal.lean","finite_stabAt_of_local",TRIV),
          src(TT+"OneAddPowOfSq.lean","unip_pow",TRIV),
          src(TT+"OneAddPowOfSq.lean","cong_coprime",TRIV),
          src(TT+"OneAddPowOfSq.lean","unip_coprime",TRIV),
          src(TT+"OneAddPowOfSq.lean","iwU_coprime",TRIV),
          src(TT+"GenCoprime.lean","gen_coprime",TRIV), src(TT+"GenCoprime.lean","gen_triv",TRIV),
          src(TT+"GramTotallyDefinite.lean","trivStabU",TRIV),
          src(TT+"GramTotallyDefinite.lean","trivStabU_rec",TRIV),
          src(TT+"GramTotallyDefinite.lean","stabZero_rec",TRIV),
          src(CP+"ClsFib.lean","stab_iff",CMP+".Fib"),
          src(CP+"ClsStab.lean","fix_iff",CMP), src(CP+"ClsStab.lean","stabRec",CMP),
          src(CP+"ClsRec.lean","trivStab",CMP)
      ], ["The auxiliary primes are distinct and prime, as supplied by D.host.g_prime and D.host.g_ne. Their actual level is the inverse image of the upper-unitriangular residue subgroup, not necessarily a principal congruence kernel."],
      status="derived_simplification", relation="Minkowski boundedness gives the same finite-stabilizer result as the source's trace-denominator construction. The prime-to-g torsion proof uses separated congruence induction, preserving the actual iwU condition even for g=2.")

claim("CR5", "The finite-class Weyl-product formula for the local rank",
      "For the actual local function module, d=|C.cls 0| product_(v,s) D_k(lambda0_(v,s)). This is the specialization of d_eq_of_classes to the proved clsR class correspondence and trivial stabilizers.",
      ["CR1", "CR2", "CR3", "CR4"], [
          src(ER,"d_eq_card_mul",CR), src(CZ,"d_eq_of_classes",CR)
      ])

claim("CR6", "The actual local rank equals the complex level-zero forms dimension",
      "For supplied D7, LevelData D, Forms0 D u, GIdx at w, and the literal LocPack X, (X.gat r e).d=dim_C (D.mem u).A.Mu0 for every r,e. The pack_d_eq wrapper follows. Joint0 is unused by this rank proof and remains necessary only for separately stated stronger comparisons.",
      ["CR5", "CR4"], [
          src(DU,"finrank_forms_level_zero",LEM),
          src(LG+"LevelGatherings.lean","lamRec",G),
          src(LG+"LevelGatherings.lean","gatRec_pos",G),
          src(LG+"LevelGatherings.lean","gatRec_lam",G),
          src(CZ,"card_ssIdx_natW",CR), src(CZ,"locPack_d_eq",CR), src(CZ,"pack_d_eq",CR),
          src("Formalism/LocalToGlobal/GroupLattices/DownNaturalLevelZero.lean","Forms0","Formalism.L2.Forms","retained supplied value/class identification record"),
          src("Formalism/LocalToGlobal/GroupLattices/DownNaturalLevelZero.lean","Joint0","Formalism.L2.Forms","separate compatibility record, not used in rank proof")
      ], ["The two level descriptions already use the same abstract finite class set C.cls 0 and the same weights. Their actual lattices, subgroups and representatives need not be identified to compare dimensions.",
          "CR6 compares rank_O M with dim_C Mu0. A separate rational-forms realization is required when replacing dim_C Mu0 by a coefficient-field dimension in a comparison-map argument."])

out = {
    "schema_version": "1.2", "artifact_version": "0.13", "date": "2026-11-21", "owner": "/root/class_rank",
    "repository": {"url": REPOSITORY, "commit": COMMIT},
    "range_convention": "One-indexed inclusive declaration ranges; exact source bytes are compared with the pinned Git blob and hashed without normalization.",
    "verification": {"full_file_bytes_compared_with_pinned_git_blob": True,
                     "range_bytes_hashed_without_normalization": True,
                     "human_mathematical_proofs_supplied": True, "lean_source_files_edited": False,
                     "local_lean_compilation": False, "lean_kernel_replay": False,
                     "replacement_arguments_formalized": False},
    "status_definitions": {
        "faithful_translation": "Complete human proof of the source assertion under explicitly supplied hypotheses and prior proved results.",
        "derived_simplification": "Complete human proof with shorter elementary arguments and the same exact source conclusion or clearly stated intermediate statement."
    },
    "independent_reviews": [], "claims": claims,
    "files": [files[p] for p in sorted(files)],
    "artifact_sha256": {p: sha((HERE / p).read_bytes()) for p in ["main.tex", "report.txt"]},
    "prior_components_reused": ["CB2", "CB3", "IW3", "LI3", "LI5", "LI7"],
    "boundary_resolved": ["Actual local class-orbit correspondence clsR_iff and clsR_surj", "Actual trivial stabilizers", "Actual locPack_d_eq and pack_d_eq rank identity"],
    "retained_inputs": common[:2] + ["The rational forms realization, actual comparison map and its value existence remain separate from CR6.", "No metric transport or global arithmetic window is proved here."],
    "scope_precision": ["Delta and nabla remain distinct integral lattices.", "Auxiliary iwU is upper unitriangular modulo a prime; identity modulo the prime is not assumed.", "The rank proof does not use Joint0.", "The same source position bijection and odd weight parity are retained."],
    "source_link_count": sum(len(c["sources"]) for c in claims), "source_file_count": len(files)
}
(HERE / "provenance.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
(HERE / "source_manifest.json").write_text(json.dumps({"commit": COMMIT, "files": out["files"]}, ensure_ascii=False, indent=2) + "\n")
lines = [f"CR source locators, commit {COMMIT}", ""]
for c in claims:
    lines.extend([f"{c['id']}: {c['title']}", c["statement"]])
    for s in c["sources"]:
        lines.extend([f"  {s['declaration']}: {s['path']}:{s['line_start']}-{s['line_end']}",
                      f"    file SHA256 {s['sha256']}", f"    range SHA256 {s['range_sha256']}",
                      "    " + s["url"]])
    lines.append("")
(HERE / "source_locators.txt").write_text("\n".join(lines) + "\n")
next_specs = [
    ("Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsStandardFormComparisonSymmetricLevelMember.lean",
     "formsTiedSym_std", "GlobalTheory.Mem.FormSym",
     "Construct the simultaneous symmetric forms, class/value/level identifications and common auxiliary character for the same TC record; Forms0 is obtained by restriction to level zero.",
     "Requires supplied TC.Ok, Pins, Laws and Later. Expand charts, the actual valuation-compatible realization and level projections; do not infer a completed global model from CR6."),
    ("Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsStandardColumnComparisonsTrueColumns.lean",
     "colsTiedSym_std", "GlobalTheory.Mem.Col2.TC",
     "Construct the joint column/forms record with matching level-zero carriers, lattice/subgroup/representative identities, character data and common frame.",
     "This is stronger than matching two dimensions: it supplies the actual compatibility later consumed by Joint0 and the comparison-value theorem. Coordinate with SF and CS upstream targets."),
    ("Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HermitianChartComplexRationalIntegralForms.lean",
     "val_tied", "GlobalTheory.Mem.Col2.TC",
     "Supply the actual complex, coefficient-field and integral polynomial realization on each chart.",
     "Expand ValuationCompatibleChart for the same ReadsK and IdY maps under TC.Ok/Pins/Laws/Later; its integral and rational conditions must remain aligned with the local comparison, not merely numerical rank equality.")
]
next_targets = []
for path, name, ns, role, scope in next_specs:
    s = src(path, name, ns, role)
    s.update({"priority_group": 1, "remaining_human_scope": scope,
              "human_status": "continuation_target_only; no reconstructed theorem is asserted by this target record"})
    next_targets.append(s)
(HERE / "next_targets.json").write_text(json.dumps({
    "version": "0.13", "commit": COMMIT,
    "status": "Source leads for still-retained simultaneous global forms/level/value supply; not additional proved claims.",
    "targets": next_targets,
    "source_files": [files[p] for p in sorted({s["path"] for s in next_targets})]
}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"claims": len(claims), "source_links": out["source_link_count"], "source_files": out["source_file_count"],
                  "continuation_targets": len(next_targets), "commit": COMMIT}))
