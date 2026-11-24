#!/usr/bin/env python3
"""Rebuild provenance for the common arithmetic character-seed packet."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
VERSION = '0.50'
COMPONENT = HERE.name
V = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
F = V + 'FrobeniusSmoothVectors/'
T = V + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'

source_specs = {
    'frame_defs': (F+'FrobeniusSplitPrimeDatum.lean', 'Original Gen, Hth, FrobeniusWitnessPrime, UFacts, Linked and HasFrameW'),
    'seed_defs': (V+'CurveDVRSpecialization/HostFrameEx.lean', 'Original GalLink, SeedClause, HasFrame, GdFrameEx and HostFrameEx'),
    'seed_conditions': (V+'IdeleGenerators/SlopeTestRemainingChoices.lean', 'Original Cong, SplitAt, auxiliary conditions and FieldPairCharacterTripleConditions'),
    'norm': (F+'ScNorm.lean', 'sc_norm: original integral norm and maximal ideal equivalence'),
    'teich': (F+'ScTeich.lean', 'sc_teich: Teichmuller lifts with exact original norm congruence'),
    'strip': (F+'ScStrip.lean', 'sc_strip: cyclotomic conductor stripping for every target group'),
    'quad': (F+'ScQuad.lean', 'sc_quad: actual embedded imaginary quadratic field'),
    'disc': (F+'ScDisc.lean', 'sc_disc: unramified quadratic discriminant'),
    'hth': (F+'HthPlace.lean', 'hth: exact cyclotomic power subgroup and local properties'),
    'theta': (F+'ScTheta.lean', 'sc_theta: order-ell auxiliary character with literal kernel'),
    'om': (F+'SoCls.lean', 'sc_om: cyclotomic factorization and complex conjugation'),
    'cong': (F+'ScCong.lean', 'sc_cong: norm-square congruence returns to original residue field'),
    'auxw': (F+'AuxwEx.lean', 'auxw_ex: one auxiliary prime for every preassigned modulus'),
    'seed': (F+'SeedCl.lean', 'seed_cl: one Q before all later compatible CM fields and primes'),
    'field': (F+'FieldEx.lean', 'field_ex: literal actual abelian-CM fixed field and maximal real subgroup'),
    'gd_gen': (F+'SqrtDiscr.lean', 'gen_gd: original Dat entry, including the seed-relevant clauses'),
    'host_gen': (F+'GenHost.lean', 'gen_host: original CountV host entry and separate kernel guard'),
    'gd_ex': (F+'GdEx.lean', 'gd_ex: install SeedClause on the same frame and marked element'),
    'host_ex': (F+'HostEx.lean', 'host_ex: install host SeedClause on the same frame and marked element'),
    'frame_ex': (F+'FrameEx.lean', 'frame_ex: remaining large-frame construction and exact choice order'),
    'gd': (V+'HeightAndVanishing/Counts.lean', 'Original GD and CountV guards'),
    'host': (V+'UnitaryThreeDeformations/IsHostFrame.lean', 'Original HostData and original rational host-frame fields'),
    'dat': (V+'UnitaryThreeGroups/RhoKApply.lean', 'Original Dat, coefficient rings and embeddings'),
    'dat_facts': (V+'UnitaryThreeGroups/DatFacts.lean', 'Original parity, inertia, residual and quadratic consequences'),
    'linked_alt': (T+'PlDefs.lean', 'Full LinkedEndEAlt contract; retained future consumer'),
    'linked_proof': (T+'LinkedEndE.lean', 'LinkedEndEAlt proof consumes both actual automorphic seeds and common coefficients'),
    'gd_end': (T+'GdEndOf.lean', 'GdEndAlt installer retains frame, seeds, local and descent hypotheses'),
    'dn_ends': (T+'DnEnds.lean', 'Shared ordinary-end and host support interfaces'),
    'coh_hyp': (V+'GaloisCochains/GLinkQuot.lean', 'GC.Hypotheses2 and exact original FLink'),
}

relations = {
    1: ([], ['norm','teich']),
    2: ([], ['strip','seed_conditions','seed']),
    3: ([], ['quad','disc']),
    4: ([2], ['hth','theta','frame_defs']),
    5: ([2], ['auxw','frame_defs']),
    6: ([1,2,3], ['seed','teich','om','frame_defs']),
    7: ([1,2,3,4,6], ['seed','seed_defs','seed_conditions','cong']),
    8: ([3], ['field','frame_defs']),
    9: ([3,6,7], ['gd_gen','gd','dat','dat_facts','seed']),
    10: ([6,7], ['host_gen','host','seed']),
    11: ([7,9,10], ['gd_ex','host_ex','seed_defs','frame_defs','frame_ex']),
}

external = [
    {'id':'CAF_COMPLETE_DVR_BACKGROUND','kind':'classical_algebraic_background',
     'scope':'Finite complete DVRs over Z_ell, Hensel lifting with a simple root, residue finite fields, and factorization into a unit and uniformizer power. The norm and actual Teichmuller congruence are proved in CAF1.',
     'source_keys':['norm','teich']},
    {'id':'CAF_LOCAL_CYCLOTOMIC_BACKGROUND','kind':'classical_algebraic_number_theory_background',
     'scope':'Galois decomposition/inertia and completions; cyclotomic polynomials and their Eisenstein shifts; prime-to-residue-characteristic roots lie in unramified extensions. The precise conductor-stripping and kernel arguments are proved in CAF2 and CAF4.',
     'source_keys':['strip','hth','theta','auxw']},
    {'id':'CAF_GALOIS_AND_TRACE_BACKGROUND','kind':'classical_algebraic_number_theory_background',
     'scope':'Finite/infinite Galois correspondence, extensions of embeddings, CM maximal-real fields, and nondegenerate finite-field trace. CAF3 and CAF8 prove the actual field identifications and discriminant consequence.',
     'source_keys':['quad','disc','field']},
    {'id':'CAF_QUADRATIC_CONDUCTOR_BACKGROUND','kind':'classical_quadratic_reciprocity_background',
     'scope':'The primitive quadratic Kronecker character of a fundamental discriminant and finite Gauss-sum evaluation. CAF9 explains the cyclotomic containment through its explicit Gauss sum; no general abelian reciprocity or automorphy theorem is inferred.',
     'source_keys':['gd_gen','dat_facts']},
    {'id':'CAF_ORIGINAL_GEN_OR_SEED_CLAUSES','kind':'original_theorem_antecedent',
     'scope':'The original Gen record remains an antecedent of seed_cl and auxw_ex. The proof uses its explicitly listed subset S. CAF9/CAF10 supply that subset for the original Dat/HostData without asserting unused Gen fields.',
     'source_keys':['frame_defs','seed']},
    {'id':'CAF_ORIGINAL_L_W_COMPATIBILITY','kind':'original_theorem_antecedent',
     'scope':'After Q is fixed: arbitrary abelian CM L, literal G_L=U_L intersect ker eta, witness prime w, w=1 mod Q, U_L subset Hth, and a residual-square separator in G_L. These are exactly the original seed_cl later inputs.',
     'source_keys':['seed','seed_defs']},
    {'id':'CAF_ORIGINAL_UFACTS','kind':'original_theorem_antecedent',
     'scope':'Original UFacts remains the input of field_ex; the proof uses its open, abelian-quotient and all-complex-conjugation clauses. No actual U_m satisfying every UFacts clause is newly claimed.',
     'source_keys':['field','frame_defs']},
    {'id':'CAF_ORIGINAL_DAT_HOSTDATA','kind':'original_arithmetic_datum_antecedent',
     'scope':'All original Dat/GD and HostData hypotheses remain in their two separate specializations. The Dat genericity guard is not transferred to the host. Host ell=3 is retained.',
     'source_keys':['gd','host','dat','gd_gen','host_gen']},
    {'id':'CAF_SUPPLIED_HASFRAMEW','kind':'explicit_unsupplied_producer_antecedent',
     'scope':'CAF11 consumes one actual HasFrameW at the already chosen Q, including its GalLink, Ok and Big. The actual large frame and its cohomological suppliers remain to be reconstructed. The same g1 gives the seed-square witness.',
     'source_keys':['frame_ex','gd_ex','host_ex']},
]
ext_uses = {
    1:['CAF_COMPLETE_DVR_BACKGROUND'],
    2:['CAF_LOCAL_CYCLOTOMIC_BACKGROUND'],
    3:['CAF_GALOIS_AND_TRACE_BACKGROUND','CAF_ORIGINAL_GEN_OR_SEED_CLAUSES'],
    4:['CAF_LOCAL_CYCLOTOMIC_BACKGROUND'],
    5:['CAF_LOCAL_CYCLOTOMIC_BACKGROUND','CAF_ORIGINAL_GEN_OR_SEED_CLAUSES'],
    6:['CAF_ORIGINAL_GEN_OR_SEED_CLAUSES'],
    7:['CAF_ORIGINAL_GEN_OR_SEED_CLAUSES','CAF_ORIGINAL_L_W_COMPATIBILITY'],
    8:['CAF_GALOIS_AND_TRACE_BACKGROUND','CAF_ORIGINAL_UFACTS'],
    9:['CAF_QUADRATIC_CONDUCTOR_BACKGROUND','CAF_LOCAL_CYCLOTOMIC_BACKGROUND','CAF_ORIGINAL_DAT_HOSTDATA'],
    10:['CAF_LOCAL_CYCLOTOMIC_BACKGROUND','CAF_ORIGINAL_DAT_HOSTDATA'],
    11:['CAF_SUPPLIED_HASFRAMEW'],
}

subcontracts = [
    {'id':'original_sc_norm_and_sc_teich','claim':'CAF1'},
    {'id':'full_original_sc_strip_and_SplitAt_return','claim':'CAF2'},
    {'id':'original_quadratic_field_and_discriminant','claim':'CAF3'},
    {'id':'full_original_hth_and_sc_theta','claim':'CAF4'},
    {'id':'full_original_auxw_ex','claim':'CAF5'},
    {'id':'fixed_core_seed_characters_before_CM_field','claim':'CAF6'},
    {'id':'full_original_seed_cl','claim':'CAF7'},
    {'id':'full_original_field_ex','claim':'CAF8'},
    {'id':'actual_Dat_seed_scope_and_modulus','claim':'CAF9'},
    {'id':'actual_CountV_host_seed_scope_including_ell3','claim':'CAF10'},
    {'id':'same_marked_frame_seed_installation','claim':'CAF11'},
]

report = '''COMMON ARITHMETIC CHARACTER SEEDS — v0.50

RESULT
CAF1–CAF11 prove the full original SeedCl.seed_cl, AuxwEx.auxw_ex and
FieldEx.field_ex, with their literal source input scopes. The seed theorem
chooses Q before every later compatible CM field L and witness prime w.
It supplies the actual quadratic field, character triple, prime-to-ell
order, parity, exact residual norm congruence, nondegenerate square witness,
local splitting, and quadratic discriminant condition.

Two actual arithmetic applications are now explicit:
  Dat: M=ell*N*|disc K| and Q=|disc K|*N_{ell'}.
  CountV HostData: M=ell*N and Q=N_{ell'}^2.
The host proof keeps ell=3, uses its dyadic kernel witness and does not
borrow the Dat restriction ell-1 not dividing 2e. Its seed input does not
need the additional host size/order inequalities, which remain part of
the original HostData and remain available downstream.

CAF8 gives L=Omega^(U intersect ker eta), literally G_L=U intersect ker eta
and G_{L+}=U. CAF11 uses the original GalLink and Ok marked element g1 to
provide the final square witness. That same g1 and every other frame field
are retained when the character seed is installed; no later frame choice
is made independently. An elementary cyclotomic argument supplies the
auxiliary prime w=1 modulo every requested Q; no full Dirichlet progression
theorem is required by this particular construction.

WHAT REMAINS
This is character-seed data, not the rank-two/rank-three automorphic seed
representations. Full GdFrameEx and HostFrameEx still require the actual
large HasFrameW: the real quadratic subgroup H0, full UFacts for
U_m=H0 intersect Hth intersect Hb intersect Hlay, one class-rank bound C0
uniform before m, strict cohomology classes, the actual linking quotient
and local frame, and the remaining cohomological Ok fields. The full Gen
entry contracts are not claimed merely because their seed-relevant subset
has been proved. Their unused fields remain needed by frame_ex.

The original shared LinkedEndEAlt continues to require both automorphic
seeds, general ModUAlt, common coefficient extension and actual local
inputs. GdEndAlt-to-original-GdEnd still requires exact matching. No selected
whole obligation is closed by this packet, and no whole RH/GRH completion
is asserted.

COUNTV DICTIONARY
Keep the rational host frame over G_{Q,S}, eta4, Psi=epsilon^e*psi,
S={primes dividing ell*N}, and the literal coefficient modules distinct
from the auxiliary cohomological frame Phi over G_{L+}. For the host,
Hb=ker(kappa_B); for Dat, Hb=G_Q. The HOST_FRAME_LENGTH, HostVanE,
HostXpp and CountV normalized-length transports remain separate.

NEXT BOUNDED PRODUCERS
1. Continue FrameEx with UFacts and RankLeOfCardLe.b0 at their full source
   quantifiers, consuming the now-written AuxwEx and FieldEx.
2. Reconstruct strict cocycles and the quotient/local FLink, then all Ok
   fields on one frame; retain GC.Hypotheses2 exactly.
3. Develop both actual automorphic seeds and the universal LinkedEndEAlt
   alongside the frame branch; keep common L, g1, iota and coefficients.

VALIDATION AND PROVENANCE
All source files are copied from, and byte-compared with, the pinned Git
blob. Source excerpts and range hashes are supplied. Numbered proof blocks
have separate hashes; reviews can bind to those hashes. No Lean replay is
claimed. The chapter is checked in two-pass draft TeX without a PDF.
'''

def sha(b): return hashlib.sha256(b).hexdigest()
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    repo=args.repo.resolve()
    actual=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
    if actual!=PIN: raise ValueError(('unexpected source HEAD',actual))
    sources={};files={};excerpts=[]
    for key,(rel,title) in source_specs.items():
        data=(repo/rel).read_bytes()
        pinned=subprocess.check_output(['git','-C',str(repo),'show',PIN+':'+rel])
        if data!=pinned: raise ValueError(('source differs from pin',rel))
        lines=data.splitlines(keepends=True)
        target=ROOT/'source_snapshot_v0_50/arithmetic'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        url='https://github.com/CocoSgt/riemann-hypothesis-lean/blob/'+PIN+'/'+rel
        files[rel]={'path':rel,'sha256':sha(data),'bytes':len(data),'line_count':len(lines),
          'verified_equal_to_pinned_git_blob':True,'url':url,
          'snapshot_path':str(target.relative_to(ROOT))}
        sources[key]={'id':'CAF_SRC_'+key.upper(),'path':rel,'declaration':title,
          'line_start':1,'line_end':len(lines),'source_commit':PIN,
          'full_file_sha256':sha(data),'file_sha256':sha(data),'range_sha256':sha(data),
          'range_bytes':len(data),'verified_equal_to_pinned_git_blob':True,
          'url':url+f'#L1-L{len(lines)}'}
        excerpts.append('['+sources[key]['id']+'] '+title+'\n'+sources[key]['url']+'\n'+data.decode())
    text=(HERE/'main.tex').read_text();main_sha=sha(text.encode())
    blocks={m.group(1):m for m in re.finditer(r'% BEGIN (CAF\d+)\n.*?% END \1\n',text,re.S)}
    expected={'CAF'+str(i) for i in relations}
    if set(blocks)!=expected:raise ValueError('claim set mismatch')
    hashes={cid:sha(m.group().encode()) for cid,m in blocks.items()}
    reviews=[]
    for p in sorted(set(HERE.glob('review_*.json')) | set(HERE.glob('independent_review*.json'))):
        v=json.loads(p.read_text())
        if v.get('result',v.get('status'))!='PASS':continue
        ids=[]
        review_claims=v.get('claims_reviewed',v.get('reviewed_claims',[]))
        full_hash=v.get('proof_file_sha256',v.get('main_sha256',v.get('main_tex_sha256')))
        if full_hash is not None and full_hash!=main_sha:raise ValueError(('stale whole-proof review',p))
        for entry in review_claims:
            cid=entry if isinstance(entry,str) else entry.get('id',entry.get('claim'))
            expected_hash=(review_claims.get(cid) if isinstance(review_claims,dict) else v.get('proof_hashes',{}).get(cid)) if isinstance(entry,str) else entry.get('proof_range_sha256',entry.get('block_sha256'))
            if expected_hash is None and full_hash==main_sha:expected_hash=hashes.get(cid)
            if cid not in hashes or expected_hash!=hashes[cid]:raise ValueError(('stale review',p,cid))
            ids.append(cid)
        reviews.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),
          'reviewer':v.get('reviewer'),'result':'PASS','proof_file_sha256':main_sha,
          'reviewed_blocks_unchanged':True,'claims':ids,'scope':v.get('scope')})
    reviewed={cid for r in reviews for cid in r['claims']}
    status='complete_at_stated_scope_independently_reviewed' if expected<=reviewed else 'complete_at_stated_scope_pending_independent_review'
    claims=[]
    for i,(deps,ss) in relations.items():
        cid='CAF'+str(i);m=blocks[cid];start=text[:m.start()].count('\n')+1
        title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',m.group(),re.S).group(1)
        claims.append({'id':cid,'title':title,'introduced_in':VERSION,'classification':'B',
          'depends_on':['CAF'+str(d) for d in deps],
          'external_input_ids':ext_uses[i],'published_input_ids':[],
          'proof_location':{'file':COMPONENT+'/main.tex','label':'claim:'+cid,
            'line_start':start,'line_end':start+m.group().count('\n')-1,
            'sha256':hashes[cid],'bytes':len(m.group().encode())},
          'sources':[sources[k] for k in ss],'source_proof_is_not_human_proof':True,
          'status':'complete_at_stated_scope_independently_reviewed' if cid in reviewed else 'complete_at_stated_scope_pending_independent_review',
          'independent_review_files':[r['file'] for r in reviews if cid in r['claims']]})
    for e in external:e['source_bindings']=[sources[k] for k in e['source_keys']]
    config={'component':COMPONENT,'artifact_version':VERSION,'source_commit':PIN,
      'proof_file_sha256':main_sha,'subcontracts':subcontracts,
      'endpoint_claim':'CAF7','field_endpoint_claim':'CAF8','frame_installation_claim':'CAF11',
      'original_admissibility_not_weakened':True,'selected_producer_closed':False,
      'fixed_before_later_fields':['Omega','O','eta','Psi','sigma','B','M','Q','K0','chi_prime','eta_prime','j'],
      'later_inputs':['L','w','abelian_CM_and_literal_Galois_subgroups','witness_prime','w_mod_Q','U_L_subset_Hth','residual_square_separator'],
      'not_claimed':['full GdFrameEx or HostFrameEx','actual HasFrameW existence','both automorphic seed representations','general ModUAlt or PfromAut','LinkedEndEAlt producer','GdEndAlt-to-original-GdEnd','AUT_UNRAM_COEF selected closure','THM_S6_S selected closure','HOST_FRAME_LENGTH or HostVanE or HostXpp transport','full RH or Dirichlet GRH completion'],
      'retained_foundations':[e['id'] for e in external],
      'host_ell3_retained':True,'Dat_genericity_guard_not_moved_to_host':True,
      'no_lean_replay':True}
    write('contracts.json',{'schema':'rh-human-component-contract/1',**config})
    write('original_contracts.json',{'schema':'rh-human-component-contract/1',**config})
    write('provenance.json',{'schema':'rh-human-component-provenance/1',**{k:config[k] for k in ['component','artifact_version','source_commit','proof_file_sha256']},
      'status':status,'claims':claims,'inherited_human_inputs':[],
      'boundary_human_references':[], 'classical_and_foundational_inputs':external,
      'independent_reviews':reviews,'source_proof_is_not_human_proof':True,
      'dependency_convention':'depends_on lists only numbered human proof claims; original antecedents and classical background are separately named. The actual large frame and automorphic seeds remain open.',
      'root_ledger_modified':False,'frozen_artifacts_modified':False})
    write('closure.json',{'schema':'rh-human-component-closure/1',**{k:config[k] for k in ['component','artifact_version','source_commit','proof_file_sha256']},
      'status':status,'closed_subcontracts':subcontracts,
      'proposed_global_frontier_leaf_closures':[],'new_global_frontier_leaf_closures':[],
      'foundation_retention_explicit':True,'independent_reviews':reviews,
      'pending':sorted(expected-reviewed,key=lambda s:int(s[3:])),
      'AUT_UNRAM_COEF_remains_open':True,'THM_S6_S_remains_open':True,
      'GdFrameEx_and_HostFrameEx_remain_open':True,
      'both_automorphic_seed_producers_remain_open':True})
    write('source_manifest.json',{'schema':'rh-source-manifest/1','component':COMPONENT,'source_commit':PIN,'files':list(files.values()),'ranges':list(sources.values())})
    write('retained_foundations.json',external)
    write('classical_inputs.json',{'schema':'rh-classical-input-registry/1','component':COMPONENT,'inputs':external})
    write('published_inputs.json',[])
    write('claim_dag.json',{'schema':'rh-human-claim-dag/1','component':COMPONENT,'claims':[{'id':c['id'],'depends_on':c['depends_on']} for c in claims]})
    (HERE/'source_excerpts.txt').write_text('\n\n'.join(excerpts))
    (HERE/'report.txt').write_text(report+f'\nPin: {PIN}\nMain SHA256: {main_sha}\nStatus: {status}\nClaims: {len(claims)}; source files: {len(files)}\n')
    write('hashes.json',{'component':COMPONENT,'artifact_version':VERSION,
      'hashes':{p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='hashes.json'}})
    print(json.dumps({'component':COMPONENT,'claims':len(claims),'source_files':len(files),'main_sha256':main_sha,'status':status},indent=2))

if __name__=='__main__':main()
