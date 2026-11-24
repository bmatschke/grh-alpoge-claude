#!/usr/bin/env python3
"""Pin the written exact algebraic WtRep producer and its source dictionary."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', required=True, type=Path)
args = parser.parse_args()
repo = args.repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
H = B + 'HeckeAlgebras/'
O = H + 'OrdinaryHeckeCharacters/'
R = B + 'BuildingsResidueChars/'

specs = {
 'coefficient_definition': (B+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean',10,15,'Coef: actual DVR subalgebra of PadicAlgCl finite over Z_l'),
 'local_integrality': (R+'ExpCharIntegralityCriterion.lean',1,None,'expChar_integrality_criterion; comparison with the elementary norm-ball coefficient extension'),
 'polynomial_definition': ('src/Formalism/LocalRingCardinality/DataCoeff.lean',13,63,'DomWeight; detShift; natW; nablaSq; detPow; sqAct'),
 'polynomial_kernel': ('src/Formalism/GradedWeylDivisibility/StatementA.lean',10,35,'column multidegree and generic colAddGen kernel; rowAct'),
 'sq_rep': ('src/Development/AbelianVarietyTheory/PublishedTheorems/PublishedFoundations/FiniteIntertwining.lean',14,40,'sqRep and its literal polynomial action'),
 'original_iwahori': (H+'TcAnti.lean',55,110,'piData; Kc; actual unif; glData, positive monoid and z'),
 'original_representation': (H+'CoefficientRepTrivialOnUnramified.lean',20,68,'GV; iwS; Emb; Emb.res; algRep; IsAlgWt'),
 'original_character': (H+'Distinct.lean',53,63,'algPow; Wt; lowW'),
 'ten_fields': (H+'ContinuousTorusCharacter.lean',269,287,'WtRep and all ten assertion fields'),
 'basis_contract': (O+'SqBasis.lean',1,None,'sqBasis: auxiliary original generic-domain contract, replaced only at the required actual DVR scope'),
 'basis_packaging': (O+'ProdZpowConst.lean',1,76,'ofBasis: generic weight-matrix packaging'),
 'tensor_congruence': (O+'ProdZpowConst.lean',78,93,'prod_delta: finite tensor-product congruence'),
 'endpoint': (O+'ProdZpowConst.lean',95,259,'UpperTheory.V.Hi.wtRep'),
 'downstream_scope': (O+'SpecIntIff.lean',100,160,'spec: arithmetic coefficient point, wtRep, finite part and absSpec installation'),
}
files = {}
sources = {}
for sid, (rel, start, end, decl) in specs.items():
    data = (repo/rel).read_bytes()
    pinned = subprocess.run(['git', 'show', PIN+':'+rel], cwd=repo,
                            check=True, stdout=subprocess.PIPE).stdout
    assert data == pinned, rel
    lines = data.splitlines(keepends=True)
    end = end or len(lines)
    assert 1 <= start <= end <= len(lines), (sid, start, end, len(lines))
    block = b''.join(lines[start-1:end])
    url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel] = {'path': rel, 'sha256': sha(data), 'bytes': len(data),
                  'line_count': len(lines), 'url': url,
                  'verified_equal_to_pinned_git_blob': True}
    sources[sid] = {'id': 'WRP_SRC_'+sid.upper(), 'path': rel,
       'declaration': decl, 'line_start': start, 'line_end': end,
       'sha256': sha(data), 'full_file_sha256': sha(data),
       'range_sha256': sha(block), 'range_bytes': len(block),
       'source_commit': PIN, 'verified_equal_to_pinned_git_blob': True,
       'url': url+f'#L{start}-L{end}'}

relations = {
 1: (['GA2'], ['local_integrality', 'original_representation']),
 2: ([1, 'GA2'], ['coefficient_definition', 'local_integrality', 'endpoint']),
 3: ([2, 'HP1'], ['polynomial_definition', 'polynomial_kernel', 'sq_rep', 'basis_contract']),
 4: ([3, 'HP1'], ['polynomial_definition', 'basis_contract']),
 5: ([4, 'HP1', 'HP2'], ['basis_contract']),
 6: ([4, 5], ['original_representation', 'basis_packaging']),
 7: ([1, 5, 6, 'OST26', 'OST27'], ['original_character', 'original_representation', 'ten_fields', 'endpoint']),
 8: ([2, 3, 4, 6, 'OST26', 'OST27'], ['original_iwahori', 'ten_fields', 'endpoint']),
 9: ([2, 5, 6, 7, 'OST26', 'OST27'], ['original_iwahori', 'ten_fields', 'endpoint']),
 10: ([2, 3, 6, 7, 'OST26', 'OST27'], ['original_iwahori', 'ten_fields', 'tensor_congruence', 'endpoint']),
 11: ([5, 6, 7], ['ten_fields', 'endpoint']),
 12: ([2, 6, 7, 8, 9, 10, 11], ['coefficient_definition', 'original_representation', 'original_character', 'ten_fields', 'endpoint', 'downstream_scope']),
}
tex = (HERE/'main.tex').read_text()
claims = []
for n, (deps, groups) in relations.items():
    cid = f'WRP{n}'
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', tex, re.S)
    assert match, cid
    block = match.group()
    start = tex[:match.start()].count('\n')+1
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n', block).group(1)
    claims.append({'id': cid, 'title': title, 'introduced_in': '0.42',
      'classification': 'B', 'status': 'complete human proof at the printed exact scope',
      'depends_on': [f'WRP{x}' if isinstance(x, int) else x for x in deps],
      'scope': 'shared RH and unrestricted Dirichlet GRH; exact original actual-DVR algebraic weight representation supplier',
      'original_hypotheses': ['L number field; ell any prime; n any natural number; finite V and original finite places S(v); specified algebraic field isomorphism iota:Qbar_ell->C; arbitrary original dominant integral weight function; c the original finite-Z_ell DVR subalgebra of Qbar_ell.'],
      'classical_inputs': [],
      'proof_location': {'file': 'weight_representation_v42/main.tex', 'label': 'claim:'+cid,
        'line_start': start, 'line_end': start+block.count('\n')-1,
        'sha256': sha(block.encode()), 'bytes': len(block.encode())},
      'source_groups': groups, 'sources': [sources[g] for g in groups],
      'dependency_scope': 'Written mathematical proof; pinned source declarations identify actual objects and endpoints and do not substitute for the written argument.'})

inherited = []
for component, ids in [('chain_closure_core', ['HP1', 'HP2']),
                       ('adic_realization', ['GA1', 'GA2'])]:
    p = ROOT/component/'main.tex'
    content = p.read_text()
    for cid in ids:
        match = re.search(r'\\paragraph\{'+cid+r':.*?(?=\n\\paragraph\{|\Z)', content, re.S)
        assert match, (component, cid)
        inherited.append({'claim': cid, 'file': component+'/main.tex',
          'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(content.encode()),
          'kind': 'inherited', 'classification': 'B',
          'use': 'Exact characteristic-zero polynomial kernel/base change/highest line/absolute irreducibility, or actual coefficient DVR norm and finite-dimensional closed-image facts; retained at their written scopes.'})

ost = (ROOT/'ordinary_structure_v42/main.tex').read_text()
peers = []
for cid in ['OST26', 'OST27']:
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', ost, re.S)
    assert match, cid
    peers.append({'claim': cid, 'file': 'ordinary_structure_v42/main.tex',
      'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(ost.encode()),
      'kind': 'peer', 'classification': 'B',
      'use': 'All actual glIwa/piIwa fields and the original compact groups, principal congruences, positive exponents and uniformizers.'})

fields = {
 'int_N': ['WRP8'],
 'integral_torusCharacter': ['WRP8'],
 'int_Nm': ['WRP8'],
 'int_P': ['WRP9'],
 'row_N': ['WRP7'],
 'torusAction': ['WRP7'],
 'nilpotent_central_action': ['WRP9'],
 'cont_Nm': ['WRP10'],
 'continuous_torusCharacter': ['WRP10'],
 'central': ['WRP11'],
}
contract = {
 'source_endpoint': 'UpperTheory.V.Hi.wtRep', 'endpoint_claim': 'WRP12',
 'original_representation': 'algRep S iota lambda on the literal tensor product over Emb ell S of nablaSq C n (lambda e.res)',
 'coefficient_scope': 'For every original c:Coef ell, construct c-prime:Coef ell with literal subalgebra inclusion c.O<=c-prime.O inside the same Qbar_ell.',
 'coefficient_map': 'The exact specified iota restricted to c-prime.O; no continuity of iota assumed.',
 'local_maps': 'Restrictions of the original continuous field embeddings j:F_v->Qbar_ell, with maximal ideal powers carried into the corresponding powers.',
 'wt_rep_assertion_fields': fields,
 'assertion_field_count': len(fields),
 'character_identity': 'chi(diag y)=iota(product_v product_i algPow(S(v),lowW(lambda,i),y_vi)), exactly the original finite-support product and reversed weight.',
 'is_alg_wt_witness': 'The explicit complex tensor basis coordinate isomorphism B in WRP6 intertwines the constructed matrices with the unchanged original algRep.',
 'positive_operator_normalization': 'Uses the original local uniformizers and antitone exponent tuples; the normalized entry is product_e phi_e(varpi_v)^Delta_e with every Delta_e>=0 and some Delta_e>0 outside column zero for the original z.',
 'choice_order': 'Fix L, ell, n, V, S, iota, lambda and c; form one finite compositum and coefficient DVR c-prime; choose one saturated integral weight basis for each factor and one tensor reindexing with lowest coordinate zero. The witness R is then fixed before any depth or precision. Set c0=0; for every precision k choose c=k.',
 'permitted_simplification': 'Only the existential actual-DVR wtRep endpoint is claimed. Saturated lattices, HP1-HP2, and the dense Gaussian cell replace the source generic-domain standard-monomial SqBasis proof. No identity with that auxiliary chosen basis is required or asserted.',
 'edge_cases_retained': ['ell=2 and ell=3', 'n=0', 'n=1', 'empty V', 'empty local embedding sets', 'negative determinant shifts', 'arbitrary dominant integer weights'],
 'source_conclusions': ['c.O<=c-prime.O as actual subalgebras', 'R:WtRep(iwS n S,c-prime.O,C) with all ten fields', 'IsAlgWt iota lambda R.xi', 'Exact original lowW/algPow character identity'],
 'not_supplied': ['Entire generic SqBasis theorem over arbitrary domains (unneeded for the proved existential endpoint)', 'Arithmetic coefficient point and finite-part character selected in SpecIntIff.spec', 'Full one-map specialization assembly over all levels', 'Nonvanishing or arithmetic separation of Hecke blocks', 'Same-ideal Hida/automorphy endpoints', 'Full COUNT_II_SUPPORT'],
}
provenance = {
 'schema': 'rh-human-component-provenance/1', 'artifact_version': '0.42', 'date': '2026-11-23',
 'component': 'weight_representation_v42', 'source_commit': PIN,
 'main_tex_sha256': sha(tex.encode()), 'proof_file_sha256': sha(tex.encode()),
 'claims': claims, 'source_groups': sources, 'source_files': list(files.values()),
 'inherited_proof_inputs': inherited, 'peer_proof_inputs': peers, 'published_applications': [],
 'endpoint_contract': contract,
 'scope_note': 'Exact original wtRep producer on the actual algebraic representation and coefficient embedding; the generic arbitrary-domain SqBasis auxiliary theorem and full arithmetic specialization are not asserted.',
 'validation': {'source_files_equal_to_pinned_git_blobs': True,
   'source_file_count': len(files), 'source_range_count': len(sources), 'claim_count': len(claims),
   'mathematical_claim_count_is_not_a_completion_percentage': True, 'no_lean_kernel_replay': True},
 'builder': {'file': 'weight_representation_v42/build_metadata.py', 'sha256': sha(Path(__file__).read_bytes())}}
(HERE/'provenance.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps({'source_commit': PIN, 'source_files': list(files.values()), 'ranges': sources}, indent=2)+'\n')
(HERE/'contract.json').write_text(json.dumps(contract, indent=2, ensure_ascii=False)+'\n')
(HERE/'closure.json').write_text(json.dumps({
 'schema': 'rh-exact-endpoint-closure/1', 'artifact_version': '0.42', 'main_tex_sha256': sha(tex.encode()),
 'completed': [{'endpoint': 'UpperTheory.V.Hi.wtRep', 'proof_claim': 'WRP12',
  'scope': 'All original quantified number-field, prime, rank, place, embedding, dominant-weight and coefficient inputs; actual algRep; all ten WtRep fields; exact lowW character.'},
 {'endpoint': 'Common actual coefficient DVR for all continuous local embeddings', 'proof_claim': 'WRP2',
  'scope': 'Literal finite-Z_ell DVR subalgebra extension inside the specified Qbar_ell; original local maps and every maximal-ideal power.'}],
 'whole_obligations_closed': [], 'remaining': contract['not_supplied'],
 'choice_order': contract['choice_order']}, indent=2, ensure_ascii=False)+'\n')
(HERE/'report.txt').write_text(
 'ACTUAL ALGEBRAIC WEIGHT REPRESENTATION — v0.42\n\n'
 'Completed: the exact original ProdZpowConst.wtRep existential supplier for every original input, with the actual algRep, specified algebraic isomorphism iota, one coefficient DVR extending the given c, all ten WtRep assertion fields, and the original lowW/algPow character identity.\n\n'
 'Simplification: the actual coefficient ring is a DVR. Intersecting the characteristic-zero polynomial kernel with the finite integral polynomial module gives a saturated free lattice. Row-weight projections give an integral weight basis. The already proved HP1–HP2 and dense Gaussian cell produce the unique lowest weight and all required dominance inequalities. This avoids reconstructing the unneeded generic-domain standard-monomial basis theorem while preserving the exact original existential endpoint.\n\n'
 'Integral precision: c0=0; depth c=k supplies every precision k. Positive normalization uses the original local uniformizers, and outside column zero the distinguished normalized z has entries in the actual maximal ideal. No continuity of iota is assumed.\n\n'
 f'Claims: WRP1–WRP12 ({len(claims)} complete B proofs). Source bytes: {len(files)} files, {len(sources)} ranges at the exact pin. No new class-A theorem import; no Lean replay.\n\n'
 'Exact scope retains all primes (including 2 and 3), rank zero, empty index sets, negative determinant shifts, and every dominant integral weight. The basis witness is explicitly intertwined with the unchanged algRep; no equality with the source auxiliary chosen basis is asserted.\n\n'
 'Boundary: the arithmetic coefficient point, finite-part character, complete one-map specialization, nonvanishing/arithmetic fibers and same-ideal Hida/automorphy remain separately supplied. No whole COUNT_II_SUPPORT obligation is retired.\n')
print(json.dumps({'component': 'weight_representation_v42', 'claims': len(claims),
 'source_files': len(files), 'source_ranges': len(sources), 'proof_sha256': sha(tex.encode()), 'status': 'PASS'}))
