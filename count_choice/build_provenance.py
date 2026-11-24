#!/usr/bin/env python3
"""Rebuild CCH metadata from the pinned Lean checkout and read-only v0.35.

Usage: python build_provenance.py --source /path/to/lean_source \
          --baseline /path/to/reconstruction_v035
Only files beside this builder are written. Stored paths are portable.
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
parser.add_argument('--baseline', type=Path, default=HERE.parent.parent/'reconstruction_v035')
args = parser.parse_args()
REPO, BASELINE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip() == PIN
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P = B+'PatchingModules/'
DP = P+'DeterminantPadicFree/'
W = B+'WeilGroupCharacters/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'

# Inclusive pinned ranges. End zero means through the end of that source file.
# Source proof routes are locators, never substitutes for the written human proof.
SPECS = [
 ('S01',W+'UniversalOrdinaryDeterminantRing.lean',[
   (10,42,'GFrame: original compact group, open eta kernel, c squared one, full epsilon and local groups'),
   (44,62,'HasFlag, mat, diagRep, pushCh and pushRep'),
   (66,80,'G0, conjugation, Gprime as the FULL epsilon kernel, mu and eps'),
   (101,104,'IsForm with exact exponent 1-n and literal form matrix'),
 ]),
 ('S01',B+'CommutativeAlgebra/ResMapBijective.lean',[
   (72,77,'AdicCont is locally constant after every ideal-power quotient'),
   (334,338,'PhiCond: all open subgroups and all open-kernel F_ell-valued characters'),
 ]),
 ('S02',P+'PairedDualFirstOrderDualMatrixSpace.lean',[
   (10,49,'unchanged original Loc and Glob groups'),
   (57,74,'Glob.frame records bottom D0/I0 without replacing the separately retained old subgroup'),
   (192,226,'blkMat, Ev, Od, ddPart, W1, pairedDualFirstOrderDualMatrixSpace and W2'),
   (232,247,'literal dY, LocAt, SelZ and Bd'),
   (251,274,'all original NP fields, including integral form, span, inertia, flags and both N1 clauses'),
   (282,294,'power-series coefficient, N3 and N4 at an arbitrary subgroup'),
   (306,315,'every original Kap field, including independence and generation'),
 ]),
 ('S03',P+'PairedDualFirstOrderDualMatrixSpace.lean',[
   (112,139,'actual DD coordinates and multiplication'),
   (148,187,'DD multiplication identities, constant embedding and epM'),
   (321,328,'literal rho1, w1 and wi1'),
   (334,348,'SelP, SelM, Sel1 and Sel2 on the original covering group'),
 ]),
 ('S03',P+'ThetaCoefficientMapEq.lean',[
   (244,258,'exact epsD, full TwZ, full TwB, eta-trace ell and Detects'),
 ]),
 ('S04',DP+'FrameWith.lean',[
   (13,44,'fraction-field twisted cocycle and DetFr matrix-span/polarization data'),
   (56,84,'IsKap, full IsTw, Ext2 and the actual DD coordinate extractions'),
 ]),
 ('S04',DP+'MapSpan.lean',[(14,150,'detFr: source bridge from NP.span/form to fraction-field matrix algebra')]),
 ('S04',DP+'DTw.lean',[(22,82,'der: trace-vanishing relation gives a derivation on the matrix algebra')]),
 ('S04',DP+'DerEv.lean',[(13,98,'derEv: inner-derivation source route; CCH4 supplies its full-block matrix-unit proof')]),
 ('S05',DP+'EvenPart.lean',[
   (38,82,'trace kills and first full-block trace reduction'),
   (130,165,'symmetric/polarized adjustment source route'),
   (169,214,'evenPart and division only by two for transpose adjustment'),
 ]),
 ('S05',DP+'DetAsm.lean',[(160,268,'detAsm: original integral Detects endpoint and denominator clearing')]),
 ('S05',P+'AutomorphicDetection/Detection.lean',[(6,10,'original Detection from a dense subset of full Gprime')]),
 ('S06',DP+'EllClosed.lean',[(90,146,'closed eta-trace zero locus from exact AdicCont')]),
 ('S06',DP+'OmDense.lean',[(8,37,'separability/discriminant field dictionary'),(66,87,'source multipoint dense intersection; CCH6 needs only direct one-point N3')]),
 ('S07',DP+'LocallyConstantCocyclesFiniteOfPhi.lean',[(11,78,'finite residual cocycles from PhiCond, finite quotient and open-kernel characters')]),
 ('S07',DP+'MemPowSmul.lean',[(64,196,'z1Fg: finite generation target; CCH7 supplies an explicit power-series lifting proof')]),
 ('S07',DP+'AcConst.lean',[(51,81,'matFg source module convention and finite-generation target')]),
 ('S08',DP+'FinSub.lean',[(5,33,'finSub: finite family of evaluation tests')]),
 ('S08',DP+'DetFin.lean',[(127,213,'detFin: original finite Detects with a list in the permitted set')]),
 ('S08',DP+'CharPOfPadic.lean',[(25,76,'general kapEx source route; CCH2 reconstructs the required g=0 specialization directly')]),
 ('S09',B+'AlgebraTools/CaDvrIc.lean',[(6,32,'integralClosure_complete_dvr: exact finite/free/DVR/complete/local/residue endpoint')]),
 ('S09',DP+'SplitEx.lean',[(6,46,'distinct integral roots with literal factorization'),(48,101,'finite common separable splitting extension and integral closure')]),
 ('S10',B+'AlgebraTools/CaDvrPs.lean',[(6,17,'exact equal-characteristic complete DVR power-series endpoint'),(32,94,'finite residue coefficient field and unique lifts'),(95,189,'adic series construction, uniformizer and residue compatibility')]),
 ('S10',DP+'ConstMap.lean',[(5,42,'exact constant-field embedding under an arbitrary power-series ring homomorphism')]),
 ('S11',DP+'PadicHomUnique.lean',[
   (5,20,'uniqueness of Z_ell coefficient map and exact adic push'),
   (22,77,'span_push with the correct ramified exponent'),
   (79,140,'pushNP and every original record field, exact character order and N1'),
   (142,163,'extEx with actual finite local injection, power-series presentation and Ext2'),
 ]),
 ('S11',DP+'ExtFree.lean',[(5,57,'finite-free coordinates, duality, continuity and j(t)=unit*u^e')]),
 ('S12',DP+'CoefficientExtensionPreservesConditionsAndDet.lean',[
   (6,29,'characteristic ell and uniqueness of the full Z_ell coefficient map'),
   (31,47,'fraction-field separability base change'),
   (49,108,'N4 for EVERY subgroup, N3 and the full determinant polynomial law'),
 ]),
 ('S12',W+'RepAlg.lean',[(79,0,'repAlg/ofRep determinant law on arbitrary coefficient algebras')]),
 ('S13',DP+'DetPush.lean',[(6,30,'left and right matrix-coordinate maps'),(77,167,'detPush: exact detector transport along finite local coefficient extension')]),
 ('S14',DP+'CharPOfPadicAlt.lean',[(26,59,'onePt source choice of common splitting ring and finite detector')]),
 ('S14',P+'AutomorphicDetection/Choice.lean',[(14,40,'literal Choice assembly from one-point data')]),
 ('S14',P+'PatchedSupportCompletions.lean',[(214,230,'Detection, every NP.Ext conjunct, and every Choice quantifier/conjunct')]),
 ('S15',P+'ThetaCoefficientMapEq.lean',[
   (14,39,'all-level original TWGrp and exact q/list'),
   (49,61,'Eig, B1 and literal B2: C before m before eventual N and full array conclusion'),
 ]),
 ('S16',P+'TaylorWilesObstructionBound.lean',[
   (13,31,'updated inertia frame, complete original Norm and unchanged CohP'),
   (33,85,'locOf/globOf/residOf/pairOf retain exact original objects'),
   (88,124,'all TWPl fields, LocCFT and full ArPl'),
   (126,154,'first-order B1, general obstruction B2, same-J HasAut and original PfromAut'),
 ]),
 ('S16',P+'PatchedSupportCompletions.lean',[
   (165,185,'literal Pt, Adapted and ChainConcl'),
   (207,212,'full Raw source predicate, restricted to h=0 in CCH17'),
 ]),
 ('S16',P+'ChebotarevFamilies/PFromAutOf.lean',[
   (23,28,'full determinant base-change equality over all coefficient algebras'),
   (30,49,'actual same-J chain order: PhiCond, Norm, Choice, same-list ArPl, then HasAut'),
   (50,81,'constant-field residual determinant and exact PL-kernel proof'),
   (82,103,'same Pt, B1/B2, O-algebra map, determinant/characters and unchanged point kernel'),
   (104,126,'Raw application and literal h=0 NiceI branch giving P1core'),
 ]),
 ('S17',D+'THidaU.lean',[(38,48,'same actual IsJ/ordinary data and common ideal for HidaPropsAlt and HasAut')]),
 ('S17',D+'UnitaryHeckeData.lean',[(59,70,'original R and same original M/ideal construction, retained producer')]),
 ('S17',D+'PointTheoremBaseObject.lean',[(26,48,'six Hida fields and exact coefficient/data/iota quantifiers')]),
 ('S17',D+'LinkTwo.lean',[(13,51,'both original rank-four Links, common kappa and distinct auxiliary primes')]),
 ('S17',D+'PotentialModularityTower.lean',[(38,55,'original tower fields'),(63,66,'fixed iota before a common coefficient threshold and every later Space')]),
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
 'CCH1':'Exact scalar, full cyclotomic kernel and full-block matrix-span identities',
 'CCH2':'Construct every original Kap field with g=0 at a=n',
 'CCH3':'Full original TwZ/TwB/Detects dictionary, including twist, transpose and adic continuity',
 'CCH4':'Trace detection on Gprime by an explicit matrix-unit derivation and central extension argument',
 'CCH5':'Exact polarized integral Detects, clearing denominators and dividing only by two',
 'CCH6':'Detection on the original one-point separable subset from N3 and closed trace zero loci',
 'CCH7':'Finite generation of actual twisted continuous cocycles from PhiCond by explicit t-adic lifting',
 'CCH8':'Construct a finite detector of original separable Gprime elements',
 'CCH9':'Independent finite-free complete DVR integral-closure proof for the actual splitting extension',
 'CCH10':'Explicit coefficient field and power-series presentation, including ramification and constants',
 'CCH11':'One finite local extension with all distinct integral eigenvalues and exact factorizations',
 'CCH12':'Construct every original NP field and every NP.Ext conjunct on that extension',
 'CCH13':'Transport N3, N4 for every old subgroup, full determinant law and the same point kernel',
 'CCH14':'Preserve the same full finite detector under the ramified finite-free extension',
 'CCH15':'Complete original h=0 full-block Choice output with a chosen g=0 Kap',
 'CCH16':'Literal B2 for that same g=0 Kap with C=0 before m and every N',
 'CCH17':'Install coupled Choice/B2 in the same-J h=0 NiceI support consumer with both Links unchanged',
}
claim_groups={
 'CCH1':['S01','S02','S04'],
 'CCH2':['S02','S08'],
 'CCH3':['S01','S02','S03','S04'],
 'CCH4':['S01','S02','S04'],
 'CCH5':['S01','S03','S05'],
 'CCH6':['S01','S02','S03','S06'],
 'CCH7':['S01','S02','S07'],
 'CCH8':['S02','S03','S08'],
 'CCH9':['S09'],
 'CCH10':['S09','S10','S11'],
 'CCH11':['S09','S14'],
 'CCH12':['S01','S02','S11','S14'],
 'CCH13':['S02','S10','S11','S12','S16'],
 'CCH14':['S02','S03','S11','S13'],
 'CCH15':['S02','S03','S09','S11','S14'],
 'CCH16':['S02','S03','S15','S16'],
 'CCH17':['S01','S02','S12','S14','S15','S16','S17'],
}
dependencies={
 'CCH1':[],
 'CCH2':['CCH1'],
 'CCH3':['CCH1','CCH2'],
 'CCH4':['CCH1'],
 'CCH5':['CCH3','CCH4'],
 'CCH6':['CCH5'],
 'CCH7':['CCH1'],
 'CCH8':['CCH6','CCH7'],
 'CCH9':[],
 'CCH10':['CCH9'],
 'CCH11':['CCH8','CCH9','CCH10'],
 'CCH12':['CCH1','CCH2','CCH9','CCH10'],
 'CCH13':['CCH1','CCH9','CCH10','CCH12'],
 'CCH14':['CCH3','CCH9','CCH10','CCH12','CCH13'],
 'CCH15':['CCH2','CCH8','CCH11','CCH12','CCH13','CCH14'],
 'CCH16':['CCH2','CCH12'],
 'CCH17':['CCH13','CCH15','CCH16','CIP10','CIP11','CAP2','CAP13',
          'JSP9','JSP10','JSP11','JSP12','QX4','QX10','YX2','KA5','KA6'],
}
hypotheses={
 'CCH1':['Original GFrame and NP; a=n; the nontrivial residual cyclotomic value is used for chi(g0) != 1.'],
 'CCH2':['Original full-block NP, a=n; no PhiCond, N3 or N4 is needed.'],
 'CCH3':['Original full-block NP and literal g=0 Kap; all original DD, TwZ and TwB conventions.'],
 'CCH4':['Full matrix E-span of r(Gprime), original form-independent twisted cocycle law, H the full cyclotomic kernel, nontrivial residual cyclotomic value.'],
 'CCH5':['CCH4 hypotheses and exact original transpose polarization/form; ell is odd.'],
 'CCH6':['Actual one-point N3 and entrywise AdicCont; full-block standing hypotheses.'],
 'CCH7':['PhiCond on original Gamma; open G=ker eta; finite field coefficients; actual adically continuous chi-twisted matrix action.'],
 'CCH8':['Standing full-block assumptions, PhiCond, N3 and nontrivial residual cyclotomic value.'],
 'CCH9':['A=k[[t]] for a finite field k; L/k((t)) finite separable.'],
 'CCH10':['The actual integral closure B of CCH9 and a chosen uniformizer; finite residue field.'],
 'CCH11':['The finite list of CCH8, with each characteristic polynomial monic of degree n and separable over k((t)); q=0 allowed.'],
 'CCH12':['Original full-block NP and the same finite local injective coefficient map of CCH10; every original ordered local character and flag retained.'],
 'CCH13':['The same extension of CCH12; old N3 or old N4(D) only when the respective conclusion is requested; D is arbitrary and can be the original old D0.'],
 'CCH14':['Same full-block old and extended NP and their chosen g=0 Kaps; old Detects on the specified same S0; actual finite-free ramified coefficient map.'],
 'CCH15':['Original h=0 full-block Choice input: ell odd, PhiCond, N3 and nontrivial residual cyclotomic value; no prescribed detector is assumed.'],
 'CCH16':['Any original TWGrp and the chosen g=0 Kap; no cohomology estimate, PL-kernel or eigenvalue hypothesis is needed by this elementary proof.'],
 'CCH17':['Same original rank-four B,Lambda,J; CohP, LocCFT, IsCoef, V0.Sprime=s.S and nontrivial residual cyclotomic value; retained same-J HasAut, B1 and h=0 Raw; all ordinary/Hida suppliers and original external threshold scope retained.'],
}
tex=(HERE/'main.tex').read_bytes()
texlines=tex.splitlines(keepends=True)
claims=[]
for cid,title in titles.items():
    starts=[i for i,l in enumerate(texlines) if l.strip()==f'% BEGIN {cid}'.encode()]
    ends=[i for i,l in enumerate(texlines) if l.strip()==f'% END {cid}'.encode()]
    assert len(starts)==len(ends)==1,cid
    start,end=starts[0],ends[0]
    assert start<end
    rb=b''.join(texlines[start:end+1])
    assert f'\\label{{claim:{cid}}}'.encode() in rb
    claims.append({'id':cid,'title':title,'introduced_in':'0.36','classification':'B',
        'status':'complete independent human proof at the printed original-data scope; CCH17 is the conditional same-J consumer reduction',
        'depends_on':dependencies[cid],'classical_inputs':[],
        'dependency_scope':{
          'CCH1':'No other claim is invoked; each original definition/hypothesis is read directly.',
          'CCH2':'Uses only the full-block Ev/Od identity from CCH1, not its cyclotomic nontriviality assertion.',
          'CCH7':'Uses only the finite coefficient, open-group and exact scalar/action identities of CCH1.',
          'CCH16':'Uses only g=0 and the original constructed point; B2 holds for any such Kap/TWGrp at every level. Choice provides this same witness.',
          'CCH17':'Consumes only h=0 NiceI and the coupled outputs of CCH15/CCH16. Reuses the unchanged PL-kernel/Adapted/GenBy/stable-discriminant arguments in JSP9-JSP11; does not invoke their old conditional result as if B1, HasAut or Raw had been proved.'
        }.get(cid,'Listed proof inputs are used only at their stated scope.'),
        'original_hypotheses':hypotheses[cid],
        'remaining_inputs':[] if cid!='CCH17' else ['same-J HasAut','first-order B1','h=0 Raw','unchanged CohP and side conditions','ordinary/control and four additional Hida endpoints for full COUNT_II_SUPPORT'],
        'proof_location':{'file':'count_choice/main.tex','label':'claim:'+cid,
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
 ('count_ii_producer/main.tex',['CIP10','CIP11'],'Exact original NiceI Norm, full block a=4, every local field and old D0; same point kernel and original O-algebra map'),
 ('count_auxiliary_primes/main.tex',['CAP2','CAP13'],'PhiCond from unchanged CohP before Choice; exact same finite list realized at every original arithmetic level'),
 ('joint_support/main.tex',['JSP9','JSP10','JSP11','JSP12'],'Exact GenBy/stable-discriminant/kernel facts, PL-kernel proof, same-J one-point consumer and both-Link assembly'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],'Both literal rank-four Links and the exact common support supplier to PMEx'),
 ('case_two_installation/main.tex',['YX2'],'Exact PMExAlt-to-CountII consumer'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],'Only CaseIII is vacuous for two-primary targets; Cases I/II/V still contribute'),
]:
    b=(BASELINE/path).read_bytes()
    inherited.append({'path':'reconstruction_v035/'+path,'sha256':sha(b),'claim_ids':ids,
        'claim_proof_blocks':[inherited_block(b,cid) for cid in ids],'role':role})

known=set(titles)|{cid for entry in inherited for cid in entry['claim_ids']}
assert all(dep in known for deps in dependencies.values() for dep in deps)

# No new theorem is assumed. These exact primary references corroborate the
# complete independent CCH9 proof and are not classified as new A leaves.
(HERE/'published_applications.json').write_text('[]\n')
references=[
 {'id':'CCH_REF_STACKS_032L','role':'corroborating reference, not an assumed theorem application',
  'url':'https://stacks.math.columbia.edu/tag/032L','title':'Stacks Project, Lemma 10.161.8',
  'statement_compared':'Integral closure of a Noetherian normal domain in a finite separable fraction-field extension is finite.',
  'matching':'CCH9 has A=k[[t]], proves A is a normal PID, and proves the finite-module conclusion by the trace-dual lattice argument.',
  'used_as_unproved_input':False,'human_proof':'CCH9','checked_on':'2026-11-22'},
 {'id':'CCH_REF_STACKS_09E8','role':'corroborating reference, not an assumed theorem application',
  'url':'https://stacks.math.columbia.edu/tag/09E8','title':'Stacks Project, Remark 15.113.6',
  'statement_compared':'Integral closure of a DVR in a finite separable extension is finite; over a complete or henselian DVR it has a single maximal ideal.',
  'matching':'CCH9 proves finite freeness, completeness, idempotent lifting, locality and the DVR property directly in the equal-characteristic case.',
  'used_as_unproved_input':False,'human_proof':'CCH9','checked_on':'2026-11-22'},
]
(HERE/'references.json').write_text(json.dumps(references,indent=2,ensure_ascii=False)+'\n')

old=json.loads((BASELINE/'count_auxiliary_primes/closure.json').read_text())
removed={'JSP_SINGLE_POINT_CHOICE','JSP_OBSTRUCTION_BOUND'}
remaining=[x for x in old['remaining'] if x['id'] not in removed]
assert len(remaining)==5
closed=[
 {'id':'JSP_SINGLE_POINT_CHOICE','old_classification':'C','by':[f'CCH{i}' for i in range(1,16)],
  'scope':'Every original h=0 full-block Choice input after NiceI normalization: finite original full-Gprime list, one finite local injective extension, every NP field and NP.Ext conjunct, a constructed g=0 Kap, full twisted polarized Detects, and distinct integral eigenvalues. Also N3, N4 at every separately retained old subgroup, full determinant law and the same original point kernel.'},
 {'id':'JSP_OBSTRUCTION_BOUND','old_classification':'C','by':['CCH2','CCH15','CCH16','CCH17'],
  'scope':'Discharged only in the selected h=0 route through the SAME g=0 Kap constructed by CCH15. For every actual T, literal B2 holds with C=0, before m, and for every N. This is a coupled witness rule, not the universal arbitrary-Kap TaylorWilesObstructionBound theorem.',
  'same_witness_guard':'The selected Choice and B2 conclusions must be consumed together, with exactly the same xprime and kprime. No replacement Kap is permitted.'},
]
closure={
 'schema':'rh-human-component-closure/1','artifact_version':'0.36','component':'count_choice',
 'source_commit':PIN,'proof_sha256':sha(tex),'proof_claims':list(titles),
 'closed':closed,'remaining':remaining,'classical_input_nodes':[],
 'selected_frontier_status':{
   'COUNT_II_SUPPORT':'OPEN C; original ordinary/control/fibers, four additional Hida endpoints, same-J HasAut, first-order B1 and h=0 Raw remain, with unchanged CohP and exact side conditions.',
   'JSP_SINGLE_POINT_CHOICE':'CLOSED at the exact h=0 full-block scope required after NiceI normalization, by CCH1-CCH15.',
   'JSP_OBSTRUCTION_BOUND':'CLOSED ON THE SELECTED COUPLED WITNESS ONLY: CCH16 supplies B2 for CCH15\'s same g=0 Kap; the universal arbitrary-Kap theorem is not claimed.',
   'JSP_FIRST_ORDER_BOUND':'OPEN C, exact same constructed point/Kap and actual realized T/TWPl, with D=4[Lplus:Q]+4T.q.',
   'JSP_ACTUAL_ARPL':'Previously closed at full conditional-on-CohP scope by CAP1-CAP13; supplies PhiCond before the present construction and realizes its precise list afterward.',
   'COUNT_III_PRODUCER':'Unchanged general-target Ctx3/SeedIV/rank-three dependencies.',
   'RH_case_note':'KA5/KA6 remove only CaseIII for two-primary targets; I, II and V remain substantive.'},
 'sufficient_rules':[
   {'conclusion':'COUPLED_ORIGINAL_H0_CHOICE_AND_CHOSEN_B2',
    'requires':['ORIGINAL_FULL_BLOCK_NP_WITH_PHI_N3_NONTRIVIAL_CYCLOTOMIC','CERT_CCH1_CCH16'],
    'logic':'AND','binding':'There is one q,sg,xprime,j,kprime,al satisfying every source h=0 Choice conjunct, kprime.g=0, and for EVERY later original T with that point, T.B2(kprime).'},
   {'conclusion':'SAME_J_P1CORE',
    'requires':['JSP_SAME_IDEAL_HASAUT','CERT_CIP10_CIP11','CERT_CAP2_CAP13','CERT_CCH1_CCH17','JSP_FIRST_ORDER_BOUND','JSP_SINGLE_POINT_RAW','EXACT_COH_P_AND_SIDE_CONDITIONS','CERT_JSP9_JSP11'],
    'logic':'AND','binding':'Fix the original B,r,J before every h=0 NiceI point. Use CCH15 and CCH16 on the SAME point/Kap; realize its SAME q/list by CAP13, preserve the old D0, full determinant law and point kernel, and use B1/Raw on that actual Pt and same-J TWAut.'},
   {'conclusion':'COUNT_II_SUPPORT',
    'requires':['BOTH_ORIGINAL_LINKS_WITH_COMMON_KAPPA_AND_DISTINCT_AUXILIARY_PRIMES','SAME_J_HIDAPROPSALT_AND_P1CORE_FOR_EACH_LINK','UNIFORM_COMMON_THRESHOLD_AFTER_FIXED_IOTA_BEFORE_COEFFICIENT_SPACE_AND_UNIVERSAL_DATA','CERT_JSP12','CERT_CCH17'],
    'logic':'AND','binding':'Each Link has its own original ring and one ideal carrying HidaPropsAlt AND P1core. Both Links remain necessary, with fixed iota before one common threshold and every later original coefficient/Space/B/Lambda.'}],
 'nonlogical_shared_links':[
   {'from':'CERT_CCH15','to':'JSP_FIRST_ORDER_BOUND','reason':'Supplies the original point, Kap, eigenvalues and detector and transports old N4. It proves no numerical B1 estimate.'},
   {'from':'CERT_CCH16','to':'JSP_SINGLE_POINT_RAW','reason':'Supplies the same chosen Pt.b2 field only; the support propagation conclusion still needs Raw.'},
   {'from':'CERT_CCH17','to':'JSP_SAME_IDEAL_HASAUT','reason':'The constructed arithmetic systems are arguments of the required all-system HasAut on the already fixed J. No higher-level automorphic modules are produced.'},
   {'from':'CERT_CCH17','to':'JSP_ORIGINAL_ORDINARY_DATA','reason':'Pointwise coefficient extensions neither construct nor replace the external ordinary/control/arithmetic-fiber system.'}],
 'not_claimed_closed':[
   'CohP itself','general multi-point or arbitrary-block Choice',
   'TaylorWilesObstructionBound for an arbitrary Kap','FirstOrderDualArithmeticBound','h=0 Raw',
   'TThetaEx/full IsWt or original neatU','original integral TypeForAlt producer',
   'original UnitaryHeckeData existence','ordinary/free/control modules, full IsUniv and separating arithmetic fibers',
   'same-J HasAut','four additional Hida endpoints','COUNT_II_SUPPORT',
   'COUNT_I_PRODUCER','COUNT_V_PRODUCER','COUNT_III_PRODUCER'],
 'quantifier_guards':[
   'Original finite coefficient field and its exact Z_ell map; ell is any odd prime, explicitly including ell=3 at rank four. No n or n! is inverted.',
   'The full-block condition a=n is supplied by the original NiceI normalization. No NiceE or arbitrary two-block conclusion is asserted.',
   'Gprime is the FULL cyclotomic kernel, not the residual cyclotomic kernel and not the later TWGrp.H.',
   'The detector is the full original TwZ-to-TwB condition, with cyclotomic twist, transpose sign and adic continuity. Rational trace vanishing alone is not the endpoint.',
   'PhiCond is used at every needed open subgroup; no topological finite-generation assumption is substituted.',
   'One finite list is chosen before one common finite local coefficient extension; the same list survives by a finite-free coordinate argument.',
   'The extension may be ramified: j(t)=v*u^e, e>=1. Both adic continuity and the final Detects exponent use this e.',
   'Every original NP flag, character, form and inertia field is checked; N4 transports for every subgroup, including old D0 even if the intermediate frame stores bottom.',
   'The complete determinant polynomial law is preserved over every coefficient algebra, as are the same O-algebra map, residue constants and point kernel.',
   'Choice and B2 are coupled on the same chosen g=0 Kap. B2 uses C=0 before all m and actually holds for all N, including zero; no arbitrary-Kap closure.',
   'Unchanged CohP and every original LocCFT/coefficient/level/cyclotomic side condition stay required in the original same-J consumer.',
   'The ideal J is fixed before the point, normalization, coefficient extension, detector/list, realized T/TWPl and all N.',
   'Both original rank-four Links remain, with common kappa and literal distinct auxiliary-prime condition; they have different original rings and need not share an ideal.',
   'Fix iota first, then one common coefficient threshold, then every later coefficient, Space and arbitrary original B,Lambda; the pointwise extension does not change that external threshold.',
 ],
 'peer_review':'pending independent review bound to final whole-proof and proof-block hashes',
 'formal_correctness_assumed':True,
}
(HERE/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')

prov={
 'schema':'rh-human-component-provenance/1','artifact_version':'0.36','date':'2026-11-22',
 'source_commit':PIN,'component':'count_choice','main_tex_sha256':sha(tex),
 'claims':claims,'source_groups':groups,'source_inventory':sources,
 'source_files':[{'path':p,'sha256':sha(b),'full_file_sha256':sha(b),'bytes':len(b)} for p,b in sorted(cache.items())],
 'inherited_proof_inputs':inherited,
 'published_applications':{'file':'published_applications.json','sha256':sha((HERE/'published_applications.json').read_bytes()),'ids':[]},
 'corroborating_primary_references':{'file':'references.json','sha256':sha((HERE/'references.json').read_bytes()),'ids':[r['id'] for r in references],'used_as_unproved_inputs':False},
 'builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable':True,'read_only_inputs':['pinned Lean checkout','reconstruction_v035']},
 'validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),
   'claim_source_ranges':sum(len(c['sources']) for c in claims),'all_source_ranges_exact':True,
   'claim_proof_blocks':len(claims),'inherited_claim_proof_blocks':sum(len(x['claim_proof_blocks']) for x in inherited),
   'new_lean_build':False,'independent_human_mathematical_proof':True},
 'scope_note':'Formal correctness is assumed. CCH1-CCH16 reconstruct the actual full-block h=0 Choice and the literal B2 on its SAME g=0 Kap. CCH17 is the exact conditional same-J consumer reduction. All seventeen are completed B arguments at printed scope; this is not a claim that the remaining C producers are complete. No new published theorem is assumed.'
}
(HERE/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc=[f'CCH1-CCH17 exact source provenance; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc += [f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",
       f"file_sha256={s['sha256']}",f"range_sha256={s['range_sha256']}",s['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))

report=f'''CCH1-CCH17: original one-point Choice and its same-Kap B2, v0.36

Source pin: {PIN}
Proof SHA256: {sha(tex)}
Provenance SHA256: {sha((HERE/'provenance.json').read_bytes())}
Closure SHA256: {sha((HERE/'closure.json').read_bytes())}

COMPLETE ORIGINAL SELECTED OUTPUT

CCH1-CCH15 construct every conjunct of the h=0 Choice output after the
original NiceI normalization, which has a=n=4. CCH2 constructs the literal
g=0 Kap because Od=0, including its original generation and independence
fields. CCH3 identifies the full original TwZ and TwB: the cyclotomic
twist, transpose sign and adic continuity are all retained. No detector
is assumed. CCH4 derives a matrix-algebra derivation from trace vanishing,
writes its inner matrix explicitly, and extends from the full cyclotomic
kernel to G0 using the nontrivial residual cyclotomic value. CCH5 imposes
the exact polarization by averaging only by two, then clears denominators.
This works at ell=3 and never divides by 4 or 24.

CCH6 uses actual N3 to restrict to the original separable subset. CCH7
proves finite generation of the actual continuous twisted cocycle module:
PhiCond gives finitely many residual cocycles at the exact open action
kernel, and a direct t-adic lifting argument produces finite generators.
CCH8 then selects finitely many trace rows. The finite detector consists
of elements of the FULL cyclotomic kernel Gprime, not the residual kernel.

CCH9 proves directly that the integral closure in the common finite
separable splitting field is finite free, local, complete and a DVR.
CCH10 constructs the coefficient field and exact k'[[u]] presentation.
The coefficient map may be ramified, j(t)=v*u^e. CCH11 supplies all distinct
integral roots, without falsely requiring the product of the individual
separable polynomials to remain separable. CCH12 checks every original NP
field and every Ext conjunct. CCH13 preserves N3, N4 for EVERY old subgroup,
the FULL determinant polynomial law, O-algebra constants and the point
kernel. CCH14 uses finite-free coordinate maps with their exact ramified
filtration bound to preserve the SAME finite detector. CCH15 assembles
all original Choice outputs on the singleton family; its cardinality
comparison is reflexive. The zero-length detector list is allowed.

THE COUPLED B2 REMOVAL

CCH16 proves literal B2 on that SAME chosen g=0 Kap. Choose C=0 before m;
the result holds for every N, not merely eventually. The array's Fin(g)
index is empty, the coefficient indexed by Fin(1) is the unit one, and
the zero function satisfies every original Sel2 field. This includes m=0
and N=0. The conclusion is not the general TaylorWilesObstructionBound for
an arbitrary Kap. It is precisely the B2 needed by the selected Choice
witness, so the two old producer entries are removed only by a coupled
same-witness rule in the selected h=0 NiceI path.

SAME-IDEAL CONSUMER AND RETAINED FRONTIER

CCH17 fixes the original B,Lambda,J before the arbitrary NiceI point.
CIP10-CIP11 provide the exact full-block normalized point and old N4;
CAP2-CAP13 provide PhiCond and then realize exactly the chosen list by
the actual all-level T/TWPl. CCH13 retains the original point kernel and
the residual/full determinant conventions. The inherited PL-kernel,
Adapted, GenBy and stable-discriminant proofs still apply. The retained
B1 is used with D=4[Lplus:Q]+4T.q, and CCH16 supplies the same Pt's B2.
Retained HasAut on the already fixed J and retained h=0 Raw then give
P1core. Neither is proved merely by constructing the detector or primes.

Five inherited producer entries remain: original ordinary/control/fibers
(including type/neatU/TThetaEx), the four further Hida endpoints, same-J
all-level HasAut, original first-order B1, and original h=0 Raw. CohP and
the exact LocCFT/coefficient/level/cyclotomic side conditions are unchanged.
COUNT_II_SUPPORT remains OPEN C. Both actual rank-four Links remain, with
common kappa and distinct auxiliary primes. Fix iota before ONE common
coefficient threshold for both Links; all later coefficient/Space/B/Lambda
quantifiers and one joint ideal per original ring are unchanged. The finite
coefficient extension is pointwise internal data, not a new external
coefficient threshold. Cases I, II and V still contribute to RH. Only
CaseIII is vacuous for two-primary targets; unrestricted Dirichlet GRH
retains its separate CaseIII/SeedIV/rank-three branch.

There is no new unproved classical import. Stacks tags 032L and 09E8 are
primary corroborating references for the CCH9 integral-closure facts;
the exact needed case is proved in full in the chapter. All new claims
are completed B proofs at their printed scope, not open B obligations.

Validation: {len(claims)} new proof blocks; {len(cache)} pinned source files;
{len(sources)} source ranges; {sum(len(c['sources']) for c in claims)} claim/source
occurrences; {sum(len(x['claim_proof_blocks']) for x in inherited)} inherited proof
blocks. Every source file equals the pinned git blob and every source/proof
range is SHA256-bound. Builder paths are portable. No Lean correctness audit
or new Lean build was performed. Independent human review is pending.

Primary counterparts:
https://stacks.math.columbia.edu/tag/032L
https://stacks.math.columbia.edu/tag/09E8
'''
(HERE/'report.txt').write_text(report)
print(json.dumps({'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'closure_sha256':sha((HERE/'closure.json').read_bytes()),'claims':len(claims),'files':len(cache),
 'source_ranges':len(sources),'claim_source_ranges':sum(len(c['sources']) for c in claims)},indent=2))
