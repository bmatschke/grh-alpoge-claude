#!/usr/bin/env python3
"""Bind the Selmer comparison to exact original contracts and inherited proofs."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
repo=p.parse_args().repo.resolve()
AV='src/Development/AbelianVarietyTheory/'
I=AV+'Proofs/InertiaEigenvalues/'
F=AV+'Proofs/FoundationProofs/'
LC='src/Formalism/SharpRestriction/LevelLetterCocycles/'
SOURCE={
 'conjugacy':(F+'ExistsConjOfTraceEqResiduallyAbsIrreducibleDVR.lean','Whole integral trace conjugacy, including general-local-ring version'),
 'burnside':(I+'SpanRepMatrixEqTopOfAbsIrreducible.lean','Original absolute irreducibility and matrix-span interface'),
 'trace':(I+'TraceRankRPartEqTraceBaseChangeTriple.lean','Whole original trace comparison with same parameter list and all normalization factors'),
 'tracechars':(I+'SemisimpleOfInjective.lean','Actual chiBar, epsilon, muEta and Speh trace normalization'),
 'twistconj':(I+'TwistedRhoConjLatTpsi.lean','Exact original inverse-character intertwiner'),
 'embeddings':(F+'PadicEmbeddingsConjugate.lean','Common unit ball to exact conjugacy of local embeddings'),
 'dense':(F+'PadicAutomorphismUnique.lean','Density of algebraically closed image and uniqueness of the bridge conjugacy'),
 'crys':(F+'CrystallineCocycleTransportConjugation.lean','Exact period-ring cocycle transport and Z_l map compatibility'),
 'coefpush':(F+'LocalCoefficientChangeCompare.lean','Original quotient crystalline local condition and push inclusion'),
 'coefpull':(F+'LocalCoefficientChangeCompareIntegral.lean','Integral coordinate maps and reverse local-condition inclusion'),
 'selconj':(F+'SelGLengthConj.lean','Integral quotient-lattice conjugacy, restriction and full Selmer length equality'),
 'seltie':(I+'SPiTopEqSTLoc.lean','Actual sPiTop equality with sTLoc and exact local bridge/bad-set ties'),
 'arbitrarycoef':(F+'TypeChangeInjectiveCoefficients.lean','Arbitrary injective local DVR maps; coherent residue coordinates, compact continuous cocycles and normalized lengths'),
 'length':(AV+'Proofs/CoherentCohomologyProofs/LengthBaseChangeQuotientOfMapMaximalIdeal.lean','Ramification index and module-length normalization for arbitrary local DVR maps'),
 'common':(F+'SameCharacterCommonExtension.lean','Whole original common DVR from identical character relation kernels'),
 'samecoef':(I+'IsLocalHomOfNatCast.lean','Full original sTLoc_eq, integral first map and local second map'),
 'siglength':(I+'NlenLeLenN.lean','Exact toPi, finite-cocycle lift, original Gen.bk, global inclusion and infinity cases'),
 'selcore':(I+'SameCharEqOne.lean','Whole original sel_at and SelCore with AttachedIn'),
 'nval':(I+'ConductorRootSubOneLengthLeTameValue.lean','Exact common-place normalized valuation, inversion and original conductor-root inequality'),
 'tame':(I+'MemZpowersOfTameGen.lean','Actual prescribed tame generator and same-character transfer'),
 'wild':(F+'FixedOfPowFixed.lean','Elementary wild fixed-power and prime-to-residue characteristic character argument'),
 'residual':(I+'ResidualAbsIrredGoodPointOfResidualIrred.lean','Whole actual ResidualIrreducibleRankR -> ResAbsIrr'),
 'residualcontract':(LC+'JointConditionsZpowers/ResidualIrreducibleOfTheorem.lean','Original full residual irreducibility interface'),
 'poly':(LC+'JointConditionsZpowers/CoefficientCompatibilityOf.lean','Original characteristic polynomial and residual coefficient ties'),
 'signature':(I+'PsiAtPsiAt.lean','Whole original JointSix.main and exactly shared Boolean orientation'),
 'lattice':(AV+'BlockTheory/TorsionBlocks/LatticeConditions.lean','Exact nlen, extCond, SameChar, lattice twists and Selmer definitions'),
 'pt':(AV+'Definitions/NonGaloisDescent/IsRhoPtOfSplitting.lean','Original SelCore, all five fields, actual PtFam and same-index transports'),
 'hub':(LC+'JointConditionsZpowers/CommutingEndomorphismCondition.lean','Full original SignatureChoiceCondition and KillAt'),
 'bk':(LC+'BlochKatoPhases.lean','Exact signature local condition, Selmer module and length/valuation conventions'),
 'tie':('src/Formalism/LocalRingCardinality/DataNChTie.lean','Original NChTie, common character and shared valuation embeddings'),
 'setup':(I+'ExistsHubDataFamily.lean','Original exists_setup_large and exact FactsF/pair/choice order'),
 'setupcontract':(AV+'Definitions/NonGaloisDescent/BoundAtTwoAndThreeForFamily.lean','Original family setup, FactsF and eight fields'),
}
CLAIMS=[
 ('SSC1',[],['conjugacy','burnside'],'Full original integral trace conjugacy, strengthened to any commutative local ring.'),
 ('SSC2',['SSC1','DFD3'],['trace','tracechars','twistconj','pt'],'Same actual parameter list, Frobenius normalization, integral representation and inverse character.'),
 ('SSC3',[],['embeddings','dense','crys'],'Exact bridge conjugation and finite crystalline cocycle transport on supplied LocPrime period rings.'),
 ('SSC4',['SSC2','SSC3'],['coefpush','coefpull','selconj','seltie','lattice'],'Both local-condition inclusions and exact point Selmer length equality, preserving integral lattices and all bad sets.'),
 ('SSC5',[],['arbitrarycoef'],'Uniform residue-basis coordinates for every torsion denominator under arbitrary injective local DVR extension.'),
 ('SSC6',['SSC5'],['arbitrarycoef','length','lattice'],'Whole original sT_map_eq at arbitrary local injective DVR scope, with compact continuous cocycles and infinite lengths.'),
 ('SSC7',[],['common','lattice'],'Whole common DVR from full SameChar, with exact integral/local hypotheses and common units-valued character.'),
 ('SSC8',['SSC3','SSC6','SSC7'],['samecoef','selcore','lattice'],'Whole sTLoc_eq and exact preservation of triviality on decomposition groups above ell.'),
 ('SSC9',['SSC3'],['siglength','coefpush','bk','lattice'],'Full original actual quotient-to-signature Selmer injection and local fraction witnesses, without finite-length premise.'),
 ('SSC10',['SSC4','SSC8','SSC9'],['siglength','bk','lattice'],'Whole original sT_le_sLen and infinity/zero-denominator normalization branches.'),
 ('SSC11',['SSC2','SSC4','SSC8','SSC10','DFD7'],['selcore','pt','lattice'],'Whole original sel_at and SelCore, all five fields on one attached signature and arbitrary original target index.'),
 ('SSC12',[],['nval','tie','bk'],'Full common-place normalized valuation identity, including zero convention and ramification cancellation.'),
 ('SSC13',[],['wild','tame','nval','pt'],'Whole original TameCyc and exact tame infimum/inversion with prescribed generator and empty-set branch.'),
 ('SSC14',['SSC12','SSC13'],['nval','tie','hub','bk'],'Whole original conductor-root length inequality and sum on exactly tied Q sets.'),
 ('SSC15',[],['residual','residualcontract','poly','pt'],'Whole original residual rank-r hypothesis -> ResAbsIrr for every actual IsRhoPt integral representation.'),
 ('SSC16',['SSC11','SSC14','DFD11'],['signature','hub','pt'],'Whole JointSix.main on the actual PtFam and exact same orientation; KillAt at original budget with TwGoodAt.'),
 ('SSC17',['SSC15','SSC16','DFD9','DFD10','DFD11','DFD13','DFD14','DFD15'],['setup','setupcontract','hub'],'Exact conditional exists_setup_large now retains only coherent HW/Fon/Cmp; full actual ConclF producer remains open.'),
]
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN
files={};sources={}
for key,(path,desc) in SOURCE.items():
 raw=(repo/path).read_bytes()
 assert raw==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
 n=len(raw.splitlines());target=ROOT/'source_snapshot_v0_52'/'denominator'/path
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
 url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
 f={'path':path,'snapshot_file':str(target.relative_to(ROOT)),'sha256':sha(raw),'file_sha256':sha(raw),
  'bytes':len(raw),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
 files[path]=f
 sources[key]={**f,'id':'SSC_SRC_'+key.upper(),'declaration':desc,'line_start':1,'line_end':n,
   'range_sha256':sha(raw),'range_bytes':len(raw),'url':url+f'#L1-L{n}'}
raw=(HERE/'main.tex').read_bytes();t=raw.decode();claims=[]
for cid,deps,groups,scope in CLAIMS:
 a=t.index('% BEGIN '+cid+'\n');b=t.index('% END '+cid+'\n',a)+len('% END '+cid+'\n')
 title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',t[a:b]).group(1)
 claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.52','depends_on':deps,
  'sources':[sources[g] for g in groups],'source_groups':groups,'scope_note':scope,
  'status':'written_pending_independent_review','proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
   'line_start':t.count('\n',0,a)+1,'line_end':t.count('\n',0,b),'sha256':sha(t[a:b].encode()),'bytes':len(t[a:b].encode())},
  'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.52','component':HERE.name,'source_commit':PIN,
 'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
 'files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
endpoints=[
 ('GlobalTheory.TraceConjugacy.exists_conj_of_trace_eq_local','SSC1'),
 ('GlobalTheory.TripleTrace.trace_eq / PtCore.twistedRho_conj_latTpsi','SSC2'),
 ('GlobalTheory.TwistedSelmerCompare.crystallineCocycle_transport_conjugation','SSC3'),
 ('GlobalTheory.ConjLatticeSelmer.extCond_eq_bkG / sPiTop_eq_sTLoc','SSC4'),
 ('GlobalTheory.SelmerFlat.sT_map_eq','SSC6'),
 ('GlobalTheory.Proof.dvr_of_reflects_facts.common','SSC7'),
 ('GlobalTheory.SelmerSameChar.sTLoc_eq','SSC8'),
 ('GlobalTheory.SelTwistLe.length_le / sT_le_sLen','SSC10'),
 ('GlobalTheory.PtSel.sel_at / selCore','SSC11'),
 ('GlobalTheory.CondTieChoice.normVal_eq_of_places','SSC12'),
 ('GlobalTheory.TameCycChoice.tameCyc','SSC13'),
 ('GlobalTheory.CondTieChoice.conductor_le_tameVal','SSC14'),
 ('GlobalTheory.PtCore.residualAbsIrredGoodPoint_of_residualIrred','SSC15'),
 ('GlobalTheory.JointSix.main','SSC16'),
]
ends=[{'endpoint':a,'claim':b,'status':'whole_original_implication_written'} for a,b in endpoints]
ends.append({'endpoint':'GlobalTheory.NLink.exists_setup_large','claim':'SSC17','status':'conditional_reduction_only',
 'qualification':'Only coherent actual HWOf/FonOf/CmpOf remains as an extra supplier; the actual SignatureChoice supplier is proved.'})
remaining=[
 'Construct actual coherent HWOf/FonOf/CmpOf across all layers from original BhattScholzeIntegral; DFD12 proves its finite-coefficient reduction only.',
 'The full original exists_setup_large producer remains conditional on that coherent Wach supplier.',
 'Actual local row estimates and all original ConclF fields on one common family remain; GLOBAL_DENOMINATOR stays open.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['exact original D7, LocTheory, local period-ring structures and coefficient bridges',
 'original Cheb in trace density and JointSix','original PtFam, NChTie, TriplesGood, SameTwist, GoodPtRow, ResAbsIrr for JointSix',
 'original ResidualIrreducibleRankR for SSC15','original TwGoodAt for KillAt','original FamP, TwGood and FactsF for SSC17',
 'actual coherent HWOf/FonOf/CmpOf only as the remaining extra supplier in SSC17'],
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'conditional_reduction_extra_inputs':{'SSC17':['actual coherent HWOf/FonOf/CmpOf supplier']},
 'arbitrary_injective_local_DVR_coefficient_changes':True,'finite_and_infinite_Selmer_lengths':True,
 'same_actual_integral_lattices_and_local_conditions':True,'same_orientation_used_twice':True,
 'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,'completed_source_endpoints':ends,
 'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],
 'whole_original_SignatureChoice_supplier_supplied':True,'whole_original_exists_setup_large_supplied':False,
 'full_GLOBAL_DENOMINATOR_supplier_supplied':False,'independent_reviews':[],'remaining':remaining})
parent=ROOT/'denominator_family_data_v51'
pp=json.loads((parent/'provenance.json').read_text());parents={c['id']:c for c in pp['claims']}
inherited=[]
for cid in sorted({d for _,deps,_,_ in CLAIMS for d in deps if d.startswith('DFD')},key=lambda x:int(x[3:])):
 c=parents[cid];pl=c['proof_location'];b=b''.join((ROOT/pl['file']).read_bytes().splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
 assert sha(b)==pl['sha256']
 inherited.append({'id':cid,'component':parent.name,'exact_parent_provenance_sha256':sha((parent/'provenance.json').read_bytes()),
  'proof_file':pl['file'],'proof_location':pl,'proof_block_sha256':sha(b),'scope_note':c['scope_note']})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[
 {'id':'SSC_ORIGINAL_DATA','kind':'original_supplied_data','statement':'Original D7, local period-ring/bridge data, prescribed tame-generator density, Cheb and precise named source premises; no new crystalline existence or automorphy premise is hidden.'},
 {'id':'SSC_LINEAR_ALGEBRA','kind':'standard_algebra_foundations','statement':'Finite-dimensional density/Burnside theorem, extension of embeddings to algebraic closures, and elementary matrix algebra. Integral trace conjugacy is proved here.'},
 {'id':'SSC_DVR','kind':'standard_commutative_algebra','statement':'DVR structure, finite torsion-free modules, faithful flatness of injective local DVR maps, module length and intersection of powers in Noetherian local rings. The problem-specific arbitrary coefficient-coordinate and normalization arguments are proved here.'},
 {'id':'SSC_LOCAL_FIELDS','kind':'standard_number_field_foundations','statement':'Compact profinite absolute Galois and closed decomposition/inertia groups, valuation extension and elementary finite-dimensional p-adic continuity. Bridge conjugacy and the needed density are proved here.'},
]})
dump('published_inputs.json',[])
(HERE/'report.txt').write_text('SELMER SIGNATURES ON THE ACTUAL FAMILY — v0.52\n'
 f'Source pin: {PIN}\nClaims: 17 (SSC1–SSC17).\nProof SHA256: {sha(raw)}\n\n'
 'Whole original JointSix.main / SignatureChoice supplier, all original premises retained.\n'
 'Integral trace conjugacy; exact local crystalline conditions; arbitrary local DVR coefficient changes;\n'
 'same-character common DVR; point-to-signature Selmer inclusion; infinity and tame-conductor cases.\n'
 'The same PtFam and oriented character are used throughout.\n'
 'SSC17 removes the separate Selmer-signature premise from DFD15. Coherent Wach/Cmp remains.\n'
 'The whole setup producer, actual ConclF family and GLOBAL_DENOMINATOR remain open.\n'
 'No selected whole closure. No Lean replay or PDF claimed. Independent review pending.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'ranges':len(sources),'inherited':len(inherited),'proof_sha256':sha(raw)},indent=2))
