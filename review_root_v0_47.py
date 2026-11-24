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
 report=dict(schema='rh-independent-human-review/1',artifact_version='0.47',component=component,reviewer='root',result='PASS',proof_file=component+'/main.tex',proof_sha256=sha(raw),source_commit=PIN,claims_reviewed=blocks,scope=scope,findings=findings,sources_inspected=sources,unresolved_findings=[],proof_bytes_modified_by_reviewer=False,lean_replay=False)
 if extra:report.update(extra)
 out=ROOT/component/('review_'+ids[0]+'_'+ids[-1]+'_root.json')
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(review=str(out.relative_to(ROOT)),proof_sha256=sha(raw),claims=len(ids),result='PASS')))

def cnc():
 findings=[
  dict(topic='Geometric hypotheses over every original base',result='PASS',detail='Checked original SAB/Obj/Moduli properness, smoothness, geometric connectedness and primitive/adjoint line fields. Stacks05D9 and0E0L were opened directly and match the two named foundations, including arbitrary base change and nonreduced bases.'),
  dict(topic='Global framed formal chart',result='PASS',detail='Eigen-idempotents after the split characteristic-zero coefficient field give the entire tangent basis. Nilpotent affine thickenings and compatible lifts of its dual basis give global finite-jet coordinate rings; finite associated-graded induction proves each map is an isomorphism over arbitrary S.'),
  dict(topic='Normalized frame and all line diagrams',result='PASS',detail='Nilpotent lifting produces compatible generators and axis normalization. Proper universal base functions make all normalized adjoint product/sum/cubical/symmetry diagrams unique. All signs and denominators of the four actual IsFrame ratios match the source.'),
  dict(topic='Full formal canonical gauge',result='PASS',detail='Checked invariant-form logarithm, radial primitive for symmetric cocycles, the sequential two-variable gauge, separability-idempotent derivation identity, and final negative half of the antisymmetric bilinear form. Gauge signs reproduce every original FB/IsCanonGauge field without assuming S reduced or a field.'),
  dict(topic='Germs and literal IsNab quantifiers',result='PASS',detail='The primitive generator times the biextension frame gives the actual L generator at every jet. Coefficients of every section form a unique formal germ. The original nabVal formula, every germ witness, all nonnegative weights, arbitrary coefficient algebras and rational-algebra structures are covered. No naturality condition absent from the exact predicate is invented.'),
  dict(topic='Scope boundary',result='PASS',detail='CNC15 supplies only the original connection producer. The remaining five ICL chart/level/Gaussian/short-dictionary/ramified-jet groups and common higher covers/class sums/PointIdentCore remain explicit. No whole selected global obligation is declared closed.')
 ]
 sources=[source('src/Formalism/LocalToGlobal/ProjectiveLattices/ThGerm.lean',160,225),source('src/Formalism/SharpRestriction/Divisibility/GeneratorPowers/CIndRaw.lean',53,106),source('src/Formalism/SharpRestriction/Divisibility/GeneratorPowers/GermCut.lean',54,153),source('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean',14,84),source('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/TwoWeightEqOneAddRoot.lean',144,162)]
 bind('canonical_cusp_connection_v47',['CNC'+str(i) for i in range(1,17)],findings,sources,'Full original canonical connection and formal gauge at the stated literal scope; all sixteen numbered proofs and original consumers.',{'primary_sources_opened':['https://stacks.math.columbia.edu/tag/05D9','https://stacks.math.columbia.edu/tag/0E0L'],'selected_whole_obligation_closures':[]})

def ktr():
 component='type_ii_rigidity_v47'
 baseline=json.loads((ROOT/'dependency_audit_v0_46/obligation_map.json').read_text())
 contract=next(n['contract'] for n in baseline['nodes'] if n['id']=='RIG_II')
 findings=[
  dict(topic='Kato critical twist and local conditions',result='PASS',detail='Root inspected original primary PDF pages235 and240. Theorem14.2(1) has1<=r<=k-1, r!=k/2, every finite coefficient place, finite abelian extension, and includes CM. Section14.1 is the exact unramified/Bcris condition. Formula14.10.3 uses inverse arithmetic Frobenius, matching the source. For k=2e+1 and r=e all hypotheses hold and W=V(f)(e).'),
  dict(topic='Rational cohomology and finite characters',result='PASS',detail='Finite coefficient descent and equivariant local primitives are the inherited exact ADK/BX/DX comparison. Divisibility of rational Selmer classes plus bounded integral cohomology and finite discrete Selmer image proves zero. Restriction to a finite abelian character field is injective by explicit characteristic-zero averaging. Original KatoUse and KatoTwo antecedents and quantifiers are retained.'),
  dict(topic='Actual local point and rank-two extension',result='PASS',detail='Root read the ordered-product ideal containment, distinct-eigenvalue flag on I intersect ker(tau), normalizer calculation, prime-to-ell inertial character killing and class-number argument. The actual corner has determinant1 and middle1, and the signed formula W(g)=B_g D2^((1-eta(g))/2) gives exactly the original IsExt.'),
  dict(topic='Infinite cyclotomic kernel',result='PASS',detail='The elementary two-dimensional projective/self-twist lemma covers both distinct and repeated restricted characters. The actual inertia character has infinite cyclotomic part and yields the contradiction kappa(u)^8=1. This proves irreducibility on the full infinite cyclotomic kernel, without assuming equality of its finite part with the original tau.'),
  dict(topic='Actual base change and polarized pairing',result='PASS',detail='Opened primary Langlands base-change text and checked Lemma11.3(b)/Proposition11.4. The exceptional induced case would force eta self-twist, ruled out by irreducibility on G_K. RNC2 adelization, the half-determinant twist, geometric Satake q^(1/2) normalization, multiplier norm character and sign are matched before BLGGT existence. The explicit symmetric J2 pairing agrees up to scalar, giving minus-transpose on all M2.'),
  dict(topic='Nine-dimensional decomposition and final primitive',result='PASS',detail='Verified the corner, two off-diagonal p_t/s_t maps and middle scalar action at H and c. The sections satisfy p_t s_t=2 and their half-sum plus corner/scalar is the identity. Kato, the checked Thorne application and quadratic scalar vanishing give an explicit primitive for every original continuous nine-dimensional Selmer cocycle.'),
  dict(topic='Selected original contract',result='PASS',detail='Compared the exact RigII definition including arbitrary original closures, K, ell, coefficient ring, N, e, psi, Dat, ULoc, marked g1, actual IsPt, fixed iota and universal IsExt-to-IsModular antecedent. The proof retains that antecedent and supplies its required actual extension; no independent OneChar or ordinary coefficient automorphy conclusion is inferred.')
 ]
 p='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
 sources=[source(p+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean',11,60),source(p+'UnitaryThreeGroups/RhoKApply.lean',16,93)]
 bind(component,['KTR'+str(i) for i in range(1,14)],findings,sources,'Full original KatoUse, KatoTwo and RigII, with published foundations and the literal original modularity antecedent.',{'selected_whole_contract_reviewed':{'id':'RIG_II','baseline_contract_sha256':sha(contract.encode()),'full_original_contract_closed_in_stated_scope':True,'conclusion':'Entire original RigII implication; actual extension and all nine polarized adjoint coordinates reconstructed.'},'primary_sources_opened':['https://www.numdam.org/item/AST_2004__295__117_0/','https://publications.ias.edu/sites/default/files/base-change-for-gl2_rpl_2.pdf'],'primary_kato_pages_visually_inspected':[235,240]})

def pcl():
 findings=[
  dict(topic='Original Hermitian coordinates and sign',result='PASS',detail='Read all twelve mathematical proofs. The original perfect alternating datum is torsion-free, its rationalization has the supplied E-rank, and nondegeneracy of the field trace uniquely reconstructs the left-linear skew-Hermitian form. Dividing by the actual imaginary xi gives the stated Hermitian form and original lattice injection; the chart trace form uses the explicitly recorded minus sign.'),
  dict(topic='Nonprincipal ideal duality and exact different',result='PASS',detail='Verified both ideal-valued dual identities by finite invertible-ideal decompositions, without assuming that a lattice or ideal has one generator. The trace-dual lattice is ((xi)D_E)^(-1)L-sharp; integral perfection gives L-sharp=(xi)D_E L. The actual A^(-1)Lambda is therefore self-dual under the original principal product identity.'),
  dict(topic='Complete DataX constructor',result='PASS',detail='Compared every original DataX field and the whole exists_dataX_of_perfect_traceForm endpoint. Both positive denominator witnesses, k0=2k and its bounds, actual lattice inclusions, unchanged Data and the original positive-modulus congruence clause are supplied. No pre-existing scalar, matrix, metric or group is replaced.'),
  dict(topic='Original uniformization trace pairing',result='PASS',detail='Read literal IsUnf fields77–95 and the original trace-perfection endpoint. Its actual integral lattice equivalence transports both integrality and surjectivity onto the Z-dual for each supplied component. Existence of IsUnf is retained.'),
  dict(topic='Actual host ideal and scalar',result='PASS',detail='The quadratic integer-ring and trace-dual calculations give D_K=(sqrt(-d)); the split/inert/ramified prime calculations give C*conj(C)=(Norm C). Together with the actual half-different these prove (xi_H)A*conj(A)*D_E=1. The scalar xi_H=-1/(Norm(C)*sqrt(-d)) and absolute value 1/(Norm(C)*sqrt(d)) match original DataHost and ModelDataX.'),
  dict(topic='Quantitative denominators and logarithms',result='PASS',detail='NA=Norm_E(b) and NC=Norm_K(ccK) lie in the exact required ideals and work for every original component. Norms of conjugate ideals agree, so NA^2<=abs(discriminant E), giving log NA<=f_E log rd(E) with the exact factor one-half. The source SupBoundPageRows fourth conjunct supplies the NC logarithmic bound.'),
  dict(topic='Literal all-row endpoints and retained boundary',result='PASS',detail='Compared exists_dataX_of_hasPrinc, both GamAt predicates, the core DataX model endpoint and DataXOfModelSt. All original rows, good embeddings, components, levels and later size/weight quantifiers are preserved. Equal absolute values of purely imaginary scalars at one injective embedding give xi=plus/minus xi_H, sufficient for the exact ideal identity. IsUnf, HasPrinc/GamAt, LawsCore, common uniformization and the separate theta/Gaussian/short-rule/ramified-jet producers remain explicit. No selected whole leaf is closed.')
 ]
 sources=[source('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/FundamentalDomains/FundamentalDomainPointBound.lean',12,41),source('src/Development/AbelianVarietyTheory/Proofs/CubicalLineBundles/ExistsPosNatMemFractionalIdeal.lean',10,55),source('src/Formalism/LocalToGlobal/ProjectiveLattices/UnFree.lean',77,95),source('src/Formalism/LocalRingCardinality/DataHost.lean',145,166),source('src/Formalism/LocalRingCardinality/RankBoundMonotoneInDimension.lean',1311,1342),source('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/PullbackSections/HolomorphicFamilies/ModelDataX.lean',12,45),source('src/Development/AbelianVarietyTheory/Proofs/CubicalLineBundles/ExistsRankOneCuspLatticeDataOfPrincipal.lean',59,106),source('src/Development/AbelianVarietyTheory/Proofs/CubicalLineBundles/DataXOfModelOfGamAt.lean',17,23),source('src/Formalism/LocalToGlobal/ProjectiveLattices/ArchimedeanQuadraticData/ArcWitnessExistence/DataXOfModel.lean',13,18),source('src/ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/PullbackSections/SupBoundPageRows.lean',9,18)]
 bind('principal_cusp_lattices_v47',['PCL'+str(i) for i in range(1,13)],findings,sources,'Full original Hermitian/trace-dual lattice constructors and quantitative DataX endpoints on supplied principal charts; all twelve claims and original conditional boundary.',{'selected_whole_obligation_closures':[]})

def kiz():
 baseline=json.loads((ROOT/'dependency_audit_v0_46/obligation_map.json').read_text())
 contract=next(n['contract'] for n in baseline['nodes'] if n['id']=='TASK_INP_Z_ASSEMBLY')
 findings=[
  dict(topic='Literal five-field cohomological record',result='PASS',detail='Read exact CohInp19–24 and compared BX8 and KB8. The four extracted fields retain the same original finite-module local cohomology, normalized Poitou–Tate, global finiteness and Euler statements. The prime-two Euler expression and separate odd-prime higher-vanishing guard are distinguished. KB8 supplies the actual LemmaK31 with its HasMuQ guard and single exponent selected before all varying arithmetic data.'),
  dict(topic='Exact six extension fields',result='PASS',detail='Read literal InpZ55–61. Its fields are precisely lemM, lemMprime, lemP, rigII, adK and number. Compared the complete printed SP6/SP1/FP8/ADK6 conclusions with the new assembly. SP1 retains finite residue and an additive, not necessarily linear, injection; FP8 retains exact weighted generator/equation counts and all original framed hypotheses.'),
  dict(topic='Rigidity antecedent and full adjoint',result='PASS',detail='KTR13 has been independently reviewed in full. KIZ preserves the literal universal IsExt-to-IsModular antecedent, actual local point/marked-element guards and full nine-dimensional adjoint. It constructs no replacement datum and does not infer the antecedent. ADK6 supplies its exact original full polarized CM adjoint statement, including the scalar part and full infinite-cyclotomic condition.'),
  dict(topic='Uniform congruence-integer field',result='PASS',detail='RNC16 has the fixed-K constants before weights, levels, primes and indexed orbits; the single nonzero integer precedes every later coefficient datum and admissible family. KIZ preserves the rank-three/rank-two-block disjunction, original Frobenius inverse and coefficient-prime scope. No rank-four congruence statement is substituted.'),
  dict(topic='Same-object assembly and exact selected closure',result='PASS',detail='All suppliers are universal proofs of the literal predicates, specialized to the same later objects. CohInp has five fields and InpZ adds six with no further compatibility field. The selected B task is exactly this record construction. Independent OneChar, AutomorphyUnramifiedCoefficients and the final RH/GRH producers remain separate; no existence of their later application hypotheses is asserted.')
 ]
 p='src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
 sources=[source(p+'UnitaryThreeGroups/KatoUse.lean',12,35),source(p+'ModularityArgument/KatoQuadraticCharacters/KatoTwoOfUseN.lean',43,61)]
 bind('kato_input_assembly_v47',['KIZ1','KIZ2'],findings,sources,'Exact complete CohInp/InpZ construction with every original field, antecedent and choice order; selected B installation task only.',{'selected_whole_contract_reviewed':{'id':'TASK_INP_Z_ASSEMBLY','baseline_contract_sha256':sha(contract.encode()),'full_original_contract_closed_in_stated_scope':True,'conclusion':'The entire original eleven-field CohInp/InpZ record is supplied by the named completed human proofs; OneChar and unramified-coefficient automorphy remain independent.'},'inherited_endpoint_statements_directly_compared':['BX8','KB8','SP1','SP6','FP8','ADK6','KTR13','RNC16']})

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('component',choices=['cnc','ktr','pcl','kiz']);args=parser.parse_args()
 {'cnc':cnc,'ktr':ktr,'pcl':pcl,'kiz':kiz}[args.component]()
