#!/usr/bin/env python3
"""Index the readable finite PsiBound supplier against pinned Lean source.

This verifies source/proof hashes and the declared human dependency graph.
It does not elaborate Lean or infer mathematical completeness from hashes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
PREFIX = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()

def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def pf(file, declaration):
    return ('PrimitiveFrobeniusFixed/'+file+'.lean', declaration)
def src(file, declaration): return (file+'.lean', declaration)

spec = [
 ('OS1', 'Existence, norm, and congruence of Jacobi elements', [],
  ['OS-CYC','OS-CHEB','OS-HCF'],
  [pf('IsAdmissiblePrimeListNil','th'),pf('IsAdmissiblePrimeListNil','IsX'),
   pf('XJacPowNe','UpperTheory.V.ML.xJac'),pf('XEx','UpperTheory.V.ML.xEx'),
   pf('XUniqConj','UpperTheory.V.ML.xUniq'),pf('XMulConjIMul','UpperTheory.V.ML.xMul'),
   pf('ThDist','UpperTheory.V.ML.thDist'),pf('XNormDiv','UpperTheory.V.ML.xNormDiv'),
   pf('XCongJac','UpperTheory.V.ML.xCongJac'),pf('XCongPrin','UpperTheory.V.ML.xCongPrin'),
   pf('AlgStep','UpperTheory.V.ML.xCong'),
   src('GaloisLibrary/StickelbergerTheorem/FfsumPow','UpperTheory.V.Stick.ffsum'),
   src('GaloisLibrary/StickelbergerTheorem/JacDvd','UpperTheory.V.Stick.jacDvd'),
   src('GaloisLibrary/StickelbergerTheorem/DegOne','UpperTheory.V.Stick.degOne')]),
 ('OS2', 'A strict finite Euler system', ['OS1'], ['OS-CYC'],
  [pf('PlaceEmb','UpperTheory.V.ML.laxEx'),pf('SysOfLax','UpperTheory.V.ML.sysOfLax'),
   pf('IsAdmissiblePrimeListNil','Lax'),pf('IsAdmissiblePrimeListNil','Sys'),
   pf('IsAdmissiblePrimeListNil','HasOrd')]),
 ('OS3', 'Auxiliary homomorphisms with local recurrence and initialization',
  ['OS2'], ['OS-CYC'],
  [pf('DerInv','UpperTheory.V.ML.derInv'),pf('KolEx','UpperTheory.V.ML.kolEx'),
   pf('KolHom','UpperTheory.V.ML.kolHom'),pf('KolUnr','UpperTheory.V.ML.kolUnr'),
   pf('ValAddSmul','UpperTheory.V.ML.nuIs'),pf('KolStep','UpperTheory.V.ML.kolStep'),
   pf('KolInit','UpperTheory.V.ML.kolInit'),pf('NuSysEx','UpperTheory.V.ML.nuSysEx'),
   pf('IsAdmissiblePrimeListNil','IsKol'),pf('IsAdmissiblePrimeListNil','nu'),
   pf('IsAdmissiblePrimeListNil','IsNu'),pf('IsAdmissiblePrimeListNil','NuSys')]),
 ('OS4', 'Simultaneous compatible auxiliary prime selection', [],
  ['OS-CYC','OS-CHEB'],
  [pf('AddPowNsmul','three_sub'),pf('AddPowNsmul','third'),
   pf('AddPowNsmul','adm'),pf('AddPowNsmul','UpperTheory.V.ML.pick'),
   pf('RadEqv','UpperTheory.V.ML.radEqv'),pf('ChebQ','UpperTheory.V.ML.chebQ')]),
 ('OS5', 'Finite reciprocity and the annihilator comparison',
  ['LD2','LD4'], ['OS-CYC'],
  [pf('IsAdmissiblePrimeListNil','Rec'),pf('OverIff','glob'),
   pf('OverIff','locq'),pf('OverIff','core'),pf('OverIff','UpperTheory.V.ML.recip'),
   pf('ImportsAlt','UpperTheory.V.ML.ext'),pf('ChiDvd','UpperTheory.V.ML.step')]),
 ('OS6', 'Complete finite length descent without a finiteness assumption',
  ['OS3','OS4','OS5'], ['OS-CHEB'],
  [pf('FrobFix','Sn'),pf('FrobFix','key'),pf('FrobFix','UpperTheory.V.ML.count'),
   pf('IsAdmissiblePrimeListNil','ShT'),pf('QocEquiv','UpperTheory.V.ML.qoCyc')]),
 ('OS7', 'Finite theta evaluation with exact Bernoulli normalization', [],
  ['OS-CYC'],
  [pf('GenBUnits','pointwise'),pf('GenBUnits','UpperTheory.V.ML.zCong'),
   pf('ZeNorm','ze_gen'),pf('ZeNorm','UpperTheory.V.ML.zEval'),
   src('GaloisLibrary/BernoulliNumbers/MapGenBChar','bcoef'),
   src('GaloisLibrary/BernoulliNumbers/MapGenBChar','genB'),
   src('GaloisLibrary/BernoulliNumbers/MapGenBChar','Bprim'),
   src('GaloisLibrary/BernoulliNumbers/MapGenBChar','den')]),
 ('OS8', 'Normalized Selmer exhaustion and the residual cyclotomic exception',
  [], ['OS-CYC','OS-KUM'],
  [pf('ShaToShT','norm_coc'),pf('ShaToShT','mem_shT'),
   pf('ShaToShT','UpperTheory.V.ML.shaToShT'),pf('PrimRam','UpperTheory.V.ML.primRam'),
   pf('RatPlace','UpperTheory.V.ML.exc'),
   src('GaloisLibrary/KummerTheory/LenDirected','UpperTheory.V.Kum.lenDirected')]),
 ('OS9', 'The literal PsiBound on the original field and eigenspace',
  ['OS6','OS7','OS8'], [],
  [pf('PrimCase','prim_case'),pf('PrimCase','lev_case'),pf('PrimCase','UpperTheory.V.ML.vChar'),
   pf('PsiOf','UpperTheory.V.ML.psiOf'),pf('Iv','UpperTheory.V.ML.iv'),
   src('CharacterLevelBounds/EigV','UpperTheory.V.Chr.eigV'),
   src('GaloisLibrary/SelmerTransport/SelEigBase','UpperTheory.V.Base.selEigBase'),
   src('GaloisLibrary/SelmerTransport/GalQuot','UpperTheory.V.Base.galQuot'),
   src('GaloisLibrary/SelmerTransport/GalEmbTop','UpperTheory.V.Base.galEmbTop'),
   src('GaloisLibrary/SelmerTransport/DvrFacts','UpperTheory.V.Base.dvrFacts'),
   src('OddResidueBounds/ZeroMemUnrHom','IsCycAct'),
   src('OddResidueBounds/ZeroMemUnrHom','alN'),
   src('OddResidueBounds/ZeroMemUnrHom','psiLen'),
   src('OddResidueBounds/ZeroMemUnrHom','PsiBound')]),
]

classical = [
 {'id':'OS-CYC','title':'Finite cyclotomic, valuation, and local unit-root facts',
  'statement':'Galois group and integral basis of Q(zeta_n), cyclotomic inertia and arithmetic Frobenius, tame inertia on roots of a uniformizer, and Hensel lifting of prime-to-residue-characteristic roots of units.',
  'reference':'Milne, Algebraic Number Theory v3.08, §§6–7; standard finite cyclotomic theory.',
  'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf'},
 {'id':'OS-CHEB','title':'Finite Chebotarev density',
  'statement':'Every conjugacy class in a finite Galois extension of number fields has positive Dirichlet density; any fixed finite set of primes may be excluded.',
  'reference':'Milne, Algebraic Number Theory v3.08, Theorem8.31.',
  'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf'},
 {'id':'OS-HCF','title':'Hilbert class field and Artin isomorphism',
  'statement':'The Hilbert class field has Galois group the ideal class group under the Artin map; together with Chebotarev this gives degree-one primes in prescribed ideal classes outside finite exclusions.',
  'reference':'Milne, Class Field Theory v4.03, V Theorem3.6, Corollary3.7, Example3.9.',
  'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf'},
 {'id':'OS-KUM','title':'Kummer exact sequence and Hilbert90',
  'statement':'H1(Q,mu_p)=Q^times/Q^{times p}, compatibly with local restriction, from the Kummer sequence and H1(Gal(L/K),L^times)=0.',
  'reference':'Milne, Class Field Theory v4.03, II Proposition1.22, together with the Kummer exact sequence.',
  'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf'},
]

decl = re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure)\s+(\S+)')
file_data = {}
anchors = {}
for _,_,_,_,links in spec:
    for rel, name in links:
        path = PREFIX+rel
        if path not in file_data:
            data=(args.repo/path).read_bytes()
            pinned=subprocess.run(['git','-C',str(args.repo),'show',f'{PIN}:{path}'],capture_output=True,check=True).stdout
            assert data==pinned, ('unpinned working file',path)
            file_data[path]=data
        data=file_data[path]
        lines=data.splitlines(keepends=True)
        declarations=[]
        for i,line in enumerate(lines):
            m=decl.match(line.decode())
            if m: declarations.append((i,m.group(1).rstrip(':')))
        matches=[i for i,n in declarations if n==name]
        assert len(matches)==1,(path,name,matches)
        start=matches[0]
        end=next((i for i,_ in declarations if i>start),len(lines))
        anchors[(path,name)]={
          'path':path,'declaration':name,'line_start':start+1,'line_end':end,
          'sha256':sha(data),'range_sha256':sha(b''.join(lines[start:end])),
          'first_line':lines[start].decode().rstrip(),
          'verified_equal_to_pinned_git_blob':True,
          'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start+1}-L{end}'
        }

tex=(HERE/'main.tex').read_bytes()
lines=tex.splitlines(keepends=True)
claims=[]
for cid,title,deps,leaf_ids,links in spec:
    start=next(i for i,line in enumerate(lines) if line.decode().strip()=='% BEGIN '+cid)
    end=next(i for i,line in enumerate(lines) if line.decode().strip()=='% END '+cid)
    claims.append({
      'id':cid,'title':title,
      'status':'Readable proof complete relative to the explicitly stated classical inputs and recorded human dependencies.',
      'mathematical_dependencies':deps,'classical_inputs':leaf_ids,
      'remaining_inputs':[],'component_ledger':'odd_minus_supplier/provenance.json',
      'human_proof':{'path':'odd_minus_supplier/main.tex','line_start':start+2,'line_end':end,
                     'range_sha256':sha(b''.join(lines[start+1:end]))},
      'sources':[anchors[(PREFIX+rel,name)] for rel,name in links]
    })
graph={c['id']:c['mathematical_dependencies'] for c in claims}
external={'LD2','LD4'}
visiting=set(); done=set()
def visit(cid):
    assert cid not in visiting,('cycle',cid)
    if cid in done or cid in external:return
    assert cid in graph,('unresolved dependency',cid)
    visiting.add(cid)
    for d in graph[cid]:visit(d)
    visiting.remove(cid);done.add(cid)
for cid in graph:visit(cid)

source_files=[{'path':p,'sha256':sha(d),'bytes':len(d),'lines':len(d.splitlines()),
               'verified_equal_to_pinned_git_blob':True} for p,d in sorted(file_data.items())]
write('provenance.json',{
 'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.24',
 'date':'2026-11-22','repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
 'commit':PIN,'main_tex_sha256':sha(tex),
 'scope':'Complete finite arithmetic supplier of literal PsiBound relative to named classical theorem leaves and LD2/LD4. No formal Lean proof-term dependency audit or full RH/GRH completion claim.',
 'claims':claims,'mathematical_dependency_graph':graph,'external_human_dependencies':sorted(external),
 'classical_inputs':classical,'source_files':source_files,
 'source_link_count':sum(len(c['sources'])for c in claims),
 'source_file_count':len(source_files),
 'validation':{'declared_graph_acyclic':True,'declared_dependencies_resolve':True,
               'all_indexed_sources_match_pinned_git':True,
               'human_proof_markers_and_ranges_verified':True,
               'lean_build_performed':False,'formal_dependency_audit_performed':False},
 'simplifications':[
   'An arbitrary fixed Bernoulli denominator-clearing integer replaces the source explicit Stk.dk in the asymptotic congruence; the final literal den(N,k) is retained.',
   'The zero algebraic-value case is handled by v(0)=infinity, so the supplier does not need analytic Bernoulli nonvanishing.',
   'Residual cyclotomic vanishing is proved by the finite Kummer group of Q and local valuation conditions.',
   'Complex conjugation itself normalizes cocycles and establishes the required oddness, sufficient for the final source interface.',
   'The finite subgroup-avoidance and length-induction arguments are written directly, retaining all simultaneous prime conditions.'
 ]
})
write('source_hashes.json',{'commit':PIN,'files':source_files})
write('closure.json',{
 'artifact_version':'0.24','component':'odd_minus_supplier','endpoint':'OS9',
 'endpoint_source':anchors[(PREFIX+'OddResidueBounds/ZeroMemUnrHom.lean','PsiBound')],
 'human_chain':graph,'external_human_dependencies':sorted(external),
 'classical_inputs':[x['id']for x in classical],
 'bespoke_retained_input_interfaces':[],
 'closed_interface':'UpperTheory.V.Odd.PsiBound',
 'consumers':[
   {'component':'odd_minus_bounds','claim':'OB3','supplier':'OS9','join':'literal universal PsiBound'},
   {'component':'odd_minus_bounds','claim':'OB5','supplier':'OS1','join':'explicit theta Jacobi principal-ideal annihilation, removing the separate Stickelberger citation leaf'}
 ],
 'same_object_preservation':['Original E and Omega','Original scalar towers and IsCycAct reading rho','Original coefficient DVR O','Original psi and exact negative cyclotomic twist','All local groups and original place choices'],
 'does_not_close':['ThmBab / two-primary supplier','PointHV / odd-plus supplier','Actual common-family LinkN and geometric suppliers','Full RH or GRH'],
 'retire_frontier':[{'declaration':'UpperTheory.V.Odd.PsiBound','replacement':'OS9 relative to the stated classical theorem leaves and LD2/LD4'}],
 'completion_percentage':None,
 'completion_percentage_reason':'This milestone is a closed dependency chain; counts of declarations and links are indexing data, not proof-completion measures.'
})
write('verification.json',{
 'component':'odd_minus_supplier','commit':PIN,'main_tex_sha256':sha(tex),
 'claims':len(claims),'source_links':sum(len(c['sources'])for c in claims),
 'pinned_source_files':len(source_files),'graph_checks_pass':True,
 'source_blob_checks_pass':True,'proof_range_checks_pass':True,
 'lean_build_performed':False,'mathematical_review':'Recorded separately against the frozen main.tex hash.'
})
print(json.dumps({'main_tex_sha256':sha(tex),'claims':len(claims),
 'source_links':sum(len(c['sources'])for c in claims),'source_files':len(source_files)},indent=2))
