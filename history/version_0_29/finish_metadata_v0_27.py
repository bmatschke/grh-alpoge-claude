#!/usr/bin/env python3
"""Write the checked v0.27 checkpoint and human-readable continuation files."""
from pathlib import Path
import copy
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_26'
REVIEW = ROOT / 'reviews_v0_27'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numbered(items):
    return '\n'.join(f'{i}. {s}' for i, s in enumerate(items, 1))

cfg = read(ROOT / 'increment_v0_27.json')
ledger = read(ROOT / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
audit = read(REVIEW / 'source_verification_v0_27_audit.json')
texcheck = read(ROOT / 'tex_validation.json')
tex = ROOT / 'RH_readable_reconstruction_v0_27.tex'
assert audit['result'] == 'PASS'
assert texcheck['tex_sha256'] == sha(tex) and texcheck['pdf_generated'] is False
for name, expected in audit['input_sha256'].items():
    assert sha(ROOT / name) == expected, name

sections = {}
for component in cfg['components']:
    data = read(ROOT / component / 'provenance.json')
    text = (ROOT / component / 'main.tex').read_text()
    prefix = re.match('[A-Z]+', data['claims'][0]['id'])[0]
    reports = [p for p in ['report.txt', 'report.md'] if (ROOT / component / p).is_file()]
    sections[prefix] = {
        'component': component,
        'title': re.search(r'\\section\{([^}]*)\}', text)[1],
        'section_label': re.search(r'\\label\{([^}]*)\}', text)[1],
        'claims': [c['id'] for c in data['claims']],
        'fragment': component + '/main.tex',
        'expanded_report': component + '/' + reports[0] if reports else None,
        'page_numbers_available': False,
    }

old = read(OLD / 'continuation_checkpoint.json')
checkpoint = copy.deepcopy(old)
checkpoint.update(
    artifact_version='0.27', predecessor_version='0.26', date=cfg['date'],
    user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and an updated ZIP suffice; no PDF requested.',
    main_note_pages=None, new_section_start_pages={},
    new_section_headings={p: s['title'] for p, s in sections.items()},
    logical_component_page_map=sections, status=cfg['scope'],
    new_in_this_version=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'],
    next_targets=cfg['next_steps'],
    next_source_targets_file='next_source_targets.json',
    previous_source_targets_file='history/version_0_26/next_source_targets.json',
)
checkpoint['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
checkpoint['retained_prior_results_note'] = (
    'Every historical proof and original claim/source field is preserved. Current closures are '
    'additive version_0_27_update annotations and semantic AND/OR map updates. Earlier open-premise '
    'statements must be read with the version-0.27 scope bridge.'
)
checkpoint['precision_constraints'].extend(cfg['precision_notes'])
checkpoint['precision_supersessions'].extend(cfg['new_in_this_version'])
checkpoint['version_0_27_update'] = {
    'local_conclusions': cfg['new_in_this_version'],
    'premise_closures': cfg['claim_updates'],
    'remaining_inputs': cfg['remaining_major_inputs'],
    'semantic_obligation_map': 'dependency_audit_v0_27/obligation_map.json',
    'next_work_packages': 'dependency_audit_v0_27/next_targets.json',
    'actual_auxiliary_data_and_conditional_G1': ['AX1–AX10'],
    'actual_local_and_cohomological_installation': ['DX1–DX8'],
    'complete_actual_model_constructor': ['MX1–MX10'],
    'complete_internal_model_comparison': ['PX1–PX10'],
    'paired_count_retained_cut': [
        'Literal SymplecticFourImageDense on the original data',
        'Actual AllIrr RigidAt on each same constructed datum',
        'SP9 exact uniformly quantified conjugation-stable finite catalogue',
    ],
    'model_comparison_retained_predicates': ['D.Fin0', 'D.NoEnd', 'D.AllIrr D.RigidAt'],
    'rigSp4_alt_producer_supplied': False,
    'entire_CohomologyHyp_supplied': False,
    'entire_BlochKatoLocal_supplied': False,
    'actual_arithmetic_deformation_model_installed': True,
    'integral_formal_smoothness_claimed': False,
    'actual_symplectic_catalogue_supplied': False,
    'CountII_and_CountIII_closed': False,
    'complete_original_field_count_to_window_assembly': ['HV1–HV10', 'TW8', 'OB8', 'VW3', 'VW4'],
    'PointHV_supplied_counts': ['CountZ', 'CountVs', 'CountIV'],
    'PointHV_retained_counts': ['CountI', 'CountII', 'CountIII', 'CountV'],
    'PointHV_original_field_case_layer_sum_assembly_retained': False,
    'unconditional_actual_family_LinkN_closed': False,
    'full_RH_GRH_closed': False,
}
checkpoint['current_deliverable'] = {
    'main': tex.name, 'archive': 'RH_reconstruction_v0_27.zip',
    'audit': 'RH_dependency_audit_v0_27.txt', 'pdf_generated': False,
    'reason': 'The user prioritizes proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.',
}
coverage = read(REVIEW / 'mathematical_review_coverage_v0_27.json')
checkpoint['validation'] = {
    **audit, 'tex': texcheck,
    'mathematical_review_coverage': 'reviews_v0_27/mathematical_review_coverage_v0_27.json',
    'mathematical_reviews': {r['review']: r['sha256'] for r in coverage['review_records']},
    'new_claims_independently_reviewed': len(coverage['coverage']),
    'formal_lean_build': False, 'independent_kernel_replay': False,
    'pdf_visual_review_performed': False,
}
write(ROOT / 'continuation_checkpoint.json', checkpoint)

mapping = read(OLD / 'component_filename_map.json')
mapping['version_0_27_component_sections'] = sections
mapping['version_0_27_note'] = (
    'No new PDF. Exact section labels and proof/source ranges identify AX/DX/MX/PX. The actual '
    'symplectic datum, local installation, Model and internal comparison are supplied; image-density, '
    'actual same-datum irreducible rigidity and the exact uniform catalogue remain. CountI/II/III/V '
    'and the independent global family/gap/local/metric/spectral obligations remain.'
)
write(ROOT / 'component_filename_map.json', mapping)

retired = targets.get('version_0_27_replaced_targets', [])
main_outcome = '''The paired symplectic count route now has its actual auxiliary datum,
local cohomology and deformation charts, a complete Model constructor on
the coefficient ring of that actual datum, and the full internal weighted-algebra,
point, torus-orbit, tangent and trace comparison.

AX constructs Raw/Good/OfCase in both cases and proves the ordinary,
level, dual and safe unlinking properties. It uses the given coefficient
ring when the required dyadic roots are present; otherwise it uses the
permitted finite extension, with SP8/RV1 supplying the normalized return
to the given ring. DX/MX/PX retain the ring of that actual datum.
Under the retained literal
SymplecticFourImageDense predicate, it supplies Fin0, NoEnd and one common
complex embedding before all irreducible points, closing SP10 G1.

DX installs PhiCond, Nums and the original LocBase from matched finite
duality and explicit matrix deformations. MX builds every field of the
actual Model, including the integral cuts and cocycle-derived derivations.
Its local charts are characteristic-zero charts; integral formal
smoothness and the entire BlochKatoLocal package are not asserted.

PX carries the model through actual point classification, integral point
scaling, conjugacy-to-orbit and infinitesimal comparisons to literal D.Ineq
under the same datum's Fin0, NoEnd and AllIrr RigidAt. The exact factor two,
integral cotangent lattice and original valuation are retained.

A sufficient remaining paired-count cut is:

    SymplecticFourImageDense
    AND actual AllIrr RigidAt on the same constructed data
    AND SP9's exact uniformly quantified finite automorphic catalogue.

The source rigSp4_alt producer, including its local Hodge/adjoint joins,
remains to be reconstructed. Naming RigiditySymplecticFour alone does not
close that implication. The catalogue must retain the original level,
weights, duality, Frobenius convention and quantifier order.

CountII and CountIII are not yet complete. CountI and CountV also remain.
HV10 already carries exactly these four actual counts through the entire
original-field PointHV assembly; TW8/OB8/VW then gives the existing
cohomological-window and fixed-pair endpoints. No downstream assembly
needs to be reopened.

The common geometric family and arithmetic gap, genuine theta/local
state, actual denominator tables and exact metric/global/spectral
comparisons remain separate obligations. This is a partial human
reconstruction, not a completed human RH/Dirichlet-GRH proof.
'''
integrity = f'''Current package: {len(ledger['claims'])} stable claims, including
{ledger['validation']['new_claims']} new consolidated endpoints;
{len(ledger['source_files'])} indexed source files and
{ledger['validation']['source_link_count']} claim-source ranges.
All {audit['source_files_checked_including_targets']} cited/target source files
and {len(targets['targets'])} active continuation ranges match the pinned Git blobs.
The semantic sufficient-obligation map has {audit['semantic_obligation_nodes']} nodes.
These counts describe navigation and integrity, not completion percentage.

Every original field of all {audit['prior_claims']} prior claims and all
their original source arrays and reference edges is preserved.
All {audit['previous_total_files_preserved']} predecessor files are retained;
{audit['previous_root_files_archived']} predecessor root files are archived exactly
in history/version_0_26. The reference and semantic graphs are acyclic.
{len(retired)} fully supplied continuation targets are retired with their
original snapshots; partial closures retain their exact remaining scope.

Independent mathematical reviews cover every new endpoint and are bound
to final component texts. Draft-mode TeX syntax and reference checks pass.
No new Lean build, independent kernel replay, PDF or visual review was
performed. The reported formal verification is accepted as background;
retained tasks describe the unfinished human reconstruction.
'''
summary = f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.27
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_27.tex.
The full archive preserves every earlier proof and includes exact proof/source
ledgers, independent mathematical reviews and the current semantic map.

MAIN OUTCOME
{main_outcome}
INTEGRITY AND REVIEW
{integrity}
'''
full_audit = (ROOT / 'dependency_audit_v0_27/audit.txt').read_text()
(ROOT / 'RH_dependency_audit_v0_27.txt').write_text(summary + '\n' + full_audit + '\n')

readme = f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.27
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_27.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_27.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_27/obligation_map.json is the finite semantic AND/OR map.
provenance.json and provenance.txt bind stable claims to exact pinned source
declarations and exact human-proof ranges. next_source_targets.json records
the active frontier. The audit directory identifies each retained count route.

No new PDF was generated. Any historical PDF is an older snapshot.

MAIN OUTCOME
------------
{main_outcome}
WHAT CLOSED
-----------
{numbered(cfg['new_in_this_version'])}

READING THE NEW PROOF
--------------------
Read symplectic_arithmetic_data/main.tex (AX1–AX10) for the actual
Raw/Good/OfCase construction and ordinary/level/dual/safe properties.
AX10 gives the exact conditional G1 endpoint under ImageDense.

Read symplectic_local_installation/main.tex (DX1–DX8) for finite duality,
the original PhiCond/Nums, and the ordinary and finite-inertia charts.
Then symplectic_model_construction/main.tex (MX1–MX10) builds the literal
Model, retaining integral cuts, all local witnesses and every actual
cocycle-to-derivation identity.

Read symplectic_model_comparison/main.tex (PX1–PX10) for the invariant
chart, integral point generation/scaling, actual point classification,
two-sided irreducibility, torus orbits, tangent rigidity and trace bound.
Return to symplectic_count_closure/main.tex (SP9–SP10) for the precise
uniform catalogue and final paired-count join. Their retained arithmetic
predicates are now the next complete-chain targets.

point_hv_assembly/main.tex (HV1–HV10), TW8, OB8 and VW3/VW4 already prove
every downstream step from CountI/II/III/V to the window endpoint. The
independent global LinkN, family, gap and metric/spectral branches retain
their stated hypotheses; WB7–WB8 and AN2/AN3/GH6 remain the global spine.

CURRENT FRONTIER
----------------
{numbered(cfg['remaining_major_inputs'])}

NEXT COMPLETE-CHAIN TARGETS
--------------------------
{numbered(cfg['next_steps'])}

INTEGRITY AND REVIEW
--------------------
{integrity}
REPRODUCE / CONTINUE
-------------------
From the extracted archive root, with a checkout at the pinned commit:

  python backtrack.py AX10 --repo PATH_TO_SOURCE
  python backtrack.py DX8 --repo PATH_TO_SOURCE
  python backtrack.py MX10 --repo PATH_TO_SOURCE
  python backtrack.py PX10 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_27.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. Current configure,
assemble and merge scripts produce the cumulative text and ledger.
Run finish_metadata_v0_27.py after audit_v0_27.py and validate_tex_v0_27.py;
package with package_v0_27.py. Old-version scripts are historical artifacts;
do not run them against current root metadata. The full Lean checkout is
not redistributed. No fresh Lean compilation or kernel replay is claimed.
'''
(ROOT / 'README.txt').write_text(readme)

scope_report = ('FINAL SCOPE REVIEW — VERSION 0.27\n\n'
                'PASS for the stated human-reconstruction scope.\n\n'
                + main_outcome + '\nEXACT SCOPE CONSTRAINTS\n'
                + numbered(cfg['precision_notes'])
                + '\n\nThis release-scope record summarizes the separately bound mathematical, '
                  'configuration and semantic reviews; source/hash and TeX checks establish '
                  'traceability and syntax, not the truth of unfinished arithmetic suppliers.\n')
(REVIEW / 'final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint': str(ROOT / 'continuation_checkpoint.json'),
                  'audit': str(ROOT / 'RH_dependency_audit_v0_27.txt'),
                  'claims': len(ledger['claims']),
                  'new_claims': ledger['validation']['new_claims']}, indent=2))
