#!/usr/bin/env python3
"""Rebuild only the exact KIZ record-assembly component, without Lean replay."""
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
VERSION = '0.47'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
repo = ap.parse_args().repo.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
specs = {
    'cohinp': (AV+'UnitaryThreeGroups/KatoUse.lean',19,24,'The original complete five-field CohInp record'),
    'inpz': (AV+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean',55,61,'The six additional fields of the exact InpZ record'),
    'cohomology': (AV+'SymplecticGSp4/EntryMem.lean',161,167,'The existing CohomologyHyp fields, projected without altered data'),
    'local': (AV+'PadicHodgeTheory/LocalPublishedTheorems.lean',12,19,'All seven local published fields'),
    'k': (AV+'GeneratorCountTuples/LemmaK.lean',9,18,'HasMuQ, kBound and full universal LemmaK'),
    'm': (AV+'CommutativeAlgebra/OrbitVanishingLocal.lean',111,118,'Literal LemmaM including original M1-M5 and every-cover conclusion'),
    'mprime': (AV+'CommutativeAlgebra/OrbitVanishingLocal.lean',120,130,'Literal LemmaM-prime with additive injection and all derivation lifts'),
    'p': (AV+'CommutativeAlgebra/FramedTwoCoboundaries.lean',232,274,'IsUnivFramed, IsRelPres and full original LemmaP'),
    'rigii': (AV+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean',49,53,'Literal RigII including universal IsExt-to-IsModular antecedent'),
    'number': (AV+'AutomorphicForms/CongruenceNumberRankThree.lean',120,142,'Original eis3 and complete CNR3 quantifier order/product inequality'),
    'adk': (AV+'AutomorphicForms/CongruenceNumberRankThree.lean',155,176,'Original full matrix IsAdOf and universal AdVanishK'),
    'onechar_boundary': (AV+'UnitaryThreeGroups/KatoUse.lean',54,64,'Separate OneChar endpoint, not a stored InpZ field or new conclusion'),
}
rels = {
    'KIZ1': (['BX8','KB8'], ['cohinp','cohomology','local','k']),
    'KIZ2': (['KIZ1','SP1','SP6','FP8','KTR13','ADK6','RNC16'],
             ['inpz','m','mprime','p','rigii','adk','number','onechar_boundary']),
}
ext = {
    'KIZ1': ['KIZ_INHERITED_LOCAL_GLOBAL','KIZ_INHERITED_K_THEORY'],
    'KIZ2': ['KIZ_INHERITED_ALGEBRA','KIZ_INHERITED_AUTOMORPHIC'],
}

def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')

def build():
    files, sources, excerpts = {}, {}, []
    for key,(path,start,end,title) in specs.items():
        data=(repo/path).read_bytes()
        assert data==subprocess.check_output(['git','show',PIN+':'+path],cwd=repo),path
        lines=data.splitlines(keepends=True)
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        block=b''.join(lines[start-1:end])
        url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}'
        files[path]={'path':path,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
                     'verified_equal_to_pinned_git_blob':True,'url':url}
        sources[key]={'id':'KIZ_SRC_'+key.upper(),'path':path,'declaration':title,
            'line_start':start,'line_end':end,'source_commit':PIN,'file_sha256':sha(data),
            'full_file_sha256':sha(data),'range_sha256':sha(block),'range_bytes':len(block),
            'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
        excerpts.append(f'[{sources[key]["id"]}] {title}\n{sources[key]["url"]}\n'+block.decode())

    proof=(HERE/'main.tex').read_bytes();text=proof.decode();mainsha=sha(proof)
    wanted=set().union(*(set(ds) for ds,_ in rels.values()))-set(rels)
    baseline=ROOT/'history/version_0_46/provenance.json'
    ledger=json.loads(baseline.read_text())
    lookup={}
    for c in ledger['claims']:
        if c['id'] not in wanted: continue
        loc=c['proof_location'];p=ROOT/loc['file'];data=p.read_bytes()
        block=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
        assert sha(block)==loc['sha256'],c['id']
        lookup[c['id']]={'claim':c['id'],'file':loc['file'],'file_sha256':sha(data),
            'claim_sha256':sha(block),'line_start':loc['line_start'],'line_end':loc['line_end'],
            'kind':'immutable_inherited_human_proof','newly_modified_by_this_component':False}
    for p in [ROOT/'type_ii_rigidity_v47/main.tex',HERE/'main.tex']:
        data=p.read_bytes();txt=data.decode()
        for m in re.finditer(r'% BEGIN ([A-Z]+\d+)\n.*?% END \1\n',txt,re.S):
            cid=m.group(1)
            if cid not in wanted|set(rels): continue
            lookup[cid]={'claim':cid,'file':str(p.relative_to(ROOT)),'file_sha256':sha(data),
                'claim_sha256':sha(m.group().encode()),'line_start':txt[:m.start()].count('\n')+1,
                'line_end':txt[:m.end()].count('\n'),'kind':'same_release_reviewed_human_proof' if cid=='KTR13' else 'local_human_proof',
                'newly_modified_by_this_component':cid in rels}
    assert wanted|set(rels)<=set(lookup), (wanted|set(rels))-set(lookup)
    foundations=json.loads((HERE/'classical_inputs.json').read_text())['inputs']
    for f in foundations:
        f['newly_reconstructed_here']=False
        f['registry_bindings']=[{'file':p,'sha256':sha((ROOT/p).read_bytes())} for p in f['registry_files']]

    claims=[]
    for cid,(deps,ss) in rels.items():
        m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S);assert m
        start=text[:m.start()].count('\n')+1
        claims.append({'id':cid,'title':re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),
            'introduced_in':VERSION,'classification':'B','depends_on':deps,'external_input_ids':ext[cid],
            'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,
                'line_end':start+m.group().count('\n')-1,'sha256':sha(m.group().encode()),'bytes':len(m.group().encode())},
            'sources':[sources[s] for s in ss],'source_proof_is_not_human_proof':True})
    reviews=[]
    for p in sorted(HERE.glob('review_*.json')):
        r=json.loads(p.read_text());assert r.get('result',r.get('status'))=='PASS',p
        ids=[]
        for x in r.get('claims_reviewed',r.get('reviewed_claims',[])):
            cid=x if isinstance(x,str) else x.get('id',x.get('claim'));assert cid in rels
            h=r.get('proof_hashes',{}).get(cid) if isinstance(x,str) else x.get('proof_range_sha256',x.get('block_sha256'))
            assert h==lookup[cid]['claim_sha256'],(p,cid,'stale block');ids.append(cid)
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':r.get('reviewer'),
            'result':'PASS','reviewed_proof_file_sha256':r.get('proof_sha256',r.get('proof_file_sha256')),
            'proof_file_sha256':mainsha,'reviewed_blocks_unchanged':True,'claims':ids,'scope':r.get('scope')})
    reviewed={c for r in reviews for c in r['claims']}
    status='complete_at_stated_scope_independently_reviewed' if set(rels)<=reviewed else 'complete_at_stated_scope_pending_independent_review'
    for c in claims:
        c['status']='complete_at_stated_scope_independently_reviewed' if c['id'] in reviewed else 'complete_at_stated_scope_pending_independent_review'
        c['independent_review_files']=[r['file'] for r in reviews if c['id'] in r['claims']]
    register=ROOT/'dependency_audit_v0_46/remaining_leaf_register.json'
    task=next(x for x in json.loads(register.read_text())['records'] if x['id']=='TASK_INP_Z_ASSEMBLY')
    task_binding={'file':str(register.relative_to(ROOT)),'sha256':sha(register.read_bytes()),'record':task}
    contracts={'schema':'rh-human-component-contract/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,
        'proof_file_sha256':mainsha,'original_endpoint':'UpperTheory.V.Z.Kato.InpZ','endpoint_claim':'KIZ2',
        'additional_original_endpoints':['UpperTheory.V.U3.CohInp'],
        'subcontracts':[{'id':'complete_original_CohInp','claim':'KIZ1'},{'id':'complete_original_InpZ','claim':'KIZ2'}],
        'original_fields':{'toCohInp':['loc','pt','gf','ge','lemK'],'extension':['lemM','lemMprime','lemP','rigII','adK','number']},
        'field_suppliers':{'loc':'BX8','pt':'BX8','gf':'BX8','ge':'BX8','lemK':'KB8','lemM':'SP6','lemMprime':'SP1','lemP':'FP8','rigII':'KTR13','adK':'ADK6','number':'RNC16'},
        'constants':{'CK':31,'CK_chosen_before':'Every original prime, totally complex L, algebraic closure, Galois datum and e>=1','CNR3_c_A_chosen_before':'After fixed imaginary quadratic K and before e,N,p,w,finite indexed root orbit','CNR3_NN_chosen_before':'Every later coefficient prime, closure/scalar tower, fixed embedding, prolongation, Frobenius and finite admissible family'},
        'hypotheses':['All previously matched classical foundations of the numbered suppliers, explicitly bound in retained_foundations.json.','Each stored theorem retains every literal source antecedent: these are universally quantified implication theorems, not assertions that an unspecified later arithmetic datum satisfies the antecedents.'],
        'preserved_guards':['All original local/global cohomology primes including2 where allowed','HasMuQ uses fourth root at2','LemmaP original ell!=2, including3','RigII exact full GD, IsPt, TypeII and universal IsExt=>IsModular hypothesis','AdVanishK full infinite-cyclotomic kernel and full M_n action at all original n>=2 and primes','CNR3 e,N>=1,p>=7,p away from N*discK,l!=2,p,all original root-orbit and coefficient closures'],
        'same_object_requirements':'Reuse BX8 normalized invariant and tied period data. Specialize all universal fields to the same original Omega,K,l,c,e,N,psi,U,g1,r,iota; no new arithmetic witness or scalar map replaces those data.',
        'not_claimed':['OneChar','AutUnramCoef','Existence of later arithmetic Model or its application hypotheses','Rank-four substitution','Completion of RH or GRH'],
        'baseline_selected_task':task_binding,'new_classical_inputs':[],'original_admissibility_not_weakened':True}
    prov={'schema':'rh-human-component-provenance/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,
        'proof_file_sha256':mainsha,'status':status,'claims':claims,'inherited_human_inputs':[lookup[c] for c in sorted(wanted)],
        'inherited_classical_and_foundational_inputs':foundations,'new_classical_inputs':[],'independent_reviews':reviews,
        'dependency_convention':'depends_on contains numbered human claims only. Named classical foundations and their immutable registries are separate. DX1 is already an ancestor of BX8; its mention in KIZ1 explains that inherited scope.',
        'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_artifacts_modified':False}
    closure={'schema':'rh-human-component-closure/1','component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,
        'proof_file_sha256':mainsha,'status':status,'closed_subcontracts':contracts['subcontracts'],
        'proposed_global_frontier_leaf_closures':[{'id':'TASK_INP_Z_ASSEMBLY','category':'B','claim':'KIZ2','contract':task['contract'],'scope':'Complete literal original CohInp/InpZ record at the already-matched classical foundations; no stored predicate or shared-object requirement remains. Root alone records selected-frontier closure.'}],
        'new_global_frontier_leaf_closures':[],'independent_reviews':reviews,'pending':sorted(set(rels)-reviewed),
        'OneChar_and_AutUnramCoef_remain_separate':True,'foundation_retention_explicit':True,
        'validation':'Two-pass standalone draft TeX; exact source/proof/registry hashes and independent mathematical review; no Lean replay.'}
    manifest={'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())}
    for name,obj in [('provenance.json',prov),('contracts.json',contracts),('original_contracts.json',contracts),('closure.json',closure),('source_manifest.json',manifest),('retained_foundations.json',foundations)]:dump(name,obj)
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    (HERE/'report.txt').write_text(f'''Kato input assembly v{VERSION}\n\nKIZ1 proves exact CohInp by retaining BX8's original normalized local/global cohomology fields and choosing the universal LemmaK constant31 from KB8. KIZ2 constructs every field of original InpZ with SP6,SP1,FP8,KTR13,ADK6,RNC16, explaining every source guard and the same-object specialization. All six stored assertions are full original implication theorems, not newly assumed producer slots. This is the complete baseline B task TASK_INP_Z_ASSEMBLY. OneChar, AutUnramCoef and later arithmetic application hypotheses remain separate. There is no rank-four substitution and no new published foundation.\n\nPin: {PIN}\nMain SHA256: {mainsha}\nStatus: {status}\nClaims: 2 B; source files: {len(files)}; ranges: {len(sources)}; inherited numbered bindings: {len(wanted)}\n\nRebuild: python build_metadata.py --repo /path/to/formal_source\nValidate: python validate_tex.py --format /path/to/pdflatex.fmt\nNo old proof bytes or common metadata are edited.\n''')
    dump('hashes.json',{'component':COMPONENT,'artifact_version':VERSION,'hashes':{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}})
    print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),'inherited_bindings':len(wanted),'main_sha256':mainsha,'status':status},indent=2))

build()
