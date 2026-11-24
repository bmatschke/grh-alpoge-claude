#!/usr/bin/env python3
"""Reproduce the byte bindings for the independent KX and YX proof reviews.

Mathematical judgments are the reviewer's recorded conclusions, not output of
the byte checker. This script does not build Lean or replay a kernel check.
"""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parent / 'lean-source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def proof_bytes(location):
    raw = (WORK / location['file']).read_bytes()
    if 'line_start' in location:
        return b''.join(raw.splitlines(keepends=True)[location['line_start'] - 1:location['line_end']])
    start = raw.index(location['start_marker'].encode())
    end = len(raw) if location['end_marker'] == 'EOF' else raw.index(location['end_marker'].encode(), start + 1)
    return raw[start:end]


def validate(component, stem):
    base = WORK / component
    metadata_raw = (base / 'provenance.json').read_bytes()
    data = json.loads(metadata_raw)
    main_hash = sha((base / 'main.tex').read_bytes())
    closure_raw = (base / 'closure.json').read_bytes()
    closure = json.loads(closure_raw)
    assert data['commit'] == PIN
    assert data['main_tex_sha256'] == main_hash
    assert closure['main_tex_sha256'] == main_hash
    assert closure['provenance_sha256'] == sha(metadata_raw)
    files = {}
    for item in data['source_files']:
        raw = (REPO / item['path']).read_bytes()
        assert sha(raw) == item['sha256'], item['path']
        pinned = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + item['path']])
        assert raw == pinned, item['path']
        files[item['path']] = raw
    ranges = []
    proofs = []
    for claim in data['claims']:
        location = claim['proof_location']
        assert sha(proof_bytes(location)) == location['sha256'], claim['id']
        proofs.append(dict(claim=claim['id'], **location))
        for item in claim['sources']:
            raw = files[item['path']]
            lines = raw.splitlines(keepends=True)
            piece = b''.join(lines[item['line_start'] - 1:item['line_end']])
            assert sha(piece) == item['range_sha256'], (claim['id'], item['declaration'])
            assert sha(raw) == item['sha256'], item['path']
            if 'first_line' in item:
                assert lines[item['line_start'] - 1].decode().rstrip('\n') == item['first_line']
            ranges.append(dict(claim=claim['id'], path=item['path'], declaration=item['declaration'],
                               line_start=item['line_start'], line_end=item['line_end'],
                               range_sha256=item['range_sha256']))
    external = []
    for item in data['external_claim_dependencies']:
        location = item['proof_location']
        assert sha(proof_bytes(location)) == location['sha256'], item['claim_id']
        external.append(dict(claim_id=item['claim_id'], proof_location=location))
    result = dict(
        schema='rh-independent-source-validation/1', artifact_version='0.29', reviewer='core_closure',
        component=component, status='PASS', commit=PIN,
        main_tex_sha256=main_hash, provenance_sha256=sha(metadata_raw), closure_sha256=sha(closure_raw),
        source_files_verified=len(files), source_ranges_verified=len(ranges),
        human_proof_ranges_verified=proofs, external_proof_ranges_verified=external, ranges=ranges,
        source_files=[dict(path=p, sha256=sha(b), matches_pinned_git_blob=True) for p, b in sorted(files.items())],
        scope='Exact source and human-proof bytes only. The mathematical judgment is separately recorded; no Lean build or kernel replay.')
    path = HERE / (stem + '_source_validation.json')
    dump(path, result)
    return data, result, path


KX_CHECKS = [
    'KX1: every O-algebra map between the exact IsCO objects is local because its composite with the fixed residue map is surjective onto k. This proves continuity rather than assuming it in an interface that quantifies over all algebra maps. The principal-unit exponent construction is valid at ell=2 and for zero variables.',
    'KX2: the quotient by closed normal inertia outside the prescribed S-prime preserves both the original CM quadratic character and the original cyclotomic character. The given finite-place unramifiedness and inclusion of all ell-adic places supply the two kernel containments. S-prime and the actual complex conjugation are unchanged.',
    'KX3: henselization/completion transports the actual decomposition group and inertia. Local reciprocity gives Z-hat times the unit group; deep logarithms and the structure theorem isolate the finite ell-primary torsion P and the free Z_ell^d part, including ell=2. The maps a and b have exactly the inertia image, primary-torsion restriction and finite-character factorization required by LocAb. The local-degree sum is exactly [F:Q].',
    'KX4: the prescribed th character descends through the closed commutator kernel to the finite torsion group P; its reduction is one. Combining it with the Teichmuller lift gives an actual IsPsi. Quotients of any other lift by this base character kill the whole inverse image of P. Testing finite maximal-ideal quotients and then using separatedness gives the claimed unique continuous factor through a.',
    'KX5: only the inertia coordinates enter the weight ring, so the number of variables is n times [F:Q], not n times the sum of d_v+1. Actual full-character extensions witness IsInert. Testing elements of inertia mapping to basis vectors proves uniqueness and independence of the chosen full extensions, including n=0.',
    'KX6: the explicit permutation-module cocycle gives an injection of continuous homomorphisms from every open subgroup into finite H1. Evaluating at the fixed coset shows that a coboundary identifies only equal homomorphisms. The global and local finite-cohomology fields of BX8 apply to these exact finite modules; the CM subgroup is open. Thus the full PhiAll interface is supplied without automorphy.',
    'KX7: the actual GDet law and coefficient continuity match Chenevier, including full base-change naturality and the source coefficients at indices greater than n. Propositions 3.3 and 3.7 under condition (F) have no residual-irreducibility or ell>n restriction. Completed base change from W(k) to the given finite coefficient DVR preserves the exact residue field and universal maps. The degree-zero branch is proved separately.',
    'KX8: the preliminary determinant/full-local-character coproduct has exactly the required universal property. Its quotient relations are the weak Pair.P, Pair.Ord and Pair.I equations with the actual star sign, ordered ordinary product, and tame subgroup. The corrected middle generator is tr_D([h] o_v). The actual nonempty pair makes the ideal proper; complete Noetherian quotients are closed and remain IsCO. This proves the full universal Pair object, without upgrading it to RingProps.',
    'KX9: restriction of the actual full local characters gives the unique weight-to-pair map, and uniqueness proves the commuting triangle for every subsequent pair and coefficient map. Universal isomorphisms return to any originally chosen universal objects. The five named existence predicates are fully supplied, while modular-support ideals and their arithmetic properties remain separate.'
]

YX_CHECKS = [
    'YX1: the exact Ctx2 datum includes Good and the original OfChar parameters (n_II,1,1). SX8 supplies the literal SeedIIAlt at the fixed iota, and UX12 supplies every original small KPair/Star promodular witness using the assumed uniform PMExAlt. The tower, coefficient witnesses and universal Space may vary later, but iota does not.',
    'YX1: the quantified witness is exactly IX.35 for this one original datum. IX9 gives the full characteristic-ell star obstruction, while IX10 gives PureW on all star pairs and IsAut4Alt on full-span pairs. IX8 then proves Fin0, NoEnd and AllIrr automorphy on the same datum. No case-III instance or full two-case ImageDense premise is inserted.',
    'YX2: CX9 provides C and A before any host, coefficient ring or representation. SP10 gives a character-dependent natural exponent before h,t,Omega,ell,c,e,psi. Its Case-II arithmetic specialization uses p1=1 and the exact unchanged n_II. This matches the quantifier order of CountShape and CountII.',
    'YX2: AX5 creates the actual Good/OfChar datum after the permitted root adjunction. AX6–AX9 give the original common level L=ell*2^n_II*N, character exponent k=(ell-1)*2^n_II*(2o), ordinary weights, dual and safety fields. Adding YX1 pointwise gives the complete AdmRAlt record at one iota; no stronger global hypothesis is silently assumed.',
    'YX2: DX2, DX4 and DX8 supply the actual MX10 model. RX6 is applied pointwise using YX1 automorphy, so PX10 receives exactly Fin0, NoEnd and AllIrr RigidAt on that same model. All source point, orbit and tangent comparisons used by SP10 are thereby installed in Case II.',
    'YX2: CX9 supplies trace separation for each actual representation and a single integral product valid for the finite pairwise nonisomorphic family selected by PX10. Its inequality has the direction needed for minus twice the ell-adic logarithm. The integer product gives minus log|N_*|_ell at most log|N_*|, and phi(k)<=k gives the displayed bound. The factor two and division by v_O(ell) are preserved.',
    'YX2: the original strict Selmer group injects into the auxiliary group because at every newly admitted unramified prime the negative-weight Frobenius scalar differs from one and acts surjectively on E/O. SP10 supplies the original-case arithmetic absorption. SP8 and RV1 return finite length and its exact normalized value to the initial coefficient DVR, preserving kernel, order, conductor, parity and n_II.',
    'YX2: the concluding height implication retains CountI, CountIII and CountV together with PMExAlt. HV5, HV6 and CZ6 supply only their already proved auxiliary counts; HV10 and the window suppliers retain the stated prime-pair hypotheses. Neither unconditional CountII nor unconditional PointHV, full ImageDense, case III or RH/GRH is claimed.'
]


def write_review(component, stem, checks, primary_sources, resolved, limitations):
    data, validation, vpath = validate(component, stem)
    base = WORK / component
    review = dict(
        schema='rh-independent-mathematical-review/1', artifact_version='0.29', reviewer='core_closure',
        component=component, result='PASS', claims_reviewed=[c['id'] for c in data['claims']],
        reviewed_main_sha256=validation['main_tex_sha256'],
        reviewed_metadata_sha256=validation['provenance_sha256'],
        reviewed_closure_sha256=validation['closure_sha256'], checks=checks,
        primary_sources_checked=primary_sources, resolved_findings=resolved, findings=[],
        unresolved_findings=[], limitations=limitations,
        source_validation_file=str(vpath.relative_to(WORK)), source_validation_sha256=sha(vpath.read_bytes()),
        no_lean_build_or_kernel_replay=True)
    path = HERE / (stem + '.json')
    dump(path, review)
    text = [f'Independent mathematical review — {component} — version 0.29',
            'Reviewer: core_closure', 'Result: PASS', '',
            'Claims reviewed: ' + ', '.join(review['claims_reviewed']),
            'Main SHA256: ' + review['reviewed_main_sha256'],
            'Provenance SHA256: ' + review['reviewed_metadata_sha256'],
            'Closure SHA256: ' + review['reviewed_closure_sha256'], '',
            'Mathematical and interface checks', '']
    text += [str(i) + '. ' + check for i, check in enumerate(checks, 1)]
    text += ['', 'Primary sources independently checked', '']
    text += [x['reference'] + '\n' + x['url'] + '\n' + x['scope'] for x in primary_sources]
    if not primary_sources:
        text += ['No new external theorem is invoked by this join; the exact incoming human claims were checked at their stated interfaces.']
    text += ['', 'Resolved findings', ''] + (resolved or ['None.'])
    text += ['', 'Review limits', ''] + limitations
    text += ['', f"Byte verification: {validation['source_ranges_verified']} source links on {validation['source_files_verified']} pinned files, "
             f"{len(validation['human_proof_ranges_verified'])} component proof ranges, "
             f"and {len(validation['external_proof_ranges_verified'])} incoming proof ranges all match.",
             'No unresolved finding. No Lean build or kernel replay.']
    (HERE / (stem + '.txt')).write_text('\n\n'.join(text) + '\n')
    print(json.dumps(dict(review=str(path.relative_to(WORK)), sha256=sha(path.read_bytes()),
                          main_sha256=review['reviewed_main_sha256'], result='PASS')))


write_review(
    'symplectic_universal_arithmetic', 'universal_arithmetic_core_review', KX_CHECKS,
    [dict(reference='Milne, Class Field Theory (v4.03), I.1.1, I.1.4 and I.1.8–1.11, printed pages 20–24.',
          url='https://www.jmilne.org/math/CourseNotes/CFT.pdf',
          scope='Local reciprocity, existence, profinite completion and units/inertia; independently opened and read. The local free/torsion decomposition is proved in KX3.'),
     dict(reference='Chenevier, The p-adic analytic space of pseudocharacters of a profinite group and pseudorepresentations over arbitrary rings, §3.1, Lemma 3.2, Propositions 3.3 and 3.7, Remark 3.5, printed pages 41–43.',
          url='https://maths.dur.ac.uk/events/Meetings/LMS/2011/GRAF11/papers/chenevier.pdf',
          scope='Primary paper independently retrieved through the institutional copy and compared with the locally retained version-2 text. Condition (F) is the exact finite-Hom predicate; the conditional alternative p>d is not imposed when (F) holds.')],
    ['The middle generator in KX.20 was changed from a two-argument-looking trace notation to the literal trace of [h] times the ordinary product.',
     'The Milne profinite-completion locator was refined to I.1.10–1.11. Subsequent alignment and line-break edits do not change the argument.'],
    ['This is an independent proof and exact-interface review of all KX1–KX9. BX8 is consumed as a previously reconstructed supplier; its entire proof is not re-reviewed here.',
     'The completed ordinary universal ring is not a modular-support ideal. RingProps, HidaPropsAlt and P1core are not supplied by this review.'])

write_review(
    'case_two_installation', 'case_two_installation_core_review', YX_CHECKS, [], [],
    ['This is an independent proof and exact-interface review of the two complete conditional joins YX1 and YX2. The incoming claims were checked at the used scopes; their full proofs and classical registries are not all independently reconstructed again in this review.',
     'PMExAlt remains an actual arithmetic premise. CountI, CountIII and CountV remain premises for the height consequence, and the previously stated prime-pair assumptions remain for its window consequences.'])
