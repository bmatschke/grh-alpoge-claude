#!/usr/bin/env python3
"""Write the checked v0.28 checkpoint and human-readable continuation files."""
from pathlib import Path
import copy
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_27'
REVIEW = ROOT / 'reviews_v0_28'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numbered(items):
    return '\n'.join(f'{i}. {s}' for i, s in enumerate(items, 1))

cfg = read(ROOT / 'increment_v0_28.json')
ledger = read(ROOT / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
audit = read(REVIEW / 'source_verification_v0_28_audit.json')
texcheck = read(ROOT / 'tex_validation.json')
tex = ROOT / 'RH_readable_reconstruction_v0_28.tex'
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
    artifact_version='0.28', predecessor_version='0.27', date=cfg['date'],
    user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and an updated ZIP suffice; no PDF requested.',
    main_note_pages=None, new_section_start_pages={},
    new_section_headings={p: s['title'] for p, s in sections.items()},
    logical_component_page_map=sections, status=cfg['scope'],
    new_in_this_version=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'],
    next_targets=cfg['next_steps'],
    next_source_targets_file='next_source_targets.json',
    previous_source_targets_file='history/version_0_27/next_source_targets.json',
)
checkpoint['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
checkpoint['retained_prior_results_note'] = (
    'Every historical proof and original claim/source field is preserved. Current closures are '
    'additive version_0_28_update annotations and semantic AND/OR map updates. Earlier open-premise '
    'statements must be read with the version-0.28 scope bridge.'
)
checkpoint['precision_constraints'].extend(cfg['precision_notes'])
checkpoint['precision_supersessions'].extend(cfg['new_in_this_version'])
checkpoint['version_0_28_update'] = {
    'local_conclusions': cfg['new_in_this_version'],
    'premise_closures': cfg['claim_updates'],
    'remaining_inputs': cfg['remaining_major_inputs'],
    'semantic_obligation_map': 'dependency_audit_v0_28/obligation_map.json',
    'next_work_packages': 'dependency_audit_v0_28/next_targets.json',
    'complete_cohomology_installation': ['BX1–BX8'],
    'complete_actual_rigidity': ['RX1–RX7'],
    'complete_actual_rank_four_catalogue': ['CX1–CX9'],
    'actual_image_density_subchains': ['IX1–IX10'],
    'complete_conditional_paired_count_and_height_joins': ['JX1–JX2'],
    'inherited_actual_model_and_comparison': ['AX1–AX10','DX1–DX8','MX1–MX10','PX1–PX10'],
    'paired_count_retained_cut': ['Literal SymplecticFourImageDense on the original data'],
    'model_comparison_retained_predicates': ['D.Fin0 and D.NoEnd supplied from ImageDense','D.AllIrr D.RigidAt supplied by RX7 from the same ImageDense automorphy assertion'],
    'literal_RigiditySymplecticFour_supplied': True,
    'source_rigSp4_alt_implication_supplied_by_stronger_endpoint': True,
    'source_rigSp4_alt_original_producer_reconstructed': False,
    'entire_UnramifiedInputs_and_AdjointLifting_packages_supplied': False,
    'entire_CohomologyHyp_supplied': True,
    'entire_BlochKatoLocal_supplied': True,
    'classical_leaf_scope': 'Precisely matched named classical local and automorphic theorems, with the original source interfaces explicitly transported.',
    'actual_arithmetic_deformation_model_installed': True,
    'integral_formal_smoothness_claimed': False,
    'actual_rank_four_symplectic_catalogue_supplied': True,
    'all_rank_CountQAlt_or_unchanged_level_LevelPNAlt_supplied': False,
    'actual_ImageDense_supplied': False,
    'CountII_and_CountIII_conditional_on_ImageDense_closed': True,
    'CountII_and_CountIII_unconditionally_supplied': False,
    'complete_original_field_count_to_window_assembly': ['JX2','HV1–HV10','TW8','OB8','VW3','VW4'],
    'PointHV_supplied_counts': ['CountZ','CountVs','CountIV'],
    'PointHV_counts_supplied_conditionally_on_ImageDense': ['CountII','CountIII'],
    'PointHV_retained_counts': ['CountI','CountV'],
    'PointHV_retained_other_input': 'SymplecticFourImageDense',
    'window_retained_additional_inputs': 'Previously stated prime-pair hypotheses and actual host installation.',
    'PointHV_original_field_case_layer_sum_assembly_retained': False,
    'unconditional_actual_family_LinkN_closed': False,
    'full_RH_GRH_closed': False,
}
checkpoint['current_deliverable'] = {
    'main': tex.name, 'archive': 'RH_reconstruction_v0_28.zip',
    'audit': 'RH_dependency_audit_v0_28.txt', 'pdf_generated': False,
    'reason': 'The user prioritizes proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.',
}
coverage = read(REVIEW / 'mathematical_review_coverage_v0_28.json')
checkpoint['validation'] = {
    **audit, 'tex': texcheck,
    'mathematical_review_coverage': 'reviews_v0_28/mathematical_review_coverage_v0_28.json',
    'mathematical_reviews': {r['review']: r['sha256'] for r in coverage['review_records']},
    'new_claims_independently_reviewed': len(coverage['coverage']),
    'formal_lean_build': False, 'independent_kernel_replay': False,
    'pdf_visual_review_performed': False,
}
write(ROOT / 'continuation_checkpoint.json', checkpoint)

mapping = read(OLD / 'component_filename_map.json')
mapping['version_0_28_component_sections'] = sections
mapping['version_0_28_note'] = (
    'No new PDF. Exact section labels and proof/source ranges identify BX/RX/CX/IX/JX. '
    'Full cohomology, actual rigidity, the exact rank-four catalogue and every paired-count join '
    'are supplied. ImageDense remains the sole paired-count predicate; CountI/CountV/ImageDense '
    'are the selected height/window cut. IX records complete conditional actual-point and '
    'promodular routes with arithmetic producers retained. Global family/gap/theta/metric branches remain.'
)
write(ROOT / 'component_filename_map.json', mapping)

retired = targets.get('version_0_28_replaced_targets', [])
main_outcome = """Three complete supplier chains and their original-count joins have closed.
BX supplies the entire actual BlochKatoLocal, LocalPublishedTheorems and
CohomologyHyp records. It identifies the literal period rings and tensor
invariants, proves both rational and torsion-inclusive integral annihilator
directions on actual cocycle representatives, and installs every containing
record field. The classical local theorems are named and matched precisely.

RX supplies literal RigiditySymplecticFour. It captures actual points and
dual-number maps over finite coefficient fields, proves their full ordinary
finite local condition, and derives cyclotomic irreducibility from the
ordinary weights. The normalized theta*chi^3 polarization, a suitable
imaginary quadratic field and Thorne's adjoint-Selmer vanishing theorem give
an actual sp4 coboundary. RX7 installs this on the same D and common complex
embedding supplied by image density. The original larger UnramifiedInputs
and AdjointLifting packages are bypassed, not claimed as reconstructed.

CX supplies the full SP9 catalogue and literal NumberSp4Alt. Fixed-cell
cohomological bounds, full global automorphic labels, integral arithmetic
Frobenius data, local conductor control and eighteen fixed CM fields give
uniformity before every coefficient prime, field, embedding and finite
family. The original Galois representation retains level M. Only the
auxiliary label set uses M^7, absorbed in fixed exponents A_*=224 and A=225.
The all-rank CountQAlt and unchanged-level LevelPNAlt packages remain
unpromoted; they are not additional premises for this rank-four endpoint.

JX1 joins BX/RX/CX to the complete AX/DX/MX/PX/SP model and count arguments:

    SymplecticFourImageDense => CountII AND CountIII.

This is a complete human proof of that exact conditional implication,
including the original datum, one embedding before every irreducible point,
the factor two in the trace/cotangent estimate, all uniform constants and
normalized return to the original coefficient ring. Image density itself
remains an arithmetic supplier; the two counts are not yet unconditional.

IX reconstructs the actual valued-point and image-density reduction. A
failure of finiteness produces a characteristic-ell curve and an actual
point. The reducible alternatives, integral primitive cocycle and nonsplit
block extension feed the source's strict weak-purity contradiction. IX9
also proves the algebraic finite-weight-module-to-special-fibre supplier
and the full characteristic-ell trace obstruction. IX10 proves the exact
doubled-weight, restriction-irreducibility and literal automorphy transports
from a uniform actual ProModAlt witness. Actual modular quotients, links,
support, potential-modularity records, seeds and component-reaching
constructions remain precisely identified producers.

JX2 now gives the selected height branch the sufficient input:

    CountI AND CountV AND SymplecticFourImageDense => PointHV.

HV10/TW8/OB8/VW already carry these exact premises through every
original-field height/window assembly step, retaining the prime-pair
hypotheses. Ct=401 still gives fixed-pair cutoff exponent 400. CountI and
CountV themselves remain, as does image density.

The common geometric family and arithmetic gap, genuine theta/local
state, actual denominator tables and exact metric/global/spectral
comparisons remain separate obligations. This is a partial human
reconstruction; the full human-readable RH/Dirichlet-GRH proof is unfinished.
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
in history/version_0_27. The reference and semantic graphs are acyclic.
{len(retired)} fully supplied continuation targets are retired with their
original snapshots; partial closures retain their exact remaining scope.

Independent mathematical reviews cover every new endpoint and are bound
to final component texts. Draft-mode TeX syntax and reference checks pass.
No new Lean build, independent kernel replay, PDF or visual review was
performed. The reported formal verification is accepted as background;
retained tasks describe the unfinished human reconstruction.
'''
summary = f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.28
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_28.tex.
The full archive preserves every earlier proof and includes exact proof/source
ledgers, independent mathematical reviews and the current semantic map.

MAIN OUTCOME
{main_outcome}
INTEGRITY AND REVIEW
{integrity}
'''
full_audit = (ROOT / 'dependency_audit_v0_28/audit.txt').read_text()
(ROOT / 'RH_dependency_audit_v0_28.txt').write_text(summary + '\n' + full_audit + '\n')

readme = f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.28
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_28.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_28.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_28/obligation_map.json is the finite semantic AND/OR map.
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
Read bloch_kato_installation/main.tex (BX1–BX8) for the complete actual
local Bloch–Kato and containing cohomology records, including all cochain,
period and integral-lattice transports.

Read symplectic_actual_rigidity/main.tex (RX1–RX7) for actual tangent
cocycles, the ordinary crystalline induction, cyclotomic irreducibility,
normalized polarization and the exact same-datum rigidity endpoint.

Read symplectic_automorphic_catalogue/main.tex (CX1–CX9) for fixed-cell
uniform counting, complete global labels, integral arithmetic Frobenius,
original-level conductor control, CM restriction and literal NumberSp4Alt.

Read symplectic_image_density/main.tex (IX1–IX10) for the actual valued
points, nonsplit block and purity contradiction, finite special-fibre
supplier, trace obstruction and precise ProModAlt transports. Its final
section and registry state the retained arithmetic producers.

Read paired_count_installation/main.tex (JX1–JX2) for every join to the
actual paired counts and reduced PointHV/window sufficient cut. The
underlying original arithmetic model and comparison remain AX/DX/MX/PX;
SP9–SP10 supply the integer-product and numerical count arguments.

HV1–HV10, TW8, OB8 and VW3/VW4 supply the complete downstream height/window
assembly. The independent global LinkN, family, gap and metric/spectral
branches retain their stated hypotheses; WB7–WB8 and AN2/AN3/GH6 remain
the global analytic spine.

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

  python backtrack.py BX8 --repo PATH_TO_SOURCE
  python backtrack.py RX6 --repo PATH_TO_SOURCE
  python backtrack.py CX9 --repo PATH_TO_SOURCE
  python backtrack.py IX10
  python backtrack.py JX1 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_28.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. Current configure,
assemble and merge scripts produce the cumulative text and ledger.
Run finish_metadata_v0_28.py after audit_v0_28.py and validate_tex_v0_28.py;
package with package_v0_28.py. Old-version scripts are historical artifacts;
do not run them against current root metadata. The full Lean checkout is
not redistributed. No fresh Lean compilation or kernel replay is claimed.
'''
(ROOT / 'README.txt').write_text(readme)

scope_report = ('FINAL SCOPE REVIEW — VERSION 0.28\n\n'
                'PASS for the stated human-reconstruction scope.\n\n'
                + main_outcome + '\nEXACT SCOPE CONSTRAINTS\n'
                + numbered(cfg['precision_notes'])
                + '\n\nThis release-scope record summarizes the separately bound mathematical, '
                  'configuration and semantic reviews; source/hash and TeX checks establish '
                  'traceability and syntax, not the truth of unfinished arithmetic suppliers.\n')
(REVIEW / 'final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint': str(ROOT / 'continuation_checkpoint.json'),
                  'audit': str(ROOT / 'RH_dependency_audit_v0_28.txt'),
                  'claims': len(ledger['claims']),
                  'new_claims': ledger['validation']['new_claims']}, indent=2))
