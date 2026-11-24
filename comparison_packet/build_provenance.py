#!/usr/bin/env python3
"""Rebuild PKT provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v039

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
COMPONENT = "comparison_packet"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v039")
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"PKT\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written PKT block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


anchors = {f"PKT{i}": [] for i in range(1, 31)}
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
 'Original interfaces and selection order',
 'Positive complexification with the exact integral carrier',
 'Actual central group-algebra action and complete Sp1/Tie1',
 'Finite congruence orbits and the original smooth admissible unitary space',
 'Projection onto arbitrary invariant subspaces through finite fixed spaces',
 'Algebraic irreducible decomposition of every smooth vector',
 'Actual finite-type function models and orthogonality of distinct types',
 'Good cuts preserve the decomposition and the actual Reps catalogue is finite',
 'Conjugate row types and adapted original row bases',
 'Actual definite compact models, tensor irreducibility and perfect pairing',
 'Original compact forms realize every definite multiplicity map',
 'Compact Schur unfolding with literal measure and class-sum normalization',
 'Exact row/lift level spans and original coordinate Gram identities',
 'Actual Hilbert level models and all three Riesz transitions',
 'Both complete original ChT chain comparisons',
 'Exact original good integral carrier in the target model',
 'Target Hilbert model with the original nP(F,false) normalization',
 'Prescribed source embeddings and the conditional original theta map',
 'Complete original LfT lift comparison',
 'Sharp original RrT coordinates, full multiplicity dimension and delp',
 'Full original exists_pkT with literal mL and all dependent ties',
 'Standard finite frames and all original Hd fields',
 'All original Mat1 laws and exact tuple-restriction identities',
 'Actual period coordinates and complete PerT',
 'Prescribed auxiliary rows, exact integer weights and Sha dictionary',
 'One numerical record valid for every later eta and V/S/N/G',
 'Full original rowPk_nonempty',
 'Original geometric realization copied with the same finite group',
 'Every comparison map, metric and sharp coordinate preserved by copying',
 'Full original exists_moved with Copy/Coh and precise reader boundary',
]
deps = {
 'PKT1':[], 'PKT2':[], 'PKT3':['PKT2'],
 'PKT4':['MR3','MR4'], 'PKT5':[], 'PKT6':['PKT5'],
 'PKT7':['PKT4','PKT5','PKT6'], 'PKT8':['PKT4','PKT6','PKT7'],
 'PKT9':['PKT8'], 'PKT10':[], 'PKT11':['PKT10'],
 'PKT12':['PKT10','PKT11','MR1'],
 'PKT13':['PKT3','PKT11','PKT12','MR1','MR2','TL7'],
 'PKT14':['PKT10','PKT13'], 'PKT15':['PKT9','PKT14'],
 'PKT16':['PKT2','DI17'], 'PKT17':['PKT16'],
 'PKT18':['PKT3','PKT13','PKT17','DI4'],
 'PKT19':['PKT9','PKT16','PKT17','PKT18'],
 'PKT20':['PKT15','RDR7'],
 'PKT21':['PKT1','PKT3','PKT8','PKT15','PKT19','PKT20'],
 'PKT22':['PKT11','DR1'], 'PKT23':['PKT3','PKT21','TL5','TL7'],
 'PKT24':['PKT3','MR1','MR2'],
 'PKT25':['PKT2','PKT24','MR1','TL6','TL7','LS18'],
 'PKT26':[], 'PKT27':['PKT21','PKT22','PKT23','PKT24','PKT25','PKT26'],
 'PKT28':[], 'PKT29':['PKT28'],
 'PKT30':['PKT27','PKT28','PKT29','RDR12','RDR20','RDR21','RDR22','RPI14','RPI15'],
}
scopes = [
 'One original D/G/A3/Ks/R/F and Hd, fixed mA/mL with all laws and literal coordinate equalities, before any packet or reader is selected.',
 'Every matrix record under the original star-preserving embedding and integral O action; exact O-lattice carrier j(N), full span and all O_K stability, including dimension zero.',
 'Every finite group and original central-only matrix action; complete Sp1/Tie1, with no claim of full noncentral multiplicativity.',
 'Original Minf, both levels, same unitary action and ipM; finite congruence orbits, smoothness/admissibility/positivity from explicitly retained Inputs.',
 'Every positive Hermitian representation, fixed subgroup with finite orbits and finite-dimensional fixed space; arbitrary invariant submodule, no completion.',
 'Every fixed vector is an algebraic finite sum of irreducible vectors; induction in fixed-space dimension, applied to original Minf.',
 'Literal FinTyp function-space realization and original action; nonisomorphic irreducible/isotypic subspaces are orthogonal.',
 'Original e0 and all level-character kernels, same two row sides; full finite Reps contract without additional catalogue assumption.',
 'Original isotE conjugate convention and isotL direct convention, shared representatives, both row sides and all lift target parts; exact basis/type spans.',
 'Original definite DS models, finite smooth compact realization, tensor irreducibility and actual prX perfect pairing; original PrIso and dimensions.',
 'Full original IsMultMap regularity and exact TopMultH range, finite coefficient forms and same pairing/action; no undefined intertwiner choice.',
 'Original definite Haar measure with level preimage mass one, actual class presentation/stabilizers, dimension coefficient and exact ipMT.',
 'Original row and lift coordinate bases, finite levels/characters, exact span equalities and Gram constants nP(F,b) or nP(F,false).',
 'All original used tuples and chain indices; finite Hilbert models of actual subspaces, three distinct Riesz transition identities and unchanged pairings.',
 'Both complete ChT on fixed sA, one shared Reps catalogue, original jE/jM/jX, zero unused transitions, all type and top-coordinate equalities.',
 'Same original FW.MK over O_Ks, Wgood with psi0 inverse and actual e, original good integral descent; exact O carrier through any injective E of prescribed range.',
 'Same original HW/e and target Wc, rescaled basis E with squared norm nP(F,false), exact good lattice and zero targets outside 1<=j<=m.',
 'Every used tuple and target index; jMt exact coordinate range/metric, theta identity conditional on an original MultW map with given low restriction and good projected image.',
 'All original LfT fields on the fixed sL family, including actual MK carrier, source/target maps, conditional theta, out/junk, isot/disj and literal lift coordinate read.',
 'True-level original jE, full exact RrT with all embeddings and cpt; Dall is full pre-cut multiplicity dimension; delp<=1 and n=(1-delp)Dall, including Dall=0.',
 'Complete exists_pkT on its stated original premises; literal p.mL=mL, simultaneous dependent ties and no additional supplier premise.',
 'Original given z0 and standard self-dual Y0/Wi lattices, host maximal-real equality; all Hd fields with tup=ixOf and same frame maps.',
 'Actual all-tuples mAU/mLU, central-only compressed action, all ten laws, exact restricted-family equalities and zero-index cases.',
 'Same original row spaces and frame-reduction maps, all words/tuples; full PerT and SameForm identities with exact coordinate maps.',
 'Full original auxiliary RowsRest stand-ins, original periods and ramified form, prescribed conjugate-invariant muAt/muTw, literal signed integer weights and ShaOK only in its conditional finite-length sense.',
 'One Nums chosen from p/d/W0 before arbitrary nonnegative eta and all later V/S/N/G; exact conditional ze, trace lam, Bu, local lattice indices including signed-length definitions.',
 'Whole original rowPk_nonempty including all universal KapDef/NumOK and every matrix/period/tuple field; given z0 retained.',
 'Same z0 and later o under original Holds/ExAt/InGeo/GrpTrue/Fits; cpDat keeps original Xg, trace, core, fields, geometry and maps, with explicit finite-group and pins transport.',
 'Same original comparison choices on both stages, exact multiplicity/good spaces, measures, maps, lattices, original type conventions and all-place RrT; etaOf and W1 unchanged.',
 'Whole exists_moved with Copy and all nine Coh clauses; joins to existing readers on same objects; full ReadL still has the original eta agreement and no outer producer inferred.',
]
base_hyp='The original fixed Inputs(D), Pins(R,F,cG), Holds(R,F), original representation/model/geometric data and all same-object conditions stated in PKT1; these are supplied premises, not reconstructed by this component.'
hyps={f'PKT{i}':[base_hyp] for i in range(1,31)}
hyps.update({
 'PKT2':['Original Mat1.Laws, star-compatible embedding, integral image of O; no O onto O_K premise.'],
 'PKT3':['PKT2 and finite G; multiplicativity of op only on central inputs.'],
 'PKT5':['Positive Hermitian form, unitary group action, finite K-orbits and finite-dimensional K-fixed space.'],
 'PKT6':['PKT5 hypotheses; invariant subspaces and ordinary finite-dimensional choice.'],
 'PKT10':['Original definite signature, unitary irreducible DS representation and finite nonzero lowest compact type, actual nonzero dual pairing and its PrIso normalization.'],
 'PKT16':[base_hyp,'Original FW IsKsForm/IntegralNorm/stability, keep.valKs/levKs, actual hO into Ks, and injective E with specified range.'],
 'PKT18':[base_hyp,'The theta conclusion has the original existing-w antecedent; no new arbitrary or unprovided intertwiner.'],
 'PKT22':['Original B,f,T,w,Z0,hX,Wt and given Dat z0; Inputs, Holds, host F=maximalRealSubfield(E), standard self-dual Y0 and every Wi lattice; original unramified CM host.'],
 'PKT23':['Same given z0, w.ok, z0.good.irr, literal all-tuples matrices and original finite action/class-sum form.'],
 'PKT24':['Same original TC/Cols data, I.Ok, Pins, Laws and fields.Ok; actual disjoint vGs and Q(a), prescribed p and complexification ties.'],
 'PKT25':['Same original column data and positive ramified metric; original character image and conjugation-stable Wt; no global Sha-finiteness assertion.'],
 'PKT26':['Any fixed original p, PerD and W0; all later parameters remain universally quantified; ze equation retains its factorization/nonzero/value antecedents.'],
 'PKT27':['Exactly original rowPk_nonempty premises including host equality, all StdLat, Inputs/Holds and conjugation invariance of Wt.'],
 'PKT28':['Given original q:RowPk and later o:Over, Holds(z0), ExAt(z0), InGeo(z0), GrpTrue(Z0.N,f) and Fits(o).'],
 'PKT29':['SameGrp, exact same tuple/frame maps and transported original realization; no fresh model, lattice, basis, measure or representation choice.'],
 'PKT30':['Exactly original exists_moved premises; full ReadL separately retains original o.eta=q.eta for every 1<=j<=m and all places.'],
})
claims=[]
for i,title in enumerate(titles,1):
 key=f'PKT{i}'
 st=[j for j,s in enumerate(lines) if s.strip()==f'% BEGIN {key}']
 en=[j+1 for j,s in enumerate(lines) if s.strip()==f'% END {key}']
 assert len(st)==len(en)==1 and st[0]<en[0] and anchors[key],key
 block=''.join(lines[st[0]:en[0]]).encode()
 assert all(d in old or d in deps for d in deps[key]),key
 claims.append({'id':key,'title':title,'introduced_in':'0.40','classification':'B',
 'status':'Complete independent human proof in its stated conditional scope','proof_status':'complete in stated scope',
 'review_status':'pending independent mathematical review','depends_on':deps[key],
 'scope':scopes[i-1],'quantifier_scope':scopes[i-1],'hypotheses_retained':hyps[key],
 'classical_inputs':(['Finite-dimensional complex spectral theorem/Gram-Schmidt; finite-dimensional Riesz representation and ordinary basis choice.'] if i in (2,5,9,10,14,17,18,22,25) else []),
 'proof_location':{'file':COMPONENT+'/main.tex','paragraph':key,'label':'claim:'+key,
 'line_start':st[0]+1,'line_end':en[0],'bytes':len(block),'sha256':sha(block),'range_sha256':sha(block),'file_sha256':sha(raw)},'sources':anchors[key]})
visited,visiting=set(),set()
def visit(k):
 if k in visited or k not in deps:return
 assert k not in visiting,('cycle',k)
 visiting.add(k)
 for d in deps[k]:visit(d)
 visiting.remove(k);visited.add(k)
for k in deps:visit(k)
inputs,blocks=[],[]
input_names={'continuation_notes_v0_39/next_division_and_readings.txt'}
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
 blocks.append({'id':key,'file':file,'release':'0.39','line_start':st+1,'line_end':en,'sha256':sha(rb),'range_sha256':sha(rb),'file_sha256':sha(b)})
for file in sorted(input_names):
 b=(BASE/file).read_bytes();inputs.append({'file':file,'release':'0.39','sha256':sha(b),'file_sha256':sha(b),'bytes':len(b)})
standing='The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. These are human-reconstruction statuses only.'
closed=[
 {'id':'PKT_ACTUAL_SP1_TIE1','claims':['PKT2','PKT3'],'contract':'Full original complexification of definite group forms, with actual central action and exact O-lattice image/stability.','requires':['original Mat1.Laws','star-compatible embedding and integral O action']},
 {'id':'PKT_ACTUAL_REPS','claims':['PKT4','PKT5','PKT6','PKT7','PKT8','PKT9'],'contract':'Complete finite actual Reps catalogue on both original row levels; algebraic irreducible decomposition, exact good cuts, conjugate row convention and adapted orthonormal bases.','requires':['original Inputs, Pins and Hd','actual smooth admissible unitary Minf supplied by original Inputs']},
 {'id':'PKT_BOTH_CHT','claims':['PKT10','PKT11','PKT12','PKT13','PKT14','PKT15'],'contract':'Both original complete ChT with actual top coefficient realization, exact class-sum/Schur factors, finite Hilbert/Riesz construction and every coordinate/transition/type field.','requires':['original Inputs/Pins/Holds','fixed Mat1/Tie1 data','PKT_ACTUAL_REPS']},
 {'id':'PKT_COMPLETE_LFT','claims':['PKT16','PKT17','PKT18','PKT19'],'contract':'Complete original LfT including actual MK good lattice, target nP factor, exact source range/metric, conditional theta extension using a left inverse, and every type/out/read field.','requires':['original Inputs/Pins/Holds and coefficient-field hO','fixed original source complexifications','PKT_ACTUAL_REPS']},
 {'id':'PKT_EXISTS_PKT','claims':['PKT20','PKT21'],'contract':'Whole original exists_pkT: p.mL=mL and Nonempty PkT with same catalogue, both ChT, full LfT, Dall/delp and sharp RrT.','requires':['exact original exists_pkT premises','PKT_ACTUAL_SP1_TIE1','PKT_BOTH_CHT','PKT_COMPLETE_LFT','inherited RDR7 sharp original coordinate proof'],'additional_premises_beyond_original_source':[]},
 {'id':'PKT_ROWPK_NONEMPTY','claims':['PKT22','PKT23','PKT24','PKT25','PKT26','PKT27'],'contract':'Whole original rowPk_nonempty on given z0; all Hd/Mat1/PerT/RowsRest/tuple/Sha fields and one Nums before every eta>=0,V,S,N,G.','requires':['exact original rowPk_nonempty premises including original given Dat, Inputs/Holds, host equality, all StdLat and conjugation-stable Wt','PKT_EXISTS_PKT'],'additional_premises_beyond_original_source':[]},
 {'id':'PKT_EXISTS_MOVED','claims':['PKT28','PKT29','PKT30'],'contract':'Whole original exists_moved, with full Copy and all nine Coh fields on the same original package and every fitting later stage.','requires':['given RowPk q and later Over o','original Holds/ExAt/InGeo/GrpTrue(Z0.N,f)/Fits(o)'],'additional_premises_beyond_original_source':[]},
 {'id':'PKT_TO_ACTUAL_READERS','claims':['PKT30'],'contract':'The completed packet/moved constructors join to RDR original level-zero side/ReadPk and RPI first DivDef3 on the same data; full ReadL still requires the original eta agreement.','requires':['PKT_ROWPK_NONEMPTY','PKT_EXISTS_MOVED','original reader/Fits guards','inherited RDR12/RDR20/RDR21','inherited RPI14/RPI15','original eta agreement only for the separate full ReadL conclusion']},
]
for x in closed:x.update({'classification':'B','status':'closed conditional implication','dependency_mode':'sufficient conjunction in the explicitly stated original scope'})
remaining=[
 {'id':'PKT_COMMON_GIVEN_REALIZATION','classification':'C','role':'retained outer common producer','contract':'One original common Dat z0 with original R/F, same core, geometry, finite classes, periods, columns, trace data and coefficient fields; no existence of z0 follows from the packet.'},
 {'id':'PKT_ORIGINAL_INPUTS_PINS_HOLDS','classification':'C','role':'retained original input package; constituent statuses governed by cumulative audit','contract':'Exactly the original Inputs (including Schur/HC/Petersson and representation data), Pins and Holds on this same z0. Existing human suppliers may discharge constituent clauses, but this component does not create the common package.'},
 {'id':'PKT_EXAT_INGEO_CORE','classification':'C','role':'retained geometric supplier','contract':'Original ExAt, InGeo and actual CoreP where required; copying preserves them and does not prove their existence.'},
 {'id':'PKT_ACTUAL_FITS','classification':'C','role':'retained later-stage supplier','contract':'Same o:Over with original DivIs sharp rational tests/metric/RRDef, GrpTrue, GrpAt and universal standard-read CenIs. No ratG/MLat or local arithmetic installation is inferred.'},
 {'id':'PKT_ETA_AGREEMENT','classification':'B','role':'exact original full-ReadL guard','contract':'For all 1<=j<=m and all places v, o.eta(j,v)=q.eta(j,v). Moved.eta proves only etaOf(copy)=etaOf(original); arbitrary eta in Over remains arbitrary.'},
 {'id':'PKT_SECOND_DIVISION_ROWS','classification':'C','role':'retained stronger comparison producer','contract':'Original stronger DivRows3 theta/primitive row comparison and compatible selector/duties remain outside this packet; first DivDef3 and RowPairInt are already closed by RPI/DI.'},
]
not_closed=[
 'Outer existence of the original common geometric Dat, Inputs/Pins/Holds, ExAt/InGeo or compatible selector/duties.',
 'An actual Fits/rational-test/ratG/MLat/local arithmetic producer or stronger DivRows3.',
 'Full ReadL for arbitrary eta without the exact original agreement.',
 'An unconditional theta extension from arbitrary input x: LfT.theta retains its original existing-w antecedent.',
 'Nonvanishing of new periods, unconditional period factorization, or finiteness of every Sha length.',
 'A common threshold or whole-family producer from these pointwise given-data constructors.',
 'Any additional whole selected-leaf closure or unconditional RH/Dirichlet-GRH statement.',
]
prov={'schema':'rh-human-component-provenance/1','artifact_version':'0.40','date':'2026-11-22','component':COMPONENT,
 'source_commit':PIN,'repository':'CocoSgt/riemann-hypothesis-lean','standing_assumption':standing,
 'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),
 'range_convention':'Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.',
 'metadata_builder':{'file':'build_provenance.py','sha256':sha(Path(__file__).read_bytes()),'portable_invocation':'python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v039','source_anchor_file':'source_anchors.txt','source_anchor_sha256':sha((HERE/'source_anchors.txt').read_bytes())},
 'claims':claims,'claim_total':len(claims),'external_literature':[],'published_applications':[],
 'inherited_proof_inputs':inputs,'inherited_proof_blocks':blocks,'not_closed':not_closed,
 'source_files':[{'path':p,'sha256':sha(b),'file_sha256':sha(b),'bytes':len(b),'line_count':len(ls),'verified_equal_to_pinned_git_blob':True} for p,(b,ls,_) in sorted(cache.items())]}
dump('provenance.json',prov);dump('published_applications.json',[])
closure={'schema':'rh-human-component-closure/1','version':'0.40','component':COMPONENT,'source_commit':PIN,
 'standing_assumption':standing,'main_sha256':sha(raw),'main_tex_sha256':sha(raw),'sha256':sha(raw),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
 'new_claim_ids':[c['id'] for c in claims],'closed_contracts':closed,'remaining_inputs':remaining,
 'selected_top_level_leaf_closed':False,
 'same_object_guards':[
 'One original D/G/A3/R/F/Ks and all fixed Mat1 records before the packet and reader.',
 'One finite Reps catalogue on both original row levels, preserving isotE conjugate and isotL direct conventions.',
 'Both original Haar measures/fundamental domains and nP(F,true)/nP(F,false) constants; actual class weights.',
 'Exact target MK and Wgood(P0,psi0 inverse,e), original FW.j/sg0, and E squared norm nP(F,false).',
 'Original theta identity is conditional on the same existing w, not an arbitrary substituted intertwiner.',
 'One Nums before every nonnegative eta and every later V/S/N/G; conditional ze and Sha clauses retained.',
 'Copied realization keeps Xg, trace data, fields, core, real data and all nine Coh functions.',
 'Full ReadL retains eta equality; no new RowPairInt premise because RPI14/RPI15 already close it.',
 'Pointwise original constructors do not alter outer common-family, NEb, selection or threshold order.'],
 'not_closed':not_closed,'review_status':'pending independent mathematical review'}
dump('closure.json',closure)
loc=[f'PKT source locators — {PIN}','Inclusive one-based source/proof lines and exact byte hashes.',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
 p=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {p['line_start']}-{p['line_end']} SHA256 {p['sha256']}")
 for s in c['sources']:loc.append(f"  {s['path']}:{s['line_start']}-{s['line_end']} | {s['declaration']} | file {s['sha256']} | range {s['range_sha256']}")
 loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
validation={'status':'PASS','source_commit':PIN,'main_sha256':sha(raw),'claims':len(claims),
 'claim_source_references':sum(len(c['sources']) for c in claims),'distinct_source_ranges':len(ranges),'source_files':len(cache),
 'inherited_files':len(inputs),'inherited_claim_blocks':len(blocks),
 'checks':['Pinned HEAD and every referenced Git blob','Unique source anchors and all marked human proof ranges','All depends_on entries indexed in baseline/new claim ledgers','New-claim dependency DAG acyclic','Exact source/proof/inherited-input hashes and unused PKT prefix','No unexpected control characters'],
 'not_performed':'No Lean compilation or kernel replay; mathematical peer review and standalone draft TeX are separately recorded.'}
dump('validation.json',validation)
report='''v0.40 — original comparison packet, PKT1–PKT30

PKT21 proves full original exists_pkT, without an extra Reps or
intertwiner premise. The substantial new argument is the algebraic
decomposition of smooth admissible unitary Minf: finite fixed-space
projections onto arbitrary invariant subspaces, a minimal fixed-dimension
irreducible subspace, and induction on that dimension. It constructs
actual FinTyp function models and proves orthogonality. The original
good cut is handled componentwise, yielding one finite Reps catalogue
for both original row levels with the exact conjugate-type convention.

The actual definite coefficient model, compact Schur/unfolding identity,
finite character projectors, original class-sum Gram factors and finite
Riesz constructions give both complete ChT. The lift has exact original
MK/Wgood carrier, nP(F,false) scaling, source coordinates and conditional
theta identity. A linear left inverse to lowest-type restriction proves
that conditional identity; existence of a new multiplicity extension is
not asserted. Dall, delp and sharp all-place RrT use the same original
objects, with inherited RDR7 supplying the exact coordinate theorem.

PKT27 proves full original rowPk_nonempty on a given realization.
It constructs standard finite frames from the original self-dual
lattices, all Mat1 laws, literal all-tuples restrictions, actual period
SameForm coordinates, the permitted auxiliary RowsRest, signed integral
weights, ShaOK in its exact scope, and one Nums chosen before every
later eta/V/S/N/G. Period factorization and Sha-finiteness guards are
preserved. The numerical local-index comparison is proved by injective
localization and quotient isomorphisms, rather than source invocation.

PKT30 proves full exists_moved, Copy and all nine Coh fields on the same
package. The original realization is copied under the original finite
group/place identification, keeping all original maps, coefficient and
integral objects, measures, periods and sharp frames. Original Fits,
Holds, ExAt and InGeo remain premises. It joins to the completed RDR
readers; full ReadL still needs the exact eta agreement. No new generic
RowPairInt is needed, and no outer common producer, actual rational
or geometric supplier, stronger DivRows3, selector or threshold is closed.

All source correctness is assumed. No Lean build/replay was used.
No new published deep application is claimed; published_applications.json
is the empty list. All inherited human inputs are separately hash-bound.
'''
report+=f"\nmain.tex SHA256 {sha(raw)}\nprovenance.json SHA256 {sha((HERE/'provenance.json').read_bytes())}\nclosure.json SHA256 {sha((HERE/'closure.json').read_bytes())}\n"
report+=f"{len(claims)} claims; {validation['claim_source_references']} claim/source references; {len(ranges)} distinct ranges; {len(cache)} source files; {len(inputs)} inherited files; {len(blocks)} inherited proof blocks.\n"
(HERE/'report.txt').write_text(report)
print(json.dumps({**validation,'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))
