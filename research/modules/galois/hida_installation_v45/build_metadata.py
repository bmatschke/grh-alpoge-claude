#!/usr/bin/env python3
"""Bind the same-ideal Hida installation and selected two-Link support proof."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
SRC = args.source.resolve()
assert subprocess.check_output(
    ['git', '-C', str(SRC), 'rev-parse', 'HEAD'], text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()
AA = 'src/Development/AutomorphicArithmetic/'
AV = AA + 'AutomorphicVarieties/'
DC = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
WG = AV + 'WeilGroupCharacters/'
PM = AV + 'PatchingModules/'
LS = AV + 'ModularityArgument/LeviSmoothLocalization/'
FG = AA + 'Foundations/GaloisRepresentations/'

# These are the literal source contracts and their actual assembly consumers.
# They are not counted as proofs; all conclusions are proved in main.tex.
SPECS = {
 'original_inputs': [
  (DC+'LitAut.lean',12,63,'original HypothesesH prime and named literature inputs'),
  (WG+'ContinuousResP.lean',73,102,'original HidaSetting, odd coefficient prime and auxiliary place'),
  (DC+'LocPublished.lean',13,21,'full CohP and local CFT matching from original literature fields')],
 'six_fields': [
  (DC+'PointTheoremBaseObject.lean',26,41,'PointTheoremBaseObject, six HidaPropsAlt fields, ModularAlt'),
  (DC+'ArithmeticPointPurity.lean',1,None,'literal end1 alias'),
  (DC+'ArithmeticPointClassicality.lean',1,None,'literal end2 alias'),
  (FG+'AdmissibleResidues/ArithmeticPointDecomposition.lean',26,35,
   'positive decomposition and exact conditional strict cofinite norm-ratio endpoint'),
  (FG+'PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean',17,58,
   'full WitOff, conditional-continuity AutOffN and every irreducible arithmetic-point endpoint'),
  (WG+'ArithmeticPointClassicality.lean',19,38,'full original RingProps including its guarded auxiliary clause'),
  (WG+'ArithmeticPointClassicality.lean',80,80,'full Dense definition'),
  (WG+'ArithmeticPointClassicality.lean',103,107,
   'TwistOk with finite ell-power order and all original local/Good guards')],
 'hida_selection': [
  (DC+'UnitaryHeckeData.lean',59,71,'eight-field actual UnitaryHeckeData and literal IsJ'),
  (DC+'ExistsHeckeIdeal.lean',70,None,'whole all-rank exists_hecke_ideal producer and zero-module branch'),
  (DC+'HidaU.lean',12,16,'full all-rank HidaUAlt with arbitrary supplied B and Lambda'),
  (DC+'THidaU.lean',31,48,'IsCoef, exact LocPAlt matching and same-J HidaU assembly')],
 'all_levels': [
  (DC+'PaLevel.lean',24,57,'LevPtAlt, vector-separating ClassicalAlt, LevelAlt, LocPAlt and HasAutOfAlt'),
  (PM+'ThetaCoefficientMapEq.lean',163,236,
   'actual TWBase, TWRing, ordered trace relations, correction coefficient map and TWAut'),
  (PM+'TaylorWilesObstructionBound.lean',147,148,
   'HasAut: every actual TWGrp/TWPl, fixed ideal, empty parameter and n[L+:Q]')],
 'cyclotomic_and_conditional_modularity': [
  (WG+'WeilCharactersModular/ToZModOneIff.lean',24,None,
   'muL: original noMu and actual residual cyclotomic condition'),
  (DC+'CoefIsCoef.lean',12,23,
   'same-J conditional ModUAlt assembly from CohP, LocCFTAll, PfromAut and HidaUAlt'),
  (DC+'PointTheoremBaseObject.lean',39,48,
   'ModularAlt includes P1core AND P3core; full all-rank ModUAlt quantifier'),
  (PM+'TaylorWilesObstructionBound.lean',150,154,
   'entire PfromAut including P3core, retained only as HIA3 conditional antecedent'),
  (WG+'UniversalOrdinaryDeterminantRing.lean',284,301,
   'exact P1core and separate arbitrary-NiceE-chain P3core')],
 'selected_support': [
  (PM+'TaylorWilesObstructionBound.lean',16,32,
   'Norm including original N4 and all eight CohP fields'),
  (PM+'TaylorWilesObstructionBound.lean',119,148,
   'ArPl, exact B1/B2 contracts, nontrivial cyclotomic and pro-ell conditions, HasAut'),
  (PM+'PatchedSupportCompletions.lean',207,231,
   'full Raw/Choice contracts, used only at selected h=0,a=n=4,g=0'),
  (PM+'ChebotarevFamilies/PFromAutOf.lean',30,49,
   'actual normalization-choice-realization order with same given HasAut ideal'),
  (PM+'ChebotarevFamilies/PFromAutOf.lean',50,103,
   'full determinant, residual kernel, PL, coupled B1/B2 and actual point map'),
  (PM+'ChebotarevFamilies/PFromAutOf.lean',104,126,
   'Raw consumer and separate one-point versus chain support conclusions')],
 'two_place_window': [
  (AV+'ModularityArgument/AutomorphyLifting/WeakOfAtt.lean',19,30,
   'Unl1, PotUnl and full WitA with one real center before all eligible places'),
  (LS+'WinUpDown.lean',22,41,'original chars, Unl and strict WinAt normalization'),
  (LS+'WinUpDown.lean',147,164,'WinUnl and one-center-before-all-places WinOf'),
  (FG+'PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean',17,47,
   'WitOff, AutOffN, witA_of and exact glueN'),
  (FG+'PlainTorsionPairs/IrrArithPointsAutomorphicAway.lean',65,None,
   'distinct auxiliary rational primes imply distinct finite places')],
 'two_link_threshold': [
  (AV+'WeakShimuraTheory/IsAlgClosureField.lean',19,58,
   'all original Link fields and exact IsPhi determinant/character identities'),
  (DC+'LinkTwo.lean',13,51,
   'one coefficient threshold before cprime and both actual Links with same kappa'),
  (DC+'PmTwo.lean',21,51,
   'both Links on same Space, two ideals, their sum and same-kappa two-place glue'),
  (DC+'PotentialModularityTower.lean',38,66,
   'all five PotentialModularityTower fields and literal PMExAlt choice order'),
  (AV+'HeightAndVanishing/Counts.lean',60,65,
   'exact CountShape and CountII consumed through the inherited YX2 proof')]
}

inventory = {}
groups = {}
excerpts = []
for group, specs in SPECS.items():
    groups[group] = []
    for index, (path, start, end, declaration) in enumerate(specs, 1):
        data = (SRC/path).read_bytes()
        assert data == subprocess.check_output(
            ['git', '-C', str(SRC), 'show', f'{PIN}:{path}']), path
        lines = data.splitlines(keepends=True)
        end = end or len(lines)
        assert 1 <= start <= end <= len(lines), (path, start, end, len(lines))
        block = b''.join(lines[start-1:end])
        item = dict(
            id=f'HIA_{group}_{index:02}', path=path,
            line_start=start, line_end=end, declaration=declaration,
            file_sha256=sha(data), range_sha256=sha(block),
            range_bytes=len(block), source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        groups[group].append(item)
        inventory[path] = dict(path=path, sha256=sha(data), bytes=len(data),
                               line_count=len(lines),
                               verified_equal_to_pinned_git_blob=True)
        excerpts.append(
            f'[{item["id"]}] {path}:{start}-{end}\n'
            f'Range SHA256 {item["range_sha256"]}\n{block.decode()}\n')

DEPS = {
 1: ['JRP15','UPA18','HPT18','HED16','HAW19','HTS8'],
 2: ['ITA13','HLM9','HIA1','JRP1','HLM26','HTW24'],
 3: ['HIA2','JRP1'],
 4: ['HIA2','HIA3','JRP1','KX3','CIP12','CIP10','CIP11','CAP13',
     'CCH13','CCH15','CCH16','CCH17','CFO20','CFO21','JSP11','SCI13'],
 5: ['HAW6'],
 6: ['QX4','HIA2','HIA4','JSP12','QX5','KX9','KX5','QX10','YX2',
     'HIA5','HIA3']
}
GROUPS = {
 1: ['original_inputs','six_fields'],
 2: ['original_inputs','hida_selection','all_levels'],
 3: ['cyclotomic_and_conditional_modularity'],
 4: ['selected_support','cyclotomic_and_conditional_modularity'],
 5: ['two_place_window'],
 6: ['two_link_threshold','six_fields','selected_support']
}
SCOPES = {
 1: 'All six exact HidaPropsAlt fields on any supplied original IsJ, all original n>=1; pt keeps its internal ranks2-4 guards; end1 keeps its all-lengths-one strict cofinite implication; end2 retains conditional continuity; twist is finite ell-power order.',
 2: 'Full literal HidaUAlt at every original positive rank and actual B,Lambda,iota, with the same J carrying HidaPropsAlt and full HasAut; no additional coefficient extension; J=top included.',
 3: 'Unconditional noMu-to-actual-residual-cyclotomic implication, plus a separate all-rank ModUAlt implication under explicit original PfromAut. The latter is not declared proved.',
 4: 'Entire original P1core at the selected rank-four two-Link scope, on the same J. Norm/Choice/B1/B2/Raw are used only at h=0,a=n=4,Kap.g=0. Original CohP, LocCFT, N4, determinant and PL conditions remain.',
 5: 'Full original glueN for every n>=1, same supplied rho and iota, distinct excluded finite places; AutCsd0 has no continuity antecedent and a single window center precedes all eligible places.',
 6: 'Entire selected COUNT_II_SUPPORT: both actual rank-four Links, one external coefficient threshold before every later DVR/Space/B/Lambda, one same-ideal witness per Link with all six Hida fields and P1core. General P3core is not asserted.'
}
FOUNDATIONS = [
 dict(id='HIA_ORIGINAL_H_PRIME',kind='retained_original_named_hypothesis',
      source_groups=['original_inputs','hida_selection'],
      statement='Original HypothesesH prime with its named base-change, polarized attachment, local classification, period and automorphic foundations. Inherited full endpoint proofs retain their recorded scope.',
      not_reconstructed=True),
 dict(id='HIA_COHOMOLOGY',kind='retained_original_eight_field_hypothesis',
      source_groups=['original_inputs','selected_support'],
      statement='All eight original CohP fields; the local/global finiteness, duality, Euler, Greenberg-Wiles, normalized Poitou-Tate and tame-local inputs are neither weakened nor proved anew here.',
      not_reconstructed=True),
 dict(id='HIA_LOCP',kind='retained_original_local_literature',
      source_groups=['hida_selection','all_levels'],
      statement='The exact LocPAlt fields: Bernstein-Zelevinsky finite length/admissibility, geometric lemma, and the original tame-local theorem obtained from original local Tate duality. Their finite consumers are the bound full HTW endpoint.',
      not_reconstructed=True),
 dict(id='HIA_RECIPROCITY',kind='retained_original_reciprocity',
      source_groups=['original_inputs','selected_support','two_link_threshold'],
      statement='Original local/global class-field foundations and Artin conventions; KX3 and CIP12 provide the exact reconstructed local-coordinate and every-map finite consumers.',
      not_reconstructed=True),
 dict(id='HIA_GENERAL_PFROMAUT_ANTECEDENT',
      kind='explicit_unproved_antecedent_of_conditional_theorem_only',
      source_groups=['cyclotomic_and_conditional_modularity'],
      statement='Full original PfromAut, including arbitrary NiceE chains and P3core, is an explicit antecedent only of HIA3 equation HIA.8. It is not an input to HIA4 or HIA6 and is not declared completed.',
      not_reconstructed=True,used_only_in_claim='HIA3',
      not_a_foundation_for_selected_closure=True),
 dict(id='HIA_ELEMENTARY_GALOIS',kind='standard_algebraic_background',
      source_groups=['cyclotomic_and_conditional_modularity'],
      statement='Fixed-field theorem and cyclotomic action on primitive roots; their exact residual-quotient consumer is proved in HIA3.',
      not_a_new_global_producer=True)
]
EXT = {
 1:['HIA_ORIGINAL_H_PRIME'],
 2:['HIA_ORIGINAL_H_PRIME','HIA_LOCP'],
 3:['HIA_COHOMOLOGY','HIA_RECIPROCITY',
    'HIA_GENERAL_PFROMAUT_ANTECEDENT','HIA_ELEMENTARY_GALOIS'],
 4:['HIA_COHOMOLOGY','HIA_RECIPROCITY'],
 5:[],
 6:['HIA_ORIGINAL_H_PRIME','HIA_COHOMOLOGY','HIA_RECIPROCITY']
}

proof = (HERE/'main.tex').read_bytes()
text = proof.decode()
claims = []
for n in range(1,7):
    cid = f'HIA{n}'
    match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', text, re.S)
    assert match, cid
    block = match.group().encode()
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',
                      match.group(), re.S).group(1)
    named = set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b', match.group()))-{cid}
    missing = named-set(DEPS[n])
    assert not missing, (cid, 'unrecorded named proof dependencies', sorted(missing))
    assert all(not d.startswith('HIA') or int(d[3:]) < n for d in DEPS[n])
    claims.append(dict(
        id=cid,title=title,introduced_in='0.45',classification='B',
        status='complete human proof at the expressly stated original scope',
        depends_on=DEPS[n],external_input_ids=EXT[n],published_input_ids=[],
        hypotheses_retained=[SCOPES[n]],source_groups=GROUPS[n],
        sources=[item for g in GROUPS[n] for item in groups[g]],
        proof_location=dict(file=f'{HERE.name}/main.tex',label='claim:'+cid,
            line_start=text[:match.start()].count('\n')+1,
            line_end=text[:match.end()].count('\n'),
            sha256=sha(block),bytes=len(block)),
        scope_note='The numbered human proof performs the assembly; original source fixes exact contracts and choice order. No formal replay.'))

# The dependency on HIA3 for selected support uses only its independent,
# unconditional first assertion; it does not import the PfromAut antecedent.
claims[3]['dependency_scope_overrides'] = {
    'HIA3':'Only the unconditional noMu -> residual cyclotomic lemma HIA.7. The PfromAut-conditional HIA.8 is not used.'}
claims[5]['dependency_scope_overrides'] = {
    'HIA3':'Only the final boundary statement separating the general conditional implication from selected support; HIA.8 is not invoked.'}
claims[2]['conditional_conclusions'] = {
    'HIA.7':'Unconditional under original noMu and level cyclotomic identity.',
    'HIA.8':'Requires the explicitly printed general PfromAut antecedent in addition to CohP, LocCFTAll and HidaUAlt.'}

human_ids = sorted({d for deps in DEPS.values() for d in deps
                    if not d.startswith('HIA')})
inherited = []
for cid in human_ids:
    matches = []
    for path in ROOT.glob('*/main.tex'):
        data = path.read_bytes()
        t = data.decode()
        match = re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n', t, re.S)
        if match:
            matches.append((path,data,t,match))
    assert len(matches)==1,(cid,[str(m[0]) for m in matches])
    path,data,t,match = matches[0]
    inherited.append(dict(
        id=cid,file=str(path.relative_to(ROOT)),main_tex_sha256=sha(data),
        block_sha256=sha(match.group().encode()),
        line_start=t[:match.start()].count('\n')+1,
        line_end=t[:match.end()].count('\n'),
        kind='numbered_human_proof_dependency',not_an_external_foundation=True))
assert not ({d for ds in DEPS.values() for d in ds}
            & {f['id'] for f in FOUNDATIONS})

reviews = []
for path in sorted(HERE.glob('review_*.json')):
    reviews.append(dict(file=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes())))
root_review = ROOT/'reviews_v0_45/hida_installation_v45_root_review.json'
if root_review.is_file():
    reviews.append(dict(file=str(root_review.relative_to(ROOT)),
                        sha256=sha(root_review.read_bytes())))

# A component-level closure is recorded only after the parent's independent
# mathematical review matches these exact proof bytes AND the unchanged prior
# whole contract. This builder never writes a common ledger.
accepted_whole = []
acceptance = None
review_path = HERE/'review_HIA1_HIA6_root.json'
if review_path.is_file():
    review = json.loads(review_path.read_text())
    assert review['result'] == 'PASS'
    assert review['proof_sha256'] == sha(proof)
    reviewed_claims = {c['id']:c for c in review['claims_reviewed']}
    assert set(reviewed_claims) == {c['id'] for c in claims}
    for claim in claims:
        checked = reviewed_claims[claim['id']]
        assert checked['result'] == 'PASS'
        assert checked['block_sha256'] == claim['proof_location']['sha256']
    selected = review['selected_whole_contract_reviewed']
    assert selected['id'] == 'COUNT_II_SUPPORT'
    assert selected['result'] == 'PASS'
    assert selected['full_original_contract_closed_in_stated_scope'] is True
    baseline_path = ROOT/selected['baseline_graph']
    baseline = json.loads(baseline_path.read_text())
    original = next(n for n in baseline['nodes'] if n['id']=='COUNT_II_SUPPORT')
    assert sha(original['contract'].encode()) == selected['baseline_contract_sha256']
    acceptance = dict(
        review_file=str(review_path.relative_to(ROOT)),
        review_sha256=sha(review_path.read_bytes()),
        proof_sha256=sha(proof),baseline_graph=selected['baseline_graph'],
        baseline_graph_sha256=sha(baseline_path.read_bytes()),
        original_contract_sha256=selected['baseline_contract_sha256'],
        full_original_contract_closed_in_stated_scope=True,
        common_ledger_edited_by_this_builder=False)
    accepted_whole = ['COUNT_II_SUPPORT']

completed = [
 'HidaPropsAlt, all six literal fields on the same original IsJ',
 'full all-rank HidaUAlt with same-J HasAut',
 'original noMu-to-residual-cyclotomic finite consumer',
 'conditional all-rank ModUAlt implication with explicit PfromAut antecedent',
 'selected rank-four P1core on both original Link ideals',
 'full original two-excluded-place glueN with one global window center',
 'entire selected COUNT_II_SUPPORT common-threshold/same-ideal contract',
 'PMExAlt and CountII via inherited QX10 and YX2, under their unchanged background inputs'
]
field_coverage = {
 'HidaPropsAlt.ring':'HIA1 / JRP15',
 'HidaPropsAlt.dense':'HIA1 / UPA18',
 'HidaPropsAlt.pt':'HIA1 / HPT18',
 'HidaPropsAlt.end1':'HIA1 / HED16',
 'HidaPropsAlt.end2':'HIA1 / HAW19',
 'HidaPropsAlt.twist':'HIA1 / HTS8',
 'HidaUAlt.one_IsJ_before_points_and_levels':'HIA2 / ITA13 / HLM9',
 'HidaUAlt.full_HasAut_same_J':'HIA2 / HLM26 / HTW24',
 'P1core.selected_rank_four':'HIA4 / JSP11 with complete selected suppliers',
 'glueN.one_center_and_conditional_continuity':'HIA5 / HAW6',
 'COUNT_II_SUPPORT.both_links_one_external_threshold':'HIA6 / QX4 / JSP12',
 'COUNT_II_SUPPORT.every_actual_B_Lambda_same_J':'HIA2 / HIA4 / HIA6',
 'general_ModularAlt_and_ModUAlt':'HIA3 ONLY under explicit original PfromAut; not declared supplied unconditionally'
}
guards = [
 'Original H prime, all named automorphic/local/period foundations and full eight-field CohP retained',
 'Original LocCFT and every-map Artin normalization retained and supplied by their bound finite consumers',
 'Every original n>=1 in HidaUAlt; point theorem keeps its internal 2<=n<=4 guards',
 'Fixed original iota, coefficient ring, residual labels, full determinant laws and ordered characters',
 'Same IsJ and same ideal across all six fields, full HasAut and selected P1core; J=top retained',
 'Ring auxiliary clause retains exactly its V0ok guard; no added global V0ok or continuity hypothesis',
 'end1 strict cofinite all-place norm ratio only under its original all-string-lengths-one condition',
 'end2 AutCsd0 without continuity antecedent; continuity only inside its WitOff conclusion',
 'TwistOk finite ell-power order and all original Good/local guards',
 'Full LevelAlt base chosen before every auxiliary level and family; one n! exponent before all levels',
 'Both actual rank-four Links have their original common kappa,beta,t and distinct auxiliary rational primes',
 'One external coefficient threshold after fixed iota but before every later DVR/Space/B/Lambda',
 'Pointwise support extensions do not change external threshold, J, B or original point kernel',
 'Selected support h=0,a=n=4,Kap.g=0, original N4, B1 parameter4[L+:Q]+4q, coupled B2 constant0 and full PL',
 'No arbitrary-chain P3core, general PfromAut or arbitrary-Kap arithmetic bound is claimed',
 'ell=3 included; no inversion of n! or24'
]
contracts = dict(
    schema='rh-hida-installation-contracts/1',artifact_version='0.45',
    component=HERE.name,source_commit=PIN,proof_file_sha256=sha(proof),
    endpoint_claim='HIA6',all_rank_endpoint_claim='HIA2',
    conditional_general_modularity_claim='HIA3',
    completed_original_substatements=completed,
    original_field_coverage=field_coverage,exact_guards_preserved=guards,
    human_dependency_ids=human_ids,external_input_ids=[f['id'] for f in FOUNDATIONS],
    published_applications=[],selected_consumer_only=True,
    selected_consumer_scope='Selected rank-four P1/COUNT_II_SUPPORT only; HIA1,HIA2,HIA5 retain their full stated all-rank scopes.',
    conditional_hypothesis_not_used_in_selected_closure='HIA_GENERAL_PFROMAUT_ANTECEDENT',
    no_lean_replay=True,
    proposed_whole_obligation_closures=['COUNT_II_SUPPORT'],
    whole_obligation_closures=accepted_whole,
    independent_whole_contract_acceptance=acceptance,
    closure_registration='The exact proof and whole contract passed the parent independent review. Only parent integration records common-ledger changes.',
    not_claimed=['general PfromAut','unconditional all-rank ModularAlt/ModUAlt without PfromAut',
                 'arbitrary NiceE chain or P3core','arbitrary-Kap B1/B2',
                 'new proof of retained foundations','complete RH or GRH'])
prov = dict(
    schema='rh-human-component-provenance/1',artifact_version='0.45',
    date='2026-11-23',component=HERE.name,source_commit=PIN,
    main_tex_sha256=sha(proof),proof_file_sha256=sha(proof),
    claims=claims,source_groups=groups,source_inventory=list(inventory.values()),
    source_files=list(inventory),published_applications=[],
    retained_foundations=FOUNDATIONS,inherited_human_inputs=inherited,
    independent_reviews=reviews,
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,
        all_source_bytes_compared_to_pinned_git_blobs=True,
        claim_blocks=len(claims),direct_named_claim_dependencies_checked=True,
        external_foundations_separate_from_claim_DAG=True,
        proposed_whole_original_leaf_closures=['COUNT_II_SUPPORT'],
        independently_accepted_whole_original_leaf_closures=accepted_whole),
    independent_whole_contract_acceptance=acceptance,
    scope_note='Full all-rank HidaUAlt; selected rank-four P1 and both-Link support closure. General ModUAlt appears only as the exact PfromAut-conditional implication.')
closure = dict(
    schema='rh-human-component-closure/1',artifact_version='0.45',
    component=HERE.name,proof_file_sha256=sha(proof),
    new_claims=[c['id'] for c in claims],new_claim_count=len(claims),
    completed_original_substatements=completed,
    completed_planning_targets=['full original HidaUAlt',
      'all six Hida fields and same-J HasAut on both original rank-four Links',
      'entire selected COUNT_II_SUPPORT joint producer'],
    proposed_whole_obligation_closures=['COUNT_II_SUPPORT'],
    whole_obligation_closures=accepted_whole,
    independent_whole_contract_acceptance=acceptance,
    status=('Complete selected producer with independently accepted whole-contract closure.'
            if accepted_whole else
            'Human proof complete; common-ledger whole closure reserved to parent full contract review.'),
    original_ideal_and_coefficient_ring_preserved=True,top_ideal_included=True,
    full_all_rank_hida_unitary=True,general_modularity_requires_explicit_PfromAut=True,
    selected_P1_only=True,arbitrary_P3_not_claimed=True,
    both_original_links=True,one_common_external_coefficient_threshold=True,
    full_CohP_LocCFT_N4_determinant_proell_scope_preserved=True,
    conditional_continuity_and_uniform_window_preserved=True,
    ell_three_included=True,all_level_factorial_exponent_preserved=True,
    no_lean_replay=True)

outputs = {
 'provenance.json':prov,'contracts.json':contracts,'closure.json':closure,
 'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,
   source_commit=PIN,source_files=list(inventory.values()),ranges=groups,
   verified_against_git=True),
 'retained_foundations.json':FOUNDATIONS,'published_inputs.json':[]
}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 f'ONE HIDA IDEAL AND COMPLETE SELECTED COUNT-II SUPPORT — v0.45\n'
 f'Source pin: {PIN}\nMain SHA256: {sha(proof)}\n\n'
 f'{len(claims)} numbered human proofs, all classification B. '
 f'{len(inventory)} pinned source files; {sum(map(len,groups.values()))} ranges; '
 f'{len(inherited)} inherited numbered claim bindings.\n\n'
 'HIA1 installs all six original HidaPropsAlt fields on a given original IsJ. '
 'HIA2 constructs the entire all-rank HidaUAlt: one original ideal, including its zero-module branch, '
 'carries those fields and full same-J HasAut. The actual all-level base precedes every family, '
 'and the original exponent n! is uniform in the level. No coefficient extension or rank restriction is added.\n'
 'HIA3 proves the exact noMu residual-cyclotomic consumer and states/proves the original all-rank '
 'ModUAlt implication under an EXPLICIT PfromAut antecedent. That general antecedent is not supplied.\n'
 'HIA4 installs completed Norm/Choice/ArPl/coupled B1-B2/selected Raw in JSP11 on the same J. '
 'This proves the original selected rank-four P1core for every NiceI point and every prime below its kernel. '
 'CohP, LocCFT, N4, exact determinant and pro-ell hypotheses remain intact; no arbitrary NiceE chain is asserted.\n'
 'HIA5 proves full glueN with the same representation, original conditional continuity and one real center '
 'chosen before all eligible places, even when the two excluded-place centers differ.\n'
 'HIA6 supplies the literal COUNT_II_SUPPORT contract for BOTH original rank-four Links, at one common '
 'external coefficient threshold chosen before every later DVR/Space/B/Lambda. Each ring has one ideal '
 'with all six fields plus P1core; no identity of ideals in different rings is asserted. QX10/YX2 '
 'then give the already reconstructed PMExAlt-to-CountII consequence under unchanged background inputs.\n\n'
 f'Independently accepted whole-contract closures: {accepted_whole}. '
 'The acceptance binds all six proof blocks and the unchanged prior COUNT_II_SUPPORT contract. '
 'Parent integration alone records any common-ledger status change. '
 'This component edits no original source or frozen common files.\n'
 'The original base-change, attachment, local classification/period and all eight cohomological '
 'foundations retain their recorded status. External hypotheses are separate from the numbered claim DAG. '
 'In particular HIA3 PfromAut is an explicitly unproved conditional antecedent only, not an input to '
 'HIA4/HIA6. No general P3core, arbitrary-Kap bounds, or complete RH/GRH proof is claimed.\n'
 'No Lean replay was used. Every cited source byte and range is checked against the immutable pin.\n')
hashes = {p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
          if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(
    dict(component=HERE.name,artifact_version='0.45',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(
    claims=len(claims),source_files=len(inventory),
    source_ranges=sum(map(len,groups.values())),
    inherited_claims=len(inherited),main_tex_sha256=sha(proof),
    all_rank_endpoint='HIA2',selected_endpoint='HIA6',
    proposed_whole_original_leaf_closures=['COUNT_II_SUPPORT'],
    independently_accepted_whole_original_leaf_closures=accepted_whole),indent=2))
