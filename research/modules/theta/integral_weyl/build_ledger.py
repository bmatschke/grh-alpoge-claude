"""Regenerate exact pinned declaration records for IW1--IW7; no Lean build."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
assert subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() == PIN
BASE = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"
PW = "src/Formalism/ThetaLogCoordinates/TraceIsometryWeights/"
SP = PW + "SchurTraceProofs/"
SM = "src/Formalism/ThetaLogCoordinates/SandwichModelDomains/"
SMP = SM + "SandwichModelProofs/"
GW = "src/Formalism/GradedWeylDivisibility/"
FM = "src/Formalism/LocalToGlobal/GroupLattices/FockModels/"
TW = FM + "TransposeWords/"
TWP = TW + "TransposeWordsProofs/"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
DF = GB + "DualFockLinear/"
RW = GB + "RootWeights/"

# A record identifies a declaration, not an asserted complete Lean dependency closure.
# Human replacement arguments are identified explicitly in the claim descriptions.
specs = [
    ("IW1", PW+"DivStable.lean", "GlRel", "Exact gl commutator convention."),
    ("IW1", PW+"DivStable.lean", "Om", "Recursive Omega operator, identical to report."),
    ("IW1", PW+"DivStable.lean", "Pstep", "Exact factorial coefficient (-1)^q s!/((q+s)!q!)."),
    ("IW1", PW+"DivStable.lean", "InvOp", "Ordered recursion over distinct indices."),
    ("IW1", PW+"DivStable.lean", "DivStable", "Off-diagonal divided-power stability, not ordinary Lie stability alone."),
    ("IW1", SP+"InvInt.lean", "Om_eq_pow", "Commuting left-right operator expansion."),
    ("IW1", SP+"InvInt.lean", "Om_insert", "Binomial version of the multinomial expansion in the human proof."),
    ("IW1", SP+"InvInt.lean", "norm_pow_log_div_choose", "Exact logarithmic binomial valuation bound."),
    ("IW1", SP+"InvInt.lean", "Om_int", "Source induction on S; replaced by explicit multinomial coefficient factorization."),
    ("IW1", SP+"InvInt.lean", "Pstep_int", "One-step denominator cost."),
    ("IW1", SP+"InvInt.lean", "invariant_integral_holds", "Sum of step costs gives binom(k,2) Nat.log p(h+k-1)."),
    ("IW1", RW+"CasimirPowerScaledInsertDividedPower.lean", "factorial_ratio_choose_identity", "Parallel actual GrowthBounds denominator mechanism."),
    ("IW1", RW+"CasimirPowerScaledInsertDividedPower.lean", "scaled_casimirPower_integral_bound", "Parallel integral Casimir power bound over the source DVR."),
    ("IW1", RW+"CasimirPowerScaledInsertDividedPower.lean", "extremalProjector_denominator_bound", "Parallel one-step bound used by actual filtered projector route."),
    ("IW2", SP+"InvInv.lean", "Cj", "Auxiliary commutator operator in the detailed recurrence proof."),
    ("IW2", SP+"InvInv.lean", "Cj_E", "Commutator with a lowering root gives the factor 2."),
    ("IW2", SP+"InvInv.lean", "Om_E", "General Omega commutator identity."),
    ("IW2", SP+"InvInv.lean", "Om_vanish", "The right-hand lowering string passes beyond the diagonal weight bound."),
    ("IW2", SP+"InvInv.lean", "cc_rec", "Exact telescoping coefficient recurrence."),
    ("IW2", SP+"InvInv.lean", "E_Om_apply", "Specialized recurrence on gl(S)-invariant vectors."),
    ("IW2", SP+"InvInv.lean", "E_Pstep_apply", "Telescoping leaves a single last term."),
    ("IW2", SP+"InvInv.lean", "lower_kill", "Finite gl2 string argument kills the opposite root."),
    ("IW2", SP+"InvInv.lean", "Pstep_sub_mem", "Every correction belongs to a root-operator image."),
    ("IW2", SP+"InvInv.lean", "Pstep_inv", "One new index extends invariance."),
    ("IW2", SP+"InvInv.lean", "invariant_inverse_holds", "Induction gives invariance and correction in root images."),
    ("IW2", SP+"InvInv.lean", "invariant_natural_holds", "The explicit operator commutes with intertwiners."),
    ("IW2", SP+"SchurTraceOfHomInv.lean", "homInv_of", "Apply invariant operator to Hom action."),
    ("IW2", SP+"SchurTraceOfHomInv.lean", "schurTrace_of_homInv", "Trace/dimension identity on the split irreducible module."),
    ("IW3", GW+"StatementA.lean", "dualWeyl", "Actual invariant polynomial coefficient module."),
    ("IW3", GW+"StatementA.lean", "rowAct", "R(g)F(X)=F(gX), with substitution anti-action convention."),
    ("IW3", GW+"StatementA.lean", "rowDiv", "Hasse coefficient definition of integral divided powers."),
    ("IW3", GW+"StatementA.lean", "hw", "Product of principal minors with partition differences."),
    ("IW3", GW+"StatementA.lean", "weyl", "Actual span of all divided-power words on the highest polynomial."),
    ("IW3", SP+"WeylInt.lean", "topC", "Highest-weight projection used as an integral Hom-lattice element."),
    ("IW3", SP+"WeylInt.lean", "wl_key", "Invariant projection of topC is dimension inverse times inclusion."),
    ("IW3", SP+"WeylInt.lean", "weylInt_of", "Actual integral Weyl proof; multiply by integral dimension at end."),
    ("IW3", SP+"WeylInt.lean", "weyl_integral_holds", "Final abstract Weyl-integrality witness."),
    ("IW3", SMP+"GlFirstLineDividedPowers.lean", "gl_first_line_divided_powers", "Match row Hasse coefficients to infinitesimal divided powers."),
    ("IW3", SMP+"SwappedHighestWeightNeZero.lean", "cor_line", "Actual highest-line source statement; replaced by Gaussian proof for square models."),
    ("IW3", SMP+"SwappedHighestWeightNeZero.lean", "cor_gen", "Evaluation at the standard identity frame makes the highest scalar integral."),
    ("IW3", SMP+"SwappedHighestWeightNeZero.lean", "coreQp_of", "Apply abstract Weyl theorem to actual coefficient lattice."),
    ("IW3", SM+"StatementW.lean", "sExp", "Exact numerical exponent."),
    ("IW3", SM+"StatementW.lean", "LBound", "Top-bound or square spread-bound source alternative."),
    ("IW3", SM+"StatementW.lean", "SandwichModelLocal", "Exact local-domain integer-weight model statement."),
    ("IW3", SM+"FinalW.lean", "sandwichModelLocal", "Final source model sandwich; our proof works directly over the DVR."),
    ("IW4", SP+"TypeInt.lean", "pr0", "Weight-zero projection on Hom."),
    ("IW4", SP+"TypeInt.lean", "weightZeroProj_mem_homLat", "Graded integral lattices make weight-zero projection integral."),
    ("IW4", SP+"TypeInt.lean", "weightZeroProj_trace", "Weight-zero projection preserves trace."),
    ("IW4", SP+"TypeInt.lean", "Psi", "Averaging after the weight-zero projection."),
    ("IW4", SP+"TypeInt.lean", "QQ", "Exact d sum_i A(u_i^* tensor y)(u_i) isotypic formula."),
    ("IW4", SP+"TypeInt.lean", "QQ_zero", "Averaging gives zero on inequivalent types."),
    ("IW4", SP+"TypeInt.lean", "QQ_id", "Naturality and trace show identity on equivalent copies."),
    ("IW4", SP+"TypeInt.lean", "QQ_int", "Isotypic projector inherits the single invariant-operator denominator."),
    ("IW4", SP+"TypeInt.lean", "typeInt_of", "Final projector statement with exact lattice hypotheses."),
    ("IW4", RW+"LatticeTheoremSingleRepLinf.lean", "isotypicProjectorTheoremField_of_linfty_bound", "Parallel actual GrowthBounds isotypic theorem."),
    ("IW4", RW+"DenominatorLemmaWithoutProjector.lean", "linf_lemma_without_projector", "Actual generic invariant denominator route."),
    ("IW4", RW+"PolynomialIsotypicLatticeOfParts.lean", "polynomial_isotypic_lattice_of_parts", "Nested/disjoint commutation, Fock adjointness and integral coefficient/BB assembly."),
    ("IW4", RW+"IntegralPolynomialsEnvelopingStable.lean", "integral_polynomials_enveloping_stable", "Actual integral and BB lattice stability; elementary BB specialization in companion."),
    ("IW4", GB+"CovariantDegrees.lean", "FilteredProjectorCorollaryField", "Exact joint-projector exponent sum binom(k,2) Nat.log p(2degIn+k-1)."),
    ("IW4", GB+"GLWeightTheory.lean", "filtered_projector_corollary_field", "Actual exported filtered projector witness."),
    ("IW4", GB+"Lemma5aAt.lean", "FockProjectorAtRing", "Actual constrained-test projector interface, including BB valuation and commutation."),
    ("IW4", GB+"ProjectionOfIsotypicDecomposition.lean", "projection_at_of_isotypic", "Actual passage to a cutoff on the last highest-weight entry."),
    ("IW5", TW+"FockR.lean", "fockR", "Actual symmetric bilinear monomial-factorial pairing."),
    ("IW5", TWP+"ProdBlockEmbMonomial.lean", "highest_weight_norm", "Positive integer N=Fock(H,H); the normalization is not arbitrary."),
    ("IW5", TWP+"FockPairingDividedAdjoint.lean", "fock_pairing_divided_adjoint", "Integral divided-power transpose adjointness."),
    ("IW5", TWP+"FockPairingDividedAdjoint.lean", "fock_pairing_word_adjoint", "Reverse-transposed words are adjoints."),
    ("IW5", TWP+"FockPairingHighestWeightProof.lean", "eval_idFrame_hw", "Exact normalization H(I)=1."),
    ("IW5", TWP+"FockPairingHighestWeightProof.lean", "fock_pairing_highest_weight_proof", "B(H,Q)=Q(I); new reproducing identity follows by row adjointness."),
    ("IW5", TWP+"WeylFormNondegenerateGlobal.lean", "weylPair_of", "Integral pairing of Delta with the coefficient lattice."),
    ("IW5", TWP+"WeylFormNondegenerateGlobal.lean", "dualWeylIn_of", "Exact source converse; its coefficient/leading-term route is replaced by the Gaussian-content proof."),
    ("IW5", TWP+"WeylFormNondegenerateGlobal.lean", "nondegK_of", "Source nondegeneracy statement; follows directly from the new reproducing identity."),
    ("IW5", DF+"FormCoreSKXOf.lean", "formCoreGX_of", "Actual B=Fock/N and normalized integral sandwich."),
    ("IW5", DF+"FormCoreSKXOf.lean", "FormCoreSKX", "Exact square polynomial form interface used by the cloud construction."),
    ("IW5", DF+"FormCoreSKXOf.lean", "formCoreSKX_of", "Normalized integer weights and the zero-spread exponent-zero branch."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "lamAt", "Even weights and odd negative reversed weights."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "nuOf", "Subtract the last integer weight before polynomial realization."),
    ("IW6", GW+"StatementD.lean", "nablaL", "Actual coefficient lattice is a COMAP under R(A), hence the image under R(A inverse)."),
    ("IW6", GW+"StatementD.lean", "nablaLTw", "Actual determinant scalar is det(A)^(-lambda_k), not its positive power."),
    ("IW6", GW+"StatementD.lean", "NablaLTwMem", "Equivalent membership test det(A)^(lambda_k)R(A)F in the integral coefficient lattice."),
    ("IW6", GW+"FockSpaceTableaux/NablaLTwMem.lean", "nabla_twist_mem", "Proof of the exact source comap/twist convention."),
    ("IW6", FM+"TestSideDef.lean", "expN", "Individual logarithmic exponent, with zero-spread branch."),
    ("IW6", GB+"ObjBridge.lean", "kap1", "Actual sum of position-wise exponents."),
    ("IW6", DF+"JetMatrixAlgebra.lean", "posCore_of_formX", "Actual single-factor determinant-twist and inverse-transpose transport."),
    ("IW6", DF+"JetMatrixAlgebra.lean", "ten_sideX", "Tensor pairing and product scalar normalization."),
    ("IW6", DF+"JetMatrixAlgebra.lean", "test_side_explicit_identification", "Actual vertex and edge transfer to RestTSX."),
    ("IW6", DF+"BaseMatrixAlgebra.lean", "RestTSX", "Exact common scalar times full Fock identity required downstream."),
    ("IW6", DF+"RestCloudBOfThree.lean", "TSProp", "Exact vertex and edge lattice sandwich interface."),
    ("IW6", FM+"TestSideEdge.lean", "latDual_colSpan", "Dual underlying lattice has inverse-transposed basis."),
    ("IW6", FM+"TestSideEdge.lean", "invT_mul_D", "Elementary diagonal midpoint inverse-transpose identity."),
    ("IW6", FM+"TestSideEdge.lean", "dual_edgeBasis", "Actual reversed dual edge basis includes diag(p I_r,I)."),
    ("IW6", DF+"LaTwInvT.lean", "dualM", "w^2=p identifies opposite midpoint with inverse transpose."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "HLe", "Tensor midpoint lattice."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "Ar", "Exact edge normalization exponent."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "Re", "Primal edge scale w^(-Ar)."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "Re'", "Dual-side edge uses the same scale w^(-Ar)."),
    ("IW6", GB+"UnramifiedQuadraticSetting.lean", "be", "Actual edge evaluation pairing multiplies by p^Ar."),
    ("IW7", DF+"LogSizeBoundLe.lean", "log_size_bound_le", "Source single-family coarse bound 2Nk^2 log_p(a)."),
    ("IW7", DF+"LogSizeBoundLe.lean", "sizeStep", "Actual top/flat shape hypotheses imply two-family cost <=4Nk^2 log_p(a)."),
    ("IW7", DF+"LogSizeBoundLe.lean", "restSize", "Pinned witness Ckappa=4."),
]

decl_re = re.compile(r"^(?:(?:private|protected|noncomputable)\s+)?(?:theorem|lemma|def|abbrev|structure|instance)\b")
stop_re = re.compile(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|open\s|include\s|omit\s|attribute\s|set_option\s|noncomputable\s+section)")
entries = []
for claim, path, name, role in specs:
    data = (ROOT/path).read_bytes()
    lines = data.decode().splitlines()
    name_re = re.compile(r"^(?:(?:private|protected|noncomputable)\s+)?(?:theorem|lemma|def|abbrev|structure)\s+" + re.escape(name) + r"(?=\s|:|\{|\()")
    starts = [i for i, line in enumerate(lines) if name_re.search(line)]
    if len(starts) != 1:
        raise ValueError((path, name, starts))
    start = starts[0]
    end = next((i for i in range(start+1, len(lines)) if decl_re.search(lines[i]) or stop_re.search(lines[i])), len(lines))
    while end > start+1 and not lines[end-1].strip():
        end -= 1
    body = "\n".join(lines[start:end]) + "\n"
    entries.append({
        "claim_id": claim,
        "source_path": path,
        "declaration_as_spelled": name,
        "line_start": start+1,
        "line_end": end,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "range_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "pinned_url": BASE+path+f"#L{start+1}-L{end}",
        "role": role,
        "first_line": lines[start],
    })

claims = [
    {"id":"IW1", "result":"p^D I_h preserves any root-divided-power-stable O-module, D=binom(k,2)floor(log_p(h+k-1)).", "status":"Proved by explicit multinomial expansion and Legendre's formula; direct general DVR proof."},
    {"id":"IW2", "result":"I_h takes weight zero to invariants, is natural, and preserves trace on End(U).", "status":"Proved by commutator recurrence, telescoping, weight cutoff, and finite gl2 strings. No unexpanded projector formula."},
    {"id":"IW3", "result":"For the actual square polynomial lattice, p^D nabla subset Delta subset nabla, with exponent zero at zero spread.", "status":"Proved from IW1/IW2 applied to highest projection in Hom(nabla,Delta), using explicitly stated classical characteristic-zero GL background."},
    {"id":"IW4", "result":"Any isotypic projector e preserves a graded divided-power-stable lattice after multiplying by p^D.", "status":"Proved by exact rank-one Hom averaging formula. h bounds same-coordinate differences of TWO V weights, not within-weight spread. BB specialization and projector commutation in companion."},
    {"id":"IW5", "result":"B=Fock/Fock(H,H), B(R(g^t)H,Q)=Q(g), Delta^#=nabla and nabla^#=Delta.", "status":"New elementary square-model proof: Gaussian recovery and primitive polynomial content replace the source integral standard-monomial/coefficient-word route."},
    {"id":"IW6", "result":"Actual normalized tensor form gives p^kappa L(A^-t) subset Psi(L(A)^*) subset L(A^-t), including correctly scaled opposite edge lattices.", "status":"Proved by inverse-transpose adjointness, determinant cancellation, tensor dual bases and w^2=p midpoint identity. Exact be pairing factor p^Ar retained."},
    {"id":"IW7", "result":"h_s+k<=a^2 implies source two-family kappa<=4Nk^2 log_p a.", "status":"Elementary bound proves the sharper 2Nk(k-1)log_p a; assembled source constant 4 is retained."},
]
ledger = {
    "title":"IW1--IW7: actual integral Weyl/Fock comparison and shared projector denominator",
    "date":"2026-11-21",
    "source_commit":PIN,
    "source_root":str(ROOT),
    "status":"Human mathematical reconstruction with exact pinned source records; no Lean build, whole-proof verification, or signed path-basis reconstruction claimed.",
    "claims":claims,
    "classical_field_background":["Finite-dimensional rational representations of split GL_k in characteristic zero are completely reducible.", "Every nonzero irreducible has a highest vector; PBW generation implies weight dominance.", "The relevant modules are split; a commuting endomorphism is scalar on its highest line and hence on the cyclic irreducible."],
    "main_formulae":{
        "step":"P_(S,z,h)=sum_(q=0)^h (-1)^q s!/((q+s)!q!)*Omega_q",
        "omega":"Omega_0=1; Omega_(q+1)=sum_(i in S)E_zi Omega_q E_iz",
        "denominator":"D=binom(k,2)floor(log_p(h+k-1)); zero at k=1 or normalized spread h=0",
        "projector":"e_U(y)=dim(U)*sum_i A(u_i^* tensor y)(u_i), A=I_h after weight-zero projection",
        "normalization":"B(P,Q)=sum_alpha P_alpha Q_alpha alpha! / sum_alpha H_alpha^2 alpha!",
        "reproduction":"B(R(g^t)H,Q)=Q(g), R(g)P(X)=P(gX)",
        "duality":"Delta^#=nabla, nabla^#=Delta, p^D nabla subset nabla^# subset nabla",
        "tensor":"kappa=sum_(s:h_s>0)binom(k,2)floor(log_p(h_s+k-1))",
        "basis_convention":"L_lambda(A)=det(A)^(-lambda_k)*R(A inverse)*nabla; equivalent membership det(A)^(lambda_k)*R(A)F in nabla",
        "edge":"R_e=w^(-Ar)H_e; R'_e=w^(-Ar)H_e^*; be(u,T)=T(p^Ar*u)",
        "projector_application":"h=2degIn(d,S) gives source denominator binom(k,2)floor(log_p(2degIn(d,S)+k-1))",
    },
    "remaining_separate_inputs":["Integral Cartan multiplication and complementary semistandard family outside the square Fock comparison.", "Signed path-column integral basis and geometric realization of tests.", "Arithmetic and cohomological window inputs for RH/Dirichlet GRH."],
    "source_entries":entries,
    "artifact_sha256":{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ["integral_weyl_section.tex","report.txt","build_ledger.py"]},
}
(HERE/"provenance.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False)+"\n")
print(f"Wrote {len(entries)} pinned declaration records for {len(claims)} claims.")
