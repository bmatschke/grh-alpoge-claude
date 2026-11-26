#!/usr/bin/env python3
"""Reproduce the TX source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
I = D + 'Proofs/IwasawaDecomposition/'
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]

def whole_decls(path, role='substantive_local_proof_and_definitions'):
    """Link each declaration separately; never hash a reconstructed source."""
    _, _, decls = read_source(path)
    return [source(path, d['qualified'], role) for d in decls]

common = [
    'The arithmetic host, CMData, ranks, coefficient fields/embeddings, and original pi with pi*conjugate(pi)=p are supplied.',
    'The true column datum I with literal Ok, Pins and Later is supplied. Laws may be taken from independent TL13; Law0 is constructed in TX10.',
    'The selected twist primes have no conjugate pair, avoid type/auxiliary primes, and pi is a unit there. The actual valuation, residue, character and coordinate conventions are retained.',
    'No separate realizability, all-twist chart, common-character, chain, terminal vector, moving-element or period-comparison existence premise is used.',
    'The endpoint TX16 retains precisely NChoice, TupTied and tp.xi=I.xi. These arithmetic data are not required by the geometry through TX15.',
    'No Lean compilation, kernel replay, proof of supplied arithmetic/analytic inputs, RH or GRH is asserted.'
]

def claim(i,title,statement,deps,srcs,relation,assumptions=()):
    return dict(id=i,title=title,status='derived_simplification',statement=statement,
        depends_on=deps,assumptions=common+list(assumptions),
        proof_location=dict(file='main.tex',anchors=[i]),
        expanded_notes=dict(file='report.txt',section=i),
        source_relation=relation,
        mathematical_status='proved_under_exact_declared_supplied_data_hypotheses',
        sources=srcs)

top=I+'ChartLastStepTwistBasePoint.lean'
chains=I+'TrueColumnChoiceTwistedChainsFormsClasses.lean'
claims=[
 claim('TX1','Completed rational level and character',
  'Construct qbU/qbChr, prove normality, exact rational intersection, character well-definedness/restriction, openness and finite exponent.',
  [],
  ss(C+'TwQGrp.lean','qbInt qbDiv qbK qbK_conj')+
  ss(C+'TwQLevU.lean','qbU qbK_princ qbU_rat qbChr_wd qbChr qbChr_rat'),
  'Explicit integral matrix factorization and congruence-discrepancy argument; does not assume a completed-level dictionary.'),
 claim('TX2','Prescribed top depth and paired-prime diagonal',
  'Use dTop=qOf(P)^(topDep+1), prove its principal-depth/character properties, and construct t in K1 with D_pi at Q and inverse conjugate transpose at conjugate Q.',
  ['TX1','AD4','FC1'],
  ss(top,'dTop')+
  whole_decls(I+'LastStepTwistLevelContainsPrincipalCongruence.lean')+
  ss(I+'ExistsUnitaryAdelicTwistDiagonalAtPrimes.lean','dEnt dAut exists_tw')+
  ss(A+'CongruenceLevelEqDepthSucc.lean','levCong extTop chr_extTop'),
  'Direct paired local components replace an opaque adelic existence step; the precise exponent is unchanged.'),
 claim('TX3','Exact framed level and inverse-character dictionary',
  'Prove topU membership iff the actual auxiliary/frame move exists, and chi0*topChi equals its embedded character, with the inverse of the product evaluated at theta^{-1}.',
  ['TX1','TX2','TG12'],
  ss(I+'NeZeroTop.lean','locLev locChr rhoP rhoT topU topChi')+
  whole_decls(I+'MemFramedLevelIffTwoAdelicPoints.lean')+
  whole_decls(I+'LevelFrameCharacterMulMovedPoint.lean')+
  ss(top,'lev_top chr_top'),
  'Uses exact rational frame discrepancy A^{-1}Aprime and integral inverses; keeps same-matrix off-Q character equality.'),
 claim('TX4','Actual framed chart and double-coset surjectivity',
  'Construct chart representatives yc=gc*(kt)^{-1}, prove rational-frame density supplies every double coset, and identify actual integral lattices and stabilizers.',
  ['TX1','TX2','TX3','DR3','AD4','LP1'],
  ss(I+'ExistsFramedChartFromAdelicDictionary.lean','rhoP_mem_qbK topU_dense exists_clsG_top'),
  'DR3 supplies valid-point realizers, while a separate rational approximation/splicing argument proves the converse double-quotient coverage.'),
 claim('TX5','Actual variable-twist terminal chart and base point',
  'Prove reads_top/root_top/top_base/chart_twm, including finite character exponent and the full IsExt-to-IsPtOf clause with point frame diag(A,pi).',
  ['TX2','TX3','TX4','TG5','TG6'],
  ss(top,'reads_top root_top top_base chart_twm')+
  ss(I+'PointOverXHasAdelicPointBlockExtendMul.lean','pt_tilF_gen')+
  ss(A+'FixedVectorEqOfStandardData.lean','ReadsTop ReadsTop.mem_chi ReadsTop.topBase'),
  'Checks all actual frames and lattice/functional domains; acting diag(gamma,1) is distinguished from point-frame diag(A,pi).'),
 claim('TX6','Middle charts with coupling stabilizers',
  'Construct finite middle chart fibres from actual index, auxiliary vector and twist cosets; complete their stabilizer cuts and preserve every reading under FunKilled normalization.',
  ['TX1','TX4','TX7','DR3','FC2','FC3','FC4','FC9'],
  ss(I+'ExistsFiniteOrderChartsMiddleSteps.lean','thetaOpen_cutQ thetaOpen_levQ lvQ_open chartQ_exists chart_of exists_charts')+
  ss(C+'FiniteSumNonzeroLargeDepth.lean','LevI locLat ybSet')+
  ss(C+'TwQThetaOpen.lean','ThetaOpen')+
  ss(I+'CouplingCosetTwistPrimeEmptyOrCoset.lean','cqOf_empty_or_coset')+
  ss(I+'LevelAtTwistPrimesIsOpen.lean','thetaOpen_levQ')+
  ss(chains,'TwStep swap_ex killK twStep_mk reads_lb_eq twStep_mid'),
  'The conditional admissible companion used here is supplied independently by TX7 from raw point/index data, with no reverse TX7 dependency.'),
 claim('TX7','Actual middle reference comparison off twist primes',
  'Match the auxiliary groups/characters and actual penultimate coupling residues, lift the conjugators locally, and prove literal Uloc and character equality away from Q.',
  ['CI7','CI13','CI14','FC1','FC2','AD4'],
  ss(I+'ExistsConjReferenceChartIndex.lean','pi_conj cosetOne idx_nonempty idx_match')+
  ss(I+'ExistsReferenceClassMatchingCouplingCoset.lean','coset_match')+
  ss(I+'MatchTupleChartMemberChart.lean','match_idx')+
  whole_decls(I+'ChartsTupleTrivQ.lean'),
  'Uses the independently reconstructed finite-sum double-coset statements, plus an explicit reference point with equal auxiliary coupling residues.'),
 claim('TX8','Common penultimate character from unique rational values',
  'Prove NearSet is a group, rational witness values are independent modulo the actual positive D(P), valV is multiplicative, and valV^{-1} restricts to every chart character; prove finite local indices.',
  ['TX6','TX7'],
  whole_decls(I+'NearPair.lean')+
  ss(I+'ExistsMidLevOfMem.lean','nearSet_closed')+
  ss(I+'CongAtOfNearSame.lean','congAt_of_near_same val_eq_of_congE nearPair_val_unique')+
  ss(I+'MidLevMulBeforeLast.lean','chiInv_last_eq_char midLev_mul_beforeLast valV_factor valV_mul')+
  ss(chains,'twBefore_cl_nonempty')+
  ss(I+'PenultimateChartLocalGroupMemNearLevelSet.lean','mem_nearSet_chart')+
  ss(I+'FurtherPlacePenultimateChartCharacterInverseValu.lean','chi_embU_mul_valV')+
  ss(I+'ExistsCharacterAllChartsFurtherPlaces.lean','exists_locChi exists_chi_further')+
  whole_decls(I+'FurtherPlacesGroupContainsChartLevels.lean')+
  ss(I+'ChartLocalGroupFiniteIndexAtFurtherPlace.lean','finiteIndex_of_princ'),
  'Does not assume that individual characters extend to a generated group; constructs a common ambient character and verifies every restriction.'),
 claim('TX9','Common level with finite auxiliary/twist coupling carrier',
  'Construct J by local joins at Q, chiJ by off-Q reference character times local inverse values, and the finite union J/H_beta with injective auxiliary/twist coordinate pair.',
  ['TX8','TX7','FC12','TG2','TG12'],
  ss(I+'ExistsLevJCosetsOfFurther.lean','exists_levJ_cosets_of_further')+
  ss(I+'ExistsLevelJCharacterEqMemberOffPlaces.lean','twLevJ_chi_off_of_lb')+
  ss(chains,'TwPack twBefore_cl_nonempty twPack_ex twJS')+
  whole_decls(HF+'TiedTwJSym.lean'),
  'Explicit common character and stabilizer carrier replace a bare record-existence assertion; label retained in the second coordinate.'),
 claim('TX10','Integral zero-step comparison and Law0',
  'Construct the frame-forgetting orbit bijection, identify the same canonical preferred decoration, and obtain a rational linear equivalence preserving the actual integral Delta lattice and embeddings.',
  ['TL13','CV7'],
  ss(I+'StepZeroClassesBijectiveSameDeco.lean','canon orb_iff bij0 stepZero_representative_deco_eq_canonical stepZero_corresponding_representatives_same_deco stepZero_classes_bijective_same_deco')+
  whole_decls(I+'FormsEquiv.lean')+
  whole_decls(I+'StepZeroFormsIdentificationReferenceTupleEqSelf.lean')+
  ss(A+'LatAtLattice.lean','Law0'),
  'Closes Law0 from literal Ok/laws without Later; proves both integral inclusions, not only equal rank or rational dimension.'),
 claim('TX11','Actual all-twist chains, values and standardness',
  'Construct TwChTied, TwChJointS, TwFormsTiedS, TwChMu0, StdW and symmetric joint forms on the actual class/latAt/identity frame data; derive the with-points endpoint.',
  ['TX5','TX6','TX7','TX9','TX10','TG12','CV9','FC7','FC18'],
  ss(chains,'twStep_top twT twJ idY_twYS twW twJS tw_chains tw_chains_std')+
  ss(I+'DecoStabTrivial.lean','deco_stab_trivial dilT_eCls0 mem_Fi_of_free twAtT_exists')+
  ss(I+'TrueColumnChoiceExistsChainDataWithBasePoints.lean','tw_ties_with_points')+
  ss(HF+'TiedTwSym.lean','TwFormsTiedS')+
  ss(A+'StdLvPr.lean','StdW'),
  'Chooses terminal data before collecting steps, and retains them throughout the later row/period join.'),
 claim('TX12','Twisted level data and zero/reference sameness',
  'Construct actual quotient projections, functionals, up/down/diamond transports and B_w compatibility, with literal StdLv and full TwLvSameS including fallback branches.',
  ['TX10','TX11','FC5','FC6','FC17','NB7','NB8','DR3'],
  whole_decls(I+'TupleChainsLevelStructureCompatibleAtLevelPrime.lean')+
  ss(I+'LvSameZero.lean','bwA lvSame_zero')+
  ss(HF+'TiedTwSym.lean','SymmetricTwistedLevelData TwLvSameS')+
  ss(A+'StdLvPr.lean','StdLv'),
  'Uses the same local kernels and moving elements; verifies equality of transports as well as equality of classes and integral localized lattices.'),
 claim('TX13','Actual all-twist row chart',
  'Construct ReadsP and ClassesAtPrimes with k=t=1 and exact row scalar d(P)=qOf(P), finite character, standard base lattice and reference equality off Q.',
  ['TX1','TX4','DR3','TG3'],
  ss(I+'TuplePrimedSpaceClassesLevelAndComparison.lean','memberLevel_read tuplePrimedSpace_classes')+
  ss(A+'LatAtLattice.lean','ReadsP'),
  'Reuses the rational-frame chart argument with the first power of qOf(P); its positive additive valuation lies inside the depth-one residue kernel.'),
 claim('TX14','Row complex/rational/integral values, norms and period',
  'Construct ValuationAtPrimes, NormPTieG and the conjugate-linear period map from actual row charts, with the exact constant weight shift and finite stabilizer-weighted Fock pairing.',
  ['TX13','CV10','CV7','FC7','FC8'],
  whole_decls(I+'FormsXTupleChainOfLevelReading.lean')+
  whole_decls(I+'TupleIntegralFormsRowPlaceByPlace.lean')+
  whole_decls(I+'TupleChainFormsRationalIffFrameValues.lean')+
  ss(I+'TupleChainComplexFormsEqAlgebraicModularForms.lean','ptC_tw')+
  ss(I+'CevInjective.lean','cev_injective jM mt_law jM_injective jM_mem jM_onto period_eq period_conj'),
  'Integral Delta and determinant shift stay exact; the period map uses actual coefficient conjugation and no continuity of arbitrary field embeddings.'),
 claim('TX15','Actual all-twist terminal moving element and evaluation',
  'Construct SymmetricTwistedTiltedData with z0=pi e_last, exact lattice/dual functional, original moving gamma, ka=(yM^{-1}rat(gamma)^{-1}ext(yP))^{-1}, all-extension adelic equality and evaluation for arbitrary frame functions.',
  ['TX5','TX11','TX12','TX13','TX14','TG5','TG6','FC6'],
  ss(I+'ExtMMulVecFix.lean','exists_ka_tw til_lat_eq_tw til_fv_eq_tw til_tw')+
  ss(I+'TupleLayerCompatibilitiesOfXPrime.lean','tupleLayer_compatibility')+
  ss(HF+'TiedTwSymP.lean','SymmetricTwistedTiltedData TwPTiedS TwPAtGS TwPEvzS')+
  ss(A+'FixedVectorEqOfStandardData.lean','StdP'),
  'Keeps all three integral lattices distinct; uses bar(pi)-unit residue cancellation and the same moving element in every scalar and stabilizer clause.'),
 claim('TX16','Complete standard all-twist comparison with exact arithmetic boundary',
  'Construct the ten fields of SymmetricTwistedColumnsAtPrimes and StdTw, identifying the exceptional-prime predicate via actual ramification; close colsTwPTiedS_std under its exact NChoice/TupTied/xi interface.',
  ['TX9','TX10','TX11','TX12','TX13','TX14','TX15','TG12','TL15'],
  whole_decls(I+'TrueColumnChoiceExistsStandardChainData.lean')+
  ss(HF+'TiedTwSymAll.lean','SymmetricTwistedColumnsCompatible SymmetricTwistedColumnsAtPrimes')+
  ss(A+'FixedVectorEqOfStandardData.lean','StdTw')+
  ss(F+'UnitaryNorms/CharTied.lean','TupTied','literal_retained_arithmetic_interface')+
  ss('src/Formalism/LocalRingCardinality/DataNChoice.lean','NChoice','literal_retained_arithmetic_interface'),
  'Final same-object join after all geometric/value suppliers; does not claim NChoice or the stronger OneLevelSymmetricColumns from character readings alone.')
]

targets=[
 dict(id='TX-NEXT-1',priority=1,title='Actual normalized arithmetic NChoice producer',
  scope='Reconstruct the actual finite DVR extension/valuation embedding and Mt rational-basis plus integral-lattice comparison from supplied ReadsAt and RankTie, then trace their arithmetic suppliers. The chart construction does not supply RankTie or local normalized Mt comparison.',
  supplied_by_this_component=['TX10','TX11','TX14','TX16'],
  sources=ss(D+'Proofs/InertiaEigenvalues/ExistsTiedChoiceOfReads.lean','exists_formsIso choiceOf choiceOfPack exists_choice exists_tied_choice_of_reads','retained_actual_arithmetic_producer')+
          ss('src/Formalism/LocalRingCardinality/DataNChoice.lean','NChoice','literal_target_fields')),
 dict(id='TX-NEXT-2',priority=2,title='Same-object distinguished tuple tie',
  scope='Reconstruct tupTied_of_muIsW from the actual MuIsW and NChoice.Q=T.Q on the active set, preserving the exact chosen xi and psi. This producer fixes xi_star/star-prime, muTw, finite/tame/trivial character facts and IsPsi; TL15 alone does not establish those same-object equalities.',
  supplied_by_this_component=['TX16'],
  sources=ss(I+'TupTiedOfMuIsW.lean','tupTied_of_muIsW','retained_same_object_tuple_producer')),
 dict(id='TX-NEXT-3',priority=3,title='Strictly stronger one-level symmetric predicate',
  scope='Determine the extra hypotheses ensuring singleton earlier charts and penultimate carrier and earlier exact HXS/lamX groups. This is stronger than the completed TX16 endpoint and is not needed by it.',
  supplied_by_this_component=['TG12','TX16'],
  sources=ss(HF+'BothSym.lean','OneLevelSymmetricColumns','stronger_definition_not_claimed_constructed'))
]

main_raw=(HERE/'main.tex').read_bytes()
paragraphs={}
for i in range(1,17):
    start=main_raw.index(f'\\paragraph{{TX{i}:'.encode())
    stop=main_raw.index(f'\\paragraph{{TX{i+1}:'.encode(),start+1) if i<16 else len(main_raw)
    paragraphs[f'TX{i}']=digest(main_raw[start:stop])

closed=[
 (top,'reads_top',['TX1','TX2','TX3','TX4','TX5']),
 (top,'root_top',['TX5']),(top,'top_base',['TX5']),(top,'chart_twm',['TX1','TX2','TX3','TX4','TX5']),
 (I+'FormsEquiv.lean','law0',['TX10']),
 (chains,'tw_chains_std',['TX6','TX7','TX8','TX9','TX10','TX11']),
 (I+'TrueColumnChoiceExistsChainDataWithBasePoints.lean','tw_ties_with_points',['TX11']),
 (I+'TupleChainsLevelStructureCompatibleAtLevelPrime.lean','tw_lv_tied_and_same',['TX12']),
 (I+'TuplePrimedSpaceClassesLevelAndComparison.lean','tuplePrimedSpace_classes',['TX13']),
 (I+'FormsXTupleChainOfLevelReading.lean','forms_tw',['TX14']),
 (I+'ExtMMulVecFix.lean','til_tw',['TX15']),
 (I+'TupleLayerCompatibilitiesOfXPrime.lean','tupleLayer_compatibility',['TX13','TX14','TX15']),
 (I+'TrueColumnChoiceExistsStandardChainData.lean','colsTwPTiedS_std',['TX16'])
]
closed=[dict(path=p,declaration=source(p,n)['declaration'],closed_by=ids,
    scope='Reconstructed under exact supplied arithmetic host/Ok/Pins/Later; TX16 also retains NChoice/TupTied/xi equality.') for p,n,ids in closed]

out=dict(schema_version='1.3',artifact_version='0.16',date='2026-11-22',
 owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes with no newline or Unicode normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Complete human proof of the exact declared supplied-data assertion; sometimes uses a shorter proof than the source.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
 paragraph_sha256=paragraphs,
 prior_components_reused=['TG','TL','FC','CV','DR','AD','NB','LP'],
 same_iteration_companions=['CI'],independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Variable-twist terminal reads_top/root_top/top_base/chart_twm with exact dTop and frame diagonal',
  'Finite actual middle charts and same-matrix reference comparison away from twist primes',
  'Common penultimate character via unique rational congruence lifts and finite joint carrier',
  'Integral Law0 and zero/reference level/transport compatibility',
  'Actual all-twist chains/forms/points with StdW/StdLv',
  'Actual row chart, complex/rational/integral values, norm and conjugate period map',
  'All-twist terminal vector/lattice/functional/moving-element/stabilizer/evaluation identities',
  'Complete colsTwPTiedS_std with its original NChoice/TupTied/xi interface'],
 scope_precision=[
  'TX6 uses the companion proved independently from raw data in TX7; no circular chart assumption.',
  'TX7 uses independent CI7/CI13/CI14 for finite-sum identity-double-coset and projected conjugation.',
  'TX10 proves Law0 from Ok/laws without an all-twist or Later premise.',
  'NChoice/TupTied and tp.xi=I.xi remain supplied only for the literal TX16 interface.',
  'No Delta=dual-Weyl, rank-only integral comparison, continuity of arbitrary embeddings, or new rational SameGenus premise.',
  'OneLevelSymmetricColumns, primitive host/Ok/Pins/Later existence and RH/GRH are not asserted.'])

review_specs=[
 ('ci_reviews_tx1_5_8_9.txt','/root/global_frame',[1,2,3,4,5,8,9],'Independent terminal chart/depth/inverse and common-character/carrier review.'),
 ('ah_reviews_tx6_7.txt','/root/class_rank',[6,7],'Independent middle coupling-fibre chart and exact reference group/character comparison review.'),
 ('root_reviews_tx_10_16.txt','/root',list(range(10,17)),'Independent Law0, all-twist join, row/period and endpoint scope review.')
]
for filename,reviewer,indices,scope in review_specs:
    p=HERE.parent/'reviews_v0_16'/filename
    if not p.exists():continue
    raw=p.read_bytes();content=raw.decode()
    chosen={f'TX{i}':paragraphs[f'TX{i}'] for i in indices}
    for key,sha in chosen.items():assert sha in content,('review paragraph changed',filename,key,sha)
    out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
      review_record='../reviews_v0_16/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
      paragraph_range='Bytes from named TX paragraph through immediately before the next TX paragraph; EOF for TX16.',
      lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc += [f"{c['id']} | {c['title']} | {c['status']}",c['statement']]
    for s in c['sources']:
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
    loc += ['']
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.16',commit=PIN,targets=targets,
    closed_source_targets=closed,
    remaining_boundary='All reference and variable-twist comparison geometry reconstructed. Exact arithmetic host/Ok/Pins/Later and TX16 NChoice/TupTied/xi remain; stronger one-level geometry separate.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),
 next_targets=len(targets),target_ranges=sum(len(t['sources']) for t in targets),verified_equal_to_pinned_git_blob=True,
 independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))

