"""Regenerate BO pinned-source correspondence; no Lean execution or edits."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'alpoge-rh'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
SR = 'src/Formalism/SharpRestriction/'
GB = SR+'GrowthBounds/'
LC = 'src/Formalism/LocalRingCardinality/'
GI = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
TF = 'src/Development/AutomorphicArithmetic/ThickFrames/'
SC = 'src/Formalism/SubspaceCounting/'
PATHS = {
 'defs':TF+'MarkedLow.lean',
 'expect':TF+'expectationSpec.lean',
 'tail':TF+'TailLe.lean',
 'mark':TF+'MarkedGe.lean',
 'mark_bounds':TF+'MarkedLowBounds.lean',
 'tiles':TF+'TilesLe.lean',
 'not_good':TF+'NotGoodLe.lean',
 'terms':TF+'orbitTerms.lean',
 'orbit':TF+'orbitSum.lean',
 'good':SC+'GoodOrbitIntervalTileCondition.lean',
 'windows':SC+'StatementB.lean',
 'params':GB+'UnramifiedQuadraticSetting.lean',
 'uniform':GI+'ChoiceOfTops.lean',
 'select':TF+'select.lean',
 'tops':TF+'topsGroup.lean',
}
PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance)\s+(\S+)')
BOUND = re.compile(r'^'+PREFIX+r'(?:def|abbrev|theorem|lemma|structure|class|instance|namespace|section|end|variable|open|include|omit|attribute|set_option)\b')
files = {}
for key, path in PATHS.items():
    raw = (REPO/path).read_bytes()
    assert raw == subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}']), ('unpinned bytes',path)
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, raw_line in enumerate(lines):
        line = raw_line.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)',line):
            stack.append(('namespace',m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$',line):
            stack.append(('section',m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$',line):
            assert stack, (path,i+1,'end without opening')
            kind,label = stack.pop()
            assert not m[1] or m[1] == label, (path,i+1,label,m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind,label in stack if kind == 'namespace')
            declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
    assert all(kind == 'section' and label is None for kind,label in stack), (path,'unclosed namespace')
    files[key] = {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                  'lines':len(lines),'verified_equal_to_pinned_git_blob':True,
                  '_lines':lines,'_decls':declarations}

def refs(key, names, role='exact_source_interface_or_parallel_proof'):
    f = files[key]
    out = []
    for name in names.split():
        hits = [d for d in f['_decls'] if d[0] == name or d[2] == name]
        assert len(hits) == 1, (key,name,hits)
        spelling,start,qualified = hits[0]
        end = start+1
        while end < f['lines'] and not BOUND.match(f['_lines'][end].decode()):
            end += 1
        while end > start+1 and not f['_lines'][end-1].strip():
            end -= 1
        selected = b''.join(f['_lines'][start:end])
        out.append({'path':f['path'],'declaration':qualified,'source_spelling':spelling,
                    'line_start':start+1,'line_end':end,'full_file_sha256':f['sha256'],
                    'range_sha256':hashlib.sha256(selected).hexdigest(),'range_bytes':len(selected),
                    'first_line':f['_lines'][start].decode().rstrip('\r\n'),
                    'role':role,'url':f'{URL}/blob/{PIN}/{f["path"]}#L{start+1}-L{end}'})
    return out

claims = [
 {'id':'BO1',
  'title':'Finite nonconstant product laws and monotone count-tail bounds',
  'status':'proved_human_finite_product_expansion_and_explicit_coupling',
  'statement':'Expand the actual independent nonconstant product weights to prove normalization, linearity, marginalization, disjoint-event factorization and the exact selected-coordinate identity. A finite three-state coupling and selected-subset union bound give both literal tail_le bounds for arbitrary q_i in [0,delta].',
  'depends_on':[],
  'assumptions':['Finite coordinate set and 0<=q_i<=delta<=1 for the probabilistic inequalities.',
                 'Conditioning is identified with the forced-coordinate law only when its selected-coordinate probability is positive; the underlying identity holds even when that probability is zero.'],
  'sources':refs('defs','pw exP ind')+
   refs('expect','ex_empty ex_insert ex_congr ex_const ex_add ex_mul_left ex_sum ex_mono ex_union ex_split ex_restrict ex_prod UpperTheory.BernoulliSumsFrobeniusOrbits.expectation_spec')+
   refs('tail','UpperTheory.BernoulliSumsFrobeniusOrbits.bernoulliExpectation_le_of_monotone UpperTheory.BernoulliSumsFrobeniusOrbits.tail_le')+
   refs('uniform','ex_contains tail_le_choose tail_eq tail_le_binUpper')+
   refs('orbit','bernoulliExpectation_mem_and'),
  'new_human_argument':'Finite states (0,0),(0,1),(1,1) with probabilities 1-delta,delta-q_i,q_i prove the exact domination without measure-theoretic machinery. No monotonicity is asserted for the entire bad-orbit event.'},
 {'id':'BO2',
  'title':'Biased marked cells and the unchanged marked-tile constant',
  'status':'proved_human_actual_markedLow_and_numeric_lower_bound',
  'statement':'For probabilities in [3delta/4,delta], a length-u empty cell has probability at least (1-delta)^u and a singleton-even cell at least floor(u/2)*(3delta/4)*(1-delta)^(u-1). Disjoint cells yield literal markedLow. For u=ceil(1/delta), 0<delta<=1/100, prove the factors >=3/10 and >=891/8000>1/10, hence 10^(-(6r+1))<=markedLow<=1.',
  'depends_on':['BO1'],
  'assumptions':['Natural r>=0, u>=1 and the literal one-based cell-number/absolute-coordinate parity convention.',
                 'General finite lower bound needs 0<=delta<=1; the uniform numeric constant uses 0<delta<=1/100 and u=ceil_Nat(1/delta).'],
  'sources':refs('defs','markedLow')+
   refs('good','cell Marked')+
   refs('mark','pow_le_prod one_sub_pow_le_bernoulliExpectation_empty le_bernoulliExpectation_singleton_even UpperTheory.BernoulliSumsFrobeniusOrbits.marked_ge')+
   refs('mark_bounds','UpperTheory.BernoulliSumsFrobeniusOrbits.markedLow_bounds')+
   refs('uniform','tile cell_subset cell_card ico_disjoint tile_disjoint prod_alternate')+
   refs('params','goodU'),
  'new_human_argument':'Give direct product/singleton probabilities for the nonmonotone marker event and verify the numerical exponential comparison by its power series. All source tile counts and constants are preserved.'},
 {'id':'BO3',
  'title':'Exact forced-point three-term bad-orbit estimate',
  'status':'proved_human_literal_not_good_le_with_remainder_and_parity',
  'statement':'Under (M+1)*(6r+1)*u<=n, forcing one coordinate gives bad-orbit probability at most n*choose(L2,K)*delta^K+n*(1-markedLow)^M+n*binUpper(G,delta,N-1). Cyclic complete-tile indices are distinct; remove at most one affected tile, leaving M independent tiles. The incomplete remainder and natural subtraction N-1 are treated explicitly.',
  'depends_on':['BO1','BO2'],
  'assumptions':['Natural n,L2,K,r,u,M,G,N,i0, u>=1, (M+1)*(6r+1)*u<=n, and probabilities in [3delta/4,delta] with 0<=delta<=1.',
                 'For the conditional-probability interpretation also i0<n and q_i0>0; the finite forced-law inequality does not divide by q_i0.'],
  'sources':refs('windows','window CondA')+
   refs('good','cell Marked CondTiles CondIntervals GoodOrbitIntervalTileCondition binUpper')+
   refs('tiles','bernoulliExpectation_one_sub UpperTheory.BernoulliSumsFrobeniusOrbits.tiles_le')+
   refs('not_good','ngl_windows_le UpperTheory.BernoulliSumsFrobeniusOrbits.not_good_le')+
   refs('uniform','tile_disjoint marked_congr'),
  'new_human_argument':'Separate the three failure events under the actual forced-coordinate law. Keep the incomplete cyclic remainder and absolute parity; no rotation-invariance premise is inserted.'},
 {'id':'BO4',
  'title':'Explicit uniform orbit_terms constants and threshold',
  'status':'proved_human_all_source_ceiling_and_tail_estimates_with_explicit_threshold',
  'statement':'For fixed eps>0 and real Co,Lb, use the actual KE,rE,dE,goodU,M,G,N. With theta=eps/8, h=2+8eps, pi0=10^(-(6r+1)), C1=(h+3)/pi0+2 and Cstar=2*(6r+1)*C1, take x0=exp(max(1,4*Cstar/theta^2,log(100)/theta)). Prove the tile-fit inequality and the entire source orbit_terms sum <=Cb*x^-2, where Cb=(|Co|+1)*((max(Lb,1))^K+2. Thus conditional bad probability is uniformly <=Cb*x^-2.',
  'depends_on':['BO1','BO2','BO3'],
  'assumptions':['x>=x0, natural n,L2 with x^(eps/4)<=n<=Co*x^(2+8eps) and L2<=Lb.',
                 'All constant choices precede x,n,L2, the probability profile, orbit base and forced coordinate. Impossible upper/lower ranges are vacuous.'],
  'sources':refs('defs','hE KE rE dE')+
   refs('params',"goodU goodEll orbitSmallMultiplicity goodG' orbitWindowCount IsGoodOrbit")+
   refs('good','binUpper')+
   refs('terms','ot_binUpper_le ot_exists_log_le_rpow UpperTheory.BernoulliSumsFrobeniusOrbits.orbit_terms'),
  'new_human_argument':'Replace the asymptotic log/power wrapper by the quadratic exponential-series term, obtaining an explicit threshold. Bound the full binomial tail by a selected-subset union bound and b!>=(b/e)^b; preserve the exact source Cb and parameter ceilings.',
  'scope_precision':'This proves (M+1)*ell<=n, the premise actually used here. It does not silently replace the separate local-geometric 3G<=n bound.'},
 {'id':'BO5',
  'title':'Literal ambient orbit identity and weighted selected-and-bad expectation',
  'status':'proved_human_actual_orbit_sum_and_pointwise_selection_input',
  'statement':'For a finite abelian group, an arbitrary step/base and a point in that based orbit, the injective order-n parametrization and finite marginalization give exactly P(point selected and based orbit bad)=q(point)*P_forced(bad). Applying BO4 gives <=delta*Cb*x^-2. Finite weighted summation yields E sum_p omega_p*bad_selected_count_p<=delta*|A|*Cb*x^-2*sum_p omega_p, with the t-dependent source selector allowed.',
  'depends_on':['BO1','BO3','BO4'],
  'assumptions':['Independent ambient probabilities q in [3delta/4,delta], x>=BO4 threshold, and every used step order in the BO4 interval.',
                 'For each step and point, the prescribed base b satisfies point=b+j*step for some natural j; b may depend on both inputs.',
                 'Finite step index set and nonnegative weights. No independence of the different bad-orbit events and no rotation invariance are assumed.'],
  'sources':refs('orbit','fibre_sum marginal fin_sum_eq bernoulliExpectation_mem_and UpperTheory.BernoulliSumsFrobeniusOrbits.orbit_sum')+
   refs('defs','pw exP ind')+
   refs('params','IsGoodOrbit')+
   refs('select','UpperTheory.BernoulliSumsFrobeniusOrbits.select','downstream_pointwise_probability_interface_only')+
   refs('tops','UpperTheory.BernoulliSumsFrobeniusOrbits.topsGroup','downstream_actual_selector_application_not_full_selection_claim'),
  'new_human_argument':'Expand the orbit fibre sum to exhibit the exact selected-point factor q(point), then sum pointwise bounds. This explicitly accommodates the parity-sensitive t-dependent base used by the actual source.',
  'separate_remaining_work':['The simultaneous coset-concentration/selection step is the separate BS component.',
                             'Identifying the selected data with an arithmetic host and its later point/local/global construction is outside BO.']},
]

for claim in claims:
    claim['proof_location']={'file':'biased_orbits/main.tex',
                             'expanded':'biased_orbits/report.txt',
                             'section':claim['id']}
    claim['remaining_inputs']=[]
    claim.setdefault('separate_remaining_work',[])

records=[source for claim in claims for source in claim['sources']]
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw=(REPO/s['path']).read_bytes().splitlines(keepends=True)
    part=b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest()==s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n')==s['first_line']
    assert len(part)==s['range_bytes']

ledger={
 'component':'biased_orbits','artifact_version':'0.12','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
 'claims':claims,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'scope':'Complete finite nonconstant Bernoulli orbit estimate and actual pointwise/weighted marginal identity under the stated hypotheses. No top-set selection or arithmetic-host/global-proof claim.',
 'related_prior_claims':['GII9','GII10'],
 'review_scope':{'status':'Passed independent root review of BO1-BO5. BO2-BO4 were checked against GoodOrbitIntervalTileCondition, NotGoodLe and orbit_terms, including parity, 891/8000, forced remainder, natural N-1, explicit threshold and full binomial-tail bound; BO1/BO5 finite marginals were also reviewed.',
                 'scope':'Human mathematical reconstruction and exact source correspondence; no full Lean build or kernel replay.'},
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

