#!/usr/bin/env python3
"""Describe the exact v0.43 increment and the unchanged whole-route frontier."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
old=json.loads((ROOT/'increment_v0_42.json').read_text())
nodes={n['id']:n for n in json.loads((ROOT/'dependency_audit_v0_42/obligation_map.json').read_text())['nodes']}
contract=nodes['COUNT_II_SUPPORT']['contract']
a=contract.index('OTW12 proves one original theta')
b=contract.index('The selected Raw patching',a)
contract=contract[:a]+(
 'OTW12 proves one original theta before every K with complete-coefficient IsTheta/IsWt. '
 'ITA1–ITA13 now construct the full original integral TypeForAlt over the unchanged O, for every IsTeich family and every IsRecT map, '
 'and substitute it into OTW13/CAP17 to give the original UnitaryHeckeData/HdEx. The matched crystalline-type theorem and inherited local Langlands/RecTExists foundation are explicit. '
 'FNL, OST, WRP, OCT, OHA, SMP and ASP supply all original finite-level/HSet, ordinary/freeness/base-change, weight, control, Hecke-algebra and arithmetic-specialization fields. '
 'ADP constructs the actual formU/decompU on the original compact unitary quotient; CFD proves full clParts_alt on its supplied original AutomorphicHeckeSet. '
 'AFS proves domain and DenseWt for every supplied LamObj and weight, TWtBridge, goodScalB_alt, partAct0_alt and TCoreSep on their original inputs. '
 'Its same-J density implication retains the exact AutomorphicHeckeSet installation input. '
 'The remaining arithmetic producers are the actual Galois-decorated partX_alt/partU_alt and AutomorphicHeckeSet supplier, the full point-output record, '
 'RingProps and the bare same-J density installation, the four exact Hida endpoints PointTheoremBaseObject, ArithmeticPointDecomposition, '
 'IrrArithPointsAutomorphicAway and TwistOk, and all-level same-ideal LevelAlt/TWAut/HasAut on both original Links. '
)+contract[b:]

cfg={
 'artifact_version':'0.43','date':'2026-11-23','source_commit':old['source_commit'],
 'components':['integral_type_v43','automorphic_decomposition_v43','classical_parts_v43','arithmetic_fibers_v43','finite_local_completion_v43'],
 'closed_selected_leaves':{},
 'closed_nested_producers':[
  'Full original integral TypeForAlt, on the explicitly matched classical local type and inherited local Langlands/RecTExists foundations',
  'Original HdEx/UnitaryHeckeData by exact substitution into OTW13 and CAP17',
  'Full original formU and decompU on the actual compact unitary quotient',
  'Full original clParts_alt on the supplied original AutomorphicHeckeSet, with arbitrary predicate refinement',
  'Full original TDenseU.isDomain_and_denseWt_of_isTheta for every supplied original LamObj and every original weight',
  'Exact TWtBridge arithmetic/good-point equivalences on the stored Artin maps',
  'Full original goodScalB_alt, hecke_operator_preserves_part and partAct0_alt on their stated original hypotheses',
  'Full original TCoreSep/Out.sep with its original AutomorphicHeckeSet input',
  'Complete same-kernel density implication for original IsJ with the exact AutomorphicHeckeSet installation input exposed',
  'Full SameFactorCount, CrossFactorCount and LocalEstimateII, including the constant 23 and all finite-field/degree quantifiers',
  'Actual pattern exchange and full lowerWtComparison; squarefree eU law and normalized-label comparison on their exact original records',
  'WeightAllRows on the original selected eventual family, using the actual rank-growth threshold and original Wg'
 ],
 'status':(
  'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge–Claude formal proof as fully checked and correct. '
  'Version 0.43 completes the integral local type and original Hecke-data supplier, the actual compact-unitary and classical decompositions, '
  'dense good weight points and the original fiber/scalar/separation arguments, and the remaining selected finite local weight estimates. '
  'The actual Galois-decorated automorphic-part supplier, its same-ideal Hida/support installation, the common geometric/local family, '
  'global quantitative producers and other arithmetic branches remain. No new whole selected leaf is closed; the 31-entry register retains its full contracts. '
  'No Lean build or kernel replay is claimed.'),
 'local_conclusions':[
  'ITA1–ITA13 construct one original integral TypeForAlt over the unchanged coefficient DVR. The proof checks every Teichmuller lift, every weaker IsRecT map, all allowed residue primes including 3, repeated inertia characters and arbitrary nonzero individually isotypic product modules. A matched crystalline inertial-type theorem supplies the local complex detector. Integer norm exponents make its detecting property invariant under coefficient conjugation; a stable lattice followed by restriction of scalars returns the final representation to the original O. The inherited local Langlands and RecTExists foundations are explicitly retained. Substitution into OTW13/CAP17 gives the original HdEx/UnitaryHeckeData.',
  'ADP1–ADP12 prove full original formU and decompU. Finite class representatives make the actual definite unitary quotient compact and its original invariant form positive; checked finite multiplicity and algebraic semisimplicity give finite equivariant projections. Exact bidual scalarization preserves the prescribed basis, infinity representation, rational equivariance and all matrix-valued coefficient equations. This constructs the actual automorphic decomposition, while its Galois decoration remains separate.',
  'CFD1–CFD12 prove full original clParts_alt and a predicate refinement. Finite left-coset averaging works without normal stabilizers, preserves every original compact scalar profile, and keeps the same level, depth and finite-part characters. Polynomial projectors preserve the original norm-one generalized eigenspaces of the normalized Uz. The original AutomorphicHeckeSet premise is retained, rather than inferred from decompU alone.',
  'AFS1–AFS22 prove the domain and full DenseWt statements on every supplied original LamObj, exact arithmetic/good-point equivalence, occurrence of every specified Hecke character in the faithful module fiber without flatness, the original distinct-unit principal-series criterion and goodScalB_alt, full partAct0_alt and TCoreSep/Out.sep. The same-kernel argument proves density for the very same IsJ ideal when the exact original AutomorphicHeckeSet supplier is present. Nonzero-block fiber nonvanishing is proved; existence of a nonzero block for an arbitrary residual label is not asserted.',
  'FLC1–FLC19 prove the full original root-injectivity collision estimate with constant 23, the exact finite pattern exchange and lower character law, the squarefree Gelfand–Graev weight formula, and transfer to the unchanged normalized polynomial labels. Green’s cuspidal theorem is the one explicit published finite-group input, with its primary-symbol and degree/value dictionary. The actual WeightAllRows bound with the original Wg now follows for the selected eventual family, including the explicit rank-growth justification for its long-prime-degree term. The unused fourth admLq upper comparison is not claimed.'
 ],
 'remaining_major_inputs':[
  'Construct the actual Galois-decorated partX_alt/partU_alt and AutomorphicHeckeSet supplier, including the original global attachment, spherical polynomial readings, ordinary local/Hodge comparison and point-property record. Then install full Out.pt, RingProps and bare same-J density, followed by PointTheoremBaseObject, ArithmeticPointDecomposition (the exact cofinite strict Frobenius-norm ratio), IrrArithPointsAutomorphicAway and TwistOk. Complete all-level LevelAlt/TWAut/HasAut on BOTH original rank-four Links, with the same original ideal J, fixed iota, prime 3, full CohP/LocCFT and one common coefficient threshold. TypeForAlt, HdEx, formU/decompU, clParts_alt, DenseWt and the generic scalar/separation machinery are now available and should not be reconstructed again.',
  old['remaining_major_inputs'][1],
  old['remaining_major_inputs'][2],
  old['remaining_major_inputs'][3],
  'Supply the original adelic HidaSetting, reduction/inflation and Haar normalization in EtOne, RowsAdd/RowsGood, one common AllRows object and the three sufficient arithmetic cylinder counts. The selected finite local WeightAllRows producer is now proved on these exact original inputs. Complete the denominator, period/height, local-gain and normalized spectral estimates on the same family, with the GQT weaker sufficient alternatives available at their stated uniform scope. Complete the compatible second-layer selector with simultaneous thresholds.',
  old['remaining_major_inputs'][5],
  old['remaining_major_inputs'][6]
 ],
 'next_targets':[
  'Actual partX_alt/partU_alt and AuTeichEx AutomorphicHeckeSet: reconstruct the GuWrap/GalUnitaryT attachment and its exact Satake, Hodge, ordinary, type and polarization dictionary. Use ADP for the actual decomposition and ITA for the original integral type.',
  'Install the already proved AFS fiber/scalar/separation machinery on that same original automorphic supplier; then full Out.pt, TJRing/TJDense and the four exact Hida outputs, before all-level same-J automorphy on both Links.',
  'In parallel, original EtOne/RowsAdd/RowsGood and common AllRows with three arithmetic counts; prescribed common geometric/local family; one-character/congruence/RIG_II and the original global estimate producers. Reuse the completed finite local laws and their unchanged Wg.'
 ],
 'selected_node_progress':{
  'COUNT_II_SUPPORT':{'completed':['ITA1–ITA13','ADP1–ADP12','CFD1–CFD12','AFS1–AFS22'],
   'remaining':'Actual Galois-decorated partX_alt/partU_alt and AutomorphicHeckeSet; full Out.pt/RingProps and bare same-J density installation; all four exact Hida endpoints and all-level same-J automorphy on both Links. The complete generic density implication retains that exact supplier. Classical local Langlands/RecTExists and the explicitly named local literature/type inputs retain their stated foundation status.'},
  'GLOBAL_RETAINED_DEFECT':{'completed':['FLC1–FLC19, reusing RRT1–RRT16 and GQT1–GQT5'],
   'remaining':'Actual supplied normalized-type compatibility, original HidaSetting, reduction/inflation EtOne with the same Haar normalization, RowsAdd/RowsGood, one common AllRows object and the three arithmetic cylinder counts. All five selected Wg terms now have local producers, with the explicit eventual rank threshold for the last. The stronger unused fourth admLq upper comparison is not asserted.'}
 },
 'updated_contracts':{'COUNT_II_SUPPORT':contract},
 'published_applications':[
  {'title':'Crystalline inertial type at every original local residue prime',
   'source':'Matthew Emerton and Toby Gee, Moduli stacks of étale (phi,Gamma)-modules and the existence of crystalline lifts, Theorem 8.2.1; conventions Section 1.12',
   'url':'https://www.math.uchicago.edu/~emerton/pdffiles/moduli.pdf',
   'claims':['ITA6','ITA8','ITA12'],
   'hypotheses_checked':'Actual finite extension F/Qp, finite-image inertia type extending to the Weil group, arbitrary rank n>=1 and arbitrary smooth irreducible pi. No genericity or prime-to-rank restriction. The original complex normalization, fixed iota, descent to original O and every-map quantifiers are separately proved.'},
  {'title':'Singleton-segment Langlands quotient dictionary',
   'source':'Caraiani, Emerton, Gee, Geraghty, Paskunas, Shin, Patching and the p-adic local Langlands correspondence, Sections 1.8 and 3.1, Proposition 3.9; Theorem 3.7 for comparison',
   'url':'https://www.ma.imperial.ac.uk/~tsg/Index_files/Gpatching.pdf',
   'claims':['ITA5','ITA7'],
   'hypotheses_checked':'Ordered rank-one smooth characters with mu_j != mu_i|.| for i<j, the exact geometric reciprocity convention and source Good/inj scope. No global patching restriction is imported into the separate unrestricted type application.'},
  {'title':'Cuspidal parameters, degree and elliptic values of finite general linear groups',
   'source':'J. A. Green, The characters of the finite general linear groups, Trans. AMS80 (1955),402–447, Theorems12–14, Lemma7.4, Definition3.1 and formula(12)',
   'url':'https://www.ams.org/tran/1955-080-02/S0002-9947-1955-0072878-2/S0002-9947-1955-0072878-2.pdf',
   'claims':['FLC16','FLC17','FLC18'],
   'hypotheses_checked':'Original finite field and supplied LabelDatum, exact Teichmuller embedding and generators, regular-character Frobenius orbits, degree-d simplex with partition(1), finite unnormalized parabolic induction, degree and elliptic sign. FLC15 supplies separate original-label uniqueness for the q>=5 consumer.'}
 ]
}
(ROOT/'increment_v0_43.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'components':cfg['components'],'closed_selected_leaves':cfg['closed_selected_leaves']}))
