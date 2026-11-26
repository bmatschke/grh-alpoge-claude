#!/usr/bin/env python3
"""Write the audited v0.26 checkpoint and current human-readable entry files."""
from pathlib import Path
import copy
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_25'
REVIEW = ROOT / 'reviews_v0_26'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numbered(items):
    return '\n'.join(f'{i}. {s}' for i, s in enumerate(items, 1))

cfg = read(ROOT / 'increment_v0_26.json')
ledger = read(ROOT / 'provenance.json')
targets = read(ROOT / 'next_source_targets.json')
audit = read(REVIEW / 'source_verification_v0_26_audit.json')
texcheck = read(ROOT / 'tex_validation.json')
tex = ROOT / 'RH_readable_reconstruction_v0_26.tex'
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
    artifact_version='0.26', predecessor_version='0.25', date=cfg['date'],
    user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and an updated ZIP suffice; no PDF requested.',
    main_note_pages=None, new_section_start_pages={},
    new_section_headings={p: s['title'] for p, s in sections.items()},
    logical_component_page_map=sections, status=cfg['scope'],
    new_in_this_version=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'],
    next_targets=cfg['next_steps'],
    next_source_targets_file='next_source_targets.json',
    previous_source_targets_file='history/version_0_25/next_source_targets.json',
)
checkpoint['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
checkpoint['retained_prior_results_note'] = (
    'Every historical proof and original claim/source field is preserved. Current closures are additive '
    'version_0_26_update annotations and semantic AND/OR map updates. Earlier open-premise statements '
    'must be read with the version-0.26 scope bridge.'
)
checkpoint['precision_constraints'].extend(cfg['precision_notes'])
checkpoint['precision_supersessions'].extend(cfg['new_in_this_version'])
checkpoint['version_0_26_update'] = {
    'local_conclusions': cfg['new_in_this_version'],
    'premise_closures': cfg['claim_updates'],
    'remaining_inputs': cfg['remaining_major_inputs'],
    'semantic_obligation_map': 'dependency_audit_v0_26/obligation_map.json',
    'next_work_packages': 'dependency_audit_v0_26/next_targets.json',
    'complete_rank_one_suppliers': ['RV1–RV7', 'BR1–BR7'],
    'complete_universal_algebra_suppliers': ['SP1–SP6', 'FP1–FP8'],
    'conditional_actual_symplectic_join': ['SP7–SP10'],
    'complete_original_field_count_to_window_assembly': ['HV1–HV10', 'TW8', 'OB8', 'VW3', 'VW4'],
    'PointHV_supplied_counts': ['CountZ', 'CountVs', 'CountIV'],
    'PointHV_retained_counts': ['CountI', 'CountII', 'CountIII', 'CountV'],
    'PointHV_original_field_case_layer_sum_assembly_retained': False,
    'universal_deformation_presentation_closed': True,
    'actual_arithmetic_deformation_model_installed': False,
    'actual_symplectic_catalogue_supplied': False,
    'unconditional_actual_family_LinkN_closed': False,
    'full_RH_GRH_closed': False,
}
checkpoint['current_deliverable'] = {
    'main': tex.name, 'archive': 'RH_reconstruction_v0_26.zip',
    'audit': 'RH_dependency_audit_v0_26.txt', 'pdf_generated': False,
    'reason': 'The user prioritizes proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.',
}
coverage = read(REVIEW / 'mathematical_review_coverage_v0_26.json')
checkpoint['validation'] = {
    **audit, 'tex': texcheck,
    'mathematical_review_coverage': 'reviews_v0_26/mathematical_review_coverage_v0_26.json',
    'mathematical_reviews': {r['review']: r['sha256'] for r in coverage['review_records']},
    'new_claims_independently_reviewed': len(coverage['coverage']),
    'formal_lean_build': False, 'independent_kernel_replay': False,
    'pdf_visual_review_performed': False,
}
write(ROOT / 'continuation_checkpoint.json', checkpoint)

mapping = read(OLD / 'component_filename_map.json')
mapping['version_0_26_component_sections'] = sections
mapping['version_0_26_note'] = (
    'No new PDF: section labels and exact proof/source ranges identify the new claims. The current '
    'semantic map closes rank-one and universal algebra suppliers and all original-field PointHV '
    'assembly. Actual CountI/II/III/V and their arithmetic installation remain, as do the independent '
    'global family/gap/local/metric/spectral obligations.'
)
write(ROOT / 'component_filename_map.json', mapping)

retired = targets.get('version_0_26_replaced_targets', [])
summary = f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.26
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_26.tex.
The full archive preserves every earlier proof and includes exact proof/source
ledgers, independent mathematical reviews and the current semantic obligation map.

MAIN OUTCOME
The rank-one and universal algebra branches now reach their literal endpoints:
SoFin, SoV, coefficient independence, LemmaX, CorX, LemmaMprime, LemmaM and
LemmaP. The weighted intersection bound retains its exact factor two. The
universal deformation theorem constructs its ring, grading, generators and
relations from the stated hypotheses; installing those hypotheses on the
actual arithmetic datum is still required.

HV proves complete CountVs and CountIV and all original-field, coefficient,
character, case, layer and finite-prime summation steps to PointHV. The exact
remaining sufficient cohomological cut is therefore:

    CountI AND CountII AND CountIII AND CountV.

HV10 carries that cut through PointHV and the earlier TW8/OB8/VW assembly to
the cohomological-window conclusion. There is no separate open PointHV
assembly task. SP7–SP10 supplies the actual cocycle/cotangent comparison and
complete conditional paired-count join, with the remaining actual data,
model/point-orbit comparison and finite catalogue stated explicitly.

The four actual counts and their remaining arithmetic suppliers are still
unfinished. The common family and arithmetic gap, genuine theta/local state,
actual denominator tables and exact metric/global/spectral comparisons remain.
This is a partial human reconstruction, not a completed human RH/GRH proof.

Current package: {len(ledger['claims'])} stable claims, of which
{ledger['validation']['new_claims']} are new consolidated endpoints;
{len(ledger['source_files'])} indexed source files and
{ledger['validation']['source_link_count']} claim-source ranges.
All {audit['source_files_checked_including_targets']} cited/target source files
and {len(targets['targets'])} active continuation ranges match the pinned Git blobs.
The semantic sufficient-obligation map has {audit['semantic_obligation_nodes']} nodes.
These counts describe navigation and integrity, not completion percentage.

Independent mathematical reviews cover every new endpoint and are bound to
the final component texts. Draft-mode TeX syntax and reference checks pass.
No new Lean build, independent kernel replay, PDF or visual check was performed.
The reported formal verification is accepted as background; retained tasks
describe the unfinished human reconstruction, not alleged formal gaps.

'''
full_audit = (ROOT / 'dependency_audit_v0_26/audit.txt').read_text()
(ROOT / 'RH_dependency_audit_v0_26.txt').write_text(summary + full_audit + '\n')

readme = f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.26
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_26.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_26.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_26/obligation_map.json is the finite semantic AND/OR map.
provenance.json and provenance.txt bind stable claims to exact pinned source
declarations and exact human-proof ranges. next_source_targets.json records
the active frontier. The audit directory contains exact retained count routes.

No new PDF was generated. TeX passed draft-mode syntax and reference checks.
Any historical PDF is an older snapshot and does not contain this increment.

WHAT CLOSED
-----------
{numbered(cfg['new_in_this_version'])}

READING THE NEW PROOF
--------------------
Read rank_one_cohomology/main.tex (RV1–RV7) for arbitrary finite-character
finiteness, actual algebraic-valued vector vanishing and coefficient return.
Read bernoulli_residual_vanishing/main.tex (BR1–BR7) for the exact dyadic
Bernoulli-unit theorem and both-character residual cocycle vanishing.

Read symplectic_count_closure/main.tex (SP1–SP6) for the complete weighted
intersection theorem, including the exact factor two. Then read
framed_deformation_presentation/main.tex (FP1–FP8) for the universal framed
presentation under the original group, local and obstruction hypotheses.
Return to SP7–SP10 for the actual cocycle/cotangent comparison, coefficient
descent, trace product and complete conditional CountII/CountIII arithmetic.
The actual arithmetic data, compatible Model with point-orbit comparison
and precisely quantified finite catalogue remain required.

Finally read point_hv_assembly/main.tex (HV1–HV10). It proves CountVs and
CountIV and all original-field and prime-summation steps. With earlier
CountZ, TW8, OB8 and VW3/VW4, this closes the full implication from the four
actual remaining counts to the cohomological-window conclusion. It retains
odd primes dividing the field degree and the original constants' quantifier order.

The original-family LinkN chain LN1–LN10 remains conditional on actual
denominator tables and the original type/theta/rank identities. It already
supplies the complete scalar/cut/restoration chain with exact cost
d_j log|G| and unchanged cohomological coefficient. Stronger NormChoiceFacts
and Tie4 and exact metric inputs remain separate obligations.

The analytic endpoint remains AN2/AN3/GH6. WB7–WB8 supplies the implication
from the exact arithmetic-gap/character/scalar contract; construction of
that contract on one actual common family is still required.

CURRENT FRONTIER
----------------
{numbered(cfg['remaining_major_inputs'])}

NEXT COMPLETE-CHAIN TARGETS
--------------------------
{numbered(cfg['next_steps'])}

INTEGRITY AND REVIEW
--------------------
All {audit['previous_total_files_preserved']} predecessor files are retained;
the {audit['previous_root_files_archived']} predecessor root files are archived
exactly in history/version_0_25. Every original field of all
{audit['prior_claims']} historical claims, their source arrays and reference
adjacency lists is unchanged. Current premise closures are additive.

The package contains {len(ledger['claims'])} stable claims,
{ledger['validation']['source_link_count']} claim-source ranges and
{len(ledger['source_files'])} indexed source files. Its continuation map has
{len(targets['targets'])} active ranges. {len(retired)} exact completed targets
are retired with their original snapshots and supplier claims recorded.
The current semantic map has {audit['semantic_obligation_nodes']} nodes,
preserves all previous node identities and snapshots every changed node.

All {ledger['validation']['new_claims']} new endpoints received independent
mathematical review. Reviews distinguish argument checks from mechanical
provenance checks. The reference DAG and semantic AND/OR map are acyclic.
Neither is an exhaustive Lean dependency graph or a certificate that the
full human proof is complete. No completion percentage is assigned.

REPRODUCE / CONTINUE
-------------------
From the extracted archive root, with a checkout at the pinned commit:

  python backtrack.py RV7 --repo PATH_TO_SOURCE
  python backtrack.py BR7 --repo PATH_TO_SOURCE
  python backtrack.py SP6 --repo PATH_TO_SOURCE
  python backtrack.py FP8 --repo PATH_TO_SOURCE
  python backtrack.py HV10 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_26.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. The current configure,
assemble and merge scripts produce the cumulative text and ledger. Run
finish_metadata_v0_26.py after audit_v0_26.py and validate_tex_v0_26.py.
Package with package_v0_26.py. Old-version scripts are historical artifacts;
do not run them against current root metadata. The full Lean checkout is
not redistributed. No fresh Lean compilation or kernel replay is claimed.
'''
(ROOT / 'README.txt').write_text(readme)

scope_report = '''FINAL SCOPE REVIEW — VERSION 0.26

PASS for the stated human-reconstruction scope.

RV1–RV7 match arbitrary finite-order characters, all primes, original
decomposition groups and all prescribed local witnesses. Finite-character
restriction controls its possibly ell-divisible quotient; actual cocycle
capture uses Baire on closed subgroups and proved Krasner approximation.
The vector argument supplies an exact global coboundary, not merely a
dense family of approximate coboundaries. Coefficient return includes
nonnested rings and the literal infinite-length convention.

BR1–BR7 prove the exact Bernoulli-unit threshold and original residual
cocycle theorem with its original residue field and tame relative-index
condition. The finite class-field step uses the earlier proved OS1 Jacobi
ideal relation. Inverse-character conventions and both CorX characters
are matched explicitly; no unexplained annihilator package replaces them.

SP1–SP6 prove literal LemmaMprime and LemmaM. The injection in LemmaMprime
is additive and cardinality comparison is justified. The weighted
intersection proof constructs the admissible Rees support, orbit slices,
generic multiplicities and leading-form differences and retains factor two.
SP7 proves the actual shaCoc/mPrime edge on a supplied graded Model;
SP8 returns the exact coefficient data. SP9 proves the trace product from
the precisely quantified finite catalogue. SP10 completes the conditional
paired-count join. Actual data/admissible representations, compatible
weighted Model/point-orbit comparison and the catalogue remain inputs.

FP1–FP8 prove universal LemmaP under the literal profinite PhiCond,
five local-condition axioms and finite framed obstruction hypotheses.
The universal representation, frame, torus grading, tangent identification,
homogeneous presentation and actual obstruction-to-relation construction
are supplied. The theorem does not establish its own arithmetic hypotheses
or install a Model on the actual Raw datum.

HV1–HV10 prove full CountVs and CountIV and all original-field comparison,
case and summation steps from CountI/II/III/V to PointHV. No odd prime dividing
the original field degree is discarded. The direct polynomial error
replaces the combined redAll/lossLe route without asserting its exact
lossAll formula. The error vanishes outside the exceptional set. LayerLe
keeps its unweighted strict-Selmer meaning; all finiteness precedes length
normalization and all constants precede varying hosts and fields.

HV10 with TW8/OB8/VW closes the full cohomological-window implication from
the exact four actual counts. Those four arithmetic suppliers remain;
the separate PointHV assembly task is closed. The actual common family,
arithmetic gap and size/error readings, genuine theta/local state, actual
denominator tables, stronger normalization fields, exact lattice/metric
transport and global/spectral operator comparisons remain substantive.

Independent mathematical reviews cover every new endpoint and are bound
to the final component hashes. Configuration and semantic scope receive
their own reviews. Source and TeX checks establish traceability and syntax,
not the truth of unfinished arithmetic suppliers. No complete human
RH/Dirichlet-GRH proof, Lean build, kernel replay or PDF review is claimed.
'''
(REVIEW / 'final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint': str(ROOT / 'continuation_checkpoint.json'),
                  'audit': str(ROOT / 'RH_dependency_audit_v0_26.txt'),
                  'claims': len(ledger['claims']),
                  'new_claims': ledger['validation']['new_claims']}, indent=2))
