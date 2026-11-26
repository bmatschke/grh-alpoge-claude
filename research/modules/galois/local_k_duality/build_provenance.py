#!/usr/bin/env python3
"""Rebuild the exact local-K proof/source ledger at the pinned source commit."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
P = 'src/Development/WeilBound/CoreStatements/EulerCharacteristicCounts/'
PATHS = {
    'interface':'src/Formalism/GaloisCohomology/LocalTateDualityK.lean',
    'local':'src/Formalism/GaloisCohomology/StatementLoc.lean',
    'cochains':'src/ReciprocityTheory/GaloisValuations/SeparatedDvrSecondCohomologyMem.lean',
    'cups':'src/ReciprocityTheory/GaloisValuations/ContinuousConstSMulQuotient.lean',
    'dual':'src/ReciprocityTheory/Hypotheses/GalCohDefs.lean',
    'field':P+'GcohField.lean','mu':P+'GcohMu.lean','cmp':P+'GcohCmp.lean',
    'fin':P+'GcohFin.lean','tate':P+'GcohTate.lean','tateA':P+'GcohTateA.lean',
    'euler':P+'GcohEuler.lean','top':P+'GcohTop.lean','topE':P+'GcohTopEuler.lean',
}

def digest(b): return hashlib.sha256(b).hexdigest()
def write(name, value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main(repo):
    cache = {}
    for key, path in PATHS.items():
        b = (repo/path).read_bytes()
        assert b == subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+path]), path
        cache[key] = b

    def anchor(key, decl, start=None, end=None):
        b = cache[key]; lines = b.decode().splitlines()
        if start is None:
            pattern = re.compile(r'^(?:def|theorem|abbrev)\s+'+re.escape(decl)+r'(?=[\s:(])')
            hits = [i+1 for i,s in enumerate(lines) if pattern.match(s)]
            assert len(hits)==1,(key,decl,hits)
            start=hits[0]
        if end is None:
            end=len(lines)
            for i in range(start,len(lines)):
                if re.match(r'^(?:def|theorem|abbrev|end|section|namespace|variable|instance|attribute)\b|^@\[',lines[i]):
                    end=i;break
            while end>start and not lines[end-1].strip():end-=1
        frag=b''.join(b.splitlines(keepends=True)[start-1:end])
        return {'path':PATHS[key],'declaration':decl,'line_start':start,'line_end':end,
                'sha256':digest(b),'range_sha256':digest(frag),'range_bytes':len(frag),
                'first_line':lines[start-1], 'url':BASE+PATHS[key]+f'#L{start}-L{end}',
                'verified_equal_to_pinned_git_blob':True}

    classical = {
      'schema':'rh-classical-input-registry/1','artifact_version':'0.25','component':'local_k_duality',
      'accessed':'2026-11-22','inputs':[
        {'id':'LK-LF','name':'Finite extensions of complete discretely valued fields',
         'accepted_statement':'A finite extension of Q_l carries the unique extended absolute value, is complete, and has discrete valuation. The rank-d integral lattice and exact quotient cardinality are proved in LK1/LK4.',
         'author':'J. S. Milne','title':'Algebraic Number Theory','version':'3.08','year':2020,
         'theorem_reference':'Theorem 7.38; the degree/ramification interpretation is also Corollary 7.42.',
         'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','printed_pages':[123,124],
         'web_source_refs':['turn296800968view2','turn580072464view0'],
         'specialization':'Apply to the original finite K subset PadicAlgCl(l), with the restricted unique norm; no new field model or global completion is selected.'},
        {'id':'LK-TATE','name':'Finite local cohomology, local Tate duality and the local invariant',
         'accepted_statement':'For a characteristic-zero nonarchimedean local field, finite discrete continuous Galois modules have finite cohomology, vanish in degree >=3, and cup product with their multiplicative Tate dual gives perfect finite duality under the usual local Brauer invariant. Kummer and Hilbert 90 identify H2(mu_m) with Br(K)[m].',
         'author':'J. S. Milne','title':'Arithmetic Duality Theorems','edition':'second','year':2006,
         'theorem_reference':'I Theorem 2.1 and Corollary 2.3, together with the Kummer computation in the proof of Theorem 2.1 and the local class formation invariant of I 1.6(b).',
         'url':'https://jmilne.org/math/Books/ADTnot.pdf','printed_pages':[26,27,28],
         'web_source_refs':['turn134137816view0','turn588116592view0'],
         'errata_url':'https://www.jmilne.org/math/Books/add/ADT2006.pdf',
         'errata_checked':'2026-11-22; the cited correction concerning higher local fields is outside this finite extension of Q_l case.',
         'specialization':'R=Z/l^r, any finite nonfree R-module. LK1 identifies original cochains; LK3 writes the exact cyclotomic dual, H2 target, cochain cups and finite bidual argument, including the flipped H1 map.'},
        {'id':'LK-EULER','name':'Finite local Euler-Poincare formula',
         'accepted_statement':'For a finite discrete G_K module A of order q invertible in the local field K, |H0||H2|/|H1| = |O_K/q O_K|^(-1).',
         'author':'J. S. Milne','title':'Arithmetic Duality Theorems','edition':'second','year':2006,
         'theorem_reference':'I Theorem 2.8.','url':'https://jmilne.org/math/Books/ADTnot.pdf',
         'printed_pages':[31],'web_source_refs':['turn883385792view1','turn296800968view1'],
         'specialization':'K has residue characteristic l and [K:Q_l]=d. LK4 computes |O_K/q O_K|=q^d for q=|M|, without assuming M free. It includes l=2 and the zero module.'}
      ],
      'not_assumed':['Any unproved project-specific local-K predicate','Freeness of the finite coefficient module','Prime-to-residue-characteristic coefficient order','An infinite-level Selmer duality or global integral H2 comparison']}
    write('classical_inputs.json',classical)

    spec = [
      ('LK1','The specified local field, cyclotomic action and cochains',[],['LK-LF'],[
        anchor('local','GK'),anchor('interface','cycK'),anchor('interface','CycKSpec'),
        anchor('cochains','ContAction'),anchor('cochains','H0'),
        anchor('cochains','Z1/d0/B1/H1',42,66),anchor('cochains','Z2/d1/B2/H2',68,102),
        anchor('cochains','Cn/dn/Zn/Bn/Hn',104,126),
        anchor('field','integer_padic_eq'),anchor('field','card_quotient_padic'),anchor('field','isSepClosure_padic'),anchor('field','gcField'),
        anchor('mu','cycKSpec'),anchor('mu','gcMu'),anchor('cmp','gcRep'),anchor('cmp','gcn')]),
      ('LK2','Literal LocalFinitenessK',['LK1'],['LK-TATE'],[
        anchor('interface','LocalFinitenessK'),anchor('fin','locfin_of'),anchor('top','top_locfin')]),
      ('LK3','H2 invariant and all four literal local Tate cup bijections',['LK1','LK2'],['LK-TATE'],[
        anchor('interface','LocalTateDualityK'),anchor('dual','charRep'),anchor('dual','TDual'),anchor('dual','twDual'),
        anchor('dual','evalPair'),anchor('dual','cupH0H2TwistedDual'),anchor('dual','cup20'),anchor('dual','cupH1H1TwistedDual'),
        anchor('cups','cupCocycleZ1Z1'),anchor('cups','cupProductH1H1'),anchor('cups','cupCocycleH0Z2'),anchor('cups','cupProductH0H2'),anchor('cups','cupCocycleZ2H0'),anchor('cups','cupProductH2H0'),
        anchor('tateA','bij_transport'),anchor('tateA','bij_flip'),anchor('tateA','exists_dualEquiv'),
        anchor('tate','tate_core'),anchor('tate','tate_of'),anchor('top','top_tate')]),
      ('LK4','Literal residue-characteristic LocalEulerCharK',['LK1','LK2','LK3'],['LK-EULER'],[
        anchor('interface','LocalEulerCharK'),anchor('euler','exists_card_eq_pow'),anchor('euler','euler_of'),anchor('topE','top_euler'),anchor('field','card_quotient_padic')])]
    raw=(HERE/'main.tex').read_bytes(); lines=raw.splitlines(keepends=True)
    claims=[]
    for cid,title,deps,cin,anchors in spec:
        starts=[i for i,s in enumerate(lines) if ('\\begin{proposition}['+cid+':').encode() in s]
        assert len(starts)==1,cid
        a=starts[0];b=next(i for i in range(a,len(lines)) if lines[i].strip()==b'\\end{proof}')
        frag=b''.join(lines[a:b+1])
        proof={'file':'local_k_duality/main.tex','line_start':a+1,'line_end':b+1,'sha256':digest(frag),'bytes':len(frag)}
        claims.append({'id':cid,'title':title,
            'status':'Complete human proof of the exact interface specialization, relative only to the matched classical inputs.',
            'depends_on':deps,'mathematical_dependencies':deps,'classical_inputs':cin,
            'remaining_inputs':[],'remaining_bespoke_inputs':[],
            'component_ledger':'local_k_duality/provenance.json','proof_location':proof,'human_proof':proof,'sources':anchors})
    files=[{'path':PATHS[k],'sha256':digest(b),'bytes':len(b),'lines':len(b.splitlines()),'url':BASE+PATHS[k],
            'verified_equal_to_pinned_git_blob':True}for k,b in cache.items()]
    validation={'main_tex_sha256':digest(raw),'claim_count':len(claims),
                'source_files':len(files),'source_links':sum(len(c['sources'])for c in claims),
                'all_sources_equal_pinned_git_blobs':True,'all_source_and_proof_range_hashes_recorded':True,
                'full_lean_build':False,'kernel_replay':False,'pdf_generated':False}
    ledger={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.25','date':'2026-11-22',
            'repository':'https://github.com/CocoSgt/riemann-hypothesis-lean','commit':PIN,
            'component':'local_k_duality','main_tex_sha256':digest(raw),
            'scope':'Exact native finite LocalFinitenessK, LocalTateDualityK and LocalEulerCharK, for every prime and finite nonfree coefficient module. No global or infinite-level comparison is inferred.',
            'claims':claims,'source_files':sorted(files,key=lambda x:x['path']),
            'mathematical_dependency_graph':{c['id']:c['depends_on']for c in claims},
            'classical_input_registry':'local_k_duality/classical_inputs.json',
            'component_input_boundary':{'bespoke_inputs':[],'classical_inputs':['LK-LF','LK-TATE','LK-EULER'],
                'not_supplied':['Global integral-cohomology reduction','KBridge or LemmaK','ThmBab','PointHV','Infinite-level shaInv <= VLen comparison','Actual arithmetic family, RH or Dirichlet GRH']},
            'validation':validation}
    write('provenance.json',ledger)
    write('source_hashes.json',{'commit':PIN,'files':files})
    write('verification.json',validation)
    endpoints=[{'interface':'Formalism.GaloisCohomology.'+name,'supplied_by':cid,
                'source':anchor('interface',name),'scope':'Full literal quantifiers, including l=2, original K inside PadicAlgCl(l), arbitrary finite nonfree Z/l^r modules and continuous action.'}
                for name,cid in [('LocalFinitenessK','LK2'),('LocalTateDualityK','LK3'),('LocalEulerCharK','LK4')]]
    write('closure.json',{'artifact_version':'0.25','component':'local_k_duality','commit':PIN,
        'main_tex_sha256':digest(raw),'claims':[c['id']for c in claims],
        'closed_bespoke_interfaces':endpoints,'remaining_bespoke_inputs':[],
        'classical_inputs':['LK-LF','LK-TATE','LK-EULER'],'classical_input_registry':'local_k_duality/classical_inputs.json',
        'exact_binding_notes':['Original finite K and original PadicAlgCl(l)','Krull topology and explicit continuous cochain differentials',
            'Actual cycK, with no roots-of-unity containment assumption on K','Finite possibly nonfree R modules and actual twisted dual',
            'Source H1 cup has dual first','Cup bijections into original H2 target before applying invariant','Flipped H1 via finite biduality, valid at l=2',
            'Euler factor from O_K of rank [K:Q_l], not from coefficient freeness'],
        'safe_to_retire_in_stated_scope':['DA24-LK-01','DA24-LK-02','DA24-LK-03'],
        'does_not_close':ledger['component_input_boundary']['not_supplied'],
        'historical_claim_suppliers':{'ThmBab source hF':'LK2','ThmBab source hT':'LK3','LemmaK source hF':'LK2','LemmaK source hT':'LK3','Local Euler inputs':'LK4'}})
    print(json.dumps(validation,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=HERE.parent.parent/'lean-source')
    main(p.parse_args().repo.resolve())
