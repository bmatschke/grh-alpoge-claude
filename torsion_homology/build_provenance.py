#!/usr/bin/env python3
"""Bind TB1--TB10 and the exact source interfaces at the preserved pin."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=HERE.parents[1]/'lean-source')
args = parser.parse_args()

def sha(b): return hashlib.sha256(b).hexdigest()
def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

cache = {}
def anchor(folder, file, spelling, role='exact source endpoint or definition'):
    path = BASE+folder+'/'+file+'.lean'
    raw = (args.repo/path).read_bytes()
    if path not in cache:
        assert raw == subprocess.check_output(['git','-C',str(args.repo),'show',PIN+':'+path]), path
        cache[path] = raw
    lines = raw.splitlines(keepends=True)
    starts=[]
    for i,b in enumerate(lines,1):
        m=re.match(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)', b.decode())
        if m: starts.append((i,m.group(1)))
    hits=[(i,n) for i,n in starts if n==spelling or n.endswith('.'+spelling)]
    assert len(hits)==1,(path,spelling,hits)
    a,name=hits[0]
    b=min([i for i,_ in starts if i>a] or [len(lines)+1])-1
    while b>a and not lines[b-1].strip(): b-=1
    frag=b''.join(lines[a-1:b])
    return {'path':path,'declaration':name,'source_spelling':spelling,
            'line_start':a,'line_end':b,'sha256':sha(raw),'range_sha256':sha(frag),
            'range_bytes':len(frag),'first_line':lines[a-1].decode().rstrip('\n'),
            'url':URL+path+f'#L{a}-L{b}','role':role,
            'verified_equal_to_pinned_git_blob':True}

def H(f,s,role='exact source endpoint or definition'): return anchor('HermiteNormalForms',f,s,role)
def C(f,s,role='exact source endpoint or definition'): return anchor('ConvexNerveComplexes',f,s,role)
def T(f,s,role='exact source endpoint or definition'): return anchor('TorsionBoundsChains',f,s,role)
def K(f,s,role='exact source endpoint or definition'): return anchor('GeneratorCountTuples',f,s,role)

spec=[
 ('TB1','Integral column and finite-group homology estimates',[],[],[
     T('Imports','base'),T('ImportsAlt','kill'),T('FaceDSingle','TorsLe')]),
 ('TB2','All-prime torsion from an exact permutation complex',['TB1'],[],[
     T('FaceDSingle','PermCx'),T('FaceDSingle','PermCx.ExactTo'),T('FaceDSingle','bound'),
     T('LogLeExp','mainFace','Alternative spectral-sequence proof of this exact bound'),
     T('FaceDSingle','faceD_single')]),
 ('TB3','The locally finite Hermitian polyhedron',[],['TB-NF'],[
     H('SmulStrictMono','Lat'),H('SmulStrictMono','HS'),H('SmulStrictMono','q'),
     H('SmulStrictMono','Ry'),H('SmulNeZeroLat','qc'),H('SmulNeZeroLat','Psd'),
     H('SmulNeZeroLat','Vx'),H('Rypos','rypos'),H('Locfin','locfin'),
     C('ExistsVert','exists_vert'),C('ConeFinite','cone_finite')]),
 ('TB4','Acyclic ordered nerve and common minimal basis',['TB3'],[],[
     H('SmulNeZeroLat','Sx'),H('SmulNeZeroLat','Sx.face'),
     H('SmulNeZeroLat','Sx.face_smul'),C('AcycSimp','acyc_simp'),
     C('NerveConvex','nerve_convex'),C('SimpSpan','simp_span'),
     T('TupExact','tupExact'),H('ColsMinSmul','sx_basis'),H('Assembly','sx_exact')]),
 ('TB5','Determinant and common-basis index bounds',['TB3'],['TB-NF'],[
     H('SmulStrictMono','I0'),H('SmulStrictMono','ColsMin'),H('SmulStrictMono','nrmDet'),
     H('Gramlow','gramlow'),H('Gramdet','gramdet'),H('Detlow','detlow'),H('DetPull','nrmle')]),
 ('TB6','A finite left-matrix quotient by counting row modules',[],['TB-NF'],[
     H('Hnf','hnf','Same endpoint proved by row-module residues, without the source normal-form construction')]),
 ('TB7','Near-vector and perfect-vertex counts',['TB3','TB5'],['TB-NF'],[
     H('SmulStrictMono','RR'),H('SmulStrictMono','nearVec'),H('SmulNeZeroLat','nearVx'),
     H('Nearcoord','nearcoord','Stronger inverse-Hermitian coordinate bound with the same source budget'),
     H('Nearvec','nearvec'),H('Nearvx','nearvx'),H('Cardsep','cardsep')]),
 ('TB8','Every tuple orbit and finite stabilizer budget',['TB3','TB4','TB5','TB6','TB7'],['TB-NF'],[
     H('SmulStrictMono','orbBound'),H('ColsMinSmul','colsMin_smul'),H('ColsMinSmul','orb'),
     H('Orbnum','orbnum'),H('Stabfin','stabfin'),H('Mink3','mink3'),
     H('Assembly','orbBound_mono')]),
 ('TB9','Literal TorsBound 49',['TB2','TB4','TB8'],[],[
     K('TorsBoundPow','HGL'),K('TorsBoundPow','torsHGL'),K('TorsBoundPow','tBound'),
     K('TorsBoundPow','TorsBound'),H('Assembly','tors_le'),H('Assembly','torsBound'),
     T('TorsBoundOf','torsBound_of')]),
 ('TB10','Explicit literal TorsBoundPow 22',['TB9'],[],[
     K('LemmaK','kBound'),K('TorsBoundPow','TorsBoundPow'),K('NumT','numT'),
     H('Assembly','torsBoundPow'),H('TorsMain','torsMain')])]

raw=(HERE/'main.tex').read_bytes(); lines=raw.splitlines(keepends=True)
claims=[]
for cid,title,deps,cinputs,sources in spec:
    starts=[i for i,b in enumerate(lines) if re.search(rb'\\begin\{(?:proposition|theorem)\}\['+cid.encode()+rb':',b)]
    assert len(starts)==1,cid
    a=starts[0]; b=next(i for i in range(a,len(lines)) if lines[i].strip()==b'\\end{proof}')
    frag=b''.join(lines[a:b+1])
    proof={'file':'torsion_homology/main.tex','line_start':a+1,'line_end':b+1,
           'sha256':sha(frag),'bytes':len(frag)}
    claims.append({'id':cid,'title':title,
      'status':'Complete human proof in the stated scope, with only the explicit elementary number-field lattice background.',
      'depends_on':deps,'mathematical_dependencies':deps,'classical_inputs':cinputs,
      'remaining_inputs':[],'remaining_bespoke_inputs':[],
      'component_ledger':'torsion_homology/provenance.json','proof_location':proof,'human_proof':proof,
      'sources':sources})
files=[{'path':path,'sha256':sha(b),'bytes':len(b),'lines':len(b.splitlines()),
        'url':URL+path,'verified_equal_to_pinned_git_blob':True} for path,b in sorted(cache.items())]
validation={'main_tex_sha256':sha(raw),'claim_count':len(claims),'source_files':len(files),
            'source_links':sum(len(c['sources']) for c in claims),
            'all_sources_equal_pinned_git_blobs':True,'all_source_and_proof_range_hashes_recorded':True,
            'full_lean_build':False,'kernel_replay':False,'pdf_generated':False}
classical={'schema':'rh-classical-input-registry/1','artifact_version':'0.25','component':'torsion_homology',
 'inputs':[{'id':'TB-NF','name':'Integral lattice and discriminant of a number field',
 'accepted_statement':'The ring of integers is free of rank [L:Q]; its Minkowski embedding is a full lattice of covolume 2^(-r_2) sqrt(|disc L|). Nonzero algebraic integers have nonzero integral norms.',
 'author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,
 'theorem_reference':'Proposition 4.26 and its integral-basis proof; elementary integral-basis and norm facts from Chapter 2.',
 'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','web_source_refs':['turn389156450view1'],
 'specialization':'L is the original totally complex field. The product lattice is O_L^N, degree d=nN, with no field or discriminant change.'}],
 'proved_here_instead_of_retained_as_inputs':['Minkowski convex-body argument used for positivity and the Gram determinant bound',
 'Finite closed-convex-cover homological nerve argument and ordered-tuple comparison',
 'Equivariant homology torsion bound with all stabilizer primes retained',
 'Finite matrix quotient by row-module residues',
 'Principal congruence kernel at 3 is torsion-free',
 'All orbit and near-vector constants and power absorption'],
 'standard_background':['Free resolutions and first-quadrant double-complex filtrations',
 'Smith normal form, saturation, Hadamard and Cauchy--Schwarz',
 'Singular subdivision and its prism homotopy'],
 'not_assumed':['Any source Good, Acyc, orb, stab, TorsBound or TorsBoundPow predicate',
 'A published torsion estimate only away from small primes',
 'A principal ideal domain structure on O_L']}
write('classical_inputs.json',classical)
ledger={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.25','date':'2026-11-22',
 'repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,
 'component':'torsion_homology','main_tex_sha256':sha(raw),
 'scope':'Complete literal arithmetic-group TorsBound(49) and explicit TorsBoundPow(22), including all primes and actual GL_N(O_L).',
 'claims':claims,'source_files':files,'mathematical_dependency_graph':{c['id']:c['depends_on'] for c in claims},
 'classical_input_registry':'torsion_homology/classical_inputs.json',
 'component_input_boundary':{'bespoke_inputs':[],'classical_inputs':['TB-NF'],
   'not_supplied':['KBridge and LemmaK comparisons, which have their own chapter',
     'ThmBab and PointHV','Actual common arithmetic family or analytic gap','RH or Dirichlet GRH']},
 'validation':validation}
write('provenance.json',ledger)
write('source_hashes.json',{'commit':PIN,'files':files})
write('closure.json',{'version':'0.25','component':'torsion_homology','commit':PIN,
 'main_tex_sha256':sha(raw),'claims':[c['id'] for c in claims],
 'outcome':'Literal TorsBound49 and TorsBoundPow22, with all-prime integral torsion and the source ordered perfect-form complex.',
 'claim_dependency_graph':{c['id']:c['depends_on'] for c in claims},
 'classical_inputs':['TB-NF'],'classical_input_registry':'torsion_homology/classical_inputs.json',
 'complete_chain_in_component':True,'additional_unreconstructed_bespoke_inputs':[],
 'closed_source_targets_in_stated_scope':[
  {'path':BASE+'GeneratorCountTuples/TorsBoundPow.lean','declaration':'TorsBound','supplier':'TB9','constant':49,'scope':'Full literal universal predicate'},
  {'path':BASE+'GeneratorCountTuples/TorsBoundPow.lean','declaration':'TorsBoundPow','supplier':'TB10','constant':22,'scope':'Full literal universal predicate'},
  {'path':BASE+'HermiteNormalForms/TorsMain.lean','declaration':'torsMain','supplier':'TB10','scope':'Existential constant supplied explicitly by 22'}],
 'retirement_candidate_ids':['DA24-K-04'],
 'quantifier_audit':['One constant before every totally complex L and every e>=1',
   'Original field degree and absolute discriminant',
   'Full integral torsion subgroup with no excluded primes',
   'N=4e+4 and degree 2e exactly as in HGL',
   'One actual ordered-vertex nerve with its original GL_N(O_L) action'],
 'full_RH_GRH_closed':False,'source_links':validation['source_links'],'source_files':len(files)})
(HERE/'report.txt').write_text('TB1--TB10: complete all-prime arithmetic-group torsion supplier.\n'
 'The written proof constructs the exact ordered perfect-form nerve, proves acyclicity, counts its orbits and stabilizers, and obtains TorsBound49 and TorsBoundPow22.\n'
 'The retained standard number-field input is recorded in classical_inputs.json; no bespoke torsion supplier remains.\n'
 f"Pinned source files: {len(files)}; exact declaration anchors: {validation['source_links']}.\n"
 'The source correspondence records alternative proofs where used. No fresh Lean build, kernel replay, PDF or full RH/GRH completion is claimed.\n')
print(json.dumps(validation,indent=2))
