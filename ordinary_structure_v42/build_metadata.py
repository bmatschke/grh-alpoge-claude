#!/usr/bin/env python3
"""Bind the ordinary proof to exact pinned source bytes and retained inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
args = ap.parse_args()
repo = args.repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
H = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/'
O = H + 'OrdinaryHeckeCharacters/'
R = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/BuildingsResidueChars/'

# The complete source file is retained as the range when several elementary
# suppliers within it are reconstructed together. The endpoint files have
# the exact declaration ranges consumed by the original downstream proof.
specs = {
 'definitions': (H+'ContinuousTorusCharacter.lean',29,237,'Iwa; Frame; FinLevel; Free; Sp; valIn; Ord; mapFn'),
 'iwahori_factor': (O+'IwMemMul.lean',1,None,'iwMem'),
 'iwahori_finite': (O+'IwahoriProUnipotentFiniteIndex.lean',1,None,'iwFin'),
 'finite_reps': (R+'ExistsFiniteIwahoriDoubleCosetRepresentatives.lean',1,None,'exists_finite_iwahori_doubleCoset_representatives'),
 'torus': (R+'ExistsIwahoriTorusProjection.lean',1,None,'exists_iwahori_torus_projection'),
 'sections': (R+'ExistsSectionAutomorphicSpaceWithPrescribedValue.lean',1,None,'exists_section_automorphicSpace_with_prescribed_values'),
 'sections_free': (R+'ExistsLinearSectionAutomorphicFunctionsOfFree.lean',1,None,'exists_linear_section_automorphicFunctions_of_free'),
 'sample_detection': (R+'MemValInOfInvariantAndValuesMemPow.lean',1,None,'mem_valIn_of_invariant_and_values_mem_pow'),
 'operator_sum': (O+'UOpSum.lean',1,None,'uOpSum'),
 'operator_mul': (O+'UOpMul.lean',1,None,'uOpMul'),
 'operator_level': (O+'UOpLevel.lean',1,None,'uOpLevel'),
 'operator_natural': (O+'UOpNat.lean',1,None,'uOpNat'),
 'space_stability': (O+'SpStab.lean',1,None,'spStab'),
 'lowering': (R+'UOperatorPowEventuallyInvariantModPow.lean',1,None,'uOperator_pow_eventually_invariant_mod_pow'),
 'space_complete': (R+'ExistsAdicLimitMemAutomorphicSpace.lean',1,None,'exists_adic_limit_mem_automorphicSpace'),
 'projector': (R+'ExistsOrdinaryProjectorOfEventuallyPeriodic.lean',1,None,'exists_ordinaryProjector_of_eventually_periodic'),
 'successive': (R+'ExistsLinearPreimageOfSuccessiveApproximation.lean',1,None,'exists_linear_preimage_of_successive_approximation'),
 'ordinary_abstract': (O+'OrdFree.lean',66,245,'exists_eventually_periodic_mod_V; ordAbs'),
 'ordinary_periodic': (O+'OrdFree.lean',268,291,'mem_ord_iff'),
 'ordinary_structure': (O+'OrdFree.lean',295,437,'ordStruct'),
 'ordinary_units': (O+'OrdFree.lean',441,481,'ordFree'),
 'basechange_abstract': (O+'OrdBCMapOrd.lean',5,42,'ordBC_abs'),
 'basechange_suppliers': (O+'OrdBCMapOrd.lean',46,194,'ordBC_mapval; ordBC_mapU; ordBC_mapSp; ordBC_mapOrd; ordBC_free; ordBC_key'),
 'basechange_endpoint': (O+'OrdBCMapOrd.lean',198,232,'ordBC'),
 'matrix_data': (H+'TcAnti.lean',13,111,'IwaData.Ax; piData; Kc; Uo; Uc; unif; glData'),
 'matrix_axioms': (O+'IndexNeZero.lean',1,None,'GlAx elementary suppliers; glAx'),
 'product_axioms': (O+'DivMono.lean',1,None,'piAx'),
 'matrix_iwahori': (H+'Distinct.lean',19,24,'glIwa; piIwa'),
 'actual_product': (H+'CoefficientRepTrivialOnUnramified.lean',20,28,'GV; iwS'),
 'actual_frame': (H+'IsTheta.lean',123,144,'hset'),
}
file_records = {}
sources = {}
for sid,(rel,start,end,decl) in specs.items():
    path=repo/rel
    data=path.read_bytes()
    pinned=subprocess.run(['git','show',PIN+':'+rel],cwd=repo,check=True,stdout=subprocess.PIPE).stdout
    assert data==pinned,rel
    lines=data.splitlines(keepends=True)
    end=end or len(lines)
    assert 1<=start<=end<=len(lines),(sid,start,end,len(lines))
    block=b''.join(lines[start-1:end])
    filerec={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
             'verified_equal_to_pinned_git_blob':True,
             'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'}
    file_records[rel]=filerec
    sources[sid]={'id':'OST_SRC_'+sid.upper(),'path':rel,'declaration':decl,
        'line_start':start,'line_end':end,'sha256':sha(data),'full_file_sha256':sha(data),
        'range_sha256':sha(block),'range_bytes':len(block),'source_commit':PIN,
        'verified_equal_to_pinned_git_blob':True,'url':filerec['url']+f'#L{start}-L{end}'}

relations = {
1:([],['definitions','iwahori_factor','iwahori_finite','finite_reps']),
2:([1],['torus']),
3:([1,2],['sections','sections_free']),
4:([1],['sample_detection']),
5:([],['operator_sum','operator_mul','operator_natural']),
6:([1,5],['operator_level']),
7:([5,6],['space_stability','lowering']),
8:([],['space_complete','ordinary_structure']),
9:([1,3,4,7],['ordinary_structure']),
10:([5,7],['ordinary_periodic','space_stability']),
11:([8,9],['ordinary_abstract']),
12:([8,10,11],['projector','ordinary_abstract']),
13:([9,12],['ordinary_abstract']),
14:([8,13],['ordinary_abstract']),
15:([8,14],['successive','ordinary_abstract']),
16:([15],['ordinary_abstract']),
17:([13,16],['ordinary_abstract']),
18:([10,16,17],['ordinary_abstract']),
19:([9,10,12,16,17,18],['ordinary_structure']),
20:([5,10,17,18],['ordinary_units']),
21:([5,10],['basechange_suppliers']),
22:([3,4,7,12,13,16,21],['basechange_suppliers','basechange_endpoint']),
23:([17,22],['basechange_abstract']),
24:([19,21,22,23],['basechange_endpoint']),
25:([5,7,12,21,24],['basechange_suppliers','projector']),
26:([],['matrix_data','matrix_axioms','matrix_iwahori']),
27:([26],['matrix_data','product_axioms','matrix_iwahori','actual_product','actual_frame']),
28:([19,20,24,27,'OTW1','OTW12','NTL17','FNL10'],['ordinary_structure','ordinary_units','basechange_endpoint','actual_frame']),
}
text=(HERE/'main.tex').read_text()
claims=[]
for num,(deps,groups) in relations.items():
    cid='OST'+str(num)
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S)
    assert match,cid
    start=text[:match.start()].count('\n')+1
    block=match.group()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    ds=['OST'+str(d) if isinstance(d,int) else d for d in deps]
    claims.append({'id':cid,'title':title,'introduced_in':'0.42','classification':'B',
       'status':'complete human proof at the printed exact scope','depends_on':ds,
       'scope':'shared RH and unrestricted Dirichlet GRH',
       'original_hypotheses':(['Original arithmetic datum; OTW12 single complete-ring character before every K; FNL10 exact finite levels; original GL/product Iwahori datum.'] if num==28 else
         ['Exactly the hypotheses printed in this claim and the standing original Iwahori/Frame/CNL conditions; no reducedness or flatness added.']),
       'classical_inputs':[],
       'proof_location':{'file':'ordinary_structure_v42/main.tex','label':'claim:'+cid,
                         'line_start':start,'line_end':start+block.count('\n')-1,
                         'sha256':sha(block.encode()),'bytes':len(block.encode())},
       'source_groups':groups,'sources':[sources[g] for g in groups],
       'dependency_scope':'Written mathematical proof; source locations identify the endpoint and do not replace proof.'})

input_paths={'OTW1':'ordinary_theta_weight/main.tex','OTW12':'ordinary_theta_weight/main.tex',
             'NTL17':'neat_levels/main.tex','FNL10':'finite_levels_v42/main.tex'}
inputs=[]
for cid,rel in input_paths.items():
    s=(ROOT/rel).read_text()
    m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',s,re.S);assert m,cid
    inputs.append({'claim':cid,'file':rel,'claim_sha256':sha(m.group().encode()),
                   'kind':'peer' if cid.startswith('FNL') else 'inherited',
                   'use':'Original actual-level installation OST28; generic OST19/20/24 do not assume these arithmetic suppliers.'})

record={'schema':'rh-human-component-provenance/1','artifact_version':'0.42','date':'2026-11-23',
 'source_commit':PIN,'component':'ordinary_structure_v42','main_tex_sha256':sha(text.encode()),
 'proof_file_sha256':sha(text.encode()),'claims':claims,'source_groups':sources,
 'source_files':list(file_records.values()),'inherited_proof_inputs':[x for x in inputs if x['kind']=='inherited'],
 'peer_proof_inputs':[x for x in inputs if x['kind']=='peer'],'published_applications':[],
 'scope_note':'Full generic original ordStruct/ordFree/ordBC plus complete local glAx/piAx and actual arithmetic installation. Same-ideal arithmetic/Hida/control endpoints remain separate.',
 'validation':{'source_files_equal_to_pinned_git_blobs':True,'source_file_count':len(file_records),
               'source_range_count':len(sources),'claim_count':len(claims),
               'mathematical_claim_count_is_not_a_completion_percentage':True,
               'no_lean_kernel_replay':True},
 'builder':{'file':'ordinary_structure_v42/build_metadata.py','sha256':sha(Path(__file__).read_bytes())}}
(HERE/'provenance.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps({'source_commit':PIN,'source_files':list(file_records.values()),'ranges':sources},indent=2)+'\n')
closure={'schema':'rh-exact-endpoint-closure/1','artifact_version':'0.42',
 'main_tex_sha256':sha(text.encode()),'completed':[
  {'endpoint':'UpperTheory.V.Hi.ordStruct','proof_claim':'OST19','scope':'Every original generic Frame with ContChar/FinLevel/Free over any IsCNL ring; one complete-ring factorial projector, finite freeness, invertibility and exact filtration.'},
  {'endpoint':'UpperTheory.V.Hi.ordFree','proof_claim':'OST20','scope':'Same original data; bijective U_a for every positive-monoid a.'},
  {'endpoint':'UpperTheory.V.Hi.ordBC','proof_claim':'OST24','scope':'Every local map A->B of IsCNL rings; exact original coefficientwise map, including nonflat maps and nonreduced rings.'},
  {'endpoint':'UpperTheory.V.Hi.glAx','proof_claim':'OST26','scope':'Every original local matrix datum and all 22 axiom fields; same uniformizer and congruence depth.'},
  {'endpoint':'UpperTheory.V.Hi.piAx','proof_claim':'OST27','scope':'Actual finite products, including common exponent choices and empty products.'},
  {'endpoint':'Actual arithmetic ordinary structure and base change at every K','proof_claim':'OST28','scope':'Original H.X, H.tau_A and one OTW12 theta before all K; no new threshold; ell=3 retained.'}],
 'whole_obligations_closed':[],
 'remaining':['Classical control and actual WtRep producer','Integral TypeForAlt','Original Hecke algebra and separating automorphic arithmetic fibers','Four Hida endpoints and all-level HasAut on the same ideal','Full COUNT_II_SUPPORT'],
 'choice_order':'Original theta fixed before every K; for each K one projector before all functions/precisions; thresholds for factorial convergence may depend on f,k; arbitrary coefficient map does not alter the map being base changed.'}
(HERE/'closure.json').write_text(json.dumps(closure,indent=2)+'\n')
(HERE/'report.txt').write_text('ORDINARY STRUCTURE AND BASE CHANGE — v0.42\n\n'
 'Completed: full original ordStruct, ordFree and ordBC, including their finite-coordinate, level-lowering, complete-projector and integral-freeness suppliers.\n'
 'OST26–28 also prove every glAx/piAx field and install the results on the actual hset Frame at every original auxiliary level using FNL10, NTL17 and OTW12.\n\n'
 'Mathematical mechanism: exact integral sample sections and U_z level lowering give eventual periodicity at every adic precision. One factorial limit gives the projector. A fixed finite correction map, successive approximation and a split evaluation map give finite projectivity/freeness and the reverse filtration inclusion. Simultaneous sample evaluation over A and B produces an explicit base-change left inverse, so no flatness or reducedness is required.\n\n'
 'Claims: OST1–OST28 (28 complete B proofs). Source bytes: '+str(len(file_records))+' files, '+str(len(sources))+' ranges at the exact pin. No new class-A theorem import. No Lean replay.\n\n'
 'Endpoint scope: all original generic CNL rings and every local coefficient map; all actual K with one previously chosen theta. The ordinary projector is chosen before f and k; its convergence threshold is allowed to depend on them. Same actual maps and congruence depth c+1 are preserved. Rank four and ell=3 remain in scope.\n\n'
 'Boundary: no whole COUNT_II_SUPPORT leaf is retired. Classical control, integral type, automorphic fibers, Hecke arithmetic, Hida endpoints and all-level same-ideal automorphy remain separate.\n')
print(json.dumps({'component':'ordinary_structure_v42','claims':len(claims),'source_files':len(file_records),'source_ranges':len(sources),'proof_sha256':sha(text.encode()),'status':'PASS'}))
