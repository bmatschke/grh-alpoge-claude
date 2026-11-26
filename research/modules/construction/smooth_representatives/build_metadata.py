#!/usr/bin/env python3
"""Exact pinned-source and human-proof certificates for SPR; no Lean replay."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,default=HERE.parent.parent/'lean_source')
p.add_argument('--human-root',type=Path,default=HERE.parent.parent/'reconstruction_v036')
p.add_argument('--peer-root',type=Path,default=HERE.parent)
a=p.parse_args(); SOURCE=a.source.resolve(); HUMAN=a.human_root.resolve(); PEER=a.peer_root.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()==PIN
cache={};sources={}
decl=re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+')
def get(path):
    if path not in cache:
        b=(SOURCE/path).read_bytes()
        assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE),path
        cache[path]=(b,b.decode().splitlines(keepends=True))
    return cache[path]
def add(sid,path,anchor,role='Exact original source contract or argument independently reconstructed'):
    path='src/'+path;b,ls=get(path);hits=[i for i,l in enumerate(ls) if anchor in l]
    assert len(hits)==1,(sid,anchor,hits)
    i=hits[0];j=next((j for j in range(i+1,len(ls)) if decl.match(ls[j])),len(ls))
    while j>i and not ls[j-1].strip():j-=1
    block=''.join(ls[i:j]).encode()
    sources[sid]={'id':sid,'path':path,'declaration':anchor,'declaration_anchor':anchor,
      'line_start':i+1,'line_end':j,'sha256':sha(b),'file_sha256':sha(b),
      'range_sha256':sha(block),'range_bytes':len(block),'first_line':ls[i].rstrip(),
      'role':role,'verified_equal_to_pinned_git_blob':True,'url':f'{REPO}/blob/{PIN}/{path}#L{i+1}-L{j}'}
oldsrc={s['id']:s for s in json.loads((HUMAN/'regular_quotient/provenance.json').read_text())['source_inventory']}
for sid in ['finite_pair','quotient_measure','original_representative','regular_representation',
 'model','model_action','model_smooth_span','bounded_holomorphic_form','central_cuspidality',
 'multiplicity_map_contract','full_multiplicity_extension','remaining_sobolev_growth',
 'point_evaluation_continuity','remaining_boundedness','remaining_target_volume',
 'actual_hilbert_map','finite_eigenclass','global_ae','local_integral_bound','smooth_map',
 'smooth_vector_adelic','l2_derivative','cusp_closure','gelf_scalar','pointwise_word',
 'pointwise_zfin','filtered_word','word_mem','word_map','smooth_automorphic_contract','automorphic_contract']:
    d=dict(oldsrc[sid]);b,ls=get(d['path'])
    assert sha(b)==d['file_sha256'] and sha(''.join(ls[d['line_start']-1:d['line_end']]).encode())==d['range_sha256']
    sources[sid]=d
D='Development/AbelianVarietyTheory/';DP=D+'Proofs/DivisorProofs/';IW=D+'Proofs/IwasawaDecomposition/'
for sid,anchor in [('rep_zero','theorem _root_.GlobalTheory.LocRep.rep_zero '),
 ('rep_add','theorem _root_.GlobalTheory.LocRep.rep_add '),('rep_smul','theorem _root_.GlobalTheory.LocRep.rep_smul '),
 ('rep_pairing','theorem _root_.GlobalTheory.LocRep.exists_pairing'),
 ('local_rep','theorem _root_.GlobalTheory.LocRep.locallyIntegrable_rep '),
 ('compact_pairing_test','theorem _root_.GlobalTheory.LocRep.rep_of_pairing ')]:
    add(sid,DP+'LocallyIntegrableRep.lean',anchor)
for sid,f,anchor in [
 ('parameter_integral','RepresentativeParametricIntegralContinuousFamily.lean','theorem rep_parametric_integral '),
 ('continuous_average','ExistsContinuousRepresentativeAverage.lean','theorem _root_.GlobalTheory.LocRep.exists_continuous_rep_average '),
 ('fixed_approx','ExistsFixedAverageApproxOfSubgroupFixed.lean','theorem _root_.GlobalTheory.exists_average_fixed_approx_of_fixed '),
 ('eval_closure','ExistsEvaluationExtensionClosureRepresentatives.lean','theorem _root_.GlobalTheory.LocRep.exists_eval_closure '),
 ('one_dimensional_taylor','EqSumIntegralCubeDerivatives.lean','private theorem eq_interval_average_sub_weighted_deriv'),
 ('cube_identity','EqSumIntegralCubeDerivatives.lean','theorem _root_.GlobalTheory.CubeTaylor.eq_sum_integral_cube_derivatives '),
 ('smooth_products','SmoothAlongCurveProductsStable.lean','theorem _root_.GlobalTheory.smooth_along_curve_products_stable '),
 ('joint_smooth_deriv','SmoothAlongCurveProductsStable.lean','private theorem jointlySmooth_deriv_action '),
 ('joint_smooth_fold','SmoothAlongCurveProductsStable.lean','private theorem jointlySmooth_foldr_deriv_action ')]:add(sid,DP+f,anchor)
for sid,anchor in [('rep_translate','theorem rep_tr '),('derivative_transfer','theorem hasDerivAt_rep '),
 ('exists_eval','theorem exists_eval '),('smooth_domain','def Sm '),('generic_smooth_rep','theorem exists_smooth_rep '),
 ('foldr_transfer','theorem foldr_rel '),('actual_smooth_rep','theorem exists_smooth_repr ')]:
    add(sid,DP+'SmoothVectorAutomorphicDerivatives.lean',anchor)
add('sum_bound',DP+'BoundedHolomorphicFormEqMultiplicitySpaceValue.lean','theorem sum_bound ')
add('full_cont_value',DP+'BoundedHolomorphicFormEqMultiplicitySpaceValue.lean','theorem cont_value ')
for sid,anchor in [('restriction','theorem restrictsTo_of_eq '),('extension','theorem exists_extension '),
 ('theta_member','theorem exists_member '),('level_open','theorem level_open '),
 ('fires_at','theorem firesAt '),('theta_map','theorem exists_thetaMap ')]:
    add(sid,IW+'ExistsThetaLiftLinearMapCuspFormMultiplicity.lean',anchor)
add('compact_cyclicity',IW+'EqTopOfTranslates.lean','theorem mem_of_translates ')
for sid,anchor in [('bilinear_theta','theorem exists_isThetaP '),('bilinear_theta_literal','theorem exists_isThetaP\' '),
 ('linear_choice','theorem exists_linear_choice '),('linear_theta_lift','theorem exists_linear_lift '),
 ('actual_kernel_linear','def kernelL ')]:
    add(sid,DP+'ExistsIsThetaPrimeMultOfFiresAt.lean',anchor)
add('theta_fires_consumer',DP+'ThetaFiresIffThetaMultExists.lean','theorem exists_isThetaMult_of_firesAt ')
add('fires_contract',D+'BlockTheory/DivisorBase/ThetaKernelFiring.lean','def FiresAt ')
add('theta_mult_contract',D+'BlockTheory/TwistedDiscreteSeries/ThetaMultiplicity.lean','def IsThetaMult ')
add('sobolev_contract','Formalism/LocalToGlobal/BesselHermitianTheta/TiedType.lean','def Sobolev₂ ')
add('principal_entry_conditions',DP+'ThetaIntegrandIntegrable.lean','theorem mem_princ ')
add('principal_neighborhood',DP+'ThetaIntegrandIntegrable.lean','theorem eventually_princ_mat ')
add('actual_finite_projection',DP+'ThetaIntegrandIntegrable.lean','theorem eventually_princ ')
add('principal_in_level','Formalism/LocalToGlobal/Divisibility/DefGroup.lean','theorem Kg_le_lev ')
maps=[
 ['rep_zero','rep_add','rep_smul','rep_pairing','local_rep','compact_pairing_test'],
 ['parameter_integral','rep_pairing','compact_pairing_test'],
 ['continuous_average','rep_pairing','compact_pairing_test'],
 ['fixed_approx','continuous_average'],['eval_closure','compact_pairing_test'],
 ['exists_eval','eval_closure','fixed_approx'],['one_dimensional_taylor'],['cube_identity','one_dimensional_taylor'],
 ['smooth_products','joint_smooth_deriv','joint_smooth_fold','smooth_domain'],
 ['derivative_transfer','rep_translate','parameter_integral'],
 ['generic_smooth_rep','exists_eval','cube_identity'],
 ['generic_smooth_rep','foldr_transfer','derivative_transfer','smooth_products'],
 ['actual_smooth_rep','finite_pair','original_representative','regular_representation','global_ae','local_integral_bound'],
 ['full_multiplicity_extension','actual_hilbert_map','finite_eigenclass','automorphic_contract'],
 ['multiplicity_map_contract','actual_hilbert_map','finite_eigenclass','rep_translate'],
 ['pointwise_word','filtered_word','word_mem','word_map','l2_derivative'],
 ['remaining_sobolev_growth','smooth_automorphic_contract','word_map'],
 ['pointwise_zfin','gelf_scalar','smooth_automorphic_contract'],
 ['cusp_closure','central_cuspidality','actual_hilbert_map'],
 ['full_cont_value','sum_bound','word_map','filtered_word','sobolev_contract'],
 ['full_multiplicity_extension','bounded_holomorphic_form','finite_pair','multiplicity_map_contract'],
 ['restriction','compact_cyclicity','multiplicity_map_contract'],
 ['extension','bounded_holomorphic_form','full_multiplicity_extension','remaining_boundedness','remaining_target_volume'],
 ['bilinear_theta','bilinear_theta_literal','linear_choice','linear_theta_lift','actual_kernel_linear','theta_fires_consumer'],
 ['theta_map','fires_at','theta_member','level_open','principal_entry_conditions','principal_neighborhood','actual_finite_projection','principal_in_level','fires_contract','theta_mult_contract','remaining_boundedness','remaining_target_volume']]
deps=[[],['SPR1'],['SPR1'],['SPR3'],['SPR1'],['SPR1','SPR2','SPR4','SPR5'],[],['SPR7'],[],
 ['SPR1','SPR2'],['SPR6','SPR8','SPR9'],['SPR9','SPR10','SPR11'],
 ['SPR1','SPR11','SPR12','ASB3','ASB4','RQC1','RQC3','RQC6','RQC11','HCU14','HCU16'],
 ['SPR13','HCU16','HCU18','RQC9','RQC10'],['SPR14','HCU18','HCU14','HCU16'],
 ['SPR13','SPR14','RQC7','RQC9','RQC10','HCU16'],['SPR16','ASB14'],
 ['SPR16','HCU12','RQC20','RQC21'],['SPR14','HCU18','RQC15','CTC12'],
 ['SPR14','RQC9','RQC10','ASB14'],
 ['SPR14','SPR15','SPR16','SPR17','SPR18','SPR19','SPR20','HCU16','HCU17','HCU18','RQC6'],
 [],['SPR21','SPR22','HCU19'],[],
 ['SPR23','SPR24','HCU20','TAE6','TAE13','CTC13','BTH5','BTH15','JIO19']]
scopes=[
 'Locally L1-bounded AE-linear representative map on a locally compact second-countable Haar group; no injectivity assumption.',
 'Arbitrary compact parameter set with locally finite measure; continuously parameterized Hilbert vectors and joint continuous representatives.',
 'Every compactly supported continuous averaging kernel and Hilbert vector; left Haar alone suffices.',
 'Every H-fixed vector, H normalized by the original open U; approximants retain the same H-fixed condition.',
 'Every bounded operator and subspace with compact-uniform evaluation bounds; extension to closure by continuous linear evaluations.',
 'Every continuous cube weight with the stated original scalar comparison; same H fixed space and same U.',
 'Every one-parameter subgroup and vector with a supplied derivative; exact weight and negative sign.',
 'One finite index set, weights and ordered derivative words before d, invariant domain and v; no commutation, including N=0.',
 'Full original arbitrary-curve-product smoothness, derivative and translation stability and all ordered derivative families.',
 'Any continuous representatives of a Hilbert vector and its derivative; original right translations and continuous pointwise derivative.',
 'One fixed assignment R for the entire smooth H-fixed space from the same cube, weights and evaluations.',
 'The same R for every derivative word, with full joint curve-product smoothness and pointwise derivative identities.',
 'Full original exists_smooth_repr for every supplied FinPair, IsReg and fixed open U; same U invariance and global AE derivatives.',
 'One pointwise multilinear map from the original Hilbert map; unchanged common finite level.',
 'Exact original J, chi and one-place atTau; no extra character or normalization assumption.',
 'Every original right-fold Lie word; literal filtered subsequences preserve order.',
 'One exponent before all model tuples and derivative words, on one original fixed level; no cross-level uniformity claim.',
 'Original gelf on actual smooth model values, one-dimensional stable space including the zero value.',
 'Full original ZCusp and IsCusp for the same Hilbert-map values, retaining separately supplied seed ZCusp.',
 'Exact Sobolev2 ambient algebraic functional; bound only on original smooth vectors and finite derivative list.',
 'Full original boundedHolomorphicForm_eq_multiplicitySpace_value on supplied bounded HolForm, FinPair and separate ZCusp.',
 'Full original restrictsTo_of_eq, with LowSm, LowIrr, original compact frames and each seed slot nonzero.',
 'Complete lowest-type extension consumer after explicit original target FinPair and initial seed bound, plus actual IsAutFun and ZCusp.',
 'Full generic linear choice and linear theta lift for arbitrary source vector space, original integral and range(ext).',
 'All i,t and x on one original R; target FinPair and initial extremal bound remain explicit unresolved producer inputs.'
]
tex=(HERE/'main.tex').read_bytes();ls=tex.splitlines(keepends=True);claims=[]
for n in range(1,26):
    cid=f'SPR{n}';i=next(i for i,l in enumerate(ls) if l.strip()==f'% BEGIN {cid}'.encode())
    j=next(i for i,l in enumerate(ls) if l.strip()==f'% END {cid}'.encode())+1
    block=b''.join(ls[i:j]);title=next(l.decode().strip() for l in ls[i:j] if l.startswith(b'\\paragraph{'))[11:-1]
    claims.append({'id':cid,'title':title,'introduced_in':'0.37','classification':'B',
      'status':'complete independent human proof of the explicitly stated implication','depends_on':deps[n-1],
      'quantifier_scope':scopes[n-1],'proof_location':{'file':'smooth_representatives/main.tex','label':'claim:'+cid,
        'line_start':i+1,'line_end':j,'sha256':sha(block),'bytes':len(block)},
      'source_ids':maps[n-1],'sources':[sources[s] for s in maps[n-1]]})
inherited=[]
for root,rel,ids in [(HUMAN,'holomorphic_uniqueness/main.tex',['HCU12','HCU14','HCU16','HCU17','HCU18','HCU19','HCU20']),
 (HUMAN,'regular_quotient/main.tex',['RQC1','RQC3','RQC6','RQC7','RQC9','RQC10','RQC11','RQC15','RQC20','RQC21']),
 (HUMAN,'constant_terms/main.tex',['CTC12','CTC13']), (HUMAN,'theta_extension/main.tex',['TAE6','TAE13']),
 (HUMAN,'base_theta/main.tex',['BTH5','BTH15']),(HUMAN,'joint_harmonic_io/main.tex',['JIO19']),
 (PEER,'adelic_sobolev/main.tex',['ASB3','ASB4','ASB14'])]:
    b=(root/rel).read_bytes();ll=b.splitlines(keepends=True);blocks=[]
    for cid in ids:
        i=next(i for i,l in enumerate(ll) if l.strip()==f'% BEGIN {cid}'.encode())
        j=next(i for i,l in enumerate(ll) if l.strip()==f'% END {cid}'.encode())+1;bb=b''.join(ll[i:j])
        blocks.append({'id':cid,'line_start':i+1,'line_end':j,'sha256':sha(bb),'bytes':len(bb)})
    inherited.append({'file':rel,'sha256':sha(b),'file_sha256':sha(b),'role':'Actual proof inputs, inherited or jointly reconstructed; claim DAG is acyclic.','claims':blocks})
remaining=[{'id':'SPR_INITIAL_TARGET_VOLUME_AND_BOUND','classification':'C','status':'retained original producers',
 'contract':'Produce the original target FinPair and bound the initial extremal theta function before the Hilbert realization. No post-Hilbert scalar or growth theorem may be used circularly.',
 'source_ids':['finite_pair','remaining_boundedness','remaining_target_volume'],'not_new_independent_top_level_obligation':True}]
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.37','date':'2026-11-22',
 'component':'smooth_representatives','source_commit':PIN,'main_tex_sha256':sha(tex),
 'metadata_builder':{'file':'build_metadata.py','sha256':sha(Path(__file__).read_bytes()),
 'portable_invocation':'python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --peer-root /path/to/reconstruction'},
 'claims':claims,'source_inventory':list(sources.values()),'baseline_dependencies':inherited,
 'remaining_producer_contracts':remaining,'validation':{'source_commit_verified':True,
 'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),'claim_source_occurrences':sum(map(len,maps)),
 'all_source_ranges_exact':True,'new_lean_build':False,'tex_validation':'Standalone and cumulative draft syntax only.'},
 'scope_note':'Full original smooth-representative and bounded-holomorphic multiplicity producers. Initial FinPair and seed bound remain inputs. ASB3/4 feed SPR13; SPR13 feeds ASB14; no later SPR claim feeds ASB.'}
(HERE/'provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
closed=[('LocRep.rep_parametric_integral',['SPR1','SPR2']),('LocRep.exists_continuous_rep_average',['SPR3']),
 ('exists_average_fixed_approx_of_fixed',['SPR4']),('LocRep.exists_eval_closure',['SPR5']),
 ('CubeTaylor.eq_sum_integral_cube_derivatives',['SPR7','SPR8']),('smooth_along_curve_products_stable',['SPR9']),
 ('SmoothRep.exists_smooth_repr',['SPR13']),('BackForm.cont_value',['SPR20']),
 ('BackForm.exists_multMap',['SPR21']),('ThetaMap.restrictsTo_of_eq',['SPR22']),
 ('ThetaFiresLinear.exists_linear_lift',['SPR24'])]
closure={'schema':'rh-component-closure/1','version':'0.37','component':'smooth_representatives','source_commit':PIN,
 'main_tex_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'new_claims':[c['id'] for c in claims],'claim_count':25,'class_counts':{'A':0,'B':25,'C':0,'D':0},
 'all_new_claims_are_conditional_implications':True,
 'closed_subtargets':[{'source_declaration':x,'proof':y} for x,y in closed],
 'closed_prior_residues':[{'id':'HCU_POINTWISE_AUTOMORPHIC_REALIZATION','status':'closed on original supplied bounded HolForm, FinPair and ZCusp','proof':['SPR21']},
 {'id':'RQC_SMOOTH_REPRESENTATIVES_AND_SOBOLEV','status':'closed jointly with ASB1–14','proof':['SPR13','SPR17','SPR20','SPR21']}],
 'conditional_final_consumer':{'proof':['SPR23','SPR25'],'remaining':['original target FinPair','initial seed boundedness']},
 'remaining_producer_contracts':remaining,'selected_top_level_leaf_closed':False,
 'same_object_guards':['same FinPair and nuQ measure','same supplied finite level','one representative for all ordered derivatives',
 'one growth exponent before tuples and derivative words','original gelf and atTau','separate seed ZCusp',
 'exact MMap five fields','same R and io_i before t','no circular initial boundedness']}
(HERE/'closure.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_locators.txt').write_text('\n'.join(f'{s["id"]}: {s["path"]}:{s["line_start"]}-{s["line_end"]} [{s["range_sha256"]}]\n{s["url"]}' for s in sources.values())+'\n')
print(json.dumps({'claims':25,'files':len(cache),'ranges':len(sources),'claim_source_references':sum(map(len,maps)),
 'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes())},indent=2))
