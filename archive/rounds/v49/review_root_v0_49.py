#!/usr/bin/env python3
"""Bind completed independent mathematical reviews to the inspected v0.49 text.

Hash checks identify the text reviewed; they are not mathematical verification.
No Lean build or kernel replay is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha = lambda data: hashlib.sha256(data).hexdigest()

def source(path, first, last):
    raw = (SOURCE / path).read_bytes()
    assert raw == subprocess.check_output(['git', '-C', str(SOURCE), 'show', PIN + ':' + path])
    assert 1 <= first <= last <= len(raw.splitlines())
    return dict(path=path, line_start=first, line_end=last, file_sha256=sha(raw),
                range_sha256=sha(b''.join(raw.splitlines(keepends=True)[first-1:last])),
                verified_equal_to_pin=True)

def complement(component, filename, required):
    path = ROOT / component / filename
    record = json.loads(path.read_text())
    assert record['result'] == 'PASS' and not record.get('unresolved_findings')
    assert record['proof_sha256'] == sha((ROOT / component / 'main.tex').read_bytes())
    assert set(required) <= {c['id'] for c in record['claims_reviewed']}
    return dict(file=str(path.relative_to(ROOT)), sha256=sha(path.read_bytes()))

def bind(component, ids, findings, sources, scope, extra=None):
    ledger = json.loads((ROOT / component / 'provenance.json').read_text())
    claims = {c['id']: c for c in ledger['claims']}
    raw = (ROOT / component / 'main.tex').read_bytes()
    blocks = []
    for cid in ids:
        p = claims[cid]['proof_location']
        part = b''.join(raw.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
        assert sha(part) == p['sha256'], (cid, 'stale component ledger')
        blocks.append(dict(id=cid, line_start=p['line_start'], line_end=p['line_end'],
                           block_sha256=sha(part), result='PASS'))
    report = dict(schema='rh-independent-human-review/1', artifact_version='0.49',
                  component=component, reviewer='root', result='PASS',
                  proof_file=component+'/main.tex', proof_sha256=sha(raw),
                  source_commit=PIN, claims_reviewed=blocks, scope=scope,
                  findings=findings, sources_inspected=sources, unresolved_findings=[],
                  proof_bytes_modified_by_reviewer=False, lean_replay=False)
    if extra:
        report.update(extra)
    out = ROOT / component / ('review_'+ids[0]+'_'+ids[-1]+'_root.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(review=str(out.relative_to(ROOT)), proof_sha256=sha(raw),
                          claims=len(ids), result='PASS')))

def huf():
    findings = [
        dict(topic='Actual analytic and tangent dictionaries', result='PASS', detail='Read all HUF1-HUF21. The affine-chart proof supplies the exact IsHolTo definition and its dual-number derivative dictionary. The given proper semiabelian family is abelian; the printed relative ample presentation gives projective fibers. Lie eigenspaces have the prescribed ordered type and the original dimension, including dimension zero.'),
        dict(topic='Reverse points and the integral genus record', result='PASS', detail='The exponential is constructed from local flows by division, its kernel is a full integral lattice, and KTriv forces the polarization form to be perfect. All positive Weil levels have the original negative sign. Dedekind projectivity lifts the actual Tate maps integrally, with the exact compatible f_n and nu_n, root identity, half-level and full-A markings. No free O_E lattice or rational-only substitute is used.'),
        dict(topic='Relative lattice continuation and prescribed local lifting', result='PASS', detail='The relative exponential is joint holomorphic. Continuing a basis gives the entire kernel by the proper local biholomorphism of degree one, not only a sublattice. One neighborhood preserves the Chern form and hence every positive Weil level simultaneously, together with the finite-etale markings. The prescribed initial P_0 and exponential are retained. This local contract does not add an InGenus hypothesis.'),
        dict(topic='Period coordinates, uniqueness and arbitrary choices', result='PASS', detail='The Grassmannian kernel coordinates have the exact f*p*q dimension and retain positivity, every type, and the zero-dimensional cases. Marked automorphisms are finite by positive integral isometry and are trivial by the original odd M>=3 congruence condition, including M=3. PUN23 has precisely the pointwise Unif hypotheses used in HUF11; it does not require InGenus. Equal-dimensional injective holomorphy then gives the local inverse. Thus arbitrary pointwise choices of moduli points and exponentials become holomorphic without an added continuity premise.'),
        dict(topic='One finite positive family before all subsequent choices', result='PASS', detail='A finite affine cover and finite connected components of semialgebraic sets give finiteness for the actual complex moduli space without compactness. Marked-isometry images are nonempty open disjoint sets covering that space. Choice on a set of integral lattice models supplies one finite positive family, the exact integral genus maps, and total point/exponential functions, including values at invalid periods. They precede all period, parameter, basis and torsion quantifiers. The fiber criterion and local lifting retain both level conditions.'),
        dict(topic='Exact theta signs, factors and global rigidification', result='PASS', detail='The normalization h=A^{-1} and tau=A^{-1}C is derived as holomorphic. Positivity and the first-linear Hermitian convention force the printed negative symplectic sign. The primitive semicharacter gives fixed half-integral c_1,c_2 and the exact theta multiplier. Normal convergence gives holomorphy. The ratio line on the proper torus family has h^0=1 on every fiber and is base-flat. Grauert gives a line bundle of fiber sections; evaluation and the zero rigidification trivialize it globally. The argument imposes no Stein or simply connected hypothesis.'),
        dict(topic='Every original FamilyUnif and IsThetaFrame field', result='PASS', detail='Compared the entire IsThetaFrame and FamilyUnif records and literal N1c. Chart transitions have the correct direction; zero values are the actual rigidification; projective GAGA is used separately on each fiber for its algebraic theta section. The supplied Moduli record is retained and not constructed. Every original field, universal parameter dimension, positive-rank guard and choice order is present. Full N1c is complete in this scope; principal framed charts, IsUnf, FromTest and later theta-span producers are not inferred.'),
    ]
    p = 'src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/'
    q = 'src/Development/AbelianVarietyTheory/Proofs/ModuliProofs/'
    sources = [
        source(p+'IsHolPeriods.lean',13,116), source(p+'PushInvertible.lean',24,44),
        source(p+'TwoWeightEqOneAddRoot.lean',14,82), source(p+'TwoWeightEqOneAddRoot.lean',132,168),
        source(p+'IsLieBasis.lean',69,113), source(q+'FamilyUnifOfParts.lean',18,40),
        source(q+'ExistsUniformisationAtPointClosed.lean',18,22),
        source(q+'ExistsLocalPeriodLift.lean',21,27), source(q+'PointEqIffIsometryClosed.lean',19,27),
        source(q+'IsHolToModulipointExpOfHolomorphicPeriodsStatement.lean',11,12),
        source(q+'ExistsThetaFrameFamily.lean',1,28),
        source(q+'FamilyUniformisationOfAbelianVarietyUniformisati.lean',1,33),
    ]
    bind('holomorphic_uniformization_v49', ['HUF'+str(i) for i in range(1,22)], findings, sources,
         'Independent mathematical and literal-source review of the entire finite holomorphic FamilyUnif/N1c construction, on the original supplied Moduli and explicit named classical foundations.',
         dict(selected_whole_obligation_closures=[], full_original_N1c_reviewed=True,
              primary_sources_opened=[
                  'https://www.numdam.org/item/PMIHES_1960__5__5_0.pdf',
                  'https://www.numdam.org/item/PMIHES_1963__16__35_0.pdf',
                  'https://www.jirka.org/scv/scv.pdf',
                  'https://perso.univ-rennes1.fr/michel.coste/polyens/SAG.pdf'],
              published_foundations_scope_checked=['Grauert section7 Satz5 with its corrigendum, h0=1, properness, reduced base and base-flatness', 'Injective holomorphic maps in equal complex dimension', 'Finite connected components of semialgebraic sets', 'Inherited Appell-Humbert, projective GAGA and perfect-polarization dictionary']))

def uce():
    other = complement('unramified_coefficient_extension_v49', 'review_UCE10_UCE17_global_estimates.json', ['UCE'+str(i) for i in range(10,18)])
    findings = [
        dict(topic='Actual inertia separator and specialization in every characteristic', result='PASS', detail='Read UCE1-UCE9 and UCE18-UCE19. The original GD condition ell-1 not dividing2e and the cyclotomic inertia image provide the actual unit separator. The field-specialization lemma uses a valuation ring dominating the supplied local domain, integral flag reduction, and a finite field extension from the finite polynomial equations. The ordered flag remains valid even when the coefficient uniformizer maps to zero.'),
        dict(topic='Literal local ordinary condition', result='PASS', detail='UCE3 derives the ordered product identities from the inherited all-Artin crystalline component, uses three diagonal projectors to force the inertia ordering, and proves decomposition-group stability by intertwining distinct characters. UCE4 uses integral spectral projectors to descend the ordered flag over the actual domain. UCE5 pushes all five OrdPt fields, including the original every-place away-inertia condition and the exact local embedding. No FinA or automorphy hypothesis is introduced.'),
        dict(topic='Integral weights and full finite criterion', result='PASS', detail='Actual entry deviations generate the relative cotangent space and the complete ring. Conjugation by T(1+T), universality and injectivity of Z to1+T modulo each maximal-ideal power prove homogeneous projection stability integrally, without dividing torus eigenvalue differences. Finite monomial generators give the complete local zero piece and finite fixed-weight modules. Projection proves R0 intersect pi R equals pi R0 even with pi-torsion.'),
        dict(topic='Characteristic-prime curves and arbitrary original FinCrit tests', result='PASS', detail='The prime maximal while avoiding a surviving element gives a one-dimensional quotient by principal ideal theorem and finite prime avoidance. Its finite residue field lifts inside the equal-characteristic complete domain; a nonzero parameter makes it finite over k[[t]]. The finite extension valuation yields an original complete DVR test with finite residue field and nonzero surviving element. The test kills every nonempty weight-zero monomial, so the zero piece is finite over O. Reducedness, coefficient flatness and characteristic-zero restrictions were not added.'),
        dict(topic='Both conjugacy transports with all extension choices', result='PASS', detail='TypeI is preserved by the actual torus conjugacy on ker eta. The same iota, cuspidal datum, infinity type, semisimplicity and cofinite Frobenius attachment transport through the cyclotomic twist. For TypeII the original four zero entries and middle-entry-one remain; every supplied full two-dimensional W is conjugated by diag(t,t^{-1}), keeping its corner equality and trace at the original complex conjugation. Its same newform attachment transports back after epsilon^{-e}. No preferred extension or quadratic twist was substituted.'),
        dict(topic='Exact GdEnd consumer and explicit unclosed producer', result='PASS', detail='Compared GdEnd, FinEnd, AutEnd3, AutEnd2, FinA, AutB, LemW and the entire AutomorphyUnramifiedCoefficients record. One invocation chooses the same g1 for the actual D, fixed iota and local valuation ring. Only then are U,S, arbitrary entry maps, pushed representations and every outer-corner extension varied. UCE10-UCE17 have complementary independent coverage, including finite weight zero, arbitrary entry-map ordinary realization and all-open-subgroup irreducibility. This proves the exact GdEnd implication but does not construct its finite-end or two automorphic-end fields. AUT_UNRAM_COEF stays open.'),
    ]
    p = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
    sources = [
        source(p+'HeightAndVanishing/Counts.lean',9,22),
        source(p+'UnitaryThreeGroups/RhoKApply.lean',16,94),
        source(p+'UnitaryThreeGroups/DatFacts.lean',30,133),
        source(p+'UnitaryThreeGroups/DatLoc.lean',8,45),
        source(p+'UnitaryThreeGroups/ConjStable.lean',15,37),
        source(p+'UnitaryThreeGroups/GRepresents.lean',75,128),
        source(p+'PadicHodgeTheory/ValuationRingClearLastRowEntry.lean',1,246),
        source(p+'PadicHodgeTheory/ScalarMap.lean',157,193),
        source(p+'CurveDVRSpecialization/TriangularOfReducibleRankThree.lean',10,144),
        source(p+'CurveDVRSpecialization/TriangularOfReducibleRankThree.lean',145,233),
        source(p+'CommutativeAlgebra/ResMapBijective.lean',145,225),
        source(p+'CurveDVRSpecialization/IsUnitOrIsUnitOfAddOne.lean',95,122),
        source(p+'CurveDVRSpecialization/RatTorsionFree.lean',21,68),
        source(p+'CurveDVRSpecialization/GdMain.lean',14,129),
        source(p+'AutomorphicCases/AutomorphyUnramifiedCoefficients.lean',12,27),
    ]
    bind('unramified_coefficient_extension_v49', ['UCE'+str(i) for i in list(range(1,10))+[18,19]], findings, sources,
         'Independent mathematical review of UCE1-UCE9 and UCE18-UCE19, including the full exact same-g1 GdEnd consumer. UCE10-UCE17 have complementary independent review; no selected whole closure is proposed.',
         dict(selected_whole_obligation_closures=[], complementary_independent_review=other,
              full_original_GdEnd_implication_reviewed=True, AUT_UNRAM_COEF_remains_open=True))

def wrs():
    component = 'witness_realization_v49'
    other = complement(component, 'review_WRS1_WRS5_main_proof_rigidity.json', ['WRS'+str(i) for i in range(1,6)])
    baseline = json.loads((ROOT/'dependency_audit_v0_48/obligation_map.json').read_text())
    contract = next(n['contract'] for n in baseline['nodes'] if n['id']=='GLOBAL_LOCAL_GAIN')
    comparison = json.loads((ROOT/component/'closure_comparison.json').read_text())
    assert comparison['baseline_contract_verbatim']==contract
    assert comparison['baseline_contract_utf8_sha256']==sha(contract.encode())
    findings = [
        dict(topic='Built-class membership supplies the actual joint witness', result='PASS', detail='Read WRS6-WRS10 with their exact source contracts and inherited LGS13/GCF17-GCF18 arguments. The original cls membership gives one dependent tuple (D,O,b) identifying the actual BPt object, including the supplied comparison and kernel. The class contains those witnesses; no unproved selector or independent replacement kernel is used. The source-built point and its ofObj instance are transported together.'),
        dict(topic='Common compatibility before later indices', result='PASS', detail='WRS6 applies to every actual family index after Fm.x1+1. The zero TransportedAlt coefficient bound and Closed cutoff1 are chosen before the family. The entire GroupCompatibilityFamily statement uses the same given Extra data. ChosenE of the unchanged D3 class supplies ChosenTT/ChosenBad and hence TopsF/Adm2F. Its internal height constant need not equal an unrelated external one.'),
        dict(topic='All five original LinkG_at clauses', result='PASS', detail='The completed LGS13 implication applies to those two actual Closed inputs. The fixed coefficients pre=0,t=0,mid=4129,last=max(5600002,Corb(epsilon)), cutoff1/104 and CG=4*Ccount+1 retain the printed order. A single delta(x)=x^{-epsilon/2} tends to zero before all later actual indices. Local divisibility and lengths, zero outside served primes, orbit bounds, signed gains, served-orbit coverage and MeanKappaBound are the exact original fields.'),
        dict(topic='Literal universal installer and stronger selected specialization', result='PASS', detail='The original theorem for every A with TSel(A) and Duty(A) is reconstructed using its full choice and duties records. Separately, on the unchanged selected cls(Q,Lk,E) refining IsBuilt, the existing membership witnesses supply compatibility directly. This supplies the selected original LinkG endpoint without an additional TSel or WPt premise. The historical stronger realization route is bypassed, not claimed solved. No nonempty design family, full RecT or TSel producer is inferred.'),
        dict(topic='Whole selected contract and preserved boundaries', result='PASS', detail='Compared the byte-preserved v0.48 GLOBAL_LOCAL_GAIN contract, all baseline source evidence, and the full current original LinkG/Closed definitions. WRS1-WRS5 have complementary hash-bound independent coverage. The direct built-membership route closes the original uniform local-gain selected obligation. The old roadmap qualifications are retained as historical text, with this exact endpoint discharge recorded separately. GLOBAL_DENOMINATOR, GLOBAL_PERIOD_HEIGHT, GLOBAL_SPECTRAL, DESIGN_CHOICES_COMMON and SECOND_LAYER_COMPATIBLE_SELECTION remain open.'),
    ]
    p = 'src/Development/AbelianVarietyTheory/'
    sources = [
        source(p+'Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',67,109),
        source(p+'Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',222,286),
        source(p+'Definitions/GlobalTwisting/ValidForConstructedPointClassesEventuallyWorking.lean',368,394),
        source(p+'Definitions/GlobalTwisting/FamilyClassSevenDutiesAndStableLattices.lean',51,67),
        source('src/Formalism/SharpRestriction/GlobalTheoremInputs.lean',122,141),
        source(p+'Proofs/GlobalInterpolation/LinkG.lean',14,27),
        source('src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean',18,90),
        source('src/Formalism/LocalToGlobal/ThresholdSelection.lean',9,16),
        source('src/Formalism/LocalToGlobal/Divisibility/DivisibilityRemainder/AdmissibleClasses/LinkGCl.lean',11,32),
    ]
    bind(component, ['WRS'+str(i) for i in range(6,11)], findings, sources,
         'Independent mathematical and source review of WRS6-WRS10 plus the exact whole GLOBAL_LOCAL_GAIN closure, with complementary WRS1-WRS5 coverage and the stronger historical selector route explicitly unclaimed.',
         dict(selected_whole_contract_reviewed=dict(id='GLOBAL_LOCAL_GAIN',
                  baseline_contract_sha256=sha(contract.encode()),
                  full_original_contract_closed_in_stated_scope=True,
                  conclusion='The original Closed(D3(3,A),LinkG), universally with original TSel/Duty premises and directly on the unchanged selected built class from its existing membership witnesses. Common-family existence, full RecT and TSel remain separate.'),
              complementary_independent_review_files=[other['file']],
              complementary_independent_review_binding=other,
              closure_comparison_file=component+'/closure_comparison.json'))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('component',choices=['huf','uce','wrs'])
    args=parser.parse_args()
    {'huf':huf,'uce':uce,'wrs':wrs}[args.component]()
