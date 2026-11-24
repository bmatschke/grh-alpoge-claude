"""Record the exact remaining Type-I interfaces without treating them as proofs."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
d = json.loads((BASE/'output/RH_reconstruction_v0_8/provenance.json').read_text())
by_id = {c['id']: c for c in d['claims']}
roles = {
    'GramDeterminantGradedHypothesis': 'The exact restricted initial-Gram premise still needed by the proved TI6 averaging application.',
    'gram_hypothesis_of_log_bound': 'First priority: prove the actual restricted saturation and highest-vector projection bridge supplying the initial-Gram determinant bound.',
    'theoremMV7': 'Assemble the actual weighted partner mean after the restricted Gram and integral-partner construction is established.',
    'tieOpsX_main': 'Construct simultaneous integral tie operators with all prefix, order and multiplicity-space identities.',
    'partnerMX_of_parts': 'Transfer the compatible tie operators into the actual weighted integral-partner estimate.',
    'RestAll': 'Exact package of terminal, dimension, digit-class and depth inputs to the segment count.',
    'segment_weighted_counting_bound_of_all_remaining_bounds': 'Match endpoint dimension weights and digit-class counts to the actual segment bad-share theorem.',
    'WittIdent': 'Identify the coefficient-ring coordinates used by the paired cleaned lifts.',
    'RestRawTail1': 'Produce the actual raw cleaned-lift polynomials with their height and other-edge bounds.',
    'RestForm': 'Prove the exact diagonal Fock pairing and error identity for those same lifts.',
    'paired_lifts_of_identity': 'Assemble actual CCe/CCe-prime lifts; TI2 already proves the final Smith perturbation argument.',
    'theorem_I_of_intermediate_bounds': 'Join harmonic-model, ring-independence, minor comparison, mean, and uniform numerical inputs into Type-I Conclusion2.',
    'HypI': 'Keep every literal Type-I numerical assumption distinct from the Type-II assumptions.',
    'WeightI': 'Keep the actual rank-one weight-box and highest-weight family fixed during averaging.',
    'tI': 'Match all constructed lifts to the literal height bound.',
    'Conclusion2': 'Endpoint: a single uniform nonnegative exceptional function with its stated mean and LPprime conclusion.',
}
targets=[]
seen=set()
for cid in ['TI6','TI9']:
    for src in by_id[cid]['sources']:
        short=src['declaration'].split('.')[-1]
        if short not in roles: continue
        key=(src['path'],src['line_start'],src['line_end'])
        if key in seen: continue
        seen.add(key)
        record=deepcopy(src)
        record['role']=roles[short]
        record['human_status']='remaining_application_or_construction_input; not claimed proved by this target list'
        raw=(BASE/'alpoge-rh'/src['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==src['sha256']
        excerpt=b''.join(raw.splitlines(keepends=True)[src['line_start']-1:src['line_end']])
        assert hashlib.sha256(excerpt).hexdigest()==src['range_sha256']
        targets.append(record)
out={
    'version':'0.8','commit':PIN,
    'status':'Read-only source targets for the remaining human reconstruction; no additional proof is asserted.',
    'completed_previous_frontier':'All former frame/cloud/edge targets are discharged locally by FG1–8, OR1–8, CP1–8 and EA1–9. Full Type-II ConclusionE follows under its literal hypotheses for C>=4129.',
    'next_local_priority':'Restricted initial-Gram bounds and compatible partners across ties, followed by weighted segment transfer and actual paired cleaned lifts.',
    'completed_Type_I_inputs':['TI1–TI2 integral lattices and Smith primitive-test interpretation','TI3 exact gamma degree and leading form','TI4 GamInt with constant10 and the proved parameter-dependent normalization','TI5 WindowFullAP polynomial-matrix averaging'],
    'precision_notes':['TI6 remains conditional on the actual graded initial-Gram premise.','The exact sharper GamIntC exponent is not claimed.','TI7–TI8 are proved transfer implications; their actual KeyIneq, density and boundary supply remain.','No Type-II local theorem is substituted for the separate rank-one construction.'],
    'targets':targets,
    'global_branches_unchanged':[
        {'claim_ids':['PL12','PL13','PL14','PL15','PL16','PL17','PL18','PL19','PL20','AG1','AG2','AG3','AG4','AG5','AG6','AG7','AG8','AG9','AG10'], 'target':'Actual theta/common-image identities, chain norms, archimedean spectral-word and arithmetic-kernel normalization.'},
        {'claim_ids':['LC7','SR1','SR2','SR3','SR4','SR5','GF1','GF2','GF3','GF4','GF5','GF6','GF7','GF8','GF9'], 'target':'Actual dimension balance, retained-source integral/isometric metric transport, and discarded-target bounds; retain all already proved conditional deductions.'},
        {'claim_ids':['OH6','OH7','OH8','GH3','GH5','GH7'], 'target':'Congruence denominators and actual two-primary, odd-minus and odd-plus cohomological windows.'},
        {'claim_ids':['OH2','OH3','OH4','OH5','GH4','GH5','GH6','GH7','SC2'], 'target':'Abundant valid local data, simultaneous PairEx selection, and the uniform centered-prime-sum window theorem.'},
    ]
}
(BASE/'v0_8/next_source_targets.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exact_local_targets':len(targets),'global_branches':len(out['global_branches_unchanged'])}))
