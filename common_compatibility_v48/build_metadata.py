#!/usr/bin/env python3
"""Bind the actual common compatibility stage to the accepted original source."""
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
SRC = parser.parse_args().source.resolve()
sha = lambda data: hashlib.sha256(data).hexdigest()
assert subprocess.check_output(
    ['git', '-C', str(SRC), 'rev-parse', 'HEAD'], text=True).strip() == PIN
D = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
P = 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
F = 'src/Formalism/LocalToGlobal/'
S = 'src/Formalism/SharpRestriction/'

SPECS = {
 'finer_quotient': [
  (D+'IsRationalUnitaryDeterminantMapRationalUnitary.lean', 16, 125,
   'Actual congruence subgroup, KDq, DtQ, UOQ, rational map and positive-part relative determinant'),
  (D+'IsRationalUnitaryDeterminantMapRationalUnitary.lean', 208, 238,
   'Quotient by the unit image and its exact relative determinant convention'),
  (D+'IsRationalUnitaryDeterminantMapRationalUnitary.lean', 285, 340,
   'Rational Hilbert--90 and the original e1Q characterization'),
  (D+'ReferenceCharactersFactorTame.lean', 430, 551,
   'Literal LevOk and local-congruence / conjugate-prime quotient criteria'),
  (P+'H90USurjective.lean', 168, 242,
   'Fixed finite-adele coefficients and approximation by the original rational local generators'),
  (P+'H90USurjective.lean', 260, 333,
   'Canonical quotient map from norm-one finite adeles and universal lift equation')],
 'scalar_determinant': [
  (P+'NormOneFiniteAdeleDetClassOfIsDetLift.lean', 21, 57,
   'Exact rank-one matrix u1Dt, every-lift equation, existence and surjectivity'),
  (P+'IsOpenKerNormOneFiniteAdeleDetClass.lean', 18, 83,
   'Original finite-adelic topology and open kernel endpoint'),
  (P+'ExistsFullHermitianColumnsTrueColumns.lean', 27, 56,
   'Integral norm-one kernel and exact UOQ image')],
 'decorated_points': [
  (D+'ReferenceCharactersFactorTame.lean', 34, 182,
   'Given local frames, point extension and positive-part point idele'),
  (D+'ReferenceCharactersFactorTame.lean', 256, 306,
   'All four IsPtOf fields, IsDetLift and actual frame realization'),
  (D+'ReferenceCharactersFactorTame.lean', 563, 565,
   'Literal ptIdl and detPt'),
  (P+'ValDetSubOneLt.lean', 54, 241,
   'Actual K matrix, congruence determinants, valuation differences and point quotient equality'),
  (P+'PointDeterminantEqNormOneClassOfLevel.lean', 13, 50,
   'Exact same-class pointDeterminant_eq_normOneClass_of_level endpoint'),
  (P+'LevOkTwists.lean', 21, 85,
   'Actual selected primes, absence of extra auxiliary primes, LevOk and disjointness')],
 'full_hermitian': [
  (F+'HermitianColumns/FullSym.lean', 14, 77,
   'All eight SymmetricHermitianColumns fields, relative law and every FullTiedS field'),
  (F+'HermitianColumns/FullSym.lean', 101, 130,
   'Exact local prime and kernel equalities in symmetric extra compatibility'),
  (F+'HermitianColumns/FullSym.lean', 215, 219,
   'Literal forgotten Herm0 level and group ties'),
  (F+'HermitianForms/ExtraSym.lean', 10, 16,
   'ColsFullS and ColsExtraTiedS dependent equalities'),
  (P+'ExistsFullHermitianColumnsTrueColumns.lean', 60, 159,
   'Actual endpoint/middle/terminal determinant readings and prescribed-g full extension'),
  (P+'ExistsFullHermitianColumnsTrueColumnsStatement.lean', 7, None,
   'Full original exists_fullHermitianColumns_trueColumns contract')],
 'torsion': [
  (P+'ExistsOrderThree.lean', 18, 130,
   'Finite CM torsion action, cubic/quartic identities and three-torsion pair'),
  (P+'ExistsOrderThree.lean', 132, 250,
   'Exact g3 sign descent and g2 cube-root descent'),
  (D+'IsHalfPtIff.lean', 18, 55,
   'Original baseLat, FieldOK, half-point predicate, chosen generator and trueGx')],
 'period_data': [
  (P+'ExistsOrderThree.lean', 255, 311,
   'Full exists_delta_data on the same coefficient image field'),
  (P+'MeanSquareEvenThetaTwelfthRootInvariant.lean', 15, 80,
   'Unit homothety, discriminant-one lattice dictionary and exact twelfth-root ambiguity'),
  (P+'MeanSquareEvenThetaTwelfthRootInvariant.lean', 134, 235,
   'Conjugate lattice, full DataIn, actual different-ideal generator and Omega identity'),
  (P+'ExistsOrderThree.lean', 353, 371,
   'ties_of_data: the original OmegaCompatible consequence, distinct from its extra theta consequence')],
 'period_endpoint': [
  (F+'GlobalTheory/LinkTiesOm.lean', 63, 78,
   'All literal OmegaCompatible fields and the exact pi/norm/area normalization'),
  (P+'ExistsGIs.lean', 21, 67,
   'Given period root, actual third roots of unity in Base, omTied_retie_of_cube and omTied_withTrue')],
 'recursive_compatibility': [
  (F+'GroupLattices/StdSubAtOfRing.lean', 36, 89,
   'Four ring isomorphisms, all five commuting equations, GatIs and all five GroupCompatibilityAll fields'),
  (F+'GroupLattices/TiedFamilies/FullTiedCBase.lean', 45, 124,
   'Actual packC, recC, identity ring maps and joint groupCompatibilityOfRecursion'),
  (F+'GroupLattices/ComparisonMaps/TiedRec.lean', 40, 67,
   'Original FrRat, StdB and complete CmpTied contract'),
  (P+'ExistsConcrete.lean', 16, 110,
   'Actual common local identifications, positions, companion and split-prime dictionary'),
  (P+'IsRecGOfIsLocalFamily.lean', 13, 74,
   'Full simultaneous IsLocalFamily and the original five-entry recursive equality'),
  (D+'TiedColumnData.lean', 36, 68,
   'Complete original IsRecG constructor and its joint dependent equality')],
 'stage_transport': [
  (D+'ExistsTiedOfIsRecG.lean', 14, 47,
   'IsRecG group-tie replacement, exact GatNum and unchanged hP/lamRec/tauRec/period data'),
  (P+'ColumnLayerConditionsTrueColumnsLaterStages.lean', 24, 94,
   'Exact degree-zero form transport, stage-zero equality, StdC and every StdLvC'),
  (P+'ExistsGIs.lean', 82, 142,
   'IsLocalFamily on later stages and full ColumnDataSplitPrimes installation with given g')],
 'stage_endpoint': [
  (D+'PositionOfIntro.lean', 23, 40,
   'Every original ColW input, including Laws, Pins, FieldOK and exact field'),
  (D+'PositionOfIntro.lean', 70, 87,
   'Original StepW, all ColT fields and earlier G-stage choice'),
  (D+'PositionOfIntro.lean', 114, 115,
   'StepW.of_all with the original Over and Forced guards'),
  (D+'TiedColumnData.lean', 91, 96,
   'Full ColumnDataSplitPrimes and GIs2 quantifiers: G before all W,V,S,N'),
  (D+'AmbientBaseHeq.lean', 26, 29,
   'Both exact GatNum formulas, including r split and original ceiling'),
  (D+'WithTrue.lean', 12, 17,
   'withTrue preserves original stage data and installs actual volume and trueGx'),
  (D+'ExistsOkPins.lean', 194, 203,
   'Literal bare Later existence on fixed true columns'),
  (D+'ExistsStagesClauses.lean', 474, 486,
   'HasLetters from the original Over guard'),
  (P+'ExistsGIs.lean', 146, 165,
   'Full exists_trueVolume_stage_of_any_column_choice and Pinned specialization')],
 'division_transport': [
  (P+'ConcreteSplitPrimeAutomorphicDataDivisionLattice.lean', 21, 80,
   'Exact arbitrary setDiv CmpIn/CmpHyp0P/latCmpC and complete IsRecG transport'),
  (P+'ConcreteSplitPrimeAutomorphicDataDivisionLatticeStatement.lean', 7, None,
   'Literal concreteSplitPrimeAutomorphicData_divisionLatticeChange contract'),
  (P+'ColsReTo0S.lean', 21, 92,
   'Actual division transport of forms, full Hermitian columns and all five group fields'),
  (P+'ColumnLocalDataTransportDivision.lean', 14, 43,
   'Entire ColT/ColumnDataSplitPrimes transport, including isRec and unchanged om')],
 'given_extra_realization': [
  (D+'DsigEq.lean', 24, 66,
   'All Wit inputs, single dependent (Gt,cmp,tw,ker) equality, WPt and joint (D,O) realization'),
  (D+'TiedColumnData.lean', 111, 125,
   'Original kernel embedding and positive-degree equalities used by ColsExtraTiedS'),
  (P+'ExtraTiedCol.lean', 10, 19,
   'Literal WPt.extraTied_col on the supplied O.ex.cmp'),
  (F+'ThresholdSelection.lean', 9, 16,
   'TSelF and TSel, with threshold preceding every original point and index'),
  (F+'ClassSLinks.lean', 9, 13,
   'Eventual same-comparison GroupCompatibilityFamily consumer'),
  (F+'ClassOfRecordOfChoice.lean', 34, 62,
   'WithChN, actual selected D3 class and tied-record projection')],
 'selected_tops_and_gain': [
  (S+'SmoothDesignExistence/DesignExistsDes.lean', 10, 15,
   'Actual Des membership contains the unchanged ChosenE witness'),
  (S+'GlobalSchurBounds/Chosen.lean', 18, 90,
   'Exact ChosenTT, ChosenBad and ChosenE selected-subset fields'),
  (S+'SmoothDesignExistence/AdmissibleTopsMertens.lean', 15, 19,
   'Literal TopsF and its projection from ChosenE'),
  (S+'SmoothDesignExistence/AdmissibleTopsMertens.lean', 73, 144,
   'Original same-subset Adm2F and exact harmonic threshold'),
  (F+'Divisibility/DivisibilityRemainder/AdmissibleClasses/LinkGCl.lean', 11, 32,
   'Original gTiedF_of_sel, admissible_tops_of_class, linkG_closed and linkG_frame'),
  (S+'ParamsHeightRankConstant.lean', 112, 181,
   'Original Closed choice order and pointwise maximum of coefficient bounds'),
  (F+'GroupLattices/LinkGConcreteNoKer.lean', 44, 56,
   'Full original linkG_concrete5 with its two class-level antecedents'),
  (S+'GlobalTheoremInputs.lean', 97, 140,
   'All five LinkG fields, original error and same-family normalization')]
}

inventory, groups, excerpts = {}, {}, []
for group, specs in SPECS.items():
    groups[group] = []
    for i, (path, lo, hi, title) in enumerate(specs, 1):
        data = (SRC/path).read_bytes()
        assert data == subprocess.check_output(
            ['git', '-C', str(SRC), 'show', PIN+':'+path]), path
        lines = data.splitlines(keepends=True)
        hi = hi or len(lines)
        assert 1 <= lo <= hi <= len(lines), (path, lo, hi, len(lines))
        block = b''.join(lines[lo-1:hi])
        item = dict(
            id=f'GCF_{group}_{i:02}', path=path, line_start=lo, line_end=hi,
            declaration=title, file_sha256=sha(data), range_sha256=sha(block),
            range_bytes=len(block), source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{lo}-L{hi}')
        groups[group].append(item)
        inventory[path] = dict(
            path=path, sha256=sha(data), bytes=len(data), line_count=len(lines),
            verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{item["id"]}] {title}\n{item["url"]}\n'
                        f'Range SHA256: {sha(block)}\n{block.decode()}\n')

DEPS = {
 1: [],
 2: ['HF15'],
 3: ['GCF1', 'GCF2', 'HF14'],
 4: ['GCF2', 'GCF3', 'HF15'],
 5: ['GCF2', 'GCF3', 'GCF4', 'HF15'],
 6: ['GCF3', 'GCF5'],
 7: ['PA1', 'TA1', 'TA5'],
 8: ['GCF7', 'PA2', 'TA11'],
 9: ['GCF7'],
 10: ['GCF8', 'GCF9', 'PA1', 'TA5'],
 11: ['GCF7', 'GCF10', 'PA1', 'TA1'],
 12: [f'LI{n}' for n in range(1, 9)]
     + [f'SF{n}' for n in range(1, 8)]
     + [f'CR{n}' for n in range(1, 7)] + ['VE8', 'VE9'],
 13: ['GCF12', 'VE7'],
 14: ['GCF6', 'GCF11', 'GCF12', 'GCF13',
      'LS22', 'HF19', 'TG12', 'FC16', 'GV19'],
 15: ['VE7'],
 16: ['GCF15'],
 17: ['GCF14', 'GCF16'],
 18: ['GCF17', 'GLG16', 'LGS13']
}
GROUPS = {
 1: ['finer_quotient'],
 2: ['finer_quotient', 'decorated_points'],
 3: ['finer_quotient', 'scalar_determinant'],
 4: ['decorated_points', 'scalar_determinant'],
 5: ['finer_quotient', 'decorated_points', 'full_hermitian'],
 6: ['full_hermitian', 'scalar_determinant'],
 7: ['torsion'],
 8: ['torsion', 'period_data'],
 9: ['torsion'],
 10: ['torsion', 'period_data', 'period_endpoint'],
 11: ['period_data', 'period_endpoint'],
 12: ['recursive_compatibility', 'stage_endpoint'],
 13: ['recursive_compatibility', 'stage_transport'],
 14: ['stage_endpoint', 'stage_transport', 'full_hermitian',
      'recursive_compatibility', 'period_endpoint'],
 15: ['division_transport', 'recursive_compatibility'],
 16: ['division_transport', 'full_hermitian', 'period_endpoint'],
 17: ['given_extra_realization', 'full_hermitian',
      'recursive_compatibility', 'stage_endpoint'],
 18: ['selected_tops_and_gain', 'given_extra_realization']
}
SCOPES = {
 1: 'Actual finite adeles and the source rational local F-unit generators; integral local lifts almost everywhere and all infinite components handled.',
 2: 'Exact KDq congruence criterion on the actual SG=vGs and SQ, with unramified finite CM primes, original LevOk and no extra selected congruence places.',
 3: 'Actual u1Dt, every-lift equality, surjectivity, exact open kernel, UOQ image and rational e1Q; specified tensor-product topology.',
 4: 'Given decorated self-dual lattice and original frames/Reads representative; exact principal-unit quotient, all ranks including zero.',
 5: 'Every original det0/detI representative and every-rank adelic relative determinant, with positive-part convention and no global-freeness assumption.',
 6: 'Full ColsFullS preserving an arbitrary given SymmetricGroupCompatibility, same columns, true volume input and universal StdDt.',
 7: 'Possibly discontinuous complex automorphisms act only on algebraic torsion identities; exact eta^6=1, g2/g3 exponents and CM annihilator equivalence.',
 8: 'Actual distinguished two-torsion class; CM d=7 mod8, normalized discriminant one, sign descent for g3 without coefficient-field extension.',
 9: 'All nonzero three-torsion abscissae, actual CM involution, exact normalized quartic and cube-root descent; beta^2=-d and 3 not dividing d retained.',
 10: 'Complete DataIn for the given original discriminant twelfth root; actual Base contains mu_3, so neither period nor coefficient field is changed.',
 11: 'All literal OmegaCompatible fields, every infinity label and complex embedding, same different-ideal generator, exact pi*norm^2/area inverse.',
 12: 'Actual local models, exact rank and numerical formulas, all four ring identities/five commuting laws, full five-field GroupCompatibilityAll and joint IsRecG.',
 13: 'The same local choices, forms and value polynomials transport between arbitrary Later stages over fixed B,C; no later re-choice of the common frame.',
 14: 'Full original exists_trueVolume_stage_of_any_column_choice and Pinned specialization: one G before all W,V,S,N, original Over/Forced/ColW input retained.',
 15: 'Every original setDiv by arbitrary submodules N and real heights h; literal LatCmp equality and all five entries of IsRecG transported, no extra lattice hypothesis.',
 16: 'Entire GroupCompatibilityAll, ColT and ColumnDataSplitPrimes under the same division transport; period field unchanged and no unrelated Extra field inferred.',
 17: 'Given WPt uses the single dependent (Gt,cmp,tw,ker) equality; eventual GroupCompatibilityFamily requires exact joint (D,O) realization or original TSel.',
 18: 'Original selected D3 membership supplies TopsF/Adm2F on the same subset; class-level full LinkG remains conditional on original common realization/TSel.'
}
FOUNDATIONS = [
 dict(id='GCF_ORIGINAL_HOST_AND_COLUMN_INPUT',
      kind='explicit_original_data_and_guards',
      statement='The original arithmetic Host/Base, actual selected auxiliary/SQ primes, I.Ok, Pins, Laws, ColW, Over and Forced guards, FieldOK and the prescribed period root. These are precisely the original stage endpoint antecedents, not a newly assumed compatibility record.',
      not_reconstructed_as_a_whole=True,
      source_groups=['decorated_points','torsion','stage_endpoint']),
 dict(id='GCF_ORIGINAL_TRUE_VOLUME_FOUNDATION',
      kind='retained_original_foundation_via_numbered_human_claim',
      statement='The original true-volume/Haar normalization premise retained in the completed GV19 proof. GCF14 uses GV19 at that exact scope, without asserting a new normalization theorem or a completed global measured/Bessel setting.',
      not_reconstructed_as_a_whole=True,
      source_groups=['stage_endpoint','full_hermitian']),
 dict(id='GCF_STANDARD_LOCAL_AND_TORSION_BACKGROUND',
      kind='standard_mathematical_background',
      statement='Finite-dimensional linear algebra, completions and restricted products, Dedekind ideal invertibility and local bases, density of a number field in a completion, elementary finite torsion linear algebra, and field-embedding extension. The elliptic uniformization, invariant and CM-action dictionaries are inherited numbered human claims PA1/PA2 and TA1/TA5/TA11, not silently reclassified as external results.',
      not_a_new_arithmetic_producer=True,
      source_groups=['finer_quotient','torsion','period_data']),
 dict(id='GCF_GIVEN_WPT_OR_TSEL_REALIZATION',
      kind='explicit_original_remaining_common_family_producer',
      statement='Only GCF17-18 retain actual WPt realizations with the joint (D,O) and dependent (Gt,cmp,tw,ker) equalities, or the original TSel selector. GCF14 supplies the full GIs2 column stage; it does not by itself supply every other Wit field or identify an arbitrary supplied FamP with these stages.',
      not_reconstructed_as_a_whole=True,
      source_groups=['given_extra_realization']),
 dict(id='GCF_ORIGINAL_SELECTED_CLASS_AND_COEFFICIENT_GUARDS',
      kind='explicit_original_family_class_guards',
      statement='The original D3(3,A)=Des(WithChN(A),3) class, sufficient coefficient region and Closed quantifier order. Its ChosenE field is actually projected to TopsF/Adm2F; this is no longer an independent producer once membership is given. The TSel/common-realization premise remains separate.',
      not_a_new_arithmetic_producer=True,
      source_groups=['selected_tops_and_gain'])
]
EXT = {n: ['GCF_STANDARD_LOCAL_AND_TORSION_BACKGROUND'] for n in range(1,19)}
for n in list(range(1,7)) + list(range(10,19)):
    EXT[n].append('GCF_ORIGINAL_HOST_AND_COLUMN_INPUT')
for n in [6,14]:
    EXT[n].append('GCF_ORIGINAL_TRUE_VOLUME_FOUNDATION')
for n in [17,18]:
    EXT[n].append('GCF_GIVEN_WPT_OR_TSEL_REALIZATION')
EXT[18].append('GCF_ORIGINAL_SELECTED_CLASS_AND_COEFFICIENT_GUARDS')

proof = (HERE/'main.tex').read_bytes()
text = proof.decode()
assert not any(c < 32 and c not in (9,10) for c in proof), 'control character'
claims, blocks = [], {}
for n in range(1,19):
    cid = f'GCF{n}'
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n', text, re.M|re.S)
    assert m, cid
    blocks[cid] = m.group()
    named = set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b', m.group())) - {cid}
    assert named <= set(DEPS[n]), (cid, 'unrecorded named references', named-set(DEPS[n]))
    assert all(not d.startswith('GCF') or int(d[3:]) < n for d in DEPS[n]), cid
    for prefix, a, b in re.findall(r'\b([A-Z]{2,4})([0-9]+)--\1([0-9]+)\b', m.group()):
        needs = {f'{prefix}{j}' for j in range(int(a),int(b)+1)}
        assert needs <= set(DEPS[n]), (cid, 'unrecorded range dependency', needs-set(DEPS[n]))
    block = m.group().encode()
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1)
    claims.append(dict(
        id=cid, title=title, introduced_in='0.48', classification='B',
        status='complete human proof at the explicitly stated original scope',
        depends_on=DEPS[n], external_input_ids=EXT[n], published_input_ids=[],
        hypotheses_retained=[SCOPES[n]], source_groups=GROUPS[n],
        sources=[s for group in GROUPS[n] for s in groups[group]],
        proof_location=dict(file=HERE.name+'/main.tex',label='claim:'+cid,
            line_start=text[:m.start()].count('\n')+1,
            line_end=text[:m.end()].count('\n'),sha256=sha(block),bytes=len(block)),
        source_proof_is_not_human_proof=True))
owners = {n: cid for cid, block in blocks.items()
          for n in re.findall(r'\\tag\{GCF\.(\d+)\}',block)}
for claim in claims:
    cid = claim['id']
    refs = set(re.findall(r'GCF\.(\d+)',blocks[cid])) - set(
        re.findall(r'\\tag\{GCF\.(\d+)\}',blocks[cid]))
    needed = {owners[n] for n in refs if n in owners and owners[n] != cid}
    assert needed <= set(claim['depends_on']), (cid,'unrecorded formula references',needed)

ledger = {c['id']:c for c in json.loads((ROOT/'provenance.json').read_text())['claims']}
human_ids = sorted({d for deps in DEPS.values() for d in deps if not d.startswith('GCF')})
inherited = []
for cid in human_ids:
    record = ledger[cid]
    loc = record['proof_location']
    path = ROOT/loc['file']
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    if 'line_start' in loc:
        lo,hi = loc['line_start'],loc['line_end']
        block = b''.join(lines[lo-1:hi])
        bound = loc.get('sha256',loc.get('range_sha256',loc.get('paragraph_sha256')))
        assert bound and sha(block) == bound, (cid,sha(block),bound)
        binding = 'exact previously recorded numbered-claim byte range'
    else:
        # Keep the older immutable record unchanged. The whole chapter is the
        # explicit byte/range binding when its historical locator has no range.
        lo,hi,block = 1,len(lines),data
        assert re.search(r'\b'+cid+r'\b',data.decode()), (cid,path)
        binding = 'entire immutable legacy chapter containing the named human proof'
    inherited.append(dict(
        id=cid,file=str(path.relative_to(ROOT)),main_tex_sha256=sha(data),
        block_sha256=sha(block),line_start=lo,line_end=hi,binding_scope=binding,
        kind='numbered_human_proof_dependency',not_an_external_foundation=True))
assert not set(human_ids) & {f['id'] for f in FOUNDATIONS}

lookup = {c['id']:c for c in claims}
reviews = []
for path in sorted(HERE.glob('review_*.json')):
    review = json.loads(path.read_text())
    assert review.get('result',review.get('status')) == 'PASS',path
    bound = review.get('proof_sha256',review.get('proof_file_sha256',review.get('main_tex_sha256')))
    assert bound == sha(proof),(path,bound,sha(proof))
    for checked in review.get('claims_reviewed',[]):
        if isinstance(checked,dict):
            assert checked['result'] == 'PASS',checked
            block_hash = checked.get('block_sha256',checked.get('proof_range_sha256'))
            assert block_hash == lookup[checked['id']]['proof_location']['sha256'],checked
    reviews.append(dict(file=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes())))

completed = [
 'Actual finite-adelic Hilbert--90, canonical u1Dt and all scalar laws, including exact open kernel (GCF1-3)',
 'Same decorated-point and every column/class determinant readings, arbitrary-rank relative law (GCF4-5)',
 'Entire ColsFullS preserving a given local-tie family and universal StdDt (GCF6)',
 'CM two-/three-torsion sign/cube descent and complete DataIn for the given period root in the same coefficient field (GCF7-10)',
 'All original OmegaCompatible fields and exact omTied_withTrue for every later stage (GCF11)',
 'Five-field actual GroupCompatibilityAll and full joint IsRecG on the constructed recursive record (GCF12)',
 'Same local family, forms and comparison before all later choices (GCF13)',
 'Full exists_trueVolume_stage_of_any_column_choice and exists_GJStage_GIs2_pinned at original premises (GCF14)',
 'Literal comparison and complete IsRecG/ColT/ColumnDataSplitPrimes under every setDiv (GCF15-16)',
 'WPt.extraTied_col on the supplied comparison/kernel, and exact conditional eventual-family consumer (GCF17)',
 'Original selected D3 supplies TopsF/Adm2F; full class LinkG conditional only on original realization/TSel and existing coefficient guards (GCF18)'
]
coverage = {
 'u1Dt.full_scalar_laws':'GCF1-GCF3',
 'pointDeterminant_eq_normOneClass_of_level':'GCF4',
 'SymmetricHermitianColumns.det0_detI':'GCF5',
 'SymmetricRelativeDeterminant':'GCF5',
 'exists_fullHermitianColumns_trueColumns':'GCF6',
 'exists_delta_data':'GCF7-GCF10',
 'DataIn.given_root_same_field':'GCF10',
 'OmegaCompatible':'GCF11',
 'omTied_withTrue':'GCF11',
 'GroupCompatibilityAll.actual_recursive_record':'GCF12',
 'IsRecG.full_dependent_equality':'GCF12',
 'IsLocalFamily.transport_before_later_choices':'GCF13',
 'exists_trueVolume_stage_of_any_column_choice':'GCF14',
 'exists_GJStage_GIs2_pinned':'GCF14',
 'GIs2.VolTieG':'GCF14 via GV19 at its retained original foundation',
 'GIs2.GatNum':'GCF12/GCF14',
 'GIs2.ColumnDataSplitPrimes':'GCF14',
 'setDiv.latCmpC_literal_equality':'GCF15',
 'setDiv.IsRecG':'GCF15',
 'columnLocalDataTransportDivision':'GCF16',
 'WPt.extraTied_col':'GCF17, on the original supplied WPt',
 'GroupCompatibilityFamily.selected_common_family':'GCF17 only after original joint realization/TSel',
 'TopsF.selected_D3':'GCF18, actual class projection',
 'Adm2F.selected_D3':'GCF18/GLG16, same selected subset and exact threshold',
 'LinkG.all_five_fields':'GCF18/LGS13, retaining the actual realization/TSel premise',
 'GLOBAL_LOCAL_GAIN.whole_selected_leaf':'remains open; actual simultaneous realization not supplied'
}
traps = [
 'The exact quotient criterion is for actual SG=vGs and SQ; arbitrary LevOk may contain extra selected primes and is not substituted.',
 'KDq retains principal-unit congruences; quotient by all units occurs only in the relative determinant.',
 'The point/class representatives and their residue/rational frames are the supplied ones; simultaneous row/column reindexing alone is used.',
 'Every-rank relative determinant permits arbitrary adelic unitary g and nonfree global lattices; local bases suffice.',
 'An existing given local-tie g is preserved in ColsFullS; no independently chosen local family is inserted.',
 'CM torsion uses discontinuous field automorphisms only on algebraic identities, never on analytic limits.',
 'The given discriminant twelfth root is retained in the actual Base; its original mu_3 field resolves the only cube-root ambiguity.',
 'Omega retains the same different-ideal generator, all complex embeddings and exactly pi*norm^2/area inverted.',
 'All four coefficient rings and five maps are the actual recursive ones; rank equality, normalized valuation and Ce=1 are exact.',
 'One GJStage is chosen before every W,V,S,N; later transport preserves the actual unique-polynomial comparison.',
 'setDiv permits arbitrary submodules and real heights and proves literal LatCmp equality, not merely isomorphic images.',
 'Given-family compatibility uses a single dependent (Gt,cmp,tw,ker) equality and original joint (D,O) realization.',
 'Selected D3 contains its actual ChosenE; TopsF/Adm2F require no resampling and use the unchanged GLG16 threshold.',
 'The two Closed-class inputs precede all later families/heights; TSel/common realization remains explicit.',
 'Full GIs2 does not imply the remaining row, kernel/theta, divisor, gauge and object fields of Wit.'
]
frontier = [
 'Construct the original eventual WPt/TSel realization of the selected common family, with the joint (D,O) equality and the single dependent (Gt,cmp,tw,ker) equality. GCF14 supplies its full GIs2 column stage, and GCF15-16 preserve that input through arbitrary division choices.',
 'Supply the remaining original Wit rows, kernel/theta, divisor, object and gauge fields at the same earlier choices; separate local compatible records do not identify the given Extra.cmp.',
 'For a completely arbitrary FamP outside the selected D3 class, actual TopsF/Adm2F is still an independent antecedent. Within D3 its original ChosenE field supplies it by GCF18.',
 'All other original global denominator, retained-defect, period-height and spectral producers remain separate. No whole GLOBAL_LOCAL_GAIN or RH/GRH closure is claimed.'
]
contracts = dict(
    schema='rh-common-compatibility-contracts/1',artifact_version='0.48',
    component=HERE.name,source_commit=PIN,proof_file_sha256=sha(proof),
    endpoint_claim='GCF14',transport_endpoint='GCF16',
    selected_family_consumer='GCF18',
    original_endpoint='GlobalTheory.Mem.Top.Bl.TrueLocal.exists_trueVolume_stage_of_any_column_choice',
    original_specialization='GlobalTheory.T.exists_GJStage_GIs2_pinned',
    original_full_scope='For any original WP p, StepW p (fun K B f T w => exists G : GJStage B w.C, GIs2 K w G); G is chosen before all W,V,S,N.',
    completed_original_substatements=completed,original_field_coverage=coverage,
    exact_guards_preserved=traps,remaining_actual_producers=frontier,
    human_dependency_ids=human_ids,external_input_ids=[f['id'] for f in FOUNDATIONS],
    selected_consumer_only=False,full_original_GIs2=True,
    prescribed_comparison_under_transport=True,same_coefficient_field=True,
    all_original_LinkG_fields=True,LinkG_requires_original_realization=True,
    whole_obligation_closures=[],proposed_whole_obligation_closures=[],
    no_lean_replay=True,
    not_claimed=['existence of every remaining Wit field',
                 'eventual realization of an arbitrary supplied FamP',
                 'identification of arbitrary independently chosen comparisons',
                 'unconditional whole GLOBAL_LOCAL_GAIN',
                 'new global measured/Bessel or Siegel--Weil producer',
                 'complete RH or GRH'])
prov = dict(
    schema='rh-human-component-provenance/1',artifact_version='0.48',
    date='2026-11-23',component=HERE.name,source_commit=PIN,
    main_tex_sha256=sha(proof),proof_file_sha256=sha(proof),claims=claims,
    source_groups=groups,source_inventory=list(inventory.values()),
    source_files=list(inventory),published_applications=[],
    retained_foundations=FOUNDATIONS,inherited_human_inputs=inherited,
    independent_reviews=reviews,
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,
        all_source_bytes_compared_to_pinned_git_blobs=True,claim_blocks=len(claims),
        direct_named_claim_dependencies_checked=True,
        numbered_range_dependencies_checked=True,
        numbered_formula_dependencies_checked=True,
        external_foundations_separate_from_claim_DAG=True,
        whole_original_leaf_closures=[]),
    scope_note='Full original actual common GIs2 stage, its determinant/period suppliers and literal comparison transport. The selected D3 top field is supplied. Actual eventual WPt/TSel realization of the given common family remains explicit; no whole selected-leaf closure.')
closure = dict(
    schema='rh-human-component-closure/1',artifact_version='0.48',
    component=HERE.name,proof_file_sha256=sha(proof),
    new_claims=[c['id'] for c in claims],new_claim_count=len(claims),
    completed_original_substatements=completed,
    whole_obligation_closures=[],proposed_whole_obligation_closures=[],
    remaining_actual_producers=frontier,
    status='Full original GIs2 supplier and same-comparison division transport completed at original inputs; selected-class TopsF/Adm2F supplied; actual common-family realization remains open.',
    full_original_GIs2=True,full_original_IsRecG=True,
    all_five_compatibility_fields_constructed_on_actual_stage=True,
    given_period_root_and_coefficient_field_unchanged=True,
    one_G_before_all_later_choices=True,
    arbitrary_division_lattice_transport=True,
    actual_comparison_equality_preserved=True,
    selected_D3_TopsF_produced=True,selected_D3_Adm2F_produced=True,
    original_common_family_realization_retained=True,
    original_geometric_chain_unchanged=True,
    exact_error_and_constants_preserved=True,no_lean_replay=True)
outputs = {
 'provenance.json':prov,'contracts.json':contracts,'closure.json':closure,
 'source_manifest.json':dict(
     schema='rh-source-manifest/1',component=HERE.name,source_commit=PIN,
     source_files=list(inventory.values()),ranges=groups,verified_against_git=True),
 'retained_foundations.json':FOUNDATIONS,'published_inputs.json':[]
}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 'ONE ACTUAL COMMON COMPATIBILITY STAGE — v0.48\n'
 f'Source pin: {PIN}\nMain SHA256: {sha(proof)}\n\n'
 f'{len(claims)} numbered human proofs, classification B; {len(inventory)} pinned source files; '
 f'{sum(map(len,groups.values()))} cited source ranges; {len(inherited)} inherited numbered human proof bindings.\n\n'
 'The completed producer is the full original exists_trueVolume_stage_of_any_column_choice, '
 'including its Pinned specialization exists_GJStage_GIs2_pinned. It chooses one actual GJStage '
 'before every later W,V,S,N. Its GIs2 contains the true-volume normalization, both exact '
 'GatNum formulas and the entire ColumnDataSplitPrimes record. The original host, column '
 'choice, FieldOK, Over/Forced guards and the true-volume foundation retained by GV19 remain '
 'the original premises. No new abstract compatibility record is assumed to produce this stage.\n\n'
 'GCF1-6 construct the actual finite-adelic norm-one determinant map. The proof gives local '
 'Hilbert--90 lifts that are units almost everywhere, verifies that fixed lifts differ by '
 'the original rational local generators, and proves the exact principal-unit congruence '
 'criterion for KDq on the actual selected primes. It supplies the open kernel, image of '
 'integral units, rational determinant and every-lift identity. The decorated-point calculation '
 'keeps the actual frames and representatives. The relative law uses local bases for arbitrary '
 'self-dual global lattices and the original positive-part determinant convention. All eight '
 'Hermitian determinant fields are then installed while preserving a given local-tie family.\n\n'
 'GCF7-11 resolve the actual period normalization over the given coefficient field. On '
 'discriminant-one CM ideal lattices, the distinguished two-torsion class fixes the sign of '
 'g3; the actual CM involution on the four three-torsion abscissae gives '
 '(g2-3*(x+y)^2)^3=1 and fixes g2 up to a third root of unity. The original Base already '
 'contains those roots. Thus the prescribed discriminant twelfth root itself has both '
 'invariants in the original coefficient field. The full DataIn and OmegaCompatible follow '
 'with the same different-ideal generator and exactly (pi*|rho(d)|^2/area)^(-1), for every '
 'infinity label and embedding. No analytic limit is subjected to a discontinuous field '
 'automorphism; only algebraic elliptic-curve identities are transported.\n\n'
 'GCF12-14 assemble previously completed LI/SF/CR/VE/TG/FC/GV constructions with these new '
 'determinant and period suppliers. All five GroupCompatibilityAll fields are on one actual '
 'recursive record: same level-zero forms, integral comparison map, four coefficient rings, '
 'five commuting ring equations and original GatIs model. Exact ranks, normalized valuations '
 'and Ce=1 are preserved. The common choices are made before the later row, division, metric '
 'and number-theoretic stages. Full IsRecG uses the joint dependent equality of its five '
 'objects, not only agreement of ranks or independent local witnesses.\n\n'
 'GCF15-16 prove literal comparison equality under every original setDiv change, allowing '
 'arbitrary submodules and real heights. The unique value-polynomial evaluation formula is '
 'unchanged. This transports all of IsRecG, GroupCompatibilityAll, ColT and '
 'ColumnDataSplitPrimes, including the unchanged period field. It does not transport unrelated '
 'fields of Extra by implication.\n\n'
 'GCF17 checks the exact given-WPt equality with O.ex.cmp through the single dependent '
 '(Gt,cmp,tw,ker) equality. Its family consequence still requires the original eventual '
 'joint (D,O) realization, or TSel. GCF18 observes that actual D3 membership already contains '
 'ChosenE and hence TopsF; GLG16 gives Adm2F with its unchanged threshold '
 'max(xa,xb,Fm.x1+1,(16*Cb+2)^(3/epsilon)). Combining the two Closed-class inputs with '
 'LGS13 preserves all five LinkG fields, b^(x^(-epsilon/2)) and C_G=4*Ccount+1. '
 'The original common realization is retained, so GLOBAL_LOCAL_GAIN remains open.\n\n'
 'PRECISE REMAINING PRODUCERS\n'
 + ''.join('- '+item+'\n' for item in frontier)
 + '\nThe reproducible builder checks all cited bytes against the accepted immutable source '
 'blob, binds every numbered inherited human proof independently of external foundations, '
 'checks named/range/formula dependencies, and records all proof-block hashes. It runs no '
 'Lean/kernel replay and changes no frozen chapter, common ledger or historical artifact.\n')
hashes = {p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
          if p.is_file() and p.name != 'hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(
    dict(component=HERE.name,artifact_version='0.48',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(
    claims=len(claims),source_files=len(inventory),
    source_ranges=sum(map(len,groups.values())),inherited_claims=len(inherited),
    main_tex_sha256=sha(proof),actual_stage_endpoint='GCF14',
    transport_endpoint='GCF16',selected_family_consumer='GCF18',
    whole_original_leaf_closures=[]),indent=2))
