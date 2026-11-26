"""Render each finished page and four-page contact sheets for visual review."""
from pathlib import Path
import json
import subprocess
from PIL import Image, ImageOps, ImageDraw
import fitz

BASE=Path(__file__).resolve().parents[1]
pdf=BASE/'output/pdf/RH_readable_reconstruction_v0_10.pdf'
out=BASE/'v0_10/pdf_review'
out.mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-png','-scale-to','1100',str(pdf),str(out/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
pages=sorted(out.glob('page-*.png'))
for offset in range(0,len(pages),4):
    block=pages[offset:offset+4]
    canvas=Image.new('RGB',(1616,2330),'#dfe3e7')
    draw=ImageDraw.Draw(canvas)
    for i,path in enumerate(block):
        im=Image.open(path).convert('RGB')
        im=ImageOps.contain(im,(778,1100))
        x=15+(i%2)*808;y=40+(i//2)*1165
        draw.text((x,y-26),'Page '+str(offset+i+1),fill='black')
        canvas.paste(im,(x,y))
    canvas.save(out/f'contact_{offset+1:02}_{offset+len(block):02}.png')
with fitz.open(pdf) as doc:
    mapping={}
    labels={'RU':'The actual coarse upper rank on each digit class',
            'RD':'The actual coarse lower rank and density',
            'HM':'Harmonic models, density, and the actual cloud maps',
            'NP':'Uniform parameters and the actual Type-I height',
            'TC':'The complete local Type-I theorem'}
    for number,page in enumerate(doc,1):
        text=' '.join(page.get_text().split())
        for cid,label in labels.items():
            if label in text: mapping[cid]=number
    (out/'page_map.json').write_text(json.dumps({'pages':len(doc),'new_section_start_pages':mapping},indent=2)+'\n')
print(json.dumps({'pages':len(pages),'contacts':(len(pages)+3)//4,'starts':mapping}))
