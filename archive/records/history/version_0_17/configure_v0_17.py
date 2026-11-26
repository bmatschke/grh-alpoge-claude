#!/usr/bin/env python3
"""Record the v0.17 increment and its exact conditional boundaries."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_16'
def read(p):return json.loads(p.read_text())
components=['vacuum_identity','canonical_analytic','arithmetic_choice','stage_existence']
ledgers={c:read(ROOT/c/'provenance.json')for c in components}
oldcp=read(OLD/'continuation_checkpoint.json');prior=read(OLD/'next_source_targets.json')
scope=('Partial human reconstruction of RH and Dirichlet GRH. The actual multidimensional vacuum, four-copy identity, rational-translate algebraic jets, normalized finite indicator and exact covariance are now reconstructed, including the signed finite-intertwiner and Gaussian determinant phase. The finite-algebraicity and canonical EvLg joins retain their literal raw PreX/frame antecedents. Finite complete-DVR readings, all NChoice and TupTied fields are constructed under the precise RankTie, LocsCarry, MuIsW and coverage interfaces. Restricted Hermitian lattices and DivStage, actual Fits/RowsRest, ordinary local/SStage, compact-dual Haar and bare GJStage are constructed. Pins are normalized from an existing sized input; Later still requires the full NStage on the same adapted rows, with its local period-ring suppliers. Analytic prime/window and geometric input existence, the remaining arithmetic ties, and four independent global branches remain. No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.')
new=[
 'VI1-VI11: identify the actual trace-dual full period lattices and semicharacter; prove all StdOK inputs, finite Fourier inversion and the positive-Iop mean isometry; construct the actual four-copy vacuum and its scalar-root normalization. Prove algebraic germs for every rational translate directly from that identity, then actual rectangular thZero/thMoved, ESmooth and normalized JetAlg using the independent finite indicator formula CA2.',
 'CA1-CA13: expand the normalized finite indicator with exact coefficient and support bounds. Prove the Hermitian norm Gauss sum, signed intertwiner composition and even-rank identification with actual positive Iop; compute the rational-unitary phase by a Gaussian trace and prove its Gauss factor nonnegative. Derive all three covariance laws and the same-data FinAlg/EvLg joins through host-level ambient definitions, without constructing unused NStage/LocStage fields.',
 'NC1-NC17: construct finite complete-DVR readings with the exact prescribed coefficient prime and valuation normalization; compare full lattices by free local bases; check all21 NChoice fields and the exact normalized packet. Prove coherent character descent and all5 NChTie fields under LocsCarry/RankTie; construct all12 TupTied fields from the exact finite conjugation-stable MuIsW support; join TX16 on the same Q,xi,psi and frame. RankTie, LocsCarry, MuIsW and coverage suppliers remain explicit.',
 'SE1-SE16: prove coefficient-field common-kernel descent, explicit restricted Hermitian frames and full intersection lattices, then all14 DivStage fields on the actual ramified lattice. Construct actual Fits and the RowsRest model; ordinary local completions and all9 SStage fields; all4 CDHaar normalization fields and bare GJStage. Prove the zero-idempotent/adapt calculation, a Later join conditional on NStage for that same adapted W, and both coordinate/scalar pins for an existing sized input.',
]
remaining=[
 'Supply the upstream arithmetic ties used by NC: RankTie from the actual Mt realization and local model, LocsCarry for the same descended character, and MuIsW/TwCover or ReadElsewhere with the exact finite support, Q and xi. The completed NChoice/TupTied constructions do not create these stronger interfaces. TX16 and NC17 join the all-twist comparison once they hold.',
 'Reconstruct the complete NStage on the exact chosen RowsRest, including actual LocStage/Fontaine period rings and tied comparisons. SE supplies the other bare Later fields and the adaptation/idempotent steps. The degenerate auxiliary stage models do not themselves establish quantitative estimates or the NChoice-compatible arithmetic interfaces.',
 'Supply the initial sized/oriented PreX and compatible geometric construction before the SE pins normal form and the CA canonical EvLg implication. The analytic prime and top/logarithmic windows, LevelPrime, and actual Lay/RecOK/LedOK/RecExP with mass/window bounds remain. AH constructs the host only under its prescribed simultaneous q,d and splitting hypotheses.',
]+oldcp['remaining_major_inputs'][3:]
def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
 out=[]
 for t in data if isinstance(data,list)else data.get('targets',[]):
  if'path'in t:out.append(t)
  else:
   for j,s in enumerate(t.get('sources',t.get('source_anchors',[])),1):
    x=dict(s);x.update({k:v for k,v in t.items()if k not in ['sources','source_anchors']and k not in x});x['id']=str(t.get('id','target'))+'-'+str(j);x['remaining_human_scope']=t.get('scope',t.get('remaining_scope',t.get('title','')));out.append(x)
 return out
completed={};candidates=list(prior['targets'])
for component in components:
 d=read(ROOT/component/'next_targets.json');candidates+=flat(d)
 for t in d.get('completed_targets',[])+d.get('closed_source_targets',[]):
  ids=t.get('claims',t.get('closed_by',t.get('completed_by',[])));ids=ids if isinstance(ids,str)else','.join(ids)
  completed[key(t)]=ids+': '+t.get('reason',t.get('scope',t.get('remaining_human_scope','Literal conditional endpoint reconstructed.')))
completed['src/Formalism/LocalRingCardinality/DataNChoice.lean:NChoice']='NC9,NC13,NC17: all21 record fields and exact normalized packet recovery are reconstructed under the actual reading and RankTie premises. The upstream simultaneous rank/character/support suppliers are separately targeted; the old generic finite-DVR construction target is discharged.'
replaced={key(t):completed[key(t)]for t in candidates if key(t)in completed}
scope_updates={}
for t in candidates:
 n=t['declaration'].split('.')[-1]
 if n=='recExP_of_recAtG':scope_updates[key(t)]='Actual RecAtG/Lay/RecOK/LedOK, mass and analytic windows remain. VI/CA now supply the primitive vacuum/indicator/covariance and conditional canonical finite-algebraicity; NC supplies precise conditional arithmetic choices/tuples; SE supplies restricted lattices and bare auxiliary stages and pins normal form. None supplies the initial geometric point.'
 if n=='levelPrime_unconditional':scope_updates[key(t)]='Analytic short norm-prime interval with uniform constants remains. Reuse AC conditional level construction and AH conditional host; the local theta/covariance/stage work does not select this prime.'
 if n=='Pins':scope_updates[key(t)]='CA13 retains the exact arbitrary-base frame-inclusion antecedent. SE15-SE16 construct both pins in coordinate/scalar normal form from an existing sized/oriented input; that initial input and its compatible later base remain substantive. No raw frame identity is inferred from norm equality.'
updates={}
def add(ids,by,scope):
 for cid in ids:updates[cid]=dict(discharged_by=by,scope=scope)
add(['TL18','TL19'],['VI3','VI7','VI8','VI9','VI10','VI11','CA2','CA9','CA11'],'The actual StdOK, four-copy vacuum, all rational-translate algebraic jets, normalized finite indicator and covariance are now supplied. Formal finite-generation reductions are preserved; CA11 supplies the literal same-ambient FinAlg conclusion without using the full Later stage.')
add(['TL20','TL21','CI19'],['CA12','CA13','SE15','SE16'],'The remaining canonical analytic supplier is reconstructed and joined on the same ambient, selector, xi range and modulus. Literal PreX and frame-inclusion antecedents remain in the EvLg implication; SE gives the frame/scalar normal form only from an existing sized input. Later is an independent supplier.')
add(['TX16','TG12','FC19','VE10','VE11','CS4','CS5','CS6','CS7','CS8','CS9','SF7','CR6'],['NC9','NC12','NC16','NC17'],'Finite complete-DVR readings and the literal NChoice/NChTie/TupTied records are now constructed with their exact same-object joins. The upstream RankTie, LocsCarry, MuIsW and coverage hypotheses retain their substantive scope; arbitrary lattice isomorphisms are not Hecke or metric identifications.')
precision=[
 'All690 predecessor claim records and every original field, source array, source-file record and graph adjacency list remain unchanged. New discharge annotations are additive; all729 predecessor package files are preserved.',
 'VI identifies the actual g, correction kappa, trace-dual lattice and multiplier, proves StdOK and finite nonvanishing, and extracts fourth roots of scalar derivatives. It never assumes a global analytic pointwise fourth-root branch, divides by a possibly zero vacuum value, or uses continuity of an arbitrary algebraic embedding.',
 'CA2 finite indicator algebra and coefficient bounds are independent of VI11 and final FinAlg. VI11 depends on CA2 only; CA11 then uses the supplied VI11 result. This direction is acyclic.',
 'The signed finite intertwiner must use the negative Hermitian norm Gauss sum at conjugation-fixed residue primes. Even opposite rectangular rank cancels those signs for the actual one-factor moves. Theta-line uniqueness leaves a phase; CA6-CA8 compute it by Gaussian trace, finite-sum positivity and exact determinant powers.',
 'CA uses the host-level ambient definitions and their literal restriction identities to avoid constructing an unused full Stages datum. The actual I, ambient periods, finite selector, xi range, same modulus and degree tie remain fixed in the canonical join. Its original PreX/frame premises are retained.',
 'NC uses finite complete-DVR integral closures and Galois prime alignment at the exact coefficient place. Full local lattices of equal rank can be identified abstractly, but that identification does not imply Hecke intertwining or metric compatibility. RankTie and LocsCarry remain explicit.',
 'NC MuIsW supplies an exact finite conjugation-stable support and exact equalities on and off Q. Finite character readings alone do not supply it. The same descended psi0, selected Q, xi and frame occur in the comparison join.',
 'SE scalar extension proves the actual common-kernel identity, and the lattice restriction uses Noetherian finite generation plus denominator clearing. It assumes no global O_K freeness. All DivStage fields and the exact ramL image are checked.',
 'SE proves all four CDHaar fields, including common finite positive exponential-chart density, rather than invoking existence of arbitrary Haar measures as sufficient. Bare GJStage uses empty situations and constant positive volume; the specific trueVol identification and nonempty-jet estimates remain separate.',
 'RowsRest and SStage have explicit auxiliary models. The source adapt operation changes eOp,eMt,eta and shaLen on that row object; an NStage must be for the exact adapted object. Its particular empty-Tw NStage construction cannot supply NChoice.twI on the nonempty coefficient-place set. Extended-natural toNat does not prove finiteness of Sha. Ordinary local completions do not supply Fontaine period rings.',
 'Pins.iX and Pins.cof are proved as a coordinate and scalar normal form from an existing sized/oriented input. Their normalization does not prove the original geometric or analytic existence input.',
 'Named standard background includes number-field completion/ideal theory, finite-dimensional linear algebra and change of variables, and ordinary Haar existence/uniqueness. No full Lean build, independent kernel replay, complete RH/Dirichlet-GRH proof, or new PDF visual review is asserted.',
 'Current deliverables are cumulative TeX and updated ZIP. Draft-mode TeX validation emits no PDF. The preserved v0.13 PDF is historical and lacks every increment after v0.13.',
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),completed_previous_frontier='Actual vacuum/four-copy, rational-translate germs, normalized indicator and covariance, FinAlg and conditional canonical EvLg; finite-DVR NChoice/NChTie and exact-support TupTied conditional suppliers; DivStage/RowsRest/SStage/CDHaar/bare GJStage; Pins normal form.',next_local_priority='Upstream RankTie/LocsCarry/MuIsW and choice-compatible stages; full NStage/LocStage; initial geometric input and analytic prime/windows; four independent global branches.',priority_groups={'1':'Arithmetic ties and exact compatible Galois/local period stages','2':'Geometric sized input, actual volume and analytic top/logarithmic/level windows','3':'Simultaneous prime selection and host/cohomological windows','4':'Independent spectral, metric, cohomological and global prime-sum branches'},precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,precision_supersessions=[
 dict(previous_version='0.16',historical_statement='Actual StdOK/four-copy vacuum, normalized indicator and covariance remain.',current_statement='VI and CA reconstruct these actual suppliers, including phase normalization, then the same-ambient FinAlg and conditional EvLg joins.',completed_by=['VI7','VI11','CA9','CA11','CA13']),
 dict(previous_version='0.16',historical_statement='NChoice/TupTied construction remains.',current_statement='NC constructs those literal records from finite-DVR readings and exact upstream RankTie/LocsCarry/MuIsW/coverage interfaces; those interfaces remain substantive.',completed_by=['NC9','NC12','NC16','NC17']),
 dict(previous_version='0.16',historical_statement='Pins.iX and all five Later stages remain.',current_statement='SE supplies the coordinate/scalar pins normal form, actual restricted DivStage, Fits/RowsRest, ordinary local/SStage, CDHaar/bare GJStage and a precise Later join conditional on full NStage for the same adapted rows. Initial sized geometry, NStage/LocStage and quantitative ties remain.',completed_by=['SE6','SE8','SE10','SE11','SE12','SE14','SE16']),
])
cfg['tex_front_summary']=r'''\textbf{What version 0.17 achieves.} The actual multidimensional
vacuum, four-copy identity and all rational-translate algebraic jets are
now constructed. The normalized indicator and covariance are proved with
their exact finite-intertwiner sign and Gaussian determinant phase, then
joined to the canonical finite-algebraicity argument. Finite complete-DVR
readings and the normalized choice/tuple records are constructed under
their precise rank, character and support ties. Restricted Hermitian
lattices and several later-stage records, including the compact-dual Haar
normalization, are explicit. The pins are put in coordinate normal form.
The full Galois/local-period stage on the same rows, upstream arithmetic
ties, initial geometric and analytic-window inputs, and four global
branches remain. This is \textbf{a partial human reconstruction, not
yet a self-contained proof of RH or Dirichlet GRH}.'''
cfg['tex_remaining_local']=r'''VI in Section~\ref{sec:vacuum-identity} now supplies the actual
trace-dual full lattices, \texttt{StdOK}, nonzero four-copy vacuum and
algebraic germs of every rational translate. CA in
Section~\ref{sec:canonical-analytic} supplies the normalized indicator,
finite signed intertwiners, exact determinant phase, all covariance laws,
and the same-ambient finite-algebraicity/canonical \texttt{EvLg} join.
The last implication retains its raw \texttt{PreX} and frame-inclusion
antecedents; unused full \texttt{Stages} fields are bypassed through the
literal host-level ambient definitions.

NC in Section~\ref{sec:arithmetic-choice} constructs finite complete-DVR
readings, \texttt{NChoice}, coherent \texttt{NChTie} and the exact-support
\texttt{TupTied}, then joins TX16 on the same $Q,\xi,\psi$ and frame.
Its upstream \texttt{RankTie}, \texttt{LocsCarry}, \texttt{MuIsW} and
coverage interfaces remain substantive. An abstract local lattice
isomorphism is not an identification of Hecke actions or metrics.

SE in Section~\ref{sec:stage-existence} supplies the actual restricted
ramified lattice and \texttt{DivStage}, \texttt{Fits}/\texttt{RowsRest},
ordinary local and \texttt{SStage} data, compact-dual Haar and bare
\texttt{GJStage}. Its five-stage join retains a full \texttt{NStage}
on the exact adapted rows, with its Fontaine period-ring suppliers.
The zero projections, zero spectral terms and empty jets in these
auxiliary models establish no later quantitative assertion. Both pins
are normalized from an existing sized/oriented input; that input is
still required.

AH/PA/TA/CI/TX and PN/SZ/AC remain available with their proved scopes.
Analytic simultaneous prime selection, top and logarithmic windows,
\texttt{LevelPrime}, and the actual geometric
\texttt{Lay/RecOK/LedOK/RecExP} with mass/window estimates remain.
These local constructions do not discharge the four global branches below.
\textsf{[VI1--11, CA1--13, NC1--17, SE1--16]}
'''
cfg['tex_next_target']=r'''\paragraph{The next target: arithmetic ties and compatible global stages.}
Continue with the exact \texttt{RankTie}, \texttt{LocsCarry} and
\texttt{MuIsW}/coverage suppliers used by NC. They must hold on the
same row, Galois, character and selected-prime data. Separately reconstruct
the full \texttt{NStage} and \texttt{LocStage} suppliers; ordinary local
completions and a degenerate auxiliary model cannot replace their ties.

Use the completed analytic vacuum/covariance and canonical finite-field
construction without reopening those primitive calculations. Continue the
initial sized geometric input, analytic prime and top/logarithmic windows,
and actual mass/volume identifications. Preserve the independent spectral,
metric, cohomological and simultaneous-prime global branches. The exact
declaration ranges and retained scopes are in the next-target ledger.
'''
cfg['tex_ledger_rows']=[
 'VI1--11 & Actual vacuum and algebraic germs & Trace-dual lattices, StdOK, Fourier inversion, normalized four-copy root, all rational translates and actual indicator jets.',
 'CA1--13 & Exact covariance and canonical algebraicity & Finite indicator bounds, signed intertwiners, Gaussian phase, all equivariance laws and same-data FinAlg/EvLg.',
 'NC1--17 & Normalized arithmetic choices & Complete-DVR readings, local lattice comparisons, all choice/character-tie/tuple fields; RankTie and exact support interfaces retained.',
 'SE1--16 & Restricted lattices and stage existence & Common-kernel descent, DivStage, row/spectral/Haar/jet models, conditional Later and pins normal form; NStage and geometric input retained.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For the present increment, VI constructs the actual vacuum and algebraic
translates; CA computes the normalized indicator and covariance phase and
joins finite algebraicity and canonical indices. CA2 is independent of
VI11, which uses it; the final CA join then uses VI11. This is the intended
dependency order, even where the text makes a forward reference.

NC constructs the normalized local arithmetic choices and exact-support
tuple used by TX16. Read its retained \texttt{RankTie}/\texttt{LocsCarry}/
\texttt{MuIsW} inputs together with its final same-object join. SE gives
restricted lattices, auxiliary later-stage constructions and pins normal
form; its last paragraphs state the exact remaining Galois and geometric
inputs. Earlier AH/PA/TA/CI/TX supply host, periods, one-dimensional theta,
indices and all-twist geometry; RF/PN/SZ/AC supply numerical and conditional
point constructors. The new ledgers preserve every predecessor proof and
dependency, with additive annotations for discharged inputs.
'''
(ROOT/'increment_v0_17.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(len(x['claims'])for x in ledgers.values()),completed_target_keys=len(replaced)),indent=2))
