#!/usr/bin/env python3
"""Record exact pinned source ranges for the closed character/window bridge."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

def sha(data):
    return hashlib.sha256(data).hexdigest()

cache = {}
files = {}
decl_rx = re.compile(r'^\s*(?:(?:private|protected|noncomputable)\s+)*(?:theorem|lemma|def|abbrev|structure)\s+([^\s(:{]+)', re.M)

def source(path, name, role='literal conclusion or substantive supplier'):
    if path not in cache:
        data = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
        assert (repo/path).read_bytes() == data
        cache[path] = data
        files[path] = {'path':path, 'sha256':sha(data), 'bytes':len(data),
                       'lines':len(data.splitlines()), 'url':URL+path}
    data = cache[path]
    text = data.decode()
    matches = list(decl_rx.finditer(text))
    hit = [i for i,m in enumerate(matches) if m.group(1) == name]
    assert len(hit) == 1, (path,name,hit)
    j = hit[0]
    # Do not absorb blank lines before the declaration into the anchor.
    begin = text.rfind('\n',0,matches[j].start(1))+1
    end = matches[j+1].start() if j+1<len(matches) else len(text)
    while end>begin and text[end-1]=='\n': end-=1
    end = text.find('\n',end)+1 if text.find('\n',end)>=0 else len(text)
    lo = text.count('\n',0,begin)+1
    hi = text.count('\n',0,end)
    if end and text[end-1]!='\n': hi+=1
    raw = b''.join(data.splitlines(keepends=True)[lo-1:hi])
    link = URL+path+f'#L{lo}-L{hi}'
    return {'path':path,'declaration':name,'source_spelling':name,
            'line_start':lo,'line_end':hi,'sha256':sha(data),
            'full_file_sha256':sha(data),'range_sha256':sha(raw),'range_bytes':len(raw),
            'first_line':raw.decode().splitlines()[0],
            'declaration_lines_within_range':[lo], 'url':link,'pinned_url':link,
            'role':role,'verified_equal_to_pinned_git_blob':True}

F='src/Formalism/SizeWindowBrackets/'
C='src/Development/AutomorphicArithmetic/PrimitiveCosets/'
D='src/Development/AutomorphicArithmetic/DedekindLFunctions/'
H='src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/'
specs = {
 'WB1':[(F+'FirstPrimeNeSecondPrime.lean','cosetMean'),(F+'FirstPrimeNeSecondPrime.lean','primVal'),
        (F+'ChainSlopeWindows/StronglyIrreducible.lean','orthogonality_ramified'),
        (F+'ChainSlopeWindows/GaloisMapComplexConjugation.lean','primitive_value_primitive'),
        (C+'PrimInj.lean','UpperTheory.Comparison₂.prim_inj'),(C+'PrimRead.lean','UpperTheory.Comparison₂.prim_read')],
 'WB2':[(D+'SplitInertia.lean','HostFactsS'),(F+'FirstPrimeNeSecondPrime.lean','ASK'),
        (F+'FirstPrimeNeSecondPrime.lean','MAIN'),(F+'FirstPrimeNeSecondPrime.lean','De'),
        (D+'LandauTheorems/ChBalance.lean','ch_balance')],
 'WB3':[(F+'ChainSlopeWindows/LipschitzWeightAndMinimum.lean','psi_le_three'),
        (F+'ChainSlopeWindows/LipschitzWeightAndMinimum.lean','lipschitz_weight_all'),
        (F+'ChainSlopeWindows/LipschitzWeightAndMinimum.lean','derivative_integral_all'),
        ('src/Formalism/ZetaNonvanishing/GzLipschitz.lean','mertens_upper'),
        ('src/Formalism/ZetaNonvanishing/GzLipschitz.lean','mertens_lower')],
 'WB4':[(D+'SplitInertia.lean','SizesA'),(F+'SChain.lean','CostWindows'),
        (F+'GrowthBoundGivesRiemannHypothesis.lean','ThinScales'),
        (D+'LandauTheorems/ChCore.lean','sum_Th'),(D+'LandauTheorems/ChCore.lean','th_le'),
        (D+'LandauTheorems/ChCore.lean','core')],
 'WB5':[(D+'SplitInertia.lean','CharsA'),(D+'LandauTheorems/ChCore.lean','one_char'),
        (C+'TopsSum.lean','UpperTheory.Comparison₂.tops_sum'),
        (C+'CardPsiA.lean','card_PsiA_index'),(C+'charsA.lean','UpperTheory.Comparison₂.charsA')],
 'WB6':[(D+'LandauTheorems/ChCore.lean','ch_core'),
        (F+'ChainSlopeWindows/LipschitzWeightAndMinimum.lean','proposition_size_bound'),
        (C+'GmAEq.lean','UpperTheory.Comparison₂.gmA_eq'),
        (C+'SigALe.lean','UpperTheory.Comparison₂.sigA_le'),
        (C+'CoreGm.lean','UpperTheory.Comparison₂.core_gm')],
 'WB7':[(C+'CoreAtH.lean','CoreAtH'),(D+'SplitInertia.lean','IdentU'),
        (D+'LandauTheorems/ChTop.lean','ch_top_main_eq'),
        (D+'LandauTheorems/ChTop.lean','ch_top'),
        (C+'LevelGmLeOnFamilyScales.lean','tiedCore_of_chainTied')],
 'WB8':[(H+'TopWin.lean','tiedWin_of_ex'),(H+'TopWin.lean','exists_small_eps'),
        (H+'TopWin.lean','level_of_tiedWin'),
        (C+'LevelGmLeOnFamilyScales.lean','level_gm_le_on_family_scales'),
        ('src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean','UpperTheory.Top.shapeWin'),
        ('src/Main.lean','LFunction_ne_zero_of_half_lt_re')]
}
titles = [
 'Actual primitive-character reading and ramified Fourier orthogonality',
 'Exact asked-minus-main balance including the exceptional prime',
 'Elementary uniform regularity and weighted Lipschitz bounds',
 'Complete thick/thin subgroup averaging with coefficient d2/2',
 'Biased coset counts and uniform fixed-family signal extraction',
 'Scalar bound, actual retained-character identity and omitted tail',
 'Complete arithmetic input contract and exact ledger reindexing',
 'Uniform arithmetic contract implies RH and Dirichlet GRH'
]
deps = {'WB1':[], 'WB2':['WB1'], 'WB3':['WB1'],
        'WB4':['WB2','WB3'], 'WB5':['WB3'],
        'WB6':['WB1','WB4','WB5','SC1'],
        'WB7':['WB6'], 'WB8':['WB7','AN2','AN3','GH6']}
assumptions = {
 'WB1':['Finite abelian host with specified local inertia/Frobenius; an onto reciprocity reading is required for the primitive identification.',
        'The actual nonprincipal linear constants equal Lprime/L(1, primitive inducer).'],
 'WB2':['WB.6 HostFactsS and positive same-host weights; a common cutoff dominates every a/w.'],
 'WB3':['Only the defining bounded multiplicative coefficients and centered ramp normalization.'],
 'WB4':['The literal common data and numerical/ThinScales hypotheses WB.12.',
        'The actual arithmetic gap WB.13 on each translate of the same subgroup.'],
 'WB5':['WB.17 fixed-family coefficient and logarithmic-derivative bounds; actual coset shares WB.20 supply its Fourier bound.'],
 'WB6':['All WB4/WB5 premises on the same data; scalar sizes, gap E<=x^(C epsilon) B, actual retained family reading/exclusion, and omitted-ramp bounds.'],
 'WB7':['Existence of a simultaneous arithmetic family satisfying the four explicit contract items is retained.',
        'The source ledger bounds from SizeData2/ErrWindows/BNBoundsU are not supplied by reindexing them.'],
 'WB8':['The full WB7 contract for every sufficiently small epsilon on arbitrarily late windows, with C fixed before epsilon.',
        'The standard analytic leaves recorded in AN2/AN3/GH6: continuation, functional equations, Euler products, boundary nonvanishing, and elementary complex analysis.']
}
tex = (HERE/'main.tex').read_bytes()
claims=[]
for i,cid in enumerate(specs):
    begin=tex.index(('% BEGIN '+cid+'\n').encode())
    end=tex.index(('% END '+cid).encode(),begin)
    end=tex.index(b'\n',end)+1
    raw=tex[begin:end]
    loc={'file':'window_bridge/main.tex','section':cid,'sha256':sha(raw),'bytes':len(raw),
         'line_start':tex[:begin].count(b'\n')+1,'line_end':tex[:end].count(b'\n')}
    claims.append({'id':cid,'title':titles[i], 'status':'derived_simplification',
       'mathematical_status':'proved_under_explicit_hypotheses', 'introduced_in':'0.23',
       'depends_on':deps[cid], 'assumptions':assumptions[cid],
       'remaining_inputs':assumptions[cid] if cid in ('WB4','WB5','WB6','WB7','WB8') else [],
       'proof_location':loc,'sources':[source(*s) for s in specs[cid]],
       'component_ledger':'window_bridge/provenance.json'})
ledger={'schema':'rh-human-reconstruction-component/2','artifact_version':'0.23',
 'component':'window_bridge','repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
 'commit':PIN,'scope':'Closed implication from the literal same-object arithmetic gap/size/host contract to fixed positive character windows and RH/Dirichlet GRH; no construction of the contract is claimed.',
 'claims':claims,'source_files':list(files.values()),
 'mathematical_dependency_graph':deps,'proof_sha256':sha(tex),
 'validation':{'source_files_equal_pinned_git':True,'full_lean_build':False,'kernel_replay':False,
               'source_range_count':sum(len(c['sources']) for c in claims)}}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' '+c['title']+'\n'+
    '\n'.join(f"{s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}\n{s['url']}" for s in c['sources']) for c in claims)+'\n')
print(json.dumps({'claims':len(claims),'sources':len(files),'ranges':ledger['validation']['source_range_count'],
                  'proof_sha256':sha(tex)}))
