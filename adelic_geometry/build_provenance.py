#!/usr/bin/env python3
"""Rebuild exact AD locators from the pinned Git objects (read-only)."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=ROOT.parents[1] / 'lean-source')
args = parser.parse_args()
REPO = args.repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
TF = 'src/Formalism/LocalToGlobal/GroupLattices/TiedFamilies/'
CM = 'src/Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/'
BR = 'src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/RationalRealBlocks/'
AM = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
cache = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def source(path, name, declaration=None, role='proof'):
    if path not in cache:
        raw = subprocess.check_output(['git', '-C', str(REPO), 'show', COMMIT + ':' + path])
        if (REPO / path).is_file():
            assert (REPO / path).read_bytes() == raw, path
        cache[path] = raw
    raw = cache[path]
    lines = raw.splitlines(keepends=True)
    text = [line.decode().rstrip('\r\n') for line in lines]
    pattern = re.compile(r'^(?:private )?(?:noncomputable )?(?:theorem|lemma|def|structure|abbrev) ' + re.escape(name) + r'(?:\s|\{|\(|:)')
    hits = [i for i, line in enumerate(text) if pattern.search(line)]
    assert len(hits) == 1, (path, name, hits)
    start = hits[0]
    stop = start + 1
    while stop < len(lines) and not re.match(r'^(?:(?:private |noncomputable )?(?:theorem|lemma|def|structure|abbrev)|variable|namespace|section|end|open|attribute)\b|^@\[', text[stop]):
        stop += 1
    while stop > start + 1 and (not text[stop - 1].strip() or text[stop - 1].startswith('set_option ')):
        stop -= 1
    return {
        'path': path, 'declaration': declaration or name,
        'line_start': start + 1, 'line_end': stop,
        'sha256': sha(raw), 'range_sha256': sha(b''.join(lines[start:stop])),
        'url': f'{URL}/blob/{COMMIT}/{path}#L{start+1}-L{stop}',
        'first_line': text[start], 'declaration_lines_within_range': [start + 1],
        'role': role, 'verified_equal_to_pinned_git_blob': True,
    }

IP='src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
AM='src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
def ip(file,name,ns,role='proof'):
    return source(IP+file+'.lean',name,'GlobalTheory.Mem.Col2.'+ns+'.'+name,role)
def pt(name,role='proof'):
    return ip('ValuedLtOfMem',name,'PtExist',role)
def sp(name,role='proof'):
    return ip('ValuedInvMulLe',name,'Splice',role)
specs=[
('AD1','Explicit unitary diagonal base point with the exact last-row residue',
 'Finite adelic idempotents give an integral unit a with inverse conjugate(a), prescribed inverse component conjugate(pi) at every prime dividing pi and identity away from pi*conjugate(pi). The diagonal matrix constructs literal exists_base, exists_kStd and kStd_spec, including rank zero.',
 ['LP1'], [pt('ad_ext'),pt('idem','definition'),pt('adAt_idem'),pt('adAt_sig_idem'),pt('glue','definition'),pt('sig_glue'),pt('adAt_glue'),
 ip('ExistsUnitaryDiagonalBasePointLevelPrime','exists_unit','BasePoint'),ip('ExistsUnitaryDiagonalBasePointLevelPrime','stdPt','BasePoint','definition'),
 ip('ExistsUnitaryDiagonalBasePointLevelPrime','exists_base','BasePoint'),ip('ExistsUnitaryDiagonalBasePointLevelPrime','exists_kStd','BasePoint'),
 ip('ExistsMemberStepCharts','kStd_spec','MemChart')]),
('AD2','Local lattice transitions are integral and residue identities cancel local units',
 'A localized inclusion of two carried lattices gives integrality of a^(-1)b; equality gives integrality of its inverse. Explicit local-unit cancellation proves HasRes on a localization after clearing denominators.',
 ['LP1'],[sp('hasRes_of_mul'),sp('adAt_pullV_osmul'),sp('adAt_pullV_congr'),sp('valued_inv_mul_le'),
 source(AM+'ReferenceCharactersFactorTame.lean','pullV','GlobalTheory.Mem.Col2.pullV','definition'),
 source(AM+'ReferenceCharactersFactorTame.lean','IsPtOf','GlobalTheory.Mem.Col2.IsPtOf','definition')]),
('AD3','Supported conjugate-pair splice preserves all five decorated-point conditions',
 'From supplied realizers h,h0 and the exact neighbor local-lattice/decorative equalities, g=(1-e)h+e*h0 with e=e_P+e_barP realizes the new point. The unitary epsilon=h^(-1)g is identity outside the conjugate pair. All five IsPtOf fields are checked; initial realization remains a premise.',
 ['AD2'],[sp('mat_ext'),sp('splice','definition'),sp('map_splice'),sp('exists_splice'),pt('mem_uad_iff'),pt('inv_apply'),pt('exists_isPtOf_cm','retained_supplier')]),
('AD4','Install exact rational frames without changing the carried lattice',
 'Prescribe M_P at finitely many oriented primes and conjugate(M_P)^(-transpose) at their conjugates. Unitarity and two-direction local integrality show the same lattice is carried; all pullbacks away from that finite set remain exact. This proves exists_modify and isolates the initial genus/reduction supplier.',
 ['AD2', 'LP2', 'LP3'],[pt('int_of_uni'),pt('mat','definition'),pt('mat_mulVec'),pt('mat_symm_mul'),pt('valued_pullV_le'),pt('valued_symm_le'),pt('carries_globLat'),pt('mulVec_int'),pt('exists_modify'),pt('exists_isPtOf_cm','remaining_join'),pt('unimodGenus','retained_supplier')])]
claims=[]
for i,title,statement,deps,sources in specs:
 claims.append({'id':i,'title':title,'statement':statement,'status':'derived_simplification','mathematical_status':'proved_under_explicit_hypotheses','depends_on':deps,
 'proof_location':{'file':'adelic_geometry/main.tex','expanded':'adelic_geometry/report.txt','section':i},
 'assumptions':['The original CM field, involution, localizations and finite adelic algebra are supplied.','AD3 assumes actual realizers and local neighbor identities; AD4 assumes an initial unitary realizer and compatible rational local bases.','General self-dual-lattice genus and decorated-point realization are not inferred from these constructions.'],
 'sources':sources})
targets=[pt('exists_isPtOf_cm','remaining_supplier'),pt('unimodGenus','remaining_supplier')]
for t in targets:
 t['remaining_human_scope']=('AD4 proves exact frame modification; reconstruct the initial unitary realization of the self-dual lattice and finite type/auxiliary reductions via the unramified Hermitian genus and reduction-surjectivity arguments.' if t['declaration'].endswith('exists_isPtOf_cm')else 'Prove the actual unramified self-dual-lattice genus and adelic class realization invoked here; this theorem uses CMData.cmUnram.')
 t['priority_group']=1
files=[{'path':p,'sha256':sha(raw),'bytes':len(raw),'lines':len(raw.splitlines()),'url':f'{URL}/blob/{COMMIT}/{p}','verified_equal_to_pinned_git_blob':True}for p,raw in sorted(cache.items())]
d={'schema':'rh-component-provenance-v1','artifact_version':'0.14','repository':URL,'commit':COMMIT,'claims':claims,'source_files':files,
 'input_boundaries':['AD1 fully supplies kStd and its prescribed residue.','AD3 supplies supported modification from realizers; actual up/down neighbor local identities and initial realizing points remain separate.','AD4 completely supplies exact rational frame modification; self-dual genus and finite reduction realization remain arithmetic inputs.'],
 'artifact_hashes':{n:sha((ROOT/n).read_bytes())for n in ['main.tex','report.txt']},
 'validation':{'claim_count':len(claims),'source_file_count':len(files),'source_links':sum(len(c['sources'])for c in claims),'pinned_bytes_verified':True,'lean_build':False,'kernel_replay':False}}
(ROOT/'provenance.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(f"{c['id']} {s['declaration']}\n{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}"for c in claims for s in c['sources'])+'\n')
(ROOT/'next_targets.json').write_text(json.dumps({'version':'0.14','commit':COMMIT,'targets':targets},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(d['validation']))
