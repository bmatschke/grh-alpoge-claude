"""Build the v0.12 continuation map without asserting a new theorem.

Validate exact pinned declaration ranges and retain the four v0.11 global
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
OLD_PATH = BASE/'output/RH_reconstruction_v0_11/next_source_targets.json'
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
            qualified=m[1][7:] if m[1].startswith('_root_.') else (ns+'.'+m[1] if ns else m[1])
            declarations.append((m[1],i,qualified))
    assert all(kind == 'section' and label is None for kind,label in stack), (path,stack)
    info = {'path':path,'sha256':sha256(raw).hexdigest(),
            'full_file_sha256':sha256(raw).hexdigest(),'bytes':len(raw),
            'line_count':len(lines),'verified_equal_to_pinned_git_blob':True,
            '_lines':lines,'_declarations':declarations}
    files[path] = info
    return info

def add(stage,path,name,role,remaining,connections=(),branch=None):
    f = source(path)
    hits = [d for d in f['_declarations'] if d[0] == name or d[2] == name or d[2].endswith('.'+name)]
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


AB = 'src/Development/AbelianVarietyTheory/'
AI = AB+'Proofs/GlobalInterpolation/'
AW = AB+'Definitions/GlobalTwisting/'
IW = AB+'Proofs/IwasawaDecomposition/'
TF = LT+'GroupLattices/TiedFamilies/'
CM = LT+'GroupLattices/ComparisonMaps/'
WL = GB+'IntegralWeylLatticeSpan/'
HG = 'src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/'
IG = HG+'InertiaGaloisSymmetry/'
MS = AA+'MeanSquareBounds/'
CB = AA+'CharacterBoxes/'

def target(group,path,name,role,remaining,connections=()):
    add(group,path,name,role,remaining,connections)

# LI supplies actual places, embeddings, arbitrary local frames and the away
# character. The stronger global frame and actual comparison are still next.
target(1,IW+'TrueColumnSpacesStandardInFrameCoords.lean',
       'GlobalTheory.Mem.Col2.TC.spaces_in_coordinates',
       'Actual global-model supplier of StdTied and the standard integral coordinates.',
       'Reconstruct the orthonormal frame and integer-coordinate assertions for the actual TC.rec7 datum under its Ok, Pins, Laws and Later premises. Supply these premises from the same global construction; LI5 alone only gives independent local frames.',
       ['HermitianColumns/ZeroPointScaledByCharacter.lean:StdTied',
        'TrueColumnSpacesStandardInFrameCoords.lean:Crd.Ortho.isStd',
        'TieStd.lean:exists_stdB_of_tied'])
target(1,LT+'HermitianColumns/ZeroPointScaledByCharacter.lean','BaseTied',
       'Exact companion-lattice identity required for a common global frame.',
       'Supply the actual BaseTied identity, including the level-zero lattice and its conjugate-character multiple of the dual, for the same global columns. Do not replace this global input by a local abstract isomorphism.',
       ['CompanionOfBaseTied.lean:companion_of_baseTied',
        'ExistsStandardColumnComparisonsTrueColumns.lean',
        'ExistsGIs.lean:companion_of_colsHermS'])
target(1,TF+'TieStd.lean','stdB_core',
       'Construct the global matrix B from the supplied orthonormal integral basis.',
       'Prove the exact Gram identity and inverse-matrix integral-coordinate criterion, including the actual rank reindexing, and then specialize the previous global-model input.',
       ['TieStd.lean:exists_stdB','TieStd.lean:exists_stdB_of_tied'])
target(1,TF+'CompanionOfBaseTied.lean','locIdStd',
       'Replace LI local frames by base changes of one global B.',
       'Use L contained in L0 contained in its dual and T times the dual contained in L; p not dividing T makes their projected local lattices equal. Check that iw, places and position compatibility stay unchanged.',
       ['CompanionOfBaseTied.lean:T_smul_mem','CompanionOfBaseTied.lean:companion_le',
        'CompanionOfBaseTied.lean:LocId.withFr','CompanionOfBaseTied.lean:locIdStd_iw'])
target(1,IW+'CharZeroOfSetting.lean','d_eq_of_classes',
       'Rank formula from the actual level-orbit representatives and Weyl lattices.',
       'Expand the finite class-orbit argument, actual HtupW bases and trivial-stabilizer premise. Reuse CB/BC only after matching the literal dual-Weyl and tensor conventions.',
       ['CharZeroOfSetting.lean:exists_basis_Dl0','CharZeroOfSetting.lean:exists_basis_HtupW',
        'TrivialTransfer/GramTotallyDefinite.lean:trivStabU_rec'])
target(1,CM+'ClsRec.lean','clsR_iff',
       'Identify global class labels with the actual local lattice-tuple orbits.',
       'Prove both the equality criterion and its accompanying clsR_surj surjectivity using the literal level and hyperbolic-place data, rather than assuming a bijection of abstract label sets.',
       ['ClsRec.lean:clsR_surj','CharZeroOfSetting.lean:locPack_d_eq'])
target(1,IW+'CharZeroOfSetting.lean','locPack_d_eq',
       'Specialize the rank formula to the actual local package and global forms.',
       'Match the class bijection, trivial stabilizers, finite tensor/tableau dimensions and the supplied Forms0 level-zero forms dimension for the original D7 and its source position map. This supplies pack_d_eq only after these substantive joins; its exported Joint0 argument is unused in the rank proof and is not an additional rank premise.',
       ['CharZeroOfSetting.lean:pack_d_eq','CharZeroOfSetting.lean:d_eq_of_classes',
        'GlobalTheory/CoordinateLengths/DuCount.lean:finrank_forms_level_zero',
        'ComparisonMaps/ClsRec.lean:clsR_iff','ComparisonMaps/ClsRec.lean:clsR_surj'])
target(1,WL+'IntSpanGSmul.lean','valIntAt_of',
       'Actual integral polynomial-value criterion behind ValIntRec.',
       'Identify the global integral Weyl span with the literal even/odd local coefficient lattices, using the same coefficient embeddings and frames. Expand WeylLatticeDescent and the local lattice/Gram suppliers; BC scalar extension alone does not give this criterion.',
       ['IntSpanGSmul.lean:valIntRec_of','WeylLatticeDescentOfIntegralModels.lean',
        'WeylLatticeDescentHolds.lean:oddFact_pf','SelfDualCongr.lean:latW_gen',
        'SelfDualCongr.lean:gramW_gen'])
target(1,WL+'ColSpanMulUnit.lean','latO_of',
       'Odd-position integral lattice transport with the Gram correction.',
       'Prove the exact inverse-transpose and conjugation identity, including the integral invertible Gram factor and determinant twist. Preserve LI4/LI6 parity and the actual local-frame normalization.',
       ['ColSpanMulUnit.lean:restLatO_of','ColSpanMulUnit.lean:restExB',
        'ColSpanMulUnit.lean:restChi_of','SelfDualCongr.lean:restGramW_of'])
target(1,TF+'TieSurj.lean','surjRat_pf',
       'Rational surjectivity of the actual comparison map.',
       'Reconstruct injectivity on the original global basis, point separation, rational-valued descent and the dimension argument using the just-established exact rank equality. The actual evaluation maps must be retained.',
       ['TieSurj.lean:cmpLin_mem_span','TieSurj.lean:card_eq_d',
        'TieLat.lean:cmpRec_lat_pf','TieLat.lean:latM_pf'])
target(1,TF+'TieWeak.lean','weak_of_locAt',
       'Weak approximation for the same local places and coefficient valuations.',
       'Use the LI place bijection and valuation dictionary to prove the actual simultaneous approximation and integral-intersection statements; preserve distinctness of all places and the original coefficient-field maps.',
       ['TieWeak.lean:weakRec_pf','TieWeak.lean:latM_rec\''])
target(1,TF+'TieLatFin.lean','comparison_lattice_span_eq',
       'Final literal equality of global comparison span with local M.',
       'Assemble ValIntRec, rational surjectivity, finite generation and weak approximation into the actual O-span equality. This endpoint is navigation to the preceding substantive tasks, not a replacement for their proofs.',
       ['TieLat.lean:latM_pf','TieLat.lean:mRatSpan_rec','TieSurj.lean:surjRat_pf',
        'TieWeak.lean:weakRec_pf','ExistsEmbeddingOfRingTie.lean:comparison_statements'])

# HW and HC transport properties of points; they do not construct the points.
target(2,AW+'ValidForConstructedPointClassesEventuallyWorking.lean','ObjCP',
       'Literal all-pairs/all-positions point-construction interface.',
       'Preserve the nested constant and threshold quantifiers and produce Val, HostArith, From, CanonInst and the requested point duties for every admissible degree pair and distinguished position. The informal label pointObjCP is not a source declaration.',
       ['ValidForConstructedPointClassesEventuallyWorking.lean:RecExP',
        'CharacterBoxes/KitS.lean:kitS'])
target(2,AI+'ExistsObjectsOfAdmissibleTwistDatum.lean','objCP_and_of_recExP',
       'Substantive assembly of actual points from recursive objects.',
       'Expand the actual RecExP and LevelPrime suppliers, compatible size data, LedPart construction, tame/Minkowski/twist data and the all-u0 output. Do not infer point existence from the record type or from HC host supply.',
       ['ObjCOfRecExObjO.lean:objC_of_recEx','ExistsObjectsOfAdmissibleTwistDatum.lean:objCP_of_recExP',
        'ExistsLedPart.lean:exists_ledPart','ExistsObjectsOfAdmissibleTwistDatum.lean:ObjCP.and_q0Pt'])
target(2,AI+'ExistsLedPart.lean','exists_ledPart',
       'Construct the actual selected global lattice and canonical local data.',
       'Prove the refill and global lattice-gluing inputs and their RecOK/LedOK compatibility. Track the chosen NuLat, ramification-normalized lengths, canonical kappa/exponent data and their equality with the original point parameters.',
       ['ExistsLedPart.lean:exists_lat','ExistsLedPart.lean:setLat',
        'GlobalTheory.Refill.exists_refill','GlobalTheory.EX.Led.LedOK'])
target(2,AI+'ExplicitConstantsParameterConditionsLarge.lean','explicitConstants_parameterConditions_large',
       'Actual uniform parameter-choice supplier used by NumAt.',
       'Derive every ParameterChoice field from the supplied global Val/HostArith data with the literal constant order; expand node, gap, word, cloud, conductor and type-prime inequalities rather than treating this conjunction assembly as a proof.',
       ['SzRowNodeGapBlockLength.lean:nodeGap_blockLength_poly',
        'SzRowNodeGapBlockLength.lean:szRow_nodeGap_blockLength',
        'SzRowElevenLeSplitBound.lean:szRow_sizesAt',
        'BandWidthLeInvSqOfRankBounds.lean:szRow_band_lambda_primes'])
target(2,AI+'SzRowNumAt.lean','szRow_numAt',
       'Supply NumAt, ChTT_at and ChCode_at for the constructed point.',
       'Assemble the preceding parameter choices with actual block-length, size and band estimates and check each literal NumAt field. Earlier GI/GII local HypI/HypII bounds do not by themselves establish this stronger record.',
       ['InertJacobiLevels/AsmIface.lean:NumAt',
        'ExplicitConstantsParameterConditionsLarge.lean:explicitConstants_parameterConditions_large',
        'SzRowNodeGapBlockLength.lean:szRow_blockLengthParams',
        'SzRowElevenLeSplitBound.lean:szRow_sizesAt'])

# HC closes downstream joins conditional on these arithmetic/analytic suppliers.
target(3,CB+'FieldChi.lean','UpperTheory.Top.fieldChi',
       'Actual general-character field and HostAx with FieldRows.',
       'Construct the prescribed cyclotomic/character field and prove its Galois, conductor, kept-character, KerChi and TwistForm data. HC10 supplies the later window and host assembly only after this field theorem.',
       ['InertiaGaloisSymmetry/AnyLevel.lean:AnyGrp.host','CharacterBoxes/OrdAny.lean:ordAny',
        'CharacterBoxes/KerChiAny.lean:kerChiAny','CharacterBoxes/TwistAny.lean:twistAny'])
target(3,IG+'AnyFrame.lean','charData',
       'Underlying character-group Artin map and actual HostRaw construction.',
       'Expand the frame and Artin-map construction, CRT surjectivity and conjugation/quadratic identities, then the fixed-field realization used by AnyGrp.host. Keep mixed odd and two-primary character data, not only the ordinary cyclic case.',
       ['AnyFrame.lean:art_surj','AnyFrame.lean:host','AnyLevel.lean:AnyGrp.host',
        'OfCharLevel.lean','CharData.toHostRaw'])
target(3,IG+'OfRawToHostRaw.lean','HostRaw.der',
       'Exact list of arithmetic HostDer obligations behind HostAx.ofRaw.',
       'Reconstruct its substantive suppliers: Frobenius/inertia and decomposition, CM fixed fields, integral different and trace-duality, discriminant bounds and root-of-unity norms. The displayed record construction is only a dependency map; it does not prove those suppliers by itself.',
       ['CycAll.lean:Der.hostCore','KcDiff.lean:diffSupport','KcDiff.lean:principal',
        'KcDiffSmulMem.lean:unimodular','RdDiff.lean','OfRawToHostRaw.lean:HostAx.ofRaw'])
target(3,IG+'KcDiff.lean','principal',
       'Actual conjugate half-different ideal and its coprimality.',
       'Prove the required different-support and prime-pairing facts, construct the ideal b with different=b*conj(b), and retain the exact coprimality and norm conclusions consumed by the host lattice construction.',
       ['KcDiff.lean:diffSupport','KcPair.lean:kc_not_dvd_different',
        'OfRawToHostRaw.lean:HostRaw.der'])
target(3,IG+'KcDiffSmulMem.lean','unimodular',
       'Trace-duality of the actual inverse half-different lattice.',
       'Identify the literal fractional ideal and conjugated trace pairing, proving both directions of its integral-dual equality. Do not infer this actual metric/lattice input from an abstract unimodular model.',
       ['KcDiffSmulMem.lean:kc_mem_diff_iff','KcDiffSmulMem.lean:kc_diff_smul_eq',
        'KcDiff.lean:principal'])
target(3,AI+'ExistsRanksRankValFrame.lean','exists_ranks_rankVal_frame',
       'Uniform integer/parity rank construction over the supplied Frame.',
       'Construct the even k,m and the literal t/r parameters while preserving the original Frame, then prove every RankVal clause. HC7 bounds supplied ranks but HC10 still requires this existence theorem.',
       ['ExistsRanksRankValFrame.lean:exists_even_between',
        'ExistsRanksRankValFrame.lean:exists_ranks_of_frame',
        'CoprimeRanks/AdmChi.lean:admissibleClassesTwistedChar'])
target(3,AI+'NormPrimesImagQuadShortIntervalLowerBound.lean','normPrimes_short_interval_lower',
       'ShortNorm: quantitative norm-prime count in the required short intervals.',
       'Expand the weighted prime-ideal count, conversion to the literal norm-prime set and all uniform d,M,X,h constants. HC5 already converts this estimate into separated auxiliary primes; it does not prove the analytic estimate.',
       ['NormPrimesImagQuadShortIntervalLowerBound.lean:sum_lam_zero_le_card_normPrimes',
        'NormPrimesImagQuadShortIntervalLowerBound.lean:sqrt_le_short_main',
        'ShortNorms/ShortNorm.lean:ShortNorm'])
target(3,AI+'PrimesInProgressionsRelativeError.lean','primesRel_holds',
       'Analytic arithmetic-progression input for SmallOne.',
       'Reconstruct the uniform relative-error prime theorem and its modulus/range dependencies, then derive the polynomial least-prime bound through smallOne_of. HC5 only applies that bound.',
       ['ShortNorms/SmallOneOf.lean:smallOne_of','ShortNorms/ShortNorm.lean:SmallOne'])
target(3,MS+'Thin.lean','thin',
       'Uniform centered character-sum estimate behind ThinH.',
       'Prove the quantitative psi_thin and integrated-error estimates, including the real exceptional-zero condition, uniformly in the conductor bound and every y above the exponential cutoff.',
       ['PsiThin.lean:psi_thin','IntThin.lean:int_thin','GIntegral.lean:g_integral',
        'GaussSumFunctionEq.lean:thinH'])
target(3,MS+'SmallZeros.lean','small_zeros',
       'Finite-small-conductor zero separation used by ThinH.',
       'Prove the common positive zero-free margin at one for all nonprincipal primitive characters in the bounded conductor family, and combine it with the real-character conductor split without assuming GRH.',
       ['GaussSumFunctionEq.lean:thinH','realCond.lean:real_cond'])
target(3,MS+'PairShare.lean','pair_share',
       'Substantive abundance of simultaneous good auxiliary-prime pairs.',
       'Prove stage1 and stage2 bad-prime estimates and nonempty candidate sets with one common constant, including twisted centered sums, logarithmic derivatives and zero boxes. Preserve the q-then-d quantifiers; mere congruence existence is insufficient.',
       ['Stage1Succ.lean:stage1','CharOf.lean:stage2','PairExists.lean:pair_exists',
        'pairEx.lean:pairEx','CharacterBoxes/PairGood.lean:PairEx'])
target(3,AA+'AutomorphicVarieties/CMFieldExponentialBounds/AdmissibleOfPageN.lean','vwinAt_of_joint',
       'Concrete cohomological-window supplier for the retained VWinAt target.',
       'Expand JointWin and ThmBc, with their actual two-primary and odd-character cohomological counts, before deriving the uniformly quantified VVle interval. HC10 proves the later window rescaling, not these geometric/arithmetic inputs.',
       ['AdmissibleOfPageN.lean:vwin_of_joint','CMFieldExponentialBounds/logpair.lean',
        'CMFieldExponentialBounds/bigpair.lean','CMFieldExponentialBounds/minusle.lean',
        'CharacterBoxes/ExistsPageN.lean:VWinAt'])

# Preserve the six exact source leads and the four independent branch values.
retained = [t for t in old['targets'] if 'unchanged_global_branch_index' in t]
assert len(retained) == 6, len(retained)
retained_anchor_keys = ('path','declaration','source_spelling','line_start','line_end',
                       'sha256','full_file_sha256','range_sha256','range_bytes',
                       'url','pinned_url','first_line','declaration_lines_within_range',
                       'unchanged_global_branch_index')
for prior in retained:
    add(4,prior['path'],prior['source_spelling'],prior['role'],prior['remaining_human_scope'],
        prior.get('source_connections',()),branch=prior['unchanged_global_branch_index'])
    for key in retained_anchor_keys:
        assert targets[-1][key] == prior[key], (key,prior['path'])

public_files = [{k:v for k,v in f.items() if not k.startswith('_')} for f in files.values()]
groups = {
 '1':'Common global frame, actual class-rank equality and integral comparison lattice.',
 '2':'Actual all-pairs point construction and the stronger NumAt parameter record.',
 '3':'Underlying character field/HostAx, half-different, rank existence and analytic prime/window suppliers.',
 '4':'Four unchanged independent global branches, with six revalidated source leads.'
}
group_counts = {k:sum(t['priority_group']==int(k) for t in targets) for k in groups}
result = {
 'version':'0.12','commit':PIN,'head_verified':head,
 'status':'Continuation map only; no additional reconstructed theorem is asserted by any target record.',
 'target_count':len(targets),'source_file_count':len(files),
 'count_policy':'All exact target ranges, including six retained leads for four unchanged global branches.',
 'line_range_convention':'Inclusive, one-indexed, exact original bytes.',
 'completed_previous_frontier':
   'BO proves nonconstant forced-point orbit estimates; BS simultaneous biased shares/bad-mass selection; HC downstream host/point transports and conditional host joins, separate thick T2 construction, and auxiliary-prime selections under named analytic inputs; LI actual local places/completions, arbitrary local frames, aligned embeddings and the integral away-character under its stated host/level/rationality hypotheses.',
 'next_local_priority':
   'Supply the common global standard frame and companion identity, actual pack_d_eq and comparison-lattice span; construct the points/NumAt and the still-retained host-field and analytic suppliers for that same family.',
 'priority_groups':groups,'priority_group_counts':group_counts,
 'removed_completed_targets':[
   'ThickFrames/orbitTerms.lean:orbit_terms',
   'ThickFrames/select.lean:select',
   'ThickFrames/SharesOfCounts.lean:shares_of_counts',
   'ThickFrames/topsGroup.lean:topsGroup',
   'ThickFrames/topsFrame.lean:topsFrame',
   'ThickFrames/topsBase.lean:topsBase',
   'ThickFrames/topsChoiceH.lean:topsChoiceH',
   'IwasawaDecomposition/ExistsLocIdOfCompletions.lean:exists_locId_of_completions',
   'IwasawaDecomposition/AddCharIsIntegral.lean:exists_psi'
 ],
 'precision_notes':[
   'Completed statements keep their literal hypotheses. In particular HC does not construct HostAx, ShortNorm, SmallOne, ThinH, PairEx or VWinAt merely by consuming their named interfaces.',
   'The biased TT subset and the separate integer shift set T2 are different constructions; neither remains a probability/counting target in this map.',
   'LI gives the actual place bijection, first-projection lattice frames and coefficient/complex alignment. A common global B and actual class-rank/comparison lattice are stronger remaining tasks.',
   'The actual rank proof locPack_d_eq uses Forms0, LocId, the class bijection and trivial stabilizers. The exported pack_d_eq wrapper ignores its Joint0 argument; Joint0 remains relevant to other comparison and character statements, not a new rank assumption.',
   'Use the same embRec, source orbRep positions, c^s parity and p-normalized valuations throughout the comparison. The integral away-character still requires the stated level-zero rationality input.',
   'CoverAll is optional. The active degree-realization route is HostWW/KitS/ChosenWall, reconstructed in HW; actual point supply remains necessary.',
   'No source declaration literally named pointObjCP was found; ObjCP and objCP_and_of_recExP are the precise point-construction targets.',
   'The ordinary o=1 host-only specialization avoids VWinAt in that host theorem. It does not prove the general cohomological window, the linked-family comparisons or a global RH/GRH conclusion.',
   'The four inherited global branch records are preserved as exact JSON values. No theta, spectral, metric, cohomological or analytic prime-window input is inferred from finite local results.'
 ],
 'targets':targets,'source_files':public_files,
 'validation':{
   'all_source_bytes_equal_pinned_git_blobs':True,
   'all_declaration_anchors_and_inclusive_range_hashes_checked':True,
   'retained_source_lead_count':6,
   'all_retained_source_lead_anchor_fields_identical_to_predecessor':True,
   'global_branch_records_identical_to_predecessor':True,
   'no_new_proof_claim_by_target_map':True,
   'no_lean_build_or_kernel_replay':True
 },
 'previous_global_branches_source':{
   'path':str(OLD_PATH.relative_to(BASE)),
   'sha256':sha256(OLD_PATH.read_bytes()).hexdigest()
 },
 'global_branches_unchanged':deepcopy(old['global_branches_unchanged'])
}
assert len({(t['path'],t['line_start'],t['line_end']) for t in targets}) == len(targets)
assert 25 <= len(targets) <= 35, len(targets)
assert len(result['global_branches_unchanged']) == 4
assert result['global_branches_unchanged'] == old['global_branches_unchanged']
out = HERE/'next_source_targets.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
written = json.loads(out.read_text())
assert written['global_branches_unchanged'] == old['global_branches_unchanged']
# Both generations serialize this last field identically; check that as well
# as semantic JSON equality so accidental reformatting is visible.
suffix_marker = '  "global_branches_unchanged": '
assert out.read_text().split(suffix_marker,1)[1] == old_raw.split(suffix_marker,1)[1]
print(json.dumps({'targets':len(targets),'source_files':len(files),
                  'priority_group_counts':group_counts,'retained_leads':6,
                  'unchanged_global_branches':4,'all_pinned_checks_passed':True}))

