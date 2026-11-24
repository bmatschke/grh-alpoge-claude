"""Hash-bind the HostRigid_s human proof to its original source interfaces."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
SOURCE = WORK.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
UD = AV + 'UnitaryThreeDeformations/'
UG = AV + 'UnitaryThreeGroups/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def src(path, declaration, start, end=None):
    data = (SOURCE / path).read_bytes()
    blob = subprocess.check_output(['git', 'show', PIN + ':' + path], cwd=SOURCE)
    assert data == blob, path
    lines = data.splitlines(keepends=True)
    end = end or len(lines)
    assert 1 <= start <= end <= len(lines), (path, start, end, len(lines))
    part = b''.join(lines[start - 1:end])
    return dict(path=path, declaration=declaration, line_start=start, line_end=end,
                sha256=sha(data), full_file_sha256=sha(data),
                range_sha256=sha(part), range_bytes=len(part),
                verified_equal_to_pinned_git_blob=True,
                url=URL + path + f'#L{start}-L{end}')


sources = {
    'endpoint': src(DT+'HostNumberS.lean', 'HostRigid_s', 12, 17),
    'bprime': src(DT+'ThmS6CoreS.lean', 'BPrime_s', 12, 16),
    'qi': src(AV+'AutomorphicCases/AutomorphyClauseStatement.lean', 'IsQi', 10, 10),
    'af': src(DT+'AfBridge.lean', 'AutOnAlt', 12, 16),
    'autcsda': src(AV+'ModularityArgument/AutomorphyLifting/IsAutCsdA.lean', 'IsAutCsdA', 11, 12),
    'autcsd0': src('src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/AdmissibleResidues/IsAutomorphicOverImagQuad.lean', 'AutCsd0', 35, 36),
    'autcsd': src(AV+'AutomorphicForms/BlochKatoSelmerVanishes.lean', 'IsAutCsd', 84, 86),
    'ad': src(AV+'AutomorphicForms/CongruenceNumberRankThree.lean', 'IsAdOf; AdVanishK', 158, 175),
    'bk': src(AV+'AutomorphicForms/BlochKatoSelmerVanishes.lean', 'decJ; IsBK; BlochKatoSelmerVanishes', 117, 144),
    'period': src(AV+'PadicHodgeTheory/FiniteCohomology.lean', 'PP; Bcr; actC; finiteCocycles', 78, 125),
    'coef': src(AV+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean', 'Coef', 10, 15),
    'parts': src(AV+'HeightAndVanishing/DirichletPrimeToLPartMulLPowerPart.lean', 'comp; kap; th0; psi2; c2; Sb; Tb', 73, 113),
    'data': src(UD+'IsHostFrame.lean', 'HostData; eta4; IsHostFrame', 12, 44),
    'point': src(UD+'IsCharZeroPt.lean', 'IsCharZeroPt; Rigid', 114, 126),
    'local': src(UD+'AdjointDiagonalRepPreservesWeightPiece.lean', 'Red; kerBar; TriIn; DiagIn; AdicCont', 18, 45),
    'frame': src(UD+'AdjointDiagonalRepPreservesWeightPiece.lean', 'Frame; loc; Iv; Nv; Tb; IsPt; Marked', 91, 145),
    'cob': src(UG+'BaseRepGL3NormalisedOfPsiEqOne.lean', 'HasMult; MatIrr; IsCoc; IsDeform; cob', 11, 62),
    'theta': src(UG+'UnitaryThreeReflectionRight.lean', 'Jmat; theta', 44, 82),
    'adjoint': src(UG+'UnitaryThreeReflectionRight.lean', 'thetaLie; GG.adFun', 155, 160),
    'tor': src(UG+'UnitaryThreeReflectionRight.lean', 'conjBy; adRep; wt1; tor; theta_tor; Normalised', 216, 289),
    'quotient': src('src/ReciprocityTheory/GaloisValuations/Global.lean', 'NS; GS; toGS; continuous_toGS', 128, 150),
    'complex': src('src/ReciprocityTheory/GaloisValuations/Global.lean', 'IsCC', 109, 110),
    'dyadic': src(UD+'DyadicCharacterPowerNeOne.lean', 'dyadic_character_power_ne_one; teichmuller_power_eq; res_ne', 50, 164),
    'sigma': src(UD+'DyadicCharacterPowerNeOne.lean', 'exists_sigma', 202),
    'subgroup': src(UD+'RigSub.lean', 'rig_sub', 47),
    'separate': src(UD+'RigSep.lean', 'rig_sep', 56),
    'eigen': src(UD+'RigEig.lean', 'rig_eig', 79),
    'desc': src(UD+'RigDesc.lean', 'rig_desc', 83),
    'fin': src(UD+'RigFin.lean', 'rig_fin', 51),
    'loc': src(UD+'RigLoc.lean', 'rig_loc', 35),
    'diag': src(UD+'RigDiag.lean', 'rig_diag', 23),
    'away': src(DT+'EHostRigidU.lean', 'rig_away', 85, 105),
    'above': src(DT+'EHostRigidU.lean', 'rig_above', 135, 183),
}

main = (HERE/'main.tex').read_bytes()
main_lines = main.splitlines(keepends=True)


def block(id_):
    start = next(i for i, line in enumerate(main_lines, 1)
                 if line.strip() == f'% BEGIN {id_}'.encode())
    end = next(i for i, line in enumerate(main_lines, 1)
               if line.strip() == f'% END {id_}'.encode())
    data = b''.join(main_lines[start - 1:end])
    return dict(file='host_rigidity_v42/main.tex', label='claim:'+id_,
                line_start=start, line_end=end, sha256=sha(data), bytes=len(data))


def claim(id_, title, scope, depends, keys, assumptions, progress):
    return dict(id=id_, title=title, introduced_in='0.42',
                status='human_implication_complete', mathematical_status=progress,
                scope=scope, depends_on=depends, assumptions=assumptions,
                remaining_inputs=[], sources=[sources[k] for k in keys],
                proof_location=block(id_))


claims = [
    claim('HSR1', 'Continuity, exact complex conjugation, and finite coefficients',
          'Actual IsCharZeroPt gives continuous r, original multiplier eta, r(c)=(1,-1), continuous full adjoint; all coefficients of each individual tangent and its finitely many bases descend to one finite local field. Also full RigDesc interface.',
          ['ADK1', 'NR19'], ['coef','point','local','frame','tor','complex','quotient','desc'],
          ['Original finite DVR coefficient model and IsCharZeroPt; continuous cocycle; specified compact group for general RigDesc.'],
          'human_proof_with_inherited_countable_field_lemma'),
    claim('HSR2', 'Dyadic conductor separation after reduction',
          'For a unit with 2-primary coordinate ell, its character value has fourth power nontrivial modulo the maximal ideal. Explicit conductor proof, CRT order/modulus distinction and prime-to-ell root injection. Also 2 notin Sb.',
          [], ['data','parts','dyadic'],
          ['ell odd; o>=1; c2>=4; 8 o ell^2<2^c2; all odd CRT components of th0 have exponent dividing2o.'],
          'human_proof_with_elementary_simplification'),
    claim('HSR3', 'Exact local subgroup and witness with epsilon=1',
          'Full rig_sub output on the actual stored ell-decomposition group, strengthening the cyclotomic closeness condition to epsilon(g)=1. Same H=ker eta intersect ker comp_ell psi.',
          ['HSR2','NR1','NR2','NR3','NR19'], ['data','parts','subgroup','sigma'],
          ['Original HostData and IsHostFrame; the actual valuation and root-of-unity actions.'],
          'human_proof_with_stronger_witness'),
    claim('HSR4', 'Eigenvalue separation in every triangular basis',
          'Exact rig_eig: in any triangular conjugate of the point at a marked-type element, all diagonal eigenvalues are units, have pairwise unit differences, and lambda_i != u lambda_j for |u-1|<1.',
          ['HSR1'], ['point','local','separate','eigen'],
          ['eta(g)=1 and Psi(g)^2-1 unit; original IsCharZeroPt.'],
          'human_proof_by_reduced_characteristic_polynomial'),
    claim('HSR5', 'Exact RigFin and RigLoc local finite implication',
          'Continuous full GG3 cocycle with upper-triangular dual deformation on an open connected subgroup, fixed strictly decreasing inertia powers, and noncyclotomic diagonal ratios is an original finiteCocycles class on the whole local group.',
          ['HSR1','RX2','BX1','BX2','BX3','BX4','DX1'], ['fin','loc','desc','period'],
          ['Same specified open local embedding; original dual-number deformation and arbitrary dual-number basis; no prime exclusion or unramified index restriction.'],
          'exact_interface_application_of_installed_local_calculation'),
    claim('HSR6', 'Explicit inertia primitives away from ell',
          'All allowed tangents are unramified classes at every p!=ell: quotient outside S, diagonal dual basis at Sb, and finite-index averaging elsewhere including p=2.',
          ['HSR2'], ['local','point','diag','away','quotient'],
          ['Original vanishing on Nv and DiagIn at Sb; original coefficient residue field is finite.'],
          'human_proof_with_explicit_primitives'),
    claim('HSR7', 'Every original host tangent is literal IsBK',
          'Continuous global tangent on the quotient gives the exact source IsBK, with original valuations, weights(e,0,-e), arbitrary local basis, exact noncyclotomic witnesses, and decJ graph/diagonal Bcris action.',
          ['HSR1','HSR3','HSR4','HSR5','HSR6','ADK5'], ['point','local','frame','above','bk','period'],
          ['All original Rigid antecedents, original HostData/IsHostFrame and IsCharZeroPt.'],
          'full_tangent_to_Selmer_matching'),
    claim('HSR8', 'Exact twist and full disconnected polarized adjoint',
          'Original BPrime_s supplies literal IsAutCsd for epsilon^-1 times the eta-kernel representation; original cyc is irreducibility on full cyclotomic kernel; actual normalized conjugation supplies P=J and multiplier epsilon^-2 for full M3.',
          ['HSR1','ADK2','ADK3','ADK6'], ['bprime','qi','af','autcsda','autcsd0','autcsd','ad','adjoint','theta','tor','complex'],
          ['Original IsQi, BPrime_s, same K-embedding supplied by AutOnAlt, and original normalized point. BPrime_s.opens retained but not used.'],
          'complete_direct_polarization_and_hypothesis_matching'),
    claim('HSR9', 'Full original HostRigid_s',
          'Every original point satisfying every original HostRigid_s antecedent is rigid, with one global matrix and exact cob sign; all odd ell, including selected e=1 ell=3,7 cases.',
          ['HSR7','HSR8','ADK6'], ['endpoint','point','bprime','cob','quotient'],
          ['Exactly the original HostRigid_s antecedents; installed human adjoint and local comparison theorems.'],
          'whole_leaf_human_discharge'),
]


def human(path, ids, ranges=None):
    data = (WORK/path).read_bytes()
    result = dict(file=path, sha256=sha(data), bytes=len(data), claims=ids)
    if ranges:
        lines = data.splitlines(keepends=True)
        result['claim_ranges'] = [dict(id=k, line_start=a, line_end=z,
            sha256=sha(b''.join(lines[a-1:z]))) for k,a,z in ranges]
    return result


inherited = [
    human('conditional_main_v42/main.tex', ['ADK1','ADK2','ADK3','ADK5','ADK6']),
    human('nonempty_realization/main.tex', ['NR1','NR2','NR3','NR19']),
    human('symplectic_actual_rigidity/main.tex', ['RX2'], [('RX2',201,326)]),
    human('bloch_kato_installation/main.tex', ['BX1','BX2','BX3','BX4'],
          [('BX1',62,142),('BX2',144,190),('BX3',192,282),('BX4',284,323)]),
    human('symplectic_local_installation/main.tex', ['DX1'], [('DX1',99,287)]),
]
adk_prov = json.loads((WORK/'conditional_main_v42/provenance.json').read_text())
primary = list(adk_prov['published_sources'])
primary.append(dict(id='FONTAINE1994', author='Jean-Marc Fontaine',
    title='Representations p-adiques semi-stables',
    publication='Asterisque 223 (1994), 113-184',
    url='https://www.numdam.org/item/AST_1994__223__113_0.pdf',
    theorem='Proposition 1.5.2, printed p.124; sections5.1.3-5.1.7, printed pp.155-158, including unramified representations in5.1.5.',
    application='Inherited from RX2: unramified crystalline representations, exact tensor/subquotient category, crystalline comparison and finite-coefficient splitting. No new published matching leaf is assumed.'))

baseline = json.loads((WORK/'dependency_audit_v0_41/remaining_leaf_register.json').read_text())
leaf = next(r for r in baseline['records'] if r['id']=='HOST_RIGID_S')

review_files = [
    'reviews_v0_42/host_rigidity_v42_root_review.json',
    'host_rigidity_v42/review_HSR_global_estimates.json',
]
reviews = []
for path in review_files:
    data = (WORK/path).read_bytes()
    record = json.loads(data)
    result = record.get('result', record.get('status'))
    reviewed_sha = record.get('proof_sha256', record.get('reviewed_sha256'))
    assert result == 'PASS', path
    assert reviewed_sha == sha(main), path
    reviews.append(dict(file=path, sha256=sha(data), result=result,
                        proof_sha256=reviewed_sha))

provenance = dict(schema='rh-human-reconstruction-component/2', artifact_version='0.42',
    component='host_rigidity_v42',
    repository='https://github.com/CocoSgt/riemann-hypothesis-lean', commit=PIN,
    scope='Full original HostRigid_s by exact tangent-to-Bloch-Kato, epsilon^-1 twist, normalized pairing J, ADK6 and inherited RX2. No quantitative host or automorphy producer claimed.',
    proof_sha256=sha(main), claims=claims, inherited_human_proofs=inherited,
    published_sources=primary,
    validation=dict(source_pin_verified=True, source_ranges_byte_checked=True,
        source_assumption_audit='No new Lean replay or source dependency audit claimed; source files define the exact contracts, human proof is given independently.',
        mathematical_review='Author completed; root and independent global-estimates agent both passed HSR1-HSR9 on the frozen final proof bytes. Review records are hash-bound below.',
        completed_reviews=reviews,
        tex='Environment nesting checked; integrated rendering is owned by root.'))

contracts = dict(schema='rh-host-rigidity-contracts-v1', artifact_version='0.42',
    source_commit=PIN, proof_sha256=sha(main), original_leaf=leaf,
    exact_endpoint=sources['endpoint'], claims=claims,
    interfaces={k:sources[k] for k in ['data','point','local','bprime','ad','bk','subgroup','eigen','desc','fin','loc','diag']},
    closed_candidate=dict(id='HOST_RIGID_S', proof_claim='HSR9',
        status='human_discharge_complete_independently_reviewed_pending_integration',
        completed_reviews=reviews,
        scope='The whole universal original theorem, stronger than the selected original CountV restriction. No fixed-target hypothesis is enlarged.',
        dependencies=['ADK6','HSR1','HSR2','HSR3','HSR4','HSR5','HSR6','HSR7','HSR8','RX2','BX1','BX2','BX3','BX4','DX1','NR1','NR2','NR3','NR19']),
    exact_dictionary=dict(K='The AutOnAlt embedding has image Q(i); its GK is exactly ker eta4.',
        twist='epsilon^-1 times the literal matrix representation on GK.',
        cyclotomic_kernel='Full closed ker cycBar=ker cycZ=G_{K(mu_ell^infinity)}.',
        pairing='P=J, the symmetric antidiagonal matrix; multiplier epsilon^(1-3)=epsilon^-2.',
        disconnected_action='At the actual normalized complex conjugation: X maps to -J X^t J on all M3.',
        local_coefficients='Each cocycle and its finitely many bases have a finite coefficient field by the group/cocycle Baire argument.',
        at_ell='H=ker eta4 intersect ker comp_ell(psi); inertia diagonal epsilon^(e,0,-e); witness epsilon(g)=1 and Psi(g)^2-1 unit; ordinary calculation RX2; finite-index descent with full diagonal Bcris action.',
        away='Diagonal derivative primitive -h1 h0^-1 on Sb; finite-index inertia averaging elsewhere; quotient kills inertia outside S.',
        final_sign='BK primitive v gives source cob primitive X=-v; descend by quotient surjectivity.'),
    strengthened_intermediate_outputs=['epsilon(g)=1 in rig_sub, rather than only |epsilon(g)-1|<1',
        'All triangular eigenvalue differences have norm1, implying exact rig_eig'],
    original_hypotheses_retained_but_unused=['BPrime_s.opens','HostData inequalities at p in Sb; only p=ell needed here','Some IsPt normalization/local clauses beyond residual and complex-conjugation normalization'],
    remaining_inputs=[],
    untouched_frontier=['Automorphic point construction and BPrime_s producer','HostNumber_s quantitative bound','All other remaining construction, congruence, geometric and global gap leaves'],
    progress_accounting=dict(proof_progress=['Complete original HOST_RIGID_S matching via HSR9',
            'Direct literal J-pairing avoids an auxiliary alternate polarization construction',
            'Corrected local Frobenius strengthens and simplifies the rig_sub witness'],
        inherited_exposition=['RX2 ordinary crystalline induction and finite-index descent, instantiated with all literal source hypotheses'],
        no_full_RH_claim=True))

report = '''HOST RIGIDITY, v0.42

MATHEMATICAL RESULT
HSR1-HSR9 provide a complete human proof of the whole original HostRigid_s
statement at the pinned source commit. This is stronger than the selected
CountV scope (including e=1 and ell=3,7) and retains every original antecedent.
The whole-leaf closure HOST_RIGID_S passed both root and independent reviews
on the frozen proof bytes; ledger integration is owned by root. It is a
reconstruction matching result, not a new claim
that RH/GRH or all host arithmetic producers are finished.

KEY STEPS
* The actual finite-DVR point gives norm continuity and r(c)=(1,-1).
* The dyadic conductor calculation supplies a residue separation witness.
  Correct arithmetic Frobenius by inertia to make epsilon(sigma)=1 exactly,
  then take g=sigma^2. This lies in the actual rig_sub subgroup and gives
  Psi(g)^2-1 a unit. The original cyclotomic norm inequality is strengthened.
* Reduction of the characteristic polynomial proves rig_eig in every
  triangular basis, without a basis-change integrality assumption.
* HSR5 matches RigDesc/RigFin/RigLoc to the already proved RX2 calculation:
  finite coefficient capture; all dual-number unramified diagonal variations;
  strictly decreasing weights; exact noncyclotomic ratios; Bcris splitting;
  and finite-index averaging for the full disconnected diagonal action.
* HSR6-HSR7 produce the literal global IsBK condition with actual valuations,
  exact decJ graph topology and explicit inertia primitives.
* BPrime_s.aut supplies the precise epsilon^-1 twist; BPrime_s.cyc supplies
  irreducibility on the full infinite cyclotomic kernel. The normalized
  complex-conjugation matrix makes P=J literally, with multiplier epsilon^-2
  and negative transpose on all M3. ADK6 therefore applies directly.
* Quotient surjectivity and X=-v give the exact source Rigid coboundary sign.

INHERITED INPUTS
ADK1-ADK6 (already independently reviewed); NR1-NR3 and NR19;
BX1-BX4 and DX1; RX2. No unproved source LocalPublishedTheorems package is
silently imported: the specific mathematical calculation is RX2 and is
recalled in the text with every hypothesis matched.

VALIDATION AND OWNERSHIP
Source ranges are byte-compared to commit
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
All claim proof blocks and inherited human files are hash-bound.
Complete independent reviews of HSR1-HSR9 both passed:
reviews_v0_42/host_rigidity_v42_root_review.json and
host_rigidity_v42/review_HSR_global_estimates.json.
Both records are hash-bound in provenance.json and contracts.json.
Root owns integration and final
rendering/saving. No new Lean replay or whole repository axiom audit is claimed.

UNCHANGED WORK
No HostNumber_s quantitative estimate, automorphy/point producer, compatible
host construction, or global gap supplier is closed by this packet.
'''

for name, obj in [('provenance.json', provenance), ('contracts.json', contracts)]:
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
(HERE/'report.txt').write_text(report)
hashes = {name:sha((HERE/name).read_bytes()) for name in
          ['main.tex','provenance.json','contracts.json','report.txt','build_metadata.py']}
(HERE/'hashes.json').write_text(json.dumps(hashes, indent=2)+'\n')
print(json.dumps(hashes, indent=2))
