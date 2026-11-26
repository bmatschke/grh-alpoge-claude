#!/usr/bin/env python3
"""Rebuild DI provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v037

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
COMPONENT = "division_identity"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v037")
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"DI\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written DI block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


anchors = {f"DI{i}": [] for i in range(1, 22)}
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
 'The common objects and exact conditional first-output contract',
 'Explicit compact polynomial averages in every original Sobolev seminorm',
 'Original HC absolute irreducibility and finite tensor interpolation',
 'A nonzero original intertwiner vector separates the equivariant defect',
 'Actual finite adelic lifts of the common residual block',
 'Original type and twist functions under block triangular changes',
 'Actual step vacuum, weighted half-model transport and exact flag ratio',
 'Original finite Weil eigenlaw on every polynomial creator vector',
 'Change of variables in the original theta-intertwiner integral',
 'Literal StepLev and TopLev on the original chain and terminal range',
 'Actual finite row idempotent adjoint, conditional on RowPairInt',
 'Literal RowProj including the ipM empty-witness fallback',
 'Both original composite intertwiner identities with unchanged measures',
 'Exact quotient-coordinate projection inside the original theta map',
 'Both original RowSideDef3 records',
 'Actual finite cardinalities, index, ranks and base embedding',
 'Integral descent of the original norm-defined good lattice',
 'Original target coordinate basis independent and spanning',
 'Exact OLatTie on the original target integral generators',
 'All nine first DivDef3 fields under explicit RowPairInt',
 'Conditional first-Div installation on CSR-updated data',
]
deps = {
 'DI1': [], 'DI2': ['RQC7'], 'DI3': [], 'DI4': ['DI2','DI3'],
 'DI5': [], 'DI6': [], 'DI7': ['DI6','WA12','QD19','JIO13','BTH15','FIA4'],
 'DI8': ['DI5','DI7','CW12'], 'DI9': ['DI8','RQC4'],
 'DI10': ['DI1','DI4','DI5','DI9'],
 'DI11': ['DI1','DI5','RQC4','GV10'], 'DI12': ['DI3','DI11'],
 'DI13': ['DI1','DI10','DI12'],
 'DI14': ['TD1','TD2','TD3','TD4','TD5','TD6','TD7','TD8','TD9'],
 'DI15': ['DI13','DI14','TD9'], 'DI16': [], 'DI17': [],
 'DI18': ['DI16'], 'DI19': ['DI17','DI18'],
 'DI20': ['DI1','DI15','DI16','DI18','DI19'],
 'DI21': ['DI20','CSR11','CSR12','CSR13','CSR22'],
}
scopes = [
 'Fix one original D,G,A3,Ks,R,F,cG,X0,Y,Z,C,sEE. Retain Pins,Holds and original real-group packet, and separately require RowPairInt for all b,t,w,c,v,vprime,g before deriving the first output.',
 'Every smooth vector in every actual local DSModel; one family of compact polynomial averages converges in every finite Lie-word Sobolev seminorm. Rank zero included.',
 'Every positive-rank original DSModel under the retained HarishChandraModules predicate, and the explicit rank-zero case; all factorwise-stable subspaces of the finite algebraic tensor product.',
 'Every archimedean-equivariant linearization of the original separately Sobolev-continuous multilinear map; a nonzero kernel vector forces the defect to vanish on all smooth tensors.',
 'Every residual g0 in the original G0, every actual inner or terminal target level, and its unchanged self-dual frames; simultaneous finite residue lifts preserve all other selected places.',
 'Every actual adjacent block size, selected residue matrix and input vector, including the complete zero/support branches and the positive step twist exponent.',
 'Every pair of actual finite matching lifts, including the terminal pair; the fixed weighted latO, original IsThetaAt universal model, splitting characters and stored vacuum are retained.',
 'Every original polynomial vector, with the same ptY/ptX, finite Weil operator and creator normalization. Same residual P-character cancels at the two adjacent levels.',
 'Every original IsIo equation and smooth target vector, with unchanged nuY/nuYprime/nuX and fundamental domains; the integrand has no hidden conjugation.',
 'All b,t,k with k+1<m and all original level vectors; terminal input is exactly range(cX.toMap(prX) composed with HX.e), with the original stored ioX.',
 'The finite projector preserves each original full level unconditionally. Its adjoint identity on the exact row pairs requires DI.3a; global-height moderate growth is not inferred from the per-coset growth field.',
 'Every b,t,w in the specified full level, c in its goodPart and all smooth tuples, with one unchanged mu_b and fd0; equality of all IsMultIP witness sets handles both choice branches.',
 'Both original row sides, all used tuples and all row coordinates; same top projection, all inner maps, final good projection and both normalized row metrics.',
 'Both levels on original toCx3(F), coefficient form, rational cut and Pq; only actual Holds.prim rational tests, Hecke/group and positive-operator clauses are matched to TD1–TD9.',
 'Both sharp and base RowSideDef3 including forms, Mtilde/lattice, and exact composite iota equality for every tuple and coordinate.',
 'Exact original finite group cardinality, subgroup index, two rank equalities and distinguished coefficient embedding; no independent field or frame choice.',
 'Original MK from all nonarchimedean norms and original good subspace; O_L-span(MK intersect good)=Mj under the actual K-form and character-coefficient fields.',
 'Every original target index i<m; the stored Z.jW coordinate vectors are complex-linearly independent and span the full actual target, including zero dimension.',
 'Every target index, every original lattice generator and every rational coordinate; exact two-clause OLatTie with the original coefficient ring and D.O_int.',
 'Literal first DivDef3 on unchanged idsOf(cG,Z,C), colOf(R,F,sEE) and C.NuC, conditional on original data plus RowPairInt; no stronger second-output fields are inferred.',
 'Pointwise installation on the exact CSR-updated Rprime,Fprime,Yprime,Zprime,Cprime,sEE, provided RowPairInt holds there; no new threshold or change to universal NEb/order of selection.',
]
hyps = [
 ['Original common readings, Pins,Holds, exact group rule, and original five real-group predicates.', 'ADDITIONAL retained analytic input DI.3a RowPairInt on every indicated original pair and finite translate; its production remains C.'],
 ['Actual strongly continuous unitary local action and the literal smooth-vector definition.'],
 ['Original HarishChandraModules predicate; no published theorem is counted as checked merely from this source name.'],
 ['Original equivariance and the separately Sobolev-continuous point-evaluation clauses, with one nonzero actual kernel vector.'],
 ['Original selected split primes with conjugate separation, given self-dual frames and lattice, and exact level datum.'],
 ['Original invertibility, block sizes, selected half and integral reduction clauses.'],
 ['Original full Weil datum, self-dual frames and weighted lattice, given vacuum/IsThetaAt, and original LevCh.Is/eta data.'],
 ['Same original finite Weil action, original creator differentiation and the data of DI7.'],
 ['Original active IsIo, both automorphic/level vectors, and the same Haar/fundamental-domain clauses.'],
 ['Original active chain, including IsItW.ne; principal multiplicity membership and exact terminal range.'],
 ['Original grp_record, finite unitary residual characters and RowPairInt(DI.3a).', 'CuspRapidDecay plus a yet-unreconstructed global-height conversion is only a possible source route to this premise.'],
 ['RowPairInt(DI.3a), original discrete-series nontriviality and unchanged mu_b/fd0.'],
 ['Original HilbTie/ProjTie/readings, both metrics and active stored chain; RowPairInt remains.'],
 ['Original Holds.prim rowTest, coefficient form, Hecke/group, levE, sumE, posScal and thmB; Ok3 and exact rational cut.'],
 ['Original supplied forms/lattice fields of Y, exact jEE/jEE0 of Z, and DI13–DI14 including RowPairInt.'],
 ['Original Pins group/level/family ties, rank inequalities and the unchanged selected primes.'],
 ['Original IsKsForm, group stability, chi/psi/e values in Ks, actual MK module and original field inclusion.'],
 ['Original Holds.prim.unif, Holds.aux.levelW, Y.mj.eW norm/range and Z.jW_read.'],
 ['Original Y.mj.eW_lat and abstract finite generator carrier, D.O_int, and the same norm-defined MK/good subspace.'],
 ['All inputs of DI1, expressly including the additional RowPairInt; original hGrp rule, same sEE/ReadC.'],
 ['Original CSR common realization, Pins/Holds/readings/geometry and support, plus RowPairInt on precisely the updated object.', 'Full original NEb and every later uniform guard are retained; no separate choice is made per output.'],
]
claims=[]
for i,title in enumerate(titles,1):
 key=f'DI{i}'
 st=[j for j,s in enumerate(lines) if s.strip()==f'% BEGIN {key}']
 en=[j+1 for j,s in enumerate(lines) if s.strip()==f'% END {key}']
 assert len(st)==len(en)==1 and st[0]<en[0] and anchors[key],key
 block=''.join(lines[st[0]:en[0]]).encode()
 assert all(d in old or d in deps for d in deps[key]),key
 claims.append({'id':key,'title':title,'introduced_in':'0.38','classification':'B',
  'status':'Complete independent human proof in its stated conditional scope',
  'proof_status':'complete in stated scope','review_status':'pending independent mathematical review',
  'depends_on':deps[key],'scope':scopes[i-1],'quantifier_scope':scopes[i-1],
  'hypotheses_retained':hyps[i-1],
  'classical_inputs':(['Existence of Haar measure on a locally compact group, compact integration and finite-dimensional complex linear algebra.'] if key in ('DI2','DI3') else ['Rings of integers of number fields are Dedekind domains; their finite field-extension rings of integers are finite torsion-free modules. The projective dual-basis argument needed here is proved in the block.'] if key=='DI17' else []),
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
input_names={'continuation_notes_v0_37/next_global_assembly.txt'}
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
 rb=''.join(ls[st:en]).encode()
 expected=pl.get('range_sha256',pl.get('sha256'))
 if expected:assert sha(rb)==expected,(key,'inherited proof-range mismatch',sha(rb),expected)
 blocks.append({'id':key,'file':file,'release':'0.37','line_start':st+1,'line_end':en,'sha256':sha(rb),'range_sha256':sha(rb),'file_sha256':sha(b)})
for file in sorted(input_names):
 b=(BASE/file).read_bytes();inputs.append({'file':file,'release':'0.37','sha256':sha(b),'file_sha256':sha(b),'bytes':len(b)})
standing='The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. These are human-reconstruction statuses only.'
remaining=[
 {'id':'DI_COMMON_REALIZATION','classification':'C','role':'retained shared producer','contract':'One actual common R/readers/geometric realization, same columns and periods, with all original Pins/Holds; no replacement model is chosen.'},
 {'id':'DI_ORIGINAL_CHAIN','classification':'C','role':'retained original producer','contract':'Original Holds.aux.ex activates the already stored full chain including nonzero real intertwiners, ioY/ioX and Th. SPR/SBD downstream MMap extension alone does not produce this complete chain.'},
 {'id':'DI_PRIMITIVE_RATIONAL_POSITIVE_DATA','classification':'C','role':'retained original producer','contract':'Actual rational row/lift tests, Hecke/group/level equations, positive theta operators and decompositions in Holds.prim; only their finite consumers are reconstructed.'},
 {'id':'DI_ROW_PAIR_INTEGRABILITY','classification':'C','role':'additional explicit sufficient analytic producer','contract':'For all b,t, original w in full P_b-level Mult, c in its goodPart, all smooth tuples v,vprime and all g in G, integrability of conjugate(A_{R.eG(g)}(c(v))) times w(vprime) on original fd0 with mu_b=ofReal(nP^-1) times nu0. Inverse translates and identity are included. A global row L2 assertion is sufficient but stronger.',
  'unclosed_source_route':'CuspRapidDecay needs IsUnifModerate in the global source height. IsAutFunSm.growth only bounds each finite coset in normInf. ExistsSigmaList.growth_iff uses polynomial unitary reduction; that producer is not reconstructed here.'},
 {'id':'DI_HARISH_CHANDRA_INPUT','classification':'C','role':'retained original representation-theoretic input','contract':'Original HarishChandraModules predicate; the absolute-irreducibility/interpolation consequence is proved conditionally. No new hypothesis-checked published application is asserted.'},
 {'id':'DI_ORIGINAL_LEVEL_AND_INTEGRAL_DATA','classification':'C','role':'retained original common input','contract':'Actual levelW, norm-defined integral K-form and stability, all original read metrics/lattices, and hGrp on the same common realization.'},
 {'id':'DI_STRONGER_DIVROWS3','classification':'B','role':'separate implication reconstruction with upstream C data','contract':'The second output DivRows3: both row-lattice metric comparisons, rational-lift cut, actual all-tuple thTheta square, numerical index identities and column pairing; retain original MjHTie, IdxDefs, BuRational and BtVanish as applicable.'},
]
closed=[
 {'id':'DI_LOCAL_HC_SEPARATION','claims':['DI2','DI3','DI4'],'contract':'Actual smooth tensor equivariant defects vanish if they kill one nonzero original kernel vector. Compact polynomial averages and finite interpolation prove this directly.','requires':['original HarishChandraModules','original unitary model and separate Sobolev evaluation']},
 {'id':'DI_ORIGINAL_LEVEL_IDENTITIES','claims':['DI5','DI6','DI7','DI8','DI9','DI10'],'contract':'Literal StepLev and TopLev on both original levels, all tuples and exact terminal range, with unchanged stored maps, finite characters and measures.','requires':['original Pins/Holds and active stored chain','DI_LOCAL_HC_SEPARATION']},
 {'id':'DI_ROW_PROJECTOR_CONSUMER','claims':['DI11','DI12'],'contract':'Original RowProj, including unchanged ipM choices in both empty and nonempty scalar-witness branches.','requires':['original grp_record/full levels/model','DI_ROW_PAIR_INTEGRABILITY']},
 {'id':'DI_BOTH_COMPOSITE_ROW_IDENTITIES','claims':['DI13','DI14','DI15'],'contract':'Both composite theta/good-projection equations and both literal RowSideDef3 records; actual Pq and nP normalization.','requires':['DI_ORIGINAL_LEVEL_IDENTITIES','DI_ROW_PROJECTOR_CONSUMER','original readers/HilbTie/ProjTie and primitive rational/positive data']},
 {'id':'DI_FIRST_THETA_SUBRECORD','claims':['DI16','DI17','DI18','DI19'],'contract':'The original first ThDef3.li/span/lat, including exact OLatTie on original generators via integral descent; no thTheta square.','requires':['original integral K-form and coefficient fields','original eW metric/range/lattice and jW_read','original uniform/levelW data']},
 {'id':'DI_FIRST_DIVDEF3_CONSUMER','claims':['DI20'],'contract':'All nine first DivDef3 fields on unchanged idsOf/colOf/NuC, under DI1 including the explicit additional RowPairInt. This is not yet the full original source theorem from its original premises alone.','requires':['DI_BOTH_COMPOSITE_ROW_IDENTITIES','DI_FIRST_THETA_SUBRECORD','original group/cardinality/readings/ReadC and fixed sEE']},
 {'id':'DI_CSR_UPDATED_INSTALLATION','claims':['DI21'],'contract':'Pointwise application on the literal CSR-updated Rprime/Fprime/Yprime/Zprime/Cprime/sEE, replacing the unexpanded first-Div premise by the exact row-pair producer and other retained inputs.','requires':['DI_FIRST_DIVDEF3_CONSUMER','CSR11–CSR13 exact update','RowPairInt on that same updated datum','original universal NEb/common threshold order']},
]
for x in closed:x.update({'classification':'B','status':'closed conditional implication','dependency_mode':'sufficient conjunction in the expressly stated scope'})
not_closed=[
 'Production of the actual common R, readings, geometry, positive/rational inputs and stored whole chain.',
 'RowPairInt on the same actual updated datum; no silent IsAutFunSm-to-global-height conversion or generic cusp-decay application.',
 'The original all-data CuspRapidDecay predicate and its global-height moderate-growth dictionary.',
 'The separate stronger DivRows3/theta square, ratG/MLat, actual eigensystem/parts/logLam and host/common-selector producers.',
 'Any additional selected whole-leaf closure or unconditional RH/Dirichlet-GRH theorem.',
]
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.38','date':'2026-11-22','component':COMPONENT,
 'source_commit':PIN,'repository':'CocoSgt/riemann-hypothesis-lean','standing_assumption':standing,
 'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),
 'range_convention':'Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.',
 'metadata_builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable_invocation':'python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v037','source_anchor_file':'source_anchors.txt','source_anchor_sha256':sha((HERE/'source_anchors.txt').read_bytes())},
 'claims':claims,'claim_total':len(claims),'external_literature':[],'published_applications':[],
 'inherited_proof_inputs':inputs,'inherited_proof_blocks':blocks,'not_closed':not_closed,
 'source_files':[{'path':p,'sha256':sha(b),'file_sha256':sha(b),'bytes':len(b),'line_count':len(ls),'verified_equal_to_pinned_git_blob':True} for p,(b,ls,_) in sorted(cache.items())]}
dump('provenance.json',prov);dump('published_applications.json',[])
closure={'schema':'rh-human-component-closure/1','version':'0.38','component':COMPONENT,'source_commit':PIN,
 'standing_assumption':standing,'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'new_claim_ids':[c['id'] for c in claims],'closed_contracts':closed,'remaining_inputs':remaining,'selected_top_level_leaf_closed':False,
 'same_object_guards':['One original R,F,Y,Z,C and actual sEE; exact CSR update only.','Same stored chain, full IsItW.ne and original terminal range; no arbitrary isomorphic replacement.','Both exact row levels and mu_b=ofReal(nP^-1) times nu0 on the same fd0.','Actual weighted latO including its fractional ideal and exact splitting/flag character signs.','One original norm-defined MK, original good subspace, base embedding and finite lattice generators.','ReadC is chosen before later TwArgs; no new asymptotic threshold and no reordering/specialization of universal NEb.','RowPairInt is an additional retained analytic supplier, not a conclusion of record transport or the unproved global growth dictionary.'],
 'not_closed':not_closed,'review_status':'pending independent mathematical review'}
dump('closure.json',closure)
loc=[f'DI source locators — {PIN}','Inclusive one-based source/proof lines and exact byte hashes.',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
 p=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
 for s in c['sources']:loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
 loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
validation={'status':'PASS','source_commit':PIN,'main_sha256':sha(raw),'claims':len(claims),'claim_source_references':sum(len(c['sources']) for c in claims),'distinct_source_ranges':len(ranges),'source_files':len(cache),'inherited_files':len(inputs),'inherited_claim_blocks':len(blocks),
 'checks':['Pinned HEAD and every referenced Git blob','Unique source anchors and all marked human proof ranges','All depends_on entries indexed in baseline/new claim ledgers','New-claim dependency DAG acyclic','Exact source/proof/inherited-input hashes and fresh DI prefix','No unexpected control characters'],
 'not_performed':'No Lean compilation or kernel replay; independent mathematical review and standalone draft TeX are separately recorded.'}
dump('validation.json',validation)
report='''v0.38 — first division identity, DI1–DI21

The finite/representation-theoretic first-output consumer is reconstructed
on the actual common readers. DI2–DI4 give compact polynomial smoothing,
HC scalar endomorphisms, finite interpolation and tensor separation.
DI5–DI10 construct original finite level lifts, calculate both type and
twist characters, transport the exact weighted vacuum, commute the finite
Weil action with every creator, and prove StepLev/TopLev from the unchanged
original intertwiner integral. Both levels and the exact terminal range
are retained. No full Fock cyclicity supplier is simply invoked.

DI11–DI12 prove the finite projector adjoint and the literal RowProj
consumer by equality of the IsMultIP scalar-witness sets, including the
empty-witness zero fallback. This uses an ADDITIONAL retained RowPairInt
premise over every original pair and finite translate, with unchanged
mu_b and fd0. The source CuspRapidDecay-to-integrability route needs the
global height growth conversion; IsAutFunSm only supplies finite-coset
normInf bounds. ExistsSigmaList.growth_iff uses polynomial unitary
reduction, and that argument is not reconstructed here. Accordingly no
full original first-Div theorem from its original premises alone is claimed.

DI13–DI15 prove both original composite identities and RowSideDef3
records, matching the retained rational/positive primitive inputs to
TD1–TD9 and checking the finite quotient projection with its exact nP.
DI16–DI19 prove original cardinalities/ranks/base place, integral descent
via a projective dual basis of O_L over O_K, independence/span of actual
Z.jW, and the exact OLatTie on original finite generators. DI20 checks
all nine first DivDef3 fields. DI21 installs this implication on CSR's
literal updated readers, preserving one prior ReadC, both metrics,
all original maps, the universal NEb guard and common-threshold order.

The common realization, geometric/rational/positive producers, complete
stored chain, row-pair analytic producer and exact level/integral inputs
remain. The stronger DivRows3 output, ratG/MLat, spectral/parts/logLam
and host/common-selector branches are separate. No selected whole leaf
is additionally closed by this component. Formal source correctness is
assumed throughout. The proof uses no Lean build or kernel replay.
'''
report+=f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE/'closure.json').read_bytes())}\n"
report+=f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} source files; {len(inputs)} inherited files; {len(blocks)} inherited proof blocks.\n"
(HERE/'report.txt').write_text(report)
print(json.dumps({**validation,'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))
