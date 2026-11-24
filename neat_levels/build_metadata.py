#!/usr/bin/env python3
"""Bind the NTL proofs to their exact pinned original contracts.

Portable invocation:
  python build_metadata.py --source /path/to/lean_source \
    --human-root /path/to/reconstruction_v040 --peer-root /path/to/work_v041

Only this component directory is written.  No Lean build or replay occurs.
The mathematical proof is independent of an inherited or peer producer.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
p.add_argument('--human-root', type=Path, default=HERE.parent.parent/'reconstruction_v040')
p.add_argument('--peer-root', type=Path, default=HERE.parent)
args = p.parse_args()
REPO, HUMAN, PEER = args.source.resolve(), args.human_root.resolve(), args.peer_root.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=REPO, text=True).strip() == PIN

B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
H = B+'HeckeAlgebras/'
O = H+'OrdinaryHeckeCharacters/'
W = B+'WeilGroupCharacters/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
AV = 'src/Development/AbelianVarietyTheory/'
NT = O+'NtExpand.lean'
SPECS = [
 ('EXP',NT,12,24,'nt_expand: truncated binomial expansion in an arbitrary ring'),
 ('STEP',NT,28,60,'nt_step: q=p and q!=p divisibility cases over the original local domain'),
 ('TORS',NT,62,99,'nt_prime and nt_mat: all prime orders and all positive finite orders'),
 ('DISC',NT,115,136,'nt_sq: the original rational discriminant hypothesis'),
 ('VALUATION',NT,107,113,'nt_le and nt_val: exact completion valuation normalization'),
 ('LOCAL',NT,138,203,'nt_free: every original Kc(1) element of finite order'),
 ('COMPACT',NT,205,212,'nt_pow: any element of any compact subgroup has a positive integral power'),
 ('CHAR',NT,214,231,'nt_char: integral characteristic coefficients of a local compact conjugate'),
 ('CM',NT,237,261,'nt_int: original CM involution and one chosen place over each real-field place'),
 ('FINITE',NT,263,302,'nt_fin: integral characteristic polynomial, all-power unitarity and finite order'),
 ('ORD',NT,304,322,'nt_ord: local compact conjugates of M and M inverse yield global integrality'),
 ('UNDER',NT,324,332,'nt_under and nt_nat: exact prime contraction and rational-integer membership'),
 ('RAT',NT,334,351,'nt_rat: same rational matrix, all-power unitarity and every finite coordinate'),
 ('SEC',NT,363,399,'nt_sec, nt_cmp, nt_out and nt_Q: original sections including the trivial fallback'),
 ('IWA',NT,403,410,'nt_Iw: full original product Iwahori subgroup lies in the integral product'),
 ('JOIN',NT,417,474,'neatU local identities, product of compact-level powers and complete place partition'),
 ('AUX',NT,433,446,'neatU actual distinguished place, original p and its separation from ell'),
 ('KILL',NT,475,487,'neatU exact auxiliary-coordinate torsion kill, M=1 and both stabilizer factors'),
 ('TARGET',NT,412,487,'Entire original UpperTheory.V.Hi.neatU, with all QData, tau0 and K'),
 ('SETTING',W+'ContinuousResP.lean',63,117,'HidaSetting, original auxiliary prime, S, Vl and full Lev record'),
 ('SETTING',W+'ContinuousResP.lean',140,162,'Original V.frame coefficient-prime places and literal field projections'),
 ('FRAME',H+'ContinuousTorusCharacter.lean',151,174,'Frame, exact Neat and exact Free predicates'),
 ('IWA_DEF',H+'ContinuousTorusCharacter.lean',110,114,'Literal Iw=N join T join Nm and I1'),
 ('GROUPS',H+'IsTheta.lean',54,92,'Original away image, cmp including ell fallback, Ub, locA and sec'),
 ('QDATA',H+'IsTheta.lean',94,119,'QData, distinct underlying places, range and actual UQ'),
 ('HSET',H+'IsTheta.lean',121,143,'Every actual hset group/frame/section/representation field'),
 ('LEVEL',H+'CoefficientRepTrivialOnUnramified.lean',18,28,'GLw, product GV and original iwS'),
 ('LEVEL',H+'CoefficientRepTrivialOnUnramified.lean',75,120,'HSet, its exact X, all compact-open Lev inputs and generated level'),
 ('LEVEL',H+'CoefficientRepTrivialOnUnramified.lean',152,165,'Actual coefficient representation and all-level IsWt consumer'),
 ('KDEF',H+'TcAnti.lean',55,71,'Product Iwahori subgroup fields and original principal congruence Kc'),
 ('KDEF',H+'TcAnti.lean',94,100,'Original glData N, T, Tc and Nm, no extra factorization premise'),
 ('IWA_DEF',H+'Distinct.lean',19,24,'glIwa and piIwa retain these literal subgroup fields'),
 ('KODEF',AV+'Definitions/Foundations/MatrixMeasurableSpace.lean',18,29,'Original KO is the integral GL image; KOne'),
 ('TORUS',AV+'Definitions/TwistedInnerProducts/IsSubquotientDetRepParInd.lean',460,474,'Original torusO is coordinatewise valuation-one units'),
 ('RATDEF',AV+'PublishedTheorems/GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',66,84,'Literal conjAd, identity-form UA, cLoc and ratU'),
 ('RATDEF',AV+'PublishedTheorems/GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',165,172,'conjAd_algebraMap: exact rational CM involution compatibility'),
 ('RATDEF',AV+'Definitions/AutomorphicMembership/DifferentiableAtChart.lean',93,93,'ratGL is the actual adelic diagonal matrix map'),
 ('RATDEF','src/Formalism/SatakeDualWeyl/Statement.lean',9,49,'Formalism.UG.cT and UJ: exact Hermitian matrix equation'),
 ('CONSUMER',D+'TThetaEx.lean',152,180,'Neat-to-Free and exact full theta/IsWt consumer, owned by the companion'),
 ('CONSUMER',D+'HdEx.lean',20,27,'Original UnitaryHeckeData assembly retains the type supplier'),
 ('OUTER',D+'LinkTwo.lean',13,51,'Two original Links with common kappa and the original distinct auxiliary primes'),
 ('OUTER',D+'PotentialModularityTower.lean',38,66,'Original fixed-iota and one common eventual coefficient threshold'),
 ('OUTER',D+'THidaU.lean',38,48,'Same ideal joint Hida and HasAut endpoint remains outside neatU'),
]

cache, sources, groups = {}, [], {}
for group,path,first,last,decl in SPECS:
    if path not in cache:
        raw=(REPO/path).read_bytes()
        assert raw == subprocess.check_output(['git','show',f'{PIN}:{path}'],cwd=REPO),path
        cache[path]=raw
    raw=cache[path]; lines=raw.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines),(path,first,last,len(lines))
    block=b''.join(lines[first-1:last])
    item=dict(id=f'NTL_SRC_{len(sources)+1:03}',group=group,path=path,
      declaration=decl,line_start=first,line_end=last,sha256=sha(raw),
      full_file_sha256=sha(raw),range_sha256=sha(block),range_bytes=len(block),
      source_commit=PIN,
      url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{first}-L{last}')
    sources.append(item); groups.setdefault(group,[]).append(item['id'])

CG={
 1:['EXP'],2:['STEP'],3:['TORS'],4:['DISC','VALUATION'],
 5:['LOCAL','KDEF','KODEF'],6:['COMPACT','KODEF'],7:['CHAR','VALUATION'],
 8:['CM'],9:['FINITE'],10:['FINITE'],11:['ORD'],
 12:['RAT','RATDEF'],13:['SEC','GROUPS','QDATA','HSET','LEVEL'],
 14:['IWA','IWA_DEF','KDEF','KODEF','TORUS','LEVEL'],
 15:['UNDER','AUX','SETTING','GROUPS'],
 16:['JOIN','UNDER','SETTING','FRAME','GROUPS','QDATA','HSET','LEVEL'],
 17:['TARGET','KILL','FRAME','SETTING','HSET','LEVEL','CONSUMER','OUTER'],
}
DEP={
 1:[],2:['NTL1'],3:['NTL2'],4:['NTL3'],5:['NTL3','NTL4'],
 6:[],7:[],8:[],9:[],10:['NTL9'],11:['NTL7','NTL8','NTL10'],
 12:[],13:[],14:[],15:[],
 16:['NTL6','NTL11','NTL12','NTL13','NTL14','NTL15'],
 17:['NTL5','NTL12','NTL15','NTL16'],
}
HYP={
 1:['Any unital ring, one element and every nonnegative exponent; no commutativity of the ring.'],
 2:['Commutative local domain; original auxiliary odd rational prime p is nonzero and nonunit; any rational prime q, any k>=0 and any matrix size.'],
 3:['The same domain is Noetherian; every positive finite exponent, not merely order prime to p. Principal-ideal separation is proved directly.'],
 4:['Number field E, rational prime p not dividing the original discriminant, and the supplied place w over p. Local discrete valuation and the discriminant implication are justified in the text.'],
 5:['The exact original Kc(1) image, odd p, p not dividing disc(E), w over p and finite order. No replacement of the maximal ideal by (p) before NTL4.'],
 6:['Any compact subgroup of the actual local GL and any element of it; exponent may depend on the element and level. No normality of the integral intersection.'],
 7:['The same rational M and actual completion; conjugacy into integral GL, not merely integral matrix entries without inverse.'],
 8:['CM field with its actual involution; one place T(v) above each real-field place; both x and its CM conjugate locally integral.'],
 9:['One fixed number field and one bound on every complex embedding; every element is an algebraic integer.'],
 10:['Integral characteristic coefficients and c_L(M^a)^t M^a=1 for every a; exact finite rank n.'],
 11:['The same M and all-power unitarity; one chosen T(v) above every v with a local conjugate in integral GL; no equality T(v)=s.w(v) required.'],
 12:['The literal rational subgroup ratU for the identity Hermitian form, not an arbitrary reductive or indefinite group.'],
 13:['Literal QData.inj, notS and range; original UQ, sec and subgroup join; sec may be the trivial homomorphism in its fallback branch.'],
 14:['Literal glData N/T/Nm and their product; full Iwahori factorization is not assumed.'],
 15:['Original HidaSetting fields, same valuation subring over w(v) and v, #k(v0)=p, p prime and p!=ell, and level as a subgroup of original Ub.'],
 16:['One actual stabilizer relation, every original compact-open K_q, finite Q, exact levels and original Iw(0); the finite product exponent is internal to that relation.'],
 17:['All original neatU structures and hypotheses; n>=1, every QData, every Coef, every m and integral tau0, and every compact-open level family K. No TypeForAlt, HSet.Ax, Hecke module or ideal existence assumption.'],
}

tex=(HERE/'main.tex').read_bytes(); texlines=tex.splitlines(keepends=True)
def proof_block(cid):
    a=[i for i,l in enumerate(texlines) if l.strip()==f'% BEGIN {cid}'.encode()]
    b=[i for i,l in enumerate(texlines) if l.strip()==f'% END {cid}'.encode()]
    assert len(a)==len(b)==1 and a[0]<b[0],cid
    block=b''.join(texlines[a[0]:b[0]+1])
    return dict(line_start=a[0]+1,line_end=b[0]+1,sha256=sha(block),bytes=len(block)),block.decode()

claims=[]
for i in range(1,18):
    cid=f'NTL{i}'; pb,block=proof_block(cid)
    assert f'\\label{{claim:{cid}}}' in block
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    claims.append(dict(id=cid,title=title,introduced_in='0.41',classification='B',
      status='complete human proof at the printed exact scope',depends_on=DEP[i],
      classical_inputs=[],original_hypotheses=HYP[i],hypotheses_retained=HYP[i],
      proof_location=dict(file='neat_levels/main.tex',label='claim:'+cid,**pb),
      source_groups=CG[i],sources=[x for x in sources if x['group'] in CG[i]],
      dependency_scope=('Entire original neatU with every original QData, integral tau0 and compact-open K; no extra existence premise.' if i==17 else
       'The complete printed elementary/moderate implication; source theorem names locate the endpoint and do not replace its proof.')))
known={c['id'] for c in claims}
assert all(d in known for ds in DEP.values() for d in ds)
# Independent arithmetic reconstruction: there are no newly imported published applications.
dump('published_applications.json',[])

closed=[
 dict(id='ORIGINAL_KC_ONE_TORSION_FREE',classification='B',by=['NTL1','NTL2','NTL3','NTL4','NTL5'],
  scope='Every finite-order element of original Kc(1) at the supplied odd rational prime unramified by the original discriminant condition is the identity, in arbitrary matrix rank.',
  conditional_inputs='Exactly p prime, p!=2, p not dividing disc(L), supplied w over p, and original Kc(1) membership.'),
 dict(id='ORIGINAL_RATIONAL_STABILIZER_FINITE_ORDER',classification='B',by=[f'NTL{i}' for i in range(6,17)],
  scope='Every stabilizer relation in the original HSet at any original compact-open auxiliary level has a rational matrix of finite order.',
  conditional_inputs='The original HidaSetting, QData, level and frame; compactness at each added place and the literal Iw(0).'),
 dict(id='ORIGINAL_NEATU',classification='B',by=[f'NTL{i}' for i in range(1,18)],
  scope='Full UpperTheory.V.Hi.neatU: every original ell,L,Omega,s,n>=1,V,Q,c,m,tau0 and every K:(hset Q tau0).Lev.',
  conditional_inputs='Only the original datum and hypotheses in NtExpand.lean:412-414; no extra unproved supplier.'),
]
remaining=[
 dict(id='ORIGINAL_TTHETAEX',classification='B',status='separate companion producer, not claimed by neat_levels alone',
  remaining_contract='Construct one complete-coefficient torus character satisfying exact IsTheta and ContChar, then use NTL17 for Free at every K; owned by ordinary_theta_weight.'),
 dict(id='ORIGINAL_ORDINARY_CONTROL_TYPE',classification='C',status='unchanged outside this component',
  remaining_contract='Integral TypeForAlt, remaining HSet.Ax fields, actual ordinary/control module and Hecke algebra, continuous determinant and separating arithmetic fibers.'),
 dict(id='COUNT_II_SUPPORT',classification='C',status='not closed by this component',
  remaining_contract='Original joint Hida/P1 support for both rank-four Links, fixed iota and one common coefficient threshold, with actual same J within each ring; four remaining Hida endpoints and all-level same-J HasAut remain along with their original arithmetic/cohomological inputs.'),
]
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.41',component='neat_levels',
 source_commit=PIN,proof_sha256=sha(tex),proof_file_sha256=sha(tex),
 proof_claims=[c['id'] for c in claims],closed=closed,remaining=remaining,
 classical_input_nodes=[],
 sufficient_rules=[dict(conclusion='ORIGINAL_NEATU',logic='PROVED_UNIVERSAL',
  requires=['CERT_NTL1_NTL17'],
  binding='Every original HidaSetting and QData, arbitrary integral tau0, all compact-open K, actual frame/level/sections. The input HidaSetting itself is supplied, not newly constructed.')],
 nonlogical_shared_links=[
  dict(source='NTL17',target='ORIGINAL_TTHETAEX_ISWT',
   reason='Universal all-level neatness is consumed after one theta is chosen; the companion owns character construction and Neat-to-Free.'),
  dict(source='NTL17',target='COUNT_II_SUPPORT',
   reason='Shared for each of the two original rank-four Links; no ideal, coefficient threshold or automorphic module is selected here.'),
 ],
 not_claimed_closed=['TypeForAlt','remaining HSet.Ax','ordinary/control','arithmetic fiber existence',
   'four original Hida endpoints','same-J HasAut/TWAut','full original CohP','LocCFT',
   'COUNT_II_SUPPORT','TThetaEx by this component alone'],
 quantifier_guards=[
  'The auxiliary prime is exactly s.p: odd, different from ell and prime to disc(L); it is not chosen from the matrix rank.',
  'No ell>n condition and no n! inversion; the permitted rank-four ell=3 case is included.',
  'The integral representation tau0 is arbitrary, including m=0, with no type or smoothness premise.',
  'Every original QData and every compact-open auxiliary level K are covered; the Q empty case uses the empty product 1.',
  'The exact sec fallback is allowed; no local section bijectivity or HSet.Ax is silently assumed.',
  'The integral power e_q is chosen inside one stabilizer relation; it introduces no outer eventual threshold.',
  'A place w_q need not equal s.w(v_q); the CM integrality lemma uses the actual chosen place over each v.',
  'The exact original Neat conclusion is u=1 and b=1 in the given stabilizer equation.',
  'Both rank-four Links, fixed iota and one common coefficient threshold remain unchanged.',
  'No ideal J or automorphic module is constructed or replaced by neatU.',
 ],
 elementary_background=['Finite-dimensional field linear algebra and characteristic polynomials.',
  'The chapter reconstructs integral-basis finiteness, the local DVR argument, the relevant discriminant implication, principal-ideal separation and bounded algebraic-integer finiteness.',
  'Basic field completion and matrix-group definitions are retained; no new published theorem is imported.'],
 formal_correctness_assumed=True,new_lean_build=False,
 peer_review='pending independent final-byte mathematical/source review')
dump('closure.json',closure)
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.41',date='2026-11-22',
 source_commit=PIN,component='neat_levels',main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),
 claims=claims,source_groups=groups,source_inventory=sources,
 source_files=[dict(path=path,sha256=sha(raw),full_file_sha256=sha(raw),bytes=len(raw))
               for path,raw in sorted(cache.items())],
 inherited_proof_inputs=[],peer_proof_inputs=[],
 inherited_input_note='No inherited or peer mathematical producer is assumed. Baseline v0.40 supplies project context; the full neatU implication is reconstructed here.',
 published_applications=dict(file='published_applications.json',
  sha256=sha((HERE/'published_applications.json').read_bytes()),ids=[],
  explanation='No newly imported theorem: all substantive arithmetic/topological implications used for neatU are written in NTL1-NTL17.'),
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes()),portable=True,
  arguments=['--source','--human-root','--peer-root'],read_only_inputs=['pinned Lean source'],
  context_arguments='--human-root and --peer-root are accepted for the common component interface; no unproved inherited or peer theorem is consumed.'),
 validation=dict(pinned_blob_verified_files=len(cache),source_ranges=len(sources),
  distinct_source_ranges=len({(x['path'],x['line_start'],x['line_end']) for x in sources}),
  claim_source_ranges=sum(len(c['sources']) for c in claims),all_source_ranges_exact=True,
  claim_proof_blocks=len(claims),inherited_claim_proof_blocks=0,peer_claim_proof_blocks=0,new_lean_build=False),
 scope_note='Full original neatU, not just a local torsion lemma or a fixed auxiliary level. Source objects, auxiliary prime and all original quantifiers are preserved.')
dump('provenance.json',prov)
loc=[f'NTL1-NTL17 exact pinned source locators; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for x in sources:
    loc += [f"{x['id']} | {x['declaration']}",f"{x['path']}:{x['line_start']}-{x['line_end']}",
            'file_sha256='+x['sha256'],'range_sha256='+x['range_sha256'],x['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f'''NTL1-NTL17: full original neatU, v0.41

Formal correctness is accepted. No Lean build or replay was performed.
Source commit {PIN}
main.tex SHA256 {sha(tex)}
provenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}
closure.json SHA256 {sha((HERE/'closure.json').read_bytes())}
published_applications.json SHA256 {sha((HERE/'published_applications.json').read_bytes())}

COMPLETED ENDPOINT

NTL17 proves the entire original UpperTheory.V.Hi.neatU. It holds for
every original HidaSetting, n>=1, level datum V, QData Q, Coef c, every
integral representation tau0 of any rank m, and every original family of
compact-open local levels K. No TypeForAlt or HSet.Ax is assumed.

NTL1-NTL5 prove torsion-freeness of the exact principal congruence group.
The p=q binomial step uses only p odd. Principal-ideal separation is
proved by an increasing chain of principal ideals. The discriminant
condition yields a nondegenerate trace form modulo p, a reduced finite
algebra and hence p as a uniformizer at the actual place. The local DVR
background is also justified by the finite integral-basis and determinant
arguments. No restriction ell>n or invertibility of n! occurs.

NTL6-NTL11 reconstruct the global finite-order criterion. Compactness
gives a positive local power using a finite coset set without assuming
normality. Conjugation preserves characteristic polynomials. One place
above each real-field place suffices after checking both a coefficient
and its CM conjugate. Cayley-Hamilton puts all powers in one bounded-
denominator module; unitarity bounds every complex embedding. The finite
set of bounded algebraic integers is proved via integer coefficients of
their minimal polynomials, without an imported finiteness theorem.

NTL12-NTL17 carry those arguments through the actual source frame and
levels. The section's trivial-map fallback is explicitly retained.
Original QData injectivity and range give both exact level inclusions.
The product Iwahori inclusion follows directly from its three defining
subgroups. One product of positive compact-level powers handles every
added place, including the empty-Q case. The actual auxiliary coordinate
then forces M=1 and both original stabilizer factors u,b to equal 1.

SCOPE AND NEXT JOIN

The fixed auxiliary prime is s.p, already odd, prime to disc(L), and
different from ell. It is never replaced by a prime depending on rank.
The allowed coefficient prime ell=3 in rank four is included. Both Links
and their fixed-iota/common-coefficient-threshold order are unchanged.
The exponents selected during a single stabilizer proof are internal
witnesses and do not introduce a new global threshold.

The companion ordinary-weight packet can consume NTL17 after constructing
one theta, thereby proving Free for every K without changing theta. The
integral type, remaining HSet.Ax fields, actual ordinary/control modules,
arithmetic fibers, four Hida endpoints and same-J all-level HasAut remain
separate. This closes ORIGINAL_NEATU, not COUNT_II_SUPPORT.

EVIDENCE

{len(claims)} proof blocks; {len(cache)} pinned source files;
{len(sources)} source ranges;
{sum(len(c['sources']) for c in claims)} claim-source references.
No inherited or peer mathematical producer and no new published theorem
is assumed. All exact source bytes equal their pinned git blobs. The
portable builder accepts --source, --human-root and --peer-root and writes
only in this component. Standalone TeX and independent final-byte review
are recorded separately.
'''
(HERE/'report.txt').write_text(report)
print(json.dumps(dict(claims=len(claims),source_files=len(cache),source_ranges=len(sources),
 claim_source_ranges=sum(len(c['sources']) for c in claims),main_sha256=sha(tex),
 provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
 closure_sha256=sha((HERE/'closure.json').read_bytes())),indent=2))
