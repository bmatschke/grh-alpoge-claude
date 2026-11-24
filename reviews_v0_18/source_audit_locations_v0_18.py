"""Read-only continuity and proof-file navigation checks for the v0.18 audit.

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

    aliases_name = 'reviews_v0_18/proof_location_aliases_v0_18.json'
    aliases = read_json(aliases_name)
    old_map_name = aliases['historical_filename_map']
    old_map = read_json(old_map_name)
    literal_aliases = aliases['literal_path_aliases']
    component_aliases = aliases.get('component_ledger_aliases', {})
    file_aliases = {k: v for k, v in old_map.items()
                    if isinstance(v, str) and k.endswith(('.tex', '.txt', '.md', '.json'))}
    old = read_json('history/version_0_17/provenance.json')
    assert len(old['claims']) == 747, ('unexpected predecessor claim count', len(old['claims']))
    prior_navigation = read_json('reviews_v0_17/source_verification_v0_17_audit.json')['proof_navigation_counts']
    old_ids = {c['id'] for c in old['claims']}
    now_claims = {c['id']: c for c in ledger['claims']}
    assert len(now_claims) == len(ledger['claims'])
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

    # Previous root files moved to their actual archive; all non-root files
    # remain at the previous relative locations, as checked by the old manifest.
    old_dir = artifact / 'history/version_0_17'
    archived_names = {p.name for p in old_dir.iterdir() if p.is_file()}
    assert len(archived_names) == 20, ('unexpected archived root-file count', len(archived_names))
    manifest = read_bytes('history/version_0_17/SHA256SUMS').decode('utf-8')
    preserved_file_count = 0
    for line in manifest.splitlines():
        expected, relative = line.split('  ', 1)
        name = ('history/version_0_17/' + relative
                if relative in archived_names else relative)
        assert digest(read_bytes(name)) == expected, ('prior package bytes changed', relative)
        preserved_file_count += 1
    assert preserved_file_count == 796, ('unexpected predecessor manifest entry count', preserved_file_count)
    old_targets = read_json('history/version_0_17/next_source_targets.json')
    current_targets = read_json('next_source_targets.json')
    assert (old_targets['global_branches_unchanged']
            == current_targets['global_branches_unchanged']), 'global branch records changed'

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
        if claim.get('introduced_in') == '0.18':
            proof_files = [r for r in resolved if r['role'].startswith('proof_location')
                           and r['resolved_path'].endswith('.tex')]
            assert proof_files and any(
                ('\\paragraph{' + cid + ':') in read_bytes(r['resolved_path']).decode('utf-8')
                for r in proof_files), ('new claim paragraph marker absent', cid)
            counts['new_claim_paragraph_markers_checked'] += 1
            proof_sha = (claim.get('proof_location', {}).get('sha256')
                         or claim.get('proof_paragraph_sha256'))
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
                assert claim.get('introduced_in') != '0.18', ('new anchor absent', cid, anchor)
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
        global_branch_records_preserved=True,
        proof_navigation_counts=dict(counts),
        archival_corpus_fallback_without_claim_id_text=absent_markers,
        historical_anchor_text_not_found=missing_legacy_anchors,
        exact_proof_pointer_not_inferred_for_legacy_fallbacks=True,
        navigation=navigation)
    return summary, snapshots
