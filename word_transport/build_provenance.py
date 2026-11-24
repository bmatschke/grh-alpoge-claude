"""Rebuild exact source provenance for the v0.6 operator-word reconstruction.

Reads the pinned checkout and hashes exact inclusive declaration ranges.
Does not run Lean, modify source, or assert a kernel replay.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path('/workspace/scratch/b992d67d27b8/alpoge-rh')
OUT = Path('/workspace/scratch/b992d67d27b8/v0_6/word_transport')
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == COMMIT
files = {}


def namespace_at(lines, first):
    stack = []
    for line in lines[:first-1]:
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s|$)', line)
        end = re.match(r'^end(?:\s|$)', line)
        if ns:
            stack.append(('namespace', ns.group(1)))
        elif sec:
            stack.append(('section', ''))
        elif end:
            assert stack, ('unmatched end', first, line)
            stack.pop()
    ns = '.'.join(name for kind, name in stack if kind == 'namespace')
    return ns+'.' if ns else ''


def reference(path, name, role='proof'):
    data = (ROOT/path).read_bytes()
    if path not in files:
        pinned = subprocess.check_output(['git', 'show', COMMIT+':'+path], cwd=ROOT)
        assert data == pinned, ('source differs from pinned blob', path)
    lines = data.decode().splitlines(keepends=True)
    pat = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev)\s+'
                     +re.escape(name)+r'(?=[\s{(:])')
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits) == 1, (path, name, hits)
    first = hits[0]+1
    top = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance)\b')
    last = next((i for i in range(first, len(lines)) if top.match(lines[i])), len(lines))
    while last > first and not lines[last-1].strip():
        last -= 1
    sha = hashlib.sha256(data).hexdigest()
    files[path] = dict(path=path, sha256=sha, line_count=len(lines), pinned_blob_verified=True,
                       url=f'{REPO}/blob/{COMMIT}/{path}')
    declaration = name.removeprefix('_root_.') if name.startswith('_root_.') else namespace_at(lines, first)+name
    return dict(path=path, declaration=declaration, line_start=first, line_end=last,
                role=role, sha256=sha,
                excerpt_sha256=hashlib.sha256(''.join(lines[first-1:last]).encode()).hexdigest(),
                url=f'{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}')


def gb(file, name, role='proof'):
    return reference(GB+file+'.lean', name, role)


def pc(file, name, role='proof'):
    return gb('PlaneCoefficients/'+file, name, role)


def tw(file, name, role='proof'):
    return gb('TwistedSubstitution/'+file, name, role)


claims = []


def claim(cid, title, statement, status, sources, assumptions=(), dependencies=(), sections=(), note=''):
    assert status in {'faithful_translation', 'derived_simplification', 'remaining_input'}
    claims.append(dict(id=cid, title=title, statement=statement, status=status,
                       sources=sources, assumptions=list(assumptions), depends_on=list(dependencies),
                       proof_location=dict(file='word_transport_section.tex', anchors=[cid]),
                       expanded_notes=dict(file='report.txt', sections=list(sections)), source_relation=note))


claim('WT1', 'Actual selected letters, prefix-touch geometry and universal membership',
      'The true letters L_j plus current frame represent TT bijectively modulo n. If a true letter belongs to NSet(j,u+1), or is carried from the previous frame, its selected physical residue touches the weak prefix x<=x_(j,u). This covers every affected plane chain/link and the adjacent normal prefixes. The definitions of levImg, thStar and MemAtG retain all residue, degree-block and joint-projector quantifiers; their inequality form allows arbitrary positive link thresholds below the budget.',
      'faithful_translation', [
          gb('SegRing', 'Frames', 'definition'), gb('SegRing', 'letters', 'definition'),
          gb('SegRing', 'LLset', 'definition'), gb('SegRing', 'Valid', 'hypothesis'),
          tw('PlaneCoeff', 'posU', 'definition'), tw('PlaneCoeff', 'posTL', 'definition'),
          tw('PlaneCoeff', 'lowP', 'definition'), tw('PlaneCoeff', 'NSet', 'definition'),
          tw('PlaneCoeff', 'InLow', 'definition'), tw('PlaneCoeff', 'InBlock', 'definition'),
          tw('PlaneCoeff', 'levImg', 'definition'), tw('PlaneCoeff', 'thStar', 'definition'),
          tw('PlaneCoeff', 'slU', 'definition'), tw('MemLin', 'MemAtG', 'interface'),
          tw('MemAtDZeroIff', 'MemAtLe', 'interface'), pc('UpdDModelLet', 'MemLev', 'interface'),
          pc('UpdDModelLet', 'XXg', 'definition'), pc('UpdDModelLet', 'Base', 'hypothesis'),
          pc('UpdDModelLet', 'ThLe', 'definition'), pc('UpdDModelLet', 'memAtLe_iff'),
          gb('DiagonalSupport/SlackBoundReal', 'posTL_inj'),
          gb('DiagonalSupport/PosTLSurj', 'posTL_surj'),
          pc('GeoTouch', 'geoTop'), pc('GeoTouch', 'geoTouch'),
          tw('WordLossNonneg', 'touchT', 'definition'), pc('UpdDModelLet', 'cost1', 'definition')],
      assumptions=['Fr.Valid with its period, ordered even frame positions and no selected positions in frame gaps.',
                   'J=Fr.J, nL_j=#Fr.LLset(j), and the signed/digit/prefix geometry specified by Base.',
                   'r,K>=1, n>=1, and a characteristic-zero coefficient field for the later normal decomposition.'],
      sections=[1],
      note='The report proves the residue bijection by partitioning a length-n half-open interval and proves the touch cases directly. It does not assume injectivity on the overlapping full window W_j. Variables outside TT may be specialized to1; no unspoken support condition is needed.')

claim('WT2', 'Signed conjugated-torus calculus for all needed first-order operators',
      'For a letter in a prefix, vector multiplication/derivative have minimum-order losses0/1 and maximum-order increases1/0; covectors have the reversed costs. Coordinate Euler has cost1 for either sign and either order. A letter outside the prefix has cost0. The proof is the exact chain rule for A(t)=g diag(t) g^(-1), whose entries use exponents0,1 and whose inverse uses0,-1.',
      'derived_simplification', [
          gb('ObjPol', 'twistMat', 'definition'), gb('ObjPol', 'twistSub', 'definition'),
          gb('ObjPol', 'valS', 'definition'), gb('ObjPol', 'lam1S', 'definition'),
          gb('RootWeights/TwistSubEqMatrixSubst', 'twistSub_eq_matrixSubst'),
          tw('TwistedMonomialFiltration/SumCCMulSumOfMulEqOne', 'flt_op_valS', 'general_source_proof'),
          tw('TwistedMonomialFiltration/SumCCMulSumOfMulEqOne', 'flt_op_lam1S', 'general_source_proof'),
          tw('TwistedMonomialFiltration/MaxTwistDegreePderivLeAddOne', 'valS_X_mul_of'),
          tw('TwistedMonomialFiltration/MaxTwistDegreePderivLeAddOne', 'valS_pderiv_of'),
          tw('TwistedMonomialFiltration/MaxTwistDegreePderivLeAddOne', 'maxTwistDegree_X_mul_le_of'),
          tw('TwistedMonomialFiltration/MaxTwistDegreePderivLeAddOne', 'maxTwistDegree_pderiv_le_of'),
          gb('MonomialSupport/Lam1SPderivAndXMulLeAddIndicator', 'lam1S_pderiv_and_X_mul_le_add_indicator')],
      assumptions=['Polynomial signed vector/covector substitution, with the generic matrix inverted in its coordinate ring.'],
      dependencies=['WT1'], sections=[2],
      note='The source proves a more general divided-Taylor filtration theorem. The report gives a shorter complete chain-rule proof of exactly its first-order consequences needed here. Euler costs one because one signed factor costs zero.')

claim('WT3', 'Exact residue/carry identities before and after the frame digit split',
      'For q>=1, L_rho(partial H)=((rho+1)Id+q y partial_y)L_(rho+1)H for rho<q-1, and q partial_y L_0 H for rho=q-1. Also L_rho(XH)=L_(rho-1)H for rho>0 and y L_(q-1)H for rho=0. After block selection carry terms use input degree d+1 or d-1; multiplication into output degree0 vanishes. These identities apply both to levImg and to Fdig; an extra Fdig Euler term occurs only at a vector frame letter.',
      'faithful_translation', [
          pc('DoubleMonomialApply', 'der_A_pl'), pc('DoubleMonomialApply', 'der_A_no'),
          pc('DoubleMonomialApply', 'der_B_pl'), pc('DoubleMonomialApply', 'der_B_no'),
          pc('DoubleMonomialApply', 'mul_A'), pc('DoubleMonomialApply', 'mul_Bpl'),
          pc('DoubleMonomialApply', 'mul_Bno'), pc('DoubleMonomialApply', 'mul_Bpl_zero'),
          pc('DoubleMonomialApply', 'mul_Bno_zero'),
          pc('DoubleMonomialApply', '_root_.Formalism.MainNotions.PairMembershipBlocks.trDerPl'),
          pc('DoubleMonomialApply', '_root_.Formalism.MainNotions.PairMembershipBlocks.trDerNo'),
          pc('DoubleMonomialApply', '_root_.Formalism.MainNotions.PairMembershipBlocks.trMulPl'),
          pc('DoubleMonomialApply', '_root_.Formalism.MainNotions.PairMembershipBlocks.trMulNo'),
          pc('TouchCOfMem', 'Fdig_der_inl'), pc('TouchCOfMem', 'Fdig_der_lt'),
          pc('TouchCOfMem', 'Fdig_der_eq'), pc('TouchCOfMem', 'Fdig_mul_zero'),
          pc('TouchCOfMem', 'Fdig_mul_pos'), pc('TouchCOfMem', 'Fdig_der_ex'),
          pc('TouchCOfMem', 'Fdig_mul_ex'), pc('TouchCOfMem', 'modelLet_vec')],
      assumptions=['The true physical variable of the affected selected letter is unique.',
                   'All digit moduli q are positive; the identities include q=1 and invalid-residue zero cases.'],
      dependencies=['WT1'], sections=[3],
      note='A single explicit monomial calculation proves all four source transport interfaces and their second-digit counterparts. All scalar factors q and residue changes are retained. No naive commutation with Frobenius powers is assumed.')

claim('WT4', 'Plane chain and link transport with one unit of cutoff loss',
      'The XXg plane conditions are preserved by derivative, multiplication and coordinate Euler when affected input cutoffs exceed the target by one. Derivative has nonzero cost only for vector letters, multiplication only for covectors; frame-to-carry derivatives are handled by the exact digit formula. Euler therefore still has cost1. Degree0 and unaffected-prefix cases are included.',
      'faithful_translation', [
          pc('NoOpStep', 'touchC', 'definition'), pc('NoOpStep', 'ThDrop', 'interface'),
          pc('NoOpStep', 'PlDer', 'interface'), pc('NoOpStep', 'PlEul', 'interface'),
          pc('NoOpStep', 'PlMul', 'interface'),
          pc('XXgZeroP', 'touchC_of_liftVar_mem_chainML'),
          pc('XXgZeroP', 'plDer\''), pc('XXgZeroP', 'plMul\''),
          pc('XXgZeroP', 'plDer'), pc('XXgZeroP', 'plMul'), pc('XXgZeroP', 'plEul'),
          pc('PlaneCoeffMonomial', 'XXg_add'), pc('PlaneCoeffMonomial', 'XXg_smul')],
      assumptions=['The explicit homogeneous degrees and ThDrop inequalities at every chain and imposed link.'],
      dependencies=['WT1', 'WT2', 'WT3'], sections=[4],
      note='This proves the sign-sensitive plDer/plMul arguments and the Euler conclusion; it does not simply invoke PlDer/PlMul as black-box assumptions.')

claim('WT5', 'Normal joint-type band and coefficient recombination',
      'For D a coordinate derivative, multiplication or Euler, e_(kappa-prime) D e_kappa can be nonzero only if kappa-prime_(j,u),1<=kappa_(j,u),1+1_(x0 in NSet(j,u)) at every cut. A finite joint decomposition and coefficientwise linear recombination then prove the exact NoOpStep. D is not assumed to commute with the projectors.',
      'faithful_translation', [
          tw('PlaneCoeff', 'jIso', 'definition'), tw('PlaneCoeff', 'IsJProj', 'definition'),
          tw('JointEIntList', 'NSet_mono'), tw('JointEIntList', 'NSet_disj'),
          tw('JointEIntList', 'eeN_spec'), tw('JointEIntList', 'eeN_comm'),
          tw('JointEIntList', 'jointN_props'), tw('CommPresIsoSub', 'jointE_factor'),
          tw('CommPresIsoSub', 'jointE_isJProj'),
          gb('MonomialSupport/SupportSubNuSet', 'joint_dec'),
          gb('GLWeightTheory', 'valuation_field', 'source_weight_identification'),
          pc('NoOpStep', 'NoOpStep', 'interface'),
          gb('MonomialSupport/Lam1SPderivAndXMulLeAddIndicator', 'noOpStep')],
      assumptions=['Finite-dimensional rational split GL representations in characteristic zero are completely reducible and obey highest-weight dominance.',
                   'All polynomial/coefficient decompositions used at a time are finite; out-of-range natural prefix indices are extended by the output tuple.'],
      dependencies=['WT1', 'WT2'], sections=[5],
      note='Commutation of nested-prefix type projectors and the generic maximum/type identification are proved in the report from the stated field-level background. No integral-projector denominator, lattice decomposition, or new representation-theoretic assertion is retained.')

claim('WT6', 'Adjacent-prefix threshold comparison and the actual OneOpStep',
      'The max defining thStar is 1-Lipschitz in the relevant adjacent normal first weights. Their transition indicators at u+1 and u-1 are bounded by the physical touch cost at u. Hence one physical derivative or multiplication adds cost1*delta(s), and X_(s,a)partial_(s,b) adds exactly2*delta(s) to the allowed loss. Universal degree-block quantifiers justify every intermediate degree update.',
      'faithful_translation', [
          pc('WithThModelLet', 'restLeOfG'), pc('UpdDModelLet', 'memAtLe_iff'),
          pc('PlaneCoeffMonomial', 'thStar_le'), pc('PlaneCoeffMonomial', 'thLe_up'),
          pc('PlaneCoeffMonomial', 'thLe_weak'), pc('PlaneCoeffMonomial', 'thLUp_pos'),
          pc('PlaneCoeffMonomial', 'thDrop_of'), pc('PlaneCoeffMonomial', 'inN_le_cost'),
          pc('PlaneCoeffMonomial', 'thLe_ka'),
          pc('PlaneCoeffMonomial', 'oneT_pderiv'), pc('PlaneCoeffMonomial', 'oneT_X_mul'),
          pc('PlaneCoeffMonomial', 'planeCoeff_pderiv'), pc('PlaneCoeffMonomial', 'planeCoeff_X_mul'),
          pc('RestOneOpOf', 'derLev'), pc('RestOneOpOf', 'mulLev'),
          pc('RestOneOpOf', 'oneOpStep_of'), pc('RestOneOpOf', 'restOneOp_of'),
          tw('WordLossNonneg', 'OneOpStep', 'target_statement')],
      assumptions=['The exact universal MemAtLe/MemLev hypothesis, with positive requested link thresholds.',
                   'The selected operator position lies in TT; coordinate indices a,b are arbitrary.'],
      dependencies=['WT1', 'WT2', 'WT3', 'WT4', 'WT5'], sections=[6],
      note='The report proves the contents of every OpSteps component used in oneOpStep_of. Raised input link thresholds remain positive. The complete operator preserves physical multidegree, but its derivative and multiplication are handled separately with the required degree updates.')

claim('WT7', 'Per-position word loss and exact numerical absorption for C>=16',
      'The actual list condition gives0<=wordLoss<=2*#letters(j)*c0<=2*N1*c0. FramesOK implies Bo>=a/p^G-prime because oldest is a selected position in the same window. WeightHyp gives flatDeg>=a. With Q=p^G-prime and cP=cStar+r*N*c0+2*r*n*cpp, Hyps gives C*k^3*r^2*N*Q^5*cP*Y<=a and N1^2<=r*N. For C>=16 these imply a>=16*N1*c0*Y*k^2*Q and sl>=16*N1*c0, including the exact floor. Thus wordLoss<=sl/8.',
      'faithful_translation', [
          tw('WordLossNonneg', 'wordLoss', 'definition'), tw('WordLossNonneg', 'wordLoss_nonneg'),
          pc('WBound', 'sum_ite_mem'), pc('WBound', 'wordLoss_le'), pc('WBound', 'posU_mem'),
          pc('WBound', 'Bo_ge'), pc('WBound', 'size_arith'), pc('WBound', 'wordBoundStep'),
          pc('WBound', 'restWordBound'),
          gb('SegRing', 'oldest', 'definition'), gb('SourceCleaning', 'levDeg', 'definition'),
          gb('SourceCleaning', 'Bo', 'definition'), gb('SourceCleaning', 'sl', 'definition'),
          gb('SourceCleaning', 'cPrime', 'definition'),
          gb('WittFrameLocaliserOrders', 'oldest_mem_segment_letters'),
          gb('ScaleEdges/FramesOf', 'FramesOK', 'hypothesis'),
          gb('ScaleEdges/ManyEdges', 'Hyps', 'hypothesis'),
          gb('TableLineDegreeFive', 'WeightHyp', 'hypothesis'),
          gb('ScaleEdges/GainBoundAt', 'flatDeg', 'definition'),
          gb('ScaleEdges/GainBoundAt', 'flatDeg_bounds'),
          tw('WordLossNonneg', 'WordBoundStep', 'target_statement')],
      assumptions=['The actual FramesOK/Hyps/WeightHyp parameter inequalities, C>=16 and at mostc0 operators at EACH selected position.',
                   'N=#TT, k=r+K, Q=p^G-prime; the physical frame window has cardinality<=N1 and span<G-prime.'],
      dependencies=['WT1'], sections=[7],
      note='The report derives the needed slack inequality explicitly. It does not leave WordBoundStep or Bo_ge as a new input, does not misread c0 as a total word-length bound, and does not omit the floor.')

claim('WT8', 'WordConditionAt and the two linear-span extensions',
      'Inducting in the source right-fold opWord adds2*delta per entry and gives MemAtLe(0,1/8,wordLoss). Since wordLoss<=sl/8, the exact target MemAtG(1/8,3/8) follows. The same argument actually permits link loss1/4, recorded only as an unused strengthening. Linearity extends the initial per-symbol condition to its span, then the transported condition to the literal OpCl span; memAt_iff identifies it with incoming MemAt.',
      'derived_simplification', [
          gb('DualFockLinear/TestSideExplicitIdentification', 'opWord', 'definition'),
          gb('DualFockLinear/TestSideExplicitIdentification', 'OpCl', 'definition'),
          tw('WordLossNonneg', 'restWordStep_of'), tw('WordLossNonneg', 'restWord_of'),
          tw('MemAtDZeroIff', 'memAtLe_mono'), tw('MemAtDZeroIff', 'memAtG_of_le'),
          tw('MemLin', 'memAtG_add'), tw('MemLin', 'memAtG_smul'), tw('MemLin', 'memAtG_zero'),
          tw('MemLin', 'memAt_iff'), tw('MemRed', 'WordConditionAt', 'target_statement'),
          tw('MemRed', 'memAt_of_wordConditionAt')],
      assumptions=['Initial MemAtG(0,1/8) for every actual symP(B_b), or for the starting polynomial F in the pointwise word theorem.',
                   'The allowed list is supported on TT and has count<=c0 separately at every position.'],
      dependencies=['WT1', 'WT6', 'WT7'], sections=[8],
      note='The 1/4 intermediate link loss is a direct human consequence of the source loss estimate. The main theorem retains3/8 exactly and changes no downstream constant. The main implication and two span extensions faithfully match MemRed.')

claim('WT9', 'Exact application frontier and actual initial-symbol interface',
      'The word transport is complete under the exact initial Lemma5aAt and actual FramesOK/Hyps data. Companion IN9 proves initial membership through lemma5a_of_monomial and rest5aMono_of_cut with MemAtB/PlanePairsOnBlocksAt, so incoming membership is closed jointly by IN and WT; the stronger GeneratorProductsAt is not silently assumed. Existence of the global frame and numerical parameters remains separate. Outgoing MembAt is the different already reconstructed DT10 assertion.',
      'remaining_input', [
          tw('MemRed', 'Lemma5aAt', 'external_initial_interface'),
          tw('Lemma5aMonomial', 'lemma5a_of_monomial', 'actual_initial_route'),
          pc('PlaneCoeffOneTTens', 'rest5aMono_of_cut', 'actual_initial_route'),
          pc('PlanePairsOnBlocksAt', 'MemAtB', 'actual_initial_block_interface'),
          pc('PlanePairsOnBlocksAt', 'PlanePairsOnBlocksAt', 'actual_initial_block_interface'),
          gb('PlaneCoefficients', 'restMEM_of_last', 'assembly'),
          tw('Proposition5Gram', 'DataII', 'application_hypotheses'),
          tw('Proposition5Gram', 'MemStep', 'application_target'),
          tw('PlaneCoeff', 'MemAt', 'incoming_target'),
          gb('DiagonalSupport/TwiceValuationFactorialProduct', 'MembAt', 'distinct_outgoing_interface')],
      assumptions=['Initial-symbol companion IN9 proves Lemma5aAt through the pinned block-aware call path.',
                   'Actual frame and numerical parameter supply, not reconstructed by this local transport theorem.',
                   'The explicit characteristic-zero field-level representation background used in WT5.'],
      dependencies=['WT8'], sections=[0, 9],
      note='Remaining_input describes the application frontier, not an unproved OneOpStep, WordBoundStep, twisted-prefix or normal-type lemma. IN9 is a completed companion result, not an unresolved premise in combined v0.6. No full Type-II, RH or GRH proof is claimed by this fragment.')


status_definitions = {
    'faithful_translation': 'A complete human proof of the cited source statement under all explicitly stated hypotheses.',
    'derived_simplification': 'A shorter complete human proof or unused stronger consequence, with its exact relation to the source stated.',
    'remaining_input': 'A precise external application hypothesis or companion theorem; not silently counted as proved by this fragment.'}
out = dict(schema_version='1.0', artifact_version='0.6', date='2026-11-21', owner='lean_audit',
           repository=dict(url=REPO, commit=COMMIT),
           verification=dict(source_ranges_checked=True, source_hashes_recorded=True, pinned_blobs_checked=True,
                             local_lean_compilation=False, kernel_replay=False,
                             full_headline_call_path_traced=False),
           status_definitions=status_definitions, claims=claims, source_manifest='source_manifest.json',
           companion_dependencies=[
               dict(component='initial_symbols', claim='IN9', status='proved_companion',
                    statement='Actual Lemma5aAt with output MemAtG(0,1/8), retaining the block-aware initial proof route.'),
               dict(component='IP/IW/PG', statement='Previously stated characteristic-zero highest-weight background and compatible prefix-projector calculus; no new integral estimate is needed.'),
               dict(component='global_supply', statement='Existence of actual FramesOK and Hyps data; WT7 proves their required word-budget consequences.')])
(OUT/'provenance.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
(OUT/'source_manifest.json').write_text(json.dumps(dict(repository=out['repository'], files=[files[p] for p in sorted(files)]), indent=2, ensure_ascii=False)+'\n')
print(json.dumps(dict(claims=len(claims), source_files=len(files), source_references=sum(len(c['sources']) for c in claims),
                     statuses={s: sum(c['status'] == s for c in claims) for s in status_definitions})))
