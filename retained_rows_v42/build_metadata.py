#!/usr/bin/env python3
"""Bind finite retained-row proofs and their exact remaining inputs to pinned bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, required=True)
source = ap.parse_args().source.resolve()
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip() == PIN
sha = lambda b: hashlib.sha256(b).hexdigest()

F = 'src/Formalism/'
I = 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/'
G = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
P = F+'PadicSubsetSums/'
R = F+'LocalToGlobal/SiegelLatticeTheory/FlagStabilizerTensors/'
ROW = F+'SharpRestriction/LevelLetterCocycles/ArithmeticCylinders.lean'
DEFS = P+'CentralIdempotents/EigenbasisOfDistinctRoots.lean'
sources = {
 'idempotents': [
  (ROW,235,261,'wtOf; AllRows'),
  (ROW,298,321,'eDat; eU; phiJ; eJ'),
  (ROW,326,354,'eUk; eJk; admLq'),
  (F+'SharpRestriction/LevelLetterCocycles/DataN.lean',960,967,'NTypes.eSer; centrality, orthogonality, zero and sum fields'),
  (I+'WhittakerJacquetIdempotentsPropertiesPrimeField.lean',307,None,'whittakerJacquetIdempotents_idem_coeff_one; original prime-field endpoint'),
  (I+'HarishChandraSeriesWeightNonnegOfIdempotentGlnPr.lean',13,None,'coefficient trace and nonnegative idempotent weights'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',36,167,'wtOf zero, total mass, identity coefficients, local positivity')],
 'character_frontier': [
  ('src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/LabelDatum.lean',19,118,'zOf; wh; derivatives; LabelDatum; eSerC; wtC; Green; ESerTie'),
  (I+'HarishChandraSeriesWeightLowerComparison.lean',49,None,'lowerWtComparison'),
  (I+'HarishChandraSeriesWeightSquarefreeLabelGelfandG.lean',238,None,'squarefree_label_unipotent; squarefree_label_gelfandGraev'),
  (G+'AdmissibleLabelWeightsOfGreenCuspidalParametrisa.lean',233,None,'original series identity after normalized-label permutation; admissible_label_weights')],
 'finite_polynomials': [
  (DEFS,280,333,'ComparisonTransfer; sqWeight; sqSet; SqMassLower; DivisorBound; TypeWeightExact; TypeSetWeight'),
  (DEFS,403,437,'LocalEstimateIV; LocalEstimateV; PropW'),
  (P+'StableGradedCounts/IRRLemmaP.lean',133,None,'prodMaxInvLeSq: LemmaP'),
  (P+'StableGradedCounts/IRRPrimeRecipSum.lean',129,184,'centralBinom_le'),
  (P+'StableGradedCounts/IRRPrimeRecipSum.lean',271,None,'S_large; prime_reciprocal_sum_bound'),
  (P+'StableGradedCounts/LocalEstimateIVOfTypeSetWeight.lean',1282,1323,'type_weight_exact'),
  (P+'StableGradedCounts/LocalEstimateIVOfTypeSetWeight.lean',1851,1963,'type_set_weight_bound; divisor_square_weight_sum_le; divisorBound_of'),
  (P+'StableGradedCounts/LocalEstimateIVOfTypeSetWeight.lean',2291,2433,'propW_of'),
  (P+'StableGradedCounts/LocalEstimateIVOfTypeSetWeight.lean',2439,None,'localEstimateIV_of_typeSetWeight; localEstimateV_of_typeSetWeight; propW_of_localEstimates')],
 'collision': [
  (DEFS,338,401,'SameFactorCount; CrossFactorCount; SeriesBounds; LocalEstimateII; PrimePowerOrderShare; PrimePowerOrderCount; LocalEstimateIII'),
  (P+'StableGradedCounts/ProdPowFactorizationLe.lean',1,None,'LTE and prime_power_order_count'),
  (P+'StableGradedCounts/FourMulSumLeProduct.lean',1,None,'prime_power_order_share'),
  (P+'StableGradedCounts/LocalEstimateThird.lean',10,114,'geometric/harmonic arithmetic sum'),
  (P+'StableGradedCounts/LocalEstimateThird.lean',138,385,'collision factors; count; weighted divisor union; local_estimate_third')],
 'literal_consumer': [
  (P+'CentralIdempotents/GaloisIrreducibility.lean',14,16,'BB'),
  (P+'CentralIdempotents/GaloisIrreducibility.lean',51,77,'primeToPart; GoodAt'),
  (F+'CyclotomicNorms/StatementT.lean',9,34,'alternate primeToPart; IsGood'),
  (F+'SharpRestriction/LevelLetterCocycles/PlaceLabelTeichmuller.lean',650,690,'exceptional prime and goodAt comparison'),
  (ROW,355,361,'goodAt; locShare'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',17,25,'TieVecW; RangeW'),
  (F+'LocalToGlobal/GlobalTheory/ConcNWeight.lean',238,None,'locShare_le_Wg; weightAllRows_of'),
  (F+'LocalToGlobal/HilbertRowConditions/AllJoin.lean',14,24,'LevelSharp; AllJoinA'),
  (F+'LocalToGlobal/HilbertRowConditions/AllJoinP.lean',18,28,'tieVecW_of_join; weight_of_join'),
  (F+'LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',56,78,'Wg; SizesAt'),
  (F+'LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean',180,199,'CountAllRows; WeightAllRows; retained-defect endpoint'),
  (F+'LocalRingCardinality/Params.lean',6,34,'actual Ranks: f=2ord<=k<=r, m>=2'),
  (G+'LinkIRROfJoinEx.lean',41,140,'sizesRec_at; actual rank comparisons and x^2<=f')],
 'row_construction': [
  (ROW,244,275,'AllRows; LabelCountGoodInjective'),
  (R+'AllRowsOf.lean',23,79,'egA; ES; eT; EtUniv; EtOne; RowsLab'),
  (R+'AllRowsOf.lean',504,526,'allRowsOf; thirdTie'),
  (R+'AllRowsOf.lean',762,883,'exists_lab; RowsAdd; RowsGood; rowsTot_of; rowsLab_of'),
  (R+'RootLatticeThresholds/AllRowsClosed.lean',18,48,'actual EtOne, allRowsOfL and admissible count installation')]
}
inventory, records, excerpts = {}, {}, []
for group, entries in sources.items():
    records[group] = []
    for i,(path,start,end,decl) in enumerate(entries,1):
        b=(source/path).read_bytes()
        assert b == subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}']), path
        lines=b.splitlines(keepends=True)
        if end is None: end=len(lines)
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        part=b''.join(lines[start-1:end])
        rec=dict(id=f'RRT_{group}_{i:02}',path=path,declaration=decl,line_start=start,line_end=end,
                 file_sha256=sha(b),range_sha256=sha(part),range_bytes=len(part),source_commit=PIN,
                 verified_equal_to_pinned_git_blob=True,
                 url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        records[group].append(rec)
        inventory[path]=dict(path=path,sha256=sha(b),bytes=len(b),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nSHA256 {rec["range_sha256"]}\n{part.decode()}\n')

tex=(HERE/'main.tex').read_bytes()
t=tex.decode()
titles={
 'RRT1':'Literal finite unipotent idempotents and exact identity coefficients',
 'RRT2':'Original NTypes series weights are nonnegative normalized probabilities',
 'RRT3':'Exact character-multiplicity formulas and sufficient targets for the remaining character laws',
 'RRT4':'One-sided local domination gives total variation at most f/q',
 'RRT5':'Squarefree factor-type domination by uniform permutation cycle types and weighted divisor bound',
 'RRT6':'Squarefree weighted mass at least 1-2/q',
 'RRT7':'Full permutation invariant proper subset probability at most 7/8',
 'RRT8':'Full original LocalEstimateIV and its independent product bound',
 'RRT9':'Elementary eventual prime reciprocal lower bound with original constant 5',
 'RRT10':'Eventual LocalEstimateV and original exponential witness failure bound',
 'RRT11':'Original WeightAllRows from three remaining local inputs, with exact guard and actual-rank growth',
 'RRT12':'Exact finite tensor cylinder idempotents and identity coefficients',
 'RRT13':'Full finite RowsLab enumeration with prescribed retained labels and multiplicities',
 'RRT14':'Full original prime-power order count and share bounds',
 'RRT15':'Actual root-to-twist collision irreducible factor count',
 'RRT16':'Full original LocalEstimateIII, exact constants and all original degrees'
}
dependencies={
 'RRT1':[], 'RRT2':['RRT1'], 'RRT3':['RRT1','RRT2'], 'RRT4':['RRT2'],
 'RRT5':[], 'RRT6':['RRT4'], 'RRT7':[], 'RRT8':['RRT5','RRT7'],
 'RRT9':[], 'RRT10':['RRT5','RRT9'],
 'RRT11':['RRT2','RRT4','RRT6','RRT8','RRT10','RRT16'],
 'RRT12':['RRT2'], 'RRT13':[], 'RRT14':[], 'RRT15':[], 'RRT16':['RRT5','RRT14','RRT15']
}
scopes={
 'RRT1':(['idempotents'],['Finite field; N=k0+2s+1; k0>=1; exact original eU/eJ formulas.']),
 'RRT2':(['idempotents'],['Original NTypes central orthogonal series partition; literal eU/eJ. This uses their stored partition properties, not an independently constructed automorphic datum.']),
 'RRT3':(['idempotents','character_frontier'],['Coefficient formula is proved for any idempotent. Weight formula uses eU/eJ with positive denominator. Actual lower comparison and squarefree character theorem remain explicit multiplicity/dimension inputs.']),
 'RRT4':(['finite_polynomials','literal_consumer'],['Finite nonnegative probability laws and Q>=(1-delta)P for 0<=delta<=1. Actual character lower comparison remains an input for application.']),
 'RRT5':(['finite_polynomials'],['Any finite field, explicit squarefree product weight, any degree N including 0.']),
 'RRT6':(['finite_polynomials'],['Any finite field; N>=1; explicit squarefree product weight.']),
 'RRT7':(['finite_polynomials'],['Uniform permutation of N symbols; 1<=a<N. No large-N restriction.']),
 'RRT8':(['finite_polynomials'],['Any finite field; 1<=a<N. Product-event application assumes a normalized law agreeing with explicit squarefree weights.']),
 'RRT9':(['finite_polynomials'],['An absolute threshold N0>=100 is proved to exist; no claim that the theorem is proved here for every N>=100.']),
 'RRT10':(['finite_polynomials'],['N>=N0; base probability agrees with explicit squarefree weights.']),
 'RRT11':(['literal_consumer','character_frontier','collision'],['Original eU/eJ local choices and NTypes; original squarefree eU identity and eJ lower comparison; original LocalEstimateII; N>=N0 and original q,q1,d arithmetic guards. Actual rank inequalities f<=k<=r plus x^2<=f justify eventual guard. Abstract SizesAt alone is insufficient for N tending to infinity.']),
 'RRT12':(['row_construction','idempotents'],['Finite local central orthogonal partitions and positive identity coefficients for local idempotents. No claim of adelic Haar or convolution comparison.']),
 'RRT13':(['row_construction'],['Exact finite additive integer multiplicities and supplied good retained-label fibers; original RowsAdd, RowsGood, EtUniv and AutTie supply these but their producers remain inputs.']),
 'RRT14':(['collision'],['q>=2, 4 divides q-1 for count. For share: 16,q1,d divide q-1; q1,d distinct odd primes; max(q1,d)>=16.']),
 'RRT15':(['collision'],['Finite field q>=3; nonzero prescribed twist; degree delta>=1.']),
 'RRT16':(['collision'],['Any finite field; N>=1; 16,q1,d divide q-1, q1,d distinct odd primes, max(q1,d)>=16; nonzero prescribed twist. No character or automorphy input.'])
}
claims=[]
for cid,title in titles.items():
    a=t.index('% BEGIN '+cid+'\n'); b=t.index('% END '+cid+'\n')+len('% END '+cid)
    block=t[a:b].encode(); groups,hyp=scopes[cid]
    claims.append(dict(id=cid,title=title,classification='B',introduced_in='0.42',
        status='complete human proof at the printed scope',depends_on=dependencies[cid],
        hypotheses_retained=hyp,source_groups=groups,sources=[r for g in groups for r in records[g]],
        proof_location=dict(file='retained_rows_v42/main.tex',label='claim:'+cid,
                            line_start=t[:a].count('\n')+1,line_end=t[:b].count('\n')+1,
                            sha256=sha(block),bytes=len(block)),
        scope_note='All applications retain the original objects and the explicitly displayed inputs; a reduction is not input production.'))

frontier=[
 dict(id='RRT_CHARACTER_SQUAREFREE',status='open_input',target='Original wtOf(eU,F)=prod_{P|F}(q^deg(P)-1)^(-1) for every squarefree valid label.',
      next_step='Prove the squarefree series identification, its one Whittaker multiplicity and degree formula, then the degree-preserving normalized-label bridge to original NTypes.',sources=records['character_frontier']),
 dict(id='RRT_CHARACTER_LOWER',status='open_input',target='Original wtOf(eJ,F)>=(1-1/q)wtOf(eU,F) for every valid label.',
      next_step='Prove m_eJ(tau)>=(q^k0-q^(k0-1))m_eU(tau) by actual mirabolic restriction/root exchange, then sum using RRT3 and the original series bridge.',sources=records['character_frontier']),
 dict(id='RRT_LOCAL_ESTIMATE_II',status='open_input',target='Original weighted root-injectivity bad mass <=23 log(q)/sqrt(q), q>=4096, all N.',
      next_step='Prove same-factor and cross-factor prime-to-part fiber counts outside BB; apply RRT5 divisor bounds and the exact convergent degree sums.',sources=records['collision'][:1]),
 dict(id='RRT_ADELIC_ROWS',status='open_input',target='Original HidaSetting, actual ES inflation/eT convolution with fixed Haar, EtOne, RowsAdd, RowsGood and AutTie.',
      next_step='Produce the original adelic reduction/kernel and spectral multiplicity identities; RRT12 and RRT13 finish only the finite algebra/enumeration inside them.',sources=records['row_construction']),
 dict(id='RRT_CYLINDER_COUNTS',status='open_input',target='Original total row count and two actual bad-cylinder counts with one uniform relative error <=1/2.',
      next_step='Supply the three sufficient original counting tests of GQT1-GQT5; this packet does not prove the automorphic counting estimate.',sources=records['literal_consumer'])
]
provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.42',date='2026-11-23',component='retained_rows_v42',
    source_commit=PIN,main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,source_groups=records,
    source_inventory=list(inventory.values()),source_files=list(inventory),published_applications=[],
    inherited_proof_inputs=[dict(file='global_quantitative_v42/main.tex',sha256=sha((HERE.parent/'global_quantitative_v42/main.tex').read_bytes()),
                                claims=['GQT1','GQT2','GQT3','GQT4','GQT5'],role='downstream consumer; not used to prove finite local lemmas')],
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
                    claim_blocks=16,whole_original_leaf_closures=0),
    scope_note='Actual finite producers and exact conditional assembly; GLOBAL_RETAINED_DEFECT remains open. No Lean replay or new published application.')
review_paths=['ordinary_control_v42/review_RRT5_RRT10.json',
              'retained_rows_v42/review_RRT14_RRT16_main_proof_rigidity.json']
provenance['independent_reviews']=[dict(file=p,sha256=sha((HERE.parent/p).read_bytes())) for p in review_paths]
outputs={
 'provenance.json':provenance,
 'source_manifest.json':dict(source_commit=PIN,source_files=list(inventory.values()),ranges=records,verified_against_git=True),
 'contracts.json':dict(schema='rh-retained-rows-contracts/1',artifact_version='0.42',source_commit=PIN,
      original_parent_contract='GLOBAL_RETAINED_DEFECT',original_parent_status='open_C',frontier=frontier,
      sufficient_local_contract=['Original NTypes series partition and eU/eJ choices.','Original squarefree eU law.','Original eJ lower comparison.','Original LocalEstimateII.','Actual host arithmetic guards and N>=N0.'],
      exact_completed_substatements=['ComparisonTransfer (from its own finite probability hypotheses)','TypeWeightExact','TypeSetWeight','SqMassLower','SqMassLeOne','DivisorBound','LemmaP','LocalEstimateIV','PrimePowerOrderCount','PrimePowerOrderShare','LocalEstimateIII'],
      eventual_sufficient_substatement='LocalEstimateV for every N>=N0, with the original constant 5; original actual rank growth makes this sufficient for the selected family.',
      row_scope='Finite ES and RowsLab construction only. Full AllRows, Haar identities, RowsAdd/RowsGood producers and counting estimates remain inputs.'),
 'closure.json':dict(component='retained_rows_v42',artifact_version='0.42',new_claims=list(titles),new_claim_count=16,
      completed_original_substatements=['LocalEstimateIII','LocalEstimateIV','LemmaP','PrimePowerOrderCount','PrimePowerOrderShare','TypeSetWeight','TypeWeightExact','SqMassLower','SqMassLeOne','DivisorBound'],
      completed_conditional_endpoint='WeightAllRows on the original local idempotents from the remaining three local inputs and exact guards.',
      whole_obligation_closures=[],remaining_global_contract_ids=['GLOBAL_RETAINED_DEFECT'],
      no_new_published_application=True,no_lean_replay=True,
      warning='A finite substatement closure is not closure of the global C contract; initial-character and automorphic input production remains open.')
}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,records.values())),
                     main_tex_sha256=sha(tex),whole_original_leaf_closures=0),indent=2))
