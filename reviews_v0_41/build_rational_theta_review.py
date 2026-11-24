#!/usr/bin/env python3
"""Bind the independent v0.41 rational-theta mathematical review."""
from pathlib import Path
import argparse,hashlib,json,subprocess
P=argparse.ArgumentParser();P.add_argument('--component',type=Path,required=True);P.add_argument('--source-root',type=Path,required=True);P.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
a=P.parse_args();C=a.component.resolve();R=a.source_root.resolve();O=a.out.resolve();O.mkdir(exist_ok=True,parents=True)
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
digest=lambda b:hashlib.sha256(b).hexdigest();sha=lambda p:digest(p.read_bytes());read=lambda p:json.loads(p.read_text())
assert subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip()==PIN
p=read(C/'provenance.json');closure=read(C/'closure.json');aux=read(O/'rational_theta_arithmetic_review.json')
assert sha(C/'main.tex')=='7897aeb33f5a91330916b0bc8c56d7b0a97cf03c7ea74ece8d673fef977268c3'
assert sha(C/'provenance.json')=='98051b0c90ce78270a79456183d33ed50540a71d509aaea3d93a60acab6d1ed9'
assert sha(C/'closure.json')=='68fea7876398ca02992b4b290c41e81ee4363f936050d9efedcf44819617f326'
assert str(aux.get('verdict',aux.get('result',aux.get('status','')))).startswith('PASS')
raw=(C/'main.tex').read_bytes();lines=raw.splitlines(keepends=True);blocks=[];seen={};ranges=set();occ=0
for c in p['claims']:
 loc=c['proof_location'];block=b''.join(lines[loc['line_start']-1:loc['line_end']]);assert digest(block)==loc['sha256']
 blocks.append({'id':c['id'],'line_start':loc['line_start'],'line_end':loc['line_end'],'proof_range_sha256':digest(block)})
 for s in c['sources']:
  path=s['path']
  if path not in seen:
   b=(R/path).read_bytes();assert b==subprocess.check_output(['git','-C',str(R),'show',PIN+':'+path]);seen[path]=b
  b=seen[path];assert digest(b)==s['file_sha256'];r=b''.join(b.splitlines(keepends=True)[s['line_start']-1:s['line_end']]);assert digest(r)==s['range_sha256']
  ranges.add((path,s['line_start'],s['line_end']));occ+=1
checks=[
 ('RTG1','The prescribed coefficient record c-prime is literally the base record, with field M=embLL.fieldRange. The higher CoversAt, all actual ClsEx including scaleXi, one PointIdentCore before O/constants, base ClassSumsSpan, phase data and outer realization remain explicit.'),
 ('RTG2-12','Independent arithmetic/source review verifies CRT local values and full XiVal via finite-image/open-kernel equality, inverse block-chi/direct xi factors, coefficient extension before all tuples, supported representatives, exact self-dual square law, half-level guards and AA-scaled lattice integrality. All eleven Pins fields retain CoversAt. See bound auxiliary review.'),
 ('RTG13-15','The fallback j=0 case is excluded by LUnif including dimension zero. IsKsForm plus LUnif/EvInj supplies complex independence of actual cusp reads. CuspBC, ActBC and EquivAt are inherited from the unchanged coefficient/level record; rational-left invariance extends representative equalities.'),
 ('RTG16-18','ClassSumsSpan gives a finite expansion in the same M-space. The two PtIdent formulas yield exact c0/c1 factor, without division by a theta value. Actual read independence proves c0/c1 lies in M in the nonzero branch; scaleXi changes only c-delta. The zero-base branch uses vanishing and never asserts that ratio is in M. Full OneMapOf retains central action, norms, original phase, uniqueness among sections, coefficient comparisons and PhRat.'),
 ('RTG19-21','The rational source vector is obtained by the finite cusp expansion and original evaluation map. The second RatAt clause uses the actual eOp=sum e_g chi(g)^(-1) rho(g). RatG uses cj(twAt embLL A3.A.v0)(R.phs i), not a freely chosen phase. One twisted coordinate basis separates and is rational on both every theta vector and every original target basis vector, for both Boolean levels.'),
 ('RTG22-24','Exact FWTie point/norm equivalence identifies the literal MK with the supplied valuation lattice. LatFull remains a premise. Noetherianity and denominator clearing prove finite generation and full span of the literal preimage Mcoord, including zero dimensions and both levels. No replacement saturated lattice or altered metric is used.'),
 ('RTG25','The retained higher-cover, class-sum uniqueness, common point identity, size-bound class-span and geometric LatFull producers remain open; actual base data, Fits/eta, second DivRows3, primitive rows and common selection are not inferred from finite consumers.')
]
d={'schema':'rh-independent-human-review/1','artifact_version':'0.41','component':'rational_theta','verdict':'PASS: all 25 claims in their stated scopes; no remaining required correction','reviewer':'root, independent of chapter author; arithmetic claims RTG2-12 independently reviewed by audit_count_path','source_commit':PIN,'proof_file_sha256':sha(C/'main.tex'),'provenance_file_sha256':sha(C/'provenance.json'),'closure_file_sha256':sha(C/'closure.json'),'published_applications_file_sha256':sha(C/'published_applications.json'),'claims_reviewed':[c['id'] for c in p['claims']],'proof_blocks':blocks,'checks':[{'claims':k,'finding':v} for k,v in checks],'auxiliary_review':{'file':'reviews_v0_41/rational_theta_arithmetic_review.json','sha256':sha(O/'rational_theta_arithmetic_review.json')},'source_checks':{'files':len(seen),'distinct_ranges':len(ranges),'occurrences':occ,'all_equal_pinned_git_blob':True},'required_corrections':[],'unresolved_review_issues':[],'whole_selected_leaf_closed':False,'new_Lean_build_performed':False,'standing_assumption':'Pinned formal proof accepted as fully checked and correct; this review concerns human arguments and exact conditional boundaries.'}
(O/'rational_theta_review.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
text='INDEPENDENT HUMAN REVIEW: RATIONAL THETA v0.41\n\n'+d['verdict']+'\n\n'
for k,v in checks:text+=k+'\n'+v+'\n\n'
text+='The source/proof hash checks are separate from the mathematical review. No Lean build or replay was performed. No whole selected leaf closes.\n\n'
for k in ['proof_file_sha256','provenance_file_sha256','closure_file_sha256']:text+=k+': '+d[k]+'\n'
(O/'rational_theta_review.txt').write_text(text)
print(json.dumps({'status':'PASS','claims':len(blocks),'source_files':len(seen),'ranges':len(ranges),'review_sha256':sha(O/'rational_theta_review.json')}))
