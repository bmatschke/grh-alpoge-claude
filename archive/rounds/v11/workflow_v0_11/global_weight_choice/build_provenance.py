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
PATHS={'DATA': 'src/Formalism/SharpRestriction/GrowthBounds/IsResidueClassZero.lean', 'SIZE': 'src/Formalism/SharpRestriction/ElevenLe.lean', 'SCALE': 'src/Formalism/LocalRingCardinality/DataParams₂.lean', 'SMALL': 'src/Formalism/SharpRestriction/GrowthBounds/SmallOrderPrimes.lean', 'SLOPE': 'src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/SlopeEstimateOfLemmaBSlopeLine.lean', 'MEAN': 'src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/MeanNum.lean', 'EXCESS': 'src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/Conclusion1OfGainBoundAll.lean', 'INST': 'src/Formalism/SharpRestriction/GrowthBounds/DefsInst.lean', 'CORE': 'src/Formalism/SharpRestriction/FamCore.lean', 'FAM': 'src/Formalism/SharpRestriction/ParConsts.lean', 'CHOICE': 'src/Formalism/SharpRestriction/GlobalSchurBounds/WeightVectorSmallSharesSeven.lean', 'VECTOR': 'src/Formalism/SharpRestriction/GlobalSchurBounds/TopDensityNGeSixteen.lean', 'TRANSPORT': 'src/Formalism/LocalToGlobal/GlobalTheory/PowFourLtCeilThresholdPrime.lean', 'SAME': 'src/Formalism/SharpRestriction/AdmissibleParameterJoins/GandSaa.lean', 'RESULT': 'src/Formalism/LocalToGlobal/GlobalTheory/LossRequirementsOfSmallShares.lean', 'SC': 'src/Formalism/SharpRestriction/GlobalSchurBounds/QuadraticLogDerivCongr.lean'}
COMPONENT='global_weight_choice'
SCOPE='Exact local/global finite means and ChosenW are proved for supplied family data. A carrier additionally needs the separately defined CoverAll property; no full arithmetic family, RH/GRH proof or kernel replay is asserted.'

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

DEFS=[{'id': 'GW1', 'title': 'Uniform small coefficients and nonempty exact degree boxes', 'dependencies': ['GJ2', 'GII2'], 'statement': 'The actual SizesAt and logarithmic bounds give the two x^-12 coefficient estimates and width>=1 in both integer degree windows, uniformly in the family index.', 'src': {'SIZE': ['szTh', 'SizeN', 'SizeM', 'SizeK', 'SizeTT', 'SizesAt'], 'SCALE': ['Scale', 'a', "X'", "b'", 'A', 'delta1'], 'DATA': ['Nstar', 'La', 'winA', 'winB', 'box', 'boxLoc'], 'SLOPE': ['NumMean', 'Icc_ceil_floor_nonempty', 'winA_nonempty', 'winB_nonempty', 'box_nonempty', 'boxLoc_nonempty'], 'MEAN': ['ev_log', 'ev_pow', 'numMean_ev']}}, {'id': 'GW2', 'title': 'The actual MeanKappaBound at every candidate good orbit', 'dependencies': ['GW1', 'GI5', 'GI8', 'GJ1', 'GJ3'], 'statement': 'Small primes have a pointwise deficit <=Nv*x^-12; large primes have the same local mean bound from the canonical Type-I deficit. Nonnegativity holds for all degrees.', 'src': {'DATA': ['kapIIf', 'kapLoc', 'kapv', 'Cand', 'goodReps', 'meanLoc', 'MeanKappaBound'], 'SMALL': ['Conclusion2', 'adm8'], 'INST': ['KapIDef.mem_Icc'], 'SLOPE': ['RestHypI', 'inBand_of_inBand0', 'meanLoc_const_le', 'kapIIf_nonneg', 'kappa_nonneg_and_mean_bound', 'slopeEstimate_of_lemmaB_slopeLine', 'kapv_nonneg', 'Sig_nonneg']}}, {'id': 'GW3', 'title': 'Exact global marginal averages and the total orbit deficit', 'dependencies': ['GW2', 'GJ3'], 'statement': 'Constant-size restriction fibres identify each local average with one common global product average; disjoint orbit fibres give E Sigma_p<=m_ch*|TT|*x^-12 without independence across primes.', 'src': {'DATA': ['box', 'boxLoc', 'meanW', 'meanLoc', 'Sig'], 'SLOPE': ['margC', 'marg_fibre', 'marg_sum', 'marg_card', 'phi', 'phi_inj', 'box_marg', 'sum_box_product_eq_mean', 'sum_kapv_le', 'sum_Nv_le', 'sum_Sig_le']}}, {'id': 'GW4', 'title': 'A uniform weighted exceptional-prime budget', 'dependencies': ['GW1', 'GW3'], 'statement': 'The elementary harmonic bound t(1+t) and pointwise indicator bound yield E Z<=8*x^(-9-gamma), gamma=1/2-(1453/150)eps>2447/7800.', 'src': {'EXCESS': ['candF', 'ZZ'], 'SLOPE': ['mem_candF', 'sum_cand_le', 'markov_ind', 'ZZ_le', 'meanEx_of'], 'SIZE': ['SizeN', 'SizeM', 'SizeTT'], 'DATA': ['Cand', 'Sig']}}, {'id': 'GW5', 'title': 'One global degree pair satisfies exact WReq', 'dependencies': ['GW4'], 'statement': 'For 32*x^-gamma<=1 finite averaging selects one pair with Z<=x^-9/4 and exact WReq coefficients 2 and 4, proving MeanEx and WeightVectorExists.', 'src': {'EXCESS': ['MeanEx', 'ZZ'], 'SMALL': ['cands', 'WReq', 'WeightVectorExists'], 'SLOPE': ['meanEx_of', 'weight_condition_of_mean_excess'], 'DATA': ['VV']}}, {'id': 'GW6', 'title': 'ChosenW transport and realization under the separate CoverAll property', 'dependencies': ['GW5'], 'statement': 'The actual family equalities and exact bTop window identify candidates and every Sigma term, proving ChosenW for the selected pair; CoverAll additionally gives a carrier and ChosenWS. Coverage is not inferred from averaging.', 'src': {'CORE': ['FamCore', 'FamCore.CoverAll', 'FamCore.coverS_carry'], 'FAM': ['FamP'], 'CHOICE': ['ChW_at', 'ChosenW', 'ChosenWS', 'chosenWS_of_cover'], 'VECTOR': ['winAz', 'winBz', 'Wt', 'avOf', 'bvOf', 'admissible_weight_of_vector', 'wt_nonempty', 'exists_carrier'], 'TRANSPORT': ['pg_sameMore', 'pg_cls', 'pg_TT', 'pg_more', 'sAt_eq', 'pg_mem_TTn', 'pg_aL', 'Sig_eq', 'pg_LaG'], 'SC': ['sc_eq'], 'SAME': ['SameServed', 'sameServed'], 'RESULT': ['chosenW_of', 'small_share_weight_exists'], 'DATA': ['aL', 'bL', 'ParametersFill', 'kapIIf', 'kapLoc', 'Sig']}}]

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
