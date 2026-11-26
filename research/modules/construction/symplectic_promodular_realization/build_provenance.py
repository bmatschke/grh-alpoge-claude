#!/usr/bin/env python3
"""Bind UX1--UX12 to exact pinned source ranges and the case-II-only boundary."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
COMPONENT = HERE.name
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPOSITORY = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
W = AV + 'WeakShimuraTheory/'
C = W + 'CompactIntegralFields/'
D = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
F = W + 'FrobeniusFields/'
G = W + 'RamifiedLineCharacters/'
H = W + 'RealPlaceConjugation/'
A = W + 'AdjointCoefficients/'
E = W + 'AdicExtensionMatrices/'
L = W + 'AdicLattices/'
B = AV + 'BuildingsResidueChars/'
sha = lambda b: hashlib.sha256(b).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main(repo):
    files = {}
    cache = {}

    def source(path, name, role=None):
        if path not in cache:
            raw = (repo / path).read_bytes()
            assert raw == subprocess.check_output(['git', '-C', str(repo), 'show', PIN + ':' + path]), path
            cache[path] = raw
            files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                'lines': len(raw.splitlines()), 'url': f'{REPOSITORY}/blob/{PIN}/{path}',
                'verified_equal_to_pinned_git_blob': True}
        raw = cache[path]
        lines = raw.splitlines(keepends=True)
        starts = []
        for n, line in enumerate(lines, 1):
            m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
            if m:
                starts.append((n, m.group(1)))
        matches = [(n, s) for n, s in starts if s == name or (name.startswith('@') and s.rsplit('.', 1)[-1] == name[1:])]
        if len(matches) != 1:
            raise ValueError((path, name, matches))
        start, spelling = matches[0]
        end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
        while end > start and not lines[end - 1].strip():
            end -= 1
        block = b''.join(lines[start - 1:end])
        return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{REPOSITORY}/blob/{PIN}/{path}#L{start}-L{end}',
            'role': role or 'Exact source definition or proof in the stated UX scope; no claim to all transitive Lean dependencies.',
            'verified_equal_to_pinned_git_blob': True}

    spec = {
        'UX1': {
            W+'NearSplit.lean': ['Ctx2', 'Tower', 'TameL', 'IsLayer', 'Dies', 'Ok', 'Two', 'Fit', 'Deep', 'Le'],
            F+'KxKapL.lean': ['@kapEx'], F+'QuadEx.lean': ['@quadEx'],
            F+'CharacterSubgroupOpenEvenIndexTamePower.lean': ['@characterSubgroup_open_even_index_tame_power'],
            F+'Elts2.lean': ['@elts2'], F+'Two2.lean': ['@two2'],
            C+'ExistsTameTowerOkTwo.lean': ['@exists_tame_tower_ok_two'],
            C+'DiesEx.lean': ['@diesEx'], C+'PowOneInj.lean': ['@leFit'], C+'LayerEx.lean': ['@layerEx'],
        },
        'UX2': {
            W+'NearSplit.lean': ['LabOk', 'QPair', 'NearSplit', 'LatShape', 'Over'],
            C+'Labels.lean': ['@labels'], W+'FlagsAndDiagonals/Choice.lean': ['@choice'],
            W+'FlagsAndDiagonals/StarConj.lean': ['@starConj'],
            C+'RootSystemLinearProgramCases.lean': ['@h7'], L+'Vertex.lean': ['@vertex'],
            L+'OddVan.lean': ['@oddVan'], L+'EntVan.lean': ['@entVan'],
            L+'LocVanK.lean': ['@locVanK'], L+'LowCase.lean': ['@shape'], C+'LatSix.lean': ['@lat'],
            C+'FlagFacts.lean': ['@goodQ'], C+'OverFacts.lean': ['@overFacts'],
        },
        'UX3': {
            G+'GysCore.lean': ['@gysCore'], G+'SelBig.lean': ['@selBig'],
            G+'GwLower.lean': ['@gwLower'], G+'SplitPrimes.lean': ['@splitPrimes'],
            G+'ExtRep.lean': ['@extRep'], G+'CupRaw.lean': ['@cupRaw'], G+'CupNorm.lean': ['@cupNorm'],
            G+'SuppMMono.lean': ['@ob'], G+'MemRamLine.lean': ['uQ_mul', 'adj_uQ', 'diag_mul_uQ', 'mem_ramLine'],
            G+'GysinPsOf.lean': ['@cupEx', '@gysinPs_of'], C+'GysinPs.lean': ['@gysinPs'],
            W+'RootsOfUnityShapes/KillQ.lean': ['@killQ'],
        },
        'UX4': {
            D+'Chain2.lean': ['@deep_tower_residue_chain_exists'],
            W+'RedIdeal.lean': ['InV', 'Good', 'IsRes', 'Linked', 'Chain', 'PD.SamePs', 'PD.SameAl'],
            C+'RestrT.lean': ['@restrT'], C+'AffSmulOne.lean': ['@lineP'],
            C+'GlobalTheory.lean': ['@lineM'], C+'ChainMap.lean': ['@chainMap'],
            D+'PotentialModularityTower.lean': ['SeedIIAlt', 'SeedPairAlt', 'IsSeedAlt'],
        },
        'UX5': {
            C+'X2.lean': ['@x2'], W+'RedIdeal.lean': ['Zloc', 'Zgl', 'Str', 'Bounds'],
            H+'ExistsIwasawaRankBoundOfFerreroWashington.lean': ['@exists_iwasawaRank_bound_of_ferreroWashington'],
            H+'KerQFacts.lean': ['@kerOverRationals_open_commutator_layer'],
            H+'PlacesBd.lean': ['@exists_uniform_bound_ncard_placesDividing'],
            H+'Strict.lean': ['@card_cocycles_vanishing_on_inertia_le_pow'],
            H+'CardGlobalCocyclesLeOfIwasawaRank.lean': ['@card_globalCocycles_le_of_iwasawaRank'],
            H+'RankLocalCocycleSpacesLe.lean': ['@rank_localCocycleSpaces_le'],
            H+'BaseCh.lean': ['@rank_le_of_linearForm_comp_mem_of_rank_le'],
            H+'BoundsExt.lean': ['@cocycleBounds_of_ringHom_comp'],
        },
        'UX6': {
            W+'RedIdeal.lean': ['Space', 'Fr.Std', 'Fr.Lifts', 'Fr.IsDef'],
            C+'ContResQ.lean': ['@std'], C+'SpaceEx.lean': ['@spaceEx'],
            E+'SxUnivD.lean': ['@sxUnivD'], E+'SubMemMax.lean': ['@sxGradD'], E+'GenZero.lean': ['@sxGenZero'],
            E+'PreOfCore.lean': ['@sxPreOfCore'], E+'PreImage.lean': ['@sxPreImage'],
            E+'PreLine.lean': ['@sxPreLine'],
            C+'CmplEx.lean': ['@cmplEx'], W+'CmplPt.lean': ['@cmplPt'],
        },
        'UX7': {
            C+'IncLoc.lean': ['count', '@x1'], W+'AdjointMemSp4.lean': ['Fr.Quo', 'adSp', 'bor', 'nil', 'TanC', 'Obs', 'HasPres'],
            A+'DualZero.lean': ['@dualZero'], A+'NotDvdIndex.lean': ['@linkT'],
            A+'ExAbove.lean': ['@ecG'], A+'RankAdjLe.lean': ['@ccDim'], A+'SpDims.lean': ['@spDims'],
            A+'ConeTan.lean': ['@coneTan'], A+'TanInj.lean': ['@tanInj'],
            A+'AbsPres.lean': ['@absPres'], A+'MapAdjAlg.lean': ['@obCoc'],
            A+'GenOfMax.lean': ['@muCyc'], A+'MuQuot.lean': ['@muQuot'],
            AV+'GaloisCochains/H2GaloisQuotientEq.lean': ['@H2_galois_quotient_eq'],
        },
        'UX8': {
            W+'RedIdeal.lean': ['redTypes', 'Good', 'Tan', 'redIdeal'],
            C+'RedList.lean': ['@redList'], C+'RedTan.lean': ['oneOdd_split', 'rel_ps', 'keyB', 'oneOdd_splitPs', 'rank_of_oneOdd', '@redTan'],
            C+'HomOfDer.lean': ['@red'],
        },
        'UX9': {
            C+'FibLow.lean': ['@fib'], W+'FibreTraces/FibTTrace.lean': ['@fibTorus'],
            D+'OffDiagonalNilpotentRankFour.lean': ['@off_diagonal_nilpotent_rank_four'],
            B+'ExistsPinningElementsOfLocAb.lean': ['@exists_pinning_elements_of_locAb'],
            B+'ExistsMemPinsInsertKerOfPadicCharacter.lean': ['@exists_mem_pins_insert_ker_of_padic_character'],
            B+'ExistsPlaceOverLLocDegMulCardEq.lean': ['@exists_place_over_l_locDeg_mul_card_eq'],
            B+'KrullDimQuotientLeCardOfRadicalParameters.lean': ['@krullDim_quotient_le_card_of_radical_parameters'],
            D+'PotentialModularityTower.lean': ['PotentialModularityTower'],
        },
        'UX10': {
            D+'ClassicalFixedByIwahori.lean': ['@ch_core', '@residual_charpoly_rank_four'],
            W+'SomeInOfLocZero.lean': ['someIn_of_locZero', 'zero_of_allIn', 'allIn_of_chain'],
            C+'AlgHomResUnique.lean': ['@conn'],
            W+'RedIdeal.lean': ['Space.SomeIn', 'Space.AllIn', 'Space.LocZero'],
        },
        'UX11': {
            C+'RestrQ.lean': ['low_desc', '@restrQ'], C+'SmallCo.lean': ['exists_map_eq_algebraMap_padicInt_of_isDvr', 'exists_coef_forall_sub_mem_maximalIdeal_of_isDvr', '@smallCo'],
            C+'SmallExt.lean': ['fin_quot', 'haus', 'key', '@smallExt'],
            AV+'CommutativeAlgebraHeight/ClSub.lean': ['@cl_sub'], C+'ChainDesc.lean': ['ev_pd', 'ev_k', 'ev_poly', '@chainDesc'],
            W+'NearSplit.lean': ['Amb', 'IsDvr', 'Small', 'QPair'],
        },
        'UX12': {
            D+'Gsp4PromodularityCaseTwo.lean': ['last_step', '@proMod_of_pmEx_of_ctx2_of_kPair_of_star'],
            D+'PotentialModularityTower.lean': ['SeedIIAlt', 'PMExAlt', 'PotentialModularityTower', 'ProModAlt'],
            W+'NearSplit.lean': ['Ctx2', 'KPair'], W+'RedIdeal.lean': ['Star'],
        },
    }
    deps = {
        'UX1':['AX5','AX6'], 'UX2':['UX1','AX4','AX6','BR7'], 'UX3':['UX1','BX8','DX1','DX3'],
        'UX4':['UX1','UX2','UX3'], 'UX5':['UX1','BX8','DX3','TW1'],
        'UX6':['BX8','FP1','FP2','FP5','PX1'], 'UX7':['UX6','BX8','DX1','FP7'],
        'UX8':['UX5','UX6'], 'UX9':['UX6'],
        'UX10':['UX5','UX6','UX7','UX8','UX9'], 'UX11':['UX1','UX2'],
        'UX12':[f'UX{i}' for i in range(1,12)],
    }
    classic = {
        'UX1':['UX-CHEB','UX-CFT'], 'UX2':[], 'UX3':['UX-CHEB','UX-CFT'], 'UX4':[],
        'UX5':['UX-CFT'], 'UX6':['UX-COMPLETE'], 'UX7':['UX-CFT'], 'UX8':['UX-DIM'],
        'UX9':['UX-CFT','UX-DIM'], 'UX10':['UX-CONNECT','UX-CURVE','UX-COMPLETE','UX-DIM'],
        'UX11':[], 'UX12':[],
    }
    retained = {k:[] for k in spec}
    retained['UX4']=['UX-H-SEED-II']
    retained['UX9']=['UX-H-PM-FIN']
    retained['UX10']=['UX-H-PM-FIN','UX-H-PM-P1']
    retained['UX12']=['UX-H-SEED-II','UX-H-PMEX']
    main_raw=(HERE/'main.tex').read_bytes()
    texlines=main_raw.splitlines(keepends=True)
    claims=[]
    for cid, sources in spec.items():
        matches=[i for i,line in enumerate(texlines) if re.search(rb'\\begin\{(?:proposition|theorem)\}\['+cid.encode()+b':',line)]
        assert len(matches)==1,(cid,matches)
        start=matches[0]
        end=next(i for i in range(start+1,len(texlines)) if texlines[i].strip()==b'\\end{proof}')
        block=b''.join(texlines[start:end+1])
        title=texlines[start].decode().split(cid+':',1)[1].rsplit(']',1)[0].strip()
        loc={'file':COMPONENT+'/main.tex','line_start':start+1,'line_end':end+1,'sha256':sha(block),'bytes':len(block)}
        links=[source(path,n) for path, names in sources.items() for n in names]
        claims.append({'id':cid,'title':title,
            'status':'Complete readable proof of the stated universal implication, with every listed theorem hypothesis retained.',
            'depends_on':deps[cid],'mathematical_dependencies':deps[cid],
            'classical_inputs':classic[cid], 'remaining_inputs':retained[cid],
            'remaining_bespoke_inputs':retained[cid],
            'component_ledger':COMPONENT+'/provenance.json', 'proof_location':loc,'human_proof':loc,'sources':links})

    frontier=[
        source(D+'PotentialModularityTower.lean','PMExAlt','Retained literal five-clause support producer, including its threshold before all later coefficient rings and all spaces.'),
        source(D+'PotentialModularityTower.lean','SeedIIAlt','Retained theorem premise in UX12; the independent SX producer may install it without altering this universal implication.'),
        source(D+'PromodularityCaseThree.lean','SeedIVAlt','Separate case-III seed, with its prior w,s and universal later-tower quantifiers; not proved here.'),
        source(D+'PromodularityCaseThreeOfLemmas.lean','@promodularity_case_three_of_chain_reduction','Remaining full case-III support realization, including tensor tower, rank-four chain, coefficient descent and chain reduction.'),
        source(D+'CuFinal.lean','main4_alt','Case-III final assembly remains outside UX12, even though shared dimension tools have been proved.'),
        source(D+'IsAut4.lean','SymplecticFourImageDense','Whole two-case interface is not unconditionally supplied by the case-II conditional endpoint.'),
    ]
    registry=classical_registry()
    dump('classical_inputs.json',registry)
    prov={'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.29','component':COMPONENT,
        'commit':PIN,'repository':REPOSITORY,'source_commit':PIN,'source_repository':REPOSITORY,
        'main_tex_sha256':sha(main_raw),'source_files':sorted(files.values(),key=lambda x:x['path']),
        'claims':claims,'retained_frontier':frontier,
        'scope':'Twelve full proofs through actual case-II ProModAlt from literal SeedIIAlt and PMExAlt. Shared space, cone, bounds, components, finite-field curves and original-coefficient return are proved. Case III and incoming automorphic producers remain separate.',
        'validation':{'claim_count':len(claims),'claim_source_links':sum(len(c['sources'])for c in claims),
            'frontier_source_links':len(frontier),'pinned_source_file_count':len(files),
            'all_files_equal_pinned_git_blobs':True,'all_proof_ranges_hashed':True,
            'formal_transitive_dependency_audit':False,'lean_kernel_replay_performed':False}}
    dump('provenance.json',prov)
    dump('source_hashes.json',{'commit':PIN,'repository':REPOSITORY,'files':prov['source_files']})
    dump('source_validation.json',{'schema':'rh-source-validation/1','component':COMPONENT,'commit':PIN,
        'main_tex_sha256':sha(main_raw),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
        **prov['validation'],'method':'Every listed whole file compared byte-for-byte with git show at the fixed commit; every declaration and proof range hashed from exact bytes. No Lean build.'})
    inputs=[
        {'id':'UX-H-SEED-II','status':'Exact retained theorem hypothesis; producer owned independently by SX.',
         'predicate':'SeedIIAlt','used_by':['UX4','UX12'],
         'scope':'For every original Ctx2 datum, every actual Ok/Two/Deep tower and fixed iota, an actual finite-coefficient integral SeedPairAlt exists with InV and the exact root-entry alternative.',
         'sources':[frontier[1]],'not_replaced_by':'Generic potential automorphy or a seed at a different iota, tower or residue field.'},
        {'id':'UX-H-PMEX','status':'Exact retained theorem hypothesis; producer owned independently by QX.',
         'predicate':'PMExAlt','used_by':['UX12'],
         'scope':'For every Fit/Deep T and iota, a threshold precedes every later coefficient ring and every actual Space; supplies one J with fin, p1, seed, pur and aut together.',
         'sources':[frontier[0]],'not_replaced_by':'Finiteness of a generic automorphic set, only fin/seed, or existence for a selected unrelated space.'},
        {'id':'UX-H-PM-FIN','status':'The fin field of the given actual support contract, retained in the universal dimension implication.',
         'used_by':['UX9','UX10'],'scope':'A power of m_B lies in J+m_Lambda B plus the ideal of all local inertia psi_i-1; on the same B/J.'},
        {'id':'UX-H-PM-P1','status':'The p1 field of the given actual support contract, retained in the universal component implication.',
         'used_by':['UX10'],'scope':'Every finite residue field power-series map killing J, local at m_B, with all ordinary character pairs separated on U1 and irreducible generic representation, satisfies literal LocZero.'},
    ]
    prior_components=['symplectic_arithmetic_data','bernoulli_residual_vanishing','bloch_kato_installation',
        'symplectic_local_installation','simultaneous_cohomological_windows','framed_deformation_presentation','symplectic_model_comparison']
    prior=[]
    for dirname in prior_components:
        path=HERE.parent/dirname
        if not path.exists():
            continue
        prior.append({'component':dirname,'files':[{'path':dirname+'/'+n,'sha256':sha((path/n).read_bytes())}
            for n in ['main.tex','provenance.json','closure.json'] if (path/n).is_file()]})
    dump('input_registry.json',{'schema':'rh-input-registry/1','artifact_version':'0.29','component':COMPONENT,
        'commit':PIN,'inputs':inputs,'proved_prior_claims':sorted(set(d for ds in deps.values()for d in ds if not d.startswith('UX'))),
        'prior_component_bindings':prior,
        'theorem_hypotheses':['Original Ctx2 datum and all its original fields and places','One iota fixed before all ambient/point quantifiers',
            'An actual Amb with the prescribed compatible coefficient maps and residue approximation','Actual small KPair and Star on the same ambient K'],
        'classical_registry':COMPONENT+'/classical_inputs.json'})
    closure={'schema':'rh-dependency-closure/1','artifact_version':'0.29','component':COMPONENT,'commit':PIN,
        'main_tex_sha256':sha(main_raw),'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
        'graph':deps,'closed_endpoints':[
            {'claim':'UX4','literal_interface':'deep_tower_residue_chain_exists in its actual case-II scope',
             'retained_bespoke_inputs':['UX-H-SEED-II']},
            {'claim':'UX5','literal_interface':'x2 and the actual arbitrary-coefficient Bounds, with C preceding the chosen later layer',
             'retained_bespoke_inputs':[]},
            {'claim':'UX6','literal_interface':'Actual tower Space and CmplEx, all fields including genB, universal lifts and polynomial lines',
             'retained_bespoke_inputs':[]},
            {'claim':'UX7','literal_interface':'Actual x1 presentation deficit b+2+2d <= a+2s',
             'retained_bespoke_inputs':[]},
            {'claim':'UX10','literal_interface':'Actual residual_charpoly_rank_four and finite-chain component propagation',
             'retained_bespoke_inputs':['UX-H-PM-FIN','UX-H-PM-P1']},
            {'claim':'UX11','literal_interface':'Actual restrQ, universal smallCo and chainDesc, with exact original coefficients',
             'retained_bespoke_inputs':[]},
            {'claim':'UX12','literal_interface':'proMod_of_pmEx_of_ctx2_of_kPair_of_star; full literal ProModAlt for every actual case-II star KPair',
             'retained_bespoke_inputs':['UX-H-SEED-II','UX-H-PMEX']}],
        'same_object_bindings':[
            'Original Omega, odd ell, D, K, V and every given compatible coefficient map',
            'A single fixed iota before every seed, space, support ideal and original-point comparison',
            'The original global representation is changed only by conjugation over the same ambient K',
            'All tower extensions preserve the chosen imaginary quadratic field and label and the required ell-power separating element',
            'The label is chosen first, then the initial tower and its separating g0, and only then the original lattice is normalized at that g0',
            'Original integral ps_i inertia ordering is retained; only residual global characters are relabelled',
            'Actual local decomposition/inertia groups and the chosen flags survive all restrictions',
            'The uniform C precedes the deep layer and all later coefficient enlargements',
            'The PMExAlt threshold precedes every actual Space on a later coefficient ring',
            'All chain, seed, small-pair and support thresholds are met in one coefficient compositum',
            'Every p1 curve has an actual finite residue field, exact Lambda structure, generic irreducibility and every local character-pair separation',
            'The final complete local descent ring has residue exactly k_Lambda; it is not asserted to be a DVR',
            'The final y kills J and returns the actual restricted original pair, not only its semisimplification'],
        'noncircularity':[
            'Tower and residual bridge are built before the automorphic support ideal.',
            'Uniform Ferrero--Washington bounds are chosen before the final layer and seed coefficients.',
            'The actual Space and its completions are constructed without assuming image density or automorphy.',
            'Finite arithmetic cohomology proves the presentation deficit independently of the support contract.',
            'The fin and p1 fields are applied to explicitly constructed loci and curves, not inferred from a desired support conclusion.',
            'The seed clause first gives SomeIn; the component proof upgrades it and transports it to the original point.',
            'No appeal to the downstream IX10 or YX count join occurs in the proof.'],
        'retained_frontier':[a['declaration']for a in frontier],
        'not_claimed':['Unconditional PMExAlt','SeedIIAlt existence within UX itself','SeedIVAlt or the complete case-III chain',
            'Universal SymplecticFourImageDense','Unconditional CountII, CountIII, PointHV, RH or GRH',
            'A single tower or coefficient ring uniform over all original valued points','Full transitive Lean audit or kernel replay'],
        'retirement_candidates':[],
        'partial_target_updates':[{'id':'DA28-SP-03','supplied_by':['UX12'],
            'closed_scope':'Complete actual case-II star-point support realization conditional on literal SeedIIAlt and PMExAlt, including all component and coefficient joins.',
            'remaining_human_scope':'The compound target retains the full actual case-III realization and any independently unsupplied seed/support producers; no whole-target retirement.'}]}
    dump('closure.json',closure)
    dump('remaining_inputs.json',{'component':COMPONENT,'inputs':inputs,'source_frontier':frontier,
        'case_ii_endpoint':'UX12','case_iii_status':'Not reconstructed in this component.'})
    dump('next_targets.json',{'targets':[
        {'id':'UX-next-01','priority':1,'title':'Install the literal five-clause PMExAlt producer',
         'scope':'Supply the actual common J at the uniform coefficient threshold, preserving all five clauses and fixed iota. Apply QX only with its exact retained ordinary-support hypotheses.',
         'sources':[frontier[0]],'consumed_by':['UX12']},
        {'id':'UX-next-02','priority':2,'title':'Close the complete case-III support realization',
         'scope':'Construct the original case-III tensor tower, SeedIVAlt bridge, actual Space/component support, finite coefficient descent and ProModAlt return under their exact source quantifiers.',
         'sources':[frontier[2],frontier[3],frontier[4]],'not_supplied_by':'The complete but specifically case-II UX12 endpoint.'}]})
    locators=[]
    for c in claims:
        locators.append(c['id']+' — '+c['title'])
        locators += ['  '+s['declaration']+' '+s['url']+' range_sha256='+s['range_sha256'] for s in c['sources']]
    locators.append('Retained frontier')
    locators += ['  '+s['declaration']+' '+s['url']+' range_sha256='+s['range_sha256']for s in frontier]
    (HERE/'source_locators.txt').write_text('\n'.join(locators)+'\n')
    own=[p for p in HERE.iterdir()if p.is_file()and p.name not in {'input_manifest.json'}]
    dump('input_manifest.json',{'schema':'rh-component-input-manifest/1','component':COMPONENT,'commit':PIN,
        'files':[{'path':COMPONENT+'/'+p.name,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}for p in sorted(own)],
        'prior_component_bindings':prior,
        'excludes':'Downstream independent reviews and semantic/package audits; no self-hash or mutable root metadata.'})
    print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_links':sum(len(c['sources'])for c in claims),
        'frontier_links':len(frontier),'pinned_files':len(files),'main_tex_sha256':sha(main_raw),
        'provenance_sha256':sha((HERE/'provenance.json').read_bytes()),
        'closure_sha256':sha((HERE/'closure.json').read_bytes())},indent=2))


def classical_registry():
    return {'schema':'rh-classical-input-registry/1','artifact_version':'0.29','component':COMPONENT,
        'inputs':[
            {'id':'UX-CHEB','name':'Chebotarev, including reduced prime progressions',
             'statement':'A prescribed conjugacy class in a finite Galois extension is represented by infinitely many unramified primes, with finite exclusions permitted.',
             'primary_sources':[{'author':'J. S. Milne','title':'Algebraic Number Theory, version 3.08',
                 'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf','location':'Theorem 8.31'}],
             'matching':'UX1 proves compatibility of the independent quadratic ramification/splitting choices; UX3 uses actual completely split auxiliary primes for the finite residual modules.'},
            {'id':'UX-CFT','name':'Finite global and local abelian reciprocity',
             'statement':'Finite unramified abelian extensions are controlled by the ideal class group; locally, abelianized inertia is the profinite unit group and its pro-ell quotient has the stated unit rank and cyclic ell-primary torsion.',
             'primary_sources':[{'author':'J. S. Milne','title':'Class Field Theory, version 4.03',
                 'url':'https://www.jmilne.org/math/CourseNotes/CFT.pdf','location':'Local reciprocity, Chapter I; global reciprocity and existence, Chapter V, Theorems 3.6--3.7 and Example 3.9'}],
             'matching':'Only the finite class-character and actual local unit statements are used. The cohomological and Ferrero--Washington estimates are separately supplied by prior reconstructed claims.'},
            {'id':'UX-COMPLETE','name':'Noetherian completion and formal algebra',
             'statement':'Completion of a Noetherian local ring is faithfully flat; finite modules complete exactly; finite-variable formal power-series rings over a complete Noetherian local coefficient ring are complete Noetherian.',
             'primary_sources':[{'author':'The Stacks Project','title':'Completion for Noetherian rings',
                 'url':'https://stacks.math.columbia.edu/tag/00MC','location':'Lemma 10.97.3'},
                 {'author':'The Stacks Project','title':'Completion for Noetherian rings',
                 'url':'https://stacks.math.columbia.edu/tag/00MA','location':'Lemma 10.97.1'},
                 {'author':'The Stacks Project','title':'Formal power series',
                 'url':'https://stacks.math.columbia.edu/tag/0306','location':'Noetherianness of finite-variable power series'}],
             'matching':'UX6 applies this to A localized at the actual finite-residue point, and proves the universal and polynomial-line comparisons separately.'},
            {'id':'UX-DIM','name':'Krull height, finite-type dimension and completion dimensions',
             'statement':'An ideal generated by h elements has height at most h; finite-type local dimension is bounded by base dimension plus transcendence degree; completion preserves the dimension of a Noetherian local ring and of its quotient.',
             'primary_sources':[{'author':'The Stacks Project','title':'Dimension',
                 'url':'https://stacks.math.columbia.edu/tag/00KD','location':'Krull height theorem and systems of parameters'},
                 {'author':'The Stacks Project','title':'The dimension formula',
                 'url':'https://stacks.math.columbia.edu/tag/02JU','location':'Lemma 29.53.1'},
                 {'author':'The Stacks Project','title':'Permanence of properties under completion',
                 'url':'https://stacks.math.columbia.edu/tag/07NU','location':'Section 15.44'}],
             'matching':'The actual parameter counts d+20C, 2+4s and 2d-d_v+1 are proved in UX8--UX9; these dimension theorems only convert those explicit counts.'},
            {'id':'UX-CONNECT','name':'Grothendieck connectedness for a complete local quotient',
             'statement':'For complete Noetherian A, Y=V(I), and closed Z in Y, Y minus Z is connected when dim Z < min(c,d-1)-cd(A,I), where c is the connectedness dimension of Spec A and d its least component dimension.',
             'primary_sources':[{'author':'The Stacks Project','title':'Application to connectedness',
                 'url':'https://stacks.math.columbia.edu/tag/0ECR','location':'Lemma 52.14.1'}],
             'matching':'UX10 applies this to the regular power-series domain Lambda[[z_1,...,z_a]], whose dimension is a+1, with b defining equations, then constructs the component graph and avoids every explicit bad locus.'},
            {'id':'UX-CURVE','name':'Normalization of a one-dimensional complete domain and Cohen structure',
             'statement':'A one-dimensional complete Noetherian domain has finite normalization, a complete DVR with finite residue extension; in equal characteristic a complete DVR with finite residue field is a one-variable power-series ring over that residue field.',
             'primary_sources':[{'author':'The Stacks Project','title':'Normalization of one dimensional schemes',
                 'url':'https://stacks.math.columbia.edu/tag/0C44','location':'Section 33.41, especially Lemma 33.41.2'},
                 {'author':'The Stacks Project','title':'The Cohen structure theorem',
                 'url':'https://stacks.math.columbia.edu/tag/0C0S','location':'Lemma 10.160.10'}],
             'matching':'UX10 first constructs the actual one-dimensional characteristic-ell prime avoiding all bad ideals. Its normalization gives a finite residue field extension, and finite-field Teichmuller lifts preserve the original Lambda-algebra map.'}
        ],
        'inherited_matched_inputs':[
            {'via':['BX8','DX1','DX3'],'scope':'Actual finite local/global duality, finiteness, Euler and Greenberg--Wiles after all original-field/coefficient transports.'},
            {'via':['TW1'],'scope':'The literal Ferrero--Washington finite-layer rank statement on the exact abelian cyclotomic tower.'},
            {'via':['BR7','AX4'],'scope':'Actual residual Bernoulli-unit vanishing with tame restriction and the original residue field.'},
            {'via':['FP1','FP2','FP5','FP7','PX1'],'scope':'Entry-wise finite prorepresentability, homogeneous formal generators, obstruction-to-relation detection and the elementary finite-monomial proof.'}],
        'not_assumed':['Potential automorphy as an unnamed black box','Generic finiteness in place of PMExAlt.fin or p1',
            'Any uniform seed coefficient bound preceding the tower','An unconditional image-density or count theorem']}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=HERE.parents[1]/'lean-source')
    main(parser.parse_args().repo)
