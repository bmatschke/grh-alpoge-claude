#!/usr/bin/env python3
"""Bind the root's completed independent LK, KB and CZ argument reviews."""
from pathlib import Path
import hashlib,json,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def sha(b):return hashlib.sha256(b).hexdigest()
checks={
 'local_k_duality':[
  ('LK1',['The original finite subfield carries the complete extended local norm; its integral lattice has rank d.',
          'Compatible roots give the source cycK, and original H0/H1/H2/Hn equal the continuous cochain quotients.']),
  ('LK2',['Classical finite local cohomology applies in characteristic zero even at residue characteristic ell.',
          'Finiteness and higher vanishing match the exact Finite and Subsingleton interface clauses.']),
  ('LK3',['The multiplicative Tate dual becomes the specified inverse-and-cyclotomic-twist R-linear dual.',
          'Finite nonfree modules have the stated evaluation biduality; the local invariant is an R-isomorphism.',
          'All original cochain cup formulas, including dual-first degree one, match; postcomposition by the invariant is explicitly inverted.',
          'The flipped pairing follows from finite biduality and uses no division by two.']),
  ('LK4',['Milne I Theorem2.8 has the factor |O_K/|M|O_K| inverse.',
          'The integral lattice calculation gives |M|^d for arbitrary finite M, including the zero module and ell=2.'])],
 'k_theory_bridge':[
  ('KB1',['The original quotient G_S and unique D.chi give the actual Tate twist and its local restrictions.',
          'Milne II Proposition2.9 and Theorem2.13 supply finite etale/continuous comparison and finiteness.',
          'Termwise surjective cochain transitions plus finite H1 give the exact compact-H2 inverse limit.',
          'The coefficient exact sequence yields H2(Z_l)/l injects into H2(F_l), without integral H3.']),
  ('KB2',['Quillen finite generation and Borel even-degree rank zero give a finite actual K_m(O_L).',
          'Independently opened Dwyer–Friedlander Propositions5.2,8.1,8.2 and Theorem8.5: finite-level surjectivity applies for m>=2; at two, r>=2 and the primitive fourth root are explicit.',
          'The Bockstein transition on K_(m-1)[l^r] is multiplication by l, so its inverse limit is zero.',
          'The etale filtration is 0→H2→K_et→H0→0; integral H0 vanishes because the cyclotomic image is infinite and e>=1.',
          'Finite compatible fibers give a surjective inverse-limit map on the original compact target.']),
  ('KB3',['The Dedekind stable-range argument by Chinese remainders is valid.',
          'Independently inspected van der Kallen Convention2.2 and Theorem4.11 scan: sr<=2 gives stable dimension1 and injectivity from rank2m+1; source rank2m+4 is sufficient.',
          'The bar complex commutes with the matrix-group union, and the canonical plus construction preserves integral homology.',
          'Independently checked Arlettaz Definition7.11/7.14 and Corollary7.19(a): actual GL-target Hurewicz kernel is killed by R_m; squarefree factors give valuation<=m-1.',
          'Flat tensoring and division by the l-adic unit produce exactly the source kernel exponent cOne(2e), without discarding primes.']),
  ('KB4',['The finite module and both maps instantiate every field of literal KBridge.',
          'No unproved theorem about arbitrary Plus/KPublished records is asserted.']),
  ('KB5',['Finite-kernel image, multiplication-kernel/cokernel equality and the l-power filtration prove the cardinality inequality.',
          'The tensor of H/T embeds in Q_l tensor H/T by flatness; every finite submodule therefore lies in the l-primary tensor of finite T.',
          'No finite-generation hypothesis on H is silently introduced.']),
  ('KB6',['Finite Poitou–Tate identifies strict Sha2 and Sha1 orders with the exact dual twist.',
          'The requested original D.A_v→henselization→completion→K inside PadicAlgCl transport is now explicit, preserving Galois actions, roots, cochains and local restriction.',
          'LK gives local H2 order at most l, and there are at most n places above l.',
          'HasMuQ trivializes the finite dual twist; an everywhere-unramified character factors through the ordinary class group of the original totally complex L.']),
  ('KB7',['Minkowski normalization, ideal Euler-factor coefficient bound and elementary harmonic sums give log h_L<=n log Delta/2.',
          'The generator logarithm, l<=n+1 and c(m)<=m(m+3) give exactly the source reduction inequality.']),
  ('KB8',['The bound Q<=10x^2<=x^9-1 and the exponential absorption are valid for x=2en>=2 and all real C.',
          'TB10=22 yields LemmaK31 with the constant chosen before all original fields, primes, twists, closures and local data.'])],
 'count_z_closure':[
  ('CZ1',['The actual coefficient algebra embeds in PadicAlgCl, is finite torsion-free over Z_l, and yields a finite-rank divisible primary module.',
          'Compactness gives finite cocycle image; divisibility moves every l-torsion class into M[l] while preserving all local coboundary conditions.',
          'Vanishing of l-torsion suffices without assuming the whole Selmer group finite.']),
  ('CZ2',['Shifted cyclotomic Eisenstein polynomials prove full finite-level inertia, and nested compact fibers give actual Z_l-unit surjectivity.',
          'Hensel lifting proves unramified cyclotomic action away from l.',
          'Finite rational ray class theory puts each unramified-outside-l additive character in the original cyclotomic tower.',
          'A single original decomposition-group coboundary then proves global injectivity on classes zero at the cyclotomic kernel.']),
  ('CZ3',['The Gauss-sum multiplication explicitly gives tau²=l and the exact quadratic residual kernel inside the original closure.',
          'The integral-basis index-square argument proves discriminant l.',
          'The two-dimensional convex-body argument produces the ideal-class norm bound, and ideal divisor counting gives h_K<l.',
          'Real inertia has order at most two, so odd-primary unramified characters factor through the ordinary Hilbert class group and vanish.']),
  ('CZ4',['The residual-trivial twist turns the representative into an additive character; rational cyclotomic control and strict local triviality give full vanishing.']),
  ('CZ5',['The divisibility and parity assumptions force the quadratic residual character with l=1 mod4.',
          'The chosen nonsquare cyclotomic scalar has alpha-1 invertible; normalization retains the l-torsion representative.',
          'At every original l-adic place the local witness is forced into M[l], giving unramified restriction to the actual G_K.',
          'Quadratic class-field vanishing and the explicit index-two coset calculation kill the entire cocycle.']),
  ('CZ6',['CaseZ and host parity give exactly PropZ hypotheses, including l>=5 and e>=2 even.',
          'The original V-prime local conditions are stronger, so their Selmer group is a subgroup of the proved zero group.',
          'Finiteness and normalized Vn=0 yield literal CountZ with uniform natural exponent C=0.'])]
}
primary_refs={
 'local_k_duality':['turn525619534view0','turn525619534view1','turn525619534view2'],
 'k_theory_bridge':['turn529427469view0','turn529427469view1','turn529427469view2',
  'turn774464902view0','turn774464902view1','turn774464902view3','turn774464902view4',
  'turn526246658view0','turn683398245view2','turn683398245view3'],
 'count_z_closure':['turn352839052view0','turn880766199view0']}
for component,items in checks.items():
 p=ROOT/component/'provenance.json';ledger=json.loads(p.read_text())
 raw=(ROOT/component/'main.tex').read_bytes();lines=raw.splitlines(keepends=True)
 assert ledger['commit']==PIN
 proof_checks=[];sources={};ranges=0
 for c in ledger['claims']:
  loc=c.get('proof_location',c.get('human_proof'));a,b=loc['line_start'],loc['line_end']
  frag=b''.join(lines[a-1:b]);assert sha(frag)==loc['sha256'],c['id']
  if 'bytes' in loc:assert len(frag)==loc['bytes']
  proof_checks.append({'id':c['id'],'line_start':a,'line_end':b,'sha256':sha(frag)})
  for s in c['sources']:
   path=s['path']
   if path not in sources:
    blob=(REPO/path).read_bytes()
    assert blob==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
    sources[path]=blob
   blob=sources[path];frag=b''.join(blob.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
   assert sha(blob)==s['sha256'] and sha(frag)==s['range_sha256'],(component,path)
   if 'range_bytes' in s:assert len(frag)==s['range_bytes']
   ranges+=1
 ids=[x[0] for x in items]
 assert set(ids)=={c['id'] for c in ledger['claims']}
 rec={'schema':'rh-human-reconstruction-independent-review/1','date':'2026-11-22','artifact_version':'0.25',
  'reviewer_role':'Root integrating agent, independent of the component author; complete mathematical argument and original-interface review',
  'component':component,'reviewed_file':component+'/main.tex','reviewed_claim_ids':ids,
  'result':'PASS','review_kind':'Independent human mathematical argument review and source/interface comparison, not formal verification',
  'reviewed_main_sha256':sha(raw),'reviewed_provenance_sha256':sha(p.read_bytes()),'pinned_lean_commit':PIN,
  'verification':{'proof_range_count':len(ids),'source_link_count':ranges,'distinct_source_file_count':len(sources),
    'all_proof_range_hashes_match':True,'all_source_range_hashes_and_lengths_match':True,
    'all_source_file_hashes_match':True,'all_source_files_equal_pinned_git_blobs':True,'proof_ranges':proof_checks},
  'mathematical_checks':[{'id':cid,'result':'PASS','checked':notes} for cid,notes in items],
  'independently_opened_primary_source_refs':primary_refs[component],
  'resolved_findings':(['Made original-place henselization/completion/native-LK transport explicit in KB6 before freezing.'] if component=='k_theory_bridge' else ['Made actual coefficient subalgebra injectivity explicit.'] if component=='count_z_closure' else []),
  'unresolved_findings':[],
  'not_claimed_closed':['Other remaining PointHV counts and assembly','Actual common family and arithmetic gap',
                         'Remaining actual local/theta/metric/spectral suppliers','Full human RH or Dirichlet-GRH reconstruction']}
 (HERE/(component+'_root_review.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 print(component,sha(raw),len(ids),ranges,len(sources))
