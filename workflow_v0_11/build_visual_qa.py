"""Record completed human/image-tool reviews, with an exact render identity bridge."""
from pathlib import Path
import hashlib
import json
import fitz

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'v0_11'
PDF = BASE / 'output/pdf/RH_readable_reconstruction_v0_11.pdf'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
final_sha = sha(PDF.read_bytes())
bridge = json.loads((ROOT / 'render_identity_bridge.json').read_text())
assert bridge['final_pdf_sha256'] == final_sha
assert bridge['changed_pages'] == [99]
assert bridge['byte_identical_page_images'] == [n for n in range(1, 126) if n != 99]
for filename, digest in bridge['final_page_image_sha256'].items():
    assert sha((ROOT / 'pdf_review' / filename).read_bytes()) == digest

# All four scoped reviews were read by root. Root displayed final page 99
# after the sole prose-direction edit. The other 124 rendered PNGs are
# byte-identical to those previously inspected through the image tool.
final_review = ROOT / 'reviews/pdf_final_wording_check.txt'
final_review.write_text(
    'FINAL WORDING AND RENDER IDENTITY REVIEW — ROOT\n'
    f'Final PDF SHA256: {final_sha}\n'
    f'Previous reviewed PDF SHA256: {bridge["previous_reviewed_pdf_sha256"]}\n'
    'One prose direction was corrected on page 99: "GI/GII below supply"\n'
    'became "GI/GII now supply", because those sections precede page 99.\n'
    'No mathematical statement or source record changed.\n'
    'The same pdftoppm command rendered every final page. The PNG files for\n'
    'all 124 pages other than 99 are byte-identical to the images covered by\n'
    'the four scoped visual reviews. Their exact hashes are recorded in\n'
    'render_identity_bridge.json. Final page 99 was separately displayed\n'
    'through view_image and visually inspected by root. PASS: prose,\n'
    'equations, headings, margins and footer remain legible and unclipped.\n'
    'No further correction is required. All 125 final page images are\n'
    'therefore covered by actual image-based visual inspection.\n',
    encoding='utf-8')
bridge_path = ROOT / 'reviews/render_identity_bridge.json'
bridge_path.write_bytes((ROOT / 'render_identity_bridge.json').read_bytes())

specs = [
    ('remarks_math', 'pdf_pages_01_40.txt', [1,40], [5,10,16,24,27,28,35,36,38,39,40]),
    ('lean_audit', 'pdf_pages_41_80.txt', [41,80], [52,54,56,60,63,71,75,80]),
    ('root', 'pdf_pages_81_108.txt', [81,108], [93,95,96]),
    ('readable_sources', 'pdf_pages_109_125.txt', [109,125], [111,115,119,121,124,125]),
]
reviews = []
for author, name, interval, individual in specs:
    path = ROOT / 'reviews' / name
    text = path.read_text()
    assert bridge['previous_reviewed_pdf_sha256'] in text
    assert 'PASS' in text
    reviews.append({'reviewer': author, 'record': 'reviews_v0_11/'+name,
        'record_sha256': sha(path.read_bytes()), 'page_range': interval,
        'individual_pages': individual, 'result': 'passed',
        'reviewed_pdf_sha256': bridge['previous_reviewed_pdf_sha256'],
        'corrections_required': False,
        'final_pdf_coverage': 'Unchanged page PNGs are byte-identical; page 99 is covered by the final root review.'})
reviews.append({'reviewer': 'root', 'record': 'reviews_v0_11/'+final_review.name,
    'record_sha256': sha(final_review.read_bytes()), 'pages': [99],
    'individual_pages': [99], 'result': 'passed', 'corrections_required': False,
    'reviewed_pdf_sha256': final_sha})
with fitz.open(PDF) as doc:
    assert len(doc) == 125
log = (ROOT / 'latex_pass4.txt').read_text()
assert not any(token in log for token in ['Warning', 'Overfull', 'Underfull', '\n!'])
qa = {'artifact_version':'0.11', 'date':'2026-11-21', 'pdf_filename':PDF.name,
    'pdf_sha256':final_sha, 'page_count':125,
    'all_pages_visually_reviewed':True,
    'corrections_required_after_final_render':False,
    'reviewed_pages':list(range(1,126)), 'reviews':reviews,
    'render_method':'pdftoppm -png -scale-to 1100; four-page contact sheets and individual pages',
    'rendered_page_count':125, 'contact_sheet_count':32,
    'final_compile_passes':4, 'final_compile_warnings':[],
    'final_render_identity_bridge':{
        'record':'reviews_v0_11/render_identity_bridge.json',
        'record_sha256':sha(bridge_path.read_bytes()),
        'byte_identical_previously_inspected_page_images':124,
        'changed_pages_visually_reinspected':[99]},
    'scope':'Visual rendering review of every page image of this exact PDF. Mathematical cross-reviews are separate. No full Lean build or independent kernel replay was run.'}
(ROOT / 'visual_qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({'pdf_sha256':final_sha,'pages':125,'visual_review':'passed'}))
