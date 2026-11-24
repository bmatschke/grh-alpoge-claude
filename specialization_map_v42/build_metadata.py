#!/usr/bin/env python3
"""Pin the written exact single-map ordinary specialization supplier."""
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
F = H + 'HeckeFixedLevelSpaces/FreeMap.lean'

specs = {
 'definitions': (H+'ContinuousTorusCharacter.lean',269,365,'WtRep; AF; raF; Cl; UF; ClOrd; ctrl'),
 'free_and_coefficients': (F,14,31,'free_map; mapFn_ra'),
 'away_integrality': (F,33,260,'hecke_eigenvalue_isIntegral and finite-value suppliers'),
 'level_and_control': (F,262,327,'cl_mono; ctrl_raF_comm; ctrl_UF_eq_U_ctrl; mapFn_of_mem_P'),
 'positive_ordinary': (F,328,369,'UF_comm_on_N_fixed; UF_maps_clOrd_of_maps_cl'),
 'away_ordinary': (F,371,423,'sum_raF_rpF_comm; raF_mem_pi_AF; sum_raF_maps_clOrd_of_maps_fixd'),
 'endpoint': (F,425,587,'UpperTheory.V.Hi.Sp.absSpec'),
 'finite_classical': (O+'ClFinMulVec.lean',1,None,'clFin: finite-dimensionality, positive stability and eigenvalue integrality'),
 'ordinary_basechange': (O+'OrdBCMapOrd.lean',1,None,'ordBC on the original coefficientwise map'),
 'control': (O+'CtrlOrd.lean',220,371,'ctrlOrd exact original injectivity and image statement'),
 'function_independence': (O+'FnIndep.lean',1,None,'fnIndep over a domain embedded in a field'),
 'downstream_scope': (O+'SpecIntIff.lean',100,200,'spec: exact arithmetic installation and coefficient/operator dictionaries'),
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
    sources[sid] = {'id': 'SMP_SRC_'+sid.upper(), 'path': rel,
       'declaration': decl, 'line_start': start, 'line_end': end,
       'sha256': sha(data), 'full_file_sha256': sha(data),
       'range_sha256': sha(block), 'range_bytes': len(block),
       'source_commit': PIN, 'verified_equal_to_pinned_git_blob': True,
       'url': url+f'#L{start}-L{end}'}

relations = {
 1: (['OST19', 'OST24'], ['free_and_coefficients', 'ordinary_basechange']),
 2: ([1, 'OCT3', 'OCT6', 'OCT7', 'OCT10', 'OCT15'], ['definitions', 'finite_classical', 'control']),
 3: ([2, 'OCT6'], ['away_integrality', 'finite_classical']),
 4: (['OCT17', 'OCT18'], ['level_and_control', 'control']),
 5: ([1, 2, 4], ['endpoint']),
 6: ([5, 'OST10'], ['endpoint']),
 7: ([1, 2, 5, 'OCT16'], ['endpoint', 'ordinary_basechange', 'function_independence']),
 8: ([5, 'OST5', 'OST20', 'OCT4', 'OCT18'], ['positive_ordinary', 'level_and_control', 'endpoint']),
 9: ([5, 'OCT4', 'OCT19'], ['free_and_coefficients', 'away_ordinary', 'endpoint']),
 10: ([2, 3, 5, 6, 7, 8, 9], ['definitions', 'endpoint', 'downstream_scope']),
}
tex = (HERE/'main.tex').read_text()
claims = []
for n, (deps, groups) in relations.items():
    cid = f'SMP{n}'
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', tex, re.S)
    assert match, cid
    block = match.group()
    start = tex[:match.start()].count('\n')+1
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n', block).group(1)
    claims.append({'id': cid, 'title': title, 'introduced_in': '0.42',
      'classification': 'B', 'status': 'complete human proof at the printed exact scope',
      'depends_on': [f'SMP{x}' if isinstance(x, int) else x for x in deps],
      'scope': 'shared RH and unrestricted Dirichlet GRH; exact original generic all-level single-map ordinary specialization',
      'original_hypotheses': ['Original Frame; CNL A and CNL domain O; arbitrary local alpha:A->O; specified injection beta:O->Omega with Omega algebraically closed and specified A->Omega=beta alpha; all ten WtRep fields; original tau, continuous theta, phi, depth c and character balance; downward-directed family U_K with original FinLevel/Free at every K.'],
      'classical_inputs': [],
      'proof_location': {'file': 'specialization_map_v42/main.tex', 'label': 'claim:'+cid,
        'line_start': start, 'line_end': start+block.count('\n')-1,
        'sha256': sha(block.encode()), 'bytes': len(block.encode())},
      'source_groups': groups, 'sources': [sources[g] for g in groups],
      'dependency_scope': 'Written mathematical proof; pinned source identifies exact quantifiers and actual functions, not an assumed-correct theorem invocation.'})

peers = []
peer_ids = sorted({x for deps, _ in relations.values() for x in deps if isinstance(x, str)})
for cid in peer_ids:
    component = 'ordinary_structure_v42' if cid.startswith('OST') else 'ordinary_control_v42'
    content = (ROOT/component/'main.tex').read_text()
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', content, re.S)
    assert match, cid
    peers.append({'claim': cid, 'file': component+'/main.tex',
      'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(content.encode()),
      'kind': 'peer', 'classification': 'B',
      'use': 'Original finite free ordinary module/base change, or actual classical lattice/control/integral operator compatibility; all original hypotheses retained.'})

contract = {
 'source_endpoint': 'UpperTheory.V.Hi.Sp.absSpec', 'endpoint_claim': 'SMP10',
 'coefficient_scope': 'A arbitrary CNL, including nonreduced; O original CNL DOMAIN; alpha:A->O arbitrary LOCAL map, including nonflat/noninjective; beta:O->Omega specified injection into algebraically closed field; exact scalar tower.',
 'ordinary_map': 'j_K(f)=pointwise alpha(f); O tensor_A M_K is the exact original ordinary base change.',
 'specialization_domain': 'The entire original X.Fn A m, not only the union of ordinary modules.',
 'specialization_codomain': 'Fin m -> X.Fn Omega (W.d+1), the original ambient classical families.',
 'specialization_definition': 'The unique F that lies in some original ClOrd(U_K,e), e>=c, and has ctrl(F)=pointwise beta alpha(f), when such F exists; zero otherwise.',
 'choice_order': 'Fix all original ring, embedding, character, WtRep and directed-level data. Prove uniqueness across levels by a common refinement and maximum depth. Define one sp on all ambient functions before K,e,basis,precision,positive operator or away sum is selected.',
 'conclusions': {
  'finite_classical': ['SMP2'], 'positive_classical_stability': ['SMP2'],
  'positive_eigenvalue_integrality': ['SMP3'], 'arbitrary_away_sum_eigenvalue_integrality': ['SMP3'],
  'additivity': ['SMP6'], 'semilinearity': ['SMP6'],
  'ordinary_span_every_level_depth': ['SMP7'], 'independence_of_every_A_basis': ['SMP7'],
  'positive_operator_compatibility': ['SMP8'], 'full_away_sum_compatibility': ['SMP9']},
 'away_sum_hypothesis': 'Exactly the source: the Omega-valued finite sum carries every U_K-fixed ambient family into the U_K-prime-fixed ambient space. No assumption that the resulting A-valued function is ordinary is added.',
 'eigenvalue_hypothesis': 'A nonzero classical eigenvector for any positive normalized operator or any finite indexed away sum. For away integrality no classical-space preservation hypothesis is added.',
 'simplification': 'The finite O-module of all untwisted coordinates is generated by finite coset evaluations. Any eigenoperator preserves this module, so the adjugate determinant trick proves integrality without requiring its image to lie in the original classical level.',
 'additional_proved_results': ['On every M_K the same sp is the actual integral inverse q_K,e^-1 after original coefficientwise base change.', 'Omega tensor_A M_K maps isomorphically onto the literal classical ordinary space for every e>=c.'],
 'not_supplied': ['Arithmetic coefficient realization, finite-part character and operator dictionary of full SpecIntIff.spec (separate packet)', 'Arithmetic density or point separation of Hecke blocks', 'Nonvanishing or same-ideal Hida/automorphy endpoints', 'Full COUNT_II_SUPPORT'],
}
provenance = {
 'schema': 'rh-human-component-provenance/1', 'artifact_version': '0.42', 'date': '2026-11-23',
 'component': 'specialization_map_v42', 'source_commit': PIN,
 'main_tex_sha256': sha(tex.encode()), 'proof_file_sha256': sha(tex.encode()),
 'claims': claims, 'source_groups': sources, 'source_files': list(files.values()),
 'inherited_proof_inputs': [], 'peer_proof_inputs': peers, 'published_applications': [],
 'endpoint_contract': contract,
 'scope_note': 'Exact generic absSpec, retaining all original all-level, basis, eigenvalue and away-sum quantifiers; no additional A-ordinarity for the away-sum image.',
 'validation': {'source_files_equal_to_pinned_git_blobs': True,
   'source_file_count': len(files), 'source_range_count': len(sources), 'claim_count': len(claims),
   'mathematical_claim_count_is_not_a_completion_percentage': True, 'no_lean_kernel_replay': True},
 'builder': {'file': 'specialization_map_v42/build_metadata.py', 'sha256': sha(Path(__file__).read_bytes())}}
(HERE/'provenance.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps({'source_commit': PIN, 'source_files': list(files.values()), 'ranges': sources}, indent=2)+'\n')
(HERE/'contract.json').write_text(json.dumps(contract, indent=2, ensure_ascii=False)+'\n')
(HERE/'closure.json').write_text(json.dumps({
 'schema': 'rh-exact-endpoint-closure/1', 'artifact_version': '0.42', 'main_tex_sha256': sha(tex.encode()),
 'completed': [{'endpoint': 'UpperTheory.V.Hi.Sp.absSpec', 'proof_claim': 'SMP10',
  'scope': 'All original local coefficient maps, all directed levels, every classical depth, every basis, every positive operator and the complete original finite away-sum and eigenvalue quantifiers.'}],
 'whole_obligations_closed': [], 'remaining': contract['not_supplied'],
 'choice_order': contract['choice_order']}, indent=2, ensure_ascii=False)+'\n')
(HERE/'report.txt').write_text(
 'SINGLE-MAP ORDINARY SPECIALIZATION — v0.42\n\n'
 'Completed: exact UpperTheory.V.Hi.Sp.absSpec, including finite classical spaces, positive stability, both eigenvalue-integrality clauses, and one ambient specialization map with all six source assertions.\n\n'
 'The map is the unique good lift under original control after the specified coefficient map, and is zero only where no good lift exists. Directedness and common-depth injectivity give uniqueness across every original level. Its domain is the whole ambient A-valued function space; this preserves the source away-sum conclusion without an added A-ordinarity assumption.\n\n'
 'Eigenvalue integrality uses the finite O-module generated by all untwisted values, which finite original coset representatives generate. Integral normalized and away matrices preserve that module, and the determinant trick yields the original monic equation.\n\n'
 f'Claims: SMP1–SMP10 ({len(claims)} complete B proofs). Source bytes: {len(files)} files, {len(sources)} ranges at the exact pin. No new class-A theorem import; no Lean replay.\n\n'
 'Exact scope: arbitrary CNL source A, original CNL domain target O, arbitrary local alpha (including nonflat/noninjective), fixed injective O->Omega and scalar tower, all ten WtRep fields and all original level/character assumptions.\n\n'
 'Boundary: full arithmetic SpecIntIff.spec assembly is separately supplied. Arithmetic density, nonvanishing and same-ideal Hida/automorphy remain separate. No whole COUNT_II_SUPPORT obligation is retired.\n')
print(json.dumps({'component': 'specialization_map_v42', 'claims': len(claims),
 'source_files': len(files), 'source_ranges': len(sources), 'proof_sha256': sha(tex.encode()), 'status': 'PASS'}))
