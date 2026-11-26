#!/usr/bin/env python3
"""Record the exact v0.14 scope used by assembly and preservation scripts."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_13'
def read(p):return json.loads(p.read_text())
components=['adelic_geometry','decorated_realization','global_forms','chart_values','neighbor_geometry','value_existence','canonical_refill']
ledgers={name:read(ROOT/name/'provenance.json')for name in components}
claim_ids={name:[c['id']for c in d['claims']]for name,d in ledgers.items()}
assert claim_ids['value_existence'][-1]=='VE11'
assert claim_ids['decorated_realization'][-1]=='DR3'
assert claim_ids['canonical_refill'][-1]=='RF16'
assert claim_ids['global_forms'][-1]=='FC19'
assert claim_ids['neighbor_geometry'][-1]=='NB8'
prior=read(OLD/'next_source_targets.json')
old_cp=read(OLD/'continuation_checkpoint.json')

scope=('Partial human reconstruction of RH and Dirichlet GRH. The actual chart values, '
       'neighbor naturality and direct Forms0/level-zero carrier construction now give '
       'the concrete integral comparison for supplied true-column Ok/Pins/Laws/Later '
       'data. The initial decorated-point realization is now constructed from the '
       'literal unramified CM and valid-decoration hypotheses, including at dyadic '
       'places. The diagonal base point, supported splice and exact frame modification are proved. Canonical '
       'refill and the conditional point installation are proved; all ParamsT fields '
       'and seven of twenty-one ParameterChoice families are proved. Actual arithmetic '
       'host and column-law supply, terminal/symmetric-column data, fourteen parameter families, '
       'SizesAt, host/point existence and the independent global branches remain. '
       'No complete self-contained RH/GRH proof or Lean kernel replay is asserted.')
new=[
    'AD1-AD4: explicit integral unitary diagonal base point with the exact last-row residue; transition integrality and residue cancellation; supported conjugate-pair splice checking every IsPtOf field; global-lattice recovery and exact rational-frame modification.',
    'DR1-DR3: derive split/unramified local algebras from literal cmUnram, lift every unit norm including in residue characteristic two, construct local orthonormal bases and an actual unitary finite-adelic realizer, and install every type/auxiliary residue and rational frame. All five IsPtOf fields and the actual adelic Col.UnimodGenus are supplied.',
    'FC1-FC19: actual finite charts, residue-functional normalization preserving all carriers, quotient projections, Fock norm and period identities, common GLoc characters, reduction levels, specified level-zero level, coefficient-field rationality, BwTie, dilation and a direct Forms0 construction. DR3 supplies its initially conditional geometric realization.',
    'CV1-CV10: actual complex member-space equality, rational preimages and exact all-prime integral chart criterion; terminal-row value clauses under its supplied row chart. Integral Weyl lattices and determinant shifts are retained.',
    'NB1-NB8: paired-prime Hermitian duality, the actual up/down decorated lattices and functional extensions, raw/preferred coupling-label preservation, exact moving matrices/projections, and both full naturality statements via AD3.',
    'VE1-VE11: explicit even/odd coefficient-field block polynomials; universal presentation-independent ValEx; evaluation injectivity and the unique semilinear comparison; all comparison hypotheses and the actual true-column concrete comparison with Ce=1 and exact integral image span. DR3 discharges the independent initial-realizer premise.',
    'RF1-RF16: complete canonical refill and conditional LedPart/point lattice-height installation; exact uniform rank/scale/thin/gap/band/prime inequalities; every ParamsT field; exponential word count <=2^(k-3). Seven parameter families are complete; fourteen and SizesAt remain.',
]
remaining=[
    'Supply the actual arithmetic host, literal CM data and true-column Ok/Pins/Laws/Later from their upstream arithmetic construction. DR3 now proves initial decorated-point realization under those data, and VE11 proves the concrete integral comparison. Neither initial realizability nor the stronger rational-semilocal genus route is an additional comparison premise.',
    'Complete the particular symmetric penultimate HSym/lamSym identification, terminal full/row levels and ReadsP, til_ties vector/incidence/evaluation geometry and the exact terminal CarT joins. The common penultimate subgroup/orbit carrier, scalar residue identity and conditional terminal values/norms are already reconstructed. These terminal tasks are not additional premises of the direct level-zero comparison.',
    'Supply actual Lay/RecOK/LedOK and RecExP geometry and its mass/window estimates, the HC/level/initial-size existence constructors, all fourteen remaining ParameterChoice families and the complete SizesAt package for the same D,L. Canonical refill, exact lattice patch, ParamsT and the band/lambda/prime/word-count estimates are already proved. The global uniform threshold and degree-pair order must be preserved.',
]+old_cp['remaining_major_inputs'][2:]

completed_reasons={
    'hermColsCh_of_forms':'FC9 proves the complete Hermitian carrier conversion under the supplied standard-form data and exact level descriptions; FC14 supplies the chart reduction levels. Remaining terminal CarT is separately targeted.',
    'val_tied':'CV9 proves the actual all-prime complex/rational/integral valuation-compatible chart from its stated compatible chart inputs.',
    'ex_C_blk':'VE1-VE6 prove the block-rationality and universal polynomial-value existence implication; FC19 now supplies the level-zero record under explicit true-column/realizability inputs.',
    "valEx_of_rep'":'VE3-VE6 expand the rational action, point-character kernel and universal adelic extension argument; no separate ValEx premise remains in VE9/VE10.',
    'exists_refill':'RF1-RF5 prove the complete canonical refill, including common finite numerical support and exact parameter preservation.',
    'exists_ledPart':'RF5-RF8 prove the literal supplied-geometric-data LedPart implication and actual point lattice/height installation; the geometric supplier remains separately targeted.',
    'ObjCP':'This definition was refined into its actual construction suppliers by RF10. The existence of ObjCP is not inferred from its record type.',
    'objCP_and_of_recExP':'RF9-RF10 expand the uniform join and isolate chGood_of_host, exists_levCh_of_levelPrime and exists_sizeData_over. Those substantive supplier proofs are the current targets.',
    'exists_isPtOf_cm':'DR1-DR3 construct the actual unitary finite-adelic point with all five IsPtOf fields from the literal unramified CM and valid-decoration data, including dyadic places. VE11 discharges this supplier in the actual comparison.',
    'unimodGenus':'DR2 proves the actual adelic Col.UnimodGenus assertion by an explicit restricted-product unitary matrix. The stronger rational-semilocal predicates are bypassed, not asserted.',
}
all_target_candidates=list(prior['targets'])
for component in components:
    p=ROOT/component/'next_targets.json'
    if p.is_file():
        d=read(p)
        all_target_candidates.extend(d if isinstance(d,list)else d['targets'])
replaced={t['path']+':'+t['declaration'].split('.')[-1]:completed_reasons[t['declaration'].split('.')[-1]]for t in all_target_candidates if t['declaration'].split('.')[-1]in completed_reasons}
scope_by_decl={
    'formsTiedSym_std':'FC19 constructs Forms0 directly using CV, NB and AD; DR3 supplies initial realization and VE11 gives the concrete level-zero comparison under true-column arithmetic inputs. The full FormsTiedSym conclusion still needs the specified penultimate HSym/lamSym identification, terminal row/full levels and til_ties incidence/evaluation geometry.',
    'colsTiedSym_std':'FC9 supplies Hermitian carriers and NB supplies actual up/down naturality. Complete the full terminal CarT and same-object symmetric/terminal joins for ColsTiedSym; do not reopen the direct Forms0 concrete comparison.',
    'explicitConstants_parameterConditions_large':'RF12-RF16 prove seven of twenty-one families: rank-k, other rank bounds, top/band/bottom, thin sizes, signature gaps, type-prime scales and word-cardinality upper bound. Fourteen specific remaining families are listed individually; prove their actual inequalities before assembling ParameterChoice.',
    'szRow_numAt':'Full ParamsT is RF15, the full band/lambda/prime/ChTT/ChCode supplier is RF14, and word-count upper bound is RF16. The NumAt join is now conditional on a complete compatible ParameterChoice and SizesAt for the same D,L.',
}
scope_updates={}
for t in prior['targets']:
    name=t['declaration'].split('.')[-1]
    if name in scope_by_decl:scope_updates[t['path']+':'+name]=scope_by_decl[name]
updates={}
for cid in ['CS4','CS5','CS6','CS7','CS8','CS9']:
    updates[cid]={'discharged_by':['VE6','VE7','VE8','VE9','VE10','VE11','FC19','DR3'],
        'scope':'The earlier conditional proof and every original field/source remain unchanged. VE proves ValEx; FC19 supplies direct Forms0/level-zero joins and DR3 proves initial decorated realization from the supplied true-column/CM data. VE11 combines these. The upstream arithmetic host and Ok/Pins/Laws/Later, and separate metric/window theorems, remain explicit.'}
for cid in ['SF1','SF2','SF3','SF7','CR6']:
    updates[cid]={'discharged_by':['FC16','FC19','NB7','NB8','VE11','DR3'],
        'scope':'The direct level-zero construction supplies the stated form/carrier/character/companion joins for the actual true-column setting, conditional on its supplied arithmetic host and Ok/Pins/Laws/Later. DR3 discharges initial realization. Full terminal FormsTiedSym/ColsTiedSym is not required for this comparison.'}
for cid in ['AD3','FC3','FC19','NB4','NB6','NB7','NB8','VE10']:
    updates[cid]={'discharged_by':['DR3','VE11'],
        'scope':'The conditional component proof is preserved. DR3 proves its initial decorated-point realization premise from the literal CM and valid-decoration data; VE11 applies that supplier to the actual comparison. No stronger rational-semilocal genus assertion is used.'}
for cid in ['LP4','LP5']:
    updates[cid]={'discharged_by':['RF5','RF7','RF8'],
        'scope':'Canonical refill and literal conditional LedPart/point installation are now expanded. The original local geometry, actual Mram, type-prime exception and normalized length convention are retained; no global saturation or containment is substituted.'}
conclusions={
    'adelic_geometry':new[0],
    'decorated_realization':new[1],
    'forms_and_carriers':new[2],
    'chart_values':new[3],
    'neighbors':new[4],
    'concrete_comparison':new[5],
    'refill_and_numerics':new[6],
    'remaining':'Actual host/CM and true-column arithmetic supply; specific terminal/symmetric-column constructions; fourteen ParameterChoice families and SizesAt; actual point construction and the four unchanged independent global branches.',
}
precision=[
    'Original v0.13 claim fields, source arrays, source-file metadata and dependency adjacency lists remain unchanged; version-0.14 links are additive. Earlier component boundaries describe their historical versions.',
    'FC19 constructs only the direct Forms0 and level-zero carrier records needed by VE10; it does not silently invoke the unfinished full FormsTiedSym/ColsTiedSym constructor.',
    'AD1 constructs the exact diagonal base point; AD3 provides supported splicing given an initial realizer; DR3 now supplies those realizers. AD4 proves global-lattice recovery and exact frame correction using single-completion density and finite CRT; no rational strong-approximation statement is inferred.',
    'DR uses literal CMData.cmUnram, not merely its name, to obtain the completed split/unramified algebra. Unit norm lifting uses the surjective residue trace and no division by 2. DR2 proves adelic Col.UnimodGenus; stronger rational-semilocal genus predicates are bypassed, not claimed. Primitive arithmetic/CM/column-law existence is retained.',
    'Hermitian dual localization exchanges P and conjugate(P). The actual up/down lattices are globally self-dual but need not be globally comparable with the old lattice. All projections and moving matrices are the literal ones.',
    'The chart functional replacement preserves the same lattice, all groups, character, representatives and stabilizers. Only cmMax-valued chosen basis pairings are commuted through arbitrary embeddings in the Fock/Gram proof.',
    'All original coefficient embeddings, determinant shifts, odd-position reversal signs and valuation normalizations are retained. Integral Delta and dual-Weyl nabla are not identified by a rank argument.',
    'VE uses the independent CS2 duality to prove ValEx before invoking later comparison-span results; the merged mathematical dependency graph must remain acyclic. The graph is not a transitive Lean audit.',
    'The discarded-prime set can be infinite although the numerical gain/forcing/error/deficit fields have common finite support. RF preserves the supplied scale, selected degrees, actual Mram and ramification-normalized lengths.',
    'RF numerical thresholds follow the exact SzRow quantifier order. Decimals such as 371.768 are exact rationals; no floating-point numerical experiment replaces an eventual inequality. Seven parameter families are proved, fourteen and complete SizesAt remain.',
    'The current deliverables are the complete TeX and updated ZIP. Any TeX draft-mode check is not a PDF render or a visual layout review. The 150-page v0.13 PDF is historical and does not contain v0.14.',
]

cfg={
    'components':components,'tex_component_order':components,'date':'2026-11-21','scope':scope,
    'claim_updates':updates,'local_conclusions':conclusions,
    'new_in_this_version':new,'remaining_major_inputs':remaining,
    'completed_previous_frontier':'The initial decorated-point realization, all-prime chart-value theorem, universal ValEx, direct Forms0 and level-zero carrier/character/companion joins, actual up/down naturality, canonical refill, conditional point installation, all ParamsT fields and seven numerical families are reconstructed under their explicit arithmetic and column-law premises.',
    'next_local_priority':'Supply actual true-column laws and complete the symmetric/terminal geometry; fourteen parameter families and SizesAt; upstream arithmetic host/CM and point existence.',
    'priority_groups':{'1':'Actual true-column laws and remaining symmetric/terminal column geometry','2':'Actual arithmetic point suppliers, fourteen ParameterChoice families and full SizesAt','3':'Underlying host, field, different-ideal and analytic arithmetic supply','4':'Unchanged independent spectral, metric, cohomological and prime-window branches'},
    'precision_notes':precision,'replaced_target_keys':replaced,'target_scope_updates':scope_updates,
    'next_steps':[
        'Continue with the actual true-column law suppliers and exact terminal/symmetric joins. Reuse DR3 for all initial realizers, AD4 for exact frames, NB for naturality and FC19/VE11 for the completed level-zero comparison.',
        'Reconstruct the fourteen remaining ParameterChoice families and all SizesAt clauses for the same D,L. RF14-RF16 and full ParamsT should be reused rather than re-proved.',
        'Complete the terminal/symmetric HSym/lamSym, row levels, til_ties and CarT joins, then continue the host/field/analytic suppliers and four unchanged independent global branches.',
    ],
    'precision_supersessions':[
        {'previous_version':'0.13','historical_statement':'ValEx and the simultaneous global form/carrier record are retained comparison inputs.','current_statement':'VE proves ValEx; FC19 directly constructs Forms0 and exact level-zero joins, and DR3 supplies decorated realization from the actual CM data. VE11 yields the comparison under supplied arithmetic host/column-law data. Full terminal FormsTiedSym/ColsTiedSym remains separate.','completed_by':['FC19','CV9','NB7','NB8','DR3','VE11']},
        {'previous_version':'0.13','historical_statement':'Canonical refill and full point/NumAt remain after the conditional lattice patch.','current_statement':'RF supplies canonical refill, literal conditional LedPart/point installation, full ParamsT and seven numerical families. Actual geometry, fourteen ParameterChoice families and complete SizesAt remain.','completed_by':['RF5','RF7','RF8','RF14','RF15','RF16']},
    ],
    'tex_front_summary':r'''\textbf{What version 0.14 achieves.} The actual chart values, up/down naturality and direct level-zero forms now give the concrete integral comparison from the supplied true-column arithmetic. The initial decorated-point realization is constructed from the literal unramified CM hypotheses, including at dyadic places, with every residue and frame condition. The diagonal adelic base point, supported splice, exact rational-frame modification, residue and Fock identities are explicit. Canonical refill and the conditional point installation are proved, as are every block-length parameter and seven of twenty-one numerical parameter families. Actual host and column-law existence, terminal/symmetric-column data, fourteen parameter families, the remaining sizes and the independent global branches are still identified precisely. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.''',
    'tex_remaining_local':r'''LI/SF/CR/CS prove the exact local identifications, common frame,
class rank and integral comparison span. VE now constructs the universal
polynomial values, with their determinant factors and odd-position signs,
so \texttt{ValEx} is no longer an additional comparison premise.
CV proves the actual complex, rational and integral chart criteria.
AD constructs the diagonal base point, supported splice and exact rational
frames. NB identifies the actual up/down lattices and proves both naturality
statements. FC19 constructs \texttt{Forms0} directly and supplies the
same \texttt{StdTied}, \texttt{Joint0}, rational character and companion
data. DR1--DR3 prove the initial decorated-point realization using local
unramified Hermitian algebra, actual finite adelic assembly and exact
residue/frame modification. VE11 therefore gives the actual concrete
comparison from the supplied arithmetic host and true-column
\texttt{Ok/Pins/Laws/Later}. The construction of those arithmetic
data and the specified terminal/symmetric geometry remain explicit.

RF constructs the canonical refill, completes the literal conditional
\texttt{LedPart} argument through LP, and installs the point's actual
lattice and height fields. It proves every \texttt{ParamsT} field,
the full band/lambda/prime supplier, and seven of the twenty-one
parameter families, including the exponential upper word count.
Fourteen parameter families and the complete \texttt{SizesAt} package
remain. The geometric \texttt{Lay/RecOK/LedOK/RecExP} and the actual
HC, level and initial-size suppliers remain distinct from those numerical
estimates. GW/HW already choose one degree pair and realize its positions;
the optional status of \texttt{CoverAll} and \texttt{IsRecCEv} is unchanged.
\textsf{[LI1--8, SF1--7, CR1--6, CS1--9, LP1--5, AD1--4,
DR1--3, FC1--19, CV1--10, NB1--8, VE1--11, RF1--16]}
''',
    'tex_next_target':r'''\paragraph{The next target: the remaining column and arithmetic suppliers.}
The initial decorated-point realization is supplied by DR, including
the actual adelic genus assertion and every residue/frame clause.
The primitive arithmetic host and true-column law construction remain
to be supplied. AD proves exact-frame correction, and NB proves the
actual neighbor geometry and naturality.
The full symmetric-column branch still needs the specified penultimate
$\texttt{HSym}/\texttt{lamSym}$ description, terminal row/full levels,
the vector/incidence/evaluation statement \texttt{til\_ties}, and the
exact terminal \texttt{CarT} joins. These are separate from the direct
level-zero comparison now obtained in VE11.

On the numerical side, prove the fourteen remaining
\texttt{ParameterChoice'} families and all \texttt{SizesAt} clauses
with the same datum and uniform threshold order. RF supplies every
block-length field and the completed seven families. The actual host,
field, level-prime and point construction, together with the four
independent global branches above, remain in the continuation map.
''',
    'tex_ledger_rows':[
        r'AD1--4 & Adelic constructions & Explicit diagonal base point, supported conjugate-pair splice, global-lattice recovery and exact rational frames.',
        r'DR1--3 & Decorated realization & Local unramified Hermitian normal form including dyadic places, actual unitary adelic realizer, and every residue and rational frame condition.',
        r'FC1--19 & Actual forms and carriers & Finite charts, normalized residues, Fock/period identities, common characters and levels, distinguished-block and dilation ties, direct Forms0; DR supplies realization.',
        r'CV1--10 & Exact chart values & Actual complex member spaces, rational preimages and all-prime integral Weyl criteria; terminal values conditional on its row chart.',
        r'NB1--8 & Actual neighbors & Paired-prime duality, literal up/down lattices and functionals, coupling labels, projections and complete naturality via the supported splice.',
        r'VE1--11 & Concrete comparison & Explicit signed block values, universal ValEx and injectivity, complete comparison hypotheses and actual integral image span with $C_e=1$; separate realizability premise discharged.',
        r'RF1--16 & Refill, point and parameters & Canonical refill and conditional point installation; full ParamsT, seven parameter families and word count; fourteen families and SizesAt retained.',
    ],
    'tex_reading_order':r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. For this increment, AD in
Section~\ref{sec:adelic-geometry} supplies the elementary adelic
constructions. DR in Section~\ref{sec:decorated-realization} constructs
the initial decorated realizers from the literal CM data, including
the dyadic local argument. Read FC1--FC6 in Section~\ref{sec:global-forms} for
the actual charts and residue maps, then CV in Section~\ref{sec:chart-values}
for their exact values, and NB in Section~\ref{sec:neighbor-geometry}
for the genuine up/down neighbors. FC19 assembles only the needed
level-zero form record. VE in Section~\ref{sec:value-existence} supplies
the universal comparison values and ends with the concrete comparison.
RF in Section~\ref{sec:canonical-refill} constructs the canonical refill
and point installation before proving the numerical estimates and full
block-length record. SF/CR/CS/LP remain the earlier algebraic and
localization foundations. Every new component has an expanded report
and exact source ledger for its technical joins and retained hypotheses.
''',
}
(ROOT/'increment_v0_14.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print({'components':len(components),'new_claims':sum(map(len,claim_ids.values())),'config':'increment_v0_14.json'})
