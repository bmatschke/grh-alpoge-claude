#!/usr/bin/env python3
"""Bind GFI human arguments to the exact pinned contracts and inherited proofs."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,required=True)
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--loss-ledger',type=Path,required=True)
p.add_argument('--loss-claim',required=True)
a=p.parse_args();SOURCE=a.source.resolve();BASE=a.baseline.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,d):(HERE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()==PIN
old={c['id']:c for c in json.loads((BASE/'provenance.json').read_text())['claims']}
loss=json.loads(a.loss_ledger.read_text());lossids={c['id'] for c in loss['claims']}
assert a.loss_claim in lossids
assert not any(re.fullmatch(r'GFI\d+',k) for k in old)
raw=(HERE/'main.tex').read_bytes();lines=raw.decode().splitlines(keepends=True)
decl=re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)')
cache={}
def source(path,name):
 if path not in cache:
  b=(SOURCE/path).read_bytes()
  assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE)
  ls=b.decode().splitlines(keepends=True)
  ds=[(i,decl.match(t)[1]) for i,t in enumerate(ls) if decl.match(t)]
  cache[path]=(b,ls,ds)
 b,ls,ds=cache[path];found=[(j,i)for j,(i,n)in enumerate(ds)if n==name]
 assert len(found)==1,(path,name,found)
 j,s=found[0];e=ds[j+1][0]if j+1<len(ds)else len(ls)
 for q in range(s+1,e):
  if re.match(r'^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)',ls[q]):e=q;break
 while e>s+1 and not ls[e-1].strip():e-=1
 rb=''.join(ls[s:e]).encode()
 return dict(path=path,declaration=name,source_spelling=name,line_start=s+1,line_end=e,
  sha256=sha(b),file_sha256=sha(b),range_sha256=sha(rb),range_bytes=len(rb),
  first_line=ls[s].rstrip(),verified_equal_to_pinned_git_blob=True,
  role='Exact original contract/dictionary/corresponding source proof; human proof is the independently hashed GFI argument.',
  url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{s+1}-L{e}')
anchors={f'GFI{i}':[]for i in range(1,18)}
for line in (HERE/'source_anchors.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 ids,path,names=line.split('|')
 for name in names.split(';'):
  r=source(path,name)
  for k in ids.split():
   if r not in anchors[k]:anchors[k].append(r)
titles=[
 'Original common scales, top labels and exact arithmetic record equality',
 'One realized degree pair carried to every original base point without CoverAll',
 'Actual top/place equivalences, weights and finite-sum reindexing',
 'Every entry of the original ledger and all point/global/local ties',
 'One character functional, universal readings and an admissible common cutoff',
 'Uniform threshold and constants with all original positivity conditions',
 'Literal divisibility and two comparisons with nonnegative coefficient enlargement',
 'Exact counting, ordinary slopes and quotient slopes on the common ledger',
 'Both original loss inequalities on the actual arithmetic reading',
 'Original all-height frame, dual-height bound and retained-defect parameters',
 'Every original error window and the full trace-error budget',
 'Exact budget, growth, cost and remaining-size records',
 'Full same-family ChainTied with all witnesses and quantifiers',
 'ChosenE plus ChosenWall supplies every required small-share input',
 'Full global consumer from the eleven original family fields and same links',
 'Closed installation with the epsilon cutoff and tuple before the family',
 'Selected global assembly closed with constants 2,3,4,2,0',
]
deps={
 'GFI1':[], 'GFI2':['GFI1'], 'GFI3':['GFI1','GFI2'],
 'GFI4':['GFI1','GFI2','GFI3'],
 'GFI5':['GFI1','GFI2','GFI3','GFI4','GFA10','GFA11','GFA12'],
 'GFI6':['GFI1','GFI2','GFI4','GFI5'],
 'GFI7':['GFI1','GFI3','GFI4','GFI6'],
 'GFI8':['GFI1','GFI3','GFI4'],
 'GFI9':['GFI1','GFI2','GFI4','GFI5','GFI6'],
 'GFI10':['GFI4','GFI6','GFA8','GFA9'],
 'GFI11':['GFI1','GFI5','GFI6','GFA11'],
 'GFI12':['GFI1','GFI3','GFI5','GFA10','GFA11','GFA12'],
 'GFI13':[f'GFI{i}' for i in range(1,13)],
 'GFI14':['HW3','SZ1','SZ2','SZ3','SZ8'],
 'GFI15':['GFI13','GFI14','GLE2','GLE10','GLE11','GLE12','RSL10','RSL11']+[f'GVC{i}'for i in range(1,19)]+[f'GFA{i}'for i in range(1,13)]+[a.loss_claim,'MT6'],
 'GFI16':['GFI15'], 'GFI17':['GFI16','GLS13','ZW1','ZW2','ZW3','ZW4'],
}
common='Same original family, fields, ranks, words, host data, metrics, coefficient maps and original size record; all choices have source quantifier order.'
hyp={
 'GFI1':['Original FamP/FamCore equality fields; x exceeds its family threshold'],
 'GFI2':['Original LossFS witness including a realizing i1; original coverS, not CoverAll'],
 'GFI3':['The actual Mod constructed in GFI2 and original place/frame coding'],
 'GFI4':['Original Mod; supplied frame errors; unchanged target and source lattices'],
 'GFI5':['Actual CharF/NodesF/WinF on the original family; common Mod and original integer degree pair'],
 'GFI6':['All nine original numerical/lattice family predicates; ChosenTT/QD/Thin; LinkIRR/LinkDIV; nonnegative Cabs,CH,eL and positive c6'],
 'GFI7':['Same LinkDIV with its actual constant Cd and same support, maps and metrics'],
 'GFI8':['Literal original CountF, SlopesMF and SlopesNF with their uniform constants'],
 'GFI9':['Literal original LossFS with common pair and every-reading quantifier'],
 'GFI10':['Same FrameF, LinkDIV, LatF and LinkIRR; common actual RR dual'],
 'GFI11':['Same original WinF, ChosenTT, FrameF and nonnegative constants'],
 'GFI12':['Same actual node/window/character records and ChosenTT/QD/Thin'],
 'GFI13':['Exactly the hypotheses of GFI6; no upstream producer existence inferred'],
 'GFI14':['Original ChosenE and ChosenWall on the same FamP; unchanged size fields'],
 'GFI15':['All eleven original FamGLmin fields with column constant4; TuSize; original chosen data and five GlobalTheoremInputs; Cabs>=0,CH>0,C0>=3; same-family LFS endpoint'],
 'GFI16':['FamGLmin on one supplied class; ChosenWall for every member; original Large and TransportedAlt; no family existence inferred'],
 'GFI17':['Original Duty on A and compatible second-layer supplier on D3(3,A), exactly as GLS13; actual local/arithmetic/spectral producers remain premises of LinkGLOBAL'],
}
known=set(old)|set(deps)|lossids;claims=[]
for i,title in enumerate(titles,1):
 k=f'GFI{i}';s=next(j for j,t in enumerate(lines)if t.strip()==f'% BEGIN {k}')
 e=next(j+1 for j,t in enumerate(lines)if t.strip()==f'% END {k}');rb=''.join(lines[s:e]).encode()
 assert set(deps[k])<=known,(k,set(deps[k])-known)
 assert anchors[k]
 claims.append(dict(id=k,title=title,introduced_in='0.35',classification='B',
  status='Complete human proof of the stated conditional result; independent review recorded separately',
  proof_status='complete in the stated scope',review_status='see frozen-byte independent review',
  scope=common,depends_on=deps[k],hypotheses_retained=hyp[k],classical_inputs=[],
  proof_location=dict(file='global_final_installation/main.tex',paragraph=k,label='claim:'+k,
   line_start=s+1,line_end=e,sha256=sha(rb),range_sha256=sha(rb),file_sha256=sha(raw),bytes=len(rb)),
  sources=anchors[k]))
inherited=[]
for k in sorted(set(sum(deps.values(),[]))&set(old)):
 q=old[k]['proof_location']['file']
 if any(v['file']==q for v in inherited):continue
 b=(BASE/q).read_bytes();inherited.append(dict(file=q,sha256=sha(b),bytes=len(b),scope='Unchanged v0.34 human proof, retained in its exact scope'))
inherited.append(dict(file='global_loss/provenance.json',sha256=sha(a.loss_ledger.read_bytes()),bytes=a.loss_ledger.stat().st_size,scope='Same-version original LossFS endpoint; indexed independently'))
not_closed=['Common original DesignChoices/recursive/geometric family existence and duties',
 'Compatible same-family second-layer selector and true-column records',
 'Actual LinkN, LinkIRR, LinkDIVt, LinkG and LinkS producers, plus remaining rank/theta/arithmetic inputs',
 'A complete human proof of RH or unrestricted Dirichlet GRH',
 'Stronger unused PartFiveFamilyBounds or general CoverAll']
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.35',date='2026-11-22',
 source_commit=PIN,repository='CocoSgt/riemann-hypothesis-lean',component='global_final_installation',
 standing_assumption='Underlying pinned Alpoge-Claude Lean proof accepted fully checked and correct; D denotes human understanding only.',
 main_sha256=sha(raw),sha256=sha(raw),claims=claims,claim_total=len(claims),
 range_convention='Inclusive one-based physical lines; hashes preserve exact UTF-8 line endings.',
 external_literature=[],inherited_proof_inputs=inherited,not_closed=not_closed,
 source_files=[dict(path=q,sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True)for q,(b,ls,_)in sorted(cache.items())])
dump('provenance.json',prov);dump('published_applications.json',[])
dump('literature.json',dict(schema='rh-exact-literature-application/1',entries=[],note='All new arguments are direct finite identities, inequalities or elementary limiting estimates; inherited inputs keep their original scopes.'))
dump('closure.json',dict(schema='rh-conditional-closure/1',artifact_version='0.35',source_commit=PIN,
 main_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
 proved_claims=[c['id']for c in claims],endpoint_claim='GFI17',
 closed_selected_task='TASK_GL_FINAL_ASSEMBLY',
 endpoint='Closed on D3(3,A): TuSize -> DGamSize -> LinkGLOBAL(Fm,2,CH,3,2,0), conditional on original Duty/compatible second-layer supplier and exact local/global input implications.',
 source_endpoints=['linkCore','FamGLmin.link8','GlobalTheory.Top.link_gl'],
 loss_dependency=a.loss_claim,retained_upstream=not_closed,
 simplifications=['Direct o(log x) second-set-density proof with unchanged endpoint','Coarse integer harmonic sum replaces a stronger prime-sum estimate only in ChosenBadp conversion'],
 constants=dict(Cabs=2,C0=3,C5_column=4,eD=2,eL=0),
 quantifiers='Closed epsilon cutoff and joined TransportedAlt precede Fm,CH; local eventual thresholds precede members, base points, words and places. Realized degree pair may depend on x.',
 lean_build=False,kernel_replay=False))
loc=[f'GFI source locators at {PIN}',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
 z=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {z['line_start']}-{z['line_end']} | {z['sha256']}")
 for s in c['sources']:loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
 loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
report='GFI1–GFI17 — ORIGINAL GLOBAL FINAL INSTALLATION\n\n'+common+'\n\n'
report+='\n'.join(f"{c['id']}: {c['title']}" for c in claims)
report+='\n\nFull source linkCore, tied-ledger and Closed consumer reconstructed. All original producer premises remain. No Lean replay.\n'
report+='The selected global assembly leaf is complete conditional on the independently reviewed original LFS endpoint; not a final theorem existence claim.\n'
(HERE/'report.txt').write_text(report)
result=dict(component='global_final_installation',claim_count=len(claims),source_files=len(cache),
 source_references=sum(len(c['sources'])for c in claims),distinct_ranges=len({(s['path'],s['line_start'],s['line_end'])for c in claims for s in c['sources']}),
 proof_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),closure_sha256=sha((HERE/'closure.json').read_bytes()),inherited_files=len(inherited),loss_dependency=a.loss_claim)
dump('validation.json',result);print(json.dumps(result,indent=2))
