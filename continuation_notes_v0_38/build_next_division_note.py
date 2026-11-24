from pathlib import Path
import argparse,hashlib,json,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[2]/'lean_source');args=ap.parse_args()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'; HERE=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
IW='src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
AM='src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
refs=[
 ('D01','First versus stronger division records','src/Formalism/LocalToGlobal/Divisibility/DivisionCompatibleToSub2Indef2.lean',210,311),
 ('D02','Original first/second division supplier',IW+'DivisionCompatibleAtReadIdentifications.lean',22,46),
 ('D03','Exact original row projector and scalar normalization',IW+'GoodProjectorSmallestSpaceForms.lean',238,258),
 ('D04','Original translated row-product and ipM route',IW+'IsLiftFlagGroupInv.lean',44,122),
 ('D05','All first-theta li/span/lattice fields and the separate theta square',IW+'LiftCuspFormSpaceThetaMapEqData.lean',19,174),
 ('R01','Original Pins, Holds and complete Read',AM+'StableIffCarrierEq.lean',81,193),
 ('R02','ReadL and one prior ReadC',AM+'StableIffCarrierEq.lean',200,247),
 ('R03','Actual moved reader with all original maps',IW+'ExistsReadingInMovedRowData.lean',154,247),
 ('R04','Rational level-zero side and localized lattice construction',IW+'ExistsSideReadingLevelZeroMoved.lean',68,139),
 ('R05','Same-map row update and two-stage base-side construction',IW+'ExistsSideReadingLevelZeroMoved.lean',141,237),
 ('R06','Final ReadPk.Pin consumer',IW+'ExistsReadingOfRowLiftFamilyMovedData.lean',18,23),
 ('A01','Actual Mult, IsMultIP and ipM fallback','src/Formalism/LocalToGlobal/IndefiniteReal/ScalarOnPartsFull.lean',82,101),
 ('A02','Per-finite-coset smooth growth','src/Formalism/LocalToGlobal/BesselHermitianTheta/TiedSmooth.lean',42,49),
 ('A03','Global adelic height and IsUnifModerate','src/Development/AbelianVarietyTheory/BlockTheory/HeightDefect/WordDerivatives.lean',114,130),
 ('A04','Polynomial unitary reduction and global growth conversion','src/Development/AbelianVarietyTheory/Proofs/HeightProofs/ExistsSigmaList.lean',386,534),
 ('A05','Source universal cuspidal rapid-decay predicate','src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/ExistsNormLeHeightPow.lean',28,32),
 ('T01','Original LiftTestB rationality contract','src/Formalism/LocalToGlobal/IndefiniteReal/RationalAdjoints/RatZOfTests.lean',26,29),
 ('T02','Actual twisted FW basis and finite tests from RatG','src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/LiftTestBOfRatG.lean',25,75),
 ('T03','Exact original RatG sufficient clauses','src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ThetaLiftsOfRationalFormsRationalOfClauses.lean',25,40),
 ('T04','Joint rational tests and MLat consumer','src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LiftTestsModularLatticeOfCoreCompatibility.lean',18,31),
]
records=[]
for i,title,path,a,b in refs:
 raw=(args.source/path).read_bytes();assert raw==subprocess.check_output(['git','-C',str(args.source),'show',PIN+':'+path]);ls=raw.splitlines(keepends=True);assert 1<=a<=b<=len(ls),(path,b,len(ls)); block=b''.join(ls[a-1:b]);records.append(dict(id=i,title=title,path=path,line_start=a,line_end=b,file_sha256=sha(raw),range_sha256=sha(block),url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{b}'))
text=r'''NEXT DIVISION AND COMMON READINGS — v0.38
22 November 2026

Standing premise: the pinned Alpoge–Claude Lean proof is fully checked and
correct. This is a source-anchored continuation plan for the human proof,
not a new theorem or a declaration that a whole remaining leaf is closed.
Source pin: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
All component and Lean paths below are relative to the released reconstruction
and the source repository, respectively. The source appendix binds exact bytes.

1. COMPLETED WORK THAT SHOULD BE REUSED

The new division_identity/ chapter DI1–DI21 has passed independent review.
It reconstructs the actual compact-polynomial/Sobolev separation argument,
the finite model and level-character transport, and the literal StepLev and
TopLev equations on both full levels. Those step/terminal identities need the
original HarishChandraModules, Pins/Holds and stored-chain inputs; they do not
need the additional row-pair integrability premise below. DI11–DI15 then prove
the exact RowProj, both composite theta/good-projection equations, the actual
Pq projection formula and both RowSideDef3 records. DI16–DI19 prove the first
ThDef3.li/span/lat, including integral descent to the original norm-defined
K-form and the original lattice generators. No unrelated isomorphic lattice
or basis has replaced the given objects. [D01–D05]

DI20 assembles every field of the first DivDef3. DI21 applies it pointwise to
the exact CSR-updated R', F', Y', Z', C' and sEE. Both full row metrics and
both measures survive unchanged. ReadC is still fixed before the later
TwArgs, and the original universal NEb and outer eventual-threshold order
are preserved. This removes the unexpanded first-division identity from the
CSR consumer in favor of explicit retained producers. The finite joins in
CSR1–CSR22 and the completed global slope/final assembly should not be
reconstructed again.

This is a SUFFICIENT CONDITIONAL REFINEMENT, not yet the source's first
output from its original premises alone. DI uses an explicit additional
RowPairInt input. The originally planned shortcut from IsAutFunSm.growth to
the hypothesis of CuspRapidDecay was not justified by existing human proofs:
its source supplier uses polynomial unitary reduction. The chapter, closure
file and independent review all retain that boundary. No further whole
selected-leaf closure is claimed by DI.

The analytic packet FV/SBD now supplies the original target FinPair and
initial seed boundedness, hence the original all-parameter theta extension
and thF through the inherited SPR/JIO/CFB consumer. Those two initial analytic
gates are no longer open. This does not produce arbitrary common geometric
readings, arbitrary full IsCuspFun rapid decay, or the whole stored chain in
Holds.aux.ex. The same underlying R and all remaining original laws are still
needed. See next_analytic_and_common.txt for the FV/SBD certificate scopes.

2. NEXT PRIMARY TARGET: THE ACTUAL LEVEL-ZERO SIDE AND MOVED READER

The highest-sharing next target is the original read_of_moved route, starting
with its actual level-zero rational side. It feeds the common Bundle, base
theta interpretation, division records and later local/second-layer data.
This is preferable to proving another record-assembly implication between
already supplied readers. The common geometric/automorphic realization is
still a C producer; the bounded coordinate/lattice subarguments are plausible
B work, not already proved closures. [R01–R06]

The exact original endpoint is
  ExistsReadingInMovedRowData.lean : read_of_moved.
For the given B, f, T, w, Z0, hX, Wt, z0, q, o and m:Moved(o), the output Y
must preserve the literal tup, tupT, PY, PW, both jA/jA0 maps, eMt, finite type
representations, both Ish/Iz embeddings, the lift map mj.eW and every IL.jMt.
The source constructs them from the SAME m.y, m.t.ch, m.t.tA and m.t.lf.
It uses rowIdentifications_realRowSide_of_chainComparison at both levels,
liftIdentifications_of_liftsComparison, the original finite type equivalence,
and the NumOK and Fits fields. A finite-dimensional equivalence preserving
only rank would not establish this endpoint. [R03]

A concrete first deliverable is the source chain in
ExistsSideReadingLevelZeroMoved.lean:
  reading_level_zero_of_side_data;
  exists_hlat and reRow/RRset_reRow;
  exists_good and read_of_good;
  exists_side_reading_level_zero.
The bounded construction is quite explicit. Start with the actual complex
basis and the actual matrices Xo at every infinite place. Build the rational
coordinate map by that same basis. At the distinguished embedding use its
actual Hilbert Gram form, and retain Xo at every other place. Define the
integral lattice by the displayed local intersection of localized spans of
the original RRset; its membership must be exactly the existence of a
multiplier outside the specified prime. The reRow update must preserve the
original downTo, iota and RRset maps, not only their ranges. [R04–R05]

The source's exists_good performs this side construction twice: the first
side supplies the actual RRset for the second, and RRset_side identifies the
sets without a circular new choice. After that, read_of_good takes the actual
sharp-side Fits.div identification and both SAME Y.Ish/Y.Iz equalities, and
returns RationalReadingWithoutCongruence. The original jW is supplied by
CoordW.exists_jW under the same Pins/Holds. Neither that rationality nor all
the input RrT/base-change data should be inferred simply from finite dimension.
The next author should give a complete field-by-field proof of this bounded
chain and separately list any still-unreconstructed producer used by rrT_exists
or the original coordinate jW. [R04–R05]

Only then join to read_of_moved and the six-line readPk_pin_exists consumer.
Keep Inputs, Fits, Moved and the same side chosen before the later reading.
This plan is not a claim that supplying the moved data themselves is elementary.
The underlying original core, geometry, comparison chain and multiplicity
support are still substantial inputs. [R01–R06]

3. A SMALL ANALYTIC SIDE TARGET THAT COMPLETES THE DI CONSUMER

The exact retained DI.3a contract is RowPairInt. For every original Boolean
level b and tuple t, every w in the full P_b-level Mult for MY 0 and every c
in its original goodPart, every pair of smooth tensor tuples v,v', and every
h in the finite residual group G, prove integrability of

  g ↦ conjugate(A_(R.eG h)(c(v))(g)) · w(v')(g)

on the unchanged fd0 with

  mu_b = ofReal(nP(F,b)^(-1)) • nu0.

A is the literal flag-normalized finite right translate. Identity and inverse
residual elements are included. Right invariance gives the adjoint-translate
products, and finite summation then gives the e0 products. There is no separate
integrability premise for e0 and no need for a new nonzero Schur scalar.
DI12 equates the actual IsMultIP witness sets, retaining the empty-set ipM=0
fallback as well as the nonempty unique-scalar case. [D03–D04,A01]

One clean sufficient target is L2 membership for every scalar value of these
original row MMaps at the same measure and domain. Cauchy–Schwarz and finite
right translation then give all of RowPairInt. This is stronger than the
printed pair contract, but much narrower than the entire source predicate
CuspRapidDecay and its global quotient-height estimate.

The precise obstacle in the longer source route is now exposed:
  TiedSmooth.IsAutFunSm.growth bounds each finite coset with normInf;
  WordDerivatives.IsUnifModerate uses the global adelic height;
  ExistsSigmaList.growth_iff passes between them using reduction.
The reduction declaration and its polynomial estimates have not been
reconstructed in the existing human ledger. Do not cite growth_iff as if its
name were a human proof. [A02–A05]

An alternative bounded route may adapt FV's actual finite-level arithmetic
components and SBD's center-finiteness/Miller–Schmid argument to these row
values. It would still have to prove the actual full IsCuspFun-to-classical
parabolic dictionary and enveloping-center finiteness on the original row
module. SBD proved these for the constructed extremal seed with its strong
ZCusp conditions; that result cannot be generalized by changing the label
of an arbitrary MMap. This is proposed work, not a checked published
application. Preserve the original MY 0, full P_b characters and both levels
throughout. [A01–A05]

4. RATIONAL TESTS AND THE STRONGER DIVISION OUTPUT ARE SEPARATE

The first DivDef3 does not contain thTheta or the full row rational-lattice
comparisons. The second DivRows3 has sharpRR, baseRR, divisionRows_rationalLift,
thTheta, num and colsBk. Its complete source supplier still requires its
own actual MjHTie, IdxDefs, BuRational and BtVanish inputs as applicable.
No field is supplied merely by the first-output theorem. [D01–D02,D05]

For the small-level rank route, the narrower BTH/SLR consumer remains the
better target: base RowsHold0_3 and the base theta square on the same P and
mu0. The needed base rational-test restriction keeps all original rational
source vectors and target-coordinate vectors, but fixes the source tuple
at mu0. It does not require all higher-lambda rows or every tuple merely
because the larger source package contains them. RowsHold0_3 remains a
separate primitive-row producer.

LiftTestBOfRatG provides a concrete finite test family in the actual twisted
FW basis once the SAME phase-correct RatG and rational model are supplied.
The real mathematical work is rationality of the actual theta images in the
fixed embedded field, including the prescribed phase/determinant twist.
An arbitrary complex basis and separation by coordinate functionals do not
prove this rationality. [T01–T02]

The nearest exact source producer ratG_of_clauses retains:
  8 f r + 4 ≤ nV; Hk3.Core on the original R,F;
  tup_mu_off and tup_mu_used;
  the original FWTie, OMPins and PhaseTie;
  IoExt, OneMapRow0, QGuard and LUnif;
  EvInj and CoverField.
It obtains the actual normalized tuple data, all-tuple lift span and field-
valued OneMap before the final rationality conclusion. The complex JIO/CFB
coefficient bridge and completed analytic extension do not automatically
supply those geometric/field-descent assertions. LiftTests_and_mLat_of_ties
joins this branch only after the exact rational inputs are available.
Keep ratG/MLat separate from the completed first-DivDef3 consumer. [T03–T04]

5. WHAT THIS PRIORITY DOES AND DOES NOT CHANGE

The next common-reader work should preserve one R, one prior ReadC, both
original row metrics/lattices, the original periods and ColPins, and the
whole dependent tuple/character/reading packet. It should aim to deliver an
original producer used by several topDesWin interfaces. It must not create
separate witnesses for SmallLevelRankEq, LinkDIVt, the second layer and
LinkGLOBAL. The final ten-input cut remains DesignExists plus its nine
Closed predicates on one class, then one shared family and selector.

The remaining multiplicity/parts/logLam and ray-reciprocity producers,
original host datum and all-embedding constraints, true local certificate,
second-layer compatible columns/Duty, and common RawSel are not consequences
of this note. The nested source-matching D boundaries remain. Full global
slope/final assembly is already reconstructed at its conditional scope.
The new CRW packet similarly closes important original full-block algebraic
subproducers, but retains coefficient/pro-ell normalization, actual Lim and
compatible patching/support before the h=0 Raw conclusion. It does not
supply the common geometric readers or change the count branches:
RH still needs I, II and V; unrestricted Dirichlet GRH also needs III.

Recommended next deliverable: the complete actual level-zero rational-side
constructor and read_of_moved, with a source-exact list of the remaining
geometric/automorphic producers. In parallel, RowPairInt on its literal
row family is a well-bounded analytic target. After a reader is installed,
base RatG/LiftTestB is the most direct shared target for the theta-square
and rank route. Do not expand to the stronger DivRows3 solely to follow the
most recently reconstructed branch.

FROZEN DI PROOF BINDINGS

main.tex SHA256:
fd391a1ec3f7698332e2f5449dce389d0e518e7f6f062b36afbfb8f83581db54
provenance.json SHA256:
1449a8a6793eea1678818df70fd72c6ab03c537cae3ccdb38edb372ebd4bd243
closure.json SHA256:
373c13fdd0285ccb840eb97c72517e108ac1284c896b1411adc480dd008c87cd
Independent DI1–DI21 review: PASS, no required correction.

SOURCE APPENDIX
'''
for r in records:
 text+=f"\n[{r['id']}] {r['title']}\n{r['path']}:{r['line_start']}-{r['line_end']}\nFile SHA256 {r['file_sha256']}\nRange SHA256 {r['range_sha256']}\n{r['url']}\n"
(HERE/'next_division_and_readings.txt').write_text(text)
(HERE/'next_division_and_readings_sources.json').write_text(json.dumps(dict(source_commit=PIN,note_sha256=sha(text.encode()),source_ranges=records),indent=2)+'\n')
print('note_sha256',sha(text.encode())); print('source_ranges',len(records)); print('words',len(text.split()))
