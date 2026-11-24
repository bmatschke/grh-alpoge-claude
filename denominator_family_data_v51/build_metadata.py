#!/usr/bin/env python3
"""Bind the actual family-data chapter to the immutable source and its contracts."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
repo=p.parse_args().repo.resolve()
AV='src/Development/AbelianVarietyTheory/'
LC='src/Formalism/SharpRestriction/LevelLetterCocycles/'
SOURCE={
 'split':(AV+'Proofs/InertiaEigenvalues/SemisimpleOfInjective.lean',1,214,'Actual characters, semisimple splitting, saturated integral complement'),
 'dense':(AV+'Proofs/InertiaEigenvalues/SemisimpleOfInjective.lean',215,310,'Exact permitted split Frobenius density and trace interface'),
 'parity':(AV+'Proofs/InertiaEigenvalues/SemisimpleOfInjective.lean',430,548,'Actual normalized cuspidal and Speh character; both parity cases'),
 'complement':(AV+'Proofs/InertiaEigenvalues/SemisimpleOfInjective.lean',549,None,'Original Complement_at, ComplementF and ComplementClosed'),
 'block':(AV+'BlockTheory/NonGaloisCusps/BlockComplementLattice.lean',1,None,'Original IsoBlock, IsComplement and family contracts'),
 'cuspidal':(AV+'Proofs/InertiaEigenvalues/GaloisRepsCuspidal.lean',1,None,'adm2 to original GaloisRepsCusp'),
 'family':(AV+'Proofs/InertiaEigenvalues/ExistsContinuousComplementFamily.lean',1,None,'Actual continuous complement selection and PtFam existence'),
 'pt':(AV+'Definitions/NonGaloisDescent/IsRhoPtOfSplitting.lean',1,None,'Exact GoodPtRow, Signature attachment and PtFam definitions'),
 'hub':(LC+'JointConditionsZpowers/CommutingEndomorphismCondition.lean',1,None,'SignatureChoiceCondition, KillAt, fourteen HubData fields, nine DataAD laws and canon'),
 'canonical':(AV+'Definitions/NonGaloisDescent/DecompositionInvariantsCondition.lean',1,72,'Actual epJ, dcOf, cBof, c0of, ourX and Canon'),
 'exists':(AV+'Proofs/InertiaEigenvalues/ExistsHubData.lean',1,None,'Whole original exists_hubData with functional errors and exceptional sets'),
 'goodrow':(AV+'Proofs/InertiaEigenvalues/LocalGlobalAssembly.lean',1,None,'Whole GoodPtRow implication on the actual eigenspace'),
 'labels':(AV+'Proofs/SatakeParameters/SplitPlaceGoodSignature.lean',1,49,'Split type places and literal goodRow/goodSig dictionary'),
 'twistkill':(AV+'Proofs/InertiaEigenvalues/ChosenTwistAnnihilatesSelmerGroups.lean',1,None,'Whole chosen-twist killing implication'),
 'twist':(LC+'TwGood.lean',1,242,'Exact TwGoodAt, TwGood and character orientation'),
 'nutie':('src/Development/AutomorphicArithmetic/CyclotomicBounds/CyclotomicOrders/NuHost.lean',1,None,'Literal prime-branch identity nu_eq_nuL'),
 'bsintegral':(AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeIntegral.lean',1,None,'Original integral crystalline input, existence and unique full faithfulness'),
 'bscoefficient':(AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeCrystallineLattices.lean',1,None,'Exact finite-coefficient output predicate'),
 'bsproof':(AV+'Proofs/InertiaEigenvalues/BhattScholzeCoefficientsOfPadicIntLattices.lean',1,None,'Restriction of scalars, unchanged lattice, Dcris and full implication'),
 'admissible':(AV+'Proofs/InertiaEigenvalues/AdmissibleParametersOfLargeScale.lean',1,None,'Original uniform AdmPar and ParametersPolynomiallyBounded output'),
 'thin':(AV+'Proofs/SatakeParameters/ThinSizeDominatesAtLargeScale.lean',1,None,'Uniform thin-size inequalities'),
 'top':(AV+'Proofs/SatakeParameters/TopSizeAddLeThreeHalvesScale.lean',1,None,'Exact top weight and rho inequality'),
 'log':(AV+'Proofs/SatakeParameters/ScaleLogMulLeSizeRatio.lean',1,None,'Uniform scale logarithmic comparison'),
 'roomy':(AV+'Definitions/GaloisGeometry/Alternates.lean',120,None,'All Roomy fields'),
 'admpar':(LC+'AdmissibleParameterJ.lean',225,None,'Actual AdmPar and AdmJ'),
 'parameters':('src/Formalism/LocalRingCardinality/DataParams.lean',1,None,'Original parameter inequalities and quantifiers'),
 'embedding':(LC+'EmbeddingTypeJumps.lean',250,270,'Original ParametersPolynomiallyBounded'),
 'small':(AV+'Proofs/InertiaEigenvalues/SpecialPrimesSmallAlongFamily.lean',1,None,'All small-prime fields and exact uniform-family theorem'),
 'smallcontract':(AV+'Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean',1,None,'Exact Small and midG definitions'),
 'scales':(LC+'NEqRZeroMulXPow.lean',250,411,'Exact lStar, lA and rbprime scale inequalities'),
 'setup':(AV+'Definitions/NonGaloisDescent/BoundAtTwoAndThreeForFamily.lean',1,None,'Original Hypotheses2, rowC, Setup and FactsF'),
 'setupfamily':(AV+'Proofs/InertiaEigenvalues/ExistsHubDataFamily.lean',1,None,'Original family choice order and coherent suppliers still required'),
 'reps':(LC+'SumRepresentations.lean',1,None,'Original adm2, Conclusion41, ConclusionZ and shared representation facts'),
}
CLAIMS=[
 ('DFD1',[],['split'],'Actual semisimple character summands over the original field, including repeated characters.'),
 ('DFD2',['DFD1'],['split','block'],'Saturated original lattice, actual integral complement and continuity; rational block splitting only.'),
 ('DFD3',[],['dense'],'Full original AE.eq_of_continuous under retained Cheb; no continuous complex embedding assumption.'),
 ('DFD4',[],['cuspidal','parity','reps'],'Whole original adm2 -> GaloisRepsCusp and normalized actual character.'),
 ('DFD5',['DFD4'],['parity'],'Whole original hasTrace_part including even parity and integer twists.'),
 ('DFD6',['DFD1','DFD2','DFD3','DFD5'],['complement','block','parity'],'Full Complement_at, ComplementF, ComplementClosed on the original coefficient DVR.'),
 ('DFD7',['DFD6'],['family','pt'],'Whole continuous complement family and PtFam including trivial representations off Z.'),
 ('DFD8',['DFD7'],['hub','canonical'],'Actual fourteen-field HubData and every original nine DataAD / six Canon field.'),
 ('DFD9',['DFD4','DFD7','DFD8'],['exists','reps','canonical'],'Whole original exists_hubData with e_prime and exc functional dependence and exact I.'),
 ('DFD10',[],['goodrow','labels','pt','reps'],'Whole original GoodPtRow implication and actual attached good signature under TriplesGood.'),
 ('DFD11',[],['twistkill','twist','hub','nutie'],'Whole original SignatureChoiceCondition + NChTie + TwGoodAt -> KillAt, including finite Selmer and tame term.'),
 ('DFD12',[],['bsintegral','bscoefficient','bsproof'],'Whole original integral-to-finite-coefficient crystalline implication; integral input retained exactly.'),
 ('DFD13',[],['admissible','thin','top','log','roomy','admpar','parameters','embedding'],'Full uniform original parameter admissibility with cutoff before D,L,P.'),
 ('DFD14',[],['small','smallcontract','scales','parameters'],'Whole original Small family theorem, including prime three and all exceptional primes.'),
 ('DFD15',['DFD9','DFD10','DFD11','DFD12','DFD13','DFD14'],['setup','setupfamily'],'Conditional original family setup with coherent Wach/Cmp and actual Selmer-signature suppliers explicitly retained; not a closure of its producer.'),
]
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN
files={};sources={}
for key,(path,a,b,decl) in SOURCE.items():
 raw=(repo/path).read_bytes()
 assert raw==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
 lines=raw.splitlines(keepends=True);b=len(lines) if b is None else b
 assert 1<=a<=b<=len(lines),(path,a,b,len(lines))
 target=ROOT/'source_snapshot_v0_51'/'denominator'/path
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
 f={'path':path,'snapshot_file':str(target.relative_to(ROOT)),'sha256':sha(raw),
    'file_sha256':sha(raw),'bytes':len(raw),'source_commit':PIN,
    'verified_equal_to_pinned_git_blob':True,'url':url}
 files[path]=f
 block=b''.join(lines[a-1:b])
 sources[key]={**f,'id':'DFD_SRC_'+key.upper(),'declaration':decl,
   'line_start':a,'line_end':b,'range_sha256':sha(block),'range_bytes':len(block),
   'url':url+f'#L{a}-L{b}'}
raw=(HERE/'main.tex').read_bytes();t=raw.decode();claims=[]
for cid,deps,groups,scope in CLAIMS:
 a=t.index('% BEGIN '+cid+'\n');b=t.index('% END '+cid+'\n',a)+len('% END '+cid+'\n')
 title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',t[a:b]).group(1)
 claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.51',
  'depends_on':deps,'sources':[sources[g] for g in groups],'source_groups':groups,
  'scope_note':scope,'status':'written_pending_independent_review',
  'proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
   'line_start':t.count('\n',0,a)+1,'line_end':t.count('\n',0,b),
   'sha256':sha(t[a:b].encode()),'bytes':len(t[a:b].encode())},
  'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.51','component':HERE.name,'source_commit':PIN,
 'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
 'files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
ends=[
 {'endpoint':'GlobalTheory.BlockComplement.Complement_at / complementF / complementClosed','claim':'DFD6','status':'whole_original_implications_written'},
 {'endpoint':'GlobalTheory.PtCore.exists_continuous_complementFamily / exists_ptFam','claim':'DFD7','status':'whole_original_implications_written'},
 {'endpoint':'GlobalTheory.HubX.canon_ourX','claim':'DFD8','status':'whole_original_implication_written'},
 {'endpoint':'GlobalTheory.HubX.exists_hubData','claim':'DFD9','status':'whole_original_implication_written'},
 {'endpoint':'GlobalTheory.Proof.LocalGlobalAssembly.main','claim':'DFD10','status':'whole_original_implication_written'},
 {'endpoint':'GlobalTheory.NLink.twist_kills_selmer','claim':'DFD11','status':'whole_original_implication_written'},
 {'endpoint':'GlobalTheory.bhattScholze_coeff','claim':'DFD12','status':'whole_original_implication_written'},
 {'endpoint':'GlobalTheory.HTW.admissibleParameters_of_large_scale','claim':'DFD13','status':'whole_original_uniform_implication_written'},
 {'endpoint':'GlobalTheory.SpecialSmall.special_primes_small','claim':'DFD14','status':'whole_original_family_implication_written'},
 {'endpoint':'GlobalTheory.NLink.exists_setup_large','claim':'DFD15','status':'conditional_reduction_only','qualification':'Actual coherent Wach comparison and actual Selmer SignatureChoice supplier remain explicit; original producer not closed.'},
]
remaining=[
 'Derive actual HWOf/FonOf/CmpOf coherently over all layers from the original BhattScholzeIntegral; DFD12 supplies only its complete finite-coefficient restriction layer.',
 'Derive SignatureChoiceCondition on the same chosen PtFam from original Facts, including exact Selmer lattice/character comparison and tame conductor ties; GoodPtRow alone is insufficient.',
 'The full original exists_setup_large producer is not claimed. DFD15 is explicitly conditional on these two suppliers.',
 'Actual local row estimates and all ConclF fields on a common family remain; GLOBAL_DENOMINATOR remains open. DNE remains the complete consumer.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['original Cheb where used','original D7 and coefficient embeddings','original adm2 and Conclusion41 for exists_hubData','original supplied HWOf for Canon','original NChTie, TwGoodAt, SignatureChoiceCondition for KillAt','original BhattScholzeIntegral for coefficient restriction','original ParameterChoice and FamP','two explicitly retained coherent suppliers for conditional DFD15'],
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'conditional_reduction_extra_inputs':{'DFD15':['actual HWOf/FonOf/CmpOf supplier','actual SignatureChoiceCondition on every selected PtFam from Facts']},
 'choice_order':['Fix original family, C, C2, CT and retained suppliers.','Choose one scale threshold from parameter, small-prime and original TwGood cutoffs.','Quantify over later x,hx,i,ShaFinOdd,exc.','Choose original I, coherent HW/Fon/Cmp and actual PtFam.','Evaluate functional error/exceptional-set data on these representations.','Assemble one X and use the same NChoice for its killing condition.'],
 'same_original_coefficient_DVR_and_host':True,'arbitrary_finite_natural_exceptional_sets':True,
 'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'proposed_global_frontier_leaf_closures':[],
 'whole_original_exists_hubData_supplied':True,
 'whole_original_exists_setup_large_supplied':False,
 'full_GLOBAL_DENOMINATOR_supplier_supplied':False,'independent_reviews':[],
 'remaining':remaining})
dump('inherited_inputs.json',{'artifact_version':'0.51','inputs':[],'note':'All new numbered deductions proved here. DNE is discussed as a separate consumer, not invoked to construct actual data.'})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[
 {'id':'DFD_ORIGINAL_DATA','kind':'original_supplied_data','statement':'All named D7/FamP/GoodR/adm2/Conclusion41/Facts/period and coefficient structures retain their source fields. Cheb and the precise integral Bhatt-Scholze predicate are retained exactly where the source theorem assumes them.'},
 {'id':'DFD_LINEAR_ALGEBRA','kind':'standard_algebra_foundations','statement':'Finite-dimensional composition series, semisimple finite algebras and their splitting over an algebraic closure in characteristic zero; PID finite torsion-free modules and splitting of free quotients. The problem-specific character descent and saturated-lattice continuity argument are proved in DFD1-DFD2.'},
 {'id':'DFD_NUMBER_FIELDS','kind':'standard_number_field_foundations','statement':'Galois decomposition-group cardinality ef, finite factorization of a nonzero ideal, and finiteness of the integers in a finite extension of Q_l. No additional automorphy or comparison theorem is asserted.'},
 {'id':'DFD_ANALYSIS','kind':'standard_elementary_analysis','statement':'Finite-dimensional module topologies, exponential power series and elementary inequalities. All new uniform cutoffs and original scale comparisons are proved here.'},
]})
dump('published_inputs.json',[])
(HERE/'report.txt').write_text('COMPATIBLE DENOMINATOR FAMILY DATA — v0.51\n'
 f'Source pin: {PIN}\nClaims: 15 (DFD1–DFD15).\nProof SHA256: {sha(raw)}\n\n'
 'Full original continuous integral complements, PtFam, Canon and exists_hubData.\n'
 'Complete good-row, twist-killing, finite-coefficient crystalline reduction,\n'
 'uniform parameter admissibility and family small-prime implications.\n'
 'Conditional exact family setup retains coherent Wach/Cmp and Selmer\n'
 'SignatureChoice producers. The whole setup producer and ConclF remain.\n'
 'No selected whole closure. No Lean replay or PDF claimed.\n'
 'Independent mathematical review pending.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'ranges':len(sources),'proof_sha256':sha(raw)},indent=2))
