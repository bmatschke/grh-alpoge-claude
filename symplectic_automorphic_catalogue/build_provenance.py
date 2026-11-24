#!/usr/bin/env python3
"""Exact pinned sources and semantic boundaries for CX1--CX9 (v0.28)."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
C='symplectic_automorphic_catalogue'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO='https://github.com/CocoSgt/riemann-hypothesis-lean'
URL=REPO+'/blob/'+PIN+'/'
P='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
D=P+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
F='src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/'
G=P+'GaloisLibrary/CrystallineBaseChange/'
A=P+'ModularityArgument/AutomorphyLifting/'
PATHS={
 'endpoint':D+'AfStmt.lean','iso':P+'AutomorphicForms/IsoOfFrob.lean',
 'level':P+'AutomorphicForms/BlochKatoSelmerVanishes.lean',
 'dual':P+'AutomorphicForms/CongruenceNumberRankThree.lean',
 'flag':P+'AutomorphicForms/LocIsotypic.lean',
 'published':P+'PublishedTheorems/GelfandKazhdanReal.lean',
 'sig':G+'CqStmt.lean',
 'weyl':P+'AutomorphicForms/TemperedLocalComponents/WeylC.lean',
 'cells':P+'AutomorphicForms/TemperedLocalComponents/CohBoundFree.lean',
 'card':D+'BrCardP.lean','conj':D+'VConjP.lean',
 'integral':P+'ModularityArgument/IntegralDeterminants/IntPHolds.lean',
 'safe':A+'AdmissibleLevelRestriction/UnlAllOf.lean',
 'aut':A+'IsAutCsdA.lean','weak':A+'WeakOfAtt.lean',
 'pol':D+'UnderCPl.lean',
 'poldef':'src/Development/AbelianVarietyTheory/Definitions/GaloisGeometry/DualIsConjByOne.lean',
 'keep':D+'KeepLevel.lean','reslevel':D+'LevelAdmissibleRestrictionHolds.lean',
 'admn':D+'AutQN.lean',
 'count':D+'FrobeniusTraceCountBoundOfCmEigensystemCount.lean',
 'num':D+'VWinNumN.lean','top':D+'VWLevel.lean',
 'twists':G+'TwCard.lean','two':G+'ResTwo.lean','quad':G+'QuadFam.lean',
 'roots':G+'RootSum.lean','frob':G+'FrobEx.lean',
 'power':P+'BuildingsResidueChars/FrobeniusPowerCompatibility.lean',
 'windef':F+'WinDefs.lean','win':F+'SumThree.lean',
 'hyp':D+'AutomorphicFormHyp.lean','lit':D+'LitAut.lean',
 'image':D+'IsAut4.lean','imageproducer':D+'Sp4In.lean',
 'comparison':D+'TIsoOfFrob.lean',
}

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,x):
 (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def main(repo):
 cache={}
 for k,p in PATHS.items():
  b=(repo/p).read_bytes()
  assert b==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+p]),p
  cache[k]=b

 def anchor(k,decl,role=None,start=None,end=None):
  b=cache[k];lines=b.decode().splitlines()
  if start is None:
   pat=re.compile(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure)\s+'+re.escape(decl)+r'(?=[\s:(])')
   hits=[i+1 for i,s in enumerate(lines)if pat.match(s)]
   assert len(hits)==1,(k,decl,hits)
   start=hits[0]
  if end is None:
   end=len(lines)
   for i in range(start,len(lines)):
    if re.match(r'^(?:(?:private|noncomputable)\s+)*(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[',lines[i]):
     end=i;break
   while end>start and not lines[end-1].strip():end-=1
  frag=b''.join(b.splitlines(keepends=True)[start-1:end])
  return {'path':PATHS[k],'declaration':decl,'line_start':start,'line_end':end,
   'sha256':sha(b),'range_sha256':sha(frag),'range_bytes':len(frag),
   'first_line':lines[start-1],'url':URL+PATHS[k]+f'#L{start}-L{end}',
   'role':role or 'Exact source statement or comparison; only the rank-four scope of the stated CX claim is promoted.',
   'verified_equal_to_pinned_git_blob':True}
 def many(k,ds,role=None):return[anchor(k,d,role)for d in ds]

 specs=[
  ('CX1','Uniform CM counting from fixed cells and actual polynomial coefficients',
   ['HP1','HP2','HP4'],['CX-CL','CX-BS','CX-BLS','CX-SMO','CX-ANT'],
   many('iso',['infOf'])+many('sig',['SigP','CardP'])+
   many('weyl',['UpperTheory.V.Af.weylC'])+many('cells',['UpperTheory.V.Af.cohBoundFree'])+
   many('card',['UpperTheory.V.Br.cardP_of_prints'])+
   many('published',['ClozelCohC','BorelInjC','BorelSerreFL'],
    'Precisely matched classical rank-four imaginary-quadratic specialization; the whole all-field source predicate is not automatically promoted.')+
   many('level',['KLev','HasFixed'])),
  ('CX2','Full global labels, algebraicity and exact Aut(C) conjugation',
   ['CX1'],['CX-CL','CX-SMO','CX-CFT'],
   many('published',['ClozelConjC'])+many('sig',['ConjP','CharConj','SatOfPol'])+
   many('conj',['dual_conj','UpperTheory.GalN.V.conjP_alt'])+
   many('poldef',['DualIsConjBy','PolarizedPair'])+many('level',['algSat'])),
  ('CX3','Arithmetic inverse-Frobenius integrality with all valuations and purity',
   ['CX2','RV4'],['CX-BG','CX-PH'],
   many('sig',['PureP','IntP'])+many('iso',['SlopesIn'])+
   many('integral',['intP_holds'],
    'Alternative classical proof of the exact rank-four slopes/integrality specialization; the source full all-rank IntP and its unitary-descent proof are not promoted.')+
   many('windef',['EigData'])+many('win',['Win'])+
   many('level',['FrobEig','algSat'])),
  ('CX4','Original quadratic restriction, exact polarized avatar, and actual Galois comparison',
   ['CX3'],['CX-CFT','CX-SMO','CX-ANT','CX-BG','CX-PH'],
   many('endpoint',['AdmRAlt'])+many('aut',['IsAutQA'])+many('weak',['WitA'],
    'The original field is retained as part of IsAutQA, but this stronger witness is not needed for the classical catalogue shortcut.')+
   many('dual',['DualTw','IsCycWt'])+many('level',['KillsMu','AttC','LevelAt','Level'])+
   many('pol',['UpperTheory.V.Z.Bc.polarization_k_of_printed_results'],
    'Full actual n=4 polarization specialization is proved directly; no full Hypotheses-prime promotion.')+
   many('poldef',['PolarizedPair'])+many('iso',['IsoOfFrob'])+
   many('comparison',['UpperTheory.V.Af.iso_of_frobenius_of_printed_results'])+
   many('sig',['CompatP'],
    'Away-ell full compatibility and ell semisimplified compatibility needed here only; no unrestricted source CompatP equality at ell is claimed.')),
  ('CX5','Original level M gives auxiliary automorphic level M^7',
   ['CX4'],['CX-CFT','CX-BGP','CX-PH','CX-LL','CX-NF','CX-SMO'],
   many('safe',['SafeRA'])+many('level',['LevelAway','LevelAt','Level','KLev','HasFixed','FrobEig'])+
   many('flag',['FlagAt'])+many('sig',['LevelP','CompatP'],
    'Semantic comparison only: the proved catalogue uses M^7, and semisimplification at ell, instead of promoting the stronger unchanged-level/full-WD interfaces.')+
   many('keep',['levelCore_alt','levelPA_alt'],
    'Source route bypassed by a polynomial conductor bound; its original unchanged-level statement remains unpromoted.')+
   many('admn',['LevelPNAlt'],
    'Not promoted. The actual four-weight representation is preserved while only the auxiliary label level is enlarged.')),
  ('CX6','Fixed eighteen quadratic fields, at most sixteen self twists, and two extensions',
   [],['CX-ANT'],
   many('sig',['QuadFam','TwCard','ResTwo'])+many('quad',['UpperTheory.V.Br.quadFam'])+
   many('twists',['UpperTheory.V.Br.twCard'])+many('two',['part_one','part_two','UpperTheory.V.Br.resTwo'])+
   many('count',['exists_over','exists_avoid'])),
  ('CX7','Complete fixed-field catalogue preceding all coefficient choices',
   ['CX1','CX2','CX3','CX4','CX5'],[],
   many('windef',['EigData','EigData.Classifies','exists_eigData'])+
   many('count',['CountPAlt','countP_alt'],
    'Exact original-Q-restriction specialization only, with label level M^7; no full unchanged-level all-rank CountPAlt promotion.')+
   many('sig',['SigP'])),
  ('CX8','Full literal SP9 rank-four catalogue and all same-object quantifiers',
   ['CX6','CX7'],[],
   many('count',['bit_of_fibre','CountQAlt','countQ_alt'],
    'The actual rank-four weight family needed by SP9 is proved in full. All-rank CountQAlt remains unpromoted.')+
   many('windef',['EigData','EigData.Classifies','RootSum'])+
   many('roots',['UpperTheory.V.Br.rootSum'])+many('frob',['UpperTheory.V.Br.frobEx'])+
   many('power',['UpperTheory.frobenius_power_compatibility'])+
   many('endpoint',['AdmRAlt'])+many('level',['FrobEig'])),
  ('CX9','Literal universal NumberSp4Alt with exponent 225',
   ['CX8','SP9'],[],
   many('endpoint',['NumberSp4Alt'])+many('num',['est','size','number_sp4_of_admissible_to_admissible_n'])+
   many('top',['numberSp4_n_alt'],
    'Literal conclusion supplied by CX9 through the specialized catalogue; full antecedent Hypotheses-prime is not required or promoted.')),
 ]

 b=(HERE/'main.tex').read_bytes();ls=b.splitlines(keepends=True)
 claims=[]
 for cid,title,deps,classics,sources in specs:
  hits=[i for i,t in enumerate(ls)if f'\\begin{{proposition}}[{cid}:'.encode()in t]
  assert len(hits)==1,(cid,hits)
  start=hits[0];end=next(i for i in range(start+1,len(ls))if ls[i].strip()==b'\\end{proof}')
  frag=b''.join(ls[start:end+1])
  loc={'file':C+'/main.tex','line_start':start+1,'line_end':end+1,
       'sha256':sha(frag),'bytes':len(frag)}
  claims.append({'id':cid,'title':title,
   'status':'Complete human proof of the stated scope relative only to individually named classical results and prior proved suppliers.',
   'depends_on':deps,'mathematical_dependencies':deps,'classical_inputs':classics,
   'remaining_inputs':[],'remaining_bespoke_inputs':[],
   'component_ledger':C+'/provenance.json','proof_location':loc,'human_proof':loc,'sources':sources})

 frontier=[
  anchor('admn','LevelPNAlt','Unchanged-level, all-rank interface remains unpromoted; not needed for the proved CX9 endpoint.'),
  anchor('count','CountQAlt','All-rank and all-weight predicate remains unpromoted; CX8 closes precisely the original four-weight family.'),
  anchor('hyp',"Hypotheses'",'Whole compound literature hypothesis is not promoted.'),
  anchor('lit','LiteratureRankNHypothesis','Whole compound literature record is not promoted.'),
  anchor('image','SymplecticFourImageDense','Independent actual automorphy supplier; CX never constructs IsAutQA for an arbitrary representation.'),
  anchor('imageproducer','sp4In_alt','Actual image-density producer remains downstream continuation work, not a premise of NumberSp4Alt as a universal theorem.'),
 ]
 files=[{'path':PATHS[k],'sha256':sha(cache[k]),'bytes':len(cache[k]),'lines':len(cache[k].splitlines()),
         'url':URL+PATHS[k],'verified_equal_to_pinned_git_blob':True}
        for k in sorted(PATHS,key=lambda k:PATHS[k])]
 allanchors=[a for c in claims for a in c['sources']]+frontier
 classical=classical_registry()
 dump('classical_inputs.json',classical)
 dump('provenance.json',{'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.28',
  'component':C,'source_repository':REPO,'source_commit':PIN,'repository':REPO,'commit':PIN,
  'main_tex_sha256':sha(b),'source_files':files,'claims':claims,'retained_frontier':frontier,
  'scope':'Nine complete proofs through literal NumberSp4Alt; no all-rank CountQAlt or unchanged-level LevelPNAlt claim, no automorphy construction.',
  'validation':{'claim_count':len(claims),'claim_source_links':sum(len(c['sources'])for c in claims),
    'frontier_source_links':len(frontier),'source_file_count':len(files),'proof_range_count':len(claims),
    'all_source_blobs_equal_pin':True,'all_source_ranges_hashed':True,'kernel_replayed':False}})
 dump('source_hashes.json',{'source_repository':REPO,'source_commit':PIN,'repository':REPO,'commit':PIN,'component':C,'files':files})
 dump('source_validation.json',{'artifact_version':'0.28','component':C,'source_commit':PIN,
   'source_files_checked':len(files),'source_ranges_checked':len(allanchors),'proof_ranges_checked':len(claims),
   'all_files_equal_pinned_git_blobs':True,'all_range_hashes_verified':True,'all_proof_ranges_verified':True,
   'main_tex_sha256':sha(b),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'kernel_replayed':False,
   'meaning':'Byte provenance and proof-locator verification only; independent mathematical review is recorded separately.'})

 closure={
  'artifact_version':'0.28','component':C,'commit':PIN,'claims':[c['id']for c in claims],
  'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
  'endpoint':'UpperTheory.V.Af.NumberSp4Alt','endpoint_claim':'CX9',
  'human_status':'literal_endpoint_proved_relative_to_precisely_matched_classical_theorems',
  'main_tex_sha256':sha(b),'supplied':[
   {'name':'Exact uniform finite SP9 catalogue','claim':'CX8','status':'complete',
    'quantifier_order':'Fixed eighteen fields and c_* first; then e,M,p and catalogue; then ell,Omega,iota,places,Frobenius,families.',
    'bounds':{'catalogue_exponent':224,'catalogue_constant':'32 * sum_{i=1}^{18} c_{K_i}',
              'original_galois_level':'M','auxiliary_automorphic_level':'M^7'}},
   {'name':'UpperTheory.V.Af.NumberSp4Alt','claim':'CX9','status':'complete',
    'bounds':{'A':225,'C':'c_* * 2^225'},
    'same_object_scope':'Every original AdmRAlt; original Omega and coefficient isomorphism; every original place and arithmetic Frobenius. No coefficient or field change of the target representation.'}],
  'remaining_bespoke_inputs':[],
  'retained_theorem_hypotheses':[
   'NumberSp4Alt original quantified e>=2, M>=1, p prime>=5, p not dividing M, k>0 and three k-th roots of unity.',
   'Later arbitrary odd ell different from p, original Omega, iota, place, arithmetic Frobenius and pairwise nonisomorphic finite family.',
   'Each representation satisfies literal AdmRAlt including its actual IsAutQA, Level, irreducibility, dual multiplier and SafeRA. These are original theorem hypotheses, not additional CX leaves.'],
  'classical_inputs':[x['id']for x in classical['inputs']],
  'prior_proved_suppliers':['HP1','HP2','HP4','RV4','SP9'],
  'not_promoted':['UpperTheory.GalN.V.Win.N.CountQAlt (all ranks and weights)',
                  'UpperTheory.GalN.V.LevelPNAlt (unchanged automorphic level)',
                  'UpperTheory.GalN.V.Win.N.CountPAlt (all ranks and original levels)',
                  'UpperTheory.V.Br.IntP (full all-rank statement)',
                  'UpperTheory.V.Af.Hypotheses-prime','LiteratureRankNHypothesis',
                  'SymplecticFourImageDense','Unconditional CountII or CountIII'],
  'safe_whole_target_retirement_candidates':[],
  'partial_target_updates':[{'id':'DA26-SP-05','supplied_by':['CX8','CX9'],
    'supplied_scope':'Complete uniform SP9 rank-four catalogue and literal NumberSp4Alt.',
    'remaining_human_scope':'The compound all-rank CountQAlt and unchanged-level LevelPNAlt source package remains unpromoted; it is no longer a premise of the actual paired-count route.'}],
  'retirement_reason':'The actual rank-four endpoint is supplied, but the older compound target also records all-rank and unchanged-level source scopes. Preserve its identity and narrow its remaining scope rather than retiring it wholesale.'}
 dump('closure.json',closure)
 dump('remaining_inputs.json',{'artifact_version':'0.28','component':C,'remaining_bespoke_inputs':[],
  'classical_inputs':[x['id']for x in classical['inputs']],
  'original_theorem_hypotheses':closure['retained_theorem_hypotheses'],
  'source_frontier':frontier,'not_promoted':closure['not_promoted']})
 dump('next_targets.json',{'artifact_version':'0.28','component':C,'targets':[],
   'reason':'No bespoke input remains inside the actual CX8/CX9 supplier. Continue the independent actual ImageDense obligation using its existing target; do not reopen general all-rank source packages just to reproduce this endpoint.',
   'continuation_source_anchors':frontier[-2:]})
 dump('retirement_candidates.json',{'artifact_version':'0.28','component':C,'targets':[],
  'partial_target_updates':[
  {'id':'DA26-SP-05','supplied_by':['CX8','CX9'],
   'scope':'Complete uniform SP9 rank-four catalogue and literal NumberSp4Alt.',
   'source':anchor('endpoint','NumberSp4Alt'),
   'do_not_infer':'No full CountQAlt, LevelPNAlt, Hypotheses-prime or ImageDense promotion.'}]})

 report='''CX1--CX9: complete actual symplectic catalogue and NumberSp4Alt

The complete human proof is in main.tex. CX8 supplies every clause of the exact
SP9 labelled catalogue, with constants before e,M,p and the catalogue before
ell,Omega,iota,places,Frobenius and families. CX9 then supplies the literal
NumberSp4Alt. No bespoke supplier remains inside this universal counting theorem.
An actual representation still has to satisfy AdmRAlt, including IsAutQA; this
component does not construct automorphy and does not prove ImageDense.

The simplification is specific and quantitative. SafeRA forces ell|M for weights
(e+1,e,1,0). After a fixed imaginary-quadratic restriction with irreducible image,
the actual weak automorphy witness is polarized using theta*cyclo^3. Published
Galois compatibility identifies its representation with the original restriction.
At ell only semisimplified local-global compatibility is used; the unknown
monodromy increases a four-dimensional conductor by at most three. Thus the
automorphic label can be placed at principal level M^7. The target representation
continues to have level M. A fixed CW model and the actual coefficient module give
c_K M^224(e+2)^32 labels. Eighteen fixed imaginary quadratic fields, at most sixteen
self twists, at most two extensions of an irreducible quadratic restriction, and
at most sixteen root multisets yield c_*[M(e+2)]^224 labels over Q.

Frobenius signs are explicit. Geometric eigenvalues are q^(3/2)*Satake. Their
inverses are the arithmetic eigenvalues used in SP9. At a coefficient prime
different from p they are units by a stable lattice. At p their crystalline
geometric slopes lie in [-e-1,0], by weak admissibility applied to the lowest
subobject and highest quotient. The inverse eigenvalues, and q^(e+1) times their
inverses, are therefore integral at every number-field valuation. Pure size gives
the required trace bound. Full global labels are retained; one-prime traces never
classify representations. Aut(C) permutes the full label multiset including bits.

The exact final constants may be chosen A=225 and C=c_*2^225. The integer product
is chosen before all auxiliary coefficient choices and representation families.
DA26-SP-05 is narrowed, not retired wholesale: its actual catalogue specialization
is now supplied. All-rank CountQAlt, unchanged-level LevelPNAlt, all-rank CountPAlt/IntP,
Hypotheses-prime and LiteratureRankNHypothesis remain unpromoted. They are not
additional premises of CX9.

Classical inputs are individually stated, with primary literature and exact
specializations in classical_inputs.json. They include Clozel cohomology and
rationality; Borel--Serre and cuspidal-cohomology injection; the polarized
automorphic Galois, local-global and purity theorems; p-adic Hodge comparison;
local Langlands conductors and generic newvectors; class field theory,
Chebotarev and strong multiplicity one. No blanket source literature record is
declared proved. Mathematical review, byte provenance and draft TeX checks are
different validations; no Lean kernel replay or PDF generation is claimed.
'''
 (HERE/'report.txt').write_text(report)
 inventory=['main.tex','build_provenance.py','validate_tex.py','provenance.json','source_hashes.json',
   'source_validation.json','classical_inputs.json','closure.json','remaining_inputs.json',
   'next_targets.json','retirement_candidates.json','report.txt','tex_validation.json']
 entries=[]
 for name in inventory:
  p=HERE/name
  if p.is_file():entries.append({'path':C+'/'+name,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
 for comp in ['chain_closure_core','rank_one_cohomology','symplectic_count_closure']:
  for name in ['main.tex','provenance.json']:
   p=HERE.parent/comp/name
   entries.append({'path':comp+'/'+name,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,
                   'role':'Previously proved supplier; preserved unchanged.'})
 dump('input_manifest.json',{'artifact_version':'0.28','component':C,'source_commit':PIN,
   'files':entries,'excluded':['input_manifest.json','independent reviews','downstream audit and package outputs','scratch research PDFs']})
 print(json.dumps({'claims':len(claims),'source_links':len(allanchors),'source_files':len(files),
   'main_sha256':sha(b),'provenance_sha256':sha((HERE/'provenance.json').read_bytes())},indent=2))

def classical_registry():
 def item(cid,name,author,title,url,locator,statement,specialization,refs,extra=None):
  d={'id':cid,'name':name,'author':author,'title':title,'url':url,
     'theorem_reference':locator,'accepted_statement':statement,
     'exact_specialization':specialization,'web_source_refs':refs,
     'status':'Accepted named classical theorem; actual specialization and joins proved in CX.'}
  if extra:d.update(extra)
  return d
 return {'schema':'rh-classical-input-registry/1','artifact_version':'0.28','component':C,
  'accessed':'2026-11-22','inputs':[
  item('CX-CL','Cohomology and rationality of regular algebraic cuspidal GLn representations',
   'Laurent Clozel','Motifs et formes automorphes: applications du principe de fonctorialite (1990)',
   'https://www.jmilne.org/math/Books/AA1988a.pdf','Theorem 3.13 and Lemma 3.14; pp.77--159',
   'Regular C-algebraic cuspidal representations are cohomological for the matching algebraic coefficient; their finite parts have number-field models and Aut(C) conjugates remain cuspidal with permuted infinity type.',
   'Only GL4 over fixed imaginary quadratic K, with parallel infOf(e+1,e,1,0). CX1 constructs the actual highest weight (-3,-3,-e-1,-e-1) and a polynomial rank bound. CX2 explicitly treats the algebraic Satake normalization and polarized subset.',
   ['turn161606053search8','turn870773939view0','turn870773939view1'],
   {'checked_primary_author_restatements':[
    {'url':'https://people.math.osu.edu/patrikis.1/variationsrevision.pdf','locator':'Theorem 2.4.5 (explicit C-algebraic form of Clozel 3.13)'},
    {'url':'https://math.berkeley.edu/~swshin/FieldRat.pdf','locator':'Lemma 2.12 and Proposition 2.15 (cohomological and rationality specialization)'}],
    'scope_guard':'No L-algebraic substitution for the C-algebraic theorem; the integer power q^{j(j-1)/2} in CX.10 removes the square-root normalization ambiguity.'}),
  item('CX-BS','Finite arithmetic CW model','Armand Borel and Jean-Pierre Serre',
   'Corners and arithmetic groups, Comment. Math. Helv. 48 (1973), 436--491',
   'https://doi.org/10.1007/BF02566134','Theorem 9.3 and the manifold-with-corners construction',
   'A torsion-free arithmetic quotient, with the rational split central direction removed, admits the compact Borel--Serre manifold-with-corners model and hence finite CW type.',
   'CX1 uses only finitely many level-three components for each fixed imaginary quadratic field. It proves torsion-freeness and the covering index <=(3L)^32, then counts lifted cells. No uniform family theorem is assumed.',
   ['turn837203340search37','turn619455920search9']),
  item('CX-BLS','Cuspidal cohomology injects ordinary cohomology','Armand Borel, Jean-Pierre Labesse and Joachim Schwermer',
   'On the cuspidal cohomology of S-arithmetic subgroups of reductive groups over number fields, Compositio 102 (1996), 1--40',
   'https://www.numdam.org/item/CM_1996__102_1_1_0.pdf','Theorem 5.2, arithmetic case; following remark identifies the cuspidal direct summand',
   'Cuspidal relative Lie algebra cohomology is a direct summand of arithmetic cohomology with the same finite-dimensional algebraic coefficient.',
   'CX1 applies to GL4/K at principal level3L and its same coefficient E_e. Distinct cusp classes yield distinct nonzero summands; their number is bounded by all ordinary cohomology dimensions.',
   ['turn944350409view3','turn582477879view2']),
  item('CX-BG','Polarized automorphic Galois representations, local-global compatibility, Hodge numbers and purity',
   'Thomas Barnet-Lamb, Toby Gee, David Geraghty and Richard Taylor',
   'Potential automorphy and change of weight, Annals of Mathematics 179 (2014), 501--609',
   'https://www.ma.imperial.ac.uk/~tsg/Index_files/potentialautomorphy.pdf','Theorem 2.1.1, clauses (1)--(4)',
   'For regular algebraic cuspidal polarized pairs over CM fields and every coefficient prime, the semisimple Galois representation exists; full Frobenius-semisimplified compatibility and purity hold away the coefficient prime; de Rham Hodge numbers are lambda_i+n-i; spherical places above that prime give crystalline representations.',
   'CX4 first constructs the actual polarized pair and corrects its sign, then identifies the original irreducible restriction by Chebotarev. CX3 uses every coefficient prime, including2 for non-p valuations, and the coefficient prime p for integrality. Hodge numbers are(0,-1,-e,-e-1); geometric weight is -e-1; arithmetic roots are their inverses.',
   ['turn522272262view0','turn128357842view2','turn128357842view3']),
  item('CX-BGP','Semisimplified local-global compatibility at the coefficient prime',
   'Thomas Barnet-Lamb, Toby Gee, David Geraghty and Richard Taylor',
   'Local-global compatibility for l=p, II, Ann. Sci. ENS 47 (2014), 165--179',
   'https://arxiv.org/pdf/1105.2242','Theorem A; Theorem 1.1 and Corollary1.2',
   'At every place over l, the semisimplified Weil--Deligne representation of a regular algebraic essentially conjugate-self-dual cuspidal automorphic representation matches rec(pi_v |det|^{(1-n)/2}) up to semisimplification.',
   'CX5 uses only equality of semisimple Weil representations. The possibly unmatched nilpotent operator is bounded by rankN<=3. No Shin-regularity or full monodromy comparison at l is inferred.',
   ['turn522272262view1','turn128357842view5']),
  item('CX-PH','Finite-coefficient p-adic Hodge exactness and weak admissibility',
   'Jean-Marc Fontaine; Pierre Colmez and Jean-Marc Fontaine; Laurent Berger',
   'Construction des representations p-adiques semi-stables (2000), with classical de Rham monodromy theorem',
   'https://webusers.imj-prg.fr/~pierre.colmez/CF.pdf','Proposition4.2 and corollary to Theorem4.3; Berger, Representations p-adiques et equations differentielles, Theorems0.6 and5.19 (arXiv v3)',
   'The potentially semistable comparison functor is exact on its category; de Rham representations of finite p-adic local fields are potentially semistable; crystalline modules are weakly admissible with the corresponding filtration and tensor, dual and scalar-extension compatibilities.',
   'Only finite common coefficient fields after the proved Baire capture. CX4 does not assume arbitrary extensions of de Rham characters are de Rham. CX5 applies exactness after identification with an automorphic de Rham representation. CX3 derives slopes in[-e-1,0] from the subobject and quotient inequalities, so inverse geometric Frobenius roots are integral.',
   ['turn582477879view1','turn555757849view0','turn878855938view1'],
   {'additional_primary_url':'https://arxiv.org/pdf/math/0102179'}),
  item('CX-LL','Local Langlands conductor compatibility','Michael Harris and Richard Taylor; Guy Henniart; Peter Scholze',
   'The local Langlands correspondence for GLn over p-adic fields, Inventiones192 (2013), 663--715',
   'https://people.mpim-bonn.mpg.de/scholze/LocalLanglands.pdf','Theorem14.1 (epsilon-factor compatibility), with the standard extension from supercuspidals to Weil--Deligne parameters',
   'The GLn correspondence preserves local L and epsilon factors, hence Artin conductor exponents; it is compatible with characters, unramified twists and spherical parameters.',
   'CX5 only uses conductor and spherical compatibility. Its elementary formula a(rho,N)=a(rho)+dimV^I-dim(kerN)^I bounds monodromy loss by3, and unramified normalization does not change conductors.',
   ['turn582477879view0','turn619455920search6']),
  item('CX-NF','Generic local newvectors','Herve Jacquet, Ilya Piatetski-Shapiro and Joseph Shalika',
   'Conducteur des representations du groupe lineaire, Math. Ann.256 (1981), 199--214',
   'https://lesesvre.perso.math.cnrs.fr/newforms-references/jpss.pdf','Theorem5.1 (printed p.211)',
   'An irreducible generic representation of GLn over a nonarchimedean local field has nonzero K1(p^a)-fixed vectors at its conductor exponent a, and a=0 is the spherical case.',
   'CX5 takes the smaller principal subgroup modulo p^{7v(M)} and tensors local vectors. The original target Galois level M is never replaced by M^7.',
   ['turn944350409view4','turn966433789view0']),
  item('CX-CFT','Finite local/global reciprocity and norm compatibility','J. S. Milne',
   'Class Field Theory, version4.03 (2020)',
   'https://www.jmilne.org/math/CourseNotes/CFT.pdf','ChapterI, Theorem1.1 and norm functoriality; ChapterIII section3; ChapterV section5',
   'Finite abelian characters correspond to finite Hecke characters, local reciprocity is compatible with norms and the cyclotomic action, and a quadratic character kills norms from its quadratic extension.',
   'CX4 explicitly constructs chi from theta*cyclo^3 and sign-corrects by eta_K, preserving equality only on G_K. CX5 proves the needed norm congruence by a determinant in an integral local basis.',
   ['turn155211860view0']),
  item('CX-SMO','Strong multiplicity one and genericity for cuspidal GLn','Jacquet, Piatetski-Shapiro and Shalika; James W. Cogdell',
   'Lectures on L-functions, converse theorems, and functoriality for GLn (2004)',
   'https://people.math.osu.edu/cogdell.1/fields-www.pdf','Theorem4.3 (strong multiplicity one); Corollary4.1.2 (global and local genericity of cuspidal representations)',
   'Cuspidal GLn representations agreeing at almost all finite places are globally isomorphic; each local component is generic.',
   'CX1 counts distinct global cusp labels, CX2 transports polarization, CX4 constructs the actual polarization by comparing Satake parameters, and CX5 invokes local newvectors only for genuine cusp components.',
   ['turn555757849view1','turn878855938view3']),
  item('CX-ANT','Finite arithmetic of quadratic fields, class groups and Chebotarev','J. S. Milne',
   'Algebraic Number Theory, version3.08 (2020)',
   'https://www.jmilne.org/math/CourseNotes/ANT.pdf','Quadratic integer-basis/discriminant calculation; finite ideal class group; Theorem8.31 (Chebotarev)',
   'Quadratic fields have the usual integral bases and discriminants; number-field class groups are finite; Frobenius conjugacy classes outside any finite set are dense in finite Galois quotients.',
   'CX6 constructs eighteen fields with pairwise prime discriminants by an elementary Euclidean argument. CX1 uses class-group finiteness for one fixed adelic quotient. CX4 passes cofinite Frobenius equality to continuous traces and proves the ensuing semisimple character comparison.',
   ['turn807102395view1'],{'note':'Primary ANT URL and theorem locator were already verified in preceding AX/LD components; this registry reuses that stable accepted leaf.'})
 ]}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=HERE.parent.parent/'lean-source')
 main(parser.parse_args().repo)
