#!/usr/bin/env python3
"""Exact-source and human-proof bindings for the faithful etale chapter."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,required=True)
REPO=parser.parse_args().repo.resolve()
I='src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/'
N='src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/'
D='src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean'
SOURCES={
 'actions':(D,472,836,'Actual period character, roots, OCb and LocAinf actions'),
 'eps':(D,944,1018,'Actual nontrivial cyclotomic tilt element and roots'),
 'tensor':(D,1038,1165,'Actual tensor lattices, RW and their maps/actions'),
 'scope':(N+'ConvZero.lean',10,31,'Full FaithH, FixBasis, EtBasis and WachEx predicates'),
 'faith':(I+'CyclotomicKernelTiltInvariantsFaithful.lean',260,None,'Original full faithH conclusion; alternate proof supplied'),
 'averaging':(I+'ExistsCyclotomicKernelFixedBasisWittTensorLattic.lean',15,94,'Generic shift and complete finite averaging'),
 'complete':(I+'ExistsCyclotomicKernelFixedBasisWittTensorLattic.lean',100,172,'Integral completion, basis and surjectivity arguments'),
 'detaverage':(I+'ExistsCyclotomicKernelFixedBasisWittTensorLattic.lean',178,210,'Full generic determinant averaging theorem'),
 'genericbasis':(I+'ExistsCyclotomicKernelFixedBasisWittTensorLattic.lean',222,343,'Generic fixed basis over the prescribed coefficient tensor'),
 'concretebasis':(I+'ExistsCyclotomicKernelFixedBasisWittTensorLattic.lean',348,None,'Actual subgroup, tilt, Witt and lattice fixed-basis construction'),
 'contraction':(I+'SeriesOfPrecomplete.lean',72,198,'Matrix filtration, contraction and Frobenius-iterate conjugacy'),
 'padic':(I+'SeriesOfPrecomplete.lean',220,324,'Original p-adic nonlinear conjugacy induction'),
 'modp':(I+'SeriesOfPrecomplete.lean',376,472,'Original initial conjugacy and full coefficient conjugacy'),
 'actualconj':(I+'EtalePhiMatrixDecompletionToWach.lean',14,None,'Actual original Frobenius matrix decompletion'),
 'conjexport':(I+'EtalePhiMatrixDecompletionToWachStatement.lean',1,None,'Full exported matrix decompletion statement'),
 'etbasis':(I+'SpanRangeMap.lean',1,None,'Actual fixed Frobenius coordinates and full EtBasis return'),
 'etmod':(I+'ResEqOneIff.lean',12,None,'Coordinate embedding, all functor fields and original nonempty_wEt'),
 'etrecord':(N+'ExistsOfLayers.lean',121,157,'Every original WEt record field'),
 'wach':(I+'WachLatticesExistAllLayersOfBhattScholze.lean',1,None,'Original conditional WachEx consumer, already supplied by WPR30'),
 'assembly':(I+'ExistsLocalWachFunctor.lean',1,None,'Next original assembly; Herr and quantitative comparison retained'),
}
CLAIMS=[
 ('FET1',['WPR2'],['actions','scope'],'Actual actions and character identified uniquely, without changing supplied records.'),
 ('FET2',[],['faith'],'Actual completed cyclotomic compositum; standard perfectoid finite-extension theorem explicitly retained as foundation.'),
 ('FET3',[],['actions','faith'],'Elementary sharp-limit and p-adic expansion, equivariant even for an automorphism not pre-assumed to preserve the subfield.'),
 ('FET4',['FET1','FET2','FET3'],['faith','scope'],'Full original FaithH, every prime and finite extension; no new hypothesis on AI.'),
 ('FET5',['FET4'],['concretebasis','eps'],'Distinct finite quotient embeddings and an infinite common value set on actual integral tilt invariants.'),
 ('FET6',[],['detaverage'],'Full generic determinant nonvanishing average, arbitrary ring to field maps and infinite common value set.'),
 ('FET7',['FET5','FET6','WIS2'],['concretebasis'],'Actual integral Witt-unit determinant average; no division by group order or p.'),
 ('FET8',['FET7'],['genericbasis'],'Exact trace-one coefficients for every actual finite quotient.'),
 ('FET9',[],['averaging'],'Finite averaging and all-precision smoothness; no continuity of arbitrary Witt elements assumed.'),
 ('FET10',['FET8','FET9','WIS2','WIS3','WIS4'],['averaging','complete'],'Exact fixed-vector limit on the original complete finite free tensor module.'),
 ('FET11',['FET7'],['genericbasis','concretebasis'],'One invertible initial average, using a Zp-basis only to test the actual O-linear operator.'),
 ('FET12',['FET10','FET11'],['genericbasis','complete'],'Actual unchanged lattice has a fixed basis of its original O-rank, including rank zero.'),
 ('FET13',['FET1','FET4','FET12'],['concretebasis','scope','tensor'],'Full original fixed-basis endpoint for every lattice, no Good or crystalline hypothesis added.'),
 ('FET14',['IFD1','IFD2','IFD14','IFD16','WIS2','WIS3','WIS4','WIS20','WIS23','WIS25'],['contraction','actualconj'],'All actual two-filtration inputs, with exact integral coefficient subring and fixed ring.'),
 ('FET15',['FET14'],['contraction'],'Actual near-parameter matrix contraction and error modulo p, arbitrary finite size.'),
 ('FET16',['FET14'],['contraction','modp'],'Correct choice order and common Frobenius-iterate precision/pole calculation.'),
 ('FET17',['FET15','FET16','WIS18'],['modp'],'Full initial fixed conjugacy modulo p and reflection of coefficient-matrix invertibility.'),
 ('FET18',['IFD24'],['padic'],'Exact linear correction using earlier quotient surjectivity with the actual coefficient matrix.'),
 ('FET19',['FET14','FET17','FET18'],['padic'],'Integral nonlinear p-adic correction and separated limiting equation.'),
 ('FET20',['FET16','FET17','FET19','WIS18'],['actualconj','conjexport'],'Full original EtalePhiMatrixDecompletionToWach; not inferred from linear matrix descent alone.'),
 ('FET21',['FET13','FET20'],['etbasis','scope'],'Full original EtBasis on unchanged lattice and ioE image.'),
 ('FET22',['FET21','WIS18','IFD25'],['etmod'],'Actual coordinate image and fixed-column Frobenius descent at full matrix scope.'),
 ('FET23',['FET22'],['etmod','etrecord'],'Original Frobenius and quotient Gamma actions, exact kernel identification and all laws.'),
 ('FET24',['FET22','FET23'],['etmod','etrecord'],'All original lattice morphisms, semilinearity, addition/composition/scalars and naturality.'),
 ('FET25',['FET21','FET22','FET23','FET24'],['etmod','etrecord'],'Full original WEt nonemptiness on every supplied good layer, every record field.'),
 ('FET26',['FET25','WPR30'],['wach','assembly'],'Actual input to completed conditional WachEx; Herr and quantitative/common family outputs retained.'),
]

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()==PIN
records={};files={}
for key,(path,first,last,desc) in SOURCES.items():
 data=(REPO/path).read_bytes()
 assert data==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
 lines=data.splitlines(keepends=True);last=last or len(lines)
 assert 1<=first<=last<=len(lines),(key,last,len(lines))
 part=b''.join(lines[first-1:last]);out=HERE/'source_snapshot'/path
 out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
 rec={'path':path,'snapshot_file':str(out.relative_to(ROOT)),'sha256':sha(data),'file_sha256':sha(data),'bytes':len(data),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
 files[path]=rec
 records[key]={**rec,'id':'FET_SRC_'+key.upper(),'declaration':desc,'line_start':first,'line_end':last,'range_sha256':sha(part),'range_bytes':len(part),'url':url+f'#L{first}-L{last}'}
raw=(HERE/'main.tex').read_bytes();text=raw.decode();claims=[]
for cid,deps,groups,scope in CLAIMS:
 a=text.index('% BEGIN '+cid+'\n');b=text.index('% END '+cid+'\n',a)+len('% END '+cid+'\n')
 block=text[a:b].encode();title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',text[a:b]).group(1)
 claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.57','depends_on':deps,'sources':[records[g] for g in groups],'source_groups':groups,'scope_note':scope,'status':'written_pending_independent_review','proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,'line_start':text.count('\n',0,a)+1,'line_end':text.count('\n',0,b),'sha256':sha(block),'bytes':len(block)},'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.57','component':HERE.name,'source_commit':PIN,'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,'files':list(files.values()),'ranges':list(records.values()),'file_count':len(files),'range_count':len(records)})
endpoints=[('GlobalTheory.TiltFaithful.faithH','FET4'),('GlobalTheory.HWL.FixedBasis.exists_det_ne_zero','FET6'),('GlobalTheory.HWL.FixedBasis.main / exists_cyclotomicKernelFixedBasis_wittTensorLattice','FET13'),('GlobalTheory.HWL.MatDecompl.decompletion / etalePhiMatrix_decompletion_to_wach','FET20'),('GlobalTheory.EtaleBasis.exists_etBasis','FET21'),('GlobalTheory.HWL.EtMod.nonempty_wEt','FET25')]
ends=[{'endpoint':e,'claim':c,'status':'whole_original_implication_written','all_original_premises_retained':True} for e,c in endpoints]
remaining=['Original good-layer and period data remain supplied; existence of GamS/WSer/IoS/IoW is a separate original input when not already constructed.', 'Herr class maps, convergent evaluation/Taylor and filtered comparison bodies at the literal ExistsLocalWachFunctor inputs.', 'Quantitative HW/Fon/Cmp and all original local row/table bounds on one common ConclF family.', 'Original BS and LocTied remain in the conditional WachEx application; whole GLOBAL_DENOMINATOR remains open.']
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,'entry_premises':['Original P/AI and all original finite extensions of Q_p and lattices.','Good/GamS/WSer/IoS/IoW only for actual coefficient/Frobenius/functor construction.','Scholze perfectoid finite-extension theorem as a named classical foundation; actual applicability proved.','Original BS and LocTied only in FET26.'],'completed_source_endpoints':ends,'whole_obligations_closed':[],'conditional_reduction_extra_inputs':{},'actual_AI_action_preserved':True,'all_primes_including_two':True,'fixed_basis_original_integral_lattice_and_rank':True,'linear_descent_distinguished_from_nonlinear_conjugacy':True,'full_original_etale_functor_all_morphisms':True,'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,'completed_source_endpoints':ends,'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'full_original_FaithH_complete':True,'full_original_fixed_basis_complete':True,'full_original_Frobenius_matrix_decompletion_complete':True,'full_original_EtBasis_complete':True,'full_original_WEt_complete':True,'full_HW_Fon_Cmp_complete':False,'full_GLOBAL_DENOMINATOR_supplier_supplied':False,'independent_reviews':[],'remaining':remaining})
inherited=[]
for cid in sorted({d for _,ds,_,_ in CLAIMS for d in ds if not d.startswith('FET')}):
 comp=('wach_inclusion_saturation_v54' if cid.startswith('WIS') else 'invariant_frobenius_descent_v55' if cid.startswith('IFD') else 'wach_prism_v56')
 parent=ROOT/comp;ledger=json.loads((parent/'provenance.json').read_text());claim=next(c for c in ledger['claims'] if c['id']==cid)
 data=(parent/'main.tex').read_bytes();pl=claim['proof_location'];first,last=pl['line_start'],pl['line_end'];part=b''.join(data.splitlines(keepends=True)[first-1:last])
 loc={'file':comp+'/main.tex','line_start':first,'line_end':last,'sha256':sha(part),'bytes':len(part)}
 inherited.append({'id':cid,'component':comp,'exact_parent_provenance_sha256':sha((parent/'provenance.json').read_bytes()),'proof_file':loc['file'],'proof_location':loc,'proof_block_sha256':sha(part),'scope_note':claim.get('scope_note',claim['title']),'role':'Exact inherited human argument on its original rings and maps.'})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
public=[{'name':'Scholze, Perfectoid spaces, Theorem 3.7(i)','url':'https://www.math.uni-bonn.de/people/scholze/PerfectoidSpaces.pdf','kind':'standard_foundation_application_checked','claim':'FET2','checked_date':'2026-11-24','scope':'Every finite extension of a perfectoid field is perfectoid. The actual field E_L is proved to equal the finite compositum LE_0 inside C.'},{'name':'Bhatt–Morrow–Scholze, Integral p-adic Hodge theory, Definition 3.5 and Example 3.6','url':'https://www.math.uni-bonn.de/people/scholze/integralpadicHodge.pdf','kind':'corroborating_primary_reference','claim':'FET2','checked_date':'2026-11-24','scope':'Completion of integers in an algebraic extension of Qp containing the cyclotomic tower is perfectoid. FET3 proves the precise sharp expansion used here.'}]
dump('published_inputs.json',public)
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[{'id':'FET_PERFECTOID','kind':'named_standard_foundation','statement':public[0]['scope'],'url':public[0]['url']},{'id':'FET_ORIGINAL_RECORDS','kind':'original_supplied_data','statement':'Original P/AI, actual Good/GamS/WSer/IoS/IoW and finite integral lattices; no new compatibility between outer layers.'},{'id':'FET_ELEMENTARY','kind':'standard_foundations','statement':'Cyclotomic Eisenstein polynomials, finite extensions of complete valued fields, Krull topology, finite free bases, Witt vector completeness and determinant/tensor algebra; limiting steps are printed.'},{'id':'FET_PRIOR','kind':'previously_proved_human_inputs','statement':'WIS/IFD/WPR precise inputs listed with exact proof hashes in inherited_inputs.json.'}]})
(HERE/'report.txt').write_text('FAITHFUL CYCLOTOMIC INVARIANTS AND THE ACTUAL ETALE FUNCTOR — v0.57\n\n26 claims FET1–FET26.\nFull original FaithH via a named standard perfectoid finite-extension theorem and explicit sharp expansion.\nFull original fixed integral Witt tensor basis, nonlinear Frobenius conjugacy, EtBasis and every field of WEt including all lattice morphisms.\nNonlinear conjugacy is proved separately from earlier IFD25; IFD24 supplies the linear corrections.\nOriginal good-layer data retained. Herr/quantitative comparison and the common ConclF family remain.\nNo whole selected obligation closure or Lean replay claimed. Independent review pending.\n')
(HERE/'next_source_handoff.txt').write_text('NEXT AFTER FET — v0.57\n\nDo not reassign FaithH, the actual fixed basis, nonlinear Frobenius conjugacy, EtBasis or WEt.\nRead ExistsLocalWachFunctor.lean:16–30. It still invokes actual GroupLayer.nonempty_gamS, Ser.nonempty_wSer, IoLayer.main, HerrClassMaps.exists_classMaps and Cmp.nonempty_cmpS.\nIdentify which of these existence inputs already has an earlier human proof before beginning.\nOriginal Herr class maps are in ExistsUniqueFits.lean; quantitative comparison enters through ChiGamPowNeOne.lean and its imports. Preserve torsion, both signed cluster orders and original normalized lengths.\nWPR30 gives WachEx under original BS+LocTied; FET25 now constructs its actual etale input on every supplied good layer. No new outer-layer transition-system assumption.\nAll common ConclF row/table estimates, ShaFinOdd, exceptional sets, summability and uniform thresholds remain for GLOBAL_DENOMINATOR.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'source_ranges':len(records),'inherited_inputs':len(inherited),'proof_sha256':sha(raw)},indent=2))
