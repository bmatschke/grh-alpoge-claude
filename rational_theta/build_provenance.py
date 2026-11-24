#!/usr/bin/env python3
"""Rebuild the RTG component from marked human proofs and exact pinned sources.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v040

Only this component directory is written. This is byte/source bookkeeping;
it does not invoke Lean or count formal source invocation as a human proof.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMPONENT = 'rational_theta'
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source', type=Path, default=HERE.parents[1]/'lean_source')
ap.add_argument('--baseline', type=Path, default=HERE.parents[1]/'reconstruction_v040')
args = ap.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()==PIN
old = {c['id']:c for c in json.loads((BASE/'provenance.json').read_text())['claims']}
assert not any(re.fullmatch(r'RTG\d+',key) for key in old)
plan = json.loads((HERE/'claim_plan.json').read_text())
contracts = json.loads((HERE/'contracts.json').read_text())
raw = (HERE/'main.tex').read_bytes()
assert not any(x<32 and x not in (9,10) for x in raw)
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)')
cache = {}
def source(path, anchor):
    name, sep, n = anchor.partition('@')
    if path not in cache:
        b=(SOURCE/path).read_bytes()
        assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE),path
        ls=b.decode().splitlines(keepends=True)
        ds=[(i,DECL.match(s).group(1)) for i,s in enumerate(ls) if DECL.match(s)]
        cache[path]=(b,ls,ds)
    b,ls,ds=cache[path]
    hits=[(j,i) for j,(i,x) in enumerate(ds) if x==name and (not sep or i+1==int(n))]
    assert len(hits)==1,(path,anchor,hits)
    j,st=hits[0]
    en=ds[j+1][0] if j+1<len(ds) else len(ls)
    for k in range(st+1,en):
        if re.match(r'^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)',ls[k]):
            en=k;break
    while en>st+1 and not ls[en-1].strip():en-=1
    rb=''.join(ls[st:en]).encode()
    return dict(path=path,declaration=name,source_spelling=name,declaration_anchor=anchor,
                line_start=st+1,line_end=en,sha256=sha(b),file_sha256=sha(b),
                range_sha256=sha(rb),range_bytes=len(rb),first_line=ls[st].rstrip(),
                verified_equal_to_pinned_git_blob=True,
                role='Original definition, exact endpoint, formal comparator or explicitly retained producer. A source invocation is never counted as its own human proof; RTG25 producer anchors remain open.',
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}')

anchors={f'RTG{i}':[] for i in range(1,26)}
for s in (HERE/'source_anchors.txt').read_text().splitlines():
    if not s or s.startswith('#'):continue
    ids,path,names=s.split('|')
    for name in names.split(';'):
        item=source(path,name)
        for key in ids.split():
            assert key in anchors,key
            if item not in anchors[key]:anchors[key].append(item)

deps=plan['depends_on']
assert len(plan['titles'])==len(plan['scopes'])==25
claims=[]
for i,(title,scope) in enumerate(zip(plan['titles'],plan['scopes']),1):
    key=f'RTG{i}'
    starts=[j for j,s in enumerate(lines) if s.strip()==f'% BEGIN {key}']
    ends=[j+1 for j,s in enumerate(lines) if s.strip()==f'% END {key}']
    assert len(starts)==len(ends)==1 and starts[0]<ends[0] and anchors[key],key
    st,en=starts[0],ends[0]
    block=''.join(lines[st:en]).encode()
    assert all(d in old or d in deps for d in deps[key]),key
    classical=[]
    if i in (2,7,8,9,10,23):
        classical=['Elementary number-field ideal factorization/localization and CRT; finite module and Noetherian lattice arguments where explicitly proved. The ideal-class finiteness used in RTG7 is inherited KB7, not a new published application.']
    if i in (4,14,21):
        classical=['Ordinary basis extension, finite-dimensional linear algebra and injectivity of field embeddings. Exact VV scalar extension is inherited CFB1 where used.']
    claims.append(dict(id=key,title=title,introduced_in='0.41',classification='B',
        status='Complete independent human proof in its stated conditional scope',
        proof_status='complete in stated scope',review_status='pending independent mathematical review',
        depends_on=deps[key],scope=scope,quantifier_scope=scope,
        hypotheses_retained=plan['common_hypotheses']+plan['additional_hypotheses'].get(key,[]),
        classical_inputs=classical,
        proof_location=dict(file=COMPONENT+'/main.tex',paragraph=key,label='claim:'+key,
                            line_start=st+1,line_end=en,bytes=len(block),sha256=sha(block),
                            range_sha256=sha(block),file_sha256=sha(raw)),sources=anchors[key]))
visited,visiting=set(),set()
def visit(k):
    if k in visited or k not in deps:return
    assert k not in visiting,('cycle',k)
    visiting.add(k)
    for d in deps[k]:visit(d)
    visiting.remove(k);visited.add(k)
for key in deps:visit(key)

inputs,blocks=[],[]
input_names={'continuation_notes_v0_40/next_division_and_readings.txt'}
for key in sorted({d for ds in deps.values() for d in ds if d in old}):
    pl=old[key]['proof_location'];file=pl['file'];input_names.add(file)
    companion=str(Path(file).with_name('provenance.json'))
    if (BASE/companion).exists():input_names.add(companion)
    b=(BASE/file).read_bytes();ls=b.decode().splitlines(keepends=True)
    if 'line_start' in pl and 'line_end' in pl:st,en=pl['line_start']-1,pl['line_end']
    else:
        hits=[j for j,s in enumerate(ls) if '\\paragraph' in s and re.search(r'\b'+key+r'(?!\d)',s)]
        assert len(hits)==1,(key,hits)
        st=hits[0];en=next((j for j in range(st+1,len(ls)) if ls[j].startswith('\\paragraph')),len(ls))
    rb=''.join(ls[st:en]).encode();expected=pl.get('range_sha256',pl.get('sha256'))
    if expected:assert sha(rb)==expected,(key,'inherited proof-range mismatch',sha(rb),expected)
    blocks.append(dict(id=key,file=file,release='0.40',line_start=st+1,line_end=en,
                       sha256=sha(rb),range_sha256=sha(rb),file_sha256=sha(b)))
for file in sorted(input_names):
    b=(BASE/file).read_bytes()
    inputs.append(dict(file=file,release='0.40',sha256=sha(b),file_sha256=sha(b),bytes=len(b)))

standing='The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Every open status concerns human reconstruction only.'
closed=contracts['closed_contracts']
for c in closed:
    c.update(classification='B',status='closed conditional implication',
             dependency_mode='sufficient conjunction only in the expressly stated same-object scope; retained geometric producers are not discharged')
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.41',date='2026-11-22',
          component=COMPONENT,source_commit=PIN,repository='CocoSgt/riemann-hypothesis-lean',
          standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
          range_convention='Inclusive one-based physical lines; exact UTF-8 bytes including line endings.',
          metadata_builder=dict(file='build_provenance.py',sha256=sha(Path(__file__).read_bytes()),
              portable_invocation='python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v040',
              source_anchor_file='source_anchors.txt',source_anchor_sha256=sha((HERE/'source_anchors.txt').read_bytes()),
              claim_plan_file='claim_plan.json',claim_plan_sha256=sha((HERE/'claim_plan.json').read_bytes()),
              contract_plan_file='contracts.json',contract_plan_sha256=sha((HERE/'contracts.json').read_bytes())),
          claims=claims,claim_total=len(claims),external_literature=[],published_applications=[],
          inherited_proof_inputs=inputs,inherited_proof_blocks=blocks,not_closed=contracts['not_closed'],
          source_files=[dict(path=p,sha256=sha(b),file_sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True)
                        for p,(b,ls,_) in sorted(cache.items())])
dump('provenance.json',prov);dump('published_applications.json',[])
closure=dict(schema='rh-human-component-closure/1',version='0.41',component=COMPONENT,
             source_commit=PIN,standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
             provenance_sha256=sha((HERE/'provenance.json').read_bytes()),new_claim_ids=[c['id'] for c in claims],
             closed_contracts=closed,remaining_inputs=contracts['remaining_inputs'],
             selected_top_level_leaf_closed=False,same_object_guards=contracts['same_object_guards'],
             not_closed=contracts['not_closed'],review_status='pending independent mathematical review')
dump('closure.json',closure)
loc=[f'RTG source locators — {PIN}','Inclusive one-based source/proof lines and exact byte hashes.',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
    p=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c['sources']:
        loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
validation=dict(status='PASS',source_commit=PIN,main_sha256=sha(raw),claims=len(claims),
                claim_source_references=sum(len(c['sources']) for c in claims),distinct_source_ranges=len(ranges),
                source_files=len(cache),inherited_files=len(inputs),inherited_claim_blocks=len(blocks),
                checks=['Pinned HEAD and every source Git blob','All unique source anchors and every marked human proof range',
                        'All dependencies are indexed human claim IDs','Acyclic new claim dependency graph',
                        'Exact source/proof/inherited hashes; unused RTG prefix; no unexpected control characters'],
                not_performed='No Lean compilation or kernel replay. Mathematical peer review and standalone draft TeX are separate records.')
dump('validation.json',validation)
report='''v0.41 — prescribed-field theta and actual rational tests, RTG1–RTG25

This component closes substantial finite and arithmetic consumers, while
retaining their exact common geometric inputs. RTG2–5 reconstruct tame
character-value descent by CRT and exact open-kernel adelic descent,
actual rational-form values, one coefficient
extension before every tuple and representative, and the actual adelic side.
RTG6–11 reconstruct split-supported representatives, every RepsOK/LatPin
clause including global element-valued SplitSupp, the paired elementary-divisor
square law, original ideal coefficients and EpIs, exact half levels/coefficient
fields, and the residue polynomial with the original inverse character.
RTG12 assembles all eleven original Pins fields on the literal base coefficient
record, conditional on the explicitly retained CoversAt geometric packet.

RTG13–21 reconstruct the full finite class-sum and phase transfer. The use of
exactly the base c-prime and level lets the base OneMapOf supply CuspBC/ActBC
without an unproved field-change theorem. Original FWTie/LUnif/EvInj give
actual-read independence. The finite span and nonzero scalar-ratio argument
preserve one point-identity lambda/z, and the all-zero base case is separately
proved. OneMapOverL retains the prescribed phase. RatAt uses unprojected y
for thF and the original eOp(y) for thG; the exact chi-inverse projector is
proved, not replaced by an adjoint. Both Boolean-level LiftTestB predicates
and LiftTest follow with the original A3.A.v0 embedding.

RTG22–24 reconstruct the full GoodLat.mLat_of_tie consumer from its printed
LatFull premise. This identifies the whole original MK valuation lattice and
the literal Mcoord preimage; it does not manufacture geometric integral
fullness from FWTie. It joins the original base tests on one three-stage R/F.

Remaining C producers are explicit: common initial geometry/FWTie/base pins
and phase, actual higher CoversAt, ClsEx cusp membership and uniqueness,
uniform geometric PointIdentCore, original base ClassSumsSpan (including its
size hypothesis), and LatFull when it is not already supplied as InB.latFull.
The original eta agreement and stronger second DivRows3 remain separate.
No whole BASE_THETA_RATIONAL_TESTS or common-selection leaf is closed.

The accepted source-correctness assumption is unchanged. No Lean build or
kernel replay was used. No new published deep theorem application is claimed;
published_applications.json is empty. Inherited BTH13, KB7, CFB and RDR inputs
are individually bound to their actual earlier proof blocks.
'''
report+=f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE/'closure.json').read_bytes())}\n"
report+=f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} source files; {len(inputs)} inherited files; {len(blocks)} inherited proof blocks.\n"
(HERE/'report.txt').write_text(report)
print(json.dumps({**validation,'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))
