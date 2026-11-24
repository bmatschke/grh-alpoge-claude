#!/usr/bin/env python3
"""Bind DEX proofs to the original source. This does not run Lean."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--repo', type=Path, required=True)
args=P.parse_args()
ROOT=Path(__file__).resolve().parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'
cache={}
def sha(b): return hashlib.sha256(b).hexdigest()
decl=re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+')
def source(path,name):
    if path not in cache:
        data=subprocess.check_output(['git','-C',str(args.repo),'show',PIN+':'+path])
        assert (args.repo/path).read_bytes()==data, path
        cache[path]=data
    data=cache[path];lines=data.splitlines(keepends=True)
    pat=re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+'+re.escape(name)+r'(?=\s|\(|\{|:|$)')
    starts=[i for i,l in enumerate(lines) if pat.search(l.decode())]
    assert len(starts)==1,(path,name,starts)
    a=starts[0];b=next((i for i in range(a+1,len(lines)) if decl.search(lines[i].decode())),len(lines))
    raw=b''.join(lines[a:b])
    return dict(path=path,declaration=name,source_spelling=name,line_start=a+1,line_end=b,
      sha256=sha(data),range_sha256=sha(raw),range_bytes=len(raw),first_line=lines[a].decode().rstrip(),
      role='Exact source contract or proof counterpart; the written human proof supplies the stated implication',
      verified_equal_to_pinned_git_blob=True,url=URL+path+f'#L{a+1}-L{b}')

F='src/Formalism/'
S=F+'SharpRestriction/'
G=S+'GlobalSchurBounds/'
A='src/Development/AbelianVarietyTheory/'
D=A+'Definitions/GlobalTwisting/'
I=A+'Proofs/GlobalInterpolation/'
C='src/Development/AutomorphicArithmetic/CharacterBoxes/'
FIRST=G+'FirstClaimLemmaTwoFourOfLemmaTwoThree.lean'
CONDUCT=G+'GeneralLinearActions/FiltrationCocycleLiftCriterion.lean'
PARS=D+'ValidForConstructedPointClassesEventuallyWorking.lean'
AUX=D+'AuxiliaryPrimeMemAvoidedPrimes.lean'
CHOICES=S+'DesignExistsOfChoices.lean'
specs=[
('DEX1','Exact host-conductor and bounded odd-part deductions',[],[
 (CONDUCT,'IsCharED'),(CONDUCT,'BoxE'),(CONDUCT,'GoodFor'),(FIRST,'level_dvd_condN'),
 (FIRST,'oddQS_le_Co'),(FIRST,'realBoxE_of_boxE')],[],[]),
('DEX2','Literal ChosenThin with coefficient one on every supplied family',
 ['DEX1','CC14','CC16','CC17','CC18'],[
 (G+'MainIn.lean','BoxesF'),(G+'MainIn.lean','QDRowsF'),(G+'Chosen.lean','ChThin_at'),
 (G+'Chosen.lean','ChosenThin'),(G+'MainSup.lean','chosenThin_of_boxesN'),
 (G+'MainSup.lean','chosenThin_closedN'),(G+'MainSup.lean','logNE_le_of_rows')],
 ['The same actual family, BoxesF and QDRowsF; the existing CC analytic inputs in their recorded scopes.'],[]),
('DEX3','Published Minkowski theorem matched to the literal rational divisor',[],[
 (G+'MainIn.lean','MinkMult'),(CHOICES,'MinkDiv'),
 (F+'FlagUnipotentLattices/MemOfOrthogonalAnisotropic.lean','minkowskiExp'),
 (F+'FlagUnipotentLattices/MemOfOrthogonalAnisotropic.lean','minkowskiM')],[],
 ['Serre, Bounds for the orders of the finite subgroups of G(k), Lecture I, §1.1, Theorem 1(i); finite H⊂GL_n(Q), n≥1; n=0 proved separately.']),
('DEX4','Elementary factorial comparison and uniform DGamSize constant twelve',['DEX3'],[
 (F+'LocalRingCardinality/MinkMEqMinkowskiNumber.lean','padicValNat_minkM'),
 (F+'LocalRingCardinality/MinkMEqMinkowskiNumber.lean','minkM_dvd_factorial'),
 (F+'FlagUnipotentLattices/MinkowskiFactorialBounds/MinkowskiNumberDvdFactorial.lean','minkowski_number_dvd_factorial'),
 (CHOICES,'log_minkM_fN'),(CHOICES,'dGamSize_of_dvd')],
 ['Actual DGamDvdF on the original family.'],[]),
('DEX5','Exact numerical rank proviso with constants one-half and e',[],[
 (G+'TopDensityNGeSixteen.lean','RankM'),(G+'TopDensityNGeSixteen.lean','gamL_eq'),
 (G+'MainSup.lean','proviso_e'),(G+'Chosen.lean','ChProviso_at'),(G+'Chosen.lean','ChosenProviso'),
 (G+'StandardLattice.lean','FactDuStar'),(G+'StandardLattice.lean','FactDstar'),
 (F+'GL3MeanSquares/HookFormulaTorsion/OneAddInvPowLeExpOne.lean','mass_corollary')],
 ['Original RankM, exact FactDuStar/FactDstar, and the original level-prime window. For a family, its actual eventual RankM supplier remains.'],[]),
('DEX6','Finite closure calculus with all thresholds before one family',[],[
 (S+'ParamsHeightRankConstant.lean','TransportedAlt.sup'),
 (S+'ParamsHeightRankConstant.lean','FamP.Large'),
 (S+'ParamsHeightRankConstant.lean','Closed'),
 (S+'ParamsHeightRankConstant.lean','Closed.and')],
 ['Closed predicates on the same class.'],[]),
('DEX7','A three-input sufficient construction of literal DesignExists',
 ['DEX2','DEX4','DEX5','DEX6'],[
 (CHOICES,'DesignChoices'),(CHOICES,'designExists_of_choices'),
 (S+'ParamsHeightRankConstant.lean','DesignExists'),(G+'Chosen.lean','ChosenE'),
 (I+'LinkEx.lean','GlobalTheory.Top.link_ex')],
 ['Actual DesignChoices on one original class; its Closed TuSize implication; its Closed eventual original RankM.'],[]),
('DEX8','One common selector from universal eventual row properties',['DEX6'],[
 (PARS,'ParEv'),(PARS,'EvP'),(PARS,'Built'),(PARS,'QOf'),(PARS,'ExB'),
 (PARS,'RowE'),(PARS,'Row'),(PARS,'pick'),(PARS,'Row.elim'),
 (D+'EventuallyAllScaleContextsAndOfBoth.lean','RowL.and'),
 (D+'EventuallyAllScaleContextsAndOfBoth.lean','RowL.elim'),(C+'ClassSel.lean','classSel')],
 ['Literal ExBL and all required RowL premises over the same core/link, plus recursive existence to make the selected class large.'],[]),
('DEX9','Actual family from kits including fallback and empty indices',[],[
 (I+'ExistsFamPOfKits.lean','cutScale'),(I+'ExistsFamPOfKits.lean','famOfKits'),
 (I+'ExistsFamPOfKits.lean','exists_famP_of_kits'),(I+'ExistsFamPOfKits.lean','bTopOf_ge')],
 ['One kit and its NumAt records on every allowed late scale, with all original kit equalities and coverage.'],[]),
('DEX10','Complete compatible DesignChoices join from the literal kit input',
 ['DEX3','DEX9','SZ9'],[
 (C+'DesignS.lean','designS'),(I+'ExistsStdLarge.lean','stdConst'),
 (I+'ExistsStdLarge.lean','exists_std_large'),(I+'FixAndWinOfNumAt.lean','fix_and_win_of_numAt'),
 (AUX,'DesignChoices'),(AUX,'withObj'),(AUX,'setTu'),(AUX,'thrTu'),(AUX,'setTu_large'),
 (D+'DisjointExceptional.lean','classOf_reqPt'),(PARS,'KitCPW'),(PARS,'Link')],
 ['The exact KitCPW premise, carrying original withDuty/withObj, WallPt and target G.pt on the same points.'],[]),
('DEX11','Exact RecExP-to-DesignChoices route with current core frontier',
 ['DEX8','DEX10','RF10','AC10','SZ12','QR25','HX1','HW1','HW2','GW5','QW9','MF20'],[
 (PARS,'RecExP'),(PARS,'ObjCP'),(C+'ObjCTrue.lean','recS'),(C+'KitS.lean','kitS'),
 (I+'MPowFiveMulFMulLLe.lean','m_pow_five_mul_f_mul_L_le'),
 (I+'MPowFiveMulFMulLLe.lean','exists_injective_words'),
 (A+'Proofs/IwasawaDecomposition/ExistsLayeredDataOfGoodScaleContexts.lean','recExP_of_recAtG'),
 (D+'FamilyClassSevenDutiesAndStableLattices.lean','cls7'),(C+'Supply.lean','ExD')],
 ['Literal RecExP(withQD QO) for the common object predicate and target HostExW. Actual RecAtG, eventual QO/bundle existence and row suppliers remain; window_lower is already supplied by QW9/MF20.'],[])
]

raw=(ROOT/'main.tex').read_bytes();lines=raw.splitlines(keepends=True)
claims=[]
for cid,title,deps,refs,inputs,classic in specs:
    a=next(i for i,l in enumerate(lines) if l.decode().startswith('\\paragraph{'+cid+':'))
    b=next((i for i in range(a+1,len(lines)) if lines[i].decode().startswith('\\paragraph{')),len(lines))
    proof=b''.join(lines[a:b])
    claims.append(dict(id=cid,title=title,introduced_in='0.31',classification='A' if cid=='DEX3' else 'B',
      status='Complete human proof in the exact explicitly stated supplied-data scope',depends_on=deps,
      remaining_inputs=inputs,classical_inputs=classic,
      mathematical_status='Matched published input' if cid=='DEX3' else 'Independently reconstructed implication on original data',
      source_relation='Exact source consumer or a proved weaker sufficient interface; no Lean replay and no unproved arithmetic existence inferred',
      proof_location=dict(file='design_existence/main.tex',paragraph=cid,label='claim:'+cid,line_start=a+1,line_end=b,sha256=sha(proof),bytes=len(proof)),
      sources=[source(*r) for r in refs],component_ledger='design_existence/provenance.json'))

registry=[dict(id='DEX-Minkowski-Q',classification='A',theorem='Minkowski, as stated in Serre, Lecture I §1.1, Theorem 1(i)',
  url='https://www.college-de-france.fr/media/jean-pierre-serre/UPL3821667391778701726_6___Bounds_for_the_orders.pdf',
  locator='Printed p.4 (PDF page 4), Theorem 1(i)',consumer='MinkDiv / MinkMult n (minkM n)',proof_claim='DEX3',
  hypotheses_checked=['n≥1 for the published theorem; rank zero is trivial and handled separately',
   'The original subgroup is finite and lies in GL_n(Q)',
   'All source prime and exponent cutoffs equal the finite nonzero part of the published product'],
  conclusion='The exact subgroup order divides the exact source minkM integer, for every rank',
  primary_source_rechecked_this_round=True)]
data=dict(schema='rh-human-component-provenance/1',artifact_version='0.31',date='2026-11-22',commit=PIN,
  repository=URL.split('/blob/')[0],component='design_existence',claims=claims,
  main_tex_sha256=sha(raw),published_applications=registry,
  source_files=[dict(path=p,sha256=sha(d),bytes=len(d),line_count=len(d.splitlines()),verified_equal_to_pinned_git_blob=True) for p,d in sorted(cache.items())],
  validation=dict(claims=len(claims),source_files=len(cache),claim_source_ranges=sum(len(c['sources']) for c in claims),
   source_files_match_pinned_git=True,proof_hashes_bound_to_current_text=True,new_lean_replay=False))
(ROOT/'provenance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n'.join(c['id']+' '+s['url'] for c in claims for s in c['sources'])+'\n')
(ROOT/'published_applications.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data['validation'],indent=2))
