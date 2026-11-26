#!/usr/bin/env python3
"""Rebuild HX/ZW exact proof and source locators without a Lean replay."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
cache = {}
decl = re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def source(path, spelling):
    if path not in cache:
        data = subprocess.check_output(['git', '-C', str(args.repo), 'show', PIN + ':' + path])
        if (args.repo / path).read_bytes() != data:
            raise ValueError('Worktree differs from pin: ' + path)
        cache[path] = data
    data = cache[path]
    lines = data.splitlines(keepends=True)
    pat = re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+' + re.escape(spelling) + r'(?=\s|\(|\{|:|$)')
    starts = [i for i, line in enumerate(lines) if pat.search(line.decode())]
    if len(starts) != 1:
        raise ValueError((path, spelling, starts))
    start = starts[0]
    end = next((j for j in range(start+1, len(lines)) if decl.search(lines[j].decode())), len(lines))
    raw = b''.join(lines[start:end])
    return dict(path=path, declaration=spelling, source_spelling=spelling,
                line_start=start+1, line_end=end, sha256=sha(data),
                range_sha256=sha(raw), range_bytes=len(raw),
                first_line=lines[start].decode().rstrip(),
                role='Exact source definition or implication reconstructed in the written proof',
                verified_equal_to_pinned_git_blob=True,
                url=URL+path+f'#L{start+1}-L{end}')

A = 'src/Development/AutomorphicArithmetic/'
F = 'src/Formalism/'
S = A + 'ShortNorms/'
C = A + 'CharacterBoxes/'
P = A + 'PrimitiveCosets/'
R = F + 'RankGapBounds/'
W = F + 'SizeWindowBrackets/'

specs = {
 'host_window_installation': [
  ('HX1', 'SmallOne from the least-prime theorem with the constant absorbed', [],
   [(S+'ShortNorm.lean','SmallOne')],
   ['Xylouris, Acta Arithmetica 150 (2011), Theorem 1.1; residue 1, modulus N>=2, gcd(1,N)=1; fixed constant absorbed into the exponent.']),
  ('HX2', 'Exact ranks and admission on the prescribed arithmetic frame', ['AH18','SZ13','HC4'],
   [(A+'CoprimeRanks/AdmChi.lean','admissible_ranks_of_CMDatum'),(A+'CoprimeRanks/AdmChi.lean','admissibleClassesTwistedChar')], []),
  ('HX3', 'Complete matching of the original host-completion inputs',
   ['HX1','HX2','QR25','QP23','QP24','HC1','HC2','HC5','HC6','HC7','HC8','HC9'],
   [(S+'hostOfFieldOf.lean','UpperTheory.T3.hostOfFieldOf'),(S+'levelData.lean','UpperTheory.T3.levelData'),(C+'PairGood.lean','PairGood'),(S+'hostOfFieldOf.lean','hof_thick'),(S+'hostOfFieldOf.lean','hof_box')], []),
  ('HX4', 'Literal VWinAt(psi,401) to HostExW on the same target field and pair',
   ['HX1','HX2','HX3','AH18','QP22','QP25'],
   [(S+'supplyOfAdmOf.lean','UpperTheory.T3.supplyOfAdmOf'),(C+'SupplyChi.lean','UpperTheory.Top.supplyChi'),
    (C+'WinPairs.lean','UpperTheory.Top.winPairs'),(C+'TwistForm.lean','KerChi'),(C+'TwistForm.lean','TwistForm'),(C+'TwistForm.lean','WinDatum'),
    (C+'ExistsPageN.lean','VVle'),(C+'ExistsPageN.lean','IsChiField'),(C+'ExistsPageN.lean','VWinAt'),(C+'ExistsPageN.lean','VVle.mono'),
    (C+'BoundedTw.lean','UpperTheory.Top.boundedTw_key'),(C+'BoundedTw.lean','UpperTheory.Top.boundedTw'),
    (F+'SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean','EAtH'),
    ('src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ThinScalesIffHostBound.lean','HostExW')], [])
 ],
 'tied_window_completion': [
  ('ZW1', 'Literal ChainTied supplies the original-host CoreAtH record', [],
   [(P+'LevelGmLeOnFamilyScales.lean','tiedCore_of_chainTied'),(P+'CoreAtH.lean','CoreAtH'),(P+'WindowInequalityOfArtinInputs.lean','FamCoreConstantBounds'),
    (F+'SharpRestriction/GlobalSchurBounds/TieGlobal.lean','ChainTied'),(F+'SharpRestriction/GlobalSchurBounds/TieGlobal.lean','TieArith'),(W+'SChain.lean','SizeData₂')], []),
  ('ZW2', 'Complete pointwise finite weighted-slope ledger inequality', [],
   [(R+'MeanBoundSecondForm.lean',n) for n in ['Data','HidaSetting','DIV','HComp','Slopes','SlopeIneq','HHBound','FParams','Vvar']]
   +[(W+'QuotientSlopeBoundsWith.lean',n) for n in ['Lo5','QuotientSlopeBoundsWith','EComp5','Count5','LossBounds','MLo5','UBar5','ErrX5at']]
   +[(W+'ChainSlopeWindows/LevelOfCongruence.lean','each_unit_bound_statement'),(R+'RankGapProofs/WeightedMeanData.lean','phi_bound')], []),
  ('ZW3', 'Uniform error absorption by an explicit 200R cubed bound', ['ZW2'],
   [(W+'ErrorFormsWeakWindowsFalse.lean',n) for n in ['ErrText','CErr','ConstsBound','ErrWindows0','ErrWindows','LargeX']]
   +[(W+'QuotientSlopeBoundsWith.lean','ErrX5at')], []),
  ('ZW4', 'Complete original tied-family to fixed-target window implication',
   ['ZW1','ZW2','ZW3','WB1','WB2','WB3','WB4','WB5','WB6','WB7','WB8','SC1','AN3'],
   [(A+'DedekindLFunctions/LandauTheorems/ChTop.lean','ch_top_main_eq'),(A+'DedekindLFunctions/LandauTheorems/ChTop.lean','ch_top'),
    (P+'CoreGm.lean','UpperTheory.Comparison₂.core_gm'),(P+'WindowInequalityOfArtinInputs.lean','windowInequality_of_artinInputs'),
    (P+'LevelGmLeOnFamilyScales.lean','level_gm_le_on_family_scales'),(C+'ZeroFreeAllOfTopG.lean','eFamC_of_cls'),(C+'ZeroFreeAllOfTopG.lean','zeroFreeAll_of_topG'),
    (F+'SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean','ChebyshevInequalityAtWindowScale'),
    (F+'SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean','level_of_tiedWin')], [])
 ]
}

for component, records in specs.items():
    main = ROOT / component / 'main.tex'
    text = main.read_bytes()
    lines = text.splitlines(keepends=True)
    claims = []
    for cid, title, deps, refs, classical in records:
        if cid.startswith('ZW'):
            first = next(i+1 for i, line in enumerate(lines) if line.decode().strip() == '% BEGIN '+cid)
            last = next(i for i, line in enumerate(lines) if line.decode().strip() == '% END '+cid)
        else:
            first = next(i for i, line in enumerate(lines) if line.decode().startswith('\\paragraph{'+cid+':'))
            last = next((i for i in range(first+1,len(lines)) if lines[i].decode().startswith('\\paragraph{')),len(lines))
        raw = b''.join(lines[first:last])
        scope = ('The exact original VWinAt target, field, prime-pair and cohomological hypotheses; no VWinAt or DesignExists existence is asserted.'
                 if cid.startswith('HX') else
                 'The supplied literal ChainTied arithmetic ledger on one original family; complete numerical implication with exact exponent, not an arithmetic producer.')
        remaining = (['Literal VWinAt(psi,401) for the target; matched classical prime-pair leaves inherited in their exact scopes.'] if cid=='HX4' else
                     ['One literal ChainTied and EFamC on the same family, with fixed eD/eL before epsilon.'] if cid=='ZW4' else [])
        claims.append(dict(id=cid,title=title,introduced_in='0.30',classification='A' if cid=='HX1' else 'B',
                           status='Complete human proof of the stated exact conditional implication',scope=scope,depends_on=deps,
                           remaining_inputs=remaining,classical_inputs=classical,
                           source_relation=('Independent numerical simplification at the exact source interface' if cid=='ZW3' else 'Exact source contract with full human proof'),
                           proof_location=dict(file=component+'/main.tex',paragraph=cid,label='claim:'+cid if cid.startswith('ZW') else None,
                                               line_start=first+1,line_end=last,sha256=sha(raw),bytes=len(raw)),
                           sources=[source(*ref) for ref in refs],component_ledger=component+'/provenance.json'))
    paths = sorted({s['path'] for c in claims for s in c['sources']})
    out = dict(schema='rh-human-component-provenance/1',artifact_version='0.30',date='2026-11-22',commit=PIN,
               repository=URL.split('/blob/')[0],component=component,claims=claims,
               main_tex_sha256=sha(text),source_files=[dict(path=p,sha256=sha(cache[p]),bytes=len(cache[p]),line_count=len(cache[p].splitlines()),
                                                         verified_equal_to_pinned_git_blob=True) for p in paths],
               validation=dict(source_files=len(paths),claim_source_ranges=sum(len(c['sources']) for c in claims),
                               exact_pinned_git_bytes=True,proof_hashes_bound_to_current_text=True,new_lean_replay=False))
    (main.parent/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (main.parent/'source_locators.txt').write_text('\n'.join(c['id']+' '+s['url'] for c in claims for s in c['sources'])+'\n')
    print(component, len(claims), 'claims;', len(paths), 'source files')
