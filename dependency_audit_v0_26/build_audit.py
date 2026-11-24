#!/usr/bin/env python3
"""Build the v0.26 semantic sufficient-condition audit; preserve all old bytes."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OLD = WORK / 'dependency_audit_v0_25'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
COMPONENTS = ['rank_one_cohomology', 'bernoulli_residual_vanishing',
              'framed_deformation_presentation', 'symplectic_count_closure',
              'point_hv_assembly']
MATHEMATICAL_REVIEW_PREFIXES = (
    'bernoulli_residual_', 'point_hv_', 'rank_one_cohomology_',
    'symplectic_algebra_', 'symplectic_count_closure_',
    'weighted_intersection_', 'framed_deformation_', 'framed_presentation_',
    'integration_scope_review')
REVIEW_WRITERS = {'write_root_reviews.py', 'write_framed_root_review.py'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main(repo):
    blobs, source_index, input_index = {}, {}, {}
    proof_checks, component_claims, ledgers = [], {}, {}
    component_manifest_checks = 0

    def file_input(p):
        input_index[str(p.relative_to(WORK))] = {
            'path': str(p.relative_to(WORK)), 'sha256': sha(p.read_bytes()),
            'bytes': p.stat().st_size}

    def blob(path):
        if path not in blobs:
            b = (repo / path).read_bytes()
            assert b == subprocess.check_output(
                ['git', '-C', str(repo), 'show', PIN + ':' + path]), path
            blobs[path] = b
        return blobs[path]

    def verify(a):
        b = blob(a['path'])
        fragment = b''.join(b.splitlines(keepends=True)[a['line_start']-1:a['line_end']])
        assert sha(b) == a['sha256'], a['path']
        assert sha(fragment) == a['range_sha256'], (a['path'], a['line_start'])
        assert PIN in a['url'], a['url']
        source_index[(a['path'], a['line_start'], a['line_end'])] = copy.deepcopy(a)
        return a

    def anchor(path, decl, start=None, end=None):
        b = blob(path)
        lines = b.decode().splitlines()
        if start is None:
            pat = re.compile(r'^(?:private\s+)?(?:theorem|def|abbrev|structure)\s+' +
                             re.escape(decl) + r'(?=[\s:(])')
            matches = [i+1 for i, s in enumerate(lines) if pat.match(s)]
            assert len(matches) == 1, (path, decl, matches)
            start = matches[0]
        if end is None:
            end = len(lines)
            for i in range(start, len(lines)):
                if re.match(r'^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure|section|namespace|end|variable|instance|attribute|open)\b|^@\[', lines[i]):
                    end = i
                    break
            while end > start and not lines[end-1].strip():
                end -= 1
        fragment = b''.join(b.splitlines(keepends=True)[start-1:end])
        return verify({'path': path, 'declaration': decl, 'line_start': start,
                       'line_end': end, 'sha256': sha(b),
                       'range_sha256': sha(fragment), 'range_bytes': len(fragment),
                       'first_line': lines[start-1],
                       'url': REPO + '/blob/' + PIN + '/' + path + f'#L{start}-L{end}',
                       'verified_equal_to_pinned_git_blob': True})

    baseline = read(OLD / 'obligation_map.json')
    assert len(baseline['nodes']) == 67
    old_targets = read(OLD / 'next_targets.json')['targets']
    for a in old_targets:
        verify(a)
    for a in read(OLD / 'source_anchors.json')['sources']:
        verify(a)
    # The preceding release and all its indexed mathematical inputs stay fixed.
    for a in read(OLD / 'input_manifest.json')['files']:
        p = WORK / a['path']
        assert sha(p.read_bytes()) == a['sha256'], a['path']
    for name in ['obligation_map.json', 'audit.txt', 'input_manifest.json',
                 'next_targets.json', 'source_anchors.json']:
        file_input(OLD / name)

    for name in COMPONENTS:
        directory = WORK / name
        ledger = read(directory / 'provenance.json')
        ledgers[name] = ledger
        b = (directory / 'main.tex').read_bytes()
        expected = ledger.get('main_tex_sha256', ledger.get('validation', {}).get('main_tex_sha256'))
        assert sha(b) == expected, name
        claims = ledger['claims']
        component_claims[name] = [c['id'] for c in claims]
        for claim in claims:
            for a in claim['sources']:
                verify(a)
            loc = claim.get('proof_location', claim.get('human_proof'))
            assert loc is not None, claim['id']
            b = (WORK / loc['file']).read_bytes()
            fragment = b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
            assert sha(fragment) == loc['sha256'], claim['id']
            proof_checks.append(claim['id'])
        for group in ledger.get('retained_frontier', []):
            for a in group['sources']:
                verify(a)
        manifest = directory / 'input_manifest.json'
        if manifest.exists():
            for a in read(manifest).get('files', []):
                p = WORK / a['path']
                assert sha(p.read_bytes()) == a['sha256'], a['path']
                component_manifest_checks += 1
                file_input(p)
        for p in sorted(directory.iterdir()):
            if p.is_file() and (p.suffix in {'.json', '.tex', '.py'} or p.name in {'report.txt', 'report.md'}):
                file_input(p)

    all_new_claims = {c for values in component_claims.values() for c in values}
    assert len(all_new_claims) == sum(map(len, component_claims.values()))
    assert component_claims['framed_deformation_presentation'][-1] == 'FP8'
    for p in sorted((WORK / 'reviews_v0_26').glob('*')):
        downstream = any(s in p.name for s in ('audit', 'coverage', 'package', 'final_scope', 'semantic_scope'))
        mathematical = (p.suffix in {'.json', '.txt', '.md'} and
                        p.name.startswith(MATHEMATICAL_REVIEW_PREFIXES))
        if p.is_file() and not downstream and (mathematical or p.name in REVIEW_WRITERS):
            file_input(p)
    for name in ['configure_v0_26.py', 'increment_v0_26.json']:
        p = WORK / name
        if p.exists():
            file_input(p)

    retirement = {
        'DA25-HV-05': (['BR7'], 'Literal CorX on the original arbitrary residue field, both character and inverse character, prescribed dyadic conductor and exact tame-index UnrEv.'),
        'DA25-HV-06': (['RV3'], 'Literal SoFin for every original number field/closure, finite coefficient DVR, finite-order open-kernel character, every prime and e>=1; no prime-to-ell character-order restriction.'),
        'DA25-HV-07': (['RV7'], 'Literal SoV/soBar for the actual algebraic-coefficient cocycle and every original local valuation condition; Baire finite-field capture and original-field witness are proved.')}

    updates = {
        'DA-next-01-b': {
            'human_status': 'PointHV_assembly_complete_actual_four_count_suppliers_remain',
            'supplied_by': ['LD3', 'LK2', 'LK3', 'KB8', 'CZ6', 'HV5', 'HV6', 'HV10'],
            'supplied_parts': ['Literal CountZ0, CountVs and CountIV', 'Original-field eigencharacter comparison at every odd prime', 'Uniform case/layer/finite-prime sum assembly to literal PointHV'],
            'remaining_human_scope': 'Supply actual CountI, CountII, CountIII and CountV with their unchanged original host/character/coefficient quantifiers and uniform constants. HV10 now proves their full implication to PointHV; no separate original-field case, layer or sum assembly remains.',
            'retained_inputs': 'Only the four actual count predicates within this cohomological assembly, plus inherited precisely matched classical inputs. Their automorphy, rigidity, catalogue and actual model premises are not supplied by HV10.'},
        'DA24-HV-06': {
            'human_status': 'CountI_actual_Kato_unitary_and_cohomology_suppliers_retained_general_algebra_leaves_supplied',
            'supplied_by': ['KB8', 'SP1', 'SP6', 'FP8'],
            'supplied_parts': ['Literal LemmaK31', 'Literal general LemmaMprime, LemmaM and LemmaP'],
            'remaining_human_scope': 'Construct the actual CohInp/InpZ arithmetic instance, RigII from KatoTwo, adjoint vanishing, rank-three congruence-number control and AutomorphyUnramifiedCoefficients; reconstruct OneChar -> PropGK -> CorGK -> CountI on the original objects. The theorem hypotheses of LemmaP and the M-model identifications must hold on those actual data.',
            'retained_inputs': 'Actual cohomology/period-ring and normalized global packages, KatoTwo/RigII, modularity/adjoint vanishing, rank-three trace counting and compatible arithmetic model installation. No general M/Mprime/P theorem remains as an unproved leaf.'},
        'DA25-HV-02': {
            'human_status': 'actual_one_character_arithmetic_comparison_retained_general_algebra_supplied',
            'supplied_by': ['SP1', 'SP6', 'FP8'],
            'remaining_human_scope': 'Actual OneChar from the original InpZ and AutomorphyUnramifiedCoefficients; preserve its rank-three/rank-two automorphic points and trace differences, then complete PropGK/CorGK and CountI.',
            'retained_inputs': 'CohInp, RigII/KatoTwo, AdVanishK, CongruenceNumberRankThree and AutomorphyUnramifiedCoefficients, with actual local conditions, framed obstruction finiteness and model comparisons. The generic M/Mprime/P implications are supplied by SP1/SP6/FP8.'},
        'DA25-HV-03': {
            'human_status': 'paired_count_arithmetic_and_coefficient_join_complete_G1_G2_catalogue_retained',
            'supplied_by': ['RV1', 'RV3', 'RV7', 'BR7', 'SP1', 'SP6', 'SP7', 'SP8', 'SP9', 'SP10', 'FP8'],
            'supplied_parts': ['Literal SoFin, SoV, CorX, LemmaMprime, LemmaM and LemmaP', 'shaCoc/mPrime for each actual supplied Model with its source GradedAlgebra structure', 'Exact coefficient invariants and normalized return', 'Uniform integer/valuation/count join conditional on the stated G1/G2/catalogue'],
            'remaining_human_scope': 'Supply the exact G1 actual Raw/Good/OfCase, level/safe admissible-class and common-embedding construction; G2 actual Model with its source GradedAlgebra Model.gr, M1-M4 and two-sided point/trace/orbit comparisons; and the uniform finite catalogue of SP9. The source route retains actual CohomologyHyp, SymplecticFourImageDense, RigiditySymplecticFour and automorphic/local-level classification and counting.',
            'retained_inputs': 'SP-R1, SP-R2 and SP-R3 exactly as symplectic_count_closure/remaining_inputs.json. Generic theorem availability does not prove the internal dataEx/exModel or arithmetic comparison edges.'},
        'DA25-HV-08': {
            'human_status': 'CountV_actual_host_frame_arithmetic_and_native_duality_retained_M_leaves_supplied',
            'supplied_by': ['SP1', 'SP6'],
            'remaining_human_scope': 'Full actual large-conductor CountV on the original host frame, marked point, universal ring and automorphic point predicate, with exact normalized coefficient descent. Apply the now-proved M/Mprime on that actual model; CountVs is a distinct complementary theorem and does not supply CountV.',
            'retained_inputs': 'ThmS6_s; native non-K LocalFiniteness, LocalTateDuality, LocalEulerChar, GlobalFiniteness, GlobalEulerChar and PoitouTateNormalised; HostVanE, HostXpp, HostRigid_s and HostNumber_s; their actual model installation and comparisons.'}}

    for tid, name in [('DA24-HV-01', 'CountI'), ('DA24-HV-02', 'CountII'),
                      ('DA24-HV-03', 'CountIII'), ('DA24-HV-04', 'CountV')]:
        updates[tid] = {
            'human_status': 'actual_' + name + '_supplier_still_open_downstream_PointHV_assembly_closed',
            'supplied_by': (['SP1', 'SP6', 'FP8'] if name == 'CountI' else
                            ['SP1', 'SP6'] if name == 'CountV' else
                            ['RV3', 'RV7', 'BR7', 'SP1', 'SP6', 'SP7', 'SP8', 'SP9', 'SP10', 'FP8']),
            'remaining_human_scope': ('Literal ' + name + ' on its original hosts, coefficients, characters and twists, with constants chosen before the varying host data. ' +
                                      ('SP10 proves the paired-count join only after the exact G1/G2/catalogue are supplied; their actual arithmetic and model construction remains.' if name in {'CountII', 'CountIII'} else
                                       'Its actual automorphy, rigidity, trace-counting, native cohomology and model-comparison content remains.')),
            'retained_inputs': ('Exact G1/G2/catalogue of SP-R1/SP-R2/SP-R3; source arithmetic suppliers and internal construction/comparison edges remain.' if name in {'CountII', 'CountIII'} else
                               'Actual arithmetic ' + name + ' supplier; proved general algebraic theorems do not instantiate its geometric hypotheses.'),
            'downstream_supplied': 'HV10: all four actual counts imply literal PointHV; VW/TW/OB/QP preserve the complete fixed-pair window chain.'}

    targets, retired = [], []
    for old in old_targets:
        q = copy.deepcopy(old)
        q.setdefault('history', []).append({'version': '0.25', 'snapshot': copy.deepcopy(old)})
        if q['id'] in retirement:
            suppliers, scope = retirement[q['id']]
            q.update(status='safe_to_retire_in_stated_scope', supplied_by=suppliers, closed_scope=scope)
            retired.append(q)
        else:
            q.update(updates.get(q['id'], {}))
            targets.append(q)
    assert {t['id'] for t in retired} == set(retirement)

    frontier = read(WORK / 'symplectic_count_closure' / 'remaining_inputs.json')['source_frontier']
    groups = {g['name']: g for g in frontier}
    for group in frontier:
        for a in group['sources']:
            verify(a)

    def front_target(tid, group_name, suffix, scope, premises, package):
        group = groups[group_name]
        matches = [a for a in group['sources'] if a['declaration'].split('.')[-1] == suffix]
        assert len(matches) == 1, (group_name, suffix)
        q = copy.deepcopy(matches[0])
        q.update(id=tid, work_package=package, priority_group=4,
                 status='human_proof_retained', human_status='precise_remaining_actual_supplier_or_comparison',
                 remaining_human_scope=scope, retained_inputs=premises,
                 supporting_sources=copy.deepcopy(group['sources']),
                 downstream='G1/G2/catalogue -> SP10 actual CountII and CountIII -> HV10 PointHV -> VW/TW/OB/QP windows')
        targets.append(q)
        return q

    front_target('DA26-SP-01', 'G1 actual data, level and admissible class', 'dataEx',
                 'Close the full G1 chain: original Raw/Good/OfCase with the prescribed n-prime,p1,m0, local characters and level; levOf/level/safe4-prime and one common embedding place every actual irreducible point in literal AdmRAlt. dataEx alone does not complete G1.',
                 'BR7 supplies literal CorX and SP8/RV1 supply coefficient enlargement/return. Actual SymplecticFourImageDense and the internal original-data, level and safe-class comparisons remain.', 'actual_symplectic_model')
    front_target('DA26-SP-02', 'G2 actual model and comparisons', 'exModel',
                 'Construct the actual weighted Model D on the same original Good Raw: provide PhiCond, Nums and LocBase, install the framed presentation and retain the exact origin, equations, weights, universal representation and derivation lifting.',
                 'FP8 supplies the universal LemmaP theorem, not PhiCond, local-condition axioms, local base points, finite framed obstruction spaces or the actual compatible local bases. CohomologyHyp and its same-data applications remain.', 'actual_symplectic_model')
    front_target('DA26-SP-03', 'G2 actual model and comparisons', 'aSmooth',
                 'Complete the remaining G2 comparison on that actual Model: the source GradedAlgebra Model.gr via aW, then aSmooth/m1b/m2/m3/m4; two-sided point lifts and irreducibility; the exact trace element; conjugate representations implying the same torus orbit. Keep the original first-weight-zero algebra and local conditions.',
                 'Actual Model D, SymplecticFourImageDense, RigiditySymplecticFour and CohomologyHyp in their precise source scopes. SP1/SP6 and SP7 do not assert these hypotheses; RV3/RV7 supply only the stated rank-one cohomology portions.', 'actual_symplectic_model')
    front_target('DA26-SP-04', 'CohomologyHyp', 'CohomologyHyp',
                 'Match the entire actual symplectic CohomologyHyp record, including its global finiteness/Euler, orthogonality/Greenberg-Wiles and local published period-ring clauses, with original local groups, coefficients, cup maps and conventions.',
                 'LD3 and LK2-LK4 supply identified finite duality/native local-K statements only. Arbitrary period-ring records and differently normalized global/local interfaces remain to be matched; no blanket inference from similarly named theorems.', 'actual_symplectic_model')
    front_target('DA26-SP-05', 'NumberSp4Alt', 'countQ_alt',
                 'Supply the complete uniform finite catalogue used in SP9: the exact four-dimensional weight/level admissible class, polynomial size, algebraic integrality, Aut(C) permutation, purity bound, injective classification and original-place arithmetic Frobenius formula. Catalogue precedes ell, Omega, embedding and family.',
                 'Actual Hypotheses-prime, LevelPNAlt, AdmResNAlt and AdmRAlt-to-AdmRNAlt comparisons with EigData/Classifies. SP9 proves the integer-product and valuation packaging only after this catalogue exists.', 'uniform_automorphic_catalogue')
    front_target('DA26-SP-06', 'RigiditySymplecticFour', 'rigSp4_alt',
                 'Supply actual RigiditySymplecticFour on the specified original EPt points, with the exact adjoint lifting and unramified deformation inputs; propagate it to M4 on the same Model.',
                 'The source UnramifiedInputs and AdjointLiftingTheorem with every local/global compatibility remain. A generic rigidity theorem or a differently normalized local package is insufficient.', 'actual_symplectic_model')

    unkeyed = anchor('src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean', 'VWinAt')
    global_scope_updates = [{
        'match': {'path': unkeyed['path'], 'declaration': 'UpperTheory.Top.VWinAt'},
        'source': unkeyed,
        'human_status': 'Complete conditional cohomological window chain; four actual count predicates remain',
        'remaining_human_scope': 'TW8 supplies simultaneous ThmBab and OB8 supplies ThmBcFree240. HV10 now supplies the full original-field CountI/II/III/V-to-PointHV assembly, including CountVs/IV and all case/layer/sum joins. The four actual arithmetic counts remain; prime-pair classical inputs, compatible host installation and global arithmetic family/gap remain in their original scopes.',
        'supplied_by': ['TW8', 'OB8', 'HV5', 'HV6', 'HV10', 'VW3', 'VW4', 'QP22']}]

    m = copy.deepcopy(baseline)
    m.update(artifact_version='0.26', baseline='0.25', previous_map='previous_obligation_map.json',
             increment_integration='RV/BR close literal SoFin, SoV, coefficient independence and CorX; SP closes M/Mprime and the conditional G1/G2/catalogue arithmetic return; FP closes universal LemmaP; HV closes CountVs/IV and all four-count-to-PointHV-to-window assembly. Actual CountI/II/III/V and the global actual-family/gap/theta/metric/spectral frontier remain.')
    byid = {n['id']: n for n in m['nodes']}
    changed = []

    def update(nid, **kwargs):
        n = byid[nid]
        previous = copy.deepcopy(n)
        n.setdefault('history', []).append({'version': '0.25', 'snapshot': previous})
        n.update(kwargs)
        changed.append(nid)

    def node(nid, title, gate='LEAF', **kwargs):
        assert nid not in byid, nid
        n = {'id': nid, 'title': title, 'gate': gate, 'introduced_in': '0.26', **kwargs}
        m['nodes'].append(n)
        byid[nid] = n

    node('CLASSICAL_RANK_ONE_FIELDS', 'Matched finite local-field valuation and completeness',
         status='named_classical_input_with_written_cocycle_capture', registry='rank_one_cohomology/classical_inputs.json', input_ids=['RV-LF'])
    node('RANK_ONE_FINITE_SELMER', 'Literal SoFin on original finite character coefficients', gate='AND',
         requires=['LEMMA_K_BOUND', 'LOCAL_K_INTERFACE_MATCH', 'FINITE_DUALITY_SPECIALIZATION'],
         status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['RV1', 'RV2', 'RV3'],
         premise='All original number fields/closures and coefficient DVRs, every prime and finite-order character, e>=1. Character order may be divisible by ell; original quotient action and all local conditions retained.')
    node('ALGEBRAIC_COEFFICIENT_VANISHING', 'Literal SoV with actual algebraic-coefficient capture', gate='AND',
         requires=['RANK_ONE_FINITE_SELMER', 'CLASSICAL_RANK_ONE_FIELDS'],
         status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['RV4', 'RV5', 'RV6', 'RV7'],
         premise='Baire is applied to closed cocycle subgroups, not arbitrary compact subsets of PadicAlgCl. Original coefficient-field witness and every local condition are retained.')
    node('EXACT_COEFFICIENT_RETURN', 'Original coefficient independence and normalized length', gate='AND',
         requires=['RANK_ONE_FINITE_SELMER', 'ALGEBRAIC_COEFFICIENT_VANISHING'],
         status='human_actual_interface_supplier_complete', claims=['RV1', 'RV6', 'RV7', 'SP8'],
         premise='Same original closure/character/local family; finiteness equivalent, exact length and v_O(ell) scale by the same ramification factor. Order, unit kernel, conductor, parity and case survive arbitrary allowed finite coefficient extension.')
    node('BERNOULLI_PRESCRIBED_CONDUCTOR', 'Literal dyadic-conductor Bernoulli unit LemmaX',
         status='complete_human_finite_arithmetic_supplier', claims=['BR1', 'BR2', 'BR3'],
         premise='Exact f*4^e<=2^n cutoff and original finite coefficient DVR; finite Frobenius projection and partial Bernoulli identity avoid division by f.')
    node('CLASSICAL_RESIDUAL_ARITHMETIC', 'Finite Hilbert class field and cyclotomic Galois inputs',
         status='named_classical_inputs_with_written_original_residue_specializations', registry='bernoulli_residual_vanishing/classical_inputs.json', input_ids=['BR-CFT', 'BR-CYC'])
    node('JACOBI_PRINCIPAL_RELATION', 'Previously proved finite Jacobi principal-ideal relation', gate='AND',
         requires=['CLASSICAL_FINITE_ARITHMETIC'], status='human_supplier_complete_in_used_scope', claims=['OS1'],
         premise='Only OS1 principal-ideal relation is used; BR proves the arbitrary-positive-index extension and the twice-Eone reindexing. The full integral ClKill/HomKill predicates are not inferred.')
    node('COR_X_RESIDUAL_SUPPLIER', 'Literal CorX on both original residue characters', gate='AND',
         requires=['BERNOULLI_PRESCRIBED_CONDUCTOR', 'JACOBI_PRINCIPAL_RELATION', 'CLASSICAL_RESIDUAL_ARITHMETIC'],
         status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['BR4', 'BR5', 'BR6', 'BR7'],
         premise='Original arbitrary k and possibly nonsurjective O->k; both character and inverse; exact tame-index UnrEv; no prime-to-ell assumption on the cyclotomic field degree.')
    node('CLASSICAL_COMMUTATIVE_ALGEBRA', 'Matched finite-module and commutative-algebra facts',
         status='named_classical_inputs_with_written_specializations', registry='symplectic_count_closure/classical_inputs.json', input_ids=['SP-C1', 'SP-C2', 'SP-C3'])
    node('LEMMA_M_PRIME', 'Literal additive-injection cotangent bound LemmaMprime', gate='AND',
         requires=['CLASSICAL_COMMUTATIVE_ALGEBRA'], status='human_general_algebraic_theorem_complete', claims=['SP1'],
         premise='Specified additive injection and derivation lifting suffice; no new O-linearity assumption.')
    node('LEMMA_M', 'Literal two-sided orbit valuation bound LemmaM', gate='AND',
         requires=['CLASSICAL_COMMUTATIVE_ALGEBRA'], status='human_general_algebraic_theorem_complete', claims=['SP2', 'SP3', 'SP4', 'SP5', 'SP6'],
         premise='Every given algebra satisfying M1-M5 has a finite two-sided cover and the exact factor-two cotangent inequality. Finite cover consists entirely of two-sided points; M1-M5 are theorem antecedents, not supplied arithmetic data.')
    fp_registry = read(WORK / 'framed_deformation_presentation' / 'classical_inputs.json')
    fp_inputs = fp_registry.get('inputs', [])
    fp_ids = list(fp_inputs) if isinstance(fp_inputs, dict) else [q['id'] for q in fp_inputs]
    node('CLASSICAL_FRAMED_ALGEBRA', 'Matched Noetherian power-series and Nakayama inputs',
         status='named_classical_algebra_inputs_with_written_formal_specializations',
         registry='framed_deformation_presentation/classical_inputs.json', input_ids=fp_ids,
         premise='Only the explicitly recorded basic commutative algebra is retained. Finite-level representability, formal torus extraction and the framed obstruction/relation construction are proved in FP.')
    node('FRAMED_WEIGHTED_PRESENTATION', 'Literal universal framed weighted presentation LemmaP',
         gate='AND', requires=['CLASSICAL_FRAMED_ALGEBRA'],
         status='human_general_algebraic_theorem_complete_in_exact_stated_hypotheses', claims=component_claims['framed_deformation_presentation'],
         endpoint='FP8: literal LemmaP', registry='framed_deformation_presentation/classical_inputs.json', input_ids=fp_ids,
         theorem_antecedents=['PhiCond', 'Residual and integral normalization', 'Residual representation trivial on each prescribed F.N q', 'Five IsLocCond axioms at each q', 'Required local base points', 'Finite actual framed Ob_j', 'Specified graded base B and local framed representations'],
         exact_hypothesis_registry='framed_deformation_presentation/closure.json#theorem_hypotheses_retained',
         not_inferred=['Unrestricted infinite-residue loc_graded/loc_graded_top helper statements', 'Existence of an arithmetic Model or installation of any original theorem hypothesis'],
         premise='The universal theorem is proved without an additional FramedUniv/ObsClass leaf. Its hypotheses and its application on actual Galois Raw data are not supplied by this theorem.')
    node('MODEL_SELMER_COTANGENT', 'shaCoc and mPrime for every actual graded Model', gate='AND',
         requires=['RANK_ONE_FINITE_SELMER', 'LEMMA_M_PRIME'], status='human_universal_implication_complete', claims=['SP7'],
         premise='Actual Good D, Model D and the source GradedAlgebra structure on its first-weight-zero algebra with pieces Model.gr are universally quantified antecedents. The conclusion supplies neither a Model nor that grading structure.')
    node('CLASSICAL_PAIRED_COUNT_ARITHMETIC', 'Matched prime choice and local Frobenius facts',
         status='named_classical_inputs_with_written_exact_normalizations', registry='symplectic_count_closure/classical_inputs.json', input_ids=['SP-C4', 'SP-C5'])
    node('SYMPLECTIC_TRACE_ARITHMETIC', 'Catalogue-to-integer and trace-valuation packaging',
         status='human_conditional_implication_complete', claims=['SP9'],
         theorem_antecedents=['The exact uniform finite catalogue SP-R3'],
         premise='Integer chosen before ell/closure/embedding/family; conjugation, integrality, nonvanishing and omitted-factor inequality are proved. The catalogue existence is not proved.')
    node('SYMPLECTIC_SOURCE_COHOMOLOGY', 'Actual symplectic cohomology and period-ring package',
         status='major_actual_interface_matching_retained', source_target_ids=['DA26-SP-04'],
         related_nodes=['LOCAL_K_INTERFACE_MATCH', 'FINITE_DUALITY_SPECIALIZATION'],
         premise='Entire CohomologyHyp, including arbitrary period-ring/local-published records and global finiteness/Euler/orthogonality/Greenberg-Wiles fields. LK and LD are available tools; no implication to this full record is asserted.')
    node('SYMPLECTIC_IMAGE_DENSITY', 'Actual finite-point, non-endoscopic and automorphic supply',
         status='major_automorphic_supplier_retained', source_target_ids=['DA25-HV-04'],
         premise='SymplecticFourImageDense: D.Fin0, D.NoEnd and one common embedding making all relevant original irreducible points automorphic, on precisely the specified Raw family.')
    node('SYMPLECTIC_RIGIDITY', 'Actual symplectic adjoint rigidity at original points',
         status='major_arithmetic_rigidity_supplier_retained', source_target_ids=['DA26-SP-06'],
         premise='Literal RigiditySymplecticFour, unramified deformation and adjoint-lifting inputs with original local/global conditions.')
    node('SYMPLECTIC_DATA_REALIZATION', 'G1 actual Raw, level and admissible-class construction',
         status='actual_constructor_and_comparison_chain_retained', source_target_ids=['DA26-SP-01'],
         retained_input_registry='symplectic_count_closure/remaining_inputs.json#SP-R1',
         related_nodes=['COR_X_RESIDUAL_SUPPLIER', 'EXACT_COEFFICIENT_RETURN', 'SYMPLECTIC_IMAGE_DENSITY'],
         premise='Complete G1 assertion as stated in SP10. Available CorX and coefficient lemmas are not a proof of dataEx/levOf/level/safe4-prime or their same-object join.')
    node('SYMPLECTIC_MODEL_COMPARISON', 'G2 actual weighted Model and point/trace/orbit comparison',
         status='actual_model_existence_and_internal_comparison_edges_retained', source_target_ids=['DA26-SP-02', 'DA26-SP-03'],
         retained_input_registry='symplectic_count_closure/remaining_inputs.json#SP-R2',
         related_nodes=['FRAMED_WEIGHTED_PRESENTATION', 'RANK_ONE_FINITE_SELMER', 'ALGEBRAIC_COEFFICIENT_VANISHING', 'SYMPLECTIC_SOURCE_COHOMOLOGY', 'SYMPLECTIC_IMAGE_DENSITY', 'SYMPLECTIC_RIGIDITY'],
         premise='Complete G2 for the same D as G1: actual Model equipped with the source GradedAlgebra Model.gr, M1-M4, two-sided-point irreducibility, exact trace element and conjugacy-to-orbit. Source packages and available universal theorems do not automatically prove these internal edges.')
    node('SYMPLECTIC_FINITE_CATALOGUE', 'Exact uniform finite automorphic trace catalogue',
         status='major_automorphic_classification_and_counting_supplier_retained', source_target_ids=['DA26-SP-05'],
         retained_input_registry='symplectic_count_closure/remaining_inputs.json#SP-R3',
         premise='Exact SP-R3 catalogue, chosen before ell/Omega/iota/family; original AdmRAlt, level and weights, integrality, conjugation, purity, classification and arithmetic Frobenius match. A generic automorphy theorem is insufficient.')
    node('SYMPLECTIC_PAIRED_ASSEMBLY', 'Complete G1/G2/catalogue-to-paired-count arithmetic join', gate='AND',
         requires=['LEMMA_M', 'MODEL_SELMER_COTANGENT', 'EXACT_COEFFICIENT_RETURN', 'SYMPLECTIC_TRACE_ARITHMETIC', 'CLASSICAL_PAIRED_COUNT_ARITHMETIC'],
         status='human_conditional_chain_complete', claims=['SP8', 'SP9', 'SP10'],
         theorem_antecedents=['G1 / SP-R1', 'G2 / SP-R2 on the same Raw object', 'Uniform catalogue / SP-R3'],
         premise='Exact factor two, original Selmer inclusion, one exponent before hosts/coefficients/characters, and normalized return are written. This theorem does not supply its three actual inputs.')
    node('CLASSICAL_HOST_COMPARISON', 'Matched elementary cyclotomic and conductor-discriminant facts',
         status='named_classical_inputs_with_written_original_host_comparison', registry='point_hv_assembly/classical_inputs.json', input_ids=['HV-CYC', 'HV-CD'])
    node('HOST_EIGENCHARACTER_COMPARISON', 'Original-field integral character comparison at every odd prime', gate='AND',
         requires=['CLASSICAL_HOST_COMPARISON'], status='human_original_field_comparison_complete', claims=['HV1', 'HV2', 'HV3', 'HV4'],
         premise='Exact original host E and source GS; psi-inverse quotient actions. Error <=(Ne)^6 at exceptional primes and exactly zero outside them. This replaces the combined reduction/error route without claiming the source lossAll formula.')
    node('COMPACT_FINITE_COHOMOLOGY_TRANSPORT', 'Previously proved compact/finite cochain and original-place transport', gate='AND',
         requires=['CLASSICAL_K_THEORY', 'FINITE_DUALITY_SPECIALIZATION', 'LOCAL_K_INTERFACE_MATCH'],
         status='human_actual_transport_complete_in_recorded_scope', claims=['KB1', 'KB6'],
         premise='Only the actual compact/finite cochain, inverse-limit and valuation/henselization/completion transport portions of KB1/KB6 are used. This node does not infer them merely from the existential KBridge predicate.')
    node('ROOT_CONTAINING_SELMER_COMPARISON', 'Previously proved root-containing strict-Selmer to H2 comparison', gate='AND',
         requires=['COMPACT_FINITE_COHOMOLOGY_TRANSPORT', 'LOCAL_K_INTERFACE_MATCH', 'FINITE_DUALITY_SPECIALIZATION'],
         status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['TW3'],
         premise='The exact strict-negative Selmer/tower comparison on each original totally complex field containing the prescribed roots, with every original local datum. This is the TW3 theorem used by HV5, not an inference from the ThmBab predicate alone.')
    node('SMALL_TWO_CONDUCTOR_COUNT', 'Literal CountVs small two-conductor supplier', gate='AND',
         requires=['LEMMA_K_BOUND', 'ROOT_CONTAINING_SELMER_COMPARISON', 'CLASSICAL_HOST_COMPARISON'],
         status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['HV5'],
         premise='Uses TW3 strict-Selmer comparison and LemmaK31. Full CountShape quantifiers, one exponent depending only on the fixed primitive character. Not the large-conductor CountV.')
    node('REFERENCE_LAYER_COUNT_IV', 'Literal CountIV strict-Selmer reference-layer comparison', gate='AND',
         requires=['CLASSICAL_HOST_COMPARISON'], status='human_supplier_complete_relative_to_matched_classical_leaves', claims=['HV6'],
         premise='All original model/closure/coefficient choices and the stated layer-degree quantifier; LayerLe/VVat are unweighted strict-Selmer bounds, not H2 bounds; no extra parity premise.')

    update('COUNT_I_SUPPLIER',
           status='major_actual_Kato_unitary_and_counting_supplier_retained_general_algebra_supplied',
           supplied_general_inputs={'LemmaMprime': 'SP1', 'LemmaM': 'SP6', 'LemmaP': 'FP8'},
           related_nodes=['LEMMA_M_PRIME', 'LEMMA_M', 'FRAMED_WEIGHTED_PRESENTATION'],
           premise='Actual OneChar -> PropGK -> CorGK -> CountI remains. General M/Mprime/P are supplied; actual CohInp/InpZ, Kato/adjoint rigidity, unramified-coefficient automorphy, rank-three trace counting and same-model applications remain.')
    update('SYMPLECTIC_COUNT_CHAIN', gate='AND',
           requires=['SYMPLECTIC_DATA_REALIZATION', 'SYMPLECTIC_MODEL_COMPARISON', 'SYMPLECTIC_FINITE_CATALOGUE', 'SYMPLECTIC_PAIRED_ASSEMBLY'],
           status='conditional_paired_count_chain_complete_exact_actual_G1_G2_catalogue_retained',
           source_target_ids=['DA24-HV-02', 'DA24-HV-03', 'DA25-HV-03', 'DA25-HV-04'] + [f'DA26-SP-0{i}' for i in range(1,7)],
           supplied_inputs={'CorX': 'BR7', 'SoFin': 'RV3', 'SoV': 'RV7', 'Coefficient return': 'RV1/SP8', 'LemmaMprime': 'SP1', 'LemmaM': 'SP6', 'LemmaP': 'FP8', 'shaCoc/mPrime on an actual Model with source GradedAlgebra': 'SP7'},
           premise='The node still means actual CountII and CountIII. SP10 closes the full arithmetic and coefficient-return join only from its exact G1/G2/catalogue. No unreviewed implication from generic source packages to G1/G2 is inserted.')
    update('COUNT_V_SUPPLIER',
           status='major_actual_host_frame_automorphy_and_counting_supplier_retained_M_leaves_supplied',
           supplied_general_inputs={'LemmaMprime': 'SP1', 'LemmaM': 'SP6'},
           related_nodes=['LEMMA_M_PRIME', 'LEMMA_M'],
           premise='ThmS6_s and HostVanE/Xpp/Rigid_s/Number_s on the same actual host frame, universal ring and marked point remain. Native non-K and normalized local/global packages require exact matching; CountVs does not supply CountV.')
    update('ACTUAL_POINT_COUNTS', status='CountZ_supplied_four_actual_count_predicates_retained_assembly_now_complete',
           supplied_inputs={'CountZ': 'CZ6'},
           premise='Actual CountI/II/III/V/Z have unchanged meanings. CountZ is complete; the other four remain actual arithmetic suppliers. The case/layer/sum assembly consuming them is now proved separately by HV.')
    update('POINT_HV_ASSEMBLY', gate='AND',
           requires=['HOST_EIGENCHARACTER_COMPARISON', 'SMALL_TWO_CONDUCTOR_COUNT', 'REFERENCE_LAYER_COUNT_IV', 'COUNT_Z_SUPPLIER'],
           status='human_original_field_case_layer_and_sum_assembly_complete', source_target_ids=[],
           claims=[f'HV{i}' for i in range(1,11)],
           theorem_antecedents=['CountI', 'CountII', 'CountIII', 'CountV'],
           premise='Complete literal four-count-to-PointHV implication. Whole reference-layer function j precedes one common constant and two prime thresholds; each bound is already uniform in all original hosts, models, local data, coefficients and twist cutoffs.',
           guard_note='The four count predicates are antecedents of this proved implication. Their actual truth is required separately at ACTUAL_POINT_COUNTS to obtain PointHV.')
    update('ODD_PLUS_BOUND', status='PointHV_assembly_complete_only_four_actual_count_suppliers_remain',
           supplied_inputs={'PoitouTateDuality': 'LD3', 'LocalFinitenessK': 'LK2', 'LocalTateDualityK': 'LK3', 'LemmaK': 'KB8', 'CountZ': 'CZ6', 'CountVs': 'HV5', 'CountIV': 'HV6', 'Full count/layer/sum assembly': 'HV10'},
           remaining_actual_inputs=['CountI', 'CountII', 'CountIII', 'CountV'],
           premise='The node still means literal PointHV on original field/local data and arbitrary fixed layer-index function. HV10 supplies its complete four-count implication, not the four actual count suppliers.')
    update('COHOMOLOGICAL_WINDOW', status='complete_human_conditional_route_from_four_actual_counts',
           completed_input_suppliers={'ODD_MINUS_BOUND': 'OB8 via OS1/OS9, constant240', 'TWO_PRIMARY_BOUND': 'TW8 via KB8/LK/LD, one K for all Ct>=1', 'ODD_PLUS_BOUND assembly': 'HV10 after actual CountI/II/III/V'},
           remaining_bespoke_suppliers=['ODD_PLUS_BOUND'], remaining_actual_count_inputs=['CountI', 'CountII', 'CountIII', 'CountV'],
           premise='ThmBab and ThmBcFree are supplied and PointHV assembly is written. All three summands use original E; separately quantified reference-layer models share the fixed pair and window. Actual four counts remain.')
    update('JOINT_WINDOW', status='conditional_ThmBab_and_four_count_route_fully_assembled',
           note='Optional direct JointWin remains unreconstructed. On the ThmBab/PointHV route, TW8 supplies ThmBab and HV10 supplies all PointHV assembly from the four actual counts.')
    update('FIXED_PAIR_WINDOWS', status='human_chain_complete_conditional_on_four_actual_counts_and_named_classical_inputs',
           supplied_cohomological_parts=['TW8', 'OB8', 'HV5', 'HV6', 'HV10'],
           remaining_cohomological_supplier='Actual CountI, CountII, CountIII and CountV through literal PointHV',
           premise='One q,d for every real x in each late interval; original field/degree/conductor/local-data and separate layer-model ties retained. QP keeps the 401-to-400 margin. Compatible-host and global arithmetic-family/gap requirements are not inferred.')

    # Each old ID and its meaning survives. A changed old node has the exact old record.
    for old in baseline['nodes']:
        assert old['id'] in byid
        current = byid[old['id']]
        if old['id'] in changed:
            assert current['history'][-1] == {'version': '0.25', 'snapshot': old}, old['id']
        else:
            assert current == old, old['id']
    seen, active = set(), set()

    def visit(nid):
        assert nid in byid, nid
        if nid in seen:
            return
        assert nid not in active, ('cycle', nid)
        active.add(nid)
        n = byid[nid]
        assert n['gate'] in {'AND', 'OR', 'LEAF'}, nid
        for dep in n.get('requires', []) + [x for group in n.get('alternatives', []) for x in group]:
            visit(dep)
        active.remove(nid)
        seen.add(nid)

    for nid in byid:
        visit(nid)
    tids = {t['id'] for t in targets}
    assert len(tids) == len(targets)
    available_claims = all_new_claims | {cid for n in baseline['nodes'] for cid in n.get('claims', [])}
    for n in m['nodes']:
        for dep in n.get('related_nodes', []):
            assert dep in byid, dep
        for tid in n.get('source_target_ids', []):
            assert tid in tids, (n['id'], tid)
        for cid in n.get('claims', []):
            assert cid in available_claims, (n['id'], cid)
    m['validation'] = {**m.get('validation', {}), 'node_count': len(m['nodes']),
        'node_ids_unique': True, 'acyclic': True, 'all_edges_resolve': True,
        'all_related_nodes_resolve': True, 'all_current_target_ids_resolve': True,
        'all_current_claim_ids_resolve': True,
        'historical_node_meanings_preserved': True, 'historical_node_count': len(baseline['nodes']),
        'changed_historical_nodes': changed, 'complete_previous_records_preserved': True,
        'historical_validation_preserved_in_previous_map': True,
        'unproved_generic_model_implication_inserted': False}
    anchors = sorted(source_index.values(), key=lambda a: (a['path'], a['line_start'], a['line_end']))
    source_obj = {'commit': PIN, 'sources': anchors, 'source_files': len(blobs), 'source_ranges': len(anchors)}
    source_bytes = (json.dumps(source_obj, ensure_ascii=False, indent=2) + '\n').encode()
    m['source_manifest_sha256'] = sha(source_bytes)
    (HERE / 'previous_obligation_map.json').write_bytes((OLD / 'obligation_map.json').read_bytes())
    write('obligation_map.json', m)
    write('source_anchors.json', source_obj)
    write('next_targets.json', {'targets': targets})
    write('retirement_candidates.json', {'targets': retired})
    write('target_scope_updates.json', updates)
    write('global_branch_scope_updates.json', {'updates': global_scope_updates})
    write('symplectic_frontier_sources.json', {'source_frontier': frontier,
        'entry_target_ids': [f'DA26-SP-0{i}' for i in range(1,7)],
        'related_nodes_are_not_proof_edges': True})
    write('input_manifest.json', {'artifact_version': '0.26', 'components': COMPONENTS,
        'review_input_policy': 'Only mathematical component reviews/source validations, integration-scope review and explicitly listed stable review writers. Downstream semantic/final-scope/coverage/package/audit outputs are excluded to prevent circular hash dependencies.',
        'files': [input_index[k] for k in sorted(input_index)]})
    write('summary.json', {'artifact_version': '0.26', 'new_claim_ids': [],
        'increment_supplier_claims': component_claims,
        'retirement_candidate_ids': list(retirement), 'retirement_count': len(retired),
        'historical_nodes_preserved': len(baseline['nodes']), 'map_node_count': len(m['nodes']),
        'changed_historical_node_ids': changed,
        'remaining_cohomological_supplier': 'PointHV, with only actual CountI/II/III/V remaining on the selected route',
        'supplied_counts': {'CountZ': 'CZ6', 'CountVs': 'HV5', 'CountIV': 'HV6'},
        'remaining_counts': ['CountI', 'CountII', 'CountIII', 'CountV'],
        'remaining_count_assembly': False,
        'paired_count_remaining_cut': ['G1 / SP-R1', 'G2 / SP-R2', 'Uniform catalogue / SP-R3'],
        'not_globally_closed': ['RH', 'Dirichlet GRH', 'PointHV', 'Actual CountI/II/III/V',
          'Actual CohomologyHyp/native non-K and normalized packages', 'Actual symplectic model/data/trace catalogue',
          'Actual-family LinkN', 'Actual common family / DesignExists', 'HostExW and actual HostGood/RankVal/EAtH',
          'Theta/type/rank/metric/spectral joins', 'Arithmetic gap / final gain']})
    write('verification.json', {'artifact_version': '0.26', 'source_commit': PIN,
        'source_files_checked': len(blobs), 'source_ranges_indexed': len(anchors),
        'all_cited_source_files_equal_pinned_git_blobs': True, 'all_source_range_hashes_verified': True,
        'new_component_proof_ranges_verified': len(proof_checks),
        'all_component_main_and_proof_hashes_match': True,
        'available_component_manifest_entries_verified': component_manifest_checks,
        'previous_release_input_manifest_verified': True,
        'historical_node_ids_preserved': True, 'complete_changed_node_snapshots_verified': True,
        'historical_snapshot_byte_identical': True, 'sufficient_condition_graph_acyclic': True,
        'current_validation_node_count': len(m['nodes']), 'historical_validation_not_edited': True,
        'all_related_and_target_ids_resolve': True, 'prior_files_modified': False,
        'root_targets_modified': False, 'new_claim_ids': [], 'Lean_kernel_replay_run': False,
        'formal_transitive_Lean_dependency_audit': False, 'audit_txt_sha256': sha((HERE / 'audit.txt').read_bytes()),
        'scope': 'Human semantic sufficient-condition audit. Integrity and graph checks validate provenance/bookkeeping, not mathematical proofs.'})
    print(json.dumps({'retirements': len(retired), 'targets': len(targets),
        'source_files': len(blobs), 'source_ranges': len(anchors),
        'proof_ranges': len(proof_checks), 'historical_nodes': len(baseline['nodes']),
        'map_nodes': len(m['nodes'])}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=WORK.parent / 'lean-source')
    main(parser.parse_args().repo.resolve())
