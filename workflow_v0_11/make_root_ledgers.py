"""Generate standalone GJ/GW provenance builders using the validated parser."""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]
TEMPLATE = (BASE / 'v0_10/type_one_closure/build_provenance.py').read_text()
PARSER = TEMPLATE[TEMPLATE.index('PREFIX ='):TEMPLATE.index('\n\n\nDEFS =')]
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
SH = 'src/Formalism/SharpRestriction/'
LR = 'src/Formalism/LocalRingCardinality/'
GT = 'src/Formalism/LocalToGlobal/GlobalTheory/'

GJ_PATHS = {
 'INST':GB+'DefsInst.lean', 'EXTRA':LR+'DataExtra.lean',
 'FAM':SH+'ParConsts.lean', 'GLOBAL':GB+'PlaneCountTheoremWithConstants.lean',
 'SCALE':LR+'DataParams₂.lean', 'SIZE':SH+'ElevenLe.lean',
 'DATA':GB+'IsResidueClassZero.lean', 'JOINT':GB+'Joints.lean',
 'SLOPE':GB+'LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean',
 'SMALL':GB+'SmallOrderPrimes.lean', 'OUT':GB+'CornerGLContinuity.lean',
 'TIES':LR+'DataGatTies.lean', 'CORE':SH+'FamCore.lean',
}

def claim(id, title, dependencies, statement, src):
    return dict(id=id,title=title,dependencies=dependencies,statement=statement,src=src)

GJ = [
claim('GJ1','The universal canonical Type-I infimum is attained',[],
 'Finite integer rank proves attainment with every ring/weight/target quantifier intact; the actual FamP Extra.kapI_def supplies that infimum and hence adm7.',
 {'INST':['kapISet','one_mem_kapISet','KapIDef','KapIDef.le','KapIDef.mem_Icc','sInf_mem_kapISet','KapIDef.mem','exists_inst_defs','EpDef'],
  'EXTRA':['Extra'],'FAM':['FamP'],'GLOBAL':['KapIDefF','kapIDefF'], 'SMALL':['adm7']}),
claim('GJ2','Uniform logarithmic and power estimates for the actual scale',['GII2'],
 'One explicit log-cube threshold yields x^(eps-eta)<=Lambda<=x^(eps+eta) and both actual log Q bounds, with A=26 and Y=x^13, uniformly in all family indices.',
 {'SCALE':['Scale','L','b','a',"X'","b'",'A','p0','delta1'],
  'SIZE':['SizeK','SizesAt'],'DATA':['Consts','N1','Gp','La','Qp'],'SMALL':['adm5'],
  'GLOBAL':['log_cube_le','sizes_bound_of_log_estimates','family_sizes_bound']}),
claim('GJ3','Exact cyclic orbit and actual representation identification',[],
 'The selector identities give the cyclic injection, Nv=|topsPos|, disjoint-fibre sum Nv<=|TT|, and the LatTied/GatTies identification of period, extremes and middle-weight bound.',
 {'DATA':['Inst','stepP','nP','reps','topsOn','Nv','topsPos','wPos','LatTied'],
  'JOINT':['not_split_of_class_zero','period_eq_addOrderOf_class_zero','shift_eq_generator_class_zero','bs_add_nsmul','bs_bs','Nv_eq_card','LPprime_cast'],
  'SLOPE':['phi','phi_inj','bs_iter','bs_idem','bs_rep','topsOn_eq_image','Nv_eq','sum_Nv_le'], 'TIES':['GatTies']}),
claim('GJ4','The literal finite-place OrbitLatticeBounds implication',['GJ1','GJ3','GI5','GII7','GII8','BC7','BC8'],
 'The two prime ranges, actual weight casts and compatible coefficient extension give the exact ceiling height, Dp, kapv and conductor 8(Dp+1); StdSubAt and actual family identifications remain explicit.',
 {'JOINT':['StdSubAt','HypIAt','HypIIAt','inBand_of_inBand0','linear_programming_input_of_hypotheses','LPprime_cast'],
  'DATA':['DIIf','DIf','tIIf','kapIIf','tIf','kapLoc','Dp','tv','kapv','Cand','goodReps','VV','LatTied'],
  'SMALL':['adm6','adm7'], 'OUT':['OrbitLatticeBounds']}),
claim('GJ5','Uniform family consequence with the actual construction boundary',['GJ4','GI8','GII3','GII7','GII8'],
 'Taking a finite maximum of thresholds yields the orbit implication uniformly after fixed coefficient choices; simultaneous construction of the full family, its chosen tops and covered degrees remains separate.',
 {'FAM':['FamP'],'CORE':['FamCore','FamCore.CoverAll'],'GLOBAL':['Ev','Ev.and','Ev.x1'],'OUT':['FamilyWindowLogBound'],'SMALL':['adm6','adm7','adm8']})
]

GW_PATHS = {
 'DATA':GB+'IsResidueClassZero.lean','SIZE':SH+'ElevenLe.lean',
 'SCALE':LR+'DataParams₂.lean','SMALL':GB+'SmallOrderPrimes.lean',
 'SLOPE':GB+'LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean',
 'MEAN':GB+'LogarithmicSums/MeanNum.lean',
 'EXCESS':GB+'LogarithmicSums/Conclusion1OfGainBoundAll.lean',
 'INST':GB+'DefsInst.lean','CORE':SH+'FamCore.lean','FAM':SH+'ParConsts.lean',
 'CHOICE':SH+'GlobalSchurBounds/WeightVectorSmallSharesSeven.lean',
 'VECTOR':SH+'GlobalSchurBounds/TopDensityNGeSixteen.lean',
 'TRANSPORT':GT+'PowFourLtCeilThresholdPrime.lean',
 'SAME':SH+'AdmissibleParameterJoins/GandSaa.lean',
 'RESULT':GT+'LossRequirementsOfSmallShares.lean',
 'SC':SH+'GlobalSchurBounds/QuadraticLogDerivCongr.lean',
}
GW = [
claim('GW1','Uniform small coefficients and nonempty exact degree boxes',['GJ2','GII2'],
 'The actual SizesAt and logarithmic bounds give the two x^-12 coefficient estimates and width>=1 in both integer degree windows, uniformly in the family index.',
 {'SIZE':['szTh','SizeN','SizeM','SizeK','SizeTT','SizesAt'],'SCALE':['Scale','a',"X'","b'",'A','delta1'],
  'DATA':['Nstar','La','winA','winB','box','boxLoc'],'SLOPE':['NumMean','Icc_ceil_floor_nonempty','winA_nonempty','winB_nonempty','box_nonempty','boxLoc_nonempty'],
  'MEAN':['ev_log','ev_pow','numMean_ev']}),
claim('GW2','The actual MeanKappaBound at every candidate good orbit',['GW1','GI5','GI8','GJ1','GJ3'],
 'Small primes have a pointwise deficit <=Nv*x^-12; large primes have the same local mean bound from the canonical Type-I deficit. Nonnegativity holds for all degrees.',
 {'DATA':['kapIIf','kapLoc','kapv','Cand','goodReps','meanLoc','MeanKappaBound'],'SMALL':['Conclusion2','adm8'],
  'INST':['KapIDef.mem_Icc'],'SLOPE':['RestHypI','inBand_of_inBand0','meanLoc_const_le','kapIIf_nonneg','kappa_nonneg_and_mean_bound','slopeEstimate_of_lemmaB_slopeLine','kapv_nonneg','Sig_nonneg']}),
claim('GW3','Exact global marginal averages and the total orbit deficit',['GW2','GJ3'],
 'Constant-size restriction fibres identify each local average with one common global product average; disjoint orbit fibres give E Sigma_p<=m_ch*|TT|*x^-12 without independence across primes.',
 {'DATA':['box','boxLoc','meanW','meanLoc','Sig'],'SLOPE':['margC','marg_fibre','marg_sum','marg_card','phi','phi_inj','box_marg','sum_box_product_eq_mean','sum_kapv_le','sum_Nv_le','sum_Sig_le']}),
claim('GW4','A uniform weighted exceptional-prime budget',['GW1','GW3'],
 'The elementary harmonic bound t(1+t) and pointwise indicator bound yield E Z<=8*x^(-9-gamma), gamma=1/2-(1453/150)eps>2447/7800.',
 {'EXCESS':['candF','ZZ'],'SLOPE':['mem_candF','sum_cand_le','markov_ind','ZZ_le','meanEx_of'],
  'SIZE':['SizeN','SizeM','SizeTT'],'DATA':['Cand','Sig']}),
claim('GW5','One global degree pair satisfies exact WReq',['GW4'],
 'For 32*x^-gamma<=1 finite averaging selects one pair with Z<=x^-9/4 and exact WReq coefficients 2 and 4, proving MeanEx and WeightVectorExists.',
 {'EXCESS':['MeanEx','ZZ'],'SMALL':['cands','WReq','WeightVectorExists'],'SLOPE':['meanEx_of','weight_condition_of_mean_excess'],'DATA':['VV']}),
claim('GW6','ChosenW transport and realization under the separate CoverAll property',['GW5'],
 'The actual family equalities and exact bTop window identify candidates and every Sigma term, proving ChosenW for the selected pair; CoverAll additionally gives a carrier and ChosenWS. Coverage is not inferred from averaging.',
 {'CORE':['FamCore','FamCore.CoverAll','FamCore.coverS_carry'],'FAM':['FamP'],
  'CHOICE':['ChW_at','ChosenW','ChosenWS','chosenWS_of_cover'],
  'VECTOR':['winAz','winBz','Wt','avOf','bvOf','admissible_weight_of_vector','wt_nonempty','exists_carrier'],
  'TRANSPORT':['pg_sameMore','pg_cls','pg_TT','pg_more','sAt_eq','pg_mem_TTn','pg_aL','Sig_eq','pg_LaG'],
  'SC':['sc_eq'],'SAME':['SameServed','sameServed'], 'RESULT':['chosenW_of','small_share_weight_exists'],
  'DATA':['aL','bL','ParametersFill','kapIIf','kapLoc','Sig']})
]

FOOTER = '''
CLAIMS=[]
for d in DEFS:
    c={k:v for k,v in d.items() if k!='src'}
    c['status']='proved_by_explicit_mathematical_reconstruction_with_stated_family_existence_boundary'
    c['sources']=[locator(key,name) for key,names in d['src'].items() for name in names]
    CLAIMS.append(c)
artifacts=[]
for name in ['main.tex','report.txt','build_provenance.py']:
    raw=(HERE/name).read_bytes()
    artifacts.append({'path':name,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
ids={c['id'] for c in CLAIMS}
payload={'artifact_version':'0.11','component':COMPONENT,'repository':BASE_URL,'commit':COMMIT,
 'head_verified':actual_head,'line_range_convention':'inclusive, one-indexed, original bytes including line endings',
 'claims':CLAIMS,'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in FILES.values()],
 'artifacts':artifacts,'explicit_external_dependencies':sorted({d for c in CLAIMS for d in c['dependencies']} - ids),
 'scope_note':SCOPE}
(HERE/'provenance.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\\n')
lines=[COMPONENT+' source ledger at '+COMMIT,'']
for c in CLAIMS:
    lines += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['dependencies'])]
    for x in c['sources']:
        lines += [x['declaration']+' | '+x['path']+':'+str(x['line_start'])+'-'+str(x['line_end']),
                  x['pinned_url'],'file '+x['full_file_sha256']+' ; range '+x['range_sha256']]
    lines.append('')
(HERE/'source_locators.txt').write_text('\\n'.join(lines)+'\\n')
print(json.dumps({'component':COMPONENT,'claims':len(CLAIMS),'files':len(FILES),'references':sum(len(c['sources']) for c in CLAIMS),'commit':COMMIT}))
'''

for component,paths,defs in [('family_join',GJ_PATHS,GJ),('global_weight_choice',GW_PATHS,GW)]:
    scope = ('Explicit supplied-family orbit application and uniform thresholds; actual simultaneous global arithmetic construction remains separate.'
      if component=='family_join' else
      'Exact local/global finite means and ChosenW are proved for supplied family data. A carrier additionally needs the separately defined CoverAll property; no full arithmetic family, RH/GRH proof or kernel replay is asserted.')
    header = '''"""Rebuild component provenance from the unchanged pinned Lean checkout."""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]/'alpoge-rh'
COMMIT='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE_URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
'''
    text=header+'PATHS='+repr(paths)+'\nCOMPONENT='+repr(component)+'\nSCOPE='+repr(scope)+'\n\n'+PARSER+'\nDEFS='+repr(defs)+'\n'+FOOTER
    (BASE/'v0_11'/component/'build_provenance.py').write_text(text)
    print(component)
