#!/usr/bin/env python3
"""Record actual patching/selected Raw closure and the exact remaining producers."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
components=["patched_ring","patched_support","coefficient_normalization","selected_core","comparison_packet"]
read=lambda p:json.loads(p.read_text())
claims={n:[c["id"] for c in read(ROOT/n/"provenance.json")["claims"]] for n in components}
allnew=sum(claims.values(),[])
old=read(ROOT/"history/version_0_39/provenance.json")
old_count=len(old["claims"])
span=lambda n:claims[n][0]+"–"+claims[n][-1]
new=[
 span("patched_ring")+": the full original rrEx and rmapsEx are reconstructed. The actual universal determinant and constrained character rings, complete coproduct, five-part tuple, ordered finite free splitting target, section, every rho_N and pi are constructed over the original O. Chenevier representability is applied through condition F, including ell=3,n=4; no factorial inversion or coefficient flatness is assumed.",
 span("patched_support")+": the full original S5 and the actual patched module are reconstructed. The original finite modules, every level, exact comparison maps, six approximate-annihilator families and common exponent give the one-ultrafilter inverse-limit module. The support, dimension, augmentation-fiber and move fields are proved on the actual completion. Full piKer, piSurj and the exact annihilator equivalence with the same J are supplied.",
 span("coefficient_normalization")+": full Core=>CoreBC is reconstructed using the actual finite free unramified O', literal Til ring and added Unit variable. Every residual, Pair, TWBase/TWRing/TWMaps/TWAut, point/kernel and finite-chain field is checked. Closed relations commute by fixed finite support and coefficient extraction; semisimplicity descends by a scalar functional without an extra finite-dimensional premise. A restricted h=0,a=n,g=0 consumer is explicit.",
 span("selected_core")+": the selected normalized Core and original Raw endpoint are complete at h=0,a=n=4,k.g=0. The actual quotient determinant, OoPair/ooMaps, point lift with prescribed kernel and all OoPt fields are supplied. One splitting prime serves both endpoints and the same completion. CRW's full-block cotangent bound forces the support ideal to be zero; the exact annihilator comparison gives original J-containment. BCN/PQL normalize and descend without changing the final point or quantifiers.",
 span("comparison_packet")+": the full original exists_pkT, rowPk_nonempty and exists_moved with Copy/Coh are reconstructed from their original given-data premises. One finite catalogue, both ChT, complete LfT, exact lattices, metrics, measures, period coordinates and all-place RrT are retained. One numerical record is chosen before every eta and later V/S/N/G. Full ReadL still requires the original eta agreement, and initial geometry/Fits/tests remain upstream.",
 f"There are {old_count+len(allnew)} cumulative human proof claims, with {len(allnew)} new claims. No whole selected compound leaf closes: 33 remain, classified as 22 C, 9 B and 2 D. The entire selected Raw patching/normalization/descent dependency is now closed under its original arithmetic antecedents. The human RH/Dirichlet-GRH reconstruction remains incomplete."
]
remaining=[
 "Construct the original ordinary/control/separating arithmetic fibers and type/neatU/TThetaEx data, the four Hida endpoints and all-level same-J TWAut/HasAut on both original rank-four Links. Preserve full CohP/LocCFT/N4, prime 3, fixed iota, nontrivial residual cyclotomic character and one common coefficient threshold. Selected Raw itself is now reconstructed and must not be relisted as an open producer.",
 "Construct one actual common recursive/geometric member with its original Inputs/Pins/Holds/ExAt/InGeo and required CoreP duties. PKT now produces the full comparison packet, RowPk and fitting-stage Moved/Copy/Coh from given data; RDR gives Side0/ReadPk/pins. Supply actual Fits/division/central compatibility and exact o.eta=q.eta for full ReadL on the same R/F.",
 "Complete primitive RatG/LiftTestB rational tests and actual base rows, host/frame fields, MultEq nonzero-part support, the original stored nonzero chain and group tie, eigensystem/carrier/parts and all-embedding logLam, HD/d3b and NEb. The stronger second DivRows3 theta square remains separate. Original row-pair integrability and first DivDef3 are already reconstructed.",
 "Construct actual NBuilt/NdSpec and the original local projection square on that common installation. Supply denominator, retained-defect, period-height, local-gain and normalized spectral estimates on the same family, with original spectra, ideals, embeddings, metrics and measures.",
 "Construct the compatible second-layer selector and all its duties, preserving the shared family/Bundle/BWit/BunU/FamGLmin inputs and original simultaneous eventual thresholds.",
 "Finish original Cases I/II/V for RH and two-primary targets. Unrestricted Dirichlet targets additionally retain CaseIII, SeedIV and original rank-four chain propagation/descent. The selected one-point Raw completion does not supply these other arithmetic branches.",
 "Resolve the two D-class human source-interface questions AD_VANISH_K_MATCH and HOST_RIGID_S. These are gaps in the present source understanding, not alleged defects in the checked Lean proof. The optional AQ route remains optional and historical RF16 remains governed by DEX11."
]
priority=(
 "Prioritize original ordinary/control/type data and four Hida endpoints leading to all-level same-J TWAut/HasAut on both rank-four Links. "
 "The selected h=0,a=n=4,k.g=0 Raw producer is now complete: reuse LIM/PRG/PMS/SCI with BCN/PQL; do not divert this route into general NonssT or arbitrary-chain Core. "
 "In parallel construct one actual common geometric member, its primitive rational tests/Fits and exact eta agreement; PKT/RDR now supply the comparison, moved and reader algorithms on original inputs. "
 "Local installation/common estimates and compatible second-layer selection remain shared final-theorem producers. "
 "Retain original shared objects, prime 3, fixed iota, same J, metrics/measures and one common coefficient threshold."
)
cnt=claims["patched_ring"]+claims["patched_support"]+claims["coefficient_normalization"]+claims["selected_core"]
pkt=claims["comparison_packet"]
updates={
 "JSP11":(cnt,"The selected Raw producer now has every actual limiting ring, map, module, support, point, normalization and descent supplier. Original ordinary/type, four Hida endpoints and all-level same-J HasAut remain."),
 "CRW18":(claims["selected_core"],"The full-block cotangent dimension result is applied to actual PMS support in SCI12: a full-dimensional support prime is zero, so the support ideal vanishes."),
 "CRW19":(claims["selected_core"],"The support/prime argument is now installed on one exact splitting prime and the actual ordinary point, yielding same-J containment without a general NonssT comparison."),
 "CRW20":(cnt,"All actual normalized Core suppliers are constructed in PRG/PMS/SCI. SCI12 proves the selected normalized Core, and SCI13 with BCN/PQL proves the selected original Raw."),
 "CRW21":(cnt,"The selected Raw branch is now closed under original TWAut antecedents; its current upstream work is ordinary/control/type/Hida/HasAut, not limiting patching or coefficient normalization."),
 "CFO21":(cnt,"The same coupled B1/B2 point data now feed the actual selected Raw proof, with one C before m and the original eventual N sets. No arbitrary-Kap assertion is added."),
 "QX10":(cnt,"Both Links retain ell=3, fixed iota and the common coefficient threshold. The selected support consumer is complete; actual ordinary/automorphic systems still have to be produced."),
 "LIM19":(cnt,"The actual full Lim is now joined to actual RRObj/RMaps/PMod/S5 and selected Core/Raw, preserving its one ultrafilter and all local maps."),
 "PQL21":(claims["coefficient_normalization"]+claims["selected_core"],"Coefficient normalization/Unit and selected normalized patching are now supplied. The original selected Raw conclusion follows with the final B,J,K,f and Selmer quantifiers unchanged."),
 "RDR22":(pkt,"Original PkT/RowPk/Moved/Copy/Coh suppliers are now constructed on given geometry and Fits; full ReadL retains eta agreement and actual outer common-member/test duties."),
 "CSR15":(pkt,"The comparison and fitting-stage copy constructors are now supplied with exact maps, metrics, periods and one numeric record. Initial common geometry, rational tests, eta agreement and remaining family duties stay upstream."),
 "BTH12":(pkt,"The initial extension remains closed; PKT/RDR now construct comparison, moved and reader packets on given original data. Actual common geometry, Fits/rational tests, eta agreement and base rows remain."),
 "DI21":(pkt,"First division's original analytic premise is already discharged, and comparison/moved suppliers now exist on original given inputs. Stronger second DivRows3 and original nonzero-chain/group-tie premises remain."),
 "DA1":(allnew,"All selected logical edges and ten final input interfaces are retained. Five components supply 124 new claims, including complete selected Raw and full given-data comparison constructors; 33 whole compound leaves remain."),
 "GH7":(allnew,"RH retains I/II/V and unrestricted Dirichlet GRH additionally III. The selected Raw patching/descent and common comparison algorithms are complete in their original scopes; full final-theorem suppliers remain.")
}
assert set(updates)<={c["id"] for c in old["claims"]}
cfg=dict(artifact_version="0.40",date="2026-11-22",predecessor_version="0.39",predecessor_claim_count=old_count,
 components=components,expected_new_claims=len(allnew),component_claims=claims,
 scope="Partial human reconstruction of RH and Dirichlet GRH, accepting the Alpoge–Claude Lean proof as fully checked and correct. Version 0.40 completes the actual universal patching rings/maps, full S5 and actual module, coefficient normalization, selected one-point full-block Core/Raw, and original given-data comparison/RowPk/Moved constructors. Original arithmetic and common geometric/quantitative producers remain. No Lean replay is claimed.",
 new_in_this_version=new,remaining_major_inputs=remaining,next_local_priority=priority,
 claim_updates={k:dict(supplied_by=v[0],statement=v[1],scope="Additive scope update; every predecessor field, source array and claim edge remains.") for k,v in updates.items()},
 precision_notes=[
 "A: checked published application; B: independent elementary/moderate argument; C: substantial reconstruction; D: unresolved human source understanding, not a formal error allegation.",
 "PRG uses Chenevier's condition-F representability alternative, with actual profinite/continuity/residual hypotheses and explicit relative O construction. ell=3,n=4 is allowed; no n! inversion or assumed flat coefficient change.",
 "PMS constructs the actual all-level patched module, paired quotient maps and six annihilator families on one ultrafilter. Full S5 includes exact fiber, dimension and move clauses. piKer/piSurj and the annihilator comparison retain original J.",
 "BCN proves full Core=>CoreBC and its restricted selected consumer. The actual finite free unramified coefficient extension and literal added Unit variable preserve all point/Kap/B1/B2 data. Closed-ideal transport uses fixed finite support, and semisimple-ring descent needs no finite-dimensional assumption.",
 "SCI supplies actual ooDet/OoPair/ooMaps/OoPt. Its Chenevier 2.22(ii) application is henselian, Cayley-Hamilton and split multiplicity free with rank-one residual blocks. The subsequent full-kernel argument is integral.",
 "SCI uses one splitting prime for both endpoint lifts, the point map kernel and the completion. The selected a=n,g=0 cotangent bound forces a full-dimensional support prime and then the support ideal to vanish. No general NonssT or multi-point move is needed for this selected conclusion.",
 "Selected normalized Core and selected Raw are complete at h=0,a=n=4,k.g=0 under their original arithmetic TWAut antecedents. This does not prove arbitrary-chain Core, a universal Kap theorem, Sel1=0, four Hida endpoints or original HasAut existence.",
 "PKT proves full original exists_pkT, rowPk_nonempty and exists_moved with Copy/Coh. It preserves exact integral lattices and all metric/measure/period constants and chooses one Nums record before every eta/V/S/N/G.",
 "The LfT theta field is the original conditional extension clause; it does not supply a new extension witness. Full ReadL still requires exact o.eta=q.eta at every original row/place.",
 "Actual initial common Inputs/Pins/Holds/ExAt/InGeo, Fits/rational tests, eta agreement, nonzero chain/group tie, remaining host/parts/NEb and stronger second DivRows3 remain distinct upstream tasks.",
 "All 245 historical compound targets in 107 groups and all 121 selected nodes with 161 edges remain. No new whole selected leaf closes; 33=22C+9B+2D is a scope register, not a completion percentage.",
 "Every predecessor proof/source/edge and historical interface cut is preserved. The v0.40 audit and explicit additive updates govern older frontier statements. Historical RF16 remains governed by DEX11.",
 "No PDF or Lean replay. Draft TeX validates syntax/references; independent mathematical reviews bind every new claim and the current audit to released bytes."
 ])
(ROOT/"increment_v0_40.json").write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+"\n")
print("Configured",len(allnew),"new claims;",old_count+len(allnew),"cumulative.")
