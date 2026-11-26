#!/usr/bin/env python3
"""Bind a bounded source-navigation note; this creates no mathematical claims."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=here.parents[1] / 'lean_source')
args = parser.parse_args()
repo = args.source.resolve()
pin = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
P = 'src/Development/AbelianVarietyTheory/Proofs/'
D = 'src/Development/AbelianVarietyTheory/Definitions/'
F = 'src/Formalism/LocalToGlobal/'
anchors = [
 ('S01','src/Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean',11,31,'topDesWin: exact ten-input cut and joined selection'),
 ('S02','src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean',27,49,'shapeWin: original target class and common family'),
 ('S03','src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean',14,28,'classSel: one class and RawSel with duties after all RowL joins'),
 ('S04',D+'GlobalTwisting/ColumnCompatibleSelection.lean',63,88,'Bundle and literal common-sigma projections'),
 ('S05a',D+'GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',190,200,'RecExP: dimension/scale choice before every compatible level'),
 ('S05b',D+'GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',250,295,'Built, QOf, IsSel, Row, pick and whole dependent-tuple transport'),
 ('S06',D+'GlobalTwisting/IsLinked.lean',27,86,'RPk, BTw, BWit, IsLinked and full BunU contract'),
 ('S07',D+'AutomorphicMembership/TwArgs.lean',27,56,'TwArgs: complete dependent package and exact original reading maps'),
 ('S08a',D+'AutomorphicMembership/ThetaChr.lean',35,74,'SPin, KPin and RecPin: original columns/theta/local package'),
 ('S08b',D+'AutomorphicMembership/ThetaChr.lean',102,116,'MemberE, WitExE, RecPinE and original prmR'),
 ('S09a',P+'IwasawaDecomposition/ExistsRowsOfHeqData.lean',117,218,'Original compatible column constructor and ColPins'),
 ('S09b',P+'IwasawaDecomposition/ExistsRowsOfHeqData.lean',257,359,'ReadC, exact TwArgs transport, exists_cols and cols_of_witnesses'),
 ('S10',P+'IwasawaDecomposition/LocalLanglandsPrmReduction.lean',43,84,'SelAll.bwit_exists: common Bundle and exact R preservation'),
 ('S11',P+'IwasawaDecomposition/ExistsSelectedRealization.lean',189,292,'Selected realization, actual evaluation and nP-normalized semilinear isometry'),
 ('S12',P+'IwasawaDecomposition/SelectedRealizationGeometric.lean',52,123,'RealIn preserving point, scalar, rational Sx and exponent maps'),
 ('S13',P+'IwasawaDecomposition/SelectedRealizationSide.lean',50,93,'RecIn and PartsRow on the same selected realization'),
 ('S14a',P+'IwasawaDecomposition/SelectedLowerMapHolds.lean',52,72,'Selected RowSideDetermined on the original RecT and division pair'),
 ('S14b',P+'IwasawaDecomposition/SelectedSideRealizationHolds.lean',120,148,'SelSideRT with the exact original host datum'),
 ('S15',P+'GlobalInterpolation/EtaSizeRecursion.lean',26,61,'Original linked existence: WitExE, ZetaCompatible and BunU to ExBL'),
 ('S16a',D+'GlobalTwisting/EventuallyAllScaleContextsAndOfBoth.lean',67,88,'RowL/ExBL and compatible strengthening/elimination'),
 ('S16b',P+'GlobalInterpolation/NonemptyHypsOfAllRows.lean',14,96,'Complete all-rows join before the common class/selector choice'),
 ('S17a',F+'ClassOfRecordOfChoice.lean',61,96,'Duty and real-place second layer using original T.theta.real/T.cols'),
 ('S17b','src/Formalism/SharpRestriction/GlobalTheoremInputs.lean',25,164,'Original LinkN/Eta/IRR/DIV/G/S/GLOBAL contracts'),
 ('S18',D+'AutomorphicMembership/RingSpecNormalisedCharacterEq.lean',446,478,'NBuilt and NTrue: retained original local constructor certificate'),
 ('S19',P+'IwasawaDecomposition/MtInputOf.lean',20,33,'Actual NBuilt record from one LC state and original Sp/Au/ss'),
 ('S20',P+'IwasawaDecomposition/FinitenessOfHyp.lean',40,80,'mtIn, original NTrue ntW and same local package'),
 ('S21',F+'IndefiniteReal/RationalAdjoints/RatZOfTests.lean',18,31,'Exact RowTest, LiftTest and two-clause LiftTestB definitions'),
 ('S22',P+'TwistedOperators/LiftTestBOfRatG.lean',25,75,'Original twisted FW basis coordinates give all base rational tests'),
 ('S23',P+'DivisorProofs/LiftTestsModularLatticeOfCoreCompatibility.lean',18,33,'Same TiesB/TiesG to LiftTest, LiftTestB and MLat'),
 ('S24',P+'DivisorProofs/ThetaLiftsOfRationalFormsRationalOfClauses.lean',25,38,'ratG_of_clauses: actual rationality producer and its three suppliers'),
 ('S25a',D+'Divisors/Params.lean',15,29,'TiesB: original arithmetic, model, phase, dimension and character fields'),
 ('S25b',D+'Divisors/TwistedPlacesOfCondition.lean',108,117,'TiesG: original FWTie, OMPins, phase, LUnif, IoExt, OneMap and CoverField'),
 ('S26',P+'DivisorProofs/PrimRows3OfParts.lean',24,50,'Complete primitive-row producer: all original type/level/positivity/decomposition inputs'),
]
def sha(x):
    return hashlib.sha256(x).hexdigest()
cache = {}
records = []
for sid, path, lo, hi, declaration in anchors:
    if path not in cache:
        data = (repo / path).read_bytes()
        pinned = subprocess.check_output(['git', 'show', f'{pin}:{path}'], cwd=repo)
        assert data == pinned, path
        cache[path] = data
    data = cache[path]
    lines = data.splitlines(keepends=True)
    assert 1 <= lo <= hi <= len(lines), (path, lo, hi, len(lines))
    block = b''.join(lines[lo-1:hi])
    records.append({'id':sid,'path':path,'declaration':declaration,
                    'line_start':lo,'line_end':hi,'file_sha256':sha(data),
                    'range_sha256':sha(block),'range_bytes':len(block),
                    'verified_equal_to_pinned_git_blob':True,
                    'url':f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{pin}/{path}#L{lo}-L{hi}'})
body=(here/'next_global_assembly_body.txt').read_text()
text=body+'\n\nSOURCE ANCHORS\n'
text+='Ranges are inclusive and preserve the original UTF-8 newlines. All source files\n'
text+='below equal the pinned git blobs. Group references S05, S08, S09, S14, S16,\n'
text+='S17 and S25 mean all correspondingly lettered entries.\n\n'
for r in records:
    text += f'[{r["id"]}] {r["declaration"]}\n{r["path"]}\n'
    text += f'Lines {r["line_start"]}–{r["line_end"]}\nFile SHA256 {r["file_sha256"]}\n'
    text += f'Range SHA256 {r["range_sha256"]}\n{r["url"]}\n\n'
(here/'next_global_assembly.txt').write_text(text)
manifest={'schema':'rh-source-navigation-note/1','artifact_version':'0.36',
          'source_commit':pin,'new_claims':[], 'selected_graph_changes':[],
          'note_file':'next_global_assembly.txt','note_sha256':sha(text.encode()),
          'body_sha256':sha(body.encode()),'source_files':len(cache),'source_ranges':len(records),
          'source_anchors':records,'formal_correctness_assumed':True}
(here/'next_global_assembly_sources.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS','note_sha256':manifest['note_sha256'],
                  'source_files':len(cache),'source_ranges':len(records)},indent=2))
