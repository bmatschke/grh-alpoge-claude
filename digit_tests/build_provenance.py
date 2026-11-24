"""Source provenance for DT1--DT11; does not run Lean or check proof terms."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2]/'alpoge-rh')
args = ap.parse_args()
ROOT = args.repo
OUT = Path(__file__).resolve().parent
COMMIT = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
REPO = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == COMMIT
GB = 'src/Formalism/SharpRestriction/GrowthBounds/'
files = {}

def namespace_at(lines, first):
    stack = []
    for line in lines[:first-1]:
        ns = re.match(r'^namespace\s+(\S+)', line)
        sec = re.match(r'^(?:noncomputable\s+)?section(?:\s|$)', line)
        end = re.match(r'^end(?:\s|$)', line)
        if ns: stack.append(('namespace', ns.group(1)))
        elif sec: stack.append(('section', ''))
        elif end:
            assert stack, ('unmatched end', first, line)
            stack.pop()
    ns = '.'.join(name for kind, name in stack if kind == 'namespace')
    return ns+'.' if ns else ''

def ref(path, declaration, role='proof'):
    raw = (ROOT/path).read_bytes()
    lines = raw.decode().splitlines(keepends=True)
    pat = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev)\s+'
                     + re.escape(declaration)+r'(?=[\s{(:])')
    hits = [i for i, line in enumerate(lines) if pat.match(line)]
    assert len(hits)==1, (path, declaration, hits)
    first = hits[0]+1
    top = re.compile(r'^(?:private\s+)?(?:noncomputable\s+)?(?:theorem|lemma|def|structure|abbrev|class|end|namespace|section|variable|include|omit|open|attribute|instance)\b')
    last = next((i for i in range(first, len(lines)) if top.match(lines[i])), len(lines))
    while last>first and not lines[last-1].strip(): last-=1
    sha = hashlib.sha256(raw).hexdigest()
    url = f'{REPO}/blob/{COMMIT}/{path}'
    files[path] = dict(path=path, sha256=sha, line_count=len(lines), url=url)
    return dict(path=path, declaration=namespace_at(lines, first)+declaration,
                line_start=first, line_end=last, role=role, sha256=sha,
                range_sha256=hashlib.sha256(''.join(lines[first-1:last]).encode()).hexdigest(),
                url=url+f'#L{first}-L{last}')

def ds(file, name, role='proof'): return ref(GB+'DiagonalSupport/'+file+'.lean', name, role)
def tw(file, name, role='proof'): return ref(GB+'TwistedSubstitution/'+file+'.lean', name, role)
claims=[]
def claim(cid, title, statement, status, sources, dependencies, sections, assumptions=(), relation=''):
    claims.append(dict(id=cid, title=title, statement=statement, status=status,
        sources=sources, depends_on=dependencies, assumptions=list(assumptions),
        proof_location=dict(file='digit_tests_section.tex', section='Digit factorials, normal tests, and admissible assembly'),
        expanded_notes=dict(file='digit_tests_report.txt', sections=sections), source_relation=relation))

claim('DT1','Ordered sums in the integral binomial basis',
      'For positive t_i and T=sum(t_i), the sum over 0<=u_1<...<u_m<b of product u_i^t_i is an integer-valued rational polynomial of degree at most T+m<=2T, hence has integral Newton coefficients.',
      'derived_simplification', [ds('DigAbs','DigAbs','target_interface'),ds('BinomCombFOnFinset','digQ','alternative_proof_target')],
      [], ['1.1'], relation='Original elementary proof supplied here. The source links identify the factorial-approximation interface it replaces, not a named source lemma for these ordered sums.')
claim('DT2','Filtered finite-product approximation',
      'If F(u)=1+sum a_t u^t with a_t in p^t Z_(p), the finite product over u<b has a binomial-polynomial approximation modulo p^c of degree at most 2(c-1). Total-grade truncation preserves this bound for products over arbitrarily many variables; inverse linear-unit products obey it too.',
      'derived_simplification', [ds('DigAbs','DigAbs','target_interface'),ds('BinomCombFOnFinset','digQ','alternative_proof_target')],
      ['DT1'], ['1.2'], relation='New finite-product argument, valid for every prime. Finite-precision expansions avoid an unstated infinite-product convergence claim.')
claim('DT3','Exact factorial factorization into linear units',
      'For P=p^g and 0<=rho<P, gamma=(rho+Pb)!/(rho! b! (P!)^b) equals product_(i<=rho)(1+Pb/i) times product_(ell=1..g,u<b,1<=a<=p^ell,p nondividing a)(1+p^ell u/a). Each nonconstant linear coefficient belongs to p Z_(p), so gamma is a unit.',
      'derived_simplification', [ds('PickDefs','gamR','exact_source_definition'),ds('BinomCombFOnFinset','gamR_zero_zero'),ds('BinomCombFOnFinset','gamR_one_zero')],
      [], ['1.3'], relation='Exact factorization proved by stripping multiples of p from factorials; gamma is the literal source gamR.')
claim('DT4','Stronger uniform factorial-unit polynomial theorem',
      'For every prime, finite product Gamma of the digit factorial units and epsilon=+1 or -1, there is an integral binomial polynomial Q of total degree <=2(c-1) approximating Gamma^epsilon modulo p^c uniformly on all natural exponent vectors. It implies DigAbs (4c) and GaAt (6c), keeping downstream constants unchanged.',
      'derived_simplification', [ds('DigAbs','DigAbs','target_interface'),ds('BinomCombFOnFinset','digQ','source_comparison'),ds('BinomCombFOnFinset','digAbs','source_comparison'),ds('BinomCombFOnFinset','gaAt','source_comparison'),ds('PickDefs','GaAt','target_interface')],
      ['DT1','DT2','DT3'], ['1.4','2'], ['c>=1; c=0 is handled by Q=0.'],
      relation='The 2(c-1) bound and p=2,3 scope are human deductions, not claims about the exported Lean statement. Prime-to-p denominator coefficients map into the actual DVR.')
claim('DT5','Exact digit Fock identity and diagonal operators',
      'Digit blocks are Fock-orthogonal. Within a block alpha!=C_rho betaPl! betaNo! GammaPl GammaNo with the exact source scalar C_rho. Multiplication of exponent coefficients by binom(alpha,m) equals X^m partial^[m].',
      'faithful_translation', [ds('PickDefs','gamPl','definition'),ds('PickDefs','gamNo','definition'),ds('PickDefs','cstOf','definition'),ds('PickDefs','DigFacts','interface'),ds('FactorLeProductSeven','coeff_mon_divDer'),ds('FactorLeProductSeven','diagK_binomCombF'),ds('PickVal','value_exact')],
      ['DT3'], ['2'], relation='Direct monomial coefficient proof includes all factorials and the actual plane/normal split.')
claim('DT6','Highest-weight cost of binomial correction',
      'A diagonal binomial polynomial of degree <=d increases a prefix largest highest-weight coordinate by at most d and preserves letter multidegrees. The proof uses the conjugation module of Euler operators and ordinary characteristic-zero highest-weight bounds.',
      'derived_simplification', [ds('FactorLeProductSeven','diagK_binomCombF'),ds('VBBMonomialOne','noAt','application'),ds('TwiceValuationFactorialProduct','NormTest','target_definition')],
      ['DT5'], ['3'], ['Characteristic-zero rational GL representation theory over the fraction field.'],
      relation='Field-level operator argument; it does not assume an integral direct sum of isotypic lattices.')
claim('DT7','Normal test with the exact scalar cY',
      'With w^2=p, cY=w^FNo p^D w^(-v_p(nu!)) makes cY e(X^nu) integral for the actual joint normal projector. Correcting by the inverse factorial unit modulo p^c gives NormTest and NoAt with scalar valuation FNo/2+D-v_p(nu!)/2 and highest-weight slack <=4c.',
      'faithful_translation', [ds('PickDefs','DnoOf','definition'),ds('PickDefs','JPOK','interface'),ds('PickDefs','NoAt','target_interface'),ds('VBBMonomialOne','noAt'),ds('FactorLeProductSeven','coefGe_of_inBB'),ds('TwiceValuationFactorialProduct','NormTest','definition')],
      ['DT4','DT6','IW4','PG3'], ['4'], ['The exact joint projector, whose denominator, self-adjointness and nested/disjoint compatibility are proved in IW/PG.', 'The actual local setting has w^2=p.'])
claim('DT8','Weighted coefficient selection and PickAt',
      'A unit coefficient of the input selects a digit block, normal joint type and coefficient Pc with b(Pc)+v_p(nu!)/2<=(VP+VN)/2. Normalize F2=z^(-1)Pc. The exact scalar k0=C_rho cY nu! z obeys v(k0)<=Ftot-FPl/2+Dn under SizeAt, and replacing the ideal normal factor gives pairing error >=c+Ftot-kappa_fl.',
      'faithful_translation', [ds('PickCore','pick_core'),ds('PickCore','gram_exponent_arithmetic'),ds('PickVal','value_exact'),ds('PickVal',"asm_coefGe'"),ds('PickDefs','SizeAt','input_interface'),ds('TwiceValuationFactorialProduct','PickAt','target_interface'),tw('PlaneCoeff','MemAt','retained_incoming_input')],
      ['DT5','DT7','DT11','CL7','CL8','IW4'], ['5'], ['Incoming MemAt places the selected plane coefficient in XX.', 'The signed datum and the explicit degree, joint-type, size and frame hypotheses must be supplied.'],
      relation='Reconstructs selection and all scalar/error calculations; does not treat the incoming word-closure condition as automatic.')
claim('DT9','Saturated tensor gluing of segment constraints',
      'For disjoint finite coefficient slots and saturated submodules X_j, the intersection of X_j tensor the other full slots equals the tensor product of all X_j. Prefix weight constraints define rational subspaces whose integral intersections are saturated; slicing, homogeneous components and equivariant renaming preserve those bounds.',
      'derived_simplification', [ds('MembDefs','ATL','target_interface'),ds('MembDefs','ValSlice','target_interface'),ds('MembDefs','ValComp','target_interface'),ds('MembDefs','ValRen','target_interface'),ds('DecIdentity','plane_dec'),ds('DecIdentity','normal_dec'),ds('DecIdentity','dec_identity')],
      [], ['6'], ['Finite degree truncation and a DVR coefficient ring.'], relation='Basis extension over a DVR proves the integral tensor statement directly; no integral semisimplicity is used.')
claim('DT10','Outgoing test assembly belongs to the actual symbol span',
      'Under MFH, Tied, BlockOK, NormTest, YY(24,60) and the fixed phi-multidegree, the assembled Gram/normal test satisfies MembAt. The margin s>=128c converts tau=T-s/2-60c to the even/odd XX separation and Bo/2-s bound. Saturated gluing, the carry Frobenius identity, physical degree and label estimates prove DecAt, AlgAt, DegAt and LabAt.',
      'faithful_translation', [ds('ExistsMapOfCoefGe','MFH','input_definition'),ds('ExistsMapOfCoefGe','MH','input_definition'),ds('ExistsMapOfCoefGe','DecAt','interface'),ds('ExistsMapOfCoefGe','AlgAt','interface'),ds('ExistsMapOfCoefGe','DegAt','interface'),ds('ExistsMapOfCoefGe','LabAt','interface'),ds('MembVB','valBd_of'),ds('MembVB','suppOK_of'),ds('ThresholdGeOddPosition','ar1'),ds('ThresholdGeOddPosition','ar3'),ds('MembXXb','cond_at'),ds('MembXXb','restXXG_b'),ds('MembDd','restDdG_holds'),ds('MembAlgF','plane_X'),ds('MembAlgF','alg_identity'),ds('MembDegF','oOf','definition'),ds('MembDegF','normDeg_bigM'),ds('MembDegF','restDegG'),ds('MembLabF','restLabG'),ds('DecIdentity','restDecG_of'),ds('ExistsMapOfCoefGe','membAt_core'),ds('TwiceValuationFactorialProduct','MembAt','target_interface'),tw('PlaneCoeff','thStar','definition'),tw('PlaneCoeff','Tied','input_definition')],
      ['DT7','DT9','PG10'], ['7'], ['All exact MFH, Tied, BlockOK, NormTest, YY and monomial phi-degree hypotheses; constructing the numerical frame system remains separate.'],
      relation='Pointwise admissibility is proved. The stronger raw degree inequality is noted, but no global threshold or valuation constant is reduced.')
claim('DT11','Incoming word-closure membership remains distinct',
      'The incoming MemAt hypothesis for the c0-word closure remains to be reconstructed: Lemma5aAt handles initial symbols; WordConditionAt transports them, and linearity gives the whole span. The reductions to Lemma5aGeneratorProductsAt, OneOpStep and WordBoundStep are identified, but their substantive prefix/twisted-substitution estimates are not claimed proved here.',
      'remaining_input', [tw('PlaneCoeff','MemAt','retained_input'),tw('MemLin','MemAtG','retained_input'),tw('MemRed','Lemma5aAt','retained_input'),tw('MemRed','WordConditionAt','retained_input'),tw('MemRed','memAt_of_wordConditionAt','reduction'),tw('Lemma5aGeneratorProducts','Lemma5aGeneratorProductsAt','retained_input'),tw('WordLossNonneg','OneOpStep','retained_input'),tw('WordLossNonneg','WordBoundStep','retained_input'),tw('WordLossNonneg','restWordStep_of','reduction')],
      [], ['8'], relation='A boundary of this human exposition, not an assertion of a Lean axiom, sorry, or defect. Selected-symbol dimension and complete frame/parameter supply remain separate too.')

out = dict(schema_version='1.0', artifact_version='0.5', date='2026-11-21',
           repository=dict(url=REPO,commit=COMMIT), claims=claims,
           source_files=[files[p] for p in sorted(files)],
           verification=dict(exact_source_ranges_and_hashes=True, local_lean_compilation=False, kernel_replay=False),
           status_definitions=dict(faithful_translation='Human proof of the cited interface under its explicit assumptions.', derived_simplification='Alternative human proof or stronger consequence, distinguished from the source proof.', remaining_input='Substantive argument not fully reconstructed here.'))
(OUT/'provenance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(claims=len(claims), source_files=len(files), source_links=sum(len(c['sources']) for c in claims))))
