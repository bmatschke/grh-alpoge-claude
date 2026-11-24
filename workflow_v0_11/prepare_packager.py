"""Generate the cumulative v0.11 packager from the prior verified workflow."""
from pathlib import Path
import json

B=Path(__file__).resolve().parents[1]
s=(B/'v0_10/package_checkpoint.py').read_text()
for old,new in [('0.10','__CURRENT_DOT__'),('0.9','0.10'),('__CURRENT_DOT__','0.11'),
                ('0_10','__CURRENT_UNDER__'),('0_9','0_10'),('__CURRENT_UNDER__','0_11')]:
    s=s.replace(old,new)
ledger=json.loads((B/'output/RH_reconstruction_v0_11/provenance.json').read_text())

def sub(old,new):
    global s
    assert old in s,old[:160]
    s=s.replace(old,new)
def block(start,end,new):
    global s
    a=s.index(start);b=s.index(end,a)
    s=s[:a]+new+s[b:]

block('COMPONENTS = {','\nMERGED_NAMES', '''COMPONENTS = {
    "GII": ("type_two_family", "main.tex", [f"GII{i}" for i in range(1,11)]),
    "GI": ("type_one_family", "main.tex", [f"GI{i}" for i in range(1,9)]),
    "BC": ("base_change", "main.tex", [f"BC{i}" for i in range(1,9)]),
    "GJ": ("family_join", "main.tex", [f"GJ{i}" for i in range(1,6)]),
    "GW": ("global_weight_choice", "main.tex", [f"GW{i}" for i in range(1,7)]),
    "HW": ("host_weight_join", "main.tex", [f"HW{i}" for i in range(1,4)]),
}
UPDATED_PRIOR_IDS = {"EA9", "TC6"}
EXPECTED_COUNTS = '''+repr({
    'old_claims':368,'claims':408,'new_claims':40,
    'old_source_files':890,'source_files':len(ledger['source_files']),
    'old_source_links':5817,'source_links':sum(len(c['sources']) for c in ledger['claims'])
})+'\n')
sub('Claim ID, for example RU8, RD15, HM12, TC6, or SW8.','Claim ID, for example GW5, HW2, GJ4, BC7, GI8, or TC6.')
sub('New IDs must be exactly RU11 + RD15 + HM12 + NP9 + TC6.',
    'New IDs must be exactly GII10 + GI8 + BC8 + GJ5 + GW6 + HW3.')
sub("('version_0_8_local_conclusion', 'version_0_10_local_conclusions')",
    "('version_0_8_local_conclusion', 'version_0_9_local_conclusions', 'version_0_10_local_conclusions')")

readme=r'''def make_readme(pages, starts, count):
    return f''' + "'''" + r'''RH AND DIRICHLET-GRH READABLE RECONSTRUCTION — VERSION 0.11
Prepared for Benjamin Matschke, 21 November 2026.

STATUS
This is a partial human reconstruction, not a completed independent proof
of RH or Dirichlet GRH. It preserves both completed supplied-data local
theorems and now proves the actual numerical family supply, finite
coefficient extension, orbit application and global degree selection.
Full arithmetic-family construction and four independent global branches
remain explicit. These are limits of this exposition, not assertions of
omitted arguments in the released source.

MAIN NOTE AND READING ORDER
RH_readable_reconstruction_v0_11.pdf is the cumulative {pages}-page note.
Its matching TeX source is included. Start with the route and analytic
argument, or go directly to the new application:

  GJ1–GJ5: actual family/orbit join, page {starts['GJ']}.
  GW1–GW6: one degree pair controlling all candidate primes, page {starts['GW']}.
  HW1–HW3: the active host preselection and fixed-pair family, page {starts['HW']}.
  GII1–GII10: actual Type-II family data and probability, page {starts['GII']}.
  GI1–GI8: actual Type-I family hypotheses and mean, page {starts['GI']}.
  BC1–BC8: standard coefficient ring and finite extension, page {starts['BC']}.

The shorter main sections are supported by complete expanded report.txt
companions in those six component directories. Each directory also has
a standalone source-ledger builder and declaration/range locators.

WHAT THE NEW PROOFS ESTABLISH
GII proves the actual per-good-orbit count, logarithmic windows and every
Type-II numerical inequality, including N1^2<=rN and the full Q^5 size
budget. Its probability argument proves uniform-Bernoulli BadProb and
existential TopsOK, with forced-point conditioning handled explicitly.
The actual host additionally needs biased coset selection and Frame.Shares;
uniform per-good-orbit density alone is not an abundance assertion.

GI proves all fourteen actual Type-I numerical fields, exact window and
forbidden-band translation, the actual cyclic predecessor/time bound,
and the canonical mean from the completed local theorem TC6. The fixed
coefficient vector is chosen before a single threshold uniform in all
family indices, primes and good representatives.

BC constructs the standard ring W(F_(q^2))[omega]/(omega^2-p), a finite
normalization and an embedding inducing the specified number-field place.
It proves integral coefficient-lattice, algebraic-dual, arbitrary clean
intersection and GoodRankK transport. LPprime extends with precisely the
same height t, depth D, deficit kappa and conductor c*. The image of omega
need not be a uniformizer in the larger ring. StdSubAt means a standard
coefficient SUBRING. The actual GroupCompatibilityFamily ring field is
one application; recC/IsRecCEv is another sufficient identification.

GJ proves attainment of the universal Type-I deficit infimum without
losing its ring/weight/target quantifiers. It obtains explicit uniform
scale bounds, identifies the actual cyclic orbits and weights, and proves
the literal OrbitLatticeBounds join for both prime ranges.

GW uses exact constant-fibre marginalization of the finite degree boxes.
The local mean bound E kappa_v<=Nv*x^-12 yields E Sigma_p<=m*|TT|*x^-12.
An elementary harmonic sum and the indicator bound give
  E Z <=8*x^(-9-gamma), gamma=1/2-(1453/150)eps>2447/7800.
For 32*x^-gamma<=1, one pair satisfies the exact source inequality
  sum_candidates (log p)/p * (2*1_(Sigma_p>x^-eps)+4*Sigma_p) <= x^-9.
The same pair is used at all primes; independence between primes is not
required. ChosenW transports it through every member carrying the pair.
Optional CoverAll gives a carrier, but it is not imposed on the active route.

HW follows that active route: transfer the point degree condition to host
WOK, preselect one pair, rebuild points at all distinguished positions
with that fixed pair, and pass through KitS/famOfKits to ChosenWall and
ChosenWS. The upstream host and point constructors, numerical supply at
that construction, and biased Frame.Shares remain explicit premises.

PRESERVED LOCAL ENDPOINTS
Type I: TC6 proves literal HypI=>Conclusion2 for C0>=880, CH>=2800001,
C=302114. Type II: EA9 proves literal Hyps=>ConclusionE for C>=4129,
with cloud constants (10,54,1088). The sufficient constants are not
claimed optimal. Their original proofs and ledgers are unchanged.

SOURCE AND BACKTRACKING
Repository: https://github.com/CocoSgt/riemann-hypothesis-lean
Pinned commit: 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
Current ledger: {count['claims']} stable claims, {count['source_links']}
source links, {count['source_files']} indexed primary source files.
There are 40 new claims: GII10+GI8+BC8+GJ5+GW6+HW3.

Every source record has its qualified declaration, inclusive original
line range, pinned URL, full-file SHA256 and range SHA256. The current
component builders compare source bytes with the pinned Git blobs.
provenance.json is authoritative; provenance.txt is its readable view.
source_index.json records the full-file hashes. The explicit mathematical
dependency graph is acyclic; it is not a Lean transitive dependency audit.

Examples after unpacking, with a local pinned source checkout:
  python backtrack.py GW5
  python backtrack.py HW2 --repo /path/to/riemann-hypothesis-lean
  python backtrack.py BC7 --repo /path/to/riemann-hypothesis-lean --entry 1
  python backtrack.py --check-all --repo /path/to/riemann-hypothesis-lean
The read-only helper works without network access and can resolve every
historical ID, its newer annotations, and the current continuation ranges.

CONTINUITY
All 368 prior claim fields/source arrays, all 890 prior source-file
records and every prior mathematical dependency edge are preserved.
Only version_0_11_update annotations are appended to EA9 and TC6.
Every predecessor file is byte-identical at its original package path or
under history/version_0_10/. Exactly twelve superseded root files are
archived there, including the v0.10 note and checkpoint. Earlier histories
and all earlier source locators remain included.

NEXT WORK
The concrete next targets are in next_source_targets.json and the
continuation checkpoint. They prioritize actual host construction with
biased Frame.Shares, the underlying local-place/character/rank/comparison
data, and the remaining gain/prime-loss estimates. They distinguish
active constructors from wrappers and optional sufficient interfaces.
The same four independent branches remain: actual theta/spectral kernels,
dimension/metric/discarded-target control, congruence/cohomological windows,
and simultaneous PairEx plus the centered prime-sum window theorem.

VERIFICATION AND LIMITS
The mathematical cross-reviews, exact-source checks, historical-preservation
checks, PDF visual review and package checksums are recorded. visual_qa.json
names the exact reviewed PDF by SHA256. Every PDF page was rendered and
visually reviewed. SHA256SUMS covers every package file except itself.
No Lean source was modified; no full Lean build or independent kernel replay
was run. This package makes no new public verification-status assertion.
''' + "'''" + '\n\n'
block('def make_readme(', 'def main():', readme)
sub("require(next_doc.get('target_count') == len(target_records) == 24,\n            'The current next-source map must contain exactly 24 declared ranges.')",
    "require(next_doc.get('target_count') == len(target_records) and len(target_records)>=8,\n            'The current next-source map range count is inconsistent.')")
sub("require(next_doc.get('source_file_count') == len(target_paths) == 12,\n            'The current next-source map must contain exactly 12 source files.')",
    "require(next_doc.get('source_file_count') == len(target_paths),\n            'The current next-source map file count is inconsistent.')")
sub("require(conclusions['constants']['C0_min'] == 880 and\n            conclusions['constants']['TM'] == 2800001 and\n            conclusions['constants']['C'] == 302114,",
    "require(ledger['version_0_10_local_conclusions']['constants']['C0_min'] == 880 and\n            ledger['version_0_10_local_conclusions']['constants']['TM'] == 2800001 and\n            ledger['version_0_10_local_conclusions']['constants']['C'] == 302114,")
sub("    plan += [(pdf_path, Path(pdf_path.name), 'main'),", "    for source in sorted((BASE/'v0_11').glob('next_*_targets.txt')):\n        plan.append((source,Path('workflow_v0_11')/source.name,'workflow'))\n    plan += [(pdf_path, Path(pdf_path.name), 'main'),")

block('    results = [','    count = {', '''    results = [
        'GII1–GII10: exact per-good-orbit counts, logarithmic window bounds, every Type-II numerical field and local application; conditional BadProb and existential uniform-Bernoulli TopsOK.',
        'GI1–GI8: every actual Type-I numerical field, uniform HypIAt, exact band/window/depth comparison, cyclic predecessor and height, and canonical mean.',
        'BC1–BC8: actual standard coefficient ring, prescribed-place finite normalization, exact integral/dual/clean lattice transfer, LPBaseChange and StdSubAt for identified constructions.',
        'GJ1–GJ5: universal canonical infimum attainment, explicit uniform scale bounds, actual cyclic and weight identifications, exact OrbitLatticeBounds join.',
        'GW1–GW6: exact local/global finite marginal averages, one simultaneous degree choice with WReq<=x^-9, ChosenW and optional full-coverage realization.',
        'HW1–HW3: active point-to-host WReq/WOK transfer, fixed-pair/all-position rebuilding, and transport to ChosenWall/ChosenWS without CoverAll.',
    ]
    remaining = [
        'Construct the actual host and full point/family data simultaneously: biased coset top selection and Frame.Shares, the point construction for admissible degrees, and the associated numerical and analytic/arithmetic duties. HW proves their preselected-pair transport without assuming optional CoverAll.',
        'Construct the underlying compatible local place identifications, integral away-characters, exact rank matching and global-to-local comparison-lattice span. BC proves coefficient extension, GJ the orbit application; supplied GroupCompatibilityFamily data must still be realized with the rest of the construction.',
        *previous['remaining_major_inputs'][2:],
    ]
    additions = [
        'All prior precision constraints remain as historical records; current v0.11 annotations supersede the numerical-family and finite-extension boundaries only to the extent explicitly proved.',
        'GI/GII prove numerical and geometric implications for the actual supplied family fields, with constants before one uniform threshold, then family index, candidate prime and good representative.',
        'Scale.A is 26; the Type-I averaging width is x^13. Global chain length m_ch=D.R.m differs from local m=k-1.',
        'Per-good-orbit top density is separate from abundance of good orbits. GII9–10 use uniform Bernoulli selection; the actual host uses biased coset probabilities and the separate Frame.Shares property.',
        'StdSubAt means a standard coefficient subring. BC constructs it rather than assuming an arbitrary Hida DVR has the doubled residue field.',
        'Finite extension preserves the source W, q, Frobenius and edge set. The image of omega^2=p need not be a uniformizer; height/depth/conductor use its actual powers and p-normalization, without an extra ramification multiplier.',
        'The universal Type-I infimum is attained after fixing each ring, weight and target. Witnesses may vary; no uniform bound on representation dimensions or interchange of infimum and universal quantifiers is assumed.',
        'GW marginalization uses exact constant-size restriction fibres. Independence across primes is not required. The selected pair bounds a weighted exceptional set, not every prime separately.',
        'CoverAll is a separate optional sufficient property. The active HW route preselects a pair, then rebuilds all distinguished positions and supplies ChosenWall; it does not require CoverAll for the final family.',
        'IsRecCEv is an optional sufficient identification. Active linked-family routes construct GroupCompatibilityFamily through local places, characters, dimensions and comparison-lattice data.',
        'All 368 prior claim fields/source arrays, 890 prior source-file records and every old dependency graph entry remain unchanged. Current annotations do not overwrite historical claims.',
    ]
    supersessions = list(previous.get('precision_supersessions', []))
    for historical in previous['precision_constraints']:
        if ('StdSubAt/LPBaseChange' in historical or 'Global abundance and compatibility' in historical):
            supersessions.append({
                'previous_checkpoint_version':'0.10','historical_statement':historical,
                'current_statement':'GI/GII supply the actual numerical-family implications; BC proves the standard-subring and finite-extension arguments; GJ proves the exact orbit join; GW/HW prove degree selection and active transport. Full host/local-comparison/family construction remains separate.',
                'completed_by':['GI5','GI8','GII7','GII8','BC7','BC8','GJ4','GW5','HW3'],
            })
''')
sub("'status': 'Partial RH/Dirichlet-GRH human reconstruction. Both local types are now complete under supplied literal data: Type I by TC6 (C0>=880, CH>=2800001, C=302114), and unchanged Type II by EA9 (C>=4129). Global family existence, finite-place base change, spectral/metric and cohomological-window inputs remain.',",
    "'status':'Partial RH/Dirichlet-GRH reconstruction. Actual supplied-family numerical hypotheses, finite coefficient extension, orbit application, one global degree selection and active host/family transport are proved. Full joint construction and independent global branches remain.',")
sub("'Distinguish the actual global HypIAt/HypIIAt family supply and finite-place StdSubAt/LPBaseChange from the completed local HypI/Hyps constructions and HM12 RS-isomorphism invariance.',",
    "'Construct the actual biased top/frame data and underlying local comparison objects; preserve the distinction between the active HW preselection route and optional CoverAll/IsRecCEv interfaces.',")
sub("'All 315 prior claim fields/source arrays and 764 prior source-file records are preserved; version histories only append new annotations.'",
    "'All 368 prior claim fields/source arrays and 890 prior source-file records are preserved; version histories only append new annotations.'")
sub("'Independent records cover RU matching and HH lattice assembly, RD tails and density, HM harmonic/cloud and ring transport, NP numerical constants, TC primitive retraction/Smith/Weyl/tensor/GoodRankK, and the final GoodShare/D0/exceptional-function joins. Review JSON source metadata and its builders are included.'",
    "'Independent records cover GI numerical and exact local translation, GII numerical/probability/selection bounds, BC finite normalization and integral/dual/rank transfer, GJ universal infimum and orbit join, GW finite averaging and family transport, and HW actual preselection/rebuilding quantifiers.'")
sub("'Historical component bytes and source arrays are preserved. The current main and version_0_11_update complete supplied-data local Type I. Global family, finite-extension, metric and arithmetic-window inputs remain. Superseded root files are archived under history/version_0_10/.'",
    "'Historical component bytes and source arrays are preserved. Current v0.11 supplies actual family numerics, finite coefficient extension, orbit application and global degree selection/transport. Full joint construction and independent global inputs remain. Superseded root files are archived under history/version_0_10/.'")
(B/'v0_11/package_checkpoint.py').write_text(s)
print('Prepared v0_11/package_checkpoint.py')
