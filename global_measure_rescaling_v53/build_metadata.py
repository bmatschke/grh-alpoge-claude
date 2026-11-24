#!/usr/bin/env python3
"""Bind the GMR human proofs to pinned original scopes; never replay Lean."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.53'
COMPONENT = HERE.name
SNAPSHOT = HERE / 'source_snapshot'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
D = 'src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'
M = 'src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/StabilizerVolume/'
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
GMV = 'src/Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean'
VOL = 'src/Formalism/PeriodIntegrals/VolFromSW.lean'
SW = 'src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def f(prefix, name):
    return (prefix + name + '.lean', None, None)

groups = {
    'character': [
        (GMV, 228, 255),
        f(S + 'HaarTransversals/UnitaryHaarProducts/', 'StdChar'),
        (S + 'CokernelGLCounts/LocVol.lean', 42, 48),
    ],
    'selfdual': [
        (GMV, 125, 192), (GMV, 346, 370),
        f(M, 'SdUniq'),
        f(D, 'LocalSelfDualMeasuresFibreFamilyExist'),
        (S + 'CokernelGLCounts/LocVol.lean', 13, 60),
    ],
    'fiber_construction': [
        (GMV, 183, 190),
        f(D, 'ExistsGramFibreOfHaar'),
        f(D, 'ExistsFibreMeasuresArchimedeanGramMap'),
        f(D, 'LocalSelfDualMeasuresFibreFamilyExistStatement'),
        f(D, 'GramFibreMeasureFreeTupleNeZeroFinite'),
    ],
    'fiber_unique_covariant': [
        f(M, 'FibUniq'),
        f(D, 'GramMapFibreMeasureLocalUnitaryInvariant'),
        f(D, 'GramMapFibreMeasureUnitriangularInvariant'),
    ],
    'finite_counts': [f(M, 'LocDensFF'), f(M, 'LocDensFFAll')],
    'good_density': [f(M, 'DensAAOf'), f(M, 'HenselCountHolds'), f(M, 'LocDensSt')],
    'euler_product': [f(M, 'LocDensQ')],
    'global_fiber': [
        (VOL, 58, 81), f(M, 'RestrProdSt'), f(M, 'RestrProd'),
        f(M, 'RestrProdAlt'), f(M, 'ExOmTOfSteps'),
    ],
    'orbit': [
        f(M, 'OrbTupFin'), f(D, 'ExistsSmulLocalWittFreeTupleGram'),
        f(D, 'LocalUnitaryGroupTuplesTopologicalFacts'),
    ],
    'quotient': [
        (VOL, 83, 90), f(M, 'ExStabSt'),
        f(D, 'WeilIntegrationFormulaOrbitStatement'),
    ],
    'global_supplier': [
        f(D, 'ExistsAdelicTorusMeasureStabiliserHaarStatement'),
        f(D, 'ExistsAdelicTorusMeasureStabiliserHaar'),
    ],
    'local_supplier': [
        f(D, 'ExistsHaarFrameStabiliserCompatibleFibreStatement'),
        f(D, 'ExistsHaarFrameStabiliserCompatibleFibre'),
        (S + 'CokernelGLCounts/LocVol.lean', 251, 277),
    ],
    'unimodular': [
        f('src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/',
          'LocalUnitaryGroupStabilizersUnimodularFinitePlac'),
    ],
    'normalizer': [
        f(D, 'SimilitudeConjPreservesUnitaryHaarAtFinitePlaceStatement'),
        f(D, 'SimilitudeConjPreservesUnitaryHaarAtFinitePlace'),
    ],
    'upper_quotient': [
        (S + 'FundamentalEquivalence/LevelIntersectParabolic.lean', 14, 176),
        f(D, 'ExistsContinuousUnitriangularSectionStatement'),
        f(D, 'HaarFrameStabilizerLocalFixerSectionProduct'),
        f(D, 'HaarFrameStabilizerLocalFixerSectionProductStatement'),
    ],
    'local_tie': [
        f(D, 'ExistsFrameStabilizerHaarNormalisedFibreMeasureStatement'),
        f(D, 'ExistsFrameStabilizerHaarNormalisedFibreMeasure'),
        (S + 'CokernelGLCounts/LocVol.lean', 251, 277),
        (S + 'CokernelGLCounts/LocVol.lean', 449, 450),
    ],
    'actual_setting': [
        ('src/Formalism/LocalRingCardinality/Params.lean', 1, 44),
        (S + 'HaarTransversals/HidaSetting.lean', 179, 237),
        (S + 'HaarTransversals/HidaSetting.lean', 372, 378),
        f(D, 'FourMulAddFiveLeRank'), f(D, 'StandardFrameGramDetNeZero'),
        f('src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/LevelStructures/', 'FrameStd'),
        (S + 'CokernelGLCounts/Measures.lean', 74, 127),
        (S + 'CokernelGLCounts/MassDataConc.lean', 151, 178),
    ],
    'rescale': [
        (S + 'FlagStabilizerTensors/SettingExistsAdapted.lean', 38, 49),
        (S + 'FlagStabilizerTensors/SettingExistsMeasured.lean', 17, 23),
        (S + 'FlagStabilizerTensors/SettingExistsMeasured.lean', 47, 63),
        f(D, 'RescaleStep3'), f(D, 'ExistsMeasWPrescribed'),
    ],
    'retained_and_next': [
        (SW, 1, None), f(M, 'SiegelWeilNarrowOfWide'), f(D, 'SiegelWeilVolumes'),
        (D + 'ExistsGlobalSetting.lean', 45, 83),
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
        first = first or 1
        last = last or len(lines)
        assert 1 <= first <= last <= len(lines), (path, first, last, len(lines))
        selected = b''.join(lines[first - 1:last])
        source_groups[group].append({
            'id': f'GMR_{group}_{number:02d}', 'path': path,
            'line_start': first, 'line_end': last,
            'declaration': 'Literal pinned contracts and producer body, with context in full snapshot',
            'file_sha256': files[path]['sha256'], 'range_sha256': sha(selected),
            'range_bytes': len(selected), 'source_commit': PIN,
            'verified_equal_to_pinned_git_blob': True,
            'url': URL + path + f'#L{first}-L{last}',
        })

specs = [
 (1, 'One standard global character and every permitted character parameter', [], ['character'], [], 'Totally real F; all IsCharAF characters; one standard character before all subsequent data.'),
 (2, 'Existence and exact uniqueness of every required self-dual measure', [1], ['selfdual'], [], 'Original Fourier-inversion predicate, split algebra, all finite places and infinity, including rank-zero coordinate space.'),
 (3, 'Gram submersion on every independent tuple', [], ['fiber_construction'], [], 'All independent tuples, including singular Gram matrices and places above two.'),
 (4, 'Full continuous fiber-family construction for arbitrary additive Haar pairs', [2,3], ['fiber_construction','selfdual'], [], 'Every prescribed additive Haar pair; full IsFibreFamily with all-parameter continuity and positivity on the independent fiber.'),
 (5, 'Pointwise fiber uniqueness and exact unitary/unitriangular covariance', [4], ['fiber_unique_covariant'], [], 'Arbitrary fixed additive Haar pair and every permitted fiber family; includes singular parameters.'),
 (6, 'Exact split and inert finite-field frame counts and full FFCount', [], ['finite_counts'], [], 'Every odd finite field, every quadratic etale algebra, all nondegenerate J,T, 0<=a<=n; FFCount in original a+2<=n range.'),
 (7, 'Exact good-place canonical density for all permitted witness choices', [1,2,3,4,5,6], ['good_density','finite_counts'], [], 'Arbitrary rational basis, IsCharAF character, rational nondegenerate tuple, 1<=a and 2a<n; exact split/inert factors.'),
 (8, 'Summable logarithms and strictly positive density product', [7], ['euler_product','good_density'], [], 'Exact exponent n-a+1>=3 and positive product; no inference of positivity merely from convergence.'),
 (9, 'Full original IsOmT by an explicitly normalized restricted product', [2,4,5,7,8], ['global_fiber'], ['AMD1'], 'All self-dual and fiber-family witnesses, all rational bases, all original continuous-compact/pure finite test factors.'),
 (10, 'Actual adelic orbit, local sections and invariant global measure', [5,6,9], ['orbit'], ['AMD1','AMD4'], 'Actual adelic tensor coordinates; integral Witt lifting almost everywhere; no replacement orbit.'),
 (11, 'Every-section quotient formula with the supplied ambient Haar measure', [], ['quotient'], [], 'Every nonnegative measurable f and every section, including nonmeasurable sections; exact unique stabilizer scalar.'),
 (12, 'Full original global stabilizer-measure supplier', [9,10,11], ['global_supplier','global_fiber','quotient','retained_and_next'], ['AMD4'], 'Original arbitrary IsCharAF, 1<=a, 2a<n, tuple, Hermitian witness and ambient Haar quantifiers; original volume premises retained but unused by direct construction.'),
 (13, 'Full local frame-stabilizer compatibility on independent singular fibers', [3,4,5,10,11], ['local_supplier','orbit'], [], 'Any supplied additive Haar pair and any original fiber family, every ambient Haar normalization; actual singular T_F and S0.'),
 (14, 'Unimodularity of the actual local unitary group', [], ['unimodular'], [], 'Every local unitary group and Haar normalization; trace-pairing determinant proof in characteristic zero.'),
 (15, 'Full normalizer invariance for every S0 Haar normalization', [5,13,14], ['normalizer'], [], 'Every original extra additive Haar/fiber input is allowed and unused; actual S, S0, arbitrary Haar and test function.'),
 (16, 'Actual upper-unitriangular quotient, explicit section and coordinate Haar', [2], ['upper_quotient','local_tie'], [], 'Exact F0, actual S/S0, explicit continuous section and literal sdE coordinate measure, including r=0.'),
 (17, 'Full all-section IsProdU on the actual flag stabilizer', [15,16], ['upper_quotient','local_tie'], [], 'Arbitrary measurable nonnegative ambient function, every valid section without measurability requirement, exact product normalization.'),
 (18, 'Full original normalized local frame-stabilizer supplier', [2,4,5,13,15,16,17], ['local_tie','retained_and_next'], [], 'Original CM/J/SWa1/compatibility/standard-character/place/frame/rank/ambient-Haar scope; all three LocTieW fields.'),
 (19, 'Full original RescaleStep3 on the supplied setting and bridge', [1,12,18], ['actual_setting','rescale','retained_and_next'], ['AMD7','AMD13','AMD14','AMD16','AMD17'], 'Every supplied HidaSetting, AdBridgeIso and MeasTie; one character before all words/tuples/places; same ambient Haar measures and same muNinf,muHinf.'),
]
main = (HERE / 'main.tex').read_bytes()
lines = main.decode().splitlines(keepends=True)
claims = []
for number, title, own, names, inherited_ids, scope in specs:
    identifier = f'GMR{number}'
    first = next(i for i,l in enumerate(lines,1) if l.strip() == '% BEGIN ' + identifier)
    last = next(i for i,l in enumerate(lines,1) if l.strip() == '% END ' + identifier)
    proof = ''.join(lines[first - 1:last]).encode()
    assert b'\\begin{proof}' in proof and b'\\end{proof}' in proof
    claims.append({
        'id': identifier, 'title': title, 'introduced_in': VERSION, 'classification': 'B',
        'status': 'complete human proof at the explicitly stated scope; awaiting independent review',
        'depends_on': [f'GMR{i}' for i in own] + inherited_ids,
        'external_input_ids': ['GMR_CLASSICAL_ANALYSIS','GMR_LOCAL_GLOBAL_ARITHMETIC']
            + (['GMR_ORIGINAL_SW_COMPONENTS'] if number in [12,18] else [])
            + (['GMR_SIEGEL_WEIL_UNITARY_CONVERGENT'] if number == 19 else []),
        'published_input_ids': [], 'scope_note': scope, 'source_groups': names,
        'sources': [e for name in names for e in source_groups[name]],
        'proof_location': {'file': COMPONENT + '/main.tex', 'label': 'claim:' + identifier,
            'line_start': first, 'line_end': last, 'sha256': sha(proof), 'bytes': len(proof)},
        'source_proof_is_not_human_proof': True, 'whole_obligation_closure': False,
    })

inherited_components = {
    'adelic_measures_v48': ['AMD1','AMD4','AMD7','AMD13','AMD14','AMD16','AMD17'],
    'bessel_quotient_suppliers_v52': ['BQS23'],
}
inherited = []
inherited_ids = set()
for component, identifiers in inherited_components.items():
    data = (WORK / component / 'main.tex').read_bytes()
    oldlines = data.splitlines(keepends=True)
    old = json.loads((WORK / component / 'provenance.json').read_text())
    index = {c['id']: c for c in old['claims']}
    bindings = []
    for identifier in identifiers:
        loc = index[identifier]['proof_location']
        first,last = loc['line_start'],loc['line_end']
        selected = b''.join(oldlines[first - 1:last])
        assert loc.get('sha256',loc.get('paragraph_sha256')) == sha(selected), identifier
        bindings.append({'id': identifier,'file': component + '/main.tex',
            'line_start': first,'line_end':last,'sha256':sha(selected),'bytes':len(selected),
            'scope': index[identifier].get('scope_note',index[identifier].get('title'))})
        inherited_ids.add(identifier)
    inherited.append({'component':component,'claims':identifiers,'file':component + '/main.tex',
        'sha256':sha(data),'proof_hashes':{b['id']:b['sha256'] for b in bindings},'claim_bindings':bindings})
known = {c['id'] for c in claims} | inherited_ids
assert all(d in known for c in claims for d in c['depends_on'])
assert len(claims) == 19

inputs = [
 {'id':'GMR_CLASSICAL_ANALYSIS','status':'ordinary mathematical background retained',
  'content':'Real and nonarchimedean inverse function and change-of-variables theorems; local Fourier inversion; Haar existence/uniqueness; elementary Radon regularity, partitions of unity, countable product measures, Fubini/Tonelli and monotone/dominated convergence. The actual Gram coarea, pointwise fiber uniqueness, global product and all-section Weil normalization are proved in GMR3--GMR11, not assumed as black boxes.'},
 {'id':'GMR_LOCAL_GLOBAL_ARITHMETIC','status':'ordinary mathematical background retained',
  'content':'Finite-dimensional linear algebra, the different as the integral trace-dual lattice, the Chinese remainder theorem and elementary facts about completions and unramified quadratic etale algebras. The adelic character parameter argument, finite-field counts, good-place lifting, exact densities and positivity are reconstructed in the human proofs.'},
 {'id':'GMR_ORIGINAL_SW_COMPONENTS','status':'exact original premises retained in supplier statements; not used by direct construction',
  'used_only_by_claims':['GMR12','GMR18'],
  'content':'Original SWa1 and NcWeil.StabilizerFirstChernCompatibility, at exactly the supplied CM extension and ambient Hermitian space. These assert finite arithmetic quotient volume and the smooth compactly supported convergent-range theta/density equality with their original universal choices. Neither is proved here.',
  'source_file':M+'SiegelWeilNarrowOfWide.lean','source_commit':PIN},
 {'id':'GMR_SIEGEL_WEIL_UNITARY_CONVERGENT','status':'exact original global premise retained',
  'used_only_by_claims':['GMR19'],
  'content':'The entire original SiegelWeilUnitaryConvergent: every CM extension/nondegenerate Hermitian space; FinVol and SiegelDensities with 2a<n, every nondegenerate rational T, basis and smooth compactly supported rapidly decaying/pure-finite test factorization; all source Haar/fundamental-domain/character/self-dual choices; continuous densities, multipliable local values and equality to the normalized arithmetic theta mean. No new theorem of arithmetic volume or theta means is claimed.',
  'source_file':SW,'source_commit':PIN},
 {'id':'GMR_SUPPLIED_SETTING_FORMS_BOUNDARY','status':'given-data scope retained; not a new existence premise for GMR19',
  'content':'GMR19 starts with any supplied actual HidaSetting, AdBridgeIso and MeasTie. Its stated application to inherited BQS23 keeps that theorem\'s original supplied Forms0 scope. Original all-family Transport/LevelMatch and ambient Forms0 existence remain separate.'},
]
manifest = {'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,
    'source_commit':PIN,'snapshot_root':str(SNAPSHOT.relative_to(WORK)),
    'checkout_head_verified':True,'source_files':list(files.values()),'total_files':len(files),
    'total_bytes':sum(f['bytes'] for f in files.values()),
    'distinct_source_ranges':len({(r['path'],r['line_start'],r['line_end']) for g in source_groups.values() for r in g}),
    'all_verified_equal_to_pinned_git_blob':True,'no_lean_replay':True,
    'source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof':True}
validation = json.loads((HERE / 'tex_validation.json').read_text())
assert validation['proof_file_sha256'] == sha(main) and validation['status'] == 'PASS'
reviews = [{'file':str(p.relative_to(WORK)),'sha256':sha(p.read_bytes()),'content':json.loads(p.read_text())}
           for p in sorted(HERE.glob('independent_review*.json'))]
dump('source_manifest.json',manifest)
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1','artifact_version':VERSION,
    'component':COMPONENT,'proof_file_sha256':sha(main),'components':inherited,
    'all_current_proof_ranges_verified':True})
dump('classical_inputs.json',{'schema':'rh-explicit-inputs/1','component':COMPONENT,'inputs':inputs,
    'new_unreconstructed_published_mathematical_premises':[],
    'original_published_premise_retained':SW})
dump('retained_inputs.json',{'schema':'rh-retained-inputs/1','artifact_version':VERSION,
    'component':COMPONENT,'proof_file_sha256':sha(main),'inputs':inputs,
    'no_disguised_local_density_or_measure_supplier':True})
dump('provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':VERSION,
    'date':'2026-11-23','component':COMPONENT,'source_commit':PIN,
    'main_tex_sha256':sha(main),'proof_file_sha256':sha(main),'claims':claims,
    'source_groups':source_groups,'source_files':list(files.values()),'source_inventory':list(files.values()),
    'retained_foundations':inputs,'inherited_human_inputs':inherited,'independent_reviews':reviews,
    'builder':COMPONENT+'/build_metadata.py','validation':validation,
    'whole_obligation_closures':[],'no_lean_replay':True})
completed = [
 'Full standard_character_exists and uniqueness/nontriviality of local factors',
 'Self-dual measures and full IsFibreFamily existence/uniqueness, including singular independent fibers',
 'Exact finite-field split/inert frame counts and full original FFCount',
 'Exact good-place density factors, positive convergent product and full IsOmT',
 'Actual adelic orbit and all-section quotient normalization',
 'Full exists_adelicTorusMeasure_stabiliserHaar',
 'Full exists_haar_frameStabiliser_compatible_fibre for arbitrary additive Haar pairs/fiber families',
 'Full similitude_conj_preserves_unitary_haar_at_finite_place',
 'Actual upper-unitriangular section and full IsProdU',
 'Full exists_frameStabilizerHaar_normalised_fibreMeasure',
 'Full original RescaleStep3 with exact supplied setting, bridge and infinite measures',
]
remaining = [
 'SiegelWeilUnitaryConvergent arithmetic theta/volume premise remains unreconstructed',
 'Ambient Forms0 and the distinct original all-family Transport/LevelMatch suppliers',
 'InVolumesAt and arithmetic stabilizer/ambient volume comparison on the constructed common measures',
 'BesselMapUniq, LocTied and the downstream global spectral identifications',
 'Full original CountIdempotentsClass and its volume/point comparison inputs',
]
dump('contracts.json',{'schema':'rh-root-producer-contracts/1','artifact_version':VERSION,
    'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':sha(main),'endpoint_claim':'GMR19',
    'global_measure_endpoint_claim':'GMR12','local_measure_endpoint_claim':'GMR18',
    'completed_original_substatements':completed,'remaining_exact_producers_for_RescaleStep3':[],
    'retained_original_premise':'SiegelWeilUnitaryConvergent, not reconstructed; direct normalization proof does not use its theta identity',
    'shared_data_preserved':['The supplied HidaSetting and all nonmeasure fields','The supplied AdBridgeIso and all five MeasTie entries',
      'One standard global character before every word, place and auxiliary tuple','Original muG, muGinf, muGf and every muGv',
      'Every original muNinf and muHinf','Actual global stabilizers and local S0/S groups',
      'All-section formulas with no additional measurable-section assumption'],
    'remaining_downstream_boundaries':remaining,'proposed_whole_obligation_closures':[],
    'whole_obligation_closures':[],'no_lean_replay':True})
dump('closure.json',{'schema':'rh-component-closure/1','artifact_version':VERSION,'component':COMPONENT,
    'proof_file_sha256':sha(main),'human_claims':[c['id'] for c in claims],
    'fully_proved_claims_at_stated_scope':[c['id'] for c in claims],
    'completed_original_producer_contracts':completed,'conditional_consequences':[
      {'claim':'GMR19','consequence':'RescaleStep3','retained_input':'Exact original SiegelWeilUnitaryConvergent'}],
    'remaining_source_producers_in_this_measure_normalization_chain':[],
    'remaining_downstream_boundaries':remaining,'whole_obligation_closures':[],
    'all_sources_pinned':True,'no_lean_replay':True})
dump('claim_dag.json',{'schema':'rh-claim-dependency-dag/1','artifact_version':VERSION,
    'component':COMPONENT,'proof_file_sha256':sha(main),
    'nodes':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims],
    'inherited_nodes':sorted(inherited_ids),'all_dependencies_resolve':True})
(HERE/'report.txt').write_text(f'''Global measure rescaling, version {VERSION}
Pinned source: {PIN}
Frozen main SHA-256: {sha(main)}

Nineteen complete human claims GMR1--GMR19; {len(main.decode().split())} TeX words.
Full original RescaleStep3 is proved on any supplied HidaSetting, supplied
AdBridgeIso and MeasTie, with the original SiegelWeilUnitaryConvergent premise
explicit. One standard global character is fixed before all words, places and
auxiliary tuples. Original muG/muGinf/muGf/muGv and muNinf/muHinf are preserved.

Substantial new mathematical route:
GMR1--5: exact character/Fourier normalization, Gram submersion on independent
tuples, arbitrary-Haar continuous coarea family, pointwise uniqueness/covariance.
GMR6--8: exact split and inert finite-field counts and good-place masses
product(j=n-a+1..n)(1-epsilon_v^j q_v^(-j)), with explicit positive summable
logarithms in the entire original 1<=a, 2a<n range.
GMR9--12: normalized restricted-product fiber, actual adelic orbit and all-section
Weil formula; full original global stabilizer-measure supplier.
GMR13--18: singular independent F0 fiber, arbitrary prescribed additive Haar
pair/family, local unitary unimodularity, exact normalizer invariance, explicit
continuous unitriangular section and full local product/LocTieW supplier.
GMR19: simultaneous actual measure records, using reviewed AMD13--17, and every
clause of the exact original RescaleStep3. No extra local-product identity is
invented for the MeasW record.

The direct canonical measure route does not assume the source's large ExOmT,
local density, nonzero Euler product or quotient-normalization suppliers.
These are proved in the chapter. It does not prove the arithmetic theta mean,
arithmetic quotient volume equality, ambient Forms0, all-family transport,
Bessel uniqueness, CountIdempotentsClass or a whole selected global obligation.

Verification: {len(files)} source files, {manifest['distinct_source_ranges']} distinct
exact ranges, {manifest['total_bytes']} bytes pinned to Git; all proof blocks and
{len(inherited_ids)} inherited blocks hash-bound. Two-pass draft TeX PASS, zero
errors/missing characters/undefined references/overfull boxes. No PDF or Lean
replay. Independent review is recorded separately after mathematical freeze.
''')
(HERE/'README.txt').write_text('Read main.tex and contracts.json.\n'
    'Draft TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n'
    'Metadata: python build_metadata.py\nRead-only bindings: python verify_hashes.py\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'main_sha256':sha(main),
    'source_files':len(files),'source_ranges':manifest['distinct_source_ranges'],
    'source_bytes':manifest['total_bytes'],'tex_status':validation['status'],
    'whole_obligation_closures':[]},indent=2))
