"""Regenerate source-reading provenance for the v0.5 local Gram reconstruction.

This checks the pinned source revision, exact declaration ranges and hashes.
It does not invoke Lean or replay any proof term.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path('/workspace/scratch/b992d67d27b8/alpoge-rh')
OUT = Path('/workspace/scratch/b992d67d27b8/v0_5/local_gram')
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == COMMIT
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
files = {}

def namespace_at(lines, first):
    stack = []
    for line in lines[:first-1]:
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s|$)', line)
        end = re.match(r'^end(?:\s|$)', line)
        if ns:
            stack.append(('namespace', ns.group(1)))
        elif sec:
            stack.append(('section', ''))
        elif end:
            assert stack, ('unmatched end', first, line)
            stack.pop()
    ns = '.'.join(name for kind, name in stack if kind == 'namespace')
    return ns + '.' if ns else ''

def reference(path, local_declaration, role='proof'):
    data = (ROOT/path).read_bytes()
    lines = data.decode().splitlines(keepends=True)
    pattern = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev)\s+'
                         + re.escape(local_declaration) + r'(?=[\s{(:])')
    hits = [i for i, line in enumerate(lines) if pattern.match(line)]
    assert len(hits) == 1, (path, local_declaration, hits)
    first = hits[0]+1
    next_top = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance)\b')
    last = next((i for i in range(first, len(lines)) if next_top.match(lines[i])), len(lines))
    while last > first and not lines[last-1].strip():
        last -= 1
    digest = hashlib.sha256(data).hexdigest()
    files[path] = dict(path=path, sha256=digest, line_count=len(lines),
                       url=f'{REPO}/blob/{COMMIT}/{path}')
    return dict(path=path, declaration=namespace_at(lines, first)+local_declaration,
                line_start=first, line_end=last, role=role, sha256=digest,
                excerpt_sha256=hashlib.sha256(''.join(lines[first-1:last]).encode()).hexdigest(),
                url=f'{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}')

def ms(file, name, role='proof'):
    return reference(GB+'MonomialOrderSegments/'+file+'.lean', name, role)
def rw(file, name, role='proof'):
    return reference(GB+'RootWeights/'+file+'.lean', name, role)
def gb(file, name, role='proof'):
    return reference(GB+file+'.lean', name, role)

claims = []
def claim(cid, title, statement, status, sources, assumptions=(), dependencies=(), sections=(), note=''):
    assert status in {'faithful_translation', 'derived_simplification', 'remaining_input'}
    claims.append(dict(id=cid, title=title, statement=statement, status=status, sources=sources,
                       assumptions=list(assumptions), depends_on=list(dependencies),
                       proof_location=dict(file='local_gram_section.tex', anchors=[cid]),
                       expanded_notes=dict(file='report.txt', sections=list(sections)), source_relation=note))

claim('PG1', 'The actual signed-chain datum and its integer-depth model',
      'Translate the original signed letters, cyclic segments, label/carry/tangent substitution, XX conditions and YY constraints into the explicit model. Good monomials have low label residues, correct substituted multidegrees, tangent degree<=dLL and no tangent of index0. With h=ceil(c)<=2c, CH>=26 gives the model slope constant13, while the depth bound remains h>4(Dm+Dl+3kp).',
      'faithful_translation', [
          gb('ObjPol', 'UniformizedDVR', 'ring_definition'), gb('ObjPol', 'AdmissibleDVR', 'ring_definition'),
          gb('Lemma5aAt', 'SignedChainData', 'data_definition'), gb('Lemma5aAt', 'ph', 'substitution_definition'),
          gb('Lemma5aAt', 'Fdig', 'digit_definition'), gb('Lemma5aAt', 'XX', 'input_definition'),
          gb('Lemma5aAt', 'YY', 'output_definition'), gb('Lemma5aAt', 'ProjectionDerivativeEstimate', 'target_statement'),
          ms('CollapseExponent', 'GoodE', 'model_definition'), ms('LiftBoundOfHypotheses', 'LiftBoundUniform', 'model_target'),
          ms('BrData', 'natCeil_le_two_mul_of_one_le'), ms('BrData', 'hypH_toData'), ms('BrData', 'hc_toData'),
          ms('BrData', 'plane_gram_of_theorem_at', 'exact_transport')],
      assumptions=['The exact SignedChainData hypotheses, including finite nonempty cyclic index and positive coordinate rank.',
                   'p>=5, mixed-characteristic source DVR, v(p)=1, c>=1, and all stated XX/slope/depth conditions.',
                   'No SqP assumption is added to the standalone theorem.'], sections=[1],
      note='The variable renamings preserve both coefficient Fock pairing and weighted valuation. The only numerical enlargement is ceil(c)<=2c.')

claim('PG2', 'The divided-derivative digit expansion is elementary',
      'For P=p^g and a_l=[z^M](1+z)^rho((1+z)^P-1)^l, the exact Newton expansion of binom(rho+P beta,M) has p^(max(0,l-floor(M/P))) dividing a_l. Tensoring and discarding terms of total coefficient valuation>=h yields a finite integral divided-derivative congruence with total carry order<=|M|/P+h. Nonnegative residual exponents follow from M<=rho+P l.',
      'faithful_translation', [
          rw('BinomialExpansionCoeffZeroOfDeg', 'coeff_binomial_power_divisibility'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'binomialExpansionCoeff', 'explicit_coefficient_definition'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'binomial_expansion_coeff_padic_dvd'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'binomial_expansion_coeff_zero_of_gt'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'binomial_expansion_coeff_zero_of_deg'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'choose_shift_binomial_expansion'),
          rw('BinomialExpansionCoeffZeroOfDeg', 'derivative_digit_expansion'),
          gb('ProjectionOfIsotypicDecomposition', 'derTriple', 'operator_conversion_definition'),
          gb('ProjectionOfIsotypicDecomposition', 'der_term'),
          gb('ProjectionOfIsotypicDecomposition', 'derivation_valuation_at_prime'),
          ms('BrRenExpandMonomial', 'brDER', 'notation_bridge'),
          ms('LiftBoundOfHypotheses', 'DER', 'exact_input_statement')],
      assumptions=['p is prime; rho is a coordinatewise residue modulo P; h is a positive integer.',
                   'Congruences of integer coefficients are transported to the source valuation ring.'],
      sections=[3], note='Complete generating-function proof, including the degree/vanishing cutoffs. It even works for primes below5, but no surrounding parameter threshold is changed.')

claim('PG3', 'Weighted Fock lattices, algebraic orders and actual cutoff projectors',
      'The lattice b(F)>=0 is full, torus-graded and divided-power stable for arbitrary ramification, by the half-sum of two binomial valuations. Apply the companion IW4 to the S-letter weight interval [-D_S,D_S], using the difference of the same coordinate in two weights <=2D_S. The cutoff ord_S>=theta is the sum of isotypic components with last highest weight>=ceil(theta). Its Fock projector is selfadjoint; nested/disjoint cutoff projectors commute. Rescaling by p^ceil(-b(F)) gives weighted loss<=r^2(log_p(2T+r)+1). The V2 order calculus and binomial-operator degree costs are proved directly.',
      'faithful_translation', [
          gb('ObjPol', 'vBB', 'weighted_valuation_definition'),
          rw('IntegralGeneratorsPreserveLattice', 'divided_powers_preserve_polarization', 'formal_counterpart'),
          rw('IntegralGeneratorsPreserveLattice', 'divided_powers_preserve_gl_operator', 'formal_counterpart'),
          rw('IntegralPolynomialsEnvelopingStable', 'integral_polynomials_enveloping_stable', 'source_provider'),
          rw('MultidegreePartFinitelyGenerated', 'fockLattice', 'lattice_definition'),
          rw('ExponentFactorialAddSingleOne', 'fock_form_contravariant'),
          rw('PolynomialIsotypicLatticeOfParts', 'polynomial_isotypic_lattice_of_parts', 'actual_projector_route'),
          ms('SecondValuationOfAdmitted', 'brPROJ', 'weighted_projector_bridge'),
          ms('LiftBoundOfHypotheses', 'PROJ', 'exact_projector_statement'),
          ms('LiftBoundOfHypotheses', 'V2', 'exact_order_statement'),
          rw('DerivativeValuationBounds', 'derivative_valuation_bound', 'formal_order_counterpart'),
          ms('ProjKeepsLetter', 'prodProj'),
          ms('SlopeOfBinomCombGen', 'choose_affine'), ms('SlopeOfBinomCombGen', 'cost_choose_affine'),
          ms('CgeZeroIffIntegral', 'fact_upper'), ms('CgeZeroIffIntegral', 'fact_lower'),
          ms('CgeZeroIffIntegral', 'fact_add_lower'), ms('CgeZeroIffIntegral', 'bge_of_cge'),
          ms('CgeZeroIffIntegral', 'cge_of_bge')],
      assumptions=['Universal isotypic-projector lattice bound IW4, with its exact coordinate-weight difference hypothesis.',
                   'Standard characteristic-zero complete reducibility, highest-weight classification and rationality of the signed polynomial representation.',
                   'The source DVR and degree hypotheses of PG1.'],
      dependencies=['PG1'], sections=[2, 4],
      note='This fragment proves the specialization and commutation/adjoint statements; IW4 supplies the universal denominator theorem in a companion proof. Weighted valuations need not be attained in the value group, so the rescaling loss1 is explicitly retained.')

claim('PG4', 'A detected integral polynomial with the original link constraints',
      'Choose a coefficient attaining b(F)=0, project its monomial onto all original link cutoffs, approximate gamma^(-1) by a degree<=6h integral binomial polynomial and multiply by p^ceil(n0+Dl-v_p(alpha!)/2). This gives integral H with link loss6h and v(<F,Gamma H>)<=n0+Dl+1. The approximation error has strictly larger valuation and cannot cancel the detected coefficient.',
      'faithful_translation', [
          ms('CardLinkIdxMulLe', 'Tset_pair'), ms('CardLinkIdxMulLe', 'card_linkIdx_le'),
          ms('CardLinkIdxMulLe', 'card_linkIdx_mul_le'), ms('CardLinkIdxMulLe', 'stepB_of'),
          ms('CollapseExponent', 'StepB', 'exact_statement')],
      assumptions=['b(F)=0 and F satisfies all original link orders.',
                   'The data gamma^(-1) approximation of order h and degree<=6h.',
                   'h>4(Dm+Dl+3kp), ensuring the error is strictly smaller in p-adic norm.'],
      dependencies=['PG1', 'PG3'], sections=[5],
      note='This is a constructed test with a specific coefficient witness, not an assumed nonzero pairing.')

claim('PG5', 'Marked path columns give the actual model lift',
      'Expand in the integral prefix-adapted signed path-column basis. Mark columns containing a base letter; only in those columns move frame indices m>0 to tangent variables. Tangent degree is bounded by the number of marked columns<=dLL. Unmarked columns have nonpositive colVal and no variables in the renamed link, so the original prefix order lower bounds survive. Injective renaming preserves each column Gauss valuation and its multiplicativity proves integrality of the full renamed product. Digit-split the remaining labels to obtain integral good Z with phi Z=H and no further link loss.',
      'faithful_translation', [
          ms('LiftBoundOfHypotheses', 'SPAN', 'shared_basis_input'),
          ms('LiftBoundOfHypotheses', 'colVal', 'column_order_definition'),
          ms('SecondEmbeddingTangentIndex', 'Marked', 'marking_definition'),
          ms('SecondEmbeddingTangentIndex', 'fk', 'renaming_definition'),
          ms('SecondEmbeddingTangentIndex', 'cnt_tp_le'),
          ms('SecondEmbeddingTangentIndex', 'PsiP', 'lift_definition'),
          ms('SecondEmbeddingTangentIndex', 'PsiP_support'),
          ms('SubstitutionXFirstEmbedding', 'PsiP_integral'), ms('SubstitutionXFirstEmbedding', 'PsiP_ph'),
          ms('SubstitutionXFirstEmbedding', 'card_unmarked'), ms('SubstitutionXFirstEmbedding', 'PsiP_val'),
          ms('ExistsMonomialOrder', 'vG_mul'),
          ms('RenamePullLCoefOut', 'segStep_of'),
          ms('ExistsOfMemSupportLin', 'splitE', 'digit_split_definition'),
          ms('ExistsOfMemSupportLin', 'stepC_of'), ms('CollapseExponent', 'StepC', 'exact_statement')],
      assumptions=['The exact integral signed path-column basis, prefix support adaptation, multilinearity and column-order clauses stated in report section6; these are shared with IP.',
                   'The input H is integral, has the prescribed multidegrees and satisfies the link cutoffs.'],
      dependencies=['PG3', 'PG4'], sections=[6],
      note='The downstream lifting map and all its constraints are proved here. The proof status of the integral prefix-adapted basis remains the proof status of the companion IP theorem; it is not silently discharged by calling this map a lift.')

claim('PG6', 'The joint chain projector has controlled coefficients and preserves every label/tangent block',
      'Form the product of the weakened chain cutoff projectors. Its sets are nested within segments, disjoint across segments, and contained in or disjoint from every relevant link set. It therefore preserves links. Euler commutation fixes every outside label/tangent exponent. On good x^zeta it has b>=v_p(zeta!)/2-Dm; within the resulting block factorial valuations differ by at most kp, so all coefficients are >=-Dm-kp/2. Hence p^ceil(Dm+kp/2) clears its coefficients on integral good inputs.',
      'faithful_translation', [
          ms('ProjKeepsLetter', 'proj_keeps_letter'), ms('ProjKeepsLetter', 'prodProj_entries'),
          ms('SubstitutedExponentApplyBlock', 'stepP_of'),
          ms('GlobalTheory', 'blk_fact'), ms('MlabNotMemYset', 'cge_Pj_monomial'),
          ms('MlabNotMemYset', 'good_Pj'), ms('CollapseExponent', 'StepP', 'exact_statement')],
      assumptions=['The cutoff projector construction and bounds in PG3.',
                   'The good-exponent conditions and actual chain/link letter sets of PG1.'],
      dependencies=['PG1', 'PG3'], sections=[7],
      note='The factorial comparison uses full fixed individual model-letter degrees and fixed outside coordinate exponents; it is not an arbitrary projection on an ungraded lattice.')

claim('PG7', 'Conjugated derivatives retain the weakened chains modulo p^h',
      'For a tangent exponent M supported on frames with each frame degree<=dLL, every digit component of Gamma^(-1) partial^[M](Gamma F) is Q+E with weakened chain levels theta-s and coefficient valuation(E)>=h-n0. The two unit approximations cost12h total. The derivative cost at a chain is the sum over predecessor frames of |M_t|/P_t+h. The model slope hypothesis13 bounds that total by s.',
      'faithful_translation', [
          ms('SumOnLetterApplyInl', 'ChOK', 'invariant_definition'),
          ms('SumOnLetterApplyInl', 'ChOK.dg'), ms('SumOnLetterApplyInl', 'ChOK.ddiv'),
          ms('SumOnLetterApplyInl', 'ChOK.ddiv_all'), ms('SumOnLetterApplyInl', 'sum_ldeg_div_add_le_sl'),
          ms('SumOnLetterApplyInl', 'stepE_of'), ms('CollapseExponent', 'StepE', 'exact_statement')],
      assumptions=['The data gamma and gamma^(-1) approximations.',
                   'The input F has b(F)>=0 and every digit component satisfies the original chains.',
                   'The exact tangent degree caps and slope inequalities of PG1.'],
      dependencies=['PG1', 'PG2', 'PG3'], sections=[9],
      note='The error invariant is preserved under each integral approximation and divided derivative, so the number of frame operations introduces no additional coefficient-valuation loss.')

claim('PG8', 'Explicit factorial-unit conjugation and construction of Omega',
      'On a good exponent zeta with collapsed exponent A and tangent M, A!M!=C_B gamma_dig(zeta) zeta!, with C_B=product(P_t!)^(carry degree_t), constant on a label/tangent block. Approximate gamma_*=gamma(A)gamma_dig and its inverse by integral diagonal g_plus,g_minus modulo p^h, each with order cost<=12h. Omega=diag(g_minus) Pi diag(g_plus) preserves goodness, has chain loss12h and additional link loss24h, and becomes coefficient-integral after p^ceil(Dm+kp/2).',
      'faithful_translation', [
          ms('CollapseExponent', 'DigOK', 'digit_input_statement'), ms('CollapseExponent', 'gaP', 'unit_definition'),
          ms('GlobalTheory', 'kapC', 'block_constant_definition'),
          ms('GlobalTheory', 'kappa_constant_same_block'), ms('GlobalTheory', 'fact_eq_kapC'),
          ms('PrimedEmbeddingInjective', 'exists_approx_gaR'),
          ms('PrimedEmbeddingInjective', 'vala_dg_labels'), ms('PrimedEmbeddingInjective', 'stepG_of'),
          ms('MlabNotMemYset', 'omega_clauses'), ms('UnitLevelOne', 'brDIG', 'explicit_digit_constants')],
      assumptions=['The factorial-unit identity, unit property and integral Mahler/binomial approximations supplied by the companion DT proof.',
                   'The original gamma input of SignedChainData.',
                   'The chain projector PG6 and order calculus PG3.'],
      dependencies=['PG1', 'PG3', 'PG6'], sections=[8],
      note='Uses the source degree6h bounds, even when the companion DT proof supplies stronger ones. The explicit C_B simplifies the more general source kapC after its actual constants are inserted.')

claim('PG9', 'The block factorial cancellation proves near-invariance of the Gram value',
      'The exact identity Lambda(x^zeta)=C_B gamma_*(zeta)(Gamma^(-1)partial^[M]Gamma F)_A zeta! converts Lambda into a blockwise Fock pairing with the conjugated derivative. Its chain-compatible part is fixed by Pi and cancels. Both v(C_B)+v_p(zeta!) and v(C_B)+v_p(zetaPrime!) are >=2n0-2kp; averaging combines this with the projector coefficient bound and error>=h-n0 to give v(Lambda(Omega Z)-Lambda(Z))>=h+n0-2kp-Dm for integral good Z.',
      'derived_simplification', [
          ms('SubstitutedExponentApplyLabel', 'coeff_GM'),
          ms('SubstitutedExponentApplyLabel', 'Lam_monomial_blk'),
          ms('GlobalTheory', 'wt_lower'), ms('GlobalTheory', 'vge_kapC'),
          ms('SubstitutedExponentApplyLabel', 'value_monomial'),
          ms('OmegaValue', 'omega_value'), ms('OmegaValue', 'stepDEF_of')],
      assumptions=['All construction hypotheses of PG6-PG8.',
                   'Fixed label/tangent blocks, so M and C_B are unchanged under the projector.'],
      dependencies=['PG3', 'PG6', 'PG7', 'PG8'], sections=[10],
      note='The source uses a two-case comparison of the two factorial valuations. The report replaces it by averaging the two exact lower bounds. This is an independent short simplification of the actual error proof, not a newly assumed estimate.')

claim('PG10', 'ProjectionDerivativeEstimate is obtained with R equal to zero',
      'Take the constructed Z and G=p^N2 Omega Z, R=0, N2=ceil(Dm+kp/2). The pairing error has strictly larger valuation than Lambda(Z), so detection survives. Since kp>=1, v(Lambda(G))<=n0+Dm+Dl+3kp; integrality gives b(phi G)>=n0-kp/2>=n0-kp. All monomials have the prescribed substituted multidegree. h<=2c gives exactly chain loss24c and link loss60c, with CH>=26 and CE=2.',
      'derived_simplification', [
          ms('TestBoundOfRhoAndNormSets', 'stepBC_of', 'assembly'),
          ms('TestBoundOfRhoAndNormSets', 'plane_gram_theorem_of_combined_lemmas'),
          ms('PlaneGramTheoremOfLemmas', 'plane_gram_theorem_of_five_lemmas', 'assembly'),
          ms('BrData', 'plane_gram_of_theorem_at', 'exact_transport'),
          gb('MonomialOrderSegments', 'stmt', 'closed_source_provider'),
          gb('Lemma5aAt', 'ProjectionDerivativeEstimate', 'target_statement')],
      assumptions=['The exact datum, order, depth and valuation assumptions in PG1.',
                   'The companion representation and digit lemmas as recorded explicitly in PG11.'],
      dependencies=['PG1', 'PG4', 'PG5', 'PG6', 'PG7', 'PG8', 'PG9', 'PG11'], sections=[11],
      note='R=0 is the actual internal witness of the cited combined-lemmas proof, stronger than the exported endpoint. The report also records the slightly stronger weighted lower bound. Neither improvement is silently used to alter the global constant54.')

claim('PG11', 'Shared proof dependencies and the remaining incoming membership condition',
      'IP3--IP5 prove the integral prefix-adapted signed path-column basis, IW4 proves the universal integral projector denominator, and DT1--DT5 prove the factorial-unit approximation. This fragment proves their complete downstream Gram construction, plus V2 and DER. Incoming MemAt, placing the actual selected F2 in XX after initial-symbol construction and c0-word transport, remains a retained application input (DT11). DT7--DT8 prove NoAt/PickAt under the signed datum and MemAt; DT10 proves outgoing MembAt under MFH, Tied, BlockOK, NormTest and YY(24,60). The incoming and outgoing assertions are not identified.',
      'remaining_input', [
          ms('LiftBoundOfHypotheses', 'SPAN', 'shared_IP_interface'),
          gb('Lemma5aAt', 'PathColumnBasisAtRing', 'shared_IP_interface'),
          gb('Lemma5aAt', 'PathSpanAtRing', 'shared_IP_interface'),
          gb('Lemma5aAt', 'ColumnDegreeBoundAtRing', 'shared_IP_interface'),
          ms('BrSpan', 'brSPAN', 'shared_IP_bridge'),
          gb('Lemma5aAt', 'FockProjectorAtRing', 'shared_IW_interface'),
          ms('SecondValuationOfAdmitted', 'brPROJ', 'shared_IW_bridge'),
          gb('GLWeightTheory', 'filtered_projector_corollary_field', 'actual_IW_source_route'),
          ms('LiftBoundOfHypotheses', 'DIG', 'shared_DT_interface'),
          gb('GLWeightTheory', 'lemma_five_two_first_holds', 'actual_DT_source_route'),
          ms('UnitLevelOne', 'brDIG', 'shared_DT_bridge'),
          reference(GB+'TwistedSubstitution/PlaneCoeff.lean', 'MemAt', 'remaining_incoming_membership_interface'),
          reference(GB+'TwistedSubstitution/MemRed.lean', 'memAt_of_wordConditionAt', 'remaining_incoming_transport'),
          reference(GB+'DiagonalSupport/TwiceValuationFactorialProduct.lean', 'PickAt', 'companion_DT8_selection_interface'),
          reference(GB+'DiagonalSupport/TwiceValuationFactorialProduct.lean', 'MembAt', 'companion_DT10_outgoing_membership_interface'),
          reference(GB+'DualFockLinear/RestXiPOfNS.lean', 'NSAt', 'remaining_global_membership_interface'),
          reference(GB+'DualFockLinear/RestXiPOfNS.lean', 'xiAtP_of_NS', 'downstream_application')],
      assumptions=['The exact lattice, degree and prefix hypotheses of IP3--IP5, IW4 and DT1--DT5.',
                   'The incoming MemAt condition and the global parameter/frame supply remain separate from this numerical Gram construction.',
                   'The outgoing MembAt proof in DT10 is conditional on MFH, Tied, BlockOK, NormTest and YY(24,60).'],
      sections=[0, 6, 12],
      note='Remaining_input records incoming MemAt and global numerical frame supply. IP3--IP5 and IW4 have companion proofs independently reviewed by this author; DT supplies factorial units, normal tests, selection and conditional outgoing membership. Their provenance must remain linked in the combined document.')

status_definitions = {
    'faithful_translation': 'A checked translation or complete human proof of the cited source statement with all explicitly named hypotheses, including identified companion lemmas.',
    'derived_simplification': 'A shorter human argument or stronger consequence extracted from the actual source proof, not asserted as a pre-existing named Lean declaration.',
    'remaining_input': 'An exact external dependency or global construction not proved inside this fragment; its status in companion work is kept separate.'}
out = dict(schema_version='1.0', artifact_version='0.5', date='2026-11-21', owner='lean_audit',
           repository=dict(url=REPO, commit=COMMIT),
           verification=dict(source_ranges_checked=True, source_hashes_recorded=True,
                             local_lean_compilation=False, kernel_replay=False,
                             full_headline_call_path_traced=False),
           status_definitions=status_definitions, claims=claims, source_manifest='source_manifest.json',
           companion_dependencies=[
               dict(component='IP', claims=['IP3', 'IP4', 'IP5'], statement='Proved integral signed path-column basis adapted to all prefix minimum/maximum cutoffs, with exact column factors and colVal clauses; see report section6.'),
               dict(component='IW', claim='IW4', statement='Universal isotypic-projector denominator for torus-graded divided-power-stable lattices; same-coordinate two-weight difference parameter.'),
               dict(component='DT', claims=['DT1', 'DT2', 'DT3', 'DT4', 'DT5'], statement='Integral binomial-polynomial approximation of factorial digit units and inverses.'),
               dict(component='DT', claims=['DT7', 'DT8', 'DT10', 'DT11'], statement='Normal test and coefficient selection under incoming MemAt; outgoing MembAt proved under MFH and the stated datum; incoming MemAt retained.')])
(OUT/'provenance.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
(OUT/'source_manifest.json').write_text(json.dumps(dict(repository=out['repository'], files=[files[p] for p in sorted(files)]), indent=2, ensure_ascii=False)+'\n')
print(json.dumps(dict(claims=len(claims), source_files=len(files), source_references=sum(len(c['sources']) for c in claims),
                      statuses={s: sum(c['status'] == s for c in claims) for s in status_definitions})))

