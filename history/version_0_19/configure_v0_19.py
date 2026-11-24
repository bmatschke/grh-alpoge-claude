#!/usr/bin/env python3
"""Describe the v0.19 increment without altering any predecessor proof."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_18'
def read(p):return json.loads(p.read_text())
components=['arithmetic_realization','host_character_frame','theta_test_inputs','quantitative_windows']
ledgers={c:read(ROOT/c/'provenance.json')for c in components}
prior=read(OLD/'next_source_targets.json')
claimids={c:[x['id']for x in d['claims']]for c,d in ledgers.items()}
def span(c):
 a=claimids[c];return a[0]+'–'+a[-1]
scope=('Partial human reconstruction of RH and Dirichlet GRH. The actual host Hecke-character frame and determinant data, local arithmetic level/character comparisons and conditional weight/series reading are expanded. Same-base initial coefficient, jet and bare later-stage constructions are joined with their exact compatibility boundaries. Primitive finite theta-test arithmetic, fixed-field sum and finite-support deductions are reconstructed with remaining analytic, separation, period and operator inputs explicit. The literal quantitative mass window is proved from SiegelMassRatioCM, including actual Euler products, local indices and Vandermonde estimates; exact prime-count and scale transports retain their uniform analytic/arithmetic suppliers. Classical nonvanishing at one gives the bounded-modulus real-zero margin. Compatible nonempty arithmetic/geometric realization, global mass and weighted prime-window inputs, the remaining primitive theta identities and the four global branches remain. No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.')
new=[
 span('arithmetic_realization')+': reconstruct exact bad places and selected halves, tame Artin readings, conductor parahoric and type unipotent levels, identity-frame reductions and the literal Joint intersection. Prove coefficient-field intertwiner descent and conditional CellWt, harmonic extremal/sign/image/injectivity, all WtMap fields, exact global LevMatch, denominator-clearing form readings and the installed SerAt.join. Retain actual global realizations, normalized algebraic adic-character existence, all-place nonempty coverage and the named complex classification/characteristic-zero coefficient inputs.',
 span('host_character_frame')+': construct actual unitary idele characters and their prescribed restrictions, exact auxiliary inertial order, the full host HFrame and determinant package. Join the resulting frame with the same original preliminary datum and the existing coefficient/jet/stage constructions. Preserve the distinction between a same-base initial datum with bare Later and a compatible V4.Core.',
 span('theta_test_inputs')+': reconstruct primitive finite theta calculations, local compact-integral arithmetic and rational coefficient descent, actual finite-support and finite-sum consequences under the same coefficient-field hypotheses. Identify the remaining convergence, separating-functionals, compatible FieldOK, period/tower/ratio and positive operator/type inputs explicitly.',
 span('quantitative_windows')+': prove absolute logarithmic convergence of the actual CM Euler product, exact finite local index formulas, the mass telescope under its explicit law, and the Vandermonde comparison with constant 30+(2+2C0)/epsilon. Verify every actual PlaceData clause and prove window_lower with its original quantifier order and same-object hypotheses. Prove weighted-to-unweighted norm-prime transport, uniform levelPrimeN and the nine-tenths dyadic count from ShortNorm, and the classical bounded-modulus real NoExc margin.',
]
remaining=[
 'Construct compatible nonempty twist/local data with the same normalized character and weight fields, all-place coverage, actual IsGalOf local readings, side/index selections and global realization. AR reconstructs the local level/character mechanics, conditional CellWt/Joint and installed series reading; it retains normalized algebraic adic-character existence and named classification/coefficient-module inputs. The empty-Tw LS stage cannot supply SideB.cover or NChoice.twI. The ColW/Pre2/St/RowPk and MuIsW joins must remain on the same objects.',
 'Supply the actual compatible V4.Core and its geometric volume/mass, layout, recursive and integral comparison fields. A constructed HFrame, same-base coefficient/jet input and bare Later do not identify their real/twist/Obj2 models with the required core. The current source targets record the surviving compatibility conditions.',
 'Prove SiegelMassRatioCM from its genuine representation and local-density mass identities. QW proves the full original window_lower implication, so its numerical reduction need not be reopened. Prove the actual LFam of conductor 4dM^2 with NormOne support and its uniform weighted trivial-class short-interval lower bound. QW supplies the subsequent prime-power removal and uniform norm-prime scale transports, not these two inputs.',
 'Complete the same-data primitive theta-test inputs: compatible FieldOK, analytic convergence, separating functionals, period/unfolding/normalized-jet identities, nonvanishing and tower/ratio statements, and actual positive ThmBop/ThmAop/PartsE/PartsW. TT reconstructs the finite/local coefficient and support arguments and narrows the remaining interfaces. Fixed-field membership is stronger than algebraicity.',
 'Quantitative eigenvalue and chain-norm bounds, AG spectral-word identities, positive-semidefinite kernel/mass normalization and exceptional-word bounds remain. Actual GalD/dimension balance, integral/isometric metric transport and discarded-target control are independent of rational common image and rank equality.',
 'Congruence denominators LinkN/LinkV, two-primary and odd-minus/odd-plus cohomological windows, full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply remain. The bounded-modulus real-zero margin has no uniform all-conductor conclusion.',
]
def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
 raw=data if isinstance(data,list)else data.get('targets',[]);out=[]
 anchor_keys={'source','sources','source_ranges','source_anchors'}
 for item in raw:
  if {'path','line_start','line_end','range_sha256','sha256'}<=item.keys():out.append(item);continue
  anchors=item.get('source_ranges',item.get('sources',item.get('source_anchors',[])))
  if not anchors and isinstance(item.get('source'),dict):anchors=[item['source']]
  assert anchors,('target lacks exact source',item)
  for index,source in enumerate(anchors,1):
   t=dict(source);t.update({k:v for k,v in item.items()if k not in anchor_keys and k not in t})
   t['id']=str(item.get('id',item.get('declaration','target')))+'-'+str(index)
   t['remaining_human_scope']=item.get('remaining_human_scope',item.get('scope',item.get('remaining_scope',item.get('objective',item.get('title','')))))
   out.append(t)
 return out
completed={};candidates=list(prior['targets'])
for component in components:
 d=read(ROOT/component/'next_targets.json');candidates+=flat(d)
 for record in d.get('completed_targets',[])+d.get('closed_source_targets',[]):
  t=dict(record.get('source',{}));t.update(record)
  assert 'path'in t and'declaration'in t,record
  ids=t.get('claims',t.get('closed_by',t.get('completed_by',t.get('supplied_by',[]))))
  ids=ids if isinstance(ids,str)else','.join(ids)
  completed[key(t)]=ids+': '+t.get('reason',t.get('scope',t.get('remaining_human_scope','Conditional endpoint reconstructed with its original inputs retained.')))
# The v0.18 proofs already supplied these bare constructors. Retire only
# the stale generic records, leaving the stronger nonempty/core targets.
for t in candidates:
 if t['declaration']=='GlobalTheory.Mem.PreX':
  completed[key(t)]='IG8–IG10 already constructed the original sized PreX in v0.18. HF now continues that same-object input. Stronger quantitative and compatible-core targets remain separately.'
 if t['declaration']=='GlobalTheory.Mem.Col2.TC.Later':
  completed[key(t)]='LS20–LS22 already constructed bare empty-index NStage/Later in v0.18; the generic retained record was stale. Compatible nonempty NChoice/SideB and V4.Core remain separate targets.'
 # Remove generic construction targets only after their conditional
 # arguments have been reconstructed; keep the suppliers in AR/HF.
 if t['declaration'] in {'GlobalTheory.JointLevel.joint_of','GlobalTheory.JointLevel.joint','GlobalTheory.LevCmp.Joint'}:
  completed[key(t)]='AR11 proves the literal Joint intersection on the supplied compatible MtAd/RatAd/SideB/SerAt/Keep/Elem data; AR21 supplies SerAt.join for the installed reading. Supplying those same actual data, with nonempty all-place coverage, remains in AR-next-06/07/08. This does not prove their unconditional existence.'
 if t['declaration'] in {'GlobalTheory.LevCmp.cellWt_all','GlobalTheory.LevCmp.WtMatch','GlobalTheory.LevCmp.CellWt'}:
  completed[key(t)]='AR12–AR14 prove coefficient-field descent, highest-weight identification and matching matrices under the literal inputs. Complex exists_equiv_VV, canonical mtRatDual_hw, and actual compatible rhoW/parameter/base-change/MtReal fields remain in AR-next-03/04/07.'
 if t['declaration']=='GlobalTheory.Mem.Col2.TC.Pins':
  completed[key(t)]='IG11/SE15/HF18 supply both pins on the same normalized original datum and actual host frame. The literal frame-inclusion antecedent of CA13 for an externally prescribed base and the stronger fixed-context/Core join remain; this is not Pins for an arbitrary base.'
 if t['declaration']=='GlobalTheory.Mem.Col2.InEx.exists_holds':
  completed[key(t)]='TL15 supplies the finite primitive-root/square-root union and HF18 applies it with n=2m before the same Base is assembled. This closes the original ColIn/JetsIn supplier target; it does not put its values in an arbitrarily preassigned field.'
replaced={key(t):completed[key(t)]for t in candidates if key(t)in completed}
scope_updates={}
for t in candidates:
 n=t['declaration'].split('.')[-1]
 if n=='levelPrime_unconditional':scope_updates[key(t)]='QW12 proves the complete uniform levelPrimeN scale transport and actual-host specialization from ShortNorm. Its compatible LFam with conductor 4dM^2/NormOne support and uniform weighted short-interval estimate remain. Qualitative ray-prime existence and finite NoExc do not supply those inputs.'
 if n=='normPrimes_short_interval_lower':scope_updates[key(t)]='QW10–QW11 prove the exact weighted-to-unweighted transport, prime-power error and all resulting constants. The actual compatible LFam and uniform weighted trivial-class short-interval theorem remain; the unconditional endpoint is not discharged.'
 if n=='recExP_of_recAtG':scope_updates[key(t)]='IG13–IG14 prove positive/integer size normalization and the exact threshold/transport join; QW9 now proves the required window_lower from SiegelMassRatioCM. Actual RecAtG/V4.Core/VolumeEqMass2/Lay/RecOK/LedOK, EvP and the substantive global mass law remain.'
updates={}
def add(ids,by,scope):
 for cid in ids:updates[cid]=dict(expanded_by=by,scope=scope)
add(['RC1','RC2','RC14','RC15','RC16','RC17','RC18','RC19','NC6','NC13'],claimids['arithmetic_realization'],'AR supplies the actual local bad-place, level/character and Joint mechanics, conditional CellWt and installed reading. Common global realizations, nonempty normalized-character coverage and named representation-theoretic inputs remain; the original claim is unchanged.')
add(['RC3','RC4','RC10','RC11','RC13','NC9','NC12','NC17','LS20','LS21','LS22'],claimids['arithmetic_realization'],'AR makes the nonempty all-place coverage and same-realization/side/index constraints more explicit. It does not construct compatible nonempty NTw/Loc data or remove the IsGalOf and MuIsW joins.')
add(['IG8','IG10','IG11','IG12','TL14','TL15','SE14','SE16','CI19','CA13'],claimids['host_character_frame'],'HF constructs the actual host-character frame and follows the same-base initial coefficient/jet/bare-stage join. The original historical assertions and hypotheses are preserved; the full compatible geometric core remains separate.')
add(['IG13','IG14','RF10'],['QW1','QW2','QW3','QW4','QW5','QW6','QW7','QW8','QW9'],'QW reconstructs the complete actual numerical window_lower implication, with explicit constant and original quantifier order. SiegelMassRatioCM and the same-object ChOK/du/Ds geometry remain hypotheses.')
add(['TD1','TD2','TD3','TD9','TD10','TD11','TD15','TD16'],claimids['theta_test_inputs'],'TT expands the primitive finite/local theta-test arithmetic and source sum/support deductions. Same-field compatibility, analytic/separation/period/ratio and positive operator/type inputs remain as itemized in the new ledger; the old common-test premises are not silently removed.')
precision=[
 'The new arithmetic reconstruction proves local character and subgroup identities on the actual cell and selected halves. It retains published global reciprocity and normalized algebraic adic-character existence. In particular, type-character comparison uses an all-place coverage field to choose a twist away from each type prime; the empty-Tw stage is insufficient.',
 'AR proves field descent of intertwiners and the ensuing CellWt under two named complex classification/highest-weight inputs. The characteristic-zero equality of Weyl and dual Weyl spaces is separately retained; no integral equality of their lattices is inferred.',
 'The actual series reading is a pointwise formula whose denominator-cleared integral preimage spans. Its equality with CellTie.rdV must be installed. A proof for a newly constructed map is not a proof for an arbitrary pre-existing reading or a complete ExportTie.',
 'HF constructs all actual Hecke-character families on the same host and weights, with unit compatibility and exact local/infinity restrictions. Its initial joins preserve the fixed preliminary datum. Bare Later and the full V4.Core have distinct compatibility requirements.',
 'QW proves the literal conditional window_lower, with C=30+(2+2C0)/epsilon in the logarithmic ratio. It checks all local PlaceData and positivity before taking logarithms. SiegelMassRatioCM is a retained theorem, not inferred from finite positive genus mass.',
 'QW reconstructs weighted-to-unweighted norm-prime counting and uniform levelPrimeN/normPrimesN consequences of ShortNorm. The same-family LFam norm support and uniform weighted interval estimate remain the substantive analytic/arithmetic inputs.',
 'The classical entire-product nonvanishing proof and finite-minimum argument give exactly a real NoExc margin depending on the fixed conductor bound N0. They provide no quantitative dependence on N0, no all-conductor constant and no complex zero-free box.',
 'The initial period-field predicate Per.FieldOK supplied in the HF join is distinct from the common theta-test FieldOK retained in TT. They index different data and cannot be substituted for one another.',
 'TT finite/local rationality statements retain the prescribed common FieldOK; algebraic values alone do not establish membership in a preassigned field. Convergence, separating functionals, compatible periods and nonvanishing/tower/operator identities are kept at their actual source interfaces.',
 'All predecessor claims, source arrays, source-file records, mathematical dependency edges and historical component bytes remain unchanged. Current targets retire completed conditional Joint/CellWt arguments and the original Pins/finite-root-field constructors, as well as stale generic PreX/Later records. The actual simultaneous input supply, external-base frame inclusion and stronger nonempty/core obligations remain. The four global branch records remain unchanged.',
 'Current deliverables are cumulative TeX and updated ZIP. Draft-mode TeX validation creates no PDF and certifies no layout. The historical v0.13 PDF remains preserved. No full Lean build, independent kernel replay or complete RH/Dirichlet-GRH proof is asserted.',
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),completed_previous_frontier='Actual host-character frame; precise conditional local arithmetic realization/weight/series comparisons; primitive finite/local theta-test calculations; complete conditional quantitative mass window and exact prime transports; bounded-modulus real NoExc.',next_local_priority='Compatible nonempty arithmetic/geometric realization and full core; genuine global mass and weighted prime-window suppliers; remaining same-field analytic theta tests and operator identities; four independent global branches.',priority_groups={'1':'Compatible nonempty arithmetic realization, normalized characters and coefficient weights','2':'Compatible geometric core, global mass and weighted quantitative prime windows','3':'Simultaneous prime selection and cohomological/global branches','4':'Remaining same-field theta tests and operator/spectral/metric suppliers'},precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,precision_supersessions=[
 dict(previous_version='0.18',historical_statement='Full host Hecke-character frame remains.',current_statement='HF constructs the actual character families and full HFrame under their literal host hypotheses, then follows the same-base initial join. A compatible V4.Core remains separate.',completed_by=claimids['host_character_frame']),
 dict(previous_version='0.18',historical_statement='window_lower and all norm-prime transport remain.',current_statement='QW proves the complete literal window_lower from SiegelMassRatioCM and the exact weighted/count/scale transports from their explicit analytic/arithmetic inputs. Those genuine inputs remain.',completed_by=['QW9','QW11','QW12','QW13']),
 dict(previous_version='0.18',historical_statement='Generic PreX and bare Later are still targets in parts of the map.',current_statement='These generic target records were stale: IG8–IG10 and LS20–LS22 already supplied them. The current map removes only those records; nonempty arithmetic stages and compatible core obligations remain.',completed_by=['IG10','LS22']),
 dict(previous_version='0.18',historical_statement='Generic Joint/CellWt and original Pins/exists_holds remain reconstruction targets.',current_statement='AR11–AR14 reconstruct Joint/CellWt conditionally and AR21 installs the series join. HF18 joins the original Pins and finite-root field on the same datum. Their actual compatible representation/character inputs, named classification theorems, externally prescribed-base frame inclusion and full Core remain separate requirements.',completed_by=['AR11','AR12','AR13','AR14','AR21','HF18']),
])
cfg['tex_front_summary']=r'''\textbf{What version 0.19 achieves.} The actual host-character frame
and its same-base initial joins are constructed. Local arithmetic level,
character, weight and series comparisons are expanded with their precise
global compatibility and representation-theoretic premises. Primitive
finite theta calculations narrow the remaining test inputs. The original
quantitative mass window is now proved from its stated mass-ratio law;
the prime-counting reductions retain their exact uniform analytic inputs.
Compatible nonempty realizations, the full geometric core, global mass
and weighted prime-window suppliers, remaining theta identities and the
four global branches remain. This is \textbf{a partial human
reconstruction, not yet a self-contained proof of RH or Dirichlet GRH}.'''
cfg['tex_remaining_local']=r'''AR in Section~\ref{sec:arithmetic-realization} supplies the actual
bad-place and selected-half comparisons, tame local readings, parahoric
and type levels, identity-frame reductions and the literal intersection
constructing \texttt{Joint}. It proves coefficient-field intertwiner
descent and conditional \texttt{CellWt}, harmonic/coefficient comparisons,
all \texttt{WtMap} fields and the installed pointwise series reading.
The same nonempty normalized-character and weight data, global realization,
published reciprocity, algebraic adic-character constructor and named
representation-theoretic inputs remain. An installed reading is not an
arbitrary pre-existing \texttt{rdV}.

HF constructs the actual host Hecke-character frame and determinant
data, and continues the original preliminary datum through its common
coefficient and jet choices. The bare local/Galois stages from LS remain
available on that datum. The full compatible \texttt{V4.Core}, including
its real/twist, object, layout and geometric volume identities, remains
separate. A bare empty-index stage cannot supply all-place arithmetic
twist coverage.

TT expands the primitive finite/local theta-test calculations, including
compact integrals, rational coefficients and finite-support/sum arguments.
Its exact field and period interfaces are retained. Compatible
\texttt{FieldOK}, analytic convergence, separating functionals, remaining
period/tower/nonvanishing identities and positive
\texttt{ThmBop/ThmAop/PartsE/PartsW} still require their actual suppliers.
TD's common-image, rational-matrix and metric conclusions retain their
historical hypotheses unless the new claim states precisely how an input
is supplied.

QW in Section~\ref{sec:quantitative-windows} proves the complete
\texttt{window\_lower} implication, with explicit logarithmic constant,
actual Euler products and local indices, and all nine place conditions.
The original \texttt{SiegelMassRatioCM} and same-object geometric size
identities remain premises. QW also proves the exact weighted-to-prime
count and uniform scale transports. Its compatible \texttt{LFam} and
uniform weighted short-interval theorem remain substantive inputs.
The finite-conductor real-zero margin is proved; its constant depends
on the conductor bound. The four independent global branches below
remain as stated.
'''
cfg['tex_next_target']=r'''\paragraph{The next target: the remaining compatible and uniform inputs.}
Continue from the actual host characters and completed conditional
arithmetic/quantitative reductions. Construct nonempty twist and local
data with the same normalized characters, sides, weights, realizations
and \texttt{IsGalOf} readings, then the compatible geometric core.
The empty-index auxiliary stage cannot supply that join.

Reconstruct the genuine mass-ratio producer and the actual arithmetic
\texttt{LFam} together with its uniform weighted interval estimate.
The ensuing window and norm-prime scale calculations are now available
in QW. Complete the same-field analytic, separating, period and operator
theta inputs isolated by TT. Preserve the separate spectral, integral
metric, cohomological, simultaneous-prime and final prime-sum branches.
The current target map records exact pinned declaration ranges and the
remaining scope of each.
'''
cfg['tex_ledger_rows']=[
 span('arithmetic_realization').replace('–','--')+' & Actual local arithmetic realization & Local character/level and Joint proofs; conditional weight descent, harmonic maps and installed series reading.',
 span('host_character_frame').replace('–','--')+' & Actual host-character frame & Character extensions, exact local restrictions, determinant package and same-base initial joins; full core retained.',
 span('theta_test_inputs').replace('–','--')+' & Primitive theta-test inputs & Finite/local rationality and support calculations; same-field analytic and period/operator inputs retained.',
 span('quantitative_windows').replace('–','--')+' & Quantitative windows & Complete conditional mass window, prime-count and scale transports, classical finite-conductor real-zero margin.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For the present increment, start with HF's actual host-character frame
and its same-base initial joins. AR expands the local arithmetic
comparison and identifies its remaining normalized-character,
representation and realization premises. TT expands the primitive
finite/local theta-test inputs used by TD's common-target deductions.
QW proves the quantitative mass window and exact prime-count transports
with their uniform inputs displayed. Read the current remaining-input
section before interpreting historical conditional claims. Individual
proofs can be located by their stable claim IDs and pinned source ledger.
'''
(ROOT/'increment_v0_19.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(map(len,claimids.values())),replaced_target_keys=len(replaced),claim_updates=len(updates)),indent=2))
