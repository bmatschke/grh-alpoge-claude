#!/usr/bin/env python3
"""Pin the exact original arithmetic specialization assembly and eleven fields."""
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
G = H + 'CoefficientRepTrivialOnUnramified.lean'
F = H + 'HeckeFixedLevelSpaces/AddOnePowEqRingHomImageAddPrimeMulZero.lean'
S = O + 'SpecIntIff.lean'

specs = {
 'coefficient_definition': (B+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean',10,15,'Coef: actual finite-Z_ell DVR subalgebra'),
 'co_algebra': (B+'CommutativeAlgebra/ResMapBijective.lean',9,34,'IsCO and its exact residue-field property'),
 'coefficient_point': (B+'SymplecticGSp4/CopNormLt.lean',139,146,'GradeZeroInterpolatingElement.coPt: first component used in spec'),
 'norm_tests': (S,12,43,'spec_intIff; spec_int; spec_unit'),
 'finite_character': (S,45,63,'spec_chi: actual compact-torus character into O-units'),
 'classical_dictionary': (S,65,96,'spec_cl: actual ClAt equals generic Cl'),
 'endpoint': (S,100,201,'UpperTheory.V.Hi.spec'),
 'original_hypotheses': (G,113,144,'Lev; lev; all original HSet.Ax fields'),
 'arithmetic_point': (G,149,185,'tauA; op; IsWt; finPart; Arith; tauC; Big'),
 'classical_operators': (G,216,234,'lowVal; opC; uzC; ClAt; OrdAt'),
 'eleven_fields': (G,236,251,'IsSpec and all eleven assertion fields'),
 'levels': (F,14,72,'lev_dir; mem_fixd_lev; lev_act'),
 'spherical_sums': (F,74,98,'lev_sph: one finite original list for every coefficient representation and level'),
 'torus_generation': (F,104,148,'elementary compact-torus generation; gen_Tc; Uc_anti; alV_mem'),
 'character_normalizations': (F,150,243,'chi_eV; chi_alV; exact z product over j=0,...,n-1'),
 'actual_weight_representation': (O+'ProdZpowConst.lean',95,259,'wtRep on original algRep with exact lowW character'),
 'single_map': (H+'HeckeFixedLevelSpaces/FreeMap.lean',425,587,'Sp.absSpec all original clauses'),
 'original_iwahori': (H+'TcAnti.lean',55,110,'piData; Kc; Uc; original uniformizers, positive monoid and depth c+1'),
 'original_low_weight': (H+'Distinct.lean',53,63,'algPow and lowW'),
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
    sources[sid] = {'id': 'ASP_SRC_'+sid.upper(), 'path': rel,
       'declaration': decl, 'line_start': start, 'line_end': end,
       'sha256': sha(data), 'full_file_sha256': sha(data),
       'range_sha256': sha(block), 'range_bytes': len(block),
       'source_commit': PIN, 'verified_equal_to_pinned_git_blob': True,
       'url': url+f'#L{start}-L{end}'}

relations = {
 1: (['WRP2'], ['coefficient_definition', 'norm_tests']),
 2: ([1, 'GA2', 'WRP2'], ['co_algebra', 'coefficient_point']),
 3: ([1, 2, 'WRP2', 'WRP12'], ['co_algebra', 'coefficient_definition', 'actual_weight_representation', 'endpoint']),
 4: ([3, 'WRP7', 'OST26', 'OST27'], ['finite_character', 'arithmetic_point', 'torus_generation', 'original_iwahori', 'original_low_weight']),
 5: ([4], ['classical_dictionary', 'arithmetic_point', 'classical_operators', 'torus_generation']),
 6: ([1, 3, 5, 'WRP7'], ['classical_operators', 'character_normalizations', 'original_iwahori']),
 7: ([], ['original_hypotheses', 'levels']),
 8: (['OHA1', 'OHA3'], ['original_hypotheses', 'spherical_sums']),
 9: ([3, 4, 5, 7, 'SMP10'], ['single_map', 'original_hypotheses', 'arithmetic_point', 'endpoint']),
 10: ([1, 5, 6, 8, 9, 'SMP2', 'SMP3', 'SMP9'], ['classical_operators', 'eleven_fields', 'endpoint']),
 11: ([6, 8, 9, 'SMP6', 'SMP7', 'SMP8', 'SMP9'], ['classical_operators', 'eleven_fields', 'endpoint']),
 12: ([7, 9, 'SMP9'], ['levels', 'eleven_fields', 'endpoint']),
 13: ([3, 4, 9, 10, 11, 12], ['eleven_fields', 'endpoint']),
}
tex = (HERE/'main.tex').read_text()
claims = []
for n, (deps, groups) in relations.items():
    cid = f'ASP{n}'
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', tex, re.S)
    assert match, cid
    block = match.group()
    start = tex[:match.start()].count('\n')+1
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n', block).group(1)
    claims.append({'id': cid, 'title': title, 'introduced_in': '0.42',
      'classification': 'B', 'status': 'complete human proof at the printed exact scope',
      'depends_on': [f'ASP{x}' if isinstance(x, int) else x for x in deps],
      'scope': 'shared RH and unrestricted Dirichlet GRH; exact original arithmetic specialization theorem',
      'original_hypotheses': ['L number field with specified algebraic closure; ell prime; n natural; original coefficient c; H:HSet with ALL original Ax fields (including ell!=2 and n>=1); A: IsCO(c.O); original theta satisfying H.IsWt; specified iota:Qbar_ell≃C; specified c.O-algebra point x:A->Qbar_ell; original dominant weight lambda satisfying H.Arith(theta,x,lambda).'],
      'classical_inputs': [],
      'proof_location': {'file': 'arithmetic_specialization_v42/main.tex', 'label': 'claim:'+cid,
        'line_start': start, 'line_end': start+block.count('\n')-1,
        'sha256': sha(block.encode()), 'bytes': len(block.encode())},
      'source_groups': groups, 'sources': [sources[g] for g in groups],
      'dependency_scope': 'Written mathematical proof; pinned source identifies all eleven fields and exact maps and is not used as an assumed-correct proof.'})

peer_components = {'WRP': 'weight_representation_v42', 'OST': 'ordinary_structure_v42',
                   'OHA': 'ordinary_hecke_algebra_v42', 'SMP': 'specialization_map_v42'}
peers = []
peer_ids = sorted({x for deps, _ in relations.values() for x in deps
                   if isinstance(x, str) and x != 'GA2'})
for cid in peer_ids:
    component = peer_components[cid[:3]]
    content = (ROOT/component/'main.tex').read_text()
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', content, re.S)
    assert match, cid
    peers.append({'claim': cid, 'file': component+'/main.tex',
      'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(content.encode()),
      'kind': 'peer', 'classification': 'B',
      'use': 'Actual coefficient DVR/weight representation, actual matrix Iwahori groups, integral spherical sums and level stability, or full original one-map specialization; only the proved scopes are used.'})

ga = (ROOT/'adic_realization/main.tex').read_text()
match = re.search(r'\\paragraph\{GA2:.*?(?=\n\\paragraph\{|\Z)', ga, re.S)
assert match
inherited = [{'claim': 'GA2', 'file': 'adic_realization/main.tex',
 'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(ga.encode()),
 'kind': 'inherited', 'classification': 'B',
 'use': 'The original coefficient fraction field is finite over Q_ell; finite-dimensional Q_ell subspaces are closed even in the uncompleted normed algebraic closure.'}]

fnl = (ROOT/'finite_levels_v42/main.tex').read_text()
match = re.search(r'% BEGIN FNL16\n.*?% END FNL16\n', fnl, re.S)
assert match
context_inputs = [{'claim': 'FNL16', 'file': 'finite_levels_v42/main.tex',
 'claim_sha256': sha(match.group().encode()), 'file_sha256': sha(fnl.encode()),
 'kind': 'peer context', 'use': 'The actual-datum H.Ax installation named in the closing scope note; the generic spec theorem still prints all its original H.Ax hypotheses.'}]

fields = {
 'alg': ['ASP3'], 'triv': ['ASP4'], 'fin': ['ASP10'],
 'stab': ['ASP10'], 'int': ['ASP1', 'ASP10'],
 'add': ['ASP11'], 'smul': ['ASP11'], 'span': ['ASP6', 'ASP11'],
 'indep': ['ASP11'], 'op': ['ASP11'], 'act': ['ASP12'],
}
contract = {
 'source_endpoint': 'UpperTheory.V.Hi.spec', 'source_file': S,
 'endpoint_claim': 'ASP13', 'consumer_structure': 'HSet.IsSpec',
 'assertion_fields': fields, 'assertion_field_count': len(fields),
 'coefficient_scope': 'Original A of class IsCO over c.O, possibly nonreduced; the given algebra point x is unchanged. Construct literal c.O<=c1.O<=c-prime.O inside the same Qbar_ell and the local codrestriction alpha(a)=x(a).',
 'fixed_embedding': 'The specified algebraic isomorphism iota:Qbar_ell≃C is retained everywhere and never assumed continuous.',
 'coefficient_point': 'ASP2 proves uniform |x(m_A^k)|<=eta^k, finite coefficient capture of the actual x, and hence its local realization; no compact-subset finite-field assertion is used.',
 'weight_representation': 'Exact WRP12 witness on algRep(n,H.S_l,iota,lambda), with its explicit intertwiner and unchanged lowW character.',
 'finite_character': 'phi(t)=alpha(theta(t))/psi(t), where psi is the unique O-unit preimage of chi on the compact torus; beta(phi(eV(v,i,y)))=iota(H.finPart(theta,x,lambda,v,i,y)).',
 'depth': 'Choose the original arithmetic witness e0 first, then c-star=max(e0,W.c0); original Tc(c-star) uses Uc(c-star+1), and IsSpec.triv retains this +1.',
 'classical_dictionary': 'Literal ClAt equals generic Cl at every K,e; Big UQ-invariance is supplied by U_K-invariance; elementary torus coordinates generate the full compact torus.',
 'ordinary_dictionary': 'Literal OrdAt equals generic ClOrd: same normalized z operator and norm-one iff IsIntUnit under the specified iota.',
 'normalization_indices': {'local_operator': 'Index (v,j) with j:Fin n uses alV(v,j+1) and lowVal(v,j+1)^(-1).', 'distinguished_operator': 'z=product_v product_{j=0}^{n-1} alV(v,j), and uzC uses precisely the matching product of lowVal(v,j).', 'spherical_operator': 'The original integral finite quotient-coset sum with its original representatives; no denominator or measure rescaling.'},
 'single_map': 'The SAME SMP good-lift map on the whole original ambient Fn A H.m supplies every level/depth, every basis and all operators; scalar is exactly iota(x(b)).',
 'auxiliary_action': 'Conjugating only the chosen auxiliary K_q gives one level K^g before the representation is chosen; singleton SMP9 gives the original act field, including its stated target-ordinarity premise.',
 'choice_order': 'Fix all original H, A, theta, iota, x and lambda. Choose the original Arith witness e0; capture x in c1; apply WRP for one c-prime and one algebraic weight representation; define one finite phi and c-star; establish original level/sum dictionaries; then define one ambient sp before any K,e,basis,operator or precision.',
 'original_hypotheses_retained': ['All eighteen H.Ax fields, including ell!=2 and n>=1', 'H.IsWt(theta), including continuity and original free stabilizers at every K', 'H.Arith(theta,x,lambda), with the given x and dominant weight', 'Original number fields, valuations, section maps, coefficient subalgebras and fixed iota'],
 'not_supplied': ['Arithmetic-point density or separation of the original Hecke algebra', 'Nonvanishing of a specified localized ordinary block at an arithmetic point', 'Same-original-ideal Hida construction with its complete automorphy and Galois conditions', 'Full COUNT_II_SUPPORT or any whole RH/GRH obligation'],
}
provenance = {
 'schema': 'rh-human-component-provenance/1', 'artifact_version': '0.42', 'date': '2026-11-23',
 'component': 'arithmetic_specialization_v42', 'source_commit': PIN,
 'main_tex_sha256': sha(tex.encode()), 'proof_file_sha256': sha(tex.encode()),
 'claims': claims, 'source_groups': sources, 'source_files': list(files.values()),
 'inherited_proof_inputs': inherited, 'peer_proof_inputs': peers,
 'context_proof_inputs': context_inputs, 'published_applications': [],
 'endpoint_contract': contract,
 'scope_note': 'Full original arithmetic spec with all eleven IsSpec fields, one map on actual functions, original point/embedding/finite character/operator normalizations and quantifiers. Arithmetic density, nonvanishing and same-ideal Hida remain distinct.',
 'validation': {'source_files_equal_to_pinned_git_blobs': True,
   'source_file_count': len(files), 'source_range_count': len(sources), 'claim_count': len(claims),
   'mathematical_claim_count_is_not_a_completion_percentage': True, 'no_lean_kernel_replay': True},
 'builder': {'file': 'arithmetic_specialization_v42/build_metadata.py', 'sha256': sha(Path(__file__).read_bytes())}}
(HERE/'provenance.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps({'source_commit': PIN, 'source_files': list(files.values()), 'ranges': sources}, indent=2)+'\n')
(HERE/'contract.json').write_text(json.dumps(contract, indent=2, ensure_ascii=False)+'\n')
(HERE/'closure.json').write_text(json.dumps({
 'schema': 'rh-exact-endpoint-closure/1', 'artifact_version': '0.42', 'main_tex_sha256': sha(tex.encode()),
 'completed': [{'endpoint': 'UpperTheory.V.Hi.spec', 'proof_claim': 'ASP13',
  'scope': 'Exact original H.Ax, IsCO, IsWt and Arith inputs; all eleven IsSpec fields on unchanged original arithmetic point, fixed iota, representation, coefficient maps and Hecke operators.'},
 {'endpoint': 'Actual arithmetic-point coefficient realization', 'proof_claim': 'ASP2–ASP3',
  'scope': 'The given x lands in a literal coefficient DVR extension and defines the required local A->O map with uniform ideal-power decay.'}],
 'whole_obligations_closed': [], 'remaining': contract['not_supplied'],
 'choice_order': contract['choice_order']}, indent=2, ensure_ascii=False)+'\n')
(HERE/'report.txt').write_text(
 'ORIGINAL ARITHMETIC SPECIALIZATION — v0.42\n\n'
 'Completed: the full original UpperTheory.V.Hi.spec endpoint in SpecIntIff.lean, with all eleven HSet.IsSpec assertion fields.\n\n'
 'The given algebra point x is captured in one literal finite coefficient DVR, with uniform ideal-power norm decay and the required local coefficient map. The constructed WtRep uses the unchanged algRep and specified iota. Its compact torus character produces the exact finite-part phi, trivial at the original c-star+1 depth.\n\n'
 'ClAt and OrdAt are identified as actual subspaces. Local opC uses alV(v,j+1); uzC uses the original product of lowVal(v,j) for j=0,...,n-1. Spherical operators use one original finite quotient list over every coefficient representation, without normalization changes. One ambient good-lift map supplies all levels, all bases, every Hecke operator and the auxiliary-group action.\n\n'
 f'Claims: ASP1–ASP13 ({len(claims)} complete B proofs). Source bytes: {len(files)} files, {len(sources)} ranges at the exact pin. No new class-A theorem import; no Lean replay.\n\n'
 'Exact scope: all original H.Ax, IsCO, IsWt and Arith premises remain, including ell!=2, n>=1, fixed iota and the given point x. Ell=3 is retained. No reducedness of A or injectivity/flatness of its specialization is added.\n\n'
 'Boundary: arithmetic density and point separation, nonvanishing at arithmetic fibers, and the same-original-ideal Hida/automorphy construction remain separate. No whole COUNT_II_SUPPORT or RH/GRH obligation is retired.\n')
print(json.dumps({'component': 'arithmetic_specialization_v42', 'claims': len(claims),
 'source_files': len(files), 'source_ranges': len(sources), 'proof_sha256': sha(tex.encode()), 'status': 'PASS'}))
