"""Rebuild TC1-TC6 provenance from the pinned, byte-identical Lean checkout.

Writes only this component's provenance.json and source_locators.txt.
No network, Lean edits, compilation or kernel replay. Inclusive ranges
retain their original bytes and line endings. Requires Python 3.11+.
"""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "alpoge-rh"
COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASE_URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
GB = "src/Formalism/SharpRestriction/GrowthBounds/"
PATHS = {k: GB + v for k,v in {'BASE': 'ProjectionLemmaBaseLevel.lean', 'OBJ': 'ObjSeg.lean', 'FLIP': 'FlipOneThree.lean', 'JNT': 'Joints.lean', 'DAT': 'ColumnSpanDensity/RhoLowerBoundLargeConductor.lean', 'SMAT': 'ColumnSpanDensity/LemmaSMat.lean', 'RET': 'ColumnSpanDensity/CloudPropOfMapsBasis.lean', 'RBASE': 'ColumnSpanDensity/CloudPropOfMapsRetractionBasis.lean', 'CNT': 'ColumnSpanDensity/CloudCount.lean', 'NLE': 'ColumnSpanDensity/NLeDAll.lean', 'FAC': 'ColumnSpanDensity/FactorsLEOfFintype.lean', 'WYL': 'ColumnSpanDensity/CloudBoundOfPropAndWeylDimension.lean', 'TEN': 'ColumnSpanDensity/Tensor.lean', 'TT': 'ColumnSpanDensity/RestTensor.lean', 'ORD': 'ColumnSpanDensity/ResidueClassCountOfTensorBasisInclusion.lean', 'TB': 'ColumnSpanDensity/TensorBoundOfOrderBound.lean', 'FIDX': 'ColumnSpanDensity/FactorsLEOfIndex.lean', 'LOW': 'ColumnSpanDensity/RhoLowerBoundOfEdgeCount.lean', 'EDGE': 'ColumnSpanDensity/RhoUpperBoundSmallDepth.lean', 'MONO': 'ColumnSpanDensity/LatticeCountPrimeMonoLevel.lean', 'END': 'ColumnSpanDensity/TheoremIOfIntermediateBounds.lean', 'THR': 'ColumnSpanDensity/ThresholdFixedWeightFacts.lean', 'ROUND': 'ColumnSpanDensity/TwoHundredLeRadius.lean', 'BN': 'ColumnSpanDensity/NumBase.lean'}.items()}

PREFIX = r"(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*"
DECL = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)")
BOUNDARY = re.compile(r"^" + PREFIX + r"(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b")
NS = re.compile(r"^namespace\s+(\S+)")
SEC = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
END = re.compile(r"^end(?:\s+(\S+))?\s*$")

actual_head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
if actual_head != COMMIT:
    raise RuntimeError(f"Source checkout is {actual_head}, expected {COMMIT}")

FILES = {}
for key, path in PATHS.items():
    raw = (REPO / path).read_bytes()
    pinned = subprocess.check_output(["git", "-C", str(REPO), "show", f"{COMMIT}:{path}"])
    if raw != pinned:
        raise RuntimeError(f"Working tree differs from pinned bytes: {path}")
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, rawline in enumerate(lines):
        line = rawline.decode("utf-8").rstrip("\r\n")
        if m := NS.match(line):
            stack.append(("namespace", m.group(1)))
        elif m := SEC.match(line):
            stack.append(("section", m.group(1)))
        elif m := END.match(line):
            if not stack:
                raise RuntimeError((path, i + 1, "unmatched end"))
            kind, label = stack.pop()
            if m.group(1) and m.group(1) != label:
                raise RuntimeError((path, i + 1, "end mismatch", label, m.group(1)))
        elif m := DECL.match(line):
            namespace = ".".join(label for kind, label in stack if kind == "namespace")
            name = m.group(1)
            declarations.append({"name": name, "line": i,
                                 "qualified": f"{namespace}.{name}" if namespace else name})
    FILES[key] = {
        "path": path, "full_file_sha256": sha256(raw).hexdigest(),
        "bytes": len(raw), "line_count": len(lines),
        "verified_equal_to_pinned_git_blob": True,
        "_lines": lines, "_declarations": declarations,
    }


def locator(key, name, role="parallel_source_proof", occurrence=0):
    info = FILES[key]
    hits = [d for d in info["_declarations"] if d["name"] == name]
    if occurrence >= len(hits):
        raise RuntimeError((key, name, occurrence, "declaration not found"))
    decl = hits[occurrence]
    start = decl["line"]
    lines = info["_lines"]
    end = start + 1
    while end < len(lines) and not BOUNDARY.match(lines[end].decode("utf-8")):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    excerpt = b"".join(lines[start:end])
    if role == "parallel_source_proof" and re.match(r"^" + PREFIX + r"(?:def|abbrev|structure)\b", lines[start].decode("utf-8")):
        role = "definition_or_statement"
    return {
        "path": info["path"], "declaration": decl["qualified"],
        "source_spelling": name, "line_start": start + 1, "line_end": end,
        "role": role, "full_file_sha256": info["full_file_sha256"],
        "range_sha256": sha256(excerpt).hexdigest(), "range_bytes": len(excerpt),
        "pinned_url": f"{BASE_URL}/blob/{COMMIT}/{info['path']}#L{start+1}-L{end}",
    }


def many(key, names, role="parallel_source_proof"):
    return [locator(key, name, role) for name in names]



DEFS = [{'id': 'TC1', 'title': 'Primitive midpoint retraction and complete cloud factor count', 'dependencies': ['HM5', 'HM8', 'HM11'], 'statement': 'The exact lattice preimage gives an integral retraction; Smith splitting and an explicit block inverse give r>=n1+n2-d(H+) and B*r actual factors at depth2D+K with the exact dual conductor.', 'src': {'SMAT': ['smt_unit', 'smt_block', 'lemmaSMat'], 'RET': ['latRetract', 'cloud_prop_of_maps_basis', 'cloud_bound_of_maps'], 'RBASE': ['RestCloudMaps', 'cloud_prop_of_maps_retraction_basis'], 'CNT': ['be_pull', 'cloud_count'], 'NLE': ['nLeD_all', 'nEdge', 'nLeD'], 'FAC': ['LemmaSMat', 'LatRetract', 'wit_of_factors', 'factorsLE_of_fintype']}}, {'id': 'TC2', 'title': 'Actual cloud Weyl comparison and retained fraction', 'dependencies': ['TC1', 'CB3'], 'statement': 'Factorwise Weyl bounds give the loss kappa1+2kappa2+12Nkc/bprime and the exact depth/conductor in CloudWeightLowerBound.', 'src': {'WYL': ['cloudAt', 'dimCl', 'CloudLowerBoundWeyl', 'weylDim_add_const', 'cwt_lower', 'top_bounds', 'dimV_weyl', 'dimV_flat', 'dimV_tops', 'top_shape', 'share_abs', 'one_sub_mul_exp_le_one_of_le', 'one_add_pow_le_exp_mul', 'top_facts_lemma_4', 'cloud_bound_of_prop_and_weyl_dimension'], 'DAT': ['CloudWeightLowerBound']}}, {'id': 'TC3', 'title': 'Small complementary weights and exact residual tensor loss', 'dependencies': ['HM8', 'EL5'], 'statement': 'The disjoint-letter tensor isomorphism and tableau inclusions prove ResidueClassCount: add2nprime*c to height, subtract it from conductor, preserve depth and retained fraction.', 'src': {'TEN': ['tnMu', 'tnDelta', 'tn_finrank_zero', 'tn_dimV', 'restTensor_of'], 'TT': ['restTensor'], 'ORD': ['Elast', 'Ar_sub_le', 'steps_rev', 'restOrdBound', 'residueClassCount_of_tensor_basis_inclusion'], 'TB': ['dual_bases', 'tensor_bound_of_order_bound'], 'FIDX': ['Ar_add'], 'DAT': ['ResidueClassCount']}}, {'id': 'TC4', 'title': 'Every-edge factors yield the literal LPprime matrix certificate', 'dependencies': ['HM5', 'HM8'], 'statement': 'Incoming-edge count and the integral inverse of I+E give GoodRankK at every target lattice, preserving source cleaning and depth D.', 'src': {'LOW': ['be_Re', 'be_Re_scale', 'CCL_le_Nsrc', "CCL'_le_Ntgt", 'CCL_other', "CCL'_other", 'rho_lower_bound_of_edge_count'], 'EDGE': ['restEdgeCount', 'rho_lower_bound_large_conductor'], 'DAT': ['RhoLowerBoundLargeConductor']}}, {'id': 'TC5', 'title': 'Infimum attainment and direct MidLP for every dominant weight', 'dependencies': ['TC2', 'TC3', 'TC4', 'NP5', 'NP7', 'NP8'], 'statement': 'Finite integer rank attains kF; the two actual degree shifts, cloud count, complementary tensor and exact depth/height budget give MidLP with Dat.kText.', 'src': {'MONO': ['vLEO_mono', 'FactorsLE_mono', 'RhoGE_mono', 'RhoL_mono', 'RhoL_zero', 'rho_inf_mem', 'kF_mem', 'kF_le_one', 'lpprime_of_one_le', 'initial_level_mono_weights', 'tStar_mono', 'topW_base', 'topW_dom', 'topW_zero', 'midLP_of'], 'DAT': ['kF', 'Inside', 'kText', 'FactsLP', 'MidLP']}}, {'id': 'TC6', 'title': 'Complete local Type-I Conclusion2 with explicit sufficient constants', 'dependencies': ['TC5', 'RU11', 'RU10', 'RD15', 'HM6', 'HM7', 'HM12', 'NP2', 'NP3', 'NP4', 'NP5', 'NP6', 'NP8', 'NP9', 'SW9'], 'statement': 'For C0>=880 and CH>=2800001, literal HypI implies Conclusion2 with C=302114. All constants precede the data; good-share attainment and the exact D0,kx identities avoid the bundled AdmB/AdmT premise. No global data existence is asserted.', 'src': {'OBJ': ['GoodSub', 'GoodShare', 'badShare', 'kapT', 'kap0G4'], 'FLIP': ['depthD'], 'JNT': ['goodSub_bot', 'badShare_spec', 'depth_bound_of_extension', 'bad_share_of_extension_proposition'], 'BASE': ['EvenGapHyp', 'IaZ', 'IbZ', 'meanKap', 'HypI', 'WeightI', 'tI', 'Conclusion2', 'kapTI', 'totalDegreeBudget', 'kapPI', 'ClosedP', 'projection_lemma_base_level'], 'DAT': ['Cst', 'Cst.Pos', 'kF', 'kx', 'kText', 'Cst.Cmean'], 'END': ['kF_nonneg', 'kText_nonneg', 'theorem_I_of_intermediate_bounds'], 'BN': ['Cst.TLP'], 'ROUND': ['Cst.TM'], 'THR': ['threshold_fixed_weight_facts', 'threshold_mean_kappa_facts']}}]

CLAIMS=[]
for d in DEFS:
    c={k:v for k,v in d.items() if k!='src'}
    c['status']='proved_by_actual_integral_maps_matrix_arguments_and_explicit_constant_assembly'
    c['sources']=[locator(key,name) for key,names in d['src'].items() for name in names]
    CLAIMS.append(c)
artifacts=[]
for name in ['main.tex','report.txt','build_provenance.py']:
    raw=(HERE/name).read_bytes()
    artifacts.append({'path':name,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
payload={'artifact_version':'0.10','component':'type_one_closure','repository':BASE_URL,'commit':COMMIT,
 'head_verified':actual_head,'line_range_convention':'inclusive, one-indexed, original bytes including line endings',
 'claims':CLAIMS,'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in FILES.values()],
 'artifacts':artifacts,'explicit_external_dependencies':['CB3', 'EL5', 'HM11', 'HM12', 'HM5', 'HM6', 'HM7', 'HM8', 'NP2', 'NP3', 'NP4', 'NP5', 'NP6', 'NP7', 'NP8', 'NP9', 'RD15', 'RU10', 'RU11', 'SW9'],
 'scope_note':'Complete supplied-data local Type-I Conclusion2, with C0>=880, CH>=2800001 and C=302114. No global arithmetic existence, full RH/Dirichlet-GRH proof, Lean compilation or kernel replay is asserted.'}
(HERE/'provenance.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
lines=[f'TC1-TC6 source ledger at {COMMIT}','']
for c in CLAIMS:
    lines += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['dependencies'])]
    for x in c['sources']:
        lines += [x['declaration']+' | '+x['path']+':'+str(x['line_start'])+'-'+str(x['line_end']),
                  x['pinned_url'],'file '+x['full_file_sha256']+' ; range '+x['range_sha256']]
    lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'claims':len(CLAIMS),'files':len(FILES),'references':sum(len(c['sources']) for c in CLAIMS),'commit':COMMIT}))
