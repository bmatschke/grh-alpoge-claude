#!/usr/bin/env python3
"""Bind the RCV human manuscript to exact original contracts; no Lean replay."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.56'
COMPONENT = HERE.name
SNAPSHOT = HERE / 'source_snapshot'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
H = S + 'HaarTransversals/'
U = H + 'UnitaryHaarProducts/'
L = U + 'LocalWeightCharts/'
C = S + 'CokernelGLCounts/'
R = C + 'RankPointCounts/'
N = R + 'DualFamilyCounting/'
J = S + 'ClosedLocalOrbits/GaugeLatticeShifts/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def f(prefix, name, first=None, last=None, declaration='Original definition or producer; full pinned file retained for context'):
    return (prefix + name + '.lean', first, last, declaration)

groups = {
 'supplied_setting': [
   f(H,'HidaSetting',167,173,'latSpanS and aaD: exact fractional ideals'),
   f(H,'HidaSetting',179,227,'Actual coefficient isomorphism, lattice, hyperbolic vectors, Lb, Lam_split and word data'),
   f(H,'HidaSetting',285,298,'Actual local orthonormal frames and their perpendicular conditions'),
 ],
 'field_norms': [
   f(N,'EmbVHomInjective',20,68,'Actual embedding representatives, discriminant transport and extended-different norm'),
   f(N,'EmbVHomInjective',158,178,'Exact absNorm_aaD and nonzero return'),
   f(N,'NOfibCut',77,99,'Literal choice theta(D) and all-coordinate tauQ definitions'),
   f(N,'NOfibFibT',7,None,'Original ThetaEx producer'),
 ],
 'additive_domains': [
   f(N,'RealCovolume',41,100,'Coordinate cube and every strict additive domain'),
   f(N,'RealCovolume',102,208,'covol_of_gram at full nondegenerate real-form scope'),
   f(N,'EmbVHomInjective',80,156,'Exact generated subgroup and full idealBlock'),
 ],
 'self_dual': [
   f(N,'CovolBRb',63,153,'Original L0 unimodularity and trace-dual orthogonal-complement argument'),
   f(N,'CovolBRb',177,224,'Different times trace dual: both inclusions'),
   f(N,'CovolBRb',359,383,'Exact dual lattice and index of its full rank module'),
 ],
 'trace_determinant': [
   f(N,'CovolBRa',17,26,'aaLbS and full TrDetUnimod for arbitrary integer bases'),
   f(N,'CovolBRb',437,454,'Index of the specified ideal-scaled row lattice'),
   f(N,'CovolBRb',509,639,'DetHOne interface and original trace determinant assembly'),
   f(N,'TrDetPfH',68,None,'Complete original perfect-trace-pairing determinant producer'),
   f(N,'CovolBRc',9,13,'Original trDetUnimod_holds and row/block producer endpoints'),
 ],
 'row_coordinates': [
   f(N,'NcRealXCC',76,101,'Exact blk, rowV, aaLb and four cLat definitions'),
   f(N,'RowParseval',1,None,'Full original RowParseval statement'),
   f(N,'PjRowPars',17,49,'Actual supplied frame row Parseval producer'),
   f(N,'TraceReHolds',15,24,'Trace is twice the real-part sum at the chosen places'),
   f(N,'RowRankHolds',18,None,'Full integer-rank and basis supplier for aaLb'),
 ],
 'row_covolume': [
   f(N,'CovolBR',15,26,'Full RowBlockCovol: countability, existence, every domain'),
   f(N,'RowBlockCovolOf',50,66,'Real row quadratic form and its exact determinant weights'),
   f(N,'RowBlockCovolOf',68,170,'Complete original rowBlockCovol_of producer'),
 ],
 'complex_ideal_blocks': [
   f(N,'EmbVHomInjective',180,None,'Full X and K block statements and norm exponents'),
   f(N,'NcRealXCC',93,113,'Exact block lattices and all four cVal formulas'),
 ],
 'imaginary_block': [
   f(N,'ReImESymmAdd',31,117,'Exact ideal square, extension and contraction'),
   f(N,'ReImESymmAdd',119,163,'Integral trace-one element and real-part identity'),
   f(N,'ReImESymmAdd',203,212,'Exact half-trace fractional ideal'),
   f(N,'ReImESymmAdd',246,365,'Real projection and anti-invariant imaginary kernel'),
   f(N,'ReImESymmAdd',468,501,'Existence of a strict diagonal-block domain'),
   f(N,'ReImESymmAdd',525,681,'Degree, half-ideal norm, every-domain diagonal covolume and BlockCovol assembly'),
 ],
 'block_contract': [
   f(N,'NcRealXCC',16,74,'Block spaces, product Lebesgue measures and exact heights'),
   f(N,'NcRealXCC',141,None,'Full original BlockCovol'),
 ],
 'polynomial_chart': [
   f(H,'HidaSetting',24,34,'Actual InN: flag, z and whole perpendicular-space conditions'),
   f(L,'NilpotentChartRightInverse',247,282,'Original standard chart parameters, phi0 and readings'),
   f(N,'CovolumeExponent',16,44,'Actual matrix readings and half-open box'),
   f(N,'CovolNOfSteps',13,37,'CIdx, kappa and full CoordMeas'),
   f(N,'NcRealXKS',55,126,'Original local reconstruction and full KapSurj'),
 ],
 'triangular_law': [
   f(N,'NcRealXCC',66,74,'Exact source cHgt'),
   f(N,'NcRealXCC',115,128,'Full KapLaw and KapSurj contracts'),
   f(N,'NcRealXKL',108,170,'Actual grouped block law and multiplication readings'),
   f(N,'NcRealXKL',693,None,'Full kapLaw_holds producer and identity correction'),
 ],
 'finite_level': [
   f(H,'HidaSetting',86,123,'Original mL/InAt/Nfin/K2cong and K2set'),
   f(H,'HidaSetting',236,281,'Original finite frame congruences, xu_fix/xu_z/xu_K'),
   f(U,'HermitianETransportInvariant',350,380,'GoodC and one common clearing integer coprime to g'),
   f(U,'HermitianETransportInvariant',426,507,'Exact integral-span coefficient descent'),
   f(U,'HermitianETransportInvariant',548,684,'Three congruence families and full unipotent_conj_mem_level'),
 ],
 'arithmetic_dictionary': [
   f(H,'PoincareInHH',254,255,'Literal NOinf with finite conjugate K2 condition'),
   f(N,'NOfibCut',103,107,'Exact full NOratC and RatLink scope'),
   f(N,'NOfibRat',23,130,'Rational-finite lattice equivalence and full noratC_holds'),
 ],
 'rational_coordinates': [
   f(N,'NOfibCut',22,75,'Q/M/x/G, DataOK, LatQ, NFl and blkQ definitions'),
   f(N,'NOfibCut',109,124,'Original DictGram, DictLat, DictEx and DictPlace'),
   f(N,'NOfibAlg',159,247,'Exact rational row identity, Gram relation and DictGram producer'),
   f(N,'InvMulOfUnitri',34,148,'Full arbitrary-DataOK rational reconstruction'),
   f(N,'NOfibPl',51,None,'Full dictionary_place_holds on actual rational adelic pair'),
 ],
 'lattice_preservation': [
   f(N,'NOfibLatF',76,134,'Necessity of ideal and row conditions, including inverse action'),
   f(N,'NOfibLatB',30,45,'Actual perpendicular component of nf'),
   f(N,'NOfibLatB',57,169,'Unitriangular inverse ideal bounds and full sufficiency'),
 ],
 'shifted_fibers': [
   f(N,'NOfibCut',77,99,'Literal theta choice and tauQ on all inputs'),
   f(N,'NOfibCut',126,188,'Full FibQ/FibOnto/ThetaEx and lower-height assembly'),
   f(N,'NOfibOnto',50,182,'Exact row/imaginary subgroup images and every-tuple rational lift'),
   f(N,'NOfibFibC',1,None,'Original nofib_holds endpoint'),
   f(N,'NcRealXCC',130,139,'Full NOfib: subgroup, shifted fibers, strict lower dependence'),
 ],
 'triangular_domains': [
   f(R,'CoordCovolOfCut',16,106,'Every ambient domain, triangular cut and product measure'),
   f(R,'CoordCovolOf',1,None,'Original coordCovol_of supplier chain'),
   f(H,'HidaSetting',141,145,'Exact ambient IsSFund and weak Haar contracts'),
   f(N,'CovolNOfSteps',43,47,'Full CoordCovol exact return'),
 ],
 'constant_product': [
   f(N,'NcRealXCV',48,77,'The four exact exponent sums'),
   f(N,'NcRealXCV',90,None,'Literal cVal_prod and covolN/twoU return'),
   f(N,'CovolumeExponent',46,58,'Exact covolumeExponent, covolN and full CovolN'),
   f(N,'CovolNOfSteps',33,47,'twoU and all-Haar/all-domain coordinate statements'),
 ],
 'haar_scope': [
   f(N,'NcRealXHU',16,None,'Weak supported Haar uniqueness without extra normalization'),
   f(N,'NcRealXLeb',469,509,'Actual coordinate Haar and full covolN_of_coordCovol'),
   f(H,'HidaSetting',141,145,'Every original ambient domain and Haar witness'),
 ],
 'lie_normalization': [
   ('src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean',379,397,'Exact realify, lieOf, real span lieE and haarLie definition'),
   f(N,'NcRealXECPfA',15,29,'Linear Lie chart, ShearStep and ConstStep exact scopes'),
   f(N,'NcRealXECPfA',124,159,'Lie conditions and root weights'),
   f(N,'NcRealXECPfC',136,145,'Exact normLm factor'),
   f(N,'NcRealXECPfC',204,211,'Literal realified Euclidean norm'),
   f(N,'NcRealXECPfC',275,300,'Exact determinant and full constant_change_holds'),
 ],
 'exponential_chart': [
   f(N,'NcRealXEC',12,15,'Full original ExpChart'),
   f(N,'NcRealXECPfA',150,177,'Positive root-height coordinates'),
   f(N,'NcRealXECPfB',151,184,'Global triangular exponential shear and measure preservation'),
   f(N,'NcRealXECPf',12,None,'Exact exponential_chart_haar assembly'),
 ],
 'local_reference': [
   f(N,'NcRealPf',63,65,'Literal refN comap of prescribed haarLie'),
   f(N,'NcRealXPlace',15,21,'General-rank refNg definition'),
   f(N,'NcRealXPlace',113,None,'Full original refNg_isHaarLoc: arbitrary z perpendicular to e'),
   f(N,'RefNMapKapL',15,37,'Exact row-scaling determinant and full refN_map_kapL statement'),
   f(N,'RefNMapKapL',150,None,'Actual reference scalar and final coordinate density'),
 ],
 'independent_words': [
   f(N,'FrameRow',16,None,'Full FrameRow at every supplied word pair and all ambient group elements'),
   f(N,'PjFrameRow',165,255,'Actual common-complement basis change and norm-square determinant'),
   f(N,'PjFrameRow',306,382,'Real row determinant and complete frameRow_holds'),
 ],
 'reference_box': [
   f(N,'NcRealXPS',106,140,'Actual rank, refNX and frame identities'),
   f(N,'NcRealXCR',15,33,'RefNBox with independent u,w and refNX_haar'),
   f(N,'RefNBoxOf',15,75,'Full independent-word reference-box computation'),
 ],
 'covolref_endpoint': [
   f(N,'NcRealXCR',35,87,'Every-word/every-domain covol_refN and full CovolRef assembly'),
   f(N,'NcRealXPS',169,174,'Exact original CovolRef statement'),
   f(C,'MassDataInst',229,231,'Literal HypX: two original independent arithmetic domains'),
   f(S+'ClosedVolumeStatements/','RealBracketOfRowBlock',35,37,'CovolRef_outright exact named endpoint'),
 ],
 'next_consumer_context': [
   f(J,'JacConst',57,67,'Exact JacGauge coefficient and all-section retained next target'),
   f(J,'JacConstWbB',59,64,'Exact RhsWLim next supplier'),
   f(N,'NcRealPf',98,107,'Full ProdExact with arbitrary sigma-finite local factors'),
   f(N,'NcRealPf',159,217,'Original full RealBracket join'),
   f(N,'NcRealXPS',176,178,'placeSplit_of consumes JacGauge and CovolRef'),
   f(N,'NcRealXPS',265,267,'Next realBracket_of_jac join'),
 ],
}

# Identifier, title, local dependencies, source groups, inherited dependencies, exact scope.
specs = [
 (1,'Actual discriminants, extended ideals and source trace-one choice',[],['field_norms'],['ASG2'],'Actual D7 host and supplied field isomorphism; original theta(D); no replacement field or unramifiedness premise.'),
 (2,'Every-domain Euclidean and ideal covolumes',[],['additive_domains'],[],'Every nonzero fractional ideal and every measurable strict additive domain; chosen embeddings and real/imaginary normalization retained.'),
 (3,'Full self-duality of the supplied orthogonal-complement lattice',[],['supplied_setting','self_dual'],[],'Actual possibly nonprincipal Lb and original unimodular L0; rank, full span and direct decomposition proved.'),
 (4,'Full original TrDetUnimod in arbitrary integer bases',[3],['trace_determinant'],[],'Stronger all nonzero fractional-ideal scaling statement; original arbitrary basis/dimension witnesses recovered exactly.'),
 (5,'Exact row realification, rank and Parseval identity',[3],['row_coordinates'],[],'All words and supplied orthonormal frames; conjugate-linear in the vector, real linear after scalar extension.'),
 (6,'Full original RowBlockCovol',[1,2,4,5],['row_covolume','row_coordinates'],[],'Countable actual row subgroup, domain existence and exact volume for every measurable strict domain.'),
 (7,'Both original complex ideal-block covolumes',[1,2],['complex_ideal_blocks'],[],'Every upper pair, original ideal ratios/products and every strict additive domain.'),
 (8,'Complete anti-invariant diagonal-block covolume',[1,2],['imaginary_block'],[],'Exact trace kernel and half-trace projection; includes residue characteristic two and every supplied domain.'),
 (9,'Full original BlockCovol',[6,7,8],['block_contract','complex_ideal_blocks'],[],'All four original blocks, actual coordinate order and all three quantified output fields.'),
 (10,'Full original coordinate chart, KapSurj and CoordMeas',[3,5],['polynomial_chart','supplied_setting'],[],'Actual full unipotent group and ambient Borel coordinate readings; global polynomial reconstruction, including zero rank.'),
 (11,'Full KapLaw and exact coordinate left/right Haar invariance',[10],['triangular_law'],[],'Corrections depend strictly on lower source block heights in both inputs, with every measurable polynomial coordinate and zero-argument property.'),
 (12,'Full original unipotent_conj_mem_level',[3],['finite_level'],[],'Every actual finite N intersection K element; all three literal K2 congruences on original Lf; no character equality or PsiDd premise.'),
 (13,'Full original NOratC',[10,12],['arithmetic_dictionary'],[],'Actual GFset pair and RatLink, finite xu-conjugate K2 condition and original L0; both directions with no auxiliary arithmetic subgroup.'),
 (14,'Full DictGram, DictEx and DictPlace',[3,5,10],['rational_coordinates'],[],'Every arbitrary rational DataOK tuple, exact first-variable conjugation and actual adelic placement.'),
 (15,'Full original DictLat',[3,14],['lattice_preservation','rational_coordinates'],[],'Both directions of actual lattice equality, including inverse-row condition and all matrix ideal entries.'),
 (16,'Full original FibQ, FibOnto and NOfib',[1,5,13,14,15],['shifted_fibers'],[],'Literal theta(D) and tauQ on all coordinate tuples; rational tuple equivalence, every admissible real tuple lift, subgroup fields and exact lower-height dependence.'),
 (17,'Every original fundamental domain has the product coordinate covolume',[9,10,11,13,16],['triangular_domains'],[],'Actual shifted-fiber subgroup, explicit strict rectangular domain, every original ambient IsSFund, and image measurability.'),
 (18,'Exact product constants and full original CoordCovol',[17],['constant_product'],[],'All Tw, powers of two and discriminant exponents, including zero rank and original covolN/twoU return.'),
 (19,'Full original CoordHaar and CovolN',[10,11,18],['haar_scope','constant_product'],['AMD8'],'Every original weak sigma-finite supported Haar normalization and every ambient strict arithmetic domain; finite positive masses are conclusions.'),
 (20,'Full original ConstStep and exact Lie volume factor',[],['lie_normalization'],[],'Arbitrary nonnegative k,r; literal realified lieE defined by all exponential paths, exact Euclidean determinant 2^(r^2+rk).'),
 (21,'Full original ShearStep and ExpChart',[10,11,20],['exponential_chart'],[],'Arbitrary k,r; global polynomial exponential/chart shear has determinant one, preserving literal haarLie with no scalar parameter.'),
 (22,'Full original local reference coordinate measure',[10,11,21],['local_reference'],[],'All n,r,k and rank-equality/signature/frame witnesses, any T>0; source AE measurability and exact density; Haar support for every z-prime perpendicular to e.'),
 (23,'Full original FrameRow and ambient coordinate transport',[5],['independent_words'],[],'Every independent word pair and supplied local frames; identity on all ambient group elements, stronger matrix identity, exact determinant (Tw/Tu)^r.'),
 (24,'Full original RefNBox and refNX_haar',[22,23],['reference_box'],[],'Reference u and box/lattice w independent; same prescribed reference measure, all places, exact Tw^(-rd)*2^(d(rk+r^2)).'),
 (25,'Full original covol_refN and CovolRef',[18,19,24],['covolref_endpoint','next_consumer_context'],[],'Every supplied X/bridge/HypX, both actual domains and independent words; no retained supplier inside CovolRef, no selected whole-obligation closure.'),
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
        source_groups[name].append({'id':f'RCV_{name}_{i:02d}','path':path,
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
    identifier = f'RCV{number}'
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
        'depends_on':[f'RCV{i}' for i in own]+inherited_ids,
        'external_input_ids':['RCV_CLASSICAL_BACKGROUND','RCV_ACTUAL_SUPPLIED_SETTING'],
        'published_input_ids':[],'scope_note':scope,'source_groups':names,
        'sources':[r for name in names for r in source_groups[name]],
        'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+identifier,
            'line_start':first,'line_end':last,'sha256':sha(proof),'bytes':len(proof)},
        'source_proof_is_not_human_proof':True,'whole_obligation_closure':False})

inherited, all_inherited = [],set()
for component,ids in {'adelic_setting_v47':['ASG2'],'adelic_measures_v48':['AMD8']}.items():
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

inputs = [
 {'id':'RCV_CLASSICAL_BACKGROUND','status':'ordinary mathematical background retained',
  'content':'Elementary finite-dimensional Hermitian and real linear algebra; number-field rings of integers as Dedekind domains, local freeness of finite projective lattices, different/codifferent definitions and integral trace discriminants; elementary finite-index determinants, real scalar extension and local integrality; Lebesgue change of variables, Tonelli and countable additivity. The exact trace determinant, diagonal factor, rational lattice dictionary, group chart, fundamental domains and reference normalization are proved in this manuscript rather than retained as inputs.'},
 {'id':'RCV_ACTUAL_SUPPLIED_SETTING','status':'exact original supplied-data scope',
  'content':'An arbitrary original D7 and supplied HidaSetting with its literal coefficient isomorphism, actual unimodular L0 and Lam_split, hyperbolic vectors, all word vectors/local frames, finite frame congruences and xu. The CovolRef conclusion accepts every original bridge, both domains and HypX. This does not construct the ambient setting or infer Forms0. No extra measure, covolume, level-membership, row-lattice or discriminant hypothesis is imposed.',
  'source_file':H+'HidaSetting.lean','line_start':179,'line_end':328,'source_commit':PIN},
]
completed = [
 'Full original TrDetUnimod, including every supplied integer basis of aaLb',
 'Full original RowBlockCovol and BlockCovol, all three output fields for all four blocks',
 'Full original unipotent_conj_mem_level at the actual supplied finite adelic lattice, without PsiDd or character premises',
 'Full original NOratC with actual GFset/RatLink and finite xu-conjugate K2 condition',
 'Full original DictGram, DictEx, DictPlace, DictLat, FibQ, FibOnto and NOfib',
 'Full original KapSurj, CoordMeas, KapLaw, CoordCovol, CoordHaar and CovolN',
 'Full original ConstStep, ShearStep and ExpChart for arbitrary nonnegative k,r',
 'Full original refN_map_kapL and refNg_isHaarLoc at every allowed local frame and witness',
 'Full original FrameRow, RefNBox and refNX_haar with independent reference and lattice words',
 'Full original covol_refN and CovolRef, including every original ambient domain/bridge/HypX',
]
remaining = [
 'Original local JacGauge/all-section disintegration, including exact RhsWLim or another fully proved supplier with the same measure constants',
 'Exact PlaceSplit consumer and full ProdExact for arbitrary sigma-finite local factorizations, then RealBracket with the already supplied AprimeInf/GaugeDens interfaces',
 'Independent finite-place factors, remaining mass/index/counting/form fields and exact global spectral identifications',
 'Ambient Forms0 and original all-family Transport/LevelMatch, Bessel uniqueness/local ties and coherent final joins',
]
shared = [
 'Same supplied D7/HidaSetting, coefficient isomorphism and actual place/embedding witnesses',
 'Original full unimodular lattice L0, specified aaD ideals, Lb and all hyperbolic/frame vectors',
 'Actual finite xu and K2 conditions in NOinf, exact rational GFset/RatLink, no auxiliary arithmetic subgroup',
 'Every original weak Haar and ambient strict fundamental-domain witness in CovolN',
 'Literal haarLie(Nset,1) reference measure with its realified Euclidean norm and exact frame pullback',
 'Reference word u and box/lattice word w independent; same reference u on both final domains',
 'Supplied global character, actual infinity measures and bridge remain unchanged; their existence/normalization is not inferred from the reference calculation',
]
manifest = {'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,
 'source_commit':PIN,'snapshot_root':str(SNAPSHOT.relative_to(WORK)),
 'checkout_head_verified':True,'source_files':list(files.values()),'total_files':len(files),
 'total_bytes':sum(x['bytes'] for x in files.values()),
 'distinct_source_ranges':len({(r['path'],r['line_start'],r['line_end']) for v in source_groups.values() for r in v}),
 'all_verified_equal_to_pinned_git_blob':True,'no_lean_replay':True,
 'source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof':True}
validation = json.loads((HERE/'tex_validation.json').read_text())
assert validation['proof_file_sha256']==sha(main) and validation['status']=='PASS'
reviews = []
for path in sorted(HERE.glob('independent_review*.json')):
    value = json.loads(path.read_text())
    assert value.get('proof_file_sha256',value.get('main_tex_sha256',sha(main)))==sha(main)
    reviews.append({'file':str(path.relative_to(WORK)),'sha256':sha(path.read_bytes()),'content':value})
dump('source_manifest.json',manifest)
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'components':inherited,
 'all_current_proof_ranges_verified':True})
dump('classical_inputs.json',{'schema':'rh-explicit-inputs/1','component':COMPONENT,
 'inputs':inputs[:1],'new_unreconstructed_published_mathematical_premises':[]})
dump('retained_inputs.json',{'schema':'rh-retained-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'inputs':inputs,
 'unsupplied_original_producers_inside_CovolRef':[],
 'no_disguised_volume_or_lattice_dictionary_premise':True,
 'remaining_downstream_boundaries':remaining})
dump('provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':VERSION,
 'date':'2026-11-23','component':COMPONENT,'source_commit':PIN,
 'main_tex_sha256':sha(main),'proof_file_sha256':sha(main),'claims':claims,
 'source_groups':source_groups,'source_files':list(files.values()),'source_inventory':list(files.values()),
 'retained_foundations':inputs,'inherited_human_inputs':inherited,'independent_reviews':reviews,
 'builder':COMPONENT+'/build_metadata.py','validation':validation,
 'whole_obligation_closures':[],'no_lean_replay':True})
dump('contracts.json',{'schema':'rh-root-producer-contracts/1','artifact_version':VERSION,
 'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':sha(main),
 'primary_endpoint_claim':'RCV25','endpoint_claim':'RCV25',
 'completed_original_substatements':completed,
 'remaining_exact_producers_for_CovolRef':[],
 'retained_original_premises':['Arbitrary original D7 and supplied HidaSetting; literal HypX only in its original final consumer scope'],
 'shared_data_preserved':shared,'remaining_downstream_boundaries':remaining,
 'proposed_whole_obligation_closures':[],'whole_obligation_closures':[],'no_lean_replay':True})
dump('closure.json',{'schema':'rh-component-closure/1','artifact_version':VERSION,'component':COMPONENT,
 'proof_file_sha256':sha(main),'human_claims':[c['id'] for c in claims],
 'fully_proved_claims_at_stated_scope':[c['id'] for c in claims],
 'completed_original_producer_contracts':completed,
 'conditional_consequences':[],
 'remaining_source_producers_inside_CovolRef':[],
 'remaining_downstream_boundaries':remaining,'whole_obligation_closures':[],
 'all_sources_pinned':True,'no_lean_replay':True})
dump('claim_dag.json',{'schema':'rh-claim-dependency-dag/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),
 'nodes':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims],
 'inherited_nodes':sorted(all_inherited),'all_dependencies_resolve':True})
(HERE/'report.txt').write_text(f'''Reference unipotent covolume, version {VERSION}
Accepted source pin: {PIN}
Main SHA-256: {sha(main)}

RCV1--RCV25 are twenty-five complete detailed human proof blocks, with
{len(main.decode().split())} TeX words. The endpoint is full original CovolRef,
not only an implication retaining a row-lattice or arithmetic subgroup
supplier. Every original supplied HidaSetting is accepted. Reference word u
and lattice word w remain independent, as do the two final domain witnesses.

The arithmetic proof shows that the actual orthogonal complement Lb is
Hermitian self-dual, computes its trace dual and determinant in every integer
basis, and obtains every row/complex/imaginary block covolume. The imaginary
block uses the integral trace-one split sequence, so its factor at two is
explicit. The actual finite K2 condition is proved by localizing at one
clearing integer coprime to g and descending modulo g; no PsiDd or character
identity is assumed. This supplies the full rational subgroup dictionary.

Explicit rational coordinates and their inverse prove both lattice
preservation directions and every shifted-fiber lift. The group law is
triangular at the exact source heights. A product of block parallelotopes
is an actual strict domain; countable translation partitions return every
other original ambient domain, without presuming finite mass. Coordinate
Haar uniqueness keeps every original normalization in CovolN.

The source's realified Lie metric has factor 2^(r^2+rk), and the exponential
to polynomial chart is a global triangular measure-preserving shear. Row
rescaling has determinant T^r. Between independent word frames the exact
determinant is (Tw/Tu)^r on all ambient group elements. Thus the reference
box mass is Tw^(-rd)*2^(d(rk+r^2)), and its product with the coordinate
lattice covolume cancels Tw and 2 exactly. Each domain has reference mass
Delta^(-(8r^3+6r^2+6kr^2+r)/6); the final pair has exponent twice this.

Inherited: ASG2 and AMD8 only. All underlying measures, words, original
coefficient/embedding/frame/lattice choices and the bridge are preserved.
Actual GMR/SVW InVolumes was already complete and is not reproved or
identified with this independent reference-volume result.

Open after this endpoint: exact local JacGauge/RhsWLim, PlaceSplit and the
full product disintegration consumer, then RealBracket; independent finite
mass/counting/form and global spectral producers remain explicit. No whole
selected obligation is newly closed, and Forms0 is not inferred.

Bindings: {len(files)} complete pinned source blobs, {manifest['distinct_source_ranges']}
distinct exact ranges, {manifest['total_bytes']} source bytes; 25 proof blocks,
two inherited blocks. Two-pass draft TeX PASS with zero diagnostics.
No PDF and no Lean replay. Independent review is bound separately to the
frozen manuscript and every individual proof block.
''')
(HERE/'README.txt').write_text('Read main.tex, contracts.json and retained_inputs.json.\n'
 'Draft TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n'
 'Build metadata: python build_metadata.py\nRead-only verification: python verify_hashes.py\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'main_sha256':sha(main),
 'source_files':len(files),'source_ranges':manifest['distinct_source_ranges'],
 'source_bytes':manifest['total_bytes'],'inherited_blocks':len(all_inherited),
 'tex_status':validation['status'],'whole_obligation_closures':[]},indent=2))
