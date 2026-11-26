#!/usr/bin/env python3
"""Bind the exact finite local completion to pinned source and inherited proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, required=True)
source = ap.parse_args().source.resolve()
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()
F = 'src/Formalism/'
AB = 'src/Development/AbelianVarietyTheory/'
I = AB+'Proofs/InertiaEigenvalues/'
FM = AB+'Proofs/FlagMeasures/'
GI = AB+'Proofs/GlobalInterpolation/'
P = F+'PadicSubsetSums/'
ROW = F+'SharpRestriction/LevelLetterCocycles/ArithmeticCylinders.lean'
LD = AB+'Definitions/NonGaloisDescent/LabelDatum.lean'
DEFS = P+'CentralIdempotents/EigenbasisOfDistinctRoots.lean'

# These are source contract/proof locators, not substitutes for the human proofs.
specs = {
 'collision_contract': [
  (P+'CentralIdempotents/GaloisIrreducibility.lean',14,16,'BB: original exceptional primes'),
  (P+'CentralIdempotents/GaloisIrreducibility.lean',51,77,'primeToPart; exact GoodAt root conditions'),
  (DEFS,291,319,'sqWeight; sqSet; original weighted divisor bound'),
  (DEFS,338,375,'PrimeFactorsLogTwo; SameFactorCount; CrossFactorCount; SeriesBounds; LocalEstimateII')],
 'root_fibers': [
  (P+'StableGradedCounts/CoeffZeroNeZeroOfIrreducible.lean',15,139,'Frobenius orbit, root-order, disjoint-root counting and polynomial root bound'),
  (P+'StableGradedCounts/CrossFactorCount.lean',11,48,'root_conj and card_samePart_le')],
 'same_factor': [
  (P+'StableGradedCounts/CoeffZeroNeZeroOfIrreducible.lean',141,None,'lpow_le_rpow_quarter and same_factor_count: original endpoint')],
 'cross_factor': [
  (P+'StableGradedCounts/CrossFactorCount.lean',51,None,'cross_factor_count: original endpoint')],
 'collision_union': [
  (P+'StableGradedCounts/SquareSetMemExceptionalUnion.lean',7,349,'divisor weights, finite bad-factor sets and square_set_mem_exceptional_union'),
  (P+'StableGradedCounts/SquareSetMemExceptionalUnion.lean',429,None,'local_estimate_second: original quantitative endpoint')],
 'finite_characters': [
  (LD,15,79,'IsClass; IsChar; IsIrr; ip; tr; zOf; hc/hcL; IsCusp; wh; der; gg; eJ prime'),
  (ROW,298,354,'literal eDat/eU/phiJ/eJ and the four admLq clauses')],
 'gelfand_mirabolic': [
  (AB+'Definitions/SemilocalFrames/IsMirClass.lean',1,None,'actual mirabolic and intermediate pattern definitions'),
  (I+'GelfandGraevCharacterGLnNormAndReciprocity.lean',47,None,'ip_gg; wh_gg; gg_norm'),
  (I+'MirabolicTraceGeWhittakerDimensionGLn.lean',112,None,'mirabolic_comparison: exact original factor')],
 'root_exchange': [
  (FM+'IsotypicTraceEqOfOneDoubleCoset.lean',11,None,'finite class-function exchange by character cancellation'),
  (FM+'PhIUnionTrans.lean',184,None,'exact pattern-union group and adjacent exchange'),
  (FM+'TrFirstPattern.lean',12,None,'front coordinate permutation; tr_first_pattern'),
  (FM+'SumGraphEqSumEntN.lean',52,None,'final phI/eeI pattern equals original eJ'),
  (I+'GroupAlgebraTracePatternIdempotentExchange.lean',13,None,'tr_eJ_eq_tr_eJ prime: original endpoint')],
 'lower_weight': [
  (I+'HarishChandraSeriesWeightLowerComparison.lean',13,None,'coefficient identity; nonnegativity; full lowerWtComparison')],
 'cuspidal_support': [
  (I+'WhittakerDimensionCuspidalGreenDegreeEqOne.lean',48,None,'cuspidal derivatives and wh_cusp_eq_one'),
  (I+'CharacterPairingHarishChandraCuspidalMackey.lean',259,None,'ip_hcL_cusp: exact matching-permutation formula'),
  (I+'HarishChandraSeriesLabelExistsUniqueGLn.lean',129,269,'label uniqueness, existence and squarefree singleton support'),
  (I+'WhittakerDimensionHarishChandraInductionMul.lean',65,None,'wh_hcT: exact finite Harish--Chandra product formula')],
 'green_label': [
  (LD,81,118,'original LabelDatum/thetaOf/IsCuspOf/HasLabel/eSerC/wtC/Green/ESerTie'),
  (AB+'PublishedTheorems/GaloisCohomology₂/GreenRegularCharacters.lean',10,None,'modern regular-character theorem contract, not used as an unproved source theorem'),
  (I+'CuspidalCharacterLabelUniqueGLn.lean',28,115,'finite Fourier support comparison'),
  (I+'CuspidalCharacterLabelUniqueGLn.lean',161,None,'thetaOf and full isCuspOf_label_unique endpoint'),
  (I+'HarishChandraSeriesWeightSquarefreeLabelGelfandG.lean',238,None,'full squarefree_label_unipotent and squarefree_label_gelfandGraev')],
 'normalized_bridge': [
  (I+'LemmaLSeriesWeightsOfGreenCuspidalParametrisatio.lean',15,30,'original type primes are at least five; literal rank split'),
  (P+'CentralIdempotents/GaloisConjCentralIdempotent.lean',25,68,'LabelMap fields and original HasLabelO'),
  (F+'LocalToGlobal/NormalizedHeckeFactors/GlobalDatumRegularityOfTypesCompatibility.lean',63,90,'actual supplied NormalizedTypesCompatibility: teichC, generator, O and eSer_def'),
  (GI+'AdmissibleLabelWeightsOfGreenCuspidalParametrisa.lean',26,104,'finite prime-label sets; exists_perm_deg; exists_perm'),
  (GI+'AdmissibleLabelWeightsOfGreenCuspidalParametrisa.lean',107,251,'factor extension; HasLabelO comparison; eSer_eq'),
  (GI+'AdmissibleLabelWeightsOfGreenCuspidalParametrisa.lean',254,None,'admissible_label_weights: original normalized-law installation')],
 'literal_consumer': [
  (ROW,235,275,'wtOf; original AllRows; LabelCountGoodInjective'),
  (ROW,355,361,'goodAt; locShare'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',17,25,'TieVecW; RangeW'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',168,219,'host_facts: exact arithmetic guards'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',238,None,'locShare_le_Wg and weightAllRows_of; fourth admLq clause explicitly discarded'),
  (F+'LocalToGlobal/HilbertRowConditions/AllJoin.lean',14,24,'LevelSharp; AllJoinA'),
  (F+'LocalToGlobal/HilbertRowConditions/AllJoinP.lean',18,25,'tieVecW_of_join; weight_of_join'),
  (F+'LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',56,78,'unchanged Wg and SizesAt'),
  (F+'LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',180,199,'original CountAllRows/WeightAllRows definitions'),
  (F+'LocalRingCardinality/Params.lean',6,34,'actual rank record f=2ord<=k<=r'),
  (GI+'LinkIRROfJoinEx.lean',41,140,'selected family size choice x^2<=f and exact rank growth')]
}
inventory, records, excerpts = {}, {}, []
for group, entries in specs.items():
    records[group] = []
    for i,(path,start,end,decl) in enumerate(entries,1):
        b=(source/path).read_bytes()
        assert b == subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}']), path
        lines=b.splitlines(keepends=True)
        end = len(lines) if end is None else end
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        block=b''.join(lines[start-1:end])
        rec=dict(id=f'FLC_{group}_{i:02}',path=path,declaration=decl,line_start=start,line_end=end,
            file_sha256=sha(b),range_sha256=sha(block),range_bytes=len(block),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        records[group].append(rec)
        inventory[path]=dict(path=path,sha256=sha(b),bytes=len(b),line_count=len(lines),
            verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nSHA256 {rec["range_sha256"]}\n{block.decode()}\n')

titles = {
 1:'Frobenius orbits and exact prime-to-part root-fiber bound',
 2:'Full original SameFactorCount',
 3:'Full original CrossFactorCount with fixed Frobenius fiber',
 4:'Weighted union of same-factor and cross-factor root collisions',
 5:'Full original LocalEstimateII with constant 23 and all degrees',
 6:'Finite averaging, reciprocity and Mackey decomposition',
 7:'Exact Gelfand--Graev norm by Bruhat compositions',
 8:'Mirabolic induction and exact Whittaker comparison',
 9:'Finite class-function exchange by cancellation',
 10:'Literal original root-pattern exchange from eJ to eJ prime',
 11:'Full original lowerWtComparison on the original projectors',
 12:'Cuspidal degree and Whittaker multiplicity identity',
 13:'Full cuspidal Mackey formula and unique support',
 14:'Whittaker multiplicativity in finite Harish--Chandra induction',
 15:'Uniqueness of the literal prime label from elliptic values',
 16:'Exact application of published Green theorem to original Green record',
 17:'Full squarefree series weight law with exact eU normalization',
 18:'Original normalized-label permutation and projector equality',
 19:'Actual selected eventual WeightAllRows with unchanged Wg'
}
deps = {
 1:[], 2:[1], 3:[1], 4:[1,2,3,'RRT5'], 5:[4], 6:[], 7:[6], 8:[6,7],
 9:[], 10:[9,'RRT1'], 11:[8,10,'RRT1','RRT3'], 12:[11], 13:[6], 14:[6],
 15:[1], 16:[15],
 17:[12,13,14,15,16,'RRT1','RRT3'],
 18:[6,11,13,15,16,17],
 19:[5,11,18,'RRT1','RRT2','RRT4','RRT6','RRT8','RRT9','RRT10','RRT11','RRT16']
}
scopes = {
 1:(['root_fibers','collision_contract'],['Every finite field, algebraically closed extension, n>=1, and every prime ell, including the characteristic.']),
 2:(['collision_contract','same_factor'],['Every d>=2 and ell^(4v_ell(q^d-1))<=q^d; exact original count, without large-q restriction.']),
 3:(['collision_contract','root_fibers','cross_factor'],['Every d>=1, any fixed irreducible with nonzero constant, same exact ell-power guard. No degree(P prime) factor.']),
 4:(['collision_contract','collision_union'],['Original squarefree weight and exceptional primes. Repeated-factor and overdegree pair events are omitted before invoking RRT5.']),
 5:(['collision_contract','collision_union'],['Every finite field q>=2^12, every algebraically closed extension and every N>=0. Constant unchanged at 23.']),
 6:(['finite_characters'],['Finite groups and finite-dimensional complex representations.']),
 7:(['finite_characters','gelfand_mirabolic'],['Prime q, n>=1, original nontrivial additive character.']),
 8:(['finite_characters','gelfand_mirabolic'],['Prime q and actual finite mirabolic groups; all finite-dimensional modules.']),
 9:(['root_exchange'],['Exact equal-order subgroup and character-cancellation hypotheses printed in FLC9.']),
 10:(['finite_characters','root_exchange','gelfand_mirabolic'],['N=k+2s+1, k>=1, s>=0, literal original phiJ, phI and eeI; original nontrivial additive character.']),
 11:(['finite_characters','gelfand_mirabolic','lower_weight'],['Same rank and character scope; every actual central series projector, including the original eSerC. No Green theorem needed.']),
 12:(['finite_characters','cuspidal_support'],['Every finite-dimensional complex cuspidal representation, d>=1, original nontrivial additive character.']),
 13:(['finite_characters','cuspidal_support'],['Actual finite block parabolics and cuspidal irreducibles of positive ranks; rank-zero empty support retained.']),
 14:(['finite_characters','cuspidal_support'],['Any finite-dimensional inducing representations and every parenthesization of original hcL.']),
 15:(['green_label'],['Prime q>=5, original LabelDatum and literal IsCuspOf elliptic values; no Green classification used in uniqueness.']),
 16:(['green_label'],['Every prime q, d>=1, original Teichmuller map and original norm-compatible generators. Published classification is explicitly retained; not reproved.']),
 17:(['finite_characters','green_label','cuspidal_support'],['Prime q>=5, every squarefree valid degree-N label, including N=0. Published input enters only via FLC16.']),
 18:(['green_label','normalized_bridge'],['Original supplied NormalizedTypesCompatibility T, its specified jE, original label map/generators/eSer_def. No construction of T from abstract projectors.']),
 19:(['literal_consumer','normalized_bridge'],['Original D, supplied T, actual AllRows A with AllJoinA, TieAdmG and RangeW; N>=absolute N0 of RRT9-RRT10. Actual selected family f<=k<=r=N and x^2<=f absorb that guard eventually.'])
}
tex=(HERE/'main.tex').read_bytes()
t=tex.decode()
claims=[]
for n,title in titles.items():
    cid='FLC'+str(n)
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',t,re.S)
    assert match,cid
    block=match.group().encode()
    groups,hyp=scopes[n]
    claims.append(dict(id=cid,title=title,introduced_in='0.43',
        classification='A' if n==16 else 'B',
        status='complete human proof or exact published application at printed scope',
        depends_on=['FLC'+str(x) if isinstance(x,int) else x for x in deps[n]],
        published_input_ids=['FLC_GREEN_CLASSIFICATION'] if n==16 else [],
        hypotheses_retained=hyp,source_groups=groups,sources=[r for g in groups for r in records[g]],
        proof_location=dict(file='finite_local_completion_v43/main.tex',label='claim:'+cid,
            line_start=t[:match.start()].count('\n')+1,line_end=t[:match.end()].count('\n'),
            sha256=sha(block),bytes=len(block)),
        scope_note='Source identifies the original contract; the displayed argument is the proof. No Lean replay or formal-proof recertification.'))

published=[dict(id='FLC_GREEN_CLASSIFICATION',classification='A',kind='matched_published_input',
    author='J. A. Green',title='The characters of the finite general linear groups',
    publication='Transactions of the American Mathematical Society 80 (1955), 402-447',
    doi='10.1090/S0002-9947-1955-0072878-2',
    url='https://www.ams.org/tran/1955-080-02/S0002-9947-1955-0072878-2/S0002-9947-1955-0072878-2.pdf',
    locators=['Definition 3.1 and equation (12), p.417','Theorem 9, pp.429-430',
        'Section 7 Schur-function homomorphism, pp.436-437','Lemma 7.4, p.438',
        'Degree-d simplexes and Theorem 12, p.439','Theorem 13, pp.439-440'],
    retrieval_date='2026-11-23',retrieval_status='AMS indexed full text retrieved through web tool; direct PDF download returns 403; no local PDF claimed',
    statement_used='Regular multiplicative-character Frobenius orbits parametrize cuspidal irreducibles, with degree product_{a=1}^{d-1}(q^a-1) and elliptic value (-1)^(d-1) sum_i theta(y^(q^i)).',
    exact_dictionary_location='main.tex, paragraph immediately before FLC16, equation FLC.23',
    dictionary=['theta=theta0^a corresponds to the degree-d simplex {a,aq,...,aq^(d-1)} modulo q^d-1',
        'The corresponding primary symbol is (g^(1))=(-1)^(d-1)I_d^a[(1)]',
        'Section 7 multiplication and Theorem 13 identify exactly these symbols with cuspidals via finite reciprocity',
        'T_(d,1)(a;y) and Lemma 7.4 give the exact elliptic sum and positive degree',
        'FLC16 identifies original thetaOf for every given LabelDatum and all original generators'],
    not_claimed=['a new proof of Green classification','replacement of original normalized labels by unrelated labels','source theorem invocation as a substitute for human matching'])]

inherited=[]
rt=ROOT/'retained_rows_v42/main.tex'
rb=rt.read_bytes(); rs=rb.decode()
rrt_ids=sorted({d for ds in deps.values() for d in ds if isinstance(d,str) and d.startswith('RRT')},key=lambda x:int(x[3:]))
for cid in rrt_ids:
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'(?:\n|$)',rs,re.S)
    assert match,cid
    inherited.append(dict(claim=cid,file='retained_rows_v42/main.tex',file_sha256=sha(rb),
        claim_sha256=sha(match.group().encode()),kind='immutable inherited human proof',newly_modified=False))

frontier=[
 dict(id='FLC_NORMALIZED_TYPES_PRODUCER',status='retained_original_input',
      target='Construct the actual NormalizedTypesCompatibility record in the selected global datum.',
      scope='FLC18 proves the comparison for the original supplied record, not its producer.',sources=records['normalized_bridge']),
 dict(id='FLC_ADELIC_ROWS',status='remaining_global_input',
      target='Original HidaSetting, actual reduction/Haar normalization EtOne, RowsAdd, RowsGood, AutTie and common AllRows object.',
      scope='Finite RRT12/RRT13 and present local laws do not produce these adelic/spectral inputs.',sources=records['literal_consumer']),
 dict(id='FLC_CYLINDER_COUNTS',status='remaining_global_input',
      target='Three sufficient actual arithmetic cylinder counts in GQT5, with one tuple-independent threshold.',
      scope='WeightAllRows is produced locally; CountAllRows and LabelCountGoodInjective are distinct remaining producers.',sources=records['literal_consumer']),
 dict(id='FLC_UNUSED_UPPER_ADMLQ',status='not_claimed_not_needed_by_this_consumer',
      target='Fourth full admLq upper eJ comparison.',
      scope='Original locShare_le_Wg discards this fourth clause. FLC19 proves the three consumed clauses without invoking it.',sources=records['finite_characters'][-1:]+records['literal_consumer'][4:5]),
 dict(id='FLC_SMALL_RANK_LONG_PRIME',status='not_claimed_not_needed_by_selected_eventual_family',
      target='Original LocalEstimateV uniformly for every N>=100.',
      scope='RRT10 gives the original constant for all N>=N0; actual f<=k<=r and x^2<=f make this sufficient eventually.',sources=records['literal_consumer'][-2:])
]
completed=['SameFactorCount','CrossFactorCount','LocalEstimateII','gg_norm',
    'tr_eJ_eq_tr_eJ_prime','mirabolic_comparison','lowerWtComparison','wh_cusp_eq_one',
    'ip_hcL_cusp','wh_hcT','isCuspOf_label_unique','Green (exact published application)',
    'squarefree_label_gelfandGraev','degree-preserving normalized eSer projector comparison']
contract=dict(schema='rh-finite-local-completion-contracts/1',artifact_version='0.43',component=HERE.name,
    source_commit=PIN,proof_file_sha256=sha(tex),original_parent_contract='GLOBAL_RETAINED_DEFECT',
    original_parent_status='open_C',completed_original_substatements=completed,
    conditional_endpoint='Original WeightAllRows on the actual AllRows A, from T, AllJoinA, TieAdmG, RangeW and N>=N0; selected original family satisfies the extra guard eventually.',
    constants_unchanged=['23 log(q)/sqrt(q)','1-1/q lower local factor','squarefree product inverse weight','all five Wg coefficients and original constant 5 in eventual long-prime term'],
    labels='Every root/collision/goodAt predicate remains on the original polynomial label. The normalized-label permutation is used only for the factor-degree-dependent character identity.',
    remaining_frontier=frontier,published_inputs=published,whole_obligation_closures=[])
provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.43',date='2026-11-23',component=HERE.name,
    source_commit=PIN,main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,
    source_groups=records,source_inventory=list(inventory.values()),source_files=list(inventory),
    published_applications=published,inherited_human_inputs=inherited,
    downstream_consumer=dict(file='global_quantitative_v42/main.tex',claims=['GQT1','GQT2','GQT3','GQT4','GQT5'],
        file_sha256=sha((ROOT/'global_quantitative_v42/main.tex').read_bytes()),role='retained-defect consumer, not used to prove finite local laws'),
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
        claim_blocks=len(claims),whole_original_leaf_closures=0),
    scope_note='Actual finite inputs and exact selected eventual WeightAllRows. Global counting/row producers remain open; no RH/GRH completion, no Lean replay.')
reviews=[]
for p in sorted(HERE.glob('review_*.json')):
    reviews.append(dict(file=f'{HERE.name}/{p.name}',sha256=sha(p.read_bytes())))
root_review=ROOT/'reviews_v0_43/finite_local_completion_v43_root_review.json'
if root_review.is_file():
    reviews.append(dict(file=str(root_review.relative_to(ROOT)),sha256=sha(root_review.read_bytes())))
provenance['independent_reviews']=reviews
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.43',component=HERE.name,
    proof_file_sha256=sha(tex),new_claims=['FLC'+str(n) for n in titles],new_claim_count=len(claims),
    completed_original_substatements=completed,
    completed_conditional_endpoint=contract['conditional_endpoint'],
    old_finite_frontier_discharged=['RRT_CHARACTER_SQUAREFREE','RRT_CHARACTER_LOWER','RRT_LOCAL_ESTIMATE_II'],
    whole_obligation_closures=[],remaining_global_contract_ids=['GLOBAL_RETAINED_DEFECT'],
    published_application='FLC_GREEN_CLASSIFICATION explicitly matched; not newly proved',
    unused_upper_comparison_not_claimed=True,small_rank_long_prime_not_claimed=True,
    original_normalized_type_record_retained=True,no_lean_replay=True,
    warning='Closing these nested finite inputs does not close the original global C obligation.')
outputs={'provenance.json':provenance,'contracts.json':contract,'closure.json':closure,
    'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,source_commit=PIN,
        source_files=list(inventory.values()),ranges=records,verified_against_git=True),
    'published_inputs.json':published}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,artifact_version='0.43',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,records.values())),
    main_tex_sha256=sha(tex),whole_original_leaf_closures=0),indent=2))
