#!/usr/bin/env python3
"""Rebuild CAP metadata from the pinned Lean checkout and read-only v0.34.

Usage: python build_provenance.py --source /path/to/lean_source \
          --baseline /path/to/reconstruction_v034
Only files beside this builder are written; all stored paths are portable.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
parser.add_argument('--baseline', type=Path, default=HERE.parent.parent/'reconstruction_v034')
args = parser.parse_args()
REPO, BASELINE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip() == PIN
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P = B+'PatchingModules/'
CF = P+'ChebotarevFamilies/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
W = B+'WeilGroupCharacters/'
H = B+'HeckeAlgebras/'
AP = 'src/Development/AbelianVarietyTheory/PublishedTheorems/'
AE = 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/'
G = 'src/ReciprocityTheory/GaloisValuations/'

# Ranges are inclusive; zero as an end means through the end of the pinned blob.
SPECS = [
 ('A01',B+'CommutativeAlgebra/ResMapBijective.lean',[(334,338,'literal PhiCond: every open subgroup and every open-kernel additive F_ell character')]),
 ('A01',P+'ThetaCoefficientMapEq.lean',[(10,39,'HomL and every original TWGrp field, exact ph/tame orientation, one hb and all N')]),
 ('A02',P+'TaylorWilesObstructionBound.lean',[(23,31,'unchanged eight-field CohP hypothesis'),(33,71,'locOf r and globOf r V, with the same original local groups and Ju'),(88,111,'every original TWPl field including same H_eq, actual valuations and inverse Frobenius'),(119,124,'full ArPl, arbitrary n/q and PhiCond before every-list realization'),(126,154,'unchanged B1/B2/HasAut and original same-J PfromAut scope')]),
 ('A02',P+'PatchedSupportCompletions.lean',[(10,13,'actual IsCoef has finite residue field of characteristic ell and adic completeness')]),
 ('A03',G+'SeparatedDvrSecondCohomologyMem.lean',[(33,66,'actual ContAction, continuous one-cocycles, coboundaries and H1 quotient')]),
 ('A03',CF+'PhiGS.lean',[(7,45,'coset permutation module and representative/cocycle topology helpers'),(47,138,'finite H1 gives PhiCond for every open subgroup'),(142,160,'actual GS application of GlobalFiniteness with exponent one')]),
 ('A03',CF+'PhiDec.lean',[(19,69,'local finite-H1-to-PhiCond argument'),(70,79,'actual decomposition-group application of LocalFiniteness')]),
 ('A04','src/ReciprocityTheory/Hypotheses/GalCoh.lean',[(13,20,'LocalFinitenessAt exact finite-module, place, exponent and continuous-action hypotheses'),(151,155,'GlobalFinitenessAt includes ContainsAbove and finite H1'),(195,199,'universal LocalFiniteness'),(219,224,'universal GlobalFiniteness')]),
 ('A04',W+'ContinuousResP.lean',[(63,92,'original CM field, algebraic closure over Lplus, HidaSetting and chosen valuations'),(100,117,'original S and Lev, including hEta and full cyclotomic hEpsilon'),(129,162,'original pr and actual frame local groups/inertia/old D0')]),
 ('A05',W+'UniversalOrdinaryDeterminantRing.lean',[(10,42,'original compact GFrame, eta/c/epsilon and local groups'),(66,99,'Gprime is full cyclotomic kernel and original star/polarization law'),(109,117,'Residual characters, their open kernels and full polarized determinant')]),
 ('A05',CF+'StarSingle.lean',[(7,17,'source star on one group-algebra element and its subtraction'),(20,54,'residual determinant proof of conjugation stability'),(56,68,'residual cyclotomic one maps to residue-coefficient one'),(70,152,'exact hEx open normal subgroup and unshrunk H_eq')]),
 ('A06',P+'PairedDualFirstOrderDualMatrixSpace.lean',[(10,49,'fixed original Loc and Glob fields'),(76,106,'all Glob.Hom fields, p0/refl and exact PL intersection')]),
 ('A06',CF+'ProkerPL.lean',[(5,32,'continuous image of proKer lies in actual PL for any image subgroup')]),
 ('A06',CF+'HomBound.lean',[(5,39,'all-conjugates normal-core proof that characters kill PL and the closed generated kernel'),(41,80,'continuous character descends along restricted compact quotient'),(82,157,'full uniform Hom bound and source exponent q*[Gamma:H]')]),
 ('A07',CF+'FrSNormal.lean',[(7,36,'finite ell-group has nontrivial F_ell character'),(40,91,'normal/open Frattini subgroup and inclusion'),(93,135,'strict decrease of nontrivial finite ell-group image'),(137,178,'compactness gives relative power/cofinality property above PL'),(183,207,'literal frat: one normal tower and eventual containment for every open V above PL')]),
 ('A08','src/Formalism/ConjugateSelfDual/Statement.lean',[(20,29,'actual IsPlaceOver, normV, inertia and arithmetic power-map IsFrob')]),
 ('A08',G+'Global.lean',[(15,20,'actual Dec as valuation stabilizer'),(45,86,'actual inertia subgroup and its conjugation behavior'),(90,107,'cyclotomic character and finite reduction'),(128,150,'NS is the whole closed normal inertia subgroup, GS and quotient map'),(199,229,'exact arithmetic-Frobenius cyclotomic reduction'),(239,261,'ratio of same-place arithmetic Frobenius lies in inertia and inertia modifications'),(265,266,'actual valuation existence endpoint'),(340,347,'actual valuation conjugacy and arithmetic Frobenius existence'),(364,368,'exact full ell-adic Frobenius norm')]),
 ('A09',AP+'GaloisCohomology₂/ChebotarevDegreeOneIffCheb.lean',[(12,18,'exact degree-one finite Galois Frobenius predicate'),(51,68,'source dense Frobenius consequence outside an arbitrary finite set')]),
 ('A09',AE+'ChebotarevDegreeOne.lean',[(17,69,'pinned source degree-one theorem; CAP6 supplies a separate checked classical route')]),
 ('A09',CF+'ChebOne.lean',[(6,52,'degree-one place avoiding a-conjugate(a) gives exact CM split decomposition group'),(54,108,'original open-coset prime/valuation/arithmetic-Frobenius supplier')]),
 ('A09',CF+'ChebFam.lean',[(6,35,'finite-list supplier, injective base primes, finite avoidance and exact cosets')]),
 ('A10',CF+'LevUp.lean',[(5,24,'actual quotient level, NS inclusion, continuous surjection'),(25,53,'transport splitting to stored valuation, every Lev and Glob.Hom field')]),
 ('A10',CF+'PLNormal.lean',[(6,35,'valuation conjugacy, inertia compatibility under resP and old-level killing'),(37,60,'PL normality and ineKer image'),(62,101,'whole closed old ramification kernel generated modulo exact PL')]),
 ('A11',AP+'GaloisCohomology₂/ContinuousCycMod.lean',[(10,36,'exact proKer, ineKer and IsProGen'),(46,61,'continuous finite cyclotomic reduction'),(116,134,'unchanged CohP.tame.1 supplies generator and arithmetic Frobenius conjugation relation'),(155,155,'TameLocal is TameQuotient and TameSymbol')]),
 ('A12',P+'AutomorphicDetection/ArPl.lean',[(13,20,'literal theorem and PhiCond/exact-H/Frattini choices'),(21,50,'lift arbitrary prescribed Gprime list and define exact open cosets'),(51,87,'ell-away primes, original tame input, level maps and norm congruence'),(88,119,'inverse-Frobenius approximation and exact tame sign'),(120,148,'every TWGrp field and common hb'),(149,179,'actual TWPl identity comparison, inverse Frobenius, H_eq and unchanged list')]),
 ('A13',CF+'PFromAutOf.lean',[(30,49,'original six-input chain, same J, PhiCond before Choice then realization of its list'),(104,126,'Raw consumer and required h=0 NiceI P1core branch')]),
 ('A13',D+'HidaU.lean',[(12,16,'same-J HidaPropsAlt and HasAut contract')]),
 ('A13',D+'PointTheoremBaseObject.lean',[(26,48,'six Hida fields, P1/P3 and exact universal coefficient/data/iota scope')]),
 ('A13',D+'LinkTwo.lean',[(13,51,'both original Links with common kappa and distinct auxiliary primes at one threshold')]),
 ('A13',D+'PotentialModularityTower.lean',[(38,55,'actual PotentialModularityTower five fields'),(63,66,'PMExAlt has fixed iota before common coefficient threshold and every later Space')]),
 ('A14',AP+'AutomorphicForms₂/HasExponentZeroIff.lean',[(145,158,'every original IsLocalArtin field, especially smooth complex-character factorization')]),
 ('A14',H+'IsTheta.lean',[(19,20,'actual artOf choice'),(96,113,'arbitrary original QData and empty case'),(123,143,'exact hset, actual local Artin maps and Wp primes'),(156,168,'exact IsTheta and both IsRes fields, every Frobenius/valuation and every uniformizer preimage'),(212,226,'original HD fields, fixed residual values, same M and IsJ')]),
 ('A14',D+'TResEx.lean',[(16,42,'diagonal residual characteristic polynomial and exact Hecke coefficient normalization'),(44,64,'independence of valuation and every arithmetic Frobenius'),(65,87,'finite-character proof of independence of all Artin preimages'),(88,104,'open residual cyclotomic kernel'),(105,140,'original universal actual IsRes supplier and all-prime first field'),(141,165,'ordered uniformizer products and one same a with both IsRes fields')]),
 ('A15',H+'Distinct.lean',[(46,47,'literal heckePol signs, norm exponents, indices and leading coefficient')]),
 ('A15',H+'CoefficientRepTrivialOnUnramified.lean',[(146,165,'actual operator index sum, op shift, MK localization and full IsWt'),(259,268,'exact epsV and the separate full IsUniv Frobenius field')]),
 ('A16',D+'UnitaryHeckeData.lean',[(59,70,'actual R fields including type/theta/full IsWt/a/res and same original M/IsJ')]),
 ('A16',D+'HdEx.lean',[(20,27,'same original type, theta and residual values chosen in one R assembly')]),
 ('A16',D+'TThetaEx.lean',[(152,180,'full theta/IsWt still requires actual neatU; not supplied by CAP')]),
 ('A16',D+'TTypeEx.lean',[(18,22,'retained original integral type existence contract')]),
]

cache, groups, sources = {}, {}, []
for group,path,ranges in SPECS:
    b=(REPO/path).read_bytes()
    if path not in cache:
        assert b == subprocess.check_output(['git','show',PIN+':'+path],cwd=REPO), path
        cache[path]=b
    lines=b.splitlines(keepends=True)
    for start,end,decl in ranges:
        end=end or len(lines)
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        rb=b''.join(lines[start-1:end])
        sid=f'{group}-{len(groups.get(group,[]))+1}'
        sources.append({'id':sid,'group':group,'path':path,'declaration':decl,
            'line_start':start,'line_end':end,'sha256':sha(b),'full_file_sha256':sha(b),
            'range_sha256':sha(rb),'range_bytes':len(rb),'verified_equal_to_pinned_git_blob':True,
            'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'})
        groups.setdefault(group,[]).append(sid)

titles={
 'CAP1':'Finite continuous H1 gives PhiCond for every open subgroup by an explicit induced cocycle',
 'CAP2':'Original global and local PhiCond from the unchanged CohP finiteness clauses',
 'CAP3':'Exact residual H is open normal using full determinant polarization without factorial division',
 'CAP4':'All continuous characters kill the actual PL and local proKer images lie in PL',
 'CAP5':'Normal Frattini tower is cofinal above the exact relative PL subgroup',
 'CAP6':'Checked Chebotarev coset matching with degree-one arithmetic Frobenius and actual valuations',
 'CAP7':'Split CM finite prime family with injective base primes and original stored-valuation splitting',
 'CAP8':'Actual level enlargement, original local datum and every Glob.Hom field',
 'CAP9':'Whole closed level kernel generated by the original tame elements modulo exact PL',
 'CAP10':'Uniform all-level Hom bound by evaluation on conjugate inertia generators',
 'CAP11':'Simultaneous congruence and inverse-Frobenius approximation with the exact tame relation',
 'CAP12':'Complete original TWGrp with one hb for all N and the full ph_lim quantifier',
 'CAP13':'Actual TWPl and the full original universal ArPl contract conditional on unchanged CohP',
 'CAP14':'Same-J CountII frontier after ArPl, retaining both Links and one threshold after fixed iota',
 'CAP15':'Finite local characters factor through every exact Artin fiber, including residual epsilon',
 'CAP16':'Exact normalized residual Hecke coefficients independent of every valuation/Frobenius choice',
 'CAP17':'One original residual-value function with all IsRes fields at every actual QData level',
}
claim_groups={
 'CAP1':['A01','A03'],
 'CAP2':['A01','A02','A03','A04','A08'],
 'CAP3':['A02','A05'],
 'CAP4':['A06','A11'],
 'CAP5':['A01','A06','A07'],
 'CAP6':['A08','A09'],
 'CAP7':['A04','A08','A09'],
 'CAP8':['A02','A04','A06','A08','A10'],
 'CAP9':['A02','A06','A08','A10','A11'],
 'CAP10':['A01','A06'],
 'CAP11':['A02','A04','A05','A08','A09','A10','A11','A12'],
 'CAP12':['A01','A02','A06','A12'],
 'CAP13':['A01','A02','A04','A12'],
 'CAP14':['A02','A13'],
 'CAP15':['A04','A05','A08','A14','A15'],
 'CAP16':['A04','A05','A08','A14','A15'],
 'CAP17':['A04','A05','A14','A15','A16'],
}
dependencies={
 'CAP1':[],
 'CAP2':['CAP1'],
 'CAP3':[],
 'CAP4':[],
 'CAP5':['CAP2','CAP4'],
 'CAP6':[],
 'CAP7':['CAP6'],
 'CAP8':['CAP7'],
 'CAP9':['CAP4','CAP7','CAP8'],
 'CAP10':['CAP4'],
 'CAP11':['CAP3','CAP5','CAP7','CAP8','CAP9'],
 'CAP12':['CAP2','CAP3','CAP5','CAP8','CAP9','CAP10','CAP11'],
 'CAP13':['CAP2','CAP3','CAP11','CAP12'],
 'CAP14':['CAP13','CIP10','CIP11','CIP12','JSP1','JSP11','JSP12','QX4','QX10','YX2','KA5','KA6'],
 'CAP15':['CIP4'],
 'CAP16':['CAP6'],
 'CAP17':['CIP4','CAP15','CAP16'],
}
original_hypotheses={
 'CAP1':['Profinite group; finite continuous H1 for every finite discrete F_ell representation'],
 'CAP2':['Unchanged original CohP; actual HidaSetting, original level and original recorded decomposition groups'],
 'CAP3':['Original GFrame and Resid; residue field characteristic ell; full residual determinant polarization'],
 'CAP4':['Profinite ambient group; K open normal for the character claim; continuous map with image in K for proKer claim'],
 'CAP5':['Original open normal H and PhiCond; open normal V contains literal PL(ell,H)'],
 'CAP6':['Number field E and its specified algebraic closure; open U; prescribed g; finite forbidden set'],
 'CAP7':['Original CM L/Lplus; open subgroup; arbitrary finite list and forbidden base primes'],
 'CAP8':['Original s,V0,r; a finite new prime set split at supplied valuations over Lplus'],
 'CAP9':['Original level quotient, same H, new primes outside V0.Sprime and actual IsProGen elements'],
 'CAP10':['Continuous surjective profinite p, open normal H, same q tame elements, exact whole-kernel inclusion, finite HomL(H)'],
 'CAP11':['Unchanged CohP; original V0.Sprime=s.S; arbitrary q and every list in full Gprime, not just its residual kernel'],
 'CAP12':['Same original q,H,r and all level data of CAP11; same original locOf(r)'],
 'CAP13':['Every original ArPl input including arbitrary n; unchanged CohP, IsCoef and V0.Sprime=s.S'],
 'CAP14':['Remaining original producers with exact same witnesses, fixed-iota common-threshold order and all inherited side conditions'],
 'CAP15':['Any source IsLocalArtin, abelian character with open kernel on the actual decomposition group; CIP4 for actual artOf'],
 'CAP16':['Original HSet Wp primes and Resid on actual arbitrary level V; original coefficient c.O'],
 'CAP17':['Original s; arbitrary V,QData,c,m,supplied tau0,r; n>=1; no V.Sprime=s.S restriction'],
}
classical_inputs={'CAP6':['CAP_CHEBOTAREV']}
tex=(HERE/'main.tex').read_bytes()
texlines=tex.splitlines(keepends=True)
claims=[]
for cid,title in titles.items():
    start=next(i for i,l in enumerate(texlines) if l.strip()==f'% BEGIN {cid}'.encode())
    end=next(i for i,l in enumerate(texlines) if l.strip()==f'% END {cid}'.encode())
    rb=b''.join(texlines[start:end+1])
    assert f'\\label{{claim:{cid}}}'.encode() in rb
    claims.append({'id':cid,'title':title,'introduced_in':'0.35','classification':'B',
        'status':'complete human proof at the printed original-data scope; CAP14 is the exact conditional frontier reduction',
        'depends_on':dependencies[cid],'classical_inputs':classical_inputs.get(cid,[]),
        'dependency_scope':{
          'CAP8':'Uses only the valuation-transitivity/splitting-transport conclusion of CAP7; the new split primes are hypotheses of CAP8.',
          'CAP9':'Uses only valuation transitivity from CAP7; the actual supplied prime system and tame generators are hypotheses.',
          'CAP16':'Reuses only the elementary finite-valuation and compact-limit proof within CAP6, which gives transitivity and Frobenius existence at each fixed prime; the Chebotarev import and prescribed-coset selection are not needed for IsRes.'
        }.get(cid,'All listed proof inputs at their stated scope.'),
        'original_hypotheses':original_hypotheses[cid],
        'remaining_inputs':[] if cid!='CAP14' else ['the seven retained JSP producer entries, including unchanged CohP and other original side conditions'],
        'proof_location':{'file':'count_auxiliary_primes/main.tex','label':'claim:'+cid,
            'line_start':start+1,'line_end':end+1,'sha256':sha(rb),'bytes':len(rb)},
        'source_groups':claim_groups[cid],
        'sources':[s for s in sources if s['group'] in claim_groups[cid]]})

def inherited_block(b,cid):
    lines=b.splitlines(keepends=True)
    starts=[i for i,l in enumerate(lines) if l.strip()==f'% BEGIN {cid}'.encode()]
    if starts:
        start=starts[0]
        end=next(i for i,l in enumerate(lines) if l.strip()==f'% END {cid}'.encode())
    else:
        label=next(i for i,l in enumerate(lines) if f'\\label{{claim:{cid}}}'.encode() in l)
        start=max(i for i in range(label+1) if b'\\paragraph{' in lines[i])
        end=next((i-1 for i in range(label+1,len(lines)) if b'\\paragraph{' in lines[i]),len(lines)-1)
    return {'id':cid,'line_start':start+1,'line_end':end+1,'sha256':sha(b''.join(lines[start:end+1]))}

inherited=[]
for path,ids,role in [
 ('count_ii_producer/main.tex',['CIP4','CIP10','CIP11','CIP12'],'Actual artOf and every-map matching; universal required NiceI Norm and exact residual CountII frontier'),
 ('joint_support/main.tex',['JSP1','JSP11','JSP12'],'Original same-J kernel construction, conditional h=0 P1core implication and two-Link assembly'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],'Both original rank-four Links and exact joint support to PMEx'),
 ('case_two_installation/main.tex',['YX2'],'Exact PMExAlt-to-CountII implication'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],'Only CaseIII vacuity for two-primary target; no vacuity of I/II/V'),
]:
    b=(BASELINE/path).read_bytes()
    inherited.append({'path':'reconstruction_v034/'+path,'sha256':sha(b),'claim_ids':ids,
        'claim_proof_blocks':[inherited_block(b,cid) for cid in ids],'role':role})

published=[{
 'id':'CAP_CHEBOTAREV','classification':'A','status':'primary statement, scope and arithmetic Frobenius convention checked',
 'reference':'J. S. Milne, Algebraic Number Theory, version 3.08 (19 July 2020), Theorem 8.31, printed p.147; arithmetic Frobenius convention preceding 8.14, printed p.141',
 'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
 'statement_used':'Every conjugacy class in a finite Galois extension of number fields occurs as the unramified arithmetic Frobenius class at a positive density of base primes.',
 'hypotheses_checked':[
   'Choose open normal U0 inside the original open U; its fixed field F/E is finite Galois.',
   'Take Eprime/Q finite Galois inside the same Omega, containing F and E; the actual prescribed g restricts to h in Gal(Eprime/E).',
   'Apply the theorem over the number field Q to the conjugacy class of h; all ramified primes and the rational primes below the finite forbidden set are excluded.',
   'Conjugation of the chosen prime makes its Frobenius exactly h. No effectiveness, GRH, class field theory or asymptotic prime bound is used.'
 ],
 'derived_matching':[
   'CAP6 proves degree-one absolute norm because h fixes E, so every residue element satisfies x^p=x.',
   'CAP6 writes the elementary finite valuation/transitivity/Frobenius and compact inverse-limit matching into the original algebraic closure.',
   'CAP7 proves actual CM splitting and realizes an arbitrary finite list with injective base primes.',
   'CAP11 selects the inverse target coset and explicitly proves the inverse-Frobenius approximation and tame sign.'
 ],
 'does_not_supply':['CohP','ordinary automorphic modules','Choice detector or eigenvalues','B1/B2 cohomological bounds','same-J HasAut'],
 'checked_on':'2026-11-22',
}]
(HERE/'published_applications.json').write_text(json.dumps(published,indent=2,ensure_ascii=False)+'\n')

old=json.loads((BASELINE/'count_ii_producer/closure.json').read_text())
remaining=[x for x in old['remaining'] if x['id']!='JSP_ACTUAL_ARPL']
assert len(remaining)==7
closed=[
 {'id':'JSP_ACTUAL_ARPL','old_classification':'C','by':[f'CAP{i}' for i in range(1,14)],
  'scope':'Full original ArPl: unchanged CohP implies PhiCond for the actual original frame and, for every q and every list in its full Gprime, an actual all-N TWGrp with nonempty TWPl and exactly that length/list; includes all original fields and uniform hb. n=0, q=0, N=0 allowed.'},
 {'id':'CAP_ACTUAL_ISRES','kind':'proved_original_subcontract','was_selected_leaf':False,
  'refines':'JSP_ORIGINAL_ORDINARY_DATA','by':['CIP4','CAP15','CAP16','CAP17'],
  'scope':'For every original s,V,QData,c,m,supplied tau0,r with n>=1, one a on the original hset.Op with both full IsRes fields. Every valuation/Frobenius and every Artin uniformizer preimage is covered; no V.Sprime=s.S restriction or coefficient extension.'},
]
closure={
 'schema':'rh-human-component-closure/1','artifact_version':'0.35','component':'count_auxiliary_primes',
 'source_commit':PIN,'proof_sha256':sha(tex),'proof_claims':list(titles),
 'closed':closed,'remaining':remaining,
 'classical_input_nodes':[
   {'id':p['id'],'kind':'published_application_certificate','classification':'A',
    'status':p['status'],'certificate_file':'published_applications.json',
    'certificate_file_sha256':sha((HERE/'published_applications.json').read_bytes()),
    'used_by':[cid for cid,ids in classical_inputs.items() if p['id'] in ids],
    'statement_used':p['statement_used'],'hypotheses_checked':p['hypotheses_checked'],'url':p['url']}
   for p in published],
 'selected_frontier_status':{
   'COUNT_II_SUPPORT':'OPEN C; original ordinary/control/fibers, four Hida endpoints, same-J HasAut and four support producers remain',
   'JSP_ACTUAL_ARPL':'CLOSED at full original conditional-on-CohP scope by CAP1-CAP13',
   'JSP_ORIGINAL_ORDINARY_DATA':'OPEN C; CAP15-CAP17 now supply actual residual a/IsRes for any supplied tau0, while type/theta/full IsWt and all ordinary/control/determinant/fiber producers remain',
   'COUNT_III_PRODUCER':'unchanged separate original Ctx3/SeedIV/rank-three dependencies for general targets',
   'RH_case_note':'KA5/KA6 remove only CaseIII for two-primary targets; I, II and V remain substantive'},
 'sufficient_rules':[
   {'conclusion':'JSP_ACTUAL_ARPL','requires':['CERT_CAP1_CAP13'],'logic':'AND','binding':'The conclusion is the full source predicate CohP -> all original arithmetic/coefficient/level/residual data -> PhiCond AND every-list realized all-N system.'},
   {'conclusion':'CAP_ACTUAL_ISRES','requires':['CERT_CIP4','CERT_CAP15_CAP17'],'logic':'AND','binding':'Same original Q,V,c,tau0,r and actual artOf; a selected once before R.M and its eventual J.'},
   {'conclusion':'SAME_J_P1CORE','requires':['JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_CHOICE','CERT_CAP1_CAP13','JSP_FIRST_ORDER_BOUND','JSP_OBSTRUCTION_BOUND','JSP_SINGLE_POINT_RAW','EXACT_COH_P_AND_SIDE_CONDITIONS','CERT_JSP9_JSP11','CERT_CIP6_CIP11'],'logic':'AND','binding':'Exact same original B,r,J; every required h=0 NiceI point, its detector and actual realized T/TWPl.'},
   {'conclusion':'COUNT_II_SUPPORT','requires':['BOTH_ORIGINAL_LINKS_WITH_COMMON_KAPPA_AND_DISTINCT_AUXILIARY_PRIMES','SAME_J_HIDAPROPSALT_AND_P1CORE_FOR_EACH_LINK','UNIFORM_COMMON_THRESHOLD_AFTER_FIXED_IOTA_BEFORE_COEFFICIENT_SPACE_AND_UNIVERSAL_DATA','CERT_JSP12','CERT_CIP12','CERT_CAP14'],'logic':'AND'}],
 'nonlogical_shared_links':[
   {'from':'CERT_CAP1_CAP13','to':'JSP_SINGLE_POINT_CHOICE','reason':'PhiCond is now supplied before Choice; no detector, Kap, eigensystem or coefficient extension is selected here.'},
   {'from':'CERT_CAP1_CAP13','to':'JSP_FIRST_ORDER_BOUND','reason':'Supplies its actual T/TWPl input only; no B1 estimate follows from the prime-system construction.'},
   {'from':'CERT_CAP1_CAP13','to':'JSP_OBSTRUCTION_BOUND','reason':'Supplies its actual T/TWPl input only; no B2 estimate follows.'},
   {'from':'CERT_CAP1_CAP13','to':'JSP_SAME_IDEAL_HASAUT','reason':'Produces arithmetic systems to which the already fixed ideal must admit automorphic modules; no module or ideal is supplied.'},
   {'from':'CAP_ACTUAL_ISRES','to':'JSP_ORIGINAL_ORDINARY_DATA','reason':'Closes literal a and res fields of original R after tau0; type, theta, full IsWt and actual ordinary/control/fiber data remain.'}],
 'not_claimed_closed':[
   'CohP itself','Choice','FirstOrderDualArithmeticBound','TaylorWilesObstructionBound','Raw',
   'TThetaEx/full IsWt or original neatU','original integral TypeForAlt producer',
   'original UnitaryHeckeData existence','ordinary/free/control modules and full IsUniv or separating fibers',
   'same-J HasAut','four additional Hida endpoints','COUNT_II_SUPPORT',
   'COUNT_I_PRODUCER','COUNT_V_PRODUCER','COUNT_III_PRODUCER'],
 'quantifier_guards':[
   'Retain full CohP; only gf, lf and tame.1 are used by the proof, but no field is removed from the original ArPl implication.',
   'PhiCond precedes the arbitrary finite list; the selected system has exactly that q and sg, not a replacement or sublist.',
   'The list lies in the FULL Gprime cyclotomic kernel; H is the exact residual kernel, not a normal core chosen in its place.',
   'The tower is cofinal above PL(ell,H), not implicitly above the identity; same H is used by every level.',
   'Every N, including zero, has original actual arithmetic level maps to V0 and one common hb = #HomL(H)*ell^(q*[Gamma:H]).',
   'Arithmetic Frobenius sigma is selected near g^-1; source ph/fr are its inverse, and tame is (ta^Nq)^-1*(ph^-1*ta*ph).',
   'No J is selected by ArPl. Existing J stays fixed before the point, detector, list, TWGrp/TWPl and all N.',
   'Both original rank-four Links remain, with common kappa, literal distinct-prime condition, and ell=3.',
   'Fix iota before a single coefficient threshold for both Links; the threshold precedes every later coefficient, Space and arbitrary original B,Lambda.',
   'CAP17 covers arbitrary original V and QData, every supplied tau0 and all allowed Frobenius/Artin preimages in the SAME c.O.',
   'The a of CAP17 is selected before the original R/module/ideal construction and is then held fixed; no transport between unrelated a choices or ideals is asserted.'
 ],
 'peer_review':'pending independent review, to be bound to whole-proof and proof-block hashes',
 'formal_correctness_assumed':True,
}
(HERE/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
prov={
 'schema':'rh-human-component-provenance/1','artifact_version':'0.35','date':'2026-11-22',
 'source_commit':PIN,'component':'count_auxiliary_primes','main_tex_sha256':sha(tex),
 'claims':claims,'source_groups':groups,'source_inventory':sources,'inherited_proof_inputs':inherited,
 'published_applications':{'file':'published_applications.json','sha256':sha((HERE/'published_applications.json').read_bytes()),'ids':[p['id'] for p in published]},
 'builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable':True,'read_only_inputs':['pinned Lean checkout','reconstruction_v034']},
 'validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),
   'claim_source_ranges':sum(len(c['sources']) for c in claims),'all_source_ranges_exact':True,
   'claim_proof_blocks':len(claims),'inherited_claim_proof_blocks':sum(len(x['claim_proof_blocks']) for x in inherited),
   'new_lean_build':False,'independent_human_mathematical_proof':True},
 'scope_note':'Formal correctness is assumed. ArPl is proved at its whole original conditional-on-CohP scope. The Chebotarev import is A; the written matching/induced-cocycle/group/level/normalization arguments are completed B proofs. CAP17 proves an original residual-Hecke subpacket without claiming the full ordinary producer.'
}
(HERE/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc=[f'CAP1-CAP17 exact source provenance; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc += [f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",
       f"file_sha256={s['sha256']}",f"range_sha256={s['range_sha256']}",s['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f'''CAP1-CAP17: original auxiliary primes and residual Hecke values, v0.35

Source pin: {PIN}
Proof SHA256: {sha(tex)}
Provenance SHA256: {sha((HERE/'provenance.json').read_bytes())}
Closure SHA256: {sha((HERE/'closure.json').read_bytes())}

THE FULL ORIGINAL ArPl ENDPOINT

CAP1-CAP13 supply the whole JSP_ACTUAL_ARPL producer, with the exact
original CohP hypothesis unchanged. Global/local H1 finiteness is used
only through that hypothesis. CAP1 writes an explicit induced cocycle
for EVERY open subgroup, proves continuity and injectivity into H1,
and CAP2 checks the actual global/local fields and exponent-one inputs.
CAP3 proves normality of the EXACT residual H from the original full
determinant polarization, without dividing by n or n!, hence at ell=3.
CAP4 uses the all-conjugates normal core correctly. CAP5 proves a normal
Frattini tower cofinal relative to the literal PL(ell,H), not the identity.

The only new published import is unconditional finite-Galois Chebotarev
(Milne ANT 3.08, Theorem 8.31, printed p.147). CAP6 checks all hypotheses
over a finite Galois extension Eprime/Q containing the required quotient
field, and derives absolute residue degree one from the chosen Frobenius
fixing E. Finite prime transitivity, Frobenius lifting and the compact
inverse-limit passage are written out. CAP7 proves CM splitting by
avoiding a-conjugate(a), then supplies any finite list with distinct
base primes. The classical application certificate is separate from
claim dependency IDs.

CAP8 constructs the actual enlarged Lev and every Glob.Hom field using
the SAME original locOf(r). CAP9 proves the WHOLE closed kernel bound,
including arbitrary valuations above new primes and exact ineKer->PL.
CAP10 proves finiteness and the uniform bound
  hb = #HomL(H) * ell^(q * [Gamma:H])
by evaluating characters on all coset conjugates of the inertia
generators. Equal evaluation arrays differ by a continuous character
of H. This bound works for every N without a new level-dependent choice.
CAP11 checks the exact inverse-Frobenius order and cyclotomic congruence,
then maps the retained tame relation with the correct conjugation sign.
CAP12 verifies every TWGrp field; CAP13 verifies every TWPl field and
returns the original q and sg definitionally unchanged. n=0, q=0 and
N=0 are included. No universal condition is replaced by a one-point or
eventual-only condition.

THE ACTUAL RESIDUAL HECKE-VALUE SUBPACKET

CAP15-CAP17 additionally prove the original TResEx conclusion for any
supplied integral representation tau0, arbitrary original level V and
QData Q, coefficient c and Resid r, with n>=1. CIP4 supplies validity
of actual artOf. CAP15 gives finite complex-character separation and
factorization through every Artin fiber, including residual epsilon.
CAP16 constructs the exact normalized Hecke-polynomial coefficients:
(-1)^j * q^(-j(j-1)/2) * coeff(P,n-j), then lifts them in the SAME c.O.
It proves independence from every valuation and every allowed arithmetic
Frobenius, with the original inverse-Frobenius input retained. CAP17
constructs the ordered i<=j uniformizer products with exponent i,
proves independence from ALL Artin preimages, and selects one a on the
original operator-index disjoint union carrying both IsRes fields.

This supplies literal R.a/R.res, but not the integral TypeForAlt input,
TThetaEx's character/full IsWt/neatU, H.Ax, ordinary/free/control modules,
continuous full IsUniv determinant or separating arithmetic fibers.
The chosen a is fixed before the future R/module/ideal assembly; no
comparison of different ideals from different a choices is asserted.

REMAINING EXACT FRONTIER

Seven inherited JSP producer entries remain: original ordinary data,
four further Hida endpoints, same-J all-level HasAut, Choice, first-order
B1, obstruction B2, and h=0 Raw. Their inherited contract text is retained
unchanged in closure.json; the closed residual-value subpacket is recorded
separately as a non-sufficient refinement of ordinary data. CohP itself
and all original LocCFT/coefficient/level/cyclotomic side conditions stay
required. COUNT_II_SUPPORT remains OPEN C.

ArPl has no J argument and selects no ideal, so it applies after the
original J has already been fixed. It first gives PhiCond for Choice,
then realizes exactly Choice's finite list. Both original rank-four Links,
common kappa and distinct auxiliary primes, ell=3, and fixed iota before
ONE common coefficient threshold for every later coefficient/Space and
arbitrary original B,Lambda remain intact. No external coefficient
enlargement or threshold is introduced. CountII still contributes to RH
and unrestricted Dirichlet GRH; only CaseIII is vacuous for two-primary
targets, and the separate general-target rank-three branch is unchanged.

Validation: {len(claims)} new proof blocks; {len(cache)} pinned source files;
{len(sources)} source ranges; {sum(len(c['sources']) for c in claims)} claim-source
references; {sum(len(x['claim_proof_blocks']) for x in inherited)} inherited proof
blocks. Every source file equals its pinned git blob and every proof/source
range is SHA256-bound by the portable builder. No Lean validity audit or
new Lean build is performed. Independent mathematical review is pending.

Primary reference: https://www.jmilne.org/math/CourseNotes/ANT.pdf
'''
(HERE/'report.txt').write_text(report)
print(json.dumps({'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'closure_sha256':sha((HERE/'closure.json').read_bytes()),'claims':len(claims),'files':len(cache),
 'source_ranges':len(sources),'claim_source_ranges':sum(len(c['sources']) for c in claims)},indent=2))
