#!/usr/bin/env python3
"""Write the checked v0.29 checkpoint and human-readable continuation files."""
from pathlib import Path
import copy
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_28'
REVIEW = ROOT / 'reviews_v0_29'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numbered(items):
    return '\n'.join(f'{i}. {s}' for i, s in enumerate(items, 1))

cfg = read(ROOT / 'increment_v0_29.json')
ledger = read(ROOT / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
audit = read(REVIEW / 'source_verification_v0_29_audit.json')
texcheck = read(ROOT / 'tex_validation.json')
tex = ROOT / 'RH_readable_reconstruction_v0_29.tex'
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
    artifact_version='0.29', predecessor_version='0.28', date=cfg['date'],
    user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and an updated ZIP suffice; no PDF requested.',
    main_note_pages=None, new_section_start_pages={},
    new_section_headings={p: s['title'] for p, s in sections.items()},
    logical_component_page_map=sections, status=cfg['scope'],
    new_in_this_version=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'],
    next_targets=cfg['next_steps'],
    next_source_targets_file='next_source_targets.json',
    previous_source_targets_file='history/version_0_28/next_source_targets.json',
)
checkpoint['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
checkpoint['retained_prior_results_note'] = (
    'Every historical proof and original claim/source field is preserved. Current closures are '
    'additive version_0_29_update annotations and semantic AND/OR map updates. Earlier open-premise '
    'statements must be read with the version-0.29 scope bridge.'
)
checkpoint['precision_constraints'].extend(cfg['precision_notes'])
checkpoint['precision_supersessions'].extend(cfg['new_in_this_version'])
checkpoint['version_0_29_update'] = {
    'local_conclusions': cfg['new_in_this_version'],
    'premise_closures': cfg['claim_updates'],
    'remaining_inputs': cfg['remaining_major_inputs'],
    'semantic_obligation_map': 'dependency_audit_v0_29/obligation_map.json',
    'next_work_packages': 'dependency_audit_v0_29/next_targets.json',
    'complete_universal_arithmetic': ['KX1–KX9'],
    'complete_adjoint_and_support_joins': ['QX1–QX10'],
    'complete_case_two_seed': ['SX1–SX8'],
    'complete_case_two_promodularity': ['UX1–UX12'],
    'complete_conditional_case_two_count': ['YX1–YX2'],
    'inherited_complete_cohomology_rigidity_catalogue': ['BX1–BX8','RX1–RX7','CX1–CX9'],
    'inherited_actual_image_density_and_count_joins': ['IX1–IX10','JX1–JX2'],
    'inherited_actual_model_and_comparison': ['AX1–AX10','DX1–DX8','MX1–MX10','PX1–PX10'],
    'case_two_count_retained_cut': ['Literal PMExAlt on the original data'],
    'tower_join_retained_producer': ['Actual rank-four HidaPropsAlt and P1core on the two constructed Links, with one common threshold and all later-coefficient/universal-ring quantifiers'],
    'model_comparison_retained_predicates': ['For Ctx2, YX1 supplies Fin0 and NoEnd from PMExAlt and YX2 applies actual RX6 rigidity pointwise on the same datum.'],
    'literal_RigiditySymplecticFour_supplied': True,
    'source_rigSp4_alt_implication_supplied_by_stronger_endpoint': True,
    'source_rigSp4_alt_original_producer_reconstructed': False,
    'entire_AdjointLiftingTheorem_supplied': True,
    'entire_UnramifiedInputs_package_supplied': False,
    'entire_HypothesesHprime_ModUAlt_HidaUAlt_packages_supplied': False,
    'LevEx_LocCFTAll_LamEx_PhiAll_ProModularRingExists_supplied': True,
    'universal_Pair_original_nonempty_antecedent_retained': True,
    'entire_CohomologyHyp_supplied': True,
    'entire_BlochKatoLocal_supplied': True,
    'classical_leaf_scope': 'Precisely matched named classical local and automorphic theorems, with the original source interfaces explicitly transported.',
    'actual_arithmetic_deformation_model_installed': True,
    'integral_formal_smoothness_claimed': False,
    'actual_rank_four_symplectic_catalogue_supplied': True,
    'all_rank_CountQAlt_or_unchanged_level_LevelPNAlt_supplied': False,
    'actual_ImageDense_supplied': False,
    'actual_case_two_ImageDense_conditional_on_PMExAlt_closed': True,
    'literal_SeedIIAlt_supplied': True,
    'literal_SeedIVAlt_supplied': False,
    'literal_case_two_ProModAlt_from_PMExAlt_closed': True,
    'literal_case_three_ProModAlt_supplied': False,
    'literal_PMExAlt_unconditionally_supplied': False,
    'literal_CountII_from_PMExAlt_closed': True,
    'CountII_and_CountIII_conditional_on_ImageDense_closed': True,
    'CountII_and_CountIII_unconditionally_supplied': False,
    'complete_original_field_count_to_window_assembly': ['YX2','JX2','HV1–HV10','TW8','OB8','VW3','VW4'],
    'PointHV_supplied_counts': ['CountZ','CountVs','CountIV'],
    'PointHV_counts_supplied_conditionally_on_ImageDense': ['CountII','CountIII'],
    'PointHV_counts_supplied_conditionally_on_PMExAlt': ['CountII'],
    'PointHV_retained_counts': ['CountI','CountIII','CountV'],
    'PointHV_retained_other_input': 'PMExAlt',
    'prior_JX_height_cut_preserved': ['CountI','CountV','SymplecticFourImageDense'],
    'window_retained_additional_inputs': 'Previously stated prime-pair hypotheses and actual host installation.',
    'PointHV_original_field_case_layer_sum_assembly_retained': False,
    'unconditional_actual_family_LinkN_closed': False,
    'full_RH_GRH_closed': False,
}
checkpoint['current_deliverable'] = {
    'main': tex.name, 'archive': 'RH_reconstruction_v0_29.zip',
    'audit': 'RH_dependency_audit_v0_29.txt', 'pdf_generated': False,
    'reason': 'The user prioritizes proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.',
}
coverage = read(REVIEW / 'mathematical_review_coverage_v0_29.json')
checkpoint['validation'] = {
    **audit, 'tex': texcheck,
    'mathematical_review_coverage': 'reviews_v0_29/mathematical_review_coverage_v0_29.json',
    'mathematical_reviews': {r['review']: r['sha256'] for r in coverage['review_records']},
    'new_claims_independently_reviewed': len(coverage['coverage']),
    'formal_lean_build': False, 'independent_kernel_replay': False,
    'pdf_visual_review_performed': False,
}
write(ROOT / 'continuation_checkpoint.json', checkpoint)

mapping = read(OLD / 'component_filename_map.json')
mapping['note'] = ('Current v0.29 locations use section labels and stable claim IDs; no current page numbers are asserted. '
                   'KX/QX/SX/UX/YX close the exact universal, adjoint, seed and complete conditional case-II chain. '
                   'PMExAlt implies CountII; the actual rank-four Hecke/support producer, Case IV/III and the separate global branches remain. '
                   'The complete predecessor map is preserved in history/version_0_28/component_filename_map.json.')
mapping['version_0_29_component_sections'] = sections
mapping['version_0_29_note'] = (
    'No new PDF. Exact section labels and proof/source ranges identify KX/QX/SX/UX/YX. '
    'SX supplies SeedIIAlt, UX supplies the actual Ctx2 promodular witness and YX closes PMExAlt implies CountII. '
    'KX supplies the universal objects and QX the adjoint/two-Link/five-clause tower join, retaining its '
    'actual rank-four ordinary Hecke/support producer. Case IV/III and the other count/global branches remain.'
)
write(ROOT / 'component_filename_map.json', mapping)

retired = targets.get('version_0_29_replaced_targets', [])
main_outcome = """The complete conditional case-II chain is reconstructed:

    PMExAlt => CountII.

SX8 constructs the literal automorphic seed on every original permissible
tower. Different ordinary refinements at the two ell-adic places exclude
every Eisenstein lift. Fixed-central weight change, an explicit Ribet
lattice, symplectic induction, exact local flags and the correcting
character then produce every original seed clause and residual entry.

UX12 constructs the actual Ctx2 promodular witness from that seed and
PMExAlt. Its proof includes the original towers, lattice normalization,
three polynomial residual links, coefficient-uniform cohomology bounds,
one actual universal Space and flat completions, quantitative component
propagation and exact-residue coefficient descent. It ends at the original
valued point annihilating the actual ideal, with the same multiplier,
ordered inertia characters and fixed embedding.

YX1–YX2 carry this witness through the existing IX, AX/DX/MX/PX, RX,
CX and SP chains to the literal original CountII. The same datum is used
throughout. All constants precede their varying parameters, the factor
two in the trace estimate is retained, and normalized lengths return to
the original coefficient ring. CountII remains conditional on PMExAlt.

KX supplies LevEx, LocCFTAll, LamEx, PhiAll and ProModularRingExists,
with the precise universal maps and the original nonempty-Pair antecedent.
QX supplies the literal AdjointLiftingTheorem and the actual two-Link,
IsPhi and five-clause PMExAlt join. Its remaining arithmetic input is
precisely rank-four HidaPropsAlt ideals plus P1core on those two Links,
with a common threshold before every later coefficient and universal ring.
The supplementary ordinary-support audit identifies the exact Hecke and
patching producers still to reconstruct. No larger all-rank package is
inferred from the selected consequences.

The added sufficient height route is:

    CountI AND CountIII AND CountV AND PMExAlt => PointHV.

The earlier JX route through full image density remains valid.
HV/TW/OB/VW already supply the downstream original-field assembly with
the stated prime-pair hypotheses; Ct=401 retains cutoff exponent 400.

SeedIVAlt and the full case-III promodularity construction remain. The
older continuation targets combine II/IV seeds and II/III promodularity;
their complete scopes are therefore not retired merely because the
case-II chain is now closed. The other actual counts and the separate
common-family, gap, theta/local, denominator and metric/spectral branches
also remain. The full human-readable RH/Dirichlet-GRH proof is unfinished.
"""

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
in history/version_0_28. The reference and semantic graphs are acyclic.
{len(retired)} fully supplied continuation targets are retired with their
original snapshots; partial closures retain their exact remaining scope.

Independent mathematical reviews cover every new endpoint and are bound
to final component texts. Draft-mode TeX syntax and reference checks pass.
No new Lean build, independent kernel replay, PDF or visual review was
performed. The reported formal verification is accepted as background;
retained tasks describe the unfinished human reconstruction.
'''
summary = f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.29
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_29.tex.
The full archive preserves every earlier proof and includes exact proof/source
ledgers, independent mathematical reviews and the current semantic map.

MAIN OUTCOME
{main_outcome}
INTEGRITY AND REVIEW
{integrity}
'''
full_audit = (ROOT / 'dependency_audit_v0_29/audit.txt').read_text()
(ROOT / 'RH_dependency_audit_v0_29.txt').write_text(summary + '\n' + full_audit + '\n' + (ROOT / 'ordinary_support_dependency_audit/audit.txt').read_text() + '\n')

readme = f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.29
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_29.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_29.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_29/obligation_map.json is the finite semantic AND/OR map.
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
Read symplectic_automorphic_seeds/main.tex (SX1–SX8) for the actual
case-II automorphic seed, including its cuspidality, fixed-central
weight change, exact induced lattice and ordered local flags.

Read symplectic_promodular_realization/main.tex (UX1–UX12) for every
step constructing the original case-II promodular witness: towers,
residual lines, uniform bounds, actual spaces, component propagation
and coefficient descent.

Read case_two_installation/main.tex (YX1–YX2) for the complete chain
PMExAlt implies CountII and its guarded height/window consequence.
Its earlier actual model and comparison are AX/DX/MX/PX; BX/IX/RX/CX/SP
supply the cohomology, image transport, rigidity, catalogue and count.

Read symplectic_universal_arithmetic/main.tex (KX1–KX9) for the exact
universal arithmetic packages. Read symplectic_modular_support/main.tex
(QX1–QX10) for the adjoint theorem, actual two Links and five-clause
tower join. ordinary_support_dependency_audit/audit.txt identifies
the exact actual rank-four Hecke/support producer still to reconstruct.

HV/TW/OB/VW supply the unchanged downstream height/window assembly.
The separate common-family, gap, theta/local, denominator and exact
metric/spectral branches retain their original roles.

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

  python backtrack.py KX9 --repo PATH_TO_SOURCE
  python backtrack.py QX10 --repo PATH_TO_SOURCE
  python backtrack.py SX8 --repo PATH_TO_SOURCE
  python backtrack.py UX12 --repo PATH_TO_SOURCE
  python backtrack.py YX2 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_29.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. Current configure,
assemble and merge scripts produce the cumulative text and ledger.
Run finish_metadata_v0_29.py after audit_v0_29.py and validate_tex_v0_29.py;
package with package_v0_29.py. Old-version scripts are historical artifacts;
do not run them against current root metadata. The full Lean checkout is
not redistributed. No fresh Lean compilation or kernel replay is claimed.
'''
(ROOT / 'README.txt').write_text(readme)

scope_report = ('FINAL SCOPE REVIEW — VERSION 0.29\n\n'
                'PASS for the stated human-reconstruction scope.\n\n'
                + main_outcome + '\nEXACT SCOPE CONSTRAINTS\n'
                + numbered(cfg['precision_notes'])
                + '\n\nThis release-scope record summarizes the separately bound mathematical, '
                  'configuration and semantic reviews; source/hash and TeX checks establish '
                  'traceability and syntax, not the truth of unfinished arithmetic suppliers.\n')
(REVIEW / 'final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint': str(ROOT / 'continuation_checkpoint.json'),
                  'audit': str(ROOT / 'RH_dependency_audit_v0_29.txt'),
                  'claims': len(ledger['claims']),
                  'new_claims': ledger['validation']['new_claims']}, indent=2))
