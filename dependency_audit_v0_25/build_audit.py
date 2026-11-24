#!/usr/bin/env python3
"""Build the v0.25 semantic sufficient-condition audit, never altering history."""
from pathlib import Path
import argparse, copy, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OLD=WORK/'dependency_audit_v0_24'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
P='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
D=P+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
COMPONENTS=['local_k_duality','torsion_homology','k_theory_bridge','simultaneous_cohomological_windows','count_z_closure']

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main(repo):
 blobs={};source_index={}
 def blob(path):
  if path not in blobs:
   b=(repo/path).read_bytes();assert b==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path;blobs[path]=b
  return blobs[path]
 def verify(a):
  b=blob(a['path']);frag=b''.join(b.splitlines(keepends=True)[a['line_start']-1:a['line_end']]);assert sha(b)==a['sha256'],a['path'];assert sha(frag)==a['range_sha256'],(a['path'],a['line_start']);assert PIN in a['url'];source_index[(a['path'],a['line_start'],a['line_end'])]=copy.deepcopy(a);return a
 def anchor(path,decl,start=None,end=None):
  b=blob(path);lines=b.decode().splitlines()
  if start is None:
   pat=re.compile(r'^(?:private\s+)?(?:theorem|def|abbrev|structure)\s+'+re.escape(decl)+r'(?=[\s:(])')
   hits=[i+1 for i,s in enumerate(lines)if pat.match(s)];assert len(hits)==1,(path,decl,hits);start=hits[0]
  if end is None:
   end=len(lines)
   for i in range(start,len(lines)):
    if re.match(r'^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure|section|namespace|end|variable|instance|attribute|open)\b|^@\[',lines[i]):end=i;break
   while end>start and not lines[end-1].strip():end-=1
  frag=b''.join(b.splitlines(keepends=True)[start-1:end])
  return verify({'path':path,'declaration':decl,'line_start':start,'line_end':end,'sha256':sha(b),'range_sha256':sha(frag),'range_bytes':len(frag),'first_line':lines[start-1],'url':REPO+'/blob/'+PIN+'/'+path+f'#L{start}-L{end}','verified_equal_to_pinned_git_blob':True})

 baseline=read(OLD/'obligation_map.json')
 oldtargets=read(OLD/'next_targets.json')['targets']
 for a in oldtargets:verify(a)
 for a in read(OLD/'source_anchors.json')['sources']:verify(a)
 retirement={
  'DA-next-01-a':(['TW8'],'Literal one BConst K for every Ct>=1, both original two-primary and all prescribed reference-layer models.'),
  'DA24-K-01':(['KB8'],'Literal LemmaK with universal C_K=31 on every original L,Omega,D,ell,e.'),
  'DA24-K-02':(['KB4'],'Actual KBridge with canonical finite Quillen K module and maps into original compact H2 and HGL tensor.'),
  'DA24-K-03':(['KB8','TB10','LD3','LK2','LK3'],'Complete KBridge/torsion/cohomology reduction to actual LemmaK31.'),
  'DA24-K-04':(['TB10'],'All-prime actual HGL torsion bound TorsBoundPow22; no small-prime exclusion.'),
  'DA24-LK-01':(['LK2'],'Literal LocalFinitenessK, all finite nonfree coefficients and every prime.'),
  'DA24-LK-02':(['LK3'],'Literal LocalTateDualityK, actual cycK, H2 invariant and all four cup bijections.'),
  'DA24-LK-03':(['LK4'],'Literal LocalEulerCharK with the residue-characteristic factor |M|^[K:Q_l].'),
  'DA24-FW-01':(['TW1'],'Exact finite-layer bounded class-group l-rank specialization from matched FW/Iwasawa/class-field inputs, including l=2.'),
  'DA24-HV-05':(['CZ6'],'Literal PropZ and CountZ, with uniform exponent C=0 and original Omega/O/host.')
 }
 updates={
  'DA-next-01-b':{'human_status':'PointHV_open_four_count_suppliers_and_actual_assembly_remain',
   'supplied_by':['LD3','LK2','LK3','KB8','CZ6'],
   'supplied_parts':['Exact finite Poitou–Tate premise','Exact native local-K finiteness and duality','Literal LemmaK31','Literal CountZ with C=0'],
   'remaining_human_scope':'Supply actual CountI, CountII, CountIII and CountV, then reconstruct their common-constant sums and layer descent, CountVs/CountIV uses, and the literal PointHV field/host/reference-layer quantifiers. The source implication is not itself a new human proof.',
   'retained_inputs':'CountI/II/III/V and the actual compatible PointHV assembly. The local-K, LemmaK and CountZ premises are now supplied in their exact scopes.'},
  'DA24-HV-06':{'human_status':'CountI_Kato_and_unitary_automorphy_supplier_retained',
   'supplied_by':['KB8'], 'supplied_parts':['Literal LemmaK31 premise only'],
   'remaining_human_scope':'Reconstruct actual InpZ/cohomology package, RigII from KatoTwo and its modularity/adjoint inputs, AdVanishK, rank-three congruence-number theorem, AutomorphyUnramifiedCoefficients, and the OneChar -> PropGK -> CorGK -> CountI chain. LitN and native non-K/normalized cohomology packages are not certified solely by LK/LD.',
   'retained_inputs':'Actual local/global cohomology package, LemmaM/Mprime/P, KatoTwo/RigII, adjoint vanishing, modularity, rank-three counting and compatible characteristic-zero automorphy.'}
 }
 for tid in ['DA24-HV-01','DA24-HV-02','DA24-HV-03','DA24-HV-04']:
  name={'DA24-HV-01':'CountI','DA24-HV-02':'CountII','DA24-HV-03':'CountIII','DA24-HV-04':'CountV'}[tid]
  updates[tid]={'human_status':'actual_'+name+'_supplier_still_open','supplied_by':[],
   'remaining_human_scope':'Literal '+name+' on the original hosts, coefficients, characters and twists, with its uniform constants chosen before varying host data. The exact deeper entry route is recorded in the v0.25 count frontier; new local-K/LemmaK results do not by themselves supply the required automorphy, rigidity or trace-counting content.',
   'retained_inputs':'Actual arithmetic '+name+' supplier and its same-object transports.'}
 targets=[];retired=[]
 for old in oldtargets:
  q=copy.deepcopy(old);q.setdefault('history',[]).append({'version':'0.24','snapshot':copy.deepcopy(old)})
  if q['id'] in retirement:
   suppliers,scope=retirement[q['id']];q.update({'status':'safe_to_retire_in_stated_scope','supplied_by':suppliers,'closed_scope':scope});retired.append(q)
  else:
   q.update(updates.get(q['id'],{}));targets.append(q)
 assert {a['id']for a in retired}==set(retirement)

 def target(tid,path,decl,scope,premises,package='actual_point_counts',**kwargs):
  a=anchor(path,decl,**kwargs);a.update({'id':tid,'work_package':package,'human_status':'precise_continuation_target_only','status':'human_proof_retained','remaining_human_scope':scope,'retained_inputs':premises,'downstream':'PointHV -> VW3/VW4 -> original VWinAt -> QP22 fixed-pair windows','priority_group':4});targets.append(a);return a
 target('DA25-HV-01',P+'UnitaryThreeGroups/CountI.lean','UpperTheory.V.U3.countI',
  'Complete finite-prime and character-orbit aggregation from actual CorGK, fixing Kstar(pK chi), r1,r2,C before the host and retaining arbitrary original coefficient families and finite prime sets.',
  'Actual CorGK; its OneChar/PropGK supplier remains substantive. Do not substitute the different fixed-exponent CorG predicate without proving a matching theorem.')
 target('DA25-HV-02',P+'ModularityArgument/KatoQuadraticCharacters/OneChar.lean','UpperTheory.V.Z.Kato.oneChar',
  'Actual one-character Selmer bound by valuations of trace differences for the compatible rank-three/rank-two automorphic points; carry through PropGK and CorGK before CountI.',
  'InpZ (actual CohInp plus LemmaM/Mprime/P, RigII, AdVanishK, CongruenceNumberRankThree) and AutomorphyUnramifiedCoefficients. RigII retains KatoTwo with its Used hypotheses, adjoint vanishing and modularity transfer.')
 target('DA25-HV-03',D+'ConductorAtMapInjectiveCoeff.lean','UpperTheory.V.Th.sp4Main_alt',
  'One complete joint CountII/CountIII supplier: same Raw object and Good/OfCase data, trace nonvanishing, finite-model inequalities, auxiliary coefficient extension, exact character order/kernel/conductor/parity, and descent of normalized Vlen.',
  'SymplecticFourImageDense; CohomologyHyp; LemmaM/Mprime/P; NumberSp4Alt; RigiditySymplecticFour; CorX; SoV and SoFin for every original Omega and ell.')
 target('DA25-HV-04',D+'IsAut4.lean','SymplecticFourImageDense',
  'Supply the actual D.Fin0, D.NoEnd and one embedding iota making every relevant irreducible point automorphic for each original host/Raw object. A generic automorphy theorem without these restrictions and ties is insufficient.',
  'Rank-four symplectic automorphy/finite-point/non-endoscopic supplier on the specified Raw family.')
 target('DA25-HV-05',P+'LevelCohomology/ChrInvNeg.lean','UpperTheory.V.X.corX',
  'Complete residual rank-one vanishing CorX on the original residue field, including both character and inverse character and the tame-index UnrEv condition.',
  'Literal LemmaX generalized Bernoulli unit at the stated large 2-power conductor, and UnramifiedCocycleIsCoboundaryOfBernoulliUnit; both have source proofs requiring readable finite arithmetic reconstructions.')
 target('DA25-HV-06',P+'LevelCohomology/ExistsAb.lean','UpperTheory.V.X.soFin',
  'Prove the original arbitrary finite-order character strict-Selmer length finite by same-closure abelian root-containing extension, restriction/control, H0 bound and normalized length transfer.',
  'KB8/LD3/LK2/LK3 now supply the named premises. Actual upV/shaLeV/H0 descent and coefficient transport in this endpoint remain to be written; TW3 supplies only its stated root-containing strict-Selmer comparison.')
 target('DA25-HV-07',P+'LevelCohomology/FdAdjoinRange.lean','UpperTheory.V.X.soBar',
  'Prove SoV for actual continuous PadicAlgCl-valued negative-twist cocycles, including finite-extension capture by the Baire/cocycle argument, a compatible coefficient lattice and the passage from finite Selmer length to vector vanishing.',
  'KB8/LD3/LK2/LK3 supply the named theorem premises, but no general compact subset of PadicAlgCl is silently assumed to lie in a finite extension. The cocycle argument and local witnesses must be reconstructed.')
 target('DA25-HV-08',D+'CountVOf.lean','UpperTheory.V.UnitaryThreeInertia.countV_of_finiteness_duality_euler_host',
  'Full CountV on original frames: choose the Gaussian base field, install hostFrame and marked point, construct the actual universal deformation ring, apply compatible automorphy/finiteness/counting/rigidity, and descend the original Vlen with one exponent.',
  'ThmS6_s; LemmaM/Mprime; native LocalFiniteness, LocalTateDuality, LocalEulerChar; GlobalFiniteness and GlobalEulerChar; Published.PoitouTateNormalised; HostVanE, HostXpp, HostRigid_s and HostNumber_s. These non-K/normalized interfaces are not automatically closed by LK/LD.')
 target('DA25-HV-09',D+'HostNumberS.lean','HostNumber_s',
  'Actual same-frame trace-separating element and valuation sum, with one C chosen before Omega,ell,O,N,e,psi, frame, embedding and marked point; preserve pairwise nonisomorphism on the actual eta kernel.',
  'Rank-three automorphic counting/trace comparison for precisely the BPrime_s points of each original HostFrame.')
 target('DA25-HV-10',D+'ThmS6CoreS.lean','ThmS6_s',
  'Actual universal-deformation finiteness and automorphy for the original host frame and a compatible marked point, including all characteristic-zero points and the stated BPrime_s condition.',
  'Rank-three potential automorphy/lifting, finite universal ring and compatible local conditions; a theorem name without exact frame/point transport is not a matched leaf.')

 supporting=[
  anchor(P+'UnitaryThreeGroups/KatoUse.lean','CohInp'),anchor(P+'UnitaryThreeGroups/KatoUse.lean','PropGK'),anchor(P+'UnitaryThreeGroups/KatoUse.lean','CorGK'),anchor(P+'UnitaryThreeGroups/KatoUse.lean','OneChar'),
  anchor(P+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean','KatoTwo'),anchor(P+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean','RigII'),anchor(P+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean','InpZ'),
  anchor(P+'ModularityArgument/KatoQuadraticCharacters/RigIIOfHypotheses.lean','caseI'),anchor(P+'AutomorphicCases/AutomorphyUnramifiedCoefficients.lean','AutomorphyUnramifiedCoefficients'),
  anchor(D+'AdjointLiftingOfCohomology.lean','countII_and_countIII_of_printsH_of_sp4In'),anchor(D+'AfDesc.lean',"HypothesesH'"),
  anchor(P+'SymplecticGSp4/EntryMem.lean','SoV'),anchor(P+'SymplecticGSp4/EntryMem.lean','SoFin'),anchor(P+'SymplecticGSp4/EntryMem.lean','CohomologyHyp'),
  anchor(P+'LevelCohomology/UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean','LemmaX'),anchor(P+'LevelCohomology/UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean','UnramifiedCocycleIsCoboundaryOfBernoulliUnit'),anchor(P+'LevelCohomology/UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean','CorX'),
  anchor(P+'LevelCohomology/LemmaX.lean','UpperTheory.V.X.lemmaX'),anchor(P+'LevelCohomology/ResidualBernoulliNonvanishing.lean','UpperTheory.V.X.residual_bernoulli_nonvanishing'),
  anchor(D+'AfStmt.lean','NumberSp4Alt'),anchor(D+'RigEnd3.lean','RigiditySymplecticFour'),
  anchor(P+'UnitaryThreeDeformations/HostNumber.lean','HostVanE'),anchor(P+'UnitaryThreeDeformations/HostNumber.lean','HostXpp'),anchor(D+'HostNumberS.lean','HostRigid_s'),
  anchor(P+'HeightAndVanishing/JointWinOfCounts.lean','pointHV_of_counts')]

 # Freeze component inputs and verify all indexed proof/source bytes.
 manifest=[];new_claims={};component_ledgers={}
 for name in COMPONENTS:
  ledger=read(WORK/name/'provenance.json');component_ledgers[name]=ledger
  raw=(WORK/name/'main.tex').read_bytes();expected=ledger.get('main_tex_sha256',ledger.get('validation',{}).get('main_tex_sha256'));assert sha(raw)==expected,name
  claims=ledger['claims'];new_claims[name]=[c['id']for c in claims]
  for c in claims:
   for a in c['sources']:verify(a)
   loc=c.get('proof_location',c.get('human_proof'));assert loc is not None,c['id']
   actual=WORK/loc['file'];b=actual.read_bytes();frag=b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);assert sha(frag)==loc['sha256'],c['id']
  for name2 in ['main.tex','provenance.json','closure.json','classical_inputs.json','tex_validation.json','report.txt','report.md']:
   f=WORK/name/name2
   if f.exists():manifest.append({'path':str(f.relative_to(WORK)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size})
 for f in sorted((WORK/'reviews_v0_25').glob('*')):
  if f.is_file():manifest.append({'path':str(f.relative_to(WORK)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size})
 for f in [OLD/'obligation_map.json',OLD/'audit.txt',WORK/'configure_v0_25.py',WORK/'increment_v0_25.json']:
  if f.exists():manifest.append({'path':str(f.relative_to(WORK)),'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size})

 m=copy.deepcopy(baseline);m.update({'artifact_version':'0.25','baseline':'0.24','previous_map':'previous_obligation_map.json','increment_integration':'LK1–LK4, TB1–TB10, KB1–KB8, TW1–TW8 and CZ1–CZ6 close exact local-K, all-prime arithmetic torsion, actual KBridge/LemmaK31, simultaneous ThmBab, and CountZ(C=0). Only PointHV remains bespoke in the selected cohomological supplier cut; its other actual counts and assembly remain. Global actual-family/gap/type/theta/metric/spectral obligations are unchanged.'})
 byid={n['id']:n for n in m['nodes']}
 def update(nid,**kw):
  n=byid[nid];previous=copy.deepcopy(n);n.setdefault('history',[]).append({'version':'0.24','snapshot':previous});n.update(kw)
 def node(nid,title,gate='LEAF',**kw):
  assert nid not in byid;n={'id':nid,'title':title,'gate':gate,'introduced_in':'0.25',**kw};m['nodes'].append(n);byid[nid]=n
 node('CLASSICAL_LOCAL_K','Precisely matched finite local Tate/finiteness/Euler input',status='named_classical_inputs_with_written_native_specializations',registry='local_k_duality/classical_inputs.json',input_ids=['LK-LF','LK-TATE','LK-EULER'])
 update('LOCAL_K_INTERFACE_MATCH',gate='AND',requires=['CLASSICAL_LOCAL_K'],status='human_supplier_complete_relative_to_matched_classical_leaves',claims=[f'LK{i}'for i in range(1,5)],source_target_ids=[],premise='Literal LocalFinitenessK, LocalTateDualityK and LocalEulerCharK on each original finite K inside PadicAlgCl(ell), all finite possibly nonfree Z/ell^r modules, actual cycK, all four cup maps, ell=2 included.',not_inferred=['Every differently named local/global or normalized automorphic cohomology package'])
 node('ARITHMETIC_TORSION_BOUND','All-prime actual arithmetic-group torsion bound',status='complete_human_geometric_and_homological_supplier',claims=[f'TB{i}'for i in range(1,11)],endpoint='TorsBound49 and TorsBoundPow22 for original HGL L (4e+4) (2e)',premise='Ordered perfect-form nerve exactness, common minimal basis, row-module orbit count, finite stabilizer bound, and integral spectral-sequence torsion estimate are proved. No torsion prime is inverted.')
 node('CLASSICAL_K_THEORY','Matched finite K-theory, stability and Hurewicz inputs',status='named_classical_inputs_with_written_actual_object_specializations',registry='k_theory_bridge/classical_inputs.json',input_ids=[f'KB-C{i}'for i in range(1,10)])
 node('K_THEORY_COMPARISON','Canonical K module and maps to original compact H2 and HGL',gate='AND',requires=['CLASSICAL_K_THEORY','FINITE_DUALITY_SPECIALIZATION'],status='human_actual_interface_supplier_complete_relative_to_classical_leaves',claims=['KB1','KB2','KB3','KB4'],endpoint='Literal KBridge',binding_keys=['original L/Omega/D','actual quotient GS and cyclotomic D.chi','compact cochain H2','canonical finite Quillen K','original HGL tensor','exact cOne(2e)'],not_inferred=['A universal theorem for every arbitrary Plus or KPublished record'])
 update('LEMMA_K_BOUND',gate='AND',requires=['K_THEORY_COMPARISON','ARITHMETIC_TORSION_BOUND','LOCAL_K_INTERFACE_MATCH','FINITE_DUALITY_SPECIALIZATION','CLASSICAL_K_THEORY'],status='human_supplier_complete_relative_to_matched_classical_leaves',claims=[f'KB{i}'for i in range(1,9)],source_target_ids=[],premise='Literal LemmaK31 with C_K fixed before every prime, original totally complex L/Omega/D and e>=1; finite coefficient PT/local transport and class-number bound feed the actual finite-module/tensor estimate.')
 node('CLASSICAL_IWASAWA','Ferrero–Washington and ordinary Iwasawa structure input',status='named_classical_inputs_with_written_finite_layer_translation',registry='simultaneous_cohomological_windows/classical_inputs.json',input_ids=['TW-FW','TW-IW','TW-CF'])
 update('FERRERO_WASHINGTON_MATCH',gate='AND',requires=['CLASSICAL_IWASAWA'],status='human_finite_layer_interface_matching_complete',claims=['TW1'],source_target_ids=[],premise='The exact bounded class-group ell-rank statement is supplied at every layer, including ell=2 with mu4. Finite-layer norm-surjectivity and the transfer from mu=0 are written; no unnamed control statement is retained.')
 node('CLASSICAL_WINDOW_ARITHMETIC','Matched abelian conductor-discriminant input',status='named_classical_input_with_uniform_field_model_transfer_written',registry='simultaneous_cohomological_windows/classical_inputs.json',input_ids=['TW-CD'])
 update('TWO_PRIMARY_BOUND',gate='AND',requires=['LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','FINITE_DUALITY_SPECIALIZATION','FERRERO_WASHINGTON_MATCH','CLASSICAL_WINDOW_ARITHMETIC'],status='human_supplier_complete_relative_to_matched_classical_leaves',claims=[f'TW{i}'for i in range(1,9)],supplied_inputs={'LemmaK':'KB8','LocalFinitenessK':'LK2','LocalTateDualityK':'LK3','PoitouTateDuality':'LD3','FerreroWashington':'TW1'},premise='One actual BConst K is fixed before every Ct>=1. One fixed pair and full real window serve the original E two-primary sum and every separately quantified reference layer model; all local-data choices, twists and finiteness clauses are retained.')
 node('CLASSICAL_COUNT_Z','Matched finite ray/Hilbert class field input for exceptional vanishing',status='named_classical_inputs_with_written_actual_cocycle_specializations',registry='count_z_closure/classical_inputs.json',input_ids=['CZ-CFT','CZ-BASIC'])
 node('COUNT_Z_SUPPLIER','Actual PropZ and CountZ with exponent zero',gate='AND',requires=['CLASSICAL_COUNT_Z'],status='human_supplier_complete_relative_to_matched_classical_leaves',claims=[f'CZ{i}'for i in range(1,7)],premise='Original Omega/O and negative cyclotomic action; both residual-trivial and quadratic cases, local normalization, finite class-field transfer and h_K<ell proved; C=0 precedes all host/window objects.')
 node('COUNT_I_SUPPLIER','Actual CountI prime-and-character sum',status='major_automorphy_rigidity_and_counting_supplier_retained',source_target_ids=['DA24-HV-01','DA24-HV-06','DA25-HV-01','DA25-HV-02'],premise='Actual OneChar -> PropGK -> CorGK -> CountI. Retain compatible cohomology, Kato/adjoint rigidity, unramified-coefficient automorphy and rank-three trace-counting.')
 node('SYMPLECTIC_COUNT_CHAIN','Actual joint CountII and CountIII supplier',status='major_rank_four_automorphy_and_counting_supplier_retained',source_target_ids=['DA24-HV-02','DA24-HV-03','DA25-HV-03','DA25-HV-04','DA25-HV-05','DA25-HV-06','DA25-HV-07'],premise='The common sp4Main_alt route still needs actual rank-four automorphy/finite points, CohomologyHyp, finite algebra models, trace counting, rigidity, CorX and fully transported SoV/SoFin. The coefficient-extension return to the original O is part of the chain.')
 node('COUNT_V_SUPPLIER','Actual rank-three CountV host-frame supplier',status='major_host_automorphy_rigidity_and_counting_supplier_retained',source_target_ids=['DA24-HV-04','DA25-HV-08','DA25-HV-09','DA25-HV-10'],premise='Retain ThmS6_s and HostVanE/Xpp/Rigid_s/Number_s on the same actual host frame, universal ring and marked point. Native non-K local/global and normalized PT packages still need their own exact matching.')
 update('ACTUAL_POINT_COUNTS',gate='AND',requires=['COUNT_I_SUPPLIER','SYMPLECTIC_COUNT_CHAIN','COUNT_V_SUPPLIER','COUNT_Z_SUPPLIER'],status='CountZ_supplied_four_other_count_predicates_retained',source_target_ids=['DA24-HV-01','DA24-HV-02','DA24-HV-03','DA24-HV-04','DA24-HV-06'],supplied_inputs={'CountZ':'CZ6'},premise='Original CountI/II/III/V/Z have unchanged meanings. CountZ is complete; the other four are substantive actual arithmetic suppliers, with the paired II/III source route exposed.')
 node('POINT_HV_ASSEMBLY','Actual counts-to-PointHV sum and layer assembly',status='human_reconstruction_retained_source_implication_identified',source_target_ids=['DA-next-01-b'],premise='Write CountVs/CountIV usage and sumIn/sumOut/point: common constants and auxiliary primes precede hosts; retain every fixed reference-layer function j, original field/local data, all twists and uniform eventual inequalities. Calling the source wrapper is not a written proof.')
 update('ODD_PLUS_BOUND',gate='AND',requires=['LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','FINITE_DUALITY_SPECIALIZATION','ACTUAL_POINT_COUNTS','POINT_HV_ASSEMBLY'],status='sole_remaining_bespoke_cohomological_supplier_on_selected_route',supplied_inputs={'PoitouTateDuality':'LD3','LocalFinitenessK':'LK2','LocalTateDualityK':'LK3','LemmaK':'KB8','CountZ':'CZ6'},premise='Literal PointHV still requires actual CountI/II/III/V and their complete original-host/reference-layer assembly. The common K-theory/local-K and exceptional count premises are supplied without replacing PointHV by an implication.')
 update('COHOMOLOGICAL_WINDOW',status='human_assembly_complete_only_PointHV_supplier_remains',completed_input_suppliers={'ODD_MINUS_BOUND':'OB8 via OS1/OS9, constant240','TWO_PRIMARY_BOUND':'TW8 via KB8/LK/LD, one K for all Ct>=1'},remaining_bespoke_suppliers=['ODD_PLUS_BOUND'],premise='VW1–VW4 preserve original E, conductor, local data and q,d through the whole real window. ThmBab and ThmBcFree are now complete relative to named matched classical leaves. PointHV is the remaining bespoke supplier; its sums need not be evaluated on the same field model as the separately quantified reference layers.')
 update('JOINT_WINDOW',status='conditional_join_with_ThmBab_supplied_PointHV_retained',note='The direct JointWin alternative remains optional and unreconstructed. On the ThmBab plus PointHV route, ThmBab is now supplied by TW8; PointHV remains.')
 update('FIXED_PAIR_WINDOWS',status='human_chain_complete_conditional_on_PointHV_and_named_classical_inputs',supplied_cohomological_parts=['TW8','OB8'],remaining_cohomological_supplier='PointHV',premise='QP22 keeps one pair q,d for all x in each full interval, retaining exact conductor/model comparisons and the 401-to-400 margin. PairEx still carries its own classical CN/BD/HD and compatible-host requirements.')

 # Validate the semantic AND/OR graph, independently of proof-count metrics.
 assert set(n['id']for n in baseline['nodes']).issubset(byid)
 def edges(n):return n.get('requires',[])+[x for a in n.get('alternatives',[])for x in a]
 seen=set();active=set()
 def visit(i):
  assert i in byid,i
  if i in seen:return
  assert i not in active,('cycle',i);active.add(i)
  for j in edges(byid[i]):visit(j)
  active.remove(i);seen.add(i)
 for i in byid:visit(i)
 tids={t['id']for t in targets}
 assert len(tids)==len(targets)
 for n in m['nodes']:
  for j in n.get('related_nodes',[]):assert j in byid,j
  for t in n.get('source_target_ids',[]):assert t in tids,(n['id'],t)
 m['validation']={**m.get('validation',{}),'node_count':len(m['nodes']),'node_ids_unique':len(byid)==len(m['nodes']),'acyclic':True,'all_edges_resolve':True,'all_related_nodes_resolve':True,'all_current_target_ids_resolve':True,'historical_node_meanings_preserved':True,'historical_node_count':len(baseline['nodes']),'historical_validation_preserved_in_previous_map':True}
 anchors=sorted(source_index.values(),key=lambda a:(a['path'],a['line_start'],a['line_end']))
 source_obj={'commit':PIN,'sources':anchors,'source_files':len(blobs),'source_ranges':len(anchors)}
 source_bytes=(json.dumps(source_obj,ensure_ascii=False,indent=2)+'\n').encode();m['source_manifest_sha256']=sha(source_bytes)
 (HERE/'previous_obligation_map.json').write_bytes((OLD/'obligation_map.json').read_bytes())
 write('obligation_map.json',m);write('source_anchors.json',source_obj)
 write('next_targets.json',{'targets':targets});write('retirement_candidates.json',{'targets':retired});write('target_scope_updates.json',updates)
 write('count_frontier_sources.json',{'sources':supporting,'entry_target_ids':[t['id']for t in targets if t['id'].startswith('DA25-HV-')]})
 write('input_manifest.json',{'artifact_version':'0.25','components':COMPONENTS,'files':manifest})
 write('summary.json',{'artifact_version':'0.25','new_claim_ids':[],'increment_supplier_claims':new_claims,'retirement_candidate_ids':list(retirement),'retirement_count':len(retired),'historical_nodes_preserved':len(baseline['nodes']),'map_node_count':len(m['nodes']),'remaining_cohomological_supplier':'PointHV','supplied_counts':{'CountZ':'CZ6'},'remaining_counts':['CountI','CountII','CountIII','CountV'],'remaining_count_assembly':True,'not_globally_closed':['RH','Dirichlet GRH','PointHV','actual-family LinkN','actual common family / DesignExists','HostExW and actual HostGood/RankVal/EAtH','theta/type/rank/metric/spectral joins','arithmetic gap / final gain','every differently named non-K local/global or normalized automorphic cohomology interface']})
 write('verification.json',{'artifact_version':'0.25','source_commit':PIN,'source_files_checked':len(blobs),'source_ranges_indexed':len(anchors),'all_cited_source_files_equal_pinned_git_blobs':True,'all_source_range_hashes_verified':True,'all_component_main_and_proof_hashes_match':True,'historical_node_ids_preserved':True,'historical_snapshot_byte_identical':True,'sufficient_condition_graph_acyclic':True,'current_validation_node_count':len(m['nodes']),'historical_validation_not_edited':True,'all_related_and_target_ids_resolve':True,'prior_files_modified':False,'root_targets_modified':False,'new_claim_ids':[],'Lean_kernel_replay_run':False,'formal_transitive_Lean_dependency_audit':False,'audit_txt_sha256':sha((HERE/'audit.txt').read_bytes())if(HERE/'audit.txt').exists()else None,'scope':'Human semantic sufficient-condition audit. Integrity and graph checks validate provenance/bookkeeping, not the mathematical proofs.'})
 print(json.dumps({'retirements':len(retired),'targets':len(targets),'source_files':len(blobs),'source_ranges':len(anchors),'historical_nodes':len(baseline['nodes']),'map_nodes':len(m['nodes'])},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=WORK.parent/'lean-source');main(p.parse_args().repo.resolve())
