#!/usr/bin/env python3
"""Bind PX1--PX10 to pinned model-comparison source and exact readable proof bytes."""
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
URL = 'https://github.com/CocoSgt/riemann-hypothesis-lean'
AV = 'src/Development/AutomorphicArithmetic/AutomorphicVarieties/'
CA = AV + 'CommutativeAlgebra/'
GM = CA + 'GradedModulesLength/'
SG = AV + 'SymplecticGSp4/'
HV = AV + 'HeightAndVanishing/'
DT = AV + 'ModularityArgument/ThresholdArguments/DenseThresholdCases/'
GE = 'src/Formalism/SharpRestriction/ValuationFrobeniusEpsilon/LeastPrimeTwists/QuotientShiftIrreducible/NoetherianQuotientCalc/'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}


def source(path, name, role='Matched definition or proof endpoint; readable reconstruction in the stated PX scope'):
    raw = (REPO / path).read_bytes()
    lines = raw.splitlines(keepends=True)
    starts = []
    for n, line in enumerate(lines, 1):
        m = re.match(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(?:def|theorem|lemma|abbrev|structure|class|instance)\s+([^\s:{(]+)', line.decode())
        if m:
            starts.append((n, m.group(1)))
    matched = [(n, s) for n, s in starts if s == name or (name.startswith('@') and s.rsplit('.', 1)[-1] == name[1:])]
    if len(matched) != 1:
        raise ValueError((path, name, matched))
    start, spelling = matched[0]
    end = min([n for n, _ in starts if n > start], default=len(lines) + 1) - 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    block = b''.join(lines[start - 1:end])
    files[path] = {'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                   'lines': len(lines), 'url': f'{URL}/blob/{PIN}/{path}'}
    return {'path': path, 'declaration': spelling, 'source_spelling': spelling,
            'line_start': start, 'line_end': end, 'sha256': sha(raw),
            'range_sha256': sha(block), 'range_bytes': len(block),
            'first_line': lines[start - 1].decode().rstrip('\n'),
            'url': f'{URL}/blob/{PIN}/{path}#L{start}-L{end}', 'role': role,
            'verified_equal_to_pinned_git_blob': True}

spec = {
 'PX1': {SG+'AGraded.lean':['aGraded_internal','@aGraded'],
  SG+'WeightAlgebraGeneratedDegreeTwo.lean':['aW_comb','aW_gen','weight_algebra_generated_degree_two','@aW'],
  CA+'OrbitVanishingLocal.lean':['IsWRing'],CA+'PartSpan.lean':['@part_span']},
 'PX2': {SG+'EntryMem.lean':['tDims','Model'],CA+'OrbitVanishingLocal.lean':['IsChart','SmoothPt','mDims'],
  SG+'ASmooth.lean':['exists_order','homog_gens','iota','main','count','@aSmooth'],
  CA+'ResMapBijective.lean':['satSq','cotLat']},
 'PX3': {SG+'TanGlob.lean':['hom_zero','unr_all','zOf_coc','zOf_sp','zOf_adic','zOf_tan','zOf_unr','wt_zero','wt_neg','@tanGlob'],
  SG+'QuotientSaturatedSquareTorsionFree.lean':['cotangent_rank_le_weight_count','quotient_saturated_square_torsion_free','spans_cotangent_transfer_equal_rank','factor_through_quotient_by_generators','derivation_zero_of_killing_generators','spans_cotangent_of_derivation_test','cotangent_rank_at_weight_eq_dims','@m1b'],
  CA+'OrbitVanishingLocal.lean':['M1'],CA+'ResMapBijective.lean':['SpansCot']},
 'PX4': {SG+'WcompMulHomog.lean':['wcomp_mul_homog','span_coeffs','@kerA'],
  SG+'SInternal.lean':['part_indep','quot_pres','@sInternal'],
  SG+'PtLift.lean':['pt_of_ft','pt_of_lin','ext_of_proj','@ptLift']},
 'PX5': {SG+'SpanMono.lean':['spanMono_prec','spanMono_top','spanMono_parts','spanMono_lift','@spanMono'],
  SG+'PtExt.lean':['@ptExt'],SG+'PtActInternal.lean':['@ptAct'],SG+'PtScale.lean':['pts_abs','@ptScale'],
  CA+'PointsFinite.lean':['pf_abs','pf_nonint','pf_step','pf_agree','pf_factor','@points_finite'],
  SG+'FgMapMk.lean':['fg_map_mk','@m2'],SG+'DecompSigmaOrd.lean':['Fin0','PtIn']},
 'PX6': {SG+'EptInt.lean':['cont_of_adic','@eptInt'],SG+'EiiUnit.lean':['eii_alg','eii_span','eii_abs','@eii'],
  SG+'PtInSmul.lean':['@ptIn'],SG+'GeAlgTop.lean':['@geAlg'],SG+'XvanExt.lean':['@xvanExt'],
  SG+'LocVanP.lean':['lv_gen','lv_dec','lv_red','@locVanP'],
  SG+'ExistsThirdIndexLinkedPair.lean':['lattice','line','root_mem','core','@exists_third_index_linked_pair'],
  SG+'TriComb.lean':['@tri_comb','@tri']},
 'PX7': {SG+'DiagChar.lean':['dchar','dual_prod','match_chars','perm_cases','open_ker','perm','@diagChar'],
  SG+'ContentBoundLevel.lean':['cob_fin','cob_conj','cover','pat_split','@diagonal_character_order_lt_of_stable_flag'],
  SG+'DiagCases.lean':['@diagCases'],SG+'SpanZero.lean':['@signs'],
  SG+'PtLimit.lean':['limit_graded','vanish_mono','@ptLimit'],SG+'TwoIrr.lean':['@twoIrr'],
  SG+'TorusConjugateCornerEntryEq.lean':['diagonal_type_corner_cases','@m3'],
  SG+'DecompSigmaOrd.lean':['NoEnd'],CA+'OrbitVanishingLocal.lean':['M3']},
 'PX8': {SG+'ConjTorus.lean':['block_of_intertwine','corner_zero','gsp_of_conj','torus_of_gsp','@conjTorus'],
  SG+'GaloisRepIneqOfAllIrreducibleNonvanishing.lean':['same_orbit_of_conjugate_reps'],
  CA+'OrbitVanishingLocal.lean':['SameOrbit']},
 'PX9': {SG+'ExistsLiftOfDerivationOnIdeal.lean':['extend_point_degree_zero_graded','exists_lift_of_derivation_on_ideal','derivation_kills_ideal_lifts','@m4'],
  SG+'TanScale.lean':['ts_agree','ts_factor','ts_ext','@tanScale'],
  SG+'RigidDiag.lean':['block_of_comm','diag_of_comm','@rigidDiag'],
  SG+'DecompSigmaOrd.lean':['RigidAt','AllIrr'],CA+'OrbitVanishingLocal.lean':['M4']},
 'PX10': {SG+'AVal.lean':['@aElt'],SG+'Nval.lean':['@nval'],
  SG+'GaloisRepIneqOfAllIrreducibleNonvanishing.lean':['exists_rep_family_from_points','covers_and_cotangent_length_bounds','@galoisRep_ineq_of_allIrreducible_nonvanishing'],
  SG+'DecompSigmaOrd.lean':['aVal','sha','Ineq'],SG+'MPrime.lean':['@mPrime'],
  CA+'OrbitVanishingLocal.lean':['M5','Covers','LemmaM']},
}
titles={
 'PX1':'Actual gradings and generation in degrees at most two',
 'PX2':'Invariant chart with exact saturated cotangent dimensions',
 'PX3':'Global tangent vanishing and all M1 spanning conditions',
 'PX4':'Exact equation ideal and lifting every algebraic point',
 'PX5':'Algebraic entry generation, actual point scaling and M2',
 'PX6':'Normalized actual points and complete matrix-pattern trichotomy',
 'PX7':'One-sided reducibility, two-sided irreducibility and M3',
 'PX8':'Normalized conjugacy, torus conjugacy and the exact point orbit',
 'PX9':'Actual dual-number lifting, infinitesimal torus and M4',
 'PX10':'Trace element, finite orbit cover and actual Selmer inequality',
}
deps={
 'PX1':[], 'PX2':['PX1'],
 'PX3':['PX2','RV7','DX6','AX6'],
 'PX4':['PX1'], 'PX5':['PX1','PX4'],
 'PX6':['AX3','AX6','AX8','DX1'],
 'PX7':['PX4','PX5','PX6','AX8','RV7'],
 'PX8':['PX5','PX6','PX7','AX6'],
 'PX9':['PX4','PX5','PX6','PX7','PX8'],
 'PX10':['PX1','PX2','PX3','PX4','PX5','PX6','PX7','PX8','PX9','RV3','SP1','SP6','SP7'],
}
inputs={
 'PX-C1':{'kind':'matched classical algebra leaves','name':'Noetherian power series, Nakayama, exact finite completion and weak Nullstellensatz',
  'statement_used':'Finite formal power series over a Noetherian ring are Noetherian; Nakayama for finite modules; I-adic completion is exact on finite modules over a Noetherian ring; maximal residue fields of a finite-type algebra over algebraically closed K equal K.',
  'urls':['https://stacks.math.columbia.edu/tag/0306','https://stacks.math.columbia.edu/tag/00DV','https://stacks.math.columbia.edu/tag/00MA','https://stacks.math.columbia.edu/tag/00FV'],
  'matching':'PX1 proves the finite-monomial reduction. PX2 proves the required cofinal invariant topology and recursive equivariant formal inverse. PX4 constructs a nonzero finite-type fibre by an explicit Reynolds retraction. Only the stated elementary completion and residue-field leaves are cited.'},
 'PX-C2':{'kind':'matched classical arithmetic leaves','name':'Finite local fields and the absence of everywhere-unramified extensions of Q',
  'statement_used':'The valuation on a finite extension of a complete discretely valued field is unique and its nonnegative elements are integral; Q has no nontrivial everywhere-unramified finite extension (Minkowski).',
  'url':'https://www.jmilne.org/math/CourseNotes/ANT.pdf',
  'matching':'Used after finite coefficient capture or on an individual algebraic element. PX3/PX7 pass through actual finite quotients of compact characters; no blanket assertion that a compact subset of Qbar_l is in a finite field is used.'},
 'PX-C3':{'kind':'matched classical arithmetic leaf supplied through DX1','name':'Finite local Tate duality and local Euler at p distinct from ell',
  'statement_used':'For finite residual modules at the actual decomposition group, h2(M)=h0(M-dual(1)) and h0-h1+h2=0 at p distinct from ell.',
  'supplier':'DX1, with original-place transport and exact cup-product normalization',
  'matching':'PX6 locVanP proves both invariant spaces vanish using the same sigma_p, residual cyclotomic value1 and actual root-character separation; this implies every local residual cocycle is a coboundary. No BlochKatoLocal input is used.'},
 'PX-R1':{'kind':'retained bespoke supplier','name':'Actual D.Fin0',
  'statement_used':'For every IsCO O R and every actual IsPt lift rho of D.rbar, the O-algebra adjoined by all entry monomials of full weight0 is finite over O.',
  'source':'DecompSigmaOrd.lean Fin0','supplier_frontier':'SymplecticFourImageDense, as used exactly in AX10'},
 'PX-R2':{'kind':'retained bespoke supplier','name':'Actual D.NoEnd',
  'statement_used':'Every actual algebraic-valued EPt with all matrices block diagonal has its {0,2} block matrix span strictly smaller than M2(K).',
  'source':'DecompSigmaOrd.lean NoEnd','supplier_frontier':'SymplecticFourImageDense, as used exactly in AX10'},
 'PX-R3':{'kind':'retained bespoke supplier','name':'Actual D.AllIrr D.RigidAt',
  'statement_used':'Every irreducible actual EPt rho and every actual PtIn over K[epsilon] reducing to rho has derivative [X,rho] with X in sp4(K).',
  'source':'DecompSigmaOrd.lean AllIrr and RigidAt',
  'supplier_frontier':'rigSp4_alt and its exact local Hodge and global adjoint prerequisites remain; this component does not equate a generic rigidity package with this assertion without its installation.'},
}
uses={
 'PX1':['PX-C1'],'PX2':['PX-C1'],'PX3':['PX-C1','PX-C2'],
 'PX4':['PX-C1'],'PX5':['PX-C1','PX-C2','PX-R1'],
 'PX6':['PX-C2','PX-C3'],'PX7':['PX-C2','PX-R1','PX-R2'],
 'PX8':['PX-R1','PX-R2'],'PX9':['PX-C1','PX-C2','PX-R1','PX-R2','PX-R3'],
 'PX10':['PX-R1','PX-R2','PX-R3'],
}
scopes={
 'PX1':'For the unchanged Raw/Good datum and any actual Model D, prove aGraded and aW, including directness, complete original degree-zero ring, finite generators in degrees plus/minus1/2, and fixed origin.',
 'PX2':'Prove literal aSmooth from the original Model.smooth, with ranks0,r,m,r-prime+1,1 at degrees-2,-1,0,1,2. IsChart is rational saturated-cotangent data; no integral formal smoothness or identification of a completed ring with its graded finite-sum algebra is claimed.',
 'PX3':'On the actual Model, derive literal TanGlob in weights -Psi and0 from DX6 and RV7, then m1b by the finite derivation separation test and equal-rank transfer. Gives every M1 field with original equations.',
 'PX4':'Prove exact kerA, induced quotient grading and every ptLift. The nonzero finite-type fibre is constructed using the first-weight-zero projection; no point-extension assertion is assumed.',
 'PX5':'Under actual Fin0, prove literal spanMono, ptExt for arbitrary target O-algebra, ptAct, ptScale to an actual EPt, and M2. Strict positive-valuation scaling and finite integral evaluation are proved, not assumed continuous.',
 'PX6':'For every actual EPt of Good D, prove finite integral coefficient capture, normalized diagonal projectors and literal tri. All root residual vanishing is actual Good.xvan, extended coordinatewise; the only local arithmetic leaf is DX1 finite local Tate/Euler.',
 'PX7':'Under actual Fin0 and NoEnd prove twoIrr. Under Fin0 alone prove m3. The diagonal-type character order, finite characters, RV7 split-cover argument, sign detection and block limit are all reconstructed.',
 'PX8':'Prove conjTorus on actual normalized irreducible points; with Fin0 and NoEnd use PX7 to prove same_orbit_of_conjugate_reps for the exact second torus on A. No arbitrary conjugacy-orbit substitution.',
 'PX9':'Under Fin0/NoEnd/actual irreducible rigidity, extend every point derivation killing I to an actual K[epsilon] representation and derive delta(f_n)=bnx(f_n). This proves literal M4 including actual PtIn witnesses.',
 'PX10':'Under the three exact actual arithmetic predicates and nonzero trace difference at every irreducible EPt, prove literal D.Ineq(g), finite original Selmer length, pairwise nonconjugate finite actual representation family and exact factor2 normalized trace bound. All internal G2 model comparisons are supplied.',
}

tex=(HERE/'main.tex').read_bytes(); lines=tex.splitlines(keepends=True); claims=[]
for cid in titles:
 start=next(i for i,line in enumerate(lines,1) if line.startswith(('\\paragraph{'+cid+':').encode()))
 end=next(i for i,line in enumerate(lines,1) if i>start and line.startswith(b'\\end{proof}'))
 retained=[k for k in uses[cid] if k.startswith('PX-R')]
 claims.append({'id':cid,'title':titles[cid],'statement':scopes[cid],
  'introduced_in':'0.27','depends_on':deps[cid],'input_ids':uses[cid],
  'status':'Complete conditional human proof; exact arithmetic predicates retained' if retained else 'Complete human proof in exact stated scope, with matched classical leaves',
  'mathematical_status':'conditional endpoint' if retained else 'closed in its exact quantified scope',
  'remaining_bespoke_inputs':retained,
  'proof_location':{'file':'symplectic_model_comparison/main.tex','paragraph':cid,'line_start':start,'line_end':end,'label':'claim:'+cid,'sha256':sha(b''.join(lines[start-1:end]))},
  'sources':[source(p,n) for p,names in spec[cid].items() for n in names],
  'source_relation':'Human reconstruction with proved simplifications; pinned ranges identify the exact source predicates and internal comparisons.',
  'component_ledger':'symplectic_model_comparison/provenance.json'})
for p,f in files.items():
 blob=subprocess.check_output(['git','-C',str(REPO),'show',PIN+':'+p])
 assert sha(blob)==f['sha256'],p
scope='Complete actual Model-to-intersection, point, tangent, trace and orbit comparison; original Fin0, NoEnd and actual irreducible RigidAt remain explicitly quantified arithmetic predicates. Model existence is supplied separately by MX10 from DX; no full CountII/III or automorphic catalogue is inferred.'
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
write(HERE/'provenance.json',{'schema':'rh-human-reconstruction-provenance/1','artifact_version':'0.27','date':'2026-11-22',
 'repository':URL,'commit':PIN,'component':'symplectic_model_comparison','scope':scope,
 'claims':claims,'source_files':list(files.values()),'dependency_graph':deps,'input_ledger':inputs,
 'component_input_boundary':{'original_objects':'Same Good D, Model, Omega, O, places, residual representation and normalization; Model quantified in comparison and instantiated by MX10.',
 'retained_arithmetic_inputs':['PX-R1','PX-R2','PX-R3'],'classical_leaves':['PX-C1','PX-C2','PX-C3'],
 'not_claimed':['Actual image density','Actual irreducible rigidity','Finite catalogue','Actual CountI/II/III/V','Full RH or Dirichlet GRH','Lean build or kernel replay']},
 'validation':{'source_files_checked_against_pinned_git_blobs':len(files),'claim_source_links':sum(len(c['sources']) for c in claims),'main_tex_sha256':sha(tex)}})
write(HERE/'classical_inputs.json',{'schema':'rh-classical-input-registry/1','artifact_version':'0.27','component':'symplectic_model_comparison','inputs':{k:v for k,v in inputs.items() if k.startswith('PX-C')}})
write(HERE/'remaining_inputs.json',{'schema':'rh-retained-supplier-registry/1','artifact_version':'0.27','component':'symplectic_model_comparison','inputs':{k:v for k,v in inputs.items() if k.startswith('PX-R')}})
write(HERE/'closure.json',{'schema':'rh-dependency-closure/1','artifact_version':'0.27','component':'symplectic_model_comparison','commit':PIN,'main_tex_sha256':sha(tex),
 'graph':deps,'closed_endpoints':[{'claim':k,'literal_interface':scopes[k],'retained_bespoke_inputs':[]}for k in ['PX1','PX2','PX3','PX4','PX6']],
 'conditional_endpoints':[{'claim':k,'literal_interface':scopes[k],'retained_bespoke_inputs':[i for i in uses[k] if i.startswith('PX-R')]}for k in ['PX5','PX7','PX8','PX9','PX10']],
 'same_object_bindings':['Original Omega, O and actual Good D','Actual Model R,S and graded finite-sum algebras B,A,SS','Exact kernel generated by original F,E,Z','Original origin and integral saturated cotangent','Every algebraic two-sided point, not selected generic points','Actual PtIn over dual numbers before rigidity','Exact second-torus orbits on A','Original trace of r0 and factor2 normalized valuation'],
 'simplifications':['Equivariant completion and explicit one-negative-variable invariant chart replace the long formal coefficient proof of aSmooth.','Explicit finite-monomial grouping handles completion versus algebraic grading.','Strongly connected components replace the source finite four-vertex case calculation.','Localizing at two opposite first-weight entries extends all dual-number points.','Normalized projectors and maximal-norm separation give both conjugacy and tangent torus comparisons.'],
 'noncircularity':['M1 uses RV7, not any count or intersection conclusion.','PX6 uses actual residual XVan plus finite local duality, not image density.','NoEnd and actual RigidAt are retained where used.','SP6 is used only after M1-M5 are proved on the same objects.','The finite cover is produced by SP6, never assumed to be an automorphic catalogue.'],
 'not_claimed':['Full source LocalPublishedTheorems/BlochKatoLocal package','Automatic passage from a named rigidity theorem to actual RigidAt','Actual CountII/III without image, rigidity and catalogue suppliers','Independent Lean verification']})
(HERE/'source_locators.txt').write_text('\n\n'.join(c['id']+' -- '+c['title']+'\n'+'\n'.join(s['declaration']+'\n'+s['url']+'\nrange SHA256 '+s['range_sha256'] for s in c['sources'])for c in claims)+'\n')
(HERE/'report.md').write_text('# Actual model comparison v0.27\n\n'+scope+'\n\n'+'\n'.join('- '+k+': '+titles[k]for k in titles)+'\n\nThe exact three remaining arithmetic predicates are written in main.tex and remaining_inputs.json. No source helper in the comparison is retained as a package alias.\n')
print(json.dumps({'claims':len(claims),'source_ranges':sum(len(c['sources'])for c in claims),'source_files':len(files),'main_tex_sha256':sha(tex)},indent=2))


