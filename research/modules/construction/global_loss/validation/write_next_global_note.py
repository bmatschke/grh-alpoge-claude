#!/usr/bin/env python3
"""Reproduce the v0.35 global continuation note without modifying proofs."""
from pathlib import Path
import argparse
import hashlib
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve()
WORKSPACE = HERE.parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=WORKSPACE / 'lean_source')
parser.add_argument('--output', type=Path, default=WORKSPACE / 'reconstruction_v035/continuation_notes_v0_35/next_global_assembly.txt')
args = parser.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()

BODY = '''NEXT GLOBAL ASSEMBLY — VERSION 0.35 SOURCE-ANCHORED HANDOFF
22 November 2026

Standing premise: the pinned Alpoge–Claude Lean proof is fully checked
and correct. This note prioritizes the remaining HUMAN reconstruction.
It adds no mathematical claim and reports no new Lean replay.
Source commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean

CHANGE IN PRIORITY
The original global slope consumer is now complete on its original
inputs. LFS1–LFS17 prove both universally quantified losses and the
original LossFS(Fm,0), keeping the same chosen degree functions and
their realizing member. GFI1–GFI17 install the common arithmetic model,
every ChainTied ledger field, the original chosen-data conversions and
the final Closed implication. GLS/GLE/GVC/GFA and the final ZW numerical
step are already supplied. No new CoverAll premise was added.

Accordingly, TASK_GL_FINAL_ASSEMBLY is closed as a B implication.
TASK_LINK_GL_INSTALL and the LinkGl pair are complete CONDITIONAL joins;
they do not produce the compatible family, its selected Bundle or its
arithmetic/spectral inputs. Closing the consumer removes a former
bounded blocker and makes the shared construction producers the next
global priority. The remaining selected register has 34 coupled leaves,
23 C, 9 B and 2 D; this is not a completion percentage.

1. THE EXACT FINAL TEN-INPUT CUT

UpperTheory.Top.topDesWin takes DesignExists plus nine Closed predicates.
For the selected constants Cabs=2, C0=3, eD=2, eL=0, these are:

  (1) DesignExists(WithTw(WithSm Cprime),3).
  (2) Closed(Des(C,3)) LinkN.
  (3) Closed(Des(C,3)) LinkEta.
  (4) Closed(Des(C,3)) LinkIRR.
  (5) Closed(Des(C,3)) SmallLevelRankEq.
  (6) Closed(Des(C,3)) [TuSize -> DGamSize -> LinkDIVt(2,CH)].
  (7) Closed(Des(C,3)) [ChosenE(3,CH) -> NuFullF and MuRank].
  (8) Closed(Des(C,3)) LinkG.
  (9) Closed(Des(C,3)) [TuSize -> LinkS(3)].
 (10) Closed(Des(C,3)) [TuSize -> DGamSize -> LinkGLOBAL(2,CH,3,2,0)].

There are also the class-side conditions Cprime -> C, Cprime -> E,
and E -> HypV. For one original Built construction class A and one fixed
target chi, shapeWin uses
  C = WithChN A,
  Cprime = WithChN(A intersect (GChi chi).cls(3/2)),
  E = (GChi chi).cls(3/2).
Thus D3(3,A)=Des(C,3). The design class
  Cdes = WithTw(WithSm Cprime)
is distinct from C and D3; its target intersection must be retained.

All nine Closed cutoffs and transport tuples are joined BEFORE selecting
the one Fm and CH through DesignExists. Their eventual x thresholds may
depend on that Fm and CH but precede every member, word, place, reading
and base point that they cover. The tuple of unrelated statements
"there exists a family with property P" does not provide this cut.

The source uses HypV + LinkN + SmallLevelRankEq to obtain DIVinN, then
LinkEta + DIVinN to activate LinkDIVt. Actual LinkDIV, NuFullF, MuRank,
TuSize and DGamSize supply LinkMu through the already reconstructed MT
transport. Finally LinkGLOBAL consumes the same ChosenE and the SAME
LinkG, LinkS, LinkIRR, LinkDIV and LinkMu. This is the explicit sufficient
route being audited, not a theorem of absolute minimality.

2. FIRST SHARED TARGET: ONE ORIGINAL CONSTRUCTION AND SELECTOR

The highest-contribution global task is the common construction behind
DESIGN_CHOICES_COMMON, LOCAL_NBUILT_COMMON,
SECOND_LAYER_COMPATIBLE_SELECTION and the four coupled base-theta inputs.
Treat this as one source-identity problem with several mathematical
producers, not as independently selectable models.

The concrete selection route is:
  RecAtG / RecExP and the original object construction;
  ExBL together with compatible RowL properties;
  classSel, yielding one class A and one RawSel sigma;
  Bundle projections sel, selS, selP, selDH, selC, selB;
  nonempty_hyps_of_allRows / shapeWin on those exact projections.

Bundle stores R, S, P, pin, DH, C and B in one dependent object.
Its pin is RowSideDetermined R.T P. C is the actual square-integrable
column realization for that SAME R.T and P. B uses that C, its Sp,
the original scale, and S. The projections in ColumnCompatibleSelection
are literal field projections from sigma; this is the binding to retain
through every later row, period, local and spectral argument.

classSel does not supply arbitrary missing geometry for free. Its exact
premises include BaseCond, FirstG, ExportF, SecondG, ExBL and RowL,
besides the mass/volume inputs. It first combines the RowL requirements,
then selects one strengthened class and sigma. nonempty_hyps_of_allRows
similarly joins all its original AllRows properties before calling
classSel once. Those source declarations explain the compatible join;
they are locators for the remaining producer proof, not substitutes for
that proof. When expanding this C leaf, keep each unfinished producer
and each unfinished implication visible separately.

The Built predicate contains an equality of the WHOLE dependent tuple
(D,O,b) with a constructed (beta.D,beta.O,b'). This is stronger than an
unrecorded isomorphism of coefficient fields. Its class parameter kappa
is chosen once before the family points. RecExP chooses du and Dstar
before every subsequent compatible LevCh; those quantifiers are also
part of the construction, not bookkeeping to discard.

DesignChoices itself supplies one family with the original thick set,
chosen tops/bad primes/quadratic data/code, boxes, row data, DGam divisor,
tame distinctness, CF=CH, code bound and CYL<=9. The already proved
DEX/DSZ/RMP consumers turn this into DesignExists on the actual class
with cT(eps,y)=cTmin(y). They prove the size/rank properties of supplied
members; they do not establish that the required common member exists.

3. WHAT THE COMMON SELECTOR CAN UNLOCK

(a) Local coverage and eta. Preserve the original NBuilt certificate
before forgetting it to a selected RecT. NBuilt carries the precise
automorphic and local data, its NdSpec, AutSpec, semisimplicity and the
identity D'=withLoc L. The already reconstructed LTD finite argument
turns that actual specialization, joint injection and rank coverage
into LinkEta. There is no remaining finite generalized-primary proof to
redo. The remaining task is to produce the certificate on the selected
Fm.D(x,i) with the original iV/Hecke/Psi/projection maps and one threshold.

(b) Full rank and global slopes. The actual selected real witness is
T.theta.real and the actual columns are T.cols, for the SAME selected T.
ClassOfRecordOfChoice.real_place_second_layer_conditions_of_choice uses
the finite-character input for those original forms. RSL and the GLE
operators then give the smaller fullness route; it does not need GL4 or
the final global slope assembly. The complete slope route additionally
uses the eleven-field GLS FamGLmin packet and the now-complete GFI
consumer, without a new deep mass/genus or metric obligation.

Duty is still required on the common class. Its original fields are
PageFix, PageWin, SmallFirstModulusBelowScale, TameDistinctF, ChosenWall,
TupUsedF and TwAllF. TG already reconstructs ColsTiedSym in its stated
scope, so an earlier FC19 pending label must not reopen it. What remains
here is the actual selection/existence and every required original tie.

(c) The small-level rank/theta interface. SLR and BTH give the finite
consumer from the SAME Bundle's RowsHold0_3 and base thTheta square.
The four remaining coupled producer records are geometric readings,
the full analytic extension, rational tests, and actual base rows.
They are joint requirements on one sigma, P, coefficient embedding,
theta map and row family. Choosing another Bundle for rationality or
another row family for rank does not satisfy the source interface.

The next bounded theta target is the simultaneous exists_ioP statement:
for each i construct ONE coefficient/Fock map y before every parameter
t, with IsIoW for each t. The source writes exactly this quantifier order
before applying choice. Reconstruct its common polynomial map and
every required original compact/Weil identity; a separate y_t for each
t is insufficient. This remains a proposed target, not a new closure.

The next analytic target after that is the actual extension following
the now-complete HCU lowest-type/coefficient/Hilbert stages: construct
the original pointwise smooth MMap from the Hilbert realization, with
Sobolev point evaluation, all derivatives, uniform growth, central
finiteness and preservation of cuspidality under closed orbit span.
The actual bounded HolForm / finite-volume regular target hypotheses
must be established in the original instance. One io_i satisfying
IsIoW for EVERY parameter t remains a distinct upstream requirement.
HCU proves full LowSm/LowIrr and the Hilbert map in its stated scope;
it does not assert the complete MMap or supply an arbitrary io_i.

These are useful branches inside the shared C producer. Successful
completion of the analytic packet would still leave geometric
readings, rational tests and base rows unless their original suppliers
are reconstructed as well. Use the separate theta continuation note
for the exact next analytic declarations and ordering of those tasks.

4. OTHER TEN-CUT PRODUCERS THAT REMAIN GENUINE TARGETS

LinkN: prove the actual etaSum bound with its exact dZ0 and same-host
vvTerm, under precisely the original ShaFinOdd and summability guards.
SmallLevelRankEq alone does not supply this denominator statement.

LinkIRR: retain the actual row datum and prove DelpNonneg plus
delp<=exp(-x^(ez/7)) uniformly. The source route linkIRR_of_join_ex /
link_irr uses original label-counting and joined-row hypotheses; the
existing finite consumer is not an independent retained-defect producer.

LinkDIVt: the original period/height comparison has every LinkDIV_at
clause. Source link_brest / wire_sel use the SAME selP, selC, selB,
PrimAll, DivRows3G, DcPtG, row realizations, period/admissibility and
remaining division inputs. A determinant identity or the already
complete MT metric transport alone does not supply this comparison.

LinkG: source link_g starts from common sel and Duty, forms the actual
GroupCompatibilityFamily, and invokes linkG_concrete5. The remaining
human reconstruction must justify the original local lengths,
served-orbit coverage and MeanKappaBound, with one delta(x)->0 before
varying indices. A scalar gain estimate on an unrelated local model
does not provide the selected LinkG.

LinkS: source link_alt retains the same spectral selS and real witness,
WuDecayOfGap, RowsFinDim, the TFrame and counting constants, TypeP,
RowNGP, RowMainEqP, the loop/selected-row estimates, CountAllPoints and
actual genus-instance ties. Its exact normalization is Gamma, with the
mixed/diagonal Hilbert–Schmidt and Dall/Dstar estimates and the original
exponentially small errors. Do not replace this package by a bare
positivity statement. These remaining names identify mathematical
work; no listed subset is asserted a newly proved sufficient AND rule.

The source LinkGl pair itself is no longer the place to spend a new
proof pass: RSL through GFI now reconstruct its required conditional
content. Supplying one of the original common producers above is the
way to make that completed implication contribute to the final theorem.

5. HOST COUNTS AND PARALLEL PRIORITY

HostExW is still supplied by the exact cohomological window route.
For the principal RH target, and more generally a fixed target of
2-power order, the selected cut is I/II/V; CaseIII is vacuous by KA5–6.
Arbitrary Dirichlet targets with odd-order part retain III, SeedIV and
the original chain arguments. The 401 window and x^400 lower floor
are unchanged. CountI's principal Kstar7 field and CountV's Gaussian/
quartic field are distinct; shared rank-three techniques do not identify
their objects. The principal CountV guard only requires e=1 and
ell in {3,7}; a universal CountV supplier is stronger than that endpoint.

The CountII leaf still requires both original rank-four Links, fixed
iota and one coefficient threshold before all later coefficient DVRs
and B/Lambda. Within each Link the SAME ideal J must satisfy the six
Hida fields and P1core. CAP now supplies full original ArPl under CohP
and IsRes for every supplied integral type and QData level. It does not
construct ordinary/control data, that type, same-J HasAut or Raw.

The count continuation identifies a bounded next subtarget: original
NiceI Choice at h=0, a=n=4, retaining the complete target statement.
The absence of an odd block and a possible zero-dimensional Kap reduce
its proposed route to an explicit finite trace/derivation detector.
This is a suggested reconstruction, not a new closed claim. It is a
more bounded parallel step than beginning the full ordinary/control
theory at once. The broad ordinary/control/HasAut producers remain C.

6. STOP RULES FOR THE NEXT RECONSTRUCTION

Choose a next claim by its literal output on the common construction,
or by the number of final-cut inputs it makes available. State the
complete sufficient interface before proving a partial calculation.
Keep producer existence, proof of an implication, and shared-work
refinements distinct. A published theorem is category A only after its
original hypotheses and representation/normalization are matched.

Do not reopen the closed global losses, ChainTied, constant 4, type-prime
constant 36, all-height frame, metric determinant or final 1/2+9epsilon
absorption. Do not add CoverAll, stronger unused Vandermonde families,
full S6Core, or arbitrary-frame generality merely to pursue an available
branch. The optional direct-gap/everyE2 route packages substantial
inputs and is not an independent shortcut around the common producer.
The two top-level D leaves still concern exact polarized-adjoint
matching (AD_VANISH_K_MATCH and HOST_RIGID_S), not formal correctness.

SOURCE LOCATORS FOR THE SHARED GLOBAL ROUTE
Paths below are relative to repository src/. Ranges are inclusive and
hash exact UTF-8 source bytes with their original newlines. Each file
has been compared with the pinned git blob. Named source declarations
are navigation anchors; their presence alone is not a human proof.
'''

ANCHORS = [
('Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean', [(11,31,'UpperTheory.Top.topDesWin: exact ten-input cut')]),
('Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean', [(27,49,'UpperTheory.Top.shapeWin: one common class and selected inputs')]),
('Development/AutomorphicArithmetic/CharacterBoxes/ExS.lean', [(10,12,'UpperTheory.Top.ExS: target host to DesignChoices')]),
('Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean', [(14,28,'UpperTheory.Top.classSel: common class and RawSel')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/NonemptyHypsOfAllRows.lean', [(14,96,'GlobalTheory.Fc.nonempty_hyps_of_allRows: all RowL joins before selection')]),
('Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean', [(190,200,'RecExP: parameter, dimension and level order'),(250,280,'Built, QOf, cls, IsSel, Row and pick')]),
('Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/CmQuadraticFormEqAlternatingForm.lean', [(180,187,'RecAtG and AtLed: original compatible record construction')]),
('Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ColumnCompatibleSelection.lean', [(15,44,'BaseLevelCompatibleSelection, SelDH, columns, spectral and real ties'),(63,88,'Bundle and its literal common-sigma projections')]),
('Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', [(446,478,'NBuilt and NTrue: original constructor certificate and dependent transport')]),
('Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsLowestKTypeFockMapThetaVectors.lean', [(298,311,'GlobalTheory.JointHarm.exists_ioP: one map before every parameter')]),
('Formalism/LocalToGlobal/ClassOfRecordOfChoice.lean', [(34,50,'WithChN, designChoices_upN and D3'),(61,96,'Duty, selected ties and actual real-place second layer')]),
('Formalism/SharpRestriction/DesignExistsOfChoices.lean', [(22,27,'DesignChoices: original whole family contract'),(54,72,'designExists_of_choices: common Closed installation')]),
('Formalism/SharpRestriction/GlobalTheoremInputs.lean', [(25,58,'ShaFinOdd, vvTerm, etaSum, LinkN/Eta, small rank and LinkIRR'),(77,96,'LinkDIV_at, LinkDIV and LinkDIVt'),(122,164,'LinkG, LinkS and final LinkGLOBAL guards')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkGl.lean', [(14,31,'GlobalTheory.Top.link_gl: conditional full-rank/global pair')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkBrest.lean', [(7,25,'GlobalTheory.Top.link_brest: same-selector division remainder')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/WireSel.lean', [(11,41,'GlobalTheory.Top.wire_sel: actual row/rank/period wiring')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkG.lean', [(14,27,'GlobalTheory.Top.link_g: common selector and Duty')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkAlt.lean', [(16,50,'GlobalTheory.Top.link_alt: original spectral inputs')]),
('Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkIRROfJoinEx.lean', [(17,37,'linkIRR_of_join_ex: exact retained-row bound'),(143,164,'GlobalTheory.Top.Irr.link_irr: class installation')]),
]
parts = [BODY]
for rel, anchors in ANCHORS:
    path = args.source / 'src' / rel
    data = path.read_bytes()
    blob = subprocess.check_output(['git','-C',str(args.source),'show',f'{PIN}:src/{rel}'])
    assert data == blob, ('pinned source differs', rel)
    lines = data.splitlines(keepends=True)
    parts.append(f'\n{rel}\nFile SHA256 {sha(data)}\n')
    for start,end,label in anchors:
        assert 1 <= start <= end <= len(lines), (rel,start,end,len(lines))
        block = b''.join(lines[start-1:end])
        parts.append(f'  {label}\n  Lines {start}–{end}; range SHA256 {sha(block)}\n')
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(''.join(parts), encoding='utf-8')
print(args.output)
print('SHA256',sha(args.output.read_bytes()))
print('Words',len(args.output.read_text().split()))
print('Pinned files',len(ANCHORS),'ranges',sum(len(a) for _,a in ANCHORS))
