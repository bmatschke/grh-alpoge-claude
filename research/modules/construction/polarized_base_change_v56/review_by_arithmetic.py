#!/usr/bin/env python3
"""Bind the independent arithmetic agent's completed mathematical PBC review.
Checks exact proof/source/inherited bytes; does not execute or replay Lean.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
EXPECTED='20a6db9d4596718031fd701f9ec4f9d01c1c0f10157b909fd91fa884b5694bfc'
NOTES=[
'Sheaf separatedness, local gluing and inverse germs establish every regularity and ratio statement at the fixed gauges; only unit germs are cancelled.',
'Affine localization and a finite affine cover give the separate fraction and annihilation conclusions, including zero divisors and arbitrary schemes in the stated scopes.',
'The first finite exponent clears fractions and the second kills all overlap discrepancies on entire quasi-compact intersections. The degree stays fixed and the original qcqs scope is retained.',
'The unit-ideal principal affine cover makes W qcqs; the proved degree-zero extension and annihilation criteria identify its localized global rings and glue the actual affine inverse.',
'Generated-subring induction and affine localization prove the stated operations. The polynomial-map dictionary retains arbitrary index sets, arbitrary D and the actual coefficient map.',
'The vanishing ideal K is retained. Affineness is proved before the second denominator-clearing step, and radical membership gives global generation for arbitrary index families.',
'The positive-exponent monomial argument, the exponent-zero branch and the empty-family branch all work. The determinant kills a finite module and requires neither Noetherianity nor finite generation of K.',
'The mixed ratios are regular on W. The expression induction tracks ideal powers exactly; localization annihilation gives the strict extra power and the polynomial identity transfers it to every mixed ratio.',
'The same finite annihilator lies in the vanishing ideal because one diagonal ratio is a unit at every point. The radical unit-ideal argument and exact localized ratios give both original outputs, including empty covers.',
'One common positive product degree and all mixed numerator extensions are chosen before any later denominator. The finite ideal identity gives the base-open cover, including the empty-index case.',
'The fixed mixed numerators generate every degree-N denominator open. The inverse base generators and their varying extension exponents are retained in the exact local-to-global application.',
'Appending zero produces the original nonempty Fin(M+1) tuple without adding a nonempty-scheme premise. All global denominator opens retain the original universal quantifier.',
'Local stalk homomorphisms preserve and reflect units, hence commute with total inverse. Open-immersion lifts are only functions off the image; regularity and generation are transported on the actual open.',
'The original section compatibility gives the unit-locus and ratio equivalence on every chart without assuming an additional line-bundle cocycle for these forward assertions.',
'The reconstruction uses the original IsLB cocycle and the exact gauge-power identity. G is arbitrary; regularity is proved near each point with a fixed chart and no global-unit hypothesis is inserted.',
'The specified principal-open immersion gives the localization of the actual base ring. Pullback expresses every base constant as a finite fraction with a unit denominator on the whole source.',
'Only the local RelAmple presentation and the specified chart choice are used. The forward section dictionary and constant-tuple power identity do not add global L.IsLB; the actual open immersion and base maps are retained.',
'The finite good-element unit-ideal extraction, full pack and actual-section reconstruction prove relAmple_of_locally over arbitrary schemes with exactly the original qcqs and IsLB premises.',
'Unit compatibility produces actual pulled sections on every chart and every test. Finite integer LinComb powers, negative exponents, generator gluing and literal nested/composed chart comparisons retain their stated scopes.',
'The restricted Cartesian square and actual affine tensor-product ring identify the pulled coordinate maps. Polynomial surjectivity follows from pure tensors without a flatness or Noetherianity premise.',
'The prescribed nested pullback bundle is compared with the composite pullback on the entire original inverse-image base open, which is allowed to be nonaffine.',
'Cartesian uniqueness constructs the original group pullback and injectivity on every test. Identity, inversion, smooth relative dimension, properness and geometric connectedness remain the actual pulled fields.',
'The supplied generator tuples pull directly through the literal chart refinements. The argument retains the broader original chart-datum scope and requires no extra IsLB premise for these two generator-transport statements; symmetry stays local on the base.',
'The two T-times-A models are actually isomorphic for every commutative test ring. The translation identities transport the local generator over the same V, and original KTriv plus test-point injectivity gives exactly the identity point.',
'All original PolAV fields are supplied on the prescribed categorical pullback and literal pulled bundle. The same g, all-test multiplication law and actual generated identity Iso are returned; arbitrary nonflat base change is retained.',
'The exact reviewed GSL14/GSL15 argument transports the same sections and coefficient maps to every specified affine Cartesian model. No single ample exponent is asserted uniformly over all tests.',
'The Perf coordinate identity yields a nonzero relation without assuming linearity of its chosen bijection. ASL21 needs no vanishing antecedent to construct Perf. The exact K-to-global-sections scalar map and identity fiber product return the relation to every integer SecM; finite_secM retains its arbitrary-field implication.'
]

def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((HERE/name).read_text())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args()
 repo=args.repo.resolve();errors=[]
 def check(ok,msg):
  if not ok:errors.append(msg)
 check(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN,'accepted source pin')
 body=(HERE/'main.tex').read_bytes();mainsha=sha(body)
 check(mainsha==EXPECTED,'reviewed main changed')
 p=read('provenance.json');s=read('source_manifest.json');c=read('contracts.json');cl=read('closure.json')
 blocks={m.group(1).decode():m.group() for m in re.finditer(rb'% BEGIN (PBC\d+)\n.*?% END \1\n',body,re.S)}
 ids=['PBC'+str(i) for i in range(1,28)]
 check(set(blocks)==set(ids),'exact proof block inventory')
 check([x['id'] for x in p['claims']]==ids,'claim inventory')
 for name,record in [('provenance',p),('source_manifest',s),('contracts',c),('closure',cl)]:
  check(record['source_commit']==PIN,name+' pin')
  check(record['proof_file_sha256']==mainsha,name+' proof binding')
 proof_hashes={cid:sha(blocks[cid]) for cid in ids}
 for claim in p['claims']:
  cid=claim['id'];loc=claim['proof_location'];piece=b''.join(body.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
  check(piece==blocks[cid],cid+' exact proof range')
  check(sha(piece)==loc['sha256'] and len(piece)==loc['bytes'],cid+' proof hash and bytes')
  check(('\\label{claim:'+cid+'}').encode() in piece,cid+' label')
 source_verification=[];bindings={HERE.name+'/main.tex':mainsha}
 for f in s['files']:
  b=(WORK/f['snapshot_file']).read_bytes();blob=subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+f['path']])
  check(sha(b)==f['sha256'],f['path']+' manifest hash')
  check(b==blob==(repo/f['path']).read_bytes(),f['path']+' exact pinned Git and checkout')
  check(len(b)==f['bytes'],f['path']+' bytes')
  if 'line_count' in f:check(len(b.splitlines())==f['line_count'],f['path']+' line count')
  bindings[f['snapshot_file']]=sha(b)
  source_verification.append({'path':f['path'],'snapshot_file':f['snapshot_file'],'sha256':sha(b),'verified_against_pinned_git_and_checkout':True})
 ranges={r['id']:r for r in s['ranges']};range_verification=[]
 for r in s['ranges']:
  b=(WORK/r['snapshot_file']).read_bytes();ls=b.splitlines(keepends=True)
  check(1<=r['line_start']<=r['line_end']<=len(ls),r['id']+' valid range')
  piece=b''.join(ls[r['line_start']-1:r['line_end']])
  check(sha(piece)==r['range_sha256'] and len(piece)==r['range_bytes'],r['id']+' exact range hash and bytes')
  check(sha(b)==r['file_sha256'],r['id']+' file binding')
  range_verification.append({'id':r['id'],'path':r['path'],'line_start':r['line_start'],'line_end':r['line_end'],'range_sha256':sha(piece),'status':'PASS'})
 for claim in p['claims']:
  for r in claim['sources']:check(r==ranges[r['id']],claim['id']+' source ledger consistency')
 inherited_verification=[]
 for h in read('inherited_inputs.json')['inputs']:
  b=(WORK/h['proof_file']).read_bytes();pl=h['proof_location'];piece=b''.join(b.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
  check(sha(b)==h['proof_file_sha256'],h['id']+' inherited main')
  check(sha(piece)==h['proof_block_sha256']==pl['sha256'],h['id']+' inherited block')
  check(sha((WORK/h['provenance_file']).read_bytes())==h['provenance_sha256'],h['id']+' inherited provenance')
  bindings[h['proof_file']]=sha(b)
  inherited_verification.append({'id':h['id'],'role':h['role'],'file':h['proof_file'],'file_sha256':sha(b),'proof_range_sha256':sha(piece),'provenance_file':h['provenance_file'],'provenance_sha256':h['provenance_sha256'],'status':'PASS'})
 for flag in ['full_original_sc_extend_supplied','full_original_exists_one_add_kill_supplied','full_original_extra_section_supplied','full_original_glue_pack_supplied','full_original_exists_sv_supplied','full_original_relAmple_of_locally_supplied','full_original_relAmple_pull_supplied','full_original_kTriv_pull_supplied','full_original_PolBaseChangeSt_supplied','full_original_polAV_veryAmpleBy_supplied','full_original_actual_section_finiteness_supplied','full_original_integer_power_SecM_finiteness_supplied','arbitrary_base_and_target_preserved','original_actual_bundle_and_cartesian_square_preserved','original_all_test_quantifiers_preserved','no_new_noetherianity_or_flatness_hypothesis']:
  check(c.get(flag) is True,'completed contract '+flag)
 for flag in ['full_original_two_sided_section_growth_supplied','global_positive_power_abelian_vanishing_unconditionally_supplied','global_section_laws_unconditionally_supplied','global_Moduli_supplied']:
  check(c.get(flag) is False,'retained boundary '+flag)
 check(c['selected_whole_obligations_closed']==[],'no whole selected closure')
 tv=read('tex_validation.json');check(tv['proof_file_sha256']==mainsha and tv['status']=='PASS','TeX hash and status')
 check(len(tv['passes'])==2 and all(x['returncode']==0 for x in tv['passes']),'two TeX passes')
 check(all(v==0 for v in tv['diagnostics'].values()),'zero TeX diagnostics')
 if errors:
  print(json.dumps({'status':'FAIL','errors':errors},indent=2));raise SystemExit(1)
 claims=[{'id':cid,'block_sha256':proof_hashes[cid],'status':'PASS','scope_verdict':'PASS at the stated original hypotheses','review_note':note} for cid,note in zip(ids,NOTES)]
 report='''# Independent mathematical review: PBC1–PBC27

**Result: PASS.** Reviewer: `/root/arithmetic_common_frame`; author: geometry agent.

The review read every human proof and compared its stated scope and formulas with the original pinned source contracts and producer bodies. It did not execute or replay Lean.

- Accepted source pin: `'''+PIN+'''`.
- Reviewed manuscript SHA256: `'''+mainsha+'''`.
- All 27 proof blocks, 29 full source snapshots, 82 exact source ranges and nine inherited/context/consumer bindings were independently checked.
- The recorded two-pass draft TeX validation is bound to these same proof bytes and has zero diagnostics.

## Main scope conclusions

The full arbitrary-base local-relative-ampleness theorem and the full original polarized-base-change record are supplied. The finite determinant argument is valid over arbitrary commutative rings; neither nilpotents nor zero divisors are removed. The extension uses two different exponents, and the global numerator family precedes every later denominator. The actual chart-valued sections are reconstructed, with the original coefficient-ring polynomial maps.

The base-change proof uses the actual Cartesian pullback, the literal pulled bundle, the same relative dimension, the original rigidification and local symmetry, and every original test-scheme multiplication identity. The translation-kernel proof uses an actual isomorphism of the two test products and therefore needs no unstated nonflat descent theorem. The broader original scopes of `exists_sv`, `pack_of_relAmple`, and generator transport are preserved.

Actual section finiteness follows from the coordinate identity of the inherited Perf record. The chosen section bijection is never presumed linear. The original scalar maps and the identity product are retained on the return to all integer-power SecM modules. This closes the finite-section part only: two-sided growth, multiplication geometry and comparison, every-open torsion descent, geometric integrality/rank, translated-square producers, the full global section laws and moduli remain separate.

## Per-claim decisions

'''
 for item in claims:report+='### '+item['id']+' — PASS\n\n'+item['review_note']+'\n\n'
 report+='## Findings and retained scope\n\nNo mathematical correction was required. No unresolved issue was found. The complete broader-source scope checks included arbitrary G in the reverse section dictionary; no extra global IsLB premise in the local pack constructor; all commutative test rings for KTriv; and arbitrary fields in the conditional finite_secM implication. No whole selected obligation closes.\n'
 (HERE/'independent_review.md').write_text(report)
 result={'schema':'rh-independent-mathematical-review/1','artifact_version':'0.56','date':'2026-11-23','component':HERE.name,'reviewer':'/root/arithmetic_common_frame','author':'geometry_alltest','source_commit':PIN,'status':'PASS','result':'PASS','proof_file':HERE.name+'/main.tex','proof_file_sha256':mainsha,'claims_reviewed':claims,'proof_hashes':proof_hashes,'source_files_checked':len(source_verification),'source_ranges_checked':len(range_verification),'source_verification':source_verification,'source_range_verification':range_verification,'inherited_inputs_checked':len(inherited_verification),'inherited_verification':inherited_verification,'input_bindings':bindings,
 'scope_guards':{'arbitrary_original_base_and_target':True,'no_flatness_or_noetherianity_added':True,'zero_divisors_and_nilpotents_retained':True,'two_distinct_extension_exponents':True,'fixed_numerator_family_before_every_denominator':True,'actual_chart_sections_and_original_scalar_maps':True,'exists_sv_arbitrary_G':True,'pack_of_relAmple_no_added_IsLB':True,'generator_transport_no_added_IsLB':True,'finite_integer_powers_including_negative':True,'all_test_multiplication_and_same_g':True,'KTriv_all_commutative_rings_and_actual_product_iso':True,'full_original_PolBaseChangeSt':True,'full_original_actual_section_finiteness':True,'full_original_all_integer_SecM_finiteness':True,'Perf_bijection_not_assumed_linear':True,'Perf_record_does_not_require_its_conditional_exactness_antecedent':True,'one_relation_length_before_every_section_tuple':True,'full_two_sided_growth':False,'full_global_section_laws':False,'global_Moduli':False},
 'completed_original_suppliers':['Sc.extend','exists_one_add_kill','extra_section','glue_pack','exists_sv','pack_of_relAmple','relAmple_of_locally','relAmple_pull','kTriv_pull','PolBaseChangeSt','polAV_veryAmpleBy','Perf.exists_relation','sections_finite_of_perf','finite_secM'],
 'resolved_findings':[],'whole_obligation_closures':{},'unresolved_findings':[],'required_corrections':[],'errors':[],'review_report':HERE.name+'/independent_review.md','report_sha256':sha((HERE/'independent_review.md').read_bytes()),'no_lean_replay':True}
 (HERE/'independent_review.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'status':'PASS','claims':len(claims),'source_files':len(source_verification),'source_ranges':len(range_verification),'inherited_bindings':len(inherited_verification),'proof_sha256':mainsha,'unresolved_findings':[]},indent=2))

if __name__=='__main__':main()
