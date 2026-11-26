#!/usr/bin/env python3
"""Rebuild the KB1--KB8 source and proof ledger; check pinned Git bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=HERE.parents[1] / 'lean-source')
REPO = parser.parse_args().repo
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
BASE = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
G = AV + 'GeneratorCountTuples/'
T = AV + 'TensorHomCubes/'
P = AV + 'PublishedTheorems/'
F = 'src/Formalism/GaloisCohomology/Statement.lean'
V = 'src/ReciprocityTheory/GaloisValuations/'
B = 'src/Development/AbelianVarietyTheory/Proofs/FoundationProofs/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}


def source(path, spelling, role='exact statement or definition matched by this human proof'):
    if path.startswith(P):
        role = 'source publication-interface definition; this chapter uses its canonical specialization, not every arbitrary-Plus quantifier'
    elif 'KBridgeOfKPublished' in path:
        role = 'source interface package for context; the actual existential KBridge is constructed independently in KB4'
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        found = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if found:
            starts.append((n, found.group(1)))
    matches = [n for n, name in starts if name == spelling]
    if len(matches) != 1:
        raise ValueError((path, spelling, matches))
    start = matches[0]
    end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b''.join(lines[start - 1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                   'lines': len(lines), 'url': f'{BASE}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{BASE}/blob/{PIN}/{path}#L{start}-L{end}',
            'role': role, 'verified_equal_to_pinned_git_blob': True}


spec = {
 'KB1': {
  F: ['Above', 'LData', 'scalRep', 'zlTw'],
  V+'Global.lean': ['cycZ', 'continuous_cycZ', 'cycMod', 'NS', 'GS', 'toGS', 'locHom', 'unramOutside_iff'],
  V+'SeparatedDvrSecondCohomologyMem.lean': ['contMaps', 'ContAction', 'Z2', 'd1', 'B2', 'H2', 'Cn', 'dn'],
  G+'CardH2QuotientLeSha.lean': ['UpperTheory.V.K.card_H2_quotient_le_sha'],
 },
 'KB2': {
  G+'LemmaK.lean': ['HasMuQ'],
  P+'KArith.lean': ['KFinGen', 'KBorelRank', 'KDwyerFriedlander'],
  T+'IsAcyclicSpace.lean': ['PlusOf', 'Plus', 'PlusOf.K'],
 },
 'KB3': {
  T+'StabDirectedSystem.lean': ['padMat', 'stab', 'GLinf', 'toGLinf', 'Unimodular', 'StableRangeLe', 'grpH', 'grpHMap'],
  T+'DedekindSR.lean': ['exists_crt_indicator', 'unimod_iff', 'UpperTheory.V.KL.dedekindSR'],
  T+'SimplexFace.lean': ['IsHurewicz', 'ArlAdm', 'arlL', 'arlR'],
  T+'IsAcyclicSpace.lean': ['BG', 'singH'],
  P+'KAcyclicHomology.lean': ['KPlusExists', 'KAcyclicHomology', 'KMilnor', 'KHurewicz', 'KStability'],
  G+'Bridge.lean': ['cOne', 'two_mul_cOne', 'cOne_le'],
  G+'TorsBoundPow.lean': ['HGL'],
 },
 'KB4': {
  G+'Bridge.lean': ['KBridge'],
  T+'KBridgeOfKPublished.lean': ['Published.KPublished'],
  T+'KBridgeOfKPublishedW.lean': ['KHurewiczW', 'Published.KPublishedW'],
 },
 'KB5': {
  G+'CardRed.lean': ['UpperTheory.V.K.cardRed'],
  G+'CardKill.lean': ['UpperTheory.V.K.cardKill'],
  G+'TensCard.lean': ['UpperTheory.V.K.tensCard'],
  G+'TorsBoundPow.lean': ['HGL', 'torsHGL'],
 },
 'KB6': {
  G+'CardH2QuotientLeSha.lean': ['UpperTheory.V.K.card_H2_quotient_le_sha'],
  G+'ChiTriv.lean': ['UpperTheory.V.K.chiTriv'],
  G+'ShaDualCard.lean': ['UpperTheory.V.K.shaDualCard'],
  G+'ShaZmCard.lean': ['UpperTheory.V.K.shaZmCard'],
  G+'Reduction.lean': ['card_mod_le'],
  AV+'GaloisLibrary/GaloisCohomologyLength/CardAbove.lean': ['UpperTheory.V.LDataCardLeFinrank.cardAbove'],
  B+'LengthEqLengthInvariantsOfTorsionLevels.lean': ['finite_cohomology_and_card_H2_eq_card_H0_dual', 'chi_loc', 'zr', 'zd', 'local_zr'],
  B+'DecompositionGroupMulEquivLocalGaloisCyclotomicStatement.lean': ['_root_.GlobalTheory.T.decompositionGroup_mulEquiv_localGalois_cyclotomic'],
  B+'ContCohomologyTransportMulEquivStatement.lean': ['_root_.GlobalTheory.T.nonempty_H1_H2_equiv_of_continuous_mulEquiv'],
 },
 'KB7': {
  'src/Development/AutomorphicArithmetic/CyclotomicBounds/ClassNumberBounds/IdealCounting/ClassC.lean': ['classNumber_le_card_ideals', 'log_classNumber_le'],
  G+'NumGens.lean': ['UpperTheory.V.K.numGens'],
  G+'PrimeLe.lean': ['UpperTheory.V.K.primeLe'],
  G+'Reduction.lean': ['generators', 'reduction'],
  G+'Bridge.lean': ['cOne', 'cOne_le'],
 },
 'KB8': {
  G+'LemmaK.lean': ['HasMuQ', 'kBound', 'LemmaK'],
  G+'TorsBoundPow.lean': ['TorsBoundPow'],
  G+'NumFin.lean': ['UpperTheory.V.K.numFin'],
  G+'Reduction.lean': ['lemmaK_of'],
  G+'LemmaKOfPublished.lean': ['lemmaK'],
 },
}

titles = {
 'KB1': 'The original Galois datum, compact cochains, finite-level comparison and mod-ell injection',
 'KB2': 'A finite actual Quillen group surjecting onto the original compact second cohomology',
 'KB3': 'Integral finite-rank Hurewicz map and exact small-prime kernel exponent',
 'KB4': 'Construction of the literal KBridge on every original datum',
 'KB5': 'Finite-module quotient and tensor-torsion cardinality bound without homology finite generation',
 'KB6': 'Strict local kernel to class-group characters and the original mod-ell cardinality bound',
 'KB7': 'Exact logarithmic reduction from actual H2 to torsion of HGL at rank 4e+4',
 'KB8': 'Universal constant absorption and the literal LemmaK 31 endpoint',
}
deps = {
 'KB1': ['LD3'],
 'KB2': ['KB1', 'LD3'],
 'KB3': [],
 'KB4': ['KB2', 'KB3'],
 'KB5': [],
 'KB6': ['KB1', 'LD3', 'LK1', 'LK2', 'LK3'],
 'KB7': ['KB4', 'KB5', 'KB6'],
 'KB8': ['KB7', 'TB10'],
}
scopes = {
 'KB1': 'Original LData D, compact Z_l(j) with all integer twists, totally complex L. Matches GS, chi, original local restrictions and H2 continuous cocycles; proves ML comparison and H2(Z_l)/l injection into H2(F_l).',
 'KB2': 'e>=1 and HasMuQ, including ell=2 and e=1. Finite K_{2e}(O_L) and its ell-primary completion; constructs a compatible arithmetic surjection onto the exact X via finite coefficient comparison and limits.',
 'KB3': 'Dedekind O_L, m=2e>=2, N=2m+4. Proves stable range by CRT, matches integral block stabilization, and uses Arlettaz R_m to obtain kernel annihilation by ell^{cOne(m)} after flat base change.',
 'KB4': 'All quantifiers of literal KBridge. Actual finite K, p, h constructed; no retained KBridge or KPublished premise and no claim about every arbitrary Plus model.',
 'KB5': 'Finite Z_l-module K, surjective p, linear h, kernel killed by ell^c; and arbitrary abelian H with finite torsion. Proves card X<=card(X/l)^c card(im h), card(finite Y in Z_l tensor H)<=card(tors H).',
 'KB6': 'All integer twists j on original D, totally complex and HasMuQ. Finite PT and local Tate, trivial residual dual twist, actual strict-local character injection into Hom(class group,F_l), and |S|<=n yield |H2(Z_l(j))/l|<=h_L ell^n.',
 'KB7': 'Under finiteness of actual T=tors H_{2e}(GL_{4e+4}(O_L),Z), proves finite X and logcard X<=4n log(2Delta)(2e)(2e+3)log(n+1)+logcard T. The class-number and prime/degree estimates are proved.',
 'KB8': 'For all real C, TorsBoundPow C implies LemmaK(max(C,0)+9); substitution TB10=TorsBoundPow22 gives literal LemmaK31 and exists CK>0 LemmaK CK with correct universal quantifier order.',
}

inputs = {
 'KB-C1': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Quillen finite generation and canonical K-theory model',
  'statement_used': 'For every number field L, K_i(O_L) is finitely generated for all i>=0. The standard Quillen K-groups for i>=1 are pi_i(BGL_infinity(O_L)^+).',
  'source': 'D. Quillen, Finite generation of the groups K_i of rings of algebraic integers, LNM341 (1973),179-198,Theorem1; canonical plus/exact-category comparison in Quillen K-theory, also Arlettaz Definition3.12 and Remark3.16.',
  'url': 'https://doi.org/10.1007/BFb0067056',
  'primary_text_url': 'https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/bass-seattle.pdf',
  'matching': 'O_L is the full ring of integers, m=2e>=2. Finite generation at m-1 is also used for the finite-coefficient inverse limit. Only the canonical model is chosen; no universal assertion for arbitrary source Plus records is inferred.',
 },
 'KB-C2': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Borel even-degree rank zero',
  'statement_used': 'For number fields and i>=2, rank K_i(O_L) is 0,r1+r2,0,r2 according to i mod4=0,1,2,3; only the even zero cases are used.',
  'source': 'A. Borel, Stable real cohomology of arithmetic groups, Ann.Sci.ENS7(1974),235-272,Proposition12.2,p.271.',
  'url': 'https://www.numdam.org/item/10.24033/asens.1269.pdf',
  'matching': 'Set D=k=L in the proposition for orders in central division algebras, and the order to O_L. Together with KB-C1 gives finiteness, not merely torsion.',
 },
 'KB-C3': {
  'kind': 'named classical citation leaf, matched in finite coefficients',
  'name': 'Dwyer-Friedlander finite coefficient comparison and etale spectral sequence',
  'statement_used': 'For a field of ell-cohomological dimension at most2, or its ring of S-integers, finite-coefficient algebraic-to-etale K comparison is onto in degrees>=2; for ell2 use r>=2 and a primitive fourth root. Localizing at ell does not change these algebraic K groups with finite ell-power coefficients in degrees>=2. The finite etale spectral sequence has E2^{p,-q}=H^p_et(U,Z/ell^r(q/2)), even q, converging to K_{q-p}^et.',
  'source': 'W.G.Dwyer and E.M.Friedlander, Algebraic and etale K-theory, Trans.AMS292(1985),247-280,Propositions5.2,8.1,8.2 and Theorem8.5; completed conclusion Theorem8.7 and Remark8.8.',
  'url': 'https://doi.org/10.1090/S0002-9947-1985-0805962-2',
  'primary_text_url': 'https://www.researchgate.net/publication/239378605_Algebraic_and_Etale_K-Theory',
  'matching': 'Total complexness supplies finite ell-cd through LD3; HasMuQ supplies integral primitive fourth root at ell2. The proof handles m2 explicitly with finite comparison, avoiding any OCR ambiguity in Theorem8.7. Cofinal r>=2 at ell2. Compatible maps pass through exact finite systems, with all limit arguments given in KB1-2.',
 },
 'KB-C4': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Finite etale/Galois comparison and finiteness',
  'statement_used': 'For U=Spec O_L[1/ell], locally constant finite ell-primary sheaves have G_S cohomology equal to etale cohomology and all finite-level groups are finite.',
  'source': 'J.S.Milne, Arithmetic Duality Theorems,2nded(2006),II Proposition2.9 and Theorem2.13. Global higher vanishing is already LD3 (I Theorem4.10).',
  'url': 'https://jmilne.org/math/Books/ADTnot.pdf',
  'matching': 'ell is invertible on U. The original closed-inertia quotient is pi1(U); original D.chi is the uniquely descended cyclotomic character. The compact integral comparison is proved here, not included in this finite theorem.',
 },
 'KB-C5': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Van der Kallen integral homology stability',
  'statement_used': 'With stable dimension d and a>=2m+max(1,d), H_m(GL_a(R),Z)->H_m(GL_{a+1}(R),Z) is an isomorphism.',
  'source': 'W.van der Kallen, Homology stability for linear groups,Invent.Math.60(1980),269-295,Convention2.2 and Theorem4.11,p.289.',
  'url': 'https://webspace.science.uu.nl/~kalle101/homstab1980.pdf',
  'matching': 'KB3 proves source StableRangeLe O_L2 by CRT, which is SR3 and permits d=1 in Convention2.2. The actual block inclusions at a>=N=2m+4 are well within the integral range. Bar homology commuting with filtered unions is proved.',
 },
 'KB-C6': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Arlettaz integral Hurewicz kernel bound',
  'statement_used': 'For any ring and m>=2, R_m kills the kernel of K_m(R)->H_m(GL_infinity(R),Z), where R_m=product_{a=2}^m L_a and L_a is squarefree.',
  'source': 'D.Arlettaz, Algebraic K-theory of rings from a topological viewpoint,PublicacionsMatematiques44(2000),3-84,Definitions7.11,7.14 and Corollary7.19(a),pp.52-55.',
  'url': 'https://mat.uab.es/pubmat/fitxers/download/FileType:pdf/FolderName:v44(1)/FileName:44100_01.pdf',
  'matching': 'Target is GL, not E. Source ArlAdm/arlL/arlR agree after zero-versus-one sequence reindexing; cutoff p<=a loses no prime, L1=1. Flat base change preserves kernel, v_ell R_m<=m-1<=cOne(m), unit part invertible. No omitted small primes.',
 },
 'KB-C7': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Unramified global Artin reciprocity',
  'statement_used': 'The Galois group of the maximal abelian extension of L unramified at all places is the ordinary ideal class group.',
  'source': 'J.S.Milne,ClassFieldTheory,v4.03(2020),Theorem0.4 and V Example3.9.',
  'url': 'https://www.jmilne.org/math/CourseNotes/CFT.pdf',
  'matching': 'Strict Sha characters vanish on original decomposition groups above ell, are unramified elsewhere by GS, and L has no real places. They therefore inject into Hom(Cl(O_L),F_ell), whose order is at most classNumber L.',
 },
 'KB-C8': {
  'kind': 'named classical citation leaf, matched',
  'name': 'Minkowski ideal-class representative bound',
  'statement_used': 'Each ideal class has an integral representative of norm <=(n!/n^n)(4/pi)^r2 sqrtDelta.',
  'source': 'J.S.Milne,AlgebraicNumberTheory,v3.08(2020),Theorem4.3,p.70.',
  'url': 'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
  'matching': 'KB7 proves the prefactor<=1, bounds ideal counts by d_n and sums these counts, deriving log h_L<=n logDelta/2 and the exact source generator constant4.',
 },
 'KB-C9': {
  'kind': 'named classical local-field comparison, matched',
  'name': 'Henselization/completion finite separable extension equivalence',
  'statement_used': 'The henselization selected by an original finite-place valuation of a global field is excellent; completion preserves its category of finite separable extensions and Galois groups.',
  'source': 'J.S.Milne,ArithmeticDualityTheorems,2nded(2006),I AppendixA,Case2,pp.130-131; classical Krasner finite-extension comparison, also the setup of LD3.',
  'url': 'https://jmilne.org/math/Books/ADTnot.pdf',
  'matching': 'Keep D.A_v. Its decomposition group is the Galois group of the selected henselization. Embed its completion L_v as a finite intermediate K_v inside PadicAlgCl(ell). The resulting continuous Galois isomorphism preserves every root-of-unity action, and precomposition transports cochains, cups and original restrictions. This matches the exact decompositionGroup_mulEquiv_localGalois_cyclotomic statement.',
 },
}
uses = {
 'KB1': ['KB-C4'], 'KB2': ['KB-C1', 'KB-C2', 'KB-C3'],
 'KB3': ['KB-C5', 'KB-C6'], 'KB4': [], 'KB5': [],
 'KB6': ['KB-C7', 'KB-C9'], 'KB7': ['KB-C8'], 'KB8': [],
}
assumptions = {
 'KB1': ['L totally complex; D is the original LData; j any integer'],
 'KB2': ['e>=1; HasMuQ ell L'],
 'KB3': ['e>=1; O_L a Dedekind domain; canonical Quillen K-theory'],
 'KB4': ['Exactly the hypotheses quantified by literal KBridge'],
 'KB5': ['Finite K; surjective p; ker h killed by ell^c; finite torsion H for the tensor conclusion'],
 'KB6': ['L totally complex; HasMuQ ell L; j any integer; original D'],
 'KB7': ['Finiteness of actual torsHGL L(4e+4)(2e), supplied by TB10 when joined'],
 'KB8': ['TorsBoundPow C for general statement; TB10 supplies C22 for actual endpoint'],
}

tex = (HERE / 'main.tex').read_bytes()
lines = tex.splitlines(keepends=True)
claims = []
for cid in titles:
    start = next(i for i, line in enumerate(lines, 1)
                 if line.startswith(('\\begin{proposition}[' + cid + ':').encode()))
    end = next(i for i, line in enumerate(lines, 1)
               if i > start and line.startswith(b'\\end{proof}'))
    loc = {'file': 'k_theory_bridge/main.tex', 'paragraph': cid,
           'line_start': start, 'line_end': end, 'label': 'claim:' + cid,
           'sha256': sha(b''.join(lines[start - 1:end]))}
    claims.append({
      'id': cid, 'title': titles[cid], 'statement': scopes[cid],
      'status': 'Complete human proof in the stated scope with explicit classical citation leaves; not replayed in Lean',
      'mathematical_status': 'closed by the listed human claims and matched classical inputs',
      'introduced_in': '0.25', 'depends_on': deps[cid],
      'assumptions': assumptions[cid],
      'named_classical_inputs': [inputs[key]['name'] for key in uses[cid]],
      'input_ids': uses[cid], 'remaining_bespoke_inputs': [],
      'proof_location': loc,
      'source_relation': 'Consolidated reconstruction and independently proved simplification. The source interface is matched on original data; canonical K-theory constructs the existential KBridge without asserting every Published package field for arbitrary Plus models.',
      'sources': [source(path, name) for path, names in spec[cid].items() for name in names],
      'component_ledger': 'k_theory_bridge/provenance.json',
    })

for path, record in files.items():
    blob = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + path])
    if sha(blob) != record['sha256']:
        raise ValueError('Pinned Git blob mismatch: ' + path)

supplier_paths = {'LD3': 'local_duality_closure/main.tex',
                  'LK1': 'local_k_duality/main.tex',
                  'LK2': 'local_k_duality/main.tex',
                  'LK3': 'local_k_duality/main.tex',
                  'TB10': 'torsion_homology/main.tex'}
suppliers = [{'claim': cid, 'file': path,
              'current_file_sha256': sha((HERE.parent / path).read_bytes()),
              'binding': 'stable claim ID; current draft file fingerprint, refresh if supplier changes'}
             for cid, path in supplier_paths.items()]

result = {
 'schema': 'rh-human-reconstruction-provenance/1', 'artifact_version': '0.25',
 'date': '2026-11-22', 'repository': BASE, 'commit': PIN,
 'component': 'k_theory_bridge',
 'scope': 'Actual KBridge construction and the complete shared LemmaK31 chain through finite duality, class number, tensor torsion and TB10. Foundational classical theorems remain explicit citation leaves; full RH/GRH is not claimed.',
 'claims': claims, 'source_files': list(files.values()), 'dependency_graph': deps,
 'input_ledger': inputs, 'human_suppliers': suppliers,
 'downstream_consumers': [{'claim': 'TW7', 'input': 'KB8 literal LemmaK31, hence exists CK>0 LemmaK CK',
                          'note': 'No ThmBab, tower/window bound or later analytic endpoint enters KB1-KB8.'}],
 'validation': {'source_files_checked_against_pinned_git_blobs': len(files),
                'claim_source_links': sum(len(c['sources']) for c in claims),
                'main_tex_sha256': sha(tex),
                'verification_kind': 'Exact source/proof byte locators and human mathematical reconstruction; no Lean kernel replay'},
}
(HERE / 'provenance.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
(HERE / 'classical_inputs.json').write_text(json.dumps({'schema': 'rh-classical-input-registry/1',
       'component': 'k_theory_bridge', 'artifact_version': '0.25', 'inputs': inputs}, indent=2, ensure_ascii=False) + '\n')
(HERE / 'source_locators.txt').write_text('\n\n'.join(
    c['id'] + ' — ' + c['title'] + '\n' + '\n'.join(
      s['declaration'] + '\n' + s['url'] + '\nfile ' + s['sha256'] + '\nrange ' + s['range_sha256']
      for s in c['sources']) for c in claims) + '\n')

closure = {
 'schema': 'rh-dependency-closure/1', 'artifact_version': '0.25',
 'component': 'k_theory_bridge', 'commit': PIN,
 'main_tex_sha256': sha(tex),
 'closed_endpoints': [
   {'claim': 'KB4', 'literal_interface': 'UpperTheory.V.K.KBridge',
    'supplier': 'Canonical finite K_{2e}(O_L) tensor Z_l with constructed p,h on each original D'},
   {'claim': 'KB8', 'literal_interface': 'UpperTheory.V.LemmaK (31 : Real)',
    'supplier': 'KB1-KB7 + TB10, with finite duality suppliers LD3,LK2,LK3'},
 ],
 'graph': deps,
 'rooted_full_chain': {'root': 'KB8', 'human_leaves': ['LD3', 'LK1', 'LK2', 'LK3', 'TB10'],
                       'classical_leaves': list(inputs),
                       'retained_bespoke_suppliers': []},
 'same_object_bindings': ['Original L and algebraic closure Omega', 'Original LData D and its places D.A',
                         'Original quotient GS and uniquely descended D.chi',
                         'Source compact continuous-cochain H2',
                         'Actual HGL L (4e+4) (2e) with integral coefficients',
                         'cOne(2e) and source kBound exact normalization'],
 'noncircularity': ['Finite-level cohomology finiteness and higher vanishing are classical/LD3 and precede integral H2 finiteness.',
                   'Integral H2 finiteness is derived from finite Quillen K via DF, not assumed in any inverse-limit argument.',
                   'Hurewicz kernel control uses universal Arlettaz bound and integral stability, not the torsion estimate.',
                   'TB10 is joined only at KB8 after actual KBridge and finite-module reduction are proved.',
                   'No TW, ThmBab, LinkV, prime-window, or RH/GRH conclusion is an input.'],
 'simplifications': ['Choose canonical Quillen K to fill existential KBridge, avoiding universal arbitrary-Plus package assertions.',
                     'Use finite DF comparison and explicit limits to cover degree2 and prime2 without theorem-statement OCR ambiguity.',
                     'Use direct cochain injection H2(Z_l)/ell -> H2(F_ell); no integral H3 input.',
                     'Use squarefree Arlettaz factors to get v_ell R_m <= m-1 <= cOne(m).',
                     'Prove tensor cardinality using flatness and torsion-free quotient; no finite-generation assumption on HGL.'],
 'quantifier_order': 'C_K=31 is fixed before ell,L,Omega,D,e. p,h may depend on these data as allowed by KBridge.',
 'not_claimed': ['A universal proof of every KPublished or KPublishedW field for every arbitrary Plus model',
                 'First-principles proofs of the explicitly cited foundational classical theorems',
                 'Full RH/GRH reconstruction', 'Lean kernel replay'],
}
(HERE / 'closure.json').write_text(json.dumps(closure, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'main_tex_sha256': sha(tex), 'claims': len(claims),
                  'source_files': len(files), 'source_links': sum(len(c['sources']) for c in claims)}, indent=2))
