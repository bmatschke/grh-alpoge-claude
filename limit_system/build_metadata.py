#!/usr/bin/env python3
"""Portable LIM source/proof binding; inputs are read-only and no Lean is run.

python build_metadata.py --source /path/to/lean_source \
    --human-root /path/to/reconstruction_v038 --peer-root /path/to/work_v039

--peer-root is accepted for the common release interface.  The S4 proof has
no peer proof dependency, so no peer file is read to establish its closure.
Only files beside this builder are written.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
parser.add_argument('--human-root', '--baseline', dest='human_root', type=Path,
                    default=HERE.parent.parent/'reconstruction_v038')
parser.add_argument('--peer-root', type=Path, default=HERE.parent)
args = parser.parse_args()
REPO, HUMAN = args.source.resolve(), args.human_root.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=REPO,
                               text=True).strip() == PIN
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P = B+'PatchingModules/'
S = P+'SeparableMatrixStability/'
A = B+'AlgebraTools/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'

# Inclusive, exact pinned ranges; last=0 means the actual final line.
SPECS = [
 ('DEFS',P+'PairedDualFirstOrderDualMatrixSpace.lean',[
  (10,49,'Loc and every Glob field, both finite local-place sets'),
  (57,99,'Original frame, G0, every Hom field and p0'),
  (103,106,'PL: original ambient open-normal residual intersection')]),
 ('DEFS',P+'ThetaCoefficientMapEq.lean',[
  (12,45,'HomL, every TWGrp field, and the exact ProL antecedent'),
  (262,299,'Close and every literal Lim field')]),
 ('DEFS',P+'PatchedSupportCompletions.lean',[
  (15,21,'S4 universal producer and original CohLim consumer')]),
 ('DEFS',B+'CommutativeAlgebra/ResMapBijective.lean',[
  (334,338,'PhiCond quantifies over every open subgroup, not only normal ones')]),
 ('TOPOLOGY',A+'QuotProf.lean',[
  (7,32,'totallyDisconnected_quot and intersection of KV for closed K')]),
 ('TOPOLOGY',A+'ProfDefs.lean',[
  (46,54,'TopGen/TopFG and exact topological closure equality')]),
 ('PL',S+'PlProps.lean',[
  (7,31,'Relative PL membership, finite-quotient criterion and finite normal core'),
  (33,116,'pl_props: normal/closed/contained, finite quotient iff, intrinsic residual')]),
 ('PL',A+'ProfDefs.lean',[
  (11,42,'IsProL, proLRes and the embedded intrinsic residual proLResOf')]),
 ('PLMAP',S+'PlMap.lean',[
  (7,26,'pl_map: equality of relative residual images under actual surjection')]),
 ('PLMAP',S+'Loc_fin.lean',[
  (36,51,'Residual functorial killing for arbitrary target subgroup Hprime')]),
 ('FINITE_CHAR',B+'GaloisLibrary/ClassFieldRamification/BurnsideHom.lean',[
  (7,30,'burnsideHom: finite ell-group character detection of a proper subgroup')]),
 ('FINITE_CHAR',A+'ProBurnside.lean',[
  (68,145,'topGen_of_hom: pro-ell character criterion and finite generator count')]),
 ('GENERATORS',S+'PlGen.lean',[
  (7,45,'pl_gen: exact Nat.card HomL <= b supplies b topological generators')]),
 ('LOCAL_QUOTIENT',S+'Loc_fin.lean',[
  (10,35,'loc_fin: one relative residual quotient is TopFG under PhiCond')]),
 ('LOCAL_QUOTIENT',S+'HomlDesc.lean',[
  (5,27,'homl_desc: continuous-character pullback injection and finiteness')]),
 ('FREE',A+'FreeProf.lean',[
  (8,34,'exists_free_profinite: free finite-list profinite universal property')]),
 ('FREE',A+'GenExt.lean',[
  (7,72,'exists_surj_over_finite: prescribed generators and common finite quotient')]),
 ('COVER',S+'SysCover.lean',[
  (8,80,'sys_cover: one finite-generated Ph, prescribed ct, all-level surjections and modH')]),
 ('COVER',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (15,22,'Original S4 theorem, supplied T.ProL, one common cover and ultrafilter')]),
 ('KERNEL',A+'ProfDefs.lean',[
  (58,73,'Exact limKer definition and normality')]),
 ('KERNEL',A+'LimKer.lean',[
  (58,114,'limKer_sup: closedness, eventual kernel joins and containment equivalence')]),
 ('KERNEL',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (23,34,'Actual K, quotient topology and finite normal-quotient separation')]),
 ('OUT',A+'FiniteHomOfTopFG.lean',[
  (13,30,'Finitely many entire continuous homomorphisms to a finite group'),
  (95,103,'finite_hom_of_topFG exact packaged endpoint')]),
 ('OUT',A+'LimOut.lean',[
  (7,144,'exists_lim_hom_out: continuous limit killing limKer and uniformity in all cover elements')]),
 ('OUT',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (35,64,'Actual quotient h, surjectivity, outgoing uniform limit, ct and all-level modH')]),
 ('IN',S+'InLim.lean',[
  (68,148,'Finite homomorphism stabilization through one TopFG quotient'),
  (150,249,'in_lim: continuous incoming homomorphism and uniform Close in all y')]),
 ('IN',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (65,83,'Exact Y/f0/fN local lift and equality of its composite with original f0')]),
 ('COMPAT',S+'CloseMap.lean',[
  (6,35,'close_map: exact comparison of the limiting image in the original global group')]),
 ('LOCAL_MAPS',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (84,99,'Both original local groups, PhiCond, actual maps and eta-kernel values'),
  (116,128,'Kernel codrestriction and all original Hom local compatibility fields'),
  (203,204,'Finite-place intersections for literal phi_lim and phiu_lim')]),
 ('ELEMENTS',S+'EltLim.lean',[
  (5,11,'elt_lim: actual element lifting and Close at every finite quotient')]),
 ('ELEMENTS',A+'LimElt.lean',[
  (7,28,'exists_lim_elt: ultrafilter element convergence in the fixed compact cover')]),
 ('ELEMENTS',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (129,164,'Actual ph/ta limits, guarded ph_lim and exact global images')]),
 ('COMMUTE',S+'CommLim.lean',[
  (8,93,'comm_lim: tame relation, ell-power finite order, tail and exact commutation')]),
 ('COMMUTE',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (165,180,'Original tame and ProL fields supply exact commutation hypotheses')]),
 ('ASSEMBLY',S+'SelmerCocyclesLimitAndDescentProperties.lean',[
  (100,128,'Every original Glob and Hom field on the same quotient'),
  (181,211,'Final every-field Lim assembly, all simultaneous quantifiers')]),
 ('CONSUMER',S+'SecondSelmerSpanBoundAtAllLevels.lean',[
  (19,43,'Actual p0 continuity/surjectivity/conjugation and local compatibility'),
  (111,164,'Common eta kernel/cover, all-level transport and all-truncation counts'),
  (246,259,'TWQuot record: actual separate quotient input to the selected route')]),
 ('CONSUMER',P+'AutomorphicDetection/CohLim.lean',[
  (12,21,'Original same-Lim B1/B2/Eig/ProL CohLim consumer')]),
 ('CONSUMER',P+'PatchedSupportCompletions.lean',[
  (189,213,'Exact Core, CoreBC, Raw and original same-J data')]),
 ('CONSUMER',S+'RawMain.lean',[
  (12,48,'Actual matched TWQuot and full descent then CoreBC -> Raw')]),
 ('OUTER',D+'LinkTwo.lean',[
  (13,51,'Both rank-four Links and the same ideal Hida/P1 quantifier scope')]),
 ('OUTER',D+'PotentialModularityTower.lean',[
  (38,66,'Fixed iota and one common coefficient threshold in PMExAlt')]),
 ('OUTER',P+'TaylorWilesObstructionBound.lean',[
  (23,31,'Original complete CohP'),
  (115,154,'Original LocCFT, all-level HasAut and actual PfromAut consumer')]),
]

cache, sources, groups = {}, [], {}
for group, path, ranges in SPECS:
    if path not in cache:
        raw = (REPO/path).read_bytes()
        blob = subprocess.check_output(['git','show',f'{PIN}:{path}'], cwd=REPO)
        assert raw == blob, path
        cache[path] = raw
    raw = cache[path]
    lines = raw.splitlines(keepends=True)
    for first,last,decl in ranges:
        last = last or len(lines)
        assert 1 <= first <= last <= len(lines), (path,first,last,len(lines))
        block = b''.join(lines[first-1:last])
        item = dict(id=f'LIM_SRC_{len(sources)+1:03}',group=group,path=path,
          declaration=decl,line_start=first,line_end=last,
          sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(block),
          range_bytes=len(block),source_commit=PIN,
          url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{first}-L{last}')
        sources.append(item)
        groups.setdefault(group,[]).append(item['id'])

def proof_block(raw,cid):
    lines=raw.splitlines(keepends=True)
    starts=[i for i,l in enumerate(lines) if l.strip()==f'% BEGIN {cid}'.encode()]
    if starts:
        ends=[i for i,l in enumerate(lines) if l.strip()==f'% END {cid}'.encode()]
        assert len(starts)==len(ends)==1,cid
        first,last=starts[0],ends[0]
    else:
        lab=next(i for i,l in enumerate(lines) if f'\\label{{claim:{cid}}}'.encode() in l)
        first=max(i for i in range(lab+1) if b'\\paragraph{' in lines[i])
        last=next((i-1 for i in range(lab+1,len(lines)) if b'\\paragraph{' in lines[i]),len(lines)-1)
    assert first<last,cid
    block=b''.join(lines[first:last+1])
    return dict(id=cid,line_start=first+1,line_end=last+1,sha256=sha(block),bytes=len(block))

CG={
 1:['DEFS','TOPOLOGY'],2:['DEFS','PL'],3:['DEFS','PL','PLMAP'],
 4:['FINITE_CHAR'],5:['DEFS','FINITE_CHAR','GENERATORS','TOPOLOGY'],
 6:['DEFS','PL','PLMAP','LOCAL_QUOTIENT'],7:['FREE','TOPOLOGY'],
 8:['DEFS','GENERATORS','FREE','COVER'],9:['DEFS','KERNEL','TOPOLOGY'],
 10:['OUT','KERNEL','TOPOLOGY'],11:['DEFS','OUT','COVER'],
 12:['DEFS','IN','LOCAL_QUOTIENT','OUT','KERNEL'],
 13:['DEFS','IN','COMPAT','OUT','KERNEL'],14:['DEFS','LOCAL_MAPS','IN'],
 15:['DEFS','ELEMENTS','COMPAT','OUT'],16:['DEFS','COMMUTE','PL','KERNEL'],
 17:['DEFS','LOCAL_MAPS','ASSEMBLY','OUT'],18:['DEFS','ASSEMBLY','COVER','KERNEL'],
 19:['DEFS','CONSUMER','OUTER']}
DEP={
 1:[],2:['LIM1'],3:['LIM1','LIM2'],4:[],5:['LIM1','LIM4'],
 6:['LIM1','LIM2','LIM3','LIM5'],7:['LIM1'],
 8:['LIM1','LIM2','LIM5','LIM7'],9:['LIM1','LIM8'],
 10:['LIM1','LIM8','LIM9'],11:['LIM1','LIM8','LIM9','LIM10'],
 12:['LIM1','LIM6','LIM8','LIM9','LIM10'],
 13:['LIM1','LIM9','LIM10','LIM11','LIM12'],14:['LIM6','LIM13'],
 15:['LIM1','LIM8','LIM9','LIM10','LIM11'],
 16:['LIM1','LIM2','LIM8','LIM9','LIM15'],
 17:['LIM1','LIM9','LIM11','LIM14','LIM15'],
 18:['LIM1','LIM8','LIM9','LIM10','LIM11','LIM14','LIM15','LIM16','LIM17'],
 19:['LIM18','CRW12','CRW13','CRW14','CRW15','QX4','QX10','YX2','KA5','KA6']}
HYP={
 1:['Original compact totally disconnected topological groups; closed normal K; all open normal finite coordinates.'],
 2:['ell prime; Gamma profinite; H is the original ambient open normal subgroup; PL defined through ambient open normal U with the original all-h power condition.'],
 3:['Continuous f of profinite groups, open normal H and arbitrary target subgroup Hprime with f(H)<=Hprime; equality additionally requires Hprime open normal, f surjective, H=f^{-1}Hprime.'],
 4:['Finite ell-group and a proper subgroup; no finite-generation theorem is assumed.'],
 5:['A pro-ell; full continuous character set finite; actual cardinality bound |HomL|<=b.'],
 6:['The original PhiCond on every open subgroup of Y; A=f0^{-1}H; actual continuous fN with pN fN=f0 and T.ProL at every level.'],
 7:['A finite number of prescribed generators and arbitrary profinite target; only the maximal-filter principle and explicit finite quotients.'],
 8:['The same original T with T.ProL, actual finN/hb, every pN surjective, and original c compatibility; one cover for all N.'],
 9:['One ultrafilter extending all cofinite subsets of N; the actual normal kernels of the common cover maps. Each open normal V has its own allowed eventual set.'],
 10:['One finite-generated cover Pi; actual continuous surjective FN=pN piN; uniform convergence of entire maps modulo each W.'],
 11:['The exact K and F already constructed; original all-level common quotient modulo H; same prescribed ct.'],
 12:['One fixed local quotient Y/PY from LIM6; every fN kills that same PY; finite target Pi/KV and the same ultrafilter/kernel stabilization.'],
 13:['Compatible whole local homomorphisms aV; source Close orientation x^{-1}xprime in V; exact pN fN=f0.'],
 14:['Both original finite local-place sets and all original local group elements; actual phiV/phiU and Glob.Hom local-map compatibility; same L, Pi, U, h and piN.'],
 15:['Actual all-level ph/ta and source guarded ph_lim, T.ProL at level zero, exact ta_ker, finite original q, one same U<=atTop.'],
 16:['Actual tame relation made exact by T.ProL; actual Nq congruent 1 modulo ell^N; finite ell-group image of HN; threshold may depend on the one finite quotient V.'],
 17:['Same quotient, original eta0/epsilon0/c0 and both local maps; c_N^2=1 at every level; exact original Glob/Hom fields.'],
 18:['Every original TWGrp T and its literal T.ProL antecedent; all primes ell including 3; no weakened Lim record.'],
 19:['Selected odd-prime Count-II scope, including ell=3; same matched pro-ell T, rank-four a=n point and chosen g=0 Kap, original B1 with C before m before eventual N and coupled B2; no new ordinary/TWAut/support producer.']}

tex=(HERE/'main.tex').read_bytes()
claims=[]
for i in range(1,20):
    cid=f'LIM{i}'
    block=proof_block(tex,cid)
    text=b''.join(tex.splitlines(keepends=True)[block['line_start']-1:block['line_end']]).decode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',text).group(1)
    assert f'\\label{{claim:{cid}}}' in text,cid
    claims.append(dict(id=cid,title=title,introduced_in='0.39',classification='B',
      status='complete independent human proof at the printed exact scope',
      depends_on=DEP[i],classical_inputs=[],original_hypotheses=HYP[i],
      dependency_scope=('Standalone generic relative-residual theorem; no S4 or arithmetic quotient producer is used.' if i in [2,3] else
        'The complete original universal S4 is proved, with its original T.ProL antecedent and every Lim field.' if i==18 else
        'Installs this actual Lim in the previously proved selected CRW cohomology implication; other actual arithmetic/patching producers remain explicit.' if i==19 else
        'Only the indicated preceding proved lemmas and original fields are used; no pointwise compactness substitute for uniform map convergence.'),
      proof_location=dict(file='limit_system/main.tex',label='claim:'+cid,**{k:v for k,v in block.items() if k!='id'}),
      source_groups=CG[i],sources=[s for s in sources if s['group'] in CG[i]]))

inherited=[]
for path,ids,role in [
 ('count_raw/main.tex',['CRW12','CRW13','CRW14','CRW15'],
  'Exact selected finite cocycle transport, constant-preserving B1-to-K1, Laurent bound and chosen g=0 K2/K3 on the actual same Lim.'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],
  'Both original rank-four Links and same-ideal Hida/P1 scope; boundary retained.'),
 ('case_two_installation/main.tex',['YX2'],
  'Original fixed-iota/common-threshold Count-II consumer; boundary retained.'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],
  'Two-primary target removes only Case III; RH still uses I/II/V, full Dirichlet GRH also uses III.')]:
    raw=(HUMAN/path).read_bytes()
    inherited.append(dict(path='reconstruction_v038/'+path,sha256=sha(raw),claim_ids=ids,
      claim_proof_blocks=[proof_block(raw,cid) for cid in ids],role=role))
known={c['id'] for c in claims}|{cid for item in inherited for cid in item['claim_ids']}
assert all(d in known for ds in DEP.values() for d in ds)

dump('published_applications.json',[])
remaining=copy.deepcopy(json.loads((HUMAN/'count_raw/closure.json').read_text())['remaining'])
for item in remaining:
    if item['id']=='JSP_SINGLE_POINT_RAW':
        item['new_progress']='LIM1-LIM18 construct the entire original S4; LIM19 installs it in CRW12-CRW15. The companion PQL packet supplies the actual TWQuot and full CoreBC=>Raw descent; neither S4 nor that descent is a current release residual.'
        item['remaining_contract']='Supply the original normalized Core limiting ring/maps/modules and the one-point S5 support dimension/fiber/annihilator contracts, together with the original Core-to-CoreBC coefficient normalization and Unit-parameter construction. Everything stays on the same selected point/Kap/T/TWPl/TWAut and original B,J. Original ordinary/control, four Hida and same-J HasAut remain separate producers.'

closed=[
 dict(id='LIM_RELATIVE_PROELL_RESIDUAL',classification='B',by=['LIM2','LIM3'],
  scope='Exact relative ambient PL equals intrinsic pro-ell residual; finite-quotient criterion and pro-ell quotient; continuous functoriality for arbitrary target subgroup and equality for a surjection onto an open normal target subgroup with full preimage.',
  conditional_inputs='Only the printed profinite/open-normal/continuity hypotheses; no S4 or actual arithmetic quotient.'),
 dict(id='ORIGINAL_S4',classification='B',by=[f'LIM{i}' for i in range(1,19)],
  scope='For every prime ell, original Loc L, Glob G0 and TWGrp T, T.ProL -> Nonempty(Lim T), with every literal field and one common cover/ultrafilter; includes ell=3.',
  conditional_inputs='The original T.ProL antecedent. This is part of S4 itself, not a new assumed limit-system producer.'),
 dict(id='SELECTED_COH_LIM_WITH_CONSTRUCTED_LIMIT',classification='B',by=['LIM18','LIM19','CRW12','CRW13','CRW14','CRW15'],
  scope='Original selected K1/Laurent K1/K2/K3 on the actual constructed Lim for the same matched pro-ell T and chosen full-block g=0 Kap; exact D0 and B1 constant order.',
  conditional_inputs='The original matched T.ProL, selected point and actual B1/coupled B2. The companion matched arithmetic descent and all other actual producers keep their exact scopes.')]
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.39',component='limit_system',
 source_commit=PIN,proof_sha256=sha(tex),proof_file_sha256=sha(tex),proof_claims=[c['id'] for c in claims],
 closed=closed,remaining=remaining,classical_input_nodes=[],
 selected_frontier_status={
  'ORIGINAL_S4':'CLOSED B: full universal S4, including uniform local-map convergence over every local element and place.',
  'SELECTED_COH_LIM':'The actual Lim input is now constructed after the original matched ProL transport; CRW selected cohomology bounds apply without a new limit hypothesis.',
  'ORIGINAL_PROELL_DESCENT':'Supplied by the separate companion PQL packet, not claimed as a LIM proof and not a current release residual.',
  'JSP_SINGLE_POINT_RAW':'OPEN C: normalized Core compatible limiting rings/maps/modules and one-point S5 support, plus original Core-to-CoreBC coefficient normalization/Unit.',
  'COUNT_II_SUPPORT':'OPEN C: ordinary/control/type/neatU/TThetaEx, four Hida endpoints, same-J HasAut and narrowed selected Raw; unchanged complete CohP/LocCFT.',
  'RH_case_note':'Only Case III has the proved two-primary-target vacuity; RH still needs I/II/V and full Dirichlet GRH also needs III.'},
 sufficient_rules=[
  dict(conclusion='ORIGINAL_S4',logic='PROVED_UNIVERSAL',requires=['CERT_LIM1_LIM18'],binding='Every original prime ell, Loc L, Glob G0 and TWGrp T; the theorem itself retains T.ProL as its antecedent.'),
  dict(conclusion='SAME_ORIGINAL_LIM',logic='AND',requires=['SAME_ORIGINAL_T','SAME_T_PROL','CERT_LIM18'],binding='The Lim is built for that literal T, with one common Pi,U,piN,G,h and every field.'),
  dict(conclusion='SELECTED_K1_WITH_CONSTRUCTED_LIMIT',logic='AND',requires=['SAME_MATCHED_PROL_T','SAME_SELECTED_POINT_AND_KAP','SAME_SELECTED_B1','CERT_LIM18_LIM19','CERT_CRW12_CRW15'],binding='Odd ell including 3; a=n=4,g=0; one B1 constant before all m and original levels; no Sel1 vanishing.'),
 ],
 nonlogical_shared_links=[
  dict(source='LIM2-LIM3',target='PQL_ACTUAL_TWQUOT',reason='Independent generic residual facts may support the companion quotient construction; no dependence on S4 and no logical cycle.'),
  dict(source='PQL_COREBC_TO_RAW',target='JSP_SINGLE_POINT_RAW',reason='The companion exact arithmetic descent removes that separate release subproducer; it does not supply normalized Core patching or ordinary data.'),
  dict(source='LIM18',target='ORIGINAL_PATCHED_SUPPORT',reason='Supplies its actual Lim input, but constructs no RRObj/RMaps/PMod or support prime.'),
  dict(source='LIM19',target='JSP_SAME_IDEAL_HASAUT',reason='Retains the originally supplied same-J system; no automorphic module producer is inferred.')],
 not_claimed_closed=['normalized Core limiting RRObj/RMaps and compatible patched modules','one-point S5 support dimension/fiber/annihilator producer','Core-to-CoreBC coefficient normalization and Unit parameter','JSP_SINGLE_POINT_RAW','ordinary/control/type/neatU/TThetaEx','four Hida endpoints','same-J all-level HasAut','complete CohP','LocCFT','COUNT_II_SUPPORT','Count I','Count V','unrestricted Count III'],
 quantifier_guards=[
  'S4 is proved for every prime ell and every original T with T.ProL, not just the selected rank-four arithmetic system.',
  'One finite-generated Pi and one U<=atTop precede all limit maps and auxiliary elements; every original level N remains.',
  'For each open normal V, ker_lim has one eventual set; no one-set-for-all-V assertion is made.',
  'For each open normal W of G0, p_lim is eventual uniformly for every x in Pi.',
  'For each open normal V of Pi, phi_lim and phiu_lim are eventual uniformly over all original local places and every local group element.',
  'Close retains x^{-1}xprime in V, not its image in an unspecified larger quotient.',
  'PhiCond retains its exact every-open-subgroup quantifier and is applied to the one fixed f0^{-1}H.',
  'The residual in the tame relation is killed by the exact all-level ProL field; finite-order and Nq congruence give exact commutation.',
  'All eta, epsilon, c, local maps, ph/ta and their global images refer to the same original T and L.',
  'At the arithmetic consumer both rank-four Links, fixed iota, one common coefficient threshold, ell=3 and each original same ideal J are preserved.',
  'Chosen g=0 B2 remains coupled to the same point/Kap/B1; no universal arbitrary-Kap or Sel1=0 inference.',
 ],formal_correctness_assumed=True,new_lean_build=False,
 peer_review='pending independent mathematical and source review of the final proof and metadata hashes')
dump('closure.json',closure)

prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.39',date='2026-11-22',
 source_commit=PIN,component='limit_system',main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,
 source_groups=groups,source_inventory=sources,
 source_files=[dict(path=path,sha256=sha(raw),full_file_sha256=sha(raw),bytes=len(raw)) for path,raw in sorted(cache.items())],
 inherited_proof_inputs=inherited,peer_proof_inputs=[],
 published_applications=dict(file='published_applications.json',sha256=sha((HERE/'published_applications.json').read_bytes()),ids=[]),
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes()),portable=True,
   arguments=['--source','--human-root','--peer-root'],read_only_inputs=['pinned Lean checkout','reconstruction_v038'],peer_root_read_for_proof=False),
 validation=dict(pinned_blob_verified_files=len(cache),source_ranges=len(sources),
  distinct_source_ranges=len({(s['path'],s['line_start'],s['line_end']) for s in sources}),
  claim_source_ranges=sum(len(c['sources']) for c in claims),all_source_ranges_exact=True,
  claim_proof_blocks=len(claims),inherited_claim_proof_blocks=sum(len(x['claim_proof_blocks']) for x in inherited),
  new_lean_build=False,independent_human_mathematical_proof=True),
 scope_note='Nineteen complete B proofs. LIM18 supplies the entire original S4; relative-PL facts are independent of that construction. Uniform local maps are built from finite Hom sets on one common quotient, with all original fields preserved. Other arithmetic and patching producers remain explicit.')
dump('provenance.json',prov)
loc=[f'LIM1-LIM19 exact source locators; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc.extend([f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",
      'file_sha256='+s['sha256'],'range_sha256='+s['range_sha256'],s['url'],''])
(HERE/'source_locators.txt').write_text('\n'.join(loc))

report=f'''LIM1-LIM19 — complete original limit system, v0.39

Source correctness is assumed; no Lean build or replay was performed.
Commit {PIN}
main.tex SHA256 {sha(tex)}
provenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}
closure.json SHA256 {sha((HERE/'closure.json').read_bytes())}

ACTUAL CLOSED PRODUCER

The whole original S4 is proved: for every prime ell, original Loc L,
Glob G0 and TWGrp T with T.ProL, construct a literal Lim(T).  Every field
is checked in LIM18.  There is one common finitely generated profinite
cover, one free ultrafilter above atTop, all original surjections and
distinguished ct, one closed limit kernel, the same quotient Glob and
Hom, exact all-level modH, uniform outgoing convergence, both complete
uniform local-map families, all auxiliary ph/ta limits, exact commutation
and their prescribed global images.  The scope includes ell=3 and ell=2.

SUBSTANTIVE PROOF POINTS

LIM1-LIM3 prove the required compact finite-quotient facts and the precise
relative ambient PL statements, including its intrinsic interpretation,
pro-ell quotient, finite-quotient criterion and functoriality.  They do not
depend on S4, so the companion actual quotient proof can use them without
a cycle.  LIM4-LIM5 reconstruct the finite ell-group character criterion
and the exact |HomL|<=T.hb generator bound.  LIM7-LIM8 construct the common
free profinite cover with c_N and the all-N common quotient modulo H.

LIM9 constructs K by finite subgroup stabilization and proves the literal
eventual equality ker(pi_N)V=KV for each original open normal V.  LIM10
selects whole outgoing homomorphisms in each finite quotient, proving
uniform convergence in every element of the common cover and surjectivity.

LIM6 and LIM12-LIM14 are the decisive local argument.  PhiCond is retained
with its actual every-open-subgroup quantifier.  One fixed local quotient
Y/PL(f0^{-1}H) is topologically finitely generated, and every level map
kills that same residual.  There are only finitely many continuous maps
from this quotient into Pi/KV.  Their ultrafilter stabilization is equality
of entire homomorphisms, so the result is uniform in all y, not merely
pointwise.  Compatibility and the inverse-limit construction give an actual
continuous map to Pi/K whose composite is exactly f0.  The source Close
relation, with x^{-1}xprime in V, is proved by altering one lift by ker(pi_N).
Finite intersections give one eventual set for all original local places.

LIM15-LIM16 retain the actual ph_N/ta_N and use the guarded original ph_lim,
ProL, ta_ker and Nq=1 modulo ell^N.  In each fixed finite quotient the tame
image has bounded ell-power order.  A permitted tail therefore makes its
power in the tame relation equal to itself, proving exact limit commutation.
This does not assert that the tame element or Sel1 vanishes.

CONTRIBUTION AND REMAINING CUT

LIM19 installs this actual Lim in CRW12-CRW15 on the same selected odd-prime
full-block point and chosen g=0 Kap, with the exact B1 constant before every
m and eventual N.  This closes the formerly supplied-Lim dependency.
The companion PQL packet supplies actual TWQuot and full CoreBC=>Raw
descent; that companion proof is not used circularly to prove S4.
The current residual arithmetic cut is normalized Core's compatible
limiting ring/maps/modules and one-point S5 support dimension, fiber and
annihilator identities, plus the original Core-to-CoreBC coefficient
normalization and Unit parameter.  Raw and Count-II support remain open.

Ordinary/control/type/neatU/TThetaEx, four Hida endpoints, same-J all-level
HasAut and the complete original CohP/LocCFT remain unchanged.  Both actual
rank-four Links, fixed iota followed by one common threshold, ell=3 and each
original same ideal J are preserved.  RH still requires I/II/V; unrestricted
Dirichlet GRH also retains III.  No alleged formal-source gap is introduced.

METADATA AND VALIDATION

{len(claims)} marked human proof blocks; {len(cache)} exact pinned source
files; {len(sources)} listed source ranges; {sum(len(c['sources']) for c in claims)}
claim/source occurrences; {sum(len(x['claim_proof_blocks']) for x in inherited)}
inherited proof blocks.  All source bytes equal the pinned git blobs.
published_applications.json is empty because all new mathematics here is
independently reconstructed.  The portable builder accepts --source,
--human-root and --peer-root, writes only this component, and reads no peer
file to prove S4.  Standalone draft TeX validation is recorded separately
under validation/.  Independent final-byte review is pending.
'''
(HERE/'report.txt').write_text(report)
print(json.dumps(dict(claims=len(claims),source_files=len(cache),source_ranges=len(sources),
 claim_source_ranges=sum(len(c['sources']) for c in claims),inherited_blocks=sum(len(x['claim_proof_blocks']) for x in inherited),
 main_sha256=sha(tex),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
 closure_sha256=sha((HERE/'closure.json').read_bytes())),indent=2))
