#!/usr/bin/env python3
"""Bind the invariant matrix reconstruction to exact pinned sources and prior proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
REPO = p.parse_args().repo.resolve()
AV = 'src/Development/AbelianVarietyTheory/'
I = AV + 'Proofs/InertiaEigenvalues/'
N = AV + 'Definitions/NonGaloisDescent/'
D = 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean'
SOURCE = {
 'near': (I+'CoeffZeroEqZeroIff.lean', 'Actual Near, coordinate criteria and ring maps', 1, None),
 'frob': (I+'FrobeniusConstantsPiAdicFiltrationModEll.lean', 'Full frobenius_and_constants, all four original clauses', 1, None),
 'idem': (I+'PadicClosed.lean', 'idem_pow and full generic idem_eq_zero', 60, 123),
 'series': (I+'PadicClosed.lean', 'exists_tail and full generic near_series', 125, 194),
 'closed': (I+'PadicClosed.lean', 'Full generic near_closed at its exact original premise scope', 202, 257),
 'perf': (I+'PadicClosed.lean', 'perf subring and matrix_eq coordinate return', 259, None),
 'actual': (I+'FixedByCyclotomicKernelEtalePhiSolutionMemWach.lean', 'All original actual and generic Rational producers through full inhomogeneous main', 1, None),
 'endpoint': (I+'FixedByCyclotomicKernelEtalePhiSolutionMemWachStatement.lean', 'Full exported inhomogeneous fixedByCyclotomicKernel_etalePhi_solution_mem_wach', 1, None),
 'data': (D, 'Original actual LocAinf action, roots and tilt data; exact coefficient compatibility', 761, 836),
 'good': (D, 'Original K_s and Good, including K subset K_s and all primes', 472, 483),
 'tensor': (D, 'Actual RA, RW, Frobenius, IsTiltOf and maps', 1097, 1123),
 'root': (I+'RootEqOfNormLt.lean', 'Original generator subring, all-index lift argument and invariant_approx; exact-sharp simplification in IFD8-11', 1, None),
 'flat': (I+'TiltInvariantApproxByEpsilonRootsClosure.lean', 'Full original fractional invariant approximation for every N above the threshold', 1, None),
 'sharp': (I+'IsAlgClosedTiltFieldAndValuationRing.lean', 'Exact sharp-root powers, reduction and tilt divisibility; algebraic-closedness not newly claimed', 173, 241),
 'cyclo': (I+'NormMemCyclotomicLayerPrimeRpow.lean', 'Original unramified norm and cyclotomic coefficient source', 1, None),
 'group': (AV+'Definitions/Foundations/HTBasis.lean', 'Original Kinf, Hinf and completed integral field', 1, 60),
 'operator': (I+'SubOneBijectiveQuotientOfTopNilpotent.lean', 'Full original additive-group quotient bijectivity with every printed hypothesis', 1, None),
 'matrix': (I+'MatrixFrobeniusSubOneBijectiveModSubring.lean', 'Full generic matrix_frob_sub_one_bijective, arbitrary finite d and P', 1, None),
 'records': (N+'ExistsOfLayers.lean', 'Supplied WGam/WSer/WIo, concrete IoS/IoW and original layer scopes', 1, None),
 'inclusion': (I+'WachInclusionInjectiveSaturatedInter.lean', 'Actual inclusion input already supplied by WIS18', 1, None),
 'fixedp': (I+'GaloisFixedSubringTensorWittSaturatedComplete.lean', 'Actual fixed-ring p-adic inputs already WIS20', 1, None),
 'fixednear': (I+'GaloisFixedTensorWittCompletePiAdicModEll.lean', 'Actual fixed-ring near-parameter completeness already WIS25', 1, None),
 'consumer': (I+'WachLatticesExistAllLayersOfBhattScholze.lean', 'Exact homogeneous descent consumer and conditional WachEx return', 1, None),
 'prism': (I+'ExistsWachPrismOverIntegers.lean', 'One retained actual Wach-prism supplier, not proved in this packet', 1, None),
 'scope': (N+'ConvZero.lean', 'WachEx and separate FaithH/EtBasis scopes', 1, None),
 'BS': (AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeCrystallineLattices.lean', 'Original retained crystalline-realization premise', 1, None),
}
CLAIMS = [
 ('IFD1',['WIS23'],['near'],'Exact Near subgroup calculus and unchanged tensor-coordinate criterion.'),
 ('IFD2',['IFD1','WIS4','WIS22'],['frob'],'Full original four-clause Frobenius/constants theorem, every original s and prime.'),
 ('IFD3',[],['idem'],'Full generic idempotent-vanishing theorem with its original saturation, separation and unit premises.'),
 ('IFD4',['IFD3'],['actual'],'Full original generic component const_dvd, retaining actual component idempotents.'),
 ('IFD5',['IFD1'],['series'],'Full generic near_series using only its stated constant criterion, and explicit formal-series tails.'),
 ('IFD6',['IFD5','IFD1'],['closed'],'Full generic near_closed modulo p, with no extra parameter-adic completeness assumption.'),
 ('IFD7',['IFD4','IFD6','WIS1','WIS5','WIS18','WIS24'],['actual','records'],'Full original fixed coefficient image, bounded pole and actual/generic closed implications.'),
 ('IFD8',['LS1','LS4'],['data','sharp','group'],'Exact original action equivariance of all sharp-root coordinates and same-field completed fixed values, including p=2.'),
 ('IFD9',['LS2'],['root','cyclo'],'Integral unramified residue representatives and the full finite cyclotomic integral coefficient calculation.'),
 ('IFD10',['IFD9'],['root','data'],'Full generator-lift conclusion at every original coefficient index N and the same K0.'),
 ('IFD11',['IFD8','IFD10','LS4'],['root','sharp'],'Full original invariant_approx, by the simpler exact-fixed-sharp-root argument; no cyclotomic Tate H1 supplier retained.'),
 ('IFD12',['IFD11','IFD8','IFD9'],['flat','data'],'Full fractional invariant approximation with one threshold and every larger N.'),
 ('IFD13',[],['actual','good','group','tensor'],'Actual Good inclusion Hinf subset GK intersect ker chi and fixed zeroth Witt coordinates.'),
 ('IFD14',[],['perf','matrix'],'Full eventual-Frobenius coefficient subring and persistence at arbitrary ring-map scope.'),
 ('IFD15',['IFD1','IFD12','IFD13'],['actual','tensor'],'Full approx_subring for every supplied subring, without falsely treating Teichmuller lift as additive.'),
 ('IFD16',['IFD7','IFD14','IFD15'],['actual','records'],'Full actual Rational.approx at the original Good/Gamma/R/I/IoW scope.'),
 ('IFD17',[],['operator'],'Every original abstract additive hypothesis is printed; one full p-adic kernel step.'),
 ('IFD18',['IFD17'],['operator'],'Full injectivity on the quotient by the original coefficient subgroup.'),
 ('IFD19',['IFD17'],['operator'],'Full one-step cokernel lifting with exact telescoping sign and saturated residual.'),
 ('IFD20',['IFD17','IFD18','IFD19'],['operator'],'Full original sub_one_bijective_quotient_of_topNilpotent, no extra topology or torsion assumption.'),
 ('IFD21',['IFD1'],['matrix'],'One common finite coefficient pole and the exact shifted contracting filtration.'),
 ('IFD22',['IFD21','IFD14'],['matrix'],'Finite common iteration and eventual smallness with no coefficient Frobenius inverse.'),
 ('IFD23',['IFD17','IFD20','IFD21','IFD22'],['matrix'],'Full original generic matrix_frob_sub_one_bijective at all original hypotheses, including d=0 and noninvertible P.'),
 ('IFD24',['IFD2','IFD7','IFD16','IFD23','WIS18','WIS19','WIS20','WIS25'],['actual','inclusion','fixedp','fixednear'],'Full original Rational.vec and both quotient bijectivity conclusions on the actual fixed ring.'),
 ('IFD25',['IFD24'],['actual','endpoint','perf'],'Full original inhomogeneous rectangular matrix descent, all original assumptions and zero dimensions preserved.'),
 ('IFD26',['IFD25','WIS18','WLD26'],['consumer','prism','scope','BS'],'Conditional full WachEx retains exactly one period-ring supplier, plus original tied data and crystalline realization.'),
]
def sha(b):
    return hashlib.sha256(b).hexdigest()
def dump(name,x):
    (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()==PIN
sources,files={},{}
for key,(path,desc,first,last) in SOURCE.items():
    data=(REPO/path).read_bytes()
    assert data==subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]),path
    lines=data.splitlines(keepends=True)
    last=last or len(lines)
    assert 1<=first<=last<=len(lines),(key,len(lines))
    excerpt=b''.join(lines[first-1:last])
    target=HERE/'source_snapshot'/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    rec={'path':path,'snapshot_file':str(target.relative_to(ROOT)),
         'sha256':sha(data),'file_sha256':sha(data),'bytes':len(data),
         'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
    files[path]=rec
    sources[key]={**rec,'id':'IFD_SRC_'+key.upper(),'declaration':desc,
                  'line_start':first,'line_end':last,'range_sha256':sha(excerpt),
                  'range_bytes':len(excerpt),'url':url+f'#L{first}-L{last}'}
raw=(HERE/'main.tex').read_bytes()
text=raw.decode()
claims=[]
for cid,deps,groups,scope in CLAIMS:
    start=text.index('% BEGIN '+cid+'\n')
    end=text.index('% END '+cid+'\n',start)+len('% END '+cid+'\n')
    title=re.search(r'\\paragraph\{'+cid+r': (.*?)\}',text[start:end]).group(1)
    block=text[start:end].encode()
    claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.55',
      'depends_on':deps,'sources':[sources[g] for g in groups],'source_groups':groups,
      'scope_note':scope,'status':'written_pending_independent_review',
      'proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
       'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end),
       'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.55','component':HERE.name,'source_commit':PIN,
        'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
     'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
     'files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
names=[
 ('GlobalTheory.DecomplFrob.frobenius_and_constants','IFD2'),
 ('GlobalTheory.HWL.Rational.idem_eq_zero','IFD3'),
 ('GlobalTheory.HWL.Rational.const_dvd','IFD4'),
 ('GlobalTheory.HWL.Rational.exists_tail / near_series','IFD5'),
 ('GlobalTheory.HWL.Rational.near_closed','IFD6'),
 ('GlobalTheory.HWL.Rational.ioE_fixed / bounded_pole / closed','IFD7'),
 ('GlobalTheory.TiltInvariants.invariant_approx','IFD11'),
 ('GlobalTheory.FlatInvariants.flat_invariant_approx','IFD12'),
 ('GlobalTheory.HWL.Rational.perf','IFD14'),
 ('GlobalTheory.HWL.Rational.approx_subring','IFD15'),
 ('GlobalTheory.HWL.Rational.approx','IFD16'),
 ('GlobalTheory.sub_one_bijective_quotient_of_topNilpotent','IFD20'),
 ('GlobalTheory.DecomplMat.matrix_frob_sub_one_bijective','IFD23'),
 ('GlobalTheory.HWL.Rational.vec','IFD24'),
 ('GlobalTheory.HWL.Rational.main','IFD25'),
 ('GlobalTheory.T.fixedByCyclotomicKernel_etalePhi_solution_mem_wach','IFD25'),
]
ends=[{'endpoint':x,'claim':c,'status':'whole_original_implication_written',
       'all_original_premises_retained':True} for x,c in names]
ends.append({'endpoint':'HWL.WachEx via WLD26','claim':'IFD26','status':'conditional_reduction_only',
 'qualification':'Exactly one remaining period-ring supplier: actual Wach prism, retaining original LocTied/IsStd and crystalline realization.'})
remaining=[
 'Actual original Wach prism with all prescribed maps, scalar identity and both finite coefficient-coordinate assertions.',
 'Original LocTied/IsStd and Bhatt-Scholze crystalline-realization premises retained in the conditional all-layer return.',
 'Separate FaithH, EtBasis, Herr class maps and quantitative comparison for full HW/Fon/Cmp.',
 'Common ConclF family and all quantitative local row/table bounds; whole GLOBAL_DENOMINATOR remains open.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['Original LocPrime/LocAinf actions, roots and maps.','Original Good/Gamma/WSer/IoS/IoW at the actual matrix endpoint; their existence is not asserted here.','Exact printed generic hypotheses for near_closed and additive/matrix bijectivity.','Original tied period data and crystalline realization only in the conditional IFD26 return.'],
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'conditional_reduction_extra_inputs':{'IFD26':remaining[:2]},
 'same_actual_period_rings_and_maps':True,'same_H_K_s_coefficient_basis':True,
 'exact_sharp_root_simplification':True,'cyclotomic_Tate_H1_not_needed_for_this_proof':True,
 'no_extra_interlayer_transition_hypothesis':True,'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'proposed_global_frontier_leaf_closures':[],
 'full_original_inhomogeneous_invariant_Frobenius_matrix_descent_complete':True,
 'full_original_generic_additive_and_matrix_bijectivity_complete':True,
 'full_original_invariant_tilt_approximation_and_near_closedness_complete':True,
 'exactly_one_period_ring_supplier_before_conditional_WachEx':True,
 'unconditional_original_all_layer_WachEx_complete':False,'full_HW_Fon_Cmp_complete':False,
 'full_GLOBAL_DENOMINATOR_supplier_supplied':False,'independent_reviews':[],'remaining':remaining})
inherited=[]
ids=sorted({d for _,ds,_,_ in CLAIMS for d in ds if not d.startswith('IFD')})
for cid in ids:
    comp='local_stages' if cid.startswith('LS') else ('wach_inclusion_saturation_v54' if cid.startswith('WIS') else 'wach_lattice_descent_v53')
    parent=ROOT/comp
    ledger=json.loads((parent/'provenance.json').read_text())
    claim=next(c for c in ledger['claims'] if c['id']==cid)
    raw_parent=(parent/'main.tex').read_bytes()
    t=raw_parent.decode()
    pl=claim.get('proof_location',{})
    if 'line_start' in pl:
        first,last=pl['line_start'],pl['line_end']
    else:
        start=t.index('\\paragraph{'+cid+':')
        end=t.find('\\paragraph{',start+1)
        if end<0: end=len(t)
        first=t.count('\n',0,start)+1
        last=t.count('\n',0,end)
    block=b''.join(raw_parent.splitlines(keepends=True)[first-1:last])
    loc={'file':comp+'/main.tex','line_start':first,'line_end':last,'sha256':sha(block),'bytes':len(block)}
    inherited.append({'id':cid,'component':comp,
      'exact_parent_provenance_sha256':sha((parent/'provenance.json').read_bytes()),
      'proof_file':loc['file'],'proof_location':loc,'proof_block_sha256':sha(block),
      'scope_note':claim.get('scope_note',claim.get('title',cid)),
      'role':'Exact prior human input; completed matrix argument uses its printed actual scope.'})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[
 {'id':'IFD_ORIGINAL_RECORDS','kind':'original_supplied_data','statement':'The exact original local period data, finite coefficient fields, actions, WGam/WSer/WIo and IoW; no existence is added or inferred.'},
 {'id':'IFD_ELEMENTARY_FOUNDATIONS','kind':'standard_foundations','statement':'Algebraic fixed-field correspondence, finite fields, polynomial division, finite sums and tensor coordinates. The needed unramified coefficient and Newton-lift facts are explained in IFD9.'},
 {'id':'IFD_PRIOR_HUMAN_PROOFS','kind':'previously_proved_human_inputs','statement':'LS1 completed fixed fields, LS2 cyclotomic norms, LS4 tilt valuation, WIS original ring/completeness inputs and WLD26 exact consumer are individually rebound in inherited_inputs.json.'},
 {'id':'IFD_BHATT_SCHOLZE','kind':'retained_original_published_input','statement':'Original tied local data, IsStd and crystalline-lattice realization remain premises of IFD26, not newly proved applications.'},
]})
dump('published_inputs.json',[{'name':'BhattScholzeCrystallineLattices',
 'status':'Retained original premise only in conditional IFD26; no new published application asserted','source':sources['BS']}])
(HERE/'report.txt').write_text(
 'INVARIANT FROBENIUS-MATRIX DESCENT — v0.55\n'
 f'Source pin: {PIN}\nClaims: 26 (IFD1–IFD26).\nProof SHA256: {sha(raw)}\n\n'
 'Full original inhomogeneous rectangular matrix descent on the unchanged actual coefficient map.\n'
 'Full generic additive and matrix quotient bijectivity; full actual invariant approximation and near-closedness.\n'
 'Exact fixed sharp-root coordinates plus LS1 replace an unnecessary cyclotomic Tate cohomology detour.\n'
 'Original p=2, good-layer, character-kernel and coefficient-basis scopes are preserved.\n'
 'Exactly one period-ring supplier remains before conditional WachEx: the actual Wach prism.\n'
 'Original tied data and crystalline realization retained; HW/Fon/Cmp and common quantitative family remain.\n'
 'No whole selected obligation closed; no Lean replay or PDF claimed. Independent review pending.\n')
(HERE/'next_source_handoff.txt').write_text(
 'NEXT PRODUCERS AFTER IFD — v0.55\n\n'
 'Do not reopen original actual ioE inclusion, fixed-subring and NearPi completeness, const_dvd/near_closed, invariant approximation, or fixed Frobenius matrix descent. WIS and IFD supply them fully.\n'
 'Next bounded task: ExistsWachPrismOverIntegers, all original maps, coefficient coordinates, scalar identity, Frobenius and Gamma laws. No layer transition system is added.\n'
 'IFD26 + WLD26 then return full WachEx for every original layer and supplied etale module, retaining original LocTied/IsStd and crystalline realization.\n'
 'Afterwards prove FaithH/EtBasis, Herr maps and quantitative comparison; assemble HW/Fon/Cmp and every local row bound in one common ConclF family.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),
 'inherited_inputs':len(inherited),'proof_sha256':sha(raw)},indent=2))
