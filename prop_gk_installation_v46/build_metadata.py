#!/usr/bin/env python3
"""Rebuild only this finite PropGK implication component; never replay Lean."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMPONENT = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.46'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
REPO = ap.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
HV = AV + 'HeightAndVanishing/'
U3 = AV + 'UnitaryThreeGroups/'
AF = AV + 'AutomorphicForms/'
specs = {
    'target': (U3+'KatoUse.lean', 36, 42, 'Literal PropGK: fixed K constants and integer before every coefficient datum'),
    'onechar': (U3+'KatoUse.lean', 54, 64, 'Exact retained OneChar implication and actual Selmer/trace estimate'),
    'producer': (U3+'OrbEquiv.lean', 111, 173, 'Original CNR3 -> OneChar -> PropGK finite consumer'),
    'frob': (U3+'OrbEquiv.lean', 22, 47, 'Arithmetic Frobenius action on roots of unity and cyclotomic character'),
    'vl': (U3+'OrbEquiv.lean', 49, 63, 'Product norm to sum of normalized valuations'),
    'orbcard': (U3+'OrbEquiv.lean', 65, 80, 'Kernel preservation and exact orbit cardinal bound'),
    'teq': (U3+'OrbEquiv.lean', 82, 109, 'Original scalar and coefficient-orbit equivalence'),
    'gd': (HV+'Counts.lean', 9, 23, 'All original GD fields'),
    'gdfacts': (HV+'GdFacts.lean', 22, None, 'Same-kernel GD propagation; complete fields and finite-component signs'),
    'orbfacts': (HV+'OrbFacts.lean', 9, None, 'Cyclic quotient, coprime-power orbit and totient cardinality'),
    'parts': (HV+'DirichletPrimeToLPartMulLPowerPart.lean', 10, 102, 'Original coefficient DVR and finite-character component definitions'),
    'lengths': (HV+'DirichletPrimeToLPartMulLPowerPart.lean', 112, 145, 'Actual Vlen, Vn and orb'),
    'partord': (HV+'PartOrd.lean', 43, None, 'Finite-order primary decomposition; prime-to-ell characters unchanged'),
    'compalg': (HV+'CompAlg.lean', 39, None, 'Original CRT component commutes with powers and has order dividing the original character'),
    'selmer': (AV+'CharacterLevelBounds/ShaFamMono.lean', 15, 72, 'Original Psi, inverse twist, ShaU length and ramification normalization'),
    'valdef': (U3+'Rigid0.lean', 8, 12, 'vl is minus the base-ell logarithm of the norm'),
    'cls': (AV+'CharacterLevelBounds/ClsFacts.lean', 1, None, 'Original cls character of the action on roots of unity'),
    'place': (AV+'PrimitiveFrobeniusFixed/PlaceBasic.lean', 165, 178, 'Original prolongation/Frobenius/root-of-unity foundational scope'),
    'iso': ('src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsPadicAlgClRingEquivComplexCompEqOfCountabl.lean', 31, 35, 'Field isomorphism between the algebraic p-adic closure and C'),
    'cnr': (AF+'CongruenceNumberRankThree.lean', 107, 140, 'Exact admissibility, Eisenstein scalar and original CNR3 quantifiers'),
    'rigii': (AV+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean', 43, 53, 'Separate original KatoTwo/RigII boundary; not supplied or used as a new theorem'),
    'onecharproducer': (AV+'ModularityArgument/KatoQuadraticCharacters/OneChar.lean', 158, 178, 'Separate original OneChar producer from InpZ and automorphy; retained as a boundary'),
}
relations = {
    1: ([], ['parts','lengths','orbfacts','orbcard','teq']),
    2: ([1], ['gd','gdfacts','parts','partord','compalg']),
    3: ([], ['frob','teq','place','iso','cls','selmer']),
    4: ([1,'RNC16'], ['target','producer','cnr','orbcard']),
    5: ([1,2,3,4,'RNC16'], ['onechar','producer','cnr','lengths']),
    6: ([4,5,'RNC16'], ['target','producer','vl','valdef','lengths']),
}


def build():
    files, sources, excerpts = {}, {}, []
    for key, (rel, a, z, title) in specs.items():
        data = (REPO/rel).read_bytes()
        assert data == subprocess.check_output(['git','show',PIN+':'+rel], cwd=REPO), rel
        lines = data.splitlines(keepends=True)
        z = z or len(lines)
        assert 1 <= a <= z <= len(lines), (rel,a,z,len(lines))
        block = b''.join(lines[a-1:z])
        url = f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
        files[rel] = {'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
                      'verified_equal_to_pinned_git_blob':True,'url':url}
        sources[key] = {'id':'PGK_SRC_'+key.upper(),'path':rel,'declaration':title,
                        'line_start':a,'line_end':z,'source_commit':PIN,
                        'file_sha256':sha(data),'full_file_sha256':sha(data),
                        'range_sha256':sha(block),'range_bytes':len(block),
                        'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{a}-L{z}'}
        excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())
    text = (HERE/'main.tex').read_text()
    main_sha = sha(text.encode())
    lookup = {}
    for path in [HERE/'main.tex', ROOT/'rank_three_congruence_v46'/'main.tex']:
        s = path.read_text()
        for m in re.finditer(r'% BEGIN ([A-Z]+\d+)\n.*?% END \1\n', s, re.S):
            lookup[m.group(1)] = {'claim':m.group(1),'file':str(path.relative_to(ROOT)),
                                 'file_sha256':sha(path.read_bytes()),'claim_sha256':sha(m.group().encode()),
                                 'line_start':s[:m.start()].count('\n')+1,
                                 'line_end':s[:m.end()].count('\n')}
    local = {'PGK'+str(i) for i in relations}
    claims = []
    for i, (deps, keys) in relations.items():
        cid = 'PGK'+str(i)
        block = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', text, re.S)
        assert block, cid
        deps = ['PGK'+str(x) if isinstance(x,int) else x for x in deps]
        assert set(deps) <= set(lookup), (cid,deps)
        location = lookup[cid]
        claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block.group(),re.S).group(1),
                       'introduced_in':VERSION,'classification':'B','depends_on':deps,
                       'conditional_input_ids':['PGK_ONE_CHAR'] if i in (5,6) else [],
                       'foundation_input_ids':['PGK_LOCAL_FIELDS'] if i==3 else [],
                       'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,
                                         'line_start':location['line_start'],'line_end':location['line_end'],
                                         'sha256':location['claim_sha256'],'bytes':len(block.group().encode())},
                       'sources':[sources[k] for k in keys],'source_proof_is_not_human_proof':True})
    onechar = {'id':'PGK_ONE_CHAR','kind':'explicit_original_conditional_premise',
               'name':'UpperTheory.V.U3.OneChar','newly_proved':False,
               'statement':'For every original GD coefficient datum, fixed iota, sigma and exact scalar Psi(sigma)+1+Psi(sigma)^-1, universal admissible trace separation implies finite original Vlen and a finite pairwise-nonisomorphic admissible set with Vn <= 2 sum vl(trace-scalar).',
               'sources':[sources['onechar']],
               'separate_producer_sources':[sources['onecharproducer'],sources['rigii']],
               'selected_frontier_boundaries':['ONE_CHAR','TASK_ONE_CHAR_PROOF','RIG_II'],
               'scope_note':'A logical antecedent of the completed finite implication. It is not converted into a proved foundational theorem or a numbered DAG node.'}
    foundation = {'id':'PGK_LOCAL_FIELDS','kind':'inherited_local_field_foundation',
                  'newly_proved':False,'statement':'Valuation prolongation to an algebraic closure and the exact decomposition-group/inertia quotient for a finite residue field; prime-to-residue-characteristic roots of unity in the maximal unramified extension.',
                  'sources':[sources['place'],sources['frob']],
                  'application_proof':'PGK3 proves the actual rational cyclotomic values and inverse-Frobenius scalar. Its field-isomorphism existence is explained by transcendence bases, without a continuity requirement.'}
    reviews = []
    paths = list(HERE.glob('review_*.json'))
    extra = ROOT/'reviews_v0_46'/f'{COMPONENT}_root_review.json'
    if extra.exists(): paths.append(extra)
    reviewed = set()
    for path in paths:
        r = json.loads(path.read_text())
        assert r.get('result',r.get('status'))=='PASS', path
        ids = []
        for item in r.get('claims_reviewed',r.get('reviewed_claims',[])):
            cid = item if isinstance(item,str) else item.get('id',item.get('claim'))
            expected = r.get('proof_hashes',{}).get(cid) if isinstance(item,str) else item.get('block_sha256',item.get('proof_range_sha256'))
            assert cid in local and expected==lookup[cid]['claim_sha256'], (path,cid)
            ids.append(cid)
        reviewed.update(ids)
        reviews.append({'file':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),
                        'reviewer':r.get('reviewer'),'result':'PASS','proof_file_sha256':main_sha,
                        'claims':ids,'reviewed_blocks_unchanged':True,'scope':r.get('scope')})
    status = 'complete_implication_independently_reviewed' if local<=reviewed else 'complete_implication_pending_independent_review'
    for c in claims:
        c['status'] = 'complete_implication_independently_reviewed' if c['id'] in reviewed else 'complete_implication_pending_independent_review'
        c['independent_review_files'] = [r['file'] for r in reviews if c['id'] in r['claims']]
    baseline = json.loads((ROOT/'dependency_audit_v0_45'/'remaining_leaf_register.json').read_text())
    def rows(x):
        if isinstance(x,dict):
            if x.get('id')=='TASK_PROP_GK_INSTALL': yield x
            for v in x.values(): yield from rows(v)
        elif isinstance(x,list):
            for v in x: yield from rows(v)
    task = next(rows(baseline))
    baseline_binding = {'version':'0.45','file':'dependency_audit_v0_45/remaining_leaf_register.json',
                        'id':task['id'],'kind':task['kind'],'category':task['category'],
                        'contract':task['contract'],'contract_text_sha256':sha(task['contract'].encode()),
                        'row_canonical_sha256':sha(json.dumps(task,sort_keys=True,separators=(',',':')).encode()),
                        'implication_source':[sources['producer']]}
    contracts = {'schema':'rh-human-component-contract/1','artifact_version':VERSION,'component':COMPONENT,
                 'source_commit':PIN,'proof_file_sha256':main_sha,'endpoint_claim':'PGK6',
                 'original_endpoint':'UpperTheory.V.U3.propGK : CNR3 -> OneChar -> PropGK',
                 'original_output_contract':sources['target'],'original_conditional_input':onechar,
                 'supplied_congruence_input':'RNC16',
                 'quantifier_order':['arbitrary number field K','natural constants c5,A','e>=1,N>=1,H subgroup of units modN,p prime avoiding30*N*abs(discK)','NN nonzero integer','every original Omega,ell!=p,Coef ell','existence of one GD character in coefficient orbit','all original Vlen finite and sum Vn<=2 padicValInt ell NN'],
                 'normalizations':{'orbit':'all characters with exact kernel H, including multiplicity of values at q','bound':'c5*phi(index H)*(N*(e+1))^A*log p','root':'z_chi=chi(q)^-1','Frobenius':'sigma arithmetic, scalar and traces at sigma^-1','scalar':'q^-e*psi(q)^-1+1+q^e*psi(q)','valuation':'vl=-log norm/log ell; integer normalized by v_ell(ell)=1','length':'original ShaU(twist2(Psi^-1),ell*N,top), divided by original eO after proving finiteness'},
                 'edge_cases':['nonimaginary-quadratic K: c5=A=0,NN=1,GD antecedent impossible','empty complex orbit allowed','ell=2 or3 not excluded by a new hypothesis; original GD antecedent is impossible there','no nonisomorphism condition across different character indices','no coefficient ring enlargement','e=0 not added to the original e>=1 scope'],
                 'original_contract_not_weakened':True,'selected_task_binding':baseline_binding,
                 'not_claimed':['OneChar producer','RigII producer','unconditional PropGK independent of OneChar','complete RH or GRH']}
    inherited = [{**lookup['RNC16'],'kind':'same_release_independently_reviewed_human_input','newly_modified_by_this_component':False}]
    provenance = {'schema':'rh-human-component-provenance/1','artifact_version':VERSION,'component':COMPONENT,
                  'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,'claims':claims,
                  'inherited_human_inputs':inherited,'conditional_inputs':[onechar],
                  'classical_and_foundational_inputs':[foundation],'independent_reviews':reviews,
                  'dependency_convention':'Only numbered human claims occur in depends_on. Original OneChar is an explicit logical premise of the finite implication, recorded separately. No open producer is silently supplied.',
                  'root_ledger_modified':False,'frozen_artifacts_modified':False,'source_proof_is_not_human_proof':True}
    closure = {'schema':'rh-human-component-closure/1','artifact_version':VERSION,'component':COMPONENT,
               'source_commit':PIN,'proof_file_sha256':main_sha,'status':status,
               'closed_subcontracts':[{'id':'complete_kernel_orbit_and_same_coefficient_realization','claim':'PGK1'},
                                      {'id':'all_original_GD_fields_under_same_kernel','claim':'PGK2'},
                                      {'id':'literal_inverse_Frobenius_scalar','claim':'PGK3'},
                                      {'id':'integer_before_coefficient_prime','claim':'PGK4'},
                                      {'id':'exact_OneChar_finite_installation','claim':'PGK5'},
                                      {'id':'whole_original_PropGK_implication','claim':'PGK6'}],
               'proposed_global_frontier_leaf_closures':[{'id':'TASK_PROP_GK_INSTALL','claim':'PGK6','classification':'B',
                   'scope':'Exactly the original CNR3 -> OneChar -> PropGK finite implication, as specified by the baseline implication task. RNC16 supplies CNR3; OneChar remains the separate original antecedent.',
                   'baseline_contract':baseline_binding}],
               'new_global_frontier_leaf_closures':[],
               'retained_open_producers':['ONE_CHAR','TASK_ONE_CHAR_PROOF','RIG_II'],
               'OneChar_is_not_newly_assumed_as_a_closed_foundation':True,
               'independent_reviews':reviews,'pending':sorted(local-reviewed),
               'validation':'Two-pass standalone draft TeX; source/proof hashes and independent mathematical review. No Lean replay.'}
    manifest = {'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,
                'files':list(files.values()),'ranges':list(sources.values())}
    objects = {'contracts.json':contracts,'original_contracts.json':contracts,'provenance.json':provenance,
               'closure.json':closure,'source_manifest.json':manifest,'conditional_inputs.json':[onechar],
               'retained_foundations.json':[foundation],'classical_inputs.json':{'inputs':[foundation]}}
    for name,obj in objects.items(): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    (HERE/'report.txt').write_text(
        f'{COMPONENT} v{VERSION}\n\n'
        'Six complete human proofs reconstruct the original finite implication CNR3 -> OneChar -> PropGK. '
        'The same-kernel orbit is realized over the original coefficient DVR; all GD fields are checked; '
        'the arithmetic-Frobenius action and the inverse-Frobenius Eisenstein scalar agree exactly. '
        'RNC16 chooses one nonzero integer before every later coefficient prime. The original OneChar '
        'premise then provides finite, pairwise-nonisomorphic families, and the norm-product inequality '
        'gives the normalized valuation sum with factor2. The nonquadratic case is handled explicitly.\n\n'
        'This closes only the finite implication task TASK_PROP_GK_INSTALL if root integration accepts '
        'its exact baseline B contract. ONE_CHAR, TASK_ONE_CHAR_PROOF and RIG_II remain separate open '
        'producers; no unconditional PropGK, CountI or RH/GRH completion is claimed. No new auxiliary '
        'coefficient enlargement, prime bound or level is introduced.\n\n'
        f'Pin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\n'
        f'Claims: {len(claims)} B; source files: {len(files)}; ranges: {len(sources)}\n'
        'Rebuild: python build_metadata.py --repo /path/to/formal_source\n'
        'Validate: python validate_tex.py --format /path/to/project/pdflatex.fmt\n')
    hashes = {p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
    (HERE/'hashes.json').write_text(json.dumps({'component':COMPONENT,'artifact_version':VERSION,'hashes':hashes},indent=2)+'\n')
    print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),
                      'source_ranges':len(sources),'inherited_bindings':len(inherited),
                      'main_sha256':main_sha,'status':status},indent=2))


build()
