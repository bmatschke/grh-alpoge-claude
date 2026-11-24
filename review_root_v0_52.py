#!/usr/bin/env python3
"""Bind root's independent mathematical readings to the exact v52 files."""
from pathlib import Path
import hashlib, json, subprocess

ROOT=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/249d32c24541/formal_source')
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def sha(b): return hashlib.sha256(b).hexdigest()

GSL=[
 'Actual chartwise sections, gluing, pullback and LinComb are used throughout; no abstract isomorphism replaces the specified bundle or section.',
 'A nonzero minor of the matrix over the field supplies a scalar left inverse already over the original ring; no domain or flatness premise on that ring is added.',
 'The two denominators give literal matrix identities D0 B=0, CB=rI and BC+HD0=rI. Kernel rank zero and empty selected-column cases are included.',
 'The identities prove a basis after every ring map inverting r. The field value of r is nonzero, and in a local residue-field application r is already a unit.',
 'The finite-projective three-term complex is converted to actual finite matrices by adjoining chosen complements. The kernel and middle-exactness correspondences survive arbitrary tensor products.',
 'Descending finite cone lifts construct the bounded nonnegative finite model over a Noetherian ring. Its degree-zero module is a finite quotient and the displayed cone is exact.',
 'The bounded flat cone is worked backward through short exact image sequences. This proves universal tensor exactness and finite flat degree-zero projectivity, with the dual-basis globalization made explicit.',
 'The nonempty cube vertices descend to the supplied Noetherian model. The resulting finite-projective complex and comparison map work over arbitrary original R; the empty-index case is handled separately.',
 'The Cech complex uses actual affine intersections and pulled line-bundle sections. Degree-zero gluing and the literal all-cover H1 vanishing are compared through refinement, without replacing the source condition.',
 'Every Perf field, including fixed coordinate functions and the universal sec equation, is constructed. The very-ample cover has affine finite intersections by explicit section ratios; the original geometric model supplier is retained.',
 'Linearity, uniqueness and naturality follow from Perf.sec even though the supplied maps are initially only set equivalences. This retains every prescribed Cartesian model.',
 'One denominator and actual sections are chosen before every affine test. Their cardinality is fixed by the specified field rank, with zero rank allowed.',
 'A surjective coefficient map lifts every section using the same fixed basis; the conclusion is the actual chartwise IsPullSecLC identity.',
 'Specified scheme and bundle isomorphisms transport sections, bases and literal H1 data by units in the charts; no unrecorded identifications enter the later twist argument.',
 'Projectivity after the actual affine pullback is proved from retained PolBaseChangeSt and RelAmple data, using explicit very-ample coordinate ratios. The geometric law itself is not claimed here.',
 'Finite-group averaging descends the H1 cocycle when the group order is invertible. Exact invariant-function descent remains an explicit geometric premise.',
 'Positive-power H1 vanishing follows from retained Serre, multiplication and invariant-descent inputs. A sufficiently large prime distinct from the characteristic is chosen, and all Serre residue classes are covered.',
 'The integer growth lemma first determines square values by iteration, then uses multiplicative spacing within two integers and monotonicity to recover every h(j)=j^g; dimension zero is included.',
 'The exact rank n^g follows from retained initial rank one, actual section decomposition, multiplication identities and growth. No degree-of-multiplication assertion is silently substituted.',
 'The rank and H1 results transfer to every actual geometric fiber using PolBaseChange and the specified pullback maps.',
 'Translated-power generation uses the original multiplication geometry and theorem-of-square generators. The root is chosen only in an algebraically closed fiber, including characteristic dividing q.',
 'The twisted geometric fiber is identified with a translated pure power through explicit maps and bundle units. The original base may be arbitrary because the root is used only over the geometric field.',
 'The full conditional SecBaseChangeAny/St chooses one affine neighborhood and one set of sections before all test rings and tuples. FPerf, P, V and R are retained with their original scopes.',
 'The full local twisted-basis statement uses the same matrix over the local ring and every coefficient extension. The geometric root is not lifted to that local ring; T remains an explicit premise.',
 'Every residue section lifts on the original twist bundle and satisfies literal IsPullSecLC. Composition is written in conventional right-to-left order; arbitrary local rings and arbitrary residue sections are retained.',
 'The two conditional global section laws install in the same TDR/NFR/NFL family. Actual geometric model, polarization, Serre/multiplication, rank and theorem-of-square suppliers, and supplied Moduli, remain open.'
]

AFE=[
 'Finite coefficient residue field, exact Z_l reduction and prime-to-ell torsion injectivity are proved at the original Coef scope; ell-primary torsion reduces to one.',
 'The modulus CRT projection and image-primary projection are distinguished and then matched to the original source formulas, conductors and kapB/kapL decomposition.',
 'The full cyclotomic inertia image and corrected Frobenius are constructed at every specified place. The ell case corrects Frobenius by inertia, and the other cases preserve the required residual cyclotomic value.',
 'The quadratic integral basis and discriminant square root give the exact sign character, including both congruence classes of the squarefree radicand.',
 'Quadratic Gauss sums, i and sqrt(2) give the precise discriminant cyclotomic containment and the inertia consequence at ell prime to the discriminant.',
 'One inertia exponent is chosen before all places. The original GD kernel and weight guard supply g4 and g5 without an extra nondegeneracy hypothesis.',
 'All nineteen Gen fields are checked for Dat with Hb=top and M=ell*N*abs(disc K), retaining full original characters and the specified valuation.',
 'The actual dyadic conductor at least four forces the Host kernel obstruction; the element is adjusted to be minus one modulo four and in the character kernel.',
 'The dyadic principal-unit order calculation uses the actual conductor and the strict numerical bound to prove the required nonquadratic value, with all exponents accounted for.',
 'A witness is produced at every p in Tb and every chosen valuation. Squaring fixes eta4, preserves the cyclotomic kernel and keeps the squared residual character nontrivial, including ell=3.',
 'The actual subgroup ker(dirG(kapB)) is open, abelian and of ell-power index, contains ell inertia and gives the full away-from-ell Teichmuller implication.',
 'All nineteen Host Gen fields hold with the literal subgroup and M=ell*N. The Host branch does not inherit the stronger Dat prime guard.',
 'All ten IsHostFrame fields are constructed on the actual GS quotient, with the original places, inertia groups, sign, character and complex conjugation; P is unnecessary.',
 'The full exists_sigma statement is proved on any supplied original Host frame and at every allowed index; the character residue field and exact local witness are retained.',
 'The full P-to-GdFrameEx join chooses the CAF modulus Q before L and w and uses the same LFC marked g1, frame and C0, including the actual SeedClause.',
 'The full P-to-HostFrameEx join preserves that same choice order, actual Host subgroup and ell=3 scope.',
 'All five Marks conditions hold on the same chosen g1; the residual square inequality gives the required unit in the original local coefficient ring.',
 'Local ordinary characters are transported through the actual conjugation and local group map. The ordered three-factor zero product follows from the preserved standard flag, with the rightmost factor acting first.',
 'The full exists_nrep3 is proved for arbitrary original local O and local Noetherian domain A. The actual kernel closure, adic continuity, polarization, residual lift and inertia character formula are retained; neither completeness nor flatness is added.',
 'The whole FinPt-to-FinEnd theorem chooses G_L before every later coefficient algebra and ordinary point. The residue map and exact NRep character formula give the original characteristic polynomial on that one subgroup.',
 'The same marked frame carries Marks and the conditional finite endpoint. P, FinPt, both automorphic seed producers and AutEnd/patching remain explicit; no full GdEnd or selected global closure is claimed.'
]

for component,author,prefix,notes in [
 ('global_section_laws_v52','geometry_alltest','GSL',GSL),
 ('arithmetic_frame_entries_v52','arithmetic_common_frame','AFE',AFE)]:
 p=ROOT/component
 prov=json.loads((p/'provenance.json').read_text())
 manifest=json.loads((p/'source_manifest.json').read_text())
 proof=(p/'main.tex').read_bytes()
 assert sha(proof)==prov['proof_file_sha256']
 assert len(prov['claims'])==len(notes)
 blobs={}; files=[]
 for f in manifest.get('files',manifest.get('source_files',[])):
  path=f['path']; data=(REPO/path).read_bytes()
  blob=subprocess.check_output(['git','show',f'{PIN}:{path}'],cwd=REPO)
  assert data==blob and sha(data)==f.get('sha256',f.get('file_sha256'))
  snapshot=f.get('snapshot_file',f.get('snapshot_path'))
  if snapshot: assert (ROOT/snapshot).read_bytes()==blob
  blobs[path]=data
  files.append({'path':path,'sha256':sha(data),'verified_equal_to_pinned_git_blob':True})
 blocks=[]; ranges={}
 for i,c in enumerate(prov['claims']):
  assert c['id']==f'{prefix}{i+1}'
  q=c['proof_location']; data=b''.join((ROOT/q['file']).read_bytes().splitlines(keepends=True)[q['line_start']-1:q['line_end']])
  assert sha(data)==q['sha256'] and len(data)==q['bytes']
  blocks.append({'id':c['id'],'block_sha256':sha(data),'status':'PASS','review_note':notes[i]})
  for s in c['sources']:
   blob=blobs[s['path']]
   assert sha(blob)==s['file_sha256'] and s['source_commit']==PIN
   data=b''.join(blob.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
   assert sha(data)==s['range_sha256'] and len(data)==s['range_bytes']
   ranges[(s['path'],s['line_start'],s['line_end'])]={'path':s['path'],'line_start':s['line_start'],'line_end':s['line_end'],'range_sha256':sha(data)}
 review={'schema':'rh-independent-mathematical-review/1','artifact_version':'0.52','component':component,
  'reviewer':'root','author':author,'source_commit':PIN,'status':'PASS','proof_file_sha256':sha(proof),
  'claims_reviewed':blocks,'unresolved_findings':[],
  'scope':'Independent reading of every human proof block and original endpoint scopes, with source and proof bytes separately verified. No Lean replay.',
  'source_files_verified':files,'source_ranges_verified':list(ranges.values()),
  'whole_selected_obligation_closed':False}
 (p/'independent_review.json').write_text(json.dumps(review,indent=2)+'\n')
 md=[f'# Independent mathematical review: {component}','','Reviewer: root. Author: '+author+'.','',
  '**Status: PASS.** Every numbered proof was read independently against the original scope; exact file and block hashes bind that review.','',
  'Main proof SHA-256: `'+sha(proof)+'`.','',f'{len(blocks)} proof blocks, {len(files)} pinned source files and {len(ranges)} distinct cited ranges verified.','']
 for c in blocks: md += ['## '+c['id'],'',c['review_note'],'']
 md += ['## Scope boundary','',notes[-1],'','No unresolved review findings. This is an independent mathematical and exposition review, not a new formal verification.','']
 (p/'independent_review.md').write_text('\n'.join(md))
 print(json.dumps({'component':component,'status':'PASS','claims':len(blocks),'files':len(files),'ranges':len(ranges),'main_sha256':sha(proof)}))
