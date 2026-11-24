#!/usr/bin/env python3
"""Rebuild the marked arithmetic frame packet and immutable source bindings."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMPONENT=HERE.name
V='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
F=V+'FrobeniusSmoothVectors/'

SPECS={
 'gen_defs':(F+'FrobeniusSplitPrimeDatum.lean','Gen, Hth, Hlay, UFacts, StrictCl, Linked, HasFrameW',None),
 'frame_defs':(F+'ContinuousCoboundaries2.lean','Actual Frame, cone cohomology, all 28 Ok fields and Big',None),
 'link_defs':(V+'CurveDVRSpecialization/HostFrameEx.lean','Actual GalLink, HasFrame, SeedClause and original exits',None),
 'coh_defs':(V+'GaloisCochains/GLinkQuot.lean','Hypotheses2, clRk, tameN, GLink, LLink, FLink',None),
 'hc_defs':(V+'LevelCohomology/HcDefs.lean','Exact retained HcPublished fields',None),
 'h0':(F+'EtaleSimplicialCochainSchemeSectionExtensionNatu.lean','exists_twistCharacter_continuousCohomology; same output via elementary CRT',None),
 'hlay':(F+'HlayPlace.lean','Full cyclotomic layer and inertia properties',None),
 'hth':(F+'HthPlace.lean','Exact Hth local and index properties; inherited CAF4',None),
 'l15':(F+'RootOfUnityEqOneOfCloseResidue.lean','Residual identity persistence l15 and power absorption',None),
 'ufacts':(F+'Ufacts.lean','Full original ufacts record','theorem UpperTheory.V.Fr.ufacts'),
 'b0':(F+'RankLeOfCardLe.lean','Uniform original b0 before every later m',None),
 'xdual':(V+'GaloisLibrary/KummerTheory/Mk0IdMapCongr.lean','Literal XDual inertia and decomposition conditions','def XDual'),
 'cl_pull':(V+'GaloisLibrary/KummerTheory/PullOnto.lean','Original class-character pullback onto XDual',None),
 'cl_card':(V+'QuadraticExtensions/CardClDual.lean','Original finite class-character bound',None),
 'field':(F+'FieldEx.lean','Literal field_ex; inherited CAF8',None),
 'auxw':(F+'AuxwEx.lean','Original auxw_ex; inherited CAF5',None),
 'seed':(F+'SeedCl.lean','Original seed_cl; inherited CAF7',None),
 'link':(F+'LinkEx.lean','Full original link_ex, including all local identifications',None),
 'basic':(F+'OkBasic.lean','Full original ok_basic conclusions','theorem UpperTheory.V.Fr.ok_basic'),
 'st_sel':(F+'StSel.lean','Full st_sel and actual global/local quotient transport',None),
 'st_count':(F+'StCount.lean','Greenberg-Wiles cardinal construction of a nonzero class',None),
 'st_local':(F+'DualNontriv.lean','Local cohomology cardinal strict inequality',None),
 'st_conj':(F+'StConj.lean','Exact conjugate local coboundary primitive',None),
 'st_res':(F+'StRes.lean','Restriction detects a global coboundary',None),
 'st_tame':(F+'StTame.lean','Tame inertia and the index-ell kernel',None),
 'strict':(F+'Strict.lean','Full strict for both residual characters',None),
 'f4':(F+'FrobeniusGaloisFieldFourCompatibility.lean','Exact strict-cocycle descent to the original cone',None),
 'frame_ex':(F+'FrameEx.lean','Original final frame constructor and seven remaining GC fields',None),
 'gd_gen':(F+'SqrtDiscr.lean','Full gen_gd remains a separate original input supplier','theorem UpperTheory.V.Fr.gen_gd'),
 'host_gen':(F+'GenHost.lean','Full gen_host remains separate from the CAF seed subset','theorem UpperTheory.V.Fr.gen_host'),
}

REL={
 1:([],['h0','gen_defs'],[]),
 2:([],['hlay','gen_defs'],[]),
 3:([1,2],['l15','gen_defs'],['CAF4']),
 4:([1,2,3],['ufacts','gen_defs'],['CAF4']),
 5:([2],['b0','xdual','cl_pull','cl_card'],['TW1','CAF4']),
 6:([4,5],['frame_ex','field','gen_defs'],['CAF8']),
 7:([4,6],['link','link_defs','coh_defs'],[]),
 8:([7],['link','link_defs','coh_defs','frame_defs'],[]),
 9:([4,6,7,8],['basic','frame_defs','frame_ex'],[]),
 10:([],['st_sel','st_count','st_local','st_conj','coh_defs','hc_defs'],[]),
 11:([],['st_res','st_tame'],[]),
 12:([4,10,11],['strict','gen_defs'],['CAF4']),
 13:([8,12],['f4','frame_defs','link_defs'],[]),
 14:([1,4,5,6,8,9,12,13],['frame_ex','link_defs','seed','gd_gen','host_gen'],['CAF5','CAF7']),
}
EXT={
 'MFC_FULL_GEN':{'kind':'original_theorem_antecedent','statement':'Full nineteen-field Gen, including local square separation, actual Hb, its ell-power index, and exact Teich lifting. CAF seed-only entry is not substituted.','source_keys':['gen_defs']},
 'MFC_COH_HYP2':{'kind':'original_theorem_antecedent','statement':'Original GC.Hypotheses2 retained. The strict-class proof uses its local finiteness, local Tate duality, local Euler characteristic, global finiteness and Greenberg-Wiles fields, at their exact finite-module instances.','source_keys':['coh_defs','hc_defs']},
 'MFC_GALOIS_LOCAL_BACKGROUND':{'kind':'standard_algebraic_number_theory','statement':'Finite/infinite Galois correspondence, profinite quotients, valuations and completion, Eisenstein/Hensel, and tame inertia structure. Specific subgroup, ramification, orbit and degree conclusions are proved in MFC1–MFC8.','source_keys':['h0','hlay','link','st_tame']},
 'MFC_CLASS_FIELD_BACKGROUND':{'kind':'inherited_named_classical_input','statement':'Finite class-field reciprocity in TW-CF identifies continuous everywhere-unramified finite additive characters with ideal-class-group characters. MFC5 checks its actual XDual module and fixed-field instances. Ferrero-Washington uniform rank is inherited through TW1, not asserted as a new proof.','source_keys':['cl_pull','cl_card','b0']},
}
USES={i:['MFC_FULL_GEN','MFC_GALOIS_LOCAL_BACKGROUND'] for i in REL}
USES[5]+=['MFC_CLASS_FIELD_BACKGROUND']
USES[10]=['MFC_COH_HYP2','MFC_GALOIS_LOCAL_BACKGROUND']
USES[11]=['MFC_GALOIS_LOCAL_BACKGROUND']
USES[12]+=['MFC_COH_HYP2']
USES[14]+=['MFC_COH_HYP2']

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def inherited(cid):
    component='simultaneous_cohomological_windows' if cid=='TW1' else 'common_arithmetic_frame_v50'
    data=(ROOT/component/'main.tex').read_bytes()
    return {'id':cid,'component':component,'file':component+'/main.tex','label':'claim:'+cid,'file_sha256':sha(data),
      'scope':'Exact uniform finite-layer class-rank theorem and retained classical inputs' if cid=='TW1' else 'Inherited human proof at its exact original scope'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve()
    head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
    if head!=PIN:raise ValueError(('wrong source HEAD',head))
    sources={};files={};excerpts=[]
    for key,(rel,title,marker) in SPECS.items():
        blob=subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel])
        if (repo/rel).read_bytes()!=blob:raise ValueError(('changed source file',rel))
        lines=blob.splitlines(keepends=True); start=1
        if marker:
            starts=[i+1 for i,l in enumerate(lines) if l.decode().startswith(marker)]
            if len(starts)!=1:raise ValueError(('ambiguous marker',rel,marker,starts))
            start=starts[0]
        end=len(lines);piece=b''.join(lines[start-1:end])
        dst=ROOT/'source_snapshot_v0_50/marked_arithmetic'/rel
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(blob)
        url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+rel
        files[rel]={'path':rel,'snapshot_file':str(dst.relative_to(ROOT)),'sha256':sha(blob),'bytes':len(blob),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,'source_commit':PIN,'url':url}
        sources[key]={'id':'MFC_SRC_'+key.upper(),'path':rel,'declaration':title,'line_start':start,'line_end':end,'source_commit':PIN,'file_sha256':sha(blob),'full_file_sha256':sha(blob),'range_sha256':sha(piece),'range_bytes':len(piece),'snapshot_file':str(dst.relative_to(ROOT)),'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{start}-L{end}'}
        excerpts.append('['+sources[key]['id']+'] '+title+'\n'+sources[key]['url']+'\n'+piece.decode())
    tex=(HERE/'main.tex').read_text(); mainhash=sha(tex.encode())
    blocks={m.group(1):m for m in re.finditer(r'% BEGIN (MFC\d+)\n.*?% END \1\n',tex,re.S)}
    expected={'MFC'+str(i) for i in REL}
    if set(blocks)!=expected:raise ValueError('claim block set mismatch')
    blockhash={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for p in sorted(set(HERE.glob('review_*.json')) | set(HERE.glob('independent_review*.json'))):
        v=json.loads(p.read_text())
        if v.get('result',v.get('status'))!='PASS':continue
        full=v.get('proof_file_sha256',v.get('main_sha256',v.get('main_tex_sha256')))
        if full and full!=mainhash:raise ValueError(('stale main review',p))
        rc=v.get('claims_reviewed',v.get('reviewed_claims',[]));ids=[]
        for item in rc:
            cid=item if isinstance(item,str) else item.get('id',item.get('claim'))
            bh=(rc.get(cid) if isinstance(rc,dict) else v.get('proof_hashes',{}).get(cid)) if isinstance(item,str) else item.get('proof_range_sha256',item.get('block_sha256'))
            if bh is None and full==mainhash:bh=blockhash.get(cid)
            if cid not in blockhash or bh!=blockhash[cid]:raise ValueError(('stale block review',p,cid))
            ids.append(cid)
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'reviewer':v.get('reviewer'),'result':'PASS','proof_file_sha256':mainhash,'claims':ids})
    reviewed={cid for r in reviews for cid in r['claims']}
    status='complete_at_stated_scope_independently_reviewed' if expected<=reviewed else 'complete_at_stated_scope_pending_independent_review'
    human={cid:inherited(cid) for _,_,ids in REL.values() for cid in ids}
    claims=[]
    for i,(deps,keys,ids) in REL.items():
        cid='MFC'+str(i);m=blocks[cid];start=tex[:m.start()].count('\n')+1
        title=m.group().split('\n')[1]
        claims.append({'id':cid,'title':title,'introduced_in':'0.50','classification':'B','depends_on':['MFC'+str(d) for d in deps]+ids,
          'external_input_ids':USES[i],'sources':[sources[k] for k in keys],
          'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':start+m.group().count('\n')-1,'sha256':blockhash[cid],'bytes':len(m.group().encode())},
          'status':'complete_at_stated_scope_independently_reviewed' if cid in reviewed else 'complete_at_stated_scope_pending_independent_review',
          'independent_review_files':[r['file'] for r in reviews if cid in r['claims']], 'source_proof_is_not_human_proof':True})
    ext=[{'id':eid,**e,'source_bindings':[sources[k] for k in e['source_keys']]} for eid,e in EXT.items()]
    common={'artifact_version':'0.50','component':COMPONENT,'source_commit':PIN,'proof_file_sha256':mainhash,'status':status}
    endpoints=[
     {'id':'full_original_real_quadratic_H0','endpoint':'UpperTheory.V.Fr.exists_twistCharacter_continuousCohomology','claim':'MFC1','simplification':'CRT with an auxiliary integer of odd valuation replaces a prime progression'},
     {'id':'full_original_hlay','claim':'MFC2'}, {'id':'full_original_l15','claim':'MFC3'},
     {'id':'full_original_ufacts','claim':'MFC4'}, {'id':'full_original_b0','claim':'MFC5','inherited_human_input':'TW1'},
     {'id':'full_original_link_ex','claim':'MFC8'}, {'id':'full_original_ok_basic','claim':'MFC9'},
     {'id':'full_original_st_sel','claim':'MFC10','retained_original_premise':'GC.Hypotheses2'},
     {'id':'full_original_strict','claim':'MFC12','retained_original_premise':'GC.Hypotheses2'},
     {'id':'full_original_frobenius_galoisField_four_compatibility','claim':'MFC13'},
     {'id':'actual_marked_frame_with_21_Ok_fields_Big_and_seed','claim':'MFC14','whole_HasFrameW':False}]
    remaining=['phi','gen','cl','ec','b1p','b1','h1']
    contracts={'schema':'rh-human-component-contract/1',**common,'closed_subcontracts':endpoints,
     'entry_premises':['Full original Gen','Original GC.Hypotheses2 for strict classes','Inherited CAF4/CAF5/CAF7/CAF8','Inherited TW1 and finite class-field reciprocity'],
     'actual_output':['same embedded CM L and maximal real field','same marked g1 in D_B intersect G_L','actual profinite quotient and all GalLink/FLink fields','both strict cohomology classes on same quotient','Big C0','21 of 28 exact Ok fields','original SeedClause at original Coef DVR'],
     'remaining_Ok_fields':remaining,'full_original_Gen_supplied_for_Dat':False,'full_original_Gen_supplied_for_HostData':False,
     'full_GdFrameEx_closed':False,'full_HostFrameEx_closed':False,'full_HasFrameW_closed':False,'full_GdEnd_closed':False,
     'both_automorphic_seed_producers_remain_open':True,'original_alt_matching_remains_open':True,
     'choice_order':['Q before construction','H0','w with w=1 mod Q','C0 uniform for every m','m=3C0+7','L','g1','Phi','both strict cocycles on same data','character seed on same L'],
     'selected_producer_closed':False,'new_global_frontier_leaf_closures':[],
     'simplifications':['H0 from CRT with n=-1 mod4M and v_p(n)=1, preserving every original output field'],
     'root_ledger_modified':False,'no_lean_replay':True}
    dump('contracts.json',contracts);dump('original_contracts.json',contracts)
    dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,'inherited_human_inputs':list(human.values()),'classical_and_foundational_inputs':ext,'independent_reviews':reviews,'source_proof_is_not_human_proof':True,'root_ledger_modified':False})
    dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
    dump('closure.json',{'schema':'rh-human-component-closure/1',**common,'closed_subcontracts':endpoints,'independent_reviews':reviews,'pending_review_claims':sorted(expected-reviewed,key=lambda x:int(x[3:])),'remaining_Ok_fields':remaining,'proposed_global_frontier_leaf_closures':[],'new_global_frontier_leaf_closures':[],'full_GdFrameEx_and_HostFrameEx_remain_open':True})
    dump('retained_foundations.json',ext);dump('classical_inputs.json',{'schema':'rh-classical-input-registry/1',**common,'inputs':ext});dump('published_inputs.json',[])
    dump('claim_dag.json',{'schema':'rh-human-claim-dag/1',**common,'claims':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims]})
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    report='''MARKED ARITHMETIC FRAME CONSTRUCTION — v0.50

MFC1–MFC14 construct a single actual arithmetic frame from the full Gen.
The complete original H0, hlay, l15, UFacts, b0, link_ex, ok_basic,
st_sel, strict and strict-to-cone suppliers are now written as human proofs.

The new H0 proof uses CRT: a fresh odd p, n=-1 mod4M and n=p mod p^2,
then Q(sqrt(D*n)). Every original local, real and ramification field is
proved. No prime-in-progression theorem is needed for this step.

The class bound C0 is chosen uniformly before m by applying inherited TW1
to the exact fixed abelian field. The actual quotient kills precisely the
closed normal closure of allowed inertia intersections. All GalLink/FLink
fields, every local place and local degree, the original g1 and characters
are retained. Two nonzero strict classes descend to this same quotient.
The construction also has Big and the exact character SeedClause.

EXACT BOUNDARY
21 of the 28 source Ok fields are supplied. The remaining seven are
phi, gen, cl, ec, b1p, b1, h1, on this SAME Phi and C0. In particular the
bare class-rank bound has not been substituted for the three twisted or
local cone-rank bounds. Full Gen_gd and Gen_host are separate actual-input
suppliers, beyond the CAF seed subset. The host Hb must remain ker(kappaB).
Original GC.Hypotheses2 is retained for strict classes. TW1 and its named
classical foundations are inherited. Both automorphic seed representations,
shared coefficient extension and original/alternative matching remain open.
No selected compound obligation, full GdFrameEx/HostFrameEx/GdEnd, or whole
human RH/Dirichlet GRH proof is claimed closed by this packet.

Choice order: Q; H0; w; uniform C0; m; L; g1; Phi; both strict classes;
character seed on the same L. No independent frame is substituted later.

All snapshots are byte-equal to pinned git blobs. No Lean replay is claimed.
'''
    (HERE/'report.txt').write_text(report+f'\nPin: {PIN}\nMain SHA256: {mainhash}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}\n')
    dump('hashes.json',{'component':COMPONENT,'artifact_version':'0.50','hashes':{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}})
    print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'main_sha256':mainhash,'status':status},indent=2))

if __name__=='__main__':main()
