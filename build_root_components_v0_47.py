#!/usr/bin/env python3
"""Bind the two root-authored mathematical chapters to their actual source contracts.

This records human proofs and source locations; it does not run Lean or prove
the mathematical text by executing the source.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip()==PIN
sha=lambda x:hashlib.sha256(x).hexdigest()
S='src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
H=S+'HaarTransversals/'
U=H+'UnitaryHaarProducts/'
F='src/Development/AbelianVarietyTheory/Proofs/FlagMeasures/'
D='src/Development/AbelianVarietyTheory/Definitions/SemilocalFrames/'
P='src/Formalism/PeriodIntegrals/'
C='src/CompanionTheory/HarishChandraModules/KFiniteAnalyticVectors/FundamentalDomainCusps/'

DATA={
 'row_finiteness_v47':{
  'prefix':'RFD','count':9,'A':[1],
  'groups':{
   'original_contract':[(H+'RowsDef.lean',19,119,'All original quotient, arbitrary test-function/vector, weak-operator and RowsFinDim quantifiers')],
   'original_finiteness_producer':[(F+'RowsFinDimLink.lean',1,None,'Original general RowsFinDim producer'),(C+'AutomorphicFormsFiniteDimensional.lean',1,None,'Original automorphic finite-dimensionality endpoint'),(C+'RowsFinDimOf.lean',28,None,'Original assembly replaced by the fixed-level Harish-Chandra simplification')],
   'original_instance': [('src/Formalism/SharpRestriction/CuspSpanNormBounds/GlobAut.lean',1,205,'Original AutInst, unitary group, lattice, measures, quotient and regular action')],
   'schur_projector':[(U+'RowsBij.lean',170,None,'Original product coefficient and four-vector Schur identities, projection and cyclic evaluation')],
   'actual_row_consumer':[(S+'FlagStabilizerTensors/RootLatticeThresholds/AllRowsAddFin.lean',1,None,'Original RowsFinDim specialization'),(F+'AllRowsAtRecord.lean',23,None,'Same-object original row installer'),(F+'IrreducibilityRowOfConcreteAutomorphicData.lean',18,None,'Conditional common-X/tie/count family consumer')]
  },
  'claim_groups':{1:['original_contract','original_finiteness_producer'],2:['original_instance','original_contract'],3:['original_instance','original_contract'],4:['schur_projector','original_contract'],5:['schur_projector','original_contract'],6:['schur_projector','original_contract'],7:['original_contract','original_finiteness_producer'],8:['original_contract','original_finiteness_producer'],9:['actual_row_consumer','original_contract']},
  'deps':{1:[],2:['FV4'],3:['RFD1','FV1','FV2','FV3','FV4','FV5','FV6','FV7','FV8','FV9','FV10','RQC2','RQC3'],4:[],5:['RFD4'],6:['RFD5'],7:['RFD3','RFD4','RFD6'],8:['RFD2','RFD5','RFD7'],9:['RFD8']+['ARO'+str(i) for i in range(17,31)]},
  'scopes':[
   'Published Harish-Chandra finite multiplicity for every irreducible continuous unitary representation on each original arithmetic real quotient, compact center and every positive Haar normalization.',
   'Arbitrary original locally constant function supported in Kset has one common compact-open bi-invariance level; no symmetry or idempotence premise.',
   'The actual finite-level adelic quotient decomposes into finitely many original arithmetic real components with the actual quotient measure.',
   'Complete finite tensor product of all original irreducible Hilbert representations with arbitrary original unit vectors, exact phInf and product formal degree.',
   'The literal weak operator is the self-adjoint Schur projection with T R(g) T=m(g)T; no spectral discreteness assumption.',
   'Every vector in the projection range gives a bounded intertwiner by the explicit cyclic isometry and all mixed inner products.',
   'Full finite-dimensionality at the one original finite level, without requiring the supplied vector to be K-finite or smooth.',
   'The entire literal RowsFinDim, with all original AutInst, measures, fundamental domains, arbitrary e/w, Hilbert spaces and weak integral operators.',
   'Exact substitution in the original ARO row construction; original common-X/ties/gap/count and simultaneous family inputs remain separate.'
  ],
  'foundations':[
   {'id':'RFD_HARISH_CHANDRA','kind':'checked_published_foundation','url':'https://homepages.math.uic.edu/~rtakloo/papers/borel/borel3.pdf','locator':'Borel, Automorphic forms on reductive groups, sections6.5,8.4,10 (printed subparagraphs8.5–8.6), pages17,23,27–28','statement':'Admissibility and finite dimensionality of automorphic forms of fixed finite compact type and finite-codimensional central ideal, including compact-finite vectors of irreducible L2 submodules. Exact finite multiplicity application proved in RFD1.'},
   {'id':'RFD_STANDARD_ANALYSIS','kind':'standard_mathematical_background','statement':'Haar/Fubini/Riesz theory, finite Hilbert tensor products, commutants, compact-open subgroups and bounded unitary intertwiners. All representation-specific and operator-normalization deductions are proved in the chapter.'},
   {'id':'RFD_ORIGINAL_CONDITIONAL_CONSUMER','kind':'retained_original_data_for_consumer_only','statement':'Only RFD9 retains the common X, its ties, original gap and arithmetic counting producer required by ARO; these are not hypotheses of the full RFD8 theorem.'}
  ],
  'external':{1:['RFD_HARISH_CHANDRA','RFD_STANDARD_ANALYSIS'],9:['RFD_ORIGINAL_CONDITIONAL_CONSUMER','RFD_STANDARD_ANALYSIS']},
  'default_external':['RFD_STANDARD_ANALYSIS'],
  'completed':['Full original RowsFinDim, with no added gap, weight, cuspidality, e-idempotence or w-smoothness assumption','Removal of the RowsFinDim input from the stated original row consumers'],
  'not_claimed':['Full common HidaSetting/ties','Actual CountIdempotentsClass','Any additional whole global leaf closure','Complete RH or GRH'],
  'endpoint':'RFD8'
 },
 'adelic_setting_v47':{
  'prefix':'ASG','count':18,'A':[3],
  'groups':{
   'setting_contract':[(U+'SettingBlocks.lean',19,207,'All original A/L/P/Rf/Xu/Bu/Pi/Mu/W block fields'),(U+'SettingBlocks.lean',337,381,'Exact block existence predicates and dependent setting constructor'),(H+'ConcreteSettingExists.lean',1,None,'Original GapHyp and full concrete endpoint')],
   'actual_instance':[(U+'InstExists.lean',1,None,'Full original-coordinate instanceOfRecord construction')],
   'ideal_trace':[('src/Formalism/HermitianLattices/StatementMass.lean',40,53,'Literal cmUnram residue-separation condition'),(P+'UnitaryGroupMassFormula/SesquilinearRowSplitting/AdjointActionReduction.lean',1,None,'Original trace-one and conjugation-invariant prescribed ideals'),(F+'UnramifiedDegreeOneOfNcardPlacesOver.lean',1,None,'Original complete-splitting unramified/local-degree consequence')],
   'primitive_vector':[(F+'ExistsIdealCoprimeConjMulEqSpanSingletonStatement.lean',1,None,'Exact original ideal-class auxiliary assertion'),(F+'ExistsPrimitiveVectorNormNegHyperbolicPairStatement.lean',1,None,'Full original primitive-vector hypothesis and conclusion'),(F+'ExistsPrimitiveVectorNormNegHyperbolicPair.lean',1,None,'Actual trace-one primitive-vector algebra')],
   'extra_isotropy':[(F+'ExistsIsotropicOrthHyp.lean',1,None,'Actual Forms0 norm-one, piU, negative-vector and orthogonal isotropic direction')],
   'integral_hyperbolic':[(D+'LatExistsOfSteps.lean',18,43,'Exact SatBasis/GenFrame auxiliary contracts'),(D+'LatExistsOfSteps.lean',135,389,'Exact projection, dual ideals and integral hyperbolic correction'),(D+'LatExistsOfSteps.lean',570,755,'All original lattice, local-generation and FixedHyp fields'),(F+'LatExistsOfForms0.lean',1,None,'Full original LatExists from Forms0 endpoint')],
   'character':[(P+'ScPsiExists.lean',1,None,'Exact finite additive character and prescribed infinity factor'),(P+'OrbitalBoundsConclusion/ScPsiExists.lean',1,None,'Original character producer')],
   'reference':[(P+'ScRefExists.lean',1,None,'Complete generic reference-frame contract and congruence predicates'),(P+'OrbitalBoundsConclusion/ScRefExists.lean',1,None,'Original reference producer'),(P+'UnitaryGroupMassFormula/LatticeReferenceFrame/TargetOfWframe.lean',1,None,'Original intermediate route simplified by split finite-adeles')],
   'transport':[(P+'ScXuExists.lean',1,None,'Complete generic transport contract including arbitrary original reference frame and OneOff'),(P+'OrbitalBoundsConclusion/ScXuExists.lean',1,None,'Original transport producer')],
   'level_bundle':[(H+'HidaSetting.lean',108,134,'Original K2cong, K2set and chi2f'),('src/Formalism/SharpRestriction/CuspSpanNormBounds/GlobAut.lean',213,259,'Full original IsAdmIdem and RowsAut fields'),(U+'BunExists.lean',1279,1464,'Actual eOf admissibility, degree/lambda casts and complete automorphic bundle')],
   'representation_measure':[('src/Formalism/LocalRingCardinality/Params.lean',6,69,'Even original k, half-integral u and integral interlacing v'),(P+'UpqRep.lean',201,231,'Exact rhoC, rhoN and lowK normalization'),(P+'UpqRep.lean',329,331,'Literal IsHCTypeU requires highest weight lowK(allPos,u)'),(H+'HidaSetting.lean',24,65,'Original S/N flag groups'),(H+'HidaSetting.lean',136,163,'Exact IsRepS/IsHaarOnSet/IsQuotMeasS/Hset/matW'),(P+'ScMuExists.lean',1,None,'Original subgroup/quotient measure producer contract'),(P+'OrbitalBoundsConclusion/ScMuExists.lean',1,None,'Original measure producer')],
   'whole_boundary':[(F+'ExistsGlobalSetting.lean',1,None,'Actual W and measured-field blocks, Siegel–Weil rescaling/ties, full setting/spectral endpoint'),(U+'SettingBlocks.lean',209,320,'Remaining measured block and complete dependent constructor'),(H+'RowsDef.lean',67,83,'Exact RowsFinDim now supplied by RFD8')]
  },
  'claim_groups':{1:['setting_contract','actual_instance'],2:['ideal_trace','integral_hyperbolic'],3:['primitive_vector'],4:['primitive_vector'],5:['extra_isotropy'],6:['integral_hyperbolic'],7:['integral_hyperbolic','ideal_trace'],8:['integral_hyperbolic','primitive_vector'],9:['setting_contract','integral_hyperbolic'],10:['character','setting_contract'],11:['reference','transport'],12:['reference','setting_contract'],13:['transport','setting_contract'],14:['level_bundle','reference'],15:['level_bundle','setting_contract'],16:['representation_measure','setting_contract'],17:['representation_measure','setting_contract'],18:['whole_boundary','setting_contract']},
  'deps':{1:['FV4'],2:[],3:[],4:['ASG3'],5:[],6:['ASG5'],7:['ASG2','ASG6'],8:['ASG2','ASG4','ASG6','ASG7'],9:['ASG2','ASG6','ASG7','ASG8'],10:[],11:[],12:['ASG1','ASG2','ASG9','ASG11'],13:['ASG8','ASG9','ASG11','ASG12'],14:[],15:['ASG1','ASG14','FV6','RQC2','RQC3','RQC4','RQC5','RQC6','DC6','DC11','DC12','DC14','DC15','RFD4'],16:['ASG9','DC1'],17:['ASG16'],18:['ASG1','ASG9','ASG10','ASG12','ASG13','ASG14','ASG15','ASG16','ASG17','RFD8']},
  'scopes':[
   'Every original D7; exact fields E/F, original frame coordinates, Gram matrix, self-dual lattice, real places/sign order and finite adelic topology.',
   'Original finite-unramified CM extension gives trace one, including characteristic2 residues; original complete splitting makes all prescribed different powers local units at both primes.',
   'Every nonzero original fractional ideal and N: an integral prime coprime to its conjugate and N, in the exact inverse ideal class. Published CFT/Chebotarev application explicitly matched.',
   'Full primitive negative vector of every positive integer norm in the actual unimodular hyperbolic plane; nonprincipal ideals retained.',
   'Actual Forms0(D,u0) produces the extra isotropic vector in the original space; no new isotropy assumption.',
   'Actual saturated isotropic submodule with the first s prescribed fractional ideals and a final determinant-class ideal.',
   'Exact integral dual hyperbolic frame, with trace-one triangular correction rather than integral division by2.',
   'Actual orthogonal lattice splitting and all original word-indexed primitive negative vectors on one fixed frame.',
   'Complete original UnitaryLatticeData and all FixedHyp fields, including local generators equal to1 at both selected primes and exact Lsub primitiveness.',
   'Full generic ScPsiExists.Target, with the actual trace sign and infinity factor; no extra factor of2.',
   'Local split-lattice description; literal InAt equivalence for g,m>=1, ZMod equivalence, and InMod residue-span equivalence for integral vectors and generators.',
   'Full generic ScRefExists.Target from its original premises, including all prime powers, arbitrary allowed ranks, k=0 and g=1.',
   'Full generic ScXuExists.Target for every given reference frame, exact rational hyperbolic fixing and OneOff support; then all original words.',
   'Full seven-field IsAdmIdem and integrability of actual eOf at the original two-prime level and arbitrary Haar normalization.',
   'Every AutomorphicBundle field under original GapHyp on the actual supplied blocks; DC decay supplies unweighted coefficient integrability without an added CoefWeightedLoc premise.',
   'Full actual RepresentationData with the exact highest weight lowK(allPos,u)=u-rhoC, integral and dominant by even k and original half-integral interlacing; orthonormal complements and all same-stabilizer tensor laws.',
   'Full original MuBlocks, including exact quotient integral against original infinity Haar; no global Siegel–Weil comparison asserted.',
   'One dependent sequence of A,L,P,Rf,Xu,Bu,Pi,Mu on the same D; retains original Forms0/gap and remaining W/measured/tie/count/common-family producers.'
  ],
  'foundations':[
   {'id':'ASG_ORIGINAL_D7','kind':'original_input_record','statement':'The exact D7 data, including its spaces, CM-unramified extension, different, original complete-splitting primes, words/norm congruences, form, lattice, signature and highest weights.'},
   {'id':'ASG_FORMS0','kind':'retained_original_endpoint_antecedent','statement':'Original Forms0(D,u0), used in ASG5 and the resulting lattice block. This chapter reconstructs latExists_of_forms0, not the independent Forms0 producer.'},
   {'id':'ASG_GAP','kind':'retained_original_endpoint_antecedent','statement':'Literal GapHyp(D), rank>=1801 and adjacent gaps>=16r^19, used only for the actual discrete-series bundle.'},
   {'id':'ASG_CLASS_FIELD_CHEBOTAREV','kind':'checked_published_foundation','url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf','locator':'Milne, Class Field Theory4.03, ChapterV section3 and Example3.9, ChapterVIII Theorem7.4','statement':'Hilbert class field Artin isomorphism and Chebotarev occurrence of any conjugacy class. ASG3 verifies the exact split inverse-ideal-class application in the original E.'},
   {'id':'ASG_DEDEKIND_HAAR_BACKGROUND','kind':'standard_mathematical_background','statement':'Projective modules/Steinitz normal form over Dedekind domains; local integral dual lattices; Gram–Schmidt; Haar and Weil quotient integration for second-countable locally compact groups and closed subgroups with matching modular characters. All actual representation, subgroup and normalization hypotheses are verified in the numbered text.'},
   {'id':'ASG_REMAINING_COMMON_SETTING','kind':'retained_original_producers_in_endpoint_consumer_only','statement':'Original normalized nonzero Bessel W, measured-field block and Siegel–Weil same-object rescaling/ties; Bessel uniqueness/local ties in the spectral endpoint; arithmetic counting and common-family thresholds. These are not claimed supplied by the eight constructed blocks.'}
  ],
  'external':{3:['ASG_CLASS_FIELD_CHEBOTAREV'],4:['ASG_DEDEKIND_HAAR_BACKGROUND'],5:['ASG_ORIGINAL_D7','ASG_FORMS0'],6:['ASG_ORIGINAL_D7','ASG_FORMS0','ASG_DEDEKIND_HAAR_BACKGROUND'],7:['ASG_ORIGINAL_D7','ASG_DEDEKIND_HAAR_BACKGROUND'],8:['ASG_ORIGINAL_D7','ASG_FORMS0','ASG_DEDEKIND_HAAR_BACKGROUND'],9:['ASG_ORIGINAL_D7','ASG_FORMS0','ASG_DEDEKIND_HAAR_BACKGROUND'],15:['ASG_ORIGINAL_D7','ASG_GAP','ASG_DEDEKIND_HAAR_BACKGROUND'],18:['ASG_ORIGINAL_D7','ASG_FORMS0','ASG_GAP','ASG_REMAINING_COMMON_SETTING']},
  'default_external':['ASG_ORIGINAL_D7','ASG_DEDEKIND_HAAR_BACKGROUND'],
  'completed':['Actual UnitaryGroupInstance on the original D','Full latExists_of_forms0, all original FixedHyp/word fields','Full generic ScPsiExists, ScRefExists and ScXuExists targets','Exact eOf admissibility and complete AutomorphicBundle under original GapHyp','Full RepresentationData and MuBlocks','One dependent same-D block sequence and exact remaining constructor boundary'],
  'not_claimed':['Independent Forms0 producer','Original Bessel W/nonvanishing/normalized decay','Measured-field block and full Siegel–Weil comparison/ties','Full common ConcreteSettingExists or spectral family','Actual CountIdempotentsClass','Any whole global leaf closure','Complete RH or GRH'],
  'endpoint':'ASG18'
 }
}

baseline=json.loads((ROOT/'history/version_0_46/provenance.json').read_text())
known={c['id']:c for c in baseline['claims']}
for name,cfg in DATA.items():
 here=ROOT/name
 raw=(here/'main.tex').read_bytes(); txt=raw.decode()
 groups={}; inventory={}; excerpts=[]
 for group,specs in cfg['groups'].items():
  records=[]
  for j,(path,start,end,desc) in enumerate(specs,1):
   data=(SRC/path).read_bytes()
   assert data==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+path])
   lines=data.splitlines(keepends=True);end=end or len(lines)
   assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
   part=b''.join(lines[start-1:end])
   rec={'id':f'{cfg["prefix"]}_{group}_{j:02}','path':path,'line_start':start,'line_end':end,'declaration':desc,'file_sha256':sha(data),'range_sha256':sha(part),'range_bytes':len(part),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'}
   records.append(rec);inventory[path]={'path':path,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),'verified_equal_to_pinned_git_blob':True}
   excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nRange SHA256 {sha(part)}\n{part.decode()}\n')
  groups[group]=records
 claims=[]
 for n in range(1,cfg['count']+1):
  cid=cfg['prefix']+str(n)
  match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert match,cid
  title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1)
  block=match.group().encode(); ext=cfg['external'].get(n,cfg['default_external'])
  claims.append({'id':cid,'title':title,'introduced_in':'0.47','classification':'A' if n in cfg['A'] else 'B','status':'complete human proof at the explicitly stated original scope','depends_on':cfg['deps'][n],'external_input_ids':ext,'published_input_ids':[x for x in ext if x in {'RFD_HARISH_CHANDRA','ASG_CLASS_FIELD_CHEBOTAREV'}],'scope_note':cfg['scopes'][n-1],'source_groups':cfg['claim_groups'][n],'sources':[s for g in cfg['claim_groups'][n] for s in groups[g]],'proof_location':{'file':name+'/main.tex','label':'claim:'+cid,'line_start':txt[:match.start()].count('\n')+1,'line_end':txt[:match.end()].count('\n'),'sha256':sha(block),'bytes':len(block)},'source_proof_is_not_human_proof':True})
 inherited=[]
 for cid in sorted({d for c in claims for d in c['depends_on'] if not d.startswith(cfg['prefix'])}):
  c=known[cid];loc=c['proof_location'];data=(ROOT/loc['file']).read_bytes();part=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);h=loc.get('sha256',loc.get('paragraph_sha256'))
  assert h in {sha(part),sha(part.rstrip(b'\r\n'))},(cid,'inherited proof hash')
  inherited.append({'id':cid,'file':loc['file'],'main_tex_sha256':sha(data),'block_sha256':sha(part),'recorded_baseline_hash':h,'line_start':loc['line_start'],'line_end':loc['line_end'],'kind':'numbered_human_proof_dependency','not_an_external_foundation':True,'introduced_in':c.get('introduced_in')})
 known.update({c['id']:c for c in claims})
 reviews=[{'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())} for p in sorted(here.glob('review_*.json'))]
 prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.47','date':'2026-11-23','component':name,'source_commit':PIN,'main_tex_sha256':sha(raw),'proof_file_sha256':sha(raw),'claims':claims,'source_groups':groups,'source_inventory':list(inventory.values()),'source_files':list(inventory),'retained_foundations':cfg['foundations'],'inherited_human_inputs':inherited,'independent_reviews':reviews,'builder':{'file':'../build_root_components_v0_47.py','sha256':sha(Path(__file__).read_bytes())},'validation':{'source_checkout_pin_verified':True,'all_source_bytes_compared_to_pinned_git_blobs':True,'claim_blocks':len(claims),'external_foundations_separate_from_claim_DAG':True,'inherited_human_proof_hashes_checked':True,'no_lean_replay':True}}
 contracts={'schema':'rh-root-producer-contracts/1','artifact_version':'0.47','component':name,'source_commit':PIN,'proof_file_sha256':sha(raw),'endpoint_claim':cfg['endpoint'],'completed_original_substatements':cfg['completed'],'not_claimed':cfg['not_claimed'],'proposed_whole_obligation_closures':[],'whole_obligation_closures':[],'no_lean_replay':True}
 for fn,obj in [('provenance.json',prov),('contracts.json',contracts),('classical_inputs.json',{'component':name,'artifact_version':'0.47','foundations':cfg['foundations']})]:
  (here/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 (here/'source_excerpt.txt').write_text('\n'.join(excerpts))
 (here/'README.txt').write_text(name+' — version0.47\n\n'+str(len(claims))+' numbered human proofs.\n\nCOMPLETED ORIGINAL SUBSTATEMENTS\n'+'\n'.join('- '+x for x in cfg['completed'])+'\n\nEXACT BOUNDARY\n'+'\n'.join('- '+x for x in cfg['not_claimed'])+'\n\nNo Lean build or kernel replay. Source bytes and inherited human proofs are hash-bound.\n')
 report=[name+' — mathematical scope and source report','Version0.47; 23 November2026','',
  'The complete human proofs are in main.tex. This report records their exact scope, retained foundations and independent review bindings.','',
  'PROVED CLAIMS']
 for c in claims:report += [c['id']+' ['+c['classification']+']: '+c['scope_note']]
 report+=['','RETAINED FOUNDATIONS AND ORIGINAL PREMISES']
 for f in cfg['foundations']:report += [f['id']+' ('+f['kind']+'): '+f['statement']]
 report+=['','COMPLETED ORIGINAL ENDPOINTS']+cfg['completed']+['','BOUNDARY']+cfg['not_claimed']
 report+=['','PROVENANCE',f'{len(inventory)} pinned source files; {sum(len(x) for x in groups.values())} exact source ranges; {len(inherited)} inherited human proof bindings.',
  'Source commit: '+PIN,'Proof SHA256: '+sha(raw),'','INDEPENDENT REVIEWS']
 report += [x['file']+' — SHA256 '+x['sha256'] for x in reviews]
 report += ['','The hash bindings record the exact inspected text. They are not a formal replay or a substitute for the mathematical arguments.']
 (here/'report.txt').write_text('\n'.join(report)+'\n')
 print(json.dumps({'component':name,'claims':len(claims),'A':len(cfg['A']),'proof_sha256':sha(raw),'source_files':len(inventory),'source_ranges':sum(len(x) for x in groups.values()),'inherited_inputs':len(inherited)}))
