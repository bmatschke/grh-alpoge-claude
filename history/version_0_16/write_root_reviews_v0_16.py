#!/usr/bin/env python3
"""Record the completed root mathematical reviews and recheck their source bytes.

The prose records human review performed during v0.16. Hash checks do not
constitute mathematical proof or independent Lean verification.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent/'lean-source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
def digest(b):return hashlib.sha256(b).hexdigest()
cache={}
reviews=[
 ('arithmetic_hosts','AH',[1,2,3,4,5,6,7,8,17,18],'root_reviews_ah_1_8_17_18.txt',r'''
AH1--AH2. Reviewed the finite character-annihilator duality and the exact cyclic
two-adic quotient, without imposing evenness or a two-group condition on Xi.
The character injection, restriction and reduction maps have the stated
domains. The CRT surjectivity used at conductor reduction is at the actual
divisor, including its prime-power factors.
AH3--AH4. Reviewed the mixed-character Artin sign correction, compatible
cyclotomic fixed field and the literal character-data record. The complex
conjugation condition and the quadratic factor are retained. The Gauss/root
constructions use the actual embeddings and do not identify unrelated choices.
AH5--AH8. Reviewed primitive conductor descent, the gcd reduction and CRT
argument, eventual order, the kept-character set, and the kernel/twist formulas.
The eventual-order argument descends the bounded auxiliary invariant before
concluding stabilization; it does not assume Q_e divides Q_(e+1). The original
arbitrary character group remains explicit.
AH18. Read the literal fieldChi declaration and its quantifier order. The
thresholds c0,e0 are chosen before e,q,d,b. All eight FieldRows fields are
accounted for by the actual construction and earlier proved lemmas. The q,d
prime, congruence, coprimality and splitting premises are retained. This is not
an analytic theorem selecting those primes in the required windows.
The HostDer arithmetic review is separately recorded for AH9--AH16. AH17's
explicit thirty-field assembly was checked against HostDer and HostRaw.der,
including the earlier AC2--AC3 norm supplier. Their raw hypotheses give the
required degree, prime d>3 and actual quadratic subfield; the assembly does
not assume HostDer.norm_mu in order to construct that very field.
The source name KcDiff.principal is interpreted as the chosen ideal factor b
with different=b*conjugate(b), not as a principal-ideal-class assertion.
No material defect remains in this reviewed conditional scope. The AH3
alignment and AH15 multiplication notation corrections are editorial.
'''),
 ('canonical_indices','CI',[1,2,3,4,5,6,7,8,9,15,16,17,18,19],'root_reviews_ci_1_9_15_19.txt',r'''
CI1--CI2. Reviewed stabilization of finite normalized boxes, common period
lattices, finite-index changes of variables, and affine reindexing. The
character-rigidity conclusion uses a nonzero stabilized sum and the full period
group: invariance of S and eigenfunction translation give S=chi(h)S. There is
no unsupported analytic integration or determinant-one premise.
CI3--CI4. Reviewed finite coset colors modulo q^(j+1), rational localization,
flag-adapted DVR elimination and the projected integral subgroup. Degree-one
unramified hypotheses appear where digit boxes need them; they are not silently
imposed on the independent finiteness statement.
CI5--CI8. Reviewed exact unfolding coordinates and affine phase transport,
support/covariance and uniform bounds for the actual twisted test function.
The empty-support case gives zero on both sides; otherwise a support point
places the constant phase discrepancy in the character domain. Double-coset
nonvanishing and projected-kernel triviality follow from the proved finite-sum
identities, without assuming completed column Laws or comparison conclusions.
CI9. Reviewed the finite recursive representatives and their predecessor,
coverage and uniqueness properties. The proof does not demand that every
intermediate candidate set be nonempty.
CI15. Reviewed the complete 34-field ChIdx.Ok accounting and the literal
exists_chIdx_of_cst endpoint. CI10--CI14 supply the explicit finite-field and
local positive-sum calculations and have a separate independent review.
CI16. Reviewed the local additive-character adjustment, the Gauss square at
q=1 mod4, and the product-formula argument for ramified local character values.
The initial constants M=A=B=m, DQ=2m, DG=1 and canonical replacement
M=m, A=B=m+1, DQ=2m are kept distinct.
CI17--CI18. Reviewed the actual representatives and choice predicates in
twIdx_ok_closed and canonical replacement. canon_ok retains its supplied
old-Ok and Deep premises; it is not an initial-data existence theorem.
CI19. Reviewed the joint supplier boundary. PA9/PA13, AH17/AH18 and TA10/TA12
are separately constructed companions. The multidimensional vacuum,
indicator/covariance, Pins.iX, and all five Later stages remain explicit.
No material defect remains in this reviewed conditional scope.
'''),
 ('twisted_comparison','TX',[10,11,12,13,14,15,16],'root_reviews_tx_10_16.txt',r'''
TX10. Reviewed the actual point-orbit reindexing, preferred representative
equality, same L-sharp and integral Delta lattice, and coefficient embedding.
The integral assertion is pointwise in that same lattice, not merely equality
of rational spans. The injective form embedding makes every permissible Law0
map equal to the displayed reindexing, so the later statements cover arbitrary
supplied l0 and not only one convenient witness.
TX11--TX12. Reviewed assembly of the actual all-twist charts and common
penultimate character; no terminal object is independently re-chosen during
the join. Up/down, diamond, kernel, residue and stabilizer maps agree at zero
and at the reference twist by the actual preferred decorations and movement
maps. The source integral Delta lattice, standard maps and type-prime residue
identifications are retained. Exact source definitions for FormsEquiv,
TrueColumnChoiceExistsStandardChainData, the tuple chain level compatibility
and the standard data records were read at the asserted interface.
TX13. Reviewed the literal row datum with unique index, no coupling and empty
type-prime set. The exact row scalar is q_P and the full terminal scalar is
q_P^(c+1). Their exponents are not silently identified with additive
P-valuations; positive valuation of q_P suffices for the row reduction kernel.
TX14. Reviewed the actual row values, periods, norm and semilinear comparison.
Clearing denominators at one coefficient prime requires a denominator outside
that prime, chosen by CRT; integrality at the other good places is preserved.
This is stronger than an unsupported passage from rational to integral forms.
TX15. Reviewed the same moving gamma, full-dual functional identification and
bar(pi)-unit cancellation, not cancellation in only a residue quotient. With
x=y M^-1 gamma^-1 ext(y'), kappa=x^-1 gives gamma y M=ext(y') kappa;
the inverse in the character yields the stated movement factor. The terminal
evaluation holds for the actual arbitrary frame function. ExtMMulVecFix and
the exact tuple terminal movement statements were compared with this formula.
TX16. Reviewed all ten SymmetricTwistedColumnsAtPrimes fields and the StdTw
clauses. The source NChoice, TupTied and tp.xi=I.xi remain original hypotheses.
Finite character readings do not supply the finite DVR/valuation/Mt integral
comparisons in NChoice. Stronger OneLevelSymmetricColumns is not inferred.
No material defect remains in this reviewed conditional scope. Reviews of
TX1--TX9 are recorded separately by the other component authors.
'''),
]
for component,prefix,numbers,name,findings in reviews:
    directory=ROOT/component
    ledger=json.loads((directory/'provenance.json').read_text())
    ids={prefix+str(i)for i in numbers}
    claims=[c for c in ledger['claims']if c['id']in ids]
    assert {c['id']for c in claims}==ids
    raw=(directory/'main.tex').read_bytes()
    lines=raw.splitlines(keepends=True)
    marks=[]
    for i,line in enumerate(lines):
        m=re.search(rb'\\paragraph\{('+prefix.encode()+rb'\d+):',line)
        if m:marks.append((m.group(1).decode(),i))
    assert ids<={cid for cid,i in marks}
    scoped=[]
    for i,(cid,start)in enumerate(marks):
        if cid not in ids:continue
        end=marks[i+1][1]if i+1<len(marks)else len(lines)
        scoped.append((cid,start+1,end,digest(b''.join(lines[start:end]))))
    links=[]
    for c in claims:
        for s in c['sources']:
            p=s['path']
            if p not in cache:
                cache[p]=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+p])
            blob=cache[p]
            assert digest(blob)==s['sha256'],p
            b=b''.join(blob.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
            assert digest(b)==s['range_sha256'],(c['id'],p,s['line_start'])
            links.append((c['id'],s))
    unique={(s['path'],s['line_start'],s['line_end'])for _,s in links}
    paths={s['path']for _,s in links}
    out=[f'ROOT MATHEMATICAL AND SOURCE-INTERFACE REVIEW: {component}',
         'Reviewer: /root, independent of the component author',
         'Result: PASS for the displayed conditional statements and explicit inputs.',
         'Pinned source: '+PIN,'',
         'This records a human review. The accompanying byte checks establish source',
         'identity; they do not mechanically prove the mathematics. Review metadata',
         'may subsequently be attached to a ledger without changing its claims or',
         'source ranges; the proof hashes below identify the reviewed text.','',
         'ARTIFACT HASHES AT REVIEW']
    for filename in ['main.tex','report.txt','provenance.json','source_manifest.json','next_targets.json']:
        p=directory/filename
        if p.is_file():out.append(filename+' SHA256 '+digest(p.read_bytes()))
    out+=['','SCOPED PROOF HASHES']
    out.extend(f'{cid}: main.tex lines {a}-{b}; SHA256 {h}'for cid,a,b,h in scoped)
    out+=['','MATHEMATICAL FINDINGS',findings.strip(),'','SOURCE IDENTITY CHECKS',
          f'{len(links)} scoped claim-source links, {len(unique)} unique inclusive ranges, {len(paths)} pinned files.',
          'All corresponding full-file and range SHA256 values match the current ledger.']
    out.extend(f"{cid}: {s['declaration']} | {s['path']}:{s['line_start']}-{s['line_end']} | {s['range_sha256']}"for cid,s in links)
    out+=['','LIMITS',
          'No Lean build, independent kernel replay, exhaustive transitive formal dependency',
          'audit, complete self-contained RH/Dirichlet-GRH proof, or PDF visual review.',
          'The earlier retained global spectral, metric, cohomological and prime-window',
          'branches are outside these conditional local/arithmetic reviews.','']
    p=ROOT/'reviews_v0_16'/name
    p.write_text('\n'.join(out))
    print(json.dumps({'file':str(p.relative_to(ROOT)),'claims':len(claims),'source_links':len(links),
                      'ranges':len(unique),'source_files':len(paths),'sha256':digest(p.read_bytes())}))
