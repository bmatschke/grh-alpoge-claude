#!/usr/bin/env python3
"""Build the exact pinned source ledger and closure boundary for AX1--AX10."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
C = 'symplectic_arithmetic_data'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
BASE = REPO + '/blob/' + PIN + '/'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
S = P + 'SymplecticGSp4/'
H = P + 'HeightAndVanishing/'
X = P + 'LevelCohomology/'
D = P + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
A = P + 'ModularityArgument/AutomorphyLifting/AdmissibleLevelRestriction/'
PATHS = {
 'defs':H+'DirichletPrimeToLPartMulLPowerPart.lean',
 'raw':S+'DecompSigmaOrd.lean', 'matrix':S+'MapRepApply.lean',
 'cases':P+'AutomorphicCases/SymplecticGSp4.lean',
 'data':S+'DataEx.lean', 'rawex':S+'ReFrob.lean', 'prime':S+'PrimeTo.lean',
 'host':H+'HostComp.lean', 'th1':H+'OrdProjNDvd.lean',
 'odd':H+'HostOdd.lean', 'sb':H+'HostSb.lean', 'bchi':H+'BchiFacts.lean',
 'arith':X+'Th1Facts.lean', 'psibar':H+'PsiBar.lean',
 'compine':H+'CompIne.lean', 'teich':H+'ExistsStrictHenselianAbsolutelyClosedLocalRing.lean',
 'teichdef':H+'EtaKer.lean', 'primprod':X+'HcPrimProd.lean',
 'omdir':X+'HcOmDir.lean', 'dirval':X+'HcDirVal.lean',
 'xvan':X+'HcXvan.lean','van':X+'HcVanOf.lean','spker':X+'HcSpKer.lean',
 'hcdefs':X+'HcDefs.lean',
 'corx':X+'UnramifiedCocycleIsCoboundaryOfBernoulliUnit.lean',
 'dyadic':S+'ExistsPrimitiveOddDirichletCharacterTwoPow.lean',
 'twist':S+'ExistsPrimitiveTwoPowTwistMul.lean',
 'quant':S+'TwoPowLtSqMulOfPrimitiveCharPowEqOne.lean',
 'auxchar':S+'ExistsDirichletCharacterPrimeOfOrderOfDvd.lean',
 'primeconstants':P+'CMFieldExponentialBounds/primesex.lean',
 'cyc': 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CyclotomicCharInertiaSurjective.lean',
 'facts':S+'LMemMax.lean', 'eii':S+'EiiUnit.lean',
 'lev':S+'DirGPowOne.lean', 'levbasis':S+'LevBasis.lean',
 'ord':S+'OrdFlag.lean',
 'spl':P+'PadicHodgeTheory/SplAdjUnit.lean',
 'ptdefs':P+'PadicHodgeTheory/IsFirstOrderDeformationOfRZero.lean',
 'pt':S+'PtInSmul.lean', 'ept':S+'EptInt.lean',
 'leveldefs':P+'AutomorphicForms/BlochKatoSelmerVanishes.lean',
 'dualdefs':P+'AutomorphicForms/CongruenceNumberRankThree.lean',
 'unl':P+'TheoremsMuLinked/GaloisRepresentationTypes/UnlPlace.lean',
 'teichdvd':P+'ModularityArgument/SemisimpleLevels/TeichNotLt.lean',
 'safe':A+'UnlAllOf.lean','unlone':A+'UnlOfOne.lean',
 'image':D+'IsAut4.lean','adm':D+'AfStmt.lean',
 'count':D+'CountS.lean','consumer':D+'ConductorAtMapInjectiveCoeff.lean',
 'imageprod':D+'Sp4In.lean','imagealt':D+'Sp4In0.lean',
}

def sha(b): return hashlib.sha256(b).hexdigest()
def write(name,obj):
 (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main(repo):
 cache={}
 for key,path in PATHS.items():
  b=(repo/path).read_bytes()
  assert b==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
  cache[key]=b

 def anchor(key,decl,start=None,end=None,role='Exact source statement or reconstructed proof, in the stated AX scope'):
  b=cache[key]; lines=b.decode().splitlines()
  if start is None:
   pat=re.compile(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure)\s+'+re.escape(decl)+r'(?=[\s:(])')
   hits=[i+1 for i,t in enumerate(lines)if pat.match(t)]
   assert len(hits)==1,(key,decl,hits)
   start=hits[0]
  if end is None:
   end=len(lines)
   for i in range(start,len(lines)):
    if re.match(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[',lines[i]):
     end=i;break
   while end>start and not lines[end-1].strip():end-=1
  frag=b''.join(b.splitlines(keepends=True)[start-1:end])
  return {'path':PATHS[key],'declaration':decl,'line_start':start,'line_end':end,
    'sha256':sha(b),'range_sha256':sha(frag),'range_bytes':len(frag),
    'first_line':lines[start-1],'url':BASE+PATHS[key]+f'#L{start}-L{end}',
    'role':role,'verified_equal_to_pinned_git_blob':True}

 def many(key,decls,role=None):
  return [anchor(key,d,**({'role':role}if role else{})) for d in decls]

 specs=[
  ('AX1','Exact host decomposition, local order restrictions, and the two original cases',[],['AX-CYC','AX-LOCAL'],
   many('defs',['Host','N','H','IsChar','Big','X','CaseII','CaseIII','nII','nIII'])+
   many('host',['UpperTheory.V.HV.hostComp'])+many('th1',['UpperTheory.V.HV.hostTh1'])+
   many('odd',['UpperTheory.V.HV.hostOdd'])+many('sb',['UpperTheory.V.HV.hostSb'])+
   many('bchi',['UpperTheory.V.HV.bchiFacts'])+many('arith',['UpperTheory.V.X.th1Facts'])+
   many('primeconstants',['UpperTheory.V.pK_pOne_prime_conditions'],
     'Only the required fixed pOne prime/congruence/coprimality assertion is reconstructed; no new proof of the unrelated pK/class-number clauses is claimed')),
  ('AX2','Primitive dyadic characters, quantitative conductor separation, and exact XData assembly',[],[],
   many('dyadic',['UpperTheory.exists_primitive_odd_dirichletCharacter_two_pow'])+
   many('twist',['UpperTheory.exists_primitive_two_pow_twist_mul'])+
   many('quant',['UpperTheory.two_pow_lt_sq_mul_of_primitive_char_pow_eq_one'])+
   many('primprod',['UpperTheory.V.X.primProd'])+many('data',['dirX'])+
   many('dirval',['UpperTheory.V.X.dirVal'])+many('corx',['XData','prodX'])),
  ('AX3','Original-field Frobenius/raw choices and full primeTo lift consequence',[],['AX-CYC','AX-LOCAL'],
   many('rawex',['re_two','re_unit','re_cc','re_frob','UpperTheory.V.GradeZeroInterpolatingElement.rawEx'])+
   many('prime',['pt_modEq_one','pt_const','pt_exists','pt_step','pt_pow','UpperTheory.V.GradeZeroInterpolatingElement.primeTo'])+
   many('cyc',['cycZ_Ine_surjective'])+many('teich',['UpperTheory.V.HV.omT'],
     'Needed original-Coef Teichmuller existence, uniqueness, finite level and inertia consequences; not an assertion about unrelated strict-Henselian constructions')+
   many('teichdef',['IsOmT'])+many('raw',['Raw'])),
  ('AX4','Exact residual XVan transfer and complete generic Good construction',['AX1','AX2','AX3','BR7'],[],
   many('data',['psi_ne','t_sub','xvOf','core'])+
   many('van',['UpperTheory.V.X.vanOf'])+many('spker',['UpperTheory.V.X.spKer'])+
   many('xvan',['UpperTheory.V.X.xvan'])+many('hcdefs',['Van'])+
   many('raw',['XVan','Good'])+many('omdir',['UpperTheory.V.X.omDir'])+
   many('psibar',['UpperTheory.V.HV.psiBar'],
     'Needed residual prime-to-l decomposition, parity and original-character injectivity; proved by explicit finite CRT and cyclotomic arguments')+
   many('compine',['UpperTheory.V.HV.compIne'],
     'Needed inertia equality with the original p-supported Dirichlet component')),
  ('AX5','Literal dataEx with both exact parameter choices',['AX1','AX2','AX4'],[],
   many('data',['UpperTheory.V.GradeZeroInterpolatingElement.dataEx'])+
   many('auxchar',['UpperTheory.exists_dirichletCharacter_prime_of_orderOf_dvd'])+
   many('cases',['OfChar','OfCase'])+many('defs',['nII','nIII'])),
  ('AX6','Full literal facts for arbitrary Good and the normalization unit',['AX3'],['AX-LOCAL'],
   many('facts',['dvd_pred','sb_facts','unrT','ps_wt','ps_ok','rbar_open','rbar_ph','UpperTheory.V.GradeZeroInterpolatingElement.facts'])+
   many('matrix',['lamW','muW','IsBlock'])+many('raw',['hEl','Nrm','Good'])+
   many('eii',['eii_unit'],
     'Only the elementary nonzero-residue/unit criterion is used; eii matrix-span construction is not claimed by AX6')),
  ('AX7','Literal levOf common level and finite exponent',['AX1','AX5'],[],
   many('lev',['UpperTheory.V.GradeZeroInterpolatingElement.levOf'])+
   many('leveldefs',['KillsMu'])+many('cases',['OfChar'])),
  ('AX8','Full ordinary component specialization with residual eigencharacter control',['AX6'],['AX-NORM','AX-HENS'],
   many('raw',['OnComp','condL'])+many('matrix',['prj','Ord'])+
   many('ptdefs',['FlagIn','PtOn'])+
   many('ord',['UpperTheory.V.GradeZeroInterpolatingElement.ordFlag'])+
   many('spl',['spl_int','spl_local','spl_norm_lt','spl_near','spl_red','spl_cont','spl_bar','UpperTheory.V.Loc.spPtL'])),
  ('AX9','Literal Level, dual multiplier, UnlAll and safe4-prime',['AX3','AX6','AX8'],[],
   many('levbasis',['lev_basis','lev_diag','lev_place','lev_dual','UpperTheory.V.GradeZeroInterpolatingElement.level'])+
   many('pt',['UpperTheory.V.GradeZeroInterpolatingElement.ptIn'],
     'Only multiplier, unramified and local polynomial-equation transport are supplied here; the stronger eii span assertion is not part of AX9')+
   many('ept',['UpperTheory.V.GradeZeroInterpolatingElement.eptInt'],
     'Only continuity and the entrywise strict residual estimate are reconstructed; the stronger common finite-coefficient and eii-span endpoint is not claimed')+
   many('leveldefs',['LevelAway','LevelAt','Level'])+
   many('dualdefs',['DualTw','IsCycWt'])+
   many('unl',['UpperTheory.V.Th.spUnl'])+many('teichdvd',['UpperTheory.V.Lev.teichDvd'])+
   many('unlone',['UpperTheory.V.Z.Win.A4.unlOfOne'])+
   many('safe',['SafeRA','unlAll_of',"safe4'"])),
  ('AX10','Complete actual G1 under exactly SymplecticFourImageDense',['AX1','AX5','AX7','AX9','RV1','SP8'],[],
   many('image',['IsAut4Alt','SymplecticFourImageDense'],
     'SymplecticFourImageDense is retained exactly; only its actual-D conclusion is applied')+
   many('adm',['AdmRAlt'])+
   many('count',['UpperTheory.V.Z.Win.A4.exists_frob_nonvanishing_with_sha_bound'],
     'Consumer admissible-class join only; AX does not prove NumberSp4Alt or the quantitative trace theorem')+
   many('consumer',['main_big','UpperTheory.V.Th.sp4Main_alt'],
     'Exact G1 and injective coefficient-return usage matched; the remaining G2, rigidity and catalogue suppliers are not claimed')),
 ]
 b=(HERE/'main.tex').read_bytes();ls=b.splitlines(keepends=True)
 claims=[]
 for cid,title,deps,classic,src in specs:
  starts=[i for i,t in enumerate(ls)if f'\\begin{{proposition}}[{cid}:'.encode() in t]
  assert len(starts)==1,(cid,starts)
  st=starts[0]; en=next(i for i in range(st+1,len(ls))if ls[i].strip()==b'\\end{proof}')
  frag=b''.join(ls[st:en+1])
  loc={'file':C+'/main.tex','line_start':st+1,'line_end':en+1,'sha256':sha(frag),'bytes':len(frag)}
  remaining=['UpperTheory.V.Aut.SymplecticFourImageDense']if cid=='AX10'else[]
  claims.append({'id':cid,'title':title,
   'status':'Complete human proof of the stated implication; only the named classical inputs, prior proved suppliers and explicitly retained original predicate are used.',
   'depends_on':deps,'mathematical_dependencies':deps,'classical_inputs':classic,
   'remaining_inputs':remaining,'remaining_bespoke_inputs':remaining,
   'component_ledger':C+'/provenance.json','proof_location':loc,'human_proof':loc,'sources':src})

 frontier=[anchor('image','SymplecticFourImageDense',role='Exact retained G1 supplier'),
           anchor('imageprod','sp4In_alt',role='Actual image-density producer; its hypotheses remain to be supplied'),
           anchor('imagealt','sp4In0_alt',role='Alternative actual image-density producer; actual HypothesesH-prime remains to be supplied')]
 files=[]
 for key,path in sorted(PATHS.items(),key=lambda z:z[1]):
  q=cache[key]
  files.append({'path':path,'sha256':sha(q),'bytes':len(q),'lines':len(q.splitlines()),'url':BASE+path,'verified_equal_to_pinned_git_blob':True})
 allsrc=[a for c in claims for a in c['sources']]+frontier
 graph={c['id']:c['depends_on']for c in claims}
 classical={
  'schema':'rh-classical-input-registry/1','artifact_version':'0.27','component':C,'accessed':'2026-11-22',
  'inputs':[
   {'id':'AX-CYC','name':'Finite cyclotomic Galois theory and original-closure extension',
    'author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,
    'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','theorem_reference':'Section 6, basic cyclotomic results (especially Proposition 6.2); finite Galois extension of embeddings',
    'web_source_refs':['turn807102395view1'],
    'accepted_statement':'The finite cyclotomic action identifies Gal(Q(mu_M)/Q) with (Z/M)^× and finite automorphisms extend to the specified algebraic closure.',
    'exact_specialization':'AX1 and AX3--AX4 evaluate every component using one cyclotomic residue in the original Omega. Total ramification of l-power roots is derived by the Eisenstein polynomial Phi_(l^r)(1+X); unramifiedness and the arithmetic Frobenius power are derived by Hensel lifting.'},
   {'id':'AX-LOCAL','name':'Finite local-field ramification and decomposition groups',
    'author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,
    'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','theorem_reference':'Theorem 7.50 and Corollaries 7.51--7.52; Proposition 7.55; Theorem 7.58 and Corollary 7.59; Proposition 8.10 and the decomposition/inertia discussion of Section 8',
    'web_source_refs':['turn398182820view1','turn937255849view1','turn937255849view2'],
    'accepted_statement':'Finite residue extensions lift uniquely to finite unramified local extensions; wild inertia is pro-p and the prime-to-p tame quotient has its root-of-uniformizer description; chosen global decomposition/inertia groups identify with their local-completion counterparts.',
    'exact_specialization':'AX3 uses compact nested fibers to obtain the full inertia cyclotomic map and changes Frobenius only by inertia. AX6 derives the p−1 bound for the finite abelian inertia image from Frob*tau*Frob^-1=tau^p, avoiding a blanket Kronecker--Weber or local-CFT predicate. All original places and conjugations are preserved.'},
   {'id':'AX-NORM','name':'Unique valuation on finite extensions of a complete discretely valued field',
    'author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,
    'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','theorem_reference':'Theorem 7.38 (same finite-local-field fact used by RV1)',
    'web_source_refs':['turn937255849view0'],
    'accepted_statement':'A finite extension of a complete discretely valued characteristic-zero field is complete and has the unique extended absolute value.',
    'exact_specialization':'AX8 derives boundedness and strict maximal-ideal bounds for every actual algebra map to Qbar_l from the norms of all conjugates and the unit criterion. It then proves a uniform m^n bound and actual entry continuity. No common finite-field assertion for arbitrary compact subsets is used.'},
   {'id':'AX-HENS','name':'Finite algebras over Henselian local rings and completeness',
    'author':'The Stacks Project','url':'https://stacks.math.columbia.edu/tag/04GH',
    'additional_urls':['https://stacks.math.columbia.edu/tag/04GM'],
    'theorem_reference':'Tags 04GH (Lemma 10.153.4(1),(2)) and 04GM (Lemma 10.153.9)',
    'web_source_refs':['turn807102395view0','turn398182820view0'],
    'accepted_statement':'Complete local rings are Henselian. A finite algebra over a Henselian local ring is a finite product of local rings, each finite and local over the base.',
    'exact_specialization':'For the actual domain B and an integral v=t/d, B[v] is a finite domain and hence one local factor. The original diagonal point maps v to zero, forcing v into that maximal ideal; every other original algebraic specialization then has norm<1. The divided eigenvalue and every transfer are proved explicitly.'},
  ],
  'previously_reconstructed_inputs':[
   {'claim_id':'BR7','component':'bernoulli_residual_vanishing','used_scope':'Literal CorX with both original and inverse residual characters, arbitrary residue field and prime-to-l relative-index UnrEv. AX4 proves the actual local T/K transfer.'},
   {'claim_id':'RV1','component':'rank_one_cohomology','used_scope':'Exact coefficient extension and normalized length cancellation under the finite DVR enlargement allowed in SP8.'},
   {'claim_id':'SP8','component':'symplectic_count_closure','used_scope':'Injective coefficient invariants and normalized return to the original coefficient; no model or automorphy predicate is inferred.'},
  ],
  'foundational_background':[
   'Finite abelian groups and their characters, cyclicity of a finite subgroup of a field multiplicative group, CRT and finite-field Frobenius',
   'The fixed positive pK and class number hStar of the earlier host setup retain their established meanings; positivity of a number-field class number follows from the classical finite ideal class group',
   'Basic DVR ideal and norm dictionary, finite-dimensional matrix spectral projectors and elementary linear algebra',
   'Profinite compactness, finite-index open subgroups and separated complete local rings',
  ],
  'not_assumed':['dataEx, rawEx, facts, levOf, spPtL, level, safe4-prime',
   'An additional Bernoulli unit or nonvanishing statement beyond reconstructed BR7',
   'CohomologyHyp, period-ring comparison or BlochKatoLocal',
   'SymplecticFourImageDense before the explicit AX10 implication',
   'Actual model, Fin0, NoEnd, actual rigidity or automorphic trace catalogue without their stated suppliers'],
 }
 write('classical_inputs.json',classical)
 source_data={'commit':PIN,'files':files}
 write('source_hashes.json',source_data)
 provenance={
  'schema':'rh-human-provenance-component/1','artifact_version':'0.27','date':'2026-11-22',
  'repository':REPO,'commit':PIN,'component':C,'main_tex_sha256':sha(b),
  'scope':'Complete actual arithmetic G1 construction and local/level comparisons, ending in the exact conditional common admissible class under SymplecticFourImageDense.',
  'claims':claims,'source_files':files,'mathematical_dependency_graph':graph,
  'classical_input_registry':C+'/classical_inputs.json','retained_frontier':frontier,
  'component_input_boundary':{
   'previously_proved_claims':['BR7','RV1','SP8'],
   'retained_bespoke_inputs':{'AX10':['UpperTheory.V.Aut.SymplecticFourImageDense']},
   'same_object_requirement':'AX5 produces actual Good/OfCase on the given Omega/O after only the SP8-allowed root enlargement. AX6--AX9 are universal on the same actual Good D. AX10 applies ImageDense to that identical D and chooses one iota before all varying points.'},
  'validation':{'all_source_files_match_pinned_git_blobs':True,'source_links':sum(len(c['sources'])for c in claims),'frontier_links':len(frontier),'source_files':len(files),'proof_ranges':len(claims),'claim_ids_unique':len(graph)==10,'lean_kernel_replayed':False,'pdf_generated':False},
 }
 write('provenance.json',provenance)
 endpoints=[
  ('rawEx','AX3',anchor('rawex','UpperTheory.V.GradeZeroInterpolatingElement.rawEx'),'Actual original-closure choices, with the same two-character g0 and finite-order-free s0.'),
  ('primeTo','AX3',anchor('prime','UpperTheory.V.GradeZeroInterpolatingElement.primeTo'),'Full profinite limit and residual/lift conclusion for every finite matrix size and actual adically continuous complete-local lift.'),
  ('dataEx','AX5',anchor('data','UpperTheory.V.GradeZeroInterpolatingElement.dataEx'),'Literal quantified endpoint in both source cases, with BR7 installed, exact nII/nIII and source OfCase.'),
  ('facts','AX6',anchor('facts','UpperTheory.V.GradeZeroInterpolatingElement.facts'),'Every source conjunct for arbitrary actual Good D, plus the hEl diagonal-difference unit.'),
  ('levOf','AX7',anchor('lev','UpperTheory.V.GradeZeroInterpolatingElement.levOf'),'All three exact KillsMu assertions and all three power assertions at L and k0.'),
  ('spPtL','AX8',anchor('spl','UpperTheory.V.Loc.spPtL'),'Full actual OnComp/PtOn domain/base-point specialization, original eigencharacter order, strict residual bound, pairing, continuity and every open subgroup containing sg_l.'),
  ('level','AX9',anchor('levbasis','UpperTheory.V.GradeZeroInterpolatingElement.level'),'Full Level plus original multiplier/IsCycWt/DualTw with exact theta equality.'),
  ('spUnl','AX9',anchor('unl','UpperTheory.V.Th.spUnl'),'Actual noncritical ordinary characters on the selected decomposition group.'),
  ('teichDvd','AX9',anchor('teichdvd','UpperTheory.V.Lev.teichDvd'),'All M>=1 with KillsMu M om have l|M.'),
  ('safe4-prime','AX9',anchor('safe',"safe4'"),'Full actual SafeRA via l|M and all-place UnlAll.'),
 ]
 closure={
  'artifact_version':'0.27','component':C,'commit':PIN,'main_tex_sha256':sha(b),
  'claims':[c['id']for c in claims],
  'closed_bespoke_interfaces':[{'interface':i,'supplied_by':q,'source':a,'scope':s}for i,q,a,s in endpoints],
  'conditional_endpoint':{'interface':'G1 in SP10','supplied_by':'AX10','retained_inputs':['UpperTheory.V.Aut.SymplecticFourImageDense'],
    'supplied_scope':'Actual Raw/Good/OfCase, prescribed level/order, every same-D point level/dual/safe, exact SP8 return, and one common admissible embedding after applying the retained literal supplier.'},
  'remaining_bespoke_inputs':['UpperTheory.V.Aut.SymplecticFourImageDense'],
  'previously_proved_inputs':['BR7','RV1','SP8'],'classical_inputs':['AX-CYC','AX-LOCAL','AX-NORM','AX-HENS'],
  'safe_to_retire_in_stated_scope':[],
  'partial_target_updates':{'DA26-SP-01':{
   'human_status':'Actual arithmetic construction and all level/safe comparisons proved; only the literal ImageDense supplier remains in G1.',
   'newly_supplied_inputs':{'dataEx':'AX5','facts':'AX6','levOf':'AX7','spPtL':'AX8','level':'AX9','safe4-prime':'AX9','conditional_G1':'AX10'},
   'remaining_human_scope':'Supply SymplecticFourImageDense on every same actual constructed Good/OfCase D, including Fin0, NoEnd and one common IsAutQA embedding. The dataEx/levOf/level/safe construction is closed.',
   'retained_inputs':['UpperTheory.V.Aut.SymplecticFourImageDense']}},
  'exact_binding_notes':[
   'Source nII and nIII are unchanged; no larger conductor is silently substituted.',
   'The actual T is proved contained in host Tb before condD, xi unramifiedness and BR7 are applied.',
   'All six XVan implications use the original residue field, the actual kernel of rbar and its prime-to-l relative index.',
   'ph is the actual factorial-power limit; rawEx and the stronger primeTo lift statement are proved.',
   'facts holds for any Good datum, not only the Dirichlet-character construction.',
   'The OnComp domain and its diagonal O-point remain in the divided-eigenvalue argument.',
   'LevelAway uses global characters extended from the finite inertia image, not merely local eigencharacters.',
   'Source Irr (full matrix span) implies the Af.IsIrr field by elementary invariant-subspace reasoning.',
   'A single iota precedes all irreducible points; it is supplied exactly by the retained source ImageDense predicate.',
   'An enlarged-coefficient D is not misidentified with a datum over the smaller O; RV1/SP8 supplies the original normalized-length return.'
  ],
  'does_not_close':['SymplecticFourImageDense itself','Actual model construction or its geometry unless supplied by other v0.27 components',
   'Actual same-D irreducible rigidity or RigiditySymplecticFour producers','NumberSp4Alt or the exact uniform catalogue',
   'Unconditional CountII/CountIII, CountI, CountV or PointHV',
   'Global family, gap, theta/type/rank, metric or spectral suppliers','An unconditional human-readable RH/Dirichlet GRH proof'],
 }
 write('closure.json',closure)
 write('remaining_inputs.json',{'schema':'rh-retained-supplier-registry/1','component':C,
  'inputs':[{'id':'AX-R1','name':'UpperTheory.V.Aut.SymplecticFourImageDense','kind':'Retained actual arithmetic/automorphic supplier',
   'used_by':['AX10'],'statement_used':'For every original host/t/c/e/psi and every same actual Good/OfCase D: Fin0 and NoEnd and one common embedding iota for IsAutQA on every source-Irr EPt.',
   'not_inferred_from':['Good','CorX','the local ordinary equations','Level or SafeRA','a separately chosen embedding for each point']}],
  'source_frontier':frontier})
 target={'id':'AX-next-01','priority':1,'component':'symplectic_arithmetic_data',
  **frontier[0],'target':'Supply literal SymplecticFourImageDense on the actual D constructed by AX5',
  'remaining_human_scope':closure['partial_target_updates']['DA26-SP-01']['remaining_human_scope'],
  'retained_inputs':['The actual arithmetic hypotheses of either sp4In_alt or sp4In0_alt, unless separately reconstructed'],
  'already_supplied_by':['AX3','AX5','AX6','AX7','AX8','AX9','AX10'],
  'continuation_sources':frontier[1:]}
 write('next_targets.json',{'targets':[target]})
 write('source_validation.json',{'commit':PIN,'source_links':len(allsrc),'unique_source_ranges':len({(x['path'],x['line_start'],x['line_end'])for x in allsrc}),
  'source_files':len(files),'all_pinned_git_blobs_equal':True,'all_source_ranges_hashed':True,
  'proof_ranges':10,'main_tex_sha256':sha(b),'scope':'Source/proof byte binding and finite dependency metadata; no Lean kernel replay.'})
 names=['main.tex','provenance.json','source_hashes.json','classical_inputs.json','closure.json','remaining_inputs.json','next_targets.json','source_validation.json','build_provenance.py','validate_tex.py','report.txt','tex_validation.json']
 manifest=[]
 for n in names:
  p=HERE/n
  if p.is_file():manifest.append({'path':C+'/'+n,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
 for old in ['bernoulli_residual_vanishing','rank_one_cohomology','symplectic_count_closure']:
  for n in ['main.tex','provenance.json','closure.json']:
   p=HERE.parent/old/n
   manifest.append({'path':old+'/'+n,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'role':'Previously reconstructed supplier; unchanged'})
 write('input_manifest.json',{'artifact_version':'0.27','component':C,'commit':PIN,'files':manifest,
  'no_circular_review_hashes':True,'scope':'Frozen component bytes and exact prior supplier files; downstream reviews and audit outputs are excluded.'})
 print(json.dumps({'component':C,'claims':len(claims),'source_links':sum(len(c['sources'])for c in claims),'frontier_links':len(frontier),'files':len(files),'main_tex_sha256':sha(b)},indent=2))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=HERE.parent.parent/'lean-source')
 main(ap.parse_args().repo)
