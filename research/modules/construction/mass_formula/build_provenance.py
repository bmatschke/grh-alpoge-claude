#!/usr/bin/env python3
"""Reproduce the MF source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
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
AL = D + 'Proofs/AdelicLatticeProofs/'
FM = D + 'Proofs/FlagMeasures/'
GI = D + 'Proofs/GlobalInterpolation/'
P = 'src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/UnimodularClassRepresentatives/'
ST = 'src/Formalism/HermitianLattices/StatementMass.lean'
SL = 'src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLattice.lean'
TH = 'src/Formalism/SharpRestriction/GlobalSchurBounds/ThickPlacesCorollaryOfAnyTranslate.lean'


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


LD = P + 'LocalDensityRatio.lean'
SC = P + 'SigmaCount.lean'
MS = P + 'MassSt.lean'
COMMON = ('Number-field and Dedekind-domain algebra, completions, residue fields, weak approximation, finite-dimensional real and nonarchimedean linear algebra, Haar integration, local analytic change of variables, Riemann sums, dominated convergence and absolutely convergent Euler products are ordinary background. Local dyadic trace/norm and correction arguments are explicitly proved or reused from DR1. Full integral lattices may be globally projective.')
BOUND = ('Human reconstruction only: no Lean compilation, kernel replay or formalization of replacement proofs. No RH/GRH conclusion. Geometric VolumeEqMass2/VolTie and actual compatible Core/arithmetic/theta data are not implied by the mass ratio.')
HM = ('Named external established theorem, not reconstructed: Hasse–Minkowski over number fields, in the isotropy formulation. MF4 proves its exact reduction to HermRepUnram. No mass formula, Tamagawa theorem or representation-average theorem is imported.')


def cl(n, title, statement, deps, sources, hm=False, assumptions=(), relation=None):
    return dict(id=f'MF{n}', title=title, status='derived_simplification',
        statement=statement, depends_on=deps,
        assumptions=[COMMON, BOUND] + ([HM] if hm else []) + list(assumptions),
        proof_location=dict(file='main.tex', anchors=[f'MF{n}']),
        expanded_notes=dict(file='report.txt', section=f'MF{n}'),
        mathematical_status=('proved_from_explicit_classical_Hasse_Minkowski_and_declared_background'
                            if hm else 'proved_under_exact_declared_background_and_data_hypotheses'),
        source_relation=relation or 'Human proof of the literal source conclusion; completed local coordinates are related to the source rational-local definitions explicitly. Source proof bytes are locators, not assumed mathematical suppliers.',
        sources=sources)


claims = [
cl(1, 'Fixed field, relative different and exact Euler/covolume conventions',
   'IsCMUnram gives a totally imaginary quadratic extension of its totally real fixed field, a unit relative different even at dyadic primes, disc(F)=(2v)^f, the real and complex covolumes, and the exact fixed-field Euler product L_m=lValEta(E,m) for m>=2.',
   ['DR1','QW1'],
   ss(ST,'fDeg vInv eulerFac lValEta IsCMUnram','literal_interface') +
   ss(P+'ExistsFixF.lean','starFixed exists_fixF') +
   ss(P+'MassLandA.lean','exists_skew eq_add_mul_skew finrank_cmF isReal_cmF') +
   ss(P+'DifferentIdealEqTop.lean','differentIdeal_eq_top natAbs_discr discr_pos discrTower') +
   ss(P+'CovolumeIntegerLatticeEq.lean','nrComplexPlaces_eq_fDeg finrank_eq_two_fDeg vInv_pos covolume_integerLattice_eq') +
   ss(P+'LValEtaEqLValEtaF.lean','lValEta_eq_lValEtaF eulerEta')),
cl(2, 'Integral Hermitian classification at every unramified finite place',
   'Unit norms are onto by trace lifting; integral Hermitian lattices have Jordan exponents, and every local rational form has a lattice of determinant valuation at most one. In that minimal range rank and determinant valuation determine integral isometry type, with a supplied norm-one vector kept first.',
   ['MF1','DR1'],
   ss(P+'ExistsIsomLocFOfVdZero.lean','exists_isom_locF_of_vd_zero exists_isom_locF_of_vd_one') +
   ss(P+'ExistsOrthTransfer.lean','sd_main asd_main') +
   ss(P+'ExistsLatticeVdLeOne.lean','exists_lattice_vd_le_one')),
cl(3, 'Exact norm orbits and rational weak approximation',
   'An explicit Hermitian reflection carries any two vectors of equal nonzero norm to one another. The Cayley map proves rational weak approximation at finitely many places, so completed lattice orbits and the source rational-local orbits agree exactly, including on the orthogonal complement.',
   ['MF2'],
   ss(P+'SumOrbitsEquivariant.lean','exists_move') +
   ss(P+'ExistsOrthTransfer.lean','exists_orth_transfer') +
   ss(P+'ExistsIsomLocFOfVdZero.lean','exists_isom_locF_of_vd_zero exists_isom_locF_of_vd_one') +
   ss(P+'ExistsLatticeVdLeOne.lean','exists_exact_near') +
   ss(LD,'locF fibLoc IsLocReps','literal_rational_local_interfaces'),
   relation='Reflection and rational Cayley weak approximation are replacement proofs. No strong approximation is asserted; open stabilizers give exact rational-local lattice actions.'),
cl(4, 'Binary Hermitian representation from named Hasse–Minkowski',
   'Over every finite split or unramified quadratic completion a binary Hermitian form represents every scalar. Applying the explicitly retained number-field Hasse–Minkowski theorem to the five-variable trace form proves the literal HermRepUnram and representation of every totally positive norm in rank at least two.',
   ['MF1','MF2'],
   ss(P+'MassLandSt.lean','TotPos HermRepUnram','literal_interface') +
   ss(FM+'BinaryHermitianRepresents.lean','binary_hermitian_represents') +
   ss(FM+'BinaryHermitianFormRepresentsTotallyPositive.lean','represents_totallyPositive') +
   ss(AL+'ExistsCongrIffTraceFormsIsometricCm.lean','isotropic_of_locally_isotropic isotropic_of_indefinite','source_classical_route_counterpart'),
   hm=True, relation='Alternative proof from an explicit established external theorem. The source Hasse norm and quadratic local-to-global proof is not claimed reconstructed; the local representation and five-variable reduction are proved here.'),
cl(5, 'Matrix density as a specified Haar measure and LocalDensityRatio',
   'The source alphaL stabilizes positively. Its exact basis-independent Haar normalization is nu(L)=q^(-m vd(L)) alphaL(L). The common stabilizer index gives nu(A)orb(B,A)=nu(B)orb(A,B), hence literal LocalDensityRatio.',
   ['MF2'],
   ss(LD,'akCount alphaL discrIdeal vd orbCount LocalDensityRatio','literal_interface') +
   ss(P+'FirstFamilyOperatorEnd.lean','akCount_succ_fine alphaL_eq akCount_pos') +
   ss(P+'NkCountLocF.lean','akCount_locF vd_locF alphaL_pos') +
   ss(P+'ExtHomInjective.lean','nu nu_pos nu_mul_relIndex') +
   ss(P+'LocalDensityRatioHolds.lean','local_density_ratio_holds'),
   relation='Convergent local projection coordinates and an explicit Hermitian-space Jacobian replace the longer congruence-index calculation. The measure constant and orbit orientation are proved, not left as Haar normalizations to be supplied.'),
cl(6, 'Finite unitary orders and exact good-prime norm density',
   'Direct finite-field counts and trace lifting give alphaL=A_m for unimodular lattices and alphaN(n)/e_m=sum_{j=0}^{ord(n)}(eta^m q^(1-m))^j, including all dyadic unramified places.',
   ['MF2','MF5'],
   ss(LD,'alphaStd nkCount alphaN','literal_interface') +
   ss(P+'CardUnitaryFin.lean','card_unitary_fin card_GL_fin') +
   ss(P+'LamGEqOneOfOrtho.lean','alphaL_of_vd_zero alphaStd_pos localMassFactor_of_valuation_eq_zero') +
   ss(P+'UnitaryDensityFieldFurther.lean','alphaN_unit alphaN_step alphaN_closed') +
   ss(P+'AlphaNOfVdZeroUnit.lean','alphaN_of_vd_zero_unit alphaN_rho_bound alphaN_rho_diff_bound')),
cl(7, 'General norm-density stabilization, uniform bounds and mean one',
   'For an arbitrary integral nondegenerate lattice, primitive derivative depth is at most vd. Splitting vectors by valuation proves stabilization for nonzero norm, uniform boundedness in rank>=2, local constancy away from zero and integral_R alphaN=1 with the actual finite-level normalization.',
   ['MF2'],
   ss(LD,'nkCount alphaN','literal_interface') +
   ss(P+'FirstFamilyOperatorEnd.lean','nkCount_succ_fine alphaN_eq nkCount_congr nkCount_le_nat') +
   ss(P+'NkCountLocF.lean','nkCount_locF nkCount_succ alphaN_congr nkCount_le') +
   ss(P+'TendstoMeanAlphaN.lean','sum_nkCount alphaN_eq_of_le tendsto_mean_alphaN') +
   ss(P+'TendstoSumBoxIdeal.lean','exists_abs_alphaN_le')),
cl(8, 'Finite local cut fibers and the relative orbit/density identity',
   'The explicit lattice sandwich makes each fibLoc finite and bounds cut determinant valuation by vd(L)+ord(n), giving finitely many cut types. Quotient Haar integration and finite orbit regrouping prove LIRatio, including empty fibers, with one scalar independent of L.',
   ['MF3','MF5','MF7'],
   ss(LD,'fibLoc IsIntegralAt IsLocReps psiP','literal_interface') +
   ss(SC,'repRatio LIRatio','literal_interface') +
   ss(P+'ExistsGlobalOfFibLocNeZero.lean','exists_locReps psiP_eq_sum') +
   ss(P+'RepRatioEqZero.lean','repRatio_eq repRatio_eq_zero liRatio') +
   ss(P+'NuGmapLocF.lean','nu_gmap_locF main_term') +
   ss(P+'ExtHomInjective.lean','extHom_injective autExt oM kap_eq')),
cl(9, 'Pin the local scalar and prove every LIStat clause',
   'A norm-one minimal reference lattice has unique complement type; finite isometry orbit counting gives alphaL=alphaN(1)alphaCut and pins the scalar. Exact form scaling then yields Psi_p=q^((m-1)(ord(n)+vd(L))) A_(m-1) alphaN/alphaL, with an actual global integral reference lattice and the rank-one empty complement handled.',
   ['MF2','MF3','MF5','MF8'],
   ss(SC,'LIPin','literal_interface') + ss(LD,'LIStat','literal_interface') +
   ss(P+'ExistsLatticeVdLeOne.lean','exists_exact_near exists_lattice_vd_le_one') +
   ss(P+'IsTotPosDefOfSmul.lean','alphaL_smul alphaN_smul isom_smul fibLoc_unscale isLocReps_scale alphaL_split') +
   ss(P+'LiPin.lean','core liPin') +
   ss(P+'LiStatOf.lean','liStat_of liStat')),
cl(10, 'A universal positive rank-one mass constant',
   'All positive Hermitian lines have the same finite genus quotient of balanced fractional ideals and the same finite norm-one unit stabilizer. Their common mass c1 is positive, and direct rank-one congruence counting gives every local lambda factor equal to one, proving MassConst in rank one.',
   ['MF3','MF5','IG9','CR4'],
   ss(LD,'MassConst lamP','literal_interface') +
   ss(P+'ExistsMassConstOne.lean','trace_pos exists_model exists_massConst_one') +
   ss(P+'AlphaStdOneNeZero.lean','akCount_eq alphaStd_one_ne_zero alphaL_eq localFactor_rank_one') +
   ss(P+'NormOneMkIff.lean','NormOne normOne_mk_iff card_normOne')),
cl(11, 'The archimedean ball count with exact determinant and covolume',
   'For every projective integral Hermitian lattice, D(L)=sqrt(N_E discrIdeal)=product q^vd. The weighted ellipsoid lattice count tends to (pi^m/m!)^f/(v^(fm) D(L)), and D is constant on the genus.',
   ['MF1','IG9'],
   ss(LD,'discrIdeal normD ballCount','literal_interface') +
   ss(P+'AbsNormSpanEqProd.lean','BrA.normD_eq_tprod integral_of_mem_genus normD_eq_prod') +
   ss(P+'CovolumeIntegerLatticeEq.lean','covolume_integerLattice_eq') +
   ss(P+'TendstoBallCount.lean','tendsto_ballCount')),
cl(12, 'Global weighted representation count by actual cut lattices',
   'For a totally positive norm n in rank>=2, binary representation supplies x0; two finite orbit-stabilizer arguments give R_L(n)=sum_[T] |F_T|/|Aut(T)| in the fixed orthogonal complement, with the exact reciprocal stabilizer weights.',
   ['MF3','MF4','IG9'],
   ss(MS,'repCount repMass','literal_interface') +
   ss(P+'SumOrbitsEquivariant.lean','fibG IsFibReps exists_move fibG_smul finite_stab_proj exists_fibReps repMass_eq_sum_fib'), hm=True),
cl(13, 'Patch actual local fibers and regroup complement genera',
   'Global extension fibers are finite products of their actual local fibers. Every finite tuple of allowed cut types patches inside the same rational complement. Under rank-(m-1) MassConst, finite regrouping proves R_L(n)=c_(m-1) product Psi_p.',
   ['MF8','MF12','LP1','LP2','LP3'],
   ss(P+'CardFibGEqProd.lean','fibLoc_eq_one card_fibG_eq_prod') +
   ss(P+'ExistsGlobalOfFibLocNeZero.lean','exists_locReps') +
   ss(P+'SumRegroup.lean','sum_regroup repMass_eq_prod_psi\'') +
   ss(P+'RepMassEqProdPsi.lean','repMass_eq_prod_psi'), hm=True,
   assumptions=['The rank-(m-1) MassConst assertion is the explicit induction hypothesis, discharged for all ranks in MF18. No arbitrary rational Hermitian-space local-global existence is inferred from lattice patching.']),
cl(14, 'The exact global factor identity before averaging',
   'LIStat and A_m=A_(m-1)e_m give R_L(n)=c_(m-1)lambda(L)D(L)^(-1)|Nn|^(m-1)S_L(n). Both lambda and the nonzero-n singular series have finite support; no infinite-average interchange is used.',
   ['MF1','MF6','MF9','MF11','MF13'],
   ss(LD,'lamP lamG singS','literal_interface') +
   ss(P+'FactorIdentity.lean','alphaStd_succ factor_identity tprod_localPsi_eq repMass_eq') +
   ss(P+'AbsNormSpanEqProd.lean','normD_eq_prod absNorm_span_eq_prod') +
   ss(P+'ALocEqRoL.lean','singS_eq'), hm=True,
   assumptions=['Rank-(m-1) MassConst is the induction hypothesis.']),
cl(15, 'Weighted ideal boxes and exact finite-place equidistribution',
   'Riemann sums give the fixed-ideal weighted box constant m^(-f)/(sqrt(disc F)Na Nc). A cube separation argument gives the uniform C/Na bound. Bounded local densities, residue steps and a q^(-j) exceptional-coset estimate give the finite-place mean including zero residues.',
   ['MF1','MF7'],
   ss(LD,'boxSet','literal_interface') +
   ss(P+'AbsNormLeOfMemIdeal.lean','absNorm_le_of_mem_ideal absNorm_le_pow eq_of_close card_box_le') +
   ss(P+'TendstoSumOfMean.lean','local_density_error_le_of_bounded_congruent tendsto_sum_of_mean') +
   ss(P+'TendstoSumBoxIdeal.lean','exists_abs_alphaN_le tendsto_sum_box_ideal') +
   ss(P+'ALocEqRoL.lean','prodS_bound')),
cl(16, 'Singular-series mean from a summably dominated divisor expansion',
   'The exact unimodular density expands S_L(n) into a finite divisor sum. Its normalized ideal contribution is bounded by C/(Na)^m, summable even at m=2. Dominated convergence and the Euler product give the literal limit m^(-f)L_m/sqrt((2v)^f).',
   ['MF1','MF6','MF7','MF15','QW1'],
   ss(P+'UnitaryDensityFieldFurther.lean','alphaN_closed') +
   ss(P+'ALocEqRoL.lean','aLoc_eq_roL roL_zero roL_diff prod_aLoc singS_eq prodS_bound') +
   ss(P+'TendstoWeightedTprod.lean','sum_eq_tsum tendsto_weighted euler_identity tendsto_weighted_tprod') +
   ss(P+'TendstoSingSSum.lean','dominated tendsto_singS_sum'),
   relation='A simpler exact geometric-divisor expansion replaces the source finite-difference Euler-product argument. The uniform ideal-box majorant explicitly justifies the infinite passage and preserves the exact constant.'),
cl(17, 'Compare the same vector count and derive the successor constant',
   'The exact zero-vector plus positive-norm decomposition, ball asymptotic and singular-series mean imply mass(L)=c_(m-1) R_m lambda(L), where R_m=(((m-1)!(v/pi)^m)^f/sqrt((2v)^f)) lValEta(E,m). Every normalization and positive cancellation is explicit.',
   ['MF11','MF14','MF16'],
   ss(P+'BoxInterEqEmpty.lean','sum_ballCount_eq') +
   ss(P+'MassConstSucc.lean','final_algebra normD_pos tendsto_left tendsto_right massConst_succ') +
   ss(ST,'massRatioRightSide','literal_interface') +
   ss(P+'MassRatioEqLvalue.lean','massRatio_eq_lvalue'), hm=True,
   assumptions=['Rank-(m-1) MassConst is the induction hypothesis.']),
cl(18, 'MassConst in all ranks and all integral projective lattices',
   'Starting from c1 and taking products of the positive successor factors proves mass(L)=c_m lambda(L) for every positive definite Hermitian rational space and integral full lattice. The local bad factors remain explicit.',
   ['MF1','MF10','MF17'],
   ss(LD,'MassConst','literal_interface') +
   ss(P+'SiegelMassRatioOfLI.lean','massConst_all') +
   ss(P+'MassConstSucc.lean','massConst_succ') +
   ss(P+'MassRatioEqLvalue.lean','massRatio_pos'), hm=True),
cl(19, 'The literal orthonormal-model and standard mass-ratio conclusions',
   'For IsOrthoLattice, every local lambda factor is one. Dividing adjacent constants proves SiegelMassRatio for all supplied orthonormal models and StandardLattice.SiegelMassRatioCM with the exact source quantifier M>=3 and normalization, conditional only on the named classical Hasse–Minkowski input and background.',
   ['MF6','MF18'],
   ss(ST,'IsOrthoLattice massRatioRightSide SiegelMassRatio','literal_interface') +
   ss(P+'FiniteDimensionalOfOrtho.lean','stdLat_isOrtho finrank_of_ortho isLattice_of_ortho isTotPosDef_of_ortho isIntegralLat_of_ortho') +
   ss(P+'LamGEqOneOfOrtho.lean','lamG_eq_one_of_ortho') +
   ss(P+'SiegelMassRatioOfLI.lean','siegelMassRatio_of_LI siegelMassRatio') +
   ss(FM+'SiegelMassRatioUnimodularDefinite.lean','siegelMassRatio_holds') +
   ss(GI+'MassRatioAllUnramifiedCmFields.lean','massRatio_all_unramified_cmFields') +
   ss(SL,'SiegelMassRatioCM SiegelMassRatioModels mass_ratio_of_general','literal_endpoint') +
   ss(TH,'standardMassRatio_of_modelMassRatio modelMassRatio_of_standardMassRatio modelMassRatio_iff_standard'), hm=True),
cl(20, 'Discharge QW mass supply without changing its data or thresholds',
   'The actual adjacent-rank mass law telescopes and supplies the mass premise of QW3/QW9. The epsilon range, threshold order, same PreCh, duStar/Dstar data and constant 30+(2+2C0)/epsilon remain unchanged. Geometric volume/Core, arithmetic and prime-estimate suppliers remain separate.',
   ['MF19','QW3','QW9'],
   ss(GI+'DimVRowPos.lean','mass_tel') +
   ss(GI+'WindowLower.lean','window_lower') +
   ss(SL,'VolumeEqMass₂ VolTie','retained_distinct_geometric_interfaces'), hm=True)
]

assert len(claims) == 20
ids = {c['id'] for c in claims}
assert len(ids) == 20
old_path = HERE.parent / 'history/version_0_19/provenance.json'
old = json.loads(old_path.read_text())
old_claims = old['claims'].values() if isinstance(old['claims'], dict) else old['claims']
old_ids = {c['id'] for c in old_claims}
assert not ids & old_ids
for c in claims:
    assert set(c['depends_on']) <= ids | old_ids, (c['id'], c['depends_on'])
    assert all(not d.startswith('MF') or int(d[2:]) < int(c['id'][2:]) for d in c['depends_on'])

mb = (HERE / 'main.tex').read_bytes()
rb = (HERE / 'report.txt').read_bytes()
paragraphs = {}
for i, c in enumerate(claims):
    marker = ('\\paragraph{' + c['id'] + ':').encode()
    start = mb.index(marker)
    stop = mb.index(('\\paragraph{MF' + str(i+2) + ':').encode()) if i+1 < len(claims) else len(mb)
    ph = digest(mb[start:stop])
    paragraphs[c['id']] = ph
    c['proof_paragraph_sha256'] = ph
    c['proof_location']['paragraph_sha256'] = ph

external_references = [
    dict(id='MF-HM-Kim', author='Sungjin Kim', title='Hasse-Minkowski Theorem',
         location='Theorem 1.1, page 1', url='https://www.csun.edu/~sungjin/HasseMinkowski.pdf',
         source_type='author-written mathematical notes', used_by=['MF4'],
         scope='General-number-field isotropy statement only. Later exposition specializes to Q; no claim that it reconstructs the general proof.',
         theorem_proof_reconstructed=False),
    dict(id='MF-HM-Hanke', author='Jonathan Hanke', title='Quadratic Forms and Automorphic Forms',
         edition='Expanded Arizona Winter School 2009 notes, May 16, 2011',
         location='Theorem 1.9.1 and Remark 1.9.2; printed page 20, PDF page 19',
         url='https://swc-math.github.io/aws/2009/09HankeNotes.pdf',
         source_type='author-written mathematical lecture notes', used_by=['MF4'],
         scope='Named classical quadratic local-to-global theorem and its number-field extension; no mass or effective assertion imported.',
         theorem_proof_reconstructed=False)
]

closed = [
    dict(id='MF-closed-local-ratio', claims=['MF5'], status='reconstructed',
         statement='Actual LocalDensityRatio with nu=q^(-m vd)alphaL and correct orbit orientation.',
         sources=ss(P+'LocalDensityRatioHolds.lean','local_density_ratio_holds','completed_endpoint')),
    dict(id='MF-closed-LIStat', claims=['MF2','MF3','MF5','MF8','MF9'], status='reconstructed',
         statement='LIRatio and LIPin are proved, including the positive pin, scaling, actual global reference lattice and all LIStat clauses.',
         sources=ss(P+'LiStatOf.lean','liStat_of liStat','completed_endpoint')),
    dict(id='MF-closed-HermRep', claims=['MF4'], status='proved_from_named_established_classical_theorem',
         statement='Actual HermRepUnram from explicit local representations plus Hasse–Minkowski; the latter theorem remains cited, not reconstructed.',
         sources=ss(FM+'BinaryHermitianRepresents.lean','binary_hermitian_represents','completed_endpoint')),
    dict(id='MF-closed-singular-mean', claims=['MF6','MF7','MF15','MF16'], status='reconstructed',
         statement='The exact singular-series mean is proved by a summably dominated divisor expansion, also at rank two.',
         sources=ss(P+'TendstoSingSSum.lean','tendsto_singS_sum','completed_endpoint')),
    dict(id='QW-next1', claims=['MF18','MF19'], status='proved_from_named_established_classical_theorem',
         statement='Literal StandardLattice.SiegelMassRatioCM is supplied; Hasse–Minkowski is the sole named external mass-specific theorem.',
         sources=ss(SL,'SiegelMassRatioCM','completed_endpoint')),
    dict(id='QW-next2', claims=['MF19'], status='proved_from_named_established_classical_theorem',
         statement='Actual massRatio_all_unramified_cmFields is supplied from the full model law.',
         sources=ss(GI+'MassRatioAllUnramifiedCmFields.lean','massRatio_all_unramified_cmFields','completed_endpoint')),
    dict(id='QW-next3', claims=['MF4','MF9','MF18','MF19'], status='proved_from_named_established_classical_theorem',
         statement='siegelMassRatio_of_LI is reconstructed through its genuine binary representation, LIStat, weighted representation and rank-induction suppliers.',
         sources=ss(P+'SiegelMassRatioOfLI.lean','massConst_all siegelMassRatio_of_LI','completed_endpoint'))
]
targets = [
    dict(id='MF-next1', priority=1, status='established_classical_theorem_cited_not_reconstructed',
         title='Internalize the exact quadratic local-to-global input if a proof without named classical theorems is desired',
         remaining_scope='Prove number-field Hasse–Minkowski, or reconstruct the source Hasse-norm-to-quadratic route sufficient for the five-variable form in MF4. All finite-place binary representations and the reduction are already proved. This is an established classical theorem, not a new conjectural bridge.',
         claims_affected=['MF4','MF12','MF13','MF14','MF17','MF18','MF19','MF20'],
         external_references=['MF-HM-Kim','MF-HM-Hanke'],
         sources=ss(AL+'ExistsCongrIffTraceFormsIsometricCm.lean','isotropic_of_locally_isotropic isotropic_of_indefinite','retained_classical_route') +
                 ss(FM+'BinaryHermitianRepresents.lean','binary_hermitian_represents','source_endpoint_now_reduced_to_classical_theorem')),
    dict(id='MF-next2', priority=2, status='distinct_geometric_supplier_not_implied_by_mass_ratio',
         title='Actual geometric volume normalization',
         remaining_scope='Reconstruct VolumeEqMass2/VolTie for the original actual volume and level data. MF19 is a genus mass ratio only; it supplies no indefinite or noncompact volume identity and no compatible Core arithmetic stage.',
         claims_affected=[],
         sources=ss(SL,'VolumeEqMass₂ VolTie','retained_distinct_geometric_interface'))
]

out = dict(schema_version='1.3', artifact_version='0.20', owner='/root/global_frame',
    repository=dict(url=URL,commit=PIN),
    range_convention='Inclusive original Git-blob line bounds; ranges preserve original newline bytes and omit only trailing blank lines before the next top-level boundary.',
    verification=dict(full_file_bytes_compared_to_pinned_git_blob=True,
        range_bytes_compared_to_pinned_git_blob=True, missing_sparse_files_read_with_git_show=True,
        declaration_boundaries_checked=True, old_claim_id_collisions_checked=True,
        component_dependency_order_checked=True, human_math_proof='main.tex and report.txt',
        lean_source_files_edited=False, local_lean_compilation=False, lean_kernel_replay=False,
        replacement_arguments_formalized=False, pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='A human proof of the literal source conclusion, sometimes replacing the source implementation by a shorter argument. Exact declared hypotheses and the explicit named classical theorem remain as marked.'),
    claims=claims, files=[files[k] for k in sorted(files)],
    artifact_sha256={'main.tex':digest(mb),'report.txt':digest(rb)},
    proof_paragraph_sha256=paragraphs,
    prior_components_reused=sorted({d for c in claims for d in c['depends_on'] if d not in ids}),
    external_references=external_references, independent_reviews=[],
    scope='Local density and orbit suppliers, weighted singular-series mean and induction prove the actual unramified Hermitian mass ratio from one explicitly named classical Hasse–Minkowski input. No geometric volume/Core or RH/GRH conclusion.',
    boundary_resolved=['Local Hermitian classification and dyadic lifting',
        'Actual LocalDensityRatio, LIRatio, LIPin and LIStat with exact normalization',
        'Binary Hermitian representation reduced to the named classical Hasse–Minkowski theorem',
        'Global weighted cut-fiber identity and lattice patching',
        'Singular-series mean including rank two and exact covolume constant',
        'MassConst induction, general orthonormal-model ratio and StandardLattice.SiegelMassRatioCM',
        'QW3/QW9 mass-law premise with unchanged same-data/threshold order'],
    retained_inputs=[COMMON,BOUND,HM,
        'Actual positive definite CM-unramified field/form/lattice hypotheses in each source interface',
        'Geometric VolumeEqMass2/VolTie, compatible arithmetic/Core objects and unrelated analytic suppliers when separately required'],
    dependency_precision=['MF1–3, MF5–11 and MF15–16 do not depend on Hasse–Minkowski.',
        'MF4 alone introduces the named classical theorem; global representation and mass descendants carry it explicitly.',
        'MF13/MF14/MF17 use an explicit rank-(m-1) induction hypothesis, discharged by MF18 without a claim-graph cycle.',
        'MF3 proves rational-local orbit agreement; completion is not silently substituted for the source rational condition.',
        'MF5 fixes its Haar normalization by the exact matrix-density Jacobian; MF9 pins the independent norm-fiber scalar.',
        'MF16 uses a C/(Na)^m summable ideal majorant, valid at m=2, before any infinite limit interchange.',
        'MF20 applies prior conditional QW claims; it does not depend on any v0.20 QR, WA or GA claim.',
        'Every predecessor file, source array and dependency is preserved.'])

for name, reviewer, nums in [
    ('mass_formula_MF1_10_review.txt','/root/comparison_span',range(1,11)),
    ('mass_formula_MF11_20_review.txt','/root',range(11,21))]:
    review = HERE.parent / 'reviews_v0_20' / name
    if review.exists():
        raw = review.read_bytes(); rt = raw.decode('utf-8')
        ph = {f'MF{n}':paragraphs[f'MF{n}'] for n in nums}
        for cid, h in ph.items():
            assert h in rt, ('reviewed paragraph changed',cid,h)
        out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',
            claim_ids=list(ph), review_record='../reviews_v0_20/'+name,
            review_record_sha256=digest(raw), paragraph_sha256=ph, lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc = []
for c in claims:
    loc += [f"{c['id']} | {c['title']} | {c['mathematical_status']}",c['statement'],
            'proof_paragraph_sha256: '+c['proof_paragraph_sha256']]
    for s in c['sources']:
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
                '  role: '+s['role'],'  file_sha256: '+s['full_file_sha256'],
                '  range_sha256: '+s['range_sha256'],'  '+s['url']]
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.20',commit=PIN,
    targets=targets,closed_source_targets=closed,
    remaining_boundary='One established classical theorem, Hasse–Minkowski over number fields, is cited and not reconstructed. Actual mass ratios are proved from it; geometric volume/Core and unrelated analytic/arithmetic suppliers remain distinct.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims), source_links=sum(len(c['sources']) for c in claims),
    source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
    source_files=len(files),next_targets=len(targets),closed_targets=len(closed),
    independent_reviews=len(out['independent_reviews']),verified_equal_to_pinned_git_blob=True,
    artifact_sha256=out['artifact_sha256'])))

