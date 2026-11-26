"""Regenerate HW pinned-source correspondence; no Lean execution or edits."""
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
GT = 'src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/'
CB = 'src/Development/AutomorphicArithmetic/CharacterBoxes/'
PATHS = {
 'host_defs':GT+'ThinScalesIffHostBound.lean',
 'val':GT+'PairRowIffQdRows.lean',
 'point':GT+'DisjointExceptional.lean',
 'construct':GT+'ValidForConstructedPointClassesEventuallyWorking.lean',
 'wall_defs':GT+'AuxiliaryPrimeMemAvoidedPrimes.lean',
 'arith':'src/Formalism/LocalToGlobal/GlobalTheory/IsResidueClassZero.lean',
 'inst':GB+'DefsInst.lean',
 'params':GB+'IsResidueClassZero.lean',
 'small':GB+'SmallOrderPrimes.lean',
 'extra':LC+'DataExtra.lean',
 'iface':SR+'InertJacobiLevels/AsmIface.lean',
 'scale':LC+'DataParams₂.lean',
 'loss_transfer':GI+'WeightRequirementOfValid.lean',
 'window_transfer':GI+'WeightWindowRequirementHostOfPoint.lean',
 'same':GI+'SamePointOfSameScale.lean',
 'kit':GI+'KitOfPoints.lean',
 'host_ww':CB+'HostWW.lean',
 'kit_s':CB+'KitS.lean',
 'has_wall':GI+'HasWithDutyWallAndChoices.lean',
 'family_ctor':GI+'ExistsFamPOfKits.lean',
 'family':SR+'FamCore.lean',
 'point_small':GI+'WeightAdmissibleSmallSharesAtPoint.lean',
 'chosen7':SR+'GlobalSchurBounds/WeightVectorSmallSharesSeven.lean',
 'chosen8':SR+'GlobalSchurBounds/WeightVectorSmallSharesEight.lean',
 'design':CB+'DesignS.lean',
 'num_supplier':GI+'SzRowNumAt.lean',
 'initial_pair':GI+'ExistsWeightsInWindows.lean',
 'initial_code':GI+'MPowFiveMulFMulLLe.lean',
 'shares':SR+'RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean',
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
 {'id':'HW1',
  'title':'Exact point-to-host and host-to-point degree-loss transport',
  'status':'proved_human_actual_relabeling_under_supplied_point_records',
  'statement':'Pt.From and Val identify the actual arithmetic bases, candidates and Frobenius steps. CanonInst supplies the canonical orbit selector, independently of Extra.kapI_def, which identifies the universal infima. Thus WeightVectorExists transfers to a zero-extended host pair with exact WinOK and WOK; conversely a point constructed From that pair satisfies actual WReq and WallPt.',
  'depends_on':['GW5'],
  'assumptions':['Supplied actual Pt C, Std C, Val C cD ch, Pt.From the indicated host, CanonInst, and its actual Extra.kapI_def.',
                 'For the forward existence application use GW5 at the point; for the reverse implication use host WOK and degrees zero off the selected set.'],
  'sources':refs('host_defs','hPH baseOf WinOK WOK Pt.From Pt.From.field Pt.From.congr_field Pt.From.QS_eq Pt.From.art_eq Pt.From.rd_eq Pt.From.cls_eq CanonInst')+
   refs('val','h0v Delv HCVal Val')+
   refs('point','Pt Val.mem_box')+
   refs('arith','Base Ins bsH ins Formalism.L2.GlobalTheoryTheory.Arith.Loc.Cand Formalism.L2.GlobalTheoryTheory.Arith.Loc.goodReps Formalism.L2.GlobalTheoryTheory.Arith.Loc.Sig Formalism.L2.GlobalTheoryTheory.Arith.Loc.kapISet')+
   refs('inst','kapISet KapIDef')+
   refs('extra','Extra')+
   refs('small','cands WReq WeightVectorExists admW')+
   refs('loss_transfer','baseOfParams kapISet_eq_loc sig_eq_loc wreq_of_wok')+
   refs('window_transfer','weightWindowRequirement_host_of_point'),
  'new_human_argument':'Explicit equality of the universal sets and canonical orbit selectors makes the loss termwise identical; the auxiliary ep parameter in Arith.ins is irrelevant to Sig and is not asserted to match the point exponent.'},
 {'id':'HW2',
  'title':'Temporary-family selection and actual fixed-pair reconstruction for every position',
  'status':'proved_human_HostWW_degree_join_and_complete_actual_Kit_equalities_conditional_on_point_supply',
  'statement':'Build a temporary family from supplied arbitrary-pair point constructors and numerical records, apply GW5 uniformly, and transfer the chosen pair to its original host. Invoke the universal point constructor again for this same pair and all u0<n. Prove every Pt.Same field, including the lifted offsets from fills and Val.hc, canonical kappaI, the whole natural-input ep function, code labels and cover; all resulting points satisfy WallPt.',
  'depends_on':['HW1','GW5'],
  'assumptions':['Literal HostExQW/HostGood with RankVal, canonical q0 and any additional retained host predicate.',
                 'Std C and C.GK.Nonneg; the actual ObjC/ObjCP point constructor for every admissible pair and all u0, with its uniform nested thresholds.',
                 'Supplied initial window pair, admissible injective code, and actual NumAt records for temporary and final points.',
                 'The temporary family meets the already stated GI/GII/GJ/GW5 hypotheses; its constants and J are fixed before the scale.'],
  'sources':refs('point','Pt.Same Kit Kit.cover_weights Pt.Same.weights')+
   refs('host_defs','Pt.From Pt.From.words CanonInst HostGood')+
   refs('val','HCVal Val')+
   refs('iface','TiesAt ExtraAt NumAt')+
   refs('extra','Extra')+
   refs('inst','EpDef kapISet KapIDef')+
   refs('params','cG DIf c6f tIf ParametersFill')+
   refs('scale',"w''")+
   refs('same','bsH_val_congr mem_iff_val_mem kapISet_congr nonempty_place off_lift same_of_from')+
   refs('kit','kit_of_points')+
   refs('wall_defs','ObjC HostExQW HostWW WClosed WallPt')+
   refs('construct','ObjCP KitCPW')+
   refs('host_ww','gk_nonneg large_sup scale_ext UpperTheory.Top.hostWW')+
   refs('kit_s','kitS')+
   refs('has_wall','has_withDuty_wall_and_choices')+
   refs('family_ctor','exists_famP_of_kits')+
   refs('initial_pair','exists_weights_in_windows','explicit_retained_initial_pair_supplier')+
   refs('initial_code','exists_injective_words','explicit_retained_word_code_supplier')+
   refs('num_supplier','szRow_numAt','explicit_retained_actual_numerical_supplier'),
  'new_human_argument':'Reconstruct the full equality record rather than cite same_of_from as a black box; the actual Hodge filling equation yields the offset formula. State the two constructor calls and nested constant order explicitly.',
  'remaining_inputs':['Arithmetic host existence with all HostGood clauses, including the required top-set properties.',
                      'Actual universal input-pair point construction, its geometric records and numerical supply; these are not asserted proved by HW2.',
                      'The nondegree portions of KitCPW, such as the thick-set and chosen-bad-prime assertions, require their separate named suppliers.']},
 {'id':'HW3',
  'title':'Literal family constructor carries WallPt to ChosenWall and ChosenWS',
  'status':'proved_human_actual_constructor_transport_without_CoverAll',
  'statement':'The explicit cutScale/index construction copies the reconstructed point and NumAt records, carries the proved common fields and cover_weights, and retains WallPt for every family index. The exact indicator identity gives ChosenWall. At each sufficiently large allowed x, Ix_win supplies a carrier of its own admissible degrees, so ChosenWS follows without CoverAll.',
  'depends_on':['HW2'],
  'assumptions':['Uniform kits and actual NumAt on the supplied unbounded scale window, Std C and C.GK.Nonneg.',
                 'All point/numerical records are retained as actual source data; outside the window the large-scale index set may be empty.'],
  'sources':refs('family_ctor','cutScale cutScale_alt cutScale_ge cutScale_mem Kit.bTopOf_eq famOfKits exists_famP_of_kits')+
   refs('point','classOf Kit.cover_weights Val.mem_box')+
   refs('wall_defs','WallPt WallAll setTu setTu_cls')+
   refs('small','admW WReq')+
   refs('point_small','weightAdmissible_smallShares_at_point')+
   refs('chosen7','ChW_at ChosenW ChosenWS chosenWS_of_cover')+
   refs('chosen8','ChosenWall chosenWS_of_wall')+
   refs('family','FamCore FamCore.CoverAll FamCore.coverS_carry FamCore.coverU_hyp_self')+
   refs('design','designS','actual_family_endpoint_transport_only')+
   refs('shares','Shares','explicit_remaining_biased_top_set_requirement'),
  'new_human_argument':'An existing member carries its own degrees and ChosenWall controls all indices. This identifies the actual primary degree-realization route without requiring an unused stronger coverage property.',
  'remaining_inputs':['The supplied host/point/NumAt inputs of HW2, including simultaneous host top construction and biased Frame.Shares.',
                      'Other global geometric, slope, arithmetic-host and final analytic assembly branches remain outside these claims.']},
]

for claim in claims:
    claim['proof_location']={'file':'host_weight_join/main.tex',
                             'expanded':'host_weight_join/report.txt',
                             'section':claim['id']}
    claim.setdefault('remaining_inputs',[])

records=[source for claim in claims for source in claim['sources']]
unique={(s['path'],s['line_start'],s['line_end'],s['range_sha256']) for s in records}
for s in records:
    raw=(REPO/s['path']).read_bytes().splitlines(keepends=True)
    part=b''.join(raw[s['line_start']-1:s['line_end']])
    assert hashlib.sha256(part).hexdigest()==s['range_sha256']
    assert raw[s['line_start']-1].decode().rstrip('\r\n')==s['first_line']
    assert len(part)==s['range_bytes']

ledger={
 'component':'host_weight_join','artifact_version':'0.11','repository':URL,'commit':PIN,
 'range_convention':'Inclusive one-based raw-line bytes, including original line endings.',
 'claims':claims,
 'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
 'scope':'Conditional actual degree-realization join. No host, biased top-set, point-construction or full global RH/Dirichlet-GRH proof is asserted.',
 'review_scope':{
  'remarks_math':'Passed HW1-HW3 against the actual host/point loss identities, HostWW, KitS, Same offsets, cutScale and chosenWS_of_wall. Clarified Std/GK.Nonneg, all-natural ep equality and totalized logarithms; no substantive error remained. Scoped record: v0_11/reviews/gi_reviews_hw.txt.',
  'root':'Reviewed main argument and notation; natural ceilings and the function w_double_prime(n)=b_prime/(xn) made explicit.',
  'scope':'Human reconstruction and exact source correspondence; no full Lean build or kernel replay.'},
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

