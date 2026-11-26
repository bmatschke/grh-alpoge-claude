#!/usr/bin/env python3
"""Reproduce the LS source ledger from immutable Lean bytes, without a build.

This script checks the supplied-data reconstruction's source provenance. It
does not formalize or kernel-check the shorter human proofs in main.tex.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
args = ap.parse_args()
repo = args.repo.resolve()
assert subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip() == PIN

D = 'src/Development/AbelianVarietyTheory/'
I = D + 'Proofs/IwasawaDecomposition/'
A = D + 'Definitions/AutomorphicMembership/'
F = 'src/Formalism/LocalToGlobal/'
C = F + 'Columns/'
HF = F + 'HermitianForms/'
G = F + 'GroupLattices/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive|instance)\s+([^\s:({]+)')
boundary_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                         r'(?:theorem|lemma|def|abbrev|structure|class|inductive|namespace|section|end|'
                         r'variable|attribute|set_option|open|include|instance|example)\b')
files = {}
cache = {}


def read_source(path):
    if path in cache:
        return cache[path]
    blob = subprocess.check_output(['git', '-C', str(repo), 'show', f'{PIN}:{path}'])
    present = (repo / path).exists()
    if present:
        assert (repo / path).read_bytes() == blob, ('worktree differs from pin', path)
    lines = blob.splitlines(keepends=True)
    decoded = [line.decode('utf-8').rstrip('\r\n') for line in lines]
    frames, decls = [], []
    for n, line in enumerate(decoded):
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', line)
        end = re.match(r'^end(?:\s+(\S+))?\s*$', line)
        if ns:
            frames.append(('namespace', ns.group(1)))
        elif sec:
            frames.append(('section', sec.group(1)))
        elif end:
            assert frames, ('unmatched top-level end', path, n + 1)
            kind, name = frames.pop()
            if end.group(1):
                assert name == end.group(1), ('namespace/section close mismatch', path, n + 1, name, end.group(1))
        match = decl_re.match(line)
        if match:
            spelling = match.group(2)
            namespace = '.'.join(name for kind, name in frames if kind == 'namespace')
            if spelling.startswith('_root_.'):
                qualified = spelling[len('_root_.'):]
            else:
                qualified = f'{namespace}.{spelling}' if namespace else spelling
            decls.append(dict(start=n, spelling=spelling, qualified=qualified, kind=match.group(1)))
    files[path] = dict(path=path, sha256=digest(blob), bytes=len(blob), line_count=len(lines),
                       verified_equal_to_pinned_git_blob=True, worktree_source_present=present,
                       worktree_bytes_compared_to_git_blob=present, url=f'{URL}/blob/{PIN}/{path}')
    cache[path] = (lines, decoded, decls)
    return cache[path]


def source(path, name, role='source_counterpart'):
    lines, decoded, decls = read_source(path)
    found = [d for d in decls if name in (d['spelling'], d['qualified'])]
    if not found:
        found = [d for d in decls if d['qualified'].endswith('.' + name)]
    assert len(found) == 1, (path, name, [d['qualified'] for d in found], [d['spelling'] for d in decls])
    d = found[0]
    start, stop = d['start'], len(lines)
    for n in range(start + 1, len(lines)):
        if boundary_re.match(decoded[n]):
            stop = n
            break
    while stop > start and not decoded[stop - 1].strip():
        stop -= 1
    raw = b''.join(lines[start:stop])
    assert raw and stop > start
    return dict(path=path, declaration=d['qualified'], source_spelling=d['spelling'],
                declaration_kind=d['kind'], line_start=start + 1, line_end=stop, role=role,
                sha256=files[path]['sha256'], full_file_sha256=files[path]['sha256'],
                range_sha256=digest(raw), range_bytes=len(raw), first_line=decoded[start],
                declaration_lines_within_range=[start + 1],
                url=f'{files[path]["url"]}#L{start + 1}-L{stop}',
                verified_equal_to_pinned_git_blob=True)


def ss(path, names, role='source_counterpart'):
    return [source(path, name, role) for name in names.split()]


FP = D + 'Proofs/FoundationProofs/'
RDL = 'src/ReciprocityTheory/DualLattices/'
CR = D + 'CrystallinePeriods/'
FL = 'src/Formalism/SharpRestriction/LevelLetterCocycles/'
WA = 'src/Formalism/WeaklyAdmissibleFiltrations/'
GT = I + 'GoodTupleConditionOfIdempotentZero.lean'

def all_sources(path, role='substantive_supplier_proof'):
    _,_,decls=read_source(path)
    return [source(path,d['qualified'],role) for d in decls if d['kind'] not in ('instance',)]

def alls(base,names,role='substantive_supplier_proof'):
    return sum((all_sources(base+n+'.lean',role) for n in names.split()),[])

COMMON=('The local prime is any rational prime, including two; Omega is the algebraic closure of Q_p and C its completion with |p|=p^-1. Ordinary finite-extension valuation theory, profinite Galois theory, finite fields, Witt identities and the defining completion/localization constructions are background. The actual Fontaine rings are constructed and identified, not replaced by an abstract field model.')
BOUND=('Human mathematical reconstruction only: no Lean compilation/kernel replay, no formalization of replacement arguments and no RH/GRH claim. Stage existence uses the exact supplied Base, Cols and adapted RowsRest; it does not construct a nonempty arithmetic twist-reading family or comparison functors for geometric representations.')

def cl(n,title,statement,deps,sources,assumptions=(),relation='Complete human proof of the stated literal source conclusion, sometimes simplifying the supplier argument.'):
    return dict(id=f'LS{n}',title=title,status='derived_simplification',statement=statement,
        depends_on=deps,assumptions=[COMMON,BOUND]+list(assumptions),
        proof_location=dict(file='main.tex',anchors=[f'LS{n}']),expanded_notes=dict(file='report.txt',section=f'LS{n}'),
        mathematical_status='proved_under_exact_declared_background_and_supplied_data_hypotheses',
        source_relation=relation,sources=sources)

claims=[
cl(1,'Uniform Ax approximation and completed fixed fields',
   'Every algebraic element whose H-orbit differences have norm at most r is within 16r of an algebraic H-fixed element. Thus C^H is the closure of Omega^H, and C^(G_K)=K for finite K.',[],
   alls(I,'BoundedOrbitHasNearbyFixedPoint AxSenTateComplexPadicFixedClosure CLTateInvariantsFiniteExtensionMem')),
cl(2,'Cyclotomic degrees and uniformly bounded trace projections',
   'For n>=1 the normalized trace K_(n+m)->K_n has norm at most p, with exact relative degree p^m. Compatible projections extend to the completed cyclotomic union and converge to its identity, including p=2,n=1.',[],
   alls(I,'NormSubOnePowTotient')),
cl(3,'All nonzero Tate-twist invariants vanish',
   'For every finite K/Q_p and nonzero integer i, the chi^i-twisted G_K invariant subspace of C is zero. Uses uniform projections for Q_p and a finite-coset product for K.', ['LS1','LS2'],
   alls(I,'EqZeroOfTateTwistInvariantFiniteExtension')),
cl(4,'Actual Ainf, surjective Fontaine theta and principal kernel',
   'Theta on W(lim_F O_C/p) is onto and its kernel is generated by the actual cyclotomic xi; p is regular on every xi-power quotient, which is p-adically complete. The dyadic xi unit calculation is explicit.', ['LS2'],
   alls(RDL,'DvdOfCoeffZero ValUntiltESubOne AinfFacts')+
   alls(I,'FontaineThetaEqZeroIffFontaineXiElementDvd FontaineXiPowSaturatedQuotientComplete')),
cl(5,'Actual de Rham DVR, filtration and algebraic section',
   'The xi-adic completion of Ainf[1/p] is a complete DVR, embeds its input, and its localization is the actual BdR field. Hensel uniqueness constructs the G-equivariant algebraic section on Omega with prescribed Z_p constants.', ['LS4'],
   alls(I,'EqZeroOfForallXiPowDvd BdRPlusFiltrationEqFontaineXiPow BdRPlusIsDomainBdRIsField ThetaBdRPlusSurjectiveKerUnitsEquivariant ExistsIsBdRPlusSectionOfTheta')),
cl(6,'Actual divided-power completion and injective bounded de Rham embedding',
   'The p-adic completion of the actual divided-power envelope embeds in BdR+. Truncated sandwich modules give the required bound p^n modulo xi^n; a finite divided-power intersection calculation proves injectivity after completion.', ['LS4','LS5'],
   alls(I,'AcrisMembershipSpanIff Acris0TorsionFree ExistsCanonicalAcrisToBdRPlus AcrisDivisibleOfKernelPowers AcrisFiltrationApproxByEnvelopeKernelPower AcrisToBdRPlusInjective')),
cl(7,'Integral logarithms, unit quotient and cyclotomic period',
   'For every tilt element e with sharp one, the integral logarithm t_e equals ([e]-1) times a unit in Acris, including p=2. The chosen t has phi(t)=pt, Galois action chi(t), and is a BdR+ uniformizer.', ['LS2','LS4','LS5','LS6'],
   alls(I,'ExistsTeichmullerTiltMinusOnePowDivEnvelope ExistsLogTeichmullerAcrisEqMuMulUnit AcrisLogTeichmullerUniqueGaloisFrobeniusBdR AcrisGaloisActionFontaineTEqCyclotomic AcrisFrobeniusFontaineTEqMul FontaineTIsUnitBcrisAndUniformizerBdRPlus')),
cl(8,'Candidate crystalline localization, unramified constants and core maps',
   'On Acris[1/t], p is invertible and the actual de Rham inclusion, unramified embedding, Frobenius and Galois actions have the required same-data laws. Identification with all source localization generators is deferred to LS13.', ['LS4','LS5','LS6','LS7'],
   alls(I,'ExistsCompatibleRootsOfUnityAndTiltPadic ExistsCyclotomicChar ExistsAlgEquivRootOfUnityEqPow RootOfUnityPrimeToTeichmullerLift ExistsMaxUnramifiedEmbeddingIntoBcris LocalPeriodRingsDataUnramifiedLaws PeriodRingsGaloisActionLawsFrobeniusComm ResEqIff')+
   ss(A+'IsCrisP.lean','Core IsCrisP IsSec IsLogA','literal_record_interface')),
cl(9,'Frobenius injectivity through divided-power completion',
   'Witt Frobenius is injective on the completed divided-power ring and on its t-localization. The finite coefficient induction with explicit indices proves the required divisibility on A[w/p]; bounded truncations then prove completion injectivity.', ['LS4','LS6','LS7','LS8'],
   alls(I,'FrobeniusPeriodRingInjective')),
cl(10,'Integral Frobenius fixed ring',
   'The phi-fixed subring of Acris is exactly Z_p, by reduction to Ainf modulo p, finite-residue nilpotence and successive fixed p-adic digits.', ['LS4','LS6'],
   alls(I,'AcrisFrobeniusFixedEqPadicInt')),
cl(11,'Simultaneous theta-Frobenius kernel and integral image decomposition',
   'If theta(phi^n a)=0 for all n then mu divides a in Ainf. Moreover phi(Acris) is contained in Ainf+w Acris for p w=mu^(p-1).', ['LS4','LS6','LS7'],
   alls(I,'TeichmullerTiltMinusOneDvdOfThetaFrobeniusZero FrobeniusAcrisDecompositionMuPower')),
cl(12,'Integral matching-filtration eigenvectors',
   'If phi(x)=p^r x in Acris and j(x) lies in Fil^r, then p^k x=z t^r for some k>=0,z in Z_p. The induction explicitly constructs the divided eigenvector, also at p=2.', ['LS5','LS6','LS7','LS10','LS11'],
   alls(I,'AcrisFrobeniusEigenFilEqQlMulTPow')),
cl(13,'Exact source Bcris localization and fundamental intersection',
   'All source logarithmic localization generators are units in Acris[1/t], identifying the actual Bcris and Core. Bcris^(phi=1) intersect iota^-1(BdR+) equals Q_p.', ['LS5','LS6','LS7','LS8','LS12'],
   alls(I,'BcrisEqAcrisLocalizationPeriodT BcrisFrobeniusFixedFilZeroEqQp NonemptyLocalPeriodRingsData')+
   alls(CR,'CrisLoc','literal_localization_and_source_identification')),
cl(14,'De Rham invariants for every finite base field',
   'BdR^(G_K)=o(K): all negative-filtration invariants are excluded by Tate-twist vanishing, and a positive-filtration invariant with zero residue vanishes by separation.', ['LS1','LS3','LS5','LS7'],
   alls(I,'BdRGaloisInvariantsEqFinExt')),
cl(15,'Crystalline invariants for every finite base field',
   'Bcris^(G_K)=u(K intersect Q_p^ur). Frobenius orbits are finite by a common minimal polynomial; a prime-to-p root orbit and finite polynomial interpolation use the fundamental intersection to isolate b.', ['LS8','LS9','LS13','LS14'],
   alls(I,'GaloisInvariantsBcrisEqMaxUnramified')),
cl(16,'Every actual finite-extension PeriodData field',
   'The same actual rings give PeriodData for every finite K, with the exact action, invariant, Frobenius, inclusion, filtration, period, character and fundamental-intersection fields and IsRealPD ties.', ['LS5','LS7','LS8','LS9','LS13','LS14','LS15'],
   alls(I,'ExistsConcretePeriodDatumPadicFiniteExtension')+
   alls(A,'IsRealPD','literal_same_ring_interface')),
cl(17,'All local prime, Ainf and literal period-ring ties',
   'For every rational prime p there exist a LocPrime P, LocAinf AI and LocTied P AI on the specified Fontaine rings, including all finite-K equalities, normalized valuations, integral filtration and logarithmic clauses. Choosing them for all primes gives LocStage.', ['NC1','NC2','LS4','LS5','LS6','LS7','LS8','LS13','LS16'],
   alls(I,'ExistsLocalPrimeAinf ExistsAddValuationNormalised LocStageInhabited')+
   ss(FL+'DataNLoc.lean','LocRings LocPrime LocTheory LocAinf','literal_full_record_interface')+
   alls('src/Formalism/LocalRingCardinality/AdicCompletionLocal/','LocTied','literal_full_record_interface')+
   ss(A+'NStageTrivialCharacterCoeffEq.lean','LocStage','literal_full_record_interface')),
cl(18,'Global cyclotomic data, selected primes and residue multiplicative maps',
   'Construct actual LData and its finite-value shaTrue reading, a CM-conjugation lift, the selected nonconjugate split prime representatives, and multiplicative Teich/reduction maps with precisely prime-to-target-characteristic injectivity.', ['AH12'],
   ss(GT,'finite_placesOver nonempty_lData isAlgebraic_rat exists_isCMConjOm conj_mul_conj conj_ne_one exists_transversal exists_places finrank_K discr_K split_K exists_teichC isOfFinOrder_fbar nonempty_reduction exists_iota lData shaTrue shaTrue_nonneg two_le_r f_pos')+
   alls(I,'ExistsRingHomOfIsIntegral'),
   relation='Reconstructs all nonempty suppliers. The multiplicative Teich map is constructed directly from compatible finite cyclic groups; the record does not require an additive field map.'),
cl(19,'Actual tame generators at the selected primes',
   'A compactness argument for nested finite cyclic inertia quotients gives gamma such that inertia is generated topologically by gamma and the explicitly defined wild subgroup, proving literal TameGenAt at each selected valuation.', [],
   alls(FP,'ExistsTameGenAtOfValuationSubring')),
cl(20,'Complete empty-local and empty-twist algebraic records',
   'For the exact row conditions shaLen=shaTrue, etaJ=0 in range and zero projectors, construct NData, NAut, NBC, NTw, NExp and NTh. Loc and Tw are empty; the remaining global multiset and character data are explicitly constructed and all nonvacuous laws checked.', ['LS18'],
   ss(GT,'monic_unip nData UnrPar UnrPar.scale UnrPar.add normV_cpow_ne_zero normV_ne_zero UnrFam negOneFam nAut nBC nTw nExp nTh')+
   ss(FL+'DataN.lean','NData NAut NBC NTw NExp NTh','literal_full_record_interfaces'),
   assumptions=['The literal supplied Base, Cols and RowsRest satisfy LS.44; the finite-group cardinal field is the one already present in RowsRest. Synthetic bare models are not identified with automorphic or geometric classification theories.']),
cl(21,'Full NTypes and exact NStage with prescribed LocStage',
   'The actual finite-polynomial idempotent and tame/residue models supply every NTypes field. Its good-tuple idempotent is zero, so all projector and coefficient ties hold. Every bridge and etaJ field is checked, yielding NStage with toLocStage equal to the prescribed L; adaptation supplies the exact row hypotheses.', ['SE13','LS17','LS18','LS19','LS20'],
   ss(GT,'unipSer unip_coeff_zero unipSer_sum unipSer_of_squarefree rootsBar_unip cenTriv nTypes idempotent_good_tuples_eq_zero good_tuple_condition_of_idempotent_zero exists_nStage_of_rows adapt exists_nStage_adapt exists_nStage')+
   ss(FL+'DataN.lean','NTypes NTypes.e0 NTypes.IdempotentMatchesAction','literal_record_and_projector_interface')+
   ss(A+'NStageTrivialCharacterCoeffEq.lean','NStage','literal_full_record_interface')),
cl(22,'Bare Later exists on the same adapted rows and retains arithmetic boundaries',
   'For supplied I, literal Laws l, and HasLetters on the same B, Later(B,I.cols(l)) is inhabited. LS supplies the exact full NStage/LocStage premise of SE14; this particular stage has empty Tw and cannot admit NChoice over nonempty coefficient places.', ['SE6','SE7','SE8','SE10','SE11','SE12','SE14','LS17','LS21'],
   ss(A+'ExistsOkPins.lean','fits later','literal_closed_endpoint')+
   ss(A+'LatAtLattice.lean','Later','literal_final_record')+
   ss(FL+'DataN.lean','NTw','empty_twist_boundary'),
   assumptions=['The source I, its Laws and HasLetters are supplied; no arithmetic RankTie, MuIsW, nonempty twist reading, true representation comparison, or positive quantitative projector bound is inferred.'])
]

targets=[]
def target(path,name,scope,ids):
    t=source(path,name,'remaining_stronger_same_object_supplier')
    t.update(priority_group=4,remaining_human_scope=scope,source_connections=ids,
        human_status='bare_existence_closed; stronger_same_object_compatibility_retained')
    targets.append(t)
target(A+'NStageTrivialCharacterCoeffEq.lean','NStage',
    'A stage compatible with the actual arithmetic twist reading and geometric representation data. LS21 proves the literal bare existential theorem using Loc=Tw=Empty; that particular model cannot supply a map from all nonempty coefficient places to Tw. Do not reopen actual local period-ring existence, which is closed by LS17.', ['LS17','LS21','LS22','NC17'])
target(D+'Proofs/InertiaEigenvalues/ExistsTiedChoiceOfReads.lean','exists_tied_choice_of_reads',
    'Supply the literal same-stage reads, index/side/Q compatibility and local character ties on a stage with adequate Tw. Empty Loc alone does not imply the global twist-index choice. NC proves the construction under those exact inputs and RC analyzes their additional joins.', ['LS22','NC17'])
target(A+'RationalRootsDef.lean','MuIsW',
    'Actual geometric/rank/weight compatibility for the stage used by the arithmetic comparison. The zero-projector bare model has no positive-rank conclusion; RC may close exact reset joins under its retained hypotheses, without identifying them with LS21 automatically.', ['LS22','NC15'])

closed=[]
for path,name,ids in [
 (I+'NonemptyLocalPeriodRingsData.lean','nonempty_core',['LS4','LS5','LS6','LS7','LS8','LS12','LS13']),
 (I+'ExistsConcretePeriodDatumPadicFiniteExtension.lean','exists_realPD',['LS16']),
 (I+'ExistsLocalPrimeAinf.lean','exists_locPrime_tied',['LS17']),
 (I+'LocStageInhabited.lean','locStage_inhabited',['LS17']),
 (GT,'exists_nStage_of_rows',['LS18','LS19','LS20','LS21']),
 (GT,'exists_nStage_adapt',['SE13','LS21']),
 (GT,'exists_nStage',['LS21']),
 (A+'ExistsOkPins.lean','later',['SE14','LS22'])]:
    s=source(path,name,'closed_literal_source_endpoint');s['closed_by']=ids;closed.append(s)

audits=[]
for path,name,ids in [
 (A+'IsCrisP.lean','Core',['LS8','LS13']),
 (A+'IsRealPD.lean','IsRealPD',['LS16']),
 (FL+'DataNLoc.lean','LocPrime',['LS17']),
 (FL+'DataNLoc.lean','LocAinf',['LS17']),
 ('src/Formalism/LocalRingCardinality/AdicCompletionLocal/LocTied.lean','LocTied',['LS17']),
 (A+'NStageTrivialCharacterCoeffEq.lean','LocStage',['LS17']),
 (A+'NStageTrivialCharacterCoeffEq.lean','NStage',['LS21']),
 (FL+'DataN.lean','NTypes',['LS21'])]:
    s=source(path,name,'literal_record_field_inventory')
    lines,_,_=read_source(path);raw=b''.join(lines[s['line_start']-1:s['line_end']]).decode()
    fields=re.findall(r'^  (?:\[)?([^\s\[:]+)\s*:',raw,re.M)
    assert fields,('no record fields',path,name)
    audits.append(dict(source=s,named_fields=fields,named_field_count=len(fields),
        used_by=ids,note='Exact named field declarations inventoried; inherited fields are covered by their separate record inventory. This is a source audit, not elaboration or kernel checking.'))

mb=(HERE/'main.tex').read_bytes()
for c in claims:
    n=int(c['id'][2:]);a=mb.index(f'\\paragraph{{LS{n}:'.encode())
    z=mb.index(f'\\paragraph{{LS{n+1}:'.encode(),a+1) if n<22 else len(mb)
    c['proof_paragraph_sha256']=digest(mb[a:z])

out=dict(schema_version='1.3',artifact_version='0.18',date='2026-11-22',owner='/root/global_frame',
 repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes, without newline or Unicode normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
    missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
    lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
    replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Complete human proof of the exactly stated assertion under ordinary declared background and supplied source inputs, with stronger geometric/arithmetic hypotheses explicitly retained.'),
 claims=claims,files=[files[p] for p in sorted(files)],record_field_audits=audits,
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
 prior_components_reused=['NC1','NC2','AH12','SE6','SE7','SE8','SE10','SE11','SE12','SE13','SE14'],
 same_iteration_companions=['RC','IG','TD'],independent_reviews=[],
 scope='LS1–LS17 construct the actual integral Fontaine rings and all local-stage fields, including invariants and literal ties. LS18–LS21 construct every field of the source bare empty-index NStage on the same base/columns/rows and prescribed LocStage. LS22 closes bare Later existence for supplied I, Laws and HasLetters. Stronger arithmetic/geometric same-object conditions remain explicit.',
 boundary_resolved=['Actual integral Ainf/Acris/Bcris/BdR construction and bounded injective comparison','Actual period invariants, filtration, t and fundamental intersection','All finite-extension PeriodData fields','All-prime LocStage with full LocAinf/LocTied','All fields of literal exists_nStage_of_rows and exact adapt join','Bare Later existence on the same adapted RowsRest'],
 retained_inputs=[COMMON,BOUND,'Supplied Base/Cols/RowsRest and the stated exact adaptation or four row conditions','Supplied I, Laws and HasLetters for the Later join','An adequate nonempty twist-reading stage for NChoice; this bare Tw=Empty stage cannot supply it','Actual RankTie/MuIsW/LocsCarry and geometric local comparison data where subsequent theorems require them','Ordinary number-field, profinite and Witt background is used; no arbitrary crystalline representation comparison is claimed'],
 dependency_precision=['LS8 constructs a provisional Acris[1/t] ring and its maps; it has no LS13 dependency.','LS13 uses integral LS12 to identify every actual localization generator and then transports the LS8 maps.','The fundamental intersection LS13 precedes LS15; LS15 is not used to prove that intersection.','LS17 assembles genuine all-prime local data before the empty-index NStage is installed.','LS18–LS20 do not use a future arithmetic NChoice or V4.Core.','LS21 retains the prescribed LocStage and exactly the same Base/Cols/RowsRest.','LS22 discharges only the same-row bare existence input of frozen SE14, without rewriting old claims or their source arrays.'])

for name,who,nums in [
 ('root_reviews_local_stages.txt','/root',list(range(1,23))),
 ('ig_reviews_ls_1_8.txt','/root/comparison_span',list(range(1,9)))]:
    review=HERE.parent/'reviews_v0_18'/name
    if review.exists():
        rb=review.read_bytes();rt=rb.decode();ph={}
        for n in nums:
            h=claims[n-1]['proof_paragraph_sha256']
            assert h in rt,('reviewed paragraph changed',n,h)
            ph[f'LS{n}']=h
        out['independent_reviews'].append(dict(reviewer=who,result='PASS',claim_ids=list(ph),
          review_record='../reviews_v0_18/'+name,review_record_sha256=digest(rb),paragraph_sha256=ph,lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc.extend([f"{c['id']} | {c['title']} | {c['mathematical_status']}",c['statement'],
       'proof_paragraph_sha256: '+c['proof_paragraph_sha256']])
    for s in c['sources']:
        loc.extend([f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
          '  role: '+s['role'],'  file_sha256: '+s['full_file_sha256'],
          '  range_sha256: '+s['range_sha256'],'  '+s['url']])
    loc.append('')
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.18',commit=PIN,targets=targets,closed_source_targets=closed,
 remaining_boundary='Actual local-period-ring and bare NStage/Later existence are closed. Continuing work concerns an adequate same-stage twist reading and genuine geometric/rank/weight/local comparison hypotheses. Tw=Empty prevents this particular bare stage from supplying NChoice; Loc=Empty alone does not remove its separate twist-read antecedent.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
 source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),source_files=len(files),
 record_fields=sum(a['named_field_count'] for a in audits),next_targets=len(targets),closed_targets=len(closed),
 verified_equal_to_pinned_git_blob=True,artifact_sha256=out['artifact_sha256'])))
