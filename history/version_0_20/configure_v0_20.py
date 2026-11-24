#!/usr/bin/env python3
"""Describe the v0.20 increment; all predecessor proof records stay immutable."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_19'
def read(p):return json.loads(p.read_text())
components=['adic_realization','finite_weil_arithmetic','mass_formula','ray_prime_estimates']
ledgers={c:read(ROOT/c/'provenance.json')for c in components}
prior=read(OLD/'next_source_targets.json')
claimids={c:[x['id']for x in d['claims']]for c,d in ledgers.items()}
def span(c):return claimids[c][0]+'–'+claimids[c][-1]
scope=('Partial human reconstruction of RH and Dirichlet GRH. This increment proves normalized one-dimensional adic-character realization from the stipulated global Artin map, its finite-DVR descent and actual shift/block/local consequences with the installed-reading compatibility retained. It proves qualitative finite Weil algebraicity for the actual supplied representation and vacuum, the normalized jet field and period fields for supplied bottom triangles. It reconstructs the local Hermitian densities and global mass-ratio induction, with Hasse–Minkowski explicitly used as a named classical theorem. It constructs the actual ray-class LFam and proves its uniform weighted interval estimate, including polynomial real-zero bounds and exact Perron endpoints, thereby supplying ShortNorm and the required level/dyadic norm primes. Compatible nonempty arithmetic data and full geometric core, canonical new bottom-Weil existence, quantitative dictionaries, critical ratio fields and same-embedding theta joins, and the four global branches remain. No complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay is asserted.')
new=[
 span('adic_realization')+': construct the actual normalized algebraic Hecke-to-adic character from GlobalArtin, prove finite-DVR closed-image/integral-unit/topology descent, and retain the exact inverse-Frobenius convention. Prove shift/block realizations, reading independence, identification with the installed first character under its reading record, all five host character laws and actual conditional local IsGalOf/DeltaRead consequences. Keep nonempty index/coverage and same-object form/tuple compatibility separate.',
 span('finite_weil_arithmetic')+': prove the actual finite-Weil algebraic-span theorem using finite Heisenberg projectors, algebraic coefficients and pairings, split normalization to fix phase, positive-power closure and local unitary generation. Supply NFJet and SumsIn for every literal supplied bottom triangle. Construct standard bottom geometry conditional on the two new full Weil data, and reduce arbitrary splitting characters to the canonical eta case. Keep quantitative DictAt, critical ratio fields and the exact Choice embedding join explicit.',
 span('mass_formula')+': prove local Hermitian diagonalization and representation, finite matrix/vector densities including dyadic places, the weighted local orbit law and literal LIStat, rank-one mass independence, global finite fiber patching, weighted singular-series averaging and the rank induction. Obtain the exact SiegelMassRatio and standard SiegelMassRatioCM normalization; explicitly retain only classical Hasse–Minkowski in the global representation step. Supply the mass premise of QW9 while retaining actual geometric volume/core identities.',
 span('ray_prime_estimates')+': construct every field of the exact ray-class LFam with conductor4dM^2 and same-family NormOne support. Prove Mellin continuation, logarithmic derivative, a uniform B^-45 real-character value bound, B^-46 zero separation, family-wide unique simple exception, the uniform explicit formula and a B^-47 weighted short-interval bound. Close both QW11 suppliers and obtain ShortNorm with exponent47, then the literal level-prime window and nine-tenths dyadic norm-prime count.',
]
remaining=[
 'Construct compatible nonempty twist/local index data on the same D, with all-place SideB.cover, actual field containments and coefficient readings, normalized installed characters, genuine representation/weight/form data and the MtReal/NExpTied/ColW/Pre2/St/RowPk joins. GA now supplies normalized characters and conditional local identities after those inputs exist. Its character replacement on an empty-Loc skeleton is explicitly not the needed nonempty form realization. Global Artin reciprocity remains a named published input.',
 'Supply the compatible V4.Core and its real/twist/object/layout, recursive and integral comparisons, including the geometric VolumeEqMass2/VolTie and indefinite volume normalizations. MF now proves the actual mass ratio using classical Hasse–Minkowski; it does not identify these unrelated geometric volumes or construct the core.',
 'Construct the canonical full adelic bottom-Weil data (exists_weilDatum_etaTilde) with actual finite/real action, commutation and rational theta-distribution automorphy. WA proves finite algebraicity for any supplied literal datum and gives explicit splitting-character adjustment, not existence of every new full datum. The stronger quantitative all-embedding and finite-unit DictAt dictionary remains.',
 'Complete the critical ToricRatioConjugates field with its exact CM/reference-twist data, and join all theta fields through the same Choice.FieldOK embedding, normalization, frame and family. The qualitative finite-Weil arithmetic, NFJet and supplied-bottom SumsIn are now proved. Remaining analytic convergence, separating functionals, nonvanishing/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs retain their literal scopes.',
 'Complete the independent quantitative chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control. Rational common image and rank equality alone do not give these estimates.',
 'Complete congruence denominators LinkN/LinkV, two-primary and odd-minus/odd-plus cohomological windows, simultaneous PairEx choices and uniform gain-to-centered-prime-sum/final parameter supply. QR now supplies the particular unconditional arithmetic ShortNorm and level/dyadic norm-prime theorems under their source interval and geometric hypotheses; it does not supply these simultaneous global objects.',
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
completed={};candidates=list(prior['targets']);retained_new_keys=set()
for component in components:
 d=read(ROOT/component/'next_targets.json');current_targets=flat(d);candidates+=current_targets
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
   if t.get('retained'):reason+=' Explicit remaining supplier(s): '+'; '.join(t['retained'])
   completed[key(t)]=ids+': '+reason
replaced={key(t):completed[key(t)]for t in prior['targets'] if key(t)in completed and key(t)not in retained_new_keys}
scope_updates={}
optional_source_route_keys=[]
for t in candidates:
 n=t['declaration'].split('.')[-1]
 if n in {'suppSplit_algComb','rat_real_algComb','exists_rep_suppSplit'}:
  optional_source_route_keys.append(key(t))
  scope_updates[key(t)]='Optional reconstruction of this auxiliary source route only. WA11 proves the actual generic finite-Adelic algebraic-span theorem for the supplied representation and vacuum by finite Heisenberg algebra, phase fixing and local unitary generation; WA14 proves NFJet and WA16 proves SumsIn for supplied bottom triangles. These auxiliary split-support/rational-real/representation-factorization arguments are bypassed by that proof and are not retained prerequisites for those conclusions. Canonical new full bottom-Weil existence, quantitative DictAt, critical ratio fields and the exact Choice.FieldOK join remain separately indexed.'
 if n=='recExP_of_recAtG':scope_updates[key(t)]='IG13–IG14 prove the size/threshold transport; QW9 proves window_lower and MF19 now supplies its exact mass law using classical Hasse–Minkowski. Actual RecAtG/V4.Core/VolumeEqMass2/Lay/RecOK/LedOK and EvP remain.'
 if n in {'Choice','FieldOK'} and 'Theta' in t['path']:
  scope_updates[key(t)]='WA supplies qualitative finite-Weil arithmetic, actual NFJet and SumsIn for supplied bottom triangles. The canonical full bottom-Weil supplier, critical ratio field, stronger quantitative dictionary and literal same-embedding/frame/family Choice join remain; use the exact new WA target scopes.'
updates={}
def add(ids,by,scope):
 for cid in ids:updates[cid]=dict(expanded_by=by,scope=scope)
add(['AR1','AR2','AR3','AR4','AR5','AR6','AR7','AR8','AR9','AR10','AR11','AR21','AR22','RC3','RC4','RC10','RC11','RC13','NC9','NC12','NC17','LS20','LS21','LS22'],claimids['adic_realization'],'GA proves normalized one-dimensional adic-character construction from the stipulated GlobalArtin map and conditional actual local/installed reading consequences. Compatible nonempty all-place coverage, same-object fields/readings/representations and the form/tuple joins remain; the old mathematical record and hypotheses are preserved.')
add(['HF13','HF16','HF18','HF19','HF20'],claimids['adic_realization'],'GA continues the actual host frame to normalized characters at every supplied coefficient index/reading, and proves the exact five host-character laws. This does not create compatible nonempty twist/local data or a full Core.')
add(['TT13','TT14','TT16','TT18','TT19','TD1','TD9','TD15','TD16'],claimids['finite_weil_arithmetic'],'WA proves qualitative finite-Weil arithmetic for the actual datum and normalized vacuum, NFJet and period fields for supplied bottom triangles. It retains new full bottom-Weil existence, stronger quantitative dictionary, critical ratio fields and the same-embedding Choice join; other analytic/operator inputs are not silently discharged.')
add(['QW3','QW6','QW9','IG13','IG14','RF10'],claimids['mass_formula'],'MF proves the exact SiegelMassRatioCM via local densities, finite global orbit patching and weighted lattice averages, explicitly using classical Hasse–Minkowski. QW9 therefore has its mass supplier; actual geometric Core/volume/ChOK/du/Ds requirements remain.')
add(['QW10','QW11','QW12','QW13'],claimids['ray_prime_estimates'],'QR constructs the actual LFam and proves the uniform weighted interval supplier. The old QW reductions now yield ShortNorm with permissible exponent47 and the literal level/dyadic norm-prime consequences, under their original scale/ModAt hypotheses. Simultaneous PairEx and centered global prime-sum objects remain separate.')
precision=[
 'The normalized Hecke-to-adic character is now constructed from the stipulated GlobalArtin map, including the archimedean correction, open-kernel Artin descent, finite-DVR closed image, integral units and topology. The algebraic complex reading is never treated as continuous. Global Artin reciprocity itself is explicitly retained as a published theorem.',
 'Identification with a preinstalled first/local character uses its actual normalized Frobenius readings and commuting coefficient-field equations. Existence of a new character does not replace these records. The empty-Loc replacement preserves Tw but empties Sig/forms and does not prove nonempty coverage or the genuine arithmetic form realization.',
 'Qualitative finite-Weil algebraicity is proved on the actual representation and vacuum, including phase. It is distinct from stronger quantitative all-embedding/finite-unit DictAt estimates. Actual latO contains the host fractional-ideal multiplier, and dyadic Heisenberg signs remain.',
 'NFJet and SumsIn for supplied bottom triangles are proved. A new full bottom-Weil datum still requires its canonical eta construction; the explicit determinant-root twist changes splitting characters but does not create that canonical representation. Critical toric L-value ratio fields and literal Choice embedding joins remain.',
 'The exact unramified CM mass ratio is reconstructed with its factorial, pi, root-discriminant and square-root constants. Hasse–Minkowski is an explicitly cited classical theorem used for global representation; its proof is not claimed. No mass formula or Tamagawa theorem is used as an unexplained premise.',
 'The mass law and geometric VolumeEqMass2/VolTie or indefinite volume identities are distinct. QW9 now has the actual mass-law supplier but still uses its literal same-object ChOK/du/Ds and core data.',
 'The arithmetic LFam keeps the exact ray congruence, norm, unit factor and conductor4dM^2. All fourteen record laws and the same-family NormOne support are proved before applying the analytic theorem.',
 'The analytic prime argument proves |F_chi(1)|>=c B^-45 for real characters, real-zero gap>=c9 B^-46, and a family-wide unique simple exception. Perron uses the full floor endpoint, with an O(log u) endpoint allowance, and tracks both residue signs. The weighted estimate has permissible exponent47 and is uniform only under its stated conductor/relative-length restrictions.',
 'The particular ShortNorm and level/dyadic arithmetic prime suppliers are now proved. They do not by themselves provide simultaneous PairEx, abundant compatible local stages, a centered prime-sum theorem or RH/Dirichlet GRH.',
 'All predecessor claims, source arrays, file records, graph edges and component bytes remain unchanged. Current annotations and target retirements are additive, with historical target records archived. The four independent global branch records remain unchanged.',
 'Current deliverables are cumulative TeX and an updated ZIP. Draft-mode TeX validation creates no PDF and gives no layout certification. The historical v0.13 PDF remains preserved. No full Lean build, independent kernel replay or complete self-contained proof is asserted.',
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),completed_previous_frontier='Normalized one-dimensional adic-character supplier from GlobalArtin; qualitative finite-Weil arithmetic with actual normalized jets and supplied-bottom periods; exact unramified CM mass ratio using Hasse–Minkowski; actual LFam and uniform weighted interval theorem, hence ShortNorm and level/dyadic norm primes.',next_local_priority='Compatible nonempty arithmetic/geometric data and full Core; canonical full bottom-Weil construction, critical ratio fields, quantitative dictionary and exact Choice join; the independent global metric/cohomological/simultaneous-prime/centered-window branches.',priority_groups={'1':'Compatible nonempty arithmetic realization and actual normalized readings','2':'Full geometric core, geometric volumes and remaining classical inputs','3':'Simultaneous prime selection and independent global/cohomological branches','4':'Canonical full Weil existence, quantitative dictionaries, critical ratio fields and same-choice theta tests'},component_priority_groups={'adic_realization':1,'finite_weil_arithmetic':4,'mass_formula':2,'ray_prime_estimates':3},precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,precision_supersessions=[
 dict(previous_version='0.19',historical_statement='Normalized algebraic adic-character existence remains a separate supplier.',current_statement='GA constructs it from the stipulated GlobalArtin map and exact field/readings. Global reciprocity and compatible nonempty same-object index/representation/form data remain.',completed_by=claimids['adic_realization']),
 dict(previous_version='0.19',historical_statement='Qualitative finite-Weil arithmetic remains in TT13/TT16.',current_statement='WA proves the actual same-vacuum algebraic span, NFJet and supplied-bottom SumsIn. Canonical new full Weil existence, quantitative DictAt, critical ratio fields and the exact Choice embedding join remain.',completed_by=['WA11','WA14','WA16','WA18','WA19']),
 dict(previous_version='0.19',historical_statement='SiegelMassRatioCM remains the substantive mass premise of QW9.',current_statement='MF proves the exact local/global mass-ratio induction, explicitly using classical Hasse–Minkowski. The separate geometric volume/core and same-object size identities remain.',completed_by=['MF18','MF19','MF20']),
 dict(previous_version='0.19',historical_statement='The actual LFam and uniform weighted trivial-class interval theorem remain in QW11.',current_statement='QR proves both suppliers and gives a permissible weighted exponent47. QW11–QW13 now yield unconditional arithmetic ShortNorm and actual level/dyadic consequences under their stated ModAt/scale conditions. Simultaneous global prime choices and centered-window objects remain.',completed_by=['QR9','QR24','QR25']),
])
cfg['optional_source_route_keys']=sorted(set(optional_source_route_keys))
cfg['tex_front_summary']=r'''\textbf{What version 0.20 achieves.} The normalized one-dimensional
adic-character supplier is constructed from the stipulated global Artin
map. Qualitative finite Weil arithmetic now supplies the actual normalized
jet field and period fields for supplied bottom triangles. The exact
unramified CM mass ratio is reconstructed using the classical
Hasse--Minkowski theorem. The actual ray-class family and its uniform
weighted interval estimate are proved, supplying the norm primes required
by the earlier reductions. Compatible nonempty arithmetic data and the
full geometric core, new full bottom-Weil existence, critical ratio and
same-embedding theta joins, and the four global branches remain.
This is \textbf{a partial human reconstruction; a complete self-contained
proof of RH or Dirichlet GRH is not yet obtained}.'''
cfg['tex_remaining_local']=r'''GA in Section~\ref{sec:adic-realization} proves normalized adic
characters from the stipulated global Artin map, including finite-DVR
descent, exact local laws and conditional identification of installed
characters. The actual nonempty twist/local indices, all-place cover,
field containments/readings, genuine representation and form data, and
same-object tuple and weight joins remain. Global reciprocity is a named
published input. Empty-index replacement constructions do not supply
these compatible nonempty data.

WA in Section~\ref{sec:finite-weil-arithmetic} supplies qualitative
finite-Weil algebraicity for the actual datum and vacuum, the normalized
jet field and the period fields of supplied bottom triangles. The
canonical full Weil construction for new bottom spaces, stronger
quantitative dictionary, critical toric ratio fields and literal
same-embedding \texttt{Choice.FieldOK} join remain. Analytic convergence,
separating functionals, nonvanishing/tower/ratio and positive theta
operator/type inputs retain their exact remaining scopes.

MF in Section~\ref{sec:mass-formula} proves the exact mass ratio and
therefore supplies the mass premise of QW9, explicitly using classical
Hasse--Minkowski in its global representation step. The independent
\texttt{VolumeEqMass2}, \texttt{VolTie}, indefinite volume and full
\texttt{V4.Core} identifications remain, as do the actual
\texttt{ChOK}/$d_u$/$D_s$ inputs of the quantitative window.

QR in Section~\ref{sec:ray-prime-estimates} proves the actual
\texttt{LFam} and its uniform weighted interval supplier. The previous
prime-power and scale reductions now give \texttt{ShortNorm} and the
literal level-prime and dyadic norm-prime conclusions under their
source hypotheses. This does not construct simultaneous
\texttt{PairEx} or the centered prime-sum data. The four independent
global branches below remain as stated.
'''
cfg['tex_next_target']=r'''\paragraph{The next target: compatible global inputs after the new suppliers.}
Continue with the nonempty same-object arithmetic realization and the
full geometric core. The normalized character construction is now
available at each supplied coefficient index, but it does not create
all-place coverage, the form realization or the required tuple joins.

For theta arithmetic, construct the canonical full bottom-Weil datum,
prove the stronger quantitative dictionary and critical-ratio field,
and join the actual coefficient embeddings and tests. The local
finite-Weil, jet and supplied-bottom period calculations are now
available. The mass ratio and the particular uniform norm-prime
supplier are also available, so their old conditional reductions need
not be reopened. Preserve the separate spectral, integral metric,
cohomological, simultaneous-prime and centered-prime-sum branches.
The current target map records exact pinned declaration ranges and
the remaining scope of each.
'''
cfg['tex_ledger_rows']=[
 span('adic_realization').replace('–','--')+' & Normalized adic realization & Exact character construction and local laws; installed readings and nonempty same-object joins retained.',
 span('finite_weil_arithmetic').replace('–','--')+' & Finite Weil arithmetic & Same-vacuum algebraic span, normalized jet field and supplied-bottom periods; full existence and field joins retained.',
 span('mass_formula').replace('–','--')+' & Exact mass ratio & Local densities, global weighted averages and rank induction; classical Hasse--Minkowski named explicitly.',
 span('ray_prime_estimates').replace('–','--')+' & Uniform norm-prime supply & Actual ray family, exceptional-zero estimates and weighted interval theorem; ShortNorm and level/dyadic consequences.',
]
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For the current increment, GA resolves the normalized adic-character
supplier; WA resolves qualitative finite Weil arithmetic and its actual
jet and supplied-bottom period consequences. MF gives the exact mass
ratio needed by the preceding quantitative window, and QR gives the
arithmetic family and uniform interval theorem needed by its norm-prime
reductions. Read the current remaining-input section before interpreting
historical conditional claims. Stable claim IDs and the pinned source
ledger locate the full proof paragraphs and their exact source ranges.
'''
(ROOT/'increment_v0_20.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(map(len,claimids.values())),replaced_target_keys=len(replaced),claim_updates=len(updates)),indent=2))
