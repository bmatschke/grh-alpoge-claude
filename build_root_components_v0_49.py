#!/usr/bin/env python3
"""Bind the written wave-packet proofs to their literal pinned contracts.

This records source and proof identity. It performs no Lean/kernel replay.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'formal_source'
PIN='7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
assert subprocess.check_output(['git','-C',str(SRC),'rev-parse','HEAD'],text=True).strip()==PIN
sha=lambda b:hashlib.sha256(b).hexdigest()
S='src/Formalism/LocalToGlobal/SiegelLatticeTheory/'
H=S+'HaarTransversals/'
U=H+'UnitaryHaarProducts/'
L=U+'LocalWeightCharts/'
P='src/Formalism/PeriodIntegrals/'
C='src/Formalism/SharpRestriction/CuspSpanNormBounds/'
DS='src/ReciprocityTheory/ReductiveGroups/DiscreteSeries/'
name='bessel_wave_packets_v49'
here=ROOT/name
groupspec={
 'groups': [('src/Formalism/FormalDegreeBessel/StatementG.lean',7,50,'Literal Hpk, flags, Nset, UWset and Sset'),(H+'HidaSetting.lean',24,65,'Original frame flag groups, root coordinates and character')],
 'representations':[(C+'RelevantZeroGramTerms.lean',24,150,'Complete literal IsDS, lowest compact subspace, unitary Cayley witnesses and compact highest type')],
 'numbers':[(C+'CayleySignature.lean',18,54,'Original lam48, eps48, interlacing, half-integrality, GapBig and RealPlaceNumericalSetting'),(DS+'FormalDegree/CoefLocGap.lean',1,None,'Exact opposite-sign and cubic-gap supplier arithmetic')],
 'nilpotent_chart':[(L+'NChartP.lean',1,None,'Original full NChart producer'),(L+'NShear.lean',1,115,'Actual multiplication coordinates and measure-preserving shear'),(L+'NilpotentChartNormBound.lean',1,None,'Quadratic inverse-chart norm bound'),(L+'OpnContinuous.lean',11,None,'Original NChart/NCoordHaar and NIntDecay contracts')],
 'reproducer':[(U+'SettingBlocks.lean',389,399,'Original HCReprodDS with arbitrary identity neighborhood'),(U+'HCReprodM.lean',1,None,'Original measurable compact reproduction predicate')],
 'weighted_coefficient':[(U+'SettingBlocks.lean',323,334,'Whole CoefWeightedLoc and the exact exponent')],
 'local_measure_kernel':[(C+'RelevantZeroGramTerms.lean',208,228,'Original IsQuotMeas, IsSPsiEquiv and squared l2SG'),(C+'RelevantZeroGramTerms.lean',419,430,'Exact fdegH and eFun normalization')],
 'wave_packet':[(L+'WavePacketL1L2.lean',1,220,'Original B0/Af, measure hypotheses and analytic supplier predicates'),(L+'WavePacketL1L2OfNilpotentChart.lean',1,None,'Original wave-packet assembly and normalization')],
 'convolution':[(L+'AKindR.lean',20,176,'Full Bochner-Fubini transfer and every-base-point convolution')],
 'nonvanishing':[(U+'SettingBlocks.lean',406,423,'Entire original BesselNVGap, retained as a premise')],
 'local_endpoint':[(U+'SettingBlocks.lean',425,452,'Exact nuH, N1H and all seven original WlocExists conclusions'),(L+'ScWlocExists.lean',1,None,'Original final local producer')],
 'global_records':[(U+'SettingBlocks.lean',149,215,'Given representation, measure and WBlk records'),(U+'SettingBlocks.lean',354,380,'Exact WExists choice order and setting assembler'),(H+'HidaSetting.lean',145,160,'Original quotient measure and IsWu'),(H+'WuDecay.lean',1,None,'Literal WuReprod, WuWeighted, nuInf and N1')],
 'frame_transport':[(U+'BesselFrame.lean',380,417,'Exact root-coordinate identity and 4pi/g character factor'),(U+'BesselFrame.lean',650,727,'Different group, subgroup and base-point measure maps'),(U+'BesselFrame.lean',814,None,'Original locPack and separate two-sided base-point transport'),(U+'WFLUnit.lean',291,337,'Actual dimension, parameter and interlacing identifications')],
 'quotient_product':[(U+'QuotRaw.lean',1,None,'Original arbitrary-measure product quotient supplier')],
 'global_assembly':[(U+'WFromLoc.lean',37,151,'Original local measures and one-place global normalization'),(U+'WFromLoc.lean',151,282,'Original tensor assembly and all WBlk fields'),(S+'FlagStabilizerTensors/RootLatticeThresholds/WuDecayAll.lean',410,527,'Original quotient-product and tensor-decay implications')],
 'global_gap':[(H+'ConcreteSettingExists.lean',13,20,'Exact GapHyp and ConcreteSettingExists'),(S+'FlagStabilizerTensors/RootLatticeThresholds/WuDecayAll.lean',44,72,'Original local cubic gap from the global nineteenth-power gap')],
 'global_endpoint':[(U+'SettingBlocks.lean',453,469,'Full GapBigOfGapHyp, WFromLoc and settingExists_of_inputs'),(S+'ClosedVolumeStatements/SettingExistsOfGap.lean',24,40,'Original same-block setting installation')]
}
claim_groups={
 1:['groups','nilpotent_chart'],2:['groups','nilpotent_chart'],3:['groups','representations'],4:['representations','reproducer'],
 5:['numbers'],6:['weighted_coefficient','numbers','representations'],7:['representations','local_measure_kernel','weighted_coefficient'],
 8:['local_measure_kernel','local_endpoint'],9:['groups','local_measure_kernel'],10:['wave_packet','nilpotent_chart'],
 11:['wave_packet','local_measure_kernel'],12:['wave_packet','local_endpoint'],13:['wave_packet','local_measure_kernel'],
 14:['nonvanishing','wave_packet'],15:['convolution','wave_packet'],16:['convolution','local_measure_kernel'],17:['reproducer','convolution'],
 18:['local_endpoint','nonvanishing'],19:['quotient_product','global_records'],20:['frame_transport','numbers','global_records'],
 21:['global_assembly','global_records'],22:['global_assembly','global_records'],23:['global_gap'],24:['global_endpoint','global_records','global_gap']
}
deps={
 1:[],2:['BWP1','AMD8'],3:['BWP1','AMD4','AMD5','AMD6'],4:[],5:[],
 6:['BWP5','DC6','DC13'],7:['AMD8','BWP4','BWP6','DC12','DC13'],8:['AMD8','BWP2'],
 9:['BWP3','AMD7','AMD8'],10:['BWP2','BWP3','BWP4','BWP7'],11:['BWP3','BWP9','BWP10'],
 12:['BWP8','BWP9','BWP10'],13:['BWP10','BWP11','BWP12'],14:['BWP9','BWP10','BWP13'],
 15:['BWP10'],16:['BWP7','BWP15'],17:['BWP4','BWP7','BWP15'],
 18:['BWP6','BWP10','BWP11','BWP12','BWP13','BWP14','BWP16','BWP17'],
 19:['ASG17'],20:['BWP3','BWP7','BWP18','ASG17'],21:['BWP12','BWP18','BWP19','BWP20','AMD7','AMD8'],
 22:['BWP5','BWP12','BWP18','BWP19','BWP20','BWP21'],23:[],
 24:['BWP6','BWP7','BWP18','BWP20','BWP21','BWP22','BWP23','ASG1','ASG2','ASG3','ASG4','ASG5','ASG6','ASG7','ASG8','ASG9','ASG10','ASG11','ASG12','ASG13','ASG14','ASG15','ASG16','ASG17','AMD12']
}
scopes=[
 'Explicit polynomial global chart on the literal Nset, with inverse and real dimension 2r^2+2rk+r, including r=0.',
 'Jacobian-one Haar construction, quadratic inverse-coordinate norm bound, and full NIntDecay at the exact exponent for every original weak Haar measure.',
 'Actual closed compact-by-unipotent S, unique factorization, unimodularity, exact psiGen character and supplied compact representation.',
 'Full original HCReprodDS with support in every prescribed neighborhood; finite-isotypic Cayley-Hamilton construction, with inherited Harish-Chandra admissibility explicitly retained.',
 'All opposite-sign gaps and precise analytic inequalities from every original GapBig witness, including arbitrary permitted k,r.',
 'Entire literal CoefWeightedLoc for every given IsDS and lowest unit vector; uses DC13 model identification and DC6 polar decay, not a model-only estimate.',
 'Exact original unitary Cayley witnesses, weak Haar normalization, formal degree and eFun reproduction on every supplied local representation.',
 'Support and measurable invariant source nuH on the originally supplied ambient quotient measure, with no added section or Radon hypothesis.',
 'Exact finite-positive product scalar for arbitrary Bessel subgroup Haar measures and the given quotient identity.',
 'Absolute convergence, continuity and polynomial ABound on every group element from compact reproduction, coefficient L1 and reciprocal-norm integration.',
 'Full IsSPsiEquiv for the actual psi and supplied pi, with all h,m,x quantified.',
 'Both ordinary and exact N1H-weighted quotient L1, for the supplied nu.',
 'Finite literal squared l2SG from height domination and weighted L1.',
 'Positive squared l2SG and nonzero packet from the complete original BesselNVGap antecedent; that endomorphism nonvanishing remains unproved.',
 'Every-base-point Bochner convolution transfer with full absolute integrability justified before Fubini.',
 'Full original eFun/rconv integrability and reproduction at the given formal-degree normalization.',
 'Original bounded measurable compact reproducer, supported in G in a compact set containing one, at every base point.',
 'Entire original WlocExists with every original antecedent, arbitrary original measures, all seven conclusions and squared L2 equal to one.',
 'Original product quotient formula for invariant functions, preserving an arbitrary given ambient quotient measure with its single finite positive scalar.',
 'Exact original locPack on every supplied frame, Hilbert space, lowest vector and compact representation; separate group/subgroup/two-sided base-point maps, exact 4pi/g character, and given measure identities.',
 'Full WBlk on the given tensor data and MuBlocks; one-place C^(-1/2) normalization, all IsWu fields, chosen before MBlk.',
 'Full WuDecay for the constructed WBlk and every later MBlk, with original N1 exponent, quotient height and compact reproducer; no arbitrary-model uniqueness claim.',
 'Entire GapBigOfGapHyp with every original dimension identification and real place, using witness t=n+6.',
 'Whole original WFromLoc; BesselNVGap implies WExists. On the inherited supplied Forms0 scope, the completed blocks give ConcreteSettingExists, retaining the nonvanishing premise and all original choice order.'
]
foundations=[
 {'id':'BWP_HAAR_ANALYSIS','kind':'standard_mathematical_background','statement':'Haar existence and finite-positive-scalar uniqueness, quotient Haar theorem with Borel sections/cutoffs on lcsc closed unimodular quotients, Tonelli and Bochner Fubini, dominated convergence, and elementary radial integration. The weak-measure promotion is the inherited numbered proof AMD8; product normalization and every exchange used here are proved explicitly.'},
 {'id':'BWP_HC_ADMISSIBILITY','kind':'inherited_named_classical_foundation','statement':'Harish-Chandra admissibility: an irreducible unitary representation of a real reductive group has finite-dimensional maximal-compact isotypic spaces. This is the same separately named foundation as in RFD1. It supplies finite dimension in BWP4; the compact reproducer is then proved by an approximate identity and Cayley-Hamilton. No universal Bessel or lowest-type theorem is imported.','primary_source':'https://homepages.math.uic.edu/~rtakloo/papers/borel/borel3.pdf','source_location':'Armand Borel, Automorphic forms on reductive groups, printed Section10 paragraph labelled8.5, printed page27; general finite-component extension on page28.','verified_this_increment':True},
 {'id':'BWP_LINEAR_BACKGROUND','kind':'standard_mathematical_background','statement':'Finite-dimensional matrix and compact-group representation theory, Cayley-Hamilton, continuous approximate identities, and tensor products of finite-dimensional Hilbert spaces.'},
 {'id':'BWP_ORIGINAL_INPUTS','kind':'original_contract_inputs','statement':'The original ranks, parameters, numerical setting, IsDS/IsDSHpk and lowest vectors, given compact representations, original weak Haar measures and quotient identities, and given setting blocks wherever their original contracts quantify them. The final setting corollary preserves the supplied Forms0(D,D.u0) scope of ASG.'},
 {'id':'BWP_BESSEL_NV_GAP','kind':'retained_original_consumer_premise','statement':'The entire source BesselNVGap at SettingBlocks.lean406–423: all original k,r,z,c,u,v,b, interlacing, half-integrality and cubic gap assumptions, every original IsDSHpk/IsHCTypeW and lowest unit vector, every weak Haar pair, and some x,x0 with the literal endomorphism-valued Bessel integral nonzero. Used explicitly in BWP14 and downstream; this chapter does not prove it.'}
]
completed=[
 'Whole original NIntDecay and an explicit alternative global nilpotent chart with quadratic inverse norm bound',
 'Whole original HCReprodDS and its compact measurable consequences, with the named inherited admissibility foundation',
 'Whole original CoefWeightedLoc, for arbitrary supplied representations and exact exponent',
 'Whole original WlocExists, with its original BesselNVGap and coefficient antecedents and all seven conclusions',
 'Exact original local frame transport locPack, keeping different subgroup and convolution coordinates and the 4pi/g character',
 'Whole original GapBigOfGapHyp and WFromLoc; BesselNVGap implies WExists on every original supplied block sequence',
 'Constructed global WBlk has WuDecay for every later MBlk without an extra Bessel uniqueness premise',
 'Conditional ConcreteSettingExists on the inherited supplied Forms0 scope, with one same-data bridge and exact measures'
]
not_claimed=[
 'The original BesselNVGap nonzero endomorphism integral itself',
 'Bessel multiplicity one, local uniqueness, or decay for every arbitrary IsWu vector',
 'Removal of the supplied Forms0 input used in the inherited lattice constructor',
 'Original orbital/fiber and Siegel-Weil measure/character comparisons, full normalized spectral statement or any whole global selected leaf',
 'Complete human RH or unrestricted Dirichlet-GRH proof'
]

baseline=json.loads((ROOT/'history/version_0_48/provenance.json').read_text())
known={c['id']:c for c in baseline['claims']}
assert not any('BWP'+str(i) in known for i in range(1,25))
raw=(here/'main.tex').read_bytes();txt=raw.decode()
groups={};inventory={};excerpts=[]
for group,specs in groupspec.items():
 records=[]
 for j,(path,start,end,desc) in enumerate(specs,1):
  data=(SRC/path).read_bytes()
  assert data==subprocess.check_output(['git','-C',str(SRC),'show',PIN+':'+path])
  lines=data.splitlines(keepends=True);end=end or len(lines)
  assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
  part=b''.join(lines[start-1:end])
  rec=dict(id=f'BWP_{group}_{j:02}',path=path,line_start=start,line_end=end,declaration=desc,file_sha256=sha(data),range_sha256=sha(part),range_bytes=len(part),source_commit=PIN,verified_equal_to_pinned_git_blob=True,url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
  records.append(rec);inventory[path]=dict(path=path,sha256=sha(data),bytes=len(data),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
  excerpts.append(f'[{rec["id"]}] {path}:{start}-{end}\nRange SHA256 {sha(part)}\n{part.decode()}\n')
 groups[group]=records
claims=[]
for n in range(1,25):
 cid='BWP'+str(n)
 match=re.search(r'% BEGIN '+cid+r'\n.*?% END '+cid+r'\n',txt,re.S);assert match,cid
 title=re.search(r'\\paragraph\{'+cid+r'\. (.*?)\}\n',match.group(),re.S).group(1)
 block=match.group().encode()
 ext=['BWP_HAAR_ANALYSIS','BWP_LINEAR_BACKGROUND','BWP_ORIGINAL_INPUTS']
 if n==4:ext.append('BWP_HC_ADMISSIBILITY')
 if n in [14,18,20,21,22,24]:ext.append('BWP_BESSEL_NV_GAP')
 claims.append(dict(id=cid,title=title,introduced_in='0.49',classification='B',status='complete human proof at the explicitly stated original scope',depends_on=deps[n],external_input_ids=ext,published_input_ids=[],scope_note=scopes[n-1],source_groups=claim_groups[n],sources=[s for g in claim_groups[n] for s in groups[g]],proof_location=dict(file=name+'/main.tex',label='claim:'+cid,line_start=txt[:match.start()].count('\n')+1,line_end=txt[:match.end()].count('\n'),sha256=sha(block),bytes=len(block)),source_proof_is_not_human_proof=True))
inherited=[]
for cid in sorted({d for c in claims for d in c['depends_on'] if not d.startswith('BWP')}):
 c=known[cid];loc=c['proof_location'];data=(ROOT/loc['file']).read_bytes();part=b''.join(data.splitlines(keepends=True)[loc['line_start']-1:loc['line_end']]);h=loc.get('sha256',loc.get('paragraph_sha256'))
 assert h in {sha(part),sha(part.rstrip(b'\r\n'))},(cid,'inherited proof hash')
 inherited.append(dict(id=cid,file=loc['file'],main_tex_sha256=sha(data),block_sha256=sha(part),recorded_baseline_hash=h,line_start=loc['line_start'],line_end=loc['line_end'],kind='numbered_human_proof_dependency',not_an_external_foundation=True,introduced_in=c.get('introduced_in')))
reviews=[dict(file=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())) for p in sorted(here.glob('review_*.json'))]
prov=dict(schema='rh-human-component-provenance/1',artifact_version='0.49',date='2026-11-23',component=name,source_commit=PIN,main_tex_sha256=sha(raw),proof_file_sha256=sha(raw),claims=claims,source_groups=groups,source_inventory=list(inventory.values()),source_files=list(inventory),retained_foundations=foundations,inherited_human_inputs=inherited,independent_reviews=reviews,builder=dict(file='../build_root_components_v0_49.py',sha256=sha(Path(__file__).read_bytes())),validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,claim_blocks=24,external_foundations_separate_from_claim_DAG=True,inherited_human_proof_hashes_checked=True,no_lean_replay=True))
contracts=dict(schema='rh-root-producer-contracts/1',artifact_version='0.49',component=name,source_commit=PIN,proof_file_sha256=sha(raw),endpoint_claim='BWP24',completed_original_substatements=completed,not_claimed=not_claimed,proposed_whole_obligation_closures=[],whole_obligation_closures=[],no_lean_replay=True)
for fn,obj in [('provenance.json',prov),('contracts.json',contracts),('classical_inputs.json',dict(component=name,artifact_version='0.49',foundations=foundations))]:
 (here/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(here/'source_excerpt.txt').write_text('\n'.join(excerpts))
(here/'README.txt').write_text(name+' — version0.49\n\n24 numbered human proofs.\n\nCOMPLETED ORIGINAL SUBSTATEMENTS\n'+'\n'.join('- '+x for x in completed)+'\n\nEXACT BOUNDARY\n'+'\n'.join('- '+x for x in not_claimed)+'\n\nNo Lean build or kernel replay. Source bytes and inherited human proofs are hash-bound.\n')
report=[name+' — mathematical scope and source report','Version0.49; 23 November2026','','The complete human proofs are in main.tex.','','PROVED CLAIMS']
report += [c['id']+' [B]: '+c['scope_note'] for c in claims]
report += ['','RETAINED FOUNDATIONS AND ORIGINAL PREMISES']+[f['id']+' ('+f['kind']+'): '+f['statement'] for f in foundations]
report += ['','COMPLETED ORIGINAL ENDPOINTS']+completed+['','BOUNDARY']+not_claimed
report += ['','PROVENANCE',f'{len(inventory)} pinned source files; {sum(map(len,groups.values()))} exact source ranges; {len(inherited)} inherited human proof bindings.','Source commit: '+PIN,'Proof SHA256: '+sha(raw),'','INDEPENDENT REVIEWS']+[x['file']+' — SHA256 '+x['sha256'] for x in reviews]
report += ['','The bindings record exact inspected text; they do not constitute a formal replay or substitute for the mathematical proofs.']
(here/'report.txt').write_text('\n'.join(report)+'\n')
print(json.dumps(dict(component=name,claims=24,proof_sha256=sha(raw),source_files=len(inventory),source_ranges=sum(map(len,groups.values())),inherited_inputs=len(inherited)),indent=2))
