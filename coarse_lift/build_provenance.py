"""Rebuild exact source provenance for v0.7 coarse-generator lifting.

Every cited source file is compared byte-for-byte with the pinned Git blob.
No Lean source is edited, and no compilation or kernel replay is performed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

WORK = Path('/workspace/scratch/b992d67d27b8')
ROOT = WORK/'alpoge-rh'
OUT = WORK/'v0_7/coarse_lift'
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == COMMIT
files = {}
cache = {}
DECL = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class)\s+(\S+)')
TOP = re.compile(r'^(?:(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance|set_option|local)\b|@\[)')


def source(path):
    if path not in cache:
        data = (ROOT/path).read_bytes()
        pinned = subprocess.check_output(['git', 'show', COMMIT+':'+path], cwd=ROOT)
        assert data == pinned, ('source differs from pinned commit', path)
        lines = data.decode('utf-8').splitlines(keepends=True)
        cache[path] = (data, lines)
        files[path] = dict(path=path, sha256=hashlib.sha256(data).hexdigest(),
                           bytes=len(data), line_count=len(lines),
                           verified_equal_to_pinned_git_blob=True,
                           url=f'{REPO}/blob/{COMMIT}/{path}')
    return cache[path]


def namespace_at(lines, first):
    stack=[]
    for line in lines[:first-1]:
        ns=re.match(r'^namespace\s+(\S+)', line)
        sec=re.match(r'^(?:noncomputable\s+)?section(?:\s|$)', line)
        end=re.match(r'^end(?:\s|$)', line)
        if ns:
            stack.append(('namespace',ns.group(1)))
        elif sec:
            stack.append(('section',''))
        elif end:
            assert stack, ('unmatched end',first,line)
            stack.pop()
    ns='.'.join(v for kind,v in stack if kind=='namespace')
    return ns+'.' if ns else ''


def reference(path, name, role='proof'):
    data,lines=source(path)
    pat=re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class)\s+'
                   +re.escape(name)+r'(?=[\s{(:])')
    hits=[i for i,l in enumerate(lines) if pat.match(l)]
    assert len(hits)==1,(path,name,hits)
    first=hits[0]+1
    last=next((i for i in range(first,len(lines)) if TOP.match(lines[i])),len(lines))
    while last>first and not lines[last-1].strip():
        last-=1
    qualified=name.removeprefix('_root_.') if name.startswith('_root_.') else namespace_at(lines,first)+name
    excerpt=''.join(lines[first-1:last]).encode('utf-8')
    return dict(path=path,declaration=qualified,line_start=first,line_end=last,role=role,
                sha256=files[path]['sha256'],excerpt_sha256=hashlib.sha256(excerpt).hexdigest(),
                url=f'{REPO}/blob/{COMMIT}/{path}#L{first}-L{last}')


def gb(file,name,role='proof'):
    return reference(GB+file+'.lean',name,role)


def sd(file,name,role='proof'):
    return gb('SegmentDegree/'+file,name,role)


def all_declarations(file,role='proof'):
    path=GB+file+'.lean'
    _,lines=source(path)
    names=[]
    for line in lines:
        hit=DECL.match(line)
        if hit:
            names.append(re.split(r'[{(:]',hit.group(1))[0])
    assert len(names)==len(set(names)),('duplicate short declaration name',file)
    return [reference(path,name,role) for name in names]


def sda(file,role='proof'):
    return all_declarations('SegmentDegree/'+file,role)


claims=[]
def claim(cid,title,statement,status,sources,sections,dependencies=(),assumptions=(),note=''):
    assert status in {'faithful_translation','derived_simplification','remaining_input'}
    claims.append(dict(id=cid,title=title,statement=statement,status=status,
                       depends_on=list(dependencies),assumptions=list(assumptions),
                       proof_location=dict(file='coarse_lift_section.tex',anchors=[cid]),
                       expanded_notes=dict(file='report.txt',sections=list(sections)),
                       source_relation=note,sources=sources))


claim('CG1','Actual paired-path basis, saturation, and reduction of XX′',
      'For any domain R, the source XX′ is the span of exactly the integral paired Psi basis indexed by segPairs. The normal-order projector keeps or kills each whole paired multidegree block. Therefore XX′ over O is saturated, its reduction is XX′ over the residue field, and total-letter-degree projection preserves it. This proves the first, third and sixth NestedTypeBound clauses used in the lift and RestLam.',
      'derived_simplification',
      [gb('SegRing',"XX'",'definition'),
       gb('SegRing','ordDeg','definition'),
       gb('ValuationLowestDegreeRename','segN','definition'),
       gb('ValuationLowestDegreeRename','segE','definition'),
       gb('ValuationLowestDegreeRename','segLL','definition'),
       gb('ValuationLowestDegreeRename','segRen','definition'),
       gb('ValuationLowestDegreeRename','segPairsAll','definition'),
       gb('ValuationLowestDegreeRename','segPairs','definition'),
       gb('ValuationLowestDegreeRename','NestedTypeBound','larger_source_package'),
       gb('ValuationLowestDegreeRename','space_criterion_clause','reverse_inclusion'),
       gb('StatementOfDegreeAndBound','A3at','previous_IP_interface'),
       gb('StatementOfDegreeAndBound','DefiniteRankOne','previous_IP_interface'),
       gb('StatementOfDegreeAndBound','Saturated','definition'),
       gb('StatementOfDegreeAndBound','XXZ','definition')]
      +[gb('ValuationLowestDegreeMapFractionField',n) for n in
        ['seg_val','mem_span_standard_of_bounds','standard_polynomial_mem_bounds',
         'crit_alt','word_ord','ord_proj','crit_words','first_clause_segment_rename',
         'li_allDeg','li_ext','space_statement_linear_independent',
         'sat_li','sat_words_top','space_statement_saturated',
         'Psi_map','PsiPl_map','PsiTan_map','XXZ_lift','space_statement_sixth_clause']],
      [1],dependencies=['IP3','IP4'],
      assumptions=['The previously reconstructed universal integral signed-path basis and exact simultaneous prefix filtration adaptation, IP3–IP4.',
                   'The source hypotheses valid frame, segN+r<=K and nonnegative integer margins are retained in application. The basis argument itself works without the latter two restrictions.'],
      note='Direct proof of the needed three clauses from the common integral basis. The larger package fourth clause, a characteristic-zero joint-isotypic characterization, is neither assumed nor claimed here. Companion LA may use the actual saturation consequence.')


claim('CG2','Literal coarse objects and Euclidean splitting of the coarse label',
      'The source coarse generator and segment modules are preserved exactly. Unique late representatives modulo the period give ell=ell0+p^dist e, with fine label ell0 and every local exponent e<P_j. This yields the exact product identity for monomials. It needs no injection on an entire overlapping segment.',
      'faithful_translation',
      [gb('SegRing',n,'definition') for n in ['Frames','letters','IsW','LLset','dist','Valid','phSeg','IsLabel','Gen']]
      +[sd('Coarse',n,'definition') for n in
        ['toLate','row','detPl','DlSeg','Dl','Et',"a'",'Rj','Qc','m0','phc','IsCLabel','resSet',
         'segDegSet','Bw','thc','oc','Mj','lamGen']]
      +[sd('DiscriminantNeZeroOfResidueNeZero',n,'definition_or_transport') for n in
        ['zSeg','IsEll','CoarseLabelFactorisation','phc_eq']]
      +sda('CoarseLabelFactorisation'),
      [0,2],assumptions=['Literal Dat.Hyp, defined in CG9 source references; all source natural-number subtractions and cutoffs are retained.'],
      note='The terminal-frame exponent restriction in Mj remains in the definition but is not used by the congruence proof. Variables outside TT remain in ell0; the required final zero degrees outside TT are supplied by the actual homogeneous-generator condition.')


claim('CG3','Determinant degree loss and exact coarse power scale',
      'Every residue occurs at most twice in all segment letter sets, and each weighted determinant-row contribution is <=2a/(k²Y), giving E_t<=4Ns*a/(k²Y). The actual numerical hypotheses imply E_t<=a/40, E0<=a/32, a′>=0.9deg on TT and E<=d everywhere. With P_j=p^R_j, T_j>=4p(E0+mStar+1), P_j<=T_j<pP_j, P_j>mStar, and 8Yk²Ns*p^dist*P_j<=a.',
      'faithful_translation',
      [sd('NonemptyDvrSettingOfStandard',n,'definition') for n in
        ['k','La','Bo','sg','mg','th','o','d']]
      +sda('TopOccursInAtMostTwoSegments')
      +sda('TopCountLowerBoundsOfOccurrence')
      +[sd('ReflectionMemGlevCastSucc',n) for n in
        ['frame_zero_le','reflection_mem_Glev_castSucc','mem_letters_bounds','Basics','basics',
         'Tj','den_pos','Tj_ge','pow_Rj_le','lt_pow_Rj','power_exceeds_max_multiplicity','l42b']]
      +sda('DiscriminantMultihomogeneous'),
      [3],dependencies=['CG2'],
      assumptions=['Ck>=32 and the literal frame/size hypotheses, including P1 and P3.'],
      note='This is the same shared completed numerical result as RS2–RS3, whose elementary proof is recorded again for local readability; it is not an additional unproved interface. SD3 supplies nonvanishing separately and is not reproved.')


claim('CG4','Internal coarse degrees and the oldest-letter dichotomy',
      'A nonzero actual coarse generator has degree a′. An intermediate physical row occurs in only one segment, so a′=p^(dist+R)*b+label degree and the label bound yields b>a′/p^(dist+R)−k. The oldest of r vector predecessors of a late letter belongs either to the old frame or the intermediate set, exactly matching the two theta^c branches.',
      'faithful_translation',
      sda('TopDegreeComparison')
      +sda('OldestLetterInSegment')
      +[sd('DiscriminantNeZeroOfResidueNeZero',n,'target_interface') for n in ['Step2','TopDegreeComparison']]
      +[sd('ReflectionMemGlevCastSucc','OldestLetterInSegment','target_interface')],
      [4],dependencies=['CG2'],
      assumptions=['The coarse product u is nonzero; the u=0 case is handled separately in CG8.',
                   'Each y_j has its declared whole-letter multidegree and satisfies the coarse allowed support.'],
      note='The degree equality uses fixed multihomogeneity, not an unjustified assertion that arbitrary product monomials cannot cancel. The integer-row and residue uniqueness distinction is preserved.')


claim('CG5','The complete threshold and normal-order numerical transfers',
      'Both actual theta^c cases satisfy P_j(theta^c−kNs)>=theta. The proof uses c>=40kNs, q>=0.9c, b>q−k or floor(q)>q−1, retaining the old-frame offsets k+r+1 and m0=kNs+1. The oldest-letter gap gives P_j*o^c+kP_j<=o, with the exact source even/odd target constants10 and1.',
      'faithful_translation',
      sda('ThresholdPowerBoundOfCounts')
      +[sd('ReflectionMemGlevCastSucc','OrderNumericBound','target_interface')]
      +[sd('ColumnConditionsOfNumericBounds',n,'target_interface') for n in
        ['EllDegreeLePowerBound','PowerExceedsMaxMultiplicity','ThresholdPowerLowerBound']],
      [5],dependencies=['CG3','CG4'],
      assumptions=['p>=13, k>=5, Ns,Y>=1, r<=k; all follow from literal Dat.Hyp.'],
      note='The even case has an unused intermediate coefficient2 rather than10. The final theorem retains10 and changes no downstream source normalization.')


claim('CG6','Canonical Frobenius product and all fine prefix and order bounds',
      'For one allowed coarse paired path polynomial B=A0G0, reduction of D_j*expand_P(B)*X^e is A0^P*ellP*D_j times G0^P*ellN. Canonical coefficients lie in the prime field, so this identity is valid without inverse coefficient Frobenius. Signed label costs dS+dV<=kNsP and the individual determinant order s_x prove every fine gap, threshold and normal-order condition, with correct even/odd prefix indices and supports.',
      'faithful_translation',
      sda('ColumnWordReductionOfFour')
      +sda('FrobeniusReductionProduct')
      +sda('ColumnConditionsOfNumericBounds')
      +sda('ValuationLambdaFieldProperties')
      +sda('AllowedLettersOfLateRows')
      +sda('WordOrderBoundOfNumericBound'),
      [6],dependencies=['CG1','CG3','CG4','CG5','IP3','IP4'],
      assumptions=['The residue field has characteristic p; canonical path polynomials have integral coefficients by their literal wedge/contraction construction.',
                   'Local label e is late-supported and every exponent is <P_j.'],
      note='The source four-premise wrapper is expanded into actual arithmetic and polynomial proofs. The general y expansion is coefficient-linear; no perfection of the residue field or false characteristic-zero Frobenius equivariance is used.')


claim('CG7','Integral segment lift with the exact letter degree',
      'Expand the coarse y in the allowed integral path basis, lift each canonical product by CG6 and CG1, and preserve the original scalar coefficients. The exact z_j degree is P_j*b plus label degree plus determinant-row occurrence degree. Projecting the integral lift onto this whole-letter degree preserves XX′ and the residue congruence, proving SegmentReductionLiftsMultihomogeneous.',
      'faithful_translation',
      sda('SegmentReductionOfColumnWords')
      +[sd('SegmentProductDegreeDetermined',n) for n in
        ['degAt_sum','degAt_C_mul','degAt_detPl','segment_image_multihomogeneous']]
      +[sd('DiscriminantNeZeroOfResidueNeZero',n,'target_interface') for n in
        ['SegmentReductionLiftsMultihomogeneous','SegmentImageMultihomogeneous']]
      +[gb('ValuationLowestDegreeMapFractionField',n,'degree_projection') for n in
        ['polComp','polComp_mem_Pol','polComp_of_mem','polComp_of_ne','twistSub_polComp',
         'valS_le_polComp','lowest_degree_compose_le','exists_sum_polComp']],
      [7],dependencies=['CG1','CG6'],
      assumptions=['The segment y has its actual fixed whole-letter degree b.'],
      note='The homogeneous-component argument is proved, not imported as an unexplained lifting theorem. A zero lift belongs to the prescribed homogeneous submodule and is allowed.')


claim('CG8','Assembly into an individual allowed global generator',
      'After the exact fine/coarse label splitting, form g=Z^ell0 product phi_j(x_j). Replacing each z_j by x_j of the same letter degree preserves the physical degree. Since Delta*u has degree E+a′=d and is nonzero when u is nonzero, g lies in the literal Gen set. Reduction commutes with products and substitutions, giving reduction(Delta*u)=reduction(g). The zero case uses the zero generator.',
      'faithful_translation',
      [sd('DiscriminantNeZeroOfResidueNeZero',n) for n in
        ['map_phSeg','phc_eq','generator_of_segment_reductions']]
      +[sd('SegmentProductDegreeDetermined',n) for n in
        ['multideg_imgMon','sum_eq_multideg','multideg_imgMon_congr','degAt_aeval',
         'degAt_monomial','mem_Pol_of_degAt','segment_product_degree_determined']]
      +[sd('DiscriminantNeZeroOfResidueNeZero','SegmentProductDegreeDetermined','target_interface')]
      +[gb('SegRing','Gen','literal_target_set')],
      [8],dependencies=['CG1','CG2','CG3','CG4','CG5','CG6','CG7','SD3'],
      assumptions=['SD3 gives Delta nonzero over the residue field and hence over O.',
                   'O is a domain, J>=1, and all supplied frame and numeric hypotheses are retained.'],
      note='The conclusion is one element of Gen, not just a residue-span relation or a claimed member of the later chosen independent basis B_b. The nonzero and zero cases are both explicit.')


claim('CG9','Exact closed theorem and remaining global scope',
      'The reconstruction proves GeneratorModuloUniformiser(C0) for every C0>=32 under the literal UniformizedDVR and Dat.Hyp data, with CLa,Ck>=C0. It removes the coarse-generator congruence item of SD8. Quantitative coarse-family dimension, global frame/parameter supply and other global arithmetic and analytic inputs remain separate.',
      'faithful_translation',
      [gb('ObjPol','UniformizedDVR','coefficient_hypotheses'),
       sd('NonemptyDvrSettingOfStandard','Dat','data'),
       sd('NonemptyDvrSettingOfStandard','Hyp','exact_hypotheses'),
       sd('NonemptyDvrSettingOfStandard','XXs','fine_segment_space'),
       sd('NonemptyDvrSettingOfStandard','gen','fine_generator_set'),
       sd('Coarse','GeneratorModuloUniformiser','exact_endpoint'),
       sd('Coarse','restRank_of','downstream_use'),
       sd('DiscriminantNonzeroModUniformiser','generator_modulo_uniformiser_of_adm','source_assembly'),
       sd('DiscriminantNonzeroModUniformiser','top_count_lower_bounds','shared_numeric_interface')],
      [0,9],dependencies=['CG1','CG2','CG3','CG4','CG5','CG6','CG7','CG8','IP3','IP4','SD3'],
      assumptions=['Supplied actual Dat.Hyp / UniformizedDVR data; global existence is outside this local theorem.'],
      note='No local specialized coarse-lifting premise remains unproved. The larger AdmB/NestedTypeBound conjunctions are not used as black boxes; only the precise needed clauses are reconstructed. No whole RH/GRH proof or kernel replay is asserted.')


companions=[]
for component,path,ids in [
    ('universal_integral_path_basis','v0_5/path_generators/provenance.json',['IP3','IP4']),
    ('multiplier_nonvanishing','v0_6/selected_dimension/provenance.json',['SD3'])
]:
    p=WORK/path
    companions.append(dict(component=component,claims=ids,path=path,
                           sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status='proved_companion'))
companions.append(dict(component='degree_and_scale_arithmetic',claims=['RS2','RS3'],
                       status='proved_companion_and_reproduced_in_CG3',
                       note='The current v0.7 root reconstruction owns RS2–RS3; CG3 records the same full elementary calculation.'))
companions.append(dict(component='actual_RestLam',claims=['LA3'],status='consumer_of_CG1',
                       note='CG1 supplies the actual XX′ saturation and base change used by LA; no reverse dependence is asserted.'))

out=dict(schema_version='1.2',artifact_version='0.7',date='2026-11-21',owner='/root/lean_audit',
         repository=dict(url=REPO,commit=COMMIT),
         range_convention='One-indexed inclusive line intervals. Source bytes are compared to the pinned git blob; the unnormalized bytes in each declared interval are hashed.',
         verification=dict(full_file_bytes_compared_with_pinned_git_blob=True,
                           range_bytes_hashed_without_normalization=True,
                           human_mathematical_proofs_supplied=True,
                           local_lean_compilation=False,lean_kernel_replay=False,
                           replacement_arguments_formalized=False),
         status_definitions=dict(
             faithful_translation='A complete human proof of the precise cited source statement under its explicit application hypotheses.',
             derived_simplification='An explicitly proved shorter route to the exact required source assertion; any unused stronger scope is stated.',
             remaining_input='An explicitly identified specialized claim still requiring a human proof. No CG claim uses this status.'),
         claims=claims,files=[files[p] for p in sorted(files)],companion_dependencies=companions)
(OUT/'provenance.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(OUT/'source_manifest.json').write_text(json.dumps(dict(repository=out['repository'],files=out['files']),indent=2,ensure_ascii=False)+'\n')
loc=[]
for c in claims:
    loc += [c['id']+': '+c['title'],'Status: '+c['status']]
    for s in c['sources']:
        loc += ['  '+s['declaration'],'  '+s['url'],
                '  file SHA256 '+s['sha256'],'  range SHA256 '+s['excerpt_sha256']]
    loc.append('')
(OUT/'source_locators.txt').write_text('\n'.join(loc))
print(json.dumps(dict(claims=len(claims),source_files=len(files),
                      source_references=sum(len(c['sources']) for c in claims),
                      statuses={s:sum(c['status']==s for c in claims) for s in out['status_definitions']})))
