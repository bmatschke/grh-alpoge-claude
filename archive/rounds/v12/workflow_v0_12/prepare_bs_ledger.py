"""Generate the standalone BS ledger builder, preserving the checked parser."""
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
old = (BASE/'v0_11/host_weight_join/build_provenance.py').read_text()
head = old.split('claims = [',1)[0]
head = head.replace('Regenerate HW pinned-source correspondence',
                    'Regenerate BS pinned-source correspondence')
start = head.index('PATHS = {')
end = head.index('PREFIX = ',start)
head = head[:start]+"""PATHS = {
 'marked':'src/Development/AutomorphicArithmetic/ThickFrames/MarkedLow.lean',
 'select':'src/Development/AutomorphicArithmetic/ThickFrames/select.lean',
 'counts':'src/Development/AutomorphicArithmetic/ThickFrames/SharesOfCounts.lean',
 'group':'src/Development/AutomorphicArithmetic/ThickFrames/topsGroup.lean',
 'orbit_terms':'src/Development/AutomorphicArithmetic/ThickFrames/orbitTerms.lean',
 'orbit_sum':'src/Development/AutomorphicArithmetic/ThickFrames/orbitSum.lean',
 'good':GB+'UnramifiedQuadraticSetting.lean',
 'shares':SR+'RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean',
 'mertens':GB+'JointsLit.lean',
 'bad':GB+'SmallOrderPrimes.lean',
}
"""+head[end:]

claims = r'''
claims = [
 {'id':'BS1',
  'title':'Finite Bernoulli moments and one variance budget for all classes',
  'status':'proved_by_finite_product_expansion',
  'statement':'For independent inclusion probabilities 0<=p_a<=delta<=1 and any finite classification, the sum of centered class-count variances is sum p_a(1-p_a)<=delta*|A|, without a class-count multiplier.',
  'depends_on':[],
  'assumptions':['Finite underlying set and finite class set; the classification and inclusion probabilities are fixed before selection.'],
  'sources':refs('marked','pw ind')+refs('select','sel_moment sel_moment\''),
  'new_human_argument':'Expand finite products and second moments directly, then sum variances over the disjoint class fibres.'},
 {'id':'BS2',
  'title':'One set simultaneously controls all class counts and weighted bad mass',
  'status':'proved_finite_selection_including_zero_expectation_case',
  'statement':'Under the pointwise joint selected-and-bad bound beta*delta and D²>=2delta|A|, there is a positive-probability T with every count error<=D and weighted bad mass<=4beta*delta|A|sum omega.',
  'depends_on':['BS1'],
  'assumptions':['D>0, beta>=0, nonnegative finite weights, and the explicitly stated joint-event bound; badness predicates may depend on the whole subset and need not be independent.'],
  'sources':refs('select','sel_exists sel_ncard UpperTheory.BernoulliSumsFrobeniusOrbits.select'),
  'new_human_argument':'For positive M average sum Y²/D²+B/(4M), whose mean is <=3/4. Handle M=0 by vanishing of B on the positive-probability support.'},
 {'id':'BS3',
  'title':'Biased coset count concentration gives exact normalized shares',
  'status':'proved_direct_coset_normalization_with_stronger_size_bounds',
  'statement':'Counts within D of delta*n0 on A0 and 3delta*n0/4 on other cosets, with 4oD<=eta*delta*n0 and eta<=1, imply 3delta*N/4<=|T|<=5delta*N/4 and every relative share error<=eta.',
  'depends_on':[],
  'assumptions':['Finite abelian group A, subgroup A0 of index o, delta>0, D>=0; the scale inequality forces eta>=0.'],
  'sources':refs('group','tg_class_sum')+refs('counts','UpperTheory.BernoulliSumsFrobeniusOrbits.shares_of_counts')+
     refs('shares','lam Shares'),
  'new_human_argument':'Sum once over distinct cosets, then subtract lambda times the total. This shortens the source sum over all representatives and improves the unused size constants.'},
 {'id':'BS4',
  'title':'Explicit scale threshold for the biased shares tolerance',
  'status':'proved_explicit_power_comparison',
  'statement':'With delta=x^(-eps/8), |A|>=x^(2+8eps)/2, o<=Co and x^eps>=64Co^4, D=sqrt(2delta|A|) satisfies 4oD<=x^-1*delta|A0|. Thus the shares tolerance is actually x^-1.',
  'depends_on':['BS3'],
  'assumptions':['eps>0, x>=1 and the stated finite-group size/index bounds. Cases Co<1 are vacuous.'],
  'sources':refs('group','tg_num')+refs('marked','hE dE')+
      refs('orbit_terms','UpperTheory.BernoulliSumsFrobeniusOrbits.orbit_terms','probability_threshold_to_be_joined'),
  'new_human_argument':'The explicit inequality delta*N>=32o^4 x² gives the square-root error condition by squaring positive quantities.'},
 {'id':'BS5',
  'title':'Complete biased topsGroup selection with exact quantifier order',
  'status':'proved_by_BO5_and_explicit_finite_selection',
  'statement':'For fixed eps,Co,Lb and sufficiently large x, every supplied admissible finite group/subgroup, point-dependent selector, finite step list of large order and nonnegative weights admit one T with the literal size, Shares and 4Cb*x^-2*delta|A|*sum omega bad-mass conclusions.',
  'depends_on':['BO5','BS2','BS3','BS4'],
  'assumptions':['The explicitly stated input group, subgroup, order, L2 and selector conditions; those inputs are supplied by the separate arithmetic construction.'],
  'sources':refs('group','UpperTheory.BernoulliSumsFrobeniusOrbits.topsGroup')+
      refs('select','UpperTheory.BernoulliSumsFrobeniusOrbits.select')+
      refs('orbit_sum','UpperTheory.BernoulliSumsFrobeniusOrbits.orbit_sum')+
      refs('good','goodU goodEll orbitSmallMultiplicity goodG\' orbitWindowCount IsGoodOrbit')+
      refs('shares','lam Shares'),
  'new_human_argument':'Apply the pointwise BO5 joint-event estimate to BS2 and normalize the same set. The selector may depend on the point; no parity rotation invariance or identical bad event along an orbit is assumed.',
  'remaining_inputs':['Construction of the actual arithmetic frame, steps and host, followed by the other global proof branches.']},
 {'id':'BS6',
  'title':'The same set satisfies the prime-weighted badness allowance',
  'status':'proved_elementary_factorial_prime_sum_and_exact_constants',
  'statement':'For candidate primes below exp(x^(eps/3)), the selected set has weighted bad mass <=16Cb|T|x^(-2+eps/3)<=|T|x^(-2+eps) once x^(2eps/3)>=16Cb.',
  'depends_on':['BS5'],
  'assumptions':['Finite candidate set of primes below the displayed bound; the same selected T from BS5.'],
  'sources':refs('mertens','mertens_bound mertens_bound_family','source_prime_sum_interface_proved_here_by_factorials')+
      refs('bad','BTT adm2','downstream_allowance_identification_is_separate')+
      refs('group','UpperTheory.BernoulliSumsFrobeniusOrbits.topsGroup'),
  'new_human_argument':'Factor n! and use floor(n/p)>=n/(2p) to obtain sum(log p)/p<=2log z. Combine with delta*N<=2|T| and increase one fixed threshold.'},
 {'id':'BS7',
  'title':'Fourier meaning of the 4-to-3 bias and the ordinary-RH specialization',
  'status':'proved_derived_finite_Fourier_explanation',
  'statement':'On A/A0 the target law is 3o/(3o+1) times uniform plus 1/(3o+1) at zero. Its Fourier averages are 1 for the trivial character and 1/(3o+1) for each nontrivial character; empirical Shares error eta gives character error <=o*eta. At o=1 Shares is automatic and selection is uniform.',
  'depends_on':['BS3','BS5'],
  'assumptions':['Finite quotient; for empirical normalization |T|>0, supplied by BS5. Matching to the actual cyclic character level uses its separately supplied host identification.'],
  'sources':refs('shares','lam Shares wt Gm Level.ofSub Level.cyc'),
  'new_human_argument':'Translation proves finite character orthogonality, and the triangle inequality sums the coset errors. This explains source weights without claiming an explicit formula or arithmetic host construction.',
  'remaining_inputs':['Actual quotient/character identification, Euler-factor treatment and arithmetic explicit-formula estimates remain their own proof components.']},
]
'''

tail = r'''
for claim in claims:
    claim['proof_location']={'file':'balanced_tops/main.tex',
                            'expanded':'balanced_tops/report.txt',
                            'section':claim['id']}
    claim.setdefault('remaining_inputs',[])
records=[source for claim in claims for source in claim['sources']]
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw=(REPO/s['path']).read_bytes().splitlines(keepends=True)
    part=b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest()==s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n')==s['first_line']
ledger={
 'component':'balanced_tops','artifact_version':'0.12','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
 'claims':claims,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'scope':'Complete finite biased selection from BO5; input arithmetic group/host construction and the remaining global RH/Dirichlet-GRH branches are separate.',
 'artifact_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in ['main.tex','report.txt','build_provenance.py']},
 'validation':{'lean_sources_modified':False,'full_lean_build_or_kernel_replay':False,
  'all_files_equal_pinned_git_blobs':True,'all_declarations_anchored':True,
  'all_range_hashes_rechecked':True,'source_records':len(records),'unique_ranges':len(unique)}
}
(HERE/'provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_locators.txt').write_text('\n'.join(
    f"{claim['id']} | {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['range_sha256']}"
    for claim in claims for s in claim['sources'])+'\n')
print(json.dumps({'claims':len(claims),'source_records':len(records),
                 'unique_ranges':len(unique),'files':len(files),
                 'all_files_equal_pinned_git_blobs':True}))
'''
out = BASE/'v0_12/balanced_tops/build_provenance.py'
out.write_text(head+claims+tail)
print(out)
