#!/usr/bin/env python3
"""Write the standalone mathematical progress report and continuation plan."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT / name).read_text())

cfg = read('increment_v0_45.json')
stats = read('integration_stats_v0_45.json')
tex = read('tex_validation.json')
assert tex['artifact_version'] == '0.45'
for item in tex['documents']:
    assert item['tex_sha256'] == hashlib.sha256((ROOT / item['tex_filename']).read_bytes()).hexdigest()
    assert item['syntax_compile_succeeded'] and not item['undefined_references_or_citations']
    assert not item['missing_character_warnings']

head = [
    'RH AND UNRESTRICTED DIRICHLET GRH — HUMAN RECONSTRUCTION v0.45',
    '23 November 2026', '',
    'CURRENT RESULT', '', cfg['status'], '',
    'This continuation completes one entire selected obligation: COUNT_II_SUPPORT. '
    'Each of the two original rank-four Links now has one ideal carrying all six '
    'Hida properties and the selected P1core support condition. The common '
    'coefficient threshold precedes every later coefficient ring and universal '
    'datum. This is a completion inside the selected human reconstruction; the '
    'overall human-readable RH/Dirichlet-GRH proof is still unfinished.', '',
    'The updated ZIP contains the complete cumulative work, the seven new '
    'chapters, the pinned source excerpts, the claim and dependency ledgers, '
    'independent review records, and the exact continuation plan. No PDF is '
    'required for this release; the two TeX readers have been compiled in draft '
    'mode for syntax and reference checks.', '',
    'INVENTORY', '',
    f"New claims: {stats['new_claims']} (all class B). Cumulative claims: {stats['cumulative_claims']}.",
    f"Predecessor claims preserved: {stats['cumulative_claims'] - stats['new_claims']}.",
    f"Selected graph: {stats['selected_nodes']} nodes and {stats['selected_edges']} edges.",
    f"Open whole obligations: {stats['open_count']} ({stats['open_categories']['C']} C and {stats['open_categories']['B']} B).",
    f"Shared RH/Dirichlet-GRH obligations: {stats['shared_open']}. Additional Dirichlet-GRH obligations: {stats['extra_grh_open']}.",
    f"New increment source inventory: {stats['new_source_files_checked']} pinned files and {stats['new_unique_source_ranges_checked']} distinct ranges.",
    'A claim count is an inventory, not a proof-completion percentage. One large '
    'compound obligation can require many lemmas. Class B identifies a written '
    'proof in its stated scope; the published and foundational inputs remain '
    'explicit.', '',
    'THE NEW CHAPTERS', '',
]
for i, (component, description) in enumerate(zip(cfg['components'], cfg['local_conclusions']), 1):
    claims = read(component + '/provenance.json')['claims']
    head.extend([f"{i}. {claims[0]['id']}–{claims[-1]['id']} ({len(claims)} claims)",
                 'Proof: ' + component + '/main.tex', description, ''])

discussion = '''WHY THE SAME IDEAL IS THE CENTRAL ASSEMBLY CONDITION

The proof needs one particular ideal in each original universal ring. It is
insufficient to produce separate ideals with separate desirable properties:
the support implication consumes arithmetic density, point return,
decomposition, automorphy away, twisting and the auxiliary-level construction
for the same ideal. HIA therefore begins with the actual ordinary Hecke data at
the empty auxiliary level. Its IsJ witness supplies J once. JRP15 and UPA18
give ring and dense on that J. HPT18, HED16, HAW19 and HTS8 give pt, end1,
end2 and twist on the same J. HLM26 and HTW24 then give the all-level
automorphy input without changing J.

The zero-module case is part of the argument. There the original IsJ relation
gives the top ideal. In the nonzero case it gives the kernel of the specified
surjective universal-ring map to the actual Hecke algebra. Subsequent steps
retain this map and ideal rather than selecting an abstract support ideal
with fewer recorded properties.

The final support step applies the previously completed selected rank-four
patching route. The one-point normalization, the chosen full-block Kap with
h=0, a=n=4 and g=0, the arithmetic prime realization, the coupled B1/B2
bounds, and the selected Raw theorem were already reconstructed. In
particular D=4[L+:Q]+4T.q and the chosen B2 constant is zero. Their original
uniformity and finiteness premises stay in place. HIA supplies the missing
HasAut input and invokes the exact JSP11 consumer, giving P1core for J.

Doing this on each QX Link yields two ideals in two different universal
rings. The word "same" is used within each ring: its Hida fields, HasAut and
P1core refer to that ring's one J. The two Links retain their common scalar
characters, their distinct auxiliary primes, the fixed coefficient-field
identification iota, and one threshold chosen before later coefficient rings,
Spaces or universal data. No identification of the two different universal
rings is asserted.

The original downstream assembly now receives its missing support input.
QX10 constructs the five-field PotentialModularityTower and PMExAlt on the
original Space, and YX2 gives CountII under its unchanged background inputs.
Case II is therefore removed from the active remaining-work sentence. This
does not remove the independent Case I/V, rigidity, congruence, common-family
or global-estimate obligations, or the additional Case III work for unrestricted
Dirichlet GRH.

DECOMPOSITION AND THE STRICT NORM INEQUALITY

The decomposition chapter retains all original cuspidal ranks and all
positive Speh lengths. It starts with the representation actually supplied by
the arithmetic point. The initial Galois representation attached to each
cuspidal constituent is shifted by the exact automorphic norm power, and the
remaining copies are its prescribed inverse cyclotomic twists. A cofinite
degree-one Frobenius comparison, followed by the already matched Chebotarev
consumer, identifies the characteristic polynomial at every group element.

When the Speh lengths are all one, each relevant generic unitary spherical
factor has Satake roots in the strict interval

                     q^(-1/2) < |alpha| < q^(1/2).

This implies |z| < q|z'| for the prescribed pairs in the Frobenius multiset.
The theorem keeps the original cofinite set, all required places and every
supplied multiset. It does not assert a uniform gap from either endpoint,
and it does not restrict the complete decomposition theorem to length one.

Automorphy away needs a related but different uniformity. One real norm
twist is chosen globally from the central character before any finite place
is selected. Its single exponent provides the common center of all local
windows. The ordered ordinary-character calculation then rules out a
positive-power cyclotomic ratio: that ratio would force an exact factor q
between two character norms, contrary to the strict window. The conditional
continuity clause is kept exactly where it occurs in the source predicate.

RETURNING A GIVEN POINT TO THE ACTUAL HECKE SUPPORT

HPT constructs an actual ordinary automorphic vector with the original
integral type, infinity weight, depth and residual block. Several normalizing
identities matter here: the q powers in the positive Hecke generators, the
degree-minus-one convention for the chosen uniformizer, and the cancellation
between the low weight and the cyclotomic exponent. The proofs write these
identities out before asserting that the vector belongs to the original
ordinary block.

The resulting Hecke point must be the point supplied at the start. Both maps
are first captured in one finite complete local coefficient ring. Equality of
the full determinant law and ordered characters then lets the original
universal property identify the entire maps. Thus J is contained in the
original point kernel. This containment is proved, not used as a starting
hypothesis.

The return theorem UpUW holds in every positive rank. The final Hida pt
field has the source's narrower antecedent 2 <= n <= 4 and retains its exact
DescWeak input. Consequently the all-rank Hida assembly is legitimate: for
ranks outside that interval the pt implication has an impossible antecedent.
This does not extend the low-rank descent foundation to arbitrary rank.

Twisting uses the all-rank return theorem. For an odd character order
m=2N+1, the power mu^(N+1) squares to mu. The resulting actual adelic
determinant character has the required split local square. Multiplying
automorphic functions by this character preserves the infinity weight and
the required finite local vectors. Full polynomial-law twisting and the
guarded local comparisons supply the return theorem's hypotheses. The
argument retains ell=3 and does not borrow the low-rank descent premise.

INTEGRAL MODULES AND THE TWO COMPARISON MAPS

At auxiliary level the proof cannot divide by the order of the diamond
group. HLM uses an integral trace-projectivity argument and an actual
group-algebra splitting. The ordinary and residual projectors preserve the
required structures; Artin–Rees supplies the residual decomposition. The
directed union consists of actual automorphic functions, so its fixed modules
are the original modules at every allowed level.

The determinant law is constructed before it is used. Compact interpolation
over the coefficient ring, integral word identities in finite-degree truncated
scalar algebras, and polynomial coefficient separation give the law after
every scalar extension. An infinite-support group ring is never substituted
for those finite computations. The full ordinary pair gives the universal
map at each level, and uniqueness glues these maps into one action.

HTW proves the finite comparison identities explicitly. With ordered
variables, write

             d = product_(i<k) (X_k-X_i),
           N_Q = product_(i<k) (X_k-Q X_i),
           partial = alternating sum divided by d.

The dual families a_T,b_T satisfy

                 sum_T a_T w(b_T) = delta_(w,1) d.

These identities give both dual expansions over the symmetric ring. The
actual finite Hecke trace operator is E(f)=partial(N_Q f), as proved in its
faithful polynomial representation. They yield both comparison maps, not
only an abstract equivalence after extending scalars. Their compositions
are then multiplied by the remaining specified factors to give exactly the
original ordered-pair polynomial fEl.

The tame Hecke calculation retains diagonal-unit terms. Its quadratic
relation is T_s^2 = Q + T_s sum_c D_c, with
T_s D_c = D_c^s T_s. The left and right inverse expressions consequently
have the appropriate conjugated terms in different positions. The simpler
Iwahori relation is recovered only in its correct specialization. A Jacquet
dimension bound gives the same exponent n! for all later auxiliary choices;
isotypic multiplicity does not enlarge this exponent.

The topologically nilpotent part is a canonical summand of a finite
coefficient algebra module. It remains projective, hence finite free, over
the local diamond group algebra. Its inverse-limit action, the ordered-root
summand and the two comparison maps survive completion. The coefficient
map sends the root variables to their chosen roots minus prior lifts, and
the additional variables to zero. This proves the exact prescribed
coefficient-map identity, together with every field of TWRing and TWMaps.
One base and one system of root lifts precede every later N.

WHAT THE CLOSURE DOES AND DOES NOT CONTAIN

The entire selected COUNT_II_SUPPORT contract is now complete: both original
rank-four Links, the fixed iota, one prior coefficient threshold, and one
ideal in each later universal ring with all six Hida fields and P1core.
The full original HidaUAlt is also assembled for every positive rank.

Full ModularAlt and ModUAlt have an additional original PfromAut supplier.
The selected single-point P1 proof does not supply arbitrary NiceE chains
or the full P3core field. Their general implication is recorded with that
premise. No arbitrary-Kap B1/B2 result, vanishing of Sel1, stronger local
estimate or arbitrary-chain patching statement is inferred.

The named foundations are preserved at their original scope: base change,
polarized cuspidal attachment, local representation and correspondence laws,
the low-rank descent input where used, CohP, local class field theory and
the relevant period laws. Prior explicitly matched published applications
remain available. This increment introduces no new literature theorem as a
separately classified published application.

VALIDATION AND REPRODUCIBILITY

Each of the seven chapters has a complete independent mathematical review
by agents other than its author; some chapters use disjoint focused reviews.
The review registry checks their union against every new claim and binds
both the whole proof file and each reviewed block by SHA-256. The source
manifest binds each cited range and verifies the entire source file against
the pinned git blob. The selected closure has its own final assembly review.

The integration audit separately checks predecessor preservation, the
acyclic mathematical dependency graph, original source records, exact
remaining-contract changes, source snapshots and current continuation
metadata. The semantic review checks the claimed scope, all-rank versus
selected-rank distinctions, the shared ideal, both Links, and choice order.
Their reports and the final validation record are included in the ZIP.

Draft-mode TeX compilation checks both complete readers. No PDF visual
review, Lean execution or kernel replay is claimed. The source formal proof
is accepted as correct for this reconstruction. The claim DAG describes the
human reconstruction and is not a mechanically extracted Lean dependency
graph. Historical proof chapters and all predecessor claim records remain
unchanged; mutable root metadata is preserved in history/version_0_44.

NEXT WORK, ALREADY AUTHORIZED

Continue towards the full human-readable RH and unrestricted Dirichlet-GRH
proof. Do not reopen the seven completed chapters or ask permission to
continue the existing reconstruction. Use the current 30-contract register,
not historical frontier descriptions, as the authority.
'''
tail = []
for i, target in enumerate(cfg['next_targets'], 1):
    tail.extend([f'{i}. {target}', ''])
tail.extend(['COMPLETE REMAINING MAJOR INPUTS', ''])
for i, target in enumerate(cfg['remaining_major_inputs'], 1):
    tail.extend([f'{i}. {target}', ''])
tail.extend([
    'TEX CHECKS', '',
    f"New-chapters reader: {tex['documents'][0]['passes']} draft passes; "
    f"{tex['documents'][0]['overfull_box_warnings']} overfull boxes; no undefined references or missing characters.",
    f"Cumulative reader: {tex['documents'][1]['passes']} draft passes; "
    f"{tex['documents'][1]['overfull_box_warnings']} overfull boxes; no undefined references or missing characters.",
    'The cumulative overfull-box count is retained from the historical manuscript '
    '(53 in v0.44). The historical proof body remains verbatim. These draft '
    'checks do not certify PDF layout; no PDF was generated.', '',
    'READING FILES', '',
    'RH_new_proofs_v0_45.tex — current audit and the seven new proof chapters.',
    'RH_readable_reconstruction_v0_45.tex — the complete cumulative manuscript.',
    'RH_dependency_audit_v0_45.txt — all 30 exact remaining selected contracts.',
    'continuation_checkpoint.json — current state and scope.',
    'next_source_targets.json — source-based continuation targets.',
    'provenance.json — all claims, exact proof/source ranges and dependencies.',
    'validation_v0_45.json — final release checks and hash-bound review registry.',
    'SHA256SUMS — hashes for the distributed files.', '',
    'SOURCE PIN', cfg['source_commit'], '',
])
text = '\n'.join(head) + discussion + '\n' + '\n'.join(tail)
(ROOT / 'RH_reconstruction_progress_v0_45.txt').write_text(text)
(ROOT / 'README.txt').write_text('\n'.join(head[:head.index('THE NEW CHAPTERS')]) +
    '\nRead RH_reconstruction_progress_v0_45.txt for the mathematical explanation, '
    'scope and next tasks. The new and cumulative TeX editions, exact audit, '
    'source snapshots and all review records are included.\n')
print(json.dumps({'progress_bytes': len(text.encode()), 'new_claims': stats['new_claims'],
                  'remaining_whole_obligations': stats['open_count']}, indent=2))
