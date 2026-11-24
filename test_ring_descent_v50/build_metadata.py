#!/usr/bin/env python3
"""Bind the AllTest human proof to the pinned source without altering shared files."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.50'
COMPONENT = HERE.name
SNAP = ROOT / 'source_snapshot_v0_50' / 'geometry'
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
BASE = 'src/Development/AbelianVarietyTheory/Proofs/UnitaryExistence/'
TOR = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/'
EXT = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ExtensionDescent/'
PJ = 'src/Formalism/LocalToGlobal/ProjectiveLattices/'

# Each triple selects one exact, byte-bound primary-source range.
SOURCES = {
 'moduli': (TOR+'PushInvertible.lean',29,53,'Moduli, Coeff, and the actual base-changed moduli scheme'),
 'frames': (PJ+'IsCombAt.lean',44,124,'IsTanAt, IsEigAt, IsCombAt, PPx, FrPt and FrMap'),
 'test_rings': (PJ+'AlgebraMapCAt.lean',9,57,'TRing and the literal FromTest witness'),
 'all_test': (PJ+'AllTest.lean',1,None,'AllTest for all reduced coefficient algebras'),
 'section_bc': (EXT+'GlobalSectionsRankAlgClosed.lean',32,44,'SecBaseChangeSt: locally Noetherian original base, arbitrary coefficient ring'),
 'univ_defs': ('src/Development/AbelianVarietyTheory/Definitions/ExistenceOfLattices/UnivFrame.lean',14,None,'FrameRing, SecGen, SecBC, FrChg, OpenChart, UnivFrame'),
 'lie_eigen': (BASE+'ExistsIsLieBasisEigen.lean',266,None,'exists_isLieBasis_eigen and actual eigenmultiplicity construction'),
 'section_local': (BASE+'ExistsLocalGeneratorStableBaseChange.lean',39,None,'Stable local theta-section generator under every coefficient change'),
 'section_generator': (BASE+'FibreSectionGeneratesOfNowhereZeroNoetherianBase.lean',1,None,'Section generator on arbitrary pullbacks of the supplied universal object'),
 'base_change': (BASE+'ExistsFramedPointBaseChangeAlgebraMap.lean',25,None,'Exact arbitrary-ring tangent and section base change'),
 'change': (BASE+'FrameChangeExistsUniqueOfSamePoint.lean',22,None,'Unique coordinate matrices and unit between frames over the same point'),
 'change_exists': (BASE+'ExistsUniqueFrameChangeByMatrices.lean',15,None,'Existence of the changed actual frame for every invertible matrix and unit'),
 'injective_eq': (BASE+'FrameEqOfBaseChangeInjective.lean',18,None,'frPt_eq_of_frMap_injective with the original same-point hypothesis'),
 'eigen_charts': (BASE+'ExistsChartEigenframe.lean',83,None,'Actual affine eigenframe chart and theta section'),
 'open_charts': (BASE+'ExistsOpenChartFramedPointTestRing.lean',39,None,'Reduced test-ring chart carrying the actual reference frame'),
 'frame_ring': (BASE+'ExistsFrameRingOverTestRing.lean',33,None,'Explicit generic-matrix localization and full FrameRing universal property'),
 'univ_frame': (BASE+'ExistsUniversalFrameTestRing.lean',17,None,'exists_univFrame_testRing'),
 'classifies': (BASE+'UniversalFrameClassifiesFramedPoints.lean',23,None,'univFrame_classifies for arbitrary coefficient algebra'),
 'away': (BASE+'ExistsFgSubalgebraDescAway.lean',24,None,'Simultaneous finite coefficient capture in principal localizations'),
 'glue': (BASE+'FramedPointsGluePrincipalCover.lean',155,None,'Exact principal-cover gluing of the original framed-point record'),
 'moduli_descent': (BASE+'ModuliPointFromFgSubalgebra.lean',14,None,'point_from_fg_subalgebra and its actual-moduli application'),
 'local_descent': (BASE+'FramedPointReducedFromTestRing.lean',95,225,'Fixed chart cover, overlap equalities and local-to-global frame descent'),
 'fg_descent': (BASE+'FramedPointReducedFromTestRing.lean',227,269,'TestDescent.exists_fg_descent'),
 'radical': (BASE+'ReducedFiniteTypeIffTestRing.lean',12,None,'reduced_finiteType_iff_testRing'),
 'alltest_exit': (BASE+'FramedPointReducedFromTestRing.lean',276,290,'Frames.allTest_of_secBaseChange'),
 'principal_exit': (BASE+'CongrOfDvdModulus.lean',41,None,'Original pointwise FromTest field in exists_unf_hasPrinc'),
}
CLAIMS = [
 ('TDR1',[],['moduli','frames','lie_eigen'],['TDR_ORIGINAL_DATA','TDR_STANDARD_AG'],
  'Actual universal Lie eigenspaces and ordered frames over every coefficient algebra, including zero multiplicities and nonflat maps.'),
 ('TDR2',[],['moduli','section_bc','section_local','section_generator'],['TDR_ORIGINAL_DATA','TDR_SEC_BASE_CHANGE','TDR_STANDARD_AG'],
  'Actual theta direct-image line and all-algebra base change, using SecBaseChangeSt only on a locally Noetherian original base.'),
 ('TDR3',['TDR1','TDR2'],['frames','base_change','univ_defs'],[],
  'Literal unique FrMap, including dualMap, pullback projections and every appLE section equation.'),
 ('TDR4',['TDR1','TDR2','TDR3'],['change','change_exists','injective_eq'],[],
  'Unique row-coordinate GL matrices and unit scalar; equality under injective base change with the source same-point premise retained.'),
 ('TDR5',['TDR1','TDR2','TDR3','TDR12'],['eigen_charts','open_charts','moduli'],[],
  'Reduced finite-type affine open charts carrying actual ordered Lie eigenframes and the original theta-section generator.'),
 ('TDR6',['TDR3','TDR4','TDR5','TDR12'],['frame_ring','univ_frame','classifies','univ_defs'],[],
  'Explicit reduced universal frame algebra; full existence and uniqueness for every target coefficient algebra.'),
 ('TDR7',['TDR1','TDR2','TDR3','TDR6'],['univ_defs','frame_ring','classifies','moduli'],['TDR_STANDARD_AG'],
  'Human simplification: the literal framed-point functor represented by its actual Lie and theta frame bundles; all coefficient rings.'),
 ('TDR8',[],['away'],['TDR_STANDARD_ALGEBRA'],
  'One finitely generated subalgebra captures all finite localization maps and unit-ideal coefficients, with injective maps for arbitrary zero divisors.'),
 ('TDR9',['TDR1','TDR2','TDR3','TDR4'],['glue','local_descent'],['TDR_STANDARD_AG'],
  'Original frames glue on finite principal covers; same-point equality and actual section pullbacks retained.'),
 ('TDR10',['TDR8'],['moduli_descent','moduli'],['TDR_STANDARD_AG'],
  'Finite-coefficient descent for separated locally finite-type schemes; proves every actual moduli and frame-scheme instance needed here.'),
 ('TDR11',['TDR5','TDR6','TDR7','TDR8','TDR9','TDR10'],['fg_descent','local_descent'],[],
  'Complete original TestDescent.exists_fg_descent for every commutative coefficient algebra, including nonreduced and non-Noetherian rings.'),
 ('TDR12',[],['radical','test_rings'],['TDR_STANDARD_ALGEBRA'],
  'Exact radical-ideal finite-polynomial presentation, including the zero ring.'),
 ('TDR13',['TDR3','TDR11','TDR12'],['all_test','alltest_exit','test_rings','principal_exit'],[],
  'Complete original AllTest at SecBaseChangeSt; exact FrMap/FromTest triple and pointwise application to any already chosen complex frame family.'),
]

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

files = {}
sources = {}
for key,(path,a,b,declaration) in SOURCES.items():
    original=(repo/path).read_bytes()
    pinned=subprocess.check_output(['git','show',PIN+':'+path],cwd=repo)
    if original != pinned: raise SystemExit('Working source differs from pin: '+path)
    dest=SNAP/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(pinned)
    lines=pinned.splitlines(keepends=True)
    b=len(lines) if b is None else b
    if not 1<=a<=b<=len(lines): raise SystemExit('Invalid source range: '+key)
    data=b''.join(lines[a-1:b])
    url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+path
    files[path]={'path':path,'snapshot_file':str(dest.relative_to(ROOT)),
      'bytes':len(pinned),'sha256':sha(pinned),'file_sha256':sha(pinned),
      'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'url':url}
    sources[key]={'id':'TDR_SRC_'+key.upper(),'path':path,'declaration':declaration,
      'line_start':a,'line_end':b,'source_commit':PIN,'file_sha256':sha(pinned),
      'full_file_sha256':sha(pinned),'range_sha256':sha(data),'range_bytes':len(data),
      'snapshot_file':str(dest.relative_to(ROOT)),'verified_equal_to_pinned_git_blob':True,
      'url':url+f'#L{a}-L{b}'}

tex=(HERE/'main.tex').read_bytes()
text=tex.decode()
claims=[]
for ident,deps,groups,external,scope in CLAIMS:
    start=text.index('% BEGIN '+ident+'\n')
    end=text.index('% END '+ident+'\n',start)+len('% END '+ident+'\n')
    block=text[start:end].encode()
    title=re.search(r'\\paragraph\{'+ident+r'\. ([^\n]+)\}',text[start:end]).group(1)
    claims.append({'id':ident,'title':title,'introduced_in':VERSION,'classification':'B',
      'depends_on':deps,'external_input_ids':external,'scope_note':scope,'source_groups':groups,
      'sources':[sources[g] for g in groups],
      'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+ident,
        'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end),
        'sha256':sha(block),'bytes':len(block)},
      'source_proof_is_not_human_proof':True,'status':'written_pending_independent_review',
      'independent_review_files':[]})
common={'artifact_version':VERSION,'component':COMPONENT,'source_commit':PIN,
        'proof_file_sha256':sha(tex),'status':'written_pending_independent_review'}
dump('source_manifest.json',{'schema':'rh-pinned-source-manifest/1',**common,
  'source_repository':'https://github.com/CocoSgt/riemann-hypothesis-lean',
  'files':list(files.values()),'ranges':list(sources.values()),
  'file_count':len(files),'range_count':len(sources)})
dump('provenance.json',{'schema':'rh-human-component-provenance/1',**common,
  'main_tex_sha256':sha(tex),'claims':claims})
foundations=[
 {'id':'TDR_ORIGINAL_DATA','kind':'original_supplied_data',
  'statement':'The original E, CM Host, Datum, Level, Coeff and Moduli record, including the universal principally polarized abelian object, smoothness, quasiprojectivity and geometric multiplicities.'},
 {'id':'TDR_SEC_BASE_CHANGE','kind':'retained_original_premise',
  'statement':'Out.SecBaseChangeSt exactly as defined at the pin: original base locally Noetherian; arbitrary affine coefficient rings and all coefficient changes. Only n=1 used here; SecBaseChangeAnySt is not assumed.',
  'source':sources['section_bc']},
 {'id':'TDR_STANDARD_AG','kind':'standard_foundational_algebraic_geometry',
  'statement':'Affine scheme/ring duality, Zariski gluing and sheaf axioms, smooth Lie bundle and arbitrary base change, finite locally free module/sheaf equivalence, separated closed diagonal. Frame representability and all finite-descent arguments are proved in the chapter.'},
 {'id':'TDR_STANDARD_ALGEBRA','kind':'standard_commutative_algebra',
  'statement':'Polynomial and localization universal properties, units and determinants, prime-ideal criterion for reducedness, first isomorphism theorem. The specific localization injection, finite capture and radical quotient proofs are written in TDR6, TDR8 and TDR12.'},
]
dump('retained_foundations.json',{'schema':'rh-retained-foundations/1',**common,'foundations':foundations})
endpoints=[
 {'endpoint':'GlobalTheory.Frames.FramedBaseChange.exists_frMap','claim':'TDR3',
  'status':'whole_original_arbitrary_ring_base_change_written'},
 {'endpoint':'GlobalTheory.Frames.frPt_eq_of_frMap_injective','claim':'TDR4',
  'status':'whole_original_same_point_injective_equality_written'},
 {'endpoint':'GlobalTheory.Frames.exists_openChart_testRing','claim':'TDR5',
  'supporting_claims':['TDR12'],'status':'whole_original_actual_affine_test_chart_written'},
 {'endpoint':'GlobalTheory.exists_frameRing_testRing','claim':'TDR6',
  'status':'whole_original_universal_matrix_ring_written'},
 {'endpoint':'GlobalTheory.Frames.exists_univFrame_testRing','claim':'TDR6',
  'status':'whole_original_actual_universal_frame_written'},
 {'endpoint':'GlobalTheory.Frames.univFrame_classifies','claim':'TDR6',
  'status':'whole_original_classifier_for_all_coefficient_rings_written'},
 {'endpoint':'GlobalTheory.exists_fg_subalgebra_desc_away','claim':'TDR8',
  'status':'whole_original_simultaneous_localization_capture_written'},
 {'endpoint':'GlobalTheory.Frames.frPt_glue','claim':'TDR9',
  'status':'whole_original_principal_cover_gluing_written'},
 {'endpoint':'GlobalTheory.moduli_point_from_fg_subalgebra','claim':'TDR10',
  'status':'whole_original_actual_moduli_instance_written',
  'qualification':'The broader source utility for any locally finitely presented morphism is replaced only at the actual separated moduli/frame-scheme instances.'},
 {'endpoint':'GlobalTheory.Frames.TestDescent.exists_fg_descent','claim':'TDR11',
  'status':'whole_original_all_coefficient_algebra_exit_written'},
 {'endpoint':'GlobalTheory.reduced_finiteType_iff_testRing','claim':'TDR12',
  'status':'whole_original_two_way_presentation_equivalence_written'},
 {'endpoint':'GlobalTheory.Frames.allTest_of_secBaseChange','claim':'TDR13',
  'status':'whole_original_AllTest_implication_written'},
]
remaining=[
 'The original SecBaseChangeSt premise is retained. This packet does not reconstruct its supplier from the full abelian-scheme law package.',
 'The supplied original Moduli record and arithmetic input data are retained; their existence is not inferred.',
 'The actual normalized FramesOK family, CoverTri, FibTri and full IsUnf package remain adjoining producers. Only their pointwise FromTest field is now supplied at SecBaseChangeSt.',
 'No selected compound common-family obligation is closed by this packet, and no complete RH or Dirichlet GRH human proof is asserted.'
]
dump('contracts.json',{'schema':'rh-human-component-contracts/1',**common,
  'entry_premises':['TDR_ORIGINAL_DATA','TDR_SEC_BASE_CHANGE','TDR_STANDARD_AG','TDR_STANDARD_ALGEBRA'],
  'completed_source_endpoints':endpoints,'extra_hypotheses_introduced':[],
  'choice_order':['Fix original data and SecBaseChangeSt.','Given arbitrary S and actual y, descend its coefficients to one finite subalgebra and one frame.','Only if S is reduced, present that same subalgebra as one radical polynomial quotient and transport its same frame.'],
  'no_hidden_flatness':True,'nonreduced_fg_descent':True,'all_reduced_coefficient_algebras':True,
  'literal_FrMap_in_exit':True,'remaining':remaining})
dump('closure.json',{'schema':'rh-human-component-closure/1',**common,
  'completed_source_endpoints':endpoints,'whole_obligations_closed':[],
  'proposed_global_frontier_leaf_closures':[],
  'full_exists_fg_descent_supplied':True,'full_AllTest_at_SecBaseChangeSt_supplied':True,
  'full_principal_uniformization_supplied':False,
  'independent_reviews':[],'remaining':remaining})
dump('published_inputs.json',[])
(HERE/'report.txt').write_text(
 'ALL COEFFICIENT TEST RINGS — v0.50\n'
 f'Source pin: {PIN}\nProof SHA256: {sha(tex)}\n'
 f'Claims: {len(claims)}; pinned source files: {len(files)}; exact ranges: {len(sources)}.\n'
 'Status: human proofs written; independent review pending.\n\n'
 'TDR1–TDR4 identify actual Lie eigenframes and the theta-section frame line,\n'
 'prove arbitrary coefficient base change with literal FrMap, and give unique\n'
 'matrix/scalar changes and same-point equality under injective maps. The n=1\n'
 'SecBaseChangeSt is applied to the supplied locally Noetherian universal base;\n'
 'its arbitrary target-ring quantifier includes nonflat maps. No stronger\n'
 'SecBaseChangeAnySt is assumed.\n\n'
 'TDR5–TDR7 construct reduced affine charts, the explicit generic-GL-matrix\n'
 'localization, its actual universal frame and its unique classifier. The\n'
 'framed-point functor is represented by the actual Lie and theta frame bundles.\n'
 'This gives a justified human simplification of the finite-descent argument.\n\n'
 'TDR8–TDR11 prove finite coefficient capture, localization injectivity even\n'
 'with zero divisors, principal-cover gluing and the full original\n'
 'TestDescent.exists_fg_descent for every commutative coefficient algebra,\n'
 'including nonreduced and non-Noetherian rings. Both the representability\n'
 'proof and the direct source-compatible local construction are written.\n\n'
 'TDR12–TDR13 prove the exact radical-quotient TRing presentation and the\n'
 'whole allTest_of_secBaseChange implication. The actual point, ordered\n'
 'eigenframes, theta section, coefficient embedding and FrMap are retained.\n'
 'Consequently every complex frame in an already chosen family is FromTest.\n\n'
 'Retained: original Moduli/data and SecBaseChangeSt. No SecTwistSt required.\n'
 'Still adjoining: normalized FramesOK, CoverTri/FibTri, IsUnf and principal\n'
 'uniformization, spanning and common-family suppliers. No whole selected\n'
 'obligation is automatically closed. No Lean replay or PDF is claimed.\n\n'
 'Rebuild: python build_metadata.py --repo /path/to/pinned/formal_source\n'
 'Validate: python validate_tex.py --format /path/to/pdflatex.fmt\n'
 'All sources were compared byte-for-byte with git show at the pin.\n')
dump('hashes.json',{p.name:sha(p.read_bytes()) for p in HERE.iterdir()
                    if p.is_file() and p.name!='hashes.json'})
print(json.dumps({'component':COMPONENT,'claims':len(claims),'files':len(files),
                  'ranges':len(sources),'proof_sha256':sha(tex)}))
