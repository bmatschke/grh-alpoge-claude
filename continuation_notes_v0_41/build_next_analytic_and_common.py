#!/usr/bin/env python3
"""Validate the v0.41 analytic/common continuation plan against exact bytes.

This builder makes no theorem claim and invokes no Lean command. It writes
only next_analytic_and_common_sources.json. Example (from any directory):
  python build_next_analytic_and_common.py --source LEAN_CHECKOUT \
      --human-root RELEASE_OR_BASELINE --peer-root CURRENT_WORK \
      --output-dir NOTE_DIRECTORY
A release containing every component can be supplied as --human-root alone.
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

# Inclusive source ranges; source tasks are not proof claims.
ANCHORS = [('A01', 'First ThDef3/DivDef3 and the stronger six-field DivRows3', 'src/Formalism/LocalToGlobal/Divisibility/DivisionCompatibleToSub2Indef2.lean', 233, 311), ('A02', 'divTied3_read: both outputs and the four extra second-output guards', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/DivisionCompatibleAtReadIdentifications.lean', 22, 46), ('A03', 'RowPk, eta, Over, Fits, Moved and ReadPk on the same objects', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ReadPk.lean', 75, 189), ('A04', 'etaOf, RationalReadingWithoutCongruence and full ReadL guard', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RowsRestWordColumnUnitBaseTupleAlt.lean', 273, 307), ('L01', 'Uniformizer/conjugate-place independence and the literal heckeLift construction', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsCoefficientLinearLiftDoubleCosetOperators.lean', 17, 152), ('L02', 'MtReal0, HeckeLift0, hLC/hKC, SplitK and the original baseC maps', 'src/Formalism/LocalToGlobal/NumberFieldFamilies/HeckeLift0.lean', 11, 81), ('L03', 'The eight actual MtInput fields, including rational preimages and integral generators', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', 96, 122), ('L04', 'exists_preimage_comb and heckeIntTw_base with original finite lattice generators', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeOperatorIntegralOnLatticeAtTwistedPlaces.lean', 13, 32), ('L05', 'Exact HeckeIntTw and operator intertwining predicates', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/UnitsLiftSpec.lean', 41, 80), ('L05b', 'GenHyp and coefficient common-overfield/local-bridge predicates', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/UnitsLiftSpec.lean', 286, 328), ('L06', 'ndSpec_exists: one coefficient extension and all its retained source premises', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SideRationalEigenData.lean', 119, 201), ('L07', 'Full original NdSpec: all maximal ideals, Psi/range/projection/action and twist/local bridges', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', 263, 332), ('L08a', 'Actual trPsi, character and original projection/intertwining transports', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/NonemptySpec.lean', 17, 64), ('L08b', 'nonempty_spec and its original lattice/action/coefficient premises', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/NonemptySpec.lean', 94, 209), ('L09', 'root_int and heckeStd0_base retain HeckeStdPlain and actual operator inputs', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HeckeStandardFactsOnLocalisationBase.lean', 205, 293), ('L10', 'NBuilt and NTrue: original full local constructor and packed equality', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/RingSpecNormalisedCharacterEq.lean', 446, 477), ('C01', 'Original HCAll/SchurAll/PetAll/SmAll/ActRep and nineteen-field Links.Inputs', 'src/Formalism/LocalToGlobal/IndefiniteReal/LinksStage.lean', 240, 309), ('C02', 'PrimIn.TiesA/TiesG and the distinct four-field PrimIn.Inputs', 'src/Development/AbelianVarietyTheory/Definitions/Divisors/TwistedPlacesOfCondition.lean', 91, 123), ('C03', 'hcFinite versus schur_multMap/schurMult: separate suppliers and exact pair identities', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/HcFiniteAndSchurMult.lean', 110, 198), ('C04', 'L2 lift and full Sobolev/closable-pair bounded-function Schur endpoint', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SchurLemmaEquivariantPairBoundedFunctions.lean', 17, 130), ('Q01', 'link_alt: exact quantitative spectral inputs and same selector/instance ties', 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/LinkAlt.lean', 16, 48), ('Q02', 'classSel: one construction class and selector from coupled RowL/ExBL', 'src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean', 14, 28), ('Q03', 'shapeWin: common selected objects and exact nested target-class restriction', 'src/Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean', 27, 49), ('Q04', 'nonempty_hyps_of_allRows: coupled original selector, row and numerical premises', 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/NonemptyHypsOfAllRows.lean', 14, 96), ('O01', 'Original Frame FinLevel/Neat/Free and actual Sp/Ord', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/ContinuousTorusCharacter.lean', 162, 230), ('O02', 'finU: actual section-patching and finite-level producer', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/OrdinaryHeckeCharacters/FuCmpMem.lean', 17, 195), ('O03', 'Identity-form finite-class application and exact UA projections', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/DefiniteUnitaryClassSetFinite.lean', 250, 293), ('O04', 'Finite-quotient periodicity and complete ordinary module', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/OrdinaryHeckeCharacters/OrdFree.lean', 66, 245), ('O05', 'ordStruct: one factorial-limit projector, filtration and finite freeness', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/OrdinaryHeckeCharacters/OrdFree.lean', 295, 437), ('O06', 'ordFree: all positive-monoid operators', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/OrdinaryHeckeCharacters/OrdFree.lean', 441, 481), ('O07', 'ordBC: original coefficientwise map for arbitrary local CNL change', 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeckeAlgebras/OrdinaryHeckeCharacters/OrdBCMapOrd.lean', 198, 232), ('F301', 'Finite prime set, fixed good bridge and one bound before all X,j', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/LocalBridgesAtPlacesOverResidueCharOfLargeCoeff.lean', 15, 62), ('F302', 'Every original LocBridge field', 'src/Formalism/SharpRestriction/LevelLetterCocycles/DataNLoc.lean', 574, 591), ('F303', 'exists_locBridge: fixed embedding before every larger LL', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 303, 325), ('F304', 'Embedding matched to the original valuation prolongation', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 36, 75), ('F305', 'Dense image and equality of normalized absolute values', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 77, 130), ('F306', 'Isometric extension and uniqueness on the dense image', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 132, 165), ('F307', 'Finite local field generated by the global image and its closure', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 171, 203), ('F308', 'Exact Galois kernel and restriction to the original global closure', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 213, 241), ('F309', 'Full decomposition-group equivalence and both topology directions', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/FiniteDimensionalAdjoinRange.lean', 243, 299), ('F310', 'Finite root extension and its universal larger-field inclusion', 'src/Development/AutomorphicArithmetic/CyclotomicBounds/FiniteDimensionalRoots.lean', 13, 51), ('F311', 'Conjugacy of valuation prolongations: exact wrapper still to reconstruct', 'src/ReciprocityTheory/GaloisValuations/Global.lean', 337, 343), ('F312', 'Literal GoodCoef conductor/root condition', 'src/Formalism/LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean', 28, 28), ('F401', 'Full uniform exists_twRing_of_large, actual codRestriction and comparisons', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsTwistRingMapLargeCoefficientRings.lean', 8, 31), ('F402', 'Reads, one finite-image phi and exact original comparison transports', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/SameTwistOfOneField.lean', 14, 83), ('F403', 'Finite integral extension into C_ell and monic-polynomial bound', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/VLeOne.lean', 8, 57), ('F404', 'The original DVR equals the pulled-back unit ball', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/VLeOne.lean', 59, 120), ('F405', 'Number-field factorization and complete common-reading endpoint', 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/VLeOne.lean', 124, 184), ('F406', 'Unit-ball conjugacy via tensor-relation kernels', 'src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/PadicEmbeddingsConjugate.lean', 9, 96), ('F407', 'TwFrameC, full compatibility and ChoiceC including emb_side', 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ConcreteTwistFrameExtraExcludedOverSmallPrimes.lean', 133, 211), ('F408', 'NChoice finite DVR extension, fixed embedding and retained eMt data', 'src/Formalism/LocalRingCardinality/DataNChoice.lean', 12, 51)]

COMPONENTS = {'local_hecke_projection': ['HLP1', 'HLP2', 'HLP3', 'HLP4', 'HLP5', 'HLP6', 'HLP7', 'HLP8', 'HLP9', 'HLP10', 'HLP11', 'HLP12', 'HLP13', 'HLP14', 'HLP15', 'HLP16', 'HLP17', 'HLP18', 'HLP19', 'HLP20', 'HLP21', 'HLP22', 'HLP23', 'HLP24', 'HLP25', 'HLP26', 'HLP27', 'HLP28', 'HLP29', 'HLP30', 'HLP31', 'HLP32'], 'neat_levels': ['NTL17'], 'ordinary_theta_weight': ['OTW12', 'OTW13'], 'rational_theta': ['RTG2', 'RTG12', 'RTG18', 'RTG19', 'RTG20', 'RTG21', 'RTG24', 'RTG25'], 'local_theta_dictionary': ['LTD3', 'LTD4', 'LTD5', 'LTD6'], 'automorphic_realization': ['MR23', 'MR24', 'MR25', 'MR26'], 'finite_volume': ['FV1', 'FV2', 'FV3', 'FV4', 'FV9', 'FV11'], 'seed_boundedness': ['SBD16'], 'joint_harmonic_io': ['JIO19'], 'smooth_representatives': ['SPR13', 'SPR25'], 'row_integrability': ['RPI11', 'RPI12', 'RPI13', 'RPI14', 'RPI15'], 'division_identity': ['DI20', 'DI21'], 'comparison_packet': ['PKT21', 'PKT27', 'PKT30'], 'common_readings': ['RDR12', 'RDR20', 'RDR21', 'RDR22'], 'count_auxiliary_primes': ['CAP17'], 'selected_core': ['SCI13']}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def bind_component(directory: Path, name: str, wanted: list[str]) -> dict:
    data = (directory/'main.tex').read_bytes()
    lines = data.splitlines(keepends=True)
    provenance = json.loads((directory/'provenance.json').read_text())
    claims = provenance['claims']
    if isinstance(claims, dict):
        claims = list(claims.values())
    index = {c['id']: c for c in claims}
    files = []
    for filename in ['main.tex','provenance.json','closure.json','published_applications.json']:
        path = directory/filename
        if path.is_file():
            files.append(dict(file=f'{name}/{filename}',sha256=sha(path.read_bytes())))
    blocks = []
    for cid in wanted:
        claim = index[cid]
        loc = claim.get('proof_location') or claim.get('proof')
        lo,hi = loc['line_start'],loc['line_end']
        assert 1 <= lo <= hi <= len(lines), (name,cid,lo,hi)
        chunk = b''.join(lines[lo-1:hi])
        expected = loc.get('range_sha256') or loc.get('sha256')
        assert expected and sha(chunk) == expected, (name,cid,'proof hash mismatch')
        if loc.get('file_sha256'):
            assert loc['file_sha256'] == sha(data), (name,cid,'proof file mismatch')
        starts = [i+1 for i,line in enumerate(lines) if line.strip()==('% BEGIN '+cid).encode()]
        ends = [i+1 for i,line in enumerate(lines) if line.strip()==('% END '+cid).encode()]
        if starts or ends:
            assert starts == [lo] and ends == [hi], (name,cid,'proof marker mismatch')
        blocks.append(dict(id=cid,claim=cid,file=f'{name}/main.tex',line_start=lo,line_end=hi,
            sha256=sha(chunk),range_sha256=sha(chunk),proof_range_sha256=sha(chunk),
            proof_file_sha256=sha(data),range_bytes=len(chunk),
            verified_against_component_provenance=True,
            proof_markers_present=bool(starts)))
    return dict(component=name,files=files,claims=blocks,
        scope='Only the printed original conditional scope of each cited claim is used.')

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root','--source',dest='source_root',type=Path,required=True)
    ap.add_argument('--reconstruction-root','--human-root',dest='human_root',type=Path,required=True)
    ap.add_argument('--peer-root',type=Path)
    ap.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    args=ap.parse_args()
    sr=args.source_root.resolve(); hr=args.human_root.resolve(); out=args.output_dir.resolve()
    peer=args.peer_root.resolve() if args.peer_root else hr
    note=out/'next_analytic_and_common.txt'
    note_data=note.read_bytes()
    anchors=[]; cache={}
    assert len({x[0] for x in ANCHORS}) == len(ANCHORS)
    for aid,description,path,lo,hi in ANCHORS:
        if path not in cache:
            data=(sr/path).read_bytes()
            pinned=subprocess.run(['git','-C',str(sr),'show',PIN+':'+path],check=True,capture_output=True).stdout
            assert data == pinned, 'Source differs from pinned blob: '+path
            cache[path]=data
        data=cache[path]; lines=data.splitlines(keepends=True)
        assert 1 <= lo <= hi <= len(lines), (aid,lo,hi,len(lines))
        chunk=b''.join(lines[lo-1:hi])
        anchors.append(dict(id=aid,description=description,path=path,line_start=lo,line_end=hi,
            sha256=sha(data),file_sha256=sha(data),full_file_sha256=sha(data),range_sha256=sha(chunk),
            range_bytes=len(chunk),source_commit=PIN,verified_equal_to_pinned_git_blob=True,
            url=f'{BASE}{path}#L{lo}-L{hi}'))
    bindings=[]
    for name,claims in COMPONENTS.items():
        directory=peer/name
        if not (directory/'main.tex').is_file():
            directory=hr/name
        bindings.append(bind_component(directory,name,claims))
    flat_files=[item for b in bindings for item in b['files']]
    companions=[]
    for name in ['next_count_ii.txt','next_count_ii_sources.json',
                 'next_division_and_readings.txt','next_division_and_readings_sources.json']:
        path=out/name
        assert path.is_file(), path
        companions.append(dict(file=name,sha256=sha(path.read_bytes())))
    for stem in ['next_count_ii','next_division_and_readings']:
        m=json.loads((out/(stem+'_sources.json')).read_text())
        expected=m.get('note_sha256') or m.get('note_file_sha256')
        assert expected == sha((out/(stem+'.txt')).read_bytes()), (stem,'companion note hash mismatch')
    cited=set(re.findall(r'\b(?:A\d\d|C\d\d|L\d\d[a-z]?|O\d\d|Q\d\d|F3\d\d|F4\d\d)\b',note_data.decode()))
    assert cited <= {x['id'] for x in anchors}, ('unknown source labels',sorted(cited-{x['id'] for x in anchors}))
    validation=dict(all_source_blobs_equal_pinned_commit=True,all_ranges_within_files=True,
        all_proof_ranges_match_component_provenance=True,all_present_proof_markers_match_ranges=True,
        all_companion_note_hashes_match=True,all_cited_source_labels_bound=True,
        source_files=len(cache),source_ranges=len(anchors),component_count=len(bindings),
        component_files=len(flat_files),proof_blocks=sum(len(x['claims']) for x in bindings),
        no_new_proof_claims=True,no_new_published_applications=True,no_whole_leaf_closure=True,no_lean_replay=True)
    result=dict(schema='rh-continuation-source-audit/2',artifact_version='0.41',
        note=note.name,note_sha256=sha(note_data),note_file_sha256=sha(note_data),source_commit=PIN,
        status='Source-bound proposed work only; all cited completed claims retain their exact original hypotheses.',
        formal_proof_assumption='The pinned Alpoge-Claude Lean proof is accepted as fully checked and correct; no Lean replay.',
        scope='Completed HLP1-32; first priority original finU/ordStruct/ordFree/ordBC; parallel exact F3/F4; preserved PKT/RPI/RDR/RTG analytic, first-Div and eta boundaries.',
        range_convention='Inclusive 1-based LF-preserving byte ranges; exact existing component proof_location ranges, with BEGIN/END marker validation where present.',
        source_ranges=anchors,source_anchors=anchors,
        component_bindings=flat_files,human_proof_bindings=bindings,companion_bindings=companions,
        proposed_targets=[
            dict(id='finU_ordStruct_ordFree_ordBC',classification='B',status='open proposed human reconstruction',
                contract='Original all-QData/all-level finite-class factorization, complete ordinary projector and full coefficientwise CNL base change; exact original Frame and operators.',
                priority='first bounded workstream'),
            dict(id='F3_local_bridges',classification='B',status='open proposed human reconstruction',
                contract='Full original brAt_of_large, with fixed valuation embedding, actual topological decomposition-group equivalence, all LocBridge fields, GoodCoef and exact iqC; one bound before every X,j.',
                priority='bounded parallel target'),
            dict(id='F4_common_reading',classification='B',status='open proposed human reconstruction',
                contract='Full exists_twRing_of_large on supplied NChoice/TwFrameC/compatibility/ChoiceC; original complete C.Oe, phiK, TwAlgAt/TwRdAt/TwEmb; one base-image finite field before every X,j.',
                priority='bounded parallel target')],
        validation=validation,builder=dict(file=Path(__file__).name,sha256=sha(Path(__file__).read_bytes())))
    target=out/'next_analytic_and_common_sources.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'note_sha256':result['note_sha256'],'manifest_sha256':sha(target.read_bytes()),
        'builder_sha256':result['builder']['sha256'],'note_words':len(note_data.decode().split()),**validation},indent=2))

if __name__=='__main__':
    main()
