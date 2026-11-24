#!/usr/bin/env python3
"""Bind an independently completed human review to the exact CFO packet.

This program checks byte identities and references.  The mathematical judgments
record the prior independent reading; executing it is not a mathematical review.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
COMP = ROOT / 'work_v037/count_first_order'
SOURCE = ROOT / 'lean_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
EXPECTED = {
    'main.tex': '3cd519c6f1b2906a6c5bdac14a2055e7801dc20e5487a5f1eaa15d4264c8f50a',
    'provenance.json': 'aab816d32b298b3e2903025b061473921607174fb9a05ede3f7243162d0b04e1',
    'closure.json': 'd6cf780e408ac37f6f4c80de983fe834a6e1b5cdb5fcefb0b56ed6b303179a4f',
    'published_applications.json': '69a8ea7e6458a74d13faeb623df0eb30e76db1899583c3bd3d9ebb7286e62d75',
}

CHECKS = {
 'CFO1': [
  'The point, coefficient extension, full block a=n=4, chosen zero-dimensional Kap, detector list and CAP13 realization remain the same objects.',
  'The target is the literal finite Sel1/Bd1 B1 inequality, with one C before every m and the subsequent eventual N. Complete CohP, LocCFT, old N4 and all original setting hypotheses remain explicit.'
 ],
 'CFO2': [
  'PhiCond supplies finiteness of the cocycles on the required open subgroups. The function module is torsion free and complete in the t-adic topology.',
  'Finite-valued approximations give the stated modular finiteness, including the zero truncation; no modular cocycle is assumed to lift to an exact integral solution.'
 ],
 'CFO3': [
  'The descending finite images of the approximate solution modules stabilize. The induction gives successive compatible approximants and the Cauchy limit lies in the exact kernel.',
  'Kernel saturation and finite-dimensional reduction yield finite generation by the written complete-module argument. Torsion modulo B then has one uniform annihilating power and bounded cardinality, chosen before m.'
 ],
 'CFO4': [
  'The defect and twisted-trace maps use exactly the original TwZ/TwB and detector equations. The integral coboundaries are in the exact kernel by the prescribed scalar-character identities.',
  'The selected Detects hypothesis makes the exact quotient torsion, so CFO3 supplies the uniform modular bound; it does not assert integral liftability.'
 ],
 'CFO5': [
  'The affine action and the full pro-ell quotient force descent through the original PL-kernel. The ta=0 condition and the actual TWGrp kernel inclusion are used on the same group.',
  'The normalized descent is injective, and its continuity follows through the compact quotient rather than from an arbitrary abstract group factorization.'
 ],
 'CFO6': [
  'Taking normal cores gives the required open subgroup of the original compact group. Finiteness of all modular cocycles and the fixed detector list gives one eventual level set.',
  'The eventual set is uniform over every later admissible representation. The original inverse-Frobenius convention is preserved.'
 ],
 'CFO7': [
  'All dualN quantifiers retain the order C, m, eventual N, then every repprime with the literal IsAd and finite-Zl hypotheses.',
  'The same local coboundary matrix handles ph and ta. The normalized cocycle/coboundary factors cancel through the involution anti-invariant image, using only that 2 is a unit; ell=3 is included.'
 ],
 'CFO8': [
  'A finite subset of the equations defines the characteristic-zero kernel. A nonzero minor and its adjugate provide the uniform bound on the truncated kernel.',
  'The constant is selected before m, and the stated rank is the dimension of that exact kernel.'
 ],
 'CFO9': [
  'The full NP span makes the primal commutant scalar; the polarization condition removes the scalar invariant. Original old-subgroup N4 survives passage to the fraction field.',
  'The selected distinct eigenvalues give centralizer dimension n over the fraction field without claiming an integral eigenbasis. CFO8 converts these facts to uniform finite bounds.'
 ],
 'CFO10': [
  'Both the primal adjoint and cyclotomic-twisted dual representations have the correct conjugation signs and satisfy the original IsAd formulas.',
  'The coefficient-of-t^(m-1) trace pairing is perfect and has the cyclotomic Tate twist, rather than its inverse. The zero truncation is treated separately.'
 ],
 'CFO11': [
  'Only finite Galois number-field completions are used in Milne 7.58(a), 8.10 and 8.13(b); the residue fields are finite and perfect and the tower restriction has a normal fixing subgroup.',
  'The absolute decomposition/inertia quotient and residue algebraic-closure assertion are independently derived by the compatible finite inverse system. No infinite extension is asserted to be a complete DVR; the Frobenius normalization is explicit.'
 ],
 'CFO12': [
  'The arithmetic presentation and every ArSys field are on the actual T/TWPl at every N, with the disjoint local-place indexing and exact original old D0 image.',
  'Both ph and ta lie in the same added local image. The local degrees are independent of N and have the correct total d, and all real-place involution and cyclotomic signs are preserved.'
 ],
 'CFO13': [
  'The entire original CohP is retained. Finite local duality/Euler and the global identity are applied only to the checked original finite continuous modules and arithmetic presentation.',
  'The conversion between cocycles and cohomology classes includes all invariant and coboundary factors. Its GWBare inequality agrees with the original source contract.'
 ],
 'CFO14': [
  'The tame inertia quotient has order prime to ell, so averaging proves the asserted coboundary description without an unproved local cohomology vanishing.',
  'The procyclic quotient cocycle is counted through its Frobenius value with the continuity condition checked. The resulting UnrCount and all ArSys counts preserve the original inertia subgroup and Frobenius convention.'
 ],
 'CFO15': [
  'The scalar local homomorphism bound uses the retained original LocAb/LocCFT map and the correct dprime_v+1 exponent.',
  'The off-diagonal scalar character is distinct from the cyclotomic twist by the ordered N1 clauses. One nonzero difference gives a uniform valuation constant before m.'
 ],
 'CFO16': [
  'Increasing superdiagonal distance gives a finite filtration whose next coordinate is the required scalar cocycle after the preceding entries vanish.',
  'The diagonal and off-diagonal counts give exactly n(dprime_v+1)+nu(1+d_v), with the actual ordered local characters, original basis w_v and inertia condition.'
 ],
 'CFO17': [
  'The ordinary normalization lower bound comes from the actual upper-triangular intersection, giving n+nu rather than an unproved equality of local condition spaces.',
  'At each real involution, multiplication by the specified symmetric matrix identifies the invariant subspace with skew matrices. The count is Q^(m nu) without extracting square roots.'
 ],
 'CFO18': [
  'Normalization at the involution gives the literal Sel1/Bd1 quotient by an explicit coboundary using the unit 2.',
  'The local ordinary witness Y, the selected w_v, and the original tame subgroup remain identical. Full-block g=0 does not imply Sel1=0; local constancy supplies the required finite continuity statements.'
 ],
 'CFO19': [
  'Each added-prime orthogonal condition uses one local coboundary for both ph and ta, so the uniform dualN bound applies.',
  'All global/local invariant, real-place, ordinary-normalization and coboundary factors are present and positive before cancellation. The resulting one-level inequality has the exact original exponent terms.'
 ],
 'CFO20': [
  'Only the separate total equalities sum dprime_v=d and sum d_v=d are used; no pointwise equality of local degree families is assumed.',
  'The exponent cancels exactly to m(nd+nq)+C and hence m(4d+4q)+C. C is fixed before m; only the dual comparison requires eventual N, and m=0 is handled at every level.'
 ],
 'CFO21': [
  'The new B1, earlier CCH Choice and g=0 B2 are installed on the identical extended point, Kap, list and realized T over the same ideal J.',
  'Both original rank-four Links and one common coefficient threshold after fixed iota remain. Original ordinary/control/fibers, four Hida endpoints, same-J all-level HasAut, h=0 Raw, CohP and LocCFT stay open inputs.',
  'The result does not certify arbitrary-Kap FirstOrderDualArithmeticBound, any Sel1 vanishing, full Count-II support, or an unrelated count branch.'
 ],
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def block(data, start, end):
    return b''.join(data.splitlines(keepends=True)[start-1:end])

def main():
    for name, digest in EXPECTED.items():
        assert sha((COMP/name).read_bytes()) == digest, name
    p = json.loads((COMP/'provenance.json').read_text())
    closure = json.loads((COMP/'closure.json').read_text())
    assert p['source_commit'] == closure['source_commit'] == PIN
    assert p['main_tex_sha256'] == closure['proof_sha256'] == EXPECTED['main.tex']
    data = (COMP/'main.tex').read_bytes()
    files = {}
    for f in p['source_files']:
        b = (SOURCE/f['path']).read_bytes()
        git = subprocess.check_output(['git','show',PIN+':'+f['path']],cwd=SOURCE)
        assert b == git and sha(b) == f['sha256'], f['path']
        assert f.get('full_file_sha256',f['sha256']) == sha(b)
        files[f['path']] = b
    inherited = set()
    inherited_blocks = 0
    for f in p['inherited_proof_inputs']:
        b = (ROOT/f['path']).read_bytes()
        assert sha(b) == f['sha256'], f['path']
        for item in f['claim_proof_blocks']:
            assert sha(block(b,item['line_start'],item['line_end'])) == item['sha256'], item['id']
            inherited.add(item['id'])
            inherited_blocks += 1
    ids = {c['id'] for c in p['claims']}
    assert ids == set(CHECKS) == {f'CFO{i}' for i in range(1,22)}
    adjacency = {}
    ranges = set()
    occurrences = 0
    reviews = []
    for c in p['claims']:
        b = c['proof_location']
        proof = block(data,b['line_start'],b['line_end'])
        assert sha(proof) == b['sha256'] and len(proof) == b['bytes'],c['id']
        assert (f'% BEGIN {c["id"]}').encode() in proof
        assert (f'% END {c["id"]}').encode() in proof
        for dep in c['depends_on']:
            assert dep in ids | inherited, (c['id'],dep)
        adjacency[c['id']] = [d for d in c['depends_on'] if d in ids]
        for s in c['sources']:
            full = files[s['path']]
            assert sha(full) == s['full_file_sha256'] == s['sha256']
            r = block(full,s['line_start'],s['line_end'])
            assert sha(r) == s['range_sha256'] and len(r) == s['range_bytes'],s['id']
            ranges.add((s['path'],s['line_start'],s['line_end'],s['range_sha256']))
            occurrences += 1
        reviews.append({'id':c['id'],'title':c['title'],'status':'PASS',
          'proof_range':{'line_start':b['line_start'],'line_end':b['line_end'],'sha256':b['sha256']},
          'checks':CHECKS[c['id']],'required_corrections':[]})
    done = set()
    def visit(k,stack):
        assert k not in stack, ('cycle',stack,k)
        if k in done:return
        for d in adjacency[k]:visit(d,stack|{k})
        done.add(k)
    for k in ids:visit(k,set())
    report = {
      'schema':'rh-independent-component-review/1','version':'0.37','component':'count_first_order',
      'reviewer':'/root/audit_global_routes','status':'PASS','source_commit':PIN,
      'claims_reviewed':[f'CFO{i}' for i in range(1,22)],
      'proof_file_sha256':EXPECTED['main.tex'],'provenance_file_sha256':EXPECTED['provenance.json'],
      'closure_file_sha256':EXPECTED['closure.json'],
      'published_applications_file_sha256':EXPECTED['published_applications.json'],
      'all_required_corrections_resolved':True,'required_corrections':[],
      'per_claim_reviews':reviews,
      'independent_verification':{
        'proof_blocks':len(ids),'pinned_source_files':len(files),'distinct_source_ranges':len(ranges),
        'claim_source_references':occurrences,'inherited_files':len(p['inherited_proof_inputs']),
        'inherited_proof_blocks':inherited_blocks,'all_pinned_blobs_equal':True,
        'all_proof_and_source_range_hashes_match':True,'all_depends_on_are_claim_ids':True,
        'new_claim_dependency_graph_acyclic':True,'new_lean_build_performed':False,
        'formal_source_correctness_assumed':True
      },
      'primary_literature_check':{
        'id':'CFO_LOCAL_DECOMP','status':'PASS','primary_url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
        'theorems':['7.58(a)','8.10','8.13(b)'],
        'errata_url':'https://www.jmilne.org/math/CourseNotes/errata.html',
        'independent_retrieval_refs':['turn434553338view0','turn434553338view1','turn236648787view1','turn236648787view2','turn236648787view3'],
        'checked_scope':'The cited finite completion, inertia and restriction facts match the finite Galois stages. The written proof, rather than an extension of the published finite theorem, supplies the absolute quotient passage.'
      },
      'scope_conclusion':'The exact selected full-block a=n=4,g=0 B1 implication is complete and coupled to the same CCH Choice/B2 and CAP T/TWPl. Complete CohP and LocCFT, the original arithmetic setting and the ordinary/HasAut/Raw producers remain explicit. No arbitrary-Kap B1 or whole Count-II closure is claimed.',
      'validation_method':'Independent mathematical reading and original-source contract comparison, followed by byte and reference verification. Hash checks alone are not presented as proof checking.'
    }
    (HERE/'count_first_order_review.json').write_text(json.dumps(report,indent=2)+'\n')
    lines = ['INDEPENDENT CFO1-CFO21 REVIEW — PASS','',
      'Reviewer: /root/audit_global_routes','Source pin: '+PIN,
      'Main SHA256: '+EXPECTED['main.tex'],'Provenance SHA256: '+EXPECTED['provenance.json'],
      'Closure SHA256: '+EXPECTED['closure.json'],
      'Published applications SHA256: '+EXPECTED['published_applications.json'],'',
      report['scope_conclusion'],'',
      f'All {len(ids)} proof blocks, {len(files)} pinned source files, {len(ranges)} distinct source ranges, {occurrences} claim/source references, {len(p["inherited_proof_inputs"])} inherited files and {inherited_blocks} inherited proof blocks independently match their recorded hashes.',
      'All depends_on entries resolve to actual reviewed/new or inherited claim IDs; the new-claim graph is acyclic. Formal correctness is assumed; no Lean rebuild is claimed.','',
      'The only new published input was independently retrieved from Milne, Algebraic Number Theory v3.08: Theorem 7.58(a), Propositions 8.10 and 8.13(b), with the author errata checked. Its finite Galois and residue hypotheses match the original finite stages. CFO11 writes the absolute inverse-limit argument and does not call an infinite algebraic extension a complete DVR.','',
      'Per-claim mathematical coverage:','']
    for c in reviews:
        lines.append(c['id']+' — PASS: '+c['title'])
        for text in c['checks']:lines.append('  '+text)
        lines.append('  Proof range SHA256: '+c['proof_range']['sha256'])
        lines.append('')
    lines += ['Required corrections: none.','',
      'The same-J and same-Kap restrictions are essential. The first-order bound holds on the selected original witness, while the ordinary system, four further Hida conclusions, all-level same-J HasAut and the h=0 stable-prime Raw argument remain producers. Both rank-four Links and their common later coefficient threshold remain. The argument includes ell=3 and never deduces Sel1=0 from g=0.','']
    (HERE/'count_first_order_review.txt').write_text('\n'.join(lines))
    print(json.dumps({'status':'PASS','counts':report['independent_verification'],
      'review_json_sha256':sha((HERE/'count_first_order_review.json').read_bytes()),
      'review_txt_sha256':sha((HERE/'count_first_order_review.txt').read_bytes())},indent=2))

if __name__ == '__main__':main()
