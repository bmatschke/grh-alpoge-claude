#!/usr/bin/env python3
"""Bind the original uniform logarithmic theorem and actual lattice consumers."""
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
SRC = parser.parse_args().source.resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip()==PIN
G = 'src/Formalism/SharpRestriction/GrowthBounds/'
S = G+'LogarithmicSums/'
L = 'src/Formalism/LocalRingCardinality/'
C = 'src/Formalism/LocalToGlobal/GroupLattices/'
T = 'src/Formalism/SharpRestriction/'

SPECS = {
 'actual_data':[
  (L+'DataParams.lean',62,None,'ParameterChoice prime: all original numerical guards'),
  (T+'ElevenLe.lean',15,144,'exact SizesAt component bounds and conjunction'),
  (T+'ParConsts.lean',31,100,'FamP: one actual instance/comparison/fill family and its constant order'),
  (G+'IsResidueClassZero.lean',14,65,'Consts, rG, Gp, N1, L1, L2 and exact La=K.La*N1^2*log(a)'),
  (G+'IsResidueClassZero.lean',66,400,'actual fills, orbits, asks, losses, served sets, gain, mean and Sv')],
 'star_contract':[
  (S+'Conclusion1OfGainBoundAll.lean',99,160,'InWin, exact askP/askG gain predicates, RequiresAll, StarAt, StarAll and AdmFam'),
  (S+'PartnerCountOfCentral.lean',440,469,'all thirteen original NumStar fields'),
  (G+'LogarithmicSums.lean',18,22,'literal RestStar with constant before every instance family')],
 'orbit_and_shift':[
  (S+'TsumTruncatedShiftLe.lean',1,None,'finite odd-exponent shift inequalities and their exact log loss'),
  (S+'PartnerCountOfCentral.lean',39,197,'actual cyclic orbit dictionary and injective predecessor kink inequality'),
  (S+'PartnerCountOfCentral.lean',198,438,'fill positivity, geometric decomposition, good-orbit lower bound and kink transport')],
 'star_cases':[
  (G+'SmallOrderPrimes.lean',70,83,'adm1 good-orbit count and central orbit guards'),
  (S+'PartnerCountOfCentral.lean',471,561,'orbit count and finite arithmetic budgets'),
  (S+'PartnerCountOfCentral.lean',562,688,'exact p<p0 StarAt branch'),
  (S+'PartnerCountOfCentral.lean',690,851,'exact p0<=p<Xprime branch and StarAll assembly')],
 'uniform_star':[
  (G+'SmallOrderPrimes.lean',115,120,'both original adm5 exponents'),
  (S+'StarNum.lean',15,327,'explicit CStar, small budgets and eventual NumStar'),
  (S+'StarNumB.lean',12,359,'N1/Gp ceilings, full polynomial budget and uniform facts'),
  (S+'StarFam.lean',10,40,'whole original star_fam quantifier order')],
 'gain_and_count':[
  (S+'NotSingularOfCentral.lean',13,18,'GainBoundConstants'),
  (S+'NotSingularOfCentral.lean',209,350,'representative partition and exact sum of losses'),
  (S+'NotSingularOfCentral.lean',358,739,'all served/empty/signal/inert branches and GainBoundAllUniform'),
  (S+'GainBoundAllAddOneOfGainBoundAllRequired.lean',139,247,'full RequiresAll, including arbitrary integer top functions'),
  (S+'GainBoundAllAddOneOfGainBoundAllRequired.lean',249,393,'exact C+1 conversion from askP to askG'),
  (S+'RemainingCountingStatement.lean',10,20,'literal FamilyAskBounds and RemainingCountingStatement'),
  (G+'LogarithmicSums.lean',43,64,'original constant choice and complete remaining-count consumer'),
  (G+'SmallOrderPrimes.lean',190,197,'adm9 original coefficient error exponent bound'),
  (G+'SmallOrderPrimes.lean',220,247,'all admG1 clauses, type-prime guards and full admitted conjunction')],
 'global_interface':[
  (T+'GlobalTheoremInputs.lean',97,140,'loG/flG and ALL FIVE LinkG_at conjuncts, then full LinkG'),
  (G+'PlaneCountTheoremWithConstants.lean',65,244,'least exponent, exact 4*abs(C)+1 loss transport and finite class sum'),
  (G+'PlaneCountTheoremWithConstants.lean',296,320,'ServedGIdx, SvBound, FrobNe and original sufficient guards'),
  (G+'PlaneCountTheoremWithConstants.lean',395,546,'ceil absorption and exact 2m*Nv*a/p Sv bound'),
  (G+'PlaneCountTheoremWithConstants.lean',621,630,'actual level-prime exclusion and even-Frobenius nonvanishing'),
  (G+'PlaneCountTheoremWithConstants.lean',718,821,'full linkG_at_core/of consumers with unchanged five fields'),
  (G+'PlaneCountTheoremWithConstants.lean',823,878,'eventual first-growth, NPDescF, finite length and uniform LinkG installation')],
 'local_depth':[
  (L+'DataGatTies.lean',7,30,'all original actual-rank, place, orbit-step and weight comparison fields'),
  (L+'DataLatDefs.lean',11,53,'actual LatCmp embedding, integrality, independent basis and NuServedDef'),
  (L+'DataDIVDefs.lean',48,56,'full NuDef, local inclusion and normalized lengths'),
  (L+'DataExtra.lean',27,33,'NuUnserved at every regular unserved place'),
  (G+'PlaneCountTheoremWithConstants.lean',547,620,'NuServed, finite-basis denominator clearing and rational descent'),
  (G+'PlaneCountTheoremWithConstants.lean',632,716,'residue-prime valuation, original depth inclusion and LenServed')],
 'integral_operator':[
  (G+'DataG.lean',11,199,'actual Weyl, dual-Weyl, component function lattices and incoming-neighbor p^ArV operator'),
  (G+'UnramifiedQuadraticSetting.lean',12,28,'original coefficient DVR and fraction fields, unramified uniformizer and z^2=p setting'),
  (G+'UnramifiedQuadraticSetting.lean',70,112,'signed weights, dual-Weyl model, actual edges and their elementary-divisor basis'),
  (G+'FormalGroupSystem.lean',802,808,'both original adm12 integral-stability fields'),
  (C+'FockModels/OperatorsPreserveLattices.lean',15,126,'row homogeneity, dominant support and integral Weyl diagonal scaling'),
  (C+'FockModels/OperatorsPreserveLattices.lean',128,234,'signed determinant twist and basis-independent Weyl model'),
  (C+'FockModels/OperatorsPreserveLattices.lean',236,344,'two original edge steps, exact p^ArV factor, and both full operator endpoints'),
  (G+'LatticeSystems.lean',1598,1775,'dual-Weyl diagonal step and tensor/basis model'),
  (G+'LatticeSystems.lean',1778,1960,'exact original edge and midpoint basis interfaces')],
 'rational_descent':[
  (C+'ComparisonMaps/YvRatOfValRat.lean',13,119,'general separating-evaluation retraction and rational linear operator descent'),
  (C+'ComparisonMaps/YvRatOfValRat.lean',123,283,'actual polynomial evaluations, invalid tuples, ValRat and yvRat_of_valRat'),
  (C+'ComparisonMaps/NpDescOfValRat.lean',8,16,'literal YvRat and NPDesc consumer'),
  (C+'ComparisonMaps/NpDescFOfValRatF.lean',9,22,'exact family descent and CmpTied.valRat'),
  (C+'StdSubAtOfRing.lean',76,89,'entire GroupCompatibilityAll and its eventual family predicate'),
  (G+'JointsLit.lean',178,346,'ordered rational products and literal NPDesc_of'),
  (L+'Lemmas.lean',968,1030,'M_inf_Vram, NPDesc and original rational-preimage NP_eq_span')],
 'lengths':[
  (G+'IsResidueClassZero.lean',430,483,'LatTied and literal LatticeLengthsAtPlace'),
  (L+'Lemmas.lean',1061,1182,'exact ramification-normalized length transport and full empty-served case'),
  (L+'Lemmas.lean',1197,1251,'finite annihilator and sizeDataLat_of_latDefs')],
 'selected_tops':[
  (T+'GlobalSchurBounds/Chosen.lean',15,70,'actual ChTT/ChBad pointwise and eventual selected-top predicates'),
  (T+'SmoothDesignExistence/AdmissibleTopsMertens.lean',15,None,'full TopsF-to-Adm2F finite harmonic consumer'),
  (G+'SmallOrderPrimes.lean',85,99,'BTT and exact full adm2 inequality')]
}
inventory, groups, excerpts = {}, {}, []
for group,specs in SPECS.items():
    groups[group]=[]
    for i,(path,lo,hi,title) in enumerate(specs,1):
        data=(SRC/path).read_bytes()
        assert data==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+path]),path
        lines=data.splitlines(keepends=True);hi=hi or len(lines)
        assert 1<=lo<=hi<=len(lines),(path,lo,hi,len(lines))
        block=b''.join(lines[lo-1:hi])
        item=dict(id=f'GLG_{group}_{i:02}',path=path,line_start=lo,line_end=hi,
          declaration=title,file_sha256=sha(data),range_sha256=sha(block),range_bytes=len(block),
          source_commit=PIN,verified_equal_to_pinned_git_blob=True,
          url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{lo}-L{hi}')
        groups[group].append(item)
        inventory[path]=dict(path=path,sha256=sha(data),bytes=len(data),line_count=len(lines),
                             verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{item["id"]}] {title}\n{item["url"]}\nRange SHA256: {sha(block)}\n{block.decode()}\n')

DEPS={
 1:[],2:[],3:['GJ3'],4:['GLG1','GLG2'],
 5:['GLG1','GLG2','GLG4'],6:['GLG1','GLG2','GLG3','GLG4'],
 7:['GLG1','GLG4','GLG5','GLG6'],8:['GLG1','GLG2','GLG5','GLG6'],
 9:['GLG1','GLG2','GLG7','GLG8'],
 10:['GLG1','GLG8'],11:['GLG1','GLG2','GLG9'],
 12:['GLG10'],13:['CB2'],14:['GLG13'],
 15:['GLG14','SR2'],16:[],
 17:['GLG8','GLG9','GLG10','GLG11','GLG12','GLG15','GW2'],
 18:['GLG9','GLG10','GLG12','GLG13','GLG14','GLG15','GLG16','GLG17',
     'GW2','TC6','EA9','GI8','GII8','BC8','GJ4']
}
GROUPS={
 1:['actual_data','orbit_and_shift'],2:['orbit_and_shift'],
 3:['actual_data','orbit_and_shift'],4:['star_contract','star_cases','orbit_and_shift'],
 5:['star_contract','star_cases'],6:['star_contract','star_cases'],
 7:['actual_data','star_contract','uniform_star'],
 8:['actual_data','star_contract','gain_and_count'],
 9:['star_contract','uniform_star','gain_and_count'],
 10:['actual_data','global_interface'],11:['actual_data','global_interface'],
 12:['actual_data','local_depth'],13:['integral_operator'],
 14:['local_depth','integral_operator','rational_descent'],
 15:['local_depth','rational_descent','lengths'],
 16:['actual_data','selected_tops'],
 17:['actual_data','global_interface','local_depth','lengths','gain_and_count'],
 18:['actual_data','star_contract','gain_and_count','global_interface','rational_descent']
}
SCOPES={
 1:'Actual original ParameterChoice and all original lifts; signed filling shifts and exact finite constants.',
 2:'Every subset of positive odd exponents and all stated nonnegative arguments; finite support is proved.',
 3:'The same selected orbit representatives, including no-predecessor cases; original partner and parity conventions.',
 4:'All thirteen NumStar fields and exact one-good-orbit lower comparison.',
 5:'Every candidate prime p<p0, every good representative and every lift; coefficient 13+4*K.tII+160*C31.',
 6:'Every p0<=p<Xprime, every good representative and every lift; original bo appears with coefficient one.',
 7:'Full RestStar: arbitrary real Ce,Cm, C0 before C before X,Y before x0, all later weights/orbits/primes; bo=b^(x^(-eps/2)).',
 8:'Full original askP GainBoundAllUniform under StarAll and the stated ep bound; every original empty/signal/inert branch.',
 9:'Complete original RemainingCountingStatement and FamilyAskBounds, on every admitted original instance family; Ccount before X,Y; no upper bound on b_s.',
 10:'Actual served GIdx, exact served coverage and Sv<=2*m*Nv*a/p; every regular word/place and empty orbit cases.',
 11:'Actual finite vonMangoldtClassSum and exact lo/fl transport with 4*abs(C)+1 for arbitrary real C and bo.',
 12:'Exact NuServed from actual LatCmp and NuServedDef; floor(ew*tau) depth over the original DVR; no operator rationality assumed.',
 13:'Both original FormalGroupSystem.adm12 fields, Mna and M, for every GAtP and vertex; signed weights, actual coefficient DVR and p^ArV unchanged.',
 14:'Full ValRat -> YvRat -> NPDesc and GroupCompatibilityFamily -> NPDescF implications; compatibility existence stays an antecedent.',
 15:'Full LatticeLengthsAtPlace with exact vO(p)=a_w*e_w normalization; finite length proved; separate original type-prime guard retained.',
 16:'Full original TopsF -> Adm2F with a single threshold and no new selection of tops; elementary harmonic estimate suffices.',
 17:'All five literal LinkG_at conjuncts on the same data under all original local-growth/mean/comparison inputs.',
 18:'Full literal LinkG implication on the same original family, retaining complete AdmFam, NPDescF/compatibility and exact eventual mean input; no whole outer producer closed.'
}
FOUNDATIONS=[
 dict(id='GLG_ORIGINAL_FAMILY_DATA',kind='explicit_original_data_and_guards',
  statement='The original D,L,FamP, ParameterChoice, SizesAt, fills, support, GatTies, LatCmp and lattice records remain the actual supplied objects. No independently selected family is substituted.',
  not_reconstructed_as_a_whole=True,source_groups=['actual_data','local_depth','lengths']),
 dict(id='GLG_ADMISSION_ANTECEDENT',kind='explicit_original_admissibility_antecedent',
  statement='The full original AdmFam/admitted record, including admG1 and its additional clauses, is retained whenever quantified. GLG7/9 prove the complete original nested counting endpoints under that exact original antecedent; they do not construct an admitted family.',
  not_reconstructed_as_a_whole=True,source_groups=['star_contract','gain_and_count']),
 dict(id='GLG_COMPATIBILITY_ANTECEDENT',kind='explicit_original_comparison_antecedent',
  statement='Actual ValRat or GroupCompatibilityFamily, including CmpTied, is retained. GLG14 supplies its complete rational-descent consumer. Existence of that comparison package is not inferred.',
  not_reconstructed_as_a_whole=True,source_groups=['rational_descent']),
 dict(id='GLG_MEAN_ANTECEDENT',kind='explicit_original_uniform_mean_antecedent',
  statement='The exact eventual MeanKappaBound on the same X and K is retained in GLG18. GW2 can discharge it only with its recorded canonical-deficit and coefficient bounds; nonnegative K alone is insufficient.',
  not_reconstructed_as_a_whole=True,source_groups=['actual_data','global_interface']),
 dict(id='GLG_STANDARD_ALGEBRA_ANALYSIS',kind='standard_mathematical_background',
  statement='Finite-dimensional linear algebra, basis extension, polynomial coefficients, elementary divisors over DVRs, torsion-free flatness over a DVR, finite tensor exactness, geometric series and elementary real limits. Their relevant finite consumers and normalizations are proved explicitly here.',
  not_a_new_arithmetic_producer=True,source_groups=['integral_operator','rational_descent','lengths','uniform_star'])
]
EXT={n:['GLG_STANDARD_ALGEBRA_ANALYSIS'] for n in range(1,19)}
for n in [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]:
    EXT[n].append('GLG_ORIGINAL_FAMILY_DATA')
for n in [4,7,9,17,18]:EXT[n].append('GLG_ADMISSION_ANTECEDENT')
for n in [14,15,18]:EXT[n].append('GLG_COMPATIBILITY_ANTECEDENT')
for n in [17,18]:EXT[n].append('GLG_MEAN_ANTECEDENT')

proof=(HERE/'main.tex').read_bytes();text=proof.decode();claims=[]
for n in range(1,19):
    cid=f'GLG{n}'
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert m,cid
    named=set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b',m.group()))-{cid}
    assert named<=set(DEPS[n]),(cid,'unrecorded named dependencies',named-set(DEPS[n]))
    assert all(not d.startswith('GLG') or int(d[3:])<n for d in DEPS[n]),cid
    block=m.group().encode()
    claims.append(dict(id=cid,title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1),
      introduced_in='0.46',classification='B',
      status='complete human proof at the explicitly stated original scope',
      depends_on=DEPS[n],external_input_ids=EXT[n],published_input_ids=[],
      hypotheses_retained=[SCOPES[n]],source_groups=GROUPS[n],
      sources=[s for g in GROUPS[n] for s in groups[g]],
      proof_location=dict(file=HERE.name+'/main.tex',label='claim:'+cid,
        line_start=text[:m.start()].count('\n')+1,line_end=text[:m.end()].count('\n'),
        sha256=sha(block),bytes=len(block)),
      source_proof_is_not_human_proof=True))
claims[16]['dependency_scope_overrides']={'GW2':'Only a recorded way to discharge the explicit mean antecedent, with its complete original hypotheses; not an automatic fact for arbitrary K.'}
claims[5]['non_premise_reference_explanations']={
 'GLG5':'Equation GLG.18 names the common StarAt target. GLG6 does not invoke the small-prime proof under its mutually exclusive p<p0 guard.'}
claims[17]['dependency_scope_overrides']={
 'GW2':'Conditional discharge of the explicit eventual mean hypothesis only, with all recorded coefficient/canonical-deficit guards.',
 'GLG13':'Its integral operator endpoint is an actual nested producer reused through GLG14.',
 'GLG16':'A separately completed original admissibility consumer; full AdmFam remains an antecedent.',
 **{d:'Frontier accounting: the previously complete local projection certificate is reused at its stated actual-model scope, not asserted without that scope.' for d in ['TC6','EA9','GI8','GII8','BC8','GJ4']}}
human_ids=sorted({d for ds in DEPS.values() for d in ds if not d.startswith('GLG')})
ledger={r['id']:r for r in json.loads((ROOT/'provenance.json').read_text())['claims']}
inherited=[]
for cid in human_ids:
    r=ledger[cid]
    loc=r.get('proof_location') or {'file':'saturation/saturation_section.tex'}
    p=ROOT/loc['file'];data=p.read_bytes();lines=data.splitlines(keepends=True)
    if 'line_start' in loc:
        lo,hi=loc['line_start'],loc['line_end']
        block=b''.join(lines[lo-1:hi])
        assert sha(block)==loc['sha256'],cid
        binding='exact previously recorded numbered-claim byte range'
    else:
        # Early immutable chapters predate numbered BEGIN/END blocks.
        # Bind the entire original chapter rather than inventing boundaries.
        lo,hi=1,len(lines);block=data
        assert re.search(r'\b'+cid+r'\b',data.decode()),cid
        binding='entire immutable legacy chapter containing this named human claim'
    inherited.append(dict(id=cid,file=loc['file'],main_tex_sha256=sha(data),
      block_sha256=sha(block),line_start=lo,line_end=hi,binding_scope=binding,
      kind='numbered_human_proof_dependency',not_an_external_foundation=True))
assert not set(human_ids)&{f['id'] for f in FOUNDATIONS}
reviews=[]
claim_lookup={c['id']:c for c in claims}
for p in sorted(HERE.glob('review_*.json')):
    d=json.loads(p.read_text())
    assert d.get('result',d.get('status'))=='PASS',p
    bound=d.get('proof_sha256',d.get('proof_file_sha256',d.get('main_tex_sha256')))
    assert bound==sha(proof),(p,bound,sha(proof))
    for checked in d.get('claims_reviewed',[]):
        if isinstance(checked,dict):
            assert checked['result']=='PASS',checked
            assert checked['block_sha256']==claim_lookup[checked['id']]['proof_location']['sha256'],checked
    reviews.append(dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())))

# Formula references can also carry proof dependencies. A reference to a shared
# displayed target is explicitly distinguished from using the prior proof.
blocks={c['id']:re.search(r'% BEGIN '+c['id']+r'\n.*?% END '+c['id']+r'\n',text,re.S).group()
        for c in claims}
owners={n:cid for cid,block in blocks.items()
        for n in re.findall(r'\\tag\{GLG\.(\d+)\}',block)}
for claim in claims:
    cid=claim['id'];block=blocks[cid]
    refs=set(re.findall(r'GLG\.(\d+)',block))-set(re.findall(r'\\tag\{GLG\.(\d+)\}',block))
    needs={owners[n] for n in refs if n in owners and owners[n]!=cid}
    non_premises=set(claim.get('non_premise_reference_explanations',{}))
    assert needs<=set(claim['depends_on'])|non_premises,(cid,'unrecorded formula dependencies',needs)

completed=[
 'Full literal RestStar, including arbitrary Ce,Cm and exact constant-before-family order (GLG7)',
 'Full literal GainBoundAllUniform finite consumer and all prime branches (GLG8)',
 'Full original RemainingCountingStatement and FamilyAskBounds (GLG9)',
 'Actual ServedGIdx, ServedOrbitsContained and sharp original SvBound (GLG10)',
 'Exact finite class-sum and lo/fl-to-loG/flG normalization (GLG11)',
 'Original NuServed depth inclusion (GLG12)',
 'Both original integral-operator adm12 fields for every actual GAtP (GLG13)',
 'Original ValRat/YvRat/NPDesc and GroupCompatibilityFamily/NPDescF consumers (GLG14)',
 'Original finite and ramification-normalized LatticeLengthsAtPlace (GLG15)',
 'Complete original TopsF-to-Adm2F finite harmonic consumer (GLG16)',
 'All five original LinkG_at fields under the exact supplied inputs (GLG17)',
 'Full same-family LinkG implication, with explicit admitted/compatibility/mean antecedents (GLG18)'
]
coverage={
 'RestStar':'GLG7','RemainingCountingStatement':'GLG9','FamilyAskBounds':'GLG9',
 'FormalGroupSystem.adm12.Mna':'GLG13','FormalGroupSystem.adm12.M':'GLG13',
 'ValRat_to_YvRat':'GLG14','YvRat_to_NPDesc':'GLG14',
 'GroupCompatibilityFamily_to_NPDescF':'GLG14',
 'LatticeLengthsAtPlace':'GLG15','TopsF_to_Adm2F':'GLG16',
 'LinkG_at.1.local_depth_length_empty':'GLG12/GLG15/GLG17, retaining full admG1',
 'LinkG_at.2.Sv':'GLG10/GLG17',
 'LinkG_at.3.gain_and_finite_class_sum':'GLG9/GLG11/GLG17',
 'LinkG_at.4.served_coverage':'GLG10/GLG17',
 'LinkG_at.5.MeanKappaBound':'Explicit original input; GW2 only under its recorded guards',
 'LinkG.uniform_threshold':'GLG18, with deltaG(x)=x^(-eps/2)'
}
traps=[
 'C0 before C before X,Y before the uniform x0 in RestStar; Ccount before X,Y in RemainingCountingStatement.',
 'Every original integer b_s>=bprime is allowed, with no upper bound; all lifts, good orbits and primes share one threshold.',
 'The actual La is K.La*N1^2*log(a); the bo term has coefficient one and deltaG(x)=x^(-eps/2).',
 'All five LinkG_at conjuncts use the same actual member, fills, local comparison, operators, lattices, ranks and deficits.',
 'The operator is p^ArV times the incoming-neighbor sum; signed determinant twists, two z-steps with z^2=p, and both integral models are retained.',
 'Flat descent concerns finite intersections and the actual rational preimage, with no Galois assumption on the coefficient field extension.',
 'Normalized length is local O-length/vO(p)=local A-length/ew; no rank or ramification factor is lost.',
 'Type primes retain their original separate definitions; empty served sets and inert zero-Frobenius branches are included.',
 'Full admG1 is retained, not just its length clause. Its occurrence in AdmFam is not a construction of local growth data.',
 'MeanKappaBound remains explicit in the uniform LinkG implication; GW2 does not establish it for arbitrary nonnegative K.',
 'No individual conditional estimate is promoted to a construction of the common original family.'
]
frontier=[
 'Realize the actual GroupCompatibilityFamily/CmpTied (or its exact NPDescF consequence) on the chosen common family.',
 'Supply every retained AdmFam input on that same family, including its original first-growth and additional local clauses.',
 'Supply the same-family mean deficit with the exact original coefficient/canonical-deficit hypotheses, or explicitly use the already proved GW2 endpoint where those hypotheses are met.',
 'The other global denominator, retained-defect, period/height and spectral suppliers remain separate; this packet asserts no whole selected-leaf closure.'
]
contracts=dict(schema='rh-global-local-gain-contracts/1',artifact_version='0.46',
 component=HERE.name,source_commit=PIN,proof_file_sha256=sha(proof),
 endpoint_claim='GLG18',unconditional_nested_counting_endpoint='GLG9',
 original_endpoint='Formalism.MainNotions.AuxBlock8.Pf.RemainingCountingStatement',
 actual_operator_endpoint='GLG13',finite_installer='GLG17',
 completed_original_substatements=completed,original_field_coverage=coverage,
 exact_guards_preserved=traps,remaining_actual_producers=frontier,
 human_dependency_ids=human_ids,external_input_ids=[f['id'] for f in FOUNDATIONS],
 selected_consumer_only=False,whole_obligation_closures=[],
 proposed_whole_obligation_closures=[],no_lean_replay=True,
 not_claimed=['existence of a compatible/admitted common family from conditional estimates',
  'unconditional whole LOCAL_GAIN producer','new mean theorem for arbitrary nonnegative constants',
  'global denominator/period-height/spectral completion','complete RH or GRH'])
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.46',date='2026-11-23',
 component=HERE.name,source_commit=PIN,main_tex_sha256=sha(proof),proof_file_sha256=sha(proof),
 claims=claims,source_groups=groups,source_inventory=list(inventory.values()),
 source_files=list(inventory),published_applications=[],retained_foundations=FOUNDATIONS,
 inherited_human_inputs=inherited,independent_reviews=reviews,
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
 validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
  claim_blocks=len(claims),direct_named_claim_dependencies_checked=True,
  numbered_formula_dependencies_checked=True,
  external_foundations_separate_from_claim_DAG=True,whole_original_leaf_closures=[]),
 scope_note='A complete original nested analytic counting producer and actual finite operator/depth/descent suppliers. The full LinkG conclusion is an exact implication with explicit common-family antecedents; no outer whole obligation is declared closed.')
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.46',component=HERE.name,
 proof_file_sha256=sha(proof),new_claims=[c['id'] for c in claims],new_claim_count=len(claims),
 completed_original_substatements=completed,whole_obligation_closures=[],
 proposed_whole_obligation_closures=[],remaining_actual_producers=frontier,
 status='Complete nested original endpoints; explicit conditional same-family LinkG installer; no whole selected-leaf closure.',
 exact_error_and_constants_preserved=True,all_five_LinkG_fields=True,
 full_admission_and_actual_compatibility_retained=True,mean_hypothesis_explicit=True,
 both_original_integral_models=True,actual_rank_and_DVR_preserved=True,no_lean_replay=True)
outputs={
 'provenance.json':prov,'contracts.json':contracts,'closure.json':closure,
 'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,
   source_commit=PIN,source_files=list(inventory.values()),ranges=groups,verified_against_git=True),
 'retained_foundations.json':FOUNDATIONS,'published_inputs.json':[]}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 'UNIFORM LOGARITHMIC GAIN AND ACTUAL LOCAL LATTICES — v0.46\n'
 f'Source pin: {PIN}\nMain SHA256: {sha(proof)}\n\n'
 f'{len(claims)} numbered human proofs, classification B; {len(inventory)} pinned source files; '
 f'{sum(map(len,groups.values()))} source ranges; {len(inherited)} inherited numbered proof bindings.\n\n'
 'Substantive new analytic producer: GLG1–9 prove the complete original RemainingCountingStatement, '
 'through full RestStar and the exact askP-to-askG conversion. C0 and Ccount are chosen before every '
 'instance family. The eventual threshold is uniform in the member, prime, orbit, lift and both top '
 'functions, including arbitrarily large b_s. The original error is b^(x^(-epsilon/2)); the original '
 'N1^2 height factor, thirteen NumStar inequalities, all ceiling losses and coefficient-one bo term '
 'are retained. The exponential polynomial budget is written explicitly, not delegated to source execution.\n\n'
 'Actual finite suppliers: GLG10–12 prove the original served-index/coverage/Sv/depth interfaces and '
 'the exact loss normalization. GLG13 proves stability of BOTH original Weyl and dual-Weyl lattices, '
 'including signed weights and the two half-steps giving exactly p^ArV. GLG14 proves rational descent '
 'of the actual operators and selected finite intersection from the original ValRat/CmpTied input. '
 'GLG15 proves finiteness and the exact ramification-normalized local length. GLG16 completes '
 'TopsF -> Adm2F by a finite harmonic sum without using a prime number theorem or reselecting the tops.\n\n'
 'GLG17 installs all FIVE literal LinkG_at fields. GLG18 gives the full uniform LinkG implication '
 'with C_G=4*Ccount+1 and deltaG(x)=x^(-epsilon/2). The exact original compatibility, full admission '
 '(including admG1) and mean-deficit hypotheses remain explicit. GW2 is used only at its recorded '
 'canonical-deficit/coefficient scope. No whole outer obligation is closed by this packet.\n\n'
 'The original local projection certificates TC6/EA9/GI8/GII8/BC8/GJ4 and normalized-length '
 'consumer SR2 are reused; this chapter supplies previously unexpanded integral/rational consumers '
 'and the original logarithmic analytic producer. It does not replace them with an abstract family '
 'or claim existence from inequalities.\n\nRemaining actual frontier:\n'
 +''.join('- '+s+'\n' for s in frontier)+
 '\nAll source bytes/ranges are checked against the immutable source commit. Numbered human '
 'dependencies and retained original antecedents/foundations have separate identifiers. No Lean replay '
 'or correctness re-certification was performed; no common, historical or original-source files are edited.\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
        if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,artifact_version='0.46',
 hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),
 source_ranges=sum(map(len,groups.values())),inherited_claims=len(inherited),
 main_tex_sha256=sha(proof),nested_analytic_endpoint='GLG9',
 uniform_conditional_endpoint='GLG18',whole_original_leaf_closures=[]),indent=2))
