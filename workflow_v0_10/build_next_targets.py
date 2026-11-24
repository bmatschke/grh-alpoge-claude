"""Build the v0.10 continuation map without asserting a new theorem.

Validate exact pinned declaration ranges and retain the four v0.9 global
branch records as identical JSON values and an identical rendered suffix.
"""
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE/'alpoge-rh'
OLD_PATH = BASE/'output/RH_reconstruction_v0_9/next_source_targets.json'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
LT = 'src/Formalism/LocalToGlobal/'
AA = 'src/Development/AutomorphicArithmetic/'
old_raw = OLD_PATH.read_text()
old = json.loads(old_raw)
assert old['commit'] == PIN
head = subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
assert head == PIN, ('unexpected checkout',head)
PREFIX = r'(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*'
DECL = re.compile(r'^'+PREFIX+r'(?:def|theorem|lemma|abbrev|structure|inductive|instance)\s+(\S+)')
BOUND = re.compile(r'^'+PREFIX+r'(?:def|theorem|lemma|abbrev|structure|inductive|instance|namespace|end|section|variable|attribute|open|include|set_option)\b')
files = {}
targets = []

def source(path):
    if path in files:
        return files[path]
    raw = (REPO/path).read_bytes()
    assert raw == subprocess.check_output(['git','-C',str(REPO),'show',f'{PIN}:{path}']), path
    lines = raw.splitlines(keepends=True)
    stack, declarations = [], []
    for i, rawline in enumerate(lines):
        line = rawline.decode().rstrip('\r\n')
        if m := re.match(r'^namespace\s+(\S+)',line):
            stack.append(('namespace',m[1]))
        elif m := re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$',line):
            stack.append(('section',m[1]))
        elif m := re.match(r'^end(?:\s+(\S+))?\s*$',line):
            assert stack, (path,i+1,'unmatched end')
            kind,label = stack.pop()
            assert not m[1] or m[1] == label, (path,i+1,label,m[1])
        elif m := DECL.match(line):
            ns = '.'.join(label for kind,label in stack if kind == 'namespace')
            declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))
    assert all(kind == 'section' and label is None for kind,label in stack), (path,stack)
    info = {'path':path,'sha256':sha256(raw).hexdigest(),
            'full_file_sha256':sha256(raw).hexdigest(),'bytes':len(raw),
            'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,
            '_lines':lines,'_declarations':declarations}
    files[path] = info
    return info

def add(stage,path,name,role,remaining,connections=(),branch=None):
    f = source(path)
    hits = [d for d in f['_declarations'] if d[0] == name or d[2] == name]
    assert len(hits) == 1, (path,name,hits)
    spelling,start,qualified = hits[0]
    lines = f['_lines']
    end = start+1
    while end < len(lines) and not BOUND.match(lines[end].decode()):
        end += 1
    while end > start+1 and not lines[end-1].strip():
        end -= 1
    part = b''.join(lines[start:end])
    link = f'{URL}/blob/{PIN}/{path}#L{start+1}-L{end}'
    rec = {'priority_group':stage,'path':path,'declaration':qualified,
           'source_spelling':spelling,'line_start':start+1,'line_end':end,
           'sha256':f['sha256'],'full_file_sha256':f['full_file_sha256'],
           'range_sha256':sha256(part).hexdigest(),'range_bytes':len(part),
           'url':link,'pinned_url':link,'first_line':lines[start].decode().rstrip('\r\n'),
           'declaration_lines_within_range':[start+1],
           'verified_equal_to_pinned_git_blob':True,'role':role,
           'remaining_human_scope':remaining,'source_connections':list(connections),
           'human_status':'continuation_target_only; no additional theorem claim or proof by this map'}
    if branch is not None:
        rec['unchanged_global_branch_index'] = branch
    targets.append(rec)

# 1. The actual global/local numerical interfaces and how local theorems are used.
add(1,GB+'Joints.lean','HypIAt',
    'Literal large-prime hypothesis at each good orbit of the actual family.',
    'Supply the good-orbit period/separation, AuxBlock8.HypI and exact weight-window membership uniformly; a local Conclusion2 under HypI does not supply these.',
    ['AdmissibleFamilyNoKernel.hypIAt_ev','LogarithmicSums/MeanNum.restHypI_ev'])
add(1,GB+'Joints.lean','HypIIAt',
    'Literal small-prime Type-II data: orbit size, prime/rank, gaps, windows and full degree/error budget.',
    'Prove every displayed inequality on the actual candidate primes and good representatives, especially N1^2<=r*#tops and the Qp^5 size bound.',
    ['SizesAtRecord.NumII','SizesAtRecord.numII_ev','SizesAtRecord.hypIIAt_ev'])
add(1,GB+'Joints.lean','type_one_hypothesis_of_bounds',
    'Entry point from the completed local Type-I Conclusion2 to the family adm8 interface.',
    'Read this as a wrapper; expand type_one_hypothesis_of_segments and its KapIDef, window and height comparisons.',
    ['Joints.type_one_hypothesis_of_segments','TopChoiceBounds.orbit_segments'])
add(1,GB+'Joints.lean','type_one_hypothesis_of_segments',
    'Substantive Type-I use: transport the local exceptional function to the actual KapIDef and average on global weight boxes.',
    'Check the infimum/serving definition, exact box identifications, tI<=tIf, uniform constants and the final mean comparison.',
    ['Joints.hypI_69_to_13','Joints.tI_le_tIf','Joints.winA_eq','Joints.winB_eq'])
add(1,GB+'Joints.lean','hypI_69_to_13',
    'Exact translation from the global AuxBlock8.HypI to the local flipOneThree.HypI.',
    'Derive its scales, conductor, odd-band exclusion and segment hypotheses using the actual global Scale and OrbitSegs; do not identify the two HypI records by their names.')
add(1,GB+'Joints.lean','tI_le_tIf',
    'Additional global-use height comparison beyond the now-proved local tStar<=tI.',
    'Match the global tIf thresholds, maxima/odd-exponent sums and all constant inequalities to the literal local tI formula.')
add(1,GB+'Joints.lean','type_two_hypothesis_of_counts',
    'Transport of the Type-II orbit-valuation theorem into AuxBlock8.adm6.',
    'Match actual candidate orbit counts and constants to the completed controlled-edge theorem, preserving rank, height and exceptional normalization.',
    ['TableLineDegreeFive.aux₃','TableLineDegreeFive.OrbitValuationBound','PlaneCountTheoremWithConstants.family_second_bound_of_theorem'])
add(1,GB+'Joints.lean','StdSubAt',
    'Existence of a standard unramified quadratic subsetting with a finite ring map into each actual local coefficient ring.',
    'Construct the compatible standard subring at every served place; HM12 compares two RS settings but does not assert this finite-extension existence.',
    ['LocalToGlobal/GroupLattices/StdSubAtOfRing.RingCompatibleAt','LocalToGlobal/GroupLattices/StdSubAtOfRing.stdSubAt_of_ring'])
add(1,LT+'GroupLattices/FockModels/LPBase.lean','lpBaseChange',
    'Actual LPprime transport along finite coefficient-ring extensions.',
    'Reconstruct the finite-extension lattice and rank transport, including changes in uniformizer valuation; distinguish it from HM12 ring isomorphism invariance.',
    ['UnramifiedQuadraticSetting.LPBaseChange','Joints.StdSubAt'])
add(1,GB+'Joints.lean','linear_programming_input_of_hypotheses',
    'Joins adm6/adm7, both actual hypothesis records, standard subrings and finite base change into OrbitLatticeBounds.',
    'Identify actual local orbit labels, TT, dominant weights and edge data with the global lattice-system ties, then follow the two prime regimes and exact normalization.',
    ['CornerGLContinuity.OrbitLatticeBounds','PlaneCountTheoremWithConstants.family_bounds_of_local_systems'])

# 2. Substantive suppliers of orbit abundance and eventual hypotheses.
add(2,GB+'TopChoiceBounds.lean','segment_count_log_bounds',
    'Logarithmic orbit geometry gives n*delta/(C log x)<=#tops<=40*n*delta.',
    'Expand the actual goodU/small-multiplicity/window-count ceiling estimates and the finite top-count argument; FG frame existence alone does not give this lower density.',
    ['TopChoiceBounds.bc_size','GrowthSums.Top.topCount','TopChoiceBounds.period_ge_three_gap_eventually'])
add(2,GB+'TopChoiceBounds.lean','uniform_constant_of_master',
    'Concrete orbit-count and gap conversion to AuxBlock8.adm1 at an instance, with one constant for fixed r,h.',
    'Match topsPos to the actual orbit vertices, parity and cyclic shifts; transport the count, next-top and preceding-top bounds with their exact cardinalities.',
    ['CornerGLContinuity.OrbitPositionsAndSizeBounds','TopChoiceBounds.vertex_count_eq_card_tops','TopChoiceBounds.mem_tops_on_orbit_iff'])
add(2,GB+'TopChoiceBounds.lean','family_uniform_constant_of_master',
    'Uniformizes the adm1 constant over every sufficiently large member of a FamP family.',
    'Check the order of choices: epsilon fixes r and h, then one constant and threshold work for every family index i and candidate orbit.',
    ['TopChoiceBounds.family_uniform_constant_holds','TopChoiceBounds.master_orbit_lemma_holds'])
add(2,GB+'SizesAtRecord.lean','numII_ev',
    'Substantive eventual numerical supplier of every NumII inequality.',
    'Derive the seven displayed Type-II bounds from SizesAt and the actual lower bound n*delta/(C31 log x)<=N, tracking eps and all uniform constants.',
    ['SizesAtRecord.NumII','SizesAtRecord.DII_arith','SizesAtRecord.SzII_arith'])
add(2,GB+'SizesAtRecord.lean','hypIIAt_ev',
    'Combines NumII with actual prime, period, window and good-representative data.',
    'Verify the finite thresholds, 13<=p, r>=2, 2L1<=L2, lower/upper top counts and shifted weight inequalities simultaneously.',
    ['SizesAtRecord.windows_at','SizesAtRecord.hypIIAt_fam_of','SizesAtRecord.hypIIAt_fam'])
add(2,GB+'LogarithmicSums/MeanNum.lean','restHypI_ev',
    'Substantive eventual large-prime Type-I numeric supplier using size, signature, orbit and mean bounds.',
    'Expand the actual RestHypI proof and its dependencies adm5, ArchimedeanSignatureMatching, adm1 and NumMean; retain simultaneous uniformity over D,L,X,p and good representatives.',
    ['LogarithmicSums/MeanNum.numMean_ev','AdmissibleFamilyNoKernel.hypIAt_ev'])
add(2,LT+'GroupLattices/AdmissibleFamilyNoKernel.lean','hypIAt_ev',
    'Actual FamP supplier of Joints.HypIAt.',
    'Match the substantive MeanNum and TopChoiceBounds results to family sizes, exact windows, LaG and the large-scale period condition, preserving one eventual threshold.',
    ['TopChoiceBounds.family_band_ratio_statement','TopChoiceBounds.family_large_scale_conditions_hold','PlaneCountTheoremWithConstants.family_sizes_bound'])
add(2,GB+'TopChoiceBounds.lean','family_log_bound_threshold',
    'Uniform source of FamilyWindowLogBound/ CbLarge from actual orbit-window counts.',
    'Prove the logarithmic bound with CN chosen after epsilon and before the family, including the empty-family branch; this is an input to both actual hypothesis suppliers.')

# 3. Narrow navigation anchors for the four unchanged global branches.
add(3,LT+'Divisibility/DivisionHeightBoundStatement.lean','DivClauses',
    'Exact package separating actual divisibility, theta/period and height outputs.',
    'Keep PL12--PL20 and AG1--AG10 boundaries: prove the remaining actual theta/common-image, chain norm, kernel and spectral identifications before applying the conditional deductions.',
    ['DivisionHeightBoundStatement.divClauses_of','DIVRecBridgeSel.linkDIVt_of_bridge_kernel'],branch=1)
add(3,'src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingHypothesesHoldFamily.lean','linkS_of_standing_hypotheses',
    'Archimedean LinkS application with its actual standing-hypothesis inputs.',
    'Reconstruct the remaining source-model and chain-norm inputs; neither the ideal-lattice packing bound nor local Type-I/II completion alone supplies this package.',
    ['CuspSpanNormBounds.StandingNumericalData.StandingHypotheses','GlobalTheoremInputs.LinkS'],branch=1)
add(3,LT+'GlobalTheory/GL6/RamifiedLatticePropsOfModel.lean','ramified_lattice_props_of_model',
    'Actual retained ramified source rank/slope transport from the model.',
    'Prove the required integral and isometric identification, dimension balance and discarded-target bounds; retain the already proved conditional LC/SR/GF deductions.',
    ['RamifiedLatticePropsOfModel.RamifiedSlopeFormula','SliceIntegralDeltaNeBot.MramH_mu'],branch=2)
add(3,AA+'CharacterBoxes/ExistsPageN.lean','VWinAt',
    'Exact cohomological window input for a fixed character and depth parameter.',
    'Expand the two-primary, odd-minus and odd-plus window constructions and congruence denominators; OH/GH character identities do not supply these estimates.',
    ['AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/VwinOfRow.UpperTheory.One.vwin_of_row'],branch=3)
add(3,AA+'CharacterBoxes/PairGood.lean','PairEx',
    'Simultaneous auxiliary-prime pair selection with full PairGood data.',
    'Prove abundant pairs satisfying congruences, zero-free boxes, logarithmic derivatives and centered twisted ramps together, uniformly in the required range.',
    ['CharacterBoxes.PairGood','CharacterBoxes.ExistsPageN.exists_pageN','CharacterBoxes.WinPairs.UpperTheory.Top.winPairs'],branch=4)
add(3,AA+'DedekindLFunctions/LandauTheorems/ChBalance.lean','ch_balance',
    'Uniform gain-to-centered-prime-sum passage used after the arithmetic family estimates.',
    'Complete the still-retained arithmetic comparison and simultaneous window inputs; do not replace them by the already proved scalar exponent balance or analytic endpoint.',
    ['PrimitiveCosets.LevelGmLeOnFamilyScales.level_gm_le_on_family_scales','PrimitiveCosets.CoreGm.UpperTheory.Comparison₂.core_gm'],branch=4)

assert len({(t['path'],t['line_start'],t['line_end']) for t in targets}) == len(targets)
for t in targets:
    raw = (REPO/t['path']).read_bytes().splitlines(keepends=True)
    part = b''.join(raw[t['line_start']-1:t['line_end']])
    assert sha256(part).hexdigest() == t['range_sha256']
    assert len(part) == t['range_bytes']
    assert raw[t['line_start']-1].decode().rstrip('\r\n') == t['first_line']
completed_names = {'UpAt','LowAt','RestUp','RestLow','restUp_of','restLow_of',
                   'countUp_of','countLow_of','tail_of','notKeptWt_of',
                   'keyIneq_of','finrank_letter','tle_of','paired_lifts_of_identity'}
assert not completed_names & {t['source_spelling'] for t in targets}
out = {
    'version':'0.10','commit':PIN,'head_verified':head,
    'status':'Read-only continuation/source map; no additional theorem claim, human proof or Lean replay is asserted.',
    'target_count':len(targets),'source_file_count':len(files),
    'count_policy':'Consumers must use target_count or len(targets); no fixed historical target count is required.',
    'line_range_convention':'inclusive, one-indexed, original source bytes including line endings',
    'completed_previous_frontier':[
        'Earlier FG/OR/CP/EA prove the local Type-II ConclusionE under its literal hypotheses for C>=4129.',
        'RU1--RU11 close the actual coarse upper count, digit-to-HH dimension conversion, weighted lattice/Smith extraction and paired-lift HH certificate.',
        'RD1--RD15 close the coarse lower count, harmonic density, exact finite-window average and exceptional mean.',
        'NP1--NP9 close uniform local Std and segment numerics, fixed-weight/mean records and the shifted tStar<=tI comparison.',
        'HM1--HM12 close actual harmonic dimensions/maps, KeyIneq, complementary cloud maps, dual-height/tensor interfaces and RS-isomorphism invariance.',
        'The final supplied-HypI local Type-I implication is tracked in the separate TC component; this source map adds no proof claim.',
    ],
    'next_local_priority':'Actual global HypIAt/HypIIAt supply, uniform good-orbit abundance, finite coefficient extension, and the precise local-to-global use of the completed local Type-I/II conclusions.',
    'priority_groups':[
        {'priority':1,'name':'Exact actual-family interfaces and use of local theorems','target_count':sum(t['priority_group']==1 for t in targets)},
        {'priority':2,'name':'Substantive orbit abundance and uniform numerical suppliers','target_count':sum(t['priority_group']==2 for t in targets)},
        {'priority':3,'name':'Navigation anchors for unchanged global branches','target_count':sum(t['priority_group']==3 for t in targets)},
    ],
    'precision_notes':[
        'HypIAt and HypIIAt are actual arithmetic-family hypothesis records, distinct from the completed local HypI and Hyps implications.',
        'A frame on a supplied good orbit does not itself prove the uniform lower density n*delta/(C log x)<=#tops needed by SizesAtRecord.numII_ev.',
        'HM12 proves RS-isomorphism invariance; StdSubAt and finite-extension LPBaseChange are different actual-place inputs and are retained explicitly.',
        'All completed v0.9 coarse-rank, local parameter, harmonic and shifted-height targets have been removed from the active frontier.',
        'The six final navigation anchors leave the four global_branches_unchanged records exactly unchanged; no global arithmetic or RH/Dirichlet-GRH completion is asserted.',
        'source_connections are lexical navigation hints, not extra checked ranges or theorem claims.',
    ],
    'targets':targets,
    'source_files':[{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()],
    'validation':{'all_source_bytes_equal_pin':True,'all_range_hashes_rechecked':True,
                  'old_global_branch_values_unchanged':True,
                  'previous_map_sha256':sha256(OLD_PATH.read_bytes()).hexdigest()},
    'previous_global_branches_source':'output/RH_reconstruction_v0_9/next_source_targets.json',
    'global_branches_unchanged':deepcopy(old['global_branches_unchanged']),
}
assert out['global_branches_unchanged'] == old['global_branches_unchanged']
rendered = json.dumps(out,ensure_ascii=False,indent=2)+'\n'
marker = '  "global_branches_unchanged":'
assert old_raw[old_raw.index(marker):] == rendered[rendered.index(marker):], 'global branch suffix changed'
(HERE/'next_source_targets.json').write_text(rendered)
print(json.dumps({'targets':len(targets),'source_files':len(files),
                  'global_branches':len(out['global_branches_unchanged']),
                  'global_branch_suffix_preserved_verbatim':True,
                  'verified_commit':PIN,'output_sha256':sha256(rendered.encode()).hexdigest()},indent=2))
