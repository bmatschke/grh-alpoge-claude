#!/usr/bin/env python3
"""Append reproducible pinned source locators to the bounded v0.37 handoff."""
from pathlib import Path
import argparse, hashlib, json, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
IW='src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
DE='src/Development/AbelianVarietyTheory/Definitions/'
GL='src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
AN=[
 ('N01','SelC.cols_of_witnesses: fixed reader before later arguments',IW+'ExistsRowsOfHeqData.lean',352,359),
 ('N02a','Original RPk, BTw, BWit and BunU',DE+'GlobalTwisting/IsLinked.lean',27,86),
 ('N02b','Same-record rpk_eq, realTB_eq and bwit_exists',IW+'LocalLanglandsPrmReduction.lean',43,84),
 ('N03','Original EvP, common construction and exact selection order',DE+'GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',1,None),
 ('N04','divTied3_read: first DivDef3 and separate stronger DivRows3',IW+'DivisionCompatibleAtReadIdentifications.lean',22,None),
 ('N05','Finite cardinality/index computation and pins_card_index_ranks',IW+'PinsCardIndexRanks.lean',14,None),
 ('N06','theta_eq_proj and rowSideDef3_both at the original two levels',IW+'RowSideDefinitionBothLevels.lean',22,None),
 ('N07a','Original composite_eq_lift from StepLev, TopLev and RowProj',IW+'CompositeIntertwinerEqThetaLiftGoodProjector.lean',23,None),
 ('N07b','Original inner-step level preservation',IW+'InnerThetaStepsPreserveFaceLevel.lean',21,None),
 ('N07c','Original terminal-step level preservation',IW+'LastThetaStepKeepsFaceLevel.lean',23,None),
 ('N07d','Original RowProj statement and supplier',IW+'RowProjHolds.lean',16,None),
 ('N08','Actual eW/jW, li/span/lattice and distinct theta square',IW+'LiftCuspFormSpaceThetaMapEqData.lean',19,None),
 ('N10','Original thin-size, host-gap and literal host/frame packet',IW+'StandardLatticesDiagonal.lean',17,294),
 ('N11','Original multiplicity nonzero support at every place',IW+'ExistsSelectedRealization.lean',238,248),
 ('N12','Five original part suppliers and finite PartsRec assembly',IW+'PartsRowOfEigensystemIndexGoodCharacters.lean',22,None),
 ('N13','Same-record RecIn with the exact logLam and good-character inputs',IW+'SelectedRealizationSide.lean',50,None),
 ('N14a','Original good-generic character/idempotent route',IW+'GeometricParameterOfReciprocity.lean',45,None),
 ('N14b','Base-embedding versus ray-reciprocity scalar route',IW+'ParameterOfDiscreteSeriesReciprocity.lean',46,None),
 ('N15a','Host pins from the original ray-field input',IW+'HostPlacesRayField.lean',16,None),
 ('N15b','HostDatumC with exactly the prescribed d3b',IW+'ExistsHostDatumOfPlaceData.lean',47,None),
 ('N16a','Original RatG to both rational-test clauses','src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/LiftTestBOfRatG.lean',25,75),
 ('N16b','Same TiesB/TiesG to LiftTest, LiftTestB and MLat','src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LiftTestsModularLatticeOfCoreCompatibility.lean',18,33),
 ('N16c','Original rationality producer and three clauses','src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ThetaLiftsOfRationalFormsRationalOfClauses.lean',25,38),
 ('N16d','Full original TiesB contract',DE+'Divisors/Params.lean',15,29),
 ('N16e','Full original geometric/field-descent TiesG contract',DE+'Divisors/TwistedPlacesOfCondition.lean',108,117),
 ('N17','Original primitive-row producer with all retained guards','src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/PrimRows3OfParts.lean',24,50),
 ('N18a','Original NBuilt and NTrue dependent certificate',DE+'AutomorphicMembership/RingSpecNormalisedCharacterEq.lean',446,478),
 ('N18b','Same LC-state MtInput/NBuilt construction',IW+'MtInputOf.lean',20,33),
 ('N18c','Original NTrue installation',IW+'FinitenessOfHyp.lean',40,80),
 ('N19','Duty and real second layer on literal theta.real/cols','src/Formalism/LocalToGlobal/ClassOfRecordOfChoice.lean',61,96),
 ('N20a','Exact selected topDesWin ten-input cut','src/Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean',11,31),
 ('N20b','Common class/selector from MemberE, ExBL and RowL','src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean',14,28),
 ('N20c','BunU with original remaining inputs to linked existence',GL+'EtaSizeRecursion.lean',26,61),
 ('N20d','All row predicates joined before the common selector',GL+'NonemptyHypsOfAllRows.lean',14,96),
]

def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=ROOT/'lean_source')
    ap.add_argument('--peer-root',type=Path,default=HERE.parent)
    args=ap.parse_args()
    note=HERE/'next_global_assembly.txt'
    marker='SOURCE AND PROOF ANCHORS FOLLOW'
    text=note.read_text().split(marker)[0]+marker+'\n\n'
    text+='Ranges are inclusive UTF-8 lines. Every source blob below was checked\nagainst the fixed commit. Group labels include all lettered entries.\n\n'
    out=[]
    for id,title,path,start,end in AN:
        b=(args.source/path).read_bytes()
        assert b==subprocess.check_output(['git','show',PIN+':'+path],cwd=args.source),path
        lines=b.splitlines(keepends=True)
        end=len(lines) if end is None else end
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        r=b''.join(lines[start-1:end])
        url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}'
        item={'id':id,'title':title,'path':path,'line_start':start,'line_end':end,
          'file_sha256':sha(b),'range_sha256':sha(r),'url':url,'pinned_blob_verified':True}
        out.append(item)
        text+=f'[{id}] {title}\n{path}\nLines {start}–{end}\nFile SHA256 {sha(b)}\nRange SHA256 {sha(r)}\n{url}\n\n'
    proofs=[]
    for id,component,label in [('P01','common_selected','CSR1–CSR22'),('P02','smooth_representatives','SPR1–SPR25; final SPR25 analytic gates'),('P03','count_first_order','CFO1–CFO21; selected same-Kap B1')]:
        f=args.peer_root/component/'main.tex'
        d=sha(f.read_bytes())
        proofs.append({'id':id,'file':component+'/main.tex','claims':label,'sha256':d})
        text+=f'[{id}] New human proof: {label}\n{component}/main.tex\nSHA256 {d}\n\n'
    note.write_text(text)
    manifest={'schema':'rh-continuation-source-locators/1','version':'0.37','source_commit':PIN,
      'note_file':'next_global_assembly.txt','note_sha256':sha(note.read_bytes()),
      'source_anchors':out,'new_proof_anchors':proofs,
      'status':'bounded proposed continuation only; no new proof or frontier closure'}
    (HERE/'next_global_assembly_sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'note_sha256':manifest['note_sha256'],'source_ranges':len(out),
      'pinned_files':len({x['path'] for x in out}),'words':len(text.split())},indent=2))

if __name__=='__main__':main()
