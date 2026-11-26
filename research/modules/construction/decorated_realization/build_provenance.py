#!/usr/bin/env python3
"""Reproduce the DR source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
I = D + 'Proofs/IwasawaDecomposition/'
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]


common = [
    'The actual CMData E/F is supplied, including [E:F]=2, exact fixed field F, and for every maximal P an integral theta with theta-conjugate(theta) outside P. This component does not construct the original CM arithmetic host.',
    'The standard Hermitian form is conjugate linear in the first variable, and selfduality means O_E-valued Hermitian integrality, not a trace dual.',
    'Finite-completion and local-basis objects are the actual ones attached to the given number fields. Selected quotient maps and prescribed frames are retained exactly.',
    'No rational weak or strong approximation, rational SameGenus statement, full terminal-column construction, RH/GRH theorem, or Lean kernel replay is asserted.'
]


def claim(i, title, statement, deps, assumptions, srcs, relation):
    return dict(id=i, title=title, status='derived_simplification', statement=statement,
        depends_on=deps, assumptions=common+assumptions,
        proof_location=dict(file='main.tex', anchors=[i]),
        expanded_notes=dict(file='report.txt', section=i), source_relation=relation,
        mathematical_status='proved_under_exact_declared_supplied_data_hypotheses', sources=srcs)


claims = [
    claim('DR1', 'Local integral Hermitian orthonormal bases, including dyadic primes',
        'The literal CM unramified condition gives the actual local integral algebra A=R direct-sum R theta with unit discriminant, hence split or unramified quadratic completion. The unit norm map is onto by explicit successive trace corrections. Every perfect integral Hermitian lattice has an orthonormal integral basis, including residue characteristic two and rank zero.',
        [],
        ['At each finite prime the base ring is the complete DVR of F_v with finite residue field. In the split case the two completed factors are exchanged by the original involution. The lattice pairing is perfect.'],
        ss('src/Formalism/LocalRingCardinality/DataSpaces.lean', 'CMData CMData.sig', 'literal_CM_field_and_fixed_field_input') +
        ss('src/Formalism/HermitianLattices/StatementMass.lean', 'IsCMUnram', 'literal_theta_minus_conjugate_prime_unit_condition') +
        ss(D+'Proofs/FlagMeasures/ExistsLocalUnitaryOfSelfDualAtPlace.lean', 'exists_isUnit_sub normal_form exists_orthonormal exists_unitary_of_selfDualAt', 'complete_local_CM_specialization_reconstructed') +
        ss(D+'Proofs/AdelicLatticeProofs/ExistsEqTransposeMulMapOfIdempotent.lean', 'exists_norm_eq_of_henselian exists_eq_transpose_mul_map_of_henselian', 'generic_source_specialized_to_the_required_complete_DVR_case') +
        ss(D+'Proofs/AdelicLatticeProofs/ExistsIsUnitFormSelfOfNotMem.lean', 'exists_add_eq_one trace_surjective', 'source_trace_and_quadratic_etale_counterparts'),
        'Derives the full local integral algebra by (a-conj(a))/(theta-conj(theta)), proves simple-root lifting and unit norms explicitly, and splits off norm-one vectors. It proves the complete CM completion application, not every extra abstract Henselian-ring generalization in the source.'),
    claim('DR2', 'An actual finite-adelic realizer of every supplied self-dual lattice',
        'For every full self-dual O_E-lattice N in standard E^n, construct g in the actual unitary finite-adelic group with g*Ohat^n=Nhat and globLat(g)=N. At nonsplit places use DR1; at split pairs use arbitrary basis and its conjugate inverse transpose; use identity away from finite support. This proves Formalism.L2.Col.UnimodGenus directly.',
        ['DR1', 'NB1', 'LP1', 'AD4'],
        ['N is the supplied full self-dual lattice. AD4 is used only for its independently proved integral adelic-span/lattice-recovery identity; its conditional modification theorem does not supply an initial realizer here.'],
        ss(F+'Columns/Inputs.lean', 'UnimodGenus', 'literal_adelic_globLat_existence_predicate_proved') +
        ss(F+'Columns/Inputs.lean', 'UnimodGenusLoc', 'distinct_rational_semilocal_predicate_not_claimed_proved') +
        ss(I+'ValuedLtOfMem.lean', 'unimodGenus', 'actual_adelic_source_conclusion_reconstructed_by_a_direct_route') +
        ss(D+'Proofs/FlagMeasures/ExistsLocalUnitaryOfSelfDualAtPlace.lean', 'exists_frame exists_unitary_of_selfDualAt', 'local_completed_lattice_isometry_counterparts') +
        ss(D+'Proofs/FlagMeasures/ExistsFiniteAdelicPointLatticeEqSelfDual.lean', 'mem_genus', 'stronger_rational_genus_intermediate_bypassed_not_claimed_proved') +
        ss(I+'ValuedLtOfMem.lean', 'carries_globLat', 'actual_adelic_carrying_relation_reconstructed_in_AD4') +
        ss(F+'Columns/AdelicLemmas.lean', 'mem_globLat', 'literal_rational_intersection_relation'),
        'Constructs tensor-algebra entries by expanding the local matrices and their inverses in a fixed F-basis of E; their coefficients are actual finite adeles. This bypasses rational SameGenus and any rational approximation theorem, while proving the source adelic endpoint exactly.'),
    claim('DR3', 'Realize every prescribed decoration and rational frame',
        'For every valid DecoF with pairwise disjoint finite ST, SG and Q whose union contains no conjugate pair, construct a unitary finite adele satisfying every IsPtOf field: the exact carried lattice, all selected last-coordinate residues, every auxiliary residue coordinate, and the exact rational Q-frame components. The actual all-twist wrapper follows from its original prime-set checks. This discharges the initial realizer premise in FC3/FC19 and NB6.',
        ['DR2', 'AD4'],
        ['The decoration is valid in the literal Deco.Ok sense, its rational frames satisfy DecoF, and ST/SG/Q obey the exact disjointness and no-conjugate-pair conditions.',
         'For the actual true-column wrapper, the original prime coprimality, good-twist-place and LevOk split/disjointness laws are supplied. They imply the required finite-set conditions.'],
        ss(F+'Columns/StdLatUnimodular.lean', 'Deco Deco.Ok', 'literal_valid_decoration_data_and_all_residue_laws') +
        ss(F+'Columns/FiniteSumNonzeroLargeDepth.lean', 'DecoF DecoF.fr', 'literal_prescribed_rational_local_frame_data') +
        ss(A+'ReferenceCharactersFactorTame.lean', 'HasRes IsPtOf', 'exact_five_field_realization_target_and_residue_convention') +
        ss(I+'ValuedLtOfMem.lean', 'exists_modify exists_isPtOf_cm exists_isPtOf', 'actual_source_supplier_completely_reconstructed') +
        ss(F+'Columns/AdelicLemmas.lean', 'decoPtSurj_of', 'source_reduction_stage_replaced_by_local_adapted_frames_and_AD4') +
        ss(I+'ExistsAdelicPointDecoratedLatticeAllTwists.lean', 'exists_ptOf_twists', 'actual_all_twist_wrapper_and_prime_set_checks_reconstructed') +
        ss(I+'LevOkTwists.lean', 'levOk_twists', 'supplied_twist_prime_split_and_disjointness_laws') +
        ss(I+'ExistsMemberStepCharts.lean', 'yStd_spec', 'previous_realizer_boundary_now_discharged'),
        'Finite-field row/basis adaptation lifts only to GL_n(O_(P)), then one AD4 modification on ST union SG union Q gives every exact IsPtOf clause. HasRes is checked with the actual quotient map and multiplicative valuation. No global GL_n(O_E) reduction-surjectivity assertion is assumed.')
]

out = dict(schema_version='1.3', artifact_version='0.14', date='2026-11-21', owner='/root/global_frame',
    repository=dict(url=URL, commit=PIN),
    range_convention='One-indexed inclusive; exact original declaration bytes, with no newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True, range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True, human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False, local_lean_compilation=False, lean_kernel_replay=False,
        replacement_arguments_formalized=False, pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof of the precisely stated supplied-data assertion, possibly by a shorter route than the source.'),
    claims=claims, files=[files[p] for p in sorted(files)],
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    prior_components_reused=['LP'], same_iteration_companions=['AD','NB','FC','VE'],
    independent_reviews=[], retained_inputs=common,
    boundary_resolved=[
        'Actual local Hermitian orthonormalization from CMData.cmUnram, including dyadic completions',
        'Actual adelic Formalism.L2.Col.UnimodGenus and the initial lattice realizer',
        'Full exists_isPtOf_cm and exists_ptOf_twists, with exact f/be/fr components',
        'Initial decorated-point realizability premise of FC3/FC19 and NB6'],
    scope_precision=[
        'DR1 proves the complete DVR/finite-residue CM application of the generic Henselian source normal form, not every abstract generalization.',
        'Formalism.L2.Col.UnimodGenus is an adelic existence predicate and is proved. UnimodGenusLoc/PI.UnimodGenus and rational SameGenus are bypassed and not claimed proved.',
        'DR2 depends on primitive NB1 only, not NB6--NB8 or FC19; DR3 depends on DR2 and AD4. Supplying FC/NB initial realizers therefore creates no dependency cycle.',
        'Rational local basis lifts need only determinant units at one prime; no global GL_n(O_E) surjectivity is used.',
        'The finite support and coordinate expansion construct actual tensor-algebra finite adeles and their inverses.',
        'Rank zero forces ST empty for valid decorations and all auxiliary/frame coordinate clauses are vacuous.',
        'The primitive CM field and true-column host existence, terminal incidence, and symmetric-penultimate group/character identification remain separate.'])

review = HERE.parent/'reviews_v0_14'/'cr_reviews_dr.txt'
if review.exists():
    review_raw = review.read_bytes()
    review_text = review_raw.decode('utf-8')
    raw = (HERE/'main.tex').read_bytes()
    hashes = {}
    for i in range(1,4):
        start = raw.index(f'\\paragraph{{DR{i}:'.encode())
        stop = raw.index(f'\\paragraph{{DR{i+1}:'.encode(), start+1) if i<3 else len(raw)
        sha = digest(raw[start:stop])
        assert sha in review_text, ('DR independent paragraph review changed', i, sha)
        hashes[f'DR{i}'] = sha
    out['independent_reviews'].append(dict(reviewer='/root/class_rank', result='PASS', claim_ids=list(hashes),
        scope='Independent review of literal CM unramified input, dyadic trace/norm lifting and Hermitian diagonalization, actual adelic matrix assembly, local GL lifts and every IsPtOf field.',
        review_record='../reviews_v0_14/cr_reviews_dr.txt', review_record_sha256=digest(review_raw),
        paragraph_sha256=hashes, paragraph_range='Bytes from the named DR paragraph marker to the next DR paragraph, or EOF for DR3.', lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
locators=[]
for c in claims:
    locators += [f"{c['id']} | {c['title']} | {c['status']}",c['statement']]
    for s in c['sources']:
        locators += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",
            f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
    locators += ['']
(HERE/'source_locators.txt').write_text('\n'.join(locators)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN, files=out['files']), ensure_ascii=False, indent=2)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.14',commit=PIN,targets=[],
    closed_source_targets=[dict(path=I+'ValuedLtOfMem.lean',declaration='GlobalTheory.Mem.Col2.PtExist.exists_isPtOf_cm',closed_by=['DR1','DR2','DR3']),
        dict(path=I+'ExistsAdelicPointDecoratedLatticeAllTwists.lean',declaration='GlobalTheory.Mem.Col2.PtTwist.exists_ptOf_twists',closed_by=['DR3'])],
    remaining_boundary='No point-realizability target remains under the supplied CM/valid-decoration data. Primitive arithmetic-host existence and the separate terminal/symmetric full-column targets remain with their owning components.'), ensure_ascii=False, indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),
    next_targets=0,verified_equal_to_pinned_git_blob=True,independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))


