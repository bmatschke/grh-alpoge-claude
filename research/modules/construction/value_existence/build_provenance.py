#!/usr/bin/env python3
"""Rebuild exact VE locators from the pinned Git objects (read-only)."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=ROOT.parents[1] / 'lean-source')
args = parser.parse_args()
REPO = args.repo.resolve()
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
TF = 'src/Formalism/LocalToGlobal/GroupLattices/TiedFamilies/'
CM = 'src/Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/'
BR = 'src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/RationalRealBlocks/'
AM = 'src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/'
cache = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def source(path, name, declaration=None, role='proof'):
    if path not in cache:
        raw = subprocess.check_output(['git', '-C', str(REPO), 'show', COMMIT + ':' + path])
        if (REPO / path).is_file():
            assert (REPO / path).read_bytes() == raw, path
        cache[path] = raw
    raw = cache[path]
    lines = raw.splitlines(keepends=True)
    text = [line.decode().rstrip('\r\n') for line in lines]
    pattern = re.compile(r'^(?:private )?(?:noncomputable )?(?:theorem|lemma|def|structure|abbrev) ' + re.escape(name) + r'(?:\s|\{|\(|:)')
    hits = [i for i, line in enumerate(text) if pattern.search(line)]
    assert len(hits) == 1, (path, name, hits)
    start = hits[0]
    stop = start + 1
    while stop < len(lines) and not re.match(r'^(?:(?:private |noncomputable )?(?:theorem|lemma|def|structure|abbrev)|variable|namespace|section|end|open|attribute)\b|^@\[', text[stop]):
        stop += 1
    while stop > start + 1 and (not text[stop - 1].strip() or text[stop - 1].startswith('set_option ')):
        stop -= 1
    return {
        'path': path, 'declaration': declaration or name,
        'line_start': start + 1, 'line_end': stop,
        'sha256': sha(raw), 'range_sha256': sha(b''.join(lines[start:stop])),
        'url': f'{URL}/blob/{COMMIT}/{path}#L{start+1}-L{stop}',
        'first_line': text[start], 'declaration_lines_within_range': [start + 1],
        'role': role, 'verified_equal_to_pinned_git_blob': True,
    }

def tf(file, name, role='proof', namespace='Formalism.L2.G.'):
    return source(TF + file + '.lean', name, namespace + name, role)

def cm(file, name, role='proof'):
    return source(CM + file + '.lean', name, 'Formalism.L2.G.Cmp.' + name, role)

def actual(name, role='proof'):
    return source(AM + 'ExistsEmbeddingOfRingTie.lean', name, 'GlobalTheory.Mem.LocalPack.Test.' + name, role)

specs = [
    ('VE1', 'Explicit even and odd coefficient-field block polynomials',
     'The signed integral duality of CS2 and the formulas det(M)^(-e) f(M^(-1)X), det(M)^(e*) f*(M^transpose X) prove BlockRationalityField and its actual place specialization without a residual block-rationality assumption.',
     ['CS2', 'SF1'], [
         source(BR+'Bridge.lean','s1','PI.BlockRatReal.UnitaryGroupMassFormula.s1'),
         source(BR+'Bridge.lean','s2','PI.BlockRatReal.UnitaryGroupMassFormula.s2'),
         source(BR+'NuOfAntitone.lean','evenStep','PI.BlockRatReal.UnitaryGroupMassFormula.evenStep'),
         source(BR+'MapDetGenM.lean','oddStep','PI.BlockRatReal.UnitaryGroupMassFormula.Odd.oddStep'),
         source(BR+'AntitoneStar.lean','stmt_of','PI.BlockRatReal.stmt_of'),
         actual('block_rational'), tf('BlockRationalityField','BlockRationalityField','input_definition'),
         tf('BlockRationalityField','blkRatRec_of_stmt')], 'derived_simplification'),
    ('VE2', 'Tensor the rational block values and recover all representative values',
     'Finite tensor products of the block polynomials, followed by finite sums and negatives, prove EvRatRep for supplied Forms0 rational values.',
     ['VE1'], [tf('TieEvR','BlockRational','input_definition'), tf('TieEvR','evRat_gen'), tf('TieEvR','evRat_of_blocks'), tf('TieEvR','evRatRep_rec')], 'faithful_translation'),
    ('VE3', 'Rational unitary transport and coefficient-field level characters',
     'The exact even/odd conjugated matrices define an action preserving VtupR; rational level-zero characters lift the level scalar, and r_kappa*rho(h)Q_c proves EvRatPt.',
     ['VE2', 'SF1'], [cm('NatActRVtupR','natActR_VtupR'), cm('NatActRVtupR','vtupStab'),
         cm('CastGLSymmBc','tPos','input_definition'), cm('CastGLSymmBc','blkLL','input_definition'),
         cm('CastGLSymmBc','unit_of_std'), cm('CastGLSymmBc','blk_hAt'), cm('CastGLSymmBc','evC_blk'),
         tf('ChiMemSubfield','chi_mem_subfield'), tf('ChiMemSubfield','chiRatAll_rec'), cm('NatActRVtupR','evRatPt_of')], 'derived_simplification'),
    ('VE4', 'Finite adelic insertion constructs all required point presentations',
     'The split unitary section above p and identity elsewhere give PtEx. Removing the same section from an adele gives PtAll and AwayEx under the supplied actual class and level descriptions.',
     ['LI3', 'LI5', 'SF7', 'CR3'], [tf('EqOneOfPh','LocGood','input_definition'),
         tf('EqOneOfPh','sec',namespace='Formalism.L2.G.LocGood.'), tf('EqOneOfPh','isPt_sec',namespace='Formalism.L2.G.LocGood.'),
         tf('EqOneOfPh','away_mem',namespace='Formalism.L2.G.LocGood.'), tf('EqOneOfPh','ptEx_of'), tf('EqOneOfPh','ptAll_of'), tf('EqOneOfPh','awayEx_of'),
         tf('TiePtRec','ptEx_rec'), tf('TiePtRec','ptAll_rec'), tf('TiePtRec','awayEx_rec')], 'derived_simplification'),
    ('VE5', 'The point ambiguity is in the kernel of the level character',
     'Two points for the same local lattice tuple differ by a full-level element with character one. Basis-span equality gives local integrality of a matrix and its inverse; Joint0 gives the same level; the good-prime exclusion kills the supported character.',
     ['VE4', 'CR3', 'SF6'], [tf('TiePtOne','LocHyp','input_definition'), tf('TiePtOne','ptOne_of'),
         tf('TiePtOneRec','locHyp_locAt'), tf('TiePtOneRec','bad_notOver'), tf('TiePtOneRec','ptOne_rec'),
         tf('TiePtRec','sameUloc_of_joint'), tf('TiePtC','hypT_C'), tf('TieExC','ptOne_C')], 'faithful_translation'),
    ('VE6', 'One rational polynomial works for every basis and representative',
     'Adelic extension of the supplied global form, rational transport, PtEx and character-kernel point uniqueness imply literal ValEx, including all universal presentation quantifiers.',
     ['VE3', 'VE4', 'VE5'], [tf('ChiMemSubfield','adExt_rec'),
         cm('NatActRVtupR','AdExt','input_definition'), cm('NatActRVtupR','PtOne','input_definition'), cm('NatActRVtupR','EvRatPt','input_definition'),
         cm('NatActRVtupR','valEx_of'), cm('NatActRVtupR',"valEx_of_rep'"), tf('ChiMemSubfield','ex_rec'), tf('TieExC','ex_C'), tf('TieExC','ex_C_blk')], 'faithful_translation'),
    ('VE7', 'Elementary polynomial separation makes the comparison unique and linear',
     'Every invertible block tuple is a frame-coordinate tuple. Multiplication by the product of generic determinants proves evaluation injectivity, hence ValUniq and the literal semilinear cmpL without an additional existence premise.',
     ['VE4', 'VE6'], [tf('IsUnitDetBlockPreimage','eq_zero_of_blocks'), tf('IsUnitDetBlockPreimage','cRev_spec'),
         tf('IsUnitDetBlockPreimage','zAt_frameOf'), tf('IsUnitDetBlockPreimage','evC_inj'), tf('IsUnitDetBlockPreimage','evInj_rec'),
         cm('ValUniqOf','valUniq_of'), cm('CmpLApply','IsVal','input_definition'), cm('CmpLApply','ValEx','input_definition'),
         cm('CmpLApply','cmpL'), cm('CmpLApply','cmpC_tie')], 'derived_simplification'),
    ('VE8', 'Supply every field of the actual comparison hypotheses',
     'VE1-VE7 supply values and point properties; LI supplies the original positions and inverse away character; CR and CS supply rank, exact integrality and integral span. This proves comparison_statements and exists_isConcrete under their supplied global form/level premises, with no residual ValEx.',
     ['VE6', 'VE7', 'LI7', 'LI8', 'CR6', 'CS9'], [tf('CmpHyp0P','CmpHyp0P','output_definition'),
         tf('TieAll','CmpLeft','intermediate_definition'), tf('TieAll','CmpLeft.core'),
         tf('TieAll','CmpLeft.toHyp0P'), actual('comparison_statements'), actual('exists_isConcrete')], 'faithful_translation'),
    ('VE9', 'Construct the concrete comparison from the exact global record hypotheses',
     'For supplied D7, LevelData, Forms0, StdTied, Joint0, rational level-zero characters and companion ideals, every supplied scale produces the literal recC with Ce=1, local identifications, characters, ranks and a concrete comparison. Its integral image spans the actual target M at every good place.',
     ['VE8', 'SF7', 'CR6', 'LI8'], [actual('exists_concrete_of_record'),
         actual('forms_and_basis','related_scope'), actual('isConcrete_record_iff','record_transport')], 'faithful_translation'),
    ('VE10', 'Actual true-column concrete comparison from the direct Forms0 construction',
     'For the actual I.rec7 datum with supplied Ok/Pins/Laws/Later and initial decorated-point realization, FC19 constructs every global-record premise of VE9. Every supplied scale therefore gives the concrete comparison with Ce=1 and exact O_w-span(c(global forms lattice))=M at each good place; no full terminal FormsTiedSym/ColsTiedSym is used.',
     ['VE9', 'FC19'], [actual('exists_concrete_of_record'), actual('forms_and_basis','downstream_consequence_not_used'), actual('isConcrete_record_iff','record_transport')], 'derived_simplification'),
    ('VE11', 'Actual comparison with the decorated-realization premise discharged',
     'For the supplied arithmetic host and actual true-column Ok/Pins/Laws/Later, DR3 supplies every initial decorated realizer required in VE10. For every scale, the constructed recC has Ce=1 and exact O_w-span(c(global forms lattice))=M at every good place, without a separate point-realizability or stronger rational-genus hypothesis.',
     ['VE10', 'DR3'], [actual('exists_concrete_of_record'),
         source('src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsAdelicPointDecoratedLatticeAllTwists.lean', 'exists_ptOf_twists', role='actual_true_column_prime_conditions'),
         source('src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ValuedLtOfMem.lean', 'exists_isPtOf_cm', role='realization_interface_supplied_by_DR3')], 'derived_simplification'),

]

assumptions = [
    'The actual global form and level records are supplied unless another component explicitly constructs them; D7/Forms0/Joint0 are not inferred from ranks.',
    'The same original coefficient embeddings and odd-position involution are retained.',
    'The earlier integral duality CS2 is used independently of its later ValEx-dependent comparison claims.',
    'Polynomial separation over an infinite field and the finite restricted-product description of finite adeles are classical background.',
    'No Lean build or independent kernel replay is asserted.',
]
claims = [dict(id=i, title=t, statement=s, status=status, mathematical_status='proved_under_explicit_hypotheses',
               depends_on=deps, assumptions=assumptions, introduced_in='0.14',
               proof_location={'file':'value_existence/main.tex','expanded':'value_existence/report.txt','section':i}, sources=sources)
          for i,t,s,deps,sources,status in specs]
files = [dict(path=p, sha256=sha(raw), bytes=len(raw), lines=len(raw.splitlines()),
              url=f'{URL}/blob/{COMMIT}/{p}', verified_equal_to_pinned_git_blob=True)
         for p,raw in sorted(cache.items())]
payload = {
    'schema':'rh-component-provenance-v1','artifact_version':'0.14','repository':URL,'commit':COMMIT,
    'claims':claims,'source_files':files,
    'input_boundaries':[
        'VE9 is the conditional global-record theorem; VE10 applies the direct FC19 source of Forms0, levels, characters and companion geometry to the actual true-column record. VE11 uses DR3 to discharge the independent initial-realizer premise, retaining the supplied arithmetic host and Ok/Pins/Laws/Later.',
        'The separate block-rationality, ValEx, point-presentation and comparison-algebra premises are now proved under that global record.',
        'Metrics, spectral estimates, cohomological windows and the final prime-sum theorem remain separate.'
    ],
    'validation':{'claim_count':len(claims),'source_files':len(files),'source_links':sum(len(c['sources'])for c in claims),
                  'pinned_bytes_verified':True,'lean_build':False,'kernel_replay':False},
    'artifact_hashes':{name:sha((ROOT/name).read_bytes())for name in ['main.tex','report.txt']},
}
(ROOT/'provenance.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source_locators.txt').write_text('\n\n'.join(f"{c['id']} {s['declaration']}\n{s['path']}:{s['line_start']}-{s['line_end']}\n{s['url']}" for c in claims for s in c['sources'])+'\n')
prior = json.loads((ROOT.parent/'history/version_0_13/next_source_targets.json').read_text())
next_targets = []
for t in prior['targets']:
    if t['priority_group']==1 and 'formsTiedSym_std' in t['declaration']:
        entry=dict(t)
        entry['remaining_human_scope']='Supply the simultaneous global form record and its actual true-column geometric/level compatibilities. VE1-VE9 now remove separate block-rationality and ValEx premises; CV/FC record the newly reconstructed chart and form portions.'
        next_targets.append(entry)
(ROOT/'next_targets.json').write_text(json.dumps({'version':'0.14','commit':COMMIT,'status':'Conditional-input continuation map; no theorem asserted here.','targets':next_targets},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(payload['validation']))
