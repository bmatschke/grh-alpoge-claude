from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('/workspace/scratch/368c004c3aea')
OUT = ROOT / 'work_v033/joint_support'
REPO = ROOT / 'lean_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
D = BASE + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
H = BASE + 'HeckeAlgebras/'
W = BASE + 'WeilGroupCharacters/'
P = BASE + 'PatchingModules/'
A = BASE + 'AlgebraTools/DeterminantRepresentations/'
C = BASE + 'CommutativeAlgebraHeight/'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip() == PIN

# Zero as an ending line means the exact last line of the pinned file.
SPECS = [
 ('J01', D+'HidaU.lean', [(12,16,'HidaUAlt: same J has HidaPropsAlt and HasAut')]),
 ('J01', D+'THidaU.lean', [(31,48,'coef_isCoef; locP_of; hida_unitary_of_printed_hida selects one IsJ witness')]),
 ('J01', D+'PointTheoremBaseObject.lean', [(26,41,'PointTheoremBaseObject; six HidaPropsAlt fields; ModularAlt'),(44,48,'ModUAlt coefficient and fixed iota quantifiers')]),
 ('J02', D+'UnitaryHeckeData.lean', [(22,28,'IsTypeAlt'),(38,55,'TypeForAlt; UnitaryPointProperties'),(59,70,'UnitaryHeckeData; original M and IsJ')]),
 ('J02', H+'IsTheta.lean', [(40,52,'HSet.IsMap and HSet.IsJ, including zero-module alternative'),(106,113,'QData.empty'),(123,143,'actual hset, original Gq/prj and admitted=Set.univ'),(156,168,'IsTheta and original residual Hecke eigenvalue identities'),(228,229,'WtOf')]),
 ('J03', H+'CoefficientRepTrivialOnUnramified.lean', [(122,144,'HSet.Ax including actual Artin maps and prime-to-ell Hecke places'),(148,176,'Op, MK, IsWt, finPart, Arith, Good, DenseWt'),(251,284,'TK/gen, IsUniv, Out: actual determinant, ordered characters and fibers')]),
 ('J04', W+'UniversalOrdinaryDeterminantRing.lean', [(109,148,'Residual datum, IsPsi and ordinary Pair'),(150,187,'Pair.Maps; universal determinant ring; weight object and toPair_spec'),(189,216,'actual finite-field power-series Point'),(226,251,'N1, TypeI, N3, N4, NiceI/NiceE'),(259,260,'IsPt'),(284,286,'P1core original prime-generization quantifiers')]),
 ('J05', H+'OrdinaryHeckeCharacters/WeightVariablesExist.lean', [(12,0,'weight_variables_exist and levelUR2WtVars on original inertia groups')]),
 ('J05', P+'ThetaCoefficientMapEq.lean', [(147,159,'WtVars; abelian2 and Sinf variable conventions')]),
 ('J06', W+'RepAlg.lean', [(10,28,'determinant law and full Kills definition'),(102,105,'GDet.Kills')]),
 ('J06', A+'InjTest.lean', [(9,0,'coefficientwise polynomial-law and kernel testing')]),
 ('J06', A+'KerTest.lean', [(7,0,'kerTest for a jointly separating family of representations')]),
 ('J07', A+'FlagRel.lean', [(6,0,'ordered flag characteristic polynomial and ordered annihilation relation')]),
 ('J07', A+'OElRep.lean', [(6,0,'original oEl order')]),
 ('J07', A+'FormRep.lean', [(21,0,'formRep: star, trace and full determinant polarization')]),
 ('J08', H+'HeckePolynomialTorsion/HeckePolCoeff.lean', [(21,56,'rels and Teichmuller tame-kernel argument'),(78,107,'residual equality and exact heckePol coefficient normalization')]),
 ('J08', D+'HeckeDeterminantSatisfiesDeformationRelations.lean', [(15,0,'actual specialized arithmetic fibers give ordinary Pair relations')]),
 ('J08', H+'HeckePolynomialTorsion/MapOfRel.lean', [(5,0,'map_of_rel: actual Pair, universal map and weight triangle')]),
 ('J09', H+'OrdinaryHeckeCharacters/DeformationRingToHeckeAlgebraSurjective.lean', [(11,0,'recover spherical and ordinary generators; exact algebraic surjectivity')]),
 ('J10', D+'ExistsHeckeIdeal.lean', [(28,69,'absH: zero branch or original Hecke kernel'),(70,83,'exists_hecke_ideal and its actual retained arithmetic suppliers')]),
 ('J10', H+'OrdinaryHeckeCharacters/LevelUR2BaseAct.lean', [(12,49,'literal B-action and kernel=J, including zero branch')]),
 ('J11', W+'ArithmeticPointClassicality.lean', [(14,18,'V0ok and IsTeich'),(22,37,'DD, psiT and all eight RingProps fields'),(53,80,'Wt, strictly increasing weights, Pt.Arith/Good and Dense'),(103,111,'TwistOk and original twist transport contract')]),
 ('J12', D+'TJRing.lean', [(23,46,'Teichmuller existence and residual-kernel identity'),(47,136,'full quotient polynomial-law, tame and auxiliary ring properties'),(137,169,'transport through exact quotient-kernel isomorphism'),(172,188,'actual RingProps supplier and retained ordinary/auxiliary inputs')]),
 ('J13', D+'TJDense.lean', [(23,36,'direct algebraic arithmetic-fiber density transfer'),(37,49,'actual dense_of_is_j_unitary_hecke_data')]),
 ('J14', W+'ContinuousResP.lean', [(49,59,'IsWtPart quantifies over every IsLocalArtin; IsLocAlg')]),
 ('J14', H+'Distinct.lean', [(62,66,'lowW and htW reversal and integer shift')]),
 ('J14', D+'TWtBridge.lean', [(27,42,'actual Artin uniqueness, units and surjectivity'),(58,99,'IsFin, finite part and exact local algebraicity equivalence'),(100,167,'embedding compatibility and increasing-to-dominant weight construction'),(168,239,'actual Arith/Good dictionary and cyclotomic norm sign')]),
 ('J15', 'src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/HasExponentZeroIff.lean', [(145,152,'literal IsLocalArtin validity, continuity, degree and global compatibility')]),
 ('J15', D+'LaArtin.lean', [(10,0,'retained actual IsLocalArtin existence supplier')]),
 ('J16', P+'ThetaCoefficientMapEq.lean', [(138,144,'pairVals; augmentationIdealKernel; StOrTh'),(163,175,'exact TWBase fields'),(185,207,'all-level TWRing fields'),(211,226,'all-level TWMaps including theta and exponent relations'),(230,236,'TWAut keeps a single base and common exponent')]),
 ('J16', H+'OrdinaryHeckeCharacters/LevelUR2BasePack.lean', [(12,39,'finite-free same-module TWBase assembly')]),
 ('J17', BASE+'CommutativeAlgebra/ResMapBijective.lean', [(9,14,'IsCO: Noetherian, complete, local, same residue field'),(27,41,'residue map isomorphism and res')]),
 ('J17', C+'UGenApprox.lean', [(7,21,'finite approximation and residue dual functional'),(23,106,'cotangent obstruction and dual-number maps'),(108,120,'u_gen: unique maps imply actual adic polynomial approximation')]),
 ('J18', C+'DGext.lean', [(8,0,'full determinant law determined by characteristic coefficients of group elements')]),
 ('J18', C+'ExistsAdjoinCoeffCharacterSubMemMaximalIdealPow.lean', [(10,0,'actual universal pair coefficient/character generation')]),
 ('J19', P+'DeterminantPadicFree/ConstMap.lean', [(1,42,'finite constant-field preservation by a ring map of power-series rings')]),
 ('J19', P+'DeterminantPadicFree/TypeIDisc.lean', [(10,20,'trace of determinant specialization'),(22,54,'normalized span after inverting t'),(56,77,'full trace Gram discriminant at every ideal below kernel')]),
 ('J20', P+'PairedDualFirstOrderDualMatrixSpace.lean', [(105,106,'PL intersection over open normal subgroups'),(251,275,'NP: original normalized block, span, form, characters and flags'),(288,294,'normalized N3 and original-subgroup N4'),(306,315,'Kap cocycle frame'),(352,360,'DiscSt, NonSS and GenBy')]),
 ('J21', P+'TaylorWilesObstructionBound.lean', [(13,31,'reIu, Norm and CohP'),(37,86,'locOf, globOf, residOf and pairOf preserve actual characters/determinant'),(88,111,'TWPl all level maps and literal H equality'),(115,124,'LocCFT and ArPl'),(126,143,'exact first-order and obstruction bound contracts'),(147,154,'HasAut and PfromAut')]),
 ('J22', P+'PatchedSupportCompletions.lean', [(165,185,'Pt, Adapted and ChainConcl'),(207,213,'Raw: retained full patched support input'),(220,230,'NP.Ext and Choice')]),
 ('J23', P+'ChebotarevFamilies/IpEq.lean', [(5,0,'exact residOf/original/tame-inertia subgroup identity')]),
 ('J23', P+'DeterminantPadicFree/CoefficientExtensionPreservesConditionsAndDet.lean', [(31,108,'fraction-field kernel preservation, N4 and determinant/character extension')]),
 ('J24', P+'ChebotarevFamilies/UnipPow.lean', [(5,18,'actual residue field characteristic'),(20,57,'matrix unipotent power estimate with n*m exponent'),(59,0,'rhoPL: original open normal core and all-conjugates argument')]),
 ('J25', P+'ChebotarevFamilies/PFromAutOf.lean', [(30,49,'exact Norm, Choice, ArPl and same-ideal HasAut setup'),(50,103,'constant-field map, determinant and N4 transport, PL, B1/B2, Pt'),(104,114,'Raw and stable discriminant arguments'),(116,126,'h=0 NiceI branch gives P1core; no thick-chain argument used')]),
 ('J26', D+'PaLevel.lean', [(24,58,'LevelAlt existential single base and all raised levels; LocPAlt; HasAutOfAlt')]),
 ('J26', D+'TLevelU.lean', [(19,22,'actual IsJ to all-level producer: retained')]),
 ('J26', D+'THasAutOf.lean', [(19,49,'same-base all-level assembly with common n! exponent')]),
 ('J27', D+'LinkTwo.lean', [(13,51,'two original Links, common kappa, distinct auxiliary primes and common coefficient threshold')]),
 ('J27', BASE+'WeakShimuraTheory/IsAlgClosureField.lean', [(19,60,'actual rank-four Link and IsPhi data')]),
 ('J28', D+'PotentialModularityTower.lean', [(38,55,'five fields of original PotentialModularityTower'),(63,66,'PMExAlt fixed-iota then coefficient threshold then all spaces')]),
 ('J28', D+'CoefIsCoef.lean', [(11,22,'same J Hida and HasAut followed by PfromAut; noMu gives residual cyclotomic witness')]),
 ('J29', D+'AfDesc.lean', [(17,22,'retained HypothesesHprime extends exact arithmetic package')]),
 ('J29', D+'AutomorphicFormHyp.lean', [(12,22,'retained Hypothesesprime named arithmetic fields')]),
 ('J30', P+'AutomorphicDetection/PfromAut.lean', [(1,0,'actual six-input PfromAut supplier chain; retained, not proved by JSP')]),
 ('J31', D+'HdEx.lean', [(20,27,'original UnitaryHeckeData construction from integral type, theta/isWt and residual eigenvalue suppliers')]),
 ('J31', H+'OrdinaryHeckeCharacters/HiAlgUnit.lean', [(127,139,'actual ordinary Hecke algebra finiteness, torsion-freeness and generators: retained control producer')]),
 ('J31', H+'PointRepUnramifiedAtAuxiliaryPlace.lean', [(285,302,'auxiliary local representation statement and stable-lattice/residual hypotheses'),(367,371,'exact point_rep_unramified_at_auxiliary_place statement: retained')]),
 ('J32', D+'ArithmeticPointPurity.lean', [(1,3,'exact arithmeticPointPurityDense alias')]),
 ('J32', D+'ArithmeticPointClassicality.lean', [(1,3,'exact arithmeticPointClassicalityDense alias')]),
 ('J32', 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/ArithmeticPointDecomposition.lean', [(26,35,'literal ArithmeticPointDecomposition retained endpoint')]),
 ('J32', 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean', [(17,29,'WitOff and AutOffN precise off-auxiliary-place automorphy'),(56,60,'literal IrrArithPointsAutomorphicAway retained endpoint')]),
]

cache = {}
sources = []
groups = {}
for group, path, ranges in SPECS:
    b = (REPO/path).read_bytes()
    if path not in cache:
        assert b == subprocess.check_output(['git','show',PIN+':'+path],cwd=REPO), path
        cache[path] = b
    lines = b.splitlines(keepends=True)
    for start, end, declaration in ranges:
        end = end or len(lines)
        assert 1 <= start <= end <= len(lines), (path,start,end,len(lines))
        rb = b''.join(lines[start-1:end])
        sid = f'{group}-{len(groups.get(group, []))+1}'
        sources.append({'id':sid,'group':group,'path':path,'declaration':declaration,
          'line_start':start,'line_end':end,'sha256':sha(b),'full_file_sha256':sha(b),
          'range_sha256':sha(rb),'range_bytes':len(rb),'first_line':lines[start-1].decode().rstrip(),
          'verified_equal_to_pinned_git_blob':True,
          'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'})
        groups.setdefault(group, []).append(sid)

titles = {
 'JSP1':'Weight coordinates on the actual local inertia groups',
 'JSP2':'Full polynomial-law and determinant-kernel detection by separating arithmetic fibers',
 'JSP3':'The actual ordinary Pair and unique weight-compatible universal map',
 'JSP4':'Explicit recovery of every Hecke generator and algebraic surjectivity',
 'JSP5':'Original IsJ, Hecke kernel and module annihilator are exactly the same ideal',
 'JSP6':'All eight original RingProps fields from the specified actual arithmetic system',
 'JSP7':'Exact increasing-weight and finite-character dictionary, then full Dense transfer',
 'JSP8':'Literal TWBase on the original ordinary module and same ideal, including zero module',
 'JSP9':'Topological generation by the actual universal determinant/character values',
 'JSP10':'Constant-field transport, unchanged kernels and stable discriminants in characteristic ell',
 'JSP11':'Complete single-point NiceI implication HasAut plus six retained support inputs to P1core',
 'JSP12':'Same-ideal Hida/P1 assembly with both rank-four Links and common coefficient threshold',
}
claim_groups = {
 'JSP1':['J04','J05','J16'],
 'JSP2':['J06','J07','J08','J12'],
 'JSP3':['J02','J03','J04','J06','J07','J08','J10','J31'],
 'JSP4':['J03','J08','J09','J10'],
 'JSP5':['J02','J10','J16'],
 'JSP6':['J03','J06','J07','J11','J12','J31'],
 'JSP7':['J02','J03','J11','J13','J14','J15'],
 'JSP8':['J05','J10','J16','J21'],
 'JSP9':['J04','J16','J17','J18','J20'],
 'JSP10':['J04','J19','J20','J23'],
 'JSP11':['J04','J16','J20','J21','J22','J23','J24','J25','J30'],
 'JSP12':['J01','J02','J11','J16','J21','J26','J27','J28','J29','J30','J31','J32'],
}
depends = {
 'JSP1':['KX3','KX4','KX5'],
 'JSP2':[],
 'JSP3':['JSP2','KX1','KX5','KX9'],
 'JSP4':['JSP3'],
 'JSP5':['JSP3','JSP4'],
 'JSP6':['JSP1','JSP2','JSP3','JSP5'],
 'JSP7':['JSP3','JSP5'],
 'JSP8':['JSP1','JSP5'],
 'JSP9':['KX1','KX9','QX5'],
 'JSP10':[],
 'JSP11':['JSP9','JSP10'],
 'JSP12':['JSP3','JSP4','JSP5','JSP6','JSP7','JSP8','JSP11','KX3','QX4','QX5','QX10','YX2'],
}
inputs = {
 'JSP1':['supplied original Link, Resid and LamObj'],
 'JSP2':['jointly separating coefficient maps and original polarized flagged representations when used'],
 'JSP3':['JSP_ORIGINAL_ORDINARY_DATA'],
 'JSP4':['JSP_ORIGINAL_ORDINARY_DATA'],
 'JSP5':['JSP_ORIGINAL_ORDINARY_DATA in nonzero module case only'],
 'JSP6':['JSP_ORIGINAL_ORDINARY_DATA including auxiliary I0 unramifiedness at a separating weight'],
 'JSP7':['JSP_ORIGINAL_ORDINARY_DATA including good separation at every weight','JSP_EXACT_RECIPROCITY_MATCH'],
 'JSP8':['JSP_ORIGINAL_ORDINARY_DATA in nonzero module case only'],
 'JSP9':['actual original universal ordinary determinant ring'],
 'JSP10':['injective local map of actual finite-field power-series rings; normalized NP with a=4'],
 'JSP11':['JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_NORM','JSP_SINGLE_POINT_CHOICE','JSP_ACTUAL_ARPL','JSP_FIRST_ORDER_BOUND','JSP_OBSTRUCTION_BOUND','JSP_SINGLE_POINT_RAW','exact CohP/LocCFT/IsCoef/hS/nontrivial residual cyclotomic side conditions'],
 'JSP12':['JSP_ORIGINAL_ORDINARY_DATA','JSP_EXACT_RECIPROCITY_MATCH','JSP_FOUR_HIDA_ENDPOINTS','JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_NORM','JSP_SINGLE_POINT_CHOICE','JSP_ACTUAL_ARPL','JSP_FIRST_ORDER_BOUND','JSP_OBSTRUCTION_BOUND','JSP_SINGLE_POINT_RAW','all retained inputs uniform for both original Links after fixed iota and before coefficient/Space/universal choices'],
}
tex = (OUT/'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    start = next(i for i,l in enumerate(lines) if l.strip()==f'% BEGIN {cid}'.encode())
    end = next(i for i,l in enumerate(lines) if l.strip()==f'% END {cid}'.encode())
    rb = b''.join(lines[start:end+1])
    claims.append({'id':cid,'title':title,'introduced_in':'0.33','classification':'B',
      'status':'complete conditional human proof at the explicitly stated supplied-original-data scope; no arithmetic producer asserted',
      'depends_on':depends[cid],'remaining_inputs':inputs[cid],
      'proof_location':{'file':'joint_support/main.tex','label':'claim:'+cid,'line_start':start+1,'line_end':end+1,'sha256':sha(rb),'bytes':len(rb)},
      'source_groups':claim_groups[cid], 'sources':[s for s in sources if s['group'] in claim_groups[cid]]})
inherited = []
for path, ids, scope in [
 ('symplectic_universal_arithmetic/main.tex',['KX1','KX3','KX4','KX5','KX9'],'actual universal rings and LocCFT; no inference of the every-IsLocalArtin normalization match'),
 ('symplectic_modular_support/main.tex',['QX4','QX5','QX10'],'two rank-four Links, actual pair, integral word identity, conditional support-to-PMEx assembly'),
 ('case_two_installation/main.tex',['YX2'],'completed conditional PMExAlt to CountII chain'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],'only Case III is vacuous for 2-primary target characters'),
]:
    p = ROOT/'reconstruction_v032'/path
    inherited.append({'path':'reconstruction_v032/'+path,'claim_ids':ids,'sha256':sha(p.read_bytes()),'role':scope})

remaining = [
 {'id':'JSP_ORIGINAL_ORDINARY_DATA','classification':'C','contract':'At every later allowed coefficient and arbitrary original universal B,Lambda for each of the two actual rank-four Links, supply R:UnitaryHeckeData Qempty iota Lambda, actual H.Ax, finite free original M, commuting Hecke operators, T IsCO, residual eigenvalues, continuous full determinant/ordered characters satisfying exact IsUniv and residual/torsion/inertia restrictions, separating good arithmetic fibers at every admitted weight with original flags/polarization/tame type, and auxiliary I0 unramifiedness at one separating weight under V0ok. Nonzero arithmetic assertions are needed only if M is nonzero.','same_witness':'R,H,M,T and the exact kernel J of JSP5, not independently chosen substitutes.'},
 {'id':'JSP_EXACT_RECIPROCITY_MATCH','classification':'D','contract':'For the actual artOf at each original ell-adic place: validity of IsLocalArtin, equality of every map satisfying that source predicate with artOf, and epsilon(sigma)=product_tau tau(Art(sigma)) on inertia. The source uses global reciprocity/local-idele injectivity and the cyclotomic norm formula; KX3 LocCFT alone is not this exact source matching.','same_witness':'The Artin maps in R.theta and H.IsUniv; every-map quantifier of IsWtPart.'},
 {'id':'JSP_FOUR_HIDA_ENDPOINTS','classification':'C','contract':'On the exact J=Ann_B M=ker(B→T), prove PointTheoremBaseObject iota J, arithmeticPointPurityDense iota J, arithmeticPointClassicalityDense iota J and TwistOk J, with their literal original point/weight/twist quantifiers.','same_witness':'Same original B,Lambda,iota,J as RingProps and Dense.'},
 {'id':'JSP_SAME_IDEAL_HASAUT','classification':'C','contract':'For every T:TWGrp(globOf r V) and its actual TWPl, supply TWAut(pairOf B.u,J,Empty,4[L+:Q],T). This includes one base, residual eigenvalue lifts, all TWRing_N and all TWMaps_N with one common exponent. JSP8 supplies the original base only; no higher-level modules or local identities are produced.','same_witness':'J fixed before the later T, TWPl and all N. Each supplied all-level system keeps its own single base over that exact J.'},
 {'id':'JSP_SINGLE_POINT_NORM','classification':'C','contract':'The literal Norm instance at each original NiceI point: injective finite local coefficient extension, normalized NP with full block a=4, same determinant/ordered characters, N3 and N4 for the original auxiliary D0.'},
 {'id':'JSP_SINGLE_POINT_CHOICE','classification':'C','contract':'The literal h=0 Choice instance after normalization and PhiCond: finite original G-prime elements, one injective finite local extension, exact Kap, Detects and distinct eigenvalues, preserving normalized block/representation/characters.'},
 {'id':'JSP_ACTUAL_ARPL','classification':'C','contract':'For the original arithmetic frame and CohP, supply PhiCond and realize the chosen finite G-prime elements by actual TWGrp and TWPl with all level maps, prime/Frobenius/tame data and the exact residual-kernel identity for its open normal H.'},
 {'id':'JSP_FIRST_ORDER_BOUND','classification':'C','contract':'For this original normalized point, Kap, realized T/TWPl and original N4/LocCFT/nontrivial residual cyclotomic conditions, prove the exact B1 with D=4[L+:Q]+4T.q.'},
 {'id':'JSP_OBSTRUCTION_BOUND','classification':'C','contract':'For the same point, Kap, realized T/TWPl and stated PL-kernel/eigenvalue/cyclotomic conditions, prove the exact B2.'},
 {'id':'JSP_SINGLE_POINT_RAW','classification':'C','contract':'The original Raw theorem restricted to h=0, rank four, actual pair/J/TWAut, Adapted, GenBy, exact Pt(B1,B2) and automatic one-point residue-cardinality equality. It propagates J from a stable prime below ker g to every stable prime below that same kernel.'},
]
prov = {'schema':'rh-human-component-provenance/1','artifact_version':'0.33','date':'2026-11-22',
  'source_commit':PIN,'component':'joint_support','main_tex_sha256':sha(tex),'claims':claims,
  'source_groups':groups,'source_inventory':sources,'inherited_proof_inputs':inherited,
  'external_input_scope':'No new published theorem is certified as A. Existing local reciprocity/universal determinant inputs retain their inherited exact scopes. Every-IsLocalArtin uniqueness and the literal cyclotomic normalization remain explicitly retained source matching, not an extrapolation of KX3.',
  'validation':{'pinned_blob_verified_files':len(cache),'source_ranges':len(sources),'claim_source_ranges':sum(len(c['sources']) for c in claims),'all_source_ranges_exact':True,'claim_proof_blocks':len(claims),'new_lean_build':False,'independent_human_mathematical_proof':True},
  'scope_note':'Lean correctness is assumed. The remaining obligations concern only human reconstruction of the original joint producer. All twelve claims are complete implications, not twelve newly supplied arithmetic existence theorems.'}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False)+'\n')
loc = [f'JSP1–JSP12 exact source provenance; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc += [f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",f"file_sha256={s['sha256']}",f"range_sha256={s['range_sha256']}",s['url'],'']
(OUT/'source_locators.txt').write_text('\n'.join(loc))
closure = {'schema':'rh-human-component-closure/1','artifact_version':'0.33','component':'joint_support',
  'source_commit':PIN,'proof_sha256':sha(tex),'proof_claims':list(titles),
  'closed':[
    {'id':'JSP_ORIGINAL_ISJ_KERNEL','by':['JSP2','JSP3','JSP4','JSP5'],'scope':'Conditional on the printed original ordinary data; exact IsJ and J=ker(B→T)=Ann_B M; zero module J=top is included.'},
    {'id':'JSP_COMPLETE_RINGPROPS_TRANSFER','by':['JSP1','JSP2','JSP3','JSP5','JSP6'],'scope':'All eight original fields on that exact J, including full polynomial-law and star identities; auxiliary I0 fiber unramifiedness remains an input.'},
    {'id':'JSP_COMPLETE_DENSE_TRANSFER','by':['JSP7'],'scope':'Every strictly increasing original weight, conditional on actual good-fiber separation and printed exact reciprocity matching; admitted weights are literally all weights.'},
    {'id':'JSP_ORIGINAL_TWBASE','by':['JSP1','JSP5','JSP8'],'scope':'Same original module and exact annihilator J; both zero and nonzero module alternatives; no all-level or patched-support production.'},
    {'id':'JSP_ACTUAL_PAIR_GENBY','by':['JSP9'],'scope':'Every supplied actual universal ordinary determinant ring; integral determinant-law word identity and dual-number/cotangent argument.'},
    {'id':'JSP_NICEI_STABLE_DISC_KERNEL_TRANSPORT','by':['JSP10'],'scope':'Exact injective finite coefficient-extension kernels and full normalized a=4 trace discriminant, valid also at ell=3.'},
    {'id':'JSP_SAME_J_HASAUT_TO_P1','by':['JSP9','JSP10','JSP11'],'scope':'The h=0 NiceI implication from the six printed source contracts and exact CohP/LocCFT/IsCoef/level/cyclotomic side conditions; J never reselected.'},
    {'id':'JSP_TWO_LINK_JOINT_ASSEMBLY','by':['JSP12'],'scope':'Conditional assembly after fixed iota and a common coefficient threshold; separate ideals in the two original universal rings, then existing QX10/YX2.'},
  ],
  'remaining':remaining,
  'selected_frontier_status':{'COUNT_II_SUPPORT':'OPEN C: no actual joint arithmetic producer is asserted','COUNT_III_PRODUCER':'UNCHANGED: Ctx3 and SeedIVAlt remain separate for unrestricted GRH','RH_case_note':'KA5/KA6 remove only Case III for 2-primary targets; I, II and V remain substantive.'},
  'sufficient_rules':[
    {'conclusion':'SAME_J_HIDAPROPSALT','requires':['JSP_ORIGINAL_ORDINARY_DATA','JSP_EXACT_RECIPROCITY_MATCH','JSP_FOUR_HIDA_ENDPOINTS','CERT_JSP1_JSP7'],'logic':'AND','binding':'Endpoint J is the exact original kernel constructed in JSP5.'},
    {'conclusion':'SAME_J_P1CORE','requires':['JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_NORM','JSP_SINGLE_POINT_CHOICE','JSP_ACTUAL_ARPL','JSP_FIRST_ORDER_BOUND','JSP_OBSTRUCTION_BOUND','JSP_SINGLE_POINT_RAW','EXACT_COH_P_AND_SIDE_CONDITIONS','CERT_JSP9_JSP11'],'logic':'AND','binding':'Every support contract is applied to the same original r,B,J and its actual derived point/TW data.'},
    {'conclusion':'COUNT_II_SUPPORT','requires':['BOTH_ORIGINAL_LINKS_WITH_COMMON_KAPPA_AND_DISTINCT_AUXILIARY_PRIMES','SAME_J_HIDAPROPSALT_AND_P1CORE_FOR_EACH_LINK','UNIFORM_COMMON_THRESHOLD_AFTER_FIXED_IOTA_BEFORE_COEFFICIENT_SPACE_AND_UNIVERSAL_DATA','CERT_JSP12'],'logic':'AND'},
  ],
  'nonlogical_shared_links':[
    {'from':'JSP_ORIGINAL_ORDINARY_DATA','to':'JSP_SAME_IDEAL_HASAUT','reason':'The same original ordinary module can be the base of the all-level construction; independent existence of two modules does not identify their ideals.'},
    {'from':'JSP_ACTUAL_ARPL','to':'CohP','reason':'Cohomological package is a shared exact hypothesis; no separate existence theorem is proved here.'},
    {'from':'COUNT_II_SUPPORT','to':'COUNT_III_PRODUCER','reason':'The common PMExAlt also contributes to unrestricted GRH, but does not supply the separate Ctx3/SeedIV chain.'},
  ],
  'quantifier_guards':[
    'Fix original Fit/Deep tower and iota before selecting the common coefficient threshold.',
    'The common threshold works for all later c prime, original Space, and arbitrary actual universal B,Lambda, on both original rank-four Links.',
    'One J per Link carries all six HidaPropsAlt fields and P1core; never combine separate existential ideals.',
    'The two Links have different universal rings and therefore separate ideals; no equality across those rings is asserted.',
    'The same J is fixed before every NiceI point and before every realized T/TWPl and all level indices N.',
    'Raw, Norm and Choice are needed only in the single-point h=0 scope; this does not prove them.',
    'Original D0 survives the reIu intermediate frame and every injective finite coefficient extension.',
    'JSP7 requires validity/uniqueness/norm matching for the actual source Artin maps, not just LocCFT.',
    'The M=0 branch uses J=top and the zero module; it requires no nonzero Hecke algebra arithmetic data.',
    'No division by 3, matrix size, or 4 factorial occurs in the completed algebraic/support transports; ell=3 is retained.',
  ],
  'peer_review':'pending independent root review; bind to proof and proof-block hashes',
  'formal_correctness_assumed':True}
(OUT/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'main_sha256':sha(tex),'provenance_sha256':sha((OUT/'provenance.json').read_bytes()),'closure_sha256':sha((OUT/'closure.json').read_bytes()),'claims':len(claims),'files':len(cache),'source_ranges':len(sources),'claim_source_ranges':sum(len(c['sources']) for c in claims)},indent=2))
