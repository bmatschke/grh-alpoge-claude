#!/usr/bin/env python3
"""Record full neat/weight endpoints and exact rational/local finite construction."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
components=['neat_levels','ordinary_theta_weight','rational_theta','local_hecke_projection']
claims={n:[c['id'] for c in read(ROOT/n/'provenance.json')['claims']] for n in components}
allnew=sum(claims.values(),[]);old=read(ROOT/'history/version_0_40/provenance.json');old_count=len(old['claims'])
span=lambda n:claims[n][0]+'–'+claims[n][-1]
new=[
 span('neat_levels')+': full original neatU is reconstructed for every QData, arbitrary integral tau0 and every original compact-open level K. The proof uses the fixed odd auxiliary prime stored in HidaSetting, its actual unramified place, bounded integral unitary powers and principal congruence torsion-freeness. Every section fallback, level join and same-coordinate identity is checked; no ell>n or integral-type premise is added.',
 span('ordinary_theta_weight')+': full original TThetaEx is reconstructed using the actual artOf and complete coefficient ring. Finite characters at every adic precision kill the actual Artin kernel; separatedness produces one full-ring character, and the inverse cyclotomic adjustment gives the original product-torus theta. This one theta is fixed before every K; full neatU supplies its IsWt freeness. The original HdEx record is assembled after the complete original TypeForAlt is supplied, using inherited CAP17 IsRes. TypeForAlt itself remains open.',
 span('rational_theta')+': prescribed-field coefficient extension, original split class representatives, self-dual lattice square law and finite residue PhiIs are reconstructed. Every Pins field is assembled from the exact CoversAt input. The class-sum finite transfer gives phase-correct OneMapOverL with common lambda,z before O; the actual good projector gives RatG and both-level LiftTestB. Exact MLat follows from the original LatFull field. Higher covers, class-sum existence/uniqueness, PointIdentCore, base ClassSumsSpan and geometric LatFull production remain explicit upstream suppliers.',
 span('local_hecke_projection')+': original HeckeLift0, all-index commutation, HeckeStd0 and HeckeIntTw are reconstructed from their original complex/form inputs. Every maximal ideal is an actual residual eigenspace class; the literal projected MtSub is finite free and localizes to the exact part. Psi, range, projection error, spans, faithful ActEx/ActHK, original MjLat relation quotient and complete nonempty_spec are supplied on their full original antecedents. One coefficient compositum preserves all four requirements. Actual F3/F4, complex Hecke/no-Jordan and arithmetic character suppliers remain open.',
 f'There are {len(allnew)} new and {old_count+len(allnew)} cumulative human proof claims. The whole selected open-leaf register remains 33=22C+9B+2D: 26 shared by RH and unrestricted Dirichlet GRH, with 7 additional GRH-only leaves. Completed internal producers reduce those obligations without declaring a compound leaf complete.'
]
remaining=[
 'Construct the full original integral TypeForAlt, the remaining HSet.Ax and ordinary/control/separating arithmetic fibers, then the four Hida endpoints and all-level same-J TWAut/HasAut on BOTH original rank-four Links. Full neatU, full TThetaEx, supplied-type IsRes and conditional HdEx assembly are now reconstructed; selected Raw is already complete. Preserve prime 3, fixed iota, original same J and one common coefficient threshold.',
 'Construct the actual prescribed higher covers, all-tuple class-sum existence/uniqueness including phase-rescaled O, one PointIdentCore with common lambda,z, base ClassSumsSpan and geometric LatFull. RTG supplies the finite coefficient/phase/projector transfer to OneMapOverL, RatG and both-level LiftTestB once these original suppliers are available. Actual common R/F geometry, Inputs/Pins/Holds/ExAt/InGeo, Fits and eta agreement remain coupled.',
 'Complete the original local coefficient producers F3 and F4, preserving exact valuation/norm/GoodCoef/iq and common-overfield reading of the entire original coefficient field. Construct the actual complex Hecke standard/normality facts and arithmetic twist-character/admissibility inputs on the same common form data. HLP supplies the finite algebra and full nonempty_spec assembly, while whole ndSpec_exists, AutSpec and NBuilt remain open.',
 'Complete actual base rows, host/frame fields, MultEq support, the stored nonzero chain and group tie, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. The stronger second DivRows3 remains separate; exact first row-pair integrability, first DivDef3 and common comparison/copy/read algorithms are already reconstructed on their original premises.',
 'Supply denominator, retained-defect, period-height, local-gain and normalized spectral estimates on the same original family, with its unchanged spectra, ideals, embeddings, metrics and measures. Complete the compatible second-layer selector with the same Bundle/BWit/BunU/FamGLmin data and simultaneous eventual thresholds.',
 'Finish original Cases I/II/V for RH and two-primary targets. Unrestricted Dirichlet GRH additionally retains Case III, Seed IV and both original rank-four chain propagation/descent requirements. No restricted-character result is substituted for the full target.',
 'Resolve AD_VANISH_K_MATCH and HOST_RIGID_S as the two D-class questions about our human source understanding. The original Lean is assumed correct; these are not allegations of formal gaps. Optional AQ remains optional and historical RF16 remains governed by DEX11.'
]
priority=('Prioritize the bounded original finite-level supplier FuCmpMem.finU, then OrdFree.ordStruct/ordFree and OrdBCMapOrd.ordBC leading into CtrlOrd/HiComm/HiAlg. In parallel reconstruct the full original TypeForAlt and separating arithmetic fibers leading to four Hida endpoints and all-level same-J HasAut, now that full neatU, TThetaEx and selected Raw are available. In parallel complete actual F3/F4 coefficient readings/bridges for the local constructor, and the geometric CoversAt/ClsEx/PointIdentCore/ClassSumsSpan/LatFull inputs for phase-correct rational theta tests. Use each constructed object on the one original common family; preserve both rank-four Links, prime 3, fixed complex embedding, same J, metrics/measures and one common coefficient threshold. General multi-point Core and abstract replacements for the original projected lattice do not contribute to the current selected route.')
ordc=claims['neat_levels']+claims['ordinary_theta_weight'];rat=claims['rational_theta'];loc=claims['local_hecke_projection']
updates={
 'JSP11':(ordc,'Full neatU and TThetaEx now supply the original all-level neatness/weight inputs; HdEx is assembled after original TypeForAlt. Integral type, ordinary/control, four Hida endpoints and same-J HasAut remain.'),
 'CIP4':(claims['ordinary_theta_weight'],'The same original artOf now yields one complete-ring theta before every K by finite-quotient character separation and separatedness; its normalization is unchanged.'),
 'CAP17':(claims['ordinary_theta_weight'],'The full original IsRes joins full neatU/TThetaEx in OTW13; only the original integral type antecedent remains for the HdEx record assembly.'),
 'SCI13':(ordc,'The selected Raw producer remains complete. Its earlier neatness and TThetaEx dependencies are now reconstructed; the original integral type/ordinary/control/Hida/HasAut packet remains.'),
 'BTH8':(rat,'Exact finite transfer now supplies the original both-level LiftTestB from phase-correct OneMapOverL on its actual geometric suppliers; finite dimensionality alone remains insufficient.'),
 'BTH11':(rat,'Rational coordinate tests now follow through the exact RatG/good-projector construction when original geometric covers, class sums and point identity are supplied.'),
 'BTH12':(rat,'Primitive rational-test wrappers and phase transfer are reconstructed, with precise higher-cover/class-sum/point-identity/spanning and LatFull producers retained.'),
 'RDR22':(rat,'Original reader/copy algorithms can now use the exact phase-correct rational-test construction under its stated geometric inputs. Actual common geometry, Fits, eta agreement and outer common-family duties remain.'),
 'LTD3':(loc,'HLP9 additionally proves exhaustion of all maximal ideals by the finite supported residual characters without presuming the whole Hecke algebra finite over O.'),
 'LTD4':(loc,'HLP supplies exact finite algebra, MtSub/Psi/action and full nonempty_spec on its arithmetic antecedents. The complete compatible NdSpec/NBuilt existence input remains upstream.'),
 'MR23':(loc,'The original splitting-field primitive joins the prescribed finite-value field and the original F3/F4 thresholds in one fixed-embedding compositum.'),
 'MR24':(loc,'Actual finite nonempty XOf and common residual-kernel hypotheses are now supplied for locality of the original TOf.'),
 'MR25':(loc,'The actual MtLoc, Psi, faithful ActEx and ActHK hypotheses are now supplied from original Hecke integrality/semisimplicity inputs.'),
 'MR26':(loc,'Actual OsInt/sOfC and the distinct original MjLat generator relation quotient are explicitly installed, including the universal coefficient-map relation clause.'),
 'DA1':(allnew,'Four new components close full neatU/TThetaEx and reconstruct exact rational and local finite constructors. All 33 whole compound leaves remain with refined original supplier boundaries.'),
 'GH7':(allnew,'Both final targets retain their original character scope and selected graph. New all-level ordinary inputs and local/rational constructors reduce shared producer work without a final theorem claim.')
}
assert set(updates)<={c['id'] for c in old['claims']}
cfg=dict(artifact_version='0.41',date='2026-11-22',predecessor_version='0.40',predecessor_claim_count=old_count,
 components=components,expected_new_claims=len(allnew),component_claims=claims,
 scope='Partial human reconstruction of RH and unrestricted Dirichlet GRH, assuming the Alpoge–Claude Lean proof fully checked and correct. Version 0.41 completes full original neatU and TThetaEx, conditional HdEx, exact finite rational-theta transfers and the original finite local Hecke/projection/nonempty_spec construction. Original integral-type, ordinary/control, geometric and arithmetic coefficient suppliers remain. No Lean replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; all predecessor fields, source arrays and mathematical edges remain unchanged.') for k,v in updates.items()},
 precision_notes=[
 'A=published application with checked hypotheses; B=independent elementary/moderate proof; C=substantial reconstruction; D=human source-interface uncertainty. Classification and closure are separate.',
 'Full original neatU is proved for arbitrary integral tau0, every original QData and all compact-open K, using the same stored odd unramified auxiliary prime. No ell>n or type premise is introduced.',
 'Full original TThetaEx uses actual artOf and one character valued in the entire complete coefficient ring, fixed before every K. The inverse cyclotomic adjustment and the exact relation Tc(c) iff Uc(c+1) are retained; ell=3 is retained.',
 'OTW13 is the complete HdEx record assembly after supplied full TypeForAlt. It does not prove unconditional nonempty_unitaryHeckeData from HypothesesH\'.',
 'Rational theta keeps phase cj(twAt embLL A3.A.v0)(R.phs i), the same base coefficient record and actual good projector. Arbitrary mu0 phase substitution is invalid.',
 'RTG geometric CoversAt, ClsEx/uniqueness for rescaled O, PointIdentCore with one lambda,z before O, base ClassSumsSpan and actual LatFull remain explicit suppliers.',
 'HLP uses full ambient Hecke range k<=nV, not only the row range k<=r. Actual MtInput.rat/int and complex Hecke/no-Jordan inputs are retained.',
 'The original Hecke algebra need not be asserted finite over O before semisimplicity. Its reduced evaluation image is finite; integral lying-over proves every maximal ideal has a supported character.',
 'MtSub is the O-span of projected original MtLat generators. Bj uses the distinct original MjLat(j).gen. Psi, its off-space error and universal coefficient relation are literal.',
 'At ell=2 the original s0 is v2(QS); at odd ell it is max(1,vell(QS)). The generic mkX uses B0.Q and Qc_eq consumes the retained hQ.',
 'HLP proves full nonempty_spec on its entire original input list. The stronger whole ndSpec_exists, AutSpec and NBuilt producers remain open with exact F3/F4 and arithmetic character obligations.',
 'Every historical interface cut remains unchanged as a checkpoint. New v041 cuts govern current boundaries, and all 245 targets receive explicit additive dispositions.',
 'The selected graph remains 121 nodes/161 edges with 33 whole open leaves, 26 shared and 7 GRH-only. These are scope counts, not a percentage of completion or an absolute minimality theorem.',
 'Every predecessor file/proof/source array/claim edge is preserved. Independent mathematical reviews bind new proofs and the current audit. Draft TeX checks syntax/references; no PDF or Lean replay.'
 ])
(ROOT/'increment_v0_41.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',len(allnew),'new claims;',old_count+len(allnew),'cumulative.')
