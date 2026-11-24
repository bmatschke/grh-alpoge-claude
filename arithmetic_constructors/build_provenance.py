#!/usr/bin/env python3
"""Reproduce AC provenance from pinned Git blobs; do not alter source checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=ROOT.parents[1] / 'lean-source')
args = parser.parse_args()
REPO = args.repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GP = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
IP = 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
DP = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
AM = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
WC = 'src/Development/AutomorphicArithmetic/WeightCongruences/'
LC = 'src/Formalism/LocalRingCardinality/'
HC = 'src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/'
PAIR = DP + 'PairRowIffQdRows.lean'
TRANS = DP + 'SetUnipotentTranslate.lean'
DU = AM + 'DuStarPos.lean'
RAW = HC + 'ConjEMemHostFIff.lean'
FRAME = HC + 'ZsmulGeneratorEqZeroOfProjection.lean'
SHIFT = WC + 'ExistsShiftWeightCongruenceLtTorsionOrder.lean'
NORM = WC + 'NormRootOfUnityQuadraticSubfield.lean'
PROD = WC + 'ProdCmTypeEqNormAndWeightCongruenceOne.lean'
MU = WC + 'ProdNegOneZpow.lean'
INT = WC + 'IsRootOfIntegral.lean'
HCP = GP + 'ExistsHcParamOfCode.lean'
LEVEL = IP + 'ModEqOneOfNorm.lean'
blob_cache = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(path):
    if path not in blob_cache:
        raw = subprocess.check_output(['git', '-C', str(REPO), 'show', COMMIT+':'+path])
        if (REPO/path).is_file():
            assert (REPO/path).read_bytes() == raw, ('modified checkout', path)
        blob_cache[path] = raw
    return blob_cache[path]


prefix = r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
boundary = re.compile(prefix + r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option|attribute|include|omit)\b|^@\[')


def source(path, spelling, namespace='', role='literal source conclusion or definition'):
    raw=blob(path); lines=raw.splitlines(keepends=True)
    txt=[s.decode().rstrip('\r\n') for s in lines]
    pat=re.compile(prefix+r'(?:theorem|lemma|def|abbrev|structure)\s+'+re.escape(spelling)+r'(?=\s|\{|\(|:)')
    hits=[i for i,s in enumerate(txt) if pat.search(s)]
    if len(hits)>1 and namespace:
        def ns_at(index):
            stack=[]
            for line in txt[:index]:
                m=re.match(r'^namespace\s+(\S+)',line)
                if m:
                    stack.append(('namespace',m.group(1)))
                elif re.match(r'^section(?:\s|$)',line):
                    stack.append(('section',None))
                elif re.match(r'^end(?:\s|$)',line) and stack:
                    stack.pop()
            return '.'.join(v for k,v in stack if k=='namespace')
        hits=[i for i in hits if ns_at(i)==namespace]
    assert len(hits)==1, (path,spelling,hits)
    a=hits[0]; b=a+1
    while b<len(lines) and not boundary.match(txt[b]):
        b+=1
    while b>a+1 and not txt[b-1].strip():
        b-=1
    r=b''.join(lines[a:b])
    decl=(namespace+'.'+spelling if namespace else spelling).removeprefix('_root_.')
    url=f'{URL}/blob/{COMMIT}/{path}#L{a+1}-L{b}'
    return dict(path=path,declaration=decl,source_spelling=spelling,
        line_start=a+1,line_end=b,sha256=sha(raw),full_file_sha256=sha(raw),
        range_sha256=sha(r),range_bytes=len(r),first_line=txt[a],
        declaration_lines_within_range=[a+1],url=url,pinned_url=url,role=role,
        verified_equal_to_pinned_git_blob=True)


def many(path,names,namespace='',role='literal source conclusion or definition'):
    return [source(path,n,namespace,role) for n in names]


def file_record(path):
    raw=blob(path)
    return dict(path=path,sha256=sha(raw),bytes=len(raw),lines=len(raw.splitlines()),
        commit=COMMIT,url=f'{URL}/blob/{COMMIT}/{path}',verified_equal_to_pinned_git_blob=True)


claims=[]

def claim(i,title,statement,deps,sources,assumptions):
    cid='AC'+str(i)
    claims.append(dict(id=cid,title=title,statement=statement,depends_on=deps,
        status='derived_simplification',mathematical_status='proved_under_explicit_hypotheses',
        introduced_in='0.15',proof_location=dict(file='arithmetic_constructors/main.tex',
        expanded='arithmetic_constructors/report.txt',section=cid),assumptions=assumptions,
        sources=sources))

claim(1,'A bounded shift makes all root products trivial',
    'For any finite family of field embeddings and integer weights, changing a single chosen weight by q with 0<=q<torsionOrder(E) makes the product one on every root of unity.',
    ['SZ10'],
    [source(SHIFT,'UpperTheory.exists_shift_weightCongruence_lt_torsionOrder')]
    +many(MU,['MU','MUQ'],'UpperTheory')
    +many(INT,['exists_shift'],'UpperTheory.Mu'),
    ['E is a number field; a finite family of embeddings into a field and a chosen index are supplied.',
     'Cyclotomic degree and the elementary finite multiplicative subgroup argument are explained; no parity-only substitute is used.'])

claim(2,'Prove the quadratic norm of every root is one',
    'If d>3 is prime, s^2=-d, K=Q(s), and 4 divides [E:Q], then N_E/K(z)=1 for every root of unity z; the 2-primary norm is proved through K(i).',
    [],
    many(NORM,['minpoly_eq','finrank_eq','repr_mem','sq_cases','rat_nsq','exists_neg_one',
               'd_nsq','neg_nsq','two_nsq','odd_root','two_pow_norm'],
               'UpperTheory.RootOfUnityNormQuadraticSubfield')
    +[source(NORM,'UpperTheory.norm_root_of_unity_quadratic_subfield')],
    ['E is a number field containing sqrt(-d), d is prime >3, and 4|[E:Q].',
     'Only elementary quadratic-field arithmetic, cyclotomic degree and field norm identities are used.',
     'HostDer.norm_mu, ramification and class-number assertions are not premises of this proof.'])

claim(3,'The actual host CM product permits all parallel integer shifts',
    'The host subgroup Psi is exactly Gal(E/K); its embedding product is the norm, so MU(1) and then MU(a+c) and the literal integral MUQ lift hold.',
    ['AC2'],
    many(PROD,['fixK','sigma_sqd','galK','galK_bij'])
    +[source(PROD,'UpperTheory.prod_cmType_eq_norm_and_weightCongruence_one')]
    +many(INT,['mu_one','mu_const','muq_of_parallel'],'UpperTheory.Mu')
    +many(MU,['add','const','add_const'],'UpperTheory.MU')
    +many(RAW,['HostRaw'],'Formalism.HC','literal raw host Galois and square-root data')
    +many(RAW,['K'],'Formalism.HC.HostRaw')
    +many(FRAME,['GG','Psi','mem_Psi_iff','natCard_GG'],'Formalism.HC.Frame')
    +many(LC+'DataHost.lean',['sigmaOf','emb'],'Formalism.BasicNotions.Host'),
    ['An actual host with its raw Galois isomorphism and gal_sqd is supplied.',
     'The subgroup is the kernel of the second sign, not an arbitrary CM type.',
     'The norm-one property is proved by AC2 rather than assumed from HostDer.norm_mu.'])

claim(4,'Construct all thirteen HCParam fields by formulas',
    'The explicit arithmetic progressions and Boolean interior shifts satisfy both strict interlacings, the strict bottom bound, both gaps and all integrality/half-integrality fields.',
    [],
    [source(HCP,'exists_hcParam_of_code','GlobalTheory.EX')]
    +many(LC+'Params.lean',['Ranks','HCParam'],'Formalism.BasicNotions'),
    ['R is the actual Ranks record; D>=1, h>=(t+3)/2, 4D(k-2)<=U0, UL<0 and -B<=UL.',
     'The Boolean code is prescribed; no replacement of endpoint integers occurs.'])

claim(5,'Uniform column numerical prerequisites',
    'For fixed epsilon,cD>=0,ch>=402, a common threshold gives D>=1, (t+3)/2<=h, 4kD<=a, k<=bprime/x and all three scale positivities before any host or column is chosen.',
    ['RF11','RF12'],
    [source(HCP,'hc_sizes','GlobalTheory.EX')]
    +many(PAIR,['Delv','h0v','RankVal'],'GlobalTheory.EX')
    +many(LC+'DataParams₂.lean',['Scale'],'Formalism.BasicNotions')
    +many(LC+'DataParams₂.lean',['a','b',"b'","X'","w''"],'Formalism.BasicNotions.Scale'),
    ['0<epsilon<1/52, cD>=0, ch>=402; every later rank record satisfies the literal RankVal.',
     'The threshold is independent of s,R,H,top weights and Boolean words.'])

claim(6,'One simultaneous compatible column family with full MUQ',
    'The single bounded correction at a thick place produces HCVal for every word and height, with exact top, thick and thin bases, the five word-independent functions, and the prescribed Boolean interior code.',
    ['AC1','AC3','AC4','AC5'],
    [source(HCP,'exists_hc_family','GlobalTheory.EX')]
    +many(PAIR,['HostVal','HCVal'],'GlobalTheory.EX')
    +many(LC+'DataHost.lean',['topPlaces','thickPlaces','IsThin'],'Formalism.BasicNotions.Host')
    +many(FRAME,['dig','tau1','tau2','iota_bijective'],'Formalism.HC.Frame')
    +[source(LC+'RankBoundMonotoneInDimension.lean','factTopsThick','Formalism.BasicNotions')],
    ['An actual host with HostVal and prescribed integer top weights aT>=a,bT>=bprime is supplied.',
     'Any finite reindexing of the actual Psi is permitted.',
     'Only a thick place is shifted; the strict torsionOrder upper bound and all top/thin values are preserved.'])

claim(7,'Complete the literal chGood_of_host constructor',
    'From the supplied HostGood, WinOK, rank, CT2 and injective code inputs, construct the actual translated PreCh and all sixteen ChOK fields, hence ChGood, with one uniform threshold.',
    ['AC5','AC6','RF11'],
    many(TRANS,['setUnipotentTranslate','GamS','ChOK','ChGood','leastOff','leastOff_eq_rPrH',
                'chGood_of_host'],'GlobalTheory.EX.OB')
    +many(DP+'ThinScalesIffHostBound.lean',['HostGood','WinOK'],'GlobalTheory.EX')
    +many(DU,['PreCh'],'GlobalTheory.Mem')
    +many(DP+'AuxiliaryPrimeMemAvoidedPrimes.lean',['rPrH','q0H','globalTwisting_spec_fact'],
          'GlobalTheory.EX.DC')
    +many(GP+'KitExOfHostWeightObj.lean',['small_prime_lt','X\'_le_b'],'GlobalTheory.EX')
    +many(PAIR,['HostVal','HostArith','Std'],'GlobalTheory.EX')
    +many(PAIR,['log_cond_le'],'GlobalTheory.EX.HostVal'),
    ['The full literal HostGood, WinOK and supplied injective code of the ceiling cardinality are retained.',
     'The actual q0H is already prime under HostGood; this implies its defining natural-infimum set is nonempty and supplies its stronger modulus.',
     'The prescribed unipotent translate is set before the column correction; no host-existence theorem is inferred.'])

claim(8,'An explicit integral norm-form equivalence',
    'A NormOne integer solution gives pi=(A+B sqrt(-d))/2=1+M(v+u omega), integral in K, norm p and congruent to one modulo M; the half-integral coordinate converse and divisor congruence are also proved.',
    [],
    [source(GP+'NormOnePrimeElements.lean','normOne_host','GlobalTheory.EX')]
    +many(IP+'NormOneIffOfSqrt.lean',['half_int_coords','exists_rat_coords','normOne_iff_of_sqrt','normOne_iff_host'],
          'GlobalTheory.Mem.An')
    +[source(IP+'NormOneModEqOneAndOfDvd.lean','_root_.GlobalTheory.Mem.An.normOne_modEq_one_and_of_dvd')]
    +many('src/Development/AbelianVarietyTheory/Definitions/Foundations/RayPrimes.lean',
          ['NormOne'],'GlobalTheory.Mem.An')
    +many(DP+'LogCondLeThree.lean',['NormOne'],'GlobalTheory.EX')
    +many('src/Formalism/LocalToGlobal/GlobalTheory/IsResidueClassZero.lean',['CongOne'],'Formalism.L2.GlobalTheoryTheory.Arith'),
    ['d is prime with d=3 mod4; the supplied square root and conjugation have their actual host meaning.',
     'The proof constructs the integral element; no prime-distribution or splitting-existence assertion is used.'])

claim(9,'All fifteen LevCh fields and the actual enlarged host',
    'Given the literal per-word prime/norm/congruence/window solutions and positive du,Ds,Gam, construct LevCh with exact parameter equalities and extend its host level set.',
    [],
    many(LEVEL,['mod_eq_one_of_norm','exists_levCh'],'GlobalTheory.Mem.LevelChoice')
    +many(DU,['LevCh','LevCh.host','LevCh.piT_ne'],'GlobalTheory.Mem'),
    ['The actual per-word prime solutions with the full modulus Nc*(g0*g1)^2 and both pde exclusions are supplied.',
     'du>0, Ds>0, Gam>1 and the literal multiplicative window are preserved.',
     'No pairwise distinctness of level primes is assumed or required.'])

claim(10,'Complete exists_levCh_of_levelPrime with exact quantifier order',
    'Under the retained analytic LevelPrime, ChOK and the prescribed positive du,Ds and logarithmic window, produce the actual LevCh with the same du,Ds,Gam at a threshold independent of cD,ch,words and discriminant data.',
    ['RF11','RF12','AC8','AC9'],
    [source(GP+'ExistsLevChOfLevelPrime.lean','exists_levCh_of_levelPrime','GlobalTheory.EX.OB')]
    +many(DP+'LogCondLeThree.lean',['LevelPrime','ModRow','modRow_host','HostVal.log_cond_le_three',
                                  'HostVal.modRow'],'GlobalTheory.EX')
    +many(TRANS,['ChOK','GamS'],'GlobalTheory.EX.OB')
    +many(LC+'DataHost.lean',['Host'],'Formalism.BasicNotions')
    +many(LC+'Params.lean',['Ranks'],'Formalism.BasicNotions')
    +many(LC+'Params.lean',['r'],'Formalism.BasicNotions.Ranks')
    +many(PAIR,['HostVal','RankVal'],'GlobalTheory.EX'),
    ['LevelPrime is an explicit analytic input and is not proved in this component.',
     'du,Ds and the logarithmic lower window are supplied, with the exact GamS C s R.',
     'The threshold is chosen after epsilon,cs,C and before cD,ch,s,P,du,Ds and all words.',
     'The simultaneous recursive global geometry and the independent RH/GRH branches remain separate.'])

# Exact record-field audit. Extract names from the pinned declarations, including
# the bracketed Fintype field in PreCh. These are interface checks, not Lean tests.
expected_fields={
    'HCParam':(LC+'Params.lean','Formalism.BasicNotions',
        ['u','v','b','e','u_gt_v','v_gt_u','u_last_gt','gap_be','gap_eb','e_int','u_half','v_int','b_int'],'AC4'),
    'PreCh':(DU,'GlobalTheory.Mem',
        ['R','H','ccK_top','level_cond','BB_disj','Word','wordFin','u₀','hcW','hcW_v','hcW_b','hcW_e','hcW_first','hcW_last'],'AC7'),
    'ChOK':(TRANS,'GlobalTheory.EX.OB',
        ['rank','ct2','val','arith','thick','dlog','gnorm','pde','small','lev','win','card','inj','hc','code','top'],'AC7'),
    'ChGood':(TRANS,'GlobalTheory.EX.OB',['ok','host'],'AC7'),
    'LevCh':(DU,'GlobalTheory.Mem',
        ['T','T_prime','T_cond','piT','piT_K','piT_norm','piT_cong','T_ne_pde','duStar','duStar_pos',
         'Dstar','Dstar_pos','GamP','one_lt_gammaP','T_win'],'AC9'),
}
record_audit=[]
for name,(path,ns,expected,cid) in expected_fields.items():
    s=source(path,name,ns)
    lines=blob(path).decode().splitlines()[s['line_start']-1:s['line_end']]
    fields=[]
    for line in lines:
        m=re.match(r'^  (?:\[)?([^\s:()\[\]]+)\s*(?:\([^\n]*?\)\s*)?:',line)
        if m:
            fields.append(m.group(1))
    assert fields==expected,(name,fields,expected)
    record_audit.append(dict(record=ns+'.'+name,fields=fields,count=len(fields),proved_by=cid,source=s))

main=(ROOT/'main.tex').read_text()
ids=re.findall(r'\\paragraph\{(AC\d+):',main)
assert ids==[c['id'] for c in claims],ids

retained=[
    source(DP+'ThinScalesIffHostBound.lean','HostGood','GlobalTheory.EX','actual supplied arithmetic and analytic host properties'),
    source(DP+'ThinScalesIffHostBound.lean','WinOK','GlobalTheory.EX','prescribed supplied top windows'),
    source(PAIR,'RankVal','GlobalTheory.EX','actual rank hypothesis; SZ13 supplies ranks in the prescribed-frame window'),
    source(PAIR,'Std','GlobalTheory.EX','fixed constant compatibility'),
    source(DP+'LogCondLeThree.lean','LevelPrime','GlobalTheory.EX','retained analytic short-interval norm-prime existence'),
    source(TRANS,'RecEx','GlobalTheory.EX.OB','separate simultaneous recursive-global geometry; not proved by AC'),
]
completed=[]
for cid, path,name,ns in [
    ('AC1',SHIFT,'UpperTheory.exists_shift_weightCongruence_lt_torsionOrder',''),
    ('AC2',NORM,'UpperTheory.norm_root_of_unity_quadratic_subfield',''),
    ('AC3',INT,'muq_of_parallel','UpperTheory.Mu'),
    ('AC4',HCP,'exists_hcParam_of_code','GlobalTheory.EX'),
    ('AC5',HCP,'hc_sizes','GlobalTheory.EX'),
    ('AC6',HCP,'exists_hc_family','GlobalTheory.EX'),
    ('AC7',TRANS,'chGood_of_host','GlobalTheory.EX.OB'),
    ('AC8',GP+'NormOnePrimeElements.lean','normOne_host','GlobalTheory.EX'),
    ('AC8',IP+'NormOneIffOfSqrt.lean','normOne_iff_of_sqrt','GlobalTheory.Mem.An'),
    ('AC9',LEVEL,'exists_levCh','GlobalTheory.Mem.LevelChoice'),
    ('AC10',GP+'ExistsLevChOfLevelPrime.lean','exists_levCh_of_levelPrime','GlobalTheory.EX.OB'),
]:
    s=source(path,name,ns,'completed literal constructor or prerequisite')
    s.update(completed_by=cid,human_status='proved_under_explicit_hypotheses',
        remaining_human_scope='none within the literal conditional conclusion')
    completed.append(s)

all_sources=[s for c in claims for s in c['sources']]
paths=sorted({s['path'] for s in all_sources})
proof_hashes={n:sha((ROOT/n).read_bytes()) for n in ['main.tex','report.txt']}
frontier=dict(
    rf10_constructor_targets_closed=['GlobalTheory.EX.OB.chGood_of_host',
        'GlobalTheory.EX.OB.exists_levCh_of_levelPrime'],
    column_family='complete under the literal HostVal and prescribed lower top weights',
    host_norm_mu='proved from raw host degree and quadratic data; not a retained premise',
    literal_record_field_counts={r['record']:r['count'] for r in record_audit},
    analytic_LevelPrime='retained input; no existence theorem proved here',
    host_and_weights='HostGood, WinOK and injective code remain supplied at chGood_of_host',
    du_Dstar_window='positive data and logarithmic lower window remain supplied at level construction',
    simultaneous_recursive_geometry='retained separate RecEx/RecExP supply',
    numerical_parameters='completed separately by PN/SZ; not repeated by AC',
)
payload=dict(schema='readable-rh-claim-provenance',artifact_version='0.15',repository=URL,commit=COMMIT,
    scope='Complete conditional column and level constructors, including actual root-congruence and integral norm proofs; retains actual HostGood, top windows/code, analytic LevelPrime and the recursive discriminant window.',
    claims=claims,source_files=[file_record(p) for p in paths],
    input_boundaries=[
        'AC7 starts from supplied HostGood, WinOK, RankVal, CT2 and injective code of the prescribed cardinality.',
        'AC2-AC3 prove the norm-one and parallel MUQ prerequisites; HostDer.norm_mu is not retained as a premise.',
        'The q0H stronger congruence follows from the natural infimum definition and its supplied primality.',
        'AC10 retains analytic LevelPrime and positive du,Ds with their exact logarithmic window; it preserves all three endpoint equalities.',
        'No arithmetic host, good weights, simultaneous recursive forms, RecExP, positive pairing or spectral branch is constructed here.',
        'No Lean build or PDF compilation was performed; proof/source interface audits are mathematical and byte-level.',
    ],
    constructor_frontier=frontier,record_field_audit=record_audit,
    retained_input_interfaces=retained,proof_file_sha256=proof_hashes,
    validation=dict(claims=len(claims),source_links=len(all_sources),source_files=len(paths),
        exact_inclusive_ranges=True,pinned_bytes_verified=True,
        record_fields_checked=sum(r['count'] for r in record_audit),record_counts_checked=True,
        lean_build=False,pdf_compiled=False,source_files_modified=False))
next_data=dict(artifact_version='0.15',repository=URL,commit=COMMIT,
    status='Both RF10 arithmetic constructor targets and their substantive prerequisites are proved under exact inputs.',
    targets=[],completed_targets=completed,retained_input_interfaces=retained,
    constructor_frontier=frontier,
    cross_component_scope='Root tracks the retained HostGood/weights/code, LevelPrime, recursive discriminant window and simultaneous global geometry suppliers; AC creates no duplicate shared target.',
    source_files=[file_record(p) for p in sorted({s['path'] for s in completed+retained})],
    validation=dict(target_count=0,completed_target_count=len(completed),
        rf10_constructor_targets_closed=2,pinned_bytes_verified=True))
for name,data in [('provenance.json',payload),('next_targets.json',next_data)]:
    (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(
    f"{c['id']} {s['declaration']} [{s['role']}]\n"
    f"{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}\n"
    f"full_sha256={s['full_file_sha256']}\nrange_sha256={s['range_sha256']}"
    for c in claims for s in c['sources'])+'\n')
print(json.dumps(payload['validation']))
print(json.dumps(next_data['validation']))
