#!/usr/bin/env python3
"""Configure the next increment only after both exact closure reviews are bound."""
from pathlib import Path
import collections
import hashlib
import json

ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads((ROOT/p).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
old=read('increment_v0_46.json')
graph=read('dependency_audit_v0_46/obligation_map.json')
nodes={n['id']:n for n in graph['nodes']}
components=['type_ii_rigidity_v47','kato_input_assembly_v47','row_finiteness_v47',
 'adelic_setting_v47','canonical_cusp_connection_v47','principal_cusp_lattices_v47',
 'local_growth_suppliers_v47']
authors=dict(zip(components,['main_proof_rigidity','main_proof_rigidity','root','root',
 'ordinary_structure','ordinary_structure','global_estimates']))
ledgers={c:read(c+'/provenance.json') for c in components}
closure_components={'RIG_II':'type_ii_rigidity_v47','TASK_INP_Z_ASSEMBLY':'kato_input_assembly_v47'}
closure_reviews={}
for key,component in closure_components.items():
 for p in sorted((ROOT/component).glob('review_*_root.json')):
  r=json.loads(p.read_text()); exact=r.get('selected_whole_contract_reviewed',{})
  if exact.get('id')!=key:continue
  assert r['result']=='PASS' and r['proof_sha256']==sha((ROOT/r['proof_file']).read_bytes())
  assert exact['full_original_contract_closed_in_stated_scope']
  assert exact['baseline_contract_sha256']==sha(nodes[key]['contract'].encode())
  closure_reviews[key]=str(p.relative_to(ROOT))
 assert key in closure_reviews,('missing exact whole-contract review',key)
closed={
 'RIG_II':dict(category='B',claims=[c['id'] for c in ledgers['type_ii_rigidity_v47']['claims']],
  conclusion='Entire literal RigII: every marked original type-II point, under its exact universal extension-modularity antecedent, has vanishing for the full nine-dimensional polarized adjoint.',
  method='Actual local ordered flag, middle/determinant character killing, explicit rank-two extension and full infinite-cyclotomic irreducibility; exact Kato critical twist, quadratic base change/polarized Thorne application, and concrete direct-sum projections and primitives.',
  boundary='Original modularity antecedent and precisely matched classical/cohomological/period foundations retained. OneChar and AutomorphyUnramifiedCoefficients are separate producers.'),
 'TASK_INP_Z_ASSEMBLY':dict(category='B',claims=[c['id'] for c in ledgers['kato_input_assembly_v47']['claims']],
  conclusion='The complete original CohInp/InpZ record with the exact local/global cohomology, LemmaK, LemmaM/LemmaMprime/LemmaP, RigII, AdVanishK and rank-three congruence fields on their original objects.',
  method='Named human proofs supply each original record field, keeping the uniform LemmaK witness before all later arithmetic inputs and inserting KTR/RNC only at their exact fields.',
  boundary='This closes the selected assembly task and supplies the original input record. It does not supply the independent one-character length theorem or the common unramified-coefficient automorphy package.')
}
conclusions=[
 'KTR reconstructs the full original KatoUse, KatoTwo and RigII. Kato Theorem14.2(1) is applied at weight2e+1 and twist e, with the paper\'s Bcris/unramified conditions and inverse-arithmetic-Frobenius polynomial checked directly. The actual local point gives the needed inertia flag from ordIdeal contained in It; prime-to-ell inertia and the class-number condition kill the middle and determinant characters. The corner extension is explicit and irreducible on the full infinite cyclotomic kernel. Actual quadratic GL2 base change and its symmetric polarization supply Thorne\'s corner-adjoint vanishing. Concrete projections decompose all nine adjoint coordinates into that corner, W, W times the quadratic character, and the quadratic scalar line, producing the required primitive for every original cocycle. The original modularity antecedent is retained.',
 'KIZ supplies the entire original CohInp/InpZ record from the completed exact human inputs. It preserves the local period model, normalized finite cohomology, original uniform LemmaK constant and every later coefficient datum, and inserts the completed LemmaM/LemmaMprime/LemmaP, KTR RigII, AdVanishK and RNC congruence integer at their literal fields. The independent original OneChar and AutomorphyUnramifiedCoefficients producers remain open.',
 'RFD proves the full original RowsFinDim with arbitrary locally constant supported e, arbitrary original unit vectors, and all original measures and weak integral operators. One compact-open level is chosen from e. The exact adelic quotient splits into finitely many arithmetic real components; the matched Harish-Chandra finite-multiplicity theorem applies there. The Schur projector\'s compression identity gives an explicit injection from its range into bounded intertwiners. This proves finite dimensionality without adding idempotence, smoothness, compact-finiteness, gap or cuspidality assumptions.',
 'ASG constructs eight actual dependent blocks of the original adelic setting: unitary instance, integral lattice/flags, finite character, reference frame, transport matrices, automorphic bundle, finite representation block, and subgroup/quotient measures. The original Forms0 produces an extra isotropic vector. Steinitz decomposition and a trace-one triangular correction give the prescribed integral hyperbolic frame; an explicit ideal-class/primitive-vector argument supplies all negative word vectors and every FixedHyp field. Split finite-adeles prove full generic ScRefExists and ScXuExists even for arbitrary supplied reference frames. Original gap and earlier discrete-series decay supply the full bundle. The original Bessel W, measured-field, Siegel-Weil ties, arithmetic count and common-family producers remain explicit.',
 'CNC constructs the entire original IsNab connection over every original coefficient algebra, including nonreduced and nonlocal rings. The full tangent eigenframe gives compatible global formal jets; normalized rigidified generators and proper base functions give every biextension law. A formal logarithm, two explicit symmetric-cocycle primitives, a separability-idempotent correction and the antisymmetric half correction prove the full generic canonical-gauge theorem. Unique germs of all sections give exactly the original nabVal formula. This removes the separate IsNab input from the ICL lattice-spanning route; principal-chart existence, finite theta systems and the other named spanning producers remain distinct.',
 'PCL constructs the exact original Hermitian-coordinate and trace-dual cusp-lattice data, and the quantitative DataX normalization on each supplied principal chart. Its explicit fractional-ideal and different calculation preserves the original fields, lattice, metric, scalar and denominator conventions. The prescribed half-different and quadratic ideal norm give the host identity and exact NA/NC and logarithmic bounds. IsUnf, HasPrinc/GamAt, LawsCore and actual common uniformization remain original antecedents; this is not a new claim of their existence.',
 'LGS supplies the actual local-growth, canonical mean-deficit and full admission inputs for the original local-gain route. It proves the required small-order and band bounds, local lattice projection/walk estimates and normalized lengths, then changes only the auxiliary Ch field to zero and verifies every field of that admitted record. The original valuation lattices, comparison maps, degree data, supports and family are unchanged. All five LinkG conclusions follow with exactly C_G=4C_count+1 and b_o=b^(x^(-epsilon/2)). The pointwise LinkG theorem retains actual GroupCompatibilityFamily and Adm2F on the same family; actual TopsF supplies Adm2F. The exact class-level linkG_concrete5 retains the two corresponding Closed predicates, with their cutoffs and coefficient bounds chosen before the family, in addition to the original ambient family bounds.'
]
remaining=[
 'Construct one original common geometric family and the higher CoversAt/all-tuple class sums and uniqueness with original phase rescalings, one PointIdentCore with common lambda,z, and base ClassSumsSpan. CNC now supplies the full original IsNab; PCL supplies the conditional trace-dual principal-lattice and quantitative normalization. Actual uniformization/HasPrinc and the five principal-chart, finite-level-system, Gaussian/reproduction, short-rule/simultaneous-dictionary and ramified-jet producer groups remain. Keep all original both-level, coefficient-field, Fits and eta agreements.',
 'Complete the remaining original F3 local coefficient bridges and F4 full common-overfield reading, with exact valuation/norm/GoodCoef/iq data and the entire coefficient field. Supply actual complex Hecke standard/no-Jordan and arithmetic character data on the same form datum; completed ordinary Hecke and Hida support remain available.',
 'Complete actual base rows, host/frame lengths, nonzero chains and group ties, MultEq support, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. Keep the stronger second DivRows3 scope separate from the completed first DivDef3 and row-pair integrability.',
 'Finish the same-D/common-family adelic setting after ASG: normalized nonzero Bessel W and decay, measured-field block, original Siegel-Weil rescaling and measure/character ties, Bessel uniqueness/local ties, then the original AutTie/RowDictTie/LabTie. RowsFinDim is now proved universally by RFD. Supply the actual CountIdempotentsClass theorem or its three sufficient arithmetic cylinder counts, with one simultaneous family threshold; reuse the completed ARO structure.',
 'Construct the original common GroupCompatibilityFamily and selected tops/Adm2F for global local gain. LGS now supplies full auxiliary admission, actual first-growth and mean inputs; these should not be reopened. Continue the distinct denominator, period/height, normalized spectral and second-layer compatible-selection producers with the original common objects and thresholds.',
 'Complete the actual AutomorphyUnramifiedCoefficients package and original OneChar trace/length producer using the now supplied InpZ, CNR3 and finite PGK consumer. RigII and InpZ assembly are complete at their exact source scopes. Continue RH Cases I/V and the independent additional Dirichlet-GRH CaseIII/promodularity, SeedIV, tensor-factor and rank-four-chain tasks.'
]
progress={
 'RIG_II':dict(completed=['KTR1-KTR13'],remaining='None within the literal RigII contract; the original universal extension-modularity antecedent and named classical foundations remain part of its stated scope.'),
 'TASK_INP_Z_ASSEMBLY':dict(completed=[c['id'] for c in ledgers['kato_input_assembly_v47']['claims']],remaining='None within the exact same-object input-record assembly; independent OneChar and unramified-coefficient automorphy remain separate.'),
 'TASK_ONE_CHAR_PROOF':dict(completed=['KTR1-KTR13','KIZ input record','RNC16','PGK1-PGK6'],remaining='The actual original OneChar trace/length estimate and the common marked unramified-coefficient automorphy datum. The complete InpZ record and finite PropGK consumer are now available.'),
 'GLOBAL_RETAINED_DEFECT':dict(completed=['ARO1-ARO30','RFD1-RFD9','ASG1-ASG18'],remaining=remaining[3]),
 'GLOBAL_LOCAL_GAIN':dict(completed=['GLG1-GLG18','LGS1-LGS13'],remaining=remaining[4]),
 'DESIGN_CHOICES_COMMON':dict(completed=['ICL1-ICL21','CNC1-CNC16','PCL1-PCL12'],remaining=remaining[0]),
 'BASE_THETA_RATIONAL_TESTS':dict(completed=['ICL1-ICL21','CNC1-CNC16','PCL1-PCL12'],remaining=remaining[0])
}
updated={}
for key in ['DESIGN_CHOICES_COMMON','BASE_THETA_RATIONAL_TESTS','GLOBAL_RETAINED_DEFECT','GLOBAL_LOCAL_GAIN','TASK_ONE_CHAR_PROOF']:
 updated[key]=nodes[key]['contract']+' CURRENT VERSION0.47 QUALIFICATION: '+progress[key]['remaining']+' Completed new original producers: '+', '.join(progress[key]['completed'])+'. Any earlier narrative naming these completed producers as outstanding is historical; this qualification is the current scope authority.'
open_before=read('dependency_audit_v0_46/remaining_leaf_register.json')['records']
open_after=[n for n in open_before if n['id'] not in closed]
cats=collections.Counter(n['category'] for n in open_after)
def reach(key):
 seen=set()
 def go(k):
  if k in seen:return
  seen.add(k)
  for dep in nodes[k]['requires']:go(dep)
 go(key);return seen
oi={n['id'] for n in open_after};rh=reach('ORDINARY_RH');grh=reach('DIRICHLET_GRH')
status=(f'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge-Claude formal source as fully checked and correct. Version0.47 completes the full original RigII and exact InpZ assembly, closing those two selected contracts. It also supplies universal RowsFinDim, the complete canonical cusp connection, eight original adelic setting blocks, conditional principal cusp-lattice normalization, and actual local-growth/mean/admission producers. {len(oi)} whole selected obligations remain: {cats["C"]} C and {cats["B"]} B; {len(oi&rh&grh)} shared RH/GRH and {len((oi&grh)-rh)} additional GRH. The remaining common geometry/compatibility, original OneChar/automorphy and quantitative/case producers remain explicit. No Lean build or kernel replay is claimed.')
published=[]
for component,ledger in ledgers.items():
 for c in ledger['claims']:
  if c['classification']=='A':published.append(dict(id=c['id'],classification='A',component=component,registry=component+'/classical_inputs.json',scope=c.get('scope_note',c.get('title')),review='Hash-bound independent component reviews'))
cfg=dict(artifact_version='0.47',date='2026-11-23',source_commit=old['source_commit'],title='Type-II rigidity, cusp connections, and actual setting inputs',components=components,component_authors=authors,closed_selected_leaves=closed,closure_reviews=closure_reviews,
 closed_nested_producers=['Full original KatoUse and KatoTwo','Full original nine-dimensional RigII','Exact entire CohInp/InpZ assembly','Universal literal RowsFinDim','Full generic canonical gauge and original IsNab','Original UnitaryGroupInstance and latExists_of_forms0 with all FixedHyp fields','Full generic ScPsiExists, ScRefExists and ScXuExists','Original eOf admissibility, complete AutomorphicBundle, RepresentationData and MuBlocks','Exact conditional Hermitian/trace-dual principal cusp lattice and DataX quantitative normalization','Actual local first-growth, canonical MeanKappaBound and full zero-Ch admissible family','Complete original LinkG and linkG_concrete5 with common compatibility/selected-top antecedents'],
 status=status,local_conclusions=conclusions,remaining_major_inputs=remaining,next_targets=remaining,selected_node_progress=progress,updated_contracts=updated,published_applications=published,publication_note='New class-A applications are separately counted from the human proofs: exact Kato critical vanishing, quadratic GL2 base change, Harish-Chandra finite multiplicity, and Hilbert class field/Chebotarev ideal selection. Previously matched classical and period foundations remain explicit; no foundational theorem is silently treated as a newly proved input.')
(ROOT/'increment_v0_47.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,closed_selected_leaves=list(closed),open_count=len(oi),open_categories=dict(cats),new_claims=sum(len(x['claims']) for x in ledgers.values()),published_applications=[x['id'] for x in published]),indent=2))
