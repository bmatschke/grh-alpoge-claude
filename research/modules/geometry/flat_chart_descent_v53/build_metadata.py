#!/usr/bin/env python3
"""Build source- and proof-bound metadata; mutate only this component."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
COMP = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
MPIN = '0df444a360eaa60ab8c11dca51a86af692955474'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
MREPO = 'https://github.com/leanprover-community/mathlib4'
P = 'src/Development/AbelianVarietyTheory/Proofs/'
C = P + 'CoherentCohomologyProofs/'
D = 'src/Development/AbelianVarietyTheory/Definitions/QuasicoherentCohomology/'
parser = argparse.ArgumentParser()
parser.add_argument('--source-root', type=Path,
                    default=Path('/workspace/scratch/249d32c24541/formal_source'))
args = parser.parse_args()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

proof = (HERE / 'main.tex').read_bytes()
proof_sha = sha(proof)
base = dict(artifact_version='0.53', component=COMP, source_commit=PIN,
            proof_file_sha256=proof_sha, status='written_pending_independent_review')
rows = []

def src(key, file, lo, hi, declaration, prefix=C):
    rows.append((key, prefix + file, lo, hi, declaration))

src('generalized_inverse', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 11, 92,
    'exists_generalized_inverse_mod_ideal')
src('chart_witnesses', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 95, 142,
    'chart_witnesses_lemma')
src('formal_smooth_converse', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 145, 182,
    'formallySmooth_quotient_of_aeval_shift_mem_sq')
src('flat_chart_descent', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 186, 287,
    'exists_noetherian_subring_homogeneous_matrix_flat_charts')
src('coefficient_union', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 190, 251,
    'single finite coefficient subring and preservation of homogeneous entries')
src('flat_chart_installation', 'ExistsNoetherianSubringHomogeneousMatrixFlatChar.lean', 253, 287,
    'descended smoothness and explicit flat-chart retract')
src('formal_smooth_witnesses', 'ExistsWitnessesOfFormallySmoothQuotient.lean', 9, 72,
    'exists_sum_mul_of_mem_span_range_sq; exists_witnesses_of_formallySmooth_quotient')
src('flat_retract', 'FlatQuotSMulTopCokerOfMatrixWitnesses.lean', 10, 117,
    'flat_quotSMulTop_coker_of_matrix_witnesses')
src('grading', 'IsGradedMapLinearCombination.lean', 39, 54,
    'polyGrading and mem_polyGrading_iff', D)
src('graded_dehom', 'ExistsXPowSmulEqZeroOfEqXSubOneSmul.lean', 22, 216,
    'finite-support recurrences, homogenization and X_sub_one_smul_graded')
src('finite_quot_generators', 'ExistsXPowSmulMemSpanOfFiniteQuot.lean', 26, 167,
    'exists_X_pow_smul_mem_span_of_finite_quot')
src('homogeneous_union', 'ExistsHomogeneousFamilySaturating.lean', 9, 32,
    'exists_homogeneous_family_saturating')
src('finite_kernel', 'ExistsPowSmulEqAddSubOneSmul.lean', 63, 114,
    'finite_quotSMulTop_ker_of_regular; finite_quotSMulTop_ker_of_graded')
src('graded_presentation', 'ExistsGradedPresentationSaturating.lean', 11, 47,
    'exists_graded_presentation_saturating')
src('dehom_kernel', 'DehomogenisingEqZeroIff.lean', 9, 25,
    'dehomogenising_eq_zero_iff')
src('finite_chart_quotient', 'FiniteQuotSMulTopXSubOneOfChart.lean', 17, 74,
    'finite_quotSMulTop_X_sub_one_of_chart')
src('dehom_composite', 'DehomogenisingCompOfSaturating.lean', 22, 42,
    'dehomogenising_comp_of_saturating')
src('noetherian_model', 'DehomogenisingCompOfSaturating.lean', 44, 114,
    'exists_noetherian_model_grCube')
src('laurent_independence', 'LinearIndependentLaurentMonomial.lean', 8, 45,
    'linearIndependent_laurentMonomial')
src('laurent_span', 'SpanLaurentMonomialEqHomLoc.lean', 8, 49,
    'span_laurentMonomial_eq_homLoc')
src('laurent_basis', 'ExistsMonomialBasisCechCubePolynomialGrading.lean', 10, 90,
    'exists_basis_grCube_polyGrading and explicit Laurent representatives')
src('monomial_contraction', 'CubeComplexExactAtOfMonomialBasis.lean', 12, 71,
    'cubeComplex_above_exactAt; cubeComplex_exactAt_of_monomialBasis')
src('top_cohomology', 'TopClassSurjective.lean', 84, 110,
    'span_topClass; main top-class finiteness and exactness')
src('polynomial_cohomology', 'CubeComplexPolyGradingFiniteExact.lean', 11, 44,
    'finite_neg_sum_eq; cubeComplex_polyGrading_finite_exact')
src('free_cohomology', 'CubeComplexGrFreeFiniteAndExactAt.lean', 9, 33,
    'cubeComplex_grFree_finite_and_exactAt')
src('finite_cube_cohomology', 'FiniteHomologyCubeComplexGradedModule.lean', 9, 46,
    'finite_cubeComplex_grCube_homology')
src('finite_piece', 'FinitePieceOfPolyGradedSMul.lean', 9, 19,
    'finite_piece_of_polyGradedSMul')
src('cech_truncation', 'FiniteCechHomologyOfFiniteCubeHomology.lean', 9, 34,
    'finite_cycles_of_finite_homology; finite_cechHomology_of_finite_cubeHomology')
src('finite_cech_cohomology', 'FiniteGrCechHomology.lean', 11, 21,
    'finite_grCech_homology')
src('complex_definitions', 'IsIsoTermComparisonRestrictScalars.lean', 371, 411,
    'cubeComplex, cechComplex and their actual differentials', D)
src('homloc_definitions', 'ExistsAwayFracOfMemHomLoc.lean', 197, 328,
    'homLoc, representatives and localization restrictions', D)
src('homloc_bijection', 'ExistsAwayFracOfMemHomLoc.lean', 436, 454,
    'homLocMap_bijective_of_X', D)
src('cube_definitions', 'ExistsAwayFracOfMemHomLoc.lean', 577, 617,
    'grCube, grCubeMap and scalar-extension conventions', D)
src('singleton_dehom', 'NonemptyHomLocSingletonEquivQuotSMulTop.lean', 10, 43,
    'nonempty_homLoc_singleton_equiv_quotSMulTop')
src('flat_homloc', 'FlatHomLocOfFlatHomLocSingleton.lean', 8, 49,
    'flat_loc_over_algebra; flat_homLoc_of_flat_homLoc_singleton')
src('coker_basechange', 'IsBaseChangeCokerMatrixMvPolynomial.lean', 8, 61,
    'exists_isBaseChange_coker; isBaseChange_coker_matrix_mvPolynomial')
src('cube_basechange', 'NonemptyBaseChangeGrCubeIso.lean', 10, 56,
    'nonempty_baseChange_grCube_iso with restriction naturality')
src('gsl8_consumer', 'ExistsFiniteProjectiveComplexOfNoetherianModel.lean', 9, 60,
    'existing GSL8: arbitrary-base transfer of a Noetherian cube model')
src('perf_consumer', 'ThreeTermComplexOfProjectiveCechModel.lean', 106, 156,
    'existing GSL10: perf_of_projective_model')
src('geometric_consumer', 'ExistsFiniteProjectiveCechComplexLineBundle.lean', 19, 43,
    'exists_finite_projective_complex_cechLB: remaining actual geometric join')
src('affine_section_producer', 'SecOnFinitePresentationProjective.lean', 24, 65,
    'actual affine section-module localization, finite presentation and projectivity')
src('smooth_chart_producer', 'CstSmoothAndFlat.lean', 12, 20,
    'cst_smooth_and_flat')
src('geometric_dehom_producer', 'ExistsDehomogenisationTwistedChart.lean', 127, 189,
    'exists_dehom_top; exists_dehom_chart on the actual sections')
src('geometric_localization_producer', 'TwistedSectionsLocaliseToCharts.lean', 24, 50,
    'twisted_sections_localise')
src('geometric_killing_producer', 'ExistsNhdsPowMulTwCoordEqZero.lean', 48, 62,
    'exists_pow_mul_twCoord_eq_zero: one power from a finite subcover')
src('geometric_extension_producer', 'ExistsTwExtendPowMul.lean', 80, 171,
    'exists_tw_extend_pow_mul: local denominator clearing and overlap gluing')
src('geometric_cube_producer', 'ExistsTwistedSectionsCubeBijective.lean', 45, 63,
    'exists_grCube_twistedSections_hom_secCube_bijective')
src('perf_wrapper', 'AbelianSchemeLawProofs/NonemptyPerfectSectionsComplexOfSmoothProj.lean', 15, 22,
    'nonempty_perf_of_smooth_isProjBy: remaining geometric exit', P)
src('mathlib_pin', 'lake-manifest.json', 1, 16,
    'repository-declared Mathlib dependency pin', '')

files = {}
sources = {}
for key, path, lo, hi, declaration in rows:
    if path not in files:
        blob = subprocess.check_output(['git', '-C', str(args.source_root), 'show', PIN + ':' + path])
        local = (args.source_root / path).read_bytes()
        assert local == blob, 'Working source differs from pin: ' + path
        dest = HERE / 'source_snapshot' / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)
        files[path] = dict(path=path, snapshot_file=str(dest.relative_to(WORK)),
                           bytes=len(blob), line_count=len(blob.splitlines()), sha256=sha(blob),
                           file_sha256=sha(blob), source_commit=PIN,
                           verified_equal_to_pinned_git_blob=True,
                           url=REPO + '/blob/' + PIN + '/' + path)
    lines = (HERE / 'source_snapshot' / path).read_bytes().splitlines(keepends=True)
    assert 1 <= lo <= hi <= len(lines), (key, lo, hi, len(lines))
    body = b''.join(lines[lo-1:hi])
    rec = files[path]
    sources[key] = dict(id='FCD_SRC_' + key.upper(), path=path, declaration=declaration,
                        line_start=lo, line_end=hi, source_commit=PIN,
                        file_sha256=rec['sha256'], full_file_sha256=rec['sha256'],
                        range_sha256=sha(body), range_bytes=len(body),
                        snapshot_file=rec['snapshot_file'], verified_equal_to_pinned_git_blob=True,
                        url=rec['url'] + f'#L{lo}-L{hi}')

dependency_files = []
for path in sorted((HERE / 'source_snapshot' / 'mathlib').rglob('*.lean')):
    rel = str(path.relative_to(HERE / 'source_snapshot' / 'mathlib'))
    b = path.read_bytes()
    dependency_files.append(dict(repository=MREPO, dependency='mathlib', source_commit=MPIN,
        path=rel, snapshot_file=str(path.relative_to(WORK)), bytes=len(b),
        line_count=len(b.splitlines()), sha256=sha(b), file_sha256=sha(b),
        verified_by_pinned_raw_url=True,
        provenance_note='Downloaded at the exact Mathlib revision declared in lake-manifest.json; separately recorded from main-repository git blobs.',
        url=MREPO + '/blob/' + MPIN + '/' + rel))

specs = [
 ('FCD1', [], ['chart_witnesses','finite_kernel'], 'Finite relations for prescribed algebra generators and kernels of surjections from finite modules; arbitrary coefficient rings.'),
 ('FCD2', [], ['generalized_inverse'], 'Actual projective quotient, semilinear surjection and prescribed kernel yield Phi Psi Phi = Phi + sum g E.'),
 ('FCD3', ['FCD1','FCD2'], ['chart_witnesses'], 'All finite annihilator and splitting certificates from one original smooth chart.'),
 ('FCD4', [], ['formal_smooth_witnesses','formal_smooth_converse'], 'Both directions of the polynomial formal-smoothness certificate over arbitrary R; no flatness assumed.'),
 ('FCD5', [], ['flat_chart_installation','mathlib_pin'], 'Noetherian flatness via a proved Rees-module Artin-Rees argument, exact completion, compatible formal-smooth lifts and retract.'),
 ('FCD6', ['FCD5'], ['flat_retract'], 'Explicit maps j and p, well-definedness, p j = 1 and flatness of the actual dehomogenized cokernel.'),
 ('FCD7', [], ['coefficient_union','grading'], 'One finite coefficient subring; injectivity descends identities and all integer homogeneous degrees.'),
 ('FCD8', ['FCD3','FCD4','FCD5','FCD6','FCD7'], ['flat_chart_descent'], 'Full original all-chart matrix descent; arbitrary R; projectivity over the original chart algebras; one R0 and Phi0.'),
 ('FCD9', [], ['graded_dehom'], 'Regularity of X-1, power-killing of homogeneous multiples, and all sufficiently large homogeneous representatives.'),
 ('FCD10', ['FCD9'], ['finite_quot_generators','homogeneous_union'], 'Finite homogeneous generators up to chart powers, simultaneously over all charts; no finite generation of the original graded module required.'),
 ('FCD11', ['FCD1','FCD9'], ['finite_kernel'], 'Finite dehomogenization of the actual graded kernel; arbitrary R and finite F, not necessarily finitely presented F.'),
 ('FCD12', ['FCD10','FCD11'], ['graded_presentation'], 'Full original finite graded presentation with actual map and both elementwise chart-power torsion conditions.'),
 ('FCD13', ['FCD1','FCD9'], ['dehom_kernel','finite_chart_quotient'], 'Actual quotient identification and both finiteness/finite-presentation transports from the original chart module.'),
 ('FCD14', ['FCD9','FCD13'], ['dehom_composite'], 'Full original composite dehomogenization, without requiring the coefficient map to be surjective or G to have a direct-sum grading.'),
 ('FCD15', [], ['laurent_independence','laurent_span','laurent_basis','monomial_contraction','top_cohomology','polynomial_cohomology','free_cohomology','finite_cube_cohomology','finite_piece','cech_truncation','finite_cech_cohomology','complex_definitions'], 'Finite graded Cech cohomology for every integer degree and cohomological degree; explicit contraction, top classes, dimension shifting and degree-zero truncation.'),
 ('FCD16', ['FCD9'], ['singleton_dehom','flat_homloc','homloc_definitions'], 'Singleton degree-zero dehomogenization and flatness at every degree of every containing nonempty localization vertex.'),
 ('FCD17', ['FCD16'], ['coker_basechange','cube_basechange','homloc_bijection','cube_definitions'], 'Actual scalar-extension cube isomorphism and saturated localization maps; no flatness of the coefficient map; restriction naturality.'),
 ('FCD18', ['FCD8','FCD12','FCD13','FCD14','FCD15','FCD16','FCD17'], ['noetherian_model'], 'Full original exists_noetherian_model_grCube: one R0/C0/theta, flat nonempty vertices, every finite Cech cohomology and actual bijective nonempty comparisons.')
]
lines = proof.splitlines(keepends=True)
text = proof.decode()
claims = []
for ident, deps, groups, scope in specs:
    start = next(i for i,l in enumerate(lines) if l.strip() == ('% BEGIN '+ident).encode())
    end = next(i for i,l in enumerate(lines) if l.strip() == ('% END '+ident).encode())
    block = b''.join(lines[start:end+1])
    title = re.search(r'\\paragraph\{' + ident + r':\s*(.*?)\}', block.decode(), re.S).group(1)
    claims.append(dict(id=ident, title=title, introduced_in='0.53', classification='B',
        depends_on=deps, external_input_ids=['FCD_STANDARD'], scope_note=scope,
        source_groups=groups, sources=[sources[g] for g in groups],
        proof_location=dict(file=COMP+'/main.tex', label='claim:'+ident,
            line_start=start+1, line_end=end+1, sha256=sha(block), bytes=len(block)),
        proof_status='complete at the stated original mathematical hypotheses',
        status='complete human proof; pending independent review',
        scope_class='complete_at_original_mathematical_hypotheses',
        source_proof_is_not_human_proof=True))

inherited = []
prev = json.loads((WORK/'global_section_laws_v52/provenance.json').read_text())
for ident in ['GSL8','GSL9','GSL10']:
    q = next(c for c in prev['claims'] if c['id']==ident)
    data = (WORK/q['proof_location']['file']).read_bytes()
    assert sha(data)==prev['proof_file_sha256']
    loc=q['proof_location']; ls=data.splitlines(keepends=True)
    assert sha(b''.join(ls[loc['line_start']-1:loc['line_end']]))==loc['sha256']
    inherited.append(dict(id=ident, component='global_section_laws_v52', title=q['title'],
        proof_file=loc['file'], proof_file_sha256=prev['proof_file_sha256'],
        proof_block_sha256=loc['sha256'], proof_location=loc, source_commit=PIN,
        use=('GSL8 consumes the now-proved FCD18 model; GSL9/GSL10 remain the unchanged actual-section and Perf join once the geometric comparison is supplied.'),
        role='downstream reuse; not a premise of any numbered FCD proof',
        all_original_premises_retained=True))

def declaration(key):
    s=sources[key]; b=(WORK/s['snapshot_file']).read_bytes().splitlines(keepends=True)
    return b''.join(b[s['line_start']-1:s['line_end']]).decode().split(':= by',1)[0].strip()

standard = dict(id='FCD_STANDARD', name='Conventional elementary commutative and homological algebra',
    kind='standard_background_not_a_selected_project_gap',
    scope_note=('Ring/module and formal-smoothness definitions, projective lifting, Hilbert basis theorem, '
                'tensor right exactness and ideal criterion for flatness, exact localization, '
                'direct sums/filtered limits of modules and long exact cohomology sequences. '
                'The particular finite-presentation kernel argument, formal-smoothness certificates, '
                'Artin-Rees inclusion, completion flatness, and all model producers are proved in this packet.'),
    sources=[sources['mathlib_pin']], supporting_dependency_sources=dependency_files,
    globally_discharged_by_this_component=False)

remaining = [
 dict(id='FCD_ACTUAL_AFFINE_SECTIONS', name='Finite presentation and projectivity of actual line-bundle sections on affine charts',
      sources=[sources['affine_section_producer']], already_proved_here=False),
 dict(id='FCD_ACTUAL_SMOOTH_CHARTS', name='Original affine chart coordinate algebra is smooth over the original base',
      sources=[sources['smooth_chart_producer']], already_proved_here=False),
 dict(id='FCD_ACTUAL_GEOMETRIC_DEHOM', name='Division by the original s_i and actual section localization/extension',
      sources=[sources['geometric_dehom_producer'],sources['geometric_localization_producer'],
               sources['geometric_killing_producer'],sources['geometric_extension_producer']], already_proved_here=False),
 dict(id='FCD_ACTUAL_GEOMETRIC_CUBE', name='Actual graded-section cube comparison, natural under every restriction, followed by the fixed M tensor H^0 identification',
      sources=[sources['geometric_cube_producer'],sources['geometric_consumer']], already_proved_here=False)
]
unchanged = ['GSL_POL_BASE_CHANGE','GSL_SERRE','GSL_MUL_PULL','GSL_MUL_GEOMETRY',
             'GSL_TORSION_DESCENT','GSL_GEOM_INTEGRAL','GSL_RANK_ONE',
             'GSL_SECTION_DECOMP','GSL_FINITE_GROWTH','GSL_SQUARE',
             'Original Moduli record and inherited HUF/PUN foundations']

endpoints = []
for ident,key,description in [
 ('FCD8','flat_chart_descent','One Noetherian subring and homogeneous presentation with every dehomogenized chart flat.'),
 ('FCD12','graded_presentation','One finite homogeneous presentation and actual map with chart-power torsion kernel and cokernel.'),
 ('FCD18','noetherian_model','One actual Noetherian graded cube model with all three original output clauses.')]:
    header=declaration(key)
    endpoints.append(dict(claim_id=ident, source=sources[key], exact_source_declaration_header=header,
        declaration_header_sha256=sha(header.encode()), output=description,
        status='complete at all original hypotheses; no newly assumed opaque producer'))

write('provenance.json', dict(schema='rh-proof-provenance/1', **base, source_repository=REPO,
    claims=claims, new_claim_count=len(claims), original_endpoints=endpoints,
    supporting_dependency_sources=dependency_files, independent_reviews=[]))
write('source_manifest.json', dict(schema='rh-source-manifest/1', **base, repository=REPO,
    snapshot_root=COMP+'/source_snapshot', files=list(files.values()), ranges=list(sources.values()),
    file_count=len(files), range_count=len(sources), total_bytes=sum(f['bytes'] for f in files.values()),
    all_files_verified_equal_to_pinned_git_blobs=True,
    dependency_repository=MREPO, dependency_commit=MPIN, dependency_files=dependency_files,
    dependency_file_count=len(dependency_files), dependency_total_bytes=sum(f['bytes'] for f in dependency_files)))
write('contracts.json', dict(schema='rh-component-contracts/1', **base,
    claim_ids=[c['id'] for c in claims], completed_original_suppliers=endpoints,
    quantifier_guards=[
        'R is an arbitrary commutative ring, including zero; no reducedness, Noetherianity, field, or flat coefficient extension is assumed.',
        'FCD8: for every fixed homogeneous Phi and every chart i with its supplied smooth algebra/projective module/actual semilinear surjection, choose ONE R0 and Phi0 before proving flatness for every i.',
        'FCD12: both chart-power torsion statements hold for every element, with powers allowed to depend on the element and chart; G itself need not be finite.',
        'FCD14: no surjectivity of pi is needed; N is graded, while only the stated target homogeneous pieces are needed in G.',
        'FCD15: all integer homogeneous degrees and all nonnegative cohomological degrees, including empty index sets and ordinary-Cech degree zero.',
        'FCD18: fixed original G and actual chart data produce one R0/C0/theta before later coefficient maps; only NONEMPTY vertices are required flat or bijective.',
        'FCD17: scalar extension of the actual presentation/cube is canonical even for a nonflat ring map.',
        'The actual geometric section module and its comparison maps remain unsupplied until the listed geometric producers are reconstructed; no global Perf, section law or Moduli supplier is claimed.'
    ], inherited_inputs=inherited, external_inputs=[standard], remaining_actual_geometric_producers=remaining,
    global_section_laws_unconditionally_supplied=False, selected_whole_obligations_closed=[], independent_reviews=[]))
write('inherited_inputs.json', dict(schema='rh-inherited-inputs/1', **base, inputs=inherited))
write('retained_foundations.json', dict(schema='rh-retained-foundations/1', **base, inputs=[standard],
    remaining_actual_geometric_producers=remaining, separate_unchanged_boundary=unchanged))
write('explicit_inputs.json', dict(schema='rh-explicit-inputs/1', **base,
    inputs=[standard], original_pointwise_interfaces=endpoints,
    actual_geometric_inputs_not_yet_globally_supplied=remaining,
    scope_note='The original chart hypotheses are inputs to fully proved algebraic theorems. Their actual geometric producers remain separate; none of the three completed target theorems is assumed.'))
write('closure.json', dict(schema='rh-component-closure/1', **base, new_claim_count=len(claims),
    completed=['Original simultaneous homogeneous-matrix flat-chart descent.',
               'Finite polynomial smoothness, generalized-inverse and annihilator certificates; explicit common coefficient ring and flatness retract.',
               'Finite graded presentation correct up to elementwise chart-power torsion.',
               'Full finite graded Cech cohomology and literal localization/base-change comparison.',
               'Original exists_noetherian_model_grCube with every original output field.'],
    completed_original_endpoint_claim_ids=['FCD8','FCD12','FCD18'],
    formerly_retained_subproducer_now_supplied='The original Noetherian graded-cube model theorem (the algebraic core of GSL_PERF_GEOMETRY).',
    pending_actual_geometric_producers=[r['id'] for r in remaining],
    unchanged_upstream_boundary=unchanged, globally_supplied_laws=[],
    global_section_laws_unconditionally_supplied=False,
    selected_whole_obligations_closed=[], selected_obligation_statuses_unchanged=True,
    earlier_proof_components_modified=[], graph_nodes_added=0, graph_edges_added=0,
    independent_reviews=[]))
write('hashes.json', dict(schema='rh-component-hashes/1', **base,
    proof_blocks={c['id']:c['proof_location']['sha256'] for c in claims},
    primary_source_files={f['path']:f['sha256'] for f in files.values()},
    dependency_source_files={f['path']:f['sha256'] for f in dependency_files}))
print(json.dumps(dict(component=COMP, proof_sha256=proof_sha, claims=len(claims),
                     primary_files=len(files), source_ranges=len(sources),
                     dependency_files=len(dependency_files)), indent=2))
