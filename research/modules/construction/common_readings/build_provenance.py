#!/usr/bin/env python3
"""Rebuild RDR provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v038

Only files beside this script are written. This is source backtracking and
human-proof bookkeeping, not a Lean kernel replay.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
COMPONENT = "common_readings"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v038")
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"RDR\d+", key) for key in old)
raw = (HERE / "main.tex").read_bytes()
assert not any(c < 32 and c not in (9, 10) for c in raw)
lines = raw.decode().splitlines(keepends=True)
DECL = re.compile(r"^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|theorem|lemma|structure|class|abbrev|inductive)\s+([^\s:{(]+)")
cache = {}


def source(path, anchor):
    name, sep, n = anchor.partition("@")
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        assert b == subprocess.check_output(["git", "show", PIN + ":" + path], cwd=SOURCE), path
        ls = b.decode().splitlines(keepends=True)
        ds = [(i, DECL.match(s).group(1)) for i, s in enumerate(ls) if DECL.match(s)]
        cache[path] = (b, ls, ds)
    b, ls, ds = cache[path]
    found = [(j, i) for j, (i, x) in enumerate(ds) if x == name and (not sep or i + 1 == int(n))]
    assert len(found) == 1, (path, anchor, found)
    j, st = found[0]
    en = ds[j + 1][0] if j + 1 < len(ds) else len(ls)
    for k in range(st + 1, en):
        if re.match(r"^(?:end(?:\s|$)|namespace\s|section(?:\s|$)|variable\s|set_option\s|attribute\s)", ls[k]):
            en = k
            break
    while en > st + 1 and not ls[en - 1].strip():
        en -= 1
    rb = "".join(ls[st:en]).encode()
    return {
        "path": path, "declaration": name, "source_spelling": name,
        "declaration_anchor": anchor, "line_start": st + 1, "line_end": en,
        "sha256": sha(b), "file_sha256": sha(b), "range_sha256": sha(rb),
        "range_bytes": len(rb), "first_line": ls[st].rstrip(),
        "verified_equal_to_pinned_git_blob": True,
        "role": "Original definition, exact contract or corresponding formal argument. The independently written RDR block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


anchors = {f"RDR{i}": [] for i in range(1, 23)}
for s in (HERE / "source_anchors.txt").read_text().splitlines():
    if not s or s.startswith("#"):
        continue
    ids, path, names = s.split("|")
    for name in names.split(";"):
        entry = source(path, name)
        for key in ids.split():
            assert key in anchors, key
            if entry not in anchors[key]:
                anchors[key].append(entry)

titles = [
 'The fixed original data and the order of side and reader selection',
 'The simultaneous localization submodule with its literal membership test',
 'The exact distinguished Gram frame including the conjugate representative',
 'The original HLat record with prescribed local tests and off-place metrics',
 'Original quotient coordinates and invertibility of every actual row frame',
 'A basis through an involutively semilinear exact range',
 'The literal RrT coordinate basis and original all-place frames',
 'Uniqueness of the standard residual read and its exact central action',
 'All fields of the original Side0 constructor',
 'RRset invariance and the noncircular two-stage Good/RRDef construction',
 'The unique actual jW from the original goodForm and norm-injective eW',
 'The full original exists_side_reading_level_zero endpoint',
 'Exact finite-level inclusions and original real parameters',
 'All original RowIds and RowSideReal fields from the given ChT',
 'All original LiftIds, MjTie and LiftTie fields from the given LfT',
 'The actual quotient of finite types and occurrence in the two row bases',
 'Triviality of the original base idele character and the period quotient',
 'Exact used tuples, original Hilbert lift and unused-chain vanishing',
 'Coordinate equality preserves forms, integral sets and both central ties',
 'The complete original read_of_moved with all twelve map equalities',
 'The same original ReadPk with all five Pin fields',
 'Installation of full ReadL under exactly the original eta agreement',
]
deps = {
 'RDR1': [], 'RDR2': [], 'RDR3': [], 'RDR4': ['RDR2','RDR3'],
 'RDR5': ['DI14','TD8','SLR2','SLR4'], 'RDR6': [],
 'RDR7': ['RDR5','RDR6'], 'RDR8': ['RDR1'],
 'RDR9': ['RDR4','RDR7','RDR8'], 'RDR10': ['RDR7','RDR9'],
 'RDR11': ['DI16'], 'RDR12': ['RDR4','RDR10','RDR11'],
 'RDR13': ['DI16'], 'RDR14': ['RDR13'], 'RDR15': ['RDR13'],
 'RDR16': [], 'RDR17': ['JIO14'], 'RDR18': ['RDR7'],
 'RDR19': [], 'RDR20': ['RDR1','RDR14','RDR15','RDR16','RDR17','RDR18','RDR19'],
 'RDR21': ['RDR12','RDR20'], 'RDR22': ['RDR21'],
}
scopes = [
 'One original B,f,T,w,Z0,hX,Wt,z0,q,o, Inputs(D), Fits(o), and given Moved(o). First exists one Side0 before every later Read; separately every Side0 admits a Read with all exact ties. No outer realization existence.',
 'Every O_K-module, arbitrary indexed prime ideals and submodules; exact universal local denominator membership, without finite-generation or full-rank conclusion.',
 'Every original coefficient embedding and finite complex Hilbert basis, including zero dimension and both representatives e or conjugate(e) of the infinite place. Frame inverse has the exact source direction.',
 'Every arbitrary prime-indexed set family and every supplied invertible off-place frame. One explicit K^n HLat record, exact base norm and all off-base pairings; not HLat.Good.',
 'Both original row sides of toCx3(F); same rational adjoint cut, actual nP^-1 Gram, actual quotient metric and joint generalized-Hecke type projections. All embeddings, including dimension zero.',
 'Every involutive semilinear injection and every fixed linear injection with exactly the same range. The output basis lies in the supplied E itself.',
 'Every given actual jE onto EEc_b. Exact RrT dimension, semilinear twist, basis map and frames Xo(v)=original XE(v), for both row sides.',
 'Every original standard residual isomorphism, both distinguished prime families and every central coefficient tuple. The resulting action is on the original base complex spaces.',
 'Full original Side0 with unchanged Amb/Mult/io/Mtilde/eOp and exact new permitted central reading, HLat and jEE.',
 'One side selected before any later Read. Exact own RRDef by two applications of Side0; RRset is independent of the new RR and jEE. Good is not HLat.Good.',
 'Every original target index and every rational coordinate, for any given actual MjTie. Unique semilinear jW, same nP(F,false), same bL/FW.j, exact original source dimension.',
 'Full original exists_side_reading_level_zero on its stated inputs: exists s, then forall Read Y with four specified ties, Nonempty RationalReadingWithoutCongruence. Both original metrics and all ten fields.',
 'Both original levels and every used inner/terminal index; exact level subgroup and character restrictions. Original target holomorphic labels and base embedding; no new integration conclusion.',
 'Every supplied original ChT, all used tuples, inner indices 1<=j<=m-1, actual end maps and all RowSideReal fields with unchanged pairings.',
 'Every supplied original LfT and LamDef, same used tuples and target indices. Original eW range/norm/lattice, theta equation and normalized trace on each nonzero type.',
 'Given exact Reps completeness/uniqueness/occurrence; actual FTR quotient, all row/lift isotypic parts, and occurrence in at least one original row basis.',
 'Actual ChrEq(c,1) gives c=1 on original AE units by local/real density. Original xi base and ColTieR for all tuples/words, retaining the exact period kernel-vanishing guard.',
 'All actual primes and tuples, both Wt cases, same principal HE model and all unused chain maps. No new Hilbert model or tuple choice.',
 'Every original equal matrix record and all Keep-compatible cG; canonical Fin equality casts only, exact FormsTie/OLatTie and both universal central-action fields.',
 'Full original read_of_moved for every given Side0, all Read fields and twelve simultaneous output ties on the same R,F,y,t; original numerical/period guards copied unchanged.',
 'Full original readPk_pin_exists: one Side0, one Read, one RationalReadingWithoutCongruence and five original Pin clauses, all dependent on those same choices.',
 'Full ReadL only if original etaJ=etaOf on 1<=j<=m; on the moved route supplied o.eta=q.eta and Moved.eta prove exactly that equality. No full ReadL for arbitrary o.eta.',
]
hyps = [
 ['Original Inputs, Fits, RowPk and Moved; all geometry, pins, comparisons, numbers and periods refer to these one fixed data.'],
 ['Each P_u is a proper prime ideal and each S_u is an O_K-submodule.'],
 ['Given basis of the actual finite-dimensional complex Hilbert space.'],
 ['Given invertible Xo at every embedding, original embedding and arbitrary specified local sets.'],
 ['Original Pins/Holds, row rational tests, Ok3, group/Hecke stability, block data, positive theta operators, sumE, levE and exact coefficient forms.'],
 ['Additive involutive semilinearity, zero kernel, fixed injective linear jE and equality of their ranges.'],
 ['Original Pins/Holds and fixed injective jE with exact range EEc_b; original HE model.'],
 ['Original Fits.grpAt.cen, Keep.grp, idG, matrix laws, Tie1 and actual coefficient equalities.'],
 ['Same original hFits and Moved, specified basis/frames and local sets.'],
 ['Original actual base jE and primitive data of RDR7; original chain and integral carrier remain fixed.'],
 ['Original Holds.aux.levelW and MjTie range/norm, with original nP positive and the original bL coordinate basis.'],
 ['Original Inputs/Fits/Moved; sharp DivIs coordinate/metric/RRDef and stored sharp RrT; four original output compatibility ties.'],
 ['Original explicit level and character definitions; original base-field/embedding and fixed target labels.'],
 ['Full original ChT including all pairings and io equations, and the exact used-tuple equivalence; original m>=2.'],
 ['Full original LfT including theta equation and eW lattice; given LamDef and same used-tuple equivalence.'],
 ['Original Reps.mem/inj/all and ChT.ft; representation completeness is retained, not inferred.'],
 ['Original BaseW.lev.xi/xi_base and BuDefQ; the exact kernel-vanishing antecedent in ColTieR.bu.'],
 ['Original MuW on/off/tw, xi injectivity, Moved tuple and mu ties, HE range/injection and ChT.junk.'],
 ['Original equality of matrix records, Tie1, Side0.is, Fits.cen and every supplied Keep.'],
 ['All original RDR1 inputs, including full actual ChT/LfT/Reps/coordinate comparisons; same-stage NumOK and KapDef.'],
 ['Exactly original Inputs(D), Fits(o) and given Moved(o); no extra compatibility premise beyond the endpoints already proved.'],
 ['Original eta agreement o.eta=q.eta on every 1<=j<=m and all places, or directly the literal etaJ=etaOf equality in that range.'],
]
claims=[]
for i,title in enumerate(titles,1):
    key=f'RDR{i}'
    st=[j for j,s in enumerate(lines) if s.strip()==f'% BEGIN {key}']
    en=[j+1 for j,s in enumerate(lines) if s.strip()==f'% END {key}']
    assert len(st)==len(en)==1 and st[0]<en[0] and anchors[key],key
    block=''.join(lines[st[0]:en[0]]).encode()
    assert all(d in old or d in deps for d in deps[key]),key
    claims.append({'id':key,'title':title,'introduced_in':'0.39','classification':'B',
      'status':'Complete independent human proof in its stated conditional scope',
      'proof_status':'complete in stated scope','review_status':'pending independent mathematical review',
      'depends_on':deps[key],'scope':scopes[i-1],'quantifier_scope':scopes[i-1],
      'hypotheses_retained':hyps[i-1],
      'classical_inputs':(['Finite-dimensional complex spectral theorem / Gram-Schmidt; its inverse-frame use is proved explicitly.'] if key in ('RDR3','RDR5') else []),
      'proof_location':{'file':COMPONENT+'/main.tex','paragraph':key,'label':'claim:'+key,
        'line_start':st[0]+1,'line_end':en[0],'bytes':len(block),'sha256':sha(block),'range_sha256':sha(block),'file_sha256':sha(raw)},
      'sources':anchors[key]})
visited,visiting=set(),set()
def visit(k):
    if k in visited or k not in deps:return
    assert k not in visiting,('cycle',k)
    visiting.add(k)
    for d in deps[k]:visit(d)
    visiting.remove(k);visited.add(k)
for k in deps:visit(k)

inputs,blocks=[],[]
input_names={'continuation_notes_v0_38/next_division_and_readings.txt'}
for key in sorted({d for ds in deps.values() for d in ds if d in old}):
    pl=old[key]['proof_location'];file=pl['file'];input_names.add(file)
    companion=str(Path(file).with_name('provenance.json'))
    if (BASE/companion).exists():input_names.add(companion)
    b=(BASE/file).read_bytes();ls=b.decode().splitlines(keepends=True)
    if 'line_start' in pl and 'line_end' in pl:st,en=pl['line_start']-1,pl['line_end']
    else:
        hits=[j for j,s in enumerate(ls) if '\\paragraph' in s and re.search(r'\b'+key+r'(?!\d)',s)]
        assert len(hits)==1,(key,hits)
        st=hits[0];en=next((j for j in range(st+1,len(ls)) if ls[j].startswith('\\paragraph')),len(ls))
    rb=''.join(ls[st:en]).encode();expected=pl.get('range_sha256',pl.get('sha256'))
    if expected:assert sha(rb)==expected,(key,'inherited proof-range mismatch',sha(rb),expected)
    blocks.append({'id':key,'file':file,'release':'0.38','line_start':st+1,'line_end':en,'sha256':sha(rb),'range_sha256':sha(rb),'file_sha256':sha(b)})
for file in sorted(input_names):
    b=(BASE/file).read_bytes();inputs.append({'file':file,'release':'0.38','sha256':sha(b),'file_sha256':sha(b),'bytes':len(b)})

standing='The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. These are human-reconstruction statuses only.'
remaining=[
 {'id':'RDR_COMMON_GEOMETRIC_MOVED_REALIZATION','classification':'C','role':'retained shared original producer',
  'contract':'One common z0,q,o,Moved(o) with the original R,F, geometric realization, columns, periods, trace sets, core and every original pin. The output reader construction does not produce this datum.'},
 {'id':'RDR_ACTUAL_PRIMITIVE_TESTS','classification':'C','role':'retained original producer',
  'contract':'Actual Holds primitive row/lift rational tests, Hecke/group equations, levels, positive theta operators and type decompositions on this one R,F. RDR5 consumes the exact row clauses; no ratG/MLat producer is inferred.'},
 {'id':'RDR_ACTUAL_COMPARISON_PACKET','classification':'C','role':'retained original producer',
  'contract':'The same PkT with both actual ChT maps and exact pairings/io equations, full LfT/eW norm/range/lattice/theta relation, Reps catalogue, original sharp RrT, coordinate ties and dall.'},
 {'id':'RDR_FITS_SHARP_AND_GROUP','classification':'C','role':'retained common-stage producer',
  'contract':'Original Fits(o): sharp DivIs coordinate/off-place metric/RRDef; GrpTrue, GrpAt and universal standard-read CenIs on the already selected V,S,N,G.'},
 {'id':'RDR_ORIGINAL_PERIOD_NUMERIC_DATA','classification':'B','role':'retained exact input and finite matching, not a new selected leaf',
  'contract':'The RowPk NumOK/KapDef and period/zero-scalar records evaluated at the same o fields. RDR20 closes their installation only; any upstream production status remains governed by the inherited common-construction audit.'},
 {'id':'RDR_ETA_AGREEMENT','classification':'B','role':'explicit original full-ReadL guard',
  'contract':'For every 1<=j<=m and every place v, o.eta(j,v)=q.eta(j,v). Moved.eta then identifies etaOf(R,F); arbitrary Over does not imply this agreement. No additional premise for the two named source endpoints.'},
]
closed=[
 {'id':'RDR_ACTUAL_HLAT_AND_GOOD_SIDE','claims':['RDR2','RDR3','RDR4','RDR5','RDR6','RDR7','RDR8','RDR9','RDR10'],
  'contract':'Literal exists_side and exists_good: exact all-place frames, distinguished norm, localized membership and own RRDef on the original base complex side, constructed before every later Read.',
  'requires':['original Fits and given Moved','original Pins/Holds and fixed base jE/ChT','same original chain and integral carrier']},
 {'id':'RDR_ACTUAL_JW','claims':['RDR11'],
  'contract':'Literal CoordW.exists_jW with exact original bL/FW.j, target dimension and mj.eW; uniquely determined by its map equality.',
  'requires':['original Holds.aux.levelW','given original MjTie range/norm and positive nP']},
 {'id':'RDR_LEVEL_ZERO_SOURCE_ENDPOINT','claims':['RDR12'],
  'contract':'Full original exists_side_reading_level_zero: exists Side0 s, then every Read Y with the four original ties admits RationalReadingWithoutCongruence on that s and Y.',
  'requires':['original Inputs, Fits, given Moved','RDR_ACTUAL_HLAT_AND_GOOD_SIDE','RDR_ACTUAL_JW'],
  'additional_premises_beyond_original_source':[]},
 {'id':'RDR_MOVED_READ_SOURCE_ENDPOINT','claims':['RDR13','RDR14','RDR15','RDR16','RDR17','RDR18','RDR19','RDR20'],
  'contract':'Full original read_of_moved: every given Side0 admits the original Read with all twelve simultaneous exact map/frame/coordinate/representative ties.',
  'requires':['original Inputs, Fits, given Moved and arbitrary Side0','original common ChT/LfT/Reps and coordinate/numerical/period records'],
  'additional_premises_beyond_original_source':[]},
 {'id':'RDR_READPK_PIN_SOURCE_ENDPOINT','claims':['RDR21'],
  'contract':'Full original readPk_pin_exists with one Side0, one Read and its RationalReadingWithoutCongruence, plus all five Pin equalities.',
  'requires':['RDR_LEVEL_ZERO_SOURCE_ENDPOINT','RDR_MOVED_READ_SOURCE_ENDPOINT','same fixed original input datum'],
  'additional_premises_beyond_original_source':[]},
 {'id':'RDR_FULL_READL_WITH_ORIGINAL_GUARD','claims':['RDR22'],
  'contract':'Exact full ReadL and reading part of RowsAre when the original eta agreement holds. No full ReadL for arbitrary Over.',
  'requires':['RDR_READPK_PIN_SOURCE_ENDPOINT','RDR_ETA_AGREEMENT']},
]
for x in closed:x.update({'classification':'B','status':'closed conditional implication','dependency_mode':'sufficient conjunction in the expressly stated original scope'})
not_closed=[
 'Existence of the original common geometric realization, RowPk/Fits/Moved and complete comparison packet.',
 'Production of primitive rational tests, positive theta operators, exact level/integral records, or the original representation catalogue.',
 'Full ReadL without the original etaJ agreement; Side0.Good does not assert HLat.Good/fullness.',
 'ReadC, ratG, MLat, stronger DivRows3, an actual common selector or a new universal-family/threshold supplier.',
 'Generic RowPairInt/CuspRapidDecay is separate; this chapter consumes exact given ChT/LfT pairings and adds no such analytic premise.',
 'Any additional whole selected-leaf closure or unconditional RH/Dirichlet-GRH theorem.',
]
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.39','date':'2026-11-22','component':COMPONENT,
 'source_commit':PIN,'repository':'CocoSgt/riemann-hypothesis-lean','standing_assumption':standing,
 'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),
 'range_convention':'Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.',
 'metadata_builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable_invocation':'python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v038','source_anchor_file':'source_anchors.txt','source_anchor_sha256':sha((HERE/'source_anchors.txt').read_bytes())},
 'claims':claims,'claim_total':len(claims),'external_literature':[],'published_applications':[],
 'inherited_proof_inputs':inputs,'inherited_proof_blocks':blocks,'not_closed':not_closed,
 'source_files':[{'path':p,'sha256':sha(b),'file_sha256':sha(b),'bytes':len(b),'line_count':len(ls),'verified_equal_to_pinned_git_blob':True} for p,(b,ls,_) in sorted(cache.items())]}
dump('provenance.json',prov);dump('published_applications.json',[])
closure={'schema':'rh-human-component-closure/1','version':'0.39','component':COMPONENT,'source_commit':PIN,
 'standing_assumption':standing,'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'new_claim_ids':[c['id'] for c in claims],'closed_contracts':closed,'remaining_inputs':remaining,'selected_top_level_leaf_closed':False,
 'same_object_guards':['One original B,f,T,w,z0,q,o,Moved and R,F,y,t; no new geometric realization.',
  'One Side0 is selected before every later Read; the final packet uses precisely that same side and reader.',
  'Original Amb/Mult/io/Mtilde/eOp, all periods, finite/full levels, and original measures remain fixed.',
  'Both original row sides: exact distinguished norm and every off-distinguished Hermitian pairing, with correct coefficient twist and frame inverse.',
  'Original target eW, norm factor nP(F,false), FW.j/bL, integral MK and good-space records; no arbitrary isomorphic target.',
  'Canonical coordinate reindexings come only from the supplied matrix-record equalities; all twelve output ties are simultaneous.',
  'Full ReadL retains the exact etaJ agreement on every 1<=j<=m and all places.',
  'Pointwise original constructors introduce no common threshold or change to outer common-family/NEb quantifiers.'],
 'not_closed':not_closed,'review_status':'pending independent mathematical review'}
dump('closure.json',closure)
loc=[f'RDR source locators — {PIN}','Inclusive one-based source/proof lines and exact byte hashes.',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
    p=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
    for s in c['sources']:loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
validation={'status':'PASS','source_commit':PIN,'main_sha256':sha(raw),'claims':len(claims),'claim_source_references':sum(len(c['sources']) for c in claims),'distinct_source_ranges':len(ranges),'source_files':len(cache),'inherited_files':len(inputs),'inherited_claim_blocks':len(blocks),
 'checks':['Pinned HEAD and every referenced Git blob','Unique source anchors and all marked human proof ranges','All depends_on entries indexed in baseline/new claim ledgers','New-claim dependency DAG acyclic','Exact source/proof/inherited-input hashes and unused RDR prefix','No unexpected control characters'],
 'not_performed':'No Lean compilation or kernel replay; independent mathematical review and standalone draft TeX are separately recorded.'}
dump('validation.json',validation)
report='''v0.39 — actual common readings, RDR1–RDR22

RDR2–RDR10 prove the original level-zero side constructor: a literal
simultaneous-localization submodule, exact distinguished Gram frame,
actual quotient coordinate basis and all-place row frames, unique
standard residual read and exact central action, and a noncircular
two-stage RRDef construction. The key is that RRset depends only on the
unchanged chain, finite complex spaces and integral carrier, not on the
new rational lattice or jEE. Side0.Good is not HLat.Good/fullness.

RDR11 constructs the unique actual target jW through norm-injective eW
and proves its exact FW.j/bL identity. RDR12 proves the whole original
exists_side_reading_level_zero statement: one side before every later
compatible reader, with both row metrics, actual quotient coordinates,
both RRDef fields and exact target jW. No extra premise is introduced.

RDR13–RDR20 reconstruct every original Read field and all twelve
read_of_moved output ties. They prove actual finite-level inclusions,
range inverses for ChT/LfT, the exact nP target normalization and
integral Mj tie, original type quotient and two-basis occurrence,
actual finite/real idele character uniqueness, the period quotient,
used-tuple and Hilbert-model dictionaries, coordinate/form/lattice
casts and universally Keep-compatible central actions. Original
ChT/LfT pairings and theta relations are supplied inputs, so this
constructor adds no generic RowPairInt premise.

RDR21 joins both endpoints on one Side0 and one Read to give the
literal ReadPk and all five Pin fields. RDR22 gives full ReadL only
under original o.eta=q.eta on 1<=j<=m; arbitrary Over does not imply
that final etaJ field. The full original named endpoints are closed
in their stated scope, but no common realization, primitive tests,
complete comparison packet, ReadC, ratG/MLat, stronger DivRows3,
selector, universal NEb or new common threshold is produced.

All source correctness is assumed. No Lean build/replay was used.
No new deep published application is claimed; published_applications
is the empty list. Existing human proofs are separately hash-bound.
'''
report+=f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE/'closure.json').read_bytes())}\n"
report+=f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} source files; {len(inputs)} inherited files; {len(blocks)} inherited proof blocks.\n"
(HERE/'report.txt').write_text(report)
print(json.dumps({**validation,'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))

