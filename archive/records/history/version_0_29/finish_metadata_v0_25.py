#!/usr/bin/env python3
"""Write the audited v0.25 checkpoint and human-readable entry documents."""
from pathlib import Path
import copy, hashlib, json, re

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'history/version_0_24'
def read(p): return json.loads(p.read_text())
def write(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

cfg = read(ROOT/'increment_v0_25.json')
ledger = read(ROOT/'provenance.json')
nt = read(ROOT/'next_source_targets.json')
audit = read(ROOT/'reviews_v0_25/source_verification_v0_25_audit.json')
texcheck = read(ROOT/'tex_validation.json')
assert audit['result'] == 'PASS'
tex = ROOT/'RH_readable_reconstruction_v0_25.tex'
assert texcheck['tex_sha256'] == sha(tex) and texcheck['pdf_generated'] is False
for name, expected in audit['input_sha256'].items():
    assert sha(ROOT/name) == expected, name

sections = {}
for component in cfg['components']:
    data = read(ROOT/component/'provenance.json')
    text = (ROOT/component/'main.tex').read_text()
    prefix = re.match('[A-Z]+', data['claims'][0]['id'])[0]
    reports = [p for p in ['report.txt', 'report.md'] if (ROOT/component/p).is_file()]
    sections[prefix] = {
        'component': component,
        'title': re.search(r'\\section\{([^}]*)\}', text)[1],
        'section_label': re.search(r'\\label\{([^}]*)\}', text)[1],
        'claims': [c['id'] for c in data['claims']],
        'fragment': component+'/main.tex',
        'expanded_report': component+'/'+reports[0] if reports else None,
        'page_numbers_available': False,
    }

old = read(OLD/'continuation_checkpoint.json')
cp = copy.deepcopy(old)
cp.update(
    artifact_version='0.25', predecessor_version='0.24', date=cfg['date'],
    user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and updated ZIP suffice; no PDF requested.',
    main_note_pages=None, new_section_start_pages={},
    new_section_headings={p:s['title'] for p,s in sections.items()},
    logical_component_page_map=sections, status=cfg['scope'],
    new_in_this_version=cfg['new_in_this_version'],
    remaining_major_inputs=cfg['remaining_major_inputs'], next_targets=cfg['next_steps'],
    next_source_targets_file='next_source_targets.json',
    previous_source_targets_file='history/version_0_24/next_source_targets.json',
)
cp['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
cp['retained_prior_results_note'] = 'Every historical proof and original claim/source field is preserved. Current closures are additive version_0_25_update annotations and semantic AND/OR map updates. Earlier open-premise statements must be read with the version-0.25 scope bridge.'
cp['precision_constraints'].extend(cfg['precision_notes'])
cp['precision_supersessions'].extend(cfg['new_in_this_version'])
cp['version_0_25_update'] = {
    'local_conclusions': cfg['new_in_this_version'],
    'premise_closures': cfg['claim_updates'],
    'remaining_inputs': cfg['remaining_major_inputs'],
    'semantic_obligation_map': 'dependency_audit_v0_25/obligation_map.json',
    'next_work_packages': 'dependency_audit_v0_25/next_targets.json',
    'complete_local_torsion_K_window_chain': ['LK1–LK4','TB1–TB10','KB1–KB8','TW1–TW8'],
    'independent_exceptional_count_chain': ['CZ1–CZ6'],
    'explicit_constants': {'TorsBound':49,'TorsBoundPow':22,'LemmaK':31,'CountZ':0,'earlier_ThmBcFree':240},
    'ThmBab_quantifier_order': 'exists K:BConst, forall Ct>=1, ThmBab K Ct; all original fields and prescribed layer models on the same window',
    'remaining_major_cohomological_supplier_on_selected_VW_route': 'PointHV',
    'PointHV_supplied_inputs': ['LD3','LK2','LK3','KB8','CZ6'],
    'PointHV_retained_counts': ['CountI','CountII','CountIII','CountV'],
    'PointHV_original_field_case_layer_sum_assembly_retained': True,
    'unconditional_actual_family_LinkN_closed': False,
    'full_RH_GRH_closed': False,
}
cp['current_deliverable'] = {
    'main': tex.name, 'archive':'RH_reconstruction_v0_25.zip',
    'audit':'RH_dependency_audit_v0_25.txt', 'pdf_generated':False,
    'reason':'The user prioritizes proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.',
}
coverage = read(ROOT/'reviews_v0_25/mathematical_review_coverage_v0_25.json')
cp['validation'] = {
    **audit, 'tex':texcheck,
    'mathematical_review_coverage':'reviews_v0_25/mathematical_review_coverage_v0_25.json',
    'mathematical_reviews':{r['review']:r['sha256'] for r in coverage['review_records']},
    'new_claims_independently_reviewed':len(coverage['coverage']),
    'formal_lean_build':False,'independent_kernel_replay':False,'pdf_visual_review_performed':False,
}
write(ROOT/'continuation_checkpoint.json', cp)
mapping = read(OLD/'component_filename_map.json')
mapping['version_0_25_component_sections'] = sections
mapping['version_0_25_note'] = 'No new PDF: section labels and exact proof/source ranges identify the new claims. The current semantic map closes the shared local/torsion/K-theory/ThmBab chain and CountZ, while retaining PointHV counts and original-field assembly and every separate global family/gap/local/metric/spectral obligation.'
write(ROOT/'component_filename_map.json', mapping)

full_audit = (ROOT/'dependency_audit_v0_25/audit.txt').read_text()
summary = f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.25
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_25.tex.
The full archive preserves all earlier proofs and includes exact proof/source
ledgers, independent reviews, the semantic obligation map and continuation state.

MAIN OUTCOME
The local/torsion/K-theory/window chain is now complete in its stated classical
theorem scope. LK supplies the exact native local-K interfaces. TB proves the
full all-prime torsion-homology bound, with TorsBound49 and TorsBoundPow22.
KB constructs the actual KBridge and proves one universal LemmaK31. TW proves
the entire simultaneous ThmBab statement, with one BConst chosen before every
Ct>=1, the original two-primary field and every prescribed reference-layer
model controlled on the same window. Separately, CZ proves PropZ and CountZ
by actual vanishing, uniformly with exponent zero.

Together with earlier OB8=ThmBcFree240 and the VW assembly, PointHV is now the
sole remaining major cohomological supplier on that selected route. Its common
local-K and LemmaK inputs and CountZ are supplied. CountI/II/III/V and their
remaining original-field case/layer/sum assembly are explicitly retained.
The actual common family and arithmetic gap, genuine theta/local installation,
actual denominator tables, and exact metric/global/spectral suppliers remain.

Current package: {len(ledger['claims'])} stable claims, of which
{ledger['validation']['new_claims']} are new consolidated endpoints;
{len(ledger['source_files'])} indexed source files and
{ledger['validation']['source_link_count']} claim-source ranges.
All {audit['source_files_checked_including_targets']} cited/target source files
and {len(nt['targets'])} active continuation ranges match the pinned Git blobs.
The finite semantic sufficient-obligation map has {audit['semantic_obligation_nodes']}
nodes. These counts describe navigation and integrity, not completion percentage.
Independent mathematical reviews cover all new endpoints and are bound to
the final component texts. Draft-mode TeX syntax and reference checks pass.
No new Lean build, kernel replay, PDF or visual layout check was performed.

The user's report of formal verification is accepted as background.
The remaining obligations concern the unfinished human reconstruction;
they are not alleged gaps in the formal development.

'''
(ROOT/'RH_dependency_audit_v0_25.txt').write_text(summary+full_audit+'\n')

readme = f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.25
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_25.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_25.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_25/obligation_map.json is the finite semantic AND/OR map.
provenance.json and provenance.txt bind stable claims to exact pinned source
declarations and exact human-proof ranges. next_source_targets.json records
the active frontier. count_frontier_sources.json in the new audit directory
identifies the deeper actual arithmetic routes for the four remaining counts.

No new PDF was generated. TeX passed draft-mode syntax and reference checks.
Any historical PDF is an older snapshot and does not contain this increment.

WHAT CLOSED
-----------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['new_in_this_version']))}

READING THE NEW PROOF
--------------------
Read local_k_duality/main.tex (LK1–LK4) and torsion_homology/main.tex
(TB1–TB10), then k_theory_bridge/main.tex (KB1–KB8), then
simultaneous_cohomological_windows/main.tex (TW1–TW8).
These chapters close the entire shared quantitative-cohomology and
simultaneous-window supplier, relative to the precisely identified classical
theorems. The torsion argument retains every prime; its exponent 22 becomes
31 in the K-theory/cohomology reduction. The final constant record is chosen
before all Ct>=1, and all original field-model quantifiers are retained.

Read count_z_closure/main.tex (CZ1–CZ6) independently for the exceptional
odd-plus count. Cyclotomic inertia, an explicit quadratic class-number estimate
and cocycle normalization prove actual vanishing, so CountZ holds with C=0.

For immediate downstream use, return to VW3/VW4 in
analytic_chain_closure/main.tex. TW8 supplies ThmBab, earlier OB8 supplies
ThmBcFree240, and PointHV remains their only major cohomological premise.
Its CountI/II/III/V and original-field assembly remain open in the human text.
Classical prime-pair inputs and actual host installation retain their roles.

The independent original-family LinkN chain LN1–LN10 remains conditional on
actual local denominator tables and the original type/theta/rank identities.
It already supplies integral algebra, complete prime summation and restoration
cost d_j log|G| with unchanged cohomological coefficient. Stronger
NormChoiceFacts/Tie4 and exact metric inputs remain separate obligations.

The analytic endpoint remains AN2/AN3/GH6. WB7–WB8 supplies the implication
from the exact arithmetic-gap/character/scalar contract. Construction of that
contract on one actual common arithmetic family is still required.

CURRENT FRONTIER
----------------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['remaining_major_inputs']))}

NEXT COMPLETE-CHAIN TARGETS
--------------------------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['next_steps']))}

The new audit compares the CountI, paired CountII/CountIII, and CountV routes.
The paired CountII/III route shares one rank-four construction, but its actual
rigidity, automorphy, congruence and normalized cohomology suppliers remain
substantive. Their wrappers are not promoted to classical citation leaves.
Native non-K and normalized automorphic cohomology interfaces require their
own matching; LK alone does not close every similarly named interface.

INTEGRITY AND REVIEW
--------------------
All {audit['previous_total_files_preserved']} predecessor files are retained;
the {audit['previous_root_files_archived']} predecessor root files are archived
exactly in history/version_0_24. Every original field of all
{audit['prior_claims']} historical claims, their source arrays and reference
adjacency lists is unchanged. Current premise closures are additive.

The package contains {len(ledger['claims'])} stable claims,
{ledger['validation']['source_link_count']} claim-source ranges and
{len(ledger['source_files'])} indexed source files. Its continuation map has
{len(nt['targets'])} active ranges. Ten completed source targets are retired
with original snapshots and exact supplier claims recorded. The current map
has {audit['semantic_obligation_nodes']} nodes, preserves all older node identities
and retains exact snapshots of changed nodes. The historical stale node-count
field is preserved in its snapshot; the current count is computed correctly.

All {ledger['validation']['new_claims']} new endpoints received independent
mathematical review. Reviews distinguish argument checks from mechanical
provenance checks. Source/proof hashes and unchanged history were checked.
The reference DAG and semantic AND/OR map are acyclic. Neither is an exhaustive
Lean dependency graph or a certificate that the full human proof is complete.

REPRODUCE / CONTINUE
-------------------
From the extracted archive root, with a checkout at the pinned commit:

  python backtrack.py TB10 --repo PATH_TO_SOURCE
  python backtrack.py KB8 --repo PATH_TO_SOURCE
  python backtrack.py TW8 --repo PATH_TO_SOURCE
  python backtrack.py CZ6 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_25.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. The current configure,
assemble and merge scripts produce the cumulative text and ledger. Run
finish_metadata_v0_25.py after audit_v0_25.py and validate_tex_v0_25.py.
Package with package_v0_25.py. Old-version scripts are historical artifacts;
do not run them against current root metadata. The full Lean checkout is not
redistributed. No fresh Lean compilation or kernel replay is claimed.
'''
(ROOT/'README.txt').write_text(readme)

scope_report = '''FINAL SCOPE REVIEW — VERSION 0.25

PASS for the stated human-reconstruction scope.

LK1–LK4 match the exact original local-K fields, roots and cochains. All four
local Tate cup-product bijections allow nonfree finite modules; the Euler
factor includes residue characteristic and the prime two. This does not
automatically discharge differently normalized non-K cohomology packages.

TB1–TB10 prove the full all-prime torsion supplier from the actual ordered
perfect-form nerve. The integral spectral sequence retains stabilizer torsion.
The finite cover/acyclicity, row-module orbit count, inverse-Hermitian vector
bound and torsion-free level-three kernel are proved. The endpoints are
TorsBound49 and TorsBoundPow22, with the original degree and discriminant.

KB1–KB8 construct the actual finite K-theory module and comparison maps.
Finite-coefficient Dwyer–Friedlander, inverse limits, Arlettaz's actual GL
Hurewicz target and van der Kallen stability are matched in their precise
scopes. The original decomposition groups are transported to native local
fields. Finite global/local duality and elementary finite-module estimates
then give the universal LemmaK31. No universal arbitrary Plus/KPublished
comparison is inferred from the canonical construction.

TW1–TW8 give the full literal ThmBab supplier. Ferrero–Washington is converted
to the required all-layer finite ranks, including two. The q,d-uniform
generator bound, strict twisted coinvariants, finite duality and limit maps,
p-adic centers, exceptional twists, simultaneous window, field models and
quantitative absorption are all proved. One BConst precedes every Ct>=1.
The original E and separately quantified layer models are controlled on the
same interval and fixed prime pair; they are not identified as fields.

CZ1–CZ6 prove literal PropZ and CountZ by vanishing, with uniform exponent
zero. The proof uses actual cyclotomic inertia, residual trivial/quadratic
cocycles, every original local condition and an explicit quadratic
class-number estimate. It is stronger than a finite-dimensional rank bound.

Substitution of TW8 and earlier OB8 into VW3/VW4 leaves PointHV as the sole
major cohomological supplier on this selected route. PointHV's shared
local-K, LemmaK and CountZ inputs are supplied; CountI/II/III/V and remaining
original-field case/layer/sum assembly are still needed. Prime-pair and actual
host assumptions retain their stated roles.

The actual common family, arithmetic gap and size/error readings, genuine
theta/toric/local data, actual denominator tables, stronger NormChoiceFacts/
Tie4 fields, exact lattice-metric transport and global/spectral comparisons
remain substantive. Earlier conditional LinkN and analytic implications are
preserved with their exact assumptions. No complete RH/Dirichlet-GRH human
proof or completion percentage is asserted.

Independent argument reviews cover every new endpoint and are bound to the
final component hashes. The configuration and semantic scope receive their
own independent reviews. Source and TeX checks establish traceability and
syntax, not the truth of unfinished arithmetic suppliers. No new Lean build,
kernel replay or PDF visual check was performed.
'''
(ROOT/'reviews_v0_25/final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint':str(ROOT/'continuation_checkpoint.json'),
                  'audit':str(ROOT/'RH_dependency_audit_v0_25.txt'),
                  'claims':len(ledger['claims']),
                  'new_claims':ledger['validation']['new_claims']},indent=2))
