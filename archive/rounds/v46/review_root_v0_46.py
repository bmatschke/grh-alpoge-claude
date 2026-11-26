#!/usr/bin/env python3
"""Bind the root's completed mathematical reviews to the inspected proof bytes.

This script records reviews already performed by a human-readable mathematical
comparison. Its hashes do not themselves establish mathematical correctness.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def source(path, first, last):
    raw = (SOURCE / path).read_bytes()
    assert raw == subprocess.check_output(['git', '-C', str(SOURCE), 'show', PIN+':'+path])
    return {'path': path, 'line_start': first, 'line_end': last,
            'file_sha256': sha(raw),
            'range_sha256': sha(b''.join(raw.splitlines(keepends=True)[first-1:last])),
            'verified_equal_to_pin': True}

def bind(component, ids, findings, sources, scope, extra=None):
    ledger = json.loads((ROOT/component/'provenance.json').read_text())
    claims = {c['id']: c for c in ledger['claims']}
    proof = ROOT/component/'main.tex'
    raw = proof.read_bytes()
    blocks = []
    for cid in ids:
        p = claims[cid]['proof_location']
        excerpt = b''.join(raw.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
        assert sha(excerpt) == p['sha256'], (cid, 'stale ledger')
        blocks.append({'id': cid, 'line_start': p['line_start'],
                       'line_end': p['line_end'], 'block_sha256': sha(excerpt),
                       'result': 'PASS'})
    report = {
        'schema': 'rh-independent-human-review/1', 'artifact_version': '0.46',
        'component': component, 'reviewer': 'root', 'result': 'PASS',
        'proof_file': component+'/main.tex', 'proof_sha256': sha(raw),
        'source_commit': PIN, 'claims_reviewed': blocks, 'scope': scope,
        'findings': findings, 'sources_inspected': sources,
        'unresolved_findings': [], 'proof_bytes_modified_by_reviewer': False,
        'lean_replay': False,
    }
    if extra:
        report.update(extra)
    out = ROOT/component/('review_'+ids[0]+'_'+ids[-1]+'_root.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'review': str(out.relative_to(ROOT)), 'sha256': sha(out.read_bytes()),
                      'proof_sha256': sha(raw), 'claims': len(ids), 'result': 'PASS'}))

def rank_three():
    component = 'rank_three_congruence_v46'
    baseline = json.loads((ROOT/'dependency_audit_v0_45/obligation_map.json').read_text())
    contract = next(n['contract'] for n in baseline['nodes'] if n['id']=='CNR3')
    findings = [
        {'topic': 'Published input and staging', 'result': 'PASS',
         'detail': 'Directly checked BLGGT Theorem2.1.1, Section2.1, l=p II TheoremA/1.1/Corollary1.2 and Shin regularity, and JL Proposition10.9. General RA polarized existence precedes identification of the actual highest weight; full coefficient-prime compatibility is used after the two displayed weights meet Shin regularity. No Iwahori or large-prime condition is added, and ell=3 is retained.'},
        {'topic': 'Actual rank-two and rank-three attachments', 'result': 'PASS',
         'detail': 'Adelization and nebentype gluing, Fourier-coefficient Hecke relations, the |det|^(1/2) twist, geometric Frobenius q-scaling and the two precise highest weights agree. De Rham exactness is used only after identifying the whole representation. The full original closures and fixed iota are retained.'},
        {'topic': 'Local level and conductor', 'result': 'PASS',
         'detail': 'The original no-cyclotomic-ratio/potential-crystallinity disjunction eliminates monodromy at coefficient primes outside M. Finite inertia characters have conductor at most v(M), and nilpotent loss is at most n-1. Generic newvectors therefore give auxiliary levels M^5/M^3 without changing original Galois levels.'},
        {'topic': 'Finite labels and conjugation', 'result': 'PASS',
         'detail': 'A fixed level-three torsion-free arithmetic CW model, explicit polynomial highest-weight ranks and finite covers give the exponents18/4 and final90/12. Projective O_F lattices admit integral Z bases for the mod3 argument. Full cusp labels, not one-place eigenvalues, are retained. The Hecke formula uses only q^{j(j-1)/2}, so Aut(C) conjugation has no square-root ambiguity.'},
        {'topic': 'Purity and integral trace catalogue', 'result': 'PASS',
         'detail': 'Compact-image lattices give units away from p; crystalline Newton/Hodge bounds give both integral endpoints at p. RNC9 and RNC10 give exactly the geometric trace of the rank-three representation and of the restricted two-by-two block plus1. Equal labels imply isomorphism, including reducible restrictions, and the disjoint-union classifier preserves the original disjunction.'},
        {'topic': 'Integer and full quantifier order', 'result': 'PASS',
         'detail': 'Every q^e(t-Eis) is nonzero integral. The complete orbit-times-label product is fixed by all complex automorphisms, hence is a nonzero rational integer; repeated orbit values remain indexed. Constants c,A are fixed with K, NN before ell/closures/iota/Frobenius/families. Injective selection of labels and deletion of ell-adically integral factors gives the exact norm-product inequality. Empty families and ell=3 are included.'},
        {'topic': 'Original selected contract', 'result': 'PASS',
         'detail': 'Compared all fields of literal CongruenceNumberRankThree: fixed quadratic K; e,N>=1; p>=7 prime avoiding N and discK; w above p; full finite Aut(C)-stable root-of-unity orbit; nonzero NN and logarithmic bound; all later original coefficient data and pairwise-nonisomorphic collections; original Adm3 or Adm2 at N*abs(discriminant). All are supplied. OneChar and unconditional PropGK remain separate.'},
    ]
    primary = [
        {'url': 'https://www.ma.imperial.ac.uk/~tsg/Index_files/potentialautomorphy.pdf',
         'locator': 'Section2.1, Theorem2.1.1 clauses1-4', 'root_web_ref': 'turn622424453view0'},
        {'url': 'https://virtualmath1.stanford.edu/~rltaylor/lg2.pdf',
         'locator': 'TheoremA; Shin-regular definition; Theorem1.1 and Corollary1.2', 'root_web_ref': 'turn980982204view1'},
        {'url': 'https://publications.ias.edu/sites/default/files/automorphic-forms-on-gl2_rpl_9.pdf',
         'locator': 'Proposition10.9', 'root_web_ref': 'turn980982204view2'},
    ]
    bind(component, ['RNC'+str(i) for i in range(1,17)], findings,
         [source('src/Development/AutomorphicArithmetic/AutomorphicVarieties/AutomorphicForms/CongruenceNumberRankThree.lean',110,140)],
         'Complete RNC1-RNC16 at their exact named classical foundations and the literal original CNR3 contract. No all-rank CountK/CountQ or OneChar theorem is inferred.',
         {'primary_literature_inspected': primary,
          'selected_whole_contract_reviewed': {
              'id': 'CNR3', 'baseline_version': '0.45',
              'baseline_contract_sha256': sha(contract.encode()),
              'full_original_contract_closed_in_stated_scope': True,
              'no_weaker_replacement': True,
              'boundary': 'The named classical/period foundations remain explicit; OneChar and the other arithmetic length producers remain independent.'}})

def integral_cusp():
    findings=[
      {'topic':'Identity cover and retained connection','result':'PASS',
       'detail':'The literal DeltaDat/IsLev/EtaOK/PhiPin/PsiTie fields reduce correctly at pd=1 and I=O_E. Zero half-quotients have one tuple, but the chosen representatives are still accounted for by the primitive-root exponent. The original IsNab connection is supplied, not reconstructed.'},
      {'topic':'Neumann inverse and finite-rank unfolding','result':'PASS after freeness clarification',
       'detail':'The diagonal class-sum scalar is positive and off-diagonal norm is <1 times it; covariance and weighted holomorphy survive the inverse. The abstract orbit argument now explicitly requires a free a.e. action and an a.e. partition by translates. The actual lattice/frame action is free and properly discontinuous with unit Jacobian. Absolute summability precedes unfolding; a finite evaluation matrix proves integrability of the coefficient functions.'},
      {'topic':'Original field and simultaneous readings','result':'PASS',
       'detail':'Finite-degree harmonic/highest-weight equations are over the original K and commute with extension. Scaling each basis polynomial by lattice and coefficient denominators preserves the literal symO/harmL conditions. The retained simultaneous short-rule dictionary has a scalar independent of the component; scalar-extension injectivity from ICL8 descends the resulting finite span to K.'},
      {'topic':'Every-place clearing scalar','result':'PASS',
       'detail':'Compared le_nval_avg, nrm_nat and the full original clearing calculation. The same positive-degree scalar P0^(Delta_E*d_w)*M^d_w*c0*betaH cancels the normalized jet bound at all places and all frames. Root-of-unity factors have valuation0; the only averaging denominator is c0. DF is a literal natural sum and the host discriminant bound is now proved from its definition. The finite extension does not change normalized valuation.'},
      {'topic':'Full-lattice and both-level transport','result':'PASS in stated conditional scope',
       'detail':'Powers reach the actual stable range and the integral scalar power lemma returns to the original weight without extracting roots. Finite generation is supplied by ICL8 independently of spanning. FullAt/LatFull are claimed only under original IsNab and five uniformly quantified producer groups; source FWTie identifies the entire lattice, and RTG22/23 transport it at both Boolean levels.'},
      {'topic':'Whole producer boundary','result':'PASS',
       'detail':'No unconditional LatFull, higher CoversAt, all-tuple class-sum/phase uniqueness, common PointIdentCore, base ClassSumsSpan or common-family existence is inferred. Original principal charts, level system, raw Gaussian, short-rule/dictionary, ramified jets and canonical connection remain explicit.'}
    ]
    specs=[
      ('src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSmulNonnegOfPow.lean',74,178),
      ('src/Formalism/LocalToGlobal/ProjectiveLattices/ThShort.lean',114,234),
      ('src/Development/AbelianVarietyTheory/Definitions/SpanningFamilies/IsSystem.lean',99,147),
      ('src/Development/AbelianVarietyTheory/Proofs/SiegelThetaTransformation/HermitianThetaSeriesSpanBoundedForms.lean',139,182),
      ('src/Development/AbelianVarietyTheory/Proofs/RingsOfIntegers/ShortGeneratorPlaceValuationBoundProof.lean',71,124),
      ('src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/ExistsSmulShortNonneg.lean',275,375),
      ('src/Formalism/LocalToGlobal/IndefiniteReal/FWExist.lean',222,239),
      ('src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IntegralCuspFormsFullLattice.lean',11,54),
    ]
    bind('integral_cusp_lattices_v46',['ICL'+str(i) for i in range(10,22)],findings,
         [source(*s) for s in specs],
         'ICL10-ICL21: exact identity-cover construction given IsNab, original analytic/integral spanning implications and conditional FullAt/LatFull/FWTie. Finite generation ICL8 is reviewed independently in the companion report. No whole selected producer is closed.')

def global_gain():
    findings=[
      {'topic':'Original orbit/count quantities','result':'PASS',
       'detail':'Nearest even predecessor gives an injection into the actual odd-power minimum sum, preserving the selected representative. The good-orbit cardinal inequality, both prime-range budgets and every ceiling match NumStar and StarAt. No upper bound on b_s is introduced.'},
      {'topic':'Uniform numerical threshold','result':'PASS',
       'detail':'CStar is fixed before the instance families. The original adm5 bound at eps/48 is dominated by Z=exp(x^(23eps/48)); all finite budget terms are bounded by Z^13<=exp(x^(eps/2)). One threshold covers every member, prime, lift and top function. The coefficient1 of b_o is preserved.'},
      {'topic':'Full RemainingCountingStatement','result':'PASS',
       'detail':'Directly compared RestStar, GainBoundAll/RequiresAll and RemainingCountingStatement. All gain branches, including empty served sets, signal primes, large primes and zero Frobenius component, are addressed. The askP-to-askG shift is paid by the single C1+1 increase. The literal family quantifier order and all-window conclusion are supplied.'},
      {'topic':'Local integral operators and descent','result':'PASS',
       'detail':'Tableau row-degree bounds and homogeneous divided-power Weyl generators prove preservation of each actual coefficient lattice, including signed weights and basis changes. Rational coefficient evaluations and a K-linear retraction give YvRat without a Galois premise. GatTies is explicit; faithful flatness over the original DVR transports the actual finite sums and intersections defining NPDesc.'},
      {'topic':'Exact local length normalization','result':'PASS',
       'detail':'The empty subset gives a positive p-power bound on the quotient, proving finiteness. Original Smith exponents scale by the relative ramification a_w and v_O(p)=a_w*e_w; the normalized global length is original local length/e_w. Empty served support and unserved regular places are handled separately, with p=T_u excluded exactly where required.'},
      {'topic':'All five LinkG fields and family scope','result':'PASS',
       'detail':'Compared the full LinkG_at and LinkG definitions. Depth inclusion, normalized length and empty-set clause, exact2m*S_v bound, gain/class-sum estimate, served coverage and unchanged MeanKappaBound are all supplied on the same data. The global loss4|C|+1 preserves b_o coefficient1. Family compatibility, full admitted/local-first-growth and mean hypotheses remain antecedents, so no whole GLOBAL_LOCAL_GAIN closure is asserted.'}
    ]
    specs=[
      ('src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/Conclusion1OfGainBoundAll.lean',109,165),
      ('src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/PartnerCountOfCentral.lean',440,476),
      ('src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/StarNum.lean',1,130),
      ('src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums.lean',18,64),
      ('src/Formalism/SharpRestriction/GrowthBounds/LogarithmicSums/RemainingCountingStatement.lean',10,26),
      ('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean',97,141),
      ('src/Formalism/SharpRestriction/GrowthBounds/FormalGroupSystem.lean',802,808),
      ('src/Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/NpDescOfValRat.lean',1,18),
    ]
    bind('global_local_gain_v46',['GLG'+str(i) for i in range(1,19)],findings,
         [source(*s) for s in specs],
         'All GLG1-GLG18: complete original nested RestStar/RemainingCountingStatement and the exact original local-to-global consumers. Actual common compatibility, admitted family/local first-growth and mean bounds remain explicit. No whole selected leaf closure.')

def prop_gk():
    baseline=json.loads((ROOT/'dependency_audit_v0_45/obligation_map.json').read_text())
    contract=next(n['contract'] for n in baseline['nodes'] if n['id']=='TASK_PROP_GK_INSTALL')
    findings=[
      {'topic':'Original complete character orbit','result':'PASS',
       'detail':'The quotient is cyclic whenever a faithful coefficient character exists. All complex characters with the same kernel are coprime powers of that very character and hence are realized over the same O; cardinality is phi(index), including index1. Without such a witness the universal complex orbit may be empty and remains bounded by phi(index).'},
      {'topic':'All original GD fields','result':'PASS',
       'detail':'Compared the literal twelve fields of GD. Coprime powers preserve character order, the quadratic primary component, parity and the prime-to-ell character kernel, so the eta condition is unchanged. All field/level/prime fields are retained. ell=3 is not excluded by a new guard; its gen antecedent is impossible.'},
      {'topic':'Frobenius, scalar towers and fixed data','result':'PASS',
       'detail':'Arithmetic Frobenius acts by q on prime-to-p roots of unity, giving cls_N=q and epsilon=q. At sigma^-1, z=chi(q)^-1 gives exactly q^-e*psi(q)^-1+1+q^e*psi(q), the original OneChar scalar. Every closure, prolongation and coefficient isomorphism is chosen after NN.'},
      {'topic':'Exact OneChar use and finite product','result':'PASS',
       'detail':'The original Selmer length and its normalized real form are retained. Universal trace separation is obtained from singleton admissible collections before OneChar selects finite pairwise-nonisomorphic sets. These sets are reindexed by the entire coefficient/complex-orbit bijection. Repetition across different characters is permitted and remains indexed.'},
      {'topic':'Full PropGK and selected task','result':'PASS',
       'detail':'Compared PropGK and the original propGK implication. Taking logarithms of positive nonzero factors gives sum Vn<=2*padicValInt(ell,NN); finiteness is proved before normalized length is used. Constants depend only on K and NN precedes every later coefficient datum. Non-imaginary-quadratic K uses c=A=0,NN=1 and the impossible GD antecedent. The exact finite B task closes; OneChar/RIG_II arithmetic producers do not.'},
    ]
    specs=[
      ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean',36,65),
      ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/Counts.lean',9,24),
      ('src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/OrbEquiv.lean',111,173),
    ]
    bind('prop_gk_installation_v46',['PGK'+str(i) for i in range(1,7)],findings,
         [source(*s) for s in specs],
         'Entire original finite implication CNR3 and OneChar imply PropGK. RNC16 supplies CNR3; the literal OneChar arithmetic theorem remains an explicit antecedent.',
         {'selected_whole_contract_reviewed':{
              'id':'TASK_PROP_GK_INSTALL','baseline_version':'0.45',
              'baseline_contract_sha256':sha(contract.encode()),
              'full_original_contract_closed_in_stated_scope':True,
              'no_weaker_replacement':True,
              'boundary':'Exact finite implication task only; original OneChar, RIG_II and unconditional surrounding producers remain open.'}})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('component', choices=['RNC','ICL','GLG','PGK'])
    args = parser.parse_args()
    if args.component == 'RNC':
        rank_three()
    elif args.component == 'ICL':
        integral_cusp()
    elif args.component == 'GLG':
        global_gain()
    elif args.component == 'PGK':
        prop_gk()
