#!/usr/bin/env python3
"""Rebuild exact source and written-proof locators for the HP closure."""
from pathlib import Path
import hashlib,json,re,argparse
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]/'lean-source');a=p.parse_args()
HERE=Path(__file__).resolve().parent
REPO=a.repo
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
D='src/Development/AbelianVarietyTheory/Proofs/'
I=D+'IwasawaDecomposition/'
R=D+'InertiaEigenvalues/'
F='src/Formalism/'
cache={}
def sha(b): return hashlib.sha256(b).hexdigest()
def source(path,spell,full=None,role='source endpoint or exact definition'):
 raw=(REPO/path).read_bytes();lines=raw.splitlines(keepends=True)
 # Definitions may share a short spelling only in separate files here.
 starts=[]
 for n,line in enumerate(lines,1):
  s=line.decode()
  m=re.match(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)',s)
  if m: starts.append((n,m.group(1)))
 found=[(n,name) for n,name in starts if name==spell]
 if len(found)!=1: raise ValueError((path,spell,found))
 start=found[0][0]
 following=[n for n,name in starts if n>start]
 end=min(following)-1 if following else len(lines)
 # Remove only empty trailing lines, retaining comments and namespace endings.
 while end>start and not lines[end-1].strip():end-=1
 body=b''.join(lines[start-1:end])
 rec={'path':path,'declaration':full or spell,'source_spelling':spell,'line_start':start,'line_end':end,'sha256':sha(raw),'range_sha256':sha(body),'range_bytes':len(body),'first_line':lines[start-1].decode().rstrip('\n'),'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}','role':role,'verified_equal_to_pinned_git_blob':False}
 cache[path]={'path':path,'sha256':sha(raw),'bytes':len(raw),'lines':len(lines),'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}'}
 return rec

def S(p,s,full=None,role='source endpoint or exact definition'):return (p,s,full,role)
spec={
'HP1':[
 S(F+'GradedWeylDivisibility/StatementA.lean','dualWeyl','Formalism.GradedWeylDivisibility.dualWeyl','exact polynomial model'),
 S(F+'GradedWeylDivisibility/StatementA.lean','hw','Formalism.GradedWeylDivisibility.hw','exact distinguished polynomial'),
 S(F+'LocalRingCardinality/DataCoeff.lean','nablaSq','Formalism.BasicNotions.nablaSq'),
 S(F+'LocalRingCardinality/DataCoeff.lean','sqAct','Formalism.BasicNotions.sqAct'),
 S(F+'LocalToGlobal/Divisibility/CoefMod.lean','VV','Formalism.L2.DIV.VV'),
 S(F+'LocalToGlobal/Divisibility/CoefMod.lean','actP','Formalism.L2.DIV.actP'),
 S(F+'LocalToGlobal/Columns/MtAdWt.lean','mtwHw','Formalism.L2.Col.mtwHw'),
 S(F+'LocalToGlobal/Columns/MtAdWtIrr.lean','HwFixedLine','Formalism.L2.Col.HwFixedLine'),
 S(F+'PeriodIntegrals/OrbitalBoundsConclusion/HwFixLine.lean','highest_weight_fixed_line')],
'HP2':[
 S(F+'LocalToGlobal/Columns/MtAdWtIrr.lean','HwFixedEx','Formalism.L2.Col.HwFixedEx'),
 S(F+'LocalToGlobal/Columns/MtAdWtIrr.lean','hwInStable_of','Formalism.L2.Col.hwInStable_of'),
 S(F+'LocalToGlobal/Columns/MtAdWtIrr.lean','mtw_bot_or_top','Formalism.L2.Col.mtw_bot_or_top'),
 S(F+'PeriodIntegrals/OrbitalBoundsConclusion/HwFixEx.lean','highest_weight_fixed_exists'),
 S(I+'DualWeylModuleSimpleCharZero.lean','nablaSq_simple_charZero','GlobalTheory.AlcZero.nablaSq_simple_charZero')],
'HP3':[
 S(I+'IncludeLInjective.lean','tenRepF','GlobalTheory.AlgWtF.tenRepF'),
 S(I+'IncludeLInjective.lean','wtRepF','GlobalTheory.AlgWtF.wtRepF'),
 S(I+'IncludeLInjective.lean','CMDist','GlobalTheory.AlgWtF.CMDist'),
 S(I+'WeightTensorRepOfEmbeddingsIsIrreducible.lean','GlobalTheory.AlgWtF.tenRepF_isIrreducible'),
 S(F+'LocalToGlobal/Columns/MtAdWtIrr.lean',"tenIrr_of'",'Formalism.L2.Col.tenIrr_of\u2032'),
 S(F+'LocalToGlobal/NormalizedHeckeFactors/ExpDefs.lean','IsAlgWeightF','Formalism.L2.NX.IsAlgWeightF'),
 S(I+'IsIrreducibleBaseChangeWeightTensorDualRepOfEmbe.lean','isIrreducible_bcRep_wtRepF','GlobalTheory.AlgWtBC.isIrreducible_bcRep_wtRepF')],
'HP4':[
 S(R+'AlgebraicWeightDominantIsoExists.lean','exists_equiv_VV','GlobalTheory.WtClass.exists_equiv_VV'),
 S(F+'LocalToGlobal/NormalizedHeckeFactors/RingHomOfBaseOrderToFraction.lean','evPtF','Formalism.L2.NX.evPtF'),
 S(F+'LocalToGlobal/NormalizedHeckeFactors/RingHomOfBaseOrderToFraction.lean','HWAtF','Formalism.L2.NX.HWAtF'),
 S(F+'LocalToGlobal/Columns/MtAdWt.lean','mtRep','Formalism.L2.Col.mtRep'),
 S(F+'LocalToGlobal/Columns/MtAdWt.lean','mtRep_eq_tenRep','Formalism.L2.Col.mtRep_eq_tenRep'),
 S(I+'WeightTensorDualRepDualHighestWeightAtEmbedding.lean','dd_hwAt','GlobalTheory.AlgWtF.DDHw.dd_hwAt'),
 S(I+'HighestWeightDoubleDualCoefficientSpaceUnique.lean','dd_hw_unique','GlobalTheory.AlgWtF.DDHw.dd_hw_unique'),
 S(R+'ContragredientPolynomialWeightUniqueHighestWeigh.lean','GlobalTheory.mtRatDual_hw')],
'HP5':[
 S(R+'IsAlgWeightOfContragredientHighestWeight.lean','isAlgWeight_of_hwAtF_dual','GlobalTheory.AlgWtDualRead.isAlgWeight_of_hwAtF_dual'),
 S(R+'IrreducibleWeightDescendsToPolynomialModule.lean','weight_descends','GlobalTheory.WtDescent.weight_descends'),
 S(I+'CellWeightOfAdmissibleTwist.lean','cellWt_all','GlobalTheory.LevCmp.cellWt_all'),
 S(I+'WeightMatricesMatchOfCoeffSpaceIso.lean','wtMatch_of_coef','GlobalTheory.CoefMatch.wtMatch_of_coef')],
'HP6':[
 S(I+'InfinitesimalCharacterHalfIntegral.lean','sh_half','GlobalTheory.EtaTildeShift.sh_half'),
 S(I+'CharZeroFractionRingCoefficientRing.lean','TwR.charZero_fractionRing_O','GlobalTheory.HeightCounting.TwR.charZero_fractionRing_O'),
 S(I+'CmTypeEmbeddingAtSideDistinctNonconjugate.lean','kEmbT_cmDist','GlobalTheory.HeightCounting.FormsStep.kEmbT_cmDist'),
 S(I+'ExistsWeightDataIntegral.lean','wt_weights','GlobalTheory.HeightCounting.FormsStep.wt_weights'),
 S(I+'LiftWeightParamEqInfinitesimalCharacterOfHalfInt.lean','paramV_eq_infOf','GlobalTheory.WtComb.paramV_eq_infOf'),
 S(I+'WeightTensorRepOfEmbeddingsIsIrreducible.lean','GlobalTheory.AlgWtF.tenRepF_isIrreducible'),
 S(I+'WeightTensorDualRepDualHighestWeightAtEmbedding.lean','dd_hwAt','GlobalTheory.AlgWtF.DDHw.dd_hwAt'),
 S(I+'HighestWeightDoubleDualCoefficientSpaceUnique.lean','dd_hw_unique','GlobalTheory.AlgWtF.DDHw.dd_hw_unique'),
 S(I+'IsIrreducibleBaseChangeWeightTensorDualRepOfEmbe.lean','isIrreducible_bcRep_wtRepF','GlobalTheory.AlgWtBC.isIrreducible_bcRep_wtRepF')]
}
titles={
'HP1':'The exact dual-Weyl polynomial fixed line from Gaussian elimination',
'HP2':'Highest-fixed-vector existence and absolute simplicity from the factorial pairing',
'HP3':'Absolute irreducibility on the original rational unitary group and coefficient field',
'HP4':'Algebraic classification and literal double-dual/conjugate highest-weight conventions',
'HP5':'Original-field coefficient descent and completion of the representation branch of CellWt',
'HP6':'All five clauses of the original-field wt_weights endpoint, with c2 equal to bottom'
}
deps={'HP1':[],'HP2':['HP1'],'HP3':['HP1','HP2'],'HP4':['HP1','HP2','HP3'],'HP5':['HP3','HP4','AR12','AR14'],'HP6':['HP1','HP2','HP3','HP4','MR19']}
# These edges point only to historical proved arguments with their relevant
# hypotheses explicit. No edge points from old AR/MR records back to HP.
scopes={
'HP1':'Characteristic-zero field K, dominant integer weights, literal dualWeyl/nablaSq/VV polynomial model. No bespoke unreconstructed premise.',
'HP2':'Same model; K has characteristic zero. Proves all base extensions directly. No named representation theorem retained.',
'HP3':'CM field with its actual involution; prescribed pairwise distinct, pairwise nonconjugate coefficient embeddings. Same polynomial module. No theta, Core or automorphic input.',
'HP4':'For classification: finite-dimensional irreducible rational complex representation; for HWAtF: actual CM embeddings and literal polynomial presentation. All highest-weight conclusions are proved here.',
'HP5':'Original e:K->C, complete CM type and irreducible W with stated dual HWAtF/polynomial input; AR14 retains actual MtReal, CharSide infinitesimal data, SideRead embedding square and cell base-change maps. Their existence is not asserted.',
'HP6':'Exactly the source wt_weights data and hypotheses (GlobalArtinReciprocity, D/frame/jE/SideA, star-stable LL0, integral eExp and later original TwR/RingSpec). Uses the proved MR19 row-weight/half-integrality calculation. No retained highest-weight/classification theorem.'
}
tex=(HERE/'main.tex').read_text();lines=tex.splitlines(keepends=True)
locs={}
for cid in titles:
 start=next(i for i,l in enumerate(lines,1) if l.startswith('\\paragraph{'+cid+':'))
 following=[i for i,l in enumerate(lines,1) if i>start and l.startswith('\\paragraph{HP')]
 end=min(following)-1 if following else len(lines)
 body=''.join(lines[start-1:end]).encode()
 locs[cid]={'file':'chain_closure_core/main.tex','paragraph':cid,'line_start':start,'line_end':end,'sha256':sha(body),'label':'claim:'+cid}
claims=[]
for cid in titles:
 claims.append({'id':cid,'title':titles[cid],'statement':scopes[cid],'status':'Complete human proof of the stated scope; not independently replayed in Lean','mathematical_status':'proved with explicit stated data; representation-theorem leaf closed','introduced_in':'0.23','depends_on':deps[cid],'assumptions':[scopes[cid]],'named_classical_inputs':[],'remaining_inputs':([] if cid in ['HP1','HP2','HP3','HP4'] else [scopes[cid]]),'proof_location':locs[cid],'source_relation':'Derived human alternative matching the literal polynomial definitions and endpoints; not a line-by-line translation of the internal source route.','sources':[source(*t) for t in spec[cid]],'component_ledger':'chain_closure_core/provenance.json'})
# Check exact repository object bytes, in addition to current-file hashing.
import subprocess
for path,rec in cache.items():
 blob=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
 if sha(blob)!=rec['sha256']:raise ValueError('Pinned blob mismatch '+path)
for c in claims:
 for s in c['sources']:s['verified_equal_to_pinned_git_blob']=True
out={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.23','date':'2026-11-22','repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,'component':'chain_closure_core','scope':'Closed characteristic-zero coefficient representation leaf and literal wt_weights endpoint; no full Core or RH/GRH completion.','claims':claims,'source_files':list(cache.values()),'dependency_graph':deps,'validation':{'source_files_checked_against_pinned_git_blobs':len(cache),'claim_source_links':sum(len(c['sources']) for c in claims),'main_tex_sha256':sha((HERE/'main.tex').read_bytes()),'verification_kind':'exact source-byte/range and proof-text locator checks; mathematical proof is human reasoning, not a Lean replay'}}
(HERE/'provenance.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nfile '+s['sha256']+'\nrange '+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
print(json.dumps(out['validation'],indent=2))
