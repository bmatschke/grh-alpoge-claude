#!/usr/bin/env python3
"""Bind the v0.41 common-reading continuation note to source and proof bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,default=HERE.parents[1]/'lean_source')
p.add_argument('--baseline',type=Path,default=HERE.parents[1]/'reconstruction_v040')
p.add_argument('--component',type=Path,default=HERE.parent/'rational_theta')
a=p.parse_args();SOURCE,BASE,RTG=a.source.resolve(),a.baseline.resolve(),a.component.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()==PIN
prior=json.loads((BASE/'continuation_notes_v0_40/next_division_and_readings_sources.json').read_text())
prov=json.loads((RTG/'provenance.json').read_text())
lookup={}
for c in prov['claims']:
 for s in c['sources']:lookup[(s['path'],s['declaration'])]=s
cache={}
def bind(identifier,desc,path,st,en):
 if path not in cache:
  b=(SOURCE/path).read_bytes()
  assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE),path
  cache[path]=(b,b.decode().splitlines(keepends=True))
 b,ls=cache[path];assert 1<=st<=en<=len(ls),(path,st,en,len(ls))
 rb=''.join(ls[st-1:en]).encode()
 return dict(id=identifier,description=desc,path=path,line_start=st,line_end=en,
             full_file_sha256=sha(b),file_sha256=sha(b),range_sha256=sha(rb),range_bytes=len(rb),
             source_commit=PIN,verified_equal_to_pinned_git_blob=True,
             url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st}-L{en}')
anchors=[]
for x in prior['source_anchors']:
 if x['id'][0] not in 'DEGNR':continue
 y=bind(x['id'],x['description'],x['path'],x['line_start'],x['line_end'])
 assert y['full_file_sha256']==x['full_file_sha256'] and y['range_sha256']==x['range_sha256']
 anchors.append(y)
def add(identifier,desc,filename,names):
 hits=[s for (path,name),s in lookup.items() if path.endswith('/'+filename+'.lean') and name in names]
 for name in names:
  if any(s['declaration']==name for s in hits):continue
  paths={path for path,_ in lookup if path.endswith('/'+filename+'.lean')}
  assert len(paths)==1,(identifier,filename,name)
  path=paths.pop();ls=(SOURCE/path).read_text().splitlines()
  pat=re.compile(r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)')
  ds=[(i,m.group(1)) for i,s in enumerate(ls) if (m:=pat.match(s))]
  found=[(j,i) for j,(i,n) in enumerate(ds) if n==name];assert len(found)==1,(identifier,name)
  j,st=found[0];en=ds[j+1][0] if j+1<len(ds) else len(ls)
  for k in range(st+1,en):
   if re.match(r'^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)',ls[k]):en=k;break
  while en>st+1 and not ls[en-1].strip():en-=1
  hits.append(dict(path=path,declaration=name,line_start=st+1,line_end=en))
 assert len(hits)==len(names),(identifier,filename,names,[s['declaration'] for s in hits])
 paths={s['path'] for s in hits};assert len(paths)==1
 anchors.append(bind(identifier,desc,paths.pop(),min(s['line_start'] for s in hits),max(s['line_end'] for s in hits)))
add('Q01','Original OMDat/Pins/OneMapOf and literal base field, row and phase conditions','OneMapT',['OMDat','Pins','OneMapOf','OMPins','OneMapRow0','PhaseTie'])
add('Q02','Selected full PinsOverL wrapper and actual exists_phi_core; retained CoversAt supply is explicit in RTG','ExistsNormalisedTupleDataOverRowFieldConditions',['exists_phi_core','pinsOverL_of_clauses'])
add('Q03','Exact higher geometric CoversAt packet with one CXiVal','ExistsCoversOfHalves',['CoversAt'])
add('Q04','Local CRT, original ChrEq adelic value bridge and complete XiVal endpoint','LocKIntMem',['locK_int_mem','locK_mem','char_mem','xiH_locK_mem','xiVal'])
add('Q05','One full coefficient extension before every tuple and representative family','ExistsCoefficientMapExtensionRationalValues',['exists_ext_placeEx'])
add('Q06','Original split representatives and all RepsOK/LatPin fields','ExistsRepsOfFiniteIndex',['exists_reps_of_finiteIndex','splitOffBad_of_suppSplit','exists_repsR_repsOK','exists_repsR_repsCov'])
add('Q07','Exact index and arbitrary odd-exponent self-dual split lattice square law','LawOfSquaresSelfDualSplitLattice',['index_eq','law_of_squares'])
add('Q08','Actual half levels, BIs and residue quotient PhiIs over the prescribed field','ExistsNormalisedTupleDataOverCoefficientField',['coverHalf_mul','exists_half_tupPrime','exists_BIs','exists_phi_over'])
add('Q09','Actual-read ratio, field-retie and base class-read comparison','OneMapOfOfPtIdent',['ratio_mem','exists_read','exists_retie'])
add('Q10','Exact common lambda/z PointIdentCore order and all-tuples LiftsSpan interface','ReferenceTupleLiftsSpanAllTuples',['PointIdentCore','liftsSpan_of_guard_core'])
add('Q11','Original scaleXi, whole Pins preservation and full OneMapOf finite consumer','OneMapOfOfPtIdent',['scaleXi','xiConst_scaleXi','pins_scaleXi','oneMapOf_of_ptIdent','const_ratio_mem'])
add('Q12','RatAt unprojected/projected distinction and exact good-projector identity','RayFieldTheta',['RatAt','proj_clause'])
add('Q13','Full same-object OneMapOverL-to-RatAt/RatG source endpoint','RatOfOneMapOverL',['ratAt_of_oneMap','rat_of_oneMapOverL'])
add('Q14','Original twisted rational basis and both-level LiftTestB','LiftTestBOfRatG',['readBasis','readBasis_coord','liftTestB_of_ratG'])
add('Q15','Exact original MK/Mcoord lattice proof and printed LatFull premise','LMLatOfLIntegral',['isLattice_comap','isLattice_span_MK','isLattice_Mcoord','mkFull_of_tie','mLat_of_tie'])
add('Q16','Remaining prescribed-field higher cover and algebraic character-section producer','CoversAtOverField',['exists_fun_of_val','coversAt_over_field'])
add('Q17','Actual moduli, level-map and Hecke-point source theorem','ModuliSchemeLevelMapsHeckePoints',['_root_.GlobalTheory.moduliScheme_levelMaps_heckePoints'])
add('Q18','Actual higher DeltaDat and all IsLev conditions','ExistsDeltaDatumHigherLevel',['exists_deltaDat_isLev'])
add('Q19','Actual algebraic finite-character section realization','ExistsSecCharVal',['exists_sec_char_val'])
add('Q20','Actual ClsEx supplier on original level/family/FWTie/base-prime equality','ReferenceTupleLiftsSpanAllTuples',['clsEx_of_core'])
add('Q21','Exact class-sum section/cuspidality/uniqueness with PsiTie and weight guards','ExistsCuspIsThClsDUnique',['exists_cusp_isThClsD_unique'])
add('Q22','Common scalar/covariance/geometric point identity implementation and original guards','CovarianceAtConstantXi',['exists_scalar_core','covAt_of_xiConst_core','point_identity_core'])
add('Q23','Actual base class-sum generation, raw theta series and finite-point comparisons with size inequality','ClassSumsSpanCuspFormsBaseTupleSecondField',['classSumsSpan_of_pins_core','classSumsSpan_core'])
add('Q24','Independent original LatFull producer: CM detection/bounded denominators and short-theta power clearing','ExistsSmulNonnegOfPow',['fullAt_of_pins'])

old={c['id']:c for c in json.loads((BASE/'provenance.json').read_text())['claims']}
bindings=[]
def component(name,root,ids,current=False):
 cs={c['id']:c for c in json.loads((root/name/'provenance.json').read_text())['claims']} if not current else {c['id']:c for c in prov['claims']}
 folder=(root/name) if not current else RTG
 item=dict(component=name,scope='Completed only in the component’s exact printed conditional scope; no outer existence is inferred.',
           origin='current v0.41 component' if current else 'frozen reconstruction_v040',files={},claims=[])
 for fn in ['main.tex','provenance.json','closure.json','published_applications.json']:
  f=folder/fn
  if f.exists():item['files'][fn]=dict(file=name+'/'+fn,sha256=sha(f.read_bytes()))
 main=(folder/'main.tex').read_bytes();ls=main.decode().splitlines(keepends=True)
 for key in ids:
  c=cs.get(key,old.get(key));assert c is not None,key
  pl=c['proof_location'];st,en=pl['line_start'],pl['line_end'];rb=''.join(ls[st-1:en]).encode()
  assert sha(rb)==pl.get('range_sha256',pl['sha256']),(key,'proof block mismatch')
  item['claims'].append(dict(id=key,line_start=st,line_end=en,proof_range_sha256=sha(rb),proof_range_bytes=len(rb)))
 bindings.append(item)
component('rational_theta',HERE.parent,[f'RTG{i}' for i in range(1,26)],True)
component('comparison_packet',BASE,['PKT21','PKT27','PKT30'])
component('common_readings',BASE,['RDR12','RDR20','RDR21','RDR22'])
component('division_identity',BASE,['DI17','DI18','DI19','DI20','DI21'])
component('row_integrability',BASE,['RPI14','RPI15'])
component('common_selected',BASE,['CSR9','CSR11','CSR16','CSR22'])
component('small_level_rank',BASE,['SLR7','SLR8'])
component('base_theta',BASE,['BTH8','BTH11','BTH12','BTH13'])
component('coefficient_fock_bridge',BASE,['CFB1','CFB13'])

note=HERE/'next_division_and_readings.txt'
result=dict(schema='rh-continuation-source-audit/1',artifact_version='0.41',note=note.name,note_sha256=sha(note.read_bytes()),
            source_commit=PIN,status='Source-grounded continuation and current-proof scope audit; no new theorem or whole-leaf closure.',
            formal_proof_assumption='Pinned Alpoge-Claude proof accepted as fully checked and correct; open statuses concern human reconstruction only.',
            scope='Exact surviving rational-theta geometry, integral fullness, common realization/Fits/eta guards and stronger second DivRows3 after RTG finite consumer closure.',
            source_anchors=sorted(anchors,key=lambda x:x['id']),component_bindings=bindings,
            validation=dict(status='PASS',source_ranges=len(anchors),distinct_source_files=len(cache),component_count=len(bindings),
              checks=['Every exact source range and whole file verified against pinned Git blob','All current and inherited component file/proof-block hashes checked','No Lean build or replay','No component mathematical file modified by this builder']),
            metadata_builder=dict(file=Path(__file__).name,sha256=sha(Path(__file__).read_bytes()),
              portable_invocation='python3 build_next_division_sources.py --source /path/to/lean_source --baseline /path/to/reconstruction_v040 --component /path/to/rational_theta'))
out=HERE/'next_division_and_readings_sources.json';out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(note_sha256=result['note_sha256'],manifest_sha256=sha(out.read_bytes()),**result['validation']),indent=2))
