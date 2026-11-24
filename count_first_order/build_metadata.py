#!/usr/bin/env python3
"""Portable CFO metadata builder. Inputs are read-only.

python build_metadata.py --source /path/to/lean_source \
  --baseline /path/to/reconstruction_v036
Only files next to this builder are written.
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
p.add_argument('--baseline', type=Path, default=HERE.parent.parent/'reconstruction_v036')
args = p.parse_args()
REPO, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda name, obj: (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==PIN
B='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
P=B+'PatchingModules/'
E=P+'EpsilonEtaMatrices/'
C=P+'DegreeCountCohomology/'
W=B+'WeilGroupCharacters/'
D=B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'

# Inclusive pinned line ranges. End zero means the end of the file.
# Formal proof routes locate the exact human endpoint; they are not proof inputs.
SPECS=[
 ('G01',W+'UniversalOrdinaryDeterminantRing.lean',[
  (10,42,'GFrame, original compact groups and local data'),
  (66,80,'G0, conjugation, full cyclotomic Gprime and scalar character'),
  (101,104,'IsForm, exponent 1-n and literal form matrix')]),
 ('G01',P+'PairedDualFirstOrderDualMatrixSpace.lean',[
  (10,107,'Loc, Glob, original Iu map, bottom intermediate D0 and full PL definition'),
  (192,226,'W1 and pairedDualFirstOrderDualMatrixSpace'),
  (232,247,'literal dY, LocAt, SelZ and Bd'),
  (251,294,'all NP data, both N1 clauses and old-subgroup N4'),
  (306,348,'Kap, rho1, w1, wi1 and literal Sel1/Bd1')]),
 ('G01',P+'ThetaCoefficientMapEq.lean',[
  (14,39,'TWGrp all-level data, ph_lim, tame kernel and normal H'),
  (49,61,'Eig, B1, B2 and their exact C/m/eventual-N order'),
  (244,258,'epsD, full TwZ/TwB, eta trace and Detects')]),
 ('G02',B+'CommutativeAlgebra/ResMapBijective.lean',[
  (72,77,'AdicCont definition'),(334,338,'PhiCond at every open subgroup')]),
 ('G02',P+'DeterminantPadicFree/LocallyConstantCocyclesFiniteOfPhi.lean',[
  (11,78,'finite modular cocycles from PhiCond and the open action kernel')]),
 ('G03',C+'SolCnt.lean',[
  (6,93,'DVR modules, approximate-solution submodules and division'),
  (94,180,'finite approximate quotients, stabilized image and iterative approximation'),
  (182,309,'complete limit, kernel finite generation and uniform torsion'),
  (313,393,'solCnt: uniform quotient-cardinality endpoint')]),
 ('G04',E+'ExistsNcardAnnihilatedCocyclesLeCoboundariesMul.lean',[
  (21,126,'dg_abs: function-module reduction to approximate equations'),
  (349,430,'actual uniform annihilated TwZ/TwB cardinality endpoint')]),
 ('G05',E+'Descend.lean',[
  (8,90,'PL compactness, affine kernel, cocycle powers and continuous factorization'),
  (104,150,'finite rho1 powers and residual cyclotomic identity'),
  (152,217,'descend with actual level kernel and normalized polarization')]),
 ('G06',E+'TwistedCocycleApplyOne.lean',[
  (150,200,'PL in the finite twisted cocycle kernel'),
  (202,269,'phEq_one and the full-group normal core'),
  (271,288,'phEq uniform over all modular TwZ and all j')]),
 ('G07',E+'DualN.lean',[
  (10,33,'full dualN statement and trivial tame linear action'),
  (36,115,'same local witness, normalization, descent and trace injection'),
  (122,154,'modular TwB comparison and exact cardinality cancellation')]),
 ('G07',C+'CCount.lean',[(6,0,'cCount: exact involution normalization factors')]),
 ('G08',E+'FixBdQZero.lean',[
  (1,0,'fixBd source endpoint for uniform congruence-kernel counts; CFO8 proves the finite-minor argument directly')]),
 ('G09',E+'CommutingMatrixOffdiagZero.lean',[
  (19,64,'full-span commuting matrices and skew invariants'),
  (158,0,'h0G uniform primal invariant endpoint')]),
 ('G09',E+'Rho1MapReductionLevel.lean',[
  (66,0,'h0v0 with original N4 at an arbitrary separately retained subgroup')]),
 ('G09',E+'FinrankCentralizerW1Le.lean',[
  (7,34,'distinct-eigenvalue centralizer rank'),
  (106,0,'h0q uniform added-prime invariant endpoint')]),
 ('G10',E+'PairEx.lean',[
  (6,75,'coefficient pairing and matrix trace pairing'),
  (77,139,'pairEx with literal primal/dual IsAd representations')]),
 ('G10',C+'IsDualPair.lean',[
  (13,37,'Bl, Zl, local constancy and cocycle conventions'),
  (43,75,'IsDualPair, LocCount, UnrCount and GWBare'),
  (79,158,'every ArData/Counts/ArSys field, IsAd and nu')]),
 ('G10',C+'AdExExt.lean',[(1,0,'extension of exact adjoint and dual actions across c')]),
 ('G11','src/ReciprocityTheory/GaloisValuations/Global.lean',[
  (13,82,'literal decomposition group, inertia and normality in decomposition')]),
 ('G11',C+'UnrBare.lean',[(5,113,'absolute procyclic quotient and exact unramified cocycle count source route')]),
 ('G12',W+'ContinuousResP.lean',[
  (73,103,'original HidaSetting, odd prime, old distinguished place and splitting'),
  (106,0,'original Lev, arithmetic projection and frame data')]),
 ('G12',C+'ArPres.lean',[
  (12,76,'disjoint exact place partition and original valuations'),
  (80,163,'arPres at every N with actual same e, local maps, old D0 and ph/ta images')]),
 ('G12',C+'ArPresAlt.lean',[(11,0,'complete original arithmetic presentation record')]),
 ('G12',C+'DecSplit.lean',[(6,0,'literal inclusion of split CM decomposition groups is a topological isomorphism')]),
 ('G12',C+'SumDegF.lean',[(6,0,'exact sum of ramification times inertia degrees')]),
 ('G12',C+'CcAt.lean',[(7,0,'real embeddings, actual complex conjugations and cyclotomic sign')]),
 ('G12','src/ReciprocityTheory/Hypotheses/GalCohDefs.lean',[
  (90,137,'orthogonal local condition, locDeg and IsCCAt definitions')]),
 ('G13','src/ReciprocityTheory/Hypotheses/GalCoh.lean',[
  (17,59,'local finiteness, local Tate duality and local Euler characteristic'),
  (151,189,'global finiteness and exact Greenberg-Wiles formula'),
  (195,0,'universal field/module/coefficient scopes of retained CohP components')]),
 ('G13',C+'LocBare.lean',[(5,121,'local cocycle and dual-invariant cardinalities'),(143,0,'locBare exact arithmetic specialization')]),
 ('G13',C+'GwBare.lean',[
  (15,125,'Selmer class/cocycle count and exact GWBare algebra'),
  (233,361,'perfect local cup product and actual number-field GWBare transport')]),
 ('G14',C+'UnrLoc.lean',[(6,46,'original J=I intersect residual-character kernels and prime-to-ell quotient')]),
 ('G14',C+'PresCounts.lean',[(9,0,'all ArData.Counts from the same presentation and retained CohP')]),
 ('G14',C+'ArSys.lean',[(8,0,'original all-level ArSys assembly with common dv and old D0')]),
 ('G15',W+'Inertia.lean',[(9,23,'actual muG and every original LocAb field')]),
 ('G15',C+'HomCount.lean',[(6,0,'LocAb factorization and exact scalar homomorphism bound')]),
 ('G15',C+'OneCount.lean',[(39,0,'scalar cocycle count using non-cyclotomic character and local duality')]),
 ('G16',E+'EpsilonEtaTensorDual.lean',[(11,43,'literal M1, EpsilonEtaTensorDual, b1 and Zb')]),
 ('G16',E+'EntryZero.lean',[
  (10,64,'finite coordinate filtration and triangular conjugation identity'),
  (110,187,'ordered character cocycle count and actual coordinate laws'),
  (204,322,'locV exponent on the same flags and ordered characters')]),
 ('G16',C+'FiltCount.lean',[(1,0,'finite successive-coordinate counting source target')]),
 ('G17',C+'SumCount.lean',[(1,0,'finite local sum cardinality with the upper-triangular coboundary subspace')]),
 ('G17',E+'OneLevel.lean',[
  (236,350,'oneLevel source endpoint, actual local conditions and old tame factors'),
  (366,424,'actual complex-conjugation matrix and real-place fixed-point count'),
  (425,483,'product estimates and exact one-level cancellation')]),
 ('G18',E+'BdCard.lean',[(65,0,'selN: literal Sel1 and Bd1 versus normalized global cocycles')]),
 ('G18',C+'PolZCases.lean',[(1,0,'normalization at c and exact index-two cocycle extension')]),
 ('G18',C+'AdicLC.lean',[(6,16,'nilpotent coefficient adic continuity equals local constancy')]),
 ('G19',E+'W1BoundArithmeticRankTwo.lean',[
  (30,38,'exact exponent-sum identity'),
  (40,165,'all-level W1_bound_arithmetic_rank_two including old N4 and every fixed-point estimate')]),
 ('G20',E+'B1abs.lean',[(12,13,'abstract B1 assembly with original ArSys, LocAb, PhiCond and exact endpoint')]),
 ('G20',P+'AutomorphicDetection/BoundW1Arithmetic.lean',[(7,16,'b1Ar original arithmetic bound consumer; CFO only supplies its selected scope')]),
 ('G21',P+'TaylorWilesObstructionBound.lean',[
  (13,31,'unchanged Norm and complete CohP package'),
  (33,85,'actual locOf/globOf/residOf/pairOf dictionaries'),
  (88,124,'every original TWPl field, LocCFT and ArPl'),
  (126,154,'B1/B2/HasAut/PfromAut with exact original arithmetic quantifiers')]),
 ('G21',P+'ChebotarevFamilies/PFromAutOf.lean',[
  (30,81,'same point/list/J and PL-kernel condition'),
  (82,126,'same Pt B1/B2, original Raw and h=0 NiceI P1core branch')]),
 ('G21',D+'THidaU.lean',[(38,48,'same original ideal for HidaPropsAlt and HasAut')]),
 ('G21',D+'LinkTwo.lean',[(13,51,'both original rank-four Links, common kappa and distinct auxiliary primes')]),
 ('G21',D+'PotentialModularityTower.lean',[(38,55,'original tower data'),(63,66,'fixed iota before one common coefficient threshold')]),
]

cache,groups,sources={},{},[]
for group,path,ranges in SPECS:
    raw=(REPO/path).read_bytes()
    if path not in cache:
        assert raw==subprocess.check_output(['git','show',PIN+':'+path],cwd=REPO),path
        cache[path]=raw
    lines=raw.splitlines(keepends=True)
    for first,last,decl in ranges:
        last=last or len(lines)
        assert 1<=first<=last<=len(lines),(path,first,last,len(lines))
        block=b''.join(lines[first-1:last])
        sid=f'{group}-{len(groups.get(group,[]))+1}'
        sources.append(dict(id=sid,group=group,path=path,declaration=decl,
            line_start=first,line_end=last,sha256=sha(raw),full_file_sha256=sha(raw),
            range_sha256=sha(block),range_bytes=len(block),verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{first}-L{last}'))
        groups.setdefault(group,[]).append(sid)

titles=[
 'The selected original objects and the literal B1 target',
 'Finite modular cocycles from full PhiCond and the complete adic function module',
 'Independent complete-DVR approximate-solution and uniform counting lemma',
 'Full selected uniform annihilated TwZ versus TwB estimate',
 'Exact pro-ell affine-kernel descent on the original level projection',
 'Eventual Frobenius comparison uniform over every modular twisted cocycle',
 'Full selected dualN quantifiers and exact involution normalization',
 'Uniform congruence-kernel bound by a fixed nonzero matrix minor',
 'Primal, old-D0 and added-prime invariant bounds on the original point',
 'Actual primal/dual actions and the exact cyclotomic Tate pairing',
 'Original decomposition group modulo inertia, with checked finite theorem import',
 'Every original arithmetic presentation at every Taylor-Wiles level',
 'Full local/global count interfaces derived from the unchanged CohP hypothesis',
 'Exact unramified cardinality and complete all-level original ArSys',
 'Original LocAb diagonal count and non-cyclotomic rank-one cocycle count',
 'Complete upper-triangular ordinary cocycle filtration and cardinality',
 'Ordinary local coboundary factor and exact real-place fixed rank',
 'Literal Sel1/Bd1 quotient equals the original global Selmer condition',
 'One-level Greenberg-Wiles count with same local matrices and old subgroup',
 'Exact 4[Lplus:Q]+4q exponent and literal selected B1 quantifier order',
 'Install coupled Choice/B1/B2 on the same point/Kap/T/J, with residual producers explicit',
]
cg={
1:['G01','G21'],2:['G01','G02'],3:['G03'],4:['G01','G02','G03','G04'],
5:['G01','G05','G10'],6:['G01','G02','G05','G06'],
7:['G01','G04','G05','G06','G07','G10'],
8:['G08'],9:['G01','G08','G09'],10:['G01','G10'],
11:['G11'],12:['G01','G10','G12','G21'],
13:['G10','G12','G13','G21'],14:['G11','G12','G13','G14','G21'],
15:['G01','G10','G13','G15','G21'],16:['G01','G15','G16'],
17:['G01','G12','G16','G17'],18:['G01','G10','G16','G17','G18'],
19:['G01','G07','G09','G10','G12','G13','G14','G16','G17','G19'],
20:['G01','G19','G20','G21'],21:['G01','G20','G21'],
}
deps={
1:['CCH1','CCH2','CCH3','CCH13','CCH15','CCH17','CAP13'],
2:['CFO1','CAP1','CAP2'],3:[],4:['CFO2','CFO3','CCH3','CCH15'],
5:['CFO1'],6:['CFO2','CFO5'],7:['CFO4','CFO5','CFO6'],
8:[],9:['CFO1','CFO8'],10:['CFO1'],11:[],12:['CFO1'],
13:['CFO12'],14:['CFO11','CFO12','CFO13'],15:['CFO13'],
16:['CFO15'],17:['CFO12','CFO16'],
18:['CFO10','CFO13','CFO14','CFO16'],
19:['CFO7','CFO9','CFO10','CFO12','CFO13','CFO14','CFO16','CFO17','CFO18'],
20:['CFO19'],21:['CFO20','CCH13','CCH15','CCH16','CCH17','CAP13','CAP17','JSP11','QX4','QX10','YX2','KA5','KA6'],
}
hyp={
1:['Same original HidaSetting/V0/Resid, actual T/TWPl, same CCH extended full-block NP and g=0 Kap; complete CohP and LocCFT; old N4, residual cyclotomic nontriviality, exact PL-kernel, Eig and Detects.'],
2:['Original PhiCond on Gamma0, including every open subgroup; finite continuous F_ell-module action.'],
3:['A=k[[t]], finite k; C complete/separated/t-torsion-free; Cprime separated/t-torsion-free; finite S1/tC; every exact kernel element becomes an element of B after some t-power.'],
4:['Full selected g=0 TwZ/TwB, original finite detector Detects, full PhiCond and finite full-cyclotomic-kernel list.'],
5:['Original TWGrp fields and normal H; exact PL-kernel of rho; odd ell; selected IsAd action; normalized cocycle zero on every original tame element.'],
6:['Same full original TWGrp.ph_lim, PL-kernel and PhiCond; no Frobenius sign replacement.'],
7:['Selected a=n, g=0; odd ell, PhiCond, exact PL-kernel and Detects; every admissible repprime with Finite(Zl repprime).'],
8:['Fixed integral finite matrix over k[[t]]; fraction-field kernel rank given; no integral eigenbasis assumption.'],
9:['Original full NP.span and odd ell; old N4 at separately retained D0; same distinct integral Eig roots for each s_j.'],
10:['Original full-block NP.form and chosen g=0 Kap; finite coefficient field; same representation inflated through p_N.'],
11:['Number field, algebraic closure, fixed valuation over a finite prime; checked finite Galois decomposition/inertia theorem.'],
12:['Original HidaSetting, V0.Sprime=s.S, T and literal TWPl at all levels; all e/local/valuation/splitting fields are preserved.'],
13:['Complete unchanged CohP; actual finite place partition containing all places above ell; ell odd; finite perfect F_ell-valued dual pairs and continuous actions.'],
14:['Same original residue-field characters and IsCoef; finite ell-torsion continuous module trivial on J; CFO11; retained CohP for the remaining Counts fields.'],
15:['Exact retained LocCFT with common dprime sum; local LocCount from CohP; original ordered N1 non-cyclotomic ratios and adic continuity.'],
16:['Original same flags w and ordered characters; exact upper-triangular/diagonal-mu Zb condition; scalar local estimates.'],
17:['Same full-block primal module, ordinary flag and original real-place conjugations with epsilon=-1; ell odd.'],
18:['Actual normalized first-order functions and local equations; original J inertia kernels; finite global H1 from CohP.'],
19:['Same original ArSys; full selected dualN; old N4 and Eig; full CohP and LocCFT; N in the common eventual set for fixed m.'],
20:['All retained original arithmetic hypotheses in CFO1; same chosen full-block g=0 Kap; no pointwise equality dprime_v=d_v is assumed.'],
21:['Same original J and coupled CCH Choice/B2 witness; same all-level T/TWPl; unchanged CohP/LocCFT and all outer source thresholds; retained ordinary/Hida/HasAut/Raw producers.'],
}
tex=(HERE/'main.tex').read_bytes()
lines=tex.splitlines(keepends=True)
claims=[]
for i,title in enumerate(titles,1):
    cid=f'CFO{i}'
    starts=[j for j,line in enumerate(lines) if line.strip()==f'% BEGIN {cid}'.encode()]
    ends=[j for j,line in enumerate(lines) if line.strip()==f'% END {cid}'.encode()]
    assert len(starts)==len(ends)==1,cid
    first,last=starts[0],ends[0]
    block=b''.join(lines[first:last+1])
    assert first<last and f'\\label{{claim:{cid}}}'.encode() in block
    claims.append(dict(id=cid,title=title,introduced_in='0.37',classification='B',
      status='complete human proof at the printed original-data scope; conditional inputs remain explicit',
      depends_on=deps[i],classical_inputs=['CFO_LOCAL_DECOMP'] if i==11 else [],
      dependency_scope=(
       'Only the original arithmetic data dictionary of CFO1 is used, not its chosen-point existence.' if i in [12,13,14] else
       'CCH15 and CCH16 must be consumed on the same constructed x/Kap/list; no universal arbitrary-Kap theorem or ordinary existence is inferred.' if i==21 else
       'Exact printed subclaims only; retained hypotheses are not silently promoted to producers.'),
      original_hypotheses=hyp[i],
      remaining_inputs=(['ordinary/control/type/neatU/TThetaEx','four additional Hida endpoints','same-J HasAut','h=0 Raw','complete CohP and LocCFT/setting side conditions'] if i==21 else []),
      proof_location=dict(file='count_first_order/main.tex',label='claim:'+cid,line_start=first+1,line_end=last+1,sha256=sha(block),bytes=len(block)),
      source_groups=cg[i],sources=[s for s in sources if s['group'] in cg[i]]))

def block_of(raw,cid):
    ls=raw.splitlines(keepends=True)
    start=next((i for i,line in enumerate(ls) if line.strip()==f'% BEGIN {cid}'.encode()),None)
    if start is not None:
        end=next(i for i,line in enumerate(ls) if line.strip()==f'% END {cid}'.encode())
    else:
        label=next(i for i,line in enumerate(ls) if f'\\label{{claim:{cid}}}'.encode() in line)
        start=max(i for i in range(label+1) if b'\\paragraph{' in ls[i])
        end=next((i-1 for i in range(label+1,len(ls)) if b'\\paragraph{' in ls[i]),len(ls)-1)
    return dict(id=cid,line_start=start+1,line_end=end+1,sha256=sha(b''.join(ls[start:end+1])))
inherited=[]
for path,ids,role in [
 ('count_choice/main.tex',['CCH1','CCH2','CCH3','CCH13','CCH15','CCH16','CCH17'],
  'Same full-block chosen g=0 Kap, exact TwZ/TwB, full finite detector/Eig and finite coefficient extension, old N4, same point kernel, coupled literal B2 and conditional same-J installation.'),
 ('count_auxiliary_primes/main.tex',['CAP1','CAP2','CAP13','CAP17'],
  'Full PhiCond from unchanged CohP; realize exactly the same finite list by actual all-level TWGrp/TWPl; IsRes remains conditional on original type data.'),
 ('joint_support/main.tex',['JSP11'],
  'Only its complete same-point PL-kernel proof and conditional same-J one-point consumer; remaining original HasAut/Raw are not assumed proved.'),
 ('symplectic_modular_support/main.tex',['QX4','QX10'],
  'Both literal rank-four Links and exact common support requirement.'),
 ('case_two_installation/main.tex',['YX2'],'Exact CountII consumer scope.'),
 ('count_i_aggregation/main.tex',['KA5','KA6'],
  'Only CaseIII vacuity for two-primary targets, with I/II/V still substantive.'),
]:
    raw=(BASE/path).read_bytes()
    inherited.append(dict(path='reconstruction_v036/'+path,sha256=sha(raw),claim_ids=ids,
        claim_proof_blocks=[block_of(raw,cid) for cid in ids],role=role))
known={c['id'] for c in claims}|{i for x in inherited for i in x['claim_ids']}
assert all(d in known for ds in deps.values() for d in ds)

applications=[dict(
 id='CFO_LOCAL_DECOMP',classification='A',status='exact primary theorem application with hypotheses checked',
 title='Finite decomposition/completion and inertia residue quotient, with compatible restrictions',
 primary_url='https://www.jmilne.org/math/CourseNotes/ANT.pdf',
 author='J. S. Milne',work='Algebraic Number Theory',version='3.08',publication_date='2020-07-19',
 theorem_locators=[
  dict(theorem='Theorem 7.58(a)',printed_pages='130-131',pdf_pages_one_based=[132,133],
       scope='Finite Galois extension of complete discretely valued fields with separable residue extension: quotient by inertia is the residue Galois group.'),
  dict(theorem='Proposition 8.10',printed_pages='139',pdf_pages_one_based=[141],
       scope='Finite Galois extension of number fields: the chosen decomposition group is the Galois group of the corresponding completions.'),
  dict(theorem='Proposition 8.13(b)',printed_pages='141',pdf_pages_one_based=[143],
       scope='Restriction in a finite Galois tower maps the chosen decomposition group onto that of the Galois subextension.')],
 hypotheses_checked=[
  'The original field is a number field and Omega its algebraic closure; the inverse system consists only of finite Galois subextensions.',
  'The valuation lies over an original finite prime; corresponding completions are complete discretely valued number-field completions.',
  'Their residue fields are finite and therefore perfect, and every finite residue extension is separable.',
  'In each transition the lower finite subextension is Galois, so the fixing subgroup is normal as required in Proposition 8.13(b).',
  'The source Dec is the valuation stabilizer and source Ine acts trivially on its residue field; these are the same definitions used by the finite theorem.'],
 human_proof_use='CFO11 uses only these finite facts; it proves the absolute inverse-limit quotient, residue algebraic-closure argument and Frobenius normalization. CFO14 proves the entire cocycle count independently.',
 excluded_scope='No local/global duality, local class-field-theory LocCFT, or ordinary automorphic existence is certified by this application.',
 checked_on='2026-11-22',
 primary_retrieval_refs=['turn207688430view0','turn207688430view1','turn207688430view2'],
 errata_url='https://www.jmilne.org/math/CourseNotes/errata.html',
 errata_checked='Checked the author errata. The proof never treats an infinite algebraic extension as a complete DVR. The finite theorem is used as stated; the absolute passage is written in CFO11.',
 exact_source_groups=['G11'],hypotheses_rechecked_in_this_component=True)]
dump('published_applications.json',applications)

old=json.loads((BASE/'count_choice/closure.json').read_text())
remaining=[x for x in old['remaining'] if x['id']!='JSP_FIRST_ORDER_BOUND']
assert len(remaining)==4
closed=[dict(
 id='JSP_FIRST_ORDER_BOUND',old_classification='C',
 by=[f'CFO{i}' for i in range(1,22)],
 scope='Exact B1 on the CCH15-selected full-block a=n=4,g=0 Kap, for the same actual T/TWPl and original old D0: exists C, forall m, eventually N, finite Sel1 and #Sel1 <= #Bd1 * #k^(m*(4*[Lplus:Q]+4*T.q)+C).',
 conditional_inputs='Original complete CohP, LocCFT, IsCoef/setting/level side conditions, old N4, exact PL-kernel, finite Eig and Detects; the selected point supplies these last fields through the inherited same-witness construction.',
 same_witness_guard='CCH15 Choice, CCH16 B2, and CFO20 B1 are consumed on the same extended point and g=0 Kap, then CAP13 realizes exactly its list. No arbitrary-Kap closure.')]
closure=dict(
 schema='rh-human-component-closure/1',artifact_version='0.37',component='count_first_order',
 source_commit=PIN,proof_sha256=sha(tex),proof_claims=[c['id'] for c in claims],
 closed=closed,remaining=remaining,
 classical_input_nodes=[dict(id='CFO_LOCAL_DECOMP',classification='A',status='checked direct application',application_file='published_applications.json')],
 selected_frontier_status={
  'JSP_FIRST_ORDER_BOUND':'CLOSED on the exact CCH-selected h=0 NiceI full-block g=0 witness; all original side hypotheses retained.',
  'COUPLED_CHOICE_B1_B2':'COMPLETE conditional supplier on the identical xprime/Kap/list/T/J. Both earlier CCH outputs remain coupled.',
  'COUNT_II_SUPPORT':'OPEN C: original ordinary/control/type/fibers, four Hida endpoints, same-J all-level HasAut and h=0 Raw remain, with unchanged CohP/LocCFT and all original setting data.',
  'FirstOrderDualArithmeticBound':'The universal predicate for arbitrary Kap is not claimed. The selected exact consumer instance is reconstructed.',
  'dualN':'Every C-before-m-before-eventual-N-before-repprime quantifier is proved at the selected a=n,g=0 scope, including Finite(Zl repprime) as the original premise.',
  'ArSys':'All original ArSys/Counts fields are constructed on the actual T/TWPl family under complete CohP; no actual T existence is inferred without CAP13 and its original inputs.',
  'RH_case_note':'Only CaseIII is removed for two-primary targets by KA5/KA6; I/II/V remain substantive. Unrestricted Dirichlet GRH retains III.'},
 sufficient_rules=[
  dict(conclusion='SELECTED_ORIGINAL_B1',
       requires=['ORIGINAL_FULL_BLOCK_CCH_WITNESS','SAME_ORIGINAL_T_AND_TWPL','ORIGINAL_COH_P_AND_LOCCFT','OLD_N4_AND_EXACT_PL_KERNEL','CERT_CFO1_CFO20','CFO_LOCAL_DECOMP'],
       logic='AND',binding='One fixed point/list/Kap/T/TWPl, with old D0 and all original arithmetic data; one C before all m and eventual N.'),
  dict(conclusion='COUPLED_ORIGINAL_CHOICE_B1_B2',
       requires=['CERT_CCH15_CCH16','CERT_CAP13','CERT_CFO20_CFO21','ORIGINAL_COH_P_AND_SIDE_CONDITIONS'],
       logic='AND',binding='CCH15 selects the same xprime,j,Kap,sg,al; CAP13 realizes that list; CFO20 adds B1; CCH16 B2 remains on that very Kap.'),
  dict(conclusion='SAME_J_P1CORE',
       requires=['JSP_SAME_IDEAL_HASAUT','JSP_SINGLE_POINT_RAW','CERT_CIP10_CIP11','CERT_CAP2_CAP13','CERT_CCH1_CCH17','CERT_CFO1_CFO21','CERT_JSP9_JSP11','ORIGINAL_COH_P_AND_SIDE_CONDITIONS'],
       logic='AND',binding='Fix original B,r,J before the arbitrary h=0 NiceI point. Use the coupled supplier without changing the ideal, polynomial-law determinant, O-map or point kernel.'),
  dict(conclusion='COUNT_II_SUPPORT',
       requires=['BOTH_ORIGINAL_LINKS','SAME_J_HIDAPROPSALT_AND_P1CORE_FOR_EACH_LINK','ONE_COMMON_COEFFICIENT_THRESHOLD_AFTER_FIXED_IOTA','CERT_CFO21'],
       logic='AND',binding='Each Link keeps its own original ring and same ideal for HidaPropsAlt AND P1core; both Links and all later coefficient Spaces remain quantified.')],
 nonlogical_shared_links=[
  dict(source='CFO20',target='JSP_SINGLE_POINT_RAW',reason='Supplies the first-order bound of the same Pt; stable-prime propagation still needs Raw.'),
  dict(source='CFO21',target='JSP_SAME_IDEAL_HASAUT',reason='Uses the all-level same-J HasAut instance; constructs no ordinary automorphic modules.'),
  dict(source='CFO14',target='JSP_ORIGINAL_ORDINARY_DATA',reason='The arithmetic group/count dictionary is not ordinary control or automorphic existence.')],
 not_claimed_closed=[
  'CohP','LocCFT','universal arbitrary-Kap dualN or FirstOrderDualArithmeticBound',
  'universal arbitrary-Kap TaylorWilesObstructionBound','original TThetaEx/type/neatU',
  'original ordinary/control/IsUniv and arithmetic fibers','four Hida endpoints','same-J HasAut','h=0 Raw',
  'COUNT_II_SUPPORT','COUNT_I_PRODUCER','COUNT_V_PRODUCER','COUNT_III_PRODUCER'],
 quantifier_guards=[
  'ell is odd and explicitly may be 3; n=4 in each original Link. No n or n! is inverted.',
  'The full first-order space is Mat_4(A_m) despite g=0; no Sel1=0 claim.',
  'The old V0.frame.D0 is retained through N4 and the exact ArSys distinguished image, even when globOf.frame.D0 is bottom.',
  'The dualN constant is chosen before m; its eventual set of N is uniform over every later repprime satisfying the literal IsAd and finite-Zl premises.',
  'The finite modular cocycles need not lift to integral exact solutions; CFO3 supplies the uniform approximation argument.',
  'The two degree families dprime_v and d_v need only have the same total d; no pointwise equality is substituted.',
  'Original local ordinary conditions use the same w_v, ordered psi_i, actual mu_v, and one local coboundary witness.',
  'Each added local dual coboundary uses the same matrix for ph and ta in the same original decomposition image.',
  'CCH Choice, same chosen g=0 B2, and new B1 are a coupled witness rule; no different Kap or ideal is substituted.',
  'Full original CohP and LocCFT remain explicit; only their conditional count consequences have been proved.',
  'Fix iota before one common coefficient threshold, then every later Space and original B,Lambda. The pointwise C does not replace that threshold.',
  'Both rank-four Links remain, with common kappa and distinct auxiliary primes; each keeps one original J carrying HidaPropsAlt and P1core.'],
 formal_correctness_assumed=True,peer_review='pending independent review bound to the final proof and metadata hashes')
dump('closure.json',closure)
prov=dict(
 schema='rh-human-component-provenance/1',artifact_version='0.37',date='2026-11-22',
 source_commit=PIN,component='count_first_order',main_tex_sha256=sha(tex),
 claims=claims,source_groups=groups,source_inventory=sources,
 source_files=[dict(path=path,sha256=sha(raw),full_file_sha256=sha(raw),bytes=len(raw)) for path,raw in sorted(cache.items())],
 inherited_proof_inputs=inherited,
 published_applications=dict(file='published_applications.json',sha256=sha((HERE/'published_applications.json').read_bytes()),ids=['CFO_LOCAL_DECOMP']),
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes()),portable=True,read_only_inputs=['pinned Lean checkout','reconstruction_v036']),
 validation=dict(pinned_blob_verified_files=len(cache),source_ranges=len(sources),claim_source_ranges=sum(len(c['sources']) for c in claims),
   all_source_ranges_exact=True,claim_proof_blocks=len(claims),inherited_claim_proof_blocks=sum(len(x['claim_proof_blocks']) for x in inherited),
   new_lean_build=False,independent_human_mathematical_proof=True),
 scope_note='All 21 claims are completed B arguments at the printed conditional scope. The selected original first-order supplier is supplied with its literal exponent and witness. The complete CohP/LocCFT and ordinary/HasAut/Raw producers are not declared proved. One new A certificate covers the exact finite decomposition/inertia theorem; its absolute passage and the cocycle count are proved.')
dump('provenance.json',prov)
loc=[f'CFO1-CFO21 source locators; commit {PIN}',f'main.tex SHA256 {sha(tex)}','']
for s in sources:
    loc.extend([f"{s['id']} | {s['declaration']}",f"{s['path']}:{s['line_start']}-{s['line_end']}",
        'file_sha256='+s['sha256'],'range_sha256='+s['range_sha256'],s['url'],''])
(HERE/'source_locators.txt').write_text('\n'.join(loc))
report=f"""CFO1-CFO21: exact selected first-order bound, v0.37

Source commit: {PIN}
main.tex SHA256: {sha(tex)}
provenance.json SHA256: {sha((HERE/'provenance.json').read_bytes())}
closure.json SHA256: {sha((HERE/'closure.json').read_bytes())}

COMPLETED OUTPUT

The same actual full-block a=n=4, g=0 Kap selected in CCH15 now has
literal T.B1 with exponent 4[Lplus:Q]+4T.q. One constant C is chosen
before every coefficient length m; only the eventual lower bound on
the level N may depend on m. Finiteness and the bound on the actual
Sel1/Bd1 sets are proved. Both m=0 and ell=3 are included.

CFO2-CFO7 prove the entire selected dualN estimate. The uniform
approximation lemma is written independently: finite residual
approximate solutions stabilize, completeness produces exact kernel
approximants, the kernel is finitely generated by digit lifting,
Detects gives uniform torsion modulo coboundaries, and a finite cover
gives a constant independent of m. Modular cocycles are not assumed
to lift to integral exact solutions. The original PL/affine kernel
argument descends normalized cocycles along the actual p_N. The
ph_lim comparison is uniform over every modular twisted cocycle.
The dualN conclusion retains every admissible repprime satisfying
IsAd and Finite(Zl repprime), after C, m and eventual N, in that order.

CFO8-CFO10 give the three exact matrix invariant bounds and the
cyclotomic pairing. N4 is used at the OLD V0.frame.D0, not the bottom
subgroup in an intermediate globOf frame. Distinct integral eigenvalues
are used only to diagonalize over the fraction field; a fixed nonzero
minor handles denominators uniformly at all truncations.

CFO11-CFO14 construct every original ArSys/Counts field on the actual
TWPl family, at every N, under unchanged complete CohP. The original
place partition, valuations, local inclusions, common local degrees,
real conjugations, old D0 image and same local ph/ta images are checked.
The unramified cocycle count is exactly #M, using the actual residual-
character inertia kernel and its prime-to-ell quotient. The only new
published A input is Milne's finite decomposition/inertia theorem:
ANT v3.08 Theorem 7.58(a), Propositions 8.10 and 8.13(b), with exact
hypotheses checked against the primary text. The infinite quotient
D/I=Zhat and the entire cocycle count are then proved in the chapter.

CFO15-CFO20 reconstruct the local/global cancellation. LocAb bounds
diagonal homomorphisms; N1's second clause bounds each ordered
off-diagonal character cocycle; a triangular coordinate filtration
counts the actual ordinary cocycles. The upper-triangular coboundary
factor removes m*(n+choose(n,2)) per l-adic place. Every real place
contributes the exact factor Q^(m*choose(n,2)). The two degree sums
are checked separately and need not agree place by place. At n=4,
the cancellation removes m*(10*#Vl+6*d) and leaves exactly m*(4*d+4*q),
plus the fixed constant. The original Sel1/Bd1 quotient is explicitly
identified with the global Selmer condition; no first-order vanishing
is inferred from g=0.

SELECTED FRONTIER CHANGE

Remove JSP_FIRST_ORDER_BOUND only on the selected h=0 NiceI route.
CCH15 Choice, CCH16 B2 and CFO20 B1 form one coupled witness rule on
the same extended point, Kap, list, T/TWPl, original O-map, determinant
law and point kernel. The ideal J stays fixed before all those choices.
The universal FirstOrderDualArithmeticBound for arbitrary Kap is not
claimed, and neither is arbitrary-Kap dualN.

Four inherited Count-II producer entries remain: original ordinary/
control/type-neatU/TThetaEx/arithmetic-fiber data; the four further Hida
endpoints; full same-J all-level HasAut; and original one-point h=0 Raw.
Complete CohP, LocCFT and every original setting/coefficient condition
remain explicit. CAP17 still gives IsRes only for supplied type data.
COUNT_II_SUPPORT remains open. Both original rank-four Links, the
distinct auxiliary primes, fixed iota before one common coefficient
threshold, and every later Space remain unchanged. KA5-KA6 remove
only CaseIII for two-primary targets, including RH; I, II and V remain.
Unrestricted Dirichlet GRH retains its additional Case-III producer.

METADATA

{len(claims)} proof blocks, {len(cache)} pinned source files,
{len(sources)} distinct source ranges and
{sum(len(c['sources']) for c in claims)} claim/source references.
{sum(len(x['claim_proof_blocks']) for x in inherited)} inherited proof
blocks are bound to exact read-only v0.36 bytes. Every source file is
compared with git show at the pinned commit. The builder accepts
--source and --baseline and writes only inside this component.
Independent review and standalone TeX result are recorded separately.
"""
(HERE/'report.txt').write_text(report)
print(json.dumps(dict(main_sha256=sha(tex),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
 closure_sha256=sha((HERE/'closure.json').read_bytes()),claims=len(claims),
 source_files=len(cache),ranges=len(sources),claim_source_references=sum(len(c['sources']) for c in claims)),indent=2))
