"""Read-only continuity and proof-file navigation checks for the v0.21 audit.

This module deliberately distinguishes explicit stored proof-file references
from archival component-corpus fallbacks. It never changes the merged ledger.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def relative_path(value):
    rel = Path(value)
    assert not rel.is_absolute() and '..' not in rel.parts, ('unsafe artifact path', value)
    return rel


def audit_locations_and_continuity(artifact, ledger):
    artifact = Path(artifact)
    snapshots = {}

    def read_bytes(relative):
        rel = relative_path(relative)
        raw = (artifact / rel).read_bytes()
        key = rel.as_posix()
        if key in snapshots:
            assert snapshots[key] == raw, ('artifact changed during navigation audit', key)
        snapshots[key] = raw
        return raw

    def read_json(relative):
        return json.loads(read_bytes(relative))

    aliases_name = 'reviews_v0_21/proof_location_aliases_v0_21.json'
    aliases = read_json(aliases_name)
    old_map_name = aliases['historical_filename_map']
    old_map = read_json(old_map_name)
    literal_aliases = aliases['literal_path_aliases']
    component_aliases = aliases.get('component_ledger_aliases', {})
    file_aliases = {k: v for k, v in old_map.items()
                    if isinstance(v, str) and k.endswith(('.tex', '.txt', '.md', '.json'))}
    old = read_json('history/version_0_20/provenance.json')
    assert len(old['claims']) == 983, ('unexpected predecessor claim count', len(old['claims']))
    prior_navigation = read_json('reviews_v0_20/source_verification_v0_20_audit.json')['proof_navigation_counts']
    old_ids = {c['id'] for c in old['claims']}
    now_claims = {c['id']: c for c in ledger['claims']}
    assert len(now_claims) == len(ledger['claims'])
    expected_new = {f'{prefix}{i}' for prefix,n in [('NR',24),('CW',25),('GV',21),('CC',20)] for i in range(1,n+1)}
    assert len(expected_new) == 90 and len(now_claims) == 1073
    assert set(now_claims) - old_ids == expected_new and not expected_new & old_ids
    preserved_fields = 0
    for claim in old['claims']:
        current = now_claims[claim['id']]
        for key, value in claim.items():
            assert key in current and current[key] == value, ('prior claim field changed', claim['id'], key)
            preserved_fields += 1
    now_files = {f['path']: f for f in ledger['source_files']}
    for record in old['source_files']:
        assert now_files[record['path']] == record, ('prior source record changed', record['path'])
    graph = ledger['mathematical_dependency_graph']
    for cid, deps in old['mathematical_dependency_graph'].items():
        assert graph[cid] == deps, ('prior dependency adjacency changed', cid)
    conclusion_keys = []
    for key, value in old.items():
        if key.startswith('version_') and 'conclusion' in key:
            assert ledger[key] == value, ('prior conclusion object changed', key)
            conclusion_keys.append(key)
    order = ledger['dependency_topological_order']
    assert len(order) == len(set(order)) == len(now_claims)
    pos = {cid: i for i, cid in enumerate(order)}
    assert set(pos) == set(graph) == set(now_claims)
    for cid, deps in graph.items():
        for dep in deps:
            assert pos[dep] < pos[cid], ('invalid topological order', cid, dep)

    def ancestors(cid):
        seen = set()
        pending = list(graph[cid])
        while pending:
            item = pending.pop()
            if item not in seen:
                seen.add(item)
                pending.extend(graph[item])
        return seen

    assert not ancestors('TL13') & (
        {'FC19', 'VE9', 'VE10', 'VE11'} | {f'TG{i}' for i in range(1, 13)})
    assert not ancestors('SZ11') & {'PN16', 'SZ8', 'SZ9'}
    assert not ancestors('SZ13') & {'PN16', 'SZ8', 'SZ9', 'SZ11'}
    assert 'PA15' not in ancestors('TA10')
    assert 'PA15' not in ancestors('TA14')
    assert not ancestors('CI13') & {'TL13', 'TX7', 'TX16'}
    assert not ancestors('TX10') & {f'TX{i}' for i in range(11,17)}
    ca_ids = {cid for cid in graph if re.fullmatch(r'CA\d+', cid)}
    for cid in [f'VI{i}' for i in range(1, 11)]:
        assert not ancestors(cid) & ca_ids, ('primitive vacuum depends on CA join', cid)
    assert 'CA2' in ancestors('VI11')
    assert not ancestors('CA2') & {f'VI{i}' for i in range(1, 12)}
    assert not ancestors('VI11') & (ca_ids - {'CA1', 'CA2'})
    assert not ancestors('NC8') & {f'NC{i}' for i in range(9, 18)}
    assert 'NC13' not in ancestors('NC12')
    assert 'TX16' not in ancestors('NC16')
    assert not ancestors('SE11') & {'SE12', 'SE14'}
    assert 'SE14' not in ancestors('SE12')
    assert 'LS2' in graph['LS4'], 'actual xi norm dependency is not recorded'

    # v0.19 construction-before-join boundaries, independent of the old checks.
    tt_ids = {cid for cid in graph if re.fullmatch(r'TT\d+', cid)}
    assert not ancestors('HF13') & (tt_ids | {f'HF{i}' for i in range(14, 21)})
    assert not ancestors('HF16') & tt_ids
    assert not ancestors('TT8') & {'TT10', 'TT13', 'TT14', 'TT16', 'TT19'}
    assert 'HF16' in ancestors('TT11')
    assert not ancestors('TT13') & {'TT14', 'TT16', 'TT19'}
    assert 'TT16' not in ancestors('TT15')
    assert not ancestors('QW14') & {'QW11', 'QW12', 'QW13'}
    assert 'QW14' in ancestors('QW15')

    # v0.20 construction-before-join boundaries, keeping every old edge intact.
    ga_ids = {cid for cid in graph if re.fullmatch(r'GA\d+', cid)}
    wa_ids = {cid for cid in graph if re.fullmatch(r'WA\d+', cid)}
    mf_ids = {cid for cid in graph if re.fullmatch(r'MF\d+', cid)}
    qr_ids = {cid for cid in graph if re.fullmatch(r'QR\d+', cid)}
    assert not ancestors('GA6') & {f'GA{i}' for i in range(7, 24)}
    assert not ancestors('GA8') & {f'GA{i}' for i in range(13, 24)}
    assert 'RC4' in ancestors('GA8')
    assert not ancestors('WA3') & {f'WA{i}' for i in range(4, 20)}
    assert not ancestors('WA11') & {f'WA{i}' for i in range(12, 20)}
    assert not ancestors('WA15') & {'WA16','WA17','WA18','WA19'}
    assert not ancestors('MF4') & {f'MF{i}' for i in range(5, 21)}
    assert not ancestors('MF9') & {f'MF{i}' for i in range(10, 21)}
    assert not ancestors('MF16') & {'MF17','MF18','MF19','MF20'}
    assert not ancestors('MF19') & {'QW3','QW9','MF20'}
    for cid in mf_ids:
        assert not ancestors(cid) & (ga_ids | wa_ids | qr_ids), ('mass supplier depends on a later companion',cid)
    assert not ancestors('QR9') & {f'QR{i}' for i in range(10, 26)}
    assert not ancestors('QR13') & {f'QR{i}' for i in range(14, 26)}
    assert {'QR9','QR24'} <= ancestors('QR25')

    # v0.21 supplier boundaries: these are actual dependencies, not target-map links.
    nr_ids = {f'NR{i}' for i in range(1, 25)}
    cw_ids = {f'CW{i}' for i in range(1, 26)}
    gv_ids = {f'GV{i}' for i in range(1, 22)}
    cc_ids = {f'CC{i}' for i in range(1, 21)}
    for cid in nr_ids:
        assert not ancestors(cid) & (cw_ids | gv_ids | cc_ids), cid
        assert not ancestors(cid) & ({'SE14', 'LS21', 'LS22'} | {f'NC{i}' for i in range(1, 18)}), cid
    for i in [3, 7, 11, 12, 15, 18]:
        assert not ancestors(f'NR{i}') & {f'NR{j}' for j in range(i + 1, 25)}, i
    assert {'NR5', 'NR6', 'LS8'} <= ancestors('NR7')
    assert {'HF13', 'HF16', 'GA16'} <= ancestors('NR13')
    assert {'NR7', 'NR11', 'NR13'} <= ancestors('NR15')
    assert {'NR15', 'NR16', 'NR17'} <= ancestors('NR18')
    assert not ancestors('NR20') & {'NR15', 'NR18', 'NR21', 'NR24'}
    assert not ancestors('NR21') & {'NR22', 'NR23', 'NR24'}
    assert not ancestors('NR2') & (nr_ids - {'NR1', 'NR2'})
    assert not ancestors('NR7') & {f'NR{i}' for i in range(8, 25)}
    assert not ancestors('NR11') & {f'NR{i}' for i in range(12, 25)}
    assert not ancestors('NR13') & {'NR14', 'NR15', 'NR17', 'NR18', 'NR24'}
    assert not ancestors('NR20') & {'NR21', 'NR22', 'NR23', 'NR24'}
    assert not ancestors('NR23') & {'NR22', 'NR24'}
    assert {'NR15', 'NR18', 'NR21', 'NR22', 'NR23'} <= ancestors('NR24')
    for cid in [f'CW{i}' for i in range(1, 14)]:
        assert not ancestors(cid) & {f'CW{i}' for i in range(14, 26)}, cid
    assert not ancestors('CW18') & {'CW23', 'CW24', 'CW25'}
    assert not ancestors('CW20') & {'CW19', 'CW21', 'CW22', 'CW23', 'CW24', 'CW25'}
    assert 'CW20' in ancestors('CW19')
    assert 'CW23' not in ancestors('CW24')
    assert {'CW24', 'WA16', 'WA17'} <= ancestors('CW25')
    assert not ancestors('GV11') & {'GV9', 'GV10', 'GV13', 'GV15', 'GV16', 'GV19', 'GV21'}
    assert not ancestors('GV14') & {'GV10', 'GV13', 'GV15', 'GV21'}
    assert {'GV10', 'GV11'} <= ancestors('GV13')
    assert {'IG12', 'GV16'} <= ancestors('GV19')
    assert {'HF20', 'GV13', 'GV19', 'GV20'} <= ancestors('GV21')
    for cid in gv_ids:
        assert not ancestors(cid) & (nr_ids | cw_ids | cc_ids), cid
    for cid in [f'CC{i}' for i in range(1, 9)]:
        assert not ancestors(cid) & {f'CC{i}' for i in range(9, 21)}, cid
    assert not ancestors('CC15') & (cc_ids - {'CC15'})
    assert not ancestors('CC17') & (cc_ids - {'CC17'})
    assert not ancestors('CC18') & {'CC19', 'HC9'}
    assert 'HC9' not in ancestors('CC19')
    assert {'CC14', 'CC16', 'CC17', 'CC18'} <= ancestors('CC19')

    # Previous root files moved to their actual archive; all non-root files
    # remain at the previous relative locations, as checked by the old manifest.
    old_dir = artifact / 'history/version_0_20'
    archived_names = {p.name for p in old_dir.iterdir() if p.is_file()}
    assert len(archived_names) == 19, ('unexpected archived root-file count', len(archived_names))
    manifest_raw = read_bytes('history/version_0_20/SHA256SUMS')
    assert digest(manifest_raw) == '9aa87d046384be2e6bc45ec00e695b8e95b726e4b850f009b987f39ae1df06be'
    manifest = manifest_raw.decode('utf-8')
    preserved_file_count = 0
    for line in manifest.splitlines():
        expected, relative = line.split('  ', 1)
        name = ('history/version_0_20/' + relative
                if relative in archived_names else relative)
        assert digest(read_bytes(name)) == expected, ('prior package bytes changed', relative)
        preserved_file_count += 1
    assert preserved_file_count == 996, ('unexpected predecessor manifest entry count', preserved_file_count)
    old_targets = read_json('history/version_0_20/next_source_targets.json')
    current_targets = read_json('next_source_targets.json')
    assert (old_targets['global_branches_unchanged']
            == current_targets['global_branches_unchanged']), 'global branch records changed'

    # Preserve a frozen snapshot of all new authored component evidence too.
    for component in ['nonempty_realization', 'canonical_weil',
                      'geometric_volumes', 'centered_character_sums']:
        for name in ['main.tex', 'report.txt', 'provenance.json',
                     'source_manifest.json', 'source_locators.txt',
                     'build_provenance.py', 'next_targets.json']:
            read_bytes(component + '/' + name)

    component_cache = {}
    navigation = []
    counts = Counter()
    legacy_counts = Counter()
    absent_markers = []
    missing_legacy_anchors = []

    def contains_claim_record(value, cid):
        if isinstance(value, dict):
            if value.get('id') == cid or value.get('claim_id') == cid:
                return True
            return any(contains_claim_record(v, cid) for v in value.values())
        if isinstance(value, list):
            return any(contains_claim_record(v, cid) for v in value)
        return False

    def stored_paths(value, context='proof_location'):
        if isinstance(value, str):
            yield context, value
        elif isinstance(value, dict):
            for key in ['file', 'expanded', 'also', 'earlier_reduction']:
                if key in value:
                    yield from stored_paths(value[key], context + '.' + key)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                yield from stored_paths(item, context + '[' + str(index) + ']')

    def resolve_literal(value, component):
        mapped = literal_aliases.get(value, [file_aliases.get(value, value)])
        output = []
        for name in mapped:
            rel = relative_path(name)
            candidates = [rel, Path(component).parent / rel]
            found = list(dict.fromkeys(p.as_posix() for p in candidates
                                      if (artifact / p).is_file()))
            assert found, ('unresolved explicit proof path', component, value)
            assert len(found) == 1, ('ambiguous explicit proof path', component, value, found)
            output.append(found[0])
        return output

    for claim in ledger['claims']:
        prior_counts = counts.copy()
        cid = claim['id']
        component = claim['component_ledger']
        component_resolved = component_aliases.get(component, component)
        if component not in component_cache:
            component_cache[component] = read_json(component_resolved)
        if component_resolved != component:
            counts['historical_component_ledger_alias_claims'] += 1
        assert contains_claim_record(component_cache[component], cid), (
            'claim absent from preserved component evidence', cid, component)
        refs = list(stored_paths(claim.get('proof_location')))
        refs += list(stored_paths(claim.get('expanded_notes'), 'expanded_notes'))
        resolved = []
        fallback = not refs
        if fallback:
            assert component in aliases['component_corpus_fallbacks'], (
                'legacy claim lacks explicit corpus evidence', cid, component)
            for name in aliases['component_corpus_fallbacks'][component]:
                resolved.append(dict(role='archival_component_corpus',
                                     recorded_path=None, resolved_path=name))
            counts['archival_corpus_fallback_claims'] += 1
        else:
            counts['claims_with_explicit_file_references'] += 1
            for role, value in refs:
                for name in resolve_literal(value, component):
                    resolved.append(dict(role=role, recorded_path=value, resolved_path=name))
                    counts['explicit_path_references_resolved'] += 1
                    if value in literal_aliases:
                        counts['literal_alias_path_expansions'] += 1
        occurrence_paths = []
        for record in resolved:
            raw = read_bytes(record['resolved_path'])
            text = raw.decode('utf-8')
            record['sha256'] = digest(raw)
            record['claim_id_text_occurs'] = bool(
                re.search(r'(?<![A-Za-z0-9])' + re.escape(cid) + r'(?![A-Za-z0-9])', text))
            if record['claim_id_text_occurs']:
                occurrence_paths.append(record['resolved_path'])
        if fallback:
            if occurrence_paths:
                counts['archival_corpus_with_claim_id_occurrence'] += 1
            else:
                counts['archival_corpus_without_claim_id_occurrence'] += 1
                absent_markers.append(cid)
        if claim.get('introduced_in') == '0.21':
            proof_files = [r for r in resolved if r['role'].startswith('proof_location')
                           and r['resolved_path'].endswith('.tex')]
            assert proof_files and any(
                ('\\paragraph{' + cid + ':') in read_bytes(r['resolved_path']).decode('utf-8')
                for r in proof_files), ('new claim paragraph marker absent', cid)
            counts['new_claim_paragraph_markers_checked'] += 1
            location = claim.get('proof_location', {})
            proof_shas = [value for value in [location.get('sha256'),
                          location.get('paragraph_sha256'),
                          claim.get('proof_paragraph_sha256')] if value]
            assert proof_shas, ('new claim has no proof paragraph hash', cid)
            assert len(set(proof_shas)) == 1, ('new proof hash aliases differ', cid, proof_shas)
            proof_sha = proof_shas[0]
            if proof_sha:
                matching = []
                for record in proof_files:
                    raw = read_bytes(record['resolved_path'])
                    marker = ('\\paragraph{' + cid + ':').encode()
                    if marker not in raw:
                        continue
                    start = raw.index(marker)
                    following = re.search(rb'(?m)^\\paragraph\{[A-Z]+\d+:',
                                          raw[start + len(marker):])
                    stop = (start + len(marker) + following.start()
                            if following else len(raw))
                    matching.append(digest(raw[start:stop]))
                assert proof_sha in matching, ('new proof paragraph hash mismatch', cid, proof_sha, matching)
                counts['new_claim_paragraph_sha256_checked'] += 1
                if 'line_start' in location and 'line_end' in location:
                    candidate = next(r for r in proof_files
                                     if ('\\paragraph{' + cid + ':').encode()
                                     in read_bytes(r['resolved_path']))
                    raw_lines = read_bytes(candidate['resolved_path']).splitlines(keepends=True)
                    first, last = location['line_start'], location['line_end']
                    assert type(first) is int and type(last) is int and 1 <= first <= last <= len(raw_lines)
                    raw_range = b''.join(raw_lines[first-1:last])
                    assert digest(raw_range) == proof_sha, ('new proof line range hash mismatch', cid)
                    if 'bytes' in location:
                        assert len(raw_range) == location['bytes'], ('new proof byte count mismatch', cid)
                    counts['new_claim_proof_line_ranges_checked'] += 1
        explicit = claim.get('proof_location', {})
        anchors = explicit.get('anchors', []) if isinstance(explicit, dict) else []
        tex = '\n'.join(read_bytes(r['resolved_path']).decode('utf-8')
                        for r in resolved if r['resolved_path'].endswith('.tex'))
        anchor_checks = []
        for anchor in anchors:
            found = anchor in tex
            anchor_checks.append(dict(anchor=anchor, textual_occurrence=found))
            counts['recorded_anchor_text_checks'] += 1
            if not found:
                missing_legacy_anchors.append(dict(claim=cid, anchor=anchor))
                assert claim.get('introduced_in') != '0.21', ('new anchor absent', cid, anchor)
        navigation.append(dict(
            claim=cid, component_ledger=component,
            component_ledger_resolved_path=component_resolved,
            component_sha256=digest(read_bytes(component_resolved)),
            explicit_recorded_file_reference=not fallback,
            resolution_kind=('archival_component_corpus_only' if fallback
                             else 'explicit_stored_file_reference'),
            files=resolved, claim_id_occurrence_paths=occurrence_paths,
            anchor_text_checks=anchor_checks,
            claim_specific_proof_pointer_asserted=False if fallback else None))
        if cid in old_ids:
            legacy_counts.update(counts - prior_counts)
    legacy_keys = ['historical_component_ledger_alias_claims', 'archival_corpus_fallback_claims',
      'archival_corpus_with_claim_id_occurrence', 'claims_with_explicit_file_references',
      'explicit_path_references_resolved', 'recorded_anchor_text_checks',
      'literal_alias_path_expansions', 'archival_corpus_without_claim_id_occurrence']
    for key in legacy_keys:
        assert legacy_counts[key] == prior_navigation[key], ('legacy navigation count changed', key, legacy_counts[key], prior_navigation[key])
    assert absent_markers == ['GF3'], ('legacy corpus fallback changed', absent_markers)
    assert {(x['claim'], x['anchor']) for x in missing_legacy_anchors} == {('WT8','WT8'),('PG4','PG4'),('PG10','PG10'),('FG3','FG3'),('OR4','OR4')}
    for field in ['new_claim_paragraph_markers_checked','new_claim_paragraph_sha256_checked','new_claim_proof_line_ranges_checked']:
        assert counts[field] == 90, (field, counts[field])
    summary = dict(
        old_claims_preserved=len(old['claims']), old_claim_fields_preserved=preserved_fields,
        old_source_file_records_preserved=len(old['source_files']),
        old_dependency_adjacencies_preserved=len(old['mathematical_dependency_graph']),
        old_conclusion_objects_preserved=conclusion_keys,
        predecessor_manifest_files_verified=preserved_file_count,
        predecessor_package_files_verified=preserved_file_count + 1,
        archived_predecessor_root_files=len(archived_names),
        legacy_navigation_counts={key:legacy_counts[key] for key in legacy_keys},
        predecessor_manifest_itself_verified_present=True,
        component_ledgers_checked=len(component_cache),
        mathematical_dependency_graph_acyclic=True,
        cycle_boundaries_TL13_SZ11_SZ13_TA10_TA14_CI13_TX10_VI_CA_NC_SE_checked=True,
        v0_19_HF_TT_QW_construction_before_join_boundaries_checked=True,
        v0_20_GA_WA_MF_QR_construction_before_join_boundaries_checked=True,
        v0_21_NR_CW_GV_CC_construction_before_join_boundaries_checked=True,
        exact_new_claim_set_and_ninety_paragraph_ranges_checked=True,
        predecessor_manifest_fixed_sha256_verified=True,
        global_branch_records_preserved=True,
        proof_navigation_counts=dict(counts),
        archival_corpus_fallback_without_claim_id_text=absent_markers,
        historical_anchor_text_not_found=missing_legacy_anchors,
        exact_proof_pointer_not_inferred_for_legacy_fallbacks=True,
        navigation=navigation)
    return summary, snapshots
