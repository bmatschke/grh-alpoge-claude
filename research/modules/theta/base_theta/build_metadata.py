from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / "lean_source"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO = "https://github.com/CocoSgt/riemann-hypothesis-lean"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
decl = re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
cache = {}
sources = {}

def add(sid, path, start, stop=None, role="Exact source contract, original-object identity, or independently reconstructed proof"):
    path = "src/" + path
    if path not in cache:
        b = (SOURCE/path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN+":"+path], cwd=SOURCE), path
        cache[path] = b, b.decode().splitlines(keepends=True)
    b, lines = cache[path]
    found = [i for i, s in enumerate(lines) if start in s]
    assert len(found) == 1, (sid, path, start, found)
    a = found[0]
    if stop:
        z = next(i for i in range(a+1, len(lines)) if stop in lines[i])
    else:
        z = next((i for i in range(a+1, len(lines)) if decl.match(lines[i])), len(lines))
    while z > a and not lines[z-1].strip():
        z -= 1
    block = "".join(lines[a:z]).encode()
    sources[sid] = {
        "id": sid, "path": path, "declaration_anchor": start, "declaration":start,
        "line_start": a+1, "line_end": z, "file_sha256": sha(b), "sha256":sha(b),
        "range_sha256": sha(block), "range_bytes": len(block),
        "first_line": lines[a].rstrip(), "role": role,
        "verified_equal_to_pinned_git_blob": True,
        "url": f"{REPO}/blob/{PIN}/{path}#L{a+1}-L{z}",
    }

D = "Development/AbelianVarietyTheory/"
AM = D+"Definitions/AutomorphicMembership/"
IW = D+"Proofs/IwasawaDecomposition/"
DP = D+"Proofs/DivisorProofs/"
TO = D+"Proofs/TwistedOperators/"
SP = D+"Proofs/SatakeParameters/"
IR = "Formalism/LocalToGlobal/IndefiniteReal/"
DV = "Formalism/LocalToGlobal/Divisibility/"

add("read", AM+"StableIffCarrierEq.lean", "structure Read (", "open Classical in")
add("readL", AM+"StableIffCarrierEq.lean", "structure ReadL (", "structure ReadC (")
add("pins", AM+"StableIffCarrierEq.lean", "structure Pins ", "structure Holds ")
add("holds", AM+"StableIffCarrierEq.lean", "structure Holds ")
add("liftform", AM+"StableIffCarrierEq.lean", "def liftForm ")
add("bundle", D+"Definitions/GlobalTwisting/ColumnCompatibleSelection.lean", "structure Bundle ", "def sel ")
add("twIn", AM+"DivisionPairOfAdelicFormsFaceColumnsData.lean", "structure TwIn ", "def divisionPairOfAdelicFormsFaceColumnsData ")
add("pair", AM+"DivisionPairOfAdelicFormsFaceColumnsData.lean", "def divisionPairOfAdelicFormsFaceColumnsData ")
add("realTB", AM+"DivisionPairOfAdelicFormsFaceColumnsData.lean", "def realTBOf ")
add("models", IR+"LinksChar.lean", "abbrev models_inf ", "abbrev chain_ωY ")
add("smooth_contract", "Formalism/LocalToGlobal/BesselHermitianTheta/TiedType.lean", "def SmoothVec ", "def IsTypeAt ")
add("reps_contract", IR+"Bridge.lean", "def IsReps ")
add("class_pres_contract", IR+"Bridge.lean", "structure ClassPres ", "namespace ClassPres")
add("measure_def_contract", IR+"LinksDefs.lean", "def IsMeasDef ")
add("measure_level_contract", IR+"SubgroupCharExtensionOneApply.lean", "def IsMeasLevW ", "def IsMeasFD ")
add("theta_contract", IR+"HasInfExpF.lean", "structure IsThetaP ")
add("hmod", IR+"LinksDefs.lean", "structure HMod ", "attribute [local instance] Formalism.BasicNotions.Host.cmStar")
add("coef", IR+"LinksDefs.lean", "structure CoefA ", "end CoefA")
add("ec", IR+"LinksDefs.lean", "def eC ", "def thDn ")
add("weak", IR+"LinksW.lean", "def PThF ", "structure IsThPW ")
add("orzero", IR+"LinksW.lean", "def OrZero ")
add("lowest_smooth", DP+"ExistsSmoothVecLowKSub.lean", "theorem exists_smoothVec_lowKSub ", "theorem lowT_ne_bot ")
add("lowest_nonzero", DP+"ExistsSmoothVecLowKSub.lean", "theorem lowT_ne_bot ")
add("sobolev", DP+"MultiplicitySpaceEqZeroOfLowestKTypes.lean", "theorem eq_zero_of_translates ", "theorem lowGenerates ")
add("lowgen", DP+"MultiplicitySpaceEqZeroOfLowestKTypes.lean", "theorem lowGenerates ", "end GlobalTheory.LowTypeDetermined")
add("span_sobolev", D+"Counterexamples/RotationExamples/SobolevContinuityLowGeneration.lean", "def LowGenerates ", "end GlobalTheory.Survey.SobolevContinuityLowGeneration")
add("weil_contract", IR+"LocalNewformFunction.lean", "structure IsThetaFunO ", "def toTWsmall ")
add("compact_definite", DP+"ExistsBoundUnitary.lean", "theorem exists_bound_unitary ", "open MeasureTheory in")
add("compact_integral", DP+"ExistsBoundUnitary.lean", "theorem integrableOn_theta ")
add("integrand", DP+"ThetaIntegrandIntegrable.lean", "theorem ext_invariant ", "end GlobalTheory.ThetaIntegrand")
add("fd_integral", D+"Proofs/HeightProofs/IntegrableOnFundamentalDomainOfCocompact.lean", "theorem integrableOn_fundamentalDomain_of_cocompact ")
add("linear_extension", DP+"ExistsIsThetaPrimeMultOfFiresAt.lean", "theorem exists_linear_lift ")
add("fires_assembly", DP+"ThetaFiresIffThetaMultExists.lean", "theorem exists_isThetaMult_of_firesAt ")
add("post_factor", IW+"PostOnSumMemRange.lean", "theorem exists_factor ", "end GlobalTheory.GoodProjLift")
add("char_cancel", TO+"WeilActionLiftPairStepVectorInvLevelChar.lean", "theorem char_identity ", "end GlobalTheory.VecInv")
add("half_move", TO+"AdjointHalfDatumStabilizerPairMove.lean", "theorem adjDatum_actO ")
add("finite_idem", TO+"WeilActionSchrodingerModelFiniteIdempotent.lean", "theorem smul_om_eq ")
add("vacuum", TO+"WeilLatticeVacuumStabilizerSplittingCharacters.lean", "theorem stab_vacuum ")
add("source_lift_surj", IR+"Bridge.lean", "structure ActTie ")
add("source_lift_reduction", IR+"LinksChar.lean", "abbrev grp_red_L ")
add("finite_lift", IR+"LevelTypeEquivalence/GEqTie.lean", "theorem exists_finLift ")
add("eta_odd", TO+"IsUnramifiedEtaTildeOfOddExponentSum.lean", "theorem isEtaTilde_of_odd ")
add("integral_shift", TO+"LiftLowestKTypeCompatibility.lean", "theorem integral_shift ", "theorem thF_type ")
add("no_lift", TO+"LiftLowestKTypeCompatibility.lean", "theorem eq_zero_of_no_lift ")
add("type_action", TO+"LiftLowestKTypeCompatibility.lean", "theorem finiteGroup_acts_by_lift_translation_principalType ")
add("smooth_shift", DP+"ThetaLiftIntertwinesLiftsSmoothVectors.lean", "theorem exists_translate ", "end GlobalTheory.ThetaShiftSmooth")
add("source_translate", TO+"ActEqTranslateLiftV.lean", "theorem isTranslate_act_V ", "end")
add("source_translate_actual", TO+"ActEqTranslateLiftV.lean", "theorem GlobalTheory.RationalFormsAction.act_eq_translate_lift_V ")
add("target_unitary", TO+"FiniteGroupActsUnitarilyHilbertMultiplicityModel.lean", "theorem finiteGroup_acts_unitarily_hilbertMultiplicityModel ")
add("gunit", TO+"GUnitOfModels.lean", "theorem gUnit_of_models ")
add("projector_laws", SP+"GoodProjectorUnitaryFormsModelLaws.lean", "theorem eH_laws ")
add("base_level", DP+"ThetaLiftMemMultiplicitySpaceBaseLevel.lean", "theorem thF_mem_conj ", "end GlobalTheory.ThetaLevelP")
add("good_level", DP+"MemLeviFlagOfMemParabolic.lean", "theorem proj_mem_good ")
add("explicit_witness", DP+"ThetaAdjointAtLiftEqLowestKTypeRestriction.lean", "theorem thetaFireL ")
add("restricted_theta", DP+"IsThetaPToLiftReal.lean", "theorem isThetaP_restrict ", "end GlobalTheory.ThetaPRead")
add("lift_tie", IR+"RecTie.lean", "structure LiftIds ", "structure RecTied ")
add("tolift", IR+"IsMultMapUnivZero.lean", "def toLiftReal ", "end")
add("theta_read", IW+"ThetaMapHilbertModelEqConcreteThetaMapFamilyThre.lean", "theorem thetaP_read ")
add("tests", IR+"RationalAdjoints/RatZOfTests.lean", "def LiftTest ", "def perpR ")
add("kernel", IW+"LiftLevelFormOrthogonalKilledByThetaMap.lean", "theorem theta_eq_zero_of_orth ", "end GlobalTheory.Mem.ThOrth")
add("kernel_actual", IW+"LiftLevelFormOrthogonalKilledByThetaMap.lean", "theorem thG_eq_zero_of_orth ")
add("lvlA", DV+"RowLat.lean", "def lvlA ")
add("idempotents", DV+"GoodPartHermitianSpec.lean", "def chiIdem ", "def gaStar ")
add("csum", IW+"SpanRangeMulVec.lean", "theorem csum_lvlForm ")
add("target_inj", IW+"LiftCuspFormSpaceThetaMapEqData.lean", "theorem eW_jW ", "theorem closure_span_eq ")
add("theta_of", IW+"LiftCuspFormSpaceThetaMapEqData.lean", "theorem theta_of ", "end GlobalTheory.Mem.ThRead")
add("matrix_defs", IR+"PartsOrth.lean", "def tC ", "def XW ")
add("matrix_read", IW+"LiftMatrixComputesLiftRational.lean", "theorem liftWeight_complexPoint_eq_twist ", "end GlobalTheory.Mem.LiftTheta")
add("stored_basis", DV+"DivisionCompatibleToSub2Indef2.lean", "structure ThDef3 ")
add("rows0", "Formalism/LocalToGlobal/HilbertRowConditions/ColumnsFunctionAtSubspaces.lean", "structure RowsHold0_3 ")
add("used0", IR+"RecTie.lean", "def Used0 ")
add("deep_extension", IW+"ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem exists_extension ", "theorem level_open ")
add("deep_fires", IW+"ExistsThetaLiftLinearMapCuspFormMultiplicity.lean", "theorem firesAt ", "end GlobalTheory.DefLift.ThetaMap")
AL = D+"Proofs/AdelicLatticeProofs/"
add("char_sequence", DP+"UnitaryAdelicCharacterTrivialRatAndSplit.lean", "theorem exists_seq ", "end Scalars")
add("char_infinity_reflection", DP+"UnitaryAdelicCharacterTrivialRatAndSplit.lean", "theorem eq_one_refl ", "end Refl")
add("char_infinity", DP+"UnitaryAdelicCharacterTrivialRatAndSplit.lean", "theorem eq_one_inf ")
add("char_congruence_limit", DP+"UnitaryAdelicCharacterTrivialRatAndSplit.lean", "theorem tendsto_one_of_finCong ")
add("char_rigidity", DP+"UnitaryAdelicCharacterTrivialRatAndSplit.lean", "theorem eq_one_of_rat_of_split ")
add("unitary_reflections", AL+"UnitaryMatrixEqProdQuasiReflections.lean", "theorem GlobalTheory.UnRep.isUnE_eq_prod_refl ")
add("unitary_infinite_approx", TO+"MemClosureUnitary.lean", "theorem weak_approx_real ")
add("norm_one_approx", AL+"NormOneApproximationAtLevelPrimes.lean", "theorem GlobalTheory.UnRep.normOne_approx ")
add("general_split_factor", AL+"ExistsUnitaryAdelicDecompositionSplitSupport.lean", "theorem _root_.GlobalTheory.UnRep.exists_rep_suppSplit ")
add("original_split_factor", AL+"ExistsRepSuppSplit.lean", "theorem exists_rep_suppSplit ")
add("weil_scalar", DP+"WeilDatumUniqueOnThetaFunctions.lean", "theorem exists_scalar ", "theorem scalar_split ")
add("weil_scalar_split", DP+"WeilDatumUniqueOnThetaFunctions.lean", "theorem scalar_split ")
add("weil_unique", DP+"WeilDatumUniqueOnThetaFunctions.lean", "theorem weilDatum_unique ")
add("half_coinvariant", DP+"ExistsSplitPlaceHalfHeisenbergInvariantForm.lean", "theorem exists_invariant_form ")
add("half_coinvariant_vacuum", SP+"ExistsInvariantForm.lean", "theorem exists_count_form' ", "theorem om_eq_smul_sum ")
add("split_vacuum", TO+"SplitPlaceWeilRepLatticeVacuumCharacter.lean", "theorem om_latVac_split ")
add("nonsplit_unit_root", DP+"WeilDatumFixesVacuumNonSplitPlaceUnramified.lean", "theorem exists_unit_root ")
add("nonsplit_vacuum", DP+"WeilDatumFixesVacuumNonSplitPlaceUnramified.lean", "theorem fixesVacAt_of_unram ")
add("nonsplit_original", TO+"WeilOperatorLatticeStabiliserFixesVacuumNonsplit.lean", "theorem om_fixes_vacuum ")
add("nonsplit_half", DP+"RelIndexNeZeroOfFinite.lean", "theorem exists_half_of_nonSplit ")
add("canonical_weil", DP+"ExistsWeilDatumPowersUnramifiedEtaTilde.lean", "theorem exists_weilDatum_etaTilde ")
add("twisted_weil", DP+"ExistsWeilDatumTwistHeckeCharacters.lean", "theorem exists_weilDatum_twist ")
add("host_unramified", "Formalism/HermitianLattices/StatementMass.lean", "def IsCMUnram ")
add("host_unit_root", D+"Proofs/FoundationProofs/ExistsNormOneRootCongruentOddHostField.lean", "theorem exists_root_odd ")

titles = {
    "BTH1": "Smooth lowest-type nonvanishing and Sobolev-topology cyclicity",
    "BTH2": "Exact multiplicity maps are determined by lowest-type restrictions",
    "BTH3": "Absolute convergence of the original base lowest-type theta integral",
    "BTH4": "Finite basis extensions activate stored thF and construct stored thG",
    "BTH5": "Actual finite Weil character covariance and inverse target level",
    "BTH6": "Target finite-action unitarity and base theta equivariance",
    "BTH7": "Original base Hilbert reading from an explicit full-tensor witness",
    "BTH8": "One base rational-test family gives the actual rational adjoint image",
    "BTH9": "Finite unitary idempotent orthogonal-kernel argument",
    "BTH10": "Original level kernel with exact cardinality normalization",
    "BTH11": "Stored target basis gives containment and original rational theta matrix",
    "BTH12": "Original base theta square and the exact same-Bundle producer cut",
    "BTH13": "Continuous adelic unitary characters trivial on rational and split points are trivial",
    "BTH14": "Full original Weil data with the same characters agree on theta functions",
    "BTH15": "Exact finite lattice-stabilizer character for the already supplied original action",
}
maps = {
 "BTH1": ["smooth_contract","lowest_smooth","lowest_nonzero","sobolev","lowgen"],
 "BTH2": ["smooth_contract","span_sobolev","lowgen","smooth_shift"],
 "BTH3": ["models","hmod","coef","reps_contract","class_pres_contract","measure_def_contract","measure_level_contract","weil_contract","compact_definite","compact_integral","integrand","fd_integral"],
 "BTH4": ["theta_contract","weak","orzero","linear_extension","fires_assembly","post_factor","models","read"],
 "BTH5": ["char_cancel","half_move","finite_idem","vacuum","eta_odd","source_lift_surj","source_lift_reduction","finite_lift","integral_shift","smooth_shift","base_level"],
 "BTH6": ["models","no_lift","type_action","source_translate","source_translate_actual","source_lift_surj","source_lift_reduction","finite_lift","target_unitary","gunit","projector_laws","idempotents","ec"],
 "BTH7": ["read","readL","lift_tie","tolift","base_level","good_level","explicit_witness","restricted_theta","theta_read"],
 "BTH8": ["tests","models","coef","pins","kernel_actual"],
 "BTH9": ["kernel","kernel_actual"],
 "BTH10": ["kernel_actual","lvlA","idempotents","csum","liftform"],
 "BTH11": ["target_inj","matrix_defs","matrix_read","stored_basis","theta_of","readL"],
 "BTH12": ["theta_of","bundle","twIn","pair","realTB","stored_basis","rows0","used0","deep_extension","deep_fires"],
 "BTH13": ["char_sequence","char_infinity_reflection","char_infinity","char_congruence_limit","char_rigidity","unitary_reflections","unitary_infinite_approx","norm_one_approx","general_split_factor","original_split_factor"],
 "BTH14": ["weil_contract","weil_scalar","weil_scalar_split","weil_unique","half_coinvariant","half_coinvariant_vacuum"],
 "BTH15": ["weil_contract","split_vacuum","half_coinvariant_vacuum","nonsplit_unit_root","nonsplit_vacuum","nonsplit_original","nonsplit_half","canonical_weil","twisted_weil","host_unramified","host_unit_root","vacuum"],
}
dependencies = {
 "BTH1": [], "BTH2": ["BTH1"], "BTH3": [],
 "BTH4": ["BTH2","BTH3"], "BTH5": ["BTH2","BTH3","BTH4","BTH15","WA3"],
 "BTH6": ["BTH4","BTH5"], "BTH7": ["BTH4","BTH5"],
 "BTH8": [], "BTH9": [], "BTH10": ["BTH6","BTH8","BTH9"],
 "BTH11": ["BTH7","BTH8"], "BTH12": ["BTH7","BTH10","BTH11","SLR2","SLR8"],
 "BTH13": ["WA10","QD13","QD14"],
 "BTH14": ["BTH13","CW3","CW15","CW24","WA5"],
 "BTH15": ["BTH14","CW23","WA5","WA18"],
}
tex = (HERE/"main.tex").read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    a = next(i for i,l in enumerate(lines) if l.strip() == ("% BEGIN "+cid).encode())
    z = next(i for i,l in enumerate(lines) if l.strip() == ("% END "+cid).encode())+1
    block = b"".join(lines[a:z])
    claims.append({
        "id": cid, "title": title, "introduced_in": "0.32", "classification": "B",
        "status": "complete human proof of the stated implication; original producer premises remain explicit",
        "depends_on": dependencies[cid],
        "proof_location": {"file":"base_theta/main.tex","label":"claim:"+cid,
            "line_start":a+1,"line_end":z,"sha256":sha(block),"bytes":len(block)},
        "source_ids": maps[cid], "sources":[sources[s] for s in maps[cid]],
        "quantifier_scope": {
          "BTH13":"Every nondegenerate Hermitian E/F-space of the original CM host, with a continuous unitary character trivial on rational points and every split-supported finite element; indefinite spaces included.",
          "BTH14":"Same D, standard psi, original S,T and both splitting characters; two full IsWeilDatumO actions; equality on ALL original theta functions only.",
          "BTH15":"Same original self-dual lattices, frames, eta:IsEtaTilde, arbitrary supplied full original action, and original IsLatVac theta function; characters unramified away from the finite selected split pairs."
        }.get(cid,"Pointwise on one original selected Bundle, at t0=A3.A.mu0 and all i<m, using the same actual R,F,Y,Z and exact maps. BTH12 states the family-uniform threshold supplier separately."),
    })

baseline = []
for component, ids in [("canonical_weil",["CW3","CW15","CW23","CW24"]),("finite_weil_arithmetic",["WA3","WA5","WA10","WA18"]),("quantitative_weil_dictionary",["QD13","QD14"]),("small_level_rank",["SLR2","SLR8"])]:
    path = ROOT/"reconstruction_v031"/component/"main.tex"
    baseline.append({"file":str(path.relative_to(ROOT)), "sha256":sha(path.read_bytes()), "claims":ids})
validation = {
    "source_commit_verified": True, "pinned_blob_verified_files": len(cache),
    "source_ranges": len(sources), "all_source_ranges_exact": True,
    "new_lean_build": False, "independent_human_mathematical_proof": True,
    "tex_validation": "See validation/validation.json; draft syntax only, not a rendered PDF."
}
provenance = {
    "schema":"rh-human-component-provenance/1","artifact_version":"0.32","date":"2026-11-22",
    "component":"base_theta","source_commit":PIN,"main_tex_sha256":sha(tex),
    "claims":claims,"source_inventory":list(sources.values()),"baseline_dependencies":baseline,
    "validation":validation,
    "scope_note":"The Lean proof is assumed fully checked and correct. Open obligations concern only the human reconstruction. No new formal replay or new category-A literature certificate."
}
(HERE/"provenance.json").write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+"\n")
(HERE/"source_locators.txt").write_text("\n".join(
    [f"Source pin: {PIN}", f"Main TeX SHA256: {sha(tex)}",""]+
    [f"{s['id']} | {s['declaration_anchor']}\n{s['path']}:{s['line_start']}-{s['line_end']}\nfile_sha256={s['file_sha256']}\nrange_sha256={s['range_sha256']}\n{s['url']}\n" for s in sources.values()]
))
remaining = [
    {"id":"BTH_ORIGINAL_BASE_READING","classification":"C","status":"open producer",
     "contract":"On the SAME selected Bundle, original R/F/Read/ReadL, WeakCharacterisation and phase-one Pins, Ok block data, identified with the stored A3/Zs/S0 and ThDef3 basis/maps.",
     "warnings":["LiftTie.theta is a substantive geometric reading; it is not supplied by arbitrary dimensions or by the Bundle type alone.",
                 "The same weak models and original kernels/measures must be used throughout."]},
    {"id":"BTH_BASE_CUSPIDAL_EXTENSION","classification":"C","status":"open producer; convergence and linear assembly closed",
     "contract":"For each i<m at t0, choose a basis of the original HV(i,t0); for each basis vector its exact now-convergent lowest-type integral has an extension in original Wall_i.",
     "closed_subtasks":["BTH3 actual absolute convergence","BTH4 simultaneous linear thF assembly","BTH4 stored thG existence and compatibility"],
     "source_route":["deep_extension","deep_fires"],
     "warnings":["No independent proof here of cuspidality, smooth multiplicity extension, or bounded holomorphic realization.",
                 "No independent IsIoW existence claim is made; a source route to the extension may use its own IsIoW supplier."]},
    {"id":"BTH_BASE_RATIONAL_TESTS","classification":"C","status":"open producer",
     "contract":"For each i<m one finite separating complex-linear family on actual twisted HW, rational over sigma(K) on EVERY original rational full-source theta image and EVERY original target-coordinate basis vector, only at t0.",
     "warnings":["Finite-dimensionality alone does not provide the simultaneous rationality conditions."]},
    {"id":"BTH_SAME_BUNDLE_BASE_ROWS","classification":"C","status":"open separate producer",
     "contract":"RowsHold0_3 on the same selected Bundle and same original data.",
     "warnings":["Not produced by the base theta square. Root branch retains primitive row construction."]},
]
closure = {
    "schema":"rh-component-closure/1","version":"0.32","component":"base_theta",
    "source_commit":PIN,"main_tex_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
    "new_claims":list(titles),"claim_count":len(titles),
    "class_counts":{"A":0,"B":len(titles),"C":0,"D":0},
    "all_new_claims_are_conditional_implications":True,
    "remaining_producers":remaining,
    "sufficient_rules":[
        {"id":"BTH_BASE_THETA_RULE","kind":"AND on same witness",
         "requires":["BTH_ORIGINAL_BASE_READING","BTH_BASE_CUSPIDAL_EXTENSION","BTH_BASE_RATIONAL_TESTS"],
         "concludes":"The exact original base-tuple thTheta square (BTH.43), all i<m and all rational coordinates.",
         "proof":["BTH1","BTH2","BTH3","BTH4","BTH5","BTH6","BTH7","BTH8","BTH9","BTH10","BTH11","BTH12","BTH13","BTH14","BTH15"]},
        {"id":"BTH_SMALL_LEVEL_RULE","kind":"AND on same witness",
         "requires":["BTH_BASE_THETA_RULE","BTH_SAME_BUNDLE_BASE_ROWS"],
         "concludes":"Original base small-level rank equality by SLR8; not yet an unconditional producer.",
         "proof":["BTH12","SLR8"]},
    ],
    "quantifiers":{
        "pointwise":"One actual original Bundle b and original R/F/Y/Z, t0=A3.A.mu0 only; forall i<m; forall x in K^{d_i}.",
        "universal_family_supplier":"forall Fm in A, exists a_Fm, forall x>=a_Fm with x>Fm.x1 and alpha in Fm.Ix x, all four producers on b=sigma(Fm,x,alpha).",
        "threshold":"max(a_Fm,Fm.x1+1)",
        "closed_warning":"If only a Closed supplier is proved, retain its own epsilon and K bounds; this chapter does not turn it into a universal-family supplier."
    },
    "eliminated_additional_requirements":[
        "full nonbase ExAt","chain Th","independent thG existence",
        "separate LiftTest","nonbase LiftTestB","PLevW","LUnif",
        "full H5 common-image identity","positive theta norm formula",
        "RowsHoldLam3","TupAllUsed",
        "separate exact finite-covariance assumption: BTH13-BTH15 prove actual-action normalization"
    ],
    "not_closed":["Original compatible selector existence","Original same-Bundle base reading","Actual base smooth cuspidal extension","Actual rational test existence","RowsHold0_3 producer","Complete RH/GRH human proof"],
    "new_lean_replay":False,
    "no_new_A_certificate":True,
    "source_interpretation":"All D-style ambiguity is resolved inside the explicitly supplied same-object contract; no claim of a formal source gap."
}
(HERE/"closure.json").write_text(json.dumps(closure,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"claims":len(claims),"source_files":len(cache),"source_ranges":len(sources),
    "main_tex_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
    "closure_sha256":sha((HERE/"closure.json").read_bytes()),
    "proof_hashes":{c["id"]:c["proof_location"]["sha256"] for c in claims}},indent=2))
