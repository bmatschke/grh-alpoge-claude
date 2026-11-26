#!/usr/bin/env python3
"""Configure v0.48 after the exact OneChar implication review is bound."""
from pathlib import Path
import collections
import hashlib
import json

ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads((ROOT/p).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
old=read('increment_v0_47.json')
graph=read('dependency_audit_v0_47/obligation_map.json')
nodes={n['id']:n for n in graph['nodes']}
components=['one_character_v48','adelic_measures_v48','principal_uniformization_v48','common_compatibility_v48']
authors=dict(zip(components,['main_proof_rigidity','root','ordinary_structure','global_estimates']))
ledgers={c:read(c+'/provenance.json') for c in components}
closure_components={'TASK_ONE_CHAR_PROOF':'one_character_v48'}
closure_reviews={}
for key,component in closure_components.items():
 for p in sorted((ROOT/component).glob('review_*_root.json')):
  r=json.loads(p.read_text());exact=r.get('selected_whole_contract_reviewed',{})
  if exact.get('id')!=key:continue
  assert r['result']=='PASS' and r['proof_sha256']==sha((ROOT/r['proof_file']).read_bytes())
  assert exact['full_original_contract_closed_in_stated_scope']
  assert exact['baseline_contract_sha256']==sha(nodes[key]['contract'].encode())
  closure_reviews[key]=str(p.relative_to(ROOT))
 assert key in closure_reviews,('missing exact whole-contract review',key)

closed={'TASK_ONE_CHAR_PROOF':dict(category='B',claims=[c['id'] for c in ledgers['one_character_v48']['claims']],
 conclusion='The full original implication InpZ -> AutomorphyUnramifiedCoefficients -> OneChar, on every supplied original coefficient datum and GD input, with finite Vlen and the exact finite trace/length estimate.',
 method='Actual crystalline ordinary component and twelve-variable local chart, exact normalized graded global model, finite quotient and derivation lifting, Selmer-to-cotangent injection, the original finite isomorphism-irredundant trace sum, and descent to unramified coefficients followed by transport back.',
 boundary='The literal AutomorphyUnramifiedCoefficients premise is retained and remains an open selected producer. A single marked g1 must provide FinA, AutB and LemW for the same actual datum and fixed iota. No automorphy or final RH/GRH producer is inferred from this implication.')}

conclusions=[
 'OCH proves the entire original implication InpZ -> AutomorphyUnramifiedCoefficients -> OneChar. It constructs the actual ordinary crystalline component over every finite Artin coefficient algebra, including nonreduced targets, and its twelve-variable chart with weight multiplicities (1,2,3,4,2). The same marked deformation datum gives the exact integral graded model. Strict-local boundedness and finite Taylor division justify points and arbitrary derivations; the Selmer-to-cotangent injection, finite algebra upper bound and original isomorphism-irredundant trace sum give finite Vlen and Vn <= 2 times the sum of the original trace-difference valuations. The same fixed iota, Adm3 at N or Adm2 at N*abs(discr K), and RepIso-irredundant finite set are retained. Unramified-coefficient descent restores arbitrary original coefficient ramification. The shared marked automorphy package remains a separate premise and open producer.',
 'AMD supplies the complete original adelic bridge and all measured-data constructors, including MExists, on the same actual frame, groups and word data. Closed subgroup and semidirect-product analysis proves the exact Haar product identities. The source weak Haar-on-set condition is promoted to the required Haar measure by a Tonelli comparison, without silently imposing extra Radon hypotheses. The constructor permits prescribed infinity measures, global N/H measures and every local S measure. A compact fundamental-domain construction for the rational unipotent group gives covolume one while retaining the prescribed infinity, H and local S data. The Bessel vector, orbital/fiber measure ties, Siegel-Weil identities and full common-family arithmetic count remain distinct.',
 'PUN supplies fixed-space arithmetic lattice models, the entire ModelsOf/ModelBase/NegXi constructor on a supplied FamilyUnif, the actual center lattice in every rank and component family, and the exact A=1 ExpoMatch. The proofs retain nonprincipal projective lattices, the original different and half-trace factors, and the original principal group. Explicit periods and a canonical primitive Appell-Humbert line produce each original moduli point, including every positive torsion level, the negative Weil sign, both markings, every C-to-k scalar extension and KTriv on all C-algebras, including nonreduced algebras. The actual point equality criterion and marked genus nonemptiness are also proved. Global finite holomorphic FamilyUnif/N1c, theta normalization and the remaining spanning producers remain separate.',
 'GCF reconstructs the actual finer determinant quotient KDq, its congruence, unit-image and rational maps, and the relative determinant law on the same given frames. It extends prescribed columns without changing their compatible group, supplies the actual normalized CM period over the existing coefficient field, and proves all GroupCompatibilityAll fields on one canonical tuple. One original GJStage is chosen before every later W,V,S,N, yielding the full true-volume GIs2 stage. Division transports the original comparison map and joint compatibility tuple exactly. For the selected D3 class, ChosenE already supplies ChosenTT and ChosenBad, hence the required TopsF and Adm2F with a common threshold. The remaining local-gain producer is the actual common WPt/TSel realization, including the given comparison and kernel data; no whole global-gain closure is claimed.'
]

remaining=[
 'Construct the original finite holomorphic FamilyUnif/N1c, normalized theta families and local lifting, then the common principal charts and finite-level theta systems. PUN now supplies the exact fixed-space models, all-family center lattices, A=1 exponent matching and individual primitive points with the full point-equality criterion; CNC supplies the full canonical connection and PCL the quantitative trace-dual normalization. Complete higher CoversAt and all-tuple class sums/uniqueness with the original phase rescalings, one PointIdentCore with common lambda,z, and base ClassSumsSpan. The Gaussian/reproduction, short-rule/simultaneous-dictionary and ramified-jet producers, and all original both-level, coefficient-field, Fits and eta agreements remain explicit.',
 'Complete the remaining original F3 local coefficient bridges and F4 full common-overfield reading, with exact valuation/norm/GoodCoef/iq data and the entire coefficient field. Supply actual complex Hecke standard/no-Jordan and arithmetic character data on the same form datum; completed ordinary Hecke and Hida support remain available.',
 'Complete actual base rows, host/frame lengths, nonzero chains and group ties, MultEq support, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. Keep the stronger second DivRows3 scope separate from the completed first DivDef3 and row-pair integrability.',
 'Finish the same-D/common-family adelic setting after ASG and AMD: normalized nonzero Bessel W and decay, original orbital/fiber and Siegel-Weil measure/character ties, Bessel uniqueness/local ties, and the full original transport theorem, then AutTie/RowDictTie/LabTie. The complete MExists measured-data block and unipotent covolume normalization are now supplied, and universal RowsFinDim remains available. Supply the actual CountIdempotentsClass theorem or its three sufficient arithmetic cylinder counts with one simultaneous family threshold.',
 'Construct the actual eventual common WPt/TSel realization and its GroupCompatibilityFamily on the given Extra comparison and kernel data. GCF supplies the full single GIs2 stage, period normalization, relative determinant and division transport; selected D3 tops and Adm2F already follow from ChosenE. LGS supplies local first-growth, mean and full auxiliary admission. Continue the separate global denominator, period/height, normalized spectral and second-layer compatible-selection producers with the original common objects and thresholds.',
 'Construct the actual AutomorphyUnramifiedCoefficients package: for every original Dat with coefficient ramification one and fixed iota, choose one marked g1 that supplies FinA, AutB and LemW together. The original InpZ record, full RigII, CNR3, finite PropGK consumer and now the entire OneChar implication are supplied. Continue RH Cases I/V and the independent additional Dirichlet-GRH CaseIII/promodularity, SeedIV, tensor-factor and rank-four-chain tasks.'
]

progress={
 'TASK_ONE_CHAR_PROOF':dict(completed=['OCH1-OCH30','KIZ original InpZ'],remaining='None within the full original implication InpZ -> AutomorphyUnramifiedCoefficients -> OneChar. The original unramified-coefficient automorphy premise remains separately open as AUT_UNRAM_COEF.'),
 'AUT_UNRAM_COEF':dict(completed=['OCH1-OCH30 (the full consumer implication)','KIZ original InpZ','KTR1-KTR13','RNC16','PGK1-PGK6'],remaining=remaining[5]),
 'GLOBAL_RETAINED_DEFECT':dict(completed=['ARO1-ARO30','RFD1-RFD9','ASG1-ASG18','AMD1-AMD17'],remaining=remaining[3]),
 'GLOBAL_SPECTRAL':dict(completed=['ASG1-ASG18','AMD1-AMD17','GCF1-GCF18 at their stated scopes'],remaining='Complete the original same-family spectral/Bessel and Siegel-Weil inputs with all measure, character, transport and common-object ties. The complete MExists measured block and prescribed-measure covolume normalization are supplied; these are not the full normalized spectral theorem.'),
 'GLOBAL_LOCAL_GAIN':dict(completed=['GLG1-GLG18','LGS1-LGS13','GCF1-GCF18'],remaining=remaining[4]),
 'DESIGN_CHOICES_COMMON':dict(completed=['ICL1-ICL21','CNC1-CNC16','PCL1-PCL12','PUN1-PUN24','GCF1-GCF18 at their stated scopes'],remaining=remaining[0]),
 'BASE_THETA_RATIONAL_TESTS':dict(completed=['ICL1-ICL21','CNC1-CNC16','PCL1-PCL12','PUN1-PUN24'],remaining=remaining[0])
}
updated={key:nodes[key]['contract']+' CURRENT VERSION0.48 QUALIFICATION: '+p['remaining']+' Completed current producers or conditional consumers: '+', '.join(p['completed'])+'. Earlier frontier descriptions are historical; this qualification is the current scope authority. Original whole-contract premises and quantifiers are retained.' for key,p in progress.items() if key not in closed}

open_before=read('dependency_audit_v0_47/remaining_leaf_register.json')['records']
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
status=(f'Partial human reconstruction of RH and unrestricted Dirichlet GRH, accepting the pinned Alpoge-Claude formal source as fully checked and correct for reconstruction. Version0.48 completes the original OneChar implication from InpZ and AutomorphyUnramifiedCoefficients, closing TASK_ONE_CHAR_PROOF while retaining the latter premise as an independent open producer. It also supplies the full measured-data constructor and prescribed-measure unipotent normalization, fixed-space principal models and individual primitive moduli points, and a single common true-volume group stage with exact transport and selected D3 admission. {len(oi)} whole selected obligations remain: {cats["C"]} C and {cats["B"]} B; {len(oi&rh&grh)} shared RH/GRH and {len((oi&grh)-rh)} additional GRH. Common holomorphic/geometric realization, original automorphy, quantitative and remaining case producers remain explicit. No Lean build or kernel replay is claimed.')
published=[]
for component,ledger in ledgers.items():
 for c in ledger['claims']:
  if c['classification']=='A':published.append(dict(id=c['id'],classification='A',component=component,registry=component+'/classical_inputs.json',scope=c.get('scope_note',c.get('title')),review='Hash-bound independent component reviews'))
cfg=dict(artifact_version='0.48',date='2026-11-23',source_commit=old['source_commit'],title='One-character estimates, exact measures, and common compatibility',components=components,component_authors=authors,closed_selected_leaves=closed,closure_reviews=closure_reviews,
 closed_nested_producers=['Full original InpZ -> AutomorphyUnramifiedCoefficients -> OneChar implication','Actual ordinary crystalline component and normalized graded model with all point/derivation/lifting fields','Full original AdelicIsomorphism, MGExists, MWCore and MExists measured constructors','Full prescribed-measure MeasW constructor and rational-unipotent covolume-one normalization','Original fixed-space model_in_same_space and complete LatModel','ModelsOf/ModelBase/NegXi for a supplied original FamilyUnif','Full all-family LatZ and original A=1 ExpoMatch','Actual primitive period points with KTriv on all coefficient algebras, negative Weil sign and exact markings','Full point_eq_iff_isometry_closed and marked InGenus nonemptiness','Actual KDq relative determinant law and full prescribed-column extension','Original OmegaCompatible period normalization in the existing coefficient field','Full exists_trueVolume_stage_of_any_column_choice / GIs2 on one prior stage','Exact comparison-map and IsRecG division transport','Selected D3 TopsF and Adm2F from the original ChosenE premise'],
 status=status,local_conclusions=conclusions,remaining_major_inputs=remaining,next_targets=remaining,selected_node_progress=progress,updated_contracts=updated,published_applications=published,publication_note='All 89 new numbered claims are class-B written deductions. Named classical foundations, including Hasse-Minkowski, Appell-Humbert, algebraization/GAGA and the universal dual Picard property, are separately recorded with their exact applications. They are not synthetic new claim-DAG nodes or assertions of newly proved foundational theorems. Inherited matched cohomological, period and automorphic inputs remain explicit.')
(ROOT/'increment_v0_48.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(components=components,closed_selected_leaves=list(closed),open_count=len(oi),open_categories=dict(cats),new_claims=sum(len(x['claims']) for x in ledgers.values()),published_applications=[x['id'] for x in published]),indent=2))
