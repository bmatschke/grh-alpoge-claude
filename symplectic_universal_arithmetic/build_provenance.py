#!/usr/bin/env python3
"""Bind KX's exact arithmetic universal-ring chain to pinned source bytes."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent / 'lean-source'
COMP = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
WG = AV + 'WeilGroupCharacters/'
CA = AV + 'CommutativeAlgebra/'
CAH = AV + 'CommutativeAlgebraHeight/'
PM = AV + 'PatchingModules/'
PH = AV + 'PadicHodgeTheory/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
files = {}

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def source(path, name, role, occurrence=None):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    pat = r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+([^\s:{(]+)'
    starts = [(i,m.group(1)) for i,l in enumerate(lines,1)
              if (m:=re.match(pat,l.decode()))]
    hits = [(i,n) for i,n in starts if n == name or n.endswith('.' + name)]
    if occurrence is None:
        assert len(hits) == 1, (path,name,hits)
        a,n = hits[0]
    else:
        a,n = hits[occurrence]
    b = min([i for i,_ in starts if i > a] or [len(lines)+1])-1
    while not lines[b-1].strip(): b -= 1
    piece = b''.join(lines[a-1:b])
    if path not in files:
        assert raw == subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path]), path
        files[path] = dict(path=path,sha256=sha(raw),bytes=len(raw),lines=len(lines),
                           verified_equal_to_pinned_git_blob=True,
                           url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}')
    return dict(path=path,declaration=n,source_spelling=n,line_start=a,line_end=b,
                sha256=sha(raw),range_sha256=sha(piece),range_bytes=len(piece),
                first_line=lines[a-1].decode().rstrip('\n'),role=role,
                verified_equal_to_pinned_git_blob=True,
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{a}-L{b}')

specs = {
 'KX1': [
  (CA+'ResMapBijective.lean','IsCO','Exact complete Noetherian local category and residue-map scope'),
  (CA+'ResMapBijective.lean','res_map','All algebra maps preserve the fixed residual coefficient map'),
  (WG+'LamZl.lean','lam_zl','Source power-series universal characters; direct principal-unit proof supplied'),
  (WG+'LamFactor.lean','factor','Finite-quotient factorization and all-prime power estimate')],
 'KX2': [
  (WG+'ContinuousResP.lean','HidaSetting','Exact original finite-place unramifiedness, splitting, places and conjugation'),
  (WG+'ContinuousResP.lean','Lev','All fields of the level being constructed'),
  (WG+'ContinuousResP.lean','c_sq','Original complex conjugation squares to one'),
  (WG+'ArithmeticPointClassicality.lean','LevEx','Complete quantified endpoint'),
  (WG+'WeilCharactersModular/SgnEqOne.lean','levEx','Source quotient construction and unchanged S-prime')],
 'KX3': [
  (WG+'Inertia.lean','muG','Inverse image of primary torsion in the full topological abelianization'),
  (WG+'Inertia.lean','LocAb','All free/torsion coordinates, inertia image and finite-character universal property'),
  (PM+'TaylorWilesObstructionBound.lean','LocCFT','Literal degree sum and all chosen decomposition groups'),
  (WG+'LocCFTAll.lean','LocCFTAll','Complete quantified endpoint'),
  (WG+'WeilCharactersModular/LocCFT.lean','locCFT','Actual original local groups and degree sum'),
  (WG+'WeilCharactersModular/LocCFT.lean','lc_ab','Exact finite-character property and torsion projection'),
  (WG+'WeilCharactersModular/LocCFT.lean','lc_sum','Degree sum over places of the maximal real subfield'),
  (PH+'DecEmb.lean','decEmb','Completion transport for the originally chosen valuation'),
  (PH+'AbStruct.lean','abStruct','Local free/torsion structure; replaced by explicit local-field construction')],
 'KX4': [
  (WG+'UniversalOrdinaryDeterminantRing.lean','Resid','Original residual and prescribed torsion datum'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','IsPsi','All continuity, residual and torsion requirements'),
  (WG+'LamFree.lean','psib_mu','Residual characters kill primary torsion'),
  (WG+'LamFree.lean','exists_character_lifting_psi_free','Actual base character with prescribed torsion'),
  (WG+'LamFactor.lean','lam_factor','Complete parameterization of every local character lift')],
 'KX5': [
  (WG+'UniversalOrdinaryDeterminantRing.lean','IsInert','Requires an actual full local-character extension'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','LamObj','All universal characters and all algebra homomorphisms'),
  (WG+'LamFree.lean','lam_ex_free','Explicit inertial power-series ring and its universal property'),
  (WG+'ArithmeticPointClassicality.lean','LamEx','Literal n times degree variable count, all natural n'),
  (WG+'WeilCharactersModular/LamEx.lean','lamEx','Exact arithmetic installation of the explicit ring')],
 'KX6': [
  (CA+'ResMapBijective.lean','PhiCond','Exact finite character condition for every open subgroup'),
  (AV+'SymplecticGSp4/EntryMem.lean','CohomologyHyp','BX8 supplies the full record; only global/local finiteness used here'),
  (PM+'ChebotarevFamilies/PhiGS.lean','phi_condition_of_finite_cohomology','Explicit permutation cocycles and injection of character groups'),
  (PM+'ChebotarevFamilies/PhiGS.lean','phiGS','Exact original global quotient and finite set above ell'),
  (PM+'ChebotarevFamilies/PhiDec.lean','phiDec','Original decomposition groups and local finite cohomology'),
  (WG+'LocCFTAll.lean','PhiAll','Complete three-part quantified endpoint'),
  (WG+'WeilCharactersModular/PhiAll.lean','phiAll','Source finite-cohomology to universal-ring finiteness join')],
 'KX7': [
  (WG+'RepAlg.lean','GDet','Polynomial-law definition matches Chenevier without dividing by n factorial'),
  (WG+'RepAlg.lean','lam','Literal coefficient convention, including truncated natural subtraction',1),
  (WG+'RepAlg.lean','tr','Literal trace convention retained at degree zero',1),
  (WG+'RepAlg.lean','IsCont','Continuity of all characteristic-polynomial coefficients'),
  (WG+'Inertia.lean','DetObj','Full determinant universal object and all algebra maps'),
  (CAH+'UnivDetMf.lean','univDet_mf','Original determinant-ring existence; only actual finite coefficient scope promoted'),
  (CAH+'UnivDet.lean','univDet','General source construction replaced in the actual arithmetic scope by matched Chenevier theorem')],
 'KX8': [
  (WG+'UniversalOrdinaryDeterminantRing.lean','Pair','Every actual field and exact weak determinant relations'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','UniversalOrdinaryDeterminantRing','Unique-map endpoint with universal Pair'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','starOp','Exact cyclotomic exponent and opposite multiplication'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','oEl','Ordered product in the ordinary relation'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','Ip','Exact intersection of tame inertia and residual character kernels'),
  (WG+'Inertia.lean','LamTObj','Full local character universal functor, distinct from inertial LamObj'),
  (CAH+'UniversalDeformationRingLocalCharacters.lean','universalDeformationRing_localCharacters','Original local-character factor replaced by the explicit full-coordinate ring'),
  (CAH+'UniversalDeformationRingNonemptyOfNonemptyPair.lean','rels','Three exact families of ordinary-pair relations'),
  (CAH+'UniversalDeformationRingNonemptyOfNonemptyPair.lean','rels_iff','Naturality of each relation under the unique maps'),
  (CAH+'UniversalDeformationRingNonemptyOfNonemptyPair.lean','pre_univ','Finite completed coproduct before the ordinary relations'),
  (CAH+'UniversalDeformationRingNonemptyOfNonemptyPair.lean','universalDeformationRing_nonempty_of_nonempty_pair','Proper quotient from an actual nonempty Pair, all fields and uniqueness'),
  (WG+'ArithmeticPointClassicality.lean','ProModularRingExists','Full endpoint retains precisely the nonempty-pair antecedent'),
  (WG+'WeilCharactersModular/ProModularRingExists.lean','b0Ex','Original arithmetic coefficient ring and final installation')],
 'KX9': [
  (WG+'UniversalOrdinaryDeterminantRing.lean','LamObj.toPair','The actual canonical inertial-to-pair algebra map'),
  (WG+'UniversalOrdinaryDeterminantRing.lean','LamObj.toPair_spec','Exact character compatibility for the canonical map'),
  (WG+'ArithmeticPointClassicality.lean','RingProps','Stronger modular ideal conditions deliberately not inferred from Pair'),
  (DT+'WsLink.lean','UnramifiedInputs','lev, lam and b0 fields supplied; pr and modU not promoted')]
}

deps = {
 'KX1':[], 'KX2':[], 'KX3':[], 'KX4':['KX1','KX3'],
 'KX5':['KX1','KX3','KX4'], 'KX6':['BX8','KX2','KX3'],
 'KX7':['KX1','KX6'], 'KX8':['KX1','KX4','KX6','KX7'],
 'KX9':['KX2','KX3','KX5','KX6','KX8']
}
titles = {
 'KX1':'All coefficient algebra maps and principal-unit coordinates',
 'KX2':'Full original LevEx',
 'KX3':'Full LocCFTAll on the actual decomposition groups',
 'KX4':'Actual local character lifts with prescribed primary torsion',
 'KX5':'Full LamEx with exactly n times the real-field degree variables',
 'KX6':'Full PhiAll from the already supplied finite cohomology',
 'KX7':'Universal determinants over the original finite coefficient ring',
 'KX8':'Full ProModularRingExists with its literal nonempty-pair antecedent',
 'KX9':'Same-object canonical weight-to-pair maps and complete supplier installation'
}
scopes = {
 'KX1':'Every object and every algebra morphism in IsCO for the actual finite coefficient ring; all d including zero and all primes.',
 'KX2':'Every original HidaSetting and every admissible finite S-prime, unchanged quotient, complex conjugation and cyclotomic character.',
 'KX3':'Every original chosen local decomposition group and inertia; full LocAb fields and exact sum of local degrees.',
 'KX4':'Every actual Resid and each local residual/torsion character; all IsCO targets and full IsPsi, with uniqueness of free-coordinate factors.',
 'KX5':'Every original s,V,c,n,r, with all algebra maps, actual IsInert extensions and the precise variable count; n=0 included.',
 'KX6':'Entire PhiAll: Gamma, its actual open CM subgroup and every original local group, on every source s,V.',
 'KX7':'Full DetObj in the actual finite coefficient DVR scope, polynomial laws for every n, including ell<=n and n=0; not the unrestricted general-base source theorem.',
 'KX8':'Entire ProModularRingExists for actual s,V,c,n,r, conditional on exactly the source Nonempty(Pair r R) input; all Pair fields and unique algebra maps.',
 'KX9':'Exact LamObj.toPair compatibility and naturality for any fixed source universal rings via their unique isomorphisms; no modular-support ideal asserted.'
}
retained = {cid:[] for cid in deps}
retained['KX8'] = ['Exactly the source antecedent: an actual Pair r R0 over some IsCO coefficient algebra.']
retained['KX9'] = ['The same actual Pair existence antecedent when invoking KX8.']
classical = {
 'KX-LOCAL-CFT':dict(name='Local reciprocity and local existence theorem',
   reference='J. S. Milne, Class Field Theory, Chapter I, Theorems 1.1 and 1.4; profinite completion and units/inertia in paragraphs 1.10-1.11.',
   url='https://www.jmilne.org/math/CourseNotes/CFT.pdf',
   precise_input='The topological abelianization of the absolute Galois group of a finite extension K/Q_ell is the profinite completion of K^times, and units correspond to inertia.',
   hypothesis_match='K is the completion at the original valuation; source splitting identifies it with F_v. Arithmetic Frobenius normalization is fixed; free/torsion decomposition is proved separately.'),
 'KX-CHENEVIER':dict(name='Continuous determinant prorepresentability under Phi_ell',
   reference='G. Chenevier, arXiv:0809.0415v2, Propositions 3.3 and 3.7 and Remark 3.5.',
   url='https://arxiv.org/abs/0809.0415',
   precise_input='Continuous determinants deforming a finite-field semisimple residual representation of a profinite group satisfying condition (F) have a complete Noetherian local universal W(k)-algebra.',
   hypothesis_match='GDet is a multiplicative homogeneous polynomial law with full naturality. Condition (F) is exact PhiCond. The residual direct sum is finite and continuous. No residual irreducibility or ell>n assumption is introduced. Actual O extension and degree zero are proved separately.')
}
use = {cid:[] for cid in deps}
use['KX3']=['KX-LOCAL-CFT']
use['KX7']=['KX-CHENEVIER']
old = json.loads((ROOT/'history/version_0_28/provenance.json').read_text())
oldclaims = {c['id']:c for c in old['claims']}
external = []
for cid in sorted(set(sum(deps.values(),[]))-set(deps)):
    c = oldclaims[cid]
    external.append(dict(claim_id=cid,title=c['title'],proof_location=copy.deepcopy(c['proof_location']),
                         use='Only the full original global and local finite-cohomology fields are used.'))
raw=(HERE/'main.tex').read_bytes()
lines=raw.splitlines(keepends=True)
claims=[]
for cid in deps:
    begin=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% BEGIN '+cid)
    a=next(i for i,l in enumerate(lines,1) if i>begin and l.decode().startswith('\\begin{'))
    b=next(i for i,l in enumerate(lines,1) if l.decode().strip()=='% END '+cid)-1
    while not lines[b-1].strip(): b-=1
    assert lines[b-1].decode().strip()==r'\end{proof}'
    piece=b''.join(lines[a-1:b])
    claims.append(dict(id=cid,title=titles[cid],introduced_in='0.29',
       status='Complete human proof in the exact stated scope with explicitly matched classical inputs',
       mathematical_status='Complete original arithmetic supplier; no Lean build or kernel replay',
       scope=scopes[cid],depends_on=deps[cid],remaining_inputs=retained[cid],
       remaining_bespoke_inputs=[],classical_inputs=use[cid],
       source_relation='Explicit reconstruction on the actual arithmetic groups, rings and universal maps; Chenevier replaces the general determinant construction only in the finite coefficient scope actually consumed.',
       proof_location=dict(file=COMP+'/main.tex',paragraph=cid,label='claim:'+cid,
                           line_start=a,line_end=b,sha256=sha(piece),bytes=len(piece)),
       sources=[source(*s) for s in specs[cid]]))
out=dict(schema='rh-human-reconstruction-provenance/1',artifact_version='0.29',date='2026-11-22',
    repository=old['repository'],commit=PIN,component=COMP,main_tex_sha256=sha(raw),
    scope='Complete LevEx, LocCFTAll, LamEx, PhiAll and ProModularRingExists with exact Pair antecedent and same-object universal maps.',
    claims=claims,source_files=list(files.values()),dependency_graph=deps,
    external_claim_dependencies=external,classical_inputs=classical,retained_inputs=retained,
    validation=dict(claim_count=len(claims),claim_source_links=sum(len(c['sources']) for c in claims),
       source_files_checked_against_pinned_git_blobs=len(files),main_tex_sha256=sha(raw),
       entire_LevEx_supplied=True,entire_LocCFTAll_supplied=True,entire_LamEx_supplied=True,
       entire_PhiAll_supplied=True,entire_ProModularRingExists_supplied=True,
       nonempty_pair_antecedent_preserved=True,unramified_character_variables_excluded_from_inertial_weight_ring=True,
       all_algebra_maps_included=True,rank_zero_source_coefficient_convention_preserved=True,
       modular_support_existence_claimed=False,PMExAlt_claimed=False,
       no_new_lean_build_or_kernel_replay=True))
dump('provenance.json',out)
endpoints=[dict(name=name,supplier=cid,scope=scopes[cid],retained_inputs=retained[cid])
           for name,cid in [('LevEx','KX2'),('LocCFTAll','KX3'),('LamEx','KX5'),('PhiAll','KX6'),
                           ('ProModularRingExists','KX8'),('LamObj.toPair naturality','KX9')]]
dump('closure.json',dict(schema='rh-human-component-closure/1',artifact_version='0.29',component=COMP,
    commit=PIN,main_tex_sha256=sha(raw),provenance_sha256=sha((HERE/'provenance.json').read_bytes()),
    closed_claim_ids=list(deps),dependency_graph=deps,external_claim_dependencies=external,endpoints=endpoints,
    no_new_lean_build_or_kernel_replay=True))
dump('input_registry.json',dict(schema='rh-component-input-registry/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),claim_inputs=external,retained_inputs=retained,new_classical_theorem_inputs=classical))
dump('remaining_inputs.json',dict(schema='rh-component-remaining-inputs/1',artifact_version='0.29',component=COMP,
    main_tex_sha256=sha(raw),retained_inputs=retained,
    not_supplied=['Actual modular-support ideal with RingProps/HidaPropsAlt/P1core/P3core.',
                 'Entire UnramifiedInputs pr and modU fields.',
                 'PMExAlt, SeedIIAlt, SeedIVAlt and uniform actual ProModAlt witnesses.'],
    clarification='The original nonempty Pair antecedent is preserved; it is not replaced with unconditional existence of a pair or an automorphic point.'))
dump('next_targets.json',dict(schema='rh-next-source-targets/1',artifact_version='0.29',component=COMP,targets=[],
    explanation='These complete arithmetic suppliers have no internal bespoke frontier. The semantic audit tracks their actual modular-support, seed and realization consumers.'))
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+
    '\n'.join(s['declaration']+'\n'+s['url']+'\n'+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
(HERE/'report.txt').write_text('Version 0.29 — actual arithmetic universal-ring suppliers\n\n'+
    '\n'.join(cid+': '+scopes[cid] for cid in deps)+'\n\n'+json.dumps(out['validation'],indent=2)+'\n')
print(json.dumps(out['validation'],indent=2))
