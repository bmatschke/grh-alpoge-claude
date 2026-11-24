#!/usr/bin/env python3
"""Bind LD's classical specializations and elementary proofs to exact bytes."""
from pathlib import Path
import hashlib,json,re,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
def digest(b):return hashlib.sha256(b).hexdigest()
def write(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
paths={
 'defs':'src/ReciprocityTheory/Hypotheses/GalCohDefs.lean',
 'hyp':'src/ReciprocityTheory/Hypotheses/GalCoh.lean',
 'global':'src/ReciprocityTheory/GaloisValuations/Global.lean',
 'uo':'src/Development/AutomorphicSpectrum/Proofs/GlobalProofs/ContinuousCompOfIsOpenKer.lean',
 'uofinal':'src/Development/AutomorphicSpectrum/Proofs/GlobalProofs/UnramifiedOrthogonality.lean',
 'ptdefs':'src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/PoitouTateNineTermTransgressionZeroApply.lean',
 'pt':'src/Development/AbelianVarietyTheory/PublishedTheorems/GaloisCohomology₂/ExistsPrimitiveRootPow.lean',
 'rec':'src/Development/AutomorphicArithmetic/AutomorphicVarieties/PrimitiveFrobeniusFixed/OverIff.lean',
 'iv':'src/Development/AutomorphicArithmetic/AutomorphicVarieties/PrimitiveFrobeniusFixed/Iv.lean',
}
cache={};files=[]
for key,path in paths.items():
 b=(REPO/path).read_bytes()
 assert b==subprocess.run(['git','-C',str(REPO),'show',PIN+':'+path],capture_output=True,check=True).stdout
 cache[key]=b
 files.append({'path':path,'sha256':digest(b),'bytes':len(b),'lines':len(b.splitlines()),'url':URL+path,'verified_equal_to_pinned_git_blob':True})
def anchor(key,decl,a,b):
 raw=cache[key];lines=raw.splitlines(keepends=True)
 assert 1<=a<=b<=len(lines),(key,a,b,len(lines))
 piece=b''.join(lines[a-1:b]);p=paths[key]
 return {'path':p,'declaration':decl,'line_start':a,'line_end':b,'sha256':digest(raw),'range_sha256':digest(piece),'range_bytes':len(piece),'first_line':lines[a-1].decode().rstrip(),'declaration_lines_within_range':[i for i in range(a,b+1) if re.match(rb'\s*(?:private )?(?:noncomputable )?(?:def|theorem|lemma|abbrev|structure)\b',lines[i-1])],'url':URL+p+f'#L{a}-L{b}','verified_equal_to_pinned_git_blob':True}
def whole(key,decl):return anchor(key,decl,1,len(cache[key].splitlines()))
spec=[
 ('LD1','Finite procyclic cohomology and tame Euler characteristic',[],
  [],[anchor('uo','geo; finite cyclic cocycles; H0 and H1ur cardinality',17,317),anchor('hyp','LocalEulerCharAt, prime-to-residue-characteristic clause',54,59)]),
 ('LD2','Exact two-sided unramified orthogonality on the original finite modules',['LD1'],
  ['Classical finite local Tate duality (Milne ADT I, Corollary 2.3).'],
  [anchor('defs','TDual and twDual',29,81),anchor('defs','cupH1H1TwistedDual',108,111),anchor('hyp','UnramifiedOrthogonalityAt',36,52),anchor('hyp','UnramifiedOrthogonality',207,211),anchor('uo','exact_annihilators and annihilators_of; unramifiedOrthogonality_of',427,577),whole('uofinal','unramifiedOrthogonality')]),
 ('LD3','One normalized invariant family and exact finite Poitou–Tate specialization',['LD2'],
  ['Classical local class field theory and Kummer/Brauer invariant normalization (Milne CFT III, Proposition 3.6, Lemma 3.7 and Section 4, Steps 1–3).','Classical finite-module Poitou–Tate duality (Milne ADT I, Theorem 4.10).'],
  [anchor('global','cycZ; cycMod; NS; GS',91,145),anchor('defs','twDual',45,66),anchor('ptdefs','InvFam; IsNormalised; ConjCompatible; IsLocalInvariants',17,53),anchor('ptdefs','toMuLoc and invAt',63,99),anchor('ptdefs','loc0/loc1/loc2; tr0/tr1/tr2; NineTermExact; ShaDual',105,177),anchor('pt','PoitouTateDuality',13,27)]),
 ('LD4','Global finite cup reciprocity and the single-exception principle',['LD2','LD3'],
  [],[anchor('ptdefs','NineTermExact.sum_eq_zero',203,220),anchor('rec','ReciprocityFromPoitouTateDuality.glob',18,56),anchor('rec','ReciprocityFromPoitouTateDuality.loc',64,100),whole('iv','UpperTheory.V.ML.iv')])
]
raw=(HERE/'main.tex').read_bytes();lines=raw.splitlines(keepends=True)
claims=[]
for cid,title,deps,inputs,srcs in spec:
 starts=[i for i,l in enumerate(lines) if ('\\begin{proposition}['+cid+':').encode() in l]
 assert len(starts)==1,cid
 a=starts[0];b=next(i for i in range(a,len(lines)) if lines[i].strip()==b'\\end{proof}')
 piece=b''.join(lines[a:b+1])
 loc={'file':'local_duality_closure/main.tex','line_start':a+1,'line_end':b+1,'sha256':digest(piece),'bytes':len(piece)}
 claims.append({'id':cid,'title':title,'status':'Complete human proof of the stated finite-module deduction; classical citation leaves explicitly matched.' if inputs else 'Complete elementary deduction in the explicitly stated finite continuous-cohomology framework.','remaining_inputs':inputs,'classical_inputs':inputs,'mathematical_dependencies':deps,'depends_on':deps,'component_ledger':'local_duality_closure/provenance.json','proof_location':loc,'human_proof':loc,'sources':srcs})
scope='Complete UO supplier and precise classical Poitou–Tate interface match on the original fields, finite modules and invariant normalization; finite reciprocity consequences proved. No special-value arithmetic supplier is inferred from duality alone.'
ledger={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.24','date':'2026-11-22','repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,'scope':scope,'range_convention':'One-based inclusive lines; ranges and files match immutable pinned Git blobs.','claims':claims,'source_files':sorted(files,key=lambda f:f['path']),'mathematical_dependency_graph':{c['id']:c['depends_on'] for c in claims},'component_input_boundary':{'bespoke_inputs':[],'classical_inputs':['Finite local Tate duality','Local class field theory with arithmetic Frobenius and the specified cup-product order','Finite-module Poitou–Tate duality'],'not_supplied':['Jacobi-sum/Kolyvagin special-value bound','ThmBab','PointHV','Arithmetic family or RH/GRH prime window']},'validation':{'main_tex_sha256':digest(raw),'source_files':len(files),'source_links':sum(len(c['sources']) for c in claims),'all_sources_equal_pinned_git_blobs':True,'full_lean_build':False,'kernel_replay':False}}
write('provenance.json',ledger)
write('closure.json',{'artifact_version':'0.24','component':'local_duality_closure','complete_endpoints':['LD1','LD2','LD3','LD4'],'closed_bespoke_interfaces':['ReciprocityTheory.Gal.UnramifiedOrthogonality','GlobalTheory.Published.PoitouTateDuality specialized to exactly its stated finite-module hypotheses'],'closure_relative_to_classical_leaves':True,'classical_leaves':ledger['component_input_boundary']['classical_inputs'],'exact_binding_notes':['Finite R modules need not be free.','Invariants are chosen before S, original places, M and its action.','Arithmetic Frobenius and Kummer-left cup require the common negative Brauer-invariant convention.','Conjugation multiplies the scalar cocycle by the root exponent c.','Modified real-place cohomology vanishes for odd ℓ; all archimedean terms vanish in the totally complex case.','No isomorphic replacement field is used.'],'remaining_bespoke_inputs':[],'main_tex_sha256':digest(raw)})
write('classical_references.json',{'accessed':'2026-11-22','references':[{'id':'MilneADT2006','author':'J. S. Milne','title':'Arithmetic Duality Theorems','edition':'second','year':2006,'url':'https://jmilne.org/math/Books/ADTnot.pdf','used':['I Corollary 2.3','I Theorem 2.6 (comparison; LD2 gives its deduction)','I Lemma 2.9 (comparison; LD1 gives its proof)','I Theorem 4.10'],'errata_url':'https://www.jmilne.org/math/Books/add/ADT2006.pdf'},{'id':'MilneCFT2020','author':'J. S. Milne','title':'Class Field Theory','version':'4.03','year':2020,'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf','used':['III Proposition 3.6','III Lemma 3.7','III Section 4, Steps 1–3']}],'citation_policy':'Precise matched classical statements are accepted foundations; the bespoke finite reciprocity and unramified/Euler deductions are written out.'})
(HERE/'report.txt').write_text('LD1–LD4: CLOSED FINITE DUALITY SUPPORT\n\n'+scope+'\n\nThe complete matched classical boundary is recorded in classical_references.json. Exact source and proof bytes are in provenance.json. LD2 and LD3 supply both hypotheses of the source Iv interface; the finite special-value arithmetic downstream remains a separate OS task.\n\nNo Lean build or kernel replay was performed.\n')
print(json.dumps(ledger['validation'],indent=2))
