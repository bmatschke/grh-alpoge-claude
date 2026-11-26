# Independent review of FCD1–FCD18

**Result: PASS at the explicitly stated original scope.**

Reviewer: `/root/arithmetic_common_frame`. Author: `/root/geometry_alltest`.
The reviewed main text is SHA256 `a7ec7d7587ba8ae7c11e9128729ab4af2fa392c4aca8df33c549726468d08d56` at accepted RH source commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`.

## Mathematical findings

The packet proves three complete original suppliers: simultaneous homogeneous-matrix flat-chart descent, the finite graded presentation with chart-power torsion kernel and cokernel, and the original Noetherian graded-cube model. I compared the literal original theorem headers and their bodies with the human proofs. The original coefficient ring stays arbitrary, the charts share one coefficient subring and presentation, and no flatness of a later coefficient map is inserted.

FCD5's completion argument is sound. The Artin–Rees bound follows from a finite graded submodule of the Noetherian Rees module. It makes completion exact on finite modules; a finite presentation identifies completion with tensoring by the completed ring. The ideal criterion then gives completion-flatness. Formal smoothness supplies compatible lifts into every quotient by a power of the same ideal, so the quotient is an actual module retract of that completion. No hidden separatedness, proper-ideal or Jacobson-radical assumption is needed.

FCD11–12 handle the relations, not merely the generators. The proof of J=K+uF homogenizes the actual preimage and removes the remaining power of X modulo X−1; K intersect uF=uK uses the finite-support degree recurrence on the target. This yields finite dehomogenized relation modules and one homogeneous matrix whose chart kernel and cokernel assertions hold for arbitrary elements. The argument does not assert that the original graded module itself is finite.

FCD15 correctly separates the augmented and ordinary Cech complexes. The monomial differential and contracting homotopy have compatible signs, the all-negative top exponent vectors are finite in a fixed degree, and descending induction handles arbitrary finite graded modules without finite projective dimension. The degree-zero ordinary Cech term is supplied by its stated exact sequence. Empty chart index sets are included.

FCD17–18 keep the actual comparison maps. Tensor right exactness is enough for the cokernel presentation, and split homogeneous components commute with tensoring even for nonflat ring maps. The localization formulas commute with every vertex restriction. The single cube C0 and the displayed composite theta therefore give all three original outputs, with no assertion of flatness or bijectivity at the unused empty vertex.

FCD14 retains the source's broader scope: pi need not be surjective, and only the source module needs a direct-sum decomposition. The subsequent geometric section module, its chart maps and all actual-section comparisons remain explicit unsupplied producers. The reuse of GSL8 is correct at its literal premises; no global Perf, section law, Moduli producer or whole RH/GRH obligation is closed.

## Source and binding checks

All 41 main-repository source snapshots were independently compared byte-for-byte with pinned Git blobs. All 49 manifest ranges and every one of the 18 marked human proof blocks were hashed independently. The three inherited GSL8–GSL10 blocks and their complete proof file were checked.

The four Mathlib files are a separate dependency, at commit `0df444a360eaa60ab8c11dca51a86af692955474`, exactly the revision recorded by the pinned `lake-manifest.json`. I independently fetched all four exact pinned raw URLs and checked equality with the saved snapshots and their hashes. These are not labeled as files from the RH repository commit.

No mathematical or scope correction is required. No Lean replay was performed.
