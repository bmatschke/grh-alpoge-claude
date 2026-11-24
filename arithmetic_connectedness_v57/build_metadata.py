#!/usr/bin/env python3
"""Bind ACC human proofs, original scopes, and inherited inputs; never run Lean."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION='0.57'
V='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
F=V+'FrobeniusSmoothVectors/'
C=V+'CurveDVRSpecialization/'
T=V+'AlgebraTools/ConnectedPrimeFields/'
A=V+'CommutativeAlgebra/'
M=V+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
SPECS={
 'co':(A+'ResMapBijective.lean',9,75,'Original IsCO coefficient algebra'),
 'space':(F+'LeAdicClosure.lean',9,219,'Original NRep, actual graded entry A, complete weight-zero B, all entry ideals'),
 'loc':(F+'LeAdicClosure.lean',220,259,'Every original Loc, specified Oprime, residue map, iota and universal property'),
 'frame':(F+'ContinuousCoboundaries2.lean',124,214,'Full original Frame/Ok/Big, all finite-character, cohomology and quantitative fields'),
 'cochains':(F+'ContinuousCoboundaries2.lean',11,111,'Strict cocycles and exact cohomology quotient'),
 'integral':(F+'Integral.lean',50,None,'Actual contraction, Pres, separate EPres and full Chained/Sharp definitions'),
 'c1ch':(F+'EnnrealVolumeRatioStepCancel.lean',24,51,'Full original c1ch; general complete Noetherian local prime-nilradical scope'),
 'clcomp':(T+'ClComp.lean',1,None,'Original component-dimension body, not separately claimed at all IsCL scopes'),
 'clchain':(T+'ClChain.lean',1,None,'Original connected-chain body; ACC uses a precise classical connectedness theorem'),
 'clconn':(T+'ClConn.lean',1,None,'Original connectedness input and arithmetic-rank scope'),
 'sharp2':(F+'ChainedBot.lean',1,86,'Surjective quotient transport and full original sharp2'),
 'pres':(F+'HasObs.lean',26,124,'Original presentation supplied by inherited APD25, exact N=Nprime+n*d+1'),
 'locdim':(F+'LocDim.lean',1,None,'Full original loc_dim, both upper inequality and exact dimension prime above every eta'),
 'fibre':(F+'TrdegQuotLeOne.lean',1,None,'Full original off-triangular transcendence-degree bound in both ranks'),
 'fibdim':(F+'FibDim.lean',1,None,'Original fibre dimension target; ACC supplies strengthened rank-two specialization only'),
 'framespace':(F+'FinrankFrameSpaceEq.lean',1,None,'Original triangular fibre algebra and dimension supplier; rank-two proof given directly'),
 'abgen':(F+'AbEval.lean',1,None,'Full original ab_gen finite abelian ell-group character detector'),
 'localres':(F+'LocalDeformationTraceModMaximal.lean',1,None,'Original actual local residue, character and continuity dictionary'),
 'l51':(F+'CharpolyCoeffsInSubalgebra.lean',1,84,'Original l51 and radical containment; ACC completes rank two only'),
 'tame':(F+'TameInertiaCondition.lean',1,280,'Exact finite-character limit, full dim_B and full l52 at both ranks'),
 'strictdim':(F+'KrullDimLtOfNotLeTriangular.lean',1,58,'Original strict bad-locus dimension theorem; rank-two specialization supplied'),
 'nice':(C+'NicePrimeEx.lean',1,None,'Full NicePrimeEx for every Noetherian local ring and arbitrary starting ideal'),
 'nice_contract':(C+'FlipTwoThree.lean',7,66,'Exact NicePrimeEx, LocData and GlobData contracts'),
 'nice_app':(C+'ExistsNicePrimeAboveOfLargeDim.lean',1,None,'Original Nice curve application, including nonprime starting ideal; rank two supplied'),
 'prop_contract':(C+'PropagationTheoremGL2.lean',16,84,'Original Nice, P1prime, P23prime, SeedIn, GL2/GL3 and finite-point contracts'),
 'gl2':(C+'ComponentsGoodRankTwo.lean',1,163,'Full original rank-two local/global component construction'),
 'abs_main':(C+'AbsMain.lean',1,30,'Actual two-rank consumer; separate maps, rings, ModIn packages and seeds'),
 'minhom':(F+'MinHom.lean',1,None,'Full min_hom on the actual integer grading'),
 'jac':(F+'FibreClosed.lean',1,None,'Full jac for every locally closed part of the original coefficient fibre'),
 'l41':(F+'MonMemPow.lean',1,None,'Full graded Nakayama and l41 homogeneous-prime incidence'),
 'homseed':(F+'FrobeniusCornerLiftTwoToThree.lean',1,None,'Original homogeneous seed-prime supplier; rank-two specialization supplied'),
 'seedpt':(F+'Seedpt.lean',1,None,'Original seedpt with x chosen before every later Loc; rank-two specialization supplied'),
 'locrho':(F+'LocRho.lean',1,None,'Actual continuity, residues, all ideal comparisons, triangular endpoint'),
 'locflat':(F+'LocFlat.lean',1,None,'Actual local chart flatness and exact x over mB'),
 'loccpl':(F+'LocCpl.lean',162,188,'Canonical completion of Oprime tensor A at the prescribed point'),
 'graded':(F+'IsInternalCongr.lean',81,86,'Generic upstream gr_A, independent of FinA'),
 'gl3':(C+'PropagationTheoremGL3.lean',213,229,'Retained rank-three component producer and its exact original inputs'),
 'sharp3':(F+'ChainedOfComap.lean',72,142,'Retained rank-three Sharp/EPres branch, not inferred from ordinary Pres'),
 'tworuns':(M+'TwoRuns.lean',80,109,'Actual two-run construction with separate rank-specific spaces and ideals'),
 'linked':(M+'LinkedEndE.lean',18,67,'Terminal linked join retaining original coefficient descent and arithmetic entry'),
}

PARENTS={
 'APD25':('arithmetic_presentations_v56','Full original pres on every supplied Loc; N=Nprime+n*d+1'),
 'RTC7':('rank_two_connectedness_v54','Upstream actual co_B, gr_A, direct grading and finite graded pieces without FinA'),
 'RTC9':('rank_two_connectedness_v54','Exact fixed-weight continuity and ideal-power topology'),
 'RTC10':('rank_two_connectedness_v54','Full coefficient-fibre point/residual/continuity dictionary'),
 'RTC13':('rank_two_connectedness_v54','Strict cocycle coefficient expansion for arbitrary target vector spaces'),
 'RTC14':('rank_two_connectedness_v54','Exact strict triangular representation dictionary over arbitrary algebras'),
 'RTC15':('rank_two_connectedness_v54','Actual triangular point realization over every prescribed target algebra'),
 'RTC16':('rank_two_connectedness_v54','Full strict-point uniqueness and functoriality'),
 'RTC19':('rank_two_connectedness_v54','Full original preconnected_rank_two on the same actual core'),
 'ALC4':('arithmetic_local_charts_v55','Full loc_cpl on the exact selected tensor-product localization'),
 'ALC7':('arithmetic_local_charts_v55','Finite-module exactness and quotient comparison for completion'),
 'ALC11':('arithmetic_local_charts_v55','Full actual loc_flat, x maximal and x intersect B=mB'),
 'ALC15':('arithmetic_local_charts_v55','Full types at every field-valued point'),
 'ALC17':('arithmetic_local_charts_v55','Full loc_rho, all ideal comparisons, full local characters and continuity'),
 'ALC21':('arithmetic_local_charts_v55','Full original loc_ex at every original maximal point over mB'),
 'ACP4':('arithmetic_component_propagation_v53','Literal ordinary characteristic-polynomial identity'),
 'ACP14':('arithmetic_component_propagation_v53','Full abstract local propagation with all ten fields'),
 'ACP15':('arithmetic_component_propagation_v53','Full global propagation with all eight fields'),
 'ACP16':('arithmetic_component_propagation_v53','Full ChartOfFlat, actual minimal-component dictionary'),
 'ACP17':('arithmetic_component_propagation_v53','Full local-to-global chart transfer'),
 'ACP11':('arithmetic_component_propagation_v53','Full original FinPtOf at all IsCD test rings, once OffFin is supplied'),
 'RTC24':('rank_two_connectedness_v54','Full original FinPtDown at all ranks and primes'),
 'AFE20':('arithmetic_frame_entries_v52','Original finite-point-to-FinEnd transport on the same marked frame'),
}

REL={
1:([],['clcomp','c1ch'],[]),
2:([1],['c1ch','clcomp','clchain','clconn','integral'],[]),
3:([],['sharp2','integral'],[]),
4:([2,3],['pres','integral','sharp2','sharp3'],['APD25']),
5:([],['locdim','loc','loccpl','locflat','graded'],['RTC7','ALC4','ALC7','ALC11']),
6:([5],['fibre','space','locrho'],['RTC7','ALC17']),
7:([],['frame','cochains','framespace','space'],['RTC10','RTC13','RTC14','RTC15','RTC16']),
8:([5,7],['fibdim','framespace','locrho'],['RTC7','ALC17']),
9:([],['abgen','frame','cochains'],[]),
10:([],['tame'],[]),
11:([9,10],['l51','localres','space','locrho'],['ACP4','RTC7','RTC9','ALC17']),
12:([1,8,11],['l51','strictdim','locrho'],['ALC17']),
13:([4,12],['sharp2','prop_contract'],[]),
14:([1,10],['tame','frame','space'],['RTC7','RTC9']),
15:([5,6,14],['tame','locrho'],['ALC17']),
16:([12,15],['strictdim'],[]),
17:([1],['nice','nice_contract'],[]),
18:([16,17],['nice_app','prop_contract'],['ALC15','ALC17']),
19:([13,18],['gl2','nice_contract','prop_contract'],['ACP14']),
20:([],['minhom','graded'],['RTC7']),
21:([],['jac','graded'],['RTC7']),
22:([21],['l41','space','graded'],['RTC7']),
23:([],['homseed','space','graded'],['RTC7']),
24:([5,22,23],['seedpt','locrho'],['ALC17']),
25:([13,19],['gl2','locflat','locrho'],['ALC11','ALC17','ALC21','ACP16','ACP17']),
26:([20,21,22,24,25],['gl2','prop_contract'],['RTC7','RTC19','ACP15']),
27:([4,5,6,9,15,17,20,21,22,26],['abs_main','prop_contract','gl3','sharp3','tworuns','linked'],['ACP11','RTC24','AFE20']),
}
SCOPES={
1:'Every Noetherian local ring for cut dimensions; every complete Noetherian local prime-nilradical ring for every minimal component bound',
2:'Full c1ch for every complete Noetherian local ring with prime nilradical, h equations in its maximal ideal and dim>=D+1+h; stronger than original IsCO antecedent',
3:'Every surjective commutative ring map, full minimal-prime/dimension/finite-chain transport',
4:'Every original Loc at either rank, Chained(0,n*d+1), no Big or nontriangularity hypothesis',
5:'Full original loc_dim, both ranks, actual selected Oprime and completion, upper inequality for every prime and exact dimension lift of every eta below x',
6:'Full original fibre at both ranks; arbitrary nonhomogeneous off-triangular prime of actual A; trdeg<=1 before completion',
7:'Actual rank-two strict triangular fibre algebra, with nilpotents retained until the polynomial isomorphism is proved; dimension<=C0',
8:'Every rank-two Loc with lower-entry ideal not contained in x; actual closed coefficient fibre dimension<=C0',
9:'Full ab_gen on any field/frame satisfying original Ok, no chosen coefficient DVR; finite k is included in Ok',
10:'Compact topological group, any characteristic-ell Noetherian local target and adic character; finite-image tests and separated limit, no added completeness or finite residue assumption in first part',
11:'Actual rank-two triangular quotient; exact finite character cuts force the entire coefficient ideal up to radical, all full ordinary characters retained',
12:'Rank-two l51 and stronger d+2*C0+2 bound; strict triangular inequality under original Big; no rank-three l51 claim',
13:'Full original sharp2, all original O,F,C0,S,x,L; Big and lower-entry nonvanishing retained',
14:'Full original coefficient dim_B argument, both ranks, arbitrary ideal p containing I and exact coincident characters; count n*d-dv+2',
15:'Full original l52 in both ranks and all original primes; stronger dim+dv<=n*d+3 implies both original +6 and conditional +5 returns',
16:'Full rank-two specialization of strict bad-locus bound, FinLam/Big and actual ideals retained',
17:'Full NicePrimeEx, arbitrary Noetherian local ring, finite possibly empty bad-ideal family, arbitrary starting ideal, N>=1; no complete/catenary/infinite-field premise',
18:'Full rank-two Nice-curve application for every original Loc and arbitrary high-dimensional starting ideal; actual characteristic and all ordered local tests',
19:'All ten literal rank-two LocData.Ok clauses at original FinLam/P1prime; no new opaque local-propagation premise',
20:'Full min_hom at both original ranks on the direct integer grading',
21:'Full jac at both ranks, every closed C/open U meeting the original core; finite residue extension allowed',
22:'Full l41 at both ranks, every homogeneous prime avoiding lower-entry ideal; actual graded Nakayama proof',
23:'Rank-two homogeneous seed-prime supplier under weak Z subset xi intersect B, with exact contraction and trdeg one',
24:'Full rank-two seedpt: one maximal core x chosen first, then every original Loc at x admits the exact type-I prime, contraction Z and dimension dim(B/Z)+1',
25:'All three original rank-two at_pt conclusions using canonical flat chart; supplied FinLam/P1prime retained',
26:'Full original PropagationTheoremGL2 at literal Ok/Big/FinLam/P1prime/SeedIn, with no strengthened seed equality',
27:'Literal AbsMain rank-two return and exact two-rank next input; rank-three/ModIn/Alt outputs not inferred',
}

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,x): (HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def inherited(cid):
    component,scope=PARENTS[cid]
    ledger=ROOT/component/'provenance.json'; raw=ledger.read_bytes()
    c=next(c for c in json.loads(raw)['claims'] if c['id']==cid)
    loc=c['proof_location']; body=(ROOT/loc['file']).read_bytes()
    piece=b''.join(body.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
    if sha(piece)!=loc.get('sha256',loc.get('proof_range_sha256')): raise ValueError(cid+' inherited proof changed')
    return {'id':cid,'component':component,'file':loc['file'],'label':'claim:'+cid,
      'file_sha256':sha(body),'line_start':loc['line_start'],'line_end':loc['line_end'],
      'proof_range_sha256':sha(piece),'parent_provenance_file':str(ledger.relative_to(ROOT)),
      'exact_parent_provenance_sha256':sha(raw),'scope':scope}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,required=True); args=ap.parse_args()
    repo=args.repo.resolve()
    if subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()!=PIN: raise ValueError('source pin')
    files={}; sources={}; excerpts=[]; texts={}
    for key,(path,first,last,decl) in SPECS.items():
        body=subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path])
        if (repo/path).read_bytes()!=body: raise ValueError(path+' checkout differs')
        lines=body.splitlines(keepends=True); last=last or len(lines)
        if not 1<=first<=last<=len(lines): raise ValueError((key,first,last,len(lines)))
        part=b''.join(lines[first-1:last]); dst=HERE/'source_snapshot'/path
        dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(body)
        url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
        files[path]={'path':path,'snapshot_file':str(dst.relative_to(ROOT)),'sha256':sha(body),'bytes':len(body),
          'line_count':len(lines),'source_commit':PIN,'url':url,'verified_equal_to_pinned_git_blob':True}
        sources[key]={'id':'ACC_SRC_'+key.upper(),'path':path,'declaration':decl,'line_start':first,'line_end':last,
          'source_commit':PIN,'file_sha256':sha(body),'full_file_sha256':sha(body),'range_sha256':sha(part),
          'range_bytes':len(part),'snapshot_file':str(dst.relative_to(ROOT)),
          'verified_equal_to_pinned_git_blob':True,'url':url+f'#L{first}-L{last}'}
        texts[key]=part.decode(); excerpts.append('['+sources[key]['id']+'] '+decl+'\n'+sources[key]['url']+'\n'+part.decode())
    mainbytes=(HERE/'main.tex').read_bytes(); text=mainbytes.decode(); mainsha=sha(mainbytes)
    blocks={m.group(1):m for m in re.finditer(r'% BEGIN (ACC\d+)\n.*?% END \1\n',text,re.S)}
    expected={'ACC'+str(i) for i in REL}
    if set(blocks)!=expected: raise ValueError('proof inventory')
    proofhashes={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for path in sorted(HERE.glob('independent_review*.json')):
        r=json.loads(path.read_text())
        if r.get('result',r.get('status'))!='PASS': continue
        if r.get('proof_file_sha256',r.get('main_sha256',r.get('main_tex_sha256')))!=mainsha: raise ValueError('review main mismatch')
        review_claims=r.get('claims_reviewed',r.get('reviewed_claims',r.get('claims',[])))
        ids=[x if isinstance(x,str) else x.get('id',x.get('claim')) for x in review_claims]
        review_hashes=dict(r.get('proof_hashes',{}))
        for item in review_claims:
            if isinstance(item,dict):
                review_hashes.setdefault(item.get('id',item.get('claim')),item.get('block_sha256',item.get('proof_hash')))
        if any(review_hashes.get(cid)!=proofhashes[cid] for cid in ids): raise ValueError('review block mismatch')
        reviews.append({'file':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'reviewer':r.get('reviewer'),
                        'result':'PASS','proof_file_sha256':mainsha,'claims':ids})
    reviewed={cid for r in reviews for cid in r['claims']}
    status='complete_at_stated_scope_independently_reviewed' if expected<=reviewed else 'complete_at_stated_scope_pending_independent_review'
    common={'artifact_version':VERSION,'component':HERE.name,'source_commit':PIN,'proof_file_sha256':mainsha,'status':status}
    claims=[]
    for i,(deps,keys,parents) in REL.items():
        cid='ACC'+str(i); m=blocks[cid]; first=text[:m.start()].count('\n')+1
        ext=['ACC_CLASSICAL_ALGEBRA']
        if i==2: ext.append('ACC_GROTHENDIECK_CONNECTEDNESS')
        if i in [1,5]: ext.append('ACC_CATENARY_DIMENSION')
        if i>=4: ext.append('ACC_ORIGINAL_DATA')
        claims.append({'id':cid,'title':m.group().splitlines()[1],'introduced_in':VERSION,'classification':'B',
          'depends_on':['ACC'+str(j) for j in deps]+parents,'external_input_ids':ext,'sources':[sources[k] for k in keys],
          'original_scope':SCOPES[i],'proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
             'line_start':first,'line_end':first+m.group().count('\n')-1,'sha256':proofhashes[cid],'bytes':len(m.group().encode())},
          'status':'complete_at_stated_scope_independently_reviewed' if cid in reviewed else 'complete_at_stated_scope_pending_independent_review',
          'independent_review_files':[r['file'] for r in reviews if cid in r['claims']],
          'source_proof_is_not_human_proof':True})
    human=[inherited(cid) for cid in PARENTS]
    external=[
      {'id':'ACC_ORIGINAL_DATA','kind':'original_theorem_antecedent','statement':
       'The supplied original Frame.Ok/Big, each universal Space and actual Loc remain. The full GL2 theorem retains exactly FinLam, P1prime and SeedIn, including the weak inclusion Z subset xi intersect B. No automorphic, ModIn or Alt witness is newly assumed to have been constructed.',
       'source_bindings':[sources[k] for k in ['frame','space','loc','prop_contract','abs_main']]},
      {'id':'ACC_CLASSICAL_ALGEBRA','kind':'named_classical_algebra','statement':
       'Krull height and principal ideal theorems; systems of parameters; finite prime avoidance; Nakayama and Krull intersection; finite-type field algebras and the maximal-ideal theorem; standard finite-dimensional linear algebra. Exact finite-module completion and flat going down are also supplied by inherited ALC and ACP proofs.',
       'source_bindings':[sources[k] for k in ['clcomp','nice','l41','jac']]},
      {'id':'ACC_GROTHENDIECK_CONNECTEDNESS','kind':'precisely_cited_published_theorem','statement':
       'Stacks Lemma 52.14.1 (0ECR), for a complete Noetherian local ring and proper ideal. At irreducible spectrum of dimension r and h generators, removing a closed subset of dimension less than r-1-h leaves a connected space. The cohomological-dimension bound follows from the h-generator Cech complex. ACC2 gives the complete graph/dimension application; regularity is not added.',
       'url':'https://stacks.math.columbia.edu/tag/0ECR','retrieval_ref':'turn998823185view0','source_bindings':[sources['c1ch'],sources['clchain']]},
      {'id':'ACC_CATENARY_DIMENSION','kind':'precisely_cited_published_theorem','statement':
       'Complete Noetherian local rings are universally catenary by Cohen structure (Stacks 032C). The finite-type domain dimension formula is Stacks 02JU/02II. ACC5 applies it before completion, then proves the exact upper/lifting chart comparison using finite flat base change and completion.',
       'urls':['https://stacks.math.columbia.edu/tag/032C','https://stacks.math.columbia.edu/tag/02JU','https://stacks.math.columbia.edu/tag/02II'],
       'retrieval_refs':['turn841149104view0','turn841149104view1','turn841149104view2'],'source_bindings':[sources['clcomp'],sources['locdim']]},
    ]
    endpoint_specs=[('full_original_c1ch',2),('full_surjective_Chained_transport',3),('actual_APD_to_Chained_both_ranks',4),
      ('full_original_loc_dim',5),('full_original_fibre',6),('rank_two_polynomial_strict_fibre',7),
      ('rank_two_stronger_fib_dim',8),('full_original_ab_gen',9),('full_finite_character_adic_limit',10),
      ('rank_two_l51',12),('full_original_sharp2',13),('full_original_dim_B',14),('full_original_l52',15),
      ('rank_two_strict_bad_loci',16),('full_original_NicePrimeEx',17),('rank_two_actual_Nice_application',18),
      ('actual_rank_two_LocData_Ok',19),('full_original_min_hom',20),('full_original_jac',21),('full_original_l41',22),
      ('rank_two_homogeneous_seed_prime',23),('rank_two_full_seedpt',24),('actual_rank_two_at_pt',25),
      ('full_original_PropagationTheoremGL2',26),('literal_AbsMain_rank_two_return',27)]
    endpoints=[{'id':key,'claim':'ACC'+str(i),'scope':SCOPES[i]} for key,i in endpoint_specs]
    retained=[
      {'id':'ACC_RANK_THREE_COMPONENTS','statement':'Original rank-three triangular bound, separate EPres/Sharp determinant-incidence construction, homogeneous seed/corner and thick-chain installation remain. Ordinary Chained is supplied, but not the extra Sharp record.', 'source_keys':['integral','l51','sharp3','homseed','gl3']},
      {'id':'ACC_ORIGINAL_MODIN_AND_AUTOMORPHY','statement':'Actual ModU, PfromAut/patching, both ModIn packages and their arithmetic seeds, FinLam/P1prime/P23prime transfers remain. ACC26 proves full GL2 at its original premises and does not construct these producers.', 'source_keys':['prop_contract','abs_main','tworuns']},
      {'id':'ACC_TERMINAL_AND_ALT','statement':'Full GL3, OffFin producer, GdEnd/HostEnd and Alt witnesses remain. Original P/GC.Hypotheses2 at frame entry, Host ell=3, Q-before-L,w order and common g1 are retained; rank rings/ideals/coefficients remain distinct.', 'source_keys':['prop_contract','gl3','tworuns','linked']},
    ]
    retained=[{**x,'source_bindings':[sources[k] for k in x['source_keys']]} for x in retained]
    flags={
      'full_original_c1ch_supplied':True,'c1ch_general_prime_nilradical_scope':True,
      'c1ch_restricted_to_regular_local':False,'c1ch_additional_IsCO_antecedent_not_needed':True,
      'exact_N_equals_Nprime_plus_n_d_plus_one_preserved':True,'actual_Chained_both_ranks_supplied':True,
      'full_original_loc_dim_supplied':True,'full_original_fibre_supplied':True,'full_original_ab_gen_supplied':True,
      'rank_two_stronger_fibre_bound_supplied':True,'rank_two_l51_supplied':True,'full_original_l51_both_ranks_supplied':False,
      'full_sharp2_supplied':True,'full_original_dim_B_supplied':True,'full_original_l52_supplied':True,
      'l52_stronger_nd_plus_three_bound':True,'full_original_NicePrimeEx_supplied':True,
      'rank_two_actual_Nice_curve_supplier_supplied':True,'full_original_min_hom_supplied':True,
      'full_original_jac_supplied':True,'full_original_l41_supplied':True,'rank_two_full_seedpt_supplied':True,
      'full_seedpt_both_ranks_supplied':False,'full_PropagationTheoremGL2_supplied':True,
      'full_PropagationTheoremGL3_supplied':False,'full_original_EPres_supplied':False,'full_sharp3_supplied':False,
      'rank_two_all_local_and_global_propagation_fields_supplied':True,
      'rank_two_seed_weak_inclusion_preserved':True,'seed_x_chosen_before_every_Loc':True,
      'FinLam_P1prime_SeedIn_are_original_antecedents':True,'ModIn_or_automorphic_seed_producers_supplied':False,
      'actual_OffFin_producer_supplied':False,'actual_automorphic_or_Alt_producer_supplied':False,
      'full_GdEnd_supplied':False,'full_HostEnd_supplied':False,'full_ClComp_and_ClChain_claimed_separately':False,
      'same_A_B_x_Oprime_R_iota_preserved':True,'same_g1':True,'original_P_retained_at_arithmetic_entry':True,
      'host_ell_3_allowed':True,'equal_characteristic_coefficient_DVR_allowed':True,
      'rank_two_and_rank_three_rings_and_ideals_kept_distinct':True,'upstream_FinA_not_assumed':True,
      'transcendence_degree_taken_before_completion':True,'exact_coefficient_uniformizer_cut_retained':True,
      'root_ledger_modified':False,'no_lean_replay':True,'selected_producer_closed':False,
    }
    contracts={'schema':'rh-human-component-contract/1',**common,'closed_subcontracts':endpoints,**flags,
      'choice_order':['Fix the original common frame, marking and separate supplied rank-specific spaces',
         'For each already supplied local object keep x,Oprime,R,iota and its exact residue embedding',
         'Apply APD25 on that same local ring, then construct its component chain',
         'Choose the frame finite-character detectors before every finite test character',
         'At a supplied weak seed pair choose its homogeneous eta, then one maximal core x',
         'Only after fixing x quantify over every original Loc and choose its prime P',
         'Return rank-two AllGood to the separate rank-three consumer without changing ideals or Alt data'],
      'retained_suppliers':retained,'exact_whole_closures':{},'new_global_frontier_leaf_closures':[]}
    dump('contracts.json',contracts)
    dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,'claims':claims,
         'inherited_human_inputs':human,'classical_and_foundational_inputs':external,'independent_reviews':reviews,
         'source_proof_is_not_human_proof':True,'root_ledger_modified':False})
    dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
         'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','files':list(files.values()),
         'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
    dump('inherited_inputs.json',{'schema':'rh-inherited-proof-bindings/1',**common,'inputs':human})
    dump('classical_inputs.json',{'schema':'rh-classical-input-registry/1',**common,'inputs':external[1:]})
    published=[]
    for tag in ['0ECR','032C','02JU','02II']:
        path=HERE/'published_snapshot'/('stacks_'+tag+'.html')
        rec={'id':'ACC_STACKS_'+tag,'url':'https://stacks.math.columbia.edu/tag/'+tag,'retrieved_utc':'2026-11-24',
             'role':'Precisely cited classical input; distinguished from pinned Lean source snapshots'}
        if path.exists(): rec.update({'snapshot_file':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'bytes':path.stat().st_size})
        published.append(rec)
    dump('published_inputs.json',published)
    dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'inputs':external,'still_unsupplied_producers':retained})
    keys=['c1ch','integral','locdim','fibre','abgen','l51','tame','nice_contract','nice_app','prop_contract','minhom','jac','l41','seedpt','gl2','abs_main']
    dump('original_contracts.json',{'schema':'rh-original-contracts/1',**common,'contract_keys':keys,
         'verbatim_source_contracts':{k:texts[k] for k in keys},
         'scope_note':'Full c1ch, sharp2 and GL2 are supplied. Rank-two-only statements are flagged as such. Full l52/loc_dim/fibre/incidence assertions apply to both ranks. No whole terminal closure or original ModIn construction is inferred.'})
    dump('claim_dag.json',{'schema':'rh-human-claim-dag/1',**common,'claims':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims]})
    dump('closure.json',{'schema':'rh-human-component-closure/1',**common,'closed_subcontracts':endpoints,
      'independent_reviews':reviews,'pending_review_claims':sorted(expected-reviewed,key=lambda c:int(c[3:])),
      'exact_whole_closures':{},'new_global_frontier_leaf_closures':[],'proposed_global_frontier_leaf_closures':[],
      'full_c1ch_closed':True,'full_sharp2_closed':True,'full_PropagationTheoremGL2_closed':True,
      'full_EPres_remains_open':True,'full_sharp3_remains_open':True,'rank_three_triangular_and_seed_producers_remain_open':True,
      'full_PropagationTheoremGL3_remains_open':True,'actual_OffFin_producer_remains_open':True,
      'ModIn_automorphic_and_Alt_producers_remain_open':True,'full_GdEnd_remains_open':True,'full_HostEnd_remains_open':True,
      'original_P_retained':True,'separate_rank_rings_and_coefficient_extensions_preserved':True})
    dump('status.json',{'schema':'rh-bounded-producer-status/1',**common,'claim_count':len(claims),
         'completed_original_targets':endpoints,'whole_closures':{},'retained_boundaries':retained})
    dump('source_mapping.json',{'schema':'rh-source-to-human-mapping/1',**common,
         'mappings':[{'claim':c['id'],'scope':c['original_scope'],'source_ranges':[s['id'] for s in c['sources']]} for c in claims]})
    dump('next_consumer.json',{'schema':'rh-next-consumer/1',**common,
         'completed_return':{'claim':'ACC26','consumer':sources['abs_main'],'statement':'Exact rank-two AllGood at original Setup/ModIn transfers'},
         'next_mathematical_producers':retained,'already_completed_inputs':['APD25','RTC7','RTC19','ALC4','ALC11','ALC17','ALC21','ACP14','ACP15','ACP16','ACP17'],
         'whole_closures':{}})
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    report=f'''ARITHMETIC CONNECTEDNESS AND RANK-TWO PROPAGATION — v0.57

ACC1–ACC27 complete full original c1ch, sharp2 and PropagationTheoremGL2.
The latter retains exactly Ok/Big, FinLam, P1prime and the original weak
SeedIn inclusion. All local/global data are constructed on the actual
Space and canonical charts; no new opaque propagation assumption enters.

c1ch is proved for general complete Noetherian local prime-nilradical
rings, using precisely stated Grothendieck connectedness and the height
theorem. APD25 gives Chained(0,n*d+1) at both original ranks without Big
or nontriangularity, with the exact extra +1 retained.

The new rank-two strict fibre is explicitly a polynomial algebra in at
most C0 parameters, giving the stronger closed-fibre bound C0 and
triangular bound d+2*C0+2. Full finite-character detectors and separated
adic-limit arguments force all ordinary characters, not only traces.

Full loc_dim, fibre, dim_B and l52 are supplied in both ranks. The latter
has the stronger bound dim(R/P)+dv <= n*d+3, implying the original +6
and conditional +5 returns. All transcendence degrees precede completion.
Full general NicePrimeEx allows an arbitrary starting ideal, finite or
empty bad family, and a finite residue field. Its arithmetic application
and the strict bad-locus theorem are completed at rank two only.

Full min_hom, jac and l41 are supplied in both ranks. The rank-two weak
seed inclusion is transported by an actual Laurent localization, then
one maximal core x is fixed before every later Loc. The canonical flat
charts and inherited RTC19/ACP propagation return full rank-two AllGood.

RETAINED: separate rank-three EPres/Sharp, triangular and seed/corner
arguments, thick chains and GL3/OffFin; actual ModU/PfromAut/patching,
both ModIn packages and arithmetic seeds; original P, Host ell=3, same
marking, separate rank rings and ideals, and Alt WitA/WitAQ. Neither
completed local charts nor APD, OCH or UCE are reopened. No whole selected
obligation closes. No frozen file is changed; no Lean replay and no PDF.

Pin: {PIN}
Main SHA256: {mainsha}
Status: {status}
Claims: {len(claims)}; source files/ranges: {len(files)}/{len(sources)}
Inherited proof blocks: {len(human)}
'''
    (HERE/'report.txt').write_text(report)
    dump('hashes.json',{'component':HERE.name,'artifact_version':VERSION,
         'hashes':{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}})
    print(json.dumps({'component':HERE.name,'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),
                      'inherited_inputs':len(human),'main_sha256':mainsha,'status':status},indent=2))

if __name__=='__main__': main()
