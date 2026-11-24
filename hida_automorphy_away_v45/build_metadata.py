#!/usr/bin/env python3
"""Bind the full human automorphy-away consumer to the immutable source contracts."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, required=True)
SRC = ap.parse_args().source.resolve()
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()
AA = 'src/Development/AutomorphicArithmetic/'
AV = AA + 'AutomorphicVarieties/'
DC = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
OJ = AV + 'ModularityArgument/OrdinaryJacquetModules/'
LS = AV + 'ModularityArgument/LeviSmoothLocalization/'
PM = LS + 'PrincipalSeriesMatching/'
FG = AA + 'Foundations/GaloisRepresentations/PlainTorsionPairs/'
AB = 'src/Development/AbelianVarietyTheory/'

# These locate the original mathematical contracts and their normalizations.
# A source range is not a substitute for the numbered human proof.
SPECS = {
 'original_inputs': [(DC+'LitAut.lean',12,63,'original local and automorphic literature fields'),
   (DC+'UnitaryHeckeData.lean',21,None,'original TypeForAlt, UnitaryHeckeData and IsJ data')],
 'same_representation': [(DC+'Link2.lean',28,None,'link2_alt for an arbitrary supplied continuous irreducible rho'),
   (DC+'ProjectedFormsLinkOfPrintedHida.lean',31,47,'same original Y and actual PartLinkAlt supplier'),
   (DC+'PartLinkAltAlt.lean',20,None,'full PartLinkAlt contract'),
   (DC+'AutUOT.lean',31,57,'part2 local equivalence and AutUOAlt producer'),
   (DC+'OrdDefs.lean',62,67,'literal part-dependent AutUOAlt predicate')],
 'support_type': [(FG+'TypePlain.lean',18,42,'TypePlain and full AwayOk'),
   (FG+'PlainTorOfMono0.lean',21,None,'generic unlinked singleton argument and full typePlain'),
   (AA+'Foundations/LocalLanglands/LocalCentralUnits/AbConv.lean',31,147,'commutator identity, irreducible Weil dimension one and abConv'),
   (PM+'PlainIff.lean',33,94,'exact character-ratio dictionary and full PlainIff'),
   (PM+'SphUnl.lean',1,None,'original spherical-unlinked endpoint')],
 'conjugate_support': [(DC+'OrdConjTor.lean',19,None,'support duality, field transport, uniformizer and ConjTor')],
 'away': [(DC+'AutAway.lean',27,77,'full AutAway on the same actual YOf and updated local family')],
 'window': [(LS+'WinUpDown.lean',22,41,'literal uniformizer, chars, Unl and WinAt'),
   (LS+'WinUpDown.lean',147,164,'WinUnl, full global WinOf and SphUnl contracts'),
   (PM+'NormAbsPowUnif.lean',59,118,'strict unitary exponent consumer with toral unlinked support'),
   (PM+'NormAbsPowUnif.lean',124,168,'one global twist and exact WinOf conclusion'),
   (AB+'Proofs/InertiaEigenvalues/ExistsIsUnitaryTwistAbsPow.lean',17,89,'norm-one compactness and a single global real power'),
   (AB+'Proofs/InertiaEigenvalues/ExistsIsUnitaryTwistAbsPow.lean',114,145,'central-character unitarization and uniformizer power'),
   (PM+'CharAbs.lean',57,67,'original common uniformizer exponent')],
 'jacquet': [(OJ+'CoreOrdAlt.lean',60,66,'full original OrdJac including rank zero'),
   (DC+'OrdOrdJac.lean',21,None,'positive stable image, character quotient, exact delta/index scalar'),
   (AV+'HeckeAlgebras/OrdinaryHeckeCharacters/ExistsNil.lean',165,237,'character quotient sharing every scalar relation of a nonzero vector')],
 'scalars': [(DC+'OrdDefs.lean',32,42,'full OrdScalAlt'),
   (DC+'OrdOrdScal.lean',24,None,'same local image and exact original lowVal and psEig factors')],
 'part_point': [(DC+'OrdDefs.lean',22,27,'AutYAlt for an arbitrary predicate on the whole part'),
   (DC+'OrdDefs.lean',43,51,'full PartPtAlt with the specified specialization and point'),
   (DC+'OrdPartPt.lean',19,None,'original ordinary-part decomposition and point extraction')],
 'ordinary_core': [(DC+'OrdDefs.lean',52,61,'full CoreOrdAlt contract'),
   (DC+'OrdCoreOrd.lean',21,43,'original same-Y core producer and nonzero universal generator values')],
 'end_ordinary': [(DC+'OrdDefs.lean',68,71,'literal EndOrdAlt'),
   (OJ+'CoreOrdAlt.lean',22,25,'exact ExpOf witnesses and every-local-component assertion'),
   (OJ+'CoreOrdAlt.lean',53,56,'full ENDO without given-rho continuity'),
   (DC+'IsoOfDet.lean',26,143,'same-point factoring, semisimple comparison and endOrd'),
   (AV+'HeckeAlgebras/Distinct.lean',62,66,'lowW and htW conventions')],
 'ordered_flag': [(OJ+'FlagJ.lean',13,17,'full original FlagJ contract'),
   (DC+'OrdFlagJ.lean',16,133,'ordered matrix product, descent and full flagJ_alt'),
   (DC+'NmRegArith.lean',45,114,'strict arithmetic weights and a rational-unit separating element'),
   (AV+'WeilGroupCharacters/ArithmeticPointClassicality.lean',19,38,'original RingProps fields O1 and O2'),
   (AV+'WeilGroupCharacters/RepAlg.lean',96,106,'universal scalar-algebra Kills'),
   (AV+'WeakShimuraTheory/EigenbasisLifts/RelKill.lean',13,None,'original full matrix trace-kernel comparison')],
 'conjugate_flag': [(OJ+'CoreOrdAlt.lean',143,150,'literal two-clause ConjUnl'),
   (DC+'OrdConjUnl.lean',16,148,'flag-character comparison and abstract dual/twist ratio transport'),
   (DC+'OrdConjUnl.lean',156,285,'actual decomposition-group field transport and common cyclotomic multiplier'),
   (DC+'OrdConjUnl.lean',287,327,'same given rho polarization and full ConjUnl producer')],
 'ordinary_torsion': [(OJ+'CoreOrdAlt.lean',131,136,'all three clauses of ExpTor'),
   (DC+'OrdExpTor.lean',15,86,'compact norm one and strictly ordered exponent zero-sum calculation'),
   (DC+'OrdExpTor.lean',100,124,'rational units tending to one'),
   (DC+'OrdExpTor.lean',129,231,'exact twist identity, linkage and torsion factor q'),
   (DC+'OrdExpTor.lean',248,306,'normalized principal-series support and full ExpTor')],
 'born': [(OJ+'FlagJ.lean',19,25,'full original BornJ definition'),
   (DC+'OrdBornJ.lean',19,50,'Satake equality and original BornJ with printed polarization/window')],
 'endpoint': [(FG+'IrrArithPointsAutomorphicAway.lean',17,58,'WitOff, conditional-continuity AutOffN and entire end2 predicate'),
   (AV+'ModularityArgument/AutomorphyLifting/WeakOfAtt.lean',19,25,'Unl1 and PotUnl with every prolongation'),
   (DC+'EndoscopyRank2Ordinary.lean',29,47,'coreA same-frame predicate and determinant output'),
   (DC+'EndoscopyRank2Ordinary.lean',48,72,'literal all-rank irrArithPointsAutomorphicAway_of_isJ')]
}

inventory = {}; groups = {}; excerpts = []
for group, entries in SPECS.items():
    groups[group] = []
    for i,(path,start,end,decl) in enumerate(entries,1):
        b=(SRC/path).read_bytes()
        assert b == subprocess.check_output(['git','-C',str(SRC),'show',f'{PIN}:{path}']), path
        lines=b.splitlines(keepends=True); end=end or len(lines)
        assert 1 <= start <= end <= len(lines), (path,start,end,len(lines))
        rb=b''.join(lines[start-1:end])
        record=dict(id=f'HAW_{group}_{i:02}',path=path,line_start=start,line_end=end,declaration=decl,
            file_sha256=sha(b),range_sha256=sha(rb),range_bytes=len(rb),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        groups[group].append(record)
        inventory[path]=dict(path=path,sha256=sha(b),bytes=len(b),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{record["id"]}] {path}:{start}-{end}\nSHA256 {record["range_sha256"]}\n{rb.decode()}\n')

DEPS={
 1:['GUA18','GUA17','UPA7','LTP19','LTP20','CAP6','BCS4'],
 2:['HAW1','UPA16','UPA7','ADP12','ITA12','ITA13'],
 3:['BCS5','GUA12'],4:[],
 5:['HAW2','HAW3','HAW4','ADP12','LTP12','LTP17','LTP18'],
 6:['BCS8','BCS1','BCS5'],
 7:['OST5','AFS11','AFS12'],8:['HAW7','AFS13'],
 9:['CFD9','CFD10','CFD11','CFD12','AFS16','AFS18','ASP11','ASP13','OHA6','OHA7','AFS9'],
 10:['HAW8','HAW9','ASP13','HEP7'],
 11:['HAW1','HAW2','HAW10','AFS6','AFS7','AFS8'],
 12:[],13:['HAW12'],14:['HAW1'],15:[],16:['HAW15'],
 17:['HAW4','HAW6','HAW13','HAW14','HAW16'],
 18:['HAW5','HAW10','AFS6','AFS7','AFS8'],
 19:['HAW1','HAW6','HAW11','HAW17','HAW18','JRP15']}
GROUPS={1:['same_representation','original_inputs'],2:['same_representation'],
 3:['support_type','window'],4:['conjugate_support'],5:['away','support_type'],
 6:['window'],7:['jacquet'],8:['scalars'],9:['part_point'],10:['ordinary_core'],
 11:['end_ordinary'],12:['ordered_flag'],13:['ordered_flag'],14:['conjugate_flag'],
 15:['ordinary_torsion'],16:['ordinary_torsion'],17:['born','conjugate_flag'],
 18:['endpoint','part_point'],19:['endpoint','original_inputs']}
SCOPES={
 1:'Full original same-given continuous irreducible rho; all ranks n>=1, every split local component, every IsUnramU place, same normalized Satake comparison.',
 2:'Every original PartLinkAlt datum; Y.Y exactly equals supplied YOf. Full AutUOAlt retains arbitrary actual part and every selected ell-place.',
 3:'Every positive-rank actual cusp, every local component and every IsRecT; the inertia characters must extend to the original global characters in TypePlain.',
 4:'Every pair of places over the same maximal-real place, including ramified support characters and all support witnesses.',
 5:'Exact original AutomorphicHeckeSet predicate AwayOk; V.Sprime=s.S, same integral type and all places away from ell and the single original auxiliary place.',
 6:'Full WinOf over every totally complex field and every positive rank; one center before all finite places, exact strict half-width, all support characters.',
 7:'Full original OrdJac including n=0, arbitrary nonarchimedean local field and all original operator scalars, with no distinctness or Good requirement.',
 8:'All original OrdScalAlt data and guards; same IsSpec map, e>=c0, same actual part and all lowVal/psEig factors.',
 9:'Full PartPtAlt with arbitrary predicate depending on the entire part, specified arithmetic specialization and specified point of the actual Hecke algebra.',
 10:'Full literal CoreOrdAlt: all original ranks, points and admitted weights; same P,Y,D,psi; full determinant polynomial law; no Good guard.',
 11:'Full EndOrdAlt and ENDO at every original IsJ; arbitrary given irreducible rho, no continuity premise, all local components of one attached cusp.',
 12:'Exact ordered matrix product gives upper-triangular flag; every original increasing arithmetic weight yields a separating inertia element.',
 13:'Full FlagJ under RingProps; same J and arbitrary representing irreducible rho; no continuity, Good or V0ok premise.',
 14:'Full ConjUnl for a continuous attached semisimple rho; every prolongation, each positive power, actual decomposition groups and original epsilon^(1-n) multiplier.',
 15:'Exact OrdChar normalization at every ell-place; no ambient global continuity assumption beyond continuity supplied in OrdChar.',
 16:'All three original ExpTor clauses; arbitrary positive m and exact factor q; all support witnesses and strict original window.',
 17:'Entire BornJ under RingProps and ENDO, with its original continuity premise; PotUnl at every prolongation and TU for every attached cusp.',
 18:'Literal coreA: same original frame, continuous semisimple rho0, exact x.IsRep and full irreducible AwayOk predicate.',
 19:'Entire IrrArithPointsAutomorphicAway/AutOffN for all n>=1 and original IsJ, V.Sprime=s.S; conditional continuity stays inside AutOffN; no added V0ok/Good guard.'}

FOUNDATIONS=[
 dict(id='HAW_ORIGINAL_H_PRIME',kind='retained_original_named_hypothesis',source_groups=['original_inputs'],
      statement='Original HypothesesH prime including named definite-inner-form base change and polarized cuspidal attachment; inherited BCS/GUA boundaries remain unchanged.',not_reconstructed=True),
 dict(id='HAW_LOCAL_CLASSIFICATION',kind='retained_original_local_literature',source_groups=['original_inputs','support_type','jacquet'],
      statement='Original bz, geo, zel, gen, multi and exh: admissibility/Jacquet finite length, geometric lemma, support uniqueness, generic unlinked segment and Langlands classification. No replacement by a spherical-only correspondence.',not_reconstructed=True),
 dict(id='HAW_REC_T',kind='retained_original_local_correspondence',source_groups=['support_type','ordinary_torsion'],
      statement='Full original IsRecT laws and RecTExists, including rank, cuspidal irreducibility, segment and sum laws, finite inertia semisimplicity and rank-one Artin normalization.',not_reconstructed=True),
 dict(id='HAW_DUALITY',kind='retained_original_duality',source_groups=['conjugate_support','conjugate_flag'],
      statement='Original Gelfand–Kazhdan and normalized-induction smooth-dual pairing. The exact dual support/field transport and given-rho polarization consumers are proved in HAW4/14.',not_reconstructed=True),
 dict(id='HAW_GLOBAL_COMPARISON',kind='retained_original_global_foundation',source_groups=['same_representation','born'],
      statement='Original strong multiplicity one and Chebotarev. CAP6 is the separately bound numbered degree-one density input; finite matrix-algebra semisimple comparison is proved in HAW1.',not_reconstructed=True),
 dict(id='HAW_GLOBAL_CENTRAL_CHARACTER',kind='original_central_character_and_idele_background',source_groups=['window'],
      statement='Actual positive-rank cusps have their original continuous central Hecke character; the norm-one idele class group is compact. HAW6 reconstructs the single global unitarizing norm twist and full WinOf consumer.',not_reconstructed=True),
 dict(id='HAW_RECIPROCITY_LOCAL_FIELDS',kind='retained_original_reciprocity_and_local_field_background',source_groups=['ordered_flag','conjugate_flag','ordinary_torsion'],
      statement='Original local/global Artin reciprocity, exact geometric Artin cyclotomic formula, finite local embeddings, density of Weil in decomposition group, transitivity on prolongations and CM conjugation dictionary.',not_reconstructed=True),
 dict(id='HAW_FINITE_ALGEBRA',kind='standard_algebraic_background',source_groups=['jacquet','ordered_flag'],
      statement='Finite-dimensional matrix-algebra density/Burnside and Wedderburn, weak Nullstellensatz and elementary generalized-character blocks. The needed trace, ordered-flag and quotient-functional consumers are explicitly proved.',not_a_new_global_producer=True)
]
EXT={
 1:['HAW_ORIGINAL_H_PRIME','HAW_GLOBAL_COMPARISON','HAW_FINITE_ALGEBRA'],
 2:['HAW_ORIGINAL_H_PRIME'],3:['HAW_LOCAL_CLASSIFICATION','HAW_REC_T'],
 4:['HAW_LOCAL_CLASSIFICATION','HAW_DUALITY','HAW_RECIPROCITY_LOCAL_FIELDS'],
 5:['HAW_ORIGINAL_H_PRIME','HAW_REC_T'],
 6:['HAW_LOCAL_CLASSIFICATION','HAW_GLOBAL_CENTRAL_CHARACTER'],
 7:['HAW_LOCAL_CLASSIFICATION','HAW_FINITE_ALGEBRA'],8:[],9:[],10:[],11:[],
 12:['HAW_RECIPROCITY_LOCAL_FIELDS'],13:['HAW_FINITE_ALGEBRA'],
 14:['HAW_DUALITY','HAW_GLOBAL_COMPARISON','HAW_RECIPROCITY_LOCAL_FIELDS'],
 15:['HAW_RECIPROCITY_LOCAL_FIELDS'],16:['HAW_LOCAL_CLASSIFICATION'],
 17:['HAW_GLOBAL_COMPARISON'],18:[],19:['HAW_ORIGINAL_H_PRIME','HAW_GLOBAL_COMPARISON']}

tex=(HERE/'main.tex').read_bytes(); text=tex.decode(); claims=[]
for n in range(1,20):
    cid=f'HAW{n}'
    m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S); assert m,cid
    block=m.group().encode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1)
    claims.append(dict(id=cid,title=title,introduced_in='0.45',classification='B',
        status='complete human proof at the printed original scope',depends_on=DEPS[n],
        external_input_ids=EXT[n],published_input_ids=[],hypotheses_retained=[SCOPES[n]],
        source_groups=GROUPS[n],sources=[s for g in GROUPS[n] for s in groups[g]],
        proof_location=dict(file=f'{HERE.name}/main.tex',label='claim:'+cid,
            line_start=text[:m.start()].count('\n')+1,line_end=text[:m.end()].count('\n'),
            sha256=sha(block),bytes=len(block)),
        scope_note='Original source fixes contracts and normalization; the human argument, not a Lean replay, proves the consumer.'))

human_ids=sorted({d for ds in DEPS.values() for d in ds if not d.startswith('HAW')})
inherited=[]
for cid in human_ids:
    matches=[]
    for p in ROOT.glob('*/main.tex'):
        b=p.read_bytes(); t=b.decode()
        m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',t,re.S)
        if m: matches.append((p,b,t,m))
    assert len(matches)==1,(cid,[str(q[0]) for q in matches])
    p,b,t,m=matches[0]
    inherited.append(dict(id=cid,file=str(p.relative_to(ROOT)),main_tex_sha256=sha(b),
        block_sha256=sha(m.group().encode()),line_start=t[:m.start()].count('\n')+1,
        line_end=t[:m.end()].count('\n'),kind='numbered_human_proof_dependency',not_an_external_foundation=True))

# Direct named dependencies, including endpoints of ranges, must be in the DAG.
for claim in claims:
    cid=claim['id']; n=int(cid[3:]); m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',text,re.S)
    named=set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b',m.group()))-{cid}
    missing=named-set(DEPS[n])
    assert not missing,(cid,'unrecorded named proof dependencies',sorted(missing))
    assert all(not d.startswith('HAW') or int(d[3:])<n for d in DEPS[n]),cid
    assert not (set(DEPS[n]) & {f['id'] for f in FOUNDATIONS})

reviews=[]
for p in sorted(HERE.glob('review_*.json')):
    reviews.append(dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())))
for p in [ROOT/'reviews_v0_45/hida_automorphy_away_v45_root_review.json']:
    if p.is_file(): reviews.append(dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())))
completed=['link2_alt','PartLinkAlt / projected_forms_link_of_printed_hida','AutUOAlt',
 'PlainIff / TypePlain / SphUnl','ConjTor','AutAway with the full AwayOk predicate','WinOf',
 'OrdJac','OrdScalAlt','PartPtAlt','CoreOrdAlt','EndOrdAlt / ENDO','FlagJ','ConjUnl','ExpTor','BornJ',
 'coreA','IrrArithPointsAutomorphicAway / full AutOffN']
contracts=dict(schema='rh-hida-automorphy-away-contracts/1',artifact_version='0.45',component=HERE.name,
 source_commit=PIN,proof_file_sha256=sha(tex),endpoint_claim='HAW19',
 completed_original_substatements=completed,original_field_coverage={
   'HidaPropsAlt.end2':'HAW19','AutOffN.AutCsd0':'HAW18 and HAW19',
   'AutOffN.conditional_continuity':'HAW19',
   'WitOff.above_ell_Unl1_implies_PotUnl':'HAW17',
   'WitOff.every_attached_cusp_one_t_before_every_place':'HAW6 and HAW19',
   'CoreOrdAlt.full_part_predicate':'HAW9 and HAW10',
   'CoreOrdAlt.full_determinant_and_all_OrdChar':'HAW10',
   'OrdFlagJ.same_ordered_characters':'HAW12 and HAW13'},
 exact_guards_preserved=['n>=1 in final endpoint; OrdJac/CoreOrdAlt retain original all-rank scope',
  'same original R.IsJ, J, f, T, coefficient ring, weight ring and level',
  'V.Sprime=s.S in AutAway and final endpoint',
  'no continuity premise before AutCsd0; original conditional continuity retained within AutOffN',
  'no added V0ok or Good premise','ell=3 included','one real t before every place for each attached cusp',
  'all prolongations and every positive integer m in PotUnl','strict original half-width and exact q factor'],
 human_dependency_ids=human_ids,external_input_ids=[f['id'] for f in FOUNDATIONS],published_applications=[],
 simplifications=['direct finite matrix-algebra comparison for arbitrary same-determinant semisimple representations',
  'spectral-idempotent proof of the ordered flag from O1/O2',
  'global window uses existing BCS8 and one explicitly constructed global norm twist',
  'coreA extracted directly from stronger CoreOrdAlt with the actual AwayOk predicate'],
 no_lean_replay=True,selected_consumer_only=False,whole_obligation_closures=[],
 not_claimed=['all remaining HidaPropsAlt fields from end2 alone','new proof of retained local/global literature foundations','unconditional RH or GRH'])
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.45',date='2026-11-23',component=HERE.name,
 source_commit=PIN,main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,source_groups=groups,
 source_inventory=list(inventory.values()),source_files=list(inventory),published_applications=[],
 retained_foundations=FOUNDATIONS,inherited_human_inputs=inherited,independent_reviews=reviews,
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
 validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
  claim_blocks=len(claims),direct_named_claim_dependencies_checked=True,whole_original_leaf_closures=0),
 scope_note='Full literal end2 consumer under the original H prime and recorded numbered human inputs. Exact foundations remain separately named; source is provenance, not proof.')
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.45',component=HERE.name,proof_file_sha256=sha(tex),
 new_claims=[c['id'] for c in claims],new_claim_count=len(claims),completed_original_substatements=completed,
 completed_planning_targets=['full original HidaPropsAlt.end2','full CoreOrdAlt reusable by point and twist branches'],
 whole_obligation_closures=[],original_ideal_and_coefficient_ring_preserved=True,top_ideal_included=True,
 conditional_continuity_clause_preserved=True,no_added_V0ok_or_Good=True,
 uniform_window_choice_order_preserved=True,universal_polynomial_law_scope_preserved=True,
 selected_consumer_only=False,no_lean_replay=True)
outputs={'provenance.json':prov,'contracts.json':contracts,'closure.json':closure,
 'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,source_commit=PIN,
  source_files=list(inventory.values()),ranges=groups,verified_against_git=True),
 'retained_foundations.json':FOUNDATIONS,'published_inputs.json':[]}
for name,value in outputs.items(): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 f'FULL ORDINARY AUTOMORPHY AWAY — v0.45\nSource pin: {PIN}\nMain SHA256: {sha(tex)}\n\n'
 f'{len(claims)} numbered human proofs, all classification B. {len(inventory)} pinned files; '
 f'{sum(map(len,groups.values()))} ranges; {len(inherited)} inherited numbered proof bindings.\n\n'
 'HAW19 proves the full original IrrArithPointsAutomorphicAway / HidaPropsAlt.end2 endpoint, not only AutCsd0. '
 'It retains the same IsJ ideal and representation, every original positive rank and odd prime including3, '
 'conditional continuity inside AutOffN, every prolongation and every positive power, and one real center '
 'before every eligible place for each attached cusp. No V0ok or Good hypothesis is added.\n'
 'HAW1–6 reconstruct same-representation PartLinkAlt, full local type/plain support, ConjTor, AutAway and WinOf. '
 'WinOf uses BCS8 strict exponents and an explicit single global unitarizing norm twist.\n'
 'HAW7–13 reconstruct OrdJac, exact normalized scalars, arbitrary-predicate PartPtAlt, full CoreOrdAlt, '
 'EndOrdAlt and the ordered FlagJ via explicit spectral idempotents and universal polynomial-law Kills.\n'
 'HAW14–19 reconstruct original polarization/conjugate-place transport, exact q torsion ratio, '
 'all ExpTor and BornJ clauses, same-frame coreA and the final AutOffN.\n'
 'Original local classification/correspondence, basic global comparison/reciprocity, central character and '
 'compact norm-one facts remain named foundations; BCS/GUA original base-change and attachment boundaries persist. '
 'No new published application is counted, no Lean replay, no original source or frozen v0.44 proof edits, '
 'and no whole RH/GRH dependency leaf closure is claimed by this component alone.\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,artifact_version='0.45',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,groups.values())),
 inherited_claims=len(inherited),main_tex_sha256=sha(tex),endpoint='HAW19',whole_original_leaf_closures=0),indent=2))
