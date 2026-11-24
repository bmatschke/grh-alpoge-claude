"""Prepare the cumulative v0.11 merger, preserving all historical fields."""
from pathlib import Path

B=Path(__file__).resolve().parents[1]
s=(B/'v0_10/merge_provenance.py').read_text()
for old,new in [('0.10','__CURRENT_DOT__'),('0.9','0.10'),('__CURRENT_DOT__','0.11'),
                ('0_10','__CURRENT_UNDER__'),('0_9','0_10'),('__CURRENT_UNDER__','0_11')]:
    s=s.replace(old,new)

def sub(old,new):
    global s
    assert old in s,old[:120]
    s=s.replace(old,new)

a=s.index('COMPONENTS = [')
b=s.index('\n\n\ndef digest',a)
s=s[:a]+'''COMPONENTS = [
    ("type_two_family","GII",1,10,"main.tex"),
    ("type_one_family","GI",1,8,"main.tex"),
    ("base_change","BC",1,8,"main.tex"),
    ("family_join","GJ",1,5,"main.tex"),
    ("global_weight_choice","GW",1,6,"main.tex"),
    ("host_weight_join","HW",1,3,"main.tex"),
]
''' +s[b:]
sub('assert len(old["claims"]) == 315','assert len(old["claims"]) == 368')
sub('assert len(old["source_files"]) == 764','assert len(old["source_files"]) == 890')
sub('(?:def|abbrev|theorem|lemma|structure|class|inductive)\\s+(?:',
    '(?:def|abbrev|theorem|lemma|structure|class|inductive|instance)\\s+(?:_root_\\.)?(?:')

a=s.index('REMAINS = [')
b=s.index('\ncomponent_inputs, artifact_inputs',a)
s=s[:a]+'''REMAINS = [
    "Construct one arithmetic host/family with the biased top selection, Frame.Shares, fixed selected degrees, local comparison data and all stated size fields simultaneously. Optional CoverAll is distinguished from the active preselected-weight/ChosenWall route.",
    "Actual theta/common-image and spectral/arithmetic-kernel identities, metric transport and discarded target control.",
    "Congruence denominators, cohomological windows, PairEx prime selection and the final uniform centered prime-sum argument.",
]
UPDATES = {"EA9":["GII7","GII8","BC7","BC8","GJ4"],
           "TC6":["GI5","GI8","GJ1","BC7","BC8","GJ4","GW5"]}
for c in claims:
    if c["id"] in UPDATES:
        c["version_0_11_update"] = {
            "status":"actual_family_numerical_supply_and_finite_place_application_reconstructed",
            "explanation":"GI/GII prove the actual local hypothesis records uniformly for supplied FamP data; BC proves the concrete standard ring and finite coefficient extension; GJ gives the exact orbit application; GW selects one global degree pair with WReq. Full simultaneous arithmetic-family existence remains separate.",
            "discharged_by":UPDATES[c["id"]],
            "separate_remaining_work":REMAINS,
            "scope":"These are supplied-family implications and explicit local/finite selections, not a complete RH or Dirichlet-GRH proof. The active preselected-weight realization and optional CoverAll route are kept distinct.",
        }
''' +s[b:]
sub('assert len(ids)==len(set(ids))==368','assert len(ids)==len(set(ids))==408')
sub('assert sum(new_counts.values())==53','assert sum(new_counts.values())==40')
a=s.index('boundaries=deepcopy(old["component_input_boundaries"])')
b=s.index('\ncounts={',a)
s=s[:a]+'''boundaries=deepcopy(old["component_input_boundaries"])
complete="Both local constructions remain complete under their literal data. GI/GII now prove the actual numerical family supply and BC/GJ the finite-place application under the stated construction identifications. Full simultaneous arithmetic-family existence remains separate."
boundaries.update({
    "GI":"All fourteen actual Type-I numerical fields, band/window/depth translation, time comparison, canonical mean and uniform HypIAt are proved for supplied FamP data.",
    "GII":"Per-good-orbit counts, uniform Type-II numerics and adm6 are proved. Uniform Bernoulli selection supplies an existential TopsOK subset; the actual host uses an additional biased selection and Frame.Shares construction.",
    "BC":"The concrete standard coefficient ring, prescribed-place finite extension and exact LPBaseChange are proved. recC gives StdSubAt; IsRecCEv is one sufficient interface, not the only family construction route.",
    "GJ":"Universal infimum attainment, uniform scales, orbit identifications and exact OrbitLatticeBounds are proved under the stated actual family identifications.",
    "GW":"MeanKappaBound, exact marginal averaging, MeanEx/WReq and ChosenW are proved. Optional CoverAll supplies ChosenWS; active preselected-weight realization is treated separately in HW.",
    "HW":"The active point/host/fixed-pair family transport is reconstructed with its upstream host and point-existence hypotheses explicit; optional CoverAll is not imposed on the full proof.",
})
''' +s[b:]
sub('"new_claims":53','"new_claims":40')
a=s.index('conclusion={')
b=s.index('\nledger={',a)
s=s[:a]+'''conclusion={
    "local_Type_I":old["version_0_10_local_conclusions"]["local_Type_I"],
    "local_Type_II":old["version_0_10_local_conclusions"]["local_Type_II"],
    "actual_family_supply":"GI5/GII7 prove eventual uniform HypIAt/HypIIAt, with explicit fixed coefficient requirements and exact actual windows and bands.",
    "finite_places":"BC7 proves LPBaseChange without changing height, depth, deficit or conductor; BC8 proves StdSubAt for recC and identified concrete constructions.",
    "orbit_application":"GJ4 yields literal OrbitLatticeBounds with the actual orbit coordinates and dominant weights.",
    "global_degree_choice":"GW5 selects one admissible pair with exact WReq<=x^-9. GW6 proves ChosenW and the optional CoverAll realization. HW follows the active preselected-weight host/family route.",
    "selection_scope":"GII9/GII10 prove uniform Bernoulli BadProb/TopsOK. The actual host additionally needs biased coset probabilities and Frame.Shares, kept as a construction boundary.",
    "remaining_inputs":REMAINS,
}
''' +s[b:]
sub('"scope":"Partial human RH/Dirichlet-GRH reconstruction. Both complete local Type-I and Type-II constructions are proved under literal supplied hypotheses; global arithmetic, spectral, metric and cohomological work remains.",',
    '"scope":"Partial human RH/Dirichlet-GRH reconstruction. Both local constructions, actual supplied-family numerical hypotheses, finite coefficient extension, orbit application and global degree averaging are proved; full arithmetic-family construction and independent global branches remain.",')
sub('"version_0_11_local_conclusions":conclusion,','"version_0_11_local_conclusions":conclusion,')
sub('"Read version_0_11_update for completed local Type-I applications; historical fields and source arrays are preserved.",',
    '"Read version_0_11_update for the actual numerical family supply and finite-place application; historical fields and source arrays are preserved.",')
sub('"53 new claims: RU11 + RD15 + HM12 + NP9 + TC6.",','"40 new claims: GII10 + GI8 + BC8 + GJ5 + GW6 + HW3.",')
sub('range(3,11)','range(3,12)')
(B/'v0_11/merge_provenance.py').write_text(s)
print('Prepared v0_11/merge_provenance.py')
