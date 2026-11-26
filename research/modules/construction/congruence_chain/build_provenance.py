#!/usr/bin/env python3
"""Rebuild LN1--LN10 exact proof/source locators, verifying pinned Git bytes."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, default=HERE.parents[1]/'lean-source')
REPO = p.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
I = 'src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/'
H = 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/HeckeGaloisCriteria/'
T = 'src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/'
N = 'src/Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/'
L = 'src/Formalism/SharpRestriction/LevelLetterCocycles/'
R = 'src/Development/AutomorphicArithmetic/ResidueCharacters/'
Y = 'src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/'
U = 'src/Development/AutomorphicArithmetic/CyclotomicBounds/'
F = 'src/Formalism/SharpRestriction/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}

def source(path, spelling):
    raw = (REPO/path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if m:
            starts.append((n, m.group(1)))
    hits = [n for n, s in starts if s == spelling]
    if len(hits) != 1:
        raise ValueError((path, spelling, hits))
    start = hits[0]
    end = min([n for n, _ in starts if n > start], default=len(lines)+1)-1
    while end > start and not lines[end-1].strip():
        end -= 1
    block = b''.join(lines[start-1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                   'lines': len(lines), 'url': f'{BASE}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start-1].decode().rstrip('\n'),
            'url': f'{BASE}/blob/{PIN}/{path}#L{start}-L{end}',
            'role': 'Exact definition, corresponding proved endpoint, or explicitly retained input; see claim scope and input ledger.',
            'verified_equal_to_pinned_git_blob': True}

spec = {
'LN1': {
 I+'TraceMemAdjoin.lean': ['trace_mem_adjoin','trace_lmul','centralIdemCoeff'],
 I+'CardMulIdemFromCenter.lean': ['exists_central_lift','card_mul_idem_from_center'],
 I+'CentralElementsFromIdempotentCoeffs.lean': ['main'],
 L+'PairedCharacterCondition.lean': ['Pend'],
 L+'DataN.lean': ['NData','e0'],
 N+'StepJumpDirect.lean': ['CentralElt'],
 H+'ExistsUnitOneAddGenerator.lean': ['exists_unit_one_add_generator'],
},
'LN2': {
 H+'RhoBar.lean': ['Tie4','CutD','CutD.Good'],
 T+'ExistsGood.lean': ['exists_good_alt'],
 T+'EigenActionAtGoodPoint.lean': ['onMt_e0_eq_self_of_mem_zgood_and_eq_zero_of_notMem'],
 H+'ExistsUnitOneAddGenerator.lean': ['exists_tuple','exists_type','tuple_labels','nc_of_type'],
 Y+'CardRootsBar.lean': ['om_gen_inj','om_pow','nc_of_roots','nc_of_label'],
 Y+'AutomorphicGaloisAdmissible.lean': ['Tm','Sqf','Nc'],
},
'LN3': {
 L+'DataN.lean': ['EigSpan','MtIn','eigSum','MtUp','MtLow','etaLoc'],
 H+'ActEqZeroOfQK.lean': ['cutT','outM','cutM','exists_sep','map_eig','mult_eq','iSup_eig','cutM_tf','cutM_free'],
 H+'LengthLeOfSpan.lean': ['decomp','qK_eq_zero_iff','length_ne_top'],
},
'LN4': {
 L+'DataN.lean': ['ccIdeal','ccAt','vcc'],
 H+'LengthLeOfSpan.lean': ['length_le_of_span'],
},
'LN5': {
 H+'LengthLeOfSpan.lean': ['length_le','lenUnit_le_add'],
 H+'IsHeckeGaloisIff.lean': ['eta_le','eta_zero','etaJ_le'],
 I+'ExistsTypeLocus.lean': ['lenUnit_natCast_le'],
 L+'DataN.lean': ['lenUnit','etaLoc','vcc'],
 R+'TwistedPlaces.lean': ['adm1'],
},
'LN6': {
 I+'GoodPointMultiplicityLeRankProof.lean': ['goodRows','dM_eq_sum','sum_mult_le','GlobalTheory.NLink.multLe_of_rank'],
 F+'AdmissibleParameterJoins/NandDIVb.lean': ['theta_injective_of_scalars','rank_at_place_eq_of_scalars','rank_uniform_over_places'],
 R+'TwistedPlaces.lean': ['adm2','adm3'],
 N+'BoundAtTwoThreeFamily.lean': ['MultLe'],
},
'LN7': {
 H+'EvPowLeExp.lean': ['sum_val_le','etaSum_le_add'],
 R+'TwistedPlaces.lean': ['admissibleMeanCondition_holds','ArchimedeanSignatureMatching','adm6','GeneratorPrimeEtaBound'],
 L+'MemPrimesOverOfMem.lean': ['etaSum_le'],
 U+'CyclotomicOrders/NuHost.lean': ['nuBudget','sum_nuL_le','nuBudget_le'],
 F+'GlobalTheoremInputs.lean': ['vvTerm','etaSum'],
},
'LN8': {
 R+'TwistedPlaces.lean': ['hB','jA','ordH','AdmT','ParametersPolynomiallyBounded','admA','admB','MediumInertPrimeLengthBound','SmallInertPrimeSmallOrderLengthBound','BandPlaceWeightApproximation','LargePrimeLengthVanishing','ExceptionalPrimesBounded','SmallPrimeLengthBound','RamifiedPrimeLengthBound'],
 R+'SumLogDivSqModPmOneLe.lean': ['sum_log_le','sum_log_div_le','sum_log_div_pred_le','sum_log_div_sq_le','sum_log_div_sq_tail','sum_log_div_sq_mod_pm_one_le','pm_one_of_pow'],
 L+'MemPrimesOverOfMem.lean': ['rowd_cong','Mst_ge'],
 L+'NEqRZeroMulXPow.lean': ['Den','rb\'lA_le','band_w\'\'','r_mul_eta_le','ratio_le_R_zero_sq','rowd_sum','sum_eP','sum_rowb','sum_rowc','sum_rowd','sum_flat'],
 L+'ExportBoundOfAdmissible.lean': ['sum_small','card_exc_le','sum_exc','point_bound','export_bound_of_admissible','large_eventually'],
 'src/Formalism/LocalRingCardinality/DataParams.lean': ["ParameterChoice'"],
},
'LN9': {
 H+'OptInEqSome.lean': ['ndCut','nautCut','layCut','cut'],
 H+'BuDefQEta.lean': ["Raw.rec'",'ledTr','parTr'],
 H+'ExtraTr.lean': ['extraTr'],
 H+'LinkNOfGd.lean': ['gd','twGood_gd','linkN_of_gd'],
 H+'EvPowLeExp.lean': ['ev_pow_le_exp'],
 L+'DataN.lean': ['NData'],
 I+'LogCardLevelGroupLeScalePowMulLength.lean': ['log_card_levelGroup_le_scale_pow_mul_length'],
},
'LN10': {
 F+'GlobalTheoremInputs.lean': ['ShaFinOdd','LinkN_at','LinkN'],
 N+'BoundAtTwoThreeFamily.lean': ['tab','Concl','ConclF'],
 I+'AdmittedStatementsOfLocalBoundsConclusion.lean': ['admittedStatements_of_localBoundsConclusion'],
 I+'LinkNAlongFamilyOfLocalBounds.lean': ['main'],
 T+'LinkNFam.lean': ['CutGivesAlt','linkN_of_twGood_galoisPreconditions'],
 T+'GaloisPreconditions.lean': ['GaloisPreconditions'],
 T+'CFacts.lean': ['facts_of_galois_preconditions_of_cutRec','exists_good_cut_facts_tie4'],
 N+'BoundAtTwoAndThreeForFamily.lean': ['Hypotheses₂','SetPt','Setup','BoundAtTwoAndThreeForFamily'],
 L+'ExportBoundOfAdmissible.lean': ['stmtU_holds','stmtF_holds'],
},
}

titles = {
'LN1': 'Integral central coefficients and the literal ordered-tuple good element in the original DVR',
'LN2': 'All five fields of the good cut from explicit same-state type and parameter compatibilities',
'LN3': 'The actual spectral quotient, preserved multiplicities and finite congruence lengths',
'LN4': 'Coordinate-congruence-ideal filtration bound with arbitrary eigenspace multiplicities',
'LN5': 'Exact cut-kernel loss and original-row adm1 with normalized v_l(N_G) correction',
'LN6': 'Localisation-disjoint multiplicity sum, theta injectivity and the exact rank input',
'LN7': 'Exact weighted global cut loss and local-denominator-to-global-sum estimate',
'LN8': 'Complete numerical prime envelope, including small-order sparsity and exceptional tails',
'LN9': 'Uniform cut-family to original-family LinkN with unchanged cohomological factor',
'LN10': 'Complete explicit-local-input to original-family LinkN supplier and minimal frontier',
}
deps = {
'LN1': [], 'LN2': ['LN1'], 'LN3': [], 'LN4': ['LN3'],
'LN5': ['LN2','LN3','LN4'], 'LN6': [], 'LN7': ['LN5','LN6'],
'LN8': ['PN1','PN4','PN5','PN6','PN15','PN16'],
'LN9': ['LN2','LN3','LN5','LN6','LN7'],
'LN10': ['LN1','LN2','LN3','LN4','LN5','LN6','LN7','LN8','LN9','PN16'],
}
scopes = {
'LN1': 'Finite group, central complex idempotents, injective original coefficient embedding containing a primitive group-order root. Proves integrality by regular-representation trace; preserves every ordered-root-vector summand.',
'LN2': 'Actual Pend and theta/type data, exact e0 action on good/bad theta types, integral/complex eigen-action compatibility, local tame-label dictionary and same-point constituent permutation. Constructs Good; does not construct NormChoiceFacts on the cut.',
'LN3': 'Finite free module over the original DVR, finite separating Hecke algebra, and explicit rational eigenspace spanning. Identifies literal cutM, proves finiteness and retained multiplicities.',
'LN4': 'Data of LN3 and a subset A. Proves length C_A <= sum dim(V_x) length(O/I_x(A)) by a filtration; no local Galois input.',
'LN5': 'LN3 plus an integral operator acting N_G on good eigenspaces and zero outside the selected set, with S intersect Z = Y. Proves exact normalized defect and original vcc bound, including empty localisation cases.',
'LN6': 'Actual internal isotypic decomposition, ConclusionZ, LocalisationUniqueness, and nonzero theta-composition scalars. Derives MultLe; equality to reference dZ0 is proved when both theta injectivities are supplied, otherwise remains explicit adm3.',
'LN7': 'LN5--LN6, actual place identification and eta ties. Proves loss <= dZ0 log N_G. The direct local denominator version retains its exact per-prime and summability premises.',
'LN8': 'Actual ParameterChoice and uniformly bounded scalar parameters; the listed split/inert, band, exceptional, small/ramified/generator inequalities and cyclotomic nu bound. Proves all numerical summation and threshold estimates, with 2000(C+1)^3; local arithmetic inequalities are not proved here.',
'LN9': 'One actual family and its literal gd cut, original MultLe/adm3, uniform polynomial rank/generator-prime bounds, and LinkN on the cut. Proves original LinkN, adds only an explicit logarithmic group-order budget, preserves the cohomological series and guards.',
'LN10': 'Same-state spectral/type/theta inputs plus uniform actual per-prime denominator tables, on the original data or the canonical cut. Proves the exact original-family LinkN quantifier order; retains deep Galois and transported NormChoiceFacts suppliers.',
}
inputs = {
'type_compatibility': {
 'kind': 'bespoke same-state compatibility, retained',
 'meaning': 'Exact e0 good/bad type action; integral central action and Pass.EigSpan; tame-character/parameter dictionary; same-Hecke-point base-change constituent permutation. Ordered tuples are not silently de-duplicated.',
 'source': T+'EigenActionAtGoodPoint.lean',
},
'spectral_spanning': {
 'kind': 'actual state hypothesis, retained',
 'meaning': 'The rational Hecke eigenspaces span the actual module; not inferred from point separation.',
 'source': L+'DataN.lean',
},
'theta_identification': {
 'kind': 'bespoke same-state identities, retained',
 'meaning': 'ConclusionZ, IsotInternal, LocalisationUniqueness and nonzero theta-composition scalars; reference/twisted rank equality adm3 unless derived from both injective maps.',
 'source': I+'GoodPointMultiplicityLeRankProof.lean',
},
'local_denominator_bounds': {
 'kind': 'bespoke local arithmetic inequalities, retained',
 'meaning': 'Original or actual-cut vcc comparison, local cyclotomic error, split/inert cases, band and exceptional set, and small/q,d/generator bounds, with one uniform constant.',
 'source': R+'TwistedPlaces.lean',
},
'parameter_budget': {
 'kind': 'stated uniform family parameter input; ParameterChoice construction linked to PN16',
 'meaning': 'Polynomial rank/density bounds, class-number logarithm and fixed parameter constants. The log group-order bound used for restoration is independently proved in LN9.',
 'source': R+'TwistedPlaces.lean',
},
'cohomological_guards': {
 'kind': 'literal conditional conclusion guards, retained',
 'meaning': 'ShaFinOdd and Summable(vvTerm). Neither finiteness nor summability nor the LinkV bound is inferred by this chapter.',
 'source': F+'GlobalTheoremInputs.lean',
},
'cut_facts_transport': {
 'kind': 'stronger source compatibility supplier, retained',
 'meaning': 'CutGivesAlt additionally demands all NormChoiceFacts and Tie4 on the same cut. LN2 proves Good but does not claim these extra fields.',
 'source': T+'LinkNFam.lean',
},
}
uses = {
'LN1': [], 'LN2': ['type_compatibility'], 'LN3': ['spectral_spanning'],
'LN4': ['spectral_spanning'], 'LN5': ['spectral_spanning','type_compatibility'],
'LN6': ['theta_identification'],
'LN7': ['theta_identification','local_denominator_bounds','cohomological_guards'],
'LN8': ['local_denominator_bounds','parameter_budget'],
'LN9': ['theta_identification','parameter_budget','cohomological_guards'],
'LN10': list(inputs),
}

tex = (HERE/'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    start = next(i for i,l in enumerate(lines,1) if l.startswith(('\\paragraph{'+cid+':').encode()))
    end = min([i for i,l in enumerate(lines,1) if i>start and l.startswith(b'\\paragraph{LN')],default=len(lines)+1)-1
    loc = {'file': 'congruence_chain/main.tex', 'paragraph': cid, 'line_start': start,
           'line_end': end, 'label': 'claim:'+cid, 'sha256': sha(b''.join(lines[start-1:end]))}
    claims.append({'id': cid, 'title': titles[cid], 'statement': scopes[cid],
       'status': 'Complete human proof of the stated conditional scope; not independently replayed in Lean',
       'mathematical_status': 'proved in the explicit scope; retained inputs separately identified',
       'introduced_in': '0.24', 'depends_on': deps[cid],
       'assumptions': [scopes[cid]], 'named_classical_inputs': [],
       'input_ids': uses[cid], 'remaining_inputs': [inputs[x]['meaning'] for x in uses[cid]],
       'proof_location': loc,
       'source_relation': 'Human alternative and consolidated exact-interface reconstruction. Novel trace/filtration simplifications are proved from the literal definitions; no claim that an abstract interface supplies its own compatible witnesses.',
       'sources': [source(path,s) for path,names in spec[cid].items() for s in names],
       'component_ledger': 'congruence_chain/provenance.json'})

for path,rec in files.items():
    blob = subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+path])
    if sha(blob) != rec['sha256']:
        raise ValueError('Pinned Git blob mismatch: '+path)
out = {'schema': 'rh-human-reconstruction-provenance/1', 'artifact_version': '0.24',
 'date': '2026-11-22', 'repository': BASE, 'commit': PIN, 'component': 'congruence_chain',
 'scope': 'Complete integral-cut/denominator/numerical/rank/threshold chain from explicit actual local inputs to original-family LinkN; deep Galois suppliers and complete RH/GRH remain outside this closure.',
 'claims': claims, 'source_files': list(files.values()), 'dependency_graph': deps,
 'input_ledger': inputs,
 'downstream_consumers': [{'claim':'DA2','input':'LinkN on the original actual family',
    'other_inputs_not_supplied':['LinkV/cohomological bound','required Sha finiteness and summability','reference rank equality to D0','actual metric premise']}],
 'validation': {'source_files_checked_against_pinned_git_blobs':len(files),
   'claim_source_links':sum(len(c['sources']) for c in claims),
   'main_tex_sha256':sha(tex),
   'verification_kind':'exact source-byte/range and proof-text locator checks; human proof, not Lean replay'}}
(HERE/'provenance.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' — '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nfile '+s['sha256']+'\nrange '+s['range_sha256'] for s in c['sources']) for c in claims)+'\n')
print(json.dumps(out['validation'],indent=2))
