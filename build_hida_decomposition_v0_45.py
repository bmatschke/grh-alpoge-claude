#!/usr/bin/env python3
"""Bind HED1--HED16 to the original source and frozen predecessor claims."""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMP='hida_decomposition_v45'
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DENSE=AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
FAM=AV+'ModularityArgument/AutomorphyLifting/UnitaryGaloisFamilies/'
FOUND='src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/'
BUILD=AV+'BuildingsResidueChars/'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cache={}
def src(path,a=1,b=None):
    if path not in cache:
        data=(SOURCE/path).read_bytes()
        assert data==subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path]),path
        cache[path]=data
    data=cache[path];lines=data.splitlines(keepends=True)
    b=len(lines) if b is None else b
    assert 1<=a<=b<=len(lines),(path,a,b,len(lines))
    part=b''.join(lines[a-1:b])
    return {'path':path,'line_start':a,'line_end':b,'file_sha256':sha(data),'sha256':sha(data),
      'range_sha256':sha(part),'range_bytes':len(part),'source_commit':PIN,
      'verified_equal_to_pinned_git_blob':True,
      'url':'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path+f'#L{a}-L{b}'}
def d(n,a=1,b=None):return src(DENSE+n+'.lean',a,b)
def f(n,a=1,b=None):return src(FAM+n+'.lean',a,b)

spec={
 1:([],[d('HeckeIdealEnd',27,36)]),
 2:(['HED1'],[d('HeckeIdealEnd',37,42),d('HeckeIdealEnd',67,73)]),
 3:(['HED1','HED2'],[d('HeckeIdealEnd',43,54)]),
 4:(['HED2','HED3','AFS8','HEP12','UPA17'],[d('HeckeIdealEnd',55,73),d('UnitaryHeckeData',38,74)]),
 5:([],[d('JEnd1W',17,30),src(AV+'HeckeAlgebras/OrdinaryHeckeCharacters/IrrOfComp.lean',42,59)]),
 6:([],[src(BUILD+'IsSplitAtOfUnramifiedOfInertiaDegEqOne.lean')]),
 7:(['CAP6'],[src(AV+'AutomorphicForms/CharpolyEqProd.lean',74)]),
 8:(['GUA1','GUA12','GUA14'],[f('FrobTwT',12)]),
 9:([],[src(AV+'AutomorphicForms/CharpolyEqProd.lean',30,55),src(BUILD+'FrobeniusEigenvaluesTwist.lean')]),
 10:(['BCS18','GUA8','GUA9'],[f('MemOfProdEq',41,54),f('IrrCaseT',65,72)]),
 11:(['HED6','HED8','HED9','HED10','GUA6','GUA13','GUA14'],[f('MemOfProdEq',53,72)]),
 12:(['HED7','HED9','HED10','HED11'],[f('MemOfProdEq',53,73)]),
 13:(['BCS1','BCS5','BCS8','BCS9','BCS14','BCS15','GUA12'],[src(FOUND+'StringRepresentations/GalAut.lean',12,17)]),
 14:(['HED8','HED12','HED13','GUA13'],[f('MemOfProdEq',74,111)]),
 15:(['HED10','HED11','HED12','HED13','HED14','BCS18','GUA8'],[f('MemOfProdEq',41,111),d('GalUnitaryT',40,42),d('GuWrap',22,24)]),
 16:(['HED4','HED5','HED15','UPA1'],[d('JEnd1W',17,30),src(FOUND+'AdmissibleResidues/ArithmeticPointDecomposition.lean',26,34)])
}
scopes={
1:'Arbitrary surjective O-algebra quotient and every field point killing its kernel.',
2:'Equality of complete polynomial laws after composition of coefficient maps and group pullback, over every scalar algebra.',
3:'Original Out.pt transfer, preserving the same weight character, representation, property and full evaluated determinant; no Good guard on these fields.',
4:'Literal hecke_ideal_end for all original data and n>=1; same IsJ, all arithmetic x on J, top-ideal branch, full UnitaryPointProperties and x.IsRep after V.pr.',
5:'Actual V.pr surjectivity and continuous semisimple pullback; invariant complements on unchanged vector spaces.',
6:'Every degree-one place of the original everywhere-finite-unramified CM quadratic extension splits over the maximal real field.',
7:'Full characteristic-polynomial product identity for every group element from cofinite degree-one Frobenius comparison; continuity only over Qbar_l.',
8:'Literal frobTwT at every w away from ell and every real shift t, retaining every prolongation, permissible correspondence and Frobenius lift.',
9:'Original cyclotomic inverse powers, all multiplicities, all inertia groups and arithmetic lifts; continuous twists.',
10:'One initial rank-a_i Galois representation for every original cusp, real shift (d_i-n)/2 and all inherited local/period quantifiers.',
11:'Degree-one Frobenius comparison for the arbitrary supplied R, all positive string lengths and the original negative cyclotomic exponents.',
12:'Every-group-element cyclotomic-string product with positive ranks/lengths and continuous initial representations.',
13:'Strict local spherical Satake interval for each generic unitarisable component; no place-uniform gap and no new Jacquet-Shalika application.',
14:'When every string length equals one, the original strict cofinite ratio at all finite places, every FrobEig multiset and pair of roots; no added split or nonzero-root guard.',
15:'Full original endShapeT and endShape_alt with original given continuous semisimple R, all split-component compatibility, all ranks and odd coefficient primes.',
16:'Complete original ArithmeticPointDecomposition/end1 at the exact same IsJ ideal, retaining V.Sprime=s.S and requiring arithmetic points only.'}
folder=ROOT/COMP;data=(folder/'main.tex').read_bytes();lines=data.splitlines(keepends=True)
old=json.loads((ROOT/'history/version_0_44/provenance.json').read_text())
oldclaims={c['id']:c for c in old['claims']}
claims=[]
for k,(deps,sources) in spec.items():
    cid='HED'+str(k)
    a=next(i+1 for i,s in enumerate(lines) if s.strip()==('% BEGIN '+cid).encode())
    b=next(i+1 for i,s in enumerate(lines) if s.strip()==('% END '+cid).encode())
    block=b''.join(lines[a-1:b])
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*)\}\n',block.decode())[1]
    title=re.sub(r'\\texttt\{([^{}]*)\}',r'\1',title).replace('\\_','_')
    claims.append({'id':cid,'title':title,'introduced_in':'0.45','classification':'B',
     'status':'Complete written human proof in stated original scope; independent review recorded separately',
     'scope':scopes[k],'depends_on':deps,
     'proof_location':{'file':COMP+'/main.tex','label':'claim:'+cid,'line_start':a,'line_end':b,
       'sha256':sha(block),'file_sha256':sha(data),'bytes':len(block)},'sources':sources})
inherited=[]
for cid in sorted({x for c in claims for x in c['depends_on'] if not x.startswith('HED')}):
    c=oldclaims[cid];pl=c['proof_location'];p=ROOT/pl['file'];raw=p.read_bytes()
    block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert sha(block)==pl['sha256'],cid
    inherited.append({'claim':cid,'proof_file':pl['file'],'file_sha256':sha(raw),
      'line_start':pl['line_start'],'line_end':pl['line_end'],'range_sha256':sha(block)})
boundary={
 'endpoint':'Full literal hecke_ideal_end, frobTwT, endShapeT/endShape_alt and ArithmeticPointDecomposition/end1 on the original IsJ ideal.',
 'original_inputs_retained':[
  'Original HypothesesHprime, HidaSetting, level/auxiliary/residual/weight objects, universal determinant ring, coefficient DVR, fixed iota, and supplied UnitaryHeckeData and IsJ.',
  'Original BaseChangeIsobaricN and RowT/PropsB foundations, original local correspondence/classification and period laws, at exactly the scope inherited from BCS/GUA.',
  'The precisely matched generic-unitary published application BCS8 and finite Galois Chebotarev application CAP6; no extra analytic bound, no Ramanujan assertion, no Lean replay.'
 ],
 'not_asserted':[
  'The stronger place-uniform AutOffN window is not inferred from HED13; that output belongs to a separate proof.',
  'No whole selected COUNT_II_SUPPORT closure, both-Link installation, or global RH/Dirichlet-GRH completion is asserted by this component.',
  'The endpoint does not prove every original named foundational theorem anew.'
 ],
 'method':'Actual quotient-point factorization and full-law naturality; original weight/Out transfer; one HalfG seed per cusp; exact cyclotomic twists; CAP6 density for the given representation; strict local Satake window from already matched generic-unitary classification; all-place cofinite comparison by the global polynomial identity.'}
reviews=[]
for p in sorted(folder.glob('review_*.json')):
    r=json.loads(p.read_text())
    if r.get('proof_sha256',r.get('reviewed_sha256'))==sha(data):
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'result':r.get('result',r.get('status'))})
write(folder/'provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':'0.45',
 'date':'2026-11-23','component':COMP,'source_commit':PIN,'main_tex_sha256':sha(data),
 'proof_file_sha256':sha(data),**boundary,'claims':claims,'inherited_claim_bindings':inherited,
 'independent_reviews':reviews,'no_lean_replay':True})
write(folder/'original_contracts.json',{'source_commit':PIN,'component':COMP,**boundary,'claims':[c['id'] for c in claims]})
write(folder/'closure.json',{'artifact_version':'0.45','component':COMP,'main_tex_sha256':sha(data),
 'complete_nested_endpoints':boundary['endpoint'],'whole_selected_leaf_closed':False,
 'exact_Hida_fields_completed':['end1'],'same_ideal_required':True,'boundary':boundary['not_asserted'],
 'independent_reviews':reviews})
write(folder/'retained_foundations.json',{'component':COMP,'proof_sha256':sha(data),'foundations':boundary['original_inputs_retained']})
unique={(s['path'],s['line_start'],s['line_end']):s for c in claims for s in c['sources']}
write(folder/'source_manifest.json',{'source_commit':PIN,'ranges':list(unique.values()),
 'range_count':len(unique),'file_count':len(cache)})
report=[COMP+' — version 0.45','23 November 2026','',boundary['endpoint'],'',boundary['method'],
 '', 'EXACT INPUTS RETAINED',*boundary['original_inputs_retained'],'','SCOPE',*boundary['not_asserted'],'','CLAIMS']
for c in claims:
    report.extend([c['id']+': '+c['title'],c['scope'],'Dependencies: '+', '.join(c['depends_on'])])
report+=['','Every source file and inclusive range is byte-checked against '+PIN,
         'No whole selected obligation is closed by this component. Mathematical reviews and TeX checks are separate records.']
(folder/'report.txt').write_text('\n'.join(report)+'\n')
print(json.dumps({'component':COMP,'claims':len(claims),'files':len(cache),'ranges':len(unique),'proof_sha256':sha(data),'inherited_claims':len(inherited)}))
