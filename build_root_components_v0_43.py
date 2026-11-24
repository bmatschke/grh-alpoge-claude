#!/usr/bin/env python3
"""Bind the two root-authored v0.43 chapters to exact pinned source ranges."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'formal_source'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
PREFIX = 'src/Development/AutomorphicArithmetic/'
AV = PREFIX + 'AutomorphicVarieties/'
DENSE = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
ORD = AV + 'HeckeAlgebras/OrdinaryHeckeCharacters/'
BUILD = AV + 'BuildingsResidueChars/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

cache = {}
def source(path, first=1, last=None):
    if path not in cache:
        data = (SOURCE / path).read_bytes()
        pinned = subprocess.check_output(['git', '-C', str(SOURCE), 'show', PIN + ':' + path])
        assert data == pinned, path
        cache[path] = data
    data = cache[path]
    lines = data.splitlines(keepends=True)
    last = len(lines) if last is None else last
    assert 1 <= first <= last <= len(lines), (path, first, last, len(lines))
    part = b''.join(lines[first-1:last])
    return {'path': path, 'line_start': first, 'line_end': last,
            'file_sha256': sha(data), 'sha256': sha(data),
            'range_sha256': sha(part), 'range_bytes': len(part),
            'verified_equal_to_pinned_git_blob': True,
            'url': 'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/' + PIN + '/' + path + f'#L{first}-L{last}'}

def tc(a, b=None):
    return source(DENSE + 'TClParts.lean', a, b)

def pb(a, b=None):
    return source(ORD + 'PlaceBetween.lean', a, b)

def dc(a, b=None):
    return source(ORD + 'DecompU.lean', a, b)

CFD = {
 1: ([], [tc(14,21)]),
 2: ([], [tc(22,43)]),
 3: (['CFD1','CFD2'], [tc(44,103)]),
 4: (['CFD1','CFD3'], [tc(104,124)]),
 5: ([], [tc(125,153)]),
 6: (['CFD5','FNL12'], [tc(208,224),tc(294,313),source(DENSE+'UnitaryPointProperties.lean',29,47)]),
 7: (['OST26','OST27','ASP4','ASP5'], [tc(225,251),tc(263,293)]),
 8: (['CFD6','CFD7','OST5','OST6','ASP6'], [tc(175,180),tc(252,262),tc(294,298)]),
 9: (['CFD4','CFD5','CFD6','CFD7','OST26'], [tc(271,293),tc(314,328)]),
 10: ([], [tc(154,174)]),
 11: (['CFD8','CFD10','ASP6','ASP10'], [tc(154,174),tc(329)]),
 12: (['CFD7','CFD9','CFD11','FNL16','ASP13'], [tc(329),source(DENSE+'UnitaryPointProperties.lean',48)])
}

ADP = {
 1: (['FNL2','FNL3','FV4','FV5','FV6','FV7','FV8'], [source(BUILD+'ExistsCompactFundamentalSetUnitary.lean'),source(BUILD+'ExistsNondegenerateRightInvariantFormOfCompactQu.lean')]),
 2: (['ADP1','FNL3'], [source(PREFIX+'DivisorFrames/FiniteDimensionalAutomorphicFormsUnitaryOfTypeLe.lean'),source(BUILD+'AdmissibleEquivariantFormsRepresentation.lean')]),
 3: (['ADP1','ADP2','PKT5','PKT6'], [source(BUILD+'MemISupIrreducibleOfAdmissibleUnitary.lean')]),
 4: (['ADP1','ADP3','PKT10'], [source(BUILD+'MemISupAutomorphicRepsOfInvariantForm.lean')]),
 5: (['ADP4'], [source(BUILD+'ExistsEquivariantProjectionsOfSumIrreducible.lean'),dc(20,65)]),
 6: (['FNL2','FNL4','FNL5','FNL6'], [pb(73,185),source(AV+'HeckeAlgebras/IsTheta.lean',186,204)]),
 7: (['ADP6','FNL2'], [pb(186,220),pb(273)]),
 8: (['ADP6','ADP7'], [pb(221,272),pb(273)]),
 9: (['ADP6','ADP7','ADP8'], [pb(273)]),
 10: (['ADP7','FNL7','FNL8','FNL9'], [source(BUILD+'EventuallyMemHeckeLevelAndIwahoriCongruence.lean'),dc(168)]),
 11: (['ADP5','ADP6','ADP7','ADP8','ADP10'], [dc(66,167)]),
 12: (['ADP10','ADP11'], [dc(168),source(AV+'HeckeAlgebras/IsTheta.lean',206,209),source(DENSE+'UnitaryPointProperties.lean',29)])
}

SCOPES = {
 'classical_parts_v43': {
  'endpoint':'Full original UpperTheory.V.Hi.clParts_alt, and its arbitrary-predicate-on-parts refinement.',
  'original_inputs_retained':['Original HSet, H.Ax, complete local coefficient ring, theta and arithmetic point, fixed iota, original weight and basis, IsSpec, and actual supplied AutomorphicHeckeSet.', 'Exact level K, depth e and original normalized uzC; source norm-one generalized eigenspace condition.'],
  'not_asserted':['Construction of AutomorphicHeckeSet or the Galois-decorated PartAltAlt supplier.', 'Nonzero original Hecke blocks or same-ideal Hida/HasAut endpoints.'],
  'method':'Finite averaging on nonnormal finite-index stabilizers, commuting compact scalar-profile refinement, and polynomial generalized-eigenspace projections.'
 },
 'automorphic_decomposition_v43': {
  'endpoint':'Full original UpperTheory.V.Hi.formU and UpperTheory.V.Hi.decompU on their stated original inputs.',
  'original_inputs_retained':['Original identity-form definite unitary group and rational quotient, original fixed iota and basis equivalence, literal infRep and toForm.', 'Original integral type with open kernel in decompU, original away level and Iwahori depth; no type-openness assumption for formU.'],
  'not_asserted':['Arithmetic/Galois decoration of a nonzero YOf, partX_alt/partU_alt, or AutomorphicHeckeSet.', 'Same-ideal Hida density, support or all-level automorphy without their remaining inputs.'],
  'method':'Actual compact quotient and positive invariant form, checked algebraic semisimplicity and finite multiplicity, exact bidual scalarization, and globally equivariant finite projections.'
 }
}

for component, prefix, spec in [('classical_parts_v43','CFD',CFD),('automorphic_decomposition_v43','ADP',ADP)]:
    folder = ROOT / component
    data = (folder/'main.tex').read_bytes()
    lines = data.splitlines(keepends=True)
    claims = []
    for number, (deps, refs) in spec.items():
        cid = prefix + str(number)
        first = next(i+1 for i,x in enumerate(lines) if x.strip() == ('% BEGIN '+cid).encode())
        last = next(i+1 for i,x in enumerate(lines) if x.strip() == ('% END '+cid).encode())
        block = b''.join(lines[first-1:last])
        title = re.search(r'\\paragraph\{'+cid+r'\. (.*)\}\n',block.decode())[1]
        title = re.sub(r'\\texttt\{([^{}]*)\}',r'\1',title).replace('\\_','_')
        claims.append({'id':cid,'title':title,'introduced_in':'0.43','classification':'B',
          'status':'Complete human proof in the exact stated scope',
          'depends_on':deps,
          'proof_location':{'file':component+'/main.tex','label':'claim:'+cid,'line_start':first,'line_end':last,'sha256':sha(block),'file_sha256':sha(data),'bytes':len(block)},
          'sources':refs})
    ledger={'schema':'rh-human-component-provenance/1','artifact_version':'0.43','date':'2026-11-23',
      'component':component,'source_commit':PIN,'main_tex_sha256':sha(data),**SCOPES[component],
      'claims':claims,'no_lean_replay':True}
    write(folder/'provenance.json',ledger)
    report=[component+' — version 0.43','23 November 2026','',SCOPES[component]['endpoint'],'',SCOPES[component]['method'],'','SCOPE AND INPUTS']
    report+=SCOPES[component]['original_inputs_retained']+['','REMAINING BOUNDARY']+SCOPES[component]['not_asserted']+['','PROOF CLAIMS']
    for c in claims:
        report += [c['id']+': '+c['title'],'Dependencies: '+', '.join(c['depends_on'])]
        report += ['  '+s['path']+f":{s['line_start']}–{s['line_end']}" for s in c['sources']]
    report += ['','Source pin: '+PIN,'Every cited source file equals the pinned git blob; full-file and inclusive-line-range hashes are recorded.','Independent mathematical review is recorded separately and bound to the exact proof bytes.','No kernel replay, Lean build or global RH/GRH completion assertion.']
    (folder/'report.txt').write_text('\n'.join(report)+'\n')
    print(json.dumps({'component':component,'claims':len(claims),'main_sha256':sha(data)}))
