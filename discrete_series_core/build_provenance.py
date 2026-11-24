#!/usr/bin/env python3
"""Reproduce DC source provenance from immutable Git objects, without a Lean build.

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


B = 'src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/'
KC = B + 'CasimirCoefficients/'
BC = B + 'BochnerInequality/'
DE = B + 'DiscreteSeriesExistence/'
FD = B + 'FormalDegree/'
AV = B + 'AnalyticVectors/'
RR = B + 'RigidityTheorems/'
QD = 'src/Formalism/FormalDegreeBessel/StatementDS.lean'
RF = 'src/Formalism/SharpRestriction/CuspSpanNormBounds/RelevantZeroGramTerms.lean'
DR = 'src/Formalism/LocalToGlobal/BesselHermitianTheta/DefsReal.lean'
DT = 'src/Formalism/LocalRingCardinality/DataTies.lean'
COMMON = ('Ordinary finite-dimensional complex/compact representation theory, Young symmetrizers, PBW, Haar integration, differential calculus, Hilbert-space spectral theorem, compact-group averaging, monotone convergence, and the Euler beta integral. Exact regular integral parameters, actual unitary group and source conventions are stated in each proof. No noncompact discrete-series existence or classification theorem is imported in DC1-17.')
GAP = ('For a noncompact signature, lambda is strictly decreasing, lambda_i-(n-1)/2 is integral, and every opposite-sign gap is at least h>max(npq+1,16n min(p,q)+8sqrt(2min(p,q))). Statements explicitly called rigidity use only h>npq+1 once a model is supplied. Compact and ranks zero/one are separate branches.')
HC = ('Explicit named established theorem HC-Deg, NOT reconstructed: Harish-Chandra, Discrete series for semisimple Lie groups II, Acta Math.116(1966), section40 Corollary2 p94 and section41 Theorem16 p96, gives formal degree proportional to the absolute positive-root product of a regular infinitesimal parameter, with constant independent of parameter/packet. DC16-18 calculate the exact compact-dual constant and prove the compact-center reduction. All DC18-22 uses of degree are conditional on HC-Deg.')
VOL = ('Actual VolTieG on the very same D is supplied. If obtained from GV18-19, their explicitly unreconstructed unitary Tamagawa-number theorem remains an additional premise; positivity of a stored volume alone is insufficient.')
CORE = ('Retained literal same-object coreOfLay data: K,X,f,T,Lay(X.toD7), Over, RecOK, LedOK, actual xi/Wt/MuIsW, forced-prime inclusion, GatNum, untwisted row vanishing, MtStableAt, primitive type-character identities, exact Q=T.Q and kprime=T.k, and the same-stage scale/dsig equalities. No automatic dependent-layout transport and no empty-twist promotion.')
BOUND = ('Human mathematical reconstruction only; no Lean build or kernel replay, no formalization of the replacement proofs, no RH/GRH conclusion. Universal DiscreteSeriesExist/FormalDegreeFormula2/RealOf remain separate from the restricted actual row supplier.')

def cl(n,title,statement,deps,srcs,hc=False,extra=(),relation=None):
    return dict(id=f'DC{n}',title=title,status='derived_simplification',statement=statement,
      depends_on=deps,assumptions=[COMMON,BOUND]+([HC] if hc else [])+list(extra),
      named_classical_inputs=['HC-Deg'] if hc else [],
      mathematical_status='proved_conditionally_on_explicit_unreconstructed_classical_input' if hc else 'proved_under_exact_stated_data_and_background_hypotheses',
      proof_location=dict(file='main.tex',anchors=[f'DC{n}']),
      expanded_notes=dict(file='report.txt',section=f'DC{n}'),
      source_relation=relation or 'Source-exact human reconstruction with explicit hypotheses and normalization; pinned declarations are locators, not imported human proofs.',
      sources=srcs)

claims=[
cl(1,'Integral compact lowest type from the actual parameter',
 'The source lowK=lambda+rhoN-rhoC is integral and compact-dominant. A finite Young-symmetrizer representation, determinant twist and averaged metric give literal KType.',[],
 ss(QD,'IsHCParam lowK','literal_interface')+
 ss(B+'IsInfUnitary.lean','rho rhoC rhoN lowK')+
 ss(KC+'PsiExistsStatement.lean','KType','literal_interface')+
 ss(B+'HighestWeights/Exists.lean','kType_exists_of_dom kType_exists')),
cl(2,'Actual principal-minor average and normalization',
 'Integral leading-minor powers give Phi; compact probability averaging gives P(1)=I and P(exp(-X))=P(exp X). The inverse in the source is in the matrix argument.',['DC1'],
 ss(KC+'IsClosedKset.lean','IsMu lead PhiM OmegaSet muK projW psM PsiM','literal_construction')+
 ss(KC+'ExistsMu.lean','exists_mu')+
 ss(KC+'Minors.lean','lead_tri_mul lead_posDef')+
 ss(KC+'PhiFacts.lean','isOpen_omega posSet_subset_omega phiM_differentiableOn phiM_tri_mul phiM_posDef phiM_one')+
 ss(KC+'PsiMExpFormula.lean','inv_conj_exp psiM_exp_formula')),
cl(3,'Compact integration-by-parts and local holomorphic kernel',
 'The compact-root divergence is -4 rhoC; mu=Lambda+2rhoC gives both block differential identities. The actual polar kernel has local extension T(k0)P(g^-1 k0), covariance and ambient smoothness.',['DC1','DC2'],
 ss(KC+'LowMinusUpExpand.lean','lowMinusUp_expand scal Ssum_eq pt psM_inf_herm')+
 ss(KC+'InfRightA.lean','infR_conj')+ss(KC+'InfRight.lean','infR_skew psM_inf_right')+
 ss(KC+'PsMInfNhd.lean','psM_inf_nhd')+ss(KC+'LocalB.lean','lcB_const')+
 ss(KC+'PsiMLocal.lean','psiM_local')+
 ss(KC+'ToMKMulInv.lean','psiM_kexp psiM_equiv psiM_one')),
cl(4,'Full central parameter rather than a Casimir surrogate',
 'Triangular commutation gives Casimir c_lambda and the literal Capelli eigenpolynomial product(Y+lambda_i), hence the complete unordered infinitesimal parameter.',['DC2','DC3'],
 ss(QD,'capP','literal_plus_sign')+
 ss('src/Formalism/FormalDegreeBessel/StatementIO.lean','Top qminorOp qdetOp capelli','literal_column_order')+
 ss(KC+'PhiCas.lean','lhol_phiM_lower lhol_phiM_diag casL_phiM')+
 ss(KC+'CapPhi.lean','capelliC_negT phiS_up phiS_diag capelliC_phiS cap_phiM')+
 ss(KC+'PsiCapelliStatement.lean','PsiCapelliStatement','literal_interface')+
 ss(KC+'TopCap.lean','psiCapelli psiAllCap')),
cl(5,'Explicit logarithmic leading-minor lower bound',
 'The elementary exponential-moment bound and Cauchy-Binet variance identity imply log Delta_m(exp Y)>=one-quarter min(1,1/(sqrt(2q0)r)) times the crossing-entry square sum.',['DC2'],
 ss(KC+'DecLog.lean','logSumExp_lower')+
 ss(KC+'DecALogLower.lean','decA_lead_re decA_log_lower')+
 ss(KC+'DecSum.lean','dec_weighted')),
cl(6,'Actual kernel decay and Haar integrability',
 'Telescoping leading-minor weights gives dimension-free exp[-h/8 min(r^2,r/sqrt(2q0))] decay. Explicit polar Jacobian bounds give the stated L1,L2 and weighted sufficient ranges.',['DC3','DC5'],
 ss(KC+'PhiDecayCore.lean','phi_decay_core phiM_exp_le psiM_dec')+
 ss(KC+'HaarPolar.lean','haar_polar_le')+
 ss(FD+'PolarHaar.lean','muPolar_isHaar')+
 ss(KC+'Integr.lean','psiM_integrable'),extra=[GAP]),
cl(7,'Every derivative is an actual L2 smooth vector',
 'Cutoff integration by parts for 2C_K-C_G proves all derivative-word L2 bounds for the finite compact-stable kernel entries, then L2 orbit differentiability; j(T) is injective.',['DC3','DC4','DC6'],
 ss(DE+'IsSmoothL2OfCasimirEigen.lean','IsSmoothL2 IsSmoothL2.Eab isSmoothL2_of_casimir_eigen')+
 ss(DE+'EqZeroOfDatumEmbeddingEqZero.lean','IsPsiFor jfun uniformisationL2 eq_zero_of_datumEmbedding_eq_zero')+
 ss(DE+'DatumIrr.lean','jSm jSm_injective datumV_isKIrrHW'),extra=[GAP]),
cl(8,'Casimir identity and negative first-layer elimination',
 'The signed adjoint identity yields the exact highest-vector Casimir equation. Compact tensor decomposition and cross-Casimir eigenvalues identify positive/negative slots; the negative multiplication map vanishes.',['DC1','DC4','DC7'],
 ss(B+'IsInfUnitary.lean','adjSign IsInfUnitary','literal_adjoint_convention')+
 ss(B+'CasimirAlgebra/KhwLowKSubRootEqZero.lean','casimir_khw_identity khw_lowK_sub_root_eq_zero')+
 ss(BC+'NumRho.lean','two_dot_rhoC_rhoN_le')+
 ss(BC+'CrossOpEigGap.lean','crossOp_eig_gap')+
 ss(BC+'NcVOneDecomp.lean','ncV_one_decomp Wm_khw Wp_bound')+
 ss(BC+'SchPhiOneApply.lean','phi_one_Wm'),extra=[GAP]),
cl(9,'Finite PBW-layer coercivity and Vogan norm',
 'Minimal tensor lifts and each positive slot give cK(nu)>=cK(Lambda)+2j(h-n+1), even under the Schmid relation alone. This proves unique lowest type, the literal minimum norm and fixed-weight layer bounds.',['DC8'],
 ss(BC+'SchPhiOneApply.lean','phi_Wm_last phi_Wm_position')+
 ss(BC+'CrossOpSlotBound.lean','position_perp crossOp_position_bound')+
 ss(BC+'BochIneq.lean','bochner_ineq')+ss(BC+'LayerBound.lean','khw_layer_succ_bound')+
 ss(BC+'SchForm.lean','phi_Wm_position_of_sch khw_layer_succ_bound_of_sch khw_lowK_mem_of_sch sch_of_no')+
 ss(BC+'Numerics.lean','gap_gt vogan_num degree_num')+
 ss(BC+'CasimirGapAtNoncompactWeight.lean','khw_mem_layer'),extra=[GAP]),
cl(10,'Analytic-vector closure and exact compact multiplicities',
 'Explicit factorial derivative growth gives group invariance of the closed generated module. Compact character projectors land in bounded finite PBW layers, so completion introduces no extra lowest type and gives admissibility/K-finite smoothness.',['DC7','DC9'],
 ss(AV+'Analytic.lean','exists_orbit_bound orbit_hasSum_taylor')+
 ss(AV+'Closure.lean','exp_apply_mem_topologicalClosure closure_genSub_stable')+
 ss(DE+'PropsKfin.lean','data_kfin_le')+ss(DE+'PropsAdm.lean','data_admissible')+
 ss(DE+'PropsLowK.lean','data_lowK_eq'),extra=[GAP]),
cl(11,'Irreducibility and the actual matrix coefficient',
 'The unique lowest K-type makes every invariant projection zero or identity. Compact Schur averaging identifies the projected translate and proves coefficient=a times Psi without assuming positivity of Psi.',['DC10'],
 ss(RR+'ClosGenStable.lean','closGen_stable rigid_irred')+
 ss(DE+'FormulaF.lean','formulaF formulaF_sigLam dec_sigLam')+
 ss(DE+'PsiFunct.lean','psi_funct'),extra=[GAP]),
cl(12,'All coefficients and full four-vector Schur orthogonality',
 'A closed coefficient operator and irreducibility show all coefficients lie in L2. Polarization proves IsFdeg, vector-independent fdegOf and inverse Haar scaling. The constructed representation satisfies every literal IsDS clause.',['DC6','DC11','DC9'],
 ss(RF,'IsURepOn IsIrredOn coefOn IsSqIntOn IsFdeg fdegOf IsDS','literal_interface')+
 ss(DE+'SigLamMemLpOfNe.lean','sigLam_memLp_of_ne sqInt_sigLam')+
 ss(DE+'IsDSSigLam.lean','isDS_sigLam')+
 ss(IW+'ExistsIsFdegSmulOfIsDS.lean','exists_isFdeg_smul_of_isDS')+
 ss(IW+'ExistsDiscreteSeriesFormalDegreeProduct.lean','fdegOf_eq_of_isFdeg'),extra=[GAP]),
cl(13,'Rigidity of every literal IsDS in the actual gap regime',
 'Smoothing preserves the lowest compact type. Vogan-minimality kills the negative first layer; the diagonal-module argument recovers Casimir and a unitary intertwiner, hence all central eigenvalues for every source IsDS.',['DC9','DC10','DC11','DC12','DC4'],
 ss(DE+'Arbitrary.lean','exists_datum_of_isKTypeOf equiv_sigLam_of_cas dsUnique_of_cas')+
 ss(DE+'CFCore.lean','casimir_eq_casVal_of_model')+
 ss(DE+'EquivSigLamOfIsDS.lean','cf_no_of_vogan casOnDatum_of_isDS equiv_sigLam_of_isDS isDS_props_of_gap')+
 ss(DE+'DiscreteSeriesUniqueLargeGap.lean','final_deg_DSUniqG discrete_series_unique_large_gap'),extra=[GAP]),
cl(14,'Literal eventual row gap and threshold ordering',
 'The exact row head/tail/sign parameters satisfy the gap from b-successor gaps. Explicit Ev witnesses eps0=1,ch0=6N+1,x0=max(max(4,A),M^4) give A rank^N<=h0 and M<=m, hence GapHyp with A16,N19,M1801.',['DC1'],
 ss(RF,'dimS_eq lamS epsS lamSH epsSH','literal_row_parameter')+
 ss(IW+'RowHCParameterIsHCParamAndFormalDegreePos.lean','lamS_succ_lt lamS_int lamSH_isHCParam')+
 ss(IW+'EventuallyNodeGapGeRankPow.lean','rank_le le_m b_eq eventually_nodeGap_ge_rank_pow ev_nodes')+
 ss(IW+'GapHypOfNodes.lean','gapHyp_of_nodes ev_gapHyp')+
 ss('src/Formalism/LocalToGlobal/SiegelLatticeTheory/HaarTransversals/ConcreteSettingExists.lean','GapHyp','literal_gap')),
cl(15,'Actual row discrete-series existence and uniqueness',
 'For every GapHyp D and every real place, construct the same actual epsSH/lamSH representation, including completeness/nonzero/unitary/irreducibility/square-integrability/lowest-minimal type, admissibility, full central character and uniqueness. Compact/rank0/rank1 branches are explicit.',['DC12','DC13','DC14'],
 ss(DE+'FinalClosed.lean','dsExistsG_closed')+
 ss(DE+'FinalExists.lean','final_existsG_of')+
 ss(DE+'EquivSigLamOfIsDS.lean','compact_isDS_unique isDS_props_of_gap')+
 ss(IW+'ExistsDiscreteSeriesFormalDegreeProduct.lean','exists_isDS_isFdeg_trueDsig','restricted_endpoint_replacement')+
 ss(DF,'DiscreteSeriesExist','stronger_universal_not_claimed')),
cl(16,'Exact compact-dual quotient Haar density',
 'GV tangent normalization gives Cpq=pi^-pq Wn/(Wp Wq) on the bounded matrix domain, whose invariant density is Cpq det(1-Z*Z)^-n dZ.',['GV5','GV17'],
 ss(CD,'IsOmegaLeb OmegaDensity CDHaar','literal_normalization')+
 ss(DF,'CdScaleIs trueScale','literal_same_measure')+
 ss(FD+'PmatIsHermitian.lean','cPQ')+
 ss(FD+'IntMuCD.lean','lintegral_muCD'),
 relation='Explicit bounded-domain change-of-variables proof refining the same compact-dual normalization; no unproved gauge-equivalence premise.'),
cl(17,'Explicit scalar Bergman calibration and beta integral',
 'A scalar holomorphic unitary irreducible model on the matrix ball has degree 1/(Cpq I(s-n)); row-by-row beta integration and its central weights give Vandermonde/Wn.',['DC12','DC16'],
 ss(FD+'FdConst.lean','fdc_vand_split formal_degree_constant_eq','alternative_source_normalization_route')+
 ss(QD,'fdegHC','literal_target')+
 ss(RF,'IsFdeg fdegOf','literal_degree'),
 relation='Independent elementary calibration proof by weighted holomorphic functions and row beta integrals. The source uses a different asymptotic/Laplace route, which remains separately identified rather than imported.'),
cl(18,'Conditional Harish-Chandra degree with the constant pinned',
 'Assuming only named HC-Deg for regular infinitesimal parameters, compact-center reduction and DC17 force exactly d=Vandermonde/Wn for the actual compact-dual Haar, including all packets.',['DC16','DC17'],
 ss(DF,'FormalDegreeFormula₂','stronger_literal_interface')+
 ss(D+'PublishedTheorems/AutomorphicForms₂/FormalDegreeCompactDualIff.lean','FormalDegreeCompactDual','source_wrapper_not_proof')+
 ss(FD+'ThmFD.lean','thmFD','optional_internal_replacement_target'),hc=True),
cl(19,'Every literal large-gap IsDS has the exact source degree',
 'Full central-parameter identification, rigidity, exact CdScaleIs and Schur orthogonality give the fdegOf formula for all source IsDS and all nonzero vectors, plus uniqueness of IsFdeg d.',['DC4','DC13','DC18','DC12','GV17'],
 ss(DF,'CdScaleIs FormalDegreeFormula₂','literal_measure_and_quantifiers')+
 ss(IW+'ExistsDiscreteSeriesFormalDegreeProduct.lean','fdegOf_eq_of_isFdeg exists_isDS_isFdeg_trueDsig','restricted_endpoint_replacement')+
 ss(IW+'ExistsDiscreteSeriesFormalDegreeProductStatement.lean','exists_discreteSeries_formalDegree_product','restricted_endpoint_replacement'),hc=True,extra=[GAP]),
cl(20,'All four actual RealTied fields under GapHyp',
 'On the same D with GapHyp, actual VolTieG, trueScale and trueDsig equalities, construct cdScale, dsig, dsig_all and vol. GV can supply the actual-volume field under its separately retained Tamagawa theorem.',['DC15','DC19','GV17','GV19'],
 ss(RT,'RealTied','four_field_interface')+ss(DR,'IsDsig','existential_degree_field')+ss(DT,'dsigTie','universal_degree_field')+
 ss(IW+'LevelThreeToFour.lean','RealOf realOf real_of','universal_wrapper_restricted_here'),hc=True,extra=[VOL]),
cl(21,'Same-object Core join with all 21 fields audited',
 'DC20 discharges the actual real field in coreOfLay; the exact retained layout/arithmetic/row/motive/NChoice witnesses populate the other fields on the same X, with no automatic dependent transport or empty-twist promotion.',['DC20','GV21'],
 ss(AM+'RationalRootsDef.lean','RowLay MuIsW Core ExTrue','literal_field_interfaces')+
 ss(AM+'ExistsStagesClauses.lean','rowLay_iff coreOfLay exists_stages_clauses loc_Q','actual_join_and_partial_constructor'),hc=True,extra=[VOL,CORE]),
cl(22,'Restricted level-three-to-four transition and exact residual boundary',
 'The actual later GapHyp survives both same-B stage replacements; the source lv4/step proof can use restricted DC20 at both real-field calls, keeping LevelThreeCondition/SatNew/PackEx and actual SameL/column/carrier transport. Universal wrappers are not required on this route but remain unproved globally.',['DC14','DC20','SE10','GV19'],
 ss(IW+'ExistsSStageTrue.lean','exists_sStage_true','actual_stage_choice')+
 ss(IW+'LevelThreeToFour.lean','RowHyp SatNew satOfDiscreteSeries PackEx sat_col lv4_of step_of stepW_has4','retained_or_restricted_transition_interfaces')+
 ss(AM+'RationalRootsDef.lean','ExTrue','stronger_global_endpoint_retained'),hc=True,extra=[VOL,
 'Retained exact LevelThreeCondition, SatNew, PackEx, volume-to-mass implication and real-idempotent tie; SExt.none only. Existing actual level-three data and explicit same-stage transport witnesses are required.'])
]

main=(HERE/'main.tex').read_bytes()
markers=list(re.finditer(rb'^\\paragraph\{(DC\d+):',main,re.M))
assert [m.group(1).decode() for m in markers]==[c['id'] for c in claims]
for i,(m,c) in enumerate(zip(markers,claims)):
    end=markers[i+1].start() if i+1<len(markers) else len(main)
    raw=main[m.start():end]
    a=main[:m.start()].count(b'\n')+1
    b=a+len(raw.splitlines())-1
    assert b''.join(main.splitlines(keepends=True)[a-1:b])==raw
    c['proof_location'].update(paragraph_sha256=digest(raw),line_start=a,line_end=b,bytes=len(raw))

prior=HERE.parent/'history/version_0_21/provenance.json'
old=json.loads(prior.read_text())
old_ids={c['id'] for c in old['claims']}
assert not old_ids.intersection(c['id'] for c in claims)
seen=set(old_ids)
for c in claims:
    assert set(c['depends_on'])<=seen,(c['id'],set(c['depends_on'])-seen)
    seen.add(c['id'])

target_specs=[
 ('DC-next1','Universal existence beyond the actual large-gap route',DF,'DiscreteSeriesExist',
  'DC15 proves actual GapHyp row existence. The all-parameter regular integral wrapper, including arbitrarily small noncompact gaps, remains a stronger source-route expansion; it is not needed by DC22.', 'optional_source_route_expansion'),
 ('DC-next2','Universal source lowest-type formal-degree interface',DF,'FormalDegreeFormula₂',
  'DC19 proves the actual large-gap universal-representation/nonzero-vector conclusion conditional on named HC-Deg. The all-parameter lowest-type-to-infinitesimal-character bridge and full wrapper are not reconstructed.', 'stronger_universal_interface'),
 ('DC-next3','Optional internal formal-degree proof replacing HC-Deg',FD+'ThmFD.lean','thmFD',
  'Reconstruct the genuine tensor-translation ratio, Lap.Base.TangentPairingStatement and exact upper/lower Laplace asymptotics to remove HC-Deg. DC16-18 already pin the compact-dual constant independently.', 'replacement_of_named_classical_input'),
 ('DC-next4','Actual spectral replacement rather than real normalization',IW+'LevelThreeToFour.lean','SatNew',
  'DC20 supplies all four real fields at actual gap parameters; still construct the same-object spectral replacement and its universal SameL property, retaining the precise cusp, infinitesimal-character, rapid-decay and row-dimension inputs until reconstructed.', 'genuine_remaining_supplier'),
 ('DC-next5','Actual integrable spectral packet',IW+'LevelThreeToFour.lean','PackEx',
  'Construct SPack and actual integral of ph from the exact Bessel/row/Siegel-Weil inputs. Neither a local discrete series nor a volume normalization supplies this packet.', 'genuine_remaining_supplier'),
 ('DC-next6','Compatible nonempty Core data',AM+'RationalRootsDef.lean','Core',
  'DC21 supplies only the exact conditional same-object coreOfLay join after DC20. Retain actual Lay/RecOK/LedOK, forced nonempty twists, MuIsW, row vanishing, motive stability, character and NChoice compatibility, with genuine dependent transports.', 'genuine_remaining_supplier'),
 ('DC-next7','Full later exact Core existence',AM+'RationalRootsDef.lean','ExTrue',
  'The restricted DC22 transition still requires actual level-three data, LevelThreeCondition, SatNew, PackEx, same-data transport and the named HC-Deg/volume inputs. It is not unconditional ExTrue or RH/GRH.', 'genuine_remaining_supplier')]
targets=[]
for tid,title,p,n,scope,role in target_specs:
    src=source(p,n,'remaining_or_optional_scope')
    targets.append(dict(id=tid,title=title,scope=scope,role=role,
      optional_for_current_reconstruction=role=='optional_source_route_expansion',sources=[src]))

fields=[]
inventories=[(RT,'RealTied','cdScale dsig dsig_all vol','DC20'),
 (AM+'RationalRootsDef.lean','Core','isOver xi Wt mu forced fval O col gatNum gy row mtStable th_io gauge_def real dsig_eq del etaF chiT nch_tie nch_Q','DC21'),
 (AM+'RationalRootsDef.lean','RowLay','rrDef rationalRoots_def kap_def lam_def bu_def ft_occ untw idx kapR_def','DC21'),
 (AM+'RationalRootsDef.lean','MuIsW',"inj range mu0 star star' tw on off sub supp",'DC21')]
for p,n,names,cid in inventories:
    src=source(p,n,'field_inventory')
    fields.append(dict(record=n,claim=cid,field_count=len(names.split()),fields=names.split(),source=src,
      status='all_four_constructed_under_explicit_hypotheses' if n=='RealTied' else 'same_object_join_with_retained_fields_explicit'))

reviews=[]
for filename in ['discrete_series_core_independent_review.json','root_reviews_discrete_series_core.json']:
    p=HERE.parent/'reviews_v0_22'/filename
    if not p.exists():continue
    rev=json.loads(p.read_text())
    for cid,h in rev['reviewed_claims'].items():
        actual=next(c['proof_location']['paragraph_sha256'] for c in claims if c['id']==cid)
        assert (h.get('paragraph_sha256') if isinstance(h,dict) else h)==actual,(filename,cid)
    reviews.append(dict(file='reviews_v0_22/'+filename,sha256=digest(p.read_bytes()),reviewer=rev.get('reviewer'),
                        author=rev.get('author'),result=rev.get('result'),reviewed_claims=rev['reviewed_claims']))

endpoints=[
 dict(id='DC-completed1',declaration='dsExistsG_closed',claims=['DC1','DC2','DC3','DC4','DC5','DC6','DC7','DC8','DC9','DC10','DC11','DC12'],sources=ss(DE+'FinalClosed.lean','dsExistsG_closed','exact_completed_endpoint'),scope='Actual constructive large-gap predicate with all literal IsDS fields; no noncompact existence theorem premise.'),
 dict(id='DC-completed2',declaration='isDS_props_of_gap',claims=['DC13'],sources=ss(DE+'EquivSigLamOfIsDS.lean','isDS_props_of_gap','exact_restricted_endpoint'),scope='Restricted to the constructive bound DC.2 / H_epsilon, hence all actual GapHyp rows: rigidity, admissibility, smooth K-finite vectors and full central character without general classification. The weaker literal source threshold h>npq+1 is not newly closed outside this range unless a model is separately supplied.'),
 dict(id='DC-completed3',declaration='exists_discreteSeries_formalDegree_product',claims=['DC14','DC15','DC19'],sources=ss(IW+'ExistsDiscreteSeriesFormalDegreeProductStatement.lean','exists_discreteSeries_formalDegree_product','exact_restricted_endpoint'),scope='Restricted to actual GapHyp row parameters; exact existential and all-representation degree clauses conditional on named HC-Deg.'),
 dict(id='DC-completed4',declaration='LevelThreeToFour.realOf',claims=['DC20'],sources=ss(IW+'LevelThreeToFour.lean','realOf','exact_restricted_endpoint'),scope='GapHyp-restricted replacement on the same D with actual volume and exact trueScale/trueDsig; HC-Deg retained, GV Tamagawa retained if used for volume.'),
 dict(id='DC-completed5',declaration='coreOfLay',claims=['DC21'],sources=ss(AM+'ExistsStagesClauses.lean','coreOfLay','exact_conditional_join_endpoint'),scope='Exact 21-field same-object join; only representation/degree real-field inputs narrowed, all other genuine layout/arithmetic/row/motive premises explicit.'),
 dict(id='DC-completed6',declaration='LevelThreeToFour.step_of',claims=['DC22'],sources=ss(IW+'LevelThreeToFour.lean','step_of','exact_restricted_transition_endpoint'),scope='SExt.none restricted transition uses actual eventual gap at both real-record calls; SatNew/PackEx/LevelThreeCondition and all same-object transports retained.')]

manifest=dict(schema_version='1.3',artifact_version='0.22',repository=dict(url=URL,commit=PIN),
  files=[files[p] for p in sorted(files)],source_file_count=len(files),
  claim_source_links=sum(len(c['sources']) for c in claims),
  distinct_claim_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}))
provenance=dict(schema_version='1.3',artifact_version='0.22',owner='/root/global_frame',
 repository=dict(url=URL,commit=PIN),
 scope='Constructive actual large-gap discrete series and exact compact-dual normalization; named HC-Deg retained for degree, actual volume/other Core data retained where stated. No universal wrapper or RH/GRH claim.',
 range_convention='Inclusive original Git-blob lines with exact newline bytes; trailing blank lines before next top-level boundary omitted.',
 verification=dict(full_file_bytes_compared_to_pinned_git_blob=True,range_bytes_compared_to_pinned_git_blob=True,
  missing_sparse_files_read_with_git_show=True,declaration_boundaries_checked=True,old_claim_id_collisions_checked=True,
  component_dependency_order_checked=True,exact_raw_paragraph_lines_and_bytes_checked=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Human proof with precise hypotheses. Explicit classical HC-Deg and volume/Core premises remain conditional where listed.'),
 claims=claims,field_inventories=fields,completed_endpoints=endpoints,
 named_classical_inputs=[dict(id='HC-Deg',status='explicitly_retained_unreconstructed_established_theorem',
  citation='Harish-Chandra, Discrete series for semisimple Lie groups II, Acta Mathematica116(1966), sections40-41, Corollary2 p94 and Theorem16 p96.',
  doi='10.1007/BF02392813',url='https://repository.ias.ac.in/30833/1/336.pdf',
  exact_used_content=HC,normalization_resolution='DC16-18 derive the finite-center conversion and pin the group/Haar constant by an explicit Bergman beta integral.')],
 reviews=reviews,source_manifest='source_manifest.json',
 artifact_hashes=dict(main_tex=digest(main),report_txt=digest((HERE/'report.txt').read_bytes())),
 counts=dict(claims=len(claims),claim_source_links=manifest['claim_source_links'],
  distinct_claim_ranges=manifest['distinct_claim_ranges'],indexed_source_files=len(files),
  field_inventories=len(fields),inventoried_fields=sum(x['field_count'] for x in fields),
  next_target_ranges=len(targets),attached_reviews=len(reviews)))
for name,obj in [('source_manifest.json',manifest),('provenance.json',provenance),
 ('next_targets.json',dict(artifact_version='0.22',component='discrete_series_core',completed_endpoints=endpoints,targets=targets))]:
    (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
lines=['DC source locators; immutable commit '+PIN,
       'Inclusive ranges; SHA256 full file / exact range. No Lean/kernel replay.','']
for c in claims:
    q=c['proof_location']
    lines.append(f"{c['id']} | main.tex:{q['line_start']}-{q['line_end']} | {q['bytes']} bytes | paragraph {q['paragraph_sha256']}")
    for s in c['sources']:
        lines.append(f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | full {s['full_file_sha256']} | range {s['range_sha256']} | {s['role']}")
        lines.append('  '+s['url'])
    lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps(provenance['counts'],sort_keys=True))
print('main.tex SHA256 '+digest(main))
print('report.txt SHA256 '+digest((HERE/'report.txt').read_bytes()))
print('provenance.json SHA256 '+digest((HERE/'provenance.json').read_bytes()))



