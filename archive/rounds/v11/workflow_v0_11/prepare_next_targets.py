"""Prepare the exact next-source map for the actual construction frontier."""
from pathlib import Path
B=Path(__file__).resolve().parents[1]
old=(B/'v0_10/build_next_targets.py').read_text()
prefix=old[:old.index('# 1. The actual')]
prefix=prefix.replace('v0.10 continuation','v0.11 continuation').replace('four v0.9 global','four v0.10 global').replace('output/RH_reconstruction_v0_9/','output/RH_reconstruction_v0_10/')
prefix=prefix.replace("declarations.append((m[1],i,ns+'.'+m[1] if ns else m[1]))",
    "qualified=m[1][7:] if m[1].startswith('_root_.') else (ns+'.'+m[1] if ns else m[1])\n            declarations.append((m[1],i,qualified))")
prefix=prefix.replace("if d[0] == name or d[2] == name]",
    "if d[0] == name or d[2] == name or d[2].endswith('.'+name)]")
body=r'''
AB='src/Development/AbelianVarietyTheory/'
AI=AB+'Proofs/GlobalInterpolation/'
AW=AB+'Definitions/GlobalTwisting/'
IW=AB+'Proofs/IwasawaDecomposition/'
TH=AA+'ThickFrames/'

def target(group,path,name,role,remaining,connections=()):
    add(group,path,name,role,remaining,connections)

# Biased probabilities and coset proportions are genuinely additional to GII.
target(1,TH+'topsGroup.lean','topsGroup','Actual simultaneous biased-top selection.',
 'Extend GII9–10 to independent probabilities delta on A0 and 3delta/4 elsewhere, with all coset shares and weighted bad mass at once.',
 ['orbit_terms','select','shares_of_counts'])
target(1,TH+'orbitTerms.lean','orbit_terms','Conditional bad-orbit estimates for nonconstant probabilities.',
 'Retain the forced selected point, actual short-window cap, marked-tile probability and long-window tail with the source probability range.')
target(1,TH+'select.lean','select','Simultaneous finite concentration and weighted bad-count selection.',
 'Prove the common event controls all required coset counts, selected cardinality and weighted bad mass; track threshold dependence on the fixed character order.')
target(1,TH+'SharesOfCounts.lean','shares_of_counts','Exact conversion from coset counts to Frame.Shares.',
 'Derive the literal ratios 4/(3o+1) and 3/(3o+1), errors and nonemptiness from the selected counts, keeping the source normalization.')
target(1,TH+'topsFrame.lean','topsFrame','Frame-level application of the biased selection.',
 'Identify the actual finite additive frame, subgroup, relevant steps and weights with the preceding probabilistic theorem.')
target(1,TH+'topsBase.lean','topsBase','Actual host-scale top-selection statement.',
 'Check every large-scale numerical hypothesis and its common threshold before applying the frame selection.')
target(1,TH+'topsChoiceH.lean','topsChoiceH','General character-host selection interface.',
 'Match the selected TT, BadOK and Shares to the same host parameters; distinguish the general character host from an ordinary cyclic specialization.')

# HW closes the degree transport. These are the construction inputs it consumes.
target(2,AA+'ShortNorms/hostOfFieldOf.lean','hostOfFieldOf','Construct the actual host and replace its selected set.',
 'Expand ShortNorm, SmallOne, PairGood, FieldRows and HostParam.Seam inputs. At the chosen TT replacement, prove all HostAx and biased-share properties persist.')
target(2,AA+'CharacterBoxes/HostOfField.lean','hostOfField','General character-host family supplier.',
 'Treat the wrapper as navigation to hostOfFieldOf and its substantive arithmetic hypotheses, not as a proof of those hypotheses.')
target(2,AA+'CharacterBoxes/HostOfField.lean','supplyOfAdm','Actual admissible-host supply.',
 'Trace the admissibility assumptions to the simultaneous field, prime and host construction.')
target(2,AW+'AuxiliaryPrimeMemAvoidedPrimes.lean','HostExQW','Exact upstream host existence record consumed by HW.',
 'Supply the unbounded/interval scale windows and the host requirements with constants chosen in their literal order.')
target(2,AW+'ValidForConstructedPointClassesEventuallyWorking.lean','ObjCP','Point constructor for every admissible pair and distinguished position.',
 'Construct Val, HostArith, From, CanonInst and requested geometric duties uniformly; HW only uses this interface after the selected pair is fixed.')
target(2,AI+'ExistsObjectsOfAdmissibleTwistDatum.lean','objCP_and_of_recExP','Substantive assembly producing the actual point constructor.',
 'Expand the RecExP, level-prime, character/twist and led-part suppliers, preserving the exact all-pairs/all-positions quantifier order.')
target(2,AI+'ExistsObjectsOfAdmissibleTwistDatum.lean','objCP_of_recExP','Named output of the point-construction assembly.',
 'Use the preceding substantive construction; the final property combination is an assembly wrapper.')
target(2,AI+'SzRowNumAt.lean','szRow_numAt','Actual numerical record for the constructed point.',
 'Supply all NumAt fields from the actual host, Val and point data, beyond the GI/GII local numerical consequences already reconstructed.')

# BC closes the coefficient rings. The comparison objects must still be built.
target(3,IW+'ExistsGIs.lean','exists_trueVolume_stage_of_any_column_choice','Rebuild actual local group data while preserving the chosen global columns.',
 'Construct the stage using the chosen local family, and prove the transported column, forms, true-volume and Omega identities together.')
target(3,IW+'ExistsGIs.lean','nonempty_columnLocalData_of_standardConcreteFamily','Supply the concrete local records below the class wrappers.',
 'Prove nonemptiness from actual local identifications and comparisons, not from an assumed GroupCompatibilityAll record.')
target(3,IW+'IsRecGOfIsLocalFamily.lean','exists_isLocalFamily','Build the compatible local family.',
 'Supply the three substantive inputs: place/Frobenius identifications, integral away-characters and rank matching.')
target(3,IW+'IsRecGOfIsLocalFamily.lean','isRecG_of_isLocalFamily','Construct actual GroupCompatibilityAll.',
 'Check level-zero forms, local places, valuation maps and comparison-lattice identification for the same global witness.')
target(3,IW+'ExistsLocIdOfCompletions.lean','exists_locId_of_completions','Actual Frobenius-orbit and completion identifications.',
 'Identify all relevant number-field places, split completions and algebraic embeddings compatibly. BC2 already supplies the prescribed coefficient-place embedding.')
target(3,IW+'AddCharIsIntegral.lean','exists_psi','Integral away-from-p character.',
 'Construct the inverse away-character with unit-valued integral coefficients and the exact compatibility used in the local package.')
target(3,IW+'CharZeroOfSetting.lean','pack_d_eq','Actual local and archimedean dimension equality.',
 'Compare the local class-function dimension to the original column representation, not merely an abstract rank bound.')
target(3,AB+'Definitions/AutomorphicMembership/ExistsEmbeddingOfRingTie.lean','comparison_statements','Actual comparison-map lattice identity.',
 'Expand rational block identities, polynomial values, integral Weyl descent and saturation proving the O-span of the global integral lattice is the actual local M.')
target(3,LT+'GroupLattices/TiedFamilies/TieLatFin.lean','comparison_lattice_span_eq','Literal comparison-lattice target.',
 'Reconstruct its substantive rational-surjectivity and integral-intersection suppliers; scalar extension alone does not prove this target.')
target(3,LT+'GroupLattices/TiedFamilies/TieSurj.lean','surjRat_pf','Rational surjectivity in the comparison lattice.',
 'Prove the actual coordinate and lattice image statements used to pass from global polynomial values to the local representation.')
target(3,LT+'GroupLattices/TiedFamilies/FullTiedCBase.lean','groupCompatibilityOfRecursion','Five-field family assembly consumer.',
 'Use it after constructing level, forms, comparison and local group identifications. Its ring field is covered by BC, but its other premises must not be inferred from the wrapper.')

# Preserve the four independent global branches and their exact source leads.
for prior in old['targets']:
    if 'unchanged_global_branch_index' in prior:
        add(4,prior['path'],prior['source_spelling'],prior['role'],prior['remaining_human_scope'],
            prior.get('source_connections',()),branch=prior['unchanged_global_branch_index'])

public_files=[{k:v for k,v in info.items() if not k.startswith('_')} for info in files.values()]
result={
 'version':'0.11','commit':PIN,'head_verified':head,
 'status':'Continuation map only; all records distinguish proved implications from remaining construction tasks.',
 'target_count':len(targets),'source_file_count':len(files),
 'count_policy':'All exact target ranges, including the six retained leads for four independent global branches.',
 'line_range_convention':'Inclusive, one-indexed, exact original bytes.',
 'completed_previous_frontier':'GI/GII prove actual supplied-family local numerical hypotheses; BC finite coefficient extension/standard ring; GJ actual orbit application; GW global degree choice; HW active preselected-pair transport.',
 'next_local_priority':'Construct the biased character-coset top selection and Frame.Shares, actual host/point supplier and compatible local comparison objects for the same arithmetic family.',
 'priority_groups':{
   '1':'Biased finite top selection and exact coset shares.',
   '2':'Actual general-character host, point constructor and NumAt supply consumed by HW.',
   '3':'Actual local places, integral characters, rank equality and comparison lattices consumed by BC/GJ.',
   '4':'Unchanged independent global branches.'},
 'precision_notes':[
   'Per-good-orbit density is not abundance of good orbits.',
   'The actual host uses delta on A0 and 3delta/4 elsewhere; uniform-Bernoulli GII9–10 does not by itself give Frame.Shares.',
   'CoverAll is an optional stronger sufficient property. The active route preselects a pair and proves ChosenWall; HW reconstructs that transport.',
   'IsRecCEv is an optional sufficient identification. Active class routes construct GroupCompatibilityFamily and its comparison objects.',
   'StdSubAt is a standard coefficient-subring assertion. The finite coefficient-extension theorem is already proved in BC.',
   'Do not infer theta, spectral, metric, cohomological or simultaneous PairEx inputs from the finite local results.'
 ],
 'targets':targets,'source_files':public_files,
 'validation':{'all_source_bytes_equal_pinned_git_blobs':True,'all_declaration_anchors_and_inclusive_range_hashes_checked':True,
               'global_branch_records_identical_to_predecessor':True,'no_new_proof_claim_by_target_map':True,'no_lean_build_or_kernel_replay':True},
 'previous_global_branches_source':{'path':str(OLD_PATH.relative_to(BASE)),'sha256':sha256(OLD_PATH.read_bytes()).hexdigest()},
 'global_branches_unchanged':deepcopy(old['global_branches_unchanged'])
}
assert len({(t['path'],t['line_start'],t['line_end']) for t in targets})==len(targets)
assert len(result['global_branches_unchanged'])==4
(HERE/'next_source_targets.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'targets':len(targets),'source_files':len(files),'global_branches':4}))
'''
(B/'v0_11/build_next_targets.py').write_text(prefix+body)
print('Prepared v0_11/build_next_targets.py')
