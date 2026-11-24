#!/usr/bin/env python3
"""Rebuild HLP provenance from exact pinned Lean bytes and marked human proofs.

python3 build_provenance.py --source /path/to/lean_source \
    --baseline /path/to/reconstruction_v040

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
COMPONENT = "local_hecke_projection"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, default=HERE.parents[1] / "lean_source")
parser.add_argument("--baseline", type=Path, default=HERE.parents[1] / "reconstruction_v040")
parser.add_argument("--companions", type=Path, default=HERE.parent)
args = parser.parse_args()
SOURCE, BASE = args.source.resolve(), args.baseline.resolve()
COMPANIONS = args.companions.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip() == PIN
old = {c["id"]: c for c in json.loads((BASE / "provenance.json").read_text())["claims"]}
assert not any(re.fullmatch(r"HLP\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written HLP block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }

a='src/Development/AbelianVarietyTheory/'
p=a+'Proofs/IwasawaDecomposition/'
f='src/Formalism/LocalToGlobal/NumberFieldFamilies/'
n='src/Formalism/LocalToGlobal/NormalizedHeckeFactors/'
d=a+'Definitions/AutomorphicMembership/'
anchors={f'HLP{i}':[] for i in range(1,33)}
anchor_rows=[]
def add(ids,path,names):
    for name in names.split(';'):
        entry=source(path,name)
        for key in ids.split():
            assert key in anchors,key
            if entry not in anchors[key]:anchors[key].append(entry)
    anchor_rows.append(ids+'|'+path+'|'+names)
add('HLP1 HLP3 HLP8',d+'RingSpecNormalisedCharacterEq.lean','MtInput')
add('HLP1 HLP9 HLP10 HLP12 HLP13 HLP14',f+'NPartCNd.lean','GenAt0;LocBase0;heckeAlg0;LocT;XOf;TOf;partOf;offOf;PartCompl;projOf;latL;MtSub;MtLoc;mtEquiv;prMtC')
add('HLP2',p+'ExistsCoefficientLinearLiftDoubleCosetOperators.lean','unif_ne_zero;tSet_subset_of_unif;tSet_eq_of_unif;tN_eq_of_conj')
add('HLP2',a+'Proofs/FlagMeasures/CmFieldSplitPlaceEqOfPlaceEq.lean','le_one_iff_frac;exists_approx;eq_of_le_one_iff;splitPlace_eq_of_w_eq')
add('HLP3',p+'ExistsCoefficientLinearLiftDoubleCosetOperators.lean','heckeLift')
add('HLP3 HLP4 HLP7',f+'HeckeLift0.lean','HeckeLift0;hLC;hLC_spec;hKC;hKC_def;SplitK;baseC')
add('HLP3 HLP4 HLP7 HLP32',p+'UnitsLiftSpec.lean','GenHyp;base;genAt_iff')
add('HLP4',p+'LiftedHeckeOperatorsAtGeneratorsCommute.lean','hLC_commute')
add('HLP5',p+'HeckeStandardFactsOnLocalisationBase.lean','exists_complexify;isRoot_of_eig;finite_MtL')
add('HLP6',p+'HeckeStandardFactsOnLocalisationBase.lean','coeff_prod_isIntegral;coeff_isIntegral_of_roots;mem_range_of_roots')
add('HLP7',p+'HeckeStandardFactsOnLocalisationBase.lean','root_int;heckeStd0_base')
add('HLP8',p+'HeckeOperatorIntegralOnLatticeAtTwistedPlaces.lean','exists_preimage_comb;heckeIntTw_base')
add('HLP8 HLP16 HLP20',p+'UnitsLiftSpec.lean','HeckeIntTw;SemisimpleTw;ActHK')
add('HLP9 HLP10 HLP12 HLP21',f+'NPartCNdStd.lean','HeckeStd0;FinDimV;partCompl_of;xNe_of;xFin_of;locsFin_of;tSep')
add('HLP10 HLP29',f+'NPartCNdTie.lean','mxC;mxC_self;mxC_max;mxC_inj;mxC_all;ptX_val')
add('HLP11 HLP12',f+'JMtInjective.lean','jMt_injective;latL_finite;mtSub_fg;mtSub_finite;mtSub_free')
add('HLP11 HLP13',f+'IsLocalizedOfSpan.lean','span_top_of_image;isLocalized_of_span;span_image_top;span_latL;span_mtSub;mtLoc_holds')
add('HLP14',f+'NPartCNdTie.lean','PsiC;PsiC_inj;PsiC_range;PsiC_pr')
add('HLP14 HLP15',f+'NPartCNdProj.lean','prMtC_lat;prMtC_latSpan;prMtC_span')
add('HLP16',p+'HeckeOperatorsOnLocalisationSpaceSemisimple.lean','isSemisimple_baseChange;isSemisimple_of_sq;apply_eq_zero_of_sq;squarefree_minpoly;semisimpleTw_base')
add('HLP16 HLP32',p+'SplitPlaceDoubleCosetOperatorSemisimpleTypeSpace.lean','tN_semisimple')
add('HLP17',p+'HeckeRingActsFaithfullyOnLocalisedLattice.lean','apply_eq_smul;mem_part;mem_off;projOf_apply;lat0;heckeGenerator_mapsTo_localisationLatticeSpan;heckeAlgebra_mapsTo_localisationLatticeSpan;projOf_mem;mem_MtSub;resL;resA')
add('HLP18 HLP19',p+'HeckeRingActsFaithfullyOnLocalisedLattice.lean','eq_zero_of_pts;evA;evA_gen;evT;evT_surjective;actR;actR_evT;actA;actA_evT;actEx_of')
add('HLP19 HLP20 HLP22 HLP27',f+'GamCSpec.lean','ActSpec;ActEx;actC;OsInt;sOfC;bjRel;BjC;tGen')
add('HLP20',p+'HeckeRingActsOnLatticeAsOperators.lean','actHK_holds')
add('HLP21',p+'LocalisationHeckeRingIsLocalRing.lean','main')
add('HLP21',p+'HeckeEigenspaceNeBotEveryLocalisationPoint.lean','heckeEig_ne_bot')
add('HLP22',p+'SideRationalEigenData.lean','osInt')
add('HLP22 HLP30',f+'NPartCNdTie.lean','bjC;bjC_sum;bjC_span;bjC_rel')
add('HLP22',p+'LatticeBaseChangeFreeOverLocalisationCoeffRing.lean','bjC_free')
add('HLP23',p+'ExistsPadicFiniteExtContainingCoeffFieldAndNumbe.lean','exists_finExt_big')
add('HLP23 HLP32',p+'UnitsLiftSpec.lean','plEmb;coefIn;iqC;iqC_alg;iqC_ec;iqC_surj;BigOk')
add('HLP24',p+'UnitsLiftSpec.lean','unitsLift;unitsLift_spec;PsiInt;psN')
add('HLP24 HLP25 HLP30',p+'SideRationalEigenData.lean','psN_spec;psN_eq_one;psN_of_art;psN_ord;psN_open;psN_anti;psN_ram')
add('HLP26',p+'SideRationalEigenData.lean','plGwDisj')
add('HLP26',p+'UnitsLiftSpec.lean','gamN;PlGwDisj;exists_tame;gamN_gen;gamN_tg')
add('HLP27',p+'UnitsLiftSpec.lean','chi1N;chiN;chiN_one;mkX')
add('HLP28',p+'UnitsLiftSpec.lean','mkT;TwEmb;TwAlgAt;TwRdAt')
add('HLP29',p+'NonemptySpec.lean','trO;trK;trK_alg;trK_ec;trPsi;trPsi_inj;trPsi_range;trPsi_pr;trX;trX_hT;trPsi_act;tr_max')
add('HLP30 HLP31',d+'RingSpecNormalisedCharacterEq.lean','NdSpec')
add('HLP31',p+'NonemptySpec.lean','recBase;nonempty_spec')
add('HLP31 HLP32',p+'UnitsLiftSpec.lean','BrAt;QOver;QConj')
add('HLP32',p+'SideRationalEigenData.lean','feSup;ndSpec_exists')
add('HLP32',p+'LocalBridgesAtPlacesOverResidueCharOfLargeCoeff.lean','brAt_of_large')
add('HLP32',p+'ExistsTwistRingMapLargeCoefficientRings.lean','GlobalTheory.HeckeLocN.exists_twRing_of_large')
(HERE/'source_anchors.txt').write_text('\n'.join(anchor_rows)+'\n')

titles=[
'The full ambient generator range and prescribed lattice',
'Uniformizer and permitted split-place witness independence',
'Complete coefficient-linear lift before all witnesses',
'All-index commutation and literal base change',
'Finite dimension and actual characteristic polynomial comparison',
'Prime-to-ell complex denominator integrality in the actual DVR',
'Full original HeckeStd0 on the specified baseC',
'Full original HeckeIntTw on the prescribed generators',
'All maximal ideals exhausted by actual residual characters',
'Literal local indices and finite nonempty separating points',
'Original finite generators span before and after base change',
'Actual projected MtSub is finite and free',
'Full original MtLoc and its fraction-field isomorphism',
'Literal Psi with exact range and original projection error',
'Both exact integral and fraction-field projection spans',
'SemisimpleTw from the original complex no-Jordan antecedent',
'Projection commutes and the original projected lattice is stable',
'Descent to the actual eigenvalue-function algebra',
'Faithfulness and complete original ActEx',
'Full ActHK for every original chosen ActEx witness',
'Original local ring and nonzero eigenspaces with inherited hypotheses checked',
'Actual integral coefficient map and original MjLat relation quotient',
'One finite coefficient extension includes all prescribed complex values',
'Unique integral lift of the original twist character and kernel equality',
'Exact order, kernel, symmetry and ramification character fields',
'All-prime tame generators preserve the stored original generators',
'Every field of the original LocNd constructor',
'Original LocTw on the same local datum with full reading guards',
'Identity transports preserve the exact ideal, Psi and point labels',
'Universal coefficient relation and original character equation',
'Full original nonempty_spec with its entire arithmetic antecedent list',
'One coefficient compositum for all four original requirements',
]
deps={
1:['LTD6'],2:[],3:['HLP1','HLP2'],4:['HLP3'],5:['HLP4'],6:[],
7:['HLP4','HLP5','HLP6','MR23'],8:['HLP1','HLP3'],9:['HLP7','LTD3'],
10:['HLP9'],11:['HLP1'],12:['HLP9','HLP10','HLP11','LTD3'],
13:['HLP11','HLP12'],14:['HLP13'],15:['HLP11','HLP14'],16:['HLP4','HLP5'],
17:['HLP8','HLP12','HLP16'],18:['HLP10','HLP17'],19:['HLP13','HLP18'],
20:['HLP14','HLP19'],21:['HLP10','HLP13','HLP14','HLP17','HLP20','MR24','MR25'],
22:['HLP6','MR26'],23:[],24:[],25:['HLP24'],26:['LS19'],
27:['HLP7','HLP10','HLP12','HLP15','HLP19','HLP21','HLP22','HLP25','HLP26'],
28:['HLP24','HLP25','HLP27'],29:['HLP10','HLP14','HLP20'],
30:['HLP22','HLP24'],31:['HLP7','HLP22','HLP23','HLP25','HLP26','HLP27','HLP28','HLP29','HLP30'],
32:['MR23','HLP23','HLP31']}
scopes=[
'Original D/M/C and full ambient GenAt range through nV; original MtLat generators, not only row k<=r.',
'Actual tSet and tN with the same conjugate split-place witness and all its uniformizers.',
'Full HeckeLift0 from original HeckeStdPlain, GenHyp and MtInput; one operator before all witnesses; empty-witness branch included.',
'Literal hLC including guarded zero branches; original split-place witnesses retained; literal hKC/baseC.',
'Original fixed epsilon, basis and iV; finite dimension and both coefficient characteristic-polynomial maps; zero-space branch included.',
'Monic polynomial over original coefficient field; each complex root has a prime-to-ell integral denominator; actual DVR and integer scalar map.',
'Full two-conjunct HeckeStd0 under original HeckeStdPlain, GenHyp, split witness and SplitK inputs; no implicit splitting inference.',
'Full HeckeIntTw at every twisted eligible pair and ambient generator from original MtInput.int and actual jMt preimages.',
'Possibly infinite commuting integral split family; finite supported characters and exhaustion of all maximal ideals, without claiming the whole algebra finite.',
'Original LocT and XOf/TOf; finite fibers, nonempty points, exact maximal ideals and point-separating actual generators.',
'Original jMt basis and finite generators in its range with full complex span.',
'Literal O-span of projected original finite generators; finite and free over its actual DVR.',
'Exact MtLoc and canonical scalar-extension isomorphism on the original part, without semisimplicity.',
'Literal PsiC and prMtC, exact range, injectivity and off-space projection error.',
'Original prMtC lattice-span and full fraction-field span with original rational domain.',
'Complete original semisimpleTw_base from its stated complex no-Jordan theorem; Petersson/positive-form producer not claimed here.',
'Original HeckeIntTw and SemisimpleTw imply actual MtSub stability and literal restricted action.',
'Exact evaluation onto TOf; kernel kills original part and projected lattice; actual action descent.',
'Complete ActEx on the original MtSub/TOf with actual generators and proof of faithfulness.',
'ActHK for the original chosen ActEx witness, not just the action constructed in this chapter.',
'MR24-MR25 invoked only after actual finite nonempty points, original Psi, MtLoc and ActHK are supplied.',
'Actual OsInt/sOfC and MjLat(j) generator relation quotient, under original OsConcrete for freeness; distinct from ambient MtLat.',
'Every prescribed finite big(w) before output; same fixed complex embedding and actual p-adic algebraic closure.',
'Original PsiInt and original psi0 comparison; unique unitsLift and exact equality of specified character kernels.',
'Original Artin properties plus actual inertia nontriviality/decomposition triviality inputs; no new arithmetic character existence.',
'Original tame generators at both selected prime families; LS19 at every other prime and exact gamN equality.',
'Full mkX under exact source input list; s0 is v2(QS) at ell=2, max(1,vell(QS)) otherwise.',
'Full mkT on the same mkX, with TwAlgAt and the stronger full-original-field TwRdAt retained separately.',
'Exact equality transports trO/trK/trPsi/trX; original mxC ideals and castX preserved.',
'For every candidate coefficient map with original fraction square; original psi_eq using injectivity of actual embW.',
'Full nonempty_spec on its printed input list, including original local bridge/norm/GoodCoef/iq and all twist/character/readings.',
'Original four finite-extension requirements simultaneously at same embedding; actual F3/F4 producers and arithmetic/automorphic inputs retained.',
]
guards=[
'Original pinned Lean proof is accepted as fully checked and correct; these are human proof and source-interface obligations only.',
'Both original rank-four Links, prime 3, fixed complex embedding, same coefficient threshold, original same J and original metrics/measures remain unchanged.',
'Full ambient GenAt index range is 1<=k<=nV; it is not replaced by row-generator range 1<=k<=r.',
'Original MtInput.rat/int, complex HeckeStdPlain and complex no-Jordan producer remain their printed antecedents.',
'Actual MtSub is the O-span of projected original MtLat generators; Bj instead uses original MjLat(j).gen and exact relation module.',
'Psi, projected action, maximal ideal, original sOfC coefficient map and fixed complex embedding are preserved, not merely abstractly isomorphic replacements.',
'Full common-overfield TwRdAt compares the entire original coefficient field, not just LL0.',
'No unconditional ndSpec_exists, AutSpec, NBuilt or final RH/GRH conclusion is claimed.',
]
claims=[]
for i,title in enumerate(titles,1):
    key=f'HLP{i}'
    starts=[j for j,x in enumerate(lines) if x.strip()==f'% BEGIN {key}']
    ends=[j+1 for j,x in enumerate(lines) if x.strip()==f'% END {key}']
    assert len(starts)==len(ends)==1 and starts[0]<ends[0] and anchors[key],key
    st,en=starts[0],ends[0];block=''.join(lines[st:en]).encode()
    assert all(x in old or x in {f'HLP{j}' for j in range(1,i)} for x in deps[i]),(key,deps[i])
    claims.append(dict(id=key,title=title,introduced_in='0.41',classification='B',
      status='Complete human proof in the exact stated scope',proof_status='complete in stated scope',
      review_status='Independent review is recorded and hash-bound separately',depends_on=deps[i],
      scope=scopes[i-1],quantifier_scope=scopes[i-1],hypotheses_retained=guards,
      proof_location=dict(file=COMPONENT+'/main.tex',paragraph=key,label='claim:'+key,line_start=st+1,line_end=en,
        bytes=len(block),sha256=sha(block),range_sha256=sha(block),file_sha256=sha(raw)),sources=anchors[key]))
inherited=[]
for key in sorted({x for c in claims for x in c['depends_on'] if not x.startswith('HLP')}):
    q=old[key]['proof_location'];ls=(BASE/q['file']).read_bytes().splitlines(keepends=True)
    if 'line_start' in q:
        st,en=q['line_start'],q['line_end']
        block=b''.join(ls[st-1:en]);assert sha(block)==q.get('range_sha256',q.get('sha256')),(key,q)
    else:
        matches=[i for i,line in enumerate(ls) if line.decode().startswith('\\paragraph{'+key+':')]
        assert len(matches)==1,(key,matches)
        start=matches[0];en=next((i for i in range(start+1,len(ls)) if ls[i].decode().startswith('\\paragraph{')),len(ls));st=start+1
        block=b''.join(ls[start:en])
    inherited.append(dict(id=key,proof_file=q['file'],line_start=st,line_end=en,proof_sha256=sha(block),file_sha256=sha((BASE/q['file']).read_bytes()),source_version='0.40 or earlier'))
apps=[]
dump('published_applications.json',apps)
closed=[
 dict(id='HLP_ORIGINAL_HECKE_LIFT_STD_INT',claims=[f'HLP{i}' for i in range(1,9)],classification='B',status='closed under original printed antecedents',contract='Full HeckeLift0, all-index commutation, HeckeStd0 and HeckeIntTw on the actual base from original MtInput and complex Hecke standard facts.'),
 dict(id='HLP_ORIGINAL_LOCALIZATION_PSI',claims=[f'HLP{i}' for i in range(9,16)],classification='B',status='closed under original printed antecedents',contract='All maximal ideals and points, literal finite free MtSub, MtLoc, PsiC, exact range and original projection/lattice span fields.'),
 dict(id='HLP_ORIGINAL_FAITHFUL_ACTION',claims=[f'HLP{i}' for i in range(16,23)],classification='B',status='closed under original printed antecedents',contract='Semisimple transfer from original no-Jordan input, ActEx, ActHK, point eigenspaces and MjLat relation quotient.'),
 dict(id='HLP_ORIGINAL_NONEMPTY_SPEC',claims=[f'HLP{i}' for i in range(23,33)],classification='B',status='full original constructor reconstructed',contract='Full nonempty_spec on its entire original input list and exact one-field compositum join; F3/F4, complex no-Jordan/standard and arithmetic suppliers retained.'),
]
remaining=[
 dict(id='HLP_ACTUAL_COMMON_FORM_INPUTS',classification='C',contract='Actual common geometric/choice datum and full ambient MtInput, preserving rational and integral operators at k<=nV.'),
 dict(id='HLP_COMPLEX_HECKE_STANDARD_AND_NORMALITY',classification='C',contract='Original HeckeStdPlain and no-Jordan producer from invariant Hermitian/Petersson/double-coset facts; HLP only transfers these actual inputs.'),
 dict(id='HLP_F3_ACTUAL_LOCAL_BRIDGES',classification='B',contract='Original brAt_of_large supplier including exact valuation, GoodCoef and iq comparison at every place above ell; review underlying PlaceBridge source before declaring full closure.'),
 dict(id='HLP_F4_ACTUAL_COMMON_READING',classification='B',contract='Original SameTw.exists_reads and exists_twRing_of_large with the same entire coefficient field and common overfield, including norm and p-adic scalar agreement.'),
 dict(id='HLP_ARITHMETIC_CHARACTER_SUPPLIERS',classification='C',contract='Original reciprocity/ChebSplit/admissibility/conductor nontriviality and above-ell triviality inputs on the same chosen character.'),
 dict(id='HLP_OTHER_NBUILT_FIELDS',classification='C',contract='Original AutSpec, Galois specialization and other NBuilt fields on this common installation.'),
]
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.41',date='2026-11-22',component=COMPONENT,
 source_commit=PIN,repository='CocoSgt/riemann-hypothesis-lean',standing_assumption=guards[0],
 main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 range_convention='Inclusive one-based physical lines; exact original UTF-8 bytes including line endings.',
 claims=claims,claim_total=len(claims),published_applications=apps,inherited_proof_blocks=inherited,
 source_files=[dict(path=x,sha256=sha(b),file_sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True) for x,(b,ls,_) in sorted(cache.items())],
 metadata_builder=dict(file='build_provenance.py',sha256=sha(Path(__file__).read_bytes()),portable_invocation='python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v040'))
dump('provenance.json',prov)
dump('closure.json',dict(schema='rh-human-component-closure/1',version='0.41',component=COMPONENT,source_commit=PIN,
 standing_assumption=guards[0],main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 provenance_sha256=sha((HERE/'provenance.json').read_bytes()),new_claim_ids=[c['id'] for c in claims],
 closed_contracts=closed,remaining_inputs=remaining,same_object_guards=guards,selected_top_level_leaf_closed=False,
 not_closed=['Whole LOCAL_NBUILT_COMMON compound leaf','Unconditional ndSpec_exists','Original AutSpec and NBuilt producers','Complete human RH or Dirichlet-GRH proof'],review_status='Independent review is recorded and hash-bound separately'))
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
val=dict(status='PASS',source_commit=PIN,main_sha256=sha(raw),claims=len(claims),claim_source_references=sum(len(c['sources']) for c in claims),
 distinct_source_ranges=len(unique),source_files=len(cache),published_applications=0,bound_dependency_blocks=len(inherited),
 checks=['Every source file equals pinned Git blob','Unique declaration anchors','All marked HLP blocks hashed','Inherited dependency proof blocks verified','Exact conditional arithmetic boundary explicit'],
 not_performed='No Lean build or kernel replay; independent mathematical review and draft TeX recorded separately.')
dump('validation.json',val)
loc=[f'HLP source/proof locators at {PIN}',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
    q=c['proof_location'];loc.append(f"{c['id']} | {c['title']} | proof {q['line_start']}-{q['line_end']} SHA256 {q['sha256']}")
    for x in c['sources']:loc.append(f"  {x['path']}:{x['line_start']}-{x['line_end']} | {x['declaration']} | file {x['sha256']} | range {x['range_sha256']}")
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'report.txt').write_text('v0.41 HLP1–HLP32: complete original finite Hecke localization and nonempty_spec construction under original printed inputs. Full fixed-map coefficient lifts, integral eigenvalues, all maximal ideals, actual projected finite free lattice, exact Psi/projection/span, faithful action, point eigenspaces, original MjLat relation quotient and all transport fields are reconstructed. Actual complex Hecke standard/no-Jordan facts, compatible geometric MtInput, F3/F4 arithmetic coefficient suppliers and global character hypotheses remain explicit. No full NBuilt or final theorem closure is claimed.\n')
print(json.dumps(val,indent=2))
