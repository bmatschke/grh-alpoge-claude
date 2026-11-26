#!/usr/bin/env python3
"""Reproduce byte/range provenance for the literal TJRing reconstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
source = parser.parse_args().source.resolve()
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'], text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
WC = AV + 'WeilGroupCharacters/'
DC = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
DT = AV + 'AlgebraTools/DeterminantRepresentations/'
HC = AV + 'HeckeAlgebras/OrdinaryHeckeCharacters/'
LOCAL = AV + 'PadicHodgeTheory/'
POINT = AV + 'HeckeAlgebras/PointRepUnramifiedAtAuxiliaryPlace.lean'
COEF = AV + 'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean'
SPECS = {
 'original_endpoint': [
  (DC+'TJRing.lean', 22, 46, 'original complete-local Teichmuller system and unit-kernel property'),
  (DC+'TJRing.lean', 47, 136, 'jr_abs: exact same-ideal determinant descent and all eight RingProps fields'),
  (DC+'TJRing.lean', 137, 169, 'jr_surj: original surjective Hecke quotient and integral finite/torsionfree transfer'),
  (DC+'TJRing.lean', 171, None, 'full original ring_props_of_is_j_unitary_hecke_data endpoint including top branch'),
  (DC+'THidaU.lean', 37, None, 'actual HidaProps.ring consumer, kept distinct from other Hida fields')],
 'literal_definitions': [
  (WC+'ArithmeticPointClassicality.lean', 12, 39, 'V0ok, IsTeich, DD, psiT, and all eight literal RingProps fields'),
  (WC+'UniversalOrdinaryDeterminantRing.lean', 46, 103, 'HasFlag, actual star exponent/order, oEl, IsPolar and IsForm'),
  (WC+'UniversalOrdinaryDeterminantRing.lean', 107, 189, 'residual datum, Ip, Pair.red, universal ring and original LamObj.toPair'),
  (WC+'RepAlg.lean', 44, 113, 'original natural multiplicative homogeneous GDet; map, comap, representation, full Kills predicate'),
  (AV+'HeckeAlgebras/IsTheta.lean', 39, 53, 'IsMap and literal two-branch IsJ with same actual scalar map and kernel'),
  (DC+'UnitaryHeckeData.lean', 43, 74, 'UnitaryPointProperties.form/type, full original data and UnitaryHeckeData.IsJ')],
 'coefficient_points': [
  (COEF, 10, 15, 'the exact Coef ring is an embedded DVR finite over Z_l'),
  (AV+'GaloisLibrary/LocalRingsCompletion/dvrFinite.lean', 59, None, 'original completeness, finite residue field, l in maximal ideal and finite freeness'),
  (AV+'CommutativeAlgebra/ResMapBijective.lean', 9, 44, 'original IsCO fields, unique residue map, and residue-kernel equality'),
  (POINT, 213, 283, 'original integral-coefficient residue compatibility target; JRP2 replaces the analytic proof by a unit argument')],
 'local_inertia': [
  (LOCAL+'ExistsNontrivialCharacterPgroup.lean', 5, 133, 'finite prime-to-p inertia eigencharacter and conjugation calculation'),
  (LOCAL+'ExistsNontrivialCharacterPgroup.lean', 134, 190, 'scalar power congruences and finite l-group character'),
  (LOCAL+'ExistsNontrivialCharacterPgroup.lean', 218, 303, 'literal no-rank-bound v0b inertia statement and finite-level proof'),
  (LOCAL+'IqBasic.lean', 1, None, 'original inertia subgroup and norm/residue characterization')],
 'actual_auxiliary': [
  (POINT, 71, 144, 'finite-field stable lattice in original point-representation proof'),
  (POINT, 146, 176, 'continuity modulo each coefficient maximal-ideal power'),
  (POINT, 285, 365, 'jv_local: exact scalar residual-polynomial local unramified consumer'),
  (POINT, 367, None, 'full point_rep_unramified_at_auxiliary_place and actual D0/I0 dictionary'),
  (LOCAL+'DecEmb.lean', 12, None, 'original finite-completion decomposition embedding preserving inertia and cyclotomic character')],
 'law_descent': [
  (DT+'InjTest.lean', 35, None, 'coefficientwise generic-polynomial descent of determinant equality and Kills'),
  (DT+'KerTest.lean', 7, None, 'full determinant kernel test at jointly separating representations'),
  (DT+'PolarInj.lean', 1, None, 'original universal polarization descent target'),
  (DT+'FormRep.lean', 21, None, 'pairing gives exact star identity and determinant polarization after every scalar extension')],
 'ordinary_relations': [
  (DT+'FlagRel.lean', 6, None, 'ordered flag characteristic polynomial and exact noncommutative annihilating product'),
  (DT+'OElRep.lean', 6, None, 'original ordered ordinary element maps to zero')],
 'installation': [
  (HC+'HiAlgUnit.lean', 137, None, 'full original finite ordinary algebra, scalar torsionfreeness and generator fields'),
  (DC+'TDenseU.lean', 374, None, 'domain and DenseWt for the original supplied weight object'),
  (AV+'HeckeAlgebras/CoefficientRepTrivialOnUnramified.lean', 276, 285, 'literal Out univ, all-weight sep and every arithmetic pt field'),
  (DC+'OrdCoreH.lean', 20, None, 'source full Out producer and exact good guard for ordered flags'),
  (DC+'UnitaryPointProperties.lean', 1, None, 'actual unitary AutomorphicHeckeSet supplier consumed by HEP12')]
}

records = {}; inventory = {}; excerpts = []
for group, rows in SPECS.items():
    records[group] = []
    for i,(path,start,end,decl) in enumerate(rows,1):
        data = (source/path).read_bytes()
        assert data == subprocess.check_output(['git','-C',str(source),'show',PIN+':'+path]),path
        lines = data.splitlines(keepends=True)
        end = len(lines) if end is None else end
        assert 1 <= start <= end <= len(lines),(path,start,end,len(lines))
        block = b''.join(lines[start-1:end])
        rec = dict(id=f'JRP_{group}_{i:02}',path=path,declaration=decl,line_start=start,line_end=end,
                   file_sha256=sha(data),range_sha256=sha(block),range_bytes=len(block),source_commit=PIN,
                   verified_equal_to_pinned_git_blob=True,
                   url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        records[group].append(rec)
        inventory[path] = dict(path=path,sha256=sha(data),bytes=len(data),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nSHA256 {rec["range_sha256"]}\n{block.decode()}\n')

TITLES = {
 1:'Original finite coefficient ring and exact Teichmuller systems',
 2:'Every original algebraic point preserves the prescribed residue map',
 3:'Finite prime-to-residue-characteristic inertia conjugation law',
 4:'Auxiliary unramifiedness from scalar residual polynomials, without a rank bound',
 5:'Full original point_rep_unramified_at_auxiliary_place',
 6:'Joint separation detects full determinant polynomial laws and Kills',
 7:'Original pairing supplies full star identity after every scalar extension',
 8:'Flag characteristic polynomial and ordered ordinary annihilator',
 9:'Actual quotient by the specified ideal has separating points',
 10:'Full polarization and both star kernel statements descend',
 11:'Exact ordinary O1 and O2 relations descend for the same characters',
 12:'Every original type, O3 and guarded unr0 descend',
 13:'Same-surjection same-kernel finite and torsionfree quotient transfer',
 14:'Entire top-ideal branch of RingProps',
 15:'Full original TJRing endpoint and all eight RingProps fields'}
DEPS = {1:[],2:['JRP1'],3:[],4:['JRP3'],5:['JRP1','JRP2','JRP4','ADK1'],6:[],7:[],8:[],9:[],
        10:['JRP6','JRP7','JRP9'],11:['JRP8','JRP9','JRP10'],12:['JRP1','JRP6','JRP9','JRP10'],
        13:['JRP9','JRP10','JRP11','JRP12'],14:[],
        15:['JRP5','JRP13','JRP14','OHA11','AFS5','AFS20','HEP12']}
GROUPS = {1:['coefficient_points','original_endpoint'],2:['coefficient_points'],3:['local_inertia'],
          4:['local_inertia'],5:['actual_auxiliary','literal_definitions'],6:['law_descent','literal_definitions'],
          7:['law_descent','literal_definitions'],8:['ordinary_relations','literal_definitions'],
          9:['original_endpoint','literal_definitions'],10:['law_descent'],11:['ordinary_relations','original_endpoint'],
          12:['literal_definitions','original_endpoint'],13:['original_endpoint'],14:['original_endpoint','literal_definitions'],
          15:['original_endpoint','installation','literal_definitions']}
EXT = {1:['JRP_LOCAL_FIELD_BACKGROUND'],2:['JRP_LOCAL_FIELD_BACKGROUND'],
       3:['JRP_LOCAL_GALOIS_BACKGROUND'],4:[],5:['JRP_DECOMPOSITION_EMBEDDING'],
       6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:['JRP_ORIGINAL_H_PRIME']}
SCOPES = {
 1:'Every original Coef l, original O unchanged; residue exponent exactly card(k)-1, and residual value1 lifts to1.',
 2:'Every O-algebra R of original IsCO and every algebraic O-point, without assumed point continuity; residue compatibility in any finite coefficient field containing the values.',
 3:'Every finite extension K/Q_p and every continuous finite prime-to-p inertia character; exact conjugation action; all residue primes.',
 4:'Every p!=l, finite local K, complete coefficient DVR with finite residue field, arbitrary n and scalar residual characteristic polynomial; no semisimplicity or rank bound.',
 5:'Exact original Hida setting, n>=1, original V0ok, any point x and continuous rho with full determinant identity. Temporary stable-lattice field enlargement does not change O, B or x.',
 6:'Every commutative base A and jointly separating family of ring maps, including empty family when A=0; full arbitrary scalar-algebra quantifier, not only traces.',
 7:'Exact frame exponent epsilon^(1-n) and original IsForm, arbitrary invertible P, no imposed symmetric or alternating form.',
 8:'Literal upper-triangular HasFlag, ascending written product acting from right to left, arbitrary tuple of group elements and every rank.',
 9:'Exactly supplied ideal J, actual quotient B/J and original determinant/characters; no reduced or characteristic-zero replacement.',
 10:'Full IsPolar on all scalar algebras and full Kills for both y and y*, using jointly separating original point representations.',
 11:'Both original O1 and O2; every v and every tuple in F.Gv, original ordered psi retained.',
 12:'All original Teichmuller families for types, original Ip for O3, and retained V0ok guard for unr0.',
 13:'Original surjection B->T, J=ker(f), exact Lambda scalar-map compatibility, full integral fin/tf on the identical quotient.',
 14:'All original B,Lambda and J=top, zero quotient included, no nonempty arithmetic-point assumption.',
 15:'Full literal TJRing with HypothesesH prime, every original datum/level, n>=1, V.Sprime=s.S, every IsJ ideal; all eight RingProps fields.'}

tex = (HERE/'main.tex').read_bytes(); text = tex.decode(); claims = []
for n,title in TITLES.items():
    cid=f'JRP{n}'; m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S); assert m,cid
    block=m.group().encode()
    claims.append(dict(id=cid,title=title,introduced_in='0.44',classification='B',
        status='complete human proof at the printed original scope',depends_on=DEPS[n],external_input_ids=EXT[n],published_input_ids=[],
        hypotheses_retained=[SCOPES[n]],source_groups=GROUPS[n],sources=[s for g in GROUPS[n] for s in records[g]],
        proof_location=dict(file=f'{HERE.name}/main.tex',label='claim:'+cid,line_start=text[:m.start()].count('\n')+1,
                            line_end=text[:m.end()].count('\n'),sha256=sha(block),bytes=len(block)),
        scope_note='Pinned source locates exact contracts and normalizations. The printed human proof reconstructs the consumer; no Lean replay.'))

INHERITED = {'ADK1':'conditional_main_v42/adjoint_matching.tex',
             'OHA11':'ordinary_hecke_algebra_v42/main.tex',
             'AFS5':'arithmetic_fibers_v43/main.tex','AFS20':'arithmetic_fibers_v43/main.tex',
             'HEP12':'hecke_eigenpoints_v44/main.tex'}
inherited=[]
for cid,path in INHERITED.items():
    b=(ROOT/path).read_bytes(); t=b.decode(); m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',t,re.S); assert m,cid
    inherited.append(dict(id=cid,file=path,main_tex_sha256=sha(b),block_sha256=sha(m.group().encode()),
                          line_start=t[:m.start()].count('\n')+1,line_end=t[:m.end()].count('\n'),
                          kind='numbered_human_proof_dependency',not_an_external_foundation=True))

foundations=[
 dict(id='JRP_LOCAL_FIELD_BACKGROUND',kind='original_basic_local_field_background',
      statement='Finite extensions of Q_l have finite complete DVR integer rings, identified by norm<=1; integrality and residue-field inclusions have their usual properties.',
      source_groups=['coefficient_points'],not_a_new_global_producer=True),
 dict(id='JRP_LOCAL_GALOIS_BACKGROUND',kind='original_basic_local_Galois_background',
      statement='Local Galois automorphisms preserve norm, inertia fixes residues and prime-to-p roots of unity, closed subgroups have their fixed fields. The needed finite-character conjugation calculation itself is proved in JRP3.',
      source_groups=['local_inertia'],not_a_new_global_producer=True),
 dict(id='JRP_DECOMPOSITION_EMBEDDING',kind='original_local_global_dictionary',
      statement='Original finite-completion decomposition embedding of the Hida setting, preserving inertia/cyclotomic character and the given quotient map. The full D0/I0 consumer is proved in JRP5.',
      source_groups=['actual_auxiliary'],not_a_new_global_producer=True),
 dict(id='JRP_ORIGINAL_H_PRIME',kind='retained_original_named_hypothesis',
      statement='The source HypothesesH prime is retained exactly; its automorphic/local inputs enter through HEP12 and the already reconstructed ordinary algebra and density.',
      source_groups=['original_endpoint','installation'],not_reconstructed=True)]
reviews=[]
for p in sorted(HERE.glob('review_*.json')):
    reviews.append(dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())))
rp=ROOT/'reviews_v0_44/ring_properties_v44_root_review.json'
if rp.is_file(): reviews.append(dict(file=str(rp.relative_to(ROOT)),sha256=sha(rp.read_bytes())))
completed=['point_rep_unramified_at_auxiliary_place','all eight UniversalOrdinaryDeterminantRing.RingProps fields',
           'ring_props_of_is_j_unitary_hecke_data (TJRing)']
contracts=dict(schema='rh-ring-properties-contracts/1',artifact_version='0.44',component=HERE.name,source_commit=PIN,
    proof_file_sha256=sha(tex),endpoint_claim='JRP15',auxiliary_endpoint_claim='JRP5',
    completed_original_substatements=completed,original_field_coverage={
      'RingProps':{'fin':'JRP13','tf':'JRP13','polar':'JRP10','O1':'JRP11','O2':'JRP11',
                   'O3':'JRP12','types':'JRP12','unr0':'JRP5 and JRP12'},
      'IsJ_branches':{'zero module / J=top':'JRP14','nonzero actual Hecke quotient / J=ker f':'JRP13 and JRP15'}},
    exact_guards_preserved=['original HypothesesH prime','n>=1','V.Sprime=s.S','original V0ok only for unr0',
       'same actual J, f, T, Lambda and O','all original Teichmuller systems','universal scalar-algebra Kills and IsPolar'],
    human_dependency_ids=list(INHERITED),external_input_ids=[f['id'] for f in foundations],published_applications=[],
    simplifications=['algebraic point residue compatibility follows from a unit contradiction, without analytic coPt boundedness',
       'full kernel and star descent uses generic polynomial coefficients and pointwise pairing matrices directly'],
    no_lean_replay=True,whole_obligation_closures=[],
    not_claimed=['other HidaProps fields from RingProps alone','unconditional RH/GRH','replacement coefficient ring','rank-restricted auxiliary statement'])
provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.44',date='2026-11-23',component=HERE.name,
    source_commit=PIN,main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,source_groups=records,
    source_inventory=list(inventory.values()),source_files=list(inventory),published_applications=[],retained_foundations=foundations,
    inherited_human_inputs=inherited,independent_reviews=reviews,builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,claim_blocks=len(claims),whole_original_leaf_closures=0),
    scope_note='Full literal TJRing producer under original H prime and numbered inherited human inputs. Source is provenance, not a proof substitute.')
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.44',component=HERE.name,proof_file_sha256=sha(tex),
    new_claims=[c['id'] for c in claims],new_claim_count=len(claims),completed_original_substatements=completed,
    completed_planning_targets=['full TJRing original RingProps consumer'],whole_obligation_closures=[],
    original_ideal_and_coefficient_ring_preserved=True,top_ideal_included=True,V0ok_guard_preserved=True,
    universal_polynomial_law_scope_preserved=True,selected_consumer_only=False,no_lean_replay=True)
outputs={'provenance.json':provenance,'contracts.json':contracts,'closure.json':closure,
         'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,source_commit=PIN,
             source_files=list(inventory.values()),ranges=records,verified_against_git=True),
         'retained_foundations.json':foundations,'published_inputs.json':[]}
for name,value in outputs.items(): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 f'ORIGINAL ORDINARY RING PROPERTIES — v0.44\nSource pin: {PIN}\nMain SHA256: {sha(tex)}\n\n'
 f'{len(claims)} numbered human proofs, all classification B. {len(inventory)} pinned files; '
 f'{sum(map(len,records.values()))} source ranges.\n\n'
 'JRP5 proves the full auxiliary-place unramifiedness statement for every original algebraic point under V0ok, '
 'using finite coefficients, a stable lattice, automatic residue compatibility, finite inertia characters and scalar power congruences. '
 'No semisimplicity or rank bound is added.\n'
 'JRP15 proves all eight original RingProps fields at the same IsJ ideal: integral fin/tf, full polynomial-law polarization, '
 'ordered O1/O2, residual-kernel O3, all Teichmuller types and guarded unr0. J=top is included.\n'
 'Exact inherited human inputs: ADK1, OHA11, AFS5, AFS20 and HEP12; external background IDs are separate from the claim DAG.\n'
 'The original HypothesesH prime remains retained. Other HidaProps fields are not inferred from RingProps. '
 'No common/frozen v0.43 edits, no source changes, no Lean replay and no whole RH/GRH leaf closure claimed by this component.\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,artifact_version='0.44',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,records.values())),
    main_tex_sha256=sha(tex),completed=completed,whole_original_leaf_closures=0),indent=2))
