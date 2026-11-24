#!/usr/bin/env python3
"""Portable CRW source/proof metadata builder; all input files are read-only.

python build_metadata.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v037
Only files beside this builder are written. No Lean command is run.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, default=HERE.parent.parent/'lean_source')
p.add_argument('--baseline', type=Path, default=HERE.parent.parent/'reconstruction_v037')
args = p.parse_args()
REPO, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==PIN
B='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P=B+'PatchingModules/'
W=B+'WeilGroupCharacters/'
S=P+'SelmerScaling/'
C=P+'ClosureConjugation/'
L=P+'SeparableMatrixStability/'
H=P+'AnnihilatorBaseChange/'
A=B+'AlgebraTools/'
CA=B+'CommutativeAlgebraHeight/'

# Inclusive pinned ranges. End zero means the actual final line.
# Source proofs locate the exact original endpoints; they are not human proof inputs.
SPECS=[
 ('G01',P+'PatchedSupportCompletions.lean',[
  (10,21,'IsCoef, S4 and CohLim with exact quantifier order'),
  (78,100,'URep: every field including N, typeI, full det, thick and one fixed B-lattice'),
  (112,147,'OoPt, original closed ker and exact S6'),
  (149,157,'GalOut: completion, K1/K2/K3, prime dimension and target condition'),
  (165,213,'Pt, Adapted, ChainConcl, Core/CoreBC/Raw and same J'),
  (220,230,'NP.Ext and original Choice quantifiers')]),
 ('G01',P+'ThetaCoefficientMapEq.lean',[
  (14,39,'Original all-level TWGrp'),(45,78,'ProL, Eig, B1/B2 and K1/K2/K3'),
  (86,139,'q1El/q2El, pairGens/qGens including star and all pairVals'),
  (163,236,'TWBase, TWRing, TWMaps and TWAut on one fixed J'),
  (262,299,'Close and every original Lim field')]),
 ('G01',P+'PairedDualFirstOrderDualMatrixSpace.lean',[
  (10,107,'Loc/Glob, local and global data, Hom and distinguished old subgroup'),
  (192,226,'Literal W1 and paired coefficient modules'),
  (232,294,'dY, LocAt, SelZ/Bd, all NP fields and original N3/N4'),
  (306,348,'Kap, first-order representation and exact Sel1/Bd1/SelP/SelM'),
  (352,368,'DiscSt, every-field NonSS, GenBy and completion dictionary')]),
 ('G01',W+'UniversalOrdinaryDeterminantRing.lean',[
  (10,42,'Original profinite frame and involution data'),
  (66,104,'G0, Gprime, eps, star, ordered oEl and form'),
  (128,155,'IsPsi.mu, full Pair including trace relations, and Maps')]),
 ('G02',B+'CommutativeAlgebra/ResMapBijective.lean',[
  (9,29,'IsCO means complete local Noetherian, local coefficient map, residue-surjectivity')]),
 ('G02',S+'RfEx.lean',[(6,0,'rfEx: original residue map on the actual completion')]),
 ('G02',S+'OoExKer.lean',[
  (11,55,'Coefficient kernel and coefficientwise power-series kernel'),
  (57,104,'Actual evaluation at the ordinary parameter'),
  (106,0,'ooEx: actual coefficient DVR and all four compatibility fields')]),
 ('G02',S+'SelmerSpannedByKappaLaurent.lean',[
  (54,98,'Ctx: original completion/rF/URep/OO and all compatibility fields'),
  (119,132,'Exact J2 and Tp derivation space')]),
 ('G02',A+'CaCplLift.lean',[(1,0,'Unique completion lift to a complete local target')]),
 ('G03',W+'RepAlg.lean',[
  (44,117,'Full natural homogeneous multiplicative GDet law, map/ofRep, and multivariable CH coefficients')]),
 ('G03',CA+'DToDet.lean',[(6,0,'Exact group-algebra/tensor polynomial-law coefficient dictionary')]),
 ('G03',CA+'DToDetCH.lean',[(6,0,'Exact equality of source CH coefficient ideal and determinant CH ideal')]),
 ('G03',P+'AutomorphicDetection/S6.lean',[(15,0,'Original S6 producer and full-block GrI path')]),
 ('G03',C+'GrI.lean',[(8,0,'Source full-block AA=B and N=0 construction')]),
 ('G03',C+'GrDet.lean',[(7,0,'Full polynomial-law determinant endpoint')]),
 ('G04',C+'StarBasic.lean',[(1,0,'Original star involution, anti-multiplication and scalar conventions')]),
 ('G04',C+'Trinv.lean',[(15,0,'Source star/trace/involution endpoint on the original relations')]),
 ('G05',C+'UrepOf.lean',[(8,0,'All actual URep fields, original finite B-lattice and continuity')]),
 ('G05',C+'HatEx.lean',[(43,0,'Original finite Cayley-Hamilton algebra producer; replaced at full-block scope')]),
 ('G06',W+'RepAlg.lean',[(119,125,'Actual coefficient-adic and every-open-normal closureIdeal')]),
 ('G06',CA+'OfDetToDet.lean',[(221,222,'Exact GDet.chBar definition')]),
 ('G06',S+'ClosureIdeal.lean',[(1,0,'Closure ideal consumer for actual matrix relations')]),
 ('G06',S+'PrVr.lean',[(1,0,'Original representation relation dictionary')]),
 ('G07',S+'TpDual.lean',[(28,146,'Relative cotangent duality and literal tpDual endpoint')]),
 ('G07',S+'SelmerSpannedByKappaLaurent.lean',[(119,132,'Original J2/Tp'),(166,174,'Original Ctx.Pres output')]),
 ('G08',S+'TrBndDen.lean',[(5,0,'Original bounded-derivative endpoint, supplied directly here in full block')]),
 ('G09',A+'OrdExt.lean',[(5,0,'Multilinear extension of ordered group relations')]),
 ('G09',A+'LagTriangular.lean',[(5,0,'Ordered middle-factor cancellation and Lagrange idempotent flag')]),
 ('G09',S+'LocLemma.lean',[(134,177,'Square-zero simultaneous idempotent conjugation'),(179,0,'Separating group-algebra element and original local flag endpoint')]),
 ('G10',S+'DefUSel.lean',[(103,186,'Actual local dual-number flag calculation'),(189,0,'Full cocycle, polarization, inertia and local Selmer fields')]),
 ('G10',S+'AlSel.lean',[(7,0,'alSel and original Laurent boundedness endpoint')]),
 ('G11',S+'ConjConst.lean',[
  (94,150,'Ordered-character rigidity and both auxiliary root/y equations'),
  (152,231,'Conjugation forces all actual generators constant'),
  (233,0,'alInj: injection modulo exact polarized coboundaries')]),
 ('G11',S+'TrConst.lean',[(1,0,'Source density/completion constancy consumer')]),
 ('G12',L+'SecondSelmerSpanBoundAtAllLevels.lean',[
  (19,43,'Exact Hom surjectivity, conjugation and local-map compatibility'),
  (158,160,'FirstSelmerCardBoundAtAllLevels')]),
 ('G12',L+'LcOfAdic.lean',[(122,0,'t1: eventual same-action and both Selmer transports on actual Lim')]),
 ('G12',L+'EventuallyFactorThroughTowerIffLimit.lean',[(1,0,'Same kernel/coset factorization at the limit')]),
 ('G13',L+'TaylorWilesFirstConditionAtLimitOfGroupCondition.lean',[(1,0,'B1 to all-truncation limit count with the original fixed constant')]),
 ('G14',L+'CoefficientsBoundedOfSelmerBoundary.lean',[(1,0,'Uniform finite-equation approximate-boundary coefficient bound')]),
 ('G15',L+'FirstCohomologyBoundOfBoundaryBound.lean',[(6,0,'Finite quotient count and the exact K1 bound')]),
 ('G15',S+'SelmerRankBoundLaurent.lean',[(47,0,'k1F: exact Laurent independence scope')]),
 ('G15',P+'AutomorphicDetection/CohLim.lean',[(12,0,'Original CohLim consumer and three K endpoints')]),
 ('G16',S+'AlCSmul.lean',[(12,147,'pres: all original X/m/c fields and generation endpoint')]),
 ('G17',S+'PresOut0.lean',[(9,68,'presOut0: evaluation surjection and exact dimension implication')]),
 ('G17',B+'CommutativeAlgebra/CoSurj.lean',[(1,0,'Source cotangent-generation-to-surjectivity endpoint')]),
 ('G18',P+'AutomorphicDetection/GalOut.lean',[(16,37,'ctx_out: typeI makes N and ired zero; exact presOut0 branch'),(39,48,'galOut: actual same-context OO and URep assembly')]),
 ('G19',P+'PatchedSupportCompletions.lean',[(27,70,'Exact patched support completion/fiber/dimension and all S5 hypotheses')]),
 ('G19',H+'ChainAbs.lean',[(7,70,'chainAbs, exact h=0 initial and terminal uses')]),
 ('G19',A+'CaCplSpec.lean',[(1,0,'Prime-over property for the original completion')]),
 ('G20',H+'SpecializationMapCompUniversalSection.lean',[
  (13,35,'PMod: original finite module, quasi-regularity, fiber and relation nilpotence'),
  (54,153,'RRObj, RMaps, actual six relation families, MN, X0 and OoPair')]),
 ('G20',P+'AutomorphicDetection/LiftPt.lean',[
  (49,72,'lift_pt: same x, actual splitting prime and point kernel'),
  (76,139,'core: same Lim/RR/RMaps/OoPt, patched module hypotheses and exact dimension'),
  (140,175,'core: same completion GalOut, support contraction and original J')]),
 ('G20',H+'OoMaps.lean',[(30,0,'ooMaps: literal full determinant and ordered-character compatibility')]),
 ('G20',H+'OoPair.lean',[(65,0,'Actual OoPair on the original quotient ring')]),
 ('G20',H+'PatchedModuleAnnihilatorLeComapIffIdealLe.lean',[(6,0,'Exact annihilator versus original same-J equivalence')]),
 ('G20',P+'AutomorphicDetection/AnnBc.lean',[(24,85,'Actual S5 support producer from PMod, and remaining patching input')]),
 ('G20',H+'RmapsEx.lean',[(1,0,'Actual common RMaps producer retained')]),
 ('G20',H+'PmodEx.lean',[(1,0,'Actual patched module producer retained')]),
 ('G21',P+'AutomorphicDetection/CoreBC.lean',[(24,127,'Original coefficient extension, Unit parameter, same ideal and point transport')]),
 ('G21',L+'RawMain.lean',[(12,48,'Original pro-ell quotient and same data descent to CoreBC')]),
 ('G21',P+'ChebotarevFamilies/PFromAutOf.lean',[(30,131,'Exact h=0 NiceI same-J consumer and chain_of/pFromAut_of')]),
 ('G21',P+'AutomorphicDetection/Imports.lean',[(1,0,'S4 producer alias; actual limit existence remains explicit')]),
 ('G21',L+'SelmerCocyclesLimitAndDescentProperties.lean',[(1,0,'Actual original limit producer to reconstruct next')]),
]
cache={}
sources=[]
groups={}
for group,path,ranges in SPECS:
    raw=cache.get(path)
    if raw is None:
        raw=(REPO/path).read_bytes()
        blob=subprocess.check_output(['git','show',f'{PIN}:{path}'],cwd=REPO)
        assert raw==blob,path
        cache[path]=raw
    lines=raw.splitlines(keepends=True)
    for first,last,decl in ranges:
        last=last or len(lines)
        assert 1<=first<=last<=len(lines),(path,first,last,len(lines))
        block=b''.join(lines[first-1:last])
        item=dict(id=f'CRW_SRC_{len(sources)+1:03}',group=group,path=path,
          declaration=decl,line_start=first,line_end=last,
          sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(block),
          range_bytes=len(block),source_commit=PIN,
          url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{first}-L{last}')
        sources.append(item)
        groups.setdefault(group,[]).append(item['id'])

cg={
1:['G01','G21'],2:['G01','G02'],3:['G01','G03'],4:['G01','G03','G04'],
5:['G01','G03','G05','G06'],6:['G01','G03','G04','G05','G06'],
7:['G02','G07'],8:['G01','G02','G05','G08'],9:['G01','G09'],
10:['G01','G09','G10'],11:['G01','G06','G11'],
12:['G01','G12'],13:['G01','G12','G13'],14:['G01','G14'],
15:['G01','G13','G14','G15'],16:['G01','G07','G16'],
17:['G02','G17'],18:['G01','G17','G18'],19:['G19'],
20:['G01','G19','G20'],21:['G01','G18','G19','G20','G21'],
}
deps={
1:['CCH1','CCH2','CCH3','CCH13','CCH15','CCH16','CFO1','CFO20','CFO21','CAP13'],
2:['CRW1'],3:['CRW1','CRW2'],4:['CRW3'],5:['CRW3','CRW4'],
6:['CRW3','CRW4','CRW5'],7:['CRW2','CRW6'],8:['CRW2','CRW5','CRW7'],
9:[],10:['CRW4','CRW6','CRW8','CRW9'],11:['CRW3','CRW6','CRW8','CRW10'],
12:['CRW1'],13:['CRW1','CRW12'],14:['CRW1'],
15:['CRW13','CRW14','CCH1','CCH2'],16:['CRW7','CRW10','CRW11','CRW15'],
17:['CRW16'],18:['CRW2','CRW6','CRW16','CRW17'],19:['CRW18'],
20:['CRW12','CRW13','CRW15','CRW18','CRW19'],
21:['CRW1','CRW6','CRW15','CRW18','CRW19','CRW20','CFO21','JSP10','JSP11','QX4','QX10','YX2','KA5','KA6'],
}
hyp={
1:['Same CCH15 extended full-block a=n=4 point, g=0 Kap, finite detector/roots; same CAP13 T/TWPl; coupled CFO B1/CCH B2; unchanged complete CohP/LocCFT, old N4 and all source setting data.'],
2:['Original OoPt surjective O->K, f_s=t, original complete DVR O and IsCO O B; actual IsCplAt B ker(f) R.'],
3:['Full natural multiplicative homogeneous determinant law; actual completion from CRW2; NP.span on Gprime, a=n>0 and surjective original h.p0.'],
4:['Original Pair.P and star, original NP.form=1 and exponent 1-n; ell odd, hence 2 a unit; same residual representation.'],
5:['Original B Noetherian local, continuous full determinant on original compact G0; same completed representation.'],
6:['All original Pair.Ord/I, OoPt.q1/q2 and star generators; full CH coefficients and every-N/every-open-normal closure; every field map in NonSS.'],
7:['Actual OO->R local with identical Laurent residue field, OO onto residue; actual N=0.'],
8:['Actual ordinary-point parameter and OO image, finite generators of ker(f), same fixed B-lattice and its uniform continuity.'],
9:['Infinite F, square-zero dual numbers, original fixed flag and ordered pairwise distinct characters, full mixed ordered product for every tuple.'],
10:['Same actual h and local maps, original IsPsi.mu values in O, original Iu=Resid.Ip, NP.N1, exact form and inertia relations.'],
11:['Full determinant polynomial law, all ordered local characters, q1/q2 with distinct roots and same tame elements, original GenBy and s; polarized actual boundary.'],
12:['One supplied original Lim(T), all of its uniform kernel/action/local/conjugation clauses; finite A_m, selected g=0 full first-order module. This does not construct Lim.'],
13:['Same B1 constant C, same Lim ultrafilter above atTop, same original T; no threshold exchange.'],
14:['Full first-order coefficient matrix space, odd ell, exact independence modulo skew integral boundaries over A=K[[t]].'],
15:['Same supplied Lim and original B1, bounded Laurent cocycles, finite original ordinary-place set; chosen g=0 Kap fixed.'],
16:['Same actual OoPt/completion and original K1 for its h/k/D0; actual OO and N=0; selected g=0.'],
17:['Actual cotangent generators from CRW16; complete coefficient DVR with residue onto F; original complete Noetherian local R.'],
18:['Same actual completion, selected K1 and a=n,g=0; prime Z with the original dimension >=1+D0. Existence of such Z is not asserted.'],
19:['One actual support completion with exact fiber equivalence and minimal-prime dimension; matched ordinary point to CRW18; starting prime containing the same annihilator and all parameters.'],
20:['Same actual Lim, RRObj/RMaps/OoPair/OoPt and splitting algebra, actual S5 support output, same prime lifts and annihilator/J equivalence; original TWAut on J. Producers are retained.'],
21:['Original coefficient normalization and pro-ell descent, actual Lim and matched patching remain; original ordinary/Hida/HasAut and full CohP/LocCFT remain; both rank-four Links, fixed iota and one outer threshold.'],
}
classical={2:['CRW_NOETHERIAN','CRW_COMPLETION','CRW_DVR_COMPLETION'],
3:['CRW_CAYLEY_HAMILTON','CRW_HENSELIAN'],5:['CRW_ARTIN_REES','CRW_KRULL'],
6:['CRW_CAYLEY_HAMILTON'],11:['CRW_COMPLETION'],
18:['CRW_NOETHERIAN','CRW_DIMENSION'],19:['CRW_COMPLETION']}

def proof_block(raw,cid):
    ls=raw.splitlines(keepends=True)
    st=[i for i,line in enumerate(ls) if line.strip()==f'% BEGIN {cid}'.encode()]
    if st:
        assert len(st)==1,cid
        first=st[0]
        en=[i for i,line in enumerate(ls) if line.strip()==f'% END {cid}'.encode()]
        assert len(en)==1,cid
        last=en[0]
    else:
        lab=next(i for i,line in enumerate(ls) if f'\\label{{claim:{cid}}}'.encode() in line)
        first=max(i for i in range(lab+1) if b'\\paragraph{' in ls[i])
        last=next((i-1 for i in range(lab+1,len(ls)) if b'\\paragraph{' in ls[i]),len(ls)-1)
    block=b''.join(ls[first:last+1])
    assert first<last
    return dict(id=cid,line_start=first+1,line_end=last+1,sha256=sha(block),bytes=len(block))

tex=(HERE/'main.tex').read_bytes()
claims=[]
for i in range(1,22):
    cid=f'CRW{i}'
    bl=proof_block(tex,cid)
    txt=b''.join(tex.splitlines(keepends=True)[bl['line_start']-1:bl['line_end']]).decode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',txt).group(1)
    assert f'\\label{{claim:{cid}}}' in txt,cid
    claims.append(dict(id=cid,title=title,introduced_in='0.38',
      classification='A' if i==3 else 'B',
      status='complete exact published application with hypotheses checked' if i==3 else 'complete human proof at the printed original-data scope; retained producer inputs explicit',
      depends_on=deps[i],classical_inputs=classical.get(i,[]),original_hypotheses=hyp[i],
      dependency_scope=('CRW1 provides the exact data dictionary; the local S6 proof does not require arithmetic existence of the selected point.' if i in [2,3,4,5,6] else
                        'The original actual Lim remains a supplied object; the proof constructs the count/rank implication, not S4.' if i in [12,13,15] else
                        'Original common patching/descent producers remain explicit. No closed Raw or Count-II producer is inferred.' if i in [19,20,21] else
                        'Only K1-to-Laurent implication of CRW15 is needed for standalone GalOut when K1 is given; actual Lim is used only to produce that K1 from B1.' if i in [16,18] else
                        'Only the stated same-object subclaims and original hypotheses are used.'),
      remaining_inputs=(['actual original Lim','matched patched ring/maps/module and support dimension/fiber','original coefficient normalization and pro-ell descent','ordinary/control/type/TThetaEx','four Hida endpoints','same-J HasAut','unchanged CohP and LocCFT'] if i==21 else []),
      proof_location=dict(file='count_raw/main.tex',label='claim:'+cid,**{k:v for k,v in bl.items() if k!='id'}),
      source_groups=cg[i],sources=[s for s in sources if s['group'] in cg[i]]))

inherited=[]
for path,ids,role in [
 ('count_choice/main.tex',['CCH1','CCH2','CCH3','CCH13','CCH15','CCH16'],
  'Exact full-block spaces, selected g=0 Kap, one finite extension/list and coupled B2; original determinant, old N4 and point kernel preserved.'),
 ('count_first_order/main.tex',['CFO1','CFO20','CFO21'],
  'Actual selected B1 with C before m before eventual N, exact exponent 4d+4q and retained same-J arithmetic boundary.'),
 ('count_auxiliary_primes/main.tex',['CAP13'],
  'Actual T/TWPl realizes the same finite list under original CohP.'),
 ('joint_support/main.tex',['JSP10','JSP11'],
  'Stable discriminant at full-block point and all smaller primes; exact same-J h=0 NiceI consumer.'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],
  'Both original rank-four Links and common same-ideal support requirement.'),
 ('case_two_installation/main.tex',['YX2'], 'Exact Count-II consumer and fixed-iota/common-threshold order.'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],
  'Only Case III is vacuous for two-primary targets; RH still needs I/II/V.')]:
    raw=(BASE/path).read_bytes()
    inherited.append(dict(path='reconstruction_v037/'+path,sha256=sha(raw),claim_ids=ids,
      claim_proof_blocks=[proof_block(raw,cid) for cid in ids],role=role))
known={c['id'] for c in claims}|{cid for d in inherited for cid in d['claim_ids']}
assert all(x in known for ds in deps.values() for x in ds)

applications=[
 dict(id='CRW_CAYLEY_HAMILTON',classification='A',status='exact primary application; hypotheses checked',
  author='Gaetan Chenevier',work='The p-adic analytic space of pseudocharacters of a profinite group and pseudorepresentations over arbitrary rings',
  primary_url='https://maths.dur.ac.uk/events/Meetings/LMS/2011/GRAF11/papers/chenevier.pdf',
  author_url='https://gaetan.chenevier.perso.math.cnrs.fr/articles/determinants.pdf',
  theorem_locators=['Lemma 1.21, printed page 18','Section 1.22, printed pages 18-19, Cayley-Hamilton quotient and arbitrary base change','Theorem 2.22(i), printed page 34'],
  precise_import='A Cayley-Hamilton determinant over a henselian local ring with split absolutely irreducible residual determinant is the full matrix determinant. The coefficient-defined CH quotient commutes with base change.',
  hypotheses_checked=['R is the original completed local B_p, hence henselian.','NP.span with a=n and the original surjection h.p0 spans all Mat_n(F).','The residual determinant is literally det(rho_x composed h.p0) by OoPt.maps.','n>=1 by NP.a_pos; the quotient is the universal multivariable CH quotient.','The original GDet is a natural homogeneous multiplicative polynomial law on all commutative scalar algebras; CH coefficients match its universal CH ideal.','There is no n! assumption, so n=4 and ell=3 are included.'],
  human_proof_use='CRW3; CRW4-CRW6 independently add exact polarization, finite original-B continuity, closure killing and every-field quotient/NonSS.',
  excluded_scope='No ordinary/control, automorphic, S4 or patched-module existence theorem is imported.',
  checked_on='2026-11-22',primary_retrieval_refs=['turn777441126view0','turn346080651view0','turn346080651view1','turn346080651view2','turn533958242view4'],
  primary_pdf_page_34_visually_checked=True),
 dict(id='CRW_NOETHERIAN',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/00FM',theorem_locators=['Lemmas 10.31.1 and 10.31.2'],
  precise_import='Localizations and finite-variable formal power-series rings over a Noetherian ring are Noetherian.',
  hypotheses_checked=['O and OO are DVRs and hence Noetherian.','Only one or D0 finitely many formal variables are used.','B is Noetherian by the original IsCO record.'],
  uses=['CRW2','CRW18'],primary_retrieval_refs=['turn711564595view0'],checked_on='2026-11-22'),
 dict(id='CRW_HENSELIAN',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/04GM',theorem_locators=['Lemma 10.153.9'],
  precise_import='A complete separated local ring is henselian.',
  hypotheses_checked=['R is the maximal-ideal completion of the actual Noetherian local B_p and is complete and separated.'],
  uses=['CRW3'],primary_retrieval_refs=['turn275646732search2'],checked_on='2026-11-22'),
 dict(id='CRW_ARTIN_REES',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/00IN',theorem_locators=['Lemma 10.51.2'],
  precise_import='For finite modules M contained in P0 over Noetherian B, some fixed c gives M intersect m^(j+c)P0 contained in m^j M.',
  hypotheses_checked=['B is the original Noetherian local ring.','P0 is generated by n^2 trace-dual matrices over B.','M is its submodule spanned by group matrices, hence is finite.','The ideal is exactly m_B, not the completion ideal p.'],
  uses=['CRW5'],primary_retrieval_refs=['turn711564595view1'],checked_on='2026-11-22'),
 dict(id='CRW_KRULL',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/00IP',theorem_locators=['Lemma 10.51.4'],
  precise_import='The intersection of m_B^j M is zero for finite M over Noetherian local B.',
  hypotheses_checked=['M is the one finite B-algebra constructed in CRW5.','m_B is proper and B is local Noetherian.'],
  uses=['CRW5','CRW6'],primary_retrieval_refs=['turn480976194view2'],checked_on='2026-11-22'),
 dict(id='CRW_COMPLETION',classification='A',status='checked direct applications',
  primary_url='https://stacks.math.columbia.edu/tag/00MC',
  additional_primary_urls=['https://stacks.math.columbia.edu/tag/031C','https://stacks.math.columbia.edu/tag/07NU'],
  theorem_locators=['Lemma 10.97.3','Lemma 10.97.4','Section 15.44 introductory completion facts'],
  precise_import='Noetherian local completion is complete Noetherian local, faithfully flat, and has unchanged quotients by maximal-ideal powers.',
  hypotheses_checked=['The local rings are B_p and O[[S]]_(varpi), or the retained actual Noetherian patched quotient localized at its specified prime.','Every completion is at that local maximal ideal; it lies in the Jacobson radical.','CRW11 uses only the quotient modulo the square of that maximal ideal.'],
  uses=['CRW2','CRW11','CRW19'],primary_retrieval_refs=['turn533958242view1','turn533958242view2','turn533958242view3'],checked_on='2026-11-22'),
 dict(id='CRW_DVR_COMPLETION',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/0AP1',theorem_locators=['Lemma 15.44.5'],
  precise_import='The maximal-ideal completion of a Noetherian local DVR is a DVR.',
  hypotheses_checked=['CRW2 proves O[[S]]_(varpi) is a DVR by coefficient valuation.','Noetherianity follows from CRW_NOETHERIAN.'],
  uses=['CRW2'],primary_retrieval_refs=['turn480976194view3'],checked_on='2026-11-22'),
 dict(id='CRW_DIMENSION',classification='A',status='checked direct application',
  primary_url='https://stacks.math.columbia.edu/tag/00KQ',theorem_locators=['Proposition 10.60.9'],
  precise_import='For a Noetherian local ring, dimension is the least number of generators of an ideal of definition; hence it is at most the number of maximal-ideal generators.',
  hypotheses_checked=['OO[[Z_1,...,Z_D0]] is local and Noetherian.','Its maximal ideal is generated by the OO uniformizer and D0 variables.','CRW18 proves the reverse inequality by an explicit chain of prime ideals.'],
  uses=['CRW18'],primary_retrieval_refs=['turn480976194view1'],checked_on='2026-11-22'),
]
dump('published_applications.json',applications)
appids={a['id'] for a in applications}
assert all(x in appids for ds in classical.values() for x in ds)

old=json.loads((BASE/'count_first_order/closure.json').read_text())
remaining=old['remaining']
assert any(x['id']=='JSP_SINGLE_POINT_RAW' for x in remaining)
remaining=[dict(x) for x in remaining]
for item in remaining:
    if item['id']=='JSP_SINGLE_POINT_RAW':
        item['new_progress']='CRW2-CRW18 close actual full-block S6, selected CohLim on supplied Lim, cotangent generation and exact GalOut; CRW19-CRW20 close the one-point support implication.'
        item['remaining_contract']='Supply actual original pro-ell quotient/descent and coefficient normalization/Unit parameter, same Lim(T), and the matched original patched ring/maps/modules and S5 support dimension/fiber/annihilator contracts. All remain on the same selected x/Kap/T/TWPl/TWAut/J; no full h=0 Raw producer is asserted closed.'

closed=[
 dict(id='SELECTED_FULL_BLOCK_S6',classification='A+B',by=[f'CRW{i}' for i in range(2,7)],
  scope='Every original S6/URep field for a=n>0, ell odd including ell=3, on the actual OoPt and completion; AA=R,N=0, full-law det, exact form, original B-lattice/continuity and original closure/NonSS.',
  conditional_inputs='Original OoPt, IsCoef, IsCO and actual IsCplAt; these are source inputs, not newly asserted arithmetic existence.'),
 dict(id='SELECTED_COH_LIM_FROM_SAME_LIMIT',classification='B',by=['CRW12','CRW13','CRW14','CRW15'],
  scope='K1/K2/K3 and exact Laurent K1 for same supplied original Lim(T), same selected g=0 full-block Kap and original B1; fixed C before every m is preserved.',
  conditional_inputs='Actual Lim is retained. The source S4 producer is not closed.'),
 dict(id='SELECTED_ORIGINAL_COMPLETION_PRESENTATION',classification='A+B',by=[f'CRW{i}' for i in range(2,19)],
  scope='Actual OO/rF, injective bounded derivative Selmer map, Ctx.Pres with exactly D0 variables, surjection OO[[X_D0]]->R, and actual full-block GalOut with dimension >=1+D0.',
  conditional_inputs='K1 for the same h/k/D0; supplied from B1 only after the original Lim is supplied. No existence of a support prime satisfying the dimension bound is asserted.'),
 dict(id='ONE_POINT_PATCHED_SUPPORT_IMPLICATION',classification='B',by=['CRW19','CRW20'],
  scope='Exact h=0 ChainAbs and one-point Core implication from the same actual completion/support/point/annihilator and prime-lift data; no move field or connecting thick prime is used.',
  conditional_inputs='Actual matched patching support dimension/fiber, same Lim/RRObj/RMaps/OoPt and ideal J are retained producers.'),
]
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.38',component='count_raw',
 source_commit=PIN,proof_sha256=sha(tex),proof_claims=[c['id'] for c in claims],closed=closed,remaining=remaining,
 classical_input_nodes=[dict(id=a['id'],classification='A',status='checked exact published application',application_file='published_applications.json') for a in applications],
 selected_frontier_status={
  'SELECTED_FULL_BLOCK_S6':'CLOSED actual URep, including full determinant, polarization, finite B-lattice, closure and every-field NonSS.',
  'SELECTED_COH_LIM':'CLOSED implication on a supplied original Lim; no independent S4 existence.',
  'SELECTED_GAL_OUT_AND_PRES_OUT_0':'CLOSED on actual completion with same K1 and selected g=0; exact D0 and dimension 1+D0.',
  'SELECTED_CHAIN_ABS_H0':'CLOSED implication on actual matched one-completion support data.',
  'JSP_SINGLE_POINT_RAW':'OPEN C: original limit, compatible patching/support and coefficient/pro-ell descent remain.',
  'COUNT_II_SUPPORT':'OPEN C: original ordinary/control/type/TThetaEx, four Hida endpoints, same-J all-level HasAut and the narrowed selected Raw producer; unchanged CohP/LocCFT.',
  'RH_case_note':'Only III is removed by KA5/KA6 for two-primary targets; RH still needs I/II/V, unrestricted Dirichlet GRH also needs III.'},
 sufficient_rules=[
  dict(conclusion='SELECTED_ACTUAL_FULL_BLOCK_UREP',logic='AND',requires=['ORIGINAL_OOPT_FULL_BLOCK','ORIGINAL_COMPLETION','CERT_CRW2_CRW6','CRW_CAYLEY_HAMILTON'],binding='Same B,u,P,h and completion; no new coefficient extension, determinant or polarization.'),
  dict(conclusion='SELECTED_COMPLETION_PRIME_COMPARISON',logic='AND',requires=['SAME_ORIGINAL_OOPT_AND_COMPLETION','SAME_ORIGINAL_K1','CERT_CRW2_CRW18'],binding='a=n and selected g=0; exact D0; if dim(R/Z)>=1+D0 then Z=0, without asserting such a Z exists.'),
  dict(conclusion='SELECTED_K1_FROM_B1',logic='AND',requires=['SAME_ORIGINAL_LIM','SAME_CCH_SELECTED_KAP_AND_B1','CERT_CRW12_CRW15'],binding='One original Lim(T), one B1 constant C, all m; all T and point data remain matched.'),
  dict(conclusion='SELECTED_ONE_POINT_CORE',logic='AND',requires=['SAME_ORIGINAL_LIM','SAME_TWAUT_AND_SELECTED_POINT','ORIGINAL_MATCHED_PATCHED_OUTPUT','ORIGINAL_SUPPORT_DIMENSION_FIBER_AND_ANN_J','CERT_CRW2_CRW20'],binding='One same quotient completion and support; dimension (1+D)+nq=1+D0; prime lifts and ann iff J use original maps.'),
  dict(conclusion='JSP_SINGLE_POINT_RAW',logic='AND',requires=['SELECTED_ONE_POINT_CORE','ORIGINAL_SELECTED_COEFFICIENT_NORMALIZATION','ORIGINAL_SELECTED_PRO_ELL_DESCENT','CERT_CRW21'],binding='h=0, same x/Kap/T/TWPl/TWAut/J and preserved kernels; does not assert arbitrary Kap or a universal arbitrary h theorem.'),
 ],
 nonlogical_shared_links=[
  dict(source='CRW6',target='JSP_SINGLE_POINT_RAW',reason='Removes actual completed full-block representation subproducer; does not construct patched modules.'),
  dict(source='CRW15',target='ORIGINAL_SELECTED_LIM',reason='Consumes the same original limit and proves all-truncation ranks; supplies no limit existence.'),
  dict(source='CRW18',target='ORIGINAL_PATCHED_SUPPORT_DIMENSION',reason='Uses the original dimension lower bound; does not prove existence of support or its dimension.'),
  dict(source='CRW20',target='JSP_SAME_IDEAL_HASAUT',reason='Consumes the fixed same-J all-level system; constructs no ordinary automorphic modules.'),
 ],
 not_claimed_closed=['S4 actual Lim existence','original RRObj/RMaps and compatible patched module construction','S5 support dimension/fiber producer','CoreBC coefficient normalization','RawMain pro-ell descent','JSP_SINGLE_POINT_RAW','ordinary/control/type/neatU/TThetaEx','four further Hida endpoints','same-J HasAut','complete CohP','LocCFT','universal arbitrary-Kap CohLim or general S6/GalOut','COUNT_II_SUPPORT','COUNT_I_PRODUCER','COUNT_V_PRODUCER','COUNT_III_PRODUCER'],
 quantifier_guards=[
  'Both original rank-four Links remain; ell=3 is explicitly included, with no inversion of n or n!.',
  'Fix iota first, then one common coefficient threshold for both Links; both HidaPropsAlt and P1core use the same original J in each ring.',
  'The same CCH point/finite extension/list/Kap and CAP T/TWPl are used; the chosen g=0 does not imply Sel1=0.',
  'B1 constant C remains before m and eventual N; the level chosen to transfer to the limit may depend on m.',
  'Lim, the patched ordinary point, coefficient DVR, completion, support ideal and annihilator/J equivalence must all belong to one common original construction.',
  'The original closureIdeal contains both every coefficient power and every open normal group neighborhood.',
  'The URep determinant is the full natural polynomial law over every scalar algebra, not merely a trace identity.',
  'The URep thick field is verified through the literal every-field NonSS definition; Ann(0) is not incorrectly placed inside a proper prime.',
  'The exact presentation uses D0=4d+4q and required support dimension 1+D0.',
  'Original complete CohP, LocCFT and old N4 are inherited unchanged; no new arithmetic existence is inferred from conditional algebra.',
 ],formal_correctness_assumed=True,peer_review='pending independent review of final proof and metadata hashes')
dump('closure.json',closure)
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.38',date='2026-11-22',
 source_commit=PIN,component='count_raw',main_tex_sha256=sha(tex),claims=claims,
 source_groups=groups,source_inventory=sources,
 source_files=[dict(path=path,sha256=sha(raw),full_file_sha256=sha(raw),bytes=len(raw)) for path,raw in sorted(cache.items())],
 inherited_proof_inputs=inherited,
 published_applications=dict(file='published_applications.json',sha256=sha((HERE/'published_applications.json').read_bytes()),ids=sorted(appids)),
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes()),portable=True,read_only_inputs=['pinned Lean checkout','reconstruction_v037']),
 validation=dict(pinned_blob_verified_files=len(cache),source_ranges=len(sources),distinct_source_ranges=len({(x['path'],x['line_start'],x['line_end']) for x in sources}),claim_source_ranges=sum(len(c['sources']) for c in claims),all_source_ranges_exact=True,claim_proof_blocks=len(claims),inherited_claim_proof_blocks=sum(len(x['claim_proof_blocks']) for x in inherited),new_lean_build=False,independent_human_mathematical_proof=True),
 scope_note='CRW3 is an exact checked A application; the other 20 claims are complete B proofs at their original conditional scopes. The actual S6 and cotangent producer are supplied; original limit/patching/descent and the remaining same-J arithmetic existence remain open.')
dump('provenance.json',prov)
loc=[f'CRW1-CRW21 source locators; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc += [f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",'file_sha256='+s['sha256'],'range_sha256='+s['range_sha256'],s['url'],'']
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f'''CRW1-CRW21: actual selected full-block completion, v0.38

Formal source assumed checked and correct. No Lean replay or build.
Source commit: {PIN}
main.tex SHA256: {sha(tex)}
provenance.json SHA256: {sha((HERE/'provenance.json').read_bytes())}
closure.json SHA256: {sha((HERE/'closure.json').read_bytes())}
published_applications.json SHA256: {sha((HERE/'published_applications.json').read_bytes())}

COMPLETED SUBSTANTIVE PRODUCERS

CRW2 constructs the actual rF and OO=completion of O[[S]]_(varpi),
including every original Ctx coefficient compatibility. CRW3 applies
Chenevier Theorem 2.22(i) to the actual full determinant: NP.span and
a=n give split absolute irreducibility over F=K((t)); the coefficient
ring is complete henselian. The theorem has no n! requirement, so
ell=3, n=4 is covered. CRW4 normalizes the actual polarization by
matrix units and a complete-ring inverse-square-root argument using
only 2 invertible. CRW5 constructs one finite original-B lattice from
the trace Gram matrix and proves uniform continuity. CRW6 handles the
literal coefficient-power AND open-normal-subgroup closed ideal, then
all its field-valued quotients. It constructs every actual URep field,
including thick, with AA=R and N=0. The nonsemisimple quotient cannot
occur; no incorrect Ann(0)<=Q assertion is used.

CRW7 proves exact relative cotangent duality. CRW8 proves derivative
boundedness directly from B/p=K[[t]] and m_B=p+(s). CRW9 writes the
ordered flag argument via a separating group-algebra element and
Lagrange idempotents. CRW10 checks every literal Selmer condition.
CRW11 proves injection modulo actual polarized coboundaries by using
the full determinant law, ordered characters, both auxiliary relations,
the original parameter and GenBy, then localization/completion. This
is the actual source ring, not a generic tangent space assumed to fit.

CRW12 proves finite Selmer stabilization on one SUPPLIED original Lim;
all cocycles, local witnesses and actions are matched on the same Ph0.
CRW13 preserves the original B1 constant before every truncation.
CRW14 uses finite DVR equations/Smith reduction to control approximate
boundaries, rather than assuming modular cocycles lift integrally.
CRW15 obtains literal K1 and its Laurent bound; K2/K3 are proved only
for the same selected g=0 full-block Kap. Sel1 is not zero.
CRW16 constructs actual cotangent generators, exactly D0=4d+4q.
CRW17 constructs the surjection OO[[X_D0]]->R. CRW18 proves presOut0
and the actual selected GalOut: every prime Z with dim(R/Z)>=1+D0
is zero. The argument asserts no existence of such a support prime.

CRW19 proves the complete h=0 ChainAbs on the actual supplied support
completion. It needs no connecting prime or move field. CRW20 writes
the exact one-point Core installation with the same RRObj/RMaps,
ordinary point, splitting prime and original J. Its dimension is
(1+D)+nq=1+D0 without an extra variable or altered exponent.

RETAINED CUT AND NEXT PRIORITY

The original selected h=0 Raw remains C. Its remaining cut comprises:
actual pro-ell quotient and same-object descent; actual coefficient
normalization and Unit parameter; original Lim(T); matched original
patched ring/maps/modules and S5 support dimension/fiber plus ann/J
equivalence. Those are not closed by naming their records. The next
best bounded supplier is the actual same-T Lim construction or the
single-point S5 module/support producer, after tracing which removes
more of this remaining conjunction. No arbitrary thick-prime chain
or nonzero odd-part branch is needed for the selected route.

Original ordinary/control/type/neatU/TThetaEx, the four further Hida
endpoints and all-level HasAut on the same J remain open. Complete
CohP, LocCFT and the old N4 remain inherited hypotheses. Both original
rank-four Links are preserved. Fix iota before one common coefficient
threshold for both links and both properties on each same ideal.
The CCH point/list/extension/Kap, CAP T/TWPl and later TWAut/J remain
coupled. Only Case III is removed for two-primary targets; RH still
needs I/II/V and unrestricted Dirichlet GRH also needs III.

METADATA

{len(claims)} proof blocks; {len(cache)} exact pinned source files;
{len(sources)} listed source ranges ({len({(x['path'],x['line_start'],x['line_end']) for x in sources})} distinct); {sum(len(c['sources']) for c in claims)}
claim/source range occurrences; {sum(len(x['claim_proof_blocks']) for x in inherited)}
inherited proof blocks. Builder accepts --source and --baseline and
writes only this component. Standalone TeX validation is recorded
separately under validation/. Independent review is pending.
'''
(HERE/'report.txt').write_text(report)
print(json.dumps({'claims':len(claims),'source_files':len(cache),'source_ranges':len(sources),
 'claim_source_ranges':sum(len(c['sources']) for c in claims),'inherited_blocks':sum(len(x['claim_proof_blocks']) for x in inherited),
 'main_sha256':sha(tex),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))
