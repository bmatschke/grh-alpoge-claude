#!/usr/bin/env python3
"""Bind the Wach descent chapter to pinned producers and exact proof blocks."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
repo=p.parse_args().repo.resolve()
AV='src/Development/AbelianVarietyTheory/'
I=AV+'Proofs/InertiaEigenvalues/'
N=AV+'Definitions/NonGaloisDescent/'
SOURCE={
 'cancel':(I+'ExistsWittTiltLatticeTensorCancel.lean','Full tensor cancellation and actual exists_kappa',1,None),
 'coord':(I+'ExistsAdicCoordinatesOfBasisModP.lean','Full original AdicCoord.exists_coord including its complete-ring lemmas',1,None),
 'matrix':(I+'ExistsIsUnitMatrixOfPowSmulSpanInvert.lean','Full denominator subring, independence and invertible matrix producer',1,None),
 'basechange':(I+'IsBaseChangeLatticeOfBasisAfterExtension.lean','Full original isBaseChange_subtype_of_basis_after_extension',1,None),
 'projective':(I+'ProjectiveOfFreeLatticeOverFiniteFreeRing.lean','Full original projective_compHom_of_free_of_finite_free',1,None),
 'prismvalue':(I+'PrismaticFCrystalValueLocalPrismAinfWittTensor.lean','Full original Prism.LocalValue.main and its matrix/localization producers',1,None),
 'build':(I+'IsUnitOfOneTmul.lean','Full original generic WachLattice.build, with all exact premises',36,218),
 'full':(I+'IsUnitOfOneTmul.lean','Fullness on the selected realizing crystals and exact trivial realized image',226,274),
 'kappa':(I+'IsUnitOfOneTmul.lean','All original tensor-map, scalar, Frobenius and basis compatibilities',283,316),
 'rings':(I+'IsUnitOfOneTmul.lean','Finite tensor coordinates and original reflection of units',324,340),
 'coordE':(I+'IsUnitOfOneTmul.lean','Original period-ring coord_EE at supplied WSer and WIo scope',358,382),
 'basis':(I+'IsUnitOfOneTmul.lean','Ranks, prescribed trivial-line basis, restriction of lattice maps and cyclotomic-kernel action',384,442),
 'integers':(I+'IsUnitOfOneTmul.lean','Perfect tilt and finite free integer coefficient basis',446,464),
 'fixed':(I+'WittTwistInvariantBasisChange.lean','Full generic EtMem.mem_range at exact hRat, and original all-layer fixed_mem_range',1,None),
 'trivcrys':(I+'IsCrysLatOfTrivial.lean','Full original trivial-representation crystalline theorem on supplied PeriodData',1,None),
 'prismbuild':(I+'WachLatticesExistAllLayersOfBhattScholze.lean','Full generic build_prism including direct hmem and hreal; original main used only conditionally at WLD26',1,None),
 'prismcontract':(N+'InvertibleSpanSingleton.lean','Exact SemiBC, FCrys, FHom and fraction-naturality definitions',1,None),
 'realises':(N+'NormLeOneOfMemOL.lean','Original Realises and unit-crystal structures; no independent period existence assertion',1,None),
 'records':(N+'ExistsOfLayers.lean','Original WSer, WIo, WEt, WN, WCmp, Layers and layerwise selection scopes',1,None),
 'alllayer':(N+'ConvZero.lean','Exact full WachEx and separately retained FaithH and EtBasis predicates',1,None),
 'BS':(AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeCrystallineLattices.lean','The exact originally supplied crystalline-lattice existence/full-faithfulness input',1,None),
 'prismsupplier':(I+'ExistsWachPrismOverIntegers.lean','Retained original Wach-prism supplier; recorded for conditional interface, not claimed proved',1,None),
 'saturatedsupplier':(I+'WachInclusionInjectiveSaturatedInter.lean','Retained original inclusion/unit-reflection supplier; only its exact conclusion is used conditionally',1,None),
 'matrixsupplier':(I+'FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean','Retained original invariant matrix-solution supplier; homogeneous case suffices for WLD26',1,None),
 'localfunctor':(I+'ExistsLocalWachFunctor.lean','Actual later HW/Fon/Cmp consumer; not claimed complete by lattice assembly',1,None),
}
CLAIMS=[
 ('WLD1',[],['cancel','kappa'],'Natural actual tensor cancellation and all specified operator/lattice-map laws.'),
 ('WLD2',[],['rings','basis'],'Finite coefficient coordinates, reflection of units and exact rank dr, including zero rank.'),
 ('WLD3',[],['coord'],'Full original adic coefficient lifting; no division by p, injectivity of c or topology on B is added.'),
 ('WLD4',['WLD3'],['coordE','records'],'Full coord_EE using the original density/completeness and supplied finite coefficients.'),
 ('WLD5',[],['matrix'],'Independence over the actual power-denominator subring by one common denominator.'),
 ('WLD6',['WLD5'],['matrix'],'Full original invertible Frobenius matrix from both power-span inclusions.'),
 ('WLD7',[],['basechange'],'Actual E-spanning via square dr-coordinate matrices and reflection of units; dr tuple is not misidentified as an E-basis.'),
 ('WLD8',['WLD7'],['basechange'],'Full original isBaseChange theorem through explicit tensor normal form; no flatness of period-ring extension.'),
 ('WLD9',[],['projective'],'Full original restriction of projectivity over the specified power-series scalar map.'),
 ('WLD10',[],['prismvalue','prismcontract'],'Semilinear-base-change bases and the original principal specialization kernel.'),
 ('WLD11',['WLD10'],['prismvalue','prismcontract','realises'],'Both Frobenius power-span conditions on one actual local-prism value; fraction cancellation is in the Witt domain.'),
 ('WLD12',['WLD10','WLD11'],['prismvalue','prismcontract','realises'],'Full original Prism.LocalValue.main group law and divisibility, with actual maps and basis.'),
 ('WLD13',[],['full','BS','prismcontract'],'All original lattice maps preserve independently selected realizing images by the original full-faithfulness input.'),
 ('WLD14',['WLD1','WLD13'],['full','basis','realises'],'Exact trivial realized image in both directions, then the specified O-line and generator.'),
 ('WLD15',[],['fixed','records'],'Full generic EtMem.mem_range from its printed matrix coefficient-descent premise, with rank-zero cases justified.'),
 ('WLD16',[],['trivcrys'],'Full original crystalline trivial representation on supplied period data, including finite coefficient extension.'),
 ('WLD17',['WLD1','WLD2','WLD6','WLD11','WLD12'],['prismbuild','matrix','basis'],'Prismatic basis descends to the given etale module using the original direct hmem input; no hRat strengthening.'),
 ('WLD18',[],['build','records'],'The one inverse-image construction is stable under the entire A through scalar-map functoriality and finite coefficients.'),
 ('WLD19',['WLD7','WLD8','WLD9','WLD18'],['build','basechange','projective','records'],'All finite-generation, scalar-extension and exact restricted-projectivity fields, including zero noncrystalline branch.'),
 ('WLD20',['WLD18'],['build','records'],'Both original Frobenius localization conditions with the same prescribed Q and original exponent order.'),
 ('WLD21',['WLD18'],['build','records'],'Full group stability and trivial action modulo the same prescribed parameter.'),
 ('WLD22',['WLD18'],['build','records'],'All original maps between crystalline lattices preserve the same construction, with functor laws inherited from WEt.'),
 ('WLD23',['WLD18'],['build','records'],'Specified trivial-line vector descends and generates the actual A-lattice.'),
 ('WLD24',['WLD19','WLD20','WLD21','WLD22','WLD23'],['build','records'],'Full original generic WachLattice.build with all six exact supplied groups of premises; actual Q unit follows from WSer.'),
 ('WLD25',['WLD1','WLD4','WLD11','WLD12','WLD13','WLD14','WLD16','WLD17','WLD24'],['prismbuild','BS','records'],'Full original generic build_prism including original hreal and direct hmem; arbitrary generic O not strengthened to a complete DVR.'),
 ('WLD26',['WLD1','WLD2','WLD15','WLD25','DFD12'],['prismbuild','alllayer','prismsupplier','saturatedsupplier','matrixsupplier','integers','localfunctor'],'Conditional full WachEx at every original layer and every supplied WEt, retaining three exact period-ring suppliers; no extra inter-layer coherence invented.'),
]
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN
files={};sources={}
for key,(path,desc,a,b) in SOURCE.items():
 raw=(repo/path).read_bytes()
 assert raw==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
 lines=raw.splitlines(keepends=True);b=b or len(lines);excerpt=b''.join(lines[a-1:b])
 assert 1<=a<=b<=len(lines)
 target=HERE/'source_snapshot'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
 f={'path':path,'snapshot_file':str(target.relative_to(ROOT)),'sha256':sha(raw),'file_sha256':sha(raw),
  'bytes':len(raw),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
 files[path]=f
 sources[key]={**f,'id':'WLD_SRC_'+key.upper(),'declaration':desc,'line_start':a,'line_end':b,
  'range_sha256':sha(excerpt),'range_bytes':len(excerpt),'url':url+f'#L{a}-L{b}'}
raw=(HERE/'main.tex').read_bytes();t=raw.decode();claims=[]
for cid,deps,groups,scope in CLAIMS:
 a=t.index('% BEGIN '+cid+'\n');b=t.index('% END '+cid+'\n',a)+len('% END '+cid+'\n')
 title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',t[a:b]).group(1)
 claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.53','depends_on':deps,
  'sources':[sources[g] for g in groups],'source_groups':groups,'scope_note':scope,
  'status':'written_pending_independent_review','proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
   'line_start':t.count('\n',0,a)+1,'line_end':t.count('\n',0,b),'sha256':sha(t[a:b].encode()),'bytes':len(t[a:b].encode())},
  'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.53','component':HERE.name,'source_commit':PIN,
 'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
 'files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
endpoints=[
 ('GlobalTheory.HWL.exists_kappa','WLD1'),
 ('GlobalTheory.WachLattice.isUnit_of_one_tmul','WLD2'),
 ('GlobalTheory.AdicCoord.exists_coord','WLD3'),
 ('GlobalTheory.WachLattice.coord_EE','WLD4'),
 ('GlobalTheory.exists_isUnit_matrix_of_pow_smul_span','WLD6'),
 ('GlobalTheory.isBaseChange_subtype_of_basis_after_extension','WLD8'),
 ('GlobalTheory.projective_compHom_of_free_of_finite_free','WLD9'),
 ('GlobalTheory.Prism.LocalValue.main','WLD12'),
 ('GlobalTheory.WachLattice.full / range_trivial','WLD14'),
 ('GlobalTheory.HWL.EtMem.mem_range','WLD15'),
 ('GlobalTheory.TrivCrys.isCrys_lat_of_trivial','WLD16'),
 ('GlobalTheory.WachLattice.build','WLD24'),
 ('GlobalTheory.WachLattice.build_prism','WLD25'),
]
ends=[{'endpoint:a':a,'endpoint':a,'claim':b,'status':'whole_original_implication_written','all_original_premises_retained':True} for a,b in endpoints]
for e in ends:e.pop('endpoint:a')
ends.append({'endpoint':'GlobalTheory.WachLattice.main / HWL.WachEx','claim':'WLD26','status':'conditional_reduction_only',
 'qualification':'Original BhattScholze input plus the actual Wach prism, injectivity/unit reflection and homogeneous fixed-Frobenius matrix descent. These three producers are not proved here.'})
remaining=[
 'Actual original Wach prism over integers with its maps, scalar-map tie, finite freeness and coefficient coordinates.',
 'Actual injectivity and reflection of units for the period embedding ioE.',
 'Homogeneous cyclotomic-kernel-fixed Frobenius matrix solution descent at every required rank and layer.',
 'Separate FaithH, EtBasis, Herr class maps and quantitative de Rham comparison needed for complete HW/Fon/Cmp.',
 'Original local row/table bounds and common ConclF family; whole GLOBAL_DENOMINATOR remains open.'
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['original WGam, WSer, WIo and supplied WEt, with all their existing maps and compatibility fields',
 'exact original local-prism, FCrys, Realises and semilinear base-change premises where stated',
 'original BhattScholzeCrystallineLattices input, retained at its exact source-defined scope',
 'original hreal and direct hmem in the full generic build_prism; hRat only in the separate generic EtMem.mem_range',
 'three explicitly displayed period-ring suppliers only for conditional WLD26'],
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'conditional_reduction_extra_inputs':{'WLD26':remaining[:3]},
 'no_extra_flatness_of_period_extension':True,'same_actual_etale_module_and_all_original_maps':True,
 'no_extra_interlayer_transition_hypothesis':True,'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,'completed_source_endpoints':ends,
 'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],
 'full_original_generic_build_complete':True,'full_original_generic_build_prism_complete':True,
 'unconditional_original_all_layer_WachEx_complete':False,'full_HW_Fon_Cmp_complete':False,
 'full_GLOBAL_DENOMINATOR_supplier_supplied':False,'independent_reviews':[],'remaining':remaining})
inherited=[]
for comp,ids in [('denominator_family_data_v51',['DFD12']),('selmer_signature_comparison_v52',['SSC17'])]:
 parent=ROOT/comp;pp=json.loads((parent/'provenance.json').read_text());lookup={c['id']:c for c in pp['claims']}
 for cid in ids:
  c=lookup[cid];pl=c['proof_location'];b=b''.join((ROOT/pl['file']).read_bytes().splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
  assert sha(b)==pl['sha256']
  inherited.append({'id':cid,'component':comp,'exact_parent_provenance_sha256':sha((parent/'provenance.json').read_bytes()),
   'proof_file':pl['file'],'proof_location':pl,'proof_block_sha256':sha(b),'scope_note':c['scope_note'],
   'role':'explicit optional input conversion' if cid=='DFD12' else 'later consumer boundary only'})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[
 {'id':'WLD_ORIGINAL_DATA','kind':'original_supplied_data','statement':'Exact WGam/WSer/WIo/WEt, local prism, FCrys and Realises fields, including original period invariant-ring identity. No existence of these original supplied records is silently added to a claimed producer.'},
 {'id':'WLD_BHATT_SCHOLZE','kind':'original_published_input','statement':'The exact source-defined BhattScholzeCrystallineLattices existence and full-faithfulness premise. This chapter proves its lattice-assembly application, not the published theorem.'},
 {'id':'WLD_ELEMENTARY_ALGEBRA','kind':'standard_algebra_foundations','statement':'Tensor-product universal property, finite free matrices and determinants over commutative rings, localization, finite projective splitting and Nakayama. The special descent and tensor-injectivity arguments are proved in the text.'},
 {'id':'WLD_PERIOD_STRUCTURE','kind':'standard_original_period_ring_structure','statement':'p-adic completeness and domain structure of the stated Witt ring, perfection of the supplied tilt, and finite free ring of integers in a finite p-adic extension. Actual period-embedding saturation and invariant matrix descent remain explicit tasks.'},
]})
dump('published_inputs.json',[{'name':'BhattScholzeCrystallineLattices','status':'retained original source premise; not a newly discharged published application','source':sources['BS']}])
(HERE/'report.txt').write_text('WACH LATTICES FROM ONE PRISMATIC REALIZATION — v0.53\n'
 f'Source pin: {PIN}\nClaims: 26 (WLD1–WLD26).\nProof SHA256: {sha(raw)}\n\n'
 'Full original adic coefficient, power-denominator matrix, scalar-extension lattice and restricted-projectivity producers.\n'
 'Full original local-prism value theorem and both generic Wach lattice constructors, all original premises retained.\n'
 'One inverse-image lattice inside the supplied etale module; exact Frobenius, group, trivial-line and functorial fields.\n'
 'WLD26 retains exactly three period-ring suppliers before full all-layer WachEx.\n'
 'FaithH, EtBasis, Herr maps, quantitative comparison and common local family bounds remain explicit.\n'
 'No whole selected obligation closed. No Lean replay or PDF claimed. Independent review pending.\n')
(HERE/'wach_descent_handoff.txt').write_text('NEXT PRODUCERS AFTER WLD — v0.53\n\n'
 'Use WLD25 as the complete generic assembly; do not redo tensor cancellation, coefficient lifting or the normal-form base-change proof.\n'
 'Independent tasks: actual Wach prism (ExistsWachPrismOverIntegers), ioE injectivity/unit reflection (WachInclusionInjectiveSaturatedInter), and homogeneous invariant Frobenius matrix descent (FixedByCyclotomicKernelEtalePhiSolutionMemWach).\n'
 'WLD26 installs their original outputs on every given etale module. It does not construct WEt or the complete HW/Fon/Cmp triple.\n'
 'Follow FaithH and EtBasis, Herr class maps and quantitative comparison to ExistsLocalWachFunctor. Keep one layer record at each original allowed index; the original Layers assembly adds no invented transition condition.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'ranges':len(sources),'inherited':len(inherited),'proof_sha256':sha(raw)},indent=2))

