from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'lean_source'
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'

def sha(b):
    return hashlib.sha256(b).hexdigest()

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip() == COMMIT

decl_re = re.compile(r'^(?:(?:private|protected|noncomputable|unsafe)\s+)*(?:def|abbrev|theorem|lemma|structure|class|instance)\s+')
cache = {}

def source(path, start, stop=None, role='Exact source contract or comparison reconstructed in the human proof'):
    path = 'src/' + path
    if path not in cache:
        b = (SOURCE / path).read_bytes()
        pinned = subprocess.check_output(['git', 'show', COMMIT + ':' + path], cwd=SOURCE)
        assert b == pinned, path
        cache[path] = (b, b.decode().splitlines(keepends=True))
    b, lines = cache[path]
    found = [i for i, s in enumerate(lines) if start in s]
    assert len(found) == 1, (path, start, found)
    a = found[0]
    if stop is None:
        z = next((i for i in range(a + 1, len(lines)) if decl_re.match(lines[i])), len(lines))
    else:
        z = next(i for i in range(a + 1, len(lines)) if stop in lines[i])
    while z > a and not lines[z - 1].strip():
        z -= 1
    block = ''.join(lines[a:z]).encode()
    name = start.split(' ', 1)[1].split(' ')[0].split('(')[0].rstrip(':') if ' ' in start else start
    return {
        'path': path, 'declaration': name, 'source_spelling': start,
        'line_start': a + 1, 'line_end': z,
        'sha256': sha(b), 'range_sha256': sha(block), 'range_bytes': len(block),
        'first_line': lines[a].rstrip(), 'role': role,
        'verified_equal_to_pinned_git_blob': True,
        'url': f'{REPO}/blob/{COMMIT}/{path}#L{a+1}-L{z}',
    }

AM = 'Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
IW = 'Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
GI = 'Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
TP = 'Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/'
HF = 'Formalism/LocalToGlobal/NormalizedHeckeFactors/'
NS = AM + 'RingSpecNormalisedCharacterEq.lean'
TR = IW + 'TwistDataAgreeAcrossCoefficientsLocalized.lean'

S = {
 'selection': source('Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ColumnCompatibleSelection.lean', 'def zsc ', 'end GlobalTheory.Fc'),
 'selection_types': source('Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ColumnCompatibleSelection.lean', 'abbrev BaseLevelCompatibleSelection ', 'def EvSel '),
 'selI': source('Formalism/LocalToGlobal/TieTwRecOf.lean', 'def selKOf ', 'def OneMapOf '),
 'wire': source(GI+'WireSel.lean', 'theorem GlobalTheory.Top.wire_sel'),
 'linkalt': source(GI+'LinkAlt.lean', 'theorem GlobalTheory.Top.link_alt'),
 'shape': source('Development/AutomorphicArithmetic/CharacterBoxes/ShapeWin.lean', 'theorem UpperTheory.Top.shapeWin'),
 'locnd': source(AM+'LocAutHodgeTateWeightsLevelZeroDef.lean', 'def LocNd.nd '),
 'loctw': source(AM+'LocAutHodgeTateWeightsLevelZeroDef.lean', 'def LocTw.ntw '),
 'loclay': source(AM+'LocAutHodgeTateWeightsLevelZeroDef.lean', 'def LocAll.lay '),
 'fixZ': source(AM+'NStageTrivialCharacterCoeffEqAlt.lean', 'def NLay0.setZ ', 'theorem NLay0.ZOk.reEta'),
 'eta': source(AM+'NStageTrivialCharacterCoeffEqAlt.lean', 'def NLay0.eta '),
 'setN': source(AM+'NStageTrivialCharacterCoeffEqAlt.lean', 'def setRaw ', 'def setK '),
 'localcopied': source(NS, 'def withLoc ', 'end Loc'),
 'nth': source('Formalism/SharpRestriction/LevelLetterCocycles/DataN.lean', 'structure NTh ', 'end Formalism.BasicNotions'),
 'nchoice': source('Formalism/LocalRingCardinality/DataNChoice.lean', 'structure NChoice '),
 'coverdefs': source(HF+'CoverAlg.lean', 'def W ', 'theorem cls_isMaximal'),
 'coverspan': source(HF+'CoverAlg.lean', 'theorem exists_pt ', 'theorem pow_sub_apply_eq_zero'),
 'nlocbase': source(HF+'HeckeStdTwOfStd.lean', 'structure NLocBase ', 'attribute [instance] NLocBase'),
 'std': source(HF+'HeckeStdTwOfStd.lean', 'def HeckeStd ', 'def LocPl '),
 'ndspec': source(NS, 'structure NdSpec ', 'structure AutSpec '),
 'autspec': source(NS, 'structure AutSpec '),
 'coverproof': source(HF+'CoverThm.lean', 'theorem finite_chooseBasisIndex ', 'end Formalism.L2'),
 'covercontract': source('Formalism/SharpRestriction/LevelLetterCocycles/LocsCoverTw.lean', 'def LocsCoverTw '),
 'openwithloc': source(TP+'HeckeOpenWithLoc.lean', 'theorem heckeOpen_withLoc_alt'),
 'nbuilt': source(NS, 'structure NBuilt '),
 'ntrue': source(NS, 'structure NTrue '),
 'ntrueconstructor': source(TP+'RowsAtStart.lean', 'def nTrueAtWeight '),
 'linketa': source('Formalism/SharpRestriction/GlobalTheoremInputs.lean', 'def LinkEta '),
 'familycover': source(HF+'CoverF.lean', 'theorem locsCoverTwF_of '),
 'genericeta': source(GI+'LinkEta.lean', 'theorem GlobalTheory.Top.link_eta '),
 'etaclosed': source(HF+'EtaClosed.lean', 'theorem linkEtaTw_closed ', 'theorem etaN_eq_etaJ'),
 'ratin': source(NS, 'def goodL ', 'structure TwNew '),
 'sideb': source(NS, 'structure SideB '),
 'choiceside': source(NS, 'structure ChoiceSide '),
 'nrow': source(AM+'RatInEig.lean', 'structure NAt ', 'abbrev NExt '),
 'originaloperator': source(TR, 'def sameL ', 'theorem fitsL '),
 'nrowconstructor': source(TP+'RowsAtStart.lean', 'def normalizedRowDatum ', 'theorem nonempty_nMore_of_xdAll '),
 'atconstructor': source(TP+'RowsAtStart.lean', 'def weightedAtData ', 'def localAtData '),
 'expstates': source(AM+'RootsOfUnityRingLeWittIntegers.lean', 'def Reads ', 'structure StA '),
 'actualstates': source(AM+'RootsOfUnityRingLeWittIntegers.lean', 'structure SettingsFormsState ', 'structure NMore '),
 'theta_original': source(TR, 'theorem geoL ', 'theorem sameGaloisL '),
 'kept': source(TR, 'theorem sameGaloisL ', 'def xdD '),
 'setup': source(IW+'SetupLGood.lean', 'def twL ', 'end GlobalTheory.HeightCounting.Fin3'),
 'sertransport': source(IW+'SeriesAtOfExpRelation.lean', 'private theorem gens_eq ', 'end GlobalTheory.HeightCounting.Fin3'),
 'serconclusion': source(IW+'SeriesAtOfExpRelation.lean', 'theorem _root_.GlobalTheory.T.series_at_of_exp_relation '),
 'serat': source(AM+'SubsetTwistExceptionalPlaces.lean', 'structure SerAt ', 'def XdAll '),
 'scalar': source('Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/ExistsIsScalar.lean', 'structure IsScalar ', 'namespace ExportTie'),
 'celltie': source('Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/GoodSetupCountEqZeroOffBadPlaces.lean', 'structure CellTie ', 'def ActRead '),
 'fieldnumbers': source('Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/MemHalfCosetSelf.lean', 'structure NumbersIn ', 'theorem numbersIn_id '),
 'fieldnormalized': source('Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/MemHalfCosetSelf.lean', 'def SumsIn ', 'variable (σ) in', 'SumsIn and BottomIn already supply normalized monomial-integral rationality under integrability guards; rationalSums discharges guards and clears nonzero periods'),
 'fieldchoice': source('Development/AbelianVarietyTheory/Definitions/TwistedInnerProducts/MemHalfCosetSelf.lean', 'def FieldIn ', 'end Choice'),
}

claims = [
 ('LTD1', 'One literal Bundle gives all selected global objects', [],
  ['selection','selection_types','selI','wire','linkalt','shape'],
  ['Actual RawSel Bundle on the selected class; bundle/design production is not asserted'],
  'For every class and actual raw bundle selection, every Fm in the class, x>Fm.x1 and original i; the selection threshold is Fm.x1.'),
 ('LTD2', 'Local installation preserves the original form/theta/choice maps', [],
  ['locnd','loctw','loclay','fixZ','eta','setN','localcopied','nth','nchoice','kept'],
  ['Actual initial D and LocAll; any substantive theta identity must be supplied on the preserved original maps'],
  'For every D and every L:LocAll(lay0 D); every original MtFam, NChoice, CharFrame and TupTied. etaJ and local fields are explicitly updated.'),
 ('LTD3', 'Integral simultaneous generalized eigenblocks give full residual coverage', [],
  ['coverdefs','coverspan'],
  ['Finite-dimensional V; possibly infinite pairwise commuting split family; every occurring generalized eigenvalue in the fixed DVR'],
  'All finite-dimensional K-spaces including zero, all possibly infinite commuting generator sets. Dimension/intersection statements apply to every finite set containing every maximal ideal.'),
 ('LTD4', 'Actual NdSpec gives LocsCoverTw and joint injectivity', ['LTD2','LTD3'],
  ['nlocbase','std','ndspec','autspec','coverproof','covercontract','openwithloc'],
  ['Actual NdSpec on the same D,L,M,C; its std, split, mx enumeration, Psi and Psi_pr are retained premises'],
  'For every 1<=j<=m and every original w with muAt(w)!=mu0; all original local projection maps. AutSpec is unnecessary for coverage/injectivity.'),
 ('LTD5', 'NBuilt implies literal LinkEta with the original family thresholds', ['LTD4'],
  ['nbuilt','ntrue','ntrueconstructor','linketa','familycover','genericeta','etaclosed'],
  ['Pointwise NBuilt on the actual final datum; for LinkEta, one threshold followed by every x and original i'],
  'For every supplied NBuilt(hLL,Dprime), LocsCoverTw(Dprime). If exists x0 forall x>=x0 forall i exists NBuilt(hLL,Fm.D x i), LinkEta(Fm), without changing x0 except if producer requires x>Fm.x1.'),
 ('LTD6', 'Original row spectrum and normalized Hecke operators transport exactly', ['LTD2'],
  ['ratin','sideb','choiceside','nrow','originaloperator','nrowconstructor','atconstructor'],
  ['One actual St P and compatible LC; RatIn.span and hL_int; actual YRel when final row reading is used'],
  'Original rank-r row operators: 1<=j<=m, k<=r and specified split/avoidance conditions, with cHk^k. Distinct rank-nV ambient operators remain distinct. Denominator n may depend on j,k,v.'),
 ('LTD7', 'Existing theta evaluation and export series survive localization', ['LTD2','LTD6'],
  ['expstates','actualstates','theta_original','setup','sertransport','serconclusion','serat','scalar','celltie'],
  ['Actual LC containing original GeoTie.ThetaTie and SerAt; for new NExpTied Xprime the exact ExpRel including reads must be supplied'],
  'Every LocAll on the fixed original state; every NExpTied Xprime related by ExpRel; every admissible tuple, level, pointwise test and original scalar, including conditional rationality antecedents.'),
 ('LTD8', 'Field rationality transport uses the original embedding', [],
  ['fieldnumbers','fieldnormalized','fieldchoice'],
  ['Actual NumbersIn/FieldIn certificate; image containment in the original embedded field for FieldOK. Analytic FieldCond inputs remain separate.'],
  'For every prescribed choice and field embedding sigma with image in embLL; every original character, supported jet/expansion, phase, critical ratio and normalized bottom sum.'),
]

tex = (HERE / 'main.tex').read_bytes()
lines = tex.decode().splitlines(keepends=True)
out = {
 'schema':'rh-human-component-provenance/1','artifact_version':'0.31','date':'2026-11-22',
 'commit':COMMIT,'repository':REPO,'component':'local_theta_dictionary',
 'formal_correctness_assumed':True,'new_lean_replay':False,
 'main_tex_sha256':sha(tex),'claims':[],
}
for ident,title,deps,ss,inputs,quant in claims:
    a=next(i for i,s in enumerate(lines) if s.strip()=='% BEGIN '+ident)
    z=next(i for i,s in enumerate(lines) if s.strip()=='% END '+ident)+1
    block=''.join(lines[a:z]).encode()
    out['claims'].append({
     'id':ident,'title':title,'introduced_in':'0.31','classification':'B',
     'status':'Complete human proof of the exact conditional implication; producer premises retained',
     'scope':quant,'depends_on':deps,'remaining_inputs':inputs,'classical_inputs':[],
     'source_relation':'Exact original-object contract, with independent finite algebra or complete same-object transport proof',
     'proof_location':{'file':'local_theta_dictionary/main.tex','paragraph':ident,'label':'claim:'+ident,'line_start':a+1,'line_end':z,'sha256':sha(block),'bytes':len(block)},
     'sources':[S[k] for k in ss],
    })
(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

frontier = [
 {'id':'GLOBAL_LOCAL_THETA_BINDINGS','classification':'D','status':'strictly_reduced_not_closed',
  'closed_slices':['LTD1 exact Bundle projections','LTD2 original maps across LocAll/fixZ/reEta','LTD6 original row hL/eig/model identity and cHk^k normalization','LTD7 existing ThetaTie/SerAt transport through localization','LTD8 fixed-field containment transport'],
  'remaining':'Production at one original state of compatible LC/NChoice/ChoiceSide, theta evaluation, ExpRel, EMtTheta and actual toric/jet/period field data; classify substantive matched arguments as C when their original meaning is settled.'},
 {'id':'GLOBAL_LOCAL_COVERAGE','classification':'B','status':'consumer_closed_from_actual_NBuilt_producer',
  'proved':'NBuilt(hLL,Dprime) -> LocsCoverTw(Dprime); one eventual family of these certificates -> LinkEta',
  'proofs':['LTD3','LTD4','LTD5'],
  'remaining':'Actual common-model NBuilt/NdSpec existence remains C. Generic TSel alone is not claimed to carry NBuilt; concrete construction certificate must be retained before forgetting it.'},
 {'id':'GLOBAL_ACTUAL_ROW_SPECTRUM','classification':'C','status':'producer_open_identity_transport_closed',
  'proved':'Exact same row hL/eig/theta-character/rational lattice under localization, with cHk^k in coefficient action',
  'proofs':['LTD6'],
  'remaining':'Original RatIn.span and hL_int and actual row reading/common geometric state; no uniform denominator exponent or equality with rank-nV ambient Hecke family is inferred.'},
]
closure={
 'schema':'rh-local-theta-closure/1','version':'0.31','source_commit':COMMIT,
 'main_tex_sha256':sha(tex),'claim_count':len(claims),'claim_ids':[c[0] for c in claims],
 'formal_correctness_assumed':True,'new_lean_replay':False,
 'classification_legend':{'A':'Specific published theorem with all hypotheses matched','B':'Complete elementary/moderate human implication with its premises explicitly retained','C':'Substantive original producer requiring reconstruction','D':'Human source/meaning identification still unresolved; never a claimed formal gap'},
 'frontier_effect':frontier,
 'same_object_keys':['same raw Bundle and FamP','same St P and LC','same Dprime=withLoc L','same tuple pack cf,C,tp','same original MtL and prMt','same rank-r row hL and eigenvalues','same prescribed cHk^k','same theta evaluation maps and nonzero scalar','same actual embedded coefficient field'],
 'source_checks':{'all_files_equal_to_pinned_git_blobs':True,'files_checked':len(cache),'anchors':len(S)},
 'validation':{'tex_syntax_draftmode_exit_code':0,'pdf_rendered':False,'new_lean_replay':False},
}
(HERE/'closure.json').write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n')

loc=['LTD source locators — pinned commit '+COMMIT,'All cited working-tree files equal their pinned Git blobs. No Lean replay.','']
for ident,_,_,ss,_,_ in claims:
    loc.append(ident)
    for key in ss:
        a=S[key]
        loc.append(f"  {a['declaration']} | {a['path']}:{a['line_start']}-{a['line_end']}")
        loc.append('  '+a['url'])
        loc.append('  file_sha256='+a['sha256']+' range_sha256='+a['range_sha256'])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
print(json.dumps({'claims':len(claims),'anchors':len(S),'source_files':len(cache),'main_tex_sha256':sha(tex)},indent=2))
