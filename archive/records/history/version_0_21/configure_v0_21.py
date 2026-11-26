#!/usr/bin/env python3
"""Describe the v0.21 increment, retaining all historical proof records."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent; OLD=ROOT/'history/version_0_20'
def read(p):return json.loads(p.read_text())
components=['nonempty_realization','canonical_weil','geometric_volumes','centered_character_sums']
ledgers={c:read(ROOT/c/'provenance.json')for c in components}
claimids={c:[x['id']for x in d['claims']]for c,d in ledgers.items()}
def span(c):return claimids[c][0]+'–'+claimids[c][-1]
prior=read(OLD/'next_source_targets.json')
scope=('Partial human reconstruction of RH and Dirichlet GRH. This increment constructs the nonempty coefficient family indexed by every finite prime of the fixed coefficient field, complete coefficient towers, universal finite anticyclotomic quotients and readings inducing every prescribed full-field place; its bounded integral row representations retain GalEx, RowCusp and ChebSplit. It constructs the canonical finite and real Weil actions on the actual theta space, proves the rational pullback identity by exact finite and real phase cancellation, and supplies full bottom-Weil data and prescribed-character adjustments. It identifies the actual normalized adelic quotient volumes and their mass/trueVol/stage consequences, explicitly conditional on the precisely normalized classical unitary Tamagawa-number theorem; Hasse–Minkowski remains named for UnitSplit. It proves the actual Dirichlet analytic inputs, exact centered integral identities and uniform QH.thin/ThinH under the original real-zero exclusion/RealBox hypotheses. Genuine form realization and compatible nonempty local stages, the remaining full Core and discrete-series/formal-degree inputs, quantitative theta dictionaries, critical ratio fields and exact Choice joins, and the independent global/cohomological/simultaneous-prime branches remain. This is not a complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay.')
new=[
 span('nonempty_realization')+': construct the actual nonempty TwR/RingSpec family on all finite primes of the fixed coefficient field, its complete unramified/cyclotomic coefficient towers, normalized characters and finite universal anticyclotomic quotients. Prove the exact SideB.cover coefficient clause and a Reading inducing every prescribed full-field place. Prove finite coefficient descent and stable integral lattices for compact representations, and the literal bounded rho_rows supplier under GalEx/RowCusp/ChebSplit. Preserve the fixed D, global fields, rows and embeddings.',
 span('canonical_weil')+': construct the finite lattice action, its signed Gauss normalization and crossed splitting character; construct the real oscillator by convergent Gaussian projectors with exact determinant phase and verified smooth domain. Prove finite-real commutation, pointwise continuity and a norm-sensitive scalar lemma. Evaluate the actual Gaussian theta test and cancel the rational finite/real phase to get the full rational pullback identity. Supply canonical and prescribed-character full Weil data, and the previously conditional standard bottom-Weil construction.',
 span('geometric_volumes')+': construct the actual normalized Haar measures and fundamental domains; compute all finite and real gauge constants including the dyadic factor and compact-dual density. Prove the definite quotient-to-genus-mass identity directly. Using the explicitly retained classical unitary Tamagawa-number theorem, derive the exact positive quotient volume, signature independence, VolumeEqMass2, trueVol and same-stage VolTieG. Prove UnitSplit using the inherited Hasse–Minkowski input, the precise volume ratio, trueScale and conditional RealTied/Core joins with the separate discrete-series/formal-degree premises retained.',
 span('centered_character_sums')+': reconstruct primitive Dirichlet completion, local zero counts, the zero-free strip with its real exception and the exact floor-endpoint explicit formula. Identify both centered constants and prove G0=-y integral psi0/u^2. A uniform tail argument supplies QH.thin and the actual same-host ThinH implication from RealBox. Add a derivative/increment estimate above the same exponential cutoff. Do not infer the distinct polynomial-window square-root estimates, PairEx or relative progression theorem.',
]
remaining=[
 'Install the new all-prime ring family into genuine compatible form and local data on the same D: TwF/TwL, MtFam/MtReal/MtAd/MtInput, full SideB, normalized residual/Hecke/tame agreements and nonempty LocsCover, followed by the exact NChoice/ColW/Pre2/St/RowPk joins. NR supplies coefficient coverage and inducing readings, not these form realizations. Global Artin reciprocity, GalEx, RowCusp and ChebSplit remain explicit inputs where used.',
 'Complete the same-object V4.Core with its layout, recursive/integral comparisons, forced primes and conductor-support/exponent identities. GV supplies actual geometric volumes and scale; its global volume theorem still uses the named unitary Tamagawa-number theorem. DiscreteSeriesExist and FormalDegreeFormula2 remain substantive separate inputs for the middle RealTied fields. Hasse–Minkowski remains named for UnitSplit and the earlier mass proof.',
 'Prove the stronger quantitative all-embedding/finite-unit DictAt dictionary, critical ToricRatioConjugates field and the exact same-embedding/frame/family Choice.FieldOK join. The canonical full Weil existence, qualitative finite arithmetic, normalized jets and supplied-bottom periods are available; the universal IsEtaTilde bridge via GlobalNormIndexTwo is not silently claimed by the actual-character bypass.',
 'Complete the remaining theta analytic convergence, separating functionals, nonvanishing/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs with their literal data. Full Weil automorphy does not prove these analytic/operator inequalities.',
 'Complete independent chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control. Equality of rational spans or ranks remains insufficient for these estimates.',
 'Complete congruence denominators LinkN/LinkV and the two-primary and odd-minus/odd-plus cohomological windows, preserving the exact source objects and quantifiers.',
 'Construct simultaneous PairEx choices and RealBox on the actual selected host; prove the stronger relative progression estimate and the uniform gain-to-centered-prime-sum/final parameter chain. CC now supplies ThinH conditional on RealBox and controls all later exponential-cutoff endpoints, but it does not supply the different polynomial-window mean-square/zero-density estimates.'
]
def key(t):return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
 raw=data if isinstance(data,list)else data.get('targets',data.get('next_targets',[]));out=[]
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
completed={}; candidates=list(prior['targets']);retained_new_keys=set()
for component in components:
 d=read(ROOT/component/'next_targets.json'); current_targets=flat(d);candidates+=current_targets
 retained_new_keys.update(key(t)for t in current_targets)
 records=[]
 for name in ['completed_targets','closed_source_targets','completed_endpoints','conditionally_reconstructed_targets']:
  records+=d.get(name,[])
 for record in records:
  if {'path','declaration'}<=record.keys():anchors=[record]
  elif isinstance(record.get('source'),dict):anchors=[record['source']]
  else:anchors=record.get('sources',record.get('source_ranges',record.get('source_anchors',[])))
  assert anchors,(component,record)
  for anchor in anchors:
   t=dict(anchor);t.update({k:v for k,v in record.items()if k not in t})
   assert 'path'in t and'declaration'in t,(component,record)
   ids=t.get('claims',t.get('claim_ids',t.get('closed_by',t.get('completed_by',t.get('supplied_by',t.get('reconstructed_by',[]))))))
   ids=ids if isinstance(ids,str)else','.join(ids)
   reason=t.get('reason',t.get('scope',t.get('remaining_human_scope',t.get('statement','Conditional endpoint reconstructed with its original hypotheses retained.'))))
   conditions=t.get('conditions',[])
   if conditions:reason+=' Conditions retained: '+'; '.join(conditions)
   if t.get('retained'):reason+=' Explicit remaining suppliers: '+'; '.join(t['retained'])
   completed[key(t)]=ids+': '+reason
replaced={key(t):completed[key(t)]for t in prior['targets']if key(t)in completed and key(t)not in retained_new_keys}
# A literal completed helper remained as an older auxiliary anchor. Its
# stronger supplied-host and quantitative joins have separate current targets.
bottom_chars_key='src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/BottomExistsIntegrable.lean:bottom_chars'
assert any(key(t)==bottom_chars_key for t in prior['targets'])
replaced[bottom_chars_key]='WA17, CW24, CW25: the exact parity/rank bottom character restrictions and the required new full Weil representations are now supplied, yielding actual standard bottom families. Host/grid existence and quantitative dictionary, critical-ratio and Choice joins remain separate current targets.'
scope_updates={};optional_source_route_keys=[]
for t in candidates:
 n=t['declaration'].split('.')[-1]
 if n in {'suppSplit_algComb','rat_real_algComb','exists_rep_suppSplit'}:
  optional_source_route_keys.append(key(t))
  scope_updates[key(t)]='Optional auxiliary source-route expansion. WA11 already supplies the generic finite-Weil algebraic span, WA14 the normalized jet field and WA16 the supplied-bottom period field. CW now supplies the canonical full finite/real Weil datum and actual prescribed-character bottom constructions. These older auxiliary split-support arguments are not missing prerequisites for those endpoints. Quantitative DictAt, critical ratio fields and exact Choice joins remain.'
 if n=='recExP_of_recAtG':
  scope_updates[key(t)]='IG13–IG14 supply threshold transport, QW9 the conditional mass window, and MF19 its mass law using classical Hasse–Minkowski. GV now supplies the actual normalized volume identities and trueVol stage, conditional on the named Tamagawa-number theorem. Same-object RecAtG/V4.Core/Lay/RecOK/LedOK and EvP still require their remaining fields.'
 if n in {'Choice','FieldOK'}and'Theta'in t['path']:
  scope_updates[key(t)]='WA and CW supply qualitative finite-Weil arithmetic, NFJet, supplied-bottom SumsIn and canonical/prescribed-character full bottom-Weil data. Stronger quantitative DictAt, critical ratio fields and the literal same-embedding/frame/family Choice join remain. These are the current target scopes.'
# Narrow inherited anchors to their stronger installation joins. Their source
# declarations remain useful navigation points, but the coefficient and full
# Weil existence suppliers are no longer future work.
for t in candidates:
 n=t['declaration'].split('.')[-1]
 tid=str(t.get('id',''))
 if tid.startswith('GA-next-02') or (n in {'Reading','Induces','nonempty'} and 'CharpolySmulOfProd.lean' in t['path']):
  scope_updates[key(t)]='NR14–NR18 now construct the all-prime TwR/RingSpec coefficient family, exact SideB.cover coefficient clause and a Reading inducing every prescribed full-field place on the fixed D and value fields. Retain the supplied fixed-field ValLL0 containment and install this family and its readings into the genuine same-object TwF/TwL, Mt/form/local data and the remaining SideB fields; these stronger joins are the remaining scope of this anchor.'
 if tid.startswith(('AR-next-06','RC-next-02')) or (n in {'TwCover','RCG/art/art_univ','TwCoverPair','ReadElsewhere','readElsewhere_of_cover'} and ('LevelLetterCocycles/' in t['path'] or 'ExistsTiedChoiceOfReads.lean' in t['path'] or 'LocalRingCardinality/DataTies.lean' in t['path'])):
  scope_updates[key(t)]='NR now supplies the actual finite universal RCG quotients, roots, normalized coefficient characters, nonempty all-prime TwR/RingSpec and full-place inducing readings. What remains is their exact installation into a single genuine NTw/form/local package, with the selected indices, sides, existing TwF/TwL/Mt data and residual/tame compatibility. TwCoverPair alone still expresses twisted-place coverage, and the rest of full SideB is retained; the coefficient-cover construction itself is no longer missing.'
 if n=='bottom_chars' and 'BottomExistsIntegrable.lean' in t['path']:
  scope_updates[key(t)]='CW24–CW25 now supply the additional full Weil representations with the exact parity-twisted bottom characters and actual standard bottom families. This anchor is retained only for the stronger supplied-host/level/grid and same-family dictionary/critical-ratio/Choice joins. The grid representation is not reused on a different space, and the existence of these new bottom representations is no longer a missing supplier.'
# Current geometric/Core anchor scopes, independently reviewed by GV's author.
core_scopes={
 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLayerParametersAdmissible.lean:lay_of_core': 'Supply an actual compatible V4.Core on the same X, then its Lay, nine RecOK duties and universal LedOK comparisons. GV13/GV16/GV19 now supply the VolumeEqMass2/VolTieG input on the exact trueVol/baseVol stage, conditional on the explicitly named unitary Tamagawa-number theorem. The actual Core, trueDsig/formal-degree fields, dependent layout and arithmetic compatibility remain; a bare GJStage/NStage does not supply them.',
 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SizesEqCount.lean:sizes_eq_count': 'Retain the exact same-X context identification K.Over X.B.toPre and all equalities X.S.dsig(tau)=trueDsig(X.B.R,X.B.hc(tau)) needed by the literal size join. Its VolumeEqMass2 input is supplied by GV13 on the trueVol/baseVol stage under the named Tamagawa theorem. The remaining same-object degree/size and Core/layout compatibility must be supplied; DiscreteSeriesExist and FormalDegreeFormula2 remain separate substantive inputs for an actual representation realization.',
 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ExistsStagesClauses.lean:isEmpty_core_untw': 'Known obstruction, explained in GV21: the forced-prime field puts the distinguished prime g0 in T.pl, so T=TwDat.untw B empty cannot admit a V4.Core. Retain this anchor as a constraint on genuine nonempty Core construction, not as a missing volume theorem or an unproved positive existence supplier.',
 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ExistsStagesClauses.lean:exists_stages_clauses': 'Complete the required same-B/f/T/Wt stage compatibility under the literal K.Over and conjugation/support/off hypotheses. This source endpoint supplies MuIsW, MtStableAt, the prescribed Del and etaF scalars, and RowLay; it does not itself assert a full V4.Core. GV supplies the actual volume and scale fields on the trueVol/baseVol stage under the named Tamagawa theorem. Genuine compatible arithmetic/form/local data, the remaining Core/layout fields, and discrete-series/formal-degree inputs remain; bare stage existence must not be promoted to those stronger conclusions.',
}
for k,v in core_scopes.items():
 assert any(key(t)==k for t in candidates),k
 scope_updates[k]=v
for t in candidates:
 if str(t.get('id','')).startswith('NC-next-A') and 'coefficient-ring' in t['declaration']:
  scope_updates[key(t)]='NR now supplies the actual nonempty all-prime coefficient-ring family, normalized characters, finite universal quotients and full-place inducing readings under fixed-field containment. Install these on the same genuine NTw/form/local data with all residual, tame, representation, weight and family equalities preserved. The remaining target is this compatible realization, not the coefficient-ring construction itself.'
for k in list(replaced):
 if k.endswith((':VolumeEqMass₂',':VolTie')) and 'StandardLattice.lean:' in k:
  replaced[k]='GV11/GV13/GV16/GV19 supply the actual geometric frontier on the exact trueVol/baseVol stage, conditional on the precisely normalized classical unitary Tamagawa-number theorem. VolumeEqMass2 follows under literal VolTie; no claim is made for an arbitrary positive D.vol or a full Core.'
updates={}
def add(ids,by,s):
 for cid in ids:updates[cid]=dict(expanded_by=by,scope=s)
add(['GA14','GA22','GA23','AR11','AR21','AR22','RC3','RC6','RC8','RC9','RC10','RC11','RC13','NC4','NC9','NC12','NC17','HF13','HF16','HF17','HF20'],claimids['nonempty_realization'],
 'NR constructs an actual all-prime nonempty TwR/RingSpec with coefficient coverage, normalized characters, finite universal quotients and full-place inducing readings. Its bounded row matrices retain GalEx/RowCusp/ChebSplit. Full SideB, genuine MtFam/MtAd/form/local data and same-object residual/tame/rank joins remain; all original claim records are preserved.')
add(['WA15','WA16','WA17','WA18','WA19','TT13','TT14','TT16','TT18','TT19','TD9','TD15','TD16'],claimids['canonical_weil'],
 'CW constructs the full canonical finite/real Weil action with exact rational pullback automorphy and supplies new bottom-Weil data and prescribed-character adjustments. WA qualitative arithmetic/jet/period consequences now have this supplier. Quantitative dictionaries, critical ratio fields, exact Choice joins and other analytic/operator inputs remain.')
add(['IG12','IG13','IG14','HF18','HF19','HF20','QW3','QW6','QW9','MF19','MF20','RF10'],claimids['geometric_volumes'],
 'GV proves the actual normalized Haar and quotient-to-mass conversions and, with the explicitly named unitary Tamagawa-number theorem, signature independence, VolumeEqMass2, trueVol and same-stage VolTieG. UnitSplit uses classical Hasse–Minkowski. Discrete-series/formal-degree inputs, the remaining exact Core/layout/tuple fields and original quantitative same-object premises remain.')
# Merge the NR and GV annotations on the shared HF20 rather than losing either.
updates['HF20']=dict(expanded_by=claimids['nonempty_realization']+claimids['geometric_volumes'],
 scope='NR supplies genuine all-prime coefficient coverage and inducing readings, with conditional bounded row representations. GV supplies actual normalized volumes and scale on the same stage using the named Tamagawa theorem. Full forms/local realization, discrete-series/formal-degree inputs and the remaining same-object Core/layout fields are retained. Empty-stage models remain insufficient.')
add(['HC8','HC9','HC10','QW14','QW15','QR25'],claimids['centered_character_sums'],
 'CC proves the actual primitive Dirichlet analytic inputs, exact centered integral and uniform QH.thin/ThinH under real-zero exclusion/RealBox. The bounded-conductor margin is reused with its correct finite quantifier. Actual PairEx, RealBox host construction, relative prime progression and the earlier polynomial-window square-root/global joins remain.')
precision=[
 'Nonempty coefficient coverage now uses Tw=Spec1(O_LL0) and retains the fixed D, LL0, LL, embeddings and rows. A full-field Reading.Induces is constructed at each prescribed place. This is stronger than an empty-index skeleton but does not assert genuine form or nonempty-local realization.',
 'Finite-field descent of a compact Qbar_l representation uses a countable cofinal family obtained by the Krasner argument, then Baire and finitely many cosets. Stable integral lattices preserve the same normalized matrices. The row supplier explicitly retains automorphic GalEx/RowCusp and dense split-Frobenius ChebSplit.',
 'The universal anticyclotomic quotient is finite by the actual global Artin map, a finite residue quotient and ideal-class finiteness. Its universal classification is limited exactly as in the source at primes over l. It is not asserted nontrivial or ramified at every allowed prime.',
 'CW constructs operators on the actual theta functions, including the signed finite index, crossed determinant character, Banach smooth-domain argument and exact real vacuum determinant. Arbitrary algebraic extensions to the whole function space are used only outside the domain of the analytic assertions.',
 'Rational automorphy follows from an explicit finite Hermitian Gauss sum, two paired rational lattice indices, the same eta product formula, a convergent Gaussian theta test and the exact real determinant phase. Norm preservation alone is not used to infer the scalar equals one.',
 'The actual prescribed-character construction can use HF11 eta0 with its explicit quadratic restriction and local signs. It does not silently prove the universal IsEtaTilde bridge through GlobalNormIndexTwo. The literal supplied-IsEtaTilde constructor and the actual-character bypass are distinguished.',
 'GV computes the finite |2|^(-n(n-1)/2) Lie-lattice factor and the matching real Omega factor, then cancels determinant and auxiliary-delta factors by the product formula. The rank-one L(1,epsilon) convergence factor is canceled locally before Euler products; no zeta(1) is introduced.',
 'The normalized global unitary Tamagawa-number theorem is an explicit unreconstructed classical input for GV10 and its volume consequences. The direct definite quotient-to-genus-mass identity and Haar scale uniqueness do not depend on it. Hasse–Minkowski remains named for the norm-sign splitting step.',
 'Actual trueVol values and same-stage VolTieG are supplied on valid SigOK spaces. An arbitrary positive D.vol or a malformed fallback is not relabeled as a geometric volume. Dependent Core/layout objects are not automatically transported across withTrue or retie.',
 'DiscreteSeriesExist and FormalDegreeFormula2 remain independent substantive premises for dsig and dsig_all. The new geometric volume and scale results do not prove these representation-theoretic assertions or a complete V4.Core.',
 'CC retains real-zero exclusion in psi_thin/thin and RealBox in ThinH. It identifies both exact centerings, including -1-gamma in the principal case, and controls all y above the specified exponential cutoff. The later-cutoff derivative bound does not replace the earlier polynomial-window square-root estimates.',
 'All predecessor claims, source arrays, file records, graph edges, component bytes and four global branch records remain unchanged. Current annotations and justified target retirements are additive, with historical maps preserved.',
 'Current deliverables are cumulative TeX and an updated ZIP. Draft-mode TeX validation creates no PDF or current page count and is not a visual layout review. The historical v0.13 PDF remains preserved. No full Lean build, independent kernel replay or complete self-contained proof is asserted.',
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,new_in_this_version=new,
 remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),
 completed_previous_frontier='Actual all-prime coefficient rings and inducing readings with conditional integral row families; canonical full Weil action and bottom suppliers; exact geometric volume/trueVol stage using the named Tamagawa theorem; actual late-cutoff centered thinning under RealBox.',
 next_local_priority='Genuine same-object form/local realization and full Core; critical ratio fields, quantitative dictionary and Choice join; remaining classical inputs and independent global/cohomological/PairEx/relative-progression branches.',
 priority_groups={'1':'Genuine nonempty forms/local realization and exact arithmetic joins','2':'Remaining geometric/representation inputs and same-object full Core','3':'Simultaneous primes, relative progressions and independent global/cohomological branches','4':'Quantitative theta dictionaries, critical ratios and exact same-choice joins'},
 component_priority_groups={'nonempty_realization':1,'canonical_weil':4,'geometric_volumes':2,'centered_character_sums':3},
 precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,
 optional_source_route_keys=sorted(set(optional_source_route_keys)),
 precision_supersessions=[
 dict(previous_version='0.20',historical_statement='Nonempty all-place coefficient indexing and compatible readings remain separate suppliers.',current_statement='NR constructs actual TwR/RingSpec on every finite coefficient prime, exact SideB.cover coefficient condition and Reading.Induces for every prescribed full-field place. Form/local installation and the rest of SideB remain.',completed_by=claimids['nonempty_realization']),
 dict(previous_version='0.20',historical_statement='Canonical full new bottom-Weil existence remains in WA17–WA19.',current_statement='CW constructs the full finite/real action with exact rational pullback automorphy and provides canonical and prescribed-character bottom data. Quantitative dictionaries, critical ratios and literal Choice joins remain.',completed_by=claimids['canonical_weil']),
 dict(previous_version='0.20',historical_statement='VolumeEqMass2, VolTie and indefinite geometric volume identities remain after the mass formula.',current_statement='GV proves the exact normalized gauge conversion and direct definite mass identity, then obtains signature-independent volumes and trueVol/VolTieG using the explicitly named unitary Tamagawa theorem. Discrete-series/formal-degree and full Core joins remain.',completed_by=claimids['geometric_volumes']),
 dict(previous_version='0.20',historical_statement='Uniform centered analytic windows remain separate from the norm-prime supplier.',current_statement='CC supplies the actual late exponential-cutoff QH.thin and ThinH conditional on RealBox, with exact centerings and analytic inputs reconstructed. PairEx, relative progression, earlier polynomial-window square-root estimates and final global joins remain.',completed_by=claimids['centered_character_sums']),
 ])
cfg['tex_front_summary']=r'''\textbf{What version 0.21 achieves.} An actual nonempty coefficient
family now covers every finite prime of the fixed coefficient field,
with readings inducing prescribed full-field places and conditional
bounded integral row representations. The full finite and real Weil
actions are constructed on the original theta functions, and exact
phase cancellation proves rational automorphy and the needed bottom
suppliers. The actual geometric volume and true-volume stage identities
are obtained with the explicitly named classical unitary Tamagawa
theorem. Exact centered integrals and uniform late-cutoff thinning are
proved under the original real-zero exclusion and host \texttt{RealBox}.
Genuine form/local realization, the remaining full Core and classical
representation inputs, quantitative theta and critical-ratio joins,
and the independent global branches remain.
This is \textbf{a partial human reconstruction; a complete self-contained
proof of RH or Dirichlet GRH is not yet obtained}.'''
cfg['tex_remaining_local']=r'''NR in Section~\ref{sec:nonempty-realization} supplies the actual
nonempty all-prime coefficient family, normalized characters, finite
universal quotients and full-place inducing readings. Its bounded row
representations retain \texttt{GalEx}, \texttt{RowCusp} and
\texttt{ChebSplit}. Genuine \texttt{TwF}/\texttt{TwL},
\texttt{MtFam}/\texttt{MtAd}, full \texttt{SideB}, compatible residual
and tame data, and nonempty local coverage remain on the same fixed
global fields and rows. Global Artin reciprocity is still a named input.

CW in Section~\ref{sec:canonical-weil} constructs the full finite/real
Weil action, proves the exact rational pullback identity, and supplies
the canonical and prescribed-character bottom constructions. WA's
qualitative arithmetic, normalized jets and supplied-bottom periods
therefore have this existence supplier. Stronger quantitative
\texttt{DictAt}, critical toric ratio fields and the exact
same-embedding/frame/family \texttt{Choice.FieldOK} join remain, as
do the separate analytic convergence, nonvanishing and operator inputs.
The actual-character construction does not prove the separate universal
\texttt{IsEtaTilde} bridge through global norm-index uniqueness.

GV in Section~\ref{sec:geometric-volumes} computes the exact normalized
Haar and quotient-to-mass conversion. Its indefinite volume,
signature-independence and \texttt{trueVol}/\texttt{VolTieG} consequences
use the explicitly stated classical unitary Tamagawa-number theorem;
the norm-sign splitting step uses Hasse--Minkowski. The same-stage
volume and scale joins are available. Discrete-series existence,
the formal-degree formula and the other exact \texttt{V4.Core}/layout
arguments remain, including their forced-prime and conductor identities.

CC in Section~\ref{sec:centered-character-sums} proves the Dirichlet
analytic inputs and exact centered integral, then supplies
\texttt{QH.thin} and \texttt{ThinH} with their real-zero
exclusion and \texttt{RealBox} premises retained. Its uniform range is
above the source's exponential cutoff. The distinct polynomial-window
square-root bounds, simultaneous \texttt{PairEx}, actual
\texttt{RealBox} hosts, relative progression theorem and final global
joins are not supplied by this thinning implication. The four
independent global branches below remain as recorded.
'''
cfg['tex_next_target']=r'''\paragraph{The next target: genuine same-object forms and the remaining global estimates.}
Use the new all-prime coefficient family and full-place readings in
the actual form and local realization; preserve the same fixed fields,
rows, levels and normalized matrices. Supply the remaining full
\texttt{Core}, including the discrete-series/formal-degree premises,
without replacing dependent layouts by unrelated choices.

For theta arithmetic, continue with quantitative dictionaries,
critical ratio fields and exact coefficient-embedding joins. The full
Weil and bottom constructions are now available. For the prime side,
use the proved late-cutoff thinning implication after constructing
the actual \texttt{RealBox}; focus on the independent simultaneous-pair,
relative progression and polynomial-window mean-square suppliers.
Keep the separate spectral, integral metric and cohomological branches.
The current target map records exact pinned declaration ranges and
the remaining scope of each.
'''
cfg['tex_ledger_rows']=[
 span('nonempty_realization').replace('–','--')+' & Nonempty coefficient families & All-prime rings and inducing readings; bounded integral row families under explicit automorphic inputs.',
 span('canonical_weil').replace('–','--')+' & Full Weil construction & Finite and real actions, exact rational phase cancellation, canonical and prescribed-character bottom data.',
 span('geometric_volumes').replace('–','--')+' & Actual geometric volumes & Exact gauge normalization and true-volume stages; classical Tamagawa and separate formal-degree inputs explicit.',
 span('centered_character_sums').replace('–','--')+' & Exact centered thinning & Dirichlet analytic inputs, exact integral and uniform late-cutoff bounds conditional on real-zero exclusion.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For this increment, NR constructs the nonempty all-prime coefficient
family and inducing readings; CW constructs the full Weil action
and rational automorphy. GV supplies actual geometric volume joins
with the named classical boundary visible, and CC supplies the exact
centered integral and late-cutoff thinning. Read the current
remaining-input section before interpreting historical conditional
claims. Stable claim IDs and the pinned source ledger locate full
proof paragraphs and their exact source ranges.
'''
(ROOT/'increment_v0_21.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(map(len,claimids.values())),replaced_target_keys=len(replaced),claim_updates=len(updates)),indent=2))
