#!/usr/bin/env python3
"""Record the exact v0.16 proof increment and its retained interfaces."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_15'
def read(p):return json.loads(p.read_text())
components=['arithmetic_hosts','period_arithmetic','theta_arithmetic','canonical_indices','twisted_comparison']
ledgers={c:read(ROOT/c/'provenance.json') for c in components}
prior=read(OLD/'next_source_targets.json')
oldcp=read(OLD/'continuation_checkpoint.json')
scope=('Partial human reconstruction of RH and Dirichlet GRH. The prescribed-character cyclotomic host, '
       'all HostDer fields and trace-self-dual half-different are constructed under the literal prime and splitting hypotheses. '
       'Actual ambient periods, trace isometries, CM-j integrality and the normalized one-dimensional theta arithmetic '
       'are reconstructed. The local-index/nonvanishing and canonical replacement suppliers and the complete standard '
       'all-twist comparison are proved with their original data and interfaces. Multidimensional vacuum/indicator/covariance, '
       'the actual NChoice/TupTied arithmetic join, Pins.iX, all five Later stages, analytic prime/window and geometric point '
       'suppliers, and the four independent global branches remain. Named classical inputs are explicit. '
       'No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.')
new=[
 'AH1-AH18: construct the mixed character frame and exact Artin sign correction, cyclotomic fixed field, primitive conductor, stabilized order, kept characters, kernel and twist formulas. Prove all 30 HostDer fields, including ramification/decomposition, CM type, relative half-different, trace self-duality and the three discriminant bounds. Complete literal fieldChi under its original q,d/splitting conditions and quantifier order.',
 'PA1-PA15: construct the actual normalized period and unkilled half-point, rational four-copy trace isometry, algebraic complex extension, all local AtP choices and all AmbIn.Ok fields. Prove genuine finite support of kappa on split primes, actual CM-j integrality and FieldOK, and algebraic torsion coordinates. The exact conditional even-theta transfer is retained and then supplied by TA.',
 'TA1-TA14: reconstruct the normalized one-dimensional odd/even theta arithmetic. A purely analytic product/Legendre argument, formal ODE uniqueness and a descended CM polynomial give galSg; exact division quotients and their constant term give gal1. Fixed-field descent proves all rational-translate coefficients algebraic, and exact half-period/conjugate-curve transport gives all use1 clauses. No arbitrary embedding is assumed continuous.',
 'CI1-CI19: reconstruct finite local cosets and normal forms, actual projected-kernel characters, finite-field support/nonzero counts and local reduction. Prove exists_chIdx_of_cst and twIdx_ok_closed, and the canonical replacement join under its actual supplied inputs. The nonvanishing comes from explicit finite counts and the character rigidity from a stabilized sum, independently of Laws or a completed comparison.',
 'TX1-TX16: construct the variable-twist full/row terminal charts with their different depths, the common penultimate character and carrier, the integral Law0 equivalence, all twisted chain/form/level data and exact terminal incidence/evaluation. Join the ten actual SymmetricTwistedColumnsAtPrimes fields in colsTwPTiedS_std, retaining the original NChoice, TupTied and same-xi interface.',
]
remaining=[
 'Complete the canonical analytic supplier: the actual StdOK/four-copy vacuum identity and normalized indicator/covariance (finAlg_step), then the remaining EvLg join. AH, PA, TA and CI now supply its host arithmetic, ambient periods, CM-j, primitive one-dimensional theta and local-index ingredients. Pins.iX and all five Later stages remain explicit.',
 'Construct the actual normalized arithmetic NChoice with its finite DVR extensions, valuation embeddings and Mt basis/integral-lattice comparison, then TupTied on the same selected primes and characters. TX16 proves the all-twist comparison conditional on this precise original interface. OneLevelSymmetricColumns is a stronger optional target with additional restrictions.',
 'Supply the simultaneous q,d prime/splitting conditions in the required analytic windows, the actual top-weight and du/Dstar logarithmic windows, analytic LevelPrime, and the geometric Lay/RecOK/LedOK/RecExP construction with its mass/window bounds. AH18 constructs the field once its stated prime hypotheses hold; the earlier numerical and conditional constructors do not themselves produce those analytic/geometric inputs.',
]+oldcp['remaining_major_inputs'][4:]

def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
 raw=data if isinstance(data,list)else data.get('targets',[])
 out=[]
 for t in raw:
  if 'path'in t:out.append(t)
  else:
   for j,s in enumerate(t.get('sources',[]),1):
    x=dict(s);x.update({k:v for k,v in t.items()if k!='sources' and k not in x})
    x['id']=str(t.get('id','target'))+'-'+str(j)
    x['remaining_human_scope']=t.get('scope',t.get('remaining_scope',t.get('title','')))
    out.append(x)
 return out
completed={}
candidates=list(prior['targets'])
for component in components:
 p=ROOT/component/'next_targets.json'
 if not p.is_file():continue
 d=read(p);candidates.extend(flat(d))
 for t in d.get('completed_targets',[])+d.get('closed_source_targets',[]):
  cs=t.get('claims',t.get('closed_by',t.get('completed_by',[])))
  cs=cs if isinstance(cs,str)else ','.join(cs)
  completed[key(t)]=cs+': '+t.get('reason',t.get('scope',t.get('remaining_human_scope','Literal conditional source conclusion reconstructed.')))
replaced={key(t):completed[key(t)] for t in candidates if key(t)in completed}
scope_by_name={
 'evLg_canonical':'AH supplies conditional arithmetic host/half-different, PA9/PA13 actual AmbIn.Ok and FieldOK, TA10/TA12 primitive normalized one-dimensional theta arithmetic, and CI the actual local-index/nonvanishing/canonical replacement suppliers. Retain the literal StdOK/four-copy vacuum and normalized indicator/covariance inputs, Pins.iX, and each of the five Later stages. A canonical choice or a finite-generation wrapper does not establish these remaining premises.',
 'thetaVector_fourthPower_algebraicGerm':'PA4 supplies algebraic complex substitution; PA10 finite nonzero algebraic kappa on exactly the split-prime subtype; TA10/TA13 supplies primitive odd/even theta coefficient algebraicity. Reconstruct the actual StdOK/four-copy vacuum identity and its same-data use in the fourth-power germ; do not infer a multivariable identity from one-dimensional algebraicity.',
 'finAlg_step':'TA now supplies the normalized one-dimensional theta coefficients and their exact conjugacy. Reconstruct the actual normalized indicator and covariance identities for the chosen multi-variable function, with its finite-degree control and exact group action; TL18-TL19 already supply formal closure/finite-generation reductions.',
 'recExP_of_recAtG':'Reconstruct the actual RecAtG/Lay/RecOK/LedOK geometric and mass/window inputs. PN/SZ complete parameter and size/NumAt, AH constructs the conditional field/host, AC proves coded HC and conditional level constructors, and PA/TA/CI/TX close specified local suppliers. Those conditional constructions do not supply the geometric point hypothesis.',
 'levelPrime_unconditional':'Prove the analytic short norm-prime interval input and its uniform constants; AC8-AC10 construct LevCh once LevelPrime and the stated logarithmic window are supplied. AH conditional field arithmetic does not select the prime in that analytic window.',
}
scope_updates={key(t):scope_by_name[t['declaration'].split('.')[-1]] for t in candidates if t['declaration'].split('.')[-1]in scope_by_name}
updates={}
def add(ids,by,scope):
 for cid in ids:updates[cid]=dict(discharged_by=by,scope=scope)
add(['TL17'],['PA9','PA13'], 'The historical conditional principalization/field reduction is preserved. PA9 supplies actual ambient data; PA11-PA13 supply actual CM-j integrality and FieldOK, including the prescribed field-containment quantifier.')
add(['TL18','TL19'],['PA4','PA10','TA10','TA12','TA13'], 'Actual algebraic complex substitution, finite split-prime correction, primitive odd/even rational-translate coefficients and one-dimensional conjugacy are now supplied. Full StdOK/four-copy vacuum and normalized indicator/covariance remain distinct inputs.')
add(['TL20','TL21'],['CI15','CI16','CI17','CI18','CI19','PA9','PA13','TA13'], 'The local initial/canonical index, projected-kernel character and first-unfolding nonvanishing suppliers are now reconstructed. Ambient and one-dimensional analytic primitives are also supplied by PA/TA. The current joint boundary retains actual vacuum/indicator/covariance, Pins.iX and all Later stages.')
add(['TG12','FC19','VE10','VE11','CS4','CS5','CS6','CS7','CS8','CS9','SF7','CR6'],['TX10','TX11','TX12','TX15','TX16'], 'The reference-to-all-twist comparison is now explicitly constructed, including integral Law0, common characters, levels, terminal rows and actual transport/evaluation. The source NChoice/TupTied/same-xi interface and Ok/Pins/Later remain as stated. Old proofs and graph edges are unchanged.')
add(['HC4','HC10'],['AH17','AH18'], 'The actual conditional cyclotomic field/HostAx and prescribed-character fieldChi suppliers are reconstructed, including all HostDer fields. Prime/splitting and analytic window hypotheses remain explicit; no PairEx or cohomological window is inferred.')
add(['AC7','AC10','SZ12','SZ13','RF9','RF10'],['AH17','AH18','PA9'], 'The field/host arithmetic can now be supplied under its literal q,d/splitting hypotheses, and the ambient period construction is explicit. The original HostGood/top WinOK, analytic LevelPrime/logarithmic window and geometric Over/RecOK interfaces retain their exact scope.')

precision=[
 'All 608 predecessor claim records, source arrays, source-file metadata, dependency adjacency lists and prior version-local conclusions are preserved. New discharge annotations are additive; historical premise paragraphs remain recognizable.',
 'AH constructs fieldChi only under its original prime, congruence, coprimality and splitting hypotheses. Its c0,e0 precede e,q,d,b. Arithmetic host construction is complete at that conditional boundary; simultaneous analytic prime selection and windows are not supplied.',
 'The source name KcDiff.principal denotes existence of an ideal b with relative different=b*bar(b), coprime factors and specified support. It is not a principal-ideal-class assertion. AH14 uses the conjugated trace to prove the actual inverse half-different self-dual.',
 'PA9 accounts for all 8 KapIn, 8 VacIn, 3 AmbIn and 2 Ok fields. Local approximation uses distinct conjugate-prime weights and does not assume conjugation continuous in one split-prime topology. PA10 and kappa are restricted to the exact prime-and-SplitK subtype.',
 'PA11 uses modularJ=1728*g2^3/(g2^3-27g3^2). The modular-translate leading coefficient must be a unit, not merely nonzero. The nonsquare determinant prevents cancellation of equal leading exponents.',
 'TA14 is a purely analytic sigma product/Legendre/uniqueness/addition lemma. TA10 does not depend on the conditional PA15 whose arithmetic premise it supplies. Formal identities are transported before any convergence conclusion. No arbitrary field embedding is assumed continuous.',
 'TA5 proves CM-output coordinate membership in the original M by Aut(C/M) descent. Only countable generated subfields are extended when transporting a general embedding. TA8 fixes the power-root ambiguity by an explicit nonzero constant term, and TA12 retains the exact 16-torsion/8-division normalization.',
 'CI local finite support, finite-field positive counts, projected-character rigidity and initial index construction are independent of completed column Laws and terminal comparison conclusions. Canonical replacement still retains the actual old Ok/Deep premises where the source does.',
 'TX uses the exact full-terminal scalar q_P^(c+1) and row scalar q_P. Their additive P-valuations must not be confused with these exponents unless q_P is a uniformizer; the row level contains the depth-one reduction kernel. The outer inverse in the character, common penultimate character, same movement matrix, bar-pi cancellation and kappa inverse orientations are all retained. Every permissible Law0 map equals the displayed reindexing, so arbitrary supplied l0 is allowed.',
 'TX16 constructs exactly ten standard all-twist fields; it retains the actual NChoice/TupTied with tp.xi=I.xi. Finite character readings alone do not provide finite DVR/Mt integral comparisons. The stronger OneLevelSymmetricColumns predicate is separate.',
 'Named ordinary classical inputs are explicit, including Lagrange four-squares, complex elliptic uniformization and stated modular/ideal-theoretic background. This is a partial human reconstruction rather than a foundation-free formalization.',
 'Exact source/file/range hashes and the acyclic human dependency graph are not a Lean build, kernel replay or transitive Lean dependency audit. No complete RH/Dirichlet-GRH proof is asserted.',
 'Current deliverables are cumulative TeX and updated ZIP. Draft-mode TeX checking produces no PDF and certifies no visual layout. The preserved v0.13 PDF is historical and lacks v0.14-v0.16.',
]
conclusions={k:v for k,v in zip(['arithmetic_host','ambient_periods','one_dimensional_theta','canonical_local_indices','all_twist_comparison'],new)}
conclusions['remaining']='Actual multidimensional vacuum/indicator/covariance, NChoice/TupTied, Pins.iX and Later; analytic prime/window and geometric point suppliers; unchanged independent global branches.'
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,
 new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=conclusions,
 completed_previous_frontier='Conditional actual cyclotomic/character host and HostDer; ambient periods/AtP/FieldOK; primitive one-dimensional normalized theta algebraicity and conjugacy; local indices/nonvanishing and canonical replacement; complete standard all-twist comparison with original NChoice/TupTied interface.',
 next_local_priority='Reconstruct actual multidimensional vacuum/indicator/covariance and normalized arithmetic NChoice/TupTied suppliers, then the canonical and global joins; retain analytic prime/window, geometric and independent global branches.',
 priority_groups={'1':'Remaining canonical analytic and normalized arithmetic comparison suppliers', '2':'Geometric point, top/logarithmic windows and analytic level-prime suppliers','3':'Analytic prime selection and host-window/cohomological suppliers after completed conditional field arithmetic','4':'Unchanged independent spectral, metric, cohomological and prime-window branches'},
 precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,
 next_steps=[
  'Start from PA/TA/CI and finish the actual StdOK/four-copy vacuum identity and finAlg_step indicator/covariance, then evLg_canonical. Do not reopen CM-j, primitive one-dimensional theta, local finite cosets or projected-kernel nonvanishing.',
  'Use TX16 with its exact next ranges to construct normalized NChoice (including Mt integral comparison) and TupTied on the same xi,psi,Q. Earlier TL character readings and completed TX geometry do not substitute for this arithmetic interface.',
  'Continue the analytic norm-prime/simultaneous q,d and top/logarithmic window suppliers and the actual Lay/RecOK/LedOK/RecExP geometry. Reuse AH17/AH18, AC and PN/SZ conditional constructors at their proved boundaries.',
  'Preserve and address the four independent global branches separately: spectral/theta common images, dimensions/metric transport, congruence/cohomological windows, and simultaneous PairEx/global prime-sum balance.',
 ],precision_supersessions=[
  dict(previous_version='0.15',historical_statement='Primitive arithmetic host, half-different and prescribed character field remain.',current_statement='AH1-AH18 reconstruct their actual conditional arithmetic construction, with all 30 HostDer and all 8 FieldRows fields; analytic prime and window selection remain.',completed_by=['AH17','AH18']),
  dict(previous_version='0.15',historical_statement='Local indices/nonvanishing, ambient periods/CM-j and primitive theta coefficients remain.',current_statement='CI supplies the local index/nonvanishing/canonical replacement theorems, PA actual ambient and FieldOK, and TA exact one-dimensional theta algebraicity/conjugacy. Multidimensional vacuum/indicator/covariance, Pins.iX and Later remain.',completed_by=['CI15','CI17','CI19','PA9','PA13','TA10','TA12','TA13']),
  dict(previous_version='0.15',historical_statement='Variable-twist terminal and complete all-twist comparisons remain.',current_statement='TX constructs Law0 and the entire standard all-twist comparison, with the original NChoice/TupTied/same-xi interface retained and separately targeted.',completed_by=['TX10','TX11','TX12','TX15','TX16']),
 ])
cfg['tex_front_summary']=r'''\textbf{What version 0.16 achieves.} The actual prescribed-character
cyclotomic host and all its derived arithmetic fields are constructed under
the stated prime hypotheses. The ambient periods, trace isometries,
CM-$j$ integrality, and normalized one-dimensional theta coefficients and
their Galois conjugacy are now explicit. Finite local indices and their
nonvanishing/character suppliers are reconstructed. The standard comparison
is extended to all twists, including its integral zero-step identification
and exact terminal evaluations. The actual multivariable vacuum and
covariance identities, normalized arithmetic choice/tuple interface,
\texttt{Pins.iX}, the five later stages, analytic prime/window and geometric
point suppliers, and the independent global branches remain. This is
\textbf{a partial human reconstruction, not yet a self-contained proof
of RH or Dirichlet GRH}.'''
cfg['tex_remaining_local']=r'''TL13 supplies the actual column laws from
\texttt{TC.Ok}; TG supplies the complete reference symmetric and terminal
construction. TX in Section~\ref{sec:twisted-comparison} now constructs
the complete standard all-twist comparison, including integral
\texttt{Law0}, common penultimate characters, level maps, terminal rows,
and the exact movement/evaluation identities. Its original
\texttt{NChoice}/\texttt{TupTied}/same-character arithmetic interface
remains substantive; the stronger one-level predicate remains separate.

AH constructs the actual conditional cyclotomic character field and all
\texttt{HostDer} fields. PA supplies actual ambient periods, trace
isometries, all local corrections and \texttt{FieldOK}; TA supplies
normalized one-dimensional theta algebraicity and exact conjugacy;
CI supplies the local index, finite-field nonvanishing and canonical
replacement theorems. Thus those old supplier boundaries have been
discharged. The remaining canonical analytic work is the actual
\texttt{StdOK}/four-copy vacuum identity and normalized indicator/covariance,
followed by their precise \texttt{EvLg} join. \texttt{Pins.iX} and each
of the five \texttt{Later} stages remain explicit.

PN/SZ give all numerical parameters, sizes, ranks and same-data
\texttt{NumAt}; AC gives the coded columns and conditional level datum.
AH18 now supplies their field/host arithmetic when its prescribed
$q,d$ and splitting hypotheses hold. The analytic selection of those
primes in the needed windows, top-weight and logarithmic windows,
\texttt{LevelPrime}, and the geometric
\texttt{Lay/RecOK/LedOK/RecExP} supply with mass/window estimates remain.
These local advances do not discharge the four global branches below.
\textsf{[AH1--18, PA1--15, TA1--14, CI1--19, TX1--16]}
'''
cfg['tex_next_target']=r'''\paragraph{The next target: multivariable identities and the arithmetic join.}
Continue from the completed period, one-dimensional theta and local-index
suppliers to the actual four-copy/vacuum and normalized indicator/covariance
identities. The reductions in TL18--TL21, now supplied by PA/TA/CI, identify
the exact remaining steps; they do not replace those identities by a
finite-generation argument. In parallel, construct the normalized
\texttt{NChoice} and same-object \texttt{TupTied} used in TX16, including
their discrete valuation extensions and integral $M_t$ comparisons.

For the global construction, use the completed conditional field/host
of AH, the arithmetic constructors AC and the numerical package PN/SZ.
The remaining prime/window and geometric existence hypotheses are
substantive. Their exact source targets are separated from the unchanged
spectral, metric, cohomological and simultaneous-prime global branches.
'''
cfg['tex_ledger_rows']=[
 'AH1--18 & Character field and host & Exact mixed frame, cyclotomic fixed field, all derived arithmetic and half-different fields; conditional prescribed-character fieldChi.',
 'PA1--15 & Ambient period arithmetic & Actual normalized periods, rational/local/complex isometries, AmbIn.Ok, finite correction, CM-j and FieldOK; exact torsion/even transfer.',
 'TA1--14 & Normalized theta arithmetic & Pure analytic normalization, formal ODE and CM rigidity, all rational-translate algebraicity and exact arbitrary-field even-theta conjugacy.',
 'CI1--19 & Canonical local indices & Finite cosets/normal forms, projected characters, finite-field nonvanishing and literal initial/canonical index suppliers.',
 'TX1--16 & Complete all-twist comparison & Exact terminal and common levels, integral Law0, chain/form/level/row data and ten-field standard join; NChoice/TupTied retained.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
The AD/DR/FC/CV/NB/VE sections give actual realizers and the concrete
integral comparison, TL gives its independent laws, and TG gives the
reference terminal construction. In this increment, read AH in
Section~\ref{sec:arithmetic-hosts} for the conditional host and character
field, then PA in Section~\ref{sec:period-arithmetic} for its actual
period and isometry data. TA in Section~\ref{sec:theta-arithmetic}
starts with the purely analytic TA14 and formal TA2 before supplying
the arithmetic theta premises; its later TA13 is the joint endpoint.
Read CI for the local index/nonvanishing supplier and TX for the full
all-twist comparison, preserving every displayed arithmetic interface.

For the numerical branch, RF supplies scales and refill, PN completes
the parameter record, SZ gives all size/NumAt and initial/rank constructions,
and AC gives coded columns and the conditional level constructor.
AH supplies their conditional field arithmetic; it does not supply
their analytic windows. Reports and source ledgers retain field-by-field
coverage and exact future targets. Historical premise paragraphs are
updated by explicit version bridges and additive claim annotations.
'''
(ROOT/'increment_v0_16.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'components':components,'new_claims':sum(len(d['claims'])for d in ledgers.values()),'completed_target_keys':len(replaced)},indent=2))
