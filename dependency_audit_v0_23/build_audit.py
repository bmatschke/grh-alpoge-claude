#!/usr/bin/env python3
"""Reproduce a scoped human-dependency audit; not a Lean dependency extractor.

No existing reconstruction records are changed. The claim DAG is assessed as
an annotated historical graph, and a separate, deliberately small sufficient-
condition graph makes retained source interfaces first-class nodes.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def write(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

# Use the exact predecessor snapshot after packaging, or the current v0.22
# record while this increment is being assembled.
BASE = ROOT/'history/version_0_22'
if not (BASE/'provenance.json').exists(): BASE = ROOT
prov = read(BASE/'provenance.json')
assert prov['artifact_version'] == '0.22'
g = {k: list(v) for k,v in prov['mathematical_dependency_graph'].items()}
reverse = {k:set() for k in g}
for a, deps in g.items():
    for b in deps:
        assert b in g, (a,b)
        reverse[b].add(a)
indegree = {k:len(v) for k,v in g.items()}
ready = sorted(k for k,v in indegree.items() if not v)
topo = []
while ready:
    a = ready.pop()
    topo.append(a)
    for b in reverse[a]:
        indegree[b] -= 1
        if not indegree[b]: ready.append(b)
unseen = set(g)
components = []
while unseen:
    todo = [min(unseen)]
    component = set(todo)
    while todo:
        a = todo.pop()
        for b in set(g[a]) | reverse[a]:
            if b not in component:
                component.add(b)
                todo.append(b)
    components.append(sorted(component))
    unseen -= component

samples = []
claims = {c['id']:c for c in prov['claims']}
for cid in ['AN2','AN3','SC2','GL1','GH5','QP25','MR22','DC21']:
    c = claims[cid]
    samples.append({
        'claim_id':cid, 'graph_dependencies':g[cid],
        'status':c['status'], 'statement':c.get('statement'),
        'remaining_inputs_field':c.get('remaining_inputs'),
        'assumptions':c.get('assumptions',[]),
        'interpretation':'A missing/empty remaining_inputs field and a zero-edge graph node do not mean that supplied hypotheses have been constructed.'
    })
targets = read(BASE/'next_source_targets.json')
write('historical_graph_audit.json', {
    'scope':'v0.22 human graph only; no Lean elaboration, proof-term traversal or semantic completeness inference',
    'source_commit':PIN,
    'inputs':{str((BASE/f).relative_to(ROOT)):sha((BASE/f).read_bytes()) for f in ['provenance.json','next_source_targets.json','continuation_checkpoint.json']},
    'node_count':len(g), 'edge_count':sum(map(len,g.values())),
    'all_references_resolve':True, 'acyclic':len(topo)==len(g),
    'zero_dependency_nodes':sum(not v for v in g.values()),
    'weak_components':len(components),
    'largest_weak_component_sizes':sorted(map(len,components),reverse=True)[:20],
    'target_records':len(targets['targets']),
    'target_distinct_declarations':len({(t['path'],t['declaration']) for t in targets['targets']}),
    'target_distinct_files':len({t['path'] for t in targets['targets']}),
    'semantic_boundary_examples':samples,
    'completion_percentage':None,
    'completion_percentage_reason':'Neither number of claims, source links, acyclicity, nor unweighted graph reachability measures mathematical closure.'
})

anchors = [
 ('src/Main.lean','riemannHypothesis'),
 ('src/Supplements/Kernels/MainTheorems.lean','allChi'),
 ('src/Supplements/Kernels/MainTheorems.lean','claimAll'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean','UpperTheory.FinalTheorems.everyCharacter_of_row'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/Supply.lean','GChi'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/Supply.lean','cls'),
 ('src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ThinScalesIffHostBound.lean','HostExW'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean','TopG'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean','zeroFreeAll_of_topG'),
 ('src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean','Closed'),
 ('src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean','Closed.and'),
 ('src/Formalism/SharpRestriction/ParamsHeightRankConstant.lean','DesignExists'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean','topDesWin'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean','UpperTheory.Top.shapeWin'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean','HypV'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean','FamilyClassConnected'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean','vvRecord'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean','divinN_of_hypV'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkN'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkEta'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkIRR'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkDIVt'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkG'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkS'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','GlobalTheoremInputs'),
 ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean','LinkGLOBAL'),
 ('src/Formalism/SharpRestriction/AdmissibleParameterJoins/SumLogPrimeFactorsLe.lean','linkMu_of_linkDIV'),
 ('src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean','tiedWin_of_ex'),
 ('src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean','level_of_tiedWin'),
 ('src/Development/AutomorphicArithmetic/CharacterBoxes/WinPairs.lean','UpperTheory.Top.winPairs'),
 ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/LayeredIsomorphisms/ThmBabOfLemmaK.lean','thmBab_of_lemmaK'),
 ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/JointWinOfCounts.lean','pointHV_of_counts'),
 ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ThmBcOfPsiBound.lean','thmBcFree_of'),
 ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/OddResidueBounds/ZeroMemUnrHom.lean','PsiBound'),
 ('src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkNFam.lean','linkN_of_twGood_galoisPreconditions'),
 ('src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkNFam.lean','linkedAt_linkN_of_boundAtTwoThree'),
 ('src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/HeckeGaloisCriteria/LinkNOfGd.lean','linkN_of_gd'),
 ('src/Formalism/SharpRestriction/LevelLetterCocycles/ThetaScalarFamilyOfEigenvalue.lean','linkN_of'),
]
decl = re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure)\s+(\S+)')
source_records=[]
oldfiles={s['path']:s for s in prov['source_files']}
for path,name in anchors:
    data=(args.repo/path).read_bytes()
    pinned=subprocess.run(['git','-C',str(args.repo),'show',f'{PIN}:{path}'],check=True,capture_output=True).stdout
    assert data==pinned,('working file differs from pinned git blob',path)
    lines=data.splitlines(keepends=True)
    found=[]
    all_decls=[]
    for i,line in enumerate(lines):
        m=decl.match(line.decode())
        if m:
            spelling=m.group(1).rstrip(':')
            all_decls.append(i)
            if spelling==name:found.append(i)
    assert len(found)==1,(path,name,found)
    start=found[0]
    end=next((i for i in all_decls if i>start),len(lines))
    chunk=b''.join(lines[start:end])
    assert path not in oldfiles or oldfiles[path]['sha256']==sha(data),path
    source_records.append({
        'path':path,'declaration':name,'line_start':start+1,'line_end':end,
        'sha256':sha(data),'range_sha256':sha(chunk),
        'first_line':lines[start].decode().rstrip(),
        'matches_predecessor_file_hash':path in oldfiles,
        'verified_equal_to_pinned_git_blob':True,
        'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start+1}-L{end}'
    })
write('cut_interface_sources.json', {'commit':PIN,'range_convention':'one-based inclusive; through next declaration boundary','sources':source_records})

spec=read(HERE/'obligation_map_spec.json')
nodes={n['id']:n for n in spec['nodes']}
for n in nodes.values():
    for dep in n.get('requires',[]):assert dep in nodes,(n['id'],dep)
    for opt in n.get('alternatives',[]):
        for dep in opt:assert dep in nodes,(n['id'],dep)
active=set();done=set()
def visit(k):
    assert k not in active,('cycle',k)
    if k in done:return
    active.add(k)
    node=nodes[k]
    deps=node.get('requires',[])+[d for a in node.get('alternatives',[]) for d in a]
    for d in deps:visit(d)
    active.remove(k);done.add(k)
for k in nodes:visit(k)
spec['validation']={'references_resolve':True,'acyclic':True,'node_count':len(nodes),'not_lean_dependency_audit':True}
spec['source_manifest_sha256']=sha((HERE/'cut_interface_sources.json').read_bytes())
write('obligation_map.json',spec)

# Exact continuation records: two closure milestones, with constituent anchors.
target_specs = [
 ('DA-next-01-a','cohomological_suppliers','thmBab_of_lemmaK',
  'UpperTheory.V.Win.thmBab_of_lemmaK',
  'PoitouTateDuality, LocalFinitenessK, LocalTateDualityK, FerreroWashington and existence of CK satisfying the literal LemmaK; one K must work for every Ct>=1.'),
 ('DA-next-01-b','cohomological_suppliers','pointHV_of_counts',
  'UpperTheory.V.HV.pointHV_of_counts',
  'PoitouTateDuality, LocalFinitenessK, LocalTateDualityK, LemmaK CK, and CountI/II/III/V/Z on the original hosts and reference layers.'),
 ('DA-next-01-c','cohomological_suppliers','thmBcFree_of',
  'UpperTheory.V.Odd.thmBcFree_of',
  'The exact PsiBound. All non-PsiBound arithmetic ingredients used in the source body still need a readable proof or precise accepted theorem; this wrapper alone does not discharge them.'),
 ('DA-next-01-d','cohomological_suppliers','PsiBound',
  'UpperTheory.V.Odd.PsiBound',
  'The literal parity eigenspace length bound by the local valuation of the algebraic L-value, with the original field, coefficient ring, cyclotomic action and all indicated local primes.'),
 ('DA-next-02-a','actual_family_LinkN','linkN_of_twGood_galoisPreconditions',
  'UpperTheory.GalC.linkN_of_twGood_galoisPreconditions',
  'Hypotheses2, CutGivesAlt, TwGood Fm, and GaloisPreconditions with Tie4 at every actual late row. Reconstruct the arithmetic suppliers, not merely their predicate wrapper.'),
 ('DA-next-02-b','actual_family_LinkN','linkN_of_gd',
  'UpperTheory.GalC.linkN_of_gd',
  'Actual good cuts, original-row multiplicity and adm3/rank bounds, and LinkN on the cut family; prove the transport back to the original family with its additional cost.'),
 ('DA-next-02-c','actual_family_LinkN','linkedAt_linkN_of_boundAtTwoThree',
  'UpperTheory.GalC.linkedAt_linkN_of_boundAtTwoThree',
  'Uniform row Galois preconditions/Tie4 and uniform two/three-prime bound on the same linked bundle, retaining Hypotheses2, CutGivesAlt and RecTExists.'),
 ('DA-next-02-d','actual_family_LinkN','linkN_of',
  'Formalism.MainNotions.N.linkN_of',
  'Alternative same-family interface: actual AdmF and KudlaFamilyStatement. They are substantial premises, not automatically supplied by their names.')
]
target_rows=[]
for tid,group,name,qualified,premises in target_specs:
    matches=[s for s in source_records if s['declaration']==name]
    assert len(matches)==1,(name,matches)
    row=dict(matches[0])
    row.update(id=tid,work_package=group,qualified_declaration=qualified,
               status='human_supplier_unclosed',retained_inputs=premises,
               downstream=('VW4 -> VWinAt -> fixed-pair windows' if group=='cohomological_suppliers' else 'DA2: HypV + LinkN + actual rank -> DIVinN'))
    target_rows.append(row)
write('next_targets.json',{
    'artifact_version':'0.23','source_commit':PIN,
    'scope':'Exactly two recommended closure milestones; rows are the constituent interfaces, not eight independent expansion projects.',
    'work_packages':[
        {'id':'cohomological_suppliers','goal':'Supply one full cohomological route into the completed VW chain.','alternative':'A direct literal JointWin+ThmBc supplier also suffices; the listed structural route is not logically necessary.'},
        {'id':'actual_family_LinkN','goal':'Supply full LinkN on the actual original family, including cut-family transport and uniformity.','alternative':'The direct Galois-row route and AdmF/Kudla route are alternatives, with their full premises.'}],
    'targets':target_rows})

def source_select(names):
    return [s for s in source_records if s['declaration'] in names]
proof_bytes=(HERE/'main.tex').read_bytes()
proof_lines=proof_bytes.splitlines(keepends=True)
claim_specs=[
 ('DA1','Finite uniform joining on one family',[],
  ['Closed','Closed.and','DesignExists'],
  ['All finitely many Closed statements refer to the same class and exact dependent objects.','DesignExists for that class is an assumed supplier; it chooses one family after every threshold.','Threshold supremum has the stated Large conjunction property.']),
 ('DA2','The conditional common-family global-link chain',['DA1'],
  ['topDesWin','HypV','FamilyClassConnected','vvRecord','divinN_of_hypV','LinkN','LinkEta','LinkIRR','LinkDIVt','LinkG','LinkS','GlobalTheoremInputs','LinkGLOBAL','linkMu_of_linkDIV'],
  ['Literal common-class DesignExists, class inclusions and all nine closed link/rank statements.','The target class supplies HypV on the same host and actual NData.sha_eq identifies its lengths.','TuSize and DGamSize supply the stated MuTu and MuDGam consequences.','The actual NprimeMuR lattice/metric transport and positive retained ranks, not only matching dimensions.','The family windows and constants eD/eL precede epsilon as stated in the source.'])]
newclaims=[]
for cid,title,deps,names,premises in claim_specs:
    starts=[i for i,l in enumerate(proof_lines) if ('['+cid+':').encode() in l]
    assert len(starts)==1,cid
    start=starts[0]
    end=next(i for i in range(start,len(proof_lines)) if proof_lines[i].strip()==b'\\end{proof}')
    chunk=b''.join(proof_lines[start:end+1])
    newclaims.append({'id':cid,'title':title,
        'status':'Complete elementary conditional proof; the exact upstream supplier obligations are retained below.',
        'remaining_inputs':premises,'mathematical_dependencies':deps,
        'component_ledger':'dependency_audit_v0_23/provenance.json',
        'human_proof':{'path':'dependency_audit_v0_23/main.tex','line_start':start+1,'line_end':end+1,'range_sha256':sha(chunk)},
        'sources':source_select(names)})
unique={s['path']:s for c in newclaims for s in c['sources']}
source_files=[]
for path,s in sorted(unique.items()):
    data=(args.repo/path).read_bytes()
    source_files.append({'path':path,'sha256':sha(data),'bytes':len(data),'lines':len(data.splitlines()),
                         'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}',
                         'verified_equal_to_pinned_git_blob':True})
write('provenance.json',{
    'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.23','date':'2026-11-22',
    'repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,
    'scope':'Two complete conditional same-family/quantifier joins plus a semantic obligation audit; no formal Lean dependency extraction or unconditional endpoint claim.',
    'claims':newclaims,'source_files':source_files,
    'mathematical_dependency_graph':{c['id']:c['mathematical_dependencies'] for c in newclaims},
    'component_input_boundary':{'retained':['DesignExists','the nine exact Closed link/rank conditions','same-host HypV and actual NData.sha_eq','actual NprimeMuR lattice/metric transport','all target-class inclusion maps and windows'],
        'does_not_supply':['existence of the actual arithmetic family','cohomological suppliers','full LinkN','original theta, lattice, spectral and metric estimates']},
    'validation':{'main_tex_sha256':sha(proof_bytes),'source_links':sum(len(c['sources']) for c in newclaims),'source_files':len(source_files),'all_sources_equal_pinned_git_blobs':True,'full_lean_build':False,'kernel_replay':False}})

reviews=[]
for name in ['analytic_chain_closure_review.json','window_bridge_review.json',
             'dependency_join_core_review.json','coefficient_chain_analytic_review.json',
             'window_bridge_core_review.json']:
    p=ROOT/'reviews_v0_23'/name
    if p.exists():
        r=read(p)
        reviewed_file=r.get('reviewed_file') or r.get('reviewed_main_file')
        if not reviewed_file and r.get('component'):
            reviewed_file=r['component']+'/main.tex'
        reviews.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),
                        'reviewed_file':reviewed_file,
                        'reviewed_text_sha256':r.get('sha256') or r.get('reviewed_main_sha256'),
                        'result':r.get('result')})
write('integration_delta.json',{
    'baseline':'0.22','increment':'0.23','source_commit':PIN,
    'historical_records_mutated':False,
    'closed_actual_local_leaf':{'claims':['HP1','HP2','HP3','HP4'],'interface_claims':['HP5','HP6'],'description':'Canonical polynomial highest-weight, fixed-line and tensor irreducibility; actual geometric realization remains separate.'},
    'complete_conditional_chains':[
        {'claims':['VW1','VW2','VW3','VW4'],'retained':['JointWin+ThmBc OR ThmBab+PointHV+ThmBcFree','CN/BD/HD for fixed-pair supply']},
        {'claims':['WB1','WB2','WB3','WB4','WB5','WB6','WB7','WB8'],'retained':['Actual same-object arithmetic gap and host/character contract on arbitrarily late windows']},
        {'claims':['DA1','DA2'],'retained':['Actual common-family design, closed links, host HypV, rank and metric transport']}],
    'root_status':'Not yet a fully discharged human proof of RH/Dirichlet GRH.','reviews':reviews})
print(json.dumps({'baseline_nodes':len(g),'baseline_edges':sum(map(len,g.values())),'baseline_acyclic':len(topo)==len(g),'semantic_nodes':len(nodes),'source_anchors':len(source_records)},indent=2))
