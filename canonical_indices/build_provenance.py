#!/usr/bin/env python3
"""Reproduce the CI source ledger from immutable Lean bytes, without a build.

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
I = D + 'Proofs/IwasawaDecomposition/'
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


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
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
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
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
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


S = D + 'Proofs/SatakeParameters/'
GI = D + 'Proofs/GlobalInterpolation/'
PI = 'src/Formalism/PeriodIntegrals/'
P2 = PI + 'UnitaryGroupMassFormula/projection2/'
TE = PI + 'UnitaryGroupMassFormula/TwistedEisensteinCoset/'
TN = PI + 'UnitaryGroupMassFormula/TwistedNormLattice/'
OB = PI + 'OrbitalBoundsConclusion/'
LOCAL = ('E is a number field; the actual prime P, residue map, coefficient field K of characteristic zero, '
         'and local coordinates are fixed. Except for CI3, every local calculation requiring digit representatives '
         'uses the literal DegOneUnram condition: q=Norm(P) is prime and q is not in P squared. '
         'The finite row/twist-prime family, ranks, character ties and constants have their explicitly stated hypotheses.')
BOUND = ('No Lean compilation, kernel replay, formalization of the shorter human proofs, source modification, '
         'PDF build, prime-window existence, arbitrary Pins.iX, Later existence or proof of RH/GRH is asserted.')


def cl(i, title, statement, deps, assumptions, sources, relation, conditional=False):
    return dict(id=i, title=title, status='derived_simplification', statement=statement,
        depends_on=deps, assumptions=[LOCAL, BOUND]+assumptions,
        proof_location=dict(file='main.tex', anchors=[i]),
        expanded_notes=dict(file='report.txt', section=i),
        mathematical_status=('proved_conditional_assembly_with_explicit_nonlocal_suppliers' if conditional
                            else 'proved_under_exact_declared_supplied_data_hypotheses'),
        source_relation=relation, sources=sources)


claims = [
cl('CI1','Finite quotient representatives and affine transport of stable sums',
   'Integer digit boxes represent q^-A O/q^B O exactly. Bounded locally periodic functions have stable normalized finite sums. Every invertible affine change of free coordinates preserves nonzero stable sum, using commensurable period lattices and nonzero finite indices.',
   [], ['Support and full-period bounds are explicitly supplied for the generic finite-sum assertion; no analytic integral or determinant-one condition is assumed.'],
   ss(GI+'RationalFractionsRepresentPrimeNormQuotient.lean','q_dvd_of_intAt q_pow_dvd_of_intAt valsQ_reps')+
   ss(GI+'SumCosetRepsNeZeroIffCommensurable.lean','finsum_quot_eq sum_reps_ne_zero_iff')+
   ss(GI+'BoxSumNeZeroInvariantAffineChange.lean','relIndex_ne_zero_of_cover exists_bound affine')+
   ss(C+'ChainTwAn.lean','twAn_sumA twAn_sumB twAn_deep_abs'),
   'Replaces the coordinate shear/diagonal sequence by a complete common-period-lattice counting proof, retaining exact finite normalization and eventual depth.'),
cl('CI2','Finite-sum affine eigenvalue rigidity without a Jacobian premise',
   'An affine eigenfunction with full-lattice periodicity, finite support on the quotient and nonzero finite sum has eigenvalue one. The full period group is affine-linear invariant and has finite index over the given lattice, so the affine map permutes the nonzero quotient support.',
   ['CI1'], ['The eigenvalue lies in a characteristic-zero field and the affine linear part is invertible. The assertion does not presume it preserves the originally chosen period lattice.'],
   ss(I+'AffineEigenvalueEqOneOfBoxSumNeZero.lean','periods eigen_eq_one_of_reps eigen_eq_one'),
   'Gives the genuine period-group proof behind kernel-character triviality, including why a zero eigenvalue is impossible and why the enlarged quotient sum stays nonzero.'),
cl('CI3','Finitely many admitted local level cosets',
   'For admitted h with h^-1 Lambda contained in Lambda and q^j h Lambda contained in Lambda, reduction of q^j h modulo q^(j+1) has finite image; equal colors differ by principal q congruence. Since that congruence is in the actual twist and symmetric levels, admitted right and double cosets are finite.',
   [], ['The local residue quotients are finite and q is a nonzero element of P. Degree-one unramified is unnecessary for this particular claim.'],
   ss(I+'AdmissibleRepresentativesFiniteLevelCosets.lean','exists_classes exists_finite_index_of_adm_cosets')+
   ss(C+'FiniteSumNonzeroLargeDepth.lean','JQ JGsym Jat SameDC'),
   'Proves actual finite coloring and both inverse congruence bounds, instead of assuming an abstract finite index set.'),
cl('CI4','Actual normal form and integral projected stabilizer',
   'A local lattice between O^Y and q^-j O^Y can be moved by the stated R group to O^X plus a triangular scaled tail, with the fixed first tail vector e0+z and z integral. Its X intersection is exactly O^X. Hence the actual projected conjugated level lies in GL_X(O).',
   ['CI1'], ['Local O-bases and principal fractional O-ideals are used; global O_E-freeness is not assumed. The zero-tail case is treated separately.'],
   ss(GI+'LatticeNormalFormUnipotent.lean','exists_equiv_map_eq exists_eq_span_zpow exists_unip exists_adapted latticeNormalFormUnip latticeNormalForm')+
   ss(TN+'IdealForm.lean','ideal_form herm')+
   ss(TN+'PrXLeOfNf.lean','Crit bdd_of_nf prX_le_of_nf')+
   ss(TN+'TwNormLatMain.lean','twNormLat_main')+
   ss(C+'ChainTwAux.lean','twNormRep'),
   'Expands the lattice-adapted triangular elimination and the constrained e0 column. Does not rely on a global free basis or rational strong approximation.'),
cl('CI5','Exact affine unfolding coordinates and additive phase',
   'The literal xx1 free-column space is preserved by left and right R actions. Their free coordinates transform invertibly and affinely, retained matrices transform by the X blocks, and the character argument shifts by the displayed additive n1Arg. The c=0 free final column is explicit.',
   [], ['The source and target tail lengths differ by one and the action preserves/fixes the literal flags and first tail vector.'],
   ss(C+'FiniteSumNonzeroLargeDepth.lean','R1cond R1 fixX N1 n1Arg Cbe prX IsFree xx1 chArg E1')+
   ss(TE+'FreeCoordinateAffineInvertible.lean','unfolding_affine_space_invariant restriction_to_affine_surjective free_coordinate_affine_invertible character_argument_constant_shift')+
   ss(S+'ExistsMoveRight.lean','chArg_right exists_move_right unfold_change'),
   'Derives transports column by column, including the actual phase sign and invertibility. The fixed f0 row is conditional on c>0.'),
cl('CI6','Twist-prime test-function covariance and exact bounds',
   'The actual JQ residue block condition preserves PhiQ support and gives its leading determinant multiplier. Splitting the full determinant yields the actual lamRow and muAt law. Admitted source/target matrices imply q^-(i+1) support and q^(i+1) periods for translated tests, with the stated phase denominator.',
   ['CI5'], ['The actual local multiplicative characters are units, and the muq/square-root scalar factors are nonzero.'],
   ss(C+'FiniteSumNonzeroLargeDepth.lean','locChar lamQB PhiQ muAt omPhi lamRow')+
   ss(TE+'JacobianTransformationLaw.lean','jq_int jq_DA CondQ phi_eq supp_comp val_comp det_comp jacobian_transformation_law')+
   ss(S+'PhiMapsAndOmegaLaw.lean','suppQ_of_JQ lamQB_eq phiQ_source phiQ_target phiAt_source phiAt_target')+
   ss(C+'ChainTwAn.lean','twAn_phiQ_int twAn_phiQ_congr twAn_bdd_inv twAn_bdd_q twAn_omPhi_supp twAn_omPhi_congr'),
   'Closes the actual twist covariance and support supplier; no future Laws or analytic Eisenstein convergence is used.'),
cl('CI7','Actual twisted double-coset nonvanishing',
   'For admitted target representatives in the same R-J double coset, their actual finite first unfoldings are eventually nonzero simultaneously. An invertible affine free-coordinate change, the exact nonzero character/scalar multiplier and bounded conductor prove the literal TwistedEisensteinNonvanishing theorem.',
   ['CI1','CI5','CI6'], ['Both representatives satisfy the displayed admission bounds; the additive character is multiplicative on its stated conductor lattice, trivial on O and unit-valued there. Depth dominates the explicit phase bound.'],
   ss(TE+'Development.lean','Tr CoVP JLawP GSuppP GPerP HGoodP ChArgBddP XXP TrAffP ResXSurjP ChArgP')+
   ss(TE+'UnfoldingMatrixFreeCoordinate.lean','unfolding_matrix_free_coordinate character_argument_bounded translated_function_support translated_function_invariance unfolding_integrand_good')+
   ss(TE+'TwistedEisensteinOfHypotheses.lean','psi_ne key_pt RS_mul core twisted_eisenstein_of_hypotheses')+
   ss(TE+'TwistedEisensteinOfRemaining.lean','ntAll twisted_eisenstein_of_remaining')+
   ss(OB+'TwistedEisensteinNonvanishing.lean','TwistedEisensteinNonvanishing')+
   ss(C+'UnfoldingNonvanishingDoubleCosetHolds.lean','firstUnfolding_eq_doubleCosetDatum doubleCosetDatum_hypotheses unfoldingNonvanishingDoubleCoset_holds'),
   'Reconstructs the nonzero finite-sum transformation itself, rather than deriving nonvanishing from root containment or citing the target theorem.'),
cl('CI8','Actual projected-kernel character triviality and descent',
   'On R intersect hJh^-1, chi_h(r)=psi(n1Arg r)^-1 lambda(h^-1 r h) is a unit-valued character. A kernel element acts affinely on a nonzero unfolding fiber, so CI2 forces chi_h(r)=1. This gives the actual descended twist level character and canonical TwChrOk, including last-tail and zero-step cases.',
   ['CI2','CI4','CI5','CI6'], ['An actual nonzero predecessor unfolding is given, together with its support/period bounds and the stated conductor depth. This is exactly the eligibility predicate of later recursive choices.'],
   ss(I+'IsAdmissibleIntegralBasisChangeOne.lean','CAt ChiMul ChiTriv GrpQ ChrQ exists_char')+
   ss(I+'NotMemVGsOfMemQE.lean','intAt_n1Arg_of_mem lamRow_mul lamRow_one chiMul chiTriv_last muAt_one chiTriv_mid exists_levQ')+
   ss(C+'ChainLawXiQF.lean','clXQ_chrOk_holds')+
   ss(C+'ChainTw.lean','TwChrOk twChiVal twChiVal_spec twChiVal_eq twLam')+
   ss(C+'ChainTwAux.lean','twChrOk_one twChrQ_of')+
   ss(C+'ChainTwFinal.lean','characterNonvanishing_holds'),
   'Closes the canonical projected-kernel theorem by actual affine eigenvalue rigidity. At step zero the complementary lamQB block is empty because n0=k; at zero tail the projection kernel is trivial.'),
cl('CI9','Finite recursive representative sets with exact quantifiers',
   'Finite local eligible double cosets admit representative sets F_j with exact predecessor, injectivity and coverage properties. Twist representatives may be normalized without losing nonzero predecessors. Their finite product gives the actual global beta_j, with singleton initial/final and empty out-of-range steps.',
   ['CI3','CI4','CI7'], ['Eligibility means that some representative from the previous local set gives FiniteSumNonzeroLargeDepth. Intermediate nonemptiness is not assumed.'],
   ss(I+'NotMemVGsOfMemQE.lean','exists_reps Rep rep_one Rep.int exists_step exists_sets')+
   ss(C+'FiniteSumNonzeroLargeDepth.lean','ChIdx SameDC FiniteSumNonzeroLargeDepth'),
   'Proves the finite recursive selection and the local-to-product predecessor quantifier. Empty products/steps are handled explicitly.'),
cl('CI10','Symmetric residue pattern, character and exact covariance',
   'The displayed three-interval allowed-entry relation forms a matrix algebra; its units with first-r diagonal one give exactly JGsym after scaled reduction. Adjacent-entry addition and diagonal block multiplication prove the actual character and PhiGS left/right covariance, including off-support zero cases.',
   ['CI5'], ['The literal symmetric ranks, additive residue character and multiplicative block characters are supplied. This argument is finite matrix algebra over the residue field.'],
   ss(P2+'AllowColLt.lean','S S_trans allow_lt_φ S_antisymm alg alg_mul alg_inv alg_diag injs_iff patClosed')+
   ss(C+'FiniteSumNonzeroLargeDepth.lean','bd5 flagS bvecS JGsym lamGvS lamGBS PhiGS')+
   ss(I+'RowTypeMulOnSymmetricLevelAtTypePrime.lean','superdiag block entB_mul entB_col entB_blk lamGBS_mul lamRow_mul')+
   ss(S+'PhiMapsAndOmegaLaw.lean','Pat.mul Pat.superdiag Pat.block SuppG.source SuppG.target levG_of_JGsym phiGS_eq phiM_source phiM_target phiAt_source phiAt_target'),
   'Proves the actual pattern closure and determinant/phase formulas, not only abstract character properties or an assumption named phi laws.'),
cl('CI11','Matrix completion proves residue one-coset support',
   'A nonzero residue unfolding summand has invertible leading minor. Completing its columns by standard last columns gives a level element; a tail-fixing unipotent adjustment and square-zero shear then place h in the identity R-J double coset.',
   ['CI5','CI10'], ['The exact one-coset range is j+1<m, so target tail c>=1. Nonzero sum is used only to select a nonzero summand.'],
   ss(P2+'KappaZeroAlt.lean','det_eq_det_castLE_of_cols_eq_one allow_mono kappaZero')+
   ss(P2+'MemFlagUnipotent.lean','symm_mem_Ufl_of_maps_Ufl R1cond_symm mem_flagUnipotent')+
   ss(P2+'GaStep.lean','fix_of_basis allow_of_mem_block_of_le_right gaStep')+
   ss(P2+'Assemble.lean','sum_step claim1_of')+
   ss(P2+'OneCosetSharpOfPatClosed.lean','oneCosetSharp_of oneCosetSharp_of_patClosed')+
   ss(OB+'OneCosetSharp.lean','support_oneCoset'),
   'Gives the genuine completion-and-elimination proof behind OneCosetSharp support; no unexplained Fourier cancellation claim is used.'),
cl('CI12','An explicit nonzero residue unfolding at the identity',
   'For the displayed x0 coordinate injection, every supported summand equals one after exact phase cancellation. A specified free-coordinate choice is the rectangular identity, so the unfolding is a positive integer and nonzero in characteristic zero.',
   ['CI5','CI10'], ['The exact source one-coset range j+1<m and coefficient characteristic zero are retained. Nontriviality of the additive character is unnecessary for this finite identity.'],
   ss(P2+'EntryEmbedMatrix.lean','xj0 τ0 facts ent_unit ent_τ0 sum_eq_chArg prod_blocks top_block term_eq claim2')+
   ss(C+'ChainOneB.lean','ResidueFieldUnfoldingNonzero ocbNe_one'),
   'Reconstructs a concrete witness and the 0/1 summand identity, instead of assuming a nonzero Eisenstein coefficient.'),
cl('CI13','Exact scaled reduction and type-prime one-coset theorem',
   'Every free coordinate has scale q^d with 1<=d<=c+1. Each residue fiber has q^(B+d-1) representatives; the normalized unfolding equals the residue unfolding times the explicit nonzero scalar q^sum(d-1). Entrywise lifts of residue R preserve the scaled lattice. Thus nonzero type-prime unfolding is exactly the identity double-coset condition, with two-sided source transport.',
   ['CI1','CI5','CI10','CI11','CI12'], ['j+1<m; target/source matrices preserve the literal scaled lattices; additive character depth is one and psi(a/q)=psi0(red(a)). Coefficient embedding is injective.'],
   ss(C+'FirstUnfoldingEqZeroOfNotIntegral.lean','ocbS_card_res ocbS_sum_pi_fiber ocbD scaledEntry_unipotentExtension ocbS_chArg ocbExp firstUnfolding_eq_zero_of_not_integral firstUnfolding_reduction_eq')+
   ss(C+'ReductionExistsInLatticeStabilizerHolds.lean','ocbA_det_unit ocbA_om_ne ocbA_red_exists reductionExistsInLatticeStabilizer_holds')+
   ss(C+'BlockTriangularMulVecMemPartialFlag.lean','residueR1_lifts_to_stabilizer liftFromResidueParabolicProduct_holds')+
   ss(C+'ResidueFieldUnfoldingClaimsHold.lean','residueFieldUnfolding_claims_hold')+
   ss(I+'UnfoldedDatumNeZeroIffDoubleCoset.lean','unfold_change₂ intAt_chArg_G unfoldedDatum_ne_zero_of_doubleCoset_source unfoldedDatum_ne_zero_iff_doubleCoset\'')+
   ss(C+'ChainTwOk.lean','twSurjG twNonVanG'),
   'Closes the actual auxiliary-prime identity-coset supplier used by reference-chart matching. The denominator direction is q*chArg integral, not chArg itself integral.'),
cl('CI14','Exact projected symmetric levels and character conjugation',
   'Deleting tail positions from the actual symmetric residue pattern gives exactly colLevSym. Integral entry lifts extended by tail identity give surjectivity. In the character, the tail phase cancels psi(n1Arg)^-1, leaving the exact X-superdiagonals and X-block determinants. Same-double-coset representatives have conjugate projected groups and transported characters.',
   ['CI5','CI10'], ['The literal scaled lattice, symmetric entry pattern and depth-one additive tie are supplied. The type-place conjugating X matrix is integral when the rational conjugating element preserves that lattice.'],
   ss(C+'ReducedMatrixExtensionEntry.lean','beta_framePos_formula not_allowed_of_beta_lt beta_lt_of_not_allowed reducedMatrix_extension_entry ocbGrpGLoc_holds')+
   ss(C+'FrameEntryAuxiliarySuperdiagonal.lean','frameEntry_auxiliary_superdiagonal frameEntry_last_auxiliary_zero columns_fact lamGBS_eq_addChar_mul_ocbXLam_of_mem_stabL ocbChrGLoc_holds')+
   ss(C+'ChainOneB.lean','ocbXAllow ocbXPat ocbXLam OcbGrpGLoc OcbChrGLoc OcbLevIs')+
   ss(C+'ColumnsProofs/SymLevEnt.lean','sl_allow_iff sl_sup_ins sl_blk_det character_level_zero_entries sl_lamJsym_ent closedLevels_by_entries_holds'),
   'Proves both group directions and exact characters, including the inverse additive phase. Supplies the independent group/character transport used by the new all-twist component.'),
cl('CI15','Full initial ChIdx.Ok from the literal local-constant inputs',
   'Under exactly exists_chIdx_of_cst hypotheses, construct finite beta and actual local levels/characters and prove all 34 ChIdx.Ok fields: nonzero predecessors, injection/coverage, initial/final singletons, group/character lifts, admission/integrality, support/period bounds and exact stabilized depths.',
   ['CI1','CI4','CI6','CI8','CI9','CI13','CI14'], ['Literal X.Ok, Pr.Ok, Chars.Ok, q-prime/unramified and disjointness inputs, sharp=true, LocCst.Ok, m<=M<=A,B, xiUnit/Weil/muqQ/muqG/mu0G/psi0 and depthG=1, depthQ>=2M, depthQ>=2(m-1)+1 are retained exactly.'],
   ss(C+'FiniteSumNonzeroLargeDepth.lean','LocCst.Ok LocCst.WeilTied ChIdx.Ok')+
   ss(I+'StepDatumBoundedAtTypePrime.lean','homBdd_of_good good_omPhi_two omPhi_bdd_type')+
   ss(I+'NotMemVGsOfMemQE.lean','intHom_pow_smul integrand_funBdd intHom_joinCol of_intHom_joinCol omPhi_bdd\' psiAt_add exists_chIdx_of_cst exists_chIdx')+
   ss(C+'ChainTwAn.lean','twAn_xiSupp twAn_psiSupp twAn_psiSuppX twAn_psiInv twAn_psiInvX twAn_xiInv twAn_deep twAnQ_of'),
   'The finite record assembly is accompanied by actual proofs of its suppliers. The exact terminal type-prime y support q^-1 and period O are distinguished from retained x support/periods.'),
cl('CI16','Actual local constants and reference local-value arithmetic',
   'Primitive q^D roots and local integer representatives construct the exact Weil additive character. The canonical type Gauss sum squares to q for q=1 mod4. Twist twSqrt requires only square=q. Tame approximation plus the Hecke product formula supplies local reference values in K. These give the nine actual LocCst.Ok fields and initial/canonical constants.',
   ['CI1','TL14','TL15'], ['Actual Hecke characters, integral infinity weights, coefficient-field containment, unit xi0, residue character ties and supplied twist q^D roots/square roots are explicit arithmetic inputs. The finite reference value field comes from TL14.'],
   ss(I+'TameHeckeCharLocalEqInvTypeCharacter.lean','exists_int_sub_div exists_root_exp exists_psi degOneUnram_of_mem_vGs degOneUnram_of_mem_QE degOneUnram_rowSG locK_mem_of_tied exists_root_vGs exists_locCst_of_values exists_locCst tameHeckeCharLocal_eq_inv_typeCharacter')+
   ss(GI+'ExpNegOneLtOne.lean','locK_eq_of_tame exists_approx locK_mem sq_div_norm')+
   ss(C+'ChainInst.lean','ciPsi ciSq ciSq_sq ciCst_ok')+
   ss(C+'ChainTw.lean','twZeta twPsiQ twSqrt twMuq twCst')+
   ss(C+'ChainTwCst.lean','twCst_ok localConstants_psi_depth_one twCst_weil twCst_base'),
   'Separates exact sign-free twist square-root choice from the actual type Gauss sum. Canonical A=B=m+1 while M=m; no missing local-value containment is hidden in a choice predicate.'),
cl('CI17','The specifically defined canonical twIdx satisfies Ok',
   'Under the literal twIdx_ok_closed arithmetic hypotheses, every actual canonical finite-class and epsilon representative choice is inhabited, admits the required normal form, and preserves its nonzero predecessor. The explicit type filter, projected characters and all support/depth fields prove the full actual twIdx.Ok record.',
   ['CI3','CI4','CI7','CI8','CI9','CI13','CI14','CI15','CI16'], ['X.Ok, Pr.Ok, Ch.Ok, character and Weil ties, type-prime reference-value containment/q=1 mod4, degree-one unramified twist primes disjoint from type primes, and exact TwCstQ are retained. Intermediate beta nonemptiness is not assumed.'],
   ss(C+'ChainTw.lean','TwCand twCSet twCFin twRep twNext twSt twIdx')+
   ss(C+'ChainTwOk.lean','TwDegOne TwFinQ TwNormDC TwChrQ TwZeroQ TwCstQ TwAnQ')+
   ss(C+'ChainTwAux.lean','twNormDC_of twChrQ_of twistedIndex_firstUnfolding_ok')+
   ss(C+'ChainTwMain.lean','twSt_chrOk twIdx_ok_of twIdx_ok')+
   ss(C+'ChainTwAll.lean','twIdx_ok\' twIdx_ok\'\' twIdx_ok_full')+
   ss(C+'ChainTwFinal.lean','twIdx_ok_left')+
   ss(C+'ChainTwAn.lean','twAnQ_twCst')+
   ss(C+'UnfoldingNonvanishingDoubleCosetHolds.lean','twIdx_ok_closed'),
   'Closes TwFinQ, TwNormDC, TwChrQ, TwZeroQ and TwAnQ with concrete proofs and identifies the actual canonical choices, not just an isomorphic existential record.'),
cl('CI18','Canonical replacement preserves actual Ok under Ok plus Deep',
   'From an actual old TC.Ok and Deep extract the exact twist square roots, inverse local values and primitive q^(2m) roots. Apply the independent local theorem CI17 to each actual tuple. Canonical replacement changes only constants/indices, preserving every other field literally, so canon.Ok and IsTw hold; TL13 supplies Laws afterward.',
   ['CI17','TL13','TL20'], ['Literal old I.Ok and I.Deep are antecedents; no unconditional TC.Ok or removal of the Deep premise is asserted. Nonvanishing/kernel triviality is supplied by CI7/CI8/CI13, not by root extraction.'],
   ss(A+'IsTwIffCanonEq.lean','IsTw canon canon_isTw Deep qOf_mod_four val_of_ok Q_notMem_of_ok degOne_of_ok sqrt_of_ok root_of_ok twIdx_ok_of_ok canon_ok'),
   'Prospectively closes TL20 canonical local nonvanishing boundary without modifying inherited claims or using Laws to prove Ok.'),
cl('CI19','Exact contribution to the canonical EvLg constructor',
   'The initial exists_colIn construction obtains local constants and every actual local-index field from CI15/CI16; with its other literal raw constructor fields it gives initial Ok and then canonical Ok/IsTw/Laws by CI18. This closes the local TL20/TL21 frontier while preserving the nonlocal vacuum/indicator/covariance, field-containment, Pins.iX and Later boundaries.',
   ['CI15','CI16','CI18','TL14','TL15','TL16','TL19','TL21'], ['The literal host/field/selection and actual ambient data of exists_colIn are supplied, with original coefficient-field containment quantifiers. PA9/PA13, AH17/AH18 and TA10/TA12 are separate companion constructions, not hidden inputs of CI1–CI18. Actual vacuum/indicator identities, covariance and smoothness used in JetsIn must still be joined.'],
   ss(I+'ExistsColumnInputAssembled.lean','exists_colIn isTwist_of_mem_set of_over lg_colIn ev_of_forall')+
   ss(I+'EvLgCanonical.lean','exists_quot evLg_canonical')+
   ss(A+'LatAtLattice.lean','TC Pins Later','literal_remaining_record_boundary'),
   'A complete local supplier and a precise conditional constructor join. It does not assert the full nonlocal analytic constructor or any Later stages have been independently proved here.',True)
]


targets = []
def target(path, name, group, scope, connections):
    t = source(path, name, 'remaining_human_reconstruction_target')
    t.update(priority_group=group, remaining_human_scope=scope, source_connections=connections,
             human_status='continuation_target_only; exact nonlocal supplier not claimed proved in CI')
    targets.append(t)

target(I+'EvLgCanonical.lean','evLg_canonical',3,
       'Join the same actual ambient datum and the remaining normalized vacuum/indicator/covariance laws to the now-proved initial/canonical local indices. Preserve the original fixed/full field containments, Pins.iX antecedent and nonempty raw data. Local nonvanishing is no longer a remaining premise.',
       ['CI15','CI16','CI18','CI19','PA9','PA13','TA10','TA12','TL19','TL21'])
target(A+'LatAtLattice.lean','Later',4,
       'Construct the literal independent later-stage record at its actual levels and data. Local index construction, Laws and canonical Ok preservation supply no existence proof for these stages.',
       ['CI18','CI19','TL13'])

closed = []
for path, name, by in [
    (I+'NotMemVGsOfMemQE.lean','exists_step',['CI3','CI4','CI7','CI9']),
    (I+'NotMemVGsOfMemQE.lean','exists_chIdx_of_cst',['CI1','CI8','CI9','CI10','CI11','CI12','CI13','CI14','CI15']),
    (I+'TameHeckeCharLocalEqInvTypeCharacter.lean','exists_locCst',['CI1','CI16']),
    (TE+'TwistedEisensteinOfRemaining.lean','twisted_eisenstein_of_remaining',['CI1','CI5','CI6','CI7']),
    (C+'ChainTwFinal.lean','characterNonvanishing_holds',['CI2','CI5','CI6','CI8']),
    (C+'UnfoldingNonvanishingDoubleCosetHolds.lean','twIdx_ok_closed',['CI1','CI2','CI3','CI4','CI5','CI6','CI7','CI8','CI9','CI10','CI11','CI12','CI13','CI14','CI15','CI16','CI17']),
    (A+'IsTwIffCanonEq.lean','canon_ok',['CI17','CI18'])]:
    s=source(path,name,'closed_source_target_under_literal_hypotheses');s['closed_by']=by;closed.append(s)

field_source=source(C+'FiniteSumNonzeroLargeDepth.lean','ChIdx.Ok','literal_record_field_audit')
lines, _, _ = read_source(field_source['path'])
record=b''.join(lines[field_source['line_start']-1:field_source['line_end']]).decode()
field_names=re.findall(r'^  ([A-Za-z_][A-Za-z0-9_\']*)\s*:',record,re.M)
assert len(field_names)==34, field_names

out=dict(schema_version='1.3',artifact_version='0.16',date='2026-11-22',owner='/root/global_frame',
    repository=dict(url=URL,commit=PIN),
    range_convention='One-indexed inclusive; exact original declaration bytes, without newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
        replacement_arguments_formalized=False,pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof of the precisely stated supplied-data assertion or conditional assembly, with retained source inputs explicitly labeled.'),
    claims=claims,files=[files[p] for p in sorted(files)],
    record_field_audit=dict(path=field_source['path'],declaration=field_source['declaration'],fields=field_names,
                           field_count=len(field_names),proved_by=['CI15','CI17'],notes='Exact field-by-field mapping is in report.txt; arithmetic inputs retain their literal hypotheses.'),
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    prior_components_reused=['TL13','TL14','TL15','TL16','TL19','TL20','TL21'],
    same_iteration_companions=['PA','TA','AH','TX'], independent_reviews=[],
    scope='CI1–CI18 reconstruct actual local index selection, normal forms, test-function covariance, finite first-unfolding nonvanishing, projected kernel characters, type-prime one-coset identities and canonical Ok preservation under literal old Ok plus Deep. CI19 makes the exact conditional nonlocal constructor join. No RH/GRH, unconditional raw data existence, Pins.iX or Later assertion is made.',
    boundary_resolved=['All four v15 local-index targets','Actual TwistedEisensteinOfRemaining finite-sum supplier','Actual characterNonvanishing_holds projected-kernel theorem','Actual type-prime OneCosetSharp support and identity nonzero in j+1<m range','Initial exists_chIdx_of_cst/exists_chIdx under literal arithmetic inputs','Actual canonical twIdx_ok_closed under its literal arithmetic inputs','canon_ok under old Ok and Deep'],
    retained_inputs=[LOCAL,BOUND,'Actual raw arithmetic/host/selection and Hecke-character data; coefficient-field root/value containments and their quantifier order','Actual normalized vacuum/four-copy/indicator identities, smoothness and covariance needed for JetsIn','Original Pins.iX and nonempty PreX antecedents; five Later stages','Old I.Ok and I.Deep for the canonical-preservation implication CI18'],
    dependency_precision=['CI1–CI17 use neither TC.Laws nor final FC/TG/TX comparisons.','CI18 derives canonical Laws only after canonical Ok, using old TL13.','CI19 mentions PA/AH/TA companion progress without making those nonlocal constructions premises of local claims.','TX may depend on CI7/CI13/CI14; CI has no dependency on TX.','All old claim fields and source arrays remain immutable; new CI claims discharge old retained suppliers prospectively.'])

for name,who,nums in [
    ('tx_reviews_ci10_14.txt','/root/comparison_span',list(range(10,15))),
    ('root_reviews_ci_1_9_15_19.txt','/root',list(range(1,10))+list(range(15,20)))]:
    review=HERE.parent/'reviews_v0_16'/name
    if review.exists():
        rb=review.read_bytes();rt=rb.decode();mb=(HERE/'main.tex').read_bytes();ph={}
        for n in nums:
            a=mb.index(f'\\paragraph{{CI{n}:'.encode())
            z=mb.index(f'\\paragraph{{CI{n+1}:'.encode(),a+1) if n<19 else len(mb)
            sh=digest(mb[a:z]);assert sh in rt,('independent review paragraph changed',n,sh);ph[f'CI{n}']=sh
        out['independent_reviews'].append(dict(reviewer=who,result='PASS',claim_ids=list(ph),
            review_record='../reviews_v0_16/'+name,review_record_sha256=digest(rb),paragraph_sha256=ph,lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc.extend([f"{c['id']} | {c['title']} | {c['mathematical_status']}",c['statement']])
    for s in c['sources']:
        loc.extend([f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            '  role: '+s['role'],'  file_sha256: '+s['full_file_sha256'],
            '  range_sha256: '+s['range_sha256'],'  '+s['url']])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.16',commit=PIN,targets=targets,closed_source_targets=closed,
    partially_reconstructed_targets=[dict(path=I+'EvLgCanonical.lean',declaration='GlobalTheory.Mem.Col2.TwIdxEx.evLg_canonical',proved_reductions=['CI15','CI16','CI18','CI19'],remaining='Only the explicit nonlocal analytic/raw-constructor joins remain here; local index, nonvanishing and canonical projected-kernel suppliers are closed under their literal hypotheses.')],
    remaining_boundary='No local first-unfolding or canonical kernel-character theorem is retained as an unexplained premise. Raw constructor inputs, exact field containments, normalized vacuum/indicator/covariance and Pins.iX/Later remain separately scoped.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),
    record_fields=len(field_names),next_targets=len(targets),closed_targets=len(closed),verified_equal_to_pinned_git_blob=True,
    artifact_sha256=out['artifact_sha256'])))


