#!/usr/bin/env python3
"""Define the additive v0.35 continuation, retaining the exact producer scopes."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
components=['global_loss','global_final_installation','holomorphic_uniqueness','count_auxiliary_primes']
claims={name:[c['id'] for c in json.loads((ROOT/name/'provenance.json').read_text())['claims']] for name in components}
def span(name):
    return claims[name][0]+'–'+claims[name][-1]
new=[
 span('global_loss')+': the complete original small-share loss supplier, including the dyadic order constant 12, all eleven prime-class/discriminant terms, uniform thirteen-error absorption, the exact finite-place gain/IO dictionary and every permitted Reads/HEq/cutoff. ChosenTT, ChosenBadp, LinkG and ChosenWS imply literal LossFS(Fm,0), with the same degree pair and its actual realizing member; CoverAll is not added.',
 span('global_final_installation')+': the literal same-family linkCore/ChainTied installation and final Closed wrapper. Every Data, tie, ledger, size, window, character and cutoff field is checked; ChosenE plus ChosenWall supplies the full Seven packet by independent density and prime-sum estimates. The complete FamGLmin consumer gives LinkGLOBAL on the original inputs, with Cabs=2, C0=3, column constant 4,eD=2, eL=0 in the selected route.',
 span('holomorphic_uniqueness')+': the actual signed-frame domain, smooth Borel/holomorphic dictionary and coefficient uniqueness, then full LowSm/LowIrr with multiplicity one of the original algebraic supremum. The original extremal coefficient identity and Hilbert multilinear realization are proved on the same quotient, retaining bounded HolForm, FinPair and IsReg. The actual base-model ordered parameter installation is checked. Common all-parameter io, boundedness/finite volume and the global smooth/Sobolev/central/cuspidal-closure suppliers remain.',
 span('count_auxiliary_primes')+': the complete original ArPl supplier under unchanged CohP. The proof constructs the exact polarized residual subgroup, the PL-relative Frattini tower, split degree-one Chebotarev primes with inverse-Frobenius convention, all actual level records and closed kernels, and one uniform Hom bound for every level. It also constructs every original IsRes Hecke value for a supplied integral type. Ordinary/control, the type/neatU, same-J HasAut, Choice, first-order/obstruction bounds and Raw remain.',
 'The selected final-global assembly leaf is now proved in its original supplied-family scope. The selected register has 34 open coupled leaves: 23 C, 9 B, 2 D. Theta and CountII leaves are strictly narrowed. Every inherited claim, source array, dependency edge, compound target, optional route and historical correction is retained; no complete human proof of RH or Dirichlet GRH is claimed.'
]
remaining=[
 'Construct the original common recursive/geometric member and compatible Bundle with its duties. DesignChoices/RecAtG, geometric readings, rational tests and actual RowsHold0_3 remain; the construction-class size/rank consumers are already complete.',
 'Finish the original base theta extension: construct one io_i satisfying IsIoW for every parameter t; produce boundedness and the actual finite-volume regular target; prove the smooth representatives and all derivatives of the original Hilbert image, Sobolev point-evaluation bounds and resulting uniform growth, central finiteness, and cusp closure. Full original LowSm/LowIrr, holomorphic uniqueness, the exact extremal coefficient and the Hilbert multilinear stage are now supplied. Preserve one same-model map on the full original Wall.',
 'Produce actual NBuilt/NdSpec and the original local projection square on the common installation, with its original spectra, maximal ideals and embeddings.',
 'Supply the original denominator, retained defect, period-height, local-gain and spectral estimates on the same family.',
 'Construct the compatible second-layer selector and duties. The complete eleven-field FamGLmin package, its count/slopes/ranks/frame/windows/characters, both losses, same-family ChainTied installation and final Closed consumer are all proved on their stated inputs. This does not create the selector or the local/spectral/arithmetic producers.',
 'For RH and power-of-two-order targets finish the original Cases I/II/V. CountII retains ordinary/control/arithmetic-fiber data, the four further Hida endpoints, same-J all-level HasAut, Choice, first-order and obstruction bounds, Raw, and original CohP and side conditions. Exact reciprocity, required universal NiceI Norm, full ArPl and supplied-type IsRes are now proved. The integral type/neatU and TThetaEx are still producers. Both original rank-four Links retain the common coefficient threshold at fixed iota.',
 'Unrestricted Dirichlet targets also retain CaseIII, SeedIV and original chain propagation/descent. The two-primary specialization does not imply universal CountIII.',
 'The AQ positive-part endpoint remains optional with its own arithmetic envelope; the selected sufficient route and the historical RF16 correction governed by DEX11 remain unchanged.'
]
priority=(
 'Re-audit the common original construction and the remaining theta/ordinary producers against the final ten-input cut. '
 'The next bounded analytic producer is the simultaneous JointHarm.exists_ioP: first construct its parameter-free exists_io_poly on the actual CoefMapTie, then prove the original compact Weil-character laws for every parameter t using the completed full lowest type. '
 'In parallel reconstruct the original one-point NiceI Choice at h=0 and a=n=4, including its finite detector and full coefficient-extension transport; prove the proposed zero-dimensional Kap specialization before using it, and only then assess its possible B2 consequence. '
 'These are work priorities, not additional closure claims. Keep bounded HolForm, the actual FinPair/IsReg target, smooth representatives, Sobolev bounds, central finiteness and cusp closure explicit, together with original ordinary/control and same-J HasAut. '
 'The common Bundle/readings/rational tests/local installation and compatible second layer still dominate several final inputs; prioritize any concrete producer that supplies several of those interfaces. '
 'Do not repeat the closed global assembly or substitute a compatible model for the original common objects.'
)
allnew=sum(claims.values(),[])
updates={
 'GLS13':(claims['global_loss']+claims['global_final_installation'],'The complete original global consumer is now supplied: both Loss_at clauses with the realized degree pair, literal same-family ChainTied and the final Closed wrapper. All upstream compatible-family/second-layer/Duty and global-input producer premises remain.'),
 'RSL13':(claims['global_loss']+claims['global_final_installation'],'The original full FamGLmin packet now feeds the complete LinkGLOBAL consumer through exact fields and uniform quantifiers. The selector and its duties, LinkG/LinkS/LinkIRR/LinkDIV, common construction and readings remain explicit.'),
 'GFA12':(claims['global_loss']+claims['global_final_installation'],'The former final-global residual is closed on its original supplied-family inputs. The retained character functional is the one used simultaneously in the final original tied ledger.'),
 'CTC13':(claims['holomorphic_uniqueness'],'Full original lowest-type smoothness and irreducibility, including multiplicity one, are now proved. Holomorphic uniqueness gives the exact extremal coefficient and original Hilbert multilinear realization. Common all-parameter io, boundedness/finite-volume and global smooth/Sobolev/central/cusp-closure producers remain.'),
 'TAE13':(claims['holomorphic_uniqueness'],'The LowSm/LowIrr premises are supplied for the actual ordered base model; the lowest-type cusp packet gives the original holomorphic extremal, and under boundedness/FinPair/IsReg the exact Hilbert map. The full pointwise Sobolev-continuous MMap and common io are not yet claimed.'),
 'BTH12':(claims['holomorphic_uniqueness'],'The analytic extension has its full-lowest-type and Hilbert coefficient stages, on the same original model and quotient. Common all-parameter io, boundedness/finite-volume, global Sobolev/central/cusp closure and separate readings/rational tests/base rows remain.'),
 'JSP11':(claims['count_auxiliary_primes'],'The full ArPl premise is now supplied under unchanged CohP, including every list/all levels and a uniform Hom bound. Required universal NiceI Norm remains supplied by CIP. Choice, first-order and obstruction bounds, Raw and same-J HasAut remain original premises.'),
 'CIP12':(claims['count_auxiliary_primes'],'JSP_ACTUAL_ARPL is fully supplied, and original supplied-type residual Hecke values are constructed at every QData level. The ordinary/control and integral-type/neatU/TThetaEx producers, HasAut and other patched-support inputs remain.'),
 'QX10':(claims['count_auxiliary_primes'],'Both original rank-four Links can use the universal ArPl and supplied-type IsRes suppliers, with ell=3 and the same threshold order. No original ring or ideal is replaced and no ordinary or automorphic producer is inferred.'),
 'DA1':(allnew,'The exact final ten-input interface is unchanged. The global assembly obligation is proved in its stated scope; theta and CountII contracts are narrowed. All common-object producers and the remaining selected leaves are still required.'),
 'GH7':(allnew,'Both final roots use the completed global assembly and new theta/auxiliary-prime subarguments. RH retains I/II/V and unrestricted Dirichlet GRH also retains III. The human reconstruction remains incomplete.')
}
cfg=dict(artifact_version='0.35',date='2026-11-22',predecessor_version='0.34',components=components,
 expected_new_claims=len(allnew),component_claims=claims,
 scope='Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Lean proof as fully checked and correct. Version 0.35 completes both original losses and the final same-family global assembly, full lowest-type multiplicity one and the original Hilbert coefficient stage, and the complete ArPl and supplied-type IsRes consumers. Common construction, theta/Sobolev, local/spectral and ordinary/automorphic producers remain. No new Lean build or kernel replay is claimed.',
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope='Additive scope update; every predecessor field, source and dependency edge retained.')for k,v in updates.items()},
 precision_notes=[
  'Formal correctness is accepted. Category D records incomplete human understanding of the source, not an alleged defect in Lean.',
  'A is a direct published application with hypotheses checked; B is independently reconstructible; C requires substantial reconstruction; D is a source-understanding issue. Completion and category are separate.',
  'LFS proves both original losses, including every Reads/HEq/cutoff, with the same av,bv and actual realizing i1. No CoverAll premise is inserted.',
  'GFI checks every field of the final ChainTied and Closed consumers; it constructs no compatible family, selector or global-input producer.',
  'The column parameter 4, final ChosenQD parameter CL, Cabs=2,C0=3,eD=2, eL=0 and the final 1/2+9epsilon endpoint retain their distinct original meanings.',
  'LowSm/LowIrr is proved for the entire original lowKSub supremum, including multiplicity one, without replacing it by an irreducible summand or another DSModel.',
  'The original Hilbert map retains bounded HolForm, FinPair and IsReg. It is not yet the full pointwise smooth/Sobolev-continuous MMap.',
  'One common io_i must still satisfy IsIoW for every parameter t. Pointwise existence with a t-dependent choice would not meet that contract.',
  'ArPl retains the full original CohP hypothesis; it uses finite H1 and the original tame clause explicitly. It is universal over every finite list and every level, including n=0, q=0, N=0.',
  'The auxiliary-prime approximation is relative to the exact PL subgroup, and TWPl uses inverse arithmetic Frobenius. The bound #HomL(H)*ell^(q[Gamma:H]) is uniform in the level.',
  'CAP15–CAP17 produce original residual Hecke values for any supplied integral type; TThetaEx/neatU and ordinary/control remain open.',
  'The Closed cutoff and transport tuple precede Fm,CH. The eventual x threshold may depend on the family but precedes all members, words, places and readings.',
  'All 245 inherited compound targets and their 107 scope groups are retained. The 34 open selected leaves are not a completion percentage or a proof of absolute minimality.',
  'No Lean replay or PDF production. Two draft TeX passes check syntax and references; historical overfull warnings remain recorded.'
 ])
(ROOT/'increment_v0_35.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print('Configured',cfg['expected_new_claims'],'new claims.')
