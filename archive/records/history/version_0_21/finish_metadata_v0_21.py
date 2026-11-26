#!/usr/bin/env python3
"""Write v0.21 continuation metadata without claiming a PDF render."""
from pathlib import Path
import copy
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
OLD=ROOT/'history/version_0_20'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

config=read(ROOT/'increment_v0_21.json')
ledger=read(ROOT/'provenance.json')
targets=read(ROOT/'next_source_targets.json')
tex=ROOT/'RH_readable_reconstruction_v0_21.tex'
validation=read(ROOT/'tex_validation.json')
source_audit=read(ROOT/'reviews_v0_21/source_verification_v0_21_audit.json')
assert source_audit['result']=='PASS'
for filename,expected in source_audit['input_sha256'].items():
    assert sha(ROOT/filename)==expected,filename
assert validation['tex_sha256']==sha(tex)
assert validation['pdf_generated'] is False
assert ledger['artifact_version']=='0.21'

sections={}
for component in config['tex_component_order']:
    data=read(ROOT/component/'provenance.json')
    text=(ROOT/component/'main.tex').read_text()
    prefix=re.match(r'[A-Z]+',data['claims'][0]['id']).group()
    sections[prefix]={
        'component':component,'title':re.search(r'\\section\{([^}]*)\}',text).group(1),
        'section_label':re.search(r'\\label\{([^}]*)\}',text).group(1),
        'claims':[c['id']for c in data['claims']],
        'fragment':component+'/main.tex','expanded_report':component+'/report.txt',
        'page_numbers_available':False,
    }

old_cp=read(OLD/'continuation_checkpoint.json')
checkpoint=copy.deepcopy(old_cp)
checkpoint.update({
    'artifact_version':'0.21','predecessor_version':'0.20','date':config['date'],
    'user_instruction':'Continue with full effort; prioritize updated ZIP and TeX. Do not render a fresh PDF unless needed and inexpensive.',
    'main_note_pages':None,'new_section_start_pages':{},
    'new_section_headings':{p:v['title']for p,v in sections.items()},
    'logical_component_page_map':sections,
    'status':config['scope'],
    'new_in_this_version':config['new_in_this_version'],
    'remaining_major_inputs':config['remaining_major_inputs'],
    'next_targets':config['next_steps'],
    'next_source_targets_file':'next_source_targets.json',
    'previous_source_targets_file':'history/version_0_20/next_source_targets.json',
    'retained_prior_results_note':'All prior component bytes, claims, source arrays and dependency adjacency lists are preserved. Older entries are historical; current scope is stated in version_0_21_update and the remaining-major-input list.',
    'current_deliverable':{'main':'RH_readable_reconstruction_v0_21.tex','archive':'RH_reconstruction_v0_21.zip',
         'pdf_generated':False,'reason':'The user prioritized proof work and an updated archive; the TeX is sufficient for continuation.'},
    'last_rendered_note':{'version':'0.13','path':'history/version_0_13/RH_readable_reconstruction_v0_13.pdf',
         'sha256':sha(ROOT/'history/version_0_13/RH_readable_reconstruction_v0_13.pdf'),'pages':150,
         'historical_only':True,'contains_current_increment':False},
})
checkpoint['retained_prior_results'].extend(copy.deepcopy(old_cp['new_in_this_version']))
checkpoint['precision_constraints'].extend(config['precision_notes'])
checkpoint['precision_supersessions'].extend(config['precision_supersessions'])
all_paths={f['path']for f in ledger['source_files']}|{t['path']for t in targets['targets']}
for name in ['source_verification.txt','continuity_audit.txt','final_scope_review.txt']:
    assert (ROOT/'reviews_v0_21'/name).is_file(),name
review_coverage=read(ROOT/'reviews_v0_21/mathematical_review_coverage_v0_21.json')
reviews={entry['review']:sha(ROOT/entry['review'])for entry in review_coverage['review_records']}
checkpoint['validation']={
    'claims':len(ledger['claims']),'new_claims':ledger['validation']['new_claims'],
    'source_links':sum(len(c['sources'])for c in ledger['claims']),
    'source_files':len(ledger['source_files']),'next_target_ranges':len(targets['targets']),
    'next_target_source_files':len({t['path']for t in targets['targets']}),
    'source_files_checked_including_next_targets':len(all_paths),
    'all_cited_ranges_and_file_hashes_checked':True,
    'all_source_bytes_match_pinned_git_blobs':True,
    'all_prior_claim_fields_and_source_arrays_preserved':True,
    'all_prior_source_records_preserved_exactly':True,
    'all_prior_dependency_graph_entries_preserved':True,
    'predecessor_package_file_count':997,'previous_root_files_archived':19,
    'source_verification_record':'reviews_v0_21/source_verification.txt',
    'source_verification_machine_record':'reviews_v0_21/source_verification_v0_21_audit.json',
    'proof_navigation_record':'reviews_v0_21/proof_location_audit_v0_21.json',
    'proof_navigation_counts':source_audit['proof_navigation_counts'],
    'proof_navigation_scope':'All explicit file references resolve and every new claim marker is present. Legacy claims lacking exact pointers retain explicitly recorded component-corpus fallbacks; literal-marker findings are preserved without inventing pointers.',
    'continuity_audit_record':'reviews_v0_21/continuity_audit.txt',
    'mathematical_reviews':reviews,
    'mathematical_review_coverage':'reviews_v0_21/mathematical_review_coverage_v0_21.json',
    'new_claims_independently_reviewed':ledger['validation']['new_claims'],
    'full_lean_build_or_kernel_replay':False,'lean_sources_modified':False,
    'tex':validation,'pdf_generated':False,'pdf_visual_review_performed':False,
}
checkpoint['version_0_21_update']={
    'local_conclusions':config['local_conclusions'],
    'remaining_inputs':config['remaining_major_inputs'],
    'precision_notes':config['precision_notes'],
    'new_claim_ids':[c['id']for c in ledger['claims']if c.get('introduced_in')=='0.21'],
}
write(ROOT/'continuation_checkpoint.json',checkpoint)

filename_map=read(OLD/'component_filename_map.json')
filename_map['note']=config['scope']+' Nineteen v0.20 root files are preserved under history/version_0_20/. The last rendered PDF remains in history/version_0_13/. Current v0.21 locations use section labels and claim IDs; no current page numbers are asserted.'
filename_map['version_0_21_component_sections']=sections
write(ROOT/'component_filename_map.json',filename_map)
stale=ROOT/'visual_qa.json'
if stale.exists():
    assert stale.read_bytes()==(OLD/'visual_qa.json').read_bytes()
    stale.unlink()

readme=f'''RH AND DIRICHLET-GRH: HUMAN RECONSTRUCTION, VERSION 0.21
Date: {config['date']}
Source: {ledger['repository']}
Pinned commit: {ledger['commit']}

CURRENT STATUS
==============
{config['scope']}

The complete current readable note is RH_readable_reconstruction_v0_21.tex.
No new PDF was rendered in this round, following the user's preference to
prioritize proof work, TeX and the updated archive. The 150-page v0.13 PDF
is preserved under history/version_0_13/ as a historical predecessor;
it does not contain any increment after v0.13. No v0.21 page count or visual
layout review is claimed. tex_validation.json records the exact check used.

NEW MATHEMATICS
===============
'''+''.join('- '+item+'\n'for item in config['new_in_this_version'])+'''
REMAINING INPUTS
===============
'''+''.join('- '+item+'\n'for item in config['remaining_major_inputs'])+f'''
HOW TO CONTINUE
===============
Start with continuation_checkpoint.json. next_source_targets.json records
{len(targets['targets'])} exact next-source ranges and their remaining human
scope. The targets are a work map, not additional proved claims.

provenance.json contains {len(ledger['claims'])} stable claims and
{sum(len(c['sources'])for c in ledger['claims'])} exact source-range links;
provenance.txt is its readable companion. Every new component has main.tex,
report.txt, a hashed source ledger and a reproducible locator builder.
The cumulative TeX embeds the complete readable proof text, so it does not
need the fragments in order to compile with a standard LaTeX installation.

For a claim lookup:
  python3 backtrack.py CC19
For source excerpts from a pinned checkout:
  python3 backtrack.py CC19 --repo /absolute/path/to/lean-source
For all recorded source byte and inclusive-range checks:
  python3 backtrack.py --check-all --repo /absolute/path/to/lean-source
For a future PDF build, run pdflatex twice on the current TeX in a build
directory, then inspect the rendered pages. Such a build is not included
in this version's verification claims.

PRESERVATION AND VERIFICATION
============================
All 983 previous claim records retain every original field and source
array. All previous source-file records and mathematical dependency lists
are unchanged. Version-0.21 notes are additive. The package preserves all
997 v0.20 files, moving only its 19 root files to history/version_0_20/
when those current filenames are replaced or retired. Earlier historical
directories and component bytes remain intact.

Scoped mathematical reviews and exact source/hash checks are recorded in
reviews_v0_21/. The mathematical dependency graph is acyclic; it is a
human reconstruction graph, not a transitive Lean dependency audit.
No full Lean compilation, independent kernel replay, or global proof
certification was performed. SHA256SUMS covers every packaged file except
itself. package_v0_21.py verifies predecessor continuity, archive CRCs and
every archived file against that manifest.
'''
(ROOT/'README.txt').write_text(readme)
print(json.dumps({'version':'0.21','sections':list(sections),'claims':len(ledger['claims']),'pdf_generated':False}))
