#!/usr/bin/env python3
"""Build the QW ledger from immutable pinned Git blobs; no checkout mutations."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT.parents[1]/'lean-source')
REPO=ap.parse_args().repo.resolve()
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean'
AB='src/Development/AbelianVarietyTheory/'
GI=AB+'Proofs/GlobalInterpolation/'
LV='src/Formalism/LogVandermondeBounds/'
LVP=LV+'LogVandermondeProofs/'
HT='src/Formalism/GL3MeanSquares/HookFormulaTorsion/'
SN='src/Development/AutomorphicArithmetic/ShortNorms/'
GC='src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/UnimodularClassRepresentatives/'
P={
 'euler':HT+'SumWeightsOverPrimeLeHalfDegree.lean',
 'index':HT+'DimensionMassJointBound.lean',
 'mass':'src/Formalism/HermitianLattices/StatementMass.lean',
 'std':'src/Formalism/SharpRestriction/GlobalSchurBounds/StandardLattice.lean',
 'thick':'src/Formalism/SharpRestriction/GlobalSchurBounds/ThickPlacesCorollaryOfAnyTranslate.lean',
 'unitri':LVP+'CardStabilizerVector.lean',
 'vand':LVP+'VandNSuccRight.lean',
 'ratio':LVP+'LogRatioLowerBoundOfLogVandermondeGap.lean',
 'logdef':LV+'LogRatioLowerBound.lean',
 'vplace':LV+'VandPlace.lean',
 'hook':LV+'HookGammaAmgmMultinomialBounds.lean',
 'dims':GI+'DimVRowPos.lean',
 'win':GI+'WindowLower.lean',
 'host':GI+'HostBoundsTwoMulRpowLogSqLe.lean',
 'scale':GI+'ScalePolynomialQuantitiesComparison.lean',
 'rank':GI+'ExplicitRanksBasicBoundsLargeScale.lean',
 'top':GI+'GoodTopCountLeConstMulLog.lean',
 'mprod':GI+'MassRatioAllUnramifiedCmFields.lean',
 'mli':GC+'SiegelMassRatioOfLI.lean',
 'li':GC+'LiStatOf.lean',
 'pnorm':GI+'NormPrimesImagQuadShortIntervalLowerBound.lean',
 'weighted':GI+'TrivialClassShortIntervalStatement.lean',
 'lfam':GI+'ExistsLFamRayStatement.lean',
 'sndef':SN+'ShortNorm.lean',
 'level':SN+'levelPrimeN.lean',
 'dyad':SN+'normPrimesN.lean',
 'puncond':GI+'NormPrimesAndLevelPrimeUnconditional.lean',
 'zero':'src/Development/AutomorphicArithmetic/MeanSquareBounds/SmallZeros.lean',
 'noexc':'src/Development/AutomorphicArithmetic/MeanSquareBounds/PrimeSetTwoBounds.lean',
}
cache={}
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(path):
 if path not in cache:
  raw=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
  if (REPO/path).is_file():assert (REPO/path).read_bytes()==raw,('changed checkout',path)
  cache[path]=raw
 return cache[path]
PREFIX=r'^(?:@\[[^\n]*?\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
BOUND=re.compile(PREFIX+r'(?:theorem|lemma|def|abbrev|structure|instance|variable|namespace|end|open|section|set_option|attribute|include|omit)\b|^@\[[^\n]*\]')
def namespace(lines,i):
 stack=[]
 for l in lines[:i]:
  m=re.match(r'^namespace\s+(\S+)',l)
  if m:stack.append(('n',m[1]))
  elif re.match(r'^(?:noncomputable\s+)?section(?:\s|$)',l):stack.append(('s',None))
  elif re.match(r'^end(?:\s|$)',l) and stack:stack.pop()
 return '.'.join(v for k,v in stack if k=='n')
def src(key,name,role='literal endpoint or substantive supplier'):
 path=P.get(key,key);raw=blob(path);ls=raw.splitlines(keepends=True);ts=[l.decode().rstrip('\r\n')for l in ls]
 pat=re.compile(PREFIX+r'(?:theorem|lemma|def|abbrev|structure)\s+'+re.escape(name)+r'(?=\s|\{|\(|:|$)')
 hits=[i for i,l in enumerate(ts)if pat.match(l)];assert len(hits)==1,(path,name,hits)
 a=hits[0];b=a+1
 while b<len(ls)and not BOUND.match(ts[b]):b+=1
 while b>a+1 and not ts[b-1].strip():b-=1
 part=b''.join(ls[a:b]);ns=namespace(ts,a);full=((ns+'.')if ns else '')+name
 if full.startswith('_root_.'):full=full[7:]
 url=f'{URL}/blob/{PIN}/{path}#L{a+1}-L{b}'
 return dict(path=path,declaration=full,source_spelling=name,line_start=a+1,line_end=b,sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(part),range_bytes=len(part),first_line=ts[a],declaration_lines_within_range=[a+1],url=url,pinned_url=url,role=role,verified_equal_to_pinned_git_blob=True)
def ss(key,*names):return[src(key,n)for n in names]
def explicit_range(key,name,a,b,role):
 path=P[key];raw=blob(path);ls=raw.splitlines(keepends=True);part=b''.join(ls[a-1:b]);url=f'{URL}/blob/{PIN}/{path}#L{a}-L{b}'
 return dict(path=path,declaration=name,source_spelling='example',line_start=a,line_end=b,sha256=sha(raw),full_file_sha256=sha(raw),range_sha256=sha(part),range_bytes=len(part),first_line=ls[a-1].decode().rstrip('\r\n'),declaration_lines_within_range=[a],url=url,pinned_url=url,role=role,verified_equal_to_pinned_git_blob=True)

main=(ROOT/'main.tex').read_bytes();mt=main.decode();report=(ROOT/'report.txt').read_bytes()
markers=list(re.finditer(r'(?m)^\\paragraph\{(QW\d+):',mt))
assert [m[1]for m in markers]==[f'QW{i}'for i in range(1,16)]
claims=[]
def claim(i,title,statement,deps,sources,assumptions):
 a=markers[i-1].start();b=markers[i].start()if i<len(markers)else len(mt);part=mt[a:b].encode()
 claims.append(dict(id=f'QW{i}',title=title,statement=statement,status='derived_simplification',mathematical_status='proved_under_explicit_hypotheses',introduced_in='0.19',depends_on=deps,assumptions=assumptions,proof_location=dict(file='quantitative_windows/main.tex',expanded='quantitative_windows/report.txt',section=f'QW{i}',sha256=sha(part),line_start=mt[:a].count('\n')+1,line_end=mt[:b].count('\n'),bytes=len(part)),sources=sources))

claim(1,'The actual CM Euler product has absolutely summable logarithms','The unramified CM residue condition forces residue degree at least two at fixed primes. Grouping absolute logarithms over rational primes gives positivity, convergence and |log L_E(M)| <= f log zeta(M) <= f for M>=2.',[],ss('mass','fDeg','eulerFac','lValEta','IsCMUnram')+ss('euler','prod_norm_dvd_prime_pow_degree','abs_norm_eq_prime_pow','inert_prime_norm_ge_sq','euler_product_le_zeta','sum_neg_log_le_log_zeta','abs_log_inv_one_sub_le_real','euler_factor_inert_prime_bound','euler_factor_split_prime_bound','idealPrimeWeight','sum_weights_over_prime_le_half_degree','euler_factor_log_bound','partial_sums_log_euler_factor_le','log_l_value_field_bound')+ss('ratio','zetaR_nonneg_le_two','log_zetaR_le_one'),['Exact IsCMUnram; finite ideal factorization and residue-field facts; M>=2.'])
claim(2,'Count the exact column and row levels','Free-entry counting gives the literal local column/row indices, their theta factors in [1/2,1], and the two-prime f-fold ratio with factor 2^(-2f).',[],ss('unitri','cardUnitriangular')+ss('thick','card_matrices_with_free_support','IsFreePosition','isLevel_iff_free_support','card_upper_pairs_in_interval','card_free_positions','rowLevCard_holds')+ss('index','card_general_linear_group','local_index_formula','index_ratio_bound')+ss('dims','idx_place','idx_ratio'),['Finite fields of cardinality >=3; actual even m>=2 and literal level zero patterns.'])
claim(3,'Telescope the retained mass law with exact normalization','Positive finite genus masses and the stated SiegelMassRatioCM multiply to the actual mass_tel; fDeg and vInv agree with the host normalizations.',['IG9'],ss('mass','mass','vInv','massRatioRightSide')+ss('std','SiegelMassRatioCM')+ss('dims','finrank_E','fDeg_E','vInv_E','mass_pos','mass_tel')+ss('mli','siegelMassRatio_of_LI'),['SiegelMassRatioCM is explicitly retained, including its representation/local-density mass suppliers; positivity alone does not prove the mass law.'])
claim(4,'Interlacing loses only endpoint factors','The positive row Vandermonde contains all column-inner comparison factors and bottom powers. The 2k-3 endpoint factors are bounded by (8a)^(2k-3), proving the literal VandPlace bound.',[],ss('logdef','vandN','dimVN','rowPar','PlaceData')+ss('vplace','VandPlace')+ss('vand','anti_of_step','gap_of_step','vandN_pos','vandN_mul_prod_pow_le_vandN_rowPar','vandN_le_pow_mul_pow_mul_vandN_of_interlace','VandPlace_holds'),['Literal PlaceData, x>=1,k>=2,m>=1,Delta>=1; all empty-product edge cases retained.'])
claim(5,'Replace bottom endpoints by middle weights with an explicit loss','Telescoping log(w_j/b_j) and the original endpoint bounds prove place_bound with loss kL(20+(2+2C0)/eps)+2mL.',['QW4'],ss('ratio','place_bound'),['Literal PlaceData and k<=x^C0 with eps>0,C0>=0.'])
claim(6,'The literal global logarithmic ratio has an explicit constant','Exact factorial cancellation, the actual mass and index ratios and the Vandermonde bound prove LogRatioLowerBound with C=30+(2+2C0)/eps.',['QW1','QW2','QW3','QW5'],ss('logdef','LogRatioLowerBound')+ss('ratio','sum_log_factorial','log_dimVN','logRatioLowerBound_of_logVandermondeGap')+ss('hook','vandermonde_place_lower_bound'),['Exact positive masses, source telescope, Euler-log and index bounds, actual Dstar lower bound and dstar equality; v>=pi and log v<=L.'])
claim(7,'Every actual top/thick/thin place satisfies PlaceData','RF scale/rank bounds and the original HCParam/HCVal/window identities prove all nine literal PlaceData clauses, including root-of-unity rounding, and every middle weight >=1.',['RF11','RF12','RF14'],ss('dims','place_data','scale_sizes','bottom_len')+ss('win','roots_le','span_roots','places_ok')+ss('scale','_root_.GlobalTheory.scale_poly_comparison')+ss('rank','rank_basic_bounds'),['Actual ChOK on the same PreCh; nonnegative cD,ch, standard constants, and fixed eps in (0,1/52). The coordinates are supplied, not created by these estimates.'])
claim(8,'Actual host and rank constants meet the logarithmic error margins','The host root-discriminant bounds yield pi<=v and log v<=L; type primes have log g_i>=8L. The actual rank windows imply 2|C|<=m,m^2<=k,2CGam*m^4<=k uniformly.',['RF11','RF12','RF14'],ss('dims','pi_le_v')+ss('host','hostBounds_two_mul_rpow_log_sq_le','hostBounds_rd','hostBounds')+ss('win','rank_consts'),['Actual host discriminant and HostVal identities; eps,cD,ch and constants fixed before the scale threshold.'])
claim(9,'Prove the original conditional mass window','With the same PreCh and exact size identities, the literal window_lower follows from SiegelMassRatioCM. Its normalized logarithm is at least 14mL, hence mL, uniformly for all words.',['QW1','QW2','QW3','QW6','QW7','QW8'],ss('dims','seqOf','dimV_col','dimV_row','dimV_row_pos','placeNo','prod_places')+ss('win','window_lower'),['Retained SiegelMassRatioCM, literal Std/ChOK, same row coordinates at all words, original du mass-index equality and Ds lower bound. c2=0 is chosen before ch and the final threshold precedes all actual data.'])
claim(10,'Remove prime powers from the same weighted arithmetic family','Nonnegative LFam coefficients and actual NormOne support give the exact weighted sum <= 2 log Y times norm-prime count plus 2(psi-theta).',[],ss('pnorm','sum_lam_zero_le_card_normPrimes'),['Actual LFam nonnegativity and von Mangoldt bound, its same-family NormOne support; elementary Chebyshev estimate is explained.'])
claim(11,'Expose the analytic and arithmetic premises of ShortNorm','The full weighted-to-count reduction proves ShortNorm with c=min(c0,1/(2(1+A)+2+K)) and cprime=e/8, retaining the literal compatible LFam and uniform weighted short-interval suppliers.',['QW10'],ss('pnorm','sqrt_le_short_main','normPrimes_short_interval_lower')+ss('weighted','_root_.GlobalTheory.T.exists_lam_zero_sum_shortInterval_ge')+ss('lfam','_root_.GlobalTheory.T.exists_lFam_normOne_of_mod_four_eq_three')+ss('sndef','ShortNorm'),['ExistsLFamRayStatement and TrivialClassShortIntervalStatement are retained explicit inputs; original d,M,X,h hypotheses and conductor B=4dM^2.'])
claim(12,'ShortNorm gives the actual prescribed level-prime interval','Uniform comparison of logarithms proves levelPrimeN with arbitrary later endpoint Ts, V<=x^12 and actual NormOne modulus N(g0*g1)^2.',['RF11','RF12','RF14','QW11'],ss('sndef','ShortNorm','ModAt')+ss('level','levelPrimeN')+ss('puncond','normOne_pair_form','levelPrime_unconditional'),['ShortNorm retained through QW11 analytic/arithmetic suppliers; eps in (0,1/52), fixed positive cs,CY, literal ModAt and source endpoint/rank/host-prime bounds.'])
claim(13,'ShortNorm gives the literal nine-tenths dyadic count','With ModAt and log Y>=8x^eps, the same quantitative input gives norm-prime count >=Y^(9/10), uniformly for all later Y.',['RF11','QW11'],ss('sndef','ShortNorm','ModAt')+ss('dyad','core_sqrt','ev_log_sq','normPrimesN')+ss('puncond','normPrimes_unconditional'),['ShortNorm retained; fixed eps>0 and literal ModAt. No bounded endpoint is assumed.'])
claim(14,'A nonnegative entire-product contradiction proves classical nonvanishing at one','Dirichlet character Euler-product coefficients are nonnegative. A hypothetical nonprincipal zero at one would make the full product entire and zero at -2, contradicting its nonnegative Taylor expansion about a real sigma>1.',['IG2'],ss('zero','noExc_one'),['Classical Dirichlet analytic continuation, principal simple pole and trivial zero at -2, finite character orthogonality; no RH or global zero-free hypothesis. This is an alternate human proof of the classical nonvanishing imported by the pinned noExc_one.'])
claim(15,'A finite positive minimum proves exactly the real NoExc margin','Continuity and nonvanishing at one yield one positive real interval for every nonprincipal character of modulus <=N0. Taking the finite minimum proves QH.small_zeros with its N0-dependent constant.',['QW14'],ss('noexc','NoExc')+ss('zero','noExc_mono','noExc_one','noExc_level','small_zeros'),['Bounded modulus N0; no effective rate, no uniform constant over all moduli and no complex zero-free box are inferred.'])

remaining=[
 dict(interface='Actual mass ratio',scope='SiegelMassRatioCM is the retained ratio law; source HermRepUnram/LIStat and global density/representation mass identities remain. QW3 proves only the telescope and QW9 its complete conditional window consequence.'),
 dict(interface='Compatible LFam and uniform weighted interval estimate',scope='The actual LFam with B=4dM^2 and NormOne support, and its uniform weighted trivial-class interval lower bound remain. QW10-QW13 supply the full ensuing count and scale transports.'),
 dict(interface='Original geometric and global inputs',scope='ChOK/HCParam and the exact same-object du/Ds identities remain supplied. Finite NoExc is not a uniform conductor estimate, simultaneous PairEx selection, or a proof of RH/Dirichlet GRH.'),
]
targets=[]
for key,name,scope in [
 ('std','SiegelMassRatioCM','Prove the original global mass-ratio law for every unramified CM field, retaining its exact standard-lattice normalization. QW3/QW9 now prove the telescope and complete conditional quantitative window.'),
 ('mprod','massRatio_all_unramified_cmFields','Reconstruct the actual mass-law producer through the representation and local-density identities, not just the positive finite mass definition.'),
 ('mli','siegelMassRatio_of_LI','Expand the substantive HermRepUnram/LIStat suppliers and induction/density constants that produce the global mass ratio. QW9 retains this law explicitly.'),
 ('weighted','_root_.GlobalTheory.T.exists_lam_zero_sum_shortInterval_ge','Prove the uniform weighted trivial-class short-interval lower bound for every actual LFam with the original conductor and h thresholds; QW11 proves its unweighted consequence.'),
 ('lfam','_root_.GlobalTheory.T.exists_lFam_normOne_of_mod_four_eq_three','Construct the actual LFam with B=4dM^2 and the same-family NormOne prime support. QW10-QW13 retain this arithmetic supplier.'),
 ('pnorm','normPrimes_short_interval_lower','QW10-QW11 now prove the weighted-to-unweighted reduction with all constants. Its actual compatible LFam and uniform weighted interval lower bound remain; the unconditional endpoint is not discharged.'),
 ('puncond','levelPrime_unconditional','QW12 proves the entire uniform levelPrimeN scale transport from ShortNorm, including the host specialization. The actual ShortNorm analytic/arithmetic producers remain.'),
 ]:
 t=src(key,name,'retained source target');t.update(id='QW-next-'+str(len(targets)+1),priority=2,scope=scope,remaining_human_scope=scope);targets.append(t)
completed=[]
for key,name,ids,scope in [
 ('euler','log_l_value_field_bound',['QW1'],'Actual absolutely convergent Euler product and literal logarithmic bound reconstructed.'),
 ('dims','idx_place',['QW2'],'Exact finite local subgroup count and local index bounds reconstructed.'),
 ('dims','idx_ratio',['QW2'],'Actual f-fold two-prime ratio with 2^(-2f) reconstructed.'),
 ('dims','mass_tel',['QW3'],'Literal telescope proved with the original SiegelMassRatioCM hypothesis retained.'),
 ('vand','VandPlace_holds',['QW4'],'Full literal PlaceData Vandermonde comparison proved, including positivity.'),
 ('hook','vandermonde_place_lower_bound',['QW6'],'Full literal LogRatioLowerBound proved with explicit constant and its original mass/index/size hypotheses.'),
 ('win','places_ok',['QW7'],'All nine PlaceData clauses checked for the same actual ChOK; realization hypotheses retained.'),
 ('win','rank_consts',['QW8'],'Literal uniform rank-constant margins proved from the original RankVal inequalities.'),
 ('win','window_lower',['QW9'],'Full original conditional endpoint proved; SiegelMassRatioCM and same-PreCh ChOK/du/Ds hypotheses remain explicit.'),
 ('level','levelPrimeN',['QW12'],'Literal conditional source theorem proved uniformly in all post-threshold data; ShortNorm retained.'),
 ('dyad','normPrimesN',['QW13'],'Literal nine-tenths uniform count proved from ShortNorm; unconditional analytic suppliers retained.'),
 ('zero','small_zeros',['QW14','QW15'],'Classical nonvanishing and finite minimum prove the exact bounded-modulus real-zero margin; no uniform-conductor or complex assertion.'),
 ]:
 s=src(key,name);completed.append(dict(path=s['path'],declaration=s['declaration'],claims=ids,reason=scope))
files=[dict(path=p,sha256=sha(b),bytes=len(b),lines=len(b.splitlines()),commit=PIN,url=f'{URL}/blob/{PIN}/{p}',verified_equal_to_pinned_git_blob=True)for p,b in sorted(cache.items())]
artifacts={n:dict(sha256=sha((ROOT/n).read_bytes()),bytes=(ROOT/n).stat().st_size)for n in ['main.tex','report.txt','build_provenance.py']}
links=sum(len(c['sources'])for c in claims);ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256'])for c in claims for s in c['sources']}
data=dict(artifact_version='0.19',component='quantitative_windows',repository=URL,commit=PIN,scope='Actual Euler/index/Vandermonde proofs and the complete conditional quantitative mass window; exact weighted/count/prime-scale transports with analytic/arithmetic premises retained; classical nonvanishing and bounded-modulus real NoExc.',claim_count=len(claims),source_link_count=links,unique_claim_source_range_count=len(ranges),source_file_count=len(files),claims=claims,source_files=files,proof_artifacts=artifacts,retained_inputs=remaining,completed_targets=completed,independent_reviews=[],validation=dict(read_only_source_access=True,source_range_hashes_regenerated=True,lean_build_performed=False,pdf_build_performed=False),external_background_sources=[dict(url='https://dlmf.nist.gov/25.15',role='Classical Dirichlet analytic continuation, principal pole and trivial zeros; QW14 supplies its own nonvanishing proof.'),dict(url='https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LSeries/Nonvanishing.html',role='Documentation for the classical nonvanishing imported by pinned noExc_one, not a claim of checking the project with current Mathlib.')])
for filename,reviewer,nums in [('quantitative_windows_QW1_9_review.txt','/root/global_frame',range(1,10)),('quantitative_windows_QW10_15_review.txt','/root/comparison_span',range(10,16))]:
 rp=ROOT.parent/'reviews_v0_19'/filename
 if not rp.exists():continue
 raw=rp.read_bytes();content=raw.decode();chosen={c['id']:c['proof_location']['sha256']for c in claims if int(c['id'][2:])in nums}
 assert 'PASS'in content
 for cid,h in chosen.items():assert h in content,('review paragraph changed',filename,cid)
 data['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),review_record='../reviews_v0_19/'+filename,review_record_sha256=sha(raw),paragraph_sha256=chosen,lean_replay=False))
for n,obj in [('provenance.json',data),('source_manifest.json',dict(artifact_version='0.19',component='quantitative_windows',repository=URL,commit=PIN,source_files=files,proof_artifacts=artifacts)),('next_targets.json',dict(artifact_version='0.19',repository=URL,commit=PIN,targets=targets,completed_targets=completed,retained_inputs=remaining))]:
 (ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
out=['QUANTITATIVE WINDOWS QW1-QW15',f'Repository {URL}',f'Commit {PIN}',f'{len(claims)} claims, {links} source links, {len(files)} pinned files.','']
for c in claims:
 out += [c['id']+': '+c['title'],'Proof paragraph SHA256 '+c['proof_location']['sha256']]
 for s in c['sources']:out += [f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']}",'  '+s['url'],f"  File {s['full_file_sha256']}; range {s['range_sha256']}"]
 out+=['']
(ROOT/'source_locators.txt').write_text('\n'.join(out)+'\n')
(ROOT/'next_targets.txt').write_text('\n'.join(['QUANTITATIVE WINDOWS - RETAINED TARGETS','']+[f"{t['declaration']}\n{t['pinned_url']}\n{t['remaining_human_scope']}\n"for t in targets])+'\n')
print(json.dumps(dict(claims=len(claims),source_links=links,unique_ranges=len(ranges),source_files=len(files),next_targets=len(targets)),indent=2))
