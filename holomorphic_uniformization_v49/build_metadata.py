#!/usr/bin/env python3
"""Rebuild HUF proof/source metadata from immutable pinned blobs; no formal replay."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENT = HERE.name
VERSION = '0.49'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True, type=Path)
repo = ap.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip() == PIN
A = 'src/Development/AbelianVarietyTheory/'
M = A+'Proofs/ModuliProofs/'
U = A+'Proofs/UnitaryExistence/'
G = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/'
T = G+'BirationalGeometry/ToroidalCompactification/'

specs = {
 'host_datum':(T+'TwoWeightEqOneAddRoot.lean',14,49,'Original Host and integral projective Datum, positivity and exact trace identities'),
 'level':(T+'TwoWeightEqOneAddRoot.lean',53,66,'Original odd M>=3, half-ideal product/coprimality, A>0 and N=lcm(M,A)'),
 'SAB':(T+'TwoWeightEqOneAddRoot.lean',72,82,'Actual universal group, rigidified/cubical/symmetric line, adjoint and primitive identities'),
 'Lie':(T+'TwoWeightEqOneAddRoot.lean',105,120,'Original dual-number Lie eigenspaces and determinant multiplicities'),
 'Tate_Obj':(T+'TwoWeightEqOneAddRoot.lean',132,None,'All original TateIso and Obj fields, geometric marking, fixed root at A'),
 'Moduli':(T+'PushInvertible.lean',12,44,'Original base field, dimension, supplied representing Moduli record and coefficient field'),
 'period':(T+'IsHolPeriods.lean',13,28,'Exact ordered IsTypeFn, IsPeriod, IsHolTo and IsHolPeriods'),
 'derivative':(T+'IsHolPeriods.lean',30,35,'The original every-open/every-function dual-number derivative predicate'),
 'theta_frame':(T+'IsHolPeriods.lean',37,49,'Every IsThetaFrame field, transition orientation, rigidification, and per-fiber algebraic section'),
 'family':(T+'IsHolPeriods.lean',51,109,'All literal FamilyUnif fields including total u/ex, finite disjoint family, holomorphy, theta and local lift'),
 'N1c':(T+'IsHolPeriods.lean',111,None,'Whole original N1c quantifiers and conclusion'),
 'RelAmple_KTriv':(G+'ExtensionDescent/NonzeroLocus.lean',28,60,'Original relative-ampleness presentation and every-coefficient-ring KTriv'),
 'Weil':(G+'ExtensionDescent/ConstGen.lean',17,None,'Actual theta-line quotient and universally tested commutator/Weil relation'),
 'InGenus_Unif':(M+'FamilyUnifOfParts.lean',18,40,'Exact InGenus and pointwise Unif predicates'),
 'class_transport':(M+'FamilyUnifOfParts.lean',42,163,'Period transport, marking congruence transfer, classes, and equality'),
 'family_assembly':(M+'FamilyUnifOfParts.lean',168,None,'Original familyUnif_of_parts and its complete finite-family installation'),
 'obj_dimension':(M+'ObjIsAbelianSchemeDimRigidifiedSym.lean',207,None,'Actual abelian-scheme, dimension, rigidification and symmetry supplier'),
 'smooth_charts':(M+'ExistsHolomorphicChart.lean',71,None,'Holomorphic chart for a smooth scheme at a prescribed complex base embedding'),
 'reverse_point':(M+'ExistsUniformisationAtPointClosed.lean',18,None,'Literal reverse point uniformization at every given original moduli point'),
 'reverse_point_core':(M+'ExistsUniformisationAtPoint.lean',16,None,'Original point extraction, integral period datum and Tate-marking assembly'),
 'tate_lift':(M+'PeriodLatticeInGenus.lean',19,91,'Exact projective lifting and genus_of_tateIso, with positive-level guards'),
 'period_tate':(M+'PeriodLatticeInGenus.lean',94,None,'Original exponential Tate description and period_lattice_in_genus'),
 'relative_exp':(M+'ExistsRelativeExpOfParts.lean',53,None,'Original local jointly holomorphic relative exponential interface'),
 'lattice_continuation':(M+'LatContMapContinuous.lean',60,None,'Original full-kernel lattice continuation conclusion'),
 'local_lift':(M+'ExistsLocalPeriodLift.lean',21,None,'Full prescribed-initial-period local lift with one open neighborhood'),
 'period_coordinates':(M+'ExistsFinsetOfMemNhds.lean',325,None,'Exact PeriodCoord.exists_period_coordinates with finite period set, radius and dimension'),
 'exponential_unique':(M+'ExpEqOfPeriodsOfMarking.lean',185,None,'Actual half-level isometry rigidity and exp_eq_of_periods_of_marking'),
 'injective_holomorphic':(M+'NotInjOnOfFderivEqZero.lean',1,None,'Original injective holomorphic map/invertible derivative interface'),
 'holomorphic_family':(M+'IsHolToModulipointExpOfHolomorphicPeriodsStatement.lean',11,None,'Whole original holomorphic dependence for arbitrary pointwise choices and InGenus data'),
 'holomorphic_core':(M+'IsHolToPointAndExp.lean',226,None,'Original coordinate/injectivity/local-lift proof of point/exponential holomorphy'),
 'finite_classes':(M+'FiniteImageOfLocallyConstantOnHolomorphicFamilie.lean',71,None,'Original finite-image consequence for locally constant holomorphic families'),
 'theta_series':(T+'IsLieBasis.lean',69,113,'Actual analytic frame convention, IsAH and exact thetaChar series'),
 'omega':(T+'Clauses.lean',14,14,'Exact source symplectic form omegaStd, including its sign'),
 'theta_single':(M+'ExistsUniqueThetaCharOfUnif.lean',11,None,'Original individual normalized theta-characteristic interface'),
 'theta_gluing':(M+'ExistsThetaFrameOfPreconnected.lean',14,None,'Original theta family, preconnected characteristic constancy and frame gluing'),
 'theta_family':(M+'ExistsThetaFrameFamily.lean',1,None,'Whole original exists_thetaFrame_family with arbitrary y/e and their holomorphy hypotheses'),
 'N1c_assembly':(M+'FamilyUniformisationOfAbelianVarietyUniformisati.lean',1,None,'Original familyUnif_of_thetaUnif assembly from the point, lift, holomorphy and theta suppliers'),
 'N1c_laws':(M+'CmModuliConsequenceOfAbelianSchemeLaws.lean',1,None,'Original N1c consumer/assembly; HUF proves the conclusion using named foundations explicitly'),
 'remaining_frames':(A+'Definitions/ExistenceOfLattices/NormConst.lean',35,126,'Retained FrameOK/FramesOK/CoverTri/FibTri on the same family'),
 'remaining_principal':(U+'CongrOfDvdModulus.lean',26,None,'Exact adjoining exists_unf_hasPrinc; not claimed closed by HUF'),
}

relations = {
 1:([],['period','derivative','smooth_charts']),
 2:([1],['SAB','Tate_Obj','Moduli','RelAmple_KTriv','obj_dimension','Lie']),
 3:([1,2,'PUN21'],['theta_series','Weil','RelAmple_KTriv','reverse_point_core']),
 4:([1,2,3],['host_datum','SAB','Lie','reverse_point_core','period']),
 5:([3,4],['Tate_Obj','InGenus_Unif','tate_lift','period_tate','level']),
 6:([1,2,3,4,5],['reverse_point','InGenus_Unif']),
 7:([2,3],['relative_exp','lattice_continuation','local_lift']),
 8:([1,3,7],['local_lift','period','InGenus_Unif','Weil','Tate_Obj']),
 9:([],['period_coordinates','period','host_datum','Moduli']),
 10:([1,3,'PUN6','PUN8'],['exponential_unique','level','InGenus_Unif']),
 11:([1,8,9,'PUN23'],['smooth_charts','period_coordinates','injective_holomorphic','holomorphic_core','Moduli']),
 12:([1,9,10,11,'PUN23'],['holomorphic_family','holomorphic_core','InGenus_Unif']),
 13:([],['finite_classes','Moduli']),
 14:([6,8,'PUN15','PUN22','PUN23'],['class_transport','family_assembly','InGenus_Unif']),
 15:([1,6,12,13,14,'PUN22','PUN23','PUN24'],['family','family_assembly','InGenus_Unif']),
 16:([8,15,'PUN23'],['class_transport','family','family_assembly']),
 17:([],['period','omega','theta_family','theta_series']),
 18:([3,17,'PUN20'],['SAB','theta_series','theta_single','theta_family','theta_frame']),
 19:([18],['theta_gluing','theta_frame']),
 20:([1,12,17,18,19],['theta_family','theta_frame','family']),
 21:([1,15,16,20],['family','N1c','N1c_assembly','N1c_laws']),
}
scopes = {
 1:'Every open base in every finite complex dimension; every source scheme open and regular function; exact vertical dual-number uniqueness in both directions.',
 2:'The supplied universal object at the fixed base embedding; all original p/q including one zero, ordered type, actual line and proper relative family.',
 3:'The actual abelian-variety fiber and full exponential kernel; perfect integral form, original negative Weil commutator, all positive levels and every generator.',
 4:'Actual integral projective O_E lattice, no O_E basis assumption or finite-index replacement; exact positive J, ranks and trace identities.',
 5:'All positive n,m simultaneously, projective integral quotient lifts, exact fixed root at A and t=f_lcm(M,A), both original markings.',
 6:'Whole original reverse-point conclusion for every given y over the prescribed sigma, supplied Moduli retained.',
 7:'Prescribed initial derivative and full lattice basis; one local jointly holomorphic exponential; continued lattice equals the entire kernel by degree-one proper covering.',
 8:'Whole original local lift, preserving P(b0)=P0, same D prime and t, every positive Weil level on one neighborhood; no added InGenus hypothesis.',
 9:'Whole original finite-neighborhood coordinate interface, dimension f*p*q, every ordered type and every parameter dimension, including standalone rank zero.',
 10:'Whole exact marked-exponential uniqueness; original half-level and A markings, integral congruence, all odd M>=3 including 3.',
 11:'Actual moduli chart with the original dimension, no analytic representability axiom; zero-dimensional case included.',
 12:'Whole original arbitrary-choice holomorphic point/exponential producer; no continuity assumption on chosen pointwise functions, every open B and every m.',
 13:'Finite analytic component set for the supplied finite-type quasiprojective Moduli, not a compactness assertion.',
 14:'Exact marked integral isometry classes with the original two congruences; equal or disjoint nonempty open images, every moduli point covered.',
 15:'One finite positive family and one set of total maps chosen before every period and every analytic base; original pointwise, onto, disj, hol and ex_diff fields.',
 16:'Literal fibre and lift fields; marking congruences transferred via exact mod-N surjectivity to the original target half-lattice and full A-lattice.',
 17:'Every supplied symplectic basis/sign and normalizing h,tau; holomorphy and symmetry are derived, first-linear Hermitian sign checked.',
 18:'Constant original half-characteristics, exact primitive semicharacter and thetaChar series; line itself and rigidification matched, not just polarization.',
 19:'Proper analytic family over any original open base; flat Hom line, constant h0=1 and rigidification yield global gluing without Stein or simply connected assumptions.',
 20:'Whole original theta-family conclusion for arbitrary y/e with the original pointwise and holomorphy hypotheses; all five IsThetaFrame clauses, per-fiber algebraic GAGA section.',
 21:'Whole literal N1c and every FamilyUnif field, original fixed sigma/type, finite positive family and universal quantifier order; supplied Moduli and named foundations explicit.',
}

conrad='https://math.stanford.edu/~conrad/papers/cmchina.pdf'
milne='https://www.jmilne.org/math/CourseNotes/AV.pdf'
foundations=[
 {'id':'HUF_ORIGINAL_DATA','kind':'original_quantified_input_data','name':'Original Host, Datum, Level and fixed complex embedding/type','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'All original number-field, CM host, perfect projective integral datum, level, fixed sigma and ordered type hypotheses remain. The N1c positive-rank guard is retained. No common field or host is constructed.',
  'source_groups':['host_datum','level','period','N1c']},
 {'id':'HUF_SUPPLIED_MODULI','kind':'original_quantified_input_data','name':'The original supplied representing Moduli record','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'The original Xo with quasiprojectivity, smoothness of dimension f*p*q, universal Obj, reduced-scheme representing property and stated infinitesimal field is supplied. The chapter constructs its finite holomorphic FamilyUnif, not Xo itself. Analytic representability is not assumed.',
  'source_groups':['Moduli','Tate_Obj']},
 {'id':'HUF_STANDARD_ALGEBRA','kind':'standard_algebraic_foundations','name':'Finite lattices, Dedekind projectivity and tangent derivations','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Finite torsion-free modules over a Dedekind domain are projective; projective modules lift through surjections. Full discrete real lattices are finite free over Z. Standard finite linear algebra, separability idempotents and tangent derivations are used.',
  'application_checked':'HUF4 uses the actual exponential kernel; HUF5 lifts into the integral target lattice, with no O_E-freeness hypothesis. HUF1 proves the original dual-number dictionary.'},
 {'id':'HUF_LOCAL_ANALYSIS','kind':'standard_analytic_foundations','name':'Holomorphic local ODE, implicit function and elementary covering theory','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Holomorphic ODE has local solutions holomorphic in parameters. The holomorphic implicit/inverse function theorem, local flows, universal covers, proper local-homeomorphism covering theory, uniform convergence and elementary compact-complex maximum principles are used.',
  'application_checked':'HUF3 writes the global exponential by division and multiplication. HUF7 proves fullness of the continued lattice by a proper finite covering of degree one, instead of assuming a relative uniformization theorem. HUF8 handles all n through one Chern form.'},
 {'id':'HUF_APPELL_HUMBERT','kind':'named_published_foundation','name':'Appell-Humbert classification and positivity','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'Hermitian/semicharacter factors classify analytic lines on a complex torus, and positive definite Hermitian form is equivalent to ampleness.',
  'application_checked':'HUF3 extracts the actual form and KTriv perfection. HUF4 checks the CM adjoint identity. HUF18 uses PUN20 primitive normalization, writes the exact theta factors and verifies the first-linear sign.',
  'references':[{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic (2005)','location':'Theorem 2.2.3, p.16; Theorem 3.1.3, p.24','url':conrad,'checked_in_inherited_packet':'principal_uniformization_v48/PUN20-PUN23'}]},
 {'id':'HUF_GAGA','kind':'named_published_foundation','name':'Riemann algebraicity and projective GAGA in the inherited form','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'A positive integral period torus is algebraic; analytic homomorphisms between the resulting projective tori and coherent sheaves/sections on projective complex varieties are algebraic.',
  'application_checked':'The actual reverse-point fibers already are projective by their printed RelAmple presentation. HUF3 algebraizes the explicit Weil generators. HUF20 uses GAGA only on each projective fiber to supply its algebraic section; no algebraization of an arbitrary analytic base is inferred.',
  'references':[{'author':'J. S. Milne','title':'Abelian Varieties, version 2.0 (2008)','location':'Chapter I, Theorems 2.8-2.9, printed p.14','url':milne,'checked_in_inherited_packet':'principal_uniformization_v48'},{'author':'Brian Conrad','title':'Abelian Varieties: Geometry, Parameter Spaces, and Arithmetic','location':'Example 4.1.4, p.34','url':conrad,'checked_in_inherited_packet':'principal_uniformization_v48'}]},
 {'id':'HUF_INJECTIVE_HOLOMORPHIC','kind':'named_published_foundation','name':'Injective holomorphic maps of equal complex dimension are local biholomorphisms','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'An injective holomorphic map from an open subset of C^d into C^d has nonzero Jacobian determinant and a holomorphic inverse onto its open image.',
  'application_checked':'HUF11 proves injectivity from PUN23 and verifies both dimensions are the original f*p*q. The d=0 case is explicit.',
  'references':[{'author':'Jiri Lebl','title':'Tasty Bits of Several Complex Variables, v4.4 (31 May 2026)','location':'Theorem 1.6.6 and proof, printed pp.43-45','url':'https://www.jirka.org/scv/scv.pdf','checked_online':True}]},
 {'id':'HUF_FINITE_COMPONENTS','kind':'named_published_foundation','name':'Finite connected components of semialgebraic sets','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'A semialgebraic subset of a finite-dimensional real affine space has finitely many connected components.',
  'application_checked':'HUF13 applies it on a finite affine cover of the complex base change of the supplied Moduli, writing complex equations as real and imaginary polynomial equations. No compactness of Moduli is assumed.',
  'references':[{'author':'Michel Coste','title':'An Introduction to Semialgebraic Geometry (October 2002)','location':'Theorem 2.23, p.40; finite cylindrical decomposition Theorem 2.20, p.37','url':'https://perso.univ-rennes1.fr/michel.coste/polyens/SAG.pdf','checked_online':True}]},
 {'id':'HUF_GRAUERT_BASE_CHANGE','kind':'named_published_foundation','name':'Analytic constant-cohomology direct image and base change','not_a_DAG_claim':True,'not_reconstructed':True,
  'statement':'For a proper holomorphic map to a reduced complex base and a coherent sheaf flat over that base, constant dimension of degree-l fiber cohomology implies locally free degree-l direct image and the fiber base-change isomorphisms.',
  'application_checked':'HUF19 uses l=0, a proper torus submersion and its Hom line, flat locally over a coordinate projection, with h0=1 on every fiber. It then proves global triviality using the rigidification; the theorem alone is not said to trivialize the direct image.',
  'references':[{'author':'Hans Grauert','title':'Ein Theorem der analytischen Garbentheorie und die Modulraume komplexer Strukturen','location':'Publications mathematiques de l IHES 5 (1960), section 7, hypotheses and Satz 5, printed pp.62-64','url':'https://www.numdam.org/item/PMIHES_1960__5__5_0.pdf','doi':'10.1007/BF02684746','checked_online':True},{'author':'Hans Grauert','title':'Erratum et addendum au memoire: Ein Theorem der analytischen Garbentheorie und die Modulraume komplexer Strukturen','location':'Publications mathematiques de l IHES 16 (1963), pp.35-36','url':'https://www.numdam.org/item/PMIHES_1963__16__35_0.pdf','checked_online':True}]},
]
external={
 1:['HUF_LOCAL_ANALYSIS','HUF_STANDARD_ALGEBRA'],
 2:['HUF_ORIGINAL_DATA','HUF_SUPPLIED_MODULI','HUF_STANDARD_ALGEBRA','HUF_LOCAL_ANALYSIS','HUF_APPELL_HUMBERT'],
 3:['HUF_LOCAL_ANALYSIS','HUF_APPELL_HUMBERT','HUF_GAGA'],
 4:['HUF_ORIGINAL_DATA','HUF_STANDARD_ALGEBRA','HUF_APPELL_HUMBERT'],
 5:['HUF_ORIGINAL_DATA','HUF_SUPPLIED_MODULI','HUF_STANDARD_ALGEBRA'],
 6:['HUF_SUPPLIED_MODULI','HUF_ORIGINAL_DATA'],
 7:['HUF_LOCAL_ANALYSIS'],
 8:['HUF_ORIGINAL_DATA','HUF_LOCAL_ANALYSIS','HUF_APPELL_HUMBERT'],
 9:['HUF_ORIGINAL_DATA','HUF_STANDARD_ALGEBRA','HUF_LOCAL_ANALYSIS'],
 10:['HUF_ORIGINAL_DATA','HUF_LOCAL_ANALYSIS'],
 11:['HUF_SUPPLIED_MODULI','HUF_INJECTIVE_HOLOMORPHIC'],
 12:['HUF_LOCAL_ANALYSIS'],
 13:['HUF_SUPPLIED_MODULI','HUF_FINITE_COMPONENTS'],
 14:['HUF_ORIGINAL_DATA'],
 15:['HUF_ORIGINAL_DATA','HUF_SUPPLIED_MODULI'],
 16:['HUF_ORIGINAL_DATA','HUF_STANDARD_ALGEBRA'],
 17:['HUF_STANDARD_ALGEBRA','HUF_LOCAL_ANALYSIS'],
 18:['HUF_ORIGINAL_DATA','HUF_APPELL_HUMBERT','HUF_LOCAL_ANALYSIS'],
 19:['HUF_GRAUERT_BASE_CHANGE','HUF_LOCAL_ANALYSIS'],
 20:['HUF_GAGA','HUF_LOCAL_ANALYSIS'],
 21:['HUF_ORIGINAL_DATA','HUF_SUPPLIED_MODULI'],
}

files={}; sources={}; excerpts=[]
for key,(rel,lo,hi,title) in specs.items():
    data=(repo/rel).read_bytes()
    assert data==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel]),rel
    lines=data.splitlines(keepends=True); hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi])
    url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'HUF_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':lo,'line_end':hi,'source_commit':PIN,'file_sha256':sha(data),'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{lo}-L{hi}'}
    excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

body=(HERE/'main.tex').read_text()
assert not any(ord(c)<32 and c not in '\n\t' for c in body)
main_sha=sha(body.encode()); claims=[]; foundation_ids={f['id'] for f in foundations}
for i,(deps,groups) in relations.items():
    cid=f'HUF{i}'; m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',body,re.M|re.S)
    assert m and r'\label{claim:'+cid+'}' in m.group(),cid
    ds=[f'HUF{d}' if isinstance(d,int) else d for d in deps]
    assert all(not d.startswith('HUF') or int(d[3:])<i for d in ds)
    assert set(external[i])<=foundation_ids
    lo=body[:m.start()].count('\n')+1
    claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),'introduced_in':VERSION,'classification':'B','depends_on':ds,'external_input_ids':external[i],'scope_note':scopes[i],'source_groups':groups,'sources':[sources[k] for k in groups],'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':lo,'line_end':lo+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},'source_proof_is_not_human_proof':True})

inherited=[]
for cid in sorted({d for ds,_ in relations.values() for d in ds if isinstance(d,str)}):
    rel='principal_uniformization_v48/main.tex'; p=ROOT/rel; txt=p.read_text()
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',txt,re.M|re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':rel,'file_sha256':sha(p.read_bytes()),'claim_sha256':sha(m.group().encode()),'line_start':txt[:m.start()].count('\n')+1,'line_end':txt[:m.end()].count('\n'),'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False})

lookup={c['id']:c['proof_location']['sha256'] for c in claims}; reviews=[]; reviewed=set()
for p in sorted(HERE.glob('review_*.json')):
    r=json.loads(p.read_text())
    if r.get('status',r.get('result'))!='PASS': continue
    ids=[]; stale=False
    for e in r.get('claims_reviewed',r.get('reviewed_claims',[])):
        cid=e if isinstance(e,str) else e.get('id',e.get('claim'))
        expected=r.get('proof_hashes',{}).get(cid) if isinstance(e,str) else e.get('proof_range_sha256',e.get('block_sha256'))
        assert cid in lookup,(p,cid)
        stale=stale or expected!=lookup[cid]; ids.append(cid)
    if stale: continue
    reviewed.update(ids)
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':r.get('reviewer'),'result':'PASS','reviewed_proof_file_sha256':r.get('proof_file_sha256',r.get('proof_sha256')),'proof_file_sha256':main_sha,'reviewed_blocks_unchanged':True,'claims':ids})
status='complete_at_stated_scope_independently_reviewed' if set(lookup)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
for c in claims:
    c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
    c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]

completed=[
 {'endpoint':'GlobalTheory.PointUnif.exists_uniformisation_at_point_closed','claim':'HUF6','supporting_claims':['HUF1','HUF2','HUF3','HUF4','HUF5'],'status':'whole_literal_conclusion_written_from_named_classical_foundations','scope':scopes[6]},
 {'endpoint':'GlobalTheory.exists_local_period_lift','claim':'HUF8','supporting_claims':['HUF7'],'status':'whole_literal_prescribed_initial_period_lift_written','scope':scopes[8]},
 {'endpoint':'GlobalTheory.PeriodCoord.exists_period_coordinates','claim':'HUF9','status':'whole_literal_finite_neighborhood_coordinate_interface_written','scope':scopes[9]},
 {'endpoint':'GlobalTheory.exp_eq_of_periods_of_marking','claim':'HUF10','status':'whole_literal_marked_exponential_uniqueness_written','scope':scopes[10]},
 {'endpoint':'GlobalTheory.T.isHolTo_modulipoint_exp_of_holomorphic_periods','claim':'HUF12','supporting_claims':['HUF11'],'status':'whole_literal_arbitrary_choice_family_conclusion_written','scope':scopes[12]},
 {'endpoint':'GlobalTheory.exists_thetaFrame_family','claim':'HUF20','supporting_claims':['HUF17','HUF18','HUF19'],'status':'whole_literal_simultaneous_theta_frame_conclusion_written','scope':scopes[20]},
 {'endpoint':'ReciprocityTheory.ChartRestriction.G.Geo.Tor.N1c','claim':'HUF21','supporting_claims':['HUF13','HUF14','HUF15','HUF16','HUF20'],'status':'whole_literal_N1c_and_all_FamilyUnif_fields_written','scope':scopes[21]},
]
boundaries=[
 'The original Host, Datum, Level and representing Moduli record remain supplied; existence of the common field or that scheme is not constructed.',
 'The full original N1c is now supplied from those original data and the separately named classical analytic/algebraic foundations. It is not inferred merely from individual points.',
 'Simultaneous normalized framed points (FramesOK/CoverTri/FibTri), the exact IsUnf dictionary, and reduced-test-ring FromTest on those same frames remain separate adjoining producers. HUF alone does not close FrameUnif.exists_unf_hasPrinc.',
 'No entire ThetaUnifAV or Out.Laws predicate is declared reconstructed; the required individual analytic facts and exact family conclusions are proved here from explicit named foundations.',
 'No compound same-common-family obligation, unconditional full LatFull, higher CoversAt, all-tuple ClsEx/PointIdentCore/ClassSumsSpan, full RH or full GRH is inferred from this packet.',
]
contract={
 'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'claims':'HUF1-HUF21','claim_count':21,
 'classification_note':'All 21 numbered claims are class B written deductions with explicit original-data and named-foundation scope. Published foundations are separate external inputs and are not fake numbered DAG nodes.',
 'main_outcome':'The actual finite positive holomorphic FamilyUnif and full literal N1c: reverse point extraction, exact integral Tate/genus comparison, prescribed local lift, arbitrary-choice holomorphy, finite disjoint class selection and globally normalized theta frames.',
 'completed_source_endpoints':completed,
 'quantifier_order':['Retain every original E/H/D/l/Xo and the fixed complex base embedding sigma and ordered type.','Choose one finite positive class family, its integral genus maps and its total u/ex functions before every subsequent period and analytic family.','For local lifting retain any prescribed initial P0/e0 and produce one neighborhood preserving all positive torsion levels and both markings.','For holomorphic dependence admit arbitrary pointwise choices; their continuity is a conclusion, not a premise.','For theta retain all parameter dimensions, all open preconnected bases, every symplectic basis/sign and every normalizing h/tau satisfying the printed pointwise equations.','Gluing is global on the original open base; no Stein, simply connected or contractible-base strengthening is imposed.'],
 'literal_normalizations':{'Hermitian':'linear in the first variable','primitive_semicharacter':'alpha(Pa)=exp(pi i B(a,w0 a))','Weil_sign':'exp(-2 pi i B(a,b)/n)','root_at_A':'sigma(zeta_A)=exp(-2 pi i nu_A/A)','period_modulus':'N=lcm(M,A), exact integral quotient lifts','markings':'eta on conjugate(Mb)*L; etaA on all L','symplectic_sign':'source omegaStd together with positive Im(tau) forces sgn=-1','theta_factors':'exp(2 pi i c1.m - pi i n.tau.n - 2 pi i n.(w+c2))','theta_frame':'original transition direction and rigidification at z=0; algebraic section separately on every projective fiber'},
 'fixed_sigma_and_ordered_type_retained':True,'original_prime_three_not_excluded':True,'positive_rank_guard_retained':True,'zero_dimensional_moduli_case_retained':True,'all_parameter_dimensions_including_zero':True,'invalid_period_total_function_values_supplied':True,'all_positive_torsion_levels_on_one_neighborhood':True,'no_free_O_lattice_assumption':True,'no_analytic_moduli_representability_assumed':True,'full_N1c_supplied':True,
 'retained_input_ids':[f['id'] for f in foundations],'not_supplied':boundaries,'whole_obligations_closed':[],
 'non_premise_references':[{'location':'Present boundary paragraph','references':['PUN11','FramesOK','IsUnf','FromTest','FrameUnif.exists_unf_hasPrinc'],'reason':'Later consumers and exact remaining adjoining contracts, not hypotheses used to prove HUF21.'}],
}
manifest={'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values()),'all_files_equal_pinned_git_blobs':True,'file_count':len(files),'range_count':len(sources)}
prov={'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'main_tex_sha256':main_sha,'status':status,'claims':claims,'source_groups':sources,'inherited_human_inputs':inherited,'classical_and_foundational_inputs':foundations,'independent_reviews':reviews,'dependency_convention':'depends_on contains numbered human deductions only; original data and named foundations use external_input_ids.','source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
dag={'schema':'rh-component-human-claim-dag/1','artifact_version':VERSION,'component':COMPONENT,'nodes':[{'id':c['id'],'classification':c['classification'],'scope_note':c['scope_note'],'proof_sha256':c['proof_location']['sha256']} for c in claims],'inherited_nodes':inherited,'edges':[{'from':d,'to':c['id']} for c in claims for d in c['depends_on']],'external_inputs_are_not_DAG_claims':True}
closure={'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'completed_source_endpoints':completed,'whole_obligations_closed':[],'proposed_global_frontier_leaf_closures':[],'remaining':boundaries,'full_N1c_supplied':True,'all_FamilyUnif_fields_supplied':True,'full_principal_uniformization_supplied':False,'full_LatFull_unconditional_supplier_closed':False,'independent_reviews':reviews,'pending_independent_review':sorted(set(lookup)-reviewed),'validation':'Two-pass standalone draft TeX; no PDF or formal replay. All source bytes match the exact pinned Git blobs.'}
for name,obj in [('provenance.json',prov),('source_manifest.json',manifest),('contracts.json',contract),('original_contracts.json',contract),('closure.json',closure),('claim_dag.json',dag),('retained_foundations.json',foundations),('classical_inputs.json',foundations)]:
    (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
report=f"""HOLOMORPHIC UNIFORMIZATION FAMILY — v0.49
Source pin: {PIN}
Proof SHA256: {main_sha}
Claims: 21; pinned source files: {len(files)}; ranges: {len(sources)}; inherited human bindings: {len(inherited)}.
Status: {status}

HUF1-HUF6 recover the actual integral period datum and complete original
uniformization at every given point of the supplied Moduli. The projective
O_E lattice is retained; the original TateIso yields integral f_n, all
positive-level compatibilities, t=f_lcm(M,A), the fixed root and both markings.
The source Weil sign and its universal generator condition are computed.

HUF7-HUF8 construct a relative exponential and continue the prescribed
initial periods. A proper degree-one covering proves the continued lattice
is the entire kernel. One neighborhood preserves all n, using the constant
integral form and the two finite torsion markings, not infinitely many shrinks.

HUF9-HUF12 construct the original f*p*q period coordinates, prove marked
exponential uniqueness including M=3, and derive holomorphic dependence
for arbitrary pointwise u/ex choices. The map from a smooth moduli chart
to the period domain is injective by PUN23, and hence locally biholomorphic.
No analytic moduli-representing property is assumed.

HUF13-HUF16 construct one finite positive disjoint family and its single
total maps before all periods and all bases. Finiteness uses a finite affine
cover and the classical semialgebraic finite-component theorem; it does not
assert compactness of the moduli scheme. The exact fibre and lift fields,
including the source half-lattice and full-A congruences, are proved.

HUF17-HUF20 derive the holomorphy of h/tau, the forced first-linear
Hermitian sign, and one constant half-characteristic from the actual
primitive semicharacter. The exact theta automorphy factors define a line.
Grauert applied to its Hom line with the actual universal line gives a
locally free direct image with h0=1; rigidification then proves global
triviality and the uniquely normalized frame on any original open base.
No Stein or simply connected assumption is imposed. Per-fiber GAGA gives
the algebraic section required by the last IsThetaFrame clause.

HUF21 installs every literal FamilyUnif field and the whole original N1c.
All 21 claims are class B written deductions. Appell-Humbert, Riemann/GAGA,
holomorphic local analysis, Lebl's injective-map theorem, Coste's finite
component theorem and Grauert's precise analytic base-change theorem
(with corrigendum) are named external foundations, not numbered proof nodes.

The original Moduli record itself is supplied. Simultaneous normalized
framed points, the complete IsUnf/FromTest dictionary and the final
FrameUnif.exists_unf_hasPrinc remain separate adjoining producers.
No compound common-family obligation or full RH/GRH closure is inferred.

Rebuild: python build_metadata.py --repo /path/to/formal_source
Validate: python validate_tex.py --format /path/to/pdflatex.fmt
No frozen v0.48 proof, source file, root ledger or shared reader was edited.
"""
(HERE/'report.txt').write_text(report)
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps({'artifact_version':VERSION,'component':COMPONENT,'hashes':hashes},indent=2)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_human_inputs':len(inherited),'proof_file_sha256':main_sha,'status':status},indent=2))
