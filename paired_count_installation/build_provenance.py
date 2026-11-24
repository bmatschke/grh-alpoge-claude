#!/usr/bin/env python3
"""Bind the complete conditional paired-count and height joins to original sources."""
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
CB = 'src/Development/AutomorphicArithmetic/CharacterBoxes/'
files = {}

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(name, obj): (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
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
    piece=b''.join(lines[a-1:b])
    if path not in files:
        assert raw==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
        files[path]=dict(path=path,sha256=sha(raw),bytes=len(raw),lines=len(lines),
                         verified_equal_to_pinned_git_blob=True,
                         url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}')
    return dict(path=path,declaration=n,line_start=a,line_end=b,sha256=sha(raw),
                range_sha256=sha(piece),range_bytes=len(piece),role=role,
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{b}')

specs={
 'JX1':[
  (DT+'IsAut4.lean','SymplecticFourImageDense','The sole retained paired-count input, applied on the original datum before choosing irreducible points'),
  (DT+'AfStmt.lean','NumberSp4Alt','Literal CX9 endpoint and all uniform integer/trace quantifiers'),
  (DT+'AfStmt.lean','AdmRAlt','Exact original irreducibility, automorphy, level, dual and safe conditions'),
  (DT+'RigEnd3.lean','RigiditySymplecticFour','Literal RX6 endpoint, installed on the same datum by RX7'),
  (SG+'EntryMem.lean','CohomologyHyp','Entire BX8 record'),
  (SG+'DecompSigmaOrd.lean','Fin0','Actual same-datum finiteness supplied by image density'),
  (SG+'DecompSigmaOrd.lean','NoEnd','Actual same-datum exclusion supplied by image density'),
  (SG+'DecompSigmaOrd.lean','AllIrr','One common embedding and then every actual irreducible point'),
  (SG+'DecompSigmaOrd.lean','RigidAt','Original dual-number rigidity used in PX'),
  (SG+'DecompSigmaOrd.lean','Ineq','Actual trace/cotangent inequality including factor two'),
  (DT+'CountS.lean','exists_frob_nonvanishing_with_sha_bound','Exact catalogue guard and finite-family trace product'),
  (SG+'ValProd.lean','shaEq','Original strict Selmer to auxiliary Selmer length comparison'),
  (SG+'TwoPowClogLe.lean','arith','Uniform arithmetic absorption with original case parameters'),
  (HV+'Counts.lean','CountShape','Exact character/host/coefficient/local-condition quantifier order'),
  (HV+'Counts.lean','CountII','Original case II endpoint'),
  (HV+'Counts.lean','CountIII','Original case III endpoint'),
  (DT+'ConductorAtMapInjectiveCoeff.lean','main_big','Original common-datum count joins before coefficient return'),
  (DT+'ConductorAtMapInjectiveCoeff.lean','sp4Main_alt','Entire paired-count endpoint including exact normalized coefficient return')
 ],
 'JX2':[
  (HV+'Counts.lean','CountI','Retained actual first count'),
  (HV+'Counts.lean','CountV','Retained actual filtration count'),
  (DT+'IsAut4.lean','SymplecticFourImageDense','Retained third member of the sufficient cut'),
  (HV+'LayerLe.lean','PointHV','Original height endpoint on all original hosts and fields'),
  (HV+'JointWinOfCounts.lean','pointHV_of_counts','Entire HV10 original-field count-to-height join'),
  (HV+'JointWinOfCounts.lean','thmHV_of_counts','Original quantified height theorem'),
  (HV+'JointWinOfCounts.lean','jointWin_of_counts','Common-window count join'),
  (HV+'JointWinOfCounts.lean','vwin_of_counts','Original window endpoint with existing prime-pair hypotheses'),
  (AV+'PrimeSetBoundDataOfPrimitiveChar.lean','ThmBab','TW8 common record before all Ct>=1'),
  (AV+'PrimeSetBoundDataOfPrimitiveChar.lean','ThmBcFree','OB8 odd-minus statement with constant 240'),
  (AV+'PrimeSetBoundDataOfPrimitiveChar.lean','JointWin','Exact common-window quantifiers'),
  (CB+'ExistsPageN.lean','VWinAt','Actual original-field window statement'),
  (CB+'WinPairs.lean','winPairs','Fixed-pair specialization with Ct=401 and cutoff 400')
 ]
}
deps={
 'JX1':['BX8','RX7','CX9','AX10','MX10','PX10','SP10'],
 'JX2':['JX1','HV10','TW8','OB8','VW3','VW4']
}
titles={'JX1':'Complete original paired-count implication from image density',
        'JX2':'Reduced original-field height and window sufficient input'}
scopes={
 'JX1':'SymplecticFourImageDense implies the literal CountII and CountIII, with constants before all varying hosts, original fields, coefficient rings and case data; exact factor two and normalized return.',
 'JX2':'CountI and CountV and SymplecticFourImageDense imply literal PointHV; with the existing prime-pair inputs, the original window and Ct=401 fixed-pair consequence follow.'
}
retained={
 'JX1':['The literal SymplecticFourImageDense on every original admissible datum.'],
 'JX2':['The literal CountI.','The literal CountV.','The literal SymplecticFourImageDense.','The previously stated prime-pair inputs for the window/fixed-pair consequences.']
}
old=read(ROOT/'history/version_0_27/provenance.json')
allclaims={c['id']:c for c in old['claims']}
for comp in ['bloch_kato_installation','symplectic_actual_rigidity','symplectic_automorphic_catalogue']:
    for c in read(ROOT/comp/'provenance.json')['claims']: allclaims[c['id']]=c
external=[]
for cid in sorted(set(sum(deps.values(),[]))-set(deps)):
    c=allclaims[cid]
    loc=c.get('proof_location',c.get('human_proof',{}))
    external.append(dict(claim_id=cid,title=c['title'],proof_location=copy.deepcopy(loc),
                         use='Only the exact scope stated in the existing proof is substituted.'))

raw=(HERE/'main.tex').read_bytes(); lines=raw.splitlines(keepends=True); claims=[]
for cid in deps:
    begin=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% BEGIN '+cid)
    a=next(i for i,l in enumerate(lines,1) if i>begin and l.decode().startswith('\\begin{'))
    b=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% END '+cid)-1
    while not lines[b-1].strip(): b-=1
    assert lines[b-1].decode().strip()==r'\end{proof}'
    piece=b''.join(lines[a-1:b])
    claims.append(dict(id=cid,title=titles[cid],status='Complete human proof of the exact conditional implication',
                       introduced_in='0.28',scope=scopes[cid],depends_on=deps[cid],
                       remaining_inputs=retained[cid],classical_inputs=['Inherited precisely matched leaves of the explicitly cited supplier claims.'],
                       source_relation='Original count/height/window join, with complete alternate suppliers for actual rigidity and the rank-four catalogue.',
                       proof_location=dict(file=COMP+'/main.tex',label='claim:'+cid,line_start=a,line_end=b,sha256=sha(piece),bytes=len(piece)),
                       sources=[source(*s) for s in specs[cid]]))
out=dict(schema='rh-human-reconstruction-provenance/1',artifact_version='0.28',date='2026-11-22',
         commit=PIN,repository=old['repository'],component=COMP,main_tex_sha256=sha(raw),
         scope='Complete conditional paired-count and height/window joins, retaining exact original objects and uniformity.',
         claims=claims,source_files=list(files.values()),dependency_graph=deps,
         external_claim_dependencies=external,retained_inputs=retained,
         validation=dict(claim_count=len(claims),claim_source_links=sum(len(c['sources']) for c in claims),
                         source_files_checked_against_pinned_git_blobs=len(files),main_tex_sha256=sha(raw),
                         unconditional_image_density_claimed=False,unconditional_CountII_III_claimed=False,
                         unconditional_PointHV_claimed=False,no_new_lean_build_or_kernel_replay=True))
dump('provenance.json',out)
dump('closure.json',dict(schema='rh-human-component-closure/1',artifact_version='0.28',component=COMP,commit=PIN,
                        main_tex_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
                        closed_claim_ids=list(deps),dependency_graph=deps,external_claim_dependencies=external,
                        endpoints=[dict(name=cid,scope=scopes[cid],retained_inputs=retained[cid]) for cid in deps],
                        no_new_lean_build_or_kernel_replay=True))
dump('input_registry.json',dict(schema='rh-component-input-registry/1',artifact_version='0.28',component=COMP,
                               main_tex_sha256=sha(raw),claim_inputs=external,retained_inputs=retained,
                               new_classical_theorem_inputs=[]))
dump('remaining_inputs.json',dict(schema='rh-component-remaining-inputs/1',artifact_version='0.28',component=COMP,
                                 main_tex_sha256=sha(raw),retained_inputs=retained,
                                 independent_global_branches=['Actual common family and arithmetic gap','Genuine theta/local installation','Actual denominator tables','Exact metric/global/spectral comparisons']))
dump('next_targets.json',dict(schema='rh-next-source-targets/1',artifact_version='0.28',component=COMP,targets=[],
                             explanation='Semantic audit narrows the paired-count cut to image density and the selected height cut to CountI, CountV and image density; it does not retire those actual suppliers.'))
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\n'+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
(HERE/'report.txt').write_text('Version 0.28 — original paired-count and height joins\n\n'+'\n'.join(cid+': '+scopes[cid] for cid in deps)+'\n\nThe implications are completely reconstructed. Their image-density and remaining-count premises are explicit; the full RH/Dirichlet-GRH reconstruction remains unfinished.\n'+json.dumps(out['validation'],indent=2)+'\n')
print(json.dumps(out['validation'],indent=2))
