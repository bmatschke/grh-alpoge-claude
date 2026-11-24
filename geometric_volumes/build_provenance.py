#!/usr/bin/env python3
"""Reproduce GV source provenance from immutable Git objects, without a Lean build.

The human replacement proofs and explicit classical premises live in main.tex.
This script verifies source bytes, claim boundaries and review bindings only.
"""
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
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
IW = D + 'Proofs/IwasawaDecomposition/'
GI = D + 'Proofs/GlobalInterpolation/'
FP = D + 'Proofs/FoundationProofs/'
AM = D + 'Definitions/AutomorphicMembership/'
DF = D + 'Definitions/Foundations/CdScaleTieIff.lean'
SL = 'src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLattice.lean'
GM = 'src/Formalism/SharpRestriction/GlobalSchurBounds/GeneralLinearActions/GenusMassVolumes.lean'
GL = 'src/Formalism/LocalToGlobal/GlobalTheory/GL5/'
CD = 'src/Formalism/LocalRingCardinality/DataCD.lean'
SP = 'src/Formalism/LocalRingCardinality/DataSpaces.lean'
ST = 'src/Formalism/HermitianLattices/StatementMass.lean'
MP = 'src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/UnimodularClassRepresentatives/'
IT = D + 'BlockTheory/GlobalSignature/IsometryTransportFrames.lean'
VP = 'src/Formalism/LocalToGlobal/ProjectiveLattices/VolProofs.lean'
RT = 'src/Formalism/LocalToGlobal/BesselHermitianTheta/MinfDensity.lean'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive|instance)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]



COMMON = ('Ordinary number-field/Dedekind-module algebra, product formula, finite-dimensional local and real analysis, Haar uniqueness, Tonelli, finite-dimensional change of variables, weak approximation and the Gaussian sphere-area formula. Every supplied Hermitian lattice is full and self-dual where stated; it need not be globally free. Literal CMData and SigOK/IsCMFam hypotheses remain.')
BOUND = ('Human reconstruction, no Lean build/kernel replay or formalization of replacement proofs. Volume identities do not supply unrelated row/local/arithmetic/layout data or RH/GRH. No arbitrary stored positive volume is identified with geometry without the literal tie or exact baseVol equality.')
TAM = ('Explicit named established theorem, NOT reconstructed: the Tamagawa-number theorem for every nontrivial unitary group over a CM quadratic extension, with positive finite quadratic L(1,epsilon) and exact measure |disc F|^(-n^2/2)L(1,epsilon)^(-1) product_real |omega| product_finite L_v(1,epsilon)|omega|; quotient mass is 2. Harris–Li–Skinner 2006 section 0.2 p.400 eq.0.2.1 and following statement; Weil IV section 4.4. All asserted descendants are conditional on this theorem.')
NORM = ('For the conversion identity only, L_F(1,epsilon) is the usual positive finite quadratic L-value supplied in the explicitly stated classical normalization. The measure is defined by GV.17. No quotient-mass or signature-independence theorem is used in this conversion.')
HM = ('Explicit inherited established theorem, NOT reconstructed: number-field Hasse–Minkowski for isotropy, as retained and referenced in MF4. GV14 proves its new exact norm-sign/complement application.')
DS = ('Retained actual representation inputs: DiscreteSeriesExist and FormalDegreeFormula2, with the source regular Harish–Chandra parameters, the exact trueScale Haar measure, and same-record dsig=trueDsig. Neither input is proved by the geometric volume calculation.')
CORE = ('Retained same-object coreOfLay inputs: the actual K,X,f,T and Lay(X.toD7), Over, RecOK, LedOK, same-map MuIsW, forced-prime inclusion, GatNum, untwisted row vanishing, MtStableAt, primitive type-character powers, and exact NChoice conductor-support/exponent equalities. No empty-model promotion or automatic transport of a dependent layout across withTrue.')


def cl(n,title,statement,deps,sources,tam=False,hm=False,ds=False,extra=(),relation=None):
    cond=[]
    if tam: cond.append(TAM)
    if hm: cond.append(HM)
    if ds: cond.append(DS)
    return dict(id=f'GV{n}',title=title,status='derived_simplification',statement=statement,
        depends_on=deps,assumptions=[COMMON,BOUND]+cond+list(extra),
        named_classical_inputs=(['GV-TAM'] if tam else [])+(['MF-HM'] if hm else [])+
            (['DiscreteSeriesExist','FormalDegreeFormula2'] if ds else []),
        mathematical_status=('proved_conditionally_on_explicit_unreconstructed_classical_inputs' if cond
            else 'proved_under_exact_declared_background_and_data_hypotheses'),
        proof_location=dict(file='main.tex',anchors=[f'GV{n}']),
        expanded_notes=dict(file='report.txt',section=f'GV{n}'),
        source_relation=relation or 'Human proof of the literal conclusion with exact hypotheses. Source declarations are pinned locators, not imported human proofs; explicit shorter replacement arguments are distinguished in main/report.',
        sources=sources)

claims=[
cl(1,'Actual adelic unitary group and unimodularity',
 'Finite-basis coordinates identify source HA with the actual restricted-product group and finite/real split; it is locally compact, second countable and unimodular by determinant Ad=1.',[],
 ss(GM,'IsCMExt IsHermND HR HFin HFinIn HA HA.mat','literal_interface')+
 ss(IW+'ExistsAdelicSplit.lean','exists_adelic_split')+
 ss(IW+'UnitaryGroupRealPointsEquivPiIndefiniteUnitary.lean','real_points')+
 ss(D+'Proofs/UnitaryExistence/LcscAdelicUnitaryGroup.lean','secondCountable_restrictedProduct lcsc_adelicUnitary')+
 ss(IW+'UpqLocallyCompactGroup.lean','upq_lcsc')),
cl(2,'Algebraic completion and the actual compact open lattice stabilizer',
 'latHat, whose closure is algebraic subgroup generation, equals the product of local completed lattices. Its actual unitary stabilizer is compact open and has the required two-sided lattice equality.',['GV1'],
 ss(SL,'intAf latHat L0c','literal_interface')+ss(DF,'latC StabHat','literal_interface')+
 ss(SP,'HSpace','literal_supplied_self_dual_lattice')+
 ss(IW+'LatCFullLattice.lean','latC_full_lattice')+
 ss(IW+'CompletedLatticeStabilizerCompactOpen.lean','exists_compact_latHat exists_compact_entries congr_mem_nhds stabGrp exists_compact_open_stab')),
cl(3,'Existence and uniqueness of the exact normalized Haar measure',
 'The finite stabilizer has mass one and the actual supplied CDHaar gives every real factor; all embedding/signature-matrix AllSome clauses hold for every choice. IsVolMeasF exists uniquely, also for mixed signatures.',['GV1','GV2'],
 ss(GM,'AllSome','literal_quantifier')+ss(DF,'IsCMFam IsVolMeasF','literal_interface')+
 ss(SL,'IsInfEmb IsVolMeas','literal_interface')+
 ss(IW+'ExistsUniqueInfEmb.lean','infEmb_exists infEmb_unique existsUnique_infEmb')+
 ss(IW+'ExistsIsUnitaryAdelicVolumeMeasure.lean','exists_haar_prod exists_upq_mul exists_isVolMeasF')+
 ss(IW+'ExistsSetPosFinite.lean','haar_eq_of_eq_on_set exists_set_pos_finite volMeas_unique')),
cl(4,'Rational discreteness and actual fundamental domains',
 'A small adelic neighborhood isolates each rational unitary point. A Borel selector gives an actual fundamental domain; Tonelli proves equality and positivity of all domain masses, without assuming finite covolume.',['GV1'],
 ss(IW+'ExistsNhdsOneUnitaryGroupRationalPointEqOne.lean','exists_nhds_one_rational_eq_one')+
 ss(IW+'FundamentalDomainUnitaryAdelicExistsMeasureEq.lean','discreteTopology_subgroup_of_nhds_one fundamentalDomain_exists_measure_eq_of_discrete fundamentalDomain_adelicUnitary')+
 ss(IW+'FiniteVolumeAdelicUnitaryQuotient.lean','countable_HFinIn')),
cl(5,'Explicit Omega density and compact-dual factorial constant',
 'Off-diagonal real determinant 4 gives Omega=2^b dX; the first-column sphere fibration gives v_n=2^n pi^a/product j!. CDHaar.prob/trick therefore force density A_n^-1 Omega, A_n=(2pi)^a/product j!, for every signature.',['GV1','SE11'],
 ss(CD,'lieU entries IsOmegaLeb ballU OmegaDensity CDHaar','literal_normalization')+
 ss(FP+'ReImMapSurjective.lean','reImMap reImMap_injective reImMap_surjective exists_isOmegaLeb')+
 ss(FP+'NonemptyCompactDualHaar.lean','exists_density_of_chart image_expU exists_omegaDensity exists_haar_of_density exists_prob_haar nonempty_cdHaar'),
 relation='Explicit numerical refinement of the actual Omega and CDHaar interfaces. The sphere-fibration and determinant calculations are replacement human proofs, not assumed source numerical formulas.'),
cl(6,'Rational top gauge and the exact isometry determinant',
 'The rational delta basis and tangent map X->JX define a gauge. On skew-Hermitian matrices det(Y->B*YB)=Norm(det B)^n; finite and real changes contribute |det J|^n, with real gauge coefficient |tau delta|^-a v_n.',['GV1','GV5'],
 ss(GM,'HermR IsHermND','literal_hermitian_algebra')+ss(CD,'lieU IsOmegaLeb','literal_real_normalization')+
 ss(SL,'IsVolMeas','literal_target_normalization')+
 ss(MP+'MassLandA.lean','exists_skew eq_add_mul_skew')+
 ss(IT,'frameMat IsConjBy','literal_rational_transport'),
 relation='New explicit rational gauge calculation supporting the source normalization. No source signature-independence or mass identity is imported.'),
cl(7,'Dyadic integral Lie lattice and smooth congruence lifting',
 'The exact integral-Lie determinant in the rational delta basis is |2|^-b |delta^2|^-a/2. Surjectivity of X+X* via residue trace gives all unitary congruence lifts and local measure q^-n^2 for an integral gauge, also at 2.',['GV6','DR1','MF1'],
 ss(SP,'CMData','literal_unramified_hypothesis')+ss(ST,'IsCMUnram','literal_unramified_hypothesis')+
 ss(D+'Proofs/AdelicLatticeProofs/ExistsIsUnitFormSelfOfNotMem.lean','trace_surjective')+
 ss(D+'Proofs/FlagMeasures/ExistsLocalUnitaryOfSelfDualAtPlace.lean','exists_isUnit_sub normal_form')+
 ss(MP+'DifferentIdealEqTop.lean','differentIdeal_eq_top')+
 ss(MP+'FirstFamilyOperatorEnd.lean','akCount_succ_fine alphaL_eq','congruence_count_counterpart'),
 relation='The local integral tangent determinant and measure calculation are proved explicitly. The source cmUnram/trace/congruence interfaces anchor the actual setting; no inverse of 2 in a residue field is assumed.'),
cl(8,'Finite standard unitary orders and exact local gauge masses',
 'The split/nonsplit group orders give q^-n^2 |U_n(k)|=product_j(1-epsilon^j q^-j). For every actual self-dual lattice the normalized local gauge factor is |det J|^n |2|^-b |delta^2|^-a/2 times this product.',['GV2','GV6','GV7','DR1','MF6'],
 ss(MP+'CardUnitaryFin.lean','card_unitary_fin card_GL_fin')+
 ss(MP+'LocalDensityRatio.lean','alphaStd','literal_finite_factor')+
 ss(MP+'LamGEqOneOfOrtho.lean','alphaL_of_vd_zero alphaStd_pos')+
 ss(D+'Proofs/FlagMeasures/ExistsLocalUnitaryOfSelfDualAtPlace.lean','exists_orthonormal exists_unitary_of_selfDualAt')+
 ss(IW+'CompletedLatticeStabilizerCompactOpen.lean','exists_compact_open_stab')),
cl(9,'Complete global gauge conversion with product-formula cancellation',
 'The normalized Tamagawa gauge equals C_n times the actual source Haar measure, C_n=|disc F|^-n^2/2 A_n^f/product_{j=1}^n L_F(j,epsilon^j). Every det J and delta factor cancels; the finite dyadic factor supplies 2^bf; local j=1 factors cancel before infinite products.',['GV3','GV5','GV6','GV7','GV8','MF1'],
 ss(CD,'IsOmegaLeb CDHaar','literal_real_target')+ss(DF,'IsVolMeasF','literal_global_target')+
 ss(MP+'LValEtaEqLValEtaF.lean','lValEta_eq_lValEtaF eulerEta','fixed_field_euler_convention')+
 ss(MP+'DifferentIdealEqTop.lean','natAbs_discr discrTower','unramified_discriminant_convention'),
 extra=[NORM],relation='New explicitly calculated conversion in the primary published Tamagawa measure convention. The conversion does not assume quotient mass 2 or signature independence.'),
cl(10,'Named unitary Tamagawa input and genuine finite covolume',
 'Conditionally on the explicitly named and normalized unitary Tamagawa-number theorem, all positive ranks have actual quotient mass M_n=2/C_n; rank zero has mass one. The same named theorem also supplies the literal general FiniteVolume2, without extending the unramified local formula to ramified places.',['GV1','GV3','GV4','GV9'],
 ss(DF,'FiniteVolume₂','literal_general_endpoint')+
 ss(IW+'FiniteVolumeAdelicUnitaryQuotient.lean','finVol','alternative_source_endpoint')+
 ss(IW+'FiniteCovolumeLatticeStabiliserUnitaryRealPoints.lean','finite_covolume_real_points','source_route_not_claimed_internalized'),tam=True,
 relation='Alternative proof from a named unreconstructed established theorem with exact conversion. The source reduction/drift/finiteness proof is not claimed reconstructed.'),
cl(11,'Geometric definite quotient-to-genus-mass identity',
 'Adelic lattice intersection gives the literal genus class correspondence and rational automorphism stabilizers. A finite weighted characteristic function with orbit sum one gives normalized quotient mass sum 1/|Aut(L_i)|, independently of Tamagawa and of the mass ratio.',['GV2','GV3','GV4','DR1','LP1','MF3','TL1'],
 ss(ST,'mass MassBasic','literal_mass_interface')+
 ss(GL+'FamilyMassVolumeIdentityOfClassDecomp.lean','stab hit hitEquiv measure_fd_eq_sum measure_fd_toReal KSet KSub measure_KSub DefClassDecomp','actual_weighted_geometry')+
 ss(GL+'FamilyMassVolumeIdentityOfClassDecomp.lean','mass_volume_identity_of_class_decomp','source_composite_endpoint'),
 relation='The weighted geometric count and actual class/stabilizer identification are proved; the later standard-rank equality is separated into GV13 and is not assumed here.'),
cl(12,'All three literal VolIndep clauses',
 'Self-dual lattice stabilizers are adelically conjugate, giving the same normalized measure. A rational isometry gives the exact matrix intertwiner, rational subgroup transport, measure pushforward and both FD directions. VolEqOfIsometric follows under supplied VolTie.',['GV1','GV2','GV3','GV4','DR1'],
 ss(IT,'withLat frameMat CarriesLat IsConjBy LatticeIndep IsometryTransport VolEqOfIsometric VolIndep','literal_interface')+
 ss(GI+'IsFundamentalDomainMap.lean','isFundamentalDomain_map isVolMeas_map latticeIndependence isometryTransport volumeInvariance volumeIndependence')+
 ss(GI+'IsFundamentalDomainIffImageHA.lean','isFundamentalDomain_iff_image_HA volumeIndependence_iff')+
 ss(GI+'VolIndep.lean','volIndep')),
cl(13,'Actual signature independence and VolumeEqMass2',
 'Under the named Tamagawa theorem the same-rank normalized quotient masses agree for all signatures; the positive standard quotient equals massI. With the literal VolTie this proves VolumeEqMass2, including rank zero, without a hidden signature-independence premise.',['GV10','GV11'],
 ss(GL+'PNamed.lean','VolSigIndep stdPos stdPos_sigOK stdPos_rank stdPos_sig vol_eq_mass_of_indep','literal_source_endpoints')+
 ss(GL+'Statement.lean','GenusMassStd','literal_genus_endpoint')+
 ss(SL,'VolTie VolumeEqMass₂','literal_volume_endpoint')+
 ss(GI+'UnitaryVolumeEqRankMassAllSignatures.lean','vol_eq_massI_all_sig','alternative_source_route'),tam=True),
cl(14,'Norm-sign vector and actual self-dual orthogonal complement',
 'From the inherited named Hasse–Minkowski theorem, all local norm-sign solutions give a rational vector of the permitted sign. Explicit local equal-norm transport, rational approximation and lattice patching supply a genuine self-dual complement and every UnitSplit field.',['DR1','MF1','MF3','MF4','LP1'],
 ss(GL+'PNamed.lean','UnitSplit unitSplit_of_landherr','literal_endpoint_and_alternative_route')+
 ss(SP,'HSpace IsIsomEmb','actual_complement_fields')+
 ss(MP+'SumOrbitsEquivariant.lean','exists_move','explicit_equal_norm_transport')+
 ss(D+'Proofs/AdelicLatticeProofs/ExistsCongrIffTraceFormsIsometricCm.lean','isotropic_of_locally_isotropic isotropic_of_indefinite','named_classical_route'),hm=True,
 relation='Alternative exact UnitSplit proof from named Hasse–Minkowski. No global Landherr normal form or global integral orthonormal basis is assumed.'),
cl(15,'Geometric successor ratio and every Conclusion2 field',
 'Dividing the actual quotient formula and substituting the exact MF1 discriminant/Euler conventions gives massRatioRightSide. Combined with the actual complement and supplied VolTie it proves Conclusion2, and before VolTie the normalized-domain VolRatioTrue.',['GV13','GV14','MF1'],
 ss(ST,'massRatioRightSide fDeg vInv lValEta','literal_normalization')+
 ss(SL,'Conclusion2','literal_geometric_endpoint')+
 ss(GL+'Statement.lean','VolRatioTrue','literal_domain_endpoint')+
 ss(GL+'PNamed.lean','volRatioTrue_of_named theorem_two_of_landherr','alternative_source_route'),tam=True,hm=True),
cl(16,'Actual VolIs(trueVol) and volumesAgreeAdelic supplier',
 'The source trueVol has a nonempty positive branch on every SigOK space and equals M_n. This proves all VolIs quantifiers and VolTieG for precisely the same record whose volume is trueVol; the host CM-type is unchanged.',['GV3','GV4','GV10'],
 ss(DF,'VolIs trueVol trueVol_pos trueVol_spec volTieG_iff','literal_choice_and_tie')+
 ss(IW+'IsCMFamHost.lean','isCMFam_host')+
 ss(IW+'UnitaryAdelicQuotientVolumeIsVolume.lean','volIs_trueVol')+
 ss(IW+'VolumesAgreeAdelicOfTrueVolume.lean','volTieG_of_trueVol'),tam=True),
cl(17,'Exact trueScale with all sorting choices and measurable sets',
 'Reindexing signs, Haar uniqueness and inner permutation invariance prove a unique positive CdScaleIs scalar for every Boolean sign ordering; the actual trueScale branch is inhabited and cdScaleTie follows under the same-record equality.',['GV1','GV5'],
 ss(DF,'CdScaleIs trueScale trueScale_pos cdScaleTie_iff','literal_scale_interface')+
 ss(FP+'CdScaleIsTrueScale.lean','Sorts Sorts.reindex_Jpq exists_sorts Sorts.equiv Sorts.exists_conj Sorts.map_eq Sorts.exists_scale exists_cdScaleIs cdScaleIs_trueScale cdScaleIs_unique')),
cl(18,'Canonical quotient probability measure and exact level-index direction',
 'Domain restriction and quotient pushforward are independent of the domain. Under the geometric tie, actual muQ1=M_n^-1 muQ, with no fallback. Renormalizing an index-r sublevel to volume one multiplies quotient mass by r and preserves probability normalization.',['GV3','GV4','GV10','GV16'],
 ss(VP,'VolPairEx volPair_isVolPair isVolPair_of_volTie mass_eq_of_isVolPair muQ_univ muQ_univ_eq_vol finVol_of_volTie normalized_quotient_measure_eq probability_measure_eq_pair'),tam=True),
cl(19,'The same original baseVol and withTrue stages satisfy the geometric volume clause',
 'The IG12 original GJStage has literal baseVol=trueVol; its VolTieG now holds uniformly over every W,V,S,N on the same B,C. withTrue and a later gat reset preserve this volume clause. Other ColumnDataSplitPrimes/Omega clauses and dependent transports remain explicit.',['IG12','GV16'],
 ss(AM+'ResCharThetaJetPlaceDegOne.lean','GJStage','actual_stage_fields')+
 ss(IW+'InhabitedStage.lean','baseVol baseVol_pos exists_noJet exists_oneJet inhabited_stage')+
 ss(AM+'WithTrue.lean','GJStage.withTrue','literal_same_base_reset')+
 ss(IW+'ExistsGIs.lean','isLocalFamily_stages nonempty_columnLocalData_of_standardConcreteFamily exists_trueVolume_stage_of_any_column_choice exists_trueVolumeStage_columnChoiceStep','exact_conditional_stage_join'),tam=True,
 extra=['The other GIs2/ColumnDataSplitPrimes/Omega-compatible clauses remain their exact same-object supplied hypotheses; only the universal volume clause is supplied by this component.']),
cl(20,'Exact conditional RealOf and all four RealTied fields',
 'For the same record with baseVol, cdScale=trueScale and dsig=trueDsig, the new volume/scale proofs give two RealTied fields; the explicitly retained DiscreteSeriesExist and FormalDegreeFormula2 give the other two. No representation existence is inferred from volume.',['GV16','GV17'],
 ss(RT,'RealTied','literal_four_field_interface')+
 ss(DF,'DiscreteSeriesExist FormalDegreeFormula₂ trueDsig','retained_representation_inputs')+
 ss(IW+'ExistsDiscreteSeriesFormalDegreeProduct.lean','fdegOf_eq_of_isFdeg exists_isDS_isFdeg_trueDsig')+
 ss(IW+'LevelThreeToFour.lean','RealOf real_of realOf')+
 ss(AM+'Retie.lean','retie','exact_nonidentity_reset'),tam=True,ds=True),
cl(21,'Strengthened same-object conditional V4.Core supplier and precise boundary',
 'On the actual X,f,T and layout, GV20 discharges RealTied and GV13 supplies geometric mass. The exact coreOfLay constructor retains its other arithmetic, row, numerical, forced-prime and NChoice-support/exponent inputs. Empty stages do not yield Core or ExTrue.',['HF20','GV13','GV19','GV20'],
 ss(AM+'RationalRootsDef.lean','RowLay MuIsW Core ExTrue','literal_current_V4_interfaces')+
 ss(AM+'ExistsStagesClauses.lean','rowLay_iff coreOfLay','exact_same_object_constructor'),tam=True,ds=True,extra=[CORE])
]

ids={c['id'] for c in claims}
assert len(claims)==len(ids)==21
old=json.loads((HERE.parent/'history/version_0_20/provenance.json').read_text())
prior=old['claims'].values() if isinstance(old['claims'],dict) else old['claims']
old_ids={c['id'] for c in prior}
assert not ids&old_ids
for c in claims:
    assert set(c['depends_on']) <= ids|old_ids,(c['id'],c['depends_on'])
    assert all(not d.startswith('GV') or int(d[2:])<int(c['id'][2:]) for d in c['depends_on'])
mb=(HERE/'main.tex').read_bytes();rb=(HERE/'report.txt').read_bytes()
paragraphs={}
for i,c in enumerate(claims):
    start=mb.index(('\\paragraph{'+c['id']+':').encode())
    stop=mb.index(('\\paragraph{GV'+str(i+2)+':').encode()) if i+1<len(claims) else len(mb)
    paragraph=mb[start:stop]
    h=digest(paragraph);paragraphs[c['id']]=h
    line_start=mb[:start].count(b'\n')+1
    line_end=line_start+len(paragraph.splitlines())-1
    assert b''.join(mb.splitlines(keepends=True)[line_start-1:line_end])==paragraph
    c['proof_paragraph_sha256']=h
    c['proof_location'].update(paragraph_sha256=h,line_start=line_start,
        line_end=line_end,bytes=len(paragraph))

external_references=[
 dict(id='GV-TAM-HLS',authors=['Michael Harris','Jian-Shu Li','Christopher M. Skinner'],
  title='p-Adic L-Functions for Unitary Shimura Varieties I: Construction of the Eisenstein Measure',
  publication='Documenta Mathematica, Extra Volume Coates (2006), 393–464',
  location='Section 0.2, printed page 400 (PDF page 8): equation (0.2.1), following Tamagawa-number statement, and equation (0.2.2)',
  url='https://ems.press/content/book-chapter-files/27474',doi='https://doi.org/10.4171/DMS/4/12',
  source_type='primary published research paper, publisher-hosted full text inspected',
  scope=TAM,theorem_proof_reconstructed=False,normalization_conversion_proved_here=['GV5','GV6','GV7','GV8','GV9']),
 dict(id='GV-TAM-Weil',author='Andre Weil',title='Adeles and Algebraic Groups',
  publication='Progress in Mathematics 23, Birkhauser, 1982',
  location='Chapter IV, section 4.4: The Tamagawa number (hermitian and quaternionic cases)',
  url='https://link.springer.com/book/10.1007/978-1-4684-9156-2',
  scope='Classical treatment of the retained theorem. The exact convention used here is pinned to the inspected HLS primary statement; no claim to have reconstructed the book proof.',theorem_proof_reconstructed=False),
 dict(id='GV-HM-inherited',inherited_reference_ids=['MF-HM-Kim','MF-HM-Hanke'],
  scope=HM,used_by=['GV14','GV15'],theorem_proof_reconstructed=False)
]
closed=[
 dict(id='GV-closed-normalized-Haar',claims=['GV1','GV2','GV3','GV4'],status='reconstructed',
  statement='Actual normalized Haar, all AllSome choices, rational fundamental domains, positivity and uniqueness.',
  sources=ss(IW+'ExistsIsUnitaryAdelicVolumeMeasure.lean','exists_isVolMeasF','completed_endpoint')+
          ss(IW+'FundamentalDomainUnitaryAdelicExistsMeasureEq.lean','fundamentalDomain_adelicUnitary','completed_endpoint')),
 dict(id='GV-closed-finite-volume',claims=['GV9','GV10'],status='proved_conditionally_on_named_unreconstructed_Tamagawa_theorem',
  statement='General FiniteVolume2 from the named classical theorem; exact unramified self-dual quotient mass from the fully proved conversion.',
  sources=ss(DF,'FiniteVolume₂','completed_conditional_endpoint')),
 dict(id='GV-closed-VolIndep',claims=['GV12'],status='reconstructed',
  statement='Actual lattice/isometry transport and volume invariance under supplied VolTie, without Tamagawa.',
  sources=ss(IT,'VolIndep','completed_endpoint')),
 dict(id='MF-next2',claims=['GV11','GV13','GV16','GV19'],status='proved_conditionally_on_named_unreconstructed_Tamagawa_theorem',
  statement='The actual geometric frontier is supplied on the exact baseVol/trueVol stage; VolumeEqMass2 follows under literal VolTie. This does not claim arbitrary positive D.vol or full Core.',
  sources=ss(SL,'VolumeEqMass₂ VolTie','completed_conditional_endpoints')+
          ss(IW+'VolumesAgreeAdelicOfTrueVolume.lean','volTieG_of_trueVol','completed_conditional_endpoint')),
 dict(id='GV-closed-UnitSplit',claims=['GV14','GV15'],status='proved_conditionally_on_named_unreconstructed_classical_inputs',
  statement='UnitSplit from inherited Hasse–Minkowski; the actual geometric Conclusion2 and VolRatioTrue additionally use the named Tamagawa theorem.',
  sources=ss(GL+'PNamed.lean','UnitSplit','completed_conditional_endpoint')+ss(SL,'Conclusion2','completed_conditional_endpoint')),
 dict(id='GV-closed-trueScale',claims=['GV17'],status='reconstructed',
  statement='Literal CdScaleIs(trueScale), all sortings/measurable sets, with uniqueness and no discrete-series premise.',
  sources=ss(FP+'CdScaleIsTrueScale.lean','cdScaleIs_trueScale cdScaleIs_unique','completed_endpoint')),
 dict(id='GV-closed-original-stage-volume',claims=['GV16','GV19'],status='proved_conditionally_on_named_unreconstructed_Tamagawa_theorem',
  statement='Original IG12 baseVol GJStage and exact withTrue reset satisfy the universal same-B,C volume field; no new twist/jet or dependent Core transport is asserted.',
  sources=ss(IW+'InhabitedStage.lean','baseVol exists_noJet','completed_conditional_endpoint')+
          ss(IW+'ExistsGIs.lean','exists_trueVolume_stage_of_any_column_choice','volume_field_only_completed'))
]
targets=[
 dict(id='GV-next1',priority=2,status='established_classical_theorem_cited_not_reconstructed',
  title='Internalize the exactly normalized unitary Tamagawa theorem if a proof without named classical inputs is desired',
  remaining_scope='Prove the named theorem in GV10, with the exact HLS 0.2.1 normalization and all CM/rank quantifiers. All local/real conversion factors and definite class weights are already proved. This is an established classical theorem, not a new conjectural signature bridge. The listed source finiteness/drift paths are alternative optional routes, not additional hidden premises.',
  external_references=['GV-TAM-HLS','GV-TAM-Weil'],
  claims_affected=['GV10','GV13','GV15','GV16','GV18','GV19','GV20','GV21'],
  sources=ss(IW+'FiniteVolumeAdelicUnitaryQuotient.lean','finVol','optional_internal_finiteness_route')+
          ss(IW+'FiniteCovolumeLatticeStabiliserUnitaryRealPoints.lean','exists_finite_measure_cover finite_covolume_real_points','optional_internal_reduction_route')),
 dict(id='GV-next2',priority=1,status='retained_actual_representation_supplier',
  title='Discrete-series existence and exact compact-dual formal degrees',
  remaining_scope='Construct the actual IsDS representations for every regular source Harish–Chandra parameter and prove FormalDegreeFormula2 under the already proved CdScaleIs. GV17 fixes the exact Haar scale; GV20 is currently the conditional field join, not a proof of representation existence/formal-degree identities.',
  claims_affected=['GV20','GV21'],
  sources=ss(DF,'DiscreteSeriesExist FormalDegreeFormula₂','retained_actual_inputs')+
          ss(IW+'ExistsDiscreteSeriesFormalDegreeProduct.lean','exists_isDS_isFdeg_trueDsig','conditional_join')+
          ss(IW+'LevelThreeToFour.lean','realOf','conditional_join')),
 dict(id='GV-next3',priority=1,status='retained_same_object_nonempty_Core_supplier',
  title='Nonempty compatible V4.Core after geometric volume and scale are supplied',
  remaining_scope=CORE+' GV19 supplies only the exact baseVol volume field and GV20 the conditional real-data join; use other components for their explicit compatible inputs. This is not the older unversioned Top.Core.',
  claims_affected=['GV21'],
  sources=ss(AM+'RationalRootsDef.lean','Core ExTrue','retained_actual_endpoint')+
          ss(AM+'ExistsStagesClauses.lean','coreOfLay','conditional_same_object_join')),
 dict(id='GV-next4',priority=3,status='optional_source_route_expansion',
  role='optional_source_route_expansion',optional_for_current_reconstruction=True,
  title='Optional source Siegel–Weil/signature route to the already conditionally proved volume equality',
  remaining_scope='The source route through its SW1b2/Conclusion1 or all-signature volume argument can be expanded independently if desired. Under the named Tamagawa theorem these are not prerequisites for GV13/GV16. Do not list signature independence itself as an unexplained input of the present proof.',
  claims_affected=[],
  sources=ss(SL,'SW1b2 Conclusion1','optional_source_route')+
          ss(GI+'UnitaryVolumeEqRankMassAllSignatures.lean','vol_eq_massI_all_sig','optional_source_route'))
]
field_inventory=[]
for path,name,role in [(CD,'CDHaar','all_four_normalization_fields_proved_or_reused'),
                      (RT,'RealTied','two_geometric_fields_proved_two_representation_fields_explicitly_conditional'),
                      (AM+'RationalRootsDef.lean','Core','conditional_same_object_field_join'),
                      (AM+'RationalRootsDef.lean','MuIsW','retained_arithmetic_compatibility_fields')]:
    sr=source(path,name,'literal_field_inventory');lines=read_source(path)[1]
    fs=[]
    for n in range(sr['line_start'],sr['line_end']+1):
        m=re.match(r'^  ([A-Za-z_][A-Za-z0-9_\'\u2080-\u2089]*)\s*(?::|\()',lines[n-1])
        if m:fs.append(dict(field=m.group(1),line=n))
    field_inventory.append(dict(path=path,record=sr['declaration'],role=role,fields=fs,source=sr))

out=dict(schema_version='1.3',artifact_version='0.21',owner='/root/global_frame',
 repository=dict(url=URL,commit=PIN),
 range_convention='Inclusive original Git-blob line bounds, preserving newline bytes; only trailing blank lines before the next top-level boundary omitted.',
 verification=dict(full_file_bytes_compared_to_pinned_git_blob=True,range_bytes_compared_to_pinned_git_blob=True,
  missing_sparse_files_read_with_git_show=True,declaration_boundaries_checked=True,
  old_claim_id_collisions_checked=True,component_dependency_order_checked=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Human proof with exact stated data/background. Explicit named classical theorem and retained representation/Core premises remain conditional where listed; source proof bytes are not treated as human proofs.'),
 claims=claims,files=[files[k] for k in sorted(files)],
 artifact_sha256={'main.tex':digest(mb),'report.txt':digest(rb)},proof_paragraph_sha256=paragraphs,
 prior_components_reused=sorted({d for c in claims for d in c['depends_on'] if d not in ids}),
 external_references=external_references,field_inventory=field_inventory,independent_reviews=[],
 scope='Exact adelic/real normalization and definite geometric mass; signature independence, VolumeEqMass2 and original baseVol VolTieG conditionally on the explicitly named unreconstructed unitary Tamagawa theorem. TrueScale is proved. Hasse–Minkowski remains for UnitSplit; actual discrete-series/formal-degree and nonempty same-object Core inputs remain explicit.',
 boundary_resolved=['Actual compact-open lattice stabilizers and normalized Haar/fundamental-domain existence',
  'Every finite/real determinant, dyadic, Omega and compact factorial factor in the conversion',
  'Direct definite quotient-to-genus-mass identity',
  'Exact VolIndep lattice/isometry transport, without Tamagawa',
  'VolSigIndep and VolumeEqMass2 conditional on named normalized Tamagawa theorem',
  'UnitSplit from inherited Hasse–Minkowski and geometric Conclusion2 with the same classical conditions',
  'Actual VolIs(trueVol), original same-base stage VolTieG and quotient probability normalization',
  'Literal CdScaleIs(trueScale), independently of Tamagawa and representation existence'],
 retained_inputs=[COMMON,BOUND,TAM,HM,DS,CORE],
 dependency_precision=['GV9 calculates the conversion before any quotient-mass equality; only its named positive L(1,epsilon) normalizer is supplied.',
  'GV11 definite class counting has no GV10/Tamagawa dependency and uses MF3 to connect completed to rational-local genus definitions.',
  'GV12 has no signature-independence or Tamagawa premise; only its third clause requires literal VolTie.',
  'GV14 uses Hasse–Minkowski separately and supplies a patched self-dual complement rather than assuming an old intersection is self-dual.',
  'GV17 has no Tamagawa or discrete-series dependency.',
  'GV19 is a new downstream supply for the inherited IG12 boundary; no old dependency is changed.',
  'GV20–GV21 retain both representation theorems and all exact same-object Core inputs. No empty-Tw/empty-Loc promotion.'])

for name,nums in [('geometric_volumes_GV1_12_review.json',range(1,13)),
                  ('geometric_volumes_GV13_21_review.json',range(13,22))]:
    p=HERE.parent/'reviews_v0_21'/name
    if p.exists():
        raw=p.read_bytes();rv=json.loads(raw)
        reviewed=rv['reviewed_claims']
        for n in nums:
            cid=f'GV{n}';item=reviewed[cid]
            h=item if isinstance(item,str) else item.get('paragraph_sha256',item.get('sha256'))
            assert h==paragraphs[cid],('reviewed paragraph changed',cid,h,paragraphs[cid])
        assert rv.get('reviewer')=='/root'
        out['independent_reviews'].append(dict(reviewer=rv['reviewer'],author='/root/global_frame',
          result=rv.get('result',rv.get('status','PASS')),claim_ids=[f'GV{n}' for n in nums],
          review_record='../reviews_v0_21/'+name,review_record_sha256=digest(raw),
          paragraph_sha256={f'GV{n}':paragraphs[f'GV{n}'] for n in nums},lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc.extend([f"{c['id']} | {c['title']} | {c['mathematical_status']}",c['statement'],
      'proof_paragraph_sha256: '+c['proof_paragraph_sha256']])
    for s in c['sources']:
        loc.extend([f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
          '  role: '+s['role'],'  file_sha256: '+s['full_file_sha256'],
          '  range_sha256: '+s['range_sha256'],'  '+s['url']])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.21',commit=PIN,targets=targets,
 closed_source_targets=closed,inherited_retained_target_ids=['MF-next1'],
 remaining_boundary='Unitary Tamagawa theorem remains a named unreconstructed classical input with fully proved normalization conversion; Hasse–Minkowski remains for UnitSplit. Exact discrete-series/formal-degree and same-object nonempty Core suppliers remain explicit. Alternative source volume proofs are optional expansions.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
 source_files=len(files),next_targets=len(targets),closed_targets=len(closed),
 independent_reviews=len(out['independent_reviews']),field_inventory_count=sum(len(x['fields']) for x in field_inventory),
 artifact_sha256=out['artifact_sha256'],verified_equal_to_pinned_git_blob=True)))
