#!/usr/bin/env python3
"""Bind the readable determinant-window and actual-row proofs; no Lean replay."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
COMP = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
U = 'src/Development/AbelianVarietyTheory/Proofs/UnramifiedDepth/'
F = 'src/Formalism/LocalToGlobal/CharacterGerms/'
ap = argparse.ArgumentParser()
ap.add_argument('--source-root', type=Path, default=Path('/workspace/scratch/249d32c24541/formal_source'))
args = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

proof = (HERE/'main.tex').read_bytes()
base = dict(artifact_version='0.57', component=COMP, source_commit=PIN,
            proof_file_sha256=sha(proof), status='written_pending_independent_review')
rows = []
def src(key, file, lo, hi, declaration, prefix=U):
    rows.append((key, prefix+file, lo, hi, declaration))

src('series_defs','src/Formalism/IncomingBounds/StatementThmP.lean',8,39,
    'PVar, detL/detR, mfact, jetAt0, mvExp, expE, hP, LamP and degrees','')
src('slope_defs','src/Formalism/IncomingBounds/IncomingBound.lean',8,10,'rho and gam','')
src('hm_contracts','BiadditiveInSingleVariables.lean',10,53,
    'numerical identities, HM1/HM2, HSeparatedRowSum and bdP',F)
src('cayley_contract','src/Formalism/IncomingBounds/StatementThmP.lean',55,59,
    'CayleyId, the original ordinary determinant differential identity','')
src('thmp_contract','BiadditiveInSingleVariables.lean',106,114,
    'S0 and full FormalSeriesBounds.ThmP',F)
src('newton_contract','BiadditiveInSingleVariables.lean',116,136,
    'CoefficientExpansionLambda, NewtonBoundPositive and P7',F)
src('row_contracts','BiadditiveInSingleVariables.lean',179,224,
    'InRow, DiagCoord, BiHyp, BiF, BiValue, BiContent, BiWindow',F)
src('factorial_source','SumEqOfIsHomogeneous.lean',974,1027,
    'integer and factorial valuations over arbitrary normalized valued fields')
src('exp_shift','SumEqOfIsHomogeneous.lean',237,323,
    'finite ordinary differential conjugation by the mixed exponential')
src('exp_binomial','SumEqOfIsHomogeneous.lean',464,685,
    'Frobenius determinant error, coefficient divisibility and expBinomial')
src('coefficient_expansion','SumEqOfIsHomogeneous.lean',700,855,
    'integer expE, factorial comparison and CoefficientExpansionLambda')
src('thmp_producer','SumEqOfIsHomogeneous.lean',917,954,'WindowValuationBound.main')
src('thmp_export','SumEqOfIsHomogeneous.lean',961,962,'GlobalTheory.OddBlock.windowBound')
src('content_producer','SumEqOfIsHomogeneous.lean',1029,1056,'slope_nonneg and biContent')
src('window_join','SumEqOfIsHomogeneous.lean',1058,1075,'biWindow_of; biContent_and_biWindow')
src('content_window_export','SumEqOfIsHomogeneous.lean',1084,1085,
    'GlobalTheory.OddBlock.content_and_window')
src('threshold','NewtonBoundPosAndNewtonStep.lean',9,134,'full positivity and Newton interpolation producer')
src('block_contract','src/Formalism/DropLevelBounds/Statement.lean',49,89,
    'DetPowDiag, embV/restr/diagMon, BlockJet, RestrictMul and RestrictExp','')
src('restriction_producer','DetPowDiagonalRowsBlockJetRestrict.lean',11,37,
    'restrictMul and unrestricted restrictExp')
src('det_diag','DetPowDiagonalRowsBlockJetRestrict.lean',82,180,
    'det_diag_rows, kill_det_pow and full DetPowDiag')
src('blockjet_producer','DetPowDiagonalRowsBlockJetRestrict.lean',418,505,
    'full BlockJet and its joint export')
src('bivalue_support','BlockValueOnRowsEq.lean',12,121,
    'OnlyIn, multigraded leading coefficient calculus and sideRow')
src('bivalue_exp','BlockValueOnRowsEq.lean',124,255,
    'coefficientwise exponential and finite exponential-sum product')
src('bivalue_producer','BlockValueOnRowsEq.lean',477,596,'GlobalTheory.blockValue_rows')
src('bivalue_export','BlockValueOnRowsEqStatement.lean',6,7,'GlobalTheory.T.blockValue_on_rows_eq')
src('normal_form_contract','LatticeInclusionFormsInjective.lean',51,102,
    'actual linear pullbacks, weighted hypotheses, main term and MConcl',F)
src('mplus_contract','LatticeInclusionFormsInjective.lean',118,121,'MPlusConcl',F)
src('normal_form_existence_contract','LatticeInclusionFormsInjective.lean',123,149,
    'LemmaM, LemmaMLeaf and LemmaMPlus: retained original existence producers',F)
src('restricted_series_contract','LatticeInclusionFormsInjective.lean',151,165,
    'hGood, restrictedCurveSystemSeries and all four MtoHM fields',F)
src('restriction_and_rows','MainTermImpliesRowHypothesis.lean',14,141,
    'killCompl pullback, coefficient renaming and signed row main term')
src('mtohm_producer','MainTermImpliesRowHypothesis.lean',145,194,
    'GlobalTheory.mainTerm_to_rowHypothesis')
src('mtohm_export','MainTermImpliesRowHypothesisStatement.lean',6,7,
    'GlobalTheory.T.mainTerm_implies_rowHypothesis')
src('cartier_datum','GeNatCast.lean',9,13,'VF',F)
src('cartier_axioms','GeNatCast.lean',118,132,
    'Cart, typed curves and original t4 existence axiom',F)
src('curve_contract','ScaledSecondIntegral.lean',46,65,'IsCurve and standard initial vectors',F)
src('system_contract','Interface.lean',17,53,
    'IsSat, Sys, IsT and ze with actual coefficient convention',F)
src('actual_germ_value_contract','Interface.lean',59,100,
    'WV/upG, IntGerm, rowCopy, RowsOK and ValOf',F)
src('original_row_data','Interface.lean',103,173,
    'Full original RowData, including actual gauge, axis, pairing and compatibility fields',F)
src('row_integer_data','Interface.lean',177,184,'Alt and m=j+jprime',F)
src('sys_exists','CartesianBoundOnCurves.lean',275,281,'sysExists from Cart.t4',F)
src('formal_coordinate_contraction','CoeffIterateZero.lean',18,91,
    'degree contraction, stabilized formal coefficients and unique fixed point',F)
src('coordinate_equation','CoeffIterateZero.lean',188,231,
    'actual coefficient equation, isT_iff and tExistsUnique',F)
src('linear_substitution','ConstantCoeffSubstSame.lean',218,245,'jetAt0_subst_linear')
src('exponential_substitution','ConstantCoeffSubstSame.lean',247,267,'subst_mvExp')
src('integral_completion','ConstantCoeffSubstSame.lean',269,348,
    'complete_step and complete_rows for every intermediate size')
src('integral_inverse','BlockOfNormalForm.lean',18,55,'integral determinants and adjugate inverse')
src('diagonal_coordinate','BlockOfNormalForm.lean',107,133,
    'diagCoord_subst, including all degree-zero and degree-one coefficients')
src('standard_coordinates','BlockOfNormalForm.lean',135,160,'exists_std_coords')
src('actual_linear_rows','BlockOfNormalForm.lean',183,290,
    'rowForm, differential substitution, row support and exact block restriction')
src('determinant_change','BlockOfNormalForm.lean',292,313,'letterDet, det_change and valuation comparison')
src('block_from_normal_form','BlockOfNormalForm.lean',317,434,
    'full original block_of_normal_form with every supplied h1/restriction identity')
src('window_monotonicity','OddLevelBlockBoundAttained.lean',71,87,
    'S0 monotonicity and positivity')
src('actual_window','OddLevelBlockBoundAttained.lean',89,147,
    'window_letterDet, separating its retained normal-form production from the proved join')
src('flag_installs','OddLevelBlockBoundAttained.lean',155,177,
    'oddBlock_supply and its two original flags; conditional next application only')
src('literal_block_bound','ContentZeroAt.lean',11,16,'blockBd and Windows',F)
src('normal_form_producer_retained','RowDataMainTermNormalFormAndLevelOne.lean',98,206,
    'both and main: retained adapted-chain, weight and residue-rank producers')
src('normal_form_export_retained','RowDataMainTermNormalFormAndLevelOneStatement.lean',6,7,
    'GlobalTheory.T.rowData_mainTerm_normalForm_and_levelOne')

files, sources = {}, {}
for key, path, lo, hi, decl in rows:
    if path not in files:
        blob = subprocess.check_output(['git','-C',str(args.source_root),'show',PIN+':'+path])
        assert (args.source_root/path).read_bytes()==blob, path
        dest=HERE/'source_snapshot'/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(blob)
        files[path]=dict(path=path,snapshot_file=str(dest.relative_to(WORK)),bytes=len(blob),
            line_count=len(blob.splitlines()),sha256=sha(blob),file_sha256=sha(blob),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,url=REPO+'/blob/'+PIN+'/'+path)
    f=files[path]
    ls=(WORK/f['snapshot_file']).read_bytes().splitlines(keepends=True)
    assert 1<=lo<=hi<=len(ls),(key,lo,hi,len(ls))
    part=b''.join(ls[lo-1:hi])
    sources[key]=dict(id='DJW_SRC_'+key.upper(),path=path,declaration=decl,line_start=lo,line_end=hi,
        source_commit=PIN,file_sha256=f['sha256'],full_file_sha256=f['sha256'],range_sha256=sha(part),
        range_bytes=len(part),snapshot_file=f['snapshot_file'],verified_equal_to_pinned_git_blob=True,
        url=f['url']+f'#L{lo}-L{hi}')

specs=[
('DJW1',[],['factorial_source','exp_binomial'],'Integer and factorial valuations.',
 'All normalized valued characteristic-zero fields; multiindex zero and factorial zero included.'),
('DJW2',[],['cayley_contract','coefficient_expansion'],'Cayley factorial and its exact adjoint quotient.',
 'Uses the explicitly cited classical ordinary Cayley identity; no analytic or geometric premise.'),
('DJW3',['DJW1'],['hm_contracts','exp_binomial'],'Weighted exponential and divisibility of the Frobenius error.',
 'Every perturbation coefficient, finite degreewise exponential sums, and every Z-degree k.'),
('DJW4',['DJW2','DJW3'],['exp_shift','coefficient_expansion'],'Exact finite Newton expansion with a0=1.',
 'Ordinary derivative normalization, exact negative scalar c, no convergence in K.'),
('DJW5',['DJW1','DJW3','DJW4'],['exp_binomial','newton_contract'],'Explicit bound on every late Newton coefficient.',
 'Both factorial losses and the exact weighted identity are retained; zero coefficients allowed.'),
('DJW6',[],['newton_contract','threshold'],'Positivity at the exact ceiling threshold.',
 'Explicit 64r^2(h+3+3log_p(r+1)); p>=5, h>=1, r>=1.'),
('DJW7',[],['newton_contract','threshold'],'Unimodular binomial interpolation on every translated window.',
 'Original P7 for every valued field, no characteristic-zero or normalized-prime premise.'),
('DJW8',['DJW1','DJW4','DJW5','DJW6','DJW7'],['thmp_contract','thmp_producer','thmp_export'],
 'Full original FormalSeriesBounds.ThmP.',
 'Every original valuation/field, all y/windows, r<=n and the separate r=0 conclusion.'),
('DJW9',[],['series_defs','restriction_producer','bivalue_exp','exponential_substitution'],
 'Restriction and formal-exponential calculus.',
 'The truncated source mvExp commutes with restriction for arbitrary constant term; addition/exponential substitution are used at zero constant term.'),
('DJW10',[],['block_contract','det_diag'],'Determinant coefficients with fixed diagonal rows.',
 'Full DetPowDiag over any commutative ring, including empty blocks and zero powers.'),
('DJW11',['DJW10'],['block_contract','blockjet_producer'],'Full original BlockJet.',
 'Every L,y,n,r with r<=n and exactly the original separate-row coefficient hypotheses.'),
('DJW12',['DJW9','DJW11'],['row_contracts','bivalue_support','bivalue_producer','bivalue_export'],
 'Full literal BiValue.',
 'Arbitrary nonnegative l,i,n,r,y; no prime, valuation, oddness, HM1/HM2 or extra separated-row condition.'),
('DJW13',['DJW1'],['row_contracts','content_producer'],'Full original BiContent.',
 'Every supplied scalar with its stated bound, exact factorial and deficit cost.'),
('DJW14',['DJW8','DJW12','DJW13'],['row_contracts','window_join','content_window_export'],
 'BiWindow and full content_and_window.',
 'Exact original n-r<=(h+1)m, same U, same BiHyp, and exact interval length.'),
('DJW15',['DJW9'],['normal_form_contract','mplus_contract','restricted_series_contract','restriction_and_rows','mtohm_producer','mtohm_export'],
 'All four original MtoHM conclusions on the same actual restricted gauge.',
 'Original supplied MConcl; every nonnegative h; includes optional h=1 MPlusConcl to HSeparatedRowSum.'),
('DJW16',[],['integral_completion'],'Full integral completion of split rows.',
 'Every intermediate r<=j<=n over the original valued field; no discrete valuation or completeness.'),
('DJW17',[],['cartier_axioms','curve_contract','system_contract','sys_exists','formal_coordinate_contraction','coordinate_equation','standard_coordinates'],
 'Actual standard Cartier systems and their formal coordinates.',
 'Uses the original Cart.t4 field of supplied RowData; no new formal-group existence assumption.'),
('DJW18',[],['linear_substitution'],'Ordinary differential pairing under actual linear substitution.',
 'Finite variable sets and all polynomials/series; transpose and determinant scalar are explicit.'),
('DJW19',['DJW15','DJW16','DJW17'],['normal_form_contract','original_row_data','diagonal_coordinate','actual_linear_rows','block_from_normal_form'],
 'Actual row substitutions and all BiHyp fields.',
 'Original MConcl and injective selected letters; all systems, matrices and coordinates fixed before y.'),
('DJW20',['DJW9','DJW16','DJW18','DJW19'],['actual_germ_value_contract','determinant_change','block_from_normal_form'],
 'Full block_of_normal_form with actual integral germs and exact unit scalar.',
 'Every supplied h1 with the original restriction identity; original MConcl retained; both sides are evaluated on the same selected letters and gauge.'),
('DJW21',['DJW8','DJW12','DJW13','DJW14','DJW15','DJW19','DJW20'],
 ['row_integer_data','window_monotonicity','actual_window','literal_block_bound'],
 'Exact actual-row window from the original supplied normal form.',
 'Normal form fixed first; then fixed S,t; every origin has y and integral germs; zero is explicitly admissible. Does not prove LemmaM existence.')
]
ls=proof.splitlines(keepends=True)
claims=[]
for ident,deps,groups,title,scope in specs:
    lo=next(i for i,l in enumerate(ls) if l.strip()==('% BEGIN '+ident).encode())
    hi=next(i for i,l in enumerate(ls) if l.strip()==('% END '+ident).encode())
    block=b''.join(ls[lo:hi+1])
    claims.append(dict(id=ident,title=title,introduced_in='0.57',classification='B',depends_on=deps,
        external_input_ids=['DJW_CAYLEY'] if ident=='DJW2' else [],scope_note=scope,
        source_groups=groups,sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+'/main.tex',label='claim:'+ident,line_start=lo+1,line_end=hi+1,
            sha256=sha(block),bytes=len(block)),
        proof_status='complete at the stated original mathematical hypotheses',
        status='complete human proof; pending independent review',
        scope_class='complete_at_stated_original_hypotheses',source_proof_is_not_human_proof=True))

cayley=dict(id='DJW_CAYLEY',kind='explicit_published_classical_theorem',
    name='Ordinary Cayley identity',
    authors=['Sergio Caracciolo','Alan D. Sokal','Andrea Sportiello'],
    title='Algebraic/combinatorial proofs of Cayley-type identities for derivatives of determinants and pfaffians',
    journal='Advances in Applied Mathematics 50 (2013), 474–594',
    theorem='Theorem 2.1, ordinary one-matrix identity; arXiv version 2, page 7',
    url='https://arxiv.org/pdf/1105.6270',
    exact_used_statement='det(partial_X) det(X)^m = product_{j=0}^{r-1}(m+j) det(X)^{m-1} for r,m>=1 over Q, hence any characteristic-zero field.',
    scope_note='No p-adic, geometric, metric, global family or RH premise; retained as a published classical input, not claimed newly proved.')
retained=[dict(id='DJW_ORIGINAL_ROW_DATA',name='The supplied original RowData',kind='original_input_data',
    sources=[sources['original_row_data'],sources['actual_germ_value_contract']],
    scope_note='Keep the actual gauges, Cartier data, valuation, types, pairings and original integral-germ interpretation. This packet does not construct a common geometric family.',globally_discharged_by_this_component=False),
 dict(id='DJW_MCONCL_INPUT',name='The literal supplied normal form MConcl',kind='original_mathematical_premise',
    sources=[sources['normal_form_contract']],
    scope_note='MtoHM and block_of_normal_form retain every original MConcl field. The same normal form determines U, row substitutions and actual germ tests before any y.',globally_discharged_by_this_component=False),
 dict(id='DJW_NORMAL_FORM_EXISTENCE',name='RowData.LemmaM (and its separate level-one refinement)',kind='remaining_original_producer',
    sources=[sources['normal_form_existence_contract'],sources['normal_form_producer_retained'],sources['normal_form_export_retained']],
    scope_note='Adapted Cartier chains, weighted gauge estimates, first-axis vanishing and residue rank estimates construct the normal form. Not supplied by this packet or assumed from the candidate reader.',globally_discharged_by_this_component=False)]

endpoint_rows=[
 ('DJW7','newton_contract','Full original P7, at every valued field.'),
 ('DJW8','thmp_contract','Full original FormalSeriesBounds.ThmP, both nonzero- and zero-size conclusions.'),
 ('DJW8','thmp_export','Original OddBlock.windowBound.'),
 ('DJW9','restriction_producer','Original RestrictMul and unrestricted RestrictExp.'),
 ('DJW10','det_diag','Original DetPowDiag over arbitrary commutative coefficient rings.'),
 ('DJW11','blockjet_producer','Full original BlockJet.'),
 ('DJW12','bivalue_export','Full original GlobalTheory.T.blockValue_on_rows_eq / BiValue.'),
 ('DJW13','content_producer','Full original BiContent.'),
 ('DJW14','content_window_export','Full original content_and_window, with BiWindow at every original hypothesis.'),
 ('DJW15','mtohm_export','Full original MtoHM, including the optional level-one separated-row conjunct.'),
 ('DJW16','integral_completion','Original complete_rows for every intermediate size.'),
 ('DJW17','standard_coordinates','Actual standard Cartier systems and coordinates used by the original row constructor.'),
 ('DJW20','block_from_normal_form','Full original block_of_normal_form, for every h1 with its prescribed restriction identity.'),
 ('DJW21','actual_window','Actual Windows conclusion conditional on the original supplied MConcl; normal-form existence remains unsupplied.')]
endpoints=[dict(claim_id=c,source=sources[k],output=out,
    status=('complete_original_conditional_conclusion' if c=='DJW21' else 'complete_at_original_hypotheses'))
    for c,k,out in endpoint_rows]

scope=dict(full_original_ThmP_supplied=True,full_original_BiValue_supplied=True,
 full_original_BiContent_supplied=True,full_original_BiWindow_supplied=True,
 full_original_content_and_window_supplied=True,full_original_MtoHM_supplied=True,
 full_original_block_of_normal_form_supplied=True,actual_integral_germs_constructed=True,
 actual_unit_scalar_identity_proved=True,
 actual_row_window_from_original_MConcl_supplied=True,
 original_LemmaM_existence_supplied=False,unconditional_BiSupply_supplied=False,
 global_Moduli_or_theta_family_supplied=False,global_section_laws_supplied=False,
 selected_whole_obligations_closed=[],GLOBAL_LOCAL_GAIN_reopened=False)
guards=[
 'The target is Formalism.L2.FormalSeriesBounds.ThmP; the distinct broader IncomingBounds.ThmP is not silently substituted.',
 'ThmP retains every original HM1/HM2 coefficient condition; no completeness, discreteness or unramified-field assumption is added.',
 'BiValue has arbitrary natural l and i, no valuation and no primality/oddness assumptions; it uses exact BiHyp and ordinary derivatives.',
 'The zero-size case is a separate equality; no zero-length window is claimed.',
 'The truncated mvExp restriction law is unrestricted in the constant coefficient; ordinary exponential product/substitution are used at zero constant term.',
 'MtoHM is proved from every original MConcl, not only selected-coordinate ones; its level-one fourth field is retained.',
 'The block constructor takes every original h1 satisfying the exact restriction identity; only the final estimated application uses canonical restrictedCurveSystemSeries.',
 'Integral germs are integral series in the original t coordinates, not necessarily coefficientwise integral in the logarithmic variables.',
 'All normal-form matrices, systems and coordinates are fixed before the order y and window origin; the germs are allowed to depend on y.',
 'Both determinant factors are tracked with the correct transpose; our constructed factors are units, yielding equality of valuations and the original weaker comparison.',
 'The entire original normal-form existence producer is retained. No whole obligation or global theta normalization is inferred from this local packet.'
]

comparison=WORK.parent/'post_proof_literature_20261124/determinant_jet_window_alternative.tex'
adaptation=dict(kind='reviewed_comparison_argument_expanded_and_installed',
    source_file=str(comparison),sha256=sha(comparison.read_bytes()),
    role='Attribution and proof-organization input for DJW1–8; all details appear in the present manuscript.',
    external_repository='https://github.com/adjoint-functor/theta-periods-to-rh-reader',
    external_commit='94107d5f1a355a4ae0bd521123dba9ffd62e00f5',
    external_path='tex/arithmetic.tex',external_line_start=6432,external_line_end=6528)

write('provenance.json',dict(schema='rh-proof-provenance/1',**base,source_repository=REPO,
 claims=claims,new_claim_count=len(claims),original_endpoints=endpoints,adaptation=adaptation,independent_reviews=[]))
write('source_manifest.json',dict(schema='rh-source-manifest/1',**base,repository=REPO,
 snapshot_root=COMP+'/source_snapshot',files=list(files.values()),ranges=list(sources.values()),
 file_count=len(files),range_count=len(sources),total_bytes=sum(f['bytes'] for f in files.values()),
 all_files_verified_equal_to_pinned_git_blobs=True,published_inputs=[cayley]))
write('contracts.json',dict(schema='rh-component-contracts/1',**base,**scope,
 claim_ids=[c['id'] for c in claims],completed_original_suppliers=endpoints,
 quantifier_guards=guards,inherited_inputs=[],external_inputs=[cayley],
 remaining_global_producers=retained,independent_reviews=[]))
write('inherited_inputs.json',dict(schema='rh-inherited-inputs/1',**base,inputs=[],
 scope_note='No earlier numbered human theorem is needed by the self-contained DJW packet; Cayley is explicitly recorded separately.',adaptation=adaptation))
write('retained_foundations.json',dict(schema='rh-retained-foundations/1',**base,
 inputs=[cayley],remaining_global_producers=retained))
write('explicit_inputs.json',dict(schema='rh-explicit-inputs/1',**base,inputs=[cayley],
 inherited_human_proofs=[],original_pointwise_interfaces=endpoints,remaining_global_producers=retained))
write('closure.json',dict(schema='rh-component-closure/1',**base,**scope,new_claim_count=len(claims),
 completed=[x['output'] for x in endpoints],pending_actual_geometric_producers=[x['id'] for x in retained],
 selected_obligation_statuses_unchanged=True,earlier_proof_components_modified=[],
 graph_nodes_added=0,graph_edges_added=0,independent_reviews=[]))
write('hashes.json',dict(schema='rh-component-hashes/1',**base,
 proof_blocks={c['id']:c['proof_location']['sha256'] for c in claims},
 primary_source_files={f['path']:f['sha256'] for f in files.values()},inherited_proof_blocks={}))
write('status.json',dict(schema='rh-component-status/1',**base,**scope,new_claim_count=len(claims),
 formal_proof_correctness_accepted=True,lean_replay_performed=False,
 proof_style='Detailed ordinary mathematics, with all actual row substitutions and scalar factors.'))
write('source_mapping.json',dict(schema='rh-source-mapping/1',**base,original_endpoints=endpoints,
 claims=[dict(id=c['id'],sources=c['sources'],scope_note=c['scope_note']) for c in claims]))
write('proof_bindings.json',dict(schema='rh-proof-bindings/1',**base,
 blocks={c['id']:c['proof_location'] for c in claims}))
print(json.dumps(dict(component=COMP,proof_sha256=sha(proof),claims=len(claims),
 primary_files=len(files),source_ranges=len(sources),inherited_bindings=0),indent=2))
