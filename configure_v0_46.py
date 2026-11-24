#!/usr/bin/env python3
"""Configure the current increment after the exact whole-contract reviews pass."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/name).read_text())
def sha(data):
    return hashlib.sha256(data).hexdigest()

old=read('increment_v0_45.json')
nodes={n['id']:n for n in read('dependency_audit_v0_45/obligation_map.json')['nodes']}
reviews={
    'CNR3':'rank_three_congruence_v46/review_RNC1_RNC16_root.json',
    'TASK_PROP_GK_INSTALL':'prop_gk_installation_v46/review_PGK1_PGK6_root.json',
}
for key,path in reviews.items():
    r=read(path)
    assert r['result']=='PASS'
    assert r['proof_sha256']==sha((ROOT/r['proof_file']).read_bytes())
    exact=r['selected_whole_contract_reviewed']
    assert exact['id']==key and exact['full_original_contract_closed_in_stated_scope']
    assert exact['baseline_contract_sha256']==sha(nodes[key]['contract'].encode())

components=['rank_three_congruence_v46','prop_gk_installation_v46',
            'arithmetic_rows_v46','integral_cusp_lattices_v46','global_local_gain_v46']
closed={
 'CNR3':{
    'category':'B','claims':['RNC'+str(i) for i in range(1,17)],
    'conclusion':'The full original rank-three congruence-number assertion, with one nonzero integer before all later coefficient primes, closures, embeddings, Frobenius lifts and admissible finite collections.',
    'method':'Actual rank-three and rank-two cuspidal attachment, coefficient-independent auxiliary levels, explicit bounded-rank cusp catalogues, all-conjugate integrality and the full indexed-orbit product.',
    'boundary':'The matched classical automorphic/cohomological/period foundations remain explicit. All-rank CountK/CountQ and the separate OneChar producer are not inferred.'},
 'TASK_PROP_GK_INSTALL':{
    'category':'B','claims':['PGK'+str(i) for i in range(1,7)],
    'conclusion':'The complete original finite implication CNR3 and OneChar imply PropGK, retaining fixed-K constants, e,N, the character kernel, the root-of-unity orbit and every later coefficient datum.',
    'method':'Exact finite orbit and Frobenius construction, the completed congruence integer, the original one-character length bound, and the finite valuation sum and product comparison.',
    'boundary':'This closes the selected implication-reconstruction task. The actual OneChar theorem, RIG_II, and unconditional PropGK/CountI remain independent open producer obligations.'},
}
conclusions=[
 'RNC1-RNC16 reconstruct the full original CNR3. The actual rank-two newform is adelized over Q and twisted by |det|^(1/2); the rank-three and rank-two original flags identify the exact weights. The literal LevelAt disjunction, with precisely matched Shin-regular coefficient-prime compatibility, removes unwanted monodromy outside the given level. Fixed arithmetic cells and explicit polynomial coefficient ranks give finite full cusp catalogues at auxiliary levels M^5 and M^3. Aut(C) acts on entire labels, with integral-power Satake normalization. Purity and both Hodge endpoints give integral trace factors. Their complete orbit-times-label product is a nonzero integer chosen before every later coefficient prime, and injective label selection gives the exact norm-product inequality. The constants may be chosen with A=103; the original Galois levels, ell=3 and all original closures and embeddings remain unchanged.',
 'PGK1-PGK6 reconstruct the entire original finite CNR3/OneChar-to-PropGK implication. The actual character orbit and Frobenius/valuation comparison are constructed with the original fixed-K constants and the nonzero integer chosen before every later coefficient datum. RNC16 supplies CNR3. The original OneChar remains the explicitly quantified arithmetic length premise, so the selected B installation task is closed while its separate C producer remains open.',
 'ARO1-ARO30 reconstruct the structural arithmetic row object on the original supplied adelic SG.HidaSetting. Actual reduction, both prime kernels, full surjectivity and exact Haar-fiber volumes identify the finite event algebra with its convolution operators. A direct reverse-flag/CRT argument proves the concrete level shape; the original additive character factors with nontrivial prime characters. This supplies full EtOne, EtUniv, EtInt and EtAlg. Schur compression gives the exact bounded-intertwiner evaluation bijection and original row multiplicities. One label completion preserves all original good rows, including repeated labels, and gives a single AllRows, AllJoinA and PCountTie. The full cylinder-count installer retains the original CountIdempotentsClass theorem; FLC19 and GQT5 then apply on that same object. Common-family existence, RowsFinDim/ties and the arithmetic count producer remain explicit.',
 'ICL1-ICL21 prove finite generation of the whole original valuation-nonnegative cusp lattice at every original weight. Nonzero integral-frame evaluations at CM points, all finite primes, principalized eigenmodules and a finite separating evaluation family give the actual finite-generation theorem without assuming spanning. The identity cover is constructed exactly given the original IsNab connection, which remains an explicit input. The remaining spanning branch is written out through a Neumann inverse, absolutely convergent orbit unfolding, integral harmonic polynomials, coefficient descent to the original field, and one explicit global clearing scalar A_w*betaH. The original principal charts, level system, raw Gaussian identities, short-rule gluing/dictionary and ramified jet bounds remain five named producer inputs. Conditional FullAt/LatFull and exact FWTie transport at both Boolean levels are proved; no unconditional full-lattice or higher-cover producer is declared complete.',
 'GLG1-GLG18 prove the entire original RemainingCountingStatement, including RestStar, both candidate-prime ranges, nearest-even-predecessor injection, exact ceiling budgets and the original b_o=b^(x^(-eps/2)). The constant is chosen before the admitted instance families, and one threshold works for all later members, primes, lifts and top weights without an upper bound on b_s. The packet also proves actual served-index/coverage/S_v bounds, original integral-operator preservation, coefficient-rational descent and NPDesc, exact normalized local lengths, selected-top admissibility and the full five-field LinkG installer. Its family conclusion retains actual GroupCompatibilityFamily, full admitted inputs, local first-growth and mean-deficit hypotheses; it does not construct those records.'
]
remaining=[
 'Construct the prescribed common geometric family and the original higher CoversAt, all-tuple ClsEx/uniqueness with phase rescalings, one PointIdentCore with common lambda,z, and base ClassSumsSpan. ICL8 now proves the actual finite-generation half of the integral cusp lattice. Its spanning half retains the original IsNab connection and five main producers: principal charts, the actual finite-level system, raw Gaussian identity/reproduction, short-rule gluing and simultaneous reading dictionary, and ramified integral jet estimates. Keep the original outer family quantifiers, Fits and eta agreement.',
 'Complete the original F3 local coefficient bridges and F4 full common-overfield reading, preserving exact valuation/norm/GoodCoef/iq data and the entire coefficient field. Supply actual complex Hecke standard/no-Jordan and arithmetic character data on one common form datum; the completed finite algebra, ordinary Hecke and selected Hida support results remain available.',
 'Complete actual base rows, host/frame lengths, nonzero chains and group ties, MultEq support, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. Keep the stronger second DivRows3 scope separate from the completed first DivDef3 and row-pair integrability.',
 'Realize one actual common adelic SG.HidaSetting and its original AutTie/RowDictTie/LabTie and RowsFinDim data, then prove the exact arithmetic cylinder count theorem or the three sufficient counts. ARO now supplies reduction, Haar/EtOne, full projector and row algebra, one common AllRows object and the exact count/weight/retained-defect consumers on those inputs. Do not redo the structural row construction.',
 'Install the original denominator, period/height, local-gain and normalized spectral estimates on that same family. GLG now proves the full logarithmic counting theorem, integral-operator/rational-descent/local-length consumers and exact LinkG installer; realize its actual compatibility, full admitted/local first-growth and mean-deficit inputs with simultaneous thresholds. Complete the compatible second-layer selector and retain the exact GQT sufficient alternatives where used.',
 'Finish the original OneChar, RIG_II and remaining Cases I/V producers for RH. CNR3 and the full finite PropGK implication are now reconstructed; the latter still uses OneChar. Unrestricted Dirichlet GRH additionally retains Case III, Seed IV and the rank-four chain propagation/descent branch. The completed AD_VANISH_K_MATCH, HOST_RIGID_S, six Hida fields and both selected rank-four support Links are not active tasks.'
]
progress={
 'CNR3':{'completed':['RNC1-RNC16'],'remaining':'None within the literal original CNR3 contract; named classical foundations retain their explicit scope.'},
 'TASK_PROP_GK_INSTALL':{'completed':['PGK1-PGK6','RNC16'], 'remaining':'None within this finite implication task. Its distinct OneChar arithmetic producer and RIG_II remain open.'},
 'GLOBAL_RETAINED_DEFECT':{'completed':['ARO1-ARO30'], 'remaining':'Actual common X and all original ties/RowsFinDim, plus CountIdempotentsClass or the exact three sufficient arithmetic counts and simultaneous family thresholds. The same-object weight and retained-defect consumers are available.'},
 'GLOBAL_LOCAL_GAIN':{'completed':['GLG1-GLG18'], 'remaining':'Realize the original common compatibility and full admitted inputs, including local first-growth and mean-deficit bounds on the same family. The full counting theorem and all written local-to-global consumers are available.'},
 'DESIGN_CHOICES_COMMON':{'completed':['ICL1-ICL21'], 'remaining':'Actual common geometry and higher covers/class sums/PointIdentCore/ClassSumsSpan, plus the supplied original IsNab and five exact producers retained for cusp-lattice spanning; existing host/chain/coefficient/Fits/eta obligations remain coupled.'},
 'BASE_THETA_RATIONAL_TESTS':{'completed':['ICL1-ICL21'], 'remaining':'Actual higher covers, all-tuple class sums/uniqueness, common PointIdentCore, base ClassSumsSpan and common geometry; integral-lattice finite generation is proved, while spanning still needs the original IsNab and five named producer groups. Original both-level FWTie transport is available on those inputs.'},
}
updated={}
for key in ['DESIGN_CHOICES_COMMON','BASE_THETA_RATIONAL_TESTS']:
    updated[key]=nodes[key]['contract']+' Version0.46 proves finite generation of the original whole integral cusp lattice by actual integral-frame evaluation. It also proves the exact identity-cover, analytic unfolding, original-field coefficient descent, global clearing-scalar and both-level lattice-transport implications. Full spanning retains the supplied original IsNab connection and the five explicit principal-chart, level-system, raw-Gaussian, short-rule/dictionary and ramified-jet producers. The higher tuple covers, actual common class sums, PointIdentCore and ClassSumsSpan remain separate.'

cfg={
 'artifact_version':'0.46','date':'2026-11-23','source_commit':old['source_commit'],
 'title':'Congruence integers, arithmetic rows, integral lattices and local gain',
 'components':components,
 'component_authors':{'rank_three_congruence_v46':'main_proof_rigidity',
    'prop_gk_installation_v46':'main_proof_rigidity','arithmetic_rows_v46':'root',
    'integral_cusp_lattices_v46':'ordinary_structure','global_local_gain_v46':'global_estimates'},
 'closed_selected_leaves':closed,
 'closed_nested_producers':[
    'Full literal CNR3 with complete bounded-rank catalogue and indexed-orbit integer proof',
    'Full original finite CNR3 and OneChar to PropGK implication',
    'Actual reduction and Haar normalization, full EtOne/EtAlg and one original AllRows/AllJoinA/PCountTie on supplied original data',
    'Finite generation of the whole original integral cusp lattice at every original weight',
    'Exact identity cover and conditional theta-spanning, original-field descent, global scalar and both-level LatFull transport',
    'Full original RestStar and RemainingCountingStatement with prior constants and all-window uniformity',
    'Actual integral local operators, coefficient rational descent/NPDesc and normalized lattice-length consumers',
    'Full conditional original LinkG_at and eventual LinkG installer with all original local/global normalizations'
 ],
 'status': 'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge-Claude formal source as fully checked and correct. Version0.46 completes the original rank-three congruence integer and the exact finite PropGK implication, closing CNR3 and TASK_PROP_GK_INSTALL in their full selected scopes. It also completes the structural original arithmetic row construction on given data, integral-cusp-lattice finite generation, and the full remaining logarithmic counting theorem, with exact conditional lattice-spanning and global-gain installations. The 28 remaining whole selected obligations are 20 C and 8 B; 21 are shared RH/GRH and 7 are additional GRH obligations. The actual OneChar theorem, common geometric/arithmetic families, lattice-spanning producers and remaining global quantitative/case producers still require reconstruction. No Lean build or kernel replay is claimed.',
 'local_conclusions':conclusions,'remaining_major_inputs':remaining,
 'next_targets':[
    'Produce the original IsNab connection and five precise cusp-lattice spanning input groups in parallel where possible: principal charts/level system; Gaussian identity and reproducing estimates; short-rule gluing/simultaneous dictionary; ramified integral jet bounds. Reuse ICL finite generation and its completed implications.',
    'Construct the remaining common higher covers, all-tuple class sums/uniqueness, PointIdentCore and ClassSumsSpan, preserving the original common family, phases, coefficient field, Fits and eta agreement.',
    'Supply the actual common SG.HidaSetting/ties/RowsFinDim and the arithmetic counting theorem or its three sufficient cylinder counts; reuse ARO rather than reconstructing row structure. Continue the exact denominator, period/height, first-growth, compatibility, normalized spectral and second-layer selection producers.',
    'Reconstruct the original OneChar and RIG_II producers and RH Case I/V installation, using completed CNR3 and PGK. Retain independent GRH Case III/Seed IV/rank-four chain tasks. Do not reopen the completed ordinary Hida/support, finite local count, host rigidity or adjoint leaves.'
 ],
 'selected_node_progress':progress,'updated_contracts':updated,
 'published_applications':[{
    'id':'RNC1','classification':'A','component':'rank_three_congruence_v46',
    'registry':'rank_three_congruence_v46/classical_inputs.json',
    'scope':'General RA polarized existence before weight identification, then exact rank3/rank2 Shin-regular full local compatibility, purity and crystalline endpoint applications. CM/totally-real fields, all coefficient primes and fixed iota retained.',
    'review':'rank_three_congruence_v46/review_RNC1_RNC16_root.json'}],
 'publication_note':'RNC1 is the one newly classified published application, with original primary theorem and normalization checks. All other newly written claims are human proofs of their stated original, conditional or eventual interfaces. Named classical and period foundations remain explicit.'
}
(ROOT/'increment_v0_46.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'components':components,'closed_selected_leaves':list(closed)},indent=2))
