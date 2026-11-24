#!/usr/bin/env python3
"""Bind the completed independent argument reviews to the frozen components."""
from pathlib import Path
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

reviews={
 'odd_minus_supplier':{
  'hash':'d84beec71cba025a3303be52ab11e0f03ca95a533a3ed333ae401b20bdd47a84',
  'scope':'Complete literal PsiBound supplier on the original coefficient ring, field, algebraic closure, cyclotomic action and local groups, relative to explicitly named finite classical theorems and LD2/LD4.',
  'checks':{
   'OS1':['Finite-field Jacobi norm and carry valuation with the inverse group-ring convention','Arbitrary ideals reduced to degree-one primes in the inverse ideal class','Root-of-unity uniqueness and simultaneous congruence at all places over q','Norm distribution and reduction preserve one global root-of-unity ambiguity'],
   'OS2':['Choice of the smoothing element and unit character difference','The P operator kills the precise root-of-unity ambiguity','Strict norm and congruence relations retain exponents prime to p'],
   'OS3':['Kolyvagin derivative identity and induction removing a prime','The finite cocycle is well-defined and continuous with choice errors killed by P','Character averaging, initialization and the exact inertia/Frobenius recurrence'],
   'OS4':['Noncontainment of the three excluded subgroups, including the Kummer-character and complex-conjugation arguments','Finite odd-primary subgroup avoidance','One compatible finite-quotient Chebotarev condition supplies every required property of the auxiliary prime'],
   'OS5':['Separating Z/p^h-linear coefficient maps rather than a potentially nonunit trace','LD2/LD4 yield actual elementwise inertia times Frobenius annihilation','The commutator extension realizes the required cyclotomic dual cocycle','The divisibility comparison retains the specified normalized cocycle and annihilator ideals'],
   'OS6':['Strict increase of the auxiliary annihilator valuation when a Selmer class remains','Finite induction on the available valuation budget; no prior finiteness assumed','Evaluation kernel and image lengths give the full module-length bound, not only annihilation'],
   'OS7':['Finite Bernoulli expansion, coefficient clearing and the factor 2','Correct primitive-to-level Euler factor, a p-adic unit in the stated case','Same O and specified scalar normalization; z and a0 z divide the required values after choosing m'],
   'OS8':['Unique complex-conjugation normalization and exhaustion by uniformly bounded cocycles and witnesses','Inertial-to-decomposition local triviality for nontrivial prime-to-p inertia character','Residual cyclotomic case reduces to k(1), then rational Kummer local conditions force the class to vanish'],
   'OS9':['Tame inflation-restriction and coefficient extension on the original field and all original local data','The twist chi_p^(-e) psi^(-1) selects the positive psi eigenspace of the source action','Finite length and the a=0 extended-valuation case match literal universal PsiBound']
  },
  'not_closed':['ThmBab and PointHV','Actual common arithmetic family and prime-window gap','Other geometric, theta, metric and spectral suppliers','Full RH or Dirichlet-GRH human reconstruction']
 },
 'odd_minus_bounds':{
  'hash':'1cf2ac7b6d471ccbf594b1fe5c57fd554679e0d520e5c57df3d3478df3907f1b',
  'scope':'Complete literal ThmBcFree with explicit constant 240, supplied by OS9 and OS1 plus the five separately stated classical inputs; all original field, conductor, coefficient and local-data choices retained.',
  'checks':{
   'OB1':['Actual cyclotomic action and complex conjugation','Character count and original IsCompField degree bound','Every odd degree divisor lies in the fixed base exceptional set'],
   'OB2':['Bernoulli algebraic integrality with explicit denominators','Primitive Fourier/Gauss/Euler-product nonvanishing for k at least 2','Galois-stable product is a nonzero rational integer','Archimedean and primorial estimates pay simultaneously for every good-prime valuation'],
   'OB3':['Absolute strict Selmer and source restricted-ramification group comparison','Finite free coefficient extension preserves the full kernel','Exact tame character projectors and length scaling by v_O(ell)','Cancellation of the same ramification factor on both sides of the PsiBound estimate'],
   'OB4':['Torsion cocycle representatives and the set injection into Kummer cohomology','Kummer S-unit/class-group exact sequence','Minkowski, discriminant and elementary ideal-count estimates give constant 8'],
   'OB5':['Bernoulli distribution and the explicit ell-adic group-ring approximation','Finite-level local triviality yields an ordinary class-group character','OS1 gives twice the required annihilator with exact inverse orientation; 2 is cancelled only in the odd-primary target','The negative cyclotomic twist is cancelled by b^e explicitly','Restriction to the infinite cyclotomic subgroup is injective without any class-group finiteness assumption; phi(R) kills the remaining finite quotient'],
   'OB6':['Signed group-ring quotient has rank n/2','Adjugate determinant produces an annihilator on the actual minus part','All character factors are nonzero, with explicit integral denominator','Valuation and factorial estimates give the uniform constant 30'],
   'OB7':['Power-kernel filtration proves length at most exponent times generators','Finiteness follows from the two proved bounds','Constants multiply to 240; the unused 2-primary statement is not inferred'],
   'OB8':['All-prime good-prime integer-product budget and finite twist sum','Exceptional prime set is exactly the original base-degree set','Elementary inequality (t-1)(2t+5) at most 3t^2','Uniformity over every original algebraic closure, local-data family and finite set of odd primes','Exact literal ThmBcFree constant 240 feeds VW3/VW4']
  },
  'not_closed':['Two-primary and prescribed-layer supplier ThmBab','Odd-plus comparison PointHV','Original-family global installation and other LinkV inputs','Full RH or Dirichlet-GRH human reconstruction']
 },
 'congruence_chain':{
  'hash':'033694f3a26f131b4ebb7b49557955e56478acd5be3ae4fbd1db32bfea0c0cac',
  'scope':'Complete conditional integral-cut, congruence-length, prime-summation and cut-to-original LinkN chain, with actual type/theta/rank identities and local Galois denominator tables explicitly retained.',
  'checks':{
   'LN1':['Regular-representation trace proves integrality of scaled central idempotent coefficients','The literal e0 is the ordered-tuple sum with its multiplicities; no idempotence or deduplication assumption'],
   'LN2':['Construction of S and keep from actual type spaces','Original integral action and Pass.EigSpan give the exact scalar clauses','Tame-character transport uses labels, not an embedding of finite fields into C','Multiplicity and power conditions hold for every tame generator and, by the same-point constituent identity, every representative','All retained type and theta compatibility inputs are stated'],
   'LN3':['Finite free lattice and explicit rational spanning input','Separation yields rational spectral projections and the original quotient lattice','Denominator clearing proves finite congruence length'],
   'LN4':['Filtration by spectral coordinates, with correctly bounded free ranks','The supported congruence ideal annihilates the appropriate associated quotient','Length estimate does not assume integral semisimplicity'],
   'LN5':['Exact cut map and kernel killed by the group order','Original DVR normalization gives v_ell of the group order','Original ideal inclusion gives the stated adm1 bound'],
   'LN6':['Multiplicity bound uses actual ConclusionZ and localization uniqueness','Nonzero theta-composition scalar yields injection and rank equality','Reference/twisted rank compatibility remains an explicit original-data input'],
   'LN7':['Ramification factor occurs exactly once in the normalized place weights','Degree identity bounds their sum by log ell','Same original eta and multiplicity bindings give E_original at most E_cut plus d_j log group order','Summability and exact denominator tables are retained at the stated point of use'],
   'LN8':['Uniform family parameter clauses and their exact PN dependencies','Elementary harmonic sums and band bounds','Split/inert envelopes explicitly follow from, and do not replace, the local arithmetic input','Small-order inert primes lie in the two sparse residue classes by the 2-adic order calculation','All small, ordinary, exceptional and generator primes are covered','Constant 2000(C+1)^3 bounds every finite prime sum; no unproved prime-distribution estimate is invoked'],
   'LN9':['Actual gd construction keeps fields, local data, Sha, vvTerm and the cohomological coefficient','Finite general-linear-group cardinality bounds the restoration cost','One uniform threshold joins the bounds before selecting the family','The coefficient d_j on the cohomological term is unchanged'],
   'LN10':['Actual local-table, theta/type and parameter inputs are sufficient for original-family LinkN','Direct and cut routes are separated without assuming either input constructs itself','Stronger CutGivesAlt/NormChoiceFacts/Tie4 supplier remains open','Full source/target metric comparison and other global links are not inferred']
  },
  'not_closed':['Actual local Galois denominator inequalities on the selected family','Actual type/e0 action and theta/localization/rank identities','All stronger CutGivesAlt fields and compatible NormChoiceFacts/Tie4','ShaFinOdd, summability and the independent cohomological bound when required as guards','Actual metric/spectral/global-link suppliers','Unconditional original-family LinkN or full RH/Dirichlet-GRH reconstruction']
 }
}

for comp,spec in reviews.items():
 main=ROOT/comp/'main.tex';raw=main.read_bytes();assert digest(raw)==spec['hash'],comp
 prov=ROOT/comp/'provenance.json';d=read(prov)
 records=[s for c in d['claims'] for s in c['sources']]
 files={s['path']:s['sha256'] for s in records}
 verified={}
 for path,h in files.items():
  b=(REPO/path).read_bytes()
  blob=subprocess.run(['git','-C',str(REPO),'show',PIN+':'+path],capture_output=True,check=True).stdout
  assert b==blob and digest(b)==h,path
  verified[path]=b.splitlines(keepends=True)
 for s in records:
  b=b''.join(verified[s['path']][s['line_start']-1:s['line_end']])
  assert digest(b)==s['range_sha256'],s
  if 'range_bytes' in s:assert len(b)==s['range_bytes'],s
 proof_ranges=[]
 for c in d['claims']:
  loc=c.get('proof_location',c.get('human_proof'))
  b=b''.join(raw.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
  assert digest(b)==loc.get('sha256',loc.get('range_sha256')),c['id']
  proof_ranges.append({'id':c['id'],'line_start':loc['line_start'],'line_end':loc['line_end'],'sha256':digest(b)})
 assert set(spec['checks'])=={c['id'] for c in d['claims']}
 result={
  'schema':'rh-human-reconstruction-independent-review/1','date':'2026-11-22','artifact_version':'0.24',
  'reviewer_role':'Root integrating agent, independent of this component author; mathematical review and source-interface checks performed before integration',
  'component':comp,'reviewed_file':comp+'/main.tex','reviewed_claim_ids':list(spec['checks']),
  'result':'PASS for '+spec['scope'],
  'review_kind':'Human mathematical argument review and literal interface comparison; not formal verification or an independent kernel replay',
  'reviewed_main_sha256':spec['hash'],'reviewed_provenance_sha256':digest(prov.read_bytes()),'pinned_lean_commit':PIN,
  'verification':{'proof_range_count':len(proof_ranges),'source_link_count':len(records),'distinct_source_file_count':len(files),'all_proof_range_hashes_match':True,'all_source_range_hashes_and_lengths_match':True,'all_source_file_hashes_match':True,'all_source_files_equal_pinned_git_blobs':True,'errors':[],'proof_ranges':proof_ranges},
  'mathematical_checks':[{'id':cid,'result':'PASS','checked':checks} for cid,checks in spec['checks'].items()],
  'closed_scope':spec['scope'],'not_claimed_closed':spec['not_closed'],'unresolved_findings':[]
 }
 out=ROOT/'reviews_v0_24'/f'{comp}_root_review.json';write(out,result)
 print(comp,len(spec['checks']),'claims;',len(records),'source ranges;',len(files),'pinned files; PASS')
