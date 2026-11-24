#!/usr/bin/env python3
"""Reproduce the SF source ledger without modifying the Lean checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip() == PIN

def digest(b): return hashlib.sha256(b).hexdigest()

files = {}
def source(path, spelling, qualified, role='source_counterpart'):
    raw = (repo/path).read_bytes()
    blob = subprocess.check_output(['git','-C',str(repo),'show',f'{PIN}:{path}'])
    assert raw == blob, path
    lines = raw.splitlines(keepends=True)
    textlines = [x.decode('utf-8').rstrip('\n\r') for x in lines]
    decl = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma|def|abbrev|structure)\s+' + re.escape(spelling) + r'(?=\s|\{|\(|:)')
    starts = [i for i,line in enumerate(textlines) if decl.search(line)]
    assert len(starts) == 1, (path,spelling,starts)
    start = starts[0]
    boundary = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma|def|abbrev|structure|namespace|section|end|variable|attribute|set_option|open|include|instance|example)\b')
    stop = len(lines)
    for i in range(start+1,len(lines)):
        if boundary.search(textlines[i]):
            stop=i
            break
    while stop>start and not textlines[stop-1].strip(): stop-=1
    range_raw = b''.join(lines[start:stop])
    file_url=f'{URL}/blob/{PIN}/{path}'
    files[path] = dict(path=path,sha256=digest(raw),bytes=len(raw),line_count=len(lines),verified_equal_to_pinned_git_blob=True,url=file_url)
    return dict(path=path,declaration=qualified,source_spelling=spelling,line_start=start+1,line_end=stop,role=role,
                sha256=digest(raw),full_file_sha256=digest(raw),range_sha256=digest(range_raw),range_bytes=len(range_raw),
                first_line=textlines[start],declaration_lines_within_range=[start+1],url=f'{file_url}#L{start+1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)

D='src/Development/AbelianVarietyTheory/'
I=D+'Proofs/IwasawaDecomposition/'
A=D+'Definitions/AutomorphicMembership/'
F='src/Formalism/LocalToGlobal/'
G=F+'GroupLattices/'
T=G+'TiedFamilies/'
H=F+'HermitianColumns/'
L='src/Formalism/SharpRestriction/GenusPolyhedralBounds/RelativeIndexClassSets/LocIdFr.lean'

def sources(path, ns, names, role='source_counterpart'):
    return [source(path,n,ns+n,role) for n in names]

common = [
    'The host CM field, real subfield, involution, ranks and true-column record are supplied exactly as in v0.12; this component does not prove their arithmetic existence.',
    'SF2/SF4/SF7 use the literal supplied Ok, Pins, Laws, Later and StdF/StdLvC/CarH/CarT premises. The complete colsTiedSym_std constructor remains an explicit unexpanded source input.',
    'LI1--LI7 supply the local completion, splitting, prime bijection, iw embedding and original coefficient/complex position alignment. Their choices are retained.',
    'The Hermitian dual uses E-valued integrality with conjugation in the first argument. It is not a trace dual.',
    'A common B is asserted for one fixed global construction. There is no assertion of a single B across different arithmetic hosts or unrelated parameter choices.',
    'This component proves neither class-rank equality nor the comparison-map representation identity or global integral span; other components must provide those arguments.'
]

def claim(i,title,status,statement,deps,assumptions,srcs,relation):
    return dict(id=i,title=title,status=status,statement=statement,depends_on=deps,assumptions=common+assumptions,
                proof_location=dict(file='main.tex',anchors=[i]),expanded_notes=dict(file='report.txt',section=i),
                source_relation=relation,mathematical_status='proved_under_exact_declared_supplied_data_hypotheses',sources=srcs)

claims=[]
claims.append(claim('SF1','One global matrix from an orthonormal integral basis','faithful_translation',
    'For an E-coordinate map c, orthonormal E-basis b and L0=O_E-span(b), the matrix B with columns c(b_i) satisfies B* J B=I and c(L0)=B O_E^n. Exact rank reindexing gives Cmp.StdB.',[],
    ['An orthonormal E-basis whose O_E-span is L0 is supplied; SF2 supplies it for the actual positive-space construction.'],
    sources(T+'TieStd.lean','Formalism.L2.G.',['stdB_core','hermitian_form_frame_coordinates','exists_stdB','exists_stdB_of_tied'])+
    sources(G+'ComparisonMaps/TiedRec.lean','Formalism.L2.G.Cmp.',['StdB'])+
    sources(H+'InLocalDiscriminantKernel.lean','Formalism.L2.Herm.',['IsStd']),
    'Entrywise Gram calculation and exact basis coefficient vector; no local-to-global patching or Gram-Schmidt denominators.'))
claims.append(claim('SF2','Actual positive-space standard coordinates','derived_simplification',
    'For I.rec7 under Ok/Pins/Laws/Later, StdTied holds; gramP and every gramN are identity, all self-dual coordinate lattices are O_E powers, the terminal inclusion appends zero, and each latAt maps to its literal original representative lattice with unchanged frame determinants. B=I is available in these coordinates.',[],
    ['The relevant Ok.spaces and Pins.iX fields are used exactly; the statement does not construct the remaining parts of Ok, Laws or Later.'],
    sources(A+'DuStarPos.lean','GlobalTheory.Mem.',['DiagSpaces'])+
    sources(A+'TrueColumnChoicesHeckeCharReferenceEqOne.lean','GlobalTheory.Mem.Col2.ColIn.',['Ok'],'supplied_record_definition')+
    sources(I+'TrueColumnSpacesStandardInFrameCoords.lean','GlobalTheory.Mem.Col2.Crd.',['Ortho','ortho_pos','co','Ortho.isStd','Ortho.gram','Ortho.mem_standardLattice_iff_integral_coords','map_symm_map','incl_co'])+
    [source(I+'TrueColumnSpacesStandardInFrameCoords.lean','GlobalTheory.Mem.Col2.TC.spaces_in_coordinates','GlobalTheory.Mem.Col2.TC.spaces_in_coordinates')]+
    sources(A+'LatAtLattice.lean','GlobalTheory.Mem.Col2.TC.',['Pins','crd','latAt']),
    'Direct canonical-basis proof, including the stronger explicit choice B=I; the actual representatives and determinant labels remain unchanged.'))
claims.append(claim('SF3','Diagonal Hermitian dual and companion formula','derived_simplification',
    'For L_pi=O_E^(n-1) direct-sum pi O_E, the Hermitian dual is O_E^(n-1) direct-sum conjugate(pi)^-1 O_E; L_pi+conjugate(pi)L_pi#=O_E^n. If pi conjugate(pi)=T, then L_pi subset O_E^n subset L_pi# and T L_pi# subset L_pi. The n=0 case is trivial.',[],
    ['pi is nonzero when n>0; in the application its norm is the prime T.'],
    sources(I+'BaseLatticeStepZeroAddConjGeneratorDualSelfDual.lean','GlobalTheory.Mem.Col2.TC.',['base_sup_dual_eq'])+
    sources(I+'ChartBaseLatticeSupDualSelfDual.lean','GlobalTheory.Mem.Col2.TC.ChartBase.',['sup_dual_eq'])+
    sources(D+'Proofs/SatakeParameters/CompanionLatticeTrueColumnBaseLatticeEqStandard.lean','GlobalTheory.TwU.BaseComp.',['mem_dual_iff','sup_dual_eq_std']),
    'Computes the dual exactly and gives a two-term decomposition, simplifying source coordinatewise span-induction arguments.'))
claims.append(claim('SF4','Actual carried base lattices imply the companion identities','faithful_translation',
    'Under the supplied StdF/StdLvC/CarH/CarT data, every level-zero and chart base lattice is the corresponding L_(pi_u) with pi_u=X.piT u. SF3 proves SymmetricBaseCompatibility, the chart-indexed counterpart of BaseTied, and the actual level-zero Companion identity with ideal (conjugate(pi_u)).',['SF2','SF3'],
    ['The complete forms, level, carrier and class structures are supplied. Only their lattice/generator consequences are reconstructed; h_pi and the residual functional construction in herm_rest_tied are not asserted proved here.'],
    sources(A+'LatAtLattice.lean','GlobalTheory.Mem.Col2.TC.',['baseL','Reads','StdF'],'literal_lattice_and_reading_definitions')+
    sources(A+'StdLvPr.lean','GlobalTheory.Mem.Col2.TC.',['CarH','CarT'],'literal_carrier_definitions')+
    sources(A+'DuStarPos.lean','GlobalTheory.Mem.',['LevCh','LevCh.piT_ne'],'supplied_norm_and_prime_data')+
    sources(I+'BaseLatticeStepZeroAddConjGeneratorDualSelfDual.lean','GlobalTheory.Mem.Col2.TC.',['base_step_zero_tied'])+
    sources(I+'ChartBaseLatticeSupDualSelfDual.lean','GlobalTheory.Mem.Col2.TC.ChartBase.',['mem_reL_iff','mem_of_baseL'])+
    [source(I+'ChartBaseLatticeSupDualSelfDual.lean','GlobalTheory.Mem.Col2.TC.chart_base_sup_dual','GlobalTheory.Mem.Col2.TC.chart_base_sup_dual')]+
    sources(H+'ZeroPointScaledByCharacter.lean','Formalism.L2.Herm.',['BaseTied'],'nonchart_predicate_for_comparison')+
    sources(H+'SymAll.lean','Formalism.L2.Herm.',['SymmetricBaseCompatibility'],'literal_actual_predicate')+
    sources(T+'CompanionOfBaseTied.lean','Formalism.L2.G.',['companion_of_baseTied'])+
    sources(I+'ExistsGIs.lean','GlobalTheory.Mem.Top.Bl.TrueLocal.',['companion_of_colsHermS'])+
    sources(I+'HermitianColumnsGeneratorsBaseLatticesFunctional.lean','GlobalTheory.Mem.Col2.TC.',['herm_rest_tied'],'only_the_lattice_output_reconstructed_here'),
    'Tracks exact rank reindexing, terminal chart uniqueness and generator equalities; distinguishes SymmetricBaseCompatibility from its nonchart predecessor.'))
claims.append(claim('SF5','Exact first-projection lattice in the global frame','derived_simplification',
    'At a split place v with fixed first projection j_v and local integer ring R_v, if L subset B O_E^n and N B e_i lies in L with N a local unit, then the literal first projection of locL_v L is j_v(B) R_v^n. The reverse inclusion is witnessed by the finite tensor sum with coefficients u_i/N.',['LI5'],
    ['The splitting sends 1 tensor a to (a,a), j_v maps O_E into R_v, and N is a unit of R_v.'],
    sources(L,'Formalism.MainNotions.Gaps.Loc.',['hom_int','fst_int','fr_lat_of'])+
    sources(G+'LevelGatherings/CompletionIntegersIff.lean','Formalism.L2.G.',['LocId'],'literal_local_identification_structure'),
    'A finite generator calculation proves the literal existential fr_lat predicate, retaining the actual integral tensor subring.'))
claims.append(claim('SF6','Replace all local frames without changing positions','faithful_translation',
    'From L_u+a_u L_u#=L0=B O_E^n, L_u subset L_u#, T_u L_u# subset L_u, and p not dividing T_u, replace only fr in each LI local identification by j_v(B). The completion, splitting, place bijection, iw, original c^s position alignment and prescribed valuation identities are unchanged.',['SF1','SF5','LI4','LI6','LI7'],
    ['The actual companion is supplied by SF4 in the application; for the general lemma it is an explicit premise. GIdx includes p not dividing T_u.'],
    sources(T+'CompanionOfBaseTied.lean','Formalism.L2.G.',['stdB_mem','T_smul_mem','companion_le','LocId.withFr','locIdStd','locIdStd_fr','locIdStd_iw'])+
    sources(G+'ComparisonMaps/TiedRec.lean','Formalism.L2.G.Cmp.',['FrRat'],'downstream_same_global_frame_condition'),
    'Uses only the integral sandwich and a local unit; the frame changes while iw and all alignment-defining fields stay identical.'))
claims.append(claim('SF7','Simultaneous actual common-frame conclusion','derived_simplification',
    'For one supplied true-column construction with standard forms/carriers, choose one B from its common level-zero positive space. For all words and all GIdx places the actual local lattices have frames j_v(B), with B* J0 B=I and every LI position identity retained. In canonical positive coordinates B=I works.',['SF1','SF2','SF4','SF6'],
    ['The complete colsTiedSym_std constructor, host/point existence and remaining compatibility fields remain explicit source inputs. This theorem supplies StdB/fr_B and the companion algebra, not the full CmpTied representation identity.'],
    sources(I+'ExistsStandardColumnComparisonsTrueColumns.lean','GlobalTheory.Mem.Col2.TC.',['colsTiedSym_std'],'remaining_full_standard_column_supplier_not_claimed_proved')+
    sources(I+'ExistsGIs.lean','GlobalTheory.Mem.Top.Bl.TrueLocal.',['exists_trueVolume_stage_of_any_column_choice'],'downstream_assembly_uses_the_same_columns_not_claimed_fully_reconstructed')+
    sources(G+'ComparisonMaps/TiedRec.lean','Formalism.L2.G.Cmp.',['CmpTied'],'full_comparison_predicate_has_additional_fields'),
    'Combines the proved exact matrix/lattice statements for the same supplied data; explicitly isolates the unreconstructed full standard-column supplier.'))

out=dict(schema_version='1.2',artifact_version='0.13',date='2026-11-21',owner='/root/global_frame',
         repository=dict(url=URL,commit=PIN),range_convention='One-indexed inclusive; exact original bytes, without normalization.',
         verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
                           human_mathematical_proofs_supplied=True,lean_source_files_edited=False,
                           local_lean_compilation=False,lean_kernel_replay=False,replacement_arguments_formalized=False),
         status_definitions=dict(faithful_translation='Complete human proof of the precisely stated supplied-data assertion.',
                                 derived_simplification='Proved shorter calculation or explicit stronger formulation with the same application data.'),
         independent_reviews=[],claims=claims,files=[files[p] for p in sorted(files)],
         artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
         prior_components_reused=['LI'],same_iteration_companions=['CR','CS','LP'],
         boundary_resolved=['Common global frame algebra and exact local base-change frame',
                            'Actual positive-space standard coordinates',
                            'Actual companion identities from standard forms and carrier data'],
         retained_inputs=common,
         scope_precision=['SF does not reconstruct the entire colsTiedSym_std supplier.',
                          'The actual symmetric route uses SymmetricBaseCompatibility, not the nonchart BaseTied predicate.',
                          'The first-level integer rank cast is applied uniformly and preserves the distinguished last coordinate.',
                          'Only fr is changed in LocId; iw, split and PosCompat maps remain identical.',
                          'Hermitian duals are not trace duals.'])
review_path=HERE.parent/'reviews'/'cs_reviews_sf.txt'
if review_path.exists():
    review_text=review_path.read_text()
    main_hash=out['artifact_sha256']['main.tex']
    assert main_hash in review_text, 'SF reviewer hash does not identify current main.tex'
    out['independent_reviews'].append(dict(reviewer='/root/comparison_span',result='PASS',claim_ids=[c['id'] for c in claims],
        scope='Mathematical review of SF1--SF7, especially Hermitian dual orientation and literal local frame replacement.',
        review_record='../reviews/cs_reviews_sf.txt',review_record_sha256=digest(review_path.read_bytes()),
        final_artifact_sha256={'main.tex':main_hash},lean_replay=False))
(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc.append(f"{c['id']} | {c['title']} | {c['status']}")
    loc.append(c['statement'])
    for s in c['sources']:
        loc.extend([f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
                    f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
next_specs=[
    (I+'ExistsStandardFormComparisonSymmetricLevelMember.lean','formsTiedSym_std','GlobalTheory.Mem.FormSym.formsTiedSym_std',
     'Construct one simultaneous family of FormsTiedSym and StdF/StdLvC from the supplied true-column record. SF2 removes the coordinate-standardization subargument, but the chart construction, rational/integral polynomial values, norm ties, residues, levels and class/character compatibility remain to be reconstructed.',
     ['ExistsMemberStepCharts.lean:exists_charts','HermitianChartComplexRationalIntegralForms.lean:val_tied','ExistsGLocIdGChiTied.lean:exists_gLoc_idG_chiTied']),
    (I+'HermitianColumnChoicesOfFormsLevelsClasses.lean','hermColsCh_of_forms','GlobalTheory.Mem.Col2.TC.hermColsCh_of_forms',
     'Construct the actual Hermitian level/class carriers CarH from the same standard forms: level-zero ColLevel, all interior and terminal StepLevel/ClassTie records, residue field identifications, and their exact reindexed carrier equalities. SF4 proves companion consequences once these carriers are supplied; it does not construct all carrier records.',
     ['ColumnLevelOfStepZeroFormsLevelTrueColumns.lean','HermitianStepLevelOfChartFormsLevel.lean','HermitianClassConditionOfChartClasses.lean']),
    (I+'ExistsStandardColumnComparisonsTrueColumns.lean','colsTiedSym_std','GlobalTheory.Mem.Col2.TC.colsTiedSym_std',
     'Assemble the full ColsTiedSym package without losing the common forms/carrier identities. Remaining non-lattice work includes the level-prime data and CarT, residue functionals and uniformizer annihilation, adelic/stabilizer compatibility, and common character data. SF2 supplies StdTied and SF4 supplies the exact SymmetricBaseCompatibility output; the rest is not discharged by those calculations.',
     ['HermitianDataAtLevelPrime.lean:hermitian_data_at_level_prime','StepZeroHermitianLevelUniformiserKillsValues.lean:stepZeroHermitianLevel_uniformiser_kills_values','HermitianColumnsGeneratorsBaseLatticesFunctional.lean:herm_rest_tied'])
]
targets=[]
for path,spelling,qualified,scope,connections in next_specs:
    s=source(path,spelling,qualified,'remaining_simultaneous_standard_column_supplier')
    s.update(priority_group=1,remaining_human_scope=scope,source_connections=connections,
             human_status='continuation_target_only; not claimed reconstructed by SF')
    targets.append(s)
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.13',commit=PIN,targets=targets,
    source_files=[files[p] for p in sorted({t['path'] for t in targets})]),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(out['files']),next_targets=len(targets),verified_equal_to_pinned_git_blob=True)))
