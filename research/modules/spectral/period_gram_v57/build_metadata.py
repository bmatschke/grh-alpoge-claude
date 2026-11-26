#!/usr/bin/env python3
"""Bind the PGR human proof to the exact original interfaces; no Lean replay."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
REPO=Path('/workspace/scratch/249d32c24541/formal_source')
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION='0.57'
COMPONENT=HERE.name
SNAPSHOT=HERE/'source_snapshot'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
S='src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
H=S+'HaarTransversals/'
U=H+'UnitaryHaarProducts/'
O=S+'ClosedLocalOrbits/'
J=O+'GaugeLatticeShifts/'
F=S+'FlagStabilizerTensors/'
Q='src/Formalism/SharpRestriction/CuspSpanNormBounds/'

def sha(data): return hashlib.sha256(data).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def f(prefix,name,first=None,last=None,declaration='Exact original definition or producer; complete pinned file retained for context'):
    return (prefix+name+'.lean',first,last,declaration)

groups={
 'setting':[
  f(H,'HidaSetting',179,234,'Actual rational lattice, fractional-ideal splitting, word frames and supplied global additive character'),
  f(H,'HidaSetting',236,277,'Actual finite reference frame, two-prime level and xu transport'),
  f(H,'HidaSetting',300,328,'Original infinity measures, wave functions and their precise laws'),
  f(F,'PoincareConstantEq',25,67,'Full record, every witness and literal normalizing constants'),
 ],
 'character':[
  f(H,'HidaSetting',42,72,'Root coordinates and finite/infinite additive-character normalization'),
  f(U,'HermitianETransportInvariant',25,27,'Full PsiDd: every inverse-different rational element and integral finite multiplier'),
  f(S+'TraceIntegralEstimates/','PsiTrCore',146,None,'Original trace-character producer, including finite Chinese remaindering'),
  f(S+'TraceIntegralEstimates/','DdTraceCore',12,None,'Different trace integrality and complete DdTraceCore'),
  f(U,'HermitianETransportInvariant',1856,1875,'Full PsiDd assembly and finite phase supplier'),
 ],
 'levi':[
  f(H,'HidaSetting',24,35,'Literal S and N stabilizer predicates'),
  f(U,'InHHAlg',575,583,'Original RatLevi and PsiProd interfaces'),
  f(U,'HermitianETransportInvariant',1029,1042,'Original rational character product'),
  f(U,'HermitianETransportInvariant',1758,1852,'Original rational Levi producer and fixed complement'),
 ],
 'finite_phase':[
  f(U,'InHHAlg',371,382,'Exact KsetSplit and UnipotentConjugateInLevel statements'),
  f(U,'HermitianETransportInvariant',696,712,'Extension of character triviality to the completed inverse different'),
  f(U,'HermitianETransportInvariant',851,962,'Codifferent location, e/z and bw phase comparison and unipotent_in_level_of_psi'),
 ],
 'integral_levi':[
  f(U,'HermitianETransportInvariant',40,90,'The actual hyperbolic projection preserves the completed lattice'),
  f(U,'HermitianETransportInvariant',240,284,'Integral Levi extraction and full ksetSplit_holds'),
 ],
 'neat':[
  f(U,'InHHNeat',12,18,'Full NeatKu and finite-order/torsion-free stabilizer scopes'),
  f(U,'InHHFinOrd',257,288,'Finite order from the actual positive complement and integral lattice'),
  f(U,'InHHFinOrd',403,None,'Every conjugate finite compact-level stabilizer and full neatKu_of_gamUnipKu'),
  f(U,'InHHGamUnipKuGlob',470,532,'Actual reference-frame reduction at both auxiliary primes'),
 ],
 'columns':[
  f(S+'SiegelMassRatios/','ColsDim',23,43,'Original scalar forms and compact-type covariance'),
  f(S+'SiegelMassRatios/','ColsDim',63,97,'Complete column decomposition and Riesz sharp interfaces'),
  f(O,'TermOp',207,230,'Actual column representatives and literal sharp map'),
  f(F,'ParametersTermRelations',18,119,'Antilinear sharp, original ColT norm and inverse coordinates'),
 ],
 'seed':[
  f(H,'PoincareInHH',144,184,'Cu, Srat, finite decomposition, actual seed, PhWellDef and PhProps'),
  f(U,'InHHAlg',404,410,'Actual decomposition-independence producer'),
  f(U,'InHHFinal',49,None,'Original complete seed properties from the primitive suppliers'),
 ],
 'density':[
  f(J,'SlabCoverPfSteps',16,42,'Exact rational injectivity, finite density, unipotent lifting and lattice dictionary'),
  f(J,'SlabNDensePf',14,None,'Original strong-approximation supplier and actual finite topology'),
  f(J,'RegroupPfColCover',19,33,'Exact arbitrary finite unipotent strong approximation'),
  f(J,'DoubleCosetSingleUnfolding',449,464,'Existence of every original NOcol strict domain'),
 ],
 'column_unipotents':[
  f(J,'KExpCut',622,629,'Literal NOcol and slab definitions'),
  f(J,'RegroupPfOrbitAlg',31,118,'Rational lifting uniqueness, unipotent group and quotient relation'),
 ],
 'slabs':[
  f(J,'DoubleCosetSingleUnfolding',280,324,'Exact support coverage and full all-section SlabCoverC'),
  f(J,'SlabCoverPf',17,127,'Actual coverage and uniqueness through rational unipotent and Levi factors'),
  f(J,'KExpCut',568,590,'Exact finite-coset product integral with one volK2 factor'),
  f(J,'KExpCut',631,648,'Full SlabFD and Regroup interfaces'),
 ],
 'fold_bound':[
  f(H,'FoldBound',11,34,'Literal multiplicity and full measurable-set FoldBound'),
  f(H,'FoldBound',75,None,'Countable transversal and left-Haar proof of the bound'),
 ],
 'mixed_unfold':[
  f(H,'PoincareSeriesSquareIntegrable',14,88,'All original finite, L2 and mixed-inner statements with all domains'),
  f(H,'WuDecay',36,44,'Exact FoldOK: one compact set and constant before all column vectors'),
 ],
 'slab_abs':[
  f(J,'RegroupPf',61,87,'Exact SlabAbs and OrbitUnfold scopes'),
  f(J,'RegroupPfSlabAbs',78,None,'Original pre-integration absolute slab bound'),
  f(U,'InHHLeaf',14,35,'Actual rational fundamental-domain bridge and measurable Poincare functions'),
  f(H,'PoincareInHH',194,200,'Original all-representative InHH and actual automorphic range'),
 ],
 'return_carrier':[
  f(O,'TermOp',60,107,'Actual RatLink, GCar, GRel, GTerm and selected representatives'),
  f(O,'TermDef',142,145,'Literal full PD: lift, admissibility and FrameOK'),
  f(Q,'IsPrimitiveSub',65,68,'ModG is localization at every prime above g'),
  f(Q,'IsPrimitiveSub',96,104,'Lift and full local/primitivity convention'),
  f(Q,'IsPrimitiveSub',136,147,'One integral upper unitriangular matrix in IsAdmissible'),
  f(Q,'FlagEEqHyperbolic',97,104,'Actual row representatives and prescribed isotropic lattice'),
  f(Q,'FlagEEqHyperbolic',119,120,'Both FrameOK fields'),
  f(J,'RegroupPfTermCar',76,149,'Full transported flag predicate and return carrier'),
  f(J,'RegroupPfFrameCong',42,None,'Actual two-frame congruence with one integral upper unitriangular lift'),
  f(J,'RegroupPfModGOfAt',18,None,'Exact finite-to-localized ModG comparison'),
 ],
 'support_reindex':[
  f(J,'RegroupPf',24,59,'GamCol, ColCl and scalar plus absolute SupportReindex'),
  f(J,'RegroupPf',271,312,'Original support-index bijection and absolutely convergent sums'),
  f(J,'RegroupPfColCover',36,None,'Actual support-cover producer from finite density'),
 ],
 'orbit_unfold':[
  f(J,'RegroupPf',330,355,'Exact OrbitAlg group, action, term and stabilizer interfaces'),
  f(J,'RegroupPfOrbitAlg',120,None,'Original exact orbit/stabilizer identification'),
  f(J,'RegroupPfUnfold',1,None,'Original countable orbit-domain unfolding and all-section integral'),
  f(O,'TermOp',140,182,'Original ROset, FundOf, OOt, FundExists and all-domain independence'),
  f(O,'TermOpStmt',50,73,'Every original AmpWellDef carrier/domain witness and both phase conclusions'),
 ],
 'term_entry':[
  f(O,'TermOp',22,34,'Exact rank-one operator, Bochner orbital integral and integrability'),
  f(O,'TermOp',244,266,'Literal scl, blk, aTerm and Hilbert-Schmidt encoding'),
  f(J,'RegroupPf',89,99,'Exact TermVal, including inner-product orientation'),
  f(J,'KExpCut',109,113,'Full original EntryUnfold'),
  f(J,'KExpCut',423,461,'Block absolute convergence and kExpansion_of_abs'),
  ('src/Formalism/HermitianCurvature/StatementPB.lean',81,82,'All three original AbsConv clauses'),
 ],
 'endpoint':[
  f(F,'PoincareConstantEq',118,136,'Full universal KExpansionC and distinct unsupplied AbsConvC'),
  f(O,'TermOpStmt',23,31,'Literal HasSum and sesquilinear KExpansion output'),
  f(J,'DoubleCosetSingleUnfolding',466,504,'Original universal KExpansionC producer and exact inputs'),
  f(S+'ClosedVolumeStatements/','UnipotentInLevelSubgroup',63,66,'Named original KExpansionC endpoint'),
 ],
 'linear_transport':[
  f(H,'PoincareInHH',202,220,'Full PuLinear implication and actual period map'),
  f(H,'PoincareInHH',254,263,'Original domains, c0X and Kform without positivity hypothesis'),
  f(F,'ParametersTermRelations',129,149,'Antilinear coordinate transport is a complex-linear operator'),
  f(F+'RootLatticeThresholds/','NormalizingConstantEq',160,231,'Continuous additive transport, exact normalizers and actual Kmat comparison'),
 ],
 'ktie_consumer':[
  f(F,'ParametersTermRelations',159,190,'All original FinX fields and actual term fibers'),
  f(F,'ParametersTermRelations',216,257,'Actual period, aT, fiber sum aR and sOf construction'),
  f(F,'ParametersTermRelations',335,355,'Full KTie and separate NormTie/IsoNorm interfaces'),
  f(F+'RootLatticeThresholds/','NormalizingConstantEq',233,267,'Original full kTie producer and finite-fiber absolute regrouping'),
  f(Q,'RelevantZeroGramTerms',335,347,'Literal dimPi, c0, normalized adjoint Kmat, KExpansion and KAbsConv'),
 ],
}
# Number, title, internal dependencies, source groups, inherited IDs, exact scope.
specs=[
 (1,'Full inverse-different triviality of every supplied additive character',[],['setting','character'],[],'Original PsiDd for arbitrary X and every original character; unitarity and local constancy are conclusions, with no continuity premise added.'),
 (2,'Rational Levi splitting and exact character product',[1],['levi','setting'],[],'Original stabilizers over F, every completion and finite adeles; exact rational psi product, including zero isotropic rank.'),
 (3,'Full UnipotentConjugateInLevel with its finite phase',[1,2],['finite_phase','setting'],['RCV12','ASG11'],'Every original finite unipotent in K0, actual xu and chi2 including the bw chain; inverse different handles all remaining places.'),
 (4,'Integral Levi extraction and exact smaller-level splitting',[2,3],['integral_levi'],[],'Every actual n,h with nh in K0; both factors preserve the actual fractional-ideal lattice and exact semidirect K2 intersection.'),
 (5,'Full original NeatKu at every finite column',[2],['neat','setting'],['ASG14'],'Every word, finite h and original character witness; finite order and both-prime unipotence, no prime-versus-rank or gap assumption.'),
 (6,'Actual sharp is an antilinear Hilbert coordinate bijection',[5],['columns'],[],'Original Cu, supplied ColReps and original ColT norm; evaluation has exactly the source Riesz orientation.'),
 (7,'Actual seed well-definedness, measurability, covariance and reproduction',[1,2,3,4],['seed'],['ASG14'],'Every original word and supplied hK; all finite decompositions and zero off support; no new compact-support premise for the reproducer.'),
 (8,'Rational unipotent density and strict column domains',[2],['density'],['RCV14'],'Full finite-adelic unipotent density and strict measurable domains for each actual column lattice; original adelic quotient retained.'),
 (9,'Exact column unipotent dictionary and finite phases',[2,3],['column_unipotents'],[],'Actual NOcol with unique rational lift and exact level/character, not a finite-index subgroup.'),
 (10,'All-section support cells and their exact product measure',[4,5,8,9],['slabs'],['ASG14'],'Every strict NOcol domain, nonnegative then integrable scalar functions, actual quotient and exactly one volK2 factor.'),
 (11,'Full general FoldBound and compact multiplicity finiteness',[],['fold_bound'],[],'General second-countable locally compact group with no Hausdorff premise, arbitrary left Haar, measurable averaging set and original null-measurable a.e. fundamental domain; compact Hausdorff refinement with Borel finite multiplicity.'),
 (12,'Full general finite, L2 and mixed Poincare identities',[11],['mixed_unfold'],[],'Full original group/domain/representative scopes, including null-measurable a.e. domains, precise a*A*J bound and absolute double-orbit unfolding; exact common FoldOK compact set for both words.'),
 (13,'Actual absolute slabs and single unfolding',[6,7,10,12],['slab_abs'],['ASG14'],'Every T,T-prime and every strict column domain; pre-integration absolute bound, original automorphic Hilbert inner product and finite volume.'),
 (14,'Complete original flag-return carrier and double quotient',[4,5,9],['return_carrier'],['ASG11'],'Full PD, including local convention, primitive lift, fixed ideal lattice and one integral upper unitriangular congruence matrix; ModG retains its exact localized scope.'),
 (15,'Full pointwise support reindexing and finite phase',[4,5,7,8,9,12,14],['support_reindex'],[],'Both scalar and absolute sums; exact ColCl quotient equals the actual right column-unipotent quotient at every infinite point.'),
 (16,'Exact orbit unfolding with every original section',[9,14,15],['orbit_unfold'],[],'Full original OrbitUnfold in the supplied setting, conditional on its stated absolute slab integral; arbitrary selected carrier and FundOf, all phase and Haar orientations retained.'),
 (17,'Exact TermVal and universal-scope EntryUnfold',[6,13,15,16],['term_entry'],[],'Actual Bochner rank-one integral and phase, original sqrt(c0*c0prime) inverse, zero convention and all term/block series; AbsConvT kept in full.'),
 (18,'Full original universal KExpansionC',[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17],['endpoint'],[],'Arbitrary D7, X, Full, both words, both FoldOK and InHH, FundExists, OOIntAll, OOFundIndep, AmpWellDef and full AbsConvT; no arithmetic gap or new positivity premise.'),
 (19,'Full period linearity and exact antilinear Gram transport',[6,7,18],['linear_transport'],[],'PuLinear under only its original InHH premise; ambient L2 adjoints, exact original ColT norm and zero-safe normalization; arbitrary source and target projections retain the correction term.'),
 (20,'Full original KTie on the supplied finite spectral datum',[6,17,19],['ktie_consumer','linear_transport'],[],'Arbitrary original FinX plus the two DimTie identities and original KExpansion/AbsConvT; actual finite fibers and normalized Kmat, no SIso or FinX existence inferred.'),
]
assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip() == PIN
files = {}
for path in sorted({e[0] for entries in groups.values() for e in entries}):
    data = subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
    assert (REPO/path).read_bytes() == data, path
    target = SNAPSHOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    files[path] = {'path':path,'snapshot_path':str(target.relative_to(WORK)),
        'source_commit':PIN,'sha256':sha(data),'bytes':len(data),
        'line_count':len(data.splitlines(keepends=True)),'url':URL+path,
        'verified_equal_to_pinned_git_blob':True}
source_groups = {}
for name, entries in groups.items():
    source_groups[name] = []
    for i,(path,first,last,declaration) in enumerate(entries,1):
        lines = (SNAPSHOT/path).read_bytes().splitlines(keepends=True)
        first,last = first or 1,last or len(lines)
        assert 1 <= first <= last <= len(lines),(path,first,last,len(lines))
        data = b''.join(lines[first-1:last])
        source_groups[name].append({'id':f'PGR_{name}_{i:02d}','path':path,
            'line_start':first,'line_end':last,'declaration':declaration,
            'file_sha256':files[path]['sha256'],'range_sha256':sha(data),
            'range_bytes':len(data),'source_commit':PIN,
            'verified_equal_to_pinned_git_blob':True,
            'url':URL+path+f'#L{first}-L{last}'})

main = (HERE/'main.tex').read_bytes()
lines = main.decode().splitlines(keepends=True)
old_claims = {}
if (HERE/'provenance.json').exists():
    old_claims = {c['id']:c for c in json.loads((HERE/'provenance.json').read_text())['claims']}
claims = []
for number,title,own,names,inherited_ids,scope in specs:
    identifier = f'PGR{number}'
    first = next(i for i,l in enumerate(lines,1) if l.strip()=='% BEGIN '+identifier)
    last = next(i for i,l in enumerate(lines,1) if l.strip()=='% END '+identifier)
    proof = ''.join(lines[first-1:last]).encode()
    assert b'\\begin{proof}' in proof and b'\\end{proof}' in proof
    status = 'complete human proof at the stated original scope; awaiting independent review'
    old = old_claims.get(identifier,{})
    if old.get('proof_location',{}).get('sha256') == sha(proof):
        status = old.get('status',status)
    claims.append({'id':identifier,'title':title,'introduced_in':VERSION,
        'classification':'B','status':status,
        'depends_on':[f'PGR{i}' for i in own]+inherited_ids,
        'external_input_ids':['PGR_CLASSICAL_BACKGROUND','PGR_ACTUAL_SUPPLIED_SETTING'],
        'published_input_ids':[],'scope_note':scope,'source_groups':names,
        'sources':[r for name in names for r in source_groups[name]],
        'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+identifier,
            'line_start':first,'line_end':last,'sha256':sha(proof),'bytes':len(proof)},
        'source_proof_is_not_human_proof':True,'whole_obligation_closure':False})

inherited, all_inherited = [],set()
for component,ids in {'adelic_setting_v47':['ASG11','ASG14'],'reference_covolume_v56':['RCV12','RCV14']}.items():
    data = (WORK/component/'main.tex').read_bytes()
    oldlines = data.splitlines(keepends=True)
    index = {c['id']:c for c in json.loads((WORK/component/'provenance.json').read_text())['claims']}
    bindings = []
    for identifier in ids:
        loc = index[identifier]['proof_location']
        selected = b''.join(oldlines[loc['line_start']-1:loc['line_end']])
        assert loc.get('sha256',loc.get('paragraph_sha256')) == sha(selected),identifier
        bindings.append({'id':identifier,'file':component+'/main.tex',
            'line_start':loc['line_start'],'line_end':loc['line_end'],
            'sha256':sha(selected),'bytes':len(selected),
            'scope':index[identifier].get('scope_note',index[identifier]['title'])})
        all_inherited.add(identifier)
    inherited.append({'component':component,'claims':ids,'file':component+'/main.tex',
        'sha256':sha(data),'proof_hashes':{b['id']:b['sha256'] for b in bindings},
        'claim_bindings':bindings})
known = {c['id'] for c in claims}|all_inherited
assert all(d in known for c in claims for d in c['depends_on'])

inputs=[
 {'id':'PGR_CLASSICAL_BACKGROUND','status':'ordinary mathematical background retained',
  'content':'Finite-dimensional linear algebra, Riesz representation and Hilbert adjoints; finite-dimensional norm equivalence; number-field integral lattices, local integrality, different/codifferent definitions and Chinese remaindering; additive approximation in finite adeles; basic topological groups and Haar integration; Tonelli, Bochner integration and absolutely convergent series. Exact finite characters, the rational Levi, column stabilizers, support/return dictionaries and all changes of quotient domain are proved in the manuscript.'},
 {'id':'PGR_ACTUAL_SUPPLIED_SETTING','status':'exact original supplied-data scope',
  'content':'Arbitrary D7 and supplied HidaSetting X, and every Full X record Y, with original coefficient isomorphisms, global character, actual infinity and finite Haar measures, wave functions, finite-level transports, rows and splitting, column representatives, coset representatives, both unipotent domains, typed reduction and local models. This chapter does not construct X or Full or infer Forms0.',
  'source_file':F+'PoincareConstantEq.lean','line_start':25,'line_end':50,'source_commit':PIN},
 {'id':'PGR_ORIGINAL_ANALYTIC_PREMISES','status':'exact named original premises retained in full',
  'content':'For each supplied ordered pair of words: FoldOK and InHH for both words; FundExists, OOIntAll, OOFundIndep and AmpWellDef for the same original rows, flags and columns; AbsConvT with its full three clauses (summable operator norms, summable auxiliary vector norms and positive Gam1). Original all-vector, all-domain, all-carrier and all-representative quantifiers are unchanged. FoldOK supplies the pre-integration bound; AbsConvT is used only after unfolding for operator series. PuLinear alone uses just its original InHH premise.',
  'source_file':F+'PoincareConstantEq.lean','line_start':118,'line_end':128,'source_commit':PIN},
 {'id':'PGR_FINX_DIMTIE','status':'exact named original consumer premises retained',
  'content':'Full KTie takes arbitrary supplied FinX Y, its complete original fields, DimTie at both words, original KExpansion and full AbsConvT. No FinX existence, SIso, source-family identification or additional period-range assertion is inferred. Other fields of FinX remain supplied even where not needed by this particular fiber regrouping.',
  'source_file':F+'ParametersTermRelations.lean','line_start':335,'line_end':342,'source_commit':PIN},
]
for c in claims:
    n=int(c['id'][3:])
    if n in [12,13,15,16,17,18,19]:
        c['external_input_ids'].append('PGR_ORIGINAL_ANALYTIC_PREMISES')
    if n==20:
        c['external_input_ids'].append('PGR_FINX_DIMTIE')
completed=[
 'Full original PsiDd for every supplied additive character, with unitarity and local constancy derived',
 'Original rational Levi, rational character product, integral KsetSplit and full UnipotentConjugateInLevel, including its exact phase',
 'Full original NeatKu for every finite h and level-character witness, with no arithmetic gap or prime-versus-rank hypothesis',
 'Actual antilinear sharp bijection, original ColT norm and complete scalar seed properties',
 'Actual finite unipotent density, NOcol dictionary and every-section SlabFD with the original product measure',
 'Full original general FoldBound without a Hausdorff premise; compact Hausdorff refinement proved separately',
 'Full original general PoincareSeriesFinite, PoincareSeriesMemLp and PoincareSeriesInner, with precise absolute and L2 bounds',
 'Actual SlabAbs, full flag-return PD, SupportReindex and OrbitUnfold on the supplied setting at original scopes',
 'Exact original TermVal and EntryUnfold, with the given rank-one integral, phase and normalizer',
 'Full universal original KExpansionC under all and only its original named analytic premises',
 'Full original PuLinear implication, exact antilinear normalized Gram identity, and projection correction formula',
 'Full original KTie under the supplied FinX, both DimTie identities and original KExpansion/AbsConvT',
]
remaining=[
 'FullExists and ambient Forms0/original all-family setting suppliers are not inferred',
 'Universal FoldOKC and InHHC producers, rather than their exact supplied premises used here',
 'FundExistsC, OOIntAllC, OOFundIndepC, AmpWellDefC and AbsConvC as independent global suppliers remain outside this endpoint',
 'Other original FinX fields, its existence and the actual coherent SIso/period range comparison remain supplied at the consumer',
 'JacGauge/RhsWLim, PlaceSplit, full ProdExact, RealBracket and independent mass/counting inputs remain separate',
 'Global operator bounds, actual family identifications, denominator/height inputs and final global spectral closure remain separate',
]
shared=[
 'One supplied D7, X and Full Y; no replacement setting or changed bridge',
 'One original global additive character, actual chi2 and both words with their xu and wave functions',
 'Original finite level K2, actual finite Haar measure and exactly one volK2 factor in slab integration',
 'Original infinity Haar measure, both muN/muH witnesses and both arbitrary FN domains in c0X',
 'Exact rows, fractional-ideal lattices, ColReps, both Dt transversals and actual rational RatLink',
 'Every prescribed GTerm representative and FundOf, including degenerate terms, with supplied all-section independence',
 'Original ColT inner product and antilinear sharp; source or target projection correction is retained',
 'At KTie, the same Y and FinX, actual sOf, both DimTie identities and actual finite toTerm fibers',
]
manifest={'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,
 'source_commit':PIN,'snapshot_root':str(SNAPSHOT.relative_to(WORK)),
 'checkout_head_verified':True,'source_files':list(files.values()),'total_files':len(files),
 'total_bytes':sum(x['bytes'] for x in files.values()),
 'distinct_source_ranges':len({(r['path'],r['line_start'],r['line_end']) for v in source_groups.values() for r in v}),
 'all_verified_equal_to_pinned_git_blob':True,'no_lean_replay':True,
 'source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof':True}
mathlib_pin='0df444a360eaa60ab8c11dca51a86af692955474'
mathlib_rel='Mathlib/MeasureTheory/Group/FundamentalDomain.lean'
mathlib_target=HERE/'supporting_sources/mathlib4'/mathlib_rel
mathlib_bytes=mathlib_target.read_bytes()
assert sha(mathlib_bytes)=='c5dbbd2d01d3f65dcfdb89b877268d836a162e5f0d0d0967d527ce5ec2473e67'
mathlib_dep=json.loads(subprocess.check_output(['git','-C',str(REPO),'show',PIN+':lake-manifest.json']))
assert next(x['rev'] for x in mathlib_dep['packages'] if x['name']=='mathlib')==mathlib_pin
mathlib_range=b''.join(mathlib_bytes.splitlines(keepends=True)[64:73])
supporting=[{'id':'PGR_MATHLIB_FUNDAMENTAL_DOMAIN','role':'exact imported definition; not a new analytic premise',
 'source_commit':mathlib_pin,'repository':'https://github.com/leanprover-community/mathlib4',
 'path':mathlib_rel,'snapshot_path':str(mathlib_target.relative_to(WORK)),
 'sha256':sha(mathlib_bytes),'bytes':len(mathlib_bytes),
 'line_start':65,'line_end':73,'range_sha256':sha(mathlib_range),'range_bytes':len(mathlib_range),
 'url':'https://github.com/leanprover-community/mathlib4/blob/'+mathlib_pin+'/'+mathlib_rel+'#L65-L73',
 'dependency_pin_verified_in_original_lake_manifest':True,
 'scope':'IsFundamentalDomain uses nullMeasurableSet and a.e. covering/disjointness; PGR11--12 preserve that full scope.'}]
for c in claims:
    if c['id'] in ['PGR11','PGR12']:
        c['supporting_source_ids']=['PGR_MATHLIB_FUNDAMENTAL_DOMAIN']
manifest['supporting_sources']=supporting
manifest['supporting_source_count']=len(supporting)
dump('supporting_sources.json',{'schema':'rh-supporting-source-bindings/1','component':COMPONENT,
 'proof_file_sha256':sha(main),'sources':supporting})
validation=json.loads((HERE/'tex_validation.json').read_text())
assert validation['proof_file_sha256']==sha(main) and validation['status']=='PASS'
reviews=[]
for path in sorted(HERE.glob('independent_review*.json')):
    value=json.loads(path.read_text())
    assert value.get('proof_file_sha256',value.get('main_tex_sha256',sha(main)))==sha(main)
    reviews.append({'file':str(path.relative_to(WORK)),'sha256':sha(path.read_bytes()),'content':value})
# This external manuscript is an acknowledged organizational starting point,
# not an additional mathematical premise or a substitute for the proof above.
brox_repo=WORK.parent/'post_proof_literature_20261124/external/brox_GRH_distillation'
brox_pin='fd38313e5c7018c3c988ba20510e6b0b3bca0519'
brox_path='paper/shared/global-gram-continuation-period-identity.tex'
brox_data=subprocess.check_output(['git','-C',str(brox_repo),'show',brox_pin+':'+brox_path])
brox_target=HERE/'external_reference'/'global-gram-continuation-period-identity.tex'
brox_target.parent.mkdir(exist_ok=True)
brox_target.write_bytes(brox_data)
external={'role':'acknowledged starting argument; no unproved external premise imported',
 'author':'Jose Brox','repository':'https://github.com/JoseBrox/GRH_distillation',
 'commit':brox_pin,'path':brox_path,
 'url':'https://github.com/JoseBrox/GRH_distillation/blob/'+brox_pin+'/'+brox_path,
 'snapshot_path':str(brox_target.relative_to(WORK)),'sha256':sha(brox_data),
 'bytes':len(brox_data),'source_scope_difference':'Brox installs an arithmetic-gap regime; PGR uses the exact universal original FoldOK/InHH/orbital/convergence premises instead.'}
dump('external_reference.json',external)
dump('source_manifest.json',manifest)
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'components':inherited,
 'all_current_proof_ranges_verified':True})
dump('classical_inputs.json',{'schema':'rh-explicit-inputs/1','component':COMPONENT,
 'inputs':inputs[:1],'new_unreconstructed_published_mathematical_premises':[]})
dump('retained_inputs.json',{'schema':'rh-retained-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'inputs':inputs,
 'unsupplied_new_mathematical_premises_inside_KExpansionC':[],
 'original_endpoint_is_an_implication_with_its_named_premises':True,
 'no_disguised_period_matching_or_unfolding_assumption':True,
 'remaining_downstream_boundaries':remaining})
dump('provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':VERSION,
 'date':'2026-11-24','component':COMPONENT,'source_commit':PIN,
 'main_tex_sha256':sha(main),'proof_file_sha256':sha(main),'claims':claims,
 'source_groups':source_groups,'source_files':list(files.values()),'source_inventory':list(files.values()),
 'retained_foundations':inputs,'inherited_human_inputs':inherited,'independent_reviews':reviews,
 'external_argument_acknowledgments':[external],'supporting_sources':supporting,
 'builder':COMPONENT+'/build_metadata.py','validation':validation,
 'whole_obligation_closures':[],'no_lean_replay':True})
dump('contracts.json',{'schema':'rh-root-producer-contracts/1','artifact_version':VERSION,
 'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':sha(main),
 'primary_endpoint_claim':'PGR18','endpoint_claim':'PGR18','next_consumer_claim':'PGR20',
 'completed_original_substatements':completed,
 'remaining_missing_proof_steps_in_KExpansionC':[],
 'retained_original_premises':[i for i in inputs if i['id']!='PGR_CLASSICAL_BACKGROUND'],
 'shared_data_preserved':shared,'remaining_downstream_boundaries':remaining,
 'proposed_whole_obligation_closures':[],'whole_obligation_closures':[],'no_lean_replay':True})
dump('closure.json',{'schema':'rh-component-closure/1','artifact_version':VERSION,'component':COMPONENT,
 'proof_file_sha256':sha(main),'human_claims':[c['id'] for c in claims],
 'fully_proved_claims_at_stated_scope':[c['id'] for c in claims],
 'completed_original_producer_contracts':completed,
 'conditional_consequences':['KExpansion for every supplied setting under the exact original KExpansionC premises',
  'Actual sOf KExpansion and KAbsConv under the exact original KTie premises'],
 'remaining_missing_proof_steps_in_KExpansionC':[],
 'retained_original_premises':[i['id'] for i in inputs[1:]],
 'remaining_downstream_boundaries':remaining,'whole_obligation_closures':[],
 'all_sources_pinned':True,'no_lean_replay':True})
dump('claim_dag.json',{'schema':'rh-claim-dependency-dag/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),
 'nodes':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims],
 'inherited_nodes':sorted(all_inherited),'all_dependencies_resolve':True})
(HERE/'report.txt').write_text(f'''The universal period Gram identity, version {VERSION}
Accepted source pin: {PIN}
Main SHA-256: {sha(main)}

Twenty detailed human proof blocks PGR1--PGR20; {len(main.decode().split())}
TeX words. PGR18 completes the FULL ORIGINAL KExpansionC, for arbitrary
D7, supplied HidaSetting X, Full Y and both words. The exact original
FoldOK/InHH hypotheses at both words, FundExists, OOIntAll, OOFundIndep,
AmpWellDef and AbsConvT remain its stated premises. No arithmetic gap,
new c0 positivity, special domain or changed Haar normalization is added.
PGR20 completes the full original KTie consumer with its supplied FinX,
two DimTie identities and original KExpansion/AbsConvT premises.

Substantive reconstruction: the supplied additive character annihilates
the completed inverse different; the actual finite K2 phase includes the
bw chain; rational and integral Levi splitting preserves the actual
fractional-ideal lattice. Both auxiliary primes kill every rational
compact column stabilizer. Original column evaluations therefore give
the antilinear sharp bijection with exactly the ColT norm.

Finite unipotent approximation and the actual lattice subgroup produce
strict support cells with no stabilizer factor and exactly one volK2.
The general FoldBound proof has no Hausdorff premise; its compact finite
multiplicity refinement and the original L2/mixed statements are at the
Hausdorff scope that those statements actually require. Null-measurable
a.e. fundamental domains are retained by measurable representatives and
countable translated null exceptions. One common
compact averaging set for both words gives the finite pre-integration
absolute bound. Operator-series summability is not used in its place.

The rational return carrier includes the COMPLETE PD predicate: lift,
local frame convention and primitivity, prescribed different-weighted
isotropic lattice, and one integral upper unitriangular congruence
matrix. ModG is kept at its original localized scope. The double
quotient, orbit stabilizer and every-section unfolding are exact.
Bochner evaluation of the original rank-one integral supplies the
phase-correct EntryUnfold. AbsConvT then supplies HasSum of the actual
operators. The literal sqrt(c0*c0prime) inverse is preserved even at its
zero convention, since unnormalized unfolding is proved first.

The normalized Gram operator is transported through the ANTILINEAR
Riesz maps. Arbitrary target projection retains its explicit correction.
For KTie, the exact common normalizers and finite toTerm fibers give
both operator HasSum and norm summability on the actual sOf datum.
No SIso or coherent family join is inferred from this identity.

Inherited human blocks: ASG11, ASG14, RCV12 and RCV14. Brox's pinned
period-Gram manuscript is acknowledged as an organizational starting
point, not an imported theorem or an extra assumption. The original
universal premises replace its installed arithmetic-gap regime.

Retained boundaries: Full/Forms0 existence; universal folding, range,
orbital and absolute-convergence suppliers; remaining FinX fields and
coherent SIso; JacGauge/RhsWLim, ProdExact, RealBracket, independent
mass/counting and global spectral bounds. No whole selected obligation
is closed; all 24 whole obligations remain open at this increment.

Bindings: {len(files)} pinned full source files, {manifest['distinct_source_ranges']}
exact ranges, {manifest['total_bytes']} source bytes; all 20 proof blocks
and four inherited blocks, plus the separately pinned imported Mathlib
fundamental-domain definition. Two-pass draft TeX PASS with zero diagnostics.
No PDF and no Lean replay. Independent review binds the frozen main and
individual proof/source ranges separately.
''')
(HERE/'README.txt').write_text('Read main.tex, contracts.json and retained_inputs.json.\n'
 'Draft TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n'
 'Build metadata: python build_metadata.py\nRead-only verification: python verify_hashes.py\n'
 'Refresh artifact inventory: python refresh_hashes.py\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'main_sha256':sha(main),
 'source_files':len(files),'source_ranges':manifest['distinct_source_ranges'],
 'source_bytes':manifest['total_bytes'],'inherited_blocks':len(all_inherited),
 'tex_status':validation['status'],'whole_obligation_closures':[]},indent=2))
