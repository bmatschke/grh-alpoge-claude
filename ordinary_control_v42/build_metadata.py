#!/usr/bin/env python3
"""Pin the written classical-control proof and every endpoint dictionary."""
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
F = B + 'AlgebraTools/HidaCompleteRings/'

specs = {
 'classical_definitions': (H+'ContinuousTorusCharacter.lean',264,365,'IsIntUnit; WtRep; AF; rpF; raF; Cl; UF; ClOrd; ctrl'),
 'lattice_definitions': (H+'CtrlDefs.lean',1,None,'mIm; unt; Lat; ClO'),
 'character': (R+'ExistsIwahoriCharacterExtendingTorusCharacter.lean',1,None,'exists_iwahori_character_extending_torus_character'),
 'coset_interpolation': (R+'ExistsAutomorphicFunctionWithValuesOnCosetReps.lean',1,None,'exists_automorphic_function_with_values_on_coset_reps'),
 'classical_interpolation': (R+'ExistsAutomorphicFormWithPrescribedIwahoriValues.lean',1,None,'exists_automorphicForm_with_prescribed_iwahori_values'),
 'lattice_evaluation': (R+'MemLatticeOfValuesAtDoubleCosetReps.lean',1,None,'mem_lattice_of_values_at_double_coset_reps'),
 'control_equivariance': (O+'CtrlEq.lean',1,None,'ctrlEq_row; ctrlEq'),
 'integral_control': (R+'ExistsIntegralFormLiftingControlMap.lean',1,None,'exists_integral_form_lifting_controlMap'),
 'contraction': (R+'UpOperatorMapsLatticeOfControlValues.lean',1,None,'Up_operator_maps_lattice_of_control_values'),
 'classical_levels': (R+'ClassicalFormsLevelMonotoneAndUpStable.lean',1,None,'classicalForms_level_monotone_and_Up_stable'),
 'operator_levels': (O+'UOpLevel.lean',1,None,'uOpLevel'),
 'spectral_lattice': (R+'ExistsFreeLatticeSpanningOrdinaryPart.lean',1,None,'exists_free_lattice_spanning_ordinary_part'),
 'spectral_equality': (R+'SpanOrdinaryPartEqSupUnitGeneralizedEigenspaces.lean',1,None,'span_ordinaryPart_eq_sup_unit_generalized_eigenspaces'),
 'spectral_integrality': (F+'EigOrdInt.lean',1,None,'eigOrdInt'),
 'periodic_kernel': (O+'CtrlOrd.lean',15,138,'ctrlOrd_per; ctrlOrd_val; ctrlOrd_valU; ctrlOrd_map; ctrlOrd_nat; ctrlOrd_stab; ctrlOrd_inj'),
 'fixed_depth_approximation': (O+'CtrlOrd.lean',140,216,'ctrlOrd_approx'),
 'independence': (O+'FnIndep.lean',1,None,'fnIndep'),
 'span_injectivity': (R+'InjectiveOnSpanOfIntegralFreeSubmodule.lean',1,None,'injective_on_span_of_integral_free_submodule'),
 'endpoint': (O+'CtrlOrd.lean',220,371,'UpperTheory.V.Hi.ctrlOrd'),
 'downstream_scope': (O+'SpecIntIff.lean',100,160,'spec: actual WtRep and finite-coefficient-extension suppliers before absSpec'),
}
files = {}
sources = {}
for sid,(rel,start,end,decl) in specs.items():
    data = (repo/rel).read_bytes()
    pinned = subprocess.run(['git','show',PIN+':'+rel],cwd=repo,
                            check=True,stdout=subprocess.PIPE).stdout
    assert data == pinned, rel
    lines = data.splitlines(keepends=True)
    end = end or len(lines)
    assert 1 <= start <= end <= len(lines), (sid,start,end,len(lines))
    block = b''.join(lines[start-1:end])
    url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),
                  'line_count':len(lines),'url':url,
                  'verified_equal_to_pinned_git_blob':True}
    sources[sid] = {'id':'OCT_SRC_'+sid.upper(),'path':rel,
       'declaration':decl,'line_start':start,'line_end':end,
       'sha256':sha(data),'full_file_sha256':sha(data),
       'range_sha256':sha(block),'range_bytes':len(block),
       'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,
       'url':url+f'#L{start}-L{end}'}

relations = {
1: (['OST2'],['character']),
2: ([1,'OST1'],['coset_interpolation','classical_interpolation']),
3: ([2,'OST1'],['lattice_evaluation']),
4: ([],['control_equivariance']),
5: ([4],['integral_control','endpoint']),
6: ([],['contraction']),
7: ([4,6,'OST5','OST6'],['classical_levels','operator_levels']),
8: (['OST17'],['spectral_lattice']),
9: ([8],['spectral_equality','spectral_integrality']),
10: ([3,7,8,9],['spectral_lattice','spectral_equality']),
11: ([6],['periodic_kernel']),
12: ([4,5,10,11,'OST5','OST10'],['periodic_kernel','endpoint']),
13: ([2,3,4,5,6,7,'OST1','OST4','OST5','OST7','OST10'],['fixed_depth_approximation']),
14: ([4,10,12,13,'OST5','OST16'],['endpoint']),
15: ([5,12,14,'OST19'],['endpoint']),
16: ([],['independence','span_injectivity']),
17: ([10,15,16],['endpoint','classical_definitions','lattice_definitions']),
18: ([4,6,7,8,10,12,15,'OST5','OST20'],['control_equivariance','classical_levels','operator_levels']),
19: ([3,4,8],['control_equivariance','spectral_lattice']),
}
tex = (HERE/'main.tex').read_text()
claims = []
for n,(deps,groups) in relations.items():
    cid = f'OCT{n}'
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',tex,re.S)
    assert match, cid
    block = match.group()
    start = tex[:match.start()].count('\n')+1
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    claims.append({'id':cid,'title':title,'introduced_in':'0.42',
      'classification':'B','status':'complete human proof at the printed exact scope',
      'depends_on':[f'OCT{x}' if isinstance(x,int) else x for x in deps],
      'scope':'shared RH and unrestricted Dirichlet GRH; exact original domain-valued generic control interface',
      'original_hypotheses':['Original Frame with every Iwa field; FinLevel and Free at the stated U; complete Noetherian local domain O with finite residue field; specified injective O->Omega with Omega algebraically closed; all ten WtRep assertion fields; c>=c0; phi trivial on Tc(c); iota(theta)=iota(phi)*chi on T.'],
      'classical_inputs':[],
      'proof_location':{'file':'ordinary_control_v42/main.tex','label':'claim:'+cid,
        'line_start':start,'line_end':start+block.count('\n')-1,
        'sha256':sha(block.encode()),'bytes':len(block.encode())},
      'source_groups':groups,'sources':[sources[g] for g in groups],
      'dependency_scope':'Written mathematical proof; source declarations identify the original endpoint and do not replace the argument.'})

ost = (ROOT/'ordinary_structure_v42/main.tex').read_text()
peer_ids = sorted({x for deps,_ in relations.values() for x in deps if isinstance(x,str)},
                  key=lambda x:int(x[3:]))
peers = []
for cid in peer_ids:
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',ost,re.S)
    assert match, cid
    peers.append({'claim':cid,'file':'ordinary_structure_v42/main.tex',
                  'claim_sha256':sha(match.group().encode()),
                  'file_sha256':sha(ost.encode()),'kind':'peer',
                  'use':'Exact finite representatives, actual operators, periodicity, filtration and ordinary finite freeness; original hypotheses retained.'})

contract = {
 'source_endpoint':'UpperTheory.V.Hi.ctrlOrd',
 'endpoint_claim':'OCT17',
 'original_map':'ctrl(F)(g)_i = (xi(g_p)^(-1) F_i(g))_0',
 'coefficient_map':'the specified pointwise algebraMap O Omega',
 'coefficient_scope':'complete Noetherian local DOMAIN O with finite residue field, embedded in an algebraically closed field Omega',
 'domain_hypothesis_retained':True,
 'wt_rep_assertion_fields':['int_N','integral_torusCharacter','int_Nm','int_P','row_N','torusAction','nilpotent_central_action','cont_Nm','continuous_torusCharacter','central'],
 'source_conclusions':['ctrl is injective on the literal ClOrd sum of integral-unit maximal generalized eigenspaces','ctrl(ClOrd)=span_Omega(mapFn(Ord))'],
 'additional_proved_results':['S_c is a finite free integral classical ordinary lattice and ctrl induces the actual integral isomorphism S_c≃Ord (OCT15)','positive original operators intertwine, are units, and integral ordinary control is independent of admissible classical depth (OCT18)','finite sums of original away translations intertwine whenever they preserve the stated classical spaces (OCT19)'],
 'choice_order':'O, Omega, W, tau, theta, phi, U and admissible c are fixed first; one factorial projector e_c precedes all G and k; convergence at precision k is uniform in the finite lattice; deeper c-prime and period in OCT13 may depend on f; final lift is at the original c.',
 'not_supplied':['Construction of WtRep for the original algebraic weight','Actual arithmetic coefficient extension and finite-part character','Full one-map SpecIntIff.spec arithmetic specialization','Nonvanishing or arithmetic separation of Hecke blocks','Same-ideal Hida/automorphy endpoints','Full COUNT_II_SUPPORT'],
}
provenance = {
 'schema':'rh-human-component-provenance/1','artifact_version':'0.42','date':'2026-11-23',
 'component':'ordinary_control_v42','source_commit':PIN,
 'main_tex_sha256':sha(tex.encode()),'proof_file_sha256':sha(tex.encode()),
 'claims':claims,'source_groups':sources,'source_files':list(files.values()),
 'inherited_proof_inputs':[],'peer_proof_inputs':peers,'published_applications':[],
 'endpoint_contract':contract,
 'scope_note':'Full original generic classical ordinary control, with all elementary suppliers reconstructed; original algebraic WtRep construction and full arithmetic specialization remain separate.',
 'validation':{'source_files_equal_to_pinned_git_blobs':True,
   'source_file_count':len(files),'source_range_count':len(sources),'claim_count':len(claims),
   'mathematical_claim_count_is_not_a_completion_percentage':True,'no_lean_kernel_replay':True},
 'builder':{'file':'ordinary_control_v42/build_metadata.py','sha256':sha(Path(__file__).read_bytes())}}
(HERE/'provenance.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps({'source_commit':PIN,'source_files':list(files.values()),'ranges':sources},indent=2)+'\n')
(HERE/'contract.json').write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n')
(HERE/'closure.json').write_text(json.dumps({
 'schema':'rh-exact-endpoint-closure/1','artifact_version':'0.42','main_tex_sha256':sha(tex.encode()),
 'completed':[{'endpoint':'UpperTheory.V.Hi.ctrlOrd','proof_claim':'OCT17',
  'scope':contract['coefficient_scope']+'; all original WtRep, FinLevel, Free and depth hypotheses; same actual maps.'},
 {'endpoint':'Integral ordinary classical control and its inverse','proof_claim':'OCT15',
  'scope':'The actual finite classical value lattice, factorial ordinary projector, and original integral ordinary module.'},
 {'endpoint':'Positive-operator, depth and away-sum compatibility','proof_claim':'OCT18–OCT19',
  'scope':'Exact original operators and level inclusions; away-sum conclusion retains the stated classical-space preservation condition.'}],
 'whole_obligations_closed':[],'remaining':contract['not_supplied'],
 'choice_order':contract['choice_order']},indent=2,ensure_ascii=False)+'\n')
(HERE/'report.txt').write_text(
 'CLASSICAL ORDINARY CONTROL — v0.42\n\n'
 'Completed: the exact original CtrlOrd.ctrlOrd endpoint, including classical interpolation, integral value lattices, actual control equivariance, finite-matrix spectral decomposition, kernel contraction, approximation at the original depth, and full injectivity/image conclusion.\n\n'
 'Simplification: a finite free integral ordinary classical lattice S_c maps isomorphically onto the original ordinary module. Mod-maximal-ideal approximation and OST16 exact filtration reduce surjectivity to Nakayama; independence of O-valued functions over an embedded domain gives the source Omega-span conclusion.\n\n'
 'Additional proved compatibility: original positive operators are units on S_c, the actual inverse is independent of admissible classical depth, and finite sums of original away translations intertwine under their stated preservation hypothesis.\n\n'
 f'Claims: OCT1–OCT19 ({len(claims)} complete B proofs). Source bytes: {len(files)} files, {len(sources)} ranges at the exact pin. No new class-A theorem import; no Lean replay.\n\n'
 'Exact scope: the source CNL domain O, specified embedding into algebraically closed Omega, all ten WtRep assertion fields, original FinLevel/Free and depth/character conditions. The separate arbitrary-CNL ordinary base-change theorem is not substituted for this domain-valued control theorem.\n\n'
 'Boundary: the actual WtRep producer, arithmetic coefficient extension and character, full one-map specialization, arithmetic fibers and same-ideal Hida/automorphy remain separate. No whole COUNT_II_SUPPORT obligation is retired.\n')
print(json.dumps({'component':'ordinary_control_v42','claims':len(claims),
 'source_files':len(files),'source_ranges':len(sources),'proof_sha256':sha(tex.encode()),'status':'PASS'}))
