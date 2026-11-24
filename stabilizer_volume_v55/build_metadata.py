#!/usr/bin/env python3
"""Bind SVW human proofs to the original pinned consumers; no Lean replay."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.55'
COMPONENT = HERE.name
SNAPSHOT = HERE / 'source_snapshot'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
P = 'src/Formalism/PeriodIntegrals/'
U = P + 'UnitaryGroupMassFormula/'
V = U + 'StabilizerVolume/'
S = 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
C = S + 'CokernelGLCounts/'
N = C + 'RankPointCounts/DualFamilyCounting/'
GMV = 'src/Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def f(prefix, name, first=None, last=None, declaration='Original contract or producer; complete file retained for context'):
    return (prefix + name + '.lean', first, last, declaration)

groups = {
 'premises_and_volume_scope': [
   f(P, 'VolFromSW', 17, 22, 'thetaS; SWa1'),
   f(P, 'VolFromSW', 91, 101, 'VolStabAt: six nested AllSome stages'),
   f(V, 'VolStabFromSWS', 14, 30, 'InCtx; VolStabW; VolStabFromSWS'),
   f(V, 'SiegelWeilNarrowOfWide', 11, 44, 'IsSmoothCc; exact StabilizerFirstChernCompatibility'),
   f(N, 'NcWeil', 40, 43, 'Original consumer VolStabW'),
 ],
 'adelic_topology': [
   (GMV, 99, 123, 'Actual HA topology, measurable space and matrix action'),
   f(U + 'SemidirectVolume/', 'EqZeroOfMemNbhdA', 21, 54, 'Rational diagonal isolation in the full adeles'),
   f(U + 'SemidirectVolume/', 'EqZeroOfMemNbhdA', 69, 153, 'Tensor isolation and discHA_of'),
   f(U + 'SemidirectVolume/', 'LocallyCompactAdelicUnitary', 7, 9, 'Actual tensor and unitary local compactness/second countability'),
   f(V, 'TopoClose', 17, 35, 'Actual tuple/group second countability and measurable group'),
 ],
 'admissible_tests': [
   (GMV, 266, 287, 'RapidDecay; latV; IsSB; IsProdInfFin; IsPureFin'),
   f(V, 'VolStabFromSWS', 32, 50, 'IsAdm and IsAdmS exact factorizations'),
   f(V, 'SiegelWeilNarrowOfWide', 65, 77, 'Smoothness under every continuous additive chart'),
   f(V, 'AdmCpt', 15, 104, 'Compact finite boxes, eventual integrality and finite product support'),
   f(V, 'TopoNuFin', 19, 74, 'Compact adelic sets and compact-open local cutoffs'),
 ],
 'finite_theta': [
   f(V, 'VolStabFromSWS', 94, 97, 'FinTheta original all-tuples scope'),
   f(V, 'FinTheta', 258, 432, 'finite_of_adm; finTheta_holds'),
 ],
 'om_and_compatibility': [
   f(P, 'VolFromSW', 55, 89, 'ratIn; IsOmT; IsCompatT exact all-witness/all-section scope'),
   f(V, 'TopoNuFin', 85, None, 'nuFin_gen: every supplied IsOmT finite on compact sets'),
   f(V, 'ExStabOrb', 7, 8, 'ExStab original universal supplied-measure endpoint'),
 ],
 'pointwise_density': [
   (GMV, 177, 192, 'IsContDensityOn and full IsFibreFamily'),
   f(V, 'VolStabFromSWS', 122, 146, 'DensFibInf and DensFibV original scopes'),
   f(V, 'DensGen', 127, 261, 'Continuous density uniqueness and compact cutoff proof'),
   f(V, 'DensFibInf', 13, 25, 'densFibInf_holds'),
   f(V, 'DensFibV', 45, 60, 'densFibV_holds'),
 ],
 'same_measure_theta_mean': [
   f(V, 'VolStabFromSWS', 66, 70, 'SWeqOm'),
   f(V, 'SWeqOm', 15, 72, 'Rapid decay from compact support; sWeqOm_of'),
 ],
 'rational_orbit': [
   f(V, 'VolStabFromSWS', 90, 92, 'Witt original context'),
   f(V, 'HformSmulRight', 154, 177, 'sigma_invol_cm; witt_holds'),
   f(V, 'Unfold', 22, 60, 'Actual rational embedding, action and injectivity'),
   f(V, 'UnfoldMain', 16, 48, 'gram_orbit_equiv'),
 ],
 'fundamental_domains': [
   f(U + 'SemidirectVolume/', 'FundamentalDomainExists', 9, 102, 'Strict Borel fundamental-domain construction'),
   f(V, 'ExFDStab', 13, 48, 'Full ExFDStab on the actual rational intersection'),
   f(V, 'ExFDStabFin', 9, 12, 'Actual discreteness and final exFDStab_holds'),
   f(V, 'UnfoldAbsAlt', 36, 98, 'Original almost-everywhere domain and countable null-set handling'),
 ],
 'unimodularity': [
   f(V, 'VolStabFromSWS', 99, 105, 'Unimod and UnimodStab original scopes'),
   f(V, 'Unimod', 186, 233, 'Rational countability and unimod_holds'),
   f(V, 'UnimodStab', 18, 41, 'Positive symmetric test and inversion invariance'),
   f(V, 'UnimodStab', 87, 160, 'Actual closed stabilizer and original right/inversion invariance'),
 ],
 'unfolding': [
   f(V, 'VolStabFromSWS', 72, 82, 'Unfold: nonzero integral before finite stabilizer mass'),
   f(V, 'UnfoldAbs', 38, 98, 'Right-coset representatives and rational sum reindexing'),
   f(V, 'UnfoldAbsAlt', 16, 34, 'Extended nonnegative unfolding interface'),
   f(V, 'UnfoldMain', 54, 149, 'Original full unfold_of and correct-stage finiteness conversion'),
   f(V, 'UnfoldFin', 11, 12, 'unfold_holds original endpoint'),
 ],
 'positive_test': [
   f(V, 'VolStabFromSWS', 84, 88, 'PosTest original arbitrary compatible measures'),
   f(V, 'PosNear', 124, 187, 'Integral basis scaling, orbit continuity and smooth bump'),
   f(V, 'PosNear', 195, 265, 'TestNear and testNear_holds'),
   f(V, 'PosTest', 13, 76, 'Original integrability and compatibility proof of PosTest'),
 ],
 'existence_order': [
   f(V, 'VolStabFromSWS', 52, 64, 'ExChar, ExOmT, ExStab and ExFDStab'),
   f(P, 'VolFromSW', 91, 101, 'VolStabAt nested existence/universality'),
   f(V, 'Assembly', 43, 78, 'Source assembly and named suppliers; not imported as a human proof'),
 ],
 'scalar_cancellation': [
   f(V, 'VolStabFromSWOf', 12, 45, 'volStabFromSW_of complete original scalar cancellation'),
 ],
 'covolume_transport': [
   f(C, 'Measures', 119, 125, 'ratOf and original choice-based covol'),
   f(C, 'MassDataInst', 60, 61, 'Original choice-based covolBy'),
   f(U + 'CovolumeFrames/', 'InVolumesAtOfSWW', 23, 49, 'covol_eq_covolBy_w'),
 ],
 'actual_setting_join': [
   f(U + 'CovolumeFrames/', 'InVolumesAtOfSWW', 51, 87, 'stepSizeW and full inVolumesAt_of_w'),
   f(V, 'InVolumesAtOfSWS', 13, 25, 'SWXS and inVolumesAt_of_SWS'),
   f(C, 'MassDataInst', 158, 163, 'Actual bOf volume fields'),
   f(C, 'MassDataInst', 257, 274, 'Full InVolumesAt and its two unipotent antecedents'),
   ('src/Formalism/HermitianCurvature/MemParahoricTimesPrincipalCongruenceIff.lean', 624, 624, 'Literal three-field InVolumes predicate'),
 ],
 'rescaled_return': [
   f(C, 'MassDataConc', 151, 179, 'MeasCompat-psi, MeasCompat and inVolumes_of_compat'),
   ('src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean', 10, None, 'Exact retained FinVol and smooth SiegelDensities premise'),
 ],
}

# Claim number, title, own dependencies, source groups, inherited dependencies, scope.
specs = [
 (1, 'Actual adelic topology and rational discrete subgroups', [], ['adelic_topology'], ['AMD1'], 'Actual CM tensor spaces, unitary group and nondegenerate-tuple stabilizer; no finite quotient mass assumed.'),
 (2, 'Admissible cutoffs and full FinTheta', [1], ['admissible_tests','finite_theta'], [], 'Every original pure test, every rational tuple and every group element; compact cutoffs on arbitrary compact adelic sets.'),
 (3, 'Every supplied IsOmT equals the canonical Radon measure', [2], ['om_and_compatibility','admissible_tests'], ['GMR2','GMR5','GMR9'], 'Any original supplied IsOmT; derives local finiteness and Radon regularity instead of imposing them; exact prescribed character and fiber normalization.'),
 (4, 'Full original DensFibInf and DensFibV', [], ['pointwise_density'], ['GMR4','GMR5'], 'All original self-dual/fiber witnesses, arbitrary continuous density and allowed test; equality at the specified rational Gram parameter, not just almost everywhere.'),
 (5, 'Full original SWeqOm on the same supplied measure', [4], ['premises_and_volume_scope','same_measure_theta_mean','om_and_compatibility'], [], 'Original smooth compatibility premise and every character, ambient Haar, domain and IsOmT witness; same local witnesses throughout.'),
 (6, 'Full rational Witt orbit and exact rational tuple equivalence', [1], ['rational_orbit'], ['GMR10'], 'Every rational tuple with the prescribed nondegenerate Gram matrix; exact actual rational group and right stabilizer cosets.'),
 (7, 'Strict Borel domains and full ExFDStab', [1], ['fundamental_domains'], [], 'General second countable topological group with discrete subgroup; on the original stabilizer, every Haar measure and no finite-mass premise.'),
 (8, 'Fundamental-domain independence at the original AE scope', [], ['fundamental_domains'], [], 'All original null-measurable, almost-everywhere disjoint/covering domains for a countable subgroup; nonnegative invariant integrals including infinity.'),
 (9, 'Actual adelic unimodularity and inversion invariance', [1], ['unimodularity'], ['GMR14'], 'All ambient/stabilizer Haar normalizations; derives global right/inversion invariance from local trace-pairing unimodularity before quotient finiteness.'),
 (10, 'Nonnegative orbit unfolding before finite stabilizer mass', [1,7,8,9], ['unfolding','om_and_compatibility'], ['GMR10'], 'Actual locally compact adelic groups; every compatible measure, measurable nonnegative test and original domain pair; extended identity allows infinity. No claim of full unrelated abstract measurable-group unfold_abs.'),
 (11, 'Full original Unfold with correct-stage finite mass', [2,6,10], ['unfolding','om_and_compatibility'], [], 'All original arbitrary witnesses and admissible nonnegative tests; only source nonzero Bochner integral hypothesis, with its default-zero convention explicit.'),
 (12, 'Full original TestNear with an explicit smooth positive test', [1,2], ['positive_test','admissible_tests'], [], 'Scaled rational basis integral for the specified tuple, all finite lattice indicators, all-coordinate smooth compact infinite bump and actual open orbit neighborhood.'),
 (13, 'Full original PosTest for every supplied compatible measure', [12], ['positive_test','om_and_compatibility'], [], 'Same nonnegative test has finite positive integral; positivity follows directly from compatibility and Haar positivity, without finite stabilizer quotient mass.'),
 (14, 'All original nested existence stages for the volume statement', [1,3,7], ['existence_order','om_and_compatibility'], ['GMR1','GMR2','GMR3','GMR4','GMR5','GMR9','GMR10','GMR11','GMR12'], 'ExChar, ExOmT, ExStab and ExFDStab with every character/Haar and every supplied IsOmT. Ambient finite volume uses only original SWa1; no stabilizer finite mass presumed.'),
 (15, 'Full original VolStabFromSWS and scalar cancellation', [5,11,13,14], ['premises_and_volume_scope','scalar_cancellation'], [], 'Exactly SWa1 and StabilizerFirstChernCompatibility retained; full strict range 1<=a and 2a<M, all original six nested AllSome stages and equality of extended masses.'),
 (16, 'Full original choice-based covolume transport', [15], ['covolume_transport'], [], 'Equality for arbitrary supplied original VolStabW; positivity only with retained SWa1 and the established finite-mass comparison; ratIn equals ratOf.'),
 (17, 'Full original actual-setting InVolumesAt implication', [15,16], ['actual_setting_join','premises_and_volume_scope'], ['GMR19','AOS9'], 'Any supplied actual X and bridge, both words, arbitrary auxiliary X0 and all original witnesses; generic two unipotent covolume-one antecedents explicitly retained.'),
 (18, 'Actual rescaled-setting InVolumes with measure inputs discharged', [17], ['rescaled_return','actual_setting_join'], ['GMR19','AMD17'], 'Same GMR19 output and one character before all words/tuples; both covolume-one inputs and three orbit compatibilities already supplied. Original SiegelWeilUnitaryConvergent, HypX and auxiliary nondegeneracy retained.'),
]

assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'], text=True).strip() == PIN
files = {}
for path in sorted({entry[0] for entries in groups.values() for entry in entries}):
    data = subprocess.check_output(['git','-C',str(REPO),'show',PIN + ':' + path])
    assert (REPO / path).read_bytes() == data, path
    target = SNAPSHOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    files[path] = {'path': path, 'snapshot_path': str(target.relative_to(WORK)),
        'source_commit': PIN, 'sha256': sha(data), 'bytes': len(data),
        'line_count': len(data.splitlines(keepends=True)), 'url': URL + path,
        'verified_equal_to_pinned_git_blob': True}
source_groups = {}
for name, entries in groups.items():
    source_groups[name] = []
    for number, (path, first, last, declaration) in enumerate(entries, 1):
        lines = (SNAPSHOT / path).read_bytes().splitlines(keepends=True)
        first, last = first or 1, last or len(lines)
        assert 1 <= first <= last <= len(lines), (path, first, last, len(lines))
        data = b''.join(lines[first-1:last])
        source_groups[name].append({'id': f'SVW_{name}_{number:02d}', 'path': path,
            'line_start': first, 'line_end': last, 'declaration': declaration,
            'file_sha256': files[path]['sha256'], 'range_sha256': sha(data),
            'range_bytes': len(data), 'source_commit': PIN,
            'verified_equal_to_pinned_git_blob': True,
            'url': URL + path + f'#L{first}-L{last}'})

main = (HERE / 'main.tex').read_bytes()
lines = main.decode().splitlines(keepends=True)
old_claims = {}
if (HERE / 'provenance.json').exists():
    old_claims = {c['id']: c for c in json.loads((HERE / 'provenance.json').read_text())['claims']}
claims = []
for number, title, own, names, inherited_ids, scope in specs:
    identifier = f'SVW{number}'
    first = next(i for i,l in enumerate(lines,1) if l.strip() == '% BEGIN ' + identifier)
    last = next(i for i,l in enumerate(lines,1) if l.strip() == '% END ' + identifier)
    proof = ''.join(lines[first-1:last]).encode()
    assert b'\\begin{proof}' in proof and b'\\end{proof}' in proof
    status = 'complete human proof at the stated original scope; awaiting independent review'
    old = old_claims.get(identifier, {})
    if old.get('proof_location', {}).get('sha256') == sha(proof):
        status = old.get('status', status)
    claim_inputs = ['SVW_CLASSICAL_BACKGROUND']
    if number in [5,15,16,17]:
        claim_inputs += ['SVW_ORIGINAL_SWA1','SVW_ORIGINAL_SMOOTH_COMPATIBILITY']
    if number == 14:
        claim_inputs += ['SVW_ORIGINAL_SWA1']
    if number == 18:
        claim_inputs += ['SVW_ORIGINAL_SIEGEL_WEIL_UNITARY_CONVERGENT','SVW_ACTUAL_SETTING_SCOPE']
    claims.append({'id': identifier, 'title': title, 'introduced_in': VERSION,
        'classification': 'B', 'status': status,
        'depends_on': [f'SVW{i}' for i in own] + inherited_ids,
        'external_input_ids': claim_inputs, 'published_input_ids': [],
        'scope_note': scope, 'source_groups': names,
        'sources': [r for name in names for r in source_groups[name]],
        'proof_location': {'file': COMPONENT + '/main.tex', 'label': 'claim:' + identifier,
            'line_start': first, 'line_end': last, 'sha256': sha(proof), 'bytes': len(proof)},
        'source_proof_is_not_human_proof': True, 'whole_obligation_closure': False})

inherited_components = {
 'adelic_measures_v48': ['AMD1','AMD17'],
 'global_measure_rescaling_v53': ['GMR1','GMR2','GMR3','GMR4','GMR5','GMR9','GMR10','GMR11','GMR12','GMR14','GMR19'],
 'archimedean_orbital_scalar_v54': ['AOS9'],
}
inherited, all_inherited = [], set()
for component, ids in inherited_components.items():
    data = (WORK / component / 'main.tex').read_bytes()
    oldlines = data.splitlines(keepends=True)
    index = {c['id']: c for c in json.loads((WORK / component / 'provenance.json').read_text())['claims']}
    bindings = []
    for identifier in ids:
        loc = index[identifier]['proof_location']
        selected = b''.join(oldlines[loc['line_start']-1:loc['line_end']])
        assert loc.get('sha256',loc.get('paragraph_sha256')) == sha(selected), identifier
        bindings.append({'id':identifier, 'file':component+'/main.tex',
            'line_start':loc['line_start'],'line_end':loc['line_end'],
            'sha256':sha(selected),'bytes':len(selected),
            'scope':index[identifier].get('scope_note',index[identifier]['title'])})
        all_inherited.add(identifier)
    inherited.append({'component':component,'claims':ids,'file':component+'/main.tex',
        'sha256':sha(data),'proof_hashes':{b['id']:b['sha256'] for b in bindings},
        'claim_bindings':bindings})
known = {c['id'] for c in claims} | all_inherited
assert all(d in known for c in claims for d in c['depends_on'])

inputs = [
 {'id':'SVW_CLASSICAL_BACKGROUND','status':'ordinary mathematical background retained',
  'content':'Finite-dimensional Hermitian linear algebra; elementary local-field and Minkowski-lattice topology; Haar existence/uniqueness, Radon regularity on locally compact second countable spaces, continuous compact cutoffs, Euclidean smooth bumps, countable product measures, Tonelli and monotone convergence. Exact continuous Gram fibers and normalized global products are inherited from GMR. Rational orbit extension, actual strict domains, domain independence, unfolding and scalar cancellation are written out here.'},
 {'id':'SVW_ORIGINAL_SWA1','status':'exact original mathematical premise retained',
  'content':'For the supplied CM extension and Hermitian space: ambient Haar existence, then for every ambient Haar measure existence of an arithmetic fundamental domain and finite mass for every such domain. No stabilizer-volume assertion is included.',
  'source_file':P+'VolFromSW.lean','line_start':21,'line_end':22,'source_commit':PIN},
 {'id':'SVW_ORIGINAL_SMOOTH_COMPATIBILITY','status':'exact original mathematical premise retained; not proved by cancellation',
  'content':'StabilizerFirstChernCompatibility exactly as defined: every a with 2a<M, rational nondegenerate Hermitian T, specified basis and pure test with continuous rapidly decaying all-coordinate smooth compact infinite factor; all nested ambient Haar/domain/character/self-dual choices; continuous local densities, multipliable values and equality to the normalized rational theta mean.',
  'source_file':V+'SiegelWeilNarrowOfWide.lean','line_start':22,'line_end':44,'source_commit':PIN},
 {'id':'SVW_ORIGINAL_SIEGEL_WEIL_UNITARY_CONVERGENT','status':'exact original upstream premise retained for actual rescaled return',
  'content':'Full original SiegelWeilUnitaryConvergent, including FinVol and smooth SiegelDensities at every supplied CM/Hermitian datum. GMR19 supplies its precise SWa1 and compatibility specializations and one character before all words/tuples. This chapter does not prove those arithmetic theta identities.',
  'source_file':'src/Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean','source_commit':PIN},
 {'id':'SVW_ACTUAL_SETTING_SCOPE','status':'exact supplied-data and downstream hypotheses retained',
  'content':'Same supplied HidaSetting and AdBridgeIso, both words, auxiliary X0, level-character witness, L/A records and literal HypX for the specified infinity domains. X0 nondegeneracy remains required. Generic InVolumesAt retains both unipotent covolume-one antecedents; actual GMR19 MeasCompat-psi supplies them, without a new measure change. Ambient Forms0 and all-family transport/level suppliers are not inferred.'},
]
manifest = {'schema':'rh-source-manifest/1','artifact_version':VERSION,'component':COMPONENT,
 'source_commit':PIN,'snapshot_root':str(SNAPSHOT.relative_to(WORK)),
 'checkout_head_verified':True,'source_files':list(files.values()),'total_files':len(files),
 'total_bytes':sum(x['bytes'] for x in files.values()),
 'distinct_source_ranges':len({(r['path'],r['line_start'],r['line_end']) for v in source_groups.values() for r in v}),
 'all_verified_equal_to_pinned_git_blob':True,'no_lean_replay':True,
 'source_is_evidence_for_target_scope_not_a_substitute_for_the_human_proof':True}
validation = json.loads((HERE/'tex_validation.json').read_text())
assert validation['proof_file_sha256'] == sha(main) and validation['status'] == 'PASS'
reviews = []
for path in sorted(HERE.glob('independent_review*.json')):
    value = json.loads(path.read_text())
    assert value.get('proof_file_sha256',value.get('main_tex_sha256',sha(main))) == sha(main)
    reviews.append({'file':str(path.relative_to(WORK)),'sha256':sha(path.read_bytes()),'content':value})
dump('source_manifest.json',manifest)
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'components':inherited,
 'all_current_proof_ranges_verified':True})
dump('classical_inputs.json',{'schema':'rh-explicit-inputs/1','component':COMPONENT,'inputs':inputs[:1],
 'new_unreconstructed_published_mathematical_premises':[]})
dump('retained_inputs.json',{'schema':'rh-retained-inputs/1','artifact_version':VERSION,
 'component':COMPONENT,'proof_file_sha256':sha(main),'inputs':inputs,
 'no_disguised_volume_equality_or_measure_normalization_premise':True,
 'stabilizer_finite_mass_proved_after_nonzero_theta_integral':True,
 'generic_unipotent_antecedents_retained_but_supplied_on_GMR19_output':True})
dump('provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':VERSION,
 'date':'2026-11-23','component':COMPONENT,'source_commit':PIN,
 'main_tex_sha256':sha(main),'proof_file_sha256':sha(main),'claims':claims,
 'source_groups':source_groups,'source_files':list(files.values()),'source_inventory':list(files.values()),
 'retained_foundations':inputs,'inherited_human_inputs':inherited,'independent_reviews':reviews,
 'builder':COMPONENT+'/build_metadata.py','validation':validation,
 'whole_obligation_closures':[],'no_lean_replay':True})
completed = [
 'Every supplied original IsOmT identified with the canonical Radon measure, without an extra regularity premise',
 'Full original FinTheta and same-measure DensFibInf/DensFibV/SWeqOm',
 'Full original rational Witt orbit, ExFDStab, Unimod and UnimodStab',
 'Full original Unfold at arbitrary supplied domains with correct-stage finite stabilizer mass',
 'Full original TestNear and PosTest, same positive finite admissible smooth test',
 'Full original ExChar/ExOmT/ExStab with every supplied IsOmT and all nested witness order',
 'Full original VolStabFromSWS under exactly SWa1 and StabilizerFirstChernCompatibility',
 'Full original covol_eq_covolBy_w, equality distinguished from extra positivity',
 'Full original InVolumesAt/inVolumesAt_of_SWS at the actual supplied setting',
 'Actual bOf.InVolumes on GMR19 output, with existing MeasCompat-psi supplying the three orbit measures and both unipotent normalizations',
]
remaining = [
 'Exact original SWa1 and smooth StabilizerFirstChernCompatibility premises themselves; full upstream SiegelWeilUnitaryConvergent',
 'Distinct RealBracket reference unipotent covolume/discriminant exponent, local JacGauge/PlaceSplit and ProdExact',
 'Finite-place factors and the other actual mass, index, counting, column and form fields',
 'Ambient Forms0, original all-family Transport/LevelMatch, Bessel uniqueness/local ties and global spectral identifications',
]
shared = [
 'Actual supplied CM extension, involution, Hermitian form, ordered X0 and Gram symmetry witness',
 'Every original character/Haar/self-dual/fiber/fundamental-domain witness; no witness changes between density identification and unfolding',
 'On actual X, one GMR19 standard character before all words, places and auxiliary tuples',
 'Unchanged actual setting bridge, infinity Haar measures, X0 and both word frames',
 'Same three compatible stabilizer measures and already normalized unipotent measures; no new infinity or global normalization',
]
dump('contracts.json',{'schema':'rh-root-producer-contracts/1','artifact_version':VERSION,
 'component':COMPONENT,'source_commit':PIN,'proof_file_sha256':sha(main),
 'primary_endpoint_claim':'SVW15','actual_setting_endpoint_claim':'SVW18','endpoint_claim':'SVW18',
 'completed_original_substatements':completed,
 'remaining_exact_producers_for_VolStabFromSWS':[],
 'remaining_exact_producers_for_InVolumesAt_given_original_SWXS':[],
 'retained_original_premises':['SWa1','StabilizerFirstChernCompatibility',
   'Original SiegelWeilUnitaryConvergent for the GMR19 actual-setting return',
   'Actual supplied setting/bridge/HypX/auxiliary nondegenerate tuple'],
 'shared_data_preserved':shared,'remaining_downstream_boundaries':remaining,
 'proposed_whole_obligation_closures':[],'whole_obligation_closures':[],'no_lean_replay':True})
dump('closure.json',{'schema':'rh-component-closure/1','artifact_version':VERSION,'component':COMPONENT,
 'proof_file_sha256':sha(main),'human_claims':[c['id'] for c in claims],
 'fully_proved_claims_at_stated_scope':[c['id'] for c in claims],
 'completed_original_producer_contracts':completed,
 'conditional_consequences':['Exact actual volume fields on GMR19 rescaled setting, retaining original Siegel--Weil and literal HypX/auxiliary nondegeneracy'],
 'remaining_source_producers_in_this_stabilizer_volume_chain':[],
 'remaining_downstream_boundaries':remaining,'whole_obligation_closures':[],
 'all_sources_pinned':True,'no_lean_replay':True})
dump('claim_dag.json',{'schema':'rh-claim-dependency-dag/1','artifact_version':VERSION,'component':COMPONENT,
 'proof_file_sha256':sha(main),'nodes':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims],
 'inherited_nodes':sorted(all_inherited),'all_dependencies_resolve':True})
(HERE/'report.txt').write_text(f'''Stabilizer volume comparison, version {VERSION}
Accepted pin: {PIN}
Main SHA-256: {sha(main)}

Eighteen complete human proofs SVW1--SVW18; {len(main.decode().split())} TeX words.
Primary endpoint: full original VolStabFromSWS with the exact retained SWa1
and StabilizerFirstChernCompatibility premises. All six original nested
character/Haar/IsOmT/compatible-Haar/domain/domain witness stages are kept.

The mathematical proof identifies every supplied IsOmT with the already
constructed Radon measure by admissible cutoffs and determining pure tests;
it identifies every continuous local density at the specified Gram value.
The rational orbit is the actual right-coset space. Strict Borel domains
give extended nonnegative unfolding without first assuming stabilizer mass
finite. Countable domain independence returns every original AE witness.
One explicit smooth nonnegative test is positive on an actual orbit
neighborhood, hence has positive finite integral for the supplied compatible
measure. The nonzero theta integral gives integrability and finite stabilizer
mass at the correct stage; scalar cancellation then proves exact equality.

The actual-setting join is full InVolumesAt and, on GMR19 output, the actual
bOf.InVolumes fields. GMR19 already supplies both unipotent covolume-one
inputs; these are retained only in the generic implication and not reopened
as missing producers. X0, both words, one character, the original bridge,
all infinity measures and the existing compatible stabilizer measures remain
common. No new normalization or unnamed volume-equality premise is used.

Retained: the original Siegel--Weil premises themselves, distinct RealBracket
unipotent/discriminant and local Jacobian/product suppliers, finite-place and
other mass/counting/form fields, ambient Forms0, all-family Transport/LevelMatch,
Bessel uniqueness and global spectral ties. No whole selected closure.

Bindings: {len(files)} full pinned source files, {manifest['distinct_source_ranges']}
distinct exact ranges, {manifest['total_bytes']} source bytes, 18 proof blocks,
and {len(all_inherited)} inherited human blocks. Two-pass draft TeX PASS with
zero diagnostics. No PDF and no Lean replay. Independent review binds the
frozen proof separately.
''')
(HERE/'README.txt').write_text('Read main.tex, contracts.json and retained_inputs.json.\n'
 'Draft TeX: python validate_tex.py --format ../global_local_gain_v46/validation/pdflatex.fmt\n'
 'Build metadata: python build_metadata.py\nRead-only verification: python verify_hashes.py\n')
print(json.dumps({'component':COMPONENT,'claims':len(claims),'main_sha256':sha(main),
 'source_files':len(files),'source_ranges':manifest['distinct_source_ranges'],
 'source_bytes':manifest['total_bytes'],'inherited_blocks':len(all_inherited),
 'tex_status':validation['status'],'whole_obligation_closures':[]},indent=2))
