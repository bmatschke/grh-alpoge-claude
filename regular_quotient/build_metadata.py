#!/usr/bin/env python3
"""Rebuild RQC exact source and human-proof certificates, without running Lean."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
DEFAULT=HERE.parent if (HERE.parent/"holomorphic_uniqueness").exists() else HERE.parent.parent/"reconstruction_v035"
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--source",type=Path,default=HERE.parent.parent/"lean_source")
p.add_argument("--human-root",type=Path,default=DEFAULT)
a=p.parse_args(); SOURCE=a.source.resolve(); HUMAN=a.human_root.resolve()
PIN="7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO="https://github.com/CocoSgt/riemann-hypothesis-lean"
sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=SOURCE,text=True).strip()==PIN
cache={};sources={}
decl=re.compile(r"^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+")
def get(path):
    if path not in cache:
        b=(SOURCE/path).read_bytes()
        assert b==subprocess.check_output(["git","show",PIN+":"+path],cwd=SOURCE),path
        cache[path]=(b,b.decode().splitlines(keepends=True))
    return cache[path]
def add(sid,path,anchor,role="Exact original definition, source argument or endpoint reconstructed independently"):
    path="src/"+path;b,lines=get(path)
    hits=[i for i,l in enumerate(lines) if anchor in l]
    assert len(hits)==1,(sid,path,anchor,hits)
    i=hits[0];j=next((j for j in range(i+1,len(lines)) if decl.match(lines[j])),len(lines))
    while j>i and not lines[j-1].strip():j-=1
    block="".join(lines[i:j]).encode()
    sources[sid]={"id":sid,"path":path,"declaration":anchor,"declaration_anchor":anchor,
      "line_start":i+1,"line_end":j,"sha256":sha(b),"file_sha256":sha(b),
      "range_sha256":sha(block),"range_bytes":len(block),"first_line":lines[i].rstrip(),
      "role":role,"verified_equal_to_pinned_git_blob":True,
      "url":f"{REPO}/blob/{PIN}/{path}#L{i+1}-L{j}"}
old=json.loads((HUMAN/"holomorphic_uniqueness/provenance.json").read_text())
oldsrc={s["id"]:s for s in old["source_inventory"]}
for sid in ["finite_pair","quotient_measure","original_representative","regular_representation",
 "smooth_vector","real_derived_action","complex_derived_action","real_involution","real_lie",
 "model","model_action","model_smooth_span","unitary_representation","irreducibility",
 "original_frame","bounded_holomorphic_form","central_cuspidality","original_cusp_packet",
 "multiplicity_map_contract","full_multiplicity_extension","remaining_smooth_representative",
 "remaining_sobolev_growth","point_evaluation_continuity","remaining_boundedness",
 "remaining_target_volume","original_archimedean_lift","source_borel_extremal",
 "actual_model_representation","actual_hilbert_map","finite_eigenclass"]:
    d=dict(oldsrc[sid]);b,ls=get(d["path"])
    assert sha(b)==d["file_sha256"]
    assert sha("".join(ls[d["line_start"]-1:d["line_end"]]).encode())==d["range_sha256"]
    sources[sid]=d
D="Development/AbelianVarietyTheory/";DP=D+"Proofs/DivisorProofs/"
IW=D+"Proofs/IwasawaDecomposition/";IR="Formalism/LocalToGlobal/IndefiniteReal/"
BT="Formalism/LocalToGlobal/BesselHermitianTheta/"
DEF=D+"Definitions/Divisors/IsSmoothVector.lean"
add("topology",IW+"AdelicUnitaryTopology.lean","theorem adelic_unitary_topology ")
add("adele_lc",D+"Proofs/UnitaryExistence/LcscAdelicUnitaryGroup.lean","theorem lcsc_adelicUnitary ")
add("adele_countable",D+"Proofs/UnitaryExistence/LcscAdelicUnitaryGroup.lean","theorem secondCountable_restrictedProduct ")
add("rational_discrete",D+"Proofs/SiegelThetaTransformation/DiscreteTopologyRationalPointsHermitianSpace.lean","theorem discreteTopology_GQ ")
add("rational_zero_neighborhood",D+"Proofs/SiegelThetaTransformation/DiscreteTopologyRationalPointsHermitianSpace.lean","theorem exists_nhds_zero_inclR ")
for sid,anchor in [("quotient_class","abbrev cl "),("right_translate","def tr "),("right_translate_law","theorem tr_mul "),
 ("quotient_measurable","theorem measurable_cl "),("translate_measurable","theorem measurable_tr "),
 ("global_ae","theorem ae_of_ae_quot "),("quotient_measure_preserving","theorem measurePreserving_tr "),
 ("symmetric_difference","theorem measure_symmDiff_le "),("regular_map","def reg "),
 ("regular_value","theorem reg_val "),("regular_norm","theorem norm_reg "),
 ("regular_continuity","theorem continuous_reg "),("regular_exists","theorem exists_isReg ")]:
    add(sid,DP+"RegularRepresentationOfFinitePair.lean",anchor)
for sid,anchor in [("lie_conjugation","theorem lie_conj "),("exponential_word","def pr "),
 ("smooth_family_deriv","theorem SmFam.deriv "),("smooth_zero","theorem smooth_zero "),
 ("smooth_add","theorem smooth_add "),("smooth_smul","theorem smooth_smul "),
 ("smooth_span","theorem smooth_span "),("smooth_action","theorem smooth_act "),
 ("smooth_derivative","theorem smooth_dRep "),("derivative_exists","theorem hasDerivAt_dRep "),
 ("smooth_word","theorem smooth_word ")]:
    add(sid,DP+"SmoothVectorsSubspaceStableSobolevFormDeriv.lean",anchor)
for sid,anchor in [("real_derived_linearity","theorem dRep_lin "),("complex_derived_linearity","theorem dRepC_lin "),
 ("complex_vector_linearity","theorem dRepC_vec "),("derived_bracket","theorem dRepC_bracket "),
 ("derived_covariance","theorem rep_dRepC "),("derived_adjoint","theorem inner_dRepC "),
 ("complete_derived_contract","theorem main ")]:
    add(sid,DP+"ComplexifiedDerivedActionIsLieAction.lean",anchor)
for sid,anchor in [("frame_group","theorem conj_mem "),("frame_rep_one","theorem rep_one "),
 ("frame_rep_mul","theorem rep_mul "),("span_is_smooth","theorem smooth_of_span "),
 ("ordered_action","theorem act_list "),("smooth_map","theorem smooth_map ")]:
    add(sid,DP+"EquivariantMultilinearMapsSmoothVectorsIntertwin.lean",anchor)
for sid,anchor in [("smooth_vector_adelic","def IsSmoothVector' "),("l2_derivative","def dL2 "),
 ("gelf_rep","def gelfRep "),("transvection_subgroup","def ZI "),("isotropic_vector","def IsoVec ")]:
    add(sid,DEF,anchor)
for sid,anchor in [("compact_orbit_bound","theorem exists_bound_orbit "),("local_integral_bound","theorem exists_lintegral_le "),
 ("average_bound","theorem lintegral_average_le "),("average_closure","theorem average_eq_zero_of_mem_closure "),
 ("cusp_closure","theorem zcusp_of_mem_closure ")]:
    add(sid,DP+"CuspidalityPreservedInClosure.lean",anchor)
add("transvection_group",DP+"AdelicTransvectionSubgroupEqAdelesClosed.lean","theorem transvection_group ")
add("compact_fundamental_domain",DP+"TransvectionSubgroupCocompactHaarFundamentalDoma.lean","theorem exists_fundamentalDomain_subset ")
add("transvection_measure",DP+"TransvectionSubgroupCocompactHaarFundamentalDoma.lean","theorem transvection_measure ")
for sid,anchor in [("operator_matrix","def opM "),("operator_frame","theorem opM_eq "),
 ("scalar_matrix_trace","theorem trace_map_mul "),("cyclic_frame_invariance","theorem trace_opM_pow "),
 ("matrix_unit_relations","theorem glRel_opM "),("operator_adjoint","theorem pow_adjoint "),
 ("derived_endomorphism","def dEnd "),("fold_order","theorem foldr_eq "),
 ("gelf_trace","theorem gelfRep_eq "),("orbit_density","theorem eq_zero_of_inner_orbit "),
 ("frame_nondegenerate","theorem orthFr_facts "),("gelf_scalar","theorem gelfRep_scalar ")]:
    add(sid,DP+"GelfandInvariantsActByScalarsHighestWeight.lean",anchor)
for sid,anchor in [("pointwise_word","theorem word_value "),("pointwise_complex_derivative","theorem rderC_value "),
 ("pointwise_complex_word","theorem wordC_value "),("pointwise_gelf","theorem gelf_value "),
 ("pointwise_zfin","theorem zfin_value "),("filtered_word","def lettersAt "),
 ("word_mem","theorem word_mem "),("word_map","theorem word_map ")]:
    add(sid,DP+"BoundedHolomorphicFormEqMultiplicitySpaceValue.lean",anchor)
for sid,anchor in [("pointwise_gelf_definition","def gelf "),("smooth_automorphic_contract","structure IsAutFunSm ")]:
    add(sid,BT+"TiedSmooth.lean",anchor)
add("automorphic_contract",BT+"IsAutFunDef.lean","structure IsAutFun ")
maps=[
 ["topology","adele_lc","adele_countable","rational_discrete","rational_zero_neighborhood"],
 ["finite_pair","quotient_measure_preserving","local_integral_bound"],
 ["global_ae","quotient_measure","original_representative"],
 ["right_translate","right_translate_law","quotient_measurable","translate_measurable","quotient_measure_preserving"],
 ["symmetric_difference","regular_continuity"],
 ["finite_pair","regular_representation","regular_map","regular_value","regular_norm","regular_continuity","regular_exists"],
 ["smooth_vector","real_derived_action","real_involution","complex_derived_action","lie_conjugation","smooth_family_deriv","smooth_zero","smooth_add","smooth_smul","smooth_span","smooth_action","smooth_derivative","derivative_exists","model_smooth_span"],
 ["real_derived_linearity","complex_derived_linearity","complex_vector_linearity","derived_bracket","derived_covariance","derived_adjoint","complete_derived_contract"],
 ["model","model_action","frame_group","frame_rep_one","frame_rep_mul","span_is_smooth","ordered_action","smooth_map","smooth_vector_adelic","l2_derivative"],
 ["filtered_word","word_mem","word_map","smooth_word","finite_eigenclass"],
 ["compact_orbit_bound","local_integral_bound","finite_pair","original_representative"],
 ["average_bound","local_integral_bound"],
 ["average_closure","regular_representation","original_representative"],
 ["transvection_subgroup","isotropic_vector","transvection_group","compact_fundamental_domain","transvection_measure"],
 ["cusp_closure","central_cuspidality","automorphic_contract"],
 ["actual_hilbert_map","finite_eigenclass","cusp_closure","automorphic_contract"],
 ["operator_matrix","operator_frame","scalar_matrix_trace","cyclic_frame_invariance","fold_order","gelf_trace","gelf_rep"],
 ["matrix_unit_relations","gelf_scalar","source_borel_extremal"],
 ["operator_adjoint","derived_covariance","derived_adjoint","cyclic_frame_invariance","gelf_scalar"],
 ["unitary_representation","irreducibility","original_frame","frame_nondegenerate","orbit_density","gelf_rep","gelf_scalar"],
 ["source_borel_extremal","actual_model_representation","pointwise_word","pointwise_complex_derivative","pointwise_complex_word","pointwise_gelf","pointwise_zfin","pointwise_gelf_definition","smooth_automorphic_contract"],
 ["actual_hilbert_map","bounded_holomorphic_form","finite_pair","full_multiplicity_extension","multiplicity_map_contract","remaining_smooth_representative","remaining_sobolev_growth","point_evaluation_continuity","remaining_boundedness","remaining_target_volume"]
]
deps=[
 [],["RQC1"],["RQC1","RQC2"],["RQC1","RQC2"],["RQC2","RQC4"],
 ["RQC3","RQC4","RQC5"],[],["RQC7"],["RQC7","HCU14"],
 ["RQC7","RQC9","HCU18"],["RQC1","RQC2"],["RQC11"],["RQC6","RQC12"],
 ["CTC1","RQC1","RQC2"],["RQC13","RQC14"],["HCU16","HCU18","RQC9","RQC10","RQC15","CTC12"],
 ["RQC8"],["RQC8","RQC17"],["RQC7","RQC8","RQC17","RQC18"],
 ["RQC18","RQC19"],["HCU12","RQC7","RQC20"],
 ["HCU16","HCU17","HCU18","RQC6","RQC9","RQC10","RQC16","RQC21"]
]
scopes=[
 "Every original D,V with its nondegenerate Gram matrix; actual module and unit-group topology; no finite-volume existence.",
 "Same supplied Haar measure, countable rational subgroup and null measurable fundamental domains; nonnegative and integrable complex functions.",
 "Same literal nuQ; quotient AE implies globally Haar AE after autMk.",
 "Every g on the same original quotient and finite pair, with unchanged measure scale.",
 "Every finite quotient-measurable indicator and then every L2 vector; exact symmetric-difference bound and norm continuity.",
 "Every supplied FinPair gives the complete original IsReg, including globally AE val; any IsReg on that quotient is identical.",
 "Every original exponential-word smooth vector in a unitary strongly continuous representation of a nonsingular Hermitian group; full span and derived stability.",
 "Every pair of original smooth vectors, every complex scalar and directions, every unitary element: full complexifiedDerivedAction_isLieAction contract.",
 "Exactly the original smooth_map target generality: any complex inner-product target and any monoid homomorphism into continuous linear operators; original IsInfFam and same DSModel, without extra target unitarity or continuity assumptions.",
 "Every original ordered real derivative word; filtered subsequences keep order and all derived tuples stay smooth; same finite laws when supplied by HCU18.",
 "Every compact K, same FinPair and every rational invariant representative; local L1 and L2 estimates.",
 "Every finite measure supported in compact K and every compact Omega; ordinary continuous functions before averaging.",
 "Every vector in the full closed regular orbit span, conditional on a supplied continuous rational invariant representative; no restriction of arbitrary L2 classes to subgroups.",
 "Every nonzero original isotropic vector and every Haar measure on the actual ZI; compactly contained Borel domain and invariance under arbitrary original fundamental-domain choice. The extra archimedean/finite factorization of transvection_measure is not newly claimed.",
 "Literal all-xi/all-Haar/all-domain/all-g ZCusp closure, for every same-quotient IsReg and supplied continuous rational invariant representatives.",
 "Same HCU18 map and seed, its actual full-adelic closed span and unchanged finite level/eigencharacter; conditional on representative existence.",
 "Every positive cyclic length, same right-fold operator convention, every invertible complex change of matrix frame; scalar-matrix trace interchange only.",
 "Every nonzero original smooth highest vector satisfying original Borel equations; produces a scalar polynomial without claiming a prescribed closed formula.",
 "All smooth pairs and all original unitary group elements; formal symmetry and covariance only, without self-adjoint extension claims.",
 "Every original OrthFr, irreducible unitary representation, nonzero smooth original Borel vector, integral weight and k; one scalar for all smooth vectors.",
 "Same original model with HolShape, WtIs and IsExtVec, and multilinear map with supplied pointwise real derivative identities; exact original gelf and one-dimensional zfin space.",
 "Same original bounded HolForm, FinPair, IsInfFam, HolShape, WtIs and IsExtVec; seed ZCusp additionally retained for every cusp conclusion. IsReg and post-Hilbert smooth/cusp/central implications proved; actual smooth representatives, Sobolev estimates, initial boundedness and target-volume production retained."
]
tex=(HERE/"main.tex").read_bytes();ls=tex.splitlines(keepends=True);claims=[]
for n in range(1,23):
    cid=f"RQC{n}";i=next(i for i,l in enumerate(ls) if l.strip()==f"% BEGIN {cid}".encode())
    j=next(i for i,l in enumerate(ls) if l.strip()==f"% END {cid}".encode())+1
    block=b"".join(ls[i:j]);title=next(l.decode().strip() for l in ls[i:j] if l.startswith(b"\\paragraph{"))[11:-1]
    claims.append({"id":cid,"title":title,"introduced_in":"0.36","classification":"B",
      "status":"complete independent human proof of the explicitly stated implication",
      "depends_on":deps[n-1],"quantifier_scope":scopes[n-1],
      "proof_location":{"file":"regular_quotient/main.tex","label":"claim:"+cid,"line_start":i+1,
       "line_end":j,"sha256":sha(block),"bytes":len(block)},
      "source_ids":maps[n-1],"sources":[sources[s] for s in maps[n-1]]})
inherited=[]
for rel,ids in [("holomorphic_uniqueness/main.tex",["HCU12","HCU14","HCU16","HCU17","HCU18"]),
                ("constant_terms/main.tex",["CTC1","CTC12"])]:
    b=(HUMAN/rel).read_bytes();lines=b.splitlines(keepends=True);blocks=[]
    for cid in ids:
        i=next(i for i,l in enumerate(lines) if l.strip()==f"% BEGIN {cid}".encode())
        j=next(i for i,l in enumerate(lines) if l.strip()==f"% END {cid}".encode())+1
        bb=b"".join(lines[i:j]);blocks.append({"id":cid,"line_start":i+1,"line_end":j,"sha256":sha(bb),"bytes":len(bb)})
    inherited.append({"file":rel,"sha256":sha(b),"file_sha256":sha(b),"role":"Actual inherited human-proof inputs, with incoming edges listed claim by claim","claims":blocks})
remaining=[
 {"id":"RQC_BOUNDEDNESS_AND_TARGET_VOLUME","classification":"C","status":"retained original analytic production",
  "contract":"Produce the original target FinPair and boundedness of the initial smooth cuspidal uniformly moderate extremal function. RQC uses these; its post-Hilbert scalar proof cannot supply earlier boundedness.",
  "source_ids":["remaining_boundedness","remaining_target_volume","finite_pair"],"not_new_independent_top_level_obligation":True},
 {"id":"RQC_SMOOTH_REPRESENTATIVES_AND_SOBOLEV","classification":"C","status":"retained exact pointwise production",
  "contract":"For every original smooth fixed-finite-level Hilbert class construct its same-quotient continuous smooth representative and every globally AE derivative representative. Produce one N and finite list S before x,F,psi in sobolev_bound_for_smooth_vectors, then Sobolev-continuous evaluation and uniform moderate growth for the same original MMap.",
  "source_ids":["remaining_smooth_representative","remaining_sobolev_growth","point_evaluation_continuity","full_multiplicity_extension","multiplicity_map_contract"],"not_new_independent_top_level_obligation":True}
]
prov={"schema":"rh-human-component-provenance/1","artifact_version":"0.36","date":"2026-11-22",
 "component":"regular_quotient","source_commit":PIN,"main_tex_sha256":sha(tex),
 "metadata_builder":{"file":"build_metadata.py","sha256":sha(Path(__file__).read_bytes()),
 "portable_invocation":"python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction"},
 "claims":claims,"source_inventory":list(sources.values()),"baseline_dependencies":inherited,
 "remaining_producer_contracts":remaining,
 "validation":{"source_commit_verified":True,"pinned_blob_verified_files":len(cache),"source_ranges":len(sources),
 "claim_source_occurrences":sum(map(len,maps)),"all_source_ranges_exact":True,"new_lean_build":False,
 "tex_validation":"Standalone and cumulative draft-mode syntax checks only; see validation records."},
 "scope_note":"Complete original IsReg, smooth_map, cusp-closure and gelfRep_scalar suppliers. The finite pair and initial boundedness remain inputs; no actual pointwise representative or Sobolev estimate is claimed."}
(HERE/"provenance.json").write_text(json.dumps(prov,indent=2,ensure_ascii=False)+"\n")
closure={"schema":"rh-component-closure/1","version":"0.36","component":"regular_quotient","source_commit":PIN,
 "main_tex_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),
 "new_claims":[c["id"] for c in claims],"claim_count":22,"class_counts":{"A":0,"B":22,"C":0,"D":0},
 "all_new_claims_are_conditional_implications":True,
 "closed_subtargets":[
 {"source_declaration":"adelic_unitary_topology","proof":["RQC1"]},
 {"source_declaration":"QuotRegular.exists_isReg","proof":["RQC1","RQC2","RQC3","RQC4","RQC5","RQC6"]},
 {"source_declaration":"complexifiedDerivedAction_isLieAction","proof":["RQC7","RQC8"]},
 {"source_declaration":"SmoothMultilinear.smooth_map","proof":["RQC9"]},
 {"source_declaration":"BackForm.word_mem and word_map","proof":["RQC10"]},
 {"source_declaration":"ZClosed.zcusp_of_mem_closure","proof":["RQC11","RQC12","RQC13","RQC14","RQC15"]},
 {"source_declaration":"GelfScalar.gelfRep_scalar","proof":["RQC17","RQC18","RQC19","RQC20"]},
 {"source_declaration":"BackForm.rderC_value, wordC_value, gelf_value and zfin_value","scope":"same supplied pointwise multilinear map with its real derivative identities","proof":["RQC21"]}
 ],
 "closed_prior_residues":[
 {"id":"HCU_REGULAR_REPRESENTATION_EXISTENCE","status":"closed on the same supplied FinPair","proof":["RQC6"]},
 {"id":"HCU_POINTWISE_AUTOMORPHIC_REALIZATION","status":"strict partial refinement",
  "closed":"Full Hilbert smoothness/derivative words, actual cusp-closure producer, original Gelfand scalar producer, conditional pointwise finite laws/cusp/central fields",
  "remaining":"actual smooth representatives with pointwise derivative identities, Sobolev-continuous evaluation and uniform moderate growth",
  "proof":["RQC9","RQC10","RQC15","RQC16","RQC20","RQC21","RQC22"]}],
 "remaining_producer_contracts":remaining,"selected_top_level_leaf_closed":False,
 "same_object_guards":["unchanged FinPair and nuQ normalization","global Repr AE on all GA","original atTau and frame action","ordered derivative words and one unchanged finite level","every original ZI/Haar/domain","exact k+1 cyclic gelf normalization","no pre-Hilbert boundedness inferred from post-Hilbert scalar action"]}
(HERE/"closure.json").write_text(json.dumps(closure,indent=2,ensure_ascii=False)+"\n")
(HERE/"source_locators.txt").write_text("\n".join(f'{s["id"]}: {s["path"]}:{s["line_start"]}-{s["line_end"]} [{s["range_sha256"]}]\n{s["url"]}' for s in sources.values())+"\n")
print(json.dumps({"claims":22,"source_files":len(cache),"ranges":len(sources),"claim_source_references":sum(map(len,maps)),
 "main_sha256":sha(tex),"provenance_sha256":sha((HERE/"provenance.json").read_bytes()),"closure_sha256":sha((HERE/"closure.json").read_bytes())},indent=2))

