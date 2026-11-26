#!/usr/bin/env python3
"""Bind the AOS human proofs to exact pinned source scopes; no Lean replay."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.54'
COMPONENT = HERE.name
SNAPSHOT = HERE / 'source_snapshot'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
A = 'src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/ArchimedeanOrbitMeasures/'
M = 'src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/MassComputations/'
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
C = 'src/Formalism/SharpRestriction/CuspSpanNormBounds/'
D = 'src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'
GMV = 'src/Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean'
NC = S + 'CokernelGLCounts/RankPointCounts/DualFamilyCounting/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def f(prefix, name, first=None, last=None):
    return (prefix + name + '.lean', first, last)

groups = {
    'pairings_and_selfdual': [
        (GMV, 52, 81), (GMV, 125, 192), (GMV, 346, 370),
        f(A, 'SdTestC', 12, 62),
        f(A, 'MuBridgeA', 17, 110), f(A, 'MuBridgeA', 135, 169),
        f(A, 'MuBridgeB', 56, 65), f(A, 'MuBridgeB', 118, 169),
        f(A, 'NuBridge', 68, 254),
    ],
    'linear_jacobian': [
        f(A, 'TupPlace', 13, 25), f(A, 'PlaceJacHolds', 155, 198),
        f(A, 'PlaceJacHolds', 200, None),
    ],
    'gram_chart': [
        f(A, 'SquareChartC1Local', 13, 177), f(A, 'JacGlue', 15, 50),
        f(A, 'PolarLocalOfAction', 15, 28),
    ],
    'gauge': [
        f(C, 'RelevantZeroGramTerms', 382, 392), f(C, 'SGauge', 13, 37),
    ],
    'compact_unitary_volume': [
        f(A, 'GaugeVolU', 8, 9),
        f(C, 'CongruenceAtSplitFrobeniusHolds', 387, 387),
        f(D, 'RiemannianHaarGaugeVolumeUnitaryGroupEq', 51, None),
        f(A, 'GrpHaarW', 13, 52),
    ],
    'orbit_density': [
        f(A, 'GrpHaarW', 54, 209), f(A, 'GrpDens', 14, 25),
        f(A, 'HaarUniqInfHolds', 15, 54),
        f(A, 'ExistsOrthonormalPerp', 196, 331),
    ],
    'actual_frame': [
        ('src/Formalism/LocalRingCardinality/Params.lean', 6, 44),
        f(S + 'HaarTransversals/', 'HidaSetting', 179, 219),
        f(A, 'DetNZHolds', 12, 49), f(A, 'DetTHolds', 14, 67),
        f(A, 'PerpPosV', 21, 75),
        f(S + 'HaarTransversals/UnitaryHaarProducts/', 'InHHDef', 262, 276),
        f(S + 'ClosedLocalOrbits/', 'RealObj', 96, 96),
        f(S + 'ClosedLocalOrbits/GaugeLatticeShifts/', 'ProductExactness', 206, 210),
        f(M, 'StrongApproxN', 32, 34),
    ],
    'actual_bridge_and_hypotheses': [
        f(S + 'HaarTransversals/', 'HidaSetting', 365, 377),
        f(C, 'GaugeVolumeBound', 15, 19),
        f(A, 'StdConjExOfWitt', 47, 107),
        f(A, 'StdConjExOfWitt', 109, 159),
        f(A, 'BridgeC', 12, 71),
        f(S + 'CokernelGLCounts/', 'MassDataInst', 229, 231),
    ],
    'push_and_positive_test': [
        f(A, 'AinfValueOf', 12, 48),
        f(A, 'PushCut', 18, 28), f(A, 'PushCut', 68, 89),
        f(A, 'ConstCut', 86, 167), f(A, 'ConstFin', 9, 19),
    ],
    'existence': [f(A, 'AinfValueOf', 23, 33), f(A, 'ExInfHolds', 12, 21)],
    'actual_stabilizer_mass': [
        f(A, 'AinfValueOf', 61, 64), f(A, 'GinfTestHolds', 30, 43),
        f(M, 'StrongApproxN', 67, 69), f(M, 'ContinuousSplitA', 64, 80),
    ],
    'all_section_formula': [
        f(A, 'AinfValueOf', 50, 59), f(A, 'WeilInfOf', 14, 32),
        f(A, 'LintegralMulRightOfMem', 232, 305),
    ],
    'exact_scalar_endpoint': [
        f(NC, 'NcReal', 15, 31), f(A, 'ClauseUnique', 17, 37),
        f(A, 'ClauseUnique', 39, 83), f(A, 'AinfValueOf', 66, 75),
        f(A, 'GinfTestHolds', 13, 28), f(A, 'AprimeInfOfLeaves', 9, 24),
        f(NC, 'NcRealPf', 109, 116),
    ],
    'next_consumers': [
        f(NC, 'NcReal', 33, 46), f(NC, 'NcRealPf', 124, 217),
        f(S + 'CokernelGLCounts/', 'MassDataInst', 257, 287),
    ],
}

assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == PIN
files = {}
for path in sorted({x[0] for entries in groups.values() for x in entries}):
    data = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
    assert (REPO / path).read_bytes() == data, path
    target = SNAPSHOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    files[path] = {
        'path': path, 'snapshot_path': str(target.relative_to(WORK)),
        'source_commit': PIN, 'sha256': sha(data), 'bytes': len(data),
        'line_count': len(data.splitlines(keepends=True)), 'url': URL + path,
        'verified_equal_to_pinned_git_blob': True,
    }
source_groups = {}
for group, entries in groups.items():
    source_groups[group] = []
    for number, (path, first, last) in enumerate(entries, 1):
        lines = (SNAPSHOT / path).read_bytes().splitlines(keepends=True)
        first, last = first or 1, last or len(lines)
        assert 1 <= first <= last <= len(lines), (path, first, last, len(lines))
        selected = b''.join(lines[first - 1:last])
        source_groups[group].append({
            'id': f'AOS_{group}_{number:02d}', 'path': path,
            'line_start': first, 'line_end': last,
            'declaration': 'Literal original contract or producer calculation; complete source file retained for context',
            'file_sha256': files[path]['sha256'], 'range_sha256': sha(selected),
            'range_bytes': len(selected), 'source_commit': PIN,
            'verified_equal_to_pinned_git_blob': True,
            'url': URL + path + f'#L{first}-L{last}',
        })

# Own dependencies, source groups, inherited dependencies, literal scope.
specs = [
 (1, 'Exact infinite-place pairings and every self-dual density', [], ['pairings_and_selfdual','actual_bridge_and_hypotheses'], ['GMR2'], 'All supplied CM coordinates and matrices P; every SdW/SdHerm witness for the original standard character; exact tuple factor 2^(nad) and Frobenius Hermitian measure.'),
 (2, 'Two determinant identities in arbitrary complex matrix dimensions', [], ['linear_jacobian'], [], 'All invertible complex B, arbitrary row number, Hermitian congruence, including zero dimensions.'),
 (3, 'Full original PlaceJac', [2], ['linear_jacobian'], [], 'Every n,m,sign function,S,w and arbitrary finite coordinate spaces L,H with the original isometry/onto hypotheses; no positivity of S imposed.'),
 (4, 'Nondegenerate Gram chart and exact pointwise fiber density', [1,3], ['gram_chart','linear_jacobian'], ['GMR4','GMR5'], 'Indefinite as well as definite nondegenerate T; all permitted continuous fiber-family witnesses; density at the actual base point.'),
 (5, 'Prescribed Haar density and full universal GaugeDens', [], ['gauge'], [], 'Every n and sign function, any positive Haar normalization; literal gLie/expSet/ratioAt/limUnder definitions; source gauge is the exact Frobenius Haar scalar.'),
 (6, 'Full original GaugeVolU with the exact source product', [5], ['compact_unitary_volume'], [], 'Every k including zero; original muGauge, product of (2*pi)^j/(j-1)!; no probability normalization substituted.'),
 (7, 'Exact local orbit density and invariant Radon uniqueness', [4,5,6], ['orbit_density','compact_unitary_volume'], ['GMR11'], 'Actual block compact stabilizer, any prescribed Haar scalar; full compact fiber volume, proper map and invariant Radon measure uniqueness.'),
 (8, 'Exact one-place orbital pushforward for every fiber witness', [4,7], ['orbit_density','gram_chart','linear_jacobian'], ['GMR4','GMR5','GMR10','GMR14'], 'Every nondegenerate tuple with positive k-dimensional complement; actual group Haar; full invariant fiber; unimodularity proved over the real field.'),
 (9, 'Source determinant, positivity of the complement and full HinfCompact', [], ['actual_frame','actual_bridge_and_hypotheses'], [], 'Every original datum, HidaSetting and word; no measure, character or gauge assumptions for compactness; Tw and supplied frame unchanged.'),
 (10, 'Full finite-product fiber identity at every parameter', [1,7], ['pairings_and_selfdual','gram_chart'], ['GMR2','GMR3','GMR4','GMR5'], 'Every global self-dual pair and every fiber family, including singular independent fibers; finite product, no restricted-product assumption.'),
 (11, 'Full original PushInf with literal KVal', [1,5,8,9,10], ['push_and_positive_test','actual_bridge_and_hypotheses'], [], 'All original X,hb,sets,words,psi,HypX,MeasCompat,IsStdChar,GaugeDens,hT,self-dual and fiber witnesses; same infinity measures.'),
 (12, 'Full original ConstTest with a positive finite continuous test', [4,9,11], ['push_and_positive_test'], ['GMR4'], 'Every original PushHyp including its existential supplied bridge; exact equality and strictly positive finite fiber integral.'),
 (13, 'Full original ExInf in its nested witness order', [1,10], ['existence','pairings_and_selfdual'], ['GMR2','GMR4'], 'Original HypX/MeasCompat/IsStdChar; every self-dual pair admits a full IsFibreFamily on the entire Hermitian parameter space; no GaugeDens needed.'),
 (14, 'Full original HtotInf for the unchanged stabilizer Haar measure', [9], ['actual_stabilizer_mass','actual_bridge_and_hypotheses'], [], 'Original HypX; exact original ambient muH total equals actual muHinf total; positive and finite without probability rescaling.'),
 (15, 'Compact-stabilizer formula for every section', [], ['all_section_formula'], [], 'Locally compact second countable bi-Haar G, compact H with local quotient sections, arbitrary H Haar; all nonnegative measurable f and every section, even nonmeasurable.'),
 (16, 'Full original WeilInf', [4,8,9,14,15], ['all_section_formula'], [], 'Every original HypX, nonnegative measurable f and arbitrary source section; actual muGinf and muHinf; no self-dual/fiber choice required.'),
 (17, 'Full original AinfValue and its all-witness integration clause', [11,13,14,16], ['exact_scalar_endpoint'], [], 'All original antecedents and hT; full nested AllSome, every test/section, literal KVal divided by the old stabilizer mass.'),
 (18, 'Full original AprimeInf and GinfTest', [13,17], ['exact_scalar_endpoint'], [], 'Every original positive a-prime satisfying AinfClause has the exact original value; same chosen witnesses and test for comparison. GinfTest itself needs HypX alone.'),
]
main = (HERE / 'main.tex').read_bytes()
lines = main.decode().splitlines(keepends=True)
old_claims = {}
if (HERE / 'provenance.json').exists():
    old_claims = {c['id']: c for c in json.loads((HERE / 'provenance.json').read_text())['claims']}
claims = []
for number, title, own, names, inherited_ids, scope in specs:
    identifier = f'AOS{number}'
    first = next(i for i, l in enumerate(lines, 1) if l.strip() == '% BEGIN ' + identifier)
    last = next(i for i, l in enumerate(lines, 1) if l.strip() == '% END ' + identifier)
    proof = ''.join(lines[first - 1:last]).encode()
    assert b'\\begin{proof}' in proof and b'\\end{proof}' in proof
    old = old_claims.get(identifier, {})
    status = 'complete human proof at the explicitly stated scope; awaiting independent review'
    if old.get('proof_location', {}).get('sha256') == sha(proof):
        status = old.get('status', status)
    claims.append({
        'id': identifier, 'title': title, 'introduced_in': VERSION, 'classification': 'B',
        'status': status, 'depends_on': [f'AOS{i}' for i in own] + inherited_ids,
        'external_input_ids': ['AOS_CLASSICAL_BACKGROUND'], 'published_input_ids': [],
        'scope_note': scope, 'source_groups': names,
        'sources': [e for name in names for e in source_groups[name]],
        'proof_location': {'file': COMPONENT + '/main.tex', 'label': 'claim:' + identifier,
            'line_start': first, 'line_end': last, 'sha256': sha(proof), 'bytes': len(proof)},
        'source_proof_is_not_human_proof': True, 'whole_obligation_closure': False,
    })

inherited_components = {
    'global_measure_rescaling_v53': ['GMR2','GMR3','GMR4','GMR5','GMR10','GMR11','GMR14','GMR19'],
}
inherited, inherited_ids = [], set()
for component, identifiers in inherited_components.items():
    data = (WORK / component / 'main.tex').read_bytes()
    oldlines = data.splitlines(keepends=True)
    index = {c['id']: c for c in json.loads((WORK / component / 'provenance.json').read_text())['claims']}
    bindings = []
    for identifier in identifiers:
        loc = index[identifier]['proof_location']
        first, last = loc['line_start'], loc['line_end']
        selected = b''.join(oldlines[first - 1:last])
        assert loc.get('sha256', loc.get('paragraph_sha256')) == sha(selected), identifier
        bindings.append({'id': identifier, 'file': component + '/main.tex',
            'line_start': first, 'line_end': last, 'sha256': sha(selected), 'bytes': len(selected),
            'scope': index[identifier].get('scope_note', index[identifier].get('title'))})
        inherited_ids.add(identifier)
    inherited.append({'component': component, 'claims': identifiers, 'file': component + '/main.tex',
        'sha256': sha(data), 'proof_hashes': {b['id']: b['sha256'] for b in bindings}, 'claim_bindings': bindings})
known = {c['id'] for c in claims} | inherited_ids
assert all(d in known for c in claims for d in c['depends_on'])
assert len(claims) == 18

inputs = [
 {'id': 'AOS_CLASSICAL_BACKGROUND', 'status': 'ordinary mathematical background retained',
  'content': 'Finite-dimensional real/complex linear algebra, singular-value decomposition and Sylvester inertia; matrix power series, inverse function theorem and smooth change of variables; Haar existence/uniqueness, Radon regularity, Fubini/Tonelli, compactly supported partitions of unity, dominated convergence and the elementary Gaussian integral. Exact self-dual/fiber uniqueness is inherited from GMR2--5. The actual Jacobian, gauge density, compact unitary volume, orbital scalar and all-section normalization are proved here, not assumed.'},
 {'id': 'AOS_SUPPLIED_SETTING_SCOPE', 'status': 'given original data, not newly manufactured setting existence',
  'content': 'Every supplied original D7, HidaSetting X, AdBridgeIso hb, FdN/FdN-prime and words. HypX is exactly MeasTie, LevelSubgroupNormalized and the two specified IsSFund clauses. No Forms0 existence, all-family Transport or LevelMatch producer is inferred.'},
 {'id': 'AOS_ORIGINAL_CHARACTER_SCOPE', 'status': 'literal original antecedents retained',
  'content': 'The same original psi satisfying MeasCompat-psi and IsStdChar is used throughout. On the rescaled setting it is the character supplied once by GMR19 before all later words, places and tuples. No character or infinity measure is selected again.'},
 {'id': 'AOS_ORIGINAL_GAUGE_SCOPE', 'status': 'literal original antecedent retained in endpoint statements and fully supplied by AOS5',
  'content': 'Original PushInf, AinfValue and AprimeInf quantify GaugeDens at every real place. AOS5 proves full GaugeDens for every dimension and sign function, from the literal small-exponential-ball limit; this premise is not an unproved analytic boundary.'},
 {'id': 'AOS_UPSTREAM_SIEGEL_WEIL_SCOPE', 'status': 'upstream original boundary retained; not used to calculate the archimedean scalar',
  'content': 'GMR19 keeps exact SiegelWeilUnitaryConvergent in its original RescaleStep3 statement. This chapter neither reconstructs its arithmetic theta mean nor eliminates it from that upstream statement. Finite-place and arithmetic quotient-volume comparisons remain separate.'},
]
manifest = {'schema': 'rh-source-manifest/1', 'artifact_version': VERSION, 'component': COMPONENT,
    'source_commit': PIN, 'snapshot_root': str(SNAPSHOT.relative_to(WORK)),
    'checkout_head_verified': True, 'source_files': list(files.values()), 'total_files': len(files),
    'total_bytes': sum(f['bytes'] for f in files.values()),
    'distinct_source_ranges': len({(r['path'], r['line_start'], r['line_end']) for g in source_groups.values() for r in g}),
    'all_verified_equal_to_pinned_git_blob': True, 'no_lean_replay': True,
    'source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof': True}
validation = json.loads((HERE / 'tex_validation.json').read_text())
assert validation['proof_file_sha256'] == sha(main) and validation['status'] == 'PASS'
reviews = [{'file': str(p.relative_to(WORK)), 'sha256': sha(p.read_bytes()), 'content': json.loads(p.read_text())}
           for p in sorted(HERE.glob('independent_review*.json'))]
for review in reviews:
    value = review['content']
    bound = value.get('proof_file_sha256', value.get('main_tex_sha256'))
    assert not bound or bound == sha(main), review['file']
dump('source_manifest.json', manifest)
dump('inherited_inputs.json', {'schema': 'rh-inherited-human-inputs/1', 'artifact_version': VERSION,
    'component': COMPONENT, 'proof_file_sha256': sha(main), 'components': inherited,
    'all_current_proof_ranges_verified': True})
dump('classical_inputs.json', {'schema': 'rh-explicit-inputs/1', 'component': COMPONENT, 'inputs': inputs,
    'new_unreconstructed_published_mathematical_premises': []})
dump('retained_inputs.json', {'schema': 'rh-retained-inputs/1', 'artifact_version': VERSION,
    'component': COMPONENT, 'proof_file_sha256': sha(main), 'inputs': inputs,
    'no_unspecified_proportionality_constant': True, 'no_new_infinity_measure': True})
dump('provenance.json', {'schema': 'rh-human-component-provenance/1', 'artifact_version': VERSION,
    'date': '2026-11-23', 'component': COMPONENT, 'source_commit': PIN,
    'main_tex_sha256': sha(main), 'proof_file_sha256': sha(main), 'claims': claims,
    'source_groups': source_groups, 'source_files': list(files.values()), 'source_inventory': list(files.values()),
    'retained_foundations': inputs, 'inherited_human_inputs': inherited, 'independent_reviews': reviews,
    'builder': COMPONENT + '/build_metadata.py', 'validation': validation,
    'whole_obligation_closures': [], 'no_lean_replay': True})
completed = [
 'Full original PlaceJac for arbitrary finite isometric coordinate spaces',
 'Full universal GaugeDens from the literal source gauge definition',
 'Full original GaugeVolU with exact Frobenius normalization and volU product',
 'Full original HinfCompact for every supplied setting and word',
 'Full original PushInf with KVal and every self-dual/fiber witness',
 'Full original ConstTest with a strictly positive finite continuous compact test',
 'Full original ExInf in its nested AllSome order',
 'Full original HtotInf and exact unchanged stabilizer mass tie',
 'Full original WeilInf for every measurable nonnegative test and every section',
 'Full original AinfValue and AinfClause at the computed positive scalar',
 'Full original GinfTest and AprimeInf/AprimeInfS',
]
remaining = [
 'ProdExact and PlaceSplit/PlaceData needed by the remaining original RealBracket consumer',
 'Finite-place factors and InVolumesAt arithmetic quotient-volume comparisons',
 'Original SiegelWeilUnitaryConvergent arithmetic theta/volume premise upstream of RescaleStep3',
 'Ambient Forms0 and the distinct original all-family Transport/LevelMatch suppliers',
 'Bessel uniqueness/local ties, CountIdempotentsClass and the remaining global spectral identifications',
]
shared = [
 'Actual supplied X and hb; all nonmeasure fields and every MeasTie field',
 'One standard global psi before all words, places, self-dual choices and tuples',
 'Original muGinf, muNinf and muHinf, and old ambient muH total',
 'Literal source tuple order, Gram matrix, Tw and Hermitian witness',
 'Every self-dual/fiber witness and every section; no measurable-section assumption added',
]
dump('contracts.json', {'schema': 'rh-root-producer-contracts/1', 'artifact_version': VERSION,
    'component': COMPONENT, 'source_commit': PIN, 'proof_file_sha256': sha(main),
    'endpoint_claim': 'AOS18', 'primary_endpoint_claim': 'AOS11', 'positive_test_endpoint_claim': 'AOS12',
    'completed_original_substatements': completed,
    'remaining_exact_producers_for_PushInf': [], 'remaining_exact_producers_for_AprimeInf': [],
    'retained_original_premises': 'Original supplied data/HypX/MeasCompat-psi/IsStdChar. Original GaugeDens antecedents are retained in source-matching statements and supplied by AOS5.',
    'shared_data_preserved': shared, 'remaining_downstream_boundaries': remaining,
    'proposed_whole_obligation_closures': [], 'whole_obligation_closures': [], 'no_lean_replay': True})
dump('closure.json', {'schema': 'rh-component-closure/1', 'artifact_version': VERSION, 'component': COMPONENT,
    'proof_file_sha256': sha(main), 'human_claims': [c['id'] for c in claims],
    'fully_proved_claims_at_stated_scope': [c['id'] for c in claims],
    'completed_original_producer_contracts': completed, 'conditional_consequences': [],
    'remaining_source_producers_in_this_archimedean_scalar_chain': [],
    'remaining_downstream_boundaries': remaining, 'whole_obligation_closures': [],
    'all_sources_pinned': True, 'no_lean_replay': True})
dump('claim_dag.json', {'schema': 'rh-claim-dependency-dag/1', 'artifact_version': VERSION,
    'component': COMPONENT, 'proof_file_sha256': sha(main),
    'nodes': [{'id': c['id'], 'depends_on': c['depends_on']} for c in claims],
    'inherited_nodes': sorted(inherited_ids), 'all_dependencies_resolve': True})
(HERE / 'report.txt').write_text(f'''Exact archimedean orbital scalar, version {VERSION}
Pinned source: {PIN}
Main SHA-256: {sha(main)}

Eighteen complete human claims AOS1--AOS18; {len(main.decode().split())} TeX words.
Primary endpoint: full original PushInf, exact KVal, every original self-dual
and fiber witness. Full ConstTest is proved with a positive finite continuous
compact test. The chapter continues through ExInf, HinfCompact, HtotInf,
WeilInf, AinfValue/AinfClause and the full original AprimeInf scalar.

The direct calculation is explicit:
  tuple self-dual density = 2^(na) at each real place;
  Hermitian self-dual density = Frobenius volume;
  real Gram-chart determinant = 2^(-na) |det T|^k;
  fiber density at the base tuple = |det T|^k;
  orbit density = source gauge times volU(k);
  volU(k) = product(j=1..k) (2*pi)^j/(j-1)!;
  |det T| = Tw at each real place.
Thus KVal = gaugeU(X.B.I) * volU(k)^d * Tw^(-kd), with no unknown
scalar. AOS3 supplies full PlaceJac at arbitrary finite coordinate scopes;
AOS5 supplies universal GaugeDens; AOS6 supplies full GaugeVolU.

The supplied X, bridge, one character and infinity Haar measures remain
unchanged. All-section identities include nonmeasurable sections by equality
of their averaged functions on the orbit. The integration scalar is KVal
divided by the unchanged original stabilizer mass. The uniqueness proof
uses one common test, self-dual pair, fiber family and section for both clauses.

No arithmetic quotient-volume, finite-place, RealBracket, all-family Forms0,
Transport/LevelMatch, Bessel-uniqueness or CountIdempotentsClass producer is
inferred. GMR19's original SiegelWeilUnitaryConvergent premise is preserved.

Verification: {len(files)} pinned full source files and {manifest['distinct_source_ranges']}
exact ranges; {manifest['total_bytes']} source bytes; 18 proof blocks and
{len(inherited_ids)} inherited human blocks hash-bound. Two-pass draft TeX PASS
with zero errors, missing characters, undefined references or overfull boxes.
No PDF or Lean replay. Independent review is recorded separately at freeze.
''')
(HERE / 'README.txt').write_text('Read main.tex and contracts.json.\n'
    'Draft TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n'
    'Metadata: python build_metadata.py\nRead-only bindings: python verify_hashes.py\n')
print(json.dumps({'component': COMPONENT, 'claims': len(claims), 'main_sha256': sha(main),
    'source_files': len(files), 'source_ranges': manifest['distinct_source_ranges'],
    'source_bytes': manifest['total_bytes'], 'tex_status': validation['status'],
    'whole_obligation_closures': []}, indent=2))
