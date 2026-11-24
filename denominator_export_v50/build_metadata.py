#!/usr/bin/env python3
"""Bind the denominator proof and its exact entry/exit contracts to the source pin."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMPONENT = HERE.name
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
SNAP = ROOT / 'source_snapshot_v0_50' / 'denominator'
AV = 'src/Development/AbelianVarietyTheory/'
LC = 'src/Formalism/SharpRestriction/LevelLetterCocycles/'
CY = 'src/Development/AutomorphicArithmetic/CyclotomicBounds/'
SOURCE = {
 'conclusion': (AV+'Definitions/NonGaloisDescent/BoundAtTwoThreeFamily.lean', 17, None, 'Bd, all Star fields, Small, actual tab, Concl and ConclF'),
 'table': (AV+'Proofs/InertiaEigenvalues/AdmissibleTableOfLocalBounds.lean', 1, None, 'All original AdmT fields from Concl on the actual patched table'),
 'size_five': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesSizeConditionFive.lean', 1, None, 'Patched error-bound admissibility'),
 'size_six': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesSizeConditionSix.lean', 1, None, 'Actual cyclotomic row and generator epsilon bound'),
 'vanishing': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesVanishingExcluded.lean', 1, None, 'Large-prime table vanishing'),
 'two_three': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesConditionTwoThree.lean', 1, None, 'Prime-three equal shares and original small-prime bound'),
 'ramified': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesRamifiedTypePrimes.lean', 1, None, 'Ramified and generator-prime fields'),
 'rows': (AV+'Proofs/InertiaEigenvalues/LocalBoundTableAllPrimesRowsAndBand.lean', 1, None, 'All four original row-length bounds and exact band'),
 'admission': (AV+'Proofs/InertiaEigenvalues/AdmittedStatementsOfLocalBoundsConclusion.lean', 1, None, 'Full original ConclF to AdmF implication'),
 'link': (AV+'Proofs/InertiaEigenvalues/LinkNAlongFamilyOfLocalBounds.lean', 1, None, 'Original common-family LinkN consumer'),
 'twisted': ('src/Development/AutomorphicArithmetic/ResidueCharacters/TwistedPlaces.lean', 20, 243, 'Actual Tab, etaSum, all seventeen AdmT fields and original guards'),
 'mean': ('src/Development/AutomorphicArithmetic/ResidueCharacters/TwistedPlaces.lean', 245, 327, 'Actual normalized coefficient-place weights and admitted'),
 'weights': (LC+'MemPrimesOverOfMem.lean', 16, 220, 'Actual host degree, coefficient-place weights, finite grouping and scalar row rank bound'),
 'scalar': (LC+'MemPrimesOverOfMem.lean', 238, 264, 'Exact bandI, flatB, rowBr, lenB, bbB, lamB'),
 'scalar_proof': (LC+'MemPrimesOverOfMem.lean', 368, 649, 'Actual scalar majorant, lamG and weighted etaSum bound'),
 'dyadic': (LC+'MemPrimesOverOfMem.lean', 659, 708, 'Original small-order dyadic congruence and modulus lower bound'),
 'scales': (LC+'NEqRZeroMulXPow.lean', 1, 412, 'Original rank, weight, Den, lStar and lA scales'),
 'low_order': (LC+'NEqRZeroMulXPow.lean', 630, 873, 'Original R0 and small-order inert prime sum'),
 'small_sums': (LC+'NEqRZeroMulXPow.lean', 888, None, 'Source small-prime length/band sums; replaced by DNE8-DNE11 uniform estimates'),
 'exceptional_sums': (LC+'ExportBoundOfAdmissible.lean', 550, 874, 'Exceptional, generator, small-prime and ramified sums plus global constants'),
 'point_export': (LC+'ExportBoundOfAdmissible.lean', 880, 1055, 'Original denominator point bound and export_bound_of_admissible'),
 'uniform_export': (LC+'ExportBoundOfAdmissible.lean', 1061, None, 'Full original uniform export and the constant 2000 (abs Ca + 1)^3'),
 'eta_identity': (LC+'ThetaScalarFamilyOfEigenvalue.lean', 1, 57, 'Definitional original etaSum identity and LinkN family conversion'),
 'family_contract': (LC+'StatementFamilies/ExportFamilies.lean', 1, None, 'AdmFC, AdmF, FamilyThinScalesBound, UniformExportStatement'),
 'link_contract': ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean', 1, 61, 'Original LinkN_at and LinkN quantifiers'),
 'params': ('src/Formalism/LocalRingCardinality/DataParams.lean', 28, None, 'Original ParameterChoice, numeric and band/scale constraints'),
 'size': ('src/Formalism/LocalRingCardinality/DataParams₂.lean', 1, None, 'Scale, SizeData2, eta and nonnegative Nc'),
 'host': ('src/Formalism/LocalRingCardinality/DataHost.lean', 1, 180, 'Same original host, QS, primes, dyadic and rank constraints'),
 'cyclo': (CY+'RootsOfUnity/HostApprox.lean', 1, None, 'Actual host cyclotomic embedding and finite-precision exponent approximation'),
 'nu': (CY+'ClassNumberBounds/CyclotomicTotient/NuInf.lean', 1, None, 'nuOf and minimum valuation definitions'),
 'sharp_nu': (CY+'CyclotomicOrders/NuHost.lean', 1, None, 'Original sharper nuBudget; weaker intermediate budget here preserves full exit'),
 'hub': (LC+'JointConditionsZpowers/CommutingEndomorphismCondition.lean', 1, None, 'Original KillAt, RangeAD, supZ, lenR, HubData and StarAD'),
}

CLAIMS = [
 ('DNE1', [], ['weights','mean','twisted','link_contract'], 'Exact coefficient-place weights, host degree, unchanged dZ0, including zero rows.'),
 ('DNE2', [], ['cyclo','nu','sharp_nu','host','params'], 'Elementary sufficient cyclotomic budget log M + log(tr); sharper source budget is not asserted.'),
 ('DNE3', [], ['conclusion','hub','table','two_three'], 'Literal patched table on the same X and host, including the prime-three equal shares.'),
 ('DNE4', ['DNE3'], ['conclusion','table','size_five','size_six','vanishing','two_three','ramified','rows','twisted'], 'All seventeen AdmT fields; also the full starF_of constructor including 2 and 3.'),
 ('DNE5', ['DNE1','DNE2'], ['weights','scalar','scalar_proof','twisted'], 'Actual finite row sum to scalar majorant and nonnegative original vvTerm series.'),
 ('DNE6', [], ['scales','params','size','host'], 'Uniform eventual exponential-scale comparisons before every family/member/index choice.'),
 ('DNE7', ['DNE6','LFS2'], ['dyadic','low_order','params','host'], 'All finite small-order inert prime sets bounded by two dyadic progressions; no prime distribution hypothesis.'),
 ('DNE8', ['DNE6'], ['small_sums','scalar','twisted'], 'Common error and split/eP costs below p_star, with both occurrences of C retained.'),
 ('DNE9', ['DNE6'], ['small_sums','scalar'], 'Large-order inert costs below A, using the actual jA ceiling and uniform b_prime decay.'),
 ('DNE10', ['DNE6','DNE7'], ['small_sums','scalar'], 'All remaining inert H/p^2 costs, including small-order primes.'),
 ('DNE11', ['DNE6'], ['small_sums','scalar','rows'], 'Actual band implication and full flat sum; uniform band cutoff from scale comparison.'),
 ('DNE12', ['DNE6'], ['exceptional_sums','conclusion','twisted','params','host'], 'Large exceptional, generator, small and ramified primes all included.'),
 ('DNE13', ['DNE5','DNE8','DNE9','DNE10','DNE11','DNE12'], ['point_export','link_contract','size'], 'Full original LinkN_at inequality under an admissible table, with source constant and original summability guard.'),
 ('DNE14', ['DNE3','DNE4','DNE6','DNE13'], ['uniform_export','eta_identity','family_contract','link_contract','admission','link'], 'Full original UniformExportStatement and ConclF -> AdmF -> LinkN; table only selected under ShaFinOdd.'),
]

def sha(data): return hashlib.sha256(data).hexdigest()
def dump(name, value): (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
files, sources = {}, {}
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==PIN
for key,(path,a,b,decl) in SOURCE.items():
    data=(repo/path).read_bytes()
    assert data==subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]),path
    lines=data.splitlines(keepends=True)
    b=len(lines) if b is None else b
    assert 1<=a<=b<=len(lines),(key,a,b,len(lines))
    piece=b''.join(lines[a-1:b])
    target=SNAP/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    rec={'path':path,'snapshot_file':str(target.relative_to(ROOT)),'sha256':sha(data),
      'file_sha256':sha(data),'bytes':len(data),'source_commit':PIN,
      'verified_equal_to_pinned_git_blob':True,'url':url}
    files[path]=rec
    sources[key]={**rec,'id':'DNE_SRC_'+key.upper(),'declaration':decl,
      'line_start':a,'line_end':b,'range_sha256':sha(piece),'range_bytes':len(piece),
      'url':url+f'#L{a}-L{b}'}

proof=(HERE/'main.tex').read_bytes()
text=proof.decode()
claims=[]
for cid,deps,groups,scope in CLAIMS:
    a=text.index('% BEGIN '+cid+'\n')
    b=text.index('% END '+cid+'\n',a)+len('% END '+cid+'\n')
    block=text[a:b].encode()
    title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',text[a:b]).group(1)
    claims.append({'id':cid,'title':title,'introduced_in':'0.50','classification':'B',
      'depends_on':deps,'sources':[sources[g] for g in groups],'source_groups':groups,
      'scope_note':scope,'status':'written_pending_independent_review',
      'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,
        'line_start':text.count('\n',0,a)+1,'line_end':text.count('\n',0,b),
        'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.50','component':COMPONENT,'source_commit':PIN,
  'proof_file_sha256':sha(proof),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
  'claims':claims,'main_tex_sha256':sha(proof)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
  'files':list(files.values()),'ranges':list(sources.values()),
  'file_count':len(files),'range_count':len(sources)})

old=json.loads((ROOT/'provenance.json').read_text())
inherited=next(c for c in old['claims'] if c['id']=='LFS2')
pl=inherited['proof_location']
raw=(ROOT/pl['file']).read_bytes()
block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
assert sha(block) in {pl['sha256'],pl.get('range_sha256')}
dump('inherited_inputs.json',{'artifact_version':'0.50','inputs':[{'claim':'LFS2',
  'use':'Elementary dyadic residue calculation only; all new uniform estimates proved here.',
  'proof_location':pl,'verified_range_sha256':sha(block)}]})
foundations=[
 {'id':'DNE_ORIGINAL_DATA','kind':'original_supplied_data','statement':'The same D7, SizeData2, ParameterChoice prime and host data. Concl/ConclF is an original entry premise when constructing the admissible table; its arithmetic supplier is not asserted.'},
 {'id':'DNE_FIELD_FOUNDATIONS','kind':'standard_number_field_foundations','statement':'Degree formula for primes, cyclotomic automorphisms and extension of an automorphism to an algebraic closure. The finite-precision CRT/LTE argument actually used is proved in DNE2.'},
 {'id':'DNE_ELEMENTARY_ANALYSIS','kind':'standard_real_analysis','statement':'Integral comparison for decreasing positive functions, elementary exponential-versus-power limits, monotonicity of finite sums and a summable nonnegative series. All problem-specific comparisons are written in DNE6-DNE13.'},
]
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':foundations})
endpoints=[
 {'endpoint':'GlobalTheory.NLink.starF_of','claim':'DNE4','status':'whole_original_two_three_constructor_written'},
 {'endpoint':'GlobalTheory.NLink.admissible_table_of_conclusion','claim':'DNE3','status':'whole_original_fourth_admissibility_field_written'},
 {'endpoint':'GlobalTheory.NLink.admittedStatements_of_localBoundsConclusion','claim':'DNE4','status':'whole_original_Concl_to_actual_AdmT_written'},
 {'endpoint':'Formalism.MainNotions.TwistedPlaces.UniformExportStatement','claim':'DNE14','status':'whole_original_uniform_statement_written','qualification':'Original numerical pointwise Large predicate replaced by a uniformly eventual cutoff; no changed exit constant or quantifiers.'},
 {'endpoint':'GlobalTheory.LinkFam.main','claim':'DNE14','status':'whole_original_ConclF_to_LinkN_written'},
]
remaining=[
 'The actual common ConclF producer remains, including NormChoiceFacts, actual compatible Galois/killing points, local row bounds, and original small-prime/type-prime suppliers on one selected family.',
 'GLOBAL_DENOMINATOR is not closed merely by this completed consumer. Original ShaFinOdd, vvTerm summability, coefficient field, host and row rank have not been strengthened or omitted.',
 'The source sharper cyclotomic budget and its exact numerical pointwise Large cutoff are not claimed; their full original uniform LinkN endpoint is obtained by the proved simplification.',
 'Common-family existence and all other selected open producer obligations remain governed by the current whole-contract register.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
  'entry_premises':['original D7/SizeData2/ParameterChoice','original Concl or ConclF when building table','original admissible table for scalar export'],
  'completed_source_endpoints':endpoints,'extra_hypotheses_introduced':[],
  'exact_output_constant':'2000 * (abs Ca + 1)^3',
  'choice_order':['Fix epsilon and Ca.','Choose output constant independent of family.','Choose uniform numerical cutoff depending only on epsilon and Ca.','Given original family, maximize with its initial and AdmFC cutoffs.','At each later member use ShaFinOdd to obtain its table, then quantify over all original lifts and retain summability antecedent.'],
  'zero_row_cases_retained':True,'same_original_coefficient_field_and_host':True,
  'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
  'completed_source_endpoints':endpoints,'whole_obligations_closed':[],
  'proposed_global_frontier_leaf_closures':[],
  'full_original_ConclF_AdmF_LinkN_consumer_supplied':True,
  'full_GLOBAL_DENOMINATOR_supplier_supplied':False,
  'independent_reviews':[],'remaining':remaining})
dump('published_inputs.json',[])
(HERE/'report.txt').write_text(
 'ACTUAL DENOMINATOR TABLE AND UNIFORM EXPORT — v0.50\n'
 f'Source pin: {PIN}\nClaims: 14 (DNE1–DNE14).\nProof SHA256: {sha(proof)}\n\n'
 'The whole original ConclF -> AdmF -> LinkN consumer is reconstructed.\n'
 'DNE1–DNE5 preserve actual place weights, row ranks, tables, the prime-three\n'
 'equal-share branch and every admissibility field. A simpler cyclotomic\n'
 'budget log M + log(tr) is proved directly by CRT and valuations.\n\n'
 'DNE6–DNE12 bound all prime classes uniformly. Exponential-scale comparison\n'
 'replaces long numerical cutoff calculations. Low dyadic order means two\n'
 'sparse residue progressions; the original band implication bounds its\n'
 'support. Exceptional, generator, small and ramified primes are included.\n\n'
 'DNE13–DNE14 prove the exact original denominator inequality with output\n'
 'constant 2000(|Ca|+1)^3 before the family. ShaFinOdd supplies its actual\n'
 'table; the original vvTerm summability guard stays at the infinite sum.\n'
 'The upstream common ConclF supplier remains. GLOBAL_DENOMINATOR is open.\n'
 'Independent mathematical review pending. No Lean replay or PDF claimed.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'ranges':len(sources),'proof_sha256':sha(proof)},indent=2))
