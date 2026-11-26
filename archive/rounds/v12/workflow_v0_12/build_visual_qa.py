"""Record completed image-based reviews of the exact final PDF.

Run only after the four named reviewers have written their scoped records.
The records, render images and final PDF are bound by SHA256; this script
does not perform or substitute for human/image-tool visual inspection.
"""
from pathlib import Path
import hashlib
import json
import fitz

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'v0_12'
PDF = BASE / 'output/pdf/RH_readable_reconstruction_v0_12.pdf'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
digest = sha(PDF.read_bytes())
expected = 'c55f419163bb9fe45cd762a45694eb3682a1f0d8ce9ad6e8075b5aea06fc032b'
assert digest == expected, 'Reassign visual review if the PDF changes.'
with fitz.open(PDF) as doc:
    pages = len(doc)
assert pages == 137
specs = [
    ('lean_audit', 'pdf_pages_01_48.txt', [1,48]),
    ('remarks_math', 'pdf_pages_49_96.txt', [49,96]),
    ('root', 'pdf_pages_97_112.txt', [97,112]),
    ('readable_sources', 'pdf_pages_113_137.txt', [113,137]),
]
reviews, covered = [], set()
for reviewer, name, interval in specs:
    p = ROOT / 'reviews' / name
    raw = p.read_bytes()
    text = raw.decode()
    assert digest in text and 'PASS' in text, name
    covered.update(range(interval[0], interval[1]+1))
    reviews.append({
        'reviewer':reviewer, 'record':'reviews_v0_12/'+name,
        'record_sha256':sha(raw), 'page_range':interval,
        'reviewed_pdf_sha256':digest, 'result':'passed',
        'corrections_required':False,
    })
assert covered == set(range(1,pages+1))
render_root = ROOT / 'pdf_review'
images = sorted(render_root.glob('page-*.png'))
contacts = sorted(render_root.glob('contact_*.png'))
assert len(images) == pages and len(contacts) == 35
assert {int(p.stem.split('-')[1]) for p in images} == covered
render_hashes = {p.name:sha(p.read_bytes()) for p in images+contacts}
manifest = ROOT / 'reviews/pdf_render_manifest.json'
manifest.write_text(json.dumps({
    'pdf_sha256':digest, 'page_count':pages,
    'render_method':'pdftoppm -png -scale-to 1100; four-page contact sheets',
    'render_image_sha256':render_hashes,
},indent=2)+'\n')
log = (ROOT / 'latex_pass3.txt').read_text()
assert not any(token in log for token in ['Warning','Overfull','Underfull','\n!'])
qa = {
    'artifact_version':'0.12','date':'2026-11-21','pdf_filename':PDF.name,
    'pdf_sha256':digest,'page_count':pages,
    'all_pages_visually_reviewed':True,
    'corrections_required_after_final_render':False,
    'reviewed_pages':sorted(covered),'reviews':reviews,
    'render_method':'pdftoppm -png -scale-to 1100; contact sheets and dense individual pages',
    'rendered_page_count':pages,'contact_sheet_count':len(contacts),
    'final_compile_passes':3,'final_compile_warnings':[],
    'render_manifest':{
        'record':'reviews_v0_12/pdf_render_manifest.json',
        'record_sha256':sha(manifest.read_bytes()),
    },
    'scope':'Actual image-tool inspection covers every page of this exact PDF. Mathematical/source cross-reviews are separate. No full Lean build or independent kernel replay was run.',
}
(ROOT/'visual_qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({'pdf_sha256':digest,'pages':pages,'reviewed_pages':len(covered),'result':'PASS'}))
