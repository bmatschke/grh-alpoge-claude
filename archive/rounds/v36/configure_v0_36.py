#!/usr/bin/env python3
"""Define the additive v0.36 producer closures with unchanged original scopes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=["coefficient_fock_bridge","joint_harmonic_io","regular_quotient","count_choice"]
claims={n:[c["id"] for c in json.loads((ROOT/n/"provenance.json").read_text())["claims"]] for n in components}
def span(n):return claims[n][0]+"–"+claims[n][-1]
new=[
 span("coefficient_fock_bridge")+": complete original coefficient-to-polynomial bridge on the same c0L, cV and BV, with exact VV range, all-real covariance and compact cyclicity; the full original ArithAt/lamLdef and weights_of_minors installation, including all signed weights and integer determinant twists.",
 span("joint_harmonic_io")+": complete original JointHarm.exists_ioP. The parameter-free polynomial construction, exact Delta normalization on unit vectors, actual vacuum theta property and actual compact Weil character/substitution give one io_i before every t. The same original weak OrZero rule activates the stored ioP without asserting equality with the constructed witness.",
 span("regular_quotient")+": complete original IsReg from the same supplied FinPair, including global AE and strong continuity; original smooth_map and every ordered Hilbert derivative word; full original cusp-closure and Gelfand-scalar suppliers. Pointwise finite level/cuspidality/central finiteness now follow once original smooth representatives and derivative identities are supplied. Initial boundedness, target volume, smooth representatives and Sobolev evaluation/growth remain.",
 span("count_choice")+": complete original one-point NiceI Choice at h=0,a=n=4, including the full twisted polarized detector, finite t-adic generation and common ramified coefficient extension with every original NP/N3/N4/determinant field. The same chosen g=0 Kap satisfies literal B2 with C=0 for all m,N. These closures form one coupled witness; no arbitrary-Kap obstruction theorem is claimed.",
 "There are now 1770 cumulative human claims, with 71 added in this version. The selected graph keeps 34 open coupled leaves: 23 C, 9 B, 2 D. Its theta and CountII leaves are substantially narrowed, but no additional whole selected leaf is closed. All original graph edges and historical compound scopes are preserved. The human RH/Dirichlet-GRH reconstruction remains incomplete."
]
remaining=[
 "Construct the original common recursive/geometric member and compatible Bundle with its duties. DesignChoices/RecAtG, geometric readings, rational tests and actual RowsHold0_3 remain; the corresponding construction-class size/rank consumers are complete.",
 "Finish the actual target analytic realization: initial boundedness of the original extremal holomorphic cusp function and its target FinPair; actual smooth representatives for every same-quotient fixed-level smooth class with all derivative identities; one fixed-order Sobolev estimate before x,F,psi, yielding continuous evaluation and uniform moderate growth. Original ioP, full lowest type, Hilbert realization, IsReg, Hilbert smoothness, central scalar action and cusp closure are now supplied on their exact inputs.",
 "Produce actual NBuilt/NdSpec and the original local projection square on the common installation, retaining spectra, maximal ideals, coefficient embeddings and metric identifications.",
 "Supply the original denominator, retained-defect, period-height, local-gain and spectral estimates on the same family.",
 "Construct the compatible second-layer selector and duties. The entire eleven-field FamGLmin and same-family ChainTied/Closed consumer remain completed, with both universal losses and unchanged final constants; none creates the upstream common selection.",
 "For RH and two-primary targets finish original Cases I/II/V. CountII retains ordinary/control/arithmetic fibers, type/neatU/TThetaEx, the four further Hida endpoints, all-level same-J HasAut, B1, Raw, CohP and original side conditions. Its h=0 Choice and B2 are now supplied together on the same chosen g=0 Kap, in addition to prior universal NiceI Norm, ArPl and supplied-type IsRes. Both rank-four Links retain ell=3, fixed iota and one common coefficient threshold.",
 "Unrestricted Dirichlet targets additionally retain CaseIII, SeedIV and original chain propagation/descent; the two-primary specialization gives no universal CountIII.",
 "The optional AQ positive-part route and its separate arithmetic envelope remain optional. Historical RF16 remains governed by DEX11."
]
priority=(
 "Prioritize the actual same-quotient smooth representative and Sobolev producers, which now sit immediately after the completed Hilbert map and jointly supply pointwise derivatives, evaluation and uniform growth. "
 "Read SmoothVectorAutomorphicDerivatives and SobolevBoundForSmoothVectors together, preserving one finite level and one exponent/list before x,F,psi; then assemble BackForm.exists_multMap on the original map. "
 "In parallel reconstruct the original common selected-realization interface, beginning with SelC.cols_of_witnesses and its one ReadC before later TwArgs, then the same-R BunU/BWit package; keep its geometric, multiplicity and NEb premises visible. "
 "The next bounded CountII target is the exact selected B1, beginning with the full dualN uniform estimate and then the original local/global cardinality cancellation to 4[L+:Q]+4q; ordinary/type/HasAut remain separate producers. "
 "The h=0 Choice and chosen g=0 B2 are a coupled package; do not reopen the universal arbitrary-Kap obstruction branch for this route. "
 "Initial boundedness and target FinPair remain separate and cannot be inferred circularly from post-Hilbert central finiteness. "
 "Preserve the same original Bundle, coefficient ties, frames, metrics and finite levels; no compatible substitute counts as the original producer."
)
allnew=sum(claims.values(),[]);theta=claims["coefficient_fock_bridge"]+claims["joint_harmonic_io"]+claims["regular_quotient"]
updates={
 "CTC13":(theta,"The original all-parameter ioP, same-quotient IsReg, full Hilbert smoothness, exact cusp-closure and original Gelfand scalar producers are now supplied. Initial boundedness, target finite volume, actual smooth representatives and Sobolev evaluation/growth remain."),
 "TAE13":(theta,"For the actual same R, full original exists_ioP now gives exists io_i forall t and activates the stored weak choice. Together with the prior lowest-type packet it reaches the actual Hilbert map once boundedness/FinPair are supplied. RQC closes regular representation, smooth transfer, central scalar and cusp-closure suppliers; actual pointwise representatives and Sobolev completion remain."),
 "HCU18":(claims["regular_quotient"],"The same original FinPair now produces IsReg. The Hilbert map has every smooth-vector derivative word, and its original closed orbit span preserves cusp integrals for supplied continuous representatives. Gelfand operators act by one scalar on every smooth model vector. No actual pointwise representative or Sobolev estimate is inferred."),
 "HCU20":(claims["coefficient_fock_bridge"]+claims["joint_harmonic_io"],"The same ordered base model now participates in the fully constructed original simultaneous ioP, with literal coefficient range/covariance, integer determinant twists and exact Delta normalization before t."),
 "BTH12":(theta,"The analytic extension now has its original simultaneous ioP and regular/smooth/central/cusp-closure suppliers. Actual boundedness/finite volume and pointwise Sobolev realization remain, as do separate geometric readings, rational tests and original base rows."),
 "JSP11":(claims["count_choice"],"The required h=0,a=n=4 Choice is constructed, and its same chosen g=0 Kap satisfies literal B2 with C=0 for every m,N. This is a coupled existential closure, not a universal arbitrary-Kap theorem. Ordinary/control/type, four Hida endpoints, same-J HasAut, B1, Raw and original CohP remain."),
 "CIP12":(claims["count_choice"],"Alongside full universal NiceI Norm and original ArPl, the selected h=0 Choice and chosen g=0 B2 are supplied with all finite-extension transport fields. No original ordinary/control, type/neatU or automorphic producer is inferred."),
 "QX10":(claims["count_choice"],"Both original rank-four Links can use the same coupled h=0 Choice/B2 construction at ell=3 and fixed iota, retaining their common coefficient threshold, actual rings and ideals. B1/Raw and ordinary/automorphic support remain."),
 "DA1":(allnew,"The final ten-input interface is unchanged. The current theta and CountII nested producer obligations are reduced while all common-object requirements, selected edges and 34 whole open leaves remain."),
 "GH7":(allnew,"Both roots use the newly completed simultaneous ioP, regular/smooth/central/cusp suppliers and coupled CountII Choice/B2. RH still retains I/II/V; unrestricted Dirichlet GRH also retains III. The human proof remains incomplete.")
}
cfg=dict(artifact_version="0.36",date="2026-11-22",predecessor_version="0.35",components=components,
 expected_new_claims=len(allnew),component_claims=claims,
 scope="Partial human reconstruction of RH and Dirichlet GRH, accepting the underlying Lean proof as fully checked and correct. Version 0.36 completes the original simultaneous ioP, regular quotient/smooth/cusp/Gelfand suppliers and the coupled one-point rank-four Choice/chosen-B2 package. Actual common construction, initial target boundedness/volume, pointwise smooth/Sobolev, local/spectral and ordinary/automorphic producers remain. No new Lean replay is claimed.",
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope="Additive scope update; every predecessor field, source and dependency edge retained.") for k,v in updates.items()},
 precision_notes=[
 "Formal correctness is accepted; D records unresolved human source understanding, not an alleged Lean gap.",
 "A is an exact published application; B is independent elementary/moderate reconstruction; C requires substantial reconstruction; D is a source-understanding issue. Completion and category are separate.",
 "CFB retains the exact c0L, cV, BV, source action, inverse frames, entire VV range and forced lamLdef.",
 "JIO proves exists io_i forall t. Stored weak-choice activation proves the stored predicate, without equating two existential witnesses.",
 "The original unit norms and exact Delta polynomial are preserved; no unspecified phase or scalar is introduced.",
 "The explicit auxiliary eta0 used in the real vacuum character is not identified with the stored level eta and is not asserted to satisfy an unproved universal IsEtaTilde restriction.",
 "RQC constructs IsReg on the same FinPair and literal nuQ, with globally Haar-AE values and strong continuity.",
 "RQC smooth_map has the full original target generality; Hilbert derivative words retain their right-fold order and the same finite level.",
 "Cusp closure is proved through compact local L1 bounds, never by restricting arbitrary ambient L2 classes to a unipotent subgroup.",
 "Gelfand scalar action uses exactly k+1 cyclic matrix-unit products and the actual smooth domain; no unbounded operator is extended by continuity.",
 "Initial boundedness, actual FinPair, smooth representatives and Sobolev evaluation/growth remain producers. Post-Hilbert central finiteness cannot justify earlier boundedness.",
 "CCH closes Choice and B2 only together for the same chosen g=0 Kap at h=0,a=n=4. The full detector and ramified finite coefficient extension retain every NP, N3/N4 and determinant field.",
 "The selected B2 has C=0 before all m and all N. No universal arbitrary-Kap TaylorWilesObstructionBound is claimed.",
 "Both original rank-four Links retain ell=3, fixed iota, the common coefficient threshold and same-J automorphic support.",
 "All 245 inherited compound targets and 107 groups are retained; 34 open selected leaves are neither a completion percentage nor an absolute minimality theorem.",
 "No new published theorem is added in this version; earlier checked applications retain their exact scopes.",
 "No Lean replay or PDF production. Draft TeX checks syntax and references only."
 ])
assert cfg["expected_new_claims"]==71
(ROOT/"increment_v0_36.json").write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+"\n")
print("Configured",len(allnew),"new human claims.")

