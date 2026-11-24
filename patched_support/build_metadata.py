#!/usr/bin/env python3
"""Bind PMS human proofs to the pinned source and exact inherited/peer bytes.

python build_metadata.py --source /path/to/lean_source \
  --human-root /path/to/reconstruction_v039 --peer-root /path/to/work_v040

Only this component directory is written.  No Lean is built or replayed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
ap.add_argument('--human-root', type=Path, default=HERE.parent.parent/'reconstruction_v039')
ap.add_argument('--peer-root', type=Path, default=HERE.parent)
args = ap.parse_args()
REPO, HUMAN, PEER = args.source.resolve(), args.human_root.resolve(), args.peer_root.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=REPO, text=True).strip() == PIN
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P = B+'PatchingModules/'
H = P+'AnnihilatorBaseChange/'
A = B+'AlgebraTools/'
CH = B+'CommutativeAlgebraHeight/'
IC = 'src/Development/AutomorphicArithmetic/IntegralCasts/CapelliIdentities/'

# Inclusive ranges.  End 0 is expanded to the actual final line and bound.
SPECS = [
 ('S5', P+'PatchedSupportCompletions.lean', 23,70,
  'kjIdeal; every field of PatchedSupportCompletions; full S5 quantifiers'),
 ('PMOD', H+'SpecializationMapCompUniversalSection.lean', 13,32,
  'Every IsYCpl and PMod field'),
 ('ULTRA', A+'UltraDefs.lean', 7,0,
  'Original ULim quotient, QRegAt, quotient/tower conventions'),
 ('ULTRA', A+'ULimKer.lean', 7,0,
  'ULim.mem_smul_top_iff: finitely generated ideal criterion'),
 ('ULTRA', A+'ULimTrans.lean', 7,0,
  'ULim transition surjection and exact ideal kernel'),
 ('CONSTANT', A+'ULimConst.lean', 7,0,
  'Constant ultralimit of a finite complete coefficient module'),
 ('PAIR_ULTRA', H+'ExistsUltraLimitPairOfEventualQuotientMaps.lean', 7,0,
  'Diagonal finite-level paired maps to actual ULim maps'),
 ('QR', H+'QuotientRegularAtOfQuotientFreeOverPowerSeries.lean', 10,0,
  'quotientRegularAt_of_quotient_free_over_powerSeries'),
 ('QR', A+'QRegPS.lean', 7,0,
  'Formal power-series homogeneous coefficient independence'),
 ('QR', A+'QRegLim.lean', 7,0,
  'Quasiregularity at every degree below k on the ultralimit'),
 ('QR', A+'QRegScal.lean', 7,0,
  'Quasiregularity under the actual scalar changes'),
 ('TOWER', A+'TowerFin.lean', 7,0,
  'exists_tower_limit: finite compatible limit with every exact quotient'),
 ('TOWER', A+'TowerCompl.lean', 7,0,
  'Actual completed-ring action and tower construction'),
 ('TOWER', A+'QRegTower.lean', 7,0,
  'Exact quotient kernels give the full quasi-regular sequence'),
 ('PATCHED', A+'Patched.lean', 7,0,
  'Localized ULim tower, module and annihilator criterion'),
 ('YCPL', H+'YCplMemOf.lean', 8,0,
  'yCpl: Noetherianity, unit, density and strictness'),
 ('FIBER', H+'FibEquiv.lean', 7,0,
  'Actual BB-linear special-fiber equivalence'),
 ('NIL', H+'ExistsPowMaximalIdealSmulFiniteEqZero.lean', 7,0,
  'Finite quotient bound with exponent before the level event'),
 ('NIL', H+'PmodEx.lean', 7,0,
  'pmodEx: exact complete PMod from the three finite-level inputs'),
 ('YPRIME', H+'YPrime.lean', 7,0,
  'yPrime: prime contraction and same original local completion'),
 ('PMFIB', H+'PmFib.lean', 7,0,
  'pmFib: support iff exact original-fiber annihilator inclusion'),
 ('PMMOVE', H+'PmMove.lean', 7,0,
  'pmMove: exact contraction equality in the new completion'),
 ('LAFREE', A+'CaCplModfree.lean', 7,0,
  'finite_free_baseChange endpoint on the actual coefficient and ring completions'),
 ('LAFREE', IC+'FlatnessPrecompleteProducts.lean', 7,0,
  'Original finite-free completed module supplier, independently reconstructed in PMS12'),
 ('DIM', H+'PmDimQuot.lean', 13,149,
  'pmDim_quot, pmDim_step and pmDim: every minimal support component'),
 ('DIM', A+'CaCmPatch.lean', 7,0,
  'Original patched_depth_dim endpoint replaced by the PMS13-PMS14 basis argument'),
 ('OUT', H+'OutOfNil.lean', 7,0,
  'outOfNil: quotient completions and all support fields'),
 ('OUT', P+'AutomorphicDetection/AnnBc.lean', 7,0,
  's5_lemma and full s5 assembly'),
 ('LADIM', H+'LaDimArith.lean', 7,0,
  'laDim for the actual normalized Unit coefficient map'),
 ('COEFFICIENT', P+'ThetaCoefficientMapEq.lean', 76,136,
  'Sinf, ordered q1El/q2El/fEl and exact splitting/del ideals'),
 ('TW', P+'ThetaCoefficientMapEq.lean', 12,45,
  'Every TWGrp field and literal ProL'),
 ('TW', P+'ThetaCoefficientMapEq.lean', 170,237,
  'Every TWBase, TWRing, TWMaps and TWAut field'),
 ('LIM', P+'ThetaCoefficientMapEq.lean', 262,299,
  'Close and every original Lim field, including uniform incoming/outgoing maps'),
 ('RM', H+'SpecializationMapCompUniversalSection.lean', 36,101,
  'Actual Ph0/pi0 maps, every Tup/RRObj/RMaps field and all-series identities'),
 ('REL', H+'SpecializationMapCompUniversalSection.lean', 103,143,
  'All six Rel constructors, ii/fo and actual MN/X0 actions; approximate annihilator'),
 ('SEES', H+'SpecializationMapCompUniversalSection.lean', 155,0,
  'Sees compares all group-algebra elements and every characteristic coefficient'),
 ('XFREE', H+'PatchedModuleFreeFiniteOverIwasawaAlgebra.lean', 7,0,
  'Actual X0 finite/free and coefficient/y action identities'),
 ('FREEN', H+'FreeNQuot.lean', 7,0,
  'freeNQuot for every k,j and the original finite-level rank'),
 ('SEES', H+'LamEqOfKer.lean', 7,0,
  'dSees via full determinant finite-quotient coefficients'),
 ('SEES', H+'PhSees.lean', 7,0,
  'Ambient open-normal subgroup inside Ph0 for all coefficient comparisons'),
 ('SEES', CH+'ExistsOpenNormalSubgroupKillsOfGroupDetLawIsCont.lean', 7,0,
  'Integral full-law finite quotient and uniform open-normal kernel'),
 ('RREXT', H+'RrExt.lean', 7,0,
  'rrExt: full tuple uniqueness from every group characteristic coefficient'),
 ('PICONG', H+'PiCong.lean', 7,0,
  'piCong: one event before every ring element and every pair of root-series lifts'),
 ('SPCONG', H+'SpCong.lean', 7,0,
  'Actual common formal quotient and its module isomorphism'),
 ('FOCONG', H+'FoCong.lean', 7,0,
  'foCong includes exact ell^j divisibility and finite-level factor equality'),
 ('PAIRS', H+'EventuallyExistsPatchedModuleQuotientMaps.lean', 7,0,
  'Paired quotient maps: actual R-linearity and both f composites'),
 ('CLOSE', H+'CloseLift.lean', 6,0,
  'closeLift with exact inverse-first coset orientation and fixed old lift'),
 ('KERREL', H+'PatchedTraceSingleMulSubOneApproxAnnihilated.lean', 7,0,
  'Kernel relation: same-coset approximate exact annihilator'),
 ('POLREL', H+'PatchedLamConjTwistApproxAnnihilated.lean', 7,0,
  'Polarization relation: original inverse and integer cyclotomic exponent'),
 ('ORDREL', H+'PatchedTraceLocalCharPolyApproxAnnihilated.lean', 7,0,
  'Every original ordered local relation, exact character components'),
 ('INEREL', H+'EventuallyTraceInertiaCongruenceOfAdapted.lean', 7,0,
  'Actual residual inertia subgroup from Adapted and level compatibility'),
 ('QREL', H+'MapRingHomSingleMulCharpolyElement.lean', 7,0,
  't3Q1: actual finite-level rel1 with same exponent'),
 ('QREL', H+'MapRingHomSingleMulPartialCharpolyElement.lean', 7,0,
  't3Q2: ordered partial polynomial and y with same exponent'),
 ('T3', H+'T3Of.lean', 7,0,
  't3Of: single exponent A.ex+1 before relation and precision'),
 ('PIKER', H+'CharpolyElementEqAevalGroupElement.lean', 12,0,
  'piKer: all six generators, with q1 Cayley-Hamilton trace identity'),
 ('PISURJ', H+'PiSurj.lean', 7,0,
  'piSurj: literal GenBy plus actual splitting roots, complete-ring surjectivity'),
 ('ANNJ', H+'PatchedModuleAnnihilatorLeComapIffIdealLe.lean', 7,0,
  'annLeJ: actual Ann_R X0 iff original J at every splitting prime'),
 ('PAIR', B+'WeilGroupCharacters/UniversalOrdinaryDeterminantRing.lean', 107,166,
  'Residual inertia Ip, complete Pair and Pair.Maps polynomial-law fields'),
 ('DET', B+'WeilGroupCharacters/RepAlg.lean', 9,105,
  'Actual natural homogeneous multiplicative Det/GDet, chi, lambda_i with Nat subtraction, trace and base change'),
 ('GEN', P+'ThetaCoefficientMapEq.lean', 127,144,
  'pairGens, qGens, actual pairVals and StOrTh'),
 ('GEN', P+'PairedDualFirstOrderDualMatrixSpace.lean', 359,361,
  'Literal GenBy quantifier and actual topological polynomial approximation'),
 ('CORE', P+'PatchedSupportCompletions.lean', 112,213,
  'All OoPt/Pt fields, Adapted, exact Core/CoreBC/Raw and ChainConcl'),
 ('CORE', P+'AutomorphicDetection/LiftPt.lean', 7,0,
  'Original actual Core consumer and S5 support installation'),
 ('OUTER', B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/LinkTwo.lean', 13,51,
  'Both rank-four Links and original same-ideal Hida/P1 conditions'),
 ('OUTER', B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/PotentialModularityTower.lean', 38,66,
  'Fixed iota followed by one common coefficient threshold'),
 ('OUTER', P+'TaylorWilesObstructionBound.lean', 23,31,
  'Complete original CohP'),
 ('OUTER', P+'TaylorWilesObstructionBound.lean', 115,154,
  'Original LocCFT, same-J HasAut and PfromAut'),
]
cache, sources, groups = {}, [], {}
for group,path,first,last,decl in SPECS:
    if path not in cache:
        raw=(REPO/path).read_bytes()
        assert raw == subprocess.check_output(['git','show',f'{PIN}:{path}'],cwd=REPO),path
        cache[path]=raw
    raw=cache[path]; lines=raw.splitlines(keepends=True)
    last=last or len(lines)
    assert 1<=first<=last<=len(lines),(path,first,last,len(lines))
    block=b''.join(lines[first-1:last])
    item=dict(id=f'PMS_SRC_{len(sources)+1:03}',group=group,path=path,
      declaration=decl,line_start=first,line_end=last,sha256=sha(raw),
      full_file_sha256=sha(raw),range_sha256=sha(block),range_bytes=len(block),
      source_commit=PIN,url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{first}-L{last}')
    sources.append(item); groups.setdefault(group,[]).append(item['id'])

def proof_block(raw,cid):
    lines=raw.splitlines(keepends=True)
    starts=[i for i,l in enumerate(lines) if l.strip()==f'% BEGIN {cid}'.encode()]
    ends=[i for i,l in enumerate(lines) if l.strip()==f'% END {cid}'.encode()]
    if starts:
        assert len(starts)==len(ends)==1,cid
        a,b=starts[0],ends[0]
    else:
        lab=next(i for i,l in enumerate(lines) if f'\\label{{claim:{cid}}}'.encode() in l)
        a=max(i for i in range(lab+1) if b'\\paragraph{' in lines[i])
        b=next((i-1 for i in range(lab+1,len(lines)) if b'\\paragraph{' in lines[i]),len(lines)-1)
    assert a<b,cid
    block=b''.join(lines[a:b+1])
    return dict(id=cid,line_start=a+1,line_end=b+1,sha256=sha(block),bytes=len(block))

CG={
 1:['S5','PMOD'],2:['ULTRA'],3:['S5','CONSTANT','PAIR_ULTRA'],
 4:['QR','ULTRA'],5:['PATCHED','TOWER','YCPL'],6:['TOWER','PATCHED'],
 7:['QR','TOWER','FIBER','PATCHED'],8:['NIL','PMOD'],
 9:['YPRIME','YCPL'],10:['PMFIB','FIBER'],11:['PMMOVE','YPRIME'],
 12:['LAFREE','DIM'],13:['DIM','QR','FIBER'],14:['DIM'],
 15:['S5','OUT','PMOD'],16:['LADIM','COEFFICIENT','CORE'],
 17:['TW','LIM','RM','REL','COEFFICIENT'],18:['XFREE','TW','RM'],
 19:['FREEN','TW','RM','COEFFICIENT'],20:['SEES','RREXT','RM','DET'],
 21:['PICONG','TW','LIM','RM','SEES'],22:['SPCONG','FOCONG','TW'],
 23:['PAIRS','SPCONG','PICONG','FOCONG','RM','TW'],
 24:['CLOSE','LIM'],25:['KERREL','POLREL','REL','RM','PAIR','DET'],
 26:['ORDREL','INEREL','REL','RM','PAIR','CORE'],
 27:['QREL','REL','TW','RM'],28:['T3','REL','FOCONG'],
 29:['S5','PMOD','REL','CORE'],30:['PIKER','REL','RM','PAIR','DET'],
 31:['PISURJ','GEN','RM','TW'],32:['ANNJ','CORE','OUTER','TW'],
}
DEP={
 1:[],2:['PMS1'],3:['PMS1','PMS2'],4:['PMS1','PMS2'],
 5:['PMS1','PMS2','PMS3','PMS4'],6:['PMS5'],
 7:['PMS4','PMS5','PMS6'],8:['PMS1','PMS3','PMS7'],
 9:['PMS5'],10:['PMS1','PMS7'],11:['PMS9','PMS10'],
 12:['PMS9','PMS10'],13:['PMS7','PMS9','PMS12'],14:['PMS13'],
 15:['PMS8','PMS9','PMS10','PMS11','PMS12','PMS13','PMS14'],
 16:[],17:['LIM18','PRG13','PRG14','PRG18','PRG24'],
 18:['PMS17','PRG18'],19:['PMS17'],20:['JSP9','PRG2','PRG14'],
 21:['PMS17','PMS20','PRG18'],22:['PMS17'],
 23:['PMS8','PMS18','PMS21','PMS22'],24:['PMS17'],
 25:['PMS17','PMS20','PMS24'],26:['PMS17','PMS20','PMS24'],
 27:['PMS17','PMS20','PMS24'],28:['PMS22','PMS25','PMS26','PMS27'],
 29:['PMS15','PMS16','PMS17','PMS18','PMS19','PMS23','PMS28'],
 30:['PMS17'],31:['PMS17','PRG2','PRG18'],
 32:['PMS10','PMS16','PMS29','PMS30','PMS31'],
}
HYP={
 1:['Exactly the full S5 ring, coefficient, module, ultrafilter and three finite-level hypotheses; X need only be finite for PMod, and is free for S5.'],
 2:['One filter containing every tail; antitone ideals; the ideal A is finitely generated. No countable completeness of the ultrafilter.'],
 3:['X finite over complete Noetherian local L0 with finite residue field; yX=0 and exact coefficient action; paired maps at every precision on allowed large events.'],
 4:['Original all-series free quotient, with rank allowed to vary at every level; every degree a<k.'],
 5:['Same ultrafilter quotient modules; S=R_f and the actual I-adic completion; no locality of BB assumed.'],
 6:['Complete coefficient ring, exact tower kernels A^k, A^k P_k=0, finite first quotient; no prior finite generation of the higher terms or the limit.'],
 7:['Exact same tower and homogeneous independence; fiber scalar action retained over all BB, not merely S.'],
 8:['Finite residue quotients and paired composites f; one annihilator exponent before all generators/precisions/levels.'],
 9:['q prime, y in q, f not in q; actual BB completion of R_f, all structural maps preserved.'],
 10:['Finite modules and arbitrary ring base change; Q contains all y for the special-fiber equivalence.'],
 11:['All original i,i-prime,Z,Q movement hypotheses; same contracted prime in R/ii; faithful flatness only at the specified local completion.'],
 12:['X finite free over L0; p=q intersect L0; actual local completions La and C; zero fiber included.'],
 13:['Actual C finite module N; exact free La-fiber, flat base change of quasiregularity, y in m_C; separated y-completeness proved, not assumed.'],
 14:['La regular local of original dimension d; nonzero N handled by actual formal-series basis; zero N has no minimal support prime.'],
 15:['Every literal S5 antecedent, arbitrary point index set, common coefficient dimension d; full move retained.'],
 16:['Actual O coefficient DVR, finite field K, surjective O->K and normalized Unit s->t; original D remaining coefficient variables.'],
 17:['Original supplied TWAut on B,J and actual constructed RRObj/RMaps; same T/Lim/U and all-level modules; T.ProL and Adapted retained.'],
 18:['Actual TWBase finite-free coefficient module and PRG full SpoCo; same original actions.'],
 19:['Exact original TWRing, a_Nj>=N, all-series action; N>=j+k supplies each k,j quotient, no uniform rank required.'],
 20:['Original continuous determinant polynomial laws over arbitrary coefficient algebras; JSP9 integral word identity; original complete tuple universal property; all source i>n reduce to signed lambda_n because of Nat subtraction.'],
 21:['T.ProL, Adapted and full Lim/RMaps/TWMaps; event chosen before every ring element and every lift.'],
 22:['Same formal root variables and quotient module killed by coefficient ideal; exact ell^j divisibility, not only m_R^j congruence.'],
 23:['Same base module, every original TWMaps semilinearity and composite field, full uniform piCong; no compatible cross-level choice assumed.'],
 24:['Exact original Close orientation and equality ker(pi_N)V=ker(pi_o)V; V normal and contained in Ph0.'],
 25:['Every original kernel/polarization generator; n>=1; same ct, cyclotomic character and exponent 1-n.'],
 26:['Every ordered ordinary tuple and inertia generator; exact original Adapted and residual compatibility; no factor permutation.'],
 27:['Both full original auxiliary-prime relations with the one A.ex; same ph/ta/U/y and module.'],
 28:['All six original generators; one e=A.ex+1 before generator/precision/level; same ideal ii and actual actions rho_N.'],
 29:['Same original TWAut, Lim, RRObj/RMaps with ProL and Adapted; n>=1. Arbitrary support centers require the original prime/y/ii/f guards; normalized dimension requires O->K onto and Unit->t.'],
 30:['Homogeneous multiplicative determinant law, n>=1, arbitrary scalar algebra; actual RMaps and Adapted. ProL is not used for piKer.'],
 31:['Literal GenBy(pairVals union original Unit), full same RRObj/RMaps/SpoCo and adapted data; complete local coefficient category with identical residue field.'],
 32:['Same piSurj and original TWBase.supp for this J; actual lifted point and distinct roots remain explicit interface inputs; both rank-four Links and outer fixed-iota/common-threshold order unchanged.'],
}

APPS=[
 dict(id='PMS_NOETHERIAN',primary_url='https://stacks.math.columbia.edu/tag/00FM',
  theorem_locators=['Lemmas 10.31.1, 10.31.2 and 10.31.4'],
  precise_import='Finite-variable formal power-series rings, finite algebras and localizations of Noetherian rings are Noetherian; submodules of finite modules are finite.',
  hypotheses_checked=['R and L0 are Noetherian by S5; O is a DVR; all variable sets are finite.','The faithful action algebras are submodules of explicit finite free endomorphism modules.'],
  uses=['PMS1','PMS5','PMS12','PMS14','PMS16','PMS18'],primary_retrieval_refs=['turn575486168view2']),
 dict(id='PMS_COMPLETION_FINITE',primary_url='https://stacks.math.columbia.edu/tag/00MA',
  theorem_locators=['Lemma 10.97.1'],
  precise_import='Completion is exact on finite modules over a Noetherian ring and equals tensoring with the completed ring.',
  hypotheses_checked=['Used rings are L0, R_f, R_q or their Noetherian finite quotients.','All modules in these applications are finite: X, fixed quotient rings, completed finite modules and their finite quotients.'],
  uses=['PMS1','PMS3','PMS9','PMS12','PMS13','PMS15'],
  primary_retrieval_refs=['turn969976420view1']),
 dict(id='PMS_COMPLETION_FLAT',primary_url='https://stacks.math.columbia.edu/tag/00MB',
  theorem_locators=['Lemma 10.97.2'],
  precise_import='Noetherian ideal-adic completion is flat.',
  hypotheses_checked=['The source for the localized support completion is the actual Noetherian (BB)_(qBB).','Flatness is used for the quasiregular graded-piece scalar extension.'],
  uses=['PMS9','PMS13'],primary_retrieval_refs=['turn969976420view2']),
 dict(id='PMS_COMPLETION_QUOTIENTS',primary_url='https://stacks.math.columbia.edu/tag/031C',
  theorem_locators=['Lemma 10.97.4'],
  precise_import='Completion is complete for the extended ideal and has unchanged quotients by its powers.',
  hypotheses_checked=['R_f is Noetherian and I=(y) has finitely many generators.','Every local completion is at its specified maximal ideal.'],
  uses=['PMS1','PMS5','PMS6','PMS9','PMS12','PMS15'],
  primary_retrieval_refs=['turn149047391view0']),
 dict(id='PMS_COMPLETION_NOETHERIAN',primary_url='https://stacks.math.columbia.edu/tag/05GH',
  theorem_locators=['Lemma 10.97.5'],
  precise_import='An ideal completion is Noetherian and complete when the quotient is Noetherian and the ideal is finitely generated.',
  hypotheses_checked=['For BB the ring R_f is Noetherian and the y-ideal is finitely generated.','For every local completion the original local ring is Noetherian.'],
  uses=['PMS1','PMS5','PMS9','PMS15'],primary_retrieval_refs=['turn575486168view1']),
 dict(id='PMS_FAITHFUL_LOCAL_COMPLETION',primary_url='https://stacks.math.columbia.edu/tag/00MC',
  theorem_locators=['Lemma 10.97.3'],
  precise_import='Completion of a Noetherian local ring at its maximal ideal is faithfully flat.',
  hypotheses_checked=['The ring is the actual localization (BB)_(qBB).','The completion ideal is its maximal ideal and hence lies in its Jacobson radical.'],
  uses=['PMS9','PMS11'],primary_retrieval_refs=['turn969976420view3']),
 dict(id='PMS_KRULL_INTERSECTION',primary_url='https://stacks.math.columbia.edu/tag/00IP',
  theorem_locators=['Lemma 10.51.4'],
  precise_import='For a finite module over a Noetherian local ring, powers of a proper ideal have zero intersection.',
  hypotheses_checked=['C is an actual Noetherian local completion.','N and N/I^kN are finite C-modules; the ideal is m_C.','This proves each I^kN is m_C-adically closed before claiming y-adic completeness.'],
  uses=['PMS13'],primary_retrieval_refs=['turn575486168view0']),
 dict(id='PMS_FINITE_ALGEBRA_FACTORS',primary_url='https://stacks.math.columbia.edu/tag/0325',
  theorem_locators=['Lemma 10.160.2'],
  precise_import='A finite algebra over a Noetherian complete local ring is a finite product of Noetherian complete local rings.',
  hypotheses_checked=['La is the actual completion of (L0)_p.','E=R/Ann_R X is proved finite over L0 using its faithful endomorphism action.','E_p tensor La is finite; reduction modulo p identifies exactly the original primes over p.'],
  uses=['PMS12'],primary_retrieval_refs=['turn969976420view0']),
 dict(id='PMS_REGULAR_PARAMETERS',primary_url='https://stacks.math.columbia.edu/tag/00NQ',
  additional_primary_urls=['https://stacks.math.columbia.edu/tag/00NP'],
  theorem_locators=['Lemmas 10.106.2 and 10.106.3'],
  precise_import='A regular local ring is a domain; quotienting by an initial segment of a regular system of parameters gives a regular local ring of the expected dimension.',
  hypotheses_checked=['La is exactly the regular coefficient completion required by S5.','Its parameters are chosen as a minimal generating list of its maximal ideal.'],
  uses=['PMS14'],primary_retrieval_refs=['turn355077836view1','turn355077836view2']),
 dict(id='PMS_HEIGHT',primary_url='https://stacks.math.columbia.edu/tag/0BBZ',
  theorem_locators=['Lemma 10.60.12(1)'],
  precise_import='A prime minimal over an ideal generated by r elements has height at most r.',
  hypotheses_checked=['A0=La[[Y]] is Noetherian and its maximal ideal is generated by d+|sigma| displayed elements.','For the normalized point, ker(g) itself is the prime generated by varpi,z_1,...,z_D in the Noetherian coefficient power-series ring.','Explicit prime chains prove the matching lower bounds.'],
  uses=['PMS14','PMS16'],primary_retrieval_refs=['turn575486168view3']),
 dict(id='PMS_MINIMAL_ASSOCIATED',primary_url='https://stacks.math.columbia.edu/tag/02CE',
  theorem_locators=['Proposition 10.63.6'],
  precise_import='Minimal primes in the support of a finite module over a Noetherian ring are associated.',
  hypotheses_checked=['C0=C/Ann_C N is finite over the Noetherian A0, hence Noetherian.','The module to which the proposition is applied is C0 itself, finite over C0.','Its A0-torsion freeness is proved by the actual faithful action on the free module N.'],
  uses=['PMS14'],primary_retrieval_refs=['turn503015159view0']),
 dict(id='PMS_INTEGRAL_DIMENSION',primary_url='https://stacks.math.columbia.edu/tag/00OK',
  theorem_locators=['Lemma 10.112.4'],
  precise_import='An injective integral extension of rings has the same Krull dimension.',
  hypotheses_checked=['A0 -> C0/Z0 is injective because each minimal prime contracts to zero.','It is finite by the endomorphism-module argument and thus integral.'],
  uses=['PMS14'],primary_retrieval_refs=['turn503015159view1']),
 dict(id='PMS_COMPLETION_DIMENSION',primary_url='https://stacks.math.columbia.edu/tag/07NV',
  additional_primary_urls=['https://stacks.math.columbia.edu/tag/07NY'],
  theorem_locators=['Lemmas 15.44.1 and 15.44.4'],
  precise_import='Maximal-ideal completion preserves dimension and regularity of a Noetherian local ring.',
  hypotheses_checked=['The actual localized coefficient ring at ker(g) is proved regular of dimension D+1 by the explicit coordinate change and prime chain.','Its completion is exactly the La specified in the source laDim contract.'],
  uses=['PMS16'],primary_retrieval_refs=['turn149047391view1','turn149047391view2']),
]
for app in APPS:
    app.update(classification='A',status='checked direct primary-source application',
      checked_on='2026-11-22',excluded_scope='No automorphic, ordinary/control, patching-module or S5 existence theorem is imported.')
dump('published_applications.json',APPS)

inherited=[]
for path,ids,role in [
 ('joint_support/main.tex',['JSP9','JSP12'],'JSP9 integral all-coefficient word identity is a mathematical input; JSP12 binds the unchanged original same-ideal and both-Links consumer.'),
 ('limit_system/main.tex',['LIM18'],'Actual full original S4 producer with every Lim field; no new limit system is assumed beyond its original T.ProL antecedent.'),
 ('count_raw/main.tex',['CRW18','CRW19','CRW20'],'Exact downstream selected full-block dimension/support consumer; retained contextual linkage, not used circularly to construct S5.'),
]:
    raw=(HUMAN/path).read_bytes()
    inherited.append(dict(path='reconstruction_v039/'+path,sha256=sha(raw),claim_ids=ids,
      claim_proof_blocks=[proof_block(raw,cid) for cid in ids],role=role))
peer=[]
for path,ids,role in [
 ('patched_ring/main.tex',['PRG2','PRG13','PRG14','PRG18','PRG24'],
  'Actual RRObj and full RMaps with same all-series identities; local/continuous maps; exact SpoCo finite-free local splitting algebra and root generators. No PMS support theorem is used in these PRG inputs.'),
]:
    raw=(PEER/path).read_bytes()
    peer.append(dict(path=path,sha256=sha(raw),claim_ids=ids,
      claim_proof_blocks=[proof_block(raw,cid) for cid in ids],role=role))
known={f'PMS{i}' for i in range(1,33)}|{c for x in inherited+peer for c in x['claim_ids']}
assert all(d in known for ds in DEP.values() for d in ds)
tex=(HERE/'main.tex').read_bytes(); claims=[]
for i in range(1,33):
    cid=f'PMS{i}'; pb=proof_block(tex,cid)
    block=b''.join(tex.splitlines(keepends=True)[pb['line_start']-1:pb['line_end']]).decode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block).group(1)
    assert f'\\label{{claim:{cid}}}' in block
    claims.append(dict(id=cid,title=title,introduced_in='0.40',classification='B',
      status='complete human proof at the printed exact scope',
      depends_on=DEP[i],classical_inputs=[a['id'] for a in APPS if cid in a['uses']],
      original_hypotheses=HYP[i],hypotheses_retained=HYP[i],
      proof_location=dict(file='patched_support/main.tex',label='claim:'+cid,
        **{k:v for k,v in pb.items() if k!='id'}),
      source_groups=CG[i],sources=[x for x in sources if x['group'] in CG[i]],
      dependency_scope=('Complete universal original S5; no actual arithmetic TWAut is needed to prove this implication.' if i==15 else
        'Actual PMod and support output on the literal original TWAut/Lim/RRObj/RMaps; unchanged ordinary/automorphic existence remains outside this endpoint.' if i==29 else
        'Same J and original point/ideal/action; supplies exact support interface, not a replacement Hecke ideal or arbitrary-Kap theorem.' if i==32 else
        'Only the printed original hypotheses and listed exact proved inputs; no source theorem invocation substitutes for the human argument.')))

closed=[
 dict(id='ORIGINAL_PMOD_FROM_LEVELS',classification='B',by=[f'PMS{i}' for i in range(1,9)],
  scope='Full PMod from the exact three finite-level hypotheses, even with X only finite over L0: actual BB/MM, every quotient, quasi-regular sequence, BB-linear fiber and radical annihilator.',
  conditional_inputs='The unchanged original complete coefficient, ring, module, single ultrafilter and all three finite-level inputs.'),
 dict(id='ORIGINAL_S5',classification='B',by=[f'PMS{i}' for i in range(1,16)],
  scope='Entire universal original S5, including arbitrary center index set and the full move field with equality of contractions.',
  conditional_inputs='Exactly the antecedents in PatchedSupportCompletions.lean:50-70; coefficient dimension d and finite-free original X.'),
 dict(id='ORIGINAL_LADIM_NORMALIZED',classification='B',by=['PMS16'],
  scope='Actual original normalized Unit coefficient completion is regular of dimension 1+D.',
  conditional_inputs='Original coefficient DVR and finite point field; O->K surjective; original Unit section maps to t.'),
 dict(id='ORIGINAL_RREXT_DSEES',classification='B',by=['PMS20','JSP9','PRG2','PRG14'],
  scope='Full-law finite quotient comparison and exact unique-map comparison of all five tuple fields; integral at ell=3.',
  conditional_inputs='Original continuous determinant law and actual full RRObj universal property.'),
 dict(id='ORIGINAL_ARITHMETIC_PMOD_SUPPORT',classification='B',by=[f'PMS{i}' for i in range(17,30)]+['PMS15','PMS16'],
  scope='All-level freeN, uniform piCong, paired maps, every six-family Rel approximation with one A.ex+1; constructed actual PMod and full S5 output.',
  conditional_inputs='Original same TWAut, Lim, RRObj/RMaps, ProL, Adapted, n>=1. Point centers retain all original prime, ii, y, f and coefficient-completion guards.'),
 dict(id='ORIGINAL_PIKER',classification='B',by=['PMS30'],
  scope='Full ii(W)<=ker(pi); determinant q1 trace identity proved integrally in a finite truncated coefficient ring.',
  conditional_inputs='Actual RMaps and adapted data; n>=1. No ProL or n! invertibility needed for this conclusion.'),
 dict(id='ORIGINAL_PISURJ',classification='B',by=['PMS31','PRG2','PRG18'],
  scope='Actual pi:R->Spo(A) is onto, before any localization or reduction.',
  conditional_inputs='Literal GenBy O(pairVals u union original Unit), actual RRObj/RMaps/SpoCo.'),
 dict(id='ORIGINAL_ANN_X0_IFF_J',classification='B',by=['PMS32','PMS31'],
  scope='For every prime P of actual Spo, Ann_R(X0)<=pi^{-1}P iff J<=P intersect B, on the same original module and ideal.',
  conditional_inputs='Actual piSurj and original TWBase.supp.'),
]
remaining=[
 dict(id='PMS_ACTUAL_ORDINARY_TWAUT_INPUT',classification='C',status='retained original producer',
  remaining_contract='Supply original ordinary/control/type-neatU/TThetaEx and same-J HasAut/TWAut data; PMS constructs support from those supplied original modules and does not construct the automorphic module itself.'),
 dict(id='PMS_SELECTED_CORE_ASSEMBLY',classification='B',status='separate companion producer; not claimed by PMS alone',
  remaining_contract='Exact original OoPair/OoPt and prescribed prime/root lift, followed by CRW18-20 with the support output. The companion selected_core packet owns this join; it is not a new assumed patched-module producer.'),
 dict(id='COUNT_II_SUPPORT',classification='C',status='not claimed closed by this component',
  remaining_contract='Original joint Hida/P1 producer for both rank-four Links, fixed iota and a single common coefficient threshold, with each actual same ideal J. Ordinary/control/type/neatU/four Hida and same-J HasAut remain; original CohP and LocCFT retain their full scopes.'),
]
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.40',component='patched_support',
 source_commit=PIN,proof_sha256=sha(tex),proof_file_sha256=sha(tex),
 proof_claims=[c['id'] for c in claims],closed=closed,remaining=remaining,
 classical_input_nodes=[dict(id=a['id'],classification='A',certificate='published_applications.json') for a in APPS],
 sufficient_rules=[
  dict(conclusion='ORIGINAL_S5',logic='PROVED_UNIVERSAL',requires=['CERT_PMS1_PMS15'],
   binding='Every original complete coefficient ring, finite variable set, one U>=tails, all finite-level modules and exact three antecedents; full arbitrary-center move.'),
  dict(conclusion='SAME_ACTUAL_PMOD',logic='AND',requires=['SAME_ORIGINAL_TWAUT','SAME_ORIGINAL_LIM','SAME_ORIGINAL_RROBJ_RMAPS','SAME_PROL_ADAPTED','CERT_PMS18_PMS29'],
   binding='Actual module MN through rho_N, X0 through pi, same J and the same Lim ultrafilter.'),
  dict(conclusion='NORMALIZED_POINT_SUPPORT_1_PLUS_D0',logic='AND',requires=['SAME_ACTUAL_PMOD','SAME_ORIGINAL_NORMALIZED_POINT_CENTERS','CERT_PMS15_PMS16'],
   binding='O->K onto; original Unit->t; prime/y/ii/f guards; sigma=q times n; dimension 1+D+nq.'),
  dict(conclusion='SAME_IDEAL_ANNIHILATOR_DICTIONARY',logic='AND',requires=['SAME_ORIGINAL_GENBY','SAME_ORIGINAL_TWBASE_SUPPORT','CERT_PMS30_PMS32'],
   binding='Actual pi and actual Spo tensor baseM; ideal J is unchanged.'),
 ],
 nonlogical_shared_links=[
  dict(source='PRG_RROBJ_RMAPS_SPOCO',target='PMS17-PMS32',reason='Peer supplies the full ring/tuple/maps and splitting algebra, not a patched module; no circular dependence.'),
  dict(source='PMS29-PMS32',target='SELECTED_CORE_CRW18_CRW20',reason='Supplies every exact patched-support input at dimension 1+D0; separate point/descent assembly is owned by selected_core.'),
  dict(source='PMS15',target='UNRESTRICTED_CHAIN_SUPPORT',reason='Full move proved at the universal S5 scope; this shared use alone does not prove unrestricted Core.'),
 ],
 not_claimed_closed=['ordinary/control automorphic system','type/neatU/TThetaEx','four original Hida endpoints','same-J HasAut/TWAut producer','full original CohP','LocCFT','COUNT_II_SUPPORT','unrestricted Core','arbitrary Kap B1/B2','Sel1 vanishing'],
 quantifier_guards=[
  'One actual Lim ultrafilter precedes every module, level map and support center.',
  'Every k,j has its own allowed event for finite freeness; ranks may vary without a global bound.',
  'Every j has one event before every R-scalar for the paired maps; piCong is uniform on every ring element.',
  'One exponent A.ex+1 precedes every Rel generator, precision and level event.',
  'All original characters, ordered products, ph/ta elements, roots, y variables and full determinant laws are retained.',
  'S5 move is proved for arbitrary i,i-prime,Z,Q and equality of contraction to the actual R/ii.',
  'The dimension1+D0 calculation retains O->K surjectivity and the original normalized Unit section.',
  'The original same ideal J is recovered by the literal TWBase.supp equivalence.',
  'Selected n=a=4,g=0,h=0 applies for every permitted odd ell, including ell=3 whenever the original input hypotheses hold, without n! inversion; no arbitrary-Kap or Sel1=0 inference.',
  'Both rank-four Links and fixed-iota then one-common-threshold order remain outside, unchanged.',
 ],formal_correctness_assumed=True,new_lean_build=False,
 peer_review='pending independent final-byte mathematical/source review')
dump('closure.json',closure)
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.40',date='2026-11-22',
 source_commit=PIN,component='patched_support',main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),
 claims=claims,source_groups=groups,source_inventory=sources,
 source_files=[dict(path=p,sha256=sha(r),full_file_sha256=sha(r),bytes=len(r)) for p,r in sorted(cache.items())],
 inherited_proof_inputs=inherited,peer_proof_inputs=peer,
 published_applications=dict(file='published_applications.json',sha256=sha((HERE/'published_applications.json').read_bytes()),ids=[a['id'] for a in APPS]),
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes()),portable=True,
  arguments=['--source','--human-root','--peer-root'],read_only_inputs=['pinned Lean source','reconstruction_v039','work_v040/patched_ring']),
 validation=dict(pinned_blob_verified_files=len(cache),source_ranges=len(sources),
  distinct_source_ranges=len({(x['path'],x['line_start'],x['line_end']) for x in sources}),
  claim_source_ranges=sum(len(c['sources']) for c in claims),all_source_ranges_exact=True,
  claim_proof_blocks=len(claims),inherited_claim_proof_blocks=sum(len(x['claim_proof_blocks']) for x in inherited),
  peer_claim_proof_blocks=sum(len(x['claim_proof_blocks']) for x in peer),new_lean_build=False),
 scope_note='Full original S5 and actual arithmetic PMod/support prerequisites; actual actions, one ultrafilter, normalized dimension and same-J comparison retained. Standard primary commutative algebra imports have explicit certificates; no imported patching-module or S5 producer.')
dump('provenance.json',prov)
loc=[f'PMS1-PMS32 exact pinned source locators; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for x in sources:
    loc += [f"{x['id']} | {x['declaration']}",f"{x['path']}:{x['line_start']}-{x['line_end']}",
            'file_sha256='+x['sha256'],'range_sha256='+x['range_sha256'],x['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f'''PMS1-PMS32: actual patched module and complete S5, v0.40

Formal correctness is accepted. No Lean build or replay was performed.
Source commit {PIN}
main.tex SHA256 {sha(tex)}
provenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}
closure.json SHA256 {sha((HERE/'closure.json').read_bytes())}

COMPLETED

PMS1-PMS8 construct the actual BB and finite MM from the original finite
quotients, using one given ultrafilter, a diagonal ideal criterion and an
explicit complete inverse-limit module. All quotient kernels, all-degree
quasiregularity, the full BB-linear fiber and radical annihilator are proved.
Ranks need not be uniformly bounded, and no compatible finite-level maps
are assumed.

PMS9-PMS15 prove the ENTIRE original S5, including the full movement field
for arbitrary centers and prime pairs, with equality of contraction to R/ii.
PMS12 proves that the actual completed fiber is free over the actual La by
a finite faithful-action algebra and its completion factors. PMS13 checks
m-adic closedness of every y^k submodule, then separated y-completeness,
before constructing a basis over La[[Y]]. PMS14 embeds the faithful support
algebra in the endomorphism ring of this free module and proves every
minimal support component has dimension d+|sigma|. Zero modules are included.

PMS16 independently computes the actual normalized coefficient completion:
the original Unit variable maps to t, O->K is onto, a coordinate change
identifies the coefficient prime as (varpi,z_1,...,z_D), and the dimension is
exactly 1+D.

PMS18-PMS29 prove every arithmetic prerequisite on the same original TWAut,
Lim and RRObj/RMaps. This includes all k,j free quotients; full uniform
specialization equality before every ring element; exact R-linearity of
the paired quotient maps; the stronger ell^j scalar congruence; all six
original relation families; and the single exponent A.ex+1 before every
generator, precision and level. No modules or ideals are replaced.

PMS30 proves an integral determinant trace identity directly in
A[t,s]/(t^(n+1),s^2), then proves every piKer constructor. PMS31 proves
actual pi surjectivity from the literal GenBy hypothesis and original
splitting roots. PMS32 proves the exact Ann_R(X0) iff J support dictionary
for every prime of the original splitting algebra. These are the support
inputs of the selected CRW18-20 consumer at dimension 1+D0.

RETAINED SCOPE

PRG supplies full RRObj/RMaps/SpoCo; its exact peer proof blocks are bound.
The original TWAut and automorphic module are inputs, not newly produced.
The separate selected_core packet owns full OoPair/OoPt, prescribed
prime/root lifting and final selected Core/Raw assembly. PMS alone does not
claim that assembly or COUNT_II_SUPPORT closed.
Ordinary/control/type/neatU/TThetaEx, four Hida endpoints, same-J HasAut and
the original CohP/LocCFT scopes remain. Both original rank-four Links,
ell=3, fixed iota and the one common coefficient threshold are unchanged.
The chosen h=0,a=n=4,g=0 rule is preserved; no arbitrary-Kap B1/B2 or Sel1=0
conclusion is asserted. Full S5 has its full universal scope and move field.

EVIDENCE

{len(claims)} proof blocks; {len(cache)} pinned source files; {len(sources)}
source ranges; {sum(len(c['sources']) for c in claims)} claim-source references;
{sum(len(x['claim_proof_blocks']) for x in inherited)} inherited blocks and
{sum(len(x['claim_proof_blocks']) for x in peer)} peer proof blocks.
All listed source bytes equal their pinned git blobs. The builder is
portable with --source, --human-root and --peer-root and writes only beside
itself. Standard published imports are explicit A certificates, while the
new module and support proofs are B, completed at their printed scopes.
Standalone two-pass draft TeX and independent review are recorded separately.
'''
(HERE/'report.txt').write_text(report)
print(json.dumps(dict(claims=len(claims),source_files=len(cache),source_ranges=len(sources),
 claim_source_ranges=sum(len(c['sources']) for c in claims),main_sha256=sha(tex),
 provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
 closure_sha256=sha((HERE/'closure.json').read_bytes())),indent=2))
