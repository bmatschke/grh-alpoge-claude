#!/usr/bin/env python3
"""Describe the v0.18 increment; preserve the predecessor and all conditional scopes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_17'
def read(p):return json.loads(p.read_text())
components=['arithmetic_compatibility','local_stages','initial_geometry','theta_descent']
ledgers={c:read(ROOT/c/'provenance.json')for c in components}
oldcp=read(OLD/'continuation_checkpoint.json');prior=read(OLD/'next_source_targets.json')
scope=('Partial human reconstruction of RH and Dirichlet GRH. Arithmetic scalar extension, actual rank comparison, finite Artin/ring-class character descent, nonempty-local character/conductor compatibility, local parahoric rigidity and the exact conditional choice/tuple join are reconstructed. The actual Fontaine, de Rham and crystalline ring constructions, invariants and fundamental intersection supply LocStage; the bare empty-index NStage and Later are constructed on the same adapted rows. A qualitative ray-prime argument supplies the original sized PreX with exact norm factors, spaces, letters, integer mass-index normalization and pins; the actual chosen-volume empty-jet stage is constructed. Rational theta adjoint/level cuts, common-image and Gram deductions, exact rational row/lift comparisons and common row-test normalization are reconstructed under their explicit tests and operator/type identities. Nonempty choice-compatible stages, actual realization/frame/core suppliers, quantitative mass and prime windows, primitive theta test/operator identities, and the four global branches remain. No complete self-contained RH/GRH proof, full Lean build or independent kernel replay is asserted.')
new=[
 'RC1–RC21: prove finite-evaluation scalar extension and actual RankTie; construct the coefficient-valued Artin character under the stated global reciprocity input and descend through the actual NTw universal map. Prove Frobenius detection, exact conductor/local-character compatibility, coherent side/packet readings and the precise ChoiceSide join. Transport all MuIsW fields on the actual ColW/Pre2/St, and prove the local parahoric, additive-character and nonzero-form arguments yielding LevEq from Joint. Prove the selector under TwCoverPair and the finite integral subbasis/prime-avoidance construction with S chosen before all forbidden sets; actual twisting/full-rank/adm7 inputs remain. Actual realization/weight/frame and compatible nonempty-stage suppliers remain.',
 'LS1–LS22: prove explicit Ax approximation, bounded cyclotomic projections and vanishing of every nonzero Tate-twist invariant, including at 2. Construct the actual Ainf theta map, BdR DVR, divided-power completion embedding, logarithmic period and crystalline ring; prove Frobenius injectivity/fixed ring, the fundamental intersection and exact de Rham/crystalline invariant fields. Check the literal local-stage fields and construct the bare empty-index NStage and Later on the same adapted rows. This model supplies no NChoice or representation comparison.',
 'IG1–IG14: reconstruct imaginary-quadratic ray partial zeta functions by Gaussian Poisson summation; prove nonvanishing at 1 by the entire character-product and nonnegative Taylor argument, hence arbitrarily large prime norms in every ray class. Construct the actual cyclic host, separated auxiliary primes, two-word HC columns, norm factors, diagonal spaces, every original PreX field and positive integer mass-index normalization. Restrict to the source singleton and set its window exactly, obtaining the original exists_pre_sized. Supply orientation/pins and the actual chosen-volume empty-jet stage. Expand the recursive-existence arrow with actual core and quantitative window premises retained.',
 'TD1–TD16: prove fixed-field coordinate recovery, rational theta kernel/adjoint cuts, finite-group and idempotent level descent, and common theta image with its exact Gram factor from positive operator identities. Construct literal rational row/lift matrices, the base-lift relation, quotient-metric spectral orthogonality and the principal Hermitian lattice. Prove one common row-test normalization, including the zero-scalar case, Boolean conjugation transport and uniform threshold order. Actual test convergence/period/rational-ratio and positive theta identity suppliers remain.',
]
remaining=[
 'Construct the same actual nonempty twist/local data needed by NChoice, with its NTw universal ring-class maps, compatible indices/sides and IsGalOf local values; supply the realized MtFam/NExpTied/TwFrameC, Joint and CellWt. RC proves the rank/character/local-level mechanics and actual MuIsW transport, but ColW/Pre2/St/RowPk and their simultaneous compatible existence remain substantive. RC20 gives readings only on twisted places, whereas RC11 needs an all-place reading. RC21 retains aux3/FullRank/adm7 and settings; finite prime avoidance does not prove their lattice-index estimates. The empty-Tw model of LS cannot supply NChoice.twI.',
 'Supply the actual full Hecke-character frame and geometric V4.Core, VolumeEqMass2, Lay/RecOK/LedOK. IG supplies an original sized PreX and exact chosen-volume noJet stage, not VolTieG or a compatible recursive core. Quantitative SiegelMassRatioCM/window_lower, prescribed top/logarithmic windows, LevelPrime and simultaneous prime selection remain; qualitative unbounded ray primes do not give these estimates.',
 'Supply the actual compatible common theta tests (choice/FieldOK, LinK/InjK, Formula2K, SumRatK, RatioK) and positive operator/type identities (ThmBop/ThmAop, PartsE/PartsW, actual HoldsL). TD derives common image, rational matrices and exact metrics from them; quantitative eigenvalue and chain-norm estimates, AG spectral-word identities, positive-semidefinite kernel/mass normalization and exceptional-word bounds remain.',
 'Actual dimension balance/GalD, retained-source integral/isometric metric transport and discarded-target control remain. Equal rank, rational common image and a constructed positive metric do not supply these stronger assertions.',
 'Congruence denominators LinkN/LinkV and two-primary/odd-minus/odd-plus cohomological windows for ordinary and fixed-character hosts remain.',
 'Full simultaneous PairEx prime selection, uniform gain-to-centered-prime-sum and final global parameter supply remain.',
]
def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
    raw=data if isinstance(data,list)else data.get('targets',[])
    out=[]
    anchor_keys={'source','sources','source_ranges','source_anchors'}
    for item in raw:
        if {'path','line_start','line_end','range_sha256','sha256'}<=item.keys():
            out.append(item)
            continue
        anchors=item.get('source_ranges',item.get('sources',item.get('source_anchors',[])))
        if not anchors and isinstance(item.get('source'),dict):anchors=[item['source']]
        assert anchors,('target has no exact source range',item)
        for index,source in enumerate(anchors,1):
            t=dict(source)
            t.update({k:v for k,v in item.items()if k not in anchor_keys and k not in t})
            t['id']=str(item.get('id',item.get('declaration','target')))+'-'+str(index)
            t['remaining_human_scope']=item.get('remaining_human_scope',item.get('scope',item.get('remaining_scope',item.get('objective',item.get('title','')))))
            out.append(t)
    return out
completed={};candidates=list(prior['targets'])
for component in components:
 d=read(ROOT/component/'next_targets.json');candidates+=flat(d)
 for record in d.get('completed_targets',[])+d.get('closed_source_targets',[]):
  # Completed endpoints may carry their exact locator inside ``source``;
  # the completion scope and supplying claims belong to the parent record.
  t=dict(record.get('source',{}));t.update(record)
  assert 'path' in t and 'declaration' in t,('completed endpoint lacks locator',record)
  ids=t.get('claims',t.get('closed_by',t.get('completed_by',t.get('supplied_by',[]))))
  ids=ids if isinstance(ids,str)else','.join(ids)
  completed[key(t)]=ids+': '+t.get('reason',t.get('scope',t.get('remaining_human_scope','Conditional endpoint reconstructed; upstream hypotheses retained.')))
replaced={key(t):completed[key(t)]for t in candidates if key(t)in completed}
scope_updates={}
for t in candidates:
 n=t['declaration'].split('.')[-1]
 if n=='levelPrime_unconditional':
  scope_updates[key(t)]='The quantitative norm-prime interval with uniform constants remains. IG1–IG3 prove qualitative prime norms in every ray class, sufficient for initial existence; IG7 chooses and normalizes an initial window freely. Neither proves the prescribed large-scale LevelPrime window.'
 if n=='Pins':
  scope_updates[key(t)]='IG10 supplies an original sized PreX and IG11 supplies orientation and both coordinate/scalar pins for that constructed datum. An arbitrary externally fixed base/frame is not identified with it; the compatible full frame/core remains a separate source supplier.'
 if n=='recExP_of_recAtG':
  scope_updates[key(t)]='IG13–IG14 reconstruct exact positive/integer size normalization and the same-object threshold/transport join. Actual RecAtG/V4.Core/VolumeEqMass2/Lay/RecOK/LedOK, EvP, and the quantitative window_lower consequence of SiegelMassRatioCM remain substantive.'
updates={}
def add(ids,by,scope):
 for cid in ids:updates[cid]=dict(discharged_by=by,scope=scope)
add(['NC6','NC9','NC12','NC13','NC17'],['RC1','RC2','RC3','RC4','RC5','RC6','RC7','RC8','RC9','RC10','RC11','RC19'],
 'RankTie now follows from actual scalar-extension and exact level/weight predicates; the local LevEq mechanics are expanded through Joint. Finite character descent, coherent readings and the exact conditional choice join are reconstructed under global reciprocity, NTw and the same realization inputs. RC10 proves nonempty-local character/conductor equality from IsGalOf, retaining compatible local index/side. It does not create a choice-compatible nonempty stage.')
add(['NC14','NC15','NC16','TX16','TG12','FC19','VE10','VE11'],['RC12','RC13'],
 'The actual ColW/Pre2/St row lift preserves MuW and supplies all ten MuIsW fields, the exact frame and Q equality, hence the same xi/psi tuple tie. Existence of those simultaneous core/row/character records remains; resetting a bare row tuple does not transport an arbitrary RowPk.')
add(['SE13','SE14'],['LS17','LS18','LS19','LS20','LS21','LS22'],
 'The actual local period construction now supplies LocStage, and every bare NStage field is constructed on the same adapted RowsRest, closing the bare Later join. Its Loc and Tw indices are empty. NChoice.twI on the nonempty coefficient-place type and representation comparison/bridge/quantitative ties remain separate.')
add(['SE12'],['IG12'],
 'The stronger actual baseVol/noJet endpoint is now constructed using the literal positive-choice definition of trueVol and the same compact-dual Haar datum. This does not prove VolTieG or identify the chosen value as a geometric covolume.')
add(['SE15','SE16','CA13','CI19','TL20','TL21'],['IG1','IG2','IG3','IG4','IG5','IG6','IG7','IG8','IG9','IG10','IG11'],
 'An original sized PreX is now constructed, including qualitative norm-prime selection, exact spaces/letters and integer duStarOf normalization. On this same datum, supplied orientation and coordinate/scalar pins are explicit. The arbitrary-base canonical implication is retained; no unrelated frame/base identification or quantitative prime window is inferred.')
add(['PL6','PL7','PL8','PL9','PL10','PL11','PL15','PL18'],['TD1','TD3','TD4','TD6','TD7','TD8','TD9','TD10','TD11','TD12','TD13','TD14','TD15','TD16'],
 'Rational adjoint/level cuts, common row/lift image, exact comparison matrices and Gram/quotient-metric deductions are now proved from explicit common tests and positive theta/type identities. The normalization and conjugation/threshold assembly of RowTest are expanded. Actual tests, period/ratio arithmetic, ThmBop/ThmAop/PartsE/PartsW and quantitative eigenvalue, dimension and integral comparison suppliers remain.')
precision=[
 'Every field of all 747 predecessor claim records, every predecessor source-file record, every old dependency adjacency list and all earlier version-local conclusions is preserved. Current discharges are additive. All 797 predecessor package files remain, with exactly 20 root files archived to history/version_0_17/.',
 'RC scalar extension uses finite separating evaluations to justify the finite coefficient expansion; it does not commute scalar extension with an arbitrary product of function values. RankTie retains the same MtReal/NExpTied and exact LevEq/CellWt.',
 'The Artin-character construction explicitly retains the stated global reciprocity theorem and the actual NTw ring-class universal map. Frobenius detection is proved from that map and weak approximation. Nonempty-local character and conductor ties follow from IsGalOf, but local index/side compatibility must still be supplied.',
 'RC local comparison proves parahoric orientation and additive-character rigidity, then uses an explicit integral frame to construct nonzero forms. Joint and the realized weight/Hecke data remain; an abstract rank equality is not an equivariant or integral isometry.',
 'LS uses the actual perfect inverse limit, Witt ring, theta kernel, divided-power and adic completions and localization. The Frobenius injectivity argument includes the coefficient induction and its completion step. All nonzero Tate twists and the logarithmic integral argument include p=2.',
 'The fundamental local identity is Bcris^{phi=1} intersect BdR+ = Qp. No stronger surjective fundamental exact sequence or comparison theorem for arbitrary geometric representations is inferred. The full bare NStage has empty Loc and Tw; it cannot satisfy NChoice.twI on the nonempty coefficient-place set.',
 'IG proves qualitative ray-prime existence from shifted-lattice partial zeta continuation and an entire nonnegative character-product contradiction. It gives arbitrarily large prime norms, with no asserted short interval, density error estimate or uniform LevelPrime window.',
 'IG constructs two initial word columns and then deliberately restricts to a singleton before replacing duStar by the actual positive integer duStarOf. The initial window endpoint is exact because Ds is chosen to make it so; this does not solve an independently prescribed window.',
 'The integer duStarOf argument uses the finite genus mass definition, finite automorphism groups and an integral Vandermonde determinant; it does not use an analytic Siegel mass formula. The trueVol positive-choice definition gives a positive baseVol even without a VolIs witness, and thus does not prove geometric covolume identification.',
 'TD preserves one fixed coefficient field and one common test family for all tuples. Algebraicity alone cannot substitute for fixed-field membership; the explicit {1,i} over Q counterexample explains the obstruction. The common normalization includes the kappa=0 case without division.',
 'TD common image is proved by theta theta* acting by positive scalars on spanning parts. The actual quotient metric is treated via orthogonal lifts; a coordinate section zE is not assumed isometric. The exact nP factor, inverse lift-level character and distinguished-place splice are preserved.',
 'All four historical global branch records remain unchanged as records; additive annotations identify the downstream parts now expanded. Positive scalar identities and rational comparisons do not establish quantitative bounds, GalD, integral/isometric transport, congruence denominators or prime windows.',
 'Current deliverables are the cumulative TeX and updated ZIP. Draft-mode TeX validation emits no PDF. The v0.13 PDF is preserved as a historical rendering only. No full Lean build, independent kernel replay or complete RH/Dirichlet-GRH proof is asserted.',
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),completed_previous_frontier='Actual conditional arithmetic rank/character/level mechanics; Fontaine local stage and bare NStage/Later; original sized PreX and chosen-volume empty jets; rational theta adjoint/level descent, conditional common image/metric and test normalization.',next_local_priority='Compatible nonempty arithmetic/geometric realization; full frame and recursive core with mass/window bounds; primitive theta tests and positive operator identities; independent quantitative global branches.',priority_groups={'1':'Compatible nonempty arithmetic realization, local comparison and actual character/weight suppliers','2':'Actual frame/core/mass and quantitative prime or logarithmic windows','3':'Simultaneous prime selection and cohomological windows','4':'Primitive theta/test identities and independent spectral/metric/global branches'},precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,precision_supersessions=[
 dict(previous_version='0.17',historical_statement='Full NStage/LocStage is retained in the bare Later join.',current_statement='LS constructs the actual local period rings and LocStage, then the bare empty-index NStage and Later on the same adapted rows. Nonempty NChoice-compatible and representation-comparison suppliers remain.',completed_by=['LS13','LS17','LS21','LS22']),
 dict(previous_version='0.17',historical_statement='Original sized PreX and exact baseVol/noJet are retained.',current_statement='IG constructs original sized PreX from qualitative norm-prime and explicit geometry data, its orientation/pins, and exact chosen-volume noJet. Actual geometric volume, frame/core and quantitative windows remain.',completed_by=['IG10','IG11','IG12']),
 dict(previous_version='0.17',historical_statement='Upstream RankTie/LocsCarry/MuIsW mechanics and theta common-image/rational metric deductions remain.',current_statement='RC expands the actual rank/character/level mechanics and MuIsW transport; TD expands the common-image, rational matrix and exact metric deductions and normalized tests. Their same-object realization, test and positive operator/type premises remain explicit.',completed_by=['RC2','RC10','RC11','RC13','RC19','TD8','TD9','TD13','TD15','TD16']),
])
cfg['tex_front_summary']=r'''\textbf{What version 0.18 achieves.} The arithmetic rank, character
and level comparisons are expanded with their exact compatibility
requirements. The actual Fontaine period rings and local invariants
supply the local stage; a bare Galois stage and the five-stage join are
constructed on the same adapted rows. A qualitative ray-prime argument
now constructs an original sized preliminary input, with exact norm
factors, integer size normalization and pins. Rational theta cuts,
common-image and metric deductions, and the common test normalization
are explicit. Compatible nonempty arithmetic/geometric realizations,
quantitative mass and prime windows, primitive theta test/operator
identities, and the four global branches remain.
This is \textbf{a partial human reconstruction, not yet a self-contained
proof of RH or Dirichlet GRH}.'''
cfg['tex_remaining_local']=r'''RC in Section~\ref{sec:arithmetic-compatibility} now supplies
finite-evaluation scalar extension, the actual rank comparison, finite
Artin/ring-class character descent, coherent readings and the conditional
choice join. It proves local parahoric/character rigidity and nonzero
forms, reducing \texttt{LevEq} to the exact \texttt{Joint} realization.
The same \texttt{MtFam/NExpTied/TwFrameC}, \texttt{CellWt} and actual
\texttt{ColW/Pre2/St/RowPk} suppliers remain. Its nonempty-local criterion
proves character and conductor equality from \texttt{IsGalOf}, while
retaining compatible index and side choices.

LS in Section~\ref{sec:local-stages} reconstructs the actual Fontaine
and period rings, their invariant fields and the fundamental intersection.
It supplies \texttt{LocStage}, the bare empty-index \texttt{NStage},
and \texttt{Later} on the same adapted rows. The construction's empty
twist type cannot supply \texttt{NChoice.twI}; arbitrary representation
comparison, nonzero projectors and quantitative estimates remain separate.

IG in Section~\ref{sec:initial-geometry} constructs an original sized
\texttt{PreX}, including qualitative ray-prime existence, exact factors,
spaces, letters and positive integer \texttt{duStarOf}. The source
singleton restriction makes its initial window exact. Both pins hold
on that datum with the prescribed orientation. Its \texttt{baseVol/noJet}
construction uses the literal positive-choice definition, which does
not prove geometric \texttt{VolTieG}. The full Hecke-character frame,
actual \texttt{V4.Core/VolumeEqMass2/Lay/RecOK/LedOK}, quantitative
\texttt{window\_lower}, \texttt{LevelPrime}, and the other prescribed
prime/logarithmic windows remain.

TD in Section~\ref{sec:theta-descent} supplies fixed-field rational
adjoint/level descent, common theta image and exact Gram deductions,
literal row/lift matrices, quotient-metric orthogonality and the
principal Hermitian lattice. Its normalization constructs common
\texttt{RowTest} from the supplied convergence, separation, period,
finite-sum and ratio statements, with a separate zero-scalar branch.
The actual tests and positive \texttt{ThmBop/ThmAop/PartsE/PartsW}
suppliers, quantitative eigenvalue estimates, \texttt{GalD} and integral
comparison controls remain. All earlier local constructions and exact
conditional joins are preserved. The four global branches below remain
independent. \textsf{[RC1--21, LS1--22, IG1--14, TD1--16]}
'''
cfg['tex_next_target']=r'''\paragraph{The next target: compatible realizations and quantitative suppliers.}
Use the completed local period construction and initial sized geometry
without reopening their elementary suppliers. The next arithmetic join
must build nonempty twist/local data compatible with the same actual
character, side, tuple, realized form spaces and \texttt{Joint/CellWt}.
A bare stage with empty twists is insufficient.

Follow the actual full-frame and \texttt{V4.Core} producers, their mass
and volume identities, and the quantitative logarithmic and norm-prime
windows. In parallel reconstruct the actual convergent common theta
tests, finite period formula, coefficient ratios and positive theta
operator/type identities now isolated by TD. Preserve the separate
spectral, metric, cohomological and simultaneous-prime global branches.
The next-target ledger gives the exact pinned declaration ranges.
'''
cfg['tex_ledger_rows']=[
 'RC1--21 & Actual arithmetic compatibility & Scalar extension, character descent, choice/tuple joins, local level rigidity and finite integral/avoidance choices; realization and twisting inputs retained.',
 'LS1--22 & Actual periods and bare Galois stages & Witt/theta/de Rham/crystalline constructions, invariants and fundamental intersection; exact empty-index NStage and Later.',
 'IG1--14 & Original sized geometry & Qualitative ray primes, explicit host/factors/spaces/letters, integer mass index, original PreX and chosen-volume jets; quantitative core/windows retained.',
 'TD1--16 & Rational theta targets and metrics & Adjoint/level descent, conditional common image and exact matrices/metric, common test normalization; primitive theta identities retained.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For the present increment, RC expands the actual arithmetic rank,
character and level comparisons; read its retained realization premises
together with the exact conditional choice join. LS constructs the
period rings and the bare local/Galois stages, ending with the explicit
empty-twist compatibility boundary. IG supplies the original sized
preliminary input and exact chosen-volume stage, then isolates the
actual recursive core and quantitative window requirements. TD gives
the rational theta cuts, common target and metric, followed by the
normalization supplying tests from their explicit period premises.

The preceding VI/CA vacuum, algebraic-jet and covariance proofs remain
available. NC supplies normalized local choices and exact tuple records;
SE supplies restricted lattices, other bare stages and the coordinate
normal form. AH/PA/TA/CI/TX supply host, periods, one-dimensional theta,
indices and all-twist geometry, and RF/PN/SZ/AC supply numerical and
conditional constructors. Historical proof text and hypotheses are
preserved; current discharge annotations are additive.
'''
(ROOT/'increment_v0_18.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(len(d['claims'])for d in ledgers.values()),completed_target_keys=len(replaced)),indent=2))
