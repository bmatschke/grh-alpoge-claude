#!/usr/bin/env python3
"""Bind the Wach-inclusion proofs to the original producers and consumers."""
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
REPO = parser.parse_args().repo.resolve()
AV = 'src/Development/AbelianVarietyTheory/'
I = AV + 'Proofs/InertiaEigenvalues/'
N = AV + 'Definitions/NonGaloisDescent/'
D = 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean'
SOURCE = {
    'integers': (I+'IntegersCompleteDVR.lean', 'integers_completeDVR: all original clauses', 1, None),
    'witt': (I+'TiltWittEqZeroOfPrimeMulEqZero.lean', 'Witt coordinate injection, saturation and finite coefficient tensor properties; no claim of the final stronger mu-adic clause', 1, None),
    'local': (I+'NilpotentOfNotIsUnit.lean', 'perfection_isUnit and witt_isUnit; only the local/Jacobson consequence is needed here', 1, None),
    'letters': (D, 'Literal LetA, letE, letpi and letphi', 52, 67),
    'tilt_data': (D, 'Literal OCb, Ainf, Cb, inclW, LocAinf and epsilon roots', 761, 836),
    'tensor_data': (D, 'Literal RW, RA, inclR and Frobenius tensor maps', 1097, 1123),
    'records': (N+'ExistsOfLayers.lean', 'Full supplied WSer and WIo records and actual concrete abbreviations', 1, None),
    'embedding': (I+'WachInclusionInjectiveSaturatedInter.lean', 'Full original abstract and actual four-clause coefficient embedding theorem', 1, None),
    'endpoint': (I+'WachInclusionInjectiveSaturatedInterStatement.lean', 'Literal exported four-clause wachInclusion_injective_saturated_inter', 1, None),
    'closed': (I+'PadicClosed.lean', 'sat_pow, sat_range and full generic padic_closed; later near_closed remains a separate supplier', 1, 79),
    'fixed_p': (I+'GaloisFixedSubringTensorWittSaturatedComplete.lean', 'Full original fixSub_ladic for every set of Galois elements', 1, None),
    'p_sums': (I+'GoodOfComplete.lean', 'good_of_complete, finite tensor sums and original ladic_RW', 1, None),
    'fixed_lift': (I+'ExistsGaloisFixedLiftOfFixedModPrime.lean', 'Full original fixed-modulo-prime lifting statement', 1, None),
    'tilt_complete': (I+'TiltSeparatedCompleteEpsilonRootSubOne.lean', 'Full original tilt separated_complete and actual cyclotomic application', 1, None),
    'coordinates': (I+'CoeffZeroEqZeroIff.lean', 'Literal tensor-coordinate, zero-coordinate and NearPi definitions and criteria', 1, None),
    'near': (I+'NearPiSepComplete.lean', 'Full original nearPi_sep_complete at every allowed s and finite coefficient field', 1, None),
    'fixed_near': (I+'GaloisFixedTensorWittCompletePiAdicModEll.lean', 'Full original fixSub_nearPi_complete including arbitrary H and fixed actual pi', 1, None),
    'consumer': (I+'WachLatticesExistAllLayersOfBhattScholze.lean', 'Original all-layer consumer uses the first two inclusion clauses; full generic construction already WLD25', 1, None),
    'matrix_boundary': (I+'FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean', 'Actual next matrix-descent consumer and its remaining source producers; not a claimed matrix theorem here', 1, None),
    'prism_boundary': (I+'ExistsWachPrismOverIntegers.lean', 'Retained actual Wach-prism supplier; not proved in this packet', 1, None),
    'wach_scope': (N+'ConvZero.lean', 'Exact WachEx and separately retained FaithH and EtBasis scopes', 1, None),
    'BS': (AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeCrystallineLattices.lean', 'Original crystalline-realization premise retained in the WLD26 return', 1, None),
}
CLAIMS = [
    ('WIS1', [], ['integers'], 'Full actual finite local-field integral coefficient properties, with a trace-lattice finiteness proof.'),
    ('WIS2', [], ['witt','local'], 'Perfect Witt coordinate completeness, torsion-freeness, unit criterion, injection and saturation.'),
    ('WIS3', ['WIS2'], ['local','tilt_data','embedding'], 'Actual local tilt and Ainf rings; every original cyclotomic mu_s is in the maximal ideal.'),
    ('WIS4', [], ['witt','coordinates'], 'Exact finite tensor coordinates, maps and principal-power membership, without flatness of an unspecified extension.'),
    ('WIS5', ['WIS1','WIS2','WIS4'], ['witt','tensor_data','tilt_data'], 'Actual tensor inclusions, p-completeness and p-saturation; does not assert the stronger mu-adic completeness clause.'),
    ('WIS6', ['WIS3','WIS4','WIS5'], ['embedding','witt','records'], 'Finite determinant proof of the exact Jacobson input in place of the stronger source completeness supplier.'),
    ('WIS7', [], ['embedding','letters'], 'Full uniformizer series/letter dichotomy with a unit of the entire component ring.'),
    ('WIS8', ['WIS1'], ['embedding','letters'], 'Exact p-adic Cauchy limit property of the given integral series ring.'),
    ('WIS9', [], ['embedding','letters','records'], 'Nonvanishing of every component from the original cyclic Frobenius maps; no Frobenius inverse required.'),
    ('WIS10', [], ['embedding'], 'Abstract radical/regularity/density consequences at the fully printed original premise scope.'),
    ('WIS11', ['WIS10'], ['embedding'], 'Reflection of one uniformizer factor through the finite component dichotomy.'),
    ('WIS12', ['WIS11','WIS10'], ['embedding'], 'Reflection of every uniformizer power by cancellation in the target, not assumed injection.'),
    ('WIS13', ['WIS12'], ['embedding','closed'], 'Injection and every p-power saturation with the actual divided target element.'),
    ('WIS14', ['WIS10'], ['embedding'], 'Full reflection of units, using a maximal ideal in the actual source ring.'),
    ('WIS15', ['WIS10'], ['embedding'], 'One integral uniformizer digit, preserving the integral-image property for iteration.'),
    ('WIS16', ['WIS15'], ['embedding'], 'Full integral intersection by reflected coefficient congruences and actual source completeness.'),
    ('WIS17', ['WIS13','WIS14','WIS16'], ['embedding'], 'Full original abstract four-clause theorem with precisely the original printed premises.'),
    ('WIS18', ['WIS1','WIS5','WIS6','WIS7','WIS8','WIS9','WIS17'], ['embedding','endpoint','records','tensor_data'], 'Full actual exported four-clause Wach embedding at every original Good/Gamma/R/I/IoW tuple.'),
    ('WIS19', ['WIS5','WIS18'], ['closed','records'], 'Full generic padic_closed and actual coefficient-image closedness, with quotient injection.'),
    ('WIS20', ['WIS5'], ['fixed_p','p_sums','tensor_data'], 'Full original fixed-subring p-adic supplier for arbitrary sets H, including Frobenius and all sums.'),
    ('WIS21', ['WIS2','WIS4'], ['fixed_lift','coordinates','tensor_data'], 'Full original actual fixed-modulo-prime lift by the unchanged integral coordinate basis.'),
    ('WIS22', [], ['tilt_complete','tilt_data'], 'Full original actual tilt separation and complete summation, all s including zero, through explicit coordinate nilpotence.'),
    ('WIS23', ['WIS2','WIS4'], ['coordinates','near','tensor_data'], 'Exact original p-divisibility and NearPi coordinate criteria on the actual tensor maps.'),
    ('WIS24', ['WIS22','WIS23'], ['near'], 'Full original NearPi separation and complete summation with every shift k.'),
    ('WIS25', ['WIS21','WIS24'], ['fixed_near','tensor_data'], 'Full original fixed-subring NearPi complete summation for arbitrary H fixing the actual pi.'),
    ('WIS26', ['WIS18','WLD26'], ['consumer','wach_scope','BS','prism_boundary','matrix_boundary'], 'Conditional full WachEx now retains exactly two period-ring suppliers; no unconditional WachEx or full comparison closure.'),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip() == PIN
files, sources = {}, {}
for key, (path, desc, first, last) in SOURCE.items():
    data = (REPO/path).read_bytes()
    assert data == subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]), path
    lines = data.splitlines(keepends=True)
    last = last or len(lines)
    assert 1 <= first <= last <= len(lines), (key, first, last, len(lines))
    excerpt = b''.join(lines[first-1:last])
    target = HERE/'source_snapshot'/path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    url = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    record = {'path':path, 'snapshot_file':str(target.relative_to(ROOT)),
              'sha256':sha(data), 'file_sha256':sha(data), 'bytes':len(data),
              'source_commit':PIN, 'verified_equal_to_pinned_git_blob':True, 'url':url}
    files[path] = record
    sources[key] = {**record, 'id':'WIS_SRC_'+key.upper(), 'declaration':desc,
                    'line_start':first, 'line_end':last, 'range_sha256':sha(excerpt),
                    'range_bytes':len(excerpt), 'url':url+f'#L{first}-L{last}'}
raw = (HERE/'main.tex').read_bytes()
text = raw.decode()
claims = []
for cid, deps, groups, scope in CLAIMS:
    first = text.index('% BEGIN '+cid+'\n')
    last = text.index('% END '+cid+'\n', first) + len('% END '+cid+'\n')
    title = re.search(r'\\paragraph\{'+cid+r': (.*?)\}',text[first:last]).group(1)
    claims.append({
        'id':cid, 'title':title, 'classification':'B', 'introduced_in':'0.54',
        'depends_on':deps, 'sources':[sources[g] for g in groups], 'source_groups':groups,
        'scope_note':scope, 'status':'written_pending_independent_review',
        'proof_location':{'file':HERE.name+'/main.tex', 'label':'claim:'+cid,
                          'line_start':text.count('\n',0,first)+1,
                          'line_end':text.count('\n',0,last),
                          'sha256':sha(text[first:last].encode()), 'bytes':len(text[first:last].encode())},
        'source_proof_is_not_human_proof':True, 'independent_review_files':[],
    })
common = {'artifact_version':'0.54', 'component':HERE.name, 'source_commit':PIN,
          'proof_file_sha256':sha(raw), 'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1', **common,
                        'claims':claims, 'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1', **common,
                             'files':list(files.values()), 'ranges':list(sources.values()),
                             'file_count':len(files), 'range_count':len(sources)})
endpoints = [
    ('GlobalTheory.Per.integers_completeDVR','WIS1'),
    ('GlobalTheory.IoInj.abstract','WIS17'),
    ('GlobalTheory.IoInj.ioE_injective_saturated_inter','WIS18'),
    ('GlobalTheory.T.wachInclusion_injective_saturated_inter','WIS18'),
    ('GlobalTheory.HWL.Rational.padic_closed','WIS19'),
    ('GlobalTheory.Decompl.FixL.fixSub_ladic','WIS20'),
    ('GlobalTheory.Decompl.exists_fix_lift_of_fix_mod','WIS21'),
    ('GlobalTheory.TiltComplete.tilt_separated_complete','WIS22'),
    ('GlobalTheory.Decompl.dvd_iff_crd / nearPi_iff_crd','WIS23'),
    ('GlobalTheory.Decompl.nearPi_sep_complete','WIS24'),
    ('GlobalTheory.Decompl.fixSub_nearPi_complete','WIS25'),
]
ends = [{'endpoint':name,'claim':cid,'status':'whole_original_implication_written',
         'all_original_premises_retained':True} for name,cid in endpoints]
remaining = [
    'Actual original Wach prism, its maps, scalar identities and coefficient coordinates.',
    'Original cyclotomic-kernel-fixed homogeneous Frobenius matrix-solution descent: remaining Frobenius-filtration, invariant approximation, near-closedness and matrix-lifting proofs.',
    'Separate FaithH, EtBasis, Herr class maps and quantitative comparison for the full HW/Fon/Cmp triple.',
    'Original common ConclF family and all local row/table bounds; whole GLOBAL_DENOMINATOR remains open.',
]
ends.append({'endpoint':'HWL.WachEx via WLD26','claim':'WIS26',
             'status':'conditional_reduction_only','qualification':'Exactly the first two remaining period-ring suppliers, with original LocTied(p,P,AI)/IsStd and the crystalline-realization premise.'})
dump('contracts.json',{'schema':'rh-human-component-contracts/1', **common,
      'entry_premises':['Original supplied LocPrime, LocAinf, finite coefficient extensions and period maps.',
                        'Original Good/Gamma/WSer/IoS/IoW data for the full inclusion endpoint; no existence of these records is asserted.',
                        'Original arbitrary set H for each fixed-subring theorem; fixed pi only where its original consumer requires it.',
                        'Original LocTied(p,P,AI), hence the realization IsStd instance, crystalline-realization input and two remaining period-ring suppliers only for WIS26.'],
      'completed_source_endpoints':ends, 'whole_obligations_closed':[],
      'conditional_reduction_extra_inputs':{'WIS26':remaining[:2]},
      'stronger_mu_adic_completeness_not_claimed':True,
      'same_actual_period_rings_and_maps':True,
      'no_extra_interlayer_transition_hypothesis':True, 'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1', **common,
      'completed_source_endpoints':ends, 'whole_obligations_closed':[],
      'proposed_global_frontier_leaf_closures':[],
      'full_original_four_clause_Wach_inclusion_complete':True,
      'full_original_padic_closed_fixed_subring_and_NearPi_suppliers_complete':True,
      'full_original_invariant_Frobenius_matrix_descent_complete':False,
      'unconditional_original_all_layer_WachEx_complete':False,
      'full_HW_Fon_Cmp_complete':False, 'full_GLOBAL_DENOMINATOR_supplier_supplied':False,
      'independent_reviews':[], 'remaining':remaining})
parent = ROOT/'wach_lattice_descent_v53'
ledger = json.loads((parent/'provenance.json').read_text())
c = next(c for c in ledger['claims'] if c['id']=='WLD26')
pl = c['proof_location']
block = b''.join((ROOT/pl['file']).read_bytes().splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
assert sha(block) == pl['sha256']
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1', **common,
      'inputs':[{'id':'WLD26','component':parent.name,
                 'exact_parent_provenance_sha256':sha((parent/'provenance.json').read_bytes()),
                 'proof_file':pl['file'],'proof_location':pl,'proof_block_sha256':sha(block),
                 'scope_note':c['scope_note'],'role':'Complete generic all-layer return; one retained period-ring supplier is now proved.'}]})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1', **common, 'foundations':[
    {'id':'WIS_ORIGINAL_RECORDS','kind':'original_supplied_data','statement':'Exact original period data, tilt, coefficient fields, WSer/WIo maps and their prescribed compatibilities. Existence of the full records remains distinct from properties of their supplied maps.'},
    {'id':'WIS_LOCAL_FIELD_FOUNDATIONS','kind':'standard_foundations','statement':'Unique extension of the p-adic absolute value, nondegenerate trace pairing for finite characteristic-zero extensions, elementary PID and DVR criteria. The finite integral lattice, ramification relation and required completeness are proved in WIS1.'},
    {'id':'WIS_WITT_FOUNDATIONS','kind':'standard_foundations','statement':'The coordinate construction and multiplication-by-p formula for perfect p-typical Witt rings, and the original tilt domain structure. Completeness, units, coefficient saturation and every approximation limit used here are proved explicitly.'},
    {'id':'WIS_COMMUTATIVE_ALGEBRA','kind':'standard_foundations','statement':'Tensor-product universal property, finite determinants/adjugates, maximal ideals and the Jacobson criterion. The determinant argument replaces only a stronger intermediate supplier, while preserving the full original inclusion endpoint.'},
    {'id':'WIS_BHATT_SCHOLZE','kind':'retained_original_published_input','statement':'Original LocTied(p,P,AI), hence the IsStd instance used for realization, and the original crystalline-lattice realization premise are retained in the WIS26/WLD26 return; they are not claimed proved here.'},
]})
dump('published_inputs.json',[{'name':'BhattScholzeCrystallineLattices',
      'status':'retained original premise with original LocTied/IsStd in the conditional WIS26 return, not a newly discharged application',
      'source':sources['BS']}])
(HERE/'report.txt').write_text(
    'THE ACTUAL WACH COEFFICIENT EMBEDDING — v0.54\n'
    f'Source pin: {PIN}\nClaims: 26 (WIS1–WIS26).\nProof SHA256: {sha(raw)}\n\n'
    'Full original four-clause Wach inclusion: injection, unit reflection, prime saturation and exact integral intersection.\n'
    'Finite determinant/Jacobson argument avoids a stronger unneeded mu-adic completeness supplier.\n'
    'Full original p-adic closed image, fixed-subring p-adic properties and actual fixed-mod-prime lift.\n'
    'Full original tilt and NearPi separation/completeness and fixed-subring NearPi supplier, including arbitrary H and all original indices.\n'
    'WIS26 retains exactly two period-ring suppliers before full WachEx.\n'
    'The matrix-descent theorem, actual prism, later comparison package and common quantitative family remain explicit.\n'
    'No whole selected obligation closed. No Lean replay or PDF claimed. Independent review pending.\n')
(HERE/'next_source_handoff.txt').write_text(
    'NEXT PRODUCERS AFTER WIS — v0.54\n\n'
    'Do not reopen the full original four-clause Wach inclusion, p-adic closed image, fixed-subring p-adic properties, fixed-mod-prime lift, or actual tilt/NearPi separation/completeness, including the fixed-subring version. WIS1–WIS25 supply them.\n'
    'Independent task 1: ExistsWachPrismOverIntegers, with its actual io, coefficient coordinates, scalar identity, Frobenius and Gamma laws.\n'
    'Independent task 2: FixedByCyclotomicKernelEtalePhiSolutionMemWach, using WIS18, WIS19, WIS20, WIS24 and WIS25 at the exact call sites in Rational.vec.\n'
    'Remaining matrix branch: FrobeniusConstantsPiAdicFiltrationModEll, actual invariant approximation in TiltInvariantApproxByEpsilonRootsClosure / Rational.approx, near_closed with its const_dvd input in PadicClosed, and the generic MatrixFrobeniusSubOneBijectiveModSubring lifting argument. The homogeneous case suffices for WIS26; do not silently assume the stronger inhomogeneous theorem.\n'
    'Then WIS26 + WLD26 give full WachEx at every supplied original layer and etale module. FaithH/EtBasis, Herr maps and quantitative comparison remain for HW/Fon/Cmp. No extra outer-layer transition condition is present.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir()
                    if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'ranges':len(sources),
                  'proof_sha256':sha(raw)},indent=2))
