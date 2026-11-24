#!/usr/bin/env python3
"""Reproduce the TA source ledger from immutable Lean bytes, without a build.

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


P = D+'Proofs/FoundationProofs/'
H = D+'Proofs/HomogeneousIdeals/'
CB = D+'Proofs/CubicalLineBundles/'
SG = P+'GaloisTaylorSeriesCanonicalOddThetaAll.lean'
GC = P+'GaloisConjTaylorThetaTranslate.lean'
JC = P+'SecondDerivSigmaProductAtZero.lean'
JR = P+'JetRelOfWeierstrassSystem.lean'
CM = P+'CmThetaTaylorCoeffAlgebraicAndConjugate.lean'
GS = P+'GalStarComplexMultiplicationPoints.lean'
CC = P+'ConjugateCurveDatumLatticeIsCurveLattice.lean'
LI = P+'LatticeInvariantsPeriodPairDictionary.lean'
OT = P+'OddThetaFunctionExistenceUniqueness.lean'
ST = 'src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLatticesGL3.lean'
INPUT = 'Literal arithmetic host D and normalized curve datum Crv(D,cc,delta), including K=Q(sqrt(-d)), d=7 mod16. The one-dimensional assertions retain their exact coefficient-field membership hypotheses until those are proved or applied with M=C.'
CLASSICAL = 'Named classical inputs: ordinary Weierstrass elliptic uniformization for a nonsingular complex cubic, meromorphic elliptic-function rationality, characteristic-zero field extension through transcendence bases, elementary ideal theory and Chinese remainders. Analytic sigma normalization, ODE uniqueness and arithmetic descent are explicitly proved; no RH/GRH or column/vacuum existence theorem is used.'
SCOPE = 'Human proof reconstruction, not a Lean build, kernel replay, independent transitive Lean audit, or a full self-contained proof of RH/Dirichlet GRH.'
def cl(i,title,statement,deps,sources,relation,extra=()):
 return dict(id='TA'+str(i),title=title,status='derived_simplification',statement=statement,
  depends_on=deps,assumptions=[INPUT,CLASSICAL,SCOPE]+list(extra),
  mathematical_status='proved_under_literal_arithmetic_data_and_explicit_classical_inputs',
  source_relation=relation,proof_location=dict(file='main.tex',anchors=['TA'+str(i)]),
  expanded_notes=dict(file='report.txt',section='TA'+str(i)),sources=sources)
claims=[
 cl(14,'Purely analytic normalized odd theta laws, independent of coefficient algebraicity',
  'The normally convergent genus-two sigma product, Legendre relation, one-pole residue argument and elliptic pole cancellation prove all actual sgStar_laws, including uniqueness, zero divisor, addition and scaling. No odd-Taylor algebraicity hypothesis is used.', ['PA1'],
  ss(OT,'law_iff eq_deriv_mul canonicalSigma_spec sgStar_eq sgStar_laws'),
  'This separate analytic premise prevents an apparent cycle through the conditional arithmetic theorem PA15.'),
 cl(1,'Conjugate invariant data selects a unique genuine period lattice',
  'A subgroup with nonzero discriminant is a rank-two discrete lattice; equal invariants determine it uniquely. Classical elliptic uniformization gives existence, so the literal choice lamConj is this unique lattice.', ['PA1','TA2'],
  ss(LI,'discrete_of_eisG_ne_zero eisG_of_cyclic discr_of_cyclic exists_periodPair_of_discr_ne_zero exists_periodPair_of_invariants invariants_dictionary')+
  ss(GC,'exists_periodPair_lamConj')+ss(CM,'lamConj_eq_self lamConj_congr'),
  'Proves the arbitrary-additive-subgroup uniqueness clause previously retained in PA1, including totalized-sum/discreteness and the cyclic discriminant-zero cases. Uniformization is a named classical input, not an unproved theta conclusion.'),
 cl(2,'Formal Weierstrass and normalized-theta uniqueness with the quadratic constant',
  'For fixed s,a,b the cleared differential equation has at most one formal series with coefficients 0,1,0 in degrees 0,1,2. The equation forces s=-2*[z^3]F. All identities commute with arbitrary field embeddings.', [],
  ss(SG,'wSer OdeSer map_deriv map_rescale OdeSer.map ode_unique ode_reduce theta_unique OdeSer.const_eq'),
  'The first nonzero difference reduces to (n+1)E(0)=0; the subsequent logarithmic-derivative integration retains both needed initial constants.'),
 cl(3,'The normalized odd theta differential equation and CM polynomial descend to the coefficient field',
  'For alpha=iota(sqrt(-d)), N=d, s(alpha*z)^2/s(z)^(2N) is an even elliptic polynomial in wp of degree at most N-1. If the original Taylor coefficients and alpha are in M, pole-order cancellation puts its polynomial coefficients and the Gaussian ODE constant in M.', ['TA14','TA2'],
  ss(SG,'exists_wE odeSer_tay exp_scale exists_poly EndSer.descend sgStar_facts'),
  'Replaces the source linear-retraction descent by a triangular Laurent pole-order argument; does not assume that a complex elliptic polynomial already has coefficients in M.'),
 cl(4,'The CM identity eliminates the quadratic exponential and proves actual galSg',
  'Transport the formal ODE, identify the image series with the Taylor series of exp(u*z^2)*sgStar(lamConj), and transport the descended CM polynomial. The resulting period identity forces 2u(alpha^2-N)=0, hence u=0 and exact coefficient conjugacy.', ['TA1','TA2','TA3','TA14'],
  ss(SG,'tay_injective endSer_tay_iff wE_twist twist_eq_zero conj_sgStar galSg_all')+ss(ST,'FixK galSg'),
  'The original all-coefficients-in-M hypothesis of galSg is retained. No arbitrary field embedding is applied to analytic limits or exponentials.'),
 cl(5,'All seven actual torsion-point transport and CM-action clauses',
  'StarPt is coordinate conjugacy on the normalized Weierstrass cubic. Prove existence, unique target modulo periods, period invariance, addition, the exact O_K scalar action, exact integer annihilation, and n-torsion surjectivity with its original field-of-coordinates hypothesis.', ['TA1'],
  ss(GS,'mapPoint exists_pointHom exists_conjEquiv IsConj.mul exists_ringEquiv_eq_cj isRat_of_forall_isConj IsConj.add IsConj.nsmul_mem_iff isStar_props galStar_holds')+ss(ST,'StarPt Adp1 galStar'),
  'The CM scalar is identified by the algebraic differential dx/(2y). Only a countable generated subfield is extended to a complex automorphism; arbitrary uncountable-domain extension is not claimed.'),
 cl(6,'The literal conjugate curve ideal with arbitrary prescribed coprimality',
  'The conjugate lattice is O_K-stable, hence a scaled nonzero integral ideal. Two finite ideal-approximation choices replace that ideal by one whose norm is prime to 2dn, preserving the exact lattice and normalized discriminant. This proves galCurve for every positive n.', ['TA1','TA5','PA1'],
  ss(CC,'exists_span_eq_mul exists_equiv_comaximal coprime_absNorm exists_ideal discr_smul exists_crv galCurve_holds')+ss(ST,'galCurve'),
  'Retains equality of lattices, not just homothety, and the prescribed n after the field embedding. No theta coefficient assertion is used.'),
 cl(7,'Division quotients and root normalization over the exact coefficient field',
  'The sigma addition formula gives Psi0=0,Psi1=1,Psi2=-wp-prime and (j+1)^2 Psi_j Psi_(j+2)=wr(Psi_(j+1)). Formal Laurent division and the Weierstrass differential system prove all coefficient descent and conjugacy, including division by nonzero germs vanishing at zero. A power root is determined by its specified nonzero constant term.', ['TA14'],
  ss(JC,'IsSigmaLike.add_wr IsSigmaLike.double divQuot IsSigmaLike.divQuot_rec IsSigmaLike.divQuot_ne jetRel_divQuot')+
  ss(JR,'JetRel.of_mul JetRel.of_pow jetRel_of_weierstrass_system'),
  'Separates nonzero germ from nonzero value. The division recurrence is used only after the Psi1/Psi2 initial cases, never by cancelling Psi0.'),
 cl(8,'Exact torsion-translation power identities and the constant that fixes the root',
  'For m>0,u outside Lambda,m^2*u in Lambda, K=(U_u s)^(4m^2) obeys the two integer-rescaling identities and K(0)=-Psi_(m^2-1)(0)/Psi_(m^2+1)(0), with nonzero denominator.', ['TA14','TA7'],
  ss(GC,'thetaTranslate_canonicalOddTheta_of_half_mem thetaTranslate_natCast_mul thetaTranslate_zero_at_shifted_point translate_facts'),
  'Keeps the Heisenberg exponential normalization and the negative sign. The latter fixes the root of unity left by the power identity.'),
 cl(9,'Exact gal1 with its original integer, divided point, and coefficient assumptions',
  'Under the literal m*(x/2) in Lambda and StarPt at x/(2m), first descend K and the base odd-theta coefficients from the assumed coefficients of U_x s; then use galSg, division-quotient conjugacy, the normalized root and inverse rescaling to prove coefficient conjugacy for U_x s and U_xprime s_prime.', ['TA4','TA5','TA7','TA8'],
  ss(GC,'galois_translate_sgStar taylorCoeff_mem_iff_iteratedDeriv_mem')+ss(ST,'gal1 Adp1'),
  'Does not add base-sigma coefficient membership as a new hypothesis; it is derived from the literal translate membership hypothesis. No root-of-unity ambiguity remains.'),
 cl(10,'Primitive odd-theta rational translates have algebraic Taylor coefficients',
  'For each rational-lattice x and every n, [z^n]U_x(sgStar) is algebraic. Apply gal1 with M=C to every automorphism fixing Qbar, using PA14 torsion coordinates and m=2r when r*x is a period; fixed-field descent gives Qbar membership. The translates are entire.', ['TA1','TA9','PA14','TA14'],
  ss(CM,'coef_translate_mem taylorCoeff_evenTheta_cmCurve_algebraic')+ss(GC,'differentiable_U1'),
  'Supplies the arithmetic premise retained in PA15. TA10 has no dependency on PA15, so that conditional transfer is not used to prove its own premise.'),
 cl(11,'Unique unkilled half-period and representative-independent normalized even theta',
  'On the two-dimensional F2 half-period space, w and 1-w are complementary nonzero idempotents, each rank one. Thus exactly one class survives both. The normalized even-theta quotient is invariant under changing its half-period representative.', ['PA1','TA14'],
  ss(CM,'two_torsion_unique weylMatrix_mul_apply twoTorsionCMPoint_iff evenTheta_add_lattice_mem'),
  'Replaces the four parity cases by the explicit direct-sum decomposition; retains w(1-w)=2k and actual O_K stability.'),
 cl(12,'All three actual use1 clauses, including general coefficient-field embeddings',
  'Using the transported 16-torsion point t/8 and m=4 gives even-theta conjugacy for embeddings fixing K. Complex conjugation handles the other restriction to K. Restriction to M intersect Qbar and countable extension proves the original arbitrary-M assertion. Together with TA10 this proves the full cmTheta_taylorCoeff_algebraic_and_conjugate.', ['TA1','TA5','TA6','TA9','TA10','TA11','TA14','PA14'],
  ss(CM,'thetaTranslate_conjugateLattice sgStar_conj evenTheta_conjugateLattice taylorCoeff_complexConj_conjugate twoTorsionCMPoint_complexConj exists_ext embeddingConj_evenTheta_coeff_of_fixes_field embeddingConj_evenTheta_coeff_top cmTheta_taylorCoeff_algebraic_and_conjugate'),
  'The same target lamConj is identified by invariants; the target distinguished half-point is identified modulo its actual lattice. Uses no extension theorem for all of an arbitrary uncountable M.'),
 cl(13,'Joint one-dimensional theta endpoint and the precise remaining vacuum boundary',
  'TA10 supplies PA15, yielding algebraic entire even-theta rational translates and exact algebraic period-shift multipliers. Together with TA12, PA4, PA10 and TL18, the remaining vacuum problem is reduced to actual StdOK/four-copy and indicator/covariance suppliers, Pins.iX and separate Later existence.', ['TA10','TA12','PA15','PA4','PA10','TL18'],
  ss(P+'AlgebraicTaylorTorsionTranslateEvenTheta.lean','algebraicTaylor_torsionTranslate_evenTheta_alt')+
  ss(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','thetaVector_fourthPower_algebraicGerm','remaining_boundary_only'),
  'A supplier composition and boundary statement, not a proof of the remaining multidimensional vacuum theorem.'),
]
completed=[
 dict(path=CM,declaration='cmTheta_taylorCoeff_algebraic_and_conjugate',claims=['TA10','TA12'],reason='All three literal use1 clauses, primitive translate algebraicity and even-theta arbitrary-field conjugacy, are reconstructed.'),
 dict(path=GC,declaration='galois_translate_sgStar',claims=['TA9'],reason='The actual gal1 theorem is proved with its original coefficient premise, divided-point normalization and integer.'),
]
remaining=[]
t=source(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','thetaVector_fourthPower_algebraicGerm','remaining_human_reconstruction_target')
t.update(priority_group=1,remaining_human_scope='PA4 supplies algebraic complex substitution, PA10 supplies finite nonzero algebraic kappa, and TA10/TA13 supply the primitive odd/even theta coefficient premises. Reconstruct the literal StdOK/four-copy vacuum identity on the actual chosen data; do not infer it from one-dimensional algebraicity.',source_connections=['PA4','PA10','TA10','TA13','TL18'])
remaining.append(t)
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
proofs={n:digest((HERE/n).read_bytes()) for n in ['main.tex','report.txt'] if (HERE/n).is_file()}
ledger=dict(component='theta_arithmetic',artifact_version='0.16',date='2026-11-22',commit=PIN,repository=dict(url=URL,commit=PIN),
 scope='Full one-dimensional normalized odd/even theta arithmetic and exact Galois conjugacy, including actual galSg, galStar, galCurve, gal1 and use1. The multidimensional vacuum/covariance and Later branches remain.',
 retained_inputs=[INPUT,CLASSICAL,'Actual StdOK/four-copy vacuum, normalized indicator/covariance, Pins.iX, and the five Later existence suppliers are not constructed here.'],
 claims=claims,source_files=sorted(files.values(),key=lambda f:f['path']),proof_files=proofs,
 validation=dict(claim_count=len(claims),source_link_count=sum(len(c['sources'])for c in claims),source_file_count=len(files),all_files_and_ranges_equal_pinned_git_blobs=True,lean_build=False,kernel_replay=False,
 no_PA15_dependency_before_TA13=True,arbitrary_field_embeddings_not_assumed_continuous=True))
write(HERE/'provenance.json',ledger)
write(HERE/'source_manifest.json',dict(commit=PIN,files=ledger['source_files']))
write(HERE/'next_targets.json',dict(commit=PIN,targets=remaining,completed_targets=completed,notes=['PA15 remains a conditional theorem; its premise is now independently proved by TA10. The dependency graph uses TA14 for analytic laws, not PA15.']))
lines=['THETA ARITHMETIC SOURCE LOCATORS — PIN '+PIN,'']
for c in claims:
 lines.extend([c['id']+' '+c['title']])
 for t in c['sources']:lines.append(t['declaration']+' '+t['path']+':'+str(t['line_start'])+'-'+str(t['line_end'])+' '+t['range_sha256'])
 lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps(ledger['validation'],indent=2))


