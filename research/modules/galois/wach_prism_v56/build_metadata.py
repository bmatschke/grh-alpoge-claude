#!/usr/bin/env python3
"""Bind the Wach-prism reconstruction to exact pinned sources and prior proofs."""
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
 'unram': (I+'ExistsSumRootsOfUnity.lean','Original unramified root-of-unity span',1,None),
 'sig': (I+'ExistsWachPrismOverIntegers.lean','Actual sigW, divisibility and Frobenius lift',24,57),
 'chi': (I+'ExistsIntegralCyclotomicChar.lean','Full original integral cyclotomic character',1,None),
 'chibasic': (I+'CyclotomicCharacterPadicBasicProperties.lean','Cyclotomic integrality, continuity and fixed-field criteria',1,None),
 'laws': (I+'CyclotomicPowerSeriesAlgHomActionLaws.lean','Full original power-series action laws',1,None),
 'lawsst': (I+'CyclotomicPowerSeriesAlgHomActionLawsStatement.lean','All six exported action-law clauses',1,None),
 'ext': (I+'AlgHomExtOfConstantCoeffZero.lean','Formal-series extensionality and full action uniqueness',1,None),
 'geom': (I+'GeomSumOneAddPrime.lean','Full generic difference divisibility and all XX_QQ properties',1,None),
 'division': (I+'CDvdOfMapEqZero.lean','Generic kernel, mixed completeness, Frobenius lift and coefficientwise series statements',1,None),
 'cyclo': (I+'CyclotomicIntegersEqWittZetaSubOne.lean','Full original integral cyclotomic polynomial theorem',1,None),
 'factor': (I+'ExistsWachInclusionPowerSeriesIntoOneTmulAinf.lean','Full generic retraction/factor and actual exists_io',1,None),
 'factorst': (I+'ExistsWachInclusionPowerSeriesIntoOneTmulAinfStatement.lean','Full exported original io existence statement',1,None),
 'tensor': (I+'UnramifiedIntegersTensorEqLetterwiseProductAinf.lean','Original scalar rigidity and prime-to-p constant calculation',1,None),
 'coords': (I+'ExistsUniqueUnramifiedIntegersCoordsBasis.lean','Full generic separated coordinates and all original unramified embeddings',1,None),
 'coordsst': (I+'ExistsUniqueUnramifiedIntegersCoordsBasisStatement.lean','Full original all-basis unramified coordinates',1,None),
 'prismmaps': (I+'ExistsWachPrismOverIntegers.lean','Original actual action/Frobenius maps, specialization and structure map',59,183),
 'prismobjs': (I+'ExistsWachPrismOverIntegers.lean','Actual bounded prism objects and all morphisms',185,302),
 'prismcoords': (I+'ExistsWachPrismOverIntegers.lean','Both original formal-series coordinate conclusions',304,324),
 'prism': (I+'ExistsWachPrismOverIntegers.lean','Full exists_prism with sixteen output fields',331,None),
 'prismst': (I+'ExistsWachPrismOverIntegersStatement.lean','Full exported Wach-prism endpoint',1,None),
 'delta': (N+'InvertibleSpanSingleton.lean','Original delta, bounded prism and morphism definitions',1,None),
 'ainf': (N+'NormLeOneOfMemOL.lean','Actual Fontaine prism and its Galois morphisms',1,None),
 'cycdefs': (N+'MemEurOfTeichmullerSeries.lean','Actual binomial series, act, phi, XX and QQ',1,92),
 'data': (D,'Original Good layer, supplied coefficient data, actions and roots',472,836),
 'records': (N+'ExistsOfLayers.lean','Original WSer/IoS/IoW, WN and coefficient scalar maps',1,None),
 'consumer': (I+'WachLatticesExistAllLayersOfBhattScholze.lean','Full original conditional WachEx theorem',1,None),
 'scope': (N+'ConvZero.lean','Original WachEx, FaithH and EtBasis scopes',1,None),
 'BS': (AV+'PublishedTheorems/GaloisCohomology₂/BhattScholzeCrystallineLattices.lean','Retained original crystalline-realization premise',1,None),
}
CLAIMS = [
 ('WPR1',['WIS1','IFD9'],['unram','sig'],'Actual unramified root basis and Frobenius lift on the same W0.'),
 ('WPR2',['IFD9'],['chi','chibasic'],'Full integral cyclotomic character including continuity and every original congruence-lifting clause, also p=2.'),
 ('WPR3',[],['laws','lawsst','cycdefs'],'Full original action laws on arbitrary commutative Zp-algebras, by finite coefficient identities.'),
 ('WPR4',[],['ext','geom','division'],'Full generic algebra-map extensionality and difference divisibility, without continuity.'),
 ('WPR5',['WPR3','WPR4'],['ext'],'Full original act_unique from explicit first-differing-coefficient comparison.'),
 ('WPR6',['WPR2','WPR5','WIS1'],['prismmaps','data'],'Exact identification of the supplied R Frobenius and Gamma actions.'),
 ('WPR7',['WPR3','WPR4'],['geom','cycdefs'],'All seven original XX_QQ_properties clauses at arbitrary ring scope.'),
 ('WPR8',[],['division'],'Full generic distinguished division and kernel theorem, no Noetherian or continuity premise.'),
 ('WPR9',[],['division'],'Full generic (p,Q)-adic completeness under the original p-adic coefficient hypothesis.'),
 ('WPR10',['WPR1','IFD9','LS2'],['cyclo'],'Full integral cyclotomic polynomial statement for every original primitive root and actual integral field.'),
 ('WPR11',[],['factor'],'Full generic normalized retraction; the coefficient free module need not be finite.'),
 ('WPR12',['WPR11'],['factor'],'Full original separated tensor factor theorem, without added continuity or completeness.'),
 ('WPR13',['WIS1','WIS2','WIS3','WIS4'],['factor'],'Actual pure-tensor parameter separation for every permitted tilt element.'),
 ('WPR14',['WPR1','WIS4','LS4'],['factor','tensor','records'],'Actual constant descent and theta identity from finite prime-to-p root sums.'),
 ('WPR15',['WPR11','WPR12','WPR13','WPR14','WIS1'],['factor','factorst','records'],'Full original Wach power-series pure-tensor inclusion and broader exists_io.'),
 ('WPR16',['WPR3','WPR6','WPR11','WPR15','WIS5','IFD8'],['prismmaps','ainf','data'],'Actual embedding injectivity and all Frobenius/Galois intertwining maps.'),
 ('WPR17',['WPR7','WPR8','WPR10','WPR15','LS4'],['prismmaps','cyclo','division'],'Full actual theta kernel, base image and structure map; full generic exists_str.'),
 ('WPR18',['WPR1','WPR3','WIS2'],['delta','division','ainf'],'Full p-torsion-free delta lift algebra, morphism criterion and actual series/Witt lifts.'),
 ('WPR19',['WPR18','WIS2','WIS22','LS4'],['ainf','delta'],'Every field of the actual Fontaine bounded prism and original Galois prism morphisms.'),
 ('WPR20',['WPR1','WPR7','WPR9','WPR17','WPR18'],['prismobjs','delta'],'Every field of the original series prism, including mixed completeness and bounded torsion.'),
 ('WPR21',['WPR1','WPR18','WPR20'],['prismobjs'],'Every field of the constant prism and evaluation morphism, surjectivity and exact kernel.'),
 ('WPR22',['WPR15','WPR16','WPR17','WPR18','WPR19','WPR20'],['prismobjs','ainf'],'The actual io prism morphism with original base structure and pure-tensor map.'),
 ('WPR23',['WPR2','WPR3','WPR7','WPR16','WPR17','WPR18','WPR19','WPR20','WPR21','WPR22'],['prismobjs'],'All original Galois prism morphisms and both exact morphism compatibilities.'),
 ('WPR24',['WPR3','WPR6','WPR16'],['prismmaps','prism'],'Actual parameter, distinguished polynomial and literal original scalar-map equality.'),
 ('WPR25',[],['coords'],'Full generic unit-separated coordinate theorem on all original commutative rings and bases.'),
 ('WPR26',['WPR1','WPR25','WIS1'],['coords','coordsst'],'Full original unramified coordinate theorem for every prescribed coefficient basis.'),
 ('WPR27',[],['division','prismcoords'],'Full generic existsUnique_series and existsUnique_of_basis, arbitrary indexing set.'),
 ('WPR28',['WPR1','WPR24','WPR26','WPR27'],['prismcoords','coordsst'],'Both original finite coordinate assertions on the same a and z; all O bases retained.'),
 ('WPR29',['WPR15','WPR16','WPR20','WPR21','WPR22','WPR23','WPR24','WPR28'],['prism','prismst','data'],'Full original exists_prism and exported Wach-prism endpoint, all sixteen output fields.'),
 ('WPR30',['WPR24','WPR29','WIS18','IFD25','WLD26'],['consumer','scope','BS'],'Full original BS and LocTied imply WachEx; no period-ring supplier left, later comparison inputs retained.'),
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
    sources[key]={**rec,'id':'WPR_SRC_'+key.upper(),'declaration':desc,
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
    claims.append({'id':cid,'title':title,'classification':'B','introduced_in':'0.56',
      'depends_on':deps,'sources':[sources[g] for g in groups],'source_groups':groups,
      'scope_note':scope,'status':'written_pending_independent_review',
      'proof_location':{'file':HERE.name+'/main.tex','label':'claim:'+cid,
       'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end),
       'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'independent_review_files':[]})
common={'artifact_version':'0.56','component':HERE.name,'source_commit':PIN,
        'proof_file_sha256':sha(raw),'status':'written_pending_independent_review'}
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
     'claims':claims,'main_tex_sha256':sha(raw)})
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
     'files':list(files.values()),'ranges':list(sources.values()),'file_count':len(files),'range_count':len(sources)})
names = [
 ('GlobalTheory.UnramSpan.exists_sum_rootsOfUnity','WPR1'),
 ('GlobalTheory.PrismS.sigW_lift','WPR1'),
 ('GlobalTheory.Cyc.exists_integral_cyclotomicChar','WPR2'),
 ('GlobalTheory.T.cyclotomicPowerSeriesAlgHom_action_laws','WPR3'),
 ('GlobalTheory.Cyc.algHom_ext_of_constantCoeff_zero / algHom_sub_dvd','WPR4'),
 ('GlobalTheory.Cyc.act_unique','WPR5'),
 ('GlobalTheory.Cyc.XX_QQ_properties','WPR7'),
 ('GlobalTheory.PrismS.ker_eq_span','WPR8'),
 ('GlobalTheory.PrismS.isAdicComplete_span','WPR9'),
 ('GlobalTheory.PrismS.Poly.main','WPR10'),
 ('GlobalTheory.PrismS.IoDescent.exists_retraction','WPR11'),
 ('GlobalTheory.PrismS.IoDescent.exists_factor','WPR12'),
 ('GlobalTheory.PrismS.IoDescent.exists_io / main','WPR15'),
 ('GlobalTheory.T.exists_wachInclusion_powerSeries_into_one_tmul_ainf','WPR15'),
 ('GlobalTheory.PrismS.ker_theta_io / exists_str','WPR17'),
 ('GlobalTheory.Prism.Delta.ofLift / Delta.map_δ_of_map_φ','WPR18'),
 ('GlobalTheory.Prism.ainfObj / ainfHom','WPR19'),
 ('GlobalTheory.PrismS.prismS','WPR20'),
 ('GlobalTheory.PrismS.prismW / evHom','WPR21'),
 ('GlobalTheory.PrismS.ioHom','WPR22'),
 ('GlobalTheory.PrismS.actHom','WPR23'),
 ('GlobalTheory.PrismSplit.existsUnique_of_separated','WPR25'),
 ('GlobalTheory.T.existsUnique_unramifiedIntegers_coords_basis','WPR26'),
 ('GlobalTheory.PrismS.existsUnique_series / existsUnique_of_basis','WPR27'),
 ('GlobalTheory.PrismS.exists_coordinates and original all-basis coordinates','WPR28'),
 ('GlobalTheory.PrismS.exists_prism','WPR29'),
 ('GlobalTheory.T.exists_wach_prism_over_integers','WPR29'),
 ('GlobalTheory.WachLattice.main','WPR30'),
]
ends=[{'endpoint':x,'claim':c,'status':'whole_original_implication_written',
       'all_original_premises_retained':True} for x,c in names]
remaining=[
 'Original LocTied/IsStd and Bhatt-Scholze crystalline-realization premises remain in the now-completed original conditional WachEx theorem.',
 'Separate FaithH, EtBasis, Herr cohomology class maps and quantitative de Rham comparison for full HW/Fon/Cmp.',
 'Every local row/table bound in one common ConclF family; original exceptional sets, summability and uniform thresholds.',
 'Whole GLOBAL_DENOMINATOR remains open; no extra outer-layer transition condition is added.',
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
 'entry_premises':['Original LocPrime/LocAinf, finite fields, Good, GamS/WSer/IoS/IoW with all actual maps.','Only the exact printed hypotheses in each generic algebra theorem.','Original BS and LocTied are retained only at the final original WachEx implication.'],
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'conditional_reduction_extra_inputs':{},
 'original_WachEx_premises_retained':['BhattScholzeCrystallineLattices','LocTied'],
 'all_sixteen_original_prism_fields':True,'same_actual_period_rings_and_maps':True,
 'both_coefficient_coordinates_all_original_bases':True,
 'no_extra_continuity_noetherian_or_interlayer_assumptions':True,
 'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
 'completed_source_endpoints':ends,'whole_obligations_closed':[],
 'proposed_global_frontier_leaf_closures':[],
 'full_original_Wach_prism_complete':True,
 'full_original_conditional_WachEx_complete':True,
 'remaining_period_ring_suppliers_before_original_conditional_WachEx':0,
 'original_BS_and_LocTied_retained':True,
 'unconditional_original_all_layer_WachEx_complete':False,
 'full_HW_Fon_Cmp_complete':False,'full_GLOBAL_DENOMINATOR_supplier_supplied':False,
 'independent_reviews':[],'remaining':remaining})
inherited=[]
ids=sorted({d for _,ds,_,_ in CLAIMS for d in ds if not d.startswith('WPR')})
for cid in ids:
    comp=('local_stages' if cid.startswith('LS') else
          'wach_inclusion_saturation_v54' if cid.startswith('WIS') else
          'invariant_frobenius_descent_v55' if cid.startswith('IFD') else
          'wach_lattice_descent_v53')
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
      'role':'Exact inherited human argument on its unchanged original rings and maps.'})
dump('inherited_inputs.json',{'schema':'rh-inherited-human-inputs/1',**common,'inputs':inherited})
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':[
 {'id':'WPR_ORIGINAL_RECORDS','kind':'original_supplied_data','statement':'Original period data, fields, Good/GamS/WSer/IoS/IoW, including all prescribed maps; their universal existence is not asserted by this chapter.'},
 {'id':'WPR_ELEMENTARY_FOUNDATIONS','kind':'standard_foundations','statement':'Finite fields, Galois extension of embeddings, finite free bases, determinant and tensor identities, coefficientwise formal-series algebra and inverse-limit completeness. The needed convergence and quotient steps are proved explicitly.'},
 {'id':'WPR_PRIOR_HUMAN_PROOFS','kind':'previously_proved_human_inputs','statement':'LS2/LS4, WIS actual rings and fixed completeness, IFD actual action and invariant descent, WLD26 original lattice consumer. Each input is rebound in inherited_inputs.json.'},
 {'id':'WPR_BS_LOCTIED','kind':'retained_original_published_input','statement':'Original tied-period data and crystalline-realization input are exactly the hypotheses of the completed WachLattice.main implication.'},
]})
dump('published_inputs.json',[{'name':'BhattScholzeCrystallineLattices',
 'status':'Retained original premise of full original WPR30 implication; no new unconditional published application asserted','source':sources['BS']}])
(HERE/'report.txt').write_text(
 'THE PRESCRIBED WACH PRISM AND ORIGINAL WACH-EXISTENCE RETURN — v0.56\n'
 f'Source pin: {PIN}\nClaims: 30 (WPR1–WPR30).\nProof SHA256: {sha(raw)}\n\n'
 'Full original actual prism with all sixteen output fields, exact maps and both all-basis coordinate assertions.\n'
 'Full generic action, difference, distinguished division, tensor-factor and separated-coordinate arguments.\n'
 'Every bounded-prism field is checked on the actual Fontaine and power-series rings.\n'
 'WIS18 and IFD25 now discharge the two other period-ring suppliers in WLD26.\n'
 'Full original BS + LocTied implies WachEx, for every original layer and supplied etale module.\n'
 'Original tied data and crystalline realization remain premises; FaithH/EtBasis/Herr/Cmp/common family remain.\n'
 'No whole selected obligation closure, Lean replay or PDF is claimed. Independent review pending.\n')
(HERE/'next_source_handoff.txt').write_text(
 'NEXT PRODUCERS AFTER WPR — v0.56\n\n'
 'Do not reopen the actual Wach prism, its scalar identity or coefficient decompositions. WPR29 supplies all sixteen original fields.\n'
 'Do not reopen the original BS + LocTied implies WachEx theorem. WPR30, WIS18, IFD25 and WLD26 complete that original implication.\n'
 'Next independent original tasks: FaithH and EtBasis in ConvZero, then Herr class maps and quantitative de Rham comparison. Preserve original bases, invariants, cyclotomic maps and every lattice morphism.\n'
 'Assemble HW/Fon/Cmp on each permitted layer without adding an outer transition-system hypothesis.\n'
 'Then obtain every local row/table bound in one common ConclF family; retain ShaFinOdd, exceptional sets, vvTerm summability and uniform thresholds. Whole GLOBAL_DENOMINATOR remains open.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json' and p.suffix!='.tmp'})
print(json.dumps({'claims':len(claims),'source_files':len(files),'source_ranges':len(sources),
 'inherited_inputs':len(inherited),'proof_sha256':sha(raw)},indent=2))
