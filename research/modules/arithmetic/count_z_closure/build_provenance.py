#!/usr/bin/env python3
"""Rebuild the CountZ proof/source ledger at the exact pinned source commit."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
BASE=REPO+'/blob/'+PIN+'/'
P='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
PATHS={
 'coeff':P+'GaloisLibrary/SelmerTransport/ConjStableShaFam.lean',
 'locsel':P+'GaloisLibrary/SelmerTransport/RestrictionMemInvariantH1.lean',
 'qo':P+'GaloisLibrary/SelmerTransport/QoFacts.lean',
 'places':P+'GaloisLibrary/SelmerTransport/Places.lean',
 'control':P+'GaloisLibrary/SelmerTransport/Control.lean',
 'kw':P+'GaloisLibrary/ClassFieldRamification/KwAbsRam.lean',
 'kwl':P+'LevelCohomology/KwlOnto.lean',
 'cyc':'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/CyclotomicCharInertiaSurjective.lean',
 'gauss':P+'GaloisLibrary/ClassFieldRamification/ExistsQuadraticGaussSum.lean',
 'pull':P+'GaloisLibrary/KummerTheory/PullOnto.lean',
 'quad':P+'LevelCohomology/ZqField.lean',
 'hquad':P+'LevelCohomology/HQuad.lean',
 'ideal':'src/Development/AbelianVarietyTheory/Proofs/CovolumeBounds/ExistsIdealInClassOfNormLeSqrtDiscr.lean',
 'tors':P+'LevelCohomology/TorsClass.lean',
 'prop':P+'LevelCohomology/PropZ.lean',
 'len':P+'CharacterLevelBounds/ShaFamMono.lean',
 'data':P+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean',
 'counts':P+'HeightAndVanishing/Counts.lean',
 'countz':P+'HeightAndVanishing/CountZ.lean',
 'stmt':P+'StmtFields.lean',
 'join':P+'HeightAndVanishing/JointWinOfCounts.lean',
}

def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main(repo):
 cache={}
 for k,path in PATHS.items():
  b=(repo/path).read_bytes()
  assert b==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
  cache[k]=b
 def anchor(k,decl,start=None,end=None,role='exact source interface or reconstructed supplier'):
  b=cache[k];lines=b.decode().splitlines()
  if start is None:
   pat=re.compile(r'^(?:private\s+)?(?:theorem|def|abbrev|structure)\s+'+re.escape(decl)+r'(?=[\s:(])')
   hits=[i+1 for i,s in enumerate(lines)if pat.match(s)]
   assert len(hits)==1,(k,decl,hits)
   start=hits[0]
  if end is None:
   end=len(lines)
   for i in range(start,len(lines)):
    if re.match(r'^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[',lines[i]):end=i;break
   while end>start and not lines[end-1].strip():end-=1
  frag=b''.join(b.splitlines(keepends=True)[start-1:end])
  return {'path':PATHS[k],'declaration':decl,'line_start':start,'line_end':end,'sha256':sha(b),'range_sha256':sha(frag),'range_bytes':len(frag),'first_line':lines[start-1],'url':BASE+PATHS[k]+f'#L{start}-L{end}','role':role,'verified_equal_to_pinned_git_blob':True}
 classical={'schema':'rh-classical-input-registry/1','artifact_version':'0.25','component':'count_z_closure','accessed':'2026-11-22','inputs':[
  {'id':'CZ-CFT','name':'Finite global ray class and Hilbert class field theory','author':'J. S. Milne','title':'Class Field Theory','version':'4.03','year':2020,'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf','theorem_reference':'V Theorems 3.5–3.6, Corollary 3.7, Examples 3.9–3.10','printed_pages':[158,159],'accepted_statement':'A finite abelian extension is a ray-class quotient for a modulus supported on its ramified places. The modulus-one ray class field is the ordinary Hilbert class field, with real places remaining real. The rational ray class field for l^r times infinity is Q(mu_(l^r)).','web_source_refs':['turn871647555view0','turn871647555view1','turn871647555view4'],'exact_specialization':'CZ2: finite image of an original G_Q -> M[l] homomorphism yields a finite abelian extension inside the same Omega; unramified outside l implies containment in a finite cyclotomic layer. CZ3: original G_K -> M[l], K constructed inside Omega, unramified at all finite places; the real-place order-two image vanishes because l is odd, so its image is a quotient of the ordinary class group.'},
  {'id':'CZ-BASIC','name':'Elementary number-field and local-field background','author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','theorem_reference':'Sections 2–3 and 6–7; Proposition 6.2 gives the finite cyclotomic ramification facts also derived in CZ2.','accepted_statement':'Integral basis/discriminant index formulas, unique ideal factorization and finite Galois inertia, Eisenstein total ramification and Hensel lifting to finite unramified extensions.','web_source_refs':['turn871647555view3','turn871647555view2'],'exact_specialization':'CZ2 derives the full finite cyclotomic inertia images and uses compact nested fibers for an actual infinite-level lift at each original valuation. CZ3 derives the Gauss identity, discriminant l, two-dimensional convex-body representative bound, ideal count, and h_K<l explicitly.'}
 ],'not_assumed':['PropZ or CountZ','The source full control or ShaToShT theorem','A Bernoulli-unit vanishing theorem','A pre-existing quadratic class-number estimate','Local-K duality or global Poitou–Tate','LemmaK, automorphy, host rigidity or any other count']}
 write('classical_inputs.json',classical)
 specs=[
  ('CZ1','Original coefficients, local Selmer conditions and l-torsion cocycles',[],[],[
   anchor('coeff','QO'),anchor('coeff','twist₂'),anchor('coeff','shaFam'),anchor('coeff','ShaU'),anchor('coeff','chiO'),
   anchor('locsel','LocSel'),anchor('locsel','mk_mem_locSel'),anchor('len','rho'),anchor('len','VS'),anchor('len','V'),
   anchor('qo','qo_inj'),anchor('qo','qo_tor'),anchor('qo','UpperTheory.V.Base.qoFacts'),anchor('tors','tors_class')]),
  ('CZ2','Exact cyclotomic inertia and rational Selmer injectivity',['CZ1'],['CZ-CFT','CZ-BASIC'],[
   anchor('cyc','exists_mem_Ine_toZModPow'),anchor('cyc','cycZ_Ine_surjective'),anchor('places','UpperTheory.V.Base.places'),
   anchor('kw','UpperTheory.V.CF.kwAbsRam'),anchor('kwl','UpperTheory.V.X.kwl'),anchor('tors','hom_kill'),
   anchor('control','UpperTheory.V.Base.control',role='stronger source theorem; only its injectivity over Q is needed, and CZ2 proves that directly')]),
  ('CZ3','Actual quadratic subfield, class-number bound and unramified vanishing',['CZ1','CZ2'],['CZ-CFT','CZ-BASIC'],[
   anchor('gauss','UpperTheory.V.CF.exists_quadratic_gauss_sum'),anchor('gauss','UpperTheory.V.CF.gauss'),
   anchor('quad','zq_root'),anchor('quad','zq_field'),anchor('quad','zq_hom'),anchor('hquad','UpperTheory.V.X.hQuad'),
   anchor('pull','UpperTheory.V.Kum.pullOnto'),anchor('ideal','exists_ideal_in_class_of_norm_le_sqrt_discr'),anchor('ideal','classNumber_le_sqrt_discr_mul_pow_pred')]),
  ('CZ4','Residual-trivial Selmer vanishing',['CZ1','CZ2'],[],[
   anchor('tors','pow_cong'),anchor('tors','UpperTheory.V.X.zOne'),anchor('len','V')]),
  ('CZ5','Residual-quadratic Selmer vanishing',['CZ1','CZ2','CZ3'],[],[
   anchor('quad','zq_four'),anchor('quad','zq_gen'),anchor('quad','zq_main'),anchor('quad','UpperTheory.V.X.zQuad')]),
  ('CZ6','Literal PropZ and CountZ with uniform exponent zero',['CZ1','CZ4','CZ5'],[],[
   anchor('counts','PropZ'),anchor('prop','UpperTheory.V.X.propZ'),anchor('counts','CountShape'),anchor('counts','CountZ'),
   anchor('countz','UpperTheory.V.HV.countZ'),anchor('data','Coef'),anchor('data','PsiEven'),anchor('data','mem_X'),
   anchor('data','CaseZ'),anchor('data','Vlen'),anchor('data','Vn'),anchor('data','VLe'),anchor('stmt','Bchi'),
   anchor('len','dirG'),anchor('len','V\''),anchor('len','V\'_le_V'),anchor('len','nrm'),
   anchor('join','pointHV_of_counts',role='downstream conditional consumer; not asserted proved by this component')])
 ]
 raw=(HERE/'main.tex').read_bytes();lines=raw.splitlines(keepends=True);claims=[]
 for cid,title,deps,cin,sources in specs:
  starts=[i for i,s in enumerate(lines)if re.search(rb'\\begin\{(?:proposition|theorem)\}\['+cid.encode()+b':',s)]
  assert len(starts)==1,cid
  a=starts[0];b=next(i for i in range(a,len(lines))if lines[i].strip()==b'\\end{proof}')
  frag=b''.join(lines[a:b+1]);loc={'file':'count_z_closure/main.tex','line_start':a+1,'line_end':b+1,'sha256':sha(frag),'bytes':len(frag)}
  claims.append({'id':cid,'title':title,'status':'Complete human proof in the stated scope, relative only to the explicitly matched finite classical inputs.','depends_on':deps,'mathematical_dependencies':deps,'classical_inputs':cin,'remaining_inputs':[],'remaining_bespoke_inputs':[],'component_ledger':'count_z_closure/provenance.json','proof_location':loc,'human_proof':loc,'sources':sources})
 files=[{'path':PATHS[k],'sha256':sha(b),'bytes':len(b),'lines':len(b.splitlines()),'url':BASE+PATHS[k],'verified_equal_to_pinned_git_blob':True}for k,b in cache.items()]
 validation={'main_tex_sha256':sha(raw),'claim_count':len(claims),'source_links':sum(len(c['sources'])for c in claims),'source_files':len(files),'all_sources_equal_pinned_git_blobs':True,'all_source_and_proof_range_hashes_recorded':True,'kernel_replay':False,'full_lean_build':False,'pdf_generated':False}
 boundary={'bespoke_inputs':[],'classical_inputs':['CZ-CFT','CZ-BASIC'],'not_supplied':['CountI','CountII','CountIII','CountV','The remaining PointHV sums/layer transport','Actual global arithmetic family or RH/Dirichlet GRH']}
 ledger={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.25','date':'2026-11-22','repository':REPO,'commit':PIN,'component':'count_z_closure','main_tex_sha256':sha(raw),'scope':'Complete actual PropZ and CountZ, uniformly C=0, with the original Omega, O, characters and host.','claims':claims,'source_files':sorted(files,key=lambda x:x['path']),'mathematical_dependency_graph':{c['id']:c['depends_on']for c in claims},'classical_input_registry':'count_z_closure/classical_inputs.json','component_input_boundary':boundary,'validation':validation}
 write('provenance.json',ledger);write('source_hashes.json',{'commit':PIN,'files':files});write('verification.json',validation)
 write('closure.json',{'artifact_version':'0.25','component':'count_z_closure','commit':PIN,'main_tex_sha256':sha(raw),'claims':[c['id']for c in claims],'closed_bespoke_interfaces':[
  {'interface':'UpperTheory.V.HV.PropZ','supplied_by':'CZ6','source':anchor('counts','PropZ'),'scope':'Full original universal quantifiers, l>=5, even e>=2 with l-1 dividing 2e, same Omega and c.O.'},
  {'interface':'UpperTheory.V.HV.CountZ','supplied_by':'CZ6','source':anchor('counts','CountZ'),'scope':'Literal CountShape CaseZ with C=0 chosen before every host, cutoff, field, coefficient, prime and twist.'}],
  'remaining_bespoke_inputs':[],'classical_inputs':['CZ-CFT','CZ-BASIC'],'safe_to_retire_in_stated_scope':['DA24-HV-05'],
  'partial_target_updates':{'DA-next-01-b':{'newly_supplied_inputs':{'CountZ':'CZ6'},'remaining_human_scope':'Retain actual CountI, CountII, CountIII, CountV and their common-window sums/layer descent. Local-K and LemmaK closures are supplied by separate components, not inferred from this chapter.'}},
  'exact_binding_notes':['Original QO tensor coefficients and negative cyclotomic rho','Original valuation groups; a finite-place subfamily already forces vanishing','Every l-torsion cohomology class represented by l-torsion values using divisibility','Same cyclotomic value lifted in inertia at each original l-place, with inverse-limit compatibility proved','Actual quadratic K constructed inside original Omega, Gauss sum evaluated','Local witness l m_A=0 follows from invertible alpha(t)-1 before restricting to G_K','Ordinary rather than narrow class group justified by odd l at real places','CountZ C=0 precedes all universal host/window objects'],
  'does_not_close':boundary['not_supplied']})
 print(json.dumps(validation,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=HERE.parent.parent/'lean-source');main(p.parse_args().repo.resolve())
