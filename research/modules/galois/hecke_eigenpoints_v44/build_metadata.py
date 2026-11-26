#!/usr/bin/env python3
"""Bind the Hecke eigenpoint reconstruction to its original source and human inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
repo = parser.parse_args().repo.resolve()
sha = lambda x: hashlib.sha256(x).hexdigest()
B = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
H = B+'HeckeAlgebras/'
D = B+'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
specs = {
 'hset_axioms': (H+'CoefficientRepTrivialOnUnramified.lean',120,149,'literal Ax, dense inverse Frobenius and original dec'),
 'weight_point': (H+'CoefficientRepTrivialOnUnramified.lean',155,176,'MK, IsWt, finPart, Arith, Good and DenseWt'),
 'universal_output': (H+'CoefficientRepTrivialOnUnramified.lean',250,284,'TK, gen, genW, epsV, every IsUniv field and complete Out record'),
 'determinant_definition': (B+'WeilGroupCharacters/RepAlg.lean',44,117,'full natural multiplicative homogeneous law, map, ofRep, chi, lam and IsCont'),
 'dense_ext': (B+'AlgebraTools/DeterminantRepresentations/ExtDense.lean',1,None,'original full-law extDense; alternate characteristic-zero proof used here'),
 'core_cont': (D+'TCoreEig.lean',13,38,'eig_cont, coefficientwise determinant characteristic polynomial and Hecke polynomial'),
 'local_generation': (D+'TCoreEig.lean',39,83,'ordered telescoping, units/uniformizer generation and exact algebraic weight identities'),
 'local_character': (D+'TCoreEig.lean',85,136,'eig_loc with complete Weil and source Artin scope'),
 'core_det': (D+'TCoreEig.lean',137,146,'eig_det: full determinant from the dense original Frobenius set'),
 'core_ord': (D+'TCoreEig.lean',147,188,'eig_ord and eig_pt, all OrdChar and continuity fields'),
 'core_endpoint': (D+'TCoreEig.lean',189,None,'full core_eigen_of_weight_char_hecke_level'),
 'cyclotomic': (B+'PadicHodgeTheory/EpsArt.lean',28,None,'full epsArt at every ell-place and every IsLocalArtin'),
 'local_definitions': (H+'Distinct.lean',28,49,'literal PS, psEig, spherical operator and heckePol'),
 'period_char_definitions': (H+'Distinct.lean',55,118,'lowW, htW, DRat, PotCrys, OrdChar and complete OrdFlag'),
 'part_definition': (D+'UnitaryPointProperties.lean',29,53,'all PartAltAlt fields and exact AutomorphicHeckeSet'),
 'at_l': (B+'ModularityArgument/OrdinaryJacquetModules/AtLOf.lean',15,32,'full AtLT and its every-correspondence/AbW tests'),
 'use_at_l': (B+'ModularityArgument/OrdinaryJacquetModules/UseAtL.lean',18,None,'literal useAtL consumer'),
 'ps_polynomial': (D+'TPsRec.lean',18,None,'full source psRec type, of which only its distinct-unit forward case is used'),
 'ps_artin_match': (D+'IsSubquotientOfHasSupport.lean',171,None,'source psRec_alt Artin equality and cancellation of algNorm'),
 'abelian_weil': (B+'ModularityArgument/SemisimpleLevels/AbW.lean',14,17,'literal AbW commutator characteristic polynomial predicate'),
 'correspondence_existence': (D+'WinConv.lean',15,21,'original exRec_alt consumes retained RecTExists'),
 'out_endpoint': (D+'OrdCoreH.lean',20,None,'full core_hecke_of_automorphic_hecke_dense_weight and all Out fields'),
 'unitary_data': (D+'UnitaryHeckeData.lean',43,74,'UnitaryPointProperties, full UnitaryHeckeData and IsJ'),
 'actual_hset': (H+'IsTheta.lean',123,145,'the actual hset, with admitted=univ'),
 'unitary_out_caller': (D+'TJRing.lean',170,189,'original unitary same-Hecke-algebra use of Out.sep and Out.pt'),
 'literature': (D+'LitAut.lean',10,63,'original local, Artin and period literature records retained'),
 'local_artin': ('src/Development/AbelianVarietyTheory/PublishedTheorems/AutomorphicForms₂/HasExponentZeroIff.lean',145,160,'full original IsLocalArtin, especially universal global compatibility'),
 'idele_injectivity': ('src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/GlobalArtinLocalIdeleInjectiveStatement.lean',1,None,'exact local idele injectivity under original ChevalleyUnits input'),
}

cache = {}; sources = {}; source_files = {}
for key,(rel,lo,hi,decl) in specs.items():
    if rel not in cache:
        data=(repo/rel).read_bytes()
        pinned=subprocess.run(['git','show',PIN+':'+rel],cwd=repo,check=True,stdout=subprocess.PIPE).stdout
        assert data==pinned,rel
        cache[rel]=data
    data=cache[rel]; lines=data.splitlines(keepends=True)
    hi = len(lines) if hi is None else hi
    assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
    block=b''.join(lines[lo-1:hi])
    url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{rel}'
    source_files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
       'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'HEP_SRC_'+key.upper(),'path':rel,'declaration':decl,
       'line_start':lo,'line_end':hi,'file_sha256':sha(data),'range_sha256':sha(block),
       'range_bytes':len(block),'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,
       'url':url+f'#L{lo}-L{hi}'}

relations = {
 1:(['ASP2'],['core_cont','core_ord','universal_output'],[]),
 2:([],['determinant_definition','dense_ext'],[]),
 3:([1,2],['core_det','core_endpoint','hset_axioms','universal_output','part_definition'],[]),
 4:(['WRP1','CIP5'],['local_generation','cyclotomic','local_artin','idele_injectivity'],['HEP_ARTIN_NORMALIZATION','HEP_LOCAL_IDELE_INJECTIVITY']),
 5:([4],['local_generation','local_character','local_definitions'],[]),
 6:([1,5],['core_ord','universal_output','weight_point','period_char_definitions'],[]),
 7:([3,6],['core_endpoint'],[]),
 8:([7,'ASP13','AFS19'],['out_endpoint','part_definition'],[]),
 9:([4,8,'AFS17','GUA2'],['out_endpoint','at_l','use_at_l','ps_polynomial','ps_artin_match','abelian_weil','correspondence_existence'],['HEP_RECT_EXISTS','HEP_LOCAL_IDELE_INJECTIVITY']),
 10:([7,8,9,'OFL16'],['out_endpoint','period_char_definitions','hset_axioms'],[]),
 11:([10,'AFS20'],['out_endpoint','universal_output'],[]),
 12:([11,'FNL16','UPA17','AFS5'],['unitary_data','actual_hset','unitary_out_caller'],[]),
}
foundations = [
 {'id':'HEP_ARTIN_NORMALIZATION','name':'Original global/local reciprocity and cyclotomic norm normalization',
  'kind':'retained_original_class_field_foundation','introduced_here':False,
  'source_field':'LiteratureRankNHypothesis.aut.art; source epsArt',
  'scope':'Local-global compatibility and norm compatibility with the geometric degree convention, every original number field/ell-place and every source IsLocalArtin. The rational cyclotomic sign and uniformizer action are written in HEP4, extending the inherited CIP5 inertia calculation.'},
 {'id':'HEP_LOCAL_IDELE_INJECTIVITY','name':'Original Chevalley local idele injectivity',
  'kind':'retained_original_literature_clause','introduced_here':False,
  'source_field':'LiteratureRankNHypothesis.loc.chev and aut.art',
  'scope':'The source GlobalArtinLocalIdeleInjectiveStatement, used only to identify two maps satisfying the complete original IsLocalArtin; no CM/split restriction is added to generic TCoreEig/OrdCoreH.'},
 {'id':'HEP_RECT_EXISTS','name':'Original correspondence nonemptiness',
  'kind':'retained_original_correspondence_foundation','introduced_here':False,
  'source_field':'WinConv.exRec_alt and recTExists',
  'scope':'One permitted IsRecT for each original place/prolongation; all subsequent AtLT and parameter identities use that same map.'},
]

tex=(HERE/'main.tex').read_text(); main_hash=sha(tex.encode()); claims=[]
scopes={
 1:'Every original complete Noetherian local O-algebra and arbitrary algebra point; adically continuous maps into it become genuinely continuous after evaluation.',
 2:'Characteristic-zero field-valued full polynomial laws only. Every scalar E-algebra is included; no integral coefficient-ring n! inversion is asserted.',
 3:'Every original part and specified nonzero spherical eigenvector. No arithmetic or good guard is added.',
 4:'Every original number field, ell-place, Weil element and IsLocalArtin, including nonzero degree and ell=3; original algebraic embedding set.',
 5:'Ordered characters recovered individually from every unit preimage and every uniformizer preimage; no abelian-source assumption.',
 6:'All three literal OrdChar fields, including continuity and every OnArt decomposition-group equality.',
 7:'Entire literal original TCoreEig endpoint, arbitrary original IsCO A and T with supplied IsUniv and all source hypotheses.',
 8:'Every admitted arithmetic point, chosen before goodness; same original part predicate, full determinant, continuity and semisimplicity.',
 9:'Only the forward distinct-unit principal-series calculation required by Out; not the whole general psRec biconditional.',
 10:'Full Out.pt: every admitted arithmetic point; actual ordered flags and every-bridge PotCrys only under its exact Good guard.',
 11:'Entire original OrdCoreH Out: supplied univ, separation at every admitted dense weight, and full arithmetic pt; original initial dense weight retained.',
 12:'Original UnitaryHeckeData installation at every supplied level and original T,D,psi; all four point properties, same flags and separation at zero weight included.'
}
for number,(deps,groups,ext) in relations.items():
    cid=f'HEP{number}';m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',tex,re.M|re.S);assert m,cid
    block=m.group();title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',block,re.S).group(1)
    start=tex[:m.start()].count('\n')+1
    claims.append({'id':cid,'title':title,'introduced_in':'0.44','classification':'B',
       'status':'complete written proof at stated original scope','depends_on':[f'HEP{x}' if isinstance(x,int) else x for x in deps],
       'external_input_ids':ext,'scope':scopes[number],
       'proof_location':{'file':'hecke_eigenpoints_v44/main.tex','label':'claim:'+cid,'line_start':start,
          'line_end':start+block.count('\n')-1,'sha256':sha(block.encode()),'bytes':len(block.encode())},
       'source_groups':groups,'sources':[sources[x] for x in groups],
       'retained_hypotheses':['Original literature hypothesis, H.Ax, IsCO A/T, IsWt, commutativity and supplied IsUniv wherever quantified.'],
       'dependency_scope':'Only numbered written human claims occur in depends_on. Retained foundations are separately named; accepted formal correctness is not a substitute for these written arguments.'})

component_for={'ASP':'arithmetic_specialization_v42','WRP':'weight_representation_v42','CIP':'count_ii_producer',
 'AFS':'arithmetic_fibers_v43','GUA':'galois_assembly_v44','OFL':'ordinary_flags_v44','FNL':'finite_levels_v42','UPA':'automorphic_installation_v44'}
inherited=[]
for cid in sorted({d for ds,_,_ in relations.values() for d in ds if isinstance(d,str)}):
    component=component_for[re.match(r'[A-Z]+',cid).group()]
    p=ROOT/component/'main.tex';t=p.read_text();m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',t,re.M|re.S)
    if not m:m=re.search(r'\\paragraph\{'+cid+r':.*?(?=\n\\paragraph\{|\Z)',t,re.S)
    assert m,cid
    inherited.append({'claim':cid,'file':component+'/main.tex','file_sha256':sha(p.read_bytes()),
       'claim_sha256':sha(m.group().encode()),'line_start':t[:m.start()].count('\n')+1,
       'line_end':t[:m.end()].count('\n')+int(not m.group().endswith('\n')),
       'kind':'inherited_or_concurrent_written_human_proof','newly_modified':False,'scope':'Only the printed claim scope and its explicit retained foundations are used.'})

completed=[
 {'endpoint':'UpperTheory.V.Hi.core_eigen_of_weight_char_hecke_level','claim':'HEP7','scope':scopes[7]},
 {'endpoint':'UpperTheory.V.Hi.HSet.Out.pt','claim':'HEP10','scope':scopes[10]},
 {'endpoint':'UpperTheory.V.Z.Ord.core_hecke_of_automorphic_hecke_dense_weight','claim':'HEP11','scope':scopes[11]},
 {'endpoint':'Original UnitaryHeckeData Out installation used in TJRing/TJDense','claim':'HEP12','scope':scopes[12]},
]
remaining=[
 'The complete RingProps/TJRing consumer and its same-ideal determinant-law descent are separate.',
 'The later Hida point decomposition, end1/end2/twist and all-level automorphy consumers are separate.',
 'The general psRec biconditional is not claimed: the exact distinct-unit forward case needed by Out is proved.',
 'No new proofs of the retained class field theory, local Langlands, RecTExists or OFL period foundations are claimed.',
 'No whole RH/GRH or COUNT_II_SUPPORT obligation is closed by this packet alone.'
]
retention=[
 {'name':'GUA2 original local classification and correspondence laws','used_through':'GUA2 in HEP9','introduced_here':False,
  'scope':'Rank-one and unlinked singleton Langlands laws; the actual algebraic normalization cancels the fixed (n-1)/2 twist.'},
 {'name':'OFL16 original period foundations','used_through':'OFL16 in HEP10','introduced_here':False,
  'scope':'All period, character globalization and de Rham/potentially semistable inputs remain exactly as recorded in ordinary_flags_v44.'},
 {'name':'UPA17 actual automorphic-part supplier and retained BCS/GUA foundations','used_through':'UPA17 in HEP12','introduced_here':False,
  'scope':'Full original UnitPointProperties installed from one actual part; base-change and Galois-attachment foundations remain explicit.'}
]
reviews=[]
for p in list(HERE.glob('review_*.json'))+[ROOT/'reviews_v0_44/hecke_eigenpoints_v44_root_review.json']:
    if not p.exists():continue
    r=json.loads(p.read_text());bound=r.get('proof_file_sha256',r.get('proof_sha256',r.get('main_tex_sha256',r.get('main_sha256'))))
    if bound!=main_hash:continue
    expected={c['id']:c['proof_location']['sha256'] for c in claims}
    assert all(expected.get(k)==v for k,v in r.get('proof_hashes',{}).items()),p
    reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'record':r})
status='complete_at_stated_scope_independently_reviewed' if reviews else 'complete_written_proof_pending_independent_review'
contract={'schema':'rh-hecke-eigenpoint-contract/1','artifact_version':'0.44','component':'hecke_eigenpoints_v44',
 'source_commit':PIN,'proof_file_sha256':main_hash,'claim_count':12,'claims':'HEP1-HEP12',
 'completed_source_endpoints':completed,'original_data':'Original HSet H, IsCO A, IsWt theta, labels a, level K, actual TK, supplied IsUniv D/psi and fixed iota.',
 'coefficient_scope':'Arbitrary original complete Noetherian local A and T; no domain, flat point, reduced-fiber or continuity-of-iota assumption.',
 'determinant_scope':'Equality of full polynomial laws after every Qbar_ell scalar-algebra extension. Newton divisions occur only in characteristic zero after evaluation, never in O,A or T.',
 'point_scope':'A single r at every admitted arithmetic point has continuity, semisimplicity, P and the full determinant. Goodness is required exactly for flags and PotCrys.',
 'local_normalization':'eps(s)=q^deg(s)*algPow(1)(art(s)); j+1 Hecke indices; htW=lowW+i; original source uniformizers and art map.',
 'quantifiers_preserved':['all original ranks','all original odd primes including 3','all levels K','every admitted arithmetic point','every admitted dense weight','every original period bridge','every IsRecT map in the original AtLT predicate','all local character labels in order'],
 'actual_unitary_installation':'HEP12 consumes UPA17 and FNL16, giving every original form/type/cusp/aut field on the same Hecke T,D,psi.',
 'inherited_foundation_retention':retention,'classical_and_foundational_inputs':foundations,'not_supplied':remaining}
provenance={'schema':'rh-human-component-provenance/1','artifact_version':'0.44','date':'2026-11-23',
 'component':'hecke_eigenpoints_v44','source_commit':PIN,'main_tex_sha256':main_hash,'proof_file_sha256':main_hash,'status':status,
 'claims':claims,'source_groups':sources,'source_files':list(source_files.values()),'inherited_human_inputs':inherited,
 'classical_and_foundational_inputs':foundations,'inherited_foundation_retention':retention,'independent_reviews':reviews,
 'dependency_convention':'depends_on uses numbered human claims only. External foundation labels appear separately, never as fake DAG nodes.',
 'source_proof_is_not_human_proof':True,'root_ledger_modified':False,'frozen_v43_modified':False}
closure={'schema':'rh-human-component-closure/1','artifact_version':'0.44','component':'hecke_eigenpoints_v44',
 'proof_file_sha256':main_hash,'status':status,'completed_source_endpoints':completed,'whole_obligations_closed':[],
 'remaining':remaining,'foundation_retention_explicit':True,'full_laws_after_every_scalar_extension':True,
 'same_Hecke_algebra_and_characters':True,'arithmetic_pt_before_good_guard':True,'prime_3_retained':True,
 'independent_reviews':reviews,'validation':'Written mathematics and exact source endpoint comparison; two-pass draft TeX; no Lean replay or visual PDF certification.'}
manifest={'schema':'rh-source-manifest/1','artifact_version':'0.44','source_commit':PIN,'files':list(source_files.values()),
 'ranges':list(sources.values()),'file_count':len(source_files),'range_count':len(sources),'all_files_equal_pinned_git_blobs':True}
for name,value in [('provenance.json',provenance),('contract.json',contract),('closure.json',closure),('source_manifest.json',manifest)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
report=[
 'HECKE EIGENPOINTS AND THE FULL ORIGINAL OUT — v0.44',
 'Source pin: '+PIN,'Proof SHA256: '+main_hash,
 f'Written claims:12. Pinned source files:{len(source_files)}. Exact source ranges:{len(sources)}.',
 'Status: '+status,'',
 'Complete endpoints:',
 '  HEP7 full TCoreEig, including full evaluated determinant law and every original OrdChar.',
 '  HEP10 full Out.pt at every admitted arithmetic point; Good is retained only on flags/PotCrys.',
 '  HEP11 complete OrdCoreH Out with every univ, sep and pt field.',
 '  HEP12 original UnitaryHeckeData installation on the same T,D,psi and every supplied level.',
 '',
 'Substantive arguments:',
 '  Uniform maximal-ideal norm decay gives pointwise continuity.',
 '  Dense inverse-Frobenius polynomials and dual-number/Newton algebra prove full polynomial-law equality.',
 '  Positive cyclotomic local norms are extended to all Weil degrees, with the source Artin map.',
 '  Ordered partial-product cancellation and units/uniformizer generation recover each individual local character.',
 '  One part realizes every arithmetic point; good fibers give exact principal-series and DRat data.',
 '  OFL16 supplies actual flags and every-bridge potential crystallinity at the original evaluated characters.',
 '',
 'No domain, flat point, continuity-of-iota or prime-greater-than-rank hypothesis is added.',
 'All integer divisions occur after evaluation in Qbar_ell, preserving the integral prime-3 setting.',
 'The complete polynomial law, not only its group-element characteristic polynomials, is identified.',
 '',
 'Remaining outside this packet:']+['  '+x for x in remaining]+[
 '',
 'Rebuild with build_metadata.py --repo <exact source checkout>. Every cited source file is',
 'checked against the pinned git blob; each source range and numbered proof block is SHA256-bound.',
 'Standalone two-pass draft TeX is reproducible using validate_tex.py --format <pdflatex.fmt>.',
 'No common ledger, historical proof file, or formal source has been modified.'
]
(HERE/'report.txt').write_text('\n'.join(report)+'\n')
print(json.dumps({'component':'hecke_eigenpoints_v44','claims':len(claims),'files':len(source_files),
 'ranges':len(sources),'proof_sha256':main_hash,'status':status}))
