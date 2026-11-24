#!/usr/bin/env python3
"""Build CS claim/source ledger from the pinned checkout, without network calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

COMMIT = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
REPO_URL = "https://github.com/CocoSgt/riemann-hypothesis-lean"
IW = "src/Formalism/SharpRestriction/GrowthBounds/IntegralWeylLatticeSpan/"
CMP = "src/Formalism/LocalToGlobal/GroupLattices/ComparisonMaps/"
TIE = "src/Formalism/LocalToGlobal/GroupLattices/TiedFamilies/"
ODD = "src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/OddDualWeylJacobian/"

CLAIMS = [
    ("CS1", "Exact contraction of polynomial spans through a valuation ring", "Derived simplification, proved by finite valuation-pivot elimination; no finite-extension hypothesis", [], [
        (IW+"CoreDesc.lean", "exists_pivot"),
        (IW+"CoreDesc.lean", "desc_main"),
        (IW+"CoreDesc.lean", "descVal"),
    ]),
    ("CS2", "Integral Weyl generators, odd inverse-transpose duality and exact coefficient descent", "Proved in the actual characteristic-zero setting; Delta is not replaced by Nabla", ["CS1"], [
        (IW+"WeylEqSpanInt.lean", "weyl_eq_span_int"),
        ("src/Formalism/PeriodIntegrals/OddDualWeyl.lean", "OddFact"),
        (ODD+"HighestWeightDualOf.lean", "highestWeightDual_of"),
        (ODD+"OddDualWeylFactorization.lean", "odd_dual_weyl_factorization"),
        (IW+"WeylLatticeDescentOfIntegralModels.lean", "OddId"),
        (IW+"WeylLatticeDescentOfIntegralModels.lean", "oddZ"),
        (IW+"RowActWeylMemDescentLattice.lean", "htupW_eq"),
        (IW+"RowActWeylMemDescentLattice.lean", "mem_htupW_iff"),
        (IW+"WeylLatticeDescentOfIntegralModels.lean", "weylLatticeDescent_of_valuation"),
        (IW+"WeylLatticeDescentHolds.lean", "weylLatticeDescent_holds"),
    ]),
    ("CS3", "Actual local bases, self-dual Gram units and parity-correct column spans", "Proved for supplied Forms0/Joint0 and the same common global frame and LI places", ["SF1", "SF6", "LI5", "LI6"], [
        ("src/Formalism/LocalToGlobal/HermitianForms/IsLocBasis.lean", "IsLocBasis"),
        ("src/Formalism/LocalToGlobal/GlobalTheory/GL6/PBwLocGen.lean", "exists_isLocBasis"),
        (IW+"SelfDualCongr.lean", "loc_facts"),
        (IW+"GramInvIntV.lean", "gram_intV"),
        (IW+"GramInvIntV.lean", "gramInv_intV"),
        (IW+"GramInvIntV.lean", "lat_of_int"),
        (IW+"SelfDualCongr.lean", "restLatW_of"),
        (IW+"SelfDualCongr.lean", "restGramW_of"),
        (IW+"ColSpanMulUnit.lean", "colSpan_mul_unit"),
        (IW+"ColSpanMulUnit.lean", "latO_of"),
        (IW+"ColSpanMulUnit.lean", "restLatO_of"),
        (IW+"ColSpanMulUnit.lean", "restExB"),
    ]),
    ("CS4", "ValIntRec from polynomial-value existence and unit level characters", "Proved implication, retaining ValEx and supplied Forms0/Joint0/LevelZeroCharacterRational", ["CS2", "CS3", "LI8"], [
        (IW+"IntSpanGSmul.lean", "valIntAt_of"),
        (IW+"IntSpanGSmul.lean", "valIntRec_of"),
        (IW+"ColSpanMulUnit.lean", "unitsW_of_pow"),
        (IW+"ColSpanMulUnit.lean", "restChi_of"),
    ]),
    ("CS5", "The local integrality criterion equals the actual localized global lattice", "Proved from supplied all-place lattice characterization and actual point/class joins", ["CS4"], [
        (CMP+"ExistsPrimeToLe.lean", "exists_prime_to_le"),
        (CMP+"ExistsPrimeToLe.lean", "locWBack_proved"),
        (CMP+"ExistsPrimeToLe.lean", "locWCrit_proved"),
        (CMP+"CmpCMemMIff.lean", "cmpC_mem_M_iff"),
        (TIE+"TieLat.lean", "cmpRec_lat_pf"),
    ]),
    ("CS6", "Weak approximation gives a single global matrix with exactly the required local lattices", "Derived number-field CRT proof of WeakApprox/RatTup, with exact integral equality", ["LI5"], [
        (TIE+"TieWeak.lean", "adic_dense"),
        (TIE+"TieWeak.lean", "adic_dist"),
        (TIE+"TieWeak.lean", "weak_of_locAt"),
        (TIE+"TieWeak.lean", "weakRec_pf"),
        (CMP+"MRatSpanOfWeak.lean", "approx_local"),
        (CMP+"MRatSpanOfWeak.lean", "ratTup_of_weak"),
    ]),
    ("CS7", "Rational integral invariant values span the actual finite-orbit module", "Proved by rational lattice bases, saturation over the coefficient DVR and orbit extension; no stabilizer averaging", ["CS2", "CS6", "LI8"], [
        (CMP+"MRatSpanOfRatInv.lean", "span_inv"),
        (CMP+"MRatSpanOfRatInv.lean", "inv_span"),
        (CMP+"MRatSpanOfRatInv.lean", "mRatSpan_of_rat_inv"),
        (CMP+"HRatInvOfTriv.lean", "jdI_mem"),
        (CMP+"HRatInvOfTriv.lean", "jdI_decomp"),
        (CMP+"HRatInvOfTriv.lean", "mRatSpan_inv"),
        (TIE+"TieLat.lean", "mRatSpan_rec"),
    ]),
    ("CS8", "Actual rank match and rational-value descent give rational surjectivity", "Proved using both the supplied emb_basis/Fi_zero bridge and CR6, retaining polynomial-value existence", ["CS5", "CR6"], [
        (TIE+"TieSurj.lean", "card_eq_d"),
        (CMP+"FramesTr.lean", "cmpC_inj"),
        (CMP+"FramesTr.lean", "cmpC_li"),
        (CMP+"YvRatOfValRat.lean", "rat_mem"),
        (TIE+"TieDim.lean", "mem_span_of_card"),
        (TIE+"TieSurj.lean", "surjRat_pf"),
    ]),
    ("CS9", "Exact integral comparison-lattice span for the compatible source data", "Proved from CmpCore/GatIs with ValIntRec supplied by CS1--CS4; global forms and ValEx supply remains", ["CS5", "CS7", "CS8"], [
        (CMP+"SpanImageOfSurj.lean", "span_image_of_surj"),
        (TIE+"TieLatFin.lean", "m_finite_rec"),
        (TIE+"TieLatFin.lean", "comparison_lattice_span_eq"),
        (TIE+"TieLat.lean", "CmpCore"),
        (TIE+"TiePtRec.lean", "sameUloc_of_joint"),
        ("src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ExistsEmbeddingOfRingTie.lean", "comparison_statements"),
    ]),
]

NEXT = [
    (TIE+"TieExC.lean", "ex_C_blk", "Reconstruct the actual polynomial-value supplier for the same recC data: block rationality plus Forms0, common B, SameUloc and LevelZeroCharacterRational imply ValEx. SameUloc follows directly from supplied Joint0; do not make it an independent missing theorem."),
    (CMP+"NatActRVtupR.lean", "valEx_of_rep'", "Prove the generic representative/value gluing with its exact adelic extension and point uniqueness hypotheses; reconstruct coefficient-field block rationality and invariance so the chosen polynomial realizes every representative, not only one chosen point."),
    ("src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ExistsStandardFormComparisonSymmetricLevelMember.lean", "formsTiedSym_std", "Construct the simultaneous actual FormsTiedSym/StdF/StdLvC objects, finite charts, common global-level data and CharacterCompatible statement under the literal true-column Ok/Pins/Laws/Later assumptions. SF proves common-frame lattice consequences, and CS proves comparison algebra, without constructing this stronger package."),
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2]/'lean-source')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    args=ap.parse_args()
    repo=args.repo.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
    if head != COMMIT: raise ValueError(('wrong source commit',head))
    cache={}; sources={}
    def entry(path,name):
        if path not in cache:
            raw=(repo/path).read_bytes()
            blob=subprocess.check_output(['git','-C',str(repo),'show',COMMIT+':'+path])
            if raw != blob: raise ValueError(('working-tree divergence',path))
            cache[path]=raw
            sources[path]={'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'line_count':len(raw.splitlines()),'verified_equal_to_pinned_git_blob':True}
        raw=cache[path];lines=raw.splitlines(keepends=True)
        pattern=re.compile(r'^(?:private\s+)?(?:theorem|lemma|def|abbrev|structure)\s+'+re.escape(name)+r'(?=\s|\{|\(|:)')
        hits=[i for i,l in enumerate(lines) if pattern.match(l.decode())]
        if len(hits)!=1: raise ValueError((path,name,hits))
        start=hits[0];end=start+1
        boundary=re.compile(r'^(?:(?:private\s+)?(?:theorem|lemma|def|abbrev|structure)\s|end(?:\s|$)|namespace\s|section\s|variable\s|attribute\s|set_option\s|include\s|open\s)')
        while end<len(lines) and not boundary.match(lines[end].decode()): end+=1
        while end>start+1 and not lines[end-1].strip():end-=1
        segment=b''.join(lines[start:end]);sha=sources[path]['sha256']
        return {'path':path,'declaration':name,'line_start':start+1,'line_end':end,'sha256':sha,'full_file_sha256':sha,'range_sha256':hashlib.sha256(segment).hexdigest(),'range_bytes':len(segment),'url':f'{REPO_URL}/blob/{COMMIT}/{path}#L{start+1}-L{end}','pinned_url':f'{REPO_URL}/blob/{COMMIT}/{path}#L{start+1}-L{end}','first_line':lines[start].decode().rstrip(),'declaration_lines_within_range':[start+1],'verified_equal_to_pinned_git_blob':True}
    claims=[]
    for cid,title,status,deps,ss in CLAIMS:
        claims.append({'id':cid,'title':title,'status':status,'introduced_in':'0.13','component_ledger':'comparison_span/provenance.json','dependencies':deps,'sources':[entry(*x) for x in ss]})
    targets=[]
    for p,n,scope in NEXT:
        t=entry(p,n);t.update({'priority_group':1,'role':'Remaining compatible global forms/value supplier','remaining_human_scope':scope,'human_status':'continuation_target_only; no additional proved claim'})
        targets.append(t)
    ledger={'schema':'RH-readable-component-v1','artifact_version':'0.13','component':'comparison_span','repository':REPO_URL,'commit':COMMIT,'head_verified':head,'scope':'CS1--CS9, exact integral comparison for supplied compatible forms/value data','claims':claims,'source_files':list(sources.values()),'mathematical_dependency_edges':[[d,c['id']] for c in claims for d in c['dependencies']],'input_boundaries':['Supplied true-column and Forms0/rational-forms packages, including their all-place lattice characterization and emb_basis/Fi_zero dimension bridge.','ValEx (CmpCore.ex) remains a substantive supplied polynomial-value condition; exact suppliers are recorded in next_targets.json.','Joint0 and LevelZeroCharacterRational retain their global supplier status. SameUloc is Joint0.Uloc_eq once Joint0 is supplied.','GatIs supplies the actual local models; CR6 supplies their rank equality.','No metric/isometric transport, theta kernel, cohomological window or prime-window theorem is claimed.'],'precision_notes':['HtupW uses integral Weyl Delta, not naive Htup/Nabla; no equality of those lattices is asserted.','Odd local weight is lambda* and its coordinate matrix is inverse transpose; LI conjugation parity changes this to inverse conjugate transpose.','Valuation descent uses finite support and a valuation pivot, not a finite coefficient extension.','The L-linear retraction K -> L need not preserve O; integrality follows separately from the exact localized-lattice criterion.','CR6 matches rank_O M to dim_C Mu0; emb_basis and Fi_zero provide the additional global L-dimension equality.','Local rational spanning includes stabilizer invariants through saturation, with no division by stabilizer order.','The final equality is integral, with no discarded finite index.'],'validation':{'all_current_source_bytes_equal_pinned_git_blob':True,'claim_count':len(claims),'source_links':sum(len(c['sources']) for c in claims),'source_file_count':len(sources),'lean_build_run':False,'kernel_replay_run':False}}
    out.joinpath('provenance.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
    out.joinpath('next_targets.json').write_text(json.dumps({'version':'0.13','commit':COMMIT,'targets':targets},indent=2,ensure_ascii=False)+'\n')
    out.joinpath('source_locators.txt').write_text('\n\n'.join(c['id']+' '+c['title']+'\n'+'\n'.join(f"  {s['path']}:{s['line_start']}-{s['line_end']} {s['declaration']}\n  {s['url']}\n  file_sha256={s['sha256']} range_sha256={s['range_sha256']}" for s in c['sources']) for c in claims)+'\n')
    print(json.dumps(ledger['validation'],indent=2))
    print('next_targets',len(targets))

if __name__=='__main__': main()
