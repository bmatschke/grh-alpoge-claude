#!/usr/bin/env python3
"""Rebuild the RSL source and proof ledger, checking every pinned git blob."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
ap.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v030")
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda x: hashlib.sha256(x).hexdigest()
dump = lambda name, obj: (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
TEXT = (HERE / "main.tex").read_bytes()
LINES = TEXT.decode().splitlines(keepends=True)
baseline = json.loads((BASE / "provenance.json").read_text())
old = {c["id"]: c for c in baseline["claims"]}
assert not any(c.startswith("RSL") for c in old)

DECL = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}
def source(path, name):
    if path not in cache:
        data = (SOURCE / path).read_bytes()
        git = subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE)
        assert data == git, path
        ls = data.decode().splitlines(keepends=True)
        decls = [(i, DECL.match(x).group(1)) for i, x in enumerate(ls) if DECL.match(x)]
        cache[path] = (data, ls, decls)
    data, ls, decls = cache[path]
    found = [(k, i) for k, (i, n) in enumerate(decls) if n == name]
    assert len(found) == 1, (path, name, found)
    k, start = found[0]
    end = decls[k + 1][0] if k + 1 < len(decls) else len(ls)
    # Exclude trailing declarations of scope, but never exclude a theorem body.
    for i in range(start + 1, end):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)", ls[i]):
            end = i
            break
    while end > start + 1 and not ls[end - 1].strip(): end -= 1
    raw = "".join(ls[start:end]).encode()
    return {
      "path": path, "declaration": name, "source_spelling": name,
      "line_start": start + 1, "line_end": end,
      "sha256": sha(data), "range_sha256": sha(raw), "range_bytes": len(raw),
      "first_line": ls[start].rstrip(), "verified_equal_to_pinned_git_blob": True,
      "role": "Literal source definition, constructor, theorem, or substantive proof checked against the independent human argument; a source citation alone is not counted as a human proof.",
      "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start+1}-L{end}"
    }

S = "src/Formalism/"
G = S + "LocalToGlobal/GlobalTheory/"
DS = G + "GL6/DiagonalSlopes/"
SH = S + "SharpRestriction/GlobalSchurBounds/"
GI = "src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/"
sources = {f"RSL{i}": [] for i in range(1, 14)}
def add(ids, path, *names):
    for n in names:
        v = source(path, n)
        for ident in ids.split():
            if v not in sources[ident]: sources[ident].append(v)

add("RSL1", G+"GL5/DiscreteSeriesOfFormalDegree.lean", "GenusMassAt", "genusMassAt_of", "volume_mass_of_class_data")
add("RSL1", G+"GL5/Statement.lean", "GenusMassStd")
add("RSL1", SH+"GeneralLinearActions/GapAtLeast.lean", "stdForm", "stdLat", "massI")
add("RSL2 RSL3", SH+"MassRatioUnfoldedOfTheoremTwo.lean", "MassRatioUnderVolume", "mass_ratio_unfolded_of_theorem_two", "mass_ratio_of_true_volume_ratio", "volTie_of_realTied")
add("RSL2", G+"GL5/Statement.lean", "VolRatioTrue")
add("RSL2 RSL3", SH+"StandardLattice.lean", "VolTie", "Conclusion2")
add("RSL3", SH+"TheoremThreeOfExplicitAndCompact.lean", "BaseVolumeEqualsMass")
add("RSL2", SH+"ThickPlacesCorollaryOfAnyTranslate.lean", "VolumeRatio₂")
add("RSL3", S+"LocalToGlobal/BesselHermitianTheta/MinfDensity.lean", "RealTied")
add("RSL3", G+"GL5/DiscreteSeriesOfFormalDegree.lean", "volume_eq_mass_rank_two")
add("RSL4", GI+"ColRootsExistsPrimitiveRoots.lean", "colRoots_exists_primitiveRoots")
add("RSL4", GI+"ExistsPrimitiveRootsCoeffFieldTrueColumns.lean", "trueCols_exists_primitiveRoots")
add("RSL4", GI+"ExistsIsPrimitiveRootOfAddCharNeOne.lean", "exists_isPrimitiveRoot_of_addChar_ne_one")
add("RSL5", GI+"FormsTiedSymChiZeroFinite.lean", "formsTiedSym_chi_zero_finite")
add("RSL5", GI+"UnipotentTypeLevelCharacterFiniteOrderRootsOfUni.lean", "unipotent_type_character_finite_order")
add("RSL5", GI+"LevelCharacterNoBlocksPthRootOfUnity.lean", "lamJ_zero_blocks_mem_range_and_pow_eq_one")
add("RSL5", GI+"ComplexRootOfUnityMemRangeOfIsPrimitiveRoot.lean", "complex_rootOfUnity_mem_range_of_isPrimitiveRoot")
add("RSL5", GI+"ExistsSymmetricColumnFormsStepZeroFiniteCharacte.lean", "colsTiedSym_chiFin0")
add("RSL5", "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsStandardColumnComparisonsTrueColumns.lean", "colsTiedSym_std")
add("RSL5 RSL6", SH+"IntegralityOfRationalityLocal.lean", "ChiFin0", "FormsTwistCompatibilityFamily")
add("RSL6", S+"LocalToGlobal/ClassOfRecordOfChoice.lean", "D3", "d3_a", "Duty", "real_place_second_layer_conditions_of_choice")
add("RSL6", S+"LocalToGlobal/ThresholdSelection.lean", "TSelF", "TSel")
add("RSL6", GI+"WeilUnitaryEntries.lean", "PtE", "ptE_of_wit", "ptE_of_linked", "row_df")
add("RSL6", SH+"LinkTied.lean", "RealPlaceSecondLayerConditions", "family_conditions_of_layer_two")
add("RSL6", SH+"LemmaBSecondBranchOfLength.lean", "ConcreteFormsLevelZero")
add("RSL6 RSL13", S+"SharpRestriction/ParamsHeightRankConstant.lean", "Closed", "Closed.and", "Closed.imp")
add("RSL7 RSL8 RSL9", S+"LocalToGlobal/GroupLattices/DownNaturalLevelZero.lean", "Forms0", "FormsTied.to0")
add("RSL7", DS+"AdmissibleStabilisersOfCompatibleForms.lean", "adms_iwU", "adms_core", "adms_triv", "admissible_stabilisers_of_compatible_forms")
add("RSL7", S+"LocalToGlobal/GroupLattices/TrivialTransfer/GenCoprime.lean", "gen_coprime", "gen_triv")
add("RSL8", DS+"PSplitT.lean", "hensel_sqrt_completion_integers", "split_idempotent_of_square_root", "splitAtT_of_tied", "diamond_elements_exist_all")
add("RSL8", DS+"LocalDiamondOfSplitIdempotent.lean", "idempotent_action_prime_card", "local_diamond_of_idempotent", "local_diamond_of_split_idempotent", "SplitAtT", "diamond_elements_of_split")
add("RSL8", G+"GL6/EqOneOfCoprimeTorsionTwoPrimes.lean", "fixed_class_mem_level_general", "multi_diamond_conj_mem", "multi_diamond_mem_level")
add("RSL8", G+"GL6/EqOneOfCoprimeTorsionTwoPrimes.lean", "gres_lemma_4", "level_prime_ne_type_prime'", "level_places_prime_to_type")
add("RSL8 RSL10 RSL12", S+"LocalRingCardinality/IntCastDvdOfDvdIntegers.lean", "modT_dvd", "tower_dvd_modT", "T_mod_four", "T_ne_two")
add("RSL8", DS+"GroupActionMulSingleEqDilation.lean", "multi_diamond_of_group_elem", "group_acts_freely_classes", "group_action_mulSingle_eq_dilation")
add("RSL9", S+"LocalToGlobal/HermitianForms/FormsTied.lean", "NormTie")
add("RSL9", DS+"CharacterFiniteLevelZeroOfForms.lean", "ChiFin0")
add("RSL9", DS+"GroupActionMulSingleEqDilation.lean", "mem_forms_level_zero_iff", "level_zero_values_ne_bot")
add("RSL9", S+"LocalToGlobal/Columns/PolyFn.lean", "extV")
add("RSL9", S+"LocalToGlobal/Columns/PolyFnLemmas.lean", "extV_ne_zero", "evV_extV_ne_zero")
add("RSL9", DS+"MetricDisjointSupportOrthogonal.lean", "metric_disjoint_support_orthogonal")
add("RSL9", DS+"PolynomialFunctionFrameTranslate.lean", "diamond_value_root_of_unity", "polynomial_function_frame_translate", "polynomial_translate_map", "normSq_root_of_unity_eq_one", "majorant_norm_diamond_invariant", "diamond_isometry_at_infinity")
add("RSL9", DS+"PolynomialFunctionFrameTranslate.lean", "residue_eval_translate_rho", "polynomial_rep_residue_eval")
add("RSL9", DS+"SlopeRamifiedInducedPrimeField.lean", "InducedLattice", "induced_of_slice", "rho_preserves_rational_forms", "t2sRho", "restriction_rational_form", "lattice_level_zero_ne_bot", "t2sW", "slice_map_bijective", "mem_lattice_iff_local", "slice_mem_lattice_iff", "slice_summands_orthogonal", "slope_formula_of_split")
add("RSL10", DS+"SlopeRamifiedInducedPrimeField.lean", "slope_eq_of_isometric_sum", "induced_lattice_map_sz", "slope_ramified_induced", "slope_ramified_induced_prime_field", "three_le_level_prime", "slope_formula_of_induced", "ramified_sub_eq_inf_norm_ker")
add("RSL10", DS+"SlopeLineRamifiedFormula.lean", "freeT_of_model", "freeT_0", "slopeLine_0")
add("RSL10", G+"GL6/RamifiedRankEqFinrank.lean", "FreeRankModel", "ramified_rank_eq_finrank", "ramified_rank_formula")
add("RSL10", G+"GL6/ExistsIntegerSmulMemOfSpanTop.lean", "ramified_max_slope_le_of_model")
add("RSL10", G+"GL6/RamifiedLatticePropsOfModel.lean", "RamifiedSlopeFormula")
add("RSL10 RSL12", S+"LocalRingCardinality/DataKernels.lean", "Nm", "Mram", "du")
add("RSL10 RSL12", S+"LocalRingCardinality/Lemmas.lean", "NuV_finrank")
add("RSL11", SH+"LinkPk.lean", "NuAtT", "nuAtT_of", "nu_le_mram", "exists_free_prime", "nuCommens_of")
add("RSL11", SH+"TopDensityNGeSixteen.lean", "NuCommens", "mramSpan", "Iu_ne_zero", "nuFull_of", "nuFullF_of")
add("RSL11", S+"SharpRestriction/ParConsts.lean", "FamP")
add("RSL11", S+"LocalRingCardinality/DataDIVDefs.lean", "Iu", "NprimeDef")
add("RSL11", S+"SharpRestriction/GlobalTheoremInputs.lean", "NuFullF")
add("RSL12", S+"SharpRestriction/AdmissibleParameterJoins/SumLogPrimeFactorsLe.lean", "MuRank")
add("RSL12", SH+"LinkMin.lean", "muRank_min", "nuCommensF_min")
add("RSL12", S+"LocalRingCardinality/DataLatDefs.lean", "Uprod", "Sram", "expT", "Nlam", "URat", "UL")
add("RSL12", SH+"FiniteModelOfAdmissibleTransports.lean", "Rat0", "gR", "GR", "GR_pow_spec", "Nlam_eq", "gR_Sram")
add("RSL12 RSL13", G+"GL6/CongruenceNoKernelOfHeckeRamified.lean", "HeckeIntegralLevelZero", "HeckeRamifiedLevelZero", "SecondBranchInclusionLength", "congruence_no_kernel_minimal")
add("RSL13", GI+"LinkGl.lean", "GlobalTheory.Top.link_gl")
add("RSL13", S+"SharpRestriction/SmoothDesignExistence/DesignExistsDes.lean", "Des")
add("RSL13", SH+"TuSizeOfRealPlaceSecondLayer.lean", "Wire.famGLmin_of_realPlaceSecondLayer")
add("RSL13", SH+"LogXLowerFamilyOfTheorems.lean", "FamGLmin", "FamGLmin.link7", "FamGLmin.link8", "FamGLmin.muRank", "family_theorems_two_and_five")
add("RSL13", SH+"LinkMin.lean", "linkGLOBAL7_items", "linkGLOBAL7_min")
add("RSL13", SH+"LinkMin.lean", "FamU")
add("RSL13", SH+"ProductFirstZerothParts.lean", "HidaSetting")
add("RSL13", G+"PlacesP.lean", "settingF_of")
add("RSL13", S+"SharpRestriction/AdmissibleParameterJoins/DIVfromGLm.lean", "numsL_wtsL_fam")
add("RSL13", S+"SharpRestriction/AdmissibleParameterJoins/DIVfromGLo.lean", "levelPrime_setting_of_sizes")
add("RSL13", SH+"TheoremThreeFamilyOfGappedMultiplicity.lean", "finrank_lowK_eqG", "theorem_three_rows_of_real_place", "explicit_bound_family")
add("RSL13", G+"GL4/ColumnLatticeExactSlope.lean", "column_lattice_exact_slope")
add("RSL13", G+"GL4/LowerSlopeInequalityFamily.lean", "lower_slope_inequality_family")
add("RSL13", G+"GL4/ClassMapArchimedean.lean", "q_frame_degree", "class_map_archimedean")
add("RSL13", G+"GL4/PStmtFree.lean", "slope_inequality_family_four")
add("RSL13", G+"ColValS.lean", "ColTieW", "column_value_nonempty_iff")
add("RSL13", G+"TransposeBaseMatrixInfinity.lean", "finCo_of", "colValOfTiedS_holds")
add("RSL13", S+"PeriodIntegrals/OrbitalBoundsConclusion/IntegralAtT0Lattice.lean", "integral_at_t0_lattice")
add("RSL13", G+"UnramifiedTrace/HeckeRamifiedZeroAll.lean", "hecke_ramified_zero_all")
add("RSL13", G+"CoordinateLengths/SecondBranchAllMembers.lean", "second_branch_all_members")

titles = [
 "Literal genus mass on the original positive Hermitian lattice",
 "Universal reciprocal mass-to-volume implication with the original complement",
 "Original real-place, Haar and base-volume transport",
 "Primitive auxiliary roots in the existing coefficient field",
 "Explicit g0*g1 exponent for every supplied symmetric form",
 "Same-selector finite-character and real-place installation with full quantifiers",
 "Trivial original stabilizers from the two auxiliary primes",
 "Local split diamonds and free action on the original class set",
 "Exact integral orbit-slice decomposition and isometry at every embedding",
 "Literal ramified rank, mean, maximal slope and FreeT/SlopeLine outputs",
 "Original NuFullF from the weaker eventual ramified inclusion",
 "Positive original rank and the sufficient operator-inclusion cut",
 "Exact eleven-field global cut and explicit remaining implication tasks"
]
deps = {
 "RSL1":["GV9","GV10","GV11","GV13"],
 "RSL2":["GV14","GV15"],
 "RSL3":["RSL1","RSL2","GV13","MF19"],
 "RSL4":[], "RSL5":["RSL4","TG12","DR3"],
 "RSL6":["RSL3","RSL5","RSL7"],
 "RSL7":["LP1"], "RSL8":["RSL7"],
 "RSL9":["RSL7","RSL8"], "RSL10":["RSL9","LC7"],
 "RSL11":["MT1"], "RSL12":["RSL6","RSL10","RSL11"],
 "RSL13":["RSL1","RSL2","RSL3","RSL6","RSL10","RSL11","RSL12","DC1","DC10","DC15","DC19","DC20","FR1","GF8","TG12"]
}
retained = {
 "RSL1":["Original D7, original HSpace, SigOK, positive signature and stated rank"],
 "RSL2":["Original D7 with its original VolTie; original signature-admissible W of rank at least three"],
 "RSL3":["Original RealTied or VolTie on the very record whose volume is used"],
 "RSL4":["Original TC(B,X), literal Ok, Laws, Later; no new field extension"],
 "RSL5":["Primitive g_i-th roots in original K, original FormsTiedSym; for the concrete constructor retain TC.Ok, Pins, Laws and Later"],
 "RSL6":["Original TSelF and eventual original-field root supply, or an equality of the entire linked (D,O,Bundle) tuple; same-record selector producer not supplied here"],
 "RSL7":["Actual Forms0 on the original D,u"],
 "RSL8":["Actual Forms0 and its original AtTTied/local functionals; original odd prime T"],
 "RSL9":["Actual Forms0 and ChiFin0; actual rational/integral/norm fields; no new choice of ambient metric"],
 "RSL10":["Actual Forms0, ChiFin0 and original division embedding/range. The source-facing HidaSetting hypothesis is retained, but the independent proof uses only T>=3, derived pointwise from the original tower/norm congruence."],
 "RSL11":["Original FamP, including its own nuDef, nprimeDef and ex.lat.atT; one eventual threshold for all actual Nlam inclusions"],
 "RSL12":["Original second-layer witness and eventual Nlam inclusion; the source-facing TuSize hypothesis is retained but unused because T>=3 holds pointwise. Alternatively use the explicit three weaker operator-inclusion clauses in RSL.26, including their bTop>=0 hypothesis."],
 "RSL13":["This claim closes exact contract identification and finite Closed-conjunction only; named producer and final assembly obligations remain open"]
}
claims=[]
for i,title in enumerate(titles,1):
    ident=f"RSL{i}"
    start=next(k for k,l in enumerate(LINES) if l.strip()==f"% BEGIN {ident}")
    end=next(k+1 for k,l in enumerate(LINES) if l.strip()==f"% END {ident}")
    proof="".join(LINES[start:end]).encode()
    assert all(d in old or d in deps for d in deps[ident]), (ident,deps[ident])
    claims.append({
      "id":ident,"title":title,"introduced_in":"0.31",
      "status": "Complete independent human proof of the stated conditional implication" if i<13 else "Complete selected-interface audit and finite conjunction proof; remaining producer and assembly tasks explicitly retained",
      "mathematical_status":"human reconstruction, under the standing assumption that the pinned Lean proof is fully checked and correct; no kernel replay or new formalization claimed",
      "classification":"A+B" if i in (1,2,3) else "B",
      "scope":"The original record, coefficient field, lattices, metrics, member index and word; no separately chosen replacement family",
      "depends_on":deps[ident], "hypotheses_retained":retained[ident],
      "classical_inputs":(["GV-TAM"] if i in (1,2,3) else []) + (["MF-HM"] if i==2 else []),
      "remaining_bespoke_inputs":retained[ident] if i in (6,11,12,13) else [],
      "proof_location":{"file":"second_layer_global/main.tex","paragraph":ident,"label":"claim:"+ident,"line_start":start+1,"line_end":end,"sha256":sha(proof),"bytes":len(proof)},
      "sources":sources[ident]
    })

inputs=[]
for file in ["geometric_volumes/main.tex","mass_formula/main.tex","terminal_geometry/main.tex","decorated_realization/main.tex","lattice_patching/main.tex","discrete_series_core/main.tex","local_accounting/augmentation_model.tex","metric_transport/main.tex","gram_frame/gram_frame_section.tex","RH_readable_reconstruction_v0_30.tex"]:
    p=BASE/file
    assert p.exists(), file
    inputs.append({"file":file,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size,"scope":"inherited v0.30 proof used only in its stated scope"})
provenance={"schema":"rh-human-component-provenance/1","artifact_version":"0.31","date":"2026-11-22","source_commit":PIN,"component":"second_layer_global",
 "standing_assumption":"The underlying pinned Alpoge-Claude Lean proof is fully checked and correct. Open/D statuses below concern only human reconstruction and source understanding.",
 "main_sha256":sha(TEXT),"claims":claims,"inherited_proof_inputs":inputs,
 "range_convention":"Inclusive one-based physical source and proof lines; SHA256 covers exact UTF-8 bytes with line endings.",
 "not_closed":["Actual common compatible-selector producer", "Complete GL4 hZa/hZb/tCV producers", "GL6 actual Hecke-integral, ramified-Hecke and second-branch-length producers", "TuSize to SettingEventually/HidaSetting numerical installation for the strong GL6 route", "h3 final finite-product/row installation", "Final linkGLOBAL7_items numerical/lattice assembly", "Full RH or unrestricted Dirichlet GRH human proof"]}
dump("provenance.json",provenance)

locator=[f"RSL source locators; repository CocoSgt/riemann-hypothesis-lean; commit {PIN}","All source blobs checked byte-for-byte against the pinned git object.",f"main.tex SHA256 {sha(TEXT)}",""]
for c in claims:
    p=c['proof_location']; locator.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c['sources']: locator.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    locator.append("")
(HERE/"source_locators.txt").write_text("\n".join(locator)+"\n")

nodes=[
 {"id":"SAME_RECORD_SELECTOR","classification":"C","status":"open producer outside this component","contract":"Compatible actual selector and true-column realization on the original FamP; original TSel.T.theta.real and TSel.T.cols identified on exactly the same D, or equality of the full dependent linked tuple.","role":"producer"},
 {"id":"MASS_RATIO_UNDER_VOLUME","classification":"A","status":"closed under inherited GV-TAM and MF-HM","claims":["RSL2"],"role":"proved universal implication"},
 {"id":"GENUS_MASS_AT_TWO","classification":"A","status":"closed under inherited GV-TAM","claims":["RSL1"],"role":"proved universal theorem"},
 {"id":"TC_FINITE_CHARACTER","classification":"B","status":"closed on literal supplied TC with Ok/Pins/Laws/Later; any supplied symmetric columns on same D","claims":["RSL4","RSL5"],"role":"proved implication"},
 {"id":"GLOBAL_SECOND_LAYER_MATCH","classification":"B","status":"same-object implication closed; actual same-record selector producer remains external","claims":["RSL6"],"role":"proved implication"},
 {"id":"GL6_INDUCED_INTEGRAL_ISOMETRIC","classification":"B","status":"closed conditional on original Forms0 and ChiFin0","claims":["RSL7","RSL8","RSL9","RSL10"],"role":"proved implication"},
 {"id":"H3_ROW_BOUND_INSTALL","classification":"B","status":"open exact finite-product and row installation; deep DS producers already covered by DC","role":"proof of implication","source_declarations":["theorem_three_rows_of_real_place","explicit_bound_family"]},
 {"id":"GL4_LOWER_SLOPE","classification":"B","status":"open actual producer","role":"producer","contract":"hZa = Closed C (FamilySlopeLowerOpenPart Fm)","source_declarations":["column_lattice_exact_slope","lower_slope_inequality_family"]},
 {"id":"GL4_MAX_SLOPE","classification":"B","status":"open actual producer","role":"producer","contract":"hZb = Closed C (FamilySlopeMaxOpenPart Fm 4)","source_declarations":["q_frame_degree","class_map_archimedean","slope_inequality_family_four"]},
 {"id":"GL4_COLVAL_DICTIONARY","classification":"B","status":"open exact ColTieW/ColVal installation; no unresolved object name remains","role":"proof of implication","contract":"Same original rational forms, actual Q_c,tau, all local integral bases, all archimedean metric matrices","source_declarations":["ColTieW","finCo_of","colValOfTiedS_holds"]},
 {"id":"GL6_HECKE_INTEGRAL","classification":"B","status":"open actual two-operator integrality producer","role":"producer","contract":"HeckeIntegralLevelZero: for all seen w above T and all v, U(Bw) subset S and D(S) subset Bw","source_declarations":["HeckeIntegralLevelZero","integral_at_t0_lattice"]},
 {"id":"GL6_HECKE_RAMIFIED","classification":"B","status":"open actual ramified operator producer","role":"producer","contract":"HeckeRamifiedLevelZero: both operators preserve the original MramI0 and U D = T^(N0-1)","source_declarations":["HeckeRamifiedLevelZero","hecke_ramified_zero_all"]},
 {"id":"GL6_SECOND_BRANCH_LENGTH","classification":"B","status":"open actual local inclusion and exact length producer","role":"producer","contract":"SecondBranchInclusionLength on the original S0w, Bw0wv, bTop, weight and ramification index","source_declarations":["SecondBranchInclusionLength","second_branch_all_members"]},
 {"id":"TASK_GL6_SIZE_SETTING","classification":"B","status":"open numerical proof of implication","role":"proof of implication","contract":"Original TuSize implies SettingEventually: one common threshold for every original i,u and full HidaSetting (prime bound, weight/alcove bounds, top bTop nonnegativity). TuSize itself is supplied by the D3 class projection; the implication remains to be reconstructed.","source_declarations":["FamU","HidaSetting","settingF_of","numsL_wtsL_fam","levelPrime_setting_of_sizes"]},
 {"id":"NLAM_INCLUSION","classification":"B","status":"weaker sufficient input; produced from RSL.26 by a completed finite product proof","claims":["RSL12"],"role":"proved implication with residual operator hypotheses","contract":"exists aN forall x>=aN i u w|T, actual Nlam(D,u,w) subset actual Sram(D,u,w)"},
 {"id":"NUFULL_MURANK","classification":"B","status":"closed conditional implication from original second layer and Nlam inclusion; source-facing TuSize is retained but unused","claims":["RSL11","RSL12"],"role":"proved implication"},
 {"id":"CONGRUENCE_LENGTH_INSTALL","classification":"B","status":"open finite local length inequality from the three exact GL6 contracts","role":"proof of implication","source_declarations":["congruence_no_kernel_minimal"]},
 {"id":"GLOBAL_FINAL_ASSEMBLY","classification":"B","status":"open numerical/lattice installation into ChainTied; FR1/GF8 abstract frame/HN part inherited complete","role":"proof of implication","source_declarations":["linkGLOBAL7_items","linkGLOBAL7_min"]},
 {"id":"TASK_LINK_GL_INSTALL","classification":"B","status":"partially closed; not the complete LinkGLOBAL pair","claims":["RSL13"],"role":"selected-route umbrella with explicit remaining tasks"}
]
gates=[
 {"id":"rsl_same_selector","rule":"all_of","premises":["SAME_RECORD_SELECTOR","TC_FINITE_CHARACTER"],"conclusion":"GLOBAL_SECOND_LAYER_MATCH","proof_status":"proved conditional implication","claims":["RSL6"],"same_object_constraint":"Use original selector T.theta.real and T.cols for the same D; threshold max(aChi,aSel,Fm.x1+1) before i,u."},
 {"id":"rsl_induced","rule":"all_of","premises":["GLOBAL_SECOND_LAYER_MATCH"],"conclusion":"GL6_INDUCED_INTEGRAL_ISOMETRIC","proof_status":"proved conditional implication","claims":["RSL7","RSL8","RSL9","RSL10"],"retained_hypotheses":["The source-facing rank/mean statement retains HidaSetting, but the independent proof only uses T>=3, already derived pointwise from original tower/norm congruences; no full SettingEventually supplier is invoked."],"same_object_constraint":"Original D,u, coefficient field K, embedding, class set, rational lattice B, local membership and all infinite-place matrices."},
 {"id":"rsl_nlam","rule":"all_of","premises":["GL6_HECKE_INTEGRAL","GL6_HECKE_RAMIFIED","GL6_SECOND_BRANCH_LENGTH","TASK_GL6_SIZE_SETTING"],"conclusion":"NLAM_INCLUSION","proof_status":"proved conditional implication once the conditional FamU producers and actual SettingEventually are installed, using only weaker components RSL.26","claims":["RSL12"],"same_object_constraint":"Same local w,v and original Bw,S,Nlam; same source ordered list and scalar exponent m sum bTop. Direct eventual Nlam inclusion can instead be supplied independently, without this stronger cut."},
 {"id":"rsl_fullness_rank","rule":"all_of","premises":["GLOBAL_SECOND_LAYER_MATCH","NLAM_INCLUSION"],"conclusion":"NUFULL_MURANK","proof_status":"proved conditional implication","claims":["RSL11","RSL12"],"retained_hypotheses":["Original FamP with literal nuDef and nprimeDef","Original TuSize is available from D3(3,A) membership but is unused in this stronger proof; original T=1 mod4 supplies T>=3 pointwise"],"same_object_constraint":"No added NprimeDef, replacement lattice, new metric or additional common ideal. Literal retained rank d_u=(D.mem u).A.du, not a nonexistent D.du field."},
 {"id":"rsl_complete_gl_selected_cut","rule":"all_of","premises":["MASS_RATIO_UNDER_VOLUME","GENUS_MASS_AT_TWO","GLOBAL_SECOND_LAYER_MATCH","GL6_INDUCED_INTEGRAL_ISOMETRIC","H3_ROW_BOUND_INSTALL","GL4_LOWER_SLOPE","GL4_MAX_SLOPE","GL4_COLVAL_DICTIONARY","GL6_HECKE_INTEGRAL","GL6_HECKE_RAMIFIED","GL6_SECOND_BRANCH_LENGTH","TASK_GL6_SIZE_SETTING","CONGRUENCE_LENGTH_INSTALL","GLOBAL_FINAL_ASSEMBLY"],"conclusion":"TASK_LINK_GL_INSTALL","proof_status":"not yet a complete human implication; source sufficient interface recorded; remaining proof-of-implication nodes are required","retained_hypotheses":["Duty on original A","C = D3(3,A)","ChosenE 3 CH for full-rank output","TuSize,DGamSize for LinkGLOBAL output"],"same_object_constraint":"Finite Closed conjunction uses min epsilon bounds and sup transported bounds before family/CH; maxima of eventual thresholds only afterwards."}
]
closure={"schema":"rh-component-closure/1","artifact_version":"0.31","component":"second_layer_global","source_commit":PIN,"main_sha256":sha(TEXT),
 "scope":"Selected global second-layer and LinkGl branch; no claim of complete RH/GRH proof or minimality beyond the named interfaces.","nodes":nodes,"implication_gates":gates,
 "shared_work_edges_are_not_sufficient_rules":[{"from":"RSL9","to":"GL4_COLVAL_DICTIONARY","reason":"rational restriction and metric mechanisms help, but original Q_c,tau identification and complete ColTieW constructor are not written"},{"from":"DC1,DC10,DC19","to":"H3_ROW_BOUND_INSTALL","reason":"deep analytic producer covered; finite-product and row matching still required"},{"from":"FR1,GF8","to":"GLOBAL_FINAL_ASSEMBLY","reason":"abstract frame/HN consequence already proved; literal input ledger still to be assembled"}],
 "retirement_scopes":[{"historical":"LC7 integral/isometric transport boundary","new":"RSL9–RSL10 close it under actual Forms0+ChiFin0+HidaSetting"},{"historical":"FC19 terminal ColsTiedSym boundary","new":"Already superseded by TG12 in literal TC.Ok/Pins/Laws/Later scope; RSL5 supplies finite character"},{"historical":"GLOBAL_SECOND_LAYER_MATCH meaning gap","new":"Exact TSel and dependent tuple dictionary proved; common compatible-selector C producer still retained"}],
 "not_retired":["Compatible selector/arithmetic producer","hZa/hZb/tCV","actual GL6 operators/length","TASK_GL6_SIZE_SETTING","full TASK_LINK_GL_INSTALL","full GLOBAL_GL_PAIR"]}
dump("closure.json",closure)

all_sources={(s['path'],s['line_start'],s['line_end']):s for c in claims for s in c['sources']}
validation={"status":"PASS","main_sha256":sha(TEXT),"source_commit":PIN,"claim_count":len(claims),"claim_source_ranges":sum(len(c['sources']) for c in claims),"distinct_source_ranges":len(all_sources),"distinct_source_files":len(cache),"inherited_proof_files":len(inputs),"all_source_files_equal_pinned_git_blobs":True,"all_proof_markers_unique_and_present":True,"all_dependencies_resolve_to_v030_or_RSL":True,"warning":"This validates provenance, not mathematics. Independent reviews are separate artifacts."}
dump("validation.json",validation)
report=["SECOND-LAYER GLOBAL RECONSTRUCTION v0.31",f"Pinned source: {PIN}",f"main.tex SHA256: {sha(TEXT)}",f"Claims: {len(claims)}; claim/source ranges: {validation['claim_source_ranges']}; distinct ranges: {len(all_sources)}; files: {len(cache)}.","",
 "Completed: literal universal hG and hU with inherited GV-TAM/MF-HM; actual RealTied→VolTie/base-volume transport; primitive roots in original K; explicit g0*g1 finite character for ANY symmetric forms on same D; exact original TSel.T.cols/T.theta.real join; actual trivial stabilizers, free diamond action, integral slice and all-embedding isometry; actual FreeT/SlopeLine/rank/mean/max-slope; original NuFullF/MuRank from the smaller Nlam inclusion.",
 "Not completed: compatible common selector producer (C), full GL4 hZa/hZb/tCV, actual GL6 operator/length producers, numerical TuSize→SettingEventually/HidaSetting installation, finite h3 row installation, and final LinkGLOBAL7 ledger assembly (B). No assertion of full GLOBAL_GL_PAIR or full RH/GRH human proof.","",
 "QUANTIFIER AND SAME-OBJECT BOUNDARY",
 "Closed means exists eps1>0, forall eps in (0,eps1], exists transported bound K, forall original Fm,CH, C(Fm) and Large(K,CH) imply P(Fm,CH). Finite conjunction uses min eps1 and sup K. The member threshold then precedes all x,i,u,w. The same-record selector T, coefficient field, local lattice, metric, and Nu lattice are retained throughout.",
 "RSL6 uses original selector.T.theta.real and selector.T.cols; its threshold is max(aChi,aSel,Fm.x1+1). If obtained through a bundle, transport the equality of the entire dependent (D,O,Bundle), not only field/rank equality.",
 "RSL11 uses original FamP.nuDef, FamP.nprimeDef and ex.lat.atT. They are not new assumptions or chosen after a word. RSL12's operator cut uses the same list/order and expT=m*sum bTop; no commutativity of U operators is required. D3(3,A) membership already supplies TuSize, and the stronger actual-forms rank proof does not use it: original tower divisibility and norm congruence give T=1 mod4 and T>=3 pointwise. Thus the longer TuSize→SettingEventually supplier is not silently claimed here. The literal ramified rank is d_u=(D.mem u).A.du; emb_basis plus rational norm operators establishes the scalar-extension rank dictionary.","",
 "EXACT THREE GL6 CONTRACTS AND SOURCE SUPPLIERS"]
for s in sources['RSL13']:
    if s['declaration'] in {"HeckeIntegralLevelZero","HeckeRamifiedLevelZero","SecondBranchInclusionLength","integral_at_t0_lattice","hecke_ramified_zero_all","second_branch_all_members","congruence_no_kernel_minimal"}:
        report.append(f"{s['declaration']}: {s['path']}:{s['line_start']}-{s['line_end']}; file SHA256 {s['sha256']}; range SHA256 {s['range_sha256']}")
report += ["","RSL.26 is the smaller fullness-only cut: U(Bw)⊂S, U preserves Mram, and T^bTop S⊂Bw, for the original selected places with bTop≥0. These imply Nlam⊂Sram by composition and powering. Full global error accounting also needs D, the inverse-composite relation and exact lengths. Promoting the strong conditional FamU contracts to actual members additionally needs TASK_GL6_SIZE_SETTING, the B numerical implication TuSize→SettingEventually via PlacesP.settingF_of, DIVfromGLm.numsL_wtsL_fam and DIVfromGLo.levelPrime_setting_of_sizes. Bare eventual Nlam inclusion remains an independent weaker sufficient input.","",
 "HIGHEST-VALUE NEXT CLOSURE",
 "For the fullness/rank output, reconstruct only RSL.26 first: it avoids the exact-length calculation. For full LinkGLOBAL, finish the three GL4 contracts and the complete GL6 operator/length producers, then write the literal LinkGLOBAL7_items assembly using FR1/GF8, inherited mass/row/metric results, and the same common threshold. Do not reopen TG12 terminal geometry or LC7's now-closed actual isometric transport.","",
 "No predecessor file was modified. No Lean build, replay or new formalization is claimed; mathematical correctness of the pinned proof is the standing premise."]
(HERE/"report.txt").write_text("\n".join(report)+"\n")
print(json.dumps(validation,ensure_ascii=False,indent=2))
