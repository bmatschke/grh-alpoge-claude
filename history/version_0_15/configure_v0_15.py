#!/usr/bin/env python3
"""Record the exact v0.15 mathematical scope and continuation boundaries."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_14'
def read(p): return json.loads(p.read_text())
components=['column_laws','terminal_geometry','parameter_completion','size_conditions','arithmetic_constructors']
ledgers={name:read(ROOT/name/'provenance.json') for name in components}
claim_ids={name:[c['id'] for c in data['claims']] for name,data in ledgers.items()}
for name,last in [('column_laws','TL21'),('terminal_geometry','TG12'),
                  ('parameter_completion','PN16'),('size_conditions','SZ13'),
                  ('arithmetic_constructors','AC10')]:
    assert claim_ids[name][-1]==last,(name,claim_ids[name][-1])
prior=read(OLD/'next_source_targets.json')
old_cp=read(OLD/'continuation_checkpoint.json')

scope=('Partial human reconstruction of RH and Dirichlet GRH. The actual '
       'TC.Ok-to-Laws implication and the complete reference symmetric/terminal '
       'FormsTiedSym and ColsTiedSym construction are now reconstructed. All '
       'twenty-one ParameterChoice families, all SizesAt clauses and the complete '
       'NumAt join are proved under the literal supplied data. The initial size '
       'datum, prescribed-frame/cyclic ranks, coded Harish-Chandra columns and '
       'conditional level-prime datum are explicitly constructed. Finite-field, '
       'orientation, principalization and normalized-jet reductions refine the '
       'canonical evaluation boundary. Primitive arithmetic host construction, '
       'local index/nonvanishing and analytic theta suppliers, the five Later '
       'stages, twisted comparisons, geometric point suppliers and the independent '
       'global branches remain. No complete self-contained RH/GRH proof or Lean '
       'kernel replay is asserted.')
new=[
    'TL1-TL13: prove TC.Ok implies all eleven TC.Laws fields directly, through finite Hermitian lattice classes, finite stabilizers and local levels, rational invariant forms, full integral lattices and all-place Fock metrics, actual residue moves and period extensions. No completed Forms0 or terminal comparison is used to supply its own law hypothesis.',
    'TL14-TL21: construct one number field for all normalized frame-character values, finite coefficient roots and tuple readings, oriented auxiliary factors and Pins.cof, finite principalizations, and the algebraic closure/finite-generation steps for normalized jets. Isolate the actual local-index/nonvanishing, period/trace-isometry, CM-j and primitive theta/covariance inputs of evLg_canonical. Full EvLg remains conditional on them.',
    'TG1-TG12: identify the exact penultimate HSym/lamSym and terminal row/full levels; prove the actual row chart, terminal vector/lattices/residue functional and adelic incidence; construct all FormsTiedSym, AtT/CarT, symmetric adelic/stabilizer and residue/level-zero joins, and the complete ColsTiedSym. Preserve the same movements, embeddings, auxiliary data and functional orientation.',
    'PN1-PN16: prove the fourteen remaining parameter families, then join them with RF into all twenty-one families and every one of the 111 actual ParameterChoice\' fields for the same D,L. Preserve the nested threshold order and all four supplied HostArith fields.',
    'SZ1-SZ13: prove all 23 named SizesAt clauses plus splitBound>=11, all 21 NumAt fields and ChTT/ChCode; independently construct all 63 initial SizeData₂ fields and all 15 Val fields, with every Over label/code identity. Construct all 13 Ranks fields over any prescribed frame, and the literal cyclic-frame specialization.',
    'AC1-AC10: prove the bounded root-of-unity correction and the actual quadratic-subfield norm/parallel-weight identity; construct every coded HCParam and simultaneous HCVal family, then the complete chGood_of_host. Convert the retained norm-prime assertion into integral norm-one elements and all 15 LevCh fields; prove exists_levCh_of_levelPrime with its uniform threshold and supplied logarithmic window.',
]
remaining=[
    'Construct the actual arithmetic host and CM/character-field data, including Galois/frame, cyclotomic, half-different, norm and window properties. SZ13 now constructs ranks over prescribed and cyclic frames; AC constructs the coded columns once that host and its top-weight window are supplied. Rank construction alone does not supply the number field.',
    'Complete canonical TC.Ok and EvLg supply: the exact local coset/index, character and first-unfolding nonvanishing theorems; ambient periods and trace isometry; CM-j algebraicity; primitive normalized theta Taylor/torsion, four-copy/vacuum and covariance identities. TL proves all elementary finite-field/ideal/tuple reductions and Ok-to-Laws. Pins.iX and all five Later stages remain explicit where required.',
    'Extend the completed reference symmetric/terminal comparison to the actual variable-twist terminal frames, all-twist chain/joint data and standard twisted columns. The stronger OneLevelSymmetricColumns assertion has additional predicates and is not inferred from TG12.',
    'Supply the geometric Lay/RecOK/LedOK/RecExP construction and mass/window estimates, actual top-weight windows and uniform du/Dstar logarithmic window, and the analytic LevelPrime hypothesis. AC and SZ now prove all three conditional arithmetic constructors isolated by RF10; PN/SZ complete the numerical parameter and size packages. Their input existence is still substantive.',
]+old_cp['remaining_major_inputs'][4:]

completed={
    'laws_of_ok':('TL13','All eleven actual Laws fields are constructed from TC.Ok; Pins/Later and any comparison theorem are not used.'),
    'laws_all':('TL10','All generic level/forms laws, including all-place B_span, are constructed from the literal FOk, I.Ok, J.Ok and Q.Ok.'),
    'exists_gLevH':('TG1-TG2','The exact HSym/lamSym group and character equalities, common frame and finite orbit carrier are proved.'),
    'levels_top_row_sym':('TG4','Actual full/row terminal groups, characters and compatible last-pi frames are proved.'),
    'til_ties':('TG5-TG6','Actual terminal lattices, vector, dual-domain functional, same movement, adelic incidence and evaluation are proved.'),
    'formsTiedSym_std':('TG7','Full simultaneous FormsTiedSym/StdF/StdLvC with finite charts, unique terminal chart and one common G is constructed under the stated arithmetic inputs.'),
    'hermitian_data_at_level_prime':('TG8-TG10','Actual AtT, all nine CarT fields and every symmetric adelic/stabilizer compatibility clause are constructed.'),
    'herm_rest_tied':('TG11-TG12','Exact cofactor/base, residue-field and level-zero compatibility joins are proved, including functional normalization and pi-annihilation.'),
    'colsTiedSym_std':('TG12','The complete reference ColsTiedSym/StdC/StdLvC is constructed. Primitive host, Ok/Pins/Later and separate twisted/stronger predicates retain their explicit boundaries.'),
    'explicitConstants_parameterConditions_large':('PN16','All21 families and all 111 named ParameterChoice\' fields are accounted for, including the four supplied HostArith fields.'),
    'szRow_sizesAt':('SZ8','All23 named clauses and splitBound>=11 hold for the same D,L with the literal nested uniform thresholds; SizeTu is not part of this output.'),
    'szRow_numAt':('SZ9','PN16, RF15 and SZ8 supply the same P,T,L and every NumAt field, plus the RF14 density/code conjunction.'),
    'exists_sizeData_explicit':('SZ10-SZ11','The initial SizeData₂ and Val are constructed without an existing size record or parameter theorem, including all 13 windows and all 63 fields.'),
    'exists_sizeData_over':('SZ12','Actual Over transport constructs the initial size datum, WtEq, host-label/Frobenius equalities and Boolean code; ChOK/Over/RecOK remain inputs.'),
    'exists_ranks_rankVal_frame':('SZ13','Explicit even ceilings and the literal odd t formula construct all 13 Ranks fields and RankVal over the unchanged prescribed frame; cyclicFrame is also supplied.'),
    'chGood_of_host':('AC1-AC7','Actual bounded root correction, parallel MUQ, coded HCParam family and all ChGood/ChOK clauses are constructed from the supplied HostGood/WinOK and injective code.'),
    'exists_levCh_of_levelPrime':('AC8-AC10','The actual integral norm-one elements and all 15 LevCh fields are constructed from LevelPrime and the specified positive du/Dstar logarithmic window; LevelPrime itself remains open.'),
}
pn_targets=read(ROOT/'parameter_completion/next_targets.json')
for item in pn_targets.get('completed_targets',[]):
    name=item['declaration'].split('.')[-1]
    completed.setdefault(name,('PN2-PN15','The precise remaining parameter family is proved and joined in PN16, with original constants and uniformity.'))

def flatten_targets(data):
    raw=data if isinstance(data,list) else data.get('targets',[])
    out=[]
    for item in raw:
        if 'path' in item:
            out.append(item)
        else:
            for index,source in enumerate(item.get('sources',[]),1):
                t=dict(source)
                t.update({k:v for k,v in item.items() if k!='sources' and k not in t})
                t['id']=str(item.get('id','target'))+'-'+str(index)
                t['remaining_human_scope']=item.get('scope',item.get('remaining_scope',item.get('title','')))
                out.append(t)
    return out

candidates=list(prior['targets'])
for component in components:
    path=ROOT/component/'next_targets.json'
    if path.is_file(): candidates.extend(flatten_targets(read(path)))
replaced={t['path']+':'+t['declaration'].split('.')[-1]:
          completed[t['declaration'].split('.')[-1]][0]+': '+completed[t['declaration'].split('.')[-1]][1]
          for t in candidates if t['declaration'].split('.')[-1] in completed}
scope_by_name={
    'der':'Reconstruct the remaining HostDer suppliers: Frobenius/inertia and decomposition, CM fixed fields, integral different and trace-duality, and discriminant bounds. AC2-AC3 now prove norm_mu from the literal raw-host quadratic subfield and Galois-degree data; that root-of-unity norm component is discharged. The full HostDer record and the primitive raw host still require their remaining arithmetic suppliers.',
    'evLg_canonical':'TL14-TL21 prove the finite-field, ideal-principalization, tuple/orientation and conditional jet finite-generation reductions, and TL13 removes the independent Laws supplier. Retain the exact local-index/first-unfolding nonvanishing, ambient period/trace-isometry, CM-j and normalized-theta/covariance primitives, Pins.iX, and separate Later existence.',
    'recExP_of_recAtG':'Reconstruct actual RecAtG/Lay/RecOK/LedOK geometric and mass/window suppliers. PN/SZ complete ParameterChoice/SizesAt/NumAt, SZ12 constructs the initial size record, and AC proves the HC and conditional level suppliers; none supplies the geometric assumptions of this theorem.',
    'levelPrime_unconditional':'AC8-AC10 now derive the actual LevCh from LevelPrime. Prove the analytic short norm-prime interval input and its uniform constants; the existence of a prime is not a consequence of AC10.',
}
scope_updates={t['path']+':'+t['declaration'].split('.')[-1]:scope_by_name[t['declaration'].split('.')[-1]]
               for t in candidates if t['declaration'].split('.')[-1] in scope_by_name}
updates={}
for cid in ['FC19','VE10','VE11','CS4','CS5','CS6','CS7','CS8','CS9','SF7','CR6']:
    updates[cid]={'discharged_by':['TL13','TG7','TG12'],
        'scope':'The historical proof, statement, sources and graph edges remain unchanged. TL13 supplies the actual Laws premise from TC.Ok independently of the comparison. TG supplies the complete reference terminal/symmetric construction. Actual host, TC.Ok/Pins and Later remain supplied; full twisted comparisons and global metric/window branches remain separate.'}
for cid in ['FC10','FC11','FC12','FC14','CV10']:
    updates[cid]={'discharged_by':['TG1','TG2','TG3','TG4','TG5','TG6','TG7'],
        'scope':'The previously retained exact reference penultimate/terminal row, level, group/character and incidence suppliers are reconstructed in TG. This does not assert the adjacent variable-twist or stronger OneLevelSymmetricColumns predicates.'}
for cid in ['RF9','RF10']:
    updates[cid]={'discharged_by':['AC7','AC10','SZ12','PN16','SZ8','SZ9'],
        'scope':'All three isolated conditional constructor theorems—chGood_of_host, exists_levCh_of_levelPrime and exists_sizeData_over—are now proved, as are full parameter/size/NumAt joins. Actual HostGood/top WinOK, analytic LevelPrime, the prescribed du/Dstar window and geometric Over/RecOK/RecExP remain substantive inputs. No point existence is inferred from conditional constructors alone.'}
for cid in ['RF11','RF12','RF13','RF14','RF15','RF16']:
    updates[cid]={'discharged_by':['PN16','SZ8','SZ9','SZ11','SZ12','SZ13'],
        'scope':'All21 parameter families and literal SizesAt/NumAt are now complete for the same actual D,L, with nested uniform thresholds. Initial size construction and actual rank construction are separate earlier steps; they do not assume the final numerical package or construct the primitive arithmetic host.'}

precision=[
    'All536 predecessor claim fields, source arrays, source-file records and old dependency adjacency lists are preserved. Current annotations are additive; old component boundaries remain historical statements.',
    'TL13 proves Ok-to-Laws from actual lattice/index/character hypotheses. The proof uses only the elementary NB1 duality lemma, not a completed Forms0/terminal comparison to construct its own Laws. Existence of Ok is separate.',
    'TL14 proves one common number field for ALL normalized unramified frame-character values. Pointwise algebraicity alone is insufficient. The coefficient-field requirements of large_2 remain antecedents, not permission to enlarge a fixed coefficient field silently.',
    'TL17 retains CM-j algebraicity and the ambient period/trace-isometry supplier. TL18-TL19 prove closure, transport and finite generation conditional on exact primitive theta/covariance inputs; they do not infer actual membership from the definition of a union restricted to FinAlg indices.',
    'TL20 retains local first-unfolding and character nonvanishing in twIdx_ok_closed. Extracting roots/square roots from old Ok does not prove replacement Ok. TL21 does not manufacture any of the five Later stages.',
    'TG uses the actual reference character with empty Q. Same movement matrices, bar-pi denominator, selected residue prime, determinant factors and coefficient embeddings are retained. The all-twist and stronger OneLevelSymmetricColumns statements are separately targeted.',
    'TG constructs AtT before functional normalization, then checks that all carrier/Ad/stabilizer fields needed by that same object are unchanged. Its cyclic residue comparison is over the selected quotient S_v/(pi), not just an abstract group of prime order.',
    'PN16 accounts for all 111 named fields: 23 constants, 23 positivity assertions, 61 family assertions and 4 literal HostArith fields. Every threshold preserves epsilon,C then cD then ch then x0 before D,L and varying J.',
    'SZ8 is the actual 23-plus-one SizesAt conjunction; SizeTu is not a conjunct. SZ9 uses the same ParameterChoice and ParamsT, and checks all 21 NumAt fields. The exact lStar=m*b/Dstar factor and variable x^theta coefficients are preserved.',
    'SZ10-SZ11 construct all 13 initial windows and all 63 SizeData₂ fields without an existing size datum or PN16. The raw Lambda estimate supplies the noncircular bottom bound. Initial zero numerical fields are later replaced by RF canonical refill and are not asserted to prove final forcing estimates.',
    'SZ13 constructs actual ranks over the unchanged prescribed frame, and the literal cyclicFrame. Rank/frame existence alone does not produce the number field/host with its required arithmetic properties.',
    'AC proves the host root-of-unity norm identity via its actual quadratic subfield and degree, not by treating an arbitrary CM-type product as one. The one-place torsion correction preserves top/thin weights and the strict thick window.',
    'AC7 uses the literal HostGood q0H prime field to justify nonemptiness of the defining least-prime set. It does not smuggle a prime-in-progression theorem into the coded-column constructor. AC10 retains analytic LevelPrime and the original du/Dstar logarithmic window.',
    'The source/hash audit and acyclic human dependency graph are not a Lean compilation, kernel replay or transitive Lean dependency audit. No complete RH/GRH proof is asserted.',
    'The deliverables are cumulative TeX and the updated ZIP. Draft-mode TeX validation does not produce a PDF or certify visual layout. The preserved 150-page v0.13 PDF is historical and lacks v0.14 and v0.15.',
]
conclusions={
    'column_laws':new[0], 'canonical_evaluation_reduction':new[1],
    'terminal_symmetric_comparison':new[2], 'parameter_completion':new[3],
    'size_and_rank_construction':new[4], 'arithmetic_constructors':new[5],
    'remaining':'Primitive host/CM supply; actual canonical local/analytic inputs and Later; all-twist comparison; geometric point and analytic LevelPrime/window suppliers; the four unchanged independent global branches.',
}
cfg={
    'components':components,'tex_component_order':components,'date':'2026-11-22',
    'scope':scope,'new_in_this_version':new,'remaining_major_inputs':remaining,
    'claim_updates':updates,'local_conclusions':conclusions,
    'completed_previous_frontier':'Actual Ok-to-Laws; complete reference terminal/symmetric forms and columns; all 21 parameter families and all SizesAt/NumAt fields; initial size, prescribed/cyclic ranks, coded HC columns and conditional level constructors. Canonical evaluation is reduced to precise retained local/analytic suppliers.',
    'next_local_priority':'Construct actual canonical local-index/nonvanishing and normalized-theta/period inputs; extend reference columns to all twists; construct the primitive arithmetic host and geometric point suppliers, preserving separate global branches.',
    'priority_groups':{'1':'Canonical column/analytic inputs and all-twist comparison after completed reference laws and terminal geometry',
                       '2':'Geometric point, actual top-degree/window and analytic level-prime supply after complete numerical constructors',
                       '3':'Primitive host, character field, different-ideal and norm arithmetic',
                       '4':'Unchanged independent spectral, metric, cohomological and prime-window branches'},
    'precision_notes':precision,'replaced_target_keys':replaced,'target_scope_updates':scope_updates,
    'next_steps':[
        'Use TL21 and its exact source targets to prove the local-index/nonvanishing, ambient period/trace-isometry and primitive normalized-theta inputs. Reuse TL13 for Laws; do not reopen lattice finiteness or the completed reference terminal comparison.',
        'Use TG12 to extend the actual reference symmetric columns to the variable-twist terminal charts and full standard twisted comparison. Preserve every twist-frame depth, character and joint datum.',
        'Continue primitive arithmetic host/field/different construction and the actual RecAtG/RecExP/LedOK geometric suppliers. AC and SZ now supply the three RF10 conditional constructors; PN/SZ supply the complete numerical package once the actual input data are built.',
        'Keep the four independent global spectral, metric, cohomological and prime-window branches separate. Analytic LevelPrime and the uniform du/Dstar window are explicit remaining inputs of AC10.',
    ],
    'precision_supersessions':[
        {'previous_version':'0.14','historical_statement':'Actual column laws and reference terminal/symmetric-column geometry remain independent suppliers.',
         'current_statement':'TL13 proves Laws from TC.Ok; TG constructs the entire reference FormsTiedSym and ColsTiedSym, including terminal geometry and carrier joins. Actual Ok/Pins/Later and separate all-twist constructions remain.',
         'completed_by':['TL13','TG7','TG10','TG11','TG12']},
        {'previous_version':'0.14','historical_statement':'Fourteen parameter families, complete SizesAt and the HC/level/initial-size constructors remain.',
         'current_statement':'PN16 completes all 21 parameter families; SZ8-SZ9 complete SizesAt/NumAt. SZ10-SZ12 construct the initial size datum, and AC7/AC10 prove both other conditional constructors. Their input host, analytic and geometric existence remains explicit.',
         'completed_by':['PN16','SZ8','SZ9','SZ11','SZ12','AC7','AC10']},
    ],
    'tex_front_summary':r'''\textbf{What version 0.15 achieves.} The actual true-column laws now follow from \texttt{Ok}, independently of the later comparison. The entire reference symmetric and terminal forms/column construction is explicit. All twenty-one numerical parameter families, the complete size inequalities, and the actual numerical join are proved. The initial size datum, prescribed and cyclic ranks, coded Harish--Chandra columns and conditional level-prime datum are constructed field by field. Canonical evaluation is reduced to specific local nonvanishing, period and primitive theta inputs, with its finite-field and ideal arguments supplied. Primitive arithmetic host construction, the five later stages, all-twist comparisons, geometric point suppliers and the independent global branches remain explicit. This is \textbf{a partial human reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.''',
    'tex_remaining_local':r'''The earlier LI/SF/CR/CS, AD/DR/FC/CV/NB/VE arguments now give the
concrete integral comparison under the supplied arithmetic host,
\texttt{TC.Ok}, \texttt{Pins}, and \texttt{Later}. TL13 supplies
\texttt{Laws} from \texttt{Ok}; a separate law premise is no longer
needed. TG1--TG12 construct the full reference \texttt{FormsTiedSym}
and \texttt{ColsTiedSym}, including the exact penultimate and terminal
groups, row levels, vector, lattices, residue functional and all carrier
and stabilizer joins. Variable-twist terminal frames and complete
twisted comparisons remain separate tasks.

TL14--TL21 supply finite coefficient fields and roots, actual character
tuple readings, orientation, ideal principalization, and the closure
and finite-generation reductions for normalized jets. They retain the
precise local-index/nonvanishing, ambient-period/trace-isometry,
CM-$j$, and primitive theta/covariance theorems. The five stages of
\texttt{Later} are not produced by this conditional assembly.

RF's canonical refill and point installation are complemented by all
twenty-one parameter families in PN16, every size clause in SZ8, and
the complete same-data \texttt{NumAt} join in SZ9. SZ10--SZ12
independently construct the initial size datum and its exact labels,
degrees and word code. SZ13 supplies actual ranks over the prescribed
frame, including the literal cyclic frame. AC1--AC7 construct the coded
columns and \texttt{ChGood} from the supplied host and top window;
AC8--AC10 construct the full level datum from \texttt{LevelPrime}
and the stated logarithmic window. Thus all three conditional
constructors isolated in RF10 are proved. Actual host and top-window
existence, the analytic norm-prime theorem, and the geometric
\texttt{Lay/RecOK/LedOK/RecExP} supply and its mass/window estimates
remain substantive. None of these joins changes the four independent
global branches below.
\textsf{[TL1--21, TG1--12, PN1--16, SZ1--13, AC1--10]}
''',
    'tex_next_target':r'''\paragraph{The next target: actual analytic and geometric suppliers.}
Start with TL21's exact canonical-evaluation boundary: local coset and
first-unfolding nonvanishing, period and trace-isometry data, CM-$j$
algebraicity, and the primitive normalized-theta identities and covariance.
The elementary coefficient-field, tuple and ideal arguments are already
available, as is the entire \texttt{Ok}$\Rightarrow$\texttt{Laws}
implication. TG supplies all reference symmetric and terminal geometry;
its next targets address the actual variable-twist terminal and chain
comparisons without importing their conclusions from the reference case.

The numerical branch is now complete at its stated conditional boundary:
PN16, SZ8 and SZ9 construct the full parameter, size and numerical records
for the same data. SZ constructs the initial size and rank records; AC
constructs coded columns and the conditional level datum. Continue with
the primitive host, actual top-weight and logarithmic windows, the
analytic norm-prime input, and the geometric point suppliers. The
source-target map distinguishes these obligations from the four
unchanged global branches, and retains stronger optional predicates
only as separate tasks.
''',
    'tex_ledger_rows':[
        r'TL1--21 & Column laws and canonical reductions & Full Ok-to-Laws; finite character fields, tuple readings, orientation, principalization and conditional jet reductions; primitive local/analytic inputs retained.',
        r'TG1--12 & Full reference symmetric columns & Exact terminal geometry, all forms and Hermitian carriers, residue normalization and complete ColsTiedSym; actual host/Ok/Pins/Later retained.',
        r'PN1--16 & Complete parameter choice & All twenty-one families and every field of ParameterChoice, with the same data and uniform threshold order.',
        r'SZ1--13 & Sizes, initial data and ranks & Complete SizesAt/NumAt, all initial size fields and Over identities, prescribed and cyclic frame rank constructors.',
        r'AC1--10 & Arithmetic constructors & Exact root congruences, coded columns and ChGood; integral norm elements and full LevCh from the retained analytic LevelPrime input.',
    ],
    'tex_reading_order':r'''For the global spine, read Sections~\ref{sec:analytic},
\ref{sec:scalar}, and \ref{sec:frame}. The earlier AD/DR/FC/CV/NB/VE
sections reconstruct the actual adelic realizers, charts, values,
neighbors and concrete integral comparison. In this increment, read
TL1--TL13 in Section~\ref{sec:column-laws} for the independent law
construction, then TG in Section~\ref{sec:terminal-geometry} for the
complete reference terminal and symmetric joins. TL14--TL21 separate
the finite arithmetic reductions from their precise remaining analytic
inputs.

For the numerical branch, RF supplies the scales, refill and seven
families, PN in Section~\ref{sec:parameter-completion} completes the
parameter record, and SZ in Section~\ref{sec:size-conditions} proves
every size and numerical join. Logically, SZ10--SZ13 give the earlier
initial-size and rank construction independently of those joins.
AC in Section~\ref{sec:arithmetic-constructors} proves the coded-column
and conditional level constructors and their exact unit constraints.
The expanded reports and field audits record the detailed joins;
the current continuation map states the still-supplied inputs.
''',
}
(ROOT/'increment_v0_15.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print({'components':len(components),'new_claims':sum(map(len,claim_ids.values())),
       'completed_target_keys':len(replaced),'config':'increment_v0_15.json'})
