#!/usr/bin/env python3
"""Bind the finite base-change bridge to its literal pinned contracts."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
source=ap.parse_args().source.resolve()
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==PIN
sha=lambda b:hashlib.sha256(b).hexdigest()
AB='src/Development/AbelianVarietyTheory/'
IP=AB+'Proofs/InertiaEigenvalues/'
IW=AB+'Proofs/IwasawaDecomposition/'
PT=AB+'PublishedTheorems/'
RG='src/Development/WeilBound/RepresentationTheoryGL/'
RS=RG+'ResidualSpectrum/'
SL=RS+'SliceTensors/'
AA='src/Development/AutomorphicArithmetic/'
BC=AA+'Foundations/BaseChangeIdentities/'
DC=AA+'AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/'
TENSOR='src/Development/WeilBound/CoreStatements/AutomorphicKernels/ResidualSpectrumHilbertSum/ResidualSpectrumTensors/'
SPEH=AB+'Definitions/NonGaloisDescent/IsUnitarisableTrivChar.lean'
SAT=IP+'SatakeParameterSphericalProductSpehQuotients.lean'

# Source ranges are contract and normalization locators, never proof substitutes.
specs={
 'literal_hypotheses':[
  (DC+'LitAut.lean',12,63,'original H.litN.loc and H.litN.aut fields'),
  (RG+'ArchimedeanBaseChange/ArchimedeanBaseChangeProof/BaseChangeIsobaricNOf.lean',18,46,'CsdAsc; all IsBaseChangeN fields; full BaseChangeIsobaricN'),
  (BC+'Narrow.lean',12,74,'all IsBaseChangeU fields; DefiniteN; AscComp; original bridge'),
  (DC+'BciNarrowSwap.lean',12,13,'actual bcSpeh_alt consumer'),
  (DC+'GuWrap.lean',19,21,'actual spehOf_alt and GalUnitaryT consumer')],
 'discrete_unitarity':[
  (PT+'GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',20,57,'literal splitCentre/latticeGL/IsSqInt/IsDiscrete/IsLocCompGL/HasInfCharGL/locProd'),
  (IP+'DiscreteAutomorphicRepGLLocalComponentIsUnitaris.lean',17,79,'common Haar/fundamental domain and positive pullback form'),
  (IP+'DiscreteAutomorphicRepGLLocalComponentIsUnitaris.lean',107,None,'modular character and original all-local component endpoint'),
  (PT+'AutomorphicForms₂/CuspDiscreteDecompositionGL.lean',103,135,'retained CuspidalSpectrumGL boundedness clause'),
  (PT+'Divisors₂/DiscreteSpectrumGLTwoOfCuspidalSpectrum.lean',68,99,'bounded normalized functions are square integrable'),
  (TENSOR+'LocalComponentGL.lean',20,None,'normalized cusp discrete and actual local forms')],
 'finite_product':[
  (PT+'TwistedTraceFormula/BernsteinUnitaryProductIrreducible.lean',10,18,'exact retained two-factor theorem'),
  (IP+'ParabolicInductionInStagesProductOfProducts.lean',1,None,'original induction-in-stages product of products'),
  (IP+'ExistsEquivOfIsSubquotient.lean',18,109,'subquotient equivalence and spherical/Satake/IsCompAlong transport')],
 'local_existence':[
  (PT+'AutomorphicForms₂/ExistsSpanFormsNeBot.lean',15,28,'literal original AutomorphicFormsFiniteGL'),
  (IW+'ExistsIsLocCompAndIsLocLoc.lean',31,127,'compact null part and minimum fixed-dimension irreducible construction'),
  (IW+'ExistsIsLocCompAndIsLocLoc.lean',151,None,'global stability, finite type, actual local existence'),
  (IP+'DiscreteAutomorphicRepGLExistsLocalComponent.lean',1,None,'same actual local existence for discrete GL subspaces'),
  (IW+'HasInfCharInfCharOfCommute.lean',13,None,'monic Capelli polynomial; finite-center eigenvector; actual infinity characters'),
  (TENSOR+'MultilinearMemOfSpan.lean',45,None,'tensor span from actual local maps')],
 'genericity':[
  (IP+'IsGenericOfIsLocComp.lean',29,None,'column Fourier steps and exact local Whittaker functional'),
  (IP+'UnipotentColumnWhittakerTransformNeZero.lean',1,None,'Fourier uniqueness at each original column stage')],
 'duality':[
  (PT+'TwistedTraceFormula/HasFiniteLengthOfIsIrreducible.lean',16,53,'retained admissibility and exact normalized-induction contragredient pairing'),
  (SL+'PLocDual.lean',24,57,'compact-averaged extension proves smooth-dual surjectivity'),
  (SL+'Clause3Asc.lean',13,34,'original ascending local injection, dual quotient, and Clause3Asc contracts')],
 'ascending_local':[
  (SL+'IsSliceMap.lean',50,58,'literal Emb and AscEmb including all-operator map and original twists'),
  (PT+'GaloisCohomology₂/IsNormalisedOfIsDiscrete.lean',38,78,'actual indForms, spehExp, normalization and HasSpehComp'),
  (RS+'IwasawaCompletion/RestrictAtPointHolds.lean',17,None,'nonzero slice at actual Iwasawa point; local parabolic covariance'),
  (SL+'ExistsProj2.lean',17,None,'nonzero equivariant isotypic tensor projection'),
  (SL+'LocSubOf.lean',24,None,'local extraction, exact delta-half subtraction and original LocSub')],
 'generic_unitary':[
  (RG+'UnitaryDualProof/GenericIrreducibility/GenUnitCCOf.lean',10,16,'exact finite generic-unitary decomposition shape used in source'),
  (PT+'GaloisCohomology₂/SquareIntegrableSegment.lean',10,13,'original retained unitary square-integrable segment theorem'),
  (PT+'GaloisCohomology₂/StandardCosocleGL.lean',10,14,'original retained ordered LFactors unique-cosocle theorem')],
 'cosocle':[
  (AB+'Definitions/NonGaloisDescent/NonemptyEquivOfRangeEq.lean',90,98,'literal IsSocle and IsCosocle'),
  (AB+'Definitions/NonGaloisDescent/NonemptyEquivMultiProdOne.lean',539,562,'ordered segment factors and exact IsSpeh'),
  (IP+'UnitarisableSegmentTwistPrecedesAddOneLe.lean',13,None,'central-character computation and exact x+1<=y bound'),
  (RS+'IwasawaCompletion/SpehCosocleUc.lean',20,None,'original finite row-major segment order and cosocle consumer'),
  (RS+'IwasawaCompletion/CharZeroCompletion.lean',20,48,'literal local quotient-to-IsSpeh consumer')],
 'capelli':[
  (IP+'CapelliDetBlockLeviCongrModUpperBlockIdeal.lean',15,None,'upper-block right ideal, two-block expansion and full shift'),
  (IP+'DiscreteSpectrumOfResidual.lean',30,70,'original block Capelli and adelic Iwasawa identities'),
  (IP+'DiscreteSpectrumOfResidual.lean',96,190,'all-operator Capelli intertwining and induced-space character'),
  (SL+'PInfAsc.lean',15,None,'ascending infinity character with exact reversal'),
  (RS+'DiscreteSpectrumUnitarity/UsedAsc.lean',31,51,'all three literal HasSpehComp fields'),
  (BC+'NarrowAsc.lean',1,None,'actual AscComp endpoint supplier')],
 'fixed_satake':[
  (AB+'Definitions/Foundations/IsSatVecUOfIsSphericalU.lean',86,158,'exact satEig; IsSatVecGL; HasSatGL and uniqueness'),
  (SAT,98,241,'tensor averaging, evaluation at one, and actual finite Hecke action'),
  (SAT,257,314,'spherical scalar line and Satake existence'),
  (SAT,324,512,'original normalized block induction Satake product')],
 'speh_satake':[
  (SAT,520,None,'unramified determinant twists; exact Speh root strings; full outer product endpoint')],
 'weights_assembly':[
  (PT+'GaloisCohomology₂/BaseChangeDefiniteUnitary.lean',139,143,'actual HasWeightAt and infOfWeight convention'),
  (IW+'ExistsUniqueWeightDefiniteUnitaryAt.lean',35,103,'actual compact infinity orbit and dominant-weight inclusion'),
  (BC+'NarrowSpeh.lean',14,110,'all-rank bridge; all Parts fields; original witnesses retained'),
  (SPEH,16,44,'literal seven Parts fields and full BcSpeh')],
 'unramified_consequence':[
  (AB+'Proofs/DivisorProofs/IsSphericalOfIsCompAlongSplit.lean',47,None,'original all-IsUnramU spherical actual cusp component consequence'),
  (BC+'Narrow.lean',21,25,'stronger DefiniteN spherical full-product clause retained by our construction')]
}

inventory={}; records={}; excerpts=[]
for group,entries in specs.items():
    records[group]=[]
    for i,(path,start,end,decl) in enumerate(entries,1):
        b=(source/path).read_bytes()
        assert b==subprocess.check_output(['git','-C',str(source),'show',f'{PIN}:{path}']),path
        lines=b.splitlines(keepends=True)
        end=len(lines) if end is None else end
        assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
        block=b''.join(lines[start-1:end])
        rec=dict(id=f'BCS_{group}_{i:02}',path=path,declaration=decl,line_start=start,line_end=end,
                 file_sha256=sha(b),range_sha256=sha(block),range_bytes=len(block),source_commit=PIN,
                 verified_equal_to_pinned_git_blob=True,
                 url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        records[group].append(rec)
        inventory[path]=dict(path=path,sha256=sha(b),bytes=len(b),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nSHA256 {rec["range_sha256"]}\n{block.decode()}\n')

titles={
1:'Actual discrete and normalized-cuspidal local unitarisability',
2:'Finite original unitary local products are irreducible',
3:'Full original DefiniteN from named BaseChangeIsobaricN',
4:'Actual local component existence, algebraic isotypy and infinity characters',
5:'Genericity of every actual cuspidal local component',
6:'Hermitian smooth duality converts the ascending map into the exact descending quotient',
7:'Actual ascending local induction with original modulus normalization',
8:'Checked published generic-unitary factorization with strict one-half bounds',
9:'Full unique cosocle of every descending Speh induction',
10:'Original IsSpeh for all actual discrete local components',
11:'Exact original block Capelli shift',
12:'Infinity character of the ascending embedding',
13:'Complete original AscComp consumer',
14:'Exact compact fixed vectors of local products and quotients',
15:'Original normalized Satake product calculation',
16:'Exact original Speh Satake strings including the outer product',
17:'Positive rank data and original equal-length distinctness',
18:'Full original BcSpeh with original witnesses',
19:'All-IsUnramU spherical cusp factors for the same witnesses'
}
deps={1:[],2:[],3:[1,2],4:[],5:[],6:[],7:[4],8:[1,5],9:[2,8],
10:[1,5,6,7,8,9],11:[],12:[4,7,11],13:[1,4,10,12],14:[],15:[14],16:[14,15],
17:[3,4,12],18:[1,3,10,12,13,16,17],19:[3,4,14,18]}
groups={1:['discrete_unitarity'],2:['finite_product'],3:['literal_hypotheses','finite_product'],
4:['local_existence'],5:['genericity'],6:['duality'],7:['ascending_local','local_existence'],
8:['generic_unitary'],9:['generic_unitary','cosocle'],10:['ascending_local','cosocle'],
11:['capelli'],12:['ascending_local','capelli'],13:['literal_hypotheses','capelli'],
14:['fixed_satake'],15:['fixed_satake'],16:['speh_satake'],
17:['weights_assembly'],18:['literal_hypotheses','weights_assembly'],19:['unramified_consequence','fixed_satake']}
external_ids={1:['BCS_CUSP_BOUND','BCS_HAAR_GL_VOLUME'],2:['BCS_BERN','BCS_LOCAL_IWASAWA'],
3:['BCS_BC_N'],4:['BCS_AUT_FIN','BCS_BZ','BCS_ALGEBRAIC_DENSITY'],5:['BCS_COMPACT_FOURIER'],
6:['BCS_BZ'],7:['BCS_LOCAL_IWASAWA'],8:['BCS_MW_GENERIC_UNITARY'],
9:['BCS_SQUARE_SEGMENT','BCS_STANDARD_COSOCLE'],10:[],11:['BCS_LOCAL_IWASAWA'],12:[],13:[],
14:['BCS_LOCAL_IWASAWA'],15:['BCS_BZ'],16:[],17:['BCS_COMPACT_HIGHEST_WEIGHT'],18:['BCS_BC_N'],19:[]}
scopes={
1:'Every original discrete GL space and every normalized cusp over a totally complex number field; every actual local component.',
2:'Every finite ordered list of positive-rank smooth irreducible unitarisable local factors; repeated factors allowed; no rank bound.',
3:'Every original CM field unramified at finite places, n>=1 and actual IsAutRepU; same c,N,V,sigma,m and exact local maps.',
4:'Actual GL cuspidal/discrete subspaces; existence uses literal automorphic finiteness; local isotypy is algebraic, not a completed tensor-product assumption.',
5:'Every positive-rank actual cusp and every finite completion, including residue characteristic two.',
6:'Every nonarchimedean local field and two smooth irreducible unitarisable factors of ranks a and ad, d>=1; retained bz duality and admissibility.',
7:'Any original AscEmb(V,P,d) with N>=1; all original actual local components; coefficient exponent (a-1)s minus delta-half as leaves -s.',
8:'Every nonarchimedean characteristic-zero local field, every positive rank, smooth irreducible generic unitarisable rho; strict abs(t_j)<1/2.',
9:'All positive lengths d; exact row-major LFactors order and literal unique maximal-kernel cosocle.',
10:'All local components at every finite place, not only one selected quotient or almost every place.',
11:'All finite ordered block ranks; the original unnormalized indForms and source Capelli determinant convention.',
12:'Every complex embedding; exact spehInf multiset with original shifts and multiplicities; no unspecified common twist.',
13:'Full AscComp: every totally complex number field, N>=1, normalized cusp length-one realization and every actual AscEmb consumer.',
14:'Smooth algebraic representations, exact compact fixed functor and actual original integral Levi; no normality assumption on compact opens.',
15:'Every smooth irreducible spherical factor, original T_j normalization and all uniformizers; exact q^(j(n-j)/2).',
16:'All positive Speh lengths, all original B, S, T multisets in complex units; q_w is absolute residue norm, distinct from IsUnramInv parameter q.',
17:'Original actual unitary automorphic representation, every original base-change witness, positive ranks and all equal-length cuspidal-class equalities.',
18:'Full literal BcSpeh under original bc and displayed foundations, for all n>=1 and every original CM/unramified guard.',
19:'Same simultaneously chosen BCS18 witnesses; every IsUnramU place, both split and inert; also every alternative actual component of each cusp.'}

tex=(HERE/'main.tex').read_bytes(); t=tex.decode(); claims=[]
for n,title in titles.items():
    cid=f'BCS{n}'
    m=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',t,re.S)
    assert m,cid
    b=m.group().encode()
    claims.append(dict(id=cid,title=title,introduced_in='0.44',classification='A' if n==8 else 'B',
        status='complete human proof or exact published application at printed scope',
        depends_on=[f'BCS{x}' for x in deps[n]],external_input_ids=external_ids[n],
        published_input_ids=['BCS_MW_GENERIC_UNITARY'] if n==8 else [],
        hypotheses_retained=[scopes[n]],source_groups=groups[n],sources=[s for g in groups[n] for s in records[g]],
        proof_location=dict(file=f'{HERE.name}/main.tex',label='claim:'+cid,line_start=t[:m.start()].count('\n')+1,
                            line_end=t[:m.end()].count('\n'),sha256=sha(b),bytes=len(b)),
        scope_note='The source range identifies original contracts and normalizations. The displayed human argument proves the bounded consumer; no Lean replay.'))

foundations=[
dict(id='BCS_BC_N',kind='retained_original_named_hypothesis',name='H.litN.aut.bc: BaseChangeIsobaricN',
     statement='Entire original all-rank definite-inner-form nongeneric package, including actual CsdAsc, all local/spherical/weight clauses.',
     source_groups=['literal_hypotheses'],not_reconstructed=True),
dict(id='BCS_BERN',kind='retained_original_named_hypothesis',name='H.litN.loc.bern: BernsteinUnitaryProductIrreducible',
     statement='Normalized two-factor induction of smooth irreducible unitarisable GL factors is irreducible.',source_groups=['finite_product'],not_reconstructed=True),
dict(id='BCS_BZ',kind='retained_original_named_hypothesis',name='H.litN.loc.bz: BernsteinZelevinskyFiniteness',
     statement='Only irreducible admissibility and the exact compact-integral normalized-induction contragredient equivalence are used here.',source_groups=['duality'],not_reconstructed=True),
dict(id='BCS_SQUARE_SEGMENT',kind='retained_original_named_hypothesis',name='H.litN.loc.sq: SquareIntegrableSegment',
     statement='A unitary square-integrable GL representation is the L-segment quotient for a segment.',source_groups=['generic_unitary'],not_reconstructed=True),
dict(id='BCS_STANDARD_COSOCLE',kind='retained_original_named_hypothesis',name='H.litN.loc.cos: StandardCosocleGL',
     statement='An actual ordered list LFactors has an irreducible cosocle with unique maximal kernel.',source_groups=['generic_unitary'],not_reconstructed=True),
dict(id='BCS_AUT_FIN',kind='retained_original_named_hypothesis',name='H.litN.aut.fin: AutomorphicFormsFiniteGL',
     statement='Finite-dimensionality at the actual open finite level, compact infinity coefficient type and scalar central character.',source_groups=['local_existence'],not_reconstructed=True),
dict(id='BCS_CUSP_BOUND',kind='retained_original_named_hypothesis',name='H.litN.aut.cusp: CuspFormsBoundedGL clause',
     statement='Every cusp function with norm invariant under the split real center is bounded.',source_groups=['discrete_unitarity'],not_reconstructed=True),
dict(id='BCS_HAAR_GL_VOLUME',kind='retained_analytic_foundation',name='Haar quotient measure and finite covolume of GL modulo its split center',
     statement='The original adelic GL group is unimodular and its latticeGL quotient has finite Haar volume; Haar uniqueness/fundamental-domain integral transport.',source_groups=['discrete_unitarity'],not_reconstructed=True),
dict(id='BCS_LOCAL_IWASAWA',kind='retained_elementary_local_and_adelic_foundation',name='Iwasawa decomposition for original GL block coordinates',
     statement='G(F)=P(F)GL(O_F), and the source adelic unipotent/Levi/compact-infinity/finite factorization; the same maps and modulus are used.',source_groups=['ascending_local','capelli','fixed_satake'],not_reconstructed=True),
dict(id='BCS_COMPACT_FOURIER',kind='retained_harmonic_analysis_foundation',name='Compact adelic additive Fourier uniqueness',
     statement='Standard character of A_E/E, nontrivial at each completion; Fourier coefficients detect continuous functions on finite products, and compact Haar/Fubini.',source_groups=['genericity'],not_reconstructed=True),
dict(id='BCS_COMPACT_HIGHEST_WEIGHT',kind='retained_classical_representation_foundation',name='Highest-weight theory for compact U(n)',
     statement='Every finite-dimensional continuous irreducible complex U(n) representation is the original dominant-integral highest-weight representation.',source_groups=['weights_assembly'],not_reconstructed=True),
dict(id='BCS_ALGEBRAIC_DENSITY',kind='retained_classical_module_foundation',name='Density theorem for simple modules with scalar endomorphisms',
     statement='A finite algebraic tensor of simple modules over complex algebras, each having scalar endomorphisms, is simple; coordinate separation of finite tensors.',source_groups=['local_existence'],not_reconstructed=True)
]
published=[dict(id='BCS_MW_GENERIC_UNITARY',kind='matched_published_input',classification='A',
    author='C. Mœglin and J.-L. Waldspurger',title='Le spectre résiduel de GL(n)',
    publication='Annales scientifiques de l’École Normale Supérieure 22 (1989), 605–674',doi='10.24033/asens.1595',
    url='https://www.numdam.org/item/10.24033/asens.1595.pdf',
    locators=['Section I.10, opening paragraph, printed p.639 / PDF index35','Section I.11, opening paragraph, printed p.640 / PDF index36'],
    retrieval_date='2026-11-23',retrieval_status='Primary NUMDAM PDF full text and both exact page views retrieved through web tool.',
    statement_used='Every generic irreducible unitary nonarchimedean GL representation is a normalized product of unitary discrete-series representations twisted by real exponents strictly between -1/2 and 1/2.',
    exact_dictionary_location='main.tex BCS8, equation BCS.15',
    dictionary=['MW pi=rho; delta_j=our unitary square-integrable delta_j; v_j=t_j.',
                'MW normalized upper-parabolic induction and absolute value agree with BCS.2.',
                'The Whittaker condition in I.11 sets the longer Speh half-length parameters from I.10 to zero.',
                'Every actual E_w has characteristic zero. BCS1 supplies local unitarisability; BCS5 supplies Whittaker genericity.',
                'BCS9 uses original SquareIntegrableSegment and StandardCosocleGL to prove its own finite ordering and cosocle consumer.'],
    not_claimed=['a new proof of the local unitary classification','the full global residual-spectrum theorem','a replacement or enlargement of H.litN.aut.bc','temperedness of cuspidal local components'])]

completed=['DefiniteN','AscComp','BcSpeh','all-IsUnramU spherical actual cusp factors for the same chosen witnesses']
frontier=[dict(id='BCS_ORIGINAL_BC_FOUNDATION',status='retained_original_named_input',
               target='Full original H.litN.aut.bc, including definite inner form, every rank and nongeneric CsdAsc scope.',sources=records['literal_hypotheses']),
          dict(id='BCS_DOWNSTREAM_GALOIS',status='separate_parallel_component',
               target='Literal GalUnitaryT and original RowT consumer; provided separately by GUA, not claimed by BCS.',sources=records['literal_hypotheses'][-1:])]
contract=dict(schema='rh-base-change-speh-contracts/1',artifact_version='0.44',component=HERE.name,source_commit=PIN,
    proof_file_sha256=sha(tex),completed_planning_target='PLAN_AUT_2',completed_original_substatements=completed,
    endpoint_claim='BCS18',strengthened_endpoint_claim='BCS19',
    rank_scope='Every original n>=1, all c>0, all positive a_i,d_i, exact sum_i a_i d_i=n.',
    original_field_coverage={
      'IsBaseChangeU':['pos','discrete','csd','loc','inf','unram','inert','split','weight'],
      'AscComp':['normalized cusp length-one discrete realization','all actual ascending embeddings give HasSpehComp'],
      'HasSpehComp':['exLoc','loc for all actual components','inf'],
      'Parts':['pos','csd','loc','inf','weight','distinct','inert'],
      'BcSpeh':['all Parts fields','unitarisable cusp local factor','unitarisable discrete local factor','literal unique-cosocle IsSpeh','full split IsCompAlong for original locProd']},
    normalizations=['upper standard block normalized induction','original finite-place subgroup and cLoc composition',
       'ascending unnormalized exponent (a-1)s; subtract a*s to get -s',
       'Hermitian dual changes -s to +s without reordering',
       'Capelli block shift -modExp/2 and exact spehInf by index reversal',
       'satEig=q_w^(j(n-j)/2)e_j; nu^t multiplies Satake roots by q_w^(-t)',
       'final root string q_w^((d-1)/2-k), absolute q_w rather than IsUnramInv q'],
    published_input_ids=['BCS_MW_GENERIC_UNITARY'],retained_foundation_ids=[x['id'] for x in foundations],
    original_base_change_retained=True,new_trace_formula_or_residual_classification_claimed=False,
    no_lean_replay=True,remaining_frontier=frontier,whole_obligation_closures=[])

reviews=[]
for p in sorted(HERE.glob('review_*.json')):
    reviews.append(dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())))
rootreview=ROOT/'reviews_v0_44/base_change_v44_root_review.json'
if rootreview.is_file(): reviews.append(dict(file=str(rootreview.relative_to(ROOT)),sha256=sha(rootreview.read_bytes())))
provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.44',date='2026-11-23',component=HERE.name,
    source_commit=PIN,main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),claims=claims,
    source_groups=records,source_inventory=list(inventory.values()),source_files=list(inventory),
    published_applications=published,retained_foundations=foundations,inherited_human_inputs=[],independent_reviews=reviews,
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,
                    claim_blocks=len(claims),whole_original_leaf_closures=0),
    scope_note='Complete literal finite bridge under original named bc and explicit foundations. BCS8 is a checked published application. No RH/GRH completion or Lean replay.')
closure=dict(schema='rh-human-component-closure/1',artifact_version='0.44',component=HERE.name,proof_file_sha256=sha(tex),
    new_claims=list(c['id'] for c in claims),new_claim_count=len(claims),completed_original_substatements=completed,
    completed_planning_targets=['PLAN_AUT_2'],whole_obligation_closures=[],
    original_named_base_change_input_preserved=True,all_positive_speh_lengths_preserved=True,
    all_original_rank_and_local_and_infinity_scopes_preserved=True,
    selected_consumer_only=False,no_lean_replay=True,
    not_claimed=['base-change trace formula','production of AscEmb for arbitrary discrete GL spaces','new local unitary classification','global Galois attachment','complete RH/GRH'])
outputs={'provenance.json':provenance,'contracts.json':contract,'closure.json':closure,
         'source_manifest.json':dict(schema='rh-source-manifest/1',component=HERE.name,source_commit=PIN,
            source_files=list(inventory.values()),ranges=records,verified_against_git=True),
         'published_inputs.json':published,'retained_foundations.json':foundations}
for name,value in outputs.items(): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpts))
(HERE/'report.txt').write_text(
 f'BASE CHANGE TO SPEH — v0.44\nSource pin: {PIN}\nMain SHA256: {sha(tex)}\n\n'
 f'{len(claims)} numbered claims: 18 human finite proofs (B), one checked published application (A).\n'
 f'{len(inventory)} pinned source files; {sum(map(len,records.values()))} cited ranges.\n\n'
 'Completed: BCS3 full original DefiniteN; BCS13 full original AscComp consumer; BCS18 full original BcSpeh; '
 'BCS19 all-IsUnramU spherical cusp consequence for the same witnesses.\n'
 'The original all-rank definite-inner-form BaseChangeIsobaricN remains expressly retained. '
 'The local generic-unitary structure is one exact published MW I.10–I.11 application, shared with downstream GUA.\n'
 'Mathematical simplification: smooth Hermitian duality, using the actual positive local forms and retained bz, '
 'reverses the ascending exponents without a new local Gelfand–Kazhdan input. '
 'The finite segment order then gives the literal unique cosocle.\n'
 'Every original positive length, rank sum, normalized cusp, split component map, inert parameter and infinity multiset is preserved. '
 'The Satake residue norm q_w remains distinct from the IsUnramInv q.\n'
 'No common/frozen v0.43 files changed. No source edits, Lean replay or formal-proof recertification. '
 'No whole RH/GRH dependency-leaf closure is asserted by this component.\n')
hashes={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}
(HERE/'hashes.json').write_text(json.dumps(dict(component=HERE.name,artifact_version='0.44',hashes=hashes),indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,records.values())),
                     main_tex_sha256=sha(tex),completed=completed,whole_original_leaf_closures=0),indent=2))
