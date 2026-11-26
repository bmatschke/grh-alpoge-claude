#!/usr/bin/env python3
"""Record root's completed mathematical readings against immutable proof blocks.

The notes below are the review judgments, not results of automated theorem checking.
Byte and source checks only bind those judgments to the reviewed version.
"""
from pathlib import Path
import hashlib
import json
import subprocess

WORK = Path(__file__).resolve().parent.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
SOURCE = Path('/workspace/scratch/249d32c24541/formal_source')
sha = lambda b: hashlib.sha256(b).hexdigest()

def record(component, expected_hash, notes, scope, corrections=()):
    here = WORK/component
    raw = (here/'main.tex').read_bytes()
    assert sha(raw) == expected_hash, (component, 'reviewed version changed')
    ledger = json.loads((here/'provenance.json').read_text())
    claims = ledger['claims']
    assert len(notes) == len(claims)
    checks, source_files, source_data = [], {}, {}
    for c, note in zip(claims, notes):
        loc = c['proof_location']
        block = b''.join(raw.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']])
        assert sha(block) == loc['sha256'], c['id']
        for s in c.get('sources', []):
            path = s.get('path')
            if not path:
                continue
            if path not in source_files:
                original = subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path])
                assert (SOURCE/path).read_bytes() == original
                source_files[path] = sha(original)
                source_data[path] = original
            assert source_files[path] == s.get('file_sha256',s.get('full_file_sha256'))
        checks.append({'id':c['id'], 'block_sha256':loc['sha256'],
                       'result':'PASS', 'mathematical_review':note})
    manifest = json.loads((here/'source_manifest.json').read_text())
    source_verification=[]
    for s in manifest.get('files',manifest.get('source_files',[])):
        path=s['path']
        if path not in source_data:
            original=subprocess.check_output(['git','-C',str(SOURCE),'show',PIN+':'+path])
            assert (SOURCE/path).read_bytes()==original
            source_data[path]=original; source_files[path]=sha(original)
        actual=sha(source_data[path])
        assert actual==s.get('sha256',s.get('file_sha256'))
        snapshot=s.get('snapshot_file',s.get('snapshot_path'))
        if snapshot:assert (WORK/snapshot).read_bytes()==source_data[path]
        source_verification.append({'path':path,'sha256':actual,'snapshot_file':snapshot,
            'source_commit':PIN,'verified_equal_to_pinned_git_blob':True,'result':'PASS'})
    ranges={}
    for s in manifest.get('ranges',[])+[s for c in claims for s in c.get('sources',[]) if 'line_start' in s]:
        key=(s['path'],s['line_start'],s['line_end'])
        data=source_data[s['path']]; lines=data.splitlines(keepends=True)
        assert 1<=s['line_start']<=s['line_end']<=len(lines)
        part=b''.join(lines[s['line_start']-1:s['line_end']])
        assert s['range_sha256'] in {sha(part),sha(part.rstrip(b'\r\n'))}
        ranges[key]={'id':s.get('id'),'path':s['path'],'line_start':s['line_start'],
            'line_end':s['line_end'],'file_sha256':sha(data),'range_sha256':sha(part),'result':'PASS'}
    inherited=[]
    inputs=json.loads((here/'inherited_inputs.json').read_text()).get('inputs',[])
    for row in inputs:
        parent_file=row.get('parent_provenance_file',row.get('provenance_file',row['component']+'/provenance.json'))
        parent_raw=(WORK/parent_file).read_bytes(); parent=json.loads(parent_raw)
        expected_parent=row.get('exact_parent_provenance_sha256',row.get('provenance_sha256'))
        if expected_parent:assert sha(parent_raw)==expected_parent
        parent_claim=next(c for c in parent['claims'] if c['id']==row['id'])
        pl=parent_claim['proof_location']; pfile=pl['file']
        if not (WORK/pfile).is_file():pfile=row['component']+'/'+pfile
        data=(WORK/pfile).read_bytes()
        part=b''.join(data.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
        assert pl['sha256'] in {sha(part),sha(part.rstrip(b'\r\n'))}
        expected=row.get('proof_block_sha256',row.get('proof_range_sha256',row.get('proof_location',{}).get('sha256')))
        if expected:assert expected in {sha(part),sha(part.rstrip(b'\r\n'))}
        expected_file=row.get('proof_file_sha256',row.get('file_sha256'))
        if expected_file:assert expected_file==sha(data)
        inherited.append({'id':row['id'],'proof_file':pfile,'proof_file_sha256':sha(data),
            'line_start':pl['line_start'],'line_end':pl['line_end'],'proof_block_sha256':sha(part),
            'parent_provenance_file':parent_file,'parent_provenance_sha256':sha(parent_raw),'result':'PASS'})
    review = {
        'schema':'rh-independent-mathematical-review/1',
        'artifact_version':'0.57', 'date':'2026-11-24',
        'component':component, 'reviewer':'root', 'status':'PASS',
        'source_commit':PIN, 'proof_file_sha256':sha(raw),
        'review_scope':scope,
        'claims_reviewed':checks, 'source_file_bindings':source_files,
        'source_files_checked':len(source_verification),'source_ranges_checked':len(ranges),
        'source_verification':source_verification,'source_range_verification':list(ranges.values()),
        'inherited_inputs_checked':len(inherited),'inherited_verification':inherited,
        'corrections_resolved':list(corrections), 'unresolved_findings':[],
        'whole_selected_obligations_closed':[],
        'formal_verification':False, 'lean_replay':False,
    }
    (here/'independent_review_root.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
    print(component, len(checks), sha(raw))

if __name__ == '__main__':
    record('determinant_jet_v57',
      'b33b9fcc74e21234fad77c3d565b80693a4708684afd949ab298a03750878435', [
      'Bezout identifies the integer valuation without discreteness; Legendre and digit sums give both factorial bounds, including zero multiindices.',
      'Ordinary Cayley, explicitly retained as a classical identity, iterates to C_r(m). Moving multiplication through the factorial pairing gives the stated ratio with nonzero denominators.',
      'The positive Y-degree makes every exponential coefficient finite. Valuation of t! is offset by the weighted lower bound. Frobenius modulo p and the number of positive Z-degree factors give the exact divisibility and degree of Psi^s.',
      'Conjugation of finite ordinary differential operators and the Cayley adjoint formula give an exact finite Newton expansion for each y; a_0=1 is justified by E(X,0)=1.',
      'The two factorial normalizations, weighted coefficient bound, Psi divisibility and e identity yield the stated s/8 bound with the full logarithmic loss; no asymptotic coefficient is substituted for a finite one.',
      'The explicit ceiling threshold and logarithmic inequalities imply strict positivity for every s at or beyond S, with all p>=5, odd h>=1 and r>=1 retained.',
      'The translated binomial evaluation matrix has determinant one and an integer inverse; this works for every translated interval and does not require large residue characteristic.',
      'Tail coefficients are strictly positive in valuation and the integer interpolation recovers a_0=1, forcing one good y. The returned original bound and the separate empty-matrix case match full ThmP.',
      'Restriction of the source mvExp is proved coefficientwise with its finite degree truncation even for nonzero constant term; use of the genuine exponential is confined to zero constant term.',
      'Determinant permutation expansions force the prescribed diagonal rows and the complementary block; the argument is over arbitrary commutative coefficient rings.',
      'Multigraded minimal degrees eliminate all higher coordinate and row-exponential terms in the extra rows. Ordinary derivatives yield exactly ((A! B!))^(n-r), including zero exponents.',
      'All BiHyp fields are used at their literal scope. The proof preserves arbitrary l,i,n,r,y, including l=0/i=0/n=0, and does not import the valuation or oddness assumptions from ThmP.',
      'The factorial valuations and monotonicity of the nonnegative slope provide the literal BiContent bound with the original r,n distinction.',
      'The exact BiValue identity followed by ThmP and the factorial content bound proves BiWindow with its original rank-defect hypothesis and window length.',
      'The original MConcl weighted remainder and axis vanishing give HM1/HM2 on the actual restricted series. Row separation and the optional level-one low-degree clause supply all four MtoHM fields.',
      'A nonzero kernel vector can be normalized at one minimum-valued coordinate without a discrete valuation. The appended row and column preserve both splittings and integrality at every intermediate size, hence give an integral square unit.',
      'The original Cart existence axiom supplies typed curves with standard initial vectors; coefficientwise contraction of the order-two correction gives actual standard coordinates and the required uniqueness.',
      'The ordinary chain rule for linear substitution is checked on monomials and factorials. The determinant factor has the displayed direction, rather than an inverse or a divided-power normalization.',
      'The completed integral Abar and integral inverse of Y supply the actual row substitutions and diagonal-coordinate first jets. The restricted original gauge equals the exact supplied main-term expression before y is chosen.',
      'The polynomial gamma has integral coefficients and its substitution by the fixed coordinates is literally IntGerm. The derivative change gives det(Abar)^(qy) det(Y)^y; both are units, yielding equality of valuations. Arbitrary supplied h1 with the original restriction identity remains allowed.',
      'The rank-defect inequality and monotonicity of S install the exact original Windows bound with one coordinate choice before every window origin. The r=0 and y=0 cases are explicit. LemmaM existence and the global theta family remain retained producers.'
      ], 'Read all 21 proof blocks and checked their original contracts, including unrestricted BiValue, all four MtoHM fields, standard coordinates, complete_rows and every-h1 block_of_normal_form. The final actual row window retains the original supplied MConcl. No whole global closure follows.')
    record('arithmetic_connectedness_v57',
      '7664888c27b6f2716697fc1dee2136fe808cb38dcf967b261fc138cb9c435b59', [
      'Systems of parameters and the height theorem give the cut inequality without a regular sequence. Passing to the reduced complete local domain and catenarity gives each minimal-component lower bound.',
      'The stated complete-local connectedness theorem applies with cd(J)<=h and min(c,d-1)=dim(T)-1. A disconnected component graph would give a closed separating locus of dimension <D, contradicting the exact threshold. Prime nilradical and h=0/D=0 are retained.',
      'The surjective quotient correspondence preserves minimal primes, sums of primes above the kernel, and all quotient dimensions, hence carries every finite component path.',
      'APD25 has N=N-prime+n*d+1; its complete regular source has dimension N+1=D+1+N-prime for D=n*d+1. No Big or nontriangularity premise is imported. This ordinary presentation is not rank-three EPres.',
      'The actual finite unramified coefficient extension is flat; the specified completion has the same quotient dimensions. The finite-type dimension formula applies over the complete universally catenary B/p. Flat going down supplies the exact contraction and the maximal-dimensional minimal prime gives equality.',
      'Surviving entries of opposite weights and their balanced products make all other entries algebraic over one surviving parameter. The argument does not require homogeneous eta or invert weights in the residue field, and works at both ranks.',
      'Strict triangular functions inject into the exact bounded strict cohomology group because the involution kills the residual coboundary parameter when ell is odd. RTC coefficient decomposition and actual universal maps give the polynomial fibre ring, before reduction.',
      'A unit lower entry forces all upper entries into m_B R via their balanced products. The full polynomial strict fibre and loc_dim then bound every component of the actual completed closed fibre by C0.',
      'The frame h1/gen/cl inputs give finite detecting evaluations and a single exponent for every finite abelian ell-group character. Symmetrized elements raised to |k^x| preserve Psi=1; the split involution argument converts their vanishing to the exact star condition.',
      'Compactness makes each continuous finite-precision image finite, even without a finite residue field. Residually one units have ell-power order. Krull separation and the domain argument for the fixed exponent yield exact identities, with no hidden completeness needed in the first statement.',
      'The uniformizer and exact character cuts force the residual diagonal character in every prime quotient. Local separation and two trace equations preserve the ordered local characters. The actual topology on B and dense balanced generators then force m_B into the radical.',
      'Cutting the triangular quotient by d+C0+2 elements and using the closed fibre bound yields d+2C0+2. This implies the original rank-two l51 bound and the strict Big inequality; rank three is explicitly excluded.',
      'Every local minimal prime has dimension at least 2d+2 by the component theorem. The unit lower ideal and strictly smaller upper-triangular quotient force type I, supplying full original sharp2.',
      'The exact local inertia generators have one exceptional index. Counting the uniformizer, all retained equations and the one exceptional omitted-character equation gives n*d-d_v+2. Finite-character detection forces the full lambda ideal in every prime quotient, including equal characteristic.',
      'Coincidence contracts along the actual coefficient map. Combining the coefficient quotient bound with the off-triangular transcendence bound yields the stronger n*d+3 bound, implying both original l52 conclusions at both ranks.',
      'Every minimal prime over a bad ideal is either triangular or off triangular; the preceding two bounds and d_v>5 give the strict dimension inequality for the full quotient, retaining nilpotents and the zero-quotient convention.',
      'After one cut, choose a component of dimension >=N and an element avoiding it and meeting every bad ideal. A maximal prime avoiding that element has one-dimensional quotient by finite prime avoidance and the principal ideal theorem. No catenarity, infinite field or primality of K is added.',
      'Using the actual uniformizer in NicePrimeEx ensures characteristic ell even in equal characteristic. Avoidance of the listed triangular and coincident-character ideals gives the original ordered Nice tests on the same chart.',
      'All ten actual rank-two LocData.Ok fields are accounted for. Empty exceptional/thick fields are vacuous; ACC supplies sharpness and Nice existence, while the original P1-prime supplies exactly downward goodness. The finite-chain propagation is also written directly.',
      'The homogeneous core of a prime is prime in a Z-graded ring by taking the largest surviving homogeneous indices. Minimality therefore forces each minimal prime homogeneous, without finite-field character detection.',
      'Localizing the finite-type closed fibre at one basic-open equation and a lower entry gives a closed point with finite field residue. Contraction stays maximal and proves the full locally closed incidence, not merely density of rational points.',
      'The negative-weight monomial count and finite graded B-modules turn a hypothetical radical containment into Nakayama vanishing of a chosen lower-entry power. This proves actual incidence before any FinA conclusion.',
      'Localizing at a surviving balanced upper/lower product gives the literal Laurent algebra B_a[U,U^-1]. The direct grading proves injectivity. Extending the smaller prime Z and contracting gives a homogeneous type-I prime with exact contraction and trdeg one, preserving the weaker seed input.',
      'The homogeneous incidence chooses one closed core point first. The full converse loc_dim then supplies the required type-I prime for every allowed local object at that point, with exact coefficient contraction and dimension.',
      'The actual flat completed chart has the required minimal-component correspondence. ACC local data and inherited ACP chart propagation give all three actual at_pt conclusions, including seed initiation.',
      'All eight global fields are verified on the actual type-I locus and core, using inherited preconnectedness, the new incidence and actual seed localization. ACP global propagation returns literal AllGood at precisely FinLam/P1-prime/SeedIn. No automorphic seed is inferred from connectedness.',
      'The AbsMain consumer uses the separate determinant maps and ideals; the rank-two return is applied to its exact transferred ideal. The rank-three suppliers proved at general scope are listed separately from EPres/Sharp/corner/thick-chain, OffFin and automorphic inputs still needed.'
      ], 'Read ACC1–ACC27 and checked the literal general and rank-two interfaces in c1ch, loc_dim, frame gen/cl/Big, PropagationTheoremGL2, P1-prime, SeedIn, AllGood, ComponentsGoodRankTwo and seedpt. The cited Stacks connectedness and dimension hypotheses were verified from the primary statements. The stronger rank-two dimension bounds and fixed seed-point choice are valid. No rank-three or whole arithmetic closure is inferred.',
      ['ACC5 wording corrected: a strictly larger contraction yields a smaller prime over qR by flat going down, contradicting minimality.',
       'ACC18 missing backslash before quad corrected.'])
    record('section_growth_v57',
      'be5d7125a72d5bb5cf84cec9c309997cbb02d2f06b1e866e421a7578fa1e935f', [
      'The specific projection from the identity-base categorical product has an explicit inverse by its universal property. Smooth proper geometrically connected fibers with identity are regular and geometrically integral; the original smoothDim field gives exactly g. This verifies Milne\'s abelian-variety hypotheses on the actual product.',
      'The singleton power charts have precisely the pulled transition units to exponent j. The source SecM equations and toSec/ofSec keep coordinate tuples unchanged. The original first-projection scalar action agrees with the canonical K-to-global-functions isomorphism, for positive and negative powers.',
      'PBC26 supplies one N before t on the actual Cartesian model. The original ratio-surjectivity data give a closed immersion chart by chart. A section nonzero at the identity stays nonzero in every positive tensor power, and Veronese preserves ampleness in all characteristics. The power-coordinate maps identify V_(Nt) literally.',
      'Milne Proposition 9.1 applies because each positive power is ample with a nonzero section; Theorem 13.3(c) then forces its unique nonzero cohomology degree to be zero. No identification with source KTriv or prime-to-characteristic condition is needed.',
      'The original nonzero section of a line bundle on the integral scheme defines an effective Cartier divisor. Applying the stated abelian Riemann–Roch formula and multilinearity gives exact t^g scaling. The factorial is used in rational intersection numbers, not inverted inside K.',
      'For g=0 the actual geometrically integral finite-type scheme has one point and is Spec of a finite algebraic field extension; algebraic closedness identifies it with K. Every invertible sheaf has one-dimensional sections, giving the same formula.',
      'PBC27 gives all integer-power finiteness. The fixed N and d=h0(H)>=1 yield exact dimension d*t^g and the literal two-sided contract with c=1,C=d. Original choice order, scalar field, every characteristic and g=0 are retained. Rank one and torsion decomposition remain separate.'
      ], 'Read all seven blocks and compared the literal finite-and-growth conclusion, actual SecM scalar action, power-coordinate maps and PolAV/isAb records. Verified Milne\'s primary Proposition 9.1 and Theorem 13.3(b),(c). The final boundary explicitly preserves SHV17 eventual all-cover Serre and SHV21 homogeneous generation, distinguishing the later every-positive-power descent input. No whole selected obligation is closed.',
      ['Clarified the final frontier so the already completed SHV17/SHV21 results are not reopened.'])
