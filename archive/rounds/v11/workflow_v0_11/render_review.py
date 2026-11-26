"""Render every final PDF page and contact sheets for visual inspection."""
from pathlib import Path
import json
import re
import subprocess
import unicodedata
from PIL import Image, ImageOps, ImageDraw
import fitz

BASE = Path(__file__).resolve().parents[1]
PDF = BASE / 'output/pdf/RH_readable_reconstruction_v0_11.pdf'
OUT = BASE / 'v0_11/pdf_review'
OUT.mkdir(exist_ok=True)
subprocess.run(['pdftoppm', '-png', '-scale-to', '1100', str(PDF),
                str(OUT / 'page')], check=True, stdout=subprocess.DEVNULL,
               stderr=subprocess.PIPE)
pages = sorted(OUT.glob('page-*.png'))
for offset in range(0, len(pages), 4):
    block = pages[offset:offset+4]
    canvas = Image.new('RGB', (1616, 2330), '#dfe3e7')
    draw = ImageDraw.Draw(canvas)
    for i, path in enumerate(block):
        im = ImageOps.contain(Image.open(path).convert('RGB'), (778, 1100))
        x, y = 15+(i % 2)*808, 40+(i // 2)*1165
        draw.text((x, y-26), f'Page {offset+i+1}', fill='black')
        canvas.paste(im, (x, y))
    canvas.save(OUT / f'contact_{offset+1:02}_{offset+len(block):02}.png')

def normalized(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s).casefold()
                   if c.isalnum())

components = {'GII': 'type_two_family', 'GI': 'type_one_family',
              'BC': 'base_change', 'GJ': 'family_join',
              'GW': 'global_weight_choice', 'HW': 'host_weight_join'}
labels = {}
for cid, folder in components.items():
    text = (BASE / 'v0_11' / folder / 'main.tex').read_text()
    labels[cid] = re.search(r'\\section\{([^}]+)\}', text).group(1)
mapping = {}
with fitz.open(PDF) as doc:
    for n, page in enumerate(doc, 1):
        text = normalized(page.get_text())
        for cid, label in labels.items():
            if normalized(label) in text:
                mapping[cid] = n
    result = {'pages': len(doc), 'contact_sheets': (len(pages)+3)//4,
              'new_section_start_pages': mapping, 'section_titles': labels}
    (OUT / 'page_map.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
