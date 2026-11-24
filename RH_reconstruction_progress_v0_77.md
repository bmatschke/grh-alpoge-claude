# Edition 0.77 · Constructing the geometric record for rational theta lifts

For an eligible column, take the geometric record and the theta map it actually stores. Edition 0.76 needed three further inputs on this record to obtain rational tests at both levels. Edition 0.77 derives two of them. The rank bound follows from the context, and the record's own geometric data give all seven comparisons in `InGeo`. After the finite request for coefficient-field values, only the analytic map-existence condition `ExAt` is needed on such a record. The manuscript also works backwards from a preliminary seed and constructs one record, with its rational tests, under the stated arithmetic and analytic hypotheses. **Ten whole obligations remain.** All ten are shared by RH and unrestricted Dirichlet GRH. [Two column theorems](continuation_v77/column.tex) · [Whole-obligation ledger](continuation_v77/obligations.json)

[New TeX manuscript](RH_new_proofs_v0_77.tex) · [Cumulative TeX manuscript](RH_readable_reconstruction_v0_77.tex) · [Previous edition](RH_reconstruction_progress_v0_76.md)

## What gets chosen, and when?

| Data already given | What the construction supplies | Where to read |
| --- | --- | --- |
| A context and a stage over it | The stable rank inequality and the standard integral lattice in each definite frame | [H77S1–H77S3](continuation_v77/stage.tex) |
| The prehost, frame, small fields and allowed twists | One finite request for residue roots, Hecke splitting at the ordinary and lift rows, and fields of definition of the higher covers | [K77F1–K77F4](continuation_v77/coefficients.tex) · [F77W1–F77W2](continuation_v77/request.tex) |
| A pinned geometric record on an admitted column | Integral stability of its lattice and all seven comparisons between sections, vectors and level actions | [G77D1–G77D7](continuation_v77/geometry.tex) |
| That same record, with the eight analytic map-existence clauses | A separating test family in each row at each of its two levels, and a full modular lattice at each level | [Q77Z1](continuation_v77/column.tex) |
| A lawful initial core, a preliminary analytic seed with readings, and the specified analytic and geometric inputs | One record satisfying the original four-part `Fine` predicate, with both levels of tests on it | [V77Q1–V77Q3](continuation_v77/seed.tex) · [Q77Z2](continuation_v77/column.tex) |
| A prescribed good core in either indicated system of conditions on points | A witness on that core's prescribed division lattice with the same dependent pair of datum and object, and its kernel certificate | [S77C1–S77C3](continuation_v77/selection.tex) |

The tests are complex-linear functionals on the target whose common kernel in each row is zero. At a given level the same finite list must distinguish target vectors and take values in the fixed embedded field on **all** rational theta inputs and **all** stored target basis vectors. Picking a new coordinate system separately for each input would leave that requirement open. Fullness of the modular lattice means that its span over the coefficient field is the row coordinate space. [Rationality and tests](continuation_v76/ties.tex) · [Application to the stored map](continuation_v77/column.tex)

## The rational vector in the chosen coordinates

Start at the distinguished embedding, where the record specifies a unit extremal vector. For a rational source vector, the base class-sum identity expresses the evaluation of its theta lift as a finite sum of readings of algebraic cusp sections $f_l$. The coefficients $a_l$ belong to the large coefficient field $L$ of the original row. If $\operatorname{coord}(f_l)$ denotes the coordinates installed by the geometric construction, take

$$
y=\sum_l a_l\,\operatorname{coord}(f_l).
$$

Evaluating the image of $y$ at the marked unit vector gives exactly the same automorphic function as evaluating the theta lift. Evaluation there is injective, so the two vectors agree. This constructs the rational vector before using a spanning theorem at the other embeddings. It also covers a zero lift. [Reference reading and its base comparison](continuation_v77/reference.tex) · [Target coordinates](continuation_v77/action.tex) · [Rational vector, V77Q1](continuation_v77/seed.tex)

The choice of field and the choice of coordinates serve different purposes. The integral coefficient pin identifies the embedded core field exactly with the prescribed small field. Principal ideles, the infinity type and approximation at the conductor then control the base character on every finite idele. In the later update the dictionary, frame and component constants change together. On an orbit where a section has a nonzero reading, the changes of reading form a cocycle whose value is one at a stabilizer. Transport from one representative then fixes the constants. When every reading on the orbit is zero, the constants can all be one. This installs one level action on the rational target. [Core field](continuation_v77/coefficients.tex) · [Changing the frame and multiplier](continuation_v77/adaptation.tex) · [Component constants and target action](continuation_v77/action.tex)

## How the geometric and analytic conditions enter

The rank identity on an admitted stage is $n_V=8fr+4+\mathrm{TOv}(s)\,\mathrm{nWv}(R,s)$, and the final summand is nonnegative. In this range the short theta generators have a strictly positive last weight in one block. That weight puts a full-block minor in their polynomial. At zero frequency the derivatives have a row relation, so such a minor vanishes. The common period lattice gives nonzero frequencies a gap. Shifting the coefficient integral into the complex domain gives exponential decay that controls the bound even as the shortest lattice vector shrinks. The resulting generators are cusp sections at every good embedding. Their readings span the given multiplicity space there. Conjugate evaluation then supplies the corresponding statement at the remaining embeddings. [Rank identity](continuation_v77/stage.tex) · [Cuspidality and uniform spanning, G77D5–G77D7](continuation_v77/geometry.tex)

For the analytic existence predicate, six of its eight fields follow under the stated definite-row kernel and realization hypotheses. The two inner-tower fields have an important order of choice. At an inner step there must be one intertwiner before choosing a twist. For each twist the theta integral must factor through the intertwiner stored in the record. The proof compares their kernels on compact-finite inputs. A compact average preserves the pair consisting of the intertwiner value and the integral, so the identity extends to smooth inputs. This construction uses the indicated archimedean embedding and positivity, the local image theorem, theta-integral estimates, cuspidality and smooth globalization. The finite-dimensional constructions alone do not discharge those hypotheses. Map existence is applied once to the preliminary weak record and once more after installing the final target fields, phase and scalars. [Eight existence clauses](continuation_v77/existence.tex) · [The two inner arrows](continuation_v77/interior.tex) · [Final record update](continuation_v77/seed.tex)

The ordinary and lift readings also have a concrete local input now supplied in the manuscript. At an allowed split prime, intersect a decorated neighbor with the starting lattice. The intersection is the kernel of a residue map of the prescribed codimension. Self-duality recovers the whole neighbor from that intersection, including the enlargement at the conjugate prime. Thus the cosets $aK_v$ in the split Hecke double coset correspond bijectively to the neighbors. One finite choice of representatives works for every translate of the starting lattice. The full-level double-coset and inert-operator comparisons still enter the seed with their stated hypotheses. [Decorated-lattice readings and split neighbors, B77R1–B77R5](continuation_v77/reading.tex)

## What keeps the whole rational-test obligation open?

The whole contract asks for the rational tests, the base readings, the row identifications and the eta comparisons on **one linked bundle**, throughout the eventually required family. Q77Z2 constructs a fine record given a seed and core. S77C3 starts with a point already certified good and moves its record to the prescribed division lattice. These are different starting hypotheses. Neither gives a good core and a compatible bundle throughout that family. [Column construction](continuation_v77/column.tex) · [Whole contracts](continuation_v77/obligations.json)

S77C4 proves that the witness at a prescribed good point and its reciprocity record can both be chosen before specifying the real lower bound on bundle size, under the stated analytic, Artin and ray-field hypotheses. For this fixed choice, S77C5 identifies the remaining size-dependent step. For every requested size there must be a bundle with that very reciprocity record and a witness for the original comparison conditions. Producing the good cores uniformly and proving this size-dependent implication would let the earlier linked transport carry the tests and readings together. These are the two places to continue the reconstruction. [Exact point, reciprocity and bundle quantifiers](continuation_v77/selection.tex) · [Bundle on a prescribed reciprocity record](continuation_v73/reading.tex) · [Transport through the common bundle](continuation_v74/bundle.tex)

## Verification

The edition adds 50 indexed manuscript claims, bringing the cumulative count to 4,317. Its ledger binds the 13 reviewed TeX chapters and their claim dependencies to 400 inclusive source ranges in 207 files at the pinned Lean revision. The verifier checks source bytes, dependency coverage and the inherited obligation graph. The validation record reports local typesetting for the supplement and cumulative manuscript. These are source and document checks. The new arguments are written in TeX and this edition does not add Lean declarations. [Claim ledger](continuation_v77/claims.json) · [Verification record](continuation_v77/validation.json) · [Checkpoint](CURRENT_CHECKPOINT_v0_77.json)

~~~sh
python3 continuation_v77/verify.py --formal-git formal_source
pdflatex RH_new_proofs_v0_77.tex
pdflatex RH_new_proofs_v0_77.tex
~~~
