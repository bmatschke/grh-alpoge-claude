#!/usr/bin/env python3
"""Bind LFC human proofs to pinned source and unchanged inherited proofs."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
V='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
G=V+'GaloisCochains/'
F=V+'FrobeniusSmoothVectors/'
K=V+'GaloisLibrary/KummerTheory/'
SPECS={
 'link_defs':(G+'GLinkQuot.lean','Exact GLink/FLink, Hypotheses2, tameN and clRk'),
 'frame_defs':(F+'ContinuousCoboundaries2.lean','Actual Frame, all 28 Ok fields and EC'),
 'gen_defs':(F+'FrobeniusSplitPrimeDatum.lean','Full Gen, UFacts, Linked and HasFrameW'),
 'has_frame':(V+'CurveDVRSpecialization/HostFrameEx.lean','GalLink, HasFrame, SeedClause and separate named-data endpoints'),
 'hc_defs':(V+'LevelCohomology/HcDefs.lean','Original retained HcPublished premises'),
 'phi_def':(V+'CommutativeAlgebra/ResMapBijective.lean','Literal PhiCond over every open subgroup'),
 'fin_char':(K+'FinChar.lean','Finite Kummer characters with fixed ramification'),
 'rad_exists':(K+'RadExists.lean','Kummer eigenvector construction'),
 'card_sel':(K+'CardSel.lean','Ideal-class exact-sequence calculation'),
 'card_sunit':(K+'CardSUnit.lean','S-unit finiteness input'),
 'dvd_ine':(K+'DvdOfIne.lean','Unramified radical implies divisible valuations'),
 'phi':(G+'PhiGam.lean','Full phiGam'),
 'phi_wrapper':(G+'Imports.lean','Exact GC.phi'),
 'cl':(G+'EqOneOfPow.lean','Full GC.cl, uniform exponent before all finite groups'),
 'dec_zhat':(G+'DecZhat.lean','Residue Frobenius and procyclic decomposition quotient'),
 'gen_dec':(G+'GenDec.lean','Full local finite-abelian-group detector theorem'),
 'gen':(G+'ToZModEqOne.lean','Full GC.gen and cyclotomic reduction convention'),
 'xdual':(K+'Mk0IdMapCongr.lean','Literal XDual and its inertia and decomposition clauses'),
 'cl_pull':(K+'PullOnto.lean','Finite class-field character dictionary'),
 'str_gen':(G+'StrGen.lean','Full strGen with its local-invariant correction'),
 'b1p':(G+'B1p.lean','Original b1p at actual FLink'),
 'b1':(G+'PsiLocalPairEqLocal.lean','Original b1 on doubled local family'),
 'h1':(G+'CastToZModPowOne.lean','Original h1 conclusion; shorter CM/Kummer proof here'),
 'h1_general':(G+'CharacterH1GaloisQuotient.lean','Broader source supplier not claimed reconstructed; only trivial-character specialization replaced'),
 'level_s':(G+'LevelS.lean','Exact finite ramification quotient and normal-closure kernel'),
 'tame_eq':(G+'TameEq.lean','Equivariant inertia correction and extension of cochains'),
 'infl_ker':(G+'InflKer.lean','Actual second-degree inflation defect estimate'),
 'loc_euler':(G+'LocEuler.lean','Local finite-module Euler and duality identities'),
 'glob_euler':(G+'GlobEuler.lean','Global finite-module Euler identity'),
 'pt_tail':(G+'PtTail.lean','Normalized Poitou-Tate tail and coefficient trace'),
 'h2_eq':(G+'H2GaloisQuotientEq.lean','Full quotient global H2 inequality'),
 'h2_surj':(G+'H2GaloisQuotientSurjective.lean','Local coefficient quotient inequality'),
 'h2_right':(G+'H2RightExactModL.lean','Source local H2 right-exactness; natural Tate-duality proof used here'),
 'cone':(G+'ConeCount.lean','Literal cone maps and dimension identity'),
 'ec':(G+'ResH1SurjectiveOfIsomorphism.lean','Full GC.ec'),
 'clrk_tr':(F+'ClrkTr.lean','Exact fixed-field XDual transport'),
 'frame_ex':(F+'FrameEx.lean','rk_link, ok_link and full original frame_ex'),
 'seed':(F+'SeedCl.lean','Original coefficient-DVR seed_cl, inherited CAF7'),
 'gd_entry':(F+'SqrtDiscr.lean','Separate gen_gd entry remains unsupplied here'),
 'host_entry':(F+'GenHost.lean','Separate gen_host entry and actual Hb remain unsupplied here'),
}
REL={
 1:([],['fin_char','rad_exists','card_sel','card_sunit','dvd_ine'],[]),
 2:([1],['phi_def','phi','phi_wrapper','link_defs'],[]),
 3:([],['cl','link_defs','cl_pull'],[]),
 4:([],['dec_zhat','tame_eq','h2_eq'],[]),
 5:([4],['gen_dec','dec_zhat','loc_euler'],[]),
 6:([5],['gen','frame_defs','link_defs'],[]),
 7:([],['xdual','cl_pull','str_gen'],[]),
 8:([7],['str_gen','frame_defs'],[]),
 9:([8],['b1p','link_defs'],[]),
 10:([8],['b1','link_defs'],[]),
 11:([1],['h1','h1_general','card_sel','card_sunit'],[]),
 12:([7,11],['h1','frame_defs','link_defs'],[]),
 13:([],['level_s','link_defs'],[]),
 14:([4],['tame_eq','loc_euler','h2_eq'],[]),
 15:([],['infl_ker'],[]),
 16:([],['glob_euler','pt_tail','loc_euler','hc_defs','link_defs'],[]),
 17:([13,14,15,16],['h2_eq'],[]),
 18:([17],['h2_surj','h2_right','loc_euler'],[]),
 19:([],['cone','frame_defs'],[]),
 20:([17,18,19],['ec','frame_defs','link_defs','loc_euler'],[]),
 21:([2,3,6,9,10,12,20],['frame_ex','clrk_tr','gen_defs','frame_defs'],
          ['MFC4','MFC5','MFC8','MFC9','MFC13','MFC14']),
 22:([21],['frame_ex','gen_defs'],['MFC1','MFC4','MFC5','MFC6','MFC8','MFC12','MFC13','CAF5','CAF8','TW1']),
 23:([22],['seed','has_frame','gd_entry','host_entry'],['CAF7','CAF11']),
}
EXT={
 'LFC_GALOIS_BACKGROUND':{
   'kind':'standard_algebraic_number_theory',
   'statement':'Finite/infinite Galois correspondence; valuations, local residue-field Frobenius, inertia and finite ramification; linear independence of field embeddings. The needed quotient, Kummer, parity, group and cone calculations are proved in the numbered claims.',
   'source_keys':['link_defs','dec_zhat','level_s','rad_exists']},
 'LFC_UNITS_CLASSES_RECIPROCITY':{
   'kind':'named_classical_number_theory',
   'statement':'Dirichlet unit theorem, finiteness of the ideal class group, and finite class-field reciprocity. The reciprocity dictionary is the same retained classical foundation as MFC5/TW1. The Kummer ideal sequence, coefficient extension, CM minus-unit argument and every required rank comparison are proved here.',
   'source_keys':['fin_char','card_sel','card_sunit','cl_pull']},
 'LFC_ORIGINAL_P':{
   'kind':'original_theorem_antecedent',
   'statement':'Original GC.Hypotheses2, using local finiteness/Tate duality/Euler characteristic and global finiteness/Euler characteristic/normalized Poitou-Tate at their precise finite-module instances. The inherited MFC strict classes retain their original Greenberg-Wiles premise.',
   'source_keys':['link_defs','hc_defs','loc_euler','glob_euler','pt_tail']},
 'LFC_FULL_GEN':{
   'kind':'original_theorem_antecedent',
   'statement':'All nineteen fields of original Gen, including actual Hb, its ell-power index and inertia containment, residual local square separation, and exact Teich lifting. Full gen_gd/gen_host are separate unsupplied entry theorems. Coefficient-DVR hypothesis is required only for LFC23 SeedClause join.',
   'source_keys':['gen_defs','has_frame','gd_entry','host_entry']},
}
USES={i:['LFC_GALOIS_BACKGROUND'] for i in REL}
for i in [1,2,3,7,11,12]:USES[i].append('LFC_UNITS_CLASSES_RECIPROCITY')
for i in [5,6,14,16,17,18,20,21,22,23]:USES[i].append('LFC_ORIGINAL_P')
for i in [21,22,23]:USES[i].append('LFC_FULL_GEN')

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(n,o):(HERE/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')

def inherited(cid):
    component=('marked_frame_construction_v50' if cid.startswith('MFC') else
               'simultaneous_cohomological_windows' if cid=='TW1' else
               'common_arithmetic_frame_v50')
    rel=component+'/main.tex'; raw=(ROOT/rel).read_bytes(); txt=raw.decode()
    provrel=component+'/provenance.json'; provraw=(ROOT/provrel).read_bytes()
    prov=json.loads(provraw)
    old=next(c for c in prov['claims'] if c['id']==cid)
    loc=old['proof_location']
    if 'line_start' in loc:
        first,last=loc['line_start'],loc['line_end']
        piece=b''.join(raw.splitlines(keepends=True)[first-1:last])
    else:
        match=re.search(r'% BEGIN '+re.escape(cid)+r'\n.*?% END '+re.escape(cid)+r'\n',txt,re.S)
        if match is None:raise ValueError(('missing inherited proof block',cid,loc))
        piece=match.group().encode();first=txt[:match.start()].count('\n')+1
        last=first+match.group().count('\n')-1
    expected=loc.get('sha256',loc.get('proof_range_sha256'))
    if expected and expected!=sha(piece):raise ValueError(('inherited block hash',cid))
    return {'id':cid,'component':component,'file':rel,'label':'claim:'+cid,
        'file_sha256':sha(raw),'line_start':first,'line_end':last,
        'proof_range_sha256':sha(piece),
        'parent_provenance_file':provrel,'exact_parent_provenance_sha256':sha(provraw),
        'scope':'Inherited human theorem at its exact reviewed scope, with all retained premises'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve()
    if subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()!=PIN:
        raise ValueError('wrong source pin')
    sources={};files={};excerpts=[]
    for key,(rel,title) in SPECS.items():
        blob=subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel])
        if (repo/rel).read_bytes()!=blob:raise ValueError(('source checkout changed',rel))
        lines=blob.splitlines(keepends=True);start=1;end=len(lines)
        dst=ROOT/'source_snapshot_v0_51/arithmetic'/rel
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(blob)
        url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+rel
        files[rel]={'path':rel,'snapshot_file':str(dst.relative_to(ROOT)),
           'sha256':sha(blob),'bytes':len(blob),'line_count':len(lines),
           'verified_equal_to_pinned_git_blob':True,'source_commit':PIN,'url':url}
        sources[key]={'id':'LFC_SRC_'+key.upper(),'path':rel,'declaration':title,
           'line_start':start,'line_end':end,'source_commit':PIN,
           'file_sha256':sha(blob),'full_file_sha256':sha(blob),'range_sha256':sha(blob),
           'range_bytes':len(blob),'snapshot_file':str(dst.relative_to(ROOT)),
           'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
        excerpts.append('['+sources[key]['id']+'] '+title+'\n'+sources[key]['url']+'\n'+blob.decode())
    txt=(HERE/'main.tex').read_text();mainhash=sha(txt.encode())
    blocks={m.group(1):m for m in re.finditer(r'% BEGIN (LFC\d+)\n.*?% END \1\n',txt,re.S)}
    expected={'LFC'+str(i) for i in REL}
    if set(blocks)!=expected:raise ValueError('claim block set mismatch')
    blockhash={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for p in sorted(set(HERE.glob('review_*.json'))|set(HERE.glob('independent_review*.json'))):
        v=json.loads(p.read_text())
        if v.get('result',v.get('status'))!='PASS':continue
        full=v.get('proof_file_sha256',v.get('main_sha256',v.get('main_tex_sha256')))
        if full and full!=mainhash:raise ValueError(('stale review main hash',p))
        rc=v.get('claims_reviewed',v.get('reviewed_claims',[]));ids=[]
        for item in rc:
            cid=item if isinstance(item,str) else item.get('id',item.get('claim'))
            bh=(rc.get(cid) if isinstance(rc,dict) else v.get('proof_hashes',{}).get(cid)) if isinstance(item,str) else item.get('proof_range_sha256',item.get('block_sha256'))
            if bh is None and full==mainhash:bh=blockhash.get(cid)
            if cid not in blockhash or bh!=blockhash[cid]:raise ValueError(('stale review proof block',p,cid))
            ids.append(cid)
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),
          'reviewer':v.get('reviewer'),'result':'PASS','proof_file_sha256':mainhash,'claims':ids})
    reviewed={cid for r in reviews for cid in r['claims']}
    status='complete_at_stated_scope_independently_reviewed' if expected<=reviewed else 'complete_at_stated_scope_pending_independent_review'
    human={cid:inherited(cid) for _,_,ids in REL.values() for cid in ids}
    claims=[]
    for i,(deps,keys,ids) in REL.items():
        cid='LFC'+str(i);m=blocks[cid];start=txt[:m.start()].count('\n')+1
        claims.append({'id':cid,'title':m.group().split('\n')[1],
          'introduced_in':'0.51','classification':'B','depends_on':['LFC'+str(d) for d in deps]+ids,
          'external_input_ids':USES[i],'sources':[sources[k] for k in keys],
          'proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
             'line_start':start,'line_end':start+m.group().count('\n')-1,
             'sha256':blockhash[cid],'bytes':len(m.group().encode())},
          'status':'complete_at_stated_scope_independently_reviewed' if cid in reviewed else 'complete_at_stated_scope_pending_independent_review',
          'independent_review_files':[r['file'] for r in reviews if cid in r['claims']],
          'source_proof_is_not_human_proof':True})
    ext=[{'id':eid,**e,'source_bindings':[sources[k] for k in e['source_keys']]} for eid,e in EXT.items()]
    common={'artifact_version':'0.51','component':HERE.name,'source_commit':PIN,
            'proof_file_sha256':mainhash,'status':status}
    endpoints=[
      {'id':'full_original_phiGam_and_GC_phi','claim':'LFC2'},
      {'id':'full_original_GC_cl','claim':'LFC3','quantifier_order':'one nonzero h before every finite abelian ell-group B and character'},
      {'id':'full_original_genDec_and_GC_gen','claims':['LFC5','LFC6']},
      {'id':'full_original_strGen','claim':'LFC8','arbitrary_coefficient_field':True,'local_invariant_correction_retained':True},
      {'id':'full_original_GC_b1p','claim':'LFC9'},
      {'id':'full_original_GC_b1','claim':'LFC10','doubled_local_family':True},
      {'id':'full_original_GC_h1','claim':'LFC12','simplification':'CM Kummer eigenspace replaces broader CharacterH1GaloisQuotient application'},
      {'id':'full_original_levelS','claim':'LFC13'},
      {'id':'full_original_tameEq','claim':'LFC14'},
      {'id':'full_original_inflKer','claim':'LFC15'},
      {'id':'full_original_H2_galois_quotient_eq','claim':'LFC17'},
      {'id':'full_original_H2_galois_quotient_surjective','claim':'LFC18'},
      {'id':'full_original_coneCount','claim':'LFC19'},
      {'id':'full_original_GC_ec','claim':'LFC20','all_finite_fields_representations_local_subspaces':True},
      {'id':'all_28_Ok_fields_and_Big_on_same_MFC_frame','claim':'LFC21'},
      {'id':'full_original_frame_ex_HasFrameW','claim':'LFC22','entry':'full Gen and original Hypotheses2','coefficient_scope':'general commutative local O with residue field characteristic ell; Gen supplies finiteness'},
      {'id':'original_HasFrame_at_coefficient_DVR','claim':'LFC23','entry':'full Gen and original Hypotheses2 at O=c.O','Q_chosen_before_L_w':True},
    ]
    contracts={'schema':'rh-human-component-contract/1',**common,
      'closed_subcontracts':endpoints,
      'entry_premises':['Full original nineteen-field Gen for final constructors','Original GC.Hypotheses2','Inherited MFC1–MFC14 at exact scope','Inherited CAF5/CAF7/CAF8/CAF11','Inherited TW1 and named classical inputs'],
      'actual_output':['all seven missing Ok fields on same frame','all 28 original Ok fields','same Big C0','actual HasFrameW for every prior Q>0','HasFrame and character SeedClause at original coefficient DVR'],
      'remaining_Ok_fields':[],'all_28_Ok_fields_completed':True,
      'full_original_Gen_supplied_for_Dat':False,'full_original_Gen_supplied_for_HostData':False,
      'full_HasFrameW_closed_at_original_premises':True,
      'full_HasFrame_closed_at_full_Gen_and_coefficient_DVR':True,
      'full_GdFrameEx_closed':False,'full_HostFrameEx_closed':False,'full_GdEnd_closed':False,
      'both_automorphic_seed_producers_remain_open':True,'original_alt_matching_remains_open':True,
      'host_ell_3_allowed':True,
      'choice_order':['for HasFrame: CAF7 core characters and Q first','H0','w=1 mod Q','C0 uniform for every m','m=3C0+7','L','g1','Phi','both strict classes and all 28 Ok fields on same Phi/C0','character SeedClause on same L at O=c.O'],
      'selected_producer_closed':False,'new_global_frontier_leaf_closures':[],
      'simplifications':['h1 from omega eigenspace of Kummer S-unit/class sequence, with integral valuation-lattice eigenspace argument','local H2 coefficient surjectivity from natural perfect Tate duality'],
      'root_ledger_modified':False,'no_lean_replay':True}
    dump('contracts.json',contracts);dump('original_contracts.json',contracts)
    dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
      'claims':claims,'inherited_human_inputs':list(human.values()),
      'classical_and_foundational_inputs':ext,'independent_reviews':reviews,
      'source_proof_is_not_human_proof':True,'root_ledger_modified':False})
    dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
      'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
      'files':list(files.values()),'ranges':list(sources.values()),
      'file_count':len(files),'range_count':len(sources)})
    dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
      'closed_subcontracts':endpoints,'independent_reviews':reviews,
      'pending_review_claims':sorted(expected-reviewed,key=lambda x:int(x[3:])),
      'remaining_Ok_fields':[],'proposed_global_frontier_leaf_closures':[],
      'new_global_frontier_leaf_closures':[],
      'full_HasFrameW_closed_at_original_premises':True,
      'full_HasFrame_closed_at_full_Gen_and_coefficient_DVR':True,
      'full_GdFrameEx_and_HostFrameEx_remain_open':True})
    dump('retained_foundations.json',ext)
    dump('classical_inputs.json',{'schema':'rh-classical-input-registry/1',**common,'inputs':ext})
    dump('published_inputs.json',[])
    dump('claim_dag.json',{'schema':'rh-human-claim-dag/1',**common,
      'claims':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims]})
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    report="""LINKED FRAME COMPLETION — v0.51

LFC1–LFC23 complete all seven remaining original Ok fields:
phi, gen, cl, ec, b1p, b1, h1. All conclusions apply to the
SAME MFC frame, Phi, CM L, marked g1, and class-rank bound C0.

The packet proves full PhiCond over every open subgroup; one uniform
class exponent before every finite abelian ell-group character; exactly
dv local generators with the one allowed cyclotomic exception; the
literal StrGen cocycle/local-primitive dictionary and both strict rank
bounds; and the full cone Euler inequality for all finite coefficient
fields, representations and stable local conditions.

The h1 proof uses a shorter Kummer/CM-unit argument. The omega part of
the unit contribution is at most one. Its S-unit valuation lattice is
handled over Z_ell with the lifted idempotent before reducing, so no
false reduction-of-inclusions assertion is used. The class contribution
injects into the same literal XDual group bounded by C0.

The full original frame_ex/HasFrameW theorem is proved under FULL Gen
and original GC.Hypotheses2, for every Q chosen first, with general
commutative local O. CAF7 chooses Q first in the original Coef DVR case;
CAF11 then installs the character SeedClause on the SAME L/Phi/g1 and
gives HasFrame. Host ell=3 remains allowed.

EXACT BOUNDARY
Full Gen_gd and Gen_host remain separate entry suppliers. In particular
host Hb=ker(dirG(kappaB)), its index, inertia containment, exact Teich
lifting and local nonquadratic witness have not been replaced by CAF's
weaker seed data. Full GdFrameEx/HostFrameEx and common GdEnd therefore
remain open. Both automorphic seed representations, shared coefficient
extension and original/alternative endpoint matching remain open.
No whole selected compound leaf or complete human RH/Dirichlet GRH
proof is claimed closed.

Classical inputs: Dirichlet units, class-group finiteness, finite
class-field reciprocity; original P local/global cohomology laws.
TW1 and all MFC/CAF proofs are inherited at their exact reviewed scope.
All snapshots are byte-equal to pinned git blobs. No Lean replay or PDF.
"""
    (HERE/'report.txt').write_text(report+f'\nPin: {PIN}\nMain SHA256: {mainhash}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}\n')
    dump('hashes.json',{'component':HERE.name,'artifact_version':'0.51',
      'hashes':{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
                if p.is_file() and p.name!='hashes.json'}})
    print(json.dumps({'component':HERE.name,'claims':len(claims),
      'source_files':len(files),'main_sha256':mainhash,'status':status},indent=2))

if __name__=='__main__':main()
