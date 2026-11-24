#!/usr/bin/env python3
"""Bind SP1--SP10 to exact pinned Lean declarations and readable proof bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
REPO = parser.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
CA = AV + 'CommutativeAlgebra/'
GM = CA + 'GradedModulesLength/'
SG = AV + 'SymplecticGSp4/'
HV = AV + 'HeightAndVanishing/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
GE = 'src/Formalism/SharpRestriction/ValuationFrobeniusEpsilon/LeastPrimeTwists/QuotientShiftIrreducible/NoetherianQuotientCalc/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}


def source(path, name, role='Matched definition or proof endpoint; readable reconstruction in the stated SP scope'):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if m:
            starts.append((n, m.group(1)))
    matched = [(n, s) for n, s in starts if s == name or (name.startswith('@') and s.rsplit('.', 1)[-1] == name[1:])]
    if len(matched) != 1:
        raise ValueError((path, name, matched))
    start, spelling = matched[0]
    end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b''.join(lines[start - 1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                   'lines': len(lines), 'url': f'{URL}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{URL}/blob/{PIN}/{path}#L{start}-L{end}', 'role': role,
            'verified_equal_to_pinned_git_blob': True}


spec = {
 'SP1': {
  CA+'ResMapBijective.lean': ['IsCO', 'PtDer', 'HasWt', 'satSq', 'cotLat', 'cotSpan', 'cotLen'],
  CA+'OrbitVanishingLocal.lean': ["LemmaM'"],
  GM+'Mprime.lean': ['der_satSq', 'len_le_of_inj', '@mprime_holds'],
 },
 'SP2': {
  GE+'EulerVanishingBelowDimension.lean': ['chi', 'HidaSetting'],
  GE+'RulePos.lean': ['rulePos'], GE+'RuleMono.lean': ['ruleMono'], GE+'RuleUB.lean': ['ruleUB'],
  GE+'VanishingBelowDimensionRule.lean': ['dev_reduce', 'prime_step'],
  GE+'EulerRuleProductZero.lean': ['euler_char_product_eventually_add', 'euler_rule_product_zero'],
  GM+'LaDifPerm.lean': ['@la_holds'],
 },
 'SP3': {
  GM+'ToDegInjective.lean': ['mN', 'idD', 'tsF', 'tsR', 'ts'],
  GM+'ExistsSecNotMem.lean': ['@zi_holds'],
  GM+'ZmOfHom.lean': ['zmJ', 'zm_abs', '@zm_holds'],
  GM+'ExistsNotInP.lean': ['@zp_holds'], GM+'FixHolds.lean': ['@fix_holds'],
  GM+'XProjZero.lean': ['@ct_holds'], GM+'SameDegreeZeroOfRestriction.lean': ['@zii_holds'],
  GM+'AdmissibilityHolds.lean': ['@admissibility_holds'],
  GM+'EventuallyMQGrFiniteAnnihilator.lean': ['@eventually_mQ_gr_finite_annihilator'],
  GM+'TspHolds.lean': ['@tsp_holds'], GM+'OzTwoMulEqPow.lean': ['@oz_two_mul_eq_pow'],
 },
 'SP4': {
  CA+'OrbitVanishingLocal.lean': ['M2', 'M4', 'Covers'],
  GM+'SliceHolds.lean': ['@slice_holds'], GM+'FinHolds.lean': ['@fin_holds'],
  GM+'LocLenQuotientWeightPieceLeOne.lean': ['@locLen_quotientWeightPiece_le_one'],
  GM+'LocLenAPieceIdeal2LeTwoPow.lean': ['@locLen_aPiece_ideal2_le_two_pow'],
 },
 'SP5': {
  CA+'OrbitVanishingLocal.lean': ['IsChart', 'SmoothPt', 'mDims', 'M1'],
  GM+'LinPartApply.lean': ['@rk_holds'], GM+'SmHolds.lean': ['sm_smith', 'sm_lift', '@sm_holds'],
  GM+'CutHolds.lean': ['@cut_holds'], GM+'ToDegInjective.lean': ['IsChart0', 'leadKer', 'cnt'],
  GM+'Latfil.lean': ['@latfil_holds'], GM+'Satfil.lean': ['@satfil_holds'],
  GM+'ReesGradedPieceSurjection.lean': ['@hf_holds'],
  GM+'FrobeniusInclusionXEqMulQ.lean': ['@num_holds'], GM+'AdmissibleMonoIdeal.lean': ['@low_holds'],
 },
 'SP6': {
  CA+'OrbitVanishingLocal.lean': ['IsNVal', 'IsWRing', 'M1', 'M2', 'M3', 'M4', 'M5', 'Covers', 'LemmaM'],
  GM+'NzCoeffMul.lean': ['nz_comp', '@nz_holds'], GM+'LkHolds.lean': ['@lk_holds'],
  GM+'HerbrandFinLen.lean': ['@th_holds'], GM+'TwoSigned.lean': ['@up_holds'],
  GM+'AlgMemCoef.lean': ['@core_holds'], GM+'MainCotSpan.lean': ['@main_holds'],
 },
 'SP7': {
  SG+'DecompSigmaOrd.lean': ['Raw', 'Psi', 'Sb', 'T', 'UnrT', 'Good', 'sha'],
  SG+'EntryMem.lean': ['ShaCoc', 'Model', 'A', 'gr', 'eqns', 'SoFin'],
  SG+'ShaCoc.lean': ['exists_norm', 'main_abs', 'conc', '@shaCoc'],
  SG+'MPrime.lean': ['der_zero', 'len_le', '@mPrime'],
  CA+'ResMapBijective.lean': ['Lift.Generates'],
 },
 'SP8': {
  HV+'DirichletPrimeToLPartMulLPowerPart.lean': ['comp', 'th0', 'th1', 'chiP', 'c2', 'f0', 'n0', 'PsiEven', 'IsChar', 'mem_X', 'CaseII', 'CaseIII', 'nII', 'nIII', 'exists_coef'],
  DT+'ConductorAtMapInjectiveCoeff.lean': ['chHom_ord', 'chHom_comp', 'map_injective_coeff_twist_comm', 'chHom_chiP', 'conductor_at_map_injective_coeff', 'chHom_ker', 'parity_at_map_injective_coeff', 'chHom_even', 'enough_of_le'],
 },
 'SP9': {
  DT+'AfStmt.lean': ['AdmRAlt', 'NumberSp4Alt'],
  DT+'VWinNumN.lean': ['est', 'size', 'number_sp4_of_admissible_to_admissible_n'],
 },
 'SP10': {
  SG+'DecompSigmaOrd.lean': ['r0', 'Fin0', 'NoEnd', 'AllIrr', 'RigidAt', 'aVal', 'sha', 'Ineq'],
  DT+'CountS.lean': ['@exists_frob_nonvanishing_with_sha_bound'],
  SG+'GaloisRepIneqOfAllIrreducibleNonvanishing.lean': ['real_ratio_bound', 'exists_rep_family_from_points', 'covers_and_cotangent_length_bounds', '@galoisRep_ineq_of_allIrreducible_nonvanishing'],
  SG+'ValProd.lean': ['vlen_le', '@shaEq'], SG+'TwoPowClogLe.lean': ['@arith'],
  HV+'HostComp.lean': ['@hostComp'], HV+'OrdProjNDvd.lean': ['@hostTh1'],
  HV+'CmDatumCharTwoAdicOrderBounds.lean': ['@cmDatum_char_two_adic_order_bounds'], HV+'PZeroLe.lean': ['@pZeroLe'],
  HV+'Counts.lean': ['CountShape', 'CountII', 'CountIII'],
  DT+'ConductorAtMapInjectiveCoeff.lean': ['main_big', '@sp4Main_alt'],
 },
}
titles = {
 'SP1': 'Literal LemmaM-prime with an additive injection and finite residue field',
 'SP2': 'Complete multigraded Euler positivity, monotonicity and scalar-product engine',
 'SP3': 'Rees support and admissibility, including both one-sided point constructions',
 'SP4': 'Finite two-sided orbit cover and generic graded multiplicity at most one',
 'SP5': 'Leading-form lattice count and the exact lower Euler factor',
 'SP6': 'Literal LemmaM with all primes, all two-sided covers and factor two',
 'SP7': 'Actual normalized Selmer cocycles and mPrime for the actual Model',
 'SP8': 'Original-character invariants and exact normalized coefficient return',
 'SP9': 'Uniform integral trace product from the precisely stated finite catalogue',
 'SP10': 'Complete original-character paired-count join with explicit remaining geometric inputs',
}
deps = {'SP1': [], 'SP2': [], 'SP3': [], 'SP4': [], 'SP5': ['SP2', 'SP3'],
        'SP6': ['SP2', 'SP3', 'SP4', 'SP5'], 'SP7': ['SP1', 'RV3'],
        'SP8': ['RV1'], 'SP9': [], 'SP10': ['SP6', 'SP7', 'SP8', 'SP9', 'RV3']}
scopes = {
 'SP1': "All hypotheses of literal LemmaM': arbitrary abelian grading, O DVR with finite residue field, nonzero c, additive injective D with O-valued weighted derivation lifts killing the equations modulo c. Gives length M<=cotLen, including infinite cotLen case.",
 'SP2': 'Finite multigraded modules over standard finitely generated multigraded Noetherian algebra over local B. Exact admissibility power containment. Eventual Euler positivity/monotonicity and scalar-product lower bound proved by homogeneous prime filtration and kernel-cokernel exact sequences.',
 'SP3': 'Exact LemmaM objects and M1-M3; every relevant homogeneous quotient has finite O graded pieces eventually, generic support lies at restrictions of two-sided points; with M5 the actual section list plus a is admissible. Symmetric J_epsilon construction uses a nonzero finite-type field algebra.',
 'SP4': 'M2 and M4 on exact scheme: finite covers consist only of two-sided points. Slice f=1 has zero tangent, hence finite etale. Explicit z^2=f cover gives reduced localized algebra and each localized weight piece length<=1. Squared F/E equations cost exactly 2^(r+1+r-prime).',
 'SP5': 'M1 with r>=1 and the actual Smith-normalized F. Weight-zero variables eliminated by a proved recursive formal substitution; leading coefficient lattices free of rank H(d); generating-function difference equals 2^(r-1+r-prime). Lower Euler bound is 2^(r+r-prime) cotLen.',
 'SP6': 'Every quantifier of literal LemmaM: exact IsCO/IsWRing/IsChart/Eqns/M1-M5/IsNVal, all two-sided finite covers, finite cotangent length and factor2 bound. Generic length formula is proved directly by determinant and field norm. No finite-residue assumption added to LemmaM.',
 'SP7': 'Original D:Raw Omega c with Good and actual Model D. Constructs literal ShaCoc from RV3; normalizes uniquely at g0, kills all actual finite local parameters, proves UnrT, and uses Model.gen to make reduced derivative choices additive. Supplies actual mPrime cotangent bound without supplying Model existence.',
 'SP8': 'Injective compatible finite coefficient DVR extensions on original Omega and character. Preserves order, unit kernel, conductor, primary projections, case II/III and all n parameters; RV1 supplies normalized length equality and finiteness equivalence. Adjoin required 2-power roots individually without changing prior uniform constants.',
 'SP9': 'Conditional on exact catalogue with constants fixed before e,M,p and catalogue fixed before ell,Omega,iota. Proves literal NumberSp4Alt with C=c*2^(A*+1), A=A*+1, including nonzero NN chosen before ell and all representation families, exact arithmetic Frobenius convention and product bound.',
 'SP10': 'Conditional on G1 actual data/admissible-class production, G2 actual Model/M1-M4/trace-point-orbit comparison, and SP9 catalogue. Derives exact D.Ineq, shaEq inequality, uniform polynomial absorption and coefficient return to literal CountII and CountIII. Does not claim any retained actual-data interface.',
}
inputs = {
 'SP-C1': {'kind': 'matched classical commutative-algebra leaf', 'name': 'DVR/PID module structure and Smith bases',
  'statement_used': 'Finite torsion-free modules over a DVR are free; finite modules decompose into free and cyclic torsion parts; full-rank submodules admit Smith bases and determinant gives their index.',
  'source': 'Keith Conrad, Modules over a PID, Corollary2.6, Theorem4.1, Section4 aligned bases and Theorem5.22.',
  'url': 'https://kconrad.math.uconn.edu/blurbs/linmultialg/modulesoverPID.pdf',
  'matching': 'Applied only to finite O modules whose finiteness is proved in the chapter. SP1 handles additive, not assumed O-linear, injections through finite cardinality. SP6 proves the norm-weighted length formula from these finite module facts.'},
 'SP-C2': {'kind': 'matched classical commutative-algebra leaf', 'name': 'Noetherian prime filtration',
  'statement_used': 'A finite module over a Noetherian ring has a finite filtration with quotients R/p; the graded refinement is obtained by choosing homogeneous annihilators.',
  'source': 'Stacks Project, Lemma10.62.1, tag00L0.', 'url': 'https://stacks.math.columbia.edu/tag/00L0',
  'matching': 'SP2 explains the homogeneous refinement and proves the specific Euler nonnegativity argument; no positivity theorem is left as an unexplained citation.'},
 'SP-C3': {'kind': 'matched classical commutative-algebra leaves', 'name': 'Nullstellensatz, Nakayama and finite etale algebras over a field',
  'statement_used': 'Maximal residue fields of finite-type algebras over algebraically closed K equal K; radical ideals are intersections of maximal ideals. For a finite local module M=mM implies M=0. Finite etale field algebras are finite products of finite separable extensions.',
  'source': 'Stacks Project tags00FV (Theorem10.34.1),00DV (Lemma10.20.1),00U3 (Lemma10.143.4).',
  'urls': ['https://stacks.math.columbia.edu/tag/00FV', 'https://stacks.math.columbia.edu/tag/00DV', 'https://stacks.math.columbia.edu/tag/00U3'],
  'matching': 'SP3 base changes the nonzero finite-type algebra ((A/J_epsilon) tensor_B Frac(B/p))[1/q], never an arbitrary transcendental residue field. SP4 uses zero cotangent at all closed points and characteristic zero to prove the finite-etale slice, then gives an explicit double cover.'},
 'SP-C4': {'kind': 'matched classical number-theory leaf', 'name': 'Bertrand prime theorem',
  'statement_used': 'For n>1 there is a prime n<p<2n.',
  'source': 'P.Erdos, Beweis eines Satzes von Tschebyschef, ActaSciMath(Szeged)5(1932),194-198.',
  'url': 'https://users.renyi.hu/~p_erdos/1932-01.pdf',
  'matching': 'Applied at n=ell*h.N*p1+5; yields source pZero<=2ell*h.N*p1+10, with p>=5, p not dividing level or D.S.'},
 'SP-C5': {'kind': 'matched elementary local and cyclotomic number theory', 'name': 'Unramified Frobenius and cyclotomic value',
  'statement_used': 'At a finite rational prime p the decomposition group modulo inertia is procyclic, generated by arithmetic Frobenius; roots of unity of order prime to p are unramified and Frobenius acts by the p-th power.',
  'source': 'J.S.Milne, AlgebraicNumberTheory,v3.08(2020), Chapters6 and8 (cyclotomic extensions, decomposition/inertia and Frobenius); original-place transport also established in KB6.',
  'url': 'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
  'matching': 'SP7 retains all original valuation subrings in UnrT; SP10 uses arithmetic Frobenius chi(Fr)=p, and computes H1_unr(E/O(theta)) directly as (E/O)/(theta(Fr)-1)(E/O), hence zero for finite character times a strictly negative twist.'},
 'SP-R1': {'kind': 'retained bespoke supplier', 'name': 'G1 actual Raw/Good/OfCase and exact admissible class',
  'statement_used': 'The complete G1 assertion in main.tex, including original Omega, conductor/case, parameters n-prime,p1,m0, level L, common finite order k, D.S, one common iota and actual AdmRAlt for every irreducible EPt.',
  'source_inputs': ['BR7 supplies CorX', 'SymplecticFourImageDense remains open'],
  'unproved_internal_edges': ['dataEx', 'levOf', 'level', 'safe4-prime', 'same common iota for all irreducible points']},
 'SP-R2': {'kind': 'retained bespoke supplier', 'name': 'G2 actual weighted Model and geometric comparisons',
  'statement_used': 'The complete G2 assertion: existence of actual Model D, M1-M4 on its first-weight-zero algebra, every two-sided point assigned an actual irreducible EPt, exact trace element and isomorphic-representation implies same orbit.',
  'source_inputs': ['CohomologyHyp', 'Literal LemmaP, supplied separately by the FP component when its reconstruction is reviewed', 'SymplecticFourImageDense', 'RigiditySymplecticFour', 'RV3/RV7 supply SoFin/SoV'],
  'unproved_internal_edges': ['phiGam', 'nums', 'locBase', 'exModel', 'aW/aSmooth/m1b/m2/m3/m4', 'ptLift/ptScale/twoIrr', 'conjTorus/ptAct/ptExt']},
 'SP-R3': {'kind': 'retained bespoke supplier', 'name': 'Exact uniform finite automorphic trace catalogue',
  'statement_used': 'All three catalogue clauses preceding SP9, with size constants uniform in e,M,p and catalogue before ell,Omega,iota and family; integrality, Aut(C) permutation, precise trace bound, classification injectivity and original-place Frobenius match.',
  'source_inputs': ['Hypotheses-prime', 'LevelPNAlt', 'AdmResNAlt', 'literal AdmRAlt-to-AdmRNAlt comparison'],
  'not_substituted': ['Generic automorphy', 'HypothesesH-prime without field-by-field proof', 'An ell-dependent trace set']},
}
uses = {'SP1':['SP-C1'], 'SP2':['SP-C2'], 'SP3':['SP-C3'], 'SP4':['SP-C3'],
        'SP5':['SP-C1'], 'SP6':['SP-C1'], 'SP7':['SP-C5'], 'SP8':[],
        'SP9':['SP-R3'], 'SP10':['SP-C4','SP-C5','SP-R1','SP-R2','SP-R3']}
frontier_spec = {
 'SymplecticFourImageDense': {DT+'IsAut4.lean':['SymplecticFourImageDense'], DT+'Sp4In.lean':['sp4In_alt'], DT+'Sp4In0.lean':['sp4In0_alt']},
 'CohomologyHyp': {SG+'EntryMem.lean':['CohomologyHyp']},
 'LemmaP': {CA+'FramedTwoCoboundaries.lean':['LemmaP'], CA+'LemmaP.lean':['@lemmaP']},
 'NumberSp4Alt': {DT+'AfStmt.lean':['NumberSp4Alt'], DT+'AutomorphicFormHyp.lean':["Hypotheses'"], DT+'VWLevel.lean':['numberSp4_n_alt'], DT+'FrobeniusTraceCountBoundOfCmEigensystemCount.lean':['CountQAlt','countQ_alt'], 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/WinDefs.lean':['EigData','EigData.Classifies']},
 'RigiditySymplecticFour': {DT+'RigEnd3.lean':['RigiditySymplecticFour'], DT+'RigSp4.lean':['@rigSp4_alt']},
 'G1 actual data, level and admissible class': {AV+'AutomorphicCases/SymplecticGSp4.lean':['OfChar','OfCase'], SG+'DataEx.lean':['@dataEx'], SG+'DirGPowOne.lean':['@levOf'], SG+'LevBasis.lean':['@level'], AV+'ModularityArgument/AutomorphyLifting/AdmissibleLevelRestriction/UnlAllOf.lean':["safe4'"]},
 'G2 actual model and comparisons': {SG+'ExModel.lean':['@exModel'], SG+'WeightAlgebraGeneratedDegreeTwo.lean':['@aW'], SG+'ASmooth.lean':['@aSmooth'], SG+'QuotientSaturatedSquareTorsionFree.lean':['@m1b'], SG+'FgMapMk.lean':['@m2'], SG+'TorusConjugateCornerEntryEq.lean':['@m3'], SG+'ExistsLiftOfDerivationOnIdeal.lean':['@m4'], SG+'PtLift.lean':['@ptLift'], SG+'PtScale.lean':['@ptScale'], SG+'TwoIrr.lean':['@twoIrr'], SG+'ConjTorus.lean':['@conjTorus'], SG+'PtActInternal.lean':['@ptAct'], SG+'PtExt.lean':['@ptExt'], SG+'GaloisRepIneqOfAllIrreducibleNonvanishing.lean':['same_orbit_of_conjugate_reps','exists_rep_family_from_points','covers_and_cotangent_length_bounds']},
}

tex = (HERE/'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    start = next(i for i,line in enumerate(lines,1) if re.match(rb'\\begin\{(?:lemma|proposition|theorem)\}\['+cid.encode()+rb':',line))
    end = next(i for i,line in enumerate(lines,1) if i>start and line.startswith(b'\\end{proof}'))
    retained = [i for i in uses[cid] if inputs[i]['kind']=='retained bespoke supplier']
    claims.append({'id':cid, 'title':titles[cid], 'statement':scopes[cid],
      'introduced_in':'0.26', 'depends_on':deps[cid], 'input_ids':uses[cid],
      'status': 'Complete conditional human proof; displayed bespoke inputs retained' if retained else 'Complete human proof in exact quantified scope, with listed classical leaves',
      'mathematical_status':'conditional endpoint' if retained else 'closed in its exact stated scope',
      'remaining_bespoke_inputs':retained,
      'proof_location':{'file':'symplectic_count_closure/main.tex','paragraph':cid,'line_start':start,'line_end':end,'label':'claim:'+cid,'sha256':sha(b''.join(lines[start-1:end]))},
      'sources':[source(p,n) for p,names in spec[cid].items() for n in names],
      'source_relation':'Consolidated human reconstruction with proved simplifications; a source locator does not mark unexpanded source suppliers as human-proved.',
      'component_ledger':'symplectic_count_closure/provenance.json'})
frontier = [{'name':name,'status':('universal algebraic implication handled by separate FP component; actual application remains G2' if name=='LemmaP' else 'retained bespoke supplier or actual-data comparison'),
             'sources':[source(p,n,'Retained supplier or internal comparison, not certified by this chapter') for p,names in entries.items() for n in names]}
            for name,entries in frontier_spec.items()]
for p,record in files.items():
    blob=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+p])
    if sha(blob)!=record['sha256']:
        raise ValueError('Pinned Git blob mismatch: '+p)
supplier_paths={'RV1':'rank_one_cohomology/main.tex','RV3':'rank_one_cohomology/main.tex','RV7':'rank_one_cohomology/main.tex','BR7':'bernoulli_residual_vanishing/main.tex'}
suppliers=[{'claim':cid,'file':p,'current_file_sha256':sha((HERE.parent/p).read_bytes()),
            'binding':'stable endpoint; RV1/RV3 are direct proof inputs, RV7/BR7 are available top-interface retirements'} for cid,p in supplier_paths.items()]
result={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.26','date':'2026-11-22',
 'repository':URL,'commit':PIN,'component':'symplectic_count_closure',
 'scope':'Complete literal LemmaM and LemmaM-prime, actual-model shaCoc/mPrime, exact coefficient return, integral finite catalogue arithmetic and an explicitly conditional CountII/III join. The actual model/catalogue/automorphy/cohomology/rigidity supplier frontier remains visible.',
 'claims':claims,'source_files':list(files.values()),'dependency_graph':deps,'input_ledger':inputs,
 'human_suppliers':suppliers,'retained_frontier':frontier,
 'validation':{'source_files_checked_against_pinned_git_blobs':len(files),
   'claim_source_links':sum(len(c['sources']) for c in claims),
   'frontier_source_links':sum(len(f['sources']) for f in frontier),
   'main_tex_sha256':sha(tex),'verification_kind':'Exact source and proof bytes plus independent human mathematical review; no kernel replay'}}
(HERE/'provenance.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
(HERE/'classical_inputs.json').write_text(json.dumps({'schema':'rh-classical-input-registry/1','component':'symplectic_count_closure','artifact_version':'0.26','inputs':{k:v for k,v in inputs.items() if k.startswith('SP-C')}},indent=2,ensure_ascii=False)+'\n')
(HERE/'remaining_inputs.json').write_text(json.dumps({'schema':'rh-retained-supplier-registry/1','component':'symplectic_count_closure','inputs':{k:v for k,v in inputs.items() if k.startswith('SP-R')},'source_frontier':frontier},indent=2,ensure_ascii=False)+'\n')
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nfile '+s['sha256']+'\nrange '+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
closure={'schema':'rh-dependency-closure/1','artifact_version':'0.26','component':'symplectic_count_closure',
 'commit':PIN,'main_tex_sha256':sha(tex),'graph':deps,
 'closed_endpoints':[{'claim':'SP1','literal_interface':"UpperTheory.V.Alg.LemmaM'",'retained_bespoke_inputs':[]},
   {'claim':'SP6','literal_interface':'UpperTheory.V.Alg.LemmaM','retained_bespoke_inputs':[]},
   {'claim':'SP7','literal_interface':'shaCoc and mPrime on original Good D and actual Model D','retained_bespoke_inputs':[],
    'scope_note':'Model is universally quantified in this implication; its existence on actual D remains G2.'},
   {'claim':'SP8','literal_interface':'Character invariants and normalized coefficient return','retained_bespoke_inputs':[]}],
 'conditional_endpoints':[{'claim':'SP9','literal_interface':'NumberSp4Alt','retained_bespoke_inputs':['SP-R3']},
   {'claim':'SP10','literal_interface':'CountII and CountIII','retained_bespoke_inputs':['SP-R1','SP-R2','SP-R3']}],
 'same_object_bindings':['Original algebraic closure Omega and all valuation subrings','Original Raw/Good/OfCase, no simplified residual representation','Actual Model presentation and first-weight-zero algebra','Only two-sided points in every Covers set','Original Dirichlet unit kernel, order, conductor and case','Arithmetic Frobenius and trace of r0','v_O(ell) normalization, exact factor2','One catalogue and integer before ell and the representation family','Uniform exponent before host, coefficient extension and character'],
 'noncircularity':['M/M-prime use only the displayed algebraic data and standard commutative algebra, no RH/GRH or arithmetic counting input.',
   'SP3 uses M3 and rational spanning; SP4 uses M2/M4. Neither assumes the desired length bound.',
   'SP5 proves lower Euler count independently of SP4 multiplicity; SP6 joins the two and derives factor2.',
   'SP7 uses previously proved RV3 finiteness, never CountII/III.',
   'SP9 proves integral arithmetic packaging while retaining catalogue existence.',
   'SP10 explicitly retains actual-model realization and comparison, and does not infer them merely from the source sp4Main_alt declaration.'],
 'simplifications':['Symmetric ideal J_epsilon produces both one-sided points with one support argument.',
   'The z^2=f double cover of a finite-etale slice gives reducedness and generic graded multiplicity one.',
   'The Herbrand length sum is derived by determinant and field norms rather than a separate associativity package.',
   'Normalized cocycle at g0 makes actual Selmer lifts canonical; universality makes derivative choices additive.',
   'A larger explicit polynomial exponent simplifies the exact original-character arithmetic absorption.'],
 'not_claimed':['Unconditional CountII or CountIII','Construction of the actual model from LemmaP/CohomologyHyp','Uniform catalogue existence or automorphy/rigidity packages','Full PointHV or RH/GRH','Lean kernel replay']}
(HERE/'closure.json').write_text(json.dumps(closure,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result['validation'],indent=2))
