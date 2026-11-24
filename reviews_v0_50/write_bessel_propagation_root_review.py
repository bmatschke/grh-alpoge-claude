#!/usr/bin/env python3
"""Bind the root's completed mathematical and original-contract BSP review."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/workspace/scratch/249d32c24541/formal_source')
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
COMP='bessel_weight_propagation_v50'
EXPECTED='f78595d1760e862c84f0683352f1d750ec0000dec83e1dec82e80c80d744546d'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=[
 'The zero-division case is explicitly excluded by the original StepGap inequality itself. The two original inequalities imply every hNeed term and beta/2 > 2nq0, beta/4 > 2rn squared. No permitted k or r is removed.',
 'The isometric lowest-type embedding gives every literal PsiDatum field for arbitrary n and signature. DC8 and DC9 apply to the broader unitary input; the energy/Taylor argument in DC10 extends to it. The diagonal initial type in the direct sum proves unitary equivalence of cyclic closures, and transports actual coefficient orthogonality. No a priori discrete-series classification is assumed for the input.',
 'Differentiation of the exact lowest-type coefficient identity gives the original ordered Capelli polynomial and its exact shift. The residual is in the closed group-generated span and orthogonal to that same span. Centrality then extends the identity from V to the entire generated module, without assuming ambient irreducibility.',
 'The original stabilizer fixes x-star both for r positive and for r zero. H-unitarity gives both multiplier invariances. The standard derivative and negative dual derivative, entry-sum bounds and allowed z=0 cases agree with the literal MultStatement.',
 'The same reciprocal norm power controls every translated derivative, with a uniform bound on a fixed neighborhood of the differentiation parameter. Dominated differentiation proves the original period identity. Source Eab/EabV are complexifications of real right derivatives; a smooth real local retraction therefore supplies exactly the required local ambient meaning.',
 'The polar eigenvalue bound and Jacobian give exponential radial decay when b > 2nq0, with only a polynomial shell factor. The inverse norm identity and submultiplicativity hold in the original unitary group and all Haar normalizations are allowed.',
 'Unimodularity is established from the adjoint trace. The double integral is controlled by norm(phi) in L1 times norm(F) in L2 times norm(gamma) in L2. Four-vector orthogonality gives the exact scalar norm(f) squared divided by d. Continuity and positive Haar mass on open sets upgrade the result from testing to every point.',
 'The supplied W-prime lowest type generates the rigid cyclic model from BSP2; all original compact stability and Casimir hypotheses remain. Integrability identifies toL2 with the actual class. Scaling in the linear inner-product slot gives the exact finProj kernel and pointwise formula.',
 'For A,B at least one and G0 at most AB, the displayed product bound is valid with beta/4 and beta/2. Each separate factor is integrable at the original thresholds. Fubini and x0=P inverse y P recover exactly the original two-translate vector period with all characters, measures and Cayley factors intact.',
 'A nonzero vector in the original irreducible W-prime has a representative in Wf by the exact image relation. The original period-injectivity premise forces a nonzero period of that representative. BSP8 and BSP9 give every literal BesselNZ witness. Existence of the shifted quotient and its injectivity is retained, not inferred.'
]
here=ROOT/COMP;raw=(here/'main.tex').read_bytes();assert sha(raw)==EXPECTED
ledger=read(here/'provenance.json');assert len(ledger['claims'])==len(notes)==10
claims=[]
for c,note in zip(ledger['claims'],notes):
    pl=c['proof_location'];block=b''.join(raw.splitlines(keepends=True)[pl['line_start']-1:pl['line_end']])
    assert sha(block)==pl['sha256']
    claims.append({'id':c['id'],'status':'PASS','block_sha256':sha(block),'reasoning':note})
manifest=read(here/'source_manifest.json');blobs={};ranges=set()
for f in manifest['source_files']:
    path=f['path'];b=subprocess.check_output(['git','show',PIN+':'+path],cwd=SOURCE)
    assert sha(b)==f['sha256'];assert (ROOT/f['snapshot_path']).read_bytes()==b;blobs[path]=b
for c in ledger['claims']:
    for r in c['sources']:
        b=b''.join(blobs[r['path']].splitlines(keepends=True)[r['line_start']-1:r['line_end']])
        assert sha(b)==r['range_sha256'];ranges.add((r['path'],r['line_start'],r['line_end']))
for h in ledger['inherited_human_inputs']:assert sha((ROOT/h['file']).read_bytes())==h['sha256']
report='# Independent mathematical review: BSP1–BSP10\n\n'
report+='Reviewer: root. Author: bessel_nonvanishing. Result: PASS at the exact original scope.\n\n'
report+='The complete chapter was read against the literal PsiDatumStatement, CapValStatement, PerStatement, MultStatement and FinStatement contracts. The supporting DC4 and DC8–DC10 arguments, source scalar/vector right derivatives, and the final pointwise/Fubini calculations were checked independently.\n\n'
for c in claims:report+='## '+c['id']+'\n\n'+c['reasoning']+'\n\n'
report+='## Exact boundary\n\nTMapStatement, TMapDStatement, EigStatement, EvalPStatement, EvalMStatement, QuotPStatement and QuotMStatement remain suppliers for the original StepStatement. The whole BesselNVGap and the supplied-form global setting remain conditional; Forms0 is retained. The source pin, all 32 source files, all cited ranges, all ten proof blocks and four inherited proof files were verified separately from the mathematical review. No whole selected obligation closes and no Lean replay is asserted. There are no unresolved findings.\n'
rp=here/'independent_review.md';rp.write_text(report)
dump(here/'independent_review.json',{
 'schema':'rh-independent-mathematical-review/1','artifact_version':'0.50','component':COMP,
 'reviewer':'/root','author':'/root/bessel_nonvanishing','status':'PASS','source_commit':PIN,
 'proof_file':COMP+'/main.tex','proof_file_sha256':EXPECTED,'claims_reviewed':claims,
 'review_report':COMP+'/independent_review.md','report_sha256':sha(rp.read_bytes()),
 'source_file_count_verified':len(blobs),'source_range_count_verified':len(ranges),
 'inherited_files_verified':len(ledger['inherited_human_inputs']),
 'corrections_resolved':[],'unresolved_findings':[],
 'scope':'Full original GapNeed, PsiDatum, CapVal, Mult, Per and Fin statements at their original premises; the two one-unit propagation producers remain explicit.'})
print(json.dumps({'component':COMP,'result':'PASS','claims':len(claims),'source_files':len(blobs),'source_ranges':len(ranges)}))
