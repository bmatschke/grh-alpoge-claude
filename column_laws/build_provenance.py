#!/usr/bin/env python3
"""Reproduce the TL source ledger from immutable Lean bytes, without a build.

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
PI = 'src/Formalism/PeriodIntegrals/'
CM = 'The number fields and their actual involution/embeddings are supplied; at every embedding of E the involution is complex conjugation. Hermitian duality is O_E-valued and conjugate-linear in its first variable.'
CORE = 'For the actual true-column application the literal TC.Ok, including ChIdx.Ok, is supplied. No Pins, Laws, Later, FC19, terminal comparison or point realizer is an input to the reconstructed Ok-to-Laws implication.'
GEN = 'Generic GStep.Ok/FOk or the explicitly stated generic ChainIn.Ok, AtIn.Ok and PerIn.Ok are supplied, with their actual lattices, representation, dominant weights and coefficient places.'
BOUND = 'Primitive arithmetic-host/context existence and Later stage existence are not asserted. No Lean kernel replay, source edit, or formalization of the shorter human proof is asserted.'


def cl(i, title, statement, deps, assumptions, sources, relation, conditional=False):
    return dict(id=i, title=title, status='derived_simplification', statement=statement,
        depends_on=deps, assumptions=[CM, BOUND]+assumptions,
        proof_location=dict(file='main.tex', anchors=[i]),
        expanded_notes=dict(file='report.txt', section=i),
        mathematical_status=('proved_conditional_reduction_with_retained_primitive_suppliers' if conditional
                            else 'proved_under_exact_declared_supplied_data_hypotheses'),
        source_relation=relation, sources=sources)


claims = [
cl('TL1','Finite rational-unitary classes of self-dual Hermitian lattices',
   'For fixed E,n satisfying positivity at all complex embeddings, full self-dual O_E-lattices have finitely many rational-unitary isometry classes and finite automorphism groups. The proof gives a trace-Gram determinant bound and an elementary short-independent-vectors/finite-overlattice argument retaining the O_E action.',
   [], ['The Hermitian form is the standard positive form and the lattice is full and self-dual; rank zero is included.'],
   ss(C+'DecoFin.lean','PosStar posStar_of_conj hStd_pos unimod_finite')+
   ss(A+'PredMemGamRanks.lean','autO autO_finite autOrd_finite'),
   'Replaces the long trace-real/class-set intermediate route by a complete bounded-Gram and bounded-action proof. Does not assert all self-dual lattices are mutually rationally isometric.'),
cl('TL2','Finite decorated, framed and coupling orbits with stabilizer divisibility',
   'Finite decoration fibers, local frame torsors modulo finite-index levels, and finite coupling quotients give finite actual step orbits. Stabilizers inject into finite lattice automorphism groups; their orders divide positive DGam at the specified ranks.',
   ['TL1'], ['The finitely many actual residue fields and local-frame groups are supplied; each twist-frame level has finite index. Coupling sets have the stated finite local denominator bounds.'],
   ss(C+'DecoFin.lean','Deco.Ok.f_eq_of_span Deco.Ok.be_eq_of_span DecoSet.finite_fibre DecoSet.finite_reps DecoSet.finite_orbits DecoSet.stab_fst_injective DecoSet.finite_stabilizer')+
   ss(S+'ExistsSmulOfDecoEq.lean','exists_smul_of_deco_eq stab_inj incl_injective grp_finiteIndex chr_root frmGSD_ok main')+
   ss(I+'FiniteOrbitsOfFiniteFibres.lean','finite_orbits_of_finite_fibres stepY_ok')+
   ss(I+'YsAtFiniteNonempty.lean','finite_cosets ysAt_finite_nonempty')+
   ss(A+'PredMemGamRanks.lean','gamRanks gamOrd DGam gamOrd_finite dvd_DGam DGam_pos')+
   ss(A+'ExtUHInjective.lean','stabAut stabAut_inj stepY_dvd'),
   'Proves the actual finite-fiber and stabilizer mechanisms, including recovery of all auxiliary/Q-frame factors, not only cardinality equality of unnamed orbit sets.'),
cl('TL3','Finite-index actual twist levels and root-of-unity characters',
   'The boundQ inclusions in ChIdx.Ok imply the q^(j+1) principal congruence kernel lies in actual levQ. Top and row levels are congruence or residue preimage levels. Their character formulas have finite-order values. Together with TL2 all actual GStep.Ok clauses follow and survive reRep.',
   ['TL2'], [CORE, 'The displayed local-index lattice bounds, level-group and character identities are literal supplied ChIdx.Ok clauses.'],
   ss(I+'LevQFiniteIndexAndRoot.lean','exists_int_congr finiteIndex_of_cong conj_extE_cong mem_Jat lev_finiteIndex tame_root levQ_finiteIndex_and_root')+
   ss(A+'CongruenceLevelEqDepthSucc.lean','levCong prinCong_le_levCong levCong_root topLev_finiteIndex topLev_root')+
   ss(A+'CardStabilizerForgetFr.lean','levRed_finiteIndex levRed_root levQX_finiteIndex levQX_root')+
   ss(I+'TrueColumnChainsSatisfyConditions.lean','GStep.Ok.reRep unrepresented_step_conditions stp_ok')+
   ss(A+'PredMemGamRanks.lean','GStep.Ok'),
   'Derives finite index using exact depth j+1 and finite local residues. Retains the original index supplier instead of treating this conclusion as construction of ChIdx.Ok.'),
cl('TL4','Zero-step freeness and exact twist class bijections',
   'The literal large auxiliary prime bound 2fk<g0−1 and unipotent zero level imply trivial stabilizers. All twist-zero classes identify by forgetting/adding full local frames, with literally equal preferred decorations. The reference xi is one; finite xi give rho/rho-prime norm one, completing chain validity and DG divisibility.',
   ['TL2','TL3'], [CORE, 'The supplied base prime bound and zero_uniq/zero_G/zero_Q clauses are used exactly.'],
   ss(I+'StepAtZeroFree.lean','frm_free_zero stepAt_zero_free')+
   ss(I+'StepZeroClassesBijectiveSameDeco.lean','levelTypePrimes_stepZero_eq_colLev chartIndexLevelTwistPrimes_stepZero_eq_top stepZero_chartIndex_subsingleton bij0 stepZero_representative_deco_eq_canonical stepZero_corresponding_representatives_same_deco stepZero_classes_bijective_same_deco')+
   ss(I+'TrueColumnChainsSatisfyConditions.lean','xi_unitary stp_zero_free chIn_ok idx0 rep_L_lattice ok_chains')+
   ss(A+'TrueColumnChoicesHeckeCharReferenceEqOne.lean','trueColumnChoices_heckeChar_reference_eq_one')+
   ss(A+'PredMemGamRanks.lean','ChainIn.Ok'),
   'Supplies a finite-order plus local-unipotence proof with the exact cyclotomic degree bound; does not use the inherited conditional CR4/Forms0 endpoint.'),
cl('TL5','Exact integral coefficient covariance and pairing invariance',
   'From generic GStep.Ok and FOk derive the actual GFam.Ok: Nabla and Delta transport exactly under inverse-transpose dual frames and the character scalar, and the normalized tensor Fock form is invariant.',
   [], [GEN],
   ss(I+'HermitianLatticeChartFamilyFamOk.lean','GStep.lsh_eq_map GStep.tauLat_smul fam_ok')+
   ss(A+'PredMemGamRanks.lean','FOk GStep.rho GStep.fam'),
   'Expands lattice, polynomial generator and root-of-unity unit arguments. The final FC7/FC19 record is not a premise.'),
cl('TL6','Fixed-vector scalar extension and the actual complex basis',
   'Evaluation after scalar extension identifies the defined complex polynomial value space, and finite stabilizer averaging commutes with that extension. The actual rational forms basis evaluates to a complex Fi basis, and Fi is finite dimensional.',
   ['TL5'], [GEN, 'Averaging divides by stabilizer orders only in the characteristic-zero field.'],
   ss(I+'HermitianLatticeChartFamilyLawBasis.lean','li_pi_of_basis mem_span_basis_image rho_sum_translates evV_rho_eq_tr lawBasis_of_ok lawBasis_all')+
   ss(I+'ComplexFormsFiniteDimensional.lean','valC_finiteDimensional GStep.fi_finiteDimensional')+
   ss(A+'PredMemGamRanks.lean','GStep.Fi GStep.FormsK GStep.embF'),
   'Proves independence by an embedded left inverse and spanning by explicit finite projectors; no integral averaging or unexplained value-space surjectivity is assumed.'),
cl('TL7','Full integral forms lattices and all-place class-sum metric',
   'The actual integral forms module is finitely generated and spans over K. Representation coefficients descend to cmMax, the chosen CSD basis lies there, and its class-sum Gram is positive at every embedding. At the distinguished embedding it equals the correctly normalized Fock class sum, proving LawGood and LawNorm.',
   ['TL5','TL6'], [GEN, 'Only the actual chosen cmMax basis is used for all-embedding conjugation compatibility; an arbitrary K-basis is not substituted.'],
   ss(I+'WeightLawGoodOfFieldEmbedding.lean','map_mulVec_injective gram_map exists_val_ne gram_posDef values_isLattice root_mem_cmMax rho_rat hasRatBasis gramV_posDef step_gram_posDef delAtr_isLattice lawGood')+
   ss(S+'HasRatBasisOfAct.lean','hasRatBasis_of_act')+
   ss(F+'Divisibility/ClassSum.lean','CSD.HasRatBasis CSD.basis CSD.Rat')+
   ss(I+'LawNormClassSumFock.lean','classSum_gram_posDef majAt_stdFrame_classSum map_pairVr_one GStep.lawNorm'),
   'Reconstructs the generic metric argument independently of conditional FC7. Keeps squared highest-vector norms and the sigma/conjugate infinite-place convention exact.'),
cl('TL8','Residue ranks, nonzero functional/vector and dilation laws',
   'Every full rank-n lattice has residue quotient dimension n. TDat.Ok gives the exact nonzero quotient functional and class of Te. Dilation preserves stabilizer cardinality and yields the literal f_new=a f_old composed with the induced quotient isomorphism. All TDat.Laws follow.',
   [], ['Generic TDat.Ok and the stated underlying group action are supplied. Actual TDat.Ok is proved independently in TL11.'],
   ss(I+'PrimeLevelStructureDataRanksModPrime.lean','finrank_red ranks')+
   ss(I+'LevelFunctionalLevelVectorLaws.lean','exists_fv fv_mk fv_ne_zero exists_f_eq_one te_ne_zero fv_te_laws')+
   ss(I+'DiamondActionOnHermitianChartClasses.lean','dia_inj stab_dia card_stab_cl diamond_action_on_classes')+
   ss(I+'LevelFunctionalDilatedClass.lean','exists_red_equiv exists_act_equiv dil_fv')+
   ss(I+'LawsOfOkAlt.lean','TDat.laws_of_ok')+
   ss(A+'PredMemGamRanks.lean','TDat.Ok TDat.Laws'),
   'Proves the natural localization/quotient isomorphism and the exact factor direction, rather than merely comparing dimensions.'),
cl('TL9','The diamond representation preserves complex and integral forms',
   'Freeness of the zero-step action gives unique move elements and a genuine diamond representation. Coefficient covariance and unchanged Lsh give an integral rational witness for the diamond-transformed evaluated form, proving dia_lat and complex stability.',
   ['TL5','TL6'], [GEN, 'The zero-step action is free, as required by generic AtIn.Ok and supplied for actual data by TL4.'],
   ss(I+'LevelPrimeDiamondRepresentation.lean','mv_smul_eq mv_rp evPt evPt_smul evPt_rep evPt_diaLin lawDiaOne lawDiaMul diamond_rep')+
   ss(I+'LevelPrimeDiamondPreservesComplexForms.lean','tr_mem mem_Fi lawDiaStable')+
   ss(I+'LevelPrimeDiamondPreservesIntegralForms.lean','exists_pull dia_lat'),
   'Constructs the actual rational integral form values using the same unique move matrices; integral stability is stronger than scalar-extension stability and is proved separately.'),
cl('TL10','All-place B_span and the full generic laws_all theorem',
   'For every step, selected prime and coefficient place, locW(BLat) spans the rational form space. Under exactly generic FOk, ChainIn.Ok, AtIn.Ok and PerIn.Ok, derive every AtIn.Laws and FmLaws field for chain and terminal weights.',
   ['TL5','TL6','TL7','TL8','TL9'], [GEN],
   ss(I+'LocalLatticeSpanAtPlace.lean','exists_smul_mem span_locW_eq_top exists_smul_mem_latOf span_locW_BLat')+
   ss(I+'LawsAll.lean','laws_all')+
   ss(A+'PredMemGamRanks.lean','AtIn.Laws FmLaws'),
   'The full finite-class denominator argument supplies B_span at every place. No seen-place filter, terminal incidence or value-comparison premise is inserted.'),
cl('TL11','Actual level data satisfy every Ok and Tied clause',
   'From literal TC.Ok/base prime data derive exact down/up local lattice tables, the actual nonzero Te class and the denominator formula for the down functional. Prove every TDat.Ok/Tied clause including raw point/coupling equivariance and inverse identities, then actual atIn.Ok for all words/twists.',
   ['NB1','TL4'], [CORE, 'Only primitive NB1 is used; raw up/down and selected-prime facts are reproved here instead of invoking NB2/3 or FC1 under their inherited conditional Laws hypotheses.'],
   ss(A+'PredMemGamRanks.lean','TDat.Ok TDat.Tied TDat.extF AtIn.Ok')+
   ss(A+'ExtUHInjective.lean','tdatY_ok dn_ok_of_res mv_up mv_dn tdatY_tied ysAt_off tdatAt_ok tdatAt_tied')+
   ss(C+'DecoFin.lean','dnN_spec upN_spec Deco.Ok.L_lattice Deco.Ok.Lsh_lattice Deco.Ok.dnN_up Deco.up_congr T_unif')+
   ss(I+'LevelPrimeDataOkOfTrueColumnChoices.lean','ok_reRep tied_reRep atIn_ok'),
   'Includes literal f-minus(y)=rho(s)^−1 g([sy]), down-after-up verification, away-from-pair frame/coupling preservation and exact integer T uniformizer. No chart naturality endpoint is used.'),
cl('TL12','Actual period Ok and Over from block extension',
   'From TC.Ok construct actual row GStep.Ok and prove every perIn.Ok/Over field: injective block extension, character equality, exact N/L/Lsh extension with denominator bar(pi), preferred image representative, full H, norm_tz and exact residue functional.',
   ['TL2','TL3'], [CORE],
   ss(A+'PredMemGamRanks.lean','PerIn PerIn.Ok PerIn.Over')+
   ss(A+'CardStabilizerForgetFr.lean','unitOf_val tilFr tilFr_fits tilFr_eq tilFr_fr tilFr_smul levQX levQX_finiteIndex levQX_root stepX tilF tilF_fr tilF_smul')+
   ss(A+'CongruenceLevelEqDepthSucc.lean','levCong_lam_extI topLev_pref_m extTop extTop_injective chr_extTop tilF_extTop')+
   ss(A+'ExtUHInjective.lean','iniH_extUH extUH_last extUH_injective Lsh_empty tilH_N tilH_f tilH_Lsh')+
   ss(I+'TrueColumnsPeriodMapDatumOkAndOverLevelPrime.lean','piT_notMem_Q til_deco pref_m stX_ok perIn_ok perIn_over perIn_laws'),
   'Independent of TG. Proves rep_til only for representatives of image orbits, preserves the specified row/top characters, and keeps N, L and Lsh distinct.'),
cl('TL13','Complete laws_of_ok with exact universal quantifiers',
   'For every Base B, PreX X and I:TC B X, literal I.Ok implies I.Laws. All eleven fields are supplied, universally in words, character indices, steps/classes and all coefficient places for B_span. No Pins/Later or terminal comparison premise is used.',
   ['TL3','TL4','TL10','TL11','TL12'], [CORE],
   ss(I+'LawsOfOk.lean','laws_of_ok')+
   ss(I+'BaseFieldsPrimesOk.lean','base_fOk base_fields_primes_ok')+
   ss(A+'LatAtLattice.lean','Laws chIn atIn perIn')+
   ss(A+'TrueColumnChoicesHeckeCharReferenceEqOne.lean','ColIn.Ok'),
   'Closes the actual Laws supplier from Ok by the preceding substantive human proofs. Does not assert Ok exists or mutate any inherited conditional claim.'),
cl('TL14','Uniform number field for normalized frame character values',
   'For a CM Hecke character with n_tau−r even, one number field contains every unramified normalized value xi(P)Norm(P)^(-r/2). Finite local roots plus class-group representatives and the exact product formula prove uniformity. Apply to all five actual frame character families and take one finite Galois field.',
   [], ['The actual continuous Hecke characters and their stated infinity types/parity are supplied. The arithmetic argument for finite class group and local conductor images is given.'],
   ss(I+'AlgebraicHeckeCharValuesInNumberField.lean','prod_rule_two locK_pow absNorm_eq valTw_two_mem exists_base_field exists_span_eq values_in_numberField')+
   ss(I+'HeckeCharacterUnramifiedAeAndExistsLevelStatement.lean','heckeCharacter_unramified_ae_and_exists_level','source_topological_conductor_counterpart_reconstructed')+
   ss(I+'ExistsGaloisGe.lean','exists_galois_ge exists_roots exists_of_order exists_of_emb frame_values'),
   'Closes the genuine frame_values supplier rather than retaining it as an unexplained number-field assertion; all normalized exponents and the finite representative argument are explicit.'),
cl('TL15','Construct finite residue characters and unique tuple readings',
   'Finite order and finite ramification give finite algebraic Holds generators. Explicit primitive additive/multiplicative lifts give actual Chars.Ok/Tied/WeilTied; tameness fixes their local identities. Finite-order Hecke characters with IsTwist and values in sigma(K) correspond uniquely to the actual tuples and Reads identities.',
   ['TL14'], ['The supplied frame character properties, prime-field orientations, unit xi0, size bound 2m<g_i−1, coefficient root containment, and literal IsTwist conditions are retained.'],
   ss(I+'ExistsColumnInputAssembled.lean','root_mem isAlgebraic_exp Holds exists_holds_one exists_holds')+
   ss(I+'LocalAdditiveCharApply.lean','red_same trueChars local_additive_char_apply chi_apply trueChars_ok trueChars_weil trueChars_tied exists_trueChars')+
   ss(I+'ContinuousOfCongSet.lean','exists_reads map_finPartI exists_read map_toIdl_eq_one exists_congN map_wildAt map_inertAt map_idF exists_reads_tup')+
   ss(A+'IsRationalUnitaryDeterminantMapRationalUnitaryTo.lean','IsTwist HFrame'),
   'Proves finite-field formulas and continuity/density descent, including uniqueness/reference character, and does not assert all powered chi_j are primitive.'),
cl('TL16','Auxiliary orientation and the quotient part of Pins',
   'Conjugate an integral quadratic-field norm-g factor if needed to orient its conjugate ideal at the prescribed prime. Under Ctx.Over replace piT by the context factors to obtain c(u)piT(u)=piT(u0), preserving auxiliary orientation. Pins is then supplied under the original explicit iX frame inclusion antecedent.',
   [], ['Nonempty PreX and the actual prescribed auxiliary PiBar are supplied. Ctx.Over supplies the context type factors. Pins.iX is an explicit antecedent, not proved for arbitrary supplied frames.'],
   ss(I+'ExistsColumnInputAssembled.lean','isMaximal_span exists_orient Oriented exists_oriented')+
   ss(I+'EvLgCanonical.lean','exists_quot')+
   ss(A+'LatAtLattice.lean','Pins')+
   ss(A+'CmQuadraticFormEqAlternatingForm.lean','Ctx.Over'),
   'Proves the orientation and exact quotient cancellation without new ideal choices affecting the retained characters.'),
cl('TL17','Finite principalization and exact remaining period-field inputs',
   'Finite families of fractional ideals become principal over a finite algebraic extension by adjoining class-group roots; flat coordinate sections give algebraic cD. The actual period lines are conjugates of bar(b). This gives FieldOK once the CM j-value algebraicity is supplied; the separate period/trace-isometry ambient datum remains explicit.',
   ['TL14'], ['CM j-value algebraicity/integrality is retained as a primitive modular input. The full AmbIn period pair, quadratic trace isometry/complex extension and local correction supplier is not reconstructed here.'],
   ss(I+'CmInverseHalfDifferentMulRelativeDifferent.lean','ideal_eq_of_pow_eq exists_pow_eq_span span_root cmInverseHalfDifferent_mul_relativeDifferent ellLat_eq exists_fieldOK')+
   ss(I+'CmInverseHalfDifferentMulRelativeDifferent.lean','isIntegral_jLat','retained_source_input')+
   ss(I+'ExistsIntMulMemInvHalfDifferent.lean','ellE ellE_fg exists_dgen')+
   ss(I+'ExistsIntMulMemInvHalfDifferent.lean','nonempty_kapIn exists_ambIn_ok','retained_source_input'),
   'Proves the finite principalization and flat-base-change part, explicitly separating the analytic CM j theorem and ambient trace-isometry construction.',True),
cl('TL18','Four-copy derivative and finite theta-translation reductions',
   'Derivative-closed algebraic germ algebras and the four-copy identity imply algebraicity of every derivative even when f(0)=0. Algebraic linear substitution, rational Heisenberg phases and finite algebraic intertwiner/indicator sums transport this to normalized JetAlg under the listed primitive theta identities and smoothness.',
   [], ['The normalized CM theta Taylor/torsion-translation theorems, actual four-copy/vacuum identity and normalized indicator presentation are supplied primitive inputs, not conclusions proved here.'],
   ss(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','Cl.contDiff Cl.val_mem Cl.deriv Cl.iterated_mem Root4.val_mem Root4.deriv alg_of_span kappa_mem thZero_coefIn TA.comb TA.transl TA.iop ta_thMoved derivAt0_mul esmooth_jetAlg')+
   ss(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','thetaVector_fourthPower_algebraicGerm','retained_primitive_identity_boundary_with_closure_steps_reconstructed')+
   ss(D+'Proofs/FoundationProofs/AlgebraicTaylorTorsionTranslateEvenTheta.lean','algebraicTaylor_torsionTranslate_evenTheta_alt','retained_source_input')+
   ss(D+'Proofs/FoundationProofs/CmThetaTaylorCoeffAlgebraicAndConjugate.lean','cmTheta_taylorCoeff_algebraic_and_conjugate','retained_source_input'),
   'Reconstructs the algebraic closure and transport mechanism; does not identify a formal finite sum with the actual analytic theta family without the retained identities.',True),
cl('TL19','Finite algebraic generators for all actual bounded-degree jets',
   'Under actual JetAlg, smoothness, covariance and normalization-character laws with algebraic cD, reduce all selfdual lattice pairs and bounded rational shifts to finite representatives and use chain rule to prove FinAlg(jetSet). The exact canonical modulus and finite bad-prime sets give allSet and JetsIn once the generators are present.',
   ['TL1','TL2','TL17','TL18'], ['The actual normalized-family unitary covariance/character identities are supplied; primitive theta hypotheses of TL18 remain. Actual step membership in allSet is proved using these hypotheses, not inferred from the FinAlg predicate in its definition.'],
   ss(I+'FinAlgOfFinite.lean','FinAlg finAlg_biUnion jetSet JetAlg VacEq')+
   ss(I+'FinAlgJetSet.lean','finAlg_range thInd_congr finite_thInd finAlg_jetSet')+
   ss(I+'DerivAt0CompMem.lean','derivAt0_comp_mem')+
   ss(I+'DegreeEqTotDeg.lean','totDeg degree_eq_totDeg badP badPrimes_finite₂ rowSG_subset Sb_subset finAlg_step')+
   ss(I+'EvLgCanonical.lean','stepSet allSet finAlg_allSet gens gens_algebraic allSet_subset jetsIn_of_isTw lg_gens'),
   'Proves finite generation conditional on analytic algebraicity and exact transformation identities; does not close those identities by the finite-union definition.',True),
cl('TL20','Local index selection reduction and canonical root extraction',
   'Finite double-coset representative selection and character descent yield the index construction under actual local normal-form/nonvanishing inputs. From supplied Ok+Deep extract sqrt(q), mu(q)^−1 and the primitive q^(2m) root by the Weil formula. Canonical replacement is definitionally IsTw but preserves Ok only under the retained twisted-unfolding and character-nonvanishing suppliers.',
   ['TL15'], ['Initial admitted-coset finiteness/normal forms, first-unfolding nonvanishing transfer and kernel-character triviality remain local inputs. Canonical TwistedEisenstein double-coset and character nonvanishing remain retained.'],
   ss(I+'NotMemVGsOfMemQE.lean','exists_step exists_sets exists_chIdx_of_cst exists_chIdx','conditional_index_selection_counterpart')+
   ss(A+'IsTwIffCanonEq.lean','IsTw canon canon_isTw Deep qOf_mod_four val_of_ok Q_notMem_of_ok degOne_of_ok sqrt_of_ok root_of_ok twIdx_ok_of_ok canon_ok')+
   ss(C+'UnfoldingNonvanishingDoubleCosetHolds.lean','firstUnfolding_eq_doubleCosetDatum doubleCosetDatum_hypotheses unfoldingNonvanishingDoubleCoset_holds twIdx_ok_closed','retained_source_input')+
   ss(C+'ChainTwFinal.lean','characterNonvanishing_holds','retained_source_input')+
   ss(PI+'OrbitalBoundsConclusion/TwistedEisensteinNonvanishing.lean','TwistedEisensteinNonvanishing','retained_source_input')+
   ss(PI+'UnitaryGroupMassFormula/TwistedEisensteinCoset/TwistedEisensteinOfRemaining.lean','twisted_eisenstein_of_remaining','retained_source_input'),
   'Separates elementary finite selection/root extraction from the source nonvanishing theorem. No unconditional canonical Ok conclusion is asserted.',True),
cl('TL21','Exact EvLg assembly with the retained supplier boundary',
   'Under the retained period/trace-isometry, CM j, local-index/nonvanishing and primitive normalized-theta inputs, construct the finite large_2 generator requirements and the actual canonical TC with Ok, Pins under iX, IsTw, JetsIn, prescribed selector/frame/excluded set/character range, all-assembly ValLL0 and FieldOK; TL13 then supplies Laws. The outer Ev quantifiers may have trivial thresholds because the inner statement holds for every context. No Later existence is inferred.',
   ['TL13','TL14','TL15','TL16','TL17','TL18','TL19','TL20'], ['All explicit primitive suppliers retained in TL17–TL20 are assumed. Nonempty PreX and literal frame inclusion remain antecedents. The large_2 fixed/full coefficient-field generator containment and Ctx.Over relation remain exact.'],
   ss(I+'EvLgCanonical.lean','evLg_canonical')+
   ss(I+'ExistsColumnInputAssembled.lean','exists_colIn isTwist_of_mem_set of_over lg_colIn ev_of_forall')+
   ss(A+'CmQuadraticFormEqAlternatingForm.lean','Ev Has₂ TwDat TwDat.xiTw TwDat.set large₂ EvLg')+
   ss(A+'LatAtLattice.lean','Later','separate_stage_record_not_constructed'),
   'A proved conditional assembly with exact quantifier order. It closes Laws and finite generator/read/orientation steps, while expressly retaining primitive Ok suppliers and Later/host existence.',True)
]


targets = []
def target(path, name, group, scope, connections):
    t=source(path,name,'remaining_human_reconstruction_target')
    t.update(priority_group=group, remaining_human_scope=scope, source_connections=connections,
             human_status='continuation_target_only; primitive supplier not claimed proved in TL')
    targets.append(t)

target(I+'NotMemVGsOfMemQE.lean','exists_step',1,
       'Prove the actual admitted-level finite coset theorem and normalized representative transfer preserving FiniteSumNonzeroLargeDepth. TL20 already supplies finite recursive selection once these exact local hypotheses hold.',
       ['admissibleRepresentatives_finite_level_cosets','latticeNormalForm_modulo_unipotentSemidirect','first_unipotent_class_transfer','TL20'])
target(I+'NotMemVGsOfMemQE.lean','exists_chIdx_of_cst',1,
       'Complete the local kernel-character/nonvanishing and level-character descent suppliers after the finite representative family. The finite products and record-field assembly are already reconstructed conditionally in TL20/TL21.',
       ['exists_step','exists_sets','exists_locCst','TL20','TL21'])
target(PI+'UnitaryGroupMassFormula/TwistedEisensteinCoset/TwistedEisensteinOfRemaining.lean','twisted_eisenstein_of_remaining',1,
       'Reconstruct the actual affine change-of-variables, Jacobian, bounded-character and free-coordinate identities proving the twisted first-unfolding/double-coset nonvanishing theorem. Canonical roots/depth arithmetic are already proved in TL20.',
       ['TwistedEisensteinNonvanishing','twIdx_ok_closed','characterNonvanishing_holds','TL20'])
target(C+'ChainTwFinal.lean','characterNonvanishing_holds',1,
       'Reconstruct actual canonical projected-kernel character nonvanishing/triviality. It must be combined with the twisted unfolding supplier to preserve Ok under canon; root containment alone is insufficient.',
       ['twIdx_ok_closed','canon_ok','TL20'])
target(I+'ExistsIntMulMemInvHalfDifferent.lean','exists_ambIn_ok',2,
       'Construct the actual period pair, rational quadratic trace isometry and complex extension, plus local correction data used in the AmbIn carrier. TL17 already proves the finite ideal-principalization/derivative-generator part.',
       ['exists_periodPair_lattice_eq_lamOf','nonempty_isoK','exists_complexLinear_extension_of_traceIsometry','nonempty_kapIn','TL17'])
target(I+'CmInverseHalfDifferentMulRelativeDifferent.lean','isIntegral_jLat',2,
       'Prove the CM period-lattice j-value algebraicity/integrality from the actual modular-polynomial/lattice identities. TL17 already gives simultaneous period-ideal principalization and FieldOK once this value is algebraic.',
       ['isIntegral_modularJ_of_ringOfIntegers','exists_periodPair_baseLat','TL17'])
target(D+'Proofs/FoundationProofs/CmThetaTaylorCoeffAlgebraicAndConjugate.lean','cmTheta_taylorCoeff_algebraic_and_conjugate',3,
       'Reconstruct primitive normalized CM theta Taylor algebraicity, with the actual period/normalization and rational-torsion domain. TL18 already proves the derivative-closed germ and four-copy root argument.',
       ['algebraicTaylor_torsionTranslate_evenTheta_alt','coefIn_translate','TL18'])
target(D+'Proofs/FoundationProofs/AlgebraicTaylorTorsionTranslateEvenTheta.lean','algebraicTaylor_torsionTranslate_evenTheta_alt',3,
       'Supply the precise torsion-translation/entirety identity for the normalized even theta germ. TL18 handles algebraic closure and finite transport after this primitive theorem.',
       ['thetaVector_fourthPower_algebraicGerm','TL18'])
target(I+'VacuumEntireAndNormalizedJetsAlgebraic.lean','thetaVector_fourthPower_algebraicGerm',3,
       'Verify the actual four-copy vacuum identity and algebraic substitution/normalization inputs against the primitive theta theorem. The purely derivative-algebra/fourth-root implication is already proved in TL18.',
       ['WeilVac.thMM_spec','FourthRootStd.stdOK','ColNorms.IndPres.pres_thInd','TL18'])
target(I+'DegreeEqTotDeg.lean','finAlg_step',3,
       'Supply the actual normalized-family unitary covariance/character identity and normalized indicator presentation, plus the remaining primitive theta/ambient inputs. TL19 already proves finite representative/chain-rule FinAlg reduction and exact canonical allSet membership once these inputs hold.',
       ['normalisedFamily_satisfies_equivarianceLaws','vacuum_entire_and_normalizedJets_algebraic','TL18','TL19'])

out=dict(schema_version='1.3',artifact_version='0.15',date='2026-11-22',owner='/root/global_frame',
    repository=dict(url=URL,commit=PIN),
    range_convention='One-indexed inclusive; exact original declaration bytes, without newline or Unicode normalization.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
        replacement_arguments_formalized=False,pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Complete human proof of the precisely stated supplied-data assertion or conditional reduction; retained source inputs are explicitly labeled and are not claimed proved.'),
    claims=claims,files=[files[p] for p in sorted(files)],
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    prior_components_reused=['NB1','LP1'],same_iteration_companions=['TG','SZ'],independent_reviews=[],
    scope='TL1–TL13 derive actual TC.Laws from literal TC.Ok independently of final Forms0/terminal comparisons. TL14–TL16 close frame fields/characters/readings/orientation and Pins.cof. TL17–TL21 prove explicit finite/principalization/derivative/index reductions and conditional EvLg assembly retaining the exact primitive local and analytic suppliers. No host, full unconditional Ok, arbitrary Pins.iX, Later or RH/GRH existence is asserted.',
    boundary_resolved=['LawsAll.laws_all under its literal generic hypotheses','LawsOfOk.laws_of_ok from literal TC.Ok','TrueColumnChainsSatisfyConditions actual finite step/chain supplier','LevelPrimeDataOkOfTrueColumnChoices actual level supplier','TrueColumnsPeriodMapDatumOkAndOverLevelPrime actual period supplier','ExistsGaloisGe.frame_values uniform number field','LocalAdditiveCharApply trueChars from frame/root data','ContinuousOfCongSet exists_reads_tup under literal IsTwist/value-range conditions','ExistsColumnInputAssembled finite Holds and orientation','EvLgCanonical exists_quot Pins.cof under Over','Finite principalization and bounded-jet finite-generation reductions'],
    retained_inputs=[CM,CORE,BOUND,'Initial/canonical local index and first-unfolding/kernel-character nonvanishing suppliers','Actual period pair and quadratic trace-isometry/local-correction AmbIn supplier','CM j algebraicity and primitive normalized CM theta Taylor/translation/four-copy/indicator and covariance identities','Original Pins.iX frame inclusion antecedent; nonempty PreX and exact Ctx.Over and large_2 field containments'],
    dependency_precision=['TL core does not depend on FC19, TG, supplied Laws or Later.','TL11 uses primitive NB1 only; the necessary up/down and prime tables are reproved to avoid inherited NB2/FC1 Laws dependencies.','Inherited claims and their hypotheses/edges remain unchanged; new TL13 supplies their Laws premise prospectively.','TL17–TL21 are conditional reductions, not assertions that retained analytic/local-index suppliers have been proved.'])

for filename, who, ids in [('tg_reviews_tl11_12.txt','/root/comparison_span',['TL11','TL12'])]:
    review=HERE.parent/'reviews_v0_15'/filename
    if review.exists():
        rt=review.read_text(); rr=review.read_bytes(); main=(HERE/'main.tex').read_bytes(); hashes={}
        for ident in ids:
            i=int(ident[2:]); start=main.index(f'\\paragraph{{{ident}:'.encode())
            stop=main.index(f'\\paragraph{{TL{i+1}:'.encode(),start+1)
            sha=digest(main[start:stop]); assert sha in rt,('independent review paragraph changed',ident,sha)
            hashes[ident]=sha
        out['independent_reviews'].append(dict(reviewer=who,result='PASS',claim_ids=ids,
             review_record='../reviews_v0_15/'+filename,review_record_sha256=digest(rr),paragraph_sha256=hashes,lean_replay=False))

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
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.15',commit=PIN,targets=targets,
    closed_source_targets=[dict(path=I+'LawsOfOk.lean',declaration='GlobalTheory.Mem.Col2.TC.laws_of_ok',closed_by=['TL1','TL2','TL3','TL4','TL10','TL11','TL12','TL13']),
        dict(path=I+'LawsAll.lean',declaration='GlobalTheory.Mem.Col2.laws_all',closed_by=['TL5','TL6','TL7','TL8','TL9','TL10']),
        dict(path=I+'ExistsGaloisGe.lean',declaration='GlobalTheory.Mem.FrameVal.frame_values',closed_by=['TL14'])],
    partially_reconstructed_targets=[dict(path=I+'EvLgCanonical.lean',declaration='GlobalTheory.Mem.Col2.TwIdxEx.evLg_canonical',proved_reductions=['TL14','TL15','TL16','TL17','TL18','TL19','TL20','TL21'],remaining='The explicit local-index, period/trace-isometry, CM j and primitive theta/covariance suppliers in targets remain; no Later or primitive host construction is asserted.')],
    remaining_boundary='Laws is closed under literal Ok. Ok existence still requires the precise local and analytic suppliers listed here; Pins.iX and nonempty PreX remain the original antecedents, and Later/host existence is separate.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),next_targets=len(targets),verified_equal_to_pinned_git_blob=True,artifact_sha256=out['artifact_sha256'])))


