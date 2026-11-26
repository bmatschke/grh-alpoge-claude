#!/usr/bin/env python3
"""Build exact SBD source/proof certificates; no Lean build or replay."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,default=HERE.parent.parent/'lean_source')
p.add_argument('--human-root',type=Path,default=HERE.parent.parent/'reconstruction_v037')
p.add_argument('--peer-root',type=Path,default=HERE.parent)
a=p.parse_args(); SOURCE=a.source.resolve(); HUMAN=a.human_root.resolve(); PEER=a.peer_root.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'; REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
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
def add(sid,path,anchor,role='Exact original source contract or dictionary; independent human argument in SBD'):
    path='src/'+path; b,ls=get(path); hits=[i for i,l in enumerate(ls) if anchor in l]
    assert len(hits)==1,(sid,anchor,hits)
    i=hits[0];j=next((j for j in range(i+1,len(ls)) if decl.match(ls[j])),len(ls))
    while j>i and not ls[j-1].strip():j-=1
    block=''.join(ls[i:j]).encode()
    sources[sid]={'id':sid,'path':path,'declaration':anchor,'declaration_anchor':anchor,
      'line_start':i+1,'line_end':j,'sha256':sha(b),'file_sha256':sha(b),'range_sha256':sha(block),
      'range_bytes':len(block),'first_line':ls[i].rstrip(),'role':role,
      'verified_equal_to_pinned_git_blob':True,'url':f'{REPO}/blob/{PIN}/{path}#L{i+1}-L{j}'}
def inherit(comp,ids):
    old={s['id']:s for s in json.loads((HUMAN/comp/'provenance.json').read_text())['source_inventory']}
    for sid in ids:
        s=dict(old[sid]);b,ls=get(s['path'])
        assert sha(b)==s.get('file_sha256',s['sha256'])
        assert sha(''.join(ls[s['line_start']-1:s['line_end']]).encode())==s['range_sha256']
        sources[sid]=s
inherit('smooth_representatives',[
 'finite_pair','quotient_measure','central_cuspidality','multiplicity_map_contract',
 'full_multiplicity_extension','bounded_holomorphic_form','remaining_boundedness','remaining_target_volume',
 'smooth_automorphic_contract','automorphic_contract','extension','theta_member','fires_at','theta_map',
 'level_open','restriction','linear_theta_lift','theta_fires_consumer','fires_contract','theta_mult_contract'])
inherit('theta_extension',['smoothness_contract','uniform_growth_contract','integral_growth','integral_smooth_growth_killed'])
inherit('holomorphic_uniqueness',['borel_killed','source_borel_extremal','extremal_vector','extremal_weight'])
inherit('regular_quotient',['transvection_subgroup','transvection_group','transvection_measure'])
D='Development/AbelianVarietyTheory/';IW=D+'Proofs/IwasawaDecomposition/';DP=D+'Proofs/DivisorProofs/';HP=D+'Proofs/HeightProofs/'
for sid,anchor in [('original_oneP','def oneP '),('original_Rder','def Rder '),
 ('original_conjAt','def conjAt '),('original_RderC','def RderC '),
 ('original_gelf','def gelf '),('original_normInf','def normInf ')]:
    add(sid,'Formalism/LocalToGlobal/BesselHermitianTheta/TiedSmooth.lean',anchor)
for sid,anchor in [('holAd','def HolAd '),('isotropic_vector','def IsoVec ')]:
    add(sid,D+'Definitions/Divisors/IsSmoothVector.lean',anchor)
add('initial_borel_equations',IW+'HolomorphicTypeAtExtremalOfKEquivariantLoweringK.lean','theorem holAd_of_kEquiv ')
add('initial_compact_derivative',IW+'HolomorphicTypeAtExtremalOfKEquivariantLoweringK.lean','theorem rder_eq ')
for sid,anchor in [('smooth_real_dictionary','theorem smooth_iff '),('op_at_bracket','theorem opAt_bracket '),
 ('op_at_comm','theorem opAt_comm '),('env_rep','theorem exists_envRep '),
 ('literal_gelf_bridge','theorem exists_gelf '),('literal_zfin_bridge','theorem zfin_iff ')]:
    add(sid,HP+'ExistsSigmaList.lean',anchor,
        'Original differential/center interface; SBD proves its needed implication independently and does not claim the full center-generation theorem')
add('source_center_generation',HP+'PolarConjTranspose.lean','theorem center_eq_adjoin ',
    'Boundary only: separate source center-generation theorem is not reconstructed or used by SBD3')
for sid,anchor in [('universal_cusp_predicate','def CuspRapidDecay '),('source_bounded_cusp','theorem bounded_of_cuspForm '),
 ('source_order_zero','theorem IsRapidDecay.bounded ')]:
    add(sid,D+'PublishedTheorems/AutomorphicForms₂/ExistsNormLeHeightPow.lean',anchor,
        'Original sufficient stronger source interface; universal global quotient-height predicate is not claimed by SBD')
add('source_initial_bound',IW+'BoundedOfSmoothCuspidalUniformModerate.lean','theorem bounded_of_smooth_unifModGrowth :',
    'Original boundedness consumer; SBD supplies the needed extremal-seed specialization without its stronger universal hP premise')
add('source_transvection_to_cusp',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem isCuspFun_of_zCusp :')
maps=[
 ['original_oneP','original_Rder','original_conjAt','original_RderC','smoothness_contract','smooth_real_dictionary','op_at_bracket','op_at_comm','env_rep'],
 ['initial_borel_equations','initial_compact_derivative','borel_killed','source_borel_extremal','extremal_vector','extremal_weight'],
 ['env_rep','source_borel_extremal','literal_zfin_bridge','source_center_generation'],
 ['original_gelf','original_RderC','smooth_automorphic_contract','literal_gelf_bridge','literal_zfin_bridge'],
 ['original_normInf','uniform_growth_contract','smoothness_contract','automorphic_contract'],
 ['transvection_measure','transvection_group'],
 ['transvection_subgroup','transvection_group','isotropic_vector'],
 ['central_cuspidality','transvection_subgroup','transvection_measure','automorphic_contract'],
 ['central_cuspidality','isotropic_vector','source_transvection_to_cusp'],
 ['source_transvection_to_cusp','transvection_measure'],
 ['source_transvection_to_cusp','central_cuspidality','source_bounded_cusp'],
 ['source_initial_bound','source_bounded_cusp','universal_cusp_predicate','source_order_zero','smooth_automorphic_contract'],
 ['fires_at','theta_member','integral_smooth_growth_killed','integral_growth','level_open','initial_borel_equations','source_initial_bound'],
 ['extension','full_multiplicity_extension','bounded_holomorphic_form','finite_pair','restriction'],
 ['theta_map','fires_at','theta_member','linear_theta_lift','theta_fires_consumer','fires_contract','theta_mult_contract','finite_pair','quotient_measure'],
 ['theta_map','multiplicity_map_contract','fires_contract','theta_mult_contract']
]
deps=[
 ['ASB1','ASB2','ASB3','HCU14'],
 ['SBD1','HCU13','HCU19'],[],
 ['SBD1','SBD2','SBD3','RQC17'],
 ['SBD1','FV4','FV10'],['ASB7','ASB9'],['FV1','FV4'],
 ['SBD6','SBD7','FV10'],['SBD7','FV1','FV2','FV4','FV10'],[],
 ['SBD8','SBD9','SBD10'],
 ['SBD2','SBD3','SBD4','SBD5','SBD11','FV10'],
 ['SBD12','FV9','HCU13','HCU20','TAE13','CTC13','FIA8','JIO19','SPR25'],
 ['SBD2','SBD12','FV8','FV9','HCU13','HCU19','SPR21','SPR22'],
 ['SBD13','SBD14','FV11','SPR22','SPR24','SPR25','JIO19'],
 ['SBD15','BTH4','BTH5','BTH6','BTH7','BTH12','SPR24','SPR25']
]
scopes=[
 'Exact smooth function module on original real cosets; original RderC, right-fold order and full direct-sum complex Lie algebra; no target Hilbert input.',
 'Original initial extremal function at every adelic point; same x0Mat, all upper units and original integral weights.',
 'Any module of a finite direct sum of gl_n with highest-weight equations; full-center scalar action by ordered spanning and weight projection, no PBW independence assumption.',
 'Full-center finiteness and literal source gelf zfin on one initial span, including zero seed; k means length k+1.',
 'Actual arithmetic Gamma_s at compact-open finite level; one source exponent before all words; original normInf matched to a faithful norm at least one.',
 'Every compact-open additive finite level; actual diagonal F, real lattice and product fundamental domain.',
 'Every original nonzero isotropic xi; exact ZI, its topology and its rational subgroup, via anti-invariant eta F line.',
 'Every finite representative and every isotropic xi; actual original ZCusp, same finite level, genuine compact integrals and no ambient measure change.',
 'Every proper rational parabolic of actual Res_F/Q U(J); checked cocharacter theorem and original central transvection found from maximal positive weight.',
 'Every unipotent rational subgroup and arithmetic lattice; rational exponential-box proof of compactness and invariant measure.',
 'Every proper rational parabolic and every real argument, for exact Gamma_s; central transvection averaging and compact Fubini.',
 'Miller-Schmid Theorem A and finite rational Siegel covering with all original group, center, arithmetic, smoothness, growth and cusp hypotheses checked.',
 'For every i,t,x there exists C before all target g; same i-extremal/io_i and compact open level before t,x; no uniform C in t,x.',
 'Full original exists_extension implication with every original data premise; stronger universal CuspRapidDecay replaced by proved needed seed bound and FV8.',
 'One actual all-i,t theta family on same R, all source vectors, original kernels/measures/levels/io_i and stored weak-choice activation.',
 'Full selected BASE_THETA_CUSPIDAL_EXTENSION on common original data, with parent threshold before all indices/basis; other common-data producers remain separate.'
]
pubs=[
 {'id':'SBD_PARABOLIC_COCHARACTER','classification':'A','status':'checked_application',
  'title':'Rational cocharacters describe parabolics and their unipotent radicals',
  'authors':'J. S. Milne','publication':'Algebraic Groups: The Theory of Group Schemes of Finite Type over a Field (2017)',
  'url':'https://www.jmilne.org/math/Books/iAG2017.pdf',
  'theorem':'Theorem 25.1, printed p.544; Proposition 17.60, printed p.372',
  'used_by':['SBD9'],
  'hypotheses_checked':['actual smooth connected reductive Q-group by FV1–FV4/FV10','proper Q-parabolic of that actual group','characteristic zero base field','cocharacter defined over Q; restriction-of-scalars adjunction supplies F-cocharacter'],
  'conclusion_used':'P=P(lambda), Ru(P)=U(lambda) contracted to the identity; subsequent central transvection construction is independently proved.',
  'not_claimed':'No replacement of original transvection subgroup or assumption that unitary group splits over F.'},
 {'id':'SBD_RAPID_DECAY','classification':'A','status':'checked_application',
  'title':'Rapid decay of smooth cuspidal automorphic forms',
  'authors':'Stephen D. Miller and Wilfried Schmid',
  'publication':'Advances in Mathematics 231 (2012), 940–964; inspected author preprint arXiv:1106.2149v1 (10 June 2011)',
  'doi':'10.1016/j.aim.2012.06.001','url':'https://arxiv.org/pdf/1106.2149',
  'theorem':'Theorem A printed p.3; exact hypotheses (6.1),(6.3) printed p.29',
  'used_by':['SBD12'],
  'hypotheses_checked':['real points of actual reductive Q-group FV10','compact real center FV10','actual arithmetic Gamma_s FV10','source smoothness SBD1/SBD5','faithful linear norm and moderate growth SBD5','full enveloping-center finiteness before Hilbert construction SBD3/SBD4','every rational-parabolic classical cusp integral SBD11','same checks for each rational left translate in finite Siegel cover'],
  'conclusion_used':'Exponent one gives a uniform bound on each indicated Siegel set; finite-cover maximum supplies all real points.',
  'not_claimed':'The stronger universal source CuspRapidDecay/global quotient-height predicate; no K- or Hecke-finiteness input assumed.'},
 {'id':'SBD_SIEGEL_COVER','classification':'A','status':'checked_application',
  'title':'Finite rational Siegel covering for the actual arithmetic subgroup',
  'authors':'Stephen D. Miller and Wilfried Schmid (recording the standard reduction theorem)',
  'publication':'Same author preprint arXiv:1106.2149v1','url':'https://arxiv.org/pdf/1106.2149',
  'theorem':'Equation (2.8), printed p.8; standing hypotheses (2.1),(2.2)',
  'used_by':['SBD12'],
  'hypotheses_checked':['actual reductive Q-group with compact real center FV10','actual arithmetic Gamma_s FV10','ordinary Siegel set with suitable compact left factor and chamber bound'],
  'conclusion_used':'Finite rational C and a Siegel set S with G_infinity=union Gamma_s c S; left-translated forms are checked separately.',
  'not_claimed':'No unproved uniform bound across infinitely many rational translates.'}
]
tex=(HERE/'main.tex').read_bytes();ll=tex.splitlines(keepends=True);claims=[]
for n in range(1,17):
    cid=f'SBD{n}'; i=next(i for i,l in enumerate(ll) if l.strip()==f'% BEGIN {cid}'.encode())
    j=next(i for i,l in enumerate(ll) if l.strip()==f'% END {cid}'.encode())+1
    block=b''.join(ll[i:j]);title=next(l.decode().strip() for l in ll[i:j] if l.startswith(b'\\paragraph{'))[11:-1]
    claims.append({'id':cid,'title':title,'introduced_in':'0.38','classification':'A' if n==12 else 'B',
      'status':'complete checked published application' if n==12 else 'complete independent human proof of the explicitly stated implication',
      'depends_on':deps[n-1],'quantifier_scope':scopes[n-1],
      'proof_location':{'file':'seed_boundedness/main.tex','label':'claim:'+cid,'line_start':i+1,'line_end':j,'sha256':sha(block),'bytes':len(block)},
      'published_application_ids':(['SBD_PARABOLIC_COCHARACTER'] if n==9 else ['SBD_RAPID_DECAY','SBD_SIEGEL_COVER'] if n==12 else []),
      'source_ids':maps[n-1],'sources':[sources[s] for s in maps[n-1]]})
baseline=[]
for root,rel,ids in [
 (HUMAN,'adelic_sobolev/main.tex',['ASB1','ASB2','ASB3','ASB7','ASB9']),
 (HUMAN,'holomorphic_uniqueness/main.tex',['HCU13','HCU14','HCU19','HCU20']),
 (HUMAN,'regular_quotient/main.tex',['RQC1','RQC17']),
 (HUMAN,'theta_extension/main.tex',['TAE13']),
 (HUMAN,'constant_terms/main.tex',['CTC13']),
 (HUMAN,'finite_isotropic_average/main.tex',['FIA8']),
 (HUMAN,'joint_harmonic_io/main.tex',['JIO19']),
 (HUMAN,'smooth_representatives/main.tex',['SPR21','SPR22','SPR24','SPR25']),
 (HUMAN,'base_theta/main.tex',['BTH4','BTH5','BTH6','BTH7','BTH12']),
 (PEER,'finite_volume/main.tex',[f'FV{i}' for i in range(1,12)])]:
    b=(root/rel).read_bytes();ls=b.splitlines(keepends=True);blocks=[]
    for cid in ids:
        i=next(i for i,l in enumerate(ls) if l.strip()==f'% BEGIN {cid}'.encode())
        j=next(i for i,l in enumerate(ls) if l.strip()==f'% END {cid}'.encode())+1;bb=b''.join(ls[i:j])
        blocks.append({'id':cid,'line_start':i+1,'line_end':j,'sha256':sha(bb),'bytes':len(bb)})
    baseline.append({'file':rel,'sha256':sha(b),'file_sha256':sha(b),'role':'Exact inherited or jointly reconstructed proof input; no reverse SBD-to-FV dependency.','claims':blocks})
remaining=[
 {'id':'SBD_UNIVERSAL_GLOBAL_HEIGHT_DECAY','classification':'C','status':'not reconstructed and not required by this selected initial-extension proof',
  'contract':'Original Published.CuspRapidDecay for arbitrary smooth uniformly moderate IsCuspFun, with every quotient-height exponent; SBD uses pre-Hilbert highest-weight and ZCusp on the actual seed only.',
  'source_ids':['universal_cusp_predicate'],'not_new_independent_top_level_obligation':True},
 {'id':'SBD_COMMON_DATA_REMAIN','classification':'C','status':'retained distinct original producers',
  'contract':'The same selected R, common geometric readings, rational tests and actual base rows are still supplied by their own branches; analytic construction does not create them.',
  'source_ids':['theta_map','fires_contract'],'not_new_independent_top_level_obligation':True}
]
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.38','date':'2026-11-22','component':'seed_boundedness',
 'source_commit':PIN,'main_tex_sha256':sha(tex),
 'metadata_builder':{'file':'build_metadata.py','sha256':sha(Path(__file__).read_bytes()),
 'portable_invocation':'python3 build_metadata.py --source /path/to/pinned/checkout --human-root /path/to/reconstruction --peer-root /path/to/reconstruction'},
 'claims':claims,'source_inventory':list(sources.values()),'baseline_dependencies':baseline,'published_applications':pubs,
 'remaining_producer_contracts':remaining,
 'validation':{'source_commit_verified':True,'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),
 'claim_source_occurrences':sum(map(len,maps)),'all_source_ranges_exact':True,'new_lean_build':False,
 'tex_validation':'Standalone and cumulative draft syntax only.'},
 'scope_note':'Full original initial theta boundedness, complete lowest-type extension and all-parameter theta family on original common data. Selected BASE_THETA_CUSPIDAL_EXTENSION supplied; stronger universal global-height decay unclaimed.'}
(HERE/'provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
closed=[('initial extremal seed bound',['SBD13']),
 ('ThetaMap.exists_extension on original data without the sufficient stronger hP',['SBD14']),
 ('ThetaMap.exists_member / firesAt on original theta data',['SBD14','SBD15']),
 ('ThetaMap.exists_thetaMap on original common data',['SBD15']),
 ('BASE_THETA_CUSPIDAL_EXTENSION',['SBD16'])]
closure={'schema':'rh-component-closure/1','version':'0.38','component':'seed_boundedness','source_commit':PIN,
 'main_tex_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'new_claims':[c['id'] for c in claims],'claim_count':16,'class_counts':{'A':1,'B':15,'C':0,'D':0},
 'all_new_claims_are_conditional_implications':True,
 'closed_subtargets':[{'source_declaration':x,'proof':y} for x,y in closed],
 'closed_prior_residues':[{'id':'SPR_INITIAL_TARGET_VOLUME_AND_BOUND','status':'closed jointly with FV8/FV11 and SBD13','proof':['FV8','FV11','SBD13','SBD15']},
 {'id':'BASE_THETA_CUSPIDAL_EXTENSION','status':'complete on original common-data premises; one whole selected producer leaf supplied','proof':['SBD16']}],
 'remaining_producer_contracts':remaining,'selected_top_level_leaf_closed':True,
 'selected_top_level_leaf_ids':['BASE_THETA_CUSPIDAL_EXTENSION'],'published_applications':pubs,
 'same_object_guards':['same original R and target W_i','same actual source integral and its measures',
 'target FinPair before every t,x','same extremal and io_i before t','full center proved before Hilbert construction',
 'exact original ZI and rational subgroup','same compact-open K and Gamma_s','literal gelf length k+1 and right-fold order',
 'original MMap and Wall_i','all t,x with no new family threshold','stored weak choice activated without witness identification',
 'common readings/rational tests/base rows remain separate']}
(HERE/'closure.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')
(HERE/'published_applications.json').write_text(json.dumps(pubs,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_locators.txt').write_text('\n'.join(f'{s["id"]}: {s["path"]}:{s["line_start"]}-{s["line_end"]} [{s["range_sha256"]}]\n{s["url"]}' for s in sources.values())+'\n')
print(json.dumps({'claims':len(claims),'files':len(cache),'ranges':len(sources),'claim_source_references':sum(map(len,maps)),
 'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes())},indent=2))
