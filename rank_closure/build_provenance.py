"""Rebuild the RK source ledger from byte-identical pinned Lean source files."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
SD = GB + 'SegmentDegree/'
PATHS = {
 'statement':GB+'ValuationLowestDegreeRename.lean',
 'data':SD+'NonemptyDvrSettingOfStandard.lean',
 'count':SD+'RestCountOf.lean',
 'coarse':SD+'Coarse.lean',
 'main':GB+'SegmentDegree.lean',
 'select':SD+'SelIsComplRestrictSupport.lean',
}

PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^' + PREFIX + r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND = re.compile(r'^' + PREFIX + r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute)\b')
files = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    expected = subprocess.check_output(['git', '-C', str(REPO), 'show', f'{PIN}:{path}'])
    assert raw == expected, ('uncommitted source bytes', path)
    lines = raw.splitlines(keepends=True)
    stack = []
    decls = []
    for i, bline in enumerate(lines):
        line = bline.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)', line):
            stack.append(('namespace', m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line):
            stack.append(('section', m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$', line):
            assert stack, (path, i + 1, 'end without namespace/section')
            kind, label = stack.pop()
            assert not m[1] or m[1] == label, (path, i + 1, label, m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind, label in stack if kind == 'namespace')
            decls.append((m[1], i, ns + '.' + m[1] if ns else m[1]))
    files[key] = {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                  'lines': len(lines), '_lines': lines, '_decls': decls,
                  'verified_equal_to_pinned_git_blob': True}


def refs(key, names, role='parallel_source_proof'):
    item = files[key]
    output = []
    for name in names.split():
        hits = [d for d in item['_decls'] if d[0] == name]
        assert len(hits) == 1, (key, name, hits)
        _, start, qualified = hits[0]
        end = start + 1
        while end < item['lines'] and not BOUND.match(item['_lines'][end].decode()):
            end += 1
        while end > start + 1 and not item['_lines'][end - 1].strip():
            end -= 1
        raw = b''.join(item['_lines'][start:end])
        output.append({'path': item['path'], 'declaration': qualified, 'source_spelling': name,
                       'line_start': start + 1, 'line_end': end,
                       'full_file_sha256': item['sha256'], 'range_sha256': hashlib.sha256(raw).hexdigest(),
                       'role': role, 'url': f'{URL}/blob/{PIN}/{item["path"]}#L{start+1}-L{end}'})
    return output


claims=[
 {'id':'RK1','title':'Complete coarse residue-rank count',
  'status':'proved_by_complete_human_component_assembly',
  'statement':'Under the exact supplied-data Hyp and CLa,Ck>=1088, the actual segment functions of GP, degree padding and sum of RS, and injection of LA prove RestCount 1088 1.',
  'depends_on':['GP12','RS4','RS8','LA6'],
  'sources':refs('count','SegOK RestLam RestSeg RestPad RestSum restCount_of')+refs('coarse','RestCount')},
 {'id':'RK2','title':'Complete rank transfer from coarse to actual symbols',
  'status':'proved_by_complete_human_component_assembly',
  'statement':'CG8 supplies an individual actual generator congruent to Delta*u for every coarse generator. SD3 makes multiplication by reduced Delta injective. Thus the full q^(-rK)(1-Nr^2k/Y) product binomial lower bound holds for the actual residue-generator span.',
  'depends_on':['RK1','CG8','SD3'],
  'sources':refs('coarse','lamGen LamBar GeneratorModuloUniformiser restRank_of')+refs('data','NNbar RestRank degSet_finite')},
 {'id':'RK3','title':'All clauses of the selected-symbol Conclusion2 with constants 1088,1,10',
  'status':'proved_human_local_theorem_for_supplied_data',
  'statement':'In the exact Conclusion2 setting with CLa,Ck>=1088, an ambient direct summand inside the actual generator span has a basis of actual generators and the stated rank. Graph planes give the nPl-normalized bound for every finite field of cardinality q. SD4 proves the whole-span normal-degree bound with constant 10. Thus C0=1088,Crk=1,Cdeg=10 are human-proved local witnesses; full Type-II data supply and separate Type I remain.',
  'depends_on':['RK2','SD1','SD4'],
  'sources':refs('statement','Conclusion2 SecondPartClosed')+refs('data','RestSel RestDeg nonempty_dvr_setting_of_standard second_estimate_of_rank_bound')+refs('select','restSel')+refs('main','second_estimate_of_restrictions secondPartClosed')}
]
for c in claims:
 c['assumptions']=['Literal Conclusion2 / Dat.Hyp supplied frame, degree, DVR and numerical hypotheses; CLa,Ck>=1088.']
 c['remaining_inputs']=[]
 c['separate_remaining_work']=['Full global/local parameter compatibility and frame existence','Separate r=1 Type-I construction','Global spectral/theta, arithmetic/cohomological windows and prime-selection inputs']
 c['proof_location']={'file':'rank_closure/rank_closure_section.tex','expanded':'rank_closure/report.txt','section':c['id']}
ledger={'component':'rank_closure','artifact_version':'0.7','repository':URL,'commit':PIN,'claims':claims,
 'source_files':[{k:v for k,v in files[key].items() if not k.startswith('_')} for key in PATHS],
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,'all_files_equal_pinned_git_blobs':True}}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(claims),'sources':sum(len(c['sources']) for c in claims),'files':len(files)}))
