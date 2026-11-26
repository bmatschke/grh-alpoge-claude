#!/usr/bin/env python3
"""Rebuild the v0.24 semantic audit without mutating historical/root files."""
import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OLD = WORK / 'dependency_audit_v0_23'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_text())


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def main(repo):
    blobs = {}

    def blob(path):
        if path not in blobs:
            data = (repo / path).read_bytes()
            pinned = subprocess.check_output(['git', '-C', str(repo), 'show', PIN + ':' + path])
            assert data == pinned, ('worktree differs from pinned source', path)
            blobs[path] = data
        return blobs[path]

    def verify(rec):
        b = blob(rec['path'])
        frag = b''.join(b.splitlines(keepends=True)[rec['line_start']-1:rec['line_end']])
        assert sha(b) == rec['sha256'], ('file hash', rec['path'])
        assert sha(frag) == rec['range_sha256'], ('range hash', rec['path'], rec['line_start'])
        assert PIN in rec['url']
        return rec

    def anchor(path, declaration, start=None, end=None):
        b = blob(path)
        lines = b.decode().splitlines()
        if start is None:
            pat = re.compile(r'^(?:def|theorem|structure|abbrev)\s+' + re.escape(declaration) + r'(?=[\s:(])')
            hits = [i+1 for i, l in enumerate(lines) if pat.match(l)]
            assert len(hits) == 1, (declaration, path, hits)
            start = hits[0]
        if end is None:
            end = len(lines)
            for i in range(start, len(lines)):
                if re.match(r'^(?:def|theorem|structure|abbrev|namespace|end)\b', lines[i]):
                    end = i
                    break
            while end > start and not lines[end-1].strip():
                end -= 1
        frag = b''.join(b.splitlines(keepends=True)[start-1:end])
        return {'path': path, 'declaration': declaration, 'line_start': start, 'line_end': end,
                'sha256': sha(b), 'range_sha256': sha(frag), 'range_bytes': len(frag),
                'first_line': lines[start-1], 'verified_equal_to_pinned_git_blob': True,
                'url': f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'}

    baseline = read(OLD / 'obligation_map.json')
    old_targets = read(OLD / 'next_targets.json')['targets']
    old_sources = read(OLD / 'cut_interface_sources.json')['sources']
    ln = read(WORK / 'congruence_chain/closure.json')
    for a in old_targets + old_sources:
        verify(a)

    retirement = {
        'DA-next-01-c': {'supplied_by': ['OS1', 'OS9', 'OB1', 'OB2', 'OB3', 'OB4', 'OB5', 'OB6', 'OB7', 'OB8'],
                         'scope': 'Literal ThmBcFree with C=240, including the non-PsiBound arithmetic ingredients; relative only to named matched classical leaves.'},
        'DA-next-01-d': {'supplied_by': ['LD2', 'LD4', 'OS1', 'OS2', 'OS3', 'OS4', 'OS5', 'OS6', 'OS7', 'OS8', 'OS9'],
                         'scope': 'Literal universal PsiBound, original E/Omega/O/rho/psi, including a=0; relative only to named matched classical leaves.'},
        'DA-next-02-b': {'supplied_by': ['LN1', 'LN2', 'LN3', 'LN4', 'LN5', 'LN6', 'LN7', 'LN9'],
                         'scope': 'Full stated conditional cut-to-original linkN_of_gd transport, exact d_j log|G| loss and unchanged cohomological term; not unconditional actual-family LinkN.'}
    }
    updates = {
        'DA-next-01-a': {
            'human_status': 'two_primary_and_reference_layer_supplier_retained_global_PoitouTate_matched',
            'supplied_by': ['LD3'],
            'supplied_parts': ['Exact GlobalTheory.Published.PoitouTateDuality finite-module specialization'],
            'remaining_human_scope': 'Literal simultaneous ThmBab on one K for all Ct>=1: reconstruct tower bounds, finite-exception common windows and field transports from LemmaK and the exact local-K/Ferrero-Washington inputs.',
            'retained_inputs': 'LocalFinitenessK, LocalTateDualityK, existence of CK with literal LemmaK, exact Published.FerreroWashington specialization, and the remaining two-primary/reference-layer construction.'},
        'DA-next-01-b': {
            'human_status': 'odd_plus_supplier_retained_global_PoitouTate_matched',
            'supplied_by': ['LD3'],
            'supplied_parts': ['Exact GlobalTheory.Published.PoitouTateDuality finite-module specialization'],
            'remaining_human_scope': 'Literal PointHV with all original field/host/reference-layer quantifiers; reconstruct actual CountI/II/III/V/Z suppliers and their sums and layer descent.',
            'retained_inputs': 'LocalFinitenessK, LocalTateDualityK, LemmaK CK and CountI/II/III/V/Z; exact common constants must precede hosts and varying layers.'}
    }
    for x in ln['partial_target_updates']:
        updates[x['id']] = {'human_status': x['status'], 'supplied_by': x['supplied_by'],
                            'supplied_parts': [x['closed_part']], 'remaining_human_scope': x['retained'],
                            'retained_inputs': x['retained']}
    targets = []
    retired = []
    for old in old_targets:
        q = copy.deepcopy(old)
        q['history'] = [{'version': '0.23', 'status': old['status'], 'retained_inputs': old['retained_inputs']}]
        if q['id'] in retirement:
            q.update(retirement[q['id']])
            q['status'] = 'safe_to_retire_only_in_stated_scope'
            retired.append(q)
        else:
            q.update(updates[q['id']])
            q['status'] = q['human_status']
            targets.append(q)

    def add_target(tid, path, declaration, package, retained, downstream, **kw):
        q = anchor(path, declaration, **kw)
        q.update({'id': tid, 'work_package': package, 'status': 'precise_remaining_human_supplier_or_interface',
                  'retained_inputs': retained, 'remaining_human_scope': retained, 'downstream': downstream})
        targets.append(q)

    coho = 'remaining_cohomological_window'
    down = 'ThmBab and PointHV, together with OB8 -> VW4/VW3 -> literal VWinAt -> QP22 fixed-pair windows'
    add_target('DA24-K-01', P+'GeneratorCountTuples/LemmaK.lean', 'LemmaK', coho,
               'Universal finite H2 and its kBound estimate for all original totally complex L/Omega/LData, every prime and e>=1, with one CK.', down)
    add_target('DA24-K-02', P+'GeneratorCountTuples/Bridge.lean', 'KBridge', coho,
               'Actual finite Z_l module, surjection to the original H2 and comparison into Z_l tensor HGL, with kernel killed by l^cOne(2e). A K-theory theorem name alone does not supply this exact bridge.', down)
    add_target('DA24-K-03', P+'GeneratorCountTuples/LemmaKOfPublished.lean', 'lemmaK', coho,
               'Human reconstruction of KBridge plus torsion homology estimate -> LemmaK. LD3 supplies hP; local-K matching, bridge and quantitative torsion supplier remain.', down)
    add_target('DA24-K-04', P+'GeneratorCountTuples/TorsBoundPow.lean', 'TorsBoundPow', coho,
               'Finiteness and uniform quantitative torsion homology bound at HGL L (4e+4) (2e). The short torsMain source wrapper is not a readable proof of this geometric/combinatorial bound.', down)
    add_target('DA24-LK-01', 'src/Formalism/GaloisCohomology/LocalTateDualityK.lean', 'LocalFinitenessK', coho,
               'Match finite cohomology in degrees 0,1,2 and vanishing above 2 for every finite discrete Z/l^r module on each finite K subset PadicAlgCl(l), including residue characteristic l.', down)
    add_target('DA24-LK-02', 'src/Formalism/GaloisCohomology/LocalTateDualityK.lean', 'LocalTateDualityK', coho,
               'Match the actual cycK representation, H2 scalar identification and all four cup-map bijectivities, including the flipped H1 pairing, for finite modules not assumed free.', down)
    add_target('DA24-LK-03', 'src/Formalism/GaloisCohomology/LocalTateDualityK.lean', 'LocalEulerCharK', coho,
               'Adjacent local-field interface: exact p-adic Euler factor |H1|=|H0||H2||M|^[K:Q_l]. This is not needed as a separate input of the two displayed final wrappers, and LD1 away-residue tame Euler does not prove it.', 'Local cohomology packages used in deeper source suppliers; retain until exact specialization is written.')
    add_target('DA24-FW-01', P+'PublishedTheorems/FerreroWashington.lean', 'FerreroWashington', coho,
               'Match or reconstruct the exact bounded l-rank of class groups across the stated abelian cyclotomic layers, including l=2 and the specified roots of unity. Classical mu=0 requires its control/translation here.', down)
    for suffix, decl in [('01','CountI'),('02','CountII'),('03','CountIII'),('04','CountV'),('05','CountZ')]:
        add_target('DA24-HV-'+suffix, P+'HeightAndVanishing/Counts.lean', decl, coho,
                   ('Actual '+decl+' for the original host, coefficient rings, characters, twists and finite prime sets, with constants chosen before the hosts. These are substantial Galois/automorphy/vanishing bounds, not the numerical finite summations already written.'), down)
    add_target('DA24-HV-06', P+'HeightAndVanishing/VwinOfLeaves.lean', 'countI', coho,
               'Exposed deeper CountI route retains LitN, LemmaK, RigII, AdVanishK, CongruenceNumberRankThree and AutomorphyUnramifiedCoefficients; RigII itself retains AdVanishQ, NewformAut and KatoTwo. Match each exact statement and its same-object compatibility.', down)
    for q in read(WORK / 'congruence_chain/next_targets.json')['targets']:
        verify(q)
        targets.append(copy.deepcopy(q))

    # Additional definitions document the semantic cut without creating artificial tasks.
    extra = [anchor(P+'PrimeSetBoundDataOfPrimitiveChar.lean', 'ThmBab'),
             anchor(P+'HeightAndVanishing/LayerLe.lean', 'PointHV'),
             anchor(P+'HeightAndVanishing/Counts.lean', 'CountShape'),
             anchor(P+'GeneratorCountTuples/Reduction.lean', 'lemmaK_of'),
             anchor(P+'HermiteNormalForms/TorsMain.lean', 'UpperTheory.V.KT.torsMain'),
             anchor(P+'TensorHomCubes/KBridgeOfKPublished.lean', 'Published.KPublished')]

    m = copy.deepcopy(baseline)
    m['artifact_version'] = '0.24'
    m['previous_map'] = 'previous_obligation_map.json'
    m['baseline'] = '0.23'
    m['increment_integration'] = ('OS1-OS9, OB1-OB8 and LD1-LD4 close the actual odd-minus chain through literal PsiBound and ThmBcFree(C=240), relative to matched classical leaves. LN1-LN10 close the conditional original-family congruence chain; actual local tables and type/theta/spectral bindings remain. No root RH/Dirichlet-GRH closure is asserted.')
    byid = {n['id']: n for n in m['nodes']}

    def update_node(nid, **changes):
        n = byid[nid]
        prev = copy.deepcopy(n)
        n.setdefault('history', []).append({'version': '0.23', 'snapshot': prev})
        n.update(changes)

    def node(nid, title, gate='LEAF', **kw):
        assert nid not in byid
        n = {'id': nid, 'title': title, 'gate': gate, 'introduced_in': '0.24', **kw}
        m['nodes'].append(n)
        byid[nid] = n

    update_node('ODD_MINUS_BOUND', gate='AND', requires=['ODD_MINUS_QUANTITATIVE'],
                status='human_supplier_complete_relative_to_named_matched_classical_leaves',
                claims=['OB8'], premise='Literal ThmBcFree with one universal C=240 on every original CM abelian field, closure and local-data family; all finite odd-prime sets and 1<=e<t. VW4 supplies ThmBc from this exact statement. No two-primary or odd-plus bound is inferred.')
    node('ODD_MINUS_QUANTITATIVE', 'All-prime odd-minus quantitative assembly, C=240', 'AND',
         requires=['PSI_BOUND_SUPPLIER','FINITE_JACOBI_SYSTEM','CLASSICAL_ODD_MINUS_INPUTS'],
         status='human_chain_complete_relative_to_named_matched_classical_leaves', claims=[f'OB{i}' for i in range(1,9)],
         binding_keys=['original E','original Omega','attained conductor','original LData family','fixed base degree exceptional primes','all twists e<t'],
         note='OB3 uses OS9. OB5 uses OS1, so no separate Stickelberger theorem is retained. OB2 nonvanishing is independent of OS9.')
    node('PSI_BOUND_SUPPLIER', 'Literal original-field PsiBound', 'AND',
         requires=['FINITE_JACOBI_SYSTEM','FINITE_DUALITY_SPECIALIZATION','CLASSICAL_FINITE_ARITHMETIC'],
         status='human_supplier_complete_relative_to_named_matched_classical_leaves', claims=[f'OS{i}' for i in range(2,10)],
         premise='Original E, Omega, coefficient DVR O, cyclotomic action rho, character psi and negative Tate twist; all algebraic values a including a=0 with infinite valuation. Finite-level Jacobi/Kolyvagin/reciprocity chain, not an unproved Iwasawa control argument.')
    node('FINITE_JACOBI_SYSTEM', 'Explicit finite Jacobi ideal and distribution identities', 'AND',
         requires=['CLASSICAL_FINITE_ARITHMETIC'], status='human_chain_complete_relative_to_named_matched_classical_leaves', claims=['OS1'],
         note='Carries, ideal factorization, norm and congruence recurrences proved; exact group-ring orientation also supplies OB5.')
    node('FINITE_DUALITY_SPECIALIZATION', 'Exact finite duality and reciprocity interfaces', 'AND',
         requires=['CLASSICAL_FINITE_DUALITY'], status='human_interface_matching_complete_in_stated_scope', claims=['LD1','LD2','LD3','LD4'],
         complete_interfaces=['ReciprocityTheory.Gal.UnramifiedOrthogonality','GlobalTheory.Published.PoitouTateDuality'],
         excluded_interfaces=['LocalFinitenessK not globally certified here','LocalTateDualityK not globally certified here','LocalEulerCharK not globally certified here'])
    node('CLASSICAL_FINITE_DUALITY', 'Matched finite local Tate, local class field and Poitou-Tate theorems',
         status='named_established_classical_inputs_with_written_specializations', registry='local_duality_closure/classical_references.json')
    node('CLASSICAL_FINITE_ARITHMETIC', 'Finite cyclotomic, Chebotarev, Hilbert-class-field and Kummer inputs',
         status='named_established_classical_inputs_with_written_specializations', registry='odd_minus_supplier/provenance.json:classical_inputs',
         input_ids=['OS-CYC','OS-CHEB','OS-HCF','OS-KUM'])
    node('CLASSICAL_ODD_MINUS_INPUTS', 'Class-field, S-unit, discriminant, Bernoulli and local-field inputs',
         status='named_established_classical_inputs_with_written_specializations', registry='odd_minus_bounds/classical_inputs.json',
         input_ids=['OB-CF','OB-KU','OB-MD','OB-BC','OB-LF'], not_retained=['General Stickelberger theorem replaced by OS1 -> OB5'])
    update_node('COHOMOLOGICAL_WINDOW', status='human_assembly_complete_two_bespoke_suppliers_remain',
                completed_input_suppliers={'ODD_MINUS_BOUND':'OB8 via OS9 and OS1'},
                remaining_bespoke_suppliers=['TWO_PRIMARY_BOUND','ODD_PLUS_BOUND'],
                premise='VW1-VW4 retain actual field/conductor/local data, same q,d and full real windows. Odd-minus is now supplied; simultaneous ThmBab and PointHV remain. These two are suppliers on the selected route, not a statement that all other global arithmetic inputs are done.')
    update_node('TWO_PRIMARY_BOUND', status='major_supplier_unreconstructed_with_one_duality_input_discharged',
                supplied_inputs={'GlobalTheory.Published.PoitouTateDuality':'LD3'},
                premise='One K works for every Ct>=1. Remaining literal LemmaK, LocalFinitenessK/LocalTateDualityK matching, exact FerreroWashington specialization and common-window/tower construction; includes both two-primary and odd reference layers.',
                related_nodes=['LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','FERRERO_WASHINGTON_MATCH'])
    update_node('ODD_PLUS_BOUND', status='major_supplier_unreconstructed_with_one_duality_input_discharged',
                supplied_inputs={'GlobalTheory.Published.PoitouTateDuality':'LD3'},
                premise='Literal PointHV for all original hosts, fields, local data and arbitrary fixed reference-layer function j. LemmaK, LocalFinitenessK/LocalTateDualityK, actual CountI/II/III/V/Z and their assembly remain.',
                related_nodes=['LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','ACTUAL_POINT_COUNTS'])
    node('LEMMA_K_BOUND', 'Actual uniform finite H2 bound LemmaK', status='major_quantitative_supplier_unreconstructed',
         source_target_ids=['DA24-K-01','DA24-K-02','DA24-K-03','DA24-K-04'],
         premise='KBridge and quantitative arithmetic-group torsion homology must be reconstructed or replaced by precisely matched theorems. A structure listing K-theoretic hypotheses does not itself prove KBridge.')
    node('LOCAL_K_INTERFACE_MATCH', 'Exact p-adic local-K interface specializations', status='classical_statement_matching_remaining',
         source_target_ids=['DA24-LK-01','DA24-LK-02','DA24-LK-03'],
         premise='Finite nonfree modules, actual cycK cup maps and both H1 pairings; all residue-characteristic cases. LocalEulerCharK has the p-adic |M|^[K:Q_l] factor. LD establishes only its recorded endpoints.')
    node('FERRERO_WASHINGTON_MATCH', 'Exact bounded class-group rank in cyclotomic layers', status='classical_statement_matching_or_finite_source_reconstruction_remaining',
         source_target_ids=['DA24-FW-01'], premise='Match the stated all-layer class-group quotient bound with roots of unity, including l=2; a bare mu=0 citation omits its control and finite-layer transfer.')
    node('ACTUAL_POINT_COUNTS', 'Original-host CountI/II/III/V/Z', status='major_galois_automorphy_and_vanishing_suppliers_unreconstructed',
         source_target_ids=[f'DA24-HV-{i:02d}' for i in range(1,7)],
         premise='These count predicates contain actual arithmetic content. The exposed CountI source route includes Kato rigidity, adjoint vanishing, rank-three congruence estimates and automorphy with unramified coefficients.')
    update_node('C_LINK_N', gate='AND',
                requires=['LN_ORIGINAL_FAMILY_CHAIN','ACTUAL_LOCAL_DENOMINATOR_TABLE','ACTUAL_TYPE_THETA_SPECTRAL_BINDINGS','UNIFORM_FAMILY_PARAMETER_INPUT'],
                status='conditional_original_family_chain_complete_actual_suppliers_open', claims=[f'LN{i}' for i in range(1,11)],
                premise='LN10 proves original LinkN from the explicit actual local table and compatible state. It preserves the original vvTerm and exact d_j coefficient; original cut loss is d_j log|G|. Actual suppliers are not supplied by the implication.',
                conclusion_guards=['ShaFinOdd of the actual D','Summable of the actual vvTerm'],
                guard_note='These are antecedents of literal LinkN, not extra antecedents needed to prove the conditional predicate. They must be supplied when a downstream theorem consumes its numerical conclusion.',
                related_nodes=['STRONG_CUT_FACTS'])
    node('LN_ORIGINAL_FAMILY_CHAIN', 'Integral cut to original-family denominator comparison', status='human_conditional_chain_complete',
         claims=[f'LN{i}' for i in range(1,11)],
         premise='Complete coordinate-ideal filtration, multiplicity and rank accounting, exact place weights, elementary all-prime sum, unchanged cohomological term, uniform cut restoration.',
         quantifier='For each actual Fm, exists K,x0 before all scales x and all i in Fm.Ix(x); no finite underlying family-index set is assumed.')
    node('ACTUAL_LOCAL_DENOMINATOR_TABLE', 'Actual local Galois-to-coordinate-ideal bounds', status='major_supplier_unreconstructed',
         source_target_ids=['LN-next-01','LN-next-02','LN-next-03','LN-next-04'],
         premise='Literal original or actual-cut vcc ideals, split/inert regimes, cyclotomic scalar, band condition, exceptional and small/q,d prime bounds, with one uniform C. The numerical prime summation is already LN8.')
    node('ACTUAL_TYPE_THETA_SPECTRAL_BINDINGS', 'Same-state type action, spanning, theta and rank identities', status='same_object_suppliers_retained',
         source_target_ids=['LN-next-06'],
         premise='Exact ordered-tuple e0 action, tame dictionary, same-point constituent permutation, actual rational spectral spanning, ConclusionZ, internal isotypic decomposition, localization uniqueness, nonzero theta scalars and actual reference/twisted rank equality unless both required injectivities are established.')
    node('UNIFORM_FAMILY_PARAMETER_INPUT', 'Original parameter record and uniform polynomial rank budget', status='actual_family_instantiation_retained',
         premise='Apply PN16 and the stated rank/density/class-number estimates to the original Fm. LN9 proves the group-order logarithm, but does not construct the compatible family or identify its rank with D0.')
    node('STRONG_CUT_FACTS', 'Same-cut NormChoiceFacts and Tie4 for source bundle routes', status='stronger_optional_route_supplier_retained',
         source_target_ids=['LN-next-05'],
         premise='CutGivesAlt is stronger than CutD.Good. LN2 does not establish all NormChoiceFacts/Tie4. This node belongs to the source bundle/cut route; it is not an extra requirement for the alternative direct original-table route.')

    # Preserve node identities and expose only sufficient routes; related nodes are annotations.
    assert set(n['id'] for n in baseline['nodes']) <= set(byid)
    edges = {}
    for n in m['nodes']:
        es = n.get('requires', []) if n['gate'] == 'AND' else [x for a in n.get('alternatives', []) for x in a] if n['gate'] == 'OR' else []
        assert all(e in byid for e in es), n['id']
        edges[n['id']] = es
    active, done = set(), set()
    def visit(n):
        assert n not in active, ('cycle', n)
        if n in done:
            return
        active.add(n)
        for e in edges[n]: visit(e)
        active.remove(n); done.add(n)
    for n in byid: visit(n)
    tids = {q['id'] for q in targets}
    assert len(tids) == len(targets), 'duplicate target ID'
    for n in m['nodes']:
        assert all(x in byid for x in n.get('related_nodes', [])), n['id']
        assert all(x in tids for x in n.get('source_target_ids', [])), n['id']

    write('previous_obligation_map.json', baseline)
    write('obligation_map.json', m)
    write('target_scope_updates.json', updates)
    write('retirement_candidates.json', {'artifact_version':'0.24','root_targets_modified':False,'candidates':retired})
    packages = [
        {'id':'remaining_cohomological_window','priority':1,
         'endpoint':'ThmBab on one K and literal PointHV -> already completed VW assembly with OB8 -> original-field VWinAt and QP22 same-pair full windows',
         'first_subchain':'Exact local-K specializations and LemmaK/KBridge plus quantitative torsion bound, then simultaneous ThmBab. Reuse LemmaK for PointHV; expose arithmetic count leaves rather than rename them.',
         'do_not_claim':'The final RH/GRH gain or actual host/family exists merely from VWinAt.'},
        {'id':'actual_congruence_family','priority':2,
         'endpoint':'Actual compatible local tables and type/theta/spectral state -> LN10 original LinkN -> DA2 with HypV and actual dZ0=D0',
         'first_subchain':'Close a whole local-denominator table on one actual common family, including small exceptional primes; use direct original-table route or complete NormChoiceFacts/Tie4 if using the cut bundle.',
         'do_not_claim':'CutD.Good equals CutGivesAlt, or a numerical Kudla sum supplies actual AdmF.'}]
    write('next_targets.json', {'artifact_version':'0.24','source_commit':PIN,
          'scope':'Precise remaining human targets and component-entry anchors; counts are indexing data, not completion percentages.',
          'work_packages':packages,'targets':targets})

    # Index all cited declarations, with historical and new ranges retained verbatim.
    source_index = {}
    for a in old_sources + old_targets + targets + extra:
        verify(a)
        key = (a['path'],a['line_start'],a['line_end'])
        source_index[key] = {k:v for k,v in a.items() if k in ['path','declaration','line_start','line_end','sha256','range_sha256','range_bytes','first_line','verified_equal_to_pinned_git_blob','url']}
    write('source_anchors.json', {'source_commit':PIN,'range_convention':'One-based inclusive line ranges; original UTF-8 bytes and line endings retained.','sources':list(source_index.values())})
    inputs = ['dependency_audit_v0_23/obligation_map.json','dependency_audit_v0_23/next_targets.json','dependency_audit_v0_23/cut_interface_sources.json']
    for c in ['odd_minus_supplier','odd_minus_bounds','local_duality_closure','congruence_chain']:
        inputs += [c+'/main.tex',c+'/provenance.json',c+'/closure.json']
        pr, cl = read(WORK/c/'provenance.json'), read(WORK/c/'closure.json')
        assert pr['commit'] == PIN
        assert cl.get('main_tex_sha256',pr.get('main_tex_sha256')) == sha((WORK/c/'main.tex').read_bytes()), ('component frozen hash',c)
    inputs += ['odd_minus_bounds/classical_inputs.json','local_duality_closure/classical_references.json','congruence_chain/next_targets.json']
    manifest = [{'path':p,'sha256':sha((WORK/p).read_bytes()),'bytes':(WORK/p).stat().st_size} for p in inputs]
    write('input_manifest.json', {'source_commit':PIN,'inputs':manifest})
    write('integration_delta.json', {
        'artifact_version':'0.24','source_commit':PIN,'new_claim_ids':[],
        'safe_to_retire_exact_target_ids':list(retirement),'retirement_scope':'See retirement_candidates.json; this audit does not edit root targets.',
        'partial_target_updates':'target_scope_updates.json','priority_successors':packages,
        'historical_nodes_preserved':True,'prior_node_count':len(baseline['nodes']),
        'new_supplier_claims':{'odd_minus_supplier':[f'OS{i}' for i in range(1,10)],'odd_minus_bounds':[f'OB{i}' for i in range(1,9)],'local_duality_closure':[f'LD{i}' for i in range(1,5)],'congruence_chain':[f'LN{i}' for i in range(1,11)]},
        'not_globally_closed':['RH','Dirichlet GRH','ThmBab','PointHV','actual-family LinkN','LocalFinitenessK','LocalTateDualityK','LocalEulerCharK','CutGivesAlt','actual common family / DesignExists','remaining host, theta, metric, spectral and arithmetic gap suppliers']})
    write('verification.json', {'source_commit':PIN,'all_cited_source_files_equal_pinned_git_blobs':True,
          'all_source_range_hashes_verified':True,'source_files_checked':len(blobs),'source_ranges_indexed':len(source_index),
          'historical_node_ids_preserved':True,'sufficient_condition_graph_acyclic':True,
          'all_component_frozen_main_hashes_match':True,'all_related_and_target_ids_resolve':True,
          'prior_files_modified':False,'root_targets_modified':False,'new_claim_ids':[],
          'Lean_kernel_replay_run':False,'formal_transitive_Lean_dependency_audit':False,
          'mathematical_scope':'Human semantic sufficient-condition audit. Byte and DAG checks prove provenance and graph bookkeeping, not the mathematical theorems.',
          'audit_txt_sha256':sha((HERE/'audit.txt').read_bytes()) if (HERE/'audit.txt').exists() else None})
    print(json.dumps({'targets':len(targets),'retirement_candidates':list(retirement),'source_files':len(blobs),'source_ranges':len(source_index),'preserved_nodes':len(baseline['nodes']),'map_nodes':len(m['nodes'])}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=WORK.parent/'lean-source')
    main(ap.parse_args().repo.resolve())
