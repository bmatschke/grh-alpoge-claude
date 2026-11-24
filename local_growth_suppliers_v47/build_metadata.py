#!/usr/bin/env python3
"""Bind actual local growth/admission suppliers to the fixed original contracts."""
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
G = 'src/Formalism/SharpRestriction/GrowthBounds/'
S = G + 'LogarithmicSums/'
C = 'src/Formalism/LocalToGlobal/GroupLattices/'
L = 'src/Formalism/LocalRingCardinality/'
T = 'src/Formalism/SharpRestriction/'

SPECS = {
 'family_data': [
  (T+'ParConsts.lean', 31, 100, 'FamP: the original simultaneous family, fixed coefficients, ex, ties and fills'),
  (T+'ElevenLe.lean', 15, 144, 'All literal SizesAt inequalities'),
  (L+'DataParams.lean', 62, None, 'Original ParameterChoice numerical hypotheses'),
  (L+'DataExtra.lean', 24, 69, 'EpTie, NuUnserved, Extra and geometric ker field; ep_def is retained'),
  (G+'IsResidueClassZero.lean', 14, 75, 'Original fifteen coefficients, scales, windows and band radii')],
 'model_sandwich': [
  (G+'UnramifiedQuadraticSetting.lean', 12, 84, 'HidaSetting and actual lattice/model definitions'),
  (G+'Joints.lean', 1462, 1578, 'wExp, WeylSandwichG, ExpBoundG, model sandwich and tensor assembly'),
  (C+'FockModels/Sandwich.lean', 42, 218, 'Primitive polynomial normalization, standard-model comparison and actual Hida-setting transport'),
  (L+'ColumnWeightSpreadOffTop.lean', 34, 250, 'Actual top/off-top spreads, both Frobenius parities and all coefficient factors'),
  (G+'Joints.lean', 1848, 1926, 'Exact actual exponent sum bounded by X.ep'),
  (G+'SmallOrderPrimes.lean', 190, 197, 'Both original adm9 clauses, all GIdx places')],
 'orbit_sizes': [
  (G+'SmallOrderPrimes.lean', 70, 120, 'Exact adm1 through adm5, including all original orbit and band clauses'),
  (G+'TopChoiceBounds.lean', 4392, 4438, 'Uniform orbit constant, original FamilyWindowLogBound and band family endpoints'),
  (G+'PlaneCountTheoremWithConstants.lean', 1472, 1531, 'Original family size/orbit/order statements and finite-class predicate')],
 'small_order': [
  (T+'AdmissibleParameterJoins/GandSk.lean', 13, 55, 'Actual hP and cyclotomic dyadic Frobenius identification'),
  (G+'CornerGLContinuity.lean', 121, 139, 'Original global dyadic order and Frobenius compatibility contracts'),
  (G+'TopChoiceBounds.lean', 1670, 1762, 'Exact size/order normalization and power-saving budget'),
  (G+'SmallOrderPrimes.lean', 103, 107, 'Literal adm3 finite weighted prime sum')],
 'power_bands': [
  (G+'TopChoiceBounds.lean', 1907, 2086, 'One-power and all-power finite interval sums and original x^-1 specialization'),
  (G+'SmallOrderPrimes.lean', 109, 113, 'All five ArchimedeanSignatureMatching fields')],
 'local_certificates': [
  (G+'SmallOrderPrimes.lean', 122, 189, 'Full adm6, fourteen HypI fields, canonical adm7 and full mean adm8'),
  (G+'Joints.lean', 1999, 2127, 'StdSubAt, full HypIAt/HypIIAt and exact LPprime producer at the original place'),
  (G+'PlaneCountTheoremWithConstants.lean', 941, 986, 'Original first/second local theorem constants and canonical infimum family'),
  (C+'AdmissibleFamilyNoKernel.lean', 99, 123, 'Full original HypIAt family supplier')],
 'canonical_mean': [
  (G+'IsResidueClassZero.lean', 270, 354, 'Candidate, actual deficit, meanLoc, MeanKappaBound, Sv/tauP/ioP'),
  (S+'SlopeEstimateOfLemmaBSlopeLine.lean', 153, 257, 'NumMean, pointwise small-prime bound, canonical large-prime mean and nonnegativity')],
 'compatibility': [
  (C+'StdSubAtOfRing.lean', 21, 89, 'Finite ring transport, exact GatIs, all five GroupCompatibilityAll fields and eventual family'),
  (C+'LinkGConcreteNoKer.lean', 13, 35, 'Actual standard-subring, finite-class/stabilizer and rational-descent consequences'),
  (L+'DataGatTies.lean', 7, 30, 'Actual rank, period, embeddings, positions and weights'),
  (L+'DataLatDefs.lean', 11, 53, 'Actual comparison lattice, independent basis, Vram and served preimage')],
 'slot_and_joint': [
  (G+'UnramifiedQuadraticSetting.lean', 85, 144, 'Signed lamAt/Ar and actual edge/midpoint coefficient definitions'),
  (G+'DataG.lean', 143, 199, 'Actual function lattices, ranks, neighbor operators and sandwich'),
  (G+'LatticeSystems.lean', 701, 724, 'Original three slots, RestLocChain and RestNat'),
  (G+'SelectionLemmas.lean', 16, 76, 'Ordered product ideal, exact tau, symmetric tails and original local conclusion'),
  (G+'FormalGroupSystem.lean', 802, 850, 'Both integral operators, full Conclusion6 and LemmaVVolumeGeneral normalization'),
  (G+'CornerGLContinuity.lean', 177, 205, 'Exact OrbitLatticeBounds, LatticeSandwich and saturation/smallness')],
 'local_growth': [
  (G+'IsResidueClassZero.lean', 330, 354, 'Exact integer Sv, tauP and ioP definitions'),
  (G+'IsResidueClassZero.lean', 410, 483, 'Complete LatInst/LatTied/yProd/NP and LatticeLengthsAtPlace definitions'),
  (G+'SmallOrderPrimes.lean', 199, 247, 'All unit bounds, complete admG1 and all twelve admitted fields'),
  (G+'PlaneCountTheoremWithConstants.lean', 1542, 1581, 'Actual ramified saturation and m>=1, x^-epsilon<=1/2 threshold'),
  (L+'DataLatDefs.lean', 111, 118, 'All three actual LatDefs fields, including unchanged atT')],
 'zero_chain': [
  (G+'DataGChain.lean', 30, 90, 'Complete Fills, Levels and Chain records and chainK composite'),
  (C+'AdmissibleFamilyNoKernel.lean', 166, 222, 'Literal zeroCh, vKge_zero and full admitted-family-no-kernel theorem'),
  (L+'DataDIVDefs.lean', 48, 56, 'NuDef has no chain variable'),
  (L+'DataExtra.lean', 41, 69, 'Extra.ker concerns original geometric chain and is not transported')],
 'admission': [
  (G+'SmallOrderPrimes.lean', 238, 269, 'TypePrimeSizeConds, complete admitted and exact AuxBlock8.AdmF quantifiers'),
  (G+'PlaneCountTheoremWithConstants.lean', 883, 939, 'All original Adm1F through Adm9F and family assembly choice order'),
  (S+'Conclusion1OfGainBoundAll.lean', 156, 161, 'Exact AdmFam contract, fixed constants before every delta'),
  (T+'GlobalSchurBounds/Chosen.lean', 15, 70, 'Actual selected tops and bad-top family predicates'),
  (T+'SmoothDesignExistence/AdmissibleTopsMertens.lean', 15, None, 'Full TopsF to Adm2F consumer on the same selected subset')],
 'global_endpoint': [
  (T+'GlobalTheoremInputs.lean', 97, 140, 'Original loG/flG and all FIVE LinkG_at conjuncts, full LinkG'),
  (G+'PlaneCountTheoremWithConstants.lean', 718, 878, 'Exact LinkG_at and same-family installation'),
  (C+'AdmissibleFamilyNoKernel.lean', 224, 289, 'Original no-kernel LinkG family and class-level endpoint'),
  (C+'LinkGConcreteNoKer.lean', 44, 56, 'Literal linkG_concrete_noKer and linkG_concrete5'),
  (T+'ParamsHeightRankConstant.lean', 112, 181, 'Actual coefficient lists, Large, Closed and pointwise maximum choice order')]
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
            id=f'LGS_{group}_{i:02}', path=path,
            line_start=lo, line_end=hi, declaration=title,
            file_sha256=sha(data), range_sha256=sha(block),
            range_bytes=len(block), source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{lo}-L{hi}')
        groups[group].append(item)
        inventory[path] = dict(path=path, sha256=sha(data), bytes=len(data),
                               line_count=len(lines),
                               verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{item["id"]}] {title}\n{item["url"]}\n'
                        f'Range SHA256: {sha(block)}\n{block.decode()}\n')

DEPS = {
 1: ['IW3', 'CB2', 'CR1'],
 2: ['LGS1'],
 3: ['GII1', 'GII2', 'GII3', 'GJ2', 'GJ3'],
 4: ['LFS2'],
 5: ['LGS3'],
 6: ['LGS3', 'LGS5', 'GI1', 'GI2', 'GI3', 'GI4', 'GI5',
     'GI6', 'GI7', 'GI8', 'GII4', 'GII5', 'GII6', 'GII7',
     'GII8', 'GJ1', 'GJ3'],
 7: ['LGS3', 'LGS6', 'GW1', 'GW2'],
 8: ['LGS1', 'CB2', 'CR1', 'CR2', 'CR3', 'CR4',
     'BC1', 'BC2', 'BC6', 'BC7', 'BC8', 'GLG13', 'GLG14'],
 9: ['LGS6', 'LGS8', 'BC6', 'BC7', 'GJ3', 'GJ4',
     'EL5', 'EL6', 'EL7', 'EL8', 'EL9', 'EL10',
     'JR1', 'JR4', 'JR5', 'JR6', 'JR7', 'JR12', 'LW4'],
 10: ['LGS2', 'LGS8', 'LGS9', 'LW1', 'LW2', 'LW3',
      'SR3', 'LC1', 'LC2'],
 11: ['LGS10'],
 12: ['LGS2', 'LGS3', 'LGS4', 'LGS5', 'LGS6', 'LGS11',
      'GLG1', 'GLG16'],
 13: ['LGS7', 'LGS8', 'LGS10', 'LGS11', 'LGS12',
      'GLG9', 'GLG10', 'GLG11', 'GLG12', 'GLG15', 'GLG17']
}
GROUPS = {
 1: ['model_sandwich'],
 2: ['family_data', 'model_sandwich'],
 3: ['family_data', 'orbit_sizes'],
 4: ['family_data', 'small_order'],
 5: ['family_data', 'orbit_sizes', 'power_bands'],
 6: ['family_data', 'local_certificates'],
 7: ['family_data', 'canonical_mean', 'local_certificates'],
 8: ['family_data', 'compatibility', 'slot_and_joint'],
 9: ['local_certificates', 'compatibility', 'slot_and_joint'],
 10: ['family_data', 'local_growth', 'slot_and_joint'],
 11: ['local_growth', 'zero_chain', 'global_endpoint'],
 12: ['family_data', 'admission', 'zero_chain'],
 13: ['family_data', 'global_endpoint', 'admission', 'zero_chain']
}
SCOPES = {
 1: 'Actual Hida-setting coefficient DVRs and original dominant polynomial lattices; signed determinant factors, both parities, empty basis intersections and nonlattice function convention distinguished.',
 2: 'Both literal adm9 fields at the actual ep=ceil(Ce*f*k^2*log_p(a)), Ce>=1; the lattice sandwich holds at all GIdx places, including p>a.',
 3: 'Original actual good orbits, all four adm1 fields, CN window guard and all adm5 inequalities; constant fixed before any positive auxiliary exponent.',
 4: 'Full actual Adm3F, with the original chosen hP and dyadic projection, all original primes, same power x^(-h+epsilon).',
 5: 'All five original ArchimedeanSignatureMatching fields, both original bands, one x^-1 threshold; endpoint integer and zero-width band included.',
 6: 'Full original Type-II adm6, attained universal canonical adm7, original adm8 at Cm=302114, and actual HypIAt/HypIIAt; fixed exact sufficient coefficient region.',
 7: 'Full MeanKappaBound for actual X, including arbitrary-degree pointwise small-prime clause; all indices and candidate primes share one threshold.',
 8: 'Original GroupCompatibilityFamily supplies actual finite classes, trivial stabilizers, finite free ranks, StdSubAt, NPDescF and original operator stability. The common record itself remains an input.',
 9: 'Actual served-coordinate LPprime with exact ceil(tv), Dp, kappav and cstar=8(Dp+1); all actual polynomial/orbit hypotheses of joint exceptional generation supplied.',
 10: 'First two original admG1 conjuncts on actual same lattices: depth inclusion and finite natural length <=vUnit(G)*G.d*(tauP+ioP); empty served set and exact ceilings retained.',
 11: 'Full original unit bounds and admG1 for auxiliary zeroCh; actual LatDefs, NP, lengths, Nu and all LinkG fields unchanged. Original Extra.ker and geometric theta chain are not transported.',
 12: 'Full original AuxBlock8.AdmF/AdmFam with C31=Corb,Ce=1,Cm=302114 before every delta>0 and one later threshold; common compatibility and selected TopsF/Adm2F retained.',
 13: 'All five original LinkG fields and literal Closed-class linkG_concrete5 implication with C_G=4*Ccount+1,delta=x^(-epsilon/2); actual compatibility and selected tops remain common-family antecedents.'
}
FOUNDATIONS = [
 dict(id='LGS_ORIGINAL_FAMILY_DATA', kind='explicit_original_data_and_guards',
      statement='The supplied original FamP with its actual params, all SizesAt fields, fixed constants, ep_def, kapI_def, fills, GatTies, LatTied, comparison, LatDefs, support and NuDef. This packet does not construct a new FamP or modify its geometric chain.',
      not_reconstructed_as_a_whole=True, source_groups=['family_data']),
 dict(id='LGS_COMPATIBILITY_ANTECEDENT', kind='explicit_original_common_record',
      statement='The actual GroupCompatibilityFamily: same Herm0, Forms0, CmpTied, all RingCompatibleAt maps and GatIs/HypAtP, with the original GatTies and actual comparison record. Its finite consumers are supplied; existence of this simultaneous record remains open.',
      not_reconstructed_as_a_whole=True, source_groups=['compatibility']),
 dict(id='LGS_SELECTED_TOPS_ANTECEDENT', kind='explicit_original_selected_subset',
      statement='The actual TopsF (ChosenTT and one ChosenBad constant) or the literal Adm2F on the given family. GLG16 supplies its exact finite harmonic consumer without resampling.',
      not_reconstructed_as_a_whole=True, source_groups=['admission']),
 dict(id='LGS_EXPLICIT_COEFFICIENT_REGION', kind='original_coefficient_choice_guard',
      statement='Exact sufficient original coefficient region (LGS.2), CN>=Corb(epsilon), all remaining coefficients nonnegative and fixed FamP fields unchanged. The final Closed statement chooses these bounds before the family and all later indices.',
      not_a_new_arithmetic_producer=True, source_groups=['family_data','global_endpoint']),
 dict(id='LGS_STANDARD_ALGEBRA_ANALYSIS', kind='standard_mathematical_background',
      statement='Finite polynomial/tensor linear algebra, finite sums, DVR elementary divisors and uniformizers, Nakayama for a finite module, and elementary power/logarithm limits. Their concrete local consumers and normalizations are written in the human proof or cited numbered human claims.',
      not_a_new_arithmetic_producer=True, source_groups=['model_sandwich','slot_and_joint','local_growth'])
]
EXT = {n: ['LGS_ORIGINAL_FAMILY_DATA', 'LGS_STANDARD_ALGEBRA_ANALYSIS']
       for n in range(1, 14)}
for n in [5, 6, 7, 8, 9, 10, 11, 12, 13]:
    EXT[n].append('LGS_EXPLICIT_COEFFICIENT_REGION')
for n in [8, 9, 10, 11, 12, 13]:
    EXT[n].append('LGS_COMPATIBILITY_ANTECEDENT')
for n in [12, 13]:
    EXT[n].append('LGS_SELECTED_TOPS_ANTECEDENT')

proof = (HERE/'main.tex').read_bytes()
text = proof.decode()
claims, blocks = [], {}
for n in range(1, 14):
    cid = f'LGS{n}'
    m = re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n', text, re.M|re.S)
    assert m, cid
    blocks[cid] = m.group()
    named = set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b', m.group())) - {cid}
    assert named <= set(DEPS[n]), (cid, 'unrecorded named references', named-set(DEPS[n]))
    assert all(not d.startswith('LGS') or int(d[3:]) < n for d in DEPS[n]), cid
    # Expand explicit ranges of inherited labels as well as their endpoints.
    for prefix, a, b in re.findall(r'\b([A-Z]{2,4})([0-9]+)--\1([0-9]+)\b', m.group()):
        if prefix == 'JR' and (a, b) == ('1', '12'):
            continue  # Historical description of the prior packet, not all its individual lemmas.
        needs = {f'{prefix}{j}' for j in range(int(a), int(b)+1)}
        assert needs <= set(DEPS[n]), (cid, 'unrecorded range dependency', needs-set(DEPS[n]))
    block = m.group().encode()
    title = re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n', m.group(), re.S).group(1)
    claims.append(dict(
        id=cid, title=title, introduced_in='0.47', classification='B',
        status='complete human proof at the explicitly stated original scope',
        depends_on=DEPS[n], external_input_ids=EXT[n], published_input_ids=[],
        hypotheses_retained=[SCOPES[n]], source_groups=GROUPS[n],
        sources=[s for group in GROUPS[n] for s in groups[group]],
        proof_location=dict(file=HERE.name+'/main.tex', label='claim:'+cid,
                            line_start=text[:m.start()].count('\n')+1,
                            line_end=text[:m.end()].count('\n'),
                            sha256=sha(block), bytes=len(block)),
        source_proof_is_not_human_proof=True))
claims[8]['dependency_scope_overrides'] = {
 'JR12': 'Actual coefficient-slot matching is supplied by EL5-EL10 here; the ending mention of JR1--JR12 describes the historical packet and does not invoke every intervening individual claim.',
 'LW4': 'All actual slot/edge premises formerly explicit there are now checked by EL and the same-model matching in LGS9.'}
claims[12]['dependency_scope_overrides'] = {
 'GLG17': 'All original local-growth, mean and full admission antecedents in this installer are discharged by LGS7-LGS12 on auxiliary Y0; common compatibility and actual selected tops remain explicit.',
 'GLG15': 'Consumed on the same original comparison/LatDefs and the exactly unchanged NP; normalization vUnit(G) is retained.'}

owners = {n: cid for cid, block in blocks.items()
          for n in re.findall(r'\\tag\{LGS\.(\d+)\}', block)}
for claim in claims:
    cid = claim['id']
    refs = set(re.findall(r'LGS\.(\d+)', blocks[cid])) - set(
        re.findall(r'\\tag\{LGS\.(\d+)\}', blocks[cid]))
    needed = {owners[n] for n in refs if n in owners and owners[n] != cid}
    assert needed <= set(claim['depends_on']), (cid, 'unrecorded formula references', needed)

# Old immutable chapters sometimes have whole-chapter or legacy path locators.
# Record their actual bytes without altering any old provenance record.
legacy_paths = {
 'EL': 'edge_lattices/edge_lattices_section.tex',
 'JR': 'joint_rank/joint_rank_section.tex',
 'LW': 'walk/walk_section.tex',
 'LC': 'local_accounting/local_accounting.tex',
 'SR': 'saturation/saturation_section.tex'}
ledger = {r['id']: r for r in json.loads((ROOT/'provenance.json').read_text())['claims']}
human_ids = sorted({d for deps in DEPS.values() for d in deps if not d.startswith('LGS')})
inherited = []
for cid in human_ids:
    record = ledger[cid]
    prefix = re.match(r'[A-Z]+', cid).group()
    loc = record.get('proof_location')
    if not isinstance(loc, dict) or not (ROOT/loc.get('file', '')).is_file():
        loc = {'file': legacy_paths[prefix]}
    path = ROOT/loc['file']
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    if 'line_start' in loc:
        lo, hi = loc['line_start'], loc['line_end']
        block = b''.join(lines[lo-1:hi])
        assert sha(block) == loc['sha256'], cid
        binding = 'exact previously recorded numbered-claim byte range'
    else:
        lo, hi, block = 1, len(lines), data
        # Consecutive legacy labels may be printed jointly as EL3--EL4 etc.
        found = re.search(r'\b'+cid+r'\b', data.decode()) is not None
        if not found:
            for pref, a, b in re.findall(r'\b([A-Z]+)(\d+)--\1(\d+)\b', data.decode()):
                found |= pref == prefix and int(a) <= int(cid[len(prefix):]) <= int(b)
        assert found, (cid, path)
        binding = 'entire immutable legacy chapter containing the named human claim'
    inherited.append(dict(
        id=cid, file=str(path.relative_to(ROOT)), main_tex_sha256=sha(data),
        block_sha256=sha(block), line_start=lo, line_end=hi,
        binding_scope=binding, kind='numbered_human_proof_dependency',
        not_an_external_foundation=True))
assert not set(human_ids) & {f['id'] for f in FOUNDATIONS}

reviews = []
lookup = {c['id']: c for c in claims}
for path in sorted(HERE.glob('review_*.json')):
    review = json.loads(path.read_text())
    assert review.get('result', review.get('status')) == 'PASS', path
    bound = review.get('proof_sha256', review.get('proof_file_sha256', review.get('main_tex_sha256')))
    assert bound == sha(proof), (path, bound, sha(proof))
    for checked in review.get('claims_reviewed', []):
        if isinstance(checked, dict):
            assert checked['result'] == 'PASS', checked
            assert checked['block_sha256'] == lookup[checked['id']]['proof_location']['sha256'], checked
    reviews.append(dict(file=str(path.relative_to(ROOT)), sha256=sha(path.read_bytes())))

completed = [
 'Actual ModelSandwichG/WeylSandwichG at every original Hida coefficient setting (LGS1)',
 'Full actual adm9/Adm9F and exact exponent sum, with fixed original Ce=1 (LGS2)',
 'Full original Adm1F, FamilyWindowLogBound and Adm5F at unchanged constants (LGS3)',
 'Literal actual dyadic small-order Adm3F (LGS4)',
 'All five original power-band/ArchimedeanSignatureMatching fields and Adm4F (LGS5)',
 'Actual full adm6/adm7/adm8 and HypIAt/HypIIAt from completed quantitative local theorems (LGS6)',
 'Full actual canonical MeanKappaBound, including pointwise small-prime clause (LGS7)',
 'Actual finite-class/freeness/standard-ring/rational-descent consequences of the original common record (LGS8)',
 'Actual served LPprime and joint exceptional-generator supplier, with all polynomial/orbit premises verified (LGS9)',
 'First two original admG1 fields, including finite integer length and exact vUnit*d*(tauP+ioP) (LGS10)',
 'Full admG1 and unit bounds for zeroCh with complete record invariance checked (LGS11)',
 'Full original AuxBlock8.AdmF/AdmFam, all twelve fields, constants before every delta (LGS12)',
 'Literal all-five-fields LinkG and original Closed-class linkG_concrete5 implication (LGS13)'
]
coverage = {
 'ModelSandwichG': 'LGS1', 'WeylSandwichG': 'LGS1',
 'ExpBoundG': 'LGS2', 'Adm1F': 'LGS3',
 'Adm2F': 'GLG16, from retained actual TopsF, or supplied directly',
 'Adm3F': 'LGS4', 'Adm4F': 'LGS5', 'Adm5F': 'LGS3',
 'Adm6F': 'LGS6', 'Adm7F': 'LGS6', 'Adm8F': 'LGS6',
 'Adm9F': 'LGS2',
 'MeanKappaBound.all_original_fields': 'LGS7',
 'TrivialStabiliserFiniteClasses': 'LGS8, from actual GroupCompatibilityFamily',
 'StdSubAt': 'LGS8, from actual GroupCompatibilityFamily',
 'NPDescF': 'LGS8/GLG14, from actual GroupCompatibilityFamily',
 'OrbitLatticeBounds': 'LGS9',
 'admG1.inclusion': 'LGS10',
 'admG1.finite_length_and_exact_bound': 'LGS10',
 'admG1.valuation': 'LGS11, for auxiliary zeroCh only',
 'unitBoundAtTwistedPlaces': 'LGS11, for auxiliary zeroCh only',
 'UnitBoundDifferenceTerm': 'LGS11, for auxiliary zeroCh only',
 'AuxBlock8.AdmF': 'LGS12, actual X and auxiliary zeroCh, retaining compatibility and actual TopsF/Adm2F',
 'LinkG_at.all_five_fields': 'LGS13',
 'linkG_concrete5': 'LGS13, exact original Closed-class implication',
 'GroupCompatibilityFamily.existence': 'explicit retained original producer',
 'Extra.ker_for_original_geometric_chain': 'unchanged; no new estimate or transport claimed'
}
traps = [
 'Global chain length m is distinct from local polynomial rank k-1.',
 'Same original FamP, same selected subset/degrees, same coefficient DVRs, same actual M/Mna/NP/Nu; no independent witness assembly.',
 'Model intersections on nonlattice input are ambient; equivariant function modules separately impose zero off actual lattice tuples.',
 'Exact ep=ceil(Ce*f*k^2*log_p(a)), Ce=1 in the actual family; the lattice sandwich holds even for p>a.',
 'Actual chosen hP is compared to dyadic Frobenius before the finite small-order bound is applied.',
 'Original canonical infimum kapI is used universally over coefficient settings; no separately selected function replaces it.',
 'MeanKappaBound retains both its local-average and every-degree small-prime clauses.',
 'Exact t=ceil(tv), D=Dp, kappa=kappav, cstar=8*(Dp+1), Sv integer and tauP already integral; no ceiling loss omitted.',
 'Finite length uses full original G.d and vUnit(G)=vO(p), and normalized descent cancels the same ramification factor.',
 'zeroCh changes only an auxiliary LatInst.Ch. Extra.ker/geometric theta maps are neither replaced nor claimed to obey a new lower valuation estimate.',
 'Every one of the twelve admitted fields holds before applying counting; C31,Ce,Cm precede every auxiliary delta and all later x,i.',
 'One Closed-class coefficient bound is chosen before every family and height parameter; same-family GroupCompatibilityFamily and TopsF/Adm2F remain explicit.'
]
frontier = [
 'Construct the actual GroupCompatibilityFamily on the chosen common family: all five Herm0/Forms0/CmpTied/ring/GatIs fields with the same comparison, level and GatTies. LGS does not infer it from separate adelic or abstract models.',
 'Supply the actual selected TopsF/Adm2F on that same family when not already available from its selected-top construction; no independent random subset is substituted.',
 'The other original denominator, retained-defect, period-height and spectral producers remain separate. No whole GLOBAL_LOCAL_GAIN closure is asserted.'
]
contracts = dict(
    schema='rh-local-growth-suppliers-contracts/1', artifact_version='0.47',
    component=HERE.name, source_commit=PIN, proof_file_sha256=sha(proof),
    endpoint_claim='LGS13', actual_first_growth_endpoint='LGS10',
    canonical_mean_endpoint='LGS7', full_admission_endpoint='LGS12',
    original_endpoint='Formalism.L2.G.linkG_concrete5',
    completed_original_substatements=completed, original_field_coverage=coverage,
    exact_guards_preserved=traps, remaining_actual_producers=frontier,
    human_dependency_ids=human_ids, external_input_ids=[f['id'] for f in FOUNDATIONS],
    selected_consumer_only=False, all_original_LinkG_fields=True,
    auxiliary_zero_chain_only=True, original_Extra_ker_unchanged=True,
    whole_obligation_closures=[], proposed_whole_obligation_closures=[],
    no_lean_replay=True,
    not_claimed=['construction of GroupCompatibilityFamily',
                 'new bounds for the actual geometric theta chain',
                 'replacement or modification of the original FamP',
                 'unconditional whole GLOBAL_LOCAL_GAIN',
                 'complete RH or GRH'])
prov = dict(
    schema='rh-human-component-provenance/1', artifact_version='0.47',
    date='2026-11-23', component=HERE.name, source_commit=PIN,
    main_tex_sha256=sha(proof), proof_file_sha256=sha(proof),
    claims=claims, source_groups=groups, source_inventory=list(inventory.values()),
    source_files=list(inventory), published_applications=[],
    retained_foundations=FOUNDATIONS, inherited_human_inputs=inherited,
    independent_reviews=reviews,
    builder=dict(file='build_metadata.py', sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,
                    all_source_bytes_compared_to_pinned_git_blobs=True,
                    claim_blocks=len(claims), direct_named_claim_dependencies_checked=True,
                    numbered_range_dependencies_checked=True,
                    numbered_formula_dependencies_checked=True,
                    external_foundations_separate_from_claim_DAG=True,
                    whole_original_leaf_closures=[]),
    scope_note='Actual local projection/joint/service/mean/admission suppliers and exact zero-chain consumer. Only the original common compatibility and selected-top producer remain at the final LinkG implication; no whole selected-leaf closure.')
closure = dict(
    schema='rh-human-component-closure/1', artifact_version='0.47',
    component=HERE.name, proof_file_sha256=sha(proof),
    new_claims=[c['id'] for c in claims], new_claim_count=len(claims),
    completed_original_substatements=completed,
    whole_obligation_closures=[], proposed_whole_obligation_closures=[],
    remaining_actual_producers=frontier,
    status='Complete local-growth, canonical-mean and full auxiliary-admission suppliers from the original common data; full literal LinkG implication; no whole selected-leaf closure.',
    exact_error_and_constants_preserved=True, all_five_LinkG_fields=True,
    actual_GatTies_LatDefs_ranks_DVR_preserved=True,
    full_admission_produced=True, mean_input_produced=True,
    local_first_growth_produced=True, auxiliary_zero_chain_only=True,
    original_geometric_chain_unchanged=True,
    actual_compatibility_retained=True, actual_selected_tops_retained=True,
    no_lean_replay=True)
outputs = {
 'provenance.json': prov, 'contracts.json': contracts, 'closure.json': closure,
 'source_manifest.json': dict(schema='rh-source-manifest/1',
     component=HERE.name, source_commit=PIN, source_files=list(inventory.values()),
     ranges=groups, verified_against_git=True),
 'retained_foundations.json': FOUNDATIONS, 'published_inputs.json': []}
for name, value in outputs.items():
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 'ACTUAL LOCAL GROWTH, FULL ADMISSION AND CANONICAL MEAN — v0.47\n'
 f'Source pin: {PIN}\nMain SHA256: {sha(proof)}\n\n'
 f'{len(claims)} numbered human proofs, classification B; {len(inventory)} pinned source files; '
 f'{sum(map(len, groups.values()))} source ranges; {len(inherited)} inherited numbered proof bindings.\n\n'
 'The v0.46 full LinkG installer retained full admitted data, first growth and the canonical mean. '
 'This chapter supplies those actual inputs at the original sufficient coefficient bounds, while '
 'keeping the simultaneous GroupCompatibilityFamily and the selected-top condition explicit.\n\n'
 'LGS1–5 prove the actual integral polynomial sandwich and its original exponent budget, exact '
 'orbit/window hypotheses, actual dyadic small-order prime bound and both full power-band estimates. '
 'All constants, parities and the chosen Frobenius are retained. LGS6–7 match the previously completed '
 'Type-I/II theorems to the actual canonical infimum and derive both clauses of MeanKappaBound, '
 'including the pointwise small-prime bound for every degree assignment.\n\n'
 'LGS8–10 use the retained common record to obtain actual class sets, trivial stabilizers, coefficient '
 'maps and rational descent, and then verify every physical hypothesis of the joint tensor/walk '
 'argument. The output is the original first-growth inclusion and finite natural length at '
 'vUnit(G)*G.d*(tauP+ioP), with original ceilings and empty-served cases included. This is a supply '
 'of the actual model inputs, not an abstract lattice-system assumption.\n\n'
 'LGS11 checks the complete auxiliary zeroCh route. Only LatInst.Ch is changed. LatTied, actual '
 'NP, ramified intersection, every LatDefs field, actual Nu and all five LinkG outputs are unchanged. '
 'The larger Extra.ker field remains attached to the original geometric theta chain and is not '
 'transported. The zero auxiliary composite supplies precisely the valuation clauses used by '
 'the counting consumer. LGS12 then supplies all twelve original admitted fields, with '
 'C31=Corb(epsilon), Ce=1, Cm=302114 fixed before every delta>0 and later family threshold.\n\n'
 'LGS13 gives the full literal LinkG and Closed-class linkG_concrete5 implication. The error remains '
 'b^(x^(-epsilon/2)); C_G=4*Ccount+1. Every field uses the same original family/member/lattices. '
 'The original common compatibility record and selected-top input remain explicit; no whole '
 'GLOBAL_LOCAL_GAIN leaf is closed.\n\nRemaining actual producers:\n'
 + ''.join('- '+item+'\n' for item in frontier)
 + '\nThe builder checks every source range against the immutable git blob, binds every numbered '
 'human dependency separately from original antecedents/foundations, expands printed dependency '
 'ranges, and records complete proof-block hashes. No Lean replay, formal proof recertification, '
 'shared-ledger modification, or frozen proof edit is performed.\n')
hashes = {p.name: sha(p.read_bytes()) for p in sorted(HERE.iterdir())
          if p.is_file() and p.name != 'hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(
    dict(component=HERE.name, artifact_version='0.47', hashes=hashes), indent=2)+'\n')
print(json.dumps(dict(
    claims=len(claims), source_files=len(inventory),
    source_ranges=sum(map(len, groups.values())), inherited_claims=len(inherited),
    main_tex_sha256=sha(proof), actual_growth_endpoint='LGS10',
    full_admission_endpoint='LGS12', final_endpoint='LGS13',
    whole_original_leaf_closures=[]), indent=2))
