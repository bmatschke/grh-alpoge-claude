#!/usr/bin/env python3
"""Rebuild LP source ranges against the pinned checkout; no source edits."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]/'lean-source')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parent
REPO=args.repo.resolve()
COMMIT='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
GP='src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
DP='src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
cache={}

def source(path,spelling,qualified=None,role='proof'):
    if path not in cache:
        raw=(REPO/path).read_bytes()
        pinned=subprocess.check_output(['git','-C',str(REPO),'show',f'{COMMIT}:{path}'])
        assert raw==pinned,path
        cache[path]=raw
    raw=cache[path]; lines=raw.splitlines(keepends=True)
    decoded=[l.decode('utf-8').rstrip('\r\n') for l in lines]
    pattern=re.compile(r'^(?:theorem|lemma|def|structure) '+re.escape(spelling)+r'(?:\s|\{|\(|:)')
    hits=[i for i,l in enumerate(decoded) if pattern.search(l)]
    assert len(hits)==1,(path,spelling,hits)
    start=hits[0]
    stop=start+1
    while stop<len(lines) and not re.match(r'^(?:theorem|lemma|def|structure|variable|namespace|end|open|noncomputable)\b|^@\[',decoded[stop]):
        stop+=1
    while stop>start+1 and not decoded[stop-1].strip():stop-=1
    return dict(path=path,declaration=qualified or spelling,line_start=start+1,line_end=stop,
                sha256=hashlib.sha256(raw).hexdigest(),range_sha256=hashlib.sha256(b''.join(lines[start:stop])).hexdigest(),
                url=f'{URL}/blob/{COMMIT}/{path}#L{start+1}-L{stop}',
                first_line=decoded[start],declaration_lines_within_range=[start+1],role=role,
                verified_equal_to_pinned_git_blob=True)

def glue(name):return source(GP+'MemLocSub.lean',name,'GlobalTheory.EX.Glue.'+name)
def led(name,role='proof'):return source(GP+'ExistsLedPart.lean',name,'GlobalTheory.EX.Led.'+name,role)
def defs(name):return source(DP+'SetUnipotentTranslate.lean',name,'GlobalTheory.EX.OB.'+name,'input_definition')

shared=[
    'Dedekind ideal factorization, maximality of nonzero primes in a number ring, and Noetherianity are declared classical background.',
    'The actual application supplies the geometric datum and comparison; the local fullness, containment and commensurability hypotheses are not constructed here.',
    'No full Lean build or kernel replay was run.'
]
specs=[
 ('LP1','One denominator clears every other prime',
  'For c nonzero and a fixed prime P, one t outside P has c dividing s*t for a suitable s outside Q at every Q != P.',
  [],[glue('exists_clear')],'faithful_translation'),
 ('LP2','Exact localization of an infinite intersection with common denominators',
  'If B_P is local at P and each vector has one nonzero denominator placing it in every B_P, then (intersection B_P)_Q = B_Q.',
  ['LP1'],[glue('locSub'),glue('inLoc_iInf')],'faithful_translation'),
 ('LP3','Finite lattice modification, exact localizations and a global sandwich',
  'For a full M and finitely many local A_P with n_P M <= A_P and n_P A_P <= M_P, the intersection construction uniquely patches A_P on S and M_P elsewhere. With d=product n_P, d M <= N <= d^(-1) M; finite M implies finite full N.',
  ['LP2'],[glue('exists_glue')],'derived_simplification'),
 ('LP4','Patch the actual served and own-type local modules',
  'Under the literal exists_lat hypotheses, pullback of NP at served GIdx places and LT.Nlam at the own type prime gives one global N_u. It is locally contained in Mram away from the type prime and equals Mram at every unserved non-type place.',
  ['LP3','LI6','PL4'],[led('cand_of_VV'),led('exists_sub'),led('exists_served'),led('exists_atT'),led('exists_lat'),defs('RecOK'),defs('LedOK'),source('src/Formalism/LocalRingCardinality/DataLatDefs.lean','LatCmp','Formalism.BasicNotions.LatCmp','input_definition'),source('src/Formalism/LocalRingCardinality/DataLatDefs.lean','Nlam','Formalism.BasicNotions.LT.Nlam','input_definition')],'faithful_translation'),
 ('LP5','Install the patched lattice and preserve the exact ramification-normalized length',
  'Given the canonical refilled datum, setLat replaces NuLat by the patched modules, keeps every other size field, and sets lenMN=lenLoc.toNat/e_w. Whenever lenLoc=l is finite, l=e_w*lenMN; unserved non-type length is zero. This is the lattice/length portion of exists_ledPart, not its entire input construction.',
  ['LP4'],[led('setLat'),led('setInst'),led('exists_ledPart','consumer_and_partial_proof'),source(GP+'ExistsRefill.lean','exists_refill','GlobalTheory.Refill.exists_refill','remaining_input')],'faithful_translation')
]
claims=[]
for ident,title,statement,deps,sources,status in specs:
    claims.append(dict(id=ident,title=title,status=status,statement=statement,depends_on=deps,
                       assumptions=shared,proof_location=dict(file='lattice_patching/main.tex',expanded='lattice_patching/report.txt',section=ident),
                       mathematical_status='proved_under_explicit_hypotheses',introduced_in='0.13',sources=sources))
files=[dict(path=p,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),lines=len(b.splitlines()),verified_equal_to_pinned_git_blob=True) for p,b in sorted(cache.items())]
payload=dict(schema='rh-component-provenance-v1',artifact_version='0.13',repository=URL,commit=COMMIT,claims=claims,source_files=files,
             input_boundaries=['Lay/RecOK/LedOK and the actual comparison are supplied.','The full exists_refill, RecExP/ObjCP and NumAt suppliers remain open in this component.'],
             validation=dict(source_files=len(files),source_links=sum(len(c['sources'])for c in claims),pinned_bytes_verified=True,lean_build=False))
(ROOT/'provenance.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(f"{c['id']} {s['declaration']}\n{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}"for c in claims for s in c['sources'])+'\n')
print(json.dumps(payload['validation']))
