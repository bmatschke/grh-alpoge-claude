#!/usr/bin/env python3
"""Bind the human HTW proof to the original local-operator/TW contracts."""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMP='hida_taylor_wiles_v45'
AV='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DENSE=AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
NIL=AV+'PatchingModules/NilpotentLevelLowering/'
ALG=AV+'AlgebraTools/'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
cache={}
def src(path,a=1,b=None):
    if path not in cache:
        data=(SOURCE/path).read_bytes()
        assert data==subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path]),path
        cache[path]=data
    data=cache[path]; lines=data.splitlines(keepends=True)
    b=len(lines) if b is None else b
    assert 1<=a<=b<=len(lines),(path,a,b,len(lines))
    part=b''.join(lines[a-1:b])
    return {'path':path,'line_start':a,'line_end':b,'file_sha256':sha(data),
      'sha256':sha(data),'range_sha256':sha(part),'range_bytes':len(part),
      'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,
      'url':'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path+f'#L{a}-L{b}'}
def d(n,a=1,b=None):return src(DENSE+n+'.lean',a,b)
def f(n,a=1,b=None):return src(NIL+n+'.lean',a,b)
def a(n,i=1,j=None):return src(ALG+n+'.lean',i,j)

spec={
1:([],[f('DelIso'),d('LevOpOf',21,124)]),
2:(['HTW1'],[f('EvalComm'),f('TrOfCommdc'),f('ActUVariableEqPow',44,58),d('LevOpOf',125),
 a('IwThetaEx'),a('IwDomMul'),a('IwSimpleQuad'),a('IwPermUnit'),a('IwFundNorm')]),
3:(['HTW2','HAW7'],[a('IwJqLine'),a('IwJqInj'),a('IwJqEmbed'),f('NilKill',45)]),
4:(['GUA1','GUA15'],[f('WdChar')]),
5:([],[f('LocData',17,74),a('IwTamePair'),f('PairRel')]),
6:(['HTW3','HTW4','HTW5','GUA1','GUA2','GUA3','GUA12'],[d('TLocDataT'),f('ArtinEl'),d('LocDataT'),d('LocOk')]),
7:(['HTW2','HTW3'],[d('LevRelOf')]),
8:(['HTW6','HTW7'],[d('LocOkLevelModuleOfThetaData')]),
9:(['HTW6','BCS15','UPA5','UPA6','UPA7'],[d('SymOfVieta'),d('LevSymOf')]),
10:([],[a('HkDefs',10,42),a('HkDualEx'),a('HkDualExp'),a('HkDdSpec')]),
11:(['HTW2','HTW10'],[a('HkDefs',43,59),a('HkSandwich'),a('HkSum'),a('IwBernHk'),a('IwBernFaith'),f('HkHypOf')]),
12:(['HTW9','HTW10','HTW11'],[f('MultiPhi'),f('MultiPsi'),f('MultiTwo')]),
13:(['HTW12'],[f('TwoMul'),d('LevTwoOf')]),
14:(['HTW1','HTW2','HTW8','HTW13'],[d('LevOpOf'),f('LevelModule',40,88)]),
15:([],[f('OpParts',20,149),a('TopNilMapMem')]),
16:(['HTW15'],[f('PsModule'),f('PsLinSmall'),f('OpParts',151,194)]),
17:(['HTW1','HTW15','HTW16'],[f('FreeSummand'),f('OpParts',196,251)]),
18:(['HTW1','HTW15'],[f('OpParts',276,429)]),
19:(['HTW13','HTW15','HTW16'],[f('SpLocIdem'),f('OpParts',431)]),
20:([],[f('OpToTW',181),src(AV+'PatchingModules/ThetaCoefficientMapEq.lean',163,236)]),
21:(['HTW8','HTW14','HTW16','HTW17','HTW18','HTW19','HTW20'],[f('OpToTW'),src(AV+'PatchingModules/ThetaCoefficientMapEq.lean',188,236)]),
22:([],[f('OpTransport')]),
23:(['HTW6','HTW14','HTW21','HTW22'],[d('THasAutOf'),d('PaLevel',24),src(AV+'PatchingModules/ThetaCoefficientMapEq.lean',238,246),src(AV+'PatchingModules/TaylorWilesObstructionBound.lean',147,154)]),
24:(['HTW23','HLM26'],[d('BaseObjectHomExt',129),d('THasAutOf'),d('PaLevel',42)])
}
scopes={
1:'The actual tame quotient, its specified diagonal generators, projective norm isomorphism and exact augmentation kernel; no division by group order.',
2:'Full ThData and trace on the actual tame/Iwahori fixed modules, including arbitrary torus elements and exact Q^i normalization.',
3:'Jacquet dimension at most n! and polynomial nilpotence of that exponent, including arbitrary local isotypic multiplicity.',
4:'Actual Weil characteristic polynomials and triviality on the original tame kernel under a unipotent characteristic polynomial; no replacement by semisimplified inertia.',
5:'The ordered matrix relation for nonresonant geometric Frobenius, with distinct and Q-separated roots; the character-polynomial premise holds at every group element.',
6:'Full LocDataTAlt and LocalLevelConditions consumer, retaining the guarded spherical/nonresonant alternatives and all IsRecT and prolongation quantifiers.',
7:'Integral vector-level descent of single-place polynomial nilpotence from every original LevPtAlt and every joint generalized torus character.',
8:'Both exact fEl-weighted trace-polynomial relations for every group element, with one exponent n! independent of the number of auxiliary places.',
9:'Elementary symmetric operator identities on the original maximal-compact fixed module, with the exact original Frobenius polynomial and beta.',
10:'Explicit integral divided-difference dual family and both expansion identities, including n=0,1; no inversion of n! or of a root difference on a module.',
11:'Actual finite Iwahori trace, integral dual sum and spherical sandwich identities with exact U_i=Q^i Theta(e_i(x)) normalization.',
12:'Both original semilinear comparison maps for the simultaneous ordered splitting algebra, with their explicit finite formulas and product correction.',
13:'Both compositions multiplied up to the literal ordered-pair fEl, without localizing or assuming its nonvanishing.',
14:'Every original OpMod and OpRel field from the actual LevMod and local conditions; same b, J, coefficient ring and exponent.',
15:'Canonical joint topologically nilpotent summand on finite modules over complete noetherian local Lambda, and full centralizer functoriality.',
16:'Power-series actions and full semilinearity from polynomial identities on finite complete modules.',
17:'Finite freeness over the exact Sinf/delIdeal quotient with each exponent a_j>=N; all diamond generators retained.',
18:'Exact augmentation quotient and its split identification with the ordered-root primary summand of the Iwahori module.',
19:'The original completed ordered splitting ring and restriction of both maps by actual idempotents, retaining exact fEl identities.',
20:'Original R-prime, full pair, s and theta with the exact theta_coefficientMap_eq, all weight variables and ordered root images.',
21:'Every TWRing and TWMaps field, both full polynomial-law trace relations on every vector, with unchanged exponent n!.',
22:'Literal opTransport along the original bijective global-data map, including residual and type kernels, all group elements and the same base.',
23:'Complete HasAutOfAlt conditional on literal LevelAlt; one b before all auxiliary levels, one root lift before N, one exponent n!, all original TW families.',
24:'Actual full same-J HasAut from HLM26 for every original positive rank, with prime 3 included; no unsupported full selected leaf closure.'
}
folder=ROOT/COMP
data=(folder/'main.tex').read_bytes(); lines=data.splitlines(keepends=True)
claims=[]
for k,(deps,sources) in spec.items():
    cid='HTW'+str(k)
    start=next(i+1 for i,s in enumerate(lines) if s.strip()==('% BEGIN '+cid).encode())
    stop=next(i+1 for i,s in enumerate(lines) if s.strip()==('% END '+cid).encode())
    block=b''.join(lines[start-1:stop])
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*)\}\n',block.decode())[1]
    claims.append({'id':cid,'title':title,'introduced_in':'0.45','classification':'B',
      'status':'Complete human proof in the stated original scope; independent review recorded separately',
      'scope':scopes[k],'depends_on':deps,
      'proof_location':{'file':COMP+'/main.tex','label':'claim:'+cid,'line_start':start,'line_end':stop,
        'sha256':sha(block),'file_sha256':sha(data),'bytes':len(block)},'sources':sources})
allclaims={c['id']:c for c in json.loads((ROOT/'history/version_0_44/provenance.json').read_text())['claims']}
for p in ROOT.glob('*_v45/provenance.json'):
    if p.parent.name!=COMP:
        allclaims.update({c['id']:c for c in json.loads(p.read_text()).get('claims',[])})
bindings=[]
for cid in sorted({dep for c in claims for dep in c['depends_on'] if not dep.startswith('HTW')}):
    c=allclaims[cid]; pl=c['proof_location']; raw=(ROOT/pl['file']).read_bytes()
    block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert sha(block)==pl['sha256'],cid
    bindings.append({'claim':cid,'proof_file':pl['file'],'file_sha256':sha(raw),'line_start':pl['line_start'],
      'line_end':pl['line_end'],'range_sha256':sha(block),'introduced_in':c.get('introduced_in')})
reviews=[]
for p in sorted(folder.glob('review_*.json')):
    r=json.loads(p.read_text())
    if r.get('proof_sha256',r.get('reviewed_sha256'))==sha(data):
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'result':r.get('result',r.get('status'))})
boundary={
 'endpoint':'Full LocDataTAlt/local conditions, OpMod/OpRel with exponent n!, opTransport, opToTW, HasAutOfAlt, and actual same-J HasAut from HLM26.',
 'original_inputs_retained':[
  'Exactly the original LocPAlt: Bernstein-Zelevinsky finiteness, geometric lemma, and TameLocal, with their original field/rank/coefficient scope.',
  'Full original IsRecT existence and laws and the already reconstructed GUA generic and spherical good-parameter consequences.',
  'The actual LevelAlt from HLM26, retaining its original HypothesesHprime, CohP/LocCFT and coefficient hypotheses, universal ring, same J, one b and all auxiliary families.',
  'Original complete noetherian coefficient-ring and finite-module algebra; the intervening idempotent, norm, finite Hecke, matrix and polynomial-law consumers are proved here.'
 ],
 'not_asserted':[
  'The full selected COUNT_II_SUPPORT leaf and both rank-four Link installations are not closed merely by this component.',
  'The original named local published foundations are not reproved or replaced with stronger assumptions.',
  'No Lean build, kernel replay, or completed human RH/Dirichlet-GRH proof is asserted.'
 ]}
write(folder/'provenance.json',{'schema':'rh-human-component-provenance/1','artifact_version':'0.45',
 'date':'2026-11-23','component':COMP,'source_commit':PIN,'main_tex_sha256':sha(data),
 'proof_file_sha256':sha(data),**boundary,'claims':claims,'inherited_claim_bindings':bindings,
 'independent_reviews':reviews,'no_lean_replay':True})
write(folder/'original_contracts.json',{'component':COMP,'source_commit':PIN,**boundary,'claims':[c['id'] for c in claims]})
write(folder/'closure.json',{'artifact_version':'0.45','component':COMP,'main_tex_sha256':sha(data),
 'complete_nested_endpoints':boundary['endpoint'],'whole_selected_leaf_closed':False,
 'same_ideal_required':True,'uniform_exponent':'n!','quantifier_order':'One b before all levels, one residual root lift before N, then all N with one exponent.',
 'boundary':boundary['not_asserted'],'independent_reviews':reviews})
write(folder/'retained_foundations.json',{'component':COMP,'proof_sha256':sha(data),'foundations':boundary['original_inputs_retained']})
unique={(s['path'],s['line_start'],s['line_end']):s for c in claims for s in c['sources']}
write(folder/'source_manifest.json',{'source_commit':PIN,'ranges':list(unique.values()),'range_count':len(unique),'file_count':len(cache)})
report=[COMP+' — version 0.45','23 November 2026','',boundary['endpoint'],'','RETAINED ORIGINAL INPUTS',
 *boundary['original_inputs_retained'],'','BOUNDARY',*boundary['not_asserted'],'','CLAIMS']
for c in claims:report.extend([c['id']+': '+c['title'],c['scope'],'Dependencies: '+', '.join(c['depends_on'])])
(folder/'report.txt').write_text('\n'.join(report)+'\n')
print(json.dumps({'component':COMP,'claims':len(claims),'files':len(cache),'ranges':len(unique),
 'proof_sha256':sha(data),'inherited_or_same_round_bindings':len(bindings),'bound_reviews':len(reviews)}))
