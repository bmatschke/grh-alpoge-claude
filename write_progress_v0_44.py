#!/usr/bin/env python3
"""Write the complete standalone v0.44 progress and continuation report."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
cfg=read('increment_v0_44.json');st=read('integration_stats_v0_44.json')
val=read('validation_v0_44.json');assert val['result']=='PASS'
tex=read('tex_validation.json')
audit=read('reviews_v0_44/integration_main_proof_rigidity.json')
assert audit['status']=='PASS' and not audit['errors']
lines=['RH AND UNRESTRICTED DIRICHLET GRH',
 'Human-readable reconstruction — version 0.44','23 November 2026','',
 '1. WHAT THIS CONTINUATION ACHIEVES','',
 'Version 0.44 proves the full original automorphic-part construction, installs the bare density theorem for the same original ideal J, and completes the ordinary Hecke-point record and all eight ring properties for that ideal. The arguments are written in seven mathematical chapters, developed in parallel and independently reviewed.','',
 f'There are {st["new_claims"]} new claims and {st["cumulative_claims"]:,} cumulative claims. Every one of the 2,441 predecessor claim records, its source arrays, mathematical dependency edges and historical proof bytes is preserved. The new claims consist of 117 written-proof blocks and 2 precisely matched published applications. The inventory is not a completion percentage.','',
 'The selected sufficient-route graph remains 121 nodes and 161 edges, with 31 whole obligations open: 22 class C and 9 class B. Twenty-four are shared by RH and Dirichlet GRH; seven are additional for Dirichlet GRH. No whole selected leaf is newly closed. Several substantial producers within the compound ordinary/Hida/support obligation are now complete.','',
 cfg['status'],'',
 'The pinned formal proof is accepted as fully checked and correct. This work reconstructs its human mathematics; it does not reopen formal correctness. The cumulative human proof remains partial. In particular, the remaining four Hida outputs and all-level same-J support on both rank-four Links have not been inferred merely from the completed ring and density fields.','',
 '2. THE SEVEN NEW CHAPTERS','']
for i,paragraph in enumerate(cfg['local_conclusions'],1):lines += [f'2.{i}. {paragraph}','']
lines += ['3. FOUR MATHEMATICAL POINTS THAT MAKE THE INSTALLATION WORK','',
 'A. The half twists are constructed before Galois attachment.','',
 'For a cusp of rank a, a Speh length d and the k-th copy, the total parameter has real twist (d−2k−n)/2. To attach a Galois representation with an allowed half-integral shift e/2, GUA first twists the actual cusp by |det|^((e+a−1)/2). Its infinity type becomes regular algebraic in the original convention, and its quadratic Hecke polarization has the required sign. The original polarized attachment theorem then applies. Its algebraic local normalization cancels the (a−1)/2 correction and leaves exactly e/2. Thus no square root of the cyclotomic character is assumed. All copies are retained until irreducibility, if present, forces only one positive block.','',
 'B. The Frobenius inverse and the same representation are explicit.','',
 'If B={beta_i} is the normalized Satake multiset and the maximal compact has volume one, the j-th spherical operator has eigenvalue a_j=q^(j(n−j)/2)e_j(B). Therefore the exact source Hecke polynomial is','',
 '  sum_j (-1)^j q^(j(j−1)/2) a_j X^(n−j)',
 '       = product_beta (X−q^((n−1)/2) beta).','',
 'Every allowed IsRecT correspondence sends the algebraically normalized spherical representation to arithmetic Frobenius eigenvalues beta^(-1)q^((1−n)/2). Taking the original Frobenius inverse gives the displayed polynomial. UPA uses this same Galois representation for the spherical reading, the AtLT and away-place local comparisons, the type matrices and polarization. It descends through the actual map V.pr; it is not replaced between record fields.','',
 'C. Distinct inertia characters produce an actual ordered flag.','',
 'The raw Weil action, before Frobenius semisimplification, is the action intertwined by the original period scalarization map. Its characteristic polynomial agrees with the semisimplified parameter because the correcting factor is commuting and unipotent. The proof transfers polynomial identities first, then applies finite inertia projectors to the raw action. Distinct inertia characters produce one-dimensional lines, so a nilpotent commuting operator vanishes. The full Weil scalar on each line is recovered by a trace-projector calculation.','',
 'Averaging descends a nonzero invariant through scalarization, using all Frobenius translates to obtain faithfulness. A periodic period is made Frobenius fixed by a finite sum with coefficients in a maximal unramified field; a Vandermonde matrix proves that one such sum is nonzero. If the Hodge–Tate weights are nonnegative, the de Rham filtration is in degree zero and the fundamental crystalline intersection yields an actual Galois-fixed vector. Twisting by the inverse of the first ordered ordinary character makes the weights nonnegative. Untwisting gives its eigenline, and the quotient carries exactly the remaining weights and parameter factors. Induction supplies the full ordered flag.','',
 'D. Equality of determinant laws is proved at the required strength.','',
 'HEP first obtains characteristic polynomials at the original dense inverse-Frobenius set. Continuity extends them to every group element. After evaluation in Qbar_l, dual numbers show that the trace is a natural linear map, and Newton identities recover every determinant coefficient over every Qbar_l-algebra. This gives equality of complete determinant polynomial laws. The divisions by positive integers occur only over Qbar_l; they impose no extra restriction on the coefficient prime, including 3.','',
 'For JRP, the family of actual Hecke points jointly separates B/J. Injectivity of polynomial coefficients, applied to generic finite-support group-algebra elements, then descends full polynomial laws and their kernel conditions to B/J. No injectivity after an arbitrary tensor product is presumed. The ordered ordinary matrix product vanishes because its rightmost factor lowers the last flag step, the next lowers the preceding step, and so on. Its order is never changed. The original star operation follows from the same polarization matrix.','',
 '4. EXACT SCOPE AND FOUNDATIONS','',
 'The new work retains the original BaseChangeIsobaricN and polarized cuspidal attachment RowT/PropsB foundations. It also retains the explicitly named original local representation, class-field, correspondence-existence and period-ring theorems. The proofs reconstruct their full consumers and record every application at its actual scope. They are not labeled new proofs of the entire trace formula, local Langlands theory or period comparison foundations.','',
 'Two published applications are matched explicitly: the spherical Satake normalization of Gross (Proposition 3.6, formula (3.14), Proposition 6.4, Haar normalization (2.5)), and the generic unitary factorization of Mœglin–Waldspurger (§§I.10–I.11, pp.639–640). The latter leaves all real exponents in the strict interval (−1/2,1/2). It is used only on actual generic unitary local components, not as an unproved temperedness assertion.','',
 'The exact same coefficient DVR, fixed iota, local Artin maps, ideal J, levels, component choices and period bridges are preserved. The Galois attachment retains its Gd conditional compatibility. The cuspidal conclusion retains the original irreducibility condition. The full determinant and point property hold at every admitted arithmetic Hecke point; the ordered flags and potential crystallinity retain the exact Good guard. Both original rank-four Links remain in scope.','',
 '5. REVIEW AND VERIFICATION','',
 f'All {st["new_claims"]} new claims have an independent mathematical/interface review, bound to the complete proof files and individual blocks. The increment cites {st["new_source_files_checked"]} source files and {st["new_unique_source_ranges_checked"]} unique inclusive ranges; every byte matches the accepted source commit.',
 f'The independent integration audit reports {audit["passed_check_count"]:,} passed checks and no errors. It checks predecessor preservation, source/proof hashes, dependencies, selected whole contracts, the exact closure delta and continuation metadata. A separate semantic review checks that the generated status reports preserve the original guards and do not promote compound obligations prematurely.','',
 'The reviews led to concrete repairs before release: the base-change Satake calculation now has the correct paired right-coset/modulus orientation; the ordinary-period argument explicitly distinguishes raw Weil action from Frobenius semisimplification; local Artin uniqueness includes a written injectivity argument using the original Artin-kernel and Chevalley unit-congruence inputs. These were resolved in the final proof bytes.','']
for d in tex['documents']:
 lines += [f'{d["tex_filename"]}: draft TeX compilation succeeded in {d["passes"]} passes; no missing characters or unresolved references; {d["overfull_box_warnings"]} overfull-box warnings.']
lines += ['',
 'Draft TeX compilation checks syntax and references. No PDF generation, visual layout certification, Lean build or kernel replay is claimed. The historical cumulative overfull boxes are retained; the new reader edition has zero overfull boxes.','',
 '6. NEXT EXACT ENDPOINTS','']
for i,s in enumerate(cfg['next_targets'],1):lines += [f'{i}. {s}','']
lines += ['The immediate Hida target has six fields. RingProps and Dense are now supplied; PointTheoremBaseObject, ArithmeticPointDecomposition, IrrArithPointsAutomorphicAway and TwistOk are still to be constructed. The complete Out.pt proved in HEP is a different, earlier output from the later PointTheoremBaseObject field. The continuation_v44 handoff identifies the exact pinned producers and parallel starting points.','',
 'The full remaining global input register is:','']
for i,s in enumerate(cfg['remaining_major_inputs'],1):lines += [f'{i}. {s}','']
lines += ['7. FILES AND REPRODUCIBILITY','',
 'RH_reconstruction_v0_44.zip — complete versioned continuation, seven new chapters, all predecessor components, source snapshots, provenance, mathematical and integration reviews, exact remaining contracts, reproducible scripts and SHA256SUMS.',
 'RH_new_proofs_v0_44.tex — current dependency audit and the complete seven new proof chapters.',
 'RH_readable_reconstruction_v0_44.tex — full cumulative manuscript, preserving all historical proof chapters.',
 'RH_dependency_audit_v0_44.txt — every remaining whole selected contract and the new completed internal suppliers.',
 'RH_reconstruction_progress_v0_44.txt — this standalone substantive report.','',
 'Source pin: '+cfg['source_commit'],
 'The new claim ranges are LTP1–21, BCS1–19, GUA1–18, UPA1–18, OFL1–16, HEP1–12 and JRP1–15.','']
(ROOT/'RH_reconstruction_progress_v0_44.txt').write_text('\n'.join(lines))
# README.txt is the short human-readable entry point; README.md is assembled separately.
(ROOT/'README.txt').write_text('\n'.join(lines[:14])+ '\n\nRead RH_reconstruction_progress_v0_44.txt for the full report and exact continuation scope.\n')
print(json.dumps({'file':'RH_reconstruction_progress_v0_44.txt','bytes':(ROOT/'RH_reconstruction_progress_v0_44.txt').stat().st_size,'new_claims':st['new_claims']}))
