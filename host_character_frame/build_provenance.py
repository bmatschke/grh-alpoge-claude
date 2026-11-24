#!/usr/bin/env python3
"""Reproduce the HF source ledger from immutable Lean bytes, without a build.

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
HFORMS = F + 'HermitianForms/'
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
                       verified_equal_to_pinned_git_blob=True, url=f'{URL}/blob/{PIN}/{path}')
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



WC = 'src/Development/AutomorphicArithmetic/WeightCongruences/'
AL = D + 'Proofs/AdelicLatticeProofs/'
GI = D + 'Proofs/GlobalInterpolation/'
FD = D + 'Definitions/Foundations/'

def all_sources(path, role='substantive_supplier_proof'):
    _, _, ds = read_source(path)
    return [source(path,d['qualified'],role) for d in ds if d['kind'] != 'instance']

def alls(base,names,role='substantive_supplier_proof'):
    return sum((all_sources(base+n+'.lean',role) for n in names.split()), [])

CH = F + 'UnitaryNorms/CharHost.lean'
HC = F + 'UnitaryNorms/IsUnitaryNormOf.lean'
CT = F + 'UnitaryNorms/CharTied.lean'
DT = A + 'IsRationalUnitaryDeterminantMapRationalUnitaryTo.lean'
DQ = A + 'IsRationalUnitaryDeterminantMapRationalUnitary.lean'
BASE = FD + 'RootOfUnityEightQMemCoeffGaloisSubfield.lean'
TOP = A + 'CmQuadraticFormEqAlternatingForm.lean'
EC = I + 'ExistsColumnInputAssembled.lean'
CAN = I + 'EvLgCanonical.lean'
EP = A + 'ExistsOkPins.lean'
LAT = A + 'LatAtLattice.lean'
CORE = A + 'RationalRootsDef.lean'
CLAUSES = A + 'ExistsStagesClauses.lean'

COMMON = ('Ordinary number fields, ideal factorization, residue fields, completion and restricted-product topology, Chinese remaindering, finite Galois closures, the circle-root/Zorn extension principle and quadratic reciprocity are background. The actual host CM/unramified/split and root identities are the prior AH/AC claims, and class-group finiteness is TL14.')
BOUND = ('Human proof only: no Lean compilation or kernel replay, no formalization of replacement arguments, and no RH/GRH conclusion. Actual HFrame and original same-base column/jet/stage existence are proved; stronger V4.Core, arithmetic twist compatibility, global theta tests and quantitative hypotheses are not inferred from nonempty records.')

def cl(n,title,statement,deps,sources,assumptions=(),relation='Human proof of the literal source conclusion under precisely stated data, with a simpler mathematical proof where indicated.'):
    return dict(id=f'HF{n}', title=title, status='derived_simplification',
        statement=statement, depends_on=deps, assumptions=[COMMON,BOUND]+list(assumptions),
        proof_location=dict(file='main.tex',anchors=[f'HF{n}']),
        expanded_notes=dict(file='report.txt',section=f'HF{n}'),
        mathematical_status='proved_under_exact_declared_background_and_supplied_data_hypotheses',
        source_relation=relation, sources=sources)

claims = [
cl(1,'Root compatibility for the actual host',
   'A principal norm-one unit of a CM field is a root of unity; for the actual host the CM-type product and norm to K of every root are one. MUQ supplies the exact integral weighted compatibility.',
   ['AC2','AC3','AH10'],
   alls(I,'ExistsUnitOfRoot')+
   alls(WC,'RootOfUnityGaloisActionCMDatum ProdCmTypeEqNormAndWeightCongruenceOne IsRootOfIntegral')+
   ss(WC+'ProdNegOneZpow.lean','MU MUQ','literal_weight_compatibility')),
cl(2,'Open-subgroup continuous circle-character extension',
   'Compatible character prescriptions on an open subgroup U and a homomorphic image alpha(A) extend to one continuous circle character on the whole abelian group.',
   [],
   alls(AL,'ExistsContinuousCircleCharExtension')+
   alls(I,'ExistsUnitaryCharOfOpenSubgroupAndHom'),
   relation='Direct product/intersection construction, divisible-circle one-generator extension and Zorn; equivalent to the source quotient construction.'),
cl(3,'Actual tame local model and idele conjugation',
   'Residue characters extend to tame continuous local characters; their finite product and the specified infinite phases give a continuous model on unitIdl. Conjugation extends to actual completions and ideles, with all IsConjI laws.',
   ['AH10'],
   alls(I,'ExistsTameLocOfResidue ContinuousOfTameLoc ContinuousOfValuedEq UnitOpenAndCongrOpen')+
   ss(DT,'unitIdl IsConjI TameLoc CMData','literal_model_interfaces')),
cl(4,'Anticyclotomic extension with exact local support',
   'For a selected prime set disjoint from its conjugate and the stated root compatibility, construct a unitary Hecke character trivial on F with infinity exponent -2e, prescribed selected residue characters, inverse conjugate characters, unramifiedness elsewhere, and exact local power kernels.',
   ['HF1','HF2','HF3'],
   alls(I,'ExistsHeckeCharTrivOnRealSubfieldInfinityType')+
   ss(HC,'HChar HasInf HasInfQ TrivOn TameAt UnrAt','literal_character_conventions'),
   assumptions=['The finite selected set contains no conjugate pair; the displayed weighted root/residue product equals one.']),
cl(5,'Global finite order from the actual local laws',
   'A zero-infinity-type character with finite tame ramification and unramified local units elsewhere has positive finite global order; for the constructed delta it divides 15 times the class-group exponent.',
   ['TL14'],
   alls(I,'HeckeCharFiniteOrderOfTrivialAtInfinity FiniteIndexUnitIdlSup IdeleCharacterTrivialOnLocalUnits'),
   relation='Proves the tame finite-support specialization used for delta directly by local-unit density and the ordinary class group. The broader arbitrary-level source theorem is not silently generalized.'),
cl(6,'Split prime orientation and norm-compatible residue products',
   'Complete splitting gives e=f=1, no conjugation-fixed prime, rational-prime residue norm and first-order p. The product over primes above one K-prime equals the residue of Norm(E/K), and primitive/exact-order residue characters exist.',
   ['HF1','AH9','AH10'],
   alls(I,'CompletelySplitPrimeHostPlaceProperties ExistsInjectiveCharacterOfIsCyclic')+
   alls(WC,'ProdResidueCharNormOneUnitEqOne')+
   ss(CH,'PiBar PiBar.Div Omg','literal_selected_prime_and_character_records')),
cl(7,'Construct every actual IsMu0 field on one PiBar and Omg',
   'For the exact integral MUQ weights and the two completely split auxiliary primes, construct all mu0_j with HasInfQ(-e), prescribed inverse powers omega_k^(-2(j+1)), trivial real restriction, tameness and exact unramified support.',
   ['HF1','HF4','HF6'],
   alls(I,'ExistsUnitaryMuZeroCharactersOfSplitTypePrimesAl')+
   ss(CH,'IsMu0 Mu0Exists','literal_six_field_endpoint'),
   assumptions=['Both auxiliary rational primes split completely; the supplied rational weights are integral and satisfy MUQ.']),
cl(8,'Construct the actual unramified chiPsi',
   'The empty selected set and e=-1 give a unitary everywhere-unramified Hecke character trivial on F with infinity exponent 2, filling IsChiPsi.',
   ['HF1','HF4'],
   alls(I,'ExistsUnramifiedCmTypeHeckeCharOnHost')+
   ss(CH,'IsChiPsi','literal_four_field_endpoint')),
cl(9,'Prove the host quadratic product formula',
   'The finite inert/split quadratic characters and infinite signs have product one on every principal F-idele. The proof reduces to a Jacobi norm identity away from d and removes bad valuations by explicit norm/CRT constructions.',
   ['AH10','AH11','AH12'],
   alls(I,'QuadraticCharProductFormulaCMHost IsUnitNormOfIsCoprime EtaEqJacobiSym')+
   ss(HC,'etaFin etaInf ResEta','literal_quadratic_restriction'),
   assumptions=['The actual host contains Q(sqrt(qd)), has d prime with its given congruences, and every prime over the host conductor splits in E/F; these are earlier host conclusions.']),
cl(10,'Construct eta from the exact odd-infinity overlap condition',
   'For a finite-unramified CM extension with the principal quadratic product formula and the stated root delta/phase/even-inert-order condition, construct a unitary everywhere-unramified Hecke character with odd prescribed infinity type and exact quadratic restriction to F.',
   ['HF1','HF2','HF3','HF9'],
   alls(I,'ExistsUnramifiedResEta'),
   assumptions=['Every root zeta has delta=zeta bar(delta), even order at inert primes, and prescribed phase product one. Infinity exponents are odd.']),
cl(11,'Construct the actual host IsEtaT',
   'The choices delta=1+zeta for zeta != -1 and delta=sqrt(-d) for zeta=-1 satisfy the precise phase/inert-order conditions, so HF10 constructs the actual host eta with all four IsEtaT fields.',
   ['HF1','HF9','HF10','AH12'],
   alls(WC,'ProdCmTypePhaseOneAddRootOfUnity ExistsUnitEqRootOfUnityMulConjPhaseOne')+
   alls(I,'HostEtaTildeCharacterExists')+
   ss(CH,'IsEtaT EtaTExists','literal_actual_eta_endpoint')),
cl(12,'Construct both exact-order-fifteen local delta characters',
   'For either distinguished prime p=1 mod 15 completely split in E, construct a finite-order character trivial on F, tame everywhere and unramified off p, whose local unit power kernel at every prime over p is exactly 15|n. The two deltas are nontrivial and distinct.',
   ['HF1','HF4','HF5','HF6'],
   alls(I,'HostDeltaCharacterInertialOrderFifteenExists IsTwistOfIsDelta')+
   ss(CH,'IsDelta DeltaExists IsPsi','literal_delta_and_distinct_IsPsi_boundary')+
   ss(DT,'IsTwist','literal_finite_tame_twist_interface'),
   assumptions=['p is prime, p=1 modulo 15 and completely split; global exact order fifteen and prime-power IsPsi are not asserted.']),
cl(13,'Construct the full same-host HFrame',
   'The actual four producers fill every HFrame field on one host and the prescribed weights. For Pre with supplied PreX.e_even, its level congruences supply the split hypotheses and hence actual Top.Fr is inhabited.',
   ['HF6','HF7','HF8','HF11','HF12','AH9'],
   alls(I,'NonemptyHostHeckeCharacterFrame ExistsHFrameDtPackPre')+
   ss(I+'NcardPrimesOverOfStabilizer.lean','split_of_one_mod')+
   ss(DT,'HFrame','literal_full_record')+
   ss(TOP,'Fr Fr.at','same_frame_on_stages'),
   assumptions=['Literal Host and integral MUQ weights; the Pre specialization uses its actual PreX, rather than constructing arbitrary missing decorations. IG10 later supplies one original such input.']),
cl(14,'Actual determinant quotient and rational unitary character law',
   'KD is open and contains infinity and diagonal F; actual mu0 and chiPsi finite restrictions descend, chiPsi kills the unit image, and explicit Hilbert 90 gives e1 with chiD(e1(z))=product phi(z)^(-1).',
   ['HF7','HF8'],
   alls(I,'UnitaryDeterminantKernelOpenAndFactor ExistsConjQuotientOfRationalUnitaryDeterminantMa TildeCharacterOnUnitary')+
   ss(DT,'congG KD DtT tildeD muTilT UOT IsRationalUnitaryDeterminantMap e1T','literal_determinant_definitions')+
   ss(DQ,'finite_level isOpen_KDq exists_diag_upF_eq diag_upF_mem_KDq','actual_finite_congruence_suppliers')),
cl(15,'Full relative determinant and finer-SQ package',
   'Balanced conjugate valuations characterize KD unitIdl. Paired self-duality and the literal positive-part representative give all relDet laws and trueDtPack. The same argument with finite SQ congruences gives the actual trueDtPackQ inserted into columns.',
   ['HF14','NB1','AH11'],
   alls(I,'MemKDSupUnitIdlIff RelativeLatticeDeterminantClassLaws OrdSubDetSubSelfDual OrdFNonnegOfIsInteger TrueDtPackRelDet')+
   ss(I+'ExistsProdUnifMulUnitIdl.lean','finite_valAt_ne_one GlobalTheory.Mem.Chr.exists_prod_unif_mul_unitIdl')+
   ss(DT,'relDetT DtPack','literal_full_package')+
   ss(DQ,'KDq DtQ UOQ relDetQ KDq_sup_unitIdl toDtTMod_bijective toDtTMod_relDetQ','literal_finer_quotient')+
   ss(I+'H90USurjective.lean','KDq_le_ker trueDtPackQ trueDtPackQ_relDet','actual_SQ_constructor')),
cl(16,'One finite field for all values of this same frame',
   'One finite Galois field contains every normalized unramified value of the constructed frame, with shifts 0,1/2,0,0,0. Containment of its primitive generator in LL0 gives ValLL0 uniformly for every later assembly and then ValLL.',
   ['HF13','TL14'],
   alls(I,'ExistsGaloisGe')+
   ss(CT,'CharFrame ValLL0 ValLL','literal_character_value_fields')+
   ss(TOP,'Fr.at','same_characters_under_assembly')+
   ss(EC,'valuesIn_of lg_colIn','literal_containment_join'),
   assumptions=['The actual coefficient field must contain the finite primitive generator; full Choice.FieldOK/NumbersIn is not inferred.']),
cl(17,'Construct actual Base with finite field requirements simultaneously',
   'For a fixed Pre and three finite algebraic sets, build one conjugation-stable finite Galois coefficient field containing them, the roots, ordinary capitulation and all type-norm generators with their every-embedding norm equations. The resulting Base.toPre equals the supplied Pre.',
   ['TL14','TL17','AH10'],
   alls(I,'ConjugateEmbApply ExistsFinsetTypeNormPrincipal ProdNormEmbeddingsEqAbsNorm SubmoduleEqSpanOfPowEqSpanPow ExistsGaloisSubfieldConjStable')+
   ss(FD+'AuxiliaryFrameNormalizedSpaces.lean','exists_finset_capitulation')+
   ss(BASE,'Base','literal_full_base_record'),
   assumptions=['The supplied Pre already has its spaces, weights, numerical data and exact type-norm exponent pair relation; this field extension changes none of them.']),
cl(18,'One original canonical column input with pins and jets',
   'Starting with IG10, fix the HF13 frame and normalized oriented Pre, then contain all character/period/root/canonical-jet generators before choosing Base. The same original I satisfies Ok, Pins, IsTw, JetsIn, prescribed frame/selector/ambient and range {1,del,delprime}; all assemblies satisfy ValLL0, and Per.FieldOK holds.',
   ['IG10','IG11','SE15','HF12','HF13','HF16','HF17','TL15','CI15','CI16','CI17','CI18','PA9','PA13','CA12'],
   ss(EP,'exists_pre exists_ok_pins','original_input_source_constructors')+
   ss(GI+'ExistsHypJetsAll.lean','exists_pre_sized exists_colIn_jets','original_sized_and_jet_endpoints')+
   ss(EC,'Oriented exists_oriented valuation_pr_incA_xi0_eq_one_of_unitAA Holds exists_holds_one exists_holds exists_ram_of_mem_QE exists_colIn avoid mem_avoid_of_dvd isTwist_of_mem_set lg_colIn','actual_finite_input_and_record_join')+
   ss(CAN,'stepSet allSet gens gens_algebraic jetsIn_of_isTw evLg_canonical','actual_canonical_modulus_and_jet_join')+
   ss(LAT,'Pins','literal_both_pin_clauses'),
   relation='A proved strengthened original existence construction: takes the source finite raw constructor, then canonical replacement and the previously proved exact canonical jet generator set. It is not a new unconditional quantitative EvLg conclusion.'),
cl(19,'Same-base Laws, Later, TwForms and ordinary all-lattice jets',
   'For the actual HF18 input, construct Laws and lattice-preserving Law0, then the exact Later and TwForms on its rec7. Its ordinary kernel Hyp and JetsAll hold for every word, twist and i<m over the canonical seam of any stages on the same base.',
   ['HF15','HF18','TL13','TX10','LS22','FC7','SE7','SE8','TL19'],
   ss(EP,'laws forms_equiv law0 ipC_herm ipC_pos fits later exists_all','literal_final_existence_join')+
   ss(LAT,'cols Law0 Later rec7 tw','literal_same_object_records')+
   ss(D+'Definitions/GlobalTwisting/JetsAllOfColIn.lean','hyp_of_colIn jetsAll_of_colIn','ordinary_hyp_and_jets_endpoints')+
   ss(GI+'StepBoxIffStepSuppDeg.lean','mulLat_le_divLat inRange_indicator degAt_eq degNu_eq JetsAll jetsIn_iff JetsDeg jetsAll_of_deg cBof_pos','actual_support_and_degree_conversion'),
   assumptions=['The Later constructed here is the literal bare stage of LS22; no nonempty arithmetic twist-reading family, actual quantitative projector bound or global theta test is inferred.']),
cl(20,'Exact conditional Core join and empty-model obstruction',
   'The finite forced-prime set is explicit. A Core for TwDat.untw(empty) is impossible because forced requires g0. On one X,f,T, literal coreOfLay fills Core under its exact retained Over/Lay/RecOK/LedOK/MuIsW/numerical/row/real/character/arithmetic-choice hypotheses.',
   ['HF19'],
   ss(CORE,'RowLay MuIsW Core','literal_additional_core_fields')+
   ss(A+'AmbientBaseHeq.lean','ColLay GatNum GyLay','literal_column_and_geometric_fields')+
   ss(CLAUSES,'rowLay_iff coreOfLay exists_forced lg_forced isEmpty_core_untw','actual_conditional_join_and_obstruction')+
   ss(TOP,'TwDat TwDat.untw','actual_empty_twisting_datum'),
   relation='Proves the conditional record join and the mathematical obstruction to promoting the bare empty model. It does not mark the retained Core suppliers as reconstructed.',
   assumptions=['Retain K.Over(X.B.toPre), the one actual Lay Y, RecOK, universal LedOK, MuIsW, forced, GatNum, untwisted row identity, MtStableAt, RealTied, true dsig, exact primitive chiT and NChoice conductor-support Q=T.Q and exponent kprime=T.k equalities, all on that same stage X.'])
]

targets=[]
def target(path,name,scope,ids,priority=2):
    t=source(path,name,'remaining_stronger_same_object_supplier')
    t.update(priority_group=priority,remaining_human_scope=scope,source_connections=ids,
        human_status='actual_HFrame_and_original_join_closed; stronger_global_core_supplier_retained')
    targets.append(t)
target(CLAUSES,'coreOfLay',
    'Supply the literal same-stage Lay/RecOK/LedOK/MuIsW and remaining real, metric, theta, numerical, character and NChoice equalities. HF20 proves the conditional assembly but does not construct those stronger suppliers. The actual HFrame and original Ok/Pins/JetsIn/Laws/Later existence are now closed.',
    ['HF18','HF19','HF20','IG14'])
target(CORE,'Core',
    'Construct the actual nonempty, prime-covering twisting and arithmetic realization on the same stage with all Core fields; the bare untw(empty) model is ruled out by forced, and LS21 Tw=Empty cannot supply NChoice.',
    ['HF20','LS22','NC17','RC18'])
target(CT,'ValLL',
    'No remaining character-value existence for the fixed actual frame: HF16 supplies a finite containment generator and HF18 chooses it in LL0. Retain only transport/containment for a prescribed external coefficient field and stronger NumbersIn/Choice.FieldOK clauses handled by the theta-test branch.',
    ['HF16','HF18'],priority=4)

closed=[]
for path,name,ids in [
 (I+'ExistsUnitaryCharOfOpenSubgroupAndHom.lean','exists_unitary_char_of_open_subgroup_and_hom',['HF2']),
 (I+'ExistsHeckeCharTrivOnRealSubfieldInfinityType.lean','exists_hecke_trivOn',['HF4']),
 (I+'ExistsUnitaryMuZeroCharactersOfSplitTypePrimesAl.lean','exists_unitary_mu_zero_characters_of_split_type_primes',['HF7']),
 (I+'ExistsUnramifiedCmTypeHeckeCharOnHost.lean','exists_chiPsi',['HF8']),
 (I+'QuadraticCharProductFormulaCMHost.lean','eta_product_formula',['HF9']),
 (I+'ExistsUnramifiedResEta.lean','exists_unramified_resEta',['HF10']),
 (I+'HostEtaTildeCharacterExists.lean','etaT_exists',['HF11']),
 (I+'HostDeltaCharacterInertialOrderFifteenExists.lean','delta_exists',['HF12']),
 (I+'NonemptyHostHeckeCharacterFrame.lean','nonempty_hFrame',['HF13']),
 (I+'ExistsHFrameDtPackPre.lean','nonempty_hframe',['HF13']),
 (I+'TrueDtPackRelDet.lean','trueDtPack',['HF15']),
 (I+'H90USurjective.lean','trueDtPackQ',['HF15']),
 (I+'ExistsGaloisGe.lean','frame_values',['TL14','HF16']),
 (I+'ConjugateEmbApply.lean','exists_base',['HF17']),
 (EC,'exists_colIn',['TL15','CI15','CI16','HF18']),
 (EP,'exists_ok_pins',['HF18']),
 (GI+'ExistsHypJetsAll.lean','exists_colIn_jets',['HF18']),
 (EP,'exists_all',['HF19']),
 (D+'Definitions/GlobalTwisting/JetsAllOfColIn.lean','hyp_of_colIn',['HF19']),
 (D+'Definitions/GlobalTwisting/JetsAllOfColIn.lean','jetsAll_of_colIn',['HF19'])]:
    s=source(path,name,'closed_literal_source_endpoint');s['closed_by']=ids;closed.append(s)

audits=[]
for path,name,ids in [
 (CH,'IsMu0',['HF7']), (CH,'IsChiPsi',['HF8']), (CH,'IsEtaT',['HF11']),
 (CH,'IsDelta',['HF12']), (DT,'HFrame',['HF13']), (DT,'DtPack',['HF15']),
 (BASE,'Base',['HF17']), (LAT,'Later',['HF19']),
 (CORE,'MuIsW',['HF20']), (CORE,'Core',['HF20'])]:
    s=source(path,name,'literal_record_field_inventory')
    lines,_,_=read_source(path)
    raw=b''.join(lines[s['line_start']-1:s['line_end']]).decode()
    fs=re.findall(r'^  (?:\[)?([^\s\[:]+)\s*:',raw,re.M)
    assert fs,('no record fields',path,name)
    audits.append(dict(source=s,named_fields=fs,named_field_count=len(fs),used_by=ids,
        note='Literal named fields; inherited fields covered by their indicated earlier records. A source inventory is not elaboration or kernel checking.'))

mb=(HERE/'main.tex').read_bytes()
for c in claims:
    n=int(c['id'][2:]);start=mb.index(f'\\paragraph{{HF{n}:'.encode())
    stop=mb.index(f'\\paragraph{{HF{n+1}:'.encode(),start+1) if n<20 else len(mb)
    h=digest(mb[start:stop])
    c['proof_paragraph_sha256']=h
    c['proof_location']['paragraph_sha256']=h
out=dict(schema_version='1.3',artifact_version='0.19',owner='/root/global_frame',
    repository=dict(url=URL,commit=PIN),
    range_convention='One-indexed inclusive; exact immutable Git declaration bytes, with original newlines and Unicode.',
    verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
        missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
        lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
        replacement_arguments_formalized=False,pdf_build_or_render=False),
    status_definitions=dict(derived_simplification='Human proof of the exact stated conclusion under ordinary declared background and literal source inputs; stronger unreconstructed implications are explicitly excluded.'),
    claims=claims,files=[files[p] for p in sorted(files)],record_field_audits=audits,
    artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt']},
    prior_components_reused=sorted({d for c in claims for d in c['depends_on'] if not d.startswith('HF')}),
    same_iteration_companions=['AR','TT','QW'],independent_reviews=[],
    scope='HF1–13 construct every actual HFrame producer. HF14–17 construct determinant and coefficient-field data. HF18–19 construct an original same-base canonical Ok/Pins/JetsIn/Laws/Later/TwForms and ordinary Hyp/JetsAll. HF20 proves the exact conditional Core join and empty-model obstruction, retaining actual global compatibility suppliers.',
    boundary_resolved=['Actual IsMu0, IsEtaT, IsChiPsi and both IsDelta constructions',
        'Full actual HFrame on the prescribed host and weights',
        'Actual KD/DtPack and finer SQ relative determinant laws',
        'Uniform fixed-frame ValLL0 finite generator and literal Base extension',
        'Original same-base canonical ColIn Ok/Pins/IsTw/JetsIn with all finite field requirements',
        'Laws/Law0/Later/TwForms and ordinary all-lattice Hyp/JetsAll on that same base'],
    retained_inputs=[COMMON,BOUND,'Literal Host and integral MUQ data for the general HFrame statement; the original IG10 PreX supplies them in HF18',
        'Coefficient containment for a separately prescribed LL0/LL; HF18 chooses one suitable Base, not every Base',
        'The exact same-object Lay/RecOK/LedOK/MuIsW/metric/real/theta/character/NChoice requirements of coreOfLay',
        'An adequately nonempty arithmetic twist-reading stage with forced prime coverage',
        'Global common theta tests, critical L-value arithmetic, quantitative mass/spectral/window statements where separately required'],
    dependency_precision=['HF1–12 do not assume an HFrame or final column input.',
        'HF13 fixes the actual characters before HF16 chooses their finite value field.',
        'HF18 normalizes and fixes Pre before choosing CA12 jet generators and invoking HF17.',
        'HF18 uses canonical exponent m+1 in the jet generator set, after raw depth 2m and canonical replacement.',
        'HF19 applies TL13/TX10/LS22 to one actual I and one actual B; it has no V4.Core premise.',
        'HF20 retains stronger Core suppliers and proves why the empty untwisted model cannot satisfy forced.',
        'All predecessor components and their claims/source arrays remain immutable.'])

for name,who,nums in [('ar_reviews_host_character_frame.txt','/root/class_rank',range(1,21))]:
    review=HERE.parent/'reviews_v0_19'/name
    if review.exists():
        rb=review.read_bytes();rt=rb.decode();ph={}
        for n in nums:
            h=claims[n-1]['proof_paragraph_sha256']
            assert h in rt,('reviewed paragraph changed',n,h)
            ph[f'HF{n}']=h
        out['independent_reviews'].append(dict(reviewer=who,result='PASS',claim_ids=list(ph),
            review_record='../reviews_v0_19/'+name,review_record_sha256=digest(rb),paragraph_sha256=ph,
            lean_replay=False))

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
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.19',commit=PIN,targets=targets,
    closed_source_targets=closed,
    remaining_boundary='Actual HFrame, determinant/coefficient data and the original same-base canonical columns/jets/laws/Later join are proved. Stronger V4.Core and arithmetic/theta/quantitative suppliers remain exactly identified; empty twisting data cannot satisfy Core.forced.'),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),
    source_ranges=len({(s['path'],s['line_start'],s['line_end']) for c in claims for s in c['sources']}),
    source_files=len(files),record_fields=sum(a['named_field_count'] for a in audits),
    next_targets=len(targets),closed_targets=len(closed),verified_equal_to_pinned_git_blob=True,
    artifact_sha256=out['artifact_sha256'])))
