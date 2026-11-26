#!/usr/bin/env python3
"""Bind the independent mathematical review to the exact reviewed PGR bytes.

The mathematical judgments below were made by geometry_alltest by reading the
human proof and the pinned original contracts and producer bodies.  Running
this script rechecks those judgments' byte bindings; it does not replay Lean
or replace the mathematical review.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = Path('/workspace/scratch/249d32c24541/formal_source')
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
# Final corrections were independently reread before this binding was set.
REVIEWED_MAIN_SHA = '8d6d48631a02e3784d9e9db686c49f6fefe80bcc582d94146ecf1a5a8d6cc94e'
REVIEWER = '/root/geometry_alltest'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def exact_range(data, first, last):
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    return b''.join(lines[first - 1:last])


REASONS = {
    1: 'The supplied finite character is used throughout. Clearing finite-adelic denominators proves unit modulus without an added continuity assumption. Rational trace integrality and Chinese remaindering prove the full inverse-different annihilator, including ramified places; finite generation extends it to the completed ideal.',
    2: 'The explicit hyperbolic projection gives the rational Levi factor over the original field and after scalar extension. The upper-flag equations imply the required additive character coordinate and its Levi invariance. The supplied rational character identity cancels the actual infinite and finite factors, including isotropic rank zero.',
    3: 'RCV12 supplies actual level membership and its stronger bw congruence. The human proof then supplies the missing phase: the rational character coordinate lies in the completed inverse different, the e/z and bw parts agree modulo g above the two level primes, and g is a unit elsewhere. PGR1 yields exactly the original chi2 equality.',
    4: 'The fractional-ideal lattice splitting makes the orthogonal projection integral. Applying it to nh and then to the inverse gives preservation by both h and h inverse, so n is integral as well. The smaller-level factorization follows on the same lattice and with the same xu, not after replacing the level.',
    5: 'A rational column stabilizer preserves the actual full lattice. Its positive-definite complement has a finite integral isometry group, hence the stabilizer has finite order. Unipotent reduction at a residue characteristic forces that order to be a power of that prime; the two distinct auxiliary primes force the element to be one. No prime-versus-rank bound or arithmetic gap is used.',
    6: 'The original Cols covariance forces the displayed reconstruction formula. Trivial column stabilizers give uniqueness of both rational and compact factors; every list of linear functionals therefore occurs. Riesz representation is conjugate-linear, and the reversed order in colCore is retained exactly.',
    7: 'Integral Levi extraction and the finite character identity establish independence of every finite decomposition. Rational covariance uses the exact finite/infinite product. Countable right-level cosets and continuity of the wave function give measurability; continuous linear evaluation commutes with the supplied Bochner reproducing identity.',
    8: 'Finite exponential and logarithm for the characteristic-zero unipotent group reduce finite-adelic density to additive approximation in a finite-dimensional rational vector space. The integral-lattice dictionary makes each original column unipotent discrete at infinity. The countable neighborhood construction gives strict measurable domains for precisely that subgroup.',
    9: 'A rational linear map preserves the lattice exactly when it preserves its completions. The actual level-membership theorem identifies this group with NOcol, and rational injectivity makes the lift unique. The finite character is the inverse of the infinite character, with no finite-index replacement.',
    10: 'Coverage uses the supplied Levi column classes and unipotent density; uniqueness uses integral Levi extraction and the full NeatKu result. Countable intersection partitions compare the original quotient with every strict column domain. Product integration contributes exactly one finite-level volume, with no hidden stabilizer mass.',
    11: 'The generic Tonelli argument needs only the original topological-group and Haar hypotheses. The unique expression gamma=delta inverse times s gives the exact multiplicity bound. The corrected statement accepts null-measurable a.e. fundamental domains and explicitly transports the proof through measurable representatives. Hausdorffness is used only for the compact finiteness and Borel refinement.',
    12: 'The averaging inequality proves the mixed absolute integral bound before any complex unfolding. It yields the exact a*A*J and a*J squared estimates, pointwise convergence, representative independence, and the original L2 statement. Nonnegative unfolding and then domination justify all complex sums. Inversion of the second coset index gives the correct S intersection rS-prime r-inverse stabilizer and arbitrary a.e. domains.',
    13: 'The nonnegative absolute quotient integral is finite before the slab change of variables. Applying the every-section cell formula and dividing only by the positive finite level volume proves SlabAbs for every strict column section. The actual InHH fields identify the original quotient L2 inner product, with precisely one volK2 factor.',
    14: 'The return identity supplies both lattice transport directions. Transport of the original row data proves IsLift and every local/primitivity and different-weighted FrameOK field. Chinese remaindering produces one integral upper-unitriangular matrix for all required primes. The conclusion is the original localized ModG condition, and active terms are exactly the original double quotient without a Gram-nondegeneracy restriction.',
    15: 'Inverting the original Poincare index and removing rational Levi and unipotent support factors gives the literal return set. Trivial Levi stabilizers reduce the remaining equivalence exactly to the original right column-unipotent quotient. The chi(k) inverse factor and right-unipotent wave covariance cancel, and absolute convergence justifies both the scalar and norm reindexings.',
    16: 'The return double quotient gives the exact orbit set and rational stabilizer. The checked covariance f_(nr)(x)=f_r(n inverse x) has the correct infinite/finite phase orientation. Countable tiling first proves equality of absolute integrals, then the complex identity for every prescribed strict orbital domain. The full original AmpWellDef and OOFundIndep premises remain supplied.',
    17: 'The Bochner rank-one operator is the literal OOt. Evaluation in the conjugate-linear first inner-product slot conjugates chi and produces precisely the scalar term phase. Absolute scalar unfolding is established independently of operator convergence. Finite-dimensional norm comparison transfers the first full AbsConvT clause to aTerm and every block, including zero-dimensional cases.',
    18: 'The complete original universal KExpansionC is obtained on arbitrary supplied D, X, Full, and ordered word pair with exactly the two FoldOK, two InHH, four orbital, and full AbsConvT premises. The original rows, sections, measures, characters, and representatives persist. The HasSum and every-vector sesquilinear identity follow, without a gap or positivity condition on c0.',
    19: 'PuLinear is proved under only its original InHH premise. The period map is continuous from the finite-dimensional original ColT into the ambient complete quotient L2 space. Two antilinear Riesz maps give the exact complex-linear Gram transport. Total inverse and square-root rules handle zero normalizers, and arbitrary target projections retain the full correction term.',
    20: 'The original FinX and both DimTie identities identify the actual sOf normalizers and adjoints. Conjugation by the two antilinear coordinates is a real-linear continuous norm isometry on operator spaces, which is sufficient to transport HasSum. The literal finite toTerm fibers and absolute norm series give both KExpansion and KAbsConv; no FinX existence, SIso, or new period-range identification is inferred.',
}


def main():
    manuscript = (HERE / 'main.tex').read_bytes()
    assert sha(manuscript) == REVIEWED_MAIN_SHA, 'Manuscript differs from the independently reviewed bytes'
    provenance = read_json(HERE / 'provenance.json')
    manifest = read_json(HERE / 'source_manifest.json')
    inherited = read_json(HERE / 'inherited_inputs.json')
    assert provenance['source_commit'] == manifest['source_commit'] == PIN
    assert provenance['proof_file_sha256'] == REVIEWED_MAIN_SHA
    assert len(provenance['claims']) == 20
    assert len(re.findall(rb'^% BEGIN PGR[0-9]+$', manuscript, re.M)) == 20

    blobs = {}
    files = []
    for row in manifest['source_files']:
        path = row['path']
        blob = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
        assert blob == (REPO / path).read_bytes() == (WORK / row['snapshot_path']).read_bytes(), path
        assert sha(blob) == row['sha256'] and len(blob) == row['bytes'], path
        blobs[path] = blob
        files.append({
            'path': path, 'snapshot_file': row['snapshot_path'],
            'sha256': sha(blob), 'bytes': len(blob), 'source_commit': PIN,
            'verified_equal_to_pinned_git_blob': True,
            'independently_verified_against_pinned_git_blob': True,
            'snapshot_and_checkout_equal': True, 'result': 'PASS',
        })
    assert len(files) == manifest['total_files'] == 39

    unique_ranges = {}
    claims = []
    proof_hashes = {}
    for claim in provenance['claims']:
        cid = claim['id']
        number = int(cid.removeprefix('PGR'))
        loc = claim['proof_location']
        block = exact_range(manuscript, loc['line_start'], loc['line_end'])
        assert block.startswith(('% BEGIN ' + cid + '\n').encode())
        assert block.rstrip().endswith(('% END ' + cid).encode())
        assert sha(block) == loc['sha256'] and len(block) == loc['bytes'], cid
        proof_hashes[cid] = sha(block)
        bound_sources = []
        for source in claim['sources']:
            path, start, end = source['path'], source['line_start'], source['line_end']
            data = exact_range(blobs[path], start, end)
            assert sha(data) == source['range_sha256'], (cid, source['id'])
            assert sha(blobs[path]) == source['file_sha256'] and len(data) == source['range_bytes']
            verified = dict(source)
            verified.update({'result': 'PASS', 'independently_verified_against_pinned_git_blob': True})
            bound_sources.append(verified)
            key = (path, start, end)
            if key in unique_ranges:
                assert unique_ranges[key]['range_sha256'] == verified['range_sha256']
            else:
                unique_ranges[key] = verified
        claims.append({
            'id': cid, 'claim': cid, 'title': claim['title'],
            'status': 'PASS', 'verdict': 'PASS', 'reviewer': REVIEWER,
            'source_commit': PIN, 'proof_file_sha256': REVIEWED_MAIN_SHA,
            'proof_location': loc, 'proof_range_sha256': sha(block),
            'range_sha256': sha(block), 'proof_sha256': sha(block),
            'source_ranges': bound_sources, 'reasoning': REASONS[number],
        })
    ranges = [unique_ranges[k] for k in sorted(unique_ranges)]
    assert len(ranges) == manifest['distinct_source_ranges'] == 84

    inherited_rows = []
    for component in inherited['components']:
        data = (WORK / component['file']).read_bytes()
        assert sha(data) == component['sha256']
        origin_path = WORK / component['component'] / 'provenance.json'
        origin = read_json(origin_path)
        origin_claims = {c['id']: c for c in origin['claims']}
        for binding in component['claim_bindings']:
            cid = binding['id']
            block = exact_range(data, binding['line_start'], binding['line_end'])
            assert sha(block) == binding['sha256'] == component['proof_hashes'][cid]
            assert sha(block) == origin_claims[cid]['proof_location']['sha256']
            assert len(block) == binding['bytes']
            assert block.startswith(('% BEGIN ' + cid + '\n').encode())
            assert block.rstrip().endswith(('% END ' + cid).encode())
            inherited_rows.append({
                'id': cid, 'proof_file': component['file'],
                'proof_file_sha256': sha(data),
                'proof_location': {k: binding[k] for k in ['file', 'line_start', 'line_end', 'sha256', 'bytes']},
                'proof_block_sha256': sha(block), 'range_sha256': sha(block),
                'parent_provenance_file': str(origin_path.relative_to(WORK)),
                'parent_provenance_sha256': sha(origin_path.read_bytes()),
                'scope': binding['scope'], 'status': 'PASS', 'result': 'PASS',
            })
    assert len(inherited_rows) == 4

    supporting = []
    support_manifest = read_json(HERE / 'supporting_sources.json')
    assert support_manifest['proof_file_sha256'] == REVIEWED_MAIN_SHA
    original_lake_bytes = subprocess.check_output(
        ['git', '-C', str(REPO), 'show', PIN + ':lake-manifest.json'])
    original_lake = json.loads(original_lake_bytes)
    mathlib_pin = next(x['rev'] for x in original_lake['packages'] if x['name'] == 'mathlib')
    assert mathlib_pin == '0df444a360eaa60ab8c11dca51a86af692955474'
    for source in support_manifest['sources']:
        assert source['source_commit'] == mathlib_pin
        raw_url = ('https://raw.githubusercontent.com/leanprover-community/mathlib4/'
                   + mathlib_pin + '/' + source['path'])
        primary_bytes = urlopen(raw_url, timeout=45).read()
        snapshot_bytes = (WORK / source['snapshot_path']).read_bytes()
        assert primary_bytes == snapshot_bytes
        assert sha(snapshot_bytes) == source['sha256'] == 'c5dbbd2d01d3f65dcfdb89b877268d836a162e5f0d0d0967d527ce5ec2473e67'
        assert len(snapshot_bytes) == source['bytes']
        part = exact_range(snapshot_bytes, source['line_start'], source['line_end'])
        assert sha(part) == source['range_sha256'] == '67d0300ca682660621e1b7aa64e1c1fdd19fefd1fa7220de5568f6336489e3a7'
        assert len(part) == source['range_bytes']
        supporting.append(dict(source, result='PASS', raw_url=raw_url,
                               independently_compared_to_pinned_primary_bytes=True,
                               original_lake_manifest_sha256=sha(original_lake_bytes),
                               original_lake_manifest_source_commit=PIN))
    assert len(supporting) == 1

    resolved = [
        {
            'id': 'PGR_REVIEW_1', 'claim': 'PGR11',
            'severity': 'original_scope_correction', 'status': 'resolved',
            'finding': 'The initial generic FoldBound statement imposed Hausdorffness, although the original FoldBound does not.',
            'resolution': 'The author removed Hausdorffness from the Tonelli folding inequality and kept it only in the compact-finiteness/Borel refinement. PGR12 explicitly uses the compact Hausdorff case.',
            'source_path': 'src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/FoldBound.lean',
            'source_lines': [24, 34],
        },
        {
            'id': 'PGR_REVIEW_2', 'claims': ['PGR10', 'PGR11', 'PGR12'],
            'severity': 'original_scope_correction', 'status': 'resolved',
            'finding': 'The initial human statement called every quotient domain measurable, whereas the original IsFundamentalDomain permits null-measurable domains with a.e. coverage and disjointness.',
            'resolution': 'The corrected statement includes the original a.e. domains and the proof replaces them by measurable representatives, removes the countable union of translated null exceptional sets, and uses unchanged restricted integrals. PGR10 explicitly uses the same convention. Strict IsSFund statements elsewhere remain strict.',
            'supporting_source_commit': '0df444a360eaa60ab8c11dca51a86af692955474',
            'supporting_source_path': 'Mathlib/MeasureTheory/Group/FundamentalDomain.lean',
            'supporting_source_lines': [65, 73],
        },
        {
            'id': 'PGR_REVIEW_3', 'claim': 'PGR20',
            'severity': 'notation_clarification', 'status': 'resolved',
            'finding': 'Root independently noted that the operator transport and the orbital term index set both used the same symbol.',
            'resolution': 'The author retained mathcal T for operator transport and changed the term index set to mathfrak T; the formulas now distinguish both objects.',
        },
        {
            'id': 'PGR_REVIEW_4', 'claim': 'PGR17',
            'severity': 'source_range_precision', 'status': 'resolved',
            'finding': 'The source range described as covering scl/blk originally began after those definitions.',
            'resolution': 'The bound range now includes the actual scl, blk, aTermL, aTerm and Hilbert-Schmidt encoding definitions. The mathematical formula needed no change.',
        },
    ]
    for finding in resolved:
        finding['reviewed_final_proof_file_sha256'] = REVIEWED_MAIN_SHA

    result = {
        'schema': 'rh-independent-mathematical-review/1',
        'artifact_version': '0.57', 'date': '2026-11-24',
        'component': HERE.name, 'reviewer': REVIEWER,
        'reviewer_name': 'geometry_alltest', 'independent_of_author': True,
        'status': 'PASS', 'verdict': 'PASS', 'source_commit': PIN,
        'proof_file': str((HERE / 'main.tex').relative_to(WORK)),
        'proof_file_sha256': REVIEWED_MAIN_SHA, 'main_tex_sha256': REVIEWED_MAIN_SHA,
        'proof_hashes': proof_hashes, 'claims': claims, 'claims_reviewed': claims,
        'source_verification': files, 'source_range_verification': ranges,
        'inherited_verification': inherited_rows,
        'supporting_source_verification': supporting,
        'source_files_checked': len(files), 'source_ranges_checked': len(ranges),
        'inherited_inputs_checked': len(inherited_rows),
        'review_scope': 'All twenty detailed human proofs, exact original universal KExpansionC and KTie scopes, every named premise and common-data choice; source and inherited-proof bytes independently verified.',
        'resolved_findings': resolved, 'corrections_resolved': resolved,
        'unresolved_findings': [], 'findings': [],
        'whole_selected_obligations_closed': [], 'whole_obligations_closed': [],
        'limitations': 'KExpansionC is the full original conditional theorem. FullExists, Forms0, the independent global FoldOK/InHH/orbital/AbsConv producers, FinX existence, SIso and the later coherent period-range/global spectral join are not supplied by this packet. KTie retains arbitrary original FinX and both DimTie identities.',
        'formal_verification': 'The accepted formal proof is used to identify original statements and data; the human arguments were reviewed independently.',
        'lean_replay': False,
    }
    (HERE / 'independent_review.json').write_text(json.dumps(result, indent=2) + '\n')

    paragraphs = [
        '# Independent mathematical review: PGR1–PGR20',
        '',
        '**Verdict: PASS.** All twenty human proofs have been read against the pinned original contracts and relevant producer bodies. No unresolved mathematical or quantifier defect remains after the corrections below.',
        '',
        '- Reviewer: `/root/geometry_alltest`, independent of the author.',
        '- Original source commit: `' + PIN + '`.',
        '- Reviewed manuscript SHA256: `' + REVIEWED_MAIN_SHA + '`.',
        '- Exact byte checks: 20 proof blocks, 39 original-repository snapshots and pinned Git blobs, 84 distinct original-source ranges, and four inherited proof blocks.',
        '- Formal correctness is accepted. No Lean replay was performed.',
        '',
        '## Main mathematical conclusions',
        '',
        'The packet proves the full original universal `KExpansionC` implication. It keeps an arbitrary original `D`, supplied `HidaSetting X`, `Full X`, both words, both `FoldOK` and `InHH` premises, all four orbital premises, and full `AbsConvT`. Its conclusion is the literal operator `HasSum` and the original every-column-vector sesquilinear identity. It also proves the full original `KTie` implication on the supplied `FinX`, with both original `DimTie` identities and the actual finite fibers of `toTerm`.',
        '',
        'The strongest mathematical checks were the finite inverse-different phase, the two-prime trivial-stabilizer argument, the exact full `PD` return carrier, and the analytic order of operations. The proof obtains an absolute mixed integral from folding before any complex unfolding. It derives absolute slab integrability for every strict column section before orbit regrouping. Only afterward does `AbsConvT` justify operator-norm convergence. Consequently the final Gram identity is not being used to prove the integrability on which it depends.',
        '',
        'The original columns use an antilinear Riesz map. The manuscript preserves the reversed inner product, both phases, the one finite-level volume, and the same supplied infinite measures and domains. Its normalized Gram identity and the transport to the original spectral datum have the correct conjugations. Zero normalizers and zero-dimensional spaces are covered by the literal total-inverse convention. A target projection retains its correction term unless a separate range statement kills it.',
        '',
        '## Corrections resolved before binding',
        '',
    ]
    for finding in resolved:
        paragraphs.append('- **' + finding['id'] + ':** ' + finding['finding'] + ' ' + finding['resolution'])
    paragraphs += ['', '## Claim-by-claim review', '']
    for claim in claims:
        paragraphs += ['### ' + claim['id'] + ': ' + claim['title'], '',
                       '**PASS.** ' + claim['reasoning'], '',
                       'Proof block SHA256: `' + claim['proof_range_sha256'] + '`.', '']
    paragraphs += [
        '## Exact retained boundary', '',
        result['limitations'], '',
        'No whole selected obligation is closed by this review. The explicit ordinary background consists of finite-dimensional linear algebra and Riesz/adjoint theory, number-field lattices and different ideals, Chinese remaindering and additive finite-adelic approximation, basic Haar theory, Tonelli and Bochner integration, and absolute convergence. The actual finite character, stabilizer, support, return-carrier and unfolding suppliers are proved in this chapter rather than imported as new assumptions.', '',
        '## Binding record', '',
        '`independent_review.json` records each of the twenty proof-block hashes, every full pinned source-file hash, every distinct exact source-range hash, and each inherited proof-file and block hash. The separate supporting Mathlib definition is pinned to its own commit, not mislabeled with the RH repository commit. `review_by_geometry.py` independently recomputes those bindings. It is a reproducibility check of the recorded review, not a substitute for mathematical reading.', '',
    ]
    (HERE / 'independent_review.md').write_text('\n'.join(paragraphs))
    print(json.dumps({'status': 'PASS', 'main_sha256': REVIEWED_MAIN_SHA,
                      'claims': len(claims), 'source_files': len(files),
                      'source_ranges': len(ranges), 'inherited': len(inherited_rows),
                      'review_json_sha256': sha((HERE / 'independent_review.json').read_bytes())}))


if __name__ == '__main__':
    main()
