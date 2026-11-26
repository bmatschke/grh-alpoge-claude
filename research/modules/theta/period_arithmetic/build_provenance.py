#!/usr/bin/env python3
"""Reproduce the PA source ledger from immutable Lean bytes, without a build.

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



P = D + 'Proofs/FoundationProofs/'
H = D + 'Proofs/HomogeneousIdeals/'
CB = D + 'Proofs/CubicalLineBundles/'
K = F + 'KernelLattices/'
PP = 'src/Formalism/PeriodIntegrals/OrbitalBoundsConclusion/'
S = D + 'Proofs/SiegelThetaTransformation/'
HOST = 'The literal arithmetic Host H is supplied: K=Q(sqrt(-d)) with d=7 mod16, E/K and its specified embeddings/conjugation, the nonzero inverse half-different A and its trace-self-duality. Existence of the host and later analytic/geometric inputs is not asserted.'
SCOPE = 'Human proof reconstruction only. No Lean build, independent kernel replay, transitive dependency audit or complete RH/GRH proof is asserted.'
def cl(i,title,statement,deps,sources,assumptions=(),relation='',conditional=False):
 return dict(id='PA'+str(i),title=title,status='derived_simplification',statement=statement,
   depends_on=deps,assumptions=[HOST,SCOPE]+list(assumptions),
   proof_location=dict(file='main.tex',anchors=['PA'+str(i)]),
   expanded_notes=dict(file='report.txt',section='PA'+str(i)),
   mathematical_status='proved_conditional_transfer_with_exact_remaining_odd_theta_premise' if conditional else 'proved_under_literal_supplied_arithmetic_data',
   source_relation=relation,sources=sources)
claims=[
 cl(1,'Actual ideal period lattices, area and nonzero discriminant',
    'Every nonzero quadratic ideal image is a genuine period lattice; the source area equals basis covolume and its lattice invariants have the exact scaling laws and nonzero discriminant.',[],
    ss(I+'ExistsCurveLattice.lean','exists_periodPair_mul_image mem_lamOf_top exists_periodPair_lamOf')+
    ss(P+'LatticeInvariantsPeriodPairDictionary.lean','eisG_eq_G g2_eq lattice_invariant_g3_eq area_eq invariants_dictionary')+
    ss(CB+'LatticeDeterminedByInvariants.lean','g₂_cube_sub_g₃_sq_ne_zero IsHomothetic.g₂_eq IsHomothetic.g₃_eq'),
    relation='Gives the rank-two module and area argument and the elliptic-function proof of discriminant nonvanishing. Only the used clauses of invariants_dictionary are asserted; its converse arbitrary-subgroup characterization is not claimed.'),
 cl(2,'Discriminant-normalized period pair with the exact unkilled half-period',
    'Choose delta^12=Delta(iota(O_K)), omega0=delta and t0=delta/2. The lattice is delta*iota(O_K), has discriminant one, and both (1±i sqrt(d))*t0/2 are outside it. This supplies the literal exists_periodPair_lattice_eq_lamOf.', ['PA1'],
    ss(I+'ExistsCurveLattice.lean','not_isIntegral_half not_isIntegral_of_re not_mem_lamOf exists_curve_lattice')+
    ss(I+'ExistsCurveLatticeStatement.lean','GlobalTheory.T.exists_periodPair_lattice_eq_lamOf')+
    ss(I+'IsIntegralHalf.lean','isIntegral_half')+
    ss(A+'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean','lamOf IsDiscriminantTwelfthRootOfIdealLattice IsTwoTorsionPointUnkilled'),
    relation='Constructs the chosen period and half-period explicitly; nonmembership follows because the trace would be 1/2, not by assuming theta nonvanishing.'),
 cl(3,'Positive rational trace form and an explicit four-copy K-isometry',
    'The host trace-Hermitian form has positive rational diagonal norms; Gram-Schmidt plus rational four squares constructs the actual IsoKG on four copies.',[],
    ss(I+'IsIntegralHalf.lean','conj_comm trace_conj trace_pos card_tau embT_K sum_embT')+
    ss(P+'ImaginaryQuadraticFieldStructure.lean','exists_orthogonal_family exists_similitude')+
    ss(I+'NonemptyIsoKG.lean','linearIndependent_of_orthogonal nonempty_isoKG')+
    ss(I+'ExistsIntMulMemInvHalfDifferent.lean','nonempty_isoK')+
    ss(K+'LateralTheory.lean','IsoKG'),
    assumptions=['Lagrange four-squares is a named classical integer theorem; its exact rational conversion and the quaternion matrix are proved here.'],
    relation='A direct orthogonal basis construction retaining the original K-linearity and first-variable-linear trace form.'),
 cl(4,'Explicit algebraic unitary complex extension of the rational trace isometry',
    'If b_w=gamma^-1(e_w), the embedding matrix B_(a,tau),w=tau((b_w)_a) satisfies B*B=1; gC=B* is the unique required extension and has algebraic entries.', ['PA3'],
    ss(I+'ExistsComplexLinearExtensionOfTraceIsometry.lean','exists_complexLinear_extension_of_traceIsometry')+
    ss(I+'ExistsComplexLinearExtensionOfTraceIsometryStatement.lean','GlobalTheory.T.exists_complexLinear_extension_of_traceIsometry\'')+
    ss(A+'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean','VacIn'),
    relation='Also proves the algebraic-coordinate property used later for substitution. No arbitrary complex extension or unproved scalar-extension surjectivity is substituted.'),
 cl(5,'Explicit conjugate prime separation including p=2',
    'For every literal SplitK rational prime obtain pfrak,alpha,beta with alpha in pfrak, beta outside and beta=conj(alpha). At 2 use (1+sqrt(-d))/2; at odd split primes use r+sqrt(-d).',[],
    ss(I+'ExistsPrimeOverSplitNotMemConj.lean','mem_xor exists_over exists_elt exists_prime_not_conj')+
    ss(A+'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean','SplitK'),
    relation='Uses only norm/trace and a prime of O_K/p, and preserves the dyadic case.'),
 cl(6,'A full lattice has a local basis with two-sided nonprime denominator bounds',
    'Every full finite O_K-lattice has a K-basis matrix g and t outside the selected prime with t g^-1 L inside O_K^r and t g O_K^r inside L.',[],
    ss(I+'ExistsMatrixBasisLatticeUpToDenominatorNotMem.lean','exists_basis_up_to_fintype exists_matrix_up_to_notMem'),
    relation='Uses the DVR basis and clears finitely many denominators, without asserting global freeness over O_K.'),
 cl(7,'Explicit split-prime unitary approximation by a Cayley sequence',
    'With q=alpha/conj(alpha), e_N=(1+q^N)^-1 approaches 1 and conj(e_N) approaches 0 at the selected prime. Skewing and the Cayley involution approximate any GL matrix by rational unitary matrices and give two-sided integral transition matrices after a denominator outside that prime.', ['PA5'],
    ss(S+'StrongApproximationUnitaryCongruence.lean','cay one_add_cay cay_cay cay_unitary skew skew_skew near near_tendsto exists_scalar exists_seq')+
    ss(I+'ExistsUnitaryMulIntegralAtSplitPrime.lean','exists_near exists_unitary_mul_integral'),
    relation='Proves the concrete approximation; never treats conjugation as continuous in a single split-prime topology.'),
 cl(8,'A rational denominator prime to p supplies both actual AtP clauses',
    'For the literal trace-self-dual A^4, local basis and unitary approximation followed by a=conj(alpha)t+alpha conj(t) give one positive rational integer s coprime to p for both inclusions. The resulting gamma_p satisfies actual AtP.', ['PA3','PA5','PA6','PA7'],
    ss(I+'SelfDualLatticeStandardAtRationalPrime.lean','selfDual_standard_at_rational_prime')+
    ss(I+'ExistsIntMulMemInvHalfDifferent.lean','form_mulVec exists_move exists_int_mul_mem_invHalfDifferent lat4 mem_fourCopiesInvHalfDifferent_iff fourCopiesInvHalfDifferent_fg fourCopiesInvHalfDifferent_selfDual exists_atP')+
    ss(A+'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean','AtP'),
    relation='Simplifies the source norm(a) integer to a itself only for the actual imaginary quadratic K. The two-direction trace duality and global denominators are explicit.'),
 cl(9,'Construct all literal KapIn, VacIn and AmbIn.Ok fields',
    'For each host construct actual AmbIn.Ok: the normalized period, half-point, rational/complex isometries, all local correction choices, and one common derivative-generator field from TL17. All 8 KapIn,8 VacIn,3 AmbIn and2 Ok fields are accounted for.', ['PA2','PA3','PA4','PA5','PA8','TL17'],
    ss(I+'ExistsIntMulMemInvHalfDifferent.lean','exists_gen_pow exists_dgen nonempty_kapIn exists_ambIn_ok')+
    ss(A+'IsDiscriminantTwelfthRootOfIdealLatticeIffDelta1.lean','IsDgen KapIn VacIn')+
    ss(A+'TrueColumnChoicesHeckeCharReferenceEqOne.lean','AmbIn AmbIn.Ok'),
    relation='Closes exists_ambIn_ok under Host; no theta Taylor, StdOK, canonical index or Later existence is a premise.'),
 cl(10,'Finite support and choice-independence of local determinant correction exponents',
    'On the exact subtype of rational primes satisfying SplitK(H,p), the y_p exponents are supported on the prime divisors of a common integer denominator for gamma0 and its inverse; they are independent of the AtP local isometry at a fixed prime. The actual correction kappa over that subtype is a finite nonzero algebraic product.', ['PA8','PA9'],
    ss(K+'LateralTheory.lean','IsoK.AtP IsoK.detRel ordK KapChoice.yP KapChoice.kappa KapChoice.YFinite YIndep')+
    ss(K+'KernelLocalFactors/BaseEx.lean','yIndep distinguished_ideal_ne_zero yFinite')+
    ss(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','kappa_mem'),
    relation='Explains the genuine finite support, rather than relying on totalized finprod. Does not assert independence of arbitrary root choices in the correction factors.'),
 cl(11,'Integral q-expansion and unit-leading modular-function criterion',
    'The source modularJ has expansion q^-1+744+... in integral coefficients. Pole cancellation by powers of j preserves integral coefficients; an invariant holomorphic function with unit-leading integral fractional-q expansion and a zero forces j at that zero integral.', ['PA1'],
    ss(H+'ExistsPolynomialModularJOfHasQExpansion.lean','modularJ modularJ_smul twelve_dvd_sigma qExpansion_E₄ qExpansion_E₆ exists_hasQExpansion_discriminant exists_hasQExpansion_modularJ exists_polynomial_modularJ_of_hasQExpansion')+
    ss(H+'ModularJExpansionAndPolynomialAndIsIntegral.lean','HasUnitLeadingExpansion HasUnitLeadingExpansion.mul HasUnitLeadingExpansion.isIntegral_modularJ hasUnitLeadingExpansion_sub')+
    ss(CB+'LatticeDeterminedByInvariants.lean','g₂_cube_div_eq_modularJ'),
    assumptions=['Standard absolutely convergent Eisenstein-series transformation/Fourier formulas and the complex maximum principle are used, with their source normalizations and coefficient argument explained.'],
    relation='Proves the needed modular-function argument, including unit rather than merely nonzero leading coefficient and the factor 1728.'),
 cl(12,'Nonsquare fixed determinant gives actual CM modular-j integrality',
    'For a quadratic tau, explicitly choose M=[[k-b,-c],[a,k]] of positive nonsquare determinant fixing tau. The finite distinct-translate product has unit leading Fourier coefficient and vanishes at tau. Therefore modularJ(tau) is integral; O_K-stability implies the needed quadratic relation.', ['PA11'],
    ss(H+'ModularJExpansionAndPolynomialAndIsIntegral.lean','isIntegral_modularJ_of_fixed isIntegral_modularJ_of_quadratic isIntegral_modularJ_of_mul_mem isIntegral_modularJ_of_ringOfIntegers'),
    relation='Reconstructs the finite modular-translate argument and its nonsquare/no-leading-cancellation step; no CM integrality black box is used.'),
 cl(13,'The literal base j-value and coefficient-field principalization',
    'Prove actual isIntegral_jLat for the nonzero ideal baseLat, then adjoin that value and finitely many conjugate ideal generators to construct the exact universal exists_fieldOK extension of any starting number field.', ['PA1','PA12','TL17'],
    ss(I+'CmInverseHalfDifferentMulRelativeDifferent.lean','cmInverseHalfDifferent_mul_relativeDifferent ellLat_eq mem_baseLat finrank_K exists_periodPair_baseLat isIntegral_jLat exists_fieldOK')+
    ss(A+'IsHalfPtIff.lean','jLat baseLat ellLat IsGen FieldOK'),
    relation='Closes the CM-j input of TL17 and preserves the fixed coefficient-field containment and all embedding compatibility; the extension is not silently inserted into a fixed field.'),
 cl(14,'Algebraic normalized invariants and actual torsion-point coordinates',
    'For every actual normalized curve-ideal lattice, prove DataIn Qbar and that wp(t),wpPrime(t) are algebraic at every nonzero rational-lattice torsion point. This reconstructs admJ_and_torsion_data_algebraic.', ['PA1','PA12'],
    ss(P+'IntegralJAndAlgebraicData.lean','exists_algHom_apply_eq isAlgebraic_of_torsion weierstrassP_mem exists_periodPair integral_j_and_algebraic_data')+
    ss(P+'IntegralJAndAlgebraicDataStatement.lean','GlobalTheory.T.admJ_and_torsion_data_algebraic')+
    ss(P+'LatticeInvariantsPeriodPairDictionary.lean','wpD_eq wpF_eq'),
    assumptions=['The standard Weierstrass uniformization/addition formula is used with the displayed curve y^2=x^3-g2*x/4-g3/4; its divisor/degree argument is explained.'],
    relation='Gives the finite-torsion algebraic descent proof. Algebraic torsion coordinates alone do not assert algebraicity of normalized sigma values or Taylor coefficients.'),
 cl(15,'Exact even-theta torsion transfer with the remaining odd-theta premise visible',
    'From the literal odd-theta rational-translate AlgEnt hypothesis derive algebraic entire even-theta translates and the exact nonzero algebraic lattice-shift multiplier. The Heisenberg phase exponent and normalization are explicit.', ['PA1'],
    ss(P+'DifferentiableSqTh.lean','IsLat AlgEnt IsLat.sg_eq_zero IsLat.sg_law')+
    ss(P+'OddThetaFunctionExistenceUniqueness.lean','canonicalSigma_spec sgStar_eq sgStar_laws')+
    ss(P+'AlgebraicTaylorTorsionTranslateEvenTheta.lean','phase thetaTranslate_comp_eq_phase_mul_add phase_mem thetaTranslate_evenTheta_eq_sigmaStar_translate sigmaStarTranslate_add_lattice_sign_phase algebraicTaylor_torsionTranslate_evenTheta_alt'),
    assumptions=['Every rational-lattice translate U_x(sgStar) is entire with algebraic Taylor coefficients. This arithmetic premise remains; the analytic sigma translation laws follow from the canonical product and Legendre relation.'],
    relation='Proves the entire stated conditional theorem, not the retained odd-sigma Taylor premise.',conditional=True),
]

completed=[
 dict(path=I+'ExistsIntMulMemInvHalfDifferent.lean',declaration='exists_ambIn_ok',claims=['PA9'],reason='All literal ambient-period, rational/complex isometry, local-correction and derivative-generator fields are now constructed from Host.'),
 dict(path=I+'CmInverseHalfDifferentMulRelativeDifferent.lean',declaration='isIntegral_jLat',claims=['PA11','PA12','PA13'],reason='The actual CM-j algebraic integrality theorem is reconstructed from nonsquare determinant modular translates.'),
 dict(path=P+'AlgebraicTaylorTorsionTranslateEvenTheta.lean',declaration='algebraicTaylor_torsionTranslate_evenTheta_alt',claims=['PA15'],reason='The exact theorem is proved under its original odd-theta translate premise; that premise remains separately targeted.'),
]
remaining=[]
for path,name,scope,connections in [
 (P+'GaloisConjTaylorThetaTranslate.lean','galois_translate_sgStar','Reconstruct the actual arithmetic Galois/Taylor identity for normalized odd-theta translates, including its period/Heisenberg normalization. PA14 supplies algebraic invariants and torsion coordinates; PA15 proves the even-theta transfer once the odd premise holds.',['PA14','PA15','TL18']),
 (I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','thetaVector_fourthPower_algebraicGerm','PA4 proves the exact complex substitution is algebraic and PA10 proves genuine finite nonzero algebraic kappa. Retain the actual StdOK/four-copy vacuum identity and the primitive odd-theta Taylor supplier; TL18 already proves the derivative algebra/root reduction.',['PA4','PA10','PA15','TL18']),
]:
 t=source(path,name,'remaining_human_reconstruction_target')
 t.update(priority_group=1,remaining_human_scope=scope,source_connections=connections)
 remaining.append(t)

def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
ledger=dict(component='period_arithmetic',artifact_version='0.16',date='2026-11-22',commit=PIN,
 repository=dict(url=URL,commit=PIN),scope='Construct actual AmbIn.Ok, CM-j integrality and FieldOK, local determinant corrections and normalized elliptic torsion data; prove exact conditional even-theta transfer. Primitive odd-theta Taylor/reciprocity and vacuum/covariance remain.',
 retained_inputs=[HOST,'Normalized odd-theta rational-translate algebraicity and arithmetic reciprocity; the actual four-copy vacuum identity, normalized indicator and covariance suppliers; all separate Later/global inputs.'],
 claims=claims,source_files=sorted(files.values(),key=lambda x:x['path']),
 proof_files={n:digest((HERE/n).read_bytes()) for n in ['main.tex','report.txt'] if (HERE/n).is_file()},
 validation=dict(claim_count=len(claims),source_link_count=sum(len(c['sources'])for c in claims),source_file_count=len(files),all_files_and_ranges_equal_pinned_git_blobs=True,lean_build=False,kernel_replay=False))
write(HERE/'provenance.json',ledger)
write(HERE/'source_manifest.json',dict(commit=PIN,files=ledger['source_files']))
write(HERE/'next_targets.json',dict(commit=PIN,targets=remaining,completed_targets=completed,notes=['The original cmTheta_taylorCoeff_algebraic_and_conjugate target remains; PA14 discharges its integral-J/invariants/torsion-coordinate supplier and PA15 its even-theta transfer, but the primitive Galois/Taylor identities remain.']))
lines=['PERIOD ARITHMETIC SOURCE LOCATORS — PIN '+PIN,'']
for c in claims:
 lines += [c['id']+' '+c['title']]
 for t in c['sources']:lines.append(t['declaration']+' '+t['path']+':'+str(t['line_start'])+'-'+str(t['line_end'])+' '+t['range_sha256'])
 lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps(ledger['validation'],indent=2))
