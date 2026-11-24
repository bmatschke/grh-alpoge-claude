#!/usr/bin/env python3
"""Rebuild PRG provenance from exact pinned Lean bytes and marked human proofs.

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
COMPONENT = "patched_ring"
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
assert not any(re.fullmatch(r"PRG\d+", key) for key in old)
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
        "role": "Original definition, exact contract or corresponding formal argument. The independently written PRG block proves only its expressly stated scope; a named producer is never counted as its own human proof.",
        "url": f"https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{st+1}-L{en}",
    }


a="src/Development/AutomorphicArithmetic/AutomorphicVarieties/"
p=a+"PatchingModules/"; h=p+"AnnihilatorBaseChange/"
c=a+"CommutativeAlgebra/"; ca=a+"CommutativeAlgebraHeight/"
w=a+"WeilGroupCharacters/"
anchors={f"PRG{i}":[] for i in range(1,25)}
anchor_rows=[]
def add(ids,path,names):
    for name in names.split(';'):
        entry=source(path,name)
        for key in ids.split():
            assert key in anchors,key
            if entry not in anchors[key]:anchors[key].append(entry)
    anchor_rows.append(ids+'|'+path+'|'+names)
add('PRG1 PRG2',c+'ResMapBijective.lean','IsCO;resMap_bijective;res;res_map;AdicCont')
add('PRG1 PRG7',h+'SpecializationMapCompUniversalSection.lean','Ph0;πo0;πN0;Tup;Tup.Maps;RRObj')
add('PRG3 PRG11',c+'CoEvLow.lean','UpperTheory.V.Alg.co_ev')
add('PRG3',c+'CoMvps.lean','UpperTheory.V.Alg.co_mvps')
add('PRG3 PRG6 PRG10',c+'CoQuot.lean','UpperTheory.V.Alg.co_quot')
add('PRG4 PRG5 PRG6 PRG8',ca+'UnivDetMf.lean','UpperTheory.V.CA.univDet_mf')
add('PRG5 PRG6 PRG8',ca+'FinDefs.lean','IsDef;IsUnivDet')
add('PRG5 PRG7',c+'ResMapBijective.lean','PhiCond')
add('PRG7',h+'FiniteOpenHomsToFiniteGroup.lean','finite_open_homs_to_finite_group;phi_of_fg;pre_univ')
add('PRG7 PRG8',w+'UniversalOrdinaryDeterminantRing.lean','Resid;Dbar')
add('PRG9 PRG10',w+'UniversalOrdinaryDeterminantRing.lean','mu;Resid;IsPsi')
add('PRG9 PRG10',ca+'UniversalDeformationRingLocalCharacters.lean','psib_th;UpperTheory.V.CA.universalDeformationRing_localCharacters')
add('PRG11',ca+'CoCoprod.lean','UpperTheory.V.CA.co_coprod')
add('PRG12',h+'FiniteOpenHomsToFiniteGroup.lean','coprod_opt;pre_univ')
add('PRG13 PRG14 PRG24',h+'SpecializationMapCompUniversalSection.lean','Tup;Tup.Maps;RRObj;RMaps')
add('PRG13 PRG14',h+'FiniteOpenHomsToFiniteGroup.lean','UpperTheory.V.Pa.Core.rrEx')
add('PRG15 PRG16 PRG17',h+'SplittingAlgebraNontrivialFreeGenerated.lean','spCo_desc;splitting_algebra_nontrivial_free_generated;UpperTheory.V.Pa.Core.spCo')
add('PRG15 PRG17',p+'ThetaCoefficientMapEq.lean','spIdeal;Sp;Sp.u')
add('PRG18',h+'ChiRes.lean','chi_diag;UpperTheory.V.Pa.Core.chiRes')
add('PRG18',h+'SpoCo.lean','UpperTheory.V.Pa.Core.spoCo')
add('PRG18 PRG19',p+'PatchedSupportCompletions.lean','Adapted')
add('PRG18 PRG19 PRG21 PRG22 PRG23 PRG24',p+'ThetaCoefficientMapEq.lean','TWBase;TWRing;TWMaps;TWAut')
add('PRG19',h+'TupNOfRep.lean','tupN_ofRep;UpperTheory.V.Pa.Core.tupN')
add('PRG20',h+'LamComap.lean','UpperTheory.V.Pa.Core.tupPi')
add('PRG21 PRG22 PRG23',h+'SinfExt.lean','UpperTheory.V.Pa.Core.sinfExt')
add('PRG21 PRG22 PRG23 PRG24',h+'RmapsEx.lean','rm_ext;rm_cc;UpperTheory.V.Pa.Core.rmapsEx')
add('PRG24',p+'AutomorphicDetection/LiftPt.lean','core')
(HERE/'source_anchors.txt').write_text('\n'.join(anchor_rows)+'\n')
titles=[
'The precise coefficient category and tuple to be represented',
'Automatic locality, residue compatibility and continuity',
'Finite power series and complete presentations',
'The Witt coefficient ring maps to the given O',
'The exact published determinant theorem used',
'Relative determinant representability over the original O',
'The finiteness and residual hypotheses on the actual cover',
'The actual global determinant deformation ring',
'Degree-one laws and compatibility on the exact subgroup mu',
'Every constrained local-character ring is constructed',
'Finite completed coproducts in the original category',
'The joint determinant and ordered local-character object',
'Construction of the complete original RRObj',
'Independence of the presentation and arbitrary supplied W',
'The ordered polynomial splitting algebra is finite free',
'A specified residue splitting selects a finite free local factor',
'Identification with the exact completed splitting algebra',
'Actual Spo(A) and every finite-level splitting target',
'Every actual finite-level datum is a tuple over its original ring',
'The specialization tuple over the exact ordered splitting algebra',
'The universal section with the original weight coordinates',
'All finite-level maps and identities on every series',
'The exact specialization map and constant-coefficient identity',
'Complete RMaps and the exact remaining patching contract']
deps={1:[],2:[1],3:[2],4:[],5:[2],6:[3,4,5],7:[1],8:[6,7],9:[],10:[3,5,6,9],11:[3],12:[8,10,11],13:[3,12],14:[13],15:[],16:[3,15],17:[3,15,16],18:[17],19:[2,3],20:[2,18],21:[2,3],22:[14,19,21],23:[14,20,21],24:[13,18,21,22,23]}
scopes=[
'Original IsCO coefficient category and full original Tup/RRObj definitions; no added map-continuity premise.',
'Every O-algebra map between original IsCO objects; finite residue field and Noetherianity only for finite quotients.',
'Finite variables over complete Noetherian local O-algebras with fixed residue k; all maps and all series.',
'The actual complete coefficient DVR O and its given Z_ell-algebra structure; equal and mixed characteristic.',
'Positive-degree full determinant over a profinite group satisfying condition F, including ell<=n; no trace-only replacement.',
'Full relative IsUnivDet at the original coefficient DVR and every IsCO target, with degree zero treated separately.',
'Actual Ph0 Lambda, original continuous surjection p and all original residual characters; no Adapted hypothesis.',
'Actual full determinant universal ring for Ph0 Lambda, with all scalar algebras and all IsCO targets.',
'Exact degree-one law/character dictionary and original mu-v subgroup with theta compatibility.',
'Every original ordered local character, with all IsPsi fields and unique maps to every IsCO target.',
'Any finite family of IsCO objects; explicit complete power-series quotient and unique coproduct maps.',
'Entire original joint determinant and local-character pre_univ datum, without premature ordinary relations.',
'Entire original rrEx for every original Lambda,A and n, including n=0.',
'Any original RRObj, not just the constructed presentation; unique tuple-preserving isomorphism.',
'Any finite list of monic degree-n polynomials over any commutative ring, including repeated roots and n=0.',
'Specified ordered residual root tuple over a complete Noetherian local ring, producing its exact positive-rank local factor.',
'Literal formal-series quotient Sp(P,u), all spCo fields including ordinary algebra generation.',
'Original Spo A and every original SpAt at finite level with unchanged ut, with adaptedness where required.',
'All five TupN entries at every N over the original finite-level ring, exact residual law and local data.',
'All five TupPi entries over literal Spo, original B-map and actual ordered roots.',
'Original nested Sinf, literal Unit variable and exact weight coefficients, all series.',
'Every N and every series z, original rho maps all five entries and rho_N(s z)=s_N z.',
'Original pi and all five entries, plus pi(s z)=Bmap(lambda(cc z)) for every series.',
'Full original rmapsEx for any RRObj under precisely Adapted, supplied with actual rrEx; no PMod or S5 claimed.']
guards=[
'Original O,B,u,J,T,Lambda,A and complete five-part tuple retained.',
'Full determinant polynomial law, all scalar extensions, no n! inversion and selected ell=3 retained.',
'All coefficient maps are the original O-algebra maps; automatic continuity proved.',
'Actual ordered roots and all finite-level maps retained, with identities for every power series.',
'Both rank-four Links and fixed complex embedding unchanged; this chapter does not substitute new arithmetic witnesses.']
claims=[]
for i,title in enumerate(titles,1):
    key=f'PRG{i}'
    starts=[j for j,line in enumerate(lines) if line.strip()==f'% BEGIN {key}']
    ends=[j+1 for j,line in enumerate(lines) if line.strip()==f'% END {key}']
    assert len(starts)==len(ends)==1 and starts[0]<ends[0] and anchors[key],key
    st,en=starts[0],ends[0];block=''.join(lines[st:en]).encode()
    claims.append(dict(id=key,title=title,introduced_in='0.40',classification='A' if i==5 else 'B',
        status='Complete human proof in the exact stated scope',proof_status='complete in stated scope',
        review_status='pending independent mathematical review',depends_on=[f'PRG{x}' for x in deps[i]],
        scope=scopes[i-1],quantifier_scope=scopes[i-1],hypotheses_retained=guards,
        proof_location=dict(file=COMPONENT+'/main.tex',paragraph=key,label='claim:'+key,
            line_start=st+1,line_end=en,bytes=len(block),sha256=sha(block),range_sha256=sha(block),file_sha256=sha(raw)),
        sources=anchors[key]))
url='https://maths.dur.ac.uk/events/Meetings/LMS/2011/GRAF11/papers/chenevier.pdf'
apps=[dict(id='PRG_CHEN_REP',citation='Gaetan Chenevier, The p-adic analytic space of pseudocharacters of a profinite group and pseudorepresentations over arbitrary rings',
 theorem='Lemma 3.2; Proposition 3.3; Remark 3.5; Proposition 3.7, first alternative (condition F)',url=url,source_url=url,
 classification='A',status='hypotheses checked',statement_used='Continuous full residual determinant functor is represented by a profinite local W(k)-algebra; condition F makes it Noetherian with finite power-series presentation.',
 hypotheses_checked=['Actual groups are profinite and k is finite of characteristic ell.',
 'Global residual representation is the original diagonal sum of pulled-back characters; local applications have degree one.',
 'Global condition F follows from actual finite topological generation and open-subgroup Schreier; local condition F is exactly T.phiV for every open subgroup.',
 'Every IsCO target is a profinite local ring with finite Artin quotients; continuity agrees with original IsCont.',
 'Original O is treated by explicit W(k)-to-O and completed relative power-series quotient in PRG4/PRG6; flatness is not presumed.',
 'No ell>n, absolute irreducibility, trace-only determinant or n! invertibility premise is used; rank zero handled independently.'],
 claims=['PRG5','PRG6','PRG8','PRG10'],checked_in='patched_ring/main.tex PRG2 and PRG4--PRG10'),
 dict(id='PRG_STACKS_NOETH',citation='The Stacks Project',theorem='Lemma 10.31.2, Tag 0306',url='https://stacks.math.columbia.edu/tag/0306',source_url='https://stacks.math.columbia.edu/tag/0306',
 classification='A',status='hypotheses checked',statement_used='A power-series ring in finitely many variables over a Noetherian ring is Noetherian.',
 hypotheses_checked=['Every base ring is IsCO and hence Noetherian, or the given coefficient DVR.', 'All variable index sets Unit, Fin D, Fin q times Fin n and finite presentation variables are finite.'],claims=['PRG3','PRG6','PRG11','PRG13','PRG17'],checked_in='patched_ring/main.tex PRG3'),
 dict(id='PRG_STACKS_FINITE_COMPLETION',citation='The Stacks Project',theorem='Lemma 10.97.1, Tag 00MA',url='https://stacks.math.columbia.edu/tag/00MA',source_url='https://stacks.math.columbia.edu/tag/00MA',
 classification='A',status='hypotheses checked',statement_used='Completion is exact on finite modules and equals tensor with the completed base.',
 hypotheses_checked=['Base rings are Noetherian; the ideal used is their maximal ideal.', 'Modules are finite modules, ideals or quotients of finite modules; submodules are finite by Noetherianity.', 'The bases are complete, so finite modules and their quotients are complete; Krull intersection supplies separation.'],
 claims=['PRG3','PRG6','PRG10','PRG11','PRG16','PRG17'],checked_in='patched_ring/main.tex PRG3 and PRG16')]
dump('published_applications.json',apps)
standing='The pinned Alpoge-Claude Lean proof is assumed fully checked and correct. Statuses refer only to the human reconstruction.'
closed=[dict(id='PRG_FULL_RROBJ',claims=[f'PRG{i}' for i in range(1,15)],contract='Entire original rrEx with exact five-part Tup universal property, for any given original Lim and TWAut.'),
 dict(id='PRG_ACTUAL_SPLITTING_TARGETS',claims=[f'PRG{i}' for i in range(15,19)],contract='Actual Spo A and all finite-level SpAt are complete local finite free algebras ordinarily generated by exact ordered roots.'),
 dict(id='PRG_FULL_RMAPS',claims=[f'PRG{i}' for i in range(19,25)],contract='Entire original rmapsEx for any RRObj under Adapted, with exact rho and pi identities on every series.')]
for x in closed:x.update(classification='B',status='closed in exact original scope')
remaining=[dict(id='PRG_ACTUAL_PMOD_S5',classification='C',contract='Actual finite-module patching, six approximate-annihilator families and original S5 support/completion, separate companion packet.'),
 dict(id='PRG_POINT_CORE_JOIN',classification='B',contract='Exact quotient determinant Pair, lifted point, semisimplicity transport and actual Core assembly, retaining full source guards.'),
 dict(id='PRG_ORDINARY_HIDA_HASAUT',classification='C',contract='Original arithmetic TWAut producers, four Hida endpoints and all-level same-J HasAut for both rank-four Links.')]
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.40',date='2026-11-22',component=COMPONENT,
 source_commit=PIN,repository='CocoSgt/riemann-hypothesis-lean',standing_assumption=standing,
 main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 range_convention='Inclusive one-based physical lines, exact original UTF-8 bytes including line endings.',
 claims=claims,claim_total=len(claims),published_applications=apps,
 external_literature=[dict(author='Gaetan Chenevier',url=url,uses=['Lemma 3.2','Proposition 3.3','Remark 3.5','Proposition 3.7 condition F'])],
 source_files=[dict(path=p,sha256=sha(b),file_sha256=sha(b),bytes=len(b),line_count=len(ls),verified_equal_to_pinned_git_blob=True) for p,(b,ls,_) in sorted(cache.items())],
 metadata_builder=dict(file='build_provenance.py',sha256=sha(Path(__file__).read_bytes()),portable_invocation='python3 build_provenance.py --source /path/to/lean_source --baseline /path/to/reconstruction_v039'))
dump('provenance.json',prov)
closure=dict(schema='rh-human-component-closure/1',version='0.40',component=COMPONENT,source_commit=PIN,
 standing_assumption=standing,main_sha256=sha(raw),main_tex_sha256=sha(raw),sha256=sha(raw),
 provenance_sha256=sha((HERE/'provenance.json').read_bytes()),new_claim_ids=[x['id'] for x in claims],
 closed_contracts=closed,remaining_inputs=remaining,same_object_guards=guards,selected_top_level_leaf_closed=False,
 not_closed=['Actual PMod or S5 by PRG alone','Complete original arithmetic TWAut producer','Complete Count-II compound producer','Unconditional RH or Dirichlet-GRH human reconstruction'],
 review_status='pending independent mathematical review')
dump('closure.json',closure)
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for c in claims for s in c['sources']}
val=dict(status='PASS',source_commit=PIN,main_sha256=sha(raw),claims=len(claims),
 claim_source_references=sum(len(c['sources']) for c in claims),distinct_source_ranges=len(unique),source_files=len(cache),published_applications=len(apps),
 checks=['Fresh prefix','Every source file equals pinned Git blob','Unique declaration anchors','Marked proof blocks hashed','Source ranges and claim dependencies checked'],
 not_performed='No Lean build or kernel replay; mathematical review and draft TeX recorded separately.')
for c in claims:assert all(x in old or x in {a['id'] for a in claims} for x in c['depends_on'])
dump('validation.json',val)
loc=[f'PRG source/proof locators at {PIN}',f'main.tex SHA256 {sha(raw)}','']
for c in claims:
    q=c['proof_location'];loc.append(f'{c["id"]} | {c["title"]} | proof {q["line_start"]}-{q["line_end"]} SHA256 {q["sha256"]}')
    for x in c['sources']:loc.append(f'  {x["path"]}:{x["line_start"]}-{x["line_end"]} | {x["declaration"]} | file {x["sha256"]} | range {x["range_sha256"]}')
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'report.txt').write_text('''v0.40 — actual universal patching ring and maps, PRG1–PRG24

Complete original rrEx and rmapsEx on the actual original Lim and TWAut.
The published determinant representability theorem is Chenevier 3.3/3.7,
using condition F, never its ell>n alternative. All hypotheses are checked;
the original coefficient DVR is handled by an explicit relative construction.
Every ordered local-character constraint is imposed on its actual mu subgroup.
Finite complete coproduct and all five Tup entries are constructed explicitly.
The exact completed splitting algebra is identified with the selected local
factor of a finite free ordered splitting algebra, including ordinary root
generation and all finite-level targets. Every rho_N and pi is constructed
using the full RRObj property; both composition identities hold on all series.
No n! inversion, change of J, new embedding or replacement arithmetic Link.

The actual limiting module, S5 support and exact Core point join remain
separate companion producers. This packet does not itself close Count-II.
The source Lean proof is assumed correct; no Lean replay is performed.
''')
print(json.dumps(val,indent=2))
