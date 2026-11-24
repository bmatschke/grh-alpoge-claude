"""Rebuild this component's hash-bound metadata, without editing the root audit."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
SOURCE = WORK.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def human(path, claims=None):
    b = (WORK/path).read_bytes()
    return dict(file=path, sha256=sha(b), bytes=len(b), claims=claims or [])

def src(path, declaration, start, end):
    data = (SOURCE/path).read_bytes()
    blob = subprocess.check_output(['git','show',PIN+':'+path], cwd=SOURCE)
    assert data == blob, path
    ls = data.splitlines(keepends=True)
    b = b''.join(ls[start-1:end])
    assert 1 <= start <= end <= len(ls), (path,start,end,len(ls))
    return dict(path=path, declaration=declaration, line_start=start,
                line_end=end, sha256=sha(data), full_file_sha256=sha(data),
                range_sha256=sha(b), range_bytes=len(b),
                verified_equal_to_pinned_git_blob=True,
                url=BASE+path+f'#L{start}-L{end}')

WB = {x['id']:x for x in json.loads((WORK/'window_bridge/provenance.json').read_text())['claims']}
AQ = {x['id']:x for x in json.loads((WORK/'analytic_envelope/provenance.json').read_text())['claims']}

def inherited(ids):
    result=[]
    seen=set()
    for id_ in ids:
        for s in (WB|AQ)[id_]['sources']:
            key=(s['path'],s['line_start'],s['line_end'])
            if key in seen: continue
            seen.add(key)
            result.append(src(s['path'],s.get('declaration',''),s['line_start'],s['line_end']))
    return result

AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
AB = 'src/Development/AbelianVarietyTheory/'
ad_sources = {
 'endpoint': src(AV+'AutomorphicForms/CongruenceNumberRankThree.lean','IsAdOf; AdVanishK',158,175),
 'attach': src(AV+'AutomorphicForms/BlochKatoSelmerVanishes.lean','FrobEig; algSat; AttachedSys; AttC; IsAutCsd',69,86),
 'bk': src(AV+'AutomorphicForms/BlochKatoSelmerVanishes.lean','decJ; IsBK; BlochKatoSelmerVanishes',117,144),
 'period': src(AV+'PadicHodgeTheory/FiniteCohomology.lean','PP; Bcr; actC; finiteCocycles',78,125),
 'cuspidal': src(AB+'Definitions/AutomorphicMembership/ExpoConjOfIsCsd.lean','IsAutForm; IsCuspidal; IsCuspForm',44,92),
 'cuspsub': src(AB+'Definitions/AutomorphicMembership/ExpoConjOfIsCsd.lean','CuspSub; Iso; HasInfChar',209,279),
 'regular': src(AB+'Definitions/AutomorphicMembership/ExpoConjOfIsCsd.lean','CG.mk; infChar; IsRegAlg; isRegAlg_iff',540,599),
 'capelli': src(AB+'Definitions/AutomorphicMembership/ContinuousConjFin.lean','Eop; cap; cap_highest',109,157),
 'satquot': src(AB+'PublishedTheorems/GaloisCohomology₂/StrongMultiplicityOne.lean','CG.HasSat; hasSat_mk',59,76),
 'sat': src(AB+'Definitions/Foundations/IsSatVecUOfIsSphericalU.lean','satEig; IsSatVecGL; HasSatGL',86,120),
 'pair': src(AB+'Definitions/GaloisGeometry/DualIsConjByOne.lean','Paired; conjOp; DualIsConj; PolarizedPair',31,59),
 'cyc': src(AB+'PublishedTheorems/GaloisCohomology₂/TrivialOnInertiaOfUnr.lean','cycBar',33,34),
 'cycz': src('src/ReciprocityTheory/GaloisValuations/Global.lean','cycZ; cyc_eq_map_cycZ; continuous_cycZ',90,102),
 'host': src(AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/HostNumberS.lean','HostRigidS',12,17),
 'hostlocal': src(AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/EHostRigidU.lean','rig_away; rig_above',85,183),
 'hostfinal': src(AV+'ModularityArgument/ThresholdArguments/DenseThresholdCases/EHostRigidU.lean','hostRigidUE_alt',390,440),
}

(HERE/'main.tex').write_text((HERE/'conditional_main.tex').read_text()+'\n\n'+(HERE/'adjoint_matching.tex').read_text())
main_lines=(HERE/'main.tex').read_text().splitlines(keepends=True)

def claim(id_, title, scope, dependencies, sources, mode, assumptions):
    a=next(i for i,s in enumerate(main_lines,1) if s.strip()==f'% BEGIN {id_}')
    z=next(i for i,s in enumerate(main_lines,1) if s.strip()==f'% END {id_}')
    b=''.join(main_lines[a-1:z]).encode()
    return dict(id=id_,title=title,introduced_in='0.42',
                status='human_implication_complete',mathematical_status=mode,
                scope=scope,depends_on=dependencies,assumptions=assumptions,
                remaining_inputs=[],sources=sources,
                proof_location=dict(file='conditional_main_v42/main.tex',
                    label='claim:'+id_,line_start=a,line_end=z,
                    sha256=sha(b),bytes=len(b)))

claims=[
 claim('CMP1','Primitive values and exact ramified balance',
       'The same onto host reciprocity and actual primitive logarithmic derivatives; no arithmetic producer.',
       ['WB1','WB2'],inherited(['WB1','WB2']),'expository_consolidation',
       ['Compatible finite datum as displayed in CMP.2–CMP.5.']),
 claim('CMP2','Average first and retain the positive target',
       'H <= mean gap/D +(4+4o)x^(1/2+epsilon)+4/(d2*x), with uniform threshold. No pointwise-in-translate gap is used.',
       ['CMP1','WB3','WB4','WB5'],inherited(['WB3','WB4','WB5','WB6']),
       'proved_weaker_sufficient_input',
       ['One compatible finite datum; fixed o, K0, CE, epsilon; all original cutoff, bias, retained and omitted character conditions.']),
 claim('CMP3','Square-root mean-gap comparison',
       'Uniform mean gap <=x^(C epsilon) B implies H<=x^(1/2+(C+4)epsilon); source C=5.',
       ['CMP2','SC1','WB6'],inherited(['WB6','WB7']),
       'expository_consolidation_with_weaker_input',
       ['CMP.6 scalar sizes and mean-gap inequality CMP.9, C>=0 fixed before epsilon.']),
 claim('CMP4','Full positive-integral-window zero exclusion',
       'All constituents nonzero to the right of fixed theta in (0,1), apart from principal pole.',
       ['AN2','AN3','AQ1','AQ2','AQ3'],inherited(['AQ1','AQ2','AQ3']),
       'expository_consolidation',
       ['Fixed positive Dirichlet character family; classical continuation, Euler products, functional equations and nonvanishing on Re(s)=1; CMP.15 for every alpha>0 on arbitrarily late windows.']),
 claim('CMP5','Conditional RH and Dirichlet GRH',
       'Complete implication from exactly the two ordinary-mathematical arithmetic inputs; no unconditional RH claim.',
       ['CMP3','CMP4','WB8','GH6'],inherited(['WB8','AQ4']),
       'expository_consolidation',
       ['Compatible construction and mean-gap estimate on one datum per x; C before epsilon; fixed character family and constants before moving windows.']),
 claim('CMP6','Positive averaged-gap envelope suffices',
       'Measurable E=(mean gap)_+/D+4/(d2*x) with arbitrarily late subpower weighted integrals excludes zeros to right of theta.',
       ['CMP2','CMP4'],inherited(['AQ1','AQ3']),
       'proved_weaker_sufficient_input',
       ['0<epsilon<theta-1/2; compatible data; measurable actual envelope; integral rate for every alpha>0.']),
 claim('ADK1','Finite coefficient capture for representations and cocycles',
       'Continuous profinite representation and each cocycle separately defined over a finite local field.',
       ['NR19','NR20','RX1'],[ad_sources['endpoint']],
       'human_proof_with_inherited_countability_argument',
       ['Usual l-adic topology on Qbar_l; finite-dimensional action; compact profinite source.']),
 claim('ADK2','Exact infinite cyclotomic subgroup',
       'ker cycBar equals G_{K(mu_l^infinity)} as a topological subgroup.',
       [],[ad_sources[x] for x in ['cyc','cycz','endpoint']],
       'human_proof',
       ['Actual source inclusions and compatible cyclotomic character.']),
 claim('ADK3','Literal automorphic and normalized Galois dictionary',
       'Source CuspSub/CG, regular Capelli parameters, normalized Satake and bilinear conjugate duality give BLGGT pair; actual r is attached r_pi,iota.',
       ['ADK1','ADK2'],[ad_sources[x] for x in ['attach','cuspidal','cuspsub','regular','capelli','satquot','sat','pair']],
       'checked_published_theorem_application',
       ['BLGGT Theorem 2.1.1 and standard admissible cusp realization/Harish-Chandra character dictionary; Chebotarev density; semisimple characteristic-zero character criterion.']),
 claim('ADK4','Equality of the full polarized adjoint',
       'Original arbitrary IsAdOf action equals unitary adjoint on all M_n, including negative scalar line; not trace-free.',
       ['ADK2','ADK3'],[ad_sources['endpoint']],
       'human_proof',
       ['Irreducibility on full infinite cyclotomic kernel; same complex conjugation and multiplier epsilon^(1-n).']),
 claim('ADK5','Exact local Selmer and coefficient comparison',
       'Literal IsBK local conditions match H_f^1 including graph topology, finite primitive descent and diagonal Bcris action.',
       ['ADK1','ADK4','BX1'],[ad_sources[x] for x in ['bk','period']],
       'human_proof_using_inherited_period_identification',
       ['Inherited BX1 identification of the original tied period model with standard equivariant Bcris.']),
 claim('ADK6','Full original AdVanishK',
       'All original ranks n>=2, every prime, every continuous IsAutCsd r irreducible on full cyclotomic kernel, every original full IsAdOf action; every source BK cocycle is a coboundary.',
       ['ADK1','ADK2','ADK3','ADK4','ADK5'],[ad_sources[x] for x in ['endpoint','attach','bk','period']],
       'whole_leaf_published_matching_discharge',
       ['Thorne 2022 Theorem 6.1 applied with F=K, F+=Q, same n, prime and iota; no residual, ordinary, split-place or prime-exclusion hypothesis.']),
]

records=json.loads((WORK/'dependency_audit_v0_41/remaining_leaf_register.json').read_text())['records']
leafmap=[]
for r in records:
    role='gap' if r['id'].startswith('GLOBAL_') else 'compatible_construction'
    if r['id'] in ['DESIGN_CHOICES_COMMON','LOCAL_NBUILT_COMMON','SECOND_LAYER_COMPATIBLE_SELECTION','BASE_THETA_READINGS','BASE_THETA_RATIONAL_TESTS','SLR_BASE_ROWS_PRODUCER']:
        role='common_geometric_construction'
    status='discharged_by_ADK6_pending_root_integration' if r['id']=='AD_VANISH_K_MATCH' else 'unchanged_open_in_this_packet'
    leafmap.append(dict(id=r['id'],title=r['title'],category=r['category'],
                        original_contract=r['contract'],role_in_main_proof=role,
                        packet_status=status))

primary=[
 dict(id='THORNE2022',author='Jack A. Thorne',
      title='On the vanishing of adjoint Bloch–Kato Selmer groups of irreducible automorphic Galois representations',
      publication='Pure and Applied Mathematics Quarterly 18 (2022), no. 5, starting p. 2159',
      doi='10.4310/pamq.2022.v18.n5.a5',
      version='arXiv:2207.04925v1 (accepted version, 11 July 2022)',
      url='https://arxiv.org/html/2207.04925v1',pdf='https://arxiv.org/pdf/2207.04925',
      theorem='Theorem 6.1, printed p. 24; full adjoint specified in introduction and notation, printed pp. 3–4',
      normalized_statement='For a CM field F, n>=2, a regular algebraic cuspidal polarized pair (pi,chi), any prime p and iota:Qbar_p≃C, irreducibility of r_pi,iota restricted to G_{F(mu_p^infinity)} implies H_f^1(F+,ad r_pi,iota)=0.',
      scope_checks=['all n>=2','any prime','same iota','characteristic-zero irreducibility on full infinite cyclotomic subgroup','full Lie(GL_n)=M_n','unitary negative-transpose conjugation action','usual finite local conditions','no extra residual image hypothesis']),
 dict(id='BLGGT2014',authors=['T. Barnet-Lamb','T. Gee','D. Geraghty','R. Taylor'],
      title='Potential automorphy and change of weight',publication='Annals of Mathematics 179 (2014), 501–609',
      url='https://annals.math.princeton.edu/wp-content/uploads/annals-v179-n2-p03-p.pdf',
      theorem='Theorem 2.1.1, p. 538; pairing/sign convention p. 535; group G_n pp. 512–513',
      application='Pair (pi,delta_K^n); norm pullback trivial, infinity sign (-1)^n; Galois multiplier delta_K^n epsilon^(1-n), value -1 on c; total oddness gives symmetric pairing; geometric Frobenius eigenvalues q^((n-1)/2) alpha.'),
]

humans=[human('window_bridge/main.tex',['WB1','WB2','WB3','WB4','WB5','WB6','WB7','WB8']),
        human('analytic_envelope/analytic_envelope.tex',['AQ1','AQ2','AQ3','AQ4','AQ5']),
        human('RH_readable_reconstruction_v0_41.tex',['AN2','AN3','SC1']),
        human('nonempty_realization/main.tex',['NR19','NR20']),
        human('symplectic_actual_rigidity/main.tex',['RX1','RX5']),
        human('bloch_kato_installation/main.tex',['BX1'])]

prov=dict(schema='rh-human-reconstruction-component/2',artifact_version='0.42',
          component='conditional_main_v42',repository='https://github.com/CocoSgt/riemann-hypothesis-lean',
          commit=PIN,scope='Conditional terminal main proof, smaller sufficient mean-gap input, and exact full AdVanishK published matching. HOST_RIGID_S remains open in this packet.',
          claims=claims,proof_sha256=sha((HERE/'main.tex').read_bytes()),
          inherited_human_proofs=humans,published_sources=primary,
          validation=dict(source_pin_verified=True,source_ranges_byte_checked=True,
                          source_assumption_audit='No new formal replay or dependency audit claimed.',
                          tex_compile='Attempt blocked: installed pdflatex executable has no pdflatex.fmt; mathematical and source review completed, no rendered-PDF claim.',
                          parent_review='Root reviewed ADK1–ADK6 after the exact automorphic/local dictionary; independent global agent reviewed same and CMP2/CMP6, with two small edits incorporated. Final review is hash-bound separately.'))

contracts=dict(schema='rh-conditional-main-and-adjoint-contracts-v1',artifact_version='0.42',source_commit=PIN,
               proof_sha256=prov['proof_sha256'],claims=claims,
               major_inputs=[
                 dict(id='CMP_INPUT_I',status='open',name='Compatible common finite construction',
                      scope='One datum satisfying CMP.2–CMP.6 at every real x of arbitrarily late windows for each fixed target and small epsilon; all primitive readings and Lprime/L values are exact.'),
                 dict(id='CMP_INPUT_II',status='open',name='Uniform mean-gap inequality on that construction',
                      scope='Same objects; meanGamma<=x^(C epsilon)B with C fixed before epsilon. Pointwise original translate bounds remain sufficient. CMP6 gives a weaker measurable positive-integral alternative.')],
               quantifier_order='forall primitive psi, exists C>=0,epsilon0>0, forall 0<epsilon<epsilon0, exists K0,CE and fixed construction constants, forall Y0, exists Y>=max(3,Y0), forall real x in [Y,Y^(3/2)], exists one common datum satisfying both inputs.',
               baseline_leaf_mapping=leafmap,adjoint_source_dictionary=ad_sources,
               published_application_certificate=primary,
               host_rigidity=dict(status='open',exact_endpoint=ad_sources['host'],
                     concrete_source_proof=[ad_sources['hostlocal'],ad_sources['hostfinal']],
                     next_task='Write actual rig_sub, rig_eig, rig_loc with finite-coefficient crystalline-extension/descent and the exact twist/disconnected pairing, then same quotient descent.'),
               progress_accounting=dict(new_whole_leaf_discharge='AD_VANISH_K_MATCH via ADK6, subject to root integration',
                    inherited_exposition=['CMP1','CMP3','CMP4','CMP5'],
                    new_sufficient_weakening=['CMP2','CMP6'],
                    published_matching=['ADK1','ADK2','ADK3','ADK4','ADK5','ADK6'],
                    no_full_RH_claim=True))

for name,obj in [('provenance.json',prov),('contracts.json',contracts)]:
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

report='''CONDITIONAL MAIN PROOF AND ADJOINT MATCHING, v0.42

Completed files: main.tex (combined fragment), conditional_main.tex (CMP1–6),
adjoint_matching.tex (ADK1–6), provenance.json, contracts.json.

MATHEMATICS
* CMP1–5 consolidate the complete end-to-end conditional terminal argument in
  ordinary notation: actual primitive readings including ramified primes;
  exact centered ramp identity; cutoffs and subgroup/Fourier averaging;
  scalar square-root bound; full one-sided pole argument and functional equations.
* Exactly two open major arithmetic inputs are stated with the same objects
  and complete quantifier order: a compatible common construction, and its
  uniform upper mean-gap inequality. All 33 v0.41 leaves are mapped, and the
  exact baseline contracts are preserved in JSON.
* CMP2 proves the source only needs an upper bound on the average of its
  translate gaps, not a separate bound for every translate. CMP6 combines
  this with the positive-integral criterion. These are weaker sufficient
  inputs, not new suppliers of the arithmetic construction.
* ADK1–6 give a checked application of Thorne 2022 Theorem 6.1 to the full
  original AdVanishK. Includes all n>=2 and every prime; source normalized
  Satake/Capelli and bilinear conjugate-duality dictionary; finite coefficient
  fields; actual infinite cyclotomic subgroup; full M_n and negative transpose;
  same pairing by Schur; graph topology; inertia and Bcris local conditions;
  and coefficient retractions commuting with the diagonal period action.
* Proposed whole-leaf closure: AD_VANISH_K_MATCH. HOST_RIGID_S remains open
  here, with its actual source local proof located. No other leaf is closed.

VALIDATION
All source ranges in provenance/contract files were byte-compared against the
pinned git blob. The pin is 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4.
Primary published sources are the accepted Thorne arXiv v1 and the official
Annals BLGGT PDF. Root and independent global-agent mathematical review passed;
the requested maximal-parabolic dictionary and spacing edits are incorporated.
Attempted standalone LaTeX compilation is blocked because the installed
pdflatex has no pdflatex.fmt; no rendered PDF validation is claimed.

NEXT
Proceed in host_rigidity_v42 to the literal ordinary tangent rig_sub/rig_eig/
rig_loc and finite coefficient crystalline-extension/descent proof, with the
same cyclotomic twist and disconnected pairing. Keep every genuine remaining
producer open. Root owns ledger integration and final saving.
'''
(HERE/'report.txt').write_text(report)
checks={name:sha((HERE/name).read_bytes()) for name in ['main.tex','conditional_main.tex','adjoint_matching.tex','provenance.json','contracts.json','report.txt']}
(HERE/'hashes.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
