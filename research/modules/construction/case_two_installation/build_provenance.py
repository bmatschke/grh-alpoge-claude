#!/usr/bin/env python3
"""Bind the complete conditional case-II count to exact original sources."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent / 'lean-source'
COMP = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
SG = AV + 'SymplecticGSp4/'
HV = AV + 'HeightAndVanishing/'
files = {}

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(n, x): (HERE/n).write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
def source(path, name, role):
    raw = (REPO/path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pat = r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)'
    starts = [(i,m.group(1)) for i,l in enumerate(lines,1) if (m:=re.match(pat,l.decode()))]
    hits = [(i,n) for i,n in starts if n==name or n.endswith('.'+name)]
    assert len(hits)==1,(path,name,hits)
    a,n = hits[0]
    b = min([i for i,_ in starts if i>a] or [len(lines)+1])-1
    while not lines[b-1].strip(): b-=1
    piece = b''.join(lines[a-1:b])
    if path not in files:
        assert raw==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
        files[path]=dict(path=path,sha256=sha(raw),bytes=len(raw),lines=len(lines),
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}')
    return dict(path=path,declaration=n,line_start=a,line_end=b,sha256=sha(raw),
        range_sha256=sha(piece),range_bytes=len(piece),role=role,
        url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{b}')

specs = {
 'YX1': [
  (AV+'WeakShimuraTheory/NearSplit.lean','Ctx2','Exact original case-II scope; no case-III quantifier is inferred'),
  (DT+'PotentialModularityTower.lean','PMExAlt','Only retained actual input, uniform before every later Space'),
  (DT+'PotentialModularityTower.lean','SeedIIAlt','Actual complete SX8 seed at every fixed iota and original tower'),
  (DT+'PotentialModularityTower.lean','ProModAlt','Entire actual UX12 witness, including the original coefficient and inertia equalities'),
  (DT+'Gsp4PromodularityCaseTwo.lean','proMod_of_pmEx_of_ctx2_of_kPair_of_star','Literal complete case-II implication reconstructed by UX12'),
  (SG+'DecompSigmaOrd.lean','Fin0','Actual original-data finiteness endpoint'),
  (SG+'DecompSigmaOrd.lean','NoEnd','Actual original-data exclusion endpoint'),
  (SG+'DecompSigmaOrd.lean','AllIrr','Every original irreducible point under one previously fixed embedding'),
  (DT+'IsAut4.lean','IsAut4Alt','Exact resulting automorphic-point record'),
  (DT+'IsAut4.lean','SymplecticFourImageDense','Full ambient source endpoint, of which only the Ctx2 restriction is supplied')
 ],
 'YX2': [
  (HV+'Counts.lean','CountShape','Character constant chosen before every varying host, coefficient ring and case datum'),
  (HV+'Counts.lean','CountII','The literal completed conditional count'),
  (HV+'Counts.lean','CountI','Retained height-assembly count'),
  (HV+'Counts.lean','CountIII','Retained distinct case-III count'),
  (HV+'Counts.lean','CountV','Retained height-assembly count'),
  (DT+'AfStmt.lean','NumberSp4Alt','Exact complete CX9 catalogue and uniform integer/trace quantifiers'),
  (DT+'AfStmt.lean','AdmRAlt','Actual level, weights, dual, safe and automorphic record on the case-II datum'),
  (DT+'RigEnd3.lean','RigiditySymplecticFour','Actual pointwise RX6 rigidity; the global RX7 premise is not assumed'),
  (SG+'EntryMem.lean','CohomologyHyp','Complete BX8 cohomology supplier'),
  (SG+'DecompSigmaOrd.lean','Ineq','Actual cotangent/trace inequality with the factor two'),
  (DT+'CountS.lean','exists_frob_nonvanishing_with_sha_bound','Finite-family Frobenius product and exact catalogue guard'),
  (SG+'ValProd.lean','shaEq','Original strict Selmer to auxiliary length comparison'),
  (SG+'TwoPowClogLe.lean','arith','Uniform arithmetic absorption at the original case-II parameters'),
  (DT+'ConductorAtMapInjectiveCoeff.lean','main_big','Same-datum count assembly before coefficient return, applied pointwise in Case II'),
  (DT+'ConductorAtMapInjectiveCoeff.lean','sp4Main_alt','Exact normalized coefficient return; the paired endpoint is not claimed unconditionally'),
  (HV+'LayerLe.lean','PointHV','Original-field height endpoint under the three other retained counts'),
  (HV+'JointWinOfCounts.lean','pointHV_of_counts','Entire four-count height join'),
  (HV+'JointWinOfCounts.lean','jointWin_of_counts','Guarded common-window consequence'),
  (HV+'JointWinOfCounts.lean','vwin_of_counts','Original window with the previously stated prime-pair inputs')
 ]
}
deps = {
 'YX1':['SX8','UX12','BX8','TW1','IX8','IX9','IX10'],
 'YX2':['YX1','AX5','AX6','AX7','AX8','AX9','BX8','RX6','CX9','DX2','DX4','DX8',
        'MX10','PX10','SP8','SP10','RV1','HV5','HV6','CZ6','HV10','TW8','OB8','VW3','VW4']
}
titles = {'YX1':'Complete original case-II image-density implication from PMExAlt',
          'YX2':'Complete original case-II count implication from PMExAlt'}
scopes = {
 'YX1':'PMExAlt implies Fin0, NoEnd and AllIrr(IsAut4Alt iota) on every original Ctx2 datum, with iota fixed before all ambient points and coefficient witnesses.',
 'YX2':'PMExAlt implies the literal CountII with its original field, normalized lengths and full uniformity; CountI, CountIII, CountV and PMExAlt consequently suffice for PointHV, and the existing prime-pair inputs give the guarded window consequences.'
}
retained = {
 'YX1':['The literal PMExAlt, including its uniform coefficient threshold and all five clauses on every actual Space.'],
 'YX2':['The literal PMExAlt for CountII.',
        'For the height consequence only: literal CountI, CountIII and CountV.',
        'For the window consequences only: the previously stated prime-pair hypotheses.']
}
old = read(ROOT/'history/version_0_28/provenance.json')
allclaims = {c['id']:c for c in old['claims']}
for comp in ['symplectic_automorphic_seeds','symplectic_promodular_realization']:
    for c in read(ROOT/comp/'provenance.json')['claims']: allclaims[c['id']]=c
external=[]
for cid in sorted(set(sum(deps.values(),[]))-set(deps)):
    c=allclaims[cid]
    external.append(dict(claim_id=cid,title=c['title'],
        proof_location=copy.deepcopy(c.get('proof_location',c.get('human_proof',{}))),
        use='Only the exact scope proved in this supplier is substituted; restricted pointwise applications are explicit.'))

raw=(HERE/'main.tex').read_bytes()
lines=raw.splitlines(keepends=True)
claims=[]
for cid in deps:
    begin=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% BEGIN '+cid)
    a=next(i for i,l in enumerate(lines,1) if i>begin and l.decode().startswith('\\begin{'))
    b=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% END '+cid)-1
    while not lines[b-1].strip(): b-=1
    assert lines[b-1].decode().strip()==r'\end{proof}'
    piece=b''.join(lines[a-1:b])
    claims.append(dict(id=cid,title=titles[cid],status='Complete human proof of the exact conditional implication',
        introduced_in='0.29',scope=scopes[cid],depends_on=deps[cid],remaining_inputs=retained[cid],
        classical_inputs=['Inherited precisely matched leaves of the explicitly cited completed supplier claims.'],
        source_relation='Exact case-II restricted reconstruction with actual seed and promodular witnesses; no full two-case image-density premise is substituted.',
        proof_location=dict(file=COMP+'/main.tex',label='claim:'+cid,line_start=a,line_end=b,sha256=sha(piece),bytes=len(piece)),
        sources=[source(*s) for s in specs[cid]]))
validation=dict(claim_count=len(claims),claim_source_links=sum(len(c['sources']) for c in claims),
    source_files_checked_against_pinned_git_blobs=len(files),main_tex_sha256=sha(raw),
    unconditional_PMExAlt_claimed=False,unconditional_CountII_claimed=False,
    full_SymplecticFourImageDense_claimed=False,case_III_producer_claimed=False,
    no_new_lean_build_or_kernel_replay=True)
out=dict(schema='rh-human-reconstruction-provenance/1',artifact_version='0.29',date='2026-11-22',
    commit=PIN,repository=old['repository'],component=COMP,main_tex_sha256=sha(raw),
    scope='The complete case-II count chain from the one actual PMExAlt input, with every intermediate original-object supplier reconstructed.',
    claims=claims,source_files=list(files.values()),dependency_graph=deps,
    external_claim_dependencies=external,retained_inputs=retained,validation=validation)
dump('provenance.json',out)
dump('closure.json',dict(schema='rh-human-component-closure/1',artifact_version='0.29',component=COMP,commit=PIN,
    main_tex_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
    closed_claim_ids=list(deps),dependency_graph=deps,external_claim_dependencies=external,
    endpoints=[dict(name=cid,scope=scopes[cid],retained_inputs=retained[cid]) for cid in deps],
    no_new_lean_build_or_kernel_replay=True))
dump('input_registry.json',dict(schema='rh-component-input-registry/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),claim_inputs=external,retained_inputs=retained,new_classical_theorem_inputs=[]))
dump('remaining_inputs.json',dict(schema='rh-component-remaining-inputs/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),retained_inputs=retained,
    independent_global_branches=['Actual CountI, CountIII and CountV','Actual common family and arithmetic gap',
        'Genuine theta/local installation','Actual denominator tables','Exact metric/global/spectral comparisons']))
dump('next_targets.json',dict(schema='rh-next-source-targets/1',artifact_version='0.29',component=COMP,targets=[],
    explanation='The semantic audit narrows the entire case-II chain to PMExAlt. The compound older targets retain case IV seeds, case III promodularity, and the actual Hecke/support producer.'))
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(
    s['declaration']+'\n'+s['url']+'\n'+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
(HERE/'report.txt').write_text('Version 0.29 — one complete case-II chain\n\n'+
    '\n'.join(cid+': '+scopes[cid] for cid in deps)+
    '\n\nPMExAlt remains an actual arithmetic input. No unconditional RH/Dirichlet-GRH conclusion or case-III supplier is claimed.\n'+json.dumps(validation,indent=2)+'\n')
print(json.dumps(validation,indent=2))
