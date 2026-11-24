#!/usr/bin/env python3
"""Rebuild the v0.42 quantitative component records from pinned source bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PIN = '7cbf7a0c32fca1badf05931879a37c3f8a2b03b4'
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--source', type=Path, required=True)
args = ap.parse_args()
source = args.source.resolve()
assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == PIN

def sha(b):
    return hashlib.sha256(b).hexdigest()

FIVE = 'src/Formalism/SharpRestriction/GlobalTheoremInputs.lean'
NUM = 'src/Formalism/LocalToGlobal/GlobalTheory/IrreducibleOfCountSizes.lean'
PROOF = 'src/Formalism/LocalToGlobal/GlobalTheory/ConcNP.lean'
ROW = 'src/Formalism/SharpRestriction/LevelLetterCocycles/ArithmeticCylinders.lean'
FRAME = 'src/Formalism/SharpRestriction/GlobalSchurBounds/QuadraticLogDerivCongr.lean'
GI = 'src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/'
groups = {
    'N': [(FIVE,40,48,'LinkN_at; LinkN'),
          ('src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/LinkNAlongFamilyOfLocalBounds.lean',11,17,'GlobalTheory.LinkFam.main'),
          ('src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkNFam.lean',35,63,'CutGivesAlt; linkN_of_twGood_galoisPreconditions; linkN_of_boundAtTwoThree_slot')],
    'IRR': [(FIVE,55,58,'LinkIRR'), (NUM,56,78,'Wg; epsC; SizesAt; WeightNumbersBound; EpsilonBoundLargeX'),
            (NUM,180,199,'DstarE; CountAllRows; WeightAllRows; FamilyIrreducibleOfCountWeightSizes'),
            (ROW,245,275,'AllRows; dimT; LabelCountGoodInjective'),
            (ROW,355,361,'goodAt; locShare'),
            ('src/Formalism/SharpRestriction/CuspSpanNormBounds/GlobAut.lean',203,207,'vol; Dstar'),
            (PROOF,130,338,'weight_numbers_bound; epsilon_bound_large_x'),
            (PROOF,509,657,'delp_of_allRows; link_irreducible_all_rows; linkIRR_of_allRows'),
            (GI+'LinkIRROfJoinEx.lean',17,38,'linkIRR_of_join_ex'),
            (GI+'LinkIRROfJoinEx.lean',143,166,'link_irr')],
    'DIV': [(FIVE,66,96,'BesselId; LinkDIV_at; LinkDIV; LinkDIVt'),
            ('src/Formalism/LocalRingCardinality/DataParams₂.lean',218,235,'Fo; Ga; Ee; logOm; La; B0; Nc; MAIN'),
            (GI+'LinkBrest.lean',7,25,'link_brest'),
            (GI+'WireSel.lean',11,41,'wire_sel')],
    'G': [(FIVE,101,141,'flG; rG; leastPowerExponent; loG; LinkG_at; LinkG'),
          (GI+'LinkG.lean',14,27,'link_g'),
          ('src/Formalism/LocalToGlobal/GroupLattices/LinkGConcreteNoKer.lean',36,58,'linkG_concrete; linkG_concrete_noKer; linkG_concrete5')],
    'S': [(FIVE,143,157,'hsDiagFull; LinkS_at; GamOf; LinkS'),
          (GI+'LinkAlt.lean',16,50,'link_alt'),
          (FRAME,188,197,'Frame_at'), (FRAME,258,261,'FrameF'),
          ('src/Formalism/SharpRestriction/GlobalSchurBounds/LossesSmallShares.lean',464,467,'LinkGLOBAL7')],
}

inventory = {}
records = {}
excerpt = []
for group, ranges in groups.items():
    records[group] = []
    for ix, (path, start, end, decl) in enumerate(ranges, 1):
        b = (source/path).read_bytes()
        blob = subprocess.check_output(['git', '-C', str(source), 'show', f'{PIN}:{path}'])
        assert b == blob, path
        lines = b.splitlines(keepends=True)
        assert 1 <= start <= end <= len(lines), (path, start, end, len(lines))
        part = b''.join(lines[start-1:end])
        rec = dict(id=f'GQT_{group}_{ix:02}',path=path,declaration=decl,line_start=start,line_end=end,
                   sha256=sha(b),file_sha256=sha(b),range_sha256=sha(part),range_bytes=len(part),
                   source_commit=PIN,verified_equal_to_pinned_git_blob=True,
                   url=f'https://github.com/CocoSgt/riemann-hypothesis-lean/blob/{PIN}/{path}#L{start}-L{end}')
        inventory[path] = dict(path=path,sha256=sha(b),bytes=len(b),line_count=len(lines),verified_equal_to_pinned_git_blob=True)
        records[group].append(rec)
        excerpt.append(f'[{rec["id"]}] {path}:{start}-{end}\nSHA256 {rec["range_sha256"]}\n{part.decode()}\n')

tex = (HERE/'main.tex').read_bytes()
t = tex.decode()
titles = {
 'GQT1':'Finite union estimate with three relative counting tests',
 'GQT2':'Actual row labels and bad-cylinder identification; smaller sufficient count contract',
 'GQT3':'Uniform elementary bound for the exact Wg envelope',
 'GQT4':'Uniform absorption to the exact stretched-exponential retained defect',
 'GQT5':'Original conditional linkIRR_of_allRows and its sufficient three-test replacement',
 'GQT6':'Polynomial spectral error suffices for the original all-height FrameF',
 'GQT7':'Replacement spectrum feeds the selected original numerical consequent',
}
deps = {'GQT1':[],'GQT2':['GQT1'],'GQT3':[],'GQT4':['GQT2','GQT3'],
        'GQT5':['GQT2','GQT3','GQT4'], 'GQT6':['GF8','GFA6','GFA7','GFA8'],
        'GQT7':['GQT6','GFI6','GFI7','GFI8','GFI9','GFI10','GFI11','GFI12','GFI13','GFI15']}
hyp = {
 'GQT1':['One finite row set; exact good-complement description; positive reference mass; uniform relative counting error below one; two nonnegative local shares.'],
 'GQT2':['Original AllRows, LabelCountGoodInjective, exact eT_one identity, CountAllRows and WeightAllRows, or the displayed three-test/two-weight restrictions on that same object.'],
 'GQT3':['Fixed 0 < theta <= 1 and Cs; original SizesAt inequalities for all later tuples.'],
 'GQT4':['Original count error exp(-c N f log N), c>0; both SizesAt tuples; the actual finite-counting/weight conclusion of GQT2.'],
 'GQT5':['One original FamP; eventual original AllRows witnesses, label identification, count and weight estimates, and SizesRec with one fixed Cs and c>0.'],
 'GQT6':['Fixed CH>0 and C0>=1; actual normalized operators; original proviso and code; actual full positive-rank source lattices and Bessel/height/rank identifications; LinkIRR; full LinkDIV; source discard <=2f/b and f<=x^5; one uniform threshold for eta0,eta1,sqrt(e0)<=x^(-CH)/16.'],
 'GQT7':['Every remaining hypothesis of GFI15 on the same family, with original exponential LinkS replaced by GQT6 exact normalized estimates and uniform polynomial rate.'],
}
claims = []
for cid,title in titles.items():
    a = t.index('% BEGIN '+cid)
    b = t.index('% END '+cid)+len('% END '+cid)
    block=t[a:b]
    gs=['IRR'] if int(cid[3:])<=5 else ['S']
    srcs=[r for g in gs for r in records[g]]
    claims.append(dict(id=cid,title=title,introduced_in='0.42',classification='B',
        status='complete human proof at the printed conditional scope',depends_on=deps[cid],
        original_hypotheses=hyp[cid],hypotheses_retained=hyp[cid],classical_inputs=[],
        proof_location=dict(file='global_quantitative_v42/main.tex',label='claim:'+cid,
            line_start=t[:a].count('\n')+1,line_end=t[:b].count('\n')+1,sha256=sha(block.encode()),bytes=len(block.encode())),
        source_groups=gs,sources=srcs,
        dependency_scope='Original objects and displayed conditional inputs; no arithmetic/spectral input-producing theorem is inferred from source correctness.'))

oldrecords=json.loads((HERE.parent/'dependency_audit_v0_41/remaining_leaf_register.json').read_text())['records'][:5]
tasks={
 'GLOBAL_DENOMINATOR': [
   ('N1','Produce original NormChoiceFacts, GaloisPreconditions and Tie4 on one common family; retain the same host/sha datum.','open_C'),
   ('N2','Prove the actual local scalar/killing table, uniform Extra constants C,CT and the two/three-place bounds; construct ConclF.','open_C'),
   ('N3','Verify actual admissibility, orbit valuation sum, local-to-global weights, and exact dZ0; export guarded LinkN.','open_C'),
   ('N4','Retain cut descent and row-multiplicity/rank comparisons if using the Alt source route.','open_C')],
 'GLOBAL_RETAINED_DEFECT': [
   ('I1','Construct actual AllRows and exact LabelCountGoodInjective, including common source, Haar measures, labels and retained image.','open_C'),
   ('I2','Prove total and two bad-cylinder counts with a common relative error at most 1/2; full CountAllRows is sufficient but stronger.','open_C'),
   ('I3','Prove nonnegative actual local weights and Wg bound for the two actual finite bad-label sets; full WeightAllRows is sufficient but stronger.','open_C'),
   ('I4','Finite union, exact original delp identification, Wg numerical domination and uniform absorption.','complete_GQT1_GQT5')],
 'GLOBAL_PERIOD_HEIGHT': [
   ('D1','Construct the common rational target and original BesselId, one target isometry before all words, nonzero word scalars, original coefficient embedding.','open_C'),
   ('D2','Prove the actual all-embedding norm/eigenvalue estimates for the period-chain maps and target metric; obtain htMap<=h.','open_C'),
   ('D3','Prove the actual mean/slope/divisor comparison with MAIN and exponent Cabs; preserve LinkEta and DIVinN antecedents.','open_C'),
   ('D4','Prove the per-lift finite-place E comparison and cross-word h+A_T log T comparison with one constant.','open_C'),
   ('D5','Obtain full target lattice, ZeroAbove, and uniform sFrame+muMax(RR)<=x^CH b on the same data; join TuSize,DGamSize and parameter order.','open_C')],
 'GLOBAL_LOCAL_GAIN': [
   ('G1','Construct actual GroupCompatibilityFamily and admissible tops on the common selected family.','open_C'),
   ('G2','Reconstruct source SecondTheoremReduced and the invoked local extremal-projector, lattice/flatness and numerical comparison results.','open_C'),
   ('G3','Supply actual valuation inclusion, lenMN bound and zero-unserved clause away from the type prime, exact gain bounds and local von Mangoldt lower estimate.','open_C'),
   ('G4','Prove served-orbit coverage, MeanKappaBound and one subexponential bo=b^rho(x), rho->0, before indices.','open_C')],
 'GLOBAL_SPECTRAL': [
   ('S1','Construct exact normalized period expansion and actual source/target spaces; ensure original Gamma and proviso.','open_C'),
   ('S2','Prove zero-determinant, nongeneric, loop and generic term estimates; Fourier/derivative bounds and arithmetic kernel/mass normalizations.','open_C'),
   ('S3','Prove the independent all-point count giving Dall/Dstar on the same normalized target.','open_C'),
   ('S4','Join exact errors uniformly and either obtain original exp(-x^(eps/8)) rate or GQT6 polynomial sufficient rate at each chosen CH.','open_C'),
   ('S5','Original normalized bounds with polynomial error <=x^(-CH)/16 imply FrameF and the final selected numerical consequent.','complete_GQT6_GQT7')],
}
sourcekey={'GLOBAL_DENOMINATOR':'N','GLOBAL_RETAINED_DEFECT':'IRR','GLOBAL_PERIOD_HEIGHT':'DIV','GLOBAL_LOCAL_GAIN':'G','GLOBAL_SPECTRAL':'S'}
contracts=[]
for old in oldrecords:
    ident=old['id']; group=sourcekey[ident]
    contracts.append(dict(id=ident,classification='C',status='open_original_contract',scope='shared RH and unrestricted Dirichlet GRH',
        baseline_contract=old['contract'],objects_and_bindings_retained=old['bindings'],
        exact_sources=records[group],
        proof_tasks=[dict(id=i,target=t,status=s) for i,t,s in tasks[ident]],
        whole_obligation_closed=False))

main_contract=json.loads(json.dumps(contracts,ensure_ascii=False))
for rec in main_contract:
    rec['exact_original_contract_text']='\n'.join(
        b''.join((source/r['path']).read_bytes().splitlines(keepends=True)[r['line_start']-1:r['line_end']]).decode()
        for r in rec['exact_sources'] if r['path']==FIVE)

inherit=[]
for name,cids in [('gram_frame/gram_frame_section.tex',['GF8']),
                  ('global_assembly/main.tex',['GFA6','GFA7','GFA8','GFA9']),
                  ('global_final_installation/main.tex',['GFI6','GFI7','GFI8','GFI9','GFI10','GFI11','GFI12','GFI13','GFI15'])]:
    b=(HERE.parent/name).read_bytes()
    inherit.append(dict(file=name,sha256=sha(b),claims=cids,role='inherited written proof; exact scope retained'))

provenance=dict(schema='rh-human-component-provenance/1',artifact_version='0.42',date='2026-11-23',
    source_commit=PIN,component='global_quantitative_v42',main_tex_sha256=sha(tex),proof_file_sha256=sha(tex),
    claims=claims,source_groups=records,source_inventory=list(inventory.values()),source_files=list(inventory),
    inherited_proof_inputs=inherit,published_applications=[],
    scope_note='Conditional quantitative reconstruction and sufficient replacements; original five C leaves remain open. No Lean build or kernel replay.',
    builder=dict(file='build_metadata.py',sha256=sha(Path(__file__).read_bytes())),
    validation=dict(source_checkout_pin_verified=True,all_source_bytes_compared_to_pinned_git_blobs=True,claim_blocks=7,whole_leaf_closures=0))

outputs={
 'provenance.json':provenance,
 'contracts.json':dict(schema='rh-global-quantitative-contracts-v1',artifact_version='0.42',source_commit=PIN,contracts=main_contract,
                      warning='Task decomposition is not a sufficient-graph refinement assertion; completed conditional substeps do not close the whole contracts.'),
 'source_manifest.json':dict(source_commit=PIN,source_files=list(inventory.values()),ranges=records,verified_against_git=True),
 'closure.json':dict(component='global_quantitative_v42',artifact_version='0.42',new_claims=list(titles),new_claim_count=7,
                    completed_conditional_endpoint='ConcN.linkIRR_of_allRows on original AllRows/label/count/weight/size inputs',
                    sufficient_replacements=['Three counting tests and two actual bad-weight estimates suffice for LinkIRR.',
                                             'Uniform eta0,eta1,sqrt(e0)<=x^(-CH)/16 suffices for the selected FrameF and ChainTied consumer.'],
                    original_spectral_endpoint_completed=False,whole_obligation_closures=[],
                    remaining_global_contract_ids=list(tasks),no_new_published_application=True,no_lean_replay=True)
}
for name,value in outputs.items():
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
(HERE/'source_excerpts.txt').write_text('\n'.join(excerpt))
print(json.dumps(dict(claims=len(claims),source_files=len(inventory),source_ranges=sum(map(len,records.values())),whole_leaf_closures=0),indent=2))
