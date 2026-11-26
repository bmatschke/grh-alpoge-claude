#!/usr/bin/env python3
"""Bind IX1--IX10 and the explicitly retained image-density frontier."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
REPO = parser.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
SG = AV + 'SymplecticGSp4/'
WS = AV + 'WeakShimuraTheory/'
WP = WS + 'PolynomialTori/'
WC = WS + 'CompactIntegralFields/'
BM = WS + 'BlockMatrixPlaces/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
CT = AV + 'ModularityArgument/CuspidalTwists/'
FGR = 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}


def source(path, name, role='Exact pinned definition or proof in the stated IX scope'):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if m:
            starts.append((n, m.group(1)))
    matches = [(n, s) for n, s in starts if s == name or (name.startswith('@') and s.rsplit('.', 1)[-1] == name[1:])]
    if len(matches) != 1:
        raise ValueError((path, name, matches))
    start, spelling = matches[0]
    end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b''.join(lines[start - 1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw), 'lines': len(lines),
                   'url': f'{URL}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{URL}/blob/{PIN}/{path}#L{start}-L{end}', 'role': role,
            'verified_equal_to_pinned_git_blob': True}


spec = {
 'IX1': {
  SG+'DecompSigmaOrd.lean': ['OnComp', 'IsPt', 'PtIn', 'Fin0'],
  WP+'UnivOf.lean': ['@univOf'], WP+'UnivGr.lean': ['@univGr'],
  WP+'PtClosed.lean': ['@ptClosed'],
  WP+'ClosedOfSet.lean': ['closedL', 'closedP', 'compL', 'compP'],
  WP+'OnCompClosed.lean': ['@onCompClosed'],
 },
 'IX2': {
  WS+'NearSplit.lean': ['Amb', 'IsZero', 'IsDvr', 'Small', 'KPair', 'VPt'],
  WC+'PtPair.lean': ['@ptPair'],
  SG+'DecompSigmaOrd.lean': ['condL', 'OnComp', 'EPt'],
 },
 'IX3': {
  WC+'PtOver.lean': ['@ptOver'], WP+'DimOne.lean': ['@dimOne'],
  WP+'PsFinEv.lean': ['@psFin'], WP+'AmbPt.lean': ['@ambPt'],
  WP+'MonoMem.lean': ['mono_mem', 'mono_max', 'factor', '@ptA'],
  WP+'NonAlg.lean': ['@nonAlg'], WP+'ZmPow.lean': ['@zMono'],
  WS+'NearSplit.lean': ['Amb', 'IsDvr', 'Small', 'VPt'],
 },
 'IX4': {
  WC+'CobOfCoord.lean': ['tri_comb', 'cob_of_coord', 'lattice', 'line', 'locVan', 'core', '@triV'],
  WC+'BlockPart.lean': ['bp', 'bp_mul', 'gsp_bp', 'flag_bp', 'span_bp', '@blockPart'],
  WC+'DiagConst.lean': ['exists_form', 'mono_fin', 'unip', 'dchar', 'mink', 'diag_fin', '@diagConst'],
  WS+'NearSplit.lean': ['KPair', 'VPt'],
 },
 'IX5': {
  BM+'BlockDiagonalOrdinaryGSpRep.lean': ['IsZ', 'Zc', 'Prim', 'Lat', 'IsZT', 'Pos'],
  BM+'GwIneq.lean': ['@gwIneq'], BM+'GwCount.lean': ['@gwCount'],
  BM+'PlusCard.lean': ['@plusCard'], BM+'UrCard.lean': ['@urCard'],
  BM+'SelToZc.lean': ['exists_norm', '@selToZc'],
  BM+'CocT.lean': ['@cocT'], BM+'PrimEx.lean': ['@primEx'],
  BM+'DivStep.lean': ['mem_of_bij', '@divStep'],
  BM+'Compat.lean': ['seq_ex', '@compat'],
  BM+'IsPrecompleteFinite.lean': ['lift_seq', '@limit'],
 },
 'IX6': {
  BM+'BlockDiagonalOrdinaryGSpRep.lean': ['hAB', 'uM', 'uPlus', 'eAB', 'Sep', 'BlockDiagonalOrdinaryGSpRep'],
  BM+'FlagVec.lean': ['cols', 'entries_one_three_zero_eq_zero_of_intertwine_up', '@flagVec'],
  BM+'ResEntry.lean': ['@adBij'], BM+'UpSupUp.lean': ['@latU'],
  BM+'TwistMul.lean': ['ac_mul', 'twist_mul', '@cocA'],
  BM+'NoCompl.lean': ['key', '@noCompl'],
  BM+'AdjointBlockSubmatrixEq.lean': ['adjoint_block_submatrix_eq', '@spanB'],
  WC+'NotOver.lean': ['@bl'], WS+'RedIdeal.lean': ['BlockExt', 'Star'],
  WS+'NearSplit.lean': ['KPair'],
 },
 'IX7': {
  WC+'WtChar.lean': ['open_ker', '@wtChar'],
  WC+'BlockDet.lean': ['bd_key', '@blockDet'], WC+'FrobIn.lean': ['@frobIn'],
  FGR+'AdmissibleResidues/ArithmeticPointDecomposition.lean': ['PureW', "pureW'"],
  FGR+'AdmissibleResidues/PosOfMulPosOfPos.lean': ['cp_block', 'det_two', '@pureDet_w', '@nePure_w'],
 },
 'IX8': {
  DT+'VWinPm.lean': ['@fin0_no_end_all_irr_of_good_con_purity_aut'],
  DT+'PotentialModularityTower.lean': ['PurityAtPoints', 'AutmAlt'],
  WS+'NearSplit.lean': ['Con'], SG+'DecompSigmaOrd.lean': ['Fin0', 'NoEnd', 'AllIrr'],
  DT+'IsAut4.lean': ['IsAut4Alt', 'SymplecticFourImageDense'],
 },
 'IX9': {
  DT+'TPmFin.lean': ['pf_const', 'pf_sect', 'pf_lam', 'pf_int', 'pf_sq', 'pf_gen', 'pf_unit', 'pf_lift', 'pf_sqK', '@exists_pow_maximalIdeal_le_of_modular_phi'],
  DT+'ContradictionStarPromodular.lean': ['con_span', 'con_block', 'con_trace', 'con_kill', 'con_const', '@contradiction_star_promodular'],
  DT+'PotentialModularityTower.lean': ['PotentialModularityTower', 'ProModAlt'],
  WS+'IsAlgClosureField.lean': ['Link', 'IsPhi'], WS+'RedIdeal.lean': ['Space', 'BlockExt', 'Star'],
  AV+'WeilGroupCharacters/UniversalOrdinaryDeterminantRing.lean': ['UniversalOrdinaryDeterminantRing', 'IsInert', 'LamObj', 'LamObj.toPair', 'LamObj.toPair_spec'],
  AV+'WeilGroupCharacters/ArithmeticPointClassicality.lean': ['UniversalOrdinaryDeterminantRing.RingProps'],
  DT+'PointTheoremBaseObject.lean': ['HidaPropsAlt', 'ModularAlt', 'ModUAlt'],
 },
 'IX10': {
  DT+'CharpolyConj.lean': ['ps_wt_any', 'charpoly_conj', '@pureW_of_proModular_of_isZero'],
  DT+'MapRepComp.lean': ['irr_sub', 'cont_small', 'comm_L', 'rt_wt', 'dist_L', 'irr_L', '@aut_n_alt'],
  DT+'AutCsdIso.lean': ['autCsd_iso_alt', 'autQIsoN'],
  DT+'PotentialModularityTower.lean': ['PurityAtPoints', 'AutmAlt', 'PotentialModularityTower', 'ProModAlt'],
  WS+'NearSplit.lean': ['Tower', 'Ok', 'Wts'],
  AV+'ModularityArgument/AutomorphyLifting/IsAutCsdA.lean': ['IsAutQA'],
  DT+'IsAut4.lean': ['IsAut4Alt', 'SymplecticFourImageDense'],
 },
}

titles = {
 'IX1': 'All-target actual point universality, closed local components and full-weight-zero ring',
 'IX2': 'Ordinary flags and full small KPair matching over arbitrary valued ambients',
 'IX3': 'Actual nonconstant characteristic-ell curve from failure of Fin0',
 'IX4': 'Valued representation pattern classification, block projection and constant diagonal invariants',
 'IX5': 'Finite duality growth through primitive compatible integral cocycles',
 'IX6': 'Nonsplit same-characteristic-polynomial block extension satisfying every KPair field',
 'IX7': 'Exact strict PureW root-ratio contradiction for a block diagonal pair',
 'IX8': 'Complete Con plus PurityAtPoints plus AutmAlt to Fin0, NoEnd and common-embedding automorphy',
 'IX9': 'Finite weight module to finite fibre to residual trace and full star obstruction',
 'IX10': 'Exact ProModAlt characteristic-zero transport and uniform common-embedding endpoint',
}
deps = {
 'IX1': ['AX6', 'DX2', 'DX5', 'DX6', 'DX7', 'FP1', 'FP2', 'FP3', 'MX1', 'PX1'],
 'IX2': ['AX6', 'IX1', 'PX6'],
 'IX3': ['IX1', 'PX1', 'PX5'],
 'IX4': ['IX2', 'AX6', 'BR7', 'DX1', 'PX6'],
 'IX5': ['DX1', 'LD3', 'KB6'],
 'IX6': ['IX5', 'AX6'],
 'IX7': ['AX6'],
 'IX8': ['IX1', 'IX2', 'IX3', 'IX4', 'IX5', 'IX6', 'IX7'],
 'IX9': [],
 'IX10': ['IX8', 'IX9', 'AX6'],
}
scopes = {
 'IX1': 'For every original Good D, constructs an actual universal IsPt ring over the original O, not merely Model.S; all-target universality, entry-based homogeneous presentation and full-weight-zero complete local ring. Finite B over O implies literal Fin0.',
 'IX2': 'Every actual VPt in every Amb, including characteristic ell and arbitrary valuation ring, becomes an actual KPair with the ordered original residual labels. Every EPt becomes a small VPt in the standard IsZero ambient. Proper flag closure replaces the long source flag-specialization chain.',
 'IX3': 'Failure of literal Fin0 produces an actual small characteristic-ell VPt and a zero-weight entry monomial fixed by no positive Frobenius power. Includes complete local curve, full ambient coefficient system and continuity-respecting invariant-fibre lift.',
 'IX4': 'All actual small valued points: full span, DiagType, or same-lambda two-block triangular pattern; cross-lambda components are excluded by exact original Good.XVan with BR7. Produces full KPair for the block projection. In characteristic ell all DiagType zero-weight entry monomials are Frobenius-periodic.',
 'IX5': 'Exact complete DVR, finite-free module, odd ell, complex-conjugation action -1, local s with cyclotomic value1 and rho(s)-1 invertible, nonzero saturated local P, and original finite ramification set: finite duality yields a primitive nonzero continuous integral cocycle with the exact local and kernel-inertia conditions. All finite modules and limit passages proved explicitly.',
 'IX6': 'For every actual small block diagonal KPair whose A block spans M2, produces a new actual KPair with BlockExt over the ambient algebraically closed field and identical characteristic polynomials at every original group element. No assertion that the new pair is an EPt is made or needed.',
 'IX7': 'Every actual characteristic-zero block diagonal KPair fails literal PureW for every fixed iota. Uses exact strict p^f root-ratio inequality, multiplier/ordered flags, global finite-character argument and positive Frobenius powers; does not assume usual equal-weight purity.',
 'IX8': 'For the same original Good D and fixed iota, exact Con(D), PurityAtPoints(D,iota) and AutmAlt(D,iota) imply literal Fin0 and NoEnd and AllIrr(IsAut4Alt iota). The complete proof has no remaining CohomologyHyp or valued-point construction premise; its three arithmetic hypotheses remain unproved here.',
 'IX9': 'First closes literal TPmFin implication from actual Fit/Deep tower, Link, IsPhi0, LamObj and finite R/J0 over its weight algebra; UnramifiedInputs is unnecessary. Then an actual characteristic-ell KPair with literal ProModAlt cannot be Star, via finite special fibre, residual traces, trace-pairing nondegeneracy and squarefree block separator. Neither the finite modular quotient nor the witness is asserted to exist.',
 'IX10': 'Literal ProModAlt plus IsZero gives PureW; adding actual KPair full span gives literal IsAut4Alt, with full Clifford/self-twist/residual-independence proof of restriction irreducibility. Uniform ProModAlt realization of every actual star pair for fixed D/iota implies the same-D Fin0/NoEnd/AllIrr conclusion. Actual realization remains a retained arithmetic input.',
}

inputs = {
 'IX-C1': {'kind': 'matched classical complete local algebra', 'name': 'Noetherian formal series, complete quotients and henselian finite algebras',
  'statement_used': 'Finite formal power series over a Noetherian ring are Noetherian; quotients of a complete Noetherian local ring remain complete; a finite algebra over a henselian local ring is a finite product of local rings, so a finite domain is local.',
  'source': 'Stacks Project, tags0306,0325,04GH.',
  'urls': ['https://stacks.math.columbia.edu/tag/0306','https://stacks.math.columbia.edu/tag/0325','https://stacks.math.columbia.edu/tag/04GH'],
  'primary_source_checked': True,
  'matching': 'Used on the actual IsCO rings, the finite eigenvalue algebra C[b], and complete prime quotients. Integrality makes the origin evaluation land in O; uniqueness of the maximal ideal proves localness before reducing quotient labels. Successive approximation arguments are given directly.'},
 'IX-C2': {'kind': 'matched classical algebraic geometry', 'name': 'Proper projective flag varieties and the valuative criterion',
  'statement_used': 'A locally projective morphism is proper; a quasi-compact morphism is universally closed exactly when it satisfies the existence part of the valuative criterion.',
  'source': 'Stacks Project, Lemma29.44.5 tag01WC and Proposition26.20.6 tag01KF.',
  'urls': ['https://stacks.math.columbia.edu/tag/01WC','https://stacks.math.columbia.edu/tag/01KF'],
  'primary_source_checked': True,
  'matching': 'The symplectic flag variety is explicitly a closed incidence/isotropy subvariety of a product of Grassmannians. The schematic closure of the actual generic flag is proper and surjects the integral base. A chosen K-point then extends over the given valuation ring. This does not assume smoothness, flatness or uniqueness of flags.'},
 'IX-C3': {'kind': 'matched classical algebraic geometry', 'name': 'Weak Nullstellensatz',
  'statement_used': 'Every nonzero finite-type algebra over an algebraically closed field has a rational closed point.',
  'source': 'Stacks Project, Theorem10.34.1 tag00FV.', 'url': 'https://stacks.math.columbia.edu/tag/00FV',
  'primary_source_checked': True,
  'matching': 'Applied only to the nonzero finite-type invariant fibre. Nonzero follows from the weight-zero retraction before field extension. Full formal evaluation is justified separately using positive valuations and finite monomial decompositions.'},
 'IX-C4': {'kind': 'matched classical local fields', 'name': 'Finite extensions of complete discrete valuation fields',
  'statement_used': 'A finite separable extension of a complete discretely valued field has a unique extended valuation, is complete, and has finite valuation ring with finite residue field if the original residue field is finite.',
  'source': 'J.S.Milne, Algebraic Number Theory, v3.08, Theorems7.38--7.40; Stacks tag09E8.',
  'urls': ['https://www.jmilne.org/math/CourseNotes/ANT.pdf','https://stacks.math.columbia.edu/tag/09E8'],
  'primary_source_checked': True,
  'matching': 'Captures finitely many algebraic flag-basis entries in a single complete DVR inside the original V. Equal-characteristic purely inseparable extensions are handled separately by adjoining ell-power roots of a uniformizer over the perfect finite residue field; Milne is not misquoted as already proving that part.'},
 'IX-C5': {'kind': 'matched classical arithmetic', 'name': 'Minkowski: no nontrivial everywhere-finite-unramified extension of Q',
  'statement_used': 'A finite extension of Q unramified at every finite prime is Q.',
  'source': 'J.S.Milne, Algebraic Number Theory, v3.08, Theorem4.9, printedp72/PDFpage74.',
  'url': 'https://www.jmilne.org/math/CourseNotes/ANT.pdf', 'primary_source_checked': True,
  'matching': 'Applied to each finite continuous reduction of a powered character. The character is first shown trivial on every original inertia group, including ell. Separatedness is used only after these finite assertions. No assertion about arbitrary infinite unramified extensions is used.'},
 'IX-C6': {'kind': 'matched classical finite-dimensional representation theory', 'name': 'Density theorem over an algebraically closed field',
  'statement_used': 'The image of an algebra in the endomorphisms of a finite-dimensional simple module over an algebraically closed field is the full endomorphism algebra.',
  'source': 'P.Etingof et al., Introduction to Representation Theory, January10,2011, Theorem2.5(i), p24; Section2.5 finite-dimensional algebra proof.',
  'url': 'https://math.mit.edu/~etingof/replect.pdf', 'primary_source_checked': True,
  'matching': 'Used only to turn simplicity on G_L back into the literal matrix-span Irr predicate. The finite-index semisimplicity, self-twist construction, injective characteristic-zero transport and distinct residual-character contradiction are proved in IX10.'},
 'IX-H-CON': {'kind': 'retained arithmetic theorem hypothesis', 'name': 'Con(D)',
  'statement_used': 'For every Amb of characteristic ell and every actual KPair, its ambient-field representation is not Star.',
  'source_definition': 'WeakShimuraTheory/NearSplit.lean:Con', 'installed_here': False,
  'matching': 'IX9 proves the obstruction from an actual ProModAlt witness; it does not construct such a witness for all pairs.'},
 'IX-H-PURE': {'kind': 'retained arithmetic theorem hypothesis', 'name': 'PurityAtPoints(D,iota)',
  'statement_used': 'For every Amb/IsZero and every actual star KPair, including the nonsplit pair from IX6, literal PureW holds after the exact identification.',
  'source_definition': 'DenseThresholdCases/PotentialModularityTower.lean:PurityAtPoints', 'installed_here': False,
  'matching': 'The full original quantifiers are retained. PureW is the strict root-ratio bound, not usual equal-absolute-value purity. IX10 transports this from the actual PM.pur clause only.'},
 'IX-H-AUT': {'kind': 'retained arithmetic theorem hypothesis', 'name': 'AutmAlt(D,iota)',
  'statement_used': 'For every Amb/IsZero and every full-span actual KPair, literal IsAut4Alt/IsAutQA holds for the same fixed iota.',
  'source_definition': 'DenseThresholdCases/PotentialModularityTower.lean:AutmAlt', 'installed_here': False,
  'matching': 'Includes the exact quadratic-CM universal clause, regular algebraic cuspidal attachment and WitA. Not replaced by generic potential automorphy.'},
 'IX-H-FINMOD': {'kind': 'explicit algebraic theorem hypothesis; arithmetic realization not supplied',
  'name': 'Actual Link/IsPhi0 and finite modular quotient over LamObj',
  'statement_used': 'On the actual Fit/Deep tower, R is the universal ordinary determinant ring, Lambda its universal inertial-character algebra, R/J0 is finite over Lambda and phi:R→X.B satisfies the two literal Link.IsPhi0 equations.',
  'installed_here': False,
  'matching': 'IX9 proves every internal step to the exact maximal-ideal-power containment. The source supplies finiteness from ModularAlt.ring.fin; that arithmetic finite module and the actual link/map remain retained objects.'},
 'IX-H-PM': {'kind': 'retained actual witness hypothesis', 'name': 'ProModAlt(D,iota,ambient,r)',
  'statement_used': 'The full existential tower/coefficient/Space/J/y/r1 record, including Fit, Deep, all five PM clauses, coefficient compatibility, local base point, y(J)=0, ambient conjugacy, multiplier, restriction and exact inertia-character identities.',
  'installed_here': False,
  'matching': 'IX9/IX10 are complete consequences of this literal witness. They never infer the witness from a formal name, verified kernel background or nonempty support.'},
 'IX-H-REALIZE': {'kind': 'retained actual arithmetic supplier', 'name': 'Uniform actual star-point ProModAlt realization',
  'statement_used': 'For fixed original Good/OfCase D and one iota chosen before all point quantifiers, every actual KPair with Star in every Amb admits the full ProModAlt witness.',
  'installed_here': False,
  'matching': 'This is the still-open exact arithmetic input at IX.35. Its source producers require PMExAlt, SeedIIAlt/SeedIVAlt and the original tower/space/component-reaching chains.'},
}
uses = {
 'IX1':['IX-C1'], 'IX2':['IX-C1','IX-C2','IX-C4'],
 'IX3':['IX-C1','IX-C3','IX-C4'], 'IX4':['IX-C2','IX-C4','IX-C5'],
 'IX5':[], 'IX6':[], 'IX7':['IX-C4','IX-C5'],
 'IX8':['IX-H-CON','IX-H-PURE','IX-H-AUT'],
 'IX9':['IX-C1','IX-H-FINMOD','IX-H-PM'],
 'IX10':['IX-C6','IX-H-PM','IX-H-REALIZE'],
}

frontier_spec = {
 'IX-F1': (DT+'PotentialModularityTower.lean', ['PotentialModularityTower','PMExAlt','ProModAlt']),
 'IX-F2': (DT+'PotentialModularityTower.lean', ['IsSeedAlt','SeedPairAlt','SeedIIAlt']),
 'IX-F3': (DT+'PromodularityCaseThree.lean', ['SeedIVAlt','ChainRankFour','RankFourChainReductionDense','PromodularityCaseThreeDense','AutomorphyRankFourDense']),
 'IX-F4': (DT+'ModularityRankFourOfPromodularity.lean', ['@modularity_rank_four_of_promodularity_case_three']),
 'IX-F5': (DT+'CuFinal.lean', ['main4_alt']),
 'IX-F6': (DT+'Sp4In.lean', ['sp4In_alt']),
 'IX-F7': (DT+'Sp4In0.lean', ['sp4In0_alt']),
 'IX-F8': (DT+'PmTwo.lean', ['@promodular_existence_of_local_zero']),
 'IX-F9': (DT+'PmExTh.lean', ['@pm_exists_of_unramified_adjoint_lifting']),
 'IX-F10': (DT+'WsLink.lean', ['UnramifiedInputs']),
 'IX-F11': (DT+'PointTheoremBaseObject.lean', ['HidaPropsAlt','ModularAlt','ModUAlt']),
 'IX-F12': (DT+'AdjointLiftingOfCohomology.lean', ['adjoint_lift_of_prints','adjoint_lifting_of_cohomology','pmEx_of_printsH']),
 'IX-F13': (DT+'AfDesc.lean', ["HypothesesH'"]),
 'IX-F14': (DT+'AutomorphicFormHyp.lean', ["Hypotheses'"]),
 'IX-F15': (DT+'AutomorphicPointGalois.lean', ['AutomorphicPointGalois','AutomorphicPointLocallyGeneric','AdjointLiftingTheorem']),
 'IX-F16': (DT+'ThFinal.lean', ['core_alt_bis','adjoint_lifting_of_cohomology']),
 'IX-F17': (DT+'TOrdVan.lean', ['@ordinary_vanishing_two_of_printed_hida']),
 'IX-F18': (DT+'BcIndCs.lean', ['seedIIs_alt']),
 'IX-F19': (DT+'BirthTop.lean', ['fourth_initial_of_prints_h']),
 'IX-F20': (CT+'PromodularityCaseThree.lean', ['ExistsTensorFactorTower','RedTanA','RedA','YCoin','TorusY','FibY','Ch4','ChainDesc4','ChainIV']),
 'IX-F21': (DT+'Gsp4PromodularityCaseTwo.lean', ['last_step','@proMod_of_pmEx_of_ctx2_of_kPair_of_star']),
 'IX-F22': (DT+'PromodularityCaseThreeOfLemmas.lean', ['allIn_of_chain4','last_step','@promodularity_case_three_of_chain_reduction']),
 'IX-F23': (DT+'CuPChainIV.lean', ['@chainIV_alt']),
}

tex = (HERE / 'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid, title in titles.items():
    start = next(n for n,line in enumerate(lines,1) if line.decode().strip() == '% BEGIN '+cid)
    end = next(n for n,line in enumerate(lines,1) if line.decode().strip() == '% END '+cid)
    conditional = cid in ['IX8','IX9','IX10']
    claims.append({'id':cid,'title':title,'statement':scopes[cid],'introduced_in':'0.28',
      'depends_on':deps[cid],'input_ids':uses[cid],
      'status':'Complete human proof in the exact quantified scope; stated arithmetic hypotheses are retained' if conditional else 'Complete human proof on the stated original Good data or explicit elementary module hypotheses',
      'mathematical_status':'closed implication with retained arithmetic hypotheses' if conditional else 'closed in its exact quantified scope',
      'remaining_bespoke_inputs':[i for i in uses[cid] if i.startswith('IX-H')],
      'proof_location':{'file':'symplectic_image_density/main.tex','paragraph':cid,'line_start':start,'line_end':end,'label':'claim:'+cid,'sha256':sha(b''.join(lines[start-1:end]))},
      'sources':[source(p,n) for p,names in spec[cid].items() for n in names],
      'source_relation':'Human reconstruction with proved simplifications. Source anchors identify exact semantics and proof counterparts; they are not independent mathematical suppliers.',
      'component_ledger':'symplectic_image_density/provenance.json'})

frontier = []
for fid,(p,names) in frontier_spec.items():
    frontier.append({'id':fid,'status':'retained source producer or interface; not asserted proved here',
      'sources':[source(p,n,'Exact retained frontier definition or producer, not a promoted human supplier') for n in names]})

for path, record in files.items():
    blob = subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
    assert sha(blob) == record['sha256'], path
    record['git_blob_oid'] = subprocess.check_output(['git','-C',str(REPO),'rev-parse',PIN+':'+path],text=True).strip()
    record['verified_equal_to_pinned_git_blob'] = True

suppliers = [
 {'claims':['AX6'],'file':'symplectic_arithmetic_data/main.tex','scope':'Full actual facts for original Good D, including exact residual separation and ordinary exponents.'},
 {'claims':['DX1','DX2','DX5','DX6','DX7'],'file':'symplectic_local_installation/main.tex','scope':'Exact original finite local/global duality, PhiCond and integral local universal-ring component charts; no entire CohomologyHyp is assumed.'},
 {'claims':['BR7'],'file':'bernoulli_residual_vanishing/main.tex','scope':'Exact CorX and original residual local-to-global coboundary vanishing, including arbitrary compatible residue fields.'},
 {'claims':['FP1','FP2','FP3'],'file':'framed_deformation_presentation/main.tex','scope':'Complete local-ring maps, actual universal finite matrix lifts and formal torus/weighted presentation.'},
 {'claims':['MX1'],'file':'symplectic_model_construction/main.tex','scope':'Original quotient/descent and polynomial local-condition transport, before any model count.'},
 {'claims':['PX1','PX5','PX6'],'file':'symplectic_model_comparison/main.tex','scope':'Full-weight formal/finite monomial algebra, valuation torus rescaling and source normalization/projector/pattern comparison; IX proves all additional characteristic-ell valued-point steps.'},
 {'claims':['LD3'],'file':'local_duality_closure/main.tex','scope':'Finite normalized Poitou-Tate specialization on the actual coefficient modules.'},
 {'claims':['KB6'],'file':'k_theory_bridge/main.tex','scope':'Exact original decomposition-group/completion comparison for the finite local formulas.'},
]
for s in suppliers:
    s['file_sha256'] = sha((HERE.parent/s['file']).read_bytes())

result = {'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.28','date':'2026-11-22',
 'repository':URL,'commit':PIN,'component':'symplectic_image_density',
 'scope':'Entire lower valued-point and nonsplit-block reduction plus exact finite-weight-fibre/ProModAlt transport. Actual modular support, seeds and support-reaching remain an arithmetic frontier; literal SymplecticFourImageDense is not supplied.',
 'claims':claims,'source_files':list(files.values()),'dependency_graph':deps,'input_ledger':inputs,
 'human_suppliers':suppliers,'retained_frontier':frontier,
 'validation':{'source_files_checked_against_pinned_git_blobs':len(files),
   'claim_source_links':sum(len(c['sources']) for c in claims),
   'frontier_source_links':sum(len(f['sources']) for f in frontier),
   'main_tex_sha256':sha(tex),'human_proof_ranges':len(claims),
   'verification_kind':'Exact source/proof byte comparison and independent mathematical review; no Lean kernel replay'}}
def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
write('provenance.json',result)
write('classical_inputs.json',{'schema':'rh-classical-input-registry/1','component':'symplectic_image_density','artifact_version':'0.28','inputs':{k:v for k,v in inputs.items() if k.startswith('IX-C')}})
write('input_registry.json',{'schema':'rh-exact-input-registry/1','component':'symplectic_image_density','artifact_version':'0.28','inputs':inputs,'human_suppliers':suppliers,'scope_rule':'All arithmetic hypotheses are shown explicitly before the conditional joins. No actual ProModAlt existence, PMExAlt, seed or full ImageDense claim is inferred from a source name or prior cohomological supplier.'})
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c.get('title',c.get('status',''))+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nfile '+s['sha256']+'\nrange '+s['range_sha256'] for s in c['sources']) for c in claims+frontier)+'\n')
closure = {'schema':'rh-dependency-closure/1','artifact_version':'0.28','component':'symplectic_image_density','commit':PIN,'main_tex_sha256':sha(tex),
 'graph':deps,
 'closed_endpoints':[
  {'claim':'IX1','literal_interface':'Actual all-target IsPt universal ring, full-weight-zero B, and finite B over O implies Fin0','retained_bespoke_inputs':[]},
  {'claim':'IX2','literal_interface':'Every actual VPt becomes a KPair; every original EPt becomes a small standard-ambient VPt','retained_bespoke_inputs':[]},
  {'claim':'IX3','literal_interface':'not Fin0 implies actual characteristic-ell VPt with a zero-weight monomial fixed by no positive Frobenius power','retained_bespoke_inputs':[]},
  {'claim':'IX5','literal_interface':'Finite duality plus exact finite-free/saturated local hypotheses gives nonzero compatible primitive integral cocycle','retained_bespoke_inputs':[]},
  {'claim':'IX6','literal_interface':'Actual block diagonal KPair with full A span implies actual nonsplit BlockExt KPair with all characteristic polynomials unchanged','retained_bespoke_inputs':[]},
  {'claim':'IX7','literal_interface':'Every characteristic-zero block diagonal KPair fails literal PureW','retained_bespoke_inputs':[]},
  {'claim':'IX8','literal_interface':'Con + PurityAtPoints + AutmAlt imply Fin0 + NoEnd + AllIrr(IsAut4Alt iota) on the same D','equation':'IX.25','retained_bespoke_inputs':['IX-H-CON','IX-H-PURE','IX-H-AUT']},
  {'claim':'IX9','literal_interface':'Actual finite ordinary determinant quotient over its weight algebra plus Link.IsPhi0 implies the literal TPmFin finite-fibre containment','equation':'IX.27','retained_bespoke_inputs':['IX-H-FINMOD']},
  {'claim':'IX9','literal_interface':'Actual ProModAlt plus characteristic-ell KPair implies not Star','retained_bespoke_inputs':['IX-H-PM']},
  {'claim':'IX10','literal_interface':'Uniform actual star-point ProModAlt realization with fixed iota implies complete same-D ImageDense endpoint','equation':'IX.35','retained_bespoke_inputs':['IX-H-REALIZE']}],
 'same_object_bindings':['Original Omega, O, residue map and all compatible ambient coefficient maps','Original D.Gp/D.Ip at every place, including all-place transport by conjugacy','Ordered ordinary quotient labels and doubled T.Wts normalization','Every actual VPt/KPair field, including smallness over one complete finite-residue DVR','Original entry monomials and full formal weight-zero ring','New nonsplit pair need not be an EPt; PurityAtPoints quantifies over all KPair','Exact strict PureW inequality and positive Frobenius degree','Single iota chosen before every ambient/point quantifier','Actual Link/IsPhi equations and full ProModAlt support/conjugacy/restriction conditions'],
 'noncircularity':['The universal point ring is constructed from FP and DX local components before Fin0 is deduced.','The curve witness is an actual local point of that same universal ring; no support or automorphy is assumed.','The primitive cocycle is obtained from finite PT/Euler formulas independently of any point-count or image-density theorem.','The block twist is constructed before applying purity, and preserves all characteristic polynomials.','IX9 uses only the explicit finite module and Link equations for TPmFin; the larger unused UnramifiedInputs is not assumed.','IX10 proves restriction irreducibility from the actual tower residual separation; generic potential automorphy is not substituted.'],
 'retained_frontier':['Actual finite modular quotient/link/support producer, including all five PMExAlt clauses and its coefficient-threshold quantifiers','Exact SeedIIAlt and SeedIVAlt, with root-entry, residual, twist/parity and regular-algebraic attachment data','Original star-point to support realization: tower/space construction and case-two/case-three component chains'],
 'not_claimed':['Actual Con, PurityAtPoints or AutmAlt unconditionally','Actual ProModAlt realization for every star pair','PMExAlt or exact seed existence','Literal SymplecticFourImageDense or sp4In_alt/sp4In0_alt as unconditional human suppliers','Generic potential automorphy as a replacement for literal IsAutQA','Equal-absolute-value purity in place of strict PureW','Full CohomologyHyp as needed by this lower chain','CountII/III or full RH/GRH','Lean kernel replay']}
write('closure.json',closure)
print(json.dumps(result['validation'],indent=2))
