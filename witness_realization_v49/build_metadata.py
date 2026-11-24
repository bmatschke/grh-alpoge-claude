#!/usr/bin/env python3
"""Bind actual built-family compatibility and local gain to the accepted source."""
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
sha = lambda data: hashlib.sha256(data).hexdigest()
assert subprocess.check_output(
    ['git', '-C', str(SRC), 'rev-parse', 'HEAD'], text=True).strip() == PIN
D = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
T = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
P = 'src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
I = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
F = 'src/Formalism/LocalToGlobal/'
S = 'src/Formalism/SharpRestriction/'
R = 'src/Formalism/LocalRingCardinality/'

SPECS = {
 'division_and_actual_objects': [
  (T+'SetUnipotentTranslate.lean', 25, 31,
   'setDiv: arbitrary Nu.L and h replacement, with the exact derived HH maximum'),
  (T+'SetUnipotentTranslate.lean', 83, 119,
   'All Lay fields, including given comparison, lattice, twisted forms and local kernel'),
  (T+'SetUnipotentTranslate.lean', 148, 171,
   'LedPart with its Gy equality and full original Obj record'),
  (T+'SetUnipotentTranslate.lean', 193, 221,
   'Actual size, group, comparison, twisted-form, divisor and row-side transports'),
  (T+'SetUnipotentTranslate.lean', 313, 353,
   'Complete extraTr and Obj.tr/Obj.ofPt; kernel uses the given record'),
  (T+'SetUnipotentTranslate.lean', 365, 413,
   'Exact nPrime, hExpl6, LedPart.pt, same Gy, and full ofPt_pt equality'),
  (D+'PointPropertyEqSizeFree.lean', 10, 64,
   'Full Obj2 retains actual comparison/kernel; complete Obj2.tr'),
  (D+'PointPropertyEqSizeFree.lean', 70, 106,
   'ofObj, pointObj, ofObj_tr and exact pointObj_pt at nPrime and hExpl6')],
 'local_kernel_transport': [
  (R+'DataKerP.lean', 26, 67,
   'All seventeen LocalToGlobal2 fields, including actual comparison, integral span and chain equation'),
  (P+'ColumnLocalDataTransportDivision.lean', 29, 41,
   'Exact kernel transport and full ColumnDataSplitPrimes division transport'),
  (P+'InstBack.lean', 25, 38,
   'Actual kerTr and complete ktTr with all KerT fields')],
 'taylor_kernel_transport': [
  (D+'TiedColumnData.lean', 106, 125,
   'KerFam and all nine KerT fields on the actual coefficient data'),
  (D+'ThetaChr.lean', 80, 87,
   'Literal EntC and BuiltE definitions'),
  (D+'StdLvPr.lean', 140, 147,
   'All seven standard lifting-object readings, with unchanged Qp'),
  (D+'FixedVectorEqOfStandardData.lean', 114, 115,
   'EntOk: same KFTie witnesses/UnIs and AdaptedTh'),
  (F+'KernelLattices/ColumnData/KerEntHyp.lean', 18, 78,
   'Given place matrices, thAtW, polynomial evaluation quotient and fixed section'),
  (F+'KernelLattices/ColumnData/KerEntHyp.lean', 80, 136,
   'Actual minor maps, source/target functionals, determinant normalization and unC convention'),
  (F+'KernelLattices/ColumnData/KerEntHyp.lean', 149, 199,
   'All four KerEntHyp clauses and entire kerEntC presentation'),
  (P+'InstBack.lean', 41, 52,
   'Full entC_tr on the same place data, matrices, KerEntHyp and actual equality'),
  (P+'KernelTaylorSeriesPreservedDivisionLatticeChange.lean', 10, 12,
   'Full original kerT_entC_setDiv at its actual input record'),
  (P+'KernelTaylorSeriesPreservedDivisionLatticeChangeStatement.lean', 7, None,
   'Original kernelTaylorSeries_preserved_divisionLatticeChange endpoint')],
 'joint_column_kernel_identity': [
  (D+'PositionOfIntro.lean', 73, 84,
   'All ColT fields, including actual Gt/cmp/g and Hermitian/form equalities'),
  (D+'TiedColumnData.lean', 91, 96,
   'Full ColumnDataSplitPrimes and original GIs2 quantifier order'),
  (D+'NonzeroPlacesOverPrimes.lean', 147, 171,
   'Full Built record, exact dependent (Gt,cmp,tw,ker) equality and IsBuilt'),
  (F+'HermitianColumns/FullSym.lean', 101, 129,
   'Exact prime and kernel embeddings, JoinTiedS and all SymmetricExtraCompatibility fields'),
  (F+'HermitianForms/ExtraSym.lean', 10, 16,
   'Literal ColsFullS and ColsExtraTiedS'),
  (P+'ExtraTiedCol.lean', 10, 21,
   'Original same-Extra column/kernel extraction for WPt, whose finite argument is extended to Built'),
  (P+'ColsReTo0S.lean', 21, 92,
   'All given column, group, Hermitian and form transports used from GCF16')],
 'built_point_and_selected_class': [
  (D+'PositionOfIntro.lean', 56, 64,
   'Original positionOf existential and one joint columns/stages/core equality'),
  (T+'ValidForConstructedPointClassesEventuallyWorking.lean', 67, 109,
   'BPt, actual layout and LedPart, original given D/O and family objAt'),
  (T+'ValidForConstructedPointClassesEventuallyWorking.lean', 222, 257,
   'Link positivity, clsP, Built joint (D,O,b), QOf and unchanged cls'),
  (T+'ValidForConstructedPointClassesEventuallyWorking.lean', 264, 286,
   'IsSel and cls_at on every actual x,hx,i; one jointly identified source object'),
  (T+'ValidForConstructedPointClassesEventuallyWorking.lean', 368, 394,
   'Actual W1/W3, EvC and class-level coefficient/threshold order'),
  (T+'FamilyClassSevenDutiesAndStableLattices.lean', 51, 67,
   'Original cls7 and actual object-property projection'),
  (D+'ThetaChr.lean', 85, 105,
   'IsGoodE and IsBuiltE really refine the unchanged IsBuilt predicate'),
  (T+'GoodReductionCondition.lean', 45, 50,
   'Original RL.At uses IsBuiltE/IsGoodE and further refinements, with same IsLinked')],
 'family_and_closed_contracts': [
  (F+'GroupLattices/StdSubAtOfRing.lean', 36, 89,
   'Every coefficient ring map, all five GroupCompatibilityAll fields, and exact GroupCompatibilityFamily'),
  (S+'GrowthBounds/PlaneCountTheoremWithConstants.lean', 823, 823,
   'Original Ev definition and threshold quantifiers'),
  (S+'ParamsHeightRankConstant.lean', 112, 181,
   'TransportedAlt, Large, pointwise sup and literal Closed choice order'),
  (S+'ParamsHeightRankConstant.lean', 187, 190,
   'Separate DesignExists existential; not concluded by memberwise compatibility'),
  (S+'SmoothDesignExistence/DGamSmooth.lean', 27, 36,
   'Closed restriction and zero-bound classwise construction')],
 'selected_tops': [
  (T+'CountsIrreducibilityConstants.lean', 32, 38,
   'Actual WithChN and D3 classes, preserving the original base member'),
  (S+'SmoothDesignExistence/DesignExistsDes.lean', 10, 15,
   'Full original selected Des membership and its actual ChosenE'),
  (S+'GlobalSchurBounds/Chosen.lean', 18, 90,
   'Exact ChosenTT, ChosenBad and ChosenE witnesses on the same selected subset'),
  (S+'SmoothDesignExistence/AdmissibleTopsMertens.lean', 15, 19,
   'TopsF and projection from original ChosenE'),
  (S+'SmoothDesignExistence/AdmissibleTopsMertens.lean', 73, 144,
   'Original Adm2F and the unchanged harmonic threshold inherited through GLG16')],
 'literal_local_gain': [
  (F+'GroupLattices/LinkGConcreteNoKer.lean', 44, 56,
   'Literal linkG_concrete5 with two Closed inputs on one unchanged class'),
  (S+'GlobalTheoremInputs.lean', 97, 141,
   'Original loG/flG, all five LinkG_at conjuncts, all-place guard and LinkG tending-to-zero error'),
  (I+'LinkG.lean', 14, 27,
   'Full universal GlobalTheory.Top.link_g with original TSel and Duty premises'),
  (F+'Divisibility/DivisibilityRemainder/AdmissibleClasses/LinkGCl.lean', 11, 32,
   'Original TSel comparison, selected tops, linkG_closed and repeated frame guards')],
 'stronger_selector_boundary': [
  (F+'ThresholdSelection.lean', 9, 16,
   'TSelF and TSel thresholds on the actual given Extra'),
  (F+'ClassRec.lean', 21, 31,
   'Full RecT: TiedDataSK, minimal row pin, joints, host and Weil equivariance'),
  (F+'ClassS.lean', 26, 59,
   'TiedDataS including the actual g comparison field'),
  (F+'ClassSLinks.lean', 9, 13,
   'Exact same-comparison family extraction from linked-level records')]
}

inventory, groups, excerpts = {}, {}, []
for group, specs in SPECS.items():
    groups[group] = []
    for i, (path, lo, hi, title) in enumerate(specs, 1):
        data = (SRC/path).read_bytes()
        assert data == subprocess.check_output(
            ['git','-C',str(SRC),'show',PIN+':'+path]), path
        lines = data.splitlines(keepends=True)
        hi = hi or len(lines)
        assert 1 <= lo <= hi <= len(lines), (path,lo,hi,len(lines))
        block = b''.join(lines[lo-1:hi])
        item = dict(id=f'WRS_{group}_{i:02}',path=path,line_start=lo,line_end=hi,
            declaration=title,file_sha256=sha(data),range_sha256=sha(block),
            range_bytes=len(block),source_commit=PIN,
            verified_equal_to_pinned_git_blob=True,
            url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{lo}-L{hi}')
        groups[group].append(item)
        inventory[path] = dict(path=path,sha256=sha(data),bytes=len(data),
            line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{item["id"]}] {title}\n{item["url"]}\n'
                        f'Range SHA256: {sha(block)}\n{block.decode()}\n')

DEPS = {
 1: [],
 2: ['WRS1','GCF16'],
 3: ['WRS1','WRS2','GCF16'],
 4: ['WRS2','WRS3','GCF16'],
 5: ['WRS4'],
 6: ['WRS4','WRS5'],
 7: ['WRS6'],
 8: ['WRS7','GCF18','GLG16'],
 9: [f'WRS{j}' for j in range(1,9)]+['LGS13','GLG9'],
 10: [f'WRS{j}' for j in range(5,10)]+['GCF17','GCF18','LGS13']
}
GROUPS = {
 1:['division_and_actual_objects','local_kernel_transport'],
 2:['division_and_actual_objects','local_kernel_transport','taylor_kernel_transport'],
 3:['division_and_actual_objects','local_kernel_transport','joint_column_kernel_identity'],
 4:['joint_column_kernel_identity','division_and_actual_objects','taylor_kernel_transport'],
 5:['built_point_and_selected_class','division_and_actual_objects','joint_column_kernel_identity'],
 6:['built_point_and_selected_class','family_and_closed_contracts'],
 7:['built_point_and_selected_class','family_and_closed_contracts','selected_tops'],
 8:['family_and_closed_contracts','selected_tops'],
 9:['family_and_closed_contracts','selected_tops','literal_local_gain'],
 10:['literal_local_gain','stronger_selector_boundary','built_point_and_selected_class','family_and_closed_contracts']
}
SCOPES = {
 1:'Every original setDiv by arbitrary submodules and real heights; all seventeen actual LocalToGlobal2 fields, coefficient maps, local models and the original nonzero geometric chain are retained.',
 2:'All nine KerT fields and full EntC equality transport on the original lift objects, same place embeddings and basis matrices; no new Taylor presentation or coefficient field is chosen.',
 3:'The entire dependent (Gt,cmp,tw,ker) equality is mapped once, including its Gy-indexed type; separate coordinate equalities are not substituted for the joint equality.',
 4:'Any original Built witness, all N/h and any given full object with the original exact Obj2 equality; full ColsExtraTiedS and all five GroupCompatibilityAll fields on its actual Extra.cmp/ker.',
 5:'The actual BPt with IsBuilt membership; exact nPrime and hExpl6 division change, same Gy, full object identity and supplied coefficient field.',
 6:'Every unchanged original Fc.cls(Q,Lk,E), with Q refining IsBuilt; every x,hx,i, same actual joint (D,O,b); no new compatibility predicate inserted into E and no TSel premise.',
 7:'Original GroupCompatibilityFamily on each given Extra, threshold Fm.x1+1 uniform in all later indices, and full Closed order with cutoff1/zero bound before family and CH.',
 8:'Original D3 membership, unchanged selected ChosenE/ChosenTT/ChosenBad and GLG16 threshold; internal chosen-top CH is not identified with external Closed CH.',
 9:'Both original Closed inputs actually supplied on the selected built class, exact earlier coefficient bound, same-family five-field LinkG_at, CG=4*Ccount+1 and delta=x^(-eps/2).',
 10:'Exact universal original GlobalTheory.Top.link_g at TSel/Duty premises, plus separate selected-built-class result without those extra premises; full RecT/TSel and common-design nonemptiness remain separate.'
}
FOUNDATIONS = [
 dict(id='WRS_ORIGINAL_RECORD_DEFINITIONS',kind='original_data_and_domain_definitions',
      statement='The original D7/Obj/Obj2, Built/BPt and Fc.cls records and their actual dependent equalities. Membership in the stated class is the domain of a universal theorem, not a newly assumed GroupCompatibilityFamily or a claimed common-design existence theorem.',
      not_a_new_assumed_producer=True,
      source_groups=['division_and_actual_objects','joint_column_kernel_identity','built_point_and_selected_class']),
 dict(id='WRS_ELEMENTARY_EQUALITY_AND_LINEAR_ALGEBRA',kind='standard_mathematical_background',
      statement='Transport along one equality in a dependent family, equality of identical semilinear maps and polynomial evaluations, quotients by the same kernel, and maxima of finitely many real thresholds. All substantive column and quantitative estimates are inherited numbered human claims, recorded in the proof DAG.',
      not_a_new_arithmetic_producer=True,
      source_groups=['local_kernel_transport','taylor_kernel_transport','family_and_closed_contracts']),
 dict(id='WRS_ORIGINAL_SELECTED_CLASS_GUARDS',kind='original_quantifier_and_class_guards',
      statement='The unchanged D3(3,A)=Des(WithChN(A),3), its actual ChosenE, and FamP.Large at the original TransportedAlt order. Every actual given Extra, local group, degree, orbit representative and valuation normalization is preserved.',
      not_a_new_assumed_producer=True,
      source_groups=['family_and_closed_contracts','selected_tops','literal_local_gain']),
 dict(id='WRS_UNIVERSAL_INSTALLER_ORIGINAL_TSEL',kind='original_premise_only_of_universal_corollary',
      statement='Only the arbitrary-class universal original link_g corollary WRS10 retains the original TSel and Duty arguments. The selected built-class producer WRS5-WRS9 does not assume TSel, WPt realization or GroupCompatibilityFamily. Full RecT/TSel is still a distinct requirement of other global arguments.',
      not_used_in_selected_local_gain_proof=True,
      source_groups=['stronger_selector_boundary','literal_local_gain'])
]
EXT = {n:['WRS_ORIGINAL_RECORD_DEFINITIONS','WRS_ELEMENTARY_EQUALITY_AND_LINEAR_ALGEBRA']
       for n in range(1,11)}
for n in [7,8,9,10]: EXT[n].append('WRS_ORIGINAL_SELECTED_CLASS_GUARDS')
EXT[10].append('WRS_UNIVERSAL_INSTALLER_ORIGINAL_TSEL')

proof = (HERE/'main.tex').read_bytes()
text = proof.decode()
assert not any(c<32 and c not in (9,10) for c in proof), 'control character'
claims, blocks = [], {}
for n in range(1,11):
    cid=f'WRS{n}'
    m=re.search(r'^% BEGIN '+cid+r'\n.*?^% END '+cid+r'\n',text,re.M|re.S)
    assert m,cid
    blocks[cid]=m.group()
    named=set(re.findall(r'\b([A-Z]{2,4}[0-9]+)\b',m.group()))-{cid}
    assert named<=set(DEPS[n]),(cid,'unrecorded named references',named-set(DEPS[n]))
    assert all(not d.startswith('WRS') or int(d[3:])<n for d in DEPS[n]),cid
    for prefix,a,b in re.findall(r'\b([A-Z]{2,4})([0-9]+)--\1([0-9]+)\b',m.group()):
        needed={f'{prefix}{j}' for j in range(int(a),int(b)+1)}
        assert needed<=set(DEPS[n]),(cid,'unrecorded range dependency',needed-set(DEPS[n]))
    block=m.group().encode()
    title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1)
    claims.append(dict(id=cid,title=title,introduced_in='0.49',classification='B',
        status='complete human proof at the explicitly stated original scope',
        depends_on=DEPS[n],external_input_ids=EXT[n],published_input_ids=[],
        hypotheses_retained=[SCOPES[n]],source_groups=GROUPS[n],
        sources=[s for group in GROUPS[n] for s in groups[group]],
        proof_location=dict(file=HERE.name+'/main.tex',label='claim:'+cid,
            line_start=text[:m.start()].count('\n')+1,line_end=text[:m.end()].count('\n'),
            sha256=sha(block),bytes=len(block)),source_proof_is_not_human_proof=True))
owners={n:cid for cid,block in blocks.items() for n in re.findall(r'\\tag\{WRS\.(\d+)\}',block)}
for c in claims:
    refs=set(re.findall(r'WRS\.(\d+)',blocks[c['id']]))-set(re.findall(r'\\tag\{WRS\.(\d+)\}',blocks[c['id']]))
    needed={owners[n] for n in refs if n in owners and owners[n]!=c['id']}
    assert needed<=set(c['depends_on']),(c['id'],'unrecorded formula dependencies',needed-set(c['depends_on']))

ledger={c['id']:c for c in json.loads((ROOT/'provenance.json').read_text())['claims']}
human_ids=sorted({d for deps in DEPS.values() for d in deps if not d.startswith('WRS')})
inherited=[]
for cid in human_ids:
    rec=ledger[cid]
    loc=rec['proof_location']
    path=ROOT/loc['file']
    data=path.read_bytes(); lines=data.splitlines(keepends=True)
    if 'line_start' in loc:
        lo,hi=loc['line_start'],loc['line_end']
        block=b''.join(lines[lo-1:hi])
        bound=loc.get('sha256',loc.get('range_sha256',loc.get('paragraph_sha256')))
        assert bound and sha(block)==bound,(cid,sha(block),bound)
        binding='exact previously recorded numbered-claim byte range'
    else:
        lo,hi,block=1,len(lines),data
        assert re.search(r'\b'+cid+r'\b',data.decode()),(cid,path)
        binding='entire immutable legacy chapter containing the named human proof'
    inherited.append(dict(id=cid,file=str(path.relative_to(ROOT)),main_tex_sha256=sha(data),
        block_sha256=sha(block),line_start=lo,line_end=hi,binding_scope=binding,
        kind='numbered_human_proof_dependency',not_an_external_foundation=True))
assert not set(human_ids)&{f['id'] for f in FOUNDATIONS}

lookup={c['id']:c for c in claims}
reviews=[]
for path in sorted(HERE.glob('review_*.json')):
    rev=json.loads(path.read_text())
    assert rev.get('result',rev.get('status'))=='PASS',path
    bound=rev.get('proof_sha256',rev.get('proof_file_sha256',rev.get('main_tex_sha256')))
    assert bound==sha(proof),(path,bound,sha(proof))
    for checked in rev.get('claims_reviewed',[]):
        if isinstance(checked,dict):
            assert checked['result']=='PASS',checked
            bh=checked.get('block_sha256',checked.get('proof_range_sha256'))
            assert bh==lookup[checked['id']]['proof_location']['sha256'],checked
    reviews.append(dict(file=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes())))

completed=[
 'All seventeen LocalToGlobal2 fields under every original setDiv, on the actual coefficient embeddings and geometric chain (WRS1).',
 'Entire nine-field KerT and EntC presentation on the same place embeddings, basis matrices, quotient evaluations and Taylor formula (WRS2).',
 'One dependent comparison/kernel tuple transport, with the actual indexed kernel type (WRS3).',
 'Full ColsExtraTiedS and GroupCompatibilityAll on any given object with the original moved-core identity, using its supplied Extra.cmp and Extra.ker (WRS4).',
 'Actual BPt supplier at exactly nPrime and hExpl6, retaining the original Gy and full object identity (WRS5).',
 'Every member of the unchanged original built class receives that supplier through its joint (D,O,b) equality; no new predicate is inserted into the class (WRS6).',
 'Full original GroupCompatibilityFamily and Closed input, with threshold Fm.x1+1 and earlier cutoff1/zero coefficient bound (WRS7).',
 'Original selected D3 tops and unchanged Adm2F threshold supply the second Closed input on the same family (WRS8).',
 'All five literal LinkG_at fields on the selected built class, exact CG=4*Ccount+1 and delta=x^(-epsilon/2), with full Closed order and no TSel/WPt premise (WRS9).',
 'Full universal original GlobalTheory.Top.link_g at its literal TSel/Duty premises, and exact distinction from common-design existence and the stronger RecT selector (WRS10).'
]
coverage={
 'LocalToGlobal2.all_17_fields_setDiv':'WRS1',
 'KerT.all_9_fields_setDiv':'WRS2',
 'kernelTaylorSeries_preserved_divisionLatticeChange.EntC':'WRS2',
 'dependent_Gt_cmp_tw_ker_equality':'WRS3',
 'ColsExtraTiedS.actual_given_Extra':'WRS4-WRS5',
 'GroupCompatibilityAll.actual_given_Extra_cmp':'WRS4-WRS6',
 'Fc.cls.actual_joint_D_O_b_realization':'WRS6',
 'GroupCompatibilityFamily.selected_built_class':'WRS7',
 'Closed.GroupCompatibilityFamily.before_family_and_CH':'WRS7',
 'Closed.Adm2F.same_D3_selected_subset':'WRS8 via GCF18/GLG16',
 'LinkG_at.all_five_fields_same_member':'WRS9 via completed GLG/LGS',
 'LinkG.delta_tends_zero_before_later_indices':'WRS9',
 'Closed.LinkG.selected_built_class_without_TSel':'WRS9',
 'GlobalTheory.Top.link_g.literal_universal_contract':'WRS10',
 'linkG_frame.original_repeated_guards':'WRS10',
 'DesignExists.common_nonempty_family':'not asserted; separate DESIGN_CHOICES_COMMON',
 'RecT.full_actual_row_host_Weil_selector':'not asserted; separate SECOND_LAYER_COMPATIBLE_SELECTION'
}
frontier=[
 'Construct the actual common nonempty design family satisfying all of the original geometric, row, spectral, period and arithmetic properties. The local-gain theorem is universal over its members and does not solve DESIGN_CHOICES_COMMON.',
 'Construct full RecT/TSel and the same-object row pin, joints, host datum, Weil equivariance and later selected bundles for the other global arguments. These are not consequences of GroupCompatibilityAll.',
 'Complete the distinct original global denominator, retained-defect, period/height and normalized spectral producers, retaining the same family and all original thresholds.',
 'For an arbitrary family outside the original built class, compatibility remains a hypothesis unless supplied by another genuine construction; the arbitrary-class universal original link_g retains its original TSel premise.'
]
traps=[
 'setDiv changes Nu.L, h and the derived HH maximum only; arbitrary N/h are permitted.',
 'The actual geometric chain and Extra.ker are preserved; LGS auxiliary zero-Ch is not used to manufacture an Extra record.',
 'The kernel is indexed by Gt, cmp, tw and Gy. All entries are transported through one dependent sum equality.',
 'BPt uses precisely nPrime(p.L) and hExpl6(D,p.L,Y.X,Csz); its coefficient field, lattice models, original metrics and prime data are unchanged.',
 'The proof uses the original unchanged Fc.cls(Q,Lk,E), not a new class formed by assuming compatibility.',
 'The IsGoodE and further-conjunction predicates used in the selected route really refine IsBuilt.',
 'Every x,hx,i receives compatibility on its own given Extra through the original joint (D,O,b) equality.',
 'The common threshold Fm.x1+1 precedes all later indices and places; Closed bounds precede the family and external CH.',
 'The internal ChosenE witness CH need not equal the arbitrary external Closed CH.',
 'TopsF/Adm2F use the unchanged selected subset and the original threshold max(xa,xb,Fm.x1+1,(16Cb+2)^(3/epsilon)).',
 'All five original LinkG_at conjuncts, inert/signal guard, valuation normalization, CG and vanishing error are retained.',
 'The arbitrary-class original link_g corollary retains TSel and Duty, while the selected-built-class producer does not.',
 'Classwise closure is distinct from existence of a common design member and from the stronger RecT/TSel record.'
]

# Preserve the frozen baseline contract verbatim for the independent closure
# reviewer.  This is a comparison file in this component, never a register edit.
baseline_path=ROOT/'dependency_audit_v0_48/obligation_map.json'
baseline_bytes=baseline_path.read_bytes()
baseline=json.loads(baseline_bytes)
baseline_node=next(n for n in baseline['nodes'] if n['id']=='GLOBAL_LOCAL_GAIN')
baseline_contract=baseline_node['contract']
baseline_node_bytes=json.dumps(baseline_node,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
# Record component acceptance only when the independent root review binds
# the unchanged original contract and complementary reviews cover all claims.
# The common register remains solely the responsibility of root integration.
accepted_whole=[]
acceptance=None
root_review_path=HERE/'review_WRS6_WRS10_root.json'
if root_review_path.is_file():
    root_review=json.loads(root_review_path.read_text())
    assert root_review['result']=='PASS'
    assert root_review['proof_sha256']==sha(proof)
    selected=root_review['selected_whole_contract_reviewed']
    assert selected['id']=='GLOBAL_LOCAL_GAIN'
    assert selected['full_original_contract_closed_in_stated_scope'] is True
    assert selected['baseline_contract_sha256']==sha(baseline_contract.encode())
    covered={c['id'] for c in root_review['claims_reviewed']}
    for relative in root_review['complementary_independent_review_files']:
        peer_path=ROOT/relative
        peer=json.loads(peer_path.read_text())
        assert peer['result']=='PASS' and peer['proof_sha256']==sha(proof)
        covered.update(c['id'] for c in peer['claims_reviewed'])
    assert covered==set(lookup)
    peer_binding=root_review['complementary_independent_review_binding']
    assert sha((ROOT/peer_binding['file']).read_bytes())==peer_binding['sha256']
    accepted_whole=['GLOBAL_LOCAL_GAIN']
    acceptance=dict(review_file=str(root_review_path.relative_to(ROOT)),
        review_sha256=sha(root_review_path.read_bytes()),proof_sha256=sha(proof),
        baseline_graph=str(baseline_path.relative_to(ROOT)),
        baseline_graph_sha256=sha(baseline_bytes),
        original_contract_sha256=sha(baseline_contract.encode()),
        complementary_review=peer_binding,
        full_original_contract_closed_in_stated_scope=True,
        common_ledger_edited_by_this_builder=False)
closure_comparison=dict(
 schema='rh-selected-leaf-contract-comparison/1',artifact_version='0.49',
 component=HERE.name,target='GLOBAL_LOCAL_GAIN',
 proof_file=HERE.name+'/main.tex',proof_sha256=sha(proof),
 baseline_file=str(baseline_path.relative_to(ROOT)),baseline_file_sha256=sha(baseline_bytes),
 baseline_node_sha256_canonical_json=sha(baseline_node_bytes),
 baseline_contract_verbatim=baseline_contract,
 baseline_contract_utf8_sha256=sha(baseline_contract.encode()),
 baseline_original_evidence=baseline_node['evidence'],
 exact_original_universal_endpoint='For every A, original TSel(A) and Duty(A) imply Closed(D3(3,A),LinkG), with unchanged LinkG_at.',
 exact_selected_endpoint='For every unchanged Fc.cls(Q,Lk,E) with Q refining original IsBuilt, Closed(D3(3,A),LinkG), with no additional TSel, WPt realization or compatibility premise.',
 selected_given_extra_supplier='WRS4-WRS7',
 original_five_field_gain_and_quantifier_match='WRS9-WRS10',
 original_closed_cutoff='1/104',
 coefficient_bound_before_family='pre=0; t=0; mid=4129; last=max(5600002,Corb(epsilon)), pointwise maximum with the two already-zero supplied bounds',
 actual_family_threshold='Fm.x1+1 for compatibility, then maximum with all original LGS/GLG/top thresholds',
 exact_error='delta(x)=x^(-epsilon/2), bo=b^delta(x), CG=4*Ccount+1',
 all_original_five_fields=True,selected_family_TSel_premise_added=False,
 independent_kernel_or_comparison_chosen=False,common_family_nonemptiness_claimed=False,
 full_RecT_or_TSel_claimed=False,
 proposed_whole_obligation_closures=['GLOBAL_LOCAL_GAIN'],
 independently_accepted_whole_obligation_closures=accepted_whole,
 independent_whole_contract_acceptance=acceptance,
 shared_register_status_changed=False,
 review_status=('Exact whole-contract closure independently accepted; parent integration controls the common register.'
  if accepted_whole else 'proposed exact closure; parent independent review controls integration'))

contracts=dict(
 schema='rh-built-family-compatibility-contracts/1',artifact_version='0.49',
 component=HERE.name,source_commit=PIN,proof_file_sha256=sha(proof),
 endpoint_claim='WRS9',literal_universal_endpoint_claim='WRS10',
 actual_given_extra_endpoint='WRS5',family_supplier_endpoint='WRS7',
 original_endpoint='GlobalTheory.Top.link_g',
 original_full_scope=closure_comparison['exact_original_universal_endpoint'],
 selected_scope=closure_comparison['exact_selected_endpoint'],
 completed_original_substatements=completed,original_field_coverage=coverage,
 exact_guards_preserved=traps,remaining_actual_producers=frontier,
 human_dependency_ids=human_ids,external_input_ids=[f['id'] for f in FOUNDATIONS],
 selected_consumer_only=False,full_original_GIs2_reused=True,
 actual_given_comparison_and_kernel=True,same_coefficient_field=True,
 all_original_LinkG_fields=True,LinkG_selected_requires_TSel=False,
 selected_GroupCompatibilityFamily_produced=True,
 both_original_Closed_inputs_produced=True,
 whole_obligation_closures=accepted_whole,proposed_whole_obligation_closures=['GLOBAL_LOCAL_GAIN'],
 independent_whole_contract_acceptance=acceptance,
 no_lean_replay=True,not_claimed=['common design nonemptiness','full RecT/TSel construction',
 'compatibility of arbitrary families outside the original built class',
 'other global quantitative leaves','complete RH or GRH'])
prov=dict(
 schema='rh-human-component-provenance/1',artifact_version='0.49',
 date='2026-11-23',component=HERE.name,source_commit=PIN,
 main_tex_sha256=sha(proof),proof_file_sha256=sha(proof),claims=claims,
 source_groups=groups,source_inventory=list(inventory.values()),source_files=list(inventory),
 published_applications=[],retained_foundations=FOUNDATIONS,
 inherited_human_inputs=inherited,independent_reviews=reviews,
 builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
 validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
 claim_blocks=len(claims),direct_named_claim_dependencies_checked=True,
 numbered_range_dependencies_checked=True,numbered_formula_dependencies_checked=True,
 external_foundations_separate_from_claim_DAG=True,whole_original_leaf_closures=accepted_whole,
 proposed_whole_original_leaf_closures=['GLOBAL_LOCAL_GAIN']),
 independent_whole_contract_acceptance=acceptance,
 scope_note='Full actual given-Extra compatibility on every original built-class member, both Closed inputs and literal five-field LinkG, without an added selected TSel premise. Original universal link_g also proved at its original premises. Common-design nonemptiness and full RecT/TSel remain separate.')
closure=dict(
 schema='rh-human-component-closure/1',artifact_version='0.49',component=HERE.name,
 proof_file_sha256=sha(proof),new_claims=[c['id'] for c in claims],new_claim_count=len(claims),
 completed_original_substatements=completed,whole_obligation_closures=accepted_whole,
 proposed_whole_obligation_closures=['GLOBAL_LOCAL_GAIN'],remaining_actual_producers=frontier,
 independent_whole_contract_acceptance=acceptance,
 status=('Full selected built-family local-gain supplier complete, with independently accepted exact GLOBAL_LOCAL_GAIN closure. No shared status changed by this builder.'
  if accepted_whole else 'Full selected built-family local-gain supplier complete; proposed exact GLOBAL_LOCAL_GAIN closure pending independent parent review. No shared status changed.'),
 actual_given_comparison_and_kernel=True,all_five_compatibility_fields_on_given_Extra=True,
 coefficient_field_and_original_geometric_chain_unchanged=True,
 arbitrary_division_lattice_transport=True,actual_common_BPt_membership_used=True,
 unchanged_Fc_cls_used=True,selected_GroupCompatibilityFamily_produced=True,
 selected_D3_TopsF_produced=True,selected_D3_Adm2F_produced=True,
 both_original_Closed_inputs_produced=True,selected_local_gain_requires_TSel=False,
 exact_error_and_constants_preserved=True,full_original_LinkG=True,
 common_design_existence_claimed=False,full_original_RecT_or_TSel_claimed=False,
 closure_contract_comparison_file='closure_comparison.json',
 no_lean_replay=True)

outputs={'provenance.json':prov,'contracts.json':contracts,'closure.json':closure,
 'closure_comparison.json':closure_comparison,
 'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,
 source_commit=PIN,source_files=list(inventory.values()),ranges=groups,verified_against_git=True),
 'retained_foundations.json':FOUNDATIONS,'published_inputs.json':[]}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 'ACTUAL BUILT-FAMILY COMPATIBILITY AND THE FULL LOCAL GAIN — v0.49\n'
 f'Source pin: {PIN}\nProof SHA256: {sha(proof)}\n\n'
 f'{len(claims)} numbered human proofs, all classification B; '
 f'{len(inventory)} pinned source files; {sum(map(len,groups.values()))} source ranges; '
 f'{len(inherited)} inherited numbered-human-proof bindings.\n\n'
 f'Independently accepted whole-contract closures: {accepted_whole}. '
 'The accepting review binds these exact proof bytes, complementary claim coverage '
 'and the unchanged original selected contract. Only parent integration changes '
 'the common register.\n\n'
 'The new supplier is compatibility on the ACTUAL given Extra of every member of the '
 'original unchanged built class. Earlier GCF gave the complete column stage and exact '
 'comparison transport. This chapter proves that the built-class membership already '
 'supplies the needed common realization, without asking for the stronger WPt/RecT/TSel '
 'record used elsewhere. The result is not obtained by adding compatibility as a new '
 'class predicate. The original Fc.cls, its arbitrary bundle type, linkage and further '
 'property E are all retained.\n\n'
 'WRS1 checks every field of the original LocalToGlobal2 record under arbitrary setDiv. '
 'That operation changes the division submodules, heights and their derived HH maximum; '
 'it leaves the coefficient fields, local embeddings, lattice tuples, classes, Taylor '
 'series and semilinear comparison maps unchanged. The exact integral-span and chain '
 'equations remain equations of the same maps. This transports the actual geometric '
 'kernel, with no zero-chain substitution. WRS2 checks all nine KerT fields and the full '
 'EntC presentation. Its polynomial evaluation quotient and section, fixed place '
 'embeddings, basis matrices, source and target minor functionals and normalizing '
 'scalar remain the original ones; all four KerEntHyp conditions and the kernel '
 'formula therefore transport simultaneously.\n\n'
 'WRS3 applies one transport map to the original dependent (Gt,cmp,tw,ker) equality. '
 'It does not try to identify separately chosen kernels over potentially different '
 'comparison maps. WRS4 uses the original Built witness and its ColumnDataSplitPrimes '
 'to obtain full ColsExtraTiedS and all five GroupCompatibilityAll fields on any supplied '
 'full object with the exact moved-core identity. This includes its actual Extra.cmp and '
 'Extra.ker, not just isomorphic images.\n\n'
 'WRS5 checks that the actual BPt is precisely such an object. Its designated division '
 'lattice is the O_L-span of a*y with a in the original Iu and y in NuLat; its height is '
 'the original hExpl6. The source pointObj_pt identity transports the whole smaller '
 'object, and its given Gy equality identifies the local lattice field and kernel type. '
 'No coefficient extension, new local frame or independently selected comparison is used.\n\n'
 'WRS6 then opens the existing Fc.cls membership at each x,hx,i. Its Built witness '
 'contains one joint equality of (D,O,b) to the actual BPt and bundle. Transporting the '
 'previous conclusion through that equality supplies every given family Extra, with '
 'arbitrary later indices and height witnesses. The selected IsGoodE predicate and '
 'its further original conjunctions refine IsBuilt by forgetting fields. No extra '
 'TSel or eventual-realization hypothesis is added.\n\n'
 'WRS7 gives the literal GroupCompatibilityFamily with x_g=Fm.x1+1. Its Closed form '
 'chooses cutoff1 and zero TransportedAlt bounds before the family and external CH. '
 'WRS8 obtains the other Closed input from the existing D3 ChosenE field, using the '
 'same selected tops and the original GLG16 threshold '
 'max(xa,xb,Fm.x1+1,(16*Cb+2)^(3/epsilon)). The internal ChosenE witness CH is not '
 'silently identified with the external arbitrary CH in Closed.\n\n'
 'WRS9 applies the already completed LGS13 consumer after both of its actual inputs '
 'have been supplied. Its coefficient bound is chosen before the family: cutoff1/104, '
 'pre=t=0, mid4129 and last=max(5600002,Corb(epsilon)). The later common height threshold '
 'precedes all members, places and local degrees. All five literal LinkG_at conjuncts '
 'are preserved: actual normalized lattice inclusion and length, empty-served zeros, '
 'the exact Sv estimate, bounded gains and class-sum inequality, served-orbit coverage '
 'and both MeanKappaBound clauses. The coefficient is C_G=4*Ccount+1 and the single '
 'vanishing error is delta(x)=x^(-epsilon/2), with b_o=b^delta(x).\n\n'
 'WRS10 also gives the universal original GlobalTheory.Top.link_g implication for an '
 'arbitrary class with its original TSel and Duty arguments. That is a separate '
 'literal endpoint; it does not reinsert TSel into the selected built-class proof. '
 'The full frozen baseline GLOBAL_LOCAL_GAIN contract is quoted verbatim and hashed '
 'in closure_comparison.json. Its independent whole-contract acceptance is recorded '
 'when the bound parent review and complementary claim coverage are present. '
 'The component builder does not edit the common register.\n\n'
 'BOUNDARIES THAT REMAIN\n'+''.join('- '+x+'\n' for x in frontier)+
 '\nThese are human mathematical proofs with exact source dictionaries, not a Lean '
 'replay or a recertification of the accepted formal source. The repeatable builder '
 'checks every cited source byte against the accepted pin, binds every inherited '
 'human proof and all new proof blocks, and keeps external definitions/foundations '
 'separate from the numbered-claim DAG.\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
        if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,
    artifact_version='0.49',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),
 source_ranges=sum(map(len,groups.values())),inherited_claims=len(inherited),
 main_tex_sha256=sha(proof),actual_family_supplier='WRS7',selected_local_gain='WRS9',
 literal_universal_endpoint='WRS10',proposed_whole_obligation_closures=['GLOBAL_LOCAL_GAIN'],
 independent_reviews=len(reviews)),indent=2))
