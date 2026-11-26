"""Rebuild the source hashes for the scoped RU11--HM6.1 join review."""
from pathlib import Path
from hashlib import sha256, sha1
import json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
REPO=ROOT/'alpoge-rh'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
GB='src/Formalism/SharpRestriction/GrowthBounds/'
REQUESTS={
 GB+'ObjSeg.lean':['segLat','segForm','SatIn','PrimIn','GoodSub','GoodShare','badShare','kapT','kap0G4'],
 GB+'Joints.lean':['depth_bound_of_extension','goodSub_bot','badShare_spec','noZeroSMul_mvPoly','depthD_nonneg','bad_share_of_extension_proposition'],
 GB+'FlipOneThree.lean':['lgA','kappaZeroExponent','depthD'],
 GB+'ProjectionLemmaBaseLevel.lean':['kap0I','m0I','segI','DjI','kapTI','totalDegreeBudget','kapPI','t0I'],
 GB+'ColumnSpanDensity/RhoLowerBoundLargeConductor.lean':['D0','t0','kx'],
}
DECL=re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure)\s+(\S+)')
BOUNDARY=re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|namespace|end|section|variable|open|set_option)\b')
assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()==PIN
files=[]; locators=[]
for path,names in REQUESTS.items():
 raw=(REPO/path).read_bytes()
 blob=subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}'])
 assert raw==blob,path
 bid=subprocess.check_output(['git','-C',str(REPO),'rev-parse',f'{PIN}:{path}'],text=True).strip()
 assert sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==bid
 lines=raw.splitlines(keepends=True)
 fhash=sha256(raw).hexdigest()
 files.append({'path':path,'sha256':fhash,'bytes':len(raw),'git_blob_oid':bid,'verified_pinned_blob':True})
 for name in names:
  candidates=[i for i,l in enumerate(lines) if (m:=DECL.match(l.decode())) and m.group(1)==name]
  assert len(candidates)==1,(path,name,candidates)
  start=candidates[0]
  end=next((i for i in range(start+1,len(lines)) if BOUNDARY.match(lines[i].decode())),len(lines))
  while end>start and not lines[end-1].strip(): end-=1
  segment=b''.join(lines[start:end])
  locators.append({'path':path,'declaration':name,'start_line':start+1,'end_line':end,'file_sha256':fhash,'range_sha256':sha256(segment).hexdigest(),'range_bytes':len(segment),'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start+1}-L{end}'})
artifacts=[]
for path in ['v0_10/reviews/remarks_math_np.txt','v0_10/reviews/remarks_math_join.txt','v0_10/numerical_parameters/report.txt','v0_10/rank_upper/report.txt','v0_10/harmonic_model/report.txt']:
 raw=(ROOT/path).read_bytes()
 artifacts.append({'path':path,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
result={'source_commit':PIN,'scope':'Pointwise badShare attainment and the exact RU11-to-HM6.1 substitution; no kernel replay.','source_files':files,'sources':locators,'reviewed_artifacts':artifacts}
(HERE/'remarks_math_join_sources.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'files':len(files),'source_links':len(locators),'reviewed_artifacts':artifacts},indent=2))
