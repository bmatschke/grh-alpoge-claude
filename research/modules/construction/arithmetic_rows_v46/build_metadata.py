#!/usr/bin/env python3
"""Bind human arithmetic-row proofs and the exact original conditional endpoints."""
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
assert subprocess.check_output(['git', '-C', str(SRC), 'rev-parse', 'HEAD'], text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
R = S + 'FlagStabilizerTensors/RootLatticeThresholds/'
H = S + 'HaarTransversals/'
A = 'src/Formalism/SharpRestriction/LevelLetterCocycles/'
C = 'src/Formalism/SharpRestriction/CuspSpanNormBounds/'
F = 'src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'

SPECS = {
 'original_setting': [
  (H+'HidaSetting.lean',179,265,'original adelic setting, fields, frame congruences, character and measure'),
  (H+'HidaSetting.lean',336,361,'original K2, chi2, volume and formal-degree conventions'),
  (C+'GlobAut.lean',213,None,'admissibility and exact RowsAut fields'),
  (S+'FlagStabilizerTensors/RowDict.lean',49,154,'reduction, GoodOp and semilinear row dictionary')],
 'reduction': [
  (R+'AllRowsRho.lean',1,None,'reduction matrices in original lifted bases'),
  (R+'AllRowsRhoX.lean',1,None,'actual simultaneous rhoX and its exact kernel'),
  (R+'AllRowsRedKer.lean',1,None,'both partner-prime congruence kernels'),
  (R+'RhoSurjPf.lean',1,None,'full original actual reduction surjectivity'),
  (R+'RowDictPf.lean',108,153,'transported prime and lattice identifications')],
 'haar_inflation': [
  (R+'AllRowsConv.lean',1,None,'finite coset convolution with original Haar volume'),
  (R+'AllRowsFin.lean',1,None,'V, exact hat transform, injectivity, convolution and egA comparison'),
  (R+'AllRowsEtAlg.lean',1,None,'finite involution, idempotence and full positive type')],
 'finite_events': [
  (S+'FlagStabilizerTensors/AllRowsOf.lean',18,79,'ES, eT, ReT, EtOne and original RowsLab'),
  (R+'AllRowsES.lean',1,None,'finite tuple event idempotents'),
  (R+'AllRowsAdd.lean',19,72,'finite event intersection and invalid-label splitting'),
  (A+'ArithmeticCylinders.lean',240,278,'AllRows and exact label count/good injection')],
 'level_shape': [
  (R+'KppFrameW.lean',33,115,'dual residue frames give full reduction bases'),
  (R+'KppFrameW.lean',242,None,'change of residue basis and entry pairing'),
  (R+'KppLoc.lean',1,None,'original level flag and pairing calculations'),
  (R+'KppLocG.lean',1,None,'all original four-block Gram pairings in both orientations'),
  (R+'KppLocS.lean',1,None,'all matrix columns and exact JPred shape'),
  (R+'KppIdx.lean',1,106,'literal indices, reversal and diagonal signs'),
  (R+'KppFwdPf.lean',1,None,'original complete forward shape and character producer'),
  (R+'AllRowsKpp.lean',15,94,'KppShape and exact J subgroup'),
  (R+'AllRowsKpp.lean',193,271,'source index-based reverse argument simplified by ARO8')],
 'level_character': [
  (R+'KppCharA.lean',77,None,'all split primes, coprime residues and CRT idempotents'),
  (R+'KppCharB.lean',1,None,'original psiK and conjugation/rational normalization'),
  (R+'KppCharN.lean',1,None,'original nontriviality endpoint; ARO9 gives full-splitting trace simplification'),
  (R+'KppCharC.lean',44,None,'full original character splitting'),
  (R+'KppLocC.lean',17,None,'actual C argument, conjugate residues and signs')],
 'etone': [
  (R+'AllRowsWt.lean',1,None,'diagonal character shift and identity coefficients'),
  (R+'AllRowsEtOne.lean',1,None,'full EtOne with exact volume and chosen characters'),
  (R+'AllRowsClosed.lean',16,41,'unconditional exact structural fields on a supplied original X'),
  (A+'ArithmeticCylinders.lean',300,341,'literal phiJ, eJ and eJk conventions')],
 'operators': [
  (R+'AllRowsRMul.lean',1,None,'regular-action facts and Fubini convolution'),
  (R+'RowsGoodRed.lean',126,None,'projection, adjoint and good kernel comparison'),
  (R+'AllRowsAdd.lean',74,195,'operator intersection, finite sums and orthogonality'),
  (R+'AllRowsAdd.lean',254,286,'finite/infinity commutation and universal operator')],
 'evaluation': [
  (H+'RowsDef.lean',19,119,'original eHom evaluation, RowsBij and RowsFinDim'),
  (H+'UnitaryHaarProducts/RowsBij.lean',170,None,'Schur product, cyclicity and exact evaluation construction'),
  (R+'AllRowsDcount.lean',1,None,'original VT identification and Dcount equality'),
  (R+'AllRowsAddFin.lean',1,None,'exact RowsFinDim and GapHyp specialization'),
  (R+'RowDictPf.lean',30,69,'actual finite-dimensionality, degree and root-discriminant transport')],
 'multiplicities': [
  (R+'AllRowsAdd.lean',197,348,'finite rank additivity on the actual intertwiner space'),
  (R+'RowsGoodRed.lean',17,125,'original VT, LabTie, RowDictTie and good-label fiber count'),
  (S+'FlagStabilizerTensors/AllRowsOf.lean',760,890,'label completion, RowsAdd, RowsGood and full RowsLab'),
  (R+'AllRowsLab.lean',1,None,'original complete RowsGood/RowsLab assembly')],
 'allrows': [
  (S+'FlagStabilizerTensors/AllRowsOf.lean',492,555,'full actual AllRows constructor and all label fields'),
  (A+'ArithmeticCylinders.lean',244,278,'all exact AllRows and LabelCountGoodInjective fields'),
  ('src/Formalism/LocalToGlobal/HilbertRowConditions/AllJoin.lean',14,24,'exact AllJoinA bundle and level fields'),
  (F+'AllRowsAtRecord.lean',23,None,'original stdChar, count comparison and full pointwise installer')],
 'partner_count': [
  (C+'BridgeCountE.lean',289,None,'literal character idempotents, RedDatum, IsCountIdem and PCount'),
  (R+'AllRowsPCount.lean',85,203,'actual two-factor reduction datum and its exact fibers'),
  (R+'AllRowsPCount.lean',300,477,'factor character idempotents and exact normalizing cardinality'),
  (R+'AllRowsPCount.lean',547,None,'arbitrary-set cylinders and full PCountTie producer'),
  (S+'FlagStabilizerTensors/AllRowsOf.lean',892,None,'original level unipotence and admissible cylinder kernel')],
 'count_parameters': [
  (C+'AdmissibleBoundsFromSource.lean',68,77,'entire original CountTheoremHypotheses'),
  (S+'FlagStabilizerTensors/AllRowsOf.lean',701,747,'SetBase, CountBase and TieCountAt'),
  (R+'AllRowsCountBase.lean',16,85,'actual parameter, splitting and gap transport'),
  (A+'JointConditionsZpowers/JCountP.lean',12,None,'original exact conditional count installer'),
  (F+'AllRowsAtRecord.lean',37,None,'all CountAllRows fields and original c<=c3 guard')],
 'family_consumer': [
  ('src/Formalism/LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',180,195,'DstarE, CountAllRows and WeightAllRows'),
  ('src/Formalism/LocalToGlobal/HilbertRowConditions/AllJoinP.lean',18,26,'same-AllRows weight consumer'),
  (F+'IrreducibilityRowOfConcreteAutomorphicData.lean',18,None,'original common-X/ties conditional family endpoint')]
}

inventory, groups, excerpts = {}, {}, []
for group, specs in SPECS.items():
    groups[group] = []
    for i, (path, start, end, declaration) in enumerate(specs, 1):
        data = (SRC/path).read_bytes()
        assert data == subprocess.check_output(['git', '-C', str(SRC), 'show', f'{PIN}:{path}'])
        lines = data.splitlines(keepends=True)
        end = end or len(lines)
        assert 1 <= start <= end <= len(lines), (path, start, end, len(lines))
        part = b''.join(lines[start-1:end])
        item = dict(id=f'ARO_{group}_{i:02}',path=path,line_start=start,line_end=end,
                    declaration=declaration,file_sha256=sha(data),range_sha256=sha(part),
                    range_bytes=len(part),source_commit=PIN,
                    verified_equal_to_pinned_git_blob=True,
                    url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        groups[group].append(item)
        inventory[path] = dict(path=path,sha256=sha(data),bytes=len(data),line_count=len(lines),
                               verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{item["id"]}] {path}:{start}-{end}\nRange SHA256 {sha(part)}\n{part.decode()}\n')

CLAIM_GROUPS = {
 1:['original_setting','reduction','level_shape'],2:['original_setting','reduction','level_shape'],
 3:['haar_inflation','reduction'],4:['finite_events','reduction','haar_inflation'],
 5:['haar_inflation'],6:['finite_events'],7:['original_setting','level_shape'],
 8:['level_shape','reduction'],9:['level_character','level_shape'],10:['level_shape','etone'],
 11:['etone'],12:['etone','haar_inflation','finite_events'],13:['haar_inflation','operators'],
 14:['original_setting','operators'],15:['operators','finite_events'],
 16:['original_setting','evaluation'],17:['evaluation','operators'],18:['evaluation'],
 19:['multiplicities','operators'],20:['multiplicities','evaluation'],21:['multiplicities','original_setting'],
 22:['multiplicities'],23:['multiplicities','allrows'],24:['allrows','original_setting'],
 25:['partner_count','original_setting'],26:['partner_count','reduction'],
 27:['count_parameters','original_setting'],28:['count_parameters','allrows'],
 29:['allrows','family_consumer','etone'],30:['family_consumer','count_parameters']
}
SCOPES = {
 1:'Exact rhoX and both one-prime kernels on the supplied original X, not a rational approximation theorem.',
 2:'Surjectivity on the actual finite adelic lattice stabilizer with original residue bases and all factors.',
 3:'Original arbitrary supplied Haar measure; positive V and every fiber/subgroup volume, no renormalization.',
 4:'Literal egA equals central inflation even with its originally chosen GoodAt witness and arbitrary event.',
 5:'Full Haar-to-finite convolution/involution comparison for supported bi-invariant functions with exact V.',
 6:'Full original event algebra on arbitrary sets; invalid labels vanish and singleton sum is finite.',
 7:'Actual original residue frame and dual in both ew orientations; no new lattice or field.',
 8:'Full KppShape membership equivalence from actual flags, using a proved direct reverse/CRT simplification.',
 9:'Actual original chi2, fixed basis signs, CRT factor characters and their nontriviality from complete splitting.',
 10:'Exact level volume, Ehat tensor product and positive original e(1).',
 11:'All nontrivial prime-field characters and all central finite algebra elements; exact character-shift calculation.',
 12:'Entire original EtOne with every finite cylinder, original Haar and any chosen nontrivial prime characters.',
 13:'Full original EtUniv, EtInt and EtAlg for every event, including zero event.',
 14:'Original quotient Hilbert representation, bounded integrable-kernel operator, exact product and adjoint.',
 15:'Literal ReT including its existential branch, full projection algebra and original infinity commutation.',
 16:'Original GapHyp; exact supplied IsDS, local unit vectors, fdegOf and infinity Haar; no HC formal-degree formula.',
 17:'Full original evaluation bijection for actual bounded intertwiners and each actual event projector.',
 18:'Original RowsFinDim is explicit retained input, specialized with original GapHyp; all actual finite multiplicities.',
 19:'Entire RowsAdd under original finite-dimensionality premise, for every set of labels.',
 20:'Original good operator, VT and Dcount; orthogonality and exact multiplicity/range equality.',
 21:'Entire RowsGood from actual RowDictTie/LabTie; conjugation remains semilinear and repeated labels allowed.',
 22:'Finite label completion preserves the original good row indices exactly, including zero dimensions.',
 23:'Entire original RowsLab with one lab/inc before every event, using original AutTie and prior row ties.',
 24:'Full actual AllRows, LabelCountGoodInjective and AllJoinA on one original X; existence of X/ties remains supplied.',
 25:'Every cylinder is IsAdmIdem at original level g and complementary prime, including zero projector.',
 26:'Full original IsCountIdem and PCountTie with exponents1,1, original quotient fibers, exact intersection Haar volume.',
 27:'Full CountBase from original CountTheoremHypotheses plus 4r<g1 and AutTie, one b,h before cylinders.',
 28:'Entire conditional CountAllRows installer; original CountIdempotentsClass(PCount) remains explicit unproved antecedent.',
 29:'Completed FLC19 applies to the actual same A, original normalized types/RangeW/TieAdmG and actual-rank guard.',
 30:'Exact conditional LinkIRR consumer with one common prior family threshold; common X/ties and arithmetic count supplier remain open.'
}
FOUNDATIONS = [
 dict(id='ARO_ORIGINAL_SETTING',kind='retained_original_data_and_compatibility',
      source_groups=['original_setting','finite_events'],not_reconstructed=True,
      statement='One supplied original D7, its normalized-type record, and actual adelic SG.HidaSetting X with original measures, fields, lattice, frames and representations. This is not the ordinary Hecke-algebra HidaSetting. Their common-family existence is not claimed.'),
 dict(id='ARO_ROWS_FIN_DIM',kind='retained_original_named_hypothesis',
      source_groups=['evaluation'],not_reconstructed=True,
      statement='The full original RowsFinDim, explicitly assumed in ARO18 and all later constructions using finite multiplicities; no new proof of general automorphic finite multiplicity is asserted.'),
 dict(id='ARO_ORIGINAL_TIES',kind='retained_original_same_object_hypotheses',
      source_groups=['original_setting','multiplicities','allrows'],not_reconstructed=True,
      statement='Original AutTie, RowDictTie and LabTie on the same X,G,iota. Their actual simultaneous global producer remains open.'),
 dict(id='ARO_COUNT_THEOREM_ANTECEDENT',kind='explicit_unproved_original_antecedent_only',
      source_groups=['count_parameters'],not_reconstructed=True,
      statement='Exact CountIdempotentsClass(PCount,D,n0,A,C,c3,cb), used only as a supplied antecedent in ARO28 and ARO30. It is not reclassified as a published foundation or claimed completed.'),
 dict(id='ARO_STANDARD_ANALYSIS_ALGEBRA',kind='standard_mathematical_background',
      source_groups=['reduction','haar_inflation','operators','evaluation'],not_a_new_global_producer=True,
      statement='Discrete valuation lattice bases, Nakayama and Chinese remaindering; Haar measure facts, Riesz representation, Fubini and elementary unitary representation algebra. Their exact consumers and normalization calculations are proved in the numbered text.')
]
proof = (HERE/'main.tex').read_bytes()
text = proof.decode()
claims = []
for n in range(1,31):
    cid=f'ARO{n}'
    match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S)
    assert match,cid
    block=match.group().encode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1)
    deps=sorted(set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b',match.group()))-{cid},
                key=lambda d:(re.sub(r'\d+$','',d),int(re.search(r'\d+$',d).group())))
    assert all(not d.startswith('ARO') or int(d[3:])<n for d in deps),(cid,deps)
    ext=['ARO_ORIGINAL_SETTING','ARO_STANDARD_ANALYSIS_ALGEBRA']
    if n in range(18,31): ext.append('ARO_ROWS_FIN_DIM')
    if n in range(21,31): ext.append('ARO_ORIGINAL_TIES')
    if n in [28,30]: ext.append('ARO_COUNT_THEOREM_ANTECEDENT')
    claims.append(dict(id=cid,title=title,introduced_in='0.46',classification='B',
        status='complete human proof at the explicitly stated original scope',depends_on=deps,
        external_input_ids=ext,published_input_ids=[],hypotheses_retained=[SCOPES[n]],
        source_groups=CLAIM_GROUPS[n],sources=[s for g in CLAIM_GROUPS[n] for s in groups[g]],
        proof_location=dict(file=f'{HERE.name}/main.tex',label='claim:'+cid,
            line_start=text[:match.start()].count('\n')+1,line_end=text[:match.end()].count('\n'),
            sha256=sha(block),bytes=len(block)),
        scope_note='Numbered mathematical proof; original source fixes the exact object and quantifiers. No formal replay.'))
claims[27]['conditional_conclusions']={'ARO.32':'Requires exact original CountIdempotentsClass(PCount) antecedent in addition to original parameter and structural inputs.'}
claims[29]['conditional_conclusions']={'LinkIRR':'Requires one common family supplier of actual X/G/iota and original ties and count theorem, or the three expressly sufficient arithmetic tests.'}

baseline=json.loads((ROOT/'history/version_0_45/provenance.json').read_text())
old={c['id']:c for c in baseline['claims']}
human_ids=sorted({d for c in claims for d in c['depends_on'] if not d.startswith('ARO')})
inherited=[]
for cid in human_ids:
    c=old[cid]
    loc=c['proof_location']; path=ROOT/loc['file']; data=path.read_bytes()
    lines=data.splitlines(keepends=True)
    block=b''.join(lines[loc['line_start']-1:loc['line_end']])
    recorded=loc.get('sha256',loc.get('paragraph_sha256'))
    assert recorded in {sha(block),sha(block.rstrip(b'\r\n'))},(cid,'inherited hash mismatch',recorded,sha(block))
    inherited.append(dict(id=cid,file=loc['file'],main_tex_sha256=sha(data),
        block_sha256=sha(block),recorded_baseline_hash=recorded,
        line_start=loc['line_start'],line_end=loc['line_end'],kind='numbered_human_proof_dependency',
        not_an_external_foundation=True))

reviews=[dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))
         for p in sorted(HERE.glob('review_*.json'))]
completed=[
 'Actual rhoX, exact one-prime and total kernel, full surjectivity on original adelic lattice stabilizer',
 'Exact original Haar inflation/convolution/involution comparison with V and every reduction fiber',
 'Full original KppShape membership and character factorization with nontrivial prime characters',
 'Full original EtOne, EtUniv, EtInt and EtAlg on every event',
 'Exact original operator algebra, Schur evaluation bijection and multiplicity/range identification',
 'Full RowsAdd, RowsGood and RowsLab under original RowsFinDim, GapHyp and the original given ties',
 'One actual AllRows with original LabelCountGoodInjective, AllJoinA and full PCountTie',
 'Exact CountBase transport and complete CountAllRows installation conditional on original counting theorem',
 'Same-object FLC19 weight and GQT5 retained-defect consumption with explicit common-family and count antecedents'
]
contracts=dict(schema='rh-arithmetic-rows-contracts/1',artifact_version='0.46',component=HERE.name,
 source_commit=PIN,proof_file_sha256=sha(proof),endpoint_claim='ARO24',count_endpoint_claim='ARO28',
 family_consumer_claim='ARO30',completed_original_substatements=completed,
 human_dependency_ids=human_ids,external_input_ids=[x['id'] for x in FOUNDATIONS],
 proposed_whole_obligation_closures=[],whole_obligation_closures=[],no_lean_replay=True,
 exact_guards_preserved=[
  'One original SG.HidaSetting X; distinct from ordinary Hecke HidaSetting',
  'Original Haar, fundamental domain, formal degrees and V retained everywhere',
  'Both distinct original split primes, all f factors and both conjugate orientations',
  'All sets of polynomial tuples, zero projectors and invalid labels included',
  'Original GapHyp, RowsFinDim and all same-X row ties retained',
  'Original good-row indices and repeated labels preserved by one label completion',
  'Counting uses complementary unipotence prime and intersection volume',
  'Exact original CountIdempotentsClass remains an explicit antecedent',
  'Common-family witnesses and simultaneous threshold remain explicit'],
 simplifications=[
  'Direct reverse flag conditions and CRT replace the intermediate DstarIdx cardinality proof',
  'Absolute trace modulo a completely split rational prime proves nontriviality of the original CRT character',
  'Finite orthogonal decomposition proves RowsAdd directly on original bounded intertwiner spaces'],
 not_claimed=['unconditional existence of common X/G/iota/ties','new general RowsFinDim theorem',
  'unconditional original CountIdempotentsClass or the three special arithmetic counts',
  'whole GLOBAL_RETAINED_DEFECT closure','complete RH or GRH'])
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.46',date='2026-11-23',
 component=HERE.name,source_commit=PIN,main_tex_sha256=sha(proof),proof_file_sha256=sha(proof),
 claims=claims,source_groups=groups,source_inventory=list(inventory.values()),source_files=list(inventory),
 published_applications=[],retained_foundations=FOUNDATIONS,inherited_human_inputs=inherited,
 independent_reviews=reviews,builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
 validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
 claim_blocks=len(claims),direct_named_claim_dependencies_checked=True,
 external_foundations_separate_from_claim_DAG=True,inherited_human_proof_hashes_checked=True,
 no_lean_replay=True))
for name,obj in [('provenance.json',prov),('contracts.json',contracts)]:
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpt.txt').write_text('\n'.join(excerpts))
(HERE/'README.txt').write_text(
 'Arithmetic rows, version 0.46\n\nThirty human proofs ARO1--ARO30 on the original adelic SG.HidaSetting.\n'
 'Main endpoint: full conditional AllRows construction, all labels and good injection, AllJoinA, PCountTie.\n'
 'EtOne, RowsAdd and RowsGood are reconstructed with original Haar, multiplicities and every event.\n'
 'RowsFinDim, common X/ties and the actual arithmetic count theorem remain explicitly scoped inputs.\n'
 'No whole selected obligation is declared closed by this component.\n'
 'No Lean or kernel replay has been run. Exact source bytes and inherited proofs are hash-bound.\n')
print(json.dumps(dict(component=HERE.name,claims=len(claims),proof_sha256=sha(proof),
 source_files=len(inventory),source_ranges=sum(map(len,groups.values())),human_dependencies=human_ids),indent=2))
