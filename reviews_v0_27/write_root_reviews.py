#!/usr/bin/env python3
"""Bind root's completed mathematical reviews to frozen texts and source bytes.

The mathematical findings below are recorded reviews, not generated proof
certificates. The executable part only verifies their byte/source bindings.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / 'lean-source'
OUT = ROOT / 'reviews_v0_27'
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'

NOTES = {
    'symplectic_arithmetic_data': {
        'AX1': 'Checked the original host/case arithmetic, CRT conductor and order factors, parity and the inclusion of the actual exceptional set in the host set before residual vanishing is invoked.',
        'AX2': 'Checked the primitive dyadic character, its exact order/conductor and quantitative bound. The required roots in O are a hypothesis, not automatic coefficient content.',
        'AX3': 'Checked choices on the original closure and places, the cyclotomic/Frobenius and s0 requirements, and the factorial-power prime-to-ell limit including its conclusion for all actual complete-local matrix lifts.',
        'AX4': 'Checked both-character residual vanishing, exact inertia/kernel relative index and passage back to the actual residue field. No unrestricted coefficient-field substitution is used.',
        'AX5': 'Checked both literal OfCase constructions, exact nII/nIII and residual Good fields. The given coefficient ring must contain the specified dyadic roots; the later finite extension and normalized return are handled by AX10/SP8/RV1.',
        'AX6': 'Checked the facts interface for arbitrary Good D, not merely the constructed example: continuity, residual separation, s0 eigenvalues, prime-to-ell normalization and the hEl diagonal-difference unit.',
        'AX7': 'Checked the literal common level/order and all KillsMu and power assertions with the prescribed integer exponents; no larger conductor is silently substituted.',
        'AX8': 'Checked full actual OnComp/PtOn specialization through the domain and diagonal base point. The divided-eigenvalue argument retains strict residual bounds, continuous ordinary characters, their pairing and noncyclotomic ratios on every indicated open subgroup.',
        'AX9': 'Checked actual Level, multiplier/IsCycWt and DualTw for the original symplectic form. UnlAll is transported to every place above ell and SafeRA follows from ell dividing the level, without invoking a potentially crystalline alternative.',
        'AX10': 'Checked G1 with literal ImageDense used only for Fin0/NoEnd and one common embedding before all irreducible points. The full-span Irr condition implies the needed invariant-subspace irreducibility. Permitted coefficient extension and exact normalized return remain explicit.'
    },
    'symplectic_local_installation': {
        'DX1': 'Checked transport to original decomposition groups, coefficient twists/cup products and the literal normalized-duality projection. Milne ADT I.5.1 explicitly uses the truncated Euler formula even at 2; high-degree real-place vanishing is odd-only. The finite-to-lattice-to-rational cohomology passage uses finite Mittag-Leffler systems, bounded cochains and the dual codifferent correctly.',
        'DX2': 'Checked the explicit continuous permutation-module cocycle and injective evaluation for every open subgroup. Finite Z1 follows from finite H1 and coboundaries, proving actual global and local PhiCond.',
        'DX3': 'Checked the modified finite Poitou–Tate sequence for arbitrary local submodules and nonfree finite coefficients. The framed H1 and obstruction sequences are derived from their cochain quotient definitions. Prime-to-ell inertia averaging, cyclic inflation and the original Euler formulas give the exact framed identity.',
        'DX4': 'Checked every original Nums quantifier, all ten adjoint directions and exact weights. Conjugation parity kills twisted-dual invariants in even weights, the chosen sigma excludes cyclotomic odd roots, and Good.xvan plus framed normalization kills the actual odd-root framed space.',
        'DX5': 'Checked integral representability by actual polynomial equations, formal-torus homogeneity and all complete-local targets. Finite O-lattice capture identifies the characteristic-zero completed deformation functor. The least initial relation contradiction proves smoothness from unobstructedness; projections return satSq to the actual graded subalgebra. IsCompl and kernel annihilation use the original augmentation and Noetherian local completion.',
        'DX6': 'Checked the actual ordinary spectral flag over every augmented Artin E-algebra, isotropy, the unique lower-unipotent flag chart and the upper-triangular deformation functor. Each positive root has H0=H2=0, so continuous defects can be corrected. The count 2+8+4=14 keeps actual representations, not conjugacy classes. Weight -Psi is an infinitesimal flag coboundary with one integral denominator; weight zero is unramified.',
        'DX7': 'Checked the full inertia-kernel equation on every deformation, the central finite cyclic quotient and its splitting over Zhat. Averaging and symplectic correction are performed only over E, where division by the inertia order is valid. The six-dimensional Cayley slice and four-dimensional GL2 centralizer give an actual equivariant formal functor equivalence, including continuity of every Frobenius value.',
        'DX8': 'Checked the completed coproduct on the same coefficient ring, arbitrary local tuples and unique maps, and every rho/eqs/hom/at0/smooth field of literal LocBase. The combined parameter count is 14+10|Sb| with exact weights. No entire BlochKatoLocal or CohomologyHyp record is inferred.'
    },
    'symplectic_model_construction': {
        'MX1': 'Checked the original global quotient, all-place UnrT equivalence, actual polynomial local equations and domain/base-point OnComp witnesses. The source coefficient ring and local maps are retained.',
        'MX2': 'Checked all five kill-inertia local-condition axioms. Small-extension lifting uses finite prime-to-ell inertia averaging and cyclic inflation for the actual quotient, with finite coefficient modules and the required normality/triviality.',
        'MX3': 'Checked FP8 is applied to the literal frame, coefficient algebra, local conditions and adjoint weight spaces, giving exact relative variable/relation counts. PhiCond, Nums and LocBase remain explicit until DX substitution.',
        'MX4': 'Checked the finite Taylor-jet identification between graded and complete rings, the relative cover over the actual local base, and integral lifting of derivations. Only a rational chart is claimed.',
        'MX5': 'Checked homogeneous independent cuts and formal implicit substitution. Taking the kernel of the separately constructed characteristic-zero chart gives a domain; saturated cotangent control ensures all relevant integral derivations descend to it.',
        'MX6': 'Checked six root cuts using actual dual-number conjugations and frame directions, the original J signs, tangent independence and the exact normalized block entries. The hEl condition uses the specific residual unit.',
        'MX7': 'Checked R/S/pi, exact homogeneous equations and dimensions, actual ru and all local OnComp witnesses using the same domain. Origin and weight assertions include every preimage of every entry.',
        'MX8': 'Checked generation through the two precise universal properties for every IsCO target. It does not substitute topological density for the source equality-of-algebra-maps assertion.',
        'MX9': 'Checked every original Selmer cocycle gives an O-valued derivation of exact weight -Psi, not merely an E-valued tangent. All cuts and the domain kernel are killed; reduction modulo a yields the required (2,0) and (3,1) entry identities for every preimage.',
        'MX10': 'Checked coverage of every Model field and the exact Good/PhiCond/Nums/LocBase implication. DX2/DX4/DX8 have been independently read and match its actual arithmetic hypotheses, giving Good D -> Nonempty Model D without a full CohomologyHyp premise. Image-density, actual irreducible rigidity, catalogue and final counts remain separate.'
    }
}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def sha(path):
    return digest(path.read_bytes())

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

parser = argparse.ArgumentParser()
parser.add_argument('component', choices=NOTES)
parser.add_argument('--expected-main-sha256', required=True)
args = parser.parse_args()
component = args.component
main = ROOT / component / 'main.tex'
assert sha(main) == args.expected_main_sha256
ledger = json.loads((ROOT / component / 'provenance.json').read_text())
assert ledger['commit'] == PIN
assert {c['id'] for c in ledger['claims']} == set(NOTES[component])
sources = [s for c in ledger['claims'] for s in c['sources']]
paths = sorted({s['path'] for s in sources})
proc = subprocess.run(['git', '-C', str(REPO), 'cat-file', '--batch'],
                      input=('\n'.join(PIN + ':' + p for p in paths) + '\n').encode(),
                      capture_output=True, check=True)
cache = {}
offset = 0
for path in paths:
    end = proc.stdout.index(b'\n', offset)
    header = proc.stdout[offset:end].split()
    assert header[1] == b'blob'
    n = int(header[2])
    raw = proc.stdout[end + 1:end + 1 + n]
    offset = end + 2 + n
    assert raw == (REPO / path).read_bytes()
    cache[path] = raw
assert offset == len(proc.stdout)
for source in sources:
    raw = cache[source['path']]
    assert digest(raw) == source['sha256']
    piece = b''.join(raw.splitlines(keepends=True)[source['line_start'] - 1:source['line_end']])
    assert digest(piece) == source['range_sha256']
for claim in ledger['claims']:
    loc = claim['proof_location']
    raw = (ROOT / loc['file']).read_bytes()
    piece = b''.join(raw.splitlines(keepends=True)[loc['line_start'] - 1:loc['line_end']])
    assert digest(piece) == loc['sha256'], claim['id']

validation = {
    'result': 'PASS', 'component': component, 'commit': PIN,
    'main_tex_sha256': sha(main), 'source_ranges_checked': len(sources),
    'source_files_equal_to_pinned_git_blobs': len(paths),
    'human_proof_ranges_checked': len(ledger['claims']),
    'scope': 'Mechanical byte/source binding of an independently recorded mathematical review; not a formal proof check.'
}
dump(OUT / (component + '_root_source_validation.json'), validation)
record = {
    'schema': 'rh-independent-mathematical-review/1', 'version': '0.27',
    'reviewer': '/root', 'author_is_reviewer': False, 'result': 'PASS',
    'reviewed_file': component + '/main.tex', 'sha256': sha(main),
    'claim_ids': list(NOTES[component]),
    'reviewed_metadata': {component + '/' + name: sha(ROOT / component / name)
                          for name in ['provenance.json', 'closure.json']},
    'mathematical_checks': NOTES[component],
    'resolved_findings': [
        'The release description distinguishes the given coefficient ring with sufficient roots from the permitted finite extension and normalized coefficient return.',
        'The full Hodge/adjoint producer of actual irreducible rigidity remains a separate continuation; the Model constructor does not supply it.'
    ],
    'unresolved_findings': [],
    'scope': 'Independent human mathematical and literal-interface review, with named classical leaves and retained arithmetic hypotheses. No kernel replay or completion claim for RH/GRH.',
    'source_validation': component + '_root_source_validation.json'
}
dump(OUT / (component + '_root_review.json'), record)
text = ('INDEPENDENT MATHEMATICAL REVIEW — VERSION 0.27\n'
        + component + '\nReviewer: /root\nResult: PASS\n'
        + 'Main SHA256: ' + sha(main) + '\n\n'
        + '\n\n'.join(k + ': ' + v for k, v in NOTES[component].items())
        + '\n\nNo unresolved finding. Classical leaves and exact conditional scopes remain explicit.\n'
          'The accompanying source validation binds this review to bytes; it is not a formal proof.\n')
(OUT / (component + '_root_review.txt')).write_text(text)
print(json.dumps(validation, indent=2))
