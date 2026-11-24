#!/usr/bin/env python3
"""Reproduce the VI source ledger from immutable Lean bytes, without a build.

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
S = D + 'Proofs/SatakeParameters/'
P = D + 'Proofs/FoundationProofs/'
V = D + 'Proofs/DivisorProofs/'
F = 'src/Formalism/LocalToGlobal/'
K = F + 'KernelLattices/'
Q = F + 'TorsionIntegrality/QuadraticSemicharacters/'
G = Q + 'CayleyGaussianIntegrals/'
GL = F + 'GlobalTheory/GL3/'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


decl_re = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe)\s+)*'
                     r'(theorem|lemma|def|abbrev|structure|class|inductive)\s+([^\s:({]+)')
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

def whole_decls(path, role='substantive_local_proof_and_definitions'):
    """Link each declaration separately; never hash a reconstructed source."""
    _, _, decls = read_source(path)
    return [source(path, d['qualified'], role) for d in decls]

common = [
 'The literal D, curve ideal cc, discriminant root delta and actual Base(D,cc,delta) with Crv are supplied. No period, half-point, isometry or KapChoice is replaced.',
 'The arithmetic host includes its actual trace-self-dual fractional ideal AA0; the argument uses that identity rather than constructing a new arithmetic host.',
 'Prior PA/TA assertions supply the named one-variable analytic and CM background. No continuity of an arbitrary field embedding is assumed.',
 'Every claimed finite sum/product is proved to have finite support or a finite indexing quotient on the actual data; positive square roots and exact Heisenberg phases are retained.',
 'No Lean compilation, kernel replay, replacement formalization, PDF, RH or GRH proof is asserted.'
]

main_raw=(HERE/'main.tex').read_bytes()
paragraphs={}
for i in range(1,12):
    start=main_raw.index(f'\\paragraph{{VI{i}:'.encode())
    stop=main_raw.index(f'\\paragraph{{VI{i+1}:'.encode(),start+1) if i<11 else len(main_raw)
    paragraphs[f'VI{i}']=digest(main_raw[start:stop])

def claim(i,title,statement,deps,srcs,relation,assumptions=()):
    return dict(id=i,title=title,status='derived_simplification',statement=statement,
        introduced_in='0.17',depends_on=deps,assumptions=common+list(assumptions),
        proof_location=dict(file='main.tex',anchors=[i],sha256=paragraphs[i]),
        expanded_notes=dict(file='report.txt',section=i),
        source_relation=relation,
        mathematical_status='proved_under_exact_declared_supplied_data_hypotheses',
        sources=srcs)

lat=K+'LateralTheory.lean'
span=S+'SpanRangeEmb4EqTop.lean'
vac=I+'VacuumEntireAndNormalizedJetsAlgebraic.lean'
ex=I+'ExistsWeilOThZeroTriv.lean'
kl=K+'KernelLocalFactors/IsAdmissibleFlagPairOfUnitriangularLeftAutomorph.lean'
mat=G+'MatrixFormFourfoldBlock.lean'
root=G+'MatrixFormFourfoldBlockFirstBlockEmb.lean'
line=G+'LogarithmEquivalence.lean'
prod=Q+'ProductThetaMem.lean'
semi=Q+'IsSemiChar.lean'
local=G+'LocalComponentGL.lean'
std=G+'Th0CharMulOpUTh0HalfPeriodEq.lean'
gen=P+'ThetaTaylorCoeffsAlgebraicAtComplexMultiplicatio.lean'
ind=V+'CosetIndicatorThetaTorsionTranslates.lean'

claims=[
 claim('VI1','Same arithmetic lattice, complex map and finite correction',
  'Identify lamM with delta*emb(cc*AA0); identify the supplied gC with its actual algebraic isometric extension; prove both denominator inclusions and genuine finite support and nonvanishing of the actual kappa.',
  ['PA1','PA4','PA10'],
  ss(lat,'Base lamMM lamM KapChoice KapChoice.yP KapChoice.kappa')+
  ss(span,'span_range_emb4_eq_top isomOK up down idx₁ idx₂')+
  ss(ex,'kappa_ne_zero'),
  'Uses exact algebraic subgroup generation, spanning-set uniqueness, and PA denominator/support proofs; does not infer support from totalized finprod.'),
 claim('VI2','Actual period lattice duality and rounded multiplier',
  'Prove full self-duality and commensurability of every admitted La by integral Hom and trace/codifferent duality, then prove q integral and identify the rounded source multiplier with the sign semicharacter.',
  ['VI1','PA1'],
  ss(GL+'PSelfDual.lean','mm_unimod hom_step alg_step coord SelfDualRec_of_curve curve_lattice_self_dual self_dual_lattice')+
  ss(GL+'PHfInt.lean','hermitian_pairing_integral arithmetic_hermitian_form')+
  ss(lat,'LatOK LatAll QIntAll')+
  ss(root,'quadMultiplierSemicharacter quadMultiplierRules')+
  ss(span,'selfDual_La selfDual betaSemi'),
  'Replaces the even 2-by-2 reindex route with an explicit integral Hom trace-dual calculation, valid also in the one-copy case; no integral orthonormal basis is assumed.'),
 claim('VI3','Distinguished half-point parity and actual StdOK',
  'Use the actual three unkilled clauses to prove equality of the quadratic and standard characters and verify all ten literal StdData fields for the supplied Base.',
  ['VI1','VI2'],
  ss(GL+'PStdChar.lean','gen q_odd char_eq stdChar_eq')+
  ss(prod,'StdData')+
  ss(span,'stdOK_of betaStd stdOK stdOK_of_crv'),
  'Explicit two-dimensional mod-2 alternating calculation supplies betaStd; same-map isometry supplies betaAlpha on all four-block vectors.'),
 claim('VI4','Heisenberg product and exact finite intertwiner',
  'Prove the minus-pi Heisenberg product phase and commutator, then construct representative-independent finite inter and its exact theta transport with positive index normalization.',
  ['VI2'],
  ss(semi,'opU IsSemiChar fixedBy inter')+
  ss(mat,'heisenbergMul heisenbergComm semicharacterHom heisenbergAnalytic')+
  ss(local,'InterClass_of cosetRepsExist InterReps_of InterFixed_of InterTh_of'),
  'Direct exponential expansion and quotient permutation; finsum is converted only after finiteness has been proved.'),
 claim('VI5','Finite Fourier inverse and literal normalized Iop norm',
  'Prove equality of both relative indices, exact positive-normalized inverse, nonvanishing and line transport, and the literal normSq/IopIso equality by Gaussian-weighted torus orthogonality.',
  ['VI2','VI4'],
  ss(Q+'LineTransport.lean','IndexEq CharSum InterInv LineTransport')+
  ss(line,'characterSum IndexEq_of InterInv_of LineTransport_of')+
  ss(mat,'heisenbergNorm')+
  ss(GL+'PIopNorm.lean','avg_sub int_zero_of_char intOn_of_full normSq_eq iso_core IopIso_of_parts')+
  ss(GL+'PLinkThIndep.lean','IopIso'),
  'Proves the exact normalization rather than an unspecified Fourier scalar; normalized finite-cover averages coincide with the source chosen fundamental-domain average.'),
 claim('VI6','Actual normalized standard theta line',
  'Identify the same normalized even theta and prove its one-variable line by the single-simple-pole residue argument, then obtain the full product line by successive coordinate slices.',
  ['VI3','TA14','TA12','PA15'],
  ss(std,'th0Char_mul_opU_th0_half_period_eq product_theta_mem th_split ThStd_proof')+
  ss(prod,'F0 ProductThetaMem ThStd')+
  ss(vac,'thetaZero_periodLattice_eq'),
  'The short elliptic quotient argument supplies the actual line theorem, with its value at zero and chosen half-point normalization; no vacuum predicate is assumed.'),
 claim('VI7','Nonzero four-copy construction and the chosen thMM',
  'Construct a nonzero four-copy generator by finite transport, slice it, take a fourth root of one nonzero complex scalar, and prove the literal thMM_spec, nonvanishing, spanning and fourth-root-of-unity uniqueness.',
  ['VI1','VI3','VI4','VI5','VI6'],
  ss(prod,'kernel4 FourthRoot ThetaVector')+
  ss(root,'restrict_mem fourfoldTensorMem FourthRoot_of ThetaVector_of')+
  ss(lat,'IsThM thM IsThMM thMM')+
  ss(ex,'thMM_spec')+
  ss(kl,'thM_spec isThM_ne_zero isThM_spans Base.thMM_spec Base.thMM_ne_zero'),
  'Genuine existence precedes the epsilon specification; no pointwise analytic fourth-root branch and no algebraicity assertion for the slicing scalar are used.'),
 claim('VI8','Actual four-copy algebraic germ',
  'Prove Root4 for the same chosen thMM by a finite sum of rational-period one-variable translates after the actual algebraic gC coordinate forms.',
  ['VI1','VI7','TA10','PA15'],
  ss(vac,'AV Root4 alg_of_span kappa_mem heisenbergOp_standardVacuum_prod thetaVector_fourthPower_algebraicGerm')+
  ss(gen,'Gen Gen.contDiff Gen.iterated_mem Gen.sum Gen.prod')+
  ss(mat,'heisenbergStandard'),
  'Uses the genuine finite quotient and actual algebraic matrix; every coefficient and linear direction is checked before invoking the Gen constructors.'),
 claim('VI9','All rational translates of the actual vacuum',
  'Apply a four-block rational Heisenberg translate to the exact identity; its phases are roots of unity, so every translated vacuum has Root4 and algebraic derivatives including at zeros.',
  ['VI2','VI4','VI8','TA10','PA15','TL18'],
  ss(mat,'heisenbergMul precompHeisenberg heisenbergFourfold')+
  ss(kl,'opU_tensPow')+
  ss(vac,'Root4.val_mem Root4.deriv TA TA.transl')+
  ss(gen,'Gen.deriv Gen.iterated_mem Gen.coefIn'),
  'A direct strengthening for this actual vacuum replaces the broader arbitrary-theta CoefInTranslate premise; no division by a possibly zero value is made.'),
 claim('VI10','Rectangular and actual moved algebraic vacua',
  'Prove the exact product period lattice and thZero formula, nonvanishing/spanning including zero rank, all rational translated coefficients, and actual ta_thMoved from its two finite moving operators.',
  ['VI2','VI4','VI5','VI7','VI9'],
  ss(lat,'tensPow powLat thZero thHalf thMoved')+
  ss(ex,'entry_mem Hf_eq thZero_mem thZero_ne_zero')+
  ss(kl,'tensPow_mem thMoved_mem thMoved_ne_zero')+
  ss(vac,'thZero_coefIn TA.comb la_le_sat TA.iop ta_thMoved'),
  'Keeps exact integral product equality and positive finite normalization; rational commutator phases are algebraic after clearing integer denominators.'),
 claim('VI11','Same-ambient smoothness and normalized indicator jets',
  'Use the independently proved actual finite indicator presentation to obtain every normalized jet and all-order smoothness for the exact ambOf seam/character/base, with the original quantifier order.',
  ['VI10','CA2','TL18'],
  ss(ind,'pres_thInd','independent_CA2_finite_presentation_interface')+
  ss(vac,'derivAt0_mul esmooth_jetAlg')+
  ss(V+'DerivAtZeroReindexEqTaylorCoefficient.lean','derivAt0_reindex'),
  'CA2 is independent of algebraic jets; the seam is a 0-1 reindex and only explicit factorials enter. No algebraicity of the unnormalized chiF is assumed.',
  ['The literal X.Ok, seam.Ok, Crv, IsChi and even source ranks hold on these same ambient data.'])
]

# No new unresolved primitive vacuum supplier remains in this component.
# Imported, unused general adelic Weil and arbitrary-theta translation
# statements are deliberately not promoted to new prerequisites.
targets=[]
closed_specs=[
 (span,'stdOK',['VI1','VI2','VI3']),
 (span,'stdOK_of_crv',['VI1','VI2','VI3']),
 (ex,'thMM_spec',['VI7']),
 (kl,'Base.thMM_spec',['VI7']),
 (vac,'thetaVector_fourthPower_algebraicGerm',['VI8']),
 (vac,'thZero_coefIn',['VI9','VI10']),
 (vac,'ta_thMoved',['VI9','VI10']),
 (vac,'esmooth_jetAlg',['VI11']),
 (GL+'PThIndep.lean','theta_operator_isometry',['VI2','VI5']),
]
closed=[]
for path,name,ids in closed_specs:
    s=source(path,name,'literal_completed_source_target')
    closed.append(dict(path=path,declaration=s['declaration'],closed_by=ids,source=s,
      scope='Human reconstruction on the supplied D/Base/Crv. VI11 additionally uses independent CA2 and its exact ambient hypotheses.'))

record_source=source(prod,'StdData','literal_ten_field_record_audit')
record_lines=read_source(prod)[1][record_source['line_start']-1:record_source['line_end']]
record_fields=[]
for line_text in record_lines[1:]:
    m=re.match(r'^  ([^\s:]+)\s*:',line_text)
    if m:record_fields.append(m.group(1))
assert record_fields==['per','half','isom','alpha0','betaStd','betaSemi','betaAlpha','selfDual','idx₁','idx₂'],record_fields
record_audit=dict(record=record_source['declaration'],source=record_source,field_count=len(record_fields),
 fields=[dict(name=name,supplied_by='VI3',support=('VI1' if name in ['isom','idx₁','idx₂'] else 'VI2' if name in ['betaSemi','selfDual'] else 'VI3')) for name in record_fields])

out=dict(schema_version='1.3',artifact_version='0.17',date='2026-11-21',
 component='vacuum_identity',owner='/root/comparison_span',repository=dict(url=URL,commit=PIN),
 range_convention='One-indexed inclusive; exact original declaration bytes with no newline or Unicode normalization.',
 verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,range_bytes_hashed_without_normalization=True,
  missing_sparse_files_read_from_pinned_git_blob=True,human_mathematical_proofs_supplied=True,
  lean_source_files_edited=False,local_lean_compilation=False,lean_kernel_replay=False,
  replacement_arguments_formalized=False,pdf_build_or_render=False),
 status_definitions=dict(derived_simplification='Human proof under the exact declared supplied data; some source arguments are replaced by explicitly explained shorter proofs.'),
 claims=claims,files=[files[p] for p in sorted(files)],
 artifact_sha256={p:digest((HERE/p).read_bytes()) for p in ['main.tex','report.txt','build_provenance.py']},
 paragraph_sha256=paragraphs,record_audits=[record_audit],
 prior_components_reused=['PA','TA','TL'],same_iteration_companions=['CA2'],
 independent_reviews=[],retained_inputs=common,
 boundary_resolved=[
  'Actual StdOK and all ten StdData fields',
  'Full admitted period-lattice self-duality, semicharacter and finite commensurability',
  'Positive finite Fourier inverse, line transport and literal IopIso',
  'Actual chosen nonzero thMM with exact kappa four-copy identity',
  'Actual fourth-power algebraic germ',
  'Rational-translate coefficients for actual thMM, rectangular thZero and moved thMoved',
  'Exact ESmooth/JetAlg from independent CA2'],
 scope_precision=[
  'Base, Crv, arithmetic host and trace-self-dual AA0 remain supplied; no new host construction is claimed.',
  'VI1 uses the actual gC_spec, and every finite determinant correction uses the actual KapChoice roots.',
  'A scalar fourth root used in existence is not assumed algebraic over Q; coefficient algebraicity is established afterwards from the four-copy identity.',
  'VI9 avoids the broader arbitrary-theta CoefInTranslate assertion; only the actual vacuum and its required translates are claimed.',
  'VI1-VI10 are independent of CA. Only independent CA2 enters VI11; no FinAlg/EvLg cycle.',
  'An integral Hom trace-dual computation is used; neither rank equality nor an integral orthonormal basis is substituted.',
  'The positive real index square root and the exact negative Heisenberg phase are retained.',
  'No unnormalized chiF algebraicity, arbitrary-embedding continuity, global conjugate-norm bounds, full adelic Weil model or RH/GRH conclusion is asserted.'])

review_specs=[
 ('root_reviews_vi.txt','/root',list(range(1,12)),'Independent full vacuum/germ and exact-scope review.'),
 ('ca_reviews_vi_2_7.txt','/root/global_frame',list(range(2,8)),'Independent integral lattice, semicharacter, Fourier normalization and vacuum-line construction review.')
]
for filename,reviewer,indices,scope in review_specs:
    p=HERE.parent/'reviews_v0_17'/filename
    if not p.exists():continue
    raw=p.read_bytes();content=raw.decode()
    chosen={f'VI{i}':paragraphs[f'VI{i}'] for i in indices}
    for key,sha in chosen.items():assert sha in content,('review paragraph changed',filename,key,sha)
    out['independent_reviews'].append(dict(reviewer=reviewer,result='PASS',claim_ids=list(chosen),scope=scope,
      review_record='../reviews_v0_17/'+filename,review_record_sha256=digest(raw),paragraph_sha256=chosen,
      paragraph_range='Bytes from named VI paragraph through immediately before the next VI paragraph; EOF for VI11.',
      lean_replay=False))

(HERE/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_manifest.json').write_text(json.dumps(dict(commit=PIN,files=out['files']),ensure_ascii=False,indent=2)+'\n')
loc=[]
for c in claims:
    loc += [f"{c['id']} | {c['title']} | {c['status']}",c['statement'],
            f"  proof_paragraph_sha256: {paragraphs[c['id']]}"]
    for s in c['sources']:
        loc += [f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}",
            f"  role: {s['role']}",f"  file_sha256: {s['sha256']}",f"  range_sha256: {s['range_sha256']}",f"  {s['url']}"]
    loc += ['']
(HERE/'source_locators.txt').write_text('\n'.join(loc)+'\n')
(HERE/'next_targets.json').write_text(json.dumps(dict(version='0.17',commit=PIN,targets=targets,
    closed_source_targets=closed,retained_inputs=common,
    remaining_boundary='No independent primitive vacuum supplier remains on supplied Base/Crv. CA2 supplies the same-round finite indicator interface. Broader arbitrary-theta transport and full adelic Weil/global conjugate norm theorems are not claimed or needed by VI.'),
    ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims),source_links=sum(len(c['sources']) for c in claims),source_files=len(files),
 next_targets=len(targets),completed_source_targets=len(closed),verified_equal_to_pinned_git_blob=True,
 independent_reviewed_claims=[i for r in out['independent_reviews'] for i in r['claim_ids']])))

