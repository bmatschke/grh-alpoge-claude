#!/usr/bin/env python3
"""Record the root's completed independent mathematical/source reviews.

Hash checks bind the inspected text; they do not establish mathematical truth.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
sha=lambda data:hashlib.sha256(data).hexdigest()
def source(path,first,last):
 raw=(SOURCE/path).read_bytes()
 assert raw==subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path])
 return dict(path=path,line_start=first,line_end=last,file_sha256=sha(raw),range_sha256=sha(b''.join(raw.splitlines(keepends=True)[first-1:last])),verified_equal_to_pin=True)
def bind(component,ids,findings,sources,scope,extra=None):
 ledger=json.loads((ROOT/component/'provenance.json').read_text());claims={c['id']:c for c in ledger['claims']}
 raw=(ROOT/component/'main.tex').read_bytes();blocks=[]
 for cid in ids:
  p=claims[cid]['proof_location'];part=b''.join(raw.splitlines(keepends=True)[p['line_start']-1:p['line_end']])
  assert sha(part)==p['sha256'],(cid,'stale ledger')
  blocks.append(dict(id=cid,line_start=p['line_start'],line_end=p['line_end'],block_sha256=sha(part),result='PASS'))
 report=dict(schema='rh-independent-human-review/1',artifact_version='0.48',component=component,reviewer='root',result='PASS',proof_file=component+'/main.tex',proof_sha256=sha(raw),source_commit=PIN,claims_reviewed=blocks,scope=scope,findings=findings,sources_inspected=sources,unresolved_findings=[],proof_bytes_modified_by_reviewer=False,lean_replay=False)
 if extra:report.update(extra)
 out=ROOT/component/('review_'+ids[0]+'_'+ids[-1]+'_root.json')
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(review=str(out.relative_to(ROOT)),proof_sha256=sha(raw),claims=len(ids),result='PASS')))

def pun():
 findings=[
  dict(topic='Fixed Hermitian space and complete local scope',result='PASS',detail='Read all PUN1-PUN24 proofs. The ternary quadratic norm argument retains square delta, all finite places including dyadic places, and every real embedding. The Hermitian local-global induction handles the isotropic zero case and local cancellation, including split algebras. The actual Host unramified condition permits the common trace-dual fractional ideal to be scaled to unimodular lattices. This preserves the given Gm and xi, rather than merely producing an isomorphic replacement space. The zero-xi case is handled by perfection forcing rank zero.'),
  dict(topic='Full arithmetic lattice model',result='PASS',detail='Compared the actual LatModel and ModelsOf contracts. Half-level congruence and dual perfection give equality with the full principal congruence kernel for lcm(M,A). The coset bound, bounded-powers flag stabilizer and odd-prime congruence argument supply the original index and free-action fields. One transvection modulus is chosen before all vectors and scalars. ModelsOf, ModelBase and NegXi remain conditional on the supplied FamilyUnif.'),
  dict(topic='Actual center lattice and exact exponent',result='PASS',detail='The center is an injective additive skew-matrix group of the original dimension. Finite index, without normality, gives finite generation and the full rational span of the actual zGam. The adapted projective cusp lattice gives the precise different and ideal factors. The source prE divides kappa0 by two: the resulting one-half rational trace is checked by the trace-one host element, not by an invalid integral division by two. General basis transport uses the correct transpose and conjugate matrices. The complete ExpoMatch endpoint retains A=1.'),
  dict(topic='Actual primitive line and nonreduced test rings',result='PASS',detail='The semicharacter alpha(Pa)=exp(pi*i*B(a,w0*a)) and Appell-Humbert factors specify the original line, its rigidification, symmetry, adjoint and cubical structures. Positivity yields algebraization and perfect B yields a principal polarization. The dual Picard universal property for every scheme, including nonreduced schemes, gives the full KTriv for every C-algebra. This is stronger than checking only complex-valued points. The original IsAHframe transformation direction and tangent dual-number condition were compared directly.'),
  dict(topic='Weil sign, original markings and every scalar extension',result='PASS',detail='The multiplication order in the literal commutator gives exp(-2*pi*i*B(a,b)/n), the required negative Weil sign. Every positive torsion level, the same f_n and nu_n, both half/full markings and the exact TateIso are retained. Obj.geom is verified after every C-to-k scalar extension, including noncontinuous embeddings, by algebraic finite-etale torsion base change. The given moduli representation supplies the actual point.'),
  dict(topic='Point equality and marked genus nonemptiness',result='PASS',detail='The actual semicharacter shows that an integral marked isometry preserves the primitive line, not only its polarization. This gives the complete point_eq_iff_isometry_closed contract. Local unit-norm surjectivity constructs a profinite lift with the correct norm and residue simultaneously, hence all compatible f_n and the original root identity at every prescribed sigma. No global norm solution is assumed.'),
  dict(topic='Remaining uniformization scope',result='PASS',detail='The full FamilyUnif definition was compared, including finite components, holomorphic families, theta frames and local lifting. Individual points, their equality and ModelsOf on a supplied family do not imply N1c. That original global holomorphic and normalized-family producer, and the later spanning inputs, remain open. No selected whole leaf is closed by this component.')
 ]
 p='src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/'
 q='src/Development/AbelianVarietyTheory/Proofs/'
 sources=[source('src/Development/AbelianVarietyTheory/PublishedTheorems/Landherr₂/ExistsNormTensor.lean',10,29),source(q+'UnitaryExistence/LatticeModelOfSameSignatureHasseNorm.lean',24,75),source(q+'UnitaryExistence/ExistsFlagDomainModelsOfFamilyUniformisation.lean',66,149),source(p+'BirationalGeometry/ToroidalCompactification/IsHolPeriods.lean',41,116),source('src/Formalism/LocalToGlobal/ProjectiveLattices/IntegrableOnIntegrand.lean',139,205),source('src/Formalism/LocalToGlobal/ProjectiveLattices/IntegrableOnIntegrand.lean',231,255),source(p+'BirationalGeometry/ToroidalCompactification/IsLieBasis.lean',69,111),source(p+'BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean',72,82),source(p+'BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean',131,168),source(q+'ModuliProofs/ExistsPointOfIsPeriod.lean',24,33),source(q+'ModuliProofs/PointEqIffIsometryClosed.lean',19,27),source(q+'ModuliProofs/FamilyUnifOfParts.lean',18,42),source(q+'ModuliProofs/FamilyUnifOfParts.lean',63,84)]
 bind('principal_uniformization_v48',['PUN'+str(i) for i in range(1,25)],findings,sources,'All twenty-four actual arithmetic-model, center-lattice, exponent, period, primitive-point and point-equality proofs at the complete stated source scopes; full N1c remains separate.',{'selected_whole_obligation_closures':[],'primary_sources_opened':['https://www.jmilne.org/math/CourseNotes/AV.pdf','https://math.stanford.edu/~conrad/papers/cmchina.pdf','https://numdam.org/item/AIF_1956__6__1_0/'],'published_foundations_scope_checked':['Appell-Humbert theorem','Polarizable complex tori and abelian varieties','Ample criterion and GAGA','Picard dual universal property on every scheme, including nonreduced bases']})

def gcf():
 findings=[
  dict(topic='Actual finer determinant quotient',result='PASS',detail='Read GCF1-GCF6 and GCF12-GCF18. Hilbert-90 lifts are integral at almost every finite place, so they belong to the actual restricted product. The kernel, unit-image quotient and rational map are computed in KDq, not only in the ideal class quotient. The exact actual SG=(B.primes X).vGs is essential: it has no extra primes, and the selected paired congruence conditions are precisely the original ones.'),
  dict(topic='Relative determinant and prescribed columns',result='PASS',detail='The positive-part decorated ideal and determinant use the same given Reads frames and satisfy the full relative law in arbitrary rank. No globally free basis is assumed for self-dual lattices. The full columns extension preserves the supplied compatible group g. The actual element and object equalities are retained through the quotient and column constructions.'),
  dict(topic='All group-compatibility fields on one tuple',result='PASS',detail='Checked the canonical packC and gatOf tuple, using completed local isometry, self-duality, comparison, character and volume inputs at their exact scopes. The proof supplies the Hermitian and form fields, the whole CmpTied record, all four ring isomorphisms and five commuting identities, and GatIs. The exact IsRecG stores the same joint tuple. GCF7-GCF11, independently reviewed by main_proof_rigidity, supply the actual required period normalization.'),
  dict(topic='Choice order and complete true-volume stage',result='PASS',detail='Read the entire original exists_trueVolume_stage_of_any_column_choice. A single original GJStage is chosen before every later W,V,S,N. The stage-independent column and comparison maps, true-volume identity, original rational characters and normalized period supply VolTieG, GatNum and ColumnDataSplitPrimes on that same G. No per-later-stage choice has been substituted.'),
  dict(topic='Division transport and actual comparison map',result='PASS',detail='For arbitrary original submodules N and height functions h, the defining comparison polynomials and universal uniqueness give literal equality of the comparison map under setDiv. The full IsRecG and column-local-data records transport together; the period is unchanged. The four-component tuple in GCF17 includes the given Extra.cmp and kernel data, so an unrelated new comparison map cannot satisfy the conditional realization premise.'),
  dict(topic='Selected tops and remaining common-family producer',result='PASS',detail='The source ChosenE definition supplies ChosenTT and ChosenBad on the actual D3 family. The simultaneous threshold max{xa,xb,x1+1,(16*Cb+2)^(3/eps)} yields TopsF and the previously proved GLG16 gives Adm2F. Thus selected-top admission is not an additional producer on this selected class. The full class-level LinkG theorem still requires its original common realization or TSel, and GCF17 is conditional on the actual joint WPt realization. No GLOBAL_LOCAL_GAIN or other whole selected leaf is closed.')
 ]
 d='src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
 p='src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/'
 sources=[source(d+'IsRationalUnitaryDeterminantMapRationalUnitary.lean',16,125),source(d+'IsRationalUnitaryDeterminantMapRationalUnitary.lean',208,238),source(d+'ReferenceCharactersFactorTame.lean',34,182),source(d+'ReferenceCharactersFactorTame.lean',430,551),source(p+'H90USurjective.lean',168,242),source(p+'PointDeterminantEqNormOneClassOfLevel.lean',13,50),source(p+'LevOkTwists.lean',21,85),source(p+'ExistsFullHermitianColumnsTrueColumns.lean',60,159),source('src/Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/TiedRec.lean',40,67),source(p+'ExistsConcrete.lean',16,110),source(p+'IsRecGOfIsLocalFamily.lean',13,74),source(p+'ExistsGIs.lean',146,165),source(p+'ConcreteSplitPrimeAutomorphicDataDivisionLattice.lean',21,80),source(p+'ColumnLocalDataTransportDivision.lean',14,43),source(d+'DsigEq.lean',24,66),source(p+'ExtraTiedCol.lean',10,19),source('src/Formalism/SharpRestriction/GlobalSchurBounds/Chosen.lean',18,90),source('src/Formalism/LocalToGlobal/ThresholdSelection.lean',9,16),source('src/Formalism/LocalToGlobal/Divisibility/DivisibilityRemainder/AdmissibleClasses/LinkGCl.lean',11,32)]
 ids=['GCF'+str(i) for i in list(range(1,7))+list(range(12,19))]
 bind('common_compatibility_v48',ids,findings,sources,'Exact finer determinant quotient, common columns/group stage, division transport and selected D3 admission. GCF7-GCF11 have a separate independent review; eventual common realization remains explicit.',{'selected_whole_obligation_closures':[],'complementary_independent_review':'common_compatibility_v48/review_GCF7_GCF11_main_proof_rigidity.json'})

def och():
 baseline=json.loads((ROOT/'dependency_audit_v0_47/obligation_map.json').read_text())
 contract=next(n['contract'] for n in baseline['nodes'] if n['id']=='TASK_ONE_CHAR_PROOF')
 findings=[
  dict(topic='All original finite Artin coefficient algebras',result='PASS',detail='Read OCH1-OCH14 in full and OCH30 against the exact original OneChar contract. Positive finite local cohomology and its reflection/lifting properties follow from the fundamental period sequence under the stated original hypotheses. Unramified diagonal deformations come from weight-zero finite cohomology, including finite-quotient invariants for disconnected actions. The positive-weight central obstruction vanishes. The triangular and arbitrary crystalline lifting arguments retain all finite Artin algebras and exact reduction maps.'),
  dict(topic='Actual ordinary ideal and crystalline component',result='PASS',detail='The canonical labelled inertia flag is stable under the decomposition group. The saturation identity uses Artin-Rees, annihilator killing and distinct projectors, with the original eigenvalue differences. Twisting by 1+t in B[t]/t^(2kh+1) handles Delta=0 and all nonreduced Artin targets. This proves the actual prime component and its twelve-variable chart, with weight multiplicities (1,2,3,4,2), and the original conjugation stability.'),
  dict(topic='Same global deformation datum and graded model',result='PASS',detail='The universal ring uses the original Dat, ULoc, marked g1 and eight normalization equations. The exact Euler/duality calculation gives the printed generator/equation counts. The integral weighted presentation is obtained from actual entry coordinates and a homogeneous kernel in the injective characteristic-zero chart; it does not divide by torus eigenvalue differences. OCH11 supplies the structural model, and OCH12-OCH14 supply its points, derivations and integral lifting fields.'),
  dict(topic='Convergence, continuity and integral lifting',result='PASS',detail='The finite algebra is (A/(Q))_0, not the ambient degree-zero ring. A valuative torus rescaling makes every required point strict-local and proves convergence of the full homogeneous series. Strict-local algebra maps are automatically bounded: if |f(u)|>1, ell*u^m contradicts maximal-ideal strictness for large m. Finite generators then give adic continuity. The dual-number and weight-minus-one derivation construction uses the original ambient ring before relations and finite Taylor division; no unproved continuity of a second component is assumed.'),
  dict(topic='Whole exact selected implication',result='PASS',detail='Compared source OneChar including arbitrary original algebraic closures, K, ell, c, N, e, psi, GD, fixed iota, sigma and the exact scalar t. OCH30 descends to an unramified coefficient ring with the same values, applies one shared marked automorphy datum there, and transports the length and trace result back. It retains Adm3 at N or Adm2 at N*abs(discr K), finite Vlen, an actual finite set of representations, RepIso-irredundancy, and the exact factor two. InpZ and AutomorphyUnramifiedCoefficients are the only two theorem-level premises; the latter remains a separate open producer.'),
  dict(topic='Complementary independent coverage and closure scope',result='PASS',detail='The global_estimates independent report covers OCH15-OCH30, including the full model upper bound, actual Selmer injection, irreducible finite trace sum and coefficient descent. This root report covers OCH1-OCH14 plus the exact original selected closure contract. Together they cover all thirty claims. Closing TASK_ONE_CHAR_PROOF does not assert AutomorphyUnramifiedCoefficients, any unrestricted automorphy theorem, or a completed human RH/GRH proof.')
 ]
 component='one_character_v48'
 candidates=list((ROOT/component).glob('review_*global_estimates.json'))
 assert candidates,'Complementary independent review not yet present'
 needed={'OCH'+str(i) for i in range(15,31)}
 covered=set()
 for p in candidates:
  r=json.loads(p.read_text())
  assert r['result']=='PASS' and not r.get('unresolved_findings')
  assert r['proof_sha256']==sha((ROOT/component/'main.tex').read_bytes())
  covered.update(c['id'] for c in r['claims_reviewed'])
 assert needed<=covered,('Incomplete complementary review',needed-covered)
 p='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
 sources=[source(p+'UnitaryThreeGroups/KatoUse.lean',54,64),source(p+'ModularityArgument/KatoQuadraticCharacters/OneChar.lean',102,178)]
 bind(component,['OCH'+str(i) for i in range(1,15)]+['OCH30'],findings,sources,'Independent mathematical review of OCH1-OCH14 and exact endpoint OCH30; full selected implication checked with complementary OCH15-OCH30 independent coverage.',{'selected_whole_contract_reviewed':{'id':'TASK_ONE_CHAR_PROOF','baseline_contract_sha256':sha(contract.encode()),'full_original_contract_closed_in_stated_scope':True,'conclusion':'The full original implication InpZ -> AutomorphyUnramifiedCoefficients -> OneChar, with the exact finite trace/length bound on all original data. AutomorphyUnramifiedCoefficients remains independently open.'},'complementary_independent_review_files':[str(p.relative_to(ROOT)) for p in candidates]})

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('component',choices=['pun','gcf','och']);args=parser.parse_args()
 {'pun':pun,'gcf':gcf,'och':och}[args.component]()

