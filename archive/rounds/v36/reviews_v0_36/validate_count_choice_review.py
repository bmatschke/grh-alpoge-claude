#!/usr/bin/env python3
"""Independent byte validation and hash binding for the completed CCH review."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parents[2])
args = parser.parse_args()
root = args.workspace.resolve()
component = root / 'work_v036/count_choice'
repo = root / 'lean_source'
baseline = root / 'reconstruction_v035'
out = root / 'work_v036/reviews'
pin = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_text())

def exact_range(data, first, last):
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    return b''.join(lines[first - 1:last])

expected = {
    'main.tex': 'd038d24462e9c18806da99e9aaa4f7746f66cfbf9854949b4d91c46ac14e1c2e',
    'provenance.json': '7ddfa3f70e34206d6afdf2eb65a850e6d120ba37f56d95d5e9746c01073117a9',
    'closure.json': '880c689216726dfc3e19dfb0acc23b9dafbcee69a9e91d36f5aa8d970315d599',
}
for name, value in expected.items():
    assert sha((component / name).read_bytes()) == value, name
p = read_json(component / 'provenance.json')
c = read_json(component / 'closure.json')
assert p['source_commit'] == c['source_commit'] == pin
assert p['main_tex_sha256'] == c['proof_sha256'] == expected['main.tex']
main = (component / 'main.tex').read_bytes()
claims = p['claims']
ids = [f'CCH{i}' for i in range(1, 18)]
assert [item['id'] for item in claims] == ids
blocks = []
for claim in claims:
    q = claim['proof_location']
    data = exact_range(main, q['line_start'], q['line_end'])
    assert sha(data) == q['sha256'] and len(data) == q['bytes'], claim['id']
    assert data.startswith(('% BEGIN ' + claim['id']).encode())
    assert data.rstrip().endswith(('% END ' + claim['id']).encode())
    blocks.append({'id': claim['id'], 'sha256': q['sha256'],
                   'line_start': q['line_start'], 'line_end': q['line_end']})

source_data = {}
for f in p['source_files']:
    data = (repo / f['path']).read_bytes()
    blob = subprocess.check_output(['git', 'show', f'{pin}:{f["path"]}'], cwd=repo)
    assert data == blob, f['path']
    assert sha(data) == f['sha256'] == f['full_file_sha256']
    assert len(data) == f['bytes']
    source_data[f['path']] = data
inventory = {r['id']: r for r in p['source_inventory']}
assert len(inventory) == len(p['source_inventory'])
ranges = set()
for r in inventory.values():
    data = source_data[r['path']]
    assert sha(data) == r['sha256'] == r['full_file_sha256']
    block = exact_range(data, r['line_start'], r['line_end'])
    assert sha(block) == r['range_sha256'] and len(block) == r['range_bytes']
    ranges.add((r['path'], r['line_start'], r['line_end']))
occurrences = 0
for claim in claims:
    for r in claim['sources']:
        assert r == inventory[r['id']], (claim['id'], r['id'])
        occurrences += 1

base = read_json(baseline / 'provenance.json')
old = {x['id']: x for x in base['claims']}
inherited = []
for entry in p['inherited_proof_inputs']:
    data = (root / entry['path']).read_bytes()
    assert sha(data) == entry['sha256'], entry['path']
    assert set(entry['claim_ids']) == {b['id'] for b in entry['claim_proof_blocks']}
    for block in entry['claim_proof_blocks']:
        assert block['id'] in old
        part = exact_range(data, block['line_start'], block['line_end'])
        assert sha(part) == block['sha256']
        recorded = old[block['id']]['proof_location']
        assert block['line_start'] <= recorded['line_start'] <= recorded['line_end'] <= block['line_end']
        assert sha(exact_range(data, recorded['line_start'], recorded['line_end'])) == recorded['sha256']
        # Older baseline entries sometimes exclude BEGIN/END markers; both ranges are checked.
        assert entry['path'].endswith('/' + recorded['file'])
        inherited.append({'id': block['id'], 'file': entry['path'], **block})
all_ids = set(old) | set(ids)
for claim in claims:
    assert set(claim['depends_on']) <= all_ids, claim['id']
seen, active = set(), set()
new = {x['id']: x for x in claims}
def visit(key):
    if key not in new or key in seen:
        return
    assert key not in active, key
    active.add(key)
    for child in new[key]['depends_on']:
        visit(child)
    active.remove(key)
    seen.add(key)
for key in ids:
    visit(key)
for key in ['builder', 'published_applications', 'corroborating_primary_references']:
    desc = p[key]
    assert sha((component / desc['file']).read_bytes()) == desc['sha256'], key
assert read_json(component / 'published_applications.json') == []

checks = {
'CCH1': 'Checked characteristic ell and exact constant Z_ell scalar map, full cyclotomic kernel Gprime, original polarization exponent, and full matrix span after inverting t. The residual kernel is not substituted for Gprime.',
'CCH2': 'Checked every Kap field for the chosen g=0 record: the odd block is zero at a=n, generation has exponent zero and empty coefficients, independence is vacuous, and every local boundary uses the zero correction.',
'CCH3': 'Checked the literal DD/eta-coordinate dictionary for TwZ, TwB and Detects, including cyclotomic twist, transpose sign, integral matrices and adic continuity. The rational trace condition is not mistaken for the endpoint.',
'CCH4': 'Checked descent of the trace-zero cocycle to a derivation of the full matrix algebra, its explicit matrix-unit inner derivation, and the central residual cocycle argument using chi(g0)-1. Nondegeneracy of the trace pairing needs no division by n or n!.',
'CCH5': 'Checked the transpose involution and averaging by 2, then clearing finitely many Laurent denominators. This yields the integral polarized TwB required by Detects and remains valid for n=4, ell=3.',
'CCH6': 'Checked the original N3 density scope and the closed trace-zero loci modulo every t power; separation of A gives exact trace vanishing on the full original Gprime.',
'CCH7': 'Checked PhiCond on the open residual-action kernel, finiteness of residual continuous cocycles, reduction kernel equal to t times the cocycle module, and the explicit coherent coefficient lifting. No unstated topological finite-generation or abstract module completeness premise is introduced.',
'CCH8': 'Checked selection of finitely many original separable elements through a basis of the row span over E. Vanishing on the finite list implies the full original Detects predicate. The empty-list case is allowed.',
'CCH9': 'Checked the trace-dual proof of integral-closure finiteness and freeness, locality by lifting finite-ring idempotents in the complete domain, the determinant-trick proof of a principal maximal ideal, and cofinal filtrations. Every nonzero ideal is a valuation power; the fraction field and residue field are the stated ones.',
'CCH10': 'Checked the finite-field Frobenius iteration giving the unique coefficient section, the exact power-series expansion, and the finite local inclusion j(t)=v*u^e with e>=1. Constants agree with the residue embedding. An unramified parameter equality is not assumed.',
'CCH11': 'Checked that one finite separable splitting extension suffices for the entire chosen list, that its roots are integral and distinct before reduction, and that the empty-list case takes the trivial extension.',
'CCH12': 'Checked every original NP field and all six NP.Ext conjuncts under that same map: integral form, full block and span, inertia and ordered flags, scalar character and N1 clauses. The finite-free extension and ramification preserve the actual adic continuity.',
'CCH13': 'Checked separability transport, N4 for every original subgroup via finite-free coordinates, including the separately retained old D0, and the full determinant polynomial law on every coefficient algebra. Original O-algebra and constant-field structures and the point kernel are preserved.',
'CCH14': 'Checked finite-free coordinate descent of the full polarized continuous cocycle, the use of j(t)^N Aprime=u^(e*N) Aprime, and the exact unit correction v^(-a) after a common exponent is chosen. The original finite detector survives unchanged.',
'CCH15': 'Checked all conjuncts of the literal h=0 Choice statement, including the one-point residue-cardinality condition. The same list, extension, point, g=0 Kap and eigenvalues are used together; no general multi-point or arbitrary-block closure is asserted.',
'CCH16': 'Checked the original B2 quantifiers directly: C=0 is chosen before all m; the proof works at every N; c=(1) has a unit coefficient; zero lies in every required Sel2 clause; the final Fin(0) equality is vacuous. This is for CCH15’s same g=0 Kap only.',
'CCH17': 'Checked the original same-J h=0 NiceI consumer, CIP normalization, CAP PhiCond/list realization, the unchanged old N4 and full residual determinant, the exact B1 parameter 4[Lplus:Q]+4T.q, and the coupled B2 witness. Both original Links and their fixed-iota/common-threshold order remain. Ordinary data, four Hida endpoints, same-J HasAut, B1, Raw and CohP are retained.'
}
assert set(checks) == set(ids)

review = {
 'schema': 'rh-independent-proof-review/1', 'artifact_version': '0.36',
 'reviewer': '/root/audit_global_routes', 'date': '2026-11-22',
 'component': 'count_choice', 'status': 'PASS', 'verdict': 'PASS',
 'scope': 'Independent full mathematical review of CCH1-CCH17 at their printed original-data scope, plus exact source-definition and inherited-consumer comparison. Formal correctness is assumed; this review concerns the human reconstruction.',
 'source_commit': pin, 'claims_reviewed': ids,
 'proof_file': 'count_choice/main.tex', 'provenance_file': 'count_choice/provenance.json',
 'closure_file': 'count_choice/closure.json',
 'proof_file_sha256': expected['main.tex'], 'main_sha256': expected['main.tex'],
 'provenance_file_sha256': expected['provenance.json'],
 'closure_file_sha256': expected['closure.json'],
 'proof_blocks': blocks,
 'per_claim_checks': [{'id': key, 'status': 'PASS', 'assessment': checks[key]} for key in ids],
 'source_validation': {
   'status': 'PASS', 'method': 'Independent SHA256 recomputation; source bytes compared with git show at the fixed pin; every cited inclusive line range and repeated claim/source occurrence checked against the inventory.',
   'pinned_files_verified': len(source_data), 'distinct_source_ranges_verified': len(ranges),
   'claim_source_occurrences_verified': occurrences, 'claim_proof_blocks_verified': len(blocks),
   'inherited_files_verified': len(p['inherited_proof_inputs']), 'inherited_proof_blocks_verified': len(inherited),
   'all_depends_on_ids_indexed': True, 'new_claim_dependency_graph_acyclic': True,
   'new_lean_build': False, 'source_definitions_and_key_consumers_read_independently': True
 },
 'inherited_blocks_verified': inherited,
 'scope_guards': c['quantifier_guards'],
 'closed_at_reviewed_scope': ['Original h=0 full-block Choice after NiceI normalization', 'Literal B2 for the SAME g=0 Kap chosen in that Choice', 'Conditional same-J support installation using these coupled outputs'],
 'not_claimed_closed': c['not_claimed_closed'],
 'issues_resolved': [{'id': 'CCH-R1', 'claim': 'CCH9', 'severity': 'wording', 'finding': 'The valuation argument concerns nonzero ideals; the original sentence omitted nonzero.', 'resolution': 'The final proof now says all nonzero ideals are powers of the maximal ideal. The revised text and hashes were rechecked.'}],
 'required_corrections': [],
 'classical_application_assessment': 'No published theorem is left as a new unproved application. The needed finite complete DVR statement is proved independently; the two Stacks references are corroborating general counterparts only.',
 'primary_references_checked': [
   {'url': 'https://stacks.math.columbia.edu/tag/032L', 'title': 'Lemma 10.161.8', 'role': 'Corroborates trace-dual finiteness for a finite separable extension of a Noetherian normal domain; not a premise.'},
   {'url': 'https://stacks.math.columbia.edu/tag/09E8', 'title': 'Remark 15.113.6', 'role': 'Corroborates the DVR integral-closure setting and unique prime for a complete base; not a premise.'}
 ],
 'review_limitations': 'All seventeen human proofs were reviewed mathematically and the listed byte bindings independently verified. This is not a new Lean build or a claim that Count II, the remaining deep producers, general Choice, or the arbitrary-Kap obstruction theorem are complete.',
}
out.mkdir(parents=True, exist_ok=True)
(out / 'count_choice_review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
txt = [
 'COUNT CHOICE CCH1-CCH17 — INDEPENDENT REVIEW', 'Version 0.36 | 2026-11-22 | /root/audit_global_routes',
 'Verdict: PASS. No required correction remains.', '',
 'Reviewed proof: count_choice/main.tex', 'SHA256: ' + expected['main.tex'],
 'Provenance SHA256: ' + expected['provenance.json'], 'Closure SHA256: ' + expected['closure.json'],
 'Pinned source: ' + pin, '',
 'The full original h=0, a=n Choice is reconstructed, with one finite list and one finite local coefficient extension. The second closure is the literal B2 on the very same constructed g=0 Kap. The coupled witness is essential: the chapter does not prove the general obstruction theorem for an arbitrary Kap.', '',
 'The proof covers residue characteristic three at rank four. The trace pairing uses matrix units, and the polarization correction divides only by two; no matrix-size or factorial denominator is introduced. The extension is allowed to ramify, with j(t)=v*u^e. The same finite detector survives through finite-free coordinates, while every original NP field, N4 at the old auxiliary subgroup, the complete determinant law and the point kernel are preserved.', '',
 'PER-CLAIM MATHEMATICAL COVERAGE', ''
 ]
for key in ids:
    txt += [key + ': PASS. ' + checks[key], '']
txt += [
 'SOURCE AND METADATA VERIFICATION',
 f'{len(blocks)} proof blocks; {len(source_data)} pinned source files; {len(ranges)} distinct inclusive source ranges; {occurrences} claim/source occurrences; {len(p["inherited_proof_inputs"])} inherited files with {len(inherited)} bound proof blocks independently verified.',
 'Every depends_on identifier is indexed in the baseline or this chapter, and the new claim graph is acyclic. The source bytes equal git show at the pin. No new Lean build was run.', '',
 'RESOLVED REVIEW FINDING',
 'CCH9 now correctly says every nonzero ideal is a power of the maximal ideal. This wording repair and the final cosmetic line breaks were checked on the final proof bytes.', '',
 'PRESERVED SCOPE',
 'CCH17 fixes J before the point, normalization, extension, list, realized Taylor-Wiles data and all levels. Its exact B1 input, same-J all-level HasAut and h=0 Raw input remain open, as do the original ordinary/control data, four additional Hida endpoints and CohP. Both rank-four Links remain necessary. The fixed-iota, common-threshold, then all later coefficients/Space/B/Lambda order is unchanged.',
 'RH and two-primary target routes still require Cases I, II and V. General Dirichlet targets retain the additional Case-III chain.', '',
 'PRIMARY REFERENCES',
 'The Stacks Project, Lemma 10.161.8 (tag 032L) and Remark 15.113.6 (tag 09E8), were checked as corroborating counterparts. CCH9-CCH10 provide the required complete equal-characteristic argument independently; these links introduce no new assumed theorem.', '',
 'The formal source is assumed correct. This PASS is a review of the human reconstruction at the exact conditional scopes above, not a declaration that the remaining proof frontier is closed.', ''
]
(out / 'count_choice_review.txt').write_text('\n'.join(txt))
print(json.dumps({'status': 'PASS', 'proof_sha256': expected['main.tex'],
  'review_json_sha256': sha((out / 'count_choice_review.json').read_bytes()),
  'review_txt_sha256': sha((out / 'count_choice_review.txt').read_bytes()),
  'source_files': len(source_data), 'source_ranges': len(ranges),
  'claim_source_occurrences': occurrences, 'inherited_blocks': len(inherited)}, indent=2))
