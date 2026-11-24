"""Rebuild component provenance from the unchanged pinned Lean checkout."""
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]/'alpoge-rh'
COMMIT='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE_URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
PATHS={'INST': 'src/Formalism/SharpRestriction/GrowthBounds/DefsInst.lean', 'EXTRA': 'src/Formalism/LocalRingCardinality/DataExtra.lean', 'FAM': 'src/Formalism/SharpRestriction/ParConsts.lean', 'GLOBAL': 'src/Formalism/SharpRestriction/GrowthBounds/PlaneCountTheoremWithConstants.lean', 'SCALE': 'src/Formalism/LocalRingCardinality/DataParams₂.lean', 'SIZE': 'src/Formalism/SharpRestriction/ElevenLe.lean', 'DATA': 'src/Formalism/SharpRestriction/GrowthBounds/IsResidueClassZero.lean', 'JOINT': 'src/Formalism/SharpRestriction/GrowthBounds/Joints.lean', 'SLOPE': 'src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean', 'SMALL': 'src/Formalism/SharpRestriction/GrowthBounds/SmallOrderPrimes.lean', 'OUT': 'src/Formalism/SharpRestriction/GrowthBounds/CornerGLContinuity.lean', 'TIES': 'src/Formalism/LocalRingCardinality/DataGatTies.lean', 'CORE': 'src/Formalism/SharpRestriction/FamCore.lean'}
COMPONENT='family_join'
SCOPE='Explicit supplied-family orbit application and uniform thresholds; actual simultaneous global arithmetic construction remains separate.'

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

DEFS=[{'id': 'GJ1', 'title': 'The universal canonical Type-I infimum is attained', 'dependencies': [], 'statement': 'Finite integer rank proves attainment with every ring/weight/target quantifier intact; the actual FamP Extra.kapI_def supplies that infimum and hence adm7.', 'src': {'INST': ['kapISet', 'one_mem_kapISet', 'KapIDef', 'KapIDef.le', 'KapIDef.mem_Icc', 'sInf_mem_kapISet', 'KapIDef.mem', 'exists_inst_defs', 'EpDef'], 'EXTRA': ['Extra'], 'FAM': ['FamP'], 'GLOBAL': ['KapIDefF', 'kapIDefF'], 'SMALL': ['adm7']}}, {'id': 'GJ2', 'title': 'Uniform logarithmic and power estimates for the actual scale', 'dependencies': ['GII2'], 'statement': 'One explicit log-cube threshold yields x^(eps-eta)<=Lambda<=x^(eps+eta) and both actual log Q bounds, with A=26 and Y=x^13, uniformly in all family indices.', 'src': {'SCALE': ['Scale', 'L', 'b', 'a', "X'", "b'", 'A', 'p0', 'delta1'], 'SIZE': ['SizeK', 'SizesAt'], 'DATA': ['Consts', 'N1', 'Gp', 'La', 'Qp'], 'SMALL': ['adm5'], 'GLOBAL': ['log_cube_le', 'sizes_bound_of_log_estimates', 'family_sizes_bound']}}, {'id': 'GJ3', 'title': 'Exact cyclic orbit and actual representation identification', 'dependencies': [], 'statement': 'The selector identities give the cyclic injection, Nv=|topsPos|, disjoint-fibre sum Nv<=|TT|, and the LatTied/GatTies identification of period, extremes and middle-weight bound.', 'src': {'DATA': ['Inst', 'stepP', 'nP', 'reps', 'topsOn', 'Nv', 'topsPos', 'wPos', 'LatTied'], 'JOINT': ['not_split_of_class_zero', 'period_eq_addOrderOf_class_zero', 'shift_eq_generator_class_zero', 'bs_add_nsmul', 'bs_bs', 'Nv_eq_card', 'LPprime_cast'], 'SLOPE': ['phi', 'phi_inj', 'bs_iter', 'bs_idem', 'bs_rep', 'topsOn_eq_image', 'Nv_eq', 'sum_Nv_le'], 'TIES': ['GatTies']}}, {'id': 'GJ4', 'title': 'The literal finite-place OrbitLatticeBounds implication', 'dependencies': ['GJ1', 'GJ3', 'GI5', 'GII7', 'GII8', 'BC7', 'BC8'], 'statement': 'The two prime ranges, actual weight casts and compatible coefficient extension give the exact ceiling height, Dp, kapv and conductor 8(Dp+1); StdSubAt and actual family identifications remain explicit.', 'src': {'JOINT': ['StdSubAt', 'HypIAt', 'HypIIAt', 'inBand_of_inBand0', 'linear_programming_input_of_hypotheses', 'LPprime_cast'], 'DATA': ['DIIf', 'DIf', 'tIIf', 'kapIIf', 'tIf', 'kapLoc', 'Dp', 'tv', 'kapv', 'Cand', 'goodReps', 'VV', 'LatTied'], 'SMALL': ['adm6', 'adm7'], 'OUT': ['OrbitLatticeBounds']}}, {'id': 'GJ5', 'title': 'Uniform family consequence with the actual construction boundary', 'dependencies': ['GJ4', 'GI8', 'GII3', 'GII7', 'GII8'], 'statement': 'Taking a finite maximum of thresholds yields the orbit implication uniformly after fixed coefficient choices; simultaneous construction of the full family, its chosen tops and covered degrees remains separate.', 'src': {'FAM': ['FamP'], 'CORE': ['FamCore', 'FamCore.CoverAll'], 'GLOBAL': ['Ev', 'Ev.and', 'Ev.x1'], 'OUT': ['FamilyWindowLogBound'], 'SMALL': ['adm6', 'adm7', 'adm8']}}]

CLAIMS=[]
for d in DEFS:
    c={k:v for k,v in d.items() if k!='src'}
    c['status']='proved_by_explicit_mathematical_reconstruction_with_stated_family_existence_boundary'
    c['sources']=[locator(key,name) for key,names in d['src'].items() for name in names]
    CLAIMS.append(c)
artifacts=[]
for name in ['main.tex','report.txt','build_provenance.py']:
    raw=(HERE/name).read_bytes()
    artifacts.append({'path':name,'sha256':sha256(raw).hexdigest(),'bytes':len(raw)})
ids={c['id'] for c in CLAIMS}
payload={'artifact_version':'0.11','component':COMPONENT,'repository':BASE_URL,'commit':COMMIT,
 'head_verified':actual_head,'line_range_convention':'inclusive, one-indexed, original bytes including line endings',
 'claims':CLAIMS,'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in FILES.values()],
 'artifacts':artifacts,'explicit_external_dependencies':sorted({d for c in CLAIMS for d in c['dependencies']} - ids),
 'scope_note':SCOPE}
(HERE/'provenance.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
lines=[COMPONENT+' source ledger at '+COMMIT,'']
for c in CLAIMS:
    lines += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['dependencies'])]
    for x in c['sources']:
        lines += [x['declaration']+' | '+x['path']+':'+str(x['line_start'])+'-'+str(x['line_end']),
                  x['pinned_url'],'file '+x['full_file_sha256']+' ; range '+x['range_sha256']]
    lines.append('')
(HERE/'source_locators.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'component':COMPONENT,'claims':len(CLAIMS),'files':len(FILES),'references':sum(len(c['sources']) for c in CLAIMS),'commit':COMMIT}))
