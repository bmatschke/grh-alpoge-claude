#!/usr/bin/env python3
"""Reproduce the FC source ledger from immutable Lean bytes, without a build.

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
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
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


common = [
    'The actual true-column arithmetic host B, PreX X, TC I, I.Ok, TC.Pins, I.Laws l and TC.Later Z are supplied. The underlying field, prime, character and column-law existence is not proved here.',
    'The indicated decorated lattices have unitary finite-adelic realizers. Their construction in exists_isPtOf_cm remains explicit. AD1 proves the canonical diagonal base point; AD3 and AD4 prove supported splicing and modification conditional on realizers.',
    'All coordinates, class representatives, selected-prime orientations, determinant labels, and finite characters are the original supplied choices. SF2 gives gramN=I and IdY in those exact coordinates.',
    'Hermitian duals mean O_E-valued integrality with conjugation in the first argument; they are not trace duals.',
    'No complete RH or GRH theorem, full FormsTiedSym/ColsTiedSym supplier, primitive host existence, or Lean kernel replay is asserted by this component.'
]


def claim(i, title, statement, deps, assumptions, srcs, relation, status='derived_simplification'):
    return dict(id=i, title=title, status=status, statement=statement, depends_on=deps,
                assumptions=common + assumptions, proof_location=dict(file='main.tex', anchors=[i]),
                expanded_notes=dict(file='report.txt', section=i), source_relation=relation,
                mathematical_status='proved_under_exact_declared_supplied_data_hypotheses', sources=srcs)


claims = []
claims.append(claim('FC1', 'Level-prime bijection and exact real residue field',
    'The norm/cardinality and coprimality data imply (pi)=product_{P in S} P with exponent one, the selected-prime restriction bijection underT, and the exact residue-field isomorphism induced by O_F -> O_E/P. The selected orientation is retained.', [],
    ['The f selected primes have residue cardinality p, pi*bar(pi)=p, and (pi,bar(pi))=1. The original coefficient-place embedding/prime correspondence for tauOf and seenP is supplied.'],
    ss(I+'UnderTBijective.lean', 'underT underT_bijective atTTied exists_atTTied') +
    ss(I+'ResidueFieldEquivRealSubfieldQuotientTrueColumns.lean', 'exists_intF res_algebraMap_surjective exists_fv_equiv fv_equiv_quot') +
    ss(C+'RecLevelLocT.lean', 'BasePi', 'literal_prime_divisibility_predicate') +
    ss(C+'AbelianHostFieldConditions.lean', 'Primes.Ok', 'supplied_prime_and_norm_data'),
    'Norm-factorization and the explicit z=y*bar(pi)+bar(y)*pi residue lift replace a black-box field-cardinality identification.'))

claims.append(claim('FC2', 'Coupling reductions determine and realize the coset',
    'For the empty reference twist set, two coupling cosets with identical auxiliary reductions are equal, and every prescribed auxiliary reduction tuple lifts to a coupling coset by local lifts and Chinese remaindering.', [],
    ['The supplied decorated-lattice reduction maps have kernel q_P D_P, and q_P is a uniformizer at the designated auxiliary prime.'],
    ss(I+'ColumnPointEqOfDecoAndCosetReduction.lean', 'inv_smul_mem_of_be_eq_zero sub_mem_of_be_eq coset_eq eq_of_deco_bar') +
    ss(I+'ExistsCouplingCosetWithGivenReduction.lean', 'exists_one_intAt_div exists_vec coset_be exists_ptAt_bar_eq'),
    'Gives explicit y=sum_P(e_P/q_P)x_P and checks every localization and reduction; this is not adelic realizability.'))

claims.append(claim('FC3', 'Actual finite charts and their point-reading identities',
    'Finite normalized coupling labels partition the actual decorated-lattice classes into charts. The exact double-coset bijection, stabilizer image, inverse character orientation and ReadsK identities hold for the chosen yStd; endpoint chart types are singletons.', ['FC2', 'AD1'],
    ['Actual unitary finite-adelic realizers are supplied for the decorated points. Finite orbit/stabilizer laws and preferred normalization are the original column data.'],
    ss(I+'ExistsMemberStepCharts.lean', 'chart_exists lev_iff chr_eq prefRep_normal cls_bij stM_range bar_norm chart_of exists_charts') +
    ss(I+'ExistsMemberStepCharts.lean', 'yStd_spec', 'retained_realizability_use') +
    ss(I+'ExistsAdelicPointDecoratedLatticeAllTwists.lean', 'exists_ptOf_twists', 'retained_realizer_wrapper'),
    'Proves orbit and stabilizer correspondences using FC2, including the inverse from the right finite action; it retains the geometric point-existence input.'))

claims.append(claim('FC4', 'Normalize residue functionals without changing levels',
    'For the standard base lattice L_pi, replacing any allowed prime-cardinality residue functional by f0(x)=bar(pi)*x_n modulo pi preserves the local unitary level subgroup, all chart carriers and ReadsK, and makes pi annihilate the functional.', ['FC1', 'FC3', 'SF3'],
    ['The supplied functional is nonzero, kills L_pi and is O_E-linear into an additive group of order p.'],
    ss(I+'InclMulInvMul.lean', 'kill_or ker_of_prime stabFun_congr stab_eq charts_funKilled') +
    ss(C+'RecLevelLocF.lean', 'fMod_card', 'source_prime_cardinality_input'),
    'A complete discriminant-module calculation L_pi#/L_pi=A/pA proves the equality of stabilizers in both possible prime orientations, including n=1.'))

claims.append(claim('FC5', 'Exact quotient projections and their kernels',
    'If two lattices have the indicated equal localization, pr(x)=bar(s)^(-1)[s*x] is well-defined, linear and surjective with kernel P*A. Applying it to the actual decorated lattices gives the literal IdL projections and level-functional kernel identities.', ['SF2'],
    ['The original decorated-lattice self-duality and reduction laws identify the localizations of L#, N, L+P L# and dnN; no new local lattice is substituted.'],
    ss(I+'ReductionModPrimeLevelPrimeSmulEq.lean', 'proj proj_mk proj_smul proj_surj proj_ker dualL_one localization_L_eq_localization_dnN localization_Lsh_eq_localization_N localization_sup_eq_localization_dnN f_eq_zero_iff reductionModPrime_levelPrime_smul_eq exists_level_projections'),
    'Clearing denominators, Bezout and a common-denominator calculation prove all quotient-map and kernel assertions.'))

claims.append(claim('FC6', 'Explicit residue comparison with the chart functional',
    'The normalized functional has a unique additive isomorphism with O_E/P, satisfying e(f(x))=rho_P(bar(pi)*x_n). The exact chart realizer and denominator projection give FvTieG; the last-coordinate Hermitian formula gives TilBaseFv once the terminal vector/incidence is supplied.', ['FC1', 'FC3', 'FC4', 'FC5', 'AD1'],
    ['The terminal TilBaseFv consequence alone retains the specified terminal incidence/vector input; no til_ties construction is claimed here.'],
    ss(I+'ChartTiedLevelChain.lean', 'exists_equiv f_eq_rho exists_equiv_level fv_of_smul fvTieG') +
    ss(I+'ExistsStandardFormComparisonSymmetricLevelMember.lean', 'hform_last sigD_conj'),
    'Checks the actual quotient map, bar(pi) multiplier, inverse-realizer order and cancellation of all projection denominators.'))

claims.append(claim('FC7', 'Fock metrics, rational Gram bases and every complex embedding',
    'The normalized factorial Fock pairing is unitary-invariant and has the source pairing order. The actual cmMax-valued chosen invariant basis gives the literal class-sum Gram matrix and positive-definite image at every complex embedding. This proves IpVTieG/NormTieG and the corresponding terminal metric under its row chart.', ['FC3', 'SF2', 'CV1'],
    ['Finite-order character data and FOk are supplied. The terminal application requires its actual ReadsP row chart. Only cmMax-valued basis coefficients are commuted through conjugation at arbitrary embeddings.'],
    ss(I+'UnitaryOfIsON.lean', 'nfAll_shift unitary_of_isON map_pairVr_rat norm_step ipVal_step ipV_norm_tie') +
    ss(I+'WeightLawGoodOfFieldEmbedding.lean', 'map_mulVec_injective gram_map gram_posDef root_mem_cmMax rho_rat hasRatBasis gramV_posDef step_gram_posDef lawGood') +
    ss(D+'Proofs/SatakeParameters/HasRatBasisOfAct.lean', 'hasRatBasis_of_act repr_mem_of_isRat') +
    ss(F+'Divisibility/ClassSum.lean', 'IsRat HasRatBasis basis csum H gramV', 'literal_chosen_basis_and_Gram_definitions') +
    ss('src/Formalism/QuotientMetricDivisors/RatHermLcvTwist.lean', 'cmMax', 'literal_conjugation_stable_subfield'),
    'Uses the Gaussian/factorial formula, explicit coefficient-field descent, the source chosen cmMax basis, and an injective finite value matrix. It does not assume an arbitrary coefficient field commutes with conjugation at every embedding.'))

claims.append(claim('FC8', 'Period comparison by coefficient conjugation',
    'Coefficient conjugation gives a conjugate-linear bijection from the terminal period space to the class polynomial space, intertwines the actual stabilizer actions, identifies the period with the stated Hermitian pairing in its correct order, and proves strict positivity for nonzero vectors.', ['FC7', 'CV1'],
    ['The literal terminal period and finite stabilizer laws are supplied; the period-space subgroup is the whole specified group.'],
    ss(I+'CevInjective.lean', 'cev cev_injective exists_cev cev_act jM jM_injective jM_onto petersson_apply period_eq re_petersson_self_pos period_conj'),
    'Proves stabilizer-independent orbit extension and surjectivity, then computes each Fock summand and inverse-stabilizer weight.'))

claims.append(claim('FC9', 'Actual Hermitian carrier conversion',
    'Exact rank reindexing transports a chart level/class structure to its Hermitian carrier, with identical lattice, local/global level groups, class matrices and stabilizer matrices. Given standard forms, this constructs the full CarH; the level-zero part needs only cls0, GLoc and GLev0.', ['FC1', 'FC3', 'FC4', 'FC14', 'LP1'],
    ['The full CarH statement assumes the relevant standard forms/charts already supplied. The separately used level-zero carrier requires no terminal or penultimate symmetric structure.'],
    ss(I+'HermitianStepLevelOfChartFormsLevel.lean', 'exists_herm_level uloc_T_iff baseL_eq level_of_chart') +
    ss(I+'HermitianClassConditionOfChartClasses.lean', 'classTie_of_reindex classTie_of_chart') +
    ss(I+'ColumnLevelOfStepZeroFormsLevelTrueColumns.lean', 'exists_reindex stab_class_lattice exists_colLevel colLevel_of_forms') +
    ss(I+'HermitianColumnChoicesOfFormsLevelsClasses.lean', 'hermColsCh_of_forms') +
    ss(A+'StdLvPr.lean', 'CarH', 'literal_same_carrier_record'),
    'The construction changes indices only. Local-to-global membership proves stabilizer preservation of the actual global class lattice.'))

claims.append(claim('FC10', 'Step-zero uniformizer annihilation on the same carrier',
    'The exact form residue comparison and prime-cardinality target imply pi*f=0. Transporting this functional to the level-zero ColLevel leaves every carried lattice/group/class/stabilizer unchanged and gives the actual uniformiser_kills_values supplier.', ['FC6', 'FC9'],
    ['The selected residue target has additive prime order; its nonzero element is supplied by surjectivity of the quotient projection.'],
    ss(I+'StepZeroHermitianLevelUniformiserKillsValues.lean', 'fun_transport smul_eq_zero_of_prime_card pi_kills stepZeroHermitianLevel_with_formsFunctional stepZeroHermitianLevel_uniformiser_kills_values'),
    'A nonzero element generates the prime-order additive group, so annihilation of one such element gives the entire target assertion.'))

claims.append(claim('FC11', 'Move factorization and local basis correction',
    'Once a move has the stated realizer and preserves the chart label, the exact factorization y_c*delta=gamma*y_cprime*kappa, its character scalar and frame transport follow. Vectors equal modulo P*A yield the same one-column enlarged local lattice; denominator cancellation extends local functional identities.', ['FC3', 'FC5'],
    ['This primitive move algebra assumes the relevant neighbor geometry, realizing point and chart preservation. NB supplies up/down geometry; FC18 supplies diamond geometry.'],
    ss(I+'InvSmulMem.lean', 'inv_smul_mem loc_sup_le exists_level upNatTie', 'move_algebra_subarguments; full_naturality_closed_by_NB') +
    ss(I+'ChartTiedLevelChainHost.lean', 'tr_eq_of_isTr dnNatTieG_cols', 'exact_down_frame_and_character_transport'),
    'Separates the proved character/basis algebra from the geometric neighbor supply, so it may be used by NB without depending on final FC19.'))

claims.append(claim('FC12', 'Actual common penultimate level and its finite carrier',
    'The zero-coupling preferred chart supplies a common level J containing every penultimate chart level, with exactly the same carried lattice and restricted character. Finite reduction kernels give finite coset sets; their disjoint union supplies the actual transitive-orbit and stabilizer carrier Yb.', ['FC2', 'FC3', 'AD1'],
    ['The specified HSym matrix-shape and lamSym character formula are not proved here; a generic finite reduction image is not substituted for them. The supplied last_uniq finite reduction action is used.'],
    ss(I+'ChartTiedTopLevelChain.lean', 'BasePt.conj BasePt.red basePt_of exists_orbits cosetIn_of_zero_mem reads_base reads_pt read_of_mem mem_of_read') +
    ss(I+'ChartTiedTopLevelChain.lean', 'exists_gLevH stepBefore_oneLevel', 'partly_reconstructed; special_HSym_lamSym_fields_retained'),
    'Proves the actual common subgroup, character restriction, finite indices and orbit carrier; explicitly isolates only the unreconstructed special shape/character identification.'))

claims.append(claim('FC13', 'One common auxiliary-prime GLoc and its characters',
    'The supplied split-prime and character data construct one common GLoc for every word: oriented split factors, canonical prime-field residue identifications, transported additive characters and the prescribed distinct multiplicative characters. IdG, piG_K and CharacterCompatible hold for these exact choices.', ['FC1'],
    ['Complete splitting, the piG elements, original field embeddings, character-agreement data and an injective primitive multiplicative character are supplied host clauses.'],
    ss(I+'ExistsGLocIdGChiTied.lean', 'nonempty_equiv_zmod orderOf_ofUnitHom exists_oriented exists_gLoc exists_gLoc_idG_chiTied') +
    ss(C+'AbelianHostFieldConditions.lean', 'Chars.Ok', 'supplied_character_existence_and_compatibility') +
    ss(A+'LatAtLattice.lean', 'IdG', 'literal_GLoc_identification'),
    'Constructs the transported characters explicitly, identifies all residue elements with integers, and checks multiplicative order and selected orientation.'))

claims.append(claim('FC14', 'Chart levels from finite reduction images',
    'At auxiliary primes the actual carried lattice has standard completed frame. The kernel of first-factor reduction fixes the decoration, coupling and character. Therefore each Uloc is the inverse image of its finite reduction image, its character descends, and the global character is the exact product of the local inverse characters. This constructs chart_gLevH.', ['FC3', 'FC13', 'SF5'],
    ['The original chart level character is trivial off the finite bad-prime set, as required by its supplied StepLevel laws.'],
    ss(I+'ValLtOfRedM.lean', 'chi_eq_prod exists_gLevH latS_eq_std isPtOf_mul reads_gLevH chart_gLevH'),
    'A kernel-and-image proof constructs the group and character, rather than recording the abstract existence of GLevH.'))

claims.append(claim('FC15', 'The specified step-zero auxiliary level',
    'For the singleton step-zero chart, the exact finite group is the prescribed upper-unitriangular group. Its additive character is the negative superdiagonal sum under inversion, yielding the literal lamJ and GLev0 with identity local frame.', ['FC3', 'FC13', 'FC14'],
    ['The original idx_ok.zero_G and step-zero column character formula are supplied. The exact rank identity N(0)=k is used throughout.'],
    ss(I+'LevelTwistPrimesStepZeroCharacterEqOne.lean', 'lev_iff mem_colLev_zero chr_colLev chi_eq inJ_iff prod_places supSum_inv lamJ_zero mem_Uloc chi_prod exists_glev glev_zero') +
    ss(C+'GenericUnipotentCharacter.lean', 'uniUT supSum sup_mul', 'literal_upper_unipotent_group_and_additive_character') +
    ss(HF+'PsiZeroNontrivialCharacter.lean', 'InJ lamJ GLoc GLev', 'literal_required_auxiliary_level_shape'),
    'Checks the finite reduction group and sign of the character, rather than identifying groups only up to isomorphism.'))

claims.append(claim('FC16', 'Exact level-zero joins for concrete comparison',
    'Every level-zero additive character value lies in the original coefficient field by its supplied roots_Ks. The exact reindexed level-zero carrier supplies Joint0; SF2 supplies StdTied; its actual L_pi base lattice supplies the companion ideal (bar(pi)) by SF3. Terminal CarT is unnecessary for these joins.', ['FC1', 'FC9', 'FC13', 'FC15', 'SF2', 'SF3'],
    ['The host contains the specified primitive q_j(q_j-1)-th roots of unity. A completed Forms0 with the same cls0 is used for the Joint0 predicate; FC19 gives that direct completion.'],
    ss(I+'AdditiveCharacterTypePrimesValuesCoefficientFiel.lean', 'natCast_resField_eq_zero range_of_pow_g additiveCharacter_typePrimes_values_coefficientField') +
    ss(G+'DownNaturalLevelZero.lean', 'Forms0 Joint0', 'literal_record_and_same_carrier_join') +
    ss(G+'TiedFamilies/ChiMemSubfield.lean', 'LevelZeroCharacterRational', 'literal_comparison_rationality_premise') +
    ss(G+'Joint0.lean', 'FormsTiedSym.to0 ColsTiedSym.joint0', 'source_projection_path_bypassed_by_direct_FC19_construction'),
    'The roots-of-unity argument does not use IdG. All five SameCar fields and the rank reindexing are retained, avoiding reliance on an unrelated terminal carrier.'))

claims.append(claim('FC17', 'Distinguished-block integral lattice comparison',
    'At a seen coefficient prime over T, the residue-kernel lattice localizes to L+P L# in the distinguished block and to L# in every other selected block. Exact localized Weyl transport and one common class denominator prove all of BwTieG with the literal piecewise inverse-frame polynomial.', ['FC5', 'CS3', 'CV6', 'CV7', 'CV8'],
    ['This statement is only for seen coefficient primes of residue characteristic T, using the original exact tauAt place correspondence. The class-local bases do not replace the common SF frame.'],
    ss(I+'IsBasisAtOfIsLocBasis.lean', 'isBasisAt_of_isLocBasis localization_LshKer_eq_localization_sup mem_localization_ker mem_localization_latticeOf bw_tie'),
    'Proves the exceptional-prime and all other-prime localizations directly, then uses the already reconstructed integral transport. The universal basis formulation is nonvacuous because both lattices are full.'))

claims.append(claim('FC18', 'Actual diamond naturality from the functional equation',
    'Any IsDia element has inverse last-row reduction equal to the prescribed scalar. Multiplication with the exact kStd realizer changes only the selected residue functional, hence realizes dia1, preserves the normalized coupling label, and gives every DilationCompatibleChart clause and the endpoint ValTied dilation field.', ['FC2', 'FC3', 'FC4', 'FC6', 'FC11', 'AD1'],
    ['The literal IsDia condition is imposed on an arbitrary given element; no additional existence of a diamond matrix is assumed. The supplied dia_act equivariance is used for normalization.'],
    ss(HF+'IsLocBasis.lean', 'IsDia', 'literal_diamond_condition') +
    ss(I+'DiamondElementIntegralSupportLastRow.lean', 'last_row dia_data', 'last_row_subargument_replaced_by_functional_calculation') +
    ss(I+'IsPointOfLastCoordinateDilationOnePrime.lean', 'isPointOf_last_coordinate_dilation_one_prime_alt') +
    ss(I+'DiamondOperatorsOnCharts.lean', 'normal_rep cosetIn_rep exists_level isPt_dia dilTied'),
    'Integrality follows from FC4. Test the normalized functional on coordinate vectors, then reduce the exact matrix product and apply the already proved factorization algebra.'))

claims.append(claim('FC19', 'Direct Forms0 construction and every matching global comparison input',
    'For the actual D=I.rec7 l Z, the proved fields and NB7/NB8 construct every Forms0 field directly, then the exact level-zero ColLevel carrier and Joint0, StdTied, LevelZeroCharacterRational and companion ideal (bar(pi_u)) for all words. The common G and standard frame B=I are retained. This supplies every global input of VE9 without using full FormsTiedSym/ColsTiedSym or terminal CarT.',
    ['FC1', 'FC3', 'FC4', 'FC5', 'FC6', 'FC7', 'FC9', 'FC13', 'FC14', 'FC15', 'FC16', 'FC17', 'FC18', 'CV9', 'NB7', 'NB8', 'SF2', 'SF3', 'LP1'],
    ['NB7 and NB8 prove the actual up/down naturality from primitive FC/AD statements without a dependency back on FC19. They are results, not additional unreconstructed naturality inputs.',
     'The actual initial full IsPtOf realizer supply remains explicit. The special penultimate HSym/lamSym identification, terminal row level/ReadsP, terminal til_ties and full CarT are separate remaining fields of the full FormsTiedSym/ColsTiedSym endpoint, not hypotheses of this direct Forms0 construction.'],
    ss(I+'ExistsStandardFormComparisonSymmetricLevelMember.lean', 'formsTiedSym_std', 'partially_reconstructed_full_simultaneous_endpoint') +
    ss(I+'HermitianColumnChoicesOfFormsLevelsClasses.lean', 'hermColsCh_of_forms', 'complete_conditional_carrier_assembly') +
    ss(I+'ExistsStandardColumnComparisonsTrueColumns.lean', 'colsTiedSym_std', 'retained_full_terminal_column_endpoint') +
    ss(G+'DownNaturalLevelZero.lean', 'Forms0 Joint0', 'directly_constructed_record_and_join') +
    ss(I+'MemFiCComp.lean', 'mem_FiC_comp clsOfChart valOfG lvOfG fvOfG upOfG dnOfG normOfG bwOfG readsK_one', 'literal_chart_to_endpoint_conversions_reconstructed') +
    ss(D+'Proofs/GlobalInterpolation/ExistsSmulMemOfMemLocW.lean', 'exists_smul_mem_of_mem_locW mem_of_forall_locW', 'all_prime_integral_recovery_proved_by_annihilator_ideal') +
    ss(I+'ColumnLevelOfStepZeroFormsLevelTrueColumns.lean', 'exists_reindex exists_place exists_colLevel', 'source_proof_uses_only_step_zero_fields') +
    ss(F+'HermitianColumns/ZeroPointScaledByCharacter.lean', 'StdTied', 'literal_standard_positive_space_predicate') +
    ss(A+'TrueColumnChoicesHeckeCharReferenceEqOne.lean', 'GlobalTheory.Mem.Col2.ColIn.Ok', 'literal_supplied_true_column_record') +
    ss(A+'LatAtLattice.lean', 'Laws Pins Later', 'literal_supplied_laws_pins_later_records'),
    'Constructs every Forms0 field individually, proves localization-to-global integrality, extracts the level-zero-only source carrier proof, and checks all five SameCar identities plus exact split/frame/character/companion joins. FC19 supplies VE9 inputs but does not depend on VE9.'))


next_specs = [
    (1, I+'ValuedLtOfMem.lean', 'exists_isPtOf_cm',
     'Construct a unitary finite-adelic realizer of the actual decorated lattice. AD1 proves kStd, AD3 proves supported splicing given realizers, and AD4 proves modification preserving the carried lattice; those do not construct the starting realizer. The remaining substantial source route invokes unimodGenus and the actual unitary genus realization.',
     ['unimodGenus', 'ExistsAdelicPointDecoratedLatticeAllTwists.lean:exists_ptOf_twists']),
    (2, I+'ChartTiedTopLevelChain.lean', 'exists_gLevH',
     'Identify the already constructed common penultimate level from FC12 with the particular HSym matrix shape, and identify its character with the literal lamSym. FC12 already proves the same common subgroup, chart inclusions, character restrictions, finite coset carrier and orbit/stabilizer identities; those are excluded from this remaining scope.',
     ['SymmetricLevelBoundLe.lean', 'SymmetricFlagBasisVectorEqSingleOfNoExtra.lean', 'ChrLast.lean', 'stepBefore_oneLevel']),
    (2, I+'LevelsTopRowSym.lean', 'levels_top_row_sym',
     'Construct and identify the specified terminal full/row auxiliary levels, lamM/lamP, their eigenvalue identity and exact common frames. CV10 and FC7 already prove terminal values and norms once the actual row chart ReadsP is supplied; no second value or metric proof is needed.',
     ['ExistsEmbFIff.lean:clsP_tie', 'frExt_of']),
    (3, I+'HermitianFormLastCoordinateUniformizerVectorSelf.lean', 'til_ties',
     'Construct the exact terminal vector/incidence lattice and adelic extension/evaluation identities for the same chart representatives. The scalar Hermitian last-coordinate identity is already FC6; it does not establish this geometric incidence supplier.',
     ['ExistsStandardFormComparisonSymmetricLevelMember.lean:formsTiedSym_std']),
    (3, I+'HermitianDataAtLevelPrime.lean', 'hermitian_data_at_level_prime',
     'Tie the terminal row lattice, class/stabilizer data, terminal vector, projections and all level-prime move data to the same Hermitian carriers, producing the literal CarT. Reuse FC5/6 projections, FC9 CarH and the separately reconstructed neighbor/dilation geometry; retain only exact terminal realization and same-object joins.',
     ['StdLvPr.lean:CarT', 'HermitianColumnsGeneratorsBaseLatticesFunctional.lean:herm_rest_tied', 'ExistsStandardColumnComparisonsTrueColumns.lean:colsTiedSym_std'])
]
targets = []
for group, path, name, scope, connections in next_specs:
    item = source(path, name, 'remaining_human_reconstruction_target')
    item.update(priority_group=group, remaining_human_scope=scope, source_connections=connections,
                human_status='not_claimed_proved_by_FC; completed_subarguments_explicitly_excluded')
    targets.append(item)

out = dict(schema_version='1.3', artifact_version='0.14', date='2026-11-21', owner='/root/global_frame',
    repository=dict(url=URL, commit=PIN),
    range_convention='One-indexed inclusive. Exact original bytes from declaration first line through its final nonblank line before the next top-level declaration/directive. No newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True, range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True, human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False, local_lean_compilation=False, lean_kernel_replay=False,
        replacement_arguments_formalized=False, pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof under the exact stated supplied-data premises, often by a shorter argument.',
        conditional_assembly='Fieldwise assembly of proved constructions with each additional input stated explicitly; not the unreconstructed full endpoint.'),
    claims=claims, files=[files[p] for p in sorted(files)],
    artifact_sha256={p: digest((HERE/p).read_bytes()) for p in ['main.tex', 'report.txt']},
    prior_components_reused=['SF', 'LP', 'CS'], same_iteration_companions=['AD', 'CV', 'NB', 'VE'],
    independent_reviews=[], retained_inputs=common,
    scope_precision=[
        'FC3 constructs primitive charts before CV9 constructs their values; FC7/8 use only CV1, and FC17 only CV6--CV8.',
        'NB uses primitive FC2/5/6/11 only. The final FC19 assembly may depend on NB; there is no reverse edge from primitive FC to FC19.',
        'FC4 and FC10 replace only functional fields, preserving all carried lattices, groups, representatives and stabilizers.',
        'The Fock normalization divides by the product of highest-polynomial squared norms. IpV uses the source reversed argument order.',
        'Only the chosen cmMax-valued basis pairings are commuted through arbitrary embeddings; no false arbitrary-LL conjugation identity is used.',
        'FC12 proves the actual common penultimate level/carrier but not the special HSym/lamSym identification.',
        'FC19 uses only step-zero fields for Forms0; the open terminal incidence and symmetric-penultimate fields are separate.'])

review = HERE.parent / 'reviews_v0_14' / 'cv_reviews_fc.txt'
if review.exists():
    review_raw = review.read_bytes()
    review_text = review_raw.decode('utf-8')
    main_raw = (HERE/'main.tex').read_bytes()
    hashes = {}
    for i in [4, 7, 8]:
        start = main_raw.index(f'\\paragraph{{FC{i}:'.encode())
        end = main_raw.index(f'\\paragraph{{FC{i+1}:'.encode(), start + 1)
        sha = digest(main_raw[start:end])
        assert sha in review_text, ('independent review paragraph changed', i, sha)
        hashes[f'FC{i}'] = sha
    out['independent_reviews'].append(dict(reviewer='/root/comparison_span', result='PASS', claim_ids=list(hashes),
        scope='Focused mathematical and pinned-source review of discriminant-module functional normalization, cmMax Gram positivity and period coefficient conjugation.',
        review_record='../reviews_v0_14/cv_reviews_fc.txt', review_record_sha256=digest(review_raw),
        paragraph_sha256=hashes, paragraph_range='Bytes from the named paragraph marker up to but excluding the next FC paragraph marker.',
        lean_replay=False))

review19 = HERE.parent / 'reviews_v0_14' / 'cr_reviews_fc19.txt'
if review19.exists():
    review_raw = review19.read_bytes()
    review_text = review_raw.decode('utf-8')
    main_raw = (HERE/'main.tex').read_bytes()
    start = main_raw.index(b'\\paragraph{FC19:')
    sha = digest(main_raw[start:])
    assert sha in review_text, ('independent FC19 review paragraph changed', sha)
    out['independent_reviews'].append(dict(reviewer='/root/class_rank', result='PASS', claim_ids=['FC19'],
        scope='Independent field-by-field construction of Forms0 and its exact level-zero ColLevel/Joint0/StdTied/character/companion joins, without a full terminal form record.',
        review_record='../reviews_v0_14/cr_reviews_fc19.txt', review_record_sha256=digest(review_raw),
        paragraph_sha256={'FC19': sha}, paragraph_range='Bytes from the FC19 paragraph marker through EOF.', lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
locators = []
for c in claims:
    locators += [f"{c['id']} | {c['title']} | {c['status']}", c['statement']]
    for s in c['sources']:
        locators += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
                     f"  role: {s['role']}", f"  file_sha256: {s['sha256']}",
                     f"  range_sha256: {s['range_sha256']}", f"  {s['url']}"]
    locators += ['']
(HERE/'source_locators.txt').write_text('\n'.join(locators)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN, files=out['files']), ensure_ascii=False, indent=2)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.14', commit=PIN, targets=targets,
    source_files=[files[p] for p in sorted({t['path'] for t in targets})]), ensure_ascii=False, indent=2)+'\n')
print(json.dumps(dict(claims=len(claims), source_links=sum(len(c['sources']) for c in claims),
    source_files=len(files), next_targets=len(targets), verified_equal_to_pinned_git_blob=True,
    independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))
