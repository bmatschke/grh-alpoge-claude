#!/usr/bin/env python3
"""Bind a continuation plan to pinned source and released proof bytes.

Usage: python build_next_analytic_and_common.py --source-root LEAN_CHECKOUT
         --reconstruction-root RELEASE_ROOT [--output-dir NOTE_DIRECTORY]
No Lean invocation, proof replay, source mutation or new theorem assertion.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
I = 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
D = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'

# Inclusive ranges; this is a source plan, not a new claim ledger.
ANCHORS = [
 ('A01', 'First ThDef3/DivDef3 and the stronger six-field DivRows3',
  'src/Formalism/LocalToGlobal/Divisibility/DivisionCompatibleToSub2Indef2.lean',233,311),
 ('A02', 'divTied3_read: both outputs and the four extra second-output guards',
  I+'DivisionCompatibleAtReadIdentifications.lean',22,46),
 ('A03', 'RowPk, eta, Over, Fits, Moved and ReadPk on the same objects',
  D+'ReadPk.lean',75,189),
 ('A04', 'etaOf, RationalReadingWithoutCongruence and full ReadL guard',
  D+'RowsRestWordColumnUnitBaseTupleAlt.lean',273,307),
 ('L01', 'Uniformizer/conjugate-place independence and the literal heckeLift construction',
  I+'ExistsCoefficientLinearLiftDoubleCosetOperators.lean',17,152),
 ('L02', 'MtReal0, HeckeLift0, hLC/hKC, SplitK and the original baseC maps',
  'src/Formalism/LocalToGlobal/NumberFieldFamilies/HeckeLift0.lean',11,81),
 ('L03', 'The eight actual MtInput fields, including rational preimages and integral generators',
  D+'RingSpecNormalisedCharacterEq.lean',96,122),
 ('L04', 'exists_preimage_comb and heckeIntTw_base with original finite lattice generators',
  I+'HeckeOperatorIntegralOnLatticeAtTwistedPlaces.lean',13,32),
 ('L05', 'Exact HeckeIntTw and operator intertwining predicates',
  I+'UnitsLiftSpec.lean',41,80),
 ('L05b', 'GenHyp and coefficient common-overfield/local-bridge predicates',
  I+'UnitsLiftSpec.lean',298,316),
 ('L06', 'ndSpec_exists: one coefficient extension and all its retained source premises',
  I+'SideRationalEigenData.lean',119,201),
 ('L07', 'Full original NdSpec: all maximal ideals, Psi/range/projection/action and twist/local bridges',
  D+'RingSpecNormalisedCharacterEq.lean',263,332),
 ('L08a', 'Actual trPsi, character and original projection/intertwining transports',
  I+'NonemptySpec.lean',17,64),
 ('L08b', 'nonempty_spec and its original lattice/action/coefficient premises',
  I+'NonemptySpec.lean',94,209),
 ('L09', 'root_int and heckeStd0_base retain HeckeStdPlain and actual operator inputs',
  I+'HeckeStandardFactsOnLocalisationBase.lean',205,293),
 ('L10', 'NBuilt and NTrue: original full local constructor and packed equality',
  D+'RingSpecNormalisedCharacterEq.lean',446,477),
 ('C01', 'Original HCAll/SchurAll/PetAll/SmAll/ActRep and nineteen-field Links.Inputs',
  'src/Formalism/LocalToGlobal/IndefiniteReal/LinksStage.lean',240,309),
 ('C02', 'PrimIn.TiesA/TiesG and the distinct four-field PrimIn.Inputs',
  'src/Development/AbelianVarietyTheory/Definitions/Divisors/TwistedPlacesOfCondition.lean',91,123),
 ('C03', 'hcFinite versus schur_multMap/schurMult: separate suppliers and exact pair identities',
  I+'HcFiniteAndSchurMult.lean',110,198),
 ('C04', 'L2 lift and full Sobolev/closable-pair bounded-function Schur endpoint',
  I+'SchurLemmaEquivariantPairBoundedFunctions.lean',17,130),
 ('Q01', 'link_alt: exact quantitative spectral inputs and same selector/instance ties',
  'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkAlt.lean',16,48),
 ('Q02', 'classSel: one construction class and selector from coupled RowL/ExBL',
  'src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean',14,28),
 ('Q03', 'shapeWin: common selected objects and exact nested target-class restriction',
  'src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean',27,49),
 ('Q04', 'nonempty_hyps_of_allRows: coupled original selector, row and numerical premises',
  'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/NonemptyHypsOfAllRows.lean',14,96),
]

COMPONENTS = {
 'seed_boundedness': ['SBD16'],
 'joint_harmonic_io': ['JIO19'],
 'smooth_representatives': ['SPR13','SPR25'],
 'finite_volume': ['FV11'],
 'row_integrability': ['RPI11','RPI12','RPI14','RPI15'],
 'division_identity': ['DI20','DI21'],
 'comparison_packet': ['PKT21','PKT27','PKT30'],
 'common_readings': ['RDR12','RDR20','RDR21','RDR22'],
 'local_theta_dictionary': ['LTD3','LTD4','LTD5','LTD6'],
}

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root',type=Path,required=True)
    ap.add_argument('--reconstruction-root',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    args=ap.parse_args()
    sr=args.source_root.resolve(); rr=args.reconstruction_root.resolve(); out=args.output_dir.resolve()
    note=out/'next_analytic_and_common.txt'
    anchors=[]; cache={}
    for aid,description,path,lo,hi in ANCHORS:
        if path not in cache:
            data=(sr/path).read_bytes()
            pinned=subprocess.run(['git','-C',str(sr),'show',PIN+':'+path],check=True,capture_output=True).stdout
            if data != pinned: raise AssertionError('Source differs from pinned blob: '+path)
            cache[path]=data
        data=cache[path]; lines=data.splitlines(keepends=True)
        if not 1 <= lo <= hi <= len(lines): raise AssertionError((aid,lo,hi,len(lines)))
        chunk=b''.join(lines[lo-1:hi])
        anchors.append(dict(id=aid,description=description,path=path,line_start=lo,line_end=hi,
            sha256=sha(data),file_sha256=sha(data),full_file_sha256=sha(data),range_sha256=sha(chunk),
            range_bytes=len(chunk),source_commit=PIN,verified_equal_to_pinned_git_blob=True,
            url=f'{BASE}{path}#L{lo}-L{hi}'))
    bindings=[]
    for name,claims in COMPONENTS.items():
        directory=rr/name; main_data=(directory/'main.tex').read_bytes(); lines=main_data.splitlines(keepends=True)
        files={}
        for filename in ['main.tex','provenance.json','closure.json','published_applications.json']:
            f=directory/filename
            if f.exists():
                h=sha(f.read_bytes()); files[filename]=dict(file=f'{name}/{filename}',sha256=h,file_sha256=h)
        blocks=[]
        for cid in claims:
            starts=[i for i,l in enumerate(lines) if l.strip()==('% BEGIN '+cid).encode()]
            ends=[i for i,l in enumerate(lines) if l.strip()==('% END '+cid).encode()]
            if len(starts)!=1 or len(ends)!=1 or starts[0]>=ends[0]: raise AssertionError((name,cid,starts,ends))
            lo,hi=starts[0]+1,ends[0]+1; b=b''.join(lines[lo-1:hi])
            blocks.append(dict(id=cid,line_start=lo,line_end=hi,proof_range_sha256=sha(b),proof_range_bytes=len(b)))
        bindings.append(dict(component=name,scope='Only the printed original conditional scope of the cited claims is used.',files=files,claims=blocks))
    companion=out/'next_division_and_readings.txt'
    companions=[]
    for p in [companion,out/'next_division_and_readings_sources.json']:
        if not p.exists(): raise FileNotFoundError(p)
        companions.append(dict(file=p.name,sha256=sha(p.read_bytes()),file_sha256=sha(p.read_bytes())))
    result=dict(schema='rh-continuation-source-audit/1',artifact_version='0.40',note=note.name,note_sha256=sha(note.read_bytes()),
        source_commit=PIN,status='Source-anchored proposed next work only; no new proof claim, published application or whole-leaf closure.',
        formal_proof_assumption='The pinned Alpoge-Claude Lean proof is accepted as fully checked and correct; no Lean replay.',
        scope='Complementary local Hecke/actual NdSpec and common analytic input installation after PKT; completed theta/RowPairInt/first DivDef3 retained; exact ReadL eta and stronger second DivRows3 kept separate.',
        range_convention='Inclusive 1-based lines; byte-exact LF-preserving splitlines(keepends=True), including BEGIN/END markers for proof blocks.',
        source_anchors=anchors,component_bindings=bindings,companion_bindings=companions,
        validation=dict(all_source_blobs_equal_pinned_commit=True,all_ranges_within_files=True,
            all_proof_markers_unique=True,source_files=len(cache),source_ranges=len(anchors),
            component_count=len(bindings),proof_blocks=sum(len(x['claims']) for x in bindings),
            no_new_proof_claims=True,no_lean_replay=True),
        builder=dict(file=Path(__file__).name,sha256=sha(Path(__file__).read_bytes())))
    target=out/'next_analytic_and_common_sources.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'note_sha256':result['note_sha256'],'manifest_sha256':sha(target.read_bytes()),**result['validation']},indent=2))

if __name__=='__main__':main()
