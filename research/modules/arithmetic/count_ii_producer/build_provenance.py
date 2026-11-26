#!/usr/bin/env python3
"""Rebuild the CIP source/proof audit using only the pinned checkout and v0.33.

Usage: python build_provenance.py --source /path/to/lean_source \
         --baseline /path/to/reconstruction_v033
No baseline file is modified.  All paths written to metadata are portable.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
parser.add_argument('--baseline', type=Path, default=HERE.parent.parent/'reconstruction_v033')
args = parser.parse_args()
REPO, BASELINE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip() == PIN
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
W = B+'WeilGroupCharacters/'
H = B+'HeckeAlgebras/'
P = B+'PatchingModules/'
PD = P+'DeterminantPadicFree/'
AP = 'src/Development/AbelianVarietyTheory/PublishedTheorems/'
AD = 'src/Development/AbelianVarietyTheory/Definitions/'
AE = 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/'

# An ending line of zero binds through the end of the actual pinned blob.
SPECS = [
 ('C01',AP+'AutomorphicForms₂/ExistsUniqueHcharOfFiniteOrder.lean',[(15,39,'Gab, toAb, infConn and all five original IsGlobalArtin fields'),(70,72,'GlobalArtinReciprocity existence contract')]),
 ('C02',AE+'GlobalArtinReciprocityMapUnique.lean',[(26,82,'eq_one_of_unit_unif and unif_eq: finite-quotient local uniqueness'),(83,122,'eq_infPart and eq_one_of_local'),(137,0,'globalArtin_unique: generic source predicate uniqueness; independent CM proof in CIP2')]),
 ('C03',W+'ContinuousResP.lean',[(48,59,'Emb, every-IsLocalArtin IsWtPart, and IsLocAlg'),(63,92,'original CM field, maximal real subfield, chosen valuations and HidaSetting.split'),(104,117,'actual Vl, Lev and exact cyclotomic hε'),(140,164,'original Lev.frame and its local groups/inertia')]),
 ('C04',AP+'AutomorphicForms₂/HasExponentZeroIff.lean',[(145,158,'complete IsLocalArtin and its smooth-character consequence')]),
 ('C04',AD+'AutomorphicMembership/ExistsNotCongPow.lean',[(149,169,'actual Weil subgroup, original inertia inclusion and degree'),(218,245,'degree-zero inertia, degree-one arithmetic Frobenius, and decomposition')]),
 ('C04',AD+'AutomorphicMembership/MonodromyZeroOfWeilDeligneRepClassIff.lean',[(13,20,'literal IsSmooth is open kernel on inertia')]),
 ('C04',AD+'TwistedInnerProducts/IsUnitarisableOfCharIff.lean',[(165,177,'IsSmoothChar is open character kernel')]),
 ('C04',AD+'TwistedInnerProducts/IsSubquotientDetRepParInd.lean',[(90,120,'normalized local ord and value one on a uniformizer')]),
 ('C05',H+'IsTheta.lean',[(19,20,'actual artOf Hilbert choice'),(123,143,'actual hset uses artOf and admitted=univ'),(156,168,'actual IsTheta and residual Frobenius/unit/uniformizer normalization')]),
 ('C06',D+'TWtBridge.lean',[(27,43,'generic artin_unique and actual inertia-unit surjectivity'),(58,99,'finite-part dictionary with every-map quantifier'),(168,239,'literal arithmetic/good weight bridge and positive cyclotomic norm factor')]),
 ('C06',B+'PadicHodgeTheory/LaCyc.lean',[(11,32,'laCyc: every admissible map gives weight -1 and positive embedding product')]),
 ('C06',H+'CoefficientRepTrivialOnUnramified.lean',[(122,144,'HSet.Ax includes original Artin validity'),(259,284,'epsV, IsUniv and Out on the same original Hecke algebra')]),
 ('C07',W+'UniversalOrdinaryDeterminantRing.lean',[(10,46,'GFrame and exact HasFlag conjugation convention'),(56,80,'pushCh, pushRep, Gprime, mu and eps'),(101,103,'original IsForm with exponent 1-n'),(189,208,'original Point: finite field, integral invertible symmetric P, ordered rational flags'),(218,251,'fraction fields, N1, TypeI, N3, original D0 N4, NiceI/NiceE'),(259,259,'original IsPt'),(284,286,'full original P1core point/prime quantifiers')]),
 ('C08',PD+'ResSqField.lean',[(5,23,'constant coefficient extension is finite as a power-series-ring map'),(25,67,'finite residue extension, injective local map and square roots in residue field')]),
 ('C08',PD+'ZlUniq.lean',[(5,0,'uniqueness of the Z_ell map in characteristic ell')]),
 ('C08',PD+'ClosedOfComb.lean',[(5,22,'finite-field characteristic of any Z_ell ring map'),(24,75,'closedness of rational linear combinations of adic-continuous entries'),(77,116,'psiMu: closed commutator kernel and characteristic-ell torsion')]),
 ('C09',B+'UnitaryThreeGroups/BaseRepGL3NormalisedOfPsiEqOne.lean',[(15,16,'MatIrr is literal invariant-subspace irreducibility')]),
 ('C09',B+'AlgebraTools/IrredIffSpan.lean',[(18,27,'source irreducibility/full-matrix-span and scalar-extension dictionary')]),
 ('C09',PD+'SpanInt.lean',[(12,38,'source integral denominator clearing for Ev span')]),
 ('C10',P+'PairedDualFirstOrderDualMatrixSpace.lean',[(192,201,'blkMat and Ev; Ev(n,n) is all matrices'),(251,275,'every NP field including integral flags, mu, full-block span and N1'),(282,294,'NP coefficient ring, normalized N3 and subgroup-parametrized N4')]),
 ('C10',PD+'FlagBasis.lean',[(38,82,'source integral flag basis and exact w inverse convention')]),
 ('C11',W+'RepAlg.lean',[(9,26,'determinant polynomial-law naturality and full coefficient-algebra scope')]),
 ('C11',PD+'SolBase.lean',[(5,26,'original twisted-commutant vanishing survives field extension')]),
 ('C11',PD+'CoefficientExtensionPreservesConditionsAndDet.lean',[(31,108,'subsequent normalized coefficient extension, original N4 and determinant/character preservation')]),
 ('C12',P+'AutomorphicDetection/ConjugationDescendsToSubring.lean',[(198,222,'twisted commutant descends through conjugation and integral inclusion'),(224,259,'general source Norm, eps convention and same characters'),(260,299,'source flag, continuity, form and tame-inertia fields'),(300,323,'source normalized record, full determinant, N3 and old D0 N4')]),
 ('C13',P+'TaylorWilesObstructionBound.lean',[(13,21,'reIu and exact Norm conclusion, with original F.D0'),(23,31,'exact CohP side-condition package'),(37,86,'locOf, globOf, residOf and pairOf'),(115,124,'original LocCFT and ArPl contracts'),(126,143,'exact first-order B1 and obstruction B2 inputs'),(147,154,'same-J HasAut and full PfromAut contract')]),
 ('C13',P+'ChebotarevFamilies/IpEq.lean',[(4,18,'literal original tame-inertia identities for Norm consumer')]),
 ('C14',P+'ChebotarevFamilies/PFromAutOf.lean',[(30,49,'Norm and Choice actual input order, exact same-J HasAut'),(50,103,'constant-field map, pair identities and unchanged point kernels'),(104,114,'Raw and stable discriminant consumer'),(116,126,'h=0 branch calls Norm only at NiceI')]),
 ('C15',D+'HidaU.lean',[(12,16,'same ideal HidaPropsAlt and HasAut original producer contract')]),
 ('C15',D+'PointTheoremBaseObject.lean',[(26,41,'six HidaPropsAlt fields, P1core and separate P3core'),(44,48,'literal universal coefficient/data/iota quantifiers')]),
 ('C15',D+'THidaU.lean',[(38,48,'actual single R, single J, six Hida fields and all-level HasAut assembly')]),
 ('C15',D+'UnitaryHeckeData.lean',[(59,70,'original UnitaryHeckeData, same module and IsJ')]),
 ('C15',D+'HdEx.lean',[(20,27,'retained original R from integral type, theta and residual Hecke eigenvalues')]),
 ('C15',H+'IsTheta.lean',[(40,52,'exact IsMap/IsJ includes zero-module branch and same kernel')]),
 ('C16',D+'LinkTwo.lean',[(13,51,'both original Links, common kappa and distinct auxiliary primes at one threshold')]),
 ('C16',D+'PotentialModularityTower.lean',[(38,55,'original five fields of PotentialModularityTower'),(63,66,'PMExAlt: fixed iota before common coefficient threshold and later Spaces')]),
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
 'CIP1':'Source-compatible inverse global Artin map with every IsGlobalArtin field checked',
 'CIP2':'Uniqueness of every literal global Artin map in the required CM scope',
 'CIP3':'Local-unit kernel injectivity at the actual split CM places',
 'CIP4':'Validity of actual artOf and equality with every admissible local map',
 'CIP5':'Positive cyclotomic norm identity and complete JSP7 reciprocity matching',
 'CIP6':'Finite constant-field extension and integral Gram-Schmidt normalization',
 'CIP7':'Independent matrix-density proof and integral full-block span',
 'CIP8':'Exact ordered integral flags, original mu-torsion and N1',
 'CIP9':'Full determinant polynomial law, normalized N3 and original-D0 N4',
 'CIP10':'Complete universal NiceI restriction of the original Norm contract',
 'CIP11':'Actual h=0 consumer, constant-field compatibility and unchanged point kernel/J',
 'CIP12':'Reduced joint-support frontier with both original rank-four Links and all quantifier guards',
}
claim_groups={
 'CIP1':['C01','C03','C04'],
 'CIP2':['C01','C02'],
 'CIP3':['C01','C03','C06'],
 'CIP4':['C01','C03','C04','C05','C06'],
 'CIP5':['C03','C04','C05','C06'],
 'CIP6':['C07','C08','C12'],
 'CIP7':['C07','C09','C10'],
 'CIP8':['C07','C08','C10','C12'],
 'CIP9':['C07','C10','C11','C12'],
 'CIP10':['C07','C08','C10','C12','C13'],
 'CIP11':['C07','C11','C13','C14'],
 'CIP12':['C05','C06','C07','C13','C14','C15','C16'],
}
dependencies={
 'CIP1':['KX3'],
 'CIP2':['CIP1'],
 'CIP3':['CIP1','KX3'],
 'CIP4':['CIP1','CIP2','CIP3','KX3'],
 'CIP5':['CIP1','CIP4','JSP7'],
 'CIP6':[],
 'CIP7':['CIP6'],
 'CIP8':['CIP6','CIP7'],
 'CIP9':['CIP6','CIP7'],
 'CIP10':['CIP6','CIP7','CIP8','CIP9'],
 'CIP11':['CIP10','JSP10','JSP11'],
 'CIP12':['CIP5','CIP11','JSP5','JSP6','JSP7','JSP8','JSP11','JSP12','QX4','QX10','YX2','KA5','KA6'],
}
classical_inputs={
 'CIP1':['CIP_CFT_GLOBAL'],
 'CIP4':['CIP_CFT_LOCAL_WEIL'],
 'CIP5':['CIP_CFT_NORM'],
}
original_hypotheses={
 'CIP1':['E a number field; Omega its specified algebraic closure; original adelic and local groups'],
 'CIP2':['E a CM number field; two maps each satisfying every source IsGlobalArtin field'],
 'CIP3':['E CM; w distinct from its conjugate; a local unit; exact global Artin kernel'],
 'CIP4':['actual HidaSetting, chosen place/valuation and original v|ell'],
 'CIP5':['same actual split ell-adic place and inertia; every source IsLocalArtin map'],
 'CIP6':['odd ell, n>0, actual Point r with integral invertible symmetric polarization'],
 'CIP7':['same actual point and its TypeI absolute irreducibility on the full original Gprime'],
 'CIP8':['same actual point, original rational HasFlag in its specified character order, N1 and AdicCont'],
 'CIP9':['same actual point, N3 and N4 for original F.D0'],
 'CIP10':['odd ell, n>0, actual Point r NiceI, and every specified Iu<=r.Ip(u)'],
 'CIP11':['actual rank-four h=0 NiceI point and original O-algebra point map matching the original universal pair'],
 'CIP12':['all remaining producer inputs below, at their exact original same-object and common-threshold scopes'],
}
tex=(HERE/'main.tex').read_bytes()
texlines=tex.splitlines(keepends=True)
claims=[]
for cid,title in titles.items():
    start=next(i for i,l in enumerate(texlines) if l.strip()==f'% BEGIN {cid}'.encode())
    end=next(i for i,l in enumerate(texlines) if l.strip()==f'% END {cid}'.encode())
    rb=b''.join(texlines[start:end+1])
    assert f'\\label{{claim:{cid}}}'.encode() in rb
    claims.append({'id':cid,'title':title,'introduced_in':'0.34',
        'classification':'A' if cid=='CIP1' else 'B',
        'status':'complete proof at the printed original-data scope; CIP12 is a conditional frontier reduction',
        'depends_on':dependencies[cid],'classical_inputs':classical_inputs.get(cid,[]),
        'original_hypotheses':original_hypotheses[cid],
        'remaining_inputs':[] if cid!='CIP12' else ['the eight retained JSP producer entries in closure.json, with their original side conditions'],
        'proof_location':{'file':'count_ii_producer/main.tex','label':'claim:'+cid,
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
 ('symplectic_universal_arithmetic/main.tex',['KX3'],'Actual completion identification and LocCFT; no extrapolation to artOf or every-map normalization'),
 ('joint_support/main.tex',['JSP5','JSP6','JSP7','JSP8','JSP10','JSP11','JSP12'],'Original same-J algebra, exact conditional Dense/P1 and two-Link assembly'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],'Both original rank-four Links and their conditional support-to-PMEx assembly'),
 ('case_two_installation/main.tex',['YX2'],'Exact PMExAlt-to-CountII implication'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],'Only CaseIII vanishes for two-primary targets; I, II and V remain'),
]:
    b=(BASELINE/path).read_bytes()
    inherited.append({'path':'reconstruction_v033/'+path,'sha256':sha(b),'claim_ids':ids,
        'claim_proof_blocks':[inherited_block(b,cid) for cid in ids],'role':role})

published=[
 {'id':'CIP_CFT_GLOBAL','classification':'A','status':'primary statement and exact hypotheses checked',
  'reference':'J. S. Milne, Class Field Theory, version 4.03; V.5.2–5.5 and Remark 5.7, printed pp.178–180; V.4.11, pp.176–177',
  'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf',
  'statement_used':'Global reciprocity is a continuous surjection with kernel closure(E×·infinite identity component), compatible with local reciprocity.',
  'hypotheses_checked':['E is a number field, in particular the original CM field L and Q in the cyclotomic sign check','Omega is the original specified algebraic closure; Gal(Eab/E) is the exact topological abelianization','All local factors are the original completions'],
  'derived_matching':['CIP1 proves openness and checks both directions of inertia/Frobenius clauses and the decomposition closure','CIP1 inverts arithmetic reciprocity to satisfy the original inverse-Frobenius convention','CIP2 independently proves uniqueness for every source predicate map in the required CM scope'],
  'does_not_supply':['generic local-idele injectivity','Chevalley units','automorphic or ordinary Hecke data']},
 {'id':'CIP_CFT_LOCAL_WEIL','classification':'A','status':'primary statement and exact hypotheses checked',
  'reference':'Milne, same source; Introduction printed p.15; I.1.1 and I.1.10–1.11, pp.20,23–24; III.3.4, p.108',
  'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf',
  'statement_used':'Local reciprocity identifies K× with the abelian Weil quotient, units with inertia, and uniformizer with arithmetic Frobenius.',
  'hypotheses_checked':['K=L_w is a nonarchimedean completion of a number field','The original Weil, inertia and degree are identified by completion as in KX3','The source degree-one element is arithmetic Frobenius and ord(uniformizer)=1'],
  'derived_matching':['CIP4 explicitly inverts the arithmetic convention','CIP4 checks smooth-character factorization and all global-map quantifiers','CIP3 independently proves the unit-kernel injectivity at original split CM places, needed for every-IsLocalArtin equality'],
  'does_not_supply':['generic source local-map uniqueness without matching','Hida arithmetic-fiber separation']},
 {'id':'CIP_CFT_NORM','classification':'A','status':'primary statement and exact hypotheses checked',
  'reference':'Milne, same source; III.3.2, printed p.107; V.5.2, p.178; sign independently proved in CIP5 and agrees with V.4.10, pp.175–176',
  'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf',
  'statement_used':'Restriction of local reciprocity along a finite local extension agrees with the local norm.',
  'hypotheses_checked':['The actual v lies over ell; the same chosen valuation shows w lies over ell','K=L_w is finite over Q_ell, so norm compatibility applies','The cyclotomic element lies in inertia, hence its Artin value is a unit'],
  'derived_matching':['CIP5 proves arithmetic reciprocity acts by inverse norm on ell-power roots','CIP5 then inverts reciprocity to obtain the positive norm required by IsWtPart of weight -1','The exact set of continuous embeddings in the source is checked against the finite norm product']},
]
(HERE/'published_applications.json').write_text(json.dumps(published,indent=2,ensure_ascii=False)+'\n')

old=json.loads((BASELINE/'joint_support/closure.json').read_text())
closed_ids={'JSP_EXACT_RECIPROCITY_MATCH','JSP_SINGLE_POINT_NORM'}
remaining=[x for x in old['remaining'] if x['id'] not in closed_ids]
assert len(remaining)==8
closed=[
 {'id':'JSP_EXACT_RECIPROCITY_MATCH','old_classification':'D','by':['CIP1','CIP2','CIP3','CIP4','CIP5'],
  'scope':'Every actual ell-adic place of every original HidaSetting: valid artOf, equality of every admissible source map on the whole Weil group, and the exact positive cyclotomic norm identity on inertia. No coefficient or iota enlargement.'},
 {'id':'JSP_SINGLE_POINT_NORM','old_classification':'C','by':['CIP6','CIP7','CIP8','CIP9','CIP10','CIP11'],
  'scope':'Universal original NiceI restriction for every odd ell, n>0 and Iu<=r.Ip(u); full integral NP with a=n, injective finite local map, exact full determinant law and ordered characters, N3 and original-D0 N4. In particular every actual h=0 rank-four point at ell=3.'},
]
closure={'schema':'rh-human-component-closure/1','artifact_version':'0.34','component':'count_ii_producer',
 'source_commit':PIN,'proof_sha256':sha(tex),'proof_claims':list(titles),'closed':closed,'remaining':remaining,
 'classical_input_nodes':[
    {'id':p['id'],'kind':'published_application_certificate','classification':'A',
     'status':p['status'],'certificate_file':'published_applications.json',
     'certificate_file_sha256':sha((HERE/'published_applications.json').read_bytes()),
     'used_by':[cid for cid,ids in classical_inputs.items() if p['id'] in ids],
     'statement_used':p['statement_used'],'hypotheses_checked':p['hypotheses_checked'],
     'url':p['url']}
    for p in published],
 'selected_frontier_status':{'COUNT_II_SUPPORT':'OPEN C; actual ordinary, four-endpoint Hida, all-level HasAut and five other support producers remain',
    'JSP_COMPLETE_DENSE_TRANSFER':'JSP7 exact reciprocity antecedent supplied; original good arithmetic-fiber separation remains conditional',
    'JSP_SAME_J_HASAUT_TO_P1':'JSP11 six-input implication now has its precise NiceI Norm instance supplied; five other support contracts and same-J HasAut remain',
    'COUNT_III_PRODUCER':'unchanged separate Ctx3/SeedIV dependencies for general targets',
    'RH_case_note':'KA5/KA6 remove only CaseIII for two-primary targets; Cases I, II and V remain substantive'},
 'sufficient_rules':[
    {'conclusion':'JSP_EXACT_RECIPROCITY_MATCH','requires':['CERT_CIP1_CIP5'],'logic':'AND','binding':'actual HidaSetting split places and artOf; every source IsLocalArtin'},
    {'conclusion':'JSP_SINGLE_POINT_NORM','requires':['CERT_CIP6_CIP11'],'logic':'AND','binding':'only original NiceI scope required by h=0; not the general NiceE theorem'},
    {'conclusion':'SAME_J_HIDAPROPSALT','requires':['JSP_ORIGINAL_ORDINARY_DATA','JSP_FOUR_HIDA_ENDPOINTS','CERT_JSP1_JSP7','CERT_CIP1_CIP5'],'logic':'AND','binding':'one original J=ker(B→T)=Ann_B(M)'},
    {'conclusion':'SAME_J_P1CORE','requires':['JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_CHOICE','JSP_ACTUAL_ARPL','JSP_FIRST_ORDER_BOUND','JSP_OBSTRUCTION_BOUND','JSP_SINGLE_POINT_RAW','EXACT_COH_P_AND_SIDE_CONDITIONS','CERT_JSP9_JSP11','CERT_CIP6_CIP11'],'logic':'AND','binding':'same original B,r,J; every point of P1core and its actual derived data'},
    {'conclusion':'COUNT_II_SUPPORT','requires':['BOTH_ORIGINAL_LINKS_WITH_COMMON_KAPPA_AND_DISTINCT_AUXILIARY_PRIMES','SAME_J_HIDAPROPSALT_AND_P1CORE_FOR_EACH_LINK','UNIFORM_COMMON_THRESHOLD_AFTER_FIXED_IOTA_BEFORE_COEFFICIENT_SPACE_AND_UNIVERSAL_DATA','CERT_JSP12','CERT_CIP12'],'logic':'AND'},
 ],
 'nonlogical_shared_links':[
    {'from':'CIP1_CIP5','to':'JSP_ORIGINAL_ORDINARY_DATA','reason':'Supplies actual Artin validity within H.Ax and the weight dictionary only; no other ordinary module/type/fiber producer follows'},
    {'from':'JSP_ORIGINAL_ORDINARY_DATA','to':'JSP_SAME_IDEAL_HASAUT','reason':'Original ordinary module may be the all-level base; independent existential modules do not identify ideals'},
    {'from':'CIP6_CIP11','to':'JSP_SINGLE_POINT_CHOICE','reason':'Supplies the exact normalized input only; does not select detector/eigenvalue/Taylor-Wiles data'},
 ],
 'not_claimed_closed':['source Norm with NiceE disjunct','source full PfromAut including P3core','actual original ordinary R/H.Ax except exact Artin validity','higher-level HasAut','COUNT_II_SUPPORT','COUNT_I_PRODUCER','COUNT_V_PRODUCER','COUNT_III_PRODUCER'],
 'quantifier_guards':[
    'Fix the original tower and iota before the common coefficient threshold; it precedes every later c prime, Space and arbitrary actual universal B,Lambda.',
    'Retain both original rank-four Links with common kappa and distinct auxiliary primes; one J per original universal ring, never an equality across different rings.',
    'Within each Link all six Hida fields and P1core must hold on the exact same original J.',
    'J is fixed before every NiceI point and before every realized TWGrp/TWPl and all level indices.',
    'CIP reciprocity works on the actual chosen split ell-adic places and compares every source IsLocalArtin on the entire Weil group.',
    'The positive norm sign is forced by inverse arithmetic reciprocity; IsWtPart weight -1 is checked explicitly.',
    'CIP normalization is universal for all actual NiceI points, including ell=3; no NiceE instance is claimed.',
    'The normalized a=n full block, every local flag and ordered character, N3, and N4 for the old D0 are kept.',
    'Pointwise constant-field enlargement j(t)=t is allowed by Norm and does not alter the earlier external coefficient threshold or J.',
    'The same-J HasAut plus five remaining support contracts and exact CohP/LocCFT/IsCoef/level/cyclotomic conditions remain required.',
 ],
 'peer_review':'pending independent review, to be bound to proof/proof-block hashes',
 'formal_correctness_assumed':True}
(HERE/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.34','date':'2026-11-22',
 'source_commit':PIN,'component':'count_ii_producer','main_tex_sha256':sha(tex),'claims':claims,
 'source_groups':groups,'source_inventory':sources,'inherited_proof_inputs':inherited,
 'published_applications':{'file':'published_applications.json','sha256':sha((HERE/'published_applications.json').read_bytes()),'ids':[p['id'] for p in published]},
 'builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable':True,'read_only_inputs':['pinned Lean checkout','reconstruction_v033']},
 'validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),
    'claim_source_ranges':sum(len(c['sources']) for c in claims),'all_source_ranges_exact':True,
    'claim_proof_blocks':len(claims),'inherited_claim_proof_blocks':sum(len(x['claim_proof_blocks']) for x in inherited),
    'new_lean_build':False,'independent_human_mathematical_proof':True},
 'scope_note':'Underlying formal correctness is assumed. Every remaining obligation is a human reconstruction obligation. CIP1 is a checked published-theorem application; CIP2–12 provide the written matching, algebra and exact conditional consumer reduction.'}
(HERE/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc=[f'CIP1–CIP12 exact source provenance; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc += [f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",
        f"file_sha256={s['sha256']}",f"range_sha256={s['range_sha256']}",s['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f'''CIP1–CIP12: exact reciprocity and original NiceI normalization, v0.34

Source pin: {PIN}
Proof SHA256: {sha(tex)}
Provenance SHA256: {sha((HERE/'provenance.json').read_bytes())}
Closure SHA256: {sha((HERE/'closure.json').read_bytes())}

Two exact endpoints are now supplied:
1. JSP_EXACT_RECIPROCITY_MATCH (formerly a D matching obligation).
   CIP1 checks the published global reciprocity theorem against every
   IsGlobalArtin field. CIP2 proves source-predicate uniqueness by finite
   quotients, the exact Frobenius iff and weak approximation. CIP3 proves
   local-unit kernel injectivity at the actual split CM places using
   e/conjugate(e) in finite mu(L), avoiding generic Chevalley units.
   CIP4 validates the actual Hilbert-choice artOf, compares every source
   IsLocalArtin on the whole Weil group, and checks its smooth-character
   and all-global-map clauses. CIP5 proves the positive cyclotomic norm
   and the exact continuous-embedding product, including weight -1.
   KX3 is used only in its real scope; it was not relabelled as this match.

2. JSP_SINGLE_POINT_NORM (formerly C at the actual required scope).
   CIP6–11 prove the entire original NiceI instance, universally for odd
   ell and n>0, hence for both actual rank-four Links at ell=3. The
   original Point already has integral invertible symmetric P. Integral
   Gram–Schmidt, a finite constant-field extension and coefficientwise
   square roots give T^t j(P)T=1 with T integral. The proof supplies the
   full block a=n via a written matrix-density argument, denominator
   clearing, integral saturated flags in the original order, psi_mu and
   both N1 clauses. It checks continuity, form, original Iu, full
   determinant polynomial law over every coefficient algebra, N3 and
   N4 for the OLD D0. The map j is explicitly finite free, local and
   injective, with j(t)=t and exact constant/residual compatibility.
   Thus ker(jf)=ker(f) and J is never reselected.

This is not the general NiceE Norm theorem. The source h=0 consumer calls
normalization only at NiceI points, so this universal restriction supplies
the complete required endpoint without asserting full PfromAut/P3core.

The eight retained JSP producer entries remain byte-for-byte in closure's
remaining register, except that the two just-closed entries are removed.
The eight consist of ordinary data; four further Hida endpoints; same-J
all-level HasAut; and five support inputs: Choice, ArPl, first-order bound,
obstruction bound, Raw. The original CohP/LocCFT/IsCoef/level/cyclotomic
side conditions remain in the sufficient rule. Both rank-four Links,
fixed iota followed by one common coefficient threshold, every later
coefficient/Space/universal datum, and the same ideal within each Link
are preserved. No new threshold is introduced by either closure.

COUNT_II_SUPPORT remains open C. It matters for RH as well as unrestricted
GRH; KA5/KA6 remove only CaseIII for two-primary target characters. Cases
I and V are unchanged, and general-character CaseIII remains separate.

Validation: {len(claims)} proof blocks; {len(cache)} pinned files;
{len(sources)} distinct source ranges; {sum(len(c['sources']) for c in claims)}
claim/source references. All source bytes equal the stated git blobs.
The portable builder verifies and regenerates every source/proof hash.
No Lean validity audit or new Lean build is part of this work.

Primary class field theory URL:
https://www.jmilne.org/math/CourseNotes/CFT.pdf
Exact application/hypothesis certificates: published_applications.json.
'''
(HERE/'report.txt').write_text(report)
print(json.dumps({'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'closure_sha256':sha((HERE/'closure.json').read_bytes()),'claims':len(claims),'files':len(cache),
 'source_ranges':len(sources),'claim_source_ranges':sum(len(c['sources']) for c in claims)},indent=2))
