#!/usr/bin/env python3
"""Build the QR ledger from immutable pinned Git blobs; no checkout mutations."""
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
 'lfam':GI+'ExistsLFamRay.lean',
 'lfams':GI+'ExistsLFamRayStatement.lean',
 'rayform':GI+'RayClassIdealCountEqNcardShiftedBinaryForm.lean',
 'basis':GI+'PlaneLatticeShortBasisOfBoundPowTwo.lean',
 'qcount':GI+'QFormCount.lean',
 'gauss':GI+'SummableExpNegMulSq.lean',
 'theta':GI+'ThetaQForm.lean',
 'raytheta':GI+'RayCountThetaFibreCount.lean',
 'finite':GI+'FiniteIdealsIn.lean',
 'lam':GI+'SumLamIdealLe.lean',
 'conv':GI+'ConvRealChar.lean',
 'classbound':GI+'ClassNumberLeAbsDiscrOfFinrankEqTwo.lean',
 'cont':GI+'RayClassLFunctionFamilyContinuationGrowth.lean',
 'log':GI+'RayClassFamilyLogDerivReGtOne.lean',
 'exp':GI+'ExpSumBounds.lean',
 'f1':GI+'NormRayClassFamilyFOneGeOfRealCharacter.lean',
 'gap':GI+'ExistsRayClassLFunctionRealZeroFarFromOne.lean',
 'blaschke':GI+'NormOneSubConjMul.lean',
 'local':GI+'RayClassLFunctionLogDerivLocalFormula.lean',
 'pos':GI+'RayClassLFunctionFamilyLogDerivPositivity.lean',
 'zfr':GI+'RayClassLFunctionZeroFreeRegion.lean',
 'unique':GI+'RayClassLFunctionUniqueSimpleExceptionalZero.lean',
 'half':GI+'LogDerivSubExceptionalLe.lean',
 'perron':GI+'TruncatedPerronPsi.lean',
 'kernel':GI+'TruncatedPerronKernel.lean',
 'percoef':GI+'TruncatedPerronOfLeTwoVonMangoldt.lean',
 'psi':GI+'RayClassFamilyPsiWithExceptionalZero.lean',
 'short':GI+'TrivialClassShortInterval.lean',
 'weighted':GI+'TrivialClassShortIntervalStatement.lean',
 'pnorm':GI+'NormPrimesImagQuadShortIntervalLowerBound.lean',
 'puncond':GI+'NormPrimesAndLevelPrimeUnconditional.lean',
 'def':AB+'Definitions/GlobalTwisting/LamIdealOfNotPrimePow.lean',
 'sndef':SN+'ShortNorm.lean',
 'level':SN+'levelPrimeN.lean',
 'dyad':SN+'normPrimesN.lean',
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

main=(ROOT/'main.tex').read_bytes(); mt=main.decode(); report=(ROOT/'report.txt').read_bytes()
markers=list(re.finditer(r'(?m)^\\paragraph\{(QR\d+):',mt))
assert [m[1] for m in markers]==[f'QR{i}' for i in range(1,26)]
claims=[]
def claim(i,title,statement,deps,sources,assumptions):
 a=markers[i-1].start();b=markers[i].start()if i<len(markers)else len(mt);part=mt[a:b].encode()
 claims.append(dict(id=f'QR{i}',title=title,statement=statement,status='derived_simplification',mathematical_status='proved_under_explicit_hypotheses',introduced_in='0.20',depends_on=deps,assumptions=assumptions,proof_location=dict(file='ray_prime_estimates/main.tex',expanded='ray_prime_estimates/report.txt',section=f'QR{i}',sha256=sha(part),line_start=mt[:a].count('\n')+1,line_end=mt[:b].count('\n'),bytes=len(part)),sources=sources))

claim(1,'The actual ray coset has no residual unit multiplicity','For the specified imaginary quadratic field and M>=3, units congruent to one are trivial. The IG1 ray-coset bijection therefore counts actual ideals with the exact norm and covolume.',['IG1'],ss('rayform','unit_eq_one','exists_equiv','aRay_eq_ncard_qForm')+ss('def','idealsIn','aRay'),['d prime, d=3 mod4, d>=100, M>=3; actual imaginary quadratic integer ring and IG1 ray-coset construction.'])
claim(2,'A reduced lattice basis gives the exact shifted binary form','A shortest primitive vector and a reduced second vector give a,b>=1, ab=dM^4/4, and a positive integral norm form whose fibers are the original ray ideal counts.',['QR1'],ss('basis','plane_lattice_reduction_step','plane_lattice_short_basis_of_bound_pow_two','plane_lattice_short_basis')+ss('rayform','exists_qForm','comb_injective','range_comb','exists_basis_im','aRay_eq_ncard_qForm'),['Same field, modulus, class, integral ideal and ray coset as QR1.'])
claim(3,'Uniform shifted ellipse count','Integer row counting and a layer-cake proof of the shifted unimodal sum/integral error give |count-pi*x/sqrt(ab)|<=10 sqrt(x) uniformly in the shifts and shear.',['QR2'],ss('qcount','unimodal_sum_integral','integral_ellipse_width','row_count','qForm_count'),['a,b>=1 and x>=1; exact shifted positive form of QR2.'])
claim(4,'Uniform shifted Gaussian estimate','Periodization and the Gaussian Fourier transform prove the absolutely convergent Poisson identity and |sum exp(-s(m+theta)^2)-sqrt(pi/s)|<=sqrt(pi/s)*s^2 for all s>0.',[],ss('gauss','exp_neg_le','summable_exp_neg_mul_sq','summable_shifted','poisson','shifted_theta_bound'),['s>0; elementary Gaussian integral and Fourier inversion for its absolutely convergent periodization, also used in IG1.'])
claim(5,'Both literal ray count and theta laws','The exact norm-fiber partition, QR3 and two applications of QR4 prove count error 10 sqrt(x) and theta error B^10*t with B=4dM^2 and kappa=2pi/(sqrt(d)M^2).',['QR1','QR2','QR3','QR4'],ss('theta','tsum_prod_weight_approx','theta_qForm')+ss('raytheta','rayCountTheta_fibre_count','rayCountTheta_fibre_tsum','rayCountTheta'),['Same actual ray family; x>=1 and 0<t<=1. Nonnegative fibers justify Tonelli.'])
claim(6,'Ideal factorization proves the actual coefficient convolution','The finite ideal-divisor identity sum_{J|I}lambda(J)=log N(I) and the actual product bijection prove every coefficient of LFam.conv, including norm zero and one.',['QR1'],ss('def','lamIdeal','lamRay','lamIdeal_prime_pow','lamIdeal_unit')+ss('finite','lamIdeal_pow','finite_dvd','sum_lamIdeal','finite_idealsIn','aRay_mul_log'),['Unique factorization of nonzero ideals in the actual degree-two integer ring; finite norm fibers.'])
claim(7,'The total weight bound keeps exact NormOne support','Residue degrees give sum_g lambda_g(n)<=2Lambda(n), including ramification. A prime supported in the identity ray class has 4p=A^2+dD^2, M|D and 2M|(A-D-2), exactly NormOne.',['QR1','QR6'],ss('lam','sum_lamIdeal_le','exists_gen','normOne_span','lamRay_props'),['Same ray group, integral coefficients and quadratic basis; p prime for the NormOne implication.'])
claim(8,'Real-character positivity and square domination','Factoring the ideal divisor sum into geometric sums gives nonnegative Dirichlet convolution coefficients; injective ideal squaring gives c_chi(n^2)>=sum_g a_g(n).',['QR1'],ss('conv','r','r_step','r_pow','geom_bounds','r_bounds','conv_eq','chi','sum_aRay','chi_mul','conv_aRay','conv_real_char'),['Real finite ray character chi^2=1; all ideals in the counts are prime to the actual modulus.'])
claim(9,'Construct every field of the arithmetic LFam','All fourteen LFam laws hold with B=4dM^2, kappa=2pi/(sqrt(d)M^2), the actual finite additive ray group and actual ideal coefficients; the same construction supplies NormOne support.',['TL14','QR5','QR6','QR7','QR8'],ss('def','LFam')+ss('lfam','aRay_norm_zero','aRay_one_norm_one','aRay_norm_one_of_ne','card_ray_le','addChar_eq_one_or_neg_one','exists_lFam_ray')+ss('classbound','_root_.GlobalTheory.classNumber_le_abs_discr_of_finrank_eq_two','_root_.GlobalTheory.classNumber_le_four_mul_abs_discr')+ss('lfams','_root_.GlobalTheory.T.exists_lFam_normOne_of_mod_four_eq_three'),['d prime, d=3 mod4, d>=100, M>=3; Explicit two-dimensional short-vector constant 2sqrt(d), proved in QR9 using the TL14 averaging principle.'])
claim(10,'Continue the actual regularized family from its remainder','Character orthogonality and the count remainder give a holomorphic Mellin integral on Re(s)>1/2, the literal F_chi, conjugation for real characters, and |F_chi(s)|<=300B(|s|+1)^2 on Re(s)>=11/20.',[],ss('def','aChi','res','mel','F')+ss('cont','norm_rem_le','differentiableAt_mel','norm_mel_le','sum_norm_isBigO','LSeries_eq','norm_res_le','mel_conj','continuation_growth'),['Any literal LFam. Dominated integration and finite character orthogonality.'])
claim(11,'Derive right-half-plane nonvanishing and logarithmic derivative','The character transform of LFam.conv yields Lprime=-G*L; comparison with exp(sum lambda_chi(n)n^-s/log n) and the real-infinity limit prove nonvanishing, the corrected logarithmic derivative, and |L|>=((sigma-1)/sigma)^2.',['QR10'],ss('def','lamChi')+ss('log','hasDerivAt_of_conv','eq_exp_of_conv','norm_ge_of_conv','norm_lamChi_le','aChi_one','conv_chi','logDeriv_F'),['Any literal LFam, Re(s)>1; absolute Dirichlet convergence and elementary zeta Euler expansion only in that region.'])
claim(12,'Heat bounds and the correct integral at one','The theta field gives O(B^11 min(t,1/t)); exponential large-t bounds prove nonprincipal integrability. Abel summation and cumulative-remainder Fubini prove integral Theta_chi=F_chi(1) without absolute series convergence at one.',['QR10'],ss('exp','tsum_exp_eq_integral','integral_integral_exp_kernel','LFam.a_le_mul','LFam.norm_aChi_le','LFam.norm_theta_large','LFam.norm_theta_small','LFam.integral_theta','LFam.exp_sum_bounds'),['Any literal LFam; chi nonprincipal for the integral identity.'])
claim(13,'Positive Bessel convolution gives the B^-45 lower bound','The real-character convolution positivity and W(y)<=12 y^-3 justify the Bessel integral identity. Choosing sqrt(v)=delta B^-22 gives |F_chi(1)|>=c_* B^-45 for every real character, with absolute c_*>0.',['QR10','QR12'],ss('f1','kerW','besW','kerW_le','integrableOn_kerW','besW_one_le','besW_one_pos','hasSum_pairs','besW_le_integral','wt','integrableOn_wt','integral_le','bRe_one','norm_F_one_ge'),['Any literal LFam and chi^2=1; positivity of LFam.sq, unit coefficient at one, all integral exchanges explicitly dominated.'])
claim(14,'Cauchy gives the B^-46 real-zero gap','The local growth bound gives |Fprime|<=18000B on |z-1|<=1/4. For a real zero beta>=3/4 of a real character, 1-beta>=c_9 B^-46 with fixed c_9>0.',['QR10','QR11','QR13'],ss('gap','LFam.norm_deriv_F_le_near_one','LFam.real_zero_far_from_one'),['Any literal LFam, chi^2=1, beta real>=3/4 and F_chi(beta)=0.'])
claim(15,'Prove the finite local zero/log-derivative estimate','Divide by a finite Blaschke product, use the maximum principle and Poisson derivative bound for a positive real part, and recover both zero multiplicity count and logarithmic-derivative remainder on a smaller disk.',[],ss('blaschke','exists_factor_one','exists_factor','norm_logDeriv_le','norm_le_of_sphere','norm_one_sub_conj_mul','main'),['Holomorphy near the closed unit disk, f(0) nonzero, |f|<=M, fixed 0<r<R<1; elementary complex analysis.'])
claim(16,'Use the actual disks with uniform family constants','The center 5/4+it has |F|>=1/100, the outer radius7/10 has the growth bound, and radii3/5 and1/2 give O(ell(t)) multiplicity and local remainder. Selected zero terms have the required nonnegative real parts.',['QR10','QR11','QR15'],ss('local','analyticOrderNatAt_comp_affine','logDeriv_local')+ss('zfr','re_one_div','re_le_one','re_LSeries_le','ell_zero_le','ell_two_le'),['Any literal LFam; exact source disks; the real-part inequality is evaluated at 1<a+1<=3/2.'])
claim(17,'Prove the family zero-free region with its two numerical cases','The nonnegative 3+4cos+cos2 polynomial and the two-/four-character analogues, together with the small-height conjugate-pair case, exclude every near-one zero except a real zero of a real character.',['QR11','QR16'],ss('pos','hasSum_re','w_nonneg','pm_one','trig','positivity')+ss('zfr','pole_le','inv_le_ell','zero_free_region'),['Any literal LFam; constants are chosen before the family. Region c_zf=1/(4*300*C+400) is one allowed choice.'])
claim(18,'There is one simple exception across the entire family','Two or four real-character positivity inequalities allow at most one principal pole. Two near-one zero occurrences, counting multiplicity, contradict the local upper bound; hence uniqueness and simplicity hold family-wide.',['QR16','QR17'],ss('unique','order_ne_top','le_order','exists_bound','main'),['Any literal LFam, real characters and their real zeros>=3/4; fixed width1/(100(C+1)).'])
claim(19,'Remove the exception in the half-width strip','For the exact ExcZ record, every nonexceptional zero in the local disk is separated by c0/(4ell(t)); count times inverse separation gives O(ell(t)^2), with exact simple-zero cancellation and a bounded outside-disk correction.',['QR11','QR16'],ss('def','ExcZ')+ss('half','ell_le','order_eq_one','exists_bound_LSeries','logDeriv_sub_exceptional_le'),['Any literal LFam, fixed0<c0<=1/20 and literal ExcZ; s in the prescribed half-width strip and not an exceptional zero.'])
claim(20,'Truncated Perron includes the actual floor endpoint','The truncated kernel estimates, absolute coefficient interchange and near/far integer summation prove error P(u log^2u/T+log u), for every coefficient sequence bounded by2Lambda and2<=T<=u.',[],ss('kernel','vinv','far_neg','far_pos','near','truncated_perron_kernel')+ss('perron','kernel_bound','interchange','harm','far_term','near_term')+ss('percoef','truncated_perron_of_le_two_vonMangoldt'),['|b(n)|<=2Lambda(n),2<=T<=u; residue theorem and absolutely convergent series on a=1+1/log u. The integer full endpoint error is retained.'])
claim(21,'Track all residues in the literal exceptional-zero contour','Choose one of1-2tau and1-4tau at distance>=tau from the exception. The corrected log derivative bounds the rectangle; principal residue+1, exceptional residue-1, and a possible omitted-left correction give the full source contour error.',['QR11','QR19'],ss('psi','shift','norm_term_le','exists_line','logDeriv_simple','contour'),['Any literal LFam, literal ExcZ,0<c0<=1/20,u>=2,T>=1; tau=c0/(8ell(T)).'])
claim(22,'Uniform exceptional-zero explicit formula','With T=exp(c0 sqrt(log u)/32), logB<=sqrt(log u) makes ell(T)<=3sqrt(log u); the contour and Perron errors give C7*u*exp(-c7 sqrt(log u)) uniformly, including the small-height range.',['QW10','QR20','QR21'],ss('psi','norm_lamChi_le','norm_psi_le','pow_four_mul_exp_le','const_le','rpow_le','total_le','psi_exceptional'),['Any literal LFam and ExcZ; u>=2 and logB<=sqrt(log u). The human proof uses a coarser absolute Chebyshev constant in the small-height case, sufficient for the same existential endpoint.'])
claim(23,'Bound the single family-wide exceptional interval loss','The minimum of the two fixed zero-free widths supplies all ExcZ sets, with total cardinality<=1. The B^-46 gap bounds the total interval residue loss by hX(1-c9 B^-46/2).',['QR14','QR17','QR18'],ss('short','zeros','exc_le','sum_le_of_unique'),['Any literal LFam; X>=e,0<=h<=1. All selected zeros are real, simple and>=3/4.'])
claim(24,'Prove the literal uniform weighted interval supplier','Orthogonality, the unique exceptional loss and an explicit conductor/error comparison give sum_{X<n<=X(1+h)}lambda_0(n)>=c9 hX/(4B^47), with fixed constants and the original X,h hypotheses.',['QR22','QR23'],ss('short','sum_psi','sum_est','err_le','trivialClass_shortInterval')+ss('weighted','_root_.GlobalTheory.T.exists_lam_zero_sum_shortInterval_ge'),['Any literal LFam; X>=1, logB<=c sqrt(log X), exp(-c sqrt(log X))<=h<=1, with c chosen once as QR24.'])
claim(25,'Close ShortNorm and the two actual prime-scale consequences','The actual LFam and weighted bound discharge both QW11 premises; prime-power removal gives exponent47 and coefficientc9/32 in ShortNorm, and QW12/QW13 give the literal level-prime interval and9/10 dyadic count.',['QR9','QR24','QW10','QW11','QW12','QW13'],ss('sndef','ShortNorm','ModAt')+ss('pnorm','sum_lam_zero_le_card_normPrimes','sqrt_le_short_main','normPrimes_short_interval_lower')+ss('level','levelPrimeN')+ss('dyad','normPrimesN')+ss('puncond','levelPrime_unconditional','normPrimes_unconditional'),['Original d,M,scale,ModAt,host/rank and endpoint hypotheses remain as in QW11–QW13. No remaining LFam or weighted-interval premise, but no simultaneous geometric choices follow from prime supply alone.'])

remaining=[
 dict(interface='Original geometric applications',scope='The arithmetic LFam, its weighted short-interval lower bound, ShortNorm and the resulting level/dyadic prime suppliers are now proved. Their actual ModAt, host/rank/endpoint hypotheses remain the explicit hypotheses of each application.'),
 dict(interface='Simultaneous global constructions',scope='This arithmetic prime supply does not construct nonempty compatible local stages, simultaneous PairEx, the same-embedding theta/data join, or the centered prime-sum window objects required by the four global branches.'),
]
targets=[]
completed=[]
for key,name,ids,reason in [
 ('lfam','exists_lFam_ray',['QR1','QR2','QR3','QR4','QR5','QR6','QR7','QR8','QR9'],'Full arithmetic LFam constructed with all14 laws, exactB=4dM^2 and same-family NormOne support.'),
 ('lfams','_root_.GlobalTheory.T.exists_lFam_normOne_of_mod_four_eq_three',['QR9'],'Public arithmetic supplier proved from the full ray-family construction.'),
 ('cont','continuation_growth',['QR10'],'Actual Mellin continuation, polynomial growth and real conjugation proved.'),
 ('log','logDeriv_F',['QR11'],'Actual abstract-family right-half-plane exponential representation, nonvanishing and logarithmic derivative proved.'),
 ('exp','LFam.exp_sum_bounds',['QR12'],'All heat estimates and nonprincipal integral at one proved with dominated interchanges.'),
 ('f1','norm_F_one_ge',['QR13'],'Uniform real-character lower bound proved with permissible exponent45.'),
 ('gap','LFam.real_zero_far_from_one',['QR14'],'Uniform polynomial real-zero gap proved with permissible exponent46.'),
 ('local','logDeriv_local',['QR15','QR16'],'Finite local zero-count and logarithmic-derivative formula proved, uniformly in family and character.'),
 ('zfr','zero_free_region',['QR17'],'Two-case zero-free region proved, with exactly the real-character real-zero exception retained for QR18–QR24.'),
 ('unique','main',['QR18'],'Family-wide uniqueness and simplicity of the possible exceptional zero proved.'),
 ('half','logDeriv_sub_exceptional_le',['QR19'],'Literal half-width strip bound after cancelling the simple exception proved.'),
 ('percoef','truncated_perron_of_le_two_vonMangoldt',['QR20'],'Full floor-endpoint truncated Perron error proved.'),
 ('psi','psi_exceptional',['QR21','QR22'],'Uniform exceptional-zero explicit formula proved with actual residue signs and conductor condition.'),
 ('short','trivialClass_shortInterval',['QR23','QR24'],'Full weighted identity-class short-interval lower bound proved, with permissible exponent47.'),
 ('weighted','_root_.GlobalTheory.T.exists_lam_zero_sum_shortInterval_ge',['QR24'],'Public weighted interval supplier proved; it is no longer retained in QW11.'),
 ('pnorm','normPrimes_short_interval_lower',['QR9','QR24','QR25'],'Both arithmetic/analytic premises from QW11 discharged; full original unconditional ShortNorm producer proved.'),
 ('puncond','levelPrime_unconditional',['QR25'],'Actual arithmetic prime supplier now proved; original geometric hypotheses of the application remain.'),
 ('puncond','normPrimes_unconditional',['QR25'],'Literal dyadic norm-prime supplier now proved; original ModAt/scale hypotheses remain.'),
]:
 s=src(key,name);completed.append(dict(path=s['path'],declaration=s['declaration'],claims=ids,reason=reason))
files=[dict(path=p,sha256=sha(b),bytes=len(b),lines=len(b.splitlines()),commit=PIN,url=f'{URL}/blob/{PIN}/{p}',verified_equal_to_pinned_git_blob=True)for p,b in sorted(cache.items())]
artifacts={n:dict(sha256=sha((ROOT/n).read_bytes()),bytes=(ROOT/n).stat().st_size)for n in ['main.tex','report.txt','build_provenance.py']}
links=sum(len(c['sources'])for c in claims);ranges={(s['path'],s['line_start'],s['line_end'],s['range_sha256'])for c in claims for s in c['sources']}
data=dict(artifact_version='0.20',component='ray_prime_estimates',repository=URL,commit=PIN,scope='Full arithmetic LFam with exact norm-prime support, and its uniform analytic weighted interval theorem; polynomial lower bound at one, exceptional-zero gap and explicit formula; unconditional arithmetic ShortNorm and actual level/dyadic consequences.',claim_count=len(claims),source_link_count=links,unique_claim_source_range_count=len(ranges),source_file_count=len(files),claims=claims,source_files=files,proof_artifacts=artifacts,retained_inputs=remaining,completed_targets=completed,independent_reviews=[],validation=dict(read_only_source_access=True,source_range_hashes_regenerated=True,lean_build_performed=False,pdf_build_performed=False),external_background_sources=[dict(url='https://dlmf.nist.gov/27.4',role='Classical absolutely convergent Dirichlet Euler products; the human derivation is in QR11.'),dict(url='https://personal.science.psu.edu/rcv4/personal/Publications/MNTI/09.0_pp_137_167_Dirichlet_series_II.pdf',role='Author-hosted Perron background; QR20 proves the particular truncation and endpoint estimate used here.')])
for filename,reviewer,nums in [('ray_prime_estimates_QR1_9_review.txt','/root/global_frame',range(1,10)),('ray_prime_estimates_QR10_14_review.txt','/root/class_rank',range(10,15)),('ray_prime_estimates_QR15_25_review.txt','/root/comparison_span',range(15,26))]:
 rp=ROOT.parent/'reviews_v0_20'/filename
 if not rp.exists():continue
 raw=rp.read_bytes();content=raw.decode();chosen={c['id']:c['proof_location']['sha256']for c in claims if int(c['id'][2:])in nums}
 assert 'PASS'in content
 for cid,h in chosen.items():assert h in content,('review paragraph changed',filename,cid)
 data['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),review_record='../reviews_v0_20/'+filename,review_record_sha256=sha(raw),paragraph_sha256=chosen,lean_replay=False))
for n,obj in [('provenance.json',data),('source_manifest.json',dict(artifact_version='0.20',component='ray_prime_estimates',repository=URL,commit=PIN,source_files=files,proof_artifacts=artifacts)),('next_targets.json',dict(artifact_version='0.20',repository=URL,commit=PIN,targets=targets,completed_targets=completed,retained_inputs=remaining))]:
 (ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
out=['RAY-CLASS FAMILY AND NORM-PRIME ESTIMATES QR1-QR25',f'Repository {URL}',f'Commit {PIN}',f'{len(claims)} claims, {links} source links, {len(files)} pinned files.','']
for c in claims:
 out += [c['id']+': '+c['title'],'Proof paragraph SHA256 '+c['proof_location']['sha256']]
 for s in c['sources']:out += [f"  {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']}",'  '+s['url'],f"  File {s['full_file_sha256']}; range {s['range_sha256']}"]
 out+=['']
(ROOT/'source_locators.txt').write_text('\n'.join(out)+'\n')
(ROOT/'next_targets.txt').write_text('RAY-CLASS FAMILY — NO RETAINED ARITHMETIC SUPPLIER TARGETS\n\n'+'\n\n'.join(r['interface']+'\n'+r['scope']for r in remaining)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=links,unique_ranges=len(ranges),source_files=len(files),completed_targets=len(completed),next_targets=len(targets)),indent=2))

