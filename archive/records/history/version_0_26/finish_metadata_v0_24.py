#!/usr/bin/env python3
"""Write the audited v0.24 checkpoint and readable entry documents."""
from pathlib import Path
import copy,hashlib,json,re

ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_23'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=read(ROOT/'increment_v0_24.json');ledger=read(ROOT/'provenance.json');nt=read(ROOT/'next_source_targets.json')
audit=read(ROOT/'reviews_v0_24/source_verification_v0_24_audit.json');texcheck=read(ROOT/'tex_validation.json')
assert audit['result']=='PASS'
tex=ROOT/'RH_readable_reconstruction_v0_24.tex'
assert texcheck['tex_sha256']==sha(tex) and texcheck['pdf_generated'] is False
for name,value in audit['input_sha256'].items():assert sha(ROOT/name)==value,name
sections={}
for component in cfg['components']:
 d=read(ROOT/component/'provenance.json');text=(ROOT/component/'main.tex').read_text()
 prefix=re.match('[A-Z]+',d['claims'][0]['id'])[0]
 reports=[p for p in ['report.txt','report.md'] if (ROOT/component/p).is_file()]
 sections[prefix]={'component':component,'title':re.search(r'\\section\{([^}]*)\}',text)[1],'section_label':re.search(r'\\label\{([^}]*)\}',text)[1],'claims':[c['id'] for c in d['claims']],'fragment':component+'/main.tex','expanded_report':component+'/'+reports[0] if reports else None,'page_numbers_available':False}
old=read(OLD/'continuation_checkpoint.json');cp=copy.deepcopy(old)
cp.update(artifact_version='0.24',predecessor_version='0.23',date=cfg['date'],user_instruction='Continue with full effort toward the full human reconstruction; prioritize complete dependency chains, allow proved simplifications and maintain an explicit dependency audit. TeX and updated ZIP suffice; no PDF requested.',main_note_pages=None,new_section_start_pages={},new_section_headings={p:s['title'] for p,s in sections.items()},logical_component_page_map=sections,status=cfg['scope'],new_in_this_version=cfg['new_in_this_version'],remaining_major_inputs=cfg['remaining_major_inputs'],next_targets=cfg['next_steps'],next_source_targets_file='next_source_targets.json',previous_source_targets_file='history/version_0_23/next_source_targets.json')
cp['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
cp['retained_prior_results_note']='Every historical proof and original claim/source field is preserved. Current premise closures are additive version_0_24_update annotations and semantic AND/OR map updates. Earlier open-premise statements must be read with the version-0.24 scope bridge.'
cp['precision_constraints'].extend(cfg['precision_notes']);cp['precision_supersessions'].extend(cfg['new_in_this_version'])
cp['version_0_24_update']={'local_conclusions':cfg['new_in_this_version'],'premise_closures':cfg['claim_updates'],'remaining_inputs':cfg['remaining_major_inputs'],'semantic_obligation_map':'dependency_audit_v0_24/obligation_map.json','next_work_packages':'dependency_audit_v0_24/next_targets.json','complete_odd_minus_chain':['LD1–LD4','OS1–OS9','OB1–OB8'],'odd_minus_constant':240,'remaining_bespoke_cohomological_cut':['ThmBab','PointHV'],'unconditional_actual_family_LinkN_closed':False,'full_RH_GRH_closed':False}
cp['current_deliverable']={'main':tex.name,'archive':'RH_reconstruction_v0_24.zip','audit':'RH_dependency_audit_v0_24.txt','pdf_generated':False,'reason':'The user prioritizes human proof reconstruction and complete chains; the cumulative TeX is sufficient for continuation.'}
coverage=read(ROOT/'reviews_v0_24/mathematical_review_coverage_v0_24.json')
cp['validation']={**audit,'tex':texcheck,'mathematical_review_coverage':'reviews_v0_24/mathematical_review_coverage_v0_24.json','mathematical_reviews':{r['review']:r['sha256'] for r in coverage['review_records']},'new_claims_independently_reviewed':len(coverage['coverage']),'formal_lean_build':False,'independent_kernel_replay':False,'pdf_visual_review_performed':False}
write(ROOT/'continuation_checkpoint.json',cp)
mapping=read(OLD/'component_filename_map.json');mapping['version_0_24_component_sections']=sections
mapping['version_0_24_note']='No new PDF: section labels and exact source/proof ranges identify all claims. The standalone audit and finite semantic AND/OR map distinguish the completed odd-minus supplier from the conditional LinkN chain and its actual arithmetic inputs.'
write(ROOT/'component_filename_map.json',mapping)

full_audit=(ROOT/'dependency_audit_v0_24/audit.txt').read_text()
summary=f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.24
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The cumulative proof text is RH_readable_reconstruction_v0_24.tex.
The full archive preserves all prior proofs and includes exact proof/source
ledgers, the semantic obligation map and the continuation checkpoint.

Main outcome: the entire odd-minus supplier is now written through from
finite duality and Jacobi elements to literal PsiBound and ThmBcFree, with
explicit uniform constant 240. The remaining bespoke cohomological cut in
the VW route is ThmBab plus PointHV. The integral congruence, prime-sum and
cut-restoration chain to original-family LinkN is complete conditionally;
its actual local arithmetic tables and type/theta/rank inputs remain.

Current package: {len(ledger['claims'])} stable claims, of which
{ledger['validation']['new_claims']} are new consolidated endpoints;
{len(ledger['source_files'])} indexed source files and
{ledger['validation']['source_link_count']} claim-source ranges.
All {audit['source_files_checked_including_targets']} cited/target source files
and {len(nt['targets'])} active continuation ranges match the pinned Git blobs.
These are navigation and integrity counts, not a completion percentage.
Independent mathematical reviews cover all new endpoints and are bound
to their final component text hashes. Draft-mode TeX syntax and references
pass. No new Lean build, kernel replay, PDF or visual layout check was done.

The user's report of formal verification is accepted as background.
Remaining obligations below describe the unfinished human reconstruction;
they are not alleged gaps in the formal development.

'''
(ROOT/'RH_dependency_audit_v0_24.txt').write_text(summary+full_audit+'\n')

readme=f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.24
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_24.tex is the complete cumulative TeX file.
RH_dependency_audit_v0_24.txt explains the closed chains and current frontier.
continuation_checkpoint.json is the machine-readable continuation state.
dependency_audit_v0_24/obligation_map.json is the finite semantic AND/OR map.
provenance.json and provenance.txt bind stable claims to exact pinned source
declarations and exact human-proof ranges. next_source_targets.json records
the active source frontier, with successor targets inside the remaining
cohomological and local-denominator suppliers.

No new PDF was generated. TeX passed draft-mode syntax and reference checks.
Any historical PDF is an older snapshot and does not contain this increment.

WHAT CLOSED
-----------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['new_in_this_version']))}

READING THE NEW PROOF
--------------------
Read local_duality_closure/main.tex (LD1–LD4), then
odd_minus_supplier/main.tex (OS1–OS9), then
odd_minus_bounds/main.tex (OB1–OB8).
These form one complete finite-duality-to-odd-minus chain, relative to the
precise standard classical theorems identified in their input registries.
The exact quantitative endpoint has uniform constant 240. Then read VW3
and VW4 in analytic_chain_closure/main.tex for its immediate downstream use.

Read congruence_chain/main.tex (LN1–LN10) for the independent conditional
local-to-global denominator chain. Its local arithmetic tables and actual
type/theta/rank identities remain inputs; its finite linear algebra,
all-prime summation and exact restoration to the original family are proved.
The restoration cost is d_j log|G| and leaves the cohomological coefficient
unchanged. Full CutGivesAlt is not inferred from CutD.Good.

The final analytic endpoint remains AN2/AN3/GH6, with its certificate in
analytic_chain_closure/analytic_endpoint_certificate.json. WB7–WB8 gives
the full arithmetic-gap/character/scalar implication. Actual construction
of that common arithmetic contract is still required.

CURRENT FRONTIER
----------------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['remaining_major_inputs']))}

NEXT COMPLETE-CHAIN TARGETS
--------------------------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['next_steps']))}

INTEGRITY AND REVIEW
--------------------
All {audit['previous_total_files_preserved']} predecessor files are retained;
the {audit['previous_root_files_archived']} predecessor root files are archived
exactly in history/version_0_23. Every original field of all
{audit['prior_claims']} historical claims, their source arrays and reference
adjacency lists is unchanged. Current premise closures are additive.

The package contains {len(ledger['claims'])} stable claims,
{ledger['validation']['source_link_count']} claim-source ranges and
{len(ledger['source_files'])} indexed source files. Its continuation map has
{len(nt['targets'])} active ranges. Exactly three obsolete source targets
were retired: literal PsiBound, the full thmBcFree_of supplier, and the
stated conditional linkN_of_gd transport. The stronger actual-family
LinkN supplier targets remain, with their scope narrowed explicitly.

All {ledger['validation']['new_claims']} new endpoints received independent
mathematical review. Review records distinguish argument checks from
mechanical provenance checks. All source/proof hashes and unchanged
history were checked. The reference graph is acyclic, but is not an
exhaustive Lean dependency graph or a proof-completion certificate.

REPRODUCE / CONTINUE
-------------------
From the extracted archive root, with a checkout at the pinned commit:

  python backtrack.py OS9 --repo PATH_TO_SOURCE
  python backtrack.py OB8 --repo PATH_TO_SOURCE
  python backtrack.py LN10 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_24.py --repo PATH_TO_SOURCE

Each new component includes its provenance builder. The current configure,
assemble and merge scripts produce the cumulative text and ledger. Run
finish_metadata_v0_24.py only after audit_v0_24.py and
validate_tex_v0_24.py. Package with package_v0_24.py.
Old-version scripts are retained as historical artifacts; do not run them
against current root metadata. The full Lean checkout is not redistributed.
No fresh compilation or kernel replay is claimed by these checks.
'''
(ROOT/'README.txt').write_text(readme)

scope_report='''FINAL SCOPE REVIEW — VERSION 0.24

PASS for the explicitly stated human-reconstruction scope.

LD1–LD4 supply the literal finite unramified orthogonality and published
Poitou–Tate interfaces relative to precise classical theorems. The sign,
primitive-root conjugation, finite nonfree coefficients, quantifier order
and archimedean Tate conventions are matched. This is not a blanket
assertion about all stronger K-theoretic duality/finiteness interfaces.

OS1–OS9 and OB1–OB8 supply the entire odd-minus branch. All bespoke finite
Jacobi/Kolyvagin, reciprocity, length, special-value, coefficient, negative-
twist and quantitative ingredients needed for PsiBound and ThmBcFree are
proved. OS9 supplies OB3; OS1 supplies OB5 with the exact inverse-oriented
factor-two identity. No circular Bernoulli nonvanishing premise is used.
The numerical constant is 240 and is uniform over the original fields,
local data, twists and finite sets of odd primes.

Substitution in VW3–VW4 leaves ThmBab and PointHV as the two bespoke
cohomological suppliers. The two/plus/minus outputs concern the same
original E, while every prescribed cyclotomic layer model is controlled
on the same parameter window and fixed pair. Classical prime-pair inputs
and actual host installation remain required.

LN1–LN10 close integral cut construction from actual type identities,
the congruence filtration and normalized kernel loss, complete prime-table
summation and restoration to the original family. Actual local Galois
tables, original type/theta/rank identities and stronger NormChoiceFacts/
Tie4 fields remain explicit. Unconditional actual-family LinkN is not
claimed; exact metric and remaining global/spectral suppliers are retained.

The historical mathematical proofs and their original hypotheses are
preserved. Current opening, scope bridge, audit section and remaining-work
text identify the newly discharged odd-minus premise and narrowed local
frontier. The full arithmetic family/gap and other global suppliers remain.
No full RH/Dirichlet-GRH reconstruction or completion percentage is claimed.

Independent argument reviews cover every new endpoint and are bound to
final component hashes. Source and syntax checks establish traceability,
not the truth of unfinished arithmetic suppliers. No new Lean build,
kernel replay or PDF visual check was performed.
'''
(ROOT/'reviews_v0_24/final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint':str(ROOT/'continuation_checkpoint.json'),'audit':str(ROOT/'RH_dependency_audit_v0_24.txt'),'claims':len(ledger['claims']),'new_claims':ledger['validation']['new_claims']},indent=2))
