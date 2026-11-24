#!/usr/bin/env python3
"""Record the completed v0.13 review and continuation boundary.

This script writes metadata only. Mathematical source ledgers are assembled by
merge_v0_13.py; the cumulative TeX is assembled by assemble_v0_13.py.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_12'
QA = ROOT.parent / 'qa_v0_13_final'
PDF = ROOT / 'RH_readable_reconstruction_v0_13.pdf'
REVIEWS = ROOT / 'reviews_v0_13'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = read(QA / 'manifest.json')
assert manifest['pdf_sha256'] == sha(PDF)
assert manifest['pages'] == 150
shutil.copy2(QA / 'manifest.json', REVIEWS / 'pdf_render_manifest.json')

root_review = f"""FINAL PDF VISUAL REVIEW: FRONT PAGE AND LATTICE PATCHING
Reviewer: root
Result: PASS

PDF: RH_readable_reconstruction_v0_13.pdf
SHA256: {sha(PDF)}
Page count: 150

Viewed the individual final RGB PNG images of pages 1, 118, 119 and 120
using the image viewer. These images are the 1.25-scale PyMuPDF renders
recorded in pdf_render_manifest.json. The final PDF hash was checked.

Page 1: title, version, date, bounded status statement, pinned commit and
source/verification qualifications are legible and fit inside the margins.
Pages 118-120: CS9's conclusion and all of LP1-LP5 fit correctly. The ideal
factorization, intersection-localization argument, boxed exact patch,
global commensurability bound, type-prime distinction and ramification-
normalized length equations have no clipping, collisions or missing glyphs.
The explicit remaining geometric/refill/NumAt boundary is visible on page
120. The following section begins normally below it.

This is a layout review. Mathematical and source checks are recorded
separately. No proof text was changed after these final renders.
"""
(REVIEWS / 'pdf_front_lp_root.txt').write_text(root_review)

review_specs = [
    ('global_frame', 'pdf_pages_001_048_sf.txt', [1, 48], [[108, 110]]),
    ('class_rank', 'pdf_pages_049_096_cr.txt', [49, 96], [[111, 113]]),
    ('comparison_span', 'pdf_pages_097_150_cs.txt', [97, 150], [[114, 118]]),
    ('root', 'pdf_front_lp_root.txt', None, [[1, 1], [118, 120]]),
]
reviews = []
for reviewer, name, contact_range, individual_ranges in review_specs:
    path = REVIEWS / name
    assert sha(PDF) in path.read_text(), name
    reviews.append({
        'reviewer': reviewer,
        'record': 'reviews_v0_13/' + name,
        'record_sha256': sha(path),
        'contact_sheet_page_range': contact_range,
        'individual_page_ranges': individual_ranges,
        'reviewed_pdf_sha256': sha(PDF),
        'result': 'passed',
        'corrections_required': False,
    })

log = (ROOT / 'build/RH_readable_reconstruction_v0_13.log').read_text()
for marker in ['Overfull', 'Missing character', 'undefined references', 'undefined citations']:
    assert marker not in log, marker
warnings = [line.strip() for line in log.splitlines() if 'Warning' in line]
visual = {
    'artifact_version': '0.13',
    'date': '2026-11-21',
    'pdf_filename': PDF.name,
    'pdf_sha256': sha(PDF),
    'page_count': 150,
    'all_pages_rendered': True,
    'all_pages_visually_reviewed_at_contact_sheet_scale': True,
    'individual_page_ranges': [[1, 1], [108, 120]],
    'corrections_required_after_final_render': False,
    'reviews': reviews,
    'render_method': manifest['renderer'],
    'rendered_page_count': 150,
    'contact_sheet_count': len(manifest['sheets']),
    'final_compile_warnings': warnings,
    'warning_assessment': 'The sole epstopdf warning reports disabled shell escape. No EPS conversion is used; the document compiled offline with embedded fonts.',
    'overfull_boxes': 0,
    'missing_character_warnings': 0,
    'unresolved_references_or_citations': 0,
    'render_manifest': {
        'record': 'reviews_v0_13/pdf_render_manifest.json',
        'record_sha256': sha(REVIEWS / 'pdf_render_manifest.json'),
    },
    'scope': 'All 150 pages were inspected in contact sheets. The front page and every newly added proof page (108-120) were also inspected individually. Mathematical/source reviews are separate. No Lean build or kernel replay was run.',
}
write(ROOT / 'visual_qa.json', visual)

sections = {
    'SF': {'component': 'global_frame', 'title': 'One global frame for all the local comparisons', 'page_start': 108, 'fragment': 'main.tex'},
    'CR': {'component': 'class_rank', 'title': 'The actual class-rank identity', 'page_start': 111, 'fragment': 'main.tex'},
    'CS': {'component': 'comparison_span', 'title': 'The exact global comparison lattice', 'page_start': 114, 'fragment': 'main.tex'},
    'LP': {'component': 'lattice_patching', 'title': 'Patching the selected local lattices into one global lattice', 'page_start': 118, 'fragment': 'main.tex'},
}
filename_map = read(OLD / 'component_filename_map.json')
filename_map['note'] = ('Historical component bytes and source arrays are preserved. Current v0.13 proves the common-frame/companion algebra, actual class-rank equality, exact integral comparison span and selected local lattice patching under their explicit supplied-data hypotheses. Simultaneous forms/value/model existence, full refill/point/NumAt and the independent global branches remain. Twelve predecessor root files are archived under history/version_0_12/.')
filename_map['version_0_13_component_pages'] = sections
write(ROOT / 'component_filename_map.json', filename_map)

provenance = read(ROOT / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
checkpoint = read(OLD / 'continuation_checkpoint.json')
old_remaining = copy.deepcopy(checkpoint['remaining_major_inputs'])
old_new = copy.deepcopy(checkpoint['new_in_this_version'])
checkpoint.update({
    'artifact_version': '0.13',
    'predecessor_version': '0.12',
    'date': '2026-11-21',
    'main_note_pages': 150,
    'new_section_start_pages': {k: v['page_start'] for k, v in sections.items()},
    'new_section_headings': {k: v['title'] for k, v in sections.items()},
    'logical_component_page_map': sections,
    'status': 'Partial RH/Dirichlet-GRH reconstruction. The common global-frame/companion algebra, actual class-rank equality and exact integral comparison span are proved for the same supplied compatible forms and values; selected served/type-prime lattices are patched exactly. Simultaneous forms/value/model construction, full refill/point/NumAt, host arithmetic supply and independent global branches remain.',
    'new_in_this_version': [
        'SF1-SF7: one common global basis; actual true-column coordinates; diagonal Hermitian companion identity; symmetric base compatibility and simultaneous local-frame replacement without changing the embeddings, orbit representatives, parity or normalized valuations.',
        'CR1-CR6: integral Weyl fiber bases, finite-class evaluation, actual double-coset/class correspondence, stabilizer triviality at two auxiliary primes, and literal locPack_d_eq/pack_d_eq. Joint0 is unused in rank; Delta and nabla are not equated integrally.',
        'CS1-CS9: valuation-ring pivot descent, signed integral Weyl duality, actual even/odd local coefficient-lattice equality, ValIntRec, rational-integral detection, exact finite-place approximation, rational integral-function spanning, rational comparison surjectivity and exact integral comparison-lattice span.',
        'LP1-LP5: Dedekind denominator clearing, exact localization of the bounded-denominator intersection, finite-place patching with a global commensurability bound, actual retained-Mram served/type-prime application and conditional installation with exact ramification-normalized lengths.',
    ],
    'retained_prior_results_note': 'Earlier entries describe their own versions and remain historical records. The current conclusions and remaining inputs are stated in version_0_13_update and remaining_major_inputs; all v0.12 mathematics and source annotations are retained.',
    'previous_source_targets_file': 'history/version_0_12/next_source_targets.json',
})
checkpoint['remaining_major_inputs'] = [
    'Construct one simultaneous family of compatible standard global forms, carriers and polynomial values supplying SF/CR/CS: formsTiedSym_std, hermColsCh_of_forms, colsTiedSym_std, val_tied, ex_C_blk and valEx_of_rep\'. This includes the actual Ok/Pins/Laws/Later, Forms0/ValEx and Joint0 data. Under supplied Joint0, SameUloc is its literal local-group equality and is not another open hypothesis.',
    'Complete the geometric Lay/RecOK/LedOK local conditions, canonical exists_refill, all-pairs pointRecExP/ObjCP and the stronger NumAt parameter record. LP supplies the exact selected lattice patch and conditional setLat length fields, not these remaining existence inputs.',
    'Construct the underlying HostAx/character field with its Galois, cyclotomic and half-different properties and actual rank/model inputs; prove the exact ShortNorm/SmallOne/ThinH and PairEx/cohomological-window suppliers retained in HC. Biased tops and the CT2=64 second set remain proved.',
] + old_remaining[2:]
checkpoint['next_targets'] = [
    'First reconstruct the simultaneous standard-forms and polynomial-value constructors, starting with formsTiedSym_std and val_tied, then the exact carrier and ValEx joins. Reuse SF/CR/CS rather than reopening their completed conditional arguments.',
    'Complete canonical refill, the geometric point construction and NumAt, retaining the actual Mram reference, type-prime exception and ramification-normalized length scale established in LP.',
    'Continue host/field and analytic supply and the four unchanged independent global branches. Preserve the active HostWW/KitS/ChosenWall route and the optional status of CoverAll and IsRecCEv.',
]
checkpoint['precision_constraints'].extend([
    'All prior precision constraints remain historical. The v0.13 annotations supersede only the explicitly reconstructed common-frame/rank/comparison algebra and lattice-patching portions.',
    'One supplied orthonormal global integral frame is used everywhere. Independent local bases alone do not construct it; actual positive true-column coordinates allow the standard frame.',
    'The diagonal base lattice has Hermitian dual O_E^(n-1) plus conjugate(pi)^(-1) O_E, and L_pi + conjugate(pi) L_pi# = O_E^n. The conjugation and same ambient coordinates are essential.',
    'At p not dividing T, the inclusions L subset L0 subset L# and T L# subset L identify the actual projected lattice with j_v(B) O_v^n. The original embeddings, representatives, c^s parity and p-normalized valuation are retained.',
    'Class-rank uses the integral Weyl lattice Delta. Delta and the coefficient dual lattice nabla have matching rational dimensions but need not agree as integer lattices.',
    'The auxiliary level condition is upper-unitriangular reduction. The torsion argument first reduces its prime-to-g part, then uses congruence induction; it does not replace that level by a principal congruence subgroup.',
    'Joint0 is unused in the rank wrapper only. It still supplies essential common local-subgroup data for the integral comparison; SameUloc is not a separate unproved theorem under supplied Joint0.',
    'The odd-position comparison uses complementary minors and the inverse integral Gram matrix. It preserves the exact integral Weyl lattice; rational representation equivalence alone would not suffice.',
    'The rational forms/rank bridge also uses emb_basis and Fi_zero; CR6 alone is not the entire bridge.',
    'The conclusion of CS is O-span(C(global lattice))=M. Exact integral equality is separate from any Hermitian norm, covolume or isometric transport assertion.',
    'LP uses the retained Mram reference. Its local saturation is closure under units outside a prime, not global primitive saturation. The prescribed type-prime lattice can enlarge the reference, so global N subset M is not asserted.',
    'The intersection-localization step requires the common-denominator condition stated in LP2. It is not a blanket rule that localization commutes with arbitrary infinite intersections.',
    'The length conversion uses lenLoc.toNat/e_w and gives l=e_w*lenMN when local length is the finite integer l. It does not assert finite length at every unspecified place.',
    'All 438 prior claim fields/source arrays, all 1032 prior source-file records and all prior mathematical dependency adjacency lists are preserved exactly. Only five version_0_13_update fields are appended to historical claims.',
])
checkpoint['precision_supersessions'].append({
    'previous_checkpoint_version': '0.12',
    'historical_statement': old_remaining[0],
    'current_statement': 'SF/CR/CS prove the common global-frame/companion algebra, literal class-rank equality and exact integral comparison span for the supplied compatible data. The remaining comparison input is the simultaneous global forms/value/model construction. LP also discharges the selected lattice-patching portion of the point route under its explicit geometric local conditions.',
    'completed_by': ['SF7', 'CR6', 'CS9', 'LP4', 'LP5'],
})
checkpoint['version_0_13_update'] = {
    'local_conclusions': copy.deepcopy(provenance['version_0_13_local_conclusions']),
    'remaining_inputs': checkpoint['remaining_major_inputs'],
    'superseded_previous_comparison_frontier': old_remaining[0],
    'unchanged_global_branches': old_remaining[2:],
    'historical_claim_updates': ['PL13', 'PL16', 'BC8', 'LI5', 'LI8'],
    'historical_source_arrays': 'All 438 prior claim fields/source arrays and 1032 prior source-file records are preserved.',
    'historical_dependency_graph': 'Every old adjacency list and all 789 prior dependency edges are preserved; 27 nodes and 50 edges are added. The graph is acyclic and is not a Lean transitive dependency audit.',
    'historical_components': 'All 425 predecessor files are byte-identical at their former path or in history/version_0_12; exactly twelve superseded root files are archived there.',
}
checkpoint['validation'] = {
    'claims': 465,
    'new_claims': 27,
    'source_links': 7593,
    'source_files': 1098,
    'next_target_ranges': 30,
    'next_target_source_files': 30,
    'source_files_checked_including_next_targets': 1109,
    'all_cited_ranges_and_file_hashes_checked': True,
    'all_source_bytes_match_pinned_git_blobs': True,
    'all_prior_claim_fields_and_source_arrays_preserved': True,
    'all_prior_source_records_preserved_exactly': True,
    'all_prior_dependency_graph_entries_preserved': True,
    'predecessor_package_file_count': 425,
    'previous_root_files_archived': 12,
    'new_component_file_count': 26,
    'source_verification_record': 'reviews_v0_13/source_verification.txt',
    'continuity_audit_record': 'reviews_v0_13/continuity_audit.txt',
    'full_lean_build_or_kernel_replay': False,
    'lean_sources_modified': False,
    'cross_reviews': 'Scoped independent reviews cover SF, CR, CS and LP. CS was cross-reviewed mathematically before a final sentence-only layout edit; root_cs_layout_edit.txt records the before/after hashes and the unchanged mathematical content. Final CS pages were re-rendered and visually reviewed.',
    'pdf': visual,
}
assert checkpoint['version_0_12_update'] == read(OLD / 'continuation_checkpoint.json')['version_0_12_update']
assert checkpoint['version_0_13_update']['unchanged_global_branches'] == old_remaining[2:]
write(ROOT / 'continuation_checkpoint.json', checkpoint)

readme = """RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.13
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed self-contained proof
of RH or Dirichlet GRH. Version 0.13 proves the common global-frame/companion
algebra, actual class-rank equality and exact integral comparison span under
the literal compatible-forms/value hypotheses. It also patches the prescribed
local lattices and installs the exact normalized length fields under their
stated local and refill assumptions. The simultaneous forms/value/model
construction and independent global inputs remain explicitly identified.
These are boundaries of this exposition, not claims of missing arguments in
the released Lean source. The GRH scope is Dirichlet L-functions.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_13.pdf is the cumulative 150-page note.
Its matching TeX source is included. The new sections start here:

  SF1-SF7: one global frame for all local comparisons, page 108.
  CR1-CR6: the actual class-rank identity, page 111.
  CS1-CS9: the exact global comparison lattice, page 114.
  LP1-LP5: patch selected local lattices into one global lattice, page 118.

For this increment, read SF then CR then CS. LP is a separate advance in the
point construction. Each component directory includes a readable expanded
report.txt, the main.tex fragment, source provenance and its ledger builder.
The current remaining-work section starts on page 139; the claim ledger
starts on page 141. Every earlier component and historical proof is retained.

NEW MATHEMATICS AND ITS BOUNDARY
SF uses one supplied global orthonormal integral basis throughout. In the
actual positive true-column coordinates that basis is standard. The explicit
Hermitian dual of L_pi=O_E^(n-1) plus pi O_E gives the exact companion identity
L_pi + conjugate(pi) L_pi# = O_E^n. The projected lattices away T are expressed
in the same global frame. The original embeddings, representatives, c^s
parity and normalized valuations survive the frame replacement. This does
not independently construct all standard forms/carriers and their values.

CR computes the actual integral Weyl fiber rank, identifies the double-coset
classes with the relevant lattice-orbit classes and proves stabilizer
triviality using the actual upper-unitriangular conditions at two distinct
auxiliary primes. Evaluation gives the product rank formula and literal
locPack_d_eq/pack_d_eq. The Joint0 argument is unused in this rank equality.
Delta is not equated with its dual coefficient lattice nabla over integers.

CS proves exact integral span O-span(C(global lattice))=M. Its odd-position
duality is an integral complementary-minor map with the correct signs and
integral Gram inverse. It retains the same embeddings and parity. Pivot
descent and exact finite-place approximation give rational integral-function
spanning. The rational comparison becomes surjective using CR and the
separate emb_basis/Fi_zero bridge; an L-linear retraction handles descent.
The final span equality follows from the integrality criterion. All steps
retain the same supplied Forms0, ValEx, Joint0, character rationality and
comparison record. SameUloc is supplied by Joint0, not another open theorem.
No norm or covolume equality is inferred from the module equality.

LP proves the exact finite-place patch over a number ring by denominator
clearing and localization of an intersection with a common-denominator
condition. For finitely many prescribed A_P, it obtains N_P=A_P and leaves
all other localizations unchanged, with dM subset N subset d^(-1)M. The
actual reference is retained Mram. Type-prime targets may enlarge it, so a
global containment N subset M is not claimed. Conditional setLat installs
lenMN=lenLoc.toNat/e_w, with the exact finite-length equality. Full geometric
Lay/RecOK/LedOK, canonical refill, pointRecExP/ObjCP and NumAt remain inputs.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants (10,54,1088). These sufficient constants and their
proofs are preserved; they are not claimed optimal. The v0.12 biased tops,
no-relation set, conditional host joins and local identifications also remain.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: 465 stable claims, 7593 source links, 1098 indexed source
files. The 27 new claims are SF7+CR6+CS9+LP5.

Each source entry records the original declaration, exact inclusive line
range, pinned URL, full-file SHA256 and range SHA256. Source bytes were
checked against pinned Git blobs. provenance.json is authoritative;
provenance.txt is its readable view; source_index.json records file hashes.
The mathematical dependency graph is acyclic. It is not a Lean transitive
dependency audit. next_source_targets.json records 30 exact continuation
ranges, grouped by forms/value supply, point/NumAt, host arithmetic and the
four independent global branches.

Examples after unpacking, with a local pinned source checkout:
  python3 backtrack.py SF7
  python3 backtrack.py CR6 --repo /path/to/riemann-hypothesis-lean
  python3 backtrack.py CS9 --repo /path/to/riemann-hypothesis-lean --entry 1
  python3 backtrack.py LP4
  python3 backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean

The read-only helper works without network access. Its final check verified
1109 distinct files including continuation targets, all 7593 claim-source
ranges and all 30 target ranges. The output is preserved in reviews_v0_13.
No Lean sources are bundled or modified; use a separate pinned checkout.

BUILD AND CONTINUITY
The PDF was built offline using the installed LaTeX packages and fonts.
Ordinary pdflatex can build the supplied cumulative TeX; build_pdf.py also
records the environment-specific offline format and font-map workaround.
assemble_v0_13.py reproduces the cumulative TeX from the archived v0.12
source and four fragments. merge_v0_13.py merges the exact ledgers and checks
the continuation against a sibling lean-source checkout at the pinned commit.
finish_metadata_v0_13.py records the final review/checkpoint metadata; its
reproduction uses the separate scratch render manifest, not bundled images.

All 438 prior claim fields/source arrays, all 1032 prior source-file records
and every old dependency adjacency list are preserved. Only explicit v0.13
annotations are appended to PL13, PL16, BC8, LI5 and LI8. Earlier local
conclusion records retain their exact values. Every one of the predecessor's
425 files is byte-identical at its original path or in history/version_0_12/.
Exactly twelve superseded root files, including the old PDF, are archived.

REMAINING WORK
The next priority is the simultaneous standard forms and polynomial-value
construction: formsTiedSym_std, val_tied, the carrier/column joins and ValEx.
The new comparison theorem is proved with those actual compatible data as
explicit premises. The remaining point and NumAt construction must retain
the Mram reference and type-prime/ramification distinctions proved in LP.
Underlying HostAx/character-field and analytic suppliers also remain.

The four independent global branches are unchanged: theta/spectral kernels;
dimension/metric/discarded-target control; congruence/cohomological windows;
and simultaneous PairEx plus the centered prime-sum window theorem.
Optional CoverAll and IsRecCEv are not imposed on the active family route.

VERIFICATION
Mathematical cross-reviews, exact source checks and continuity checks are
recorded. visual_qa.json identifies the final PDF by SHA256. All 150 pages
were rendered and reviewed in contact sheets; the front page and every new
proof page were also inspected individually. No clipping or missing-glyph
issues were observed. The final TeX log has no overfull boxes or unresolved
references. SHA256SUMS covers every package file except itself; transient
build output and render images are excluded. No full Lean build or independent
kernel replay was run. No new public verification-status assertion is made.
"""
(ROOT / 'README.txt').write_text(readme)
print('Wrote v0.13 README, checkpoint, filename map and final visual-review metadata.')
