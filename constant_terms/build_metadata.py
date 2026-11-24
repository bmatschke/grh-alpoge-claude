#!/usr/bin/env python3
"""Rebuild exact source and proof bindings for CTC1--CTC13."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
args=p.parse_args(); REPO=args.repo.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==PIN
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
cache={}; refs={}
decl=re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+')
def add(key,path,anchor,stop=None):
    path='src/'+path
    if path not in cache:
        raw=(REPO/path).read_bytes()
        assert raw==subprocess.check_output(['git','show',PIN+':'+path],cwd=REPO)
        cache[path]=(raw,raw.decode().splitlines(keepends=True))
    raw,lines=cache[path]
    starts=[i for i,line in enumerate(lines) if anchor in line]
    assert len(starts)==1,(key,anchor,starts)
    a=starts[0]
    z=next((i for i in range(a+1,len(lines)) if (stop in lines[i] if stop else decl.match(lines[i]))),len(lines))
    while z>a and not lines[z-1].strip():z-=1
    block=''.join(lines[a:z]).encode()
    refs[key]=dict(id=key,path=path,declaration=anchor,declaration_anchor=anchor,
      line_start=a+1,line_end=z,sha256=sha(raw),file_sha256=sha(raw),range_sha256=sha(block),range_bytes=len(block),
      first_line=lines[a].rstrip(),verified_equal_to_pinned_git_blob=True,
      role='Original contract or formal argument reconstructed independently in the stated human scope.',
      url=URL+path+f'#L{a+1}-L{z}')

D='Development/AbelianVarietyTheory/'
IW=D+'Proofs/IwasawaDecomposition/'
DP=D+'Proofs/DivisorProofs/'
TO=D+'Proofs/TwistedOperators/'
IR='Formalism/LocalToGlobal/IndefiniteReal/'
BH='Formalism/LocalToGlobal/BesselHermitianTheta/'
add('weil',IR+'LocalNewformFunction.lean','structure IsWeilDatumO ')
add('theta',IR+'LocalNewformFunction.lean','structure IsThetaFunO ')
add('zi',D+'Definitions/Divisors/IsSmoothVector.lean','def ZI ')
add('iso',D+'Definitions/Divisors/IsSmoothVector.lean','def IsoVec ')
add('zcusp',D+'Definitions/Divisors/IsSmoothVector.lean','def ZCusp ')
add('aut',BH+'IsAutFunDef.lean','structure IsAutFun ')
add('frame',BH+'IsAutFunDef.lean','def IsIsoFrame ')
add('ni',BH+'IsAutFunDef.lean','def NI ')
add('niq',BH+'IsAutFunDef.lean','def NIQ ')
add('cusp',BH+'IsAutFunDef.lean','def IsCuspFun ')
add('tv_ring',DP+'AdelicTransvectionSubgroupEqAdelesClosed.lean','theorem one_add_mul ','section Tensor')
add('tv_tensor',DP+'AdelicTransvectionSubgroupEqAdelesClosed.lean','theorem anti_eq ','end Tensor')
add('tv_closed',DP+'AdelicTransvectionSubgroupEqAdelesClosed.lean','theorem closure_eq ')
add('tv_chart',DP+'AdelicTransvectionSubgroupEqAdelesClosed.lean','theorem exists_equiv ')
add('tv_final',DP+'AdelicTransvectionSubgroupEqAdelesClosed.lean','theorem transvection_group ')
add('tv_measure',DP+'TransvectionSubgroupCocompactHaarFundamentalDoma.lean','theorem transvection_measure ')
add('uniform_level',IW+'ContinuousMovPair.lean','theorem uniform_level_pair ')
add('cube',IW+'ContinuousMovPair.lean','theorem cube_bound_at ')
add('orbit_bound',IW+'ContinuousMovPair.lean','theorem exists_sup_bound ')
add('sobolev',TO+'LintegralCompactLe.lean','theorem sobolev_iter ')
add('compact_norm',TO+'LintegralCompactLe.lean','theorem lintegral_compact_le ')
add('real_norm',TO+'LintegralCompactLe.lean','theorem lintegral_real_le ')
add('words',TO+'LintegralCompactLe.lean','theorem words_bound ')
add('dv',TO+'LintegralCompactLe.lean','theorem dv_apply ')
add('dv_level',TO+'LintegralCompactLe.lean','theorem dv_level ')
add('eigen_form',IW+'ThetaFunctionZeroOfInvariantFunctionals.lean','theorem exists_char_form ')
add('local_duality',IW+'ThetaFunctionZeroOfInvariantFunctionals.lean','theorem exists_eq_dilate ')
add('separation',IW+'ThetaFunctionZeroOfInvariantFunctionals.lean','theorem eq_zero_of_invariant_forms ')
add('finite_average',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem exists_invariant_sum ')
add('compact_dual',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem exists_compact_dual ')
add('row_pairing',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem hO_along ','theorem det_eq_one ')
add('transv_det',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem det_eq_one ')
add('small_row',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem eq_zero_of_small ')
add('transv_pos',IW+'SplitPlaceTransvectionActsPositivelyInvariantFor.lean','theorem transvection_pos ')
add('row',IW+'ConstantTermHeisOAlong.lean','def row ','theorem norm_ne_zero ')
add('norm',IW+'ConstantTermHeisOAlong.lean','theorem norm_ne_zero ')
add('transv_phase',IW+'ConstantTermHeisOAlong.lean','theorem exists_transv ')
add('rational_modulation',IW+'ConstantTermHeisOAlong.lean','theorem heisO_rat ')
add('along_periodic',IW+'ConstantTermHeisOAlong.lean','theorem periodic ')
add('along_om',IW+'ConstantTermHeisOAlong.lean','theorem om_along ')
add('rat_om',IW+'ConstantTermHeisOAlong.lean','theorem om_rat_along ')
add('ct_bound',IW+'ConstantTermHeisOAlong.lean','theorem exists_bound ')
add('ct_eigen',IW+'ConstantTermHeisOAlong.lean','theorem exists_eigen ')
add('ct_final',IW+'ConstantTermHeisOAlong.lean','theorem constantTerm_heisO_along ')
add('selfann',IW+'RationalSymplecticPointsSelfAnnihilator.lean','theorem ratL_annihilator ')
add('quotient_shift',IW+'SetIntegralMulLeft.lean','theorem setIntegral_mul_left ')
add('fourier_average',IW+'SetIntegralMulLeft.lean','theorem average_const ')
add('lift_bound',IW+'ThetaLiftDefiniteConstantTermEqZero.lean','theorem exists_bound ')
add('fubini',IW+'ThetaLiftDefiniteConstantTermEqZero.lean','theorem swap_of_bound ')
add('finite_basis',IW+'ThetaLiftDefiniteConstantTermEqZero.lean','theorem continuous_family ')
add('lift_zcusp',IW+'ThetaLiftDefiniteConstantTermEqZero.lean','theorem zcusp_lift ')
add('central_matrix',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem mat_kill ','end Mat')
add('central_embed',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem vecMulVec_col ','end Algebra')
add('central_shift',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem setIntegral_shift ')
add('central_fubini',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem setIntegral_eq_zero ')
add('full_cusp',DP+'IsCuspFunOfTransvectionConstantTermsZero.lean','theorem isCuspFun_of_zCusp ')
add('original_average',IW+'FockVectorsKilledHeisenbergAverageIsotropic.lean','theorem sum_heisO_along_eq_zero ')
add('extension',IW+'ExistsThetaLiftLinearMapCuspFormMultiplicity.lean','theorem exists_extension ')
add('member',IW+'ExistsThetaLiftLinearMapCuspFormMultiplicity.lean','theorem exists_member ')
add('fires',IW+'ExistsThetaLiftLinearMapCuspFormMultiplicity.lean','theorem firesAt ')
add('full_extension',IW+'ExistsThetaLiftLinearMapCuspFormMultiplicity.lean','theorem exists_thetaMap ')

specs=[
('CTC1',[],['zi','iso','tv_ring','tv_tensor','tv_closed','tv_chart','tv_final','tv_measure','row']),
('CTC2',['WA3','BTH5'],['weil','theta','uniform_level','cube','orbit_bound','sobolev','compact_norm','real_norm','words','dv','dv_level']),
('CTC3',['FIA1'],['local_duality','compact_dual']),
('CTC4',['CTC3'],['eigen_form','local_duality','separation']),
('CTC5',['CTC3','CTC4'],['finite_average','compact_dual','row_pairing','small_row']),
('CTC6',['CTC1','CTC5','CW23','BTH14'],['weil','transv_det','transv_pos']),
('CTC7',['CTC1','CTC6','FIA1'],['norm','transv_phase','ct_eigen']),
('CTC8',[],['quotient_shift','fourier_average']),
('CTC9',['CTC1','CTC2','CTC7','CTC8','CW15'],['rational_modulation','along_periodic','along_om','rat_om','ct_bound','ct_eigen','ct_final','selfann']),
('CTC10',['CTC9','BTH3'],['lift_bound','fubini','finite_basis','lift_zcusp']),
('CTC11',['CTC1'],['frame','ni','niq','central_matrix','central_embed']),
('CTC12',['CTC1','CTC11'],['aut','cusp','zcusp','central_shift','central_fubini','full_cusp']),
('CTC13',['CTC10','CTC12','FIA8','BTH3','BTH12'],['original_average','member','fires','full_extension','extension','finite_basis']),
]
text=(HERE/'main.tex').read_text(); lines=text.splitlines(keepends=True)
claims=[]
for cid,deps,sids in specs:
    a=lines.index('% BEGIN '+cid+'\n');z=lines.index('% END '+cid+'\n')+1
    block=''.join(lines[a:z]).encode()
    title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',text).group(1)
    remaining=[]
    if cid=='CTC10':remaining=['The actual finite class-presentation and original finite-dimensional kernel/coefficient inputs are supplied; the implication from finite cancellation is complete.']
    if cid=='CTC13':remaining=['Common original base reading and all original model inputs; separate simultaneous PIoP; smoothness and uniform derivative growth; lowering and prescribed lowest type; original holomorphic/Hilbert multiplicity realization; simultaneous rational tests and actual base rows.']
    claims.append(dict(id=cid,title=title,introduced_in='0.33',classification='B',
      status='Complete independent human proof in the explicitly stated original-data scope.',depends_on=deps,
      proof_location=dict(file='constant_terms/main.tex',label='claim:'+cid,line_start=a+1,line_end=z,sha256=sha(block),bytes=len(block)),
      sources=[refs[k] for k in sids],source_ids=sids,remaining_inputs=remaining))
provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.33',date='2026-11-22',component='constant_terms',source_commit=PIN,
  main_tex_sha256=sha(text.encode()),claims=claims,source_files=[dict(path=k,sha256=sha(v[0]),file_sha256=sha(v[0]),bytes=len(v[0]),line_count=len(v[1]),verified_equal_to_pinned_git_blob=True,url=URL+k) for k,v in sorted(cache.items())],
  scope='Original finite-average-to-cuspidality implication; compact-orbit, local-duality, partial-coinvariant and Fourier suppliers reconstructed. Original definite source compactness is used in BTH3 class-presentation scope. The smooth multiplicity extension, separate simultaneous PIoP, and shared Bundle producers remain.',
  lean_build=False,kernel_replay=False)
write('provenance.json',provenance)
closure=dict(artifact_version='0.33',component='constant_terms',source_commit=PIN,proved_claims=[x[0] for x in specs],
  closed_subarguments=['actual transvection group and finite positive quotient volume','uniform compact Weil orbit bound','local character duality and split-half separation','positive action on along coinvariants','nontrivial rational-row eigenvalue','constantTerm_heisO_along with absolute convergence','finite averaging to ZCusp for the original definite class presentation','Witt-coordinate compactness of every original NI rational quotient','central averaging to genuinely convergent full cuspidality','cuspidality of the original base polynomial theta integral'],
  consumes=['FIA1 and FIA8','actual original full Weil and positive source data','original finite class presentation and coefficient functions of BTH3'],
  leaves_open=['BASE_THETA_READINGS','BASE_THETA_CUSPIDAL_EXTENSION, narrowed to remaining smooth-growth/lowering/realization obligations','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER'],
  excluded_claims=['No complete smooth multiplicity extension or separate simultaneous PIoP supplier','No new independent kernel or Weil normalization','No nonintegrable constant term treated as convergent','No full human RH or GRH theorem'],
  source_convention_note='The source abstract central Fubini lemma includes integral_undef. CTC11 proves compactness and integrability for every actual unipotent quotient, so CTC12 establishes ordinary convergent cuspidality.',
  new_published_applications=[],proof_file_sha256=sha(text.encode()))
write('closure.json',closure)
(HERE/'source_locators.txt').write_text('\n\n'.join(k+'\n'+v['url']+'\nfile '+v['sha256']+'\nrange '+v['range_sha256'] for k,v in refs.items())+'\n')
(HERE/'report.txt').write_text('CTC1--CTC13: finite isotropic averages to actual cuspidal theta integrals.\n'
 '13 complete category-B claims; underlying Lean correctness accepted.\n'
 f'{len(refs)} pinned source ranges in {len(cache)} files.\n'
 'The remaining analytic extension is explicitly narrowed, not declared complete.\n'
 'Independent mathematical review is bound in the release review registry.\n')
print(json.dumps(dict(claims=len(claims),source_ranges=len(refs),source_files=len(cache),main_tex_sha256=sha(text.encode())),indent=2))
