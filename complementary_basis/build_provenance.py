"""Regenerate exact pinned declaration records for CB1--CB7; no Lean build."""
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
GW = "src/Formalism/GradedWeylDivisibility/"
FT = GW + "FockSpaceTableaux/"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
DF = GB + "DualFockLinear/"
SE = GB + "ScaleEdges/"
FM = "src/Formalism/LocalToGlobal/GroupLattices/FockModels/"
PD = "src/Formalism/PeriodIntegrals/AdmissibleModel/"
TL = "src/Formalism/ThetaLogCoordinates/"

# Each record identifies its exact statement/proof, not a claimed complete
# dependency closure. Human replacements and previous-section boundaries are
# distinguished in the role text and claim statuses below.
specs = [
    ("CB1", GW+"StatementA.lean", "colW", "Exact column multigrading."),
    ("CB1", GW+"StatementA.lean", "colAddGen", "Generic polynomial column addition, including the new parameter."),
    ("CB1", GW+"StatementA.lean", "dualWeyl", "Actual coefficient lattice: multidegree intersected with kernels of generic additions."),
    ("CB1", GW+"StatementC.lean", "cmIdx", "Column-first then row variable order."),
    ("CB1", GW+"StatementC.lean", "colLex", "Actual monomial order."),
    ("CB1", GW+"StatementC.lean", "InterlacedAt", "Cumulative inequality with degree allowance s."),
    ("CB1", GW+"StatementC.lean", "Interlaced", "Adjacent-column zero-allowance inequalities."),
    ("CB1", FT+"CompDeg.lean", "componentDegree", "Merged-pair grading preserves the generic-parameter degree bound."),
    ("CB1", FT+"LeadComp.lean", "leadingComponent", "The homogeneous component selected by the leading exponent has the same leading monomial."),
    ("CB1", FT+"PeelDecomp.lean", "peelDecomposition", "First-row homogeneous expansion."),
    ("CB1", FT+"PeelLead.lean", "sliceLeading", "Largest x exponent gives the first-row leading monomial."),
    ("CB1", FT+"PeelDegBound.lean", "le_and_degreeOf_top_le_of_degreeOf_sum_le", "Source x=1,y=-t specialization and degree estimate; reconstructed explicitly."),
    ("CB1", FT+"PeelDegBound.lean", "peelDegBound_of", "Exact e<=s and remaining degree <=s-e+K interface."),
    ("CB1", FT+"TwoColumn.lean", "lctwo_main", "Row induction proving cumulative leading-exponent inequalities."),
    ("CB1", FT+"TwoColumn.lean", "twoColumn_of", "Full two-column interface."),
    ("CB1", FT+"LeadInterlaced.lean", "leadInterlaced_of", "Apply degree zero to the actual generic invariants."),
    ("CB1", GW+"FinalC.lean", "leadInterlaced", "Exported source witness."),
    ("CB2", GW+"StatementA.lean", "initMinor", "Initial-column determinant, including row-list convention."),
    ("CB2", GW+"StatementA.lean", "bideterminant", "Product of initial-column minors."),
    ("CB2", GW+"StatementA.lean", "shapeDeg", "Column degree counted by minor heights."),
    ("CB2", GW+"StatementD.lean", "ssIdx", "Exact exponent-array basis index set."),
    ("CB2", GW+"StatementD.lean", "IsWeightBasis", "Integral independence, spanning and row-weight homogeneity."),
    ("CB2", GW+"StatementD.lean", "SSBasis", "Actual existential monic minor-product basis interface."),
    ("CB2", FT+"ColLexInitMinor.lean", "colLexInitMinor_of", "Monic diagonal leading term of an increasing-row minor."),
    ("CB2", FT+"ColumnLexBideterminant.lean", "columnLexBideterminant_of_initialMinor", "Leading terms multiply without coefficient division."),
    ("CB2", FT+"SSYTPeel.lean", "semistandardPeel", "Source constructive tableau existence; replaced by sorting the rows of the array."),
    ("CB2", FT+"SSYTExists.lean", "sSYTExists_of", "Existence of a minor product with prescribed interlaced leading exponent."),
    ("CB2", FT+"SMSAssembly.lean", "semistandard_module_assembly", "Integral leading-term subtraction proving spanning."),
    ("CB2", GW+"FinalC.lean", "standardMonomialSpanDomain", "Exported all-domain minor-product span."),
    ("CB2", FT+"SSBasis.lean", "semistandard_basis", "Exact integral basis proof and row homogeneity."),
    ("CB2", GW+"FinalD.lean", "sSBasis", "Exported source basis witness."),
    ("CB2", GW+"StatementD.lean", "tensorLat", "Actual tensor lattice embedded as products in disjoint polynomial blocks."),
    ("CB2", FT+"TensorBasis.lean", "tensor_power_basis", "Source tensor-basis theorem; monic block products give the needed specialization directly."),
    ("CB3", PD+"WeylDim.lean", "Intl", "Array interlacing in curried indexing."),
    ("CB3", PD+"WeylDim.lean", "SSZ", "Integer-shape version of the finite array set."),
    ("CB3", TL+"JacobiPathWeights/StatementP.lean", "gtBox", "Exact inclusive interlacing ranges."),
    ("CB3", TL+"JacobiPathWeights/StatementP.lean", "dGT", "Recursive finite Gelfand--Tsetlin count."),
    ("CB3", PD+"WeylDim.lean", "card_SSZ", "Removing the last symbol gives the source count recurrence."),
    ("CB3", PD+"WeylDim.lean", "card_ssIdx", "Exact identification with the source basis index set."),
    ("CB3", PD+"WeylDim.lean", "finrank_dualWeyl", "Basis count equals the actual coefficient-module dimension over every field."),
    ("CB3", PD+"WeylDim.lean", "weylQ", "Weyl product endpoint; CB proves it by an explicit discrete Vandermonde determinant."),
    ("CB3", TL+"ResidueClassEstimates/FinalT.lean", "weylGT", "Source count/product endpoint, not an unexpanded input to CB."),
    ("CB3", GB+"UnramifiedQuadraticSetting.lean", "lamAt", "Actual even and odd negative-reversed effective weights."),
    ("CB3", GB+"UnramifiedQuadraticSetting.lean", "nuOf", "Normalize a dominant integer tuple by subtracting its last entry."),
    ("CB3", GB+"UnramifiedQuadraticSetting.lean", "Vsp", "Actual product polynomial module whose dimension is computed."),
    ("CB3", GB+"UnramifiedQuadraticSetting.lean", "dimV", "Actual finrank used downstream."),
    ("CB3", GB+"TableLineDegreeFive.lean", "FewBadOrbits", "Exactly the product dimension formula; CB discharges this interface, not selected-symbol density."),
    ("CB4", SE+"SymbolRealisableBound.lean", "dT", "Selected flat degree and zero off the selected set."),
    ("CB4", SE+"SymbolRealisableBound.lean", "restW", "Exact residual weight lambda0-flW(dT)."),
    ("CB4", DF+"IsMultiHom.lean", "Xs", "Actual selected exponent-array restrictions in both parities."),
    ("CB4", DF+"IsMultiHom.lean", "CntTop", "Selected-position count interface."),
    ("CB4", DF+"IsMultiHom.lean", "CntSpec", "Unselected-position count interface."),
    ("CB4", DF+"TestSideCounting.lean", "TX", "Curried arrays with the selected restrictions."),
    ("CB4", DF+"TestSideCounting.lean", "TN", "Smaller unselected array module."),
    ("CB4", DF+"TestSideCounting.lean", "equivE", "Delete/insert first row and first column at an even selected position."),
    ("CB4", DF+"TestSideCounting.lean", "equivO", "Delete/insert first row and last column at an odd selected position."),
    ("CB4", DF+"TestSideCounting.lean", "cntSpec", "Unselected count and shift invariance."),
    ("CB4", DF+"TestSideCounting.lean", "cntTop", "Exact tail count in both parities."),
    ("CB4", DF+"TestSideCounting.lean", "card_all", "Full complementary tensor cardinality."),
    ("CB4", SE+"RemainingWeightVectorCount.lean", "remainingWeightVectorCount", "Exact rational expression n2."),
    ("CB4", DF+"TheoremIIClosedOfTestBound.lean", "primStep_of", "Actual bX/sO selected-family construction and source primitive-combination assembly; latter also uses separate CL inputs."),
    ("CB5", GB+"TableLineDegreeFive.lean", "WeightHyp", "Exact tail/first-gap hypotheses used to derive d>=a and delta<=c0."),
    ("CB5", GB+"UnramifiedQuadraticSetting.lean", "IsBaseWeight", "Base endpoints and cpp bounds on interior weights."),
    ("CB5", SE+"GainBoundAt.lean", "flatDeg_bounds", "Source first-gap lower bound a<=d, independently immediate from WeightHyp here."),
    ("CB5", SE+"WeylDimShift.lean", "weylDim_cons_le_choose_mul", "Source looser k*c0/a comparison; CB derives an exact ratio and (k-1)*c0/a bound."),
    ("CB5", SE+"RemainingWeightVectorCount.lean", "dimV_eq", "Dimension formula in the original base weights, after parity invariance."),
    ("CB5", SE+"RemainingWeightVectorCount.lean", "top_count", "Actual one-position source count inequality."),
    ("CB5", SE+"RemainingWeightVectorCount.lean", "count_of_exact", "Actual product inequality; source requires nonnegative common lower factor."),
    ("CB6", FM+"Cartan.lean", "ProdSpan", "Exact integral multiplication span."),
    ("CB6", FM+"Cartan.lean", "bidet_mem_prod", "Source splitting of minor factors; CB groups them directly by height."),
    ("CB6", FM+"Cartan.lean", "dualWeyl_le_prod", "Integral onto for normalized polynomial partitions."),
    ("CB6", FM+"Cartan.lean", "cartanOnto_proved", "Source integral Cartan product after signed weight/basis transport."),
    ("CB6", FM+"Cartan.lean", "cartanDomain_proved", "Primitive-product assertion from prime coefficient reduction and saturation."),
    ("CB6", GB+"ProjectionLemmaBaseLevel.lean", "CartanDomain", "Exact DVR primitive-product interface."),
    ("CB6", GB+"ProjectionLemmaBaseLevel.lean", "CartanOnto", "Exact source integral, not merely generic-fibre, surjectivity statement."),
    ("CB6", FT+"DualWeylSat.lean", "dualWeylModuleSaturated", "Coefficient divisibility is lattice divisibility."),
    ("CB7", GW+"StatementA.lean", "rowAct", "Row substitution anti-action convention."),
    ("CB7", GW+"StatementD.lean", "nablaL", "Comap under rowAct(M), hence image under rowAct(M inverse)."),
    ("CB7", GW+"StatementD.lean", "nablaLTw", "Correct scalar det(M)^(-lambda_last)."),
    ("CB7", FT+"NablaLTwMem.lean", "nabla_twist_mem", "Equivalent membership condition with positive determinant exponent and rowAct(M)."),
    ("CB7", GW+"StatementD.lean", "NablaLBasis", "Actual transported integral basis interface."),
    ("CB7", GW+"StatementD.lean", "NablaLKBasis", "The same transported basis spans the actual generic-fibre coefficient module."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "H0", "Source intersection over all basis presentations."),
    ("CB7", GB+"LatticeSystems.lean", "la_indep", "Source basis-independence witness; elementary GL(O) proof repeated in CB."),
    ("CB7", GB+"LatticeSystems.lean", "H0_eq_twisted_nabla", "Actual H0 identification, now with the explicit basis-independence proof."),
    ("CB7", GB+"LatticeSystems.lean", "la_basis", "Source integral and generic-fibre transported monic basis."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "Hten", "Actual effective-weight tensor lattice."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "LeAt", "Source midpoint lattice; its explicit basis was established in EL."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "HLe", "Actual tensor lattice at midpoint."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "Ar", "Signed additive edge exponent."),
    ("CB7", GB+"UnramifiedQuadraticSetting.lean", "Re", "Actual source edge lattice w^(-Ar)HLe."),
    ("CB7", FM+"FlatModels/EdgeLatOfG.lean", "edgeLat_of", "Exact actual-edge midpoint matrices, supplied by the previous EL proof."),
    ("CB7", DF+"OneSidedLemma4.lean", "tr_tens_int", "Forward coefficient map on the actual tensor lattice."),
    ("CB7", DF+"OneSidedLemma4.lean", "tr_tens_lift", "Inverse coefficient map; CB gives its explicit basis-vector formula."),
    ("CB7", DF+"TransStep.lean", "transStep", "Actual sh_i construction, signed determinant factors and primitive-coordinate transfer."),
    ("CB7", DF+"RestCloudBOfThree.lean", "OntoAll", "Exact edge Cartan span needed by the contraction argument."),
    ("CB7", DF+"RestCloudBOfTwo.lean", "tensor_onto", "Finite distributivity of local product spans; proved directly in CB."),
    ("CB7", DF+"RestCloudBOfTwo.lean", "ontoAll", "Actual final integral edge-product witness."),
]

decl_re = re.compile(r"^(?:(?:private|protected|noncomputable)\s+)?(?:theorem|lemma|def|abbrev|structure|instance)\b")
stop_re = re.compile(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|open\s|include\s|omit\s|attribute\s|set_option\s|noncomputable\s+section)")
entries = []
for claim, path, name, role in specs:
    data = (ROOT/path).read_bytes()
    raw_lines = data.splitlines(keepends=True)
    lines = [line.decode().rstrip("\r\n") for line in raw_lines]
    name_re = re.compile(r"^(?:(?:private|protected|noncomputable)\s+)?(?:theorem|lemma|def|abbrev|structure)\s+" + re.escape(name) + r"(?=\s|:|\{|\()")
    starts = [i for i,line in enumerate(lines) if name_re.search(line)]
    if len(starts) != 1:
        raise ValueError((path,name,starts))
    start = starts[0]
    end = next((i for i in range(start+1,len(lines)) if decl_re.search(lines[i]) or stop_re.search(lines[i])),len(lines))
    while end>start+1 and not lines[end-1].strip():
        end -= 1
    body = b"".join(raw_lines[start:end])
    byte_start = sum(map(len,raw_lines[:start]))
    entries.append({
        "claim_id":claim,
        "source_path":path,
        "declaration_as_spelled":name,
        "line_start":start+1,
        "line_end":end,
        "byte_start":byte_start,
        "byte_end_exclusive":byte_start+len(body),
        "source_sha256":hashlib.sha256(data).hexdigest(),
        "range_sha256":hashlib.sha256(body).hexdigest(),
        "pinned_url":BASE+path+f"#L{start+1}-L{end}",
        "role":role,
        "first_line":lines[start],
    })

claims = [
    {"id":"CB1","result":"Generic column-invariant polynomials have interlaced column-lex leading exponent arrays.","status":"Proved over every integral domain by merged-pair grading, the x=1,y=-t specialization and row induction."},
    {"id":"CB2","result":"The actual dualWeyl module has a monic minor-product integral basis indexed by ssIdx, homogeneous in row weights and valid over every domain.","status":"Proved constructively by sorted tableau rows, diagonal leading terms and terminating integral leading-term subtraction; no standard-monomial theorem imported."},
    {"id":"CB3","result":"#ssIdx=D_k(lambda), and dimV equals the product of D_k over positions, discharging FewBadOrbits.","status":"Proved by removing the largest entry and an explicit discrete Vandermonde determinant identity. Distinct from selected-symbol density."},
    {"id":"CB4","result":"The actual even/odd selected array family has count n2=product_T D_(k-1)(tail) product_notT D_k(lambda0).","status":"Proved by explicit delete/insert bijections and parity/shift invariance; selected tensor products form a direct summand."},
    {"id":"CB5","result":"Exact complementary dimension ratio gives source top_count and count_of_exact under WeightHyp and nonnegative product factor.","status":"Proved by the explicit product ratio and product(1-u)>=1-sum u; a slightly sharper k-1 local cost is recorded but the source k is retained downstream."},
    {"id":"CB6","result":"Integral Cartan multiplication spans nabla_(nu+mu); primitive factors have primitive product over a DVR.","status":"Proved by partitioning minor factors of each height and by saturated coefficient reduction. No field-only surjectivity substituted."},
    {"id":"CB7","result":"The bases, complementary family and Cartan span transport to the exact H0/Hten/Re lattices, with inverse-basis, signed determinant and w^(-Ar) conventions.","status":"Proved using the explicit coordinate isomorphism and additivity; actual midpoint matrices supplied by the prior EL argument. Exact source OntoAll is obtained."},
]
ledger = {
    "title":"CB1--CB7: actual complementary integral basis, count and Cartan multiplication",
    "date":"2026-11-21",
    "source_commit":PIN,
    "source_root":str(ROOT),
    "status":"Human mathematical reconstruction with exact pinned source records; no Lean build or whole-proof verification claim.",
    "claims":claims,
    "source_entries":entries,
    "range_hash_convention":"SHA-256 of the exact source bytes spanning the inclusive line range; byte offsets are zero-based and the end is exclusive.",
    "main_formulae":{
        "interlacing":"sum_(b<=a)e_(b,j)<=sum_(b<a)e_(b,j-1)",
        "degree_allowance":"deg_t f(x,y+t*x)<=s => sum_(i<=q)b_i<=s+sum_(i<q)a_i",
        "basis":"b_e=product_(tableau columns c)det X_(entries(c),[1,height(c)])",
        "dimension":"D_k(lambda)=product_(i<j)(lambda_i-lambda_j+j-i)/(j-i)",
        "vandermonde":"sum_(x_(i+1)<=y_i<x_i)Delta(y)=Delta(x)/(k-1)!",
        "complement":"n2=product_(s in T)D_(k-1)(tail(lambda0_s))*product_(s notin T)D_k(lambda0_s)",
        "ratio":"binom(d+k-1,k-1)*D_(k-1)(tail)/D_k(lambda)=product_(j=2)^k(d+j-1)/(d+lambda_2-lambda_j+j-1)",
        "source_count":"(1-k*c0/a)^|T| dimV <= product_(s in T)binom(d_s+k-1,k-1)*n2, assuming k*c0/a<=1",
        "cartan":"nabla_(nu+mu)=span{f*g:f in nabla_nu,g in nabla_mu}",
        "lattice":"L_lambda(M)=det(M)^(-lambda_k)*rowAct(M inverse)*nabla_(lambda-lambda_k)",
        "edge_coordinates":"C_lambda(F)=w^Ar*product_s det(M_s)^(lambda_eff_s,k)*blockAct(M_s)F",
    },
    "previous_proved_inputs":[
        "EL midpoint matrices and the local coefficient-lattice model.",
        "CL2--CL3 additional product-family exponent injection and primitive-combination argument; CB supplies its basis hypothesis.",
        "IW normalized Fock duality and denominator sandwich are separate previously proved claims."
    ],
    "remaining_separate_inputs":[
        "The distinct incoming argument is proved by IN/WT: initial Lemma5aAt via blocked MemAtB/PlanePairsOnBlocksAt and rest5aMono_of_cut, then WordConditionAt via OneOpStep/WordBoundStep. The stronger Lemma5aGeneratorProductsAt is not the instantiated initial route.",
        "Quantitative dimension/saturation of the selected symbol space and simultaneous frame/size hypotheses; different from n2 and FewBadOrbits.",
        "Global arithmetic/cohomological windows and the separately recorded geometric/spectral estimates."
    ],
    "artifact_sha256":{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ["complementary_basis_section.tex","report.txt","build_provenance.py"]},
}
(HERE/"provenance.json").write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+"\n")
print(f"Wrote {len(entries)} exact pinned declaration records for {len(claims)} claims.")
