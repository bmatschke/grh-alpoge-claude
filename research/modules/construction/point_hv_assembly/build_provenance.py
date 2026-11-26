#!/usr/bin/env python3
"""Rebuild exact proof/source locators for the complete PointHV assembly."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
P = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
PATHS = {
    'stmt': P+'StmtFields.lean',
    'data': P+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean',
    'counts': P+'HeightAndVanishing/Counts.lean',
    'layer': P+'HeightAndVanishing/LayerLe.lean',
    'index': P+'HeightAndVanishing/HostIndex.lean',
    'hostcomp': P+'HeightAndVanishing/HostComp.lean',
    'hostodd': P+'HeightAndVanishing/HostOdd.lean',
    'hostlevel': P+'HeightAndVanishing/HostLevel.lean',
    'bchi': P+'HeightAndVanishing/BchiFacts.lean',
    'card': P+'HeightAndVanishing/CardLeLevel.lean',
    'vord': P+'HeightAndVanishing/PowTotientConductor.lean',
    'v2': P+'HeightAndVanishing/CmDatumCharTwoAdicOrderBounds.lean',
    'vsfield': P+'HeightAndVanishing/VsField.lean',
    'countvs': P+'HeightAndVanishing/CountVs.lean',
    'ivfield': P+'HeightAndVanishing/IvField.lean',
    'countiv': P+'HeightAndVanishing/CountIV.lean',
    'cases': P+'HeightAndVanishing/Cases.lean',
    'red': P+'HeightAndVanishing/RedAll.lean',
    'loss': P+'HeightAndVanishing/LossLe.lean',
    'sumin': P+'HeightAndVanishing/FinalLe.lean',
    'sumout': P+'HeightAndVanishing/SumOut.lean',
    'point': P+'HeightAndVanishing/PointArith.lean',
    'join': P+'HeightAndVanishing/JointWinOfCounts.lean',
    'len': P+'CharacterLevelBounds/ShaFamMono.lean',
    'sign': P+'CharacterLevelBounds/SignLe.lean',
    'part': P+'CharacterLevelBounds/PartModel.lean',
    'up': P+'CharacterLevelBounds/LiftGens.lean',
    'parts': P+'PartsSign.lean',
    'coeff': P+'GaloisLibrary/SelmerTransport/ConjStableShaFam.lean',
    'locsel': P+'GaloisLibrary/SelmerTransport/RestrictionMemInvariantH1.lean',
    'lchi': P+'PrimeSetBoundDataOfPrimitiveChar.lean',
}

def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def main(repo):
    cache = {}
    for key, path in PATHS.items():
        raw = (repo/path).read_bytes()
        assert raw == subprocess.check_output(['git', '-C', str(repo), 'show', PIN+':'+path]), path
        cache[key] = raw

    def anchor(key, declaration, role='exact definition or reconstructed source consumer'):
        raw = cache[key]; lines = raw.decode().splitlines()
        pat = re.compile(r'^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure)\s+'+re.escape(declaration)+r'(?=[\s:(])')
        hits = [i+1 for i, line in enumerate(lines) if pat.match(line)]
        assert len(hits) == 1, (key, declaration, hits)
        start = hits[0]; end = len(lines)
        for i in range(start, len(lines)):
            if re.match(r'^(?:(?:private|noncomputable)\s+)?(?:theorem|def|abbrev|structure|end|section|namespace|variable|instance|attribute|omit|open)\b|^@\[', lines[i]):
                end = i; break
        while end > start and not lines[end-1].strip(): end -= 1
        frag = b''.join(raw.splitlines(keepends=True)[start-1:end])
        return {'path': PATHS[key], 'declaration': declaration, 'line_start': start, 'line_end': end,
                'sha256': sha(raw), 'range_sha256': sha(frag), 'range_bytes': len(frag),
                'first_line': lines[start-1], 'role': role,
                'url': REPO+'/blob/'+PIN+'/'+PATHS[key]+f'#L{start}-L{end}',
                'verified_equal_to_pinned_git_blob': True}

    def A(key, *names): return [anchor(key, name) for name in names]

    remaining = ['CountI', 'CountII', 'CountIII', 'CountV']
    specs = [
        ('HV1', 'Actual host field, all component/conductor bounds and exceptional primes', [], [], [],
         A('data','Host','N','H','IsChar','Big','X','comp','chiP','th1','c2')+
         A('stmt','Bchi')+A('index','UpperTheory.V.HV.hostIndex')+
         A('hostcomp','UpperTheory.V.HV.hostComp')+A('hostodd','UpperTheory.V.HV.hostOdd')+
         A('hostlevel','UpperTheory.V.HV.hostLevel')+A('bchi','UpperTheory.V.HV.bchiFacts')+
         A('card','UpperTheory.V.HV.xCard')),
        ('HV2', 'Quantitative finite-field restriction at every odd prime, including degree primes', [], ['HV-CYC'], [],
         A('up','UpperTheory.V.Chr.upV')+A('len','rho','h0','VS','V','V\'','nrm')+
         A('coeff','QO','twist₂','shaFam','ShaU')+A('locsel','LocSel','mk_mem_locSel')),
        ('HV3', 'Integral simultaneous character inequality without inverting the group order', [], [], [],
         A('sign','UpperTheory.V.Chr.signLe')),
        ('HV4', 'Original-field plus comparison with polynomial error and exact good-prime control', ['HV1','HV2','HV3'], [], [],
         A('part','UpperTheory.V.Chr.partModel')+A('parts','twScal_conj','mk_mem_ShaPlus_iff')+
         A('len','rho','eigL','dirG','levH','HasLevel','evenSet','V\'')+
         [anchor('red','UpperTheory.V.HV.redAll','source comparison replaced by HV4; its specific lossAll formula is not claimed'),
          anchor('loss','UpperTheory.V.HV.lossLe','combined source error-estimate route replaced by direct +(Ne)^6 proof')]),
        ('HV5', 'Literal CountVs from a fixed-degree field and LemmaK31', ['HV1','HV2','TW3','KB8'], ['HV-CD'], [],
         A('counts','CountShape','CountVs')+A('data','f0','n0','R1','CaseV','Vlen','Vn','VLe')+
         A('v2','UpperTheory.V.HV.cmDatum_char_two_adic_order_bounds')+A('vord','UpperTheory.V.HV.vsOrd')+
         A('vsfield','UpperTheory.V.HV.vsField')+A('countvs','UpperTheory.V.HV.countVs')),
        ('HV6', 'Literal CountIV on the prescribed actual cyclotomic layer', ['HV1','HV2'], [], [],
         A('layer','LayerLe','CountIV')+A('lchi','Lchi')+A('stmt','IsLayer')+
         A('ivfield','UpperTheory.V.HV.ivField')+A('countiv','UpperTheory.V.HV.countIV')+A('len','SumLe')),
        ('HV7', 'Exhaustive original case partition and the exact CaseV split', ['HV1'], [], [],
         A('data','CaseI','CaseZ','CaseII','CaseIII','CaseIV','CaseV')+
         A('cases','UpperTheory.V.HV.cases')+A('counts','CountV','CountVs')),
        ('HV8', 'Complete SumIn from CountII and CountV', ['HV1','HV4','HV5','HV6','HV7'], [], ['CountII','CountV'],
         A('counts','CountII','CountV')+A('layer','SumIn','PlusLe')+A('sumin','UpperTheory.V.HV.sumIn')),
        ('HV9', 'Complete SumOut from CountI, CountII and CountIII', ['HV1','HV4','HV7','CZ6'], [], ['CountI','CountII','CountIII'],
         A('counts','CountI','CountII','CountIII','CountZ')+A('layer','SumOut','PlusLe')+
         A('sumout','UpperTheory.V.HV.sumOut')),
        ('HV10', 'Full literal PointHV assembly from the four-count cut and immediate VWinAt propagation',
         ['HV5','HV6','HV8','HV9','CZ6','TW8','OB8','VW3','VW4'], [], remaining,
         A('layer','PointHV')+A('point','UpperTheory.V.HV.point')+
         A('join','pointHV_of_counts','thmHV_of_counts','jointWin_of_counts','vwin_of_counts')),
    ]
    raw = (HERE/'main.tex').read_bytes(); lines = raw.splitlines(keepends=True); claims = []
    for cid, title, deps, classical, retained, sources in specs:
        hits = [i for i, line in enumerate(lines) if line.startswith(('\\paragraph{'+cid+':').encode())]
        assert len(hits) == 1, cid
        a = hits[0]; b = next(i for i in range(a, len(lines)) if lines[i].strip() == b'\\end{proof}')
        frag = b''.join(lines[a:b+1])
        loc = {'file':'point_hv_assembly/main.tex','line_start':a+1,'line_end':b+1,'sha256':sha(frag),'bytes':len(frag)}
        status = ('Complete human proof of the stated implication; the exact count hypotheses listed below remain.'
                  if retained else 'Complete human proof in the stated scope, relative to the named classical inputs and previously proved suppliers.')
        claims.append({'id':cid,'title':title,'status':status,'depends_on':deps,'mathematical_dependencies':deps,
                       'classical_inputs':classical,'remaining_inputs':retained,'remaining_bespoke_inputs':retained,
                       'component_ledger':'point_hv_assembly/provenance.json','proof_location':loc,'human_proof':loc,'sources':sources})
    files = [{'path':PATHS[key],'sha256':sha(data),'bytes':len(data),'lines':len(data.splitlines()),
              'url':REPO+'/blob/'+PIN+'/'+PATHS[key],'verified_equal_to_pinned_git_blob':True}
             for key, data in cache.items()]
    validation = {'main_tex_sha256':sha(raw),'claim_count':len(claims),
                  'source_links':sum(len(c['sources']) for c in claims),'source_files':len(files),
                  'all_sources_equal_pinned_git_blobs':True,'all_source_and_proof_range_hashes_recorded':True,
                  'kernel_replay':False,'full_lean_build':False,'pdf_generated':False}
    boundary = {'bespoke_inputs':remaining,'classical_inputs':['HV-CYC','HV-CD'],
                'not_supplied':['The actual four count theorems','The residual symplectic model, image, rigidity or automorphy suppliers',
                                'Actual common arithmetic family/gap','Genuine theta/local installation and denominator tables',
                                'Exact metric/spectral comparisons','A complete human proof of RH or Dirichlet GRH']}
    ledger = {'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.26','date':'2026-11-22',
              'repository':REPO,'commit':PIN,'component':'point_hv_assembly','main_tex_sha256':sha(raw),
              'scope':'Complete literal CountVs and CountIV; complete original-field four-count implication to PointHV and the existing cohomological window endpoint.',
              'claims':claims,'source_files':sorted(files,key=lambda f:f['path']),
              'mathematical_dependency_graph':{c['id']:c['depends_on'] for c in claims},
              'classical_input_registry':'point_hv_assembly/classical_inputs.json','component_input_boundary':boundary,'validation':validation}
    write('provenance.json',ledger); write('source_hashes.json',{'commit':PIN,'files':files}); write('verification.json',validation)
    classical = {'schema':'rh-classical-input-registry/1','artifact_version':'0.26','component':'point_hv_assembly','accessed':'2026-11-22',
      'inputs':[
       {'id':'HV-CYC','name':'Elementary cyclotomic local-field background','author':'J. S. Milne','title':'Algebraic Number Theory',
        'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','version':'3.08','year':2020,
        'theorem_reference':'Proposition 6.2 and the local-field theory in Chapter 7; the required Eisenstein and index argument is written in HV2.',
        'accepted_statement':'Finite cyclotomic extensions and their Galois actions; uniqueness of a local valuation and the usual original-place decomposition groups.',
        'web_source_refs':['turn590417141view0'],
        'exact_specialization':'For K/Q_ell of degree <=b, the actual cyclotomic image has index <=b. The finite-level surjectivity, compact inverse-limit step and valuation bound 1+v_ell(a)+v_ell(e)<=3be are proved in HV2.'},
       {'id':'HV-CD','name':'Abelian conductor-discriminant formula already matched in TW-CD','author':'Romyar Sharifi','title':'Iwasawa Theory, Chapter 4',
        'url':'https://math.ucla.edu/~sharifi/notes/iwasawa-ch04.html','theorem_reference':'Equation (4.2.1)',
        'accepted_statement':'The absolute discriminant of an abelian number field is the product of the conductors of its characters.',
        'web_source_refs':['turn590417141view1'],
        'exact_specialization':'The actual field F=ker(psi) intersect ker(cyc mod ell) lies in Q(mu_(ell N)), so Delta_F <= (ell N)^[F:Q]. This is used only in HV5.'}],
      'inherited_classical_boundary':['TW3 and KB8 retain their precisely matched finite duality and K-theory leaves','TW8, OB8 and VW3/VW4 retain their existing inputs in the immediate window corollary'],
      'not_assumed':['CountVs','CountIV','redAll or its exact lossAll formula','An integral semisimplicity assertion','A prime-to-ell degree condition at exceptional primes','An auxiliary-only field/coefficients comparison','PointHV or its sum/layer assembly']}
    write('classical_inputs.json', classical)
    closure = {'artifact_version':'0.26','component':'point_hv_assembly','commit':PIN,'main_tex_sha256':sha(raw),'claims':[c['id'] for c in claims],
      'closed_bespoke_interfaces':[
       {'interface':'UpperTheory.V.HV.CountVs','supplied_by':'HV5','source':anchor('counts','CountVs'),
        'scope':'Full CountShape statement; exponent depending only on chi before every host, cutoff, closure, prime, coefficient and character.'},
       {'interface':'UpperTheory.V.HV.CountIV','supplied_by':'HV6','source':anchor('layer','CountIV'),
        'scope':'Full unweighted strict-Selmer layer comparison, every original layer model and coefficient ring, without a character parity assumption.'},
       {'interface':'CountI and CountII and CountIII and CountV imply PointHV','supplied_by':'HV10','source':anchor('join','pointHV_of_counts'),
        'scope':'Full original-field assembly, with CountVs and CountIV supplied here and CountZ supplied by CZ6; the four actual count predicates remain.'}],
      'remaining_bespoke_inputs':remaining,'classical_inputs':['HV-CYC','HV-CD'],
      'exact_binding_notes':['Same original CM E, algebraic closure and all LData records',
       'Pure-twist inertia vanishing descends to the exact source GS quotient',
       'The psi-inverse quotient action is retained in both global and local restriction-inflation',
       'Integral character filtration includes every prime dividing the field degree',
       'Direct polynomial error replaces the combined redAll/lossLe route; no claim of the exact source lossAll formula',
       'Exceptional-prime error is polynomial and nonexceptional-prime error is zero',
       'All character lengths proved finite before normalized inequalities',
       'LayerLe is exactly an unweighted strict Selmer bound, not an H2 bound',
       'One C and two prime thresholds after chi and the whole layer-index function but before every host and field'],
      'does_not_close':boundary['not_supplied']}
    write('closure.json',closure)
    report = ['POINT-HV ASSEMBLY -- VERSION 0.26', ledger['scope'], '',
              'Full suppliers: HV5 = CountVs; HV6 = CountIV.',
              'Complete implication: CountI + CountII + CountIII + CountV => PointHV => existing VWinAt endpoint.',
              'The four count hypotheses remain substantive; no global family, gap or metric/spectral obligation is removed.',
              '',json.dumps(validation,indent=2)]
    (HERE/'report.txt').write_text('\n'.join(report)+'\n')
    print(json.dumps(validation,indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--repo',type=Path,default=HERE.parent.parent/'lean-source')
    main(parser.parse_args().repo.resolve())
