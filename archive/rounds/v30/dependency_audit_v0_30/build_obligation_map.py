#!/usr/bin/env python3
"""Build the connected, sufficient-interface graph without promoting work links."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve()
DEFAULT_PACKAGE = (HERE.parents[1] if HERE.parent.name == 'dependency_audit_v0_30'
                   else HERE.parents[2] / 'reconstruction_v030')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package', type=Path, default=DEFAULT_PACKAGE,
                    help='Reconstruction v0.30 package directory')
parser.add_argument('--repo', type=Path, default=DEFAULT_PACKAGE.parent / 'lean_source',
                    help='Exact pinned Lean checkout')
parser.add_argument('--validation-dir', type=Path, default=HERE.parent,
                    help='Directory for machine validation reports')
ARGS = parser.parse_args()
NEW = ARGS.package.resolve()
ROOT = NEW.parent
REPO = ARGS.repo.resolve()
WORK = ARGS.validation_dir.resolve()
WORK.mkdir(parents=True, exist_ok=True)
OUT = NEW / 'dependency_audit_v0_30/obligation_map.json'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
OLD_PATH = NEW / 'dependency_audit_v0_29/obligation_map.json'
OLD_BYTES = OLD_PATH.read_bytes()
OLD = json.loads(OLD_BYTES)
OLD_NODES = {n['id']: n for n in OLD['nodes']}
COUNT_PATH = NEW / 'dependency_audit_v0_30/count_frontier.json'
COUNT = json.loads(COUNT_PATH.read_text())
CN = {n['id']: n for n in COUNT['nodes']}
GLOBAL_PATH = NEW / 'dependency_audit_v0_30/global_frontier_inventory.json'
GLOBAL = json.loads(GLOBAL_PATH.read_text())
GN = {n['id']: n for n in GLOBAL['records']}
LIT_PATH = NEW / 'dependency_audit_v0_30/literature_audit.json'
LIT = json.loads(LIT_PATH.read_text())
NODES = {}
REFINEMENTS = {}
OPTIONAL = {}
WORK_LINKS = []
SOURCE_CACHE = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def original_evidence(*ids):
    result = []
    for ident in ids:
        n = OLD_NODES[ident]
        r = {k: v for k, v in n.items()
             if k not in ('history', 'requires', 'alternatives', 'related_nodes', 'gate')}
        r['inherited_node_id'] = ident
        r['inherited_map_sha256'] = sha(OLD_BYTES)
        r['evidence_role'] = 'Prior proved/certified scope, not import of stale dependency edges.'
        registry = n.get('registry')
        if registry and (NEW / registry).exists():
            r['registry_sha256'] = sha((NEW / registry).read_bytes())
        result.append(r)
    return result


def proof(module, claims=()):
    d = NEW / module
    p = d / 'provenance.json'
    result = {'module': module, 'claims': list(claims)}
    if p.exists():
        j = json.loads(p.read_text())
        result.update(provenance_file=str(p.relative_to(NEW)), provenance_sha256=sha(p.read_bytes()))
        result['claim_records'] = [n for n in j.get('claims', [])
                                   if not claims or n.get('id') in claims]
    for name in ['main.tex', 'grh_section.tex', 'window_bridge_section.tex', 'main_section.tex']:
        if (d / name).exists():
            result['proof_file'] = str((d / name).relative_to(NEW))
            result['proof_sha256'] = sha((d / name).read_bytes())
            break
    return result


def src(path, declaration, start=None, end=None):
    data = SOURCE_CACHE.setdefault(path, (REPO / path).read_bytes())
    lines = data.splitlines(keepends=True)
    if start is None:
        pat = re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:theorem|def|abbrev|lemma|structure|class)\s+' + re.escape(declaration) + r'(?:\s|\{|\(|:)')
        matches = [i for i, line in enumerate(lines) if pat.search(line.decode())]
        if len(matches) != 1:
            raise ValueError((path, declaration, matches))
        start = matches[0] + 1
        end = start
        nextdecl = re.compile(r'^(?:(?:private|protected|noncomputable)\s+)*(?:theorem|def|abbrev|lemma|structure|class)\s+')
        while end < len(lines) and not nextdecl.search(lines[end].decode()):
            end += 1
    segment = b''.join(lines[start-1:end])
    return dict(path=path, declaration=declaration, line_start=start, line_end=end,
                file_sha256=sha(data), range_sha256=sha(segment),
                url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')


def node(ident, title, category, status, contract, requires=(), *, kind='contract',
         evidence=(), bindings=None, rule=None, **extra):
    assert ident not in NODES
    n = dict(id=ident, title=title, category=category, kind=kind, status=status,
             contract=contract, gate='AND' if requires else 'LEAF', requires=list(requires),
             evidence=list(evidence), **extra)
    if bindings:
        n['bindings'] = bindings
    if rule:
        n['sufficient_rule'] = rule
    NODES[ident] = n
    return n


def certificate(ident, title, contract, *, evidence=(), requires=(), category='B', **extra):
    return node(ident, title, category, 'proved_in_stated_scope', contract, requires,
                kind='implication_certificate', evidence=evidence, **extra)


def task(ident, title, category, contract, evidence=()):
    return node(ident, title, category, 'human_proof_still_required', contract,
                kind='implication_reconstruction_task', evidence=evidence,
                not_an_extra_mathematical_hypothesis=True)


def count_node(ident, oldid, requires=(), *, status=None, contract=None, kind='contract', **extra):
    n = CN[oldid]
    return node(ident, n['title'], n['classification'], status or n['status'],
                contract or n.get('contract', n['title']), requires,
                kind=kind, evidence=n.get('sources', []),
                inherited_count_frontier_id=oldid, **extra)


def refinement(ident, title, category, contract, evidence=(), **extra):
    assert ident not in REFINEMENTS
    REFINEMENTS[ident] = dict(id=ident, title=title, category=category,
                             kind='work_refinement', status='open',
                             contract=contract, evidence=list(evidence),
                             no_sufficient_implication_claim=True, **extra)


def work(consumer, *items, rationale='Shared work or a partial proof breakdown; not a sufficient AND rule.'):
    for item in items:
        WORK_LINKS.append(dict(consumer=consumer, dependency=item, relation='work_refinement',
                               logical=False, rationale=rationale))


CB = 'src/Development/AutomorphicArithmetic/CharacterBoxes/'
PC = 'src/Development/AutomorphicArithmetic/PrimitiveCosets/'
GI = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'

# Explicit completed analytic and native source glue. Proof certificates do not
# assert their antecedents; their contract explains the conditional arrow.
certificate('CERT_ANALYTIC_ZERO_EXCLUSION', 'Window bound implies the target zero-free half-plane',
            'For a fixed primitive chi, arbitrarily late fixed-stretch windows with exponent approaching 1/2 imply L(s,chi)!=0 for Re(s)>1/2, with the principal pole exception.',
            evidence=original_evidence('ANALYTIC_ENDPOINT'))
certificate('CERT_RH_EXPORT', 'Principal target exports ordinary RH',
            'Apply the principal-target zero-free half-plane statement, functional equation and standard trivial-zero/pole conventions to the source RH conclusion.',
            evidence=[proof('grh', ['GH6', 'GH7'])])
certificate('CERT_DIRICHLET_EXPORT', 'Primitive targets export unrestricted Dirichlet GRH',
            'For every primitive target use the zero-free half-plane; GH6 handles the imprimitive Euler factors and functional equation to obtain the original open-strip statement for every Dirichlet character.',
            evidence=[proof('grh', ['GH6', 'GH7'])])
certificate('CERT_ZW_TERMINAL', 'Exact ChainTied ledger gives the original target windows',
            'ZW1-ZW4, with WB, send literal ChainTied plus EFamC and the same family windows to exponent 1/2+(eD+eL+7)eps on those real windows. No separate arithmetic-gap premise remains.',
            evidence=[proof('tied_window_completion', ['ZW1', 'ZW2', 'ZW3', 'ZW4']),
                      proof('window_bridge', ['WB7', 'WB8'])],
            reviewed_proof_sha256='3e102f1a3e4ddced78b5cd3e92378a3ebdfa68a52b7de5fb69e2ac997eddc7b1')
certificate('CERT_TARGET_CLASS', 'Literal target class gives HypV, EFamC and the same windows',
            'For G=GChi chi and ell=3/2, membership in E=G.cls ell gives HypV on the actual D.nd local-data model, EFamC(Level.cyc chi) with constant4, and the original family windows. FReq.at_of_from preserves original HostAx and TT.',
            evidence=[src(CB+'Supply.lean','GChi'), src(CB+'Supply.lean','cls'),
                      src(CB+'Supply.lean','at_of_from'),
                      src(CB+'ZeroFreeAllOfTopG.lean','hypV_of_cls'),
                      src(CB+'ZeroFreeAllOfTopG.lean','eFamC_of_cls')],
            bindings=['same chi', 'same Fm', 'same D.host.E', 'same TT', 'same cutoff R.t', 'same L.x/L.eps'])
certificate('CERT_CLASS_INCLUSIONS', 'The two source class inclusions are projections',
            'Fix one A. C=WithChN A; Cprime=WithChN(fun Fm => A Fm and (GChi chi).cls(3/2) Fm); E=(GChi chi).cls(3/2). Cprime->C and Cprime->E are the source projections. D3(3,A)=Des(C,3) in the consumed class interface.',
            evidence=[src(CB+'ShapeWin.lean','UpperTheory.Top.shapeWin'),
                      src('src/Formalism/LocalToGlobal/ClassOfRecordOfChoice.lean','D3'),
                      src('src/Formalism/LocalToGlobal/ClassOfRecordOfChoice.lean','WithChN')])
certificate('CERT_DIVINN_FROM_HYPV', 'Same-field cohomology supplies DIVinN',
            'On the same FamP with eps>0, HypV plus LinkN plus SmallLevelRankEq imply DIVinN. vvRecord uses the actual nd.Om and nd.ldat and sha_eq, includes finiteness and summability, and never changes the field or local conditions.',
            evidence=[src(CB+'DivinNOfHypV.lean','vvRecord'), src(CB+'DivinNOfHypV.lean','divinN_of_hypV')],
            evidence_note='Source argument is the explicit finite nonnegative-sum and numerical transport used in DA topDesWin; no new arithmetic supplier.')
certificate('GLOBAL_METRIC', 'MT1-MT7 close the literal LinkMu implication',
            'On one FamP, LinkDIV, NuFullF, MuRank, TuSize and DGamSize imply LinkMu. FamP.nprimeDef is already an original field; NuH changes only the lattice, preserving every metric and ambient object.',
            evidence=[proof('metric_transport', [f'MT{i}' for i in range(1,8)])],
            premises_already_supplied_inside_topDesWin=['LinkDIV from hDIV/hEta/DIVinN', 'fullness and MuRank from hRk', 'TuSize and DGamSize from hEx'],
            reviewed_proof_sha256='55ac8034b4312f450ceb7be32320e2039cc6a063c89db454159b2fa5bb4142a3')
certificate('CERT_TOPDESWIN', 'Finite threshold join and topDesWin assembly',
            'After epsilon is chosen, take one common transported threshold for all nine Closed predicates, then invoke DesignExists once. On that single Fm,CH use the target HypV, LinkN/rank -> DIVinN, hDIV -> LinkDIV, MT -> LinkMu, and hGL -> ChainTied. This proves FamilyClassConnected E.',
            evidence=[src(CB+'DesWin.lean','topDesWin'),
                      src(CB+'DivinNOfHypV.lean','FamilyClassConnected'),
                      proof('dependency_audit_v0_29', ['DA1', 'DA2'])],
            requires=['CERT_DIVINN_FROM_HYPV','GLOBAL_METRIC'])

# Exact first-level ten-input interface. The shared package is a proof template
# with explicit parameter bindings, not one Fm chosen independently for each link.
TEN = ['GLOBAL_DESIGN', 'GLOBAL_DENOMINATOR', 'GLOBAL_LOCAL_COVERAGE',
       'GLOBAL_RETAINED_DEFECT', 'GLOBAL_SMALL_RANK', 'GLOBAL_PERIOD_HEIGHT',
       'GLOBAL_FULL_RANK', 'GLOBAL_LOCAL_GAIN', 'GLOBAL_SPECTRAL', 'GLOBAL_SLOPE']
for ident in TEN:
    if ident in ['GLOBAL_DESIGN','GLOBAL_FULL_RANK','GLOBAL_SLOPE']:
        continue
    g = GN[ident]
    node(ident, g['title'], g['category'], 'open_original_contract', g['exact_obligation'],
         evidence=g['source_anchors'], bindings=g['binding_keys'],
         opaque_frontier=True,
         frontier_note='Partial work packages are in nonlogical work_refinements; they are not asserted sufficient for this contract.')
node('GLOBAL_DESIGN', 'Actual compatible DesignExists producer for a supplied target host', 'C',
     'open_original_construction',
     'For one common source class A and the actual supplied target HostExW, construct the exact DesignExists(WithTw(WithSm Cprime),3) of the selected link_ex/shapeWin route. For every small eps and every transported K choose ONE Fm,CH with class membership, Large K, ChosenE, TuSize and DGamSize. The host is an input to this still-open construction, not a sufficient producer by itself.',
     evidence=GN['GLOBAL_DESIGN']['source_anchors']+[src(CB+'Supply.lean','ExD')],
     bindings=GN['GLOBAL_DESIGN']['binding_keys'],
     open_implication_contract='HostExW(3/2,(GChi chi).req) -> the displayed DesignExists, with all original family-producing hypotheses discharged in this C task.',
     exact_first_level_output=GN['GLOBAL_DESIGN']['exact_obligation'])

# link_gl has a complete exact signature. Its actual inputs and the final human
# installation remain explicit rather than inferring them from mass-ratio labels.
node('GLOBAL_SECOND_LAYER_MATCH', 'Exact common real-place, mass and genus-volume inputs', 'D',
     'open_source_instance_match',
     'On the same A: hduty: forall Fm,A Fm->Duty Fm; tie: Closed(D3 3 A) RealPlaceSecondLayerConditions; hU: forall D,MassRatioUnderVolume D; hG: forall D,GenusMassAt D 2. Match the original operators, metrics, row targets and normalizations to the existing MF/GV/DC/FR/GF suppliers.',
     evidence=[src(GI+'LinkGl.lean','GlobalTheory.Top.link_gl')],
     exact_argument_list=['hduty','tie','hU','hG'],
     no_automatic_promotion='MF/GV/DC theorem names do not alone establish these actual same-D hypotheses.')
task('TASK_LINK_GL_INSTALL', 'Write the exact shared link_gl installation', 'B',
     'Given precisely hduty,tie,hU,hG in GLOBAL_SECOND_LAYER_MATCH, complete the human identification with famGLmin_of_realPlaceSecondLayer, its MuRank/fullness consequence and link8. Preserve Cabs=2,C0=3,eD=2,eL=0.',
     [src(GI+'LinkGl.lean','GlobalTheory.Top.link_gl')])
node('GLOBAL_GL_PAIR', 'The one original link_gl pair of conclusions', 'B', 'conditional_join_open',
     'Both Closed(ChosenE -> NuFullF and MuRank) and Closed(TuSize -> DGamSize -> LinkGLOBAL at 2,3,2,0) on D3(3,A).',
     ['GLOBAL_SECOND_LAYER_MATCH','TASK_LINK_GL_INSTALL'],
     rule='The full LinkGl.lean signature is sufficient; the B node is the remaining human proof/instance installation, not a new arithmetic axiom.')
for ident, side in [('GLOBAL_FULL_RANK', 'first'), ('GLOBAL_SLOPE', 'second')]:
    g=GN[ident]
    node(ident,g['title'],g['category'],'conditional_projection',g['exact_obligation'],
         ['GLOBAL_GL_PAIR'],evidence=g['source_anchors'], rule=f'Take the {side} conjunct of the same link_gl result.')

shared_global = [x for x in TEN if x!='GLOBAL_DESIGN']
for tag, target in [('RH','the principal primitive character 1'),
                    ('GRH','an arbitrary fixed primitive character chi')]:
    inst = dict(target=target, stretch='3/2', Cabs=2, C0=3, eD=2, eL=0,
                A='one common source class A', C='WithChN A',
                Cprime='WithChN(fun Fm => A Fm and (GChi chi).cls(3/2) Fm)',
                E='(GChi chi).cls(3/2)', family='ONE Fm,CH after the common threshold')
    node(f'DESIGN_{tag}', f'Actual target-compatible DesignExists ({tag})', 'C', 'conditional_on_open_design_producer',
         'The literal hEx argument of topDesWin at the displayed target and common class.',
         [f'HOST_{tag}','GLOBAL_DESIGN','CERT_CLASS_INCLUSIONS'],
         bindings=inst, rule='Apply the open GLOBAL_DESIGN construction contract to this actual host; this is not an assertion that the host alone constructs a family.')
    node(f'TOPDESWIN_{tag}', f'Exact ten-input common-family gate ({tag})', 'B', 'proved_implication_with_open_inputs',
         'FamilyClassConnected E from precisely hEx and nine Closed predicates plus h1,h2,hV.',
         [f'DESIGN_{tag}']+shared_global+['CERT_CLASS_INCLUSIONS','CERT_TARGET_CLASS','CERT_TOPDESWIN'],
         kind='sufficient_implication_gate', bindings=inst,
         exact_source_argument_ids=dict(hEx=f'DESIGN_{tag}',hN='GLOBAL_DENOMINATOR',hEta='GLOBAL_LOCAL_COVERAGE',
              hIRR='GLOBAL_RETAINED_DEFECT',hZ='GLOBAL_SMALL_RANK',hDIV='GLOBAL_PERIOD_HEIGHT',hRk='GLOBAL_FULL_RANK',
              hG='GLOBAL_LOCAL_GAIN',hS='GLOBAL_SPECTRAL',hGL='GLOBAL_SLOPE'),
         class_arguments={'h1':'CERT_CLASS_INCLUSIONS','h2':'CERT_CLASS_INCLUSIONS','hV':'CERT_TARGET_CLASS'},
         evidence=[src(CB+'DesWin.lean','topDesWin')],
         quantifier_guard='Closed thresholds precede hEx; never choose nine unrelated families.')
    node(f'FAMILY_CONNECTED_{tag}', f'One connected family for every small epsilon ({tag})', 'B', 'conditional_endpoint',
         'There exist eD,eL,eps1>0; for each 0<eps<eps1 there is one FamP in the target class with K,cHH,eK,CL,x0 before every later x in the same Win, satisfying ChainTied.',
         [f'TOPDESWIN_{tag}'],bindings=inst,
         evidence=[src(CB+'DivinNOfHypV.lean','FamilyClassConnected')])
    node(f'WINDOW_{tag}', f'Arbitrarily late actual target windows ({tag})', 'B', 'conditional_endpoint',
         'For the same fixed target, all sufficiently small eps give the actual real-continuum window bound with exponent 1/2+(2+0+7)eps; the stretch is fixed before the windows.',
         [f'FAMILY_CONNECTED_{tag}','CERT_TARGET_CLASS','CERT_ZW_TERMINAL'],bindings=inst)
    node(f'ZERO_FREE_{tag}', f'Target zero-free half-plane ({tag})', 'B', 'conditional_endpoint',
         'L(s,chi)!=0 when Re(s)>1/2 with the exported principal pole convention.',
         [f'WINDOW_{tag}','CERT_ANALYTIC_ZERO_EXCLUSION'],bindings=inst)
node('ORDINARY_RH','Ordinary Riemann hypothesis','B','not_yet_human_closed',
     'The source RH conclusion for the zeta function, obtained only at the principal target.',
     ['ZERO_FREE_RH','CERT_RH_EXPORT'],kind='final_goal')
node('DIRICHLET_GRH','Unrestricted Dirichlet GRH','B','not_yet_human_closed',
     'For every primitive target, then every induced Dirichlet character: the source right-half-plane/open-strip conclusion.',
     ['ZERO_FREE_GRH','CERT_DIRICHLET_EXPORT'],kind='final_goal',
     quantifier='Prove the parametric GRH branch for every fixed primitive chi; no constants uniform in chi are required beyond each source theorem.')

# Analytic/host leaves, with the exactly checked application scopes preserved.
for short in ['CN','BD','HD']:
    entry=next(x for x in LIT['rechecked_classical_applications'] if x['id']==f'A-{short}')
    node(f'A_{short}', entry['theorem'], 'A', 'published_application_checked', entry['conclusion'],
         kind='published_theorem_application', evidence=[entry]+original_evidence(short))
node('A_SMALL_ONE','Linnik least-prime specialization to residue 1','A','published_application_checked',
     'An absolute C*N^L bound for primes p=1 mod N gives p<=N^a for all N>=2 by absorbing C into the exponent; exact HX1 hypotheses and finite small-modulus adjustment.',
     kind='published_theorem_application',evidence=[proof('host_window_installation',['HX1'])])
certificate('CERT_HOST_PRIOR_CONSTRUCTIONS','Original field, ranks, norm primes and selected host sets',
            'AH18, SZ13, QR25 and HC1-HC9 provide the original field/frame, exact rank/admission, ShortNorm, five auxiliary primes, second set, tops, shares and all compatible host clauses under their recorded exact hypotheses. Their matched classical inputs are retained in the original chapter evidence.',
            evidence=[proof('arithmetic_hosts',['AH18']),proof('size_conditions',['SZ13']),
                      proof('ray_prime_estimates',['QR25']),proof('host_tops',[f'HC{i}' for i in range(1,10)])])
certificate('CERT_PAIR_EX','Actual PairEx, RealBox and ThinH in the original range',
            'QP22-24 construct the same pair and original analytic bounds from CN/BD/HD, with eps in (0,1/52); QP25 is the exact fixed-pair rescaling after VWinAt.',
            requires=['A_CN','A_BD','A_HD'],evidence=[proof('simultaneous_prime_pairs',['QP22','QP23','QP24','QP25'])])
certificate('CERT_HX_HOST','HX1-HX4 install the full actual target host',
            'For a fixed primitive chi, VWinAt(chi,401) implies HostExW(3/2,(GChi chi).req). All constants precede scales; the same q,d,page,field,HostAx,TT and exact bounded-character inducing level are retained. The rescaled cohomological cutoff is floor(x^400).',
            requires=['CERT_HOST_PRIOR_CONSTRUCTIONS','CERT_PAIR_EX','A_SMALL_ONE'],
            evidence=[proof('host_window_installation',['HX1','HX2','HX3','HX4'])],
            reviewed_proof_sha256='37c561051ae31c618455e73bf558530e2545cbb1e8808da26018fc91a3dafaeb')
for tag in ['RH','GRH']:
    node(f'HOST_{tag}',f'Literal same-target HostExW ({tag})','B','conditional_endpoint_closed_by_HX',
         'HostExW(3/2,(GChi chi).req) including RankVal, HostGood, EAtH and VVle on each actual host, with a single scale family and constants.',
         [f'VWIN_{tag}','CERT_HX_HOST'],
         bindings={'target':'principal' if tag=='RH' else 'arbitrary fixed primitive chi',
                   'host_cohomology':'same H.E and R.t; t<=floor(x^400)',
                   'scale':'one J; s.J=J; s.eps=eps'},
         evidence=GN['GLOBAL_HOST_WINDOW']['source_anchors'])

# Closed inherited arithmetic is represented by its precise proved endpoint,
# not by importing all old navigation/history nodes into the selected graph.
certificate('CERT_COHOMOLOGY_NATIVE','Original native cohomology and LemmaK interfaces',
            'Exact source CohomologyHyp, finite native duality/Euler/finiteness, LemmaK, local-K and SoV inputs already reconstructed, including every original coefficient-prime range. SP1-SP6 also supply literal LemmaMprime/LemmaM and FP8 literal LemmaP in their exact original antecedents. No automorphic existence is inferred.',
            evidence=original_evidence('SYMPLECTIC_SOURCE_COHOMOLOGY','NATIVE_FINITE_COHOMOLOGY',
                'LEMMA_K_BOUND','LOCAL_K_INTERFACE_MATCH','FINITE_DUALITY_SPECIALIZATION','ALGEBRAIC_COEFFICIENT_VANISHING',
                'LEMMA_M_PRIME','LEMMA_M','FRAMED_WEIGHTED_PRESENTATION')+
                [proof('symplectic_count_closure',['SP1','SP2','SP3','SP4','SP5','SP6']),
                 proof('framed_deformation_presentation',['FP8'])])
certificate('CERT_COR_X','Literal original CorX','Literal CorX on both original residual characters, retaining exact tame index, arbitrary residue map and local conditions.',
            evidence=original_evidence('COR_X_RESIDUAL_SUPPLIER'))
certificate('CERT_COH_WINDOW_ASSEMBLY','Actual count-to-height-to-window assembly',
            'HV/TW/OB/VW: actual I/II/III/V counts, native K/duality, exceptional count cases and the original two-primary/odd/reference-layer inputs yield fixed-target JointWin and VWinAt. Real scales, original fields, all local data, finite prime sets and arbitrary reference-layer functions are preserved.',
            requires=['CERT_COHOMOLOGY_NATIVE','CERT_PAIR_EX'],
            evidence=original_evidence('TWO_PRIMARY_BOUND','ODD_MINUS_BOUND','FERRERO_WASHINGTON_MATCH','CLASSICAL_WINDOW_ARITHMETIC')+
                     [proof('point_hv_assembly',['HV8','HV9','HV10']),
                      proof('simultaneous_cohomological_windows',['TW8'])])
certificate('CERT_KA4_COUNT_I','KA4 converts reduced CorGK to actual CountI',
            'For a fixed target chi only CorGK at Kchi=Kstar(pK chi) is needed. Kernel-orbit counting and original coefficient return give literal CountI with the required order of constants and both exceptional primes.',
            evidence=[proof('count_i_aggregation',['KA1','KA2','KA4'])])
certificate('CERT_KA3_COR_GK','KA3 converts PropGK to CorGK',
            'For that same fixed Kchi, the exact PropGK integer contract gives the two-prime CorGK estimate. CorGK is the smaller interface; PropGK is a selected sufficient upstream construction.',
            evidence=[proof('count_i_aggregation',['KA3'])])
certificate('CERT_KA5_VACUITY','Case III is vacuous only for 2-power-order target characters',
            'Every permitted original host psi has order dividing 2^(s+2)*order(chi). If order(chi) is a power of two, odd nontrivial CaseIII is impossible. This does not prove universal CountIII.',
            evidence=[proof('count_i_aggregation',['KA5'])],
            target_guard='order(chi) is a power of two, including chi=1')
certificate('CERT_KA6_TARGET_TRANSPORT','KA6 preserves the fixed 2-primary target through all window consumers',
            'Under the 2-power-order target guard, the CorGK/PMExAlt/CountV cut reaches VWinAt(chi,401) through only that fixed target. No CaseIII producer is needed.',
            evidence=[proof('count_i_aggregation',['KA6'])])
certificate('CERT_YX_COUNT_II','QX/UX/YX propagate PMExAlt to literal CountII',
            'The full original Ctx2 seed, realization, point/image/model/rigidity/catalogue and coefficient-return joins supply CountII from PMExAlt. All inherited classical applications remain in their exact recorded ranks and hypotheses.',
            evidence=original_evidence('CASE_TWO_COUNT_SUPPLIER','CASE_TWO_PROMODULAR_REALIZATION','CASE_TWO_IMAGE_DENSITY','CLASSICAL_CASE_TWO_SEED','CLASSICAL_PROMODULAR_GEOMETRY'))
certificate('CERT_QX_PMEX','QX10 builds PMExAlt from joint support on the two actual Links',
            'After the two original Links and their maps are constructed, the same-ideal HidaPropsAlt plus original P1core input at a common coefficient threshold yields the five-clause PMExAlt tower. No separately chosen support ideal is substituted.',
            evidence=original_evidence('ACTUAL_TWO_LINKS','ACTUAL_PM_TOWER_JOIN','FULL_ADJOINT_LIFTING','CLASSICAL_ORDINARY_SUPPORT_TRANSPORT'))
certificate('CERT_CASE3_INHERITED','Inherited cohomology, seed-II and full case-III consumer joins',
            'CohomologyHyp, Ferrero-Washington, HFit, SeedIIAlt, the actual original constructors and JX count consumer are supplied in their exact conditional scopes. SeedIVAlt and Ctx3 realization are not supplied by this certificate.',
            requires=['CERT_COHOMOLOGY_NATIVE'],
            evidence=original_evidence('CASE_TWO_SEED','CLASSICAL_CASE_TWO_SEED','FERRERO_WASHINGTON_MATCH','PAIRED_COUNT_ONE_INPUT_JOIN')+
                [src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/WeakShimuraTheory/NearSplit.lean','Three0'),
                 src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/WeakShimuraTheory/NearSplit.lean','Fit'),
                 src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/CuspidalTwists/PromodularityCaseThree.lean','Four'),
                 src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/CuspidalTwists/PromodularityCaseThree.lean','HFit'),
                 src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/CuspidalTwists/Sp4In.lean','hFit')],
            HFit_human_proof='Given Ctx3 D, T.Ok and Four T, the fields Four.five, Four.sb and Four.psi are exactly T.Three0. The pair (T.Ok, right branch(Ctx3 D,T.Three0)) is the definition of T.Fit. This proves the literal HFit uniformly; Four.quad is unused in this dictionary step.')

# Count I: expose the selected smaller CorGK interface and its sufficient
# PropGK upstream route. Every open proof of an implication has its own node.
count_node('COUNT_I_PRODUCER','COR_GK',['PROP_GK','CERT_KA3_COR_GK'],
           status='reduced_arithmetic_interface_open_upstream',
           contract='For each fixed target chi, literal CorGK only at Kchi=Kstar(pK chi), with uniform constants before all later original hosts/coefficient data. PropGK is sufficient upstream, not logically necessary.',
           interface_cut_member=True,
           bindings={'RH':'Kchi is Q(sqrt(-7)); exceptional prime set {3,7}',
                     'GRH':'Kchi is fixed once from pK chi',
                     'distinct_from_CountV':'The Gaussian/quartic field used by CountV is a different original source field.'})
node('COUNT_I','Actual CountI at the fixed target','B','conditional_endpoint',
     'The original CountI bound, restricted only by the fixed target parameter; all later host/ring/twist/finite-prime-set quantifiers are intact.',
     ['COUNT_I_PRODUCER','CERT_KA4_COUNT_I'])
task('TASK_PROP_GK_INSTALL','Install OneChar and the congruence integer into PropGK','B',
     'Complete the finite orbit/Frobenius/valuation argument producing one nonzero integer before every later coefficient prime, with the original e,N,kernel,p and fixed-K constants.',CN['PROP_GK']['sources'])
count_node('PROP_GK','PROP_GK',['ONE_CHAR','CNR3','TASK_PROP_GK_INSTALL'],
           rule='Exact source OrbEquiv.propGK input chain; the B task is the remaining reconstruction of this implication.')
task('TASK_ONE_CHAR_PROOF','Reconstruct the original one-character argument','C',
     'From exact InpZ and AutomorphyUnramifiedCoefficients, prove the original OneChar trace/length estimate on the supplied coefficient datum and GD input.',CN['ONE_CHAR']['sources'])
count_node('ONE_CHAR','ONE_CHAR',['INP_Z','AUT_UNRAM_COEF','TASK_ONE_CHAR_PROOF'])
task('TASK_INP_Z_ASSEMBLY','Install the exact Kato input record','B',
     'Build the original CohInp/InpZ record using exactly lemM,lemMprime,lemP,RigII,AdVanishK and number on the same arithmetic objects. No rank-four replacement is permitted.',CN['INP_Z']['sources'])
count_node('INP_Z','INP_Z',['CERT_COHOMOLOGY_NATIVE','RIG_II','AD_VANISH_K_MATCH','CNR3','TASK_INP_Z_ASSEMBLY'])
for ident in ['RIG_II','AD_VANISH_K_MATCH','AUT_UNRAM_COEF','CNR3']:
    count_node(ident,ident,opaque_frontier=True)
NODES['RIG_II']['supplier_expansion_incomplete']=True
NODES['RIG_II']['exact_unexpanded_supplier_arguments']=['LitN','LemmaK','Af.AdVanishQ','Af.NewformAut','KatoTwo']
NODES['RIG_II']['warning']='KATO_TWO_MATCH alone is not a sufficient logical producer. Its navigation link is stored only as a work refinement.'

# Count II: one existential scope, never AND of independent ideal existences.
count_node('COUNT_II_SUPPORT','RANK4_JOINT_ORDINARY_SUPPORT',
           contract='For each of the two original QX Links, at the already fixed iota, choose one common coefficient threshold before every later coefficient DVR and every actual universal B/Lambda; then construct one ideal J0 with ring,dense,pt,end1,end2,twist AND the original P1core for that very J0.',
           joint_witness_constraint=dict(
               witness='J0(link,coefficient_DVR,B,Lambda)',
               scope='one witness per actual Link and permitted later universal datum',
               common_threshold_precedes=['later coefficient DVR','actual universal B','weight algebra Lambda','ideal J0'],
               properties_on_same_witness=['HidaPropsAlt.ring','HidaPropsAlt.dense','HidaPropsAlt.pt','HidaPropsAlt.end1','HidaPropsAlt.end2','HidaPropsAlt.twist','P1core'],
               prohibited_inference='(exists J,Hida(J)) and (exists Jprime,P1(Jprime)) does not imply exists J,Hida(J) and P1(J).'),
           opaque_frontier=True)
count_node('PMEX_ALT','PMEX_ALT',['COUNT_II_SUPPORT','CERT_QX_PMEX'],status='conditional_endpoint_closed_by_QX10')
count_node('COUNT_II','COUNT_II',['PMEX_ALT','CERT_YX_COUNT_II'],status='conditional_endpoint_closed_by_YX2')

# Case III is reachable only through the unrestricted target branch.
count_node('COUNT_III_PRODUCER','CASE3_AUT',
           ['CASE3_PROMOD','SEED_IV_ALT','PMEX_ALT','CERT_CASE3_INHERITED','TASK_CASE3_AUT_JOIN'],
           target_guard='Unrestricted target with possible nontrivial odd-order part; absent from selected RH route.')
task('TASK_CASE3_AUT_JOIN','Complete the original Case-III automorphy/image join','B',
     'Install the actual Case-III ProModAlt, SeedIVAlt and shared PMExAlt with the inherited CohomologyHyp/Ferrero-Washington/HFit/SeedII facts into the original whole Case-III automorphy/image conclusion.',CN['CASE3_AUT']['sources'])
task('TASK_CASE3_PROMOD_JOIN','Reconstruct the actual Case-III chain-to-promodularity proof','C',
     'Use the original tensor-factor tower, ChainRankFour, ChainDesc4, seeded rank-four chain reduction, actual PMExAlt and SeedIVAlt to construct ProModAlt on every original Ctx3 star point at the same fixed iota, preserving all finite-coefficient, inertia and support maps.',CN['CASE3_PROMOD']['sources'])
count_node('CASE3_PROMOD','CASE3_PROMOD',
           ['TENSOR_FACTOR_TOWER','CHAIN_RANK_FOUR','CHAIN_DESC4','RANK4_CHAIN_REDUCTION','PMEX_ALT','SEED_IV_ALT','TASK_CASE3_PROMOD_JOIN'])
for ident in ['SEED_IV_ALT','TENSOR_FACTOR_TOWER','CHAIN_RANK_FOUR','CHAIN_DESC4']:
    count_node(ident,ident,opaque_frontier=True)
count_node('RANK4_CHAIN_REDUCTION','RANK4_CHAIN_REDUCTION',opaque_frontier=True,
           warning='SeedIVAlt is a shared input, but its existence alone does not prove this C producer.')
node('COUNT_III_GENERAL','Actual CountIII for the unrestricted target','B','conditional_endpoint',
     'The original CountShape CaseIII conclusion follows from the actual Case-III automorphy/image producer and the completed original count consumer.',
     ['COUNT_III_PRODUCER','CERT_CASE3_INHERITED'],evidence=CN['COUNT_III_GENERAL']['sources'])

# Count V: different original field, complete endpoint argument list and every
# outstanding installation retained. Universal producers are sufficient stronger
# implementations of the fixed-target interfaces, not claimed necessary.
task('TASK_COUNT_V_INSTALL','Complete the original CountV finite assembly','B',
     'From exactly the listed source host/cohomology inputs, complete countV_of_finiteness_duality_euler_host, including original host/frame formation, normalized length, the CaseV guard and R1<=2^c2.',CN['COUNT_V']['sources'])
count_node('COUNT_V_PRODUCER','COUNT_V',
           ['THM_S6_S','HOST_FRAME_LENGTH','HOST_VAN_E','HOST_XPP','HOST_RIGID_S','HOST_NUMBER_S','CERT_COHOMOLOGY_NATIVE','TASK_COUNT_V_INSTALL'],
           status='original_target_restricted_CountV_interface_open',
           contract='Literal CountV for the same fixed target chi and every permitted original CaseV datum. The selected universal ThmS6_s/host-number implementation below is sufficient, and stronger than the fixed-target restriction.',
           bindings={'field':'Original Gaussian/quartic-character field of CountVOf.lean, not Kstar(pK chi) of CountI.',
                     'RH_specialization':'CaseV forces e=1 and ell in {3,7}; dyadic conductors/hosts remain unbounded.',
                     'quantifier_guard':'Constants precede all later original hosts/rings/marked points. Universal all-e/all-prime helper theorems are sufficient, not asserted necessary for RH.'})
for ident in ['THM_S6_S','HOST_FRAME_LENGTH','HOST_RIGID_S','HOST_NUMBER_S']:
    count_node(ident,ident,opaque_frontier=True)
    NODES[ident]['fixed_target_scope'] = (
        'The selected requirement is this source contract restricted to original CountV host/frame data arising from the same fixed chi. '
        'At chi=1 these have e=1 and ell in {3,7}, with unbounded dyadic conductors. '
        'The fully universal source theorem is a sufficient stronger implementation, not an additional logically necessary universal CountV premise.')
    NODES[ident]['source_universal_contract_is_stronger_than_selected_restriction'] = True
task('TASK_HOST_VAN_E_INSTALL','Transport K/duality to literal HostVanE','B',
     'Use the already supplied LemmaK/local-global duality and finiteness on the actual CountV host/frame and exact original coefficient modules.',CN['HOST_VAN_E']['sources'])
count_node('HOST_VAN_E','HOST_VAN_E',['CERT_COHOMOLOGY_NATIVE','TASK_HOST_VAN_E_INSTALL'])
task('TASK_HOST_XPP_INSTALL','Transport CorX to literal HostXpp','B',
     'Preserve Psi^-2 eta, the prime-to-ell quotient, actual local conditions and the original CountV host while installing BR7.',CN['HOST_XPP']['sources'])
count_node('HOST_XPP','HOST_XPP',['CERT_COR_X','TASK_HOST_XPP_INSTALL'])

# The two different cuts are separate logical paths. They share count methods,
# but RH never traverses the general Case-III producer.
node('VWIN_RH','Cohomological target windows for the principal character','B','conditional_endpoint',
     'VWinAt(1,401) on every original target field/local-data model, with the exact page/window quantifiers. The same argument works for any fixed 2-power-order target.',
     ['COUNT_I','COUNT_II','COUNT_V_PRODUCER','CERT_KA5_VACUITY','CERT_KA6_TARGET_TRANSPORT','CERT_COH_WINDOW_ASSEMBLY'],
     selected_arithmetic_cut=['COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'],
     explicit_nonrequirements=['COUNT_III_PRODUCER','SEED_IV_ALT','CASE3_PROMOD'],
     target_binding='chi=1, order=1=2^0; never universally quantify this node over arbitrary primitive chi')
node('VWIN_GRH','Cohomological target windows for arbitrary primitive characters','B','conditional_endpoint',
     'For each arbitrary fixed primitive chi, VWinAt(chi,401) with the complete original host/reference-layer/local-data/window quantifiers.',
     ['COUNT_I','COUNT_II','COUNT_III_GENERAL','COUNT_V_PRODUCER','CERT_COH_WINDOW_ASSEMBLY'],
     selected_arithmetic_cut=['COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_III_PRODUCER','COUNT_V_PRODUCER'])

# Global common work is intentionally not promoted into sufficient AND rules.
for ident in ['GLOBAL_LOCAL_THETA_BINDINGS','GLOBAL_ACTUAL_ROW_SPECTRUM']:
    g=GN[ident]
    refinement(ident,g['title'],g['category'],g['exact_obligation'],g['source_anchors'],
               retained_work=g['remaining_work'], bindings=g['binding_keys'])
refinement('GLOBAL_SMALL_PROJECTION_MATCH','Find the actual zL projection-surjectivity supplier','D',
           'Identify the original lPrj, mu0, target row space and exact zL premise. Only after that match can the finite-dimensional rank argument run.',GN['GLOBAL_SMALL_RANK']['source_anchors'])
refinement('GLOBAL_SMALL_RANK_LINEAR_JOIN','Install the actual finite-dimensional small-rank implication','B',
           'Given the exact original level-projection surjectivity and source row identifications, write the finite-dimensional SmallLevelRankEq argument.',GN['GLOBAL_SMALL_RANK']['source_anchors'])
for consumer in ['GLOBAL_DESIGN','GLOBAL_DENOMINATOR','GLOBAL_LOCAL_COVERAGE','GLOBAL_PERIOD_HEIGHT','GLOBAL_LOCAL_GAIN','GLOBAL_SPECTRAL']:
    work(consumer,'GLOBAL_LOCAL_THETA_BINDINGS')
for consumer in ['GLOBAL_DESIGN','GLOBAL_DENOMINATOR','GLOBAL_RETAINED_DEFECT','GLOBAL_SMALL_RANK','GLOBAL_SPECTRAL']:
    work(consumer,'GLOBAL_ACTUAL_ROW_SPECTRUM')
work('GLOBAL_SMALL_RANK','GLOBAL_SMALL_PROJECTION_MATCH','GLOBAL_SMALL_RANK_LINEAR_JOIN')
work('GLOBAL_DESIGN','GLOBAL_SECOND_LAYER_MATCH', rationale='Shared actual real-stage normalization can contribute to design construction; this is not a sufficient Core/DesignExists rule.')

for oldid in ['KATO_TWO_MATCH','HIDA_FIELDS','P1_CORE_MATCH']:
    n=CN[oldid]
    refinement(oldid,n['title'],n['classification'],n['contract'],n.get('sources',[]),
               underlying_reconstruction_category=n.get('underlying_reconstruction_category'))
refinement('RIG_II_AD_VANISH_Q_MATCH','Exact rank-two AdVanishQ source matching','D',
           'The VwinOfLeaves.rigII supplier also requires Af.AdVanishQ on the original rank-two representation; no rank-three/four transfer by name is asserted.',
           [src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/VwinOfLeaves.lean','rigII')])
refinement('RIG_II_NEWFORM_AUT','Actual NewformAut producer in the RigII source route','C',
           'Construct/match Af.NewformAut in the exact VwinOfLeaves.rigII signature with the original modular form, local and coefficient hypotheses.',
           [src('src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/VwinOfLeaves.lean','rigII')])
work('RIG_II','KATO_TWO_MATCH','RIG_II_AD_VANISH_Q_MATCH','RIG_II_NEWFORM_AUT','CERT_COHOMOLOGY_NATIVE',
     rationale='The exact source supplier lists LitN,LemmaK,AdVanishQ,NewformAut,KatoTwo; RigII remains opaque. This partial work list is not a sufficient replacement for RigII.')
work('COUNT_II_SUPPORT','HIDA_FIELDS','P1_CORE_MATCH',rationale='Subproperties of one jointly constructed J0 above one common threshold, not independent existential ideal suppliers.')
refinement('P1_CORE_ARITHMETIC_PRODUCER','Original same-ideal characteristic-ell support','C',
           'After the D literature/source match, prove the original P1core for the very Hida ideal, including characteristic three if permitted by the actual Link. A candidate theorem with ell>3 is not enough.',CN['P1_CORE_MATCH']['sources'])
work('COUNT_II_SUPPORT','P1_CORE_ARITHMETIC_PRODUCER')
work('RANK4_CHAIN_REDUCTION','SEED_IV_ALT',rationale='SeedIVAlt is an input to the seeded chain route; it is not a sufficient producer of the full reduction.')
refinement('HOST_RIGID_ARITHMETIC','Original CountV adjoint/automorphy hypotheses if not already available','C',
           'If the D HostRigid_s theorem match requires arithmetic hypotheses beyond the installed original host, reconstruct those actual hypotheses. Do not import rank-four rigidity unchanged.',CN['HOST_RIGID_S']['sources'])
work('HOST_RIGID_S','HOST_RIGID_ARITHMETIC')

# Optional/reuse routes never occur in selected logical requires.
for oldid in ['RANK4_TO_RANK3_CATALOGUE_MATCH','COUNT_V_BROAD_ALTERNATIVE']:
    n=CN[oldid]
    OPTIONAL[oldid]=dict(id=oldid,title=n['title'],category=n['classification'],status=n['status'],
                        contract=n['contract'],evidence=n.get('sources',[]),
                        relation='optional_reuse_or_stronger_route',selected=False,
                        note=n.get('note'))
OPTIONAL['COUNT_I_DIRECT_COR_GK']=dict(id='COUNT_I_DIRECT_COR_GK',category='C',selected=False,
    title='An independent direct proof of the reduced CorGK interface',
    contract='CorGK at Kchi would suffice without proving the stronger PropGK construction. No independent new direct producer is supplied.',
    replaces=['PROP_GK'],consumer='COUNT_I_PRODUCER')
OPTIONAL['DIRECT_GAP_WINDOWS']=dict(id='DIRECT_GAP_WINDOWS',category='C',selected=False,
    title='Direct arithmetic-gap window contract',
    contract='An independent producer of the explicit arithmetic-gap windows would suffice analytically, but none is supplied. The earlier contract repackages common family, local gain, period, spectral and host inputs.',
    evidence=original_evidence('DIRECT_GAP_WINDOWS'))
OPTIONAL['AQ_POSITIVE_PART_ENVELOPE']=dict(id='AQ_POSITIVE_PART_ENVELOPE',category='B',selected=False,
    title='Weaker positive-part integral terminal contract',
    contract='AQ1-AQ5 prove the terminal analytic implication from late positive-part integral envelopes (or integer-window control). No arithmetic producer is asserted.',
    evidence=[n for n in LIT['claims'] if n['id'].startswith('AQ')])
OPTIONAL['UNIVERSAL_REAL_STAGE']=dict(id='UNIVERSAL_REAL_STAGE',category='C',selected=False,
    title='Universal real-stage/discrete-series interface',
    contract='Stronger universal interfaces and internal proofs of matched Harish-Chandra/Tamagawa inputs remain optional beyond the actual large-gap route.',
    evidence=original_evidence('ACTUAL_REAL_STAGE','POLYNOMIAL_REPRESENTATION'))
OPTIONAL['ALL_RANK_CATALOGUES']=dict(id='ALL_RANK_CATALOGUES',category='C',selected=False,
    title='All-rank and unchanged-level catalogue packages',
    contract='The actual paired-count catalogue is complete in its scope. Stronger CountQAlt/LevelPNAlt source records are not new prerequisites.')
OPTIONAL['OTHER_BACKLOG_OPTIONAL_SCOPES']=dict(id='OTHER_BACKLOG_OPTIONAL_SCOPES',category='D',selected=False,
    title='Remaining explicitly optional stronger or alternative source routes',
    contract='See target_disposition.json: source-specific huge density constants, fixed-1/8 selection, older wrappers, internal classical proofs, split-support routes and stronger symmetric columns are retained with exact scopes.',
    inventory_file='dependency_audit_v0_30/target_disposition.json')


def reach(start, adjacency):
    seen=set()
    todo=[start]
    while todo:
        x=todo.pop()
        if x in seen: continue
        seen.add(x)
        todo.extend(adjacency.get(x, []))
    return seen


def cycles(adjacency):
    state={}
    stack=[]
    def visit(x):
        if state.get(x)==1:
            raise ValueError('cycle '+str(stack+[x]))
        if state.get(x)==2:return
        state[x]=1;stack.append(x)
        for y in adjacency.get(x,[]):visit(y)
        stack.pop();state[x]=2
    for x in adjacency:visit(x)


roots=['ORDINARY_RH','DIRICHLET_GRH']
adj={k:v['requires'] for k,v in NODES.items()}
missing=sorted({x for ys in adj.values() for x in ys if x not in NODES})
assert not missing, missing
cycles(adj)
rh=reach('ORDINARY_RH',adj);grh=reach('DIRICHLET_GRH',adj)
assert rh|grh==set(NODES), sorted(set(NODES)-(rh|grh))
case3={'COUNT_III_PRODUCER','COUNT_III_GENERAL','CASE3_PROMOD','SEED_IV_ALT',
       'TENSOR_FACTOR_TOWER','CHAIN_RANK_FOUR','CHAIN_DESC4','RANK4_CHAIN_REDUCTION',
       'TASK_CASE3_AUT_JOIN','TASK_CASE3_PROMOD_JOIN','CERT_CASE3_INHERITED'}
assert not case3&rh, sorted(case3&rh)
assert case3<=grh, sorted(case3-grh)
assert {'COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'}<=rh
assert not set(OPTIONAL)&set(NODES)
assert all(len(NODES[f'TOPDESWIN_{tag}']['exact_source_argument_ids'])==10 for tag in ['RH','GRH'])
assert all(set(NODES[f'TOPDESWIN_{tag}']['exact_source_argument_ids'].values())<=set(NODES[f'TOPDESWIN_{tag}']['requires']) for tag in ['RH','GRH'])
assert NODES['COUNT_II_SUPPORT']['requires']==[]
assert len(NODES['COUNT_II_SUPPORT']['joint_witness_constraint']['properties_on_same_witness'])==7
all_ids=set(NODES)|set(REFINEMENTS)|set(OPTIONAL)
assert len(all_ids)==len(NODES)+len(REFINEMENTS)+len(OPTIONAL)
assert all(e['consumer'] in all_ids and e['dependency'] in all_ids for e in WORK_LINKS)
assert all(not e['logical'] for e in WORK_LINKS)
assert set(REFINEMENTS)<={e['dependency'] for e in WORK_LINKS}
workadj=defaultdict(list)
for k,v in adj.items():workadj[k].extend(v)
for e in WORK_LINKS:workadj[e['consumer']].append(e['dependency'])
cycles(workadj)
assert set(REFINEMENTS)<=reach('ORDINARY_RH',workadj)|reach('DIRICHLET_GRH',workadj)
assert not NODES['RIG_II']['requires']

# Verify every actual source block recursively present in the assembled evidence.
checks={}
def check_blocks(obj):
    if isinstance(obj,dict):
        path=obj.get('path')
        if isinstance(path,str) and path.startswith('src/') and 'line_start' in obj and 'line_end' in obj:
            data=SOURCE_CACHE.setdefault(path,(REPO/path).read_bytes())
            a,b=obj['line_start'],obj['line_end']
            key=(path,a,b)
            segment=b''.join(data.splitlines(keepends=True)[a-1:b])
            expected=obj.get('range_sha256')
            if expected:assert sha(segment)==expected,(key,'range')
            file_expected=obj.get('file_sha256') or obj.get('full_file_sha256') or obj.get('sha256')
            if file_expected:assert sha(data)==file_expected,(key,'file')
            checks[key]=dict(path=path,line_start=a,line_end=b,range_sha256=sha(segment),file_sha256=sha(data))
        for value in obj.values():check_blocks(value)
    elif isinstance(obj,list):
        for value in obj:check_blocks(value)

check_blocks(list(NODES.values())+list(REFINEMENTS.values())+list(OPTIONAL.values()))
for ident,module,expected in [
    ('CERT_ZW_TERMINAL','tied_window_completion','3e102f1a3e4ddced78b5cd3e92378a3ebdfa68a52b7de5fb69e2ac997eddc7b1'),
    ('CERT_HX_HOST','host_window_installation','37c561051ae31c618455e73bf558530e2545cbb1e8808da26018fc91a3dafaeb'),
    ('GLOBAL_METRIC','metric_transport','55ac8034b4312f450ceb7be32320e2039cc6a063c89db454159b2fa5bb4142a3')]:
    assert sha((NEW/module/'main.tex').read_bytes())==expected,(ident,'proof hash')

validation=dict(
    missing_selected_logical_references=missing,
    logical_graph_acyclic=True,
    logical_plus_work_graph_acyclic=True,
    all_selected_nodes_reachable_from_roots=True,
    selected_node_count=len(NODES),work_refinement_node_count=len(REFINEMENTS),
    optional_node_count=len(OPTIONAL),
    rh_reachable_count=len(rh),dirichlet_grh_reachable_count=len(grh),
    rh_excludes_every_case_III_producer=True,
    unrestricted_grh_includes_case_III=True,
    both_roots_reach_I_II_V=True,
    ten_exact_topDesWin_arguments_checked=True,
    same_ideal_count_II_coupling_checked=True,
    no_separate_existential_Hida_P1_AND_rule=True,
    RigII_partial_dependencies_not_promoted=True,
    CountI_and_CountV_field_bindings_distinct=True,
    all_work_refinements_attached=True,
    optional_nodes_not_in_selected_logical_graph=True,
    source_range_count_verified=len(checks),
    source_file_count_verified=len({k[0] for k in checks}),
    HX_MT_ZW_peer_reviewed_proof_hashes_checked=True,
    new_Lean_build_performed=False,
)
payload=dict(
    schema='rh-connected-selected-route-audit/1',artifact_version='0.30',source_commit=PIN,
    formal_proof_assumption='The underlying Alpoge-Claude Lean proof is fully checked and correct. All open statuses concern human reconstruction only.',
    scope='A connected selected sufficient-interface route, not a theorem of mathematical minimality and not an exhaustive Lean declaration dependency graph.',
    roots=roots,
    schema_explanation={
        'edge_direction':'A node points to the premises/proof tasks required by its displayed selected sufficient rule.',
        'AND':'All requires entries are required by that complete displayed rule. It is sufficiency, not necessity.',
        'LEAF':'A proved certificate or an exact remaining opaque producer/implication task. Open leaves are not asserted true by this audit.',
        'implication_certificate':'A completed conditional argument. It proves only its arrow; it does not supply its antecedents.',
        'implication_reconstruction_task':'The remaining B/C human proof of a precisely stated source implication; included separately so its inputs are not falsely treated as already sufficient in the human manuscript.',
        'work_refinements':'Nonlogical shared work or partial source expansion. No subset or conjunction here is asserted to produce the consumer.',
        'optional_routes':'Stronger interfaces, possible theorem reuse or alternate analytic contracts; excluded from selected logical reachability.',
        'parametric_bindings':'Shared templates are instantiated at the target carried by the root. RH uses chi=1; unrestricted GRH uses an arbitrary fixed primitive chi and then universal quantification.',
        'category_vs_status':'A/B/C/D classifies the argument or human matching problem independently of whether it is complete.'},
    categories=GLOBAL['category_key'],
    source_inputs=dict(old_map=dict(file=str(OLD_PATH.relative_to(NEW)),sha256=sha(OLD_BYTES)),
                       count_frontier=dict(file=str(COUNT_PATH.relative_to(NEW)),sha256=sha(COUNT_PATH.read_bytes())),
                       global_inventory=dict(file=str(GLOBAL_PATH.relative_to(NEW)),sha256=sha(GLOBAL_PATH.read_bytes())),
                       narrative=dict(file='dependency_audit_v0_30/main.tex',sha256=sha((NEW/'dependency_audit_v0_30/main.tex').read_bytes())),
                       literature=dict(file='dependency_audit_v0_30/literature_audit.json',sha256=sha(LIT_PATH.read_bytes()))),
    selected_interface_cuts={
        'common_family':dict(source='UpperTheory.Top.topDesWin',source_argument_count=10,
            ten_contracts=TEN,class_side_conditions=['Cprime -> C','Cprime -> E','E -> HypV'],
            constants={'Cabs':2,'C0':3,'eD':2,'eL':0},
            binding='One C,Cprime,E and ONE Fm,CH selected after the common Closed threshold.'),
        'RH_cohomology':dict(target='chi=1',smaller_interface=['CorGK at Kstar7','PMExAlt','CountV at chi=1'],
            canonical_producers=['COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_V_PRODUCER'],
            excluded=['COUNT_III_PRODUCER','SeedIVAlt','Ctx3 promodularity'],certificate='KA5-KA6'),
        'Dirichlet_GRH_cohomology':dict(target='arbitrary primitive chi',smaller_interface=['CorGK at Kchi','PMExAlt','CountIII at chi','CountV at chi'],
            canonical_producers=['COUNT_I_PRODUCER','COUNT_II_SUPPORT','COUNT_III_PRODUCER','COUNT_V_PRODUCER']),
        'warning':'Cuts are relative to the explicit selected source interfaces and the recorded completed classical/assembly certificates. Shared refinement lists are not additional sufficient cuts.'},
    nodes=list(NODES.values()),
    work_refinement_nodes=list(REFINEMENTS.values()),
    work_refinement_links=WORK_LINKS,
    optional_routes=list(OPTIONAL.values()),
    backlog_crosswalk='dependency_audit_v0_30/target_disposition.json',
    validation=validation,
)
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
validation['output_sha256']=sha(OUT.read_bytes())
validation['output_file']=str(OUT)
validation['rh_reachable_ids']=sorted(rh)
validation['grh_reachable_ids']=sorted(grh)
(WORK/'connected_graph_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
(WORK/'connected_graph_validation.txt').write_text(
    'CONNECTED SELECTED-ROUTE GRAPH VALIDATION\n\n'+
    '\n'.join(f'{k}: {v}' for k,v in validation.items() if not k.endswith('_ids'))+
    '\n\nEvery selected logical node is reachable from ORDINARY_RH or DIRICHLET_GRH. '
    'Case III and its seed/tower/promodularity nodes occur only in the unrestricted Dirichlet route. '
    'The CountII joint support node is one opaque coupled existential, not an AND of separately existing ideals. '
    'RigII stays opaque with its incomplete source expansion only in work links. '
    'Open reconstruction tasks are separated from mathematical contract inputs. '
    'Shared dictionaries and possible rank-changing reuse are not treated as sufficient theorem rules.\n')
print(json.dumps({k:v for k,v in validation.items() if not k.endswith('_ids')},indent=2))
