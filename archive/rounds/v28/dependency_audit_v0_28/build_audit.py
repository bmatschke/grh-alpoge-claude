#!/usr/bin/env python3
"""Build v0.28's finite semantic sufficient-condition map and exact source audit."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OLD = WORK / 'dependency_audit_v0_27'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
S = P + 'SymplecticGSp4/'
D = P + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
COMPONENTS = ['bloch_kato_installation', 'symplectic_actual_rigidity',
              'symplectic_automorphic_catalogue', 'symplectic_image_density',
              'paired_count_installation']
REVIEW_PREFIXES = ('bloch_kato_', 'actual_rigidity_', 'symplectic_rigidity_',
                  'symplectic_actual_rigidity_', 'symplectic_automorphic_catalogue_',
                  'rigidity_', 'automorphic_catalogue_', 'symplectic_catalogue_',
                  'catalogue_', 'image_density_', 'symplectic_image_',
                  'paired_count_', 'integration_scope_review')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def walk_anchors(value):
    if isinstance(value, dict):
        if {'path', 'line_start', 'line_end', 'sha256', 'range_sha256', 'url'} <= value.keys():
            yield value
        for child in value.values():
            yield from walk_anchors(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_anchors(child)


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
            assert b == subprocess.check_output(['git', '-C', str(repo), 'show', PIN + ':' + path]), path
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
            pat = re.compile(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure)\s+' + re.escape(decl) + r'(?=[\s:(])')
            hits = [i+1 for i,t in enumerate(lines) if pat.match(t)]
            assert len(hits) == 1, (path, decl, hits)
            start = hits[0]
        if end is None:
            end = len(lines)
            for i in range(start, len(lines)):
                if re.match(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[', lines[i]):
                    end = i
                    break
            while end > start and not lines[end-1].strip():
                end -= 1
        fragment = b''.join(b.splitlines(keepends=True)[start-1:end])
        return verify({'path': path, 'declaration': decl, 'line_start': start, 'line_end': end,
            'sha256': sha(b), 'range_sha256': sha(fragment), 'range_bytes': len(fragment),
            'first_line': lines[start-1], 'url': REPO + '/blob/' + PIN + '/' + path + f'#L{start}-L{end}',
            'verified_equal_to_pinned_git_blob': True})

    baseline = read(OLD / 'obligation_map.json')
    assert len(baseline['nodes']) == 111
    old_targets = read(OLD / 'next_targets.json')['targets']
    for a in walk_anchors(old_targets):
        verify(a)
    for a in read(OLD / 'source_anchors.json')['sources']:
        verify(a)
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
        expected = ledger.get('main_tex_sha256', ledger.get('validation', {}).get('main_tex_sha256'))
        assert sha((directory / 'main.tex').read_bytes()) == expected, name
        component_claims[name] = [c['id'] for c in ledger['claims']]
        for claim in ledger['claims']:
            loc = claim.get('proof_location', claim.get('human_proof'))
            assert loc is not None, claim['id']
            b = (WORK / loc['file']).read_bytes()
            fragment = b''.join(b.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
            assert sha(fragment) == loc['sha256'], claim['id']
            proof_checks.append(claim['id'])
        manifest = directory / 'input_manifest.json'
        if manifest.exists():
            for a in read(manifest).get('files', []):
                p = WORK / a['path']
                assert sha(p.read_bytes()) == a['sha256'], a['path']
                component_manifest_checks += 1
                file_input(p)
        for p in sorted(directory.iterdir()):
            if p.is_file() and (p.suffix in {'.json', '.tex', '.py'} or p.name in {'report.txt', 'report.md', 'source_locators.txt', 'README.md'}):
                file_input(p)
                if p.suffix == '.json':
                    for a in walk_anchors(read(p)):
                        verify(a)

    all_new_claims = {c for group in component_claims.values() for c in group}
    assert len(all_new_claims) == sum(map(len, component_claims.values())) == 36
    for p in sorted((WORK / 'reviews_v0_28').glob('*')):
        downstream = any(s in p.name for s in ('audit', 'coverage', 'package', 'final_scope', 'semantic_scope'))
        mathematical = p.suffix in {'.json', '.txt', '.md'} and p.name.startswith(REVIEW_PREFIXES)
        if p.is_file() and not downstream and mathematical:
            file_input(p)
    for name in ['configure_v0_28.py', 'increment_v0_28.json']:
        p = WORK / name
        if p.exists():
            file_input(p)

    paired_cut = ['Literal SymplecticFourImageDense on the original Good/OfCase data, including one common embedding before all point quantifiers']
    height_cut = ['Actual CountI', 'Actual CountV'] + paired_cut
    retirement = {
        'DA26-SP-04': (['BX7', 'BX8'],
            'Entire original BlochKatoLocal, LocalPublishedTheorems and CohomologyHyp, with every prime and exact original period/cochain/lattice interfaces. All original oddness antecedents of global statements are retained.'),
        'DA26-SP-06': (['RX1', 'RX2', 'RX3', 'RX4', 'RX5', 'RX6'],
            'Literal RigiditySymplecticFour is proved directly. Therefore the source rigSp4_alt implication is proved even without its larger producer antecedents. This does not construct UnramifiedInputs, HypothesesH-prime or AdjointLiftingTheorem, and same-D automorphy is still needed for application.')}
    updates = {
        'DA26-SP-01': {
            'human_status':'actual_G1_complete_conditional_only_on_ImageDense',
            'supplied_by':['AX10','BX8','RX7','CX9','JX1'],
            'remaining_human_scope':'The literal ImageDense predicate remains. AX supplies every actual data/Good/OfCase/level/safe constructor; JX1 now completes the entire paired-count implication from ImageDense. No separate cohomology, actual rigidity or catalogue premise remains in that implication.',
            'retained_inputs':paired_cut},
        'DA26-SP-03': {
            'human_status':'actual_G2_complete_conditional_only_on_ImageDense',
            'supplied_by':['MX10','PX10','RX7','CX9','JX1'],
            'remaining_human_scope':'ImageDense supplies Fin0 and NoEnd and the single automorphic embedding; RX7 installs AllIrr RigidAt on that same D, and CX9 supplies the original trace guard. The actual Model/grading/M1-M4/point/trace/orbit chain is complete. ImageDense itself remains.',
            'retained_inputs':paired_cut},
        'DA26-SP-05': {
            'human_status':'actual_uniform_rank_four_catalogue_and_NumberSp4Alt_supplied_broader_source_scope_unpromoted',
            'supplied_by':['CX8','CX9'],
            'supplied_scope':'Every clause of the exact SP9 finite catalogue and the literal NumberSp4Alt endpoint, uniformly before auxiliary coefficients, places, embeddings and families.',
            'remaining_human_scope':'The exact actual catalogue goal is closed. Preserve this compound source record only for the broader all-rank CountQAlt and unchanged-level LevelPNAlt source packages. Those stronger scopes are not promoted and are not premises of the completed actual paired-count route.',
            'retained_inputs':['All-rank CountQAlt and unchanged-level LevelPNAlt if those stronger source declarations are themselves reconstructed.'],
            'remaining_scope_blocks_selected_paired_route':False,
            'level_precision':'Original Galois level M; auxiliary automorphic label level M^7 absorbed in A_*=224 and A=225.'},
        'DA27-SP-01': {
            'human_status':'same_D_actual_rigidity_installed_from_ImageDense',
            'supplied_by':['RX3','RX6','RX7'],
            'remaining_human_scope':'The universal RigiditySymplecticFour theorem and its exact same-D installation are written. The only remaining premise in the selected actual application is ImageDense supplying IsAut4Alt under its one common embedding. No independent actual-rigidity supplier remains after that premise.',
            'retained_inputs':paired_cut,
            'not_inferred':'The direct theorem does not reconstruct the broader original adjoint-lifting producer packages.'},
        'DA25-HV-04': {
            'human_status':'ImageDense_retained_actual_internal_and_promodular_transports_complete',
            'supplied_by':['AX10','BX8']+[f'IX{i}' for i in range(1,11)],
            'remaining_human_scope':'Construct actual ImageDense on every original Good/OfCase datum. IX closes all internal actual-point, nonsplit-block and strict weak-purity steps and the exact consequences of actual ProModAlt witnesses. The uniform witness realization, actual finite modular quotient/link/support, PMExAlt and exact SeedIIAlt/SeedIVAlt/component-reaching producers remain.',
            'retained_inputs':['One fixed iota before every actual ambient and star-point quantifier','Actual PMExAlt with all five clauses','Exact SeedIIAlt and SeedIVAlt','Original tower/Space/support and both case component-reaching chains']},
        'DA27-SP-02': {
            'human_status':'ImageDense_source_producer_narrowed_full_cohomology_and_internal_transports_supplied',
            'supplied_by':['BX8']+[f'IX{i}' for i in range(1,11)],
            'remaining_human_scope':'The source sp4In_alt cohomology premise is now supplied, and its finite arithmetic Ferrero-Washington leaf is already matched. The remaining seed/PMExAlt and actual case-two/case-three tower, space and support realization must be reconstructed on the same objects. IX10 supplies the complete final implication once uniform ProModAlt realization has been constructed.',
            'retained_inputs':['SeedIIAlt','SeedIVAlt','PMExAlt','Actual finite modular quotient and compatible Link/IsPhi/support','Actual uniform star-point ProModAlt realization'],
            'bypassed_not_promoted':['Whole HypothesesH-prime','UnramifiedInputs','AdjointLiftingTheorem']},
        'DA25-HV-03': {
            'human_status':'complete_paired_count_implication_with_single_ImageDense_premise',
            'supplied_by':['JX1','BX8','RX7','CX9','AX10','MX10','PX10','SP10'],
            'remaining_human_scope':'Supply literal SymplecticFourImageDense. JX1 proves the exact CountII and CountIII conclusions from that one premise, including actual original hosts, uniform exponents, the common embedding, factor two and normalized coefficient return.',
            'retained_inputs':paired_cut},
        'DA-next-01-b': {
            'human_status':'complete_reduced_height_window_implication_CountI_CountV_ImageDense_retained',
            'supplied_by':['JX1','JX2','HV10','TW8','OB8','VW3','VW4'],
            'remaining_human_scope':'Actual CountI, actual CountV and literal ImageDense on their original objects. JX1 supplies II/III from ImageDense and JX2 propagates all three premises to literal PointHV and the established guarded cohomological window. No unconditional count, PointHV or final H-window is asserted.',
            'retained_inputs':height_cut},
        'DA24-HV-01': {
            'human_status':'actual_CountI_retained_full_cohomology_supplied_only_where_identical',
            'supplied_by':['BX8'],
            'remaining_human_scope':'Literal CountI on its original hosts, coefficients, characters and twists, with constants before varying host data. Full CohomologyHyp is now supplied where the entry theorem asks for that exact record. Its actual Kato/unitary, rank-two/rank-three automorphy, adjoint, congruence-number and model-comparison chain remains; rank-four CX/RX is not silently substituted.',
            'retained_inputs':['Actual original CountI arithmetic data and automorphy/vanishing/count suppliers']},
        'DA24-HV-06': {
            'human_status':'actual_CountI_constructor_chain_retained_full_cohomology_record_supplied',
            'supplied_by':['BX8'],
            'remaining_human_scope':'Construct the actual CohInp/InpZ arithmetic instance, RigII from KatoTwo, adjoint vanishing, rank-three congruence-number control and AutomorphyUnramifiedCoefficients; reconstruct OneChar -> PropGK -> CorGK -> CountI. The exact full CohomologyHyp record is available, but does not construct these objects.',
            'retained_inputs':['Actual InpZ/CohInp realization','KatoTwo and actual rank-two/rank-three rigidity and counting','AutomorphyUnramifiedCoefficients and actual model comparison']},
        'DA25-HV-08': {
            'human_status':'actual_CountV_host_chain_retained_complete_cohomology_inputs_available',
            'supplied_by':['DX1','BX8','SP1','SP6'],
            'remaining_human_scope':'Full actual large-conductor CountV on its original host/frame, marked point and universal ring: ThmS6_s, HostVanE, HostXpp, HostRigid_s and HostNumber_s with their arithmetic model/automorphic comparisons. DX/BX supplies exact cohomology fields where identically quantified; rank-four RX/CX is not an automatic proof of the differently scoped host inputs. CountVs is not CountV.',
            'retained_inputs':['ThmS6_s','HostVanE','HostXpp','HostRigid_s','HostNumber_s','Actual same host/frame/model and normalized coefficient comparison']}}
    for tid,name in [('DA24-HV-02','CountII'),('DA24-HV-03','CountIII')]:
        updates[tid]={'human_status':'literal_count_supplied_from_ImageDense_only',
            'supplied_by':['JX1'],
            'remaining_human_scope':'Supply ImageDense; the complete literal '+name+' conclusion follows by JX1 with the original uniform CountShape quantifiers. The implication is complete, its arithmetic antecedent remains.',
            'retained_inputs':paired_cut}
    updates['DA24-HV-04']=copy.deepcopy(updates['DA25-HV-08'])

    targets,retired=[],[]
    for old in old_targets:
        q=copy.deepcopy(old)
        if q['id'] in retirement or q['id'] in updates:
            q.setdefault('history',[]).append({'version':'0.27','snapshot':copy.deepcopy(old)})
        if q['id'] in retirement:
            suppliers,scope=retirement[q['id']]
            q.update(status='safe_to_retire_in_stated_scope',
                     human_status='literal_target_scope_supplied_by_complete_human_proof',
                     supplied_by=suppliers,closed_scope=scope,
                     remaining_human_scope='No remaining supplier inside this exact retired scope. '+scope,
                     retained_inputs=[])
            if q['id']=='DA26-SP-06':
                q['retained_theorem_hypotheses']=['Literal IsAut4Alt and every original point/local-condition antecedent of RigiditySymplecticFour']
                q['bypassed_not_promoted']=['Whole UnramifiedInputs','HypothesesH-prime','AdjointLiftingTheorem']
            retired.append(q)
        else:
            q.update(updates.get(q['id'],{}))
            targets.append(q)

    ix_frontier=ledgers['symplectic_image_density']['retained_frontier']
    ix_by_id={x['id']:x for x in ix_frontier}
    def ix_sources(*ids):
        return [copy.deepcopy(a) for fid in ids for a in ix_by_id[fid]['sources']]
    def ix_anchor(fid,decl):
        hits=[a for a in ix_by_id[fid]['sources'] if a['declaration']==decl]
        assert len(hits)==1,(fid,decl)
        return copy.deepcopy(hits[0])
    def next_target(tid,primary,package,scope,inputs,sources):
        q=copy.deepcopy(primary)
        q.update(id=tid,work_package=package,priority_group=1,status='human_proof_retained',
                 human_status='exact_actual_arithmetic_producer_after_complete_IX_transport',
                 remaining_human_scope=scope,retained_inputs=inputs,supporting_sources=sources,
                 downstream='IX10 -> literal ImageDense -> JX1 CountII/III -> JX2 reduced PointHV/window branch')
        targets.append(q)
    next_target('DA28-SP-01',ix_anchor('IX-F1','PMExAlt'),'actual_finite_modular_quotient_and_PMEx',
        'Construct the actual potential-modularity theorem with all five PMExAlt clauses, one permitted coefficient threshold, the original tower/Space, finite ordinary modular quotient, compatible Link/IsPhi equations and actual support. IX9 supplies the finite-fibre containment once those exact objects and finiteness are present; it does not construct them.',
        ['Actual modular R/J0 finite over its exact weight algebra','Original compatible Link/IsPhi and support ideal','All five PMExAlt clauses and their coefficient-threshold quantifiers','Any exact Hida/adjoint or unramified producer hypotheses used to construct this arithmetic package'],
        ix_sources('IX-F1','IX-F8','IX-F9','IX-F10','IX-F11','IX-F12','IX-F13','IX-F14','IX-F15','IX-F16','IX-F17'))
    next_target('DA28-SP-02',ix_anchor('IX-F2','SeedIIAlt'),'exact_case_two_and_case_four_automorphic_seeds',
        'Construct both literal SeedIIAlt and SeedIVAlt, with their original root-entry, residual twist/parity, coefficient, regular-algebraic cuspidal attachment and common-embedding requirements. Keep both seed conclusions and their different quantifier scopes; a generic nonempty automorphic family does not supply them.',
        ['Actual IsSeedAlt and SeedPairAlt on the given tower','Exact SeedIVAlt root-entry and residue conditions','Original attachment and WitA data','The arithmetic hypotheses of the selected seed producers'],
        ix_sources('IX-F2','IX-F3','IX-F18','IX-F19'))
    next_target('DA28-SP-03',ix_anchor('IX-F1','ProModAlt'),'uniform_actual_star_point_support_realization',
        'For every original Good/OfCase D construct one iota before all Amb/KPair/Star quantifiers, and then an actual full ProModAlt witness for every star pair. Complete both original case-two and case-three tower/Space/component-reaching chains, including every support, coefficient, restriction and conjugacy clause. IX10 proves all consequences once these witnesses exist.',
        ['Actual PMExAlt and exact seed witnesses where used','Actual Fit/Deep tower and compatible coefficients','Both case component/support-reaching constructions','One common iota before all varying points'],
        ix_sources('IX-F1','IX-F3','IX-F4','IX-F5','IX-F20','IX-F21','IX-F22','IX-F23'))
    for a in walk_anchors(targets):
        verify(a)

    unkeyed=anchor('src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean','VWinAt')
    global_scope_updates=[{
        'match':{'path':unkeyed['path'],'declaration':'UpperTheory.Top.VWinAt'},'source':unkeyed,
        'human_status':'Complete conditional cohomological window chain with CountI_CountV_ImageDense sufficient cut',
        'remaining_human_scope':'JX2 reduces the actual odd-plus supplier to CountI, CountV and ImageDense. TW8 and OB8 supply ThmBab and ThmBcFree240; HV/VW supplies every original-field assembly and fixed-pair rescaling, retaining the established prime-pair hypotheses. The independent compatible-host/global-family/gap requirements are not supplied.',
        'retained_inputs':height_cut+['The established VW/QP prime-pair and host hypotheses where stated'],
        'supplied_by':['JX1','JX2','TW8','OB8','HV10','VW3','VW4','QP22']}]

    m=copy.deepcopy(baseline)
    m.update(artifact_version='0.28',baseline='0.27',previous_map='previous_obligation_map.json',
        current_count_cut=height_cut,conditional_count_suppliers={'CountII':'JX1 from ImageDense','CountIII':'JX1 from ImageDense'},
        increment_integration='BX closes entire source local/global cohomology records; RX closes literal rigidity and its same-D application from ImageDense; CX closes exact SP9/NumberSp4Alt; IX closes actual-point and promodular transport implications with arithmetic realization retained; JX closes ImageDense -> CountII/III and CountI+CountV+ImageDense -> PointHV/window. The independent family/gap/theta/metric/spectral frontier remains.')
    byid={n['id']:n for n in m['nodes']}
    changed=[]
    def update(nid,remove=(),**kwargs):
        n=byid[nid]
        previous=copy.deepcopy(n)
        n.setdefault('history',[]).append({'version':'0.27','snapshot':previous})
        for key in remove:
            n.pop(key,None)
        n.update(kwargs)
        changed.append(nid)
    def node(nid,title,gate='LEAF',**kwargs):
        assert nid not in byid,nid
        n={'id':nid,'title':title,'gate':gate,'introduced_in':'0.28',**kwargs}
        m['nodes'].append(n);byid[nid]=n
    def registry_ids(component):
        values=read(WORK/component/'classical_inputs.json')['inputs']
        return list(values) if isinstance(values,dict) else [v['id'] for v in values]

    node('CLASSICAL_FULL_BLOCH_KATO','Exact classical local period and Bloch-Kato theorem leaves',
        status='named_classical_inputs_with_complete_source_model_transports',
        registry='bloch_kato_installation/classical_inputs.json',input_ids=registry_ids('bloch_kato_installation'))
    node('FULL_LOCAL_BLOCH_KATO','Entire original finite-coefficient BlochKatoLocal interface',gate='AND',
        requires=['CLASSICAL_FULL_BLOCH_KATO','NATIVE_FINITE_COHOMOLOGY','LOCAL_K_INTERFACE_MATCH'],
        status='literal_full_local_record_supplied',claims=[f'BX{i}' for i in range(1,8)],
        premise='Every prime, original tied period model, finite extension, arbitrary de Rham representation, nondegenerate pairing and lattice. Both rational cup orders and all integral annihilator directions include torsion, original lifts/coboundaries and scalar normalization. No automorphic existence is inferred.')
    node('CLASSICAL_POLARIZED_ADJOINT','Precisely matched polarized-adjoint Selmer vanishing theorem',
        status='named_primary_classical_theorem_with_actual_hypothesis_verification',
        registry='symplectic_actual_rigidity/classical_inputs.json',input_ids=registry_ids('symplectic_actual_rigidity'))
    node('ACTUAL_TANGENT_BLOCH_KATO','Actual ordinary dual-number tangent lies in the exact finite local conditions',gate='AND',
        requires=['FULL_LOCAL_BLOCH_KATO','ACTUAL_GOOD_FACTS','NATIVE_FINITE_COHOMOLOGY','CLASSICAL_POLARIZED_ADJOINT'],
        status='literal_tanBK_supplied_on_original_points',claims=['RX1','RX2','RX3'],
        theorem_antecedents=['Original Good D','Original EPt and actual PtIn dual-number lift'],
        premise='Finite coefficient capture, original ordered ordinary flag, fixed multiplier, local cyclotomic characters and original completion/decomposition maps are retained. Full Bloch-Kato matching supplies the local comparison, not a replacement local condition.')
    node('DIRECT_SYMPLECTIC_RIGIDITY','Direct original-point polarized adjoint proof of RigiditySymplecticFour',gate='AND',
        requires=['ACTUAL_TANGENT_BLOCH_KATO','ACTUAL_GOOD_FACTS','CLASSICAL_POLARIZED_ADJOINT'],
        status='human_universal_rigidity_implication_complete',claims=['RX4','RX5','RX6'],
        theorem_antecedents=['The literal original IsAut4Alt and point hypotheses of RigiditySymplecticFour'],
        premise='Cyclotomic irreducibility is proved from ordinary distinct weights; the chosen CM restriction preserves it. The Hecke infinity-sign correction by eta_K preserves the theta*cyclo^3 avatar equality on G_K; no corrected global equality is asserted. Thorne6.1 applies to the exact polarized adjoint, and the explicit sp4 projection gives the original symplectic commutator. Whole UnramifiedInputs/AdjointLiftingTheorem is bypassed, not supplied.')
    node('CLASSICAL_UNIFORM_CATALOGUE','Precisely matched cohomological, automorphic Galois and local conductor leaves',
        status='named_primary_classical_theorems_with_complete_rank_four_specialization',
        registry='symplectic_automorphic_catalogue/classical_inputs.json',input_ids=registry_ids('symplectic_automorphic_catalogue'))
    node('UNIFORM_FIXED_CM_CATALOGUES','Uniform full global labels at polynomially enlarged auxiliary level',gate='AND',
        requires=['CLASSICAL_UNIFORM_CATALOGUE','POLYNOMIAL_REPRESENTATION'],
        status='human_actual_rank_four_catalogue_construction_complete',claims=[f'CX{i}' for i in range(1,8)],
        premise='One fixed cell complex for each of eighteen fixed quadratic fields gives c_K L^32(e+2)^32. Actual SafeRA forces ell|M; exact polarization/compatibility gives label level M^7 while the original representation stays at M. Arithmetic eigenvalues are inverse geometric roots; crystalline slope signs, all valuations, Aut(C) and full-label classification are proved.')
    node('LITERAL_NUMBER_SP4','Literal NumberSp4Alt with fixed uniform constants',gate='AND',
        requires=['SYMPLECTIC_FINITE_CATALOGUE','SYMPLECTIC_TRACE_ARITHMETIC'],
        status='literal_universal_rank_four_counting_endpoint_complete',claims=['CX9','SP9'],
        theorem_antecedents=['Original AdmRAlt families and the source prime/root/order conditions'],
        constants={'A':225,'C':'c_* * 2^225','catalogue_exponent':224},
        premise='The integer and finite label family precede ell, Omega, iota, original places and varying representation families. Labels retain all root and two-extension bit multiplicities. No unconditional automorphy or all-rank unchanged-level source theorem is inferred.')
    node('CLASSICAL_IMAGE_POINT_ALGEBRA','Matched complete local algebra, flags, local fields and finite representation theory',
        status='named_classical_leaves_with_actual_point_constructions',
        registry='symplectic_image_density/classical_inputs.json',input_ids=registry_ids('symplectic_image_density'))
    node('ACTUAL_IMAGE_POINT_ENGINE','Actual universal points, valued flags, characteristic-ell curves and nonsplit blocks',gate='AND',
        requires=['ACTUAL_GOOD_FACTS','ACTUAL_PHI_COND','ACTUAL_LOCAL_BASES','FRAMED_WEIGHTED_PRESENTATION','COR_X_RESIDUAL_SUPPLIER','NATIVE_FINITE_COHOMOLOGY','FINITE_DUALITY_SPECIALIZATION','CLASSICAL_IMAGE_POINT_ALGEBRA'],
        status='human_complete_actual_point_and_purity_contradiction_chain',claims=[f'IX{i}' for i in range(1,8)],
        premise='The actual universal IsPt ring and full-weight-zero algebra are constructed before Fin0. Proper flags preserve original quotient labels; a failure of Fin0 produces a genuinely nonconstant characteristic-ell valued point. A primitive integral cocycle constructs a nonsplit KPair preserving every characteristic polynomial, and the exact strict PureW contradiction is proved. No automorphic support is presumed.')
    node('ACTUAL_IMAGE_CONDITION_JOIN','Con, PurityAtPoints and AutmAlt imply the actual ImageDense conclusions',gate='AND',
        requires=['ACTUAL_IMAGE_POINT_ENGINE'],status='human_complete_conditional_ImageDense_endpoint',claims=['IX8'],
        theorem_antecedents=['Con on original characteristic-ell KPairs','PurityAtPoints on all actual star KPairs','AutmAlt for the same iota chosen before all points'],
        premise='Same-D Fin0, NoEnd and AllIrr(IsAut4Alt iota) follow. The nonsplit KPair need not be an EPt, which is why the full purity quantifier is essential.')
    node('ACTUAL_CON_PURITY_AUTOMORPHY','Actual simultaneous Con, PurityAtPoints and AutmAlt on every original datum',
        status='major_actual_arithmetic_realization_retained',source_target_ids=['DA25-HV-04','DA27-SP-02'],
        retained_input_registry='symplectic_image_density/input_registry.json#IX-H-CON,IX-H-PURE,IX-H-AUT',
        premise='One fixed iota for each original Good/OfCase datum precedes all ambient fields, characteristic-zero/characteristic-ell points and KPair quantifiers. Separate pointwise automorphy or purity of an unrelated representation is insufficient.')
    node('ACTUAL_FINITE_MODULAR_QUOTIENT','Actual modular quotient, compatible Link and support realizing the PM package',
        status='major_arithmetic_module_and_support_construction_retained',source_target_ids=['DA28-SP-01'],
        premise='Actual ordinary determinant ring R, weight algebra Lambda, finite R/J0 over Lambda, exact Link.IsPhi equations and original support, with all five PMExAlt fields and coefficient thresholds. IX9 proves their consequences but does not construct these arithmetic objects.')
    node('EXACT_AUTOMORPHIC_SEEDS','Both exact SeedIIAlt and SeedIVAlt arithmetic seed suppliers',
        status='major_automorphic_seed_construction_retained',source_target_ids=['DA28-SP-02'],
        premise='Original root-entry, residual character, twist/parity, coefficient and regular-algebraic attachment conditions are retained separately for both seeds. Generic automorphic existence does not meet these quantifiers.')
    node('ACTUAL_PROMODULAR_REALIZATION','One common-embedding actual ProModAlt witness for every original star pair',
        status='major_actual_tower_space_support_realization_retained',source_target_ids=['DA28-SP-03'],
        related_nodes=['ACTUAL_FINITE_MODULAR_QUOTIENT','EXACT_AUTOMORPHIC_SEEDS','SYMPLECTIC_SOURCE_COHOMOLOGY'],
        premise='For every original Good/OfCase D, choose one iota before every Amb and star KPair; construct the complete Fit/Deep tower, coefficients, Space, J, y, r1, support, local base, conjugacy, multiplier, restriction and inertia-character witness. Source seed/PMEx/component-reaching connections are continuation relationships, not asserted completed proof edges.')
    node('PROMODULAR_TRANSPORT_JOIN','Full actual finite-fibre and ProModAlt transport to ImageDense',gate='AND',
        requires=['ACTUAL_IMAGE_CONDITION_JOIN','ACTUAL_GOOD_FACTS'],
        status='human_complete_conditional_promodular_transport',claims=['IX9','IX10'],
        theorem_antecedents=['Actual finite modular quotient and Link for the IX9 finite-fibre subtheorem','Uniform original star-point ProModAlt realization for the IX10 endpoint'],
        premise='IX9 proves the exact maximal-ideal-power containment from actual finite weight-module data, and characteristic-ell non-Star from the literal witness. IX10 proves all characteristic-zero attachment/purity transports, including restriction irreducibility and original coefficient maps. It does not supply the witness existence.')
    node('PAIRED_COUNT_ONE_INPUT_JOIN','All original count joins from one ImageDense premise',gate='AND',
        requires=['SYMPLECTIC_DATA_REALIZATION','SYMPLECTIC_MODEL_COMPARISON','LITERAL_NUMBER_SP4','SYMPLECTIC_PAIRED_ASSEMBLY'],
        status='human_complete_original_CountII_CountIII_implication',claims=['JX1'],
        theorem_antecedents=paired_cut,
        premise='Uniform C_chi before varying host/t/ell/Omega/O/e/psi; one iota before all points; actual same-D Model/grading/rigidity; original L and k; exact factor two and trace guard; permitted coefficient enlargement returns normalized length to the original ring.')
    node('REDUCED_POINT_HV_JOIN','Complete CountI plus CountV plus ImageDense to PointHV and guarded windows',gate='AND',
        requires=['POINT_HV_ASSEMBLY','SYMPLECTIC_COUNT_CHAIN'],
        status='human_complete_reduced_height_and_window_implication',claims=['JX2'],
        theorem_antecedents=height_cut,
        premise='The source four-count assembly is unchanged. CountII/III are supplied from ImageDense, while I and V remain actual inputs. JX2 preserves every original field/layer/constant choice and the window prime-pair guards. It does not supply the final arithmetic H-window.')

    update('SYMPLECTIC_SOURCE_COHOMOLOGY',gate='AND',
        requires=['FULL_LOCAL_BLOCH_KATO','NATIVE_FINITE_COHOMOLOGY','LOCAL_K_INTERFACE_MATCH','FINITE_DUALITY_SPECIALIZATION'],
        status='literal_entire_CohomologyHyp_record_supplied',claims=['BX8'],source_target_ids=[],
        retired_source_target_ids=['DA26-SP-04'],remaining_record_fields={},
        supplied_parts={'BlochKatoLocal':'BX7','LocalPublishedTheorems':'BX8','Entire CohomologyHyp':'BX8'},
        related_nodes=['ACTUAL_PHI_COND','ACTUAL_DEFORMATION_NUMERICS','ACTUAL_LOCAL_BASES'],
        premise='The node retains the entire original record meaning. BX supplies the previously missing full loc.bk and installs all seven local published and all six CohomologyHyp fields, preserving every source prime and antecedent. This does not construct seeds, support or automorphy.')
    update('SYMPLECTIC_RIGIDITY',gate='AND',requires=['DIRECT_SYMPLECTIC_RIGIDITY'],
        status='literal_RigiditySymplecticFour_supplied_by_direct_proof',claims=['RX6'],source_target_ids=[],
        retired_source_target_ids=['DA26-SP-06'],related_nodes=['ACTUAL_TANGENT_BLOCH_KATO','NATIVE_FINITE_COHOMOLOGY'],
        bypassed_not_promoted=['UnramifiedInputs','HypothesesH-prime','AdjointLiftingTheorem'],
        premise='The same literal RigiditySymplecticFour conclusion is now proved directly, hence the older rigSp4_alt implication follows from the stronger conclusion. Its larger source producer hypotheses are not reconstructed. The theorem retains actual IsAut4Alt in its original statement; application on the chosen D still needs that automorphy.')
    update('ACTUAL_SAME_DATUM_RIGIDITY',gate='AND',requires=['SYMPLECTIC_RIGIDITY','SYMPLECTIC_IMAGE_DENSITY','ACTUAL_LEVEL_SAFE_COMPARISON'],
        status='complete_actual_rigidity_installation_conditional_only_on_ImageDense',claims=['RX7'],
        source_target_ids=['DA27-SP-01'],remove=['retained_input_registry'],
        related_nodes=['ACTUAL_TANGENT_BLOCH_KATO'],
        premise='RX7 applies RX6 to each original irreducible EPt using the very same D and one common embedding supplied by ImageDense. Every actual dual-number PtIn lift has an sp4 commutator derivative. No independent unresolved rigidity premise remains after ImageDense.')
    update('SYMPLECTIC_FINITE_CATALOGUE',gate='AND',requires=['UNIFORM_FIXED_CM_CATALOGUES'],
        status='exact_SP9_catalogue_fully_supplied',claims=['CX8'],source_target_ids=[],
        related_source_target_ids=['DA26-SP-05'],remove=['retained_input_registry'],
        supplied_input_registry='symplectic_automorphic_catalogue/closure.json',
        premise='The original exact SP-R3 meaning is unchanged and now supplied: catalogue chosen before ell/Omega/iota/family, original AdmRAlt and level M, integral arithmetic eigenvalues, Aut(C) permutation with root/bit multiplicity, purity, injective full-label classification and every original-place Frobenius formula. Only labels use M^7. Broader all-rank unchanged-level declarations remain nonblocking unpromoted scopes.')
    update('SYMPLECTIC_IMAGE_DENSITY',gate='OR',
        alternatives=[['ACTUAL_IMAGE_CONDITION_JOIN','ACTUAL_CON_PURITY_AUTOMORPHY'],
                      ['PROMODULAR_TRANSPORT_JOIN','ACTUAL_PROMODULAR_REALIZATION']],
        status='actual_internal_and_promodular_implications_complete_arithmetic_realization_retained',
        source_target_ids=['DA25-HV-04','DA27-SP-02','DA28-SP-01','DA28-SP-02','DA28-SP-03'],
        claims=['IX8','IX9','IX10'],related_nodes=['SYMPLECTIC_SOURCE_COHOMOLOGY','ACTUAL_FINITE_MODULAR_QUOTIENT','EXACT_AUTOMORPHIC_SEEDS'],
        premise='The node still means literal Fin0/NoEnd/common-iota automorphy on every original Good/OfCase D. IX gives two sufficient conditional routes on the same objects. Neither the actual Con/Purity/Autm package nor the uniform ProModAlt witnesses are supplied; PMEx/seeds/support producers remain. Source producer links are not promoted merely by being present in the pinned Lean code.')
    update('SYMPLECTIC_DATA_REALIZATION',
        status='actual_G1_complete_one_ImageDense_premise',claims=['AX10','JX1'],
        premise='The full original G1 meaning is preserved. AX provides data, Good/OfCase, level and safe membership; ImageDense supplies Fin0/NoEnd and its one common embedding. RX/CX now close all previously separate rigidity/catalogue joins downstream, without constructing ImageDense.')
    update('SYMPLECTIC_MODEL_COMPARISON',
        status='actual_G2_complete_one_ImageDense_premise',claims=['MX10','PX10','RX7','JX1'],
        source_target_ids=['DA26-SP-03','DA27-SP-01'],
        premise='Full same-D G2, including actual Model.gr, M1-M4, points, trace and orbits, now follows once ImageDense is given. RX7 supplies the formerly retained actual rigidity from its same common embedding. Fin0/NoEnd and the ImageDense antecedent remain actual arithmetic data; the catalogue supplies the precise trace guard.')
    update('SYMPLECTIC_COUNT_CHAIN',
        requires=['PAIRED_COUNT_ONE_INPUT_JOIN'],
        status='complete_original_CountII_CountIII_implication_conditional_only_on_ImageDense',
        claims=['JX1'],source_target_ids=['DA24-HV-02','DA24-HV-03','DA25-HV-03','DA25-HV-04','DA27-SP-02'],
        supplied_inputs={**byid['SYMPLECTIC_COUNT_CHAIN']['supplied_inputs'],
            'Entire CohomologyHyp':'BX8','Literal rigidity and same-D installation':'RX6/RX7',
            'Exact catalogue and NumberSp4Alt':'CX8/CX9','All actual count joins':'JX1'},
        remaining_bespoke_cut=paired_cut,
        premise='The node still means actual CountII and CountIII with unchanged uniform quantifiers. JX1 supplies every downstream join from ImageDense, including exact C_chi choice, common embedding, original coefficient return and factor two. It is a complete implication with one substantive remaining antecedent, not unconditional counts.')
    update('COUNT_I_SUPPLIER',
        status='actual_CountI_chain_retained_full_cohomology_available',
        supplied_general_inputs={'Entire CohomologyHyp where the identical record is requested':'BX8'},
        premise='Literal original CountI is still required. Its actual Kato/unitary, rank-two/rank-three arithmetic, automorphy, adjoint vanishing and counting/model chain remains; complete rank-four catalogue/rigidity does not by itself install those differently quantified inputs.')
    update('COUNT_V_SUPPLIER',
        status='actual_CountV_host_frame_chain_retained_full_cohomology_available',
        supplied_general_inputs={**byid['COUNT_V_SUPPLIER']['supplied_general_inputs'],'Entire CohomologyHyp where the identical record is requested':'BX8'},
        related_nodes=['LEMMA_M_PRIME','LEMMA_M','NATIVE_FINITE_COHOMOLOGY','FULL_LOCAL_BLOCH_KATO'],
        premise='The actual ThmS6_s/HostVanE/HostXpp/HostRigid_s/HostNumber_s host and marked-point chain remains. BX closes its identically requested cohomological leaves, not those arithmetic objects. CX/RX is rank-four-specific; no unmatched host catalogue or rigidity is inferred. CountVs remains distinct from CountV.')
    update('ACTUAL_POINT_COUNTS',
        status='CountZ_supplied_II_III_from_ImageDense_I_V_retained',
        premise='The original five count meanings are preserved. CountZ is unconditional in its proved scope; JX1 supplies II/III from ImageDense; actual CountI and CountV remain. HV supplies the case/layer/sum assembly; no four-count predicate is replaced by a merely named theorem.')
    update('ODD_PLUS_BOUND',
        status='complete_PointHV_implication_with_CountI_CountV_ImageDense_cut',
        claims=['HV10','JX2'],remaining_actual_inputs=height_cut,
        remaining_paired_count_cut=paired_cut,related_nodes=['LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','ACTUAL_POINT_COUNTS','REDUCED_POINT_HV_JOIN'],
        supplied_inputs={**byid['ODD_PLUS_BOUND']['supplied_inputs'],'CountII and CountIII from ImageDense':'JX1','Reduced sufficient height input':'JX2'},
        premise='Literal PointHV is unchanged. JX2 supplies its full implication from actual CountI, CountV and ImageDense using JX1 and HV10. The common original field, separate reference-layer models, host, twist cutoff and order of every uniform constant are retained. The three antecedents remain.')
    update('COHOMOLOGICAL_WINDOW',
        status='complete_guarded_window_chain_with_CountI_CountV_ImageDense_cut',
        claims=['VW3','JX2'],remaining_paired_count_cut=paired_cut,remaining_count_cut=height_cut,
        premise='TW8 and OB8 supply simultaneous two-primary and odd-minus240. JX2 supplies the complete odd-plus-to-window propagation from CountI/CountV/ImageDense with the established prime-pair guards. Original E is common to the three summands; separately quantified reference layers share the fixed pair/window and need not equal E. No final H-window or global family follows without its independent inputs.')
    update('FIXED_PAIR_WINDOWS',
        status='complete_fixed_pair_window_implication_with_reduced_count_cut',
        claims=['QP22','VW4','JX2'],remaining_paired_count_cut=paired_cut,
        remaining_cohomological_supplier=height_cut,
        premise='The same pair q,d works on every real scale in a late interval. JX2 reduces the remaining count input to CountI/CountV/ImageDense, with the original prime-pair and separately quantified layer-model ties. Ct=401 yields cutoff400. Compatible host, global family and arithmetic gap are independent obligations.')

    for old in baseline['nodes']:
        current=byid[old['id']]
        if old['id'] in changed:
            assert current['history'][-1]=={'version':'0.27','snapshot':old},old['id']
        else:
            assert current==old,old['id']
    seen,active=set(),set()
    def visit(nid):
        assert nid in byid,nid
        if nid in seen:return
        assert nid not in active,('cycle',nid)
        active.add(nid)
        n=byid[nid]
        assert n['gate'] in {'AND','OR','LEAF'},nid
        if n['gate']=='LEAF':assert not n.get('requires') and not n.get('alternatives'),nid
        for dep in n.get('requires',[])+[x for group in n.get('alternatives',[]) for x in group]:visit(dep)
        active.remove(nid);seen.add(nid)
    for nid in byid:visit(nid)
    tids={t['id'] for t in targets}
    assert len(tids)==len(targets)
    available_claims=all_new_claims|{c for n in baseline['nodes'] for c in n.get('claims',[])}
    for n in m['nodes']:
        for dep in n.get('related_nodes',[]):assert dep in byid,dep
        for tid in n.get('source_target_ids',[])+n.get('related_source_target_ids',[]):assert tid in tids,(n['id'],tid)
        for cid in n.get('claims',[]):assert cid in available_claims,(n['id'],cid)
    m['validation']={**m.get('validation',{}),'node_count':len(m['nodes']),
        'node_ids_unique':True,'acyclic':True,'all_edges_resolve':True,'all_related_nodes_resolve':True,
        'all_current_target_ids_resolve':True,'all_current_claim_ids_resolve':True,
        'historical_node_meanings_preserved':True,'historical_node_count':len(baseline['nodes']),
        'changed_historical_nodes':changed,'complete_previous_records_preserved':True,
        'historical_validation_preserved_in_previous_map':True,
        'whole_CohomologyHyp_or_LocalPublished_promoted':True,'basis_for_full_record_promotion':'BX7/BX8 exact full interface matching',
        'unconditional_ImageDense_or_paired_counts_promoted':False,
        'all_rank_or_unchanged_level_catalogue_promoted':False,
        'actual_rigidity_distinguished_from_generic_source_rigidity':True,
        'related_node_annotations_are_not_proof_edges':True}
    anchors=sorted(source_index.values(),key=lambda a:(a['path'],a['line_start'],a['line_end']))
    source_obj={'commit':PIN,'sources':anchors,'source_files':len(blobs),'source_ranges':len(anchors)}
    source_bytes=(json.dumps(source_obj,ensure_ascii=False,indent=2)+'\n').encode()
    m['source_manifest_sha256']=sha(source_bytes)
    (HERE/'previous_obligation_map.json').write_bytes((OLD/'obligation_map.json').read_bytes())
    write('obligation_map.json',m)
    write('source_anchors.json',source_obj)
    write('next_targets.json',{'targets':targets})
    write('retirement_candidates.json',{'targets':retired})
    write('target_scope_updates.json',updates)
    write('global_branch_scope_updates.json',{'updates':global_scope_updates})
    write('symplectic_frontier_sources.json',{'actual_image_density_frontier':ix_frontier,
        'paired_count_remaining_cut':paired_cut,'height_remaining_cut':height_cut,
        'broader_catalogue_source_scope_unpromoted_and_nonblocking':['All-rank CountQAlt','Unchanged-level LevelPNAlt'],
        'related_nodes_are_not_proof_edges':True})
    file_input(HERE/'build_audit.py')
    file_input(HERE/'audit.txt')
    write('input_manifest.json',{'artifact_version':'0.28','components':COMPONENTS,
        'review_input_policy':'Only explicit mathematical component reviews/source validations and integration-scope reviews. Downstream semantic/final-scope/coverage/package/audit outputs are excluded to prevent circular hashes.',
        'files':[input_index[k] for k in sorted(input_index)]})
    write('summary.json',{'artifact_version':'0.28','new_claim_ids':[],
        'increment_supplier_claims':component_claims,'retirement_candidate_ids':list(retirement),
        'retirement_count':len(retired),'historical_nodes_preserved':len(baseline['nodes']),
        'map_node_count':len(m['nodes']),'changed_historical_node_ids':changed,
        'remaining_independent_count_suppliers':['CountI','CountV'],
        'conditional_supplied_counts':{'CountII and CountIII':'JX1 from literal ImageDense'},
        'supplied_counts':{'CountZ':'CZ6','CountVs':'HV5','CountIV':'HV6'},
        'remaining_count_assembly':False,'paired_count_remaining_cut':paired_cut,'height_remaining_cut':height_cut,
        'current_count_cut':height_cut,
        'whole_CohomologyHyp_promoted':True,'whole_CohomologyHyp_supplier':'BX8',
        'literal_RigiditySymplecticFour_supplier':'RX6','same_D_rigidity_from_ImageDense_supplier':'RX7',
        'exact_SP9_catalogue_supplier':'CX8','literal_NumberSp4Alt_supplier':'CX9',
        'not_globally_closed':['RH','Dirichlet GRH','PointHV','Actual CountI and CountV',
          'Unconditional actual CountII and CountIII','SymplecticFourImageDense',
          'Actual PMExAlt, seed and uniform ProModAlt realization',
          'Actual-family LinkN','Actual compatible family/DesignExists/HostExW',
          'Theta/type/rank/metric/spectral joins','Final arithmetic gap/gain'],
        'unpromoted_but_not_required_for_selected_rigidity_catalogue_endpoints':[
          'Full UnramifiedInputs','AdjointLiftingTheorem','HypothesesH-prime',
          'LiteratureRankNHypothesis','All-rank CountQAlt','Unchanged-level LevelPNAlt']})
    write('verification.json',{'artifact_version':'0.28','source_commit':PIN,
        'source_files_checked':len(blobs),'source_ranges_indexed':len(anchors),
        'all_cited_source_files_equal_pinned_git_blobs':True,'all_source_range_hashes_verified':True,
        'new_component_proof_ranges_verified':len(proof_checks),'all_component_main_and_proof_hashes_match':True,
        'available_component_manifest_entries_verified':component_manifest_checks,
        'previous_release_input_manifest_verified':True,'historical_node_ids_preserved':True,
        'complete_changed_node_snapshots_verified':True,'historical_snapshot_byte_identical':True,
        'sufficient_condition_graph_acyclic':True,'current_validation_node_count':len(m['nodes']),
        'historical_validation_not_edited':True,'all_related_and_target_ids_resolve':True,
        'prior_files_modified':False,'root_targets_modified':False,'new_claim_ids':[],
        'Lean_kernel_replay_run':False,'formal_transitive_Lean_dependency_audit':False,
        'audit_txt_sha256':sha((HERE/'audit.txt').read_bytes()),
        'scope':'Human semantic sufficient-condition audit. Integrity and graph checks validate provenance/bookkeeping, not mathematical proofs.'})
    print(json.dumps({'retirements':len(retired),'targets':len(targets),'source_files':len(blobs),
        'source_ranges':len(anchors),'proof_ranges':len(proof_checks),'historical_nodes':len(baseline['nodes']),
        'map_nodes':len(m['nodes']),'manifest_inputs':len(input_index)},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=WORK.parent/'lean-source')
    main(parser.parse_args().repo.resolve())

