#!/usr/bin/env python3
"""Bind DSZ human proofs to pinned source contracts; no Lean replay."""
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
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+')
def source(path,name):
    if path not in cache:
        data=subprocess.check_output(['git','-C',str(args.repo),'show',PIN+':'+path])
        assert (args.repo/path).read_bytes()==data, path
        cache[path]=data
    data=cache[path];lines=data.splitlines(keepends=True)
    pat=re.compile(r'^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable)\s+)*(?:def|abbrev|theorem|lemma|structure|class)\s+'+re.escape(name)+r'(?=\s|\(|\{|:|$)')
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
I=A+'Proofs/GlobalInterpolation/'
PARS=A+'Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean'
GAP=G+'GeneralLinearActions/GapAtLeast.lean'
THREE=G+'TheoremThreeFamilyOfGappedMultiplicity.lean'
EX=G+'TheoremThreeOfExplicitAndCompact.lean'
JOINT=G+'JointsL.lean'
THICK=G+'ThickPlacesCorollaryOfAnyTranslate.lean'
STD=G+'StandardLattice.lean'
SIZES=S+'ElevenLe.lean'
DATA=F+'LocalRingCardinality/DataParams₂.lean'
HEIGHT=S+'ParamsHeightRankConstant.lean'
TIES=F+'LocalRingCardinality/DataTies.lean'
UP=G+'TheoremThreeFamilyOfFormalDegreeInput.lean'
ALL=F+'LocalToGlobal/GlobalTheory/GL5/TheoremThreeAllUnitary.lean'
groups={
 'Z01':[(GAP,n) for n in ['vand','facProd','dimV','rhoN','nPlus','nMinus','dTau','lamAbs','GapAtLeast']],
 'Z02':[(ALL,n) for n in ['ncPairs_card_le','lamAbs_ge_one','facProd_mul_le','fdegHC_le_dTau','fdegHC_nonneg']],
 'Z03':[(THREE,'finrank_lowK_eqG'),(THREE,'theorem_three_of_gap_bound')],
 'Z04':[(THREE,'thrDS_lt'),(F+'PeriodIntegrals/UnitaryGroupMassFormula/FormalDegreeGap/DimensionBoundOfGapUniform.lean','gap_big')],
 'Z05':[(THREE,'theorem_three_of_weyl_gapped_multiplicity'),(THREE,'explicit_bound_all_scales')],
 'Z06':[(EX,'DiscreteSeriesDegreeBoundsOfGap'),(EX,'spectralGapLowerBound'),(EX,'SigmaDegreeTwoSidedBoundOfGap')],
 'Z07':[(GAP,'rowLam'),(GAP,'rowSgn'),(THREE,'theorem_three_rows_of_real_place')],
 'Z08':[(TIES,'cdScaleTie'),(TIES,'dsigTie'),(TIES,'Ties')],
 'Z09':[(THREE,'explicit_bound_family'),(THREE,'theorem_three_rows_family_holds'),(G+'FlipTwoThree.lean','fam0'),(HEIGHT,'Closed'),(S+'ParConsts.lean','FamP')],
 'Z10':[(SIZES,n) for n in ['SizeN','SizeM','SizeK','SizeKRel','SizeCond','SizeQD','SizeNodes','SizeDel','SizesAt']],
 'Z11':[(JOINT,n) for n in ['db_rk','db_rdE','db_pi_le_v','db_basic','sizes_clause_seventeen']]+[(F+'LocalRingCardinality/DataParams.lean',"ParameterChoice'")],
 'Z12':[(DATA,'SizeData₂'),(JOINT,'db_cloud'),(JOINT,'db_vN'),(JOINT,'db_uN'),(JOINT,'db_bN'),(JOINT,'db_wj')],
 'Z13':[(SIZES,n) for n in ['SizeRho','SizeBot','SizeEta']]+[(JOINT,n) for n in ['db_w','eta_size_le_b_div_27','db_xeta','db_bT','db_xS','db_xk','db_win','db_top','db_be']],
 'Z14':[(STD,'DataB'),(JOINT,'dataB_of'),(JOINT,'dataB_fam'),(THICK,'one_le_column_sub_of_lt'),(THICK,'place_data_under_section_B')],
 'Z15':[(SIZES,'SizeKRel'),(JOINT,'logGam_le'),(JOINT,'m_ge'),(JOINT,'m_large_fam')],
 'Z16':[(GAP,n) for n in ['idxColLoc','idxRowLoc','idxPi','idxSig','duStarP','DstarP','volY0','uColR','duStarU','DstarD','logXuD']],
 'Z17':[(THICK,'gap_bound_at_one_third'),(THICK,'parameter_gap_under_section_B'),(STD,'FactDuStar'),(STD,'FactDstar')],
 'Z18':[(EX,'LocalIndexFormulasAndBounds'),(EX,'IndexProductFormulasAndRatio'),(EX,'LemmaFiveOneIdentity')],
 'Z19':[(G+'LinkMin.lean','family_of_global_statements'),(THICK,'mass_telescope'),(THICK,'mass_eq_mass_mul_ratio_prod')],
 'Z20':[(G+'GlobalRankLatticeProofs/LogFactorialProductDifference.lean','place_dimension_upper_bound'),(G+'GlobalRankLatticeProofs/LogFactorialProductDifference.lean','log_X_upper_arithmetic')],
 'Z21':[(G+'GlobalRankLatticeProofs/LogWeightMinusLogBBound.lean','place_dimension_lower_bound'),(G+'GlobalRankLatticeProofs/LogWeightMinusLogBBound.lean','log_X_lower_arithmetic')],
 'Z22':[(G+'LinkMin.lean','upper_weight_bound_eventually'),(G+'LinkMin.lean','part_five_family_of_mass_volume')],
 'Z23':[(DATA,'AdmT'),(F+'LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean','D7')]+[(F+'LocalRingCardinality/DataKernels.lean',n) for n in ['ColumnsAtT','Xu','Tstar']],
 'Z24':[(HEIGHT,'TuSize'),(DATA,'TuGe'),(JOINT,'tuGe_of'),(JOINT,'tuSize_of'),(JOINT,'tuSize_fam')],
 'Z25':[(UP,'cTmin'),(UP,'tuSize_min')],
 'Z26':[(PARS,n) for n in ['Built','QOf','cls','IsSel','cls_at','pick','pick_isSel','Built.ind']],
 'Z27':[(I+'RealTiedSetDiv.lean','realTied_setDiv'),(I+'RealTiedSetDiv.lean','built_val'),(A+'Definitions/GlobalTwisting/SetUnipotentTranslate.lean','setDiv'),(A+'Definitions/AutomorphicMembership/AmbientBaseHeq.lean','Core')],
 'Z28':[(PARS,'Row'),(PARS,'Row.of_sel'),(PARS,'Row.elim'),(HEIGHT,'Closed'),('src/Development/AutomorphicArithmetic/CharacterBoxes/ClassSel.lean','classSel')],
 'Z29':[(I+'GenusMassEntry.lean','row_hTu_cTmin')],
}
specs=[
 ('DSZ1','Finite product comparison with the exact lowest compact type',['DC1','DC10','DC13'],['Z01','Z02','Z03'],[],[]),
 ('DSZ2','Source gap reaches actual reconstructed discrete-series range',['DSZ1']+['DC'+str(i) for i in range(1,13)]+['DC18','DC19'],['Z04','Z05','Z06'],[],['HC-Deg in DC18, with all normalization and group hypotheses retained.']),
 ('DSZ3','Stored-degree equality and the original h3 family slot',['DSZ2'],['Z06','Z07','Z08','Z09'],['The original cdScaleTie and dsigTie; both are supplied by every FamP member.'],['HC-Deg in DC18.']),
 ('DSZ4','Actual family coordinates and all needed window bounds',['QW8'],['Z10','Z11','Z12','Z13','Z14','Z15'],['One original FamP and its params/sizes fields, eventually after its own threshold.'],[]),
 ('DSZ5','Exact row degree polynomial on every late original member',['DSZ3','DSZ4'],['Z09','Z14','Z16','Z17'],['For the displayed Dstar mass identity: original BaseVolumeEqualsMass.'],['HC-Deg in DC18.']),
 ('DSZ6','Literal mass-index-factorial identity',['DSZ5','QW1','QW2','QW3','MF19','RSL1','RSL2','RSL3'],['Z16','Z18','Z19'],['The original eventual BaseVolumeEqualsMass; supplied on the construction class by DSZ10.'],['Inherited MF Hasse–Minkowski and GV Tamagawa applications in their established scopes.']),
 ('DSZ7','Harmonic upper Vandermonde comparison on the actual cloud',['DSZ4'],['Z12','Z14','Z20','Z21'],[],[]),
 ('DSZ8','Two-sided actual logarithmic ratio bounds',['DSZ4','DSZ6','DSZ7','QW1','QW2','QW3','QW4','QW5','QW6'],['Z17','Z18','Z19','Z20','Z21','Z22'],['The same original volume identity as DSZ6.'],['Inherited mass and formal-degree inputs.']),
 ('DSZ9','Literal TuSize with the original cTmin constant',['DSZ8'],['Z15','Z17','Z23','Z24','Z25'],['An original family with eventual BaseVolumeEqualsMass and cTmin(CYL) <= CTu.'],['Inherited mass and formal-degree inputs.']),
 ('DSZ10','Construction-class row supplier and Closed quantifiers',['DSZ9','DEX6','DEX7','DEX8','RSL1','RSL2','RSL3'],['Z26','Z27','Z28','Z29'],['The exact construction class cls(Q,Lk,E), or its original subclasses, with Bd=Bundle. Its membership supplies Built; no nonemptiness of that class is concluded.'],['Inherited MF Hasse–Minkowski, GV Tamagawa, and HC-Deg applications.']),
]
raw=(ROOT/'main.tex').read_bytes(); lines=raw.splitlines(keepends=True)
claims=[]
anchors={a:[source(*r) for r in refs] for a,refs in groups.items()}
for cid,title,deps,refs,inputs,classic in specs:
    a=next(i for i,l in enumerate(lines) if l.decode().startswith('\\paragraph{'+cid+':'))
    b=next((i for i in range(a+1,len(lines)) if lines[i].decode().startswith('\\paragraph{')),len(lines))
    proof=b''.join(lines[a:b]); seen=set(); ss=[]
    for group in refs:
        for s in anchors[group]:
            key=(s['path'],s['line_start'],s['line_end'])
            if key not in seen: ss.append(s);seen.add(key)
    claims.append(dict(id=cid,title=title,introduced_in='0.32',classification='B',
      status='Complete human proof in the exact explicitly stated supplied-data scope',depends_on=deps,
      remaining_inputs=inputs,classical_inputs=classic,
      mathematical_status='Independently reconstructed implication on original data',
      source_relation='Exact source consumer or independently proved sufficient estimate; no Lean replay and no unsupported arithmetic existence',
      proof_location=dict(file='degree_prime_size/main.tex',paragraph=cid,label='claim:'+cid,line_start=a+1,line_end=b,sha256=sha(proof),bytes=len(proof)),
      source_anchors=refs,sources=ss,component_ledger='degree_prime_size/provenance.json'))
registry=[dict(id='HC-Deg-retained-DSZ',classification='A',proof_claim='DSZ2',
 theorem='Harish–Chandra, Discrete series for semisimple Lie groups II, Acta Mathematica 116 (1966), §40 Corollary 2, §41 Theorem 16',
 url='https://repository.ias.ac.in/30833/1/336.pdf',locator='Printed pp.94–96; inherited DC18 application',
 hypotheses_checked=['Connected semisimple SU(p,q), p,q>=1, with finite center and compact Cartan',
 'Actual regular integral infinitesimal parameter and genuine discrete-series representation from the general construction in DC1–DC12',
 'DC18 passes through U(1) x SU(p,q) -> U(p,q), probability central measure and representation-independent finite-cover scalar',
 'DC16–DC18 determine the group-and-Haar constant for the literal compact-dual Haar measure',
 'DSZ2 proves the source numerical gap exceeds the actual DC existence/rigidity thresholds'],
 conclusion='Exact degree equals dimV(lambda), hence the source h3 inequalities after DSZ1',
 new_independent_classical_assumption=False)]
data=dict(schema='rh-human-component-provenance/1',artifact_version='0.32',date='2026-11-22',commit=PIN,
 repository=URL.split('/blob/')[0],component='degree_prime_size',claims=claims,main_tex_sha256=sha(raw),
 published_applications=registry,source_anchor_groups=anchors,
 source_files=[dict(path=p,sha256=sha(d),bytes=len(d),line_count=len(d.splitlines()),verified_equal_to_pinned_git_blob=True) for p,d in sorted(cache.items())],
 validation=dict(claims=len(claims),source_files=len(cache),claim_source_ranges=sum(len(c['sources']) for c in claims),
 source_files_match_pinned_git=True,proof_hashes_bound_to_current_text=True,new_lean_replay=False))
(ROOT/'provenance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n'.join(a+' '+s['url'] for a,ss in anchors.items() for s in ss)+'\n')
(ROOT/'published_applications.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.32',component='degree_prime_size',
 closed=['TASK_GL3_GAP_DEGREE: exact h3 on every supplied family, DSZ1–3.',
 'DESIGN_TUSIZE_CLOSED: on the original Built construction class with cT=cTmin, DSZ4–10.'],
 remaining=['Actual common construction-class DesignChoices/family existence.',
 'No full Vandermonde variation/counting package is asserted by this sufficient size proof.',
 'All inherited named classical inputs retain their existing stated scopes.'],
 main_tex_sha256=sha(raw),provenance_sha256=sha((ROOT/'provenance.json').read_bytes()))
(ROOT/'closure.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')
(ROOT/'report.txt').write_text('DSZ1–DSZ10: exact original formal degree and a direct level-prime size proof.\n'
 'The actual class membership supplies Built and RealTied, then RSL supplies BaseVolumeEqualsMass. The construction of a compatible class member remains.\n'
 'The harmonic interior Vandermonde comparison replaces only the upper estimate needed for TuSize; the source stronger variation package is not claimed.\n'
 'Named inherited inputs: HC-Deg (DC18), Hasse–Minkowski (MF), Tamagawa (GV). No new Lean build/replay.\n')
print(json.dumps(data['validation'],indent=2))

