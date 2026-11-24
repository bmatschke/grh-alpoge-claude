#!/usr/bin/env python3
"""Verify independently written reviews and normalize their release registry."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
CFG=read(ROOT/'increment_v0_50.json')
REG=ROOT/'reviews_v0_50';REG.mkdir(exist_ok=True)
registry=[]
for comp in CFG['components']:
    here=ROOT/comp; ledger=read(here/'provenance.json')
    claims={c['id']:c for c in ledger['claims']}
    author=CFG['component_authors'][comp].removeprefix('/root/')
    author='root' if author=='/root' else author
    raw=(here/'main.tex').read_bytes(); full=hashlib.sha256(raw).hexdigest()
    paths=sorted(set(here.glob('independent_review*.json')) | set(here.glob('review_*.json')))
    assert paths,('no independent review',comp)
    all_covered=set();records=[]
    for rp in paths:
        r=read(rp)
        assert str(r.get('status',r.get('result',r.get('verdict','')))).startswith('PASS'),rp
        for key in ['unresolved_findings','remaining_findings','issues','required_corrections','material_corrections_required']:
            assert not r.get(key,[]),(rp,key)
        reviewer=r['reviewer'].removeprefix('/root/')
        reviewer='root' if reviewer=='/root' else reviewer
        assert reviewer!=author,('self review',comp,rp)
        assert r['source_commit']==CFG['source_commit'],rp
        bound=r.get('proof_file_sha256',r.get('proof_sha256',r.get('reviewed_sha256',r.get('main_sha256'))))
        assert bound==full,('reviewed proof changed',rp)
        claimed=r.get('claims_reviewed',r.get('reviewed_claims',r.get('claims',r.get('blocks',[]))))
        hashes=dict(r.get('proof_hashes',{}))
        if isinstance(claimed,dict):
            for cid,v in claimed.items():
                hashes[cid]=v if isinstance(v,str) else v.get('block_sha256',v.get('proof_range_sha256',v.get('sha256')))
        else:
            for v in claimed:
                if isinstance(v,str): assert v in hashes,(rp,'no block hash',v)
                else:
                    cid=v.get('id',v.get('claim'))
                    hashes[cid]=v.get('block_sha256',v.get('proof_range_sha256',v.get('range_sha256',v.get('sha256',v.get('proof_location',{}).get('sha256')))))
        assert hashes and set(hashes)<=set(claims),(rp,'claim scope')
        for cid,h in hashes.items():
            pl=claims[cid]['proof_location']
            block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
            actual=hashlib.sha256(block).hexdigest()
            assert actual==h,(rp,cid,'review hash')
            assert actual==pl['sha256'],(rp,cid,'provenance hash')
        all_covered.update(hashes)
        records.append({'review_file':str(rp.relative_to(ROOT)),'review_sha256':sha(rp),
          'reviewer':reviewer,'proof_file':comp+'/main.tex','proof_file_sha256':full,
          'claims':list(hashes),'proof_hashes':hashes,'result':'PASS'})
    assert all_covered==set(claims),('incomplete review',comp,set(claims)-all_covered)
    for c in ledger['claims']:
        c.setdefault('author_status_before_review',c.get('status'))
        c['status']='complete human proof in the explicitly stated scope; independently reviewed'
        c['proof_status']='complete in the explicitly stated scope'
        c['review_status']='PASS; exact mathematical review and block hashes recorded'
        c['independent_review_files']=[r['review_file'] for r in records if c['id'] in r['claims']]
    ledger['status']='independently reviewed at the explicitly stated scope'
    ledger['independent_reviews']=records
    dump(here/'provenance.json',ledger)
    for name in ['closure.json','contracts.json']:
        p=here/name
        if p.exists():
            d=read(p);d['independent_reviews']=records
            d['review_status']='PASS at the explicitly stated scope'
            dump(p,d)
    dump(here/'hashes.json',{p.name:sha(p) for p in here.iterdir() if p.is_file() and p.name!='hashes.json'})
    registry.append({'component':comp,'author':author,'claims':list(claims),
      'independent_reviews':records,'coverage':'all new claims','result':'PASS'})
dump(REG/'review_registry.json',{'artifact_version':'0.50','complete_component_reviews':registry,
 'scope':'Independent mathematical and original-contract review of every new claim, bound to exact proof bytes. This is not formal verification or a Lean replay.'})
# Review normalization changes only new metadata. Rebind inherited parent-ledger
# hashes in component order after those changes; actual proof blocks are immutable.
def rebind(x):
    changed=False
    if isinstance(x,dict):
        if 'exact_parent_provenance_sha256' in x:
            parent=ROOT/x['component']/'provenance.json'
            assert parent.is_file(),parent
            current=sha(parent)
            if x['exact_parent_provenance_sha256']!=current:
                x['exact_parent_provenance_sha256']=current;changed=True
        for v in x.values():changed=rebind(v) or changed
    elif isinstance(x,list):
        for v in x:changed=rebind(v) or changed
    return changed
for comp in CFG['components']:
    here=ROOT/comp
    for p in here.glob('*.json'):
        if p.name=='hashes.json' or 'review' in p.name:continue
        d=read(p)
        changed=rebind(d)
        if isinstance(d,dict):
            oldstatus=d.get('status','')
            if 'pending_independent_review' in oldstatus:
                d['status']='complete_at_stated_scope_independently_reviewed';changed=True
            if d.get('pending_review_claims'):
                d['pending_review_claims']=[];changed=True
        if changed:dump(p,d)
    for name in ['report.txt','README.txt']:
        p=here/name
        if p.exists():
            t=p.read_text()
            for a,b in [
              ('complete_at_stated_scope_pending_independent_review','complete_at_stated_scope_independently_reviewed'),
              ('Independent mathematical review pending.','Independent mathematical review PASS at the stated scope.'),
              ('independent review pending.','independent review PASS at the stated scope.')]:
                t=t.replace(a,b)
            p.write_text(t)
for comp in CFG['components']:
    here=ROOT/comp
    dump(here/'hashes.json',{p.name:sha(p) for p in here.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'components':len(registry),'reviewed_claims':sum(len(r['claims']) for r in registry),'result':'PASS'}))
