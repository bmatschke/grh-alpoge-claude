#!/usr/bin/env python3
"""Describe v0.22, preserving every historical proof claim and its hypotheses."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_21'
def read(p): return json.loads(p.read_text())
components=['automorphic_realization','quantitative_weil_dictionary','discrete_series_core','simultaneous_prime_pairs']
ledgers={c:read(ROOT/c/'provenance.json') for c in components}
claimids={c:[x['id'] for x in d['claims']] for c,d in ledgers.items()}
prior=read(OLD/'next_source_targets.json')
scope=('Partial human reconstruction of RH and Dirichlet GRH. This increment supplies actual full-range Mt forms on a compatible supplied geometric state, original-DVR good lattices and Hecke signatures, and the literal initial SideB endpoint with its zero theta/empty toric initialization and supplied NTh exposed. It proves four supported local primitives. It proves the quantitative moved-vacuum dictionary with exponent [F:Q]ab and one common scalar unit. It constructs the large-gap discrete series used later and calibrates formal degree using the named Harish-Chandra theorem, giving a restricted RealTied join. It proves PrimesRel and full simultaneous PairEx using the explicitly named quadratic class-number formula, Bombieri log-free density/exception refinement, and Heath-Brown density theorem; compatible supplied hosts satisfy RealBox/ThinH, while winPairs retains VWinAt. Genuine same-object theta/local installation, critical toric ratios and original-choice joins, the remaining full Core, named classical inputs and independent global/cohomological/spectral branches remain. This is not a complete self-contained RH/Dirichlet-GRH proof, full Lean build or independent kernel replay.')
new=[
'MR1–MR26: actual full-range Mt realization, exact normalized Hecke integrality and used/unused tuple readings on a supplied compatible state. An integral additive K-reading into the original DVR fraction field and flat descent prove stability of the actual good lattice. Integral finite signatures and actual type spaces give the literal initial SideB conditional on NTh; Theta=ThetaPsi=0, Dat=PEmpty, thP=twDel=0, eH=1 and TwL.empty are exposed. Four local primitives give finite simultaneous splitting, residual-block locality, supported nonzero eigenvectors and freeness of the original relation quotient.',
'QD1–QD22: the moved-vacuum scalar has all conjugates of modulus one and is a unit at every standard finite prime. Entire-jet uniqueness gives one kappa for all these primes. The finite Fourier quotient has cardinal n dividing k^([F:Q]ab), coefficients nu_i/n with nu_i^(2k^2)=1, conjugate l1 norm at most one and k-torsion translations. Rational/split/stabilizer factorization and the real vacuum determinant give exists_kappa, movedVacuum_dict and dictAt_big on the supplied original choices.',
'DC1–DC22: a principal-minor average, decay/Hilbert closure, Schmid/PBW coercivity, unique lowest type and rigidity construct the actual large-gap discrete series. Full central parameters and signs are identified. Compact-dual Haar density and a scalar Bergman integral calibrate the named Harish-Chandra formal-degree theorem. The later weights satisfy the gap, giving all four restricted RealTied fields. All 21 Core fields are audited with the exact remaining layout/arithmetic inputs retained.',
'QP1–QP25: the effective exceptional-zero gap, Page uniqueness and relative progression theorem follow from named CN/BD inputs. Twist cancellation, bounded-coefficient mean squares and a continuum maximal argument give polynomial-window selection. Zero-box tails, including imprimitive Euler factors, give the exact 4 log y bound. Named HD density bounds bad conductors. Both primes satisfy all congruences, windows, character rows and primitive-inducer clauses, yielding full PairEx. A compatible supplied host satisfies RealBox/ThinH; winPairs retains VWinAt.'
]
remaining=[
'Construct the compatible original St/ColPin/R3.Read and all tuple lattice ties, and the genuine RatIn good-row spectral/integral inputs. MR now supplies form realization and lattice/signature construction from these. GlobalArtin, GalEx, RowCusp, ChebSplit, fixed-field containment and the precise polynomial highest-weight theorem remain explicit where used.',
'Install a compatible nonplaceholder theta/toric NTh and genuine nonempty local family on those same forms. Complete NChoice/TupTied/ChoiceSide, NdSpec/LocAll, actual Psi/MtLoc/Act comparisons, residual/tame agreements and IsTripleWith/IsTripleFor. The initial second_step has zero theta fields and an empty toric family and assumes a later NTh; it does not solve these joins.',
'Complete the same-object V4.Core and dependent layout/RecOK/LedOK, ranks, forced primes, conductor support/exponents and stage compatibility. DC supplies the sufficient large-gap RealTied portion with exact Haar scale, retaining Harish-Chandra formal degree and GV unitary Tamagawa. Universal DiscreteSeriesExist/FormalDegreeFormula2 remain separate if their stronger ranges are needed. Hasse–Minkowski remains named.',
'Prove actual critical ToricRatioConjugates/ratio_algebraic/NFRatio arithmetic and the original-embedding/frame/family Choice.FieldOK join. QD supplies quantitative DictAt and common scalar units; WA/CW supply normalized jets, bottom periods and full Weil data. The separate universal IsEtaTilde/global-norm-index bridge is not inferred.',
'Complete actual theta convergence, separation, nonvanishing, unfolding/tower/ratio and positive ThmBop/ThmAop/PartsE/PartsW inputs. Quantitative finite Weil arithmetic does not supply these analytic/operator identities.',
'Complete independent chain-norm and archimedean spectral-word identities, positive kernel/mass normalization, exceptional-word bounds, actual GalD/dimension balance, integral/isometric metric transport and discarded-target control.',
'Complete LinkN/LinkV congruence denominators, two-primary and odd-minus/odd-plus cohomological windows and the literal JointWin/ThmBc/VWinAt supplier. QP proves PrimesRel/PairEx and compatible-host RealBox/ThinH, but does not construct arbitrary hosts or VWinAt.',
'For a fully self-contained analytic reconstruction, expand the retained quadratic class-number formula CN, Bombieri log-free density with exceptional-zero factor BD, and Heath-Brown 1979 Theorem 1 HD. Current PrimesRel/PairEx follow from these unconditional classical theorems without RH/GRH. The fixed 1/8 auxiliary PNTAPRelW and oversized explicit source density constants are not claimed; existential-constant PrimesRel and direct twistK suffice.'
]
def key(t): return t['path']+':'+t['declaration'].split('.')[-1]
def flat(data):
 raw=data if isinstance(data,list) else data.get('targets',data.get('next_targets',[]))
 out=[]; anchor_keys={'source','sources','source_ranges','source_anchors'}
 for item in raw:
  if {'path','line_start','line_end','range_sha256','sha256'}<=item.keys():out.append(item);continue
  anchors=item.get('source_ranges',item.get('sources',item.get('source_anchors',[])))
  if not anchors and isinstance(item.get('source'),dict):anchors=[item['source']]
  assert anchors,('target lacks exact source',item)
  for i,source in enumerate(anchors,1):
   t=dict(source);t.update({k:v for k,v in item.items() if k not in anchor_keys and k not in t})
   t['id']=str(item.get('id',item.get('declaration','target')))+'-'+str(i)
   t['remaining_human_scope']=item.get('remaining_human_scope',item.get('scope',item.get('remaining_scope',item.get('objective',item.get('title','')))))
   out.append(t)
 return out
completed={};candidates=list(prior['targets']);retained_new_keys=set()
for component in components:
 data=read(ROOT/component/'next_targets.json');current=flat(data)
 candidates+=current;retained_new_keys.update(map(key,current))
 records=[]
 for name in ['completed_targets','closed_source_targets','completed_endpoints','conditionally_reconstructed_targets']:records+=data.get(name,[])
 for record in records:
  if {'path','declaration'}<=record.keys():anchors=[record]
  elif isinstance(record.get('source'),dict):anchors=[record['source']]
  else:anchors=record.get('sources',record.get('source_ranges',record.get('source_anchors',[])))
  assert anchors,(component,record)
  for anchor in anchors:
   t=dict(anchor);t.update({k:v for k,v in record.items() if k not in t})
   ids=t.get('claims',t.get('claim_ids',t.get('closed_by',t.get('completed_by',t.get('supplied_by',t.get('reconstructed_by',[]))))))
   ids=ids if isinstance(ids,str) else ','.join(ids)
   reason=t.get('reason',t.get('scope',t.get('remaining_human_scope',t.get('statement','Conditional endpoint reconstructed with its original hypotheses retained.'))))
   for field,heading in [('conditions',' Conditions retained: '),('retained',' Remaining suppliers: ')]:
    if t.get(field):reason+=heading+(t[field] if isinstance(t[field],str) else '; '.join(t[field]))
   completed[key(t)]=ids+': '+reason
replaced={key(t):completed[key(t)] for t in prior['targets'] if key(t) in completed and key(t) not in retained_new_keys}
scope_updates={};optional_source_route_keys=[]
for t in candidates:
 n=t['declaration'].split('.')[-1];p=t['path']
 if n in {'suppSplit_algComb','rat_real_algComb','exists_rep_suppSplit'}:
  optional_source_route_keys.append(key(t))
  scope_updates[key(t)]='Optional auxiliary route: WA11/WA14/WA16 supply qualitative span, jets and bottom periods; CW supplies full Weil/bottom data and QD quantitative DictAt. These split-support lemmas are not missing prerequisites. Critical ratios and exact Choice joins remain.'
 if n in {'MtReal','MtFam','MtInput','MtAd','HeckeTied','HeckeRational','AVTied','mtAd_L'}:
  scope_updates[key(t)]='MR1–MR10 supply actual full-range MtReal/MtFam, normalized integral MtInput and pointwise MtAd from the original compatible St/ColPin/R3.Read and tuple basis/lattice ties. Supply that same state and stronger downstream automorphic/SerAt comparisons. The form construction is no longer missing; an unrelated equal-dimensional space is insufficient.'
 if n in {'RatIn','RatAd','SerAt'}:
  scope_updates[key(t)]='MR11 supplies the finite full rational-lattice portion and exact conditional RatIn/RatAd assembly. Genuine good-row spectral decomposition, K-valued normalized eigenvalues, Hecke reading/transform identities and norm-power denominator bounds remain.'
 if n in {'SideB','TwF','NTw'} or 'coefficient-ring fields' in n:
  scope_updates[key(t)]='NR supplies all-prime rings/readings; MR supplies actual form lattices/signatures and the literal initial SideB on setTw, conditional on a supplied NTh. Theta/ThetaPsi=0, Dat=PEmpty, thP=twDel=0, eH=1 and TwL.empty. A compatible nonplaceholder theta/toric and nonempty local installation with every residual/tame/coefficient square remains.'
 if n in {'Reading','Induces','nonempty','TwCover','RCG/art/art_univ','TwCoverPair','ReadElsewhere','readElsewhere_of_cover'} and any(x in p for x in ['CharpolySmulOfProd','LevelLetterCocycles/','ExistsTiedChoiceOfReads','LocalRingCardinality/']):
  scope_updates[key(t)]='NR supplies universal quotients, all-prime rings and full-place readings; MR supplies initial form/signature fields under rational/automorphic inputs. Retain the stronger same-object theta/toric/local installation with NChoice/ChoiceSide and residual/tame agreements, not coefficient coverage as a missing supplier.'
 if n in {'IsParam','IsResidual','IsChars','IsTripleWith','IsTripleFor','TameTie','exists_tameTie','exists_isTripleOf'}:
  scope_updates[key(t)]='MR17–MR18 supply exact finite occurring-row signatures, normalized integral eigenvalues and NR24 representations. Identification with prescribed residual/Teichmuller data, actual tame equations and every IsTriple clause remains, with nonempty support and the genuine comparison maps.'
 if n in {'tw','ex'} and p.endswith('/NonGaloisDescent/IsCharsOfReading.lean'):
  scope_updates[key(t)]='MR conditionally constructs the actual positive form and good-lattice spaces, finite occurring-row signatures and their NR24 Galois representations. Install these same fields in one compatible nonempty twist/local and toric package, with cover and all comparison maps on the same D. The older exists_isTripleOf requires Loc empty and resets Sig and abelian_2 to empty and Fm to zero; it cannot replace this remaining installation.'
 if n in {'Choice','FieldOK','exKey_of','exField_of_keyFin_exKey','dat_choice_exists'} and ('Theta' in p or 'TwistedOperators' in p):
  scope_updates[key(t)]='WA/CW supply jets, bottom periods and full Weil data; QD supplies exists_kappa, quantitative movedVacuum_dict and dictAt_big on supplied choices. Critical toric ratio/NFRatio arithmetic and the exact original-embedding/frame/family Choice.FieldOK remain.'
 if n=='vK_mem' and p.endswith('/TwistedOperators/RowTestRationalSumsOfFiniteSumsMeaningful.lean'):
  scope_updates[key(t)]='TT8–TT10 already give SumOKK/SumRatK under the literal FieldOK hypotheses; WA/CW supply jets and bottom periods, and QD supplies the quantitative dictionary on the original supplied choices. The unresolved arithmetic is the critical toric ratio/NFRatio supplier and the original-embedding/frame/family Choice.FieldOK join. The actual Formula2K operator equality is an independent obligation; finite field closure is not a new missing supplier.'
 if n in {'DiscreteSeriesExist','FormalDegreeFormula₂','exists_isDS_isFdeg_trueDsig','realOf'}:
  scope_updates[key(t)]='DC supplies the sufficient actual large-gap discrete series and exact formal degree via the named Harish-Chandra theorem and GV Haar normalization, then restricted RealTied with the Tamagawa input. Universal all-regular-parameter interfaces and full same-object Core remain separate.'
 if n in {'Core','ExTrue','coreOfLay','lay_of_core','sizes_eq_count','exists_stages_clauses','recExP_of_recAtG'}:
  scope_updates[key(t)]='GV supplies volume/scale and DC the four large-gap RealTied fields under named Harish-Chandra/Tamagawa inputs. DC21 audits 21 Core fields using the actual layObj(Y). Retain same-X/context/layout, RecOK/LedOK, SatNew/PackEx/LevelThreeCondition where used, forced primes, conductors and arithmetic/form/local comparisons. A full compatible Core is not supplied.'
 if n=='isEmpty_core_untw':
  scope_updates[key(t)]='Known obstruction, retained in GV21/DC21: g0 belongs to T.pl, so T=TwDat.untw B empty cannot have a V4.Core. This constrains genuine nonempty Core construction; it is not a missing volume/discrete-series theorem.'
 if n in {'PairGood','PairEx','pairEx','pair_exists','pair_share','PrimesRel','primesRel_holds','RealBox','winPairs','realBox','thinH','ThinH'}:
  scope_updates[key(t)]='QP supplies PrimesRel and full PairEx under named CN/BD/HD inputs, plus RealBox/ThinH on a compatible supplied PairGood host. Retain only stronger same-host construction and independent VWinAt/cohomological-window requirements at this anchor; no arbitrary host or VWinAt is constructed.'
 if n in {'ExceptionalCharacterCountBound','JacobiTwistedMeanSquareBound'}:
  scope_updates[key(t)]='QP9–QP12 and QP16–QP22 supply the mean-square and bad-conductor estimates used in actual PairEx, under the named CN/BD/HD inputs. This older auxiliary wrapper may be expanded separately with its literal premise/constant conventions; it is not a missing prerequisite for the reconstructed PairEx endpoint.'
 if n in {'VWinAt','vwinAt_of_joint','ch_balance'}:
  scope_updates[key(t)]='QP supplies PrimesRel/PairEx under CN/BD/HD and compatible-host RealBox/ThinH. Two-primary, odd-minus/odd-plus windows, congruence denominators, literal JointWin/ThmBc/VWinAt and final global comparison remain. QP25 proves winPairs only after VWinAt is supplied.'
 if ' Mt fields' in n or n=='D7 coefficient/place fields':
  scope_updates[key(t)]='MR supplies fixed-state global Mt and coefficient-field TypeSpF/lattice data in the initial expansion. Construct the actual compatible state, NChoice/ChoiceSide and genuine theta/local comparisons with original bases and maps. MR23–MR26 close four local primitives, not full NdSpec/LocAll.'
updates={}
def add(ids,c,s):
 for cid in ids:updates[cid]={'expanded_by':claimids[c],'scope':s}
add(['NR17','NR18','NR24','RC3','RC6','RC8','RC9','RC10','RC11','RC13','NC4','NC9','NC12','NC17'],'automorphic_realization',
'MR supplies actual conditional form realization, original-DVR good lattices/signatures, initial SideB and four local primitives. Its zero theta/empty toric initialization and supplied NTh are explicit; genuine theta/local and residual/tame joins remain.')
add(['WA11','WA14','WA16','WA19','CW23','CW24','CW25','TT13','TT16','TT19'],'quantitative_weil_dictionary',
'QD supplies quantitative DictAt with n|k^([F:Q]ab), all-conjugate control and common scalar units on original supplied choices. Critical toric ratio arithmetic and original-embedding Choice remain.')
add(['GV17','GV19','GV20','GV21','MF20','QW9'],'discrete_series_core',
'DC supplies the actual large-gap representation range and calibrated formal degree using named Harish-Chandra, then restricted RealTied with GV Tamagawa. Universal interfaces and remaining full same-object Core/layout fields are separate.')
add(['CC10','CC16','CC18','CC19','CC20','QR25','HC9','HC10'],'simultaneous_prime_pairs',
'QP supplies PrimesRel/PairEx under CN/BD/HD, continuum polynomial-window bounds and exact 4 log y. Compatible-host RealBox/ThinH follow; VWinAt/cohomological windows remain independent.')
updates['HF20']={'expanded_by':claimids['automorphic_realization']+claimids['discrete_series_core'],'scope':'MR supplies conditional actual forms and initial SideB; DC supplies large-gap RealTied under named Harish-Chandra/Tamagawa. Genuine same-stage theta/local installation and remaining Core/layout fields remain.'}
assert set(updates)<={c['id'] for c in read(OLD/'provenance.json')['claims']}
precision=[
'MR realizes the entire TypeSp from original basis/lattice ties, including unused tuples. Hecke integrality excludes exactly the Hecke residue characteristic. An additive K-reading, not a ring embedding of all L, keeps the original DVR; flat descent proves actual good-lattice stability.',
'Literal second_step supplies genuine Fm/B/signature/type fields but initializes Theta=ThetaPsi=0, Dat=PEmpty, thP=twDel=0, eH=1 and TwL.empty. Its forall supplied NTh conclusion does not construct an NTh or genuine theta/local family. The statement parameters M,tup,Q,hM do not create comparisons absent from its proof.',
'MR23–MR26 preserve the fixed row/place, nonzero supported block and original relations. Simultaneous triangularization does not assert semisimplicity; nonzero eigenvectors need nonzero support and transport uses the actual retained Psi.',
'QD uses f=[F:Q], not [E:Q]. The quotient n divides k^(fab); uncollected coefficients nu_i/n satisfy nu_i^(2k^2)=1 and conjugate l1 sum one, with grouping only decreasing the bound. Entire-jet uniqueness fixes one kappa at all standard primes.',
'Rational real-vacuum scalars are genuine determinant characters. Norm preservation alone is not used to infer roots of unity, integrality or finite-prime units.',
'DC constructs the sufficient gap range for actual b_j=b0+j h0, h0≥16 rank^19, rank≥1801. Universal DiscreteSeriesExist is not claimed. The full Capelli central polynomial, including rank-one/rank-two signs, is identified; a Casimir eigenvalue alone is insufficient.',
'Harish-Chandra Discrete Series II, §40 Corollary2 and §41 Theorem16, remains a named input. The group/Haar constant and compact center are calibrated by the explicit scalar Bergman integral. GV unitary Tamagawa and earlier Hasse–Minkowski remain named.',
'QP explicitly retains unconditional classical CN, BD and HD. PrimesRel has existential constants; the stronger fixed 1/8 PNTAPRelW auxiliary formulation and huge explicit density constants are not claimed. The direct twistK route uses the proved literal PrimesRel.',
'QP controls every real y in the polynomial interval by a mean-square derivative argument. Its zero-box tails include imprimitive Euler factors; the leading-one Mertens coefficient preserves the exact 4 log y constant.',
'Bad primitive conductors are counted with zero multiplicity, and principal conductor-one data are handled separately. PairEx includes both primes, all congruences/windows/rows, every primitive inducer and the required real zero boxes.',
'QP23 retains an existing compatible HostRaw with PairGood and its conductor/odd-part conditions; QP25 retains VWinAt(psi,401), checking rescaling and the 401-to-400 cutoff. Arbitrary hosts and cohomological windows are not supplied.',
'All old claim fields, source arrays, dependency lists, component bytes and four global branch JSON records are preserved. New annotations do not add edges to old claims; current scopes supersede older future-work descriptions.',
'Deliverables are cumulative TeX and the complete updated ZIP. Draft-mode TeX checking creates no PDF or current page count and is not visual QA. No full Lean build, independent kernel replay or complete self-contained RH/GRH proof is claimed.'
]
cfg=dict(components=components,tex_component_order=components,date='2026-11-22',scope=scope,
 new_in_this_version=new,remaining_major_inputs=remaining,claim_updates=updates,local_conclusions=dict(zip(components,new)),
 completed_previous_frontier='Conditional actual form/lattice/signature construction and supported local primitives; quantitative Weil dictionary; sufficient large-gap discrete series and RealTied under named inputs; PrimesRel/PairEx under CN/BD/HD with compatible-host RealBox/ThinH.',
 next_local_priority='Genuine same-object theta/toric and nonempty local installation; critical ratios and original-choice FieldOK; remaining full Core, VWinAt and global/cohomological/spectral joins.',
 priority_groups={'1':'Genuine form/theta/local realization and exact arithmetic joins','2':'Remaining classical representation/volume inputs and full Core','3':'Cohomological windows, compatible prime hosts and global branches','4':'Critical ratios, analytic theta operators and original-choice joins'},
 component_priority_groups={'automorphic_realization':1,'quantitative_weil_dictionary':4,'discrete_series_core':2,'simultaneous_prime_pairs':3},
 precision_notes=precision,replaced_target_keys=replaced,target_scope_updates=scope_updates,next_steps=remaining,
 optional_source_route_keys=sorted(set(optional_source_route_keys)),precision_supersessions=[
 dict(previous_version='0.21',historical_statement='Actual Mt/form realization and full SideB remain.',current_statement=new[0],completed_by=claimids[components[0]]),
 dict(previous_version='0.21',historical_statement='Quantitative DictAt remains after full Weil existence.',current_statement=new[1],completed_by=claimids[components[1]]),
 dict(previous_version='0.21',historical_statement='Discrete-series/formal-degree inputs remain for actual middle RealTied.',current_statement=new[2],completed_by=claimids[components[2]]),
 dict(previous_version='0.21',historical_statement='PrimesRel, polynomial-window bounds, PairEx and RealBox remain.',current_statement=new[3],completed_by=claimids[components[3]])])
cfg['tex_front_summary']=r'''\textbf{What version 0.22 achieves.} Actual form realizations on a
supplied compatible state, original-coefficient-ring good lattices and
Hecke signatures are constructed; the initial \texttt{SideB} endpoint
has its zero theta/empty toric boundary exposed. The quantitative
moved-vacuum dictionary now has exponent $[F:\mathbb Q]ab$ and a common
scalar unit. Large-gap discrete series cover the parameters used later,
with formal degree calibrated using the named Harish--Chandra theorem.
Relative progressions and full simultaneous \texttt{PairEx} follow
using three precisely stated classical analytic inputs; compatible
supplied hosts then satisfy \texttt{RealBox}/\texttt{ThinH}.
Genuine theta/local installation, critical ratios, full same-object
\texttt{Core}, \texttt{VWinAt} and the independent global branches remain.
This is \textbf{a partial human reconstruction; a complete self-contained
proof of RH or Dirichlet GRH is not yet obtained}.'''
cfg['tex_remaining_local']=r'''MR in Section~\ref{sec:automorphic-realization} supplies full-range
\texttt{MtReal}/\texttt{MtInput}/\texttt{MtAd} from a compatible fixed
geometric state, and actual good lattices/signatures over the original
DVRs. Its initial \texttt{SideB} is conditional on a supplied
\texttt{NTh}; theta fields are zero and the toric family is empty.
The rational spectral inputs, named Artin/automorphic/highest-weight
theorems and genuine compatible theta/local installation remain.
Finite splitting, supported eigenvectors and relation freeness do not
replace \texttt{NChoice}/\texttt{ChoiceSide}/\texttt{NdSpec}/\texttt{LocAll}.

QD in Section~\ref{sec:quantitative-weil-dictionary} supplies the
all-conjugate, all-standard-prime scalar normalization and quantitative
\texttt{DictAt}, with exponent $[F:\mathbb Q]ab$, on the supplied
original choices. Critical toric ratio arithmetic and the original
embedding/frame/family \texttt{Choice.FieldOK} remain, together with
actual theta convergence, separation, nonvanishing and operator
identities. The universal \texttt{IsEtaTilde} bridge is not inferred.

DC in Section~\ref{sec:discrete-series-core} constructs the sufficient
large-gap discrete-series range. Exact degree uses the named
Harish--Chandra theorem after a direct Haar/Bergman calibration.
With GV's unitary Tamagawa input this gives the four restricted
\texttt{RealTied} fields. Universal representation interfaces and
the remaining same-object \texttt{Core}/layout/arithmetic fields
remain. Hasse--Minkowski retains its stated earlier uses.

QP in Section~\ref{sec:simultaneous-prime-pairs} supplies
\texttt{PrimesRel}, continuum polynomial-window bounds and full
\texttt{PairEx} using the stated classical inputs CN, BD and HD.
Every primitive inducer and the exact $4\log y$ bound are included.
Compatible supplied hosts satisfy \texttt{RealBox}/\texttt{ThinH};
\texttt{winPairs} still requires \texttt{VWinAt}. Cohomological
windows, congruence denominators, actual host/global joins and
the four independent branches below remain.
'''
cfg['tex_next_target']=r'''\paragraph{The next target: genuine theta/local installation and critical ratios.}
Use the actual form lattices/signatures to construct a compatible
nonplaceholder theta/toric witness and nonempty local family on the
same fields, rows and coefficient maps. Keep the rational spectral
and local comparison premises visible; initial zero theta/empty
toric data do not solve this existence step.

For theta arithmetic, focus on the critical ratio field and the
original-embedding \texttt{Choice.FieldOK}; the quantitative dictionary
is available. Use the large-gap \texttt{RealTied} supplier to complete
the exact \texttt{Core}/layout fields. Use \texttt{PrimesRel}/\texttt{PairEx}
and compatible-host \texttt{RealBox} while proving the independent
\texttt{VWinAt} windows and final joins. Named classical inputs and
separate spectral/integral metric branches stay explicit. The
current work map gives exact pinned source ranges.
'''
cfg['tex_ledger_rows']=[
'MR1--MR26 & Actual form and local primitives & Fixed-state full-range forms, original-DVR good lattices/signatures; initial theta boundary explicit.',
'QD1--QD22 & Quantitative Weil dictionary & Common scalar units, all-conjugate control and the exact totally-real-degree denominator exponent.',
'DC1--DC22 & Large-gap discrete series & Constructive sufficient range, calibrated formal degree with named input, restricted RealTied.',
'QP1--QP25 & Relative progressions and prime pairs & Continuum bounds, all-inducer PairEx and compatible-host RealBox under named inputs.']
cfg['tex_reading_order']=r'''For the global spine, read
Sections~\ref{sec:analytic}, \ref{sec:scalar}, and \ref{sec:frame}.
For this increment, MR constructs actual form/lattice/signature data
and identifies the initial theta boundary. QD gives the quantitative
dictionary. DC constructs the sufficient large-gap range and
calibrates formal degree. QP proves relative progressions and
simultaneous prime selection, retaining independent host/cohomological
joins. Read the current remaining inputs before historical conditional
claims. Stable IDs and the ledger locate full proofs and exact sources.
'''
(ROOT/'increment_v0_22.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,new_claims=sum(map(len,claimids.values())),replaced_target_keys=len(replaced),claim_updates=len(updates)),indent=2))

