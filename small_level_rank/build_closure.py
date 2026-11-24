from pathlib import Path
import json,hashlib
p=Path('/workspace/scratch/368c004c3aea/work_v031/small_level_rank')
prov=json.loads((p/'provenance.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
proofs={c['id']:c['proof_location'] for c in prov['claims']}
closure={
 'schema':'rh-human-closure/1','artifact_version':'0.31','component':'small_level_rank',
 'source_commit':prov['source_commit'],'proof_file':'small_level_rank/main.tex','proof_file_sha256':prov['main_tex_sha256'],
 'formal_proof_assumption':'The underlying Lean proof is fully checked and correct. All open statuses below concern human reconstruction.',
 'target':{'id':'GLOBAL_SMALL_RANK','literal':'Closed (D3 3 A) (fun Fm _ => SmallLevelRankEq Fm)','source':'S01/S27/S38','status':'conditional implication completely reconstructed; actual common producer remains open','unconditionally_closed':False},
 'closed':[
  {'id':'SLR_ACTUAL_PROJECTION','category':'B','status':'closed on every supplied literal Bundle','claims':['SLR1','SLR2','SLR3','SLR8'],'conclusion':'Actual lPrj is surjective, with lZ0 as a right inverse; H_zL uses epsilon1=1, K=0, xr=0.','additional_open_premises':[],'context':'Original Bundle and its existing C.ok1 fields are supplied; no period premise, FormsTie premise, or arithmetic largeness estimate is used.'},
  {'id':'SLR_TYPED_BASE_RANK','category':'B','status':'closed conditional theorem','claims':['SLR4','SLR5'],'conclusion':'RowsHold0_3 on the original P implies dW(k)=S0.D=D0 and dim_C Mj(k+1)=D0.','additional_open_premises':['SLR_SAME_BUNDLE_BASE_PRODUCER.rows'],'note':'Generalized primary spaces retained; no semisimplicity assumed; direct eRR0/jEE_basis/onb0 comparison replaces RowsHoldLam3.'},
  {'id':'SLR_THETA_ADJOINT_RANK','category':'B','status':'closed conditional theorem','claims':['SLR6','SLR7'],'conclusion':'The actual base-tuple theta square plus the preceding row data gives onto thetaP and dim_C Zj(mu0,j)=D0.','additional_open_premises':['SLR_SAME_BUNDLE_BASE_PRODUCER.rows','SLR_SAME_BUNDLE_BASE_PRODUCER.base_theta'],'note':'Only the original base tuple is used. Its Used0 proof is automatic; no TupAllUsed or whole DivRows3 upgrade.'},
  {'id':'CERT_SLR_FINITE_JOIN','category':'B','status':'closed conditional original-target implication','claims':['SLR1','SLR2','SLR3','SLR4','SLR5','SLR6','SLR7','SLR8','SLR9'],'conclusion':'Common selected base row/theta producer -> original Closed SmallLevelRankEq','additional_open_premises':['SLR_SAME_BUNDLE_BASE_PRODUCER'],'thresholds':{'epsilon1':1,'TransportedAlt_K':'all four components zero','projection_xr':0,'rank_x0':'max(a_Fm,Fm.x1+1)','a_Fm':'common eventual producer threshold, enlarged to the selector threshold','quantifier_note':'K is chosen before Fm,CH; a_Fm and x0 are existential only inside SmallLevelRankEq.'}}
 ],
 'remaining':[
  {'id':'SLR_SAME_BUNDLE_BASE_PRODUCER','category':'C','status':'open human reconstruction of actual arithmetic/analytic producer','contract':'For the original common compatible Bundle selector and each allowed Fm, there exists a_Fm such that every selected P at x>=a_Fm and x>Fm.x1 has RowsHold0_3 P and the same P base-tuple thTheta square (SLR.17), for all lift indices and rational coordinates. a_Fm also exceeds the original selection threshold.','bindings':['same A and original Fm','same coefficient field','same x and i','same literal selected Bundle.P','same Zs,S0,I','same base tuple t0=A3.A.mu0 with I.tup t0=original mu0','same lPrj/lZ0 at inverse lift character','same original thetaP,jMt,eMt,jW','one common threshold across i and lifts'],'joint_and_contract':True,'subclauses':[
   {'id':'rows','literal':'RowsHold0_3 P','category':'C','source_groups':['S15','S39'],'unreconstructed':'Produce the original stable/block-contained subspaces and base IndefRows on P.S0 with its bijective row and theta matrices, mapped type subspaces, matching type dimensions, and type separation. PrimRows3 -> actual IndefRows construction remains upstream.'},
   {'id':'base_theta','literal':'ThTheta restricted to t0=P.A3.A.mu0','category':'C','source_groups':['S19','S20','S21','S23','S30','S31','S32','S33','S34'],'unreconstructed':'Identify original thetaP on rational lift coordinates with the same jW, rational theta matrix and lPrj. SLR7 closes factorization from actual readings but does not produce the Hilbert-model/lowest-K-type and rational-adjoint readings.'}],
   'minimality_note':'A bounded sufficient cut, not a claim of absolute logical minimality. The square need only hold on E theta^{-1} of the coordinate basis; the all-coordinate base version is retained for a recognizable source contract.'}
 ],
 'context_inputs':[
  {'id':'ORIGINAL_COMMON_BUNDLE_SELECTION','status':'supplied context; construction remains outside this component','source_groups':['S24','S25','S29'],'not_created_here':True}
 ],
 'sufficient_rules':[
  {'conclusion':'SLR_ACTUAL_PROJECTION','requires':['ORIGINAL_COMMON_BUNDLE_SELECTION'],'certificate':['SLR1','SLR2','SLR8'],'complete_human_implication':True},
  {'conclusion':'GLOBAL_SMALL_RANK','requires':['ORIGINAL_COMMON_BUNDLE_SELECTION','SLR_SAME_BUNDLE_BASE_PRODUCER','CERT_SLR_FINITE_JOIN'],'gate':'AND','complete_human_implication':True,'same_witness_required':True}
 ],
 'shared_work_links':[
  {'from':'SLR_SAME_BUNDLE_BASE_PRODUCER','to':'GLOBAL_ACTUAL_ROW_SPECTRUM','relation':'shared actual row/realization work; not a sufficient logical edge'},
  {'from':'SLR_SAME_BUNDLE_BASE_PRODUCER','to':'GLOBAL_PERIOD_HEIGHT','relation':'shared original theta, rational image and period realization; not a sufficient logical edge'},
  {'from':'ORIGINAL_COMMON_BUNDLE_SELECTION','to':'actual_bundle_dictionary','relation':'same Bundle selection dictionary shared with LTD/second-layer work; existence not supplied by this link'}
 ],
 'stronger_source_routes':[
  {'inputs':['PrimAll sel (selIOf selB)','pointwise DivRows3G on same selP','original compatible selectors and C.ok1'], 'source_groups':['S20','S27','S39'],'scope':'Source supplies the common producer this way; human reconstruction of primitive-row construction/actual readings remains open. Do not mark this as an independently completed arithmetic producer.'}
 ],
 'not_needed_for_this_rank_implication':['RowsHoldLam3','TupAllUsed','theta square at nonbase tuples','full DivRows3 pairing/column identities','BkLaw','MIstar2','extra zL size threshold','surjectivity onto an independently prescribed integral lattice'],
 'not_claimed':['Unconditional RH or GRH','Existence of original family or Bundle','Unconditional GLOBAL_SMALL_RANK without same actual producer','Integral equality cutZ=Tl','A new ClassNumberFormula2 identity','Closure of the actual analytic lowest-K-type comparison'],
 'proof_hashes':proofs,
 'validation':{'source_ranges':81,'pinned_source_files':41,'all_exact_pinned_blobs':True,'latex_draft_compile_exit_code':0,'latex_undefined_commands':0,'latex_overfull_boxes':0,'latex_page_count':7,'latex_notes':'Draft compile with the inherited preamble and microtype expansion disabled in the test harness because this isolated TEXMF lacks pdftex.map. No main-text font override. No PDF visual claim.','peer_review':'Pending independent literature agent review; report path work_v031/reviews/small_level_rank_review.json','new_lean_compile':False}
}
(p/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
report=f'''SMALL-LEVEL RANK: v0.31 HUMAN RECONSTRUCTION

Source pin: {prov['source_commit']}
Main TeX SHA256: {prov['main_tex_sha256']}
Claims: SLR1--SLR9. Exact source audit: 81 ranges in 41 pinned files.

OUTCOME
The previously opaque level-projection issue is closed pointwise on the actual selected Bundle. lPrj has the explicit right inverse lZ0. No period-admissibility assumption, FormsTie assumption or new eventual arithmetic bound is required. H_zL has epsilon1=1, all-zero K and xr=0.

The complete finite implication to original SmallLevelRankEq is also proved. It retains the original coefficient spaces and matrices, inverse lift character, base tuple, original jMt/eMt/jW, original thetaP and its adjoint image. Generalized joint primary spaces are used; no accidental semisimplicity assumption is made. The proof gives dim_C Mj = dW = S0.D = D0 and, from the base theta square, surjectivity of thetaP and dim_C im(thetaP*)=D0.

The comparison S0.D=D0 is shorter than the original wrapper: eRR0 identifies K^S0.D with the original base rational row space; its given basis maps to a complex basis of original EE0; onb0 has D0 elements. Thus RowsHoldLam3 is unnecessary for this numerical comparison.

REMAINING ACTUAL PRODUCER
GLOBAL_SMALL_RANK is not marked unconditionally closed. The explicit sufficient remaining contract is eventual RowsHold0_3 together with the theta square at t0=A3.A.mu0, on one and the same selected P and one common threshold. The base tuple is automatically Used0. No full TupAllUsed upgrade is needed. Even the square can be restricted to the finite list lZ0*theta^(-1)(coordinate basis), though the recognizable all-coordinate base version is retained.

RowsHold0_3 is not a field of an arbitrary Bundle. Producing its actual IndefRows from PrimRows3 remains upstream. Likewise ThDef3 in P.tied contains li/span/lat but not thTheta. The actual theta comparison uses the Hilbert-model reading and lowest-K-type uniqueness, the rational adjoint-image/level statement, and the actual rational theta matrix. SLR7 proves the projection-factorization once those exact readings are supplied. It does not invoke a source theorem as a substitute for their human proof.

DEPENDENCY AUDIT CHANGE
Retire the separate D uncertainty about identifying/proving zL. Retire the finite B join from original base row/theta inputs to Closed SmallLevelRankEq. Replace the broad remaining D leaf by the precise C joint actual base-row/theta producer in closure.json. Shared links to actual row/spectral and period work are explicitly nonlogical; their mere existence does not prove either conjunct. Original Bundle/family construction remains supplied context. These statements apply equally to the RH and Dirichlet-GRH global branches; this is not a target-character specialization.

NORMALIZATION AND INTEGRAL BOUNDARY
The proof keeps H_L=|P|^(-1)L*HL and H_V=|P|^(-1)V*HV. It proves both Pi E=1 and Pi=(E*H_LE)^(-1)E*H_L. At lift level the character is psi0^(-1). The lattice identities are cut_E(level lattice)=cut_Z and delZ subset cutZ subset Tl, with Tl the image lattice. Surjectivity is over K; no unsupported equality cutZ=Tl or integral right inverse is asserted.

QUANTIFIERS
Given a common eventual threshold a_Fm for the two actual inputs and the selector, take x0=max(a_Fm,Fm.x1+1). This yields one threshold for every i and used lift j. Closed chooses epsilon1=1 and K=0 before the family and CH. The family-dependent x0 remains inside SmallLevelRankEq's existential quantifier, where the original definition allows it.

VALIDATION
All 81 source ranges were checked against the exact pinned git blobs. Nine proof blocks and the whole text have SHA256 certificates. Draft TeX compilation succeeded, seven pages, zero undefined commands and zero overfull boxes. The test harness disables microtype font expansion only to accommodate its missing font map. An independent peer review is being performed by the literature agent. No new Lean kernel build was needed or claimed; correctness of the underlying checked Lean development is the task premise.

FILES
main.tex, provenance.json, source_locators.txt, closure.json, this report.txt.
The reproducible metadata scripts and exact source inventory are also included in this work directory. No baseline files were modified.
'''
(p/'report.txt').write_text(report)
print(json.dumps({'main_sha256':prov['main_tex_sha256'],'closure_sha256':sha((p/'closure.json').read_bytes()),'report_sha256':sha((p/'report.txt').read_bytes())},indent=2))
