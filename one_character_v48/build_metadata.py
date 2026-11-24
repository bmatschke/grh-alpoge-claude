#!/usr/bin/env python3
"""Rebuild only the v0.48 OneChar component, from immutable source and human proofs."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION='0.48'; PREFIX='OCH'; COMPONENT=HERE.name
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
repo=ap.parse_args().repo.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
B='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P=B+'PadicHodgeTheory/'; C=B+'ModularityArgument/CrystallineOrdinaryIdeals/'
U=B+'UnitaryThreeGroups/'; Z=B+'ModularityArgument/KatoQuadraticCharacters/'
A=B+'AutomorphicForms/'; H=B+'HeightAndVanishing/'
# Each named range is inclusive and checked against the exact pinned git blob.
# Entire-file ranges are used only when the reconstructed producer uses its chain of helpers.
specs={
 'gd':(H+'Counts.lean',9,22,'All original GD guards, including e>=1 and the exact residual genericity condition'),
 'cohinp':(U+'KatoUse.lean',19,24,'The unchanged five-field CohInp foundation'),
 'inpz':(Z+'KatoTwoOfUseN.lean',55,61,'The exact InpZ record already supplied by KIZ2'),
 'onechar':(U+'KatoUse.lean',54,64,'Complete original OneChar contract on every coefficient datum and fixed complex bridge'),
 'aut_unram':(B+'AutomorphicCases/AutomorphyUnramifiedCoefficients.lean',12,27,'FinA, AutB, LemW and their one-joint-marked-element unramified-coefficient producer'),
 'onechar_transfer':(Z+'OneChar.lean',23,100,'Injective coefficient transport, unramified realization, actual point push and base trace'),
 'onechar_unram':(Z+'OneChar.lean',102,156,'The original same-object unramified-coefficient OneChar consumer'),
 'onechar_original':(Z+'OneChar.lean',158,178,'The exact full oneChar implication and return to the original coefficients'),
 'local_data':(P+'IsInertiaInfiniteCyclotomic.lean',11,85,'Dat3, HL, actual crystalline/ordinary deformation predicates and chosen inertia/Frobenius'),
 'local_ideals':(P+'IsInertiaInfiniteCyclotomic.lean',87,183,'The literal cc, tr, dd, del, ordinary ideal, saturation, It and all point predicates'),
 'positive_periods':(P+'PosExact.lean',227,683,'Positive-character Frobenius no-fixed-vector and exact finite-cocycle construction'),
 'positive_change':(P+'TorsionDatumFiniteCocyclesBaseChange.lean',1,None,'Finite coefficient change for positive crystalline cocycles'),
 'positive_compare':(P+'TorsionDatumFiniteCocyclesCompare.lean',1,None,'Exact finite-cocycle comparison on filtered positive modules'),
 'annihilator':(C+'CocycleCrysAddAnn.lean',1,None,'Actual finite-cocycle plus cyclotomic-annihilator decomposition'),
 'dimension':(C+'FinrankCocyclesEqCrysAddDualInvOfPositive.lean',1,None,'The exact positive Z1/Zf1 dimension difference'),
 'annihilator_compare':(C+'CocycleMemCrystallineSupSubrepOfPositive.lean',1,None,'Surjectivity of the annihilator subrepresentation in the nonfinite cocycle quotient'),
 'tri_lift':(P+'TriLift.lean',1,None,'Actual triangular lifts, their central obstruction and exact reduction adjustment'),
 'tri_crys':(C+'TriCrys.lean',1,None,'Last-column crystalline criterion for the actual triangular rank-three representation'),
 'tri_push':(C+'TriangularRankThreeCrystallineAfterPush.lean',1,None,'Annihilator-killing push makes the actual triangular rank-three representation crystalline'),
 'ordinary_induction':(P+'ExistsEps.lean',1,None,'Socle-line/fibre-product induction proving ordEq at every finite Artin algebra'),
 'ordinary_dual':(P+'OrdDual.lean',1,None,'Negative-weight finite-cocycle elimination in the actual dual-number deformation'),
 'cr_lift':(P+'CrLift.lean',1,None,'Full crystalline small-extension lifting after ordinary conjugation'),
 'artin_rees':(C+'ExistsFiniteLocalLiftOfSaturatedIdeal.lean',1,None,'Actual finite local thickening killing the saturated annihilator, via Artin--Rees'),
 'saturated_point':(C+'IsLCrystallinePointOfSaturatedOrdIdeal.lean',1,None,'Every finite local saturated-ideal point is crystalline'),
 'finite_targets':(C+'SaturatedOrdIdealPointsIsLCrystalline.lean',1,None,'All finite-algebra targets, including their product/local decomposition'),
 'crys_ann_ideal':(C+'CrystallineDeformationPointsSaturatedOrdinaryIde.lean',1,None,'Crystalline ordinary points annihilate the saturated ideal through the actual base'),
 'truncated_square':(C+'ExistsTruncatedPolynomialThickeningFibreSquareStatement.lean',1,None,'Actual truncated polynomial fibre square and nilpotent cancellation'),
 'twist_saturation':(C+'SaturatingElementUnramifiedTwistEqPowMulUnit.lean',1,None,'Unramified formal twist makes del a power t^j times a unit with j<=2'),
 'artin_residue':(C+'CrystallinePointsSaturatedOrdinaryIdealArtinian.lean',1,None,'Original Artin coefficient/reduction field scope of the reverse crystalline implication'),
 'local_equality':(C+'SaturatedOrdinaryIdealCutsOutCrystallineLocus.lean',1,None,'Both directions of the exact local crystalline locus equality'),
 'local_prime':(C+'OrdinaryLocusIdealLeKerOfIsBasePoint.lean',1,None,'The unique minimal prime through the base and its integral contraction'),
 'local_completion':(C+'RtCompl.lean',1,None,'The original twelve-variable completed ordinary component'),
 'tangent_twelve':(C+'SaturatedOrdinaryIdealTangentFinrankEqTwelve.lean',1,None,'Exact tangent dimension twelve for the specified saturated ordinary ideal'),
 'local_weights':(P+'DimZ1fCrystallineDeformation.lean',1,None,'Finite adjoint tangent dimensions in all five matrix weights'),
 'local_chart':(P+'RtChart.lean',1,None,'Actual weighted local chart from entry coordinates'),
 'locgood_original':(P+'LocGood.lean',93,124,'Full original LocGood endpoint with linear surjectivity and scalar-cleared injection'),
 'conjugation':(C+'ExistsConjLift.lean',1,None,'Universal formal near-identity conjugation and minimal-prime preservation'),
 'full_inertia':(P+'ScalarMap.lean',157,193,'The actual chart gives full-inertia characteristic and ordered-product identities'),
 'ordered_flag':(P+'CommutingUpperTriangularDistinct.lean',15,167,'Actual ordered inertia projectors and normality under the decomposition group'),
 'dat':(U+'RhoKApply.lean',16,94,'Original Dat, ULoc, Ring, Marked, IsPt, rhoK, IsExt, IsAutI and IsModular'),
 'exists_dat':(U+'ExistsDat.lean',1,None,'Construction of all fields of the actual Dat from GD'),
 'dat_local':(U+'DatLoc.lean',1,None,'The specified embedding identifies decomposition and inertia groups'),
 'dat_facts':(U+'DatFacts.lean',1,None,'Original residual, killed-inertia and inertia-unit consequences of GD'),
 'local_universal':(U+'ULocEx.lean',1,None,'Actual local universal lift from local finite-cohomology and Phi'),
 'global_ring':(U+'RingEx.lean',1,None,'Actual normalized global ring and its universal property for every original target'),
 'global_predicates':(U+'GRepresents.lean',19,171,'The original representation, entry algebra, push, tangent, rigidity and strict local point predicates'),
 'local_contract':(U+'ConjStable.lean',15,37,'Literal ConjStable, locDims, LocChart and LocGood fields'),
 'model_contract':(U+'ConjStable.lean',49,90,'All fields of the actual graded Model and its length'),
 'points_sha_contract':(U+'ConjStable.lean',94,112,'Original TwoPt, CoversPt, trDiff and shaCoc predicates'),
 'box_contract':(U+'IsLocPres.lean',9,41,'Exact local-presentation and five-weight BoxPres count contract'),
 'box_absolute':(U+'BoxAbs.lean',1,None,'Specialization of the actual framed presentation to the box quotient'),
 'box_count':(U+'BoxPresOf.lean',1,None,'The complete relative presentation and Euler-weight count'),
 'global_dual_zero':(U+'ExistsGaloisCyclotomicNegOneTrivialOnEtaPsi.lean',1,None,'Actual GD.eta element kills all residual Tate-dual invariants'),
 'normalizations':(U+'MopBase.lean',1,None,'Eight actual normalization equations and their exact weights'),
 'model_presentation':(U+'ModelOfPres.lean',23,329,'Actual weighted integral presentation, numerical dimensions, model maps and full model_of_pres'),
 'model_exists':(U+'ModelEx.lean',156,178,'Complete original exists_model with unchanged CohInp and LemmaP antecedents'),
 'model_finite':(U+'ModelIdealFinitenessOfWeightZeroFinite.lean',1,None,'FinA gives the finite quotient weight-zero module M2'),
 'model_points':(U+'ExistsTorusTwistEqLocalPointOfWeightedPres.lean',1,None,'Actual torus rescaling, convergent evaluation and the all-points field'),
 'model_derivations':(U+'ExistsDualNumberPointOfPointDerivationVanishing.lean',1,None,'Actual all-derivations extension through the complete normalized ring'),
 'actual_points':(U+'IsPtOf.lean',1,None,'All literal IsPt fields of a strict local point of the normalized ring'),
 'point_shape':(U+'PtShape.lean',85,171,'Type-I/type-II alternatives and actual torus conjugacy from an intertwiner'),
 'coordinate_shape':(U+'ExistsCoordOfNotMatIrr.lean',1,None,'Ordered marked eigenvalues force invariant coordinate subspaces and exact six cases'),
 'torus_intertwiner':(U+'FreeEtaleSheafZmodExistsHomSendingGenerator.lean',1,None,'The actual diagonal intertwiner and the square-root outer-block case'),
 'fixed_point':(U+'RootOfCharpoly.lean',1,None,'Exact inertia root matching, class-group argument and pt_fixed'),
 'inertia_away':(U+'PtInertiaAway.lean',1,None,'Actual finite prime-to-ell averaging conjugacy on inertia'),
 'inertia_ell':(U+'PtIneL.lean',1,None,'All ell-place ordered inertia conditions and potential crystallinity'),
 'typeI_cyclo':(U+'TypeIIrrCyc.lean',1,None,'Full infinite-cyclotomic-kernel irreducibility for the original type-I point'),
 'clifford':(U+'Clifford.lean',1,None,'Elementary normal-subgroup semisimplicity and abelian-quotient self-twist producer'),
 'base_rigidity':(U+'BlochKatoNonpositiveWeight.lean',194,414,'Negative and zero matrix-weight global finite-cohomology vanishing'),
 'tangent_BK':(U+'TanCocIsBK.lean',1,None,'Actual normalized tangent cocycle, finite coefficient continuity and all local primitives'),
 'normal_cob':(U+'NormCob.lean',1,None,'Exact normalized coboundary primitive equals a scalar diagonal(1,0,-1)'),
 'typeI_rigidity':(U+'LiftingTheory.lean',40,84,'Exact polarized type-I AdVanishK application with epsilon^-1 twist'),
 'point_hypotheses':(U+'Rigid0.lean',9,22,'Literal PtHyp and each of its three original fields'),
 'point_hyp_producer':(Z+'MapReducibleThreeDim.lean',64,89,'Complete original ptHyp_of implication on the same actual ring'),
 'adm_contract':(A+'CongruenceNumberRankThree.lean',33,44,'Original cyclotomic-weight and LevelO clauses'),
 'adm_ranks':(A+'CongruenceNumberRankThree.lean',103,119,'All exact Adm3 and Adm2 fields, weights and direct-sum isomorphism'),
 'adk_contract':(A+'CongruenceNumberRankThree.lean',158,175,'Original full polarized adjoint action and AdVanishK'),
 'adm_three':(U+'ExistsFlagCharactersOfUpperTriangular.lean',1,None,'Actual all-place ordered flags and complete rank-three admissibility'),
 'adm_two':(U+'AdmissibleOfTypeII.lean',1,None,'Actual type-II extension, conductor allowance and complete rank-two admissibility'),
 'sha_normalization':(U+'ShaInjGen.lean',1,None,'Full canonical normalized torsion-Selmer cocycle and its additive injection'),
 'sha_injection':(U+'ShaInj.lean',13,37,'Original shaFam(ell*N) local placement and literal sha_inj'),
 'model_lower':(U+'ModelLower.lean',296,401,'Actual square-zero ring, map and integral lift into the lower length comparison'),
 'vlen_lower':(U+'VlenLe.lean',13,67,'Full original vlen_le before finiteness, via the union of torsion layers'),
 'vlen_norm':(H+'DirichletPrimeToLPartMulLPowerPart.lean',103,118,'Original Vlen and normalized Vn with exact level ell*N'),
 'model_M1':(U+'GradedModelSpansCotOfRigidWeights.lean',1,None,'Actual rational cotangent spanning from normalized nonpositive-weight rigidity'),
 'model_M3':(U+'GradedModelPointConditionOfPtHyp.lean',1,None,'Actual fixed-point condition for the graded model'),
 'model_M4':(U+'GradedModelDerivationConditionOfPtHyp.lean',1,None,'The exact dimension-one point derivation condition on the same model'),
 'model_upper':(U+'ModelUpper.lean',103,250,'Every-cover valuation inequality and actual irredundant point-orbit cover'),
 'length_contract':(B+'CommutativeAlgebra/OrbitVanishingLocal.lean',9,128,'All M1--M5, count, valuation, LemmaM and LemmaM-prime contracts'),
 'coefficient_independence':(H+'CoefIndep.lean',1,None,'Original full coefficient-independence and normalized-length equality target'),
}
relations={
 1:(['BX1','BX5','KTR1'],['local_data','positive_periods','positive_change','positive_compare']),
 2:([1,'BX8'],['annihilator','dimension','annihilator_compare']),
 3:([1,2,'BX5','BX8'],['local_data','tri_lift','tri_crys']),
 4:([3,'BX5'],['ordinary_dual','ordinary_induction','cr_lift']),
 5:([2,3],['local_ideals','artin_rees','tri_push','saturated_point','finite_targets','ordered_flag']),
 6:([4,'BX5'],['local_ideals','crys_ann_ideal','truncated_square','twist_saturation','artin_residue']),
 7:([4,5,6,'BX5'],['local_equality','local_prime','local_completion','tangent_twelve','local_weights','local_chart','locgood_original','local_contract']),
 8:([7],['conjugation','local_contract','local_ideals']),
 9:(['FP2','DX1'],['gd','dat','exists_dat','dat_local','dat_facts','local_universal','global_ring','global_predicates','normalizations']),
 10:([9,'FP8','DX3'],['box_contract','box_absolute','box_count','global_dual_zero','normalizations']),
 11:([7,10],['model_contract','model_presentation','length_contract','normalizations']),
 12:([11],['aut_unram','model_finite','model_points','model_contract']),
 13:([11,12],['model_derivations','model_contract']),
 14:([11,12,13,'FP8'],['model_presentation','model_exists','model_contract']),
 15:([4,5,7,9],['actual_points','dat','inertia_away','full_inertia','ordered_flag','inertia_ell','tangent_BK']),
 16:([9,15],['point_shape','coordinate_shape','torus_intertwiner','points_sha_contract']),
 17:([15],['fixed_point','dat_facts','gd']),
 18:([15],['typeI_cyclo','clifford','dat_local']),
 19:(['KTR1','BX5','BX7','RV7'],['base_rigidity','point_hypotheses']),
 20:([9,15,'KTR1'],['tangent_BK','normal_cob','normalizations','global_predicates']),
 21:([16,17,18,19,20,'ADK6','KTR4','KTR5','KTR6','KTR7','KTR8','KTR13','KIZ2'],['aut_unram','point_hypotheses','point_hyp_producer','typeI_rigidity','adk_contract','inpz']),
 22:([15,16,'KTR5','KTR6','KTR7'],['aut_unram','adm_contract','adm_ranks','adm_three','adm_two','dat']),
 23:([9],['sha_normalization','sha_injection','points_sha_contract','dat_facts']),
 24:([8,9,11,14],['model_lower','points_sha_contract','model_contract']),
 25:([23,24,'SP1','RV1'],['vlen_lower','model_lower','length_contract','vlen_norm']),
 26:([11,12,13,20],['model_M1','model_M3','model_M4','length_contract','point_hypotheses','model_upper']),
 27:([12,26,'SP6'],['model_upper','points_sha_contract','length_contract']),
 28:([9,14,16,21,22,25,27],['onechar_unram','onechar','aut_unram','vlen_norm']),
 29:([],['onechar_transfer','gd']),
 30:([28,29,'RV7','KIZ2'],['onechar_original','onechar','coefficient_independence','inpz','aut_unram']),
}
external=[
 {'id':'OCH_ORIGINAL_AUT_UNRAM_COEF','kind':'retained_original_selected_antecedent','title':'The exact AutomorphyUnramifiedCoefficients premise','source_keys':['aut_unram'],'scope':'For every original Dat with eO=1 and fixed iota, one marked g1 jointly supplies FinA, AutB and LemW, on every original local/global universal ring and every original IsPush. LemW retains its universal quantifier over every actual IsExt. This producer is not supplied in this packet. Local uses of FinA, AutB or LemW assume only their explicitly stated field; OCH28 obtains them together from this one original premise.','newly_reconstructed_here':False,'selected_frontier_id':'AUT_UNRAM_COEF'},
 {'id':'OCH_INHERITED_PERIOD_AND_COHOMOLOGY','kind':'inherited_named_foundations','title':'The original tied periods, finite local duality, global finiteness and normalized global cohomology','human_endpoints':['BX1','BX5','BX7','BX8','DX1','DX3','KIZ1','KTR1'],'registry_files':['bloch_kato_installation/classical_inputs.json','symplectic_local_installation/classical_inputs.json','kato_input_assembly_v47/retained_foundations.json'],'scope':'All original tied period presentations and actual Bcris kernels; finite-dimensional and finite-Artin coefficient realization; local Euler/Tate and finite global Galois cohomology. Positive exactness, the saturated ordinary component, its chart, conjugation stability and its concrete global model are proved here, rather than assumed as a crystalline deformation-ring theorem.','newly_reconstructed_here':False},
 {'id':'OCH_INHERITED_RIGIDITY_AND_LENGTH','kind':'inherited_named_foundations','title':'Already reconstructed Kato/adjoint rigidity, strict rank-one cohomology and generic M/M-prime/P theorems','human_endpoints':['KTR13','ADK6','RV1','RV7','SP1','SP6','FP2','FP8','KIZ2'],'registry_files':['type_ii_rigidity_v47/classical_inputs.json','conditional_main_v42/contracts.json','rank_one_cohomology/provenance.json','symplectic_count_closure/classical_inputs.json','framed_deformation_presentation/classical_inputs.json'],'scope':'Exact original modularity premise and polarized full adjoint, no change to the infinite cyclotomic kernel; original strict Selmer local-family and normalized coefficient-independence; literal generic weighted-model length and framed presentation inputs, with every arithmetic antecedent checked in OCH.','newly_reconstructed_here':False},
 {'id':'OCH_CLASS_FIELD_AND_LOCAL_FIELD_BACKGROUND','kind':'retained_standard_classical_foundation','title':'Original class-field and elementary local-field background','source_keys':['dat_facts','fixed_point','typeI_cyclo','base_rigidity','onechar_transfer'],'scope':'Unramified abelian characters factor through the ideal class group; cyclotomic local extensions are totally ramified and inertia surjects at every finite level; Hensel lifting of roots of unity of order prime to ell in the original unramified coefficient datum. All usages retain the exact GD hypotheses and chosen algebraic closures.','newly_reconstructed_here':False},
 {'id':'OCH_STANDARD_COMMUTATIVE_ALGEBRA','kind':'retained_standard_foundation','title':'Complete Noetherian local algebra, Artin--Rees and finite-dimensional linear algebra','source_keys':['artin_rees','local_prime','model_presentation','length_contract'],'scope':'Artin--Rees, faithful flatness of Noetherian local completion, Nakayama, finite module boundedness over a complete DVR, convergent formal Taylor division at small integral points, and elementary graded-monomial finite generation. Their actual constructions and role in each OCH application are spelled out in the proof. No additional model, chart, point-rigidity, finiteness or automorphy producer is postulated.','newly_reconstructed_here':False}
]
ext_uses={i:['OCH_STANDARD_COMMUTATIVE_ALGEBRA'] for i in relations}
for i in list(range(1,11))+[15,19,20,23,24,25]:ext_uses[i].append('OCH_INHERITED_PERIOD_AND_COHOMOLOGY')
for i in [10,14,19,21,22,25,26,27,28,30]:ext_uses[i].append('OCH_INHERITED_RIGIDITY_AND_LENGTH')
for i in [12,21,22,26,28,30]:ext_uses[i].append('OCH_ORIGINAL_AUT_UNRAM_COEF')
for i in [9,15,17,18,19,22,29,30]:ext_uses[i].append('OCH_CLASS_FIELD_AND_LOCAL_FIELD_BACKGROUND')
subcontracts=[
 (1,'positive_finite_cocycle_exactness'),(2,'cyclotomic_annihilator_obstruction'),(3,'all_artin_triangular_lifts'),(4,'actual_ordinary_conjugacy_and_formal_smoothness'),(5,'all_finite_targets_saturated_points_are_crystalline'),(6,'critical_and_noncritical_crystalline_points_annihilate_same_ideal'),(7,'literal_It_and_twelve_variable_weighted_chart'),(8,'complete_original_LocGood'),(9,'actual_Dat_ULoc_and_normalized_global_ring'),(10,'literal_BoxPres_and_exact_weight_counts'),(11,'actual_integral_graded_presentation_and_structural_model_fields'),(12,'finite_quotient_weight_zero_and_all_graded_points'),(13,'all_point_derivations_extend'),(14,'integral_weight_minus_one_lift_and_complete_Model'),(15,'full_original_IsPt_and_all_place_inertia'),(16,'type_I_type_II_shapes_and_actual_torus_orbits'),(17,'exact_fixed_point'),(18,'full_infinite_cyclotomic_irreducibility'),(19,'all_nonpositive_base_weights_rigid'),(20,'all_normalized_tangents_are_BK_and_primitive_is_H0'),(21,'literal_PtHyp_on_the_same_ring'),(22,'every_actual_two_sided_point_is_Adm3_or_Adm2'),(23,'actual_normalized_torsion_Sha_injection'),(24,'actual_square_zero_deformations_and_integral_derivation_lift'),(25,'original_Vlen_lower_bound_before_finiteness'),(26,'all_M1_M5_on_same_model'),(27,'finite_irredundant_actual_orbits_and_every_cover_valuation_bound'),(28,'literal_unramified_coefficient_OneChar'),(29,'same_character_values_in_an_unramified_coefficient_datum'),(30,'complete_original_OneChar_implication')]
config={
 'component':COMPONENT,'prefix':PREFIX,'endpoint_claim':'OCH30','original_endpoint':'UpperTheory.V.Z.Kato.oneChar : InpZ -> AutomorphyUnramifiedCoefficients -> UpperTheory.V.U3.OneChar',
 'additional_original_endpoints':['UpperTheory.V.Loc.locGood','UpperTheory.V.U3.exists_model','UpperTheory.V.Z.Kato.ptHyp_of','UpperTheory.V.U3.sha_inj','UpperTheory.V.U3.vlen_le','UpperTheory.V.U3.model_upper'],
 'subcontracts':[{'id':n,'claim':'OCH'+str(i)} for i,n in subcontracts],
 'hypotheses':['Exact InpZ, supplied by KIZ2 with its explicitly retained foundations.','Exact AutomorphyUnramifiedCoefficients remains the independent selected AUT_UNRAM_COEF antecedent; one g1 supplies all three fields together.','Every original algebraic closure Omega/Q and K, CM K with its supplied embedding and closure structure, prime ell, original Coef ell, N!=0, e, psi and the full GD predicate.','The original fixed iota:Qbar_ell~C, sigma in G_K, given exact base trace t, and trace nonvanishing on every original Adm3(iota,e,N) or Adm2(iota,e,N*abs(disc K)) representation.'],
 'quantifier_order':['the exact InpZ and original AutomorphyUnramifiedCoefficients inputs','every original closure, CM field, prime, supplied coefficient datum, N,e,psi and GD','the fixed iota, sigma, t and original universal trace-nonvanishing premise','same-valued unramified coefficient realization','one joint marked g1, then actual local and global universal rings and their model','finite length and one irredundant finite set of actual original admissible representation maps','return to the original coefficient datum with the same iota, sigma,t and representation set'],
 'original_GD_fields':{'ell_odd':'ell!=2','e_pos':'1<=e','N_even':'Even N','ord':'ell does not divide orderOf psi','ine':'comp ell psi squared is one','par':'PsiEven e psi','quad':'[K:Q]=2','imag':'K totally complex','ell_cop':'ell does not divide abs(disc K)*classNumber K','cop':'abs(disc K) coprime to N','eta':'ker(cycMod ell,1) intersect ker(dirG(chiP ell psi)) is not contained in G_K','gen':'ell-1 does not divide2e'},
 'small_prime_scope':'No additional lower bound on ell or e is imposed. Local Dat3 constructions include ell=3 and e=1 wherever their original hypotheses allow them; the full GD predicate itself excludes ell=3 through its unchanged gen field. Critical e=1 saturation is proved by explicit truncated polynomial cancellation.',
 'normalizations':{'group':'GL3 semidirect {+1,-1}, theta(A)=J A^-t J; disconnected adjoint -J X^t J','base':'diag(Psi,1,Psi^-1), Psi=epsilon^e psi, weights(1,0,-1)','local_chart':'weight multiplicities(-2,-1,0,1,2)=(1,2,3,4,2)','relative_counts':'b_j=a_j+1 for |j|<=1 and b_j=a_j otherwise','model_counts':'r=a_-1+2,s=a_-2+1,rprime=a_1+3,sprime=a_2+1,m=a_0+3; ambient(s,r,m,rprime+1,sprime+1), equations(s,r+1,m,rprime,sprime)','local_ideal':'literal saturated IY=Iord:(ell*dd0*dd1)^infinity and original It; no replacement crystalline component','typeI_adjoint':'rho_K*epsilon^-1 has pairing J and multiplier epsilon^-2=epsilon^(1-3)','Selmer':'alpha=Psi^-1; exact shaFam(ell*N); inject a normalized representative as u(E10-E21)','length':'Vlen in N union infinity first; Vn=length/eO only after finite upper bound','valuation':'v_ell(ell)=1, use eO*v_ell for the generic length theorem; final factor2 unchanged'},
 'not_claimed':['AUT_UNRAM_COEF or any of its actual automorphy/finite-entry producers','A new local p-adic Hodge or global cohomology foundation beyond the recorded original ones','Unconditional OneChar without its exact original automorphy premise','All arithmetic installation inputs or RH/GRH completion'],
 'report':'OCH1--OCH30 reconstruct the complete original oneChar implication. The local component is proved explicitly: positive cocycle exactness, the cyclotomic-annihilator exceptional direction, nilpotent triangular lifts, ordinary conjugacy, Artin--Rees thickening, critical truncated-twist cancellation, the literal twelve-variable It chart, and all-target conjugation stability. The actual universal global ring and integral graded model retain every entry, normalization, weight count and all points/derivations/lifts. Exact point shapes, all-place inertia, full infinite-cyclotomic irreducibility, polarized adjoint rigidity and original admissibility feed the same model. The normalized Selmer injection produces actual square-zero deformations and the original lower bound before finiteness. The generic upper bound is reapplied to the final irredundant cover. Same-valued unramified coefficient realization and RV7 then return the identical finite representation set and normalized inequality to the supplied coefficient datum. The sole separate selected antecedent AUT_UNRAM_COEF remains open. No frozen proof or shared metadata is edited.'
}
# These references identify constructions, later completions or original boundaries,
# rather than use a later theorem conclusion as an earlier premise.
nonpremise={
 'OCH11':[{'reference':'OCH12--OCH14','reason':'Forward reference to the three fields not asserted in OCH11; OCH11 proves the structural presentation only. OCH14 assembles the full Model after those fields are proved.'}],
 'OCH26':[{'reference':'SP6','reason':'Only the definitions of its original M1--M5 antecedents are being identified here. OCH26 proves those antecedents from its stated FinA and PtHyp hypotheses. The conclusion of SP6 is first applied in OCH27, where it is an explicit dependency.'}],
}

def build():
 files={};sources={};excerpts=[]
 for key,(rel,start,end,title) in specs.items():
  data=(repo/rel).read_bytes();pinned=subprocess.check_output(['git','show',PIN+':'+rel],cwd=repo);assert data==pinned,rel
  ls=data.splitlines(keepends=True);end=end or len(ls);assert 1<=start<=end<=len(ls),(rel,start,end,len(ls))
  block=b''.join(ls[start-1:end]);url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
  files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(ls),'verified_equal_to_pinned_git_blob':True,'url':url}
  sources[key]={'id':PREFIX+'_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':start,'line_end':end,'source_commit':PIN,'full_file_sha256':sha(data),'file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
  excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())
 txt=(HERE/'main.tex').read_text();main_sha=sha(txt.encode());lookup={}
 for m in re.finditer(r'% BEGIN (OCH\d+)\n.*?% END \1\n',txt,re.S):
  lookup[m.group(1)]={'claim':m.group(1),'file':COMPONENT+'/main.tex','file_sha256':main_sha,'claim_sha256':sha(m.group().encode()),'line_start':txt[:m.start()].count('\n')+1,'line_end':txt[:m.end()].count('\n')}
 baseline=ROOT/'history/version_0_47/provenance.json'; ledger=json.loads(baseline.read_text());old={x['id']:x for x in ledger['claims']}
 inherited_ids={d for ds,_ in relations.values() for d in ds if isinstance(d,str)}
 for cid in inherited_ids:
  r=old[cid];loc=r['proof_location'];f=ROOT/loc['file'];data=f.read_bytes();block=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);assert sha(block)==loc['sha256'],cid
  lookup[cid]={'claim':cid,'file':loc['file'],'file_sha256':sha(data),'claim_sha256':sha(block),'line_start':loc['line_start'],'line_end':loc['line_end'],'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False}
 local={PREFIX+str(i) for i in relations};assert set(lookup)-inherited_ids==local
 claims=[]
 for i,(deps,ss) in relations.items():
  cid=PREFIX+str(i);m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert m,cid
  ds=[PREFIX+str(d) if isinstance(d,int) else d for d in deps];assert set(ds)<=set(lookup),(cid,set(ds)-set(lookup))
  start=txt[:m.start()].count('\n')+1
  claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),'introduced_in':VERSION,'classification':'B','depends_on':ds,'external_input_ids':ext_uses[i],'published_input_ids':[],'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},'sources':[sources[k] for k in ss],'source_proof_is_not_human_proof':True})
  if cid in nonpremise:claims[-1]['non_premise_reference_explanations']=nonpremise[cid]
 # Verify the local DAG directly; external numbered human dependencies remain immutable.
 edges={x['id']:[d for d in x['depends_on'] if d in local] for x in claims};done=set();active=set()
 def visit(cid):
  assert cid not in active,('dependency cycle',cid)
  if cid in done:return
  active.add(cid)
  for d in edges[cid]:visit(d)
  active.remove(cid);done.add(cid)
 for cid in local:visit(cid)
 for e in external:
  e['source_bindings']=[sources[k] for k in e.get('source_keys',[])]
  e['registry_bindings']=[{'file':p,'sha256':sha((ROOT/p).read_bytes())} for p in e.get('registry_files',[])]
 all_ext={e['id'] for e in external};assert all(set(c['external_input_ids'])<=all_ext for c in claims)
 reviews=[];paths=list(HERE.glob('review_*.json'));rp=ROOT/'reviews_v0_48'/f'{COMPONENT}_root_review.json'
 if rp.exists():paths.append(rp)
 for p in paths:
  v=json.loads(p.read_text());assert v.get('result',v.get('status'))=='PASS',p;ids=[]
  for entry in v.get('claims_reviewed',v.get('reviewed_claims',[])):
   cid=entry if isinstance(entry,str) else entry.get('id',entry.get('claim'));assert cid in local,(p,cid)
   expected=v.get('proof_hashes',{}).get(cid) if isinstance(entry,str) else entry.get('proof_range_sha256',entry.get('block_sha256'))
   assert expected==lookup[cid]['claim_sha256'],(p,cid,'stale reviewed block');ids.append(cid)
  reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':v.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':v.get('proof_sha256',v.get('proof_file_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids,'scope':v.get('scope')})
 reviewed={c for r in reviews for c in r['claims']}
 status='complete_at_stated_scope_independently_reviewed' if local<=reviewed else 'complete_at_stated_scope_pending_independent_review'
 for c in claims:c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review';c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]
 contracts={'schema':'rh-human-component-contract/1','artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,**config,'retained_foundations':[e['id'] for e in external],'original_admissibility_not_weakened':True,'selected_contract_is_implication':True}
 prov={'schema':'rh-human-component-provenance/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'claims':claims,'inherited_human_inputs':[lookup[cid] for cid in sorted(inherited_ids)],'classical_and_foundational_inputs':external,'independent_reviews':reviews,'dependency_convention':'depends_on contains numbered human claims only. Original open antecedents, inherited foundations and standard algebra are named separately; the literal OneChar implication is distinguished from AUT_UNRAM_COEF.','baseline_provenance':{'file':str(baseline.relative_to(ROOT)),'sha256':sha(baseline.read_bytes())},'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
 proposed={'id':'TASK_ONE_CHAR_PROOF','claim':'OCH30','scope':'Complete original implication InpZ plus AutomorphyUnramifiedCoefficients implies OneChar. Every actual local component, normalized global ring, graded model, point rigidity/admissibility, normalized Selmer lower bound, irredundant every-cover trace upper bound and coefficient return is supplied. AUT_UNRAM_COEF remains the unchanged separate original selected antecedent. Root alone records selected-frontier closure.','retained_selected_antecedents':['AUT_UNRAM_COEF'],'not_a_closure_of_AUT_UNRAM_COEF':True}
 validation='Two-pass standalone draft TeX with exact proof hash; no Lean or kernel replay. Independent mathematical/source reviews are bound by proof blocks as listed.'
 closure={'schema':'rh-human-component-closure/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'closed_subcontracts':config['subcontracts'],'proposed_global_frontier_leaf_closures':[proposed],'new_global_frontier_leaf_closures':[],'foundation_retention_explicit':True,'independent_reviews':reviews,'validation':validation,'pending':sorted(local-reviewed,key=lambda x:int(x[3:])),'AUT_UNRAM_COEF_remains_separate':True,'original_GD_unchanged':True}
 manifest={'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())}
 for name,obj in [('contracts.json',contracts),('original_contracts.json',contracts),('provenance.json',prov),('closure.json',closure),('source_manifest.json',manifest),('retained_foundations.json',external),('classical_inputs.json',{'schema':'rh-classical-input-registry/1','component':COMPONENT,'inputs':external})]:
  (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
 (HERE/'report.txt').write_text(COMPONENT+' v'+VERSION+'\n\n'+config['report']+'\n\nThirty explicit human claims B; no new published application A. The exact original AUT_UNRAM_COEF antecedent remains separate from the proposed TASK_ONE_CHAR_PROOF implication closure. The critical e=1 case is explicit. No extra prime cutoff is imposed: local Dat3 includes3 where permitted, while GD.gen itself excludes3 in the final arithmetic application. All old proof/ledger objects are immutable.\n\nRebuild: python build_metadata.py --repo /path/to/formal_source\nValidate: python validate_tex.py --format /path/to/pdflatex.fmt\n\n'+f'Pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}; ranges: {len(sources)}; inherited bindings: {len(inherited_ids)}\n')
 hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
 (HERE/'hashes.json').write_text(json.dumps({'component':COMPONENT,'artifact_version':VERSION,'hashes':hashes},indent=2)+'\n')
 print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_bindings':len(inherited_ids),'main_sha256':main_sha,'status':status},indent=2))
build()
