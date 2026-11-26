#!/usr/bin/env python3
"""Write the continuation checkpoint and concise entry documents."""
from pathlib import Path
import copy,hashlib,json,re

ROOT=Path(__file__).resolve().parent;OLD=ROOT/'history/version_0_22'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=read(ROOT/'increment_v0_23.json');ledger=read(ROOT/'provenance.json');nt=read(ROOT/'next_source_targets.json')
audit=read(ROOT/'reviews_v0_23/source_verification_v0_23_audit.json');texcheck=read(ROOT/'tex_validation.json')
assert audit['result']=='PASS'
tex=ROOT/'RH_readable_reconstruction_v0_23.tex'
assert texcheck['tex_sha256']==sha(tex) and texcheck['pdf_generated'] is False
for name,value in audit['input_sha256'].items():assert sha(ROOT/name)==value,name
sections={}
for component in cfg['components']:
 d=read(ROOT/component/'provenance.json');text=(ROOT/component/'main.tex').read_text()
 prefix=re.match('[A-Z]+',d['claims'][0]['id'])[0]
 reports=[p for p in ['report.txt','report.md','audit_draft.md'] if (ROOT/component/p).is_file()]
 sections[prefix]={'component':component,'title':re.search(r'\\section\{([^}]*)\}',text)[1],'section_label':re.search(r'\\label\{([^}]*)\}',text)[1],'claims':[c['id'] for c in d['claims']],'fragment':component+'/main.tex','expanded_report':component+'/'+reports[0] if reports else None,'page_numbers_available':False}
old=read(OLD/'continuation_checkpoint.json');cp=copy.deepcopy(old)
cp.update(artifact_version='0.23',predecessor_version='0.22',date=cfg['date'],user_instruction='Continue with full effort; prioritize complete dependency chains and a useful dependency audit; TeX and updated ZIP are sufficient, no new PDF requested.',main_note_pages=None,new_section_start_pages={},new_section_headings={p:s['title'] for p,s in sections.items()},logical_component_page_map=sections,status=cfg['scope'],new_in_this_version=cfg['new_in_this_version'],remaining_major_inputs=cfg['remaining_major_inputs'],next_targets=cfg['next_steps'],next_source_targets_file='next_source_targets.json',previous_source_targets_file='history/version_0_22/next_source_targets.json')
cp['retained_prior_results'].extend(copy.deepcopy(old['new_in_this_version']))
cp['retained_prior_results_note']='Historical results, original claim fields, source arrays and adjacency lists are preserved. Current closures are additive in version_0_23_update and dependency_audit_v0_23/obligation_map.json. Historical statements about now-supplied premises must be read with these scope updates.'
cp['precision_constraints'].extend(cfg['precision_notes'])
cp['precision_supersessions'].extend(cfg['new_in_this_version'])
cp['version_0_23_update']={'local_conclusions':cfg['new_in_this_version'],'premise_closures':cfg['claim_updates'],'remaining_inputs':cfg['remaining_major_inputs'],'semantic_obligation_map':'dependency_audit_v0_23/obligation_map.json','next_work_packages':'dependency_audit_v0_23/next_targets.json'}
cp['current_deliverable']={'main':tex.name,'archive':'RH_reconstruction_v0_23.zip','audit':'RH_dependency_audit_v0_23.txt','pdf_generated':False,'reason':'The user requested proof reconstruction and dependency closure; self-contained TeX is sufficient for continuation.'}
coverage=read(ROOT/'reviews_v0_23/mathematical_review_coverage_v0_23.json')
cp['validation']={**audit,'tex':texcheck,'mathematical_review_coverage':'reviews_v0_23/mathematical_review_coverage_v0_23.json','mathematical_reviews':{r['review']:r['sha256'] for r in coverage['review_records']},'new_claims_independently_reviewed':len(coverage['coverage']),'formal_lean_build':False,'independent_kernel_replay':False,'pdf_visual_review_performed':False}
write(ROOT/'continuation_checkpoint.json',cp)
mapping=read(OLD/'component_filename_map.json')
mapping['version_0_23_component_sections']=sections
mapping['version_0_23_note']='No new PDF: section labels and exact proof/source locators, rather than invented page numbers, identify this increment. The standalone audit and finite AND/OR map record semantic dependencies separately from the unchanged historical reference graph.'
write(ROOT/'component_filename_map.json',mapping)

full_audit=(ROOT/'dependency_audit_v0_23/audit_draft.md').read_text()
summary=f'''RH / DIRICHLET-GRH RECONSTRUCTION — VERSION 0.23
DEPENDENCY AUDIT AND CONTINUATION MILESTONE
22 November 2026

The complete cumulative proof text is RH_readable_reconstruction_v0_23.tex.
The archive includes all historical proofs and the full source/proof ledgers.

Current audited package: {len(ledger['claims'])} stable claims, of which
{ledger['validation']['new_claims']} are new consolidated endpoints; {len(ledger['source_files'])}
indexed source files and {ledger['validation']['source_link_count']} claim-source
ranges. These are navigation/integrity counts, not a completion percentage.
Every cited file and active continuation range matches the pinned Git blobs.
All new chains have independent human mathematical reviews tied to their
frozen text hashes. No new Lean build, kernel replay or PDF was performed.

The formal source's reported verification is treated as background.
The remaining obligations below describe what is still absent from this
human reconstruction, not alleged omissions in the formal development.

'''
(ROOT/'RH_dependency_audit_v0_23.txt').write_text(summary+full_audit+'\n')

readme=f'''RH AND DIRICHLET-GRH — HUMAN-READABLE RECONSTRUCTION v0.23
========================================================
Date: 22 November 2026
Pinned source: {ledger['commit']}
Repository: {ledger['repository']}

START HERE
----------
RH_readable_reconstruction_v0_23.tex is the cumulative, self-contained TeX.
RH_dependency_audit_v0_23.txt is the readable audit and next-work guide.
continuation_checkpoint.json is the machine-readable checkpoint.
dependency_audit_v0_23/obligation_map.json is the finite semantic AND/OR map.
provenance.json and provenance.txt bind stable claim IDs to exact source
declarations, ranges and hashes. next_source_targets.json records the active
source frontier; its new rows belong to two complete-chain work packages.

No new PDF was generated. TeX passed draft-mode syntax and reference checks.
The historical PDF, if used, is explicitly an older snapshot and does not
contain this increment.

WHAT CLOSED
-----------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['new_in_this_version']))}

HOW TO READ THE STATUS
---------------------
HP's elementary representation theorem is a newly discharged substantive
leaf. VW and WB are complete downstream implications from explicitly stated
arithmetic inputs. DA explains how uniform conditions can be joined on one
family, while keeping the actual suppliers as separate obligations.

The final analytic endpoint was already complete in AN2/AN3/GH6; its
certificate is analytic_chain_closure/analytic_endpoint_certificate.json.
No missing Fourier or scalar calculation is hidden behind the new WB
contract. The remaining challenge is to construct that contract and the
cohomological/geometric suppliers on the original maps and fields.

CURRENT FRONTIER
----------------
{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(cfg['remaining_major_inputs']))}

NEXT COMPLETE-CHAIN TARGETS
--------------------------
First pursue one full deep cohomological supplier, most concretely the
odd-minus ThmBcFree/PsiBound route, and integrate it into VW. The broader
cohomological route also needs ThmBab and PointHV on the same field/windows.
The second work package is full LinkN on an actual family, including the
cut-family-to-original-family transport. The exact eight constituent source
anchors and all retained premises are in dependency_audit_v0_23/next_targets.json.
These are two work packages, not eight independent claim-count targets.

INTEGRITY AND REVIEW
--------------------
All {audit['previous_total_files_preserved']} predecessor files are retained;
the {audit['previous_root_files_archived']} prior root files are archived in
history/version_0_22. Every original field of all {audit['prior_claims']}
earlier claims and all their source arrays/graph adjacency lists is unchanged.
Current premise closures are additive version_0_23_update annotations.

There are {len(ledger['claims'])} stable claims, {ledger['validation']['source_link_count']}
claim-source ranges and {len(ledger['source_files'])} indexed source files.
The active continuation map has {len(nt['targets'])} ranges. Nine obsolete
continuation anchors were retired after their exact conditional/local
endpoints were proved; their deep suppliers remain separately recorded.

Independent mathematical reviews cover all {ledger['validation']['new_claims']}
new endpoints. Exact source/proof hashes and unchanged history were checked.
The reference graph is acyclic, but is not an exhaustive Lean dependency
graph and is not a certificate that all mathematical premises are discharged.

REPRODUCE / CONTINUE
-------------------
From the extracted archive root, with a checkout at the pinned commit:

  python backtrack.py HP6 --repo PATH_TO_SOURCE
  python backtrack.py WB7 --repo PATH_TO_SOURCE
  python backtrack.py --check-all --repo PATH_TO_SOURCE
  python audit_v0_23.py --repo PATH_TO_SOURCE

The component build_provenance.py scripts and dependency_audit_v0_23/build_audit.py
regenerate their exact source records. The version scripts configure, merge,
assemble and validate this increment. Run finish_metadata_v0_23.py only after
audit_v0_23.py and validate_tex_v0_23.py. Package with package_v0_23.py.
Do not run old-version scripts against current root metadata; their exact
historical copies are preserved for provenance.

The source checkout itself is not redistributed in this archive. No fresh
Lean compilation or kernel replay is part of these checks.
'''
(ROOT/'README.txt').write_text(readme)
scope_report='''FINAL SCOPE REVIEW — VERSION 0.23

PASS for the explicitly stated human-reconstruction scope.

The actual closed representation leaf is HP1–HP4. HP5–HP6 connect it to
the earlier original-field endpoints and retain only the stated actual
data, rather than a highest-weight/classification theorem. The potential
dual/inverse-transpose ambiguity in HP5 was removed by classifying the
chosen constituent's dual and dualizing back. No irreducibility of arbitrary
complexification is assumed.

VW1–VW4 close the same-field cohomological assembly and fixed-pair window
rescaling, conditional on precise deep suppliers. WB1–WB8 close every
ramified-character, averaging, moving-cutoff, scalar and analytic step from
the explicit WB7 arithmetic contract. DA1–DA2 prove the uniform-family and
conditional global-link joins, retaining the actual NprimeMuR metric
comparison. None of these three chains is described as construction of
its open arithmetic premises.

The original formal development's verification is not in dispute or rerun
here. Missing human arguments are not alleged formal gaps. No RH/GRH
completion percentage is asserted. The source's Dirichlet scope is preserved.

The final cumulative TeX states the current frontier in its opening summary,
version-0.23 historical-scope bridge, new component status paragraphs and
remaining-work section. The checkpoint and audit distinguish classical
citation leaves, bespoke unproved suppliers, and actual common-object
bindings. All historical mathematical proof paragraphs remain intact.

Independent review records cover every new endpoint and bind to exact final
component hashes. Hash and syntax checks validate traceability, not the
truth of the remaining arithmetic suppliers. No PDF visual check is claimed.
'''
(ROOT/'reviews_v0_23/final_scope_review.txt').write_text(scope_report)
print(json.dumps({'checkpoint':str(ROOT/'continuation_checkpoint.json'),'audit':str(ROOT/'RH_dependency_audit_v0_23.txt'),'claims':len(ledger['claims']),'new_claims':ledger['validation']['new_claims']},indent=2))
