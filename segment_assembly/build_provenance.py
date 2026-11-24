"""Regenerate LA1--LA6 exact pinned declaration records; no Lean build."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
ROOT = WORK / "alpoge-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
assert subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() == PIN
BASE = "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
SD = GB + "SegmentDegree/"

# These are exact source-object and proof locators, not a claim that this list
# is a transitive Lean dependency closure. The mathematical replacements and
# shared reconstructed inputs are distinguished in each claim's status.
specs = [
    ("LA1", SD+"NonemptyDvrSettingOfStandard.lean", "Dat", "Exact original parameter data."),
    ("LA1", SD+"NonemptyDvrSettingOfStandard.lean", "Hyp", "Literal complete hypothesis list preserved at the RestLam endpoint."),
    ("LA1", GB+"SegRing.lean", "posOf", "Residue position convention for integer letters."),
    ("LA1", GB+"SegRing.lean", "Frames", "Periodic selected-frame datum."),
    ("LA1", GB+"SegRing.lean", "letters", "Actual inclusive full segment interval."),
    ("LA1", GB+"SegRing.lean", "IsW", "Old-frame cut at the previous last frame letter."),
    ("LA1", GB+"SegRing.lean", "LLset", "Actual open interval of intermediate selected letters."),
    ("LA1", GB+"SegRing.lean", "Valid", "Exact periodicity, ordering, selected-frame gaps and remaining validity conditions."),
    ("LA1", SD+"Coarse.lean", "toLate", "Actual late-letter finite set."),
    ("LA1", SD+"LamImgApply.lean", "LamGeo", "Four exact geometry/scale/coverage conditions reconstructed in LA1--LA2."),
    ("LA1", SD+"LamImgApply.lean", "RestLamGeo", "Quantified source geometry interface."),
    ("LA1", SD+"LamMZero.lean", "lam_W_late", "Old selected letters are previous-frame entries and are late in the previous segment."),
    ("LA1", SD+"LamMZero.lean", "eq_of_mod_eq_of_mem_Ioc_fr_last", "Source one-period uniqueness; replaced by the half-open interval partition proof."),
    ("LA1", SD+"LamMZero.lean", "restLamGeo", "Exact source endpoint, including the wraparound old/late overlap."),
    ("LA1", SD+"SumPosOfPer.lean", "mem_late_iff", "Late letters equal selected letters in (z_(j-1),z_j]."),
    ("LA1", SD+"SumPosOfPer.lean", "prod_tiling", "Source periodic selected-position tiling witness."),
    ("LA2", GB+"SegRing.lean", "dist", "Natural conversion of last-frame minus letter distance."),
    ("LA2", SD+"Coarse.lean", "Rj", "Exact coarse integer logarithm of a natural floor."),
    ("LA2", SD+"Coarse.lean", "Qc", "Actual positive-part exponent of the adjacent coarse scale."),
    ("LA2", SD+"RestCountOf.lean", "Pz", "Exact monomial substitution power."),
    ("LA2", SD+"LamMZero.lean", "nat_log_div_pow_eq_sub", "Integer logarithm under division by a power; explicitly proved in LA2."),
    ("LA2", SD+"LamMZero.lean", "Rj_eq_log_floor", "Source common-cutoff expression; converted in LA2 to A_j=max(z_j,H+s_j)."),
    ("LA2", SD+"LamMZero.lean", "Pz_eq_Pz_mul_Qc", "Exact source overlap-scale conclusion; follows directly from the max formula."),
    ("LA2", SD+"FrameZeroStrictMono.lean", "sum_PzQc", "Adjacent-scale identity for all x<=z_j."),
    ("LA2", SD+"FrameZeroStrictMono.lean", "sum_prodQ", "Exact product of coarse radices p^n'."),
    ("LA2", SD+"SumPosOfPer.lean", "sum_Rj_per", "Coarse exponent periodicity."),
    ("LA2", SD+"SumPosOfPer.lean", "sum_Pz_per", "Simultaneous letter/segment-shift invariance."),
    ("LA2", SD+"SumPosOfPer.lean", "sum_Qc_per", "Adjacent radix periodicity."),
    ("LA3", GB+"SegRing.lean", "plEmb", "Plane-coordinate embedding."),
    ("LA3", GB+"SegRing.lean", "nmEmb", "Normal-coordinate embedding."),
    ("LA3", GB+"SegRing.lean", "ordDeg", "Parity-dependent order support restriction."),
    ("LA3", GB+"SegRing.lean", "XX'", "Literal separated-pair span intersected with order support bounds."),
    ("LA3", GB+"ValuationLowestDegreeRename.lean", "segN", "Segment cardinal used in the dimensional hypothesis."),
    ("LA3", GB+"ValuationLowestDegreeRename.lean", "segE", "Increasing enumeration of actual segment letters."),
    ("LA3", GB+"ValuationLowestDegreeRename.lean", "segRen", "Injective variable renaming into integer letters."),
    ("LA3", GB+"ValuationLowestDegreeRename.lean", "segPairs", "Exact allowed paired paths and prefix/order inequalities used by shared CG1."),
    ("LA3", GB+"ValuationLowestDegreeRename.lean", "NestedTypeBound", "Exact six-clause interface; LA uses only actual path identification and saturation, not its characteristic-zero isotypic clause."),
    ("LA3", GB+"ValuationLowestDegreeMapFractionField.lean", "first_clause_segment_rename", "Source actual XX' paired-path-span identification, proved in shared CG1 using IP3--IP4."),
    ("LA3", GB+"ValuationLowestDegreeMapFractionField.lean", "space_statement_saturated", "Source actual saturation consequence of the integral paired basis; shared CG1 provides its literal identification."),
    ("LA3", GB+"ValuationLowestDegreeMapFractionField.lean", "XXZ_lift", "Source integral lifting of an allowed residue path expansion; identifies the shared CG1 base-change scope."),
    ("LA3", GB+"ValuationLowestDegreeMapFractionField.lean", "space_statement_sixth_clause", "Source actual separated residue-pair lifting clause, reconstructed separately by CG1."),
    ("LA3", GB+"StatementOfDegreeAndBound.lean", "Saturated", "Source saturation under every nonzero scalar."),
    ("LA3", GB+"StatementOfDegreeAndBound.lean", "XXZ", "Actual paired integral Psi product span supplied by shared CG1."),
    ("LA3", SD+"Coarse.lean", "m0", "Constant nonnegative coarse prefix gap k*Ns+1."),
    ("LA3", SD+"Coarse.lean", "Bw", "Old-frame reference degree with k+r+1 subtraction margin."),
    ("LA3", SD+"Coarse.lean", "thc", "Actual coarse plane valuation threshold, depending on b."),
    ("LA3", SD+"Coarse.lean", "oc", "Actual parity-dependent coarse order cutoff."),
    ("LA3", SD+"Coarse.lean", "segDegSet", "Fixed exact degree at every integer letter."),
    ("LA3", SD+"Coarse.lean", "resSet", "Strict terminal-frame plane digit bound by Qc."),
    ("LA3", SD+"Coarse.lean", "Mj", "Actual restricted module whose rank is multiplied in RestLam."),
    ("LA3", SD+"LamSatRestrict.lean", "lam_sat_restrict", "Coefficient-support conditions preserve saturation."),
    ("LA3", SD+"LamSatRestrict.lean", "lam_dvd_of_res", "Vanishing reduction is coefficientwise divisibility by a uniformizer."),
    ("LA3", SD+"LamSatRestrict.lean", "restLamA_of", "Source application of NestedTypeBound saturation followed by a residue-independent O-basis."),
    ("LA3", SD+"FiniteRestrictSupport.lean", "segDegSet_finite", "Finite monomial box for a degree function supported on the finite segment."),
    ("LA3", SD+"FiniteRestrictSupport.lean", "restFin", "Actual Mj finiteness endpoint."),
    ("LA3", SD+"RestLamOfRests.lean", "RestLamA", "Exact residue-basis interface discharged using shared CG1 and LA3."),
    ("LA4", SD+"RestCountOf.lean", "laSet", "All row-label inequalities, congruences and finite index bound."),
    ("LA4", SD+"RestCountOf.lean", "LA", "Finite product of admissible row labels."),
    ("LA4", SD+"RestCountOf.lean", "nz", "Exact quotient after subtracting the row-label sum."),
    ("LA4", SD+"RestCountOf.lean", "EE", "All terminal-degree families: range below r*Qc and one residue class."),
    ("LA4", SD+"RestCountOf.lean", "eZ", "Periodic extension of terminal parameters to all integer segments."),
    ("LA4", SD+"RestCountOf.lean", "bfam", "Actual three-case family degree definition, including natural subtraction/division."),
    ("LA4", SD+"StrictMonoIntExists.lean", "okVars", "Allowed variables: no normal coordinates at old-frame letters."),
    ("LA4", SD+"StrictMonoIntExists.lean", "XX'_supported", "Literal separated-pair definition implies the allowed variable support."),
    ("LA4", SD+"RestLamOfRests.lean", "lamG", "Actual residue-position map of variables."),
    ("LA4", SD+"RestLamOfRests.lean", "lamE", "Actual segment-dependent monomial exponents."),
    ("LA4", SD+"RestLamOfRests.lean", "lamL", "Flattening of label coordinates to a monomial exponent."),
    ("LA4", SD+"RestLamOfRests.lean", "lamS", "Exact support, fixed degree and digit restriction used in decoding."),
    ("LA4", SD+"RestLamOfRests.lean", "lam_mem_lamS", "Every actual Mj element has the required monomial support."),
    ("LA4", SD+"LamImgApply.lean", "lam_digit", "Elementary two-stage quotient/remainder uniqueness."),
    ("LA4", SD+"LamImgApply.lean", "lam_img_apply", "Evaluation of the actual imgMon exponent at a residue coordinate."),
    ("LA4", SD+"LamImgApply.lean", "segmentWeightExponent", "Old-frame contribution before using uniqueness."),
    ("LA4", SD+"LamImgApply.lean", "lam_eval", "Exact ell+P*(late+Q*old) formula."),
    ("LA4", SD+"LamImgApply.lean", "restLamInj_of", "Full recovery of label, terminal parameter and every monomial."),
    ("LA4", SD+"LamMZero.lean", "restLamTau", "Current-frame family degree equals e exactly."),
    ("LA4", SD+"LamMZero.lean", "restLamInj", "Source injection endpoint, valid for arbitrary C0."),
    ("LA4", SD+"RestLamOfRests.lean", "RestLamInj", "Exact globally quantified simultaneous injection statement."),
    ("LA5", SD+"NonemptyDvrSettingOfStandard.lean", "d", "Original row degree deg-E' on TT and zero off TT."),
    ("LA5", SD+"Coarse.lean", "Et", "Exact determinant multiplier row-degree loss reconstructed in shared RS2."),
    ("LA5", SD+"Coarse.lean", "a'", "Exact coarse row degree d-Et, with natural subtraction."),
    ("LA5", SD+"Coarse.lean", "IsCLabel", "Required label bounds for every integer segment."),
    ("LA5", SD+"FrameZeroStrictMono.lean", "sum_aP", "Exact source numerical margin a'/P >= (36/5)Y*k^2*Ns; reconstructed in RS3."),
    ("LA5", SD+"BfamAtWLetterEq.lean", "bfam_at_w_letter_eq", "Actual old-frame degree is (nz-eZ)/Qc."),
    ("LA5", SD+"BfamAtWLetterEq.lean", "lamd_eZ_per", "Terminal parameter periodicity used at the wraparound."),
    ("LA5", SD+"BfamAtWLetterEq.lean", "lamd_nz_per", "Quotient degree periodicity at the wraparound."),
    ("LA5", SD+"BfamAtWLetterEq.lean", "restLamDeg", "Exact source degree endpoint; LA replaces its RestPad/Bw-positive detour by the narrow RS3 estimate."),
    ("LA5", SD+"RestLamOfRests.lean", "RestLamDeg", "Both exact target multidegree and IsCLabel conclusions."),
    ("LA6", SD+"Coarse.lean", "phc", "Actual coarse polynomial algebra substitution."),
    ("LA6", SD+"Coarse.lean", "lamGen", "Actual integral coarse generator set with exact multidegree."),
    ("LA6", SD+"Coarse.lean", "LamBar", "Residue-field span whose dimension is bounded below."),
    ("LA6", GB+"SegRing.lean", "RRdeg", "Target exact row-degree coefficient module."),
    ("LA6", SD+"RestLamOfRests.lean", "lam_map_phc", "Coefficient reduction commutes with the actual coarse substitution."),
    ("LA6", SD+"LamProdMonomial.lean", "lam_expand", "Source product expansion into monomial tuples."),
    ("LA6", SD+"LamProdMonomial.lean", "lam_li_fixed", "Source fixed-family tensor-product independence."),
    ("LA6", SD+"LamProdMonomial.lean", "lam_li_all", "All-family independence; LA proves it by an explicit free-monomial injection."),
    ("LA6", SD+"RestLamOfRests.lean", "restLam_of_rests", "Assembly of residue bases, simultaneous injection and exact multidegree."),
    ("LA6", SD+"RestCountOf.lean", "RestLam", "Exact source sum-of-product-of-ranks lower bound for dim LamBar."),
    ("LA6", SD+"RestLamOf.lean", "restLam_of", "Source endpoint incorporating saturation and geometry."),
    ("LA6", GB+"SegmentDegree.lean", "secondPartClosed", "Actual downstream use of RestLam 1088; other rank components remain distinct."),
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
    {"id":"LA1","result":"Actual periodic frame geometry gives unique late and old occurrences, full selected-position coverage and exactly the adjacent-frame overlaps.","status":"Proved by partitioning one-period half-open intervals and using the literal no-selected-letter gaps inside frames."},
    {"id":"LA2","result":"A_j=max(z_j,H+s_j) exactly controls Pz and Qc; all exponent signs, overlap factors and periodic identities follow, including product Q_j=p^n'.","status":"Proved from natural floor/logarithm identities and ordered periodic frames; no large-parameter approximation or separate geometric input."},
    {"id":"LA3","result":"The actual Mj lattices are saturated finite free modules whose integral bases reduce independently.","status":"Proved from the actual XX' paired path-basis identification CG1, then exact support intersections, finite monomial boxes and uniformizer division. CG1 is explicitly shared; no characteristic-zero isotypic claim is used."},
    {"id":"LA4","result":"The exact label/segment exponent map is injective simultaneously over all LA/EE support families: RestLamInj.","status":"Proved by two quotient/remainder steps at frame plane coordinates, one step elsewhere, and recovery of e from exact current-frame row sums."},
    {"id":"LA5","result":"All assembled support monomials have exact target row degrees a', and labels satisfy IsCLabel: RestLamDeg 1088.","status":"Proved using only shared RS3's narrow numerical margin to obtain e<nz and justify cancellation of natural subtraction; the full RestPad detour is avoided."},
    {"id":"LA6","result":"sum_(ell in LA)sum_(e in EE(ell))product_j rank_O Mj(bfam) <= dim_f LamBar: full RestLam 1088.","status":"Proved by an injective direct sum of monomial tensor spaces, residue-independent actual bases and exact membership in lamGen. Individual segment dimensions are not estimated here."},
]

ledger = {
    "title":"LA1--LA6: actual segment geometry, saturation, monomial assembly and exact degrees",
    "date":"2026-11-21",
    "source_commit":PIN,
    "source_root":str(ROOT),
    "status":"Human mathematical reconstruction with exact pinned source records; no Lean modification, build or whole-proof verification claim.",
    "claims":claims,
    "source_entries":entries,
    "range_hash_convention":"SHA-256 of the exact source bytes spanning the inclusive line range; byte offsets are zero-based and the end is exclusive.",
    "main_formulae":{
        "late_interval":"L_j=TT_Z intersect (z_(j-1),z_j]",
        "common_cutoff":"H=integer_log_p floor(a/(8Yk^2Ns)), A_j=max(z_j,H+s_j)",
        "coarse_scale":"P_j(x)=p^(A_j-x) for x<=z_j, Q_j=p^(A_(j+1)-A_j)",
        "overlap":"P_(j+1)(x)=P_j(x)Q_j; product_(j=0)^(J-1)Q_j=p^n'",
        "decoder":"N_(t,c)=ell_(t,c)+P_j(x)(u+Q_j v), ell<P, u<Q at frame-plane coordinates; v=0 elsewhere",
        "degree_margin":"a'_t/(P_j(x)Q_j)>=(36/5)Yk^2Ns>=k+r+1 => nz>rQ_j>e",
        "exact_degree":"e+Q_j*((nz-e) div Q_j)=nz; L_t+P_j(x)nz=a'_t",
        "assembly":"sum_(ell in LA)sum_(e in EE(ell))product_j rank_O M_j(b_(ell,e,j)) <= dim_f LamBar",
    },
    "shared_reconstructed_inputs":[
        {"claim_id":"CG1","report":"v0_7/coarse_lift/report.txt","result":"Actual XX' equals the same allowed integral paired path-basis span over O and the residue field, hence is saturated. CG1's proof has been independently cross-reviewed against IP3--IP4 and the literal source segPairs/XX' definitions.","application":"m(x)=m0=kNs+1>=0, theta=thc(j,b), o=oc(j); segN+r<=Ns+r<=K. Only identification/saturation, not the characteristic-zero joint-type clause."},
        {"claim_id":"RS3","report":"v0_7/residue_summation/report.txt","result":"a'_t/P_j(y)>=(36/5)Yk^2Ns for every actual segment letter, proved from Dat.Hyp via RS2's exact determinant loss.","application":"Use y=current-frame x in segment j+1, so P_(j+1)(x)=P_j(x)Q_j. This proves all degree nonunderflow uniformly in ell,e."},
    ],
    "previous_proved_inputs":[
        "IP integral signed-letter path basis and simultaneous prefix filtration, used through shared CG1.",
        "SD2's elementary saturation/reduction and tensor injection mechanism, now applied to the fully identified actual data."
    ],
    "remaining_separate_inputs":[
        "Individual segment good-path abundance and its dimension comparison (RestSeg); LA does not estimate its summands.",
        "Quantitative residue-family summation (RestSum), reconstructed separately in RS.",
        "Coarse-generator congruence (GeneratorModuloUniformiser), reconstructed separately in CG.",
        "Global arithmetic/cohomological windows and separately recorded spectral/geometric inputs."
    ],
    "artifact_sha256":{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ["segment_assembly_section.tex","report.txt","build_provenance.py"]},
}
(HERE/"provenance.json").write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+"\n")
print(f"Wrote {len(entries)} exact pinned declaration records for {len(claims)} claims.")
